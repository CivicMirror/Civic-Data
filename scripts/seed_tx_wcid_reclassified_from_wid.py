#!/usr/bin/env python3
"""
Structure only: two districts tagged Entity Type == "Water Improvement
District" by the Comptroller's SPDPID, but named as Water Control and
Improvement Districts (WCID, Water Code Ch. 51) -- neither appears under
its own name in the WCID raw sheet (tx_wcid_raw_2026-09-03.csv), so they
were never seeded by seed_tx_wcid_jurisdictions_orgs_posts.py. See issue
#32's WID batch comment for the full reasoning.

Both statutes (Ch. 51 WCID Sec. 51.071, Ch. 55 WID Sec. 55.101) fix the
board at 5 directors, so the structural template is identical either way
-- this script mints them under the water_control_improvement_district:
type key to match their actual statutory name, not the water_improvement_
district: key their raw Entity Type would suggest.

- Harris County Water Control and Improvement District #74 (SPD ID 103227267)
- Travis County Water Control and Improvement District #18 (SPD ID 103227480)

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_wcid_reclassified_from_wid.py [--write]
"""
import re
import sys
import unicodedata
import uuid
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
JUR_DIR = DATA_DIR / "jurisdictions" / "wcid"
ORGS_DIR = DATA_DIR / "organizations" / "wcid"
POSTS_DIR = DATA_DIR / "posts" / "wcid"

RETRIEVED = "2026-09-03"
TYPE_KEY = "water_control_improvement_district"
DIRECTOR_COUNT = 5
NS = uuid.UUID("7a1c9e2d-4b6f-58a3-9c7e-2d5f8a1b4c9e")  # same namespace as the original WCID script

NOTE = (
    "Enumerated via the Texas Comptroller's SPDPID under Entity Type "
    "'Water Improvement District', but named as a Water Control and "
    "Improvement District -- reclassified to Water Code Ch. 51 (Sec. "
    "51.071, 5 directors, fixed) rather than Ch. 55, since it doesn't "
    "appear under its own name in the separate WCID raw enumeration. See "
    "issue #32's WID batch comment."
)

ROWS = [
    ("Harris County Water Control and Improvement District #74", "Harris County", "https://www.harriscowcid74.org/", "103227267"),
    ("Travis County Water Control and Improvement District #18", "Travis County", None, "103227480"),
]

NOISE_RE = re.compile(r"\bwater control (?:and|&) improvement district\b|\bcounty\b", re.IGNORECASE)


def slugify(name):
    s = name.replace("&", "and")
    s = re.sub(r"\bNo\.\s*(\d+)", r"#\1", s, flags=re.IGNORECASE)
    s = NOISE_RE.sub("", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"#\s*(\d+)", r"-\1", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


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
    jur_ids = existing_ids("jurisdictions")
    stats = Counter()

    for name, county, website, spd_id in ROWS:
        slug = slugify(name)
        jid = f"ocd-jurisdiction/country:us/state:tx/{TYPE_KEY}:{slug}/sewer"
        if jid in jur_ids:
            print(f"ALREADY EXISTS (skipping -- check for a real slug collision with the WCID batch): {jid}")
            stats["skip_existing"] += 1
            continue

        source_entry = {
            "url": website or "https://spdpid.comptroller.texas.gov/",
            "note": f"{name} (SPD Public ID {spd_id}) -- {county}. {NOTE}",
            "retrieved": RETRIEVED,
        }
        jur = {
            "id": jid,
            "name": name,
            "state": "tx",
            "division_id": f"ocd-division/country:us/state:tx/{TYPE_KEY}:{slug}",
            "classification": "sewer",
            "identifiers": [{"scheme": "tx-spdpid", "identifier": spd_id}],
            "sources": [source_entry],
        }
        write_file(JUR_DIR / f"{slug}-sewer.yaml", jur, write)
        stats["jurisdiction_new"] += 1

        oid = f"ocd-organization/{uuid.uuid5(NS, f'organization|{slug}')}"
        org = {
            "id": oid,
            "name": f"{name} Board of Directors",
            "jurisdiction_id": jid,
            "identifiers": [],
            "status": "active",
            "sources": [source_entry],
        }
        write_file(ORGS_DIR / f"{slug}-wcid-board.yaml", org, write)
        stats["org_new"] += 1

        for n in range(1, DIRECTOR_COUNT + 1):
            pid = f"{slug}-tx-wcid/director-{n}"
            post = {
                "id": pid,
                "organization_id": oid,
                "title": f"Director, Position {n}",
                "seats": 1,
                "identifiers": [],
                "sources": [source_entry],
            }
            write_file(POSTS_DIR / f"{slug}-tx-wcid-director-{n}.yaml", post, write)
            stats["post_new"] += 1

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded by scripts/seed_tx_wcid_reclassified_from_wid.py (issue #32) --\n"
    "# a WID-Entity-Type-tagged district reclassified as WCID by name.\n"
    "# Structure only -- current officeholders are not yet researched.\n"
)


if __name__ == "__main__":
    main()
