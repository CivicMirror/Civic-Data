# TX special-district jurisdiction type-key registry

Tracks issue #32 (and #15/#28's related special-district work). Each row is a
canonical `<type_key>` for the `ocd-division/country:us/state:tx/<type_key>:<slug>`
/ `ocd-jurisdiction/country:us/state:tx/<type_key>:<slug>/<classification>` ID
pattern used when a district doesn't map 1:1 onto an existing county/place
jurisdiction (mirrors the `school_district:` and `appraisal_district:`
precedent already in the repo — see `docs/GLOSSARY.md`).

**Naming rule**: full snake_case words, noise words (`and`, `of`, etc.)
dropped, no abbreviations — e.g. "Water Control **and** Improvement District"
-> `water_control_improvement_district`, not `wcid`. Keeps the key
self-describing and portable to other states' audits, consistent with the
two type keys that already exist in this repo.

`jurisdiction.classification` is a **fixed schema enum**
(`government, legislature, executive, judiciary, school, park, sewer, forest,
transit_authority` — inherited from the original OpenStates project this
schema descends from). Several entity types below don't have a clean fit;
those are flagged rather than forced into the wrong bucket.

| Type key | Statutory name | Enabling chapter | Elected? (Phase 0) | classification | Status |
|---|---|---|---|---|---|
| `water_control_improvement_district` | Water Control and Improvement District (WCID) | Water Code Ch. 51 | Elected | `sewer` | **In progress** — first type minted under #32 |
| `special_utility_district` | Special Utility District (SUD) | Water Code Ch. 65 | Elected | `sewer` | **Jurisdiction-only, in progress** — 54 of 66 raw rows seeded; board size is 5-11 directors set per-district (Sec. 65.101/65.103), not a fixed number, so no Organization/Post records yet pending individual board-size research. 9 rows held back on the name-vs-Entity-Type check (see `scripts/seed_tx_sud_jurisdictions.py`), including a River Authority misfiled under this type. |
| `fresh_water_supply_district` | Fresh Water Supply District (FWSD) | Water Code Ch. 53 | Elected | `sewer` | **Done (structure)** — 58 of 60 raw rows seeded (jurisdiction + board + 5 director posts each, board fixed at 5 per Sec. 53.062, no override clause). 2 rows held back on the name-vs-Entity-Type check (a MUD misfiled under this type, and a plain "Water Supply District" not assumed to be Ch. 53). No officeholders yet. |
| `water_improvement_district` | Water Improvement District (WID) | Water Code Ch. 55 | Elected | `sewer` | **Done (structure, curated)** — only 5 of 22 raw rows cleanly matched this type by name (board fixed at 5 per Sec. 55.101); the rest were excluded/held back individually (one non-government garbage row, several no-"water"-token ambiguous names, a resolved 3-way Comal County duplicate cluster, a dissolved predecessor entity). 2 further rows tagged this Entity Type but named as WCID were reclassified into `water_control_improvement_district:` instead (`scripts/seed_tx_wcid_reclassified_from_wid.py`). See `scripts/seed_tx_wid_jurisdictions_orgs_posts.py` for full per-row reasoning. |
| `irrigation_district` | Irrigation District | Water Code Ch. 58 | Elected | `sewer` | Not started |
| `groundwater_conservation_district` | Groundwater Conservation District (GCD) | Water Code Ch. 36 | Elected (many individual GCDs override to appointed by special act — verify per district) | `sewer` | Not started |
| `drainage_district` | Drainage District | Water Code Ch. 56 | Elected by default; special law can make appointment permanent | `sewer` | Not started |
| `underground_water_conservation_district` | Underground Water Conservation District | Water Code (legacy Ch. 52, largely superseded by Ch. 36) | Likely elected, legacy/grandfather districts — verify | `sewer` | Not started |
| `levee_improvement_district` | Levee Improvement District (LID) | Water Code Ch. 57 | Appointed by default (3 directors); converts to elected (5 directors) on petition of 100 electors | `sewer` | Not started |
| `hospital_district` | Hospital District | Health & Safety Code Ch. 286 (many individual districts instead under Ch. 281-285 or a special act — confirm which governs) | Elected (Ch. 286 default) | `government` — no health-specific enum value exists; flag if a schema PR to add one is ever worth it | Not started |
| `emergency_services_district` | Emergency Services District (ESD) | Health & Safety Code Ch. 775 | Appointed by default; **elected** if population > 3,000,000 or district spans more than one county | `government` — no fire/emergency-specific enum value exists | Not started |
| `municipal_management_district` | Municipal Management District (MMD) | Local Gov't Code Ch. 375 | Appointed by default (TCEQ appoints initial board; typically self-perpetuating per district-specific special act) | `government` | Not started |
| `municipal_development_district` | Municipal Development District (MDD) | Local Gov't Code Ch. 377 | Appointed (municipality appoints board) | `government` | Not started |
| `crime_control_prevention_district` | Crime Control and Prevention District | Local Gov't Code Ch. 363 | Appointed (county/municipality governing body appoints board) | `government` | Not started |
| `library_district` | Library District | Local Gov't Code Ch. 326 (single-jurisdiction, elected) or Ch. 336 (multi-jurisdictional, appointed) | Mixed — depends which chapter created the specific district | `government` — no library-specific enum value exists | Not started |
| `navigation_district` | Navigation District | Water Code Ch. 60-63 | **Under individual research** (no safe general-chapter default; see issue #32 comments) | Needs a new enum value — `transit_authority` is a poor fit (covers port/transit function only, not full district governance) | User researching directly |
| `river_authority` | River Authority | No general chapter — each created by individual special act | **Under individual research** (no safe general-chapter default; see issue #32 comments) | Needs a new enum value — none of the existing 9 fit a multi-purpose river/water-resource authority | User researching directly |

## Types confirmed out of scope (no entry needed)

- **Soil and Water Conservation District** — closed #27, landowner-only franchise, not general-public election (see `docs/GLOSSARY.md`-adjacent memory `tx_audit_general_public_election_scope`).
- **Public Improvement District (PID)** — no separate board exists; governed directly by the creating municipality/county's own governing body (Local Gov't Code Ch. 372).
- **Road District** (general-law type) — governed ex officio by the county judge/commissioners court; not a distinct elected office.
- **Appraisal District** — already uses `appraisal_district:` (tracked under #28, folded into county jurisdiction files except Potter/Randall).
- **Tax Increment Reinvestment Zone, Public Housing Authority/Agency, Public Utility Agency** — appointed under general statutory knowledge, not yet verified against chapter text (see #32 Phase 0 comment) — no type key reserved until confirmed in scope.

## When adding a new type

1. Confirm elected-vs-appointed against the actual enabling statute (not general knowledge) — see `tx_audit_general_public_election_scope` and `feedback_verify_elected_status_claims` memories.
2. Confirm the ongoing director/board *election* (not just the creation petition) is open to general-public qualified voters, not a restricted franchise — the #27 SWCD test.
3. Pick a full-word snake_case key per the naming rule above, add a row here before minting any jurisdiction file with it.
4. If no existing `classification` enum value fits, note that here and flag it rather than forcing a wrong fit — a schema change is a separate, deliberate decision.
