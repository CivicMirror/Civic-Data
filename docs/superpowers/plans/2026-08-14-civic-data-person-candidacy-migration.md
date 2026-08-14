# Civic-Data Person and Candidacy Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Migrate Civic-Data from `Official` records and per-contest election linkages to validated `Person`, `Candidacy`, `Election`, and `Contest` records while preserving the tiered Massachusetts dataset.

**Architecture:** Add strict person and election schemas, convert the existing data with a deterministic non-destructive script, and make `scripts/validate.py` the single repository-integrity gate. The active model uses geographic OCD divisions as `jurisdiction_id`; organization/body modeling is tracked separately in issue #5.

**Tech Stack:** Python 3.12+, PyYAML, jsonschema Draft 2020-12, pytest, YAML data, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-08-14-civic-data-person-candidacy-migration-design.md`

## Global Constraints

- No legacy `official.schema.json`, `officials/`, or `official_id` aliases remain active after migration.
- Candidate filing contact data never enters Civic-Data schemas, fixtures, logs, or docs.
- `jurisdiction_id` remains a geographic OCD division; government-body modeling is issue #5.
- External identifiers are reviewed links and must be unique by scheme and identifier.
- Cross-validation warnings remain non-fatal unless `--strict` is supplied.
- The migration script must refuse destination collisions and preserve source files when conversion fails.

### Task 1: Add failing schema and migration tests

**Files:**
- Create: `tests/test_schemas.py`
- Create: `tests/test_migration.py`
- Create: `tests/fixtures/person-candidacy/nc-jordan-lee.yaml`
- Create: `tests/fixtures/person-candidacy/nc-2026-general.yaml`

**Interfaces:**
- Tests consume `scripts/validate.py::load_schemas`, `scripts/migrate_to_person.py::convert_official`, and the fixture documents.
- Tests establish expected Person, Election, reciprocal-reference, privacy, duplicate-identifier, and migration behavior before implementation.

- [ ] **Step 1: Write tests for valid candidate-only and candidate-plus-role records.** Assert `person.schema.json` accepts the NC candidate fixture with `roles: []`, accepts a person with both a role and candidacy, and rejects a person with both arrays empty.
- [ ] **Step 2: Write tests for contest lifecycle and statewide/seat fields.** Assert a scheduled election accepts `winners: null`, a certified contest requires resolved winner IDs, Democratic and Republican primary IDs differ, and a multi-seat contest preserves `seat`.
- [ ] **Step 3: Write tests for privacy and external-identifier rules.** Assert a candidacy containing `filing_address`, `filing_phone`, or `filing_email` fails schema validation; assert duplicate `(scheme, identifier)` values are reported as errors.
- [ ] **Step 4: Write migration tests.** Build a temporary tiered `officials/federal/example.yaml`, run the converter, assert output is under `people/federal/example.yaml`, retains public contact/address data, renames `official_id` references to `person_id`, and refuses to overwrite an existing destination.
- [ ] **Step 5: Run the new tests and verify RED.** Run `pytest -q tests/test_schemas.py tests/test_migration.py`; expected failures are missing `person.schema.json`, missing conversion module, and missing new validator behavior.

### Task 2: Implement the Person schema

**Files:**
- Create: `schemas/person.schema.json`
- Delete: `schemas/official.schema.json`
- Modify: `tests/test_schemas.py`

**Interfaces:**
- Produces the `person.schema.json` Draft 2020-12 schema consumed by the validator.
- Defines `identifiers[]`, `candidacies[]`, nested `roles[].term`, existing public `contact`/`addresses`, verification, and sources.

- [ ] **Step 1: Implement canonical ID, name, identifiers, and provenance properties.** Use the existing OCD person UUID pattern; require unique identifier schemes with `uniqueItems` and per-item `scheme`/`identifier` fields.
- [ ] **Step 2: Implement candidacy properties.** Require `contest_id`, `election_id`, `jurisdiction_id`, `office_id`, `ballot_name`, and `party`; allow only `unknown`, `active`, `withdrawn`, and `disqualified` statuses; reject all filing-contact properties through `additionalProperties: false`.
- [ ] **Step 3: Implement roles using nested `term`.** Preserve `jurisdiction_id`, `office_id`, optional `seat`, and `term.start`, `term.end`, `term.how_seated` exactly as current shipped records use them.
- [ ] **Step 4: Require at least one relationship.** Add an `anyOf` constraint requiring non-empty `candidacies` or non-empty `roles`, while permitting either array to be empty individually.
- [ ] **Step 5: Run schema tests and verify GREEN.** Run `pytest -q tests/test_schemas.py`; all Person schema tests pass while migration/validator tests remain red.

### Task 3: Implement the election and contest schema

**Files:**
- Create: `schemas/election.schema.json`
- Delete: `schemas/election-linkage.schema.json`
- Modify: `tests/test_schemas.py`

**Interfaces:**
- Produces `election.schema.json` for one election document containing `contests[]`.
- Contest winner references use `person_id`; candidate membership uses `candidate_ids`.

- [ ] **Step 1: Define election identity and lifecycle.** Require `id`, `name`, `date`, `election_type`, `status`, `contests`, and `sources`; use scheduled/unofficial/official/certified/corrected statuses.
- [ ] **Step 2: Define contest identity and membership.** Require collision-safe `id`, `jurisdiction_id`, `office_id`, `vote_for`, `candidate_ids`, `result_status`, and `winners`; permit nullable winners only for pending contests and include optional `seat` and `party`.
- [ ] **Step 3: Define winner references.** Require `person_id` and allow certified winner metadata such as `name`, `votes`, and `party`; reject `official_id`.
- [ ] **Step 4: Run schema tests and verify GREEN.** Run `pytest -q tests/test_schemas.py`; all schema tests pass.

### Task 4: Implement deterministic migration tooling

**Files:**
- Create: `scripts/migrate_to_person.py`
- Modify: `tests/test_migration.py`

**Interfaces:**
- `convert_official(document: dict) -> dict` converts one official document to a Person document without inventing data.
- `convert_election_linkage(document: dict) -> dict` converts one linkage to an Election document with one Contest.
- `migrate_tree(source_root: Path, destination_root: Path) -> list[Path]` converts tiered directories, refuses destination collisions, and returns converted paths.

- [ ] **Step 1: Implement `convert_official`.** Copy all public fields, add `candidacies: []`, preserve roles and nested terms, and reject an input containing private filing-contact fields.
- [ ] **Step 2: Implement `convert_election_linkage`.** Derive an election ID from jurisdiction/date/type, create a one-contest election record, map each `official_id` winner reference to `person_id`, and preserve seat/certification/sources.
- [ ] **Step 3: Implement `migrate_tree`.** Walk `officials/**` and `elections/*.yaml`, mirror every tier and town subdirectory under `people/**`, write only into a new destination, and raise a descriptive collision error before any write.
- [ ] **Step 4: Run migration tests and verify GREEN.** Run `pytest -q tests/test_migration.py`; all converter and collision tests pass.

### Task 5: Migrate Massachusetts data and add acceptance fixtures

**Files:**
- Rename: `data/us/ma/officials/` → `data/us/ma/people/`
- Modify: `data/us/ma/elections/*.yaml`
- Create: `tests/fixtures/person-candidacy/nc-2026-democratic-primary.yaml`
- Create: `tests/fixtures/person-candidacy/nc-2026-republican-primary.yaml`
- Create: `tests/fixtures/person-candidacy/nc-2026-certified.yaml`
- Create: `tests/fixtures/person-candidacy/ma-legislative-multi-seat.yaml`

**Interfaces:**
- Repository data is valid under the new schemas and contains no active `officials/` paths or `official_id` keys.
- Fixtures provide candidate-only, primary, scheduled, certified, statewide, and multi-seat examples without private contact data.

- [ ] **Step 1: Run the migration script into a temporary tree.** Compare converted file counts and YAML keys to the source tree; stop if any source record loses a public field.
- [ ] **Step 2: Apply the validated tree conversion.** Preserve 15 Massachusetts people and all tiered directory paths, then convert the two existing election records into election documents with `contests[]`.
- [ ] **Step 3: Add NC and Massachusetts acceptance fixtures.** Include separate primary contest IDs, a statewide NC contest, a certified winner, and two contests sharing one office but carrying distinct seats.
- [ ] **Step 4: Run the schema and migration tests against the migrated data.** Run `pytest -q tests`; expected remaining failures concern validator reference collection only.

### Task 6: Upgrade validator and repository checks

**Files:**
- Modify: `scripts/validate.py`
- Create: `tests/test_validate.py`

**Interfaces:**
- `scripts/validate.py` recognizes `people`, `jurisdictions`, and `elections` directories and loads `person.schema.json`/`election.schema.json`.
- Validator reports duplicate external IDs, unresolved candidacy/contest references, non-reciprocal membership, and privacy errors as exit-code 1 errors.

- [ ] **Step 1: Add validator tests for directory discovery and references.** Assert migrated people are collected, contest candidate IDs resolve, and a missing person or office reference produces an error.
- [ ] **Step 2: Add duplicate and reciprocal-index checks.** Index `(scheme, identifier)` globally; index person candidacies by contest ID; require each contest candidate ID to appear in the matching person candidacy and each candidacy to appear in one election contest.
- [ ] **Step 3: Add lifecycle winner checks.** Require pending contests to have `winners: null`; require certified contests to have at least one winner whose person ID is in `candidate_ids`.
- [ ] **Step 4: Preserve and adapt cross-validation warnings.** Compare `person_id` winners and `roles[].term.how_seated`; keep current warning wording updated from official/officials to person/people.
- [ ] **Step 5: Run validator tests and repository validation.** Run `pytest -q tests/test_validate.py` followed by `python scripts/validate.py`; expected result is schema/reference success with the existing human-review warnings.

### Task 7: Update documentation, CI, and remove legacy references

**Files:**
- Modify: `README.md`
- Modify: `docs/ARCHITECTURE.md`
- Modify: `docs/GLOSSARY.md`
- Modify: `.github/workflows/validate.yml`
- Modify: `scripts/requirements.txt`

**Interfaces:**
- Documentation describes Person, Candidacy, Election, Contest, reviewed PR writes, read-only consumers, privacy boundary, and issue #5 organization follow-up.
- CI runs the complete validator and pytest suite for schema/data/script changes.

- [ ] **Step 1: Replace README entity-model and layout language.** Document `people/`, candidacies, contest lifecycle, and that Civic-Data is not an operational results store.
- [ ] **Step 2: Update architecture and glossary.** Add canonical definitions for person, candidacy, contest, winner, reciprocal references, and geographic jurisdiction; link issue #5 for organizations and `post_id` transforms.
- [ ] **Step 3: Extend CI paths and commands.** Add `pytest` to `scripts/requirements.txt`, include `tests/**` and `docs/**` where relevant, and run `pytest -q` before `python scripts/validate.py`.
- [ ] **Step 4: Search for stale names.** Run `rg -n 'official\.schema|officials/|official_id|Official' --glob '!docs/superpowers/**'`; only historical migration notes may remain, and active code/data must have zero matches.
- [ ] **Step 5: Run full verification.** Run `git diff --check`, `pytest -q`, `python scripts/validate.py`, and the CI-equivalent command sequence.

### Task 8: Commit, publish, and close issue #4

**Files:**
- Modify: no additional files; commit the completed implementation.

- [ ] **Step 1: Review the final diff and status.** Confirm only issue #4 implementation, its spec/plan, and intentional fixture/docs changes are present.
- [ ] **Step 2: Commit the implementation.** Use separate commits for schemas/data, validator/tests, and docs/CI where practical.
- [ ] **Step 3: Push the isolated branch and open a PR targeting the current tiered-directory branch.** The PR must explain that it is stacked on PR #1 or retargeted after PR #1 merges, and must link issues #4 and #5.
- [ ] **Step 4: Re-read issue #4 and post a completion comment.** Include validation commands, test counts, migration notes, and the organization-model follow-up link.
- [ ] **Step 5: Close issue #4 only after the PR is merged and CI is green.** Do not close it merely because the branch or PR exists.
