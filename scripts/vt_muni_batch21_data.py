#!/usr/bin/env python3
"""Batch 21 of the VT #163 municipal fan-out (alphabetical positions
200-209): Shaftsbury, Sharon, Sheffield, Shelburne, Sheldon,
Shoreham, Shrewsbury, South Burlington (city), South Hero,
Springfield. Emits one JSON spec per municipality for
build_vt_municipality.py. Research: vt_muni_batch21_research.md.

Identity calls baked into this batch (all flagged on #163):
- Springfield Selectboard Chair Kristi C. Morris is the sitting
  State Representative for Windsor-3 (the district is the Town of
  Springfield): her selectboard holder entry reuses the state-tier
  person record ocd-person/84e1d009-a245-5fc2-b1a9-efe282efe309
  (SB-only reuse, no file edit).
- Springfield JP Alice M. Emmons is the other Windsor-3 State
  Representative: her JP holder entry reuses
  ocd-person/03b80132-73dd-5092-ac62-3d240998978d, and her JP
  candidacy is appended to that record by hand after the build
  (Howland pattern).
- Springfield cemetery commissioner "Beth Gray" (the town's page
  form) is the JP listing's "Elizabeth Gray" -- one person, two
  memberships; the variance is noted in the sources.
- Springfield's prior Trustee of Public Funds "Sue Dana" (term to
  2026) and the 2026 write-in winner Susan Phelps are recorded as
  printed, as two people; no merge is made on the resemblance of
  Phelps's town email (sdanatax@) alone.
- Sharon JP Lisa Flanders is named in the certified listing but
  appears nowhere in the town's own records: the 2025 town report
  shows only four elected JPs serving, with Sherri Lorette seated
  by state appointment to a vacancy. Flanders is excluded entirely
  (Gervais pattern); Lorette is a no-candidacy appointee.
- Shelburne Moderator Thomas A. Little and Constable Robert Lake
  are minted ELECTED under the disclosed sole-candidate exception:
  each was the only candidate on the town's official sample ballot
  and the incumbent; the town's results sheet (self-labeled
  UNOFFICIAL) names both as winners and the current rosters concur.
- Springfield Trustee of Public Funds Susan Phelps and South Hero
  library trustee Elisabeth Wirsing are write-in winners NAMED in
  their towns' certified tallies, with roster concurrence (the
  Norwich Gere pattern); both are minted ELECTED and disclosed.
- South Hero balloted lister seats in 2025 (Cindy Gokey) and 2026
  (Russell Stratton) although ch. 148 sec. 3 makes the listers
  Selectboard-appointed; neither is minted and no lister post is
  created (the appointees are published nowhere). Flagged on #163.
- South Hero Treasurer Kim T. Julow is APPOINTED: the March 2025
  voters authorized a Selectboard-appointed treasurer under
  17 V.S.A. sec. 2651f (YES 578, NO 83) and she continues in the
  office (Pittsford pattern).
- Shoreham's Clerk Laura Siebecker and Treasurer Carol Murphy are
  APPOINTED: the town report files both under Appointed Town
  Officers and neither office appeared on the 2025 warning's ballot
  list or the certified 2026 ballot (secs. 2651e/2651f pattern).
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
CHARTER_013 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/013",
    "note": "PLACEHOLDER",
}
CHARTER_147 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/147",
    "note": "PLACEHOLDER",
}
CHARTER_148 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/148",
    "note": "PLACEHOLDER",
}
CHARTER_149 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/149",
    "note": "PLACEHOLDER",
}
SHAFT_RESULTS = {"url": "https://shaftsburyvt.gov",
                 "note": "PLACEHOLDER"}
SHAFT_REPORT = {"url": "https://shaftsburyvt.gov",
                "note": "PLACEHOLDER"}
SHARON_REPORT = {"url": "https://webgen1files1.revize.com/sharonvt/Documents/Annual%20Reports/2025%20Digital%20Town%20Report.pdf",
                 "note": "PLACEHOLDER"}
SHARON_RESULTS = {"url": "https://webgen1files1.revize.com/sharonvt/Documents/Meeting%20documents/Town%20Meeting/2026%20Sharon%20Town.School%20results.pdf",
                  "note": "PLACEHOLDER"}
SHARON_WARNING = {"url": "https://webgen1files1.revize.com/sharonvt/Documents/Meeting%20documents/Town%20Meeting/3%20Town%20Meeting%202026_WARNING_RECORDED.pdf",
                  "note": "PLACEHOLDER"}
SHARON_SITE = {"url": "https://www.sharonvt.gov/your_government/elected_offices",
               "note": "PLACEHOLDER"}
SHEFF_REPORT = {"url": "https://sheffieldvt.org",
                "note": "PLACEHOLDER"}
SHEL_BALLOT = {"url": "https://shelburnevt.org/DocumentCenter/View/7582/SAMPLE-BALLOT-TOWN-MEETING-2026",
               "note": "PLACEHOLDER"}
SHEL_RESULTS = {"url": "https://shelburnevt.org/DocumentCenter/View/7618/Unofficial-Results-Town-Election-2026",
                "note": "PLACEHOLDER"}
SHEL_REPORT = {"url": "https://shelburnevt.org/Archive.aspx?AMID=38",
               "note": "PLACEHOLDER"}
SHEL_SITE = {"url": "https://shelburnevt.org",
             "note": "PLACEHOLDER"}
SHELD_OFFICERS = {"url": "https://sheldonvt.com",
                  "note": "PLACEHOLDER"}
SHORE_RETURN = {"url": "https://shorehamvt.us",
                "note": "PLACEHOLDER"}
SHORE_REPORT = {"url": "https://shorehamvt.us",
                "note": "PLACEHOLDER"}
SHREW_REPORT = {"url": "https://shrewsburyvt.org",
                "note": "PLACEHOLDER"}
SHREW_RESULTS = {"url": "https://shrewsburyvt.org",
                 "note": "PLACEHOLDER"}
SBURL_RESULTS26 = {"url": "https://www.southburlingtonvt.gov/697/March-3-2026-Town-Meeting-Day-Results",
                   "note": "PLACEHOLDER"}
SBURL_RESULTS24 = {"url": "https://www.southburlingtonvt.gov/214/2024-Town-Meeting-Day-Election-Results",
                   "note": "PLACEHOLDER"}
SBURL_CLERK = {"url": "https://www.southburlingtonvt.gov/209/City-Clerk",
               "note": "PLACEHOLDER"}
SH_RETURN26 = {"url": "https://southherovt.org/town-report/",
               "note": "PLACEHOLDER"}
SH_RETURN25 = {"url": "https://southherovt.org/wp-content/uploads/2026/02/Town-Election-Results-March-2025.pdf",
               "note": "PLACEHOLDER"}
SH_SITE = {"url": "https://southherovt.org/selectboard/",
           "note": "PLACEHOLDER"}
SPR_RETURN = {"url": "https://springfieldvt.gov/elections",
              "note": "PLACEHOLDER"}
SPR_REPORT = {"url": "https://springfieldvt.gov",
              "note": "PLACEHOLDER"}
SPR_SITE = {"url": "https://springfieldvt.gov",
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


def charter013(phrase):
    return S(CHARTER_013, f"24 App. V.S.A. ch. 13 (City of South "
             f"Burlington): {phrase}")


def charter147(phrase):
    return S(CHARTER_147, f"24 App. V.S.A. ch. 147 (Town of "
             f"Shelburne): {phrase}")


def charter148(phrase):
    return S(CHARTER_148, f"24 App. V.S.A. ch. 148 (Town of South "
             f"Hero): {phrase}")


def charter149(phrase):
    return S(CHARTER_149, f"24 App. V.S.A. ch. 149 (Town of "
             f"Springfield): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 21); issue #163 "
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
                  f"# municipal fan-out batch 21; issue #163 "
                  f"(VT master tracking).\n",
        "offices": offices,
    }
    if jp:
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
# Town of Shaftsbury (Bennington County) -- general law.
SHAFT_RES_C = ("Town of Shaftsbury, official results of the March 3, "
               "2026 town meeting ballot (429 ballots cast; attested "
               "by Town Clerk Marlene Hall, March 4, 2026), published "
               "on the town website shaftsburyvt.gov")
SHAFT_REP_C = ("Town of Shaftsbury, 2025 Annual Report, 'TOWN "
               "OFFICERS - ELECTED' table (terms with expiry years)")
SPECS["shaftsbury"] = spec("shaftsbury", "Town of Shaftsbury", [
    office("moderator", "Town Moderator",
           "Town of Shaftsbury Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year term"),
            S(SHAFT_RESULTS, f"{SHAFT_RES_C}: Thomas J. Dailey was "
                             "elected Moderator with 362 votes")],
           [holder("Thomas J. Dailey", "thomas-j-dailey")]),
    office("town-clerk", "Town Clerk",
           "Town of Shaftsbury Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(SHAFT_REPORT, f"{SHAFT_REP_C}: Marlene Hall holds the "
                            "clerk's term to 2027"),
            guide("lists Marlene Hall as Shaftsbury's Town Clerk")],
           [holder("Marlene Hall", "marlene-hall")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Shaftsbury Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(SHAFT_REPORT, f"{SHAFT_REP_C}: Melanie Dexter holds "
                            "the treasurer's term to 2027"),
            guide("lists Melanie Dexter as Shaftsbury's Town "
                  "Treasurer")],
           [holder("Melanie Dexter", "melanie-dexter")]),
    office("selectboard", "Selectboard Member",
           "Town of Shaftsbury Selectboard", 5,
           [S(SHAFT_REPORT, f"{SHAFT_REP_C}: Zoe Contros Kearl "
                            "(Chair, term to 2028), Naomi Miller "
                            "(Vice Chair, to 2027), Michael "
                            "Cichanowski (to 2027), and Marlene Hall "
                            "and Eamon Mulligan held or won the "
                            "remaining seats"),
            S(SHAFT_RESULTS, f"{SHAFT_RES_C}: Marlene Hall was "
                             "elected to a two-year selectboard "
                             "term (359 votes) and Eamon Mulligan "
                             "to a three-year term (333 votes)")],
           [holder("Zoe Contros Kearl", "zoe-contros-kearl"),
            holder("Naomi Miller", "naomi-miller"),
            holder("Michael Cichanowski", "michael-cichanowski"),
            holder("Eamon Mulligan", "eamon-mulligan"),
            holder("Marlene Hall", "marlene-hall")]),
    office("auditor", "Auditor",
           "Town of Shaftsbury Auditors", 3,
           [statute2646("towns elect auditors (three, staggered "
                        "terms) unless the office is eliminated"),
            S(SHAFT_REPORT, f"{SHAFT_REP_C}: Michael Caslin holds "
                            "an auditor term to 2028; the third "
                            "auditor seat is printed 'Vacant'"),
            S(SHAFT_RESULTS, f"{SHAFT_RES_C}: Lisa Lent was "
                             "re-elected auditor with 356 votes")],
           [holder("Michael Caslin", "michael-caslin"),
            holder("Lisa Lent", "lisa-lent")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Shaftsbury Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes"),
            S(SHAFT_RESULTS, f"{SHAFT_RES_C}: Holly Snow Bahan was "
                             "elected Collector of Delinquent Taxes "
                             "with 356 votes (the ballot form of "
                             "her name governs over the annual "
                             "report's 'Holly S. Bahan')")],
           [holder("Holly Snow Bahan", "holly-snow-bahan")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Shaftsbury Trustees of Public Funds", 3,
           [statute2646("towns elect trustees of public funds "
                        "(three)"),
            S(SHAFT_REPORT, f"{SHAFT_REP_C}: Rob Steuer holds a "
                            "term to 2027 and Maggie Royle a term "
                            "to 2028; the third seat's term expired "
                            "in 2026 and no outcome is published, "
                            "so it stands unfilled")],
           [holder("Rob Steuer", "rob-steuer"),
            holder("Maggie Royle", "maggie-royle")]),
    office("first-constable", "First Constable",
           "Town of Shaftsbury First Constable", 1,
           [statute2646_structure("towns elect a first constable "
                                  "for a two-year term; the 2025 "
                                  "report's incumbent's term "
                                  "expired in 2026 and no outcome "
                                  "is published")]),
    office("second-constable", "Second Constable",
           "Town of Shaftsbury Second Constable", 1,
           [statute2646_structure("towns elect a second constable "
                                  "for a two-year term; the 2025 "
                                  "report's incumbent's term "
                                  "expired in 2026 and no outcome "
                                  "is published")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Shaftsbury Justices of the Peace", 12,
           [jp_src("lists twelve Shaftsbury justices of the peace: "
                   "Nancy Burns, Mike Caslin, Abby Chaloux, Joe "
                   "Coonradt, Marna Dailey, Joan Dornhoefer, Carol "
                   "Korman, Ann Mele, Karen Mellinger, Alice "
                   "Miller, Linda Morris, and Joan Vargo")],
           [holder("Nancy Burns", "nancy-burns"),
            holder("Michael Caslin", "michael-caslin",
                   ballot_name="Mike Caslin"),
            holder("Abby Chaloux", "abby-chaloux"),
            holder("Joe Coonradt", "joe-coonradt"),
            holder("Marna Dailey", "marna-dailey"),
            holder("Joan Dornhoefer", "joan-dornhoefer"),
            holder("Carol Korman", "carol-korman"),
            holder("Ann Mele", "ann-mele"),
            holder("Karen Mellinger", "karen-mellinger"),
            holder("Alice Miller", "alice-miller"),
            holder("Linda Morris", "linda-morris"),
            holder("Joan Vargo", "joan-vargo")]),
], jp=jp_election("shaftsbury-vt", "Town of Shaftsbury", 12,
                  "the certified listing names twelve winners for "
                  "Shaftsbury's twelve justice of the peace seats. "
                  "The 2025 annual report's Board of Civil Authority "
                  "table swaps in Dave Mance and Katie Seaton for "
                  "the listing's Nancy Burns and Carol Korman; on "
                  "an equal-count name swap the certified listing "
                  "governs, and Mance and Seaton are held as "
                  "stragglers (flagged on issue #163)",
                  extra_sources=[S(SHAFT_REPORT, f"{SHAFT_REP_C}: "
                                   "the Board of Civil Authority "
                                   "table lists the town's justices "
                                   "of the peace")]))

# ----------------------------------------------------------------
# Town of Sharon (Windsor County) -- general law.
SHARON_REP_C = ("Town of Sharon, 2025 Town Report, 'Town of Sharon "
                "2025 Elected Officials' and '2025 Appointed "
                "Officials' lists (report pp. 14-15)")
SHARON_RES_C = ("Town of Sharon, 'TOWN OF SHARON VERMONT 2026 "
                "RESULTS' sheet, attested by Town Clerk Catherine "
                "Sartor, March 3, 2026 (160 Australian-ballot voters; "
                "100 at the floor meeting)")
SHARON_WARN_C = ("Town of Sharon, Warning for the Annual Town "
                 "Meeting of March 3, 2026 (recorded January 31, "
                 "2026)")
SPECS["sharon"] = spec("sharon", "Town of Sharon", [
    office("moderator", "Town Moderator",
           "Town of Sharon Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(SHARON_RESULTS, f"{SHARON_RES_C}: Stephen Basham was "
                              "elected Town Moderator. The 2025 "
                              "report's meeting guide records that "
                              "no nominating petitions were filed "
                              "for the office; Basham is the "
                              "incumbent moderator, named as the "
                              "winner in the town's own attested "
                              "results, and is recorded as elected "
                              "on that certified outcome (disclosed "
                              "on issue #163)")],
           [holder("Stephen Basham", "stephen-basham")]),
    office("town-clerk", "Town Clerk",
           "Town of Sharon Town Clerk", 1,
           [statute2646("towns elect a town clerk; Sharon elects "
                        "its clerk to a three-year term"),
            S(SHARON_REPORT, f"{SHARON_REP_C}: Catherine Sartor "
                             "holds the clerk's three-year term "
                             "to 2027"),
            guide("lists Catherine Sartor as Sharon's Town Clerk")],
           [holder("Catherine Sartor", "catherine-sartor")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Sharon Town Treasurer", 1,
           [S(SHARON_REPORT, f"{SHARON_REP_C}: the Appointed "
                             "Officials list names Deborah Jones "
                             "as Treasurer (the treasurer is not "
                             "in the town's elected-offices list)"),
            guide("lists Deborah Jones as Sharon's Town Treasurer")],
           [holder("Deborah Jones", "deborah-jones",
                   how_seated="appointed")]),
    office("selectboard", "Selectboard Member",
           "Town of Sharon Selectboard", 3,
           [sb_dir("lists Sharon's three selectboard members: "
                   "Theodore Austin, Kevin Gish (Vice Chair), and "
                   "Scott Henkels (Chair)"),
            S(SHARON_RESULTS, f"{SHARON_RES_C}: Kevin Gish was "
                               "re-elected to the selectboard"),
            S(SHARON_REPORT, f"{SHARON_REP_C}: Scott Henkels's term "
                             "runs to 2027 (Chair) and Ted Austin's "
                             "to 2028; the town's own form 'Ted "
                             "Austin' governs over the directory's "
                             "'Theodore Austin'")],
           [holder("Scott Henkels", "scott-henkels"),
            holder("Kevin Gish", "kevin-gish"),
            holder("Ted Austin", "ted-austin")]),
    office("lister", "Lister",
           "Town of Sharon Board of Listers", 3,
           [statute2646("towns elect a board of listers of three"),
            S(SHARON_REPORT, f"{SHARON_REP_C}: Ken Wright holds a "
                             "lister term to 2028; Helen Barrett "
                             "was appointed to fill a vacancy "
                             "through 2027 (the remainder of Galen "
                             "Mudgett Jr.'s term -- Mudgett "
                             "departed and is not recorded); Nara "
                             "Moore's vacancy appointment ran "
                             "through the 2026 meeting"),
            S(SHARON_RESULTS, f"{SHARON_RES_C}: both 2026 lister "
                               "contests (three-year term and "
                               "one-year remainder) returned "
                               "'Vacant', so the third seat stands "
                               "empty")],
           [holder("Ken Wright", "ken-wright"),
            holder("Helen Barrett", "helen-barrett",
                   how_seated="appointed")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Sharon Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes for a one-year term"),
            S(SHARON_RESULTS, f"{SHARON_RES_C}: Ken Wright was "
                               "re-elected Collector of Delinquent "
                               "Taxes. No nominating petitions were "
                               "filed for the office; Wright is the "
                               "incumbent, named as the winner in "
                               "the town's own attested results, "
                               "and is recorded as elected on that "
                               "certified outcome (disclosed on "
                               "issue #163)")],
           [holder("Ken Wright", "ken-wright")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Sharon Trustees of Public Funds", 3,
           [statute2646("towns elect trustees of public funds "
                        "(three)"),
            S(SHARON_REPORT, f"{SHARON_REP_C}: Pauline Morrill "
                             "holds a term to 2027 and Mary Ayer "
                             "a term to 2028"),
            S(SHARON_RESULTS, f"{SHARON_RES_C}: the floor vote for "
                               "the third seat returned 'Trustee "
                               "of Public Funds -- vacant', so "
                               "Martha Fisk's expiring seat stands "
                               "unfilled")],
           [holder("Pauline Morrill", "pauline-morrill"),
            holder("Mary Ayer", "mary-ayer")]),
    office("library-trustee", "Library Trustee",
           "Baxter Memorial Library Board of Trustees", 5,
           [S(SHARON_REPORT, f"{SHARON_REP_C}: the Trustees of "
                             "Baxter Memorial Library serve "
                             "three-year terms: Finnie Trimpi (to "
                             "2027), Maureen Bassaillon and "
                             "Rebekah Bakos-Kallgren (to 2028), "
                             "with Emma Basham's and Karen Rodis's "
                             "terms expiring in 2026 (Rodis had "
                             "resigned; Marissa Lindman had "
                             "served her seat by appointment since "
                             "February 2025)"),
            S(SHARON_RESULTS, f"{SHARON_RES_C}: the floor meeting "
                               "elected Dee Gish and Marissa "
                               "Lindman trustees of Baxter Library")],
           [holder("Dee Gish", "dee-gish"),
            holder("Marissa Lindman", "marissa-lindman"),
            holder("Finnie Trimpi", "finnie-trimpi"),
            holder("Maureen Bassaillon", "maureen-bassaillon"),
            holder("Rebekah Bakos-Kallgren", "rebekah-bakos-kallgren")]),
    office("chester-downer-endowment-fund-trustee",
           "Chester Downer Endowment Fund Trustee",
           "Chester Downer Endowment Fund", 3,
           [S(SHARON_REPORT, f"{SHARON_REP_C}: Jim Kearns (Chair) "
                             "holds a Downer Fund term to 2027 "
                             "and Justin Shipman a term to 2028"),
            S(SHARON_RESULTS, f"{SHARON_RES_C}: the floor meeting "
                               "elected Chelsea Hadlock a Trustee "
                               "of the Downer Fund")],
           [holder("Chelsea Hadlock", "chelsea-hadlock"),
            holder("Jim Kearns", "jim-kearns"),
            holder("Justin Shipman", "justin-shipman")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Sharon Justices of the Peace", 5,
           [jp_src("lists five Sharon justices of the peace: "
                   "Suzanne Jones, Chelsea Gray, Victoria "
                   "Fullerton, Helen Barrett, and Lisa Flanders")],
           [holder("Suzanne Jones", "suzanne-jones"),
            holder("Chelsea Gray", "chelsea-gray"),
            holder("Victoria Fullerton", "victoria-fullerton"),
            holder("Helen Barrett", "helen-barrett"),
            holder("Sherri Lorette", "sherri-lorette",
                   how_seated="appointed", no_candidacy=True)]),
], jp=jp_election("sharon-vt", "Town of Sharon", 5,
                  "the certified listing names five winners for "
                  "Sharon's five justice of the peace seats. Only "
                  "four of the five serve: the 2025 town report's "
                  "elected list shows Barrett, Fullerton, Gray, and "
                  "Jones, with Sherri Lorette seated by state "
                  "appointment to fill a vacancy -- Lisa Flanders, "
                  "the fifth name in the listing, appears nowhere "
                  "in the town's records and is excluded entirely "
                  "under the departed-winner pattern, her story "
                  "told here. The town voted in March 2025 to "
                  "increase its justices to seven, effective for "
                  "the next cycle",
                  extra_sources=[S(SHARON_REPORT, f"{SHARON_REP_C}: "
                                   "the Justices of the Peace list "
                                   "names Helen Barrett, Victoria "
                                   "Fullerton, Chelsea Gray, and "
                                   "Suzanne Jones from the November "
                                   "2024 general election, plus "
                                   "Sherri Lorette by state "
                                   "appointment to fill a vacancy")]))

# ----------------------------------------------------------------
# Town of Sheffield (Caledonia County) -- general law.
SHEFF_REP_C = ("Town of Sheffield, 2025 Annual Report, 'Town "
               "Officers' tables (elected and appointed; terms with "
               "expiry years), pp. 4-5")
SPECS["sheffield"] = spec("sheffield", "Town of Sheffield", [
    office("moderator", "Town Moderator",
           "Town of Sheffield Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term; the report's "
                                  "incumbent's term expired in "
                                  "2026 and no outcome is "
                                  "published")]),
    office("town-clerk", "Town Clerk",
           "Town of Sheffield Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            clerk_xlsx("lists Erika Lavallee as Sheffield's Town "
                       "Clerk (June 2026, after the 2026 meeting at "
                       "which her reported term expired)"),
            S(SHEFF_REPORT, f"{SHEFF_REP_C}: Erika Lavallee held "
                            "the clerk's term to 2026")],
           [holder("Erika Lavallee", "erika-lavallee")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Sheffield Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            treas_xlsx("lists Erika Lavallee as Sheffield's Town "
                       "Treasurer (June 2026)"),
            guide("lists Erika Lavallee as Sheffield's Town "
                  "Treasurer")],
           [holder("Erika Lavallee", "erika-lavallee")]),
    office("selectboard", "Selectboard Member",
           "Town of Sheffield Selectboard", 3,
           [sb_dir("lists Sheffield's three selectboard members: "
                   "Kate Berry-Buonanno, Erik Lavallee (Chairman), "
                   "and Benjamin Robinson (Walter Smith, whose "
                   "term expired in 2026, has departed)"),
            S(SHEFF_REPORT, f"{SHEFF_REP_C}: the report prints the "
                            "chair as 'Kate Buonanno' -- the "
                            "Secretary of State directory's fuller "
                            "form 'Kate Berry-Buonanno' governs")],
           [holder("Kate Berry-Buonanno", "kate-berry-buonanno"),
            holder("Erik Lavallee", "erik-lavallee"),
            holder("Benjamin Robinson", "benjamin-robinson")]),
    office("lister", "Lister",
           "Town of Sheffield Board of Listers", 3,
           [statute2646("towns elect a board of listers of three"),
            S(SHEFF_REPORT, f"{SHEFF_REP_C}: Edward Jewell holds a "
                            "lister term to 2027 and Mark Cilley a "
                            "term to 2028; the third seat's term "
                            "expired in 2026 and no outcome is "
                            "published, so it stands unfilled")],
           [holder("Edward Jewell", "edward-jewell"),
            holder("Mark Cilley", "mark-cilley")]),
    office("auditor", "Auditor",
           "Town of Sheffield Auditors", 3,
           [statute2646("towns elect auditors (three, staggered "
                        "terms) unless the office is eliminated"),
            S(SHEFF_REPORT, f"{SHEFF_REP_C}: Sarah Warner holds an "
                            "auditor term to 2027 and Vanessa "
                            "Aguilera a term to 2028; the third "
                            "seat's term expired in 2026 and no "
                            "outcome is published")],
           [holder("Sarah Warner", "sarah-warner"),
            holder("Vanessa Aguilera", "vanessa-aguilera")]),
    office("planning-commissioner", "Planning Commissioner",
           "Town of Sheffield Planning Commission", 5,
           [S(SHEFF_REPORT, f"{SHEFF_REP_C}: the report's elected "
                            "officers table lists an elected "
                            "Planning Commission of five (24 V.S.A. "
                            "section 4323 permits an elected "
                            "commission): Barbara Bristol (to "
                            "2027), Al Robertson and Carolyn "
                            "Crankshaw (to 2028); two seats' terms "
                            "expired in 2026 with no published "
                            "outcome")],
           [holder("Barbara Bristol", "barbara-bristol"),
            holder("Al Robertson", "al-robertson"),
            holder("Carolyn Crankshaw", "carolyn-crankshaw")]),
    office("tax-collector", "Tax Collector",
           "Town of Sheffield Tax Collector", 1,
           [S(SHEFF_REPORT, f"{SHEFF_REP_C}: the report's appointed "
                            "officers table names Erika Lavallee "
                            "as the Selectboard-appointed Tax "
                            "Collector (Sheffield elects no "
                            "collector of delinquent taxes)")],
           [holder("Erika Lavallee", "erika-lavallee",
                   how_seated="appointed")]),
    office("constable", "Constable",
           "Town of Sheffield Constable", 1,
           [statute2646_structure("towns elect a constable for a "
                                  "one-year term; the report's "
                                  "incumbent's term expired in "
                                  "2026 and no outcome is "
                                  "published")]),
    office("town-agent", "Town Agent",
           "Town of Sheffield Town Agent", 1,
           [statute2646_structure("towns elect a town agent; the "
                                  "report's incumbent's term "
                                  "expired in 2026 and no outcome "
                                  "is published")]),
    office("cemetery-sexton", "Cemetery Sexton",
           "Town of Sheffield Cemetery Sexton", 1,
           [statute2646_structure("Sheffield's report lists a "
                                  "cemetery sexton among its "
                                  "one-year officers; the "
                                  "incumbent's term expired in "
                                  "2026 and no outcome is "
                                  "published")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Sheffield Justices of the Peace", 5,
           [jp_src("lists five Sheffield justices of the peace: "
                   "Kathy Newland, Sally Wood-Simons, Edward "
                   "Jewell, Gay Ellis, and Barbara 'Bobbie' "
                   "Bristol")],
           [holder("Kathy Newland", "kathy-newland"),
            holder("Sally Wood-Simons", "sally-wood-simons"),
            holder("Edward Jewell", "edward-jewell"),
            holder("Gay Ellis", "gay-ellis"),
            holder("Barbara Bristol", "barbara-bristol",
                   ballot_name="Barbara 'Bobbie' Bristol")]),
], jp=jp_election("sheffield-vt", "Town of Sheffield", 5,
                  "the certified listing names five winners for "
                  "Sheffield's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Shelburne (Chittenden County) -- charter ch. 147.
SHEL_REP_C = ("Town of Shelburne, Town Report for 2025 (238th "
              "Annual Town Report), elected and appointed officers "
              "lists, pp. 5-6")
SHEL_BAL_C = ("Town of Shelburne, Official Sample Ballot, Annual "
              "Town Meeting Election, March 3, 2026")
SHEL_RES_C = ("Town of Shelburne, 'TOWN MEETING RESULTS---"
              "UNOFFICIAL', March 3, 2026 (1,746 ballots cast; "
              "published by Town Clerk Diana Vachon)")
SPECS["shelburne"] = spec("shelburne", "Town of Shelburne", [
    office("moderator", "Town Moderator",
           "Town of Shelburne Town Moderator", 1,
           [charter147("sec. 3.2: the elective officers are the "
                       "five Selectboard members, a Town Clerk, a "
                       "Moderator, and a First Constable"),
            S(SHEL_BALLOT, f"{SHEL_BAL_C}: Thomas A. Little was "
                           "the sole candidate for Town "
                           "Moderator (one-year term)"),
            S(SHEL_RESULTS, f"{SHEL_RES_C}: Thomas A. Little won "
                            "the moderator election with 1,581 "
                            "votes. The results sheet is "
                            "self-labeled UNOFFICIAL; the mint "
                            "rests on the official ballot (sole "
                            "candidate), his incumbency in the "
                            "town report, and the town's current "
                            "rosters (the disclosed sole-candidate "
                            "pattern, flagged on issue #163)")],
           [holder("Thomas A. Little", "thomas-a-little")]),
    office("town-clerk", "Town Clerk",
           "Town of Shelburne Town Clerk", 1,
           [charter147("sec. 3.2: the Town Clerk is an elective "
                       "officer"),
            S(SHEL_REPORT, f"{SHEL_REP_C}: Diana Vachon holds the "
                           "clerk's three-year term to 2027"),
            guide("lists Diana Vachon as Shelburne's Town Clerk")],
           [holder("Diana Vachon", "diana-vachon")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Shelburne Town Treasurer", 1,
           [charter147("sec. 3.5(f): the Selectboard appoints the "
                       "Town Treasurer"),
            S(SHEL_REPORT, f"{SHEL_REP_C}: the 'Appointed by the "
                           "Selectboard' list names Linda Barker "
                           "as Treasurer"),
            guide("lists Linda Barker as Shelburne's Town "
                  "Treasurer")],
           [holder("Linda Barker", "linda-barker",
                   how_seated="appointed")]),
    office("selectboard", "Selectboard Member",
           "Town of Shelburne Selectboard", 5,
           [charter147("sec. 3.2: the Selectboard's five members "
                       "are elective"),
            sb_dir("lists Shelburne's five selectboard members: "
                   "Michael Ashooh, Andrew Everett, Luce Hillman "
                   "(Vice Chair), Chunka Mui, and Matt Wormser "
                   "(Chair)"),
            S(SHEL_BALLOT, f"{SHEL_BAL_C}: Matt Wormser (two-year "
                           "term) and Andrew Everett (three-year "
                           "term) were the sole candidates for "
                           "the two seats on the 2026 ballot"),
            S(SHEL_RESULTS, f"{SHEL_RES_C}: Wormser (1,465) and "
                            "Everett (1,447) were returned as "
                            "elected (self-labeled UNOFFICIAL "
                            "sheet; corroborated by the town's "
                            "current selectboard page)")],
           [holder("Matt Wormser", "matt-wormser"),
            holder("Luce Hillman", "luce-hillman"),
            holder("Michael Ashooh", "michael-ashooh"),
            holder("Andrew Everett", "andrew-everett"),
            holder("Chunka Mui", "chunka-mui")]),
    office("first-constable", "Town Constable",
           "Town of Shelburne Town Constable", 1,
           [charter147("sec. 3.2: a First Constable is an elective "
                       "officer (the town styles the office Town "
                       "Constable)"),
            S(SHEL_BALLOT, f"{SHEL_BAL_C}: Bob Lake was the sole "
                           "candidate for Town Constable "
                           "(two-year term)"),
            S(SHEL_RESULTS, f"{SHEL_RES_C}: Bob Lake won with "
                            "1,476 votes (self-labeled UNOFFICIAL "
                            "sheet; the mint rests on the official "
                            "ballot, his incumbency in the town "
                            "report, and roster concurrence -- "
                            "disclosed sole-candidate pattern)"),
            S(SHEL_REPORT, f"{SHEL_REP_C}: Robert Lake, Constable, "
                           "term to 2026")],
           [holder("Robert Lake", "robert-lake",
                   ballot_name="Bob Lake")]),
    office("grand-juror", "Grand Juror",
           "Town of Shelburne Grand Juror", 1,
           [charter147("sec. 3.5(a): the Selectboard appoints the "
                       "other officers required by law"),
            S(SHEL_SITE, "Town of Shelburne, Selectboard page "
                         "(current): the 'Town Officials "
                         "Appointed by the Selectboard' list "
                         "names Tim Pudvar as Grand Juror")],
           [holder("Tim Pudvar", "tim-pudvar",
                   how_seated="appointed")]),
    office("champlain-water-district-representative",
           "Champlain Water District Representative",
           "Champlain Water District", 1,
           [S(SHEL_REPORT, f"{SHEL_REP_C}: the elected officials "
                           "list names Pete Gadue as Champlain "
                           "Water District Director, term to 2027 "
                           "(Shelburne elects its representative "
                           "to the district)")],
           [holder("Peter E. Gadue", "peter-e-gadue")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Shelburne Justices of the Peace", 15,
           [jp_src("lists fifteen Shelburne justices of the peace: "
                   "Nancy E. Baker, Susan Bowen, Jessica Brumsted, "
                   "Joanna Cole, Bill Deming, Mike Donohue, Peter "
                   "E. Gadue, Joan G. Lenes, Jennifer Leopold, Deb "
                   "Mayfield, Rebecca A. Moore, Judy P. "
                   "Rosenstreich, Randy Roland, Lee Suskin, and "
                   "David W. Webster")],
           [holder("Nancy E. Baker", "nancy-e-baker"),
            holder("Susan Bowen", "susan-bowen"),
            holder("Jessica Brumsted", "jessica-brumsted"),
            holder("Joanna Cole", "joanna-cole"),
            holder("Bill Deming", "bill-deming"),
            holder("Mike Donohue", "mike-donohue"),
            holder("Peter E. Gadue", "peter-e-gadue"),
            holder("Joan G. Lenes", "joan-g-lenes"),
            holder("Jennifer Leopold", "jennifer-leopold"),
            holder("Deb Mayfield", "deb-mayfield"),
            holder("Rebecca A. Moore", "rebecca-a-moore"),
            holder("Judy P. Rosenstreich", "judy-p-rosenstreich"),
            holder("Randy Roland", "randy-roland"),
            holder("Lee Suskin", "lee-suskin"),
            holder("David W. Webster", "david-w-webster")]),
], jp=jp_election("shelburne-vt", "Town of Shelburne", 15,
                  "the certified listing names fifteen winners for "
                  "Shelburne's fifteen justice of the peace seats; "
                  "the 2025 town report's justice list concurs "
                  "name-for-name",
                  extra_sources=[S(SHEL_REPORT, f"{SHEL_REP_C}: the "
                                   "Justices of the Peace list "
                                   "names all fifteen")]))

# ----------------------------------------------------------------
# Town of Sheldon (Franklin County) -- general law.
SHELD_OFF_C = ("Town of Sheldon, Town Officers page "
               "(sheldonvt.com), headed 'March 3, 2026 - March 2, "
               "2027', listing elected and appointed officers with "
               "term years")
SPECS["sheldon"] = spec("sheldon", "Town of Sheldon", [
    office("moderator", "Town Moderator",
           "Town of Sheldon Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(SHELD_OFFICERS, f"{SHELD_OFF_C}: Rebecca Jacobs is "
                              "Town Moderator")],
           [holder("Rebecca Jacobs", "rebecca-jacobs")]),
    office("town-clerk", "Town Clerk",
           "Town of Sheldon Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(SHELD_OFFICERS, f"{SHELD_OFF_C}: Jane Lanza is Town "
                              "Clerk (the page styles the combined "
                              "office 'Town Clerk & Treasurer'; "
                              "the two posts are recorded "
                              "separately)"),
            guide("lists Jane Lanza as Sheldon's Town Clerk")],
           [holder("Jane Lanza", "jane-lanza")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Sheldon Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(SHELD_OFFICERS, f"{SHELD_OFF_C}: Jane Lanza is Town "
                              "Treasurer"),
            guide("lists Jane Lanza as Sheldon's Town Treasurer")],
           [holder("Jane Lanza", "jane-lanza")]),
    office("selectboard", "Selectboard Member",
           "Town of Sheldon Selectboard", 5,
           [sb_dir("lists Sheldon's five selectboard members: "
                   "Maria Davison, Stephen Dodd (Chair), Nicholas "
                   "Norris, Richard Piaseczny, and Porsche "
                   "Trombley"),
            S(SHELD_OFFICERS, f"{SHELD_OFF_C}: Stephen Dodd "
                              "(Chair, term to 2029), Richard "
                              "Piaseczny (Vice Chair, to 2028 -- "
                              "the officers page misprints "
                              "'Piascezny'; the directory, the "
                              "justices listing, and his town "
                              "email all spell Piaseczny), "
                              "Porsche Trombley (to 2028), Maria "
                              "Davison (to 2027), Nicholas Norris "
                              "(to 2027)")],
           [holder("Stephen Dodd", "stephen-dodd"),
            holder("Richard Piaseczny", "richard-piaseczny"),
            holder("Porsche Trombley", "porsche-trombley"),
            holder("Maria Davison", "maria-davison"),
            holder("Nicholas Norris", "nicholas-norris")]),
    office("library-trustee", "Library Trustee",
           "Town of Sheldon Library Trustees", 5,
           [S(SHELD_OFFICERS, f"{SHELD_OFF_C}: the Library Trustees "
                              "serve staggered five-year terms, "
                              "one expiring each year (22 V.S.A. "
                              "section 143 pattern): Lindsay "
                              "Dunlavey (to 2027), Jessica Draper "
                              "(to 2028), John Stryker (to 2029), "
                              "Maria Davison (Chair, to 2030), "
                              "Amy Jenkins (to 2031)")],
           [holder("Lindsay Dunlavey", "lindsay-dunlavey"),
            holder("Jessica Draper", "jessica-draper"),
            holder("John Stryker", "john-stryker"),
            holder("Maria Davison", "maria-davison"),
            holder("Amy Jenkins", "amy-jenkins")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Sheldon Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes"),
            S(SHELD_OFFICERS, f"{SHELD_OFF_C}: Jane Lanza is "
                              "Collector of Delinquent Taxes")],
           [holder("Jane Lanza", "jane-lanza")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Sheldon Justices of the Peace", 5,
           [jp_src("lists five Sheldon justices of the peace: "
                   "Susan Brooks, Deborah Kittell, Dianne Crane, "
                   "Shannon Kane, and Stephen Dodd"),
            S(SHELD_OFFICERS, f"{SHELD_OFF_C}: the town's justices "
                              "page concurs (its 'DiAnne Crane' "
                              "yields to the listing's 'Dianne "
                              "Crane')")],
           [holder("Susan Brooks", "susan-brooks"),
            holder("Deborah Kittell", "deborah-kittell"),
            holder("Dianne Crane", "dianne-crane"),
            holder("Shannon Kane", "shannon-kane"),
            holder("Stephen Dodd", "stephen-dodd")]),
], jp=jp_election("sheldon-vt", "Town of Sheldon", 5,
                  "the certified listing names five winners for "
                  "Sheldon's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Shoreham (Addison County) -- general law; clerk and
# treasurer converted to appointed offices.
SHORE_RET_C = ("Town of Shoreham, Official Return of Votes, "
               "Annual Town Meeting, March 3, 2026 (191 voters; "
               "certified by Town Clerk Laura Siebecker), published "
               "on the town website shorehamvt.us")
SHORE_REP_C = ("Town of Shoreham, 2024 Annual Report, elected and "
               "appointed town officers tables")
SPECS["shoreham"] = spec("shoreham", "Town of Shoreham", [
    office("moderator", "Town Moderator",
           "Town of Shoreham Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(SHORE_RETURN, f"{SHORE_RET_C}: the 2026 moderator "
                            "contest had no ballot candidate; "
                            "the write-in plurality (Jonathan "
                            "Hescock, 78) does not seat, so the "
                            "post stands without a membership "
                            "(flagged on issue #163)")]),
    office("town-clerk", "Town Clerk",
           "Town of Shoreham Town Clerk", 1,
           [S(SHORE_REPORT, f"{SHORE_REP_C}: the Town Clerk is "
                            "filed under Appointed Town Officers, "
                            "and the office appeared on neither "
                            "the 2025 warning's ballot list nor "
                            "the 2026 ballot -- Shoreham has "
                            "converted the clerk to an appointed "
                            "office (17 V.S.A. section 2651e "
                            "pattern). Laura Siebecker signs the "
                            "2026 return as Town Clerk"),
            guide("lists Laura Siebecker as Shoreham's Town Clerk")],
           [holder("Laura Siebecker", "laura-siebecker",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Shoreham Town Treasurer", 1,
           [S(SHORE_REPORT, f"{SHORE_REP_C}: the Town Treasurer is "
                            "filed under Appointed Town Officers "
                            "(17 V.S.A. section 2651f pattern)"),
            guide("lists Carol Murphy as Shoreham's Town "
                  "Treasurer")],
           [holder("Carol Murphy", "carol-murphy",
                   how_seated="appointed")]),
    office("selectboard", "Selectboard Member",
           "Town of Shoreham Selectboard", 5,
           [sb_dir("lists Shoreham's five selectboard members: "
                   "Stephen Goodrich (Chair), Rebecca Kerr (Vice "
                   "Chair), Peter Lynch, Mark Spitzner, and Loren "
                   "Wood"),
            S(SHORE_RETURN, f"{SHORE_RET_C}: Rebecca Kerr was "
                            "re-elected (166 votes), Peter Lynch "
                            "re-elected to a three-year term "
                            "(172), and Mark Spitzner elected "
                            "(163); Molly Francis departed")],
           [holder("Stephen Goodrich", "stephen-goodrich"),
            holder("Rebecca Kerr", "rebecca-kerr"),
            holder("Peter Lynch", "peter-lynch"),
            holder("Mark Spitzner", "mark-spitzner"),
            holder("Loren Wood", "loren-wood")]),
    office("lister", "Lister",
           "Town of Shoreham Board of Listers", 3,
           [statute2646("towns elect a board of listers of three"),
            S(SHORE_REPORT, f"{SHORE_REP_C}: Phil Kivlin holds a "
                            "lister term to 2027"),
            S(SHORE_RETURN, f"{SHORE_RET_C}: the 2026 lister "
                            "contest drew only three scattered "
                            "write-in votes against 188 blanks, "
                            "which never seats; the second seat "
                            "(an appointee's expiring term) and "
                            "the third (already vacant) stand "
                            "unfilled")],
           [holder("Phil Kivlin", "phil-kivlin")]),
    office("auditor", "Auditor",
           "Town of Shoreham Auditors", 3,
           [statute2646("towns elect auditors (three, staggered "
                        "terms) unless the office is eliminated"),
            S(SHORE_REPORT, f"{SHORE_REP_C}: Maureen Gour holds "
                            "an auditor term to 2027"),
            S(SHORE_RETURN, f"{SHORE_RET_C}: both 2026 auditor "
                            "contests (three-year term and "
                            "one-year remainder) drew only "
                            "scattered write-ins, which never "
                            "seat")],
           [holder("Maureen Gour", "maureen-gour")]),
    office("planning-commissioner", "Planning Commissioner",
           "Town of Shoreham Planning Commission", 7,
           [S(SHORE_REPORT, f"{SHORE_REP_C}: the report's elected "
                            "table lists a seven-member elected "
                            "Planning Commission; Caroline Paske "
                            "holds a term to 2028. The four seats "
                            "filled at the 2025 meeting are "
                            "published nowhere, so their holders "
                            "are held as stragglers (flagged on "
                            "issue #163)"),
            S(SHORE_RETURN, f"{SHORE_RET_C}: Carrie Marini was "
                            "re-elected (150 votes), Timothy "
                            "Steady elected (164), and Peter Lynch "
                            "elected to a one-year remainder (168)")],
           [holder("Caroline Paske", "caroline-paske"),
            holder("Carrie Marini", "carrie-marini"),
            holder("Timothy Steady", "timothy-steady"),
            holder("Peter Lynch", "peter-lynch")]),
    office("library-trustee", "Library Trustee",
           "Town of Shoreham Library Trustees", 5,
           [S(SHORE_REPORT, f"{SHORE_REP_C}: Tanya Scuteri holds a "
                            "library term to 2027, Cora Waag "
                            "(Chair) to 2028, and Katie Flagg to "
                            "2029"),
            S(SHORE_RETURN, f"{SHORE_RET_C}: Laura Siebecker was "
                            "re-elected a library trustee (168 "
                            "votes) and Susan Spitzner elected "
                            "(175). The return labels the two "
                            "2026 seats four-year and three-year "
                            "terms, which does not square with "
                            "the report's five-year stagger; the "
                            "discrepancy is flagged on issue "
                            "#163")],
           [holder("Tanya Scuteri", "tanya-scuteri"),
            holder("Cora Waag", "cora-waag"),
            holder("Katie Flagg", "katie-flagg"),
            holder("Laura Siebecker", "laura-siebecker"),
            holder("Susan Spitzner", "susan-spitzner")]),
    office("tri-town-water-district-representative",
           "Tri-Town Water District Commissioner",
           "Tri-Town Water District", 3,
           [S(SHORE_REPORT, f"{SHORE_REP_C}: the Tri-Town Water "
                            "Commissioners are elected; Lance "
                            "Wood holds a term to 2027"),
            S(SHORE_RETURN, f"{SHORE_RET_C}: Brian R. Treadway "
                            "was elected a Tri-Town Water "
                            "Commissioner (172 votes); the third "
                            "seat's 2025 outcome is unpublished "
                            "(straggler)")],
           [holder("Lance Wood", "lance-wood"),
            holder("Brian R. Treadway", "brian-r-treadway")]),
    office("constable", "Constable",
           "Town of Shoreham Constable", 1,
           [statute2646("towns elect a constable"),
            S(SHORE_REPORT, f"{SHORE_REP_C}: the constable seat "
                            "is printed vacant, and the office "
                            "did not appear on the 2026 ballot, "
                            "so the post stands without a "
                            "membership")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Shoreham Justices of the Peace", 7,
           [jp_src("lists two Shoreham justices of the peace: "
                   "Roberta Blodgett and Martha Teer (verified "
                   "against the raw listing text -- the slate is "
                   "not truncated at a page break)")],
           [holder("Roberta Blodgett", "roberta-blodgett"),
            holder("Martha Teer", "martha-teer")]),
], jp=jp_election("shoreham-vt", "Town of Shoreham", 7,
                  "the certified listing names two winners; the "
                  "2024 annual report's justice line reads "
                  "'Vacancies (5)', fixing Shoreham's justice of "
                  "the peace seats at seven with five unfilled at "
                  "the November 2024 election",
                  extra_sources=[S(SHORE_REPORT, f"{SHORE_REP_C}: "
                                   "the officers table gives the "
                                   "justices of the peace with "
                                   "five vacancies")]))

# ----------------------------------------------------------------
# Town of Shrewsbury (Rutland County) -- general law.
SHREW_REP_C = ("Town of Shrewsbury, 2025 Annual Report, '2025 "
               "Elected Town Officers as of December 31, 2025' "
               "table")
SHREW_RES_C = ("Town of Shrewsbury, published results of the "
               "March 3, 2026 annual meeting (Australian ballot)")
SPECS["shrewsbury"] = spec("shrewsbury", "Town of Shrewsbury", [
    office("moderator", "Town Moderator",
           "Town of Shrewsbury Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(SHREW_RESULTS, f"{SHREW_RES_C}: Eldred French was "
                             "re-elected Moderator with 167 "
                             "votes")],
           [holder("Eldred French", "eldred-french")]),
    office("town-clerk", "Town Clerk",
           "Town of Shrewsbury Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(SHREW_REPORT, f"{SHREW_REP_C}: Rebecca Rice holds "
                            "the clerk's term to 2027"),
            guide("lists Rebecca Rice as Shrewsbury's Town Clerk")],
           [holder("Rebecca Rice", "rebecca-rice")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Shrewsbury Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(SHREW_REPORT, f"{SHREW_REP_C}: Linda McGuire holds "
                            "the treasurer's term to 2027"),
            guide("lists Linda McGuire as Shrewsbury's Town "
                  "Treasurer")],
           [holder("Linda McGuire", "linda-mcguire")]),
    office("selectboard", "Selectboard Member",
           "Town of Shrewsbury Selectboard", 3,
           [sb_dir("lists Shrewsbury's three selectboard members: "
                   "Marc Cimonetti (the directory's 'Cimonette' is "
                   "a misprint -- its own email for him reads "
                   "mcimonetti), Aaron Korzun (Chairman), and "
                   "Francis Wyatt"),
            S(SHREW_RESULTS, f"{SHREW_RES_C}: Francis Wyatt was "
                             "re-elected with 154 votes; Marc "
                             "Cimonetti's term runs to 2028 and "
                             "Aaron Korzun's to 2027")],
           [holder("Marc Cimonetti", "marc-cimonetti"),
            holder("Aaron Korzun", "aaron-korzun"),
            holder("Francis Wyatt", "francis-wyatt")]),
    office("auditor", "Auditor",
           "Town of Shrewsbury Auditors", 3,
           [statute2646("towns elect auditors (three, staggered "
                        "terms) unless the office is eliminated"),
            S(SHREW_REPORT, f"{SHREW_REP_C}: Sanford Bragg holds "
                            "an auditor term to 2027"),
            S(SHREW_RESULTS, f"{SHREW_RES_C}: Michelle Greene was "
                             "re-elected auditor with 156 votes; "
                             "the two-year auditor contest drew "
                             "only write-ins and 'no candidate "
                             "received the requisite number of "
                             "votes', so the third seat stands "
                             "vacant")],
           [holder("Michelle Greene", "michelle-greene"),
            holder("Sanford Bragg", "sanford-bragg")]),
    office("first-constable", "First Constable",
           "Town of Shrewsbury First Constable", 1,
           [statute2646("towns elect a first constable"),
            S(SHREW_RESULTS, f"{SHREW_RES_C}: the 2026 first "
                             "constable contest drew only "
                             "write-ins and produced no winner, "
                             "so the post stands without a "
                             "membership")]),
    office("second-constable", "Second Constable",
           "Town of Shrewsbury Second Constable", 1,
           [statute2646("towns elect a second constable"),
            S(SHREW_RESULTS, f"{SHREW_RES_C}: Steve Walsh was "
                             "elected Second Constable with 158 "
                             "votes (the 2025 report shows him "
                             "holding the seat by appointment; "
                             "the ballot form 'Steve Walsh' is "
                             "recorded as the candidacy name for "
                             "Stevenson Walsh)")],
           [holder("Stevenson Walsh", "stevenson-walsh")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Shrewsbury Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes"),
            S(SHREW_REPORT, f"{SHREW_REP_C}: Steven Nicholson "
                            "holds the collector's term to 2027")],
           [holder("Steven Nicholson", "steven-nicholson")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Shrewsbury Cemetery Commission", 3,
           [S(SHREW_REPORT, f"{SHREW_REP_C}: Benny Carrara and "
                            "Eric Carrara hold cemetery terms to "
                            "2027"),
            S(SHREW_RESULTS, f"{SHREW_RES_C}: George Brigham Jr. "
                             "was re-elected a Cemetery "
                             "Commissioner with 173 votes")],
           [holder("George Brigham Jr.", "george-brigham-jr"),
            holder("Benny Carrara", "benny-carrara"),
            holder("Eric Carrara", "eric-carrara")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Shrewsbury Justices of the Peace", 7,
           [jp_src("lists seven Shrewsbury justices of the peace: "
                   "Barry E. Griffith, Adrienne Raymond, Patricia "
                   "Norton, Betsy Jesser, Robert W. Ferguson, "
                   "Johanna (Taffy) Maynard, and Lucy (Ludy) "
                   "Biddle")],
           [holder("Barry E. Griffith", "barry-e-griffith"),
            holder("Adrienne Raymond", "adrienne-raymond"),
            holder("Patricia Norton", "patricia-norton"),
            holder("Betsy Jesser", "betsy-jesser"),
            holder("Robert W. Ferguson", "robert-w-ferguson"),
            holder("Johanna Maynard", "johanna-maynard",
                   ballot_name="Johanna (Taffy) Maynard"),
            holder("Lucy Biddle", "lucy-biddle",
                   ballot_name="Lucy (Ludy) Biddle")]),
], jp=jp_election("shrewsbury-vt", "Town of Shrewsbury", 7,
                  "the certified listing names seven winners for "
                  "Shrewsbury's seven justice of the peace seats; "
                  "the 2025 annual report's officers table concurs"))

# ----------------------------------------------------------------
# City of South Burlington (Chittenden County) -- charter ch. 13.
SBURL_R26_C = ("City of South Burlington, official results of the "
               "March 3, 2026 Annual City Election, published by "
               "the City Clerk")
SBURL_R24_C = ("City of South Burlington, official results of the "
               "March 2024 Town Meeting Day election, published by "
               "the City Clerk")
SPECS["south-burlington"] = spec(
    "south-burlington", "City of South Burlington", [
    office("moderator", "City Moderator",
           "City of South Burlington City Moderator", 1,
           [charter013("sec. 301: the officers provided by law for "
                       "towns are elected except those the charter "
                       "makes appointive; the Moderator remains "
                       "elective"),
            S(SBURL_RESULTS26, f"{SBURL_R26_C}: the city's "
                               "published results never list the "
                               "moderator office and no holder is "
                               "published, so the post stands "
                               "without a membership")]),
    office("city-clerk", "City Clerk",
           "City of South Burlington City Clerk", 1,
           [charter013("sec. 301(2): the City Clerk is not among "
                       "the officers the Council appoints, and "
                       "remains elective"),
            S(SBURL_RESULTS24, f"{SBURL_R24_C}: Holly B. Rees won "
                               "the City Clerk election for a "
                               "three-year term with 4,084 votes"),
            guide("lists Holly Rees as South Burlington's City "
                  "Clerk")],
           [holder("Holly B. Rees", "holly-b-rees")]),
    office("city-treasurer", "City Treasurer",
           "City of South Burlington City Treasurer", 1,
           [charter013("sec. 301(2): the City Council appoints "
                       "annually a City Treasurer, 'whose office "
                       "shall be no longer elective'"),
            guide("lists Martha Machar as South Burlington's "
                  "City Treasurer")],
           [holder("Martha Machar", "martha-machar",
                   how_seated="appointed")]),
    office("city-councilor", "City Councilor",
           "City of South Burlington City Council", 5,
           [charter013("sec. 302: the City Council consists of "
                       "five members elected at large"),
            sb_dir("lists South Burlington's five city councilors: "
                   "Tim Barritt (Chair), Andrew Chalnick (Vice "
                   "Chair), Elizabeth Fitzgerald, Laurie Smith, "
                   "and Beth Zigmund"),
            S(SBURL_RESULTS26, f"{SBURL_R26_C}: Andrew Chalnick "
                               "was re-elected to a three-year "
                               "term (2,826 votes) and Beth "
                               "Zigmund to a two-year term (1,699, "
                               "over Amy Allen, 1,668)")],
           [holder("Tim Barritt", "tim-barritt"),
            holder("Andrew Chalnick", "andrew-chalnick"),
            holder("Elizabeth Fitzgerald", "elizabeth-fitzgerald"),
            holder("Laurie Smith", "laurie-smith"),
            holder("Beth Zigmund", "beth-zigmund")]),
    office("champlain-water-district-representative",
           "Champlain Water District Representative",
           "Champlain Water District", 1,
           [S(SBURL_RESULTS26, f"{SBURL_R26_C}: Dennis Lutz was "
                               "elected 'Water Commissioner for "
                               "3 Years' with 2,929 votes -- "
                               "South Burlington's elected "
                               "representative to the Champlain "
                               "Water District (the post title "
                               "follows the Milton precedent; the "
                               "ballot's styling is recorded "
                               "here)")],
           [holder("Dennis Lutz", "dennis-lutz")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "City of South Burlington Justices of the Peace", 15,
           [jp_src("lists fifteen South Burlington justices of "
                   "the peace: Linda Bailey, T.J. Donovan, Meaghan "
                   "Emery, Donna Kinville, Jason Kirchick, Christy "
                   "Liddy, Maurice Mahoney, Jennifer Oakes, Ann "
                   "Pugh, Helen Riehle, Chris A. Shaw, Michel St. "
                   "Germain, Christi Surmont, Lynn Vera, and "
                   "Matthew Vigneau")],
           [holder("Linda Bailey", "linda-bailey"),
            holder("T.J. Donovan", "tj-donovan"),
            holder("Meaghan Emery", "meaghan-emery"),
            holder("Donna Kinville", "donna-kinville"),
            holder("Jason Kirchick", "jason-kirchick"),
            holder("Christy Liddy", "christy-liddy"),
            holder("Maurice Mahoney", "maurice-mahoney"),
            holder("Jennifer Oakes", "jennifer-oakes"),
            holder("Ann Pugh", "ann-pugh"),
            holder("Helen Riehle", "helen-riehle"),
            holder("Chris A. Shaw", "chris-a-shaw"),
            holder("Michel St. Germain", "michel-st-germain"),
            holder("Christi Surmont", "christi-surmont"),
            holder("Lynn Vera", "lynn-vera"),
            holder("Matthew Vigneau", "matthew-vigneau")]),
], jp=jp_election("south-burlington-vt", "City of South Burlington",
                  15,
                  "the certified listing names fifteen winners for "
                  "South Burlington's fifteen justice of the peace "
                  "seats"))

# ----------------------------------------------------------------
# Town of South Hero (Grand Isle County) -- charter ch. 148.
SH_R26_C = ("Town of South Hero, Official Return of Votes, March "
            "3, 2026 annual meeting (526 voters; certified by Town "
            "Clerk Naomi S. King), published on the town website "
            "southherovt.org")
SH_R25_C = ("Town of South Hero, Official Return of Votes, March "
            "4, 2025 annual meeting (688 voters; certified by Town "
            "Clerk Naomi King)")
SPECS["south-hero"] = spec("south-hero", "Town of South Hero", [
    office("moderator", "Town Moderator",
           "Town of South Hero Town Moderator", 1,
           [charter148("sec. 2: the elected officers are those "
                       "required by State law, elected by "
                       "Australian ballot"),
            S(SH_RETURN26, f"{SH_R26_C}: the 2026 moderator "
                           "contest had no ballot candidate; the "
                           "write-in plurality (Rich Goggin, 125) "
                           "does not seat -- the incumbent, "
                           "Timothy Maxham, had won as a ballot "
                           "candidate in 2025 and drew only 15 "
                           "write-ins -- so the post stands "
                           "without a membership (flagged on "
                           "issue #163)")]),
    office("town-clerk", "Town Clerk",
           "Town of South Hero Town Clerk", 1,
           [charter148("sec. 2: the Town Clerk is elected as "
                       "required by State law"),
            S(SH_RETURN26, f"{SH_R26_C}: Naomi S. King certifies "
                           "the return as Town Clerk; she also "
                           "certified the 2025 return"),
            guide("lists Naomi King as South Hero's Town Clerk")],
           [holder("Naomi King", "naomi-king")]),
    office("town-treasurer", "Town Treasurer",
           "Town of South Hero Town Treasurer", 1,
           [S(SH_RETURN25, f"{SH_R25_C}: the voters authorized the "
                           "Selectboard to appoint a Treasurer as "
                           "provided in 17 V.S.A. section 2651f "
                           "(YES 578, NO 83)"),
            guide("lists Kim T. Julow as South Hero's Town "
                  "Treasurer -- she continues in the office as "
                  "the appointee after the conversion vote "
                  "(disclosed on issue #163)")],
           [holder("Kim T. Julow", "kim-t-julow",
                   how_seated="appointed")]),
    office("selectboard", "Selectboard Member",
           "Town of South Hero Selectboard", 5,
           [S(SH_SITE, "Town of South Hero, Selectboard page "
                       "(southherovt.org): the five members are "
                       "David Carter, David Lane, Graham Brown, "
                       "Steve Robinson, and Anne Zolotas"),
            S(SH_RETURN26, f"{SH_R26_C}: David C. Carter was "
                           "re-elected to a three-year term "
                           "(315 votes, over Joan Falcao, 184) "
                           "and Steven Robinson elected to a "
                           "two-year term (381, over Leo Wermer, "
                           "111)"),
            S(SH_RETURN25, f"{SH_R25_C}: Graham 'Skip' Brown won "
                           "the three-year selectboard seat in "
                           "2025")],
           [holder("David Carter", "david-carter"),
            holder("Steven Robinson", "steven-robinson"),
            holder("Graham Brown", "graham-brown",
                   ballot_name="Graham 'Skip' Brown"),
            holder("David Lane", "david-lane"),
            holder("Anne Zolotas", "anne-zolotas")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of South Hero Cemetery Commission", 3,
           [S(SH_RETURN25, f"{SH_R25_C}: James G. Robinson was "
                           "elected Cemetery Commissioner for "
                           "three years with 635 votes"),
            S(SH_RETURN26, f"{SH_R26_C}: Samuel Robinson was "
                           "elected Cemetery Commissioner for "
                           "three years with 483 votes. One seat "
                           "is filled each year on three-year "
                           "terms, fixing the commission at three "
                           "seats; the third seat's holder is "
                           "published nowhere")],
           [holder("James G. Robinson", "james-g-robinson"),
            holder("Samuel Robinson", "samuel-robinson")]),
    office("library-trustee", "Library Trustee",
           "Town of South Hero Library Trustees", 5,
           [S(SH_RETURN25, f"{SH_R25_C}: Gabrielle Ramseyer was "
                           "elected to a one-year library term "
                           "(586 votes) and Ken Kowalewitz to a "
                           "two-year term -- remainder terms on "
                           "the staggered board"),
            S(SH_RETURN26, f"{SH_R26_C}: Gabrielle Ramseyer was "
                           "re-elected (454 votes), Kristen "
                           "Bartle elected to a two-year term "
                           "(462), and Elisabeth Wirsing elected "
                           "on write-ins the return itself names "
                           "(470 of 473 write-in votes) -- a "
                           "write-in winner named in the "
                           "certified tally is a certified "
                           "outcome (disclosed on issue #163). "
                           "The fifth trustee seat's holder is "
                           "published nowhere")],
           [holder("Gabrielle Ramseyer", "gabrielle-ramseyer"),
            holder("Ken Kowalewitz", "ken-kowalewitz"),
            holder("Kristen Bartle", "kristen-bartle"),
            holder("Elisabeth Wirsing", "elisabeth-wirsing")]),
    office("constable", "Constable",
           "Town of South Hero Constable", 1,
           [charter148("sec. 2 keeps the State-law elected "
                       "officers"),
            statute2646_structure("towns elect a constable; the "
                                  "office appears on neither the "
                                  "2025 nor the 2026 South Hero "
                                  "ballot and no holder is "
                                  "published")]),
    office("grand-juror", "Grand Juror",
           "Town of South Hero Grand Juror", 1,
           [statute2646_structure("towns elect a grand juror")]),
    office("town-agent", "Town Agent",
           "Town of South Hero Town Agent", 1,
           [statute2646_structure("towns elect a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of South Hero Justices of the Peace", 7,
           [jp_src("lists seven South Hero justices of the peace: "
                   "Karen Browning, David Carter, Emily Lee, "
                   "Christine Mack, Carol Tremble, Kevin Winch, "
                   "and Mary Jane Wirsing")],
           [holder("Karen Browning", "karen-browning"),
            holder("David Carter", "david-carter"),
            holder("Emily Lee", "emily-lee"),
            holder("Christine Mack", "christine-mack"),
            holder("Carol Tremble", "carol-tremble"),
            holder("Kevin Winch", "kevin-winch"),
            holder("Mary Jane Wirsing", "mary-jane-wirsing")]),
], jp=jp_election("south-hero-vt", "Town of South Hero", 7,
                  "the certified listing names seven winners for "
                  "South Hero's seven justice of the peace seats. "
                  "Note: ch. 148 sec. 3 makes the town's three "
                  "listers and its delinquent tax collector "
                  "Selectboard-appointed and sec. 4 makes the "
                  "auditor appointed, so no posts are created for "
                  "those offices; the town nevertheless balloted "
                  "lister seats in 2025 and 2026, and those ballot "
                  "winners are not recorded because the charter "
                  "controls (flagged on issue #163)",
                  extra_sources=[charter148("sec. 3: the "
                                   "Selectboard appoints the "
                                   "delinquent tax collector and "
                                   "three town listers; sec. 4: "
                                   "the Selectboard appoints the "
                                   "town auditor annually")]))

# ----------------------------------------------------------------
# Town of Springfield (Windsor County) -- charter ch. 149.
SPR_RET_C = ("Town of Springfield, Australian Ballot Official "
             "Return of Votes, Annual Town Meeting, March 3, 2026 "
             "(1,357 ballots of 6,562 registered voters; certified "
             "by Town Clerk Barbara A. Courchesne and Assistant "
             "Town Clerk Carrie M. Kellow)")
SPR_REP_C = ("Town of Springfield, 2025 Annual Report (FY2025), "
             "'ELECTED MUNICIPAL OFFICERS' and 'APPOINTED "
             "MUNICIPAL OFFICERS' lists, p. 5")
SPECS["springfield"] = spec("springfield", "Town of Springfield", [
    office("moderator", "Town Moderator",
           "Town of Springfield Town Moderator", 1,
           [charter149("sec. 23(a): the Moderator is an elective "
                       "office"),
            S(SPR_RETURN, f"{SPR_RET_C}: John Brady was "
                          "re-elected Town Moderator with 1,148 "
                          "votes")],
           [holder("John Brady", "john-brady")]),
    office("town-clerk", "Town Clerk",
           "Town of Springfield Town Clerk", 1,
           [charter149("sec. 24(b)(1): the Town Clerk is appointed "
                       "by the Selectboard"),
            S(SPR_REPORT, f"{SPR_REP_C}: the appointed officers "
                          "list names Barbara A. Courchesne as "
                          "Town Clerk/Treasurer"),
            guide("lists Barbara Courchesne as Springfield's "
                  "Town Clerk")],
           [holder("Barbara A. Courchesne", "barbara-a-courchesne",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Springfield Town Treasurer", 1,
           [charter149("sec. 24(b)(1): the Town Treasurer is "
                       "appointed by the Selectboard"),
            guide("lists Barbara Courchesne as Springfield's "
                  "Town Treasurer")],
           [holder("Barbara A. Courchesne", "barbara-a-courchesne",
                   how_seated="appointed")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Springfield Collector of Delinquent Taxes", 1,
           [charter149("sec. 24(b)(1): the Delinquent Tax "
                       "Collector is appointed by the Selectboard"),
            S(SPR_SITE, "Town of Springfield, Town Clerk page "
                        "(springfieldvt.gov): 'Delinquent Tax "
                        "Collector: Barbara A. Courchesne'")],
           [holder("Barbara A. Courchesne", "barbara-a-courchesne",
                   how_seated="appointed")]),
    office("selectboard", "Selectboard Member",
           "Town of Springfield Selectboard", 5,
           [charter149("sec. 23(a): the Selectboard's five members "
                       "are elected to staggered three-year terms"),
            sb_dir("lists Springfield's five selectboard members: "
                   "Tara Chase, Heather Frahm (Vice Chair), "
                   "Douglas Johnston, Kristi Morris (Chair), and "
                   "Michael Schmitt"),
            S(SPR_RETURN, f"{SPR_RET_C}: Kristi C. Morris (813 "
                          "votes) and Douglas Johnston (705) won "
                          "the two three-year seats over Bryan "
                          "Stascavage (451); Michael E. Martin's "
                          "term expired and he did not return")],
           [holder("Kristi C. Morris", "kristi-c-morris",
                   existing_person_id="ocd-person/84e1d009-a245-5fc2-b1a9-efe282efe309"),
            holder("Heather Frahm", "heather-frahm"),
            holder("Tara Chase", "tara-chase"),
            holder("Michael Schmitt", "michael-schmitt"),
            holder("Douglas Johnston", "douglas-johnston")]),
    office("library-trustee", "Library Trustee",
           "Town of Springfield Library Trustees", 7,
           [charter149("sec. 23(a): Library Trustees are an "
                       "elective office"),
            S(SPR_SITE, "Town of Springfield, Library Trustees "
                        "page (current): pattrice jones (Chair; "
                        "elected March 4, 2025, term to 2028), "
                        "Christine Boardman and Suzette Chivers "
                        "(elected 2024, terms to 2027), and Geetu "
                        "Melwani 'Appointed for 1 year term out of "
                        "a 3 year term' (March 2026 to March "
                        "2027). The report shows Melwani was "
                        "first appointed in 2025 after a "
                        "resignation"),
            S(SPR_RETURN, f"{SPR_RET_C}: Sharon Ayer (963 votes) "
                          "and Chris Goding (946) won three-year "
                          "library terms, and Britton Herring "
                          "(1,070) won a two-year remainder term. "
                          "The trustees page styles Goding 'L. "
                          "Chris Goding'; the certified return's "
                          "form governs the recorded name")],
           [holder("Pattrice Jones", "pattrice-jones"),
            holder("Sharon Ayer", "sharon-ayer"),
            holder("Chris Goding", "chris-goding"),
            holder("Christine Boardman", "christine-boardman"),
            holder("Suzette Chivers", "suzette-chivers"),
            holder("Britton Herring", "britton-herring"),
            holder("Geetu Melwani", "geetu-melwani",
                   how_seated="appointed")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Springfield Trustees of Public Funds", 3,
           [charter149("sec. 23(a): Trustees of Public Funds are "
                       "an elective office"),
            S(SPR_SITE, "Town of Springfield, Trustees of Public "
                        "Funds page (current): Marc Aube (elected "
                        "March 5, 2024, term to 2027) and Peter "
                        "Andrews (elected March 4, 2025, term to "
                        "2028)"),
            S(SPR_RETURN, f"{SPR_RET_C}: the three-year trustee "
                          "contest had no ballot candidate; Sue "
                          "Phelps was the highest write-in with 68 "
                          "votes, and the town's trustees page "
                          "records her as 'Elected: 3/5/2026, "
                          "Term Expires: 2029' -- a write-in "
                          "winner named in the certified tally "
                          "with roster concurrence, recorded as "
                          "elected (disclosed on issue #163)")],
           [holder("Marc Aube", "marc-aube"),
            holder("Peter Andrews", "peter-andrews"),
            holder("Susan Phelps", "susan-phelps")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Springfield Cemetery Commission", 5,
           [charter149("sec. 23(a): Cemetery Commissioners are an "
                       "elective office"),
            S(SPR_SITE, "Town of Springfield, Cemetery Commission "
                        "page (current): Scott Page (Chair, term "
                        "to 2027), Cathryn Feickert (to 2028), "
                        "Ronald Griffin (to 2029), Judith Stern "
                        "(to 2030); Barbara A. Courchesne sits ex "
                        "officio and is not a member"),
            S(SPR_RETURN, f"{SPR_RET_C}: Beth Gray was "
                          "re-elected Cemetery Commissioner for "
                          "five years with 1,102 votes (term to "
                          "2031). The commission page's 'Beth "
                          "Gray' is the justices listing's "
                          "'Elizabeth Gray' -- one person, "
                          "recorded under the listing's form")],
           [holder("Scott Page", "scott-page"),
            holder("Cathryn Feickert", "cathryn-feickert"),
            holder("Ronald Griffin", "ronald-griffin"),
            holder("Judith Stern", "judith-stern"),
            holder("Elizabeth Gray", "elizabeth-gray")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Springfield Justices of the Peace", 15,
           [jp_src("lists fifteen Springfield justices of the "
                   "peace: Ernest Lamphere, Alice Emmons, Ted "
                   "Cody, Judith Stern, Steve Matush, Lisa Young, "
                   "Michael Jasinski, James Fog, Scott Farr, "
                   "Timothy Gagnier, Asa Baptie Jr, Warren Cross, "
                   "Julia Buffum, Elizabeth Gray, and Randy Gray")],
           [holder("Ernest Lamphere", "ernest-lamphere"),
            holder("Alice M. Emmons", "alice-m-emmons",
                   existing_person_id="ocd-person/03b80132-73dd-5092-ac62-3d240998978d"),
            holder("Ted Cody", "ted-cody"),
            holder("Judith Stern", "judith-stern"),
            holder("Steve Matush", "steve-matush"),
            holder("Lisa Young", "lisa-young"),
            holder("Michael Jasinski", "michael-jasinski"),
            holder("James Fog", "james-fog"),
            holder("Scott Farr", "scott-farr"),
            holder("Timothy Gagnier", "timothy-gagnier"),
            holder("Asa Baptie Jr.", "asa-baptie-jr"),
            holder("Warren Cross", "warren-cross"),
            holder("Julia Buffum", "julia-buffum"),
            holder("Elizabeth Gray", "elizabeth-gray"),
            holder("Randy Gray", "randy-gray")]),
], jp=jp_election("springfield-vt", "Town of Springfield", 15,
                  "the certified listing names fifteen winners for "
                  "Springfield's fifteen justice of the peace "
                  "seats"))

ORDER = ["shaftsbury", "sharon", "sheffield", "shelburne",
         "sheldon", "shoreham", "shrewsbury", "south-burlington",
         "south-hero", "springfield"]

for slug in ORDER:
    (OUT / f"{slug}.json").write_text(
        json.dumps(SPECS[slug], indent=1) + "\n")
print("wrote", len(ORDER), "specs")
