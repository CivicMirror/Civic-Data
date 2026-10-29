from __future__ import annotations

from pathlib import Path
import shutil

import yaml

from scripts import validate as validator


ROOT = Path(__file__).resolve().parents[1]


def copied_data(tmp_path: Path) -> Path:
    target = tmp_path / "data"
    shutil.copytree(ROOT / "data", target)
    return target


def test_fresh_millbury_repository_validates_with_only_expected_review_warning() -> None:
    assert validator.validate(ROOT / "data", ROOT / "schemas") == 0
    assert not validator.ERRORS
    assert any("no-election-trace" in message for message in validator.WARNINGS)


def test_duplicate_organization_external_identifier_is_an_error(tmp_path: Path) -> None:
    data = copied_data(tmp_path)
    first = data / "us/ma/organizations/municipal/millbury-select-board.yaml"
    second = data / "us/ma/organizations/municipal/millbury-school-committee.yaml"
    first_doc = yaml.safe_load(first.read_text())
    second_doc = yaml.safe_load(second.read_text())
    second_doc["identifiers"] = first_doc["identifiers"]
    second.write_text(yaml.safe_dump(second_doc, sort_keys=False))
    assert validator.validate(data, ROOT / "schemas") == 1
    assert any("duplicate external identifier" in message for message in validator.ERRORS)


def test_membership_post_organization_mismatch_is_an_error(tmp_path: Path) -> None:
    data = copied_data(tmp_path)
    membership = data / "us/ma/memberships/municipal/millbury-select-board-mary-krumsiek.yaml"
    document = yaml.safe_load(membership.read_text())
    document["organization_id"] = "ocd-organization/550e8400-e29b-41d4-a716-446655440001"
    membership.write_text(yaml.safe_dump(document, sort_keys=False))
    assert validator.validate(data, ROOT / "schemas") == 1
    assert any("different organization" in message for message in validator.ERRORS)


def test_validator_enforces_date_format_but_not_uri(tmp_path: Path) -> None:
    # format is annotation-only unless a checker is supplied (issue #62).
    # sources[].retrieved is now really enforced; sources[].url is not,
    # because ~295 records cite offline provenance ("user-supplied PDF, ...")
    # rather than a URL.
    validators = validator.load_schemas(ROOT / "schemas")
    membership = validators["membership.schema.json"]
    document = {
        "id": "example",
        "person_id": "ocd-person/4c28941f-6f8a-4e86-b702-0741297db7d0",
        "organization_id": "ocd-organization/550e8400-e29b-41d4-a716-446655440001",
        "role": "Select Board Member",
        "sources": [{"url": "user-supplied PDF, Town of Oakham FY2025 Annual Town Report",
                     "retrieved": "https://example.gov/roster"}],
    }
    messages = [error.message for error in membership.iter_errors(document)]
    assert any("is not a 'date'" in message for message in messages), messages
    assert not any("'uri'" in message for message in messages), messages

    document["sources"][0]["retrieved"] = "2026-10-01"
    assert not list(membership.iter_errors(document))
