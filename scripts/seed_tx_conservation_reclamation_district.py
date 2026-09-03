#!/usr/bin/env python3
"""
Structure only: two districts tagged Entity Type == "Drainage District" by
the Comptroller's SPDPID, but named and confirmed governed as Conservation
and Reclamation Districts -- a statutorily distinct category, NOT Water
Code Ch. 56 Drainage Districts. See issue #32's Drainage District batch
comment for the full research trail.

- Brazoria County Conservation And Reclamation District #3 (SPD 103225885):
  created 1910 as a drainage district, recreated 1929 as a Conservation &
  Reclamation District by Senate Bill 24, reestablished 1969 under Art.
  8280-476. Confirmed elected: 3 Commissioners (titled "Commissioner
  Place" #1/#2/#3), but on a NOVEMBER general-election cycle rather than
  the May uniform date most Water Code Ch. 49-family districts use.
- Matagorda County Conservation and Reclamation District #1 (SPD
  103227326): originally the Matagorda County Levee Improvement District
  No. One (est. 1919), converted to its current name/status in 1991.
  Statutory basis is Article XVI, Sec. 59, Texas Constitution (the
  "Conservation Amendment"), not Water Code Ch. 56 or Ch. 62. Confirmed
  elected: 3 Commissioners (Chairman + 2 members).

Per the Texas Senate Research Center's "Invisible Government" report
(already read for this audit), districts "created pursuant to Chapter 62,
Acts of the 52nd Legislature, 1951" are explicitly EXCLUDED from Water
Code Chapter 49's general provisions that apply to most other district
types in this audit -- consistent with these two having their own
distinct statutory lineage rather than fitting the Ch. 56 Drainage
District template this audit has used elsewhere. Both happen to have the
same 3-seat board size as the Ch. 56 default, but that's coincidence, not
inheritance from Ch. 56 -- hence the separate type key rather than
folding them into drainage_district:.

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_conservation_reclamation_district.py [--write]
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
JUR_DIR = DATA_DIR / "jurisdictions" / "conservation_reclamation"
ORGS_DIR = DATA_DIR / "organizations" / "conservation_reclamation"
POSTS_DIR = DATA_DIR / "posts" / "conservation_reclamation"

RETRIEVED = "2026-09-03"
TYPE_KEY = "conservation_and_reclamation_district"
SEATS = 3
NS = uuid.UUID("f2a5c8e1-4b7d-59f3-8c1a-2e5f8b1c4d7a")

ROWS = [
    (
        "Brazoria County Conservation And Reclamation District #3",
        "Brazoria County",
        "https://bccd3.com",
        "103225885",
        (
            "Created 1910 as a drainage district, recreated 1929 as a "
            "Conservation & Reclamation District by Senate Bill 24, "
            "reestablished 1969 under Art. 8280-476. 3 elected Commissioner "
            "seats (titled 'Commissioner Place #1/#2/#3'), on a NOVEMBER "
            "general-election cycle -- unlike the May uniform election date "
            "most other districts in this audit use."
        ),
    ),
    (
        "Matagorda County Conservation and Reclamation District #1",
        "Matagorda County",
        "https://matagorda-crd.org/",
        "103227326",
        (
            "Originally the Matagorda County Levee Improvement District No. "
            "One (est. 1919), converted to its current name/status in 1991. "
            "Statutory basis is Article XVI, Sec. 59, Texas Constitution "
            "(the 'Conservation Amendment'), not Water Code Ch. 56 or Ch. "
            "62. 3 elected Commissioner seats (Chairman + 2 members)."
        ),
    ),
]

NOISE_RE = re.compile(r"\bconservation an?d? reclamation district\b", re.IGNORECASE)


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

    for name, county, website, spd_id, note in ROWS:
        slug = slugify(name)
        jid = f"ocd-jurisdiction/country:us/state:tx/{TYPE_KEY}:{slug}/sewer"
        if jid in jur_ids:
            stats["skip_existing"] += 1
            continue

        source_entry = {
            "url": website,
            "note": f"{name} (SPD Public ID {spd_id}) -- {county}. Enumerated via the Texas Comptroller's SPDPID under Entity Type 'Drainage District', but reclassified per issue #32 research: {note}",
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
            "name": f"{name} Board of Commissioners",
            "jurisdiction_id": jid,
            "identifiers": [],
            "status": "active",
            "sources": [source_entry],
        }
        write_file(ORGS_DIR / f"{slug}-board.yaml", org, write)
        stats["org_new"] += 1

        for n in range(1, SEATS + 1):
            pid = f"{slug}-tx-crd/commissioner-{n}"
            post = {
                "id": pid,
                "organization_id": oid,
                "title": f"Commissioner, Position {n}",
                "seats": 1,
                "identifiers": [],
                "sources": [source_entry],
            }
            write_file(POSTS_DIR / f"{slug}-tx-crd-commissioner-{n}.yaml", post, write)
            stats["post_new"] += 1

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded by scripts/seed_tx_conservation_reclamation_district.py\n"
    "# (issue #32) -- a Drainage-District-Entity-Type-tagged district\n"
    "# reclassified as its own statutorily distinct type. Structure only\n"
    "# -- current officeholders are not yet researched.\n"
)


if __name__ == "__main__":
    main()
