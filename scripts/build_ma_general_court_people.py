#!/usr/bin/env python3
"""
Seed person + membership records for current Massachusetts General Court
members (House + Senate), from openstates/people's MA legislature bulk data
-- the same source build_ma_general_court.py used to build the district
jurisdiction/organization/post structure this attaches to.

Reuses each legislator's openstates person id directly as their ocd-person
id (openstates already mints a stable UUID per person; no reason to mint a
second one). Deduplicates by name against every person already in the repo
(federal, municipal, or a prior run of this script) before writing, same
as build_federal_records.py's index_people().

Does not set party -- this schema has no person-level party field; party
only lives on candidacies[], which Phase C (OCPF) will populate.

Idempotent by id AND by filename -- never overwrites.

Usage: python3 build_ma_general_court_people.py [--write]
Without --write, prints a dry-run summary only.
"""
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_federal_records as bfr  # reuse index_people/index_memberships/slugify-adjacent helpers
import build_ma_general_court as gc  # reuse slugify + CHAMBER_INFO

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "ma"
LEGISLATURE_CACHE = Path("/tmp/ma_openstates_legislature")

HEADER = (
    "# Machine-generated from openstates/people's MA legislature bulk data\n"
    "# by scripts/build_ma_general_court_people.py.\n"
)


def normalize_name(name):
    name = name.lower()
    name = re.sub(r"[.,'’]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def slugify(name):
    return gc.slugify(name)


def load_org_post(chamber, slug):
    suffix = gc.CHAMBER_INFO[chamber]["file_suffix"]
    org_path = DATA_DIR / "organizations" / "state" / f"{slug}-{suffix}.yaml"
    post_path = DATA_DIR / "posts" / "state" / f"{slug}-{suffix}.yaml"
    if not org_path.exists() or not post_path.exists():
        return None, None
    org = yaml.safe_load(org_path.read_text())
    post = yaml.safe_load(post_path.read_text())
    return org["id"], post["id"]


def build_person_and_membership(doc, people_by_name):
    roles = [r for r in doc.get("roles", []) if not r.get("end_date")]
    if not roles:
        return None
    role = roles[-1]
    chamber = role["type"]
    if chamber not in ("lower", "upper"):
        return None
    district = role["district"]
    slug = slugify(district)

    org_id, post_id = load_org_post(chamber, slug)
    if not org_id:
        return None, None, None, f"no org/post on file for {chamber} {district!r}"
    if not role.get("start_date"):
        return None, None, None, f"role has no start_date ({chamber} {district!r}) -- not guessing, skipped"

    name = doc["name"]
    existing = people_by_name.get(normalize_name(name))
    person_id = existing["id"] if existing else doc["id"]
    person_is_new = existing is None

    identifiers = []
    member_code = (doc.get("extras") or {}).get("member code")
    if member_code:
        identifiers.append({"scheme": "malegislature-member-code", "identifier": member_code})
    legacy_ids = [oid["identifier"] for oid in doc.get("other_identifiers", [])
                  if oid.get("scheme") == "legacy_openstates"]
    if legacy_ids:
        # Repo policy is one identifier per scheme per person (validate.py's
        # _check_external_identifiers); some legislators have been re-indexed
        # under multiple legacy openstates ids over time. Keep the most
        # recent (last in the list).
        identifiers.append({"scheme": "openstates-legacy-id", "identifier": legacy_ids[-1]})

    office = next((o for o in doc.get("offices", []) if o.get("classification") == "capitol"), None)
    contact = {}
    if office and office.get("voice"):
        contact["phone"] = office["voice"]
    links = doc.get("links", [])
    if links and links[0].get("url"):
        contact["profile_url"] = links[0]["url"]

    addresses = []
    if office and office.get("address"):
        addr = {"classification": "capitol", "name": "State House Office", "address": office["address"]}
        if office.get("voice"):
            addr["phone"] = office["voice"]
        if office.get("fax"):
            addr["fax"] = office["fax"]
        addresses.append(addr)

    sources = [{"url": s["url"]} for s in doc.get("sources", []) if s.get("url")]
    if not sources:
        sources = [{"url": "https://malegislature.gov/"}]

    person = {
        "id": person_id,
        "name": name,
        "identifiers": identifiers,
        "candidacies": [],
        **({"image": doc["image"]} if doc.get("image") else {}),
        **({"contact": contact} if contact else {}),
        **({"addresses": addresses} if addresses else {}),
        "verification": {
            "status": "machine-extracted",
            "pipeline": "openstates-people",
        },
        "sources": sources,
    }

    info = gc.CHAMBER_INFO[chamber]
    role_slug = "state-representative" if chamber == "lower" else "state-senator"
    family_name = doc.get("family_name") or name.split()[-1]
    membership_id = f"{info['post_prefix']}-{slug}-{role_slug}-{slugify(family_name)}"

    membership = {
        "id": membership_id,
        "person_id": person_id,
        "organization_id": org_id,
        "post_id": post_id,
        "role": info["title"],
        "seat": "At-Large",
        "start": str(role["start_date"]),
        "how_seated": "elected",
        "sources": sources,
    }

    return person, membership, person_is_new, None


def main():
    write = "--write" in sys.argv[1:]

    people_by_bioguide, people_by_name, people_by_path = bfr.index_people()
    membership_ids, membership_spans = bfr.index_memberships()

    stats = {}
    skipped_no_org = []

    for path in sorted(LEGISLATURE_CACHE.glob("*.yml")):
        doc = yaml.safe_load(path.read_text())
        result = build_person_and_membership(doc, people_by_name)
        if result is None:
            continue
        person, membership, person_is_new, err = result
        if err:
            skipped_no_org.append((doc.get("name"), err))
            continue

        if person_is_new:
            stats["person_new"] = stats.get("person_new", 0) + 1
            if write:
                out = DATA_DIR / "people" / "state" / f"{slugify(person['name'])}.yaml"
                out.parent.mkdir(parents=True, exist_ok=True)
                if out.exists():
                    stats["person_skipped_filename_conflict"] = stats.get("person_skipped_filename_conflict", 0) + 1
                else:
                    out.write_text(HEADER + yaml.safe_dump(person, sort_keys=False, allow_unicode=True,
                                                             default_flow_style=False, width=1000))
                    people_by_name[normalize_name(person["name"])] = person
        else:
            stats["person_existing"] = stats.get("person_existing", 0) + 1

        if membership["id"] in membership_ids:
            stats["membership_existing_by_id"] = stats.get("membership_existing_by_id", 0) + 1
            continue
        span_key = (membership["person_id"], membership["post_id"], membership["start"])
        if span_key in membership_spans:
            stats["membership_existing_by_span"] = stats.get("membership_existing_by_span", 0) + 1
            continue

        stats["membership_new"] = stats.get("membership_new", 0) + 1
        if write:
            out = DATA_DIR / "memberships" / "state" / f"{membership['id']}.yaml"
            out.parent.mkdir(parents=True, exist_ok=True)
            if out.exists():
                stats["membership_skipped_filename_conflict"] = stats.get("membership_skipped_filename_conflict", 0) + 1
            else:
                out.write_text(HEADER + yaml.safe_dump(membership, sort_keys=False, allow_unicode=True,
                                                         default_flow_style=False, width=1000))
                membership_ids[membership["id"]] = out
                membership_spans[span_key] = out

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    print(f"\nSkipped, no org/post on file: {len(skipped_no_org)}")
    for name, err in skipped_no_org:
        print(f"  {name}: {err}")


if __name__ == "__main__":
    main()
