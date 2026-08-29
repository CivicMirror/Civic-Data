from scripts.ecode360.errors import ECodeError
from scripts.ecode360.models import CharterResult, DirectoryEntry, SectionResult
from scripts.ecode360.output import build_error, build_success


def test_build_success_preserves_ordered_charter_contract() -> None:
    source = DirectoryEntry(
        "Town of Example",
        "EX",
        "Sample County",
        "EX1000",
        "https://ecode360.com/EX1000",
    )
    sections = (
        SectionResult(
            "2001",
            "1-1",
            "Purpose",
            ("Charter", "Article 1"),
            "https://ecode360.com/2001",
            "Purpose text.",
            "",
        ),
    )
    charter = CharterResult(
        "2000", "Charter", "https://ecode360.com/2000", 1, sections
    )

    result = build_success(
        "Example", "EX", source, charter, "2026-08-28T00:00:00Z"
    )

    assert result["schema_version"] == "1.0"
    assert result["status"] == "success"
    assert result["resolved_source"]["directory_url"] == (
        "https://www.icccodesolutions.org/text-library/"
    )
    assert result["charter"]["section_count"] == 1
    assert result["charter"]["sections"][0]["hierarchy"] == [
        "Charter",
        "Article 1",
    ]
    assert result["charter"]["sections"][0]["history"] == ""
    assert result["warnings"] == []


def test_build_error_omits_candidates_when_they_are_absent() -> None:
    error = ECodeError("municipality_not_found", "No municipality matched", 3)

    result = build_error(
        "Missing", "EX", error, "2026-08-28T00:00:00Z"
    )

    assert result["status"] == "error"
    assert result["error"] == {
        "code": "municipality_not_found",
        "message": "No municipality matched",
    }


def test_build_error_preserves_candidates() -> None:
    error = ECodeError(
        "ambiguous_municipality",
        "Multiple municipalities matched",
        3,
        candidates=({"display_name": "Town of Example", "state": "EX"},),
    )

    result = build_error(
        "Example", "EX", error, "2026-08-28T00:00:00Z"
    )

    assert result["error"]["candidates"] == [
        {"display_name": "Town of Example", "state": "EX"}
    ]
