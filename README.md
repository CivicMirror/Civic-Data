# Civic-Data

**A shared, human-reviewable spine of U.S. local government data — jurisdictions, offices, officials, and the elections that seated them.**

This repository is a proof of concept for a shared dataset between two independent projects:

- **[CivicPatch](https://civicpatch.org)** — a crowdsourced, volunteer-verified directory of local elected officials, built from automated scrapers + human review.
- **CivicMirror** — a multi-state election data aggregation platform, built from deterministic per-vendor adapters + LLM extraction pipelines for the long tail.

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
  GLOSSARY.md                     Term definitions (start here if a field name is ambiguous)
  layout-demos/                   Non-live comparison files for open layout/schema questions
                                   (not read by validate.py); see file headers for what each shows
.github/workflows/validate.yml    CI: runs validate.py on every PR
```

### Entity model (short version)

For precise definitions — including terms that mean different things in
different places, like `classification` and `seat` — see
[`docs/GLOSSARY.md`](docs/GLOSSARY.md).

- **Jurisdiction** — a place with a government. Keyed by [OCD Division ID](https://github.com/opencivicdata/ocd-division-ids). Carries the official website URL, government form, and *site intelligence* (CMS/vendor platform) useful to both scraper teams. `classification` covers both local government forms (`city`, `town`, `county`, …) and `congressional-district`.
- **Office** — an elected position that exists within a jurisdiction (embedded in the jurisdiction file): title, seat structure (at-large / ward / district), term length, election authority.
- **Official** — a person, and *every* office they've held, past or present — not just their current one. One YAML file per person; each office held is one entry in `roles[]`, since people change offices (redistricting, running for a different seat) far more often than an office's own definition changes. Also carries `addresses[]` (physical offices — a capitol/D.C. office plus any number of district offices, each with its own address/phone/fax) and an optional `image`. `contact` stays as a short quick-reference block (email/phone/profile URL); `addresses[]` is where the full, possibly-multiple office locations live. Contact fields are copied **verbatim** from the official source (CivicPatch convention). Every record carries provenance and a `verification` block.
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

- **IDs**: OCD Division IDs for places, OCD Person-style UUIDs for people. Where [Open States](https://github.com/openstates/people) has a convention, we adopt it rather than invent one — including career-spanning `roles[]` on an official rather than one flat office per record.
- **Names/contacts**: verbatim from the official source.
- **File naming**: currently one file per person, named by person (not jurisdiction), with the ID inside the file only — not appended to the filename the way Open States does it. See `docs/layout-demos/` for what the alternatives would look like; this is an open question, not yet finalized.
- **License**: [CC0 1.0](LICENSE) — public domain dedication, maximally reusable downstream.

## Status

🚧 **Proof of concept.** Massachusetts's full 9-seat U.S. House delegation is populated end-to-end (jurisdictions, offices, officials, and election linkages) with **real, sourced data** — not placeholders. Every official record cites where its facts came from (official House.gov pages, Wikipedia, or web search where a direct fetch was blocked) rather than inventing anything; where a phone/fax/address couldn't be verified, it's simply omitted. `verification.status` is still `unverified` on every record (no human reviewer has signed off), even though the underlying facts are real — don't treat that field as "fictional vs. real," it tracks review status only.

Two known gaps, tracked as open follow-ups rather than silently resolved:
- 7 of the 9 officials have no `elections/` linkage file yet (Richard Neal and, indirectly, the 1st district are the exception — his two real district wins are fully linked), so `validate.py` reports 8 standing `no-election-trace` warnings. These are expected, not bugs.
- `docs/layout-demos/` holds non-live comparison files for an open schema/layout question (grouped-by-place vs. one-file-per-person, ID-in-filename vs. not) — not part of the dataset, not read by CI.

Earlier fictional sample data (Oxford/Springfield/Worcester, MA) has been removed; this repo currently only carries data it can back with a real source.
