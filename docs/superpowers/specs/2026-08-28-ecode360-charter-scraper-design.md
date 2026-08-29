# eCode360 Charter Research Tool Design

**Date:** 2026-08-28
**Issue:** [CivicMirror/Civic-Data#19](https://github.com/CivicMirror/Civic-Data/issues/19)

## Purpose

Add a municipality-neutral command-line research tool to Civic-Data that an
LLM can invoke when it needs the current Charter for a municipality. The tool
accepts a municipality and state, resolves the municipality through ICC Code
Solutions' live library, retrieves only the Charter subtree from eCode360,
validates that the extraction is complete, and writes one structured JSON
document to stdout.

The tool is deterministic. It does not invoke an LLM, interpret Charter text,
or write Civic-Data records. The calling LLM decides which provisions are
relevant to its research and may save the authoritative source URLs as record
provenance.

## Scope

The initial implementation will:

- support any U.S. state represented in the ICC library;
- require both a municipality name and a state;
- support ICC entries whose authoritative code URL is hosted by eCode360;
- locate a Charter without a hard-coded municipality registry or eCode ID;
- return the complete selected Charter hierarchy as cleaned plain text;
- operate entirely in memory; and
- use Python and Playwright with Chromium.

It will not:

- scrape an entire municipal code when only its Charter is needed;
- semantically answer a research question or extract elected-office facts;
- cache the ICC directory, TOC, HTML, or Charter text;
- create manifests, monitoring state, or resume state;
- write normalized Civic-Data YAML; or
- silently choose among ambiguous municipality or Charter candidates.

Directory-wide discovery, recurring change monitoring, non-eCode360 code
providers, and semantic Charter search are separate future features.

## Command-line interface

The package will live at `scripts/ecode360/` and be invoked as:

```bash
python -m scripts.ecode360 --municipality "Abington" --state MA
```

The state argument accepts either a two-letter USPS abbreviation or a full
state name and is normalized to the abbreviation. The municipality argument
is required and must resolve to one municipality in that state.

The browser runs headlessly by default. `--headed` is available for diagnosing
Cloudflare challenges or browser behavior. Successful and failed invocations
both emit JSON to stdout. Progress and browser diagnostics go only to stderr.

## Components

The package has five responsibilities with explicit boundaries:

- `directory.py` fetches and parses the live ICC library and resolves a source.
- `browser.py` owns Playwright and Chromium lifecycle, navigation, retries, and
  capture of the live eCode360 TOC response.
- `charter.py` selects the Charter subtree, plans page visits, extracts section
  content, and verifies completeness.
- `output.py` constructs and validates the versioned success or error document.
- `__main__.py` parses CLI arguments, orchestrates the pipeline, writes stdout
  and stderr, and selects the process exit status.

Pure parsing and selection functions will not depend on Playwright. This keeps
source resolution, TOC selection, content normalization, and output validation
testable with small synthetic fixtures.

## Data flow

Each invocation performs a fresh pipeline:

1. Fetch `https://www.icccodesolutions.org/text-library/`.
2. Resolve `(state, municipality)` to one authoritative eCode360 URL and ID.
3. Open that URL in Chromium and capture `/toc/{ecode_id}`.
4. Validate the recursive TOC before using it as the extraction contract.
5. Select one Charter subtree and enumerate its expected section GUIDs.
6. Visit the necessary article or chapter pages and extract their sections.
7. Fetch an individual section page when its parent page did not inline it.
8. Compare the extracted GUID set with the expected live TOC set.
9. Build one JSON response, write it to stdout, and close the browser.

All intermediate objects remain in process memory. The tool does not create
temporary artifacts in the repository or retain retrieved content after exit.

## Municipality resolution

The ICC page's state anchors, municipality entries, counties, and `codeLink`
URLs are the source of truth. The resolver will not derive an eCode ID from a
municipality name.

State matching is exact after conversion of full state names to USPS
abbreviations. Municipality normalization performs Unicode normalization,
case folding, whitespace and punctuation normalization, and removal of one
leading government-form prefix such as `Town of`, `City of`, `Village of`,
`Borough of`, or `Municipality of`. It does not apply approximate matching.

After normalization:

- one match in the requested state proceeds;
- no match fails and reports nearby names as non-authoritative suggestions;
- more than one match fails and reports every candidate; and
- a match whose authoritative URL is not on `ecode360.com` fails with an
  `unsupported_provider` error that includes that URL.

Suggestions help the caller correct input but are never selected automatically.

## TOC capture and validation

Plain HTTP access to eCode360 currently returns `403`, so the tool uses
Playwright navigation and captures the matching live TOC response made by the
site. The response must be JSON with:

- one `code` root;
- a nonempty root GUID and municipality name;
- recursively valid, uniquely identified nodes;
- recognized node types; and
- at least one section.

A challenge page, error object, malformed tree, duplicate GUID, empty tree, or
TOC for a different eCode ID is a fetch failure. The browser retries navigation
with a fresh page and exponential backoff. The initial request plus three
retries are allowed. Navigation has a 30-second timeout, requests for content
pages are separated by at least two seconds, and backoff delays are one, two,
and four seconds. It never substitutes cached data.

## Charter selection

Candidate selection recursively examines nodes that contain section
descendants. Normalized titles receive deterministic ranks:

1. exact Charter labels such as `Charter`, `The Charter`, `Home Rule Charter`,
   `Town Charter`, and `City Charter`;
2. compound labels such as `Charter and Related Acts`, `Charter and State
   Acts`, and `Special Act Charter`; and
3. the fallback label `Structure of Government`.

Nodes without section descendants are rejected regardless of title. For nested
candidates on the same ancestor chain, a `chapter` is preferred over a
`division`, followed by the deeper node, because it is the more specific
content root. If unrelated candidates remain tied at the highest rank, the run
fails with `ambiguous_charter` and reports their GUID paths and URLs.

The selected subtree, not the entire municipal code, defines the extraction
contract.

## Section extraction

The tool recursively enumerates articles, parts, subarticles, and sections
under the selected Charter node while preserving TOC order. Sections are
grouped under their nearest article page. A selected chapter with direct
section children is itself a page target.

For each page target, the extractor:

- navigates to its canonical GUID URL;
- reads section containers identified by eCode360 section GUIDs;
- maps each body back to its TOC node;
- extracts cleaned plain text with paragraph boundaries preserved;
- extracts legislative or history text separately when present; and
- records the section's GUID, number, title, hierarchy, and canonical URL.

If a page does not inline every expected section, each missing section GUID is
retried through its own canonical page. A section is not successful merely
because its container exists: its normalized text must be nonempty.

The final expected and extracted section GUID sets must be exactly equal. A
missing, duplicate, unexpected, or empty section causes the entire invocation
to fail. Partial Charter output is never labeled successful.

Raw HTML is used only during the in-memory extraction and is excluded from the
JSON response to reduce noise and LLM context size.

## Output contract

Success uses a versioned JSON object:

```json
{
  "schema_version": "1.0",
  "status": "success",
  "request": {
    "municipality": "Abington",
    "state": "MA"
  },
  "resolved_source": {
    "display_name": "Town of Abington",
    "state": "MA",
    "county": "Plymouth County",
    "ecode_id": "AB2001",
    "directory_url": "https://www.icccodesolutions.org/text-library/",
    "code_url": "https://ecode360.com/AB2001"
  },
  "retrieved_at": "2026-08-28T00:00:00Z",
  "charter": {
    "guid": "12064945",
    "title": "Charter",
    "url": "https://ecode360.com/12064945",
    "article_count": 8,
    "section_count": 65,
    "sections": [
      {
        "guid": "12345678",
        "number": "1-1",
        "title": "Example provision",
        "hierarchy": ["Charter", "Article 1"],
        "url": "https://ecode360.com/12345678",
        "text": "The municipality is governed under this Charter.",
        "history": ""
      }
    ]
  },
  "warnings": []
}
```

Counts are computed from the selected TOC and verified extraction rather than
copied from known baselines. `retrieved_at` is UTC. Section order follows the
live TOC. The section shown above illustrates the field contract rather than
an actual Abington section. `history` is an empty string when the source has no
separate history text. `warnings` is a list of objects with `code` and
`message` string fields.

Failure uses the same `schema_version`, `status`, `request`, and
`retrieved_at` fields, sets `status` to `error`, and adds:

```json
{
  "error": {
    "code": "ambiguous_charter",
    "message": "Multiple Charter subtrees matched",
    "candidates": []
  }
}
```

The `candidates` field is present only when it can help the caller correct or
disambiguate the request. Each candidate is an object containing the available
`display_name`, `state`, `county`, `url`, and `guid_path` fields; fields that do
not apply to that error are omitted. Error messages must not contain raw
browser dumps or unbounded HTML.

## Exit statuses and failure handling

The process uses stable exit categories:

- `0`: complete success;
- `2`: invalid CLI input;
- `3`: directory fetch, municipality resolution, or unsupported provider;
- `4`: eCode360 navigation, challenge, or TOC failure;
- `5`: missing or ambiguous Charter;
- `6`: incomplete or invalid section extraction; and
- `1`: unexpected internal failure.

Browser operations use bounded timeouts, rate limiting, and retry with a fresh
page. Cleanup runs on success, known failure, interruption, and unexpected
exception. A persistent challenge in headless mode reports a structured error
that suggests rerunning with `--headed`; the tool does not unexpectedly open a
visible browser itself.

## Dependencies and documentation

`scripts/requirements.txt` will add Playwright. Setup documentation will state
both required installation steps:

```bash
pip install -r scripts/requirements.txt
playwright install chromium
```

Documentation will include CLI examples, the JSON and exit-status contracts,
headed troubleshooting, live-test commands, and the data-handling rule: Charter
text is ephemeral research input, while authoritative URLs may be saved as
Civic-Data provenance.

## Testing strategy

Default tests are offline and deterministic. Small synthetic fixtures cover:

- ICC state and municipality parsing;
- full-name and USPS state normalization;
- government-form prefix normalization;
- exact, missing, ambiguous, and unsupported-provider results;
- TOC shape validation and duplicate GUID rejection;
- Charter ranking, nested candidate preference, and unrelated ties;
- article extraction and individual-section fallback;
- empty, duplicate, missing, and unexpected section rejection;
- stable success and error JSON;
- stdout/stderr separation and exit statuses; and
- browser response capture through intercepted fixture responses.

Fixtures will contain invented municipality and Charter text. Live municipal
Charter content will not be committed merely to support tests.

Network-dependent tests are explicitly marked and excluded from normal CI.
Initial live acceptance requires:

1. Abington, Massachusetts resolves dynamically to `AB2001`.
2. Its Charter resolves to GUID `12064945`.
3. The current Issue #19 baseline of 8 articles and 65 sections is reproduced.
4. Every expected section has nonempty text and a canonical URL.
5. The same command succeeds for the other 11 confirmed municipalities in
   Issue #19, producing a transient result matrix with municipality, eCode ID,
   Charter GUID, article count, section count, status, and warnings.
6. No Charter content or result matrix is left in the repository after the
   validation run.
7. The repository's existing test suite and `python3 scripts/validate.py` pass.

The live baseline is an implementation acceptance check, not a permanent
assertion in ordinary CI. Municipal codes can legitimately change; future live
runs establish completeness from the current TOC rather than requiring the
historical 8/65 count forever.

## Repository and review behavior

Implementation changes will remain limited to the new package, its tests,
Python requirements, and focused usage documentation. Existing data files and
unrelated research artifacts are outside scope. Any later workflow that turns
the returned text into Civic-Data records must follow the repository's normal
bot-authored PR, CI validation, provenance, and human-review process.
