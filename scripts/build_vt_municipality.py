#!/usr/bin/env python3
"""Generalized Vermont municipal builder -- issue #163 (VT master
tracking), municipal fan-out.

Builds one municipality (town, city, or village) per JSON spec in
scripts/vt_muni_data/<place-slug>.json, in the Bloomfield shape (the
worked example, scripts/build_vt_bloomfield_sweep.py):

- one org + one post per office (org filename = post filename for
  single-post bodies), post id "{place-slug}-vt/{office-slug}";
- one person per distinct holder, keyed vt|<person-scope>|<slug>
  (person-scope defaults to the municipality's place slug; a holder
  shared across municipalities -- e.g. a town selectboard member who
  is also a village trustee -- names the owning scope explicitly so
  a single person record carries both memberships);
- one membership per holder per office, how_seated "elected" unless
  the spec says "appointed";
- offices with an empty holders list are created as STRUCTURE ONLY
  (the spec's source note must state the statutory basis and that no
  official source publishes the current holder);
- towns with a "jp_election" block get a Justice of the Peace
  election record for the 2024-11-05 general election (winners only,
  per the SOS JP listing; no votes or party labels are published in
  that listing and none are recorded).

Person-file naming: people/municipal/<name-slug>.yaml; if that file
already exists for a DIFFERENT person id (same name, another town),
the file is <name-slug>-<first 8 hex of the person uuid>.yaml. An
existing file with the SAME id is left untouched (idempotent).

No term starts or ends are recorded. Dry run by default; --write to
create files.

Usage: build_vt_municipality.py <spec.json> [<spec.json> ...] [--write]
"""
import json
import sys
import uuid
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "vt"
RETRIEVED = "2026-10-19"

NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")


def oid(kind, key):
    return f"ocd-{kind}/{uuid.uuid5(NS, kind + '|' + key)}"


def person_id(scope, name_slug):
    return oid("person", f"vt|{scope}|{name_slug}")


def dump(path, doc, write, header):
    if path.exists():
        print(f"SKIP exists: {path.relative_to(REPO)}")
        return False
    print(f"{'WRITE' if write else 'WOULD WRITE'}: {path.relative_to(REPO)}")
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not header.endswith("\n"):
            header += "\n"
        path.write_text(
            header + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True)
        )
    return True


def build(spec, write):
    place = spec["place_slug"]
    prefix = f"{place}-vt"
    jurisdiction_id = spec["jurisdiction_id"]
    header = spec["header"]
    created = 0
    people = {}  # (scope, slug) -> {"name":..., "sources":[...], "jp":bool}

    def note_person(scope, slug, name, sources, is_jp, existing_id=None,
                    ballot_name=None):
        entry = people.setdefault(
            (scope, slug), {"name": name, "sources": [], "jp": False})
        for s in sources:
            if s not in entry["sources"]:
                entry["sources"].append(s)
        if is_jp:
            entry["jp"] = True
        if existing_id:
            entry["existing_id"] = existing_id
        if ballot_name:
            # The SOS JP listing's printed form of the name, when it
            # differs from the person's display name (e.g. the
            # listing's "Sheila Martin" for Shelia Martin, or a
            # suffixed "Tom Haley III" for Tom Haley).
            entry["ballot_name"] = ballot_name

    for office in spec["offices"]:
        oslug = office["slug"]
        post_id = f"{prefix}/{oslug}"
        # An office may share its organization with sibling posts
        # (city council ward posts, a village board's president +
        # trustee posts) by naming an "org_key"; the org file is
        # written once, by the first post that defines it, and its
        # filename names the body. Default: one org per post.
        org_key = office.get("org_key", post_id)
        org_id = oid("organization", f"vt|municipal|{org_key}")
        sources = []
        for s in office["sources"]:
            s = dict(s)
            s.setdefault("retrieved", RETRIEVED)
            sources.append(s)
        org_sources = []
        for s in office.get("org_sources", office["sources"]):
            s = dict(s)
            s.setdefault("retrieved", RETRIEVED)
            org_sources.append(s)
        org = {
            "id": org_id,
            "name": office["org_name"],
            "jurisdiction_id": jurisdiction_id,
            "identifiers": [
                {"scheme": "civicmirror-office", "identifier": org_key}
            ],
            "status": "active",
            "sources": org_sources,
        }
        created += dump(
            DATA_DIR / "organizations" / "municipal"
            / (org_key.replace("/", "-") + ".yaml"),
            org, write, header)
        post = {
            "id": post_id,
            "organization_id": org_id,
            "title": office["title"],
            "seats": office["seats"],
            "sources": sources,
        }
        created += dump(
            DATA_DIR / "posts" / "municipal" / f"{prefix}-{oslug}.yaml",
            post, write, header)

        for holder in office.get("holders", []):
            scope = holder.get("person_scope", place)
            hsources = []
            for s in holder.get("sources", office["sources"]):
                s = dict(s)
                s.setdefault("retrieved", RETRIEVED)
                hsources.append(s)
            membership = {
                "id": f"{prefix}-{oslug}-{holder['slug']}",
                "person_id": holder.get(
                    "existing_person_id",
                    person_id(scope, holder["slug"])),
                "organization_id": org_id,
                "post_id": post_id,
                "role": office["title"],
                "how_seated": holder.get("how_seated", "elected"),
                "sources": hsources,
            }
            created += dump(
                DATA_DIR / "memberships" / "municipal"
                / f"{prefix}-{oslug}-{holder['slug']}.yaml",
                membership, write, header)
            note_person(scope, holder["slug"], holder["name"], hsources,
                        oslug == "justice-of-the-peace"
                        and not holder.get("no_candidacy"),
                        holder.get("existing_person_id"),
                        holder.get("ballot_name"))

    jp_election = spec.get("jp_election")
    for (scope, slug), entry in sorted(people.items()):
        if entry.get("existing_id"):
            # Cross-tier reuse: the person record already exists in
            # another tier. No person file is written here; the JP
            # candidacy must be appended to the existing record by
            # the operator (the build report lists these).
            print(f"REUSE existing person {entry['existing_id']} "
                  f"for {entry['name']} -- append the candidacy to "
                  f"the existing person file manually")
            continue
        candidacies = []
        if entry["jp"] and jp_election:
            candidacies = [{
                "contest_id": jp_election["contest_id"],
                "election_id": jp_election["election_id"],
                "jurisdiction_id": jurisdiction_id,
                "office_id": f"{prefix}/justice-of-the-peace",
                # required by schema; party is not published in the
                # SOS JP listing and is recorded as null
                "party": None,
                "ballot_name": entry.get("ballot_name", entry["name"]),
                "status": "active",
            }]
        person = {
            "id": person_id(scope, slug),
            "name": entry["name"],
            "identifiers": [],
            "candidacies": candidacies,
            "verification": {
                "status": "machine-extracted",
                "reviewed_on": RETRIEVED,
                "pipeline": "build_vt_municipality",
            },
            "sources": entry["sources"],
        }
        pdir = DATA_DIR / "people" / "municipal"
        path = pdir / f"{slug}.yaml"
        if path.exists():
            # header comments precede the YAML body; strip them first
            body = "\n".join(
                ln for ln in path.read_text().splitlines()
                if not ln.startswith("#"))
            existing = yaml.safe_load(body)
            if existing and existing.get("id") == person["id"]:
                print(f"SKIP exists: {path.relative_to(REPO)}")
                continue
            suffix = person["id"].rsplit("-", 1)[-1][:8]
            path = pdir / f"{slug}-{suffix}.yaml"
        created += dump(path, person, write, header)

    if jp_election:
        jp_people = [
            (slug, entry.get("ballot_name", entry["name"]),
             entry.get("existing_id",
                       person_id(spec.get("jp_person_scope", place), slug)))
            for (scope, slug), entry in sorted(people.items()) if entry["jp"]
        ]
        esources = []
        for s in jp_election["sources"]:
            s = dict(s)
            s.setdefault("retrieved", RETRIEVED)
            esources.append(s)
        election = {
            "id": jp_election["election_id"],
            "name": jp_election["name"],
            "date": "2024-11-05",
            "election_type": "general",
            "status": "official",
            "contests": [{
                "id": jp_election["contest_id"],
                "jurisdiction_id": jurisdiction_id,
                "office_id": f"{prefix}/justice-of-the-peace",
                "vote_for": jp_election["vote_for"],
                "candidate_ids": [pid for _, _, pid in jp_people],
                "result_status": "official",
                "winners": [
                    {"person_id": pid, "name": name}
                    for _, name, pid in jp_people
                ],
            }],
            "sources": esources,
        }
        created += dump(
            DATA_DIR / "elections" / jp_election["filename"],
            election, write, jp_election["header"])

    print(f"{spec['label']}: {'created' if write else 'would create'} "
          f"{created} files.")
    return created


def main():
    args = [a for a in sys.argv[1:] if a != "--write"]
    write = "--write" in sys.argv
    total = 0
    for arg in args:
        spec = json.loads(Path(arg).read_text())
        total += build(spec, write)
    print(f"TOTAL: {total} files.")


if __name__ == "__main__":
    main()
