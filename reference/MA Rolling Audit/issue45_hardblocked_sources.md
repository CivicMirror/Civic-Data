# Issue #45 — Hard-blocked towns (13), partial source research

Captured from https://github.com/CivicMirror/Civic-Data/issues/45#issuecomment-5704122208
(2026-09-16). Sourcing found so far for the 13 "hard blocker" towns.

## Applied (2026-09-16) -- all 13 hard-blocked towns addressed
Newburyport (6/6), Southampton Norris (3/5, genuine remaining vacancies), Natick (7/7),
Scituate (5/5), Stoneham (5/5 -- also fixed a same-named-office data error: on-file "Jordan"
school-committee record was actually his Board of Assessors seat, not School Committee),
Stockbridge (3/3 -- full turnover, prior holder Vogt confirmed gone), Salisbury (3/3),
Plainfield Mohawk Trail (2/2), Rehoboth (5/5) + Dighton (5/5, bonus -- discovered alongside
Rehoboth on the same source), Williamsburg local (5/5, incl. 2 confirmed genuine "failure to
elect" vacancies in 2024/2025 before the seat was finally filled in 2025), Worthington (5/5).
Southbridge and New Ashford intentionally left as documented blockers (no source found /
out of scope per prior decision) -- not attempted this pass.

### Sibling-office leads found in passing (not yet applied -- flag for a #34/#43 follow-up)
- **Plainfield Select Board**: 2026 ATE has Elizabeth Lambert winning a 3-year seat (113 votes,
  unopposed) but none of the 3 on-file members (Gillett, Cole, Marshall) is her -- turnover, but
  which specific on-file seat she replaces isn't determinable from this one result alone (seats
  aren't numbered by election cycle on file).
- **Plainfield Library Trustee**: on-file has only 1 of 3 seats (Morann). 2026 ATE: Adrian Almquist
  beat incumbent Donna Monroe (68 to 40) for a 3-year seat -- Almquist not yet on file.
- **Southampton Hampshire Regional School Committee** (southampton-ma/hampshire-regional-school-committee-southampton-member,
  already 4/4 on file): 2026 ATE ("Two for three years") shows Jon D. Lumbra (1493 votes) and a
  write-in, Kelley Labrie (23 votes), as the only entrants -- both on-file members whose terms
  read "2026" (Jennings, Thibodeau) may have just been replaced by these two. Not touched this
  pass since the post wasn't the one flagged as broken; needs its own verification pass.

## Natick
- Roster: https://www.natickps.org/page/school-committee
- Town Charter: https://www.natickma.gov/1059/Town-Charter
  - Elected Officials (Art. 6): https://www.natickma.gov/DocumentCenter/View/15007/Article-6----Adminstrative-Organization
  - Sec. 3-3: 7 members, 3-year terms, staggered so ~equal number expire each year
- ATE results: [2026](https://www.natickma.gov/DocumentCenter/View/21814/Election-Results-3-31-2026) · [2025](https://www.natickma.gov/DocumentCenter/View/19458/Official-Election-Results-3-25-25) · [2024](https://www.natickma.gov/DocumentCenter/View/17206/2024_ANNUAL-TOWN-ELECTION_UNOFFICIAL-RESULTS_3-26-24) · [2023](https://www.natickma.gov/DocumentCenter/View/15126/Election-Results-3-28-23)

## Salisbury (Triton Regional School District)
- Roster: https://tritonschools.org/en-US/committee-members-31b11901
  - Linda Litcofsky (Chair, Salisbury), Nerissa Wallen (VC, Rowley), Erin Berger (Sec, Salisbury), Brett Alger (Newbury), Paul Goldner (Newbury), Caitlin Hunter (Salisbury), Matthew Landers (Newbury), Paul Lees (Rowley), Owen Silva (Rowley)
- Regional agreement (town allocation): https://drive.google.com/file/d/1y5DlENg54teEoOGYR_eN2YZBlX7X0l8q/view
- Blocker was: district-wide source doesn't label which town a winner represents — roster above actually does list town per member, needs re-check against agreement's per-town seat count before minting.

## Rehoboth / Dighton (Dighton-Rehoboth Regional)
- District: https://www.drregional.org/
- Committee: https://www.drregional.org/page/sc-contact — **Fastly JS-challenge wall, use FlareSolverr directly** (see [[ma_waf_gated_sites_fetch_technique]] memory, confirmed 2026-09-16)
- Agreement: https://drive.google.com/file/d/1N0hevVlFemqcvUb9QqG23iV_Rn1X4CrI/view

## Southbridge
- District: https://www.southbridgepublic.org/
- Committee: https://www.southbridgepublic.org/school-committee
- Contacted town clerk for election results — none found online. Both posts affected. Still no working source for results.

## New Ashford
- Shares Mount Greylock Regional School District: https://www.mgrsd.org/district-info/our-schools
- District committee roster: https://www.mgrsd.org/school-committee/mgrsd-school-committee — shows **no New Ashford members**, which matches the regional agreement (7 seats: 4 Williamstown, 3 Lanesborough; New Ashford has no allocated seat despite tuitioning students there and electing its own committee)
- Agreement: https://resources.finalsite.net/images/v1625048756/mtgreylock/ev6ovu2ajl1uwq3f8lvb/Mt_Greylock_approval_letter_and_approved_agreement.pdf
- **Recommendation: leave New Ashford out of scope for now** — town too small (<300 residents), no usable source for its own School Committee roster (local news dead/stale). Revisit if a source surfaces.

## Scituate
- https://www.scit.org/school-committee-home , https://www.scit.org/members
- Policy manual (BBBA/BBBB): 5 members, 3-year terms, staggered at Annual Town Election
- ATE results found: [2024](https://www.scituatema.gov/DocumentCenter/View/900/2024-Town-Election) · [2023](https://www.scituatema.gov/DocumentCenter/View/899/2023-Annual-Town-Election) · [2026 warrant only](https://www.scituatema.gov/DocumentCenter/View/17937/2026-Annual-Town-Election-Warrant?bidId=)
- No 2024–2026 official results found — 2023/2024 results above may still be usable to disambiguate carryover members.

## Newburyport
- Roster: https://www.newburyport.k12.ma.us/district/school-committee
- Charter (Municode): https://library.municode.com/ma/newburyport/codes/code_of_ordinances?nodeId=PTICHRELA_ART7EL
  - Sec. 4-1: 7 members total — 6 elected at-large (4-year terms, staggered so ≥3 seats fill each regular election) + **the mayor, who chairs ex officio**
- ATE results: [2023](https://www.cityofnewburyport.com/sites/g/files/vyhlif12211/f/uploads/11-07-2023_official_election_results_signed.pdf) · [2025](https://www.cityofnewburyport.com/sites/g/files/vyhlif12211/f/uploads/municipal_election_11-4-25_official_results.pdf) · [2021](https://www.cityofnewburyport.com/sites/g/files/vyhlif12211/f/uploads/november_2_2021_election_results.pdf)
- Note: current post (`newburyport-ma-school-committee-member`) has `seats: 6` — per charter this is actually 7 with the mayor as ex-officio chair; check whether mayor should be minted as a member (may need `how_seated: ex-officio` or similar) before reconciling seat count.

## Plainfield
- District: https://www.plainfield-ma.us/ (Mohawk Trail & Hawlemont Regional School Districts)
  - MTRSD School Committee: 16 elected reps, 2 per member town
- ATE results: [2026](https://www.plainfield-ma.us/media/10036) (WAF-blocked doc server — see [[ma_waf_gated_sites_fetch_technique]] header-matching-curl fix; a downloaded copy of the 2026 results PDF was attached directly to the GitHub comment since the source is hard to fetch programmatically) · [2025](https://www.plainfield-ma.us/town-clerk/page/2025-plainfield-town-election-results) (results are **inline HTML on the page itself**, not a separate document)

## Stoneham
- Roster: https://www.stonehamschools.org/school-committee
- Committee assignments PDF (2026-2027, dated 2026-09-10): https://campussuite-storage.s3.amazonaws.com/prod/1558555/4ef830ae-605d-11e8-9fe8-12ef42415eba/3142940/e56af400-b030-11f1-ad18-0a58a9feac02/file/School%20Committee%20Assignments%202026-2027%20rev%209.10.26.pdf
- ATE results: [2026](https://www.stoneham-ma.gov/DocumentCenter/View/12032/Unofficial-April-7-2026) · [2025](https://www.stoneham-ma.gov/DocumentCenter/View/10423/Unofficial-Results-April-1-2025)

## Stockbridge (Berkshire Hills Regional School District)
- District: https://www.bhrsd.org/school-committee
- Roster: https://www.bhrsd.org/school-committee-members
- Regional agreement (June 2017): https://github.com/user-attachments/files/32315270/bhrsd-regional-agreement-june-2017.pdf

## Southampton
- Committee: https://www.townofsouthampton.org/government/boards-and-committees/school-committee-norris — **"Norris" is only in the URL slug; the page's actual full member list has no one named Norris.** Origin of the slug (former member? historical committee name?) is unconfirmed — don't assume it identifies the on-file "Norris seat," it doesn't match current membership.
- Town Clerk / General Elections page: https://www.townofsouthampton.org/government/administration/town-clerk
- ATE results: [2026](https://resources.finalsite.net/images/v1779392556/townofsouthamptonorg/ihxp3ycdtu79klur3jis/ATE5-19-26.pdf) · [2025](https://resources.finalsite.net/images/v1779392684/townofsouthamptonorg/pagvyzun0m001cjtaq05/ATE5-20-25_3.pdf) — both flagged as good sources for other elected offices too (sibling issues)
- 2025 Town Report (also good for sibling-office sourcing): https://resources.finalsite.net/images/v1780950151/townofsouthamptonorg/s8s8pxftmprpjdpyouor/Southampton2025AnnualReportFinal.pdf

## Williamsburg
- Roster: https://www.burgy.org/williamsburg-school-committee
- ATE results: [2026](https://www.burgy.org/sites/g/files/vyhlif1451/f/minutes/election_minutes_may_4_2026_0.pdf) · [2025](https://www.burgy.org/sites/g/files/vyhlif1451/f/minutes/ate_min.pdf) · [2024](https://www.burgy.org/sites/g/files/vyhlif1451/f/minutes/town_election_5-6-2024.pdf) — titled "Minutes of Annual Town Election" but confirmed to include **full tally sheets**, usable as certified results.

## Worthington
- Roster: https://worthington-ma.us/municipal-directory/school-district/worthington-school-committee/
- ATE results: [2026](https://worthington-ma.us/2026/05/2026-preliminary-town-election-results/) (confirmed best/only source found — no other official source exists) · [2025](https://worthington-ma.us/2025/05/2025-election-results/)

## Status after this batch
All 13 originally hard-blocked towns now have at least a roster + some election-result sourcing (captured across the two comments above, 2026-09-16). None of it has been applied to data files yet — next step is minting/reconciling against on-file holders per the "committee turnover" caution in [[ma_issue45_school_committee]] (don't just append live-roster names; use certified results to correctly resolve departed vs. new).

See also [[ma_issue34_conventions]], [[ma_waf_gated_sites_fetch_technique]].
