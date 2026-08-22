#!/usr/bin/env python3
"""
Import the v27 MA municipal charter/elected-office rolling audit
(`reference/MA Rolling Audit/`) into data/us/ma/{organizations,posts,
people,memberships}/municipal/.

v27 is cumulative (supersedes v20/v25/v26): its schema-ready files contain
every previously-audited municipality plus the new batch (New Marlborough,
New Salem, Newbury, Newburyport, Newton). Records already imported from v20
are skipped by this script's idempotency check (same id, same filename), so
only the net-new v21-v27 records get written.

See scripts/import_ma_charter_audit_v20.py for the rationale behind the
placement rules (filenames, membership id regeneration, and why persons are
never merged into existing repo people by name match) -- this script repeats
that logic unchanged, pointed at the v27 source files.

Idempotent by id AND by filename -- never overwrites.

Usage: python3 import_ma_charter_audit_v27.py [--write]
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "ma"
SRC_DIR = REPO / "reference" / "MA Rolling Audit"

HEADER = (
    "# Imported from reference/MA Rolling Audit/ (MA municipal charter/\n"
    "# elected-office rolling audit, generated 2026-08-21) by scripts/\n"
    "# import_ma_charter_audit_v27.py. Source rows were machine-extracted from\n"
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

    orgs = load("ma_schema_ready_organizations_rolling_2026-08-21_v27.json")
    posts = load("ma_schema_ready_posts_rolling_2026-08-21_v27.json")
    persons = load("ma_schema_ready_persons_rolling_2026-08-21_v27.json")
    memberships = load("ma_schema_ready_memberships_rolling_2026-08-21_v27.json")

    rec = Recorder(write)

    # id -> existing file, scanned across ALL of organizations/ and posts/ (not just
    # municipal/, and not just the exact target path) -- catches an id already used by
    # a record from a different pipeline (e.g. an earlier CivicPatch import), which a
    # path-only exists() check would miss because that record lives under a different
    # filename.
    def id_index(kind):
        idx = {}
        for f in (DATA_DIR / kind).glob("*/*.yaml"):
            doc = yaml.safe_load(f.read_text()) or {}
            if "id" in doc:
                idx[doc["id"]] = f
        return idx

    existing_post_ids = id_index("posts")
    skipped_post_ids = set()

    # --- organizations & posts: filename derived from the civicmirror-office / post id ---
    # (org office_id and post id are the same string 1:1 in this source, verified
    # against the v27 files before writing this check.)
    for org in orgs:
        office_id = next(
            (i["identifier"] for i in org["identifiers"] if i["scheme"] == "civicmirror-office"),
            org["id"],
        )
        target_path = DATA_DIR / "posts" / "municipal" / f"{office_id.replace('/', '-')}.yaml"
        existing_file = existing_post_ids.get(office_id)
        if existing_file is not None and existing_file != target_path:
            # Same post id already claimed by a different file (a pre-existing,
            # differently-sourced record for this office) -- skip this org/post pair
            # and every downstream person/membership tied to it, rather than writing a
            # duplicate office alongside the one that's already there.
            rec.stats["post_skipped_id_conflict"] = rec.stats.get("post_skipped_id_conflict", 0) + 1
            rec.stats["organization_skipped_id_conflict"] = rec.stats.get("organization_skipped_id_conflict", 0) + 1
            skipped_post_ids.add(office_id)
            continue
        rec.emit("organizations", org, f"{office_id.replace('/', '-')}.yaml")

    for post in posts:
        if post["id"] in skipped_post_ids:
            continue
        rec.emit("posts", post, f"{post['id'].replace('/', '-')}.yaml")

    # --- persons: slug-of-name filenames, disambiguated on collision within this batch ---
    # v27 is cumulative -- every v20 person id reappears here. Dedup by id (scanned
    # across all of people/, not just the naively-computed filename) so a person
    # already imported under a different collision-suffixed filename isn't re-written
    # under a second file with the same id.
    existing_person_ids = set()
    for f in (DATA_DIR / "people").glob("*/*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            existing_person_ids.add(doc["id"])

    # A person whose only membership(s) in this batch point at a skipped (id-conflicted)
    # post has no surviving reason to exist in this batch -- importing them anyway would
    # create an orphaned duplicate-human record (this is what happened with Millbury's
    # select-board-member conflict before this check existed).
    persons_with_surviving_membership = {
        mem["person_id"] for mem in memberships if mem["post_id"] not in skipped_post_ids
    }

    existing_people_dir = DATA_DIR / "people" / "municipal"
    taken_slugs = {p.stem for p in existing_people_dir.glob("*.yaml")}
    person_filename_by_id = {}
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
        filename = unique_filename(taken_slugs, base_slug, suffix)
        person_filename_by_id[person["id"]] = filename
        rec.emit("people", person, filename)

    # --- memberships: regenerate id as a slug ({post-slug}-{surname}), matching repo convention ---
    # Dedup by (person_id, post_id): the source membership id isn't preserved in the
    # written record (its id is regenerated as a slug), so identity across a re-run
    # is the person/post pair, not the source id.
    existing_membership_pairs = set()
    for f in (DATA_DIR / "memberships").glob("*/*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "person_id" in doc and "post_id" in doc:
            existing_membership_pairs.add((doc["person_id"], doc["post_id"]))

    existing_membership_dir = DATA_DIR / "memberships" / "municipal"
    taken_membership_slugs = {p.stem for p in existing_membership_dir.glob("*.yaml")}
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

    print("==================== SUMMARY ====================")
    for k in sorted(rec.stats):
        print(f"{k}: {rec.stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


if __name__ == "__main__":
    main()
