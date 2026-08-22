You are continuing an existing **Massachusetts municipal election-structure research project** for CivicMirror.

## Primary Objective

Complete a **municipality-by-municipality audit of all 351 Massachusetts cities and towns** to determine every municipal office, seat, board, committee, commission, authority, or other position that is filled by **election**, and to identify the people **currently holding** those elected seats.

The governing charter, special act, municipal code, bylaws, district agreement, or other authoritative legal source should control the elected/appointed determination.

Office structure and current-officeholder coverage are tracked as **separate progress dimensions**. Office structure is the controlling determination; current-officeholder research is part of the same primary workflow, not a later phase.

The final goal is a machine-readable statewide municipal election-structure dataset — including current officeholders — compatible with the supplied CivicMirror schemas.

---

# Existing Project State

Use the supplied schemas and Files

**Do not restart the audit from municipality #1.**

First read the coverage-status file and inventory to determine which municipalities remain unresolved.

The persisted files are the source of truth for progress. Do not assume research mentioned only conversationally was saved unless it is present in those files.

---

# Research Question for Each Municipality

Research two linked questions for each municipality:

> 1. What positions can the voters of this municipality actually elect (under the charter, special act, bylaws, regional agreement, and other controlling law)?
> 2. Who currently occupies each of those elected offices or seats, as of the research/retrieval date?

Question 1 (office structure) is the controlling determination; question 2 (current officeholders) is researched in the same workflow. For question 1, this includes both obvious and unusual positions.

Examples include:

- Mayor
- City Council
- Aldermen
- Select Board / Board of Selectmen
- Moderator
- Town Clerk
- Treasurer
- Collector
- Treasurer-Collector
- Assessors
- Board of Health
- Planning Board
- School Committee
- Regional School Committee
- Library Trustees
- Housing Authority
- Redevelopment Authority
- Recreation / Park Commissioners
- Cemetery Commissioners
- Sewer Commissioners
- Water Commissioners
- Municipal Light Board
- Constables
- Tree Warden
- Finance Committee
- Commissioners of Trust Funds
- regional vocational-school representatives
- district officers
- representative Town Meeting members
- any other locally elected position

Do **not** assume that a common Massachusetts office is elected.

Many charters convert traditionally elected offices into appointed offices.

---

# Source Priority

Prefer authoritative sources in roughly this order:

1. Current municipal home-rule charter
2. Massachusetts Legislature special act
3. Current codified municipal charter/code
4. Municipal bylaws
5. Regional/district agreement
6. Official municipal clerk/election department
7. Official municipal board/committee page
8. Massachusetts Secretary of the Commonwealth
9. Massachusetts General Laws when local law has not modified the default
10. Massachusetts Municipal Association as supporting evidence

Avoid relying on:

- Ballotpedia
- Wikipedia
- generic civic directories
- campaign websites
- unofficial election aggregators
- search-result snippets without checking the underlying source

Secondary sources may help locate primary sources but should not control an elected/appointed determination.

## Current-Officeholder Sources

For identifying **who currently holds** an elected seat, begin with the municipality's official website (and save that URL if not already preserved), then prefer in order:

1. official current elected-official directory
2. official board/committee/commission roster
3. official mayor/council/select-board or department page
4. official town/city clerk roster
5. official regional/district website for regional bodies
6. official current election results plus legally established term information when needed to reconcile a roster

Secondary sources may help locate a page but should not control identity or current incumbency when an official source is available. Record the exact source URL and retrieval/as-of date for every material current-officeholder claim.

---

# Charter Overrides Are Critical

Massachusetts general law is only a baseline.

A local charter or special act may turn a normally elected office into an appointed one.

Example pattern:

A general-law town might normally elect assessors or a town clerk, but its charter may explicitly make those positions appointed.

In those cases:

**The local charter controls.**

Capture these negative findings.

Maintain an appointed-exclusions dataset containing fields such as:

- municipality
- office/body
- status = appointed
- controlling source URL
- explanatory note

This is necessary to prevent downstream systems from recreating false elected offices from Massachusetts general-law defaults.

---

# Representative Town Meeting Rules

Handle Town Meeting carefully.

## Open Town Meeting

Do **not** create elected offices for ordinary registered voters who attend Town Meeting.

Open Town Meeting voters are not elected representatives.

## Representative Town Meeting

Create an elected office for Town Meeting representatives.

Capture when possible:

- total elected representatives
- number of precincts
- members per precinct
- term length
- staggered structure
- ex-officio members separately from elected representative seats

Example:

If a Town Meeting consists of:

- 144 elected precinct representatives
- plus 5 Select Board members ex officio

then the elected Town Meeting office should have:

`seats = 144`

not 149.

---

# Housing Authorities and Similar Mixed Bodies

Be careful with Massachusetts authorities containing both elected and appointed members.

For example, a five-member Housing Authority may contain:

- 3 locally elected members
- 1 state-appointed member
- 1 tenant/resident-appointed member

The elected Office record should use:

`seats = 3`

Do not count appointed members as elected seats.

If the composition cannot be determined, preserve:

- elected status = verified
- seat count = unresolved

rather than guessing.

---

# Regional Bodies

Regional school districts, vocational school districts, water districts, fire districts, historic districts, and similar bodies require special handling.

Determine the number of seats elected **by or for that municipality**, not necessarily the total size of the regional body.

Example:

If a regional school committee has 11 total members but Town X elects 3 of them:

`seats = 3`

for Town X's office.

Use the regional agreement or authoritative local documentation whenever necessary.

---

# Required Office Data

For every elected office attempt to determine:

- municipality
- stable `office_id`
- standardized role
- local title
- elected = true
- number of elected seats
- seat structure:
  - at-large
  - ward
  - district
  - mixed
- term length
- staggered terms
- partisan status
- legal source URL
- election administration/creation URL
- election results URL
- verification status
- notes

Where useful, record ward, precinct, district, or seat allocation details in notes.

---

# CivicMirror Office ID Convention

Use stable IDs in this form:

`<municipality-slug>-ma/<office-slug>`

Examples:

`oxford-ma/select-board-member`

`boston-ma/mayor`

`arlington-ma/town-meeting-member`

Do not create IDs based on the current officeholder.

---

# `office.schema.json` Rule

The supplied `office.schema.json` requires:

- `id`
- `role`
- `seats`

and `seats` must be at least 1.

Therefore maintain two layers.

## Research inventory

May contain:

`seats = null`

when elected status is established but total seat count is still unresolved.

## Schema-ready Office records

Only generate an `Office` object when a positive seat count has been established.

Never invent a seat count just to satisfy the schema.

---

# Terms and Vacancies

Distinguish:

- regular term length
- temporary vacancy/unexpired term

Example ballot:

- Planning Board — 5 years
- Planning Board — 2 years

This usually means the regular office has a 5-year term and the 2-year contest is filling an unexpired term.

Store:

`term_years = 5`

for the stable Office definition.

Mention the temporary unexpired contest in notes if useful.

Do not redefine the office term as 2 years.

---

# Conflicting Sources

Do not silently resolve conflicts.

If two authoritative sources disagree, preserve the conflict.

Example:

- charter says 5-year term
- current election notice says 3-year term

Store the uncontested facts and note:

`term_years = unresolved`

with the conflict described.

Likewise, if an old charter says:

- 7 district councilors
- 2 at-large

but the current official roster shows:

- 3 district
- 6 at-large

retain:

- total seats = 9
- structure = mixed

and flag the allocation for amendment/revision research.

Search for amendments or special acts before leaving the conflict unresolved.

---

# Election Creation / Candidate Source

For each municipality identify the best authoritative source for creation of the election or identification of offices appearing on the ballot.

Useful sources include:

- annual town election notice
- warrant
- nomination-paper notice
- "offices on the ballot"
- specimen ballot
- city election calendar
- town clerk election page
- candidate list
- election warrant

Save the URL.

This source is particularly useful for CivicMirror's future pre-election ingestion.

---

# Election Results

Identify the strongest reusable results source.

Prefer:

1. official municipal election-results archive
2. town/city clerk certified results
3. official municipal PDF
4. Secretary of the Commonwealth where applicable

Record whether results are:

- HTML
- PDF
- downloadable file
- external election vendor
- state ElectionStats
- other

Do not assume a municipal results URL supports every historical election.

---

# Website / Site Intelligence

When encountered, also preserve useful pipeline information such as:

- official municipal website
- elections page
- elected-official directory
- results archive
- CMS platform
- election-results vendor
- document archive
- unusual URL patterns
- recurring ballot/result naming patterns

This may later populate `jurisdiction.site_intelligence`.

---

# Research Workflow

Work through unresolved municipalities in batches, **5 at a time**

For every batch:

1. Read the current coverage/inventory files.
2. Select unresolved-structure municipalities and/or municipalities needing officeholder backfill.
3. Verify the official municipal website.
4. Research authoritative sources for office structure.
5. Research current holders for every elected office found.
6. Add elected-office rows.
7. Add appointed exclusions and vacancy/officeholder notes.
8. Update the source audit.
9. Generate schema-ready Office records and schema-ready Person records.
10. Validate against `office.schema.json` and `person.schema.json`.
11. Update the separate structure and officeholder coverage ledgers.
12. Rebuild the ZIP (including officeholder/person files after meaningful batches).
13. Confirm files actually exist before reporting completion.

Do not perform 351 municipalities entirely in memory before saving.

**Persist every batch.**

This is extremely important because previous research sessions lost work when files were referenced in prose but never actually created.

---

# Required Rolling Artifacts

Maintain these files:

### Full research inventory

`ma_charter_elected_office_inventory_rolling.json`

and

`ma_charter_elected_office_inventory_rolling.csv`

One row/object per:

**municipality × elected office**

---

### Schema-ready offices

`ma_charter_schema_ready_offices_rolling.json`

Only records valid under `office.schema.json`.

---

### Current officeholders (research layer)

`ma_current_officeholders_rolling.json`

and

`ma_current_officeholders_rolling.csv`

One row/object per current officeholder (or per vacant/unresolved elected seat). This layer may represent unresolved or vacant seats **without** fabricating Person objects.

---

### Schema-ready persons

`ma_schema_ready_persons_rolling.json`

Only records valid under `person.schema.json`.

If memberships are produced, also maintain:

`ma_schema_ready_memberships_rolling.json`

validated against `membership.schema.json` with stable IDs.

---

### Source audit

`ma_charter_source_audit_rolling.csv`

and preferably JSON.

At minimum include:

- municipality
- official website
- charter / governing-law URLs
- election creation/calendar URLs
- result URLs
- office row count
- schema-ready row count
- unresolved row count
- current-officeholder count
- known vacancies / unresolved seats
- Person validation results
- status
- conflicts / notes

---

### Appointed exclusions

`ma_charter_appointed_exclusions_rolling.csv`

Record offices that authoritative sources establish as appointed.

---

### Statewide coverage

`ma_351_charter_coverage_status_rolling.json`

Must contain **all 351 municipalities** and identify which have:

- no local research
- partial research
- substantial research
- complete charter audit
- unresolved conflicts

Do not equate "one office found" with "municipality complete."

---

### Validation

`ma_charter_validation_report_rolling.json`

Include:

- municipalities researched
- total research rows
- schema-ready Office count
- verified current-officeholder count
- schema-ready Person count
- known vacancies / unresolved seats
- schema validation errors (Office and Person)
- unresolved municipalities
- remaining officeholder-backfill municipalities
- source conflicts
- most recent structure batch
- most recent officeholder batch

---

### ZIP

Rebuild:

`ma_charter_audit_rolling.zip`

after every meaningful batch.

The ZIP should contain all rolling data files and all supplied schemas.

---

# Completion Standard

A municipality should only be considered **charter-audit complete** when reasonable research has established:

1. governing form
2. controlling charter/special act/bylaws
3. complete elected-office inventory
4. meaningful appointed-office exclusions
5. seat counts
6. term structure
7. district/ward/at-large structure
8. election administration source
9. results source
10. unresolved conflicts documented

If one or more are missing, use statuses such as:

- `partial`
- `substantial`
- `needs-seat-normalization`
- `needs-charter-source`
- `needs-regional-agreement`
- `source-conflict`

Do not label it complete merely because some elected positions were found.

Officeholder coverage is tracked as a **separate dimension**: a municipality's charter/office-structure status and its current-officeholder status are reported independently, and structure completeness does not imply officeholder completeness.

---

# Current Officeholders

For every municipal elected office discovered or already preserved, also identify the people currently holding the elected seats as of the research/retrieval date. Office structure remains the controlling determination, but current-officeholder research is part of the primary workflow — not a deferred phase.

Keep office structure and officeholder coverage as separate progress dimensions. Do not erase, downgrade, or restart the existing elected-office checkpoint merely because current-officeholder backfill has not yet been done. Existing municipalities with office research need an officeholder backfill pass. Newly researched municipalities should receive officeholder research in the same persisted batch whenever feasible.

## Incumbency

Do not assume the latest election winner is still the incumbent. Check for resignations, vacancies, appointments to fill vacancies, special elections, updated board pages, and term expiration. Election results may support incumbency only when the chain to the present is reasonably established. If the evidence is incomplete, record the person/seat as unresolved rather than guessing.

An office may be elective even when the current occupant entered by appointment to fill a vacancy. Include that current occupant because they hold an elected office, but record `how_seated = appointed` when supported. Likewise preserve `elected`, `succeeded`, or `acting` when supported. Do not falsely label an appointed vacancy-filler as elected.

## Mixed and Regional Bodies

For mixed bodies, connect people only to the locally elected seats represented by the elected Office record. Do not count governor-appointed, tenant-appointed, board-appointed, or ex-officio members as elected seats. If an appointed or ex-officio person appears on the same roster, use that information to reconcile composition and document exclusions, but do not attach that person to the elected office unless they actually occupy one of its elected seats. If the number of apparent current holders exceeds the elected seat count, investigate before serializing; this often signals ex-officio/appointed members or an office-structure error.

For ward, district, precinct, numbered-seat, or mixed structures, capture the seat label when the official source supports it. For representative Town Meeting, capture all currently seated elected representatives when an authoritative precinct/roster source is available; exclude ex-officio members from the elected representative count and preserve vacancies. Open Town Meeting attendees are never modeled as officeholders merely by participation.

## Board Leadership

Do not create a separate elected office for Chair, Vice Chair, President, or similar internal board leadership unless voters separately elect that position. A person selected internally as chair remains linked to the underlying elected member office; an organizational membership role may preserve chair status if modeled.

## Person Identity

Create/persist stable Person identities using existing person IDs whenever available; never regenerate IDs for a person already in the rolling dataset. For a newly discovered person, create one schema-valid stable ID and persist it for reuse. Deduplicate the same person across multiple offices or municipalities when evidence establishes the identity; do not merge people merely because names match.

For each current officeholder attempt to preserve: municipality; `jurisdiction_id`; `office_id`; standardized office role; local title; `person_id`; person name as shown by the authoritative source; seat/ward/district/precinct label when applicable; current status; how seated when known; term start/end only when supported; official profile/roster URL; source URL(s); retrieved/as-of date; verification status; and notes about vacancies, appointments, conflicting rosters, or uncertainty. Optional contact/image data may be captured only from authoritative public government sources and only when useful; never invent missing values.

## `person.schema.json` Rule

Use `person.schema.json` for schema-ready Person records. A Person officeholder record should link through `roles[].jurisdiction_id` and `roles[].office_id`, and may include `roles[].seat` and `roles[].term` when supported. Use `verification.status` conservatively: `machine-extracted` for sourced but not human-reviewed records unless another supplied status is genuinely warranted. Every schema-ready Person needs at least one source. Validate all generated Person records against `person.schema.json`. If Organization/Post/Membership records are generated, validate them against the supplied organization, post, and membership schemas and keep IDs stable. Do not force Membership creation merely to represent a person-office link when `Person.roles` already provides the required connection.

## Seat Reconciliation

For each office compare expected elected seats with currently verified holders. Record verified holder count, known vacancy count, and unresolved seat count where possible. A shortage of names is not proof of vacancy. If an official page explicitly marks a vacancy, preserve it. If the roster is stale, contradictory, or incomplete, flag it and search current official election/vacancy materials before deciding.

Maintain a research-layer current-officeholder dataset that can represent unresolved or vacant seats without fabricating Person objects.

## Downstream Linkage

Preserve URLs and identifiers that support later connection of:

`Jurisdiction → Organization → Post/Office → Election Contest → Person`

---

# Source Discipline

For every material elected/appointed claim, save the supporting URL.

Whenever possible capture the specific charter article/section in notes, for example:

- Charter §3-1
- Article IV
- Acts of 2026, c.124
- Town Bylaws §2-4

A URL alone is acceptable when the official page itself explicitly states the composition.

Never manufacture a charter citation.

---

# Research Style

Be conservative.

Preferred:

> Elected status verified; seat count unresolved.

Not acceptable:

> This is probably a three-member board.

Preferred:

> Charter says 5 years; 2026 election notice says 3 years. Conflict requires amendment research.

Not acceptable:

> Used the newer number without documenting the conflict.

---

# Progress Reporting

After each persisted batch report both dimensions:

- municipalities researched for structure in the batch
- municipalities backfilled for current holders in the batch
- total municipalities with structure research
- total office rows
- schema-ready Office records
- verified current-officeholder records
- schema-ready Person records
- known vacancies / unresolved seats
- validation success (Office and Person)
- remaining structure municipalities
- remaining officeholder-backfill municipalities
- significant charter, roster, vacancy, or identity conflicts

Always provide actual downloadable artifacts when available.

Do not merely mention hypothetical sandbox filenames.

Before presenting a download link, verify the file actually exists.

---

# Current Starting Point

Begin from the latest persisted checkpoint:


First inspect the coverage JSON and determine the next unresolved municipalities.

Then continue the audit — researching office structure for unresolved municipalities and current holders for every elected office found. All rules above remain in force for authoritative sourcing, charter overrides, elected vs appointed status, seat counting, regional bodies, Town Meeting, office IDs, conflicts, persistence, validation, and conservative uncertainty handling. Never invent facts or values to fill gaps or satisfy schemas.

The overall goal is a **fully sourced, legally defensible, machine-readable map of every elected municipal office in Massachusetts — and the people currently holding those elected seats** — suitable for CivicMirror election creation and results ingestion.