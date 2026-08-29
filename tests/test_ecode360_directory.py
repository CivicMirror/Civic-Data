import pytest

from scripts.ecode360.directory import (
    normalize_municipality,
    normalize_state,
    parse_directory,
    resolve_municipality,
)
from scripts.ecode360.errors import ECodeError


DIRECTORY_HTML = """
<a id="MA" class="stateAnchor"></a>
<div class="listItem">
  <div class="codeTitle"><a class="codeLink" href="https://ecode360.com/EX1000">Town of Example</a></div>
  <div class="codeCounty">(Sample County)</div>
</div>
<div class="listItem">
  <div class="codeTitle"><a class="codeLink" href="https://ecode360.com/EL1000">City of Elsewhere</a></div>
  <div class="codeCounty">(Other County)</div>
</div>
<div class="listItem">
  <div class="codeTitle"><a class="codeLink" href="https://example.municipal.codes/">Village of Thirdplace</a></div>
  <div class="codeCounty">(Third County)</div>
</div>
<a id="NY" class="stateAnchor"></a>
<div class="listItem">
  <div class="codeTitle"><a class="codeLink" href="https://ecode360.com/EL2000">City of Elsewhere</a></div>
  <div class="codeCounty">(New York County)</div>
</div>
"""


def test_normalizers_accept_full_state_and_strip_government_prefix() -> None:
    assert normalize_state("Massachusetts") == "MA"
    assert normalize_state(" ma ") == "MA"
    assert normalize_municipality("Town of Saint-Pierre") == "saint pierre"


def test_parser_tracks_state_name_county_and_ecode_id() -> None:
    entries = parse_directory(DIRECTORY_HTML)
    assert entries[0].display_name == "Town of Example"
    assert entries[0].state == "MA"
    assert entries[0].county == "Sample County"
    assert entries[0].ecode_id == "EX1000"
    assert entries[2].ecode_id == ""


def test_resolves_full_state_name_and_bare_municipality() -> None:
    result = resolve_municipality(parse_directory(DIRECTORY_HTML), "Example", "Massachusetts")
    assert result.ecode_id == "EX1000"


def test_rejects_unsupported_provider() -> None:
    with pytest.raises(ECodeError) as caught:
        resolve_municipality(parse_directory(DIRECTORY_HTML), "Thirdplace", "MA")
    assert caught.value.code == "unsupported_provider"
    assert caught.value.exit_status == 3
    assert "municipal.codes" in str(caught.value)


def test_rejects_ambiguous_normalized_municipality() -> None:
    entries = parse_directory(
        DIRECTORY_HTML
        + '<a id="MA" class="stateAnchor"></a><div class="listItem"><a class="codeLink" href="https://ecode360.com/EL1001">City of Elsewhere</a></div>'
    )
    with pytest.raises(ECodeError) as caught:
        resolve_municipality(entries, "Elsewhere", "MA")
    assert caught.value.code == "ambiguous_municipality"
    assert len(caught.value.candidates or ()) == 2


def test_reports_not_found_with_non_authoritative_suggestions() -> None:
    with pytest.raises(ECodeError) as caught:
        resolve_municipality(parse_directory(DIRECTORY_HTML), "Exampl", "MA")
    assert caught.value.code == "municipality_not_found"
    assert caught.value.exit_status == 3
    assert caught.value.candidates


def test_rejects_unknown_state() -> None:
    with pytest.raises(ECodeError) as caught:
        resolve_municipality(parse_directory(DIRECTORY_HTML), "Example", "ZZ")
    assert caught.value.code == "invalid_state"
    assert caught.value.exit_status == 2
