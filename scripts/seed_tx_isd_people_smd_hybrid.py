#!/usr/bin/env python3
"""
Phase 4b (SMD/hybrid follow-up -- issue #13): fill named-trustee-to-numbered-
seat Person/Membership records for the 142 single-member-district and hybrid
ISDs that seed_tx_isd_people_atlarge.py and its TSD-2025 follow-up couldn't
cover -- neither bulk TEA source carries a per-person seat/district number,
so those districts were left with structural Posts (Phase 3) but no
officeholders (see reference/TX Rolling Audit/
tx_isd_smd_hybrid_needs_seat_mapping_2026-09-02.csv, 142 rows).

Source: per-district manual research compiled in a Google Doc (issue #13
follow-up, "Backfill of the missing 142 districts with notes",
https://docs.google.com/document/d/1uwA52vc6aTpXsJN20UN7L3t-2Lep2H10d6D_vaeSXBI),
extracted into the tracked, clean CSV this script reads:
reference/TX Rolling Audit/tx_isd_smd_hybrid_seat_roster_2026-09-02.csv
(1,001 rows -- one per named/vacant seat, columns: tea_cdn, isd_name,
seat_label, seat_type, trustee_name, board_role, term_start, term_end,
verification_status, source_title, source_url). That doc mixed superseded
draft/"pilot"/"deep dive" sections with a final "Master Seat Roster --
Batch N" table per batch; the CSV already reflects only the reconciled
canonical rows (batch tables took precedence over the pilot draft for the
2 districts -- Brady, Brazosport ISDs -- both covered).

Seat-label parsing: districts across this state use wildly inconsistent
local terminology for the same numbered-SMD-seat concept (District N, Place
N, Precinct N, Ward N, Trustee Area N, SMD N, Position N, District N-A/B/...,
Place N (District <roman>) ...). Since Phase 3 already seeded exactly one
Post per numbered SMD seat (`<slug>-tx-isd/trustee-district-N`) regardless
of the district's own label for it, this script only needs the integer --
extracted from the seat_label (digit first, then a roman-numeral fallback
for the one district, Nacogdoches ISD, whose doc rows use pure roman
numerals with no digit at all). "Super District" seat_type (Victoria ISD's
2 rows, "District 6"/"District 7" on a 5-SMD+2-at-large board) and all
"At-Large ..." seat_type rows map to the district's single at-large Post
regardless of seat-label wording -- both a Seat A/Seat B doc label and a
Place-numbered at-large label collapse to that one Post the same way Phase
3 already models any at-large bloc (see seed_tx_isd_organizations_posts.py).

Skips (counted, not guessed through):
  - vacant seats (trustee_name "Vacant") -- a real vacancy, not an error.
  - ambiguous names carrying a doc author's uncertainty marker, i.e. a "/"
    joining two candidate names (e.g. "Austin Swaim / Garcia") -- could not
    be resolved to one person from this source alone.
  - seat_type "Single-Member District / At-Large" (Jim Hogg County ISD's 4
    rows) -- the doc itself couldn't determine which of that hybrid board's
    7 posts (3 at-large, 4 SMD) these 4 identically-labeled trustees hold.
  - a seat number that doesn't match any existing Post for that district
    (post_not_found) -- signals a parsing error or a doc/Post mismatch,
    logged rather than silently dropped.
  - over-count/duplicate-name-in-district, same caution as the at-large
    seed scripts.

`start`/`end` are omitted: the doc's term dates are month/year only ("May
2025") and membership.schema.json's start/end require a full ISO date --
fabricating a day would be a guessed default. Term span and verification
status are folded into the source note text instead, same treatment as
seed_tx_isd_people_atlarge_tsd2025.py gives its own unmappable-precision
fields.

Idempotent: person_id() is namespaced by (name, cdn) using the same fixed
UUID namespace as seed_tx_isd_people_atlarge.py, so a person already seeded
by an earlier pass under an identically-cleaned name is recognized and not
duplicated.

Usage: python3 seed_tx_isd_people_smd_hybrid.py [--write]
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
PEOPLE_DIR = DATA_DIR / "people" / "school"
MEMBERSHIPS_DIR = DATA_DIR / "memberships" / "school"
POSTS_DIR = DATA_DIR / "posts" / "school"

sys.path.insert(0, str(REPO / "scripts"))
from seed_tx_isd_organizations_posts import load_jurisdictions, org_id  # noqa: E402
from seed_tx_isd_people_atlarge import (  # noqa: E402
    person_id, slugify, to_name_case, unique_filename,
)

ROSTER_CSV = REPO / "reference" / "TX Rolling Audit" / "tx_isd_smd_hybrid_seat_roster_2026-09-02.csv"
RETRIEVED = "2026-09-02"
DOC_URL = (
    "https://docs.google.com/document/d/"
    "1uwA52vc6aTpXsJN20UN7L3t-2Lep2H10d6D_vaeSXBI"
)

ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10}

ROLE_NORMALIZE = {
    "MEMBER": "Trustee",
    "TRUSTEE / MEMBER": "Trustee",
    "BOARD MEMBER": "Trustee",
    "BOARD PRESIDENT": "President",
    "BOARD VICE PRESIDENT": "Vice President",
    "BOARD VICE-PRESIDENT": "Vice President",
    "VICE-PRESIDENT": "Vice President",
    "BOARD SECRETARY": "Secretary",
    "BOARD TREASURER": "Treasurer",
    "ASSISTANT BOARD SECRETARY": "Assistant Secretary",
}


def normalize_role(role):
    role = role.strip()
    return ROLE_NORMALIZE.get(role.upper(), role)


def parse_seat(seat_label, seat_type):
    """Returns ('at-large', None) / ('district', N) / (None, reason) to skip."""
    st = seat_type.lower()
    if seat_type.strip() == "Single-Member District / At-Large":
        return None, "ambiguous_seat_type"
    if "super district" in st:
        return "at-large", None
    if "at-large" in st or "at large" in st:
        return "at-large", None
    if re.search(r"\d+\s*/\s*\d+", seat_label):
        # e.g. "Precinct 3/4" -- doc couldn't resolve which numbered Post
        return None, "ambiguous_seat_number"
    m = re.search(r"\d+", seat_label)
    if m:
        return "district", int(m.group())
    for token in re.split(r"[\s()]+", seat_label):
        if token in ROMAN:
            return "district", ROMAN[token]
    return None, "no_seat_number_found"


def load_roster():
    with ROSTER_CSV.open(newline="") as f:
        return list(csv.DictReader(f))


def main():
    write = "--write" in sys.argv[1:]

    jurisdictions = load_jurisdictions()
    jur_by_cdn = jurisdictions  # already CDN -> {slug, jurisdiction_id, name}
    # load actual post ids (not just filenames) for a reliable check
    post_ids = set()
    for f in POSTS_DIR.glob("*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            post_ids.add(doc["id"])

    rows = load_roster()

    taken_person_slugs = {p.stem for p in PEOPLE_DIR.glob("*.yaml")}
    taken_membership_slugs = {p.stem for p in MEMBERSHIPS_DIR.glob("*.yaml")}
    existing_person_ids = set()
    for f in PEOPLE_DIR.glob("*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            existing_person_ids.add(doc["id"])
    existing_membership_ids = set()
    for f in MEMBERSHIPS_DIR.glob("*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            existing_membership_ids.add(doc["id"])

    stats = Counter()
    districts_touched = set()
    by_district_names = {}  # cdn -> list of trustee_name, for duplicate-in-district check

    for row in rows:
        cdn = row["tea_cdn"].strip().zfill(6)
        name_raw = row["trustee_name"].strip()
        if not name_raw:
            stats["skip_blank_name"] += 1
            continue
        if name_raw.lower() == "vacant":
            stats["skip_vacant"] += 1
            continue
        if "/" in name_raw:
            stats["skip_ambiguous_name"] += 1
            continue

        jur = jur_by_cdn.get(cdn)
        if not jur:
            stats["skip_no_jurisdiction"] += 1
            continue

        kind, val = parse_seat(row["seat_label"], row["seat_type"])
        if kind is None:
            stats[f"skip_{val}"] += 1
            continue

        if kind == "at-large":
            post_id = f"{jur['slug']}-tx-isd/trustee-at-large"
        else:
            post_id = f"{jur['slug']}-tx-isd/trustee-district-{val}"

        if post_id not in post_ids:
            stats["skip_post_not_found"] += 1
            continue

        by_district_names.setdefault(cdn, []).append(name_raw)

        name = to_name_case(name_raw)
        pid = person_id(name, cdn)
        role = normalize_role(row["board_role"])
        source_url = row["source_url"].strip()
        source_note = (
            f"TX ISD SMD/hybrid seat-mapping research doc (issue #13 follow-up, "
            f"{DOC_URL}), district {cdn} ({jur['name']}) -- seat "
            f"{row['seat_label']!r}, term {row['term_start']}-{row['term_end']}, "
            f"verification status: {row['verification_status']}. "
            f"Source: {row['source_title'] or source_url}."
        )

        if pid not in existing_person_ids:
            stats["person_new"] += 1
            filename = unique_filename(taken_person_slugs, slugify(name))
            person_doc = {
                "id": pid,
                "name": name,
                "candidacies": [],
                "verification": {
                    "status": "machine-extracted",
                    "reviewed_on": RETRIEVED,
                    "pipeline": "TX ISD SMD/hybrid seat-mapping research doc (issue #13 follow-up)",
                },
                "sources": [{"url": source_url, "note": source_note, "retrieved": RETRIEVED}],
            }
            if write:
                (PEOPLE_DIR / f"{filename}.yaml").write_text(
                    PEOPLE_HEADER + yaml.safe_dump(
                        person_doc, sort_keys=False, allow_unicode=True,
                        default_flow_style=False, width=1000,
                    )
                )
            existing_person_ids.add(pid)

        mem_base_slug = f"{jur['slug']}-tx-isd-trustee-{slugify(name)}"
        if mem_base_slug in existing_membership_ids:
            stats["skip_membership_already_exists"] += 1
            continue
        mem_slug = unique_filename(taken_membership_slugs, mem_base_slug)
        membership_doc = {
            "id": mem_slug,
            "person_id": pid,
            "organization_id": org_id(cdn),
            "post_id": post_id,
            "role": role,
            "sources": [{"url": source_url, "note": source_note, "retrieved": RETRIEVED}],
        }
        stats["membership_new"] += 1
        districts_touched.add(cdn)
        if write:
            (MEMBERSHIPS_DIR / f"{mem_slug}.yaml").write_text(
                MEMBERSHIPS_HEADER + yaml.safe_dump(
                    membership_doc, sort_keys=False, allow_unicode=True,
                    default_flow_style=False, width=1000,
                )
            )
        existing_membership_ids.add(mem_slug)

    for cdn, names in by_district_names.items():
        if len(names) != len(set(names)):
            stats["duplicate_name_in_district_warning"] += 1

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    print(f"districts_with_new_membership: {len(districts_touched)}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


PEOPLE_HEADER = (
    "# Seeded from the TX ISD SMD/hybrid seat-mapping research doc\n"
    "# (issue #13 follow-up) by scripts/seed_tx_isd_people_smd_hybrid.py.\n"
    "# See reference/TX Rolling Audit/tx_isd_smd_hybrid_seat_roster_2026-09-02.csv\n"
    "# for the full extracted source data.\n"
)
MEMBERSHIPS_HEADER = PEOPLE_HEADER


if __name__ == "__main__":
    main()
