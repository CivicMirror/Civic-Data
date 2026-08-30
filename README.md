# Civic-Data

**A shared, human-reviewable spine of U.S. civic identity data — jurisdictions, offices, people, candidacies, and elections.**

This repository is a proof of concept for a shared dataset between independent projects that continue to grow:

- **[States](https://en.wikipedia.org/wiki/Wikipedia:List_of_U.S._state_portals)** - LLM scraped data from individual states
- **[OpenStates]([https://civicpatch.org](https://github.com/openstates))** — a crowdsourced Open States aggregates legislative information from all 50 states.
- **[CivicPatch](https://civicpatch.org)** — a crowdsourced, volunteer-verified directory of local elected officials, built from automated scrapers + human review.
- **[CivicMirror](https://civicmirror.app)** — a multi-state election data aggregation platform, built from deterministic per-vendor adapters + LLM extraction pipelines for the long tail.

Each project keeps its own tooling, repos, and scope. This repo holds only the data **both** projects consume, in formats a volunteer can review in a GitHub diff.



## Repository layout

```
schemas/                          JSON Schemas for every entity type
data/
  us/
    ma/                           One directory per state
      jurisdictions/              One YAML file per place/district; tiered
        <state>.yaml                 by government level:
        federal/                     federal (Congress)
        state-upper/ state-lower/    state legislature (sldu/sldl; per-district
                                      jurisdiction files, added only if a tier
                                      needs its own site_intelligence/sources)
        county/                      counties + county-level districts (DA, etc.)
        municipal/                   municipalities
  people/                     One YAML file per person; same tiers
        federal/ state-upper/ state-lower/ county/
        municipal/<town-slug>/      further split per town — this is the one
                                     tier where person-count sprawl warrants it
      elections/                  One YAML file per contest linkage
scripts/
  validate.py                     Schema validation + cross-validation
docs/
  ARCHITECTURE.md                 Design decisions and data model
  GLOSSARY.md                     Term definitions (start here if a field name is ambiguous)
  layout-demos/                   Non-live comparison files for open layout/schema questions
                                   (not read by validate.py); see file headers for what each shows
.github/workflows/validate.yml    CI: runs validate.py on every PR
```

### Entity model (short version)

For precise definitions — including terms that mean different things in
different places, like `classification` and `seat` — see
[`docs/GLOSSARY.md`](docs/GLOSSARY.md).

- **Jurisdiction** — a place with a government. Keyed by [OCD Division ID](https://github.com/opencivicdata/ocd-division-ids). Carries an optional official website URL, government form, and *site intelligence* (CMS/vendor platform) useful to both scraper teams. `classification` covers both local government forms (`city`, `town`, `county`, …) and `congressional-district`.
- **Organization** — one immutable, canonically-IDed record per government body within a jurisdiction (a council, a board, a legislature). Source system identifiers (CivicPatch, Open States) live in `identifiers[]`.
- **Post** — a position that exists independently of the person who holds it (title, seat count) within an organization.
- **Membership** — a time-bounded relationship linking a person to an organization and, usually, a post: start/end dates, `how_seated` (elected/appointed/succeeded/acting), and sources. This is where officeholding lives; `person.yaml` no longer carries office relationships directly.
- **Person** — an individual independent of any office or election. A person can have `candidacies[]` (participation in specific contests); current or historical officeholding lives in `membership.yaml` records instead. One YAML file per person also carries reviewed external identifiers, public office contact information, provenance, and verification.
- **Candidacy** — a person's participation in a specific election contest. Filing addresses, personal phones, and personal emails never enter this shared repository.
- **Election and Contest** — an election record contains one or more contest records. Contests support scheduled pre-election membership with no winners, certified winner references, separate partisan primaries, and explicit seats for multi-seat offices. Raw results (precinct-level rows, live ENR snapshots) stay in CivicMirror; only the small, reviewable outcome linkage lives here.

## Running validation locally

Government data is modeled as `division -> jurisdiction -> organization -> post -> membership/person`. The current sample is a fresh Millbury, MA dataset;


Exit code is non-zero on schema errors or broken references. Cross-validation mismatches are reported as warnings with a full report (they may represent real-world events, not errors — a human decides).

## Researching municipal Charters

The ephemeral eCode360 research tool resolves a municipality through the live
[ICC Code Solutions library](https://www.icccodesolutions.org/text-library/),
retrieves only its Charter, and emits structured JSON for an LLM to review. It
does not write Charter text or other artifacts to the repository; save only the
authoritative URLs needed for provenance.

eCode360 entries use the eCode360 adapter. American Legal Publishing entries
(`codelibrary.amlegal.com`) use a separate browser adapter and are currently
supported for rendered Charter pages such as Wells, Nevada.

Install its Python dependency and browser once:

```bash
pip install -r scripts/requirements.txt
playwright install chromium
```

Invoke it with both a municipality and state (a USPS abbreviation or full state
name):

```bash
python3 -m scripts.ecode360 --municipality "Abington" --state MA
python3 -m scripts.ecode360 --municipality "Abington" --state Massachusetts --headed
```

The single JSON document goes to stdout; progress and diagnostics go to stderr.
Known failures use stable exit statuses: `2` invalid input, `3` directory or
provider resolution, `4` navigation/TOC, `5` Charter selection, and `6`
incomplete extraction. A persistent browser challenge can be diagnosed with
`--headed`. Offline tests exclude network access; the live acceptance test is
explicit:

```bash
python3 -m pytest -m live tests/test_ecode360_live.py -q -s
```

## Data conventions

- **IDs**: OCD Division IDs for geographic places, OCD Person-style UUIDs for people, and stable election/contest keys. External CivicMirror and CivicPatch identifiers are namespaced and accepted only after human review.
- **Names/contacts**: verbatim from the official source.
- **File naming**: currently one file per person, named by person (not jurisdiction), with the ID inside the file only — not appended to the filename the way Open States does it. See `docs/layout-demos/` for what the alternatives would look like; this is an open question, not yet finalized.
- **License**: [CC0 1.0](LICENSE) — public domain dedication, maximally reusable downstream.

## Status

🚧 **Proof of concept.** Massachusetts's congressional and county records are populated end-to-end (jurisdictions, offices, people, and election contests) with **real, sourced data** — not placeholders. Every person record cites where its facts came from; where a phone/fax/address couldn't be verified, it is omitted. `verification.status` is still `unverified` on every record (no human reviewer has signed off), even though the underlying facts are real — it tracks review status only.



Earlier fictional sample data (Oxford/Springfield/Worcester, MA) has been removed; this repo currently only carries data it can back with a real source.
