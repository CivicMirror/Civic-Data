import pytest

from scripts.ecode360.charter import (
    PageTarget,
    RawSection,
    expected_sections,
    merge_page_results,
    normalize_page_sections,
    page_targets,
    select_charter,
    validate_toc,
)
from scripts.ecode360.errors import ECodeError


def node(kind: str, guid: str, title: str, children: list[dict] | None = None) -> dict:
    return {"type": kind, "guid": guid, "title": title, "children": children or []}


def toc(children: list[dict], guid: str = "EX1000") -> dict:
    return {"type": "code", "guid": guid, "tocName": "Example", "children": children}


def test_rejects_duplicate_guids_and_empty_sections() -> None:
    duplicate = toc([node("section", "s1", "First"), node("section", "s1", "Again")])
    with pytest.raises(ECodeError) as duplicate_error:
        validate_toc(duplicate, "EX1000")
    assert duplicate_error.value.code == "toc_invalid"

    with pytest.raises(ECodeError) as empty_error:
        validate_toc(toc([]), "EX1000")
    assert empty_error.value.code == "toc_invalid"


def test_prefers_nested_charter_chapter_over_division() -> None:
    chapter = node("chapter", "chapter", "Charter", [node("section", "s1", "Purpose")])
    division = node("division", "division", "The Charter", [chapter])
    selected = select_charter(validate_toc(toc([division]), "EX1000"))
    assert selected["guid"] == "chapter"


def test_accepts_compound_charter_label() -> None:
    candidate = node("chapter", "chapter", "Charter and Related Acts", [node("section", "s1", "Purpose")])
    assert select_charter(validate_toc(toc([candidate]), "EX1000"))["guid"] == "chapter"


def test_rejects_unrelated_equal_charter_candidates() -> None:
    first = node("chapter", "first", "Charter", [node("section", "s1", "First")])
    second = node("chapter", "second", "Charter", [node("section", "s2", "Second")])
    with pytest.raises(ECodeError) as caught:
        select_charter(validate_toc(toc([first, second]), "EX1000"))
    assert caught.value.code == "ambiguous_charter"
    assert len(caught.value.candidates or ()) == 2


def test_plans_article_targets_in_toc_order_and_direct_chapter_sections() -> None:
    article = node(
        "article",
        "article-1",
        "Article 1",
        [node("part", "part-1", "General", [node("section", "s1", "First")])],
    )
    direct = node("section", "s2", "Transition")
    charter = node("chapter", "chapter", "Charter", [article, direct])
    assert page_targets(charter) == (
        PageTarget("article-1", ("s1",)),
        PageTarget("chapter", ("s2",)),
    )
    sections = expected_sections(charter)
    assert [section["guid"] for section in sections] == ["s1", "s2"]
    assert sections[0]["hierarchy"] == ("Charter", "Article 1", "General")


def test_normalizes_page_text_and_history() -> None:
    result = normalize_page_sections(
        [{"guid": "s1", "text": " First\r\n\r\n  paragraph  two. ", "history": "  Acts\u00a0 1 "}]
    )
    assert result == (RawSection("s1", "First\n\nparagraph two.", "Acts 1"),)


def test_fallback_fills_missing_article_section_in_toc_order() -> None:
    expected = (
        {"guid": "s1", "number": "1-1", "title": "First", "hierarchy": ("Charter", "Article 1")},
        {"guid": "s2", "number": "1-2", "title": "Second", "hierarchy": ("Charter", "Article 1")},
    )
    page = ({"guid": "s1", "text": "First text.", "history": ""},)
    fallback = ({"guid": "s2", "text": "Second text.", "history": "History note."},)
    result = merge_page_results(expected, page, fallback)
    assert [section.guid for section in result] == ["s1", "s2"]
    assert result[1].history == "History note."


def test_rejects_empty_and_unexpected_sections() -> None:
    expected = ({"guid": "s1", "number": "", "title": "First", "hierarchy": ()},)
    with pytest.raises(ECodeError) as empty:
        merge_page_results(expected, ({"guid": "s1", "text": "", "history": ""},), ())
    assert empty.value.code == "section_extraction_incomplete"

    with pytest.raises(ECodeError) as unexpected:
        merge_page_results(expected, ({"guid": "s2", "text": "Other", "history": ""},), ())
    assert unexpected.value.code == "section_extraction_incomplete"


def test_rejects_duplicate_page_sections() -> None:
    with pytest.raises(ECodeError) as caught:
        normalize_page_sections(
            [
                {"guid": "s1", "text": "First", "history": ""},
                {"guid": "s1", "text": "Again", "history": ""},
            ]
        )
    assert caught.value.code == "section_extraction_incomplete"


def test_fallback_replaces_empty_primary_section() -> None:
    expected = ({"guid": "s1", "number": "1", "title": "Scope", "hierarchy": ()},)
    result = merge_page_results(
        expected,
        (RawSection("s1", "", ""),),
        (RawSection("s1", "Recovered text", ""),),
    )
    assert result[0].text == "Recovered text"


def test_preserves_explicitly_deleted_section_with_empty_text() -> None:
    expected = (
        {"guid": "47392127", "number": "4-12", "title": "Park Commission. (DELETED)", "hierarchy": ("Charter",)},
    )
    result = merge_page_results(expected, (RawSection("47392127", "", ""),), ())
    assert result[0].guid == "47392127"
    assert result[0].text == ""


def test_page_targets_mark_explicitly_deleted_sections_as_empty_allowed() -> None:
    charter = node(
        "chapter",
        "charter",
        "Charter",
        [node("article", "article", "Article IV", [node("section", "47392127", "Park Commission. (DELETED)")])],
    )
    assert page_targets(charter) == (PageTarget("article", ("47392127",), ("47392127",)),)
