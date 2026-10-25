#!/usr/bin/env python3
"""Build OR_Municipalities.xlsx for Civic-Data issue #170 (Oregon tracking).

Mirrors the VT_Municipalities.xlsx format (itself modeled on
MS_Municipalities / TX_Municipalities): README, Government Structure,
Municipalities, School Districts, Counties, Office Titles (Ref), Sources,
Status Log, Open Issues (last, per Walter 2026-10-23).

Seeds are read from the repo's Oregon jurisdiction files (themselves seeded
from the U.S. Census Bureau 2022 Census of Governments). Creyton Loud's OR
Jurisdiction Factory v0.1 is a lead layer only and is registered in Sources
as such -- never a source of record.
"""
import re
import sys
from pathlib import Path

import yaml
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

REPO = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/home/hatch/workspace/civic-data-or170")
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("/home/hatch/workspace/or170/OR_Municipalities.xlsx")
ORDIR = REPO / "data/us/or/jurisdictions"

BOLD = Font(bold=True)
WRAP = Alignment(wrap_text=True, vertical="top")
TOP = Alignment(vertical="top")


def style_sheet(ws, widths, wrap_cols=()):
    for cell in ws[1]:
        if cell.value is not None:
            cell.font = BOLD
    ws.freeze_panes = "A2"
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        for cell in row:
            cell.alignment = WRAP if (cell.column in wrap_cols) else TOP


def load_jurisdictions(sub):
    out = []
    for p in sorted((ORDIR / sub).glob("*.yaml")):
        d = yaml.safe_load(p.read_text())
        note = ""
        for s in d.get("sources") or []:
            note = s.get("note", "") or note
        m = re.search(r"county area=([A-Z .']+)", note)
        fips = re.search(r"FIPS (41-\d{3})", note)
        out.append({
            "name": d.get("name", ""),
            "id": d.get("id", ""),
            "website": d.get("website") or "Needs Research",
            "county": m.group(1).title() if m else "Needs Research",
            "fips": fips.group(1) if fips else "Needs Research",
        })
    return out


municipal = load_jurisdictions("municipal")
counties = load_jurisdictions("county")
assert len(municipal) == 240, len(municipal)
assert len(counties) == 36, len(counties)

wb = Workbook()

# ---------------- README ----------------
ws = wb.active
ws.title = "README"
ws["A1"] = "OR_Municipalities -- Sheet Guide"
ws["A2"] = ("Master reference workbook for CivicMirror's Oregon elected-office audit (issue #170, OR master tracking). "
            "Modeled on VT_Municipalities (itself modeled on MS_Municipalities / TX_Municipalities). Enumerations are seeded from official, "
            "automatable sources (the repo's jurisdiction files, built from the U.S. Census Bureau 2022 Census of Governments); per-city charters, "
            "codes, and websites are backfilled from official city/county sources during each pass. Sourcing rules: official sources only; the League of "
            "Oregon Cities is an association source -- used to locate and verify, not as source of record, mirroring the MS MML / VT VLCT rule. Creyton Loud's "
            "OR Jurisdiction Factory v0.1 is a LEAD LAYER ONLY (read-only, verify against the official source it cites, flag divergences on #170) -- never a source of record.")
ws.append([])
ws.append(["Sheet", "What it tracks", "Coverage / Status"])
guide = [
    ("README", "This guide. Regenerate coverage counts whenever another sheet's row counts change.", "--"),
    ("Government Structure", "How Oregon government is organized at each level, which offices are elected vs appointed, terms, and the statute/constitution basis. Oregon has no Lieutenant Governor (the Secretary of State is first in succession) and its counties ARE general-purpose governments, unlike Vermont's.", "Structure determined 2026-10-23 (issue #170 first pass). Federal tier built; statewide executive and legislative tiers built (PR #171); judicial, county, municipal, then schools / ESDs / special districts pending in Walter's order."),
    ("Municipalities", "Every Oregon city in the repo: 240 cities (all home-rule charters), with county, jurisdiction ID, website on file, and charter/code backfill status. The Census-seeded count of 241 included a stray file -- the Township of Auburn, Susquehanna County, PENNSYLVANIA (FIPS 42-115-03496), misfiled under state:or -- removed 2026-10-23 (PR #171); Auburn, Oregon is a deserted Baker County ghost town, never an incorporated city. 240 now matches Creyton Loud's factory and the League of Oregon Cities count exactly.", "240 cities -- jurisdiction scaffolds only; municipal pass runs fifth (alphabetical batches of 10), factory as lead layer."),
    ("School Districts", "Oregon school districts, Education Service Districts, and special districts. School boards are elected (May odd-year elections); the 19 ESD boards are mixed elected/appointed and need a #158-style classification; the ~1,035 special districts are mostly elected boards, with the restricted-franchise rule applied district by district.", "0 districts seeded -- this pass runs LAST, after municipalities (Walter, 2026-10-23). Sheet carries headers only until then."),
    ("Counties", "The 36 counties with FIPS, county website, and elected-office build status. Officer sets vary: most counties elect Sheriff / Clerk / Assessor / Treasurer / Commissioners under ORS 204.005, County Court counties elect a County Judge + 2 commissioners, every county elects a District Attorney (ORS 8.610), and 9 home-rule charters vary the set -- per-county charter check required.", "36 counties -- BUILT 2026-10-25 (county pass, PR #171): governing body, row offices and District Attorney in every county, from the Blue Book rosters, each county's own website and the certified state abstracts (1,110 new files across seven commits, Baker as worked example plus six batches)."),
    ("Office Titles (Ref)", "Reference: which state / county / municipal offices are popularly elected, with statute basis. Per-county and per-city variation (charters) is resolved during each pass.", "Reference -- verify per county / per city."),
    ("Sources", "Source registry for this workbook and the OR build.", "Seed sources registered."),
    ("Status Log", "Dated log of workbook changes.", "Opened 2026-10-23."),
    ("Open Issues", "Every flagged item from the OR run: factory-vs-official divergences, factory gaps, and verifications owed, tracked as they pop up until resolved.", "13 items (2026-10-25): items 1, 2, 3 and 5 resolved by the county pass; items 6-13 are the county pass's own holds, conflicts and forward watches."),
]
for row in guide:
    ws.append(list(row))
ws.column_dimensions["A"].width = 26
ws.column_dimensions["B"].width = 110
ws.column_dimensions["C"].width = 60
for cell in ws[4]:
    cell.font = BOLD
ws["A1"].font = Font(bold=True, size=13)
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    for cell in row:
        cell.alignment = WRAP

# ---------------- Government Structure ----------------
ws = wb.create_sheet("Government Structure")
ws.append(["Level", "Body / Office", "Elected?", "Term", "Seats / Districts", "Basis", "Notes"])
gov = [
    ("Federal", "U.S. Representative", "Elected", "2 years", "6 seats (CD-1 to CD-6)", "U.S. Const.", "Already in repo (federal tier complete for OR: Bonamici, Bentz, Dexter, Hoyle, Bynum, Salinas)."),
    ("Federal", "U.S. Senator", "Elected", "6 years", "2 seats (Class 2, Class 3)", "U.S. Const.", "Already in repo (Merkley Class 2, Wyden Class 3)."),
    ("State", "Governor", "Elected", "4 years", "1", "Or. Const. Art. V", "BUILT (PR #171): Tina Kotek, 2022 general election (SOS certified abstract: 917,074). Next election Nov 3, 2026."),
    ("State", "Secretary of State", "Elected", "4 years", "1", "Or. Const. Art. VI", "First in line of succession -- Oregon has NO Lieutenant Governor. BUILT (PR #171): Tobias Read, 2024 general election (SOS certified abstract: 1,166,447); sworn in Jan 6, 2025."),
    ("State", "State Treasurer", "Elected", "4 years", "1", "Or. Const. Art. VI", "BUILT (PR #171): Elizabeth Steiner, 2024 general election (SOS certified abstract: 1,050,119); sworn in Jan 6, 2025."),
    ("State", "Attorney General", "Elected", "4 years", "1", "ORS 180.010 et seq.", "BUILT (PR #171): Dan Rayfield, 2024 general election (SOS certified abstract: 1,156,489); sworn in Dec 31, 2024 on the early resignation of Ellen Rosenblum."),
    ("State", "Commissioner of Labor and Industries", "Elected (nonpartisan)", "4 years", "1", "ORS 651.030", "BUILT (PR #171): Christina Stephenson, 2022 general election (SOS certified abstract: 916,455, nonpartisan); assumed office Jan 2, 2023. Re-elected in the May 2026 primary (majority in May under the nonpartisan rule)."),
    ("State", "Superintendent of Public Instruction", "APPOINTED -- out of elected scope", "--", "--", "ORS 326.300", "Appointed by the Governor; the formerly elected office was abolished. Excluded."),
    ("State", "Supreme Court", "Elected (nonpartisan)", "6 years", "7 positions", "Or. Const. Art. VII; ORS 2.020", "BUILT (PR #171, appellate tier of the judicial pass): all 7 positions + holders from the certified SOS Abstracts of Votes (2020/2022/2024, primary + general). Appointee-then-elected justices (Bushong Pos 1, James Pos 7, Masih Pos 5, DeHoog Pos 6) carry appointed + elected memberships; departed 2020 winners Balmer (Pos 1) and Walters (Pos 7) carry ended memberships. Chief Justice: Meagan Flynn (Pos 3), since Jan 2023."),
    ("State", "Court of Appeals", "Elected (nonpartisan)", "6 years", "13 positions", "ORS 2.540", "BUILT (PR #171, appellate tier of the judicial pass): all 13 positions + holders from the certified SOS abstracts. Appointee-then-elected judges (Pagan Pos 8, Kamins Pos 9, Joyce Pos 11) carry appointed + elected memberships; departed 2020 winner DeVore (Pos 11) carries an ended membership (year-precision end)."),
    ("State", "Tax Court", "Elected (nonpartisan)", "6 years", "1 judge", "ORS 305.400s", "BUILT (PR #171, appellate tier of the judicial pass): Judge Robert Manicke, re-elected in the May 21, 2024 primary (566,517, certified abstract). The Tax Court race appears in the primary abstract under 'Judge of the Oregon Tax Court' with no position line."),
    ("State", "Circuit Courts", "Elected (nonpartisan)", "6 years", "27 judicial districts, 186 positions", "Or. Const. Art. VII; ORS 3.010 / 3.012", "BUILT (PR #171, circuit tier of the judicial pass): all 27 district jurisdictions + court organizations, all 186 posts (the OJD judges-directory count -- the directory runs ahead of the ORS 3.012 text in Districts 1, 2, 5, 16 and 20, which have recently created judgeships), 200 deciding contests from the certified SOS abstracts appended to the six election files, and elected memberships for the 169 seats whose holder's class-aligned win fully determines the seating. Memberships at 17 seats are held for the research step (5 new-judgeship appointees, 4 departure->appointment seats, 4 class contradictions, 3 vacancies, 1 surname-masked succession at 20-14); the 12 winner-not-seated validation warnings are that queue."),
    ("County / justice districts", "Justices of the Peace", "Elected (nonpartisan)", "6 years", "22 seats in 21 counties (Douglas has 2 districts)", "ORS 51.210", "BUILT (PR #171, JP slice of the judicial pass, commit 2beb5a1): one Justice Court organization per county on the existing county jurisdictions, 22 posts, 28 new people, 25 memberships, 14 contests in 13 new county election files from county official results (the state abstracts carry no JP races). Denominator = SOS Blue Book county pages: 22 seats -- the factory's 20 missed Hood River and Union. Three holders are gubernatorial appointees (Rastetter/Clackamas 2026, Hayter/Gilliam 2024, Joseph/Union 2026); Union's 2022 winner Dall is held without a membership (resignation date undocumented -- the tier's one winner-not-seated warning). Blue Book term years were wrong for Hood River, Klamath, Sherman and Tillamook and were overridden by county documents, disclosed in the source notes. Certified totals not posted online for Baker, Harney, Wheeler, Klamath, Lane, Linn, Sherman and Gilliam-2020 are clerk-request items."),
    ("State", "State Senate", "Elected", "4 years (staggered, 15 per cycle)", "30 districts", "Or. Const. Art. IV", "BUILT (PR #171): all 30 district jurisdictions + posts + holders from the certified SOS abstracts (2024 class: Districts 1, 2, 5, 9, 12, 14, 18, 21, 22, 23, 25, 27, 28, 29, 30; 2022 class: the other 15, plus the District 18 two-year-term contest). Mid-term appointments modeled in Districts 13, 17, 26. Each Senate district = exactly 2 House districts."),
    ("State", "State House of Representatives", "Elected", "2 years", "60 districts", "Or. Const. Art. IV", "BUILT (PR #171): all 60 district jurisdictions + posts + holders from the certified 2024 SOS abstract. Mid-term appointments modeled in Districts 26, 34, 48, 51 (District 34: the re-elected winner resigned before the term began -- candidacy recorded, no membership). All 60 seats up Nov 3, 2026."),
    ("Judicial", "Supreme Court", "Elected (nonpartisan)", "6 years", "7 justices, statewide", "Or. Const. Art. VII; ORS ch. 2", "Judicial pass -- sits directly under the legislative pass (Walter, 2026-10-23)."),
    ("Judicial", "Court of Appeals", "Elected (nonpartisan)", "6 years", "13 judges, statewide", "ORS ch. 2", "Judicial pass."),
    ("Judicial", "Tax Court", "Elected (nonpartisan)", "6 years", "1 judge, statewide", "ORS ch. 305", "Judicial pass."),
    ("Judicial", "Circuit Courts", "Elected (nonpartisan)", "6 years", "27 judicial districts", "ORS ch. 3", "Judicial pass. District lines follow county boundaries (some multi-county)."),
    ("Judicial", "Justice of the Peace (Justice Courts)", "Elected (nonpartisan)", "6 years", "1 per justice district", "ORS 51.210", "County-authorized courts, NOT part of the Oregon Judicial Department. Verified denominator is 22 seats in 21 counties (Blue Book county pages) -- the factory's 20 missed Hood River and Union; built in the judicial pass (PR #171). County Court judicial functions in County Court counties sit here too."),
    ("Judicial", "Municipal court judges", "APPOINTED -- out of elected scope", "--", "--", "City charters", "Excluded."),
    ("County", "Board of County Commissioners", "Elected", "4 years (staggered)", "30 counties (3 or 5 seats)", "ORS 204.013 / 204.017", "BUILT (PR #171, county pass 2026-10-25): numbered posts where the county's own listing gives positions or districts, one multi-seat post where it does not (Walter's rule, from his Baker/Jefferson checks). Separately elected Chairs in Clackamas, Hood River, Multnomah and Washington. Two seats sit vacant: Lincoln Position 2 and the Washington County Chair."),
    ("County", "County Court (County Judge + 2 Commissioners)", "Elected", "6 years (Judge) / 4 years (Commissioners)", "6 counties: Gilliam, Grant, Harney, Malheur, Sherman, Wheeler", "ORS ch. 204 / 205", "BUILT (PR #171, county pass 2026-10-25). The three-way divergence is resolved: the factory's six are exactly right -- Morrow is a Board of Commissioners on its own documents (Open Issues #1), and CROOK is also a Board of Commissioners on its own budget documents, superseding the Blue Book's County Court listing. Harney and Malheur judgeships were seated from the certified May 2022 County Judge contests in the state abstract; Gilliam's judge (Patnode, the former JP) was appointed in June 2024 after winning the primary."),
    ("County", "Sheriff / County Clerk / County Assessor / County Treasurer", "Elected", "4 years", "1 per county each (where the office exists)", "ORS 204.005", "BUILT (PR #171, county pass 2026-10-25). The charter counties vary the set sharply, verified county by county: Benton, Clatsop, Hood River, Lane, Multnomah, Umatilla and Washington each appoint or abolish several of these offices (Multnomah and Umatilla elect only the board, Sheriff, DA -- and Multnomah an Auditor). Assessor/Tax Collector is a combined elected office in Clackamas, Grant, Lake, Linn, Morrow, Union, Wasco and Yamhill; Josephine also elects a county Legal Counsel."),
    ("County", "County Surveyor", "Elected where not made appointive", "4 years", "Elected in 19 counties", "ORS 204.005", "BUILT where elected (PR #171): appointed in Benton, Clatsop, Columbia, Curry, Deschutes, Gilliam, Lincoln, Malheur, Sherman, Tillamook, Yamhill and others; not modeled where the county makes it appointive. One man, Michael Springer, is elected Surveyor of both Grant and Wheeler counties (modeled as one person, disclosed)."),
    ("County", "District Attorney", "Elected", "4 years", "1 per county (36)", "ORS 8.610", "BUILT (PR #171, county pass 2026-10-25): every county's DA seated from the certified state abstracts -- the only county office the abstracts carry -- in two classes (21 counties elected 2024, 15 elected 2022) plus November specials in Columbia and Klamath (2024) and the Lincoln 2020 general precedent. The factory's Clatsop and Hood River gaps were factory errors (Open Issues #2-3, resolved). Mid-term turnovers built: Curry (Spansail -> Kelley), Gilliam (Davis -> Rodighiero; Davis is now Wasco's DA on the same person record). Jefferson's winner (Leriche) is contest-only -- his service is undocumented (Open Issues #8)."),
    ("Municipal", "Mayor + City Council", "Elected", "Charter terms (2-4 years typical)", "240 cities", "City charters (all home-rule)", "Every Oregon city is a home-rule charter city -- mayor/council set, titles, and terms come from each city charter. Municipal pass (fifth), alphabetical batches of 10, factory as lead layer."),
    ("School", "School district boards", "Elected", "4 years", "District count to verify against ODE", "ORS ch. 332", "Elections in May of odd years. School pass runs LAST (Walter, 2026-10-23)."),
    ("School", "Education Service District boards", "MIXED -- elected/appointed by district", "4 years", "19 ESDs", "ORS ch. 334", "Needs a #158-style per-district classification in the school pass."),
    ("Special districts", "Fire / water / port / park / library / SWCD and other special district boards", "Mostly elected boards", "Varies", "~1,035 districts (OCCMA count)", "ORS ch. 198 et seq.", "Deferred to the final pass with schools. The restricted-franchise rule (Walter, 2026-10-15) applies district by district: a body the general public cannot vote for is out of scope. Port of Portland commissioners are Governor-appointed -- out."),
]
for r in gov:
    ws.append(list(r))
style_sheet(ws, [18, 44, 18, 30, 34, 40, 95], wrap_cols=(2, 5, 6, 7))

# ---------------- Municipalities ----------------
ws = wb.create_sheet("Municipalities")
ws.append(["Municipality Name", "Type", "County", "Jurisdiction ID", "Municipal Website", "Charter", "Municipal Code Link", "Code Host", "Status", "Notes"])
for j in municipal:
    name = j["name"]
    if name.startswith("City of "):
        name = name[len("City of "):]
    elif name.startswith("Town of "):
        name = name[len("Town of "):]
    ws.append([name, "City", j["county"], j["id"], j["website"],
               "Home-rule charter -- link to verify at municipal pass", "Needs Research", "",
               "Scaffold only",
               "Census 2022-seeded jurisdiction scaffold; no posts built yet. Municipal pass: alphabetical batches of 10, factory v0.1 as lead layer."])
style_sheet(ws, [24, 10, 16, 58, 34, 22, 22, 12, 16, 80], wrap_cols=(6, 10))

# ---------------- School Districts ----------------
ws = wb.create_sheet("School Districts")
ws.append(["District Name", "Type", "Education Service District", "Jurisdiction ID", "District Website", "Posts", "Memberships", "Status", "Notes"])
style_sheet(ws, [42, 16, 26, 58, 30, 7, 12, 30, 70], wrap_cols=(9,))

# ---------------- Counties ----------------
ws = wb.create_sheet("Counties")
ws.append(["County Name", "County FIPS", "County Website", "Elected Offices in Repo", "Status", "Jurisdiction ID"])
for j in counties:
    name = j["name"]
    if name.startswith("County of "):
        name = name[len("County of "):]
    ws.append([name, j["fips"], j["website"], "Governing body, elected row offices and District Attorney built 2026-10-25", "Built -- county pass (PR #171)", j["id"]])
style_sheet(ws, [18, 12, 20, 90, 16, 58], wrap_cols=(4,))

# ---------------- Office Titles (Ref) ----------------
ws = wb.create_sheet("Office Titles (Ref)")
ws.append(["Office", "Popularly Elected?", "Statute / Basis", "Notes"])
titles = [
    ("Governor", "Elected", "Or. Const. Art. V", "Statewide, 4-year term. Built (PR #171)."),
    ("Secretary of State", "Elected", "Or. Const. Art. VI", "First in succession (no Lieutenant Governor in Oregon)."),
    ("State Treasurer", "Elected", "Or. Const. Art. VI", ""),
    ("Attorney General", "Elected", "ORS 180.010 et seq.", ""),
    ("Commissioner of Labor and Industries", "Elected (nonpartisan)", "ORS 651.030", "The one nonpartisan statewide executive office."),
    ("State Senator", "Elected", "Or. Const. Art. IV", "30 districts, 4-year staggered terms."),
    ("State Representative", "Elected", "Or. Const. Art. IV", "60 districts, 2-year terms; each Senate district nests exactly 2 House districts."),
    ("Supreme Court Justice", "Elected (nonpartisan)", "Or. Const. Art. VII; ORS ch. 2", "7 justices, 6-year terms, statewide."),
    ("Court of Appeals Judge", "Elected (nonpartisan)", "ORS ch. 2", "13 judges, 6-year terms, statewide."),
    ("Tax Court Judge", "Elected (nonpartisan)", "ORS ch. 305", "1 judge, 6-year term, statewide."),
    ("Circuit Court Judge", "Elected (nonpartisan)", "ORS ch. 3", "27 judicial districts, 6-year terms."),
    ("Justice of the Peace", "Elected (nonpartisan)", "ORS 51.210", "One per justice district, 6-year term; county-authorized, outside the OJD."),
    ("County Commissioner", "Elected", "ORS 204.013 / 204.017", "Numbered positions; 3 or 5 per board in most counties; 2 alongside a County Judge in County Court counties."),
    ("County Judge", "Elected", "ORS ch. 204 / 205", "Chairs the County Court and carries judicial functions. Factory: 6 counties."),
    ("Sheriff", "Elected", "ORS 204.005", "Verify per county charter."),
    ("County Clerk", "Elected", "ORS 204.005", "Combined or appointed in some home-rule counties."),
    ("County Assessor", "Elected", "ORS 204.005", "Combined or appointed in some home-rule counties."),
    ("County Treasurer", "Elected", "ORS 204.005", "Combined or appointed in some home-rule counties."),
    ("County Surveyor", "Elected (conditional)", "ORS 204.005", "Elected only where charter/ordinance has not made it appointive."),
    ("County Auditor", "Elected (where it exists)", "County charters", "Factory models 2 (home-rule counties)."),
    ("District Attorney", "Elected", "ORS 8.610", "One per county, 4-year term."),
    ("Mayor", "Elected", "City charter", "All 240 cities are home-rule; verify title/term per charter."),
    ("City Council Member", "Elected", "City charter", "Titles vary by charter (Councilor, Council Member, Commissioner in Portland's former system)."),
    ("School Board Member", "Elected", "ORS ch. 332", "May odd-year elections, 4-year terms. School pass runs last."),
    ("ESD Board Member", "MIXED", "ORS ch. 334", "Elected or appointed by district -- classification owed in the school pass."),
]
for r in titles:
    ws.append(list(r))
style_sheet(ws, [30, 22, 36, 95], wrap_cols=(4,))

# ---------------- Sources ----------------
ws = wb.create_sheet("Sources")
ws.append(["Source", "Level", "Official?", "Automation", "URL", "Provides", "Status", "Notes"])
sources = [
    ("U.S. Census Bureau -- 2022 Census of Governments, Government Units Listing", "State", "Official (federal)", "Bulk download", "https://www.census.gov/data/datasets/2022/econ/gus/public-use-files.html", "Enumeration of OR general-purpose governments seeded into repo jurisdiction files (2026-08-17).", "USED -- seeded repo jurisdictions", "Municipality / county mapping, FIPS, and websites in this workbook trace to these files."),
    ("Oregon Secretary of State, Elections Division -- Abstracts of Votes", "State", "Official (state)", "PDF download", "https://sos.oregon.gov/elections/Pages/records.aspx", "Certified general-election results by contest (2022 abstract used for the Governor step).", "USED -- Governor (2022)", "Source of record for candidacies, winners, and vote totals."),
    ("Oregon Revised Statutes (Oregon Legislature)", "State", "Official (state)", "Web", "https://www.oregonlegislature.gov/bills_laws/Pages/ORS.aspx", "Office structure and terms: ORS 204.005 (county officers), 8.610 (district attorneys), 51.210 (justices of the peace), ch. 332/334 (schools/ESDs).", "USED -- structure pass (issue #170)", "Cite the Legislature as source of record."),
    ("Oregon Blue Book (Secretary of State)", "State", "Official (state)", "Web", "https://sos.oregon.gov/blue-book/Pages/default.aspx", "Official directory of state/county officials and government structure; its county pages list each county's officers including Justices of the Peace.", "USED -- JP denominator (all 36 county pages)", "Directory aid; election facts come from certified results. The Blue Book is stale for Clackamas (pre-retirement) and its term years were wrong for Hood River, Klamath, Sherman and Tillamook -- county documents governed there, disclosed in the repo source notes."),
    ("County clerks' certified election results (per county)", "County", "Official (county)", "PDF download / web", "Per-county clerk pages", "Certified Justice of the Peace results, which the state abstracts do not carry: Columbia, Douglas, Grant, Malheur, Tillamook, Clackamas, Deschutes, Hood River, Marion, Washington, Jackson, Morrow, Union documents used for the JP tier.", "USED -- JP contests", "Retrieval gaps (Laserfiche/PDF viewers) were pulled in a live browser. Eight seats have no certified total posted online (clerk-request items)."),
    ("Oregon Judicial Department", "Judicial", "Official (state)", "Web", "https://www.courts.oregon.gov/about/Pages/default.aspx", "Court structure: Supreme Court, Court of Appeals, Tax Court, 27 circuit-court districts; County Court counties.", "USED -- structure pass (issue #170)", "Justice Courts are county-authorized and outside the OJD -- verify JPs per county."),
    ("League of Oregon Cities", "Municipal", "Association", "Web", "https://www.orcities.org/about/how-we-work", "City count (241 incorporated cities incl. the former Auburn listing question; 240 govern after the Auburn correction) and charter-city orientation.", "USED -- locate/verify only", "Association source: used to locate and verify, NOT as source of record (mirrors the MS MML / VT VLCT rule)."),
    ("Creyton Loud -- OR Jurisdiction Factory v0.1 (Google Sheet)", "County / Municipal", "NOT official -- lead layer", "Sheets API / export", "https://docs.google.com/spreadsheets/d/15A-_pC85UZevw2bInfn4bG-3Zuya_KwFJl_cm1TWMXw", "277 jurisdictions (36 counties, 240 cities), 1,844 offices, 1,809 people/role terms, 1,485 evidence rows -- county and municipal tiers only.", "USED -- concordance posted to #170 (2026-10-23)", "Creyton Loud's file, shared for collaboration; READ-ONLY. Verify every roster against the official source its evidence rows cite before minting; flag divergences on #170."),
]
for r in sources:
    ws.append(list(r))
style_sheet(ws, [44, 14, 16, 16, 52, 62, 30, 62], wrap_cols=(1, 6, 8))

# ---------------- Status Log ----------------
ws = wb.create_sheet("Status Log")
ws.append(["Date", "Change", "Sheets affected", "Source(s)", "By"])
log = [
    ("2026-10-23", "Created workbook for issue #170 in the VT_Municipalities format (9 sheets, Open Issues last per Walter). Government Structure determined from ORS / OJD / SOS; Municipalities seeded with all 240 repo city jurisdictions and Counties with all 36, from the Census-seeded repo jurisdiction files. Build order (Walter): Governor, statewide executive, legislative, judicial, county, municipal, then schools / ESDs / special districts last.", "All", "Or. Const.; ORS (oregonlegislature.gov); OJD; SOS Elections Division; Census 2022 Census of Governments via repo files", "CivicMirror"),
    ("2026-10-23", "Governor step built on tracking branch or-170-master-tracking (PR #171): state executive jurisdiction, Governor post, Tina Kotek person + membership, 2022 general election contest. Validation on the OR tree PASSED, 0 errors.", "Government Structure", "SOS November 8, 2022 General Election Abstract of Votes (certified); oregon.gov", "CivicMirror"),
    ("2026-10-23", "Auburn scaffold removed (PR #171): the file under data/us/or was the Township of Auburn, Susquehanna County, Pennsylvania (FIPS 42-115-03496 per its own Census source note), misfiled under state:or; PA already carries its own correct record. Auburn, Oregon is a deserted Baker County ghost town (post office closed 1903), not an incorporated city. Municipalities 241 -> 240, now an exact match with the factory and the League of Oregon Cities count.", "Municipalities, README", "Repo jurisdiction file source note (Census 2022 CoG); A.R. Bowman Museum / Baker County history; League of Oregon Cities", "CivicMirror"),
    ("2026-10-23", "Judicial pass, appellate tier built on PR #171 (commit 9807891): state judiciary jurisdiction + Supreme Court (7), Court of Appeals (13) and Tax Court (1) organizations, posts, holders and 24 contests across six election files (new 2020 primary, 2020 general, 2022 primary, 2024 primary files; contests appended to the 2022/2024 general files), all from the certified SOS Abstracts of Votes. Oregon judicial races are decided at the May primary on a majority, so the primary abstracts carry most of the bench. Seven holders carry appointed + elected membership pairs (Bushong, James, Masih, DeHoog, Pagan, Kamins, Joyce) and three departed 2020 winners carry ended memberships (Balmer, Walters, DeVore). Validation PASSED, 0 errors, 10 warnings (9 baseline + HD34 by-design). Circuit Courts and Justices of the Peace remain in the judicial pass.", "Government Structure, Status Log", "SOS Abstracts of Votes 2020-2024 (Archives uris 13735448-13735458); Governor's appointment releases (Brown Dec 2022 / Jan 19, 2022; Kotek Aug 16, 2023); OSB Capitol Insider (Balmer/Walters retirements)", "CivicMirror"),
    ("2026-10-23", "Walter's order rulings recorded: judicial sits directly under legislative; schools / ESDs / special districts run after the municipal pass; XLSX workbook ruled IN (this file). JUD / ESD / SPC settled; no scope items left parked.", "README, Government Structure, Status Log", "Walter, via #170 side chat 2026-10-23", "CivicMirror"),
    ("2026-10-23", "Legislative pass built on PR #171: 90 district jurisdictions + organizations + posts (Senate 30, House 60), 93 new people, 96 memberships, and 91 legislative contests appended to the 2022 and 2024 general election files, all from the certified SOS Abstracts of Votes with county-row sums matching the printed totals; CivicMirror API 2026 race list used as the Senate-class cross-check. Seven mid-term successions modeled (SD13, SD17, SD26, HD26, HD34, HD48, HD51). Validation on the OR tree PASSED, 0 errors, 10 warnings (9 pre-existing baseline + 1 by-design winner-not-seated for HD34).", "Government Structure, Status Log", "SOS Abstracts of Votes 2024 (Archives uri 13735458) and 2022 (uri 13735454); county commission appointment releases (Washington, Multnomah, Clackamas); Oregon Legislature", "CivicMirror"),
    ("2026-10-23", "Judicial pass, Circuit Courts built on PR #171 (commit 696e17f): 27 judicial-district jurisdictions + circuit court organizations (ORS 3.010/3.012), 186 posts -- the Oregon Judicial Department judges-directory count, which runs ahead of the ORS 3.012 text in Districts 1 (11), 2 (17), 5 (13), 16 (6) and 20 (16) with recently created judgeships; raced position numbers match directory numbers everywhere, so no renumbering. 200 deciding contests appended to the six election files (indecisive primaries feeding a November runoff are not separate contests); candidacies for all 200 winners; elected memberships for the 169 seats whose sitting judge's class-aligned certified win fully determines the seating (term start = first Monday in January: 2021-01-04 / 2023-01-02 / 2025-01-06). Three winners already on file (Bushong, Jacquot, McLane) had candidacies appended to their existing person records. HELD for the research step (Walter's direction): memberships at 17 seats -- new-judgeship appointees 2-16, 2-17, 5-12, 5-13, 16-6; departure->appointment seats 4-18, 4-34, 5-6, 13-2; class contradictions 2-14, 4-6, 5-5, 20-1; vacancies 4-2, 4-14, 11-3; surname-masked succession 20-14 (Miranda Summer won the 2022 race, Maalik M. Summer holds the seat). Validation PASSED, 0 errors, 22 warnings (10 baseline + the 12 held-seat winner-not-seated warnings, which are the research queue). Remaining in the judicial pass: Justices of the Peace.", "Government Structure, Status Log", "SOS Abstracts of Votes 2020-2024 (Archives uris 13735448-13735458); Oregon Judicial Department judges directory (courts.oregon.gov, accessed 2026-10-23); ORS 3.010/3.012 (oregonlegislature.gov)", "CivicMirror"),
    ("2026-10-25", "County pass built on PR #171 (seven commits: Baker worked example dda1a83, then batches 9f4c7c0, 0d434c6, 99f9f91, 933e955, 2902471, 43c6104): governing body, elected row offices and District Attorney in all 36 counties -- 1,110 new files (orgs, posts, people, memberships, county election files carrying every DA contest from the certified state abstracts). Sources: SOS Blue Book county rosters (all 36 read firsthand), each county's own website for board structure and current holders, the OHA Commissioner and Judges Contact List (2025-06-04) as a cross-check, and the certified abstracts. Walter's rule applied: numbered commissioner posts where the county's own listing gives positions, one multi-seat post where it does not. County Courts are exactly the factory's six (Gilliam, Grant, Harney, Malheur, Sherman, Wheeler); Crook and Morrow are Boards of Commissioners on their own documents. Validation PASSED, 0 errors, 24 warnings (the 23 prior plus Jefferson's DA winner-not-seated hold, by design). County research items and forward watches are Open Issues #6-13.", "Government Structure, Counties, Status Log, Open Issues", "SOS Blue Book county pages; counties' own websites (board/elected-officials/budget documents, read 2026-10-25); OHA Commissioner and Judges Contact List 2025-06-04; SOS Abstracts of Votes 2022/2024 (Archives uris 13735452/13735456/13735458)", "CivicMirror"),
    ("2026-10-23", "Judicial pass, Justices of the Peace built on PR #171 (commit 2beb5a1), completing the judicial tier's build phase: 21 Justice Court organizations (on the existing county jurisdictions), 22 posts, 28 new people, 25 memberships, and 13 new county election files with 14 contests from county official results. Denominator from the SOS Blue Book county pages: 22 seats in 21 counties (Douglas has two districts) -- the factory's 20 seats missed Hood River and Union, and the Oregon Law Commission's '22 justice courts' agrees. The state abstracts carry no JP races and JP races are decided at the May primary on a majority (only Jackson and Union were November decisions). Three sitting JPs are gubernatorial appointees: Rastetter (Clackamas, effective 2026-01-01 on Brisbin's retirement -- factory right, Blue Book stale), Hayter (Gilliam, June 2024; the 2020 holder was Patnode), Joseph (Union, 2026-02-01). Union's 2022 winner Dall (7,938) carries a candidacy + contest but no membership -- his resignation date is undocumented, and the resulting winner-not-seated warning is the hold. Joe Charter's Nov 2024 JP win (43,176) was appended to his existing circuit-court person record (he left Circuit 1-8 in 2024). Blue Book term years overridden by county documents for Hood River (Harvey elected May 2022, Cascade Locks district), Klamath, Sherman and Tillamook (Connell re-elected May 2024; separate 2019-2024 membership from the county's 2018 order). Validation PASSED, 0 errors, 23 warnings (22 prior + the Dall hold). Remaining in the judicial pass: the circuit research items (17 seats).", "Government Structure, Status Log, Open Issues", "SOS Blue Book county pages (sos.oregon.gov); county clerks' certified results (Columbia, Douglas, Grant, Malheur, Tillamook, Clackamas, Deschutes, Hood River, Marion, Washington, Jackson, Union); Clackamas County releases and minutes (Rastetter appointment); Sherman County elected-officials list; Tillamook County BOC order (2018) and ACFRs", "CivicMirror"),
    ("2026-10-23", "Statewide executive completed on PR #171: Secretary of State (Read), State Treasurer (Steiner), and Attorney General (Rayfield) built from the certified Nov 5, 2024 abstract, and Commissioner of Labor and Industries (Stephenson) from the certified Nov 8, 2022 abstract -- each as org + post + new person + membership + election contest, cross-checked against the CivicMirror API's 2026 races. All 5 elected statewide offices now built. Validation on the OR tree PASSED, 0 errors. Also: the SOS retired the old sos.oregon.gov abstract PDF paths; abstracts are now published via the Oregon State Archives records system (records.sos.state.or.us), and the Governor-step source URLs were repaired to the current official location.", "Government Structure, Status Log", "SOS Abstracts of Votes 2024 (Archives uri 13735458) and 2022 (uri 13735454); Multnomah County elected-officials page; BOLI commissioner page; CivicMirror API", "CivicMirror"),
]
for r in log:
    ws.append(list(r))
style_sheet(ws, [12, 120, 16, 52, 14], wrap_cols=(2, 4))

# ---------------- Open Issues ----------------
ws = wb.create_sheet("Open Issues")
ws.append(["#", "Category", "Applies to", "What's open", "Resolving document / next step"])
issues = [
    (1, "Divergence (factory vs official) -- RESOLVED 2026-10-25", "Morrow (and Crook) County governing body", "Resolved at the county pass: Morrow's own documents (a 2024 plan signature block printing 'Commissioner, Chair, Position 3') establish a Board of Commissioners -- the factory was right and the OJD's seven-county County Court description is wrong for Morrow. The same check resolved CROOK the other way against the Blue Book: Crook's own budget documents a Board of Commissioners of three numbered positions, superseding the Blue Book's 'County Court / Judge Crawford' listing. County Courts are exactly six: Gilliam, Grant, Harney, Malheur, Sherman, Wheeler.", "Done. Both counties built as Boards of Commissioners on PR #171."),
    (2, "Factory gap -- RESOLVED 2026-10-25", "Clatsop County District Attorney", "Factory gap confirmed: Clatsop elects a DA (Ron Brown, certified May 2022 primary, 6,745). Built on PR #171. Clatsop's charter in fact elects only the Board (5 districts), Sheriff and DA -- Assessor, Clerk and Surveyor are appointed and the Treasurer's office was abolished.", "Done."),
    (3, "Factory gap -- RESOLVED 2026-10-25", "Hood River County District Attorney", "Factory gap confirmed: Hood River elects a DA (Matthew Ellis, certified May 2024 primary, 4,660 -- he had been Wasco County's DA in 2020). Built on PR #171.", "Done."),
    (4, "Verification owed -- RESOLVED 2026-10-23", "Justice of the Peace seats (all counties)", "The factory modeled 20 JP seats; the verified denominator is 22 seats in 21 counties (SOS Blue Book county pages, corroborated by the Oregon Law Commission's count of 22 justice courts). The factory missed Hood River (Harvey) and Union (Joseph) entirely and was right against a stale Blue Book in Clackamas (Rastetter's appointment). All 22 seats are built (PR #171, commit 2beb5a1).", "Done. Leftovers in the research queue: certified totals not posted online for 8 seats (clerk requests), Dall's resignation date (Union), Joseph's appointment announcement, Charter's circuit departure date, and whether Hood River has a second justice district."),
    (5, "Verification owed -- RESOLVED 2026-10-25", "County officer sets, home-rule charter counties", "Every county's elected set was verified against its own website and charter documents at the county pass and built accordingly (PR #171). The thinnest sets: Multnomah and Umatilla (board, Sheriff, DA -- Multnomah also Auditor); the widest add an elected Auditor (Multnomah, Washington) or a Legal Counsel (Josephine).", "Done."),
    (6, "Source conflict -- clerk confirmation", "Baker County Commissioner Position 1 (Kaseberg)", "The county's own commissioners page shows Kaseberg's term as Jan. 2024-Dec. 2027; the Blue Book and the factory both give 2029. Modeled on the Blue Book class (from Jan. 2025) with the conflict quoted in her records.", "Baker County Clerk confirmation; amend the record if the county's Jan. 2024 start (appointment, then election to the remainder) is confirmed."),
    (7, "Source conflict -- clerk confirmation", "Klamath County (Schutt term class; Nichols expiry)", "DA Schutt won at the November 2024 general after Costello's mid-term departure, but the Blue Book gives him a full term to 2029 although Klamath sits in the 2022 class. Separately, one county document gives Commissioner Nichols's expiry as January 2028 against the Blue Book's 2029. Both are modeled on the Blue Book with the conflicts disclosed.", "Klamath County Clerk confirmation of the 2024 DA election's term and of Nichols's class."),
    (8, "Research item", "Jefferson County District Attorney", "Leriche won the certified May 2024 primary (3,467), but a June 2025 Board agenda carries DA applicant presentations -- a vacancy being filled by appointment. Whether Leriche ever served, and who holds the office now, is undocumented in the sources read. Contest + candidacy only (the pass's one new winner-not-seated warning).", "Jefferson County sources / clerk: Leriche's service and the appointed successor's identity and date."),
    (9, "Forward watch -- November 3, 2026 election", "Lincoln County Commissioner Position 2; Washington County Chair", "Lincoln Position 2 is vacant (Hall departed) and is on the ballot as a two-year unexpired term. The Washington County Chair is vacant (Harrington resigned effective October 2, 2026); the successor elected November 3, 2026 is sworn in January 3, 2027.", "Seat both winners from the certified November 2026 results after the election."),
    (10, "Forward watch -- November 3, 2026 election", "Deschutes County Board expansion and districting", "Measure 9-173 (approved Nov. 2024) adds Positions 4 and 5, elected at-large in November 2026 for initial two-year terms from January 2027. Measure 9-185 on the same ballot would switch the Board to five geographic districts (Map C) from the 2028 election. The Sheriff's office is also on the November 2026 ballot (Rupert's interim runs through December 31, 2026).", "Seat the Position 4/5 and Sheriff winners after certification; if 9-185 passes, plan the 2028 district restructure."),
    (11, "Forward watch -- January 2027", "Morrow County District Attorney", "An October 2026 county meeting report says DA Nelson expects to leave for a circuit-court judgeship (District 6) in early January 2027.", "Verify in January 2027; if he goes, end his DA membership, model the successor, and check the District 6 circuit vacancy against the circuit research queue."),
    (12, "Verification owed", "Harney County Judge; Wallowa County third seat", "An October 21, 2026 report outside county sources says Harney County Judge Hart resigned; unverified, and he is modeled as holding. Wallowa's third seat: Commissioner Roberts died in office July 30, 2025 (ended membership built); her successor is reported in meeting coverage as Cody Lathrop but is not verified on a county page.", "County sources for both; amend on documentation."),
    (13, "Research items (county successions)", "Josephine, Curry, Lane succession details", "Josephine's Martin and Richardson were appointed in January 2026 to vacant seats (dates/manner from county sources are summary-grade); Curry's Coker filled Alcorn's seat on an undocumented date and manner; Lane's elected Sheriff Harrold resigned in 2025 on an undocumented date (successor Wilkerson is built as appointed).", "County minutes/orders for the exact instruments and dates; amend the records when documented."),
]
for r in issues:
    ws.append(list(r))
style_sheet(ws, [5, 22, 42, 62, 58], wrap_cols=(3, 4, 5))

OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)
print("WROTE", OUT, "municipalities:", len(municipal), "counties:", len(counties))
