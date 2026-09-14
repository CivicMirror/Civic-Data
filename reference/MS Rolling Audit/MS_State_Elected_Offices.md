# Mississippi state elected office structure

Issue #68, under master issue #36. Sources retrieved September 13, 2026.
This pass creates offices and their supporting organizations/jurisdictions only;
it adds no people, memberships, candidacies, or elections.

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
outside this state-office pass. No officeholder currency or human verification
is asserted.

## Validation baseline

Before this pass, full repository validation reported 2,396 errors in existing
Texas person candidacy/election references. Mississippi validation and the
before/after comparison must be considered separately from those existing errors.
