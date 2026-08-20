#!/usr/bin/env python3
"""
Import the v20 MA municipal charter/elected-office rolling audit
(`reference/MA Rolling Audit  V20/`) into data/us/ma/{organizations,posts,
people,memberships}/municipal/.

Source files are already schema-ready (validated against organization.schema.json,
post.schema.json, person.schema.json, membership.schema.json before this script
is run) -- this script only handles repo placement: filenames, idempotency, and
regenerating membership ids to match this repo's human-readable slug convention
(the source file uses "ocd-membership/<uuid>" ids, which is valid per-schema but
inconsistent with every other membership record in this repo).

Deliberately does NOT attempt to merge new persons into existing repo people by
normalized-name match (the pattern used in build_ma_mayors_people.py / build_
federal_records.py): a charter-audit officeholder and an OCPF candidacy record
sharing a common name (e.g. "Michael McGee") are not verifiably the same person
without a stronger identity signal (address, DOB, office history) than name
alone, and this batch's source municipalities were not cross-checked against
OCPF district/committee data. Wrongly merging two different people would
corrupt both bios. Each v20 person is written to a new person record; a
same-name existing repo entry, if any, is left alone.

Idempotent by id AND by filename -- never overwrites.

Usage: python3 import_ma_charter_audit_v20.py [--write]
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "ma"
SRC_DIR = REPO / "reference" / "MA Rolling Audit  V20"

HEADER = (
    "# Imported from reference/MA Rolling Audit  V20/ (MA municipal charter/\n"
    "# elected-office rolling audit, generated 2026-08-20) by scripts/\n"
    "# import_ma_charter_audit_v20.py. Source rows were machine-extracted from\n"
    "# municipal government sites; see the record's sources for provenance.\n"
)


def slugify(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def load(name):
    return json.loads((SRC_DIR / name).read_text())


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


def main():
    write = "--write" in sys.argv[1:]

    orgs = load("ma_schema_ready_organizations_rolling_2026-08-20_v20.json")
    posts = load("ma_schema_ready_posts_rolling_2026-08-20_v20.json")
    persons = load("ma_schema_ready_persons_rolling_2026-08-20_v20.json")
    memberships = load("ma_schema_ready_memberships_rolling_2026-08-20_v20.json")

    rec = Recorder(write)

    # --- organizations & posts: filename derived from the civicmirror-office / post id ---
    for org in orgs:
        office_id = next(
            (i["identifier"] for i in org["identifiers"] if i["scheme"] == "civicmirror-office"),
            org["id"],
        )
        rec.emit("organizations", org, f"{office_id.replace('/', '-')}.yaml")

    for post in posts:
        rec.emit("posts", post, f"{post['id'].replace('/', '-')}.yaml")

    # --- persons: slug-of-name filenames, disambiguated on collision within this batch ---
    existing_people_dir = DATA_DIR / "people" / "municipal"
    taken_slugs = {p.stem for p in existing_people_dir.glob("*.yaml")}
    person_filename_by_id = {}
    for person in persons:
        base_slug = slugify(person["name"])
        suffix = person["id"].rsplit("/", 1)[-1][:8]
        filename = unique_filename(taken_slugs, base_slug, suffix)
        person_filename_by_id[person["id"]] = filename
        rec.emit("people", person, filename)

    # --- memberships: regenerate id as a slug ({post-slug}-{surname}), matching repo convention ---
    existing_membership_dir = DATA_DIR / "memberships" / "municipal"
    taken_membership_slugs = {p.stem for p in existing_membership_dir.glob("*.yaml")}
    persons_by_id = {p["id"]: p for p in persons}

    for mem in memberships:
        person = persons_by_id[mem["person_id"]]
        surname = person["name"].split()[-1]
        post_slug = mem["post_id"].replace("/", "-")
        base_slug = f"{post_slug}-{slugify(surname)}"
        suffix = mem["id"].rsplit("/", 1)[-1][:8]
        new_id = unique_filename(taken_membership_slugs, base_slug, suffix)[:-len(".yaml")]

        doc = dict(mem)
        doc["id"] = new_id
        rec.emit("memberships", doc, f"{new_id}.yaml")

    print("==================== SUMMARY ====================")
    for k in sorted(rec.stats):
        print(f"{k}: {rec.stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


if __name__ == "__main__":
    main()
