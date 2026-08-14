# Glossary

Terms used throughout this repo's schemas, scripts, and documentation.

## Core entities

**Jurisdiction** — a geographic place identified by an OCD Division ID. It
contains the offices currently modeled for that place. `jurisdiction_id` does
not yet identify a separate government organization; that follow-up is tracked
in [Civic-Data#5](https://github.com/CivicMirror/Civic-Data/issues/5).

**Office** — an elected position embedded in a jurisdiction's `offices[]`
array, such as Mayor, Select Board Member, or U.S. Representative. Structural
facts (`seats`, `seat_structure`, `term_years`, and `partisan`) live on the
office, not on a person.

**Person** — an individual independent of any office or election. One YAML
file lives under `data/us/{state}/people/`. Its `id` is an
`ocd-person/<uuid>`. A person must have at least one `roles[]` or
`candidacies[]` entry and may have both.

**Role** — a person's relationship to an office. It carries
`jurisdiction_id`, `office_id`, optional `seat`, and a nested `term` with
start/end dates and `how_seated`. A person can have multiple historical roles.

**Candidacy** — a person's participation in one election contest. It carries
`contest_id`, `election_id`, `jurisdiction_id`, `office_id`, party,
`ballot_name`, and optional status. Candidate filing addresses, personal phone
numbers, and personal email addresses are prohibited.

**Election** — a dated event with a lifecycle status and one or more
`contests[]`. Election records are compact and reviewable; raw precinct and
results data remain in CivicMirror.

**Contest** — one office/seat opportunity within an election. It carries
`candidate_ids`, `vote_for`, `result_status`, optional `party` and `seat`, and
nullable `winners`. Party primaries are separate contests even when they share
an election date and permanent office.

**Winner** — a certified or otherwise established outcome reference containing
`person_id` and the reported name, with optional vote and party metadata.

## Contact and provenance

**Address** — a physical public office location in a person's `addresses[]`.
It is distinct from an elected **Office**. A person may have one capitol and
multiple district addresses.

**Contact** — the person's short public-office quick-reference block
(`contact.email`, `contact.phone`, `contact.profile_url`). Filing contact data
is never represented here.

**verification** — review status (`unverified`, `machine-extracted`,
`volunteer-verified`, or `disputed`), reviewer, date, and producing pipeline.

**sources** — URLs with optional notes and retrieval dates supporting a record.

## Overloaded terms

**classification** means the jurisdiction's type when used at
`jurisdiction.classification` (`city`, `town`, `county`,
`congressional-district`, etc.), but means a physical-office type
(`capitol` or `district`) at `person.addresses[].classification`.

**seat** means office structure at `office.seat_structure` (`at-large`,
`ward`, `district`, or `mixed`), but identifies a specific seat at
`role.seat` or `contest.seat` (for example, `5th Suffolk`).

**id** has an entity-specific shape: jurisdiction IDs are OCD divisions,
office IDs are two-segment slugs, person IDs are OCD person UUIDs, election IDs
identify a dated election, and contest IDs identify a seat/opportunity within
that election. They are not interchangeable.

## Integration contract

CivicMirror and CivicPatch propose changes through reviewed pull requests.
Consumers read Civic-Data as a read-only comparison source; it never
automatically overwrites local names, roles, candidacies, contact data, or
identity decisions. External identifiers in `person.identifiers[]` represent
accepted human-reviewed links and are unique by scheme and identifier.

Organization-scoped identifiers and CivicPatch `post_id` mappings are not part
of the current model. They require an explicit transformation and a future
government-body design under issue #5.

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for design rationale and
`schemas/*.schema.json` for authoritative field definitions.
