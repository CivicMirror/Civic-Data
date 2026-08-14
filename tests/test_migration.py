from __future__ import annotations

from pathlib import Path

import pytest

from scripts.migrate_to_person import convert_official, migrate_tree


def test_convert_official_adds_candidacies_without_losing_public_fields() -> None:
    source = {
        "id": "ocd-person/4c28941f-6f8a-4e86-b702-0741297db7d0",
        "name": "Jordan Lee",
        "roles": [{
            "jurisdiction_id": "ocd-division/country:us/state:nc",
            "office_id": "nc/us-senator",
            "term": {"start": "2023-01-03", "how_seated": "elected"},
        }],
        "contact": {"phone": "555-0100"},
        "verification": {"status": "unverified"},
        "sources": [{"url": "https://example.gov"}],
    }
    result = convert_official(source)
    assert result["candidacies"] == []
    assert result["contact"] == source["contact"]
    assert result["roles"] == source["roles"]


def test_migrate_tree_preserves_tiered_directory_and_refuses_collision(tmp_path: Path) -> None:
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    input_path = source / "officials" / "federal" / "example.yaml"
    input_path.parent.mkdir(parents=True)
    input_path.write_text("""id: ocd-person/4c28941f-6f8a-4e86-b702-0741297db7d0\nname: Jordan Lee\nroles:\n  - jurisdiction_id: ocd-division/country:us/state:nc\n    office_id: nc/us-senator\nverification:\n  status: unverified\nsources:\n  - url: https://example.gov\n""")
    migrated = migrate_tree(source, destination)
    assert migrated == [destination / "people" / "federal" / "example.yaml"]
    assert (destination / "people" / "federal" / "example.yaml").exists()
    with pytest.raises(FileExistsError):
        migrate_tree(source, destination)
