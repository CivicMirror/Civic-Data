#!/usr/bin/env python3
"""
Extract each TX CCD's BBB(LOCAL) policy text ("Board Members: Elections",
local-adoption tier) from TASB Policy Online, using the TASB<->THECB
crosswalk already committed to this branch
(tx_ccd_tasb_crosswalk_2026-09-02.csv, 43 districts).

Adapted from tx_isd_bbb_local_extract.py (see issue #13) for issue #14 --
same fetch mechanics (verified against ISDs; TASB hosts community college
board policy manuals identically to ISD ones, including their own BBB-series
codes, per the issue's earlier discovery comment), same heuristic classifier.
Does NOT classify at-large vs. single-member vs. hybrid definitively; that's
still a human/LLM review step over the raw sourced text.

Rate-limited (0.5s between requests) and resumable: writes incrementally,
skips any tasb_key already present in the output CSV on a re-run.

Usage: python3 tx_ccd_bbb_local_extract.py [--limit N] [--out PATH]
"""
import argparse
import csv
import re
import time
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parent.parent.parent
SRC_DIR = REPO / "reference" / "TX Rolling Audit"
CROSSWALK = SRC_DIR / "tx_ccd_tasb_crosswalk_2026-09-02.csv"
DEFAULT_OUT = SRC_DIR / "tx_ccd_bbb_local_2026-09-02.csv"

HEADERS = {
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
    "source", "source_key", "thecb_fice", "ccd_name", "source_url",
    "policy_name", "update_name", "date_issued", "local_text",
    "heuristic_structure", "fetch_status",
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
                "source": "tasb", "source_key": d["tasb_key"],
                "thecb_fice": d["thecb_fice"], "ccd_name": d["ccd_name"],
                "source_url": d["tasb_url"], "policy_name": "", "update_name": "",
                "date_issued": "", "local_text": "", "heuristic_structure": "",
                "fetch_status": "",
            }
            row.update(result)
            writer.writerow(row)
            out_f.flush()

            print(f"[{i:4}/{total}] {d['thecb_fice']} {d['ccd_name']:45s} "
                  f"{row['fetch_status']:25s} {row['heuristic_structure']}")

            time.sleep(args.delay)


if __name__ == "__main__":
    main()
