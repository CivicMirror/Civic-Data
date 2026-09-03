#!/usr/bin/env python3
"""
Structure only: generate Jurisdiction, Organization (Board of Directors),
and Post (elected director seat) records for Texas Irrigation Districts
-- see issue #32, Phase 1.

Source: reference/TX Rolling Audit/tx_irrigation_raw_2026-09-03.csv, the
"Special Districts (Non-MUD)" sheet of TX_Municipalities.xlsx filtered to
Entity Type == "Irrigation District" (18 raw rows from the Texas
Comptroller's SPDPID enumeration).

Structure confirmed against statute before templating, same discipline as
WCID/FWSD/WID: Water Code Sec. 58.071 fixes the board at "five directors"
unconditionally -- no special-law override clause found. Sec. 49.103 sets
staggered 4-year terms; the franchise is the district's general qualified
(registered) voters per Sec. 49.1025, not a restricted landowner
franchise -- stays in scope per the #27/SWCD test.

Unlike WCID/SUD/WID, this is a very clean batch: all 18 raw rows contain
an "Irrigation District" token in the name (0 name-vs-Entity-Type
mismatches, a first for this audit). Only one exact-duplicate name
("Brownsville Irrigation District", same county, two ACTIVE filings from
different report years) needed dedup -- resolved by preferring the more
recent report_year's SPD ID as primary and recording both as identifiers,
same approach as SUD's ACTIVE/INACTIVE pairs.

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_irrigation_jurisdictions_orgs_posts.py [--write]
"""
import csv
import re
import sys
import unicodedata
import uuid
from collections import Counter, defaultdict
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
JUR_DIR = DATA_DIR / "jurisdictions" / "irrigation"
ORGS_DIR = DATA_DIR / "organizations" / "irrigation"
POSTS_DIR = DATA_DIR / "posts" / "irrigation"
RAW_CSV = REPO / "reference" / "TX Rolling Audit" / "tx_irrigation_raw_2026-09-03.csv"

RETRIEVED = "2026-09-03"
TYPE_KEY = "irrigation_district"
DIRECTOR_COUNT = 5
COMPTROLLER_NOTE = (
    "Enumerated via the Texas Comptroller's Special Purpose District Public "
    "Information Database (SPDPID); board structure per Water Code Sec. "
    "58.071 (5 directors, fixed, no special-law override clause found) and "
    "Sec. 49.103 (staggered 4-year terms, general public qualified-voter "
    "franchise per Sec. 49.1025). Not yet individually verified against "
    "this district's own governing documents beyond the name/type checks "
    "noted in issue #32."
)

NS = uuid.UUID("c4f1a8d3-6b2e-59a7-9d3c-1e4f7a9c2b6d")

NOISE_RE = re.compile(r"\birrigation district\b", re.IGNORECASE)


def slugify(name):
    s = name.replace("&", "and")
    s = re.sub(r"\bNo\.\s*(\d+)", r"#\1", s, flags=re.IGNORECASE)
    s = NOISE_RE.sub("", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"#\s*(\d+)", r"-\1", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def jurisdiction_id(slug):
    return f"ocd-jurisdiction/country:us/state:tx/{TYPE_KEY}:{slug}/sewer"


def division_id(slug):
    return f"ocd-division/country:us/state:tx/{TYPE_KEY}:{slug}"


def org_id(slug):
    return f"ocd-organization/{uuid.uuid5(NS, f'organization|{slug}')}"


def existing_ids(kind):
    ids = {}
    base = DATA_DIR / kind
    if not base.exists():
        return ids
    for f in base.glob("**/*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            ids[doc["id"]] = doc
    return ids


def write_file(path, doc, write):
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            HEADER
            + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
        )


def main():
    write = "--write" in sys.argv[1:]

    with RAW_CSV.open(newline="") as f:
        rows = list(csv.DictReader(f))

    jur_ids = existing_ids("jurisdictions")
    org_ids = existing_ids("organizations")
    post_ids = existing_ids("posts")
    stats = Counter()

    by_name = defaultdict(list)
    for r in rows:
        by_name[r["name"]].append(r)

    slug_seen = {}
    for name, group in by_name.items():
        if len(group) > 1:
            primary = max(group, key=lambda g: g["report_year"] or "")
            spd_ids = sorted({g["spd_id"] for g in group})
            stats["dedup_pair"] += 1
        else:
            primary = group[0]
            spd_ids = [primary["spd_id"]]

        slug = slugify(name)
        if slug in slug_seen:
            stats["skip_slug_collision"] += 1
            print(f"SKIPPED (slug collision with {slug_seen[slug]!r}, needs manual resolution): {name!r}")
            continue
        slug_seen[slug] = name

        source_entry = {
            "url": primary["website"] or "https://spdpid.comptroller.texas.gov/",
            "note": f"{name} (SPD Public ID {', '.join(spd_ids)}) -- {primary['county']}. {COMPTROLLER_NOTE}"
            + (f" Status per Comptroller's latest filing: {primary['status']}." if primary["status"] != "ACTIVE" else ""),
            "retrieved": RETRIEVED,
        }

        jid = jurisdiction_id(slug)
        if jid not in jur_ids:
            jur = {
                "id": jid,
                "name": name,
                "state": "tx",
                "division_id": division_id(slug),
                "classification": "sewer",
                "identifiers": [{"scheme": "tx-spdpid", "identifier": s} for s in spd_ids],
                "sources": [source_entry],
            }
            write_file(JUR_DIR / f"{slug}-sewer.yaml", jur, write)
            stats["jurisdiction_new"] += 1
            jur_ids[jid] = jur
        else:
            stats["jurisdiction_existing"] += 1

        oid = org_id(slug)
        if oid not in org_ids:
            org = {
                "id": oid,
                "name": f"{name} Board of Directors",
                "jurisdiction_id": jid,
                "identifiers": [],
                "status": "active",
                "sources": [source_entry],
            }
            write_file(ORGS_DIR / f"{slug}-irrigation-board.yaml", org, write)
            stats["org_new"] += 1
            org_ids[oid] = org
        else:
            stats["org_existing"] += 1

        for n in range(1, DIRECTOR_COUNT + 1):
            pid = f"{slug}-tx-irrigation/director-{n}"
            if pid in post_ids:
                stats["post_existing"] += 1
                continue
            post = {
                "id": pid,
                "organization_id": oid,
                "title": f"Director, Position {n}",
                "seats": 1,
                "identifiers": [],
                "sources": [source_entry],
            }
            write_file(POSTS_DIR / f"{slug}-tx-irrigation-director-{n}.yaml", post, write)
            stats["post_new"] += 1
            post_ids[pid] = post

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded from the TX Irrigation District rolling audit (issue #32,\n"
    "# Phase 1) by scripts/seed_tx_irrigation_jurisdictions_orgs_posts.py.\n"
    "# Structure only -- current officeholders are not yet researched.\n"
    "# Board size/terms templated from Water Code Sec. 58.071/49.103, not\n"
    "# yet individually verified against this district's own governing\n"
    "# documents beyond the name/type checks noted in issue #32.\n"
)


if __name__ == "__main__":
    main()
