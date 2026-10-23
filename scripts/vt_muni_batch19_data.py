#!/usr/bin/env python3
"""Batch 19 of the VT #163 municipal fan-out (alphabetical positions
180-189): Proctor, Putney, Randolph, Reading, Readsboro, Richford,
Richmond, Ripton, Rochester, Rockingham. Emits one JSON spec per
municipality for build_vt_municipality.py.
Research: vt_muni_batch19_research.md.

Identity calls baked into this batch (all flagged on #163):
- Randolph Selectboard member Larry Satcowitz is the sitting State
  Representative for Orange-Washington-Addison (the district
  includes Randolph): his SB membership reuses the state-tier
  person record ocd-person/96aec30c-01e8-5b0e-905f-2e925a4886cf.
- Rockingham Moderator and JP Paul Obuchowski is the Village of
  Bellows Falls Village President (batch 2): both Rockingham
  memberships reuse ocd-person/6d6d72e1-192d-5297-9e70-
  0ca72fb41e6f, and his JP candidacy is appended to that record
  by hand after the build.
- Rockingham JP Dennis Harty is the Village of Bellows Falls
  Moderator (batch 2): reuse ocd-person/fd82594b-92ae-5ab2-9e36-
  85c3a953a763, JP candidacy appended by hand after the build.
- Rockingham Town Clerk/Treasurer Kathleen Kelly is the Village
  of Bellows Falls Village Clerk (batch 2; that record's own
  source note identifies her as the Rockingham Town Clerk):
  reuse ocd-person/415f603f-55ab-5bb4-be75-de1d7971b087.
- Rochester JP Kevin Dougherty is a NEW person, distinct from
  the Clarendon JP of the same name (batch 6): a JP serves the
  town of residence, and Clarendon and Rochester are in
  different counties.
- Readsboro's Town Clerk and Town Treasurer (Cheryl Green) are
  minted APPOINTED on a disclosed inference: Amber Holland's
  elected terms expired at the March 2026 meeting, the town
  published no 2026 results, Holland still acted as clerk on
  March 24, 2026, the town advertised the combined
  Clerk/Treasurer position as a job, and the town's current
  Town Info page names Green (Plainfield batch-18 pattern).
- Ripton's JP Amy McGlashan (elected November 2024) vacated
  the seat in 2025 and Irene Poole was appointed: per the
  batch-8 Enosburgh (Gervais) pattern McGlashan is minted
  nowhere; Poole holds an appointed membership with no
  candidacy, and the election note tells the story.
- Putney's Town Clerk and Town Treasurer, Ripton's Town Clerk,
  and Richmond's Delinquent Tax Collector are APPOINTED (see
  the per-office notes); Ripton's Treasurer has been appointed
  since 2018 per the town's own treasurer page.
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
CHARTER_141 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/141",
    "note": "PLACEHOLDER",
}
CHARTER_142 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/142",
    "note": "PLACEHOLDER",
}
CHARTER_143 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/143",
    "note": "PLACEHOLDER",
}
PCT_SB = {"url": "https://proctorvermont.com/selectboard/",
          "note": "PLACEHOLDER"}
PCT_CLERK = {"url": "https://proctorvermont.com/town-clerk-treasurer/",
             "note": "PLACEHOLDER"}
PCT_CEM = {"url": "https://proctorvermont.com/cemetery-commission/",
           "note": "PLACEHOLDER"}
PCT_DIR = {"url": "https://proctorvermont.com/contact-directory/",
           "note": "PLACEHOLDER"}
PCT_WARN = {"url": "https://proctorvermont.com/wp-content/uploads/Warning.png",
            "note": "PLACEHOLDER"}
PCT_REPORT = {"url": "https://proctorvermont.com/wp-content/uploads/web-proctor-Final-Report.pdf",
              "note": "PLACEHOLDER"}
PUT_WARN = {"url": "https://putneyvt.gov/Documents/Department/Clerk/Annual%20Town%20Meetings/2026/2026%20Town%20of%20Putney%20Warning%20for%20Annual%20Meeting.pdf",
            "note": "PLACEHOLDER"}
PUT_MIN = {"url": "https://putneyvt.gov/Documents/Department/Clerk/Annual%20Town%20Meetings/2026/03.03.26%20Draft%20Town%20Meeting%20Minutes.pdf",
           "note": "PLACEHOLDER"}
PUT_REPORT = {"url": "https://putneyvt.gov/Documents/Department/Clerk/Town%20Reports/2025_Town_Report.pdf",
              "note": "PLACEHOLDER"}
PUT_LIB = {"url": "https://putneylibrary.org/about-the-library/library-board-governance/",
           "note": "PLACEHOLDER"}
RAN_WARN = {"url": "https://legacy.randolphtownvt.org/vertical/sites/%7BD7EA543D-4DEE-41D3-BD57-86E65A3C936B%7D/uploads/Town_of_Randolph_-_2026_Town_Meeting_Warning_(signed_as_adopted_01-29-26).pdf",
            "note": "PLACEHOLDER"}
RAN_REPORT = {"url": "https://legacy.randolphtownvt.org/vertical/sites/%7BD7EA543D-4DEE-41D3-BD57-86E65A3C936B%7D/uploads/2024_Town_Report___web_version(2).pdf",
              "note": "PLACEHOLDER"}
RAN_HERALD = {"url": "https://www.ourherald.com/articles/randolph-keeps-meeting-passes-budgets/",
              "note": "PLACEHOLDER"}
RDG_BASE = ("https://readingvt.govoffice.com/vertical/sites/"
            "%7B29D76170-2CBD-4DB0-A089-6F91F5BED766%7D/uploads/")
RDG_REPORT = {"url": RDG_BASE + "Town_Report_Fiscal_Y-E_2024.pdf",
              "note": "PLACEHOLDER"}
RDG_FEB26 = {"url": RDG_BASE + "February_2026_Informer.pdf",
             "note": "PLACEHOLDER"}
RDG_APR26 = {"url": RDG_BASE + "April_2026_Informer.pdf",
             "note": "PLACEHOLDER"}
RDG_MIN = {"url": RDG_BASE + "5-11-26_Mtg._Minutes_Selectboard.pdf",
           "note": "PLACEHOLDER"}
RDS_REPORT = {"url": "https://readsborovt.org/uploads/2025-town-report-final.pdf",
              "note": "PLACEHOLDER"}
RDS_POS = {"url": "https://readsborovt.org/uploads/positions-for-election-2026.pdf",
           "note": "PLACEHOLDER"}
RDS_MIN = {"url": "https://towncloud-core-prod.s3.us-west-2.amazonaws.com/uploads/readsboro-vt/meetings/agenda_packet/minutes/1022/town-meeting_minutes_2026-03-02_123440.pdf",
           "note": "PLACEHOLDER"}
RDS_INFO = {"url": "https://readsborovt.org/pages/town-info",
            "note": "PLACEHOLDER"}
RDS_BOARDS = {"url": "https://readsborovt.org/pages/boards-commissions",
              "note": "PLACEHOLDER"}
RFR_SB = {"url": "https://www.richfordvt.org/select-board.html",
          "note": "PLACEHOLDER"}
RFR_PC = {"url": "https://www.richfordvt.org/planning-commission.html",
          "note": "PLACEHOLDER"}
RFR_DIR = {"url": "https://www.richfordvt.org/municipal-directory.html",
           "note": "PLACEHOLDER"}
RFR_REPORT = {"url": "https://www.richfordvt.org/uploads/1/2/0/4/120478017/town_report_2025.pdf",
              "note": "PLACEHOLDER"}
RMD_MEMBERS = {"url": "https://www.richmondvt.gov/boards-meetings/all-committee-board-members",
               "note": "PLACEHOLDER"}
RMD_CLERK = {"url": "https://www.richmondvt.gov/departments/town-clerk",
             "note": "PLACEHOLDER"}
RMD_REPORT = {"url": "https://www.richmondvt.gov/fileadmin/files/News/2026/02/2025_Richmond_Town_Report.pdf",
              "note": "PLACEHOLDER"}
RIP_SB = {"url": "https://www.riptonvermont.org/selectboard",
          "note": "PLACEHOLDER"}
RIP_LIST = {"url": "https://www.riptonvermont.org/listers",
            "note": "PLACEHOLDER"}
RIP_CLERK = {"url": "https://www.riptonvermont.org/town-clerk",
             "note": "PLACEHOLDER"}
RIP_TREAS = {"url": "https://www.riptonvermont.org/treasurer",
             "note": "PLACEHOLDER"}
RIP_CEM = {"url": "https://www.riptonvermont.org/cemetery-commission",
           "note": "PLACEHOLDER"}
RIP_REPORT = {"url": "https://drive.google.com/file/d/1M3hBxYFnzukIMUEIJVBJ5lyY0qcFk_qE/view",
              "note": "PLACEHOLDER"}
ROC_REPORT = {"url": "https://rochestervermont.org/wp-content/uploads/2026/02/Rochester-Town-Report-FY-2025.pdf",
              "note": "PLACEHOLDER"}
ROC_MIN = {"url": "https://rochestervermont.org/wp-content/uploads/2026/03/2026-DRAFT-TOWN-MEETING-MINUTES.pdf",
           "note": "PLACEHOLDER"}
ROC_HERALD = {"url": "https://www.ourherald.com/articles/rochester-holds-lively-town-meeting/",
              "note": "PLACEHOLDER"}
RKH_LIB_DOCS = {"url": "https://www.rockinghamvt.org/documentlibrary",
                "note": "PLACEHOLDER"}
RKH_SB = {"url": "https://www.rockinghamvt.org/rockinghamselect",
          "note": "PLACEHOLDER"}
RKH_CLERK = {"url": "https://www.rockinghamvt.org/townclerk",
             "note": "PLACEHOLDER"}
RKH_LIST = {"url": "https://www.rockinghamvt.org/listersoffice",
            "note": "PLACEHOLDER"}
RKH_LIB = {"url": "https://rockinghamlibrary.org/administration-board-of-trustees/",
           "note": "PLACEHOLDER"}
RKH_LIBBYLAWS = {"url": "http://rockinghamlibrary.org/wp/wp-content/uploads/2015/02/Draft-Bylaws-with-revisions-at-Nov-25-Board-meeting.pdf",
                 "note": "PLACEHOLDER"}
RKH_COMMONS = {"url": "https://vimnews.org/authorproofs/COMM-0855.rock.TM_election_results.authorproof.pdf",
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


def charter141(phrase):
    return S(CHARTER_141, f"24 App. V.S.A. ch. 141 (Town of "
             f"Readsboro): {phrase}")


def charter142(phrase):
    return S(CHARTER_142, f"24 App. V.S.A. ch. 142 (Town of "
             f"Richford): {phrase}")


def charter143(phrase):
    return S(CHARTER_143, f"24 App. V.S.A. ch. 143 (Town of "
             f"Richmond): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 19); issue #163 "
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
                  f"# municipal fan-out batch 19; issue #163 "
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
# Town of Proctor (Rutland County) -- general law.
PCT_WARN_C = ("Town of Proctor, Warning for the Annual Town "
              "Meeting (signed January 26, 2026; floor meeting "
              "March 2, 2026 and Australian ballot March 3, 2026)")
PCT_REPORT_C = ("Town of Proctor, 2023 Annual Report, Elected "
                "Officials table (the report posted on the town "
                "website)")
SPECS["proctor"] = spec("proctor", "Town of Proctor", [
    office("moderator", "Town Moderator",
           "Town of Proctor Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term"),
            S(PCT_WARN, f"{PCT_WARN_C}: the ballot articles elect "
                        "a Moderator for a one-year term. The "
                        "2023 report's table names Andrew Maass "
                        "(term to 2024); no official source "
                        "publishes the 2026 outcome, so the post "
                        "is created without a membership")]),
    office("town-clerk", "Town Clerk",
           "Town of Proctor Town Clerk", 1,
           [statute2646("towns elect a town clerk; Proctor elects "
                        "the clerk to a three-year term"),
            S(PCT_WARN, f"{PCT_WARN_C}: the ballot articles elect "
                        "a Town Clerk for a three-year term"),
            S(PCT_CLERK, "Town of Proctor, Town Clerk & Treasurer "
                         "page (proctorvermont.com): Celia "
                         "Lisananti is the Town Clerk. Her "
                         "three-year term expired at the 2026 "
                         "meeting and the seat stood; she is "
                         "recorded as the continuing clerk on "
                         "the town's maintained clerk page and "
                         "contact directory (incumbent continuity, "
                         "disclosed)"),
            guide("lists Celia Lisananti as Proctor's Town Clerk")],
           [holder("Celia Lisananti", "celia-lisananti")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Proctor Town Treasurer", 1,
           [statute2646("towns elect a town treasurer; Proctor "
                        "elects the treasurer to a three-year "
                        "term"),
            S(PCT_WARN, f"{PCT_WARN_C}: the ballot articles elect "
                        "a Town Treasurer for a three-year term"),
            S(PCT_CLERK, "Town of Proctor, Town Clerk & Treasurer "
                         "page (proctorvermont.com): Celia "
                         "Lisananti is the Town Treasurer; see "
                         "the clerk note on incumbent continuity"),
            guide("lists Celia Lisananti as Proctor's Town "
                  "Treasurer")],
           [holder("Celia Lisananti", "celia-lisananti")]),
    office("selectboard", "Selectboard Member",
           "Town of Proctor Selectboard", 5,
           [sb_dir("lists Proctor's five selectboard members: "
                   "Bruce Baccei, Linda Doty, Lisa Miser, Jason "
                   "Thornton, and Albert Wenta"),
            S(PCT_SB, "Town of Proctor, Selectboard page "
                      "(proctorvermont.com): Lisa Miser, Chair; "
                      "Bruce Baccei, Vice Chair; Linda Doty; "
                      "Albert Wenta; and Jay Thornton (the "
                      "directory's Jason Thornton)")],
           [holder("Lisa Miser", "lisa-miser"),
            holder("Bruce Baccei", "bruce-baccei"),
            holder("Linda Doty", "linda-doty"),
            holder("Albert Wenta", "albert-wenta"),
            holder("Jason Thornton", "jason-thornton")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Proctor Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes for a one-year term unless the "
                        "town votes a longer term"),
            S(PCT_REPORT, f"{PCT_REPORT_C}: the table gives the "
                          "Collector of Delinquent Taxes its own "
                          "three-year term (Celia Lisananti); the "
                          "seat did not stand in 2026"),
            S(PCT_CLERK, "Town of Proctor, Town Clerk & Treasurer "
                         "page: Celia Lisananti 'also serves as "
                         "the collector of current and delinquent "
                         "taxes'")],
           [holder("Celia Lisananti", "celia-lisananti")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Proctor Cemetery Commission", 1,
           [S(PCT_CEM, "Town of Proctor, Cemetery Commission page "
                       "(proctorvermont.com): 'The Riverside "
                       "Cemetery Commissioner is Albert Wenta... "
                       "Since there is no Commission other than "
                       "Albert Wenta' -- Proctor's cemetery "
                       "commission is a single commissioner, on a "
                       "five-year term expiring in 2028")],
           [holder("Albert Wenta", "albert-wenta")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Proctor Justices of the Peace", 5,
           [jp_src("lists five Proctor justices of the peace: "
                   "Judith Taranovich, Frank Beyette, Raymond "
                   "Beyette, Lisa Miser, and Bruce Baccei")],
           [holder("Judith Taranovich", "judith-taranovich"),
            holder("Frank Beyette", "frank-beyette"),
            holder("Raymond Beyette", "raymond-beyette"),
            holder("Lisa Miser", "lisa-miser"),
            holder("Bruce Baccei", "bruce-baccei")]),
], jp=jp_election("proctor-vt", "Town of Proctor", 5,
                  "the certified listing names five winners for "
                  "Proctor's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Putney (Windham County) -- general law; town-manager
# form. The town's posted 2026 results and certification PDFs
# returned 404 on October 19, 2026; the officers elected in 2026
# rest on the town's DRAFT minutes of the March 3, 2026 annual
# meeting (disclosed).
PUT_MIN_C = ("Town of Putney, DRAFT Minutes of the Annual Town "
             "Meeting, March 3, 2026 (the town's posted 2026 "
             "results documents returned 404; the draft minutes "
             "record the outcomes)")
PUT_REPORT_C = ("Town of Putney, 2025 Town Report, ELECTED "
                "OFFICIALS table and directory pages")
SPECS["putney"] = spec("putney", "Town of Putney", [
    office("moderator", "Town Moderator",
           "Town of Putney Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(PUT_MIN, f"{PUT_MIN_C}: Benjamin 'Benjie' Cragin "
                       "was elected Moderator (Meg Mott retired)")],
           [holder("Benjamin Cragin", "benjamin-cragin")]),
    office("town-clerk", "Town Clerk",
           "Town of Putney Town Clerk", 1,
           [statute2646("towns elect a town clerk unless the town "
                        "has voted to authorize appointment under "
                        "17 V.S.A. section 2651e"),
            S(PUT_REPORT, f"{PUT_REPORT_C}: the Town Clerk does "
                          "not appear in the town's ELECTED "
                          "OFFICIALS table nor on the 2025 or "
                          "2026 ballots (Putney is a town-manager "
                          "town); Jonathan Johnson serves as "
                          "Town Clerk by appointment. The "
                          "conversion instrument itself was not "
                          "located (disclosed)"),
            guide("lists Jonathan Johnson as Putney's Town Clerk")],
           [holder("Jonathan Johnson", "jonathan-johnson",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Putney Town Treasurer", 1,
           [statute2646("towns elect a town treasurer unless the "
                        "town has voted to authorize appointment "
                        "under 17 V.S.A. section 2651f"),
            S(PUT_REPORT, f"{PUT_REPORT_C}: the Town Treasurer "
                          "does not appear in the town's ELECTED "
                          "OFFICIALS table nor on the 2025 or "
                          "2026 ballots; Kimberly Munro serves "
                          "as Town Treasurer by appointment "
                          "(disclosed as for the clerk)"),
            guide("lists Kimberly Munro as Putney's Town "
                  "Treasurer")],
           [holder("Kimberly Munro", "kimberly-munro",
                   how_seated="appointed")]),
    office("selectboard", "Selectboard Member",
           "Town of Putney Selectboard", 5,
           [sb_dir("lists Putney's five selectboard members: Peg "
                   "Alden, Eric Mcgowan, Logan Sears, Rebecca "
                   "Slattery, and Aileen Tulloch"),
            S(PUT_MIN, f"{PUT_MIN_C}: Peg Alden was re-elected "
                       "to the three-year seat and Logan Sears "
                       "won the two-year seat; the board sits as "
                       "Eric McGowan (Chair), Peg Alden (Vice "
                       "Chair), Aileen Tulloch, Rebecca 'Bex' "
                       "Slattery, and Logan Sears")],
           [holder("Eric McGowan", "eric-mcgowan"),
            holder("Peg Alden", "peg-alden"),
            holder("Aileen Tulloch", "aileen-tulloch"),
            holder("Rebecca Slattery", "rebecca-slattery"),
            holder("Logan Sears", "logan-sears")]),
    office("lister", "Lister",
           "Town of Putney Board of Listers", 3,
           [statute2646("towns elect a board of listers of three "
                        "on staggered three-year terms"),
            S(PUT_REPORT, f"{PUT_REPORT_C}: listers Kurt Lynch, "
                          "Geordie Heller, and Doug Harlow "
                          "(Harlow's seat stood in 2026)"),
            S(PUT_MIN, f"{PUT_MIN_C}: Doug Harlow was elected "
                       "Lister for the three-year term")],
           [holder("Kurt Lynch", "kurt-lynch"),
            holder("Geordie Heller", "geordie-heller"),
            holder("Doug Harlow", "doug-harlow")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Putney Cemetery Commission", 3,
           [S(PUT_REPORT, f"{PUT_REPORT_C}: cemetery "
                          "commissioners Jonathan Johnson "
                          "(Chair) and Lindley Speers, on "
                          "staggered three-year terms"),
            S(PUT_MIN, f"{PUT_MIN_C}: the 2026 three-year "
                       "cemetery commission seat returned 'None "
                       "elected'; the third seat is unfilled")],
           [holder("Jonathan Johnson", "jonathan-johnson"),
            holder("Lindley Speers", "lindley-speers")]),
    office("library-trustee", "Library Trustee",
           "Putney Public Library Board of Trustees", 9,
           [S(PUT_REPORT, f"{PUT_REPORT_C}: the library trustees "
                          "are nine, on staggered three-year "
                          "terms, elected from the floor (2026 "
                          "warning Article 2 elects four)"),
            S(PUT_MIN, f"{PUT_MIN_C}: Amber Paris, Trish "
                       "Roberts, Mike Keim, and Lydia Mathewson "
                       "were elected library trustees from the "
                       "floor"),
            S(PUT_LIB, "Putney Public Library, Library Board "
                      "Governance page (putneylibrary.org): the "
                      "current board names Amber Paris (Chair), "
                      "Trish Roberts, Mike Keim, Lydia Mathewson, "
                      "and Nancy Hood. The report table's other "
                      "mid-term names do not appear on the "
                      "library's current page and are not "
                      "recorded; four seats are unfilled")],
           [holder("Amber Paris", "amber-paris"),
            holder("Trish Roberts", "trish-roberts"),
            holder("Mike Keim", "mike-keim"),
            holder("Lydia Mathewson", "lydia-mathewson"),
            holder("Nancy Hood", "nancy-hood")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Putney Justices of the Peace", 10,
           [jp_src("lists ten Putney justices of the peace: "
                   "Laura Chapman, Karen Gustafson, Holly "
                   "Hammond, Abby Jacobson, Nancy Olson, Amelia "
                   "Struthers, Vanessa Vadim, Wendy Wilson, Gay "
                   "Foster, and Lynne Wilken (the town report "
                   "prints 'Lynne Wilkins'; the certified "
                   "listing governs)")],
           [holder("Laura Chapman", "laura-chapman"),
            holder("Karen Gustafson", "karen-gustafson"),
            holder("Holly Hammond", "holly-hammond"),
            holder("Abby Jacobson", "abby-jacobson"),
            holder("Nancy Olson", "nancy-olson"),
            holder("Amelia Struthers", "amelia-struthers"),
            holder("Vanessa Vadim", "vanessa-vadim"),
            holder("Wendy Wilson", "wendy-wilson"),
            holder("Gay Foster", "gay-foster"),
            holder("Lynne Wilken", "lynne-wilken")]),
], jp=jp_election("putney-vt", "Town of Putney", 10,
                  "the certified listing names ten winners for "
                  "Putney's ten justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Randolph (Orange County) -- general law. The town
# posts no 2026 results; its 2026 outcomes rest on the White
# River Valley Herald's report of the March 2026 meeting
# (March 5, 2026; newspaper class, disclosed).
RAN_REPORT_C = ("Town of Randolph, 2024 Town Report, ELECTED "
                "OFFICIALS and APPOINTMENTS tables (a 2024 "
                "article to convert the Town Clerk to an "
                "appointed office was debated and not passed; "
                "the clerk remains elected)")
RAN_HERALD_C = ("White River Valley Herald, 'Randolph Keeps "
                "Meeting, Passes Budgets' (March 5, 2026): the "
                "town's March 2026 outcomes (newspaper source, "
                "disclosed; the town posts no 2026 results)")
SPECS["randolph"] = spec("randolph", "Town of Randolph", [
    office("moderator", "Town Moderator",
           "Town of Randolph Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(RAN_HERALD, f"{RAN_HERALD_C} -- Kelly Green was "
                          "re-elected Moderator, unopposed")],
           [holder("Kelly Green", "kelly-green")]),
    office("town-clerk", "Town Clerk",
           "Town of Randolph Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(RAN_REPORT, f"{RAN_REPORT_C}: Tammy Munyon is "
                          "Town Clerk; the seat did not stand "
                          "in 2026"),
            guide("lists Tammy Munyon as Randolph's Town Clerk")],
           [holder("Tammy Munyon", "tammy-munyon")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Randolph Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(RAN_REPORT, f"{RAN_REPORT_C}: Tammy Munyon is "
                          "Town Treasurer; the seat did not "
                          "stand in 2026"),
            guide("lists Tammy Munyon as Randolph's Town "
                  "Treasurer")],
           [holder("Tammy Munyon", "tammy-munyon")]),
    office("selectboard", "Selectboard Member",
           "Town of Randolph Selectboard", 5,
           [sb_dir("lists Randolph's five selectboard members: "
                   "Emery Mattheis, Alissa Matthews, Larry "
                   "Satkowitz, Bethany Silloway, and Stephanie "
                   "Tyler (the directory's name columns are "
                   "swapped for Tyler)"),
            S(RAN_HERALD, f"{RAN_HERALD_C} -- Emery Mattheis "
                          "won the three-year seat (480-460 "
                          "over Ashley Lincoln) and Bethany "
                          "Silloway won the two-year seat "
                          "(514-418 over Dustin Adams); Alissa "
                          "Matthews, Larry Satcowitz, and "
                          "Stephanie Tyler continue")],
           [holder("Emery Mattheis", "emery-mattheis"),
            holder("Bethany Silloway", "bethany-silloway"),
            holder("Alissa Matthews", "alissa-matthews"),
            holder("Larry Satcowitz", "larry-satcowitz",
                   existing_person_id="ocd-person/96aec30c-01e8-5b0e-905f-2e925a4886cf"),
            holder("Stephanie Tyler", "stephanie-tyler")]),
    office("lister", "Lister",
           "Town of Randolph Board of Listers", 3,
           [statute2646("towns elect a board of listers of three "
                        "on staggered three-year terms"),
            S(RAN_REPORT, f"{RAN_REPORT_C}: lister Mimi "
                          "Burstein serves to 2027. Dennis "
                          "Brown's seat expired in 2025 with no "
                          "published outcome, and the 2026 "
                          "three-year race had no declared "
                          "candidate (a write-in leader is not "
                          "seated on a plurality alone); two "
                          "seats are unfilled")],
           [holder("Mimi Burstein", "mimi-burstein")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Randolph Trustees of Public Funds", 3,
           [statute2646("towns elect trustees of public funds"),
            S(RAN_REPORT, f"{RAN_REPORT_C}: trustees Joyce "
                          "Mazzucco and Clifford Rankin; Bruce "
                          "Butler's seat expired in 2025 with no "
                          "published outcome (unfilled)"),
            S(RAN_HERALD, f"{RAN_HERALD_C} -- Clifford Rankin "
                          "was re-elected Trustee of Public "
                          "Funds in 2026")],
           [holder("Joyce Mazzucco", "joyce-mazzucco"),
            holder("Clifford Rankin", "clifford-rankin")]),
    office("library-trustee", "Library Trustee",
           "Kimball Public Library Board of Trustees", 5,
           [S(RAN_REPORT, f"{RAN_REPORT_C}: the Kimball Library "
                          "trustees are five: Heather Bowman, "
                          "Karen Lowry Reed, Edward Rooney, "
                          "Morgan James Eaton, and Margaret "
                          "'Peg' Maupin"),
            S(RAN_HERALD, f"{RAN_HERALD_C} -- Morgan James "
                          "Eaton won the three-year library "
                          "seat (547-254) and Margaret Maupin "
                          "won the one-year remainder seat")],
           [holder("Heather Bowman", "heather-bowman"),
            holder("Karen Lowry Reed", "karen-lowry-reed"),
            holder("Edward Rooney", "edward-rooney"),
            holder("Morgan James Eaton", "morgan-james-eaton"),
            holder("Margaret Maupin", "margaret-maupin")]),
    office("budget-committee", "Budget Committee Member",
           "Town of Randolph Budget Committee", 5,
           [S(RAN_REPORT, f"{RAN_REPORT_C}: the Budget Committee "
                          "has five seats elected from the floor "
                          "of the annual meeting. The 2025 and "
                          "2026 floor outcomes are published in "
                          "no official source, so the post is "
                          "created without memberships")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Randolph Collector of Delinquent Taxes", 1,
           [S(RAN_REPORT, f"{RAN_REPORT_C}: the APPOINTMENTS "
                          "table styles the Town Manager as the "
                          "appointed collector of delinquent "
                          "taxes (temporary, early 2025). No "
                          "current confirmation is published, so "
                          "the post is created without a "
                          "membership")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Randolph Justices of the Peace", 8,
           [jp_src("lists eight Randolph justices of the peace: "
                   "Dennis Brown, Kristin Chandler, Kristen "
                   "Gage, Thomas Harty, Emery Mattheis, Ceciele "
                   "Smith, Stephen Webster, and Peter Nowlan "
                   "(the town report's twelve-name list is the "
                   "stale 2022 slate; the certified listing "
                   "governs)")],
           [holder("Dennis Brown", "dennis-brown"),
            holder("Kristin Chandler", "kristin-chandler"),
            holder("Kristen Gage", "kristen-gage"),
            holder("Thomas Harty", "thomas-harty"),
            holder("Emery Mattheis", "emery-mattheis"),
            holder("Ceciele Smith", "ceciele-smith"),
            holder("Stephen Webster", "stephen-webster"),
            holder("Peter Nowlan", "peter-nowlan")]),
], jp=jp_election("randolph-vt", "Town of Randolph", 8,
                  "the certified listing names eight winners "
                  "for Randolph's eight justice of the peace "
                  "seats"))

# ----------------------------------------------------------------
# Town of Reading (Windsor County) -- general law.
RDG_REPORT_C = ("Town of Reading, Town Report Fiscal Year "
                "Ending 2024, 'Elected Officials March 2024' "
                "table")
RDG_WARN_C = ("Town of Reading, 2026 Warning (printed in the "
              "February 2026 Informer): Article 1 elects by "
              "Australian ballot on March 3, 2026 a Moderator "
              "(one year), Town Clerk (three years), Town "
              "Treasurer (three years), a Selectperson (three "
              "years), Trustees of Public Funds, a Cemetery "
              "Commissioner, and Library Trustees; Article 3 "
              "elects the Treasurer as collector of delinquent "
              "taxes; Articles 5 and 6 ask the voters to "
              "authorize appointing the Treasurer and the Clerk")
SPECS["reading"] = spec("reading", "Town of Reading", [
    office("moderator", "Town Moderator",
           "Town of Reading Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for "
                                  "a one-year term"),
            S(RDG_FEB26, f"{RDG_WARN_C}. Rayna Bishop held the "
                         "seat to 2026; the 2026 outcome is "
                         "published nowhere official, so the "
                         "post is created without a membership")]),
    office("town-clerk", "Town Clerk",
           "Town of Reading Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(RDG_REPORT, f"{RDG_REPORT_C}: Calista Brennan, "
                          "Town Clerk on a three-year term "
                          "expiring at the 2026 meeting"),
            S(RDG_FEB26, f"{RDG_WARN_C}"),
            S(RDG_APR26, "Town of Reading, April 2026 Informer "
                         "(Selectboard minutes, March 9, 2026): "
                         "the board took up hiring a Town Clerk "
                         "and Town Treasurer after the meeting, "
                         "and by July 2026 the minutes are "
                         "submitted by an Assistant Town Clerk. "
                         "No winner or appointee for the "
                         "clerkship is named in any published "
                         "official source, so the post is created "
                         "without a membership (flagged)")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Reading Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(RDG_REPORT, f"{RDG_REPORT_C}: Calista Brennan, "
                          "Town Treasurer on a three-year term "
                          "expiring at the 2026 meeting"),
            S(RDG_FEB26, f"{RDG_WARN_C}"),
            S(RDG_APR26, "Town of Reading, April 2026 Informer "
                         "(Selectboard minutes, March 9, 2026): "
                         "as for the clerkship, no winner or "
                         "appointee for the treasurership is "
                         "named in any published official "
                         "source, so the post is created without "
                         "a membership (flagged)")]),
    office("selectboard", "Selectboard Member",
           "Town of Reading Selectboard", 3,
           [sb_dir("lists one Reading selectboard member, "
                   "Michael Sanderson (the directory prints a "
                   "single row for Reading)"),
            S(RDG_REPORT, f"{RDG_REPORT_C}: the selectboard was "
                          "Robert Allen, Robert Hartnett, and "
                          "Lisa Silvester; Hartnett's three-year "
                          "seat ended at the 2026 meeting"),
            S(RDG_APR26, "Town of Reading, April 2026 Informer "
                         "(Selectboard minutes, March 9, 2026): "
                         "the board thanked Robert Hartnett for "
                         "three years of service and welcomed "
                         "Mike Sanderson; the board sits as "
                         "Robert Allen (Chair), Lisa Silvester, "
                         "and Mike Sanderson")],
           [holder("Robert Allen", "robert-allen"),
            holder("Lisa Silvester", "lisa-silvester"),
            holder("Mike Sanderson", "mike-sanderson")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Reading Trustees of Public Funds", 3,
           [statute2646("towns elect trustees of public funds"),
            S(RDG_REPORT, f"{RDG_REPORT_C}: trustee Gary "
                          "Vittum serves to 2027; the 2026 "
                          "three-year seat and a two-year seat "
                          "also stood in 2026 and their winners "
                          "are published nowhere official (two "
                          "seats unfilled)"),
            S(RDG_FEB26, f"{RDG_WARN_C}")],
           [holder("Gary Vittum", "gary-vittum")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Reading Cemetery Commission", 3,
           [S(RDG_REPORT, f"{RDG_REPORT_C}: cemetery "
                          "commissioner Adam Kozlowski serves "
                          "to 2027; the seats expiring in 2025 "
                          "and 2026 have no published outcomes "
                          "(two seats unfilled)"),
            S(RDG_FEB26, f"{RDG_WARN_C}")],
           [holder("Adam Kozlowski", "adam-kozlowski")]),
    office("library-trustee", "Library Trustee",
           "Reading Public Library Board of Trustees", 5,
           [S(RDG_REPORT, f"{RDG_REPORT_C}: the library "
                          "trustees are five on staggered "
                          "five-year terms: Vanessa Maxham (to "
                          "2027), Janet Malcolm (to 2028), and "
                          "Heather Evans (to 2029); the 2026 "
                          "five-year seat and warned one- and "
                          "two-year seats have no published "
                          "winners (two seats unfilled)"),
            S(RDG_FEB26, f"{RDG_WARN_C}")],
           [holder("Vanessa Maxham", "vanessa-maxham"),
            holder("Janet Malcolm", "janet-malcolm"),
            holder("Heather Evans", "heather-evans")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Reading Justices of the Peace", 5,
           [jp_src("lists five Reading justices of the peace: "
                   "Rayna Bishop, Robert Hartnett, Jonathan "
                   "Springer, Mary Springer, and Steven Vogl "
                   "(the 2024 town table's Robin French did not "
                   "survive the November 2024 election; the "
                   "certified listing governs)")],
           [holder("Rayna Bishop", "rayna-bishop"),
            holder("Robert Hartnett", "robert-hartnett"),
            holder("Jonathan Springer", "jonathan-springer"),
            holder("Mary Springer", "mary-springer"),
            holder("Steven Vogl", "steven-vogl")]),
], jp=jp_election("reading-vt", "Town of Reading", 5,
                  "the certified listing names five winners for "
                  "Reading's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Readsboro (Bennington County) -- ch. 141 merger
# charter; officers follow general law. The town publishes no
# 2026 election results.
RDS_REPORT_C = ("Town of Readsboro, 2025 Town Report, READSBORO "
                "TOWN OFFICERS table")
RDS_POS_C = ("Town of Readsboro, 'Positions for Election March "
             "2026' (readsborovt.org): the offices standing in "
             "2026 are a Selectboard three-year seat, a Library "
             "Trustee five-year seat, a Cemetery Commissioner "
             "five-year seat, Moderator, Town Clerk (three "
             "years), and Town Treasurer (three years); no Town "
             "Agent, lister, or auditor position is listed")
SPECS["readsboro"] = spec("readsboro", "Town of Readsboro", [
    office("moderator", "Town Moderator",
           "Town of Readsboro Town Moderator", 1,
           [charter141("the Readsboro charter makes the "
                       "Selectboard the legislative body and "
                       "leaves town officers to general law"),
            statute2646_structure("towns elect a moderator for "
                                  "a one-year term"),
            S(RDS_POS, f"{RDS_POS_C}. Bill LeQuier held the "
                       "seat to 2026 per the town officers "
                       "table; the 2026 outcome is published "
                       "nowhere official, so the post is created "
                       "without a membership")]),
    office("town-clerk", "Town Clerk",
           "Town of Readsboro Town Clerk", 1,
           [charter141("town officers follow general law under "
                       "the merger charter"),
            statute2646("towns elect a town clerk"),
            S(RDS_REPORT, f"{RDS_REPORT_C}: Amber Holland, "
                          "Town Clerk on a term expiring at the "
                          "2026 meeting"),
            S(RDS_POS, f"{RDS_POS_C}"),
            S(RDS_MIN, "Town of Readsboro, minutes of the "
                       "March 2, 2026 annual meeting (adopted): "
                       "the promised election results do not "
                       "appear in the minutes; Amber Holland "
                       "still acted as clerk on March 24, 2026"),
            S(RDS_INFO, "Town of Readsboro, Town Info page "
                        "(readsborovt.org): the current Town "
                        "Clerk is Cheryl Green. With Holland's "
                        "elected term expired, no 2026 winner "
                        "published, and the town having "
                        "advertised the combined Clerk/Treasurer "
                        "position as a job, Green is recorded as "
                        "appointed (disclosed inference, batch-18 "
                        "Plainfield pattern)")],
           [holder("Cheryl Green", "cheryl-green",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Readsboro Town Treasurer", 1,
           [charter141("town officers follow general law under "
                       "the merger charter"),
            statute2646("towns elect a town treasurer"),
            S(RDS_REPORT, f"{RDS_REPORT_C}: Amber Holland, "
                          "Town Treasurer on a term expiring at "
                          "the 2026 meeting"),
            S(RDS_INFO, "Town of Readsboro, Town Info page "
                        "(readsborovt.org): the current Town "
                        "Treasurer is Cheryl Green; recorded "
                        "as appointed on the same disclosed "
                        "inference as the clerkship")],
           [holder("Cheryl Green", "cheryl-green",
                   how_seated="appointed")]),
    office("selectboard", "Selectboard Member",
           "Town of Readsboro Selectboard", 3,
           [sb_dir("lists Readsboro's three selectboard members: "
                   "Joseph Berard, Raymond Eilers, and "
                   "Bartholomew Howes"),
            S(RDS_BOARDS, "Town of Readsboro, Boards & "
                          "Commissions page (readsborovt.org): "
                          "Joseph Berard (Chair), Raymond "
                          "Eilers (Vice Chair), and Bartholomew "
                          "Howes. Nathan Kurz's term expired in "
                          "2026 and the one standing three-year "
                          "seat was Howes's")],
           [holder("Joseph Berard", "joseph-berard"),
            holder("Raymond Eilers", "raymond-eilers"),
            holder("Bartholomew Howes", "bartholomew-howes")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Readsboro Collector of Delinquent Taxes", 1,
           [S(RDS_REPORT, f"{RDS_REPORT_C}: Teddy Hopkins, "
                          "Collector of Delinquent Taxes, "
                          "'Appointed April 2017'"),
            S(RDS_INFO, "Town of Readsboro, Town Info page "
                        "(readsborovt.org): 'Ted Hopkins - "
                        "Delinquent Taxes'")],
           [holder("Teddy Hopkins", "teddy-hopkins",
                   how_seated="appointed")]),
    office("library-trustee", "Library Trustee",
           "Readsboro Community Library Board of Trustees", 5,
           [S(RDS_REPORT, f"{RDS_REPORT_C}: the library "
                          "trustees are five on staggered "
                          "five-year terms: Mary Angus (to "
                          "2027), Kayla Royce (to 2028), Diane "
                          "Marchegiani (to 2029), and Meghan "
                          "Deblois (to 2030); Rose Bolognani's "
                          "seat expired in 2026 with no "
                          "published outcome (unfilled)"),
            S(RDS_POS, f"{RDS_POS_C}")],
           [holder("Mary Angus", "mary-angus"),
            holder("Kayla Royce", "kayla-royce"),
            holder("Diane Marchegiani", "diane-marchegiani"),
            holder("Meghan Deblois", "meghan-deblois")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Readsboro Cemetery Commission", 5,
           [S(RDS_REPORT, f"{RDS_REPORT_C}: cemetery "
                          "commissioners Forrest Hicks, Al "
                          "Zander, Eunice Crowell, Devon "
                          "Carrier, and Tom Dente (to 2029)"),
            S(RDS_BOARDS, "Town of Readsboro, Boards & "
                          "Commissions page (readsborovt.org): "
                          "the current commission names Forrest "
                          "Hicks (whose seat stood in 2026; "
                          "recorded as continuing, incumbent "
                          "continuity disclosed), Albert "
                          "Zander, Eunice Crowell, Devon "
                          "Carrier, and Al Bachand. Bachand "
                          "sits in Dente's seat, whose term ran "
                          "to 2029, so he is recorded as "
                          "appointed to the mid-term vacancy "
                          "(instrument unpublished, disclosed)")],
           [holder("Forrest Hicks", "forrest-hicks"),
            holder("Albert Zander", "albert-zander"),
            holder("Eunice Crowell", "eunice-crowell"),
            holder("Devon Carrier", "devon-carrier"),
            holder("Al Bachand", "al-bachand",
                   how_seated="appointed")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Readsboro Justices of the Peace", 5,
           [jp_src("lists five Readsboro justices of the peace: "
                   "Raymond Eilers, Normajean Marchegiani, "
                   "Richard Codogni, Rhonda Eilers Smith, and "
                   "Bruce Busa"),
            S(RDS_REPORT, f"{RDS_REPORT_C}: the town table names "
                          "the same five justices of the peace; "
                          "the two sources are in exact "
                          "agreement")],
           [holder("Richard Codogni", "richard-codogni"),
            holder("Raymond Eilers", "raymond-eilers"),
            holder("Bruce Busa", "bruce-busa"),
            holder("Normajean Marchegiani",
                   "normajean-marchegiani"),
            holder("Rhonda Eilers Smith", "rhonda-eilers-smith")]),
], jp=jp_election("readsboro-vt", "Town of Readsboro", 5,
                  "the certified listing names five winners for "
                  "Readsboro's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Richford (Franklin County) -- ch. 142 merger charter
# (village abolished effective January 1, 1999); officers are
# general-law under section 202(a); the Treasurer collects taxes
# under section 203, so there is no separate collector post.
RFR_REPORT_C = ("Town of Richford, 2025 Town Report, TOWN "
                "OFFICERS table (report p. 7); the 2026 warning "
                "is printed at report p. 9 (floor meeting March "
                "2, 2026; ballot March 3, 2026)")
RFR_WARN_C = ("the 2026 warning, Article 2, elects a Moderator "
              "(one year), a Selectman for two years, a "
              "Selectman for three years, two Listers (three "
              "years), a First Constable (one year), four "
              "Planning Commission members (three years), and "
              "three Directors of the Richford Community Fund "
              "Inc (three years)")
SPECS["richford"] = spec("richford", "Town of Richford", [
    office("moderator", "Town Moderator",
           "Town of Richford Town Moderator", 1,
           [charter142("section 202(a): town officers are those "
                       "provided by general law"),
            statute2646_structure("towns elect a moderator for "
                                  "a one-year term"),
            S(RFR_REPORT, f"{RFR_REPORT_C}: Marianne Hall, "
                          "Moderator on a one-year term; "
                          f"{RFR_WARN_C}. The 2026 outcome is "
                          "published nowhere official, so the "
                          "post is created without a membership")]),
    office("town-clerk", "Town Clerk",
           "Town of Richford Town Clerk", 1,
           [charter142("section 202(a): town officers are those "
                       "provided by general law"),
            statute2646("towns elect a town clerk"),
            S(RFR_REPORT, f"{RFR_REPORT_C}: Kiley Deuso, Town "
                          "Clerk on a three-year term to 2027; "
                          "the seat did not stand in 2026"),
            guide("lists Kiley Deuso as Richford's Town Clerk")],
           [holder("Kiley Deuso", "kiley-deuso")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Richford Town Treasurer", 1,
           [charter142("section 202(a): town officers are those "
                       "provided by general law; section 203 "
                       "makes the Treasurer the collector of "
                       "taxes ('The Town shall not elect other "
                       "collectors of current or delinquent "
                       "taxes'), so Richford has no separate "
                       "collector of delinquent taxes post"),
            statute2646("towns elect a town treasurer"),
            S(RFR_REPORT, f"{RFR_REPORT_C}: Kiley Deuso, Town "
                          "Treasurer on a three-year term to "
                          "2027; the seat did not stand in 2026"),
            guide("lists Kiley Deuso as Richford's Town "
                  "Treasurer")],
           [holder("Kiley Deuso", "kiley-deuso")]),
    office("selectboard", "Selectboard Member",
           "Town of Richford Selectboard", 5,
           [sb_dir("lists four of Richford's five selectboard "
                   "members: Joseph Desmarais, Stephen Fletcher, "
                   "Kristin Murphy, and Wallace Steinhour"),
            S(RFR_SB, "Town of Richford, Select Board page "
                      "(richfordvt.org): the current board is "
                      "Wallace Steinhour (Chair), Alan Fletcher "
                      "(Vice Chair), Joseph Desmarais, Stephen "
                      "Fletcher, and Kristin Murphy (the report "
                      "table spells the chair 'Steinour'; the "
                      "board page's Steinhour governs). The two "
                      "seats that stood in 2026 were held by "
                      "Sherry Paquette and Andrew Pond, who "
                      "departed")],
           [holder("Wallace Steinhour", "wallace-steinhour"),
            holder("Alan Fletcher", "alan-fletcher"),
            holder("Joseph Desmarais", "joseph-desmarais"),
            holder("Stephen Fletcher", "stephen-fletcher"),
            holder("Kristin Murphy", "kristin-murphy")]),
    office("lister", "Lister",
           "Town of Richford Board of Listers", 3,
           [statute2646("towns elect a board of listers of three "
                        "on staggered three-year terms"),
            S(RFR_REPORT, f"{RFR_REPORT_C}: lister Eric Collins "
                          f"serves to 2027; {RFR_WARN_C} -- two "
                          "lister seats stood in 2026"),
            S(RFR_DIR, "Town of Richford, Municipal Directory "
                       "(richfordvt.org): Jon Hancock is a "
                       "current lister. One of the two seats "
                       "that stood in 2026 remains unfilled")],
           [holder("Eric Collins", "eric-collins"),
            holder("Jon Hancock", "jon-hancock")]),
    office("first-constable", "First Constable",
           "Town of Richford First Constable", 1,
           [statute2646("towns elect a first constable for a "
                        "one-year term"),
            S(RFR_REPORT, f"{RFR_REPORT_C}: Jeremy Paquette, "
                          f"First Constable; {RFR_WARN_C}. The "
                          "2026 outcome is published nowhere "
                          "official, so the post is created "
                          "without a membership")]),
    office("planning-commissioner", "Planning Commissioner",
           "Town of Richford Planning Commission", 7,
           [S(RFR_PC, "Town of Richford, Planning Commission "
                      "page (richfordvt.org): the commission is "
                      "elected in Richford (the 2026 warning "
                      "elects four members to three-year terms) "
                      "and currently sits as Laura Hancock "
                      "(Chair), Jacques Desautels, Arthur Pond, "
                      "Mark Waterhouse, Rachel Dollar, Karen "
                      "Cangelosi, and Sherry Paquette; Marc "
                      "Jaffee departed")],
           [holder("Laura Hancock", "laura-hancock"),
            holder("Jacques Desautels", "jacques-desautels"),
            holder("Arthur Pond", "arthur-pond"),
            holder("Mark Waterhouse", "mark-waterhouse"),
            holder("Rachel Dollar", "rachel-dollar"),
            holder("Karen Cangelosi", "karen-cangelosi"),
            holder("Sherry Paquette", "sherry-paquette")]),
    office("community-fund-director",
           "Richford Community Fund Director",
           "Richford Community Fund Board of Directors", 5,
           [S(RFR_REPORT, f"{RFR_REPORT_C}: the Directors of "
                          "the Richford Community Fund Inc are "
                          "five (Alan Fletcher, Marissa Tessier, "
                          "Beth O'Brian, Ginger Morse, and one "
                          f"vacant seat); {RFR_WARN_C} -- three "
                          "seats stood in 2026 and no current "
                          "roster is published, so the post is "
                          "created without memberships")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Richford Justices of the Peace", 10,
           [jp_src("lists ten Richford justices of the peace: "
                   "Eric Collins, Mary Finola Cournane, Alan "
                   "Fletcher, Timothy Greene, Morton H. "
                   "Greenwood, Ann Lavery, Noela McGroarty, "
                   "Daniel Newton, Mary Robinson, and Heidi "
                   "Tessier (the town report omits Greene and "
                   "misspells Newton as 'Danial'; the certified "
                   "listing governs)")],
           [holder("Eric Collins", "eric-collins"),
            holder("Mary Finola Cournane",
                   "mary-finola-cournane"),
            holder("Alan Fletcher", "alan-fletcher"),
            holder("Timothy Greene", "timothy-greene"),
            holder("Morton H. Greenwood", "morton-h-greenwood"),
            holder("Ann Lavery", "ann-lavery"),
            holder("Noela McGroarty", "noela-mcgroarty"),
            holder("Daniel Newton", "daniel-newton"),
            holder("Mary Robinson", "mary-robinson"),
            holder("Heidi Tessier", "heidi-tessier")]),
], jp=jp_election("richford-vt", "Town of Richford", 10,
                  "the certified listing names ten winners for "
                  "Richford's ten justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Richmond (Chittenden County) -- ch. 143 charter:
# section 302(c) provides the town shall not have a Road
# Commissioner, Town Agent, Town Auditor, or Town Grand Juror;
# section 303(b) makes the collector of delinquent taxes
# Selectboard-appointed; section 902 Water & Sewer
# Commissioners are appointed; section 501 fixes a five-member
# Selectboard.
RMD_REPORT_C = ("Town of Richmond, 2025 Town Report, ELECTED "
                "and APPOINTED officials tables")
RMD_MEMBERS_C = ("Town of Richmond, All Committee & Board "
                 "Members page (richmondvt.gov): the town's "
                 "current roster, with Elected/Appointment types "
                 "and term dates")
SPECS["richmond"] = spec("richmond", "Town of Richmond", [
    office("moderator", "Town Moderator",
           "Town of Richmond Town Moderator", 1,
           [charter143("the charter leaves the moderator to "
                       "general law; section 302(c) provides "
                       "the town shall not have a Road "
                       "Commissioner, Town Agent, Town Auditor, "
                       "or Town Grand Juror, so no posts are "
                       "created for those offices"),
            statute2646_structure("towns elect a moderator for "
                                  "a one-year term"),
            S(RMD_REPORT, f"{RMD_REPORT_C}: Clinton Buxton, "
                          "Moderator on a one-year term "
                          "expiring at the 2026 meeting. The "
                          "2026 outcome is published nowhere "
                          "official, so the post is created "
                          "without a membership")]),
    office("town-clerk", "Town Clerk",
           "Town of Richmond Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(RMD_REPORT, f"{RMD_REPORT_C}: Susanne Parent, "
                          "Town Clerk, won the contested 2025 "
                          "race (502-485 over Katie Nelson) for "
                          "a term to 2028"),
            S(RMD_CLERK, "Town of Richmond, Town Clerk page "
                         "(richmondvt.gov): Susanne Parent is "
                         "the Town Clerk")],
           [holder("Susanne Parent", "susanne-parent")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Richmond Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(RMD_REPORT, f"{RMD_REPORT_C}: James Feinson, "
                          "Town Treasurer, re-elected in 2025 "
                          "unopposed for a term to 2028"),
            guide("lists James Feinson as Richmond's Town "
                  "Treasurer")],
           [holder("James Feinson", "james-feinson")]),
    office("selectboard", "Selectboard Member",
           "Town of Richmond Selectboard", 5,
           [charter143("section 501: the Selectboard has five "
                       "members, one three-year and one "
                       "two-year seat elected each year"),
            sb_dir("lists Richmond's five selectboard members: "
                   "Caitlin Filkins, David Sander, Bard Hill, "
                   "Gregory Rabideau, and Adam Wood"),
            S(RMD_MEMBERS, f"{RMD_MEMBERS_C}: Adam Wood (Chair, "
                           "2026-2028), Caitlin Filkins (Vice "
                           "Chair, 2025-2027), Greg Rabideau "
                           "(2024-2027), Bard Hill (2025-2028), "
                           "and David Sander (2026-2029), each "
                           "typed Elected. Rabideau's history "
                           "is disclosed: the town report styles "
                           "him 'Appointed Mid-Term Until Town "
                           "Meeting 3/3/2026', and the town's "
                           "current members page carries him as "
                           "Elected for the seat running to "
                           "2027, so he is recorded as elected")],
           [holder("Adam Wood", "adam-wood"),
            holder("Caitlin Filkins", "caitlin-filkins"),
            holder("Greg Rabideau", "greg-rabideau"),
            holder("Bard Hill", "bard-hill"),
            holder("David Sander", "david-sander")]),
    office("constable", "Constable",
           "Town of Richmond Constable", 1,
           [statute2646("towns elect constables"),
            S(RMD_REPORT, f"{RMD_REPORT_C}: Andy Squires held "
                          "the elected one-year constable "
                          "office to 2026. The 2026 outcome is "
                          "published nowhere official, so the "
                          "post is created without a membership")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Richmond Collector of Delinquent Taxes", 1,
           [charter143("section 303(b): the collector of "
                       "delinquent taxes is appointed by the "
                       "Selectboard"),
            S(RMD_REPORT, f"{RMD_REPORT_C}: the APPOINTED "
                          "officials table names Laurie Brisbin "
                          "as Collector of Delinquent Taxes")],
           [holder("Laurie Brisbin", "laurie-brisbin",
                   how_seated="appointed")]),
    office("library-trustee", "Library Trustee",
           "Richmond Free Library Board of Trustees", 5,
           [S(RMD_MEMBERS, f"{RMD_MEMBERS_C}: the Richmond Free "
                           "Library trustees are five on "
                           "five-year terms, each typed Elected: "
                           "Ellen Crary (2026-2031), Amy Klinger "
                           "(2025-2030), Dana Van Horn "
                           "(2024-2029), Matthew Crabb "
                           "(2023-2028), and Amy Wardwell "
                           "(2022-2027)")],
           [holder("Ellen Crary", "ellen-crary"),
            holder("Amy Klinger", "amy-klinger"),
            holder("Dana Van Horn", "dana-van-horn"),
            holder("Matthew Crabb", "matthew-crabb"),
            holder("Amy Wardwell", "amy-wardwell")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Richmond Justices of the Peace", 12,
           [jp_src("lists twelve Richmond justices of the "
                   "peace: Aimee Alexander, Denise Barnard, "
                   "Andrew Bessette, Heather Chadwick, Francis "
                   "Churchill, Joel Furr, Mary Houle, Keith "
                   "Kasper, Matthew Moultroup, Michael Parent, "
                   "Marshall Paulsen, and Becky Vigneault (the "
                   "town report's garbled 'Denise Begins "
                   "Barnard' is the listing's Denise Barnard)")],
           [holder("Aimee Alexander", "aimee-alexander"),
            holder("Denise Barnard", "denise-barnard"),
            holder("Andrew Bessette", "andrew-bessette"),
            holder("Heather Chadwick", "heather-chadwick"),
            holder("Francis Churchill", "francis-churchill"),
            holder("Joel Furr", "joel-furr"),
            holder("Mary Houle", "mary-houle"),
            holder("Keith Kasper", "keith-kasper"),
            holder("Matthew Moultroup", "matthew-moultroup"),
            holder("Michael Parent", "michael-parent"),
            holder("Marshall Paulsen", "marshall-paulsen"),
            holder("Becky Vigneault", "becky-vigneault")]),
], jp=jp_election("richmond-vt", "Town of Richmond", 12,
                  "the certified listing names twelve winners "
                  "for Richmond's twelve justice of the peace "
                  "seats"))

# ----------------------------------------------------------------
# Town of Ripton (Addison County) -- general law. Sources: the
# town website (several rosters live in the pages' raw HTML)
# and the 2025 Town Report (warning + officers tables), read
# from the town's own Google Drive reports folder.
RIP_REPORT_C = ("Town of Ripton, 2025 Town Report: the signed "
                "2026 warning (floor meeting March 2, 2026; "
                "Australian ballot March 3, 2026, Article 9) and "
                "the Elected and Appointed Town Officers tables")
RIP_WARN_C = ("Article 9 elects a Selector (three years), a "
              "Moderator (one year), a Delinquent Tax Collector "
              "(one year), a Lister (three years), a Cemetery "
              "Commissioner (five years), and a Constable (one "
              "year); no auditor, grand juror, town agent, or "
              "trustee of public funds stands")
SPECS["ripton"] = spec("ripton", "Town of Ripton", [
    office("moderator", "Town Moderator",
           "Town of Ripton Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for "
                                  "a one-year term"),
            S(RIP_REPORT, f"{RIP_REPORT_C}: Tim O'Leary, "
                          f"Moderator; {RIP_WARN_C}. The 2026 "
                          "outcome is published nowhere "
                          "official, so the post is created "
                          "without a membership")]),
    office("town-clerk", "Town Clerk",
           "Town of Ripton Town Clerk", 1,
           [statute2646("towns elect a town clerk unless the "
                        "town has voted to authorize appointment "
                        "under 17 V.S.A. section 2651e"),
            S(RIP_REPORT, f"{RIP_REPORT_C}: the officers tables "
                          "place Alison Joseph Dickinson in the "
                          "Appointed table ('Town Admin/Clerk'), "
                          "not the Elected table, and the office "
                          "did not stand on the 2026 ballot; she "
                          "serves as Town Clerk by appointment. "
                          "The conversion instrument was not "
                          "located (disclosed)"),
            guide("lists Alison Joseph Dickinson as Ripton's "
                  "Town Clerk")],
           [holder("Alison Joseph Dickinson",
                   "alison-joseph-dickinson",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Ripton Town Treasurer", 1,
           [statute2646("towns elect a town treasurer unless "
                        "the town has voted to authorize "
                        "appointment under 17 V.S.A. section "
                        "2651f"),
            S(RIP_TREAS, "Town of Ripton, Treasurer page "
                         "(riptonvermont.org): the treasurer "
                         "has been appointed by the Selectboard "
                         "since 2018; Carolyn Smith is the Town "
                         "Treasurer"),
            S(RIP_REPORT, f"{RIP_REPORT_C}: Carolyn Smith "
                          "appears in the Appointed officers "
                          "table as Treasurer")],
           [holder("Carolyn Smith", "carolyn-smith",
                   how_seated="appointed")]),
    office("selectboard", "Selectboard Member",
           "Town of Ripton Selectboard", 3,
           [sb_dir("lists Ripton's three selectboard members: "
                   "Giles Hoyler, William Hunsinger, and 'H "
                   "Wilcox' (the directory truncates her given "
                   "name)"),
            S(RIP_SB, "Town of Ripton, Selectboard page "
                      "(riptonvermont.org): Giles Hoyler "
                      "(Chair), Bill Hunsinger, and Brooke "
                      "Wilcox; Laureen 'Laurie' Cox retired at "
                      "the 2026 meeting after 40 years")],
           [holder("Giles Hoyler", "giles-hoyler"),
            holder("William Hunsinger", "william-hunsinger"),
            holder("Brooke Wilcox", "brooke-wilcox")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Ripton Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes for a one-year term"),
            S(RIP_TREAS, "Town of Ripton, Treasurer page "
                         "(riptonvermont.org): 'Carolyn Smith "
                         "is the Delinquent Tax Collector'. The "
                         "office stands on the ballot annually; "
                         "she is recorded as the continuing "
                         "elected collector (incumbent "
                         "continuity, disclosed)"),
            S(RIP_REPORT, f"{RIP_REPORT_C}: {RIP_WARN_C}")],
           [holder("Carolyn Smith", "carolyn-smith")]),
    office("lister", "Lister",
           "Town of Ripton Board of Listers", 3,
           [statute2646("towns elect a board of listers of "
                        "three on staggered three-year terms"),
            S(RIP_LIST, "Town of Ripton, Listers page "
                        "(riptonvermont.org): the listers are "
                        "Alison Joseph Dickinson, Erik Eriksen, "
                        "and Beth Eliason (the full names appear "
                        "in the page's underlying text)"),
            S(RIP_REPORT, f"{RIP_REPORT_C}: Dickinson's lister "
                          "seat stood in 2026; the town's "
                          "current listers page still names all "
                          "three, so she is recorded as "
                          "continuing (incumbent continuity, "
                          "disclosed)")],
           [holder("Alison Joseph Dickinson",
                   "alison-joseph-dickinson"),
            holder("Erik Eriksen", "erik-eriksen"),
            holder("Beth Eliason", "beth-eliason")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Ripton Cemetery Commission", 5,
           [S(RIP_CEM, "Town of Ripton, Cemetery Commission page "
                       "(riptonvermont.org): the commission is "
                       "five: Elizabeth Walker (Co-Chair, to "
                       "2027), Samantha Smith (2028), Bonnie "
                       "Swan (2029), and Karen Heppell "
                       "(Co-Chair, to 2030), with the seat "
                       "ending in 2026 unfilled"),
            S(RIP_REPORT, f"{RIP_REPORT_C}: the report's "
                          "officers table gives the 2028 "
                          "commissioner as Samantha Smith Lau "
                          "and names Carole Cummings for the "
                          "seat ending 2026, where the website "
                          "table names Meredyth Harple; no 2026 "
                          "outcome is published, so that seat "
                          "is unfilled (the divergence is "
                          "flagged)")],
           [holder("Elizabeth Walker", "elizabeth-walker"),
            holder("Samantha Smith Lau", "samantha-smith-lau"),
            holder("Bonnie Swan", "bonnie-swan"),
            holder("Karen Heppell", "karen-heppell")]),
    office("constable", "Constable",
           "Town of Ripton Constable", 1,
           [statute2646("towns elect constables for one-year "
                        "terms"),
            S(RIP_REPORT, f"{RIP_REPORT_C}: Chris Smith, "
                          f"Constable to 2026; {RIP_WARN_C}. The "
                          "2026 outcome is published nowhere "
                          "official, so the post is created "
                          "without a membership")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Ripton Justices of the Peace", 5,
           [jp_src("lists five Ripton justices of the peace: "
                   "Alexander Cox, Jenna Hunsinger, Richard Kim "
                   "Kimler, Amy McGlashan, and Norm Tjossem. "
                   "McGlashan vacated the seat in 2025 (see the "
                   "election note); Irene Poole was appointed "
                   "in her place and holds an appointed "
                   "membership with no candidacy")],
           [holder("Alexander Cox", "alexander-cox"),
            holder("Jenna Hunsinger", "jenna-hunsinger"),
            holder("Richard Kim Kimler", "richard-kim-kimler"),
            holder("Norm Tjossem", "norm-tjossem"),
            holder("Irene Poole", "irene-poole",
                   how_seated="appointed", no_candidacy=True)]),
], jp=jp_election("ripton-vt", "Town of Ripton", 5,
                  "the certified listing names five winners for "
                  "Ripton's five justice of the peace seats; "
                  "one winner, Amy McGlashan, vacated the seat "
                  "in 2025 and is not recorded (the 2025 Town "
                  "Report's justice list shows Irene Poole "
                  "'appointed 2025' in her place); the winners "
                  "list holds the four surviving elected "
                  "justices while vote_for stays at the slate "
                  "size, per the Enosburgh/Maidstone/Pomfret "
                  "pattern",
                  extra_sources=[S(RIP_REPORT,
                                   f"{RIP_REPORT_C}: the "
                                   "report's justice of the "
                                   "peace list shows Irene Poole "
                                   "appointed in 2025 and does "
                                   "not list McGlashan")]))

# ----------------------------------------------------------------
# Town of Rochester (Windsor County) -- general law. Sources:
# the FY2025 Town Report Elected Officials table and the town's
# DRAFT minutes of the March 2, 2026 annual floor meeting
# (draft status disclosed; the White River Valley Herald's
# meeting report concurs on every outcome).
ROC_REPORT_C = ("Town of Rochester, FY2025 Town Report, "
                "Elected Officials table")
ROC_MIN_C = ("Town of Rochester, DRAFT Minutes of the Annual "
             "Town Meeting, March 2, 2026 (draft status "
             "disclosed; the White River Valley Herald's "
             "report of the meeting concurs on every outcome)")
SPECS["rochester"] = spec("rochester", "Town of Rochester", [
    office("moderator", "Town Moderator",
           "Town of Rochester Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(ROC_MIN, f"{ROC_MIN_C}: Dan McKinley was "
                       "re-elected Moderator")],
           [holder("Dan McKinley", "dan-mckinley")]),
    office("town-clerk", "Town Clerk",
           "Town of Rochester Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(ROC_REPORT, f"{ROC_REPORT_C}: Julie Smith, Town "
                          "Clerk on a term to 2028; the seat "
                          "did not stand in 2026"),
            guide("lists Julie Smith as Rochester's Town "
                  "Clerk")],
           [holder("Julie Smith", "julie-smith")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Rochester Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(ROC_REPORT, f"{ROC_REPORT_C}: Julie Smith, Town "
                          "Treasurer on a term to 2028; the "
                          "seat did not stand in 2026"),
            guide("lists Julie Smith as Rochester's Town "
                  "Treasurer")],
           [holder("Julie Smith", "julie-smith")]),
    office("selectboard", "Selectboard Member",
           "Town of Rochester Selectboard", 3,
           [sb_dir("lists Rochester's three selectboard "
                   "members: Mary Fratini, Patricia Harvey, and "
                   "Michael Teetsel"),
            S(ROC_MIN, f"{ROC_MIN_C}: Mary Fratini won the "
                       "three-year seat that Chad Richardson "
                       "had held (81-19 over Alvina "
                       "Risinger-Harvey); Patricia Harvey "
                       "(Chair, to 2027) and Michael Teetsel "
                       "(to 2028) continue (the report table "
                       "prints 'Pat Harvey' and 'Mike Teetsel')")],
           [holder("Patricia Harvey", "patricia-harvey"),
            holder("Michael Teetsel", "michael-teetsel"),
            holder("Mary Fratini", "mary-fratini")]),
    office("lister", "Lister",
           "Town of Rochester Board of Listers", 3,
           [statute2646("towns elect a board of listers of "
                        "three on staggered three-year terms"),
            S(ROC_REPORT, f"{ROC_REPORT_C}: listers Louis "
                          "Donnet, Jessica Arsenault, and "
                          "Caroline Meagher"),
            S(ROC_MIN, f"{ROC_MIN_C}: Louis Donnet was "
                       "re-elected Lister")],
           [holder("Louis Donnet", "louis-donnet"),
            holder("Jessica Arsenault", "jessica-arsenault"),
            holder("Caroline Meagher", "caroline-meagher")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Rochester Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes"),
            S(ROC_MIN, f"{ROC_MIN_C}: Kristen LaPell was "
                       "re-elected Collector of Delinquent "
                       "Taxes"),
            S(ROC_REPORT, f"{ROC_REPORT_C}: Kristen LaPell, "
                          "Collector of Delinquent Taxes")],
           [holder("Kristen LaPell", "kristen-lapell")]),
    office("library-trustee", "Library Trustee",
           "Rochester Public Library Board of Trustees", 5,
           [S(ROC_REPORT, f"{ROC_REPORT_C}: the library "
                          "trustees are five: Vincent Martinez, "
                          "Melody Balzcon, Barbara Shenton, "
                          "Lauren Scogin, and Natalie Cassidy "
                          "(minutes and report spell 'Balzcon'; "
                          "the Herald's 'Balczon' is the typo)"),
            S(ROC_MIN, f"{ROC_MIN_C}: Vincent Martinez was "
                       "re-elected to a five-year term and "
                       "Melody Balzcon to a two-year remainder "
                       "term")],
           [holder("Vincent Martinez", "vincent-martinez"),
            holder("Melody Balzcon", "melody-balzcon"),
            holder("Barbara Shenton", "barbara-shenton"),
            holder("Lauren Scogin", "lauren-scogin"),
            holder("Natalie Cassidy", "natalie-cassidy")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Rochester Trustees of Public Funds", 3,
           [statute2646("towns elect trustees of public funds"),
            S(ROC_REPORT, f"{ROC_REPORT_C}: trustees Greg "
                          "White, Barbara DeHart, and Linda "
                          "Crosby"),
            S(ROC_MIN, f"{ROC_MIN_C}: Greg White was elected "
                       "Trustee of Public Funds (Michael Harvey "
                       "retired after 30 years)")],
           [holder("Greg White", "greg-white"),
            holder("Barbara DeHart", "barbara-dehart"),
            holder("Linda Crosby", "linda-crosby")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Rochester Cemetery Commission", 5,
           [S(ROC_REPORT, f"{ROC_REPORT_C}: the cemetery "
                          "commissioners are five (the report "
                          "text confirms a 'five-member board "
                          "elected at Town Meeting'): Joe "
                          "Schenkman, Michele Schnabel, Thomas "
                          "Paquette, Nancy Woolley, and Ray "
                          "Harvey"),
            S(ROC_MIN, f"{ROC_MIN_C}: Joe Schenkman was "
                       "re-elected Cemetery Commissioner")],
           [holder("Joe Schenkman", "joe-schenkman"),
            holder("Michele Schnabel", "michele-schnabel"),
            holder("Thomas Paquette", "thomas-paquette"),
            holder("Nancy Woolley", "nancy-woolley"),
            holder("Ray Harvey", "ray-harvey")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Rochester Justices of the Peace", 5,
           [jp_src("lists five Rochester justices of the peace: "
                   "Kevin Dougherty, Michael Harvey, Brenda B "
                   "Goupee, Annette West, and Amy Braun (Braun's "
                   "line spills past a page header in the "
                   "listing, at a Rochester address; the town "
                   "report's five-name slate agrees)"),
            S(ROC_REPORT, f"{ROC_REPORT_C}: the town table "
                          "lists the same five justices; the "
                          "person record uses the report's "
                          "'Brenda Goupee' with the listing's "
                          "'Brenda B Goupee' as the ballot name")],
           [holder("Kevin Dougherty", "kevin-dougherty"),
            holder("Michael Harvey", "michael-harvey"),
            holder("Brenda Goupee", "brenda-goupee",
                   ballot_name="Brenda B Goupee"),
            holder("Annette West", "annette-west"),
            holder("Amy Braun", "amy-braun")]),
], jp=jp_election("rochester-vt", "Town of Rochester", 5,
                  "the certified listing names five winners for "
                  "Rochester's five justice of the peace seats "
                  "(including Amy Braun, whose entry follows a "
                  "page header in the listing)"))

# ----------------------------------------------------------------
# Town of Rockingham (Windham County) -- no Title 24 Appendix
# charter; town-manager form under general law. Sources: the
# 2025 Annual Report's ELECTED OFFICIALS table and the printed
# 2026 warning, read in the town's document library (the site
# is JavaScript-driven); the town posts no 2026 results
# document, and the March 2026 ballot outcomes rest on The
# Commons' report of the March 3, 2026 Australian ballot
# (newspaper class, disclosed).
RKH_REPORT_C = ("Town of Rockingham, 2025 Annual Report (July "
                "1, 2024 - June 30, 2025), 'TOWN OF ROCKINGHAM "
                "ELECTED OFFICIALS 2024-2025' table and the "
                "printed 2026 warning, read in the town's "
                "document library")
RKH_COMMONS_C = ("The Commons, report of the March 3, 2026 "
                 "Rockingham Australian ballot (newspaper "
                 "source, disclosed; the town posts no 2026 "
                 "results document)")
SPECS["rockingham"] = spec("rockingham", "Town of Rockingham", [
    office("moderator", "Town Moderator",
           "Town of Rockingham Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(RKH_COMMONS, f"{RKH_COMMONS_C}: Paul Obuchowski "
                           "was re-elected Moderator, "
                           "uncontested"),
            S(RKH_LIB_DOCS, f"{RKH_REPORT_C}: Paul Obuchowski, "
                            "Moderator (March 2025 - March "
                            "2026). He is also the Village of "
                            "Bellows Falls Village President; "
                            "the membership reuses that person "
                            "record")],
           [holder("Paul Obuchowski", "paul-obuchowski",
                   existing_person_id="ocd-person/6d6d72e1-192d-5297-9e70-0ca72fb41e6f")]),
    office("town-clerk", "Town Clerk",
           "Town of Rockingham Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(RKH_LIB_DOCS, f"{RKH_REPORT_C}: Kathleen Kelly, "
                            "Town Clerk (March 2025 - March "
                            "2028); the seat did not stand in "
                            "2026"),
            S(RKH_CLERK, "Town of Rockingham, Town Clerk page "
                         "(rockinghamvt.org): Kathleen Kelly is "
                         "the Town Clerk. She is also the "
                         "Village of Bellows Falls Village "
                         "Clerk; the membership reuses that "
                         "person record"),
            guide("lists Kathleen Kelly as Rockingham's Town "
                  "Clerk")],
           [holder("Kathleen Kelly", "kathleen-kelly",
                   existing_person_id="ocd-person/415f603f-55ab-5bb4-be75-de1d7971b087")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Rockingham Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(RKH_LIB_DOCS, f"{RKH_REPORT_C}: Kathleen Kelly, "
                            "Town Treasurer (March 2025 - "
                            "March 2028); the seat did not stand "
                            "in 2026"),
            guide("lists Kathleen Kelly as Rockingham's Town "
                  "Treasurer")],
           [holder("Kathleen Kelly", "kathleen-kelly",
                   existing_person_id="ocd-person/415f603f-55ab-5bb4-be75-de1d7971b087")]),
    office("selectboard", "Selectboard Member",
           "Town of Rockingham Selectboard", 5,
           [sb_dir("lists three of Rockingham's five selectboard "
                   "members: Dalila Hall, Amy Howlett, and "
                   "Bonnie North (the directory's Rockingham "
                   "entry is truncated)"),
            S(RKH_SB, "Town of Rockingham, Selectboard page "
                      "(rockinghamvt.org): the current board is "
                      "Rick Cowan, John Dunbar, Amy Howlett, "
                      "Bonnie North, and Dalila Hall"),
            S(RKH_COMMONS, f"{RKH_COMMONS_C}: Amy Howlett won "
                           "a three-year seat (391-73 over "
                           "William Crowther) and Bonnie North "
                           "(315) and Dalila Hall (251) won the "
                           "two one-year seats -- the vacancy "
                           "remainders of the departed Peter "
                           "Golec and Elijah Zimmer -- in an "
                           "eight-candidate field")],
           [holder("Rick Cowan", "rick-cowan"),
            holder("John Dunbar", "john-dunbar"),
            holder("Amy Howlett", "amy-howlett"),
            holder("Bonnie North", "bonnie-north"),
            holder("Dalila Hall", "dalila-hall")]),
    office("lister", "Lister",
           "Town of Rockingham Board of Listers", 3,
           [statute2646("towns elect a board of listers of "
                        "three on staggered three-year terms"),
            S(RKH_LIST, "Town of Rockingham, Lister's Office "
                        "page (rockinghamvt.org): 'The Listers "
                        "are elected to assess property in the "
                        "Town of Rockingham'; the page names "
                        "Paul Noble and Tad Dedrick"),
            S(RKH_COMMONS, f"{RKH_COMMONS_C}: Paul Noble was "
                           "re-elected Lister, uncontested"),
            S(RKH_LIB_DOCS, f"{RKH_REPORT_C}: listers Tad "
                            "Dedrick (2024-2027) and Paul Noble "
                            "(Chair); Michael Stack resigned "
                            "from a term ending in 2025 and no "
                            "successor is published, so the "
                            "third seat is unfilled")],
           [holder("Paul Noble", "paul-noble"),
            holder("Tad Dedrick", "tad-dedrick")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Rockingham Trustees of Public Funds", 3,
           [statute2646("towns elect three trustees of public "
                        "funds on staggered terms"),
            S(RKH_LIB_DOCS, f"{RKH_REPORT_C}: Trustees of "
                            "Public Funds Pat Fowler (to 2028) "
                            "and David Lambert (to 2028); no "
                            "third trustee is named, so one "
                            "seat is unfilled")],
           [holder("Pat Fowler", "patricia-fowler"),
            holder("David Lambert", "david-lambert")]),
    office("library-trustee", "Library Trustee",
           "Rockingham Free Public Library Board of Trustees", 9,
           [S(RKH_LIBBYLAWS, "Rockingham Free Public Library, "
                             "bylaws: the board has nine "
                             "trustees, three elected yearly to "
                             "three-year terms"),
            S(RKH_LIB, "Rockingham Free Public Library, Board "
                       "of Trustees page "
                       "(rockinghamlibrary.org): the current "
                       "trustees are Margo Ghia, Virginia "
                       "Driscoll, Virginia Massucco, Mike Sola, "
                       "Bonnie North, Martha Rowley, and Carol "
                       "Blackwood; two seats are vacant (the "
                       "board's May 21, 2026 agenda carries a "
                       "Board Vacancy item)"),
            S(RKH_COMMONS, f"{RKH_COMMONS_C}: Carol Blackwood "
                           "and Ginny Massucco were elected "
                           "library trustees at the 2026 "
                           "meeting. Blackwood had first joined "
                           "as a 2025 appointee per the town "
                           "report table, and Sola joined as a "
                           "2023 vacancy appointee but sits "
                           "under an elected term in that "
                           "table, so both are recorded as "
                           "elected")],
           [holder("Margo Ghia", "margo-ghia"),
            holder("Virginia Driscoll", "virginia-driscoll"),
            holder("Virginia Massucco", "virginia-massucco"),
            holder("Mike Sola", "mike-sola"),
            holder("Bonnie North", "bonnie-north"),
            holder("Martha Rowley", "martha-rowley"),
            holder("Carol Blackwood", "carol-blackwood")]),
    office("trustee-of-campbell-fund",
           "Trustee of the Campbell Fund",
           "Town of Rockingham Campbell Fund", 1,
           [S(RKH_LIB_DOCS, f"{RKH_REPORT_C}: the elected "
                            "officials table prints a "
                            "'Trustee of the Campbell Fund' "
                            "heading with no holder's name, so "
                            "the post is created without a "
                            "membership")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Rockingham Justices of the Peace", 14,
           [jp_src("lists fourteen Rockingham justices of the "
                   "peace and one 'Vacant' seat: Stuart Brown, "
                   "Carol Buchdahl, Mark Condon, Patricia "
                   "Fowler, Dennis Harty, Amy Howlett, Charlie "
                   "Hunter, Chris Kibbe, Sally MacPhee, Paul "
                   "Obuchowski, Richard O'Donnell, Peter "
                   "Stickney, Gloria Vancor, and Deborah Wright "
                   "(the town report's BCA list agrees; it "
                   "prints 'Chris Kibbee' where the certified "
                   "listing has Kibbe). The post carries "
                   "fourteen filled seats of the fifteen the "
                   "voters fill. Paul Obuchowski and Dennis "
                   "Harty also hold Village of Bellows Falls "
                   "offices; their memberships reuse those "
                   "person records")],
           [holder("Stuart Brown", "stuart-brown"),
            holder("Carol Buchdahl", "carol-buchdahl"),
            holder("Mark Condon", "mark-condon"),
            holder("Patricia Fowler", "patricia-fowler"),
            holder("Dennis Harty", "dennis-harty",
                   existing_person_id="ocd-person/fd82594b-92ae-5ab2-9e36-85c3a953a763"),
            holder("Amy Howlett", "amy-howlett"),
            holder("Charlie Hunter", "charlie-hunter"),
            holder("Chris Kibbe", "chris-kibbe"),
            holder("Sally MacPhee", "sally-macphee"),
            holder("Paul Obuchowski", "paul-obuchowski",
                   existing_person_id="ocd-person/6d6d72e1-192d-5297-9e70-0ca72fb41e6f"),
            holder("Richard O'Donnell", "richard-odonnell"),
            holder("Peter Stickney", "peter-stickney"),
            holder("Gloria Vancor", "gloria-vancor"),
            holder("Deborah Wright", "deborah-wright")]),
], jp=jp_election("rockingham-vt", "Town of Rockingham", 15,
                  "the certified listing names fourteen winners "
                  "and one 'Vacant' seat for Rockingham's "
                  "fifteen justice of the peace seats (the "
                  "Georgia 'Open' pattern); vote_for is fifteen"))

ORDER = ["proctor", "putney", "randolph", "reading", "readsboro",
         "richford", "richmond", "ripton", "rochester",
         "rockingham"]

for slug in ORDER:
    (OUT / f"{slug}.json").write_text(
        json.dumps(SPECS[slug], indent=1) + "\n")
print("wrote", len(ORDER), "specs")
