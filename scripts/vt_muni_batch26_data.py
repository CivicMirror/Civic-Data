#!/usr/bin/env python3
"""Batch 26 of the VT #163 municipal fan-out (alphabetical positions
250-259): West Burke Village, West Fairlee, West Haven, West Rutland,
West Windsor, Westbury Village, Westfield, Westford, Westminster
Town, Westminster Village. Emits one JSON spec per municipality for
build_vt_municipality.py. Research: vt_muni_batch26_research.md.

Identity calls baked into this batch (all flagged on #163):
- West Fairlee: Jen Shatney holds a cemetery commission seat and a
  JP seat on one record; Staci Sargent holds Town Clerk and
  Collector of Delinquent Taxes. Maurice "Chuck" Eaton, a March
  2024 selectboard winner, is minted only as a JP (he is not on the
  current board). The clerk page's "March 3, 2026 results" link in
  fact serves the MARCH 2024 tally; it is cited as 2024 evidence.
- West Haven: Kerry Ellis holds a selectboard seat and a JP seat;
  Jennifer Jackson is the clerk (the town page's "Jenny" yields to
  the SOS spreadsheet's full form).
- West Rutland: John Harvey (selectboard chair) and the certified
  JP John M. Harvey are one person (same 546 Pleasant Hts address
  in the SOS directory and JP listing); Debora Jasmin holds Town
  Clerk and Town Treasurer. Library trustee Yvonne Wedin is NOT
  minted (the officers table fixes no board size) -- straggler.
- West Windsor: Amy Yates holds Town Clerk and Town Treasurer as
  APPOINTED offices (two consecutive warnings omit both from the
  officers to be elected, and the town report's elected roster omits
  them) and the elected Collector of Delinquent Taxes post, all on
  one record; Nancy Gaynor holds an auditor seat and a JP seat.
  Anne P. Yates the JP is a different person from Amy Yates.
- Westfield: Nicole "Niki" Dunn holds the Town Clerk office as a
  Selectboard appointee filling an unexpired term, plus a JP seat;
  Lisa Deslandes holds Town Treasurer (elected), a lister seat
  (appointed July 20, 2026), and the appointed Collector of
  Delinquent Taxes. The town page's JP list swaps in Karen Blais
  for the certified Anne Lazor -- certified governs; Blais is
  minted as a library trustee only.
- Westford: Kelsi Cross is an appointed library trustee on an
  elected board (hybrid pattern); Patricia Hechmer's expiring
  library seat is a straggler. The town report's JP list diverges
  from the certified slate by three names at equal count --
  certified governs; Dennis Angiono, Martha Bennett, and Suzanne
  Blanchard are not minted.
- Westminster Town: Mildred "Millie" Barry holds Town Clerk
  (term to 2027) and Town Treasurer (elected March 3, 2026 to the
  remaining year after Pauline O'Brien departed). Matthew Conklin
  holds a Campbell Fund trustee seat, a Trustee of Public Funds
  seat, and a JP seat on one record; John Ewald holds a lister
  seat and a JP seat. Charles Lawrence's selectboard seat is
  vacant. The Campbell Fund and public-funds seats decided by
  scattered write-ins only are not minted.
- The three villages are structure-only: no official holder roster
  is published for any of them (all stragglers). Westbury Village
  is in COLCHESTER (SOS villages list), not Middlebury, and is a
  factory gap. Westminster Village's ch. 289 charter remains in
  force although the town's own profile describes the village as
  performing no municipal functions.
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
CHARTER_161 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/161",
    "note": "PLACEHOLDER",
}
CHARTER_163 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/163",
    "note": "PLACEHOLDER",
}
CHARTER_165 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/165",
    "note": "PLACEHOLDER",
}
CHARTER_289 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/289",
    "note": "PLACEHOLDER",
}
VILLAGE_LAW = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24/039",
    "note": "PLACEHOLDER",
}
SOS_VILLAGES = {
    "url": "https://sos.vermont.gov/vsara/learn/municipalities/incorporated-villages",
    "note": "PLACEHOLDER",
}
WF_SB = {"url": "https://westfairleevt.gov/selectboard", "note": "PLACEHOLDER"}
WF_CLERK = {"url": "https://westfairleevt.gov/clerk", "note": "PLACEHOLDER"}
WF_TREASURER = {"url": "https://westfairleevt.gov/treasurer", "note": "PLACEHOLDER"}
WF_LISTERS = {"url": "https://westfairleevt.gov/listers", "note": "PLACEHOLDER"}
WF_CEMETERY = {"url": "https://westfairleevt.gov/cemetery", "note": "PLACEHOLDER"}
WF_LIBRARY = {"url": "https://westfairleevt.gov/library", "note": "PLACEHOLDER"}
WF_JP = {"url": "https://westfairleevt.gov/justicepeace", "note": "PLACEHOLDER"}
WF_DTC = {"url": "https://westfairleevt.gov/tax-collector", "note": "PLACEHOLDER"}
WF_TALLY2024 = {"url": "https://westfairleevt.govoffice3.com/vertical/Sites/%7B11C05066-8FAE-4AAC-9EBF-DC9E04E9CB00%7D/uploads/Town_Meeting_Day_Election_Results_2026.pdf",
                "note": "PLACEHOLDER"}
WF_WARNING2026 = {"url": "https://westfairleevt.gov/vertical/sites/%7B11C05066-8FAE-4AAC-9EBF-DC9E04E9CB00%7D/uploads/03_-_Warning_2026.pdf",
                  "note": "PLACEHOLDER"}
WH_OFFICIALS = {"url": "https://townofwesthavenvt.org/officials-staff/",
                "note": "PLACEHOLDER"}
WR_OFFICERS = {"url": "https://www.westrutlandvt.org/town-officers-appointments/",
               "note": "PLACEHOLDER"}
WW_HOME = {"url": "https://westwindsorvt.govoffice2.com/", "note": "PLACEHOLDER"}
WW_REPORT2025 = {"url": "https://westwindsorvt.govoffice2.com/vertical/sites/%7BD8CDCAEE-6783-4071-AE03-8A27DD92A280%7D/uploads/West_Windsor_Town_Report_2025.pdf",
                 "note": "PLACEHOLDER"}
WW_REPORT2024 = {"url": "https://westwindsorvt.govoffice2.com/vertical/sites/%7BD8CDCAEE-6783-4071-AE03-8A27DD92A280%7D/uploads/2024_West_Windsor_Town_Report.pdf",
                 "note": "PLACEHOLDER"}
WFD_OFFICERS = {"url": "https://westfield.vt.gov/town-departments/",
                "note": "PLACEHOLDER"}
WFD_HOME = {"url": "https://westfield.vt.gov/", "note": "PLACEHOLDER"}
WFO_REPORT2026 = {"url": "https://westfordvt.us/wp-content/uploads/2026/02/Town-Report-2026.pdf",
                  "note": "PLACEHOLDER"}
WFO_SBMIN = {"url": "https://westfordvt.us/wp-content/uploads/2026/05/SELECTBOARD-MARCH-12-2026-V3-Nick-Edits.pdf",
             "note": "PLACEHOLDER"}
WM_REPORT = {"url": "https://www.westminstervt.org/wp-content/uploads/2026/03/TOWN-REPORT-2025-2026.pdf",
             "note": "PLACEHOLDER"}
WM_BALLOT = {"url": "https://www.westminstervt.org/wp-content/uploads/2026/02/WESTMINSTER-VT-BALLOT-PROOF-030326.pdf",
             "note": "PLACEHOLDER"}
WM_TALLY = {"url": "https://www.westminstervt.org/wp-content/uploads/2026/03/20260304124744.pdf",
            "note": "PLACEHOLDER"}
WM_SB = {"url": "https://www.westminstervt.org/selectboard/", "note": "PLACEHOLDER"}
WM_LHMP = {"url": "https://www.westminstervt.org/wp-content/uploads/2022/06/Westminster-LHMP-Draft-06142022.pdf",
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


def charter161(phrase):
    return S(CHARTER_161, f"24 App. V.S.A. ch. 161 (Town of "
             f"West Fairlee): {phrase}")


def charter163(phrase):
    return S(CHARTER_163, f"24 App. V.S.A. ch. 163 (Town of "
             f"Westford): {phrase}")


def charter165(phrase):
    return S(CHARTER_165, f"24 App. V.S.A. ch. 165 (Town of "
             f"Westminster): {phrase}")


def charter289(phrase):
    return S(CHARTER_289, f"24 App. V.S.A. ch. 289 (Village of "
             f"Westminster): {phrase}")


def village_law(phrase):
    return S(VILLAGE_LAW, f"24 V.S.A. ch. 39 (incorporated "
             f"villages): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 26); issue #163 "
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
                  f"# municipal fan-out batch 26; issue #163 "
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
# Village of West Burke (Caledonia County) -- general-law village,
# incorporated under 24 V.S.A. sec. 1301 in 1902 (SOS list). No
# official roster is published online; structure-only build.
SPECS["west-burke"] = spec("west-burke", "Village of West Burke", [
    office("village-trustee", "Village Trustee",
           "Village of West Burke Board of Trustees", 5,
           [village_law("sec. 1304 elects five trustees at the "
                        "village meeting"),
            S(SOS_VILLAGES, "Secretary of State, incorporated "
              "villages list: West Burke, in Burke, Caledonia "
              "County, was incorporated under the general statute "
              "24 V.S.A. sec. 1301 in 1902. No official source "
              "publishes the current trustees, so the post is "
              "created without memberships")]),
    office("village-president", "Village President",
           "Village of West Burke Village President", 1,
           [village_law("sec. 1304 elects a presiding officer; "
                        "the current holder is unpublished, so "
                        "the post is created without a membership")]),
    office("village-clerk", "Village Clerk",
           "Village of West Burke Village Clerk", 1,
           [village_law("sec. 1304 elects a clerk; the current "
                        "holder is unpublished, so the post is "
                        "created without a membership")]),
    office("village-treasurer", "Village Treasurer",
           "Village of West Burke Village Treasurer", 1,
           [village_law("sec. 1304 elects a treasurer; the "
                        "current holder is unpublished, so the "
                        "post is created without a membership")]),
    office("collector-of-taxes", "Collector of Taxes",
           "Village of West Burke Collector of Taxes", 1,
           [village_law("sec. 1304 elects a collector of taxes; "
                        "the current holder is unpublished, so "
                        "the post is created without a membership")]),
])

# ----------------------------------------------------------------
# Town of West Fairlee (Orange County) -- general law except the
# ch. 161 treasurer appointment; floor meeting Feb. 28 + Australian
# ballot March 3, 2026.
WF_TALLY_C = ("Town of West Fairlee, Town Meeting Day election "
              "results tally (the tally the clerk's page links as "
              "the March 3, 2026 results is in fact the March 2024 "
              "tally -- it carries the 2024 presidential primary and "
              "is dated March 4, 2024; cited here as 2024 evidence "
              "only, divergence disclosed on #163)")
SPECS["west-fairlee"] = spec("west-fairlee", "Town of West Fairlee", [
    office("selectboard", "Selectboard Member",
           "Town of West Fairlee Selectboard", 5,
           [sb_dir("names Delsie Hoyt (Chair), Beverly Jo Ash, "
                   "Stuart (Tiger) Bacon, Bree Carlson, and Bruce "
                   "Durkee for West Fairlee's five-member board"),
            S(WF_SB, "Town of West Fairlee, Selectboard page: "
              "Delsie Hoyt, Chair; Beverly Ash; Stuart \"Tiger\" "
              "Bacon; Bree Carlson; Bruce Durkee"),
            S(WF_WARNING2026, "Town of West Fairlee, Warning for "
              "the 2026 Town Meeting (signed January 26, 2026): "
              "the warning is signed by the same five members. "
              "Maurice Eaton, who won a three-year selectboard "
              "seat on the March 2024 tally, is not on the current "
              "board -- he departed by an unpublished mechanism "
              "and is minted only as a justice of the peace")],
           [holder("Delsie Hoyt", "delsie-hoyt"),
            holder("Beverly Jo Ash", "beverly-jo-ash"),
            holder("Stuart Bacon", "stuart-bacon"),
            holder("Bree Carlson", "bree-carlson"),
            holder("Bruce Durkee", "bruce-durkee")]),
    office("town-clerk", "Town Clerk",
           "Town of West Fairlee Town Clerk", 1,
           [S(WF_CLERK, "Town of West Fairlee, Town Clerk page: "
              "Staci Sargent, Town Clerk; she also recorded the "
              "2026 warning"),
            S(WF_TALLY2024, WF_TALLY_C + ": Staci Sargent was "
              "elected Town Clerk for a three-year term in March "
              "2024")],
           [holder("Staci Sargent", "staci-sargent")]),
    office("town-treasurer", "Town Treasurer",
           "Town of West Fairlee Town Treasurer", 1,
           [charter161("sec. 1: the Selectboard appoints the Town "
                       "Treasurer through a nominating-committee "
                       "process -- the office is appointed, not "
                       "elected"),
            S(WF_TREASURER, "Town of West Fairlee, Town Treasurer "
              "page: Joe MacPherson, Treasurer")],
           [holder("Joe MacPherson", "joe-macpherson",
                   how_seated="appointed")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of West Fairlee Collector of Delinquent Taxes", 1,
           [S(WF_DTC, "Town of West Fairlee, Tax Collector page: "
              "Staci Sargent, Collector of Delinquent Taxes"),
            statute2646("towns elect a collector of delinquent "
                        "taxes")],
           [holder("Staci Sargent", "staci-sargent")]),
    office("lister", "Lister",
           "Town of West Fairlee Board of Listers", 3,
           [S(WF_TALLY2024, WF_TALLY_C + ": Kenneth Parrot was "
              "elected Lister for a three-year term in March 2024"),
            S(WF_LISTERS, "Town of West Fairlee, Listers page: "
              "the listers' office contact is Peggy Burden, and "
              "the page states the town contracts an appraisal "
              "consultant to assist the Lister. Burden and Parrot "
              "may hold different seats of the three-member board "
              "or Burden may have succeeded Parrot; the third "
              "seat's holder is unpublished (divergence flagged "
              "on #163)")],
           [holder("Kenneth Parrot", "kenneth-parrot"),
            holder("Peggy Burden", "peggy-burden")]),
    office("auditor", "Auditor",
           "Town of West Fairlee Board of Auditors", 3,
           [S(WF_TALLY2024, WF_TALLY_C + ": Jennifer Williams was "
              "elected Auditor for a three-year term in March "
              "2024; the other two seats' holders are unpublished "
              "-- stragglers")],
           [holder("Jennifer Williams", "jennifer-williams")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of West Fairlee Cemetery Commissioners", 5,
           [S(WF_CEMETERY, "Town of West Fairlee, Cemetery "
              "Commission page: Candy Malinoski, Chair; Jen "
              "Shatney; Darlene Cook; Bart Koop; Jason Johns. "
              "Peter Lange, who won a five-year seat in March "
              "2024, is not on the current commission -- "
              "straggler")],
           [holder("Candy Malinoski", "candy-malinoski"),
            holder("Jen Shatney", "jen-shatney"),
            holder("Darlene Cook", "darlene-cook"),
            holder("Bart Koop", "bart-koop"),
            holder("Jason Johns", "jason-johns")]),
    office("library-trustee", "Library Trustee",
           "Town of West Fairlee Library Trustees", 5,
           [S(WF_LIBRARY, "Town of West Fairlee, West Fairlee "
              "Public Library page, 'Trustees': Jillian Hatch, "
              "Chair; Rebekah Cadwell; Melanie Bacon; Caitlin "
              "Leonard; Sarah Molesworth"),
            S(WF_TALLY2024, WF_TALLY_C + ": a library trustee is "
              "elected by ballot in West Fairlee (Marcia Lange won "
              "a four-year seat in March 2024); Lange is not on "
              "the current board -- straggler. The four-year term "
              "against five listed trustees is flagged on #163")],
           [holder("Jillian Hatch", "jillian-hatch"),
            holder("Rebekah Cadwell", "rebekah-cadwell"),
            holder("Melanie Bacon", "melanie-bacon"),
            holder("Caitlin Leonard", "caitlin-leonard"),
            holder("Sarah Molesworth", "sarah-molesworth")]),
    office("moderator", "Town Moderator",
           "Town of West Fairlee Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term; Christopher "
                                  "Pierce won the office on the "
                                  "floor in 2024 and the current "
                                  "holder is unpublished")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of West Fairlee Justices of the Peace", 5,
           [jp_src("lists three West Fairlee justices of the "
                   "peace: Maurice \"Chuck\" Eaton, Jen Shatney, "
                   "and Rebecca Wurdack"),
            S(WF_JP, "Town of West Fairlee, Justice of the Peace "
              "page ('Terms Ending 2027'): Chuck Eaton, Jennifer "
              "Shatney, and Rebecca Wurdak, with two vacancies on "
              "the five-seat slate; the certified listing's "
              "'Wurdack' governs over the page's 'Wurdak.' "
              "Shatney is also a cemetery commissioner; one "
              "record carries both memberships")],
           [holder("Maurice Eaton", "maurice-eaton",
                   ballot_name="Maurice \"Chuck\" Eaton"),
            holder("Jen Shatney", "jen-shatney"),
            holder("Rebecca Wurdack", "rebecca-wurdack")]),
], jp=jp_election("west-fairlee-vt", "Town of West Fairlee", 5,
                  "certifies the winners of West Fairlee's "
                  "November 5, 2024 justice of the peace election: "
                  "Maurice \"Chuck\" Eaton, Jen Shatney, and "
                  "Rebecca Wurdack were elected; two of the five "
                  "seats drew no winning candidate (the town's "
                  "own justice of the peace page shows the two "
                  "vacancies), so the winners list holds the "
                  "three elected justices"))

# ----------------------------------------------------------------
# Town of West Haven (Rutland County) -- general law; the town's
# Officials & Staff page is the roster of record.
WH_OFF_C = ("Town of West Haven, Officials & Staff page "
            "(townofwesthavenvt.org)")
SPECS["west-haven"] = spec("west-haven", "Town of West Haven", [
    office("selectboard", "Selectboard Member",
           "Town of West Haven Selectboard", 3,
           [S(WH_OFFICIALS, WH_OFF_C + ": 'Select Board Members: "
              "Kerry Ellis - Chair; John Garrison; Elaine "
              "McDevitt'")],
           [holder("Kerry Ellis", "kerry-ellis"),
            holder("John Garrison", "john-garrison"),
            holder("Elaine McDevitt", "elaine-mcdevitt")]),
    office("town-clerk", "Town Clerk",
           "Town of West Haven Town Clerk", 1,
           [S(WH_OFFICIALS, WH_OFF_C + ": 'Town Clerk: Jenny "
              "Jackson'"),
            clerk_xlsx("names Jennifer Jackson as West Haven's "
                       "Town Clerk -- the full form governs over "
                       "the town page's diminutive")],
           [holder("Jennifer Jackson", "jennifer-jackson")]),
    office("town-treasurer", "Town Treasurer",
           "Town of West Haven Town Treasurer", 1,
           [S(WH_OFFICIALS, WH_OFF_C + ": 'Town Treasurer/Tax "
              "Collector: Jennifer Book'"),
            guide("names Jennifer Book as West Haven's Treasurer")],
           [holder("Jennifer Book", "jennifer-book")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of West Haven Collector of Delinquent Taxes", 1,
           [S(WH_OFFICIALS, WH_OFF_C + ": 'Delinquent Tax "
              "Collector: Sharon Ryan'")],
           [holder("Sharon Ryan", "sharon-ryan")]),
    office("lister", "Lister",
           "Town of West Haven Board of Listers", 3,
           [S(WH_OFFICIALS, WH_OFF_C + ": 'Listers: Joan Eckley; "
              "Donald Markie; Susan Trafton'")],
           [holder("Joan Eckley", "joan-eckley"),
            holder("Donald Markie", "donald-markie"),
            holder("Susan Trafton", "susan-trafton")]),
    office("moderator", "Town Moderator",
           "Town of West Haven Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of West Haven Justices of the Peace", 5,
           [jp_src("lists five West Haven justices of the peace: "
                   "Brian Book, Theresa Book, Leland Ellis, Kerry "
                   "Ellis, and Carol Richards. Ellis also holds a "
                   "selectboard seat; one record carries both "
                   "memberships")],
           [holder("Brian Book", "brian-book"),
            holder("Theresa Book", "theresa-book"),
            holder("Leland Ellis", "leland-ellis"),
            holder("Kerry Ellis", "kerry-ellis"),
            holder("Carol Richards", "carol-richards")]),
], jp=jp_election("west-haven-vt", "Town of West Haven", 5,
                  "certifies the five winners of West Haven's "
                  "November 5, 2024 justice of the peace election "
                  "(vote for five): Brian Book, Theresa Book, "
                  "Leland Ellis, Kerry Ellis, and Carol Richards"))

# ----------------------------------------------------------------
# Town of West Rutland (Rutland County) -- general law; the town's
# officers table marks appointed rows "(by appointment)".
WR_OFF_C = ("Town of West Rutland, Town Officers / Appointments "
            "table (the table marks appointed rows '(by "
            "appointment)'; unmarked rows are elected)")
SPECS["west-rutland"] = spec("west-rutland", "Town of West Rutland", [
    office("selectboard", "Selectboard Member",
           "Town of West Rutland Selectboard", 5,
           [sb_dir("names John Harvey, Chester Brown, John "
                   "Center, David Webster, and Robert Bach for "
                   "West Rutland's five-member board"),
            S(WR_OFFICERS, WR_OFF_C + ": Selectpersons -- John "
              "Harvey, Chair (term to 2027); Chester Brown, Vice "
              "Chair (to 2029); John Center, Secretary (to 2028); "
              "David Webster (to 2027); Robert Bach (to 2027)")],
           [holder("John Harvey", "john-harvey"),
            holder("Chester Brown", "chester-brown"),
            holder("John Center", "john-center"),
            holder("David Webster", "david-webster"),
            holder("Robert Bach", "robert-bach")]),
    office("town-clerk", "Town Clerk",
           "Town of West Rutland Town Clerk", 1,
           [S(WR_OFFICERS, WR_OFF_C + ": Town Clerk -- Debora "
              "Jasmin, three-year term to 2028")],
           [holder("Debora Jasmin", "debora-jasmin")]),
    office("town-treasurer", "Town Treasurer",
           "Town of West Rutland Town Treasurer", 1,
           [S(WR_OFFICERS, WR_OFF_C + ": Treasurer -- Debora "
              "Jasmin, three-year term to 2028; she holds the "
              "clerkship on the same record")],
           [holder("Debora Jasmin", "debora-jasmin")]),
    office("moderator", "Town Moderator",
           "Town of West Rutland Town Moderator", 1,
           [S(WR_OFFICERS, WR_OFF_C + ": Town Moderator -- "
              "Michael Moser, one-year term to 2027")],
           [holder("Michael Moser", "michael-moser")]),
    office("lister", "Lister",
           "Town of West Rutland Board of Listers", 3,
           [S(WR_OFFICERS, WR_OFF_C + ": Listers -- Lisa Wright, "
              "Lister/Assessor Chair (term to 2027); the other "
              "two seats are listed 'Vacant' (terms to 2028 and "
              "2026)")],
           [holder("Lisa Wright", "lisa-wright")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of West Rutland Justices of the Peace", 10,
           [jp_src("lists ten West Rutland justices of the peace: "
                   "Marci Barrows, Thomas Burditt, Patricia Kulig, "
                   "Paul Kulig, Elizabeth Moser, David O'Rourke, "
                   "Barbara Trepanier, Tammy Mclaren, Luann Graves, "
                   "and John M. Harvey. Harvey is the selectboard "
                   "chair (the SOS directory and the JP listing "
                   "both place him at 546 Pleasant Heights); one "
                   "record carries both memberships")],
           [holder("Marci Barrows", "marci-barrows"),
            holder("Thomas Burditt", "thomas-burditt"),
            holder("Patricia Kulig", "patricia-kulig"),
            holder("Paul Kulig", "paul-kulig"),
            holder("Elizabeth Moser", "elizabeth-moser"),
            holder("David O'Rourke", "david-orourke"),
            holder("Barbara Trepanier", "barbara-trepanier"),
            holder("Tammy Mclaren", "tammy-mclaren"),
            holder("Luann Graves", "luann-graves"),
            holder("John Harvey", "john-harvey",
                   ballot_name="John M. Harvey")]),
], jp=jp_election("west-rutland-vt", "Town of West Rutland", 10,
                  "certifies the ten winners of West Rutland's "
                  "November 5, 2024 justice of the peace election "
                  "(vote for ten): Marci Barrows, Thomas Burditt, "
                  "Patricia Kulig, Paul Kulig, Elizabeth Moser, "
                  "David O'Rourke, Barbara Trepanier, Tammy "
                  "Mclaren, Luann Graves, and John M. Harvey"))

# ----------------------------------------------------------------
# Town of West Windsor (Windsor County) -- general law; floor
# meeting. The town's official site is its govoffice2 host;
# westwindsorvt.org has lapsed to a parking lander.
WW_REP_C = ("Town of West Windsor, 2025 Town Report, 'TOWN "
            "OFFICES' elected-officers list (with term-expiry "
            "years)")
WW_HOME_C = ("Town of West Windsor, official website homepage, "
             "'2026 Town Meeting Recap'")
SPECS["west-windsor"] = spec("west-windsor", "Town of West Windsor", [
    office("selectboard", "Selectboard Member",
           "Town of West Windsor Selectboard", 3,
           [sb_dir("names Mark Higgins (Chair), Mark Harley, and "
                   "John Brodie for West Windsor's three-member "
                   "board"),
            S(WW_REPORT2025, WW_REP_C + ": Mark Harley, Vice Chair "
              "(term to 2026); John Brodie (to 2027); Mark "
              "Higgins, Chair (to 2028)"),
            S(WW_HOME, WW_HOME_C + ": 'Selectboard - Mark Harley, "
              "reelected by voice vote' at the March 2026 meeting")],
           [holder("Mark Higgins", "mark-higgins"),
            holder("Mark Harley", "mark-harley"),
            holder("John Brodie", "john-brodie")]),
    office("moderator", "Town Moderator",
           "Town of West Windsor Town Moderator", 1,
           [S(WW_HOME, WW_HOME_C + ": 'Article 1 - Moderator, "
              "Shelley Seward, elected by voice vote' (2026). She "
              "succeeds Matthew Birmingham, whose term expired in "
              "2026 and whose memorial the 2025 Town Report "
              "carries")],
           [holder("Shelley Seward", "shelley-seward")]),
    office("town-clerk", "Town Clerk",
           "Town of West Windsor Town Clerk", 1,
           [S(WW_REPORT2025, "Town of West Windsor, 2025 Town "
              "Report: the elected 'TOWN OFFICES' roster omits "
              "the clerk, and the report's directory names 'Amy "
              "W. Yates, Town Clerk/Treasurer'; the 2026 warning "
              "(printed in the report) lists the officers to be "
              "elected in its Article 3 and omits the clerk"),
            S(WW_REPORT2024, "Town of West Windsor, 2024 Town "
              "Report: the warning for the March 2025 meeting "
              "likewise omits the clerk from the officers to be "
              "elected. Two consecutive warnings plus the roster "
              "omission are read as a conversion of the office to "
              "appointment under 17 V.S.A. sec. 2651e; Yates is "
              "seated as the appointee (call disclosed on #163)")],
           [holder("Amy Yates", "amy-yates",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of West Windsor Town Treasurer", 1,
           [S(WW_REPORT2025, "Town of West Windsor, 2025 Town "
              "Report: the elected roster omits the treasurer; "
              "its directory names 'Amy W. Yates, Town "
              "Clerk/Treasurer,' and she signs the treasurer's "
              "report. Read as a sec. 2651f appointment conversion "
              "on the same evidence as the clerkship (disclosed "
              "on #163)")],
           [holder("Amy Yates", "amy-yates",
                   how_seated="appointed")]),
    office("auditor", "Auditor",
           "Town of West Windsor Board of Auditors", 3,
           [S(WW_REPORT2025, WW_REP_C + ": Auditors -- Justin "
              "Burrows (term to 2026); Nancy Gaynor (to 2027); "
              "Barbara Gerstner (to 2028)"),
            S(WW_HOME, WW_HOME_C + ": 'Auditor - Justin Burrows, "
              "reelected by voice vote' (2026). Gaynor also holds "
              "a justice of the peace seat; one record carries "
              "both memberships")],
           [holder("Justin Burrows", "justin-burrows"),
            holder("Nancy Gaynor", "nancy-gaynor"),
            holder("Barbara Gerstner", "barbara-gerstner")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of West Windsor Collector of Delinquent Taxes", 1,
           [S(WW_HOME, WW_HOME_C + ": 'Delinquent Tax Collector - "
              "Amy Yates, reelected by voice vote' (2026) -- this "
              "membership is elected, unlike her appointed clerk "
              "and treasurer posts")],
           [holder("Amy Yates", "amy-yates")]),
    office("first-constable", "First Constable",
           "Town of West Windsor First Constable", 1,
           [S(WW_HOME, WW_HOME_C + ": 'First Constable - Matt "
              "Kantola, reelected by voice vote' (2026)")],
           [holder("Matt Kantola", "matt-kantola")]),
    office("second-constable", "Second Constable",
           "Town of West Windsor Second Constable", 1,
           [S(WW_HOME, WW_HOME_C + ": 'Second Constable - Vacant' "
              "(2026); Mark Morse held the seat to 2026 per the "
              "2025 Town Report and was not reelected, so the "
              "post is created without a membership")]),
    office("town-agent", "Town Agent",
           "Town of West Windsor Town Agent", 1,
           [S(WW_HOME, WW_HOME_C + ": 'Town Agent - Vacant' "
              "(2026) -- the office was warned as a one-year "
              "elective office in 2025; the post is created "
              "without a membership")]),
    office("trustee-of-campbell-fund", "Trustee of Campbell Fund",
           "Town of West Windsor Campbell Fund Trustees", 3,
           [S(WW_REPORT2025, WW_REP_C + ": Campbell Fund Trustees "
              "-- Patricia Kenyon (term to 2026); Jennifer "
              "Hastings Tobias (to 2027); Betty French (to 2028)"),
            S(WW_HOME, WW_HOME_C + ": 'Campbell Fund Trustee - "
              "Patricia Kenyon, reelected by voice vote' (2026)")],
           [holder("Patricia Kenyon", "patricia-kenyon"),
            holder("Jennifer Hastings Tobias",
                   "jennifer-hastings-tobias"),
            holder("Betty French", "betty-french")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of West Windsor Justices of the Peace", 5,
           [jp_src("lists five West Windsor justices of the "
                   "peace: Margaret Clough, Nancy Gaynor, Debra "
                   "Shearer, Debra Bullock Spackman, and Anne P. "
                   "Yates; the town report's short forms (Deb "
                   "Shearer, Deb Spackman, Anne Yates) yield to "
                   "the certified forms. Anne Yates is a different "
                   "person from Amy Yates the clerk/treasurer")],
           [holder("Margaret Clough", "margaret-clough"),
            holder("Nancy Gaynor", "nancy-gaynor"),
            holder("Debra Shearer", "debra-shearer"),
            holder("Debra Bullock Spackman",
                   "debra-bullock-spackman"),
            holder("Anne Yates", "anne-yates",
                   ballot_name="Anne P. Yates")]),
], jp=jp_election("west-windsor-vt", "Town of West Windsor", 5,
                  "certifies the five winners of West Windsor's "
                  "November 5, 2024 justice of the peace election "
                  "(vote for five): Margaret Clough, Nancy Gaynor, "
                  "Debra Shearer, Debra Bullock Spackman, and "
                  "Anne P. Yates"))

# ----------------------------------------------------------------
# Town of Westfield (Orleans County) -- general law; the town's
# officers page labels offices "(elected)" or appointed expressly.
WFD_OFF_C = ("Town of Westfield, Town Officers/Departments page "
             "(westfield.vt.gov; the page labels each office "
             "'(elected)' or appointed)")
SPECS["westfield"] = spec("westfield", "Town of Westfield", [
    office("selectboard", "Selectboard Member",
           "Town of Westfield Selectboard", 3,
           [sb_dir("names Jacques Couture (Chair), Richard Degre, "
                   "and Dennis Vincent for Westfield's "
                   "three-member board"),
            S(WFD_OFFICERS, WFD_OFF_C + ": 'Selectboard: "
              "(elected): Jacques Couture, Chair (expires 2028); "
              "Dennis Vincent, Vice-Chair (expires 2029); "
              "Richard Degre (expires 2027)'")],
           [holder("Jacques Couture", "jacques-couture"),
            holder("Dennis Vincent", "dennis-vincent"),
            holder("Richard Degre", "richard-degre")]),
    office("town-clerk", "Town Clerk",
           "Town of Westfield Town Clerk", 1,
           [S(WFD_OFFICERS, WFD_OFF_C + ": 'Town Clerk: Niki Dunn "
              "(appointed by Selectboard to fill one year of an "
              "unexpired term - expires 2027)' -- the office is "
              "elective but the current holder is an appointee. "
              "The Secretary of State's clerk spreadsheet gives "
              "her full name as Nicole Dunn; the Guide's 'LaDonna "
              "Dunn' is her Assistant Town Clerk (appointed by "
              "the Clerk), a staff role with no post. Dunn also "
              "holds a justice of the peace seat; one record "
              "carries both")],
           [holder("Nicole Dunn", "nicole-dunn",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Westfield Town Treasurer", 1,
           [S(WFD_OFFICERS, WFD_OFF_C + ": 'Town Treasurer: Lisa "
              "Deslandes (elected-expires 2027)'")],
           [holder("Lisa Deslandes", "lisa-deslandes")]),
    office("lister", "Lister",
           "Town of Westfield Board of Listers", 3,
           [S(WFD_OFFICERS, WFD_OFF_C + ": 'Listers: (elected): "
              "Danny Young (Chair) (term expires 2029); Shelley "
              "Martin (term expires 2028); Lisa Deslandes* (term "
              "expires 2027)' with the page's footnote "
              "'*Appointed 7/20/2026' on Deslandes -- her lister "
              "membership is appointed; Young and Martin are "
              "elected")],
           [holder("Danny Young", "danny-young"),
            holder("Shelley Martin", "shelley-martin"),
            holder("Lisa Deslandes", "lisa-deslandes",
                   how_seated="appointed")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Westfield Collector of Delinquent Taxes", 1,
           [S(WFD_OFFICERS, WFD_OFF_C + ": 'Delinquent Tax "
              "Collector: Lisa Deslandes (appointed*)' with the "
              "page's note 'At the 2024 Town Meeting the voters "
              "approved making this an appointed position'"),
            S(WFD_HOME, "Town of Westfield, official website "
              "homepage: 'Tax Collector/Delinquent Tax Collector, "
              "Lisa Deslandes'")],
           [holder("Lisa Deslandes", "lisa-deslandes",
                   how_seated="appointed")]),
    office("library-trustee", "Library Trustee",
           "Town of Westfield Library Trustees", 5,
           [S(WFD_OFFICERS, WFD_OFF_C + ": 'Library Trustees: "
              "(elected) Karen Blais (2027); Jenn Stelma (2028); "
              "Carrie Glessner (2029); Rebecca Velazquez (2030); "
              "Carolyn Lyster (2031)' -- five-year staggered "
              "terms")],
           [holder("Karen Blais", "karen-blais"),
            holder("Jenn Stelma", "jenn-stelma"),
            holder("Carrie Glessner", "carrie-glessner"),
            holder("Rebecca Velazquez", "rebecca-velazquez"),
            holder("Carolyn Lyster", "carolyn-lyster")]),
    office("moderator", "Town Moderator",
           "Town of Westfield Town Moderator", 1,
           [S(WFD_OFFICERS, WFD_OFF_C + ": 'Moderator: Pat Sagui "
              "(elected-term expires 2027)'; Sagui also holds a "
              "justice of the peace seat on the same record")],
           [holder("Pat Sagui", "pat-sagui")]),
    office("first-constable", "First Constable",
           "Town of Westfield First Constable", 1,
           [S(WFD_OFFICERS, WFD_OFF_C + ": '1st Constable: "
              "VACANT' -- the post is created without a "
              "membership")]),
    office("second-constable", "Second Constable",
           "Town of Westfield Second Constable", 1,
           [S(WFD_OFFICERS, WFD_OFF_C + ": '2nd Constable: "
              "VACANT' -- the post is created without a "
              "membership")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Westfield Justices of the Peace", 4,
           [jp_src("lists four Westfield justices of the peace: "
                   "Nicole Dunn, Anne Lazor, Michael Piper, and "
                   "Pat Sagui"),
            S(WFD_OFFICERS, WFD_OFF_C + ": the town's justice of "
              "the peace list names Karen Blais, Niki Dunn, "
              "Michael Piper, and Pat Sagui -- it swaps Blais in "
              "for the certified Anne Lazor at equal count. The "
              "certified listing governs: Lazor is seated and "
              "Blais (minted as a library trustee) is held as a "
              "straggler for this office (divergence flagged on "
              "#163)")],
           [holder("Nicole Dunn", "nicole-dunn"),
            holder("Anne Lazor", "anne-lazor"),
            holder("Michael Piper", "michael-piper"),
            holder("Pat Sagui", "pat-sagui")]),
], jp=jp_election("westfield-vt", "Town of Westfield", 4,
                  "certifies the four winners of Westfield's "
                  "November 5, 2024 justice of the peace election "
                  "(vote for four): Nicole Dunn, Anne Lazor, "
                  "Michael Piper, and Pat Sagui"))

# ----------------------------------------------------------------
# Town of Westford (Chittenden County) -- ch. 163 charter: elected
# officers per state law (sec. 2); the Selectboard appoints the
# Treasurer, listers or an assessor, the Delinquent Tax
# Collector, and cemetery commissioners (sec. 3).
WFO_REP_C = ("Town of Westford, Town Report 2026 (for the March "
             "2026 annual meeting), 'ELECTED TOWN OFFICES' and "
             "'APPOINTED TOWN OFFICES' lists")
SPECS["westford"] = spec("westford", "Town of Westford", [
    office("selectboard", "Selectboard Member",
           "Town of Westford Selectboard", 5,
           [S(WFO_REPORT2026, WFO_REP_C + ": Selectboard -- Deb "
              "Sawyer Jorschick (term expires 2026); Casey "
              "Mathieu (2026); Patrick Haller (2027); Julia "
              "Andrews (2027); William \"Nick\" Nichols (2028)"),
            S(WFO_SBMIN, "Town of Westford, Selectboard minutes, "
              "March 12, 2026: 'Casey Mathieu and Deb Jorschick "
              "had been reelected to the Selectboard at the March "
              "3, 2026 Town Meeting and there were no changes to "
              "the makeup of the Selectboard'; the minutes elect "
              "Patrick Haller chair")],
           [holder("Patrick Haller", "patrick-haller"),
            holder("Casey Mathieu", "casey-mathieu"),
            holder("Julia Andrews", "julia-andrews"),
            holder("William Nichols", "william-nichols"),
            holder("Deb Sawyer Jorschick", "deb-sawyer-jorschick")]),
    office("town-clerk", "Town Clerk",
           "Town of Westford Town Clerk", 1,
           [S(WFO_REPORT2026, WFO_REP_C + ": 'Town Clerk (3 years, "
              "term expires 2028): Callie Hamdy'; the report's "
              "March 2025 meeting minutes record her election to "
              "the three-year term"),
            charter163("sec. 2: the elected officers of the town "
                       "are those required by state law, elected "
                       "by Australian ballot")],
           [holder("Callie Hamdy", "callie-hamdy")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Westford Town Treasurer", 1,
           [charter163("sec. 3: the Selectboard appoints the Town "
                       "Treasurer"),
            S(WFO_REPORT2026, WFO_REP_C + ": 'APPOINTED TOWN "
              "OFFICES: Town Treasurer -- Gregory Barrows'")],
           [holder("Gregory Barrows", "greg-barrows",
                   how_seated="appointed")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Westford Collector of Delinquent Taxes", 1,
           [charter163("sec. 3: the Selectboard appoints the "
                       "Delinquent Tax Collector"),
            S(WFO_REPORT2026, WFO_REP_C + ": 'APPOINTED TOWN "
              "OFFICES: Delinquent Tax Collector -- Marjorie "
              "McIntosh (Retired 2026)' -- no successor is "
              "published, so the post is created without a "
              "membership")]),
    office("library-trustee", "Library Trustee",
           "Town of Westford Library Trustees", 5,
           [S(WFO_REPORT2026, WFO_REP_C + ": Library Trustees -- "
              "Patricia Hechmer (term expires 2026); Kelsi Cross "
              "(2027, marked '(Appointed)'); Marianne Bassford "
              "(2028); Helen Sterling, Chair (2029); Becky Roy "
              "(2030) -- five-year staggered terms. Cross is "
              "seated as an appointee on the elected board; "
              "Hechmer's seat stood at the March 2026 meeting "
              "with no published outcome -- straggler")],
           [holder("Marianne Bassford", "marianne-bassford"),
            holder("Helen Sterling", "helen-sterling"),
            holder("Becky Roy", "becky-roy"),
            holder("Kelsi Cross", "kelsi-cross",
                   how_seated="appointed")]),
    office("moderator", "Town Moderator",
           "Town of Westford Town Moderator", 1,
           [S(WFO_REPORT2026, WFO_REP_C + ": 'Town Moderator (1 "
              "year, term expires 2026): VACANT' -- the 2025 "
              "holder, Lee McClenny, departed and the 2026 floor "
              "outcome is unpublished, so the post is created "
              "without a membership")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Westford Justices of the Peace", 7,
           [jp_src("lists seven Westford justices of the peace: "
                   "Caroline Brown, Lynn Bursell, Christian "
                   "Frenette, Martha Heath, Andrea Letorney, "
                   "Derrick Kendrew, and Francois Ross"),
            S(WFO_REPORT2026, WFO_REP_C + ": the town report's "
              "justice of the peace list names Dennis Angiono, "
              "Martha Bennett, Lynn Bursell, Andrea Letorney, "
              "Christian Frenette, Suzanne Blanchard, and Martha "
              "Heath -- a three-name divergence from the "
              "certified slate at equal count (it omits Brown, "
              "Kendrew, and Ross). The certified listing "
              "governs; Angiono, Bennett, and Blanchard are held "
              "as stragglers (possible Board of Civil Authority "
              "appointees), flagged on #163")],
           [holder("Caroline Brown", "caroline-brown"),
            holder("Lynn Bursell", "lynn-bursell"),
            holder("Christian Frenette", "christian-frenette"),
            holder("Martha Heath", "martha-heath"),
            holder("Andrea Letorney", "andrea-letorney"),
            holder("Derrick Kendrew", "derrick-kendrew"),
            holder("Francois Ross", "francois-ross")]),
], jp=jp_election("westford-vt", "Town of Westford", 7,
                  "certifies the seven winners of Westford's "
                  "November 5, 2024 justice of the peace election "
                  "(vote for seven): Caroline Brown, Lynn Bursell, "
                  "Christian Frenette, Martha Heath, Andrea "
                  "Letorney, Derrick Kendrew, and Francois Ross"))

# ----------------------------------------------------------------
# Town of Westminster (Windham County) -- ch. 165 charter sec. 2
# keeps the general-law officers. Sources: the 2025-2026 Town
# Report's elected-officials list, the official March 3, 2026
# sample ballot, and the certified March 3, 2026 tally (uploaded
# to the town site March 4, 2026).
WM_REP_C = ("Town of Westminster, Town Report 2025-2026, 'Town of "
            "Westminster - Elected Officials' list (with "
            "term-expiration dates)")
WM_TALLY_C = ("Town of Westminster, certified return of votes for "
              "the March 3, 2026 annual election (machine tally, "
              "certified by the election inspectors; posted on the "
              "town clerk's page)")
SPECS["westminster-81400"] = spec("westminster-81400",
                                  "Town of Westminster", [
    office("selectboard", "Selectboard Member",
           "Town of Westminster Selectboard", 5,
           [S(WM_REPORT, WM_REP_C + ": Selectboard -- Craig Allen "
              "(term to 2028); Jason Perry (to 2027); Real Bazin "
              "(to 2026); Charles Lawrence (to 2027); Stephen "
              "Major (to 2026)"),
            S(WM_TALLY, WM_TALLY_C + ": SELECTBOARD 3 YEARS -- "
              "Stephen Major 230; SELECTBOARD 2 YEARS -- Real J. "
              "Bazin, Sr. 207"),
            S(WM_SB, "Town of Westminster, Selectboard page "
              "(current): 'Members: Craig Allen, Chair; Real "
              "Bazin, Vice Chair; Jason Perry, Clerk; Stephen "
              "Major, Member; Vacancy' -- Lawrence's seat is "
              "vacant (the town posted a selectboard-member "
              "vacancy notice in April 2026); no appointee is "
              "published")],
           [holder("Craig Allen", "craig-allen"),
            holder("Real Bazin", "real-bazin"),
            holder("Jason Perry", "jason-perry"),
            holder("Stephen Major", "stephen-major")]),
    office("moderator", "Town Moderator",
           "Town of Westminster Town Moderator", 1,
           [S(WM_TALLY, WM_TALLY_C + ": MODERATOR OF THE TOWN -- "
              "David Major 234")],
           [holder("David Major", "david-major")]),
    office("town-clerk", "Town Clerk",
           "Town of Westminster Town Clerk", 1,
           [S(WM_REPORT, WM_REP_C + ": 'Town Clerk: (3 Year) "
              "Mildred Barry' with term expiring March 2027 -- "
              "the seat did not stand in 2026"),
            guide("names Mildred Barry as Westminster's Town "
                  "Clerk")],
           [holder("Mildred Barry", "mildred-barry")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Westminster Town Treasurer", 1,
           [S(WM_REPORT, WM_REP_C + ": 'Town Treasurer (3 Year) "
              "Pauline O'Brien' with term expiring March 2027"),
            S(WM_BALLOT, "Town of Westminster, official ballot "
              "for March 3, 2026: the treasurer race is for the "
              "'Remaining 1 year of a three-year term' with "
              "Mildred (Millie) Barry the printed candidate -- "
              "O'Brien departed before her term ended"),
            S(WM_TALLY, WM_TALLY_C + ": TREASURER -- Mildred "
              "(Millie) Barry 239. Barry holds the clerkship and "
              "the treasurership on one record")],
           [holder("Mildred Barry", "mildred-barry")]),
    office("lister", "Lister",
           "Town of Westminster Board of Listers", 3,
           [S(WM_REPORT, WM_REP_C + ": Board of Listers -- Jacklyn "
              "Atwood (term to 2027), with two seats expiring in "
              "2026"),
            S(WM_TALLY, WM_TALLY_C + ": LISTER 3 YEARS -- John E. "
              "Ewald 210. The LISTER 2 YEARS REM race drew 15 "
              "scattered write-in votes with no name tallied, so "
              "no winner is recorded for the third seat. Ewald "
              "also holds a justice of the peace seat on the "
              "same record")],
           [holder("Jacklyn Atwood", "jacklyn-atwood"),
            holder("John Ewald", "john-ewald")]),
    office("commissioner-of-campbell-fund",
           "Commissioner of the Campbell Fund",
           "Town of Westminster Commissioners of the Campbell Fund",
           3,
           [S(WM_REPORT, WM_REP_C + ": Commissioners of the "
              "Campbell Fund: (1 Year) Karen Walter; Matthew "
              "Conklin; Vacant (all expiring March 2026)"),
            S(WM_TALLY, WM_TALLY_C + ": COMMISSIONER OF CAMPBELL "
              "FUND (3) -- Karen Walter 228, with 14 scattered "
              "write-in votes and no other name tallied: only "
              "Walter is recorded as elected to the three "
              "one-year seats in 2026")],
           [holder("Karen Walter", "karen-walter")]),
    office("trustee-of-campbell-fund", "Trustee of Campbell Fund",
           "Town of Westminster Campbell Fund Trustees", 3,
           [S(WM_REPORT, WM_REP_C + ": Trustees of Campbell Fund: "
              "(3 Year) Michael Fawcett (to 2027); Peter Harrison "
              "(to 2028, marked 'Resigned'); Barbara Taylor (to "
              "2026)"),
            S(WM_TALLY, WM_TALLY_C + ": TRUSTEE CAMPBELL FUND -- "
              "Matthew S. Conklin 220 (the resigned seat's "
              "remaining two years). The three-year seat (Taylor) "
              "drew 22 scattered write-in votes with no name "
              "tallied, so no winner is recorded for it")],
           [holder("Michael Fawcett", "michael-fawcett"),
            holder("Matthew Conklin", "matthew-conklin")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Westminster Trustees of Public Funds", 3,
           [S(WM_BALLOT, "Town of Westminster, official ballot for "
              "March 3, 2026: Trustee of Public Funds races for a "
              "three-year term and for the remaining two years of "
              "a three-year term (Matthew S. Conklin the printed "
              "candidate for the remainder)"),
            S(WM_TALLY, WM_TALLY_C + ": TRUSTEE OF PUBLIC FUNDS "
              "2 YEARS REM -- Matthew S. Conklin 227. The "
              "three-year race drew 25 scattered write-in votes "
              "with no name tallied, so no winner is recorded "
              "for that seat")],
           [holder("Matthew Conklin", "matthew-conklin")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Westminster Justices of the Peace", 11,
           [jp_src("lists eleven Westminster justices of the "
                   "peace: Matt Conklin, Frances (Nancy) Dalzell, "
                   "John Ewald, Elizabeth Harlow, Susan Harlow, "
                   "Charles Lovell, Adrienne Major, Susan Roman, "
                   "Peggy O'Toole, Jeanette Staley, and Sarah "
                   "Waldo. Conklin's full form, Matthew Conklin, "
                   "follows the town's certified 2026 tally")],
           [holder("Matthew Conklin", "matthew-conklin",
                   ballot_name="Matt Conklin"),
            holder("Frances Dalzell", "frances-dalzell",
                   ballot_name="Frances (Nancy) Dalzell"),
            holder("John Ewald", "john-ewald"),
            holder("Elizabeth Harlow", "elizabeth-harlow"),
            holder("Susan Harlow", "susan-harlow"),
            holder("Charles Lovell", "charles-lovell"),
            holder("Adrienne Major", "adrienne-major"),
            holder("Susan Roman", "susan-roman"),
            holder("Peggy O'Toole", "peggy-otoole"),
            holder("Jeanette Staley", "jeanette-staley"),
            holder("Sarah Waldo", "sarah-waldo")]),
], jp=jp_election("westminster-vt", "Town of Westminster", 11,
                  "certifies the eleven winners of Westminster's "
                  "November 5, 2024 justice of the peace election: "
                  "Matt Conklin, Frances (Nancy) Dalzell, John "
                  "Ewald, Elizabeth Harlow, Susan Harlow, Charles "
                  "Lovell, Adrienne Major, Susan Roman, Peggy "
                  "O'Toole, Jeanette Staley, and Sarah Waldo"))

# ----------------------------------------------------------------
# Village of Westminster (Windham County) -- ch. 289 (Act 334 of
# 1912). The charter remains in force and the village remains on
# the SOS list, but no holder roster is published; structure-only.
SPECS["westminster"] = spec("westminster", "Village of Westminster", [
    office("village-trustee", "Village Trustee",
           "Village of Westminster Board of Trustees", 5,
           [charter289("sec. 4: the officers of the corporation "
                       "shall be a Board of five trustees, with "
                       "five-year terms"),
            S(WM_LHMP, "Town of Westminster, Local Hazard "
              "Mitigation Plan profile: the Village of "
              "Westminster 'in recent times has performed no "
              "municipal functions... Its governance structure "
              "is all volunteer and consists of five trustees a "
              "treasurer and a clerk.' No official source names "
              "the current trustees, so the post is created "
              "without memberships")]),
    office("village-clerk", "Village Clerk",
           "Village of Westminster Village Clerk", 1,
           [charter289("sec. 4 elects a Clerk for a one-year "
                       "term; the current holder is unpublished, "
                       "so the post is created without a "
                       "membership")]),
    office("village-treasurer", "Village Treasurer",
           "Village of Westminster Village Treasurer", 1,
           [charter289("sec. 4 elects a Treasurer for a one-year "
                       "term; the current holder is unpublished, "
                       "so the post is created without a "
                       "membership")]),
    office("collector-of-taxes", "Collector of Taxes",
           "Village of Westminster Collector of Taxes", 1,
           [charter289("sec. 4 elects a Collector of Taxes for a "
                       "one-year term; the town profile states the "
                       "village no longer collects taxes, and no "
                       "holder is published, so the post is "
                       "created without a membership")]),
    office("village-auditor", "Village Auditor",
           "Village of Westminster Village Auditor", 1,
           [charter289("sec. 4 elects an Auditor for a one-year "
                       "term; the current holder is unpublished, "
                       "so the post is created without a "
                       "membership")]),
])

# ----------------------------------------------------------------
# Village of Westbury (Chittenden County, in the Town of
# Colchester) -- formed under 24 V.S.A. sec. 1301; acknowledged by
# the Colchester Selectboard in 2023 (SOS villages list). A
# factory gap. No official roster is published; structure-only.
SPECS["westbury"] = spec("westbury", "Village of Westbury", [
    office("village-trustee", "Village Trustee",
           "Village of Westbury Board of Trustees", 5,
           [village_law("sec. 1304 elects five trustees at the "
                        "village meeting"),
            S(SOS_VILLAGES, "Secretary of State, incorporated "
              "villages list: 'Westbury: in Colchester, "
              "Chittenden County; acknowledged by Colchester "
              "Selectboard in 2023.' No official source publishes "
              "the village's officers (the formation project's "
              "website names none), so the post is created "
              "without memberships and the roster is held for "
              "the straggler sweep")]),
    office("village-president", "Village President",
           "Village of Westbury Village President", 1,
           [village_law("sec. 1304 elects a presiding officer; "
                        "the current holder is unpublished, so "
                        "the post is created without a membership")]),
    office("village-clerk", "Village Clerk",
           "Village of Westbury Village Clerk", 1,
           [village_law("sec. 1304 elects a clerk; the current "
                        "holder is unpublished, so the post is "
                        "created without a membership")]),
    office("village-treasurer", "Village Treasurer",
           "Village of Westbury Village Treasurer", 1,
           [village_law("sec. 1304 elects a treasurer; the "
                        "current holder is unpublished, so the "
                        "post is created without a membership")]),
    office("collector-of-taxes", "Collector of Taxes",
           "Village of Westbury Collector of Taxes", 1,
           [village_law("sec. 1304 elects a collector of taxes; "
                        "the current holder is unpublished, so "
                        "the post is created without a membership")]),
])

ORDER = ["west-burke", "west-fairlee", "west-haven", "west-rutland",
         "west-windsor", "westbury", "westfield", "westford",
         "westminster-81400", "westminster"]

for slug in ORDER:
    (OUT / f"{slug}.json").write_text(
        json.dumps(SPECS[slug], indent=1) + "\n")
print("wrote", len(ORDER), "specs")
