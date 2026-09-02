#!/usr/bin/env python3
"""
Seed Person/Membership records for TX community college district trustees
from per-district research batches (see issue #14). Unlike the ISD audit,
no bulk officeholder source exists for CCDs (THECB, CCATT, and TACC were all
checked and ruled out in this issue's early comments) -- every seat is
sourced individually from each district's own board page or (when that page
doesn't label seats) a county election canvass, one CSV batch at a time.

Reads every reference/TX Rolling Audit/tx_ccd_officeholders_batch*_*.csv
file present (so a re-run after adding a new batch file picks up only the
new rows -- idempotent by person/membership id, same as every other seeder
in this audit). Each row already carries the EXACT target post_id (computed
by hand/research per batch, not derived by a generic seat-label parser --
CCD seat labels are too inconsistent across districts, e.g. numbered
Districts, numbered Places, or Hill College's town names, to be worth a
shared regex the way ISD single-member districts were).

CSV columns: ccd_slug, post_id, trustee_name, role, seat, source_title,
source_url, retrieved. `seat` is optional free text (e.g. "Place 4",
"Position 2") for districts where the source names a specific seat/position
number even though the Post itself is a shared at-large bloc --
membership.seat is exactly this field (see schemas/membership.schema.json);
an empty `seat` is fine and common (most at-large districts' own board
pages don't publish a position number per trustee).

Skip rather than guess: a row is simply omitted from the CSV rather than
included with a placeholder when a seat is vacant or a name is
ambiguous/unconfirmed -- there is no dedicated skip-tracking here because
the skip decision already happened during research, before the CSV was
written (contrast with seed_tx_isd_people_smd_hybrid.py, which parses a
single large machine-extractable source and needs its own skip logic).

Usage: python3 seed_tx_ccd_people.py [--write]
"""
import csv
import glob
import sys
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
PEOPLE_DIR = DATA_DIR / "people" / "school"
MEMBERSHIPS_DIR = DATA_DIR / "memberships" / "school"
POSTS_DIR = DATA_DIR / "posts" / "school"
SRC_DIR = REPO / "reference" / "TX Rolling Audit"

sys.path.insert(0, str(REPO / "scripts"))
from seed_tx_ccd_organizations_posts import load_jurisdictions, org_id  # noqa: E402
from seed_tx_isd_people_atlarge import (  # noqa: E402
    person_id, slugify, to_name_case, unique_filename,
)

PEOPLE_HEADER = (
    "# Seeded from per-district officeholder research (issue #14) by\n"
    "# scripts/seed_tx_ccd_people.py. See reference/TX Rolling Audit/\n"
    "# tx_ccd_officeholders_batch*_*.csv for the full source data.\n"
)
MEMBERSHIPS_HEADER = PEOPLE_HEADER


def load_batches():
    rows = []
    for path in sorted(glob.glob(str(SRC_DIR / "tx_ccd_officeholders_batch*_*.csv"))):
        with open(path, newline="") as f:
            rows.extend(csv.DictReader(f))
    return rows


def main():
    write = "--write" in sys.argv[1:]

    jurisdictions_by_fice = load_jurisdictions()
    # This script keys off ccd_slug (from the CSV), not fice -- build a
    # slug -> fice reverse index from the same jurisdiction data.
    fice_by_slug = {j["slug"]: fice for fice, j in jurisdictions_by_fice.items()}

    post_ids = set()
    for f in POSTS_DIR.glob("*-tx-ccd-*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            post_ids.add(doc["id"])

    rows = load_batches()

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

    for row in rows:
        slug = row["ccd_slug"].strip()
        fice = fice_by_slug.get(slug)
        if not fice:
            stats["skip_unknown_slug"] += 1
            print(f"UNKNOWN SLUG: {slug!r} (row for {row['trustee_name']!r})")
            continue

        post_id = row["post_id"].strip()
        if post_id not in post_ids:
            stats["skip_post_not_found"] += 1
            print(f"POST NOT FOUND: {post_id!r} (row for {row['trustee_name']!r})")
            continue

        name_raw = row["trustee_name"].strip()
        if not name_raw:
            stats["skip_blank_name"] += 1
            continue

        name = to_name_case(name_raw)
        pid = person_id(name, fice)
        role = row["role"].strip() or "Trustee"
        seat = row.get("seat", "").strip()
        source_url = row["source_url"].strip()
        source_note = (
            f"CCD officeholder research (issue #14), district {fice} "
            f"({jurisdictions_by_fice[fice]['name']}) -- {row['source_title']}."
        )
        retrieved = row["retrieved"].strip()

        if pid not in existing_person_ids:
            stats["person_new"] += 1
            filename = unique_filename(taken_person_slugs, slugify(name))
            person_doc = {
                "id": pid,
                "name": name,
                "candidacies": [],
                "verification": {
                    "status": "machine-extracted",
                    "reviewed_on": retrieved,
                    "pipeline": "TX CCD officeholder research (issue #14)",
                },
                "sources": [{"url": source_url, "note": source_note, "retrieved": retrieved}],
            }
            if write:
                (PEOPLE_DIR / f"{filename}.yaml").write_text(
                    PEOPLE_HEADER + yaml.safe_dump(
                        person_doc, sort_keys=False, allow_unicode=True,
                        default_flow_style=False, width=1000,
                    )
                )
            existing_person_ids.add(pid)

        mem_base_slug = f"{slug}-tx-ccd-trustee-{slugify(name)}"
        if mem_base_slug in existing_membership_ids:
            stats["skip_membership_already_exists"] += 1
            continue
        mem_slug = unique_filename(taken_membership_slugs, mem_base_slug)
        membership_doc = {
            "id": mem_slug,
            "person_id": pid,
            "organization_id": org_id(fice),
            "post_id": post_id,
            "role": role,
        }
        if seat:
            membership_doc["seat"] = seat
        membership_doc["sources"] = [{"url": source_url, "note": source_note, "retrieved": retrieved}]
        stats["membership_new"] += 1
        if write:
            (MEMBERSHIPS_DIR / f"{mem_slug}.yaml").write_text(
                MEMBERSHIPS_HEADER + yaml.safe_dump(
                    membership_doc, sort_keys=False, allow_unicode=True,
                    default_flow_style=False, width=1000,
                )
            )
        existing_membership_ids.add(mem_slug)

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


if __name__ == "__main__":
    main()
