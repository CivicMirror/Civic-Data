"""Lightweight charter-existence check: TOC fetch + charter-subtree detection only.

Skips scripts.ecode360's full section-text extraction (which throttles 2s between
every article/chapter page navigation) -- we only need a yes/no on whether an
eCode360 town has a distinct Charter subtree in its table of contents.
"""
from __future__ import annotations

import json
import sys

from scripts.ecode360.browser import ECodeBrowser
from scripts.ecode360.charter import select_charter, validate_toc
from scripts.ecode360.directory import fetch_directory, normalize_state, parse_directory, resolve_municipality
from scripts.ecode360.errors import ECodeError


def check(municipality: str, state: str) -> dict:
    state_code = normalize_state(state)
    source = resolve_municipality(parse_directory(fetch_directory()), municipality, state_code)
    if source.provider != "ecode360":
        return {"municipality": municipality, "status": "skipped", "reason": f"provider={source.provider}"}
    with ECodeBrowser(headless=True) as browser:
        toc = validate_toc(browser.fetch_toc(source), source.ecode_id)
        try:
            charter_node = select_charter(toc)
        except ECodeError as exc:
            return {"municipality": municipality, "status": "no_charter", "code": exc.code}
        return {
            "municipality": municipality,
            "status": "has_charter",
            "charter_title": charter_node.get("title") or charter_node.get("name"),
            "charter_guid": charter_node.get("guid"),
        }


def main(argv: list[str]) -> int:
    municipality, state = argv[0], argv[1]
    try:
        result = check(municipality, state)
    except ECodeError as exc:
        result = {"municipality": municipality, "status": "error", "code": exc.code, "message": exc.message}
    except Exception as exc:  # noqa: BLE001
        result = {"municipality": municipality, "status": "error", "code": "internal_error", "message": str(exc)}
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
