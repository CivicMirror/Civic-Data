#!/usr/bin/env python3
"""
Collision-safe helper for minting Person + Membership records against an
EXISTING post, for the MA #34 town-by-town research follow-up. Does not
touch organizations/posts -- only used when the post already exists.

Two lessons baked in after a real duplication incident (wenham et al.,
2026-09-06): several towns' post `id` suffix doesn't match its `title`
text (e.g. id "wenham-ma/select-board" but title "Select Board Member") --
deriving the membership id from the title created a second, differently-
named membership+person for someone who already existed under the post's
own naming convention. Fixed by (1) deriving the membership id from the
POST's own id suffix, not the title, and (2) pre-checking every existing
membership on the target post by normalized name before minting -- a
normalized-name match is skipped outright, never re-created under a new
id, regardless of filename/id collisions.

Usage: import and call mint_town(slug, post_filename, role_title, members,
source_url, source_note, retrieved, existing_people_index).
members: list of (name, end_year_or_None) tuples.
"""
import re
import unicodedata
import uuid
from pathlib import Path

import yaml

BASE = Path("/data/Projects/Civic/Civic-Data/data/us/ma")
PERSON_NS = uuid.UUID("2f6f6a2f-2f9b-5c1a-9d6a-3e6f9c2a4b1d")


def slugify(v):
    v = unicodedata.normalize("NFKD", v).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", v.casefold()).strip("-")


def normalize_name(name):
    name = re.sub(r"[.,]", "", name).strip().casefold()
    name = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", name).strip()
    return re.sub(r"\s+", " ", name)


def load_existing_people_index():
    index = {}
    for p in (BASE / "people" / "municipal").glob("*.yaml"):
        doc = yaml.safe_load(p.read_text()) or {}
        index[p.stem] = doc.get("id")
    return index


def load_people_names_by_id():
    index = {}
    for p in (BASE / "people" / "municipal").glob("*.yaml"):
        doc = yaml.safe_load(p.read_text()) or {}
        if doc.get("id"):
            index[doc["id"]] = doc.get("name", "")
    return index


def existing_normalized_names_for_post(post_id, people_names_by_id):
    names = set()
    for m in (BASE / "memberships" / "municipal").glob("*.yaml"):
        doc = yaml.safe_load(m.read_text()) or {}
        if doc.get("post_id") == post_id:
            pname = people_names_by_id.get(doc.get("person_id"), "")
            if pname:
                names.add(normalize_name(pname))
    return names


def write_yaml(path, doc):
    if path.exists():
        existing = yaml.safe_load(path.read_text()) or {}
        if existing.get("id") == doc["id"]:
            return "existing"
        raise SystemExit(f"conflicting existing record: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        "# Hand-verified against the town's official website for issue #34's\n"
        "# MA municipal officeholder backfill (never covered by issue #16's\n"
        "# original research pass). Machine-extracted via a Claude web-fetch\n"
        "# pass, pending human sign-off.\n"
    )
    path.write_text(header + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000))
    return "new"


def mint_town(slug, post_filename, role_title, members, source_url, source_note, retrieved,
              existing_people_index, people_names_by_id, vacant_ok=True):
    post_path = BASE / "posts" / "municipal" / post_filename
    post = yaml.safe_load(post_path.read_text())
    post_id = post["id"]
    organization_id = post["organization_id"]
    seats = post["seats"]
    # Derive the membership-id suffix from the post's OWN id, not the title
    # text -- these can differ (e.g. id ".../select-board", title "Select
    # Board Member") and using the title created duplicate records for
    # people who already existed under the post's real naming convention.
    id_suffix = post_id.split("/", 1)[1]

    already = existing_normalized_names_for_post(post_id, people_names_by_id)

    real_members = [(n, e) for n, e in members if n and normalize_name(n) not in ("vacant", "")]
    if len(real_members) + len([n for n, _ in members if not n or normalize_name(n) == "vacant"]) > seats:
        raise SystemExit(f"{slug}: {len(members)} members > {seats} seats -- structure mismatch, do not mint")

    results = []
    for name, end in members:
        norm = normalize_name(name) if name else "vacant"
        if norm in already:
            results.append((name, None, "skipped-already-present", None, None))
            continue
        if norm == "vacant":
            results.append((name, None, "skipped-vacant-no-person-record", None, None))
            continue

        person_id = f"ocd-person/{uuid.uuid5(PERSON_NS, f'ma-town-research|{slug}|{post_id}|{name}')}"
        base_slug = slugify(name)
        candidate = base_slug
        if existing_people_index.get(candidate) not in (None, person_id):
            candidate = f"{base_slug}-{slug}"
        if existing_people_index.get(candidate) not in (None, person_id):
            candidate = f"{base_slug}-{slug}-{str(uuid.uuid5(PERSON_NS, person_id))[:8]}"
        existing_people_index[candidate] = person_id

        person = {
            "id": person_id,
            "name": name,
            "candidacies": [],
            "verification": {
                "status": "machine-extracted",
                "reviewed_on": retrieved,
                "pipeline": "ma-town-website-verification-2026-09-06",
            },
            "sources": [{"url": source_url, "note": source_note, "retrieved": retrieved}],
        }
        person_status = write_yaml(BASE / "people" / "municipal" / f"{candidate}.yaml", person)

        mem_id = f"{slug}-ma-{id_suffix.replace('/', '-')}-{slugify(name)}"
        membership = {
            "id": mem_id,
            "person_id": person_id,
            "organization_id": organization_id,
            "post_id": post_id,
            "role": role_title,
            "how_seated": "elected",
            "sources": [{"url": source_url, "note": source_note, "retrieved": retrieved}],
        }
        if end:
            membership["end"] = str(end)
        mem_status = write_yaml(BASE / "memberships" / "municipal" / f"{mem_id}.yaml", membership)
        already.add(norm)
        results.append((name, candidate, person_status, mem_id, mem_status))
    return results
