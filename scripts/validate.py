#!/usr/bin/env python3
"""Civic-Data validator.

Runs four layers of checks over data/:

  1. Schema validation      — every YAML file matches its JSON Schema.
  2. Reference integrity    — each role's jurisdiction_id / office_id resolves,
                               and official_id links resolve.
  3. Duplicate detection    — no duplicate entity IDs anywhere in the repo.
  4. Cross-validation       — officials directory vs. election linkages:
       * an official seated as 'elected' should have a matching election
         linkage for their office (warn if none found);
       * an election winner linked via official_id should name-match the
         official record (warn on disagreement);
       * a winner of the most recent certified election for an office should
         appear in the officials directory for that office (warn if absent).

Exit code: 1 on any ERROR (layers 1–3). Cross-validation findings are
WARNINGS by default — they may represent real-world events (resignation,
appointment, recall), so a human decides. Pass --strict to make warnings
fail CI too.
"""

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


def load_schemas() -> dict[str, Draft202012Validator]:
    """Load all schemas into a shared registry so $ref between them resolves."""
    raw = {}
    for path in SCHEMA_DIR.glob("*.schema.json"):
        with open(path) as f:
            raw[path.name] = json.load(f)

    registry = Registry()
    for name, schema in raw.items():
        registry = registry.with_resource(name, Resource.from_contents(schema))
        # Also register under the declared $id so absolute refs resolve.
        if "$id" in schema:
            registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))

    return {
        name: Draft202012Validator(schema, registry=registry)
        for name, schema in raw.items()
    }


def load_yaml(path: Path) -> dict | None:
    try:
        with open(path) as f:
            doc = yaml.safe_load(f)
    except yaml.YAMLError as e:
        error(f"{path.relative_to(REPO)}: YAML parse error: {e}")
        return None
    if not isinstance(doc, dict):
        error(f"{path.relative_to(REPO)}: top-level document must be a mapping")
        return None
    return doc


def validate_schema(validator: Draft202012Validator, doc: dict, path: Path) -> bool:
    ok = True
    for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        loc = "/".join(str(p) for p in err.path) or "(root)"
        error(f"{path.relative_to(REPO)}: [{loc}] {err.message}")
        ok = False
    return ok


def norm_name(name: str) -> str:
    """Normalize a person name for comparison: casefold, strip accents,
    collapse whitespace and punctuation. Deliberately conservative — this is
    a *flagging* heuristic, not identity resolution."""
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = "".join(c if c.isalnum() or c.isspace() else " " for c in s.casefold())
    return " ".join(s.split())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true",
                        help="treat cross-validation warnings as errors")
    args = parser.parse_args()

    validators = load_schemas()

    jurisdictions: dict[str, dict] = {}   # ocd-division id -> doc
    offices: dict[str, tuple[str, dict]] = {}  # office id -> (jurisdiction id, office doc)
    officials: dict[str, dict] = {}       # ocd-person id -> doc
    linkages: dict[str, dict] = {}        # linkage id -> doc
    file_of: dict[str, Path] = {}

    # ---------- Layer 1: schema validation + collection ----------
    for path in sorted(DATA_DIR.rglob("*.yaml")):
        doc = load_yaml(path)
        if doc is None:
            continue
        kind = path.parent.name  # jurisdictions | officials | elections
        if kind == "jurisdictions":
            if validate_schema(validators["jurisdiction.schema.json"], doc, path):
                _register(jurisdictions, doc["id"], doc, path, file_of)
                for office in doc.get("offices", []):
                    _register(dict_view := offices, office["id"],
                              (doc["id"], office), path, file_of,
                              raw_store=True)
        elif kind == "officials":
            if validate_schema(validators["official.schema.json"], doc, path):
                _register(officials, doc["id"], doc, path, file_of)
        elif kind == "elections":
            if validate_schema(validators["election-linkage.schema.json"], doc, path):
                _register(linkages, doc["id"], doc, path, file_of)
        else:
            warn(f"{path.relative_to(REPO)}: unrecognized data directory '{kind}', skipped")

    # ---------- Layer 2: reference integrity ----------
    for oid, doc in officials.items():
        rel = file_of[oid].relative_to(REPO)
        for i, role in enumerate(doc["roles"]):
            loc = f"roles[{i}]"
            if role["jurisdiction_id"] not in jurisdictions:
                error(f"{rel}: {loc} jurisdiction_id '{role['jurisdiction_id']}' does not resolve")
            if role["office_id"] not in offices:
                error(f"{rel}: {loc} office_id '{role['office_id']}' does not resolve")
            elif role["jurisdiction_id"] in jurisdictions:
                juris_of_office = offices[role["office_id"]][0]
                if juris_of_office != role["jurisdiction_id"]:
                    error(f"{rel}: {loc} office '{role['office_id']}' belongs to "
                          f"'{juris_of_office}', not '{role['jurisdiction_id']}'")

    for lid, doc in linkages.items():
        rel = file_of[lid].relative_to(REPO)
        if doc["jurisdiction_id"] not in jurisdictions:
            error(f"{rel}: jurisdiction_id '{doc['jurisdiction_id']}' does not resolve")
        if doc["office_id"] not in offices:
            error(f"{rel}: office_id '{doc['office_id']}' does not resolve")
        for w in doc["winners"]:
            pid = w.get("official_id")
            if pid and pid not in officials:
                error(f"{rel}: winner official_id '{pid}' does not resolve")

    # ---------- Layer 4: cross-validation ----------
    # Index: most recent certified linkage per office.
    latest_certified: dict[str, dict] = {}
    for doc in linkages.values():
        if doc["certification"]["status"] != "certified":
            continue
        cur = latest_certified.get(doc["office_id"])
        if cur is None or doc["election_date"] > cur["election_date"]:
            latest_certified[doc["office_id"]] = doc

    officials_by_office: dict[str, list[dict]] = defaultdict(list)
    for doc in officials.values():
        for role in doc["roles"]:
            officials_by_office[role["office_id"]].append(doc)

    findings = 0

    # 4a. Linked winners must name-match their official record.
    for lid, doc in linkages.items():
        rel = file_of[lid].relative_to(REPO)
        for w in doc["winners"]:
            pid = w.get("official_id")
            if pid and pid in officials:
                official_name = officials[pid]["name"]
                if norm_name(official_name) != norm_name(w["name"]):
                    findings += 1
                    warn(f"CROSS[name-disagreement] {rel}: winner '{w['name']}' is "
                         f"linked to official '{official_name}' ({pid}) but names differ")

    # 4b. Most recent certified winner should appear in the officials directory.
    for office_id, link in latest_certified.items():
        holders = {norm_name(o["name"]) for o in officials_by_office.get(office_id, [])}
        for w in link["winners"]:
            if norm_name(w["name"]) not in holders:
                findings += 1
                current = ", ".join(
                    f"'{o['name']}'" for o in officials_by_office.get(office_id, [])
                ) or "(no one on record)"
                warn(f"CROSS[winner-not-seated] office '{office_id}': "
                     f"'{w['name']}' won the certified {link['election_date']} election "
                     f"but the officials directory lists {current}. "
                     f"Possible scrape error OR real-world succession event — human review needed.")

    # 4c. Elected officials should trace back to an election linkage.
    for oid, doc in officials.items():
        for role in doc["roles"]:
            if role.get("term", {}).get("how_seated") != "elected":
                continue
            office_links = [l for l in linkages.values() if l["office_id"] == role["office_id"]]
            traced = any(
                norm_name(w["name"]) == norm_name(doc["name"]) or w.get("official_id") == oid
                for l in office_links for w in l["winners"]
            )
            if not traced:
                findings += 1
                warn(f"CROSS[no-election-trace] {file_of[oid].relative_to(REPO)}: "
                     f"'{doc['name']}' is recorded as elected to '{role['office_id']}' "
                     f"but no election linkage names them.")

    # ---------- Report ----------
    print(f"Validated: {len(jurisdictions)} jurisdictions, {len(offices)} offices, "
          f"{len(officials)} officials, {len(linkages)} election linkages\n")

    if WARNINGS:
        print(f"⚠ {len(WARNINGS)} warning(s):")
        for w in WARNINGS:
            print(f"  ⚠ {w}")
        print()
    if ERRORS:
        print(f"✗ {len(ERRORS)} error(s):")
        for e in ERRORS:
            print(f"  ✗ {e}")
        print()

    if ERRORS:
        print("FAILED (schema/reference errors)")
        return 1
    if WARNINGS and args.strict:
        print("FAILED (--strict: warnings treated as errors)")
        return 1
    print("PASSED" + (f" with {len(WARNINGS)} warning(s) for human review" if WARNINGS else ""))
    return 0


def _register(store: dict, key: str, value, path: Path, file_of: dict,
              raw_store: bool = False) -> None:
    if key in store:
        error(f"{path.relative_to(REPO)}: duplicate ID '{key}' "
              f"(already defined in {file_of[key].relative_to(REPO)})")
        return
    store[key] = value
    file_of[key] = path


if __name__ == "__main__":
    sys.exit(main())
