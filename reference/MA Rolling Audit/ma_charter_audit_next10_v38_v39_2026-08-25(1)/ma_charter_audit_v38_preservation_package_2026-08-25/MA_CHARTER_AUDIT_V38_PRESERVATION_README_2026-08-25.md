# Massachusetts Municipal Charter / Elected-Office Audit — v38 Preservation Overlay

Generated: 2026-08-25
Version: v38
Baseline: saved v37 checkpoint
Batch: Salisbury, Sandisfield, Sandwich, Saugus, Savoy

## Batch counts
- Municipalities researched: **5**
- Elected-office research rows: **37**
- Schema-ready office rows / Posts: **36**
- Unresolved structure rows: **1**
- Current-officeholder research rows: **166**
- Verified current officeholders: **51**
- Explicit vacancies: **0**
- Unresolved holder markers: **115**
- Schema-ready Persons: **50**
- Schema-ready Memberships: **51**

## Projected cumulative after applying to v37
- Municipalities with local findings: **255 / 351**
- Remaining without preserved structure research: **96**
- Office research rows: **2072**
- Schema-ready inventory rows: **1720**
- Organizations / Posts: **1718 / 1718**
- Current-officeholder research rows: **5944**
- Persons / Memberships: **3673 / 3726**

## Significant findings
- **Salisbury:** Planning Board is explicitly appointed; Triton regional representation is kept distinct from town boards.
- **Sandisfield:** Official roster is authoritative for structure, but seats expiring May 2026 are unresolved unless post-election evidence safely identifies the holder.
- **Sandwich:** Historical official material proves two elected Sandwich representatives, but current term/cycle evidence is insufficient; the research row is withheld from schema serialization.
- **Saugus:** Fifty Town Meeting seats are direct-voter elected; Moderator is elected by those Town Meeting Members and is therefore excluded from the direct-voter Post inventory.
- **Savoy:** 2026 ballot positions establish structure, while several current member identities remain unresolved rather than inferred from pre-election lists.

## Validation
- Organization validation errors: **0**
- Post schema errors: **0**
- Person schema errors: **0**
- Membership schema errors: **0**
- Referential-integrity errors: **0**
- Duplicate-ID errors: **0**

Apply this overlay to the exact saved v37 checkpoint and rerun whole-package validation after materializing the cumulative rolling files.
