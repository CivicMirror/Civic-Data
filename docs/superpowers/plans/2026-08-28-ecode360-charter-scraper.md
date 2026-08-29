# eCode360 Charter Research Tool Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic Python CLI that resolves a municipality and state through the live ICC library, retrieves its complete eCode360 Charter, validates completeness, and emits ephemeral structured JSON.

**Architecture:** A `scripts.ecode360` package separates directory resolution, TOC/Charter logic, Playwright browser operations, output contracts, and CLI orchestration. Pure functions handle parsing, normalization, selection, and validation so ordinary tests remain offline; explicitly marked live tests exercise the current ICC/eCode360 sites.

**Tech Stack:** Python 3.12+, standard-library `html.parser`, Playwright for Python with Chromium, pytest

**Spec:** `docs/superpowers/specs/2026-08-28-ecode360-charter-scraper-design.md`

## Global Constraints

- Require both `--municipality` and `--state`; accept USPS abbreviations and full state names.
- Resolve eCode IDs from the current ICC library and never derive them from names.
- Support only authoritative URLs on `ecode360.com`; report other providers without following them.
- Run headlessly unless the caller explicitly passes `--headed`.
- Keep directory HTML, TOC JSON, page HTML, and Charter text in memory only.
- Emit exactly one JSON document to stdout; write diagnostics only to stderr.
- Return a nonzero stable exit status for every incomplete, ambiguous, challenged, or malformed result.
- Exclude raw HTML from output and never commit live Charter text as a test fixture.
- Use an initial browser request plus at most three retries, 30-second navigation timeouts, one/two/four-second retry backoff, and at least two seconds between content page requests.
- Preserve unrelated `data/us/nc/NC-research.md` and `reference/` working-tree content.

---

### Task 1: Domain Types, Errors, and Versioned Output

**Files:**
- Create: `scripts/ecode360/__init__.py`
- Create: `scripts/ecode360/models.py`
- Create: `scripts/ecode360/errors.py`
- Create: `scripts/ecode360/output.py`
- Test: `tests/test_ecode360_output.py`

**Interfaces:**
- Consumes: no earlier task interfaces.
- Produces: `DirectoryEntry`, `SectionResult`, and `CharterResult` frozen dataclasses; `ECodeError`; `utc_now()`; `build_success()`; and `build_error()`.

- [ ] **Step 1: Write failing output-contract tests**

Create `tests/test_ecode360_output.py` with fixed dataclass instances and assertions that success includes schema version `1.0`, normalized source metadata, ordered sections, and empty history/warnings. Add an error assertion that candidates are omitted when absent and preserved when present.

```python
from scripts.ecode360.errors import ECodeError
from scripts.ecode360.models import CharterResult, DirectoryEntry, SectionResult
from scripts.ecode360.output import build_error, build_success


def test_build_success_preserves_ordered_charter_contract() -> None:
    source = DirectoryEntry("Town of Example", "EX", "Sample County", "EX1000", "https://ecode360.com/EX1000")
    sections = (
        SectionResult("2001", "1-1", "Purpose", ("Charter", "Article 1"), "https://ecode360.com/2001", "Purpose text.", ""),
    )
    charter = CharterResult("2000", "Charter", "https://ecode360.com/2000", 1, sections)
    result = build_success("Example", "EX", source, charter, "2026-08-28T00:00:00Z")
    assert result["schema_version"] == "1.0"
    assert result["status"] == "success"
    assert result["charter"]["section_count"] == 1
    assert result["charter"]["sections"][0]["history"] == ""


def test_build_error_uses_structured_error_contract() -> None:
    error = ECodeError("municipality_not_found", "No municipality matched", 3)
    result = build_error("Missing", "EX", error, "2026-08-28T00:00:00Z")
    assert result["status"] == "error"
    assert result["error"] == {"code": "municipality_not_found", "message": "No municipality matched"}
```

- [ ] **Step 2: Run the tests and confirm the package is missing**

Run: `python -m pytest tests/test_ecode360_output.py -q`

Expected: collection fails with `ModuleNotFoundError: No module named 'scripts.ecode360'`.

- [ ] **Step 3: Implement the domain and output types**

Use frozen dataclasses and tuples so downstream code cannot accidentally mutate an already validated result.

```python
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
```

Implement `ECodeError(Exception)` with `code`, `message`, `exit_status`, and optional tuple-of-dict `candidates`. Implement output builders using `dataclasses.asdict`, explicitly converting `hierarchy` tuples to JSON arrays and adding `section_count = len(sections)`.

- [ ] **Step 4: Run output tests**

Run: `python -m pytest tests/test_ecode360_output.py -q`

Expected: all tests pass.

- [ ] **Step 5: Commit Task 1**

```bash
git add scripts/ecode360/__init__.py scripts/ecode360/models.py scripts/ecode360/errors.py scripts/ecode360/output.py tests/test_ecode360_output.py
git commit -m "feat: define eCode360 tool output contract"
```

### Task 2: Live ICC Directory Parsing and Conservative Resolution

**Files:**
- Create: `scripts/ecode360/directory.py`
- Test: `tests/test_ecode360_directory.py`

**Interfaces:**
- Consumes: `DirectoryEntry` and `ECodeError` from Task 1.
- Produces: `normalize_state(value: str) -> str`, `normalize_municipality(value: str) -> str`, `parse_directory(html: str) -> tuple[DirectoryEntry, ...]`, `resolve_municipality(entries, municipality, state) -> DirectoryEntry`, and `fetch_directory(timeout_seconds: float = 30.0) -> str`.

- [ ] **Step 1: Write failing parser and resolver tests**

Build a short invented HTML fixture containing state anchors, eCode links, counties, a duplicate normalized municipality, and one non-eCode provider. Cover full state names, government-form prefixes, punctuation, missing matches with suggestions, ambiguity, and unsupported providers.

```python
DIRECTORY_HTML = """
<a id="EX" class="stateAnchor"></a>
<div class="listItem"><div class="codeTitle"><a class="codeLink" href="https://ecode360.com/EX1000">Town of Example</a></div><div class="codeCounty">(Sample County)</div></div>
<div class="listItem"><div class="codeTitle"><a class="codeLink" href="https://example.municipal.codes/">City of Elsewhere</a></div><div class="codeCounty">(Other County)</div></div>
"""


def test_resolves_full_state_name_and_bare_municipality() -> None:
    entries = parse_directory(DIRECTORY_HTML)
    result = resolve_municipality(entries, "Example", "Example State")
    assert result.ecode_id == "EX1000"
```

Use `monkeypatch` for a synthetic state-name mapping entry where needed; production code contains the complete 50-state plus DC mapping.

- [ ] **Step 2: Run directory tests and verify failure**

Run: `python -m pytest tests/test_ecode360_directory.py -q`

Expected: import fails because `scripts.ecode360.directory` does not exist.

- [ ] **Step 3: Implement state and municipality normalization**

Normalize municipality input with NFKD ASCII folding, case folding, removal of one anchored government prefix, replacement of non-alphanumeric runs with one space, and whitespace collapse. Validate state codes against a constant complete mapping rather than accepting arbitrary two-letter strings.

```python
PREFIX_RE = re.compile(r"^(?:town|city|village|borough|municipality)\s+of\s+", re.I)


def normalize_municipality(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    without_prefix = PREFIX_RE.sub("", ascii_value.strip())
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", without_prefix.casefold())).strip()
```

- [ ] **Step 4: Implement the ICC HTML parser and fetcher**

Subclass `html.parser.HTMLParser`. Track the current two-letter state from `a.stateAnchor[id]`, begin an entry at `div.listItem`, capture the `a.codeLink` URL/text and `div.codeCounty` text, and emit on the closing list item. For non-eCode URLs, retain the entry with an empty `ecode_id`; resolution must report `unsupported_provider` with its source URL.

Fetch the library with `urllib.request.urlopen` using a descriptive Civic-Data user agent, a 30-second timeout, UTF-8 decoding with response charset support, and `directory_fetch_failed` wrapping for network or decode failures.

- [ ] **Step 5: Implement exact resolution and suggestions**

Filter by normalized state first, then exact normalized municipality. Use `difflib.get_close_matches` only to populate error candidates. Return `municipality_not_found`, `ambiguous_municipality`, or `unsupported_provider` with exit status `3`; never use a suggestion as the result.

- [ ] **Step 6: Run directory and output tests**

Run: `python -m pytest tests/test_ecode360_directory.py tests/test_ecode360_output.py -q`

Expected: all tests pass.

- [ ] **Step 7: Commit Task 2**

```bash
git add scripts/ecode360/directory.py tests/test_ecode360_directory.py
git commit -m "feat: resolve municipalities from ICC library"
```

### Task 3: TOC Validation, Charter Selection, and Page Planning

**Files:**
- Create: `scripts/ecode360/charter.py`
- Test: `tests/test_ecode360_charter.py`

**Interfaces:**
- Consumes: `ECodeError`, `CharterResult`, and `SectionResult`.
- Produces: `validate_toc(payload: object, ecode_id: str) -> dict`, `select_charter(toc: dict) -> dict`, `expected_sections(charter: dict) -> tuple[dict, ...]`, `page_targets(charter: dict) -> tuple[PageTarget, ...]`, and `assemble_charter(charter_node, extracted_sections) -> CharterResult`.

- [ ] **Step 1: Write failing recursive TOC tests**

Create invented trees that cover valid node types, duplicate GUIDs, no sections, a wrong root, nested division/chapter Charter labels, compound labels, fallback labels, and two unrelated equal candidates.

```python
def node(kind: str, guid: str, title: str, children: list[dict] | None = None) -> dict:
    return {"type": kind, "guid": guid, "title": title, "children": children or []}


def test_prefers_nested_charter_chapter_over_division() -> None:
    chapter = node("chapter", "chapter", "Charter", [node("section", "s1", "Purpose")])
    division = node("division", "division", "The Charter", [chapter])
    toc = {"type": "code", "guid": "EX1000", "tocName": "Example", "children": [division]}
    assert select_charter(validate_toc(toc, "EX1000"))["guid"] == "chapter"
```

Add page-planning tests for an article with nested parts and for a chapter with direct section children.

- [ ] **Step 2: Run Charter tests and verify failure**

Run: `python -m pytest tests/test_ecode360_charter.py -q`

Expected: import fails because `scripts.ecode360.charter` does not exist.

- [ ] **Step 3: Implement strict TOC validation**

Recognize only `code`, `division`, `chapter`, `article`, `part`, `subarticle`, and `section`. Require nonempty string `guid`, list `children`, one `code` root, nonempty root `tocName`, no repeated GUID, and at least one section. Accept both `title` and eCode's display fields through one `node_title()` helper, but retain the original node dictionaries.

Raise `toc_invalid` with exit status `4` for every contract violation and require the root GUID or explicit code field to match the requested eCode ID.

- [ ] **Step 4: Implement deterministic candidate ranking**

Return no candidate unless it has section descendants. Rank exact labels above compound labels above `structure of government`; among nested candidates prefer `chapter`, then greater depth. Collapse nested candidates to the best node on that chain. If multiple unrelated top-ranked candidates remain, raise `ambiguous_charter` with exit status `5` and candidate `url`/`guid_path`; if none remain, raise `charter_not_found`.

- [ ] **Step 5: Implement expected section and page-target planning**

Define a frozen `PageTarget(guid: str, section_guids: tuple[str, ...])`. Preserve depth-first TOC order. Each section belongs to its nearest `article`; sections without an article ancestor belong to the selected chapter. Do not create targets for parts or subarticles because their nearest article or chapter page owns the fallback contract.

- [ ] **Step 6: Run Charter tests**

Run: `python -m pytest tests/test_ecode360_charter.py -q`

Expected: all tests pass.

- [ ] **Step 7: Commit Task 3**

```bash
git add scripts/ecode360/charter.py tests/test_ecode360_charter.py
git commit -m "feat: select and plan eCode360 Charter extraction"
```

### Task 4: Section Normalization and Completeness Enforcement

**Files:**
- Modify: `scripts/ecode360/charter.py`
- Modify: `tests/test_ecode360_charter.py`

**Interfaces:**
- Consumes: validated Charter nodes, ordered expected section nodes, and raw dictionaries returned from browser DOM evaluation.
- Produces: `normalize_page_sections(raw_sections: object) -> tuple[RawSection, ...]`, frozen `ExtractionResults(primary: tuple[RawSection, ...], fallback: tuple[RawSection, ...])`, `merge_page_results(expected, page_results, fallback_results) -> tuple[SectionResult, ...]`, and the completed `assemble_charter()`.

- [ ] **Step 1: Add failing normalization and completeness tests**

Test paragraph whitespace normalization, history separation, TOC metadata taking precedence over DOM titles, fallback filling a missing section, and rejection of empty, duplicate, missing, and unexpected GUIDs.

```python
def test_fallback_fills_missing_article_section_in_toc_order() -> None:
    expected = (
        {"guid": "s1", "number": "1-1", "title": "First", "hierarchy": ("Charter", "Article 1")},
        {"guid": "s2", "number": "1-2", "title": "Second", "hierarchy": ("Charter", "Article 1")},
    )
    page = ({"guid": "s1", "text": "First text.", "history": ""},)
    fallback = ({"guid": "s2", "text": "Second text.", "history": "History note."},)
    result = merge_page_results(expected, page, fallback)
    assert [section.guid for section in result] == ["s1", "s2"]
```

- [ ] **Step 2: Run the new tests and verify they fail**

Run: `python -m pytest tests/test_ecode360_charter.py -q`

Expected: failures report missing normalization and merge functions.

- [ ] **Step 3: Implement raw DOM result validation**

Define frozen `RawSection(guid: str, text: str, history: str)` and `ExtractionResults(primary: tuple[RawSection, ...], fallback: tuple[RawSection, ...])`. Reject non-list page results, non-object entries, blank GUIDs, duplicate GUIDs within a page, and non-string text/history. Normalize CRLF, nonbreaking spaces, spaces around newlines, runs of horizontal whitespace, and more than two blank lines while preserving paragraph boundaries.

- [ ] **Step 4: Implement exact set reconciliation**

Merge article-page results first and individual-section fallback results second. A fallback may replace a missing section but may not overwrite a nonempty article result. Reject unexpected GUIDs immediately. After merging, require every expected GUID exactly once with nonempty normalized text. Raise `section_extraction_incomplete` with exit status `6` and candidates that identify missing, empty, duplicate, or unexpected GUIDs.

- [ ] **Step 5: Assemble ordered output from TOC metadata**

Build `SectionResult` objects in expected TOC order using TOC number/title/hierarchy and canonical `https://ecode360.com/{guid}` URLs. Count `article` descendants for `article_count`, compute section count from the final tuple, and use an empty history string when absent.

- [ ] **Step 6: Run all pure eCode360 tests**

Run: `python -m pytest tests/test_ecode360_output.py tests/test_ecode360_directory.py tests/test_ecode360_charter.py -q`

Expected: all tests pass.

- [ ] **Step 7: Commit Task 4**

```bash
git add scripts/ecode360/charter.py tests/test_ecode360_charter.py
git commit -m "feat: validate complete Charter section extraction"
```

### Task 5: Playwright Browser Client

**Files:**
- Create: `scripts/ecode360/browser.py`
- Create: `tests/test_ecode360_browser.py`
- Modify: `scripts/requirements.txt`

**Interfaces:**
- Consumes: `DirectoryEntry`, `PageTarget`, `validate_toc()`, and `normalize_page_sections()`.
- Produces: context-managed `ECodeBrowser(headless: bool = True)`, `fetch_toc(source: DirectoryEntry) -> dict`, and `extract_sections(targets: tuple[PageTarget, ...]) -> ExtractionResults`.

- [ ] **Step 1: Add Playwright dependency and failing browser unit tests**

Add `playwright>=1.48,<2` to `scripts/requirements.txt`. Test retry and response-selection logic using fake Playwright page/context objects; no test may launch a real browser by default. Assert that only `/toc/{ecode_id}` is accepted and that retries close failed pages.

```python
def test_toc_response_match_is_exact() -> None:
    assert is_toc_response("https://ecode360.com/toc/EX1000", "EX1000")
    assert not is_toc_response("https://ecode360.com/toc/EX10001", "EX1000")
    assert not is_toc_response("https://other.example/toc/EX1000", "EX1000")
```

- [ ] **Step 2: Install Python package dependency and run browser tests**

Run: `python -m pip install -r scripts/requirements.txt`

Run: `python -m pytest tests/test_ecode360_browser.py -q`

Expected: tests fail because the browser module is absent.

- [ ] **Step 3: Implement browser lifecycle and bounded retry**

Use `playwright.sync_api.sync_playwright`. Launch Chromium only in `__enter__`, set a current desktop Chrome user agent and `locale="en-US"`, create a fresh context/page on retry, apply a 30,000 ms default timeout, and close page/context/browser/Playwright in `__exit__` even after exceptions.

Implement four total attempts with one/two/four-second delays. Convert Playwright timeouts, closed-page failures, HTTP errors, response JSON errors, and visible challenge markers into `ecode_navigation_failed` or `toc_invalid` with exit status `4`.

- [ ] **Step 4: Implement live TOC interception**

Register response waiting before navigating to `source.code_url`. Accept only HTTPS responses on host `ecode360.com` whose path is exactly `/toc/{source.ecode_id}`. Parse JSON, pass it through `validate_toc`, and reject 4xx/5xx responses and HTML challenge bodies.

- [ ] **Step 5: Implement DOM extraction and section fallback**

For each target GUID, navigate to `https://ecode360.com/{guid}`, then evaluate JavaScript that returns JSON-safe objects from `.section_content.content` containers. Derive a GUID from the container ID after removing `_content`; collect cleaned visible text and separate history text from history/legislative child selectors before removing that text from the body copy.

If an article page omits expected GUIDs, visit each missing GUID individually and evaluate the same extraction function. Enforce at least two seconds between page navigations. Return article/chapter results in `ExtractionResults.primary` and individual-section results in `ExtractionResults.fallback`; do not persist page HTML.

- [ ] **Step 6: Run browser and pure tests**

Run: `python -m pytest tests/test_ecode360_browser.py tests/test_ecode360_charter.py tests/test_ecode360_directory.py tests/test_ecode360_output.py -q`

Expected: all tests pass without launching Chromium.

- [ ] **Step 7: Commit Task 5**

```bash
git add scripts/ecode360/browser.py tests/test_ecode360_browser.py scripts/requirements.txt
git commit -m "feat: retrieve eCode360 content with Playwright"
```

### Task 6: CLI Orchestration and Machine-Readable Failures

**Files:**
- Create: `scripts/ecode360/__main__.py`
- Create: `tests/test_ecode360_cli.py`

**Interfaces:**
- Consumes: all public interfaces from Tasks 1 through 5.
- Produces: `create_parser() -> argparse.ArgumentParser`, `execute(municipality, state, headed=False) -> dict`, and `main(argv: Sequence[str] | None = None) -> int`.

- [ ] **Step 1: Write failing CLI tests with dependency substitution**

Monkeypatch `fetch_directory`, `resolve_municipality`, and `ECodeBrowser` so CLI tests never use network or Chromium. Cover success, known `ECodeError`, invalid CLI input, unexpected exceptions, headed propagation, one stdout JSON document, and diagnostics only on stderr.

```python
def test_main_emits_one_success_document(monkeypatch, capsys) -> None:
    install_success_fakes(monkeypatch)
    assert main(["--municipality", "Example", "--state", "EX"]) == 0
    captured = capsys.readouterr()
    assert json.loads(captured.out)["status"] == "success"
    assert "Resolving Example, EX" in captured.err
```

- [ ] **Step 2: Run CLI tests and verify failure**

Run: `python -m pytest tests/test_ecode360_cli.py -q`

Expected: import fails because `scripts.ecode360.__main__` does not exist.

- [ ] **Step 3: Implement parser and orchestration**

Use a custom `ArgumentParser` that raises `ECodeError("invalid_cli_input", message, 2)` rather than printing non-JSON usage to stdout. `execute()` fetches and parses the directory, resolves one source, opens `ECodeBrowser(headless=not headed)`, captures/selects the TOC, plans targets, calls `extract_sections()`, passes its `primary` and `fallback` tuples to `merge_page_results()`, assembles the Charter, and builds success output with one shared UTC timestamp.

- [ ] **Step 4: Implement exception-to-output boundary**

`main()` prints progress lines to stderr, catches `ECodeError` and prints `build_error()` to stdout with its stable status, catches unexpected exceptions into `internal_error` status `1` without traceback or HTML on stdout, and returns the selected integer. Serialize with `json.dumps(..., ensure_ascii=False, indent=2)` and one trailing newline.

- [ ] **Step 5: Run CLI and all offline tests**

Run: `python -m pytest -m "not live" -q`

Expected: all tests pass.

- [ ] **Step 6: Commit Task 6**

```bash
git add scripts/ecode360/__main__.py tests/test_ecode360_cli.py
git commit -m "feat: add eCode360 Charter research CLI"
```

### Task 7: Documentation, Live Acceptance, and Repository Verification

**Files:**
- Modify: `README.md`
- Create: `pytest.ini`
- Create: `tests/test_ecode360_live.py`

**Interfaces:**
- Consumes: the completed `python -m scripts.ecode360` CLI.
- Produces: documented setup/usage and an opt-in `live` pytest marker.

- [ ] **Step 1: Write the opt-in live test**

Register `live` in `pytest.ini` and set default `addopts = -m "not live"`. Create a test that invokes the public Python interfaces for Abington, asserts `AB2001`, Charter GUID `12064945`, 8 articles, 65 sections, nonempty text, and canonical URLs. Do not write returned JSON to disk.

```python
@pytest.mark.live
def test_abington_current_charter_baseline() -> None:
    result = execute("Abington", "MA")
    assert result["resolved_source"]["ecode_id"] == "AB2001"
    assert result["charter"]["guid"] == "12064945"
    assert result["charter"]["article_count"] == 8
    assert result["charter"]["section_count"] == 65
    assert all(item["text"].strip() and item["url"].startswith("https://ecode360.com/") for item in result["charter"]["sections"])
```

- [ ] **Step 2: Document setup and usage**

Add a focused README section containing:

```bash
pip install -r scripts/requirements.txt
playwright install chromium
python -m scripts.ecode360 --municipality "Abington" --state MA
python -m scripts.ecode360 --municipality "Abington" --state Massachusetts --headed
python -m pytest -m live tests/test_ecode360_live.py -q
```

Explain stdout/stderr, stable error statuses, ephemeral data handling, unsupported providers, and that only authoritative URLs should be copied into Civic-Data provenance.

- [ ] **Step 3: Run offline tests and repository validation**

Run: `python -m pytest -m "not live" -q`

Run: `python3 scripts/validate.py`

Run: `git diff --check`

Expected: tests and validation exit `0`; diff check emits no output.

- [ ] **Step 4: Install Chromium and run Abington live acceptance**

Run: `playwright install chromium`

Run: `python -m pytest -m live tests/test_ecode360_live.py -q -s`

Expected: Abington resolves to `AB2001`, selects `12064945`, and returns 8 articles and 65 complete sections. If the current live TOC has legitimately changed, inspect the returned current GUID/counts and update the acceptance evidence rather than weakening completeness validation.

- [ ] **Step 5: Run the other 11 Issue #19 municipalities transiently**

Invoke the CLI in a shell loop for Adams MA, Barnstable MA, Blackstone MA, Chatham MA, Dartmouth MA, Easton MA, Norwell MA, Townsend MA, Watertown MA, Webster MA, and Winchendon MA. Parse each stdout document in memory and print only municipality, eCode ID, Charter GUID, article count, section count, status, and warnings. Do not redirect Charter JSON into repository files.

Expected: every municipality returns complete success or an explicit actionable error; no partial extraction reports success.

- [ ] **Step 6: Commit Task 7**

```bash
git add README.md pytest.ini tests/test_ecode360_live.py
git commit -m "docs: document eCode360 Charter research tool"
```

- [ ] **Step 7: Final verification evidence**

Run: `python -m pytest -m "not live" -q`

Run: `python3 scripts/validate.py`

Run: `git diff --check`

Run: `git status --short`

Expected: all offline tests pass, repository validation exits `0`, diff check is clean, and status lists only the user's pre-existing unrelated untracked paths.
