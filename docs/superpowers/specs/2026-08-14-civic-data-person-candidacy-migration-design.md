# Civic-Data Person and Candidacy Migration Design

## Status

Approved scope for implementation of Civic-Data issue #4. The government-body
model is explicitly deferred to issue #5.

## Goal

Replace the officeholder-only `Official` model with a shared `Person` model
that can represent officeholders, candidates, or both, while retaining a
small, reviewable election and contest index for CivicMirror and CivicPatch.

## Scope and boundaries

The migration covers the existing Massachusetts dataset and reusable schemas,
validator, fixtures, documentation, and migration tooling. It does not create
an operational results store, import precinct rows, resolve identities
automatically, or introduce a government-body/organization entity.

`jurisdiction_id` continues to mean an OCD geographic division in this
release. Organization-scoped identifiers and CivicPatch `post_id` mappings
are documented as a follow-up contract in issue #5; they must not be silently
discarded by future consumers.

Candidate filing addresses, phone numbers, and email addresses remain private
CivicMirror source data. They are not valid fields on a Civic-Data candidacy or
fixture and are rejected by schema validation. Public office contact data may
remain on a person record only when its source identifies it as office contact
information.

## Data model

### Person

`person.schema.json` replaces `official.schema.json`. A person record has:

- a canonical `ocd-person/<uuid>` `id` and display `name`;
- optional unique-scheme `identifiers[]` entries for reviewed external links;
- `candidacies[]` for election participation;
- `roles[]` for current or historical office relationships;
- existing public office `contact`, `addresses`, and `image` fields;
- `verification` and `sources` provenance.

At least one of `candidacies` or `roles` must be non-empty. An external
identifier is accepted only as a reviewed link; names, addresses, phones,
party, office, and changed contact data are not automatic merge evidence.

Role terms use the shipped nested shape:

```yaml
term:
  start: "2022-12-05"
  end: "2026-12-07"
  how_seated: elected
```

A candidacy contains `contest_id`, `election_id`, `office_id`,
`jurisdiction_id`, `party`, `ballot_name`, optional `status`, and optional
public `sources`. It contains no filing-contact fields.

### Election and contest

Election files remain under `data/us/<state>/elections/`, but each file becomes
an election record containing its identity and a `contests[]` array. An
election has `id`, `name`, `date`, `election_type`, `status`, `contests`, and
`sources`.

Each contest has a collision-safe `id`, `office_id`, `jurisdiction_id`, an
optional `seat`, optional `party`, `vote_for`, `candidate_ids`,
`result_status`, and `winners`. The `seat` field is required whenever the
office's seat structure makes it necessary; the Massachusetts legislative
fixture must demonstrate multiple seats sharing one office. Party primaries
are separate contests with distinct party components in their IDs.

`status` distinguishes scheduled, unofficial, official, certified, and
corrected lifecycle states. A pre-election contest has `result_status: pending`
and `winners: null`; a certified contest has `result_status: certified` and
one or more winner person IDs. Civic-Data stores only outcome linkage, never
precinct results, raw filings, or result snapshots.

## Migration

The migration is an explicit clean schema-version change:

1. Add `person.schema.json` and the revised election schema.
2. Mechanically rename `officials/` to `people/` while preserving every tier
   and municipal town subdirectory.
3. Convert each official document to a person document, retaining all public
   fields and converting its elected role into the corresponding `roles[]`
   shape without fabricating dates.
4. Convert existing per-contest election linkages into one-contest election
   records with `contests[]`; preserve winner names, reviewed official IDs as
   person IDs, seats, certification, and sources.
5. Add representative fixtures for candidate-only, officeholder-only,
   candidate-plus-officeholder, partisan primary, pre-election contest,
   certified winner, and statewide office cases.
6. Update the validator, CI, README, glossary, architecture documentation,
   and all schema references.

The migration script is deterministic, refuses to overwrite an existing
destination, preserves source files on failure, and emits a report of every
converted path and ID. Human review remains required for ambiguous person
records, role dates, and external identifiers.

## Validation and integrity

The validator must:

- validate all person and election documents against the new schemas;
- reject private filing-contact fields and unknown candidacy fields;
- detect duplicate canonical IDs and duplicate external identifiers by scheme;
- resolve every role and candidacy jurisdiction/office reference;
- require every `candidate_ids` person reference to exist;
- require reciprocal person-candidacy and election-contest membership;
- require contest winners to resolve to candidate/person records;
- preserve existing warning-based cross-validation for elected roles and
  certified winners;
- report all errors with repository-relative paths and stable locations.

## Compatibility and rollback

This is a clean schema-version migration. Legacy `official.schema.json`,
`officials/`, `official_id`, and per-contest election shape are removed from
the active model rather than accepted as undocumented aliases. Git provides
rollback before merge; the migration script is non-destructive until its
destination checks pass.

## Acceptance criteria

- Person records validate with candidacies, roles, or both.
- Existing tiered Massachusetts records migrate without information loss.
- Candidate-only and officeholder-only records validate.
- Pre-election contests validate with no winners.
- Certified contests validate with one or more winner references.
- Separate Democratic and Republican primary contests validate.
- A statewide contest and a multi-seat contest with `seat` validate.
- CivicMirror and CivicPatch identifiers coexist and duplicate external IDs
  fail validation.
- Candidate filing contact fields fail validation.
- Person and contest references are reciprocal and validator-enforced.
- Existing jurisdictions and offices remain valid.
- Documentation states the reviewed-PR/read-only-consumer contract and points
  organization/body questions to issue #5.
- The complete validator and fixture test suite passes in CI.
