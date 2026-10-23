#!/usr/bin/env python3
"""Batch 25 of the VT #163 municipal fan-out (alphabetical positions
240-249): Waltham, Wardsboro, Warren, Washington, Waterbury,
Waterford, Waterville, Weathersfield, Wells, Wells River Village.
Emits one JSON spec per municipality for build_vt_municipality.py.
Research: vt_muni_batch25_research.md.

Identity calls baked into this batch (all flagged on #163):
- Wardsboro JP Nancy Clark Dawson and cemetery commissioner
  Nancy Dawson are one person (certified JP form governs the name).
  Michelle Hull holds Town Clerk and Town Treasurer as two posts;
  Leigh Ann Varese (auditor + lister), Janice Hull (lister +
  cemetery commissioner) and Patricia Hayes (trustee of public
  funds; her auditor seat is a straggler) are single records.
- Waltham's clerk and treasurer are APPOINTED (Rose Russett, in the
  2026 Town Report's appointed-officials table) -- the Guide's
  Linda Devino is stale. Roberta "Cookie" Steponaitis holds the
  elected Collector of Delinquent Taxes post and a JP seat on one
  record.
- Warren JP J Kenneth Scott was the printed candidate for a 2-year
  Selectboard seat in March 2026 but is NOT on the current board
  (the fifth seat is vacant); he is minted only as a JP. Treasurer
  Patricia Begin is minted from the official 2026 ballot (sole
  printed candidate) + the June 2026 SOS treasurer spreadsheet;
  Jeff Campbell (cemetery) and David Ellison (library) are minted
  under the disclosed sole-candidate + incumbency exception.
- Washington: Scott Blanchard holds Treasurer, Collector of
  Delinquent Taxes and a JP seat on one record; Lois Deberville
  (clerk + JP) and Harry Roush (lister + JP) likewise.
- Waterbury: Bob Butler (lister + JP) and Erin Mooney (library
  commissioner + JP) are single records. Treasurer William
  Shepeluk's name follows the town site over the Guide's
  "Shepeluka."
- Waterford: Kathleen Hodgdon (selectboard + JP) is one record;
  JP Bernard Willey follows the certified form over the town BCA
  page's "Bernard Willey II."
- Waterville: William Baker (lister + JP) and Wanda Locke
  (auditor + JP) are single records; clerk/treasurer Brandi Broe
  is an incumbent-continuity mint (June 2026 SOS spreadsheets +
  Guide), disclosed.
- Wells: Cheryl Woodruff (planning commissioner + JP) is one
  record; Nora Sargent holds Town Clerk and Town Treasurer.
- Wells River: Mary Schilke holds Village Clerk, Village
  Treasurer and Collector of Taxes on one record.
"""
import json
from pathlib import Path

OUT = Path(__file__).parent / "vt_muni_data"
OUT.mkdir(exist_ok=True)

SB_DIR = {
    "url": "https://outside.vermont.gov/dept/sos/Elections_Division/election_info_resources/town_meeting_local_elections/selectboardinformation.pdf",
    "note": "PLACEHOLDER",
}
JP_PDF = {
    "url": "https://outside.vermont.gov/dept/sos/Elections_Division/election_info_resources/candidates/local_office_descriptions/vermont_justices_of_the_peace.pdf",
    "note": "PLACEHOLDER",
}
GUIDE = {
    "url": "https://outside.vermont.gov/dept/sos/Elections_Division/voters/guide_vermonts_town_clerks_treasurers_county.pdf",
    "note": "PLACEHOLDER",
}
STATUTE_2646 = {
    "url": "https://legislature.vermont.gov/statutes/section/17/055/02646",
    "note": "PLACEHOLDER",
}
CLERK_XLSX = {
    "url": "https://outside.vermont.gov/dept/sos/Elections_Division/voters/vermont_town_clerk_contact_information.xlsx",
    "note": "PLACEHOLDER",
}
TREAS_XLSX = {
    "url": "https://outside.vermont.gov/dept/sos/Elections_Division/voters/vermont_town_treasurer_contact_information.xlsx",
    "note": "PLACEHOLDER",
}
CHARTER_159 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/159",
    "note": "PLACEHOLDER",
}
CHARTER_285 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/285",
    "note": "PLACEHOLDER",
}
WALTHAM_REPORT = {"url": "https://www.walthamvt.org/s/2026-Waltham-Town-Report-final.pdf",
                  "note": "PLACEHOLDER"}
WALTHAM_REPORTS_PAGE = {"url": "https://www.walthamvt.org/resources/town-meetings-reports",
                        "note": "PLACEHOLDER"}
WARDSBORO_OFFICIALS = {"url": "https://wardsborovt.gov/town-officials/",
                       "note": "PLACEHOLDER"}
WARDSBORO_BOARDS = {"url": "https://wardsborovt.gov/boards-committees/",
                    "note": "PLACEHOLDER"}
WARDSBORO_REPORT = {"url": "https://wardsborovt.gov/wp-content/uploads/2026/02/Wardsboro-2026-Annual-Town-Report.pdf",
                    "note": "PLACEHOLDER"}
WARDSBORO_WARNING = {"url": "https://wardsborovt.gov/wp-content/uploads/2026/01/2026-Annual-Town-Meeting-Warning.pdf",
                     "note": "PLACEHOLDER"}
WARDSBORO_CEM_NOTICE = {"url": "https://wardsborovt.gov/cemetery-commissioners-meeting-4/",
                        "note": "PLACEHOLDER"}
WARREN_SB = {"url": "https://www.warrenvt.org/departments/select-board/",
             "note": "PLACEHOLDER"}
WARREN_BALLOT = {"url": "https://www.warrenvt.org/wp-content/uploads/2026/02/2026-3-Warnings-Town-Meeting-Combined.pdf",
                 "note": "PLACEHOLDER"}
WARREN_REPORT2023 = {"url": "https://www.warrenvt.org/wp-content/uploads/2023/02/2023-Warren-Town-Report.pdf",
                     "note": "PLACEHOLDER"}
WASHINGTON_OFFICIALS = {"url": "https://www.washingtonvt.org/current-officials",
                        "note": "PLACEHOLDER"}
WATERBURY_SB = {"url": "https://www.waterburyvt.com/boards/selectboard",
                "note": "PLACEHOLDER"}
WATERBURY_CLERK = {"url": "https://www.waterburyvt.com/departments/clerk",
                   "note": "PLACEHOLDER"}
WATERBURY_LISTERS = {"url": "https://www.waterburyvt.com/boards/listers",
                     "note": "PLACEHOLDER"}
WATERBURY_CEMETERY = {"url": "https://www.waterburyvt.com/boards/cemetery",
                      "note": "PLACEHOLDER"}
WATERBURY_COMMISSION = {"url": "https://www.waterburyvt.com/boards/commission",
                        "note": "PLACEHOLDER"}
WATERFORD_SB = {"url": "https://waterfordvt.gov/selectboard.html",
                "note": "PLACEHOLDER"}
WATERFORD_CLERK = {"url": "https://waterfordvt.gov/townclerk.html",
                   "note": "PLACEHOLDER"}
WATERFORD_LISTERS = {"url": "https://waterfordvt.gov/listers.html",
                     "note": "PLACEHOLDER"}
WATERFORD_BCA = {"url": "https://waterfordvt.gov/board-of-civil-authority.html",
                 "note": "PLACEHOLDER"}
WATERFORD_CEMETERY = {"url": "https://waterfordvt.gov/-cemetery-committee",
                      "note": "PLACEHOLDER"}
WATERVILLE_BOARDS = {"url": "http://www.watervillevt.org/boards/",
                     "note": "PLACEHOLDER"}
WATERVILLE_WARNING = {"url": "http://www.watervillevt.org/wp-content/uploads/2026/01/WARNING-FOR-THE-ANNUAL-MEETING-2026.pdf",
                      "note": "PLACEHOLDER"}
WATERVILLE_REPORT = {"url": "http://www.watervillevt.org/wp-content/uploads/2026/02/Waterville-Town-Report-2025.pdf",
                     "note": "PLACEHOLDER"}
WEATHERSFIELD_HOME = {"url": "https://www.weathersfieldvt.org/",
                      "note": "PLACEHOLDER"}
WELLS_OFFICES = {"url": "https://wellsvermont.town/town-offices-2/",
                 "note": "PLACEHOLDER"}
WELLS_SB_PAGE = {"url": "https://wellsvermont.town/town-offices/",
                 "note": "PLACEHOLDER"}
WELLS_DOCS = {"url": "https://wellsvermont.town/documents-reports/",
              "note": "PLACEHOLDER"}
WELLS_PC = {"url": "https://wellsvermont.town/planning-commission/",
            "note": "PLACEHOLDER"}
WELLS_JP = {"url": "https://wellsvermont.town/justice-of-the-peace/",
            "note": "PLACEHOLDER"}
WELLSRIVER_STAFF = {"url": "https://www.wellsrivervillage.org/general-5-1",
                    "note": "PLACEHOLDER"}
WELLSRIVER_WARNING = {"url": "https://www.wellsrivervillage.org/about-1",
                      "note": "PLACEHOLDER"}


def S(src, note):
    d = dict(src)
    d["note"] = note
    return d


def sb_dir(roster_note):
    return S(SB_DIR, "Vermont Secretary of State, Elections Division, "
             "'Vermont Selectboard Members' directory (updated "
             f"June 5, 2026): {roster_note}")


def jp_src(count_note):
    return S(JP_PDF, "Vermont Secretary of State, Elections Division, "
             "'Vermont Justices of the Peace' listing (updated "
             f"December 4, 2025): {count_note}")


def guide(what):
    return S(GUIDE, "Vermont Secretary of State, Elections Division, "
             f"'Guide to Vermont's Town Clerks, Treasurers, and "
             f"County Officials' (January 2026): {what}")


def clerk_xlsx(what):
    return S(CLERK_XLSX, "Vermont Secretary of State, Elections "
             f"Division, town clerk contact spreadsheet (updated "
             f"June 12, 2026): {what}")


def treas_xlsx(what):
    return S(TREAS_XLSX, "Vermont Secretary of State, Elections "
             f"Division, town treasurer contact spreadsheet "
             f"(updated June 12, 2026): {what}")


def statute2646(office_phrase):
    return S(STATUTE_2646, f"17 V.S.A. section 2646: {office_phrase}")


def statute2646_structure(office_phrase):
    return S(STATUTE_2646, "17 V.S.A. section 2646 establishes the "
             f"office ({office_phrase}); no official source "
             "publishes the current holder, so the post is created "
             "without a membership")


def charter159(phrase):
    return S(CHARTER_159, f"24 App. V.S.A. ch. 159 (Town of "
             f"Waterbury): {phrase}")


def charter285(phrase):
    return S(CHARTER_285, f"24 App. V.S.A. ch. 285 (Village of "
             f"Wells River): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 25); issue #163 "
                  f"(VT master tracking).",
    }


def holder(name, slug, **kw):
    d = {"name": name, "slug": slug}
    d.update(kw)
    return d


def spec(place_slug, label, offices, jp=None):
    d = {
        "label": label,
        "place_slug": place_slug,
        "jurisdiction_id": f"ocd-jurisdiction/country:us/state:vt/place:{place_slug}/government",
        "header": f"# {label} municipal roster backfill -- Vermont\n"
                  f"# municipal fan-out batch 25; issue #163 "
                  f"(VT master tracking).\n",
        "offices": offices,
    }
    if jp is not None:
        d["jp_election"] = jp
    return d


def office(slug, title, org_name, seats, sources, holders=(), **kw):
    d = {
        "slug": slug,
        "title": title,
        "org_name": org_name,
        "seats": seats,
        "sources": sources,
        "holders": list(holders),
    }
    d.update(kw)
    return d


SPECS = {}

# ----------------------------------------------------------------
# Town of Waltham (Addison County) -- general law; floor meeting.
# The 2026 Town Report (a scan, read from renders) prints elected
# and appointed officials tables with term-expiry years, plus the
# 2026 warning (Monday, March 2, 2026).
WALTHAM_REP_C = ("Town of Waltham, 2026 Town Report (posted on the "
                 "town's Town Meetings & Reports page)")
SPECS["waltham"] = spec("waltham", "Town of Waltham", [
    office("selectboard", "Selectboard Member",
           "Town of Waltham Selectboard", 3,
           [sb_dir("names Anthony Duprey, Don Ross, and Rhonda "
                   "Williams for Waltham's three-member board"),
            S(WALTHAM_REPORT, WALTHAM_REP_C + ": the pre-meeting "
              "elected-officials table lists Dan Morris (term to "
              "2028) as the third member and Don Ross as Moderator; "
              "the June 2026 directory and the post-meeting state "
              "give Ross the seat -- Morris departed and Ross took "
              "the seat (divergence disclosed on #163)")],
           [holder("Anthony Duprey", "anthony-duprey"),
            holder("Don Ross", "don-ross"),
            holder("Rhonda Williams", "rhonda-williams")]),
    office("town-clerk", "Town Clerk",
           "Town of Waltham Town Clerk", 1,
           [S(WALTHAM_REPORT, WALTHAM_REP_C + ": the APPOINTED "
              "officials table lists Rose Russett as Town Clerk, "
              "'Effective 3/1/26' -- Waltham's clerk is appointed, "
              "so no election is recorded for the office. The "
              "Secretary of State's Guide lists Linda Devino, whom "
              "the report's dedication page shows served "
              "2021-2025 (stale)"),
            clerk_xlsx("names Rose Russett as Waltham's Town "
                       "Clerk")],
           [holder("Rose Russett", "rose-russett",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Waltham Town Treasurer", 1,
           [S(WALTHAM_REPORT, WALTHAM_REP_C + ": the APPOINTED "
              "officials table lists Rose Russett as Town "
              "Treasurer, 'Effective 3/1/26' -- the office is "
              "appointed in Waltham"),
            treas_xlsx("names Rose Russett as Waltham's Town "
                       "Treasurer")],
           [holder("Rose Russett", "rose-russett",
                   how_seated="appointed")]),
    office("moderator", "Town Moderator",
           "Town of Waltham Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term; Don Ross held "
                                  "the office to 2026 per the 2026 "
                                  "report and the 2026 outcome is "
                                  "unpublished")]),
    office("auditor", "Auditor",
           "Town of Waltham Board of Auditors", 3,
           [S(WALTHAM_REPORT, WALTHAM_REP_C + ": elected-officials "
              "table lists Julia Cox (term to 2027) and Jay "
              "Stetzel (term to 2028); Jeffry Glassberg's seat "
              "expired in 2026 (Warning Art. 3C) and its outcome is "
              "unpublished -- straggler, not seated")],
           [holder("Julia Cox", "julia-cox"),
            holder("Jay Stetzel", "jay-stetzel")]),
    office("lister", "Lister",
           "Town of Waltham Board of Listers", 3,
           [S(WALTHAM_REPORT, WALTHAM_REP_C + ": elected-officials "
              "table lists Alexander Cary (term to 2027) and "
              "Robin Jackman (term to 2028); Cathy Sargent's seat "
              "expired in 2026 (Warning Art. 3B), outcome "
              "unpublished -- straggler")],
           [holder("Alexander Cary", "alexander-cary"),
            holder("Robin Jackman", "robin-jackman")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Waltham Cemetery Commissioners", 3,
           [S(WALTHAM_REPORT, WALTHAM_REP_C + ": the report lists "
              "the office among ELECTED officials and the 2026 "
              "Warning (Art. 3D) elects a commissioner for a "
              "three-year term. Amanda Bodell (to 2027) and Susan "
              "Bourdon (to 2028) are seated; Margo Grace's seat "
              "expired in 2026, outcome unpublished -- straggler")],
           [holder("Amanda Bodell", "amanda-bodell"),
            holder("Susan Bourdon", "susan-bourdon")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Waltham Collector of Delinquent Taxes", 1,
           [S(WALTHAM_REPORT, WALTHAM_REP_C + ": elected-officials "
              "table lists Roberta 'Cookie' Steponaitis as "
              "Collector of Delinquent Taxes, term to 2027. She "
              "is also a Justice of the Peace; one person record "
              "carries both memberships")],
           [holder('Roberta "Cookie" Steponaitis',
                   "roberta-steponaitis")]),
    office("first-constable", "First Constable",
           "Town of Waltham First Constable", 1,
           [statute2646_structure("towns elect a first constable; "
                                  "Robin Jackman held the office "
                                  "to 2026 per the 2026 report and "
                                  "the 2026 outcome (Warning "
                                  "Art. 3E) is unpublished")]),
    office("second-constable", "Second Constable",
           "Town of Waltham Second Constable", 1,
           [statute2646_structure("towns may elect a second "
                                  "constable; Waltham's 2026 "
                                  "Warning (Art. 3E) warns the "
                                  "office. Anthony Duprey held it "
                                  "to 2026; the 2026 outcome is "
                                  "unpublished")]),
    office("grand-juror", "Grand Juror",
           "Town of Waltham Grand Jurors", 2,
           [statute2646_structure("towns elect a grand juror; "
                                  "Waltham elects TWO (2026 "
                                  "Warning Art. 3F). Julie Jackman "
                                  "and Nancy Pecca held the seats "
                                  "to 2026; outcomes unpublished")]),
    office("town-agent", "Town Agent",
           "Town of Waltham Town Agent", 1,
           [statute2646_structure("towns elect a town agent; "
                                  "Kevin Bourdon held the office "
                                  "to 2026 per the 2026 report; "
                                  "the 2026 outcome (Warning "
                                  "Art. 3G) is unpublished")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Waltham Justices of the Peace", 3,
           [jp_src("lists three Waltham justices of the peace: "
                   "Roberta 'Cookie' Steponaitis, Terrance Evarts, "
                   "and Rachel Steponaitis")],
           [holder('Roberta "Cookie" Steponaitis',
                   "roberta-steponaitis"),
            holder("Terrance Evarts", "terrance-evarts"),
            holder("Rachel Steponaitis", "rachel-steponaitis")]),
], jp=jp_election("waltham-vt", "Town of Waltham", 3,
                  "certifies the three winners of Waltham's "
                  "November 5, 2024 justice of the peace election "
                  "(vote for three): Roberta 'Cookie' Steponaitis, "
                  "Terrance Evarts, and Rachel Steponaitis. All "
                  "three remain in office"))

# ----------------------------------------------------------------
# Town of Wardsboro (Windham County) -- general law; the 241st
# annual meeting was March 3, 2026. Sources: the town's live Town
# Officials and Boards & Committees pages, the 2026 Annual
# Report's elected-officials list, and the 2026 Warning.
WARDSBORO_REP_C = ("Town of Wardsboro, 2026 Annual Town Report, "
                   "'Elected Town Officials' list")
SPECS["wardsboro"] = spec("wardsboro", "Town of Wardsboro", [
    office("selectboard", "Selectboard Member",
           "Town of Wardsboro Selectboard", 5,
           [S(WARDSBORO_OFFICIALS, "Town of Wardsboro, Town "
              "Officials page (wardsborovt.gov): lists the current "
              "five-member Selectboard -- Duane Tompkins (Chair), "
              "Peter Sebastian (Vice Chair), Clarence 'Dewey' "
              "Ballantine Jr., Michael S. Fitzpatrick Jr., and "
              "Mitch Plimpton. The June 2026 Secretary of State "
              "directory's four rows (incl. 'Harvey Plimpton,' no "
              "Tompkins) are stale; the 2026 report's fifth "
              "pre-meeting member, Diane Schips, held a one-year "
              "seat expiring in 2026, and Plimpton holds a "
              "2026-warned one-year seat")],
           [holder("Duane Tompkins", "duane-tompkins"),
            holder("Peter Sebastian", "peter-sebastian"),
            holder("Clarence Ballantine Jr.", "clarence-ballantine"),
            holder("Michael S. Fitzpatrick Jr.", "michael-fitzpatrick"),
            holder("Mitch Plimpton", "mitch-plimpton")]),
    office("town-clerk", "Town Clerk",
           "Town of Wardsboro Town Clerk", 1,
           [statute2646("towns elect a town clerk; Wardsboro's "
                        "2026 Warning (Art. 2a) elects the clerk "
                        "for a one-year term"),
            guide("lists Michelle Hull as Wardsboro's Town Clerk"),
            clerk_xlsx("names Michelle Hull as Wardsboro's Town "
                       "Clerk"),
            S(WARDSBORO_CEM_NOTICE, "Town of Wardsboro, Cemetery "
              "Commissioners meeting notice (September 10, 2026): "
              "signed 'Michelle Hull, Town Clerk.' Hull's seat "
              "stood at the March 2026 meeting with no published "
              "outcome; the September 2026 signature and both June "
              "2026 Secretary of State sources present her as the "
              "current clerk (incumbent-continuity mint, "
              "disclosed on #163)")],
           [holder("Michelle Hull", "michelle-hull")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Wardsboro Town Treasurer", 1,
           [statute2646("towns elect a town treasurer; "
                        "Wardsboro's 2026 Warning (Art. 2b) elects "
                        "the treasurer for a one-year term"),
            guide("lists Michelle Hull as Wardsboro's Town "
                  "Treasurer"),
            treas_xlsx("names Michelle Hull as Wardsboro's Town "
                       "Treasurer")],
           [holder("Michelle Hull", "michelle-hull")]),
    office("moderator", "Town Moderator",
           "Town of Wardsboro Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term; John Moran held "
                                  "the office to 2026 per the 2026 "
                                  "report and the 2026 floor-vote "
                                  "outcome (Warning Art. 1) is "
                                  "unpublished")]),
    office("auditor", "Auditor",
           "Town of Wardsboro Board of Auditors", 3,
           [S(WARDSBORO_REPORT, WARDSBORO_REP_C + ": lists Leigh "
              "Ann Varese (term to 2028) and Julie McNeal (term "
              "to 2027); Patricia Hayes's seat expired in 2026 "
              "(Warning Art. 2g), outcome unpublished -- "
              "straggler. Hayes is seated as a Trustee of Public "
              "Funds")],
           [holder("Leigh Ann Varese", "leigh-ann-varese"),
            holder("Julie McNeal", "julie-mcneal")]),
    office("lister", "Lister",
           "Town of Wardsboro Board of Listers", 3,
           [S(WARDSBORO_OFFICIALS, "Town of Wardsboro, Town "
              "Officials page: presents Janice Hull, Leigh Ann "
              "Varese, and Katryna Fitzpatrick as the current "
              "listers (the page governs currency; Varese's "
              "report-listed term expired in 2026). Varese is also "
              "an auditor; one record carries both memberships")],
           [holder("Janice Hull", "janice-hull"),
            holder("Leigh Ann Varese", "leigh-ann-varese"),
            holder("Katryna Fitzpatrick", "katryna-fitzpatrick")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Wardsboro Cemetery Commissioners", 5,
           [S(WARDSBORO_REPORT, WARDSBORO_REP_C + ": lists five "
              "commissioners on five-year terms -- Christopher "
              "Shea (to 2030), James Hescock (to 2029), Nancy "
              "Dawson (to 2028), Jane Robinson (to 2027), and "
              "Janice Hull (to 2026, confirmed serving in "
              "September 2026: she signs the commission's "
              "September 10, 2026 meeting notice as Acting "
              "Secretary). DIVERGENCE: the town's Boards & "
              "Committees page names Dewey Ballantine a "
              "commissioner and omits Robinson; the "
              "term-structured report governs (disclosed on "
              "#163). Dawson is the Justice of the Peace Nancy "
              "Clark Dawson; one record carries both")],
           [holder("Christopher Shea", "christopher-shea"),
            holder("James Hescock", "james-hescock"),
            holder("Nancy Clark Dawson", "nancy-clark-dawson"),
            holder("Jane Robinson", "jane-robinson"),
            holder("Janice Hull", "janice-hull")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Wardsboro Collector of Delinquent Taxes", 1,
           [statute2646_structure("towns elect a collector of "
                                  "delinquent taxes; Michelle Hull "
                                  "held the office to 2026 per the "
                                  "2026 report, the seat stood in "
                                  "2026 (Warning Art. 2j), and no "
                                  "current source styles her in "
                                  "the office")]),
    office("first-constable", "First Constable",
           "Town of Wardsboro First Constable", 1,
           [statute2646_structure("towns elect a first constable; "
                                  "the 2026 report shows the seat "
                                  "vacant into 2026 and the 2026 "
                                  "outcome (Warning Art. 2i) is "
                                  "unpublished")]),
    office("town-agent", "Town Agent",
           "Town of Wardsboro Town Agent", 1,
           [statute2646_structure("towns elect a town agent; the "
                                  "2026 report shows the office "
                                  "vacant and the 2026 outcome "
                                  "(Warning Art. 2k) is "
                                  "unpublished")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Wardsboro Trustees of Public Funds", 3,
           [S(WARDSBORO_REPORT, WARDSBORO_REP_C + ": lists "
              "Patricia Hayes (term to 2028) and Thomas Almeida "
              "(term to 2027); Mike Cooney's seat expired in 2026 "
              "(Warning Art. 2h), outcome unpublished -- "
              "straggler")],
           [holder("Patricia Hayes", "patricia-hayes"),
            holder("Thomas Almeida", "thomas-almeida")]),
    office("library-trustee", "Library Trustee",
           "Town of Wardsboro Library Trustees", 7,
           [S(WARDSBORO_REPORT, WARDSBORO_REP_C + ": the report's "
              "own list fixes the board at seven seats and names "
              "Patricia Rappazzo (to 2028), Donna Fernandes (to "
              "2028), Sheri Lewis (to 2027), Karina Martin (to "
              "2027), and Steve Herd (to 2027). The two seats "
              "warned in 2026 (Warning Arts. 2m/2n -- Martin "
              "Loftus's seat and a vacant seat) have no published "
              "outcome -- stragglers")],
           [holder("Patricia Rappazzo", "patricia-rappazzo"),
            holder("Donna Fernandes", "donna-fernandes"),
            holder("Sheri Lewis", "sheri-lewis"),
            holder("Karina Martin", "karina-martin"),
            holder("Steve Herd", "steve-herd")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Wardsboro Justices of the Peace", 5,
           [jp_src("lists five Wardsboro justices of the peace: "
                   "Ken Brace, Nancy Clark Dawson, Nancy "
                   "Meinhard, Cherie Keeler Moran, and George "
                   "Wilson"),
            S(WARDSBORO_REPORT, WARDSBORO_REP_C + ": the town's "
              "own list names only Dawson, Meinhard, and Moran, "
              "with '2 vacancies' -- Brace and Wilson have left "
              "the office, so only the three surviving winners "
              "are seated (departed-winner pattern). Dawson is "
              "also a cemetery commissioner; one record carries "
              "both memberships")],
           [holder("Nancy Clark Dawson", "nancy-clark-dawson"),
            holder("Nancy Meinhard", "nancy-meinhard"),
            holder("Cherie Keeler Moran", "cherie-keeler-moran")]),
], jp=jp_election("wardsboro-vt", "Town of Wardsboro", 5,
                  "certifies the five winners of Wardsboro's "
                  "November 5, 2024 justice of the peace election "
                  "(vote for five): Ken Brace, Nancy Clark Dawson, "
                  "Nancy Meinhard, Cherie Keeler Moran, and George "
                  "Wilson. The town's 2026 Annual Report lists only "
                  "Dawson, Meinhard, and Moran in office, with two "
                  "vacancies, so Brace and Wilson are recorded as "
                  "winners who no longer hold the seat and are not "
                  "seated; the winners list holds the three "
                  "survivors"))

# ----------------------------------------------------------------
# Town of Warren (Washington County) -- general law; Australian
# ballot. Sources: the town's live Selectboard page, the official
# combined 2026 warnings + sample ballot, and the 2023 Town
# Report's officers pages.
WARREN_BALLOT_C = ("Town of Warren, 2026 Town Meeting combined "
                   "warnings and sample ballot (official)")
SPECS["warren"] = spec("warren", "Town of Warren", [
    office("selectboard", "Selectboard Member",
           "Town of Warren Selectboard", 5,
           [S(WARREN_SB, "Town of Warren, Select Board page "
              "(warrenvt.org): lists the current board -- Devin "
              "Klein Corrigan (Chair), Harvey Blake, Joel Taplin, "
              "and Jeremiah Kemp -- four members of a five-seat "
              "board; the fifth seat is VACANT. The June 2026 "
              "Secretary of State directory's Camilla Behn is "
              "stale. J Kenneth Scott was the printed candidate "
              "for a two-year seat on the March 2026 ballot but "
              "is not on the current board; the vacancy sequence "
              "is unpublished and Scott is minted only as a "
              "Justice of the Peace (disclosed on #163)")],
           [holder("Devin Klein Corrigan", "devin-klein-corrigan"),
            holder("Harvey Blake", "harvey-blake"),
            holder("Joel Taplin", "joel-taplin"),
            holder("Jeremiah Kemp", "jeremiah-kemp")]),
    office("town-clerk", "Town Clerk",
           "Town of Warren Town Clerk", 1,
           [statute2646("towns elect a town clerk; Warren elects "
                        "the clerk for a three-year term"),
            guide("lists Brent Adams as Warren's Town Clerk"),
            clerk_xlsx("names Brent Adams as Warren's Town "
                       "Clerk. No clerk race appeared on the "
                       "2026 ballot (the three-year term did not "
                       "stand)")],
           [holder("Brent Adams", "brent-adams")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Warren Town Treasurer", 1,
           [S(WARREN_BALLOT, WARREN_BALLOT_C + ": Patricia Begin "
              "is the sole printed candidate for Town Treasurer "
              "(three-year term). She succeeds Dayna Lisaius, "
              "whom the Secretary of State's Guide still lists "
              "(stale). Ballot + spreadsheet concurrence mint, "
              "disclosed on #163"),
            treas_xlsx("names Patricia Begin as Warren's Town "
                       "Treasurer")],
           [holder("Patricia Begin", "patricia-begin")]),
    office("moderator", "Town Moderator",
           "Town of Warren Town Moderator", 1,
           [S(WARREN_BALLOT, WARREN_BALLOT_C + ": the 2026 "
              "moderator race was write-in only and the winner is "
              "unpublished, so the post is created without a "
              "membership")]),
    office("lister", "Lister",
           "Town of Warren Board of Listers", 3,
           [S(WARREN_REPORT2023, "Town of Warren, 2023 Town "
              "Report, officers pages: fixes the Board of Listers "
              "at three seats on three-year terms, but its roster "
              "is fully expired (2023/2024/2025)"),
            S(WARREN_BALLOT, WARREN_BALLOT_C + ": the 2026 sole "
              "printed lister candidate, Carolyn C. Adams, has no "
              "incumbency or published-outcome evidence -- "
              "straggler sweep; the post is created without "
              "memberships")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Warren Cemetery Commissioners", 5,
           [S(WARREN_REPORT2023, "Town of Warren, 2023 Town "
              "Report: fixes the Cemetery Commission at five "
              "seats on five-year terms and lists Jeff Campbell "
              "to 2026"),
            S(WARREN_BALLOT, WARREN_BALLOT_C + ": Campbell was "
              "the sole printed candidate for the seat in 2026. "
              "Minted under the disclosed sole-candidate + "
              "incumbency exception (#163). The other four "
              "seats' 2024/2025 winners are unpublished -- "
              "stragglers")],
           [holder("Jeff Campbell", "jeff-campbell")]),
    office("library-trustee", "Library Trustee",
           "Town of Warren Library Commission", 5,
           [S(WARREN_REPORT2023, "Town of Warren, 2023 Town "
              "Report: fixes the library board at five seats on "
              "three-year terms (the ballot styles the office "
              "'Library Commission') and lists David Ellison"),
            S(WARREN_BALLOT, WARREN_BALLOT_C + ": Ellison was "
              "the sole printed candidate for one of the two "
              "2026 seats, for a second consecutive cycle. "
              "Minted under the disclosed sole-candidate + "
              "incumbency exception (#163). The second seat's "
              "printed candidate has no incumbency evidence and "
              "no published outcome -- not minted")],
           [holder("David Ellison", "david-ellison")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Warren Trustee of Public Funds", 1,
           [S(WARREN_BALLOT, WARREN_BALLOT_C + ": the office "
              "(styled 'Trustee of Public Money,' three-year "
              "term) stood in 2026 as a write-in-only race; "
              "Dayna Lisaius held it to 2023 per the 2023 Town "
              "Report and the current winner is unpublished")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Warren Collector of Delinquent Taxes", 1,
           [S(WARREN_REPORT2023, "Town of Warren, 2023 Town "
              "Report: Dayna Lisaius held the office (three-year "
              "term) to 2024; the 2024 winner is unpublished and "
              "no race appeared in 2026, so the post is created "
              "without a membership")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Warren Justices of the Peace", 5,
           [jp_src("lists five Warren justices of the peace: "
                   "J Kenneth Scott, Margaret Bullock Wade, Susan "
                   "K Bauchner, Joni Zweig, and Sandra L Brodeur")],
           [holder("J Kenneth Scott", "j-kenneth-scott"),
            holder("Margaret Bullock Wade", "margaret-bullock-wade"),
            holder("Susan K Bauchner", "susan-bauchner"),
            holder("Joni Zweig", "joni-zweig"),
            holder("Sandra L Brodeur", "sandra-brodeur")]),
], jp=jp_election("warren-vt", "Town of Warren", 5,
                  "certifies the five winners of Warren's "
                  "November 5, 2024 justice of the peace election "
                  "(vote for five): J Kenneth Scott, Margaret "
                  "Bullock Wade, Susan K Bauchner, Joni Zweig, and "
                  "Sandra L Brodeur. All five remain in office"))

# ----------------------------------------------------------------
# Town of Washington (Orange County) -- general law. The town's
# Current Officials page is a complete current roster with term
# expiries; read firsthand.
WASHINGTON_PAGE_C = ("Town of Washington, 'Current Officials' "
                     "page (washingtonvt.org)")
SPECS["washington"] = spec("washington", "Town of Washington", [
    office("selectboard", "Selectboard Member",
           "Town of Washington Selectboard", 5,
           [S(WASHINGTON_OFFICIALS, WASHINGTON_PAGE_C + ": lists "
              "the five-member board -- Josh Bell, Maria West, "
              "Tammy Johnson, Jennifer Farnham, and Ricky "
              "Roberts. Concordant with the Secretary of State "
              "directory (which shows Johnson as Chair and styles "
              "her in full; the page's 'Jen Farnham' is Jennifer "
              "Farnham)")],
           [holder("Josh Bell", "josh-bell"),
            holder("Maria West", "maria-west"),
            holder("Tammy Johnson", "tammy-johnson"),
            holder("Jennifer Farnham", "jennifer-farnham"),
            holder("Ricky Roberts", "ricky-roberts")]),
    office("town-clerk", "Town Clerk",
           "Town of Washington Town Clerk", 1,
           [S(WASHINGTON_OFFICIALS, WASHINGTON_PAGE_C + ": lists "
              "Lois Deberville as Town Clerk, three-year term to "
              "2028. She is also a Justice of the Peace; one "
              "person record carries both memberships"),
            guide("lists Lois Deberville as Washington's Town "
                  "Clerk")],
           [holder("Lois Deberville", "lois-deberville")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Washington Town Treasurer", 1,
           [S(WASHINGTON_OFFICIALS, WASHINGTON_PAGE_C + ": lists "
              "Scott Blanchard as Town Treasurer, three-year term "
              "to 2028. He is also the Collector of Delinquent "
              "Taxes and a Justice of the Peace; one person "
              "record carries all three memberships"),
            guide("lists Scott Blanchard as Washington's Town "
                  "Treasurer")],
           [holder("Scott Blanchard", "scott-blanchard")]),
    office("moderator", "Town Moderator",
           "Town of Washington Town Moderator", 1,
           [S(WASHINGTON_OFFICIALS, WASHINGTON_PAGE_C + ": lists "
              "Ben Tiefenthaler as Moderator, one-year term "
              "expiring 2027 (elected at the March 2026 floor "
              "meeting)")],
           [holder("Ben Tiefenthaler", "ben-tiefenthaler")]),
    office("auditor", "Auditor",
           "Town of Washington Board of Auditors", 3,
           [S(WASHINGTON_OFFICIALS, WASHINGTON_PAGE_C + ": the "
              "town's own page states all three auditor seats are "
              "VACANT, so the post is created without "
              "memberships")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Washington Cemetery Commissioners", 3,
           [S(WASHINGTON_OFFICIALS, WASHINGTON_PAGE_C + ": lists "
              "Robert Farnham (term to 2027), Tony Ziter (to "
              "2028), and Robert Blanchard (to 2029) on "
              "three-year terms")],
           [holder("Robert Farnham", "robert-farnham"),
            holder("Tony Ziter", "tony-ziter"),
            holder("Robert Blanchard", "robert-blanchard")]),
    office("library-trustee", "Library Trustee",
           "Town of Washington Library Trustees", 5,
           [S(WASHINGTON_OFFICIALS, WASHINGTON_PAGE_C + ": lists "
              "Andrea Poulin (to 2027), Linda Beede (to 2028), "
              "Joyce Waters (to 2028, on a two-year term), Maxine "
              "Durbrow (to 2029), and Jacob Pelletier (to 2030). "
              "The page notes the trustees voted to move to "
              "two-year terms going forward")],
           [holder("Andrea Poulin", "andrea-poulin"),
            holder("Linda Beede", "linda-beede"),
            holder("Joyce Waters", "joyce-waters"),
            holder("Maxine Durbrow", "maxine-durbrow"),
            holder("Jacob Pelletier", "jacob-pelletier")]),
    office("lister", "Lister",
           "Town of Washington Board of Listers", 3,
           [S(WASHINGTON_OFFICIALS, WASHINGTON_PAGE_C + ": lists "
              "Harry Roush (term to 2028) and Paul Wadkins (to "
              "2027); the third seat is stated VACANT on the "
              "town's page. Roush is also a Justice of the Peace; "
              "one record carries both memberships")],
           [holder("Harry Roush", "harry-roush"),
            holder("Paul Wadkins", "paul-wadkins")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Washington Collector of Delinquent Taxes", 1,
           [S(WASHINGTON_OFFICIALS, WASHINGTON_PAGE_C + ": lists "
              "Scott Blanchard as Collector of Delinquent Taxes, "
              "one-year term expiring 2027")],
           [holder("Scott Blanchard", "scott-blanchard")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Washington Justices of the Peace", 7,
           [jp_src("lists seven Washington justices of the "
                   "peace: Scott Blanchard, Peter Carbee, Lois "
                   "Deberville, Ray McCormack, H. Brooke Paige, "
                   "Harry Roush, and Anna Strong")],
           [holder("Scott Blanchard", "scott-blanchard"),
            holder("Peter Carbee", "peter-carbee"),
            holder("Lois Deberville", "lois-deberville"),
            holder("Ray McCormack", "ray-mccormack"),
            holder("H. Brooke Paige", "h-brooke-paige"),
            holder("Harry Roush", "harry-roush"),
            holder("Anna Strong", "anna-strong")]),
], jp=jp_election("washington-vt", "Town of Washington", 7,
                  "certifies the seven winners of Washington's "
                  "November 5, 2024 justice of the peace election "
                  "(vote for seven): Scott Blanchard, Peter Carbee, "
                  "Lois Deberville, Ray McCormack, H. Brooke Paige, "
                  "Harry Roush, and Anna Strong. All seven remain "
                  "in office"))

# ----------------------------------------------------------------
# Town of Waterbury (Washington County) -- general law; the town
# charter (24 App. V.S.A. ch. 159) covers only a local-option tax
# and the municipal manager and does not displace sec. 2646.
SPECS["waterbury"] = spec("waterbury", "Town of Waterbury", [
    office("selectboard", "Selectboard Member",
           "Town of Waterbury Selectboard", 5,
           [S(WATERBURY_SB, "Town of Waterbury, Selectboard page "
              "(waterburyvt.com): lists the current five-member "
              "board -- Martha Staskus (Chair), Don Schneider "
              "(Vice Chair), Sandy Sabin (Secretary), Roger "
              "Clapp, and Evan Karl Hoffman. The June 2026 "
              "Secretary of State directory's three rows were "
              "partial"),
            charter159("the charter contains only a local-option "
                       "tax (sec. 1) and the municipal-manager "
                       "provision (sec. 2, Act M-20, effective "
                       "March 29, 2024); it does not displace the "
                       "elected town officers of 17 V.S.A. "
                       "sec. 2646")],
           [holder("Martha Staskus", "martha-staskus"),
            holder("Don Schneider", "don-schneider"),
            holder("Sandy Sabin", "sandy-sabin"),
            holder("Roger Clapp", "roger-clapp"),
            holder("Evan Karl Hoffman", "evan-karl-hoffman")]),
    office("town-clerk", "Town Clerk",
           "Town of Waterbury Town Clerk", 1,
           [S(WATERBURY_CLERK, "Town of Waterbury, Clerk page "
              "(waterburyvt.com): names Wes Pollock as Town "
              "Clerk. The Secretary of State's Guide lists Beth "
              "Jones as 'temporary' clerk (stale -- Jones now "
              "sits as a lister)"),
            clerk_xlsx("names Wes Pollock as Waterbury's Town "
                       "Clerk")],
           [holder("Wes Pollock", "wes-pollock")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Waterbury Town Treasurer", 1,
           [S(WATERBURY_CLERK, "Town of Waterbury, Clerk page: "
              "names William Shepeluk as Town Treasurer, without "
              "qualification. The Secretary of State's Guide "
              "styles him 'temporary' treasurer and spells the "
              "name 'Shepeluka'; the transition is complete on "
              "the town's own site and its spelling governs "
              "(disclosed on #163). The June 2026 treasurer "
              "spreadsheet carries no Waterbury row")],
           [holder("William Shepeluk", "william-shepeluk")]),
    office("moderator", "Town Moderator",
           "Town of Waterbury Town Moderator", 1,
           [statute2646_structure("towns elect a moderator; no "
                                  "current official source names "
                                  "a Waterbury moderator (the town "
                                  "votes its articles by "
                                  "Australian ballot), so the post "
                                  "is created without a "
                                  "membership")]),
    office("lister", "Lister",
           "Town of Waterbury Board of Listers", 3,
           [S(WATERBURY_LISTERS, "Town of Waterbury, Listers page "
              "(waterburyvt.com): the three listers -- Bob "
              "Butler, Alec Tuscany, and Beth Jones -- sign the "
              "town's July 2026 grievance notice. Butler is also "
              "a Justice of the Peace; one person record carries "
              "both memberships")],
           [holder("Bob Butler", "bob-butler"),
            holder("Alec Tuscany", "alec-tuscany"),
            holder("Beth Jones", "beth-jones")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Waterbury Cemetery Commissioners", 5,
           [S(WATERBURY_CEMETERY, "Town of Waterbury, Cemetery "
              "Commission page (waterburyvt.com): lists Jill "
              "Chase, Robert Dostis, Jan Gendreau, and John "
              "Woodruff IV (Chair); the fifth seat is shown "
              "VACANT on the town's page")],
           [holder("Jill Chase", "jill-chase"),
            holder("Robert Dostis", "robert-dostis"),
            holder("Jan Gendreau", "jan-gendreau"),
            holder("John Woodruff IV", "john-woodruff")]),
    office("library-trustee", "Library Commissioner",
           "Town of Waterbury Library Commissioners", 5,
           [S(WATERBURY_COMMISSION, "Town of Waterbury, Library "
              "Commission page (waterburyvt.com): lists Michelle "
              "Baker, Anna Black (Chair), Erin Mooney, and Kit "
              "Walker; the fifth seat is shown VACANT on the "
              "town's page. Mooney is also a Justice of the "
              "Peace; one person record carries both "
              "memberships")],
           [holder("Michelle Baker", "michelle-baker"),
            holder("Anna Black", "anna-black"),
            holder("Erin Mooney", "erin-mooney"),
            holder("Kit Walker", "kit-walker")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Waterbury Justices of the Peace", 12,
           [jp_src("lists twelve Waterbury justices of the "
                   "peace: Jim Adams, John Bauer, Bob Butler, "
                   "Linda Gravell, Steve Karcher, Amanda McKay, "
                   "Chris McKay, Mary Miller, Erin Mooney, Bob "
                   "Stanton, Liz Schlegel Stevens, and Katrina "
                   "VanTyne")],
           [holder("Jim Adams", "jim-adams"),
            holder("John Bauer", "john-bauer"),
            holder("Bob Butler", "bob-butler"),
            holder("Linda Gravell", "linda-gravell"),
            holder("Steve Karcher", "steve-karcher"),
            holder("Amanda McKay", "amanda-mckay"),
            holder("Chris McKay", "chris-mckay"),
            holder("Mary Miller", "mary-miller"),
            holder("Erin Mooney", "erin-mooney"),
            holder("Bob Stanton", "bob-stanton"),
            holder("Liz Schlegel Stevens", "liz-schlegel-stevens"),
            holder("Katrina VanTyne", "katrina-vantyne")]),
], jp=jp_election("waterbury-vt", "Town of Waterbury", 12,
                  "certifies the twelve winners of Waterbury's "
                  "November 5, 2024 justice of the peace election "
                  "(vote for twelve): Jim Adams, John Bauer, Bob "
                  "Butler, Linda Gravell, Steve Karcher, Amanda "
                  "McKay, Chris McKay, Mary Miller, Erin Mooney, "
                  "Bob Stanton, Liz Schlegel Stevens, and Katrina "
                  "VanTyne. All twelve remain in office"))

# ----------------------------------------------------------------
# Town of Waterford (Caledonia County) -- general law. Sources:
# the town's live Selectboard, clerk, listers, BCA and cemetery
# pages (waterfordvt.gov).
SPECS["waterford"] = spec("waterford", "Town of Waterford", [
    office("selectboard", "Selectboard Member",
           "Town of Waterford Selectboard", 5,
           [S(WATERFORD_SB, "Town of Waterford, Selectboard page "
              "(waterfordvt.gov): lists the current five-member "
              "board -- Tim Yarrow (Chair), Wade Cochran, Shawn "
              "Hallisey, Kathleen Hodgdon, and Ron Gray. "
              "DIVERGENCE: the June 2026 Secretary of State "
              "directory lists William Jones (Vice Chair) as the "
              "fifth member and omits Gray; the town's live page "
              "governs currency (disclosed on #163). Hodgdon is "
              "also a Justice of the Peace; one record carries "
              "both memberships")],
           [holder("Tim Yarrow", "tim-yarrow"),
            holder("Wade Cochran", "wade-cochran"),
            holder("Shawn Hallisey", "shawn-hallisey"),
            holder("Kathleen Hodgdon", "kathleen-hodgdon"),
            holder("Ron Gray", "ron-gray")]),
    office("town-clerk", "Town Clerk",
           "Town of Waterford Town Clerk", 1,
           [S(WATERFORD_CLERK, "Town of Waterford, Town Clerk page "
              "(waterfordvt.gov): styles her 'Deb Benoit'; the "
              "Secretary of State's Guide gives the full form"),
            guide("lists Debra Benoit as Waterford's Town Clerk")],
           [holder("Debra Benoit", "debra-benoit")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Waterford Town Treasurer", 1,
           [S(WATERFORD_CLERK, "Town of Waterford, Town Clerk page: "
              "names Heather M. Gonyaw as Town Treasurer"),
            guide("lists Heather Gonyaw as Waterford's Town "
                  "Treasurer")],
           [holder("Heather M. Gonyaw", "heather-gonyaw")]),
    office("moderator", "Town Moderator",
           "Town of Waterford Town Moderator", 1,
           [statute2646_structure("towns elect a moderator; no "
                                  "published official source names "
                                  "Waterford's current moderator")]),
    office("lister", "Lister",
           "Town of Waterford Board of Listers", 3,
           [S(WATERFORD_LISTERS, "Town of Waterford, Listers page "
              "(waterfordvt.gov): the page's own sign-off names "
              "the three listers -- Michael Keach, Howard Remick, "
              "and Richard Kozlowski")],
           [holder("Michael Keach", "michael-keach"),
            holder("Howard Remick", "howard-remick"),
            holder("Richard Kozlowski", "richard-kozlowski")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Waterford Justices of the Peace", 7,
           [jp_src("lists seven Waterford justices of the peace: "
                   "Erin Dimick, Kristen Fessenden, Kevin "
                   "Gillander, Kathleen Hodgdon, David Morrison, "
                   "Miriam Simon, and Bernard Willey"),
            S(WATERFORD_BCA, "Town of Waterford, Board of Civil "
              "Authority page: the board (Selectboard + the seven "
              "justices) concurs with the certified slate; it "
              "styles Willey 'Bernard Willey II' -- the certified "
              "form governs his name")],
           [holder("Erin Dimick", "erin-dimick"),
            holder("Kristen Fessenden", "kristen-fessenden"),
            holder("Kevin Gillander", "kevin-gillander"),
            holder("Kathleen Hodgdon", "kathleen-hodgdon"),
            holder("David Morrison", "david-morrison"),
            holder("Miriam Simon", "miriam-simon"),
            holder("Bernard Willey", "bernard-willey")]),
], jp=jp_election("waterford-vt", "Town of Waterford", 7,
                  "certifies the seven winners of Waterford's "
                  "November 5, 2024 justice of the peace election "
                  "(vote for seven): Erin Dimick, Kristen "
                  "Fessenden, Kevin Gillander, Kathleen Hodgdon, "
                  "David Morrison, Miriam Simon, and Bernard "
                  "Willey. All seven remain in office"))

# ----------------------------------------------------------------
# Town of Waterville (Lamoille County) -- general law; floor
# meeting. Sources: the town's live Boards page, the 2026 Warning,
# and the 2025 Town Report's Town Officers list (both PDFs are
# scans, read from renders). NOTE: watervillevt.org serves over
# HTTP only; townoftwaterville.com is Waterville, Wisconsin.
WATERVILLE_REP_C = ("Town of Waterville, 2025 Town Report, 'Town "
                    "Officers' list")
SPECS["waterville"] = spec("waterville", "Town of Waterville", [
    office("selectboard", "Selectboard Member",
           "Town of Waterville Selectboard", 3,
           [S(WATERVILLE_BOARDS, "Town of Waterville, Boards & "
              "Minutes page (watervillevt.org): lists the current "
              "Select Board -- Jay Marsh (Chair), L. Carlos "
              "Martin, and Christopher Mann. Concordant with the "
              "Secretary of State directory and the 2025 Town "
              "Report; Mann's report-listed term expired in 2026 "
              "but the live page presents him as a current "
              "member")],
           [holder("Jay Marsh", "jay-marsh"),
            holder("L. Carlos Martin", "l-carlos-martin"),
            holder("Christopher Mann", "christopher-mann")]),
    office("town-clerk", "Town Clerk",
           "Town of Waterville Town Clerk", 1,
           [S(WATERVILLE_WARNING, "Town of Waterville, Warning for "
              "the Annual Meeting, March 3, 2026: Article 2 elects "
              "the Town Clerk for one year, and Brandi Broe attests "
              "the warning as Town Clerk (January 26, 2026). Her "
              "seat stood in March 2026 with no published outcome; "
              "the Guide and both June 2026 Secretary of State "
              "spreadsheets list her as the current clerk "
              "(incumbent-continuity mint, disclosed on #163)"),
            guide("lists Brandi Broe as Waterville's Town Clerk"),
            clerk_xlsx("names Brandi Broe as Waterville's Town "
                       "Clerk")],
           [holder("Brandi Broe", "brandi-broe")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Waterville Town Treasurer", 1,
           [guide("lists Brandi Broe as Waterville's Town "
                  "Treasurer"),
            treas_xlsx("names Brandi Broe as Waterville's Town "
                       "Treasurer. Incumbent-continuity mint on "
                       "the same basis as the clerk's office "
                       "(disclosed on #163)")],
           [holder("Brandi Broe", "brandi-broe")]),
    office("moderator", "Town Moderator",
           "Town of Waterville Town Moderator", 1,
           [statute2646_structure("towns elect a moderator; "
                                  "Heather Thomas held the office "
                                  "into 2026 per the 2025 Town "
                                  "Report and the 2026 floor-vote "
                                  "outcome (Warning Art. 1) is "
                                  "unpublished")]),
    office("road-commissioner", "Road Commissioner",
           "Town of Waterville Road Commissioner", 1,
           [S(WATERVILLE_WARNING, "Town of Waterville, 2026 "
              "Warning: Article 2 elects a Road Commissioner for "
              "one year -- an elected office in Waterville. "
              "Hunter Locke's term expired in 2026 per the 2025 "
              "Town Report and the outcome is unpublished, so "
              "the post is created without a membership")]),
    office("lister", "Lister",
           "Town of Waterville Board of Listers", 3,
           [S(WATERVILLE_REPORT, WATERVILLE_REP_C + ": lists Cathy "
              "Day (term to 2027) and William Baker (term to "
              "2028); Linda Ward's seat expired in 2026 -- "
              "straggler (Ward remains a Justice of the Peace). "
              "Baker is also a JP; one record carries both")],
           [holder("Cathy Day", "cathy-day"),
            holder("William Baker", "william-baker")]),
    office("auditor", "Auditor",
           "Town of Waterville Board of Auditors", 3,
           [S(WATERVILLE_REPORT, WATERVILLE_REP_C + ": lists "
              "Wanda Locke (term to 2027) and Dustin Tilton (term "
              "to 2028); Donna Barry's seat expired in 2026 -- "
              "straggler. Locke is also a Justice of the Peace; "
              "one record carries both")],
           [holder("Wanda Locke", "wanda-locke"),
            holder("Dustin Tilton", "dustin-tilton")]),
    office("library-trustee", "Library Trustee",
           "Town of Waterville Library Trustees", 7,
           [S(WATERVILLE_REPORT, WATERVILLE_REP_C + ": the "
              "report's own list fixes the board at seven seats "
              "and names Annie Schools (to 2027), Kimberly Mann "
              "(to 2028), and Laurie Ferron (to 2028)"),
            S(WATERVILLE_BOARDS, "Town of Waterville, Boards & "
              "Minutes page: names the same three as the library "
              "board's Chair, Vice Chair, and Secretary. The page "
              "also names Lisa Towery (Treasurer), who is not in "
              "the report -- she may hold the seat warned in 2026 "
              "(Wade Chivington's), outcome unpublished; Towery "
              "and the report's three 2027 trustees absent from "
              "the page (Fairweather, Bressel, Nielson) are "
              "stragglers (disclosed on #163)")],
           [holder("Annie Schools", "annie-schools"),
            holder("Kimberly Mann", "kimberly-mann"),
            holder("Laurie Ferron", "laurie-ferron")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Waterville Collector of Delinquent Taxes", 1,
           [statute2646_structure("towns elect a collector of "
                                  "delinquent taxes; Brandi Broe "
                                  "held the office into 2026 per "
                                  "the 2025 Town Report, the seat "
                                  "stood in 2026 (Warning Art. 2), "
                                  "and no current source styles "
                                  "her in the office")]),
    office("first-constable", "First Constable",
           "Town of Waterville First Constable", 1,
           [statute2646_structure("towns elect a first constable; "
                                  "Robin Genetti held the office "
                                  "into 2026 per the 2025 Town "
                                  "Report; the 2026 outcome is "
                                  "unpublished")]),
    office("second-constable", "Second Constable",
           "Town of Waterville Second Constable", 1,
           [statute2646_structure("towns may elect a second "
                                  "constable; Warren Lyon held the "
                                  "office into 2026 per the 2025 "
                                  "Town Report; the 2026 outcome "
                                  "is unpublished")]),
    office("grand-juror", "Grand Juror",
           "Town of Waterville Grand Juror", 1,
           [statute2646_structure("towns elect a grand juror; "
                                  "Lucas Tilton held the office "
                                  "into 2026 per the 2025 Town "
                                  "Report; the 2026 outcome is "
                                  "unpublished")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Waterville Trustee of Public Funds", 1,
           [S(WATERVILLE_WARNING, "Town of Waterville, 2026 "
              "Warning: Article 2 elects a 'Trustee of Public "
              "Money' for one year. Diane Schwarm held the office "
              "into 2026 per the 2025 Town Report; the outcome is "
              "unpublished, so the post is created without a "
              "membership")]),
    office("town-agent", "Town Agent",
           "Town of Waterville Town Agent", 1,
           [S(WATERVILLE_WARNING, "Town of Waterville, 2026 "
              "Warning: Article 2 elects an 'Agent to Prosecute "
              "and Defend Suits' (the town agent) for one year. "
              "Shawn LaRose held the office into 2026 per the "
              "2025 Town Report; the outcome is unpublished")]),
    office("agent-to-convey-real-estate",
           "Agent to Convey Real Estate",
           "Town of Waterville Agent to Convey Real Estate", 1,
           [S(WATERVILLE_WARNING, "Town of Waterville, 2026 "
              "Warning: Article 2 elects an Agent to Convey Real "
              "Estate for one year -- a distinct warned office in "
              "Waterville, modeled as its own post. Diane Schwarm "
              "held it into 2026 per the 2025 Town Report; the "
              "outcome is unpublished")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Waterville Justices of the Peace", 5,
           [jp_src("lists five Waterville justices of the peace: "
                   "William Baker, Trista Hutchins, Edna "
                   "Lafountain, Wanda Locke, and Linda Ward")],
           [holder("William Baker", "william-baker"),
            holder("Trista Hutchins", "trista-hutchins"),
            holder("Edna Lafountain", "edna-lafountain"),
            holder("Wanda Locke", "wanda-locke"),
            holder("Linda Ward", "linda-ward")]),
], jp=jp_election("waterville-vt", "Town of Waterville", 5,
                  "certifies the five winners of Waterville's "
                  "November 5, 2024 justice of the peace election "
                  "(vote for five): William Baker, Trista Hutchins, "
                  "Edna Lafountain, Wanda Locke, and Linda Ward. "
                  "All five remain in office"))

# ----------------------------------------------------------------
# Town of Wells (Rutland County) -- general law. The town's
# current site is wellsvermont.town (its new 2026 website); the
# old wellsvt.com domain has lapsed. Sources: the site's office
# pages and the 2025 Annual Report's TOWN OFFICIALS table
# (verified firsthand from the report PDF).
WELLS_REP_C = ("Town of Wells, 2025 Annual Report (posted on the "
               "town's Documents & Reports page), 'TOWN OFFICIALS' "
               "table")
SPECS["wells"] = spec("wells", "Town of Wells", [
    office("selectboard", "Selectboard Member",
           "Town of Wells Selectboard", 3,
           [S(WELLS_SB_PAGE, "Town of Wells, Select Board page "
              "(wellsvermont.town): the current board is Don "
              "Preuss (Chair), Paul Woodruff, and Julie Cannata -- "
              "the page states Cannata 'replaces Tammy as select "
              "board member' (Holcomb, whose 2025-report term "
              "expired in 2026). The Secretary of State directory "
              "carries only a referral row for Wells")],
           [holder("Don Preuss", "don-preuss"),
            holder("Paul Woodruff Jr.", "paul-woodruff"),
            holder("Julie Cannata", "julie-cannata")]),
    office("town-clerk", "Town Clerk",
           "Town of Wells Town Clerk", 1,
           [S(WELLS_DOCS, WELLS_REP_C + ": lists Nora Sargent as "
              "Clerk/Treasurer on a three-year term to 2028; the "
              "2025 official ballot carried the clerk and "
              "treasurer as separate races, so the offices are "
              "modeled as two posts with one holder"),
            guide("lists Nora Sargent as Wells's Town Clerk"),
            clerk_xlsx("names Nora Sargent as Wells's Town "
                       "Clerk")],
           [holder("Nora Sargent", "nora-sargent")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Wells Town Treasurer", 1,
           [S(WELLS_DOCS, WELLS_REP_C + ": lists Nora Sargent as "
              "Clerk/Treasurer, three-year term to 2028"),
            guide("lists Nora Sargent as Wells's Town Treasurer")],
           [holder("Nora Sargent", "nora-sargent")]),
    office("moderator", "Town Moderator",
           "Town of Wells Town Moderator", 1,
           [S(WELLS_DOCS, WELLS_REP_C + ": lists Francis Gilman as Moderator "
              "on a one-year term expiring 2026. The seat stood "
              "at the March 2026 meeting and the outcome is "
              "unpublished -- straggler (Gilman is seated as a "
              "planning commissioner on the town's current page)")]),
    office("library-trustee", "Library Trustee",
           "Town of Wells Library Trustees", 5,
           [S(WELLS_DOCS, WELLS_REP_C + ": lists five trustees on five-year "
              "terms -- Amanda Butler (to 2030), Annie "
              "Constantinos (to 2029), Michael Lindley (to "
              "2028), and Nancy Dauenhauer (to 2027); MaryBeth "
              "Harrison's seat expired in 2026, outcome "
              "unpublished -- straggler")],
           [holder("Amanda Butler", "amanda-butler"),
            holder("Annie Constantinos", "annie-constantinos"),
            holder("Michael Lindley", "michael-lindley"),
            holder("Nancy Dauenhauer", "nancy-dauenhauer")]),
    office("planning-commissioner", "Planning Commissioner",
           "Town of Wells Planning Commission", 7,
           [S(WELLS_DOCS, WELLS_REP_C + ": fixes the commission at seven "
              "seats (one shown vacant). Wells elects its "
              "planning commissioners (24 V.S.A. sec. 4323; the "
              "2025 official ballot carried planning commission "
              "races)"),
            S(WELLS_PC, "Town of Wells, Planning Commission page "
              "(wellsvermont.town): names the current members -- "
              "William Chmielewski, Cherry Hopson, Cheryl "
              "Woodruff, Heather Thomas, and Fran Gilman. "
              "Woodruff's and Chmielewski's report-listed terms "
              "expired in 2026, but the current page presents "
              "both as members. DIVERGENCE: Douglas Schlaefer "
              "(report term to 2027) is not on the current page "
              "-- straggler, not seated (disclosed on #163). "
              "Woodruff is also a Justice of the Peace; one "
              "record carries both")],
           [holder("William Chmielewski", "william-chmielewski"),
            holder("Cherry Hopson", "cherry-hopson"),
            holder("Cheryl Woodruff", "cheryl-woodruff"),
            holder("Heather Thomas", "heather-thomas"),
            holder("Francis Gilman", "francis-gilman")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Wells Justices of the Peace", 5,
           [jp_src("lists five Wells justices of the peace: "
                   "Michelle Bates, William Steinmetz, Cheryl "
                   "Woodruff, Jerry Stein, and Victoria Angis"),
            S(WELLS_JP, "Town of Wells, Justice of the Peace page "
              "(wellsvermont.town): concurs on the five names but "
              "misspells Angis as 'Angus' -- the certified form "
              "governs")],
           [holder("Michelle Bates", "michelle-bates"),
            holder("William Steinmetz", "william-steinmetz"),
            holder("Cheryl Woodruff", "cheryl-woodruff"),
            holder("Jerry Stein", "jerry-stein"),
            holder("Victoria Angis", "victoria-angis")]),
], jp=jp_election("wells-vt", "Town of Wells", 5,
                  "certifies the five winners of Wells's "
                  "November 5, 2024 justice of the peace election "
                  "(vote for five): Michelle Bates, William "
                  "Steinmetz, Cheryl Woodruff, Jerry Stein, and "
                  "Victoria Angis. All five remain in office"))

# ----------------------------------------------------------------
# Village of Wells River (in Newbury; Orange County) -- charter,
# 24 App. V.S.A. ch. 285. Sources: the village's Staff page and
# the 2026 Village Warning (annual meeting March 17, 2026).
SPECS["wells-river"] = spec("wells-river", "Village of Wells River", [
    office("village-trustee", "Village Trustee",
           "Village of Wells River Board of Trustees", 3,
           [charter285("sec. 6 elects three trustees on "
                       "three-year staggered terms"),
            S(WELLSRIVER_STAFF, "Village of Wells River, Staff "
              "page (wellsrivervillage.org): lists the trustees "
              "-- Jean Welch (Head Trustee), Mike Thomas, and "
              "Erik White. All three signed the February 12, 2026 "
              "village warning as Trustees")],
           [holder("Jean Welch", "jean-welch"),
            holder("Mike Thomas", "mike-thomas"),
            holder("Erik White", "erik-white")]),
    office("village-president", "Village President",
           "Village of Wells River Village President", 1,
           [charter285("sec. 6 lists the Village President among "
                       "the village's elective officers, and the "
                       "2026 Warning (Art. 1) elects one for a "
                       "one-year term; no official source names "
                       "the current president, so the post is "
                       "created without a membership")]),
    office("village-clerk", "Village Clerk",
           "Village of Wells River Village Clerk", 1,
           [charter285("sec. 6 elects a Village Clerk"),
            S(WELLSRIVER_STAFF, "Village of Wells River, Staff "
              "page: styles Mary Schilke 'Village Clerk, "
              "Treasurer and Tax Collector'; she recorded the "
              "2026 village warning as Village Clerk. One person "
              "record carries all three memberships")],
           [holder("Mary Schilke", "mary-schilke")]),
    office("village-treasurer", "Village Treasurer",
           "Village of Wells River Village Treasurer", 1,
           [charter285("sec. 6 elects a Village Treasurer"),
            S(WELLSRIVER_STAFF, "Village of Wells River, Staff "
              "page: Mary Schilke is the village Treasurer")],
           [holder("Mary Schilke", "mary-schilke")]),
    office("collector-of-taxes", "Collector of Taxes",
           "Village of Wells River Collector of Taxes", 1,
           [charter285("sec. 6 elects a Collector of Taxes"),
            S(WELLSRIVER_STAFF, "Village of Wells River, Staff "
              "page: Mary Schilke is the village Tax Collector")],
           [holder("Mary Schilke", "mary-schilke")]),
    office("village-auditor", "Village Auditor",
           "Village of Wells River Village Auditors", 3,
           [charter285("sec. 6 elects three auditors"),
            S(WELLSRIVER_WARNING, "Village of Wells River, 2026 "
              "Village Warning: Article 1 elects three Village "
              "Auditors for one-year terms. No official source "
              "names the current auditors, so the post is created "
              "without memberships")]),
])

# ----------------------------------------------------------------
# Town of Weathersfield (Windsor County) -- general law; annual
# meeting Feb. 28, 2026 (floor) + March 3, 2026 (Australian
# ballot). Sources: the town's current Selectboard page, the
# FY2024-2025 Town Report's elected-officials list (as of
# Dec. 31, 2025), and the town's posted official March 3, 2026
# ballot tally -- the report list and the tally were verified
# firsthand from the town's own documents.
WEATHERSFIELD_SB = {"url": "https://www.weathersfieldvt.org/326/Selectboard",
                    "note": "PLACEHOLDER"}
WEATHERSFIELD_REPORT = {"url": "https://www.weathersfieldvt.org/DocumentCenter/View/419/FY2025-Town-Report",
                        "note": "PLACEHOLDER"}
WEATHERSFIELD_RESULTS = {"url": "https://www.weathersfieldvt.org/DocumentCenter/View/3229/3326-Town-Voting-Results",
                         "note": "PLACEHOLDER"}
WEATHERSFIELD_CLERK = {"url": "https://www.weathersfieldvt.org/267/Town-Clerk",
                       "note": "PLACEHOLDER"}
WEATHERSFIELD_FINANCE = {"url": "https://www.weathersfieldvt.org/237/Finance",
                         "note": "PLACEHOLDER"}
WTH_REP_C = ("Town of Weathersfield, FY2024-2025 Town Report, "
             "'Town of Weathersfield, Vermont Elected Officials' "
             "list (as of December 31, 2025)")
WTH_RES_C = ("Town of Weathersfield, '3/3/26 Town Voting "
             "Results' -- the official March 3, 2026 ballot with "
             "handwritten tallies, posted on the town's Voting "
             "Results page")
SPECS["weathersfield"] = spec("weathersfield", "Town of Weathersfield", [
    office("selectboard", "Selectboard Member",
           "Town of Weathersfield Selectboard", 5,
           [S(WEATHERSFIELD_SB, "Town of Weathersfield, "
              "Selectboard page (weathersfieldvt.org): lists the "
              "current board -- Rika Henderson (Chair, term to "
              "2029), Dave Fuller (Vice Chair, to 2027), deForest "
              "Bearse (to 2028), Zach Van Valkenburgh (to 2027), "
              "and Joseph Bublat (to 2028)"),
            S(WEATHERSFIELD_RESULTS, WTH_RES_C + ": Henderson "
              "was re-elected to a three-year term (543 votes) "
              "and Bublat elected to a two-year term (471) on "
              "March 3, 2026"),
            S(WEATHERSFIELD_REPORT, WTH_REP_C + ": the "
              "December 2025 roster -- Michael Todd, Henderson, "
              "Kelly O'Brien, Bearse, Nathan McNaughton -- is "
              "what the June 2026 Secretary of State directory "
              "carries (stale). Fuller and Van Valkenburgh now "
              "sit in the seats the report gave Todd and "
              "O'Brien (both expiring 2027); the succession "
              "mechanism is unpublished and the town's current "
              "page governs (disclosed on #163)")],
           [holder("Rika Henderson", "rika-henderson"),
            holder("Dave Fuller", "dave-fuller"),
            holder("DeForest Bearse", "deforest-bearse"),
            holder("Zach Van Valkenburgh", "zach-van-valkenburgh"),
            holder("Joseph Bublat", "joseph-bublat")]),
    office("town-clerk", "Town Clerk",
           "Town of Weathersfield Town Clerk", 1,
           [S(WEATHERSFIELD_REPORT, WTH_REP_C + ": lists Flo-Ann "
              "Dango as Town Clerk, three-year term to 2027"),
            S(WEATHERSFIELD_CLERK, "Town of Weathersfield, Town "
              "Clerk page: names Flo-Ann Dango as Town Clerk"),
            guide("lists Flo-Ann Dango as Weathersfield's Town "
                  "Clerk"),
            clerk_xlsx("names Flo-Ann Dango as Weathersfield's "
                       "Town Clerk")],
           [holder("Flo-Ann Dango", "flo-ann-dango")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Weathersfield Town Treasurer", 1,
           [S(WEATHERSFIELD_REPORT, WTH_REP_C + ": lists Steven "
              "A. Hier as Town Treasurer, three-year term to "
              "2027. He is also a Trustee of Public Funds and a "
              "Justice of the Peace; one person record carries "
              "all three memberships"),
            S(WEATHERSFIELD_FINANCE, "Town of Weathersfield, "
              "Finance page: names Steven Hier as Town Treasurer"),
            guide("lists Steven Hier as Weathersfield's Town "
                  "Treasurer")],
           [holder("Steven Hier", "steven-hier")]),
    office("moderator", "Town Moderator",
           "Town of Weathersfield Town Moderator", 1,
           [S(WEATHERSFIELD_RESULTS, WTH_RES_C + ": Sean Whalen "
              "was elected Moderator (one-year term) on March 3, "
              "2026 with 610 votes. The FY2025 report shows he "
              "held the office as a write-in winner, and he "
              "signed the February 28, 2026 annual meeting "
              "minutes as Moderator")],
           [holder("Sean Whalen", "sean-whalen")]),
    office("lister", "Lister",
           "Town of Weathersfield Board of Listers", 3,
           [S(WEATHERSFIELD_REPORT, WTH_REP_C + ": lists Barbara "
              "Thomas (three-year term to 2027); the other two "
              "seats are shown VACANT"),
            S(WEATHERSFIELD_RESULTS, WTH_RES_C + ": both vacant "
              "seats stood in 2026 as write-in races; the "
              "handwritten write-in names on the tally are not "
              "legibly readable, so those winners are "
              "stragglers, not seated")],
           [holder("Barbara Thomas", "barbara-thomas")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Weathersfield Trustees of Public Funds", 3,
           [S(WEATHERSFIELD_REPORT, WTH_REP_C + ": lists Steven "
              "A. Hier (to 2027), Rick Bates (to 2028), and David "
              "(Hank) Ainley, appointed to a vacancy ('appt. "
              "3yr./1yr. rem.')"),
            S(WEATHERSFIELD_RESULTS, WTH_RES_C + ": Ainley was "
              "then ELECTED to a three-year term on March 3, "
              "2026 (568 votes)")],
           [holder("Steven Hier", "steven-hier"),
            holder("Rick Bates", "rick-bates"),
            holder("David Ainley", "david-ainley")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Weathersfield Cemetery Commissioners", 5,
           [S(WEATHERSFIELD_REPORT, WTH_REP_C + ": lists five "
              "commissioners on five-year terms -- Michael "
              "Stankevich (to 2029), Julia Lloyd Wright (to "
              "2030), Ashley Esty (to 2027), Robert Holtorf (to "
              "2028), and Ken Blum (to 2026)"),
            S(WEATHERSFIELD_RESULTS, WTH_RES_C + ": Blum was "
              "re-elected March 3, 2026 (612 votes). Stankevich "
              "and Lloyd Wright are also Justices of the Peace; "
              "one record each carries both memberships")],
           [holder("Michael J. Stankevich", "michael-stankevich"),
            holder("Julia Lloyd-Wright", "julia-lloyd-wright"),
            holder("Ashley Esty", "ashley-esty"),
            holder("Robert Holtorf", "robert-holtorf"),
            holder("Ken Blum", "ken-blum")]),
    office("library-trustee", "Library Trustee",
           "Town of Weathersfield Library Trustees", 5,
           [S(WEATHERSFIELD_REPORT, WTH_REP_C + ": lists Anne "
              "Parent (to 2027), John Waite (to 2027), Alicia "
              "Jenks (to 2027 -- a write-in winner NAMED in the "
              "town's own officials list), and Rick Bates (to "
              "2028); Mavis Shand's seat expired in 2026. Bates "
              "is also a Trustee of Public Funds; one record "
              "carries both"),
            S(WEATHERSFIELD_RESULTS, WTH_RES_C + ": the 2026 "
              "ballot prints 'MAVIS SHAND ELLINGWOOD' and the "
              "tally elects her (611 votes) -- the same person "
              "as the report's Mavis Shand; the ballot form "
              "governs her name")],
           [holder("Anne Parent", "anne-parent"),
            holder("John Waite", "john-waite"),
            holder("Alicia Jenks", "alicia-jenks"),
            holder("Rick Bates", "rick-bates"),
            holder("Mavis Shand Ellingwood",
                   "mavis-shand-ellingwood")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Weathersfield Justices of the Peace", 10,
           [jp_src("lists ten Weathersfield justices of the "
                   "peace: John Arrison, Andrea Murray, Joseph "
                   "Bublat, Michael J. Stankevich, James Cahill, "
                   "Steven Hier, Julia Lloyd-Wright, August "
                   "Murray, Annemarie Christensen, and Elaine "
                   "Dunham"),
            S(WEATHERSFIELD_REPORT, WTH_REP_C + ": the town's "
              "own justice list concurs on the ten names (in the "
              "variants 'Andrea DeLuna-Murray,' 'Annmarie "
              "Christensen,' 'Steve Hier') and records Elaine "
              "Dunham as RESIGNED -- only the nine surviving "
              "winners are seated (departed-winner pattern)")],
           [holder("John Arrison", "john-arrison"),
            holder("Andrea Murray", "andrea-murray"),
            holder("Joseph Bublat", "joseph-bublat"),
            holder("Michael J. Stankevich", "michael-stankevich"),
            holder("James Cahill", "james-cahill"),
            holder("Steven Hier", "steven-hier"),
            holder("Julia Lloyd-Wright", "julia-lloyd-wright"),
            holder("August Murray", "august-murray"),
            holder("Annemarie Christensen",
                   "annemarie-christensen")]),
], jp=jp_election("weathersfield-vt", "Town of Weathersfield", 10,
                  "certifies the ten winners of Weathersfield's "
                  "November 5, 2024 justice of the peace election "
                  "(vote for ten): John Arrison, Andrea Murray, "
                  "Joseph Bublat, Michael J. Stankevich, James "
                  "Cahill, Steven Hier, Julia Lloyd-Wright, August "
                  "Murray, Annemarie Christensen, and Elaine "
                  "Dunham. The town's FY2025 report records Dunham "
                  "as resigned, so she is recorded as a winner who "
                  "no longer holds the seat and is not seated; "
                  "the winners list holds the nine survivors"))

ORDER = ["waltham", "wardsboro", "warren", "washington",
         "waterbury", "waterford", "waterville", "weathersfield",
         "wells", "wells-river"]

for slug in ORDER:
    (OUT / f"{slug}.json").write_text(
        json.dumps(SPECS[slug], indent=1) + "\n")
print("wrote", len(ORDER), "specs")
