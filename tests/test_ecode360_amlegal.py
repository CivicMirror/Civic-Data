import pytest

from scripts.ecode360.amlegal import (
    AMLEGAL_EXTRACT_SCRIPT,
    article_labels_for_page,
    navigation_urls,
    parse_amlegal_payload,
    parse_amlegal_sections,
    scoped_article_labels,
    select_charter_url,
)
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


def test_absent_charter_link_returns_structured_error_without_waiting() -> None:
    with pytest.raises(ECodeError) as caught:
        select_charter_url("https://codelibrary.amlegal.com/codes/kingcove/latest/overview", [])
    assert caught.value.code == "amlegal_charter_not_found"


def test_next_doc_is_followed_when_charter_has_no_child_links() -> None:
    charter_url = "https://codelibrary.amlegal.com/codes/lamc/latest/lamc_ca/0-0-0-1"
    page_result = {
        "sections": {},
        "children": (),
        "next": "https://codelibrary.amlegal.com/codes/lamc/latest/lamc_ca/0-0-0-2",
    }
    assert navigation_urls(page_result, charter_url, charter_url) == (page_result["next"],)


def test_navigation_is_scoped_to_selected_amlegal_book() -> None:
    charter_url = "https://codelibrary.amlegal.com/codes/sf/latest/sf_charter/0-0-0-1"
    charter_child = "https://codelibrary.amlegal.com/codes/sf/latest/sf_charter/0-0-0-2"
    page_result = {
        "sections": {},
        "children": (
            charter_child,
            "https://codelibrary.amlegal.com/codes/sf/latest/sf_admin/0-0-0-3",
            "https://example.test/codes/sf/latest/sf_charter/0-0-0-4",
        ),
        "next": "",
    }
    assert navigation_urls(page_result, charter_url, charter_url) == (charter_child,)


def test_hierarchical_content_page_follows_scoped_children_and_same_book_next() -> None:
    charter_url = "https://codelibrary.amlegal.com/codes/hamden/latest/hamden_ct/0-0-0-9"
    current_url = "https://codelibrary.amlegal.com/codes/hamden/latest/hamden_ct/0-0-0-8431"
    next_url = "https://codelibrary.amlegal.com/codes/hamden/latest/hamden_ct/0-0-0-8432"
    page_result = {
        "children": (
            "https://codelibrary.amlegal.com/codes/hamden/latest/hamden_ct/0-0-0-9000",
            "https://codelibrary.amlegal.com/codes/hamden/latest/hamden_admin/0-0-0-1",
        ),
        "next": next_url,
    }
    assert navigation_urls(page_result, current_url, charter_url) == (
        "https://codelibrary.amlegal.com/codes/hamden/latest/hamden_ct/0-0-0-9000",
        next_url,
    )


def test_browser_payload_joins_all_blocks_until_next_section() -> None:
    result = parse_amlegal_payload(
        {
            "title": "Hamden Charter",
            "blocks": [
                {"anchor": "JD_Section1-4", "text": "SECTION 1-4: DEFINITIONS", "classes": "Section rbox"},
                {"anchor": "", "text": "Whenever used in this Charter:", "classes": "Normal-Level rbox"},
                {"anchor": "", "text": '"Board" means a municipal board.', "classes": "Normal-Level rbox"},
                {"anchor": "JD_Section1-5", "text": "SECTION 1-5: APPLICATION", "classes": "Section rbox"},
                {"anchor": "", "text": "This Charter applies.", "classes": "Normal-Level rbox"},
            ],
            "children": [],
            "next": "",
            "articles": ["CHAPTER I"],
        },
        "https://codelibrary.amlegal.com/codes/hamden/latest/hamden_ct/0-0-0-8431",
    )
    assert result["sections"]["JD_Section1-4"].text == 'Whenever used in this Charter:\n"Board" means a municipal board.'


def test_browser_extractor_does_not_treat_body_cross_references_as_section_anchors() -> None:
    assert 'a[href*="#JD_"]' not in AMLEGAL_EXTRACT_SCRIPT
    assert 'a[name^="JD_"]' in AMLEGAL_EXTRACT_SCRIPT


def test_browser_extractor_scopes_navigation_to_selected_charter_tree() -> None:
    assert "charterUrl" in AMLEGAL_EXTRACT_SCRIPT
    assert "closest('.toc-entry')" in AMLEGAL_EXTRACT_SCRIPT


def test_article_labels_are_deduplicated_from_page_metadata() -> None:
    result = parse_amlegal_payload(
        {"title": "Charter", "blocks": [], "children": [], "next": "", "articles": ["ARTICLE I", "ARTICLE II", "ARTICLE I"]},
        "https://codelibrary.amlegal.com/codes/wells/latest/wells_nv/0-0-0-1",
    )
    assert result["articles"] == ("ARTICLE I", "ARTICLE II")


def test_article_count_metadata_is_scoped_to_selected_book() -> None:
    charter_url = "https://codelibrary.amlegal.com/codes/sf/latest/sf_charter/0-0-0-1"
    assert scoped_article_labels(
        (
            ("CHAPTER I", "https://codelibrary.amlegal.com/codes/sf/latest/sf_charter/0-0-0-2"),
            ("CHAPTER II", "https://codelibrary.amlegal.com/codes/sf/latest/sf_admin/0-0-0-3"),
            ("CHAPTER I", "https://codelibrary.amlegal.com/codes/sf/latest/sf_charter/0-0-0-4"),
        ),
        charter_url,
    ) == ("CHAPTER I",)


def test_hierarchical_article_count_ignores_repeated_child_page_sidebar() -> None:
    charter_url = "https://codelibrary.amlegal.com/codes/hamden/latest/hamden_ct/0-0-0-9"
    page_result = {
        "article_documents": (
            ("CHAPTER I", "https://codelibrary.amlegal.com/codes/hamden/latest/hamden_ct/0-0-0-8431"),
        )
    }
    assert article_labels_for_page(page_result, charter_url, charter_url, False) == ("CHAPTER I",)
    assert article_labels_for_page(
        page_result,
        "https://codelibrary.amlegal.com/codes/hamden/latest/hamden_ct/0-0-0-8431",
        charter_url,
        False,
    ) == ()
