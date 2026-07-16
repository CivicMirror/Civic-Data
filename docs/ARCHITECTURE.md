# Architecture & design decisions

This document records *why* the repo is shaped the way it is, so the design
can be debated concretely at the CivicPatch × CivicMirror meeting.

## 1. Two projects, one spine

CivicPatch and CivicMirror remain independent projects with their own repos,
tooling, and governance. This repo holds **only** data both projects consume:

```
        CivicPatch                          CivicMirror
   scrapers + review UI              adapters + LLM pipelines
        │       ▲                          │        ▲
   bot PRs      │ read-only           bot PRs       │ read-only
        ▼       │                          ▼        │
        ┌───────┴──────────────────────────┴────────┐
        │              Civic-Data (this repo)       │
        │  jurisdictions · offices · officials ·    │
        │  election linkages · CI cross-validation  │
        └───────────────────────────────────────────┘
```

**Scope discipline:** the moment a piece of data is only needed by one
project, it moves back into that project's repo. This keeps the spine small,
reviewable, and prevents "shared repo" from quietly becoming "merged project."

## 2. Git + YAML, one file per entity

Follows the proven `openstates/people` model, which CivicPatch already
contributes to:

- **Diffs are the review unit.** One YAML file per official means a scraper
  update produces a small, human-readable diff — exactly what CivicPatch's
  volunteer verification process reviews today.
- **PRs are the write path.** Both projects' bots author PRs; humans merge.
  No direct pushes to `main`.
- **CI is the first reviewer.** Schema validation, reference integrity, and
  duplicate detection run before a human ever looks.

## 3. What stays out: raw election results

Precinct-level rows, live ENR snapshots, and certification revisions are
large, spiky, and churn during canvass — git handles that badly and no
volunteer can meaningfully review a 40,000-row diff.

Instead, the shared repo stores an **election linkage**: contest date,
winner(s), certification status, and a `detail_ref` URI pointing at the full
results in CivicMirror. Small, stable, reviewable.

## 4. Identifiers

| Entity | Scheme | Rationale |
|---|---|---|
| Jurisdiction | OCD Division ID | Ecosystem standard; joins to Census, Open States, Google Civic |
| Office | `<jurisdiction-slug>/<office-slug>` | Human-readable join key between the two datasets |
| Official | `ocd-person/<uuid4>` | Open States convention; survives name changes |
| Election linkage | `<jurisdiction-slug>/<date>/<office-slug>` | Sorts naturally; one contest per file |

Where Open States / OCD has a convention, we adopt it rather than invent one.
This keeps the door open to upstreaming officials data to `openstates/people`.

## 5. Cross-validation semantics

The CI check joins the two datasets and asks three questions:

1. **name-disagreement** — a winner explicitly linked (`official_id`) to an
   official record, but the names don't match. Almost always a data error.
2. **winner-not-seated** — the most recent *certified* election's winner is
   absent from the officials directory for that office. Either a scrape gap
   **or a real-world event** (resignation, appointment, recall, death).
3. **no-election-trace** — an official recorded as `how_seated: elected`
   with no election linkage naming them. Either a missing linkage or a
   miscoded `how_seated`.

Findings 2 and 3 are deliberately **warnings, not failures**: the mismatch is
the *product*, not a bug. A mismatch that survives human review becomes a
recorded succession event — that's the audit-trail value neither project can
produce alone. (`--strict` mode exists for teams who want warnings to gate.)

Name matching is a conservative normalization heuristic (casefold, strip
accents/punctuation), not identity resolution. False positives go to humans;
that's the point.

## 6. Provenance & verification

Every record carries `sources` (URL + retrieval date) and officials carry a
`verification` block:

`unverified → machine-extracted → volunteer-verified` (or `disputed`)

This makes the trust level of every record explicit and queryable — an
LLM-extracted record and a volunteer-verified record are never
indistinguishable. This is also the natural integration point with
CivicPatch's AI policy: machine output is always labeled as such, and human
review is the promotion mechanism.

## 7. Open questions for the meeting

- **Where does the repo live?** CivicPatch org, CivicMirror org, or a neutral
  shared org? (Neutral org avoids perceived ownership asymmetry.)
- **License** — CC0 proposed here; confirm it's compatible with CivicPatch's
  existing open-data licensing and upstream expectations.
- **Merge rights** — proposal: CivicPatch volunteer reviewers are the merge
  gate for `officials/`; either project's maintainers for `jurisdictions/`
  and `elections/`.
- **Upstreaming** — should volunteer-verified officials flow to
  `openstates/people` automatically, and what attribution does that need?
- **Schema governance** — schema changes require sign-off from both projects?
- **Sync cadence** — do bots PR continuously, on a schedule, or post-election?
