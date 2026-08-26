# Massachusetts Municipal Charter / Elected-Office Audit — Peru One-Off Gap Repair

Generated: 2026-08-26
Version: `peru-oneoff`
Intended baseline: saved **v32** checkpoint (Paxton, Peabody, Pelham, Pembroke, Pepperell)
Gap location: **Peru**, alphabetically between Pepperell and the v33 batch beginning Petersham

## Batch counts
- Municipalities researched: **1**
- Elected-office research rows: **9**
- Schema-ready office rows / Posts: **8**
- Research-only unresolved structure rows: **1**
- Current-officeholder research rows: **22**
- Verified current role holders: **22**
- Explicit vacancies: **0**
- Unresolved holder markers: **0**
- Schema-ready Persons: **15**
- Schema-ready Memberships: **21**

## Schema-ready direct-voter offices
1. Select Board — 3 seats, 3-year staggered terms
2. Town Clerk — 1 seat, 3-year term
3. Finance Committee — 5 seats, 3-year staggered terms
4. Planning Board — 5 seats, 5-year staggered terms
5. Board of Health — 3 seats, 3-year staggered terms
6. Constables — 2 seats, 2-year staggered terms
7. Moderator — 1 seat, **1-year term** (newer 2025 election-specific notice controls over stale 3-year annual-report heading)
8. Central Berkshire Regional School Committee — 1 Peru-allocated direct-voter seat, 4-year term

## Research-only conflict
**Tree Warden** is deliberately **not schema-ready**. Older official election results and the current Town “Officials: Elected & Appointed” page classify the office as elected. The 2024-2025 annual report instead lists Tree Warden under appointed positions, and the June 2025 annual-election candidate notice does not include it. Justin Russell is preserved as the current role holder, but no elected Post, Person, or Membership is generated from this row until the classification is resolved.

## Current holder coverage
Current Town/CBRSD pages support full holder coverage for the eight schema-ready offices: **21 serialized Memberships across 15 unique Persons**. A 22nd research-layer holder row preserves Justin Russell as current Tree Warden without asserting election status.

## Primary/current sources
- Town home: https://townofperuma.com/
- Current elected/appointed classification page: https://townofperuma.com/officials-elected-appointed/
- 2024-2025 Annual Town Report: https://files.heygov.com/townofperuma.com/Annual%20Town%20Report%202024-2025.pdf
- Elections & Town Meetings archive: https://townofperuma.com/voting-elections/
- June 14, 2025 Annual Town Election candidate notice: https://www.townofperuma.com/node/19351
- Select Board: https://www.townofperuma.com/select-board/
- Town Clerk: https://www.townofperuma.com/town-clerk/
- Finance Committee: https://www.townofperuma.com/finance-committee/
- Planning Board: https://www.townofperuma.com/planning-board/
- Board of Health: https://townofperuma.com/board-of-health/
- Town contacts directory (Constables, Moderator, Tree Warden): https://www.townofperuma.com/contacts-directory/
- Central Berkshire Regional School Committee members: https://www.cbrsd.org/school-committee/members
- General bylaws: https://www.townofperuma.com/town-clerk/files/general-bylaws

## Validation
Organization manual checks, Post schema, Person schema, Membership schema, referential-integrity checks, and duplicate-ID checks all return **zero errors** for serialized records.

## Application note
This is a **gap-repair overlay**, not a replacement for v32 or v33. Applying it to the exact saved v32 checkpoint would move that checkpoint from 225 to **226 municipalities with local findings**, while preserving the original v32/v33 artifacts unchanged. Later statewide cumulative counters should be reconciled separately because the historic rolling series had additional duplicate/reprocessed-town corrections.
