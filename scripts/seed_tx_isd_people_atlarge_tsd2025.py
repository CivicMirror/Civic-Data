#!/usr/bin/env python3
"""
Phase 4a follow-up (at-large only): fill remaining vacant at-large trustee
seats using TEA's official "Texas Public School Districts and Charters:
Board Members..." export (TSD-2025-final.xlsx, March 2025), attached to
issue #13 comment 5496322162.

seed_tx_isd_people_atlarge.py already seeded the 862 pure at-large districts
from the TEA AskTED Staff Directory CSV. Re-running that script against a
2026-09-02 refresh of the same CSV source found zero new names -- that
export hadn't changed. This TSD export is a *different* TEA source (the
biennial print-directory data pull) and, checked district-by-district
against current seat counts, names 70 additional trustees across districts
that were seeded with an apparent vacancy from the CSV pull. Everything
else about scope and skip logic mirrors seed_tx_isd_people_atlarge.py:
pure at-large districts only (no seat-number field here either), same
over-count/duplicate-name caution, vacancies still imported as-is.

The sheet is laid out in blocks, not rows-with-columns: a "CNTY-DIST" row
(e.g. "197-902") starts each district's block, followed by one row per
staff member (name, role) until the next district's block starts. Roles
outside BOARD_ROLES (PEIMS Coordinator, Business Manager, Superintendent,
etc.) are non-elected staff and are skipped.

Idempotent: person_id() is namespaced by (name, cdn) using the same fixed
UUID namespace as seed_tx_isd_people_atlarge.py, so a person already seeded
from the CSV pull (identical cleaned name) is recognized and not
duplicated; only genuinely new names produce new Person/Membership records.

Usage: python3 seed_tx_isd_people_atlarge_tsd2025.py [--write]
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

import openpyxl
import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
PEOPLE_DIR = DATA_DIR / "people" / "school"
MEMBERSHIPS_DIR = DATA_DIR / "memberships" / "school"

sys.path.insert(0, str(REPO / "reference" / "TX Rolling Audit"))
from tx_isd_parse_structure import parse_district, EXCLUDED_TAGS  # noqa: E402

sys.path.insert(0, str(REPO / "scripts"))
from seed_tx_isd_organizations_posts import load_jurisdictions, org_id  # noqa: E402
from seed_tx_isd_people_atlarge import (  # noqa: E402
    person_id, slugify, to_name_case, unique_filename,
)

BBB_CSV = REPO / "reference" / "TX Rolling Audit" / "tx_isd_bbb_local_2026-08-24.csv"
TSD_XLSX = REPO / "reference" / "TX Rolling Audit" / "TSD-2025-final.xlsx"
RETRIEVED = "2026-09-02"
SOURCE_URL = (
    "https://github.com/CivicMirror/Civic-Data/files/31700042/TSD-2025-final.xlsx"
)

BOARD_ROLES = {
    "BOARD PRESIDENT", "BOARD VICE-PRESIDENT", "BOARD SECRETARY",
    "BOARD TREASURER", "BOARD ASSISTANT SECRETARY", "BOARD MEMBER",
}
CNTY_DIST_RE = re.compile(r"^\d{3}-\d{3}$")
TITLE_TOKENS = {"DR", "MR", "MRS", "MS", "REV", "HON", "JUDGE"}


def clean_full_name(raw):
    s = re.sub(r",\s*", " ", raw.strip())
    tokens = [t for t in s.split() if t]
    while tokens and tokens[0].upper().rstrip(".") in TITLE_TOKENS:
        tokens.pop(0)
    return " ".join(tokens)


def load_tsd_board_members():
    wb = openpyxl.load_workbook(TSD_XLSX, read_only=True)
    ws = wb["Board of Trustee Members"]
    by_cdn = {}
    cur_cdn = None
    for row in ws.iter_rows(values_only=True):
        a, b = row[0], row[1]
        if isinstance(a, str) and CNTY_DIST_RE.match(a):
            cur_cdn = a.replace("-", "").zfill(6)
            by_cdn.setdefault(cur_cdn, [])
            continue
        if cur_cdn and isinstance(a, str) and b in BOARD_ROLES:
            by_cdn[cur_cdn].append((a.strip(), b.strip()))
    return by_cdn


def main():
    write = "--write" in sys.argv[1:]

    jurisdictions = load_jurisdictions()
    bbb_by_cdn = {r["tea_cdn"]: r for r in csv.DictReader(BBB_CSV.open(newline=""))}
    tsd_by_cdn = load_tsd_board_members()

    taken_person_slugs = {p.stem for p in PEOPLE_DIR.glob("*.yaml")}
    taken_membership_slugs = {p.stem for p in MEMBERSHIPS_DIR.glob("*.yaml")}
    existing_person_ids = set()
    for f in PEOPLE_DIR.glob("*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            existing_person_ids.add(doc["id"])
    existing_membership_ids = set()
    membership_count_by_post = Counter()
    for f in MEMBERSHIPS_DIR.glob("*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            existing_membership_ids.add(doc["id"])
        if "post_id" in doc:
            membership_count_by_post[doc["post_id"]] += 1

    stats = Counter()

    for cdn, jur in sorted(jurisdictions.items()):
        bbb_row = bbb_by_cdn.get(cdn)
        if not bbb_row or bbb_row["heuristic_structure"] in EXCLUDED_TAGS:
            continue
        plan = parse_district(cdn, bbb_row["local_text"])
        if "skip_reason" in plan or plan["smd_seats"] > 0:
            continue

        post_id = f"{jur['slug']}-tx-isd/trustee"
        already_seated = membership_count_by_post.get(post_id, 0)
        if already_seated >= plan["board_size"]:
            continue  # fully seeded already, nothing to check here

        trows = tsd_by_cdn.get(cdn, [])
        named = [(clean_full_name(n), r) for n, r in trows if n.strip()]
        if len(named) > plan["board_size"]:
            stats["skip_over_count"] += 1
            continue
        names_only = [n for n, _ in named]
        if len(names_only) != len(set(names_only)):
            stats["skip_duplicate_name_in_district"] += 1
            continue
        if not named:
            stats["skip_no_named_rows"] += 1
            continue

        organization_id = org_id(cdn)
        source_note = (
            f"TEA official district directory export (TSD-2025-final.xlsx, "
            f"March 2025 -- issue #13 comment 5496322162), district {cdn} "
            f"({jur['name']}) -- board roster, filling a seat left vacant by "
            f"the AskTED staff-directory pull."
        )

        district_added = 0
        for raw_name, role in named:
            name = to_name_case(raw_name)
            pid = person_id(name, cdn)
            if pid in existing_person_ids:
                continue  # already seeded from the other CSV pull

            stats["person_new"] += 1
            filename = unique_filename(taken_person_slugs, slugify(name))
            person_doc = {
                "id": pid,
                "name": name,
                "candidacies": [],
                "verification": {
                    "status": "machine-extracted",
                    "reviewed_on": RETRIEVED,
                    "pipeline": "TEA TSD district directory export (TSD-2025-final.xlsx)",
                },
                "sources": [{"url": SOURCE_URL, "note": source_note, "retrieved": RETRIEVED}],
            }
            if write:
                (PEOPLE_DIR / f"{filename}.yaml").write_text(
                    HEADER + yaml.safe_dump(person_doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
                )
            existing_person_ids.add(pid)

            mem_base_slug = f"{jur['slug']}-tx-isd-trustee-{slugify(name)}"
            if mem_base_slug in existing_membership_ids:
                continue
            mem_slug = unique_filename(taken_membership_slugs, mem_base_slug)
            membership_doc = {
                "id": mem_slug,
                "person_id": pid,
                "organization_id": organization_id,
                "post_id": post_id,
                "role": role,
                "sources": [{"url": SOURCE_URL, "note": source_note, "retrieved": RETRIEVED}],
            }
            stats["membership_new"] += 1
            district_added += 1
            if write:
                (MEMBERSHIPS_DIR / f"{mem_slug}.yaml").write_text(
                    HEADER + yaml.safe_dump(membership_doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
                )
            existing_membership_ids.add(mem_slug)

        if district_added:
            stats["district_improved"] += 1

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded from TEA's official TSD-2025-final.xlsx district directory\n"
    "# export by scripts/seed_tx_isd_people_atlarge_tsd2025.py (Phase 4a\n"
    "# follow-up -- see issue #13 comment 5496322162). Fills at-large seats\n"
    "# left vacant by the AskTED staff-directory pull; single-member-\n"
    "# district and hybrid boards are still out of scope for this source.\n"
)


if __name__ == "__main__":
    main()
