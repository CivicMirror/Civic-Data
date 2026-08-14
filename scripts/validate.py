#!/usr/bin/env python3
"""Validate Civic-Data schemas, references, identity links, and elections."""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError:
    print("Missing dependencies. Run: pip install -r scripts/requirements.txt")
    sys.exit(2)

REPO = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO / "schemas"
DATA_DIR = REPO / "data"

ERRORS: list[str] = []
WARNINGS: list[str] = []


def error(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def load_schemas(schema_dir: Path = SCHEMA_DIR) -> dict[str, Draft202012Validator]:
    raw = {path.name: json.loads(path.read_text()) for path in schema_dir.glob("*.schema.json")}
    registry = Registry()
    for name, schema in raw.items():
        registry = registry.with_resource(name, Resource.from_contents(schema))
        if "$id" in schema:
            registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return {name: Draft202012Validator(schema, registry=registry) for name, schema in raw.items()}


def load_yaml(path: Path) -> dict | None:
    try:
        document = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        error(f"{path}: YAML parse error: {exc}")
        return None
    if not isinstance(document, dict):
        error(f"{path}: top-level document must be a mapping")
        return None
    return document


def validate_schema(validator: Draft202012Validator, document: dict, path: Path) -> bool:
    valid = True
    for failure in sorted(validator.iter_errors(document), key=lambda item: list(item.path)):
        location = "/".join(str(part) for part in failure.path) or "(root)"
        error(f"{path}: [{location}] {failure.message}")
        valid = False
    return valid


def norm_name(name: str) -> str:
    text = unicodedata.normalize("NFKD", name)
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = "".join(char if char.isalnum() or char.isspace() else " " for char in text.casefold())
    return " ".join(text.split())


def _register(store: dict, key: str, value, path: Path, file_of: dict) -> None:
    if key in store:
        error(f"{path}: duplicate ID '{key}' (already defined in {file_of[key]})")
        return
    store[key] = value
    file_of[key] = path


def _kind(path: Path) -> str:
    return next((parent.name for parent in path.parents if parent.name in {"jurisdictions", "people", "elections"}), path.parent.name)


def validate(data_dir: Path = DATA_DIR, schema_dir: Path = SCHEMA_DIR) -> int:
    """Validate a data tree; return a process-style status code."""
    ERRORS.clear()
    WARNINGS.clear()
    validators = load_schemas(schema_dir)
    jurisdictions: dict[str, dict] = {}
    offices: dict[str, tuple[str, dict]] = {}
    people: dict[str, dict] = {}
    elections: dict[str, dict] = {}
    file_of: dict[str, Path] = {}
    person_candidacies: dict[str, list[tuple[str, dict, Path]]] = defaultdict(list)
    contests: dict[str, tuple[dict, dict, Path]] = {}

    for path in sorted(data_dir.rglob("*.yaml")):
        document = load_yaml(path)
        if document is None:
            continue
        kind = _kind(path)
        if kind == "jurisdictions":
            if validate_schema(validators["jurisdiction.schema.json"], document, path):
                _register(jurisdictions, document["id"], document, path, file_of)
                for office in document.get("offices", []):
                    _register(offices, office["id"], (document["id"], office), path, file_of)
        elif kind == "people":
            if validate_schema(validators["person.schema.json"], document, path):
                _register(people, document["id"], document, path, file_of)
                for candidacy in document.get("candidacies", []):
                    person_candidacies[candidacy["contest_id"]].append((document["id"], candidacy, path))
                schemes: set[str] = set()
                for identifier in document.get("identifiers", []):
                    if identifier["scheme"] in schemes:
                        error(f"{path}: person '{document['id']}' repeats external identifier scheme '{identifier['scheme']}'")
                    schemes.add(identifier["scheme"])
                    key = (identifier["scheme"], identifier["identifier"])
                    if key in file_of:
                        error(f"{path}: duplicate external identifier {key!r} (already defined in {file_of[key]})")
                    else:
                        file_of[key] = path
        elif kind == "elections":
            if validate_schema(validators["election.schema.json"], document, path):
                _register(elections, document["id"], document, path, file_of)
                for contest in document["contests"]:
                    _register(contests, contest["id"], (document, contest, path), path, file_of)
        else:
            warn(f"{path}: unrecognized data directory '{kind}', skipped")

    for person_id, person in people.items():
        path = file_of[person_id]
        for index, role in enumerate(person["roles"]):
            _check_office_reference(role, path, f"roles[{index}]", jurisdictions, offices)
        for candidacy in person["candidacies"]:
            _check_office_reference(candidacy, path, "candidacy", jurisdictions, offices)

    for contest_id, (election, contest, path) in contests.items():
        _check_office_reference(contest, path, f"contests[{contest_id}]", jurisdictions, offices)
        for person_id in contest["candidate_ids"]:
            if person_id not in people:
                error(f"{path}: contest '{contest_id}' candidate person_id '{person_id}' does not resolve")
            elif not any(c["contest_id"] == contest_id for c in people[person_id]["candidacies"]):
                error(f"{path}: contest '{contest_id}' candidate '{person_id}' has no reciprocal person candidacy")
        winners = contest["winners"]
        if contest["result_status"] == "pending" and winners is not None:
            error(f"{path}: pending contest '{contest_id}' must have winners: null")
        if contest["result_status"] == "certified" and not winners:
            error(f"{path}: certified contest '{contest_id}' must have at least one winner")
        for winner in winners or []:
            person_id = winner["person_id"]
            if person_id not in people:
                error(f"{path}: contest '{contest_id}' winner person_id '{person_id}' does not resolve")
            if person_id not in contest["candidate_ids"]:
                error(f"{path}: contest '{contest_id}' winner '{person_id}' is not in candidate_ids")

    for contest_id, candidacies in person_candidacies.items():
        if contest_id not in contests:
            for person_id, _, path in candidacies:
                error(f"{path}: person '{person_id}' candidacy '{contest_id}' has no reciprocal election contest")

    _cross_validate(people, elections, contests, file_of)
    print(f"Validated: {len(jurisdictions)} jurisdictions, {len(offices)} offices, {len(people)} people, {len(elections)} elections")
    if WARNINGS:
        print(f"⚠ {len(WARNINGS)} warning(s):")
        for message in WARNINGS:
            print(f"  ⚠ {message}")
    if ERRORS:
        print(f"✗ {len(ERRORS)} error(s):")
        for message in ERRORS:
            print(f"  ✗ {message}")
        print("FAILED (schema/reference errors)")
        return 1
    print("PASSED" + (f" with {len(WARNINGS)} warning(s) for human review" if WARNINGS else ""))
    return 0


def _check_office_reference(reference: dict, path: Path, location: str, jurisdictions: dict, offices: dict) -> None:
    jurisdiction_id = reference["jurisdiction_id"]
    office_id = reference["office_id"]
    if jurisdiction_id not in jurisdictions:
        error(f"{path}: {location} has no jurisdiction '{jurisdiction_id}'")
        return
    if office_id not in offices:
        error(f"{path}: {location} has no office '{office_id}'")
        return
    if offices[office_id][0] != jurisdiction_id:
        error(f"{path}: {location} office '{office_id}' belongs to '{offices[office_id][0]}', not '{jurisdiction_id}'")


def _cross_validate(people: dict, elections: dict, contests: dict, file_of: dict) -> None:
    latest_certified: dict[str, tuple[dict, dict]] = {}
    for election, contest, _ in contests.values():
        if contest["result_status"] != "certified":
            continue
        previous = latest_certified.get(contest["office_id"])
        if previous is None or election["date"] > previous[0]["date"]:
            latest_certified[contest["office_id"]] = (election, contest)
        for winner in contest["winners"] or []:
            person = people.get(winner["person_id"])
            if person and norm_name(person["name"]) != norm_name(winner["name"]):
                warn(f"CROSS[name-disagreement] winner '{winner['name']}' is linked to person '{person['name']}' ({winner['person_id']})")

    by_office: dict[str, list[dict]] = defaultdict(list)
    for person in people.values():
        for role in person["roles"]:
            by_office[role["office_id"]].append(person)
    for office_id, (election, contest) in latest_certified.items():
        holders = {norm_name(person["name"]) for person in by_office.get(office_id, [])}
        for winner in contest["winners"] or []:
            if norm_name(winner["name"]) not in holders:
                current = ", ".join(repr(person["name"]) for person in by_office.get(office_id, [])) or "(no one on record)"
                warn(f"CROSS[winner-not-seated] office '{office_id}': '{winner['name']}' won the certified {election['date']} election but people lists {current}")
    for person_id, person in people.items():
        for role in person["roles"]:
            if role.get("term", {}).get("how_seated") != "elected":
                continue
            traced = any(
                person_id in contest["candidate_ids"] or any(w["person_id"] == person_id for w in contest["winners"] or [])
                for _, contest, _ in contests.values() if contest["office_id"] == role["office_id"]
            )
            if not traced:
                warn(f"CROSS[no-election-trace] {file_of[person_id]}: '{person['name']}' is recorded as elected to '{role['office_id']}' but no election candidacy names them")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    result = validate()
    if result == 0 and WARNINGS and args.strict:
        print("FAILED (--strict: warnings treated as errors)")
        return 1
    return result


if __name__ == "__main__":
    raise SystemExit(main())
