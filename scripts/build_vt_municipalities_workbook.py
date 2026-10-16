#!/usr/bin/env python3
"""Build reference/VT Rolling Audit/VT_Municipalities.xlsx for issue #163.

Modeled on reference/MS Rolling Audit/MS_Municipalities.xlsx.
Seeded from the repo's own Vermont jurisdiction files, which were
machine-generated from the U.S. Census Bureau 2022 Census of
Governments government-units listing (see each file's sources).
Per-municipality charter / code / website backfill is marked
'Needs Research' where the repo does not already carry it --
nothing is guessed.

Sheets: README, Government Structure, Municipalities, Counties,
Office Titles (Ref), Sources, Status Log.
"""
import re
from pathlib import Path

import yaml
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

REPO = Path(__file__).resolve().parent.parent
VT = REPO / "data" / "us" / "vt"
OUT = REPO / "reference" / "VT Rolling Audit" / "VT_Municipalities.xlsx"
RETRIEVED = "2026-10-16"

BOLD = Font(bold=True)


def style_header(ws):
    for c in ws[1]:
        if c.value is not None:
            c.font = BOLD
    ws.freeze_panes = "A2"


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[get_column_letter(col)].width = w


def county_area(note):
    m = re.search(r"county area=([A-Z ]+)", note or "")
    return m.group(1).title() if m else "Needs Research"


def load_jurisdictions(kind):
    rows = []
    for f in sorted((VT / "jurisdictions" / kind).glob("*.yaml")):
        d = yaml.safe_load(f.read_text()) or {}
        note = " ".join(s.get("note", "") for s in d.get("sources", []))
        rows.append((f, d, note))
    return rows


# Per-municipality backfill results that override the seeded
# "Needs Research" cells, keyed by short municipality name.
MUNICIPAL_OVERRIDES = {
    "Bloomfield": {
        "website": "None (no official town website)",
        "charter": "None (general law; no Title 24 Appendix chapter)",
        "code": "None published",
        "status": "Roster backfilled 2026-10-16",
        "note": (
            "Added 2026-10-16 (issue #163 fix): missing from the Census 2022 seed; "
            "verified on the official Vermont.gov Towns & Cities explorer. Municipal "
            "sweep completed 2026-10-16 (worked example, tracking PR #168): Selectboard, "
            "Town Treasurer, and Justices of the Peace backfilled from SOS Elections "
            "Division directories; November 5, 2024 JP election record built. Town "
            "Clerk holder HELD (SOS guide, SOS contact spreadsheet, and Vermont.gov "
            "explorer name three different people). Lesser town officers await the "
            "printed town report or a clerk reply. No charter (general law), no "
            "official website, no published code."),
    },
}


def main():
    munis = load_jurisdictions("municipal")
    counties = load_jurisdictions("county")

    muni_rows = []
    counts = {"Town": 0, "City": 0, "Village": 0}
    for f, d, note in munis:
        name = d["name"]
        if name.startswith("Town of "):
            typ, short = "Town", name[len("Town of "):]
        elif name.startswith("City of "):
            typ, short = "City", name[len("City of "):]
        elif name.startswith("Village of "):
            typ, short = "Village", name[len("Village of "):]
        else:
            typ, short = "Needs Research", name
        counts[typ] = counts.get(typ, 0) + 1
        if "govt_units_2022" in note:
            row_note = (
                "Seeded from repo jurisdiction file (Census 2022 Census of Governments). "
                "Charter chapter in Title 24 Appendix V.S.A. and code link to be backfilled "
                "from the Vermont Legislature municipal charters index and the official "
                "municipal website.")
        elif "Vermont.gov" in note:
            row_note = (
                "Added 2026-10-16 (issue #163 fix): missing from the Census 2022 seed; "
                "verified on the official Vermont.gov Towns & Cities explorer. "
                "Charter/code/website backfill as per sheet.")
        else:
            row_note = (
                "Added 2026-10-16 (issue #163 fix): missing from the Census 2022 seed; "
                "verified on the Vermont Secretary of State (VSARA) List of Incorporated "
                "Villages. Charter/code/website backfill as per sheet.")
        row = [
            short, typ, county_area(note), d["id"], d.get("website") or "Needs Research",
            "Needs Research", "Needs Research", None, "Needs Research", row_note,
        ]
        if short in MUNICIPAL_OVERRIDES:
            o = MUNICIPAL_OVERRIDES[short]
            row[4] = o.get("website", row[4])
            row[5] = o.get("charter", row[5])
            row[6] = o.get("code", row[6])
            row[8] = o.get("status", row[8])
            row[9] = o.get("note", row[9])
        muni_rows.append(row)
    muni_rows.sort(key=lambda r: (r[0].lower()))

    county_rows = []
    for f, d, note in counties:
        m = re.search(r"FIPS (50-\d+)", note or "")
        short = d["name"].replace("County of ", "")
        county_rows.append([
            short, m.group(1) if m else "Needs Research", "Needs Research",
            "Seeded in this pass (issue #163): State's Attorney, Sheriff, "
            "Assistant Judge (2 seats), High Bailiff -- posts only, no officeholders yet. "
            "Judge of Probate HELD: 18 probate districts do not map 1:1 to the 14 counties.",
            "Posts seeded", d["id"],
        ])
    county_rows.sort(key=lambda r: r[0].lower())

    wb = Workbook()

    ws = wb.active
    ws.title = "README"
    ws.append(["VT_Municipalities -- Sheet Guide"])
    ws.append([
        "Master reference workbook for CivicMirror's Vermont elected-office audit "
        "(issue #163, VT master tracking). Modeled on MS_Municipalities / TX_Municipalities. "
        "Enumerations are seeded from official, automatable sources (the repo's jurisdiction "
        "files, built from the U.S. Census Bureau 2022 Census of Governments); per-municipality "
        "charters, codes, and websites are backfilled from the Vermont Legislature (Title 24 "
        "Appendix municipal charters) and official municipal sites. Sourcing rules: official "
        "sources only; the Vermont League of Cities and Towns (VLCT) is an association source -- "
        "used to locate and verify, not as source of record, mirroring the MS MML rule."
    ])
    ws.append([])
    ws.append(["Sheet", "What it tracks", "Coverage / Status"])
    for row in [
        ["README", "This guide. Regenerate coverage counts whenever another sheet's row counts change.", "--"],
        ["Government Structure", "Sheet 1 of issue #163: how Vermont government is organized at each level, which offices are elected vs appointed, terms, and the statute/constitution basis. Vermont is a Dillon's Rule, town-meeting state whose counties are judicial / law-enforcement units, not general-purpose governments like MA counties were.", "Complete for state + county (2026-10-16); municipal detail per-town is backfill."],
        ["Municipalities", "Every Vermont municipality in the repo: 237 towns, 10 cities, 31 active incorporated villages (278 total), with county, jurisdiction ID, website on file, and charter/code backfill status. The Census 2022 seed (235 / 10 / 30 = 275) was reconciled place-by-place on 2026-10-16 against the official Vermont.gov Towns & Cities explorer and the SOS/VSARA List of Incorporated Villages: Bloomfield and Sudbury towns and Jericho and Westbury villages added; Lyndonville village retired (merged into the Town of Lyndon, Act M-14). VLCT's headline count (237 / 10 / 28) still differs on villages by 3, unexplained in its document; the SOS list governs. Two SOS-listed villages are inactive and excluded: Groton (town assumed functions 1965/67) and Townshend (inactive since 1961).", f"{len(muni_rows)} municipalities (repo split: {counts.get('Town')} towns / {counts.get('City')} cities / {counts.get('Village')} villages); charters & code links = Needs Research."],
        ["Counties", "The 14 counties with FIPS, county website status, and the elected-office seeding status.", "14 counties; 4 elected offices per county seeded as posts (56 posts, 70 seats). Probate held."],
        ["Office Titles (Ref)", "Reference: which municipal / county / state offices are popularly elected, with statute basis. Per-town variation (charters, votes to appoint or eliminate an office) is resolved per municipality during backfill.", "Reference -- verify per municipality."],
        ["Sources", "Source registry for this workbook and the VT build.", "Seed sources registered."],
        ["Status Log", "Change history.", "--"],
    ]:
        ws.append(row)
    widths(ws, {1: 26, 2: 110, 3: 60})

    ws = wb.create_sheet("Government Structure")
    ws.append(["Level", "Body / Office", "Elected?", "Term", "Seats / Districts",
               "Basis", "Notes"])
    gov_rows = [
        ["Federal", "U.S. Representative (at-large)", "Elected", "2 years", "1 seat",
         "U.S. Const.", "Already in repo (federal tier complete for VT)."],
        ["Federal", "U.S. Senator", "Elected", "6 years", "2 seats (Class 1, Class 3)",
         "U.S. Const.", "Already in repo."],
        ["State", "Governor", "Elected", "2 years", "1", "Vt. Const. Ch. II sections 47, 49",
         "Statewide, every November general election in even years. Post seeded 2026-10-16."],
        ["State", "Lieutenant Governor", "Elected", "2 years", "1", "Vt. Const. Ch. II sections 47, 49",
         "Elected separately from the Governor. Post seeded."],
        ["State", "Secretary of State", "Elected", "2 years", "1", "Vt. Const. Ch. II section 48",
         "Post seeded."],
        ["State", "State Treasurer", "Elected", "2 years", "1", "Vt. Const. Ch. II sections 47, 49",
         "Post seeded."],
        ["State", "Auditor of Accounts", "Elected", "2 years", "1", "Vt. Const. Ch. II section 48",
         "Post seeded."],
        ["State", "Attorney General", "Elected", "2 years", "1", "3 V.S.A. section 151 (elected since 1908)",
         "Statutory statewide office (not constitutional). Post seeded."],
        ["State", "State Senate", "Elected", "2 years", "30 seats; district count to be enumerated from apportionment statute",
         "Vt. Const. Ch. II sections 43-46", "HELD for a dedicated legislative pass from the official apportionment lists / legislature directory (the MS issue #68 pattern). Multi-member districts are normal in VT."],
        ["State", "House of Representatives", "Elected", "2 years", "150 seats; district count to be enumerated from apportionment statute",
         "Vt. Const. Ch. II sections 43-46", "HELD with the Senate pass. Districts are named by county / town groupings, one- and two-member."],
        ["State", "Supreme Court / Superior Court judges", "APPOINTED -- out of elected scope", "6 years, retention by General Assembly", "--",
         "Vt. Const. Ch. II sections 32-34", "Appointed by the Governor with Senate consent from Judicial Nominating Board nominees. Excluded, mirroring the appointed-office exclusions in MS/TX."],
        ["County", "State's Attorney", "Elected", "4 years (from Feb. 1 after election)", "1 per county (14)",
         "Vt. Const. Ch. II section 50; 24 V.S.A. chapter 5", "Post seeded for all 14 counties. County prosecutor; a state-paid office elected by county voters."],
        ["County", "Sheriff", "Elected", "4 years (from Feb. 1 after election)", "1 per county (14)",
         "Vt. Const. Ch. II section 50; 24 V.S.A. chapter 5 subchapter 5", "Post seeded for all 14 counties."],
        ["County", "Assistant Judge", "Elected", "4 years (from Feb. 1 after election)", "2 per county (28 seats)",
         "Vt. Const. Ch. II section 50; 24 V.S.A. chapter 5 subchapter 1 (section 131)",
         "Post seeded (seats: 2). Assistant judges sit with Superior Court judges and administer county government (county property, courthouse, county tax) -- Vermont's closest analog to a county commission, but elected as judges."],
        ["County", "Judge of Probate", "Elected", "4 years (from Feb. 1 after election)", "18 probate districts (NOT 14)",
         "Vt. Const. Ch. II section 51", "HELD: probate districts do not map 1:1 onto counties (four counties are split into two districts each). Posts wait for the official Vermont Judiciary district enumeration -- do not mint by county."],
        ["County", "High Bailiff", "Elected", "2 years", "1 per county (14)",
         "Vt. Const. Ch. II section 43; 24 V.S.A. sections 331-333 (approx.)",
         "Post seeded for all 14 counties. Vermont-only office: serves process the sheriff cannot serve and succeeds the sheriff on vacancy/incapacity. Unpaid, rarely acts. Term length flagged for verification in the membership pass."],
        ["County", "County Clerk", "APPOINTED -- excluded", "--", "--",
         "24 V.S.A. section 171 (Appointment)", "Appointed by the assistant judges. Not an elected office."],
        ["County", "County Treasurer", "APPOINTED -- excluded", "--", "--",
         "24 V.S.A. section 211 (Appointment; vacancy)", "Appointed. Not an elected office. Vermont counties levy a county tax through the assistant judges but run almost no general government -- there are no county commissioners, councils, or legislatures."],
        ["Municipal (town)", "Selectboard", "Elected", "3 years (staggered); a town may vote a 5-member board", "3 or 5 per town",
         "17 V.S.A. section 2646 et seq.; 24 V.S.A. chapter 33",
         "The town legislative/executive body in 237 towns. Elected at annual town meeting (first Tuesday in March) or by Australian ballot where adopted. Per-town board size is backfill."],
        ["Municipal (town)", "Town Clerk", "Elected (default)", "3 years (a town may vote a different term / appointment route)", "1 per town",
         "17 V.S.A. sections 2646, 2651e", "Default is elected; some towns have voted or chartered appointment. Verify per town -- the MA lesson applies: never assume."],
        ["Municipal (town)", "Town Treasurer", "Elected (default)", "3 years", "1 per town",
         "17 V.S.A. section 2646", "Same verify-per-town rule; clerk and treasurer are sometimes combined, sometimes split, sometimes appointed by charter."],
        ["Municipal (town)", "Moderator", "Elected", "1 year", "1 per town", "17 V.S.A. sections 2646, 2658",
         "Presides at town meeting."],
        ["Municipal (town)", "Listers", "Elected (default)", "3 years (staggered)", "3 per town",
         "17 V.S.A. sections 2649, 2651c", "Property valuation board. A town may vote to eliminate elected listers in favor of a hired assessor -- verify per town."],
        ["Municipal (town)", "Auditors", "Elected (default)", "3 years (staggered)", "3 per town",
         "17 V.S.A. sections 2649, 2651b; 24 V.S.A. sections 1681-1682",
         "A town may vote to eliminate the office and hire a public accountant -- verify per town."],
        ["Municipal (town)", "Collector of Delinquent Taxes", "Elected or appointed (varies)", "1-3 years", "1 per town",
         "17 V.S.A. section 2651d", "Verify per town. Where no tax collector is elected, the first constable is the default collector."],
        ["Municipal (town)", "First Constable (and Second, if voted)", "Elected", "1-2 years (town option)", "1-2 per town",
         "17 V.S.A. section 2646", "Duties vary widely by town; some are full law enforcement, most are process-servers."],
        ["Municipal (town)", "Grand Juror / Town Agent", "Elected", "1 year", "1 each per town",
         "17 V.S.A. section 2646", "Largely dormant offices in many towns; still on the statutory list. Mint only where a town actually elects them -- research item."],
        ["Municipal (town)", "Justices of the Peace", "Elected", "2 years (from Feb. 1 after the November general election)",
         "Per town/city, apportioned by population (Vt. Const. Ch. II section 52)",
         "Vt. Const. Ch. II section 52; 17 V.S.A. chapter 55",
         "Unusual placement: a town office elected on the November state ballot, not at town meeting. JP counts per town are a research item (BCA membership follows from the office)."],
        ["Municipal (town)", "Library Trustees / Cemetery Commissioners / Trustees of Public Funds / Planning, school and other boards",
         "MIXED -- elected in some towns, appointed in others", "Varies", "Varies",
         "24 V.S.A. and Title 17; town charters (Title 24 Appendix)",
         "The MA pattern exactly: resolve per town from its charter (Title 24 Appendix), bylaws, and annual reports. School governance is a separate district tier -- see Sources / Status Log."],
        ["Municipal (city)", "Mayor + City Council / Board of Aldermen", "Elected", "Charter terms (1-3 years typical)",
         "10 cities", "City charters, Title 24 Appendix (one chapter per city)",
         "Vermont cities are charter governments ( Burlington, Rutland, Barre, Montpelier, Newport, St. Albans, South Burlington, Winooski, Vergennes, Essex Junction -- a city only since 2022). Each charter enumerates its own elected offices: mayor, council/aldermen, clerk, treasurer, and in some cities listers/auditors/constables or a city grand juror."],
        ["Municipal (village)", "Board of Trustees (village president, trustees, clerk, treasurer)", "Elected",
         "Charter terms", "31 active incorporated villages per the SOS/VSARA list (33 listed incl. 2 inactive: Groton, Townshend; VLCT headline count is 28, definitional difference unresolved)",
         "Village charters, Title 24 Appendix; 24 V.S.A. chapter 81",
         "Incorporated villages are municipalities INSIDE towns (a second, overlapping general-purpose layer -- VT is one of three New England states with them). Village officers are elected at the village annual meeting. The host town's offices are unaffected."],
        ["Unorganized", "Unified Towns and Gores of Essex County (UTG) + unorganized towns/gores",
         "Special -- UTG has an elected/organized structure; other unorganized places are run by a Governor-appointed supervisor",
         "--", "1 UTG + several gores/grants", "24 V.S.A. chapter 43; 1 V.S.A. section 126",
         "NOT in the repo's 275 municipal jurisdictions (Census lists UTG separately). Research item: decide scope before minting. Glastenbury and Somerset disincorporated; their residents vote in neighboring towns."],
        ["School", "School district boards", "MIXED (elected boards for unified / town districts)",
         "Varies", "Statewide district inventory not yet built",
         "Title 16; Act 46 / Act 49 mergers", "Out of this pass, mirroring MS #158 being its own issue-sized sweep. Vermont's post-merger district map (unified union districts vs town districts) needs its own classification pass before any minting."],
    ]
    for r in gov_rows:
        ws.append(r)
    style_header(ws)
    widths(ws, {1: 18, 2: 44, 3: 18, 4: 30, 5: 34, 6: 40, 7: 95})

    ws = wb.create_sheet("Municipalities")
    ws.append(["Municipality Name", "Type", "County", "Jurisdiction ID",
               "Municipal Website", "Charter (Title 24 Appendix)",
               "Municipal Code Link", "Code Host", "Status", "Notes"])
    for r in muni_rows:
        ws.append(r)
    style_header(ws)
    widths(ws, {1: 24, 2: 10, 3: 16, 4: 58, 5: 34, 6: 22, 7: 22, 8: 12, 9: 16, 10: 80})

    ws = wb.create_sheet("Counties")
    ws.append(["County Name", "County FIPS", "County Website", "Status",
               "Elected Offices in Repo", "Jurisdiction ID"])
    # reorder to header: Name, FIPS, Website, Offices, Status, Jurisdiction -- rebuild rows
    ws.append(["County Name", "County FIPS", "County Website", "Elected Offices in Repo",
               "Status", "Jurisdiction ID"])
    ws.delete_rows(1)
    for r in county_rows:
        ws.append([r[0], r[1], r[2], r[3], r[4], r[5]])
    style_header(ws)
    widths(ws, {1: 18, 2: 12, 3: 20, 4: 90, 5: 16, 6: 58})

    ws = wb.create_sheet("Office Titles (Ref)")
    ws.append(["Office", "Popularly Elected?", "Statute / Basis", "Notes"])
    for r in [
        ["Selectboard Member", "Elected", "17 V.S.A. section 2646", "Towns: 3 members default, 5 if voted; staggered 3-year terms. Cities use councils/alderboards under charter instead."],
        ["Town Clerk", "Elected (default)", "17 V.S.A. sections 2646, 2651e", "Some towns appoint by vote/charter -- verify per town."],
        ["Town Treasurer", "Elected (default)", "17 V.S.A. section 2646", "May be combined with clerk; may be appointed by charter -- verify per town."],
        ["Moderator", "Elected", "17 V.S.A. sections 2646, 2658", "1-year term."],
        ["Lister", "Elected (default)", "17 V.S.A. sections 2649, 2651c", "3-member board; town may vote to replace with a hired assessor."],
        ["Auditor", "Elected (default)", "17 V.S.A. sections 2649, 2651b", "3-member board; town may vote to eliminate and use a public accountant."],
        ["Collector of Delinquent Taxes", "Needs Review (per town)", "17 V.S.A. section 2651d", "Elected in some towns, appointed or held by constable/treasurer in others."],
        ["First / Second Constable", "Elected", "17 V.S.A. section 2646", "Second constable only where voted."],
        ["Grand Juror", "Elected", "17 V.S.A. section 2646", "Dormant in many towns."],
        ["Town Agent", "Elected", "17 V.S.A. section 2646", "Prosecutes/defends town suits. Dormant in many towns."],
        ["Justice of the Peace", "Elected", "Vt. Const. Ch. II section 52", "Town office on the November ballot; 2-year terms; counts apportioned by population."],
        ["Mayor (city)", "Elected", "City charters, Title 24 Appendix", "All 10 cities elect a mayor."],
        ["City Councilor / Alderman", "Elected", "City charters, Title 24 Appendix", "By ward/district and/or at-large per charter."],
        ["Village Trustee / Village President", "Elected", "Village charters, Title 24 Appendix; 24 V.S.A. chapter 81", "31 active incorporated villages (SOS/VSARA list)."],
        ["State's Attorney", "Elected", "Vt. Const. Ch. II section 50", "County office, 4-year term. Seeded."],
        ["Sheriff", "Elected", "Vt. Const. Ch. II section 50", "County office, 4-year term. Seeded."],
        ["Assistant Judge", "Elected", "Vt. Const. Ch. II section 50", "2 per county, 4-year terms. Seeded (one post, seats: 2)."],
        ["Judge of Probate", "Elected", "Vt. Const. Ch. II section 51", "18 probate districts -- HELD, not seeded by county."],
        ["High Bailiff", "Elected", "Vt. Const. Ch. II section 43", "1 per county. Seeded; term to verify in membership pass."],
        ["County Clerk", "Appointed -- excluded", "24 V.S.A. section 171", "Appointed by the assistant judges."],
        ["County Treasurer", "Appointed -- excluded", "24 V.S.A. section 211", "Appointed."],
        ["Town Manager", "Appointed -- excluded", "24 V.S.A. chapter 37", "Appointed by the selectboard where the town has voted the manager form. The FORM is structural data for the Municipalities sheet, the person is never minted as elected."],
        ["School Board Director", "Elected (district-dependent)", "Title 16", "Separate school-district pass -- not in this workbook's scope yet."],
    ]:
        ws.append(r)
    style_header(ws)
    widths(ws, {1: 30, 2: 22, 3: 36, 4: 95})

    ws = wb.create_sheet("Sources")
    ws.append(["Source", "Level", "Official?", "Automation", "URL", "Provides", "Status", "Notes"])
    for r in [
        ["U.S. Census Bureau -- 2022 Census of Governments, Government Units Listing",
         "State", "Official (federal)", "Bulk download",
         "https://www.census.gov/data/datasets/2022/econ/gus/public-use-files.html",
         "Enumeration of VT general-purpose governments seeded into repo jurisdiction files (275 municipal + 14 county at seed time; corrected 2026-10-16 -- see Status Log).",
         "USED -- seeded repo jurisdictions (2026-08-17)", "Municipality / county mapping and websites in this workbook come from those repo files. The seed is stale in four places and wrong-by-omission in one more (Lyndonville merger) -- all corrected from official state sources on 2026-10-16."],
        ["Vermont Statutes Online -- Title 24, chapter 5 (County Officers)",
         "County", "Official (state)", "Scrape",
         "https://legislature.Vermont.gov/statutes/chapter/24/005",
         "County officer structure: assistant judges, county clerk (appointed), county treasurer (appointed), sheriffs.",
         "USED -- county post seeding (issue #163)", "Cite the Legislature as source of record; Justia etc. are convenience mirrors only."],
        ["Vermont Statutes Online -- Title 24 Appendix (Municipal Charters)",
         "Municipal", "Official (state)", "Scrape",
         "https://legislature.vermont.gov/statutes/chapter/24appendix/143",
         "Per-municipality charters (example chapter shown: Town of Richmond, ch. 143). Each chartered town/city/village has its own chapter enumerating its elected offices.",
         "TODO -- charter backfill, Municipalities sheet", "Most towns operate under general law (Titles 17/24) with NO individual charter; a blank charter field after research means general-law, not missing data."],
        ["Vermont Statutes Online -- Title 17, chapter 55 (Local Elections; town officers)",
         "Municipal", "Official (state)", "Scrape",
         "https://law.justia.com/codes/vermont/2022/title-17/chapter-55/section-2650/",
         "Default elected town officers and terms (section 2646 list; sections 2649-2651 series for listers/auditors/collectors).",
         "USED -- Government Structure + Office Titles sheets",
         "Justia URL is a mirror used in research; cite legislature.vermont.gov as source of record in repo files."],
        ["Vermont Legislative Counsel -- constitutional officers memorandum (2024-02-20)",
         "State/County", "Official (state)", "Manual",
         "https://legislature.Vermont.gov/Documents/2024/WorkGroups/Senate%20Judiciary/Bills/PR.1/Drafts,%20Amendments,%20Legal%20Documents/PR.1~Tim%20Devlin~Memorandum-%20Removal%20of%20Elected%20County%20Officers%20from%20Office~2-20-2024.pdf",
         "Enumeration of Vermont constitutional officers (statewide exec + county officers).",
         "USED -- state/county post seeding (issue #163)", "Summary in prose, not quoted, in the VT_State_and_County_Offices.md reference note."],
        ["Vermont League of Cities and Towns (VLCT) -- municipal counts and elected town officers guides",
         "Municipal", "Secondary (association)", "Scrape / manual",
         "https://www.vlct.org/print/pdf/node/3294",
         "Plain-language guide to elected town officers; municipal counts (237 towns, 10 cities incl. Essex Junction, 28 incorporated villages, 1 UTG).",
         "USED -- cross-check of the repo jurisdictions",
         "Association, not government: use to locate/verify official sources, never as source of record (the MS MML rule). COUNT RECONCILIATION RESOLVED 2026-10-16: VLCT's town count (237) proved right and its village count (28) still differs by 3 from the SOS-governed active count (31); the Census seed's split (235 towns / 30 villages) was stale, not differently classified -- see Status Log."],
        ["Vermont Secretary of State -- Elections Division",
         "State/County", "Official (state)", "Scrape / manual",
         "https://sos.vermont.gov/secretarys-desk/contact/",
         "Certified election results: statewide + county officers are elected in the November general election (county officers 2022, next 2026; terms from Feb. 1). Source for the membership pass.",
         "TODO -- membership pass (issue #163 item 6)", "Use the SOS results / candidate listings as the certified tier; town-meeting offices are certified by town clerks, not the SOS."],
        ["Vermont Judiciary",
         "County", "Official (state)", "Scrape / manual",
         "https://www.vermontjudiciary.org/",
         "Probate division districts and judges; assistant judge listings. Source for resolving the 18 probate districts.",
         "TODO -- probate district enumeration", "Do not mint probate posts until this enumeration is in hand."],
        ["Vermont.gov -- Towns & Cities explorer",
         "Municipal", "Official (state)", "Scrape / manual",
         "https://www.vermont.gov/towns-and-Cities",
         "The state portal's per-town/city entries: county, census population, land area, town clerk, website. Covers towns and cities (plus gores/grants) -- NOT incorporated villages.",
         "USED -- municipality reconciliation (2026-10-16)", "Source of record for the town/city universe; verified Bloomfield and Sudbury, missing from the Census 2022 seed."],
        ["Vermont Secretary of State (VSARA) -- List of Incorporated Villages",
         "Municipal", "Official (state)", "Scrape / manual",
         "https://sos.vermont.gov/vsara/learn/municipalities/incorporated-villages",
         "The official village universe: 33 villages named with parent town/county and incorporation citation; Groton and Townshend flagged inactive on the page itself.",
         "USED -- village reconciliation (2026-10-16)", "Governs the village count (31 active). Added Jericho (1933) and Westbury (2023) to the repo; Lyndonville absent from the current page, consistent with its merger."],
        ["Vermont General Assembly -- H.490 bill status (Act M-14)",
         "Municipal", "Official (state)", "Manual",
         "https://legislature.vermont.gov/bill/status/2024/H.490",
         "Merger of the Village of Lyndonville with the Town of Lyndon: voter approval 2022-11-08, Governor approval 2023-06-19; Town of Lyndon charter at 24 App. V.S.A. chapter 126.",
         "USED -- Lyndonville retirement (2026-10-16)", "Basis for deleting the Lyndonville jurisdiction and noting the merger on the Town of Lyndon record."],
    ]:
        ws.append(r)
    style_header(ws)
    widths(ws, {1: 44, 2: 14, 3: 16, 4: 16, 5: 52, 6: 62, 7: 30, 8: 62})

    ws = wb.create_sheet("Status Log")
    ws.append(["Date", "Change", "Sheets affected", "Source(s)", "By"])
    ws.append([
        RETRIEVED,
        "Created workbook for issue #163. Government Structure determined from the Vermont "
        "Constitution and Titles 17/24 (town-meeting state; counties are judicial/law-enforcement "
        "units whose only elected officers are State's Attorney, Sheriff, Assistant Judges x2, "
        "Judge of Probate, and High Bailiff; county clerk and treasurer are appointed). "
        "Municipalities seeded with all 275 repo jurisdictions (Census 2022 split: 235 towns, 10 cities, 30 "
        "incorporated villages; VLCT's current split is 237 towns / 28 villages -- same 275 total, two-place classification drift flagged in Sources). Counties seeded (14). "
        "State executive posts (6) and county posts (56 posts / 70 seats) built in the repo by "
        "scripts/build_vt_state_county_posts.py; validation PASSED, 0 errors (5 pre-existing "
        "federal no-election-trace warnings). HELD: probate posts (18 districts, not 14), "
        "legislative districts (House 150 / Senate 30), all memberships, school districts, UTG.",
        "All", "Vt. Const. Ch. II; Titles 17/24 V.S.A.; Census 2022 Census of Governments (via repo); VLCT (cross-check)",
        "CivicMirror",
    ])
    ws.append([
        RETRIEVED,
        "Municipality reconciliation fix (same day, at Walter's direction). A name-level diff "
        "against the VT Jurisdiction Factory (276) plus official verification settled the count "
        "drift: (1) Town of Bloomfield (Essex Co.) and Town of Sudbury (Rutland Co.) were missing "
        "from the Census 2022 seed entirely -- both verified on the official Vermont.gov Towns & "
        "Cities explorer and added as jurisdictions. (2) Village of Jericho (Act 12, Special "
        "Session 1933) and Village of Westbury (Colchester, 2023) were missing from BOTH the seed "
        "and the factory -- added from the SOS/VSARA List of Incorporated Villages. (3) Village of "
        "Lyndonville was retired: merged into the Town of Lyndon by Act M-14 (H.490; voters "
        "2022-11-08, Governor 2023-06-19; charter at 24 App. ch. 126), noted on the Lyndon record. "
        "Groton and Townshend villages were NOT added (SOS flags both inactive). New totals: 278 "
        "municipal jurisdictions (237 towns / 10 cities / 31 active villages). Towns now reconcile "
        "exactly across Census-corrected repo, factory, and VLCT (237); VLCT's village headline "
        "(28) remains 3 below the SOS-governed 31, definitional, unresolved in its document.",
        "Municipalities, Sources, Government Structure, Office Titles (Ref)",
        "Vermont.gov Towns & Cities explorer; SOS/VSARA List of Incorporated Villages; VT General Assembly H.490 (Act M-14); VLCT municipal counts (cross-check)",
        "CivicMirror",
    ])
    ws.append([
        RETRIEVED,
        "Bloomfield municipal sweep -- worked example for the VT municipal tier (tracking PR #168). "
        "Roster backfilled from SOS Elections Division directories: Selectboard -- Eric Brault, Josh "
        "Riley, Denault Routhier (SOS selectboard directory, June 5, 2026); Town Treasurer -- Sharon "
        "Belknap (SOS treasurer contact spreadsheet, June 12, 2026, corroborated by the SOS clerk "
        "guide, January 2026); Justices of the Peace x5 -- Ray Bowen, Sharon Belknap, Bryant Wheeler, "
        "Suzanne Routhier, Steven Bunnell (SOS '2025-2026 Vermont Justices of the Peace' listing, "
        "December 4, 2025), with the November 5, 2024 JP election record built from the same listing "
        "(vote totals not published there and not recorded). Town Clerk membership HELD: the SOS guide "
        "(January 2026) names Susan Robidas, the SOS clerk contact spreadsheet (June 2026) names Ray "
        "Bowen, and the Vermont.gov explorer names Paulette Routhier -- post created, holder awaits a "
        "tiebreak. Moderator, Listers, Auditors, Constables, Grand Juror, and Town Agent were NOT "
        "minted: no official online source names Bloomfield's holders (no town website; the printed "
        "annual town report is not posted). Charter: none -- no Title 24 Appendix chapter (general-law "
        "town, full index checked); no official website; no published municipal code. Factory "
        "concordance: the VT Jurisdiction Factory carries Selectboard only for Bloomfield and matches "
        "name-for-name; every other office is outside its bounded scope.",
        "Municipalities (Bloomfield row), Status Log",
        "VT SOS Elections Division directories (selectboard directory; clerk/treasurer contact spreadsheets; JP listing); Title 24 Appendix chapter index (Vermont Statutes Online)",
        "CivicMirror",
    ])
    style_header(ws)
    widths(ws, {1: 12, 2: 120, 3: 16, 4: 52, 5: 14})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    print(f"Wrote {OUT} -- municipalities: {len(muni_rows)} "
          f"(towns {counts.get('Town')}, cities {counts.get('City')}, villages {counts.get('Village')}), "
          f"counties: {len(county_rows)}")


if __name__ == "__main__":
    main()
