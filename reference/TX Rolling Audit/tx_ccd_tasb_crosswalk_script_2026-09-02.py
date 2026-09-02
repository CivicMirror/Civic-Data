#!/usr/bin/env python3
"""
TASB Policy Online <-> THECB community college district crosswalk.

Adapted from tx_isd_tasb_tea_crosswalk_script_2026-08-23.py's key-scanning
approach (see issue #13) for issue #14's ~50 CCDs. Reads
tx_ccd_thecb_enumeration_2026-09-02.csv (this repo's canonical 50-district
list, derived from the THECB almanac with TSTC/Lamar State/Lamar Institute
excluded as state-governed, non-locally-elected institutions) and scans
TASB Policy Online keys for a name match.

Usage: python3 tx_ccd_tasb_crosswalk_script_2026-09-02.py --start-key 1 --end-key 1400 --out-dir .
"""
import argparse
import csv
import html
import re
import time
import unicodedata
from pathlib import Path

import requests
from bs4 import BeautifulSoup

TASB_URL = "https://pol.tasb.org/PolicyOnline?key={key}"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

STRIP_SUFFIXES = [
    "COMMUNITY COLLEGE DISTRICT", "COUNTY COMMUNITY COLLEGE DISTRICT",
    "COUNTY JUNIOR COLLEGE DISTRICT", "JUNIOR COLLEGE DISTRICT",
    "COLLEGE DISTRICT", "COMMUNITY COLLEGE", "JUNIOR COLLEGE",
    "COLLEGE SYSTEM", "COLLEGE",
]


def normalize_name(value: str) -> str:
    if not value:
        return ""
    value = html.unescape(value)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.upper().strip()
    value = re.sub(r"[’'`]", "", value)
    value = re.sub(r"[-–—_/.,()]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    for suf in STRIP_SUFFIXES:
        if value.endswith(" " + suf):
            value = value[: -(len(suf) + 1)].strip()
            break
    return value


def get_title(soup: BeautifulSoup) -> str:
    t = soup.find("title")
    return t.get_text(strip=True) if t else ""


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


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ccd-csv", type=Path, default=Path(__file__).parent / "tx_ccd_thecb_enumeration_2026-09-02.csv")
    parser.add_argument("--start-key", type=int, default=1)
    parser.add_argument("--end-key", type=int, default=1400)
    parser.add_argument("--delay", type=float, default=0.15)
    parser.add_argument("--out-dir", type=Path, default=Path("."))
    args = parser.parse_args()

    with args.ccd_csv.open(newline="") as f:
        ccds = list(csv.DictReader(f))
    by_norm = {}
    for r in ccds:
        by_norm.setdefault(normalize_name(r["name"]), []).append(r)
    print(f"Loaded {len(ccds)} CCDs.")

    session = requests.Session()
    session.headers.update({"User-Agent": UA})

    matched = []
    college_hits = []  # any TASB page that looks like a college/university, matched or not
    matched_fice = set()

    total = args.end_key - args.start_key + 1
    for index, key in enumerate(range(args.start_key, args.end_key + 1), start=1):
        url = TASB_URL.format(key=key)
        try:
            resp = session.get(url, timeout=20, allow_redirects=False)
            status = resp.status_code
            if status in (301, 302, 303, 307, 308):
                time.sleep(args.delay)
                continue
            if status != 200:
                time.sleep(args.delay)
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            browser_title = get_title(soup)
            tasb_name = extract_tasb_name(resp.text, browser_title)
            if not tasb_name:
                time.sleep(args.delay)
                continue

            norm = normalize_name(tasb_name)
            candidates = by_norm.get(norm, [])
            if len(candidates) == 1:
                r = candidates[0]
                matched.append({
                    "tasb_key": key, "tasb_name": tasb_name,
                    "thecb_fice": r["thecb_fice"], "ccd_name": r["name"],
                    "tasb_url": url,
                })
                matched_fice.add(r["thecb_fice"])
                print(f"[{index:4}/{total}] {key:4} -> {r['name']} (matched)")
            elif "college" in tasb_name.lower() or "college" in norm.lower():
                college_hits.append({"tasb_key": key, "tasb_name": tasb_name, "tasb_url": url})
                print(f"[{index:4}/{total}] {key:4} college-like, no match: {tasb_name}")
        except Exception as exc:
            print(f"[{index:4}/{total}] {key}: ERROR {exc}")
        time.sleep(args.delay)

    unmatched_ccds = [r for r in ccds if r["thecb_fice"] not in matched_fice]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "tx_ccd_tasb_crosswalk_2026-09-02.csv", matched, ["tasb_key", "tasb_name", "thecb_fice", "ccd_name", "tasb_url"])
    write_csv(args.out_dir / "tx_ccd_tasb_college_like_unmatched_2026-09-02.csv", college_hits, ["tasb_key", "tasb_name", "tasb_url"])
    write_csv(args.out_dir / "tx_ccd_tasb_unmatched_ccds_2026-09-02.csv", unmatched_ccds, ["thecb_fice", "name", "city", "website", "campus_count", "slug"])

    print()
    print("=" * 60)
    print(f"Matched:              {len(matched)}")
    print(f"Unmatched CCDs:       {len(unmatched_ccds)} -- {[r['name'] for r in unmatched_ccds]}")
    print(f"College-like, no CCD match: {len(college_hits)}")


if __name__ == "__main__":
    main()
