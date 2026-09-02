#!/usr/bin/env python3
"""
Structure only: generate Organization (Board of Directors) and Post
(elected director seat) records for the 49 Texas Central Appraisal
Districts with SB 2 (2021)-elected seats (see issue #28).

Source: reference/TX Rolling Audit/tx_cad_elected_2026-09-02.csv, derived
from the "Appraisal Districts" sheet of TX_Municipalities.xlsx (253 CADs
enumerated from TAAD's district directory; 49 flagged "Yes" for elected
seats by cross-referencing each CAD's county against the 2020 Census
75,000+ population threshold in Tax Code 6.0301).

Board structure, per Tax Code 6.0301 (added by SB 2, 2021) for a county
with population 75,000+: a 9-member board -- 5 appointed by the county's
taxing units (unchanged from the pre-2021 default), 3 popularly elected
countywide ("Place 1/2/3", per the Dallas County 2024 special-election
results already checked in this issue), and 1 ex officio (the county's own
Tax Assessor-Collector, unless the commissioners court removes that seat).
Per this project's elected-boards-only scope, ONLY the 3 elected Place
seats get a Post here -- the 5 appointed seats and the ex officio seat are
out of scope, same reasoning as every prior TX audit phase.

Jurisdiction: Tax Code 6.01(a) establishes "an appraisal district ... in
each county", so 48 of the 49 CADs map directly to their existing county
jurisdiction file (data/us/tx/jurisdictions/county/<slug>-government.yaml)
-- no new jurisdiction needed for those. The one exception is Potter/
Randall CAD, a single legal entity spanning two counties; see
scripts/seed_tx_cad_potter_randall_jurisdiction.py, which must run BEFORE
this script to mint that joint jurisdiction (same "no existing OCD
division fits" reasoning as the ISD/CCD standalone-jurisdiction precedent,
opencivicdata/ocd-division-ids#195).

Officeholder research is separate future work: the first elected term
began with a May 4, 2024 special election (not the November 2024 general
already imported for county offices under #25), so no existing TX 2024
election-results source covers these seats. Not started here.

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_cad_organizations_posts.py [--write]
"""
import csv
import re
import sys
import unicodedata
import uuid
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
COUNTY_JUR_DIR = DATA_DIR / "jurisdictions" / "county"
ORGS_DIR = DATA_DIR / "organizations" / "appraisal"
POSTS_DIR = DATA_DIR / "posts" / "appraisal"
CAD_CSV = REPO / "reference" / "TX Rolling Audit" / "tx_cad_elected_2026-09-02.csv"

RETRIEVED = "2026-09-02"
TAAD_URL = "https://taad.org/resources/texas-cad-websites/"

# Fixed namespace for this script's deterministic organization ids.
NS = uuid.UUID("c3d8f9a1-6e2b-5f4c-8a9d-1b2e3f4a5c6d")


def slugify(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def org_id(county_slugs):
    return f"ocd-organization/{uuid.uuid5(NS, f'organization|{county_slugs}')}"


def load_county_jurisdictions():
    """county-slug -> jurisdiction_id, for every existing TX county jurisdiction."""
    by_slug = {}
    for f in COUNTY_JUR_DIR.glob("*-government.yaml"):
        doc = yaml.safe_load(f.read_text())
        slug = f.stem.replace("-government", "")
        by_slug[slug] = doc["id"]
    return by_slug


def load_potter_randall_jurisdiction():
    """The one hand-minted joint jurisdiction, if seed_tx_cad_potter_randall_jurisdiction.py has been run."""
    f = DATA_DIR / "jurisdictions" / "appraisal" / "potter-randall-appraisal-government.yaml"
    if not f.exists():
        return None
    doc = yaml.safe_load(f.read_text())
    return doc["id"]


def existing_ids(kind):
    ids = {}
    for f in (DATA_DIR / kind).glob("**/*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            ids[doc["id"]] = doc
    return ids


def main():
    write = "--write" in sys.argv[1:]

    with CAD_CSV.open(newline="") as f:
        cads = list(csv.DictReader(f))

    county_jur = load_county_jurisdictions()
    potter_randall_jur = load_potter_randall_jurisdiction()

    org_ids = existing_ids("organizations")
    post_ids = existing_ids("posts")

    stats = Counter()
    ORGS_DIR.mkdir(parents=True, exist_ok=True)
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    for r in cads:
        county_slugs = r["county_slugs"].split(";")
        if len(county_slugs) > 1:
            if potter_randall_jur is None:
                stats["skip_no_joint_jurisdiction"] += 1
                continue
            jurisdiction_id = potter_randall_jur
            org_slug = "potter-randall"
        else:
            slug = county_slugs[0]
            if slug not in county_jur:
                stats["skip_no_county_jurisdiction"] += 1
                continue
            jurisdiction_id = county_jur[slug]
            org_slug = slug

        source_entry = {
            "url": r["website"] or TAAD_URL,
            "note": (
                f"{r['cad_name']} -- enumerated via TAAD's Texas CAD "
                f"website directory; elected-seat status confirmed per "
                f"Tax Code 6.0301 (county population {r['population']}, "
                f"2020 Census, over the 75,000 threshold). Only the 3 "
                f"popularly-elected \"Place\" seats get a Post here; the "
                f"board's 5 appointed seats and 1 ex officio seat "
                f"(county Tax Assessor-Collector) are out of scope."
            ),
            "retrieved": RETRIEVED,
        }

        oid = org_id(org_slug)
        org = {
            "id": oid,
            "name": f"{r['cad_name']} Board of Directors",
            "jurisdiction_id": jurisdiction_id,
            "identifiers": [],
            "status": "active",
            "sources": [source_entry],
        }

        if oid in org_ids:
            stats["org_existing"] += 1
        else:
            stats["org_new"] += 1
            path = ORGS_DIR / f"{org_slug}-tx-cad-board.yaml"
            if write:
                path.write_text(
                    HEADER + yaml.safe_dump(org, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
                )
            org_ids[oid] = org

        for n in (1, 2, 3):
            post = {
                "id": f"{org_slug}-tx-cad/director-place-{n}",
                "organization_id": oid,
                "title": f"Director, Place {n}",
                "seats": 1,
                "identifiers": [],
                "sources": [source_entry],
            }
            if post["id"] in post_ids:
                stats["post_existing"] += 1
                continue
            stats["post_new"] += 1
            path = POSTS_DIR / f"{org_slug}-tx-cad-director-place-{n}.yaml"
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
    "# Seeded from the TX Appraisal District rolling audit's TAAD/Tax-Code-\n"
    "# 6.0301 enumeration by scripts/seed_tx_cad_organizations_posts.py\n"
    "# (structure only -- see issue #28). Current officeholders are not yet\n"
    "# researched; this covers the 3 popularly-elected \"Place\" seats only,\n"
    "# not the board's 5 appointed seats or 1 ex officio seat.\n"
)


if __name__ == "__main__":
    main()
