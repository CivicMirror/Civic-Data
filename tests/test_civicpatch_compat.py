from scripts.civicpatch_compat import (
    CANONICAL_MILLBURY_DIVISION,
    MILLBURY_SELECT_BOARD_POST,
    map_millbury_post,
    normalize_division_ocdid,
)


def test_normalizes_county_qualified_millbury_division() -> None:
    assert normalize_division_ocdid(
        "ocd-division/country:us/state:ma/county:worcester/place:millbury"
    ) == CANONICAL_MILLBURY_DIVISION


def test_maps_internal_and_generic_civicpatch_titles_to_formal_post() -> None:
    result = map_millbury_post({"post_id": "civicpatch-123", "office": {"name": "Chair"}})
    assert result["post_id"] == MILLBURY_SELECT_BOARD_POST
    assert result["identifier"] == {"scheme": "civicpatch-post", "identifier": "civicpatch-123"}
    assert result["source_role"] == "Chair"
