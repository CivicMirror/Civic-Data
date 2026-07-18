# Civic-Data

**A shared, human-reviewable spine of U.S. local government data — jurisdictions, offices, officials, and the elections that seated them.**

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
      jurisdictions/              One YAML file per municipality/county
      officials/                  One YAML file per officeholder
      elections/                  One YAML file per contest linkage
scripts/
  validate.py                     Schema validation + cross-validation
docs/
  ARCHITECTURE.md                 Design decisions and data model
.github/workflows/validate.yml    CI: runs validate.py on every PR
```

### Entity model (short version)

- **Jurisdiction** — a place with a government. Keyed by [OCD Division ID](https://github.com/opencivicdata/ocd-division-ids). Carries the official website URL, government form, and *site intelligence* (CMS/vendor platform) useful to both scraper teams.
- **Office** — an elected position that exists within a jurisdiction (embedded in the jurisdiction file): title, seat structure (at-large / ward / district), term length, election authority.
- **Official** — a person currently holding an office. Contact fields are copied **verbatim** from the official municipal source (CivicPatch convention). Every record carries provenance and a `verification` block.
- **Election linkage** — a compact summary of the contest that seated an official: date, winner, certification status, and source. Raw results (precinct-level rows, live ENR snapshots) stay in CivicMirror; only the small, reviewable linkage lives here.

## Contribution model

1. **Bots open PRs.** CivicPatch scrapers and CivicMirror pipelines both write via bot-authored pull requests — never direct pushes to `main`.
2. **CI validates.** Every PR runs schema validation, OCD-ID reference checks, duplicate detection, and officials↔elections cross-validation.
3. **Humans merge.** CivicPatch's volunteer review process is the merge gate. If CI flags a mismatch, the PR description says exactly what disagrees and why.
4. **Projects consume read-only.** Both projects pin releases (or track `main`) and treat this repo as a dependency.

## Running validation locally

```bash
pip install -r scripts/requirements.txt
python scripts/validate.py
```

Exit code is non-zero on schema errors or broken references. Cross-validation mismatches are reported as warnings with a full report (they may represent real-world events, not errors — a human decides).

## Data conventions

- **IDs**: OCD Division IDs for places, OCD Person-style UUIDs for people. Where [Open States](https://github.com/openstates/people) has a convention, we adopt it rather than invent one.
- **Names/contacts**: verbatim from the official municipal source.
- **License**: [CC0 1.0](LICENSE) — public domain dedication, maximally reusable downstream.

## Status

🚧 **Proof of concept.** Massachusetts is partially populated with sample data to demonstrate the model, including one *deliberate* officials↔elections mismatch so you can see the cross-validation CI in action. Sample officials are marked `verification.status: unverified` and must not be treated as accurate until reviewed.
