#!/usr/bin/env python3
"""Batch 28 of the VT #163 municipal fan-out (alphabetical positions
270-278, the final alphabetical batch): Windsor, Winhall, Winooski,
Wolcott, Woodbury, Woodford, Woodstock (town), Woodstock (village),
Worcester. Emits one JSON spec per municipality for
build_vt_municipality.py. Research: vt_muni_batch28_research.md.

Identity calls baked into this batch (all flagged on #163):
- Windsor: the March 3, 2026 ballot carried NO printed candidates for
  Moderator, Clerk, Treasurer, three Lister seats, or two Trustee of
  Public Funds seats (all write-in only) and no certified tally or
  current roster naming the winners is published -- all five offices
  are POSTS ONLY and their last known holders are stragglers. Ch. 173
  sec. 29(d) abolishes auditor, grand juror, and town agent, so no
  posts exist for them; the constable is a permissive appointment
  (sec. 29(a)(9)) with no published holder -- no post. JP Ryan Palmer
  REUSES his Windsor County sheriff record; the operator appends his
  JP candidacy to that record.
- Winhall: the SB member sits as Christie Boswell (certified JP
  listing, the certified 2026 return, and the live SB page); the town
  report's "Christina" is the outlier. Debra Avison is Town Treasurer
  (report elected table + SOS Guide); an undated clerk-directory PDF
  naming Elizabeth Grant as treasurer is the disclosed outlier.
  Alexander W. Bilka holds Listers, Town Agent, and Grand Juror on
  one record. The DTC and the single cemetery commissioner are
  APPOINTED per the report's appointed-officials table (printed
  terms ran to June 30, 2026; renewals unpublished).
- Winooski: Mayor Thomas Renner won the one-year remainder of the
  unexpired mayoral term in the certified March 3, 2026 return; Al
  Turkos won a one-year remainder of a two-year council term. City
  Clerk Jenny Willingham and City Treasurer Johnathan Fenney are
  APPOINTED (ch. 19 sec. 506(b); the treasurer is not enumerated in
  sec. 506(c) -- the sec. 506(a) import plus the manager-appointment
  rule is the stated basis). JPs Daisy Berbeco and Chloe Tomlinson
  REUSE their Chittenden-21 state representative records; the
  operator appends their JP candidacies.
- Wolcott: SB member Richard Lee departed mid-term; Dolan Patrick
  sits APPOINTED (hybrid post). Belinda Harris Clegg holds Clerk and
  Treasurer on one record. The library board is hybrid per the town
  report's own layout (two appointed trustees minted; the expired
  elected seats and the printed-vacant appointed seat unfilled).
  Moderator Joe Hester-Ingram, lister W. Samuel Hill, cemetery
  commissioner Lucien Gravel, and library trustees Johanna Duff and
  Anne LeRiche are stragglers -- their seats stood in 2026 and the
  outcomes are unpublished.
- Woodbury: Town Treasurer is minted Lillian Baron (the SOS
  treasurer spreadsheet's full form) over the town directory's
  "Lilly Baron". Town Clerk Graham Christie follows the June 2026
  SOS spreadsheet over the Guide's stale "R Durkee". Ron Wells holds
  Listers (chair) and DTC on one record; Susan Stitely holds
  Cemetery Commissioners (chair) and JP. First Constable Andrew
  Delaney and Road Commissioner Peter Dailey are APPOINTED per the
  directory's own labels.
- Woodford: listers were ELIMINATED by voter approval March 1, 2022
  (replaced by an outside assessing firm) -- the vote controls over
  ch. 175 sec. 8(3), so NO lister post, flagged. Trustees of Public
  Funds are the SB plus the Treasurer ex officio (ch. 175 sec.
  8(a)) -- no separate post. Moderator (Richard Frantz), DTC (James
  Kinney), and the auditors (Virginia Ulitsch) are stragglers from
  the 2024 report -- posts only. An officers table naming other
  holders surfaced in one download pass but is not in the verified
  report on disk and coheres with nothing -- discarded as
  unverified and disclosed.
- Woodstock (town): the live SB page (Frates, Sweeney, Chiefsky,
  Ben Ford, Clay Reed) governs over the factory's stale four and
  the SOS directory's lone "Susan Ford"; the entire post-2025 board
  turned over by unpublished mechanisms. Auditors were ELIMINATED
  March 1, 2025 -- no post. F. Charles Degener III holds Clerk and
  Treasurer on one record. Moderator Matthew Maxham, TPF Lauren
  Thompson, and First Constable Kelly Linton are stragglers (their
  seats stood in 2026; outcomes unpublished). DTC Eric Duffy is
  APPOINTED (the report's annually-appointed list). The report's JP
  table (12 names incl. Soule, Baumgartner, Dunn) yields to the
  certified ten.
- Woodstock (village): the fourth trustee is minted Wendy Marinan
  (Village Report form "Wendy Wright Marinan") over the live page's
  "Werndy Marrinan". Clerk (Donald R. Wheeler), Treasurer (F.
  Charles Degener), Moderator (Greg Camp), and Trustee of Public
  Funds (Jill Davies) are POSTS ONLY -- the village's published
  rosters expired in 2025 and no later outcomes are published; the
  charter's Collector of Taxes post is likewise holderless. Ch. 291
  sec. 9 fire wardens are permissive under bylaws -- no post, joins
  the fire-officer scope question.
- Worcester: Town Treasurer Heather Pagel is APPOINTED -- the SOS
  sources name Katie Miller as treasurer into 2026, but the town's
  live directory presents Pagel at the treasurer's desk and Miller
  as DTC; the turnover's mechanism is unpublished (flagged). Pagel
  was separately ELECTED Cemetery Commissioner at the March 3, 2026
  meeting. Constable Shawn McManus is minted from the signed
  meeting minutes (the election record) over the directory's
  "McManis". Lister Jonathan Scherbatskoy takes the directory's
  full form over the minutes' "John Sherbatskoy". The cemetery
  board's size (3) is derived from the minutes' single-seat
  three-year election and the 18 V.S.A. sec. 5373 pattern --
  flagged; only Pagel's seat has a published holder.
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
CHARTER_173 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/173",
    "note": "PLACEHOLDER",
}
CHARTER_19 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/19",
    "note": "PLACEHOLDER",
}
CHARTER_175 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/175",
    "note": "PLACEHOLDER",
}
CHARTER_291 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/291",
    "note": "PLACEHOLDER",
}
STATUTE_5373 = {
    "url": "https://legislature.vermont.gov/statutes/section/18/121/05373",
    "note": "PLACEHOLDER",
}

WINDSOR_SB = {"url": "https://windsorvt.org/1230/Selectboard",
              "note": "PLACEHOLDER"}
WINDSOR_CLERK = {"url": "https://windsorvt.org/1219/Town-Clerk",
                 "note": "PLACEHOLDER"}
WINDSOR_TREAS = {"url": "https://windsorvt.org/1217/Town-Treasurer",
                 "note": "PLACEHOLDER"}
WINDSOR_WARNING = {"url": "https://windsorvt.org/DocumentCenter/View/2508",
                   "note": "PLACEHOLDER"}
WINDSOR_BALLOT = {"url": "https://windsorvt.org/DocumentCenter/View/2524",
                  "note": "PLACEHOLDER"}
WINDSOR_REPORT = {"url": "https://windsorvt.org/DocumentCenter/View/1956",
                  "note": "PLACEHOLDER"}
WINDSOR_JPLIST = {"url": "https://windsorvt.org/DocumentCenter/View/847",
                  "note": "PLACEHOLDER"}

WINHALL_RESULTS = {"url": "https://winhall.org/ElectionResults030326.pdf",
                   "note": "PLACEHOLDER"}
WINHALL_REPORT = {"url": "https://winhall.org/TownReportDraftFull.pdf",
                  "note": "PLACEHOLDER"}
WINHALL_SB = {"url": "https://winhall.org/government/select_board.php",
              "note": "PLACEHOLDER"}
WINHALL_ELECTIONS = {"url": "https://winhall.org/government/elections.php",
                     "note": "PLACEHOLDER"}

WINOOSKI_ORV = {"url": "https://winooskivt.gov/DocumentCenter/View/10778",
                "note": "PLACEHOLDER"}
WINOOSKI_COUNCIL = {"url": "https://winooskivt.gov/1473/City-Council",
                    "note": "PLACEHOLDER"}
WINOOSKI_CLERK = {"url": "https://winooskivt.gov/152/City-Clerks-Office",
                  "note": "PLACEHOLDER"}

WOLCOTT_REPORT = {"url": "https://wolcottvt.org/wp-content/uploads/2026/02/Wolcott-Town-Report-2025-1.4.pdf",
                  "note": "PLACEHOLDER"}
WOLCOTT_SB = {"url": "https://wolcottvt.org/selectboard/",
              "note": "PLACEHOLDER"}

WOODBURY_DIR = {"url": "https://woodburyvt.org/directory",
                "note": "PLACEHOLDER"}
WOODBURY_SB = {"url": "https://woodburyvt.org/select-board/",
               "note": "PLACEHOLDER"}
WOODBURY_CLERK = {"url": "https://woodburyvt.org/clerk/",
                  "note": "PLACEHOLDER"}

WOODFORD_REPORT = {"url": "https://woodfordvt.org/uploads/woodford-town-report-2024.pdf",
                   "note": "PLACEHOLDER"}

WSTOCK_SB = {"url": "https://townofwoodstock.org/boards-meetings/town-selectboard",
             "note": "PLACEHOLDER"}
WSTOCK_CLERK = {"url": "https://townofwoodstock.org/departments/town-clerk",
                "note": "PLACEHOLDER"}
WSTOCK_REPORT = {"url": "https://townofwoodstock.org/fileadmin/files/Boards_and_Committees/Finance_Committee/TownReport2026-Final07.30.26.pdf",
                 "note": "PLACEHOLDER"}
WSV_TRUSTEES = {"url": "https://townofwoodstock.org/boards-meetings/village-trustees",
                "note": "PLACEHOLDER"}
WSV_REPORT = {"url": "https://townofwoodstock.org/fileadmin/files/General/Village_Report-Final2025.pdf",
              "note": "PLACEHOLDER"}

WORC_MINUTES = {"url": "https://worcestervt.org/wp/public_html/wp/wp-content/uploads/2026/03/Worcester-Town-Meeting-3.3.2026.pdf",
                "note": "PLACEHOLDER"}
WORC_DIR = {"url": "https://worcestervt.org/wp/directory",
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


def charter173(phrase):
    return S(CHARTER_173, f"24 App. V.S.A. ch. 173 (Town of "
             f"Windsor): {phrase}")


def charter19(phrase):
    return S(CHARTER_19, f"24 App. V.S.A. ch. 19 (City of "
             f"Winooski): {phrase}")


def charter175(phrase):
    return S(CHARTER_175, f"24 App. V.S.A. ch. 175 (Town of "
             f"Woodford): {phrase}")


def charter291(phrase):
    return S(CHARTER_291, f"24 App. V.S.A. ch. 291 (Village of "
             f"Woodstock): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 28); issue #163 "
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
                  f"# municipal fan-out batch 28; issue #163 "
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
# Town of Windsor (Windsor County) -- charter ch. 173. Sources:
# the town site (windsorvt.org, CivicPlus): live Selectboard page,
# the March 3, 2026 warning and sample ballot (scanned, read from
# renders), the FY2023-24 town report, and the town's own JP list.
WINDSOR_WARN_C = ("Town of Windsor, Warning for the March 3, 2026 "
                  "annual town meeting (DocumentCenter/View/2508)")
WINDSOR_BALLOT_C = ("Town of Windsor, official sample ballot, "
                    "March 3, 2026 (DocumentCenter/View/2524)")
WINDSOR_REP_C = ("Town of Windsor, FY2023-24 Annual Town Report "
                 "(DocumentCenter/View/1956)")
SPECS["windsor"] = spec("windsor", "Town of Windsor", [
    office("selectboard", "Selectboard Member",
           "Town of Windsor Selectboard", 5,
           [charter173("sec. 11 (Subchapter 003) elects a "
                       "five-member selectboard: three members for "
                       "three-year terms and two for two-year terms"),
            sb_dir("names Tera Howard (Chair), Emma Caffrey "
                   "(Vice Chair), Jeffrey Johnson, Mary "
                   "McNaughton, and Heather Prebish for Windsor"),
            S(WINDSOR_SB, "Town of Windsor, Selectboard page "
              "(live): the same five members with term expiries "
              "-- Howard (2029), Johnson (2028), McNaughton "
              "(2028), Caffrey (2027), Prebish (2027); Howard's "
              "2029 expiry reflects his 2026 re-election"),
            S(WINDSOR_BALLOT, f"{WINDSOR_BALLOT_C}: the printed "
              "2026 selectboard contests -- the three-year seat "
              "and two two-year seats (one contested: Jeffrey "
              "Johnson over Eric Saltonstall)")],
           [holder("Tera Howard", "tera-howard"),
            holder("Emma Caffrey", "emma-caffrey"),
            holder("Jeffrey Johnson", "jeffrey-johnson"),
            holder("Mary McNaughton", "mary-mcnaughton"),
            holder("Heather Prebish", "heather-prebish")]),
    office("town-clerk", "Town Clerk",
           "Town of Windsor Town Clerk", 1,
           [charter173("sec. 11 elects a town clerk for a "
                       "three-year term"),
            S(WINDSOR_WARNING, f"{WINDSOR_WARN_C}: the 2026 ballot "
              "carried Town Clerk for the one-year remainder of a "
              "three-year term"),
            S(WINDSOR_BALLOT, f"{WINDSOR_BALLOT_C}: the clerk "
              "contest printed no candidate -- write-in only. No "
              "certified tally or current roster naming the "
              "winner is published, so no holder is minted; the "
              "office's history is carried as a straggler on "
              "issue #163"),
            S(WINDSOR_REPORT, f"{WINDSOR_REP_C}: Jane Mayhew held "
              "clerk (and treasurer) to 2027 and departed before "
              "the 2026 meeting, which is why a remainder term "
              "stood on the 2026 ballot")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Windsor Town Treasurer", 1,
           [charter173("sec. 11 elects a town treasurer for a "
                       "three-year term; the treasurer is ex "
                       "officio collector of current and delinquent "
                       "taxes"),
            S(WINDSOR_WARNING, f"{WINDSOR_WARN_C}: the 2026 ballot "
              "carried Town Treasurer for the one-year remainder "
              "of a three-year term"),
            S(WINDSOR_BALLOT, f"{WINDSOR_BALLOT_C}: the treasurer "
              "contest printed no candidate -- write-in only. No "
              "certified tally or current roster naming the "
              "winner is published, so no holder is minted; the "
              "office is carried as a straggler on issue #163"),
            guide("shows Windsor's treasurer seat as vacant")]),
    office("moderator", "Town Moderator",
           "Town of Windsor Town Moderator", 1,
           [charter173("sec. 11 elects a moderator for a one-year "
                       "term"),
            S(WINDSOR_BALLOT, f"{WINDSOR_BALLOT_C}: the moderator "
              "contest printed no candidate -- write-in only. No "
              "certified tally or current roster naming the "
              "winner is published, so no holder is minted; the "
              "office is carried as a straggler on issue #163"),
            S(WINDSOR_REPORT, f"{WINDSOR_REP_C}: the moderator "
              "line printed vacant")]),
    office("lister", "Lister",
           "Town of Windsor Listers", 3,
           [charter173("sec. 11 elects three listers"),
            S(WINDSOR_WARNING, f"{WINDSOR_WARN_C}: the 2026 ballot "
              "carried three lister seats"),
            S(WINDSOR_BALLOT, f"{WINDSOR_BALLOT_C}: the lister "
              "contests printed no candidates -- write-in only. "
              "No certified tally or current roster naming the "
              "winners is published, so no holders are minted; "
              "the seats are carried as stragglers on issue #163"),
            S(WINDSOR_REPORT, f"{WINDSOR_REP_C}: the lister lines "
              "printed vacant")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Windsor Trustees of Public Funds", 3,
           [charter173("sec. 11 elects three trustees of public "
                       "funds"),
            S(WINDSOR_WARNING, f"{WINDSOR_WARN_C}: the 2026 ballot "
              "carried two trustee of public funds seats"),
            S(WINDSOR_BALLOT, f"{WINDSOR_BALLOT_C}: the trustee "
              "contests printed no candidates -- write-in only. "
              "No certified tally or current roster naming the "
              "winners is published, so no holders are minted; "
              "the seats are carried as stragglers on issue #163"),
            S(WINDSOR_REPORT, f"{WINDSOR_REP_C}: Riley White held "
              "one trustee seat to 2025; the other lines printed "
              "vacant")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Windsor Justices of the Peace", 12,
           [jp_src("lists twelve Windsor justices of the peace: "
                   "William Ballantyne, Paul Belaski, Marianne N "
                   "Blake, Janet Farley, Linda Farnsworth, Patricia "
                   "Crikett French, Steve Giroux, Amy McMullen, "
                   "David Morin, Sara Morin, Ryan Palmer, and "
                   "Donna Sweaney"),
            S(WINDSOR_JPLIST, "Town of Windsor, Justices of the "
              "Peace list (DocumentCenter/View/847): names the "
              "same twelve")],
           [holder("William Ballantyne", "william-ballantyne"),
            holder("Paul Belaski", "paul-belaski"),
            holder("Marianne Blake", "marianne-blake",
                   ballot_name="Marianne N Blake"),
            holder("Janet Farley", "janet-farley"),
            holder("Linda Farnsworth", "linda-farnsworth"),
            holder("Patricia French", "patricia-french",
                   ballot_name="Patricia Crikett French"),
            holder("Steve Giroux", "steve-giroux"),
            holder("Amy McMullen", "amy-mcmullen"),
            holder("David Morin", "david-morin"),
            holder("Sara Morin", "sara-morin"),
            holder("Ryan Palmer", "ryan-palmer",
                   existing_person_id="ocd-person/489b6937-5dd5-5eb5-9aa1-9a43cde0c2ed"),
            holder("Donna Sweaney", "donna-sweaney")]),
], jp=jp_election("windsor-vt", "Town of Windsor", 12,
                  "certifies the November 5, 2024 election of "
                  "twelve justices of the peace for Windsor: "
                  "William Ballantyne, Paul Belaski, Marianne N "
                  "Blake, Janet Farley, Linda Farnsworth, Patricia "
                  "Crikett French, Steve Giroux, Amy McMullen, "
                  "David Morin, Sara Morin, Ryan Palmer, and Donna "
                  "Sweaney. Ryan Palmer is Windsor County's elected "
                  "sheriff; his existing county-tier record is "
                  "reused and the JP candidacy is appended to it"))

# ----------------------------------------------------------------
# Town of Winhall (Bennington County) -- general law. Sources:
# the certified Official Return of Votes, March 3, 2026 (scanned,
# read from renders), the 2026 Annual Town Report officers
# tables, and the live Selectboard page (winhall.org, Revize).
WINHALL_RET_C = ("Town of Winhall, Official Return of Votes, "
                 "March 3, 2026 (certified; attested by E. Stuart "
                 "Coleman and Elizabeth Grant)")
WINHALL_REP_C = ("Town of Winhall, 2026 Annual Town Report, "
                 "officers tables")
SPECS["winhall"] = spec("winhall", "Town of Winhall", [
    office("selectboard", "Selectboard Member",
           "Town of Winhall Selectboard", 5,
           [statute2646("towns elect a selectboard"),
            sb_dir("refers readers to the town's own roster for "
                   "Winhall"),
            S(WINHALL_SB, "Town of Winhall, Selectboard page "
              "(live): E. Stuart Coleman (Chair), Julie Isaacs "
              "(Vice Chair), Christie Boswell, Elizabeth Grant, "
              "and Stacy Eddy-Gordon"),
            S(WINHALL_RESULTS, f"{WINHALL_RET_C}: Christie Boswell "
              "elected to a two-year term (99 votes) and Stacy "
              "Eddy-Gordon re-elected to a three-year term (99 "
              "votes) in 2026"),
            S(WINHALL_REPORT, f"{WINHALL_REP_C}: Coleman (Chair, "
              "to 2027), Isaacs (Vice Chair, to 2028), Grant (to "
              "2027); Boswell was first appointed to a vacancy and "
              "then elected in 2026")],
           [holder("E. Stuart Coleman", "e-stuart-coleman"),
            holder("Julie Isaacs", "julie-isaacs"),
            holder("Christie Boswell", "christie-boswell"),
            holder("Elizabeth Grant", "elizabeth-grant"),
            holder("Stacy Eddy-Gordon", "stacy-eddy-gordon")]),
    office("town-clerk", "Town Clerk",
           "Town of Winhall Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Elizabeth Grant as Winhall's Town Clerk"),
            S(WINHALL_REPORT, f"{WINHALL_REP_C}: Town Clerk "
              "Elizabeth Grant, term to 2028")],
           [holder("Elizabeth Grant", "elizabeth-grant")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Winhall Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists Debra Avison as Winhall's Town "
                  "Treasurer"),
            S(WINHALL_REPORT, f"{WINHALL_REP_C}: the elected "
              "officials table lists Town Treasurer Debra "
              "Avison, term to 2028; an undated town "
              "clerk-directory PDF naming Elizabeth Grant as "
              "treasurer is the disclosed outlier")],
           [holder("Debra Avison", "debra-avison")]),
    office("moderator", "Town Moderator",
           "Town of Winhall Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(WINHALL_RESULTS, f"{WINHALL_RET_C}: Scott H. Bushee "
              "re-elected Moderator in 2026 (99 votes)")],
           [holder("Scott Bushee", "scott-bushee")]),
    office("lister", "Lister",
           "Town of Winhall Listers", 3,
           [statute2646("towns elect a board of listers"),
            S(WINHALL_RESULTS, f"{WINHALL_RET_C}: Doug Poulter "
              "re-elected Lister in 2026 (99 votes)"),
            S(WINHALL_REPORT, f"{WINHALL_REP_C}: listers Doug "
              "Poulter, Alexander Bilka (to 2027), and Lucia "
              "Wing (to 2028)")],
           [holder("Doug Poulter", "doug-poulter"),
            holder("Alexander Bilka", "alexander-bilka"),
            holder("Lucia Wing", "lucia-wing")]),
    office("town-agent", "Town Agent",
           "Town of Winhall Town Agent", 1,
           [statute2646("towns elect a town agent"),
            S(WINHALL_RESULTS, f"{WINHALL_RET_C}: Alexander W. "
              "Bilka re-elected Town Agent in 2026 (103 votes)")],
           [holder("Alexander Bilka", "alexander-bilka")]),
    office("grand-juror", "Grand Juror",
           "Town of Winhall Grand Juror", 1,
           [statute2646("towns elect a grand juror"),
            S(WINHALL_RESULTS, f"{WINHALL_RET_C}: Alexander W. "
              "Bilka re-elected Grand Juror in 2026 (105 votes)")],
           [holder("Alexander Bilka", "alexander-bilka")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Winhall Collector of Delinquent Taxes", 1,
           [S(WINHALL_REPORT, f"{WINHALL_REP_C}: the appointed "
              "officials table lists Collector of Delinquent "
              "Taxes Debra Avison (printed term to June 30, "
              "2026; a renewal is unpublished, disclosed). The "
              "office is modeled appointed on the town's own "
              "table")],
           [holder("Debra Avison", "debra-avison",
                   how_seated="appointed")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Winhall Cemetery Commissioners", 1,
           [S(WINHALL_REPORT, f"{WINHALL_REP_C}: the appointed "
              "officials table lists Cemetery Commissioner "
              "Elizabeth Grant (printed term to June 30, 2026; a "
              "renewal is unpublished, disclosed). The town "
              "publishes a single appointed seat, so the post "
              "carries one seat")],
           [holder("Elizabeth Grant", "elizabeth-grant",
                   how_seated="appointed")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Winhall Justices of the Peace", 5,
           [jp_src("lists five Winhall justices of the peace: "
                   "Timothy Apps, Robin Apps, Christie Boswell, "
                   "Michael Cole, and Cliff DesMarais"),
            S(WINHALL_REPORT, f"{WINHALL_REP_C}: the town "
              "report's JP line prints the third justice "
              "'Christina Boswell'; the certified listing, the "
              "certified 2026 return, and the live Selectboard "
              "page all give Christie Boswell, which governs")],
           [holder("Timothy Apps", "timothy-apps"),
            holder("Robin Apps", "robin-apps"),
            holder("Christie Boswell", "christie-boswell"),
            holder("Michael Cole", "michael-cole"),
            holder("Cliff DesMarais", "cliff-desmarais")]),
], jp=jp_election("winhall-vt", "Town of Winhall", 5,
                  "certifies the November 5, 2024 election of five "
                  "justices of the peace for Winhall: Timothy "
                  "Apps, Robin Apps, Christie Boswell, Michael "
                  "Cole, and Cliff DesMarais"))

# ----------------------------------------------------------------
# City of Winooski (Chittenden County) -- charter ch. 19.
# Sources: the certified Official Return of Votes, March 3, 2026
# (certified by City Clerk Jenny Willingham; contest pages read
# from renders) and the live City Council page (winooskivt.gov).
WINOOSKI_ORV_C = ("City of Winooski, Official Return of Votes, "
                  "March 3, 2026 (certified by City Clerk Jenny "
                  "Willingham)")
SPECS["winooski"] = spec("winooski", "City of Winooski", [
    office("mayor", "Mayor",
           "City of Winooski Mayor", 1,
           [charter19("sec. 303 provides for a mayor serving a "
                      "three-year term; sec. 301 vests the "
                      "city's legislative body in the mayor and "
                      "four councilors"),
            S(WINOOSKI_ORV, f"{WINOOSKI_ORV_C}: Thomas Renner "
              "elected Mayor in 2026 (780 votes) to the one-year "
              "remainder of the unexpired mayoral term"),
            S(WINOOSKI_COUNCIL, "City of Winooski, City Council "
              "page (live): Mayor Thomas Renner, term expiring "
              "March 2, 2027")],
           [holder("Thomas Renner", "thomas-renner")]),
    office("city-councilor", "City Councilor",
           "City of Winooski City Council", 4,
           [charter19("sec. 301: the council consists of the "
                      "mayor and four councilors elected at large "
                      "for staggered two-year terms"),
            S(WINOOSKI_ORV, f"{WINOOSKI_ORV_C}: Elsie Goodrich "
              "(727 votes), Eli Ogilvie (651), and Al Turkos "
              "(722, one-year remainder of a two-year term) "
              "elected in 2026"),
            S(WINOOSKI_COUNCIL, "City of Winooski, City Council "
              "page (live): Bryn Oakleaf (Deputy Mayor, term to "
              "March 2, 2027), Elsie Goodrich, Eli Ogilvie, and "
              "Al Turkos")],
           [holder("Bryn Oakleaf", "bryn-oakleaf"),
            holder("Elsie Goodrich", "elsie-goodrich"),
            holder("Eli Ogilvie", "eli-ogilvie"),
            holder("Al Turkos", "al-turkos")]),
    office("city-clerk", "City Clerk",
           "City of Winooski City Clerk", 1,
           [charter19("sec. 506(b)-(c): city officers other than "
                      "the council are appointed by the city "
                      "manager; the city clerk is enumerated "
                      "among the appointive offices"),
            S(WINOOSKI_CLERK, "City of Winooski, City Clerk's "
              "Office page: Jenny Willingham is the City Clerk; "
              "she certified the March 3, 2026 return of votes "
              "in that office")],
           [holder("Jenny Willingham", "jenny-willingham",
                   how_seated="appointed")]),
    office("city-treasurer", "City Treasurer",
           "City of Winooski City Treasurer", 1,
           [charter19("sec. 506(a)-(b): the city has the "
                      "officers provided by law for towns, and "
                      "all officers other than the council are "
                      "appointed by the city manager; no treasurer "
                      "is enumerated in sec. 506(c), so the "
                      "appointment basis is the sec. 506(a)/(b) "
                      "reading, disclosed on issue #163"),
            treas_xlsx("lists Johnathan Fenney as Winooski's "
                       "City Treasurer (the Guide prints 'John "
                       "Fenney'; the June 2026 spreadsheet's "
                       "fuller form is minted)")],
           [holder("Johnathan Fenney", "johnathan-fenney",
                   how_seated="appointed")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "City of Winooski Justices of the Peace", 15,
           [jp_src("lists fifteen Winooski justices of the "
                   "peace: Daisy Berbeco, Stewart Ledbetter, "
                   "Katherine Decarreau, Susan O'Brien, Taylor "
                   "Small, Emily Bowers, Thomas Renner, Steven "
                   "Berbeco, Chloe Tomlinson, George Cross, "
                   "Michael O'Brien, Diana Gonzalez, Thea "
                   "Wurzburg, Bridget Ahrens, and Mary Hussmann")],
           [holder("Daisy Berbeco", "daisy-berbeco",
                   existing_person_id="ocd-person/a7fdd2dc-e7e7-5bbb-ab6e-6a7f05fdf575"),
            holder("Stewart Ledbetter", "stewart-ledbetter"),
            holder("Katherine Decarreau", "katherine-decarreau"),
            holder("Susan O'Brien", "susan-o-brien"),
            holder("Taylor Small", "taylor-small"),
            holder("Emily Bowers", "emily-bowers"),
            holder("Thomas Renner", "thomas-renner"),
            holder("Steven Berbeco", "steven-berbeco"),
            holder("Chloe Tomlinson", "chloe-tomlinson",
                   existing_person_id="ocd-person/6ef197ee-cdde-5fb4-92fb-00b3acd767c0"),
            holder("George Cross", "george-cross"),
            holder("Michael O'Brien", "michael-o-brien"),
            holder("Diana Gonzalez", "diana-gonzalez"),
            holder("Thea Wurzburg", "thea-wurzburg"),
            holder("Bridget Ahrens", "bridget-ahrens"),
            holder("Mary Hussmann", "mary-hussmann")]),
], jp=jp_election("winooski-vt", "City of Winooski", 15,
                  "certifies the November 5, 2024 election of "
                  "fifteen justices of the peace for Winooski: "
                  "Daisy Berbeco, Stewart Ledbetter, Katherine "
                  "Decarreau, Susan O'Brien, Taylor Small, Emily "
                  "Bowers, Thomas Renner, Steven Berbeco, Chloe "
                  "Tomlinson, George Cross, Michael O'Brien, "
                  "Diana Gonzalez, Thea Wurzburg, Bridget Ahrens, "
                  "and Mary Hussmann. Berbeco and Tomlinson are "
                  "Winooski's Chittenden-21 state representatives; "
                  "their existing state-tier records are reused "
                  "and the JP candidacies are appended to them"))

# ----------------------------------------------------------------
# Town of Wolcott (Lamoille County) -- general law. Sources:
# the FY2025 Town Report officers table (published February
# 2026, pre-election expiries) and the live Selectboard page
# (wolcottvt.org).
WOLCOTT_REP_C = ("Town of Wolcott, FY2025 Town Report, officers "
                 "table (published February 2026)")
SPECS["wolcott"] = spec("wolcott", "Town of Wolcott", [
    office("selectboard", "Selectboard Member",
           "Town of Wolcott Selectboard", 5,
           [statute2646("towns elect a selectboard"),
            sb_dir("refers readers to the town's own roster for "
                   "Wolcott"),
            S(WOLCOTT_SB, "Town of Wolcott, Selectboard page "
              "(live, October 2026): Linda J. Martin (Chair), "
              "Michael Paradee (Vice Chair), Kurt Billings, "
              "Allen Carpenter, and Dolan Patrick"),
            S(WOLCOTT_REPORT, f"{WOLCOTT_REP_C}: Martin (Chair), "
              "Paradee (Vice Chair), Billings (to 2027), and "
              "Carpenter (to 2028) elected; the fifth seat was "
              "Richard Lee's (to 2027). Lee has departed and "
              "Dolan Patrick sits with no election record, so "
              "Patrick is minted as a vacancy appointee on this "
              "hybrid post (flagged). Martin's and Paradee's "
              "printed terms expired in 2026; both still chair "
              "the live board, so they are carried on "
              "incumbent-continuity (disclosed)")],
           [holder("Linda J. Martin", "linda-j-martin"),
            holder("Michael Paradee", "michael-paradee"),
            holder("Kurt Billings", "kurt-billings"),
            holder("Allen Carpenter", "allen-carpenter"),
            holder("Dolan Patrick", "dolan-patrick",
                   how_seated="appointed")]),
    office("town-clerk", "Town Clerk",
           "Town of Wolcott Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Belinda Harris Clegg as Wolcott's Town "
                  "Clerk"),
            S(WOLCOTT_REPORT, f"{WOLCOTT_REP_C}: Town Clerk "
              "Belinda Harris Clegg, term to 2028")],
           [holder("Belinda Harris Clegg", "belinda-harris-clegg")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Wolcott Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists Belinda Harris Clegg as Wolcott's Town "
                  "Treasurer"),
            S(WOLCOTT_REPORT, f"{WOLCOTT_REP_C}: Town Treasurer "
              "Belinda Harris Clegg, term to 2028")],
           [holder("Belinda Harris Clegg", "belinda-harris-clegg")]),
    office("moderator", "Town Moderator",
           "Town of Wolcott Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                   "one-year term"),
            S(WOLCOTT_REPORT, f"{WOLCOTT_REP_C}: Moderator Joe "
              "Hester-Ingram, one-year term expiring 2026. The "
              "March 2026 outcome is unpublished, so no holder "
              "is minted; Hester-Ingram is carried as a "
              "straggler on issue #163")]),
    office("lister", "Lister",
           "Town of Wolcott Listers", 3,
           [statute2646("towns elect a board of listers"),
            S(WOLCOTT_REPORT, f"{WOLCOTT_REP_C}: listers Thomas "
              "Martin (to 2028), Tracey LaPorte (to 2027), and "
              "W. Samuel Hill (expiring 2026). Hill's seat stood "
              "in 2026 with the outcome unpublished, so it is "
              "left unfilled and Hill is carried as a straggler "
              "on issue #163")],
           [holder("Thomas Martin", "thomas-martin"),
            holder("Tracey LaPorte", "tracey-laporte")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Wolcott Cemetery Commissioners", 5,
           [S(WOLCOTT_REPORT, f"{WOLCOTT_REP_C}: Cemetery "
              "Commissioners Crista Lowell (Chair, to 2028), "
              "Bradley Horstman (to 2027), and John Michael "
              "Green (to 2029); Lucien Gravel's seat expired in "
              "2026 with the outcome unpublished and the fifth "
              "seat printed vacant, so both are left unfilled "
              "and Gravel is carried as a straggler on issue "
              "#163")],
           [holder("Crista Lowell", "crista-lowell"),
            holder("Bradley Horstman", "bradley-horstman"),
            holder("John Michael Green", "john-michael-green")]),
    office("library-trustee", "Library Trustee",
           "Town of Wolcott Library Trustees", 5,
           [S(WOLCOTT_REPORT, f"{WOLCOTT_REP_C}: the report's own "
              "layout splits the Wolcott Public Library board "
              "into appointed trustees -- Charmone Lloyd (to "
              "2030) and Jennifer Ward (to 2029), with a third "
              "appointed seat printed vacant -- and elected "
              "trustees Johanna Duff and Anne LeRiche, whose "
              "terms expired in 2026 with the outcomes "
              "unpublished. The two appointed trustees are "
              "minted on this hybrid post; the elected seats "
              "are left unfilled and Duff and LeRiche are "
              "carried as stragglers on issue #163")],
           [holder("Charmone Lloyd", "charmone-lloyd",
                   how_seated="appointed"),
            holder("Jennifer Ward", "jennifer-ward",
                   how_seated="appointed")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Wolcott Justices of the Peace", 7,
           [jp_src("lists seven Wolcott justices of the peace: "
                   "Katie Black, Stacey Boivin, Sarena Moodie "
                   "Boland, Amy Kolb Noyes, Linda Reeve, Kimberly "
                   "Gravel, and Lucien Gravel"),
            S(WOLCOTT_REPORT, f"{WOLCOTT_REP_C}: the report's "
              "justices line names six of the seven, omitting "
              "Amy Kolb Noyes; the certified listing governs")],
           [holder("Katie Black", "katie-black"),
            holder("Stacey Boivin", "stacey-boivin"),
            holder("Sarena Moodie Boland", "sarena-moodie-boland"),
            holder("Amy Kolb Noyes", "amy-kolb-noyes"),
            holder("Linda Reeve", "linda-reeve"),
            holder("Kimberly Gravel", "kimberly-gravel"),
            holder("Lucien Gravel", "lucien-gravel")]),
], jp=jp_election("wolcott-vt", "Town of Wolcott", 7,
                  "certifies the November 5, 2024 election of "
                  "seven justices of the peace for Wolcott: Katie "
                  "Black, Stacey Boivin, Sarena Moodie Boland, "
                  "Amy Kolb Noyes, Linda Reeve, Kimberly Gravel, "
                  "and Lucien Gravel"))

# ----------------------------------------------------------------
# Town of Woodbury (Washington County) -- general law. Source of
# record: the town's live Directory page (woodburyvt.org), which
# prints the full officers table with term years and the town's
# own Elected/Appointed labels, corroborated by the live board
# pages.
WOODBURY_DIR_C = "Town of Woodbury, Directory page (live)"
SPECS["woodbury"] = spec("woodbury", "Town of Woodbury", [
    office("selectboard", "Selectboard Member",
           "Town of Woodbury Selectboard", 3,
           [statute2646("towns elect a selectboard"),
            sb_dir("names Chris Casey (Chair), Diana Peduzzi, "
                   "and John Gordon for Woodbury"),
            S(WOODBURY_DIR, f"{WOODBURY_DIR_C}: Selectboard -- "
              "Chris Casey (Chair, to 2027), Diana Peduzzi (to "
              "2028), and John Gordon (to 2029), labeled Elected"),
            S(WOODBURY_SB, "Town of Woodbury, Selectboard page "
              "(live): the same three members")],
           [holder("Chris Casey", "chris-casey"),
            holder("Diana Peduzzi", "diana-peduzzi"),
            holder("John Gordon", "john-gordon")]),
    office("town-clerk", "Town Clerk",
           "Town of Woodbury Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            clerk_xlsx("lists Graham Christie as Woodbury's "
                       "Town Clerk (the January 2026 Guide's 'R "
                       "Durkee' is stale against the June 2026 "
                       "spreadsheet and the town's live page)"),
            S(WOODBURY_DIR, f"{WOODBURY_DIR_C}: Town Clerk "
              "Graham Christie, term to 2027, labeled Elected"),
            S(WOODBURY_CLERK, "Town of Woodbury, Town Clerk page "
              "(live): Graham Christie")],
           [holder("Graham Christie", "graham-christie")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Woodbury Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            treas_xlsx("lists Lillian Baron as Woodbury's Town "
                       "Treasurer"),
            S(WOODBURY_DIR, f"{WOODBURY_DIR_C}: Town Treasurer "
              "'Lilly Baron', term to 2029, labeled Elected; the "
              "Secretary of State's full form Lillian Baron is "
              "minted, disclosed on issue #163")],
           [holder("Lillian Baron", "lillian-baron")]),
    office("moderator", "Town Moderator",
           "Town of Woodbury Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(WOODBURY_DIR, f"{WOODBURY_DIR_C}: Moderator "
              "Stephen Murphy, term to 2027, labeled Elected")],
           [holder("Stephen Murphy", "stephen-murphy")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Woodbury Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes"),
            S(WOODBURY_DIR, f"{WOODBURY_DIR_C}: Collector of "
              "Delinquent Taxes Ron Wells, term to 2027, "
              "labeled Elected")],
           [holder("Ron Wells", "ron-wells")]),
    office("auditor", "Auditor",
           "Town of Woodbury Auditors", 3,
           [statute2646("towns elect a board of auditors"),
            S(WOODBURY_DIR, f"{WOODBURY_DIR_C}: Auditors Jonah "
              "Meacham (to 2027), John Reid (Chair, to 2028), "
              "and Susan Martin (to 2029), labeled Elected")],
           [holder("Jonah Meacham", "jonah-meacham"),
            holder("John Reid", "john-reid"),
            holder("Susan Martin", "susan-martin")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Woodbury Cemetery Commissioners", 5,
           [S(WOODBURY_DIR, f"{WOODBURY_DIR_C}: Cemetery "
              "Commissioners Amy Hunt (to 2027), Cacky Peltz "
              "(to 2028), Stephanie Appleton (to 2029), Patti "
              "Garbeck (Vice Chair, to 2030), and Susan Stitely "
              "(Chair, to 2031), labeled Elected -- five-year "
              "staggered terms")],
           [holder("Amy Hunt", "amy-hunt"),
            holder("Cacky Peltz", "cacky-peltz"),
            holder("Stephanie Appleton", "stephanie-appleton"),
            holder("Patti Garbeck", "patti-garbeck"),
            holder("Susan Stitely", "susan-stitely")]),
    office("library-trustee", "Library Trustee",
           "Town of Woodbury Library Trustees", 5,
           [S(WOODBURY_DIR, f"{WOODBURY_DIR_C}: Library "
              "Trustees Deanna Slayton Avery (Chair, to 2027), "
              "Elisha Renne (to 2027), David Barber (to 2028), "
              "Tepin Delaney (to 2028), and Allison Schmitt "
              "(to 2028), labeled Elected")],
           [holder("Deanna Slayton Avery", "deanna-slayton-avery"),
            holder("Elisha Renne", "elisha-renne"),
            holder("David Barber", "david-barber"),
            holder("Tepin Delaney", "tepin-delaney"),
            holder("Allison Schmitt", "allison-schmitt")]),
    office("lister", "Lister",
           "Town of Woodbury Listers", 3,
           [statute2646("towns elect a board of listers"),
            S(WOODBURY_DIR, f"{WOODBURY_DIR_C}: Listers Bonnie "
              "Collins (to 2027), Sara Hedrick (to 2028), and "
              "Ron Wells (Chair, to 2029), labeled Elected")],
           [holder("Bonnie Collins", "bonnie-collins"),
            holder("Sara Hedrick", "sara-hedrick"),
            holder("Ron Wells", "ron-wells")]),
    office("first-constable", "First Constable",
           "Town of Woodbury First Constable", 1,
           [S(WOODBURY_DIR, f"{WOODBURY_DIR_C}: First Constable "
              "Andrew Delaney, labeled Appointed by the town")],
           [holder("Andrew Delaney", "andrew-delaney",
                   how_seated="appointed")]),
    office("road-commissioner", "Road Commissioner",
           "Town of Woodbury Road Commissioner", 1,
           [S(WOODBURY_DIR, f"{WOODBURY_DIR_C}: Road "
              "Commissioner Peter Dailey, labeled Appointed by "
              "the town. The office is published in the town's "
              "officers table; 17 V.S.A. sec. 2646 does not "
              "create it and no election evidence exists")],
           [holder("Peter Dailey", "peter-dailey",
                   how_seated="appointed")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Woodbury Justices of the Peace", 5,
           [jp_src("lists five Woodbury justices of the peace: "
                   "Patrick Flood, Merry Gangemi, Jayne "
                   "Nold-Laurendeau, Monty Shatney, and Susan G "
                   "Stitely"),
            S(WOODBURY_DIR, f"{WOODBURY_DIR_C}: the directory's "
              "justices of the peace match the certified slate "
              "name-for-name")],
           [holder("Patrick Flood", "patrick-flood"),
            holder("Merry Gangemi", "merry-gangemi"),
            holder("Jayne Nold-Laurendeau",
                   "jayne-nold-laurendeau"),
            holder("Monty Shatney", "monty-shatney"),
            holder("Susan Stitely", "susan-stitely",
                   ballot_name="Susan G Stitely")]),
], jp=jp_election("woodbury-vt", "Town of Woodbury", 5,
                  "certifies the November 5, 2024 election of "
                  "five justices of the peace for Woodbury: "
                  "Patrick Flood, Merry Gangemi, Jayne "
                  "Nold-Laurendeau, Monty Shatney, and Susan G "
                  "Stitely"))

# ----------------------------------------------------------------
# Town of Woodford (Bennington County) -- charter ch. 175.
# Source of record: the 2024 Annual Report office-holders table
# (p. 4, read from the page render; the PDF text layer
# column-jumbles the two-column table), corroborated by the SOS
# directory, Guide, and June 2026 spreadsheets.
WOODFORD_REP_C = ("Town of Woodford, 2024 Annual Report, "
                  "office-holders table (p. 4)")
SPECS["woodford"] = spec("woodford", "Town of Woodford", [
    office("selectboard", "Selectboard Member",
           "Town of Woodford Selectboard", 3,
           [charter175("sec. 8(a) elects a three-member "
                       "selectboard for staggered three-year "
                       "terms"),
            sb_dir("names Ryan Thurber, Wayne Tifft, and Steven "
                   "Wright for Woodford"),
            S(WOODFORD_REPORT, f"{WOODFORD_REP_C}: Selectboard "
              "Ryan Thurber (to 2027), Wayne Tifft (to 2026), "
              "and Steven Wright (to 2025). The June 2026 "
              "Secretary of State directory still seats all "
              "three, so Wright is carried on "
              "incumbent-continuity (disclosed)")],
           [holder("Ryan Thurber", "ryan-thurber"),
            holder("Wayne Tifft", "wayne-tifft"),
            holder("Steven Wright", "steven-wright")]),
    office("town-clerk", "Town Clerk",
           "Town of Woodford Town Clerk", 1,
           [charter175("sec. 8(a) elects a town clerk for a "
                       "three-year term"),
            guide("lists Susan Wright as Woodford's Town Clerk"),
            clerk_xlsx("lists Susan Wright as Woodford's Town "
                       "Clerk (June 2026)"),
            S(WOODFORD_REPORT, f"{WOODFORD_REP_C}: Town Clerk "
              "Susan Wright (printed term to 2025); the January "
              "2026 Guide and the June 2026 spreadsheet still "
              "name her, so she is carried on "
              "incumbent-continuity (disclosed)")],
           [holder("Susan Wright", "susan-wright")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Woodford Town Treasurer", 1,
           [charter175("sec. 8(a) elects a town treasurer for a "
                       "three-year term; the treasurer is ex "
                       "officio collector of current taxes"),
            guide("lists Gail Rutkowski as Woodford's Town "
                  "Treasurer"),
            treas_xlsx("lists Gail Rutkowski as Woodford's Town "
                       "Treasurer (June 2026)"),
            S(WOODFORD_REPORT, f"{WOODFORD_REP_C}: Town "
              "Treasurer Gail Rutkowski (printed term to 2025); "
              "the January 2026 Guide and the June 2026 "
              "spreadsheet still name her, so she is carried on "
              "incumbent-continuity (disclosed)")],
           [holder("Gail Rutkowski", "gail-rutkowski")]),
    office("moderator", "Town Moderator",
           "Town of Woodford Town Moderator", 1,
           [charter175("sec. 8(a) elects a moderator from the "
                       "floor for a one-year term"),
            S(WOODFORD_REPORT, f"{WOODFORD_REP_C}: Moderator "
              "Richard Frantz (printed term to 2025). No later "
              "outcome is published, so no holder is minted; "
              "Frantz is carried as a straggler on issue #163")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Woodford Collector of Delinquent Taxes", 1,
           [charter175("sec. 8(a) elects a collector of "
                       "delinquent taxes for a three-year term"),
            S(WOODFORD_REPORT, f"{WOODFORD_REP_C}: Collector of "
              "Delinquent Taxes James Kinney (printed term to "
              "2026). No current roster names the holder, so no "
              "holder is minted; Kinney is carried as a "
              "straggler on issue #163")]),
    office("auditor", "Auditor",
           "Town of Woodford Auditors", 3,
           [charter175("sec. 8(a) elects three auditors for "
                       "staggered three-year terms"),
            S(WOODFORD_REPORT, f"{WOODFORD_REP_C}: the report "
              "names only Auditor Virginia Ulitsch (printed "
              "term to 2025) and prints the other two seats "
              "vacant. No later outcome is published, so no "
              "holder is minted; Ulitsch is carried as a "
              "straggler on issue #163")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Woodford Cemetery Commissioners", 3,
           [charter175("sec. 11(a)(8): cemetery commissioners "
                       "are appointed"),
            S(WOODFORD_REPORT, f"{WOODFORD_REP_C}: the appointed "
              "officials table lists Cemetery Commissioners "
              "Maureen O'Neil, Linda Dovitski, and Virginia "
              "Ulitsch on indefinite terms (2024 vintage, "
              "disclosed)")],
           [holder("Maureen O'Neil", "maureen-o-neil",
                   how_seated="appointed"),
            holder("Linda Dovitski", "linda-dovitski",
                   how_seated="appointed"),
            holder("Virginia Ulitsch", "virginia-ulitsch",
                   how_seated="appointed")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Woodford Justices of the Peace", 4,
           [jp_src("lists four Woodford justices of the peace: "
                   "Virginia Ulitsch, Nancy Coleman, Maureen "
                   "O'Neil, and Geraldine Leahy"),
            S(WOODFORD_REPORT, f"{WOODFORD_REP_C}: the report's "
              "justices line concurs with the certified slate")],
           [holder("Virginia Ulitsch", "virginia-ulitsch"),
            holder("Nancy Coleman", "nancy-coleman"),
            holder("Maureen O'Neil", "maureen-o-neil"),
            holder("Geraldine Leahy", "geraldine-leahy")]),
], jp=jp_election("woodford-vt", "Town of Woodford", 4,
                  "certifies the November 5, 2024 election of "
                  "four justices of the peace for Woodford: "
                  "Virginia Ulitsch, Nancy Coleman, Maureen "
                  "O'Neil, and Geraldine Leahy. NOTE: Woodford's "
                  "listers were eliminated by voter approval on "
                  "March 1, 2022 and replaced by an outside "
                  "assessing firm (2024 Annual Report), so no "
                  "lister post is created even though ch. 175 "
                  "sec. 8(a) still prints the office -- flagged "
                  "on issue #163"))

# ----------------------------------------------------------------
# Town of Woodstock (Windsor County) -- general law. Sources:
# the live Selectboard and Town Clerk pages (townofwoodstock.org)
# and the 2026 Annual Town Report (its Elected Officials table
# is the post-March-2025 roster; its warning fixes the March 3,
# 2026 ballot).
WSTOCK_REP_C = ("Town of Woodstock, 2026 Annual Town Report, "
                "Elected Officials table and 2026 warning "
                "(Article 9)")
SPECS["woodstock-85975"] = spec("woodstock-85975",
                                "Town of Woodstock", [
    office("selectboard", "Selectboard Member",
           "Town of Woodstock Selectboard", 5,
           [statute2646("towns elect a selectboard"),
            S(WSTOCK_SB, "Town of Woodstock, Town Selectboard "
              "page (live): Norm Frates Jr. (Chair, to 2029), "
              "MaryAnn Sweeney (Vice Chair, to 2028), Susan "
              "Chiefsky (to 2027), Ben Ford (to 2027), and Clay "
              "Reed (to 2027)"),
            S(WSTOCK_REPORT, f"{WSTOCK_REP_C}: the report's "
              "post-March-2025 roster (Bourgeois, Susan Ford, "
              "Cole, Cliff Johnson, Powell) has entirely turned "
              "over; the exit mechanisms are unpublished. The "
              "town's live page governs; the factory's four-name "
              "set and the Secretary of State directory's lone "
              "'Susan Ford' are stale (disclosed)")],
           [holder("Norm Frates Jr.", "norm-frates-jr"),
            holder("MaryAnn Sweeney", "maryann-sweeney"),
            holder("Susan Chiefsky", "susan-chiefsky"),
            holder("Ben Ford", "ben-ford"),
            holder("Clay Reed", "clay-reed")]),
    office("town-clerk", "Town Clerk",
           "Town of Woodstock Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists F. Charles Degener III as Woodstock's "
                  "Town Clerk"),
            S(WSTOCK_CLERK, "Town of Woodstock, Town Clerk page "
              "(live): 'F. Charles Degener, III -- Town Clerk "
              "(current)'"),
            S(WSTOCK_REPORT, f"{WSTOCK_REP_C}: Town Clerk F. "
              "Charles Degener (printed term to 2026); the 2026 "
              "warning carried a three-year clerk term and the "
              "live page still names him, so he is carried on "
              "incumbent-continuity (disclosed)")],
           [holder("F. Charles Degener III",
                   "f-charles-degener-iii")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Woodstock Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists F. Charles Degener III as Woodstock's "
                  "Town Treasurer"),
            S(WSTOCK_REPORT, f"{WSTOCK_REP_C}: Town Treasurer "
              "F. Charles Degener (printed term to 2026); the "
              "2026 warning carried a three-year treasurer term "
              "and the Secretary of State sources still name "
              "him, so he is carried on incumbent-continuity "
              "(disclosed)")],
           [holder("F. Charles Degener III",
                   "f-charles-degener-iii")]),
    office("moderator", "Town Moderator",
           "Town of Woodstock Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                   "one-year term"),
            S(WSTOCK_REPORT, f"{WSTOCK_REP_C}: Moderator "
              "Matthew Maxham (printed term to 2026); the 2026 "
              "warning carried the moderator election but the "
              "outcome is unpublished, so no holder is minted; "
              "Maxham is carried as a straggler on issue #163")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Woodstock Cemetery Commissioners", 3,
           [S(WSTOCK_REPORT, f"{WSTOCK_REP_C}: Cemetery "
              "Commissioners Gregory Camp (to 2027) and two "
              "seats printed VACANT (expiring 2026 and 2028); "
              "the 2026 warning carried three-year and two-year "
              "cemetery seats with the outcomes unpublished, so "
              "only Camp is minted")],
           [holder("Gregory Camp", "gregory-camp")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Woodstock Trustees of Public Funds", 3,
           [statute2646("towns elect trustees of public funds"),
            S(WSTOCK_REPORT, f"{WSTOCK_REP_C}: Trustees of "
              "Public Funds Jill M. Davies (to 2027), Lauren "
              "Thompson (to 2026), and Michael Green (to 2028); "
              "the 2026 warning carried three-year and one-year "
              "trustee seats with the outcomes unpublished, so "
              "Thompson's seat is left unfilled and she is "
              "carried as a straggler on issue #163")],
           [holder("Jill Davies", "jill-davies"),
            holder("Michael Green", "michael-green")]),
    office("grand-juror", "Grand Juror",
           "Town of Woodstock Grand Juror", 1,
           [statute2646_structure("towns elect a grand juror"),
            S(WSTOCK_REPORT, f"{WSTOCK_REP_C}: the grand juror "
              "line printed VACANT (expiring 2026); the 2026 "
              "warning carried the election and the outcome is "
              "unpublished")]),
    office("first-constable", "First Constable",
           "Town of Woodstock First Constable", 1,
           [statute2646_structure("towns elect a first "
                                   "constable"),
            S(WSTOCK_REPORT, f"{WSTOCK_REP_C}: First Constable "
              "Kelly Linton (printed term to 2026); the 2026 "
              "warning carried the election but the outcome is "
              "unpublished, so no holder is minted; Linton is "
              "carried as a straggler on issue #163")]),
    office("town-agent", "Town Agent",
           "Town of Woodstock Town Agent", 1,
           [statute2646_structure("towns elect a town agent"),
            S(WSTOCK_REPORT, f"{WSTOCK_REP_C}: the town agent "
              "line printed VACANT (expiring 2026); the 2026 "
              "warning carried the election and the outcome is "
              "unpublished")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Woodstock Collector of Delinquent Taxes", 1,
           [S(WSTOCK_REPORT, f"{WSTOCK_REP_C}: the report's "
              "Annually Appointed Officials list names "
              "Delinquent Tax Collector Eric Duffy (2026 "
              "vintage, disclosed)")],
           [holder("Eric Duffy", "eric-duffy",
                   how_seated="appointed")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Woodstock Justices of the Peace", 10,
           [jp_src("lists ten Woodstock justices of the peace: "
                   "Fred Barr, Susan Chiefsky, Rick Fiske, David "
                   "Green, Matt Maxham, Jan Noskey, Michael "
                   "Ricci, Mary Riley, Bill Boardman, and Jill "
                   "Davies (Davies's entry continues across the "
                   "listing's pp. 42-43 page break)"),
            S(WSTOCK_REPORT, f"{WSTOCK_REP_C}: the report's "
              "justices table names twelve, adding Jane Soule, "
              "Catie Baumgartner, and BJ Dunn and omitting "
              "certified winners Jan Noskey and Michael Ricci; "
              "the certified slate governs and the table is "
              "disclosed on issue #163")],
           [holder("Fred Barr", "fred-barr"),
            holder("Susan Chiefsky", "susan-chiefsky"),
            holder("Rick Fiske", "rick-fiske"),
            holder("David Green", "david-green"),
            holder("Matthew Maxham", "matthew-maxham",
                   ballot_name="Matt Maxham"),
            holder("Jan Noskey", "jan-noskey"),
            holder("Michael Ricci", "michael-ricci"),
            holder("Mary Riley", "mary-riley"),
            holder("William Boardman", "william-boardman",
                   ballot_name="Bill Boardman"),
            holder("Jill Davies", "jill-davies")]),
], jp=jp_election("woodstock-85975-vt", "Town of Woodstock", 10,
                  "certifies the November 5, 2024 election of ten "
                  "justices of the peace for Woodstock: Fred "
                  "Barr, Susan Chiefsky, Rick Fiske, David Green, "
                  "Matt Maxham, Jan Noskey, Michael Ricci, Mary "
                  "Riley, Bill Boardman, and Jill Davies. NOTE: "
                  "the town's auditors were eliminated by the "
                  "March 1, 2025 vote (Article 14), so no "
                  "auditor post is created"))

# ----------------------------------------------------------------
# Village of Woodstock (Windsor County) -- charter ch. 291.
# Sources: the live Village Trustees page (townofwoodstock.org)
# and the Village Report 2025 (officers as of early 2025).
SPECS["woodstock"] = spec("woodstock", "Village of Woodstock", [
    office("village-trustee", "Village Trustee",
           "Village of Woodstock Board of Trustees", 5,
           [charter291("sec. 3: the annual meeting elects five "
                       "trustees"),
            S(WSV_TRUSTEES, "Village of Woodstock, Village "
              "Trustees page (live): Lisa Lawlor (Chair, to "
              "2027), Jeffrey Kahn (Vice Chair, to 2027), "
              "Brenda Blakeman (to 2028), Wendy Marinan (to "
              "2027), and Jamie Fox (to 2028). The page prints "
              "the fourth trustee 'Werndy Marrinan'; the "
              "Village Report prints 'Wendy Wright Marinan', "
              "whose form is minted (disclosed)")],
           [holder("Lisa Lawlor", "lisa-lawlor"),
            holder("Jeffrey Kahn", "jeffrey-kahn"),
            holder("Brenda Blakeman", "brenda-blakeman"),
            holder("Wendy Marinan", "wendy-marinan"),
            holder("Jamie Fox", "jamie-fox")]),
    office("village-clerk", "Village Clerk",
           "Village of Woodstock Village Clerk", 1,
           [charter291("sec. 3: the annual meeting elects a "
                       "clerk"),
            S(WSV_REPORT, "Village of Woodstock, Village Report "
              "2025, Village Board and Officers -- Elected "
              "Officials: Village Clerk Donald R. Wheeler "
              "(term to 2025). No later outcome is published, "
              "so no holder is minted; Wheeler is carried as a "
              "straggler on issue #163")]),
    office("village-treasurer", "Village Treasurer",
           "Village of Woodstock Village Treasurer", 1,
           [charter291("sec. 3: the annual meeting elects a "
                       "treasurer"),
            S(WSV_REPORT, "Village of Woodstock, Village Report "
              "2025, Village Board and Officers -- Elected "
              "Officials: Village Treasurer F. Charles Degener "
              "(term to 2025). No later outcome is published, "
              "so no holder is minted; the seat is carried as a "
              "straggler on issue #163")]),
    office("collector-of-taxes", "Collector of Taxes",
           "Village of Woodstock Collector of Taxes", 1,
           [charter291("sec. 3: the annual meeting elects a "
                       "collector of taxes; no holder is "
                       "published in any source read, so the post "
                       "is created without a membership")]),
    office("moderator", "Village Moderator",
           "Village of Woodstock Moderator", 1,
           [charter291("sec. 4 permits the election of other "
                       "officers as the public interest requires; "
                       "the village's own officers list elects a "
                       "moderator"),
            S(WSV_REPORT, "Village of Woodstock, Village Report "
              "2025, Village Board and Officers -- Elected "
              "Officials: Moderator Greg Camp (term to 2025). "
              "No later outcome is published, so no holder is "
              "minted; Camp is carried as a straggler on issue "
              "#163")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Village of Woodstock Trustees of Public Funds", 1,
           [charter291("sec. 4 permits the election of other "
                       "officers as the public interest requires; "
                       "the village's own officers list elects a "
                       "trustee of public funds"),
            S(WSV_REPORT, "Village of Woodstock, Village Report "
              "2025, Village Board and Officers -- Elected "
              "Officials: Trustee of Public Funds Jill Davies "
              "(term to 2025). No later outcome is published, "
              "so no holder is minted; the seat is carried as a "
              "straggler on issue #163")]),
])

# ----------------------------------------------------------------
# Town of Worcester (Washington County) -- general law.
# Sources: the official minutes of the March 3, 2026 annual town
# meeting (signed by the Moderator and the Town Clerk) and the
# town's live Directory page (worcestervt.org).
WORC_MIN_C = ("Town of Worcester, official minutes of the annual "
              "town meeting, March 3, 2026")
SPECS["worcester"] = spec("worcester", "Town of Worcester", [
    office("selectboard", "Selectboard Member",
           "Town of Worcester Selectboard", 3,
           [statute2646("towns elect a selectboard"),
            sb_dir("names John Kaeding (Chair), Carter Stowell, "
                   "and Jeffery Boudreau for Worcester"),
            S(WORC_DIR, "Town of Worcester, Directory page "
              "(live): Selectboard -- John Kaeding (Chair), "
              "Jeff Boudreau, and Carter Stowell. One three-year "
              "seat stood at the March 2026 meeting with the "
              "ballot outcome unpublished; all three are "
              "carried on incumbent-continuity (disclosed)")],
           [holder("John Kaeding", "john-kaeding"),
            holder("Jeffery Boudreau", "jeffery-boudreau"),
            holder("Carter Stowell", "carter-stowell")]),
    office("town-clerk", "Town Clerk",
           "Town of Worcester Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Jennifer LeStat as Worcester's Town "
                  "Clerk"),
            S(WORC_MINUTES, f"{WORC_MIN_C}: Town Clerk Jennifer "
              "LeStat declared the polls open for the Australian "
              "ballot items and signed the minutes as Town "
              "Clerk")],
           [holder("Jennifer LeStat", "jennifer-lestat")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Worcester Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(WORC_DIR, "Town of Worcester, Directory page "
              "(live): 'Town Treasurer/Tax Collector/Delinquent "
              "Taxes/Billing: Heather Pagel' at the treasurer's "
              "email address, and Delinquent Tax Collector "
              "Katie Miller listed separately. The Secretary of "
              "State's Guide (January 2026) and June 2026 "
              "spreadsheet name Katie Miller as treasurer, so a "
              "turnover occurred in 2026; its mechanism is "
              "unpublished, and Pagel is minted as an appointee "
              "(the vacancy-appointment reading) -- flagged on "
              "issue #163")],
           [holder("Heather Pagel", "heather-pagel",
                   how_seated="appointed")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Worcester Collector of Delinquent Taxes", 1,
           [S(WORC_DIR, "Town of Worcester, Directory page "
              "(live): Delinquent Tax Collector Katie Miller. "
              "The office was not on the March 2026 meeting's "
              "ballot list and no election evidence is "
              "published, so the holder is modeled appointed")],
           [holder("Katie Miller", "katie-miller",
                   how_seated="appointed")]),
    office("moderator", "Town Moderator",
           "Town of Worcester Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(WORC_MINUTES, f"{WORC_MIN_C}: Article 1 -- Paul "
              "Hanlon was elected Moderator for the year ensuing "
              "and signed the minutes as Town Moderator")],
           [holder("Paul Hanlon", "paul-hanlon")]),
    office("constable", "Constable",
           "Town of Worcester Constable", 1,
           [statute2646("towns elect a constable"),
            S(WORC_MINUTES, f"{WORC_MIN_C}: Article 4 -- Shawn "
              "McManus was elected Town Constable for the year "
              "ensuing. The town Directory prints 'Shawn M. "
              "McManis'; the signed minutes, the election "
              "record, govern (disclosed)")],
           [holder("Shawn McManus", "shawn-mcmanus")]),
    office("lister", "Lister",
           "Town of Worcester Listers", 3,
           [statute2646("towns elect a board of listers"),
            S(WORC_DIR, "Town of Worcester, Directory page "
              "(live): Listers Peter Strobridge, Alan Erdossy, "
              "and Jonathan Scherbatskoy. Two lister seats "
              "stood at the March 2026 meeting (Article 2) with "
              "the ballot outcomes unpublished; the three are "
              "carried on the town's own current directory "
              "(disclosed). The minutes' motion credits print "
              "'John Sherbatskoy'; the directory's full form "
              "governs")],
           [holder("Peter Strobridge", "peter-strobridge"),
            holder("Alan Erdossy", "alan-erdossy"),
            holder("Jonathan Scherbatskoy",
                   "jonathan-scherbatskoy")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Worcester Cemetery Commissioners", 3,
           [S(STATUTE_5373, "18 V.S.A. section 5373 provides "
              "for a three-member board of cemetery "
              "commissioners on staggered terms"),
            S(WORC_MINUTES, f"{WORC_MIN_C}: Article 5 -- "
              "Heather Pagel was elected Cemetery Commissioner "
              "for a term of three years. The board's size (3) "
              "follows the statute's three-member pattern and "
              "the single-seat three-year election in the "
              "minutes -- a flagged derivation; the other two "
              "seats' holders are unpublished")],
           [holder("Heather Pagel", "heather-pagel")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Worcester Justices of the Peace", 5,
           [jp_src("lists five Worcester justices of the peace: "
                   "Paul Hanlon, Marcia Mimi Hill, Michele Hill, "
                   "Sara Baker, and Angelica Angie Romero"),
            S(WORC_DIR, "Town of Worcester, Directory page "
              "(live): the justices of the peace roster -- Paul "
              "Hanlon (Chair), Marcia 'Mimi' Hill, Michele "
              "Hill, Angie Romero, and Sara Baker -- matches "
              "the certified slate name-for-name")],
           [holder("Paul Hanlon", "paul-hanlon"),
            holder("Marcia Hill", "marcia-hill",
                   ballot_name="Marcia Mimi Hill"),
            holder("Michele Hill", "michele-hill"),
            holder("Sara Baker", "sara-baker"),
            holder("Angelica Romero", "angelica-romero",
                   ballot_name="Angelica Angie Romero")]),
], jp=jp_election("worcester-vt", "Town of Worcester", 5,
                  "certifies the November 5, 2024 election of "
                  "five justices of the peace for Worcester: Paul "
                  "Hanlon, Marcia Mimi Hill, Michele Hill, Sara "
                  "Baker, and Angelica Angie Romero"))

ORDER = ["windsor", "winhall", "winooski", "wolcott", "woodbury",
         "woodford", "woodstock-85975", "woodstock", "worcester"]

for slug in ORDER:
    (OUT / f"{slug}.json").write_text(
        json.dumps(SPECS[slug], indent=1) + "\n")
print("wrote", len(ORDER), "specs")
