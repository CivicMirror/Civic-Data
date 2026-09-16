# Mississippi state elected office structure

Issue #68, under master issue #36. Sources retrieved September 13, 2026.
The initial pass created offices and their supporting organizations/jurisdictions.
The September 14 officeholder pass adds people and memberships as detailed below.

| Office group | Posts / elected seats |
| --- | ---: |
| Governor, Lieutenant Governor, Secretary of State, Attorney General, State Auditor, State Treasurer, Commissioner of Insurance, Commissioner of Agriculture and Commerce | 8 |
| House of Representatives, districts 1–122 | 122 |
| State Senate, districts 1–52 | 52 |
| Supreme Court, districts 1–3, places 1–3 in each | 9 |
| Court of Appeals, districts 1–5, places 1–2 in each | 10 |
| Public Service Commission, Northern/Central/Southern districts | 3 |
| Transportation Commission, Northern/Central/Southern districts | 3 |
| Total | 207 |

Issue #41's trial-court judicial-district pass adds 20 Chancery Court District
posts with 52 seats and 23 Circuit Court District posts with 59 seats. Each
district is modeled as a multi-county judicial-district jurisdiction and
organization; the post's `seats` count preserves the number of elected judges
without creating one duplicate office per county.

Each post has one seat. Legislative records follow the existing NC pattern:
one district jurisdiction, organization, and post per district. Each executive
office has its own organization under the statewide executive jurisdiction.
Each commission and appellate court has one organization; post IDs and titles
distinguish its elected districts and, for courts, places. The courts exercise
statewide authority; their electoral districts are not separate courts.
Chief/presiding judicial titles and legislative leadership positions are not
additional elected seats. Vacant legislative seats remain represented.
The Senate directory internally labels the Lieutenant Governor's leadership
card as district 53; it is not a Senate district and is not imported as one.

## Sources and interpretation

- [SOS statewide candidate qualifying forms](https://www.sos.ms.gov/elections-and-voting/candidate-referenda-information/candidate-qualifying-forms?tid=15): the eight statewide executive offices.
- [SOS complete qualifying forms](https://www.sos.ms.gov/elections-and-voting/candidate-referenda-information/candidate-qualifying-forms): elected legislative, appellate judicial, and commission offices.
- [Official House directory](https://www.legislature.ms.gov/member/?chamber=H&fiscalyear=26) and [Senate directory](https://www.legislature.ms.gov/member/?chamber=S&fiscalyear=26): complete district enumeration, including vacant cards and leadership cards. The latter use district attributes rather than the ordinary visible district label. These public pages required a certificate-verification bypass during retrieval.
- [State legislature overview](https://www.ms.gov/agencies/mississippi-legislature): confirms 122 representatives and 52 senators.
- [SOS 2025 judicial directory](https://www.sos.ms.gov/content/documents/ed_pubs/pubs/2025SC/Judicial%20Branch%20and%20Legal%20Resources%20State%20%26%20County%20Officials_2025-3.pdf), printed page 30 (PDF page 5): visually verified all nine Supreme Court and ten Court of Appeals district/place combinations. Only office structure is imported. The overview on printed page 26 calls Court of Appeals districts congressional districts, but page 30 explicitly notes separately designated Court of Appeals districts; no congressional-district linkage is asserted here. Direct court roster pages returned HTTP 500 during this pass.
- [Public Service commissioners](https://www.psc.ms.gov/home/commissioners) and [Transportation Commission](https://mdot.ms.gov/portal/commission): Northern, Central, and Southern district seats.

## Separate work

District attorneys remain a separate judicial-district item under #41. Existing
county offices are not duplicated. Appointed offices and municipal offices are
outside this state-office pass. No human verification is asserted.

## Officeholder backfill — September 14, 2026

The current official rosters account for all 207 state posts: 204 named
officeholders and three explicitly vacant legislative seats. This pass adds
204 people and 204 memberships under `people/state/` and `memberships/state/`.

| Office group | Memberships | Vacant posts |
| --- | ---: | --- |
| Statewide executive | 8 | None |
| House | 120 | Districts 70 and 77 |
| Senate | 51 | District 34 |
| Supreme Court | 9 | None |
| Court of Appeals | 10 | None |
| Public Service Commission | 3 | None |
| Transportation Commission | 3 | None |

Sources retrieved September 14, 2026:

- [MS.gov elected officials](https://www.ms.gov/government/elected-officials): executive office/name pairs.
- [House roster](https://www.legislature.ms.gov/member/?chamber=H&fiscalyear=26) and [Senate roster](https://www.legislature.ms.gov/member/?chamber=S&fiscalyear=26): all numbered districts, names, portraits, and explicit vacancies. Leadership cards count toward their districts; the Lieutenant Governor's internal Senate district 53 card is excluded.
- [Live Supreme Court roster](https://courts.ms.gov/appellatecourts/sc/scjustices.php) and [live Court of Appeals roster](https://courts.ms.gov/appellatecourts/coa/coajudges.php): current names and exact district/place or district/position assignments. Court of Appeals `Position` maps to the existing post's `Place`. Chief/presiding titles do not create additional memberships.
- [Celeste Embrey Wilson appointment](https://governorreeves.ms.gov/governor-reeves-appoints-celeste-embrey-wilson-to-mississippi-supreme-court/): District 3, Place 1, effective August 1, 2026.
- [Amanda Jones Tollison appointment](https://governorreeves.ms.gov/governor-reeves-appoints-amanda-jones-tollison-to-mississippi-supreme-court/): District 3, Place 2, effective September 1, 2026.
- [PSC commissioners](https://www.psc.ms.gov/home/commissioners): names and Northern/Central/Southern assignments.
- [MDOT commission contacts](https://mdot.ms.gov/portal/contacts): names and Northern/Central/Southern assignments, retrieved through indexed official-page content; direct page retrieval returned the JavaScript application shell.

The live court pages returned HTTP 500 to ordinary retrieval but returned complete
HTTP 200 rosters through the local FlareSolverr service. They supersede the older
SOS court directory for officeholder identity; Robert P. Chamberlin and James D.
Maxwell II are not imported as current state justices.

People remain `machine-extracted`; no human review status is implied. The source
retrieval date is not a term start. Exact starts and `how_seated: appointed` are
recorded for Wilson and Tollison using the governor's announcements. Legislative
memberships use `how_seated: elected`. Other starts, ends, and seating methods are
omitted where this roster pass does not establish the current term or selection
event; an old biography's initial appointment is not assumed to describe the
current term. No election or candidacy records are synthesized.

Existing-person checks found no Mississippi name matches (including first/last
name comparisons). Exact-name matches in other states belong to separately
modeled Texas school-board officials and California's federal representative;
they are not merged merely by name. New people use fresh UUIDs.

## Validation baseline

Before this pass, full repository validation reported 2,396 errors in existing
Texas person candidacy/election references. Mississippi validation and the
before/after comparison must be considered separately from those existing errors.
