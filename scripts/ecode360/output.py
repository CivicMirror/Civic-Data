from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Mapping, Sequence

from .errors import ECodeError
from .models import CharterResult, DirectoryEntry

DIRECTORY_URL = "https://www.icccodesolutions.org/text-library/"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _section_dict(section: object) -> dict[str, object]:
    value = asdict(section)
    value["hierarchy"] = list(value["hierarchy"])
    return value


def build_success(
    municipality: str,
    state: str,
    source: DirectoryEntry,
    charter: CharterResult,
    retrieved_at: str,
    warnings: Sequence[Mapping[str, str]] = (),
) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "status": "success",
        "request": {"municipality": municipality, "state": state},
        "resolved_source": {
            "display_name": source.display_name,
            "state": source.state,
            "county": source.county,
            "ecode_id": source.ecode_id,
            "provider": source.provider,
            "directory_url": DIRECTORY_URL,
            "code_url": source.code_url,
        },
        "retrieved_at": retrieved_at,
        "charter": {
            "guid": charter.guid,
            "title": charter.title,
            "url": charter.url,
            "article_count": charter.article_count,
            "section_count": len(charter.sections),
            "sections": [_section_dict(section) for section in charter.sections],
        },
        "warnings": [dict(warning) for warning in warnings],
    }


def build_error(
    municipality: str,
    state: str,
    error: ECodeError,
    retrieved_at: str,
) -> dict[str, object]:
    details: dict[str, object] = {"code": error.code, "message": error.message}
    if error.candidates:
        details["candidates"] = [dict(candidate) for candidate in error.candidates]
    return {
        "schema_version": "1.0",
        "status": "error",
        "request": {"municipality": municipality, "state": state},
        "retrieved_at": retrieved_at,
        "error": details,
    }
