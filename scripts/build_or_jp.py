#!/usr/bin/env python3
"""Build OR Justice of the Peace tier for issue #170 into the sparse ws.
Sources: SOS Blue Book county pages (denominator), county certified results
(11 contests), county official documents for appointments/terms.
Run: ~/workspace/venvs/civic-data/bin/python build_or_jp.py
"""
import json, os, re, sys, uuid

WS = os.path.expanduser("~/workspace/civic-data-or170/data/us/or")
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
DATE = "2026-10-23"
HDR = "# Built for issue #170 (Oregon master tracking)."
BB = {c: v["source_url"] for c, v in json.load(open(os.path.expanduser("~/workspace/or170/jp_bluebook.json")))["counties"].items()}
OJD_ABOUT = "https://www.courts.oregon.gov/about/Pages/default.aspx"

def u5(key): return str(uuid.uuid5(NS, key))
def yq(s): return "'" + s.replace("'", "''") + "'"
def src(url, note): return f"- url: {url}\n  note: {yq(note)}\n  retrieved: '{DATE}'"
def jur_id(slug): return f"ocd-jurisdiction/country:us/state:or/county:{slug}/government"

created, edited = [], []
def write(path, content):
    full = os.path.join(WS, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    if os.path.exists(full): raise SystemExit(f"EXISTS already: {path}")
    with open(full, "w") as f: f.write(content)
    created.append(path)

# ---------- seat table ----------
# per seat: county slug, county display, pos (None|1|2), district note,
# holder dict(slug, name, ballot), membership dict(start, end, how),
# contest dict(date, type, figures, url, title) or None,
# extra_sources: list of (url, note) appended to person+membership sources,
# losers: list of (slug, name, ballot, figures-note)
SEATS = [
 dict(c="baker", cn="Baker", pos=None, district=None,
   holder=("brent-kerns", "Brent Kerns", "L Brent Kerns"),
   mem=dict(start="2025-01-06", end=None, how="elected"), contest=None,
   note="Sole candidate for the seat at the May 21, 2024 primary per the official Secretary of State 2024 Primary Voters' Pamphlet candidate list (ballot name: L Brent Kerns); as a nonpartisan office decided by majority at the primary, an unopposed candidate is elected there. Baker County posts no certified 2024 results document online, so no vote total is recorded; the certified total is a clerk-request item on issue #170.",
   bb_note="Oregon Blue Book, Baker County page (Secretary of State): county officials list 'Justice of the Peace Brent Kerns (2031)'."),
 dict(c="clackamas", cn="Clackamas", pos=None, district=None,
   holder=("karen-brisbin", "Karen Brisbin", "Karen Brisbin"),
   mem=dict(start="2023-01-02", end="2026-01-01", how="elected"),
   contest=dict(date="2022-05-17", type="primary",
     figures="Karen Brisbin 52,953; write-in lines as printed 478 and 157; cast votes 53,588; undervotes 52,850; overvotes 3.",
     url="https://dochub.clackamas.us/documents/drupal/92fdc2da-f437-4f61-b4f4-d089d9aab909",
     title="Clackamas County, Canvass Results Report, May 17, 2022 Primary Election, Official Results (run date 06/13/2022)"),
   note="Retired effective January 1, 2026 (Clackamas County elections release, November 10, 2025: filing opened 'upon notification of the planned retirement of Judge Karen Brisbin on January 1, 2026'); the membership ends on the retirement date. The seat was filled by gubernatorial appointment (Kathleen Rastetter, from 2026-01-01) ahead of the November 2026 election.",
   bb_note="Oregon Blue Book, Clackamas County page (Secretary of State): county officials list 'Justice of the Peace Karen Brisbin (2029)'. The Blue Book listing predates her January 1, 2026 retirement and is stale for the current holder."),
 dict(c="clackamas", cn="Clackamas", pos=None, district=None, appointee=True,
   holder=("kathleen-rastetter", "Kathleen Rastetter", "Kathleen Rastetter"),
   mem=dict(start="2026-01-01", end=None, how="appointed"), contest=None,
   extra_sources=[("https://www.clackamas.us/news/2025-11-10/clackamas-county-elections-opens-filing-for-the-justice-of-the-peace",
     "Clackamas County Elections release, November 10, 2025: filing for the Justice of the Peace opened 'upon notification of the planned retirement of Judge Karen Brisbin on January 1, 2026. This judicial vacancy will first be filled with an appointment by Governor Kotek until election in 2026', and the seat 'will be elected in the November General Election and serve for a full six-year term'."),
    ("https://www.clackamas.us/recording/officiants.html",
     "Clackamas County, Marriage Officiants page: 'Judge Kathleen J. Rastetter -- Justice of the Peace, Clackamas County Justice Court in Happy Valley'."),
    ("https://www.clackamas.us/meetings/des/compensation-board/2026-02-10",
     "Clackamas County Compensation Board minutes, February 10, 2026: Judge Rastetter 'has been in the position of Justice of the Peace for the Justice Court for just over a month... She was appointed by the Governor and will run for elected office'. A county news release dated January 15, 2026 states Governor Tina Kotek appointed Kathleen J. Rastetter to serve as Justice of the Peace effective January 1, 2026, filling the position created by Judge Brisbin's retirement."),
    ("https://www.clackamas.us/elections/november-3-2026-general-election",
     "Clackamas County, November 3, 2026 General Election candidate filings: 'Justice of the Peace -- Kathleen Rastetter'.")],
   note="",
   bb_note="Oregon Blue Book, Clackamas County page (Secretary of State): still lists Karen Brisbin (2029); the listing predates her January 1, 2026 retirement and is stale -- the county's own current pages list Rastetter."),
 dict(c="columbia", cn="Columbia", pos=None, district=None,
   holder=("james-gibson", "James Gibson", "James (Jim) Gibson"),
   mem=dict(start="2025-01-06", end=None, how="elected"),
   contest=dict(date="2024-05-21", type="primary",
     figures="James (Jim) Gibson 7,297 (97.88%), unopposed; write-in totals 158; total votes cast 7,455; undervotes 4,163.",
     url="https://www.columbiacountyor.gov/media/Election/Abstracts/2024-05-21_Certified_SUMMARY-ABSTRACT_Columbia.pdf",
     title="Columbia County, May 21, 2024 Primary Election Certified Final Results -- Summary Abstract"),
   note="", bb_note="Oregon Blue Book, Columbia County page (Secretary of State): county officials list 'Justice of the Peace James Gibson (2031)'."),
 dict(c="deschutes", cn="Deschutes", pos=None, district="The Deschutes County justice district covers part of the county.",
   holder=("charles-fadeley", "Charles Fadeley", "Charles Fadeley"),
   mem=dict(start="2023-01-02", end=None, how="elected"),
   contest=dict(date="2022-05-17", type="primary",
     figures="Charles Fadeley 18,171 (99.08%), sole candidate; write-in 169; total 18,340; undervotes 13,390.",
     url="https://weblink.deschutes.org/Public/DocView.aspx?id=95932&dbid=0&repo=LFPUB",
     title="Deschutes County Clerk, 2022-05-17 Canvass Report (Laserfiche public portal, document 95932), p. 7"),
   note="The county's certified November 8, 2022 canvass contains no Justice of the Peace contest; the race was decided at the May 2022 primary, as Oregon nonpartisan judicial races are when a candidate wins a majority.",
   bb_note="Oregon Blue Book, Deschutes County page (Secretary of State): county officials list 'Justice of the Peace Charles Fadeley (2029)'."),
 dict(c="douglas", cn="Douglas", pos=1, district="South Douglas Justice Court District.",
   holder=("machelle-briggs-mayfield", "Machelle Briggs-Mayfield", "Machelle Briggs-Mayfield"),
   mem=dict(start="2025-01-06", end=None, how="elected"),
   contest=dict(date="2024-05-21", type="primary",
     figures="Machelle Briggs-Mayfield 2,687 (98.53%), sole candidate; write-in 40; total votes 2,727; undervotes 1,308; 4,035 ballots cast in the district.",
     url="https://www.douglascountyor.gov/DocumentCenter/View/25777/May-21-2024-Official-Final-Results-Summary-Certified-PDF",
     title="Douglas County, May 21, 2024 Official Final Results Summary (Certified)"),
   note="", bb_note="Oregon Blue Book, Douglas County page (Secretary of State): county officials list two Justices of the Peace, 'Machelle Briggs-Mayfield (2031) & Kathleen Miller (2031)'."),
 dict(c="douglas", cn="Douglas", pos=2, district="Reedsport Justice of the Peace District.",
   holder=("kathleen-miller", "Kathleen Miller", "Kathleen K Miller"),
   mem=dict(start="2025-01-06", end=None, how="elected"),
   contest=dict(date="2024-05-21", type="primary",
     figures="Kathleen K Miller 2,008 (98.33%), sole candidate; write-in 34; total votes 2,042; undervotes 1,052; 3,094 ballots cast in the district.",
     url="https://www.douglascountyor.gov/DocumentCenter/View/25777/May-21-2024-Official-Final-Results-Summary-Certified-PDF",
     title="Douglas County, May 21, 2024 Official Final Results Summary (Certified)"),
   note="", bb_note="Oregon Blue Book, Douglas County page (Secretary of State): county officials list two Justices of the Peace, 'Machelle Briggs-Mayfield (2031) & Kathleen Miller (2031)'."),
 dict(c="gilliam", cn="Gilliam", pos=None, district=None,
   holder=("cris-patnode", "Cris Patnode", "Cris Patnode"),
   mem=dict(start="2021-01-04", end="2024", how="elected"), contest=None,
   note="Incumbent and the only candidate listed for Gilliam County Justice of the Peace in the official Secretary of State 2020 Primary Voters' Pamphlet; no certified Gilliam County 2020 results document is posted online, so no vote total is recorded. He left the seat in 2024 (year precision): Kari Hayter was appointed Justice of the Peace effective June 2024. The end year is bounded by that appointment; the exact departure date and manner are a research item on issue #170.",
   bb_note="Oregon Blue Book, Gilliam County page (Secretary of State): county officials list the current Justice of the Peace as Kari Hayter (2027) -- the appointee who succeeded Patnode in June 2024."),
 dict(c="gilliam", cn="Gilliam", pos=None, district=None, appointee=True,
   holder=("kari-hayter", "Kari Hayter", "Kari Hayter"),
   mem=dict(start="2024-06", end=None, how="appointed"), contest=None,
   note="Appointed Gilliam County Justice of the Peace effective June 2024 (month precision; her candidate filing posted on the Gilliam County site states the appointment and her prior service as City Recorder of Arlington, and the appointment was announced by the Governor). She succeeded Cris Patnode. She is recorded as a candidate for election to the seat in 2026.",
   bb_note="Oregon Blue Book, Gilliam County page (Secretary of State): county officials list 'Justice of the Peace Kari Hayter (2027)'."),
 dict(c="grant", cn="Grant", pos=None, district=None,
   holder=("richard-tirico", "Richard Tirico", "Richard Tirico"),
   mem=dict(start="2025-01-06", end=None, how="elected"),
   contest=dict(date="2024-05-21", type="primary",
     figures="Richard Tirico 1,318 (54.06% of 2,438 votes cast in the contest -- a majority, elected outright at the primary); Dale Valade 705; Josh Fuller 409; write-in 6; undervotes 333; total ballots cast 2,774.",
     url="https://grantcountyoregon.net/DocumentCenter/View/1761/May-21-2024-Primary-Election-Certified-Results",
     title="Grant County, May 21, 2024 Primary Election Certified Results -- Detail Results"),
   losers=[("dale-valade", "Dale Valade", "Dale Valade"), ("josh-fuller", "Josh Fuller", "Josh Fuller")],
   note="", bb_note="Oregon Blue Book, Grant County page (Secretary of State): county officials list 'Justice of the Peace Richard Tirico (2031)'."),
 dict(c="harney", cn="Harney", pos=None, district=None,
   holder=("riley-richardson", "Riley Richardson", "Riley Richardson"),
   mem=dict(start="2025-01-06", end=None, how="elected"), contest=None,
   note="Sole candidate for the seat at the May 21, 2024 primary per the official Secretary of State 2024 Primary Voters' Pamphlet candidate list (incumbent Vicky Clemens did not run); as a nonpartisan office decided by majority at the primary, an unopposed candidate is elected there. Harney County posts no certified 2024 results document online, so no vote total is recorded; the certified total is a clerk-request item on issue #170.",
   bb_note="Oregon Blue Book, Harney County page (Secretary of State): county officials list 'Justice of the Peace Riley Richardson (2031)'."),
 dict(c="hood-river", cn="Hood River", pos=None, district="Cascade Locks Justice District -- the only Hood River County justice district with a listed Justice of the Peace in the Blue Book. Whether a second district exists is an open item on issue #170.",
   holder=("john-harvey", "John Harvey", "John Harvey"),
   mem=dict(start="2023-01-02", end=None, how="elected"),
   contest=dict(date="2022-05-17", type="primary",
     figures="John Harvey 205 (93.18%); write-in 15; total 220; undervotes 73; 293 ballots cast, 974 registered voters in the district.",
     url="https://www.hoodrivercounty.gov/",
     title="Hood River County, certified May 17, 2022 primary election results summary (Official Election Results Summary)"),
   note="The county's certified May and November 2020 summaries were read in full and contain no Justice of the Peace contest, so the Blue Book's (2027) term attribution is not supported; the certified record puts his election at the May 17, 2022 primary for the six-year term that began January 2, 2023. County financial reports have variously shown his term expiring December 31, 2022 (FY2019) and December 31, 2024 (FY2024) for earlier service; the discrepancy is flagged on issue #170.",
   bb_note="Oregon Blue Book, Hood River County page (Secretary of State): county officials list 'Justice of the Peace John Harvey (2027)' -- see the election note: the county's certified documents do not support the 2027 attribution."),
 dict(c="jackson", cn="Jackson", pos=None, district=None, existing_person="people/judicial-district/joe-charter.yaml",
   holder=("joe-charter", "Joe Charter", "Joe Charter"),
   mem=dict(start="2025-01-06", end=None, how="elected"),
   contest=dict(date="2024-11-05", type="general",
     figures="Joe Charter 43,176 (98.88%), the only named candidate; write-in 490; total contest votes 43,666. The county document is precinct-level and prints no contest aggregate; 43,176 is the sum of its 43 Justice of the Peace precinct blocks, re-verified.",
     url="https://webarchive.jacksoncountyor.gov/DesktopModules/Bring2mind/DMX/API/Entries/Download?Command=Core_Download&EntryId=11918&language=en-US&PortalId=0&TabId=41",
     title="Jackson County, Statement of Votes Cast by Geography, November 5, 2024 General Election -- Official Results, Precinct Level Report"),
   note="Charter previously served as a Circuit Court judge (District 1, Position 8), winning that seat at the May 19, 2020 primary; his candidacy for that seat is on his person record. He left the circuit bench in 2024 and won this seat at the November 5, 2024 general election; the circuit departure date is a held research item on issue #170.",
   bb_note="Oregon Blue Book, Jackson County page (Secretary of State): county officials list 'Justice of the Peace Joseph Charter (2031)'; Jackson County's own officials list likewise names Joe Charter as Justice of the Peace."),
 dict(c="klamath", cn="Klamath", pos=None, district=None,
   holder=("karen-oakes", "Karen Oakes", "Karen Oakes"),
   mem=dict(start="2023-01-02", end=None, how="elected"), contest=None,
   note="Documented as a Justice of the Peace candidate at the May 2022 primary in the official Secretary of State 2022 Primary Voters' Pamphlet; her earlier elections (2004, 2010, 2016) put the seat on a 2022 cycle. The county's certified May and November 2020 documents were read in full and contain no Justice of the Peace contest, so the Blue Book's (2027) attribution is not supported and her current term is modeled from January 2, 2023. No certified county vote total for the 2022 race was located online; it is a clerk-request item on issue #170.",
   bb_note="Oregon Blue Book, Klamath County page (Secretary of State): county officials list 'Justice of the Peace Karen Oakes (2027)' -- see the note: the county's certified 2020 documents contain no JP contest; the documented candidacy is 2022."),
 dict(c="lane", cn="Lane", pos=None, district=None,
   holder=("rick-brissenden", "Rick Brissenden", "Rick Brissenden"),
   mem=dict(start="2023-01-02", end=None, how="elected"), contest=None,
   note="Appointed Justice of the Peace in 2016 to succeed Cindy Forsythe and elected that year; on a six-year cycle his current term began January 2, 2023. The Blue Book's (2027) term attribution conflicts with that documented history and is flagged on issue #170. No certified Lane County results document for the 2022 race was located online (the county's historical results are served through an app that posts no abstract); the certified total is a clerk-request item on issue #170.",
   bb_note="Oregon Blue Book, Lane County page (Secretary of State): county officials list 'Justice of the Peace Rick Brissenden (2027)' -- see the note on the conflicting term history."),
 dict(c="linn", cn="Linn", pos=None, district=None,
   holder=("jessica-meyer", "Jessica Meyer", "Jessica K Meyer"),
   mem=dict(start="2021-01-04", end=None, how="elected"), contest=None,
   note="Linn County's official news release (October 24, 2023) states she served as Justice of the Peace pro tempore 2012-2018 and 'has been Justice of the Peace since 2018'; her current term is modeled on the Blue Book's term-expiry year (2027), i.e. the term that began January 4, 2021. No certified Linn County 2020 results document is posted online and no 2020 race record was located; the election record is a clerk-request item on issue #170.",
   bb_note="Oregon Blue Book, Linn County page (Secretary of State): county officials list 'Justice of the Peace Jessica K. Meyer (2027)'."),
 dict(c="malheur", cn="Malheur", pos=None, district=None,
   holder=("margaret-mahony", "Margaret Mahony", "Margie Mahony"),
   mem=dict(start="2025-01-06", end=None, how="elected"),
   contest=dict(date="2024-05-21", type="primary",
     figures="Margie Mahony 2,868; John-Paul (JP) Carey 1,176; write-in 13; over votes 3; under votes 396; total ballots 4,456.",
     url="https://www.malheurco.org/wp-content/uploads/Departments/CountyClerk/Election%20Results/Group-4-5-21-2024-final.pdf",
     title="Malheur County, Detail Results -- Group 4, Final Official, May 2024 Primary Election (May 21, 2024), p. 14"),
   losers=[("john-paul-carey", "John-Paul Carey", "John-Paul (JP) Carey")],
   note="", bb_note="Oregon Blue Book, Malheur County page (Secretary of State): county officials list 'Justice of the Peace Margaret (Margie) Mahony (2031)'."),
 dict(c="marion", cn="Marion", pos=None, district=None,
   holder=("justin-kidd", "Justin Kidd", "Justin Kidd"),
   mem=dict(start="2023-01-02", end=None, how="elected"),
   contest=dict(date="2022-05-17", type="primary",
     figures="Justin Kidd 19,783 (100.00% of cast votes), sole candidate; misc. write-in 246; undervotes 15,962; overvotes 1. Race heading as printed: 'Justice of the Peace - NonPartisan - Vote for 1'.",
     url="https://www.co.marion.or.us/CO/elections/Results/Documents/20220517/Cumulative%20Results-6-8-2022%2003-13-42%20PM.pdf",
     title="Marion County, Cumulative Results -- May 17, 2022 Primary Election (final published cumulative results, June 8, 2022)"),
   note="Marion County's certified November 2022 document contains no Justice of the Peace contest; the race was decided at the May primary. The county's final published cumulative primary results are used for the figures; the document is not itself captioned 'certified'.",
   bb_note="Oregon Blue Book, Marion County page (Secretary of State): county officials list 'Justice of the Peace Justin Kidd (2029)'."),
 dict(c="morrow", cn="Morrow", pos=None, district=None,
   holder=("glen-diehl", "Glen Diehl", "Glen G Diehl"),
   mem=dict(start="2021-01-04", end=None, how="elected"),
   contest=dict(date="2020-11-03", type="general",
     figures="Runoff between the top two primary finishers (no candidate won a majority at the May 19, 2020 primary: Theresa Crawford 42.2%, Glen G Diehl 39.7% per contemporaneous reporting; incumbent Kelly L Doherty also stood at the primary per the official voters' pamphlet). Newspaper reports of the certified count give Diehl 2,393 (52.28%) to Crawford 2,182 (47.67%); Morrow County posts no certified 2020 abstract online, so those figures are reported here as unofficial pending the County Clerk's abstract -- a clerk-request item on issue #170.",
     url="https://digitalcollections.library.oregon.gov/assets/displaypdf/24795",
     title="Secretary of State, 2020 Primary Voters' Pamphlet (State Library of Oregon digital copy) -- Morrow County Justice of the Peace candidates"),
   losers=[("theresa-crawford", "Theresa Crawford", "Theresa Crawford")],
   note="Diehl was first appointed Justice of the Peace by Governor Brown in early 2020, then won the November 3, 2020 runoff election; following the appellate-tier precedent, a single elected membership is recorded for the current term with the appointment noted here.",
   bb_note="Oregon Blue Book, Morrow County page (Secretary of State): county officials list 'Justice of the Peace Glen G. Diehl (2027)'."),
 dict(c="sherman", cn="Sherman", pos=None, district=None,
   holder=("shandie-johnson", "Shandie Johnson", "Shandie Johnson"),
   mem=dict(start="2021-01-04", end=None, how="elected"), contest=None,
   extra_sources=[("https://storage.googleapis.com/proudcity/shermancountyor/uploads/2023/12/Elected-Officials-and-Court-Appointments-2024.pdf",
     "Sherman County, Elected Officials & Court Appointments (official county document, December 2023): Shandie Johnson is listed as Justice of the Peace with a term expiring January 2027 and the seat's next election on November 3, 2026 -- a six-year term that began in January 2021. No 2020 certified vote total is recorded; it is a clerk-request item on issue #170.")],
   note="", bb_note="Oregon Blue Book, Sherman County page (Secretary of State): county officials list 'Justice of the Peace Shandie L. Johnson (2031)' -- the county's own officials list gives her term expiring January 2027 and governs; the Blue Book year appears to be an error and is flagged on issue #170."),
 dict(c="tillamook", cn="Tillamook", pos=None, district=None,
   holder=("ryan-connell", "Ryan Connell", "Ryan C Connell"),
   mem=dict(start="2025-01-06", end=None, how="elected"), prior=dict(start="2019-01-02", end="2024-12-31"),
   contest=dict(date="2024-05-21", type="primary",
     figures="Ryan C Connell 5,006 (98.47%), sole candidate; write-in totals 78; total votes cast 5,084; undervotes 3,528.",
     url="https://tillamookcounty.gov/DocumentCenter/View/213/May-21-2024-Primary-Election-Summary-Results",
     title="Tillamook County, Election Summary -- Official Results, May 2024 Primary Election (report dated June 13, 2024)"),
   note="Earlier term documented by the county: a Board of Commissioners order filed November 29, 2018 records that Ryan C. Connell 'has been duly elected as the next Justice of the Peace' with a term starting January 2, 2019, and the county's Annual Comprehensive Financial Reports list his term expiring December 31, 2024 -- a separate prior membership is recorded. The Blue Book's (2029) term attribution conflicts with the May 2024 re-election (term to December 2030) and is flagged on issue #170.",
   bb_note="Oregon Blue Book, Tillamook County page (Secretary of State): county officials list 'Justice of the Peace Ryan Connell (2029)' -- see the note: county documents put his re-election in May 2024."),
 dict(c="union", cn="Union", pos=None, district=None, hold_membership=True,
   holder=("rick-dall", "Rick Dall", "Rick Dall"),
   mem=None,
   contest=dict(date="2022-11-08", type="general",
     figures="Rick Dall 7,938, sole named candidate; write-in totals 112; undervotes 4,590; total votes cast 8,050. Race heading as printed: 'Justice of the Peace COUNTY JUSTICE COURT - Vote For 1'. The county report is precinct-level and prints no contest aggregate; 7,938 is the sum of its 19 precinct rows, re-verified (7,938 + 112 + 4,590 = 12,640, the sum of precinct contest totals). The report does not carry the words 'certified' or 'official' in its extracted text.",
     url="https://unioncountyor.gov/wp-content/uploads/2023/09/2022-11_Final-Precinct.pdf",
     title="Union County, Precinct Results Report -- November 2022 General Election (Final)"),
   note="Dall resigned the seat at an undocumented date; Governor Kotek appointed J. Logan Joseph effective February 1, 2026. No membership is built for Dall: his start is documented by this election but his departure date is not, and it is held as a research item on issue #170 rather than guessed.",
   bb_note="Oregon Blue Book, Union County page (Secretary of State): county officials list 'Justice of the Peace J. Logan Joseph (2029)' -- the appointed successor, not the 2022 winner."),
 dict(c="union", cn="Union", pos=None, district=None, appointee=True,
   holder=("j-logan-joseph", "J. Logan Joseph", "J. Logan Joseph"),
   mem=dict(start="2026-02-01", end=None, how="appointed"), contest=None,
   note="Appointed by Governor Kotek effective February 1, 2026, filling the vacancy left by Judge Rick Dall's resignation (the 2022 election winner). Appointment reporting styles him 'Logan L. Joseph'; the Blue Book lists 'J. Logan Joseph'. The Governor's appointment announcement has not yet been captured as a source; the appointment date is corroborated by news reporting and his Blue Book listing as the sitting Justice of the Peace, and is flagged for verification on issue #170.",
   bb_note="Oregon Blue Book, Union County page (Secretary of State): county officials list 'Justice of the Peace J. Logan Joseph (2029)'."),
 dict(c="washington", cn="Washington", pos=None, district="The Washington County justice district covers part of the county (120,013 ballots cast in the district of 141,228 countywide).",
   holder=("dan-cross", "Dan Cross", "Dan Cross"),
   mem=dict(start="2023-01-02", end=None, how="elected"),
   contest=dict(date="2022-05-17", type="primary",
     figures="Dan Cross 63,586, sole candidate; write-in 1,061 (1.64%); total votes 64,647; undervotes 55,366.",
     url="https://www.washingtoncountyor.gov/elections/documents/may-2022-ballots-cast-contest-precincts/download?inline",
     title="Washington County, Ballots Cast per Contest with Precincts -- May 2022 Primary Election (official results)"),
   note="Washington County's November 2022 official results contain no Justice of the Peace contest; the race was decided at the May primary.",
   bb_note="Oregon Blue Book, Washington County page (Secretary of State): county officials list 'Justice of the Peace Dan Cross (2029)'."),
 dict(c="wheeler", cn="Wheeler", pos=None, district=None,
   holder=("robin-ordway-campbell", "Robin Ordway Campbell", "Robin Ordway"),
   mem=dict(start="2021-01-04", end=None, how="elected"), contest=None,
   extra_sources=[("https://www.wheelercountyoregon.com/justice-court",
     "Wheeler County Justice Court page: the court's Justice of the Peace is Robin Ordway Campbell (styled 'Robin Ordway' on the court's own page and in the voters' pamphlet).")],
   note="Sole candidate for the seat in the official Secretary of State 2020 Primary Voters' Pamphlet (ballot name: Robin Ordway, incumbent); as a nonpartisan office decided by majority at the primary, an unopposed candidate is elected there. Wheeler County posts no certified 2020 results document online, so no vote total is recorded; the certified total is with the County Clerk (Fossil) -- a clerk-request item on issue #170.",
   bb_note="Oregon Blue Book, Wheeler County page (Secretary of State): county officials list 'Justice of the Peace Robin Ordway Campbell (2027)'."),
]

# ---------- collision scan ----------
existing = {}
for root, _dirs, files in os.walk(os.path.join(WS, "people")):
    for fn in files:
        if fn.endswith(".yaml"): existing[fn[:-5]] = os.path.join(root, fn)
new_slugs = set()
for s in SEATS:
    new_slugs.add(s["holder"][0])
    for l in s.get("losers", []): new_slugs.add(l[0])
for slug in sorted(new_slugs):
    if slug in existing and slug != "joe-charter":
        raise SystemExit(f"COLLISION: {slug} already exists at {existing[slug]} -- reuse, do not mint")

# ---------- orgs & posts ----------
org_ids, post_ids = {}, {}
counties = sorted({(s["c"], s["cn"]) for s in SEATS})
for cslug, cname in counties:
    oid = "ocd-organization/" + u5(f"org|or|county|{cslug}-justice-court")
    org_ids[cslug] = oid
    bb = BB[cname]
    content = (f"{HDR}\nid: {oid}\nname: {cname} County Justice Court\njurisdiction_id: {jur_id(cslug)}\nidentifiers: []\nsources:\n"
      + src(bb, f"Oregon Blue Book, {cname} County page (Secretary of State): the county officials list includes a Justice of the Peace, the judge of the county justice court.") + "\n"
      + src(OJD_ABOUT, "Oregon Judicial Department, About page: justice courts are established by counties and are not part of the Oregon Judicial Department; justices of the peace are elected to six-year terms (ORS 51.210).") + "\n")
    write(f"organizations/county/or-{cslug}-justice-court.yaml", content)
seen_posts = set()
for s in SEATS:
    if (s["c"], s["pos"]) in seen_posts: continue
    seen_posts.add((s["c"], s["pos"]))
    cslug, pos = s["c"], s["pos"]
    stem = f"or-{cslug}-justice-of-the-peace" + (f"-position-{pos}" if pos else "")
    pid = f"or-{cslug}/justice-of-the-peace" + (f"-position-{pos}" if pos else "")
    post_ids[(cslug, pos)] = (pid, stem)
    title = "Justice of the Peace" + (f", Position {pos}" if pos else "")
    note = f"Oregon Blue Book, {s['cn']} County page (Secretary of State): county officials list {s['bb_note'].split(': ',1)[1] if ': ' in s['bb_note'] else s['bb_note']}"
    content = (f"{HDR}\nid: {pid}\norganization_id: {org_ids[cslug]}\ntitle: {title}\nseats: 1\nidentifiers: []\nsources:\n"
      + src(BB[s["cn"]], note) + "\n")
    if s.get("district"):
        content = content.rstrip("\n") + "\n" + src(BB[s["cn"]], s["district"]) + "\n"
    write(f"posts/county/{stem}.yaml", content)

# ---------- people, candidacies, memberships, contests ----------
elections = {}  # (county, date, type) -> [contest yaml blocks]
election_srcs = {}
def person_file(slug, name, candidacies, sources):
    cand = "candidacies: []\n" if not candidacies else "candidacies:\n" + "".join(candidacies)
    body = (f"{HDR}\nid: ocd-person/{u5(f'person|or|county|{slug}')}\nname: {name}\nidentifiers: []\n" + cand
      + f"verification:\n  status: machine-extracted\n  reviewed_on: '{DATE}'\n  pipeline: build_or_jp\nsources:\n"
      + "\n".join(sources) + "\n")
    write(f"people/county/{slug}.yaml", body)
    return "ocd-person/" + u5(f"person|or|county|{slug}")

def cand_block(contest_id, election_id, jid, office_id, ballot):
    return (f"- contest_id: {contest_id}\n  election_id: {election_id}\n  jurisdiction_id: {jid}\n"
            f"  office_id: {office_id}\n  party: Nonpartisan\n  ballot_name: {ballot}\n  status: active\n")

def membership(slug, name, s, mem, stem_suffix=""):
    pid, stem = post_ids[(s["c"], s["pos"])]
    mstem = f"{stem}-{slug}{stem_suffix}"
    lines = [HDR, f"id: {mstem}", f"person_id: ocd-person/{u5(f'person|or|county|{slug}')}" if slug != 'joe-charter' else f"person_id: ocd-person/2a1caefe-9648-5615-bd18-1a79949d5425",
             f"organization_id: {org_ids[s['c']]}", f"post_id: {pid}", "role: Justice of the Peace", f"start: '{mem['start']}'"]
    if mem.get("end"): lines.append(f"end: '{mem['end']}'")
    lines.append(f"how_seated: {mem['how']}")
    srcs = []
    if s.get("contest"):
        srcs.append(src(s["contest"]["url"], f"{s['contest']['title']}: {s['contest']['figures']}"))
    srcs.append(src(BB[s["cn"]], s["bb_note"]))
    for u, n in s.get("extra_sources", []): srcs.append(src(u, n))
    if s.get("note"): srcs.append(src(BB[s["cn"]], s["note"]))
    lines.append("sources:\n" + "\n".join(srcs))
    write(f"memberships/county/{mstem}.yaml", "\n".join(lines) + "\n")

charter_append = None
for s in SEATS:
    slug, name, ballot = s["holder"]
    pid, stem = post_ids[(s["c"], s["pos"])]
    cands, psrcs = [], []
    if s.get("contest"):
        ct = s["contest"]
        cid = f"{s['c']}/{ct['date']}/justice-of-the-peace" + (f"-position-{s['pos']}" if s["pos"] else "")
        eid = f"{s['c']}/{ct['date']}/{ct['type']}"
        cands.append(cand_block(cid, eid, jur_id(s["c"]), pid, ballot))
        psrcs.append(src(ct["url"], f"{ct['title']}: {ct['figures']}"))
        key = (s["c"], s["cn"], ct["date"], ct["type"])
        person_id = "ocd-person/2a1caefe-9648-5615-bd18-1a79949d5425" if slug == "joe-charter" else "ocd-person/" + u5(f"person|or|county|{slug}")
        election_srcs.setdefault(key, []).append((ct["url"], ct["title"]))
        elections.setdefault(key, []).append(
          f"- id: {cid}\n  jurisdiction_id: {jur_id(s['c'])}\n  office_id: {pid}\n  vote_for: 1\n  candidate_ids:\n  - {person_id}\n  result_status: certified\n  winners:\n  - person_id: {person_id}\n    name: {name}\n")
    psrcs.append(src(BB[s["cn"]], s["bb_note"]))
    for u, n in s.get("extra_sources", []): psrcs.append(src(u, n))
    if s.get("note"): psrcs.append(src(BB[s["cn"]], s["note"]))
    if slug == "joe-charter":
        charter_append = (cands, psrcs)
    else:
        person_file(slug, name, cands, psrcs)
    for lslug, lname, lballot in s.get("losers", []):
        ct = s["contest"]
        cid = f"{s['c']}/{ct['date']}/justice-of-the-peace" + (f"-position-{s['pos']}" if s["pos"] else "")
        eid = f"{s['c']}/{ct['date']}/{ct['type']}"
        person_file(lslug, lname, [cand_block(cid, eid, jur_id(s["c"]), pid, lballot)],
                    [src(ct["url"], f"{ct['title']}: {ct['figures']}")])
    if s.get("mem") and not s.get("hold_membership"):
        if s.get("prior"):
            s_prior = dict(s); s_prior["contest"] = None
            membership(slug, name, s_prior, dict(start=s["prior"]["start"], end=s["prior"]["end"], how="elected"), "-2019")
            membership(slug, name, s, s["mem"], "-2025")
        else:
            membership(slug, name, s, s["mem"])

# Charter: append JP candidacy to his existing person file
p = os.path.join(WS, "people/judicial-district/joe-charter.yaml")
text = open(p).read()
cands, psrcs = charter_append
assert "justice-of-the-peace" not in text
text = text.replace("verification:", "".join(cands) + "verification:", 1)
text = text.rstrip("\n") + "\n" + "\n".join(psrcs) + "\n"
with open(p, "w") as f: f.write(text)
edited.append("people/judicial-district/joe-charter.yaml")
# ---------- election files ----------
for (cslug, cname, date, etype), blocks in sorted(elections.items()):
    eid = f"{cslug}/{date}/{etype}"
    hdr_note = (f"# Built for issue #170 (Oregon master tracking): Justice of the Peace\n"
                f"# contest(s) from {cname} County's official results for this election.\n"
                f"# Oregon nonpartisan judicial races are decided at the primary when a\n"
                f"# candidate wins a majority; only races without a primary majority\n"
                f"# reach the general election.")
    src_lines = []
    seen_src = set()
    for u, ti in election_srcs.get((cslug, cname, date, etype), []):
        if u in seen_src: continue
        seen_src.add(u)
        src_lines.append(src(u, ti + "."))
    body = (f"{hdr_note}\nid: {eid}\nname: {cname} County {date} {etype} election\ndate: '{date}'\n"
            f"election_type: {etype}\nstatus: official\ncontests:\n" + "".join(blocks)
            + "sources:\n" + "\n".join(src_lines) + "\n")
    write(f"elections/{cslug}--{date}--{etype}.yaml", body)

print(f"created {len(created)} files, edited {len(edited)}")
from collections import Counter
print(Counter(p.split('/')[0] for p in created))
print("election files:", len(elections))
