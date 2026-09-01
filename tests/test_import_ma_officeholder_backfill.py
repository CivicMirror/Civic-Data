import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "import_ma_officeholder_backfill.py"


def test_importer_writes_person_and_membership_records(tmp_path: Path) -> None:
    data_dir = tmp_path / "data" / "us" / "ma"
    (data_dir / "organizations" / "municipal").mkdir(parents=True)
    (data_dir / "posts" / "municipal").mkdir(parents=True)

    organization_id = "ocd-organization/11111111-1111-4111-8111-111111111111"
    (data_dir / "organizations" / "municipal" / "example-select-board.yaml").write_text(
        yaml.safe_dump(
            {
                "id": organization_id,
                "name": "Select Board Member",
                "jurisdiction_id": "ocd-jurisdiction/country:us/state:ma/place:example/government",
                "identifiers": [],
                "sources": [{"url": "https://example.gov/select-board"}],
            },
            sort_keys=False,
        )
    )
    (data_dir / "posts" / "municipal" / "example-select-board.yaml").write_text(
        yaml.safe_dump(
            {
                "id": "example-ma/select-board",
                "organization_id": organization_id,
                "title": "Select Board Member",
                "seats": 3,
                "sources": [{"url": "https://example.gov/select-board"}],
            },
            sort_keys=False,
        )
    )
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "retrieved": "2026-08-26",
                "pipeline": "MA municipal officeholder backfill",
                "officeholders": [
                    {
                        "municipality": "example",
                        "post_id": "example-ma/select-board",
                        "name": "Ada Example",
                        "civicpatch_id": "22222222-2222-4222-8222-222222222222",
                        "sources": ["https://example.gov/select-board"],
                    }
                ],
            },
            sort_keys=False,
        )
    )

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--data-dir", str(data_dir), "--manifest", str(manifest), "--write"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    people = list((data_dir / "people" / "municipal").glob("*.yaml"))
    memberships = list((data_dir / "memberships" / "municipal").glob("*.yaml"))
    assert len(people) == 1
    assert people[0].name == "ada-example.yaml"
    assert len(memberships) == 1
    person = yaml.safe_load(people[0].read_text())
    membership = yaml.safe_load(memberships[0].read_text())
    assert person["name"] == "Ada Example"
    assert person["identifiers"] == [
        {"scheme": "civicpatch", "identifier": "22222222-2222-4222-8222-222222222222"}
    ]
    assert membership["person_id"] == person["id"]
    assert membership["organization_id"] == organization_id
    assert membership["post_id"] == "example-ma/select-board"
    assert membership["how_seated"] == "elected"


def test_importer_rejects_conflicting_existing_record(tmp_path: Path) -> None:
    data_dir = tmp_path / "data" / "us" / "ma"
    (data_dir / "organizations" / "municipal").mkdir(parents=True)
    (data_dir / "posts" / "municipal").mkdir(parents=True)
    organization_id = "ocd-organization/11111111-1111-4111-8111-111111111111"
    (data_dir / "organizations" / "municipal" / "example.yaml").write_text(
        yaml.safe_dump({"id": organization_id})
    )
    (data_dir / "posts" / "municipal" / "example.yaml").write_text(
        yaml.safe_dump(
            {
                "id": "example-ma/select-board",
                "organization_id": organization_id,
                "title": "Select Board Member",
            }
        )
    )
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "retrieved": "2026-08-26",
                "pipeline": "MA municipal officeholder backfill",
                "officeholders": [
                    {
                        "municipality": "example",
                        "post_id": "example-ma/select-board",
                        "name": "Ada Example",
                        "sources": ["https://example.gov/select-board"],
                    }
                ],
            },
            sort_keys=False,
        )
    )
    command = [
        sys.executable,
        str(SCRIPT),
        "--data-dir",
        str(data_dir),
        "--manifest",
        str(manifest),
        "--write",
    ]
    first = subprocess.run(command, capture_output=True, text=True)
    assert first.returncode == 0, first.stderr
    person_path = next((data_dir / "people" / "municipal").glob("*.yaml"))
    original = person_path.read_text()
    person_path.write_text(original.replace("name: Ada Example", "name: Wrong Person"))

    second = subprocess.run(command, capture_output=True, text=True)

    assert second.returncode != 0
    assert "conflicting existing record" in second.stderr
    assert "name: Wrong Person" in person_path.read_text()
