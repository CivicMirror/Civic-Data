#!/usr/bin/env python3
"""Batch 24 of the VT #163 municipal fan-out (alphabetical positions
230-239): Troy, Tunbridge, Underhill, Vergennes, Vernon, Vershire,
Victory, Waitsfield, Walden, Wallingford. Emits one JSON spec per
municipality for build_vt_municipality.py. Research:
vt_muni_batch24_research.md.

Identity calls baked into this batch (all flagged on #163):
- Troy Town Clerk and Town Treasurer Terri Medley is the Village of
  North Troy trustee chair minted in batch 17 (the village sits
  inside the town): her holder entries reuse
  ocd-person/03da541b-7f45-56d8-8833-83fabdd4953d and no new person
  file is written. Troy JP Helene Croteau is likewise the North
  Troy trustee of batch 17: her JP holder entry reuses
  ocd-person/d5d93b7c-4c70-5fca-9658-85c3ad6c87e2, and her JP
  candidacy is appended to that record by hand after the build
  (the batch-22/23 reuse pattern).
- Vergennes Mayor Chris Bearor and JP Christopher Bearor are one
  person (the certified JP listing gives the full form); Alderman
  Mark Koenig is also a JP -- single records.
- Vernon's warned 2026 treasurer candidate Joshua Kubecka is NOT
  seated: the March 2, 2026 meeting voted 52-38 under 17 V.S.A.
  sec. 2651f to convert the treasurer to a Selectboard-appointed
  Finance Director the night before the ballot, and Katherine
  Walker holds the office by appointment. He is not minted.
- Vershire's certified JP slate governs over the town report's JP
  table (equal-count name-swap, Strout vs Hancy): Strout's only
  documented resignation is from her appointed lister seat.
- Waitsfield's Jennifer Peterson holds three roles on one record:
  appointed Town Clerk (ch. 157 sec. 5(a)), elected Collector of
  Delinquent Taxes, and elected Justice of the Peace.
- Walden's Emily Varvir (lister + auditor), Marie Blodgett
  (auditor + library trustee), and Judith Clifford (auditor +
  cemetery commissioner; the auditors page styles her Judy) are
  single records. Wallingford's Maureen Duchesne (auditor + JP),
  Patricia Pranger (trustee of public funds + JP), and Anne Awad
  (selectboard + trustee of public funds) are single records.
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
CHARTER_015 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/015",
    "note": "PLACEHOLDER",
}
CHARTER_155 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/155",
    "note": "PLACEHOLDER",
}
CHARTER_157 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/157",
    "note": "PLACEHOLDER",
}
TROY_SB = {"url": "https://troyvt.gov/town/selectboard",
           "note": "PLACEHOLDER"}
TROY_CLERK = {"url": "https://troyvt.gov/town/town-clerk-treasurer/contact-hours",
              "note": "PLACEHOLDER"}
TROY_ASSESSORS = {"url": "https://troyvt.gov/town/assessors",
                  "note": "PLACEHOLDER"}
TROY_REPORT = {"url": "https://troyvt.gov/fileadmin/files/General/Troy_Annual_Report_2025.pdf",
               "note": "PLACEHOLDER"}
TUNBRIDGE_MINUTES = {"url": "https://tunbridgevt.org/wp-content/uploads/2026/03/20260303-town-meeting-mins-tunbridge-vt.pdf",
                     "note": "PLACEHOLDER"}
TUNBRIDGE_REPORT = {"url": "https://tunbridgevt.org/wp-content/uploads/2026/02/2025-town-report-tunbridge-vt.pdf",
                    "note": "PLACEHOLDER"}
VERGENNES_REPORT = {"url": "https://www.dropbox.com/scl/fi/6nexrlvrr71dfvy1naqld/2026-Annual-Report-Corrected-ver.1.pdf?rlkey=sx1tpjd6iz5y06omf8zp1icoz&st=kc45msyz&dl=1",
                    "note": "PLACEHOLDER"}
VERGENNES_COUNCIL = {"url": "https://www.vergennes.org/government/city_council/index.php",
                     "note": "PLACEHOLDER"}
VERGENNES_MIN_0310 = {"url": "https://www.vergennes.org/FINAL%20minutes%2003%2010%2026%20-.pdf",
                      "note": "PLACEHOLDER"}
VERGENNES_MIN_0324 = {"url": "https://www.vergennes.org/Final%20MINUTES%2003%2024%2026%20-%20MH-BS.pdf",
                      "note": "PLACEHOLDER"}
VERGENNES_MIN_0414 = {"url": "https://www.vergennes.org/FINAL%20MINUTES%20%2004%2014%2026.pdf",
                      "note": "PLACEHOLDER"}
VERNON_MINUTES = {"url": "https://storage.googleapis.com/juniper-media-library/62/2026/03/2026%20Vernon%20Town%20Meeting%20minutes%20(003).pdf",
                  "note": "PLACEHOLDER"}
VERNON_REPORT = {"url": "https://storage.googleapis.com/juniper-media-library/62/2026/02/2025%20Town%20of%20Vernon%20Annual%20Report-2.pdf",
                 "note": "PLACEHOLDER"}
VERNON_LIBRARY = {"url": "https://vernonvt.org/library",
                  "note": "PLACEHOLDER"}
VERSHIRE_REPORT = {"url": "https://vershirevt.org/wp-content/uploads/2026/02/Town-Report-2026-Final-Draft-02.23.26-compressed.pdf",
                   "note": "PLACEHOLDER"}
VERSHIRE_RESULTS = {"url": "https://vershirevt.org/wp-content/uploads/2026/04/2026-Town-Meeting-article-results-1.pdf",
                    "note": "PLACEHOLDER"}
WAITSFIELD_SB = {"url": "https://waitsfieldvt.gov/boards-meetings/selectboard",
                 "note": "PLACEHOLDER"}
WAITSFIELD_REPORT = {"url": "https://waitsfieldvt.gov/fileadmin/files/Departments/Town_Clerk/Annual_Reports/2025_Waitsfield_Town_Report.pdf",
                     "note": "PLACEHOLDER"}
WAITSFIELD_LISTERS = {"url": "https://waitsfieldvt.gov/departments/assessors-listers",
                      "note": "PLACEHOLDER"}
WAITSFIELD_CLERK = {"url": "https://www.waitsfieldvt.gov/departments/town-clerk",
                    "note": "PLACEHOLDER"}
WALDEN_SB = {"url": "https://waldenvt.gov/selectboard",
             "note": "PLACEHOLDER"}
WALDEN_BOARDS = {"url": "https://waldenvt.gov/boardsandcommissions",
                 "note": "PLACEHOLDER"}
WALDEN_LISTERS = {"url": "https://waldenvt.gov/index.asp?SEC=F0B11452-9588-4F76-B976-8D3003149C66",
                  "note": "PLACEHOLDER"}
WALDEN_AUDITORS = {"url": "https://waldenvt.gov/index.asp?SEC=EE7B6355-A700-4005-9B0E-7B1CC3520773",
                   "note": "PLACEHOLDER"}
WALDEN_CEMETERY = {"url": "https://waldenvt.gov/index.asp?SEC=89C3FC4C-08FB-4FEC-A478-75593F87E589",
                   "note": "PLACEHOLDER"}
WALDEN_LIBRARY = {"url": "https://waldenvt.gov/index.asp?SEC=CB8BF7A4-A694-435F-9BDE-FC246D10D47C",
                  "note": "PLACEHOLDER"}
WALDEN_JP = {"url": "https://waldenvt.gov/index.asp?SEC=EA5D721F-2520-47BF-8C90-1F275A41743D",
             "note": "PLACEHOLDER"}
WALLINGFORD_OFFICERS = {"url": "https://www.wallingfordvt.com/government/elected-appointed-officers/",
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


def charter015(phrase):
    return S(CHARTER_015, f"24 App. V.S.A. ch. 15 (City of "
             f"Vergennes): {phrase}")


def charter155(phrase):
    return S(CHARTER_155, f"24 App. V.S.A. ch. 155 (Town of "
             f"Underhill): {phrase}")


def charter157(phrase):
    return S(CHARTER_157, f"24 App. V.S.A. ch. 157 (Town of "
             f"Waitsfield): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 24); issue #163 "
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
                  f"# municipal fan-out batch 24; issue #163 "
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
# Town of Troy (Orleans County) -- general law; floor meeting.
# The 2026 warning elects a moderator and "all officers required
# by law"; the town publishes no minutes, so the warned offices
# beyond the directory-sourced roster are structure-only.
TROY_REP_C = ("Town of Troy, 2025 Annual Report, warning for the "
              "2026 annual meeting printed at pages 5-6")
SPECS["troy"] = spec("troy", "Town of Troy", [
    office("selectboard", "Selectboard Member",
           "Town of Troy Selectboard", 3,
           [sb_dir("names Robert Langlands (Chair), Anne Quirion, "
                   "and Gaston Bathalon for Troy's three-member "
                   "board"),
            S(TROY_SB, "Town of Troy, Selectboard page "
              "(troyvt.gov): lists the same three members. On "
              "March 1, 2022 the town voted to hire New England "
              "Municipal Consultants to perform the duties of the "
              "listers' office (town Assessors page), so no lister "
              "post is created")],
           [holder("Robert Langlands", "robert-langlands"),
            holder("Anne Quirion", "anne-quirion"),
            holder("Gaston Bathalon", "gaston-bathalon")]),
    office("town-clerk", "Town Clerk",
           "Town of Troy Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Terri Medley as Troy's Town Clerk"),
            clerk_xlsx("names Terri Medley as Troy's Town Clerk"),
            S(TROY_CLERK, "Town of Troy, Town Clerk & Treasurer "
              "page (troyvt.gov): Terri Medley holds both offices. "
              "She is also Chair of the Village of North Troy Board "
              "of Trustees (batch 17); one person record carries "
              "all three memberships")],
           [holder("Terri Medley", "terri-medley",
                   existing_person_id="ocd-person/03da541b-7f45-56d8-8833-83fabdd4953d")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Troy Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists Terri Medley as Troy's Town Treasurer"),
            treas_xlsx("names Terri Medley as Troy's Town "
                       "Treasurer"),
            S(TROY_CLERK, "Town of Troy, Town Clerk & Treasurer "
              "page (troyvt.gov): Terri Medley holds both offices")],
           [holder("Terri Medley", "terri-medley",
                   existing_person_id="ocd-person/03da541b-7f45-56d8-8833-83fabdd4953d")]),
    office("moderator", "Town Moderator",
           "Town of Troy Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term; the 2026 warning's "
                                  "Article 1 warns the office"),
            S(TROY_REPORT, TROY_REP_C)]),
    office("auditor", "Auditor",
           "Town of Troy Auditors", 3,
           [statute2646_structure("towns elect auditors (three, "
                                  "staggered terms) unless the "
                                  "office is eliminated")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Troy Collector of Delinquent Taxes", 1,
           [statute2646_structure("towns elect a collector of "
                                  "delinquent taxes; the 2026 "
                                  "warning's Article 3 itemizes the "
                                  "office"),
            S(TROY_REPORT, TROY_REP_C)]),
    office("first-constable", "First Constable",
           "Town of Troy First Constable", 1,
           [statute2646_structure("towns elect constables")]),
    office("grand-juror", "Grand Juror",
           "Town of Troy Grand Juror", 1,
           [statute2646_structure("towns elect a grand juror")]),
    office("town-agent", "Town Agent",
           "Town of Troy Town Agent", 1,
           [statute2646_structure("towns elect a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Troy Justices of the Peace", 7,
           [jp_src("lists seven Troy justices of the peace: "
                   "Robert Starr, John Starr, Holly Wyllie, Eric "
                   "McCann, Cris Choquette, Helene Croteau, and "
                   "Samuel Douglass. Helene Croteau is also a "
                   "Village of North Troy trustee (batch 17); one "
                   "person record carries both memberships, and "
                   "her candidacy is appended to that record")],
           [holder("Robert Starr", "robert-starr"),
            holder("John Starr", "john-starr"),
            holder("Holly Wyllie", "holly-wyllie"),
            holder("Eric McCann", "eric-mccann"),
            holder("Cris Choquette", "cris-choquette"),
            holder("Helene Croteau", "helene-croteau",
                   existing_person_id="ocd-person/d5d93b7c-4c70-5fca-9658-85c3ad6c87e2"),
            holder("Samuel Douglass", "samuel-douglass")]),
], jp=jp_election("troy-vt", "Town of Troy", 7,
                  "the certified listing names seven winners for "
                  "Troy's seven justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Tunbridge (Orange County) -- general law; floor meeting.
# The signed 2026 town meeting minutes and the 2025 Annual Report's
# Elected Town Officers page together carry the full roster.
TUN_MIN_C = ("Town of Tunbridge, minutes of the annual town "
             "meeting of March 3, 2026 (signed; town website)")
TUN_REP_C = ("Town of Tunbridge, 2025 Annual Report, 'Elected "
             "Town Officers' page (town website)")
SPECS["tunbridge"] = spec("tunbridge", "Town of Tunbridge", [
    office("moderator", "Town Moderator",
           "Town of Tunbridge Town Moderator", 1,
           [S(TUNBRIDGE_MINUTES,
              f"{TUN_MIN_C}: Article 1 re-elected Israel "
              "Provoncha as Moderator")],
           [holder("Israel Provoncha", "israel-provoncha")]),
    office("selectboard", "Selectboard Member",
           "Town of Tunbridge Selectboard", 3,
           [S(TUNBRIDGE_MINUTES,
              f"{TUN_MIN_C}: Mike McPhetres won the three-year "
              "selectboard seat in 2026"),
            S(TUNBRIDGE_REPORT,
              f"{TUN_REP_C}: lists Gary Mullen (Chair), John "
              "O'Brien, and Mike McPhetres")],
           [holder("Gary Mullen", "gary-mullen"),
            holder("John O'Brien", "john-obrien"),
            holder("Mike McPhetres", "mike-mcphetres")]),
    office("town-clerk", "Town Clerk",
           "Town of Tunbridge Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Bonnie McCrillis as Tunbridge's Town "
                  "Clerk"),
            clerk_xlsx("names Bonnie McCrillis as Tunbridge's "
                       "Town Clerk; her seat did not stand in "
                       "2026")],
           [holder("Bonnie McCrillis", "bonnie-mccrillis")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Tunbridge Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists Rebecca Hoyt as Tunbridge's Town "
                  "Treasurer"),
            S(TUNBRIDGE_REPORT,
              f"{TUN_REP_C}: lists Rebecca Hoyt as Treasurer "
              "(the treasurer contact spreadsheet carries no "
              "Tunbridge row)")],
           [holder("Rebecca Hoyt", "rebecca-hoyt")]),
    office("lister", "Lister",
           "Town of Tunbridge Listers", 3,
           [S(TUNBRIDGE_MINUTES,
              f"{TUN_MIN_C}: Christine Battcock won the "
              "three-year lister seat in 2026; the minutes' "
              "Article 11 line for the two-year seat is blank in "
              "the document itself, but the same minutes present "
              "Daniel Ruddell and Deb Mullen as sitting listers"),
            S(TUNBRIDGE_REPORT,
              f"{TUN_REP_C}: lists Christine Battcock, Deb "
              "Mullen, and Daniel Ruddell as the three listers")],
           [holder("Christine Battcock", "christine-battcock"),
            holder("Deb Mullen", "deb-mullen"),
            holder("Daniel Ruddell", "daniel-ruddell")]),
    office("auditor", "Auditor",
           "Town of Tunbridge Auditors", 3,
           [S(TUNBRIDGE_MINUTES,
              f"{TUN_MIN_C}: Linda Hoyt won an auditor seat in "
              "2026"),
            S(TUNBRIDGE_REPORT,
              f"{TUN_REP_C}: lists Linda Hoyt, Betsy Race, and "
              "Anissa Morrison as the three auditors")],
           [holder("Linda Hoyt", "linda-hoyt"),
            holder("Betsy Race", "betsy-race"),
            holder("Anissa Morrison", "anissa-morrison")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Tunbridge Cemetery Commissioners", 3,
           [S(TUNBRIDGE_MINUTES,
              f"{TUN_MIN_C}: Dennis Cilley won a cemetery "
              "commissioner seat in 2026"),
            S(TUNBRIDGE_REPORT,
              f"{TUN_REP_C}: lists Dennis Cilley, Ben Tucker, "
              "and Baxter Doty as the three cemetery "
              "commissioners")],
           [holder("Dennis Cilley", "dennis-cilley"),
            holder("Ben Tucker", "ben-tucker"),
            holder("Baxter Doty", "baxter-doty")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Tunbridge Trustees of Public Funds", 3,
           [S(TUNBRIDGE_MINUTES,
              f"{TUN_MIN_C}: Matthew Frost won a trustee of "
              "public funds seat in 2026"),
            S(TUNBRIDGE_REPORT,
              f"{TUN_REP_C}: lists Matthew Frost, Liz York, and "
              "Laura Ginsburg as the three trustees of public "
              "funds")],
           [holder("Matthew Frost", "matthew-frost"),
            holder("Liz York", "liz-york"),
            holder("Laura Ginsburg", "laura-ginsburg")]),
    office("library-trustee", "Library Trustee",
           "Town of Tunbridge Library Trustees", 5,
           [S(TUNBRIDGE_MINUTES,
              f"{TUN_MIN_C}: Elise Gabriel and Liz Williams won "
              "library trustee seats in 2026 (Williams succeeding "
              "Cheryl Metcalf)"),
            S(TUNBRIDGE_REPORT,
              f"{TUN_REP_C}: lists five library trustees")],
           [holder("Elise Gabriel", "elise-gabriel"),
            holder("Liz Williams", "liz-williams"),
            holder("Anna Dechart", "anna-dechart"),
            holder("Laura Ketchum", "laura-ketchum"),
            holder("Leland Whitehouse", "leland-whitehouse")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Tunbridge Collector of Delinquent Taxes", 1,
           [S(TUNBRIDGE_MINUTES,
              f"{TUN_MIN_C}: Joseph Paquin was re-elected "
              "Collector of Delinquent Taxes; Article 4 "
              "separately authorized the Treasurer under "
              "32 V.S.A. section 4791 to collect current taxes")],
           [holder("Joseph Paquin", "joseph-paquin")]),
    office("first-constable", "First Constable",
           "Town of Tunbridge First Constable", 1,
           [S(TUNBRIDGE_MINUTES,
              f"{TUN_MIN_C}: Roger Clark was elected First "
              "Constable")],
           [holder("Roger Clark", "roger-clark")]),
    office("second-constable", "Second Constable",
           "Town of Tunbridge Second Constable", 1,
           [S(TUNBRIDGE_MINUTES,
              f"{TUN_MIN_C}: Mike O'Donnell was elected Second "
              "Constable (the 2025 report showed the second seat "
              "vacant)")],
           [holder("Mike O'Donnell", "mike-odonnell")]),
    office("grand-juror", "Grand Juror",
           "Town of Tunbridge Grand Juror", 1,
           [S(TUNBRIDGE_REPORT,
              f"{TUN_REP_C}: lists Lenora Kimball as Grand "
              "Juror")],
           [holder("Lenora Kimball", "lenora-kimball")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Tunbridge Justices of the Peace", 7,
           [jp_src("lists seven Tunbridge justices of the peace: "
                   "Gordon Barnaby, Helen O'Donnell, Rob Howe, "
                   "Judy Howe, Jonathan Bicknell, John O'Brien, "
                   "and Margaret Rogers. The 2025 Annual Report's "
                   "officers page concurs; it gives Rob Howe's "
                   "full form as Robert Howe")],
           [holder("Gordon Barnaby", "gordon-barnaby"),
            holder("Helen O'Donnell", "helen-odonnell"),
            holder("Robert Howe", "robert-howe",
                   ballot_name="Rob Howe"),
            holder("Judy Howe", "judy-howe"),
            holder("Jonathan Bicknell", "jonathan-bicknell"),
            holder("John O'Brien", "john-obrien"),
            holder("Margaret Rogers", "margaret-rogers")]),
], jp=jp_election("tunbridge-vt", "Town of Tunbridge", 7,
                  "the certified listing names seven winners for "
                  "Tunbridge's seven justice of the peace seats",
                  extra_sources=[S(TUNBRIDGE_REPORT,
                                   f"{TUN_REP_C}: concurs on the "
                                   "seven justices of the peace")]))

# ----------------------------------------------------------------
# City of Vergennes (Addison County) -- charter ch. 15. Section 4
# elects the Mayor, six aldermen, one lister at a time on staggered
# terms, one auditor at a time, and a City Grand Juror; section 9
# has the City Council appoint the City Clerk, Treasurer, and
# constables; section 6 makes the Mayor the presiding officer, so
# there is no moderator post.
VERG_REP_C = ("City of Vergennes, 2026 Annual Report, table of "
              "city officials as of December 31, 2025 (report "
              "page 46)")
SPECS["vergennes"] = spec("vergennes", "City of Vergennes", [
    office("mayor", "Mayor",
           "City of Vergennes Mayor", 1,
           [charter015("section 4 elects a Mayor to a two-year "
                       "term"),
            S(VERGENNES_COUNCIL, "City of Vergennes, City Council "
              "page (vergennes.org): styles Chris Bearor as "
              "Mayor; he was elected in March 2025 to a two-year "
              "term. The certified justices of the peace listing "
              "gives his full form as Christopher Bearor")],
           [holder("Christopher Bearor", "christopher-bearor")]),
    office("alderman", "Alderman",
           "City of Vergennes City Council", 6,
           [charter015("section 4 elects six aldermen, three "
                       "elected annually to two-year terms"),
            S(VERGENNES_COUNCIL, "City of Vergennes, City Council "
              "page: lists Dickie Austin (Senior Alderman and "
              "Deputy Mayor), Michael Daniels, James Dragon, "
              "Melvin Hawley, Mark Koenig, and Jill "
              "Murray-Killon"),
            S(VERGENNES_MIN_0414, "City of Vergennes, City Council "
              "minutes of April 14, 2026: James Dragon was "
              "appointed (4-2) to the alderman seat resigned by "
              "Carson Harder-Hyde on March 6, 2026, for a term to "
              "March 2027; Dickie Austin, Michael Daniels, Melvin "
              "Hawley, and Jill Murray-Killon won election in "
              "March 2026, and Mark Koenig's term runs to 2027")],
           [holder("Dickie Austin", "dickie-austin"),
            holder("Michael Daniels", "michael-daniels"),
            holder("Melvin Hawley", "melvin-hawley"),
            holder("Jill Murray-Killon", "jill-murray-killon"),
            holder("Mark Koenig", "mark-koenig"),
            holder("James Dragon", "james-dragon",
                   how_seated="appointed")]),
    office("city-clerk", "City Clerk",
           "City of Vergennes City Clerk", 1,
           [charter015("section 9: the City Council appoints the "
                       "City Clerk"),
            guide("lists Betsy Sullivan as Vergennes' City Clerk "
                  "(the Guide does not mark the charter "
                  "appointment)")],
           [holder("Betsy Sullivan", "betsy-sullivan",
                   how_seated="appointed")]),
    office("city-treasurer", "City Treasurer",
           "City of Vergennes City Treasurer", 1,
           [charter015("section 9: the City Council appoints the "
                       "City Treasurer"),
            guide("lists Betsy Sullivan as Vergennes' City "
                  "Treasurer")],
           [holder("Betsy Sullivan", "betsy-sullivan",
                   how_seated="appointed")]),
    office("lister", "Lister",
           "City of Vergennes Listers", 3,
           [charter015("section 4 elects one lister at a time to "
                       "staggered three-year terms"),
            S(VERGENNES_REPORT, f"{VERG_REP_C}: lists William "
              "Benton as the elected lister with a term to 2027"),
            S(VERGENNES_MIN_0414, "City of Vergennes, City Council "
              "minutes of April 14, 2026: the March 2026 election "
              "left both warned lister seats unfilled and the "
              "Council reappointed incumbents Danelle Birong and "
              "Sarah Cowan (the signed minutes' spelling governs "
              "over the report table's 'Cowen')")],
           [holder("William Benton", "william-benton"),
            holder("Danelle Birong", "danelle-birong",
                   how_seated="appointed"),
            holder("Sarah Cowan", "sarah-cowan",
                   how_seated="appointed")]),
    office("auditor", "Auditor",
           "City of Vergennes Auditors", 3,
           [charter015("section 4 elects one Auditor at a time to "
                       "staggered three-year terms"),
            S(VERGENNES_REPORT, f"{VERG_REP_C}: the December "
              "2025 holders (David Austin, Chris LaPierre, "
              "Jennifer Clark) were themselves appointees with "
              "terms ending March 2026; the 2026 election warned "
              "three-year, two-year, and one-year auditor seats "
              "but no winners are published, so the post is "
              "created without memberships")]),
    office("city-grand-juror", "City Grand Juror",
           "City of Vergennes City Grand Juror", 1,
           [charter015("section 4 elects a City Grand Juror"),
            S(VERGENNES_REPORT, f"{VERG_REP_C}: Michelle "
              "Eastman's term ended March 2026 and no successor "
              "is published, so the post is created without a "
              "membership")]),
    office("constable", "Constable",
           "City of Vergennes Constables", 1,
           [charter015("section 9: the City Council appoints one "
                       "or more constables"),
            S(VERGENNES_REPORT, f"{VERG_REP_C}: lists Jason "
              "Ouellette as the city's constable")],
           [holder("Jason Ouellette", "jason-ouellette",
                   how_seated="appointed")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "City of Vergennes Justices of the Peace", 10,
           [jp_src("lists ten Vergennes justices of the peace: "
                   "Beth Bearor, Christopher Bearor, Lowell "
                   "Bertrand, Abigail Blum, Tara Brooks, Patricia "
                   "Ganson, Mark Koenig, Nial Rele, Christopher "
                   "Spencer, and Rena Trepanier")],
           [holder("Beth Bearor", "beth-bearor"),
            holder("Christopher Bearor", "christopher-bearor"),
            holder("Lowell Bertrand", "lowell-bertrand"),
            holder("Abigail Blum", "abigail-blum"),
            holder("Tara Brooks", "tara-brooks"),
            holder("Patricia Ganson", "patricia-ganson"),
            holder("Mark Koenig", "mark-koenig"),
            holder("Nial Rele", "nial-rele"),
            holder("Christopher Spencer", "christopher-spencer"),
            holder("Rena Trepanier", "rena-trepanier")]),
], jp=jp_election("vergennes-vt", "City of Vergennes", 10,
                  "the certified listing names ten winners for "
                  "Vergennes' ten justice of the peace seats",
                  extra_sources=[S(VERGENNES_REPORT,
                                   f"{VERG_REP_C}: the report's "
                                   "justice of the peace table "
                                   "matches the certified listing "
                                   "exactly")]))

# ----------------------------------------------------------------
# Town of Vernon (Windham County) -- general law; Australian
# ballot for officers, floor meeting for articles. The signed
# 2026 town meeting minutes, the 2026 Warning and Town Officers
# page in the 2025 Annual Report, and the town library page carry
# the roster.
VERNON_MIN_C = ("Town of Vernon, minutes of the annual town "
                "meeting of March 2-3, 2026 (signed; town "
                "website)")
VERNON_REP_C = ("Town of Vernon, 2025 Annual Report: the 2026 "
                "Warning (Article 1 prints the sole ballot "
                "candidates) and the Town Officers page")
SPECS["vernon"] = spec("vernon", "Town of Vernon", [
    office("moderator", "Town Moderator",
           "Town of Vernon Town Moderator", 1,
           [S(VERNON_MINUTES, f"{VERNON_MIN_C}: Kerry Amidon "
              "presided as Moderator; the Warning's Article 1 "
              "prints her as the sole candidate")],
           [holder("Kerry Amidon", "kerry-amidon")]),
    office("selectboard", "Selectboard Member",
           "Town of Vernon Selectboard", 5,
           [sb_dir("names Sandra Harris (Chair), Brandon Bucossi, "
                   "Jean Carr, Shelli Harvey, and Jim Pinkerton "
                   "for Vernon's five-member board"),
            S(VERNON_MINUTES, f"{VERNON_MIN_C}: Jean Carr and "
              "Shelli Harvey won the two selectboard seats on the "
              "2026 ballot (the Warning prints Harvey as 'Shelli "
              "Dunklee Harvey')")],
           [holder("Sandra Harris", "sandra-harris"),
            holder("Brandon Bucossi", "brandon-bucossi"),
            holder("Jean Carr", "jean-carr"),
            holder("Shelli Harvey", "shelli-harvey"),
            holder("Jim Pinkerton", "jim-pinkerton")]),
    office("town-clerk", "Town Clerk",
           "Town of Vernon Town Clerk", 1,
           [S(VERNON_REPORT, f"{VERNON_REP_C}: the Town Officers "
              "page lists Heidi Johnson-Clement under 'Town Clerk "
              "and Treasurer Appointments' and the elected-clerk "
              "line reads Vacant; the office was not on the 2026 "
              "ballot, the town having converted it to a "
              "Selectboard-appointed office")],
           [holder("Heidi Johnson-Clement", "heidi-johnson-clement",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Vernon Town Treasurer", 1,
           [S(VERNON_MINUTES, f"{VERNON_MIN_C}: Article 9 passed "
              "52-38 on March 2, 2026, authorizing the Selectboard "
              "to appoint the Town Treasurer as Finance Director "
              "under 17 V.S.A. section 2651f; Katherine Walker "
              "holds the office by appointment. The warned "
              "ballot's treasurer candidate Joshua Kubecka was "
              "therefore not seated and is not recorded"),
            treas_xlsx("names 'Katerine Walker, Financial "
                       "Director' as Vernon's treasurer contact")],
           [holder("Katherine Walker", "katherine-walker",
                   how_seated="appointed")]),
    office("lister", "Lister",
           "Town of Vernon Listers", 3,
           [S(VERNON_MINUTES, f"{VERNON_MIN_C}: Chad Baldwin won "
              "the 2026 lister seat; Jesse Jobin's term runs to "
              "2028. The third seat drew no candidate ('Lister - "
              "remaining year - None' on the Warning) and is left "
              "without a membership")],
           [holder("Jesse Jobin", "jesse-jobin"),
            holder("Chad Baldwin", "chad-baldwin")]),
    office("first-constable", "First Constable",
           "Town of Vernon First Constable", 1,
           [S(VERNON_MINUTES, f"{VERNON_MIN_C}: Jesse Jobin won "
              "the First Constable seat on the 2026 ballot")],
           [holder("Jesse Jobin", "jesse-jobin")]),
    office("second-constable", "Second Constable",
           "Town of Vernon Second Constable", 1,
           [S(VERNON_MINUTES, f"{VERNON_MIN_C}: Chad Baldwin won "
              "the Second Constable seat on the 2026 ballot")],
           [holder("Chad Baldwin", "chad-baldwin")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Vernon Collector of Delinquent Taxes", 1,
           [S(VERNON_MINUTES, f"{VERNON_MIN_C}: Marylynn Scherlin "
              "won the 2026 election; Article 27, to make the "
              "office appointed under 17 V.S.A. section 2651d, "
              "was defeated 36-51")],
           [holder("Marylynn Scherlin", "marylynn-scherlin")]),
    office("library-trustee", "Library Trustee",
           "Town of Vernon Library Trustees", 5,
           [S(VERNON_LIBRARY, "Town of Vernon, Vernon Free "
              "Library page (vernonvt.org): lists five elected "
              "trustees -- Cassie Sailsman (Chair), Julie Nevins, "
              "Nicole Deyo, Kristin Bratton, and Erin Harris"),
            S(VERNON_MINUTES, f"{VERNON_MIN_C}: Erin Harris won "
              "the 2026 library trustee seat by floor article "
              "(the report's spelling 'Kristen Bratton' yields "
              "to the library page's 'Kristin Bratton'; Deyo "
              "appears as 'Nikki' on the library page)")],
           [holder("Cassie Sailsman", "cassie-sailsman"),
            holder("Julie Nevins", "julie-nevins"),
            holder("Nicole Deyo", "nicole-deyo"),
            holder("Kristin Bratton", "kristin-bratton"),
            holder("Erin Harris", "erin-harris")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Vernon Justices of the Peace", 10,
           [jp_src("lists ten Vernon justices of the peace: Tim "
                   "Arsenault, Sue Arsenault, David Emery Sr, "
                   "Sandra Harris, Robert Miller, Susan Miller, "
                   "Lynda Starorypinski, Marylynn Scherlin, Jesse "
                   "Jobin, and Nancy Gassett (the town's block "
                   "continues across the listing's page break; "
                   "the annual report's justice table omits "
                   "Scherlin and styles Robert Miller 'Jr.', and "
                   "the certified listing governs)")],
           [holder("Tim Arsenault", "tim-arsenault"),
            holder("Sue Arsenault", "sue-arsenault"),
            holder("David Emery Sr", "david-emery-sr"),
            holder("Sandra Harris", "sandra-harris"),
            holder("Robert Miller", "robert-miller"),
            holder("Susan Miller", "susan-miller"),
            holder("Lynda Starorypinski", "lynda-starorypinski"),
            holder("Marylynn Scherlin", "marylynn-scherlin"),
            holder("Jesse Jobin", "jesse-jobin"),
            holder("Nancy Gassett", "nancy-gassett")]),
], jp=jp_election("vernon-vt", "Town of Vernon", 10,
                  "the certified listing names ten winners for "
                  "Vernon's ten justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Vershire (Orange County) -- general law. The 2026 Town
# Report (warning + 2025 Town Officers page) and the town's
# published results of the postponed April 11, 2026 meeting carry
# the roster.
VERS_REP_C = ("Town of Vershire, 2026 Town Report: the 2026 "
              "Warning and the 2025 Town Officers page")
VERS_RES_C = ("Town of Vershire, published results of the "
              "annual town meeting of April 11, 2026 (postponed "
              "from March; town website)")
SPECS["vershire"] = spec("vershire", "Town of Vershire", [
    office("moderator", "Town Moderator",
           "Town of Vershire Town Moderator", 1,
           [S(VERSHIRE_RESULTS, f"{VERS_RES_C}: Eileen Murphy "
              "was elected Moderator from the floor")],
           [holder("Eileen Murphy", "eileen-murphy")]),
    office("selectboard", "Selectboard Member",
           "Town of Vershire Selectboard", 3,
           [sb_dir("names Nicole White-Fogarty (Chair), Vernal "
                   "Stone, and Amy Record for Vershire's "
                   "three-member board"),
            S(VERSHIRE_RESULTS, f"{VERS_RES_C}: Nicole "
              "White-Fogarty won the three-year ballot seat 88-60 "
              "over Gene Craft")],
           [holder("Nicole White-Fogarty", "nicole-white-fogarty"),
            holder("Vernal Stone", "vernal-stone"),
            holder("Amy Record", "amy-record")]),
    office("town-clerk", "Town Clerk",
           "Town of Vershire Town Clerk", 1,
           [S(VERSHIRE_RESULTS, f"{VERS_RES_C}: Chelsea Parker "
              "won the one-year Town Clerk ballot seat with 169 "
              "votes; she had filled the vacancy left by Gene "
              "Craft's January 2026 resignation"),
            clerk_xlsx("names Chelsea Parker as Vershire's Town "
                       "Clerk")],
           [holder("Chelsea Parker", "chelsea-parker")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Vershire Town Treasurer", 1,
           [S(VERSHIRE_REPORT, f"{VERS_REP_C}: Gene Craft held "
              "the treasurer's office with an elected term to "
              "2027; he resigned in January 2026 and the "
              "Selectboard filled the vacancy by appointment"),
            treas_xlsx("names 'F Naomi Labarr' as Vershire's "
                       "Town Treasurer (the town also advertised "
                       "the post in May 2026)")],
           [holder("Naomi LaBarr", "naomi-labarr",
                   how_seated="appointed")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Vershire Collector of Delinquent Taxes", 1,
           [S(VERSHIRE_RESULTS, f"{VERS_RES_C}: Naomi LaBarr won "
              "the 2026 ballot seat with 167 votes (the same "
              "person the Selectboard appointed Treasurer)")],
           [holder("Naomi LaBarr", "naomi-labarr")]),
    office("lister", "Lister",
           "Town of Vershire Listers", 3,
           [S(VERSHIRE_RESULTS, f"{VERS_RES_C}: Debra S. "
              "Kingsbury won the two-year seat (164) and John "
              "Raynor the one-year seat (148); the three-year "
              "seat drew only scattered one-vote write-ins "
              "against 163 blanks, electing nobody, and is left "
              "without a membership"),
            S(VERSHIRE_REPORT, f"{VERS_REP_C}: the listers' own "
              "report (signed Debra S. Kingsbury) records that "
              "Bonnie Strout and Allison Towle served the year as "
              "appointees after resignations; the officers page "
              "gives Raynor's form as John P. Raynor")],
           [holder("Debra S. Kingsbury", "debra-s-kingsbury"),
            holder("John P. Raynor", "john-p-raynor")]),
    office("cemetery-commissioner", "Cemetery Trustee",
           "Town of Vershire Cemetery Trustees", 3,
           [S(VERSHIRE_REPORT, f"{VERS_REP_C}: lists three "
              "cemetery trustees -- Eleanor Zue (to 2028), Peggy "
              "Darrow (to 2026), and Rita French (to 2027); the "
              "trustees double as sextons"),
            S(VERSHIRE_RESULTS, f"{VERS_RES_C}: Liva Vitols was "
              "elected from the floor to the three-year cemetery "
              "trustee seat (Darrow's term expired)")],
           [holder("Eleanor Zue", "eleanor-zue"),
            holder("Rita French", "rita-french"),
            holder("Liva Vitols", "liva-vitols")]),
    office("planning-commissioner", "Planning Commissioner",
           "Town of Vershire Planning Commission", 5,
           [S(VERSHIRE_REPORT, "24 V.S.A. section 4323 permits a "
              f"town to elect its planning commission; {VERS_REP_C}: "
              "lists five commissioners -- Liana Horster, "
              "Michelle Massa, Eleanor Zue, Gregory Wilson "
              "(Chair), and Seann Cram"),
            S(VERSHIRE_RESULTS, f"{VERS_RES_C}: Michelle Massa "
              "was re-elected and Martin Hale elected, each to a "
              "four-year term, from the floor")],
           [holder("Gregory Wilson", "gregory-wilson"),
            holder("Liana Horster", "liana-horster"),
            holder("Seann Cram", "seann-cram"),
            holder("Michelle Massa", "michelle-massa"),
            holder("Martin Hale", "martin-hale")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Vershire Justices of the Peace", 5,
           [jp_src("lists five Vershire justices of the peace: "
                   "Benjamin 'Pat' Barnes, Margaret 'Peggy' "
                   "Darrow, Bonnie Strout, Reva Seybolt, and "
                   "Andrea Wasserman. The town report's justice "
                   "table swaps Strout for Dawn Hancy, an "
                   "equal-count name-swap; the certified slate "
                   "governs, Strout's only documented resignation "
                   "being from her appointed lister seat, and "
                   "Hancy is recorded as the divergence")],
           [holder("Benjamin Barnes", "benjamin-barnes",
                   ballot_name="Benjamin \"Pat\" Barnes"),
            holder("Margaret Darrow", "margaret-darrow",
                   ballot_name="Margaret \"Peggy\" Darrow"),
            holder("Bonnie Strout", "bonnie-strout"),
            holder("Reva Seybolt", "reva-seybolt"),
            holder("Andrea Wasserman", "andrea-wasserman")]),
], jp=jp_election("vershire-vt", "Town of Vershire", 5,
                  "the certified listing names five winners for "
                  "Vershire's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Victory (Essex County) -- general law; SOS-spine build
# (the town has no website; victoryvt.org is a church in
# Vergennes). The Selectboard directory names no Victory members,
# so the roster comes from the elected-officials roster the Town
# Clerk supplied in September 2026.
SPECS["victory"] = spec("victory", "Town of Victory", [
    office("selectboard", "Selectboard Member",
           "Town of Victory Selectboard", 3,
           [sb_dir("publishes no Victory members ('Contact the "
                   "Town Clerk for more information')"),
            S(SB_DIR, "Town of Victory, 'ELECTED OFFICIALS' "
              "roster for 2026/2027 supplied by Town Clerk "
              "Tracey Martel on September 28, 2026, and logged "
              "in the Vermont Jurisdiction Factory's "
              "source-evidence record "
              "src-vt-recovery-073-victory-roster: Edward Brown "
              "(Chairman, to March 2027), Lori Miller (to March "
              "2028), and Clifford Whiting (to March 2029)")],
           [holder("Edward Brown", "edward-brown"),
            holder("Lori Miller", "lori-miller"),
            holder("Clifford Whiting", "clifford-whiting")]),
    office("town-clerk", "Town Clerk",
           "Town of Victory Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Tracey Martel as Victory's Town Clerk"),
            clerk_xlsx("names Tracey Martel as Victory's Town "
                       "Clerk")],
           [holder("Tracey Martel", "tracey-martel")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Victory Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists Tracey Martel as Victory's Town "
                  "Treasurer (the treasurer contact spreadsheet "
                  "carries no Victory row)")],
           [holder("Tracey Martel", "tracey-martel")]),
    office("moderator", "Town Moderator",
           "Town of Victory Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for "
                                  "a one-year term")]),
    office("lister", "Lister",
           "Town of Victory Listers", 3,
           [statute2646_structure("towns elect three listers on "
                                  "staggered three-year terms")]),
    office("auditor", "Auditor",
           "Town of Victory Auditors", 3,
           [statute2646_structure("towns elect auditors (three, "
                                  "staggered terms) unless the "
                                  "office is eliminated")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Victory Collector of Delinquent Taxes", 1,
           [statute2646_structure("towns elect a collector of "
                                  "delinquent taxes")]),
    office("first-constable", "First Constable",
           "Town of Victory First Constable", 1,
           [statute2646_structure("towns elect constables")]),
    office("grand-juror", "Grand Juror",
           "Town of Victory Grand Juror", 1,
           [statute2646_structure("towns elect a grand juror")]),
    office("town-agent", "Town Agent",
           "Town of Victory Town Agent", 1,
           [statute2646_structure("towns elect a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Victory Justices of the Peace", 5,
           [jp_src("lists five Victory justices of the peace: "
                   "Laurie Gilman, Howard Lynaugh, Sylvia "
                   "McKinstry, Lori Miller, and Walter Neborsky")],
           [holder("Laurie Gilman", "laurie-gilman"),
            holder("Howard Lynaugh", "howard-lynaugh"),
            holder("Sylvia McKinstry", "sylvia-mckinstry"),
            holder("Lori Miller", "lori-miller"),
            holder("Walter Neborsky", "walter-neborsky")]),
], jp=jp_election("victory-vt", "Town of Victory", 5,
                  "the certified listing names five winners for "
                  "Victory's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Waitsfield (Washington County) -- charter ch. 157:
# section 4 elects the officers required by state law by
# Australian ballot, but section 5(a) has the Selectboard appoint
# the Town Clerk and Town Treasurer. The 2025 Town Report's Town
# Officers pages (read from the rendered report) and the live
# town pages carry the roster.
WF_REP_C = ("Town of Waitsfield, 2025 Annual Report, 'TOWN "
            "OFFICERS 2025' pages: elected by Australian ballot, "
            "elected from the floor, and appointed by the "
            "Selectboard")
SPECS["waitsfield"] = spec("waitsfield", "Town of Waitsfield", [
    office("selectboard", "Selectboard Member",
           "Town of Waitsfield Selectboard", 5,
           [sb_dir("names Brian Shupe, Larissa Ursprung, Fred "
                   "Messer, Charles 'Chach' Curtis, and David "
                   "Babbott-Klein for Waitsfield's five-member "
                   "board"),
            S(WAITSFIELD_SB, "Town of Waitsfield, Selectboard "
              "page (waitsfieldvt.gov): Brian Shupe (Chair, term "
              "to March 2028), Larissa Ursprung (Vice Chair, to "
              "March 2028), Fred Messer (to March 2027), Charles "
              "'Chach' Curtis (to March 2029), and David "
              "Babbott-Klein (to March 2027)")],
           [holder("Brian Shupe", "brian-shupe"),
            holder("Larissa Ursprung", "larissa-ursprung"),
            holder("Fred Messer", "fred-messer"),
            holder("Charles \"Chach\" Curtis", "charles-chach-curtis"),
            holder("David Babbott-Klein", "david-babbott-klein")]),
    office("town-clerk", "Town Clerk",
           "Town of Waitsfield Town Clerk", 1,
           [charter157("section 5(a): the Selectboard appoints "
                       "the Town Clerk to a term of one to three "
                       "years"),
            S(WAITSFIELD_REPORT, f"{WF_REP_C}: lists Jennifer "
              "Peterson as Town Clerk (appointed, term to March "
              "2027); the town's live Town Clerk page concurs")],
           [holder("Jennifer Peterson", "jennifer-peterson",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Waitsfield Town Treasurer", 1,
           [charter157("section 5(a): the Selectboard appoints "
                       "the Town Treasurer to a term of one to "
                       "three years"),
            S(WAITSFIELD_REPORT, f"{WF_REP_C}: lists Steve Lewis "
              "as Town Treasurer (appointed, term to March "
              "2028); the town's live Town Clerk page styles him "
              "Town Treasurer today")],
           [holder("Steve Lewis", "steve-lewis",
                   how_seated="appointed")]),
    office("moderator", "Town Moderator",
           "Town of Waitsfield Town Moderator", 1,
           [S(WAITSFIELD_REPORT, f"{WF_REP_C}: Kari Dolan was "
              "elected Moderator from the floor with a term "
              "ending March 2026; the 2026 Warning's Article 1 "
              "warns the office but no outcome is published, so "
              "the post is created without a membership")]),
    office("lister", "Lister",
           "Town of Waitsfield Listers", 3,
           [S(WAITSFIELD_LISTERS, "Town of Waitsfield, Assessors "
              "& Listers page (waitsfieldvt.gov): 'Lister: Ted "
              "Joslin (term expires March 2028)'; the Chair seat "
              "(term to 2029) and the seat to 2027 are both "
              "shown Vacant -- Charlie Goodman III's term "
              "expired March 2026 and Steve McKenzie has "
              "departed, so only Joslin is seated")],
           [holder("Ted Joslin", "ted-joslin")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Waitsfield Collector of Delinquent Taxes", 1,
           [S(WAITSFIELD_REPORT, f"{WF_REP_C}: lists Jennifer "
              "Peterson as Collector of Delinquent Taxes "
              "(elected); the 2026 Warning's Article 3 confirms "
              "the one-year term stood in 2026 (and asks to "
              "lengthen it to three years from 2027)"),
            S(WAITSFIELD_CLERK, "Town of Waitsfield, Town Clerk "
              "page: styles Jennifer Peterson 'Town Clerk, "
              "Delinquent Tax Collector, Assistant Town "
              "Treasurer' today -- incumbent continuity on the "
              "town's own current presentation")],
           [holder("Jennifer Peterson", "jennifer-peterson")]),
    office("library-trustee", "Library Trustee",
           "Town of Waitsfield Joslin Memorial Library Trustees",
           5,
           [S(WAITSFIELD_REPORT, f"{WF_REP_C}: lists five "
              "elected library trustees -- Caitlin Ennis (to "
              "2026), David Babic (to 2027), Patricia Read (to "
              "2028), Carol Hosford (to 2029), and Jean Joslin "
              "(to 2030); Ennis's seat expired March 2026 with "
              "no published outcome, so it is left without a "
              "membership")],
           [holder("David Babic", "david-babic"),
            holder("Patricia Read", "patricia-read"),
            holder("Carol Hosford", "carol-hosford"),
            holder("Jean Joslin", "jean-joslin")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Waitsfield Cemetery Commissioners", 5,
           [S(WAITSFIELD_REPORT, f"{WF_REP_C}: lists five "
              "elected cemetery commissioners -- Mark Peal (to "
              "2026), Laura Brines (to 2027), Robin Preuss (to "
              "2028), Robin McDermott (to 2029), and Nancy "
              "Coombs (to 2030); Peal's seat expired March 2026 "
              "with no published outcome, so it is left without "
              "a membership")],
           [holder("Laura Brines", "laura-brines"),
            holder("Robin Preuss", "robin-preuss"),
            holder("Robin McDermott", "robin-mcdermott"),
            holder("Nancy Coombs", "nancy-coombs")]),
    office("trustee-of-cemetery-funds",
           "Trustee of Cemetery Funds",
           "Town of Waitsfield Trustees of Cemetery Funds", 3,
           [S(WAITSFIELD_REPORT, f"{WF_REP_C}: lists three "
              "trustees of cemetery funds, one seat already "
              "vacant (term to 2026), Gib Geiger Jr. (to 2027), "
              "and Robert Cook (to 2028)")],
           [holder("Gib Geiger Jr.", "gib-geiger-jr"),
            holder("Robert Cook", "robert-cook")]),
    office("first-constable", "First Constable",
           "Town of Waitsfield First Constable", 1,
           [S(WAITSFIELD_REPORT, f"{WF_REP_C}: places the "
              "Constable under 'Appointed by the Selectboard': "
              "Jeff Campbell")],
           [holder("Jeff Campbell", "jeff-campbell",
                   how_seated="appointed")]),
    office("second-constable", "Second Constable",
           "Town of Waitsfield Second Constable", 1,
           [S(WAITSFIELD_REPORT, f"{WF_REP_C}: places the "
              "Second Constable under 'Appointed by the "
              "Selectboard': Jeff Campbell")],
           [holder("Jeff Campbell", "jeff-campbell",
                   how_seated="appointed")]),
    office("road-commissioner", "Road Commissioner",
           "Town of Waitsfield Road Commissioner", 1,
           [S(WAITSFIELD_REPORT, f"{WF_REP_C}: places the Road "
              "Commissioner under 'Appointed by the Selectboard' "
              "with a term to March 2026: Charles Goodman III "
              "(a 17 V.S.A. section 2646 office whose holder the "
              "town publishes as an appointee)")],
           [holder("Charles Goodman III", "charles-goodman-iii",
                   how_seated="appointed")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Waitsfield Justices of the Peace", 7,
           [jp_src("lists seven Waitsfield justices of the "
                   "peace: Cecil 'Zeke' Church, Andreas Lehner, "
                   "Mary Lehner, Helen Myers, Jennifer Peterson, "
                   "Roberta 'Bobbi' Rood, and Karen Rookwood")],
           [holder("Cecil \"Zeke\" Church", "cecil-zeke-church"),
            holder("Andreas Lehner", "andreas-lehner"),
            holder("Mary Lehner", "mary-lehner"),
            holder("Helen Myers", "helen-myers"),
            holder("Jennifer Peterson", "jennifer-peterson"),
            holder("Roberta \"Bobbi\" Rood", "roberta-bobbi-rood"),
            holder("Karen Rookwood", "karen-rookwood")]),
], jp=jp_election("waitsfield-vt", "Town of Waitsfield", 7,
                  "the certified listing names seven winners for "
                  "Waitsfield's seven justice of the peace seats",
                  extra_sources=[S(WAITSFIELD_REPORT,
                                   f"{WF_REP_C}: the report's "
                                   "justice of the peace table "
                                   "matches the certified listing "
                                   "exactly")]))

# ----------------------------------------------------------------
# Town of Walden (Caledonia County) -- general law. The town's own
# board pages (waldenvt.gov) carry the rosters page by page.
SPECS["walden"] = spec("walden", "Town of Walden", [
    office("selectboard", "Selectboard Member",
           "Town of Walden Selectboard", 3,
           [sb_dir("names Jonathan Augeri, Brenda Huntoon, and "
                   "Randolph Wilson for Walden's three-member "
                   "board"),
            S(WALDEN_SB, "Town of Walden, Selectboard page "
              "(waldenvt.gov): Randolph Wilson (Chair), Brenda "
              "Huntoon, and Jon Augeri")],
           [holder("Randolph Wilson", "randolph-wilson"),
            holder("Brenda Huntoon", "brenda-huntoon"),
            holder("Jonathan Augeri", "jonathan-augeri")]),
    office("town-clerk", "Town Clerk",
           "Town of Walden Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Deborah Messier as Walden's Town Clerk"),
            clerk_xlsx("names the clerk as 'Debbie Messier,' a "
                       "diminutive; the town's own site gives "
                       "Deborah Messier, which governs"),
            S(WALDEN_BOARDS, "Town of Walden, Boards and "
              "Commissions page (waldenvt.gov): 'Walden Town "
              "Clerk, Deborah Messier'")],
           [holder("Deborah Messier", "deborah-messier")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Walden Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists Deborah Messier as Walden's Town "
                  "Treasurer (the treasurer contact spreadsheet "
                  "carries no Walden row)")],
           [holder("Deborah Messier", "deborah-messier")]),
    office("moderator", "Town Moderator",
           "Town of Walden Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for "
                                  "a one-year term")]),
    office("lister", "Lister",
           "Town of Walden Listers", 3,
           [S(WALDEN_LISTERS, "Town of Walden, Listers page "
              "(waldenvt.gov): 'The Board of Listers is a "
              "three-member elected board... Members are elected "
              "for staggered three-year terms': Victoria Atwood, "
              "Dia Michaud, and Emily Varvir")],
           [holder("Victoria Atwood", "victoria-atwood"),
            holder("Dia Michaud", "dia-michaud"),
            holder("Emily Varvir", "emily-varvir")]),
    office("auditor", "Auditor",
           "Town of Walden Auditors", 3,
           [S(WALDEN_AUDITORS, "Town of Walden, Auditors page "
              "(waldenvt.gov): 'The job of the elected auditors "
              "is to review the accounts of local officials': "
              "Marie Blodgett, Judy Clifford, and Emily Varvir")],
           [holder("Marie Blodgett", "marie-blodgett"),
            holder("Judith Clifford", "judith-clifford"),
            holder("Emily Varvir", "emily-varvir")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Walden Cemetery Commissioners", 3,
           [S(WALDEN_CEMETERY, "Town of Walden, Cemetery page "
              "(waldenvt.gov): 'Cemetery Commissioners': Judith "
              "Clifford, Lynette Farnham, and Daniel Mencucci "
              "(the Auditors page styles Clifford as Judy; one "
              "person holds both seats)")],
           [holder("Judith Clifford", "judith-clifford"),
            holder("Lynette Farnham", "lynette-farnham"),
            holder("Daniel Mencucci", "daniel-mencucci")]),
    office("library-trustee", "Library Trustee",
           "Town of Walden Library Trustees", 5,
           [S(WALDEN_LIBRARY, "Town of Walden, Library page "
              "(waldenvt.gov): 'Library Trustees': Sarah Augeri, "
              "Martha Bissell, Marie Blodgett, Allison Gulka, "
              "and Tammy Hall")],
           [holder("Sarah Augeri", "sarah-augeri"),
            holder("Martha Bissell", "martha-bissell"),
            holder("Marie Blodgett", "marie-blodgett"),
            holder("Allison Gulka", "allison-gulka"),
            holder("Tammy Hall", "tammy-hall")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Walden Collector of Delinquent Taxes", 1,
           [statute2646_structure("towns elect a collector of "
                                  "delinquent taxes")]),
    office("first-constable", "First Constable",
           "Town of Walden First Constable", 1,
           [statute2646_structure("towns elect constables; the "
                                  "town's Constable page is a "
                                  "bare heading naming no holder")]),
    office("grand-juror", "Grand Juror",
           "Town of Walden Grand Juror", 1,
           [statute2646_structure("towns elect a grand juror")]),
    office("town-agent", "Town Agent",
           "Town of Walden Town Agent", 1,
           [statute2646_structure("towns elect a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Walden Justices of the Peace", 5,
           [jp_src("lists five Walden justices of the peace: "
                   "Diane Cochran, Jeremiah Cook, Roger Fox, "
                   "Annie Gaillard, and Elizabeth Wilkel")],
           [holder("Diane Cochran", "diane-cochran"),
            holder("Jeremiah Cook", "jeremiah-cook"),
            holder("Roger Fox", "roger-fox"),
            holder("Annie Gaillard", "annie-gaillard"),
            holder("Elizabeth Wilkel", "elizabeth-wilkel")]),
], jp=jp_election("walden-vt", "Town of Walden", 5,
                  "the certified listing names five winners for "
                  "Walden's five justice of the peace seats",
                  extra_sources=[S(WALDEN_JP,
                                   "Town of Walden, Justices of "
                                   "the Peace page (waldenvt.gov): "
                                   "'Walden has five current JP's' "
                                   "and lists the same five; it "
                                   "styles Annie Gaillard as 'Anne "
                                   "Gaillard' and the certified "
                                   "listing's form governs")]))

# ----------------------------------------------------------------
# Town of Wallingford (Rutland County) -- general law. The town's
# Elected and Appointed Officers page (wallingfordvt.com) carries
# the roster; the town uses a contracted assessor, so there is no
# lister post.
WF_OFF_C = ("Town of Wallingford, Elected and Appointed "
            "Officers page (wallingfordvt.com)")
SPECS["wallingford"] = spec("wallingford", "Town of Wallingford", [
    office("selectboard", "Selectboard Member",
           "Town of Wallingford Selectboard", 5,
           [sb_dir("lists only Carolyn Behrendt and Katherine "
                   "Luzader of Wallingford's five-member board"),
            S(WALLINGFORD_OFFICERS, f"{WF_OFF_C}: Anne Awad, Rob "
              "Barker, Carolyn Behrendt, Kathy Luzader (Chair), "
              "and Glenn Mayer (Vice Chair). The directory's "
              "'Katherine Luzader' is the Chair's formal variant; "
              "the town's own page and the roster of record read "
              "Kathy Luzader")],
           [holder("Anne Awad", "anne-awad"),
            holder("Rob Barker", "rob-barker"),
            holder("Carolyn Behrendt", "carolyn-behrendt"),
            holder("Kathy Luzader", "kathy-luzader"),
            holder("Glenn Mayer", "glenn-mayer")]),
    office("town-clerk", "Town Clerk",
           "Town of Wallingford Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Jill Stone-Teer as Wallingford's Town "
                  "Clerk"),
            clerk_xlsx("names Jill Stone-Teer as Wallingford's "
                       "Town Clerk"),
            S(WALLINGFORD_OFFICERS, f"{WF_OFF_C}: 'Town Clerk, "
              "Jill Stone Teer' (the page drops the hyphen; the "
              "Guide's form governs)")],
           [holder("Jill Stone-Teer", "jill-stone-teer")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Wallingford Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists Jill Stone-Teer as Wallingford's Town "
                  "Treasurer"),
            treas_xlsx("names Jill Stone-Teer as Wallingford's "
                       "Town Treasurer")],
           [holder("Jill Stone-Teer", "jill-stone-teer")]),
    office("moderator", "Town Moderator",
           "Town of Wallingford Town Moderator", 1,
           [S(WALLINGFORD_OFFICERS, f"{WF_OFF_C}: 'Town "
              "Moderator, Tammy Heffernan'")],
           [holder("Tammy Heffernan", "tammy-heffernan")]),
    office("auditor", "Auditor",
           "Town of Wallingford Auditors", 3,
           [S(WALLINGFORD_OFFICERS, f"{WF_OFF_C}: 'Auditors: "
              "Maureen Duchesne, Chelsey LaRock and Karen "
              "Smith'")],
           [holder("Maureen Duchesne", "maureen-duchesne"),
            holder("Chelsey LaRock", "chelsey-larock"),
            holder("Karen Smith", "karen-smith")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Wallingford Collector of Delinquent Taxes", 1,
           [S(WALLINGFORD_OFFICERS, f"{WF_OFF_C}: 'Del. Tax "
              "Collector, Julie Sharon'")],
           [holder("Julie Sharon", "julie-sharon")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Wallingford Trustees of Public Funds", 3,
           [S(WALLINGFORD_OFFICERS, f"{WF_OFF_C}: 'Trustees of "
              "Public Funds: Pat Pranger, Anne Awad, and John "
              "Rauch' (Pranger is the justices of the peace "
              "listing's Patricia Pranger)")],
           [holder("Patricia Pranger", "patricia-pranger"),
            holder("Anne Awad", "anne-awad"),
            holder("John Rauch", "john-rauch")]),
    office("first-constable", "First Constable",
           "Town of Wallingford First Constable", 1,
           [S(WALLINGFORD_OFFICERS, f"{WF_OFF_C}: prints the "
              "First Constable office with no holder named, so "
              "the post is created without a membership")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Wallingford Justices of the Peace", 10,
           [jp_src("lists ten Wallingford justices of the peace: "
                   "Wendy Savery, Sandy Eddy, Gary Fredette, "
                   "Curtis Lidstone, Anthony Petrossi, Nikolaus "
                   "Houghton, Maureen Duchesne, Nanette Dubin, "
                   "Michael Luzader, and Patricia Pranger")],
           [holder("Wendy Savery", "wendy-savery"),
            holder("Sandy Eddy", "sandy-eddy"),
            holder("Gary Fredette", "gary-fredette"),
            holder("Curtis Lidstone", "curtis-lidstone"),
            holder("Anthony Petrossi", "anthony-petrossi"),
            holder("Nikolaus Houghton", "nikolaus-houghton"),
            holder("Maureen Duchesne", "maureen-duchesne"),
            holder("Nanette Dubin", "nanette-dubin"),
            holder("Michael Luzader", "michael-luzader"),
            holder("Patricia Pranger", "patricia-pranger")]),
], jp=jp_election("wallingford-vt", "Town of Wallingford", 10,
                  "the certified listing names ten winners for "
                  "Wallingford's ten justice of the peace seats",
                  extra_sources=[S(WALLINGFORD_OFFICERS,
                                   f"{WF_OFF_C}: lists all ten "
                                   "justices of the peace in short "
                                   "forms (Tony Petrossi, Nik "
                                   "Houghton, Nan Dubin); the "
                                   "certified listing's full forms "
                                   "govern")]))

# ----------------------------------------------------------------
# Town of Underhill (Chittenden County) -- charter ch. 155 (only
# sec. 22 departs from general law: the town does not elect other
# collectors of taxes; the Treasurer collects). All sources were
# read firsthand; a delegated read of this town returned a roster
# that exists in no town document and was discarded.
UNDERHILL_SB = {"url": "https://www.underhillvt.gov/selectboard",
                "note": "PLACEHOLDER"}
UNDERHILL_JP = {"url": "https://www.underhillvt.gov/justice-peace",
                "note": "PLACEHOLDER"}
UNDERHILL_WARNING = {"url": "https://www.underhillvt.gov/media/18361",
                     "note": "PLACEHOLDER"}
UNDERHILL_RESULTS = {"url": "https://www.underhillvt.gov/media/18981",
                     "note": "PLACEHOLDER"}
UNDERHILL_REPORT = {"url": "https://www.underhillvt.gov/media/18656",
                    "note": "PLACEHOLDER"}
UH_WARN_C = ("Town of Underhill, Official Warning for the "
             "annual town meeting of March 3, 2026 (town "
             "website)")
UH_RES_C = ("Town of Underhill, official ballot return of the "
            "annual town meeting of March 3, 2026 (town "
            "website)")
UH_REP_C = ("Town of Underhill, FY2025 Town Report, abstract of "
            "the annual town meeting of March 4, 2025")
SPECS["underhill"] = spec("underhill", "Town of Underhill", [
    office("selectboard", "Selectboard Member",
           "Town of Underhill Selectboard", 5,
           [sb_dir("names Patricia Richards, Maureen "
                   "Collins-Kolb, Daniel Steinbauer, Robert "
                   "Stone, and Shara Tarule for Underhill's "
                   "five-member board"),
            S(UNDERHILL_SB, "Town of Underhill, Selectboard page "
              "(underhillvt.gov): Patricia Richards (Chair), "
              "Maureen Collins-Kolb (Vice-Chair), Dan "
              "Steinbauer, Robert Stone, and Shara Tarule"),
            S(UNDERHILL_RESULTS, f"{UH_RES_C}: Patricia "
              "Richards won the three-year seat (548) and Shara "
              "Tarule the two-year seat (530)"),
            S(UNDERHILL_REPORT, f"{UH_REP_C}: Robert Stone won "
              "a three-year seat (484), Maureen Collins-Kolb a "
              "two-year seat (455), and Shara Tarule a one-year "
              "seat (227) in 2025")],
           [holder("Patricia Richards", "patricia-richards"),
            holder("Maureen Collins-Kolb", "maureen-collins-kolb"),
            holder("Dan Steinbauer", "dan-steinbauer"),
            holder("Robert Stone", "robert-stone"),
            holder("Shara Tarule", "shara-tarule")]),
    office("town-clerk", "Town Clerk",
           "Town of Underhill Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(UNDERHILL_RESULTS, f"{UH_RES_C}: Sherri Morin won "
              "the Town Clerk seat (620) for a three-year term"),
            guide("lists Sherri Morin as Underhill's Town Clerk"),
            clerk_xlsx("names Sherri Morin as Underhill's Town "
                       "Clerk")],
           [holder("Sherri Morin", "sherri-morin")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Underhill Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            charter155("section 22: the town shall not elect "
                       "other collectors of current or "
                       "delinquent taxes -- the Treasurer "
                       "collects, and no collector of delinquent "
                       "taxes post is created"),
            S(UNDERHILL_REPORT, f"{UH_REP_C}: Sherri Morin won "
              "the Treasurer seat (511) for a three-year term in "
              "2025; the clerk and treasurer offices run on "
              "staggered three-year cycles and she holds both"),
            guide("lists Sherri Morin as Underhill's Town "
                  "Treasurer"),
            treas_xlsx("names Sherri Morin as Underhill's Town "
                       "Treasurer")],
           [holder("Sherri Morin", "sherri-morin")]),
    office("moderator", "Town Moderator",
           "Town of Underhill Town Moderator", 1,
           [S(UNDERHILL_WARNING, f"{UH_WARN_C}: Article 1 elects "
              "a Moderator from the floor for the ensuing year"),
            S(UNDERHILL_REPORT, f"{UH_REP_C}: Dan Manz was "
              "elected Moderator in 2025; the 2026 floor outcome "
              "is not published, so the post is created without "
              "a membership")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Underhill Justices of the Peace", 9,
           [jp_src("lists nine Underhill justices of the peace: "
                   "Linda Almy, Ellen Arrowsmith, James "
                   "Beebe-Woodard, Travis Beebe-Woodard, William "
                   "Frank, Nancy Geise, Joseph O'Brien, Dan "
                   "Steinbauer, and Patricia Sabalis")],
           [holder("Linda Almy", "linda-almy"),
            holder("Ellen Arrowsmith", "ellen-arrowsmith"),
            holder("James Beebe-Woodard", "james-beebe-woodard"),
            holder("Travis Beebe-Woodard", "travis-beebe-woodard"),
            holder("William Frank", "william-frank"),
            holder("Nancy Geise", "nancy-geise"),
            holder("Joseph O'Brien", "joseph-obrien"),
            holder("Dan Steinbauer", "dan-steinbauer"),
            holder("Patricia Sabalis", "patricia-sabalis")]),
], jp=jp_election("underhill-vt", "Town of Underhill", 9,
                  "the certified listing names nine winners for "
                  "Underhill's nine justice of the peace seats",
                  extra_sources=[S(UNDERHILL_JP,
                                   "Town of Underhill, Justice "
                                   "of the Peace page "
                                   "(underhillvt.gov): concurs on "
                                   "eight of the nine, omitting "
                                   "Nancy Geise; the certified "
                                   "listing governs")]))

ORDER = ["troy", "tunbridge", "underhill", "vergennes", "vernon",
         "vershire", "victory", "waitsfield", "walden",
         "wallingford"]

for slug in ORDER:
    (OUT / f"{slug}.json").write_text(
        json.dumps(SPECS[slug], indent=1) + "\n")
print("wrote", len(ORDER), "specs")
