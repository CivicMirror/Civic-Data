#!/usr/bin/env python3
"""
Import the 13 Norfolk-Oakham municipalities from the v30 rolling package into
data/us/ma/{organizations,posts,people,memberships}/municipal/.

v30 is a *rolling* (cumulative) package, not a delta: it carries all 215
municipalities audited through Oakham, ~1200 of whose records are already in
this repo. Only the towns with no elected-office coverage at all are imported
here -- Norfolk, North Andover, North Attleborough, North Brookfield, North
Reading, Northborough, Northbridge, Northfield, Norton, Norwell, Norwood, Oak
Bluffs and Oakham. Everything else in the file is deliberately left alone, for
two reasons:

  * v30 shares the v20/v27 id lineage, and its ids agree with this repo for
    1204 of the 1223 organizations they have in common. Re-importing them
    would churn a large amount of already-correct data for no gain.
  * The 19 they disagree on are exactly the offices that
    fix_ma_stale_office_conflicts.py upgraded to newer v33/v41/v47/v54
    research. v30 still carries the superseded v20-era organization ids for
    those, and its memberships point at them. Importing those rows would
    reintroduce the dangling-reference bug that script just fixed, because a
    filename conflict skips the organization while the membership referencing
    it still gets written.

v30 also spells Oak Bluffs' jurisdiction as `place:oak_bluffs` while this
repo's Census-sourced jurisdiction record is `oak-bluffs` (its office ids
already use the hyphen -- only jurisdiction_id is affected). PLACE_FIXUPS
corrects that on load, and every resulting jurisdiction_id is verified against
the jurisdictions on disk before anything is written.

Placement rules (filenames, membership id regeneration, and why persons are
never merged into existing repo people by name match) follow
scripts/import_ma_charter_audit_v20.py unchanged.

Idempotent by id AND by filename -- never overwrites.

Usage: python3 import_ma_charter_audit_v30_rolling.py [--write]
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "ma"
SRC_DIR = REPO / "reference" / "MA Rolling Audit" / "ma_charter_audit_rolling_v30_2026-08-25"
VERSION = "v30"

# Municipalities with no elected-office coverage before this import.
TOWNS = {
    "norfolk", "north-andover", "north-attleborough", "north-brookfield",
    "north-reading", "northborough", "northbridge", "northfield", "norton",
    "norwell", "norwood", "oak-bluffs", "oakham",
}

# Source-package place slugs that don't match this repo's jurisdiction records.
PLACE_FIXUPS = {
    "oak_bluffs": "oak-bluffs",
}

HEADER = (
    "# Imported from reference/MA Rolling Audit/ (v30 MA municipal charter/\n"
    "# elected-office rolling audit package, generated 2026-08-25) by scripts/\n"
    "# import_ma_charter_audit_v30_rolling.py. Source rows were machine-\n"
    "# extracted from municipal government sites; see the record's sources for\n"
    "# provenance.\n"
)


def slugify(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def apply_place_fixups(obj):
    if isinstance(obj, str):
        for bad, good in PLACE_FIXUPS.items():
            obj = obj.replace(bad, good)
        return obj
    if isinstance(obj, list):
        return [apply_place_fixups(v) for v in obj]
    if isinstance(obj, dict):
        return {k: apply_place_fixups(v) for k, v in obj.items()}
    return obj


def load(kind):
    name = f"ma_schema_ready_{kind}_rolling_2026-08-25_{VERSION}.json"
    return apply_place_fixups(json.loads((SRC_DIR / name).read_text()))


class Recorder:
    def __init__(self, write):
        self.write = write
        self.stats = {}

    def emit(self, kind, doc, filename):
        singular = kind.rstrip("s")
        path = DATA_DIR / kind / "municipal" / filename

        if path.exists():
            existing = yaml.safe_load(path.read_text()) or {}
            if existing.get("id") == doc["id"]:
                self.stats[f"{singular}_existing"] = self.stats.get(f"{singular}_existing", 0) + 1
            else:
                self.stats[f"{singular}_skipped_filename_conflict"] = (
                    self.stats.get(f"{singular}_skipped_filename_conflict", 0) + 1
                )
            return False

        self.stats[f"{singular}_new"] = self.stats.get(f"{singular}_new", 0) + 1
        if self.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            text = HEADER + yaml.safe_dump(
                doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000
            )
            path.write_text(text)
        return True


def unique_filename(taken, base_slug, suffix):
    slug = base_slug
    if slug in taken:
        slug = f"{base_slug}-{suffix}"
    taken.add(slug)
    return f"{slug}.yaml"


def place_of(org):
    m = re.search(r"place:([^/]+)", org.get("jurisdiction_id", "") or "")
    return m.group(1) if m else None


def main():
    write = "--write" in sys.argv[1:]

    all_orgs = load("organizations")
    all_posts = load("posts")
    all_persons = load("persons")
    all_memberships = load("memberships")

    # Narrow to the target towns, then follow the graph outwards so the slice
    # is self-contained: orgs -> posts -> memberships -> persons.
    orgs = [o for o in all_orgs if place_of(o) in TOWNS]
    org_ids = {o["id"] for o in orgs}
    posts = [p for p in all_posts if p["organization_id"] in org_ids]
    post_ids = {p["id"] for p in posts}
    memberships = [m for m in all_memberships if m["post_id"] in post_ids]
    person_ids = {m["person_id"] for m in memberships}
    persons = [p for p in all_persons if p["id"] in person_ids]

    print(f"v30 slice for {len(TOWNS)} towns: {len(orgs)} organizations, "
          f"{len(posts)} posts, {len(persons)} persons, "
          f"{len(memberships)} memberships")

    missing_towns = TOWNS - {place_of(o) for o in orgs}
    if missing_towns:
        print(f"WARNING: no organizations found for: {', '.join(sorted(missing_towns))}")

    rec = Recorder(write)

    known_places = set()
    for f in (DATA_DIR / "jurisdictions" / "municipal").glob("*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        m = re.search(r"place:([^/]+)", doc.get("id", "") or "")
        if m:
            known_places.add(m.group(1))

    unknown = sorted({place_of(o) for o in orgs} - known_places, key=str)
    if unknown:
        print("ERROR: organizations reference unknown jurisdictions:")
        for place in unknown:
            print(f"  place:{place}")
        print("\nNo records written. Add the slug to PLACE_FIXUPS (or add the "
              "jurisdiction) and re-run.")
        sys.exit(1)

    def id_index(kind):
        idx = {}
        for f in (DATA_DIR / kind).glob("*/*.yaml"):
            doc = yaml.safe_load(f.read_text()) or {}
            if "id" in doc:
                idx[doc["id"]] = f
        return idx

    existing_post_ids = id_index("posts")
    skipped_post_ids = set()

    for org in orgs:
        office_id = next(
            (i["identifier"] for i in org["identifiers"] if i["scheme"] == "civicmirror-office"),
            org["id"],
        )
        target_path = DATA_DIR / "posts" / "municipal" / f"{office_id.replace('/', '-')}.yaml"
        existing_file = existing_post_ids.get(office_id)
        if existing_file is not None and existing_file != target_path:
            rec.stats["post_skipped_id_conflict"] = rec.stats.get("post_skipped_id_conflict", 0) + 1
            rec.stats["organization_skipped_id_conflict"] = rec.stats.get("organization_skipped_id_conflict", 0) + 1
            skipped_post_ids.add(office_id)
            continue
        rec.emit("organizations", org, f"{office_id.replace('/', '-')}.yaml")

    for post in posts:
        if post["id"] in skipped_post_ids:
            continue
        rec.emit("posts", post, f"{post['id'].replace('/', '-')}.yaml")

    existing_person_ids = set()
    for f in (DATA_DIR / "people").glob("*/*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            existing_person_ids.add(doc["id"])

    persons_with_surviving_membership = {
        mem["person_id"] for mem in memberships if mem["post_id"] not in skipped_post_ids
    }

    taken_slugs = {p.stem for p in (DATA_DIR / "people" / "municipal").glob("*.yaml")}
    for person in persons:
        if person["id"] in existing_person_ids:
            rec.stats["person_existing"] = rec.stats.get("person_existing", 0) + 1
            continue
        if person["id"] not in persons_with_surviving_membership:
            rec.stats["person_skipped_no_surviving_membership"] = (
                rec.stats.get("person_skipped_no_surviving_membership", 0) + 1
            )
            continue
        base_slug = slugify(person["name"])
        suffix = person["id"].rsplit("/", 1)[-1][:8]
        rec.emit("people", person, unique_filename(taken_slugs, base_slug, suffix))

    existing_membership_pairs = set()
    for f in (DATA_DIR / "memberships").glob("*/*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "person_id" in doc and "post_id" in doc:
            existing_membership_pairs.add((doc["person_id"], doc["post_id"]))

    taken_membership_slugs = {p.stem for p in (DATA_DIR / "memberships" / "municipal").glob("*.yaml")}
    persons_by_id = {p["id"]: p for p in persons}

    for mem in memberships:
        if mem["post_id"] in skipped_post_ids:
            rec.stats["membership_skipped_id_conflict"] = rec.stats.get("membership_skipped_id_conflict", 0) + 1
            continue
        if (mem["person_id"], mem["post_id"]) in existing_membership_pairs:
            rec.stats["membership_existing"] = rec.stats.get("membership_existing", 0) + 1
            continue
        person = persons_by_id[mem["person_id"]]
        surname = person["name"].split()[-1]
        post_slug = mem["post_id"].replace("/", "-")
        base_slug = f"{post_slug}-{slugify(surname)}"
        suffix = mem["id"].rsplit("/", 1)[-1][:8]
        new_id = unique_filename(taken_membership_slugs, base_slug, suffix)[:-len(".yaml")]

        doc = dict(mem)
        doc["id"] = new_id
        rec.emit("memberships", doc, f"{new_id}.yaml")

    print("\n==================== SUMMARY ====================")
    for k in sorted(rec.stats):
        print(f"{k}: {rec.stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


if __name__ == "__main__":
    main()
