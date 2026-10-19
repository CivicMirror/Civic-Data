#!/usr/bin/env python3
"""Batch 20 of the VT #163 municipal fan-out (alphabetical positions
190-199): Roxbury, Royalton, Rupert, Rutland Town (rutland-61300),
Rutland City (rutland), Ryegate, Salisbury, Sandgate, Saxtons River
Village, Searsburg. Emits one JSON spec per municipality for
build_vt_municipality.py. Research: vt_muni_batch20_research.md.

Identity calls baked into this batch (all flagged on #163):
- Rutland Town JP Christopher K. Howland is the sitting State
  Representative for Rutland-4 (the district includes Rutland
  Town): his JP holder entry reuses the state-tier person record
  ocd-person/72aeb83f-ecbe-5078-9559-e6497ad30543, and his JP
  candidacy is appended to that record by hand after the build.
- Ryegate Selectboard member Andrew Smith is a NEW person,
  distinct from the Town of Berkshire's Andrew Smith (batch 3).
- Salisbury JP Jeff McDonough is a NEW person, distinct from the
  Town of Leicester's Jeff McDonough (batch 13, First Constable):
  both offices require residence in their own town.
- Salisbury has NO state-tier record for Jonathan Blake: the
  volunteers page's 'State Rep' styling is historical (the
  certified 2024 legislative build seats Olson and Lueders in
  Addison-4); Blake is minted new here.
- Searsburg's Chris Reynolds and Christopher Reynolds are minted
  as TWO people: the SOS directory and the factory both list
  them as separate selectboard rows with different addresses and
  emails. Flagged on #163 in case the directory duplicated one
  man.
- Salisbury Town Clerk Fred Kenney is minted APPOINTED on a
  disclosed inference: Allen Hathaway held the office through
  June 2026 (Guide, SOS clerk spreadsheet, and the archived
  town clerk page concur), but the town's live clerk page now
  names Kenney -- a post-June succession, i.e. a selectboard
  vacancy appointment (Plainfield/Readsboro pattern).
- Rutland City aldermen Barry Beauchamp and Curt Esposito hold
  APPOINTED memberships: neither won in the certified 2025 or
  2026 results, and the city's roster seats both in the 2025
  class -- vacancy appointees under ch. 9 sec. 15.7(a).
- Rutland City Mayor Thomas Donahue's 2026 win was for a
  ONE-YEAR term, the remainder of the term Mike Doenges won in
  2025; Doenges is not minted.
- Royalton's Tim Parker II is APPOINTED to the Selectboard (the
  SOS directory styles him 'Selectboard-Appointment through
  March 2027'); Royalton's Treasurer Rita Hull (ch. 145) and
  Salisbury's Treasurer Kerry Dashnaw (ch. 146 sec. 1) are
  APPOINTED.
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
CHARTER_009 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/009",
    "note": "PLACEHOLDER",
}
CHARTER_145 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/145",
    "note": "PLACEHOLDER",
}
CHARTER_146 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/146",
    "note": "PLACEHOLDER",
}
VSARA_VILLAGES = {
    "url": "https://sos.vermont.gov/vsara/learn/municipalities/incorporated-villages",
    "note": "PLACEHOLDER",
}
ROX_RESULTS = {"url": "https://roxburyvt.gov/wp-content/uploads/2026/03/town-ballot-results.pdf",
               "note": "PLACEHOLDER"}
ROX_SITE = {"url": "https://roxburyvt.gov",
            "note": "PLACEHOLDER"}
RYL_RETURN = {"url": "https://royaltonvt.gov/Australian%20Ballot%20Official%20Return%20Of%20Votes%20(3).pdf",
              "note": "PLACEHOLDER"}
RYL_SITE = {"url": "https://royaltonvt.gov",
            "note": "PLACEHOLDER"}
RUP_CERT = {"url": "https://rupert.vt.gov/wp-content/uploads/2026/03/Certificate-of-Election-3-3-2026.pdf",
            "note": "PLACEHOLDER"}
RUP_SITE = {"url": "https://rupert.vt.gov",
            "note": "PLACEHOLDER"}
RT_OFFICIALS = {"url": "https://www.rutlandtown.com/town-departments/elected-and-appointed-officials/",
                "note": "PLACEHOLDER"}
RT_DTC = {"url": "https://www.rutlandtown.com/town-departments/collector-of-delinquent-taxes/",
          "note": "PLACEHOLDER"}
RT_SITE = {"url": "https://www.rutlandtown.com",
           "note": "PLACEHOLDER"}
RC_RESULTS_2026 = {"url": "https://rutlandcity.org/wp-content/uploads/2026/03/Election-Results-March-3-2026-1.xlsx",
                   "note": "PLACEHOLDER"}
RC_RESULTS_2025 = {"url": "https://rutlandcity.org/wp-content/uploads/2025/03/Election-Results-March-4-2025.pdf",
                   "note": "PLACEHOLDER"}
RC_SITE = {"url": "https://rutlandcity.org",
           "note": "PLACEHOLDER"}
RYG_SB = {"url": "https://www.ryegatevt.org/board-of-selectmen",
          "note": "PLACEHOLDER"}
RYG_CLERK = {"url": "https://www.ryegatevt.org/town-clerk",
             "note": "PLACEHOLDER"}
RYG_CEM = {"url": "https://www.ryegatevt.org/cemetery-commission",
           "note": "PLACEHOLDER"}
RYG_LIB = {"url": "https://www.ryegatevt.org/library-trustees",
           "note": "PLACEHOLDER"}
RYG_SITE = {"url": "https://www.ryegatevt.org",
            "note": "PLACEHOLDER"}
SAL_WARN = {"url": "https://www.townofsalisbury.org/vertical/sites/%7B59D8C83C-9968-4A65-BB2B-00DE19899066%7D/uploads/2026_Warning.Town_Meeting.Final(1).pdf",
            "note": "PLACEHOLDER"}
SAL_CLERK = {"url": "https://www.townofsalisbury.org/clerk",
             "note": "PLACEHOLDER"}
SAL_SITE = {"url": "https://www.townofsalisbury.org",
            "note": "PLACEHOLDER"}
SAN_ELECTED = {"url": "https://sandgatevermont.org/elected_officers/",
               "note": "PLACEHOLDER"}
SR_TRUSTEES = {"url": "https://www.rockinghamvt.org/saxtonsrivertrustees",
               "note": "PLACEHOLDER"}
SR_WARNING = {"url": "https://www.fact8.com/on-fact-tv/government-programming/saxtons-river-select-board/saxtons-river-village-trustees-annual-meeting-april-13th-2026-live-700pm/",
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


def charter009(phrase):
    return S(CHARTER_009, f"24 App. V.S.A. ch. 9 (City of Rutland): "
             f"{phrase}")


def charter145(phrase):
    return S(CHARTER_145, f"24 App. V.S.A. ch. 145 (Town of "
             f"Royalton): {phrase}")


def charter146(phrase):
    return S(CHARTER_146, f"24 App. V.S.A. ch. 146 (Town of "
             f"Salisbury): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 20); issue #163 "
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
                  f"# municipal fan-out batch 20; issue #163 "
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
# Town of Roxbury (Washington County) -- general law.
ROX_CERT_C = ("Town of Roxbury, Certificate of Election, Town "
              "Officers, March 3, 2026 (attested by Town Clerk "
              "Tammy Legacy, March 4, 2026)")
ROX_REPORT_C = ("Town of Roxbury, 2024 Annual Report, town "
                "officers table (terms with expiry years)")
SPECS["roxbury"] = spec("roxbury", "Town of Roxbury", [
    office("moderator", "Town Moderator",
           "Town of Roxbury Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(ROX_RESULTS, f"{ROX_CERT_C}: Jacqueline Frazier was "
                           "elected Moderator with 161 votes")],
           [holder("Jacqueline Frazier", "jacqueline-frazier")]),
    office("town-clerk", "Town Clerk",
           "Town of Roxbury Town Clerk", 1,
           [statute2646("towns elect a town clerk; Roxbury elects "
                        "its clerk to a one-year term"),
            S(ROX_RESULTS, f"{ROX_CERT_C}: Tammy Legacy was "
                           "elected Town Clerk with 163 votes"),
            guide("lists Tammy Legacy as Roxbury's Town Clerk")],
           [holder("Tammy Legacy", "tammy-legacy")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Roxbury Town Treasurer", 1,
           [statute2646("towns elect a town treasurer; Roxbury "
                        "elects its treasurer to a one-year term"),
            S(ROX_RESULTS, f"{ROX_CERT_C}: Anne Maxham was "
                           "elected Town Treasurer with 171 votes"),
            guide("lists Anne Maxham as Roxbury's Town Treasurer")],
           [holder("Anne Maxham", "anne-maxham")]),
    office("selectboard", "Selectboard Member",
           "Town of Roxbury Selectboard", 5,
           [sb_dir("lists Roxbury's five selectboard members: "
                   "Jeremy Reed (Chair), Donna French (Vice "
                   "Chair), Nathan Donahue, Heather Holter, and "
                   "Timothy Martin"),
            S(ROX_RESULTS, f"{ROX_CERT_C}: Heather Holter won the "
                           "three-year selectboard seat (160 "
                           "votes) and Timothy Martin the two-year "
                           "seat (113 votes) at the March 3, 2026 "
                           "election")],
           [holder("Jeremy Reed", "jeremy-reed"),
            holder("Donna French", "donna-french"),
            holder("Nathan Donahue", "nathan-donahue"),
            holder("Heather Holter", "heather-holter"),
            holder("Timothy Martin", "timothy-martin")]),
    office("lister", "Lister",
           "Town of Roxbury Board of Listers", 3,
           [statute2646("towns elect a board of listers of three"),
            S(ROX_RESULTS, f"{ROX_CERT_C}: William Hansen won the "
                           "three-year lister seat (164 votes) and "
                           "Thomas L. Frazier the two-year "
                           "remainder (146 votes)"),
            S(ROX_SITE, f"{ROX_REPORT_C}: Robert Ketchel's lister "
                        "term runs to 2027")],
           [holder("William Hansen", "william-hansen"),
            holder("Thomas L. Frazier", "thomas-l-frazier"),
            holder("Robert Ketchel", "robert-ketchel")]),
    office("auditor", "Auditor",
           "Town of Roxbury Auditors", 3,
           [statute2646("towns elect auditors (three, staggered "
                        "terms) unless the office is eliminated"),
            S(ROX_RESULTS, f"{ROX_CERT_C}: Karen Tassinari won "
                           "the two-year auditor seat (153 "
                           "votes); the three-year and one-year "
                           "auditor seats both returned 'No one "
                           "received enough votes', so one of "
                           "Roxbury's three auditor seats stands "
                           "vacant"),
            S(ROX_SITE, f"{ROX_REPORT_C}: Jillian Abraham (Chair) "
                        "holds an auditor term to 2027")],
           [holder("Jillian Abraham", "jillian-abraham"),
            holder("Karen Tassinari", "karen-tassinari")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Roxbury Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes for a one-year term unless the "
                        "town votes a longer term"),
            S(ROX_RESULTS, f"{ROX_CERT_C}: William Hansen was "
                           "elected Collector of Delinquent Taxes "
                           "with 166 votes")],
           [holder("William Hansen", "william-hansen")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Roxbury Cemetery Commission", 3,
           [S(ROX_RESULTS, f"{ROX_CERT_C}: William Cecil won the "
                           "three-year cemetery commissioner seat "
                           "(166 votes)"),
            S(ROX_SITE, f"{ROX_REPORT_C}: Wendy Cashman's "
                        "cemetery commissioner term runs to 2027. "
                        "The third seat, whose term stood in 2025, "
                        "has no published outcome, so it is left "
                        "unfilled")],
           [holder("Wendy Cashman", "wendy-cashman"),
            holder("William Cecil", "william-cecil")]),
    office("first-constable", "First Constable",
           "Town of Roxbury First Constable", 1,
           [statute2646("towns elect a first constable"),
            S(ROX_RESULTS, f"{ROX_CERT_C}: William Hansen was "
                           "elected First Constable with 164 "
                           "votes")],
           [holder("William Hansen", "william-hansen")]),
    office("second-constable", "Second Constable",
           "Town of Roxbury Second Constable", 1,
           [statute2646("towns may elect a second constable"),
            S(ROX_RESULTS, f"{ROX_CERT_C}: Andrew Apgar was "
                           "elected Second Constable with 156 "
                           "votes")],
           [holder("Andrew Apgar", "andrew-apgar")]),
    office("library-trustee", "Library Trustee",
           "Town of Roxbury Library Trustees", 5,
           [S(ROX_RESULTS, f"{ROX_CERT_C}: Heidi Albright was "
                           "re-elected a library trustee (165 "
                           "votes); the other two 2026 trustee "
                           "seats returned 'No one received enough "
                           "votes'"),
            S(ROX_SITE, f"{ROX_REPORT_C}: Carl Ellis's library "
                        "trustee term runs to 2027. A third seat "
                        "filled in 2025 has no published holder, "
                        "so three of the five seats are left "
                        "unfilled")],
           [holder("Carl Ellis", "carl-ellis"),
            holder("Heidi Albright", "heidi-albright")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Roxbury Justices of the Peace", 5,
           [jp_src("lists five Roxbury justices of the peace: Amy "
                   "Barrett, Gerald D'Amico, William Hansen, Sarah "
                   "Kirn, and Susan Nevins")],
           [holder("Amy Barrett", "amy-barrett"),
            holder("Gerald D'Amico", "gerald-damico"),
            holder("William Hansen", "william-hansen"),
            holder("Sarah Kirn", "sarah-kirn"),
            holder("Susan Nevins", "susan-nevins")]),
], jp=jp_election("roxbury-vt", "Town of Roxbury", 5,
                  "the certified listing names five winners for "
                  "Roxbury's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Royalton (Windsor County) -- ch. 145 (treasurer
# appointed); all else general law.
RYL_RETURN_C = ("Town of Royalton, Official Return of Votes, "
                "March 3, 2026 town meeting (certified by the "
                "Town Clerk; 390 ballots cast)")
RYL_REPORT_C = ("Town of Royalton, 2025 Town Report, Elected Town "
                "Officers and Appointed Officers tables")
SPECS["royalton"] = spec("royalton", "Town of Royalton", [
    office("moderator", "Town Moderator",
           "Town of Royalton Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(RYL_RETURN, f"{RYL_RETURN_C}: Allison N. Fulcher "
                          "was elected Moderator with 362 votes")],
           [holder("Allison Fulcher", "allison-fulcher")]),
    office("town-clerk", "Town Clerk",
           "Town of Royalton Town Clerk", 1,
           [statute2646("towns elect a town clerk; Royalton "
                        "elects its clerk to a three-year term"),
            S(RYL_RETURN, f"{RYL_RETURN_C}: Karmen Bascom was "
                          "elected Town Clerk with 373 votes"),
            guide("lists Karmen Bascom as Royalton's Town Clerk")],
           [holder("Karmen Bascom", "karmen-bascom")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Royalton Town Treasurer", 1,
           [charter145("the Town Treasurer is appointed by the "
                       "Selectboard (term of up to three years, at "
                       "the pleasure of the board); the charter's "
                       "only section"),
            S(RYL_SITE, f"{RYL_REPORT_C}: Rita Hull is listed "
                        "among the town's appointed officers as "
                        "Town Treasurer"),
            guide("lists Rita Hull as Royalton's Town Treasurer")],
           [holder("Rita Hull", "rita-hull", how_seated="appointed")]),
    office("selectboard", "Selectboard Member",
           "Town of Royalton Selectboard", 5,
           [sb_dir("lists Royalton's five selectboard members: "
                   "Kip Bergstrom, Patrick Dakin, Nell Gwin, Tim "
                   "Parker II (styled 'Selectboard-Appointment "
                   "through March 2027'), and Larry Trottier"),
            S(RYL_RETURN, f"{RYL_RETURN_C}: Nell Gwin was "
                          "re-elected to a two-year seat (323 "
                          "votes) and Christopher 'Kip' Bergstrom "
                          "won the three-year seat (198 votes)"),
            S(RYL_SITE, "Town of Royalton, Selectboard minutes of "
                        "March 10, 2026: the board organized with "
                        "Patrick Dakin as Chair and Larry Trottier "
                        "as Vice Chair, with Bergstrom seated. Tim "
                        "Parker II holds the fifth seat by "
                        "appointment (see the directory note); he "
                        "fills the seat Robert A. Gray, Jr. held "
                        "at the March 10 meeting before departing")],
           [holder("Patrick Dakin", "patrick-dakin"),
            holder("Larry Trottier", "larry-trottier"),
            holder("Nell Gwin", "nell-gwin"),
            holder("Christopher Bergstrom", "christopher-bergstrom"),
            holder("Tim Parker II", "tim-parker-ii",
                   how_seated="appointed")]),
    office("lister", "Lister",
           "Town of Royalton Board of Listers", 3,
           [statute2646("towns elect a board of listers of three"),
            S(RYL_RETURN, f"{RYL_RETURN_C}: Walter Hastings was "
                          "re-elected a lister (340 votes); the "
                          "one-year remainder lister seat drew no "
                          "ballot candidate (write-ins 30, blanks "
                          "360), so it is left unfilled"),
            S(RYL_SITE, f"{RYL_REPORT_C}: Jeffrey Barcelow's "
                        "lister term runs to 2028")],
           [holder("Jeffrey Barcelow", "jeffrey-barcelow"),
            holder("Walter Hastings", "walter-hastings")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Royalton Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes for a one-year term unless the "
                        "town votes a longer term"),
            S(RYL_RETURN, f"{RYL_RETURN_C}: Theresa Harrington "
                          "was elected Collector of Delinquent "
                          "Taxes with 357 votes"),
            S(RYL_SITE, "Town of Royalton, Collector of Delinquent "
                        "Taxes page (royaltonvt.gov): Theresa "
                        "Harrington is the Collector of Delinquent "
                        "Taxes")],
           [holder("Theresa Harrington", "theresa-harrington")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Royalton Trustees of Public Funds", 3,
           [statute2646("towns elect trustees of public funds "
                        "where the town holds public funds"),
            S(RYL_RETURN, f"{RYL_RETURN_C}: Donna Bohonnon was "
                          "re-elected a trustee of public funds "
                          "(347 votes) and Jerry Barcelow won the "
                          "two-year remainder seat (359 votes); "
                          "Barcelow had been appointed to the seat "
                          "in 2025"),
            S(RYL_SITE, f"{RYL_REPORT_C}: John P. Dumville's "
                        "trustee of public funds term runs to "
                        "2027")],
           [holder("John Dumville", "john-dumville"),
            holder("Donna Bohonnon", "donna-bohonnon"),
            holder("Jerry Barcelow", "jerry-barcelow")]),
    office("first-constable", "First Constable",
           "Town of Royalton First Constable", 1,
           [statute2646_structure("towns elect a first constable; "
                                  "Royalton elects its constables "
                                  "to two-year terms"),
            S(RYL_RETURN, f"{RYL_RETURN_C}: the two-year first "
                          "constable seat drew no ballot candidate "
                          "(write-ins 67, no winner certified), "
                          "so the post is created without a "
                          "membership")]),
    office("second-constable", "Second Constable",
           "Town of Royalton Second Constable", 1,
           [statute2646("towns may elect a second constable"),
            S(RYL_SITE, f"{RYL_REPORT_C}: Linc Farrington's second "
                        "constable term runs to 2027; the seat "
                        "did not stand in 2026")],
           [holder("Linc Farrington", "linc-farrington")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Royalton Cemetery Commission", 3,
           [S(RYL_RETURN, f"{RYL_RETURN_C}: Heather Leavitt was "
                          "re-elected a cemetery commissioner (350 "
                          "votes)"),
            S(RYL_SITE, "Town of Royalton, Cemetery Commission "
                        "page (royaltonvt.gov): the commissioners "
                        "are Josephine Levasseur (term to 2028), "
                        "Kenneth Alton (to 2027), and Heather "
                        "Leavitt")],
           [holder("Josephine Levasseur", "josephine-levasseur"),
            holder("Kenneth Alton", "kenneth-alton"),
            holder("Heather Leavitt", "heather-leavitt")]),
    office("library-trustee", "Library Trustee",
           "Town of Royalton Library Trustees", 2,
           [S(RYL_RETURN, f"{RYL_RETURN_C}: Steven W. Hall was "
                          "re-elected a library trustee (339 votes) "
                          "to a two-year seat"),
            S(RYL_SITE, f"{RYL_REPORT_C}: the library trustees "
                        "table lists exactly two trustees -- Steven "
                        "W. Hall and Fran Flannery (term to 2027) "
                        "-- with one two-year seat elected each "
                        "year, so the board has two seats")],
           [holder("Steven Hall", "steven-hall"),
            holder("Fran Flannery", "fran-flannery")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Royalton Justices of the Peace", 10,
           [jp_src("lists ten Royalton justices of the peace: Peg "
                   "Ainsworth, Charles Bascom, John Dumville, "
                   "Allison Fulcher, Robert 'Bob' Hull, Suzanne "
                   "Long, Bruce Post, Joshua 'Bushrod' Powers, "
                   "Scott Puopolo, and Larry Trottier")],
           [holder("Peg Ainsworth", "peg-ainsworth"),
            holder("Charles Bascom", "charles-bascom"),
            holder("John Dumville", "john-dumville"),
            holder("Allison Fulcher", "allison-fulcher"),
            holder("Robert Hull", "robert-hull",
                   ballot_name="Robert 'Bob' Hull"),
            holder("Suzanne Long", "suzanne-long"),
            holder("Bruce Post", "bruce-post"),
            holder("Joshua Powers", "joshua-powers",
                   ballot_name="Joshua 'Bushrod' Powers"),
            holder("Scott Puopolo", "scott-puopolo"),
            holder("Larry Trottier", "larry-trottier")]),
], jp=jp_election("royalton-vt", "Town of Royalton", 10,
                  "the certified listing names ten winners for "
                  "Royalton's ten justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Rupert (Bennington County) -- general law.
RUP_CERT_C = ("Town of Rupert, Certificate of Votes, Results of "
              "Town Meeting, March 3, 2026 (196 votes cast; "
              "certified by the Town Clerk)")
RUP_REPORT_C = ("Town of Rupert, 2025 Town Report, 'Rupert Town "
                "Officers' table")
SPECS["rupert"] = spec("rupert", "Town of Rupert", [
    office("moderator", "Town Moderator",
           "Town of Rupert Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(RUP_CERT, f"{RUP_CERT_C}: Mark Lourie was elected "
                        "Moderator with 184 votes")],
           [holder("Mark Lourie", "mark-lourie")]),
    office("town-clerk", "Town Clerk",
           "Town of Rupert Town Clerk", 1,
           [statute2646("towns elect a town clerk; Rupert elects "
                        "its clerk to a three-year term"),
            S(RUP_CERT, f"{RUP_CERT_C}: Andrea Lenhardt was "
                        "elected Town Clerk to a three-year term "
                        "with 188 votes"),
            guide("lists Andrea Lenhardt as Rupert's Town Clerk")],
           [holder("Andrea Lenhardt", "andrea-lenhardt")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Rupert Town Treasurer", 1,
           [statute2646("towns elect a town treasurer; Rupert "
                        "elects its treasurer to a three-year term"),
            S(RUP_CERT, f"{RUP_CERT_C}: Andrea Lenhardt was "
                        "elected Town Treasurer to a three-year "
                        "term with 187 votes"),
            guide("lists Andrea Lenhardt as Rupert's Town "
                  "Treasurer")],
           [holder("Andrea Lenhardt", "andrea-lenhardt")]),
    office("selectboard", "Selectboard Member",
           "Town of Rupert Selectboard", 5,
           [sb_dir("lists only four of Rupert's five selectboard "
                   "members: Kyle Hunter (Chair), Philip Mazzucco, "
                   "Charles Rockwell, and Thomas Wilson"),
            S(RUP_CERT, f"{RUP_CERT_C}: Kyle Hunter won a one-year "
                        "seat (159 votes), Charles Rockwell the "
                        "three-year seat (173), Colin Driscoll the "
                        "two-year seat (94), and Philip E. Mazzucco "
                        "a one-year seat (146)"),
            S(RUP_SITE, f"{RUP_REPORT_C}: Colin Driscoll was "
                        "appointed to the selectboard on October "
                        "14, 2025, after Deborah Baker resigned on "
                        "August 26, 2025, and was then elected to "
                        "the seat's two-year remainder in 2026; "
                        "Thomas Wilson's term runs to 2027")],
           [holder("Kyle Hunter", "kyle-hunter"),
            holder("Charles Rockwell", "charles-rockwell"),
            holder("Colin Driscoll", "colin-driscoll"),
            holder("Philip Mazzucco", "philip-mazzucco"),
            holder("Thomas Wilson", "thomas-wilson")]),
    office("lister", "Lister",
           "Town of Rupert Board of Listers", 3,
           [statute2646("towns elect a board of listers of three"),
            S(RUP_CERT, f"{RUP_CERT_C}: Jed Rubin was re-elected "
                        "a lister with 166 votes"),
            S(RUP_SITE, f"{RUP_REPORT_C}: the listers are Jed "
                        "Rubin (Chair), Carl Yackel (term to "
                        "2027), and Daniel Fuller (term to 2028)")],
           [holder("Jed Rubin", "jed-rubin"),
            holder("Carl Yackel", "carl-yackel"),
            holder("Daniel Fuller", "daniel-fuller")]),
    office("auditor", "Auditor",
           "Town of Rupert Auditors", 3,
           [statute2646("towns elect auditors (three, staggered "
                        "terms) unless the office is eliminated"),
            S(RUP_CERT, f"{RUP_CERT_C}: Kelly Joe Lewis was "
                        "elected an auditor with 183 votes"),
            S(RUP_SITE, f"{RUP_REPORT_C}: the auditors are Kelly "
                        "Joe Lewis, Chris Porter (term to 2027), "
                        "and Jeremy Russo (term to 2028)")],
           [holder("Kelly Joe Lewis", "kelly-joe-lewis"),
            holder("Chris Porter", "chris-porter"),
            holder("Jeremy Russo", "jeremy-russo")]),
    office("first-constable", "First Constable",
           "Town of Rupert First Constable", 1,
           [statute2646("towns elect a first constable"),
            S(RUP_CERT, f"{RUP_CERT_C}: Brett Lourie was elected "
                        "First Constable to a two-year term with "
                        "177 votes")],
           [holder("Brett Lourie", "brett-lourie")]),
    office("second-constable", "Second Constable",
           "Town of Rupert Second Constable", 1,
           [statute2646("towns may elect a second constable"),
            S(RUP_CERT, f"{RUP_CERT_C}: Jay 'Skip' Wilson was "
                        "elected Second Constable to a two-year "
                        "term with 169 votes")],
           [holder("Jay Wilson", "jay-wilson",
                   ballot_name="Jay 'Skip' Wilson")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Rupert Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes for a one-year term unless the "
                        "town votes a longer term"),
            S(RUP_CERT, f"{RUP_CERT_C}: Mark Lourie was elected "
                        "Collector of Delinquent Taxes with 182 "
                        "votes")],
           [holder("Mark Lourie", "mark-lourie")]),
    office("library-trustee", "Library Trustee",
           "Town of Rupert Library Trustees", 7,
           [S(RUP_CERT, f"{RUP_CERT_C}: Wendy McRoy (179 votes) "
                        "and Lynn Vail (182 votes) were elected "
                        "library trustees, taking the two seats "
                        "expiring in 2026"),
            S(RUP_SITE, f"{RUP_REPORT_C}: the Rosalind Keshin "
                        "Kittay Library has seven trustees: Judy "
                        "Zinn, Jean Nardi, and Morgan Horton (terms "
                        "to 2028), Sarah Porter and Anniken "
                        "Davenport (to 2027), and Wendy McRoy and "
                        "Lynn Vail (elected 2026)")],
           [holder("Judy Zinn", "judy-zinn"),
            holder("Jean Nardi", "jean-nardi"),
            holder("Morgan Horton", "morgan-horton"),
            holder("Sarah Porter", "sarah-porter"),
            holder("Anniken Davenport", "anniken-davenport"),
            holder("Wendy McRoy", "wendy-mcroy"),
            holder("Lynn Vail", "lynn-vail")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Rupert Justices of the Peace", 5,
           [jp_src("lists five Rupert justices of the peace: Kate "
                   "Canning, Karen Graf, Mark Lourie, Kelli "
                   "Raymond, and Jeremy Russo")],
           [holder("Kate Canning", "kate-canning"),
            holder("Karen Graf", "karen-graf"),
            holder("Mark Lourie", "mark-lourie"),
            holder("Kelli Raymond", "kelli-raymond"),
            holder("Jeremy Russo", "jeremy-russo")]),
], jp=jp_election("rupert-vt", "Town of Rupert", 5,
                  "the certified listing names five winners for "
                  "Rupert's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Rutland (Rutland County) -- general law. Town roster is
# the authority; no 2026 tally is published.
RT_OFF_C = ("Town of Rutland, 'Elected and Appointed Officials & "
            "Term Information' page (rutlandtown.com), the town's "
            "current roster with term expirations")
RT_WARN_C = ("Town of Rutland, 2026 Warning printed in the FY2025 "
             "Town Report (Article 23, dated January 20, 2026)")
SPECS["rutland-61300"] = spec("rutland-61300", "Town of Rutland", [
    office("moderator", "Town Moderator",
           "Town of Rutland Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(RT_OFFICIALS, f"{RT_OFF_C}: Dan Alcorn is Town "
                            "Moderator, term to March 2027"),
            S(RT_SITE, f"{RT_WARN_C}: the warning elects a "
                       "Moderator for a one-year term")],
           [holder("Dan Alcorn", "dan-alcorn")]),
    office("town-clerk", "Town Clerk",
           "Town of Rutland Town Clerk", 1,
           [statute2646("towns elect a town clerk; Rutland Town "
                        "elects its clerk to a three-year term"),
            S(RT_OFFICIALS, f"{RT_OFF_C}: Kari Clark is Town "
                            "Clerk, her three-year term running "
                            "to March 2029 (the seat stood and was "
                            "won at the March 2026 meeting)"),
            guide("lists Kari Clark as Rutland Town's Town Clerk")],
           [holder("Kari Clark", "kari-clark")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Rutland Town Treasurer", 1,
           [statute2646("towns elect a town treasurer; Rutland "
                        "Town elects its treasurer to a three-year "
                        "term"),
            S(RT_OFFICIALS, f"{RT_OFF_C}: Kari Clark is Town "
                            "Treasurer, her three-year term "
                            "running to March 2029"),
            guide("lists Kari Clark as Rutland Town's Town "
                  "Treasurer")],
           [holder("Kari Clark", "kari-clark")]),
    office("selectboard", "Selectboard Member",
           "Town of Rutland Selectboard", 5,
           [sb_dir("lists Rutland Town's five selectboard members "
                   "under the directory form 'Mary "
                   "Ashcroft-Billings' (Chair), Joseph Denardo, "
                   "Matthew Getty, Kurt Hathaway, and Sharon "
                   "Russell"),
            S(RT_OFFICIALS, f"{RT_OFF_C}: the board is Mary "
                            "Ashcroft (Chair; won the three-year "
                            "seat, term to March 2029), Kurt "
                            "Hathaway (won the two-year seat, to "
                            "March 2028), Joseph Denardo (to March "
                            "2028), Matthew Getty (to March 2027), "
                            "and Sharon Russell (to March 2027). "
                            "The town's own roster and report "
                            "signatures read 'Mary Ashcroft', which "
                            "governs over the directory's fuller "
                            "form")],
           [holder("Mary Ashcroft", "mary-ashcroft"),
            holder("Kurt Hathaway", "kurt-hathaway"),
            holder("Joseph Denardo", "joseph-denardo"),
            holder("Matthew Getty", "matthew-getty"),
            holder("Sharon Russell", "sharon-russell")]),
    office("lister", "Lister",
           "Town of Rutland Board of Listers", 3,
           [statute2646("towns elect a board of listers of three"),
            S(RT_OFFICIALS, f"{RT_OFF_C}: the listers are Marcia "
                            "Chioffi (won the three-year seat, "
                            "term to March 2029), Cathy Kapitanski "
                            "(to March 2028), and Marie Fabian (to "
                            "March 2027)")],
           [holder("Marcia Chioffi", "marcia-chioffi"),
            holder("Cathy Kapitanski", "cathy-kapitanski"),
            holder("Marie Fabian", "marie-fabian")]),
    office("first-constable", "First Constable",
           "Town of Rutland First Constable", 1,
           [statute2646("towns elect a first constable"),
            S(RT_OFFICIALS, f"{RT_OFF_C}: Michael Delehanty is "
                            "First Constable, having won the "
                            "two-year seat (term to March 2028)")],
           [holder("Michael Delehanty", "michael-delehanty")]),
    office("second-constable", "Second Constable",
           "Town of Rutland Second Constable", 1,
           [statute2646("towns may elect a second constable"),
            S(RT_OFFICIALS, f"{RT_OFF_C}: John Paul Faignant is "
                            "Second Constable, term to March 2027; "
                            "the seat did not stand in 2026")],
           [holder("John Paul Faignant", "john-paul-faignant")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Rutland Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes for a one-year term unless the "
                        "town votes a longer term"),
            S(RT_DTC, "Town of Rutland, Collector of Delinquent "
                      "Taxes page (rutlandtown.com): Donald "
                      "'Don' Chioffi holds the office -- 'As an "
                      "elected official answerable to the voters "
                      "of our town'"),
            S(RT_OFFICIALS, f"{RT_OFF_C}: Donald Chioffi's term "
                            "as Collector of Delinquent Taxes "
                            "runs to March 2027")],
           [holder("Donald Chioffi", "donald-chioffi")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Rutland Cemetery Commission", 3,
           [S(RT_OFFICIALS, f"{RT_OFF_C}: the cemetery "
                            "commissioners are Dakota Harvey "
                            "(term to March 2028), Byron 'BJ' "
                            "Hathaway (to March 2027), and Kurt "
                            "Hathaway (to March 2027)")],
           [holder("Dakota Harvey", "dakota-harvey"),
            holder("Byron Hathaway", "byron-hathaway"),
            holder("Kurt Hathaway", "kurt-hathaway")]),
    office("grand-juror", "Grand Juror",
           "Town of Rutland Grand Juror", 1,
           [statute2646("towns elect a grand juror for a one-year "
                        "term"),
            S(RT_OFFICIALS, f"{RT_OFF_C}: Jennifer Roberts is "
                            "Grand Juror, term to March 2027"),
            S(RT_SITE, f"{RT_WARN_C}: the warning elects a Grand "
                       "Juror for a one-year term")],
           [holder("Jennifer Roberts", "jennifer-roberts")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Rutland Justices of the Peace", 12,
           [jp_src("lists twelve Rutland Town justices of the "
                   "peace: Leigh Adams, Howard Burgess, Glen "
                   "Giles, Martin Wasserman, Marc D. Brierre, "
                   "William T. Matteson, Christopher K. Howland, "
                   "James B. Hall, Marcia Chioffi, Donald Chioffi, "
                   "Frederick Nicholson, and Joseph Bertelloni. "
                   "Christopher Howland is also Rutland Town's "
                   "State Representative (Rutland-4); his justice "
                   "of the peace membership reuses his state-tier "
                   "person record")],
           [holder("Leigh Adams", "leigh-adams"),
            holder("Howard Burgess", "howard-burgess"),
            holder("Glen Giles", "glen-giles"),
            holder("Martin Wasserman", "martin-wasserman"),
            holder("Marc D. Brierre", "marc-d-brierre"),
            holder("William T. Matteson", "william-t-matteson"),
            holder("Christopher Howland", "christopher-howland",
                   existing_person_id="ocd-person/72aeb83f-ecbe-5078-9559-e6497ad30543"),
            holder("James B. Hall", "james-b-hall"),
            holder("Marcia Chioffi", "marcia-chioffi"),
            holder("Donald Chioffi", "donald-chioffi"),
            holder("Frederick Nicholson", "frederick-nicholson"),
            holder("Joseph Bertelloni", "joseph-bertelloni")]),
], jp=jp_election("rutland-61300-vt", "Town of Rutland", 12,
                  "the certified listing names twelve winners for "
                  "Rutland Town's twelve justice of the peace "
                  "seats"))

# ----------------------------------------------------------------
# City of Rutland (Rutland County) -- charter ch. 9.
RC_2026_C = ("City of Rutland, official election results for the "
             "March 3, 2026 city election (the clerk's official "
             "totals spreadsheet)")
RC_2025_C = ("City of Rutland, official election results for the "
             "March 4, 2025 city election (the clerk's official "
             "results)")
SPECS["rutland"] = spec("rutland", "City of Rutland", [
    office("mayor", "Mayor",
           "City of Rutland Mayor", 1,
           [charter009("section 2.1(a): the mayor is elected at "
                       "the March election in odd-numbered years "
                       "to a two-year term"),
            S(RC_RESULTS_2026, f"{RC_2026_C}: Thomas Donahue won "
                               "the 2026 mayoral election with "
                               "1,323 votes over David Allaire "
                               "(1,000) and six others. The seat "
                               "was filled for a ONE-YEAR term -- "
                               "the remainder of the two-year term "
                               "Mike Doenges won in March 2025 "
                               "before departing mid-term; Doenges "
                               "is not recorded as a holder"),
            S(RC_RESULTS_2025, f"{RC_2025_C}: Mike Doenges won the "
                               "2025 mayoral election with 2,075 "
                               "votes")],
           [holder("Thomas Donahue", "thomas-donahue")]),
    office("city-treasurer", "City Treasurer",
           "City of Rutland City Treasurer", 1,
           [charter009("section 2.1(a): the City Treasurer is "
                       "elected in odd-numbered years to a "
                       "two-year term; section 10.6 makes the "
                       "Treasurer ex officio Constable and Tax "
                       "Collector, so no separate constable or tax "
                       "collector post is created"),
            S(RC_RESULTS_2025, f"{RC_2025_C}: Mary Markowski was "
                               "elected City Treasurer with 3,198 "
                               "votes"),
            guide("lists Mary Markowski as Rutland City's City "
                  "Treasurer")],
           [holder("Mary Markowski", "mary-markowski")]),
    office("city-assessor", "City Assessor",
           "City of Rutland City Assessor", 1,
           [charter009("section 2.1(a): the City Assessor is "
                       "elected in odd-numbered years to a "
                       "two-year term"),
            S(RC_RESULTS_2025, f"{RC_2025_C}: Katie Burke Langlois "
                               "was elected City Assessor with "
                               "2,913 votes"),
            S(RC_SITE, "City of Rutland, Assessor's Office page "
                       "(rutlandcity.org): Katie Burke Langlois "
                       "is the City Assessor")],
           [holder("Katie Burke Langlois", "katie-burke-langlois")]),
    office("city-clerk", "City Clerk",
           "City of Rutland City Clerk", 1,
           [charter009("section 15.2: the Mayor appoints the City "
                       "Clerk (two-year term, in March of "
                       "odd-numbered years)"),
            guide("lists Tracy Kapusta as Rutland City's City "
                  "Clerk")],
           [holder("Tracy Kapusta", "tracy-kapusta",
                   how_seated="appointed")]),
    office("alderman", "Alderman",
           "City of Rutland Board of Aldermen", 11,
           [charter009("sections 2.1(a)-(b): six aldermen are "
                       "elected in odd-numbered years and five in "
                       "even-numbered years, each to two-year "
                       "terms; section 15.7(a): a vacancy in an "
                       "elective office is filled by mayoral "
                       "appointment until the next annual meeting"),
            S(RC_RESULTS_2025, f"{RC_2025_C}: the 2025 aldermanic "
                               "winners included David Allaire, "
                               "Paul Clifford, Larry Cupoli, Bill "
                               "Gillam, Jr., Thomas Donahue, and "
                               "Kiana McClure"),
            S(RC_RESULTS_2026, f"{RC_2026_C}: the five 2026 "
                               "aldermanic winners were Alex Adams, "
                               "Sharon Davis, Peter Franzoni, Anna "
                               "Tadio, and Michael Talbott"),
            S(RC_SITE, "City of Rutland, Board of Aldermen roster "
                       "(rutlandcity.org): the sitting board is "
                       "David Allaire (President), Paul Clifford, "
                       "Larry Cupoli, and Bill Gillam, Jr. of the "
                       "2025 class (terms to March 2027); Alex "
                       "Adams, Sharon Davis, Peter Franzoni, Anna "
                       "Tadio, and Michael Talbott of the 2026 "
                       "class (to March 2028); and Barry Beauchamp "
                       "and Curt Esposito, seated in the 2025 "
                       "class. Donahue vacated his aldermanic "
                       "seat on winning the mayoralty and McClure "
                       "departed; Beauchamp and Esposito won in "
                       "neither certified election and hold the "
                       "two seats by appointment under section "
                       "15.7(a). (The June 2026 Secretary of "
                       "State directory still lists McClure -- "
                       "stale.)")],
           [holder("David Allaire", "david-allaire"),
            holder("Paul Clifford", "paul-clifford"),
            holder("Larry Cupoli", "larry-cupoli"),
            holder("William Gillam, Jr.", "william-gillam-jr"),
            holder("Barry Beauchamp", "barry-beauchamp",
                   how_seated="appointed"),
            holder("Curt Esposito", "curt-esposito",
                   how_seated="appointed"),
            holder("Alex Adams", "alex-adams"),
            holder("Sharon Davis", "sharon-davis"),
            holder("Peter Franzoni", "peter-franzoni"),
            holder("Anna Tadio", "anna-tadio"),
            holder("Michael Talbott", "michael-talbott")]),
    office("ward-clerk", "Ward Clerk",
           "City of Rutland Ward Clerks", 4,
           [charter009("section 2.8: each ward elects a Ward Clerk "
                       "at the even-year election, to a two-year "
                       "term; the city has four wards (charter "
                       "section 1.3 leaves ward boundaries to "
                       "ordinance, and the city's 2026 ballots are "
                       "issued for four wards)"),
            S(RC_RESULTS_2026, f"{RC_2026_C}: the ward clerks "
                               "elected in 2026 are Barbara "
                               "Spaulding (Ward 1), Beth Kiernan "
                               "(Ward 2), Anthony P. Romeo, Jr. "
                               "(Ward 3), and Steve Reynolds "
                               "(Ward 4)")],
           [holder("Barbara Spaulding", "barbara-spaulding"),
            holder("Beth Kiernan", "beth-kiernan"),
            holder("Anthony P. Romeo, Jr.", "anthony-p-romeo-jr"),
            holder("Steve Reynolds", "steve-reynolds")]),
    office("inspector-of-elections", "Inspector of Elections",
           "City of Rutland Inspectors of Elections", 12,
           [charter009("section 2.8: each ward elects a First, a "
                       "Second, and a Third Inspector of Elections "
                       "at the even-year election, to two-year "
                       "terms -- twelve seats across four wards"),
            S(RC_RESULTS_2026, f"{RC_2026_C}: the inspectors "
                               "elected in 2026 are First "
                               "Inspectors Gary Spaulding (Ward 1), "
                               "Thomas A. Carpenter (Ward 2), "
                               "Stephen A. Leach (Ward 3), and Judy "
                               "A. Delpha (Ward 4); Second "
                               "Inspectors Cynthia Sinos (Ward 2), "
                               "Denise Caggige Leach (Ward 3), and "
                               "Angela M. Rivers (Ward 4); and "
                               "Third Inspector Becky Boggess "
                               "(Ward 2). Four seats -- Ward 1 "
                               "Second and Third, Ward 3 Third, and "
                               "Ward 4 Third -- returned no winner "
                               "(write-ins only) and are left "
                               "unfilled")],
           [holder("Gary Spaulding", "gary-spaulding"),
            holder("Thomas A. Carpenter", "thomas-a-carpenter"),
            holder("Stephen A. Leach", "stephen-a-leach"),
            holder("Judy A. Delpha", "judy-a-delpha"),
            holder("Cynthia Sinos", "cynthia-sinos"),
            holder("Denise Caggige Leach", "denise-caggige-leach"),
            holder("Angela M. Rivers", "angela-m-rivers"),
            holder("Becky Boggess", "becky-boggess")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "City of Rutland Justices of the Peace", 15,
           [jp_src("lists fifteen Rutland City justices of the "
                   "peace: David Allaire, Barry Beauchamp, Phil "
                   "Beauchamp, Chris Bove, Paul Clifford, Larry "
                   "Cupoli, Tom Donahue, Peter Fagan, Peg Flory, "
                   "Sandra Gartner, William 'Billy' Gillam, Cheryl "
                   "Hooker, George Hooker, Mary E. Howard, and "
                   "Jack Welch, Jr.")],
           [holder("David Allaire", "david-allaire"),
            holder("Barry Beauchamp", "barry-beauchamp"),
            holder("Phil Beauchamp", "phil-beauchamp"),
            holder("Chris Bove", "chris-bove"),
            holder("Paul Clifford", "paul-clifford"),
            holder("Larry Cupoli", "larry-cupoli"),
            holder("Thomas Donahue", "thomas-donahue",
                   ballot_name="Tom Donahue"),
            holder("Peter Fagan", "peter-fagan"),
            holder("Peg Flory", "peg-flory"),
            holder("Sandra Gartner", "sandra-gartner"),
            holder("William Gillam, Jr.", "william-gillam-jr",
                   ballot_name="William 'Billy' Gillam"),
            holder("Cheryl Hooker", "cheryl-hooker"),
            holder("George Hooker", "george-hooker"),
            holder("Mary E. Howard", "mary-e-howard"),
            holder("Jack Welch, Jr.", "jack-welch-jr")]),
], jp=jp_election("rutland-vt", "City of Rutland", 15,
                  "the certified listing names fifteen winners "
                  "for Rutland City's fifteen justice of the "
                  "peace seats"))

# ----------------------------------------------------------------
# Town of Ryegate (Caledonia County) -- general law. CORRECTED:
# the first delegated read of the town site was partly fabricated
# (invented cemetery/library rosters); this spec rests only on
# the live pages read firsthand, the town's 2016 Annual Report
# officers table, and the SOS spine.
RYG_TREAS = {"url": "https://www.ryegatevt.org/treasurer",
             "note": "PLACEHOLDER"}
RYG_REPORT = {"url": "https://storage.googleapis.com/juniper-media-library/546/2026/04/2016%20Annual%20Report.pdf",
              "note": "PLACEHOLDER"}
RYG_REPORT_C = ("Town of Ryegate, 2016 Annual Report, 'Town "
                "Officers' table (the report posted on the "
                "town's website)")
SPECS["ryegate"] = spec("ryegate", "Town of Ryegate", [
    office("moderator", "Town Moderator",
           "Town of Ryegate Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term"),
            S(RYG_REPORT, f"{RYG_REPORT_C}: Ryegate elects a "
                          "moderator at its annual meeting; no "
                          "official source publishes the current "
                          "holder")]),
    office("town-clerk", "Town Clerk",
           "Town of Ryegate Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(RYG_CLERK, "Town of Ryegate, Town Clerk page "
                         "(ryegatevt.org): Elizabeth Page is the "
                         "Town Clerk (Marsha Nelson is Assistant "
                         "Town Clerk)"),
            guide("lists Elizabeth Page as Ryegate's Town Clerk"),
            clerk_xlsx("names Elizabeth Page as Ryegate's Town "
                       "Clerk")],
           [holder("Elizabeth Page", "elizabeth-page")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Ryegate Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(RYG_TREAS, "Town of Ryegate, Treasurer page "
                         "(ryegatevt.org): Lorinda Blood is the "
                         "Town Treasurer (Pat Crocker is "
                         "Assistant Treasurer)"),
            treas_xlsx("names Lorinda Blood as Ryegate's Town "
                       "Treasurer"),
            guide("lists Cheryl Slayton as Ryegate's Town "
                  "Treasurer -- superseded by the town's own "
                  "current page and the June 2026 treasurer "
                  "spreadsheet; Slayton, who held the office in "
                  "2016, is not recorded as the current holder")],
           [holder("Lorinda Blood", "lorinda-blood")]),
    office("selectboard", "Selectboard Member",
           "Town of Ryegate Selectboard", 3,
           [sb_dir("lists Ryegate's three selectboard members: "
                   "Regina Hazel, Darryl Perkins, and Andrew "
                   "Smith"),
            S(RYG_SB, "Town of Ryegate, Board of Selectmen page "
                      "(ryegatevt.org): the selectboard members "
                      "are Regina Hazel, Darryl Perkins, and "
                      "Andrew Smith. This Andrew Smith is a "
                      "Ryegate resident and a different man from "
                      "the Town of Berkshire's selectboard member "
                      "of the same name")],
           [holder("Regina Hazel", "regina-hazel"),
            holder("Darryl Perkins", "darryl-perkins"),
            holder("Andrew Smith", "andrew-smith")]),
    office("lister", "Lister",
           "Town of Ryegate Board of Listers", 3,
           [statute2646_structure("towns elect a board of listers "
                                  "of three"),
            S(RYG_REPORT, f"{RYG_REPORT_C}: Ryegate elects three "
                          "listers; no official source publishes "
                          "the current holders")]),
    office("auditor", "Auditor",
           "Town of Ryegate Auditors", 3,
           [statute2646_structure("towns elect auditors (three, "
                                  "staggered terms) unless the "
                                  "office is eliminated"),
            S(RYG_REPORT, f"{RYG_REPORT_C}: Ryegate elects three "
                          "auditors; no official source "
                          "publishes the current holders")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Ryegate Collector of Delinquent Taxes", 1,
           [statute2646_structure("towns elect a collector of "
                                  "delinquent taxes for a "
                                  "one-year term unless the town "
                                  "votes a longer term"),
            S(RYG_REPORT, f"{RYG_REPORT_C}: Ryegate elects a "
                          "delinquent tax collector; no official "
                          "source publishes the current holder")]),
    office("first-constable", "First Constable",
           "Town of Ryegate First Constable", 1,
           [statute2646_structure("towns elect a first constable"),
            S(RYG_REPORT, f"{RYG_REPORT_C}: Ryegate elects a "
                          "first constable; no official source "
                          "publishes the current holder")]),
    office("grand-juror", "Grand Juror",
           "Town of Ryegate Grand Juror", 1,
           [statute2646_structure("towns elect a grand juror for "
                                  "a one-year term"),
            S(RYG_REPORT, f"{RYG_REPORT_C}: Ryegate elects a "
                          "grand juror; no official source "
                          "publishes the current holder")]),
    office("town-agent", "Town Agent",
           "Town of Ryegate Town Agent", 1,
           [statute2646_structure("towns elect a town agent"),
            S(RYG_REPORT, f"{RYG_REPORT_C}: Ryegate elects a "
                          "town agent; no official source "
                          "publishes the current holder")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Ryegate Cemetery Commission", 5,
           [S(RYG_CEM, "Town of Ryegate, Cemetery Commission page "
                       "(ryegatevt.org): the commissioners are "
                       "Rick Colby (Chair), Bruce Nelson (Vice "
                       "Chair), Dan LaCoss (Clerk), Bill Nelson "
                       "(Treasurer), and Melissa Mann (Assistant "
                       "Clerk)"),
            S(RYG_REPORT, f"{RYG_REPORT_C}: Ryegate's cemetery "
                          "commission is a board of five elected "
                          "commissioners on staggered terms; the "
                          "2016 members included William Nelson, "
                          "Richard Colby II, Dan LaCoss, and Bruce "
                          "Nelson")],
           [holder("Richard Colby II", "richard-colby-ii"),
            holder("Bruce Nelson", "bruce-nelson"),
            holder("Dan LaCoss", "dan-lacoss"),
            holder("William Nelson", "william-nelson"),
            holder("Melissa Mann", "melissa-mann")]),
    office("library-trustee", "Library Trustee",
           "Town of Ryegate Library Trustees", 5,
           [S(RYG_REPORT, f"{RYG_REPORT_C}: Ryegate elects five "
                          "library trustees on staggered terms"),
            S(RYG_LIB, "Town of Ryegate, Library Trustees page "
                       "(ryegatevt.org): the page publishes no "
                       "current trustee names (a heading and a "
                       "meeting agendas and minutes button only), "
                       "so the post is created without "
                       "memberships")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Ryegate Justices of the Peace", 7,
           [jp_src("lists seven Ryegate justices of the peace: "
                   "Michael Murray, Darcy Nelson, Robert Rowden, "
                   "Nancy Perkins, Jerry Esposito, Sr., Lauren "
                   "Nelson, and William Dickey")],
           [holder("Michael Murray", "michael-murray"),
            holder("Darcy Nelson", "darcy-nelson"),
            holder("Robert Rowden", "robert-rowden"),
            holder("Nancy Perkins", "nancy-perkins"),
            holder("Jerry Esposito, Sr.", "jerry-esposito-sr"),
            holder("Lauren Nelson", "lauren-nelson"),
            holder("William Dickey", "william-dickey")]),
], jp=jp_election("ryegate-vt", "Town of Ryegate", 7,
                  "the certified listing names seven winners for "
                  "Ryegate's seven justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Salisbury (Addison County) -- ch. 146 (clerk elected
# one-year; treasurer appointed).
SAL_WARN_C = ("Town of Salisbury, Warning for the Annual Town "
              "Meeting (floor meeting February 28, 2026; "
              "Australian ballot March 3, 2026)")
SPECS["salisbury"] = spec("salisbury", "Town of Salisbury", [
    office("moderator", "Town Moderator",
           "Town of Salisbury Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term"),
            S(SAL_WARN, f"{SAL_WARN_C}: Article 4 elects a "
                        "Moderator for a one-year term; no "
                        "official source publishes the 2026 "
                        "outcome")]),
    office("town-clerk", "Town Clerk",
           "Town of Salisbury Town Clerk", 1,
           [charter146("section 2: the Town Clerk is elected for "
                       "a one-year term"),
            S(SAL_WARN, f"{SAL_WARN_C}: Article 4 elects a Town "
                        "Clerk for a one-year term; no tally is "
                        "published"),
            S(SAL_CLERK, "Town of Salisbury, Town Clerk page "
                         "(townofsalisbury.org), as read October "
                         "19, 2026: Fred Kenney is the Town Clerk"),
            clerk_xlsx("names Allen Hathaway as Salisbury's Town "
                       "Clerk (June 2026); the January 2026 Guide "
                       "names him as well, and the town's clerk "
                       "page still named him in June 2026. "
                       "Hathaway held the office through June "
                       "2026 and Kenney succeeded him afterward; "
                       "Kenney is recorded as an appointed "
                       "successor on the disclosed inference that "
                       "the Selectboard filled a vacancy (the "
                       "Plainfield/Readsboro pattern). Hathaway, "
                       "a departed holder, is not recorded")],
           [holder("Fred Kenney", "fred-kenney",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Salisbury Town Treasurer", 1,
           [charter146("section 1: the Town Treasurer is appointed "
                       "by the Selectboard to a one-year employment "
                       "term (July 1 to June 30)"),
            guide("lists Kerry Dashnaw as Salisbury's Town "
                  "Treasurer")],
           [holder("Kerry Dashnaw", "kerry-dashnaw",
                   how_seated="appointed")]),
    office("selectboard", "Selectboard Member",
           "Town of Salisbury Selectboard", 5,
           [sb_dir("lists Salisbury's five selectboard members: "
                   "Patrick Dunn (Chair), Jonathan Blake (Vice "
                   "Chair), Robbie Devoid, Mark Gleason, and Susan "
                   "Mackey"),
            S(SAL_SITE, "Town of Salisbury official website "
                        "(townofsalisbury.org): the selectboard "
                        "pages name the same five members. Jonathan "
                        "Blake is styled a former state "
                        "representative on the town's volunteers "
                        "page; the sitting Addison-4 "
                        "representatives are Herb Olson and Karen "
                        "Lueders, and Blake is minted new here")],
           [holder("Patrick Dunn", "patrick-dunn"),
            holder("Jonathan Blake", "jonathan-blake"),
            holder("Robbie Devoid", "robbie-devoid"),
            holder("Mark Gleason", "mark-gleason"),
            holder("Susan Mackey", "susan-mackey")]),
    office("lister", "Lister",
           "Town of Salisbury Board of Listers", 3,
           [statute2646_structure("towns elect a board of listers "
                                  "of three"),
            S(SAL_SITE, "Town of Salisbury official website "
                        "(townofsalisbury.org): the site carries "
                        "a Board of Listers and 2025 lister "
                        "minutes, but publishes no current lister "
                        "names, and no lister seat stood on the "
                        "2026 warning")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Salisbury Collector of Delinquent Taxes", 1,
           [statute2646_structure("towns elect a collector of "
                                  "delinquent taxes for a "
                                  "one-year term unless the town "
                                  "votes a longer term"),
            S(SAL_WARN, f"{SAL_WARN_C}: Article 4 elects a "
                        "Collector of Delinquent Taxes for a "
                        "one-year term; no official source "
                        "publishes the 2026 outcome")]),
    office("first-constable", "First Constable",
           "Town of Salisbury First Constable", 1,
           [statute2646_structure("towns elect a first constable"),
            S(SAL_WARN, f"{SAL_WARN_C}: Article 4 elects a First "
                        "Constable for a one-year term; no "
                        "official source publishes the 2026 "
                        "outcome")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Salisbury Justices of the Peace", 7,
           [jp_src("lists seven Salisbury justices of the peace: "
                   "Jonathan Blake (as 'Jonathon Blake'), Brian "
                   "Christie, Jaclyn Davidson, Jeff McDonough, "
                   "David Moats, Kathryn Schloff, and Susan Scott. "
                   "This Jeff McDonough is a Salisbury resident, "
                   "a different man from the Town of Leicester's "
                   "first constable of the same name")],
           [holder("Jonathan Blake", "jonathan-blake",
                   ballot_name="Jonathon Blake"),
            holder("Brian Christie", "brian-christie"),
            holder("Jaclyn Davidson", "jaclyn-davidson"),
            holder("Jeff McDonough", "jeff-mcdonough"),
            holder("David Moats", "david-moats"),
            holder("Kathryn Schloff", "kathryn-schloff"),
            holder("Susan Scott", "susan-scott")]),
], jp=jp_election("salisbury-vt", "Town of Salisbury", 7,
                  "the certified listing names seven winners for "
                  "Salisbury's seven justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Sandgate (Bennington County) -- general law; the town's
# own post-meeting roster is the authority.
SAN_PAGE_C = ("Town of Sandgate, 'Elected Officers' page "
              "(sandgatevermont.org), headed 'As of March 3, "
              "2026' -- the town's current post-meeting roster")
SPECS["sandgate"] = spec("sandgate", "Town of Sandgate", [
    office("moderator", "Town Moderator",
           "Town of Sandgate Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(SAN_ELECTED, f"{SAN_PAGE_C}: Sheila Kearns is Town "
                           "Moderator")],
           [holder("Sheila Kearns", "sheila-kearns")]),
    office("town-clerk", "Town Clerk",
           "Town of Sandgate Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(SAN_ELECTED, f"{SAN_PAGE_C}: Jessica Lewis is Town "
                           "Clerk. The January 2026 Secretary of "
                           "State Guide still lists Sandra Reidy, "
                           "whom the town's post-meeting roster "
                           "supersedes; Reidy is not recorded")],
           [holder("Jessica Lewis", "jessica-lewis")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Sandgate Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(SAN_ELECTED, f"{SAN_PAGE_C}: Jessica Lewis is Town "
                           "Treasurer (see the clerk note on the "
                           "superseded Guide entry)")],
           [holder("Jessica Lewis", "jessica-lewis")]),
    office("selectboard", "Selectboard Member",
           "Town of Sandgate Selectboard", 5,
           [sb_dir("lists Sandgate's five selectboard members: "
                   "Joseph Nolan (Chair), Jessica Pendleton, John "
                   "Phelps, Linda Schmidt, and Robert Viglas"),
            S(SAN_ELECTED, f"{SAN_PAGE_C}: the same five members "
                           "are listed")],
           [holder("Joseph Nolan", "joseph-nolan"),
            holder("Jessica Pendleton", "jessica-pendleton"),
            holder("John Phelps", "john-phelps"),
            holder("Linda Schmidt", "linda-schmidt"),
            holder("Robert Viglas", "robert-viglas")]),
    office("lister", "Lister",
           "Town of Sandgate Board of Listers", 3,
           [statute2646("towns elect a board of listers of three"),
            S(SAN_ELECTED, f"{SAN_PAGE_C}: the listers are "
                           "Phyllis Skidmore and Adam Hess; the "
                           "third seat reads 'pending "
                           "appointment' and is left unfilled")],
           [holder("Phyllis Skidmore", "phyllis-skidmore"),
            holder("Adam Hess", "adam-hess")]),
    office("auditor", "Auditor",
           "Town of Sandgate Auditors", 3,
           [statute2646("towns elect auditors (three, staggered "
                        "terms) unless the office is eliminated"),
            S(SAN_ELECTED, f"{SAN_PAGE_C}: the auditors are "
                           "Valerie dePeyster and Mark Neff; the "
                           "third seat reads 'pending appointment' "
                           "and is left unfilled")],
           [holder("Valerie dePeyster", "valerie-depeyster"),
            holder("Mark Neff", "mark-neff")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Sandgate Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes for a one-year term unless the "
                        "town votes a longer term"),
            S(SAN_ELECTED, f"{SAN_PAGE_C}: Eleanor LaCross is "
                           "Collector of Delinquent Taxes")],
           [holder("Eleanor LaCross", "eleanor-lacross")]),
    office("constable", "Constable",
           "Town of Sandgate Constable", 1,
           [statute2646("towns elect constables"),
            S(SAN_ELECTED, f"{SAN_PAGE_C}: Richard Dahm is "
                           "Constable (the page styles the office "
                           "'State Officer & Constable'); Sandgate "
                           "elects a single constable")],
           [holder("Richard Dahm", "richard-dahm")]),
    office("town-agent", "Town Agent",
           "Town of Sandgate Town Agent", 1,
           [statute2646("towns elect a town agent"),
            S(SAN_ELECTED, f"{SAN_PAGE_C}: Jean Eisenhart is "
                           "Town Agent")],
           [holder("Jean Eisenhart", "jean-eisenhart")]),
    office("grand-juror", "Grand Juror",
           "Town of Sandgate Grand Juror", 1,
           [statute2646("towns elect a grand juror for a one-year "
                        "term"),
            S(SAN_ELECTED, f"{SAN_PAGE_C}: Jean Eisenhart is "
                           "Grand Juror")],
           [holder("Jean Eisenhart", "jean-eisenhart")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Sandgate Cemetery Commission", 3,
           [S(SAN_ELECTED, f"{SAN_PAGE_C}: the cemetery "
                           "commissioners are Ann Hammerle, "
                           "Kathleen Hill, and Julie Robertson")],
           [holder("Ann Hammerle", "ann-hammerle"),
            holder("Kathleen Hill", "kathleen-hill"),
            holder("Julie Robertson", "julie-robertson")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Sandgate Justices of the Peace", 5,
           [jp_src("lists five Sandgate justices of the peace: "
                   "Valerie dePeyster, Julie Robertson, Nancy "
                   "Tschorn, Joyce Trachte, and Margaret Phelps; "
                   "the town's elected-officers page agrees "
                   "exactly")],
           [holder("Valerie dePeyster", "valerie-depeyster"),
            holder("Julie Robertson", "julie-robertson"),
            holder("Nancy Tschorn", "nancy-tschorn"),
            holder("Joyce Trachte", "joyce-trachte"),
            holder("Margaret Phelps", "margaret-phelps")]),
], jp=jp_election("sandgate-vt", "Town of Sandgate", 5,
                  "the certified listing names five winners for "
                  "Sandgate's five justice of the peace seats"))

# ----------------------------------------------------------------
# Village of Saxtons River (in the Town of Rockingham, Windham
# County) -- incorporated under the general statute, 24 V.S.A.
# sec. 1301 (1905); no Title 24 Appendix charter.
SR_WARN_C = ("Village of Saxtons River, Warning for the Annual "
             "Meeting, April 13, 2026 (posted on Falls Area "
             "Community TV, the village's public-access mirror)")
SPECS["saxtons-river"] = spec("saxtons-river",
                              "Village of Saxtons River", [
    office("moderator", "Moderator",
           "Village of Saxtons River Moderator", 1,
           [S(SR_WARNING, f"{SR_WARN_C}: Article 1 elects a "
                          "Moderator; no official source "
                          "publishes the current holder, so the "
                          "post is created without a membership"),
            S(VSARA_VILLAGES, "Vermont State Archives and Records "
                              "Administration, incorporated "
                              "villages list: Saxtons River, in "
                              "Rockingham, Windham County, was "
                              "incorporated under general statute "
                              "24 V.S.A. section 1301 in 1905 (no "
                              "special charter)")]),
    office("trustee", "Village Trustee",
           "Village of Saxtons River Board of Trustees", 5,
           [S(SR_TRUSTEES, "Village of Saxtons River Trustees page "
                           "on the Town of Rockingham's official "
                           "website (rockinghamvt.org), and the "
                           "live roster feed embedded in it: the "
                           "trustees are Andrew Dunbar, Ellen "
                           "Clark-Lawrence, Jason Snell, Kristen "
                           "Swartwout, and Laura Wolfe. "
                           "Clark-Lawrence's feed entry carries "
                           "the board's chair email address"),
            S(SR_WARNING, f"{SR_WARN_C}: Article 3 elects 'any "
                          "open Trustee positions'")],
           [holder("Andrew Dunbar", "andrew-dunbar"),
            holder("Ellen Clark-Lawrence", "ellen-clark-lawrence"),
            holder("Jason Snell", "jason-snell"),
            holder("Kristen Swartwout", "kristen-swartwout"),
            holder("Laura Wolfe", "laura-wolfe")]),
    office("village-treasurer", "Village Treasurer",
           "Village of Saxtons River Village Treasurer", 1,
           [S(SR_WARNING, f"{SR_WARN_C}: Article 3 elects a "
                          "Treasurer; no official source "
                          "publishes the current holder, so the "
                          "post is created without a membership")]),
    office("tax-collector", "Tax Collector",
           "Village of Saxtons River Tax Collector", 1,
           [S(SR_WARNING, f"{SR_WARN_C}: Article 3 elects a Tax "
                          "Collector; no official source "
                          "publishes the current holder, so the "
                          "post is created without a membership")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Village of Saxtons River Collector of Delinquent "
           "Taxes", 1,
           [S(SR_WARNING, f"{SR_WARN_C}: Article 3 elects a "
                          "Collector of Delinquent Taxes; no "
                          "official source publishes the current "
                          "holder, so the post is created without "
                          "a membership")]),
    office("village-clerk", "Village Clerk",
           "Village of Saxtons River Village Clerk", 1,
           [S(SR_WARNING, f"{SR_WARN_C}: Article 3 elects a "
                          "Village Clerk; no official source "
                          "publishes the current holder, so the "
                          "post is created without a membership. "
                          "The trustees' April 27, 2026 "
                          "reorganization agenda also lists an "
                          "'appoint clerk' item, which is noted "
                          "as ambiguous against the warning's "
                          "election article")]),
    office("auditor", "Village Auditor",
           "Village of Saxtons River Auditors", 3,
           [S(SR_WARNING, f"{SR_WARN_C}: Article 3 elects 'up to "
                          "Three Auditors'; no official source "
                          "publishes the current holders, so the "
                          "post is created without memberships")]),
])

# ----------------------------------------------------------------
# Town of Searsburg (Bennington County) -- general law; no town
# website or published documents; built on the SOS spine only.
SPECS["searsburg"] = spec("searsburg", "Town of Searsburg", [
    office("moderator", "Town Moderator",
           "Town of Searsburg Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term. Searsburg has "
                                  "no town website and publishes "
                                  "no documents online")]),
    office("town-clerk", "Town Clerk",
           "Town of Searsburg Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Quintina Reynolds as Searsburg's Town "
                  "Clerk")],
           [holder("Quintina Reynolds", "quintina-reynolds")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Searsburg Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists Zettella Penson as Searsburg's Town "
                  "Treasurer")],
           [holder("Zettella Penson", "zettella-penson")]),
    office("selectboard", "Selectboard Member",
           "Town of Searsburg Selectboard", 5,
           [sb_dir("lists Searsburg's five selectboard members as "
                   "five separate rows: Scott Horwath, Tony "
                   "Kilbride (Chair), Chris Reynolds (Vice Chair), "
                   "Christopher Reynolds, and Gary Sage. Chris "
                   "Reynolds and Christopher Reynolds are printed "
                   "as separate members with different addresses "
                   "(1488 and 1478 VT Route 9 W) and different "
                   "email addresses, and are recorded as two "
                   "people; if the directory duplicated one man, "
                   "the duplication is the directory's, flagged "
                   "on issue #163")],
           [holder("Scott Horwath", "scott-horwath"),
            holder("Tony Kilbride", "tony-kilbride"),
            holder("Chris Reynolds", "chris-reynolds"),
            holder("Christopher Reynolds", "christopher-reynolds"),
            holder("Gary Sage", "gary-sage")]),
    office("lister", "Lister",
           "Town of Searsburg Board of Listers", 3,
           [statute2646_structure("towns elect a board of listers "
                                  "of three")]),
    office("auditor", "Auditor",
           "Town of Searsburg Auditors", 3,
           [statute2646_structure("towns elect auditors (three, "
                                  "staggered terms) unless the "
                                  "office is eliminated")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Searsburg Collector of Delinquent Taxes", 1,
           [statute2646_structure("towns elect a collector of "
                                  "delinquent taxes for a "
                                  "one-year term unless the town "
                                  "votes a longer term")]),
    office("first-constable", "First Constable",
           "Town of Searsburg First Constable", 1,
           [statute2646_structure("towns elect a first constable")]),
    office("grand-juror", "Grand Juror",
           "Town of Searsburg Grand Juror", 1,
           [statute2646_structure("towns elect a grand juror for "
                                  "a one-year term")]),
    office("town-agent", "Town Agent",
           "Town of Searsburg Town Agent", 1,
           [statute2646_structure("towns elect a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Searsburg Justices of the Peace", 5,
           [jp_src("lists five Searsburg justices of the peace: "
                   "Daniel Hollister, Tammy Hollister, Derick "
                   "Lind, Sherrie Fox, and Tamera Wood")],
           [holder("Daniel Hollister", "daniel-hollister"),
            holder("Tammy Hollister", "tammy-hollister"),
            holder("Derick Lind", "derick-lind"),
            holder("Sherrie Fox", "sherrie-fox"),
            holder("Tamera Wood", "tamera-wood")]),
], jp=jp_election("searsburg-vt", "Town of Searsburg", 5,
                  "the certified listing names five winners for "
                  "Searsburg's five justice of the peace seats"))

ORDER = ["roxbury", "royalton", "rupert", "rutland-61300",
         "rutland", "ryegate", "salisbury", "sandgate",
         "saxtons-river", "searsburg"]

for slug in ORDER:
    (OUT / f"{slug}.json").write_text(
        json.dumps(SPECS[slug], indent=1) + "\n")
print("wrote", len(ORDER), "specs")
