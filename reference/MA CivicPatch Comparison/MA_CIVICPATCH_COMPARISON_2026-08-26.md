# MA Municipal Data Comparison: this repo vs. CivicPatch/open-data

Generated: 2026-08-26
Compared against: https://github.com/CivicPatch/open-data/tree/main/data/ma/local (172 towns)
Repo state compared: `data/us/ma` at commit `9d5aa10ff` (all 351 towns imported)

## Method

CivicPatch's per-town files are a flat list of current officeholders, almost
entirely for one body: Select Board / Town Council / City Council (or Mayor
for the handful of cities that elect one). This repo's data is broader — it
covers every locally elected office a town has (Assessor, Housing Authority,
Library Trustee, Planning Board, School Committee, etc.), not just the
executive body.

To compare like with like, `ma_execboard_name_diff_2026-08-26.csv` restricts
the repo side to just the executive-body office (`select-board-member`,
`council-member`, `mayor`, and equivalents) per town, then diffs the holder
name sets against CivicPatch's full roster for that town. Names are
normalized (lowercased, punctuation stripped, Jr/Sr/II/III suffix dropped)
before comparing, so `"Robert E. Betsold"` and `"robert betsold"` count as a
match; nickname/initial differences (`"Sal Bramante"` vs `"Salvatore
Bramante"`) do not.

`ma_town_overview_2026-08-26.csv` is broader: total repo org count, total
repo current-holder count (across *all* offices, not just the executive
body), and CivicPatch's row/name count, per town, plus the earliest batch
version detected in that town's org file headers (a rough proxy for "when was
this town researched").

145 of CivicPatch's 172 towns overlap with this repo's 351.

## Headline numbers (executive-body comparison, 145 towns)

| Bucket | Towns |
|---|---:|
| Repo has zero current holders for the executive body | 73 |
| Repo has holders, names match CivicPatch exactly (normalized) | 29 |
| Repo has holders, but the name sets differ | 43 |

## Finding 1: officeholder backfill is uneven, not just an early-batch gap

Of the 73 zero-holder towns, 33 trace to the original `v20` batch
(2026-08-20). Checking the actual `v20` source file (recovered from git
history, commit `8295e4dbb`) confirms these towns have **zero membership
rows in the source itself** — not an import-script omission. `v20`'s source
did capture 1,433 people across other towns in the same batch, so the office
structure vs. officeholder split was applied per-town within v20, not a
schema limitation of the whole batch.

The remaining 40 zero-holder towns are scattered across `v30` through `v56`
— mostly single-town gap-fill batches whose own READMEs already flag the gap
(e.g. Leverett, v56: *"current holders are left unresolved absent a clean
post-2026 roster"*).

**Practical read:** treat "zero holders" as "structure researched, holder
backfill not yet done" rather than "batch is broken." A backfill pass focused
on these 73 towns' executive board is the most direct way to close this.

## Finding 2: most of the 43 partial-match towns are formatting noise, not errors

Typical pattern — same person, different string:

| Repo | CivicPatch |
|---|---|
| `Salvatore Bramante` | `Sal Bramante` |
| `Anthony Michael Alves` | `Anthony Alves` |
| `Lorraine Carboni` | `Lorraine A Carboni` |
| `Carleton "Toby" Burr` | `Carleton (Toby) Burr` |

A few look like a real spelling difference rather than a nickname, worth a
one-off check: `Eric Kelley` (repo, Marshfield) vs. `Erik S Kelley`
(CivicPatch) — "Eric" vs "Erik" is a genuine name discrepancy, not a format
difference.

## Finding 3: eight towns have a real roster gap, not just formatting

These have mostly-disjoint name sets after normalization — the repo is
missing seats' worth of actual current officeholders, not just spelling
them differently:

- **Hardwick** — repo has 1 holder, CivicPatch has 3
- **Lee** — repo has 1, CivicPatch has 3
  
  - https://leema.gov/DocumentCenter/View/218/Town-Leadership-Team-Charter-PDF
  - https://leema.gov/DocumentCenter/View/167/Special-Act-Charter-Review-Final-Report-PDF?bidId=
  - https://ecode360.com/LE1695
  - https://leema.gov/DocumentCenter/View/580/TOWN-MEETING-or-TOWN-ELECTION-WARRANT-2022
  - https://leema.gov/235/Past-Town-Elections
  - https://leema.gov/468/Select-Board
  - https://leema.gov/272/Planning-Board
  - https://leema.gov/276/Housing-Authority
  - https://leema.gov/282/Board-of-Public-Works
  - https://leema.gov/268/Youth-Commission
- **Milton** — repo has 5, CivicPatch has 5, but 0 matched as identical  strings (on inspection these are the same 5 people, formatted very differently — needs a manual pass, not a backfill)
  - https://www.miltonma.gov/399/Select-Board
  - https://www.miltonma.gov/1292/Annual-Town-Election--APRIL-28-2026
  - https://www.miltonma.gov/ArchiveCenter/ViewFile/Item/288
  - https://www.miltonma.gov/ArchiveCenter/ViewFile/Item/282
 
- **Monson** — repo has 3, CivicPatch has 3, 0 matched (same situation as
  Milton — likely a formatting-only mismatch, not a roster gap; verify before
  treating as missing data)
  - https://www.monson-ma.gov/381/Select-Board
- **Pembroke** — repo has 5, CivicPatch has 5, only 1 matched
  - https://www.pembroke-ma.gov/1762/Select-Board
- **Rehoboth** — repo has 2, CivicPatch has 5
  - https://www.rehobothma.gov/town-administrator-board-selectmen-personnel
- **Rowley** — repo has 3, CivicPatch has 6
  - https://www.townofrowley.net/board-selectmen
- **Sandisfield** — repo has 2, CivicPatch has 4
  - https://www.sandisfieldma.gov/select-board

Hardwick, Lee, Rehoboth, Rowley, and Sandisfield look like genuine
under-coverage (repo seat count is short of CivicPatch's). Milton and Monson
need a closer manual look before concluding anything — they may turn out to
be Finding 2's formatting-noise pattern rather than an actual gap.

## Case studies from the initial 3-town spot check (Oak Bluffs, Norton, Falmouth)

- **Oak Bluffs**: clean match. Select Board's 5 names (Alley, Cleary,
  DeBettencourt, Green-Beach, Leonard) are identical in both datasets.
- **Norton**: structure exists (8 offices, Select Board included) but zero
  officeholders anywhere in the repo — one of the 73 in Finding 1. Confirmed
  the 5 CivicPatch names (Luciano, O'Neil, Rich, Marsan, Kimball) don't
  appear elsewhere in the repo under a different town; two similarly-named
  people that do exist in the repo (Robert Kimball, Ronald Marsan) are
  confirmed different people in Whitman and Methuen.
- **Falmouth**: a structural gap, not just a holder gap. The repo has only 2
  offices total for Falmouth (Moderator, Town Clerk) — no Select Board
  organization exists at all, versus CivicPatch's 5-member Select Board plus
  Moderator. Traces to the original `v20` import and was never revisited by
  a later batch. Falmouth (~32k population) almost certainly has more
  elected offices than these two (School Committee, Library Trustees,
  Housing Authority are typical for a town this size).

## A format difference worth normalizing eventually (not a data error)

CivicPatch's `jurisdiction_ocdid` includes the county component
(`ocd-jurisdiction/country:us/state:ma/county:bristol/place:norton/government`);
this repo's `jurisdiction_id` omits it
(`ocd-jurisdiction/country:us/state:ma/place:norton/government`). Both
resolve to the same jurisdiction, but the ID strings won't match directly
without stripping the county segment first.

## Files in this directory

- `ma_town_overview_2026-08-26.csv` — one row per comparable town: earliest
  repo batch, repo org/holder counts, CivicPatch row/name counts.
- `ma_execboard_name_diff_2026-08-26.csv` — one row per comparable town:
  repo vs. CivicPatch holder counts for the executive body, and the specific
  names that didn't match on either side.
