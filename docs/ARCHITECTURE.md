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

## 3. What stays out

**Raw election results.** Precinct-level rows, live ENR snapshots, and
certification revisions are large, spiky, and churn during canvass — git
handles that badly and no volunteer can meaningfully review a 40,000-row
diff.

Instead, the shared repo stores an **election linkage**: contest date,
winner(s), certification status, and a `detail_ref` URI pointing at the full
results in CivicMirror. Small, stable, reviewable.

**Internal board titles.** CivicPatch sometimes labels a board member by an
internally-assigned title (Chair, Vice Chair, Clerk) rather than their
formal elected office. These titles aren't separately elected — the charter
creates one office (e.g. "Select Board Member") and the board assigns roles
to itself after the election, not the ballot. Surfaced by
[CivicMirror/Civic-Data#3](https://github.com/CivicMirror/Civic-Data/issues/3):
CivicPatch's raw Millbury data gave its 5 Select Board members 4 different
`office.name` values (Council Member ×2, Chair, Vice Chair, Clerk) — none of
which slug to this repo's one real office, `millbury-ma/select-board`, and
"Council Member" is factually wrong for a Select Board town besides.

civic-data tracks only the formal office, since that's what a `roles[]`
entry needs to join to an actual election contest — internal titles have no
election behind them to join to. Nothing in `official.schema.json` carries
an internal title (`roles[]` has no `notes` field); this is a deliberate
omission, not a gap. The title is CivicPatch's data to keep, not something
normalized into this schema.

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

## 7. Directory tiering by government level

`jurisdictions/` and `officials/` are both subdivided by government tier —
`federal/`, `state-upper/`, `state-lower/`, `county/`, `municipal/` — inside
each state's directory (`data/us/<state>/{jurisdictions,officials}/<tier>/`).
Settled now, before a second state is added, so every state inherits the
same convention rather than each one improvising its own.

**Why tier at all.** A flat `officials/` directory scales with total
officeholder count, not place count: Massachusetts alone has 200 state
legislature seats and 351 municipalities, each with several elected
officials — thousands of files nationally, in one directory, mixing federal,
state, county, and town records together. Tiering makes a PR's blast radius
legible at a glance (a diff under `officials/state-upper/` obviously can't
touch a town clerk) without changing the one-file-per-person model itself.

**Why `state-upper`/`state-lower`, not `state-house`/`state-senate`.** State
chamber names aren't uniform (California/New York call the lower chamber
"Assembly," Virginia calls it "House of Delegates," Nebraska is unicameral).
Naming the tier after a specific state's chamber name breaks on the next
state. `state-upper`/`state-lower` borrows OCD's own division-type vocabulary
(`sldu`/`sldl`) per the convention set in §4 — chamber-generic, and a
unicameral state simply never populates `state-lower/`.

**Why `officials/municipal/` nests one level further, by town slug, and
`jurisdictions/municipal/` does not.** A jurisdiction file is already 1:1
with its place (`millbury.yaml` is one file regardless of how many Select
Board seats it defines) — flat is fine. An officials directory is 1:many
(Millbury's Select Board alone is 5 files); at hundreds of towns per state,
that's the tier where person-count sprawl is worst, so it's the one tier
that subdivides again:
`officials/municipal/<town-slug>/<person>.yaml`.

**State legislature seats stay embedded, not per-district files.** Unlike
congressional districts (one `cd-N.yaml` jurisdiction file per district,
each with its own officeholder/site), Massachusetts's state House/Senate
seats are modeled as two offices — `seats: 160`/`40`,
`seat_structure: district` — embedded directly on `ma.yaml`, with each
official's `role.seat` naming their district (e.g. `"5th Suffolk"`). This
keeps 200 legislative seats from requiring 200 new jurisdiction files; a
`state-upper`/`state-lower` jurisdiction tier exists in principle for a
state where a legislative district needs its own `site_intelligence` or
sources, but isn't needed for the embedded-office case.

## 8. Open questions for the meeting

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
