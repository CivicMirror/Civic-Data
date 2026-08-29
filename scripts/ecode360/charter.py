from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata
from typing import Iterable, Iterator, Mapping

from .errors import ECodeError
from .models import CharterResult, SectionResult

NODE_TYPES = {"code", "division", "chapter", "article", "part", "subarticle", "section"}
EXACT_LABELS = {
    "charter",
    "the charter",
    "home rule charter",
    "town charter",
    "city charter",
}
COMPOUND_LABELS = {
    "charter and related acts",
    "charter and state acts",
    "special act charter",
}


@dataclass(frozen=True)
class PageTarget:
    guid: str
    section_guids: tuple[str, ...]


@dataclass(frozen=True)
class RawSection:
    guid: str
    text: str
    history: str


@dataclass(frozen=True)
class ExtractionResults:
    primary: tuple[RawSection, ...]
    fallback: tuple[RawSection, ...]


def _clean_text(value: str) -> str:
    value = value.replace("\r\n", "\n").replace("\r", "\n").replace("\u00a0", " ")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in value.split("\n")]
    cleaned: list[str] = []
    blank_count = 0
    for line in lines:
        if line:
            blank_count = 0
            cleaned.append(line)
        elif blank_count < 2:
            blank_count += 1
            cleaned.append("")
    return "\n".join(cleaned).strip()


def normalize_page_sections(raw_sections: object) -> tuple[RawSection, ...]:
    if not isinstance(raw_sections, (list, tuple)):
        raise ECodeError("section_extraction_incomplete", "Page section result is not a list", 6)
    result: list[RawSection] = []
    seen: set[str] = set()
    for raw in raw_sections:
        if isinstance(raw, RawSection):
            guid, text, history = raw.guid, raw.text, raw.history
        elif isinstance(raw, Mapping):
            guid = raw.get("guid")
            text = raw.get("text")
            history = raw.get("history", "")
        else:
            raise ECodeError("section_extraction_incomplete", "Page section result is not an object", 6)
        if not isinstance(guid, str) or not guid.strip() or not isinstance(text, str) or not isinstance(history, str):
            raise ECodeError("section_extraction_incomplete", "Page section result has invalid fields", 6)
        if guid in seen:
            raise ECodeError("section_extraction_incomplete", f"Duplicate section GUID {guid}", 6, ({"guid": guid},))
        seen.add(guid)
        result.append(RawSection(guid, _clean_text(text), _clean_text(history)))
    return tuple(result)


def merge_page_results(
    expected: tuple[dict, ...],
    page_results: object,
    fallback_results: object,
) -> tuple[SectionResult, ...]:
    primary = normalize_page_sections(page_results)
    fallback = normalize_page_sections(fallback_results)
    expected_guids = [str(item["guid"]) for item in expected]
    expected_set = set(expected_guids)
    primary_map = {item.guid: item for item in primary}
    fallback_map = {item.guid: item for item in fallback}
    unexpected = (set(primary_map) | set(fallback_map)) - expected_set
    if unexpected:
        raise ECodeError(
            "section_extraction_incomplete",
            "Extraction returned unexpected section GUIDs",
            6,
            tuple({"guid": guid} for guid in sorted(unexpected)),
        )
    result: list[SectionResult] = []
    missing: list[str] = []
    for item in expected:
        guid = str(item["guid"])
        raw = primary_map.get(guid) or fallback_map.get(guid)
        if raw is None or not raw.text:
            missing.append(guid)
            continue
        hierarchy = tuple(str(value) for value in item.get("hierarchy", ()))
        result.append(
            SectionResult(
                guid=guid,
                number=str(item.get("number", "")),
                title=str(item.get("title", "")),
                hierarchy=hierarchy,
                url=f"https://ecode360.com/{guid}",
                text=raw.text,
                history=raw.history,
            )
        )
    if missing or len(result) != len(expected):
        raise ECodeError(
            "section_extraction_incomplete",
            "Extraction did not contain complete nonempty section text",
            6,
            tuple({"guid": guid} for guid in missing),
        )
    return tuple(result)


def node_title(node: Mapping[str, object]) -> str:
    for key in ("title", "name", "label", "text", "tocName"):
        value = node.get(key)
        if isinstance(value, str) and value.strip():
            return " ".join(value.split())
    return ""


def node_number(node: Mapping[str, object]) -> str:
    for key in ("number", "indexNum", "sectionNum", "index"):
        value = node.get(key)
        if isinstance(value, (str, int, float)) and str(value).strip():
            return str(value).strip()
    return ""


def _children(node: Mapping[str, object]) -> list[dict]:
    children = node.get("children")
    return children if isinstance(children, list) else []


def _walk(node: dict, path: tuple[dict, ...] = ()) -> Iterator[tuple[dict, tuple[dict, ...]]]:
    yield node, path
    for child in _children(node):
        yield from _walk(child, path + (node,))


def _section_count(node: Mapping[str, object]) -> int:
    return sum(1 for candidate, _ in _walk(dict(node)) if candidate.get("type") == "section")


def validate_toc(payload: object, ecode_id: str) -> dict:
    if not isinstance(payload, dict):
        raise ECodeError("toc_invalid", "TOC payload is not an object", 4)
    if payload.get("type") != "code":
        raise ECodeError("toc_invalid", "TOC root is not a code node", 4)
    root_guid = payload.get("guid")
    explicit_code = payload.get("code")
    if not isinstance(root_guid, str) or not root_guid.strip():
        raise ECodeError("toc_invalid", "TOC root has no GUID", 4)
    if root_guid != ecode_id and explicit_code != ecode_id:
        raise ECodeError("toc_invalid", "TOC is for a different eCode360 code", 4)
    if not isinstance(payload.get("tocName"), str) or not payload["tocName"].strip():
        raise ECodeError("toc_invalid", "TOC root has no municipality name", 4)

    seen: set[str] = set()
    sections = 0

    def visit(candidate: object) -> None:
        nonlocal sections
        if not isinstance(candidate, dict):
            raise ECodeError("toc_invalid", "TOC child is not an object", 4)
        guid = candidate.get("guid")
        kind = candidate.get("type")
        if not isinstance(guid, str) or not guid.strip():
            raise ECodeError("toc_invalid", "TOC node has no GUID", 4)
        if guid in seen:
            raise ECodeError("toc_invalid", f"TOC contains duplicate GUID {guid}", 4)
        if kind not in NODE_TYPES:
            raise ECodeError("toc_invalid", f"TOC contains unknown node type {kind!r}", 4)
        if not isinstance(candidate.get("children"), list):
            raise ECodeError("toc_invalid", f"TOC node {guid} has no children list", 4)
        seen.add(guid)
        if kind == "section":
            sections += 1
        for child in candidate["children"]:
            visit(child)

    visit(payload)
    if sections == 0:
        raise ECodeError("toc_invalid", "TOC contains no sections", 4)
    return payload


def _normalized_title(value: str) -> str:
    folded = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    folded = re.sub(r"[^a-z0-9]+", " ", folded.casefold())
    return re.sub(r"\s+", " ", folded).strip()


def _candidate_rank(title: str) -> int:
    normalized = _normalized_title(title)
    if normalized in EXACT_LABELS:
        return 3
    if normalized in COMPOUND_LABELS or "charter and " in normalized or normalized.endswith(" special act charter"):
        return 2
    if normalized == "structure of government":
        return 1
    # eCode360 frequently prefixes a title with "Chapter C" or "Division 1".
    if re.search(r"\bcharter\b", normalized):
        return 3
    return 0


def _candidate_info(node: dict, path: tuple[dict, ...]) -> dict[str, object]:
    return {
        "display_name": node_title(node),
        "url": f"https://ecode360.com/{node['guid']}",
        "guid_path": [str(ancestor.get("guid")) for ancestor in path] + [str(node["guid"])],
    }


def select_charter(toc: dict) -> dict:
    candidates: list[tuple[int, int, int, dict, tuple[dict, ...]]] = []
    for node, path in _walk(toc):
        if node.get("type") not in {"division", "chapter", "part"}:
            continue
        if _section_count(node) == 0:
            continue
        rank = _candidate_rank(node_title(node))
        if rank:
            type_preference = 1 if node.get("type") == "chapter" else 0
            candidates.append((rank, type_preference, len(path), node, path))
    if not candidates:
        raise ECodeError("charter_not_found", "No Charter subtree with sections was found", 5)
    best_score = max((rank, type_preference, depth) for rank, type_preference, depth, _, _ in candidates)
    best = [item for item in candidates if item[:3] == best_score]
    if len(best) > 1:
        raise ECodeError(
            "ambiguous_charter",
            "Multiple Charter subtrees matched",
            5,
            tuple(_candidate_info(node, path) for _, _, _, node, path in best),
        )
    return best[0][3]


def expected_sections(charter: dict) -> tuple[dict, ...]:
    result: list[dict] = []

    def visit(node: dict, hierarchy: tuple[str, ...]) -> None:
        title = node_title(node)
        next_hierarchy = hierarchy + ((title,) if title else ())
        if node.get("type") == "section":
            result.append(
                {
                    "guid": str(node["guid"]),
                    "number": node_number(node),
                    "title": title,
                    "hierarchy": hierarchy,
                }
            )
        for child in _children(node):
            visit(child, next_hierarchy)

    visit(charter, ())
    return tuple(result)


def page_targets(charter: dict) -> tuple[PageTarget, ...]:
    grouped: dict[str, list[str]] = {}
    order: list[str] = []

    def visit(node: dict, nearest_page: str | None) -> None:
        kind = node.get("type")
        page = str(node["guid"]) if kind in {"article", "chapter"} else nearest_page
        if kind == "section":
            if page is None:
                page = str(charter["guid"])
            if page not in grouped:
                grouped[page] = []
                order.append(page)
            grouped[page].append(str(node["guid"]))
            return
        for child in _children(node):
            visit(child, page)

    visit(charter, None)
    return tuple(PageTarget(guid, tuple(grouped[guid])) for guid in order)


def assemble_charter(charter_node: dict, extracted_sections: tuple[SectionResult, ...]) -> CharterResult:
    article_count = sum(1 for node, _ in _walk(charter_node) if node.get("type") == "article")
    guid = str(charter_node["guid"])
    return CharterResult(
        guid=guid,
        title=node_title(charter_node),
        url=f"https://ecode360.com/{guid}",
        article_count=article_count,
        sections=extracted_sections,
    )
