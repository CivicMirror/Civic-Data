from __future__ import annotations

import copy
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "person-candidacy"


def load_schema(name: str) -> dict:
    return json.loads((ROOT / "schemas" / name).read_text())


def load_fixture(name: str) -> dict:
    return yaml.safe_load((FIXTURES / name).read_text())


def assert_valid(schema_name: str, document: dict) -> None:
    errors = sorted(Draft202012Validator(load_schema(schema_name)).iter_errors(document), key=lambda e: list(e.path))
    assert not errors, "\n".join(error.message for error in errors)


def test_candidate_only_person_is_valid() -> None:
    assert_valid("person.schema.json", load_fixture("nc-jordan-lee.yaml"))


def test_person_must_have_a_role_or_candidacy() -> None:
    document = load_fixture("nc-jordan-lee.yaml")
    document["candidacies"] = []
    errors = list(Draft202012Validator(load_schema("person.schema.json")).iter_errors(document))
    assert any("candidacies" in error.message or "roles" in error.message for error in errors)


def test_person_can_have_both_role_and_candidacy() -> None:
    document = load_fixture("nc-jordan-lee.yaml")
    document["roles"] = [{
        "jurisdiction_id": "ocd-division/country:us/state:nc",
        "office_id": "nc/us-senator",
        "term": {"start": "2023-01-03", "how_seated": "elected"},
    }]
    assert_valid("person.schema.json", document)


def test_scheduled_contest_can_have_no_winners() -> None:
    assert_valid("election.schema.json", load_fixture("nc-2026-general.yaml"))


def test_candidacy_rejects_private_filing_contact() -> None:
    document = load_fixture("nc-jordan-lee.yaml")
    document["candidacies"][0]["filing_email"] = "jordan@example.com"
    errors = list(Draft202012Validator(load_schema("person.schema.json")).iter_errors(document))
    assert any("filing_email" in error.message for error in errors)


def test_duplicate_external_identifier_entries_are_rejected() -> None:
    document = load_fixture("nc-jordan-lee.yaml")
    document["identifiers"].append(copy.deepcopy(document["identifiers"][0]))
    errors = list(Draft202012Validator(load_schema("person.schema.json")).iter_errors(document))
    assert any("unique" in error.message for error in errors)


def test_certified_contest_has_a_person_winner() -> None:
    document = load_fixture("nc-2026-general.yaml")
    document["status"] = "certified"
    contest = document["contests"][0]
    contest["result_status"] = "certified"
    contest["winners"] = [{
        "person_id": "ocd-person/4c28941f-6f8a-4e86-b702-0741297db7d0",
        "name": "Jordan Lee",
    }]
    assert_valid("election.schema.json", document)
