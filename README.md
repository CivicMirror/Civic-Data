# Civic-Data

**A shared, human-reviewable spine of U.S. civic identity data — jurisdictions, offices, people, candidacies, and elections.**

This repository is a proof of concept for a shared dataset between two independent projects:

- **[CivicPatch](https://civicpatch.org)** — a crowdsourced, volunteer-verified directory of local elected officials, built from automated scrapers + human review.
- **[CivicMirror](https://civicmirror.app)** — a multi-state election data aggregation platform, built from deterministic per-vendor adapters + LLM extraction pipelines for the long tail.

Each project keeps its own tooling, repos, and scope. This repo holds only the data **both** projects consume, in formats a volunteer can review in a GitHub diff.

## Why share a spine?

The two projects work opposite ends of the same pipeline:

| | CivicPatch | CivicMirror |
|---|---|---|
| Answers | *Who holds this office?* | *What election put them there?* |
| Collection | Scrapers on municipal websites | ENR feeds, certification PDFs, vendor APIs |
| Verification | Volunteer diff review | Deterministic adapters + confidence scoring |

Joined on a common jurisdiction/office key, **each dataset becomes the audit trail for the other**: an election winner who doesn't match the current officeholder is either a data error (caught!) or a real-world event worth recording (resignation, appointment, recall). The CI in this repo performs that cross-validation on every pull request.

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

## Contribution model

1. **Bots open PRs.** CivicPatch scrapers and CivicMirror pipelines both write via bot-authored pull requests — never direct pushes to `main`.
2. **CI validates.** Every PR runs schema validation, OCD-ID reference checks, duplicate detection, reciprocal person↔contest checks, and people↔elections cross-validation.
3. **Humans merge.** CivicPatch's volunteer review process is the merge gate. If CI flags a mismatch, the PR description says exactly what disagrees and why.
4. **Projects consume read-only.** Both projects pin releases (or track `main`) and treat this repo as a dependency.

## Running validation locally

Government data is modeled as `division -> jurisdiction -> organization -> post -> membership/person`. The current sample is a fresh Millbury dataset; old sample IDs are not migration inputs. External source identifiers are retained under each entity's `identifiers[]` field.

```bash
pip install -r scripts/requirements.txt
python scripts/validate.py
```

Exit code is non-zero on schema errors or broken references. Cross-validation mismatches are reported as warnings with a full report (they may represent real-world events, not errors — a human decides).

## Data conventions

- **IDs**: OCD Division IDs for geographic places, OCD Person-style UUIDs for people, and stable election/contest keys. External CivicMirror and CivicPatch identifiers are namespaced and accepted only after human review.
- **Names/contacts**: verbatim from the official source.
- **File naming**: currently one file per person, named by person (not jurisdiction), with the ID inside the file only — not appended to the filename the way Open States does it. See `docs/layout-demos/` for what the alternatives would look like; this is an open question, not yet finalized.
- **License**: [CC0 1.0](LICENSE) — public domain dedication, maximally reusable downstream.

## Status

🚧 **Proof of concept.** Massachusetts's congressional and county records are populated end-to-end (jurisdictions, offices, people, and election contests) with **real, sourced data** — not placeholders. Every person record cites where its facts came from; where a phone/fax/address couldn't be verified, it is omitted. `verification.status` is still `unverified` on every record (no human reviewer has signed off), even though the underlying facts are real — it tracks review status only.

Two known gaps, tracked as open follow-ups rather than silently resolved:
- Most current people have no corresponding election contest in this proof-of-concept dataset, so `validate.py` reports standing `no-election-trace` warnings. These are expected review findings, not schema failures.
- `docs/layout-demos/` holds non-live comparison files for an open schema/layout question (grouped-by-place vs. one-file-per-person, ID-in-filename vs. not) — not part of the dataset, not read by CI.

Earlier fictional sample data (Oxford/Springfield/Worcester, MA) has been removed; this repo currently only carries data it can back with a real source.
