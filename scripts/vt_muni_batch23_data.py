#!/usr/bin/env python3
"""Batch 23 of the VT #163 municipal fan-out (alphabetical positions
220-229): Stratton, Sudbury, Sunderland, Sutton, Swanton Town,
Swanton Village, Thetford, Tinmouth, Topsham, Townshend. Emits one
JSON spec per municipality for build_vt_municipality.py. Research:
vt_muni_batch23_research.md.

Identity calls baked into this batch (all flagged on #163):
- Swanton JP Randy Brock is the sitting State Senator for the
  Franklin District (he won re-election November 5, 2024): his JP
  holder entry reuses the state-tier person record
  ocd-person/351d1b5d-e438-5984-b81d-14f8eaada494, and his JP
  candidacy is appended to that record by hand after the build
  (the batch-22 Brigham/Luneau pattern). The JP listing gives his
  Swanton address and his own campaign contact email.
- Topsham JP Larry Hart Sr. is the former State Senator for the
  Orange District (won November 5, 2024; resigned effective
  November 14, 2025): his JP holder entry reuses
  ocd-person/4bb39537-886b-5eca-b8d4-d059e24b00b5 (exact name
  including the Sr suffix; Topsham sits in the district he
  represented and the listing's address is in Topsham), and his
  JP candidacy is appended by hand after the build.
- Townshend Lister Helen Holt is a DIFFERENT person from
  Brookline's appointed lister of the same name (batch 4):
  listers must be residents of the town they serve, so the
  builder suffixes the new person file automatically.
- Swanton Village Trustee Neal Speer is also a Town of Swanton
  justice of the peace: the town builds first in ORDER and the
  village holder entry carries person_scope="swanton-71725", so
  one person record carries both memberships (the batch-7 Bumps
  pattern).
- Sudbury's selectboard member Thomas Williams and its JP Tim
  Williams share the address 2425 Route 30; they are minted as
  DISTINCT people, identity unproven (the Fairlee precedent).
- Sunderland's fifth selectboard seat stands VACANT: the March
  3, 2026 ballot for Bruce Mattison's expiring seat drew only
  scattered write-ins with no declared winner, and the April and
  October 2026 selectboard minutes both seat only four members.
  Moderator incumbent Alyson Grzyb topped the write-in count but
  the certified return declares no winner, so she is held under
  the batch-3 write-in rule, as are the write-in-only auditor
  seats, the tied lister and second-constable seats, and the
  inconclusive cemetery seat.
- Swanton Town elects a combined "Town Clerk & Treasurer"
  warned as one three-year office; it is modeled as two posts
  with one holder (the Hardwick combined-office precedent).
- Townshend's town treasurer is Elisha Stratford, not the
  Guide's Elaine Hill: Hill declined the nomination at the 2026
  town meeting and Stratford was elected; the Guide is stale.
- Sudbury has no town website (sudburyvt.org is a parked spam
  domain; sudburyvt.gov does not resolve); it is built on the
  SOS spine in the Stannard shape, with structure-only posts for
  the sec. 2646 offices whose holders no official source
  publishes.
- Swanton Village is built under ch. 279: three elected trustees
  and an elected Village President (who is moderator ex officio,
  so no moderator post), an elected Village Clerk (sec. 6), and
  an APPOINTED Village Treasurer (sec. 7).
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
CHARTER_279 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/279",
    "note": "PLACEHOLDER",
}
STRATTON_SB = {"url": "https://www.townofstrattonvt.com/selectboard",
               "note": "PLACEHOLDER"}
STRATTON_PC = {"url": "https://www.townofstrattonvt.com/planning-commission",
               "note": "PLACEHOLDER"}
STRATTON_ASSESSORS = {"url": "https://www.townofstrattonvt.com/assessors-office",
                      "note": "PLACEHOLDER"}
STRATTON_TM = {"url": "https://www.townofstrattonvt.com/town-meeting-report",
               "note": "PLACEHOLDER"}
SUTTON_GOV = {"url": "https://www.suttonvt.org/government",
              "note": "PLACEHOLDER"}
SUTTON_WARNING = {"url": "https://irp.cdn-website.com/e7d9f92e/files/uploaded/08-Town+Meeting+Warning.pdf",
                  "note": "PLACEHOLDER"}
SUTTON_MINUTES = {"url": "https://irp.cdn-website.com/e7d9f92e/files/uploaded/Town+Meeting+Minutes.pdf",
                  "note": "PLACEHOLDER"}
SUNDERLAND_RETURN = {"url": "https://sunderlandvt.org/wp-content/uploads/2026/03/Australian-Ballot-Official-Return-Of-Votes-2026.pdf",
                     "note": "PLACEHOLDER"}
SUNDERLAND_REPORT = {"url": "https://sunderlandvt.org/wp-content/uploads/2026/02/Sunderland_Complete-Annual-Report-FY25.pdf",
                     "note": "PLACEHOLDER"}
SUNDERLAND_SBMIN_APR = {"url": "https://sunderlandvt.org/wp-content/uploads/2026/04/Minutes_260413-Meeting-Select-Board.pdf",
                        "note": "PLACEHOLDER"}
SUNDERLAND_SBMIN_OCT = {"url": "https://sunderlandvt.org/wp-content/uploads/2026/10/Minutes_261012-Meeting-Select-Board.pdf",
                        "note": "PLACEHOLDER"}
SWANTON_SB = {"url": "https://www.swantonvt.gov/town/selectboard",
              "note": "PLACEHOLDER"}
SWANTON_CLERK = {"url": "https://www.swantonvt.gov/town/clerk-treasurer",
                 "note": "PLACEHOLDER"}
SWANTON_WARNING = {"url": "https://www.swantonvt.gov/fileadmin/files/town/Town_Meeting/Signed_Warning_2026.pdf",
                   "note": "PLACEHOLDER"}
SWANTON_REPORT = {"url": "https://www.swantonvt.gov/fileadmin/files/town/Town_Meeting/2025_Town_Report.pdf",
                  "note": "PLACEHOLDER"}
SWANTON_CEMETERY = {"url": "https://www.swantonvt.gov/services/cemetery",
                    "note": "PLACEHOLDER"}
SWANTON_TRUSTEES = {"url": "https://www.swantonvt.gov/village/trustees",
                    "note": "PLACEHOLDER"}
SWANTON_ADMIN = {"url": "https://www.swantonvt.gov/village/administration",
                 "note": "PLACEHOLDER"}
TINMOUTH_OFFICIALS = {"url": "https://tinmouthvt.gov/boards-commissions-committees-officials",
                      "note": "PLACEHOLDER"}
TINMOUTH_REPORT = {"url": "https://storage.googleapis.com/juniper-media-library/611/2026/06/2025-Tinmouth-Town-Report.pdf",
                   "note": "PLACEHOLDER"}
TOPSHAM_OFFICIALS = {"url": "https://www.townoftopshamvt.org/town",
                     "note": "PLACEHOLDER"}
TOPSHAM_TM = {"url": "https://www.townoftopshamvt.org/selectboardmeetings/town-meeting",
              "note": "PLACEHOLDER"}
TOWNSHEND_SB = {"url": "https://www.townshendvt.gov/boards-meetings/selectboard",
                "note": "PLACEHOLDER"}
TOWNSHEND_LISTERS = {"url": "https://www.townshendvt.gov/boards-meetings/listers",
                     "note": "PLACEHOLDER"}
TOWNSHEND_LIBRARY = {"url": "https://www.townshendvt.gov/boards-meetings/library-trustees",
                     "note": "PLACEHOLDER"}
TOWNSHEND_CEMETERY = {"url": "https://www.townshendvt.gov/boards-meetings/cemetery-commission",
                      "note": "PLACEHOLDER"}
TOWNSHEND_PC = {"url": "https://www.townshendvt.gov/boards-meetings/planning-commission",
                "note": "PLACEHOLDER"}
TOWNSHEND_BCA = {"url": "https://www.townshendvt.gov/boards-meetings/board-of-civil-authority",
                 "note": "PLACEHOLDER"}
TOWNSHEND_MINUTES = {"url": "https://www.townshendvt.gov/fileadmin/files/Boards_and_Committees/Selectboard/Town_Meeting/2026_Town_meeting_minutes_-_signed.pdf",
                     "note": "PLACEHOLDER"}
TOWNSHEND_REPORT = {"url": "https://www.townshendvt.gov/fileadmin/files/Boards_and_Committees/Selectboard/Town_Reports/2026_Twn_Report.Final.pdf",
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


def charter279(phrase):
    return S(CHARTER_279, f"24 App. V.S.A. ch. 279 (Village of "
             f"Swanton): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 23); issue #163 "
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
                  f"# municipal fan-out batch 23; issue #163 "
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
# Town of Stratton (Windham County) -- general law; the town's
# March 3, 2026 town meeting minutes record every election from
# the floor.
STRATTON_MIN_C = ("Town of Stratton, minutes of the annual town "
                  "meeting of March 3, 2026 (town website, town "
                  "meeting page)")
STRATTON_MIN25_C = ("Town of Stratton, minutes of the annual "
                    "town meeting of March 4, 2025 (town website, "
                    "town meeting page)")
SPECS["stratton"] = spec("stratton", "Town of Stratton", [
    office("moderator", "Town Moderator",
           "Town of Stratton Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(STRATTON_TM, f"{STRATTON_MIN_C}: Elizabeth Liller "
                            "was elected Moderator (the minutes' "
                            "body calls her Beth Liller; her "
                            "approval signature reads 'Moderator "
                            "- Elizabeth Liller')")],
           [holder("Elizabeth Liller", "elizabeth-liller")]),
    office("town-clerk", "Town Clerk",
           "Town of Stratton Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(STRATTON_TM, f"{STRATTON_MIN_C}: the meeting "
                            "elected Kent Young Town Clerk to a "
                            "three-year term; he signs the minutes "
                            "'Town Clerk - David Kent Young'"),
            guide("lists Kent Young as Stratton's Town Clerk"),
            clerk_xlsx("names David Young as Stratton's Town "
                       "Clerk; the full name is David Kent Young "
                       "per his own signature on the town meeting "
                       "minutes")],
           [holder("David Kent Young", "david-kent-young")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Stratton Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(STRATTON_TM, f"{STRATTON_MIN_C}: Alyson Peterson "
                            "was elected Town Treasurer to a "
                            "three-year term"),
            guide("lists Alyson Peterson as Stratton's Town "
                  "Treasurer"),
            treas_xlsx("names Alyson Peterson as Stratton's Town "
                       "Treasurer")],
           [holder("Alyson Peterson", "alyson-peterson")]),
    office("selectboard", "Selectboard Member",
           "Town of Stratton Selectboard", 5,
           [S(STRATTON_SB, "Town of Stratton official website, "
                            "Selectboard page: names Albert "
                            "Dupell (Chair), Larry Bills (Vice "
                            "Chair), Chris Liller, Greg Marcucci, "
                            "and Boomer Walker"),
            sb_dir("names Larry Bills, Albert Dupell (Chair), "
                   "Chris Liller, Greg Marcucci, and Boomer "
                   "Walker for Stratton's five-member board"),
            S(STRATTON_TM, f"{STRATTON_MIN_C}: Albert Dupell, "
                            "Greg Marcucci, and Boomer Walker won "
                            "their seats at the 2026 meeting")],
           [holder("Albert Dupell", "albert-dupell"),
            holder("Larry Bills", "larry-bills"),
            holder("Chris Liller", "chris-liller"),
            holder("Greg Marcucci", "greg-marcucci"),
            holder("Boomer Walker", "boomer-walker")]),
    office("planning-commissioner", "Planning Commissioner",
           "Town of Stratton Planning Commission", 5,
           [S(STRATTON_PC, "Town of Stratton official website, "
                            "Planning Commission page: names "
                            "Elizabeth Liller (Chair), Ray "
                            "Hawksley, Rob Wadsworth, Chris Mann, "
                            "and George Rigoulot"),
            S(STRATTON_TM, f"{STRATTON_MIN_C}: Stratton elects "
                            "its planning commissioners from the "
                            "floor -- Elizabeth Liller and George "
                            "Rigoulot were elected to three-year "
                            "terms and Ray Hawksley to a one-year "
                            "term in 2026")],
           [holder("Elizabeth Liller", "elizabeth-liller"),
            holder("Ray Hawksley", "ray-hawksley"),
            holder("Rob Wadsworth", "rob-wadsworth"),
            holder("Chris Mann", "chris-mann"),
            holder("George Rigoulot", "george-rigoulot")]),
    office("lister", "Lister",
           "Town of Stratton Listers", 3,
           [statute2646("towns elect three listers on staggered "
                        "three-year terms"),
            S(STRATTON_ASSESSORS, "Town of Stratton official "
                                   "website, Assessors page: "
                                   "names Elizabeth Liller "
                                   "(Chair), Britt Wohler, and "
                                   "Candie Bernard as listers"),
            S(STRATTON_TM, f"{STRATTON_MIN_C}: Elizabeth Liller "
                            "won the 2026 three-year lister seat")],
           [holder("Elizabeth Liller", "elizabeth-liller"),
            holder("Britt Wohler", "britt-wohler"),
            holder("Candie Bernard", "candie-bernard")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Stratton Cemetery Commissioners", 3,
           [S(STRATTON_SB, "Town of Stratton official website, "
                            "Selectboard page roster: names David "
                            "Kent Young, Larry Bills, and Chris "
                            "Liller as Cemetery Commissioners"),
            S(STRATTON_TM, f"{STRATTON_MIN_C}: David Kent Young "
                            "won the 2026 three-year cemetery "
                            "commissioner seat")],
           [holder("David Kent Young", "david-kent-young"),
            holder("Larry Bills", "larry-bills"),
            holder("Chris Liller", "chris-liller")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Stratton Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes"),
            S(STRATTON_TM, f"{STRATTON_MIN_C}: Candie Bernard "
                            "was elected Collector of Delinquent "
                            "Taxes to a one-year term")],
           [holder("Candie Bernard", "candie-bernard")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Stratton Trustees of Public Funds", 1,
           [statute2646("towns elect trustees of public funds"),
            S(STRATTON_TM, f"{STRATTON_MIN_C}: the meeting "
                            "elected exactly one Trustee of "
                            "Public Funds, Alyson Peterson, to a "
                            f"one-year term; {STRATTON_MIN25_C} "
                            "did the same, so the office is "
                            "single-seat in the town's practice")],
           [holder("Alyson Peterson", "alyson-peterson")]),
    office("constable", "Constable",
           "Town of Stratton Constable", 1,
           [statute2646("towns elect a constable"),
            S(STRATTON_TM, f"{STRATTON_MIN_C}: Paul Bernard was "
                            "elected Constable")],
           [holder("Paul Bernard", "paul-bernard")]),
    office("town-agent", "Town Agent",
           "Town of Stratton Town Agent", 1,
           [statute2646("towns elect a town agent"),
            S(STRATTON_TM, f"{STRATTON_MIN_C}: Victor Rivas was "
                            "elected Town Agent")],
           [holder("Victor Rivas", "victor-rivas")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Stratton Justices of the Peace", 5,
           [jp_src("lists five Stratton justices of the peace: "
                   "Patricia Coolidge, Nancy Ferrucci, Lorraine "
                   "Weeks-Newell, Helen Fuller Eddy, and Diane "
                   "Niederhauser")],
           [holder("Patricia Coolidge", "patricia-coolidge"),
            holder("Nancy Ferrucci", "nancy-ferrucci"),
            holder("Lorraine Weeks-Newell", "lorraine-weeks-newell"),
            holder("Helen Fuller Eddy", "helen-fuller-eddy"),
            holder("Diane Niederhauser", "diane-niederhauser")]),
], jp=jp_election("stratton-vt", "Town of Stratton", 5,
                  "the certified listing names five winners for "
                  "Stratton's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Sudbury (Rutland County) -- general law; no town
# website, built on the SOS spine (Stannard shape).
SPECS["sudbury"] = spec("sudbury", "Town of Sudbury", [
    office("selectboard", "Selectboard Member",
           "Town of Sudbury Selectboard", 3,
           [sb_dir("names Shaun Ketcham (Chair), Travis Romano, "
                   "and Thomas Williams for Sudbury's "
                   "three-member board. The town has no website "
                   "(sudburyvt.org is a parked domain and "
                   "sudburyvt.gov does not resolve), so the "
                   "directory is the roster of record. "
                   "Selectboard member Thomas Williams and "
                   "Justice of the Peace Tim Williams share the "
                   "address 2425 Route 30 in the state sources; "
                   "they are recorded as distinct people, "
                   "identity unproven")],
           [holder("Shaun Ketcham", "shaun-ketcham"),
            holder("Travis Romano", "travis-romano"),
            holder("Thomas Williams", "thomas-williams")]),
    office("town-clerk", "Town Clerk",
           "Town of Sudbury Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Steve Sgorbati as Sudbury's Town Clerk"),
            clerk_xlsx("names the clerk as 'Stevie Sgorbati,' a "
                       "diminutive artifact; the Guide, the "
                       "treasurer spreadsheet, and the certified "
                       "justices of the peace listing all read "
                       "Steve Sgorbati, which governs")],
           [holder("Steve Sgorbati", "steve-sgorbati")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Sudbury Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists Steve Sgorbati as Sudbury's Town "
                  "Treasurer"),
            treas_xlsx("names Steve Sgorbati as Sudbury's Town "
                       "Treasurer")],
           [holder("Steve Sgorbati", "steve-sgorbati")]),
    office("moderator", "Town Moderator",
           "Town of Sudbury Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term")]),
    office("lister", "Lister",
           "Town of Sudbury Listers", 3,
           [statute2646_structure("towns elect three listers on "
                                  "staggered three-year terms")]),
    office("auditor", "Auditor",
           "Town of Sudbury Auditors", 3,
           [statute2646_structure("towns elect auditors (three, "
                                  "staggered terms) unless the "
                                  "office is eliminated")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Sudbury Collector of Delinquent Taxes", 1,
           [statute2646_structure("towns elect a collector of "
                                  "delinquent taxes")]),
    office("first-constable", "First Constable",
           "Town of Sudbury First Constable", 1,
           [statute2646_structure("towns elect constables")]),
    office("grand-juror", "Grand Juror",
           "Town of Sudbury Grand Juror", 1,
           [statute2646_structure("towns elect a grand juror")]),
    office("town-agent", "Town Agent",
           "Town of Sudbury Town Agent", 1,
           [statute2646_structure("towns elect a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Sudbury Justices of the Peace", 5,
           [jp_src("lists five Sudbury justices of the peace: "
                   "Ross Eisenbrey, Tim Williams, Steve Sgorbati, "
                   "Philip 'Ted' Russell, and Arnold 'Skip' "
                   "Abelson (the town's block continues across "
                   "the listing's page 34/35 break)")],
           [holder("Ross Eisenbrey", "ross-eisenbrey"),
            holder("Tim Williams", "tim-williams"),
            holder("Steve Sgorbati", "steve-sgorbati"),
            holder("Philip \"Ted\" Russell", "philip-ted-russell"),
            holder("Arnold \"Skip\" Abelson", "arnold-skip-abelson")]),
], jp=jp_election("sudbury-vt", "Town of Sudbury", 5,
                  "the certified listing names five winners for "
                  "Sudbury's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Sunderland (Bennington County) -- general law;
# Australian ballot, certified return of votes in hand.
SUNDERLAND_RET_C = ("Town of Sunderland, Official Return of "
                    "Votes, Australian ballot election of March "
                    "3, 2026 (certified; town website)")
SUNDERLAND_REP_C = ("Town of Sunderland, FY25 Annual Report, "
                    "'ELECTED TOWN OFFICERS' page (town website)")
SPECS["sunderland"] = spec("sunderland", "Town of Sunderland", [
    office("moderator", "Town Moderator",
           "Town of Sunderland Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term"),
            S(SUNDERLAND_RETURN, f"{SUNDERLAND_RET_C}: the "
                                  "moderator election was "
                                  "write-in only -- incumbent "
                                  "Alyson Grzyb received 20 of "
                                  "164 votes cast (135 blank) "
                                  "and the return declares no "
                                  "winner; no post-election "
                                  "roster names a moderator, so "
                                  "no membership is created (a "
                                  "write-in plurality alone does "
                                  "not seat)")]),
    office("town-clerk", "Town Clerk",
           "Town of Sunderland Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(SUNDERLAND_REPORT, f"{SUNDERLAND_REP_C}: Caroline "
                                  "Hartshorn, Town Clerk, "
                                  "three-year term to 2028"),
            guide("lists Caroline Hartshorn as Sunderland's Town "
                  "Clerk"),
            clerk_xlsx("names her in the fuller form 'Caroline "
                       "Morse Hartshorn'; the town's own "
                       "documents use Caroline Hartshorn, which "
                       "governs")],
           [holder("Caroline Hartshorn", "caroline-hartshorn")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Sunderland Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(SUNDERLAND_REPORT, f"{SUNDERLAND_REP_C}: Caroline "
                                  "Hartshorn, Town Treasurer, "
                                  "three-year term to 2028"),
            guide("lists Caroline Hartshorn as Sunderland's Town "
                  "Treasurer")],
           [holder("Caroline Hartshorn", "caroline-hartshorn")]),
    office("selectboard", "Selectboard Member",
           "Town of Sunderland Selectboard", 5,
           [S(SUNDERLAND_REPORT, f"{SUNDERLAND_REP_C}: names "
                                  "Todd Lawrence (Chair), Martin "
                                  "Nadler, Richard Timmerman, "
                                  "Anthony Thompson, and Bruce "
                                  "Mattison, whose three-year "
                                  "term expired in 2026"),
            S(SUNDERLAND_RETURN, f"{SUNDERLAND_RET_C}: Richard "
                                  "Timmerman re-won a one-year "
                                  "seat with 118 votes and "
                                  "Anthony Thompson with 117; the "
                                  "ballot for Mattison's expiring "
                                  "seat drew only scattered "
                                  "write-ins (top count 13) and "
                                  "declared no winner"),
            S(SUNDERLAND_SBMIN_APR, "Town of Sunderland, "
                                     "selectboard minutes of "
                                     "April 13, 2026: the board "
                                     "seats four members only"),
            S(SUNDERLAND_SBMIN_OCT, "Town of Sunderland, "
                                     "selectboard minutes of "
                                     "October 12, 2026: the "
                                     "board still seats four "
                                     "members; the fifth seat "
                                     "stands vacant")],
           [holder("Todd Lawrence", "todd-lawrence"),
            holder("Martin Nadler", "martin-nadler"),
            holder("Richard Timmerman", "richard-timmerman"),
            holder("Anthony Thompson", "anthony-thompson")]),
    office("lister", "Lister",
           "Town of Sunderland Listers", 3,
           [statute2646("towns elect three listers on staggered "
                        "three-year terms"),
            S(SUNDERLAND_REPORT, f"{SUNDERLAND_REP_C}: Peter Van "
                                  "Vleck Jr. (term to 2027) and "
                                  "Neil Humphrey (to 2028); "
                                  "Robert Goodfellow's seat "
                                  "expired in 2026"),
            S(SUNDERLAND_RETURN, f"{SUNDERLAND_RET_C}: the 2026 "
                                  "ballot for the expiring "
                                  "lister seat was write-in only "
                                  "and tied at one vote each, so "
                                  "no winner is recorded")],
           [holder("Peter Van Vleck Jr.", "peter-van-vleck-jr"),
            holder("Neil Humphrey", "neil-humphrey")]),
    office("auditor", "Auditor",
           "Town of Sunderland Auditors", 3,
           [statute2646_structure("towns elect auditors (three, "
                                  "staggered terms) unless the "
                                  "office is eliminated"),
            S(SUNDERLAND_REPORT, f"{SUNDERLAND_REP_C}: one "
                                  "auditor seat stood vacant and "
                                  "Theodore Rappahahn served as "
                                  "an appointed auditor to 2026"),
            S(SUNDERLAND_RETURN, f"{SUNDERLAND_RET_C}: all three "
                                  "auditor seats were write-in "
                                  "only in 2026 (counts of one "
                                  "to six) with no declared "
                                  "winners, so no memberships "
                                  "are created")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Sunderland Cemetery Commissioners", 3,
           [S(SUNDERLAND_REPORT, f"{SUNDERLAND_REP_C}: Avis "
                                  "Hayden (term to 2027) and "
                                  "Neil Humphrey (to 2028); "
                                  "Kathleen Johnston's seat "
                                  "expired in 2026"),
            S(SUNDERLAND_RETURN, f"{SUNDERLAND_RET_C}: the 2026 "
                                  "ballot for the expiring "
                                  "cemetery seat drew inconclusive "
                                  "write-ins, so no third "
                                  "membership is created")],
           [holder("Avis Hayden", "avis-hayden"),
            holder("Neil Humphrey", "neil-humphrey")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Sunderland Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes"),
            S(SUNDERLAND_RETURN, f"{SUNDERLAND_RET_C}: Allison "
                                  "Murphy was elected Collector "
                                  "of Delinquent Taxes with 140 "
                                  "votes on the printed ballot")],
           [holder("Allison Murphy", "allison-murphy")]),
    office("first-constable", "First Constable",
           "Town of Sunderland First Constable", 1,
           [statute2646("towns elect constables"),
            S(SUNDERLAND_RETURN, f"{SUNDERLAND_RET_C}: Kevin "
                                  "Hewes was elected First "
                                  "Constable with 126 votes on "
                                  "the printed ballot (he moved "
                                  "up from Second Constable)")],
           [holder("Kevin Hewes", "kevin-hewes")]),
    office("second-constable", "Second Constable",
           "Town of Sunderland Second Constable", 1,
           [statute2646_structure("towns elect constables"),
            S(SUNDERLAND_RETURN, f"{SUNDERLAND_RET_C}: the 2026 "
                                  "second constable ballot was "
                                  "write-in only and tied at one "
                                  "vote each, so no membership "
                                  "is created")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Sunderland Justices of the Peace", 5,
           [jp_src("lists five Sunderland justices of the peace: "
                   "Virginia Dexter, Lorene 'Loree' Zeif, Julia "
                   "'Julie' Hutchinson-Smith, Samuel E. Liss, and "
                   "Theodore 'Ted' Rappahahn")],
           [holder("Virginia Dexter", "virginia-dexter"),
            holder("Lorene \"Loree\" Zeif", "lorene-loree-zeif"),
            holder("Julia \"Julie\" Hutchinson-Smith",
                   "julia-julie-hutchinson-smith"),
            holder("Samuel E. Liss", "samuel-e-liss"),
            holder("Theodore \"Ted\" Rappahahn",
                   "theodore-ted-rappahahn")]),
], jp=jp_election("sunderland-vt", "Town of Sunderland", 5,
                  "the certified listing names five winners for "
                  "Sunderland's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Sutton (Caledonia County) -- general law; 2026 warning
# and town meeting minutes in hand.
SUTTON_GOV_C = "Town of Sutton official website, government page"
SUTTON_WARN_C = ("Town of Sutton, Warning for the annual town "
                 "meeting of March 3, 2026 (town website)")
SUTTON_MIN_C = ("Town of Sutton, minutes of the annual town "
                "meeting of March 3, 2026 (town website)")
SPECS["sutton"] = spec("sutton", "Town of Sutton", [
    office("moderator", "Town Moderator",
           "Town of Sutton Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(SUTTON_MINUTES, f"{SUTTON_MIN_C}: Marlin 'Chip' "
                               "Devenger called the meeting to "
                               "order and was re-elected "
                               "Moderator")],
           [holder("Marlin \"Chip\" Devenger",
                   "marlin-chip-devenger")]),
    office("selectboard", "Selectboard Member",
           "Town of Sutton Selectboard", 3,
           [S(SUTTON_GOV, f"{SUTTON_GOV_C}: names Tim Simpson "
                           "(term to 2027), Denis Royer II (to "
                           "2028), and Jeffrey 'Joe' Solinsky "
                           "(to 2029)"),
            S(SUTTON_MINUTES, f"{SUTTON_MIN_C}: Jeffrey 'Joe' "
                               "Solinsky was re-elected March 3, "
                               "2026")],
           [holder("Tim Simpson", "tim-simpson"),
            holder("Denis Royer II", "denis-royer-ii"),
            holder("Jeffrey \"Joe\" Solinsky",
                   "jeffrey-joe-solinsky")]),
    office("town-clerk", "Town Clerk",
           "Town of Sutton Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Patricia McClure as Sutton's Town "
                  "Clerk"),
            clerk_xlsx("names Patricia McClure as Sutton's Town "
                       "Clerk"),
            S(SUTTON_WARNING, f"{SUTTON_WARN_C}: attested by "
                               "Patricia J. McClure as 'Town "
                               "Clerk & Treasurer'")],
           [holder("Patricia J. McClure", "patricia-j-mcclure")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Sutton Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists Patricia McClure as Sutton's Town "
                  "Treasurer"),
            S(SUTTON_WARNING, f"{SUTTON_WARN_C}: attested by "
                               "Patricia J. McClure as 'Town "
                               "Clerk & Treasurer'")],
           [holder("Patricia J. McClure", "patricia-j-mcclure")]),
    office("lister", "Lister",
           "Town of Sutton Listers", 3,
           [statute2646("towns elect three listers on staggered "
                        "three-year terms"),
            S(SUTTON_GOV, f"{SUTTON_GOV_C}: names Paul Lane "
                           "(term to 2027), Mary Gray (to 2028), "
                           "and Candace Heath (to 2029)"),
            S(SUTTON_MINUTES, f"{SUTTON_MIN_C}: Candace Heath "
                               "won the 2026 lister seat")],
           [holder("Paul Lane", "paul-lane"),
            holder("Mary Gray", "mary-gray"),
            holder("Candace Heath", "candace-heath")]),
    office("auditor", "Auditor",
           "Town of Sutton Auditors", 3,
           [statute2646("towns elect auditors (three, staggered "
                        "terms) unless the office is eliminated"),
            S(SUTTON_MINUTES, f"{SUTTON_MIN_C}: Elaine Bandy was "
                               "elected to the 2026 three-year "
                               "auditor seat; the holders of the "
                               "other two seats are published in "
                               "no official source in hand")],
           [holder("Elaine Bandy", "elaine-bandy")]),
    office("first-constable", "First Constable",
           "Town of Sutton First Constable", 1,
           [statute2646("towns elect constables"),
            S(SUTTON_MINUTES, f"{SUTTON_MIN_C}: Kurt Nygren was "
                               "elected First Constable")],
           [holder("Kurt Nygren", "kurt-nygren")]),
    office("second-constable", "Second Constable",
           "Town of Sutton Second Constable", 1,
           [statute2646_structure("towns elect constables"),
            S(SUTTON_MINUTES, f"{SUTTON_MIN_C}: the minutes "
                               "record 'No nominations' for "
                               "Second Constable, so no membership "
                               "is created")]),
    office("grand-juror", "Grand Juror",
           "Town of Sutton Grand Juror", 1,
           [statute2646("towns elect a grand juror"),
            S(SUTTON_MINUTES, f"{SUTTON_MIN_C}: Kathy Keizer was "
                               "elected Grand Juror")],
           [holder("Kathy Keizer", "kathy-keizer")]),
    office("town-agent", "Town Agent",
           "Town of Sutton Town Agent", 1,
           [statute2646("towns elect a town agent"),
            S(SUTTON_WARNING, f"{SUTTON_WARN_C}: the warning "
                               "elects an 'Agent to Convey Real "
                               "Estate,' the town agent's "
                               "real-estate function"),
            S(SUTTON_MINUTES, f"{SUTTON_MIN_C}: John Sylvester "
                               "was elected to the office")],
           [holder("John Sylvester", "john-sylvester")]),
    office("water-commissioner", "Water Commissioner",
           "Town of Sutton Water Commissioners", 1,
           [S(SUTTON_WARNING, f"{SUTTON_WARN_C}: the warning "
                              "elects a Water Commissioner from "
                              "the floor -- a general-franchise "
                              "town office"),
            S(SUTTON_MINUTES, f"{SUTTON_MIN_C}: Scott Spencer "
                               "was elected Water Commissioner")],
           [holder("Scott Spencer", "scott-spencer")]),
    office("cemetery-sexton", "Cemetery Sexton",
           "Town of Sutton Cemetery Sexton", 1,
           [S(SUTTON_WARNING, f"{SUTTON_WARN_C}: the warning "
                              "elects a Cemetery Sexton"),
            S(SUTTON_GOV, f"{SUTTON_GOV_C}: names Patricia "
                           "Jackson, Cemetery Sexton, term to "
                           "2027")],
           [holder("Patricia Jackson", "patricia-jackson")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Sutton Justices of the Peace", 3,
           [jp_src("lists three Sutton justices of the peace: "
                   "Dianna Simpson, Chip Devenger, and Adam "
                   "Bruggeman; the town's own minutes and "
                   "government page give Devenger's full name as "
                   "Marlin 'Chip' Devenger")],
           [holder("Dianna Simpson", "dianna-simpson"),
            holder("Marlin \"Chip\" Devenger",
                   "marlin-chip-devenger",
                   ballot_name="Chip Devenger"),
            holder("Adam Bruggeman", "adam-bruggeman")]),
], jp=jp_election("sutton-vt", "Town of Sutton", 3,
                  "the certified listing names three winners for "
                  "Sutton's three justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Swanton (Franklin County) -- general law; Australian
# ballot; joint town/village website.
SWANTON_REP_C = ("Town of Swanton, 2025 Town Report, 'ELECTED "
                 "TOWN OFFICERS' page (town/village website)")
SWANTON_WARN_C = ("Town of Swanton, Warning for the 2026 annual "
                  "town meeting, signed January 2026 "
                  "(town/village website)")
SPECS["swanton-71725"] = spec("swanton-71725", "Town of Swanton", [
    office("moderator", "Town Moderator",
           "Town of Swanton Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term"),
            S(SWANTON_REPORT, f"{SWANTON_REP_C}: Brian Savage "
                              "held the moderator's one-year term "
                              "expiring in 2026; the 2026 winner "
                              "is published in no official source "
                              "in hand, so no membership is "
                              "created")]),
    office("town-clerk", "Town Clerk",
           "Town of Swanton Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(SWANTON_CLERK, "Town of Swanton official website, "
                             "Town Clerk & Treasurer page: Cathy "
                             "L. Fournier is the Town Clerk; the "
                             "page notes the Clerk also serves as "
                             "the Town Treasurer"),
            S(SWANTON_WARNING, f"{SWANTON_WARN_C}: presents a "
                                "combined 'Town Clerk & Treasurer' "
                                "as one three-year office; modeled "
                                "as two posts with one holder (the "
                                "Hardwick combined-office "
                                "precedent)"),
            guide("lists Cathy Fournier as Swanton's Town Clerk"),
            clerk_xlsx("names Cathy Fournier as Swanton's Town "
                       "Clerk")],
           [holder("Cathy L. Fournier", "cathy-l-fournier")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Swanton Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(SWANTON_CLERK, "Town of Swanton official website, "
                             "Town Clerk & Treasurer page: Cathy "
                             "L. Fournier holds both offices"),
            S(SWANTON_WARNING, f"{SWANTON_WARN_C}: presents a "
                                "combined 'Town Clerk & Treasurer' "
                                "as one three-year office"),
            guide("lists Cathy Fournier as Swanton's Town "
                  "Treasurer"),
            treas_xlsx("names Cathy Fournier as Swanton's Town "
                       "Treasurer")],
           [holder("Cathy L. Fournier", "cathy-l-fournier")]),
    office("selectboard", "Selectboard Member",
           "Town of Swanton Selectboard", 5,
           [S(SWANTON_SB, "Town of Swanton official website, "
                          "Selectboard page: names Joel Clark "
                          "(Chair), Nicholas Brosseau (Vice "
                          "Chair), Nicole Draper, Earl Fournier, "
                          "and Ronald Underwood"),
            sb_dir("names Joel Clark (Chair), Nicholas Brosseau "
                   "(Vice Chair), Nicole Draper, Earl Fournier, "
                   "and Ronald Underwood for Swanton's "
                   "five-member board"),
            S(SWANTON_WARNING, f"{SWANTON_WARN_C}: the January "
                                "2026 signature block still "
                                "shows Steven J. Bourgeois, whose "
                                "three-year seat stood in 2026; "
                                "he is absent from the current "
                                "board and is not seated")],
           [holder("Joel Clark", "joel-clark"),
            holder("Nicholas A. Brosseau", "nicholas-a-brosseau"),
            holder("Nicole Draper", "nicole-draper"),
            holder("Earl Fournier", "earl-fournier"),
            holder("Ronald Underwood", "ronald-underwood")]),
    office("lister", "Lister",
           "Town of Swanton Listers", 3,
           [statute2646("towns elect three listers on staggered "
                        "three-year terms"),
            S(SWANTON_REPORT, f"{SWANTON_REP_C}: David Horton "
                              "(term to 2027) and Kevin Nichols "
                              "(to 2028); Amy Giroux's seat "
                              "expired in 2026 and its outcome is "
                              "published in no official source in "
                              "hand")],
           [holder("David Horton", "david-horton"),
            holder("Kevin Nichols", "kevin-nichols")]),
    office("auditor", "Auditor",
           "Town of Swanton Auditors", 3,
           [statute2646("towns elect auditors (three, staggered "
                        "terms) unless the office is eliminated"),
            S(SWANTON_REPORT, f"{SWANTON_REP_C}: Joyce "
                              "Bombardier (term to 2027) and "
                              "Diane Larocque (to 2028); Amy "
                              "Giroux's seat expired in 2026 and "
                              "its outcome is published in no "
                              "official source in hand")],
           [holder("Joyce Bombardier", "joyce-bombardier"),
            holder("Diane Larocque", "diane-larocque")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Swanton Trustees of Public Money", 3,
           [statute2646("towns elect trustees of public funds; "
                        "Swanton styles the office Trustees of "
                        "Public Money"),
            S(SWANTON_REPORT, f"{SWANTON_REP_C}: Nicholas A. "
                              "Brosseau (term to 2027) and Brian "
                              "K. Savage (to 2028); Cody "
                              "Hemenway's seat stood in 2026 and "
                              "its outcome is published in no "
                              "official source in hand")],
           [holder("Nicholas A. Brosseau", "nicholas-a-brosseau"),
            holder("Brian K. Savage", "brian-k-savage")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Swanton Cemetery Commissioners", 5,
           [S(SWANTON_CEMETERY, "Town of Swanton official "
                                "website, Cemetery Commission "
                                "page: names Nicholas Brosseau, "
                                "John Kaczkowski, Brian Savage, "
                                "and Macy Lavoie-Dupont as the "
                                "current commissioners"),
            S(SWANTON_REPORT, f"{SWANTON_REP_C}: the report's "
                              "roster also carried Cody Hemenway "
                              "with a term to 2029; he is absent "
                              "from the current commission page "
                              "and is not seated")],
           [holder("Nicholas A. Brosseau", "nicholas-a-brosseau"),
            holder("John Kaczkowski", "john-kaczkowski"),
            holder("Brian K. Savage", "brian-k-savage",
                   ballot_name="Brian Savage"),
            holder("Macy Lavoie-Dupont", "macy-lavoie-dupont")]),
    office("library-trustee", "Library Trustee",
           "Town of Swanton Library Trustees", 5,
           [S(SWANTON_REPORT, f"{SWANTON_REP_C}: Kathy Kneebone "
                              "(term to 2027), Sarah Garvey (to "
                              "2028), Richard Kelly (to 2029), "
                              "and Bianca Braman (to 2030); "
                              "Rebecca Rupp's seat expired in "
                              "2026 and its outcome is published "
                              "in no official source in hand")],
           [holder("Richard Kelly", "richard-kelly"),
            holder("Kathy Kneebone", "kathy-kneebone"),
            holder("Bianca Braman", "bianca-braman"),
            holder("Sarah Garvey", "sarah-garvey")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Swanton Collector of Delinquent Taxes", 1,
           [statute2646_structure("towns elect a collector of "
                                  "delinquent taxes"),
            S(SWANTON_REPORT, f"{SWANTON_REP_C}: Betty Cheney's "
                              "one-year term expired in 2026; the "
                              "successor is published in no "
                              "official source in hand")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Swanton Justices of the Peace", 15,
           [jp_src("lists fifteen Town of Swanton justices of "
                   "the peace: Tamar Bouchard, Randy Brock, "
                   "Nicholas A. Brosseau, Donald Collins, Edward "
                   "Daniel, Stephanie Gagne, Steven D. Pike, "
                   "Pamela Pouliot, Jeffery 'Jeff' Raleigh, "
                   "Joseph 'Joe' Raleigh, Brian Savage, Alan "
                   "Shannon, Neal Speer, Matthew E. Walker, and "
                   "Suzanne Washburn. Village of Swanton "
                   "residents vote in this election, so the "
                   "village has no justice of the peace post of "
                   "its own")],
           [holder("Tamar Bouchard", "tamar-bouchard"),
            holder("Randy Brock", "randy-brock",
                   existing_person_id="ocd-person/351d1b5d-e438-5984-b81d-14f8eaada494"),
            holder("Nicholas A. Brosseau", "nicholas-a-brosseau"),
            holder("Donald Collins", "donald-collins"),
            holder("Edward Daniel", "edward-daniel"),
            holder("Stephanie Gagne", "stephanie-gagne"),
            holder("Steven D. Pike", "steven-d-pike"),
            holder("Pamela Pouliot", "pamela-pouliot"),
            holder("Jeffery \"Jeff\" Raleigh",
                   "jeffery-jeff-raleigh"),
            holder("Joseph \"Joe\" Raleigh", "joseph-joe-raleigh"),
            holder("Brian K. Savage", "brian-k-savage",
                   ballot_name="Brian Savage"),
            holder("Alan Shannon", "alan-shannon"),
            holder("Neal Speer", "neal-speer"),
            holder("Matthew E. Walker", "matthew-e-walker"),
            holder("Suzanne Washburn", "suzanne-washburn")]),
], jp=jp_election("swanton-71725-vt", "Town of Swanton", 15,
                  "the certified listing names fifteen winners "
                  "for the Town of Swanton's fifteen justice of "
                  "the peace seats"))

# ----------------------------------------------------------------
# Village of Swanton (Franklin County) -- ch. 279 charter.
SPECS["swanton"] = spec("swanton", "Village of Swanton", [
    office("village-president", "Village President",
           "Village of Swanton Village President", 1,
           [charter279("section 4: the Village President is "
                       "elected to a one-year term"),
            S(SWANTON_TRUSTEES, "Village of Swanton official "
                                "website, Trustees page: David "
                                "Winchester is Village President, "
                                "term to March 2027")],
           [holder("David Winchester", "david-winchester")]),
    office("village-trustee", "Village Trustee",
           "Village of Swanton Board of Trustees", 3,
           [charter279("section 4: the Board of Trustees is "
                       "three trustees elected to staggered "
                       "three-year terms"),
            S(SWANTON_TRUSTEES, "Village of Swanton official "
                                "website, Trustees page: Suzie "
                                "Kelleher (term to 2027) and "
                                "Damon Broderick (to 2029)"),
            S(SWANTON_ADMIN, "Village of Swanton official "
                             "website, Administration page: "
                             "names Neal Speer as a Village "
                             "Trustee (he is also a Town of "
                             "Swanton justice of the peace; one "
                             "person record carries both "
                             "memberships)")],
           [holder("Damon Broderick", "damon-broderick"),
            holder("Suzie Kelleher", "suzie-kelleher"),
            holder("Neal Speer", "neal-speer",
                   person_scope="swanton-71725")]),
    office("village-clerk", "Village Clerk",
           "Village of Swanton Village Clerk", 1,
           [charter279("section 6: the Village Clerk is elected "
                       "to a one-year term"),
            S(SWANTON_TRUSTEES, "Village of Swanton official "
                                "website, Trustees page: styles "
                                "Dianne Day 'Village Clerk & "
                                "Treasurer'")],
           [holder("Dianne Day", "dianne-day")]),
    office("village-treasurer", "Village Treasurer",
           "Village of Swanton Village Treasurer", 1,
           [charter279("section 7: the Village Treasurer is "
                       "appointed by the Board of Trustees"),
            S(SWANTON_TRUSTEES, "Village of Swanton official "
                                "website, Trustees page: Dianne "
                                "Day serves as Village Treasurer "
                                "as the Board's appointee")],
           [holder("Dianne Day", "dianne-day",
                   how_seated="appointed")]),
])

# ----------------------------------------------------------------
# Town of Tinmouth (Rutland County) -- general law.
TINMOUTH_REP_C = ("Town of Tinmouth, 2025 Town Report, 'ELECTED "
                  "TOWN AND SCHOOL OFFICERS' page")
TINMOUTH_OFF_C = ("Town of Tinmouth official website, boards, "
                  "commissions, committees and officials page")
SPECS["tinmouth"] = spec("tinmouth", "Town of Tinmouth", [
    office("town-clerk", "Town Clerk",
           "Town of Tinmouth Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(TINMOUTH_REPORT, f"{TINMOUTH_REP_C}: Gail Fallar, "
                               "Town Clerk (asterisked: term "
                               "expired 2026)"),
            guide("lists Gail Fallar as Tinmouth's Town Clerk"),
            clerk_xlsx("names Gail Fallar as Tinmouth's Town "
                       "Clerk (June 2026, postdating the March "
                       "2026 town meeting); she is seated on "
                       "disclosed incumbency continuity"),
            S(TINMOUTH_OFFICIALS, f"{TINMOUTH_OFF_C}: confirms "
                                  "one person customarily holds "
                                  "the clerkship and treasurership")],
           [holder("Gail Fallar", "gail-fallar")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Tinmouth Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(TINMOUTH_REPORT, f"{TINMOUTH_REP_C}: Gail Fallar, "
                               "Town Treasurer (asterisked: term "
                               "expired 2026)"),
            guide("lists Gail Fallar as Tinmouth's Town "
                  "Treasurer; she is seated on disclosed "
                  "incumbency continuity (see the clerk sources)")],
           [holder("Gail Fallar", "gail-fallar")]),
    office("selectboard", "Selectboard Member",
           "Town of Tinmouth Selectboard", 3,
           [S(TINMOUTH_OFFICIALS, f"{TINMOUTH_OFF_C}: names "
                                  "Kevin Eaton (Chair) and "
                                  "Melody Squier"),
            S(TINMOUTH_REPORT, f"{TINMOUTH_REP_C}: Kevin Eaton "
                               "(term to 2028) and Melody Squier "
                               "(to 2027); Judy Gilmore's seat "
                               "expired in 2026 and its outcome "
                               "is published in no official "
                               "source in hand, so she is not "
                               "seated")],
           [holder("Kevin Eaton", "kevin-eaton"),
            holder("Melody Squier", "melody-squier")]),
    office("road-commissioner", "Road Commissioner",
           "Town of Tinmouth Road Commissioner", 1,
           [S(TINMOUTH_REPORT, f"{TINMOUTH_REP_C}: Tinmouth "
                               "elects a Road Commissioner; Eric "
                               "Buffum, term to 2027"),
            S(TINMOUTH_OFFICIALS, f"{TINMOUTH_OFF_C}: names Eric "
                                  "Buffum as Road Commissioner")],
           [holder("Eric Buffum", "eric-buffum")]),
    office("lister", "Lister",
           "Town of Tinmouth Listers", 3,
           [statute2646("towns elect three listers on staggered "
                        "three-year terms"),
            S(TINMOUTH_REPORT, f"{TINMOUTH_REP_C}: Pat Psholka "
                               "(term to 2027) and Rick Fallar "
                               "(to 2028); Gail Fallar's lister "
                               "seat expired in 2026 and its "
                               "outcome is unpublished")],
           [holder("Pat Psholka", "pat-psholka"),
            holder("Rick Fallar", "rick-fallar")]),
    office("auditor", "Auditor",
           "Town of Tinmouth Auditors", 3,
           [statute2646("towns elect auditors (three, staggered "
                        "terms) unless the office is eliminated"),
            S(TINMOUTH_REPORT, f"{TINMOUTH_REP_C}: Gene Usher "
                               "(term to 2027) and Sandy Goyette "
                               "(to 2028); Ann Czar's seat expired "
                               "in 2026 and its outcome is "
                               "unpublished")],
           [holder("Gene Usher", "gene-usher"),
            holder("Sandy Goyette", "sandy-goyette")]),
    office("moderator", "Town Moderator",
           "Town of Tinmouth Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term"),
            S(TINMOUTH_REPORT, f"{TINMOUTH_REP_C}: Holly Ross's "
                               "one-year moderator term expired "
                               "in 2026; the outcome is published "
                               "in no official source in hand")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Tinmouth Collector of Delinquent Taxes", 1,
           [statute2646_structure("towns elect a collector of "
                                  "delinquent taxes"),
            S(TINMOUTH_REPORT, f"{TINMOUTH_REP_C}: Catherine "
                               "Yoder's term expired in 2026; the "
                               "outcome is published in no "
                               "official source in hand")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Tinmouth Justices of the Peace", 5,
           [jp_src("lists five Tinmouth justices of the peace: "
                   "Nelson Jaquay, Marshall Squier, Alan Gilmore, "
                   "Anna Majorell, and Michael Fallar")],
           [holder("Nelson Jaquay", "nelson-jaquay"),
            holder("Marshall Squier", "marshall-squier"),
            holder("Alan Gilmore", "alan-gilmore"),
            holder("Anna Majorell", "anna-majorell"),
            holder("Michael Fallar", "michael-fallar")]),
], jp=jp_election("tinmouth-vt", "Town of Tinmouth", 5,
                  "the certified listing names five winners for "
                  "Tinmouth's five justice of the peace seats",
                  extra_sources=[S(TINMOUTH_REPORT,
                                   f"{TINMOUTH_REP_C}: lists the "
                                   "same five justices of the "
                                   "peace")]))

# ----------------------------------------------------------------
# Town of Topsham (Orange County) -- general law.
TOPSHAM_TM_C = ("Town of Topsham, summary of the minutes of the "
                "town meeting of March 5, 2024 (town website)")
TOPSHAM_OFF_C = ("Town of Topsham official website, Town "
                 "Officials and Employees page")
SPECS["topsham"] = spec("topsham", "Town of Topsham", [
    office("moderator", "Town Moderator",
           "Town of Topsham Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(TOPSHAM_TM, f"{TOPSHAM_TM_C}: Henry Buermeyer was "
                          "elected Moderator"),
            S(TOPSHAM_OFFICIALS, f"{TOPSHAM_OFF_C}: still names "
                                 "Henry Buermeyer as Moderator")],
           [holder("Henry Buermeyer", "henry-buermeyer")]),
    office("town-clerk", "Town Clerk",
           "Town of Topsham Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(TOPSHAM_TM, f"{TOPSHAM_TM_C}: Karen Walker won "
                          "the town clerk's three-year term by "
                          "paper ballot, 79-29 over Kara Appleton, "
                          "so the term runs into 2027"),
            guide("lists Karen Walker as Topsham's Town Clerk"),
            clerk_xlsx("names Karen Walker as Topsham's Town "
                       "Clerk")],
           [holder("Karen Walker", "karen-walker")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Topsham Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(TOPSHAM_TM, f"{TOPSHAM_TM_C}: Karen Walker holds "
                          "the treasurer's three-year term won "
                          "at the same 2024 meeting"),
            guide("lists Karen Walker as Topsham's Town "
                  "Treasurer")],
           [holder("Karen Walker", "karen-walker")]),
    office("selectboard", "Selectboard Member",
           "Town of Topsham Selectboard", 5,
           [S(TOPSHAM_OFFICIALS, f"{TOPSHAM_OFF_C}: names Jim "
                                 "Bulger, Tom Otterman, Carl "
                                 "Hildebrandt, Jake Thompson, "
                                 "and Brad Calhoun"),
            S(TOPSHAM_TM, f"{TOPSHAM_TM_C}: James Bulger chairs "
                          "the board; Tom Otterman and Brad "
                          "Calhoun won their seats at the 2024 "
                          "meeting (Calhoun by paper ballot, "
                          "58-52)")],
           [holder("Jim Bulger", "jim-bulger"),
            holder("Tom Otterman", "tom-otterman"),
            holder("Carl Hildebrandt", "carl-hildebrandt"),
            holder("Jake Thompson", "jake-thompson"),
            holder("Brad Calhoun", "brad-calhoun")]),
    office("lister", "Lister",
           "Town of Topsham Listers", 3,
           [statute2646("towns elect three listers on staggered "
                        "three-year terms"),
            S(TOPSHAM_OFFICIALS, f"{TOPSHAM_OFF_C}: names Amelia "
                                 "Evans, John Hood, and Pam "
                                 "Langlitz as listers"),
            S(TOPSHAM_TM, f"{TOPSHAM_TM_C}: Pam Langlitz won her "
                          "lister seat at the 2024 meeting by "
                          "paper ballot, 52-47")],
           [holder("Amelia Evans", "amelia-evans"),
            holder("John Hood", "john-hood"),
            holder("Pam Langlitz", "pam-langlitz")]),
    office("auditor", "Auditor",
           "Town of Topsham Auditors", 3,
           [statute2646("towns elect auditors (three, staggered "
                        "terms) unless the office is eliminated"),
            S(TOPSHAM_OFFICIALS, f"{TOPSHAM_OFF_C}: names Peggy "
                                 "Welch and Nancy Frost as the "
                                 "town's auditors"),
            S(TOPSHAM_TM, f"{TOPSHAM_TM_C}: the 2024 meeting "
                          "drew no auditor nominations at all; "
                          "Welch and Frost are seated on the "
                          "current officials page's presentation "
                          "of them as the town's auditors")],
           [holder("Peggy Welch", "peggy-welch"),
            holder("Nancy Frost", "nancy-frost")]),
    office("constable", "Constable",
           "Town of Topsham Constable", 1,
           [statute2646("towns elect a constable"),
            S(TOPSHAM_OFFICIALS, f"{TOPSHAM_OFF_C}: lists David "
                                 "Mott as Constable among the "
                                 "town officers")],
           [holder("David Mott", "david-mott")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Topsham Collector of Delinquent Taxes", 1,
           [statute2646_structure("towns elect a collector of "
                                  "delinquent taxes"),
            S(TOPSHAM_TM, f"{TOPSHAM_TM_C}: Cynthia Flannigan won "
                          "the one-year office in 2024; no "
                          "current holder is published")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Topsham Justices of the Peace", 5,
           [jp_src("lists five Topsham justices of the peace: "
                   "Donna Otterman, Yvette Tomlinson, Larry Hart "
                   "Sr., Sheila Herman, and Dylan Magwire")],
           [holder("Donna Otterman", "donna-otterman"),
            holder("Yvette Tomlinson", "yvette-tomlinson"),
            holder("Larry Hart Sr.", "larry-hart-sr",
                   ballot_name="Larry Hart Sr.",
                   existing_person_id="ocd-person/4bb39537-886b-5eca-b8d4-d059e24b00b5"),
            holder("Sheila Herman", "sheila-herman"),
            holder("Dylan Magwire", "dylan-magwire")]),
], jp=jp_election("topsham-vt", "Town of Topsham", 5,
                  "the certified listing names five winners for "
                  "Topsham's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Townshend (Windham County) -- general law; signed 2026
# town meeting minutes and the 2026 warning in hand.
TOWNSHEND_MIN_C = ("Town of Townshend, signed minutes of the "
                   "annual town meeting of March 3, 2026 (town "
                   "website)")
TOWNSHEND_REP_C = ("Town of Townshend, 2026 Town Report, Warning "
                   "for the annual town meeting (town website)")
SPECS["townshend"] = spec("townshend", "Town of Townshend", [
    office("moderator", "Town Moderator",
           "Town of Townshend Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(TOWNSHEND_MINUTES, f"{TOWNSHEND_MIN_C}: David "
                                  "Liebow was re-elected "
                                  "Moderator")],
           [holder("David Liebow", "david-liebow")]),
    office("town-clerk", "Town Clerk",
           "Town of Townshend Town Clerk", 1,
           [statute2646("towns elect a town clerk; Townshend "
                        "elects its clerk to one-year terms"),
            S(TOWNSHEND_MINUTES, f"{TOWNSHEND_MIN_C}: Ellenka "
                                  "Wilson was elected Town Clerk"),
            guide("lists Ellenka Wilson as Townshend's Town "
                  "Clerk"),
            clerk_xlsx("names Ellenka Wilson as Townshend's Town "
                       "Clerk")],
           [holder("Ellenka Wilson", "ellenka-wilson")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Townshend Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(TOWNSHEND_MINUTES, f"{TOWNSHEND_MIN_C}: the "
                                  "Guide's Elaine Hill declined "
                                  "the nomination at the 2026 "
                                  "meeting and Elisha Stratford "
                                  "was elected Town Treasurer"),
            guide("lists Elaine Hill as Townshend's Town "
                  "Treasurer -- stale; the 2026 minutes govern "
                  "(see the minutes note)")],
           [holder("Elisha Stratford", "elisha-stratford")]),
    office("selectboard", "Selectboard Member",
           "Town of Townshend Selectboard", 5,
           [S(TOWNSHEND_SB, "Town of Townshend official website, "
                            "Selectboard page: names Nick Suarez "
                            "(Chair), Catherine Marrow (Vice "
                            "Chair), Rob Wright, Alene Evans, and "
                            "Steve Frisk"),
            S(TOWNSHEND_MINUTES, f"{TOWNSHEND_MIN_C}: Catherine "
                                  "Marrow, Rob Wright, and Steve "
                                  "Frisk won the three 2026 "
                                  "seats")],
           [holder("Nick Suarez", "nick-suarez"),
            holder("Catherine Marrow", "catherine-marrow"),
            holder("Rob Wright", "rob-wright"),
            holder("Alene Evans", "alene-evans"),
            holder("Steve Frisk", "steve-frisk")]),
    office("lister", "Lister",
           "Town of Townshend Listers", 3,
           [statute2646("towns elect three listers on staggered "
                        "three-year terms"),
            S(TOWNSHEND_LISTERS, "Town of Townshend official "
                                 "website, Listers page: names "
                                 "Mike Bills, Helen Holt, and "
                                 "Eugene Kuch (Holt is a "
                                 "different person from "
                                 "Brookline's appointed lister of "
                                 "the same name -- listers must "
                                 "reside in the town they serve)"),
            S(TOWNSHEND_MINUTES, f"{TOWNSHEND_MIN_C}: Eugene "
                                  "Kuch won the 2026 three-year "
                                  "lister seat")],
           [holder("Mike Bills", "mike-bills"),
            holder("Helen Holt", "helen-holt"),
            holder("Eugene Kuch", "eugene-kuch")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Townshend Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes"),
            S(TOWNSHEND_MINUTES, f"{TOWNSHEND_MIN_C}: Becky "
                                  "Nystrom Reilly was elected "
                                  "Collector of Delinquent Taxes")],
           [holder("Becky Nystrom Reilly", "becky-nystrom-reilly")]),
    office("first-constable", "First Constable",
           "Town of Townshend First Constable", 1,
           [statute2646("towns elect constables"),
            S(TOWNSHEND_MINUTES, f"{TOWNSHEND_MIN_C}: Warren "
                                  "Beattie was elected First "
                                  "Constable")],
           [holder("Warren Beattie", "warren-beattie")]),
    office("second-constable", "Second Constable",
           "Town of Townshend Second Constable", 1,
           [statute2646("towns elect constables"),
            S(TOWNSHEND_MINUTES, f"{TOWNSHEND_MIN_C}: Mike Cutts "
                                  "was elected Second Constable")],
           [holder("Mike Cutts", "mike-cutts")]),
    office("library-trustee", "Library Trustee",
           "Town of Townshend Library Trustees", 5,
           [S(TOWNSHEND_LIBRARY, "Town of Townshend official "
                                 "website, Library Trustees page: "
                                 "names Sandy Glaser, Miriam "
                                 "Schuldenfrei, Katherine "
                                 "Dugrenier, Judy Slowik, and "
                                 "Elizabeth Brown"),
            S(TOWNSHEND_MINUTES, f"{TOWNSHEND_MIN_C}: Sandy "
                                  "Glaser won the 2026 five-year "
                                  "seat after Marilee Attley "
                                  "declined")],
           [holder("Sandy Glaser", "sandy-glaser"),
            holder("Miriam Schuldenfrei", "miriam-schuldenfrei"),
            holder("Katherine Dugrenier", "katherine-dugrenier"),
            holder("Judy Slowik", "judy-slowik"),
            holder("Elizabeth Brown", "elizabeth-brown")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Townshend Cemetery Commissioners", 5,
           [S(TOWNSHEND_CEMETERY, "Town of Townshend official "
                                  "website, Cemetery Commission "
                                  "page: names Scott Nystrom, "
                                  "Tim Massucco, Jay Warren, "
                                  "Charles Marchant, and Paula "
                                  "Newton"),
            S(TOWNSHEND_REPORT, f"{TOWNSHEND_REP_C}: the warning "
                                 "sets five-year staggered terms "
                                 "(Nystrom to 2031, Newton to "
                                 "2030, Massucco to 2029, Warren "
                                 "to 2028, Marchant to 2027); "
                                 "Massucco was elected to the "
                                 "remainder of departed member "
                                 "Bruce Bills's seat and Jay "
                                 "Warren, first appointed to his "
                                 "seat, was elected to its "
                                 "remainder")],
           [holder("Scott Nystrom", "scott-nystrom"),
            holder("Tim Massucco", "tim-massucco"),
            holder("Jay Warren", "jay-warren"),
            holder("Charles Marchant", "charles-marchant"),
            holder("Paula Newton", "paula-newton")]),
    office("planning-commissioner", "Planning Commissioner",
           "Town of Townshend Planning Commission", 5,
           [S(TOWNSHEND_PC, "Town of Townshend official website, "
                            "Planning Commission page: names Doug "
                            "Ballentine (Chair), John Evans, and "
                            "Rick Matschke"),
            S(TOWNSHEND_REPORT, f"{TOWNSHEND_REP_C}: the warning "
                                 "elects planning commissioners "
                                 "under 24 V.S.A. section 4323 "
                                 "(Ballentine to 2028, Evans to "
                                 "2027, Matschke to 2030); the two "
                                 "seats warned in 2026 (a "
                                 "five-year seat and a "
                                 "three-years-remaining seat) have "
                                 "no winners recorded in the "
                                 "minutes")],
           [holder("Doug Ballentine", "doug-ballentine"),
            holder("John Evans", "john-evans"),
            holder("Rick Matschke", "rick-matschke")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Townshend Justices of the Peace", 7,
           [jp_src("lists seven Townshend justices of the peace: "
                   "Elizabeth Brown, Alene 'Allie' Evans, "
                   "Kathleen 'Kathy' Greve, Barbara Guerrero, "
                   "Constance 'Connie' Holt, Catherine 'Katie' "
                   "Marrow, and Ellenka Wilson")],
           [holder("Elizabeth Brown", "elizabeth-brown"),
            holder("Alene Evans", "alene-evans",
                   ballot_name="Alene 'Allie' Evans"),
            holder("Kathleen \"Kathy\" Greve",
                   "kathleen-kathy-greve"),
            holder("Barbara Guerrero", "barbara-guerrero"),
            holder("Constance \"Connie\" Holt",
                   "constance-connie-holt"),
            holder("Catherine Marrow", "catherine-marrow",
                   ballot_name="Catherine 'Katie' Marrow"),
            holder("Ellenka Wilson", "ellenka-wilson")]),
], jp=jp_election("townshend-vt", "Town of Townshend", 7,
                  "the certified listing names seven winners for "
                  "Townshend's seven justice of the peace seats",
                  extra_sources=[S(TOWNSHEND_BCA,
                                   "Town of Townshend official "
                                   "website, Board of Civil "
                                   "Authority page: names the "
                                   "town's justices of the "
                                   "peace")]))

# ----------------------------------------------------------------
# Town of Thetford (Orange County) -- general law with a town
# manager (since 2019); researched via a delegated read of the
# bot-gated town website (October 20, 2026): the town's 'Elected
# and Appointed Officers' roster (updated September 22, 2026)
# and the 2025 Annual Report's elected-officials pages.
THETFORD_ROSTER = {"url": "https://www.thetfordvt.gov",
                   "note": "PLACEHOLDER"}
THETFORD_REPORT = {"url": "https://www.thetfordvt.gov",
                   "note": "PLACEHOLDER"}
THETFORD_ROSTER_C = ("Town of Thetford, 'Elected and Appointed "
                     "Officers' roster (updated September 22, "
                     "2026; town website)")
THETFORD_REP_C = ("Town of Thetford, 2025 Annual Report (for the "
                  "March 2026 town meeting), 'THETFORD ELECTED "
                  "OFFICIALS' pages 1-2")
SPECS["thetford"] = spec("thetford", "Town of Thetford", [
    office("moderator", "Town Moderator",
           "Town of Thetford Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(THETFORD_ROSTER, f"{THETFORD_ROSTER_C}: names "
                               "Sarah Aspell as Town Moderator "
                               "(the roster prints her one-year "
                               "term as expiring in 2026 -- the "
                               "same stale-line anomaly as the "
                               "town clerk's line; the roster is "
                               "the town's current post-election "
                               "roster and presents her as the "
                               "sitting moderator). She is also "
                               "School Moderator, a school office "
                               "not modeled here")],
           [holder("Sarah Aspell", "sarah-aspell")]),
    office("town-clerk", "Town Clerk",
           "Town of Thetford Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(THETFORD_ROSTER, f"{THETFORD_ROSTER_C}: names "
                               "Tracy Borst as Town Clerk, and "
                               "the town's Town Clerk page "
                               "identifies her as the sitting "
                               "clerk. Both the roster and the "
                               "annual report print her "
                               "three-year term as expiring in "
                               "2026 even though the March 2026 "
                               "election has passed -- the line "
                               "appears stale; she is seated on "
                               "the live clerk page and the "
                               "Secretary of State concurrence"),
            guide("lists Tracy Borst as Thetford's Town Clerk"),
            clerk_xlsx("names Tracy Borst as Thetford's Town "
                       "Clerk (June 2026, postdating the March "
                       "2026 town meeting)")],
           [holder("Tracy Borst", "tracy-borst")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Thetford Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(THETFORD_ROSTER, f"{THETFORD_ROSTER_C}: names "
                               "Tracy Borst as Town Treasurer, "
                               "term to 2028"),
            guide("lists Tracy Borst as Thetford's Town "
                  "Treasurer"),
            treas_xlsx("names Tracy Borst as Thetford's Town "
                       "Treasurer")],
           [holder("Tracy Borst", "tracy-borst")]),
    office("selectboard", "Selectboard Member",
           "Town of Thetford Selectboard", 5,
           [S(THETFORD_ROSTER, f"{THETFORD_ROSTER_C}: names "
                               "Sharon Harkay (Chair, term to "
                               "2029), David Goodrich (Vice "
                               "Chair, to 2028), David Forbes "
                               "(to 2028), Li Shen (to 2027), "
                               "and Steve Tofel (to 2027)"),
            S(THETFORD_REPORT, f"{THETFORD_REP_C}: the "
                               "pre-election roster confirms the "
                               "same five members, with Harkay's "
                               "and Goodrich's seats standing in "
                               "2026"),
            sb_dir("names David Forbes, David Goodrich, Sharon "
                   "Harkay (Chair), Li Shen, and Steven Tofel "
                   "for Thetford's five-member board")],
           [holder("David Forbes", "david-forbes"),
            holder("David Goodrich", "david-goodrich"),
            holder("Sharon Harkay", "sharon-harkay"),
            holder("Li Shen", "li-shen"),
            holder("Steven Tofel", "steven-tofel")]),
    office("lister", "Lister",
           "Town of Thetford Listers", 3,
           [statute2646("towns elect three listers on staggered "
                        "three-year terms"),
            S(THETFORD_ROSTER, f"{THETFORD_ROSTER_C}: names Sean "
                               "Boyce (term to 2027), Sue Howard "
                               "(printed as expiring 2026 -- her "
                               "seat stood at the March 2026 "
                               "meeting and the updated September "
                               "roster still presents her as a "
                               "sitting lister), and Barbara "
                               "Harrington (to 2028)")],
           [holder("Sean Boyce", "sean-boyce"),
            holder("Sue Howard", "sue-howard"),
            holder("Barbara Harrington", "barbara-harrington")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Thetford Cemetery Commissioners", 5,
           [S(THETFORD_ROSTER, f"{THETFORD_ROSTER_C}: names Sam "
                               "Eaton (term to 2027), Ruth "
                               "MacKinnon (to 2028), Ellen Stone "
                               "(to 2029), Richard Landry (to "
                               "2030), and Keith Waterman (to "
                               "2031) on five-year staggered "
                               "terms"),
            S(THETFORD_REPORT, f"{THETFORD_REP_C}: the "
                               "pre-election roster shows "
                               "Landry's, Stone's, and Waterman's "
                               "seats expiring in 2026; the "
                               "September roster's new expiries "
                               "reflect their March 2026 "
                               "re-elections")],
           [holder("Sam Eaton", "sam-eaton"),
            holder("Richard Landry", "richard-landry"),
            holder("Ruth MacKinnon", "ruth-mackinnon"),
            holder("Ellen Stone", "ellen-stone"),
            holder("Keith Waterman", "keith-waterman")]),
    office("trustee-of-public-funds", "Trustee of Trust Funds",
           "Town of Thetford Trustees of Trust Funds", 3,
           [statute2646("towns elect trustees of public funds; "
                        "Thetford styles the office Trustees of "
                        "Trust Funds"),
            S(THETFORD_ROSTER, f"{THETFORD_ROSTER_C}: names Joe "
                               "Tofel (term to 2027), J. Rick "
                               "Hoffman (to 2028), and Charlie "
                               "Buttrey (to 2029)"),
            S(THETFORD_REPORT, f"{THETFORD_REP_C}: the "
                               "pre-election roster carried "
                               "Priscilla Hall (term expiring "
                               "2026) in the seat the September "
                               "roster gives to Charlie Buttrey")],
           [holder("Charlie Buttrey", "charlie-buttrey"),
            holder("J. Rick Hoffman", "j-rick-hoffman"),
            holder("Joe Tofel", "joe-tofel")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Thetford Justices of the Peace", 10,
           [jp_src("lists ten Thetford justices of the peace: "
                   "Richard Balagur, Martie Betts, Robin Brown, "
                   "Wendy Cole, Jessica Eaton, Gregory Kasten, "
                   "Bill Keegan, Diana Kimball Anderson, Orin "
                   "Pacht, and Kate Van Arman (the town roster "
                   "hyphenates Kimball-Anderson; the certified "
                   "listing's form governs)")],
           [holder("Richard Balagur", "richard-balagur"),
            holder("Martie Betts", "martie-betts"),
            holder("Robin Brown", "robin-brown"),
            holder("Wendy Cole", "wendy-cole"),
            holder("Jessica Eaton", "jessica-eaton"),
            holder("Gregory Kasten", "gregory-kasten"),
            holder("Bill Keegan", "bill-keegan"),
            holder("Diana Kimball Anderson",
                   "diana-kimball-anderson"),
            holder("Orin Pacht", "orin-pacht"),
            holder("Kate Van Arman", "kate-van-arman")]),
], jp=jp_election("thetford-vt", "Town of Thetford", 10,
                  "the certified listing names ten winners for "
                  "Thetford's ten justice of the peace seats",
                  extra_sources=[S(THETFORD_ROSTER,
                                   f"{THETFORD_ROSTER_C}: lists "
                                   "the same ten justices of "
                                   "the peace")]))

ORDER = ["stratton", "sudbury", "sunderland", "sutton",
         "swanton-71725", "swanton", "thetford", "tinmouth",
         "topsham", "townshend"]

for slug in ORDER:
    (OUT / f"{slug}.json").write_text(
        json.dumps(SPECS[slug], indent=1) + "\n")
print("wrote", len(ORDER), "specs")
