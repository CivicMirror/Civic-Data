from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from .browser import ECodeBrowser
from .charter import (
    assemble_charter,
    expected_sections,
    merge_page_results,
    page_targets,
    select_charter,
    validate_toc,
)
from .directory import fetch_directory, normalize_state, parse_directory, resolve_municipality
from .errors import ECodeError
from .output import build_error, build_success, utc_now


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ECodeError("invalid_cli_input", message, 2)


def create_parser() -> argparse.ArgumentParser:
    parser = _ArgumentParser(prog="python -m scripts.ecode360")
    parser.add_argument("--municipality")
    parser.add_argument("--state")
    parser.add_argument("--headed", action="store_true", help="show the Chromium window")
    return parser


def execute(municipality: str, state: str, headed: bool = False) -> dict[str, object]:
    state_code = normalize_state(state)
    source = resolve_municipality(parse_directory(fetch_directory()), municipality, state_code)
    with ECodeBrowser(headless=not headed) as browser:
        toc = validate_toc(browser.fetch_toc(source), source.ecode_id)
        charter_node = select_charter(toc)
        expected = expected_sections(charter_node)
        extraction = browser.extract_sections(page_targets(charter_node))
        sections = merge_page_results(expected, extraction.primary, extraction.fallback)
        charter = assemble_charter(charter_node, sections)
    return build_success(municipality, state_code, source, charter, utc_now())


def main(argv: Sequence[str] | None = None) -> int:
    municipality = ""
    state = ""
    retrieved_at = utc_now()
    try:
        args = create_parser().parse_args(argv)
        municipality = (args.municipality or "").strip()
        state = (args.state or "").strip()
        if not municipality or not state:
            raise ECodeError("invalid_cli_input", "--municipality and --state are required", 2)
        print(f"Resolving {municipality}, {state}", file=sys.stderr)
        document = execute(municipality, state, headed=args.headed)
        print(json.dumps(document, ensure_ascii=False, indent=2))
        return 0
    except ECodeError as exc:
        print(json.dumps(build_error(municipality, state, exc, retrieved_at), ensure_ascii=False, indent=2))
        return exc.exit_status
    except Exception as exc:
        print(f"Unexpected internal error: {type(exc).__name__}: {exc}", file=sys.stderr)
        error = ECodeError("internal_error", "Unexpected internal error", 1)
        print(json.dumps(build_error(municipality, state, error, retrieved_at), ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
