#!/usr/bin/env python3
"""Deterministically convert the legacy Civic-Data YAML layout to v2."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def convert_official(document: dict) -> dict:
    """Return a Person document without inventing or dropping public fields."""
    forbidden = {"filing_address", "filing_phone", "filing_email"}
    present = forbidden.intersection(document)
    if present:
        raise ValueError(f"private filing fields are not allowed: {', '.join(sorted(present))}")
    result = dict(document)
    result.pop("official_id", None)
    result.setdefault("identifiers", [])
    result["candidacies"] = list(result.get("candidacies", []))
    return result


def convert_election_linkage(document: dict) -> dict:
    """Wrap one legacy linkage in an Election with one Contest."""
    linkage_id = document["id"]
    parts = linkage_id.split("/")
    if len(parts) != 3:
        raise ValueError(f"legacy election linkage ID must have three components: {linkage_id}")
    jurisdiction_slug, election_date, office_slug = parts
    election_type = document.get("election_type", "general")
    election_id = f"{jurisdiction_slug}/{election_date}/{election_type}"
    contest_id = linkage_id
    contest = {
        "id": contest_id,
        "jurisdiction_id": document["jurisdiction_id"],
        "office_id": document["office_id"],
        "vote_for": 1,
        "candidate_ids": [winner["official_id"] for winner in document["winners"] if winner.get("official_id")],
        "result_status": "certified" if document["certification"]["status"] == "certified" else "unofficial",
        "winners": [
            {
                **{"person_id": winner["official_id"]},
                "name": winner["name"],
                **({"votes": winner["votes"]} if "votes" in winner else {}),
                **({"party": winner["party"]} if "party" in winner else {}),
            }
            for winner in document["winners"]
            if winner.get("official_id")
        ],
    }
    if "seat" in document:
        contest["seat"] = document["seat"]
    return {
        "id": election_id,
        "name": f"{jurisdiction_slug} {election_date} {election_type} election",
        "date": election_date,
        "election_type": election_type,
        "status": "certified" if document["certification"]["status"] == "certified" else "unofficial",
        "contests": [contest],
        "sources": document["sources"],
    }


def _yaml_files(root: Path, directory: str) -> list[Path]:
    base = root / "data" / "us"
    if not base.exists():
        base = root
    return sorted(base.rglob(f"{directory}/**/*.yaml"))


def _replace_component(relative: Path, old: str, new: str) -> Path:
    parts = list(relative.parts)
    try:
        index = parts.index(old)
    except ValueError as exc:
        raise ValueError(f"{old!r} is not present in {relative}") from exc
    parts[index] = new
    return Path(*parts)


def migrate_tree(source_root: Path, destination_root: Path) -> list[Path]:
    """Convert a source checkout into a new checkout-shaped destination."""
    source_root = Path(source_root)
    destination_root = Path(destination_root)
    people_files = _yaml_files(source_root, "officials")
    election_files = _yaml_files(source_root, "elections")
    if destination_root.exists():
        raise FileExistsError(f"destination already exists: {destination_root}")
    outputs: list[tuple[Path, dict]] = []
    for path in people_files:
        relative = path.relative_to(source_root)
        destination = destination_root / _replace_component(relative, "officials", "people")
        outputs.append((destination, convert_official(yaml.safe_load(path.read_text()))))
    for path in election_files:
        relative = path.relative_to(source_root)
        destination = destination_root / relative
        outputs.append((destination, convert_election_linkage(yaml.safe_load(path.read_text()))))
    for destination, _ in outputs:
        destination.parent.mkdir(parents=True, exist_ok=True)
    for destination, document in outputs:
        destination.write_text(yaml.safe_dump(document, sort_keys=False))
    return [destination for destination, _ in outputs]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    for path in migrate_tree(args.source, args.destination):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
