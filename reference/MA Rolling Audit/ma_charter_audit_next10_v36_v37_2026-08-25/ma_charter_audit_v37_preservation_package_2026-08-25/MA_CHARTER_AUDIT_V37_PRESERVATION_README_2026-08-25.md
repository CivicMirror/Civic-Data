# Massachusetts Municipal Charter / Elected-Office Audit — v37 Preservation Overlay

Generated: 2026-08-25
Version: v37
Baseline: saved v36 checkpoint
Batch: Rowley, Royalston, Russell, Rutland, Salem

## Batch counts
- Municipalities researched: **5**
- Elected-office research rows: **50**
- Schema-ready office rows / Posts: **49**
- Unresolved structure rows: **1**
- Current-officeholder research rows: **152**
- Verified current officeholders: **99**
- Explicit vacancies: **0**
- Unresolved holder markers: **53**
- Schema-ready Persons: **96**
- Schema-ready Memberships: **99**

## Projected cumulative after applying to v36
- Municipalities with local findings: **250 / 351**
- Remaining without preserved structure research: **101**
- Office research rows: **2035**
- Schema-ready inventory rows: **1684**
- Organizations / Posts: **1682 / 1682**
- Current-officeholder research rows: **5778**
- Persons / Memberships: **3623 / 3675**

## Significant findings
- **Rowley:** Housing state/tenant seats and Planning associate are excluded. Several 2026-expiring holders remain unresolved rather than stale-carried.
- **Royalston:** Three Royalston-designated Athol-Royalston school seats are modeled; Montachusett vocational representative is appointed.
- **Russell:** Constable complement is not fully resolved: 2023 ballot proves at least two simultaneous seats, but current exact total was not safely established; row is withheld from schema-ready serialization.
- **Rutland:** Board of Public Works is the Select Board serving in an ex-officio capacity, not a separate elected Post. Several 2026-expiring seats remain unresolved.
- **Salem:** Mayor is ex-officio School Committee chair; six separately voter-elected School Committee seats are serialized.

## Validation
- Organization validation errors: **0**
- Post schema errors: **0**
- Person schema errors: **0**
- Membership schema errors: **0**
- Referential-integrity errors: **0**
- Duplicate-ID errors: **0**

Apply this overlay to the exact saved v36 checkpoint and rerun whole-package validation after materializing cumulative rolling files.
