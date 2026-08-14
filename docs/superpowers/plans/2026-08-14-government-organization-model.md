# Government Organization Model Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement issue #5 by separating geographic divisions, jurisdiction classifications, and government organizations while preserving stable Civic-Data IDs and external identifiers.

**Architecture:** A geographic division remains the place identified by `ocd-division/...`. A jurisdiction is a governing authority within that division and receives an `ocd-jurisdiction/.../<classification>` ID. Organizations are first-class records with stable `ocd-organization/<uuid>` IDs; CivicPatch, Open States, and other source identifiers are retained in an `identifiers[]` collection. Posts describe positions, memberships connect people to organizations/posts, and roles describe functions.

**Tech Stack:** YAML data, JSON Schema Draft 2020-12, Python 3, `jsonschema`, `referencing`, PyYAML, and the existing `scripts/validate.py` CI workflow.

**Spec:** [Civic-Data issue #5](https://github.com/CivicMirror/Civic-Data/issues/5), supplemented by the approved OCDEP 3 classification proposal and the decisions recorded in this plan.

## Global Constraints

- Treat the current one-state/one-town sample dataset as disposable; rebuild it from scratch under the new model.
- Use `ocd-jurisdiction/.../<classification>` for jurisdiction IDs; do not use a division ID where a jurisdiction ID is required.
- Use `ocd-organization/<uuid>` for Civic-Data’s canonical organization ID; generate once and persist it.
- Store source-system IDs under `identifiers[]`; never silently discard CivicPatch `post_id` or organization-scoped IDs.
- Do not treat internal titles such as Chair, Vice Chair, or Clerk as separately elected posts without an authoritative source proving they are distinct positions.
- Do not import CivicPatch scraper telemetry as legal term dates.
- Do not add backward-compatibility aliases or migration shims for the old schema; data loss is acceptable for this reset.
- CivicPatch compatibility is an explicit acceptance criterion: normalize its division IDs, preserve its source IDs, and map its post labels to formal Civic-Data Posts.
- Keep unrelated working-tree changes, including the existing `docs/GLOSSARY.md` modification and `docs/Example.yaml`, intact.

---

### Task 1: Record the approved data model and controlled vocabularies

**Files:**
- Create: `reference/division-classifications.yaml`
- Create: `reference/jurisdiction-classifications.yaml`
- Test: `scripts/test_reference_data.py`

**Interfaces:**
- Produces the exact classification keys consumed by `jurisdiction.schema.json` and the validator.
- Produces definitions and source links for each vocabulary entry so additions are reviewable.

- [ ] **Step 1: Write failing reference-data tests** that load both YAML files and assert every entry has `id`, `label`, `definition`, and `source`, IDs are unique, and the OCDEP 3 baseline keys are present.
- [ ] **Step 2: Run `python3 -m pytest scripts/test_reference_data.py -v`** and verify it fails because the reference files and loader do not exist.
- [ ] **Step 3: Add the vocabulary files.** Put geographic forms such as `town`, `county`, and `prosecutorial-district` in the division vocabulary. Put `government`, `legislature`, `executive`, `school`, `park`, `sewer`, `forest`, and `transit_authority` in the jurisdiction vocabulary, with OCDEP 3 citations.
- [ ] **Step 4: Implement the minimal YAML loader/test helpers** and rerun the focused tests.
- [ ] **Step 5: Commit** with `git add reference docs/superpowers/specs scripts/test_reference_data.py && git commit -m "docs: define division and jurisdiction vocabularies"`.

### Task 2: Add reusable identifiers and organization schemas

**Files:**
- Create: `schemas/identifier.schema.json`
- Create: `schemas/organization.schema.json`
- Create: `data/us/ma/organizations/municipal/millbury-select-board.yaml`
- Create: `data/us/ma/organizations/municipal/millbury-school-committee.yaml`
- Create: `data/us/ma/organizations/municipal/millbury-planning-board.yaml`
- Test: `scripts/test_organization_schema.py`

**Interfaces:**
- `identifier.schema.json` defines `{scheme, value, source?}` and rejects empty values.
- `organization.schema.json` defines `id`, `name`, `jurisdiction_id`, `identifiers`, `sources`, and optional status/notes.
- Organization IDs match `^ocd-organization/[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`.

- [ ] **Step 1: Write failing schema tests** for valid Millbury organizations, duplicate identifiers within one organization, malformed UUIDs, and a missing jurisdiction reference.
- [ ] **Step 2: Run the focused tests** and verify the new schema/data paths fail validation.
- [ ] **Step 3: Add the identifier and organization schemas** with `additionalProperties: false`, reusable `$ref` to the identifier schema, and clear descriptions distinguishing canonical IDs from external IDs.
- [ ] **Step 4: Add Millbury fixture organizations** using generated UUIDs that are recorded once and never derived from names. Map CivicPatch IDs into `identifiers[]` where available.
- [ ] **Step 5: Extend `scripts/validate.py` collection and reference checks** to load `organizations/`, reject duplicate organization IDs, and require each organization’s `jurisdiction_id` to resolve.
- [ ] **Step 6: Run `python3 scripts/validate.py` and the focused tests**, then commit with `git commit -m "feat: add canonical organization and external identifier schemas"`.

### Task 3: Convert jurisdiction records to division-plus-jurisdiction semantics

**Files:**
- Modify: `schemas/jurisdiction.schema.json`
- Replace: `data/us/ma/jurisdictions/municipal/millbury.yaml`
- Replace: `data/us/ma/jurisdictions/county/worcester-county.yaml`
- Replace: `data/us/ma/jurisdictions/county/da-middle-district.yaml`
- Modify: `scripts/validate.py`
- Test: `scripts/test_jurisdiction_ids.py`

**Interfaces:**
- A jurisdiction record carries a geographic `division_id` and a jurisdiction `id`.
- `jurisdiction.classification` accepts only the jurisdiction vocabulary; geographic forms move to `division.classification`.
- Roles and election linkages resolve against jurisdiction IDs, not division IDs.

- [ ] **Step 1: Write failing tests** asserting Millbury resolves as `ocd-division/country:us/state:ma/place:millbury` plus `ocd-jurisdiction/country:us/state:ma/place:millbury/government`, while `town` remains a division classification.
- [ ] **Step 2: Run the focused tests** and capture the current schema/pattern failures.
- [ ] **Step 3: Update the jurisdiction schema and records**. Do not assign `.../school` merely because a School Committee exists; reserve that classification for an independent school-system jurisdiction.
- [ ] **Step 4: Rebuild the jurisdiction, official, and election fixtures** against the new canonical jurisdiction IDs; do not preserve old division-shaped references or aliases.
- [ ] **Step 5: Remove obsolete records that cannot conform to the new model**, then run validator and focused tests against the fresh dataset.
- [ ] **Step 6: Commit** with `git commit -m "feat: rebuild data with division and jurisdiction classifications"`.

### Task 4: Model Posts, Memberships, and Roles explicitly

**Files:**
- Create: `schemas/post.schema.json`
- Create: `schemas/membership.schema.json`
- Create: `data/us/ma/posts/municipal/millbury-select-board-member.yaml`
- Create: `data/us/ma/memberships/municipal/<person>-millbury-select-board.yaml` for the migrated Millbury members
- Modify: `schemas/official.schema.json`
- Modify: `scripts/validate.py`
- Test: `scripts/test_post_membership_references.py`

**Interfaces:**
- A Post belongs to one organization and represents a position independent of its holder.
- A Membership links `person_id`, `organization_id`, and optionally `post_id`, with `role`, `start`, and `end`.
- A Role is a function/title and is not itself the unique position identifier.

- [ ] **Step 1: Write failing tests** for post-to-organization, membership-to-person/post/organization, date validation, and rejection of an organization mismatch between membership and post.
- [ ] **Step 2: Run the focused tests** and verify references fail before implementation.
- [ ] **Step 3: Add the post and membership schemas** and Millbury fixtures. Represent all five Select Board seats as memberships to the same formal post definition; preserve internal Chair/Vice Chair/Clerk only as source metadata or role notes when supported.
- [ ] **Step 4: Update `official.schema.json` and validator collection/indexes** so person records can link to memberships without duplicating canonical identity data.
- [ ] **Step 5: Run the full validator and focused tests**, then commit with `git commit -m "feat: add posts and memberships"`.

### Task 5: Document the fresh-start model and update all documentation

**Files:**
- Modify: `README.md`
- Modify: `docs/ARCHITECTURE.md`
- Modify: `docs/GLOSSARY.md`
- Modify: `docs/RESOURCES.md`
- Modify: `docs/Example.yaml`
- Create: `docs/FRESH-START-ORGANIZATIONS.md`

**Interfaces:**
- Documentation must use the same ID and relationship names as the schemas.
- Examples must show both canonical IDs and external `identifiers[]`.

- [ ] **Step 1: Write documentation checks** (a grep-based CI check or test) that rejects stale phrases such as “jurisdiction is identified by an OCD Division ID” and verifies required organization terms appear in the glossary/example.
- [ ] **Step 2: Update the glossary** with Division, Jurisdiction, Organization, Post, Membership, Role, canonical ID, and external identifier definitions.
- [ ] **Step 3: Update architecture and README diagrams/tables** to show `division -> jurisdiction -> organization -> post -> membership/person`, and document UUID persistence and external-ID preservation.
- [ ] **Step 4: Write fresh-start guidance** covering removal of the old sample data, organization UUID assignment, CivicPatch `post_id` mapping, and how to add new records under the new schemas. Explicitly document that old IDs are not preserved.
- [ ] **Step 5: Update examples/resources** so no example contradicts the new schemas, then run the documentation checks and validator.
- [ ] **Step 6: Commit** with `git commit -m "docs: document organization model and fresh-start workflow"`.

### Task 6: Integrate CI validation and complete issue #5 verification

**Files:**
- Modify: `scripts/validate.py`
- Modify: `.github/workflows/validate.yml`
- Modify: `scripts/requirements.txt` only if a new test dependency is required
- Test: `scripts/test_organization_model.py`

- [ ] **Step 1: Add integration tests** covering duplicate IDs, unresolved references, invalid classifications, duplicate external identifiers, and a complete Millbury organization/post/membership graph.
- [ ] **Step 2: Run `python3 scripts/validate.py`, `python3 -m pytest`, and `git diff --check`**; fix all errors and keep only explicitly documented cross-validation warnings.
- [ ] **Step 3: Add CivicPatch compatibility tests and fixtures** proving that the county-qualified Millbury `division_ocdid` normalizes to the canonical OCD division, CivicPatch `post_id` values are retained under `identifiers[]`, and labels such as `Council Member`, `Chair`, `Vice Chair`, and `Clerk` map to the formal Select Board Post without creating false elected offices.
- [ ] **Step 4: Verify CI uses the same validator/test commands locally and remotely.** Do not weaken strict reference checks to accommodate legacy data; the rebuilt fixtures and explicit CivicPatch mappings must satisfy the new schemas directly.
- [ ] **Step 5: Review the final diff** for accidental changes to unrelated working-tree files, then commit with `git commit -m "test: enforce organization model and CivicPatch compatibility"`.
- [ ] **Step 6: Publish an issue #5 implementation PR** with a checklist linking the schemas, fresh fixtures, CivicPatch compatibility tests, fresh-start document, documentation updates, and validation output; leave issue #5 open until review confirms the model, then close issue #3 as resolved by the new implementation.

## Verification Checklist

- [ ] Every jurisdiction classification is drawn from `reference/jurisdiction-classifications.yaml`.
- [ ] Division classifications remain separate and are not reused as jurisdiction classifications.
- [ ] Every newly created organization has one immutable canonical `ocd-organization/<uuid>` ID.
- [ ] External IDs are preserved under `identifiers[]` with a source scheme.
- [ ] CivicPatch’s county-qualified Millbury division ID normalizes to the canonical OCD division ID.
- [ ] CivicPatch `post_id` values are retained as external identifiers and do not become Civic-Data canonical IDs.
- [ ] CivicPatch office labels map to formal Civic-Data Posts without treating internal Chair/Vice Chair/Clerk titles as separate elected offices.
- [ ] Every post resolves to one organization, and every membership resolves to a person and organization.
- [ ] Millbury’s Select Board, School Committee, and Planning Board are organizations under the Millbury government jurisdiction; the School Committee is not automatically a `school` jurisdiction.
- [ ] Worcester County’s abolished government is not represented as a current unified body without an explicit historical/status decision.
- [ ] README, Architecture, Glossary, examples, schemas, fresh-start guidance, fixtures, and validator behavior agree.
- [ ] `python3 scripts/validate.py`, the full test suite, and `git diff --check` pass.
