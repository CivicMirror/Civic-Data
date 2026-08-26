#!/usr/bin/env python3
"""
Import the v31-v49 MA municipal charter/elected-office rolling audit
preservation packages into data/us/ma/{organizations,posts,people,
memberships}/municipal/. (The filename says v32 because v31 was added after
the first run; records already written carry the original script name in
their header comment, so the name is kept stable rather than churned.)

Each listed version is an independent delta package (not cumulative), like
v56-v58.

Every organization's jurisdiction_id is checked against the jurisdiction
records actually on disk before anything is written -- the v57 package
shipped `place:mount-washington` for a town whose canonical slug is
`mt-washington`, which silently created 21 records pointing at a
non-existent jurisdiction. An unknown slug is now a hard error.

See scripts/import_ma_charter_audit_v20.py, _v27.py, and _v56_v58.py for the
placement rationale (filenames, membership id regeneration, why persons are
never merged into existing repo people by name match) -- this script repeats
that logic unchanged, pointed at the v32-v49 delta packages.

Idempotent by id AND by filename -- never overwrites.

Usage: python3 import_ma_charter_audit_v32_v49.py [--write]
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "ma"
SRC_ROOT = REPO / "reference" / "MA Rolling Audit"

BATCHES = [
    ("v31", SRC_ROOT / "ma_charter_audit_v31_preservation_package_2026-08-25"),
    ("v32", SRC_ROOT / "ma_charter_audit_next10_v32_v33_2026-08-25" / "ma_charter_audit_v32_preservation_package_2026-08-25"),
    ("v33", SRC_ROOT / "ma_charter_audit_next10_v32_v33_2026-08-25" / "ma_charter_audit_v33_preservation_package_2026-08-25"),
    ("v34", SRC_ROOT / "ma_charter_audit_next10_v34_v35_2026-08-25" / "ma_charter_audit_v34_preservation_package_2026-08-25"),
    ("v35", SRC_ROOT / "ma_charter_audit_next10_v34_v35_2026-08-25" / "ma_charter_audit_v35_preservation_package_2026-08-25"),
    ("v36", SRC_ROOT / "ma_charter_audit_next10_v36_v37_2026-08-25" / "ma_charter_audit_v36_preservation_package_2026-08-25"),
    ("v37", SRC_ROOT / "ma_charter_audit_next10_v36_v37_2026-08-25" / "ma_charter_audit_v37_preservation_package_2026-08-25"),
    ("v38", SRC_ROOT / "ma_charter_audit_next10_v38_v39_2026-08-25(1)" / "ma_charter_audit_v38_preservation_package_2026-08-25"),
    ("v39", SRC_ROOT / "ma_charter_audit_next10_v38_v39_2026-08-25(1)" / "ma_charter_audit_v39_preservation_package_2026-08-25"),
    ("v40", SRC_ROOT / "ma_charter_audit_next10_v40_v41_2026-08-25(1)" / "ma_charter_audit_v40_preservation_package_2026-08-25"),
    ("v41", SRC_ROOT / "ma_charter_audit_next10_v40_v41_2026-08-25(1)" / "ma_charter_audit_v41_preservation_package_2026-08-25"),
    ("v42", SRC_ROOT / "ma_charter_audit_next10_v42_v43_2026-08-25(1)" / "v42"),
    ("v43", SRC_ROOT / "ma_charter_audit_next10_v42_v43_2026-08-25(1)" / "v43"),
    ("v44", SRC_ROOT / "ma_charter_audit_next20_v44_v47_2026-08-25(1)" / "v44"),
    ("v45", SRC_ROOT / "ma_charter_audit_next20_v44_v47_2026-08-25(1)" / "v45"),
    ("v46", SRC_ROOT / "ma_charter_audit_next20_v44_v47_2026-08-25(1)" / "v46"),
    ("v47", SRC_ROOT / "ma_charter_audit_next20_v44_v47_2026-08-25(1)" / "v47"),
    ("v48", SRC_ROOT / "ma_charter_audit_next10_v48_v49_2026-08-25(1)" / "v48"),
    ("v49", SRC_ROOT / "ma_charter_audit_next10_v48_v49_2026-08-25(1)" / "v49"),
]

HEADER_TMPL = (
    "# Imported from reference/MA Rolling Audit/ ({version} MA municipal\n"
    "# charter/elected-office rolling audit preservation package, generated\n"
    "# 2026-08-25) by scripts/import_ma_charter_audit_v32_v49.py. Source rows\n"
    "# were machine-extracted from municipal government sites; see the\n"
    "# record's sources for provenance.\n"
)


def slugify(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def load(src_dir, version, kind):
    name = f"ma_schema_ready_{kind}_delta_2026-08-25_{version}.json"
    return json.loads((src_dir / name).read_text())


class Recorder:
    def __init__(self, write):
        self.write = write
        self.stats = {}

    def emit(self, kind, doc, filename, header):
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
            text = header + yaml.safe_dump(
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

    # Keep each record's provenance to its own version for the header comment,
    # while still processing all batches together so cross-batch idempotency
    # (existing_post_ids etc.) works the same way the v56-v58 script does.
    orgs, posts, persons, memberships = [], [], [], []
    version_by_org_id, version_by_post_id = {}, {}
    version_by_person_id, version_by_membership_id = {}, {}

    for version, src_dir in BATCHES:
        v_orgs = load(src_dir, version, "organizations")
        v_posts = load(src_dir, version, "posts")
        v_persons = load(src_dir, version, "persons")
        v_memberships = load(src_dir, version, "memberships")

        for o in v_orgs:
            version_by_org_id[o["id"]] = version
        for p in v_posts:
            version_by_post_id[p["id"]] = version
        for p in v_persons:
            version_by_person_id[p["id"]] = version
        for m in v_memberships:
            version_by_membership_id[m["id"]] = version

        orgs += v_orgs
        posts += v_posts
        persons += v_persons
        memberships += v_memberships

    rec = Recorder(write)

    # Fail before writing anything if a batch references a jurisdiction that
    # doesn't exist in the repo (see module docstring: the v57 Mount Washington
    # slug mismatch). Checked up front so a bad batch aborts cleanly rather
    # than leaving a half-written import behind.
    known_places = set()
    for f in (DATA_DIR / "jurisdictions" / "municipal").glob("*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        m = re.search(r"place:([^/]+)", doc.get("id", "") or "")
        if m:
            known_places.add(m.group(1))

    unknown = {}
    for org in orgs:
        m = re.search(r"place:([^/]+)", org.get("jurisdiction_id", "") or "")
        place = m.group(1) if m else None
        if place not in known_places:
            unknown.setdefault((version_by_org_id[org["id"]], place), 0)
            unknown[(version_by_org_id[org["id"]], place)] += 1
    if unknown:
        print("ERROR: organizations reference unknown jurisdictions:")
        for (v, place), n in sorted(unknown.items()):
            print(f"  [{v}] place:{place} -- {n} organization(s)")
        print("\nNo records written. Fix the source package's jurisdiction_id "
              "(or add the jurisdiction) and re-run.")
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
        header = HEADER_TMPL.format(version=version_by_org_id[org["id"]])
        rec.emit("organizations", org, f"{office_id.replace('/', '-')}.yaml", header)

    for post in posts:
        if post["id"] in skipped_post_ids:
            continue
        header = HEADER_TMPL.format(version=version_by_post_id[post["id"]])
        rec.emit("posts", post, f"{post['id'].replace('/', '-')}.yaml", header)

    existing_person_ids = set()
    for f in (DATA_DIR / "people").glob("*/*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            existing_person_ids.add(doc["id"])

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
        header = HEADER_TMPL.format(version=version_by_person_id[person["id"]])
        rec.emit("people", person, filename, header)

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
        header = HEADER_TMPL.format(version=version_by_membership_id[mem["id"]])
        rec.emit("memberships", doc, f"{new_id}.yaml", header)

    print("==================== SUMMARY ====================")
    for k in sorted(rec.stats):
        print(f"{k}: {rec.stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


if __name__ == "__main__":
    main()
