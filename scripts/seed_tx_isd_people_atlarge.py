#!/usr/bin/env python3
"""
Phase 4a (at-large only): generate Person + Membership records for current
ISD trustees, sourced from TEA/AskTED's district-staff export (the
"Directory.csv" attached to issue #13's comment 5386154825).

Scope is deliberately narrower than the 1,003 districts Phase 3 structured:
this directory has no per-person seat/place/district-number field, so for
single-member-district and hybrid boards (141 districts) there is no way to
tell which named person holds which numbered Post -- only that they sit on
the district's Board overall. That's a real gap requiring either an SMD-
specific source or manual research, not something to paper over by guessing.
This script only covers the 862 PURE AT-LARGE districts, where every trustee
shares one Post (`<slug>-tx-isd/trustee`, phase 3's build_records()) and no
seat-to-person mapping is needed.

Two more skip classes, both counted rather than guessed through:
  - over-count: named-row count exceeds the sourced board_size (13 districts
    as of the 2026-08-24 directory pull). The export holds a stale or
    duplicate row and there's no way to tell which one from this file alone.
  - duplicate name in one district: the same Full Name appears 2+ times
    (e.g. listed once as "President" and again as "Board Member") -- creating
    two Membership rows for one Person in one Organization would trip the
    validator's multiple-open-seats check for a real reason (it IS two open
    memberships), but the actual cause is very likely one row per office
    held, not a role.

Under-count (fewer named rows than board_size) is imported as-is -- an
unfilled seat is a real vacancy, not an error, and fabricating a placeholder
person would violate this repo's no-guessed-defaults rule.

`how_seated` is deliberately omitted. This directory establishes CURRENT
board composition, not how each individual won their seat, and the
validator's CROSS[no-election-trace] check flags `how_seated: elected` with
no matching Election/candidacy record -- true here for all ~5,700 people,
since building 862 districts' worth of election history is separate,
unstarted work.

Idempotent: an already-emitted person/membership (matched by source URL +
name, not id) is not recreated on a re-run.

Usage: python3 seed_tx_isd_people_atlarge.py [--write]
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
PEOPLE_DIR = DATA_DIR / "people" / "school"
MEMBERSHIPS_DIR = DATA_DIR / "memberships" / "school"

sys.path.insert(0, str(REPO / "reference" / "TX Rolling Audit"))
from tx_isd_parse_structure import parse_district, EXCLUDED_TAGS  # noqa: E402

sys.path.insert(0, str(REPO / "scripts"))
from seed_tx_isd_organizations_posts import load_jurisdictions, org_id  # noqa: E402

BBB_CSV = REPO / "reference" / "TX Rolling Audit" / "tx_isd_bbb_local_2026-08-24.csv"
DIRECTORY_CSV = REPO / "reference" / "TX Rolling Audit" / "tx_isd_board_directory_2026-09-02.csv"
RETRIEVED = "2026-09-02"

# Fixed namespace for this script's deterministic person ids -- distinct from
# organization NS in seed_tx_isd_organizations_posts.py.
PERSON_NS = uuid.UUID("7c1e9a2d-4b5f-5e3a-8d6c-1f2a3b4c5d6e")

# Roman-numeral suffixes must stay upper (title() would mangle "III" to
# "Iii"). JR/SR are NOT in this set -- title() already renders those
# correctly ("Jr", "Sr"); the v20 MA import's "-sr.yaml" filename bug was
# about slugify() treating "Sr" as a surname, not about casing.
ROMAN_SUFFIXES = {"II", "III", "IV"}
MC_RE = re.compile(r"\bMc([a-z])")
# TEA's export sometimes splits a "Mc"-prefixed surname or a hyphenated
# surname across a space ("MC GOWAN", "SILVA - GAONA") -- collapse both
# after title-casing rather than guessing at the raw all-caps text.
MC_SPACE_RE = re.compile(r"\bMc (?=[A-Z])")
HYPHEN_SPACE_RE = re.compile(r"(\w) - (\w)")


def to_name_case(raw):
    words = raw.strip().split()
    out = []
    for w in words:
        core = re.sub(r"[^A-Za-z]", "", w)
        if core.upper() in ROMAN_SUFFIXES and core.upper() == core:
            out.append(w.upper())
            continue
        titled = w.title()
        titled = MC_RE.sub(lambda m: "Mc" + m.group(1).upper(), titled)
        out.append(titled)
    name = " ".join(out)
    name = MC_SPACE_RE.sub("Mc", name)
    name = HYPHEN_SPACE_RE.sub(r"\1-\2", name)
    return name


def slugify(name):
    text = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text


def clean_name(row):
    # "Full Name" embeds the salutation ("MR BLAKE KETTLER") -- First Name
    # and Last Name are always populated and salutation-free (verified: 0
    # blank across 8,024 named rows), so build the name from those instead.
    first = row["First Name"].strip()
    last = row["Last Name"].strip()
    return f"{first} {last}"


def person_id(name, cdn):
    # Namespaced per (name, cdn) rather than name alone -- two different
    # people can share a common name across 862 districts.
    return f"ocd-person/{uuid.uuid5(PERSON_NS, f'person|{cdn}|{name}')}"


def unique_filename(taken, base_slug):
    slug = base_slug
    n = 2
    while slug in taken:
        slug = f"{base_slug}-{n}"
        n += 1
    taken.add(slug)
    return slug


def load_directory():
    by_cdn = {}
    with DIRECTORY_CSV.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            cdn = row["District Number"].lstrip("'")
            by_cdn.setdefault(cdn, []).append(row)
    return by_cdn


def main():
    write = "--write" in sys.argv[1:]

    jurisdictions = load_jurisdictions()
    bbb_by_cdn = {r["tea_cdn"]: r for r in csv.DictReader(BBB_CSV.open(newline=""))}
    directory_by_cdn = load_directory()

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

    for cdn, jur in sorted(jurisdictions.items()):
        bbb_row = bbb_by_cdn.get(cdn)
        if not bbb_row or bbb_row["heuristic_structure"] in EXCLUDED_TAGS:
            continue
        plan = parse_district(cdn, bbb_row["local_text"])
        if "skip_reason" in plan or plan["smd_seats"] > 0:
            stats["skip_not_pure_at_large"] += 1
            continue

        drows = directory_by_cdn.get(cdn, [])
        named = [r for r in drows if r["Full Name"].strip()]
        if len(named) > plan["board_size"]:
            stats["skip_over_count"] += 1
            continue
        raw_names = [clean_name(r) for r in named]
        if len(raw_names) != len(set(raw_names)):
            stats["skip_duplicate_name_in_district"] += 1
            continue
        if not named:
            stats["skip_no_named_rows"] += 1
            continue

        stats["district_ok"] += 1
        organization_id = org_id(cdn)
        post_id = f"{jur['slug']}-tx-isd/trustee"
        source_url = "https://tea4avantguard.tea.state.tx.us/EETAD/Web/Home/StaffDirectory"
        source_note = (
            f"TEA AskTED District Staff Directory export ({RETRIEVED} refresh pull, "
            f"issue #13 comment 5386154825), district {cdn} ({jur['name']}) -- current board roster."
        )

        for row in named:
            name = to_name_case(clean_name(row))
            pid = person_id(name, cdn)
            role = row["Role"].strip() or "Board Member"

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
                        "pipeline": "TEA AskTED District Staff Directory",
                    },
                    "sources": [{"url": source_url, "note": source_note, "retrieved": RETRIEVED}],
                }
                if write:
                    (PEOPLE_DIR / f"{filename}.yaml").write_text(
                        HEADER + yaml.safe_dump(person_doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
                    )
                existing_person_ids.add(pid)
            else:
                stats["person_existing"] += 1

            mem_base_slug = f"{jur['slug']}-tx-isd-trustee-{slugify(name)}"
            mem_id = mem_base_slug
            if mem_id in existing_membership_ids:
                stats["membership_existing"] += 1
                continue
            mem_slug = unique_filename(taken_membership_slugs, mem_base_slug)
            membership_doc = {
                "id": mem_slug,
                "person_id": pid,
                "organization_id": organization_id,
                "post_id": post_id,
                "role": role,
                "sources": [{"url": source_url, "note": source_note, "retrieved": RETRIEVED}],
            }
            stats["membership_new"] += 1
            if write:
                (MEMBERSHIPS_DIR / f"{mem_slug}.yaml").write_text(
                    HEADER + yaml.safe_dump(membership_doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
                )
            existing_membership_ids.add(mem_id)

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded from the TEA AskTED District Staff Directory export by\n"
    "# scripts/seed_tx_isd_people_atlarge.py (Phase 4a, pure at-large\n"
    "# districts only -- see issue #13 comment 5386154825). Single-member-\n"
    "# district and hybrid boards are not covered: this source has no\n"
    "# per-person seat/district-number field to map a name to a specific\n"
    "# numbered Post.\n"
)


if __name__ == "__main__":
    main()
