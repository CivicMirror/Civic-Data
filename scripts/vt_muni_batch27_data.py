#!/usr/bin/env python3
"""Batch 27 of the VT #163 municipal fan-out (alphabetical positions
260-269): Westmore, Weston, Weybridge, Wheelock, Whiting, Whitingham,
Williamstown, Williston, Wilmington, Windham. Emits one JSON spec per
municipality for build_vt_municipality.py. Research:
vt_muni_batch27_research.md.

Identity calls baked into this batch (all flagged on #163):
- Westmore: John Zimmer holds Town Treasurer and Trustee of Public
  Funds on one record. The certified JP listing prints "Kathy L
  Homes"; both town sources print "Holmes" -- the person is Kathy
  Holmes with ballot_name "Kathy L Homes". Moderator Andrew Berley
  and DTC Annette Parenteau are stragglers (their seats stood in
  March 2026; the outcome is unpublished) -- posts only.
- Weston: the March 2026 meeting re-elected Denis Benson (SB) and
  then he departed; the Sept. 26, 2026 special meeting elected Duane
  Hart and Susan Morris to the remainders -- both minted ELECTED.
  Wayne Granquist holds Moderator and JP on one record; Kim Seymour
  holds Clerk and Treasurer; Richard Lechthaler holds a library
  seat and a cemetery seat; Duane Hart holds SB and cemetery.
  The report's stale JP table (Goodwin, Mason) is NOT minted.
- Weybridge: Brenda Jaring holds Town Clerk and Town Treasurer,
  both APPOINTED under ch. 167 sec. 103. The SB member is minted
  T. Charles Jordan (report form) over the directory's "T. Charlie".
  Town Agent Nancy Foster and Grand Juror Maura Huddleston are
  stragglers -- posts only.
- Wheelock: Erin Swigart holds Clerk and Treasurer. The certified
  JP slate is four; Sharon Fialco sits as a fifth JP with no
  election record -- APPOINTED on the hybrid post. Charlton Dill
  (the page's "Chuck") per the directory/factory full form.
- Whiting: Heather Bouchard holds Clerk and Treasurer (the town
  page states the treasurer is elected). The SOS SB directory's
  lone Quenneville row was a thin entry; the board is three.
- Whitingham: Dennis Pike sits on the SB as a vacancy APPOINTEE
  (James Weber signed the Jan. 2026 warning as Vice Chair; Pike
  sits by the May 7, 2026 minutes; no election seated him).
  Almira Aekus won the clerk term in 2025 and departed; Rachel
  Littlehale was elected in 2026 to the remainder. Treasurer and
  DTC both became appointed offices March 5, 2025 (FYE24 report
  footnote); Marylee Putnam holds both. Clerk Seth Boyd also
  holds Moderator and JP -- Seth Boyd is moderator + JP; the
  clerk is Rachel Littlehale. (Boyd: moderator and JP only.)
  Rosemary Tefft (JP) is not Lyman Tefft Jr. (SB).
- Williamstown: Jenn Allard holds Treasurer (appointed, ch. 169)
  and Collector of Taxes (appointed); Ryan Lockwood (Town
  Manager) holds DTC (appointed). Matt Walker is minted as a
  cemetery commissioner from the officers page although the
  cemetery department page names only three -- flagged. The
  Assessor is NOT modeled (no term, no charter basis -- read as
  an appointed staff assessor). Jasmin/Matt "Couillard" over the
  page's mixed "Coulliard" spellings.
- Williston: three cross-tier reuses -- Charity R. Clark (the
  Attorney General) holds a library trustee seat and a JP seat;
  Virginia "Ginny" Lyons (state senator) holds a JP seat; Angela
  Arsenault (Chittenden-2 House candidate) holds a JP seat; the
  operator appends their JP candidacies to the existing records.
  Moderator is POST ONLY: Christopher D. Roy was elected
  unanimously at the 2025 meeting and presided in 2026, but the
  office is filled from the floor and the 2026 outcome is
  unpublished -- straggler. Listers are NOT modeled: the office
  was eliminated by the March 3, 2026 Article 17 vote approved
  as Act M-12. Cemetery commissioners are appointed (ch. 171).
- Wilmington: Gordon Boyd moved from Second Constable (2025) to
  First Constable (certified 2026); the Second Constable post is
  created without a holder ("NONE REACHING 17 REQUIRED VOTES").
  Treasurer Christine Richter is APPOINTED (the report lists her
  as Finance Officer under Appointed Officials). The certified
  JP Joanne Fowler departed; Matthew Moore sits APPOINTED per
  the report's JP roster (post seats=7: six certified winners'
  seats, one filled by appointment, per the roster's own seven
  lines including a "Vacant" line). Library trustee Louis Clark
  (report, to 2029) yields to the live page's Tom Young --
  flagged; cemetery commissioner Jennifer Goodell (to 2030)
  yields to the live page's vacant line.
- Windham: Emily Shusdock (Clerk) and Cathy Fales (Treasurer)
  hold the offices per the live Town Directory; Bea Eliastam and
  Courtney Roth (Aug. 2025 officials form / SOS Guide) departed.
  Road Commissioner Kord Scott is modeled APPOINTED (the office
  is published in the town's officials form; no election evidence;
  17 V.S.A. sec. 2646 does not create it). JP Philip McDuffie is
  a departed winner (the live directory's JP roster names four)
  -- excluded entirely; the election note carries the story.
  Moderator is POST ONLY (no town source names a holder).
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
CHARTER_167 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/167",
    "note": "PLACEHOLDER",
}
CHARTER_169 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/169",
    "note": "PLACEHOLDER",
}
CHARTER_171 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/171",
    "note": "PLACEHOLDER",
}
ACT_M12 = {
    "url": "https://legislature.vermont.gov/Documents/2026/Docs/BILLS/H-0957/H-0957%20As%20Passed%20by%20Both%20House%20and%20Senate%20Unofficial.pdf",
    "note": "PLACEHOLDER",
}

WMORE_REPORT = {"url": "https://irp.cdn-website.com/2728571a/files/uploaded/Westmore_2025.F.pdf",
                "note": "PLACEHOLDER"}
WMORE_SB = {"url": "https://westmoreonline.org/selectboard", "note": "PLACEHOLDER"}
WMORE_LISTERS = {"url": "https://westmoreonline.org/listers", "note": "PLACEHOLDER"}
WMORE_CEMETERY = {"url": "https://westmoreonline.org/cemetery", "note": "PLACEHOLDER"}
WMORE_JP = {"url": "https://westmoreonline.org/justices-of-the-peace", "note": "PLACEHOLDER"}

WESTON_TM26 = {"url": "https://www.westonvt.org/s/2026-TM-Results.pdf",
               "note": "PLACEHOLDER"}
WESTON_SPEC26 = {"url": "https://www.westonvt.org/s/Sept-26-2026-Special-TM-Results.pdf",
                 "note": "PLACEHOLDER"}
WESTON_JP24 = {"url": "https://www.westonvt.org/s/Official-Results-11-5-2024.pdf",
               "note": "PLACEHOLDER"}
WESTON_SB = {"url": "https://www.westonvt.org/selectboard", "note": "PLACEHOLDER"}
WESTON_LISTERS = {"url": "https://www.westonvt.org/listers", "note": "PLACEHOLDER"}
WESTON_LIBRARY = {"url": "https://www.westonvt.org/library", "note": "PLACEHOLDER"}
WESTON_CEM = {"url": "https://www.westonvt.org/cemeteries", "note": "PLACEHOLDER"}
WESTON_TPF = {"url": "https://www.westonvt.org/trusteespublicfunds", "note": "PLACEHOLDER"}
WESTON_DTC = {"url": "https://www.westonvt.org/collectordelinquentaxes", "note": "PLACEHOLDER"}

WEY_REPORT = {"url": "https://weybridgevt.govoffice.com/vertical/Sites/%7B69F46EA2-C090-426C-A030-0C9E82EFF0C1%7D/uploads/Town_Report_2025.pdf",
              "note": "PLACEHOLDER"}
WEY_ELECTIONS = {"url": "https://www.townofweybridge.org/elections", "note": "PLACEHOLDER"}

WHEEL_CONTACTS = {"url": "https://townofwheelockvt.org/contacts", "note": "PLACEHOLDER"}

WHIT_DOCS = {"url": "https://www.whitingvt.com/documents", "note": "PLACEHOLDER"}
WHIT_LISTERS = {"url": "https://www.whitingvt.com/lister-board", "note": "PLACEHOLDER"}
WHIT_AUDITORS = {"url": "https://www.whitingvt.com/auditors", "note": "PLACEHOLDER"}
WHIT_CLERK = {"url": "https://www.whitingvt.com/town-clerk", "note": "PLACEHOLDER"}

WHAM_RES26 = {"url": "https://whitinghamvt.org/sites/default/files/Election%20Results%20of%2003.03.26.pdf",
              "note": "PLACEHOLDER"}
WHAM_RES25 = {"url": "https://whitinghamvt.org/sites/default/files/ELECTION%20NIGHT%20RESULTS.pdf",
              "note": "PLACEHOLDER"}
WHAM_WARN26 = {"url": "https://whitinghamvt.org/sites/default/files/Warning%20for%20Town%20Meeting%202026_0.pdf",
               "note": "PLACEHOLDER"}
WHAM_REPORT24 = {"url": "https://whitinghamvt.org/sites/default/files/Annual%20Town%20Report%20fye%2006.30.24.pdf",
                 "note": "PLACEHOLDER"}
WHAM_SB = {"url": "https://whitinghamvt.org/TownDepartments/whitingham-selectboard",
           "note": "PLACEHOLDER"}
WHAM_COLLECTOR = {"url": "https://whitinghamvt.org/TownDepartments/collector-taxes",
                  "note": "PLACEHOLDER"}
WHAM_CEMMIN = {"url": "https://whitinghamvt.org/sites/default/files/Cemetery%20Commission%20Minutes%2009.26.26.pdf",
               "note": "PLACEHOLDER"}

WTOWN_OFFICERS = {"url": "https://williamstownvt.org/town-officers/", "note": "PLACEHOLDER"}
WTOWN_CEMETERY = {"url": "https://williamstownvt.org/cemetery/", "note": "PLACEHOLDER"}

WILL_REPORT = {"url": "https://www.town.williston.vt.us/vertical/sites/%7BF506B13C-605B-4878-8062-87E5927E49F0%7D/uploads/Final_Town_Report_2025.pdf",
               "note": "PLACEHOLDER"}
WILL_JP = {"url": "https://www.town.williston.vt.us/index.asp?Type=B_DIR&SEC={5DAA0A2C-3A9C-454C-B8F5-3CB64AB1C4C3}",
           "note": "PLACEHOLDER"}
WILL_CEM = {"url": "https://www.town.williston.vt.us/index.asp?Type=B_DIR&SEC={3076BCA1-3425-474F-8F7E-1103631082A0}",
            "note": "PLACEHOLDER"}
WILL_LIBMIN = {"url": "https://damlvt.org/images/stories/boardmeet/06152026trusteeminutes.pdf",
               "note": "PLACEHOLDER"}
WILL_LIBBOARD = {"url": "https://www.town.williston.vt.us/index.asp?Type=B_BASIC&SEC={5A2BD214-6CE0-4384-A0FA-BDAF486DACE3}",
                 "note": "PLACEHOLDER"}

WILM_SB = {"url": "https://wilmingtonvermont.us/boards-committees/selectboard/",
           "note": "PLACEHOLDER"}
WILM_CEM = {"url": "https://wilmingtonvermont.us/boards-committees/cemetery-commission/",
            "note": "PLACEHOLDER"}
WILM_LIB = {"url": "https://wilmingtonvermont.us/boards-committees/library-trustees-pettee-memorial-library/",
            "note": "PLACEHOLDER"}
WILM_CERT = {"url": "https://wilmingtonvermont.us/wp-content/uploads/2026/03/TM-Cert-of-Votes-Wilmington-2026-1.pdf",
             "note": "PLACEHOLDER"}
WILM_REPORT = {"url": "https://wilmingtonvermont.us/wp-content/uploads/2026/02/Town-Report-Final.pdf",
               "note": "PLACEHOLDER"}
WILM_FINANCE = {"url": "https://wilmingtonvermont.us/departments/treasurerfinance-office/",
                "note": "PLACEHOLDER"}

WIND_DIR = {"url": "https://townofwindhamvt.org/town-directory/", "note": "PLACEHOLDER"}
WIND_OFFICIALS = {"url": "https://docs.google.com/document/d/1Hn2P1BtVJZt4R46Y89IMjhUREp0OSraT/edit",
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


def charter167(phrase):
    return S(CHARTER_167, f"24 App. V.S.A. ch. 167 (Town of "
             f"Weybridge): {phrase}")


def charter169(phrase):
    return S(CHARTER_169, f"24 App. V.S.A. ch. 169 (Town of "
             f"Williamstown): {phrase}")


def charter171(phrase):
    return S(CHARTER_171, f"24 App. V.S.A. ch. 171 (Town of "
             f"Williston): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 27); issue #163 "
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
                  f"# municipal fan-out batch 27; issue #163 "
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
# Town of Westmore (Orleans County) -- general law (17 V.S.A.
# sec. 2646). Sources: the town site (westmoreonline.org) and the
# 2025 Town Report's ELECTED OFFICIALS table (report dated
# Feb. 23, 2026), read firsthand.
WMORE_REP_C = ("Town of Westmore, 2025 Town Report (dated "
               "February 23, 2026), ELECTED OFFICIALS table")
SPECS["westmore"] = spec("westmore", "Town of Westmore", [
    office("selectboard", "Selectboard Member",
           "Town of Westmore Selectboard", 5,
           [sb_dir("names David Stevens (Chair), William Perkins "
                   "(Vice Chair), Miriam Simonds, Isaiah Casey, "
                   "and Jason Petrarca"),
            S(WMORE_SB, "Town of Westmore, Selectboard page: names "
              "the same five members with term expiries -- Stevens "
              "(2027), Casey (2027), Simonds (2028), Petrarca "
              "(2028), Perkins (2029)"),
            S(WMORE_REPORT, f"{WMORE_REP_C}: the pre-meeting table "
              "showed Peter Hyslop's seat expiring in 2026; the "
              "live board page seats Jason Petrarca in it")],
           [holder("David Stevens", "david-stevens"),
            holder("William Perkins", "william-perkins"),
            holder("Miriam Simonds", "miriam-simonds"),
            holder("Isaiah Casey", "isaiah-casey"),
            holder("Jason Petrarca", "jason-petrarca")]),
    office("town-clerk", "Town Clerk",
           "Town of Westmore Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Elaine Cashin as Westmore's Town Clerk"),
            S(WMORE_REPORT, f"{WMORE_REP_C}: Town Clerk Elaine "
              "Cashin, three-year term to 2028")],
           [holder("Elaine Cashin", "elaine-cashin")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Westmore Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists John Zimmer as Westmore's Town Treasurer"),
            S(WMORE_REPORT, f"{WMORE_REP_C}: Town Treasurer John "
              "Zimmer, three-year term to 2028")],
           [holder("John Zimmer", "john-zimmer")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Westmore Trustees of Public Funds", 1,
           [statute2646("towns elect trustees of public funds"),
            S(WMORE_REPORT, f"{WMORE_REP_C}: Trustee of Public "
              "Funds John Zimmer, term to 2028 -- the town elects "
              "a single trustee")],
           [holder("John Zimmer", "john-zimmer")]),
    office("lister", "Lister",
           "Town of Westmore Listers", 3,
           [statute2646("towns elect a board of listers"),
            S(WMORE_LISTERS, "Town of Westmore, Listers page: "
              "names Susan Blackstone, Maree Bushey, and Amanda "
              "Smith as the current listers"),
            S(WMORE_REPORT, f"{WMORE_REP_C}: listers Susan "
              "Blackstone (2027) and Maree Bushey (2028); the "
              "third seat, John Zimmer's, expired in 2026 and the "
              "live page seats Amanda Smith (to 2029)")],
           [holder("Susan Blackstone", "susan-blackstone"),
            holder("Maree Bushey", "maree-bushey"),
            holder("Amanda Smith", "amanda-smith")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Westmore Cemetery Commissioners", 3,
           [S(WMORE_CEMETERY, "Town of Westmore, Cemetery page: "
              "names Miriam Simonds and William Perkins as "
              "commissioner contacts"),
            S(WMORE_REPORT, f"{WMORE_REP_C}: Cemetery "
              "Commissioners Stephen Davenport (2027), William "
              "Perkins (2028), and Miriam Simonds (2029)")],
           [holder("Miriam Simonds", "miriam-simonds"),
            holder("William Perkins", "william-perkins"),
            holder("Stephen Davenport", "stephen-davenport")]),
    office("moderator", "Town Moderator",
           "Town of Westmore Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                   "one-year term"),
            S(WMORE_REPORT, f"{WMORE_REP_C}: Moderator Andrew "
              "Berley, one-year term expiring 2026. The March 2026 "
              "outcome is unpublished, so no holder is minted; "
              "Berley is carried as a straggler on issue #163")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Westmore Collector of Delinquent Taxes", 1,
           [statute2646_structure("towns elect a collector of "
                                   "delinquent taxes"),
            S(WMORE_REPORT, f"{WMORE_REP_C}: Collector of "
              "Delinquent Taxes Annette Parenteau, one-year term "
              "expiring 2026. The March 2026 outcome is "
              "unpublished, so no holder is minted; Parenteau is "
              "carried as a straggler on issue #163")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Westmore Justices of the Peace", 5,
           [jp_src("lists five Westmore justices of the peace: "
                   "Alison J Valley, Christine Evans, Kathy L "
                   "Homes, Linda Michniewicz, and Joanna Burgess"),
            S(WMORE_JP, "Town of Westmore, Justices of the Peace "
              "page: names the same five, printing the third as "
              "Kathy Holmes"),
            S(WMORE_REPORT, f"{WMORE_REP_C}: the justices of the "
              "peace table also prints Kathy Holmes. Both town "
              "sources give 'Holmes' where the certified listing "
              "gives 'Homes'; the person is minted as Kathy "
              "Holmes with the certified form kept as her ballot "
              "name")],
           [holder("Joanna Burgess", "joanna-burgess"),
            holder("Christine Evans", "christine-evans"),
            holder("Kathy Holmes", "kathy-holmes",
                   ballot_name="Kathy L Homes"),
            holder("Linda Michniewicz", "linda-michniewicz"),
            holder("Alison Valley", "alison-valley")]),
], jp=jp_election("westmore-vt", "Town of Westmore", 5,
                  "certifies the November 5, 2024 election of five "
                  "justices of the peace for Westmore: Alison J "
                  "Valley, Christine Evans, Kathy L Homes, Linda "
                  "Michniewicz, and Joanna Burgess"))

# ----------------------------------------------------------------
# Town of Weston (Windsor County) -- general law. Sources: the
# town site (westonvt.org, Squarespace), the 2025 Town Report
# officers table, the official March 3, 2026 Town Meeting Results,
# and the official September 26, 2026 Special Town Meeting Results.
WESTON_TM_C = ("Town of Weston, official Town Meeting Results, "
               "March 3, 2026")
WESTON_SPEC_C = ("Town of Weston, official Special Town Meeting "
                 "Results, September 26, 2026")
SPECS["weston"] = spec("weston", "Town of Weston", [
    office("selectboard", "Selectboard Member",
           "Town of Weston Selectboard", 5,
           [sb_dir("names Denis Benson (Chair), Pamela Dickman, "
                   "Brian Gehlich, James Linville (Vice Chair), "
                   "and Kathleen Moriarty-Fitzpatrick -- a "
                   "pre-September 2026 vintage"),
            S(WESTON_SB, "Town of Weston, Selectboard page (live): "
              "Duane Hart (Chair, seat to 2029), Jim Linville "
              "(Vice Chair, 2028), Kathleen Moriarty-Fitzpatrick "
              "(2028), Brian Gehlich (2027), and Susan Morris "
              "(2027)"),
            S(WESTON_TM26, f"{WESTON_TM_C}: Denis Benson was "
              "re-elected to the three-year seat and a two-year "
              "seat was left vacant"),
            S(WESTON_SPEC26, f"{WESTON_SPEC_C}: after Benson's "
              "departure, the special meeting elected Duane Hart "
              "to the remainder of the three-year seat (to March "
              "2029) and Susan Morris to the remainder of the "
              "two-year seat (to March 2027); both are minted as "
              "elected. Pamela Dickman no longer sits")],
           [holder("Duane Hart", "duane-hart"),
            holder("Jim Linville", "jim-linville"),
            holder("Kathleen Moriarty-Fitzpatrick",
                   "kathleen-moriarty-fitzpatrick"),
            holder("Brian Gehlich", "brian-gehlich"),
            holder("Susan Morris", "susan-morris")]),
    office("moderator", "Town Moderator",
           "Town of Weston Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                         "term"),
            S(WESTON_TM26, f"{WESTON_TM_C}: Article 1 elected "
              "Wayne Granquist Moderator for the ensuing year")],
           [holder("Wayne Granquist", "wayne-granquist")]),
    office("town-clerk", "Town Clerk",
           "Town of Weston Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Kim Seymour as Weston's Town Clerk"),
            S(WESTON_TM26, f"{WESTON_TM_C}: Kim Seymour was "
              "elected Town Clerk (one-year term, as Weston "
              "elects the office)")],
           [holder("Kim Seymour", "kim-seymour")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Weston Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists Kim Seymour as Weston's Town Treasurer"),
            S(WESTON_TM26, f"{WESTON_TM_C}: Kim Seymour was "
              "elected Town Treasurer (one-year term)")],
           [holder("Kim Seymour", "kim-seymour")]),
    office("lister", "Lister",
           "Town of Weston Listers", 3,
           [statute2646("towns elect a board of listers"),
            S(WESTON_LISTERS, "Town of Weston, Listers page: "
              "names Greg Carroll and Jeff Seymour; the third "
              "seat is printed 'VACANT'"),
            S(WESTON_TM26, f"{WESTON_TM_C}: the three-year lister "
              "seat 'remains vacant'; the seated listers' terms "
              "run to 2027 (Carroll) and 2028 (Seymour)")],
           [holder("Greg Carroll", "greg-carroll"),
            holder("Jeff Seymour", "jeff-seymour")]),
    office("library-trustee", "Library Trustee",
           "Town of Weston Library Trustees", 10,
           [S(WESTON_LIBRARY, "Town of Weston, Library page and "
              "the 2025 Town Report's trustees table: a ten-member "
              "board of library trustees on staggered five-year "
              "terms (the board size is derived from the report's "
              "table together with the four seats warned in 2026 "
              "-- flagged on issue #163)"),
            S(WESTON_TM26, f"{WESTON_TM_C}: Carrie Chalmers, "
              "Nicole Pfister, Linda Saarnijoki, and Nancy "
              "O'Connell were elected library trustees in 2026; "
              "the continuing trustees are Deborah Granquist and "
              "Joanne Prouty (2027), Tina Hartell (2028), and "
              "Malcolm Hamblett, Richard Lechthaler, and Gene "
              "Palma (2030)")],
           [holder("Carrie Chalmers", "carrie-chalmers"),
            holder("Nicole Pfister", "nicole-pfister"),
            holder("Linda Saarnijoki", "linda-saarnijoki"),
            holder("Nancy O'Connell", "nancy-oconnell"),
            holder("Deborah Granquist", "deborah-granquist"),
            holder("Joanne Prouty", "joanne-prouty"),
            holder("Tina Hartell", "tina-hartell"),
            holder("Malcolm Hamblett", "malcolm-hamblett"),
            holder("Richard Lechthaler", "richard-lechthaler"),
            holder("Gene Palma", "gene-palma")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Weston Trustees of Public Funds", 3,
           [statute2646("towns elect trustees of public funds"),
            S(WESTON_TPF, "Town of Weston, Trustees of Public "
              "Funds page: Andrew Clapp, Nicole Pfister, and "
              "Ronald Prouty (terms to 2028, 2027, and 2028)")],
           [holder("Andrew Clapp", "andrew-clapp"),
            holder("Nicole Pfister", "nicole-pfister"),
            holder("Ronald Prouty", "ronald-prouty")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Weston Cemetery Commissioners", 5,
           [S(WESTON_CEM, "Town of Weston, Cemeteries page: the "
              "Cemetery Commissioners are Duane Hart (2030), "
              "William Hoyt (2028), Doris Ingram (2029), Richard "
              "'Dick' Lechthaler, and Patrick Walsh (2027), on "
              "five-year terms"),
            S(WESTON_TM26, f"{WESTON_TM_C}: Richard Lechthaler "
              "was re-elected Cemetery Commissioner in 2026")],
           [holder("Duane Hart", "duane-hart"),
            holder("William Hoyt", "william-hoyt"),
            holder("Doris Ingram", "doris-ingram"),
            holder("Richard Lechthaler", "richard-lechthaler"),
            holder("Patrick Walsh", "patrick-walsh")]),
    office("constable", "Constable",
           "Town of Weston Constable", 1,
           [statute2646("towns elect constables"),
            S(WESTON_TM26, f"{WESTON_TM_C}: Marisa Bolognese was "
              "elected Constable (one-year term)")],
           [holder("Marisa Bolognese", "marisa-bolognese")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Weston Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                         "taxes"),
            S(WESTON_DTC, "Town of Weston, Collector of Delinquent "
              "Taxes page: Gretchen Hauser states she was "
              "appointed to fill a vacancy in 2025"),
            S(WESTON_TM26, f"{WESTON_TM_C}: Gretchen Hauser was "
              "elected Collector of Delinquent Taxes in 2026 "
              "(one-year term)")],
           [holder("Gretchen Hauser", "gretchen-hauser")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Weston Justices of the Peace", 5,
           [jp_src("lists five Weston justices of the peace: "
                   "Marisa Bolognese, Carolyn L. Brosseau, Wayne "
                   "G. Granquist, William 'Bill' Hoyt, and Donna "
                   "Taranko-Moulton"),
            S(WESTON_JP24, "Town of Weston, 'Justice of the Peace "
              "Results, November 5, 2024' (official town PDF): "
              "confirms the same five winners. The 2025 Town "
              "Report's JP table (Charles Goodwin, Marguerite "
              "Mason) is stale and is not used")],
           [holder("Marisa Bolognese", "marisa-bolognese"),
            holder("Carolyn L. Brosseau", "carolyn-l-brosseau"),
            holder("Wayne G. Granquist", "wayne-g-granquist",
                   ballot_name="Wayne G. Granquist"),
            holder("William Hoyt", "william-hoyt",
                   ballot_name="William \"Bill\" Hoyt"),
            holder("Donna Taranko-Moulton",
                   "donna-taranko-moulton")]),
], jp=jp_election("weston-vt", "Town of Weston", 5,
                  "certifies the November 5, 2024 election of five "
                  "justices of the peace for Weston: Marisa "
                  "Bolognese, Carolyn L. Brosseau, Wayne G. "
                  "Granquist, William 'Bill' Hoyt, and Donna "
                  "Taranko-Moulton"))

# ----------------------------------------------------------------
# Town of Weybridge (Addison County) -- charter ch. 167: the
# Selectboard appoints the Town Clerk and Town Treasurer (sec. 103);
# general law otherwise. Sources: the 2025 Town Report officers
# table and the town Elections page (2026 results).
WEY_REP_C = ("Town of Weybridge, 2025 Town Report, officers table "
             "(pp. 5-8)")
SPECS["weybridge"] = spec("weybridge", "Town of Weybridge", [
    office("selectboard", "Selectboard Member",
           "Town of Weybridge Selectboard", 5,
           [sb_dir("names Megan Sutton (Chair), Kelly Flynn (Vice "
                   "Chair), T. Charlie Jordan, William Mayers, "
                   "and Stacey Rainey"),
            S(WEY_ELECTIONS, "Town of Weybridge, Elections page, "
              "2026 results: Kelly Flynn was re-elected (137 "
              "votes, two-year term) and Charlie Jordan was "
              "re-elected (175 votes, three-year term)"),
            S(WEY_REPORT, f"{WEY_REP_C}: lists the board with "
              "Megan Sutton as Chair; the report prints 'T. "
              "Charles Jordan' where the directory prints 'T. "
              "Charlie Jordan' -- the report's formal roster form "
              "governs the person name")],
           [holder("Megan Sutton", "megan-sutton"),
            holder("Kelly Flynn", "kelly-flynn"),
            holder("T. Charles Jordan", "t-charles-jordan"),
            holder("Stacey Rainey", "stacey-rainey"),
            holder("William Mayers", "william-mayers")]),
    office("moderator", "Town Moderator",
           "Town of Weybridge Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                         "term"),
            S(WEY_ELECTIONS, "Town of Weybridge, Elections page, "
              "2026 results: Spencer Putnam was re-elected "
              "Moderator (218 votes)")],
           [holder("Spencer Putnam", "spencer-putnam")]),
    office("town-clerk", "Town Clerk",
           "Town of Weybridge Town Clerk", 1,
           [charter167("sec. 103: the Selectboard appoints the "
                       "Town Clerk"),
            S(WEY_REPORT, f"{WEY_REP_C}: 'Town Clerk/Treasurer -- "
              "Appointed -- Brenda Jaring'")],
           [holder("Brenda Jaring", "brenda-jaring",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Weybridge Town Treasurer", 1,
           [charter167("sec. 103: the Selectboard appoints the "
                       "Town Treasurer"),
            S(WEY_REPORT, f"{WEY_REP_C}: 'Town Clerk/Treasurer -- "
              "Appointed -- Brenda Jaring'")],
           [holder("Brenda Jaring", "brenda-jaring",
                   how_seated="appointed")]),
    office("constable", "Constable",
           "Town of Weybridge Constable", 1,
           [charter167("sec. 103: the Selectboard appoints other "
                       "town officers, including the Constable"),
            S(WEY_REPORT, f"{WEY_REP_C}: Constable Kristin "
              "Bowdish, shown as an appointed officer")],
           [holder("Kristin Bowdish", "kristin-bowdish",
                   how_seated="appointed")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Weybridge Collector of Delinquent Taxes", 1,
           [charter167("sec. 103: the Selectboard appoints other "
                       "town officers, including the Collector of "
                       "Delinquent Taxes"),
            S(WEY_REPORT, f"{WEY_REP_C}: Collector of Delinquent "
              "Taxes Phyllis Bowdish, shown as an appointed "
              "officer")],
           [holder("Phyllis Bowdish", "phyllis-bowdish",
                   how_seated="appointed")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Weybridge Trustees of Public Funds", 3,
           [statute2646("towns elect trustees of public funds"),
            S(WEY_REPORT, f"{WEY_REP_C}: Trustee of Public Funds "
              "Diane DaPolito (term to 2028); the other two seats "
              "are printed 'Open Seat' and are vacant")],
           [holder("Diane DaPolito", "diane-dapolito")]),
    office("town-agent", "Town Agent",
           "Town of Weybridge Town Agent", 1,
           [statute2646_structure("towns elect a town agent"),
            S(WEY_REPORT, f"{WEY_REP_C}: Town Agent Nancy "
              "Foster, 'Elected,' term expiring 2026. The 2026 "
              "outcome is unpublished, so no holder is minted; "
              "Foster is carried as a straggler on issue #163")]),
    office("grand-juror", "Grand Juror",
           "Town of Weybridge Grand Juror", 1,
           [statute2646_structure("towns elect a grand juror"),
            S(WEY_REPORT, f"{WEY_REP_C}: Grand Juror Maura "
              "Huddleston, 'Elected,' term expiring 2026. The "
              "2026 outcome is unpublished, so no holder is "
              "minted; Huddleston is carried as a straggler on "
              "issue #163")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Weybridge Justices of the Peace", 5,
           [jp_src("lists five Weybridge justices of the peace: "
                   "Peter James, Amy Mason, Megan Sutton, Jamie "
                   "K. McCallum, and Heather Neuwirth Lovejoy"),
            S(WEY_REPORT, f"{WEY_REP_C}: the justices of the "
              "peace table concurs with the certified slate")],
           [holder("Peter James", "peter-james"),
            holder("Jamie K. McCallum", "jamie-k-mccallum"),
            holder("Amy Mason", "amy-mason"),
            holder("Megan Sutton", "megan-sutton"),
            holder("Heather Neuwirth Lovejoy",
                   "heather-neuwirth-lovejoy")]),
], jp=jp_election("weybridge-vt", "Town of Weybridge", 5,
                  "certifies the November 5, 2024 election of five "
                  "justices of the peace for Weybridge: Peter "
                  "James, Amy Mason, Megan Sutton, Jamie K. "
                  "McCallum, and Heather Neuwirth Lovejoy"))

# ----------------------------------------------------------------
# Town of Wheelock (Caledonia County) -- general law. Source: the
# town's contacts page (current; term years; offices labeled
# Elected/Appointed).
WHEEL_C = ("Town of Wheelock, town contacts page "
           "(townofwheelockvt.org)")
SPECS["wheelock"] = spec("wheelock", "Town of Wheelock", [
    office("selectboard", "Selectboard Member",
           "Town of Wheelock Selectboard", 3,
           [sb_dir("names Ann Lawless (Chair), Charlton Dill, "
                   "and Michael Richardson"),
            S(WHEEL_CONTACTS, f"{WHEEL_C}: Selectboard -- Ann "
              "Lawless (Chair, to 2028), Chuck Dill (to 2027), "
              "and Michael Richardson (Vice Chair, to 2029), all "
              "labeled Elected; the directory's full form "
              "Charlton Dill governs over the page's 'Chuck'")],
           [holder("Ann Lawless", "ann-lawless"),
            holder("Charlton Dill", "charlton-dill"),
            holder("Michael Richardson", "michael-richardson")]),
    office("town-clerk", "Town Clerk",
           "Town of Wheelock Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Erin Swigart as Wheelock's Town Clerk"),
            S(WHEEL_CONTACTS, f"{WHEEL_C}: Town Clerk/Treasurer "
              "Erin Swigart, Elected, term ending 2029")],
           [holder("Erin Swigart", "erin-swigart")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Wheelock Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists Erin Swigart as Wheelock's Town "
                  "Treasurer"),
            S(WHEEL_CONTACTS, f"{WHEEL_C}: Town Clerk/Treasurer "
              "Erin Swigart, Elected, term ending 2029")],
           [holder("Erin Swigart", "erin-swigart")]),
    office("auditor", "Auditor",
           "Town of Wheelock Auditors", 3,
           [statute2646("towns elect a board of auditors"),
            S(WHEEL_CONTACTS, f"{WHEEL_C}: Auditors Kim "
              "Crady-Smith (2027), Scott Lange (2028), and Enid "
              "Ellis (2029), all labeled Elected")],
           [holder("Kim Crady-Smith", "kim-crady-smith"),
            holder("Scott Lange", "scott-lange"),
            holder("Enid Ellis", "enid-ellis")]),
    office("lister", "Lister",
           "Town of Wheelock Listers", 3,
           [statute2646("towns elect a board of listers"),
            S(WHEEL_CONTACTS, f"{WHEEL_C}: Listers Carol Rossi "
              "(2027) and Atti Seguin (2028), labeled Elected; "
              "the third seat (term to 2029) is vacant")],
           [holder("Carol Rossi", "carol-rossi"),
            holder("Atti Seguin", "atti-seguin")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Wheelock Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                         "taxes"),
            S(WHEEL_CONTACTS, f"{WHEEL_C}: Collector of "
              "Delinquent Taxes Teresa Stimpson (2027), labeled "
              "Elected")],
           [holder("Teresa Stimpson", "teresa-stimpson")]),
    office("first-constable", "First Constable",
           "Town of Wheelock First Constable", 1,
           [statute2646("towns elect constables"),
            S(WHEEL_CONTACTS, f"{WHEEL_C}: First Constable Owen "
              "Montgomery (2027), labeled Elected")],
           [holder("Owen Montgomery", "owen-montgomery")]),
    office("second-constable", "Second Constable",
           "Town of Wheelock Second Constable", 1,
           [statute2646("towns elect constables"),
            S(WHEEL_CONTACTS, f"{WHEEL_C}: Second Constable "
              "Shane Lanpher (2027), labeled Elected")],
           [holder("Shane Lanpher", "shane-lanpher")]),
    office("moderator", "Town Moderator",
           "Town of Wheelock Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                   "one-year term"),
            S(WHEEL_CONTACTS, f"{WHEEL_C}: the comprehensive "
              "contacts page omits the moderator's office "
              "entirely, so the holder is unpublished")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Wheelock Justices of the Peace", 5,
           [jp_src("lists four Wheelock justices of the peace: "
                   "Carol Rossi, Kim Crady-Smith, Eileen Boland, "
                   "and Steve Amos"),
            S(WHEEL_CONTACTS, f"{WHEEL_C}: the town page lists "
              "five sitting justices of the peace -- the four "
              "certified winners plus Sharon Fialco, who has no "
              "election record; she is seated as an appointee to "
              "the fifth seat (the appointment mechanism is "
              "unpublished; flagged on issue #163)")],
           [holder("Carol Rossi", "carol-rossi"),
            holder("Kim Crady-Smith", "kim-crady-smith"),
            holder("Eileen Boland", "eileen-boland"),
            holder("Steve Amos", "steve-amos"),
            holder("Sharon Fialco", "sharon-fialco",
                   how_seated="appointed", no_candidacy=True)]),
], jp=jp_election("wheelock-vt", "Town of Wheelock", 4,
                  "certifies the November 5, 2024 election of "
                  "four justices of the peace for Wheelock: Carol "
                  "Rossi, Kim Crady-Smith, Eileen Boland, and "
                  "Steve Amos"))

# ----------------------------------------------------------------
# Town of Whiting (Addison County) -- general law. Sources: the
# town site (whitingvt.com), including the Selectboard minutes of
# July 27 and August 24, 2026, the Lister Board page, and the
# Auditors page.
WHIT_MIN_C = ("Town of Whiting, Selectboard minutes (town site): "
              "the August 24, 2026 minutes' attendance line names "
              "the board as 'SB- Bob Wood, Steve Quenneville, "
              "Marcia King'; the July 27, 2026 minutes concur")
SPECS["whiting"] = spec("whiting", "Town of Whiting", [
    office("selectboard", "Selectboard Member",
           "Town of Whiting Selectboard", 3,
           [sb_dir("lists only Steven Quenneville for Whiting -- "
                   "a thin directory entry"),
            S(WHIT_DOCS, f"{WHIT_MIN_C}. The minutes print 'Bob' "
              "and 'Steve'; the directory and factory full forms "
              "(Robert Wood, Steven Quenneville, Marcia King) "
              "govern the person names")],
           [holder("Robert Wood", "robert-wood"),
            holder("Steven Quenneville", "steven-quenneville"),
            holder("Marcia King", "marcia-king")]),
    office("town-clerk", "Town Clerk",
           "Town of Whiting Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Heather Bouchard as Whiting's Town "
                  "Clerk"),
            S(WHIT_CLERK, "Town of Whiting, Town Clerk page: "
              "Heather Bouchard is the Town Clerk and also the "
              "Town Treasurer")],
           [holder("Heather Bouchard", "heather-bouchard")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Whiting Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists Heather Bouchard as Whiting's Town "
                  "Treasurer"),
            S(WHIT_CLERK, "Town of Whiting, Town Clerk page: "
              "'The Treasurer is an elected position' and the "
              "clerk, Heather Bouchard, holds it")],
           [holder("Heather Bouchard", "heather-bouchard")]),
    office("lister", "Lister",
           "Town of Whiting Listers", 3,
           [statute2646("towns elect a board of listers"),
            S(WHIT_LISTERS, "Town of Whiting, Lister Board page: "
              "Stacey Freeguard, Marguerite 'Peg' Allen, and "
              "Rani Fallon")],
           [holder("Stacey Freeguard", "stacey-freeguard"),
            holder("Marguerite \"Peg\" Allen",
                   "marguerite-peg-allen"),
            holder("Rani Fallon", "rani-fallon")]),
    office("auditor", "Auditor",
           "Town of Whiting Auditors", 3,
           [statute2646("towns elect a board of auditors"),
            S(WHIT_AUDITORS, "Town of Whiting, Auditors page: "
              "Alison Remy, Suzanne Denis, and Pat Mattison")],
           [holder("Alison Remy", "alison-remy"),
            holder("Suzanne Denis", "suzanne-denis"),
            holder("Pat Mattison", "pat-mattison")]),
    office("moderator", "Town Moderator",
           "Town of Whiting Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                   "one-year term"),
            S(WHIT_DOCS, "Town of Whiting, town site: no page or "
              "document on the town's comprehensive site names "
              "the moderator, so the holder is unpublished")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Whiting Justices of the Peace", 5,
           [jp_src("lists five Whiting justices of the peace: "
                   "Stacey Freeguard, Jeanne Leno, Marguerite "
                   "'Peg' Allen, Pat Mattison, and Carolyn "
                   "Schmidt")],
           [holder("Stacey Freeguard", "stacey-freeguard"),
            holder("Jeanne Leno", "jeanne-leno"),
            holder("Marguerite \"Peg\" Allen",
                   "marguerite-peg-allen",
                   ballot_name="Marguerite \"Peg\" Allen"),
            holder("Pat Mattison", "pat-mattison"),
            holder("Carolyn Schmidt", "carolyn-schmidt")]),
], jp=jp_election("whiting-vt", "Town of Whiting", 5,
                  "certifies the November 5, 2024 election of five "
                  "justices of the peace for Whiting: Stacey "
                  "Freeguard, Jeanne Leno, Marguerite 'Peg' Allen, "
                  "Pat Mattison, and Carolyn Schmidt"))

# ----------------------------------------------------------------
# Town of Whitingham (Windham County) -- general law. Sources: the
# town's certified Election Results of March 3, 2026; the 2025 and
# 2026 warnings; the FYE24 Town Report officers page; Selectboard
# minutes; and the department pages on whitinghamvt.org.
WHAM_RES_C = ("Town of Whitingham, Election Results of March 3, "
              "2026 (attested by Rachel Littlehale, Town Clerk)")
WHAM_REP_C = ("Town of Whitingham, Annual Town Report for the "
              "fiscal year ending June 30, 2024, 'Officers for "
              "the Town of Whitingham for the Year 2024'")
SPECS["whitingham"] = spec("whitingham", "Town of Whitingham", [
    office("selectboard", "Selectboard Member",
           "Town of Whitingham Selectboard", 5,
           [sb_dir("names Scott Reed (Chair), Rick Gramlin, Craig "
                   "Hammer, and Lyman Tefft, plus an anomalous "
                   "'Town Council' row for Bob Fisher, who is the "
                   "town's counsel and not a board member"),
            S(WHAM_SB, "Town of Whitingham, Selectboard page: "
              "names five current members -- Scott Reed (Chair), "
              "Rick Gramlin, Lyman 'Skip' Tefft Jr., Craig "
              "Hammer, and Dennis Pike"),
            S(WHAM_RES26, f"{WHAM_RES_C}: Craig Hammer was "
              "elected to the two-year seat (131 votes) and Rick "
              "Gramlin to the three-year seat (136 votes)"),
            S(WHAM_WARN26, "Town of Whitingham, Warning for Town "
              "Meeting 2026 (signed January 21, 2026): the "
              "board's signature block names James Weber as Vice "
              "Chair. Weber has since departed, and the board's "
              "minutes of May 7, 2026 show Dennis Pike sitting "
              "as a member; no election seated Pike, so he holds "
              "the seat as a vacancy appointee (the appointment "
              "minutes are not in the published set; flagged on "
              "issue #163)")],
           [holder("Scott Reed", "scott-reed"),
            holder("Rick Gramlin", "rick-gramlin"),
            holder("Lyman Tefft Jr.", "lyman-tefft-jr"),
            holder("Craig Hammer", "craig-hammer"),
            holder("Dennis Pike", "dennis-pike",
                   how_seated="appointed")]),
    office("moderator", "Town Moderator",
           "Town of Whitingham Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                         "term"),
            S(WHAM_RES26, f"{WHAM_RES_C}: Seth Boyd was elected "
              "Town Moderator (151 votes)")],
           [holder("Seth Boyd", "seth-boyd")]),
    office("town-clerk", "Town Clerk",
           "Town of Whitingham Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Rachel Littlehale as Whitingham's Town "
                  "Clerk"),
            S(WHAM_RES26, f"{WHAM_RES_C}: Rachel Littlehale was "
              "elected Town Clerk (143 votes) to the two years "
              "remaining on a three-year term. The term was won "
              "in 2025 by Almira Aekus (Election Night Results, "
              "March 4, 2025), who departed within the year; "
              "Aekus is not minted")],
           [holder("Rachel Littlehale", "rachel-littlehale")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Whitingham Town Treasurer", 1,
           [S(WHAM_REPORT24, f"{WHAM_REP_C}: the officers table "
              "marks the Town Treasurer with the footnote "
              "'*Position will be an appointed position beginning "
              "March 5, 2025' (the town advertised the post in "
              "February 2025)"),
            guide("lists Marylee Putnam as Whitingham's Town "
                  "Treasurer")],
           [holder("Marylee Putnam", "marylee-putnam",
                   how_seated="appointed")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Whitingham Collector of Delinquent Taxes", 1,
           [S(WHAM_REPORT24, f"{WHAM_REP_C}: the officers table "
              "marks the Delinquent Tax Collector with the same "
              "footnote -- an appointed position beginning March "
              "5, 2025"),
            S(WHAM_COLLECTOR, "Town of Whitingham, Collector of "
              "Taxes page: 'The town Treasurer is the collector "
              "of current and delinquent taxes'; contact person "
              "Marylee Putnam")],
           [holder("Marylee Putnam", "marylee-putnam",
                   how_seated="appointed")]),
    office("road-commissioner", "Road Commissioner",
           "Town of Whitingham Road Commissioner", 1,
           [S(WHAM_RES26, f"{WHAM_RES_C}: Stanley Janovsky Jr "
              "was elected Road Commissioner for a three-year "
              "term (142 votes); the 2024 officers table shows "
              "him holding the same seat on the prior cycle")],
           [holder("Stanley Janovsky Jr.", "stanley-janovsky-jr")]),
    office("library-trustee", "Library Trustee",
           "Town of Whitingham Library Trustees", 5,
           [S(WHAM_REPORT24, f"{WHAM_REP_C}: the library trustee "
              "lines of the officers table resolve to five seats "
              "on three-year staggered terms"),
            S(WHAM_RES26, f"{WHAM_RES_C}: Wendy Sergeant was "
              "elected Library Trustee for a three-year term "
              "(138 votes). The continuing trustees, from the "
              "March 4, 2025 Election Night Results, are Judy "
              "(Judith) Bernard and Tanya Bernard (three-year "
              "terms) and Angela Dornburgh (a two-year "
              "remainder), with Shandell Soumar seated on the "
              "2024 table")],
           [holder("Wendy Sergeant", "wendy-sergeant"),
            holder("Shandell Soumar", "shandell-soumar"),
            holder("Angela Dornburgh", "angela-dornburgh"),
            holder("Tanya Bernard", "tanya-bernard"),
            holder("Judith Bernard", "judith-bernard")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Whitingham Cemetery Commissioners", 3,
           [S(WHAM_RES26, f"{WHAM_RES_C}: Bradford Lackey was "
              "elected Cemetery Commissioner for a three-year "
              "term (150 votes) and Katherine MacLean to the "
              "two years remaining on a three-year term (141 "
              "votes) -- the seat that drew no candidate in "
              "2025"),
            S(WHAM_CEMMIN, "Town of Whitingham, Cemetery "
              "Commission minutes, September 29, 2026: attendees "
              "Brad Lackey, Madeline Klein, and Katherine "
              "MacLean -- the commission is these three members; "
              "Klein is the continuing member (term to 2027)")],
           [holder("Bradford Lackey", "bradford-lackey"),
            holder("Madeline Klein", "madeline-klein"),
            holder("Katherine MacLean", "katherine-maclean")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Whitingham Justices of the Peace", 7,
           [jp_src("lists seven Whitingham justices of the "
                   "peace: Seth Boyd, Julie Muller, Abbie Corse, "
                   "Susan Cooke Johnson, Mary LeMaire, Terry "
                   "Morse, and Rosemary Tefft"),
            S(WHAM_REPORT24, f"{WHAM_REP_C}: the prior cycle's "
              "justices table prints 'Abigail Corse' in full; "
              "the certified form 'Abbie Corse' governs the "
              "person name. Rosemary Tefft is a different person "
              "from Selectboard member Lyman Tefft Jr.")],
           [holder("Seth Boyd", "seth-boyd"),
            holder("Julie Muller", "julie-muller"),
            holder("Abbie Corse", "abbie-corse"),
            holder("Susan Cooke Johnson", "susan-cooke-johnson"),
            holder("Mary LeMaire", "mary-lemaire"),
            holder("Terry Morse", "terry-morse"),
            holder("Rosemary Tefft", "rosemary-tefft")]),
], jp=jp_election("whitingham-vt", "Town of Whitingham", 7,
                  "certifies the November 5, 2024 election of "
                  "seven justices of the peace for Whitingham: "
                  "Seth Boyd, Julie Muller, Abbie Corse, Susan "
                  "Cooke Johnson, Mary LeMaire, Terry Morse, and "
                  "Rosemary Tefft"))

# ----------------------------------------------------------------
# Town of Williamstown (Orange County) -- charter ch. 169 (the
# Treasurer is Selectboard-appointed); clerk stays elected.
# Source: the town's live Town Officers page (term expiries).
WTOWN_C = ("Town of Williamstown, Town Officers page "
           "(williamstownvt.org)")
SPECS["williamstown"] = spec("williamstown", "Town of Williamstown", [
    office("selectboard", "Selectboard Member",
           "Town of Williamstown Selectboard", 5,
           [sb_dir("names Cote Griggs, Laurence Hebert "
                   "(Chairman), Scott McCarthy, Tyler Mitchell, "
                   "and Clayton Woodworth"),
            S(WTOWN_OFFICERS, f"{WTOWN_C}: Selectboard -- "
              "Clayton Woodworth (2027), Larry Hebert (2027), "
              "Cote Griggs (2028), Tyler Mitchell (2028), and "
              "Scott McCarthy (2029)")],
           [holder("Scott McCarthy", "scott-mccarthy"),
            holder("Cote Griggs", "cote-griggs"),
            holder("Tyler Mitchell", "tyler-mitchell"),
            holder("Clayton Woodworth", "clayton-woodworth"),
            holder("Larry Hebert", "larry-hebert")]),
    office("moderator", "Town Moderator",
           "Town of Williamstown Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                         "term"),
            S(WTOWN_OFFICERS, f"{WTOWN_C}: Moderator Heather "
              "King (term expiring 2027)")],
           [holder("Heather King", "heather-king")]),
    office("town-clerk", "Town Clerk",
           "Town of Williamstown Town Clerk", 1,
           [statute2646("towns elect a town clerk; ch. 169 "
                         "converted only the treasurer"),
            guide("lists Barbara Graham as Williamstown's Town "
                  "Clerk"),
            S(WTOWN_OFFICERS, f"{WTOWN_C}: Town Clerk Barbara "
              "Graham (term expiring 2028)")],
           [holder("Barbara Graham", "barbara-graham")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Williamstown Town Treasurer", 1,
           [charter169("sec. 1-2: the elective Town Treasurer "
                       "was converted to a Selectboard-appointed "
                       "position (eff. May 7, 2012)"),
            S(WTOWN_OFFICERS, f"{WTOWN_C}: under Appointed Town "
              "Officers -- Town Treasurer Jenn Allard")],
           [holder("Jenn Allard", "jenn-allard",
                   how_seated="appointed")]),
    office("collector-of-taxes", "Collector of Taxes",
           "Town of Williamstown Collector of Taxes", 1,
           [S(WTOWN_OFFICERS, f"{WTOWN_C}: under Appointed Town "
              "Officers -- Tax Collector Jenn Allard (the "
              "Treasurer serves as collector of current taxes)")],
           [holder("Jenn Allard", "jenn-allard",
                   how_seated="appointed")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Williamstown Collector of Delinquent Taxes", 1,
           [S(WTOWN_OFFICERS, f"{WTOWN_C}: under Appointed Town "
              "Officers -- Delinquent Tax Collector Ryan "
              "Lockwood (the Town Manager)")],
           [holder("Ryan Lockwood", "ryan-lockwood",
                   how_seated="appointed")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Williamstown Trustees of Public Funds", 3,
           [statute2646("towns elect trustees of public funds"),
            S(WTOWN_OFFICERS, f"{WTOWN_C}: Trustees of Public "
              "Funds Orvil Lasell (2027) and Gary Storrs (2028); "
              "the third seat is printed 'Vacant (2029)'")],
           [holder("Orvil Lasell", "orvil-lasell"),
            holder("Gary Storrs", "gary-storrs")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Williamstown Cemetery Commissioners", 5,
           [S(WTOWN_OFFICERS, f"{WTOWN_C}: Cemetery "
              "Commissioners Daphne Herwig (2027), Matt Walker "
              "(2028), Matt Couillard (2030), and Susan Lyons "
              "(2031) -- five seats on five-year staggered "
              "terms, one seat (2029) unlisted and vacant"),
            S(WTOWN_CEMETERY, "Town of Williamstown, Cemetery "
              "page: names commissioners Matt Couillard, Susan "
              "Lyons, and Daphne Herwig. DIVERGENCE: the "
              "department page omits Matt Walker, who is carried "
              "on the officers page with a term to 2028; the "
              "officers page governs and the divergence is "
              "flagged on issue #163. The pages spell the family "
              "name both Couillard and Coulliard; Couillard "
              "governs")],
           [holder("Daphne Herwig", "daphne-herwig"),
            holder("Matt Walker", "matt-walker"),
            holder("Matt Couillard", "matt-couillard"),
            holder("Susan Lyons", "susan-lyons")]),
    office("library-trustee", "Library Trustee",
           "Town of Williamstown Library Trustees", 5,
           [S(WTOWN_OFFICERS, f"{WTOWN_C}: Library Trustees "
              "(Ainsworth Public Library) Laura Carter (2027), "
              "Richard Ferno (2027), Jill McGlynn (2028), Liesl "
              "Wulff (2029), and Helen Duke (2030) -- five seats; "
              "the doubled 2027 expiry is the page's own")],
           [holder("Laura Carter", "laura-carter"),
            holder("Richard Ferno", "richard-ferno"),
            holder("Jill McGlynn", "jill-mcglynn"),
            holder("Liesl Wulff", "liesl-wulff"),
            holder("Helen Duke", "helen-duke")]),
    office("trustee-of-henry-s-baker-fund",
           "Trustee of Henry S. Baker Fund",
           "Town of Williamstown Trustees of Henry S. Baker Fund",
           3,
           [S(WTOWN_OFFICERS, f"{WTOWN_C}: Trustees of Henry S. "
              "Baker Fund Jasmin Couillard (2027), Marie Graham "
              "(2027), and Susan Lyons (2028)")],
           [holder("Jasmin Couillard", "jasmin-couillard"),
            holder("Marie Graham", "marie-graham"),
            holder("Susan Lyons", "susan-lyons")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Williamstown Justices of the Peace", 10,
           [jp_src("lists ten Williamstown justices of the peace "
                   "(the town's block runs across the listing's "
                   "pp. 39-40 page break): Justin Ducey, Barbara "
                   "Graham, Orvil Lasell, Susan Lyons, Heather "
                   "King, Philip Winters, Sherry Chase, Elaine "
                   "Owen, C. Christopher Cate, and Willet Knight "
                   "Jr"),
            S(WTOWN_OFFICERS, f"{WTOWN_C}: the town's justice of "
              "the peace list concurs, printing 'Phil Winters' "
              "and 'Willett Knight, Jr.'; the certified forms "
              "govern")],
           [holder("Justin Ducey", "justin-ducey"),
            holder("Barbara Graham", "barbara-graham"),
            holder("Orvil Lasell", "orvil-lasell"),
            holder("Susan Lyons", "susan-lyons"),
            holder("Heather King", "heather-king"),
            holder("Philip Winters", "philip-winters"),
            holder("Sherry Chase", "sherry-chase"),
            holder("Elaine Owen", "elaine-owen"),
            holder("C. Christopher Cate", "c-christopher-cate"),
            holder("Willet Knight Jr.", "willet-knight-jr")]),
], jp=jp_election("williamstown-vt", "Town of Williamstown", 10,
                  "certifies the November 5, 2024 election of ten "
                  "justices of the peace for Williamstown: Justin "
                  "Ducey, Barbara Graham, Orvil Lasell, Susan "
                  "Lyons, Heather King, Philip Winters, Sherry "
                  "Chase, Elaine Owen, C. Christopher Cate, and "
                  "Willet Knight Jr"))

# ----------------------------------------------------------------
# Town of Williston (Chittenden County) -- charter ch. 171 as
# amended by Act M-12 (2026). Elected: Selectboard, Town Clerk,
# Moderator, Library Trustees (7). Sources: the 2025 Town Report
# (officials listings; March 2026 candidate list; 2025 meeting
# minutes), the town's JP and Cemetery Commission pages, and the
# Dorothy Alling Memorial Library trustee minutes of June 15, 2026.
WILL_REP_C = ("Town of Williston, 2025 Annual Town Report: "
              "'Listing of Town and School District Elected "
              "Officials' and 'List of Candidates for Town and "
              "School Officials to be voted on March 3, 2026'")
SPECS["williston"] = spec("williston", "Town of Williston", [
    office("selectboard", "Selectboard Member",
           "Town of Williston Selectboard", 5,
           [charter171("sec. 14: the Selectboard is one of the "
                       "town's elective offices"),
            sb_dir("names Ellie Beckett, Greta D'Agostino (Vice "
                   "Chair), Mckew Devitt, Jeanne Jensen, and Ted "
                   "Kenney (Chair)"),
            S(WILL_REPORT, f"{WILL_REP_C}: the March 3, 2026 "
              "ballot listed Jeanne Jensen (three-year term) and "
              "McKew Devitt (two-year term) as the sole "
              "candidates; the library trustee minutes of June "
              "15, 2026 record all five members (Kenney, "
              "D'Agostino, Beckett, Jensen, Devitt) in "
              "attendance. Mike Isham has departed")],
           [holder("Ted Kenney", "ted-kenney"),
            holder("Greta D'Agostino", "greta-dagostino"),
            holder("Ellie Beckett", "ellie-beckett"),
            holder("Jeanne Jensen", "jeanne-jensen"),
            holder("McKew Devitt", "mckew-devitt")]),
    office("town-clerk", "Town Clerk",
           "Town of Williston Town Clerk", 1,
           [charter171("sec. 14: the Town Clerk is an elective "
                       "office with a three-year term"),
            guide("lists Sarah Mason as Williston's Town Clerk"),
            S(WILL_REPORT, f"{WILL_REP_C}: the March 3, 2026 "
              "ballot listed Sarah Mason as the sole candidate "
              "for Town Clerk (three-year term)")],
           [holder("Sarah Mason", "sarah-mason")]),
    office("moderator", "Town Moderator",
           "Town of Williston Town Moderator", 1,
           [charter171("sec. 14: the Moderator is one of the "
                       "town's elective offices"),
            S(WILL_REPORT, "Town of Williston, 2025 Annual Town "
              "Report, minutes of the March 2025 annual meeting: "
              "'Christopher D. Roy was unanimously elected "
              "Moderator for the ensuing year.' The office is "
              "filled from the floor at the annual meeting (it "
              "is not on the March 3, 2026 ballot list) and the "
              "2026 outcome is unpublished; Roy presided over "
              "the March 2026 meeting. No holder is minted; Roy "
              "is carried as a straggler on issue #163")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Williston Town Treasurer", 1,
           [charter171("sec. 14-15: the elective treasurer "
                       "subsection is repealed; the Treasurer "
                       "serves under the Town Manager"),
            S(WILL_REPORT, "Town of Williston, 2025 Annual Town "
              "Report, 'Listing of Town Appointed Officials': "
              "Town Treasurer Mary Gratton, term 'Indef'"),
            guide("lists Mary Gratton as Williston's Town "
                  "Treasurer")],
           [holder("Mary Gratton", "mary-gratton",
                   how_seated="appointed")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Williston Collector of Delinquent Taxes", 1,
           [charter171("sec. 15(b)(1): the Collector of "
                       "Delinquent Taxes is appointed by the "
                       "Selectboard"),
            S(WILL_REPORT, "Town of Williston, 2025 Annual Town "
              "Report, 'Listing of Town Appointed Officials': "
              "Collector of Delinquent Taxes Erik Wells (the "
              "Town Manager), term 'Indef'")],
           [holder("Erik Wells", "erik-wells",
                   how_seated="appointed")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Williston Cemetery Commissioners", 5,
           [charter171("sec. 15(b)(5): the Cemetery Commission "
                       "(up to five members) is appointed by the "
                       "Selectboard"),
            S(WILL_CEM, "Town of Williston, Cemetery Commission "
              "page: 'There are five Commissioners appointed by "
              "the Selectboard to staggered five-year terms' -- "
              "Tim Ross (6/30/2027), Hazel Winter (6/30/2028), "
              "and Cameron Clark (6/30/2029); the 2030 and 2031 "
              "seats are open")],
           [holder("Tim Ross", "tim-ross", how_seated="appointed"),
            holder("Hazel Winter", "hazel-winter",
                   how_seated="appointed"),
            holder("Cameron Clark", "cameron-clark",
                   how_seated="appointed")]),
    office("library-trustee", "Library Trustee",
           "Town of Williston Library Trustees", 7,
           [charter171("sec. 14: the Board of Library Trustees "
                       "(seven members, staggered five-year "
                       "terms) is an elective office"),
            S(WILL_LIBBOARD, "Town of Williston, Library Board of "
              "Trustees page: 'The seven members serving on this "
              "board are elected and serve staggered five-year "
              "terms'"),
            S(WILL_REPORT, f"{WILL_REP_C}: lists Stephen Perkins "
              "(2026), Brian Goodwin and Barbara Mieder (2027), "
              "Charity Clark (2028), Diane Downer and Karla "
              "Karstens (2029), and Shari Westman (2030); the "
              "March 3, 2026 ballot listed Stephen J. Perkins as "
              "the sole candidate for the five-year seat"),
            S(WILL_LIBMIN, "Dorothy Alling Memorial Library, "
              "Trustee Minutes, June 15, 2026: present -- "
              "Charity Clark, Shari Westman, Karla Karstens, "
              "Steve Perkins, Diane Downer, Barbara Mieder, and "
              "Brian Goodwin, the full seven-member board")],
           [holder("Stephen J. Perkins", "stephen-j-perkins"),
            holder("Brian Goodwin", "brian-goodwin"),
            holder("Barbara Mieder", "barbara-mieder"),
            holder("Charity R. Clark", "charity-r-clark",
                   existing_person_id="ocd-person/91490526-620b-5fd0-b847-13db063ea337"),
            holder("Diane Downer", "diane-downer"),
            holder("Karla Karstens", "karla-karstens"),
            holder("Shari Westman", "shari-westman")]),
    office("champlain-water-district-representative",
           "Champlain Water District Representative",
           "Champlain Water District", 1,
           [S(WILL_REPORT, f"{WILL_REP_C}: the elected officials "
              "listing shows the Champlain Water District "
              "representative (Liz Royer, term expiring 2026), "
              "and the March 3, 2026 ballot listed Liz Royer as "
              "the sole candidate for a three-year term")],
           [holder("Liz Royer", "liz-royer")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Williston Justices of the Peace", 15,
           [jp_src("lists fifteen Williston justices of the "
                   "peace: Ginny Lyons, Angela Arsenault, Charity "
                   "Clark, Ellie Beckett, Ted Kenney, Debbie "
                   "Ingram, Terry Macaig, Tony Lamb, Sarah Mason, "
                   "Carter Smith, Jeanne Jensen, Andy Mikell, "
                   "Greta D'Agostino, Bruce Roy, and Ruth "
                   "Wallman"),
            S(WILL_JP, "Town of Williston, Justice of the Peace "
              "page ('Current JP's until 1/31/2027'): concurs "
              "name-for-name with the certified slate")],
           [holder("Angela Arsenault", "angela-arsenault",
                   existing_person_id="ocd-person/029525c3-02fc-53e1-9b6e-94db513c0275"),
            holder("Ellie Beckett", "ellie-beckett"),
            holder("Charity R. Clark", "charity-r-clark",
                   ballot_name="Charity Clark",
                   existing_person_id="ocd-person/91490526-620b-5fd0-b847-13db063ea337"),
            holder("Greta D'Agostino", "greta-dagostino"),
            holder("Debbie Ingram", "debbie-ingram"),
            holder("Jeanne Jensen", "jeanne-jensen"),
            holder("Ted Kenney", "ted-kenney"),
            holder("Tony Lamb", "tony-lamb"),
            holder("Virginia \"Ginny\" Lyons", "virginia-ginny-lyons",
                   ballot_name="Ginny Lyons",
                   existing_person_id="ocd-person/6a6e1aa7-d31e-5be1-a79f-98832a63ca70"),
            holder("Terry Macaig", "terry-macaig"),
            holder("Sarah Mason", "sarah-mason"),
            holder("Andy Mikell", "andy-mikell"),
            holder("Bruce Roy", "bruce-roy"),
            holder("Carter Smith", "carter-smith"),
            holder("Ruth Wallman", "ruth-wallman")]),
], jp=jp_election("williston-vt", "Town of Williston", 15,
                  "certifies the November 5, 2024 election of "
                  "fifteen justices of the peace for Williston: "
                  "Ginny Lyons, Angela Arsenault, Charity Clark, "
                  "Ellie Beckett, Ted Kenney, Debbie Ingram, Terry "
                  "Macaig, Tony Lamb, Sarah Mason, Carter Smith, "
                  "Jeanne Jensen, Andy Mikell, Greta D'Agostino, "
                  "Bruce Roy, and Ruth Wallman"))

# ----------------------------------------------------------------
# Town of Wilmington (Windham County) -- general law; town-manager
# town. Sources: the certified Certificate of Votes for March 3,
# 2026; the 2025 Town Report officers pages; the town's board
# pages on wilmingtonvermont.us.
WILM_CERT_C = ("Town of Wilmington, Certificate of Votes for "
               "March 3, 2026 (attested by Therese M. Lounsbury, "
               "Town Clerk)")
WILM_REP_C = ("Town of Wilmington, 2025 Town Report, '2025 Town "
              "Officers, Boards, and Commissions'")
SPECS["wilmington"] = spec("wilmington", "Town of Wilmington", [
    office("selectboard", "Selectboard Member",
           "Town of Wilmington Selectboard", 5,
           [sb_dir("names Thomas Fitzgerald (Chair), John "
                   "Lebron, Vince Rice, Tony Tribuno, and "
                   "Charlie Foster (the directory's row for "
                   "Foster is transposed)"),
            S(WILM_CERT, f"{WILM_CERT_C}: Thomas J. Fitzgerald "
              "was elected to the two-year seat (161 votes) and "
              "Tony Tribuno to the three-year seat (40 votes)"),
            S(WILM_SB, "Town of Wilmington, Selectboard page "
              "(2026): Tom Fitzgerald (Chair), Vince Rice (Vice "
              "Chair), Tony Tribuno, Charlie Foster, and John "
              "Lebron")],
           [holder("Thomas J. Fitzgerald", "thomas-j-fitzgerald"),
            holder("Tony Tribuno", "tony-tribuno"),
            holder("Vince Rice", "vince-rice"),
            holder("Charlie Foster", "charlie-foster"),
            holder("John Lebron", "john-lebron")]),
    office("moderator", "Town Moderator",
           "Town of Wilmington Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                         "term"),
            S(WILM_CERT, f"{WILM_CERT_C}: Robert M. Fisher was "
              "elected Town Moderator (202 votes)")],
           [holder("Robert M. Fisher", "robert-m-fisher")]),
    office("town-clerk", "Town Clerk",
           "Town of Wilmington Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            guide("lists Therese Lounsbury as Wilmington's Town "
                  "Clerk"),
            S(WILM_REPORT, f"{WILM_REP_C}: Town Clerk Therese "
              "Lounsbury, three-year term expiring 2028; she "
              "attested the March 2026 certificate of votes")],
           [holder("Therese Lounsbury", "therese-lounsbury")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Wilmington Town Treasurer", 1,
           [S(WILM_REPORT, f"{WILM_REP_C}: Christine Richter "
              "appears under APPOINTED OFFICIALS as Finance "
              "Officer; no treasurer contest appears on the "
              "March 2026 ballot. The office is modeled as "
              "appointed (flagged on issue #163)"),
            S(WILM_FINANCE, "Town of Wilmington, Treasurer/"
              "Finance Office page: 'Finance Officer/Treasurer "
              "and Tax Collector: Christine Richter' -- she also "
              "serves as collector of taxes; no separate "
              "collector post is modeled"),
            guide("lists Christine Richter as Wilmington's Town "
                  "Treasurer")],
           [holder("Christine Richter", "christine-richter",
                   how_seated="appointed")]),
    office("first-constable", "First Constable",
           "Town of Wilmington First Constable", 1,
           [statute2646("towns elect constables"),
            S(WILM_CERT, f"{WILM_CERT_C}: Gordon 'Joe' Boyd was "
              "elected First Constable (191 votes). He held the "
              "Second Constable office in 2025; the 2025 First "
              "Constable, Gary Wax, has departed")],
           [holder("Gordon Boyd", "gordon-boyd")]),
    office("second-constable", "Second Constable",
           "Town of Wilmington Second Constable", 1,
           [statute2646_structure("towns elect constables"),
            S(WILM_CERT, f"{WILM_CERT_C}: for Second Constable "
              "the certificate records 'NONE REACHING 17 "
              "REQUIRED VOTES' among the write-ins, so the seat "
              "is unfilled and no holder is minted")]),
    office("library-trustee", "Library Trustee",
           "Town of Wilmington Library Trustees", 5,
           [S(WILM_LIB, "Town of Wilmington, Pettee Memorial "
              "Library Trustees page: 'Library Trustees are "
              "elected one each year for five-year terms' -- Tom "
              "Young (Chair), Monique Johnson, Chrystal Holt, "
              "Marie Paige, and Mary Genella"),
            S(WILM_CERT, f"{WILM_CERT_C}: Mary Genella was "
              "elected Library Trustee for five years (195 "
              "votes)"),
            S(WILM_REPORT, f"{WILM_REP_C}: the pre-2026 roster "
              "lists Carolyn Palmer (expiring 2026, succeeded by "
              "Genella) and Louis Clark (to 2029) in the seat "
              "the live page gives to Tom Young; Clark's "
              "departure is unpublished and the live page "
              "governs -- flagged on issue #163")],
           [holder("Tom Young", "tom-young"),
            holder("Monique Johnson", "monique-johnson"),
            holder("Chrystal Holt", "chrystal-holt"),
            holder("Marie Paige", "marie-paige"),
            holder("Mary Genella", "mary-genella")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Wilmington Cemetery Commissioners", 5,
           [S(WILM_CEM, "Town of Wilmington, Cemetery Commission "
              "page: '2026 Cemetery Commission Members (5 year "
              "terms)' -- Janet Boyd (2027), Richard "
              "Khachadoorian (2028), Walter White (2029), Ralph "
              "Staib (2031), and one seat vacant (2030)"),
            S(WILM_CERT, f"{WILM_CERT_C}: Ralph C. Staib was "
              "elected Cemetery Commissioner for five years "
              "(197 votes)"),
            S(WILM_REPORT, f"{WILM_REP_C}: the pre-2026 roster "
              "names Jennifer Goodell in the 2030 seat the live "
              "page shows vacant; Goodell has departed")],
           [holder("Janet Boyd", "janet-boyd"),
            holder("Richard Khachadoorian",
                   "richard-khachadoorian"),
            holder("Walter White", "walter-white"),
            holder("Ralph C. Staib", "ralph-c-staib")]),
    office("trustee-of-cc-haynes-fund",
           "Trustee of C.C. Haynes Fund",
           "Town of Wilmington Trustees of C.C. Haynes Fund", 1,
           [S(WILM_REPORT, f"{WILM_REP_C}: the elected officials "
              "table carries the heading 'Trustee of C.C. "
              "Haynes Fund' with no holder named; the seat count "
              "is also unpublished, so the post is created with "
              "one seat and no membership, flagged on issue "
              "#163")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Wilmington Justices of the Peace", 7,
           [jp_src("lists six Wilmington justices of the peace: "
                   "Bonnie L. Lorimer, Margaret 'Meg' Streeter, "
                   "Joanne Fowler, Andrew Kirkman, John Lebron, "
                   "and Polly 'Nicki' Steel"),
            S(WILM_REPORT, f"{WILM_REP_C}: the town's justice of "
              "the peace roster lists six names plus a 'Vacant' "
              "line (seven seats): the certified winner Joanne "
              "Fowler no longer appears, and Matthew Moore sits "
              "in her place; Moore is seated as an appointee to "
              "the vacancy (mechanism unpublished; flagged on "
              "issue #163)")],
           [holder("Bonnie L. Lorimer", "bonnie-l-lorimer"),
            holder("Margaret \"Meg\" Streeter",
                   "margaret-meg-streeter"),
            holder("Andrew Kirkman", "andrew-kirkman"),
            holder("John Lebron", "john-lebron"),
            holder("Polly \"Nicki\" Steel", "polly-nicki-steel"),
            holder("Matthew Moore", "matthew-moore",
                   how_seated="appointed", no_candidacy=True)]),
], jp=jp_election("wilmington-vt", "Town of Wilmington", 6,
                  "certifies the November 5, 2024 election of six "
                  "justices of the peace for Wilmington: Bonnie L. "
                  "Lorimer, Margaret 'Meg' Streeter, Joanne "
                  "Fowler, Andrew Kirkman, John Lebron, and Polly "
                  "'Nicki' Steel. Fowler is not carried as a "
                  "winner: the town's 2025 Town Report roster "
                  "shows Matthew Moore sitting in her place, so "
                  "she is treated as a departed winner and "
                  "excluded entirely (the contest's vote_for "
                  "remains six); Moore sits as an appointee"))

# ----------------------------------------------------------------
# Town of Windham (Windham County) -- general law. Sources: the
# town's live Town Directory and its "Town Officials of Windham,
# August 2025" form (linked from the directory).
WIND_OFF_C = ("Town of Windham, 'Town Officials of Windham' "
              "(August 2025), the town's own officials form "
              "linked from its Town Directory")
SPECS["windham"] = spec("windham", "Town of Windham", [
    office("selectboard", "Selectboard Member",
           "Town of Windham Selectboard", 3,
           [sb_dir("refers Windham inquiries to the Town Clerk; "
                   "no members are named"),
            S(WIND_OFFICIALS, f"{WIND_OFF_C}: Selectboard -- "
              "Kord Scott (Chair), George Dutton, and Michael "
              "Pelton")],
           [holder("Kord Scott", "kord-scott"),
            holder("George Dutton", "george-dutton"),
            holder("Michael Pelton", "michael-pelton")]),
    office("town-clerk", "Town Clerk",
           "Town of Windham Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(WIND_DIR, "Town of Windham, Town Directory (live): "
              "Town Clerk Emily Shusdock. The August 2025 "
              "officials form and the Secretary of State's Guide "
              "name Bea Eliastam, who has since departed; the "
              "turnover mechanism is unpublished (flagged on "
              "issue #163)")],
           [holder("Emily Shusdock", "emily-shusdock")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Windham Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(WIND_DIR, "Town of Windham, Town Directory (live): "
              "Town Treasurer Cathy Fales. The August 2025 "
              "officials form names Courtney Roth, who has since "
              "departed; the turnover mechanism is unpublished "
              "(flagged on issue #163)")],
           [holder("Cathy Fales", "cathy-fales")]),
    office("lister", "Lister",
           "Town of Windham Listers", 3,
           [statute2646("towns elect a board of listers"),
            S(WIND_DIR, "Town of Windham, Town Directory (live): "
              "Town Listers Bill Casey, Antje Ruppert, and Howie "
              "Ires"),
            S(WIND_OFFICIALS, f"{WIND_OFF_C}: Antje Ruppert is "
              "the Board of Listers chair (the form's 'Rupert' "
              "spelling in the staff block yields to the "
              "directory's 'Ruppert')")],
           [holder("Bill Casey", "bill-casey"),
            holder("Antje Ruppert", "antje-ruppert"),
            holder("Howie Ires", "howie-ires")]),
    office("auditor", "Auditor",
           "Town of Windham Auditors", 3,
           [statute2646("towns elect a board of auditors"),
            S(WIND_OFFICIALS, f"{WIND_OFF_C}: Board of Auditors "
              "-- Kathy Jungermann, Becky Philips, and Pat "
              "McLaine")],
           [holder("Kathy Jungermann", "kathy-jungermann"),
            holder("Becky Philips", "becky-philips"),
            holder("Pat McLaine", "pat-mclaine")]),
    office("road-commissioner", "Road Commissioner",
           "Town of Windham Road Commissioner", 1,
           [S(WIND_OFFICIALS, f"{WIND_OFF_C}: 'Road Commissioner: "
              "Kord Scott.' The office is not created by 17 "
              "V.S.A. section 2646 and no election for it is "
              "published, so the membership is modeled as "
              "appointed with the mechanism unpublished "
              "(flagged on issue #163)")],
           [holder("Kord Scott", "kord-scott",
                   how_seated="appointed")]),
    office("moderator", "Town Moderator",
           "Town of Windham Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                   "one-year term"),
            S(WIND_DIR, "Town of Windham, Town Directory (live): "
              "no section of the directory or the officials form "
              "names a moderator, so the holder is unpublished")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Windham Justices of the Peace", 5,
           [jp_src("lists five Windham justices of the peace: "
                   "Marcia Clinton, Mary McCoy, Philip McDuffie, "
                   "Alan McLaine, and Meredith Tips-McLaine"),
            S(WIND_DIR, "Town of Windham, Town Directory (live), "
              "Justices of the Peace: Mary McCoy, Marcia "
              "Clinton, Meredith Tips-McLaine, and Al McLaine "
              "-- four names; Philip McDuffie no longer appears "
              "and is treated as a departed winner (see the "
              "election note)")],
           [holder("Marcia Clinton", "marcia-clinton"),
            holder("Mary McCoy", "mary-mccoy"),
            holder("Alan McLaine", "alan-mclaine"),
            holder("Meredith Tips-McLaine",
                   "meredith-tips-mclaine")]),
], jp=jp_election("windham-vt", "Town of Windham", 5,
                  "certifies the November 5, 2024 election of five "
                  "justices of the peace for Windham: Marcia "
                  "Clinton, Mary McCoy, Philip McDuffie, Alan "
                  "McLaine, and Meredith Tips-McLaine. McDuffie "
                  "is not carried as a winner: the town's live "
                  "Town Directory lists only the other four as "
                  "sitting justices, so he is treated as a "
                  "departed winner and excluded entirely (the "
                  "contest's vote_for remains five)"))

ORDER = ["westmore", "weston", "weybridge", "wheelock", "whiting",
         "whitingham", "williamstown", "williston", "wilmington",
         "windham"]

for slug in ORDER:
    (OUT / f"{slug}.json").write_text(
        json.dumps(SPECS[slug], indent=1) + "\n")
print("wrote", len(ORDER), "specs")
