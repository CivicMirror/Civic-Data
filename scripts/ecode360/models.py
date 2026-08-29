from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DirectoryEntry:
    display_name: str
    state: str
    county: str
    ecode_id: str
    code_url: str


@dataclass(frozen=True)
class SectionResult:
    guid: str
    number: str
    title: str
    hierarchy: tuple[str, ...]
    url: str
    text: str
    history: str


@dataclass(frozen=True)
class CharterResult:
    guid: str
    title: str
    url: str
    article_count: int
    sections: tuple[SectionResult, ...]
