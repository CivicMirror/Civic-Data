# Glossary

Terms used throughout this repo's schemas, scripts, and docs — written down
because a few of them are overloaded (the same word means different things
in different fields) and that's caused real confusion during development.
When a term collides with another use of the same word, both meanings are
listed with the field paths that disambiguate them.

## Core entities

 Concept         Correct identifier                       Meaning
  ━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Division        ocd-division/...                         Geographic area: state, county, city, district
  ──────────────  ───────────────────────────────────────  ──────────────────────────────────────────────────────────────────────────
   Jurisdiction    ocd-jurisdiction/.../<classification>    Governing authority within that division
  ──────────────  ───────────────────────────────────────  ──────────────────────────────────────────────────────────────────────────
   Organization    ocd-organization/<uuid>                  Concrete body or institution, such as a legislature, council, or chamber
  ──────────────  ───────────────────────────────────────  ──────────────────────────────────────────────────────────────────────────
   Post                                                      The position that exists under the Org
  ──────────────  ───────────────────────────────────────  ──────────────────────────────────────────────────────────────────────────
   Membership      ocd-person/<jane-doe>                     The person that holds the membership
  ──────────────  ───────────────────────────────────────  ──────────────────────────────────────────────────────────────────────────
   Role                                                     What function does the position or member perform?
  ──────────────  ───────────────────────────────────────  ──────────────────────────────────────────────────────────────────────────


The data model distinguishes a geographic **Division** from the **Jurisdiction** governing it. A jurisdiction uses an `ocd-jurisdiction/.../<classification>` ID and carries a `division_id` pointing to the geographic `ocd-division/...` record. A concrete board or agency is an **Organization**, identified canonically as `ocd-organization/<uuid>`.

Organizations may carry an `identifiers[]` array. These are source-scoped identifiers from CivicPatch, Open States, or another project; they do not replace the Civic-Data canonical `id`.

**Post** is a position independent of its holder. **Membership** connects a person to an organization and optional post over time. **Role** describes the function or title performed in that membership; it is not a unique position ID.
**Jurisdiction** — a governing authority within a geographic division. One
YAML file per jurisdiction, under `data/us/{state}/jurisdictions/`.
Identified by an OCD jurisdiction ID such as
`ocd-jurisdiction/country:us/state:ma/place:millbury/government`; its
`division_id` points to `ocd-division/country:us/state:ma/place:millbury`.
Its `classification` is a governance type such as `government`, `school`,
or `transit_authority`.

**Post** = **elected position** = **seat** (loosely) = **office name.**
A position that exists within an Organization — e.g. "Mayor," "Select
Board Member," "U.S. Representative." A standalone file under
`data/us/{state}/posts/`, not embedded in the jurisdiction. Identified by
`post.id`, a slug in `<jurisdiction-slug>/<office-slug>` form (e.g.
`oxford-ma/select-board`). Structural facts about the position —
`seats` (how many people hold it at once), `organization_id` — live
here, not on the person.

**Person** — an individual, real or (in remaining sample data)
fictional. One YAML file per person, under `data/us/{state}/people/`.
Identified by `person.id`, an `ocd-person/<uuid>`. A file's `name` is the
person; everything about *which office(s)* they hold lives in
`membership.yaml` records, not on the person directly — a person is not
tied to one office for life (see "Membership" below).

**Membership** — the link between a Person and an Organization/Post: a
standalone file under `data/us/{state}/memberships/`. Carries
`person_id`, `organization_id`, optionally `post_id`, `role` (the
title/function held), `start`/`end` dates, and `how_seated`
(`elected`/`appointed`/`succeeded`/`acting`). **A person can have more
than one membership** — this is not a hypothetical: Richard Neal has
two, because he represented a different-numbered district before 2013
redistricting. "People change memberships; posts themselves rarely
change" is the operating assumption — this is why membership data lives
in its own directory, keyed by person, rather than as flat fields on
either the person or the post.

**Election linkage** — a compact, reviewable summary of the contest that
seated an official: date, winner(s), certification status, one source.
One YAML file per contest, under `data/us/{state}/elections/`. **Not**
the full result set — precinct-level rows and raw ENR data stay in
CivicMirror; this repo only holds the small linkage record plus an
optional `detail_ref` pointer to the full data.

## Contact & location

**Address** — a *physical* place to reach an official: a mailing
address, phone, fax. Lives in `official.addresses[]`, one entry per
office location. **This is not the same concept as "Office."** A
representative has one Office (their elected position) but can have
several Addresses (a D.C./capitol office plus multiple district
offices) — e.g. Bill Keating has one `us-representative` office and
four addresses. Each entry's `classification` is `capitol` or
`district` (see "classification" below).

**Contact** — the *short* quick-reference block on an official
(`official.contact`): `email`, `phone`, `profile_url`. `phone` here is
the person's primary/capitol number, for convenience — the full address
list (if there's more than one office) is in `addresses[]`, not here.
These two fields aren't kept in sync automatically; both are
hand/scraper-maintained.

## Overloaded terms — read the field path, not just the word

**classification** means two unrelated things depending on where it
appears:
- `jurisdiction.classification` — the jurisdiction's own type:
  `city`, `town`, `county`, `congressional-district`, etc.
- `official.addresses[].classification` — which kind of physical office
  an address is: `capitol` or `district`.

**seat** also means two related-but-distinct things:
- `office.seat_structure` — *how* an office's seat(s) are structured:
  `at-large`, `ward`, `district`, or `mixed`. A property of the office
  itself.
- `role.seat` — *which* seat a specific official holds, when an office
  has more than one (e.g. `"Ward 3"`, `"District 2"`, or `"At-Large"`
  for a single/at-large seat). A property of the person's role, not the
  office.

**id** exists on every entity but in a different shape each time —
`jurisdiction.id` is an OCD Division ID, `office.id` is a two-segment
slug, `official.id` is an `ocd-person/<uuid>`, `election-linkage.id` is
a `<jurisdiction-slug>/<date>/<office-slug>` path. None of these are
interchangeable; each schema documents its own pattern.

## Provenance

**verification** — an official record's review status
(`unverified` / `machine-extracted` / `volunteer-verified` /
`disputed`), who reviewed it, and what pipeline produced it. Distinct
from **sources** (below) — verification says *how trustworthy this
record is judged to be*; sources says *where the data came from*.

**sources** — a list of `{url, note, retrieved}` citing where a
record's facts were found. Every jurisdiction, official, and election
linkage requires at least one. `retrieved` is when the data was pulled,
not when the source itself was published or last updated.

## See also

- [`ARCHITECTURE.md`](ARCHITECTURE.md) — *why* the repo is shaped this
  way, not just what the terms mean.
- `schemas/*.schema.json` — the authoritative, machine-checked
  definition of every field named here. If this glossary and a schema
  ever disagree, the schema is correct and this file is stale.
