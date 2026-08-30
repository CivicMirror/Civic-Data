from scripts.ecode360.amlegal import parse_amlegal_payload, parse_amlegal_sections
from scripts.ecode360.errors import ECodeError


FIXTURE = """
<div id="rid-title" class="rbox Title"><div>WELLS CITY CHARTER</div></div>
<div id="rid-article" class="rbox Normal-Level"><div>ARTICLE I</div></div>
<div id="rid-heading" class="rbox Normal-Level"><h5><a id="JD_Chtr.Sec.1.010"></a>Sec. 1.010&nbsp;&nbsp;&nbsp;Preamble: Legislative Intent.</h5></div>
<div id="rid-content" class="rbox Normal-Level"><div>&nbsp;&nbsp;&nbsp;The legislature establishes this charter.</div></div>
"""


def test_parses_amlegal_rendered_charter_blocks() -> None:
    result = parse_amlegal_sections(FIXTURE, "https://codelibrary.amlegal.com/codes/wellsnv/latest/wells_nv/0-0-0-14784")
    assert result.title == "WELLS CITY CHARTER"
    assert result.article_count == 1
    assert result.sections[0].guid == "JD_Chtr.Sec.1.010"
    assert result.sections[0].number == "1.010"
    assert result.sections[0].title == "Preamble: Legislative Intent."
    assert result.sections[0].text == "The legislature establishes this charter."
    assert result.sections[0].url.endswith("#JD_Chtr.Sec.1.010")


def test_rejects_page_without_sections() -> None:
    try:
        parse_amlegal_sections('<div class="rbox Title"><div>Charter</div></div>', "https://example.test/charter")
    except ECodeError as error:
        assert error.code == "amlegal_extraction_failed"
    else:
        raise AssertionError("expected extraction failure")


def test_parses_browser_payload_and_skips_empty_rows() -> None:
    result = parse_amlegal_payload(
        {
            "title": "Wells Charter",
            "sections": [
                {"guid": "JD_Chtr.Sec.1.010", "heading": "Sec. 1.010 Preamble.", "text": "Text."},
                {"guid": "JD_Chtr.Sec.1.020", "heading": "Sec. 1.020 Empty.", "text": ""},
            ],
            "next": "",
            "children": ["https://example.test/article-1"],
        },
        "https://example.test/charter",
    )
    assert list(result["sections"])[0] == "JD_Chtr.Sec.1.010"
    assert result["sections"]["JD_Chtr.Sec.1.010"].text == "Text."
    assert result["children"] == ("https://example.test/article-1",)


def test_parses_hamden_section_heading_style() -> None:
    result = parse_amlegal_payload(
        {"title": "Hamden Charter", "sections": [{"guid": "JD_Section1-3", "heading": "SECTION 1-3: TIME OF APPOINTMENTS", "text": "Meeting text."}]},
        "https://codelibrary.amlegal.com/codes/hamden/latest/hamden_ct/0-0-0-8431",
    )
    section = result["sections"]["JD_Section1-3"]
    assert section.number == "1-3"
    assert section.title == "TIME OF APPOINTMENTS"
