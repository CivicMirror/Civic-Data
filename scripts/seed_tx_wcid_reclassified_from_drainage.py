#!/usr/bin/env python3
"""
Structure only: one district tagged Entity Type == "Drainage District" by
the Comptroller's SPDPID, but named and confirmed governed as a Water
Control and Improvement District (WCID, Water Code Ch. 51) -- doesn't
appear under its own name in the WCID raw sheet
(tx_wcid_raw_2026-09-03.csv), so it was never seeded by
seed_tx_wcid_jurisdictions_orgs_posts.py. Same pattern as two rows
reclassified earlier from the WID batch
(seed_tx_wcid_reclassified_from_wid.py).

- Grand Lakes Water Control and Improvement District (Fort Bend County,
  SPD 103226024): confirmed via issue #32 research to have a 5-director
  board with May-dated staggered terms, consistent with Water Code Sec.
  51.071's elected 5-director WCID model. No official standalone website
  was found (only third-party district-directory aggregator pages) --
  moderate confidence, flagged for a follow-up check when a primary
  source becomes available.

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_wcid_reclassified_from_drainage.py [--write]
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

NAME = "Grand Lakes Water Control and Improvement District"
COUNTY = "Fort Bend County"
SPD_ID = "103226024"
NOTE = (
    "Enumerated via the Texas Comptroller's SPDPID under Entity Type "
    "'Drainage District', but named as a Water Control and Improvement "
    "District -- reclassified to Water Code Ch. 51 (Sec. 51.071, 5 "
    "directors) per issue #32 research: confirmed 5-director board with "
    "May-dated staggered terms consistent with the Ch. 51 elected model. "
    "No official standalone website found (only third-party district-"
    "directory aggregator pages) -- moderate confidence."
)

NOISE_RE = re.compile(r"\bwater control (?:and|&) improvement district\b|\bcounty\b", re.IGNORECASE)


def slugify(name):
    s = name.replace("&", "and")
    s = NOISE_RE.sub("", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
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

    slug = slugify(NAME)
    jid = f"ocd-jurisdiction/country:us/state:tx/{TYPE_KEY}:{slug}/sewer"
    if jid in jur_ids:
        print(f"ALREADY EXISTS (skipping -- check for a real slug collision with the WCID batch): {jid}")
        stats["skip_existing"] += 1
    else:
        source_entry = {
            "url": "https://spdpid.comptroller.texas.gov/",
            "note": f"{NAME} (SPD Public ID {SPD_ID}) -- {COUNTY}. {NOTE}",
            "retrieved": RETRIEVED,
        }
        jur = {
            "id": jid,
            "name": NAME,
            "state": "tx",
            "division_id": f"ocd-division/country:us/state:tx/{TYPE_KEY}:{slug}",
            "classification": "sewer",
            "identifiers": [{"scheme": "tx-spdpid", "identifier": SPD_ID}],
            "sources": [source_entry],
        }
        write_file(JUR_DIR / f"{slug}-sewer.yaml", jur, write)
        stats["jurisdiction_new"] += 1

        oid = f"ocd-organization/{uuid.uuid5(NS, f'organization|{slug}')}"
        org = {
            "id": oid,
            "name": f"{NAME} Board of Directors",
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
    "# Seeded by scripts/seed_tx_wcid_reclassified_from_drainage.py\n"
    "# (issue #32) -- a Drainage-District-Entity-Type-tagged district\n"
    "# reclassified as WCID by name. Structure only -- current\n"
    "# officeholders are not yet researched.\n"
)


if __name__ == "__main__":
    main()
