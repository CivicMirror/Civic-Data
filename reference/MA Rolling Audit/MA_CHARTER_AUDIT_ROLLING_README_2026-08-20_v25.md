# Massachusetts Municipal Charter / Elected-Office Audit — Rolling Preservation

Generated: 2026-08-20
Version: v25

- Municipalities with local elected-office findings: **190 / 351**
- Elected-office research rows: **1477**
- Explicitly schema-ready inventory rows: **1152**
- Schema-ready Organizations: **1153**
- Schema-ready Posts: **1153**
- Schema-ready Persons: **2051**
- Schema-ready Memberships: **2071**
- Schema validation / referential-integrity errors: **0**
- Municipalities remaining without preserved local office research: **161**
- Latest batch verified current officeholders: **138**
- Latest batch explicit vacancies: **2**
- Latest batch unresolved officeholder markers: **449**
- Total current-officeholder research rows: **3210**

Latest batch: **Milton, Monroe, Monson, Montague, Monterey**.

## Batch notes

- **Milton:** 14 elected Posts / 328 elected seats are preserved, including **279 Representative Town Meeting members**. Forty-eight named holders are verified; one Library Trustee seat is explicitly vacant after a May 2026 resignation; all 279 Town Meeting member slots remain holder-unresolved pending complete roster reconciliation.
- **Monroe:** 9 elected Posts / 19 elected seats are preserved. Mass.gov confirms Monroe has no municipal website, so successive election reporting is used with the source limitation explicitly preserved. Fourteen current holders are verified, one Library Trustee seat is explicitly vacant, and four seats remain unresolved.
- **Monson:** 11 elected Posts / 30 elected seats are preserved. **Acts of 2026, c.69** controls the expanded five-member Select Board structure; three incumbents are verified and two transition seats remain unresolved rather than being inferred vacant.
- **Montague:** 11 elected Posts / 164 elected seats are preserved, including **126 Representative Town Meeting members**. Town Clerk, Treasurer/Tax Collector, and Tree Warden are preserved as appointed exclusions. Twenty-nine named current holders are verified and 135 seats remain unresolved, mostly Town Meeting.
- **Monterey:** 15 elected Posts / 48 elected seats are preserved. Nineteen current holders are conservatively verified; 29 remain unresolved because the complete post-2026 official result attachment could not be fully retrieved. Town Clerk and the Planning Board associate are excluded as non-elected.
- Open Town Meeting voters in Monroe, Monson, and Monterey are not modeled as elected offices.
- The all-351 `ma_351_charter_coverage_status_rolling.json` file is not present in the supplied workspace and was not fabricated.
- `scripts/validate.py` is not present in the supplied workspace; validation uses the supplied CivicMirror JSON schemas plus referential-integrity checks.

## Serialization

This checkpoint continues the CivicMirror **Organization / Post / Person / Membership** model. Existing v24 IDs are preserved unchanged. New v25 entity IDs use the deterministic UUIDv5 namespace established in v23.
