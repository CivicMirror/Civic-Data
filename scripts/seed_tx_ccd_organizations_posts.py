#!/usr/bin/env python3
"""
Structure only: generate Organization (Board of Trustees) and Post (trustee
seat) records for TX community college districts from the seat plan each
district's sourced BBB(LOCAL) text implies (see issue #14).

Reuses tx_isd_parse_structure.parse_district() as-is (see issue #13) --
its regexes operate purely on the BBB(LOCAL) text and a district key, with
no ISD-specific vocabulary; its CDN-keyed MANUAL_OVERRIDES/MANUAL_REVIEW_CDNS/
EXCLUDED_CURRENTLY_APPOINTED_CDNS dicts simply never match a THECB FICE code,
so nothing ISD-specific leaks in. Verified against all 43 TASB-matched CCDs
before writing this script: 31 parse cleanly (27 pure at-large, 4 pure SMD),
12 do not -- 6 hybrid districts whose "Membership"/"Method of Election"
wording doesn't match the ISD-derived hybrid-count regex closely enough
(CCD BBB(LOCAL) text phrases the split differently district to district),
2 with no BBB(LOCAL) policy on file at all (Galveston, San Jacinto), 3 SMD
district-number-count mismatches (Houston City, McLennan, South Texas), 1
with no board-size sentence found (South Texas College). Combined with the
7 CCDs no TASB page exists for at all (Alamo, Central Texas, Cisco, Del Mar,
Howard County, Lone Star, Navarro), that's 19 of 50 districts needing
individual per-district research -- same two-tier shape as the ISD Phase 3
pass, not seeded here.

Seat modeling: identical convention to seed_tx_isd_organizations_posts.py
(one shared Post for an at-large bloc, one Post per SMD seat).

Excludes: nothing yet at the exclusion level (no CCD has been individually
confirmed appointed-not-elected the way Houston ISD was) -- the 19 unparsed
districts are simply not templated, not excluded.

ID collisions checked globally across every existing
data/us/tx/organizations/**/*.yaml and posts/**/*.yaml id, same as the ISD
script (this repo already has *-tx-isd/... ids that could theoretically
share a base slug with a same-named CCD, e.g. no known case yet but not
assumed collision-free either).

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_ccd_organizations_posts.py [--write]
"""
import csv
import re
import sys
import uuid
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
JURISDICTIONS_DIR = DATA_DIR / "jurisdictions" / "school"
ORGS_DIR = DATA_DIR / "organizations" / "school"
POSTS_DIR = DATA_DIR / "posts" / "school"

sys.path.insert(0, str(REPO / "reference" / "TX Rolling Audit"))
from tx_isd_parse_structure import parse_district  # noqa: E402

BBB_CSV = REPO / "reference" / "TX Rolling Audit" / "tx_ccd_bbb_local_2026-09-02.csv"

# Fixed namespace for this script's deterministic organization ids -- distinct
# from the ISD script's namespace so a same-FICE/same-CDN coincidence (never
# expected, THECB FICE and TEA CDN are different numbering spaces entirely)
# can't collide organization ids.
NS = uuid.UUID("6b6f5e1d-6a8e-5b2a-8b0e-1c9d7a4f2e33")

FICE_RE = re.compile(r"FICE (\d{6})")
SLUG_RE = re.compile(r"community_college_district:([a-z0-9-]+)/school$")


def load_jurisdictions():
    """FICE -> {slug, jurisdiction_id, name} for every seeded CCD jurisdiction."""
    by_fice = {}
    for f in JURISDICTIONS_DIR.glob("*-ccd-school.yaml"):
        doc = yaml.safe_load(f.read_text())
        slug_match = SLUG_RE.search(doc["id"])
        fice_match = None
        for src in doc["sources"]:
            m = FICE_RE.search(src.get("note", ""))
            if m:
                fice_match = m.group(1)
                break
        if not slug_match or not fice_match:
            raise ValueError(f"could not parse slug/fice from {f}")
        by_fice[fice_match] = {
            "slug": slug_match.group(1),
            "jurisdiction_id": doc["id"],
            "name": doc["name"],
        }
    return by_fice


def load_bbb_rows():
    with BBB_CSV.open(newline="") as f:
        return list(csv.DictReader(f))


def org_id(fice):
    return f"ocd-organization/{uuid.uuid5(NS, f'organization|{fice}')}"


def existing_ids(kind):
    ids = {}
    for f in (DATA_DIR / kind).glob("*/*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            ids[doc["id"]] = doc
    return ids


def build_records(fice, jur, bbb_row, plan):
    slug = jur["slug"]
    source_entry = {
        "url": bbb_row["source_url"],
        "note": (
            f"{bbb_row['policy_name']} ({bbb_row['source']}, "
            f"{bbb_row['update_name']}, issued {bbb_row['date_issued']}) -- "
            f"election-method/board-size source. Full text in "
            f"reference/TX Rolling Audit/tx_ccd_bbb_local_2026-09-02.csv."
        ),
        "retrieved": "2026-09-02",
    }

    org = {
        "id": org_id(fice),
        "name": f"{jur['name']} Board of Trustees",
        "jurisdiction_id": jur["jurisdiction_id"],
        "identifiers": [{"scheme": "thecb-fice", "identifier": fice}],
        "status": "active",
        "sources": [source_entry],
    }

    posts = []
    if plan["at_large_seats"]:
        posts.append(
            {
                "id": f"{slug}-tx-ccd/trustee-at-large" if plan["smd_seats"] else f"{slug}-tx-ccd/trustee",
                "organization_id": org["id"],
                "title": "Trustee, At-Large" if plan["smd_seats"] else "Trustee",
                "seats": plan["at_large_seats"],
                "identifiers": [],
                "sources": [source_entry],
            }
        )
    for n in plan["smd_district_numbers"]:
        posts.append(
            {
                "id": f"{slug}-tx-ccd/trustee-district-{n}",
                "organization_id": org["id"],
                "title": f"Trustee, District {n}",
                "seats": 1,
                "identifiers": [],
                "sources": [source_entry],
            }
        )
    return org, posts


def main():
    write = "--write" in sys.argv[1:]

    jurisdictions = load_jurisdictions()
    bbb_by_fice = {r["thecb_fice"]: r for r in load_bbb_rows()}

    org_ids = existing_ids("organizations")
    post_ids = existing_ids("posts")

    stats = Counter()
    ORGS_DIR.mkdir(parents=True, exist_ok=True)
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    for fice, jur in sorted(jurisdictions.items()):
        bbb_row = bbb_by_fice.get(fice)
        if bbb_row is None:
            stats["skip_no_bbb_row"] += 1
            continue

        plan = parse_district(fice, bbb_row["local_text"])
        if "skip_reason" in plan:
            stats["skip_unparsed"] += 1
            continue

        org, posts = build_records(fice, jur, bbb_row, plan)

        if org["id"] in org_ids:
            stats["org_existing"] += 1
        else:
            stats["org_new"] += 1
            path = ORGS_DIR / f"{jur['slug']}-tx-ccd-board.yaml"
            if write:
                path.write_text(
                    HEADER + yaml.safe_dump(org, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
                )
            org_ids[org["id"]] = org

        for post in posts:
            existing_doc = post_ids.get(post["id"])
            if existing_doc is not None:
                if existing_doc.get("organization_id") == post["organization_id"]:
                    stats["post_existing"] += 1
                else:
                    stats["post_skipped_id_conflict"] += 1
                    print(f"ID CONFLICT: {post['id']} already claimed by "
                          f"organization_id={existing_doc.get('organization_id')}")
                continue
            stats["post_new"] += 1
            fname = post["id"].replace("/", "-") + ".yaml"
            path = POSTS_DIR / fname
            if write:
                path.write_text(
                    HEADER + yaml.safe_dump(post, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
                )
            post_ids[post["id"]] = post

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded from the TX CCD rolling audit's sourced BBB(LOCAL) election-\n"
    "# structure text by scripts/seed_tx_ccd_organizations_posts.py\n"
    "# (structure only -- see issue #14). Current officeholders are not yet\n"
    "# researched; this covers board size and seat structure only.\n"
)


if __name__ == "__main__":
    main()
