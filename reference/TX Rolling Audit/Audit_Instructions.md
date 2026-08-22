You are conducting a **Texas elected-office structure research project** for CivicMirror. Tracking issue: #10.

## Primary Objective

Complete a statewide audit to determine every elected office across Texas's local governing entities, and identify the people **currently holding** those elected seats, producing a machine-readable dataset compatible with the supplied CivicMirror schemas.

**Scope for this audit:**

- Counties (254)
- Municipalities — general-law (Type A/B/C) and home-rule (1,225 total)
- Independent school districts (ISDs, ~1,207)
- Public community/junior college districts (~50)
- Special districts other than Municipal Utility Districts (ESDs, hospital districts, groundwater/water districts, etc.)

**Explicitly out of scope: Municipal Utility Districts (MUDs).** MUDs are tracked separately under issue #11 and must not be folded into this audit's inventory, coverage, or ZIP artifacts.

---

# How Texas Differs From the MA Audit

The Massachusetts audit (`reference/MA Rolling Audit/`) is **charter-first**: every town's office set had to be individually determined, because MA charters and special acts routinely override the general-law default, and nothing about a municipality's office structure could be assumed from its size or type.

Texas is substantially **statute-first**. For most entities in scope, office structure is fixed by state law based on a classification determination, not by an individually negotiated charter:

- **General-law cities** (Type A, B, or C under the Local Government Code) have office structure fixed by statute for their type. Once a city's type is known, its office set is templated, not individually researched.
- **Home-rule cities** (population-eligible cities that have adopted a home-rule charter) set their own structure, same as MA — these require individual charter reads.
- **ISDs** have trustee-board structure set by the Education Code (7-member board is the common default), with exceptions where a district operates under a single-member-district or hybrid election plan (often the result of a Voting Rights Act settlement or lawsuit).
- **Community college districts** follow a similar templated pattern to ISDs.
- **Special districts** are created and structured by their individual enabling legislation (a special act or a general enabling chapter), which varies by district type; many special-district boards are appointed rather than elected and must not be assumed elected by default.

**Practical consequence:** this audit should run as *classify-then-template*, not *read-every-entity's-founding-document*. The individual-document-read effort concentrates on home-rule cities, ISDs/community colleges with non-default election plans, and special districts — not on the ~850 general-law cities or the ~1,200 ISDs using the statutory default.

Do not assume a classification without a source. "This city looks small, so it's probably general-law Type A" is not acceptable — confirm the classification from an authoritative source before templating.

---

# Jurisdiction / Office ID Collisions — Read Before Minting Any ID

Unlike Massachusetts, Texas has substantial name overlap between different entity layers operating over the same or overlapping geography:

- **County vs. municipality:** at least 85 name collisions exist between `data/us/tx/jurisdictions/county/*-government.yaml` and `data/us/tx/jurisdictions/municipal/*-government.yaml` (e.g. Anderson County and the City of Anderson). The seeded jurisdiction IDs already disambiguate these via `county:` vs. `place:` in the OCD ID (`ocd-jurisdiction/country:us/state:tx/county:anderson/government` vs. `.../place:anderson/government`), but a bare `<slug>-tx/<office-slug>` office-ID convention (mirroring MA's `<slug>-ma/<office-slug>`) does **not** disambiguate and must not be used as-is.
- **ISDs and community college districts** frequently share a name with a city or county without matching its boundary (e.g. an ISD that serves parts of several municipalities), and are not guaranteed to be collision-free against county or municipal slugs either.

**Before generating any schema-ready Office or Post ID for this audit, confirm the ID convention includes an entity-type qualifier** (e.g. `<slug>-tx-county/<office-slug>`, `<slug>-tx-place/<office-slug>`, `<slug>-tx-isd/<office-slug>`) that mirrors the `county:`/`place:` distinction already present in the seeded jurisdiction IDs. Do not mint IDs against the existing 85+ known collisions using an unqualified slug.

Office IDs must key to jurisdiction IDs already seeded from the 2022 Census of Governments (GUS) data under `data/us/tx/jurisdictions/{county,municipal,federal}/`. Do not mint new jurisdiction slugs during office research — if an entity in scope (ISD, community college district, special district) has no seeded jurisdiction file yet, that is a prerequisite gap to flag, not something to work around informally.

---

# Research Question for Each Entity

Research two linked questions for each entity in scope:

> 1. What positions can voters of this entity actually elect (under the Constitution, statute, charter, enabling legislation, or election plan that controls it)?
> 2. Who currently occupies each of those elected offices or seats, as of the research/retrieval date?

Question 1 (office structure) is the controlling determination; question 2 (current officeholders) is researched in the same workflow, same as the MA audit.

## Counties

Structure is set by the Texas Constitution and is close to uniform statewide:

- County Judge
- Commissioners Court (4 commissioners, by precinct)
- Sheriff
- County and/or District Clerk
- County Tax Assessor-Collector
- County Attorney and/or District Attorney
- County Treasurer
- Justices of the Peace, Constables (by precinct)

Texas county elections are **partisan** — unlike MA municipal elections, which are nonpartisan. Record party affiliation where the official source supports it.

Watch for **contract/urban counties** (e.g. Harris, Bexar, Dallas, Tarrant) that carry additional statutorily-created offices not present in most counties. Verify rather than assume the baseline list applies unmodified.

## Municipalities

First determine classification for every municipality before researching office structure:

- **General-law Type A, B, or C** — office structure comes from the Local Government Code provisions for that type. Confirm the type from an authoritative source (Texas Municipal League, Texas Comptroller, or the city's own official designation) before templating the office set.
- **Home-rule** — city has adopted a home-rule charter (population-eligible, generally 5,000+, though many eligible cities remain general-law by choice). Office structure must be individually sourced from the current charter, same discipline as the MA audit: do not assume a common office (mayor, council seats, at-large vs. district) without confirming against the charter text.

Do not assume a city's type from population alone — some population-eligible cities have not adopted home-rule; confirm the designation itself, not just the theoretical eligibility.

## Independent School Districts (ISDs)

Default structure is a 7-member elected Board of Trustees under the Education Code. Before templating, confirm whether the district operates under:

- the statutory default (at-large or district-based per its standard election order), or
- a modified single-member-district or hybrid plan, often adopted following a Voting Rights Act challenge or settlement — these require individual sourcing of the current election order/plan, not the statutory default.

ISD boundaries do not follow municipal or county boundaries. An ISD serving parts of multiple cities/counties is not an error — record it as such.

## Community College Districts

Same treatment as ISDs: confirm board size and structure from the district's enabling statute/election order rather than assuming a fixed number.

## Special Districts (excluding MUDs)

Covers entities such as Emergency Services Districts (ESDs), hospital districts, groundwater conservation districts, and similar special-purpose governments — **not** Municipal Utility Districts (see issue #11).

Do not assume a special district's board is elected. Many special-district boards (including many ESDs) are appointed by a county commissioners court or another appointing authority under their enabling legislation, not elected by district voters. Confirm elected vs. appointed status per entity before creating any elected-office record; when a district's board is appointed, record it as an appointed exclusion (see below), not as an elected office.

---

# Source Priority

Prefer authoritative sources in roughly this order:

1. Texas Constitution and Texas statutes (Local Government Code, Election Code, Education Code, Health and Safety Code, Water Code) as applicable to the entity type
2. The entity's own current charter, election order, or governing enabling legislation
3. Official entity website (county, city, ISD, district)
4. Texas Secretary of State (elections administration, county/city classification data)
5. Texas Education Agency (TEA) — for ISD enumeration and classification
6. Texas Comptroller of Public Accounts — Special Purpose District Public Information Database, for special-district enumeration
7. Texas Association of Counties — for county-office supporting detail
8. Texas Municipal League (including `directory.tml.org`) — useful for locating official city sites and contacts for TML-member cities; it is a member directory, not a comprehensive statutory roster, and does not itself control an elected/appointed determination
9. Legislative Reference Library of Texas — for locating a special district's enabling act

Avoid relying on:

- Ballotpedia
- Wikipedia (including the "List of municipalities in Texas" page referenced in issue #10 — useful only as a non-authoritative starting enumeration, not as a structure or officeholder source)
- generic civic directories
- campaign websites
- unofficial election aggregators
- search-result snippets without checking the underlying source

Secondary sources may help locate primary sources but should not control an elected/appointed or structure determination.

## Current-Officeholder Sources

For identifying who currently holds an elected seat, begin with the entity's official website (save the URL if not already preserved), then prefer in order:

1. official current elected-official directory
2. official board/commissioners-court/trustees roster
3. official county/city/ISD clerk or secretary roster
4. official current election results plus legally established term information when needed to reconcile a roster

Record the exact source URL and retrieval/as-of date for every material current-officeholder claim, same discipline as the MA audit.

---

# Charter/Statute Overrides Are Still Critical

Even though most of this audit is statute-templated, do not assume the template applies unmodified:

- A home-rule city's charter always controls over the general-law default, by definition.
- An ISD or community college district's adopted election plan may override the statutory default board size or structure.
- A special district's enabling act may create a structure that departs from the type's typical pattern.

Capture negative findings (an office assumed elected but confirmed appointed) in an appointed-exclusions dataset with:

- entity
- office/body
- status = appointed
- controlling source URL
- explanatory note

---

# Required Office Data

For every elected office attempt to determine:

- entity (county / municipality / ISD / community college district / special district)
- stable `office_id` (using the type-qualified convention described above)
- standardized role
- local title
- elected = true
- number of elected seats
- seat structure: at-large / precinct / ward / district / mixed
- term length
- staggered terms
- partisan status (note: Texas counties are partisan; most municipalities, ISDs, and special districts are nonpartisan — do not assume, confirm per entity type)
- legal source URL (statute, charter, election order, or enabling act)
- election administration/creation URL
- election results URL
- verification status
- notes

---

# Texas Office ID Convention

Use stable, type-qualified IDs in this form:

`<entity-slug>-tx-<entity-type>/<office-slug>`

Examples:

`anderson-tx-county/county-judge`

`anderson-tx-place/mayor`

(distinguishing Anderson County from the City of Anderson)

`houston-tx-isd/trustee-district-3`

Do not create IDs based on the current officeholder. Do not reuse an unqualified `<slug>-tx/...` form given the known county/municipality collisions.

---

# `office.schema.json` Rule

The supplied `office.schema.json` requires `id`, `role`, and `seats`, and `seats` must be at least 1.

Maintain two layers, same as the MA audit:

## Research inventory

May contain `seats = null` when elected status is established but seat count is still unresolved.

## Schema-ready Office records

Only generate an `Office` object when a positive seat count has been established. Never invent a seat count to satisfy the schema.

---

# Conflicting Sources

Do not silently resolve conflicts. If statute and an entity's current election materials disagree (e.g. a general-law type's statutory seat count vs. a city's actual current roster), preserve the conflict and flag it rather than picking one, same discipline as the MA audit.

---

# Research Workflow

Work through unresolved entities in batches, grouped by phase rather than mixed:

1. **Phase 0 — ID convention.** Confirm/implement the type-qualified office-ID convention before any batch mints IDs.
2. **Phase 1 — Counties (254).** Template from the Constitution; verify contract/urban-county exceptions.
3. **Phase 2 — Municipalities.**
   - 2a: Classify all 1,225 as general-law (A/B/C) or home-rule, sourced (not assumed from population).
   - 2b: Template general-law cities from the Local Government Code by type; spot-verify a sample per type.
   - 2c: Individually research home-rule cities (~370) from their current charters, MA-style, in batches.
4. **Phase 3 — ISDs (~1,207).** Template from the Education Code default; individually verify and source districts with non-default (single-member/hybrid) election plans.
5. **Phase 4 — Community college districts (~50).** Same treatment as ISDs.
6. **Phase 5 — Special districts excluding MUDs.** Enumerate from the Comptroller's Special Purpose District database; confirm elected vs. appointed status per entity before creating any office record.

Within each phase:

1. Read the current coverage/inventory files for that phase.
2. Select unresolved entities and/or entities needing officeholder backfill.
3. Verify the official entity website.
4. Research authoritative sources for office structure (statute/charter/election order/enabling act as applicable).
5. Research current holders for every elected office found.
6. Add elected-office rows.
7. Add appointed exclusions and vacancy/officeholder notes.
8. Update the source audit.
9. Generate schema-ready Office records and schema-ready Person records.
10. Validate against `office.schema.json` and `person.schema.json`.
11. Update the phase's coverage ledger.
12. Rebuild the ZIP after every meaningful batch.
13. Confirm files actually exist before reporting completion.

Do not perform an entire phase entirely in memory before saving. **Persist every batch.**

---

# Required Rolling Artifacts

Maintain the same artifact set as the MA audit, scoped per phase and clearly excluding MUDs:

- `tx_elected_office_inventory_rolling.json` / `.csv` — one row per entity × elected office
- `tx_schema_ready_offices_rolling.json` — valid `office.schema.json` records only
- `tx_current_officeholders_rolling.json` / `.csv`
- `tx_schema_ready_persons_rolling.json`, and `tx_schema_ready_memberships_rolling.json` if memberships are produced
- `tx_source_audit_rolling.csv` (and JSON)
- `tx_appointed_exclusions_rolling.csv`
- `tx_coverage_status_rolling.json` — must track each in-scope phase (counties, municipalities, ISDs, community colleges, non-MUD special districts) separately, and must not include MUDs
- `tx_validation_report_rolling.json`
- `tx_audit_rolling.zip` — rebuilt after every meaningful batch, containing all rolling files and supplied schemas

---

# Completion Standard

An entity should only be considered audit-complete when reasonable research has established:

1. governing form / classification (county / general-law type / home-rule / ISD default or modified plan / special-district type)
2. controlling statute/charter/election order/enabling act
3. complete elected-office inventory
4. meaningful appointed-office exclusions
5. seat counts
6. term structure
7. district/ward/at-large/precinct structure
8. election administration source
9. results source
10. unresolved conflicts documented

Officeholder coverage is tracked as a separate dimension from structure completeness, same as the MA audit.

---

# Current Officeholders, Incumbency, Person Identity

Follow the same discipline as the MA audit (`reference/MA Rolling Audit/Audit_Instructions.md`) for:

- not assuming the latest election winner is still the incumbent
- recording `how_seated` (elected / appointed / succeeded / acting) accurately, including elected offices currently filled by vacancy-appointment
- not creating a separate elected office for internally-selected board leadership (Chair, Vice Chair, etc.) unless voters separately elect that position
- deduplicating people using stable IDs, never regenerating an existing person's ID
- seat reconciliation: comparing expected elected seats to verified current holders, and not treating a shortage of names as proof of vacancy without an explicit official source

---

# Source Discipline

For every material elected/appointed claim, save the supporting URL. Whenever possible, capture the specific statutory citation in notes, for example:

- Local Government Code §22.031 (Type A general-law city)
- Education Code §11.052 (ISD trustee elections)
- City Charter Art. III §2
- Special District enabling act citation

Never manufacture a statutory or charter citation.

---

# Research Style

Be conservative, same as the MA audit.

Preferred:

> Elected status verified; seat count unresolved.

Not acceptable:

> This is probably a 5-member board.

Preferred:

> Statute sets 5-member Type A board; district's current official roster shows 4 seated with 1 vacancy noted on the city website.

Not acceptable:

> Used the statutory number without checking the current roster.

---

# Progress Reporting

After each persisted batch, report per phase:

- entities researched for structure in the batch
- entities backfilled for current holders in the batch
- total entities with structure research, per phase
- total office rows
- schema-ready Office records
- verified current-officeholder records
- schema-ready Person records
- known vacancies / unresolved seats
- validation success (Office and Person)
- remaining structure entities, per phase
- remaining officeholder-backfill entities
- significant statutory, charter, roster, vacancy, or identity conflicts

Always provide actual downloadable artifacts when available. Do not merely mention hypothetical sandbox filenames. Before presenting a download link, verify the file actually exists.

---

# Current Starting Point

No prior checkpoint exists for this audit. Begin with **Phase 0** (confirm the type-qualified office-ID convention against the existing 85+ county/municipal slug collisions) before minting any IDs, then proceed to **Phase 1 (Counties)**.

MUDs are out of scope for this audit — see issue #11.

The overall goal is a fully sourced, legally defensible, machine-readable map of every elected office across Texas's counties, municipalities, ISDs, community college districts, and non-MUD special districts — and the people currently holding those elected seats — suitable for CivicMirror election creation and results ingestion.
