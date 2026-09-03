#!/usr/bin/env python3
"""
Structure only: generate Jurisdiction, Organization (Board of Directors),
and Post (elected supervisor seat) records for Texas Fresh Water Supply
Districts (FWSD) -- see issue #32, Phase 1.

Source: reference/TX Rolling Audit/tx_fwsd_raw_2026-09-03.csv, the
"Special Districts (Non-MUD)" sheet of TX_Municipalities.xlsx filtered to
Entity Type == "Fresh Water Supply District" (60 raw rows from the Texas
Comptroller's SPDPID enumeration).

Structure confirmed against statute before templating, same discipline as
WCID: Water Code Sec. 53.062 fixes the board at "five elected supervisors"
unconditionally -- no special-law override clause found, same situation
as WCID's Sec. 51.071 (5 directors) and unlike SUD's Sec. 65.101 (5-11,
set per-district, jurisdiction-only pending individual board-size
research). Sec. 49.103 (Provisions Applicable to All Districts) sets
staggered four-year terms; the franchise is the district's general
qualified (registered) voters per Sec. 49.1025, not a restricted
landowner franchise -- stays in scope per the #27/SWCD test. Seats are
at-large.

FWSD districts don't map 1:1 onto an existing county (same situation as
WCID/ISD) -- each gets its own jurisdiction file using the
fresh_water_supply_district: type key (see reference/TX Rolling Audit/
Special_District_Type_Keys.md). classification = "sewer".

Same name-vs-Entity-Type check applied as WCID/SUD: of 60 raw rows, only
2 have a name matching no "fresh water (supply) district"/"FWSD" token:
"Bayview Municipal Utility District" (a MUD, out of #32's scope entirely,
tracked under #11) and "Beeville Water Supply District" (a plain "Water
Supply District" -- an ambiguous, possibly different type, not assumed
to be a Ch. 53 FWSD). Both held back. Every other row, including
formatting variants ("Freshwater Supply District" one word, "Fresh Water
District" missing "Supply"), was confirmed a genuine FWSD naming variant,
not a type mismatch -- no exact-duplicate names found in this batch
(unlike WCID's Plum Creek or SUD's ACTIVE/INACTIVE pairs), so no
dedup logic is needed here.

Officeholder research is separate future work, not started here.

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_fwsd_jurisdictions_orgs_posts.py [--write]
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
JUR_DIR = DATA_DIR / "jurisdictions" / "fwsd"
ORGS_DIR = DATA_DIR / "organizations" / "fwsd"
POSTS_DIR = DATA_DIR / "posts" / "fwsd"
RAW_CSV = REPO / "reference" / "TX Rolling Audit" / "tx_fwsd_raw_2026-09-03.csv"

RETRIEVED = "2026-09-03"
TYPE_KEY = "fresh_water_supply_district"
DIRECTOR_COUNT = 5
COMPTROLLER_NOTE = (
    "Enumerated via the Texas Comptroller's Special Purpose District Public "
    "Information Database (SPDPID); board structure per Water Code Sec. "
    "53.062 (5 supervisors, fixed, no special-law override clause found) "
    "and Sec. 49.103 (staggered 4-year terms, general public qualified-"
    "voter franchise per Sec. 49.1025). Not yet individually verified "
    "against this district's own governing documents beyond the name/type "
    "checks noted in issue #32; a district-specific special act overriding "
    "board size would not be caught by this pass."
)

# Fixed namespace for this script's deterministic organization ids.
NS = uuid.UUID("9d3e7b1a-2c5f-5a68-b1d4-6e8f0a2c4d7b")

HELD_BACK_NAMES = {
    "Bayview Municipal Utility District",  # a MUD, out of #32's scope entirely -- tracked under #11
    "Beeville Water Supply District",  # plain "Water Supply District" -- not assumed to be a Ch. 53 FWSD
}

NOISE_RE = re.compile(r"\bfresh\s*water(?:\s*supply)?\s*district\b", re.IGNORECASE)


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

    slug_seen = {}
    for r in rows:
        if r["name"] in HELD_BACK_NAMES:
            stats["anomaly_held_back"] += 1
            print(f"HELD BACK (needs individual research, not seeded): {r['name']} -- {r['county']}")
            continue

        slug = slugify(r["name"])
        if slug in slug_seen:
            stats["skip_slug_collision"] += 1
            print(f"SKIPPED (slug collision with {slug_seen[slug]!r}, needs manual resolution): {r['name']!r}")
            continue
        slug_seen[slug] = r["name"]

        source_entry = {
            "url": r["website"] or "https://spdpid.comptroller.texas.gov/",
            "note": f"{r['name']} (SPD Public ID {r['spd_id']}) -- {r['county']}. {COMPTROLLER_NOTE}"
            + (f" Status per Comptroller's latest filing: {r['status']}." if r["status"] != "ACTIVE" else ""),
            "retrieved": RETRIEVED,
        }

        jid = jurisdiction_id(slug)
        if jid not in jur_ids:
            jur = {
                "id": jid,
                "name": r["name"],
                "state": "tx",
                "division_id": division_id(slug),
                "classification": "sewer",
                "identifiers": [{"scheme": "tx-spdpid", "identifier": r["spd_id"]}],
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
                "name": f"{r['name']} Board of Directors",
                "jurisdiction_id": jid,
                "identifiers": [],
                "status": "active",
                "sources": [source_entry],
            }
            write_file(ORGS_DIR / f"{slug}-fwsd-board.yaml", org, write)
            stats["org_new"] += 1
            org_ids[oid] = org
        else:
            stats["org_existing"] += 1

        for n in range(1, DIRECTOR_COUNT + 1):
            pid = f"{slug}-tx-fwsd/director-{n}"
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
            write_file(POSTS_DIR / f"{slug}-tx-fwsd-director-{n}.yaml", post, write)
            stats["post_new"] += 1
            post_ids[pid] = post

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded from the TX FWSD rolling audit (issue #32, Phase 1) by\n"
    "# scripts/seed_tx_fwsd_jurisdictions_orgs_posts.py. Structure only --\n"
    "# current officeholders are not yet researched. Board size/terms\n"
    "# templated from Water Code Sec. 53.062/49.103, not yet individually\n"
    "# verified against this district's own governing documents beyond the\n"
    "# name/type checks noted in issue #32.\n"
)


if __name__ == "__main__":
    main()
