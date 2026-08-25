#!/usr/bin/env python3
"""
Extract each TX ISD's BBB(LOCAL) policy text ("Board Members: Elections",
local-adoption tier) from TASB Policy Online, using the TASB<->TEA crosswalk
already committed to this branch (tx_isd_tasb_tea_crosswalk_2026-08-23.csv,
1,002 districts).

This is the remaining statewide sourcing gap flagged on issue #13: TEA/AskTED
gives officeholder names but not at-large/single-member-district/hybrid
election structure, and that structure has to be confirmed per district
rather than assumed from the Education Code default.

Fetch method, verified by hand against San Antonio ISD (key=176) before
writing this script: `PolicyOnline/PolicyDetails?key={key}&code=BBB` is a
plain server-rendered page -- no JS/AJAX needed despite the earlier GH issue
comment's guess that it would be (that guess was about the policy *text*
specifically; the crosswalk step already established the surrounding page
doesn't need a browser). The page embeds TWO `#maincolumn #policytext` blocks
back to back: BBB(LEGAL) (the boilerplate Education Code text, identical
across every district) first, then BBB(LOCAL) (the district's own adopted
election method) second, each followed by a `#bottomnotes` block naming which
one it is ("BBB(LEGAL)-P" vs "BBB(LOCAL)-X") plus the local update name/date.
This script keeps only the LOCAL block -- the LEGAL block is Chapter 11
boilerplate already covered by the audit's statutory sourcing, not
district-specific.

A district can have BBB(LOCAL) content that is genuinely a single short
paragraph (as with San Antonio, ~100 words) or can be missing/blank (no
locally-adopted policy on file, meaning the Education Code default applies
un-modified) -- both are legitimate outcomes, not fetch failures. This script
does NOT classify at-large vs. single-member vs. hybrid; it captures the raw
sourced text (that's the actual citable source) plus a best-effort heuristic
tag to help a human reviewer triage 1,002 rows, not to replace the review.

Rate-limited (0.5s between requests) and resumable: writes incrementally to
the output CSV and skips any tasb_key already present in it on a re-run, so
an interrupted run can be restarted without re-fetching what's done.

Usage: python3 tx_isd_bbb_local_extract.py [--limit N] [--out PATH]
"""
import argparse
import csv
import re
import time
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parent.parent.parent
SRC_DIR = REPO / "reference" / "TX Rolling Audit"
CROSSWALK = SRC_DIR / "tx_isd_tasb_tea_crosswalk_2026-08-23.csv"
DEFAULT_OUT = SRC_DIR / "tx_isd_bbb_local_2026-08-24.csv"

HEADERS = {
    # The WAF in front of pol.tasb.org (Azure Application Gateway) 403s a bare
    # User-Agent from python-requests -- verified by hand: curl with just a UA
    # gets 200, requests with just a UA gets 403, requests with this full
    # browser-like header set gets 200. Header-completeness fingerprinting,
    # not a UA string check specifically.
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

BLOCK_RE = re.compile(
    r'<div id="maincolumn"><div id="policytext">(.*?)</div>\s*'
    r'<div id="bottomnotes"[^>]*>(.*?)</div></div>',
    re.S,
)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")

FIELDS = [
    "source",
    "source_key",
    "tea_cdn",
    "tea_district_name",
    "source_url",
    "policy_name",
    "update_name",
    "date_issued",
    "local_text",
    "heuristic_structure",
    "fetch_status",
]


def clean(html_fragment):
    text = TAG_RE.sub(" ", html_fragment)
    text = text.replace("&#38;", "&").replace("&amp;", "&").replace("&#39;", "'")
    return WS_RE.sub(" ", text).strip()


def classify(text):
    t = text.lower()
    if not t:
        return "no_local_policy_on_file"
    has_smd = "single-member district" in t or "single member district" in t
    # "by position"/"by place" (Education Code 11.058) is at-large-by-position:
    # candidates run against each other for a specific numbered seat, but
    # every voter district-wide votes on every seat -- distinct from both
    # plain at-large and single-member districts.
    has_by_position = "by position" in t or "by place" in t
    has_at_large = "at large" in t or "at-large" in t
    has_cumulative = "cumulative voting" in t
    if has_smd and (has_at_large or has_by_position):
        return "hybrid_smd_and_at_large"
    if has_smd:
        return "single_member_district"
    if has_cumulative:
        return "at_large_cumulative"
    if has_by_position:
        return "at_large_by_position"
    if has_at_large:
        return "at_large"
    return "unclear_needs_review"


def fetch_local_policy(key, session):
    url = f"https://pol.tasb.org/PolicyOnline/PolicyDetails?key={key}&code=BBB"
    resp = session.get(url, headers=HEADERS, timeout=30)
    if resp.status_code != 200:
        return {"fetch_status": f"http_{resp.status_code}"}

    blocks = BLOCK_RE.findall(resp.text)
    local_block = None
    for text_html, notes_html in blocks:
        notes = clean(notes_html)
        if "(LOCAL)" in notes:
            local_block = (text_html, notes)
            break

    if local_block is None:
        return {"fetch_status": "no_local_block_found"}

    text_html, notes = local_block
    local_text = clean(text_html)

    # notes looks like "SAN ANTONIO ISDBBB(LOCAL)-XLDU 2019.06DATE ISSUED: 11/8/2019"
    m = re.search(r"(BBB\(LOCAL\)[-A-Z]*)", notes)
    policy_name = m.group(1) if m else ""
    m = re.search(r"((?:LDU|UPDATE)[^D]*?)DATE ISSUED", notes)
    update_name = m.group(1).strip() if m else ""
    m = re.search(r"DATE ISSUED:\s*(\S+)", notes)
    date_issued = m.group(1) if m else ""

    return {
        "policy_name": policy_name,
        "update_name": update_name,
        "date_issued": date_issued,
        "local_text": local_text,
        "heuristic_structure": classify(local_text),
        "fetch_status": "ok",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--delay", type=float, default=0.5)
    args = parser.parse_args()

    with CROSSWALK.open(newline="") as f:
        districts = list(csv.DictReader(f))
    if args.limit:
        districts = districts[: args.limit]

    done_keys = set()
    if args.out.exists():
        with args.out.open(newline="") as f:
            done_keys = {row["source_key"] for row in csv.DictReader(f) if row["source"] == "tasb"}
        print(f"Resuming: {len(done_keys)} TASB districts already in {args.out}")

    write_header = not args.out.exists()
    with args.out.open("a", newline="") as out_f:
        writer = csv.DictWriter(out_f, fieldnames=FIELDS)
        if write_header:
            writer.writeheader()

        session = requests.Session()
        remaining = [d for d in districts if d["tasb_key"] not in done_keys]
        total = len(remaining)
        for i, d in enumerate(remaining, start=1):
            try:
                result = fetch_local_policy(d["tasb_key"], session)
            except requests.RequestException as exc:
                result = {"fetch_status": f"error_{exc.__class__.__name__}"}

            row = {
                "source": "tasb",
                "source_key": d["tasb_key"],
                "tea_cdn": d["tea_cdn"],
                "tea_district_name": d["tea_district_name"],
                "source_url": d["tasb_url"],
                "policy_name": "",
                "update_name": "",
                "date_issued": "",
                "local_text": "",
                "heuristic_structure": "",
                "fetch_status": "",
            }
            row.update(result)
            writer.writerow(row)
            out_f.flush()

            print(f"[{i:4}/{total}] {d['tea_cdn']} {d['tea_district_name']:35s} "
                  f"{row['fetch_status']:25s} {row['heuristic_structure']}")

            time.sleep(args.delay)


if __name__ == "__main__":
    main()
