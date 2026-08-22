# Massachusetts Municipal Charter / Elected-Office Audit — Rolling Preservation

Generated: 2026-08-21
Version: v26

- Municipalities with local elected-office findings: **195 / 351**
- Elected-office research rows: **1525**
- Explicitly schema-ready inventory rows: **1194**
- Schema-ready Organizations / Posts: **1192 / 1192**
- Schema-ready Persons / Memberships: **2139 / 2162**
- Schema and referential-integrity errors: **0**
- Municipalities remaining without preserved local office research: **156**
- Latest batch verified current officeholders: **104**
- Latest batch explicit vacancies: **1**
- Latest batch unresolved officeholder markers: **460**

Latest batch: **Nantucket, Natick, Needham, New Bedford, New Braintree**.

## Important limitations

- Nantucket and New Braintree preserve several elected offices with unresolved total seat counts; those rows are research-only.
- Natick and Needham representative Town Meeting rosters were found but were not fully transcribed; unresolved markers preserve the seat shortfall without implying vacancies.
- New Bedford's accessible official council roster conflicts with later election reporting for two seats; those seats remain unresolved.
- New Braintree's Treasurer/Tax Collector structure and several possible elective boards require further controlling-law research.
- The all-351 coverage JSON remains absent and was not fabricated.

## Serialization

Existing v25 IDs are preserved. Because v25 named but did not record the v23 UUID namespace, v26 records an explicit deterministic namespace in `build_v26.py` for all new Organization, Person, and Membership IDs.
