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


def test_migrated_repository_validates_with_human_review_warnings() -> None:
    assert validator.validate(ROOT / "data", ROOT / "schemas") == 0
    assert not validator.ERRORS
    assert validator.WARNINGS


def test_duplicate_external_identifier_is_an_error(tmp_path: Path) -> None:
    data = copied_data(tmp_path)
    first = data / "us/ma/people/federal/ed-markey.yaml"
    second = data / "us/ma/people/federal/elizabeth-warren.yaml"
    first_doc = yaml.safe_load(first.read_text())
    second_doc = yaml.safe_load(second.read_text())
    first_doc["identifiers"] = [{"scheme": "civicmirror", "identifier": "same-person"}]
    second_doc["identifiers"] = [{"scheme": "civicmirror", "identifier": "same-person"}]
    first.write_text(yaml.safe_dump(first_doc, sort_keys=False))
    second.write_text(yaml.safe_dump(second_doc, sort_keys=False))
    assert validator.validate(data, ROOT / "schemas") == 1
    assert any("duplicate external identifier" in message for message in validator.ERRORS)


def test_person_cannot_repeat_external_identifier_scheme(tmp_path: Path) -> None:
    data = copied_data(tmp_path)
    person = data / "us/ma/people/federal/ed-markey.yaml"
    document = yaml.safe_load(person.read_text())
    document["identifiers"] = [
        {"scheme": "civicmirror", "identifier": "one"},
        {"scheme": "civicmirror", "identifier": "two"},
    ]
    person.write_text(yaml.safe_dump(document, sort_keys=False))
    assert validator.validate(data, ROOT / "schemas") == 1
    assert any("repeats external identifier scheme" in message for message in validator.ERRORS)


def test_unresolved_contest_candidate_is_an_error(tmp_path: Path) -> None:
    data = copied_data(tmp_path)
    election = data / "us/ma/elections/cd-1--2012-11-06--us-representative.yaml"
    document = yaml.safe_load(election.read_text())
    document["contests"][0]["candidate_ids"] = ["ocd-person/00000000-0000-0000-0000-000000000000"]
    election.write_text(yaml.safe_dump(document, sort_keys=False))
    assert validator.validate(data, ROOT / "schemas") == 1
    assert any("does not resolve" in message for message in validator.ERRORS)


def test_candidacy_without_contest_is_an_error(tmp_path: Path) -> None:
    data = copied_data(tmp_path)
    person = data / "us/ma/people/federal/richard-neal.yaml"
    document = yaml.safe_load(person.read_text())
    document["candidacies"][0]["contest_id"] = "ma/does-not-exist"
    person.write_text(yaml.safe_dump(document, sort_keys=False))
    assert validator.validate(data, ROOT / "schemas") == 1
    assert any("no reciprocal election contest" in message for message in validator.ERRORS)
