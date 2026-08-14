"""Small, explicit CivicPatch-to-Civic-Data identifier mappings."""

from __future__ import annotations

from collections.abc import Mapping


CANONICAL_MILLBURY_DIVISION = "ocd-division/country:us/state:ma/place:millbury"
MILLBURY_JURISDICTION = "ocd-jurisdiction/country:us/state:ma/place:millbury/government"
MILLBURY_SELECT_BOARD_POST = "millbury-ma/select-board-member"


def normalize_division_ocdid(value: str) -> str:
    """Normalize CivicPatch's county-qualified place ID to the OCD registry ID."""
    if value == "ocd-division/country:us/state:ma/county:worcester/place:millbury":
        return CANONICAL_MILLBURY_DIVISION
    return value


def map_millbury_post(record: Mapping[str, object]) -> dict[str, object]:
    """Map a CivicPatch Millbury office record without losing its source ID."""
    name = str(record.get("office", {}).get("name", "")) if isinstance(record.get("office"), Mapping) else ""
    source_id = str(record.get("post_id", ""))
    if name in {"Council Member", "Chair", "Vice Chair", "Clerk", "Select Board Member"}:
        return {
            "post_id": MILLBURY_SELECT_BOARD_POST,
            "identifier": {"scheme": "civicpatch-post", "identifier": source_id},
            "source_role": name,
        }
    raise ValueError(f"unmapped Millbury CivicPatch office label: {name!r}")
