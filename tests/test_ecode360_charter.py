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


def test_accepts_litem_leaf_nodes() -> None:
    # Regression for issue #69: eCode360 sometimes nests a leaf "litem" node
    # (a lettered subsection like "(a) Composition.") under a section --
    # this must not be rejected as an unknown node type.
    section = node("section", "s1", "Purpose")
    section["children"] = [node("litem", "s1a", "Composition.")]
    validate_toc(toc([section]), "EX1000")


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


def test_accepts_prefixed_charter_label() -> None:
    # "<Town> Charter" / "<Town> Home Rule Charter" / eCode360's occasional
    # "Chapter C Charter" baked-in-title format.
    for title in ("Braintree Charter", "Falmouth Home Rule Charter", "Chapter C Charter"):
        candidate = node("chapter", "chapter", title, [node("section", "s1", "Purpose")])
        assert select_charter(validate_toc(toc([candidate]), "EX1000"))["guid"] == "chapter"


def test_rejects_charter_adjacent_titles_that_are_not_the_charter() -> None:
    # Regression for issue #69: a title merely containing the word "charter"
    # (not ending with it) must not be treated as a charter candidate --
    # e.g. Nantucket's "Taxicabs, Charter, Limousine and Tour Vehicles" and
    # Northampton/Stoughton/East Longmeadow's "Charter Review Committee".
    review_committee = node("chapter", "committee", "Charter Review Committee", [node("section", "s1", "Purpose")])
    with pytest.raises(ECodeError) as caught:
        select_charter(validate_toc(toc([review_committee]), "EX1000"))
    assert caught.value.code == "charter_not_found"

    taxicabs = node("chapter", "taxi", "Taxicabs, Charter, Limousine and Tour Vehicles", [node("section", "s1", "Purpose")])
    with pytest.raises(ECodeError) as caught:
        select_charter(validate_toc(toc([taxicabs]), "EX1000"))
    assert caught.value.code == "charter_not_found"


def test_prefers_town_charter_over_sibling_county_charter() -> None:
    # Regression for issue #69: a combined town/county code (e.g. Nantucket)
    # has both a "Town Charter" and a "County Charter" part -- the exact
    # "town charter" label must win outright, not tie into an
    # ambiguous_charter error.
    town = node("part", "town", "Town Charter", [node("section", "s1", "Purpose")])
    county = node("part", "county", "County Charter", [node("section", "s2", "Purpose")])
    wrapper = node("chapter", "wrapper", "Charters", [town, county])
    selected = select_charter(validate_toc(toc([wrapper]), "EX1000"))
    assert selected["guid"] == "town"


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


def test_preserves_explicitly_reserved_section_with_empty_text() -> None:
    # Wakefield, MA's charter (guid 13594366) uses "(Reserved)" rather than
    # "(Deleted)" for placeholder sections with no content -- ecode360.com
    # itself renders these with a genuinely empty content div, not a
    # loading/timing issue, so they must not be treated as fetch failures.
    expected = (
        {
            "guid": "13594366",
            "number": "5-9",
            "title": "Sec. 5-9: through Sec. 5-10. (Reserved)",
            "hierarchy": ("Charter",),
        },
    )
    result = merge_page_results(expected, (RawSection("13594366", "", ""),), ())
    assert result[0].guid == "13594366"
    assert result[0].text == ""


def test_page_targets_mark_explicitly_reserved_sections_as_empty_allowed() -> None:
    charter = node(
        "chapter",
        "charter",
        "Charter",
        [node("article", "article", "Part V", [node("section", "13594366", "Sec. 5-9: through Sec. 5-10. (Reserved)")])],
    )
    assert page_targets(charter) == (PageTarget("article", ("13594366",), ("13594366",)),)


def test_preserves_reserve_for_future_use_section_with_empty_text() -> None:
    # Regression for issue #69: Greenfield, MA's charter (guid 49697236)
    # titles a placeholder section "Reserve section for future use." rather
    # than using a "(Reserved)" suffix -- ecode360.com renders it with a
    # genuinely empty content div, same as the parenthesized form, and it
    # must not be treated as an incomplete/failed scrape.
    expected = (
        {
            "guid": "49697236",
            "number": "SECTION 6-6",
            "title": "Reserve section for future use.",
            "hierarchy": ("Charter", "Administrative Organization"),
        },
    )
    result = merge_page_results(expected, (RawSection("49697236", "", ""),), ())
    assert result[0].guid == "49697236"
    assert result[0].text == ""


def test_preserves_unparenthesized_repealed_title_variants() -> None:
    # Regression for issue #69: Springfield ("Repealed, 1961, 146, Sec. 2"),
    # Wellfleet ("Action on Proposed Budget - Repealed 4/30/13" and "Deleted
    # content moved to 7-5-3 <4-29-2019>") mark a repealed/deleted section
    # in the title using free text rather than a parenthesized or "reserve
    # ... for future use" convention.
    for guid, title in (
        ("14659290", "Repealed, 1961, 146, Sec. 2"),
        ("38070325", "Action on Proposed Budget - Repealed 4/30/13"),
        ("38070338", "Deleted content moved to 7-5-3 <4-29-2019>"),
    ):
        expected = ({"guid": guid, "number": "1", "title": title, "hierarchy": ("Charter",)},)
        result = merge_page_results(expected, (RawSection(guid, "", ""),), ())
        assert result[0].text == ""


def test_preserves_repealed_section_signaled_only_by_history() -> None:
    # Regression for issue #69: Mansfield's "Municipal Electric Department
    # Director." and North Andover's "Limit on spending" give no hint in
    # their own title that the section is empty -- only the fetched
    # history note ("[Repealed by Chapter 147 of the Acts of 2010, approved
    # 7-1-2010]") does, which is only known after fetching, unlike
    # is_explicitly_empty()'s title-based check.
    expected = (
        {"guid": "28866367", "number": "7-2", "title": "Municipal Electric Department Director.", "hierarchy": ("Charter",)},
    )
    result = merge_page_results(
        expected,
        (RawSection("28866367", "", "[Repealed 2006]"),),
        (),
    )
    assert result[0].guid == "28866367"
    assert result[0].text == ""
