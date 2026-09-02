#!/usr/bin/env python3
"""
TASB Policy Online <-> TEA AskTED crosswalk, v2.

Adds on top of v1 (requests-based, dedup-by-CDN):
  1. Filters out TEA rows that are not real locally-governed ISDs, despite
     being tagged Organization SubType=INDEPENDENT in AskTED (state
     university lab schools, the Windham School District [TDCJ], etc.) -
     these have no elected local board and should never be force-matched.
  2. County-suffix disambiguation: TASB disambiguates same-named districts
     with a "<Name> ISD-<County> County" suffix. Strip that suffix and
     match on (base name, county) against TEA's separate County Name field.
  3. A small abbreviation-expansion table, applied to both sides before
     normalizing, for the mismatches found in the v1 run (FT/MT/CO/CONS/
     DEPT/ED/MSD, plus a couple of one-off full-name aliases).

Everything that doesn't clear an explicit rule stays unmatched rather than
being fuzzy-guessed - a wrong CDN<->key mapping is worse than a gap.
"""

import argparse
import csv
import html
import re
import time
from collections import defaultdict
from pathlib import Path

import requests
from bs4 import BeautifulSoup

TASB_URL = "https://pol.tasb.org/PolicyOnline?key={key}"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# TEA rows tagged INDEPENDENT in AskTED that are not locally-elected ISDs.
NON_ISD_NAME_PATTERNS = [
    r"^UNIVERSITY OF\b",
    r"\bUNIVERSITY$",
    r"^TEXAS TECH UNIVERSITY\b",
    r"^TEXAS A&M .* UNIVERSITY\b",
    r"^WINDHAM SCHOOL DISTRICT$",  # TDCJ (prison system) school district - no elected board
    r"^TEXAS ACADEMY OF LEADERSHIP\b",  # university-chartered academy, not an ISD
]

# Token-level abbreviation expansion, applied after tokenizing on spaces.
TOKEN_EXPANSIONS = {
    "FT": "FORT",
    "MT": "MOUNT",
    "CO": "COUNTY",
    "CONS": "CONSOLIDATED",
    "DEPT": "DEPARTMENT",
    "ED": "EDUCATION",
}

# One-off full-name aliases that don't reduce to a token rule cleanly.
NAME_ALIASES = {
    "SCHERTZ CIBOLO U CITY ISD": "SCHERTZ CIBOLO UNIVERSAL CITY ISD",
    "WEST RUSK COUNTY CONSOLIDATED ISD": "WEST RUSK COUNTY CISD",
    "STAFFORD MSD": "STAFFORD MUNICIPAL SCHOOL DISTRICT",
}

COUNTY_SUFFIX_RE = re.compile(r"^(.*?)\s*-\s*([A-Za-z.\s]+?)\s+COUNTY$", re.I)


def normalize_name(value: str, expand: bool = False) -> str:
    if not value:
        return ""
    value = html.unescape(value)
    value = value.upper().strip()
    value = re.sub(r"[’'`]", "", value)
    value = re.sub(r"[-–—_/.,()]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()

    if value in NAME_ALIASES:
        value = NAME_ALIASES[value]

    if expand:
        tokens = [TOKEN_EXPANSIONS.get(t, t) for t in value.split(" ")]
        value = " ".join(tokens)

    return value


def is_real_isd(name: str) -> bool:
    upper = name.upper()
    return not any(re.search(pat, upper) for pat in NON_ISD_NAME_PATTERNS)


def find_column(fieldnames, candidates):
    lookup = {f.strip().lower(): f for f in fieldnames}
    for candidate in candidates:
        if candidate.lower() in lookup:
            return lookup[candidate.lower()]
    return None


def load_tea_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        name_col = find_column(reader.fieldnames, ["District Name", "District", "Organization Name", "Organization"])
        cdn_col = find_column(reader.fieldnames, ["District Number", "District #", "District ID", "CDN", "County District Number"])
        type_col = find_column(reader.fieldnames, ["District Type", "Organization SubType", "Organization Type", "Type"])
        county_col = find_column(reader.fieldnames, ["County Name", "County"])

        if not name_col or not cdn_col:
            raise RuntimeError(f"Cannot find name/CDN column. Columns: {reader.fieldnames}")

        by_cdn = {}
        excluded_non_isd = []
        for row in reader:
            district_name = (row.get(name_col) or "").strip()
            cdn = (row.get(cdn_col) or "").strip()
            if not district_name or not cdn:
                continue
            digits = re.sub(r"\D", "", cdn)
            if digits:
                cdn = digits.zfill(6)

            if type_col and type_col.lower().startswith("organization subtype"):
                subtype = (row.get(type_col) or "").strip().upper()
                if subtype and subtype != "INDEPENDENT":
                    continue

            if not is_real_isd(district_name):
                excluded_non_isd.append({"cdn": cdn, "district_name": district_name})
                continue

            county = (row.get(county_col) or "").strip() if county_col else ""
            county = re.sub(r"\s+COUNTY$", "", county.upper()).strip()

            by_cdn[cdn] = {
                "cdn": cdn,
                "district_name": district_name,
                "district_type": (row.get(type_col) or "").strip() if type_col else "",
                "county": county,
                "normalized_name": normalize_name(district_name),
                "normalized_name_expanded": normalize_name(district_name, expand=True),
            }

    rows = list(by_cdn.values())
    by_name = defaultdict(list)
    by_name_expanded = defaultdict(list)
    by_name_county = defaultdict(list)
    for record in rows:
        by_name[record["normalized_name"]].append(record)
        by_name_expanded[record["normalized_name_expanded"]].append(record)
        by_name_county[(record["normalized_name_expanded"], record["county"])].append(record)

    return rows, by_name, by_name_expanded, by_name_county, excluded_non_isd


def extract_tasb_name(page_html: str, browser_title: str):
    soup = BeautifulSoup(page_html, "html.parser")
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(" ", strip=True)
        if not text:
            continue
        m = re.match(r"^Welcome\s+to\s+(.+?)$", text, flags=re.I)
        if m:
            return m.group(1).strip()

    title = browser_title.strip()
    if title:
        for pattern in [r"\s+Board Policy Manual\s*-\s*Policy Online\s*$", r"\s*-\s*Policy Online\s*$", r"\s*\|\s*Policy Online\s*$"]:
            title = re.sub(pattern, "", title, flags=re.I).strip()
        if title and title.lower() != "policy online" and "error" not in title.lower():
            return title
    return None


def get_title(soup: BeautifulSoup) -> str:
    t = soup.find("title")
    return t.get_text(strip=True) if t else ""


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def try_match(tasb_name, by_name, by_name_expanded, by_name_county):
    """Return (record_or_None, method, ambiguous_bool)."""
    normalized = normalize_name(tasb_name)

    # 1. Exact normalized match.
    candidates = by_name.get(normalized, [])
    if len(candidates) == 1:
        return candidates[0], "exact_normalized_name", False
    if len(candidates) > 1:
        return None, "exact_normalized_name", True

    # 2. County-suffix disambiguation: "Base Name-County County".
    m = COUNTY_SUFFIX_RE.match(tasb_name.strip())
    if m:
        base, county = m.group(1), m.group(2)
        base_norm = normalize_name(base, expand=True)
        county_norm = county.strip().upper()
        candidates = by_name_county.get((base_norm, county_norm), [])
        if len(candidates) == 1:
            return candidates[0], "county_suffix_disambiguation", False
        if len(candidates) > 1:
            return None, "county_suffix_disambiguation", True

    # 3. Abbreviation-expanded match (no county suffix involved).
    expanded = normalize_name(tasb_name, expand=True)
    candidates = by_name_expanded.get(expanded, [])
    if len(candidates) == 1:
        return candidates[0], "abbreviation_expanded_name", False
    if len(candidates) > 1:
        return None, "abbreviation_expanded_name", True

    return None, None, False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("askted_csv", type=Path)
    parser.add_argument("--start-key", type=int, default=90)
    parser.add_argument("--end-key", type=int, default=1300)
    parser.add_argument("--delay", type=float, default=0.15)
    parser.add_argument("--out-dir", type=Path, default=Path("."))
    args = parser.parse_args()

    tea_rows, by_name, by_name_expanded, by_name_county, excluded_non_isd = load_tea_csv(args.askted_csv)
    print(f"Loaded {len(tea_rows):,} TEA ISD records (deduped by CDN).")
    print(f"Excluded {len(excluded_non_isd):,} non-ISD records tagged INDEPENDENT in AskTED: "
          f"{[r['district_name'] for r in excluded_non_isd]}")

    session = requests.Session()
    session.headers.update({"User-Agent": UA})

    matched = []
    unmatched_tasb = []
    matched_cdns = set()

    total = args.end_key - args.start_key + 1
    for index, key in enumerate(range(args.start_key, args.end_key + 1), start=1):
        url = TASB_URL.format(key=key)
        try:
            resp = session.get(url, timeout=20, allow_redirects=False)
            status = resp.status_code

            if status in (301, 302, 303, 307, 308):
                print(f"[{index:4}/{total}] {key}: redirect ({status}) -> skip")
                time.sleep(args.delay)
                continue
            if status != 200:
                print(f"[{index:4}/{total}] {key}: HTTP {status}")
                time.sleep(args.delay)
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            browser_title = get_title(soup)
            tasb_name = extract_tasb_name(resp.text, browser_title)

            if not tasb_name:
                print(f"[{index:4}/{total}] {key}: no district name")
                time.sleep(args.delay)
                continue

            record, method, ambiguous = try_match(tasb_name, by_name, by_name_expanded, by_name_county)

            if record:
                matched.append({
                    "tasb_key": key,
                    "tasb_name": tasb_name,
                    "tea_cdn": record["cdn"],
                    "tea_district_name": record["district_name"],
                    "district_type": record["district_type"],
                    "match_method": method,
                    "tasb_url": url,
                })
                matched_cdns.add(record["cdn"])
                print(f"[{index:4}/{total}] {key:4} -> {record['cdn']} {record['district_name']} ({method})")
            elif ambiguous:
                unmatched_tasb.append({"tasb_key": key, "tasb_name": tasb_name, "reason": f"ambiguous_{method}", "tasb_url": url})
                print(f"[{index:4}/{total}] {key:4} AMBIGUOUS {tasb_name}")
            else:
                unmatched_tasb.append({"tasb_key": key, "tasb_name": tasb_name, "reason": "no_match", "tasb_url": url})
                print(f"[{index:4}/{total}] {key:4} TASB only: {tasb_name}")

        except Exception as exc:
            print(f"[{index:4}/{total}] {key}: ERROR {exc}")

        time.sleep(args.delay)

    unmatched_tea = [
        {"tea_cdn": tea["cdn"], "tea_district_name": tea["district_name"], "district_type": tea["district_type"]}
        for tea in tea_rows if tea["cdn"] not in matched_cdns
    ]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "tasb_tea_crosswalk.csv", matched, ["tasb_key", "tasb_name", "tea_cdn", "tea_district_name", "district_type", "match_method", "tasb_url"])
    write_csv(args.out_dir / "tasb_unmatched.csv", unmatched_tasb, ["tasb_key", "tasb_name", "reason", "tasb_url"])
    write_csv(args.out_dir / "tea_unmatched.csv", unmatched_tea, ["tea_cdn", "tea_district_name", "district_type"])
    write_csv(args.out_dir / "tea_excluded_non_isd.csv", excluded_non_isd, ["cdn", "district_name"])

    print()
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Matched:            {len(matched):,}")
    print(f"TASB unmatched:     {len(unmatched_tasb):,}")
    print(f"TEA unmatched:      {len(unmatched_tea):,}")
    print(f"TEA excluded (non-ISD): {len(excluded_non_isd):,}")


if __name__ == "__main__":
    main()
