#!/usr/bin/env python3
"""
Extract BBB(LOCAL) text for the 7 TX ISDs that use Policy Connect
(policyconnect.org) instead of TASB Policy Online, closing the last gap from
issue #13's BBB(LOCAL) extraction pass.

The user found that policyconnect.org has a public, unauthenticated content
route (`/policy/{org-slug}/BBB`) distinct from the org dashboard route
(`/org/{org-slug}`) this script's earlier investigation got stuck on -- the
dashboard route gates content behind a client-side login check that never
even attempts a fetch, but the direct policy-page route calls a public REST
API with no auth. Verified by hand for Crane ISD before writing this script.

API: GET /api/v1/policyContent/getPolicyContent-By-subsectionCode/{org-slug}/{code}/{policyTypeId}
`policyTypeId` for "Local Policy" (659690121db25d07a8d17e34) is a global
constant, not per-org -- confirmed by reusing it successfully across Crane
and Lingleville ISDs before running this at scale.

Response shape: data.data[0].policyData has {version, issuedAt}; contents[]
holds {title, desc (HTML), children[]} blocks, recursively nested (e.g.
"Terms and Election Schedule" > "At Large" > text). This script flattens
title+desc pairs depth-first into one local_text string, matching the shape
tx_isd_bbb_local_extract.py already produces for the TASB-sourced districts,
so both feed the same classify() heuristic and the same output CSV.

Usage: python3 tx_isd_bbb_local_policyconnect_extract.py
"""
import csv
import html
import re
import sys
import time
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parent.parent.parent
SRC_DIR = REPO / "reference" / "TX Rolling Audit"
OUT = SRC_DIR / "tx_isd_bbb_local_2026-08-24.csv"

LOCAL_POLICY_TYPE_ID = "659690121db25d07a8d17e34"
HEADERS = {"User-Agent": "Mozilla/5.0"}

DISTRICTS = [
    ("crane-isd", "052901", "CRANE ISD"),
    ("lingleville-isd", "072909", "LINGLEVILLE ISD"),
    ("schulenburg-isd", "075903", "SCHULENBURG ISD"),
    ("sherman-isd", "091906", "SHERMAN ISD"),
    ("midland-isd", "165901", "MIDLAND ISD"),
    ("conroe-isd", "170902", "CONROE ISD"),
    ("carroll-isd", "220919", "CARROLL ISD"),
]

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tx_isd_bbb_local_extract import classify, FIELDS  # noqa: E402

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def clean(html_fragment):
    # desc fields come back double-encoded -- the JSON string literally
    # contains "&lt;p&gt;...&lt;/p&gt;", not real "<p>" tags, so entities must
    # be unescaped before tag-stripping or the regex never matches anything.
    text = html.unescape(html_fragment or "")
    text = TAG_RE.sub(" ", text)
    text = html.unescape(text)
    return WS_RE.sub(" ", text).strip()


def flatten(contents):
    parts = []
    for block in contents:
        title = clean(block.get("title", ""))
        desc = clean(block.get("desc", ""))
        if title and desc:
            parts.append(f"{title}: {desc}")
        elif desc:
            parts.append(desc)
        parts.extend(flatten(block.get("children") or []))
    return parts


def fetch(slug, session):
    url = f"https://policyconnect.org/api/v1/policyContent/getPolicyContent-By-subsectionCode/{slug}/BBB/{LOCAL_POLICY_TYPE_ID}"
    resp = session.get(url, headers=HEADERS, timeout=30)
    if resp.status_code != 200:
        return {"fetch_status": f"http_{resp.status_code}"}, url

    body = resp.json()
    if not body.get("status") or not body.get("data", {}).get("data"):
        return {"fetch_status": "no_policy_data"}, url

    policy = body["data"]["data"][0]
    policy_data = policy.get("policyData", {})
    local_text = " ".join(flatten(policy.get("contents", [])))

    return {
        "policy_name": "BBB(LOCAL)",
        "update_name": f"Version {policy_data.get('version', '')}".strip(),
        "date_issued": policy_data.get("issuedAt", ""),
        "local_text": local_text,
        "heuristic_structure": classify(local_text),
        "fetch_status": "ok",
    }, url


def main():
    done_keys = set()
    if OUT.exists():
        with OUT.open(newline="") as f:
            done_keys = {row["source_key"] for row in csv.DictReader(f) if row["source"] == "policyconnect"}

    session = requests.Session()
    with OUT.open("a", newline="") as out_f:
        writer = csv.DictWriter(out_f, fieldnames=FIELDS)
        for slug, cdn, name in DISTRICTS:
            if slug in done_keys:
                print(f"skip (already present): {slug}")
                continue
            result, url = fetch(slug, session)
            row = {
                "source": "policyconnect",
                "source_key": slug,
                "tea_cdn": cdn,
                "tea_district_name": name,
                "source_url": url,
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
            print(f"{cdn} {name:25s} {row['fetch_status']:20s} {row['heuristic_structure']}")
            time.sleep(0.5)


if __name__ == "__main__":
    main()
