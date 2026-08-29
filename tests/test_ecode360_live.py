import pytest

from scripts.ecode360.__main__ import execute


@pytest.mark.live
def test_abington_current_charter_baseline() -> None:
    result = execute("Abington", "MA")
    assert result["resolved_source"]["ecode_id"] == "AB2001"
    assert result["charter"]["guid"] == "12064945"
    assert result["charter"]["article_count"] == 8
    assert result["charter"]["section_count"] == 65
    assert all(
        item["text"].strip()
        and item["url"].startswith("https://ecode360.com/")
        for item in result["charter"]["sections"]
    )
