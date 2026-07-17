# Data Flow: CivicPatch × CivicMirror × Civic-Data

How data moves between the two source projects and the shared repository — both the one-time backfill and the ongoing steady-state flow.

## The Big Picture

```mermaid
flowchart TB
    subgraph CP["CivicPatch"]
        CPS["Municipal site scrapers"]
        CPD["Existing officials dataset"]
        CPV["Volunteer reviewers"]
    end

    subgraph CM["CivicMirror"]
        CMA["State ENR adapters<br/>(TX, OH, NY, CT, AR, KY, AZ, SC, IA, WI, MA...)"]
        CMD[("Results database<br/>(Django/PostgreSQL)")]
        CME["Linkage export<br/>(management command)"]
    end

    subgraph CD["Civic-Data (shared GitHub repo)"]
        PR["Bot-authored PRs"]
        CI["GitHub Actions CI<br/>schema · references · duplicates · cross-validation"]
        MAIN[("main branch<br/>canonical YAML")]
    end

    CPS -->|"transform to YAML<br/>(machine-extracted)"| PR
    CPD -->|"one-time backfill<br/>(volunteer-verified)"| PR
    CMA --> CMD
    CMD --> CME
    CME -->|"election linkages<br/>(winners + certification)"| PR

    PR --> CI
    CI -->|"report posted on PR"| CPV
    CPV -->|"review + merge<br/>= verification gate"| MAIN

    MAIN -->|"builds & serves"| API["Elections / Officials API<br/>(public, merged)"]
    MAIN -->|"optional upstream"| OS["openstates/people"]

    API --> C1["Journalists"]
    API --> C2["Civic apps & researchers"]
    API --> C3["Anyone who needs it"]
```

**The key idea:** both projects *contribute* through pull requests; neither consumes the data back — they already have their own copies. The shared repo exists to power something new: a single public **Elections/Officials API** that can answer "who holds this office, and what election put them there?" — a question neither dataset can answer alone. Nothing enters `main` without passing CI and a human merge; the merge itself is the verification event.

## Flow 1 — CivicPatch → Civic-Data (officials & jurisdictions)

### Ongoing (steady state)

```
Municipal website
      │  scraper run (existing CivicPatch tooling)
      ▼
Raw extracted record (name, role, email, phone, url, ward/district)
      │  transform step: map to official.schema.json
      │  - verification.status: machine-extracted
      │  - sources: [{url, retrieved: <date>}]
      ▼
Bot opens PR  ──  one jurisdiction per PR, small & thematic
      │
      ▼
CI runs: schema ✓  refs ✓  dupes ✓  cross-validation vs election linkages
      │  report posted to PR (matches, warnings, conflicts)
      ▼
CivicPatch volunteer reviews the diff  (same review they do today,
      │                                 just on GitHub instead of custom UI)
      ▼
Merge → record lands in main as volunteer-verified
```

### One-time backfill

```
Existing CivicPatch dataset
      │  migration script (run once per state)
      │  - already-verified records keep status: volunteer-verified
      │  - unreviewed records enter as: machine-extracted
      ▼
One PR per state  →  CI  →  spot-check the *conversion*, not each record
      ▼
Merge
```

Records their volunteers already verified don't get re-reviewed — the human review already happened. Reviewers only sanity-check that the format conversion is faithful.

## Flow 2 — CivicMirror → Civic-Data (election linkages)

### Ongoing (steady state)

```
State ENR / certification source
      │  existing CivicMirror adapter ingests full results
      ▼
CivicMirror results DB (full detail: precincts, vote counts, candidates)
      │  Django management command: export_linkages
      │  - winners per contest only (compact)
      │  - certification status
      │  - detail_ref URI → back to full CivicMirror results
      ▼
Bot opens PR  ──  linkage YAML per contest
      ▼
CI + cross-validation:
      - does the winner match a seated official?      → CROSS: name-disagreement
      - is the winner missing from officials?          → CROSS: winner-not-seated
      - is an elected official missing an election?    → CROSS: no-election-trace
      ▼
Review + merge
```

Full election results **never** enter the shared repo — only the compact linkage record. Raw results stay in CivicMirror; `detail_ref` points back to them.

### One-time backfill

```
CivicMirror results DB
      │  same management command, run historically
      │  batched: one PR per state
      ▼
CI  →  review  →  merge
```

The main effort is not the YAML dump — it's **mapping contests to stable office IDs and OCD division IDs**. Budget roughly a weekend for the first state; subsequent states reuse the mapping patterns.

## Flow 3 — The Cross-Validation Loop (where the value is)

```
        officials/*.yml                election-linkages/*.yml
        (CivicPatch data)              (CivicMirror data)
              │                               │
              └──────────┬────────────────────┘
                         ▼
              scripts/validate.py  (runs in CI on every PR,
                         │          or locally by anyone)
                         ▼
        ┌────────────────┼────────────────────┐
        ▼                ▼                    ▼
   ✓ MATCH          ⚠ CROSS WARNING      ✗ ERROR
   winner is        winner-not-seated    schema violation
   seated with      name-disagreement    broken reference
   matching name    no-election-trace    duplicate ID
        │                │                    │
        ▼                ▼                    ▼
   merge freely     human investigates:  CI fails,
                    data error? or       PR blocked
                    resignation /        until fixed
                    appointment /
                    recall? (real-world
                    events are OK —
                    document & merge)
```

**Warnings don't block merges by default** (`--strict` makes them fail) because a mismatch can be a *real-world event* — a resignation, an appointment, a recall — not a data error. Each dataset is the audit trail for the other.

## Who Touches What

| Actor | Writes via | Reads from | Merge rights |
|---|---|---|---|
| CivicPatch scrapers/bot | PRs (machine-extracted) | — | No |
| CivicMirror export bot | PRs (linkages) | — | No |
| CivicPatch volunteers | Manual fix PRs | main | **Yes — the gate** |
| Elections/Officials API | — | main (build source) | No |
| API consumers (public) | — | the API | No |
| openstates/people | — | optional downstream sync | — |

Bots never merge their own PRs, and bots never emit `volunteer-verified` — that status can only be conferred by a human merge. The source projects don't read the data back — they already hold their own copies. The repo's output is the API.

## Flow 4 — Civic-Data → Elections/Officials API

```
main branch (canonical YAML)
      │  merge to main triggers build (GitHub Action)
      ▼
Build step: YAML → single queryable dataset
      │  (SQLite bundle, JSON dumps, or generated static API —
      │   decision for the two teams)
      ▼
Elections / Officials API  (public)
      │
      ├─ GET /jurisdictions/{ocd-id}
      ├─ GET /officials?office=worcester-ma/mayor
      ├─ GET /elections?jurisdiction=springfield-ma
      └─ GET /officials/{id}/elections   ← the merged question:
                                            "what election seated this person?"
```

The API is the product of the collaboration — the thing neither project can offer alone. CivicPatch answers *who is in office*; CivicMirror answers *how they got there*; the API answers both in one call.

**Cheapest v1:** a static build — every merge regenerates JSON files served from GitHub Pages or a CDN. No servers, no ops burden, and it can graduate to a real hosted API later without changing the repo side at all.
