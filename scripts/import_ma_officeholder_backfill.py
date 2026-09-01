#!/usr/bin/env python3
"""Import a reviewed Massachusetts municipal-officeholder manifest."""

import argparse
import re
import unicodedata
import uuid
from pathlib import Path

import yaml


NAMESPACE = uuid.UUID("631fbcda-af55-4d76-82f4-124d7f40fa6e")


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def load_index(directory: Path) -> dict[str, dict]:
    index = {}
    for path in directory.glob("*.yaml"):
        document = yaml.safe_load(path.read_text()) or {}
        if "id" in document:
            index[document["id"]] = document
    return index


def write_yaml(path: Path, document: dict, header: str) -> None:
    if path.exists():
        existing = yaml.safe_load(path.read_text()) or {}
        if existing == document:
            return
        raise SystemExit(f"conflicting existing record: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        header
        + yaml.safe_dump(
            document,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
            width=1000,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    manifest = yaml.safe_load(args.manifest.read_text())
    retrieved = str(manifest["retrieved"])
    pipeline = manifest["pipeline"]
    posts = load_index(args.data_dir / "posts" / "municipal")
    organizations = load_index(args.data_dir / "organizations" / "municipal")
    people_dir = args.data_dir / "people" / "municipal"
    memberships_dir = args.data_dir / "memberships" / "municipal"

    written_people = 0
    written_memberships = 0
    for row in manifest["officeholders"]:
        post = posts.get(row["post_id"])
        if post is None:
            raise SystemExit(f"unknown post_id: {row['post_id']}")
        organization_id = post["organization_id"]
        if organization_id not in organizations:
            raise SystemExit(f"post references unknown organization: {row['post_id']}")

        person_uuid = uuid.uuid5(NAMESPACE, f"{row['municipality']}|{row['name']}")
        person_id = f"ocd-person/{person_uuid}"
        base_person_path = people_dir / f"{slugify(row['name'])}.yaml"
        person_path = base_person_path
        if base_person_path.exists():
            base_document = yaml.safe_load(base_person_path.read_text()) or {}
            if base_document.get("id") != person_id:
                person_path = people_dir / f"{slugify(row['name'])}-{str(person_uuid)[:8]}.yaml"
        membership_id = f"{row['post_id'].replace('/', '-')}-{slugify(row['name'])}"
        membership_path = memberships_dir / f"{membership_id}.yaml"
        sources = [{"url": url, "retrieved": retrieved} for url in row["sources"]]
        identifiers = []
        if row.get("civicpatch_id"):
            identifiers.append({"scheme": "civicpatch", "identifier": row["civicpatch_id"]})

        person = {
            "id": person_id,
            "name": row["name"],
            "identifiers": identifiers,
            "candidacies": [],
            "verification": {
                "status": "machine-extracted",
                "reviewed_on": retrieved,
                "pipeline": pipeline,
            },
            "sources": sources,
        }
        membership = {
            "id": membership_id,
            "person_id": person_id,
            "organization_id": organization_id,
            "post_id": row["post_id"],
            "role": post["title"],
            "how_seated": "elected",
            "sources": sources,
        }
        header = (
            f"# Machine-extracted from official municipal roster page(s), retrieved {retrieved}.\n"
            "# Imported by scripts/import_ma_officeholder_backfill.py; see sources below.\n"
        )
        if args.write:
            write_yaml(person_path, person, header)
            write_yaml(membership_path, membership, header)
        written_people += 1
        written_memberships += 1

    print(f"people={written_people} memberships={written_memberships} write={args.write}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
