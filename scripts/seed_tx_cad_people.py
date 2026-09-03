#!/usr/bin/env python3
"""
Seed Person/Membership records for TX Central Appraisal District elected
directors (the 3 popularly-elected "Place" seats per qualifying county's
board -- see issue #28), from per-county research batches.

No bulk officeholder source exists: these seats were filled for the first
time in a May 4, 2024 special election (not the November 2024 general
already imported for other TX county offices under #25), so each county
needs individual discovery of its own election-results source (official
county elections-office canvass/results PDF where findable, otherwise a
news article confirming the winner). A county CAD's own "our board" page
is NOT sufficient sourcing on its own unless it explicitly labels which
members are elected (vs. appointed/ex officio) -- most don't, and get
skipped rather than guessed.

Reads every reference/TX Rolling Audit/tx_cad_officeholders_batch*_*.csv
file present (idempotent by person/membership id, same pattern as
seed_tx_ccd_people.py).

CSV columns: county_slug, post_id, director_name, role, source_title,
source_url, retrieved.

Usage: python3 seed_tx_cad_people.py [--write]
"""
import csv
import glob
import sys
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
PEOPLE_DIR = DATA_DIR / "people" / "appraisal"
MEMBERSHIPS_DIR = DATA_DIR / "memberships" / "appraisal"
POSTS_DIR = DATA_DIR / "posts" / "appraisal"
SRC_DIR = REPO / "reference" / "TX Rolling Audit"

sys.path.insert(0, str(REPO / "scripts"))
from seed_tx_cad_organizations_posts import org_id  # noqa: E402
from seed_tx_isd_people_atlarge import (  # noqa: E402
    person_id, slugify, to_name_case, unique_filename,
)

PEOPLE_HEADER = (
    "# Seeded from per-county officeholder research (issue #28) by\n"
    "# scripts/seed_tx_cad_people.py. See reference/TX Rolling Audit/\n"
    "# tx_cad_officeholders_batch*_*.csv for the full source data.\n"
)
MEMBERSHIPS_HEADER = PEOPLE_HEADER


def load_batches():
    rows = []
    for path in sorted(glob.glob(str(SRC_DIR / "tx_cad_officeholders_batch*_*.csv"))):
        with open(path, newline="") as f:
            rows.extend(csv.DictReader(f))
    return rows


def main():
    write = "--write" in sys.argv[1:]

    post_ids = set()
    for f in POSTS_DIR.glob("*-tx-cad-*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            post_ids.add(doc["id"])

    rows = load_batches()

    PEOPLE_DIR.mkdir(parents=True, exist_ok=True)
    MEMBERSHIPS_DIR.mkdir(parents=True, exist_ok=True)

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
        slug = row["county_slug"].strip()
        post_id = row["post_id"].strip()
        if post_id not in post_ids:
            stats["skip_post_not_found"] += 1
            print(f"POST NOT FOUND: {post_id!r} (row for {row['director_name']!r})")
            continue

        name_raw = row["director_name"].strip()
        if not name_raw:
            stats["skip_blank_name"] += 1
            continue

        name = to_name_case(name_raw)
        pid = person_id(name, slug)
        role = row["role"].strip() or "Director"
        source_url = row["source_url"].strip()
        source_note = f"CAD officeholder research (issue #28) -- {row['source_title']}."
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
                    "pipeline": "TX CAD officeholder research (issue #28)",
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

        mem_base_slug = f"{slug}-tx-cad-director-{slugify(name)}"
        if mem_base_slug in existing_membership_ids:
            stats["skip_membership_already_exists"] += 1
            continue
        mem_slug = unique_filename(taken_membership_slugs, mem_base_slug)
        membership_doc = {
            "id": mem_slug,
            "person_id": pid,
            "organization_id": org_id(slug),
            "post_id": post_id,
            "role": role,
            "how_seated": "elected",
        }
        term_start = row.get("term_start", "").strip()
        if term_start:
            membership_doc["start"] = term_start
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
