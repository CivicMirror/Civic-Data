# Massachusetts Municipal Charter / Elected-Office Audit — v31 Preservation Overlay

Generated: 2026-08-25
Version: v31
Baseline: authoritative persisted v30 File-Library checkpoint
Batch: Orange, Orleans, Otis, Oxford, Palmer

## Why this is an overlay

The authoritative v30 rolling files are persisted File-Library artifacts, but those references are not writable local sandbox files. This package therefore **does not pretend to contain a byte-for-byte full v30→v31 merge**. It preserves the complete v31 delta with stable IDs, source URLs, schema-ready Organization/Post/Person/Membership records, validation results, appointed exclusions, and a baseline manifest.

Apply the delta files in this package to the exact persisted v30 rolling checkpoint to materialize a full v31 rolling package.

## V31 batch counts

- Municipalities researched: **5**
- Elected-office research rows: **49**
- Schema-ready office rows / Posts: **46**
- Unresolved structure rows: **3**
- Current-officeholder research rows: **151**
- Verified current officeholders: **123**
- Explicit vacancies: **2**
- Unresolved holder markers: **26**
- Schema-ready Persons: **119**
- Schema-ready Memberships: **122**

## Projected cumulative counts after applying to v30

- Municipalities with local findings: **220 / 351**
- Municipalities remaining without preserved local office research: **131**
- Office research rows: **1748**
- Explicit schema-ready inventory rows: **1401**
- Organizations / Posts: **1399 / 1399**
- Current-officeholder research rows: **4526**
- Persons / Memberships: **2647 / 2684**

## Important batch findings

- **Orange:** Chapter 116 of the Acts of 2026 took effect July 1, 2026 and controls the elected-office inventory. Regional-school allocation, Soldiers' Memorial trustee composition, and total elected Constable count remain unresolved rather than guessed.
- **Orleans:** current official rosters support Select Board, Board of Health, Snow Library, Nauset Regional representatives, elementary School Committee, Housing Authority elected seats, and the Old King's Highway roster. A stale expired School Committee entry is excluded.
- **Otis:** current official pages distinguish elected and appointed seats clearly. The Library has three elected trustee seats plus four appointed trustees; one elected seat is explicitly vacant. Heather Gray is an appointed occupant of an elected Assessor seat and is encoded with `how_seated=appointed`.
- **Oxford:** six elected office groups are structure-ready and all 19 current elected-seat holders were reconciled in this batch. The Housing Authority model excludes its state-appointed and tenant seats.
- **Palmer:** the town charter offices are supplemented by separately elected fire/water district offices. District-specific uncertainties are preserved as review items rather than collapsed into the town government.

## Validation

Post, Person, and Membership delta records were validated against the supplied CivicMirror schemas. Organization IDs and cross-record references were also checked.

- Organization validation errors: **0**
- Post schema errors: **0**
- Person schema errors: **0**
- Membership schema errors: **0**
- Referential-integrity errors: **0**
- Duplicate-ID errors: **0**

## Application rule

1. Start from the exact persisted v30 checkpoint.
2. Append the v31 inventory/current-holder/source-audit/exclusion deltas to the corresponding v30 research layers.
3. Append the v31 Organization/Post/Person/Membership delta records to the corresponding v30 schema-ready layers.
4. Preserve v30 IDs unchanged.
5. Do not generate Posts for the three Orange rows whose seat count remains unresolved.
6. Re-run whole-package schema, duplicate-ID, and referential-integrity validation after materializing the full merge.
7. Rebuild the canonical rolling ZIP from the merged files.

The package manifest contains SHA-256 hashes for every file in this preservation package.
