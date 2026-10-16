# Vermont state and county elected office structure

Issue #163 (VT master tracking). Sources retrieved October 16, 2026.
This pass creates offices and their supporting organizations/jurisdictions
only. No officeholders are imported; memberships are a separate pass
(the pattern of MS issues #68 then the September 14, 2026 officeholder pass).

## What was built

| Office group | Posts / elected seats |
| --- | ---: |
| Governor, Lieutenant Governor, Secretary of State, Attorney General, State Treasurer, Auditor of Accounts | 6 posts / 6 seats |
| State's Attorney (per county) | 14 posts / 14 seats |
| Sheriff (per county) | 14 posts / 14 seats |
| Assistant Judge (per county) | 14 posts / 28 seats |
| High Bailiff (per county) | 14 posts / 14 seats |
| Total built in this pass | 62 posts / 82 seats |

Built by `scripts/build_vt_state_county_posts.py` (125 files: 1 executive
jurisdiction, 62 organizations, 62 posts). Validation of the Vermont tree:
PASSED, 0 errors; the only warnings are 5 pre-existing federal
no-election-trace warnings on the machine-generated federal memberships.

Each statewide executive office has its own organization under the new
statewide executive jurisdiction (`vt-executive.yaml`), following the
Mississippi pattern. Each county office has its own organization under
the existing county government jurisdiction, following the Mississippi
county pattern (post IDs like `addison-vt-county/states-attorney`).

## Government structure in brief

Vermont is a Dillon's Rule, town-meeting state. The municipality (town,
city, incorporated village) is the general-purpose local government.
Counties are **not** general-purpose governments: there are no county
commissioners or county legislatures. County government consists of the
elected officers below plus a county tax administered by the assistant
judges for the courthouse and jail. That is why the county tier is only
five offices, against 13 office types per county in Mississippi.

### State level

- Six offices are elected statewide every two years at the November
  general election: Governor, Lieutenant Governor, Secretary of State,
  and Auditor of Accounts (Vermont Constitution, Ch. II, sections
  47-49), State Treasurer (same), and Attorney General (a statutory
  office, elected since 1908; the first five are constitutional).
  Vermont and New Hampshire are the only states with two-year
  gubernatorial terms.
- General Assembly: Senate 30 seats, House 150 seats, all two-year
  terms. **Not built in this pass** -- district enumeration (multi-member
  Senate districts; one- and two-member House districts named for their
  towns) must come from the official apportionment lists, as its own
  pass, mirroring MS issue #68.
- Judiciary above the county level is **appointed**, not elected:
  Supreme Court justices and Superior Court judges are appointed by the
  Governor with Senate consent and retained by vote of the General
  Assembly (Ch. II, sections 32-34). Out of elected scope.

### County level (all 4-year terms beginning February 1 after the election)

- **State's Attorney** -- county prosecutor, one per county (Ch. II,
  section 50).
- **Sheriff** -- one per county (Ch. II, section 50; Title 24, chapter 5,
  subchapter 5).
- **Assistant Judges** -- two per county (Ch. II, section 50; Title 24,
  chapter 5, subchapter 1). They sit with Superior Court judges and also
  administer county property and the county tax -- the closest Vermont
  analog to a county commission, held as a judicial office.
- **Judge of Probate** -- elected (Ch. II, section 51), but **HELD**:
  Vermont has 18 probate districts, not 14. Four counties are split into
  two districts each, so probate posts must be modeled on probate-district
  jurisdictions from the Vermont Judiciary's official enumeration, not
  minted per county. Do not guess the district list.
- **High Bailiff** -- one per county, a Vermont-only office that serves
  process the sheriff cannot serve and succeeds the sheriff on vacancy
  or incapacity. Elected at the November general election (Ch. II,
  section 43 lists high bailiffs among the biennially elected officers,
  while the four-year county officers are covered by sections 50-51;
  exact current term to be pinned in the membership pass). Unpaid and
  rarely active, but a real elected office, so it is in scope.
- **Excluded as appointed**: County Clerk (24 V.S.A. section 171,
  appointment by the assistant judges) and County Treasurer
  (24 V.S.A. section 211, appointment).

### Municipal level (inventory in VT_Municipalities.xlsx)

- Repo seed (Census 2022 Census of Governments): 275 municipal
  jurisdictions -- 235 towns, 10 cities, 30 incorporated villages.
  VLCT's current count splits the same 275 as 237 towns / 28 villages;
  the two-place classification drift is flagged in the workbook's
  Sources sheet and must be reconciled place-by-place in backfill.
- Towns elect at annual town meeting (first Tuesday in March, or by
  Australian ballot where adopted) under 17 V.S.A. section 2646 and
  related sections: selectboard (3, or 5 if voted), town clerk, town
  treasurer, moderator, listers, auditors, constables, collector of
  delinquent taxes, grand juror, town agent -- with charter and
  voted variations (appointed clerks, eliminated auditors/listers)
  resolved **per town**, exactly as in Massachusetts. Most towns have
  no individual charter and operate under general law; chartered
  municipalities have one chapter each in Title 24 Appendix.
- Justices of the Peace are a town office elected on the November state
  ballot for two-year terms, apportioned by population (Ch. II,
  section 52).
- Cities (10) elect a mayor and council/aldermen under individual
  charters. Incorporated villages (inside towns) elect trustees and
  village officers under their own charters -- a second overlapping
  municipal layer, unique in New England along with Connecticut
  boroughs and Maine plantations.
- Not in the repo seed: the Unified Towns and Gores of Essex County
  and the remaining unorganized towns/gores (governor-appointed
  supervisors, 24 V.S.A. chapter 43). Scope decision needed before
  any minting.
- School districts are deferred to their own classification pass
  (post-Act 46 merger map), mirroring MS issue #158.

## Membership pass -- planned sources (issue #163, item 6)

- Statewide executive: the six offices' official sites (vermont.gov
  agencies) for current holders; term starts are the January
  inauguration following the 2024 general election. **Timing note:**
  the November 3, 2026 general election re-elects all six offices and
  all county officers -- a membership pass run before certification
  should record the 2024-elected holders; winners of the 2026 cycle
  are seated in January / February 2027.
- State's Attorneys: the Department of State's Attorneys and Sheriffs
  official directory (all 14).
- Sheriffs: the 14 county sheriff department sites / Vermont Sheriffs'
  Association as a locator only.
- Assistant Judges and Judges of Probate: the Vermont Judiciary's
  official court directories.
- High Bailiffs: the Secretary of State's certified 2024 general
  election results (several counties elect by write-in; blanks are
  not votes and write-in winners must be read from the certified
  canvass, not news reports).
- County officers were last elected in 2022 (terms February 1, 2023 --
  January 31, 2027), except high bailiffs and justices of the peace,
  who were on the 2024 ballot.

## Sources

- Vermont Constitution, Chapter II, sections 43, 47-52 (elections,
  terms, county officers) -- summarized, not quoted.
- Vermont Statutes Online, Title 24, chapter 5 (County Officers):
  https://legislature.Vermont.gov/statutes/chapter/24/005
- Legislative Counsel memorandum on constitutional officers
  (2024-02-20), Vermont General Assembly workgroup records.
- Vermont Statutes Online, Title 17, chapter 55 (local elections and
  town officers, sections 2646-2651 series) and Title 24 Appendix
  (municipal charters).
- U.S. Census Bureau, 2022 Census of Governments government-units
  listing -- the repo jurisdiction files' own source.
- Vermont League of Cities and Towns guides (association source;
  locator / cross-check only, per the MS MML rule).
