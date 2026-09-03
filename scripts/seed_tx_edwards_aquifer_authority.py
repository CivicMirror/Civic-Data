#!/usr/bin/env python3
"""
Structure only: the Edwards Aquifer Authority (EAA), a single unique
entity -- see issue #32, Phase 1's follow-up research on the "Underground
Water Conservation District" Entity Type bucket.

Tagged Entity Type == "Underground Water Conservation District" in the
Comptroller's SPDPID (SPD Public ID 103227509, Bexar County), but the EAA
is NOT a Water Code Ch. 36 Groundwater Conservation District -- it's
governed by its own unique enabling legislation, the Edwards Aquifer
Authority Act, reflecting its much larger footprint and higher public
profile than a standard GCD. Given its one-of-a-kind statutory basis,
this gets its own type key (edwards_aquifer_authority:) rather than being
folded into groundwater_conservation_district:, same reasoning already
applied to the conservation_and_reclamation_district: type key.

Board structure per issue #32 research: 17 total members -- 15 elected
in single-member districts spanning Bexar, Comal, Guadalupe, Hays,
Caldwell, Medina, Atascosa, and Uvalde counties (a footprint far larger
than the "Bexar County" the raw SPDPID sheet lists), plus 2 APPOINTED
non-voting members (one from the South-Central Texas Water Advisory
Committee, one rotating between Medina/Uvalde county commissioners
courts). Per this audit's elected-boards-only scope (same discipline as
the TX Appraisal District work, which only seeded the popularly-elected
"Place" seats and excluded appointed/ex officio ones), ONLY the 15
elected single-member-district seats get a Post here; the 2 appointed
non-voting seats are excluded.

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_edwards_aquifer_authority.py [--write]
"""
import sys
import uuid
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
JUR_DIR = DATA_DIR / "jurisdictions" / "eaa"
ORGS_DIR = DATA_DIR / "organizations" / "eaa"
POSTS_DIR = DATA_DIR / "posts" / "eaa"

RETRIEVED = "2026-09-03"
TYPE_KEY = "edwards_aquifer_authority"
SLUG = "edwards-aquifer-authority"
NAME = "Edwards Aquifer Authority"
WEBSITE = "https://www.edwardsaquifer.org"
SPD_ID = "103227509"
ELECTED_SEATS = 15
NS = uuid.UUID("a1b2c3d4-5e6f-5789-9abc-1d2e3f4a5b6c")


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

    jid = f"ocd-jurisdiction/country:us/state:tx/{TYPE_KEY}:{SLUG}/sewer"
    if jid in jur_ids:
        print("Already seeded, nothing to do.")
        return

    source_entry = {
        "url": WEBSITE,
        "note": (
            f"{NAME} (SPD Public ID {SPD_ID}). Enumerated via the Texas "
            "Comptroller's SPDPID under Entity Type 'Underground Water "
            "Conservation District' and listed under Bexar County only, "
            "but confirmed via issue #32 research to be governed by its own "
            "unique enabling act (the Edwards Aquifer Authority Act), not "
            "Water Code Ch. 36, with a board spanning single-member "
            "districts in Bexar, Comal, Guadalupe, Hays, Caldwell, Medina, "
            "Atascosa, and Uvalde counties -- far larger than the raw "
            "sheet's single-county attribution. 15 of the board's 17 total "
            "seats are popularly elected; the other 2 are appointed "
            "non-voting members (South-Central Texas Water Advisory "
            "Committee; a rotating Medina/Uvalde county commissioners court "
            "seat) and are out of scope for this elected-boards-only audit."
        ),
        "retrieved": RETRIEVED,
    }

    jur = {
        "id": jid,
        "name": NAME,
        "state": "tx",
        "division_id": f"ocd-division/country:us/state:tx/{TYPE_KEY}:{SLUG}",
        "classification": "sewer",
        "identifiers": [{"scheme": "tx-spdpid", "identifier": SPD_ID}],
        "sources": [source_entry],
    }
    write_file(JUR_DIR / f"{SLUG}-sewer.yaml", jur, write)
    stats["jurisdiction_new"] += 1

    oid = f"ocd-organization/{uuid.uuid5(NS, f'organization|{SLUG}')}"
    org = {
        "id": oid,
        "name": f"{NAME} Board of Directors",
        "jurisdiction_id": jid,
        "identifiers": [],
        "status": "active",
        "sources": [source_entry],
    }
    write_file(ORGS_DIR / f"{SLUG}-board.yaml", org, write)
    stats["org_new"] += 1

    for n in range(1, ELECTED_SEATS + 1):
        pid = f"{SLUG}-tx-eaa/director-district-{n}"
        post = {
            "id": pid,
            "organization_id": oid,
            "title": f"Director, Single-Member District {n}",
            "seats": 1,
            "identifiers": [],
            "sources": [source_entry],
        }
        write_file(POSTS_DIR / f"{SLUG}-tx-eaa-director-district-{n}.yaml", post, write)
        stats["post_new"] += 1

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded by scripts/seed_tx_edwards_aquifer_authority.py (issue #32).\n"
    "# Structure only -- current officeholders are not yet researched.\n"
    "# Only the 15 popularly-elected single-member-district seats are\n"
    "# seeded; the board's 2 appointed non-voting seats are out of scope.\n"
)


if __name__ == "__main__":
    main()
