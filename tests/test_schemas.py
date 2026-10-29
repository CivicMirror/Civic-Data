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


def test_person_with_no_candidacies_is_valid() -> None:
    # Officeholding now lives entirely in membership.yaml records, so a
    # person with no candidacies (e.g. an appointed officeholder with no
    # election on file) is a valid person record on its own.
    document = load_fixture("nc-jordan-lee.yaml")
    document["candidacies"] = []
    assert_valid("person.schema.json", document)


def test_person_schema_rejects_roles() -> None:
    # roles[] was retired in favor of membership.yaml; person.schema.json
    # no longer recognizes it.
    document = load_fixture("nc-jordan-lee.yaml")
    document["roles"] = [{
        "jurisdiction_id": "ocd-jurisdiction/country:us/state:nc/government",
        "office_id": "nc/us-senator",
        "term": {"start": "2023-01-03", "how_seated": "elected"},
    }]
    errors = list(Draft202012Validator(load_schema("person.schema.json")).iter_errors(document))
    assert any("roles" in error.message for error in errors)


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


def test_primary_contests_keep_party_specific_identity() -> None:
    democratic = load_fixture("nc-2026-democratic-primary.yaml")
    republican = load_fixture("nc-2026-republican-primary.yaml")
    assert democratic["contests"][0]["id"] != republican["contests"][0]["id"]
    assert_valid("election.schema.json", democratic)
    assert_valid("election.schema.json", republican)


def test_multi_seat_fixture_preserves_seat_identity() -> None:
    document = load_fixture("ma-legislative-multi-seat.yaml")
    assert {contest["seat"] for contest in document["contests"]} == {"5th Suffolk", "6th Suffolk"}
    assert_valid("election.schema.json", document)


def test_all_acceptance_election_fixtures_validate() -> None:
    for path in FIXTURES.glob("*.yaml"):
        if path.name == "nc-jordan-lee.yaml":
            continue
        assert_valid("election.schema.json", yaml.safe_load(path.read_text()))


# --- membership start/end precision (issue #62) ---------------------------

MEMBERSHIP = {
    "id": "millbury-select-board-example",
    "person_id": "ocd-person/4c28941f-6f8a-4e86-b702-0741297db7d0",
    "organization_id": "ocd-organization/550e8400-e29b-41d4-a716-446655440001",
    "post_id": "millbury-ma/select-board",
    "role": "Select Board Member",
    "sources": [{"url": "https://example.gov/roster"}],
}


def membership_with(**fields: str) -> dict:
    document = copy.deepcopy(MEMBERSHIP)
    document.update(fields)
    return document


def test_membership_dates_accept_every_source_precision() -> None:
    # Precision varies by source: most town rosters print only "term expires
    # 2029", a few print "May 2029", and only a charter with an explicit
    # seating rule yields a full date. All three are recorded as published.
    for value in ("2029", "2029-05", "2029-05-14"):
        assert_valid("membership.schema.json", membership_with(start="2026", end=value))


def test_membership_dates_reject_non_iso_and_non_date_values() -> None:
    for value in ("5/14/2029", "412", "2029-13", "2029-05-32", "2029-5-4", "May 2029", ""):
        errors = list(
            Draft202012Validator(load_schema("membership.schema.json")).iter_errors(
                membership_with(end=value)
            )
        )
        assert errors, f"{value!r} should not be a valid membership end"
