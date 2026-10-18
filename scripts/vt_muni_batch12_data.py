#!/usr/bin/env python3
"""Batch 12 of the VT #163 municipal fan-out (alphabetical positions
110-119): Jacksonville Village, Jamaica, Jay, Jeffersonville
Village, Jericho (town), Jericho Village, Johnson (town), Johnson
Village, Killington, Kirby. Emits one JSON spec per municipality
for build_vt_municipality.py.
Research: vt_muni_batch12_research.md.

Identity calls baked into this batch (all flagged on #163):
- Killington's Selectboard follows the town's own Elected
  Officials page (updated Aug 2026): Celia Clancy sits, and
  the June 2026 SOS directory's Ricky Bowen is stale. The
  factory agrees with the town page. Killington's JP slate
  follows the certified SOS listing (one winner, Patrick
  Cushing); the town page's seven-name JP block is a stale
  carryover that omits Cushing.
- Johnson (town) clerk/treasurer turned over in spring 2026:
  Rosemary Audibert attested the March 4, 2026 certificate as
  Town Clerk, but the town's current directory seats Susan
  Tinker as clerk (the town clerk page states the office is
  appointed by the Selectboard) and Lydia Beach Putvain as
  treasurer; the June 2026 SOS spreadsheets agree. The
  January 2026 Guide's Audibert for both is pre-transition.
- Johnson Village's factory roster is stale: Steven Hatfield
  retired at the April 2025 annual meeting; Ellis O'Hear
  holds his trustee seat (village minutes govern).
- Jacksonville's trustee roster is the Village's own board
  page (hosted by the Jacksonville Electric Company, the
  village's utility): the same five names as the factory,
  with rotated board roles. Laura Allen is styled "Interim"
  there; the charter fills vacancies only at special
  meetings, so she is minted as a seated trustee with the
  styling disclosed.
- Eric Osgood is Johnson Village President and a Johnson
  (town) justice of the peace -- one person record scoped
  to the town (person_scope), the town built before the
  village in this batch.
- Johnson (town) and Jericho each list a Jennifer Burton as
  a justice of the peace; the office is town-bound, so
  these are two person records and the second-built file
  takes the builder's collision suffix.
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
CHARTER_227 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/227",
    "note": "PLACEHOLDER",
}
CHARTER_123B = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/123B",
    "note": "PLACEHOLDER",
}
CHARTER_124 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/124",
    "note": "PLACEHOLDER",
}


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


def charter227(phrase):
    return S(CHARTER_227, f"24 App. V.S.A. ch. 227 (Village of "
             f"Jacksonville charter): {phrase}")


def charter123b(phrase):
    return S(CHARTER_123B, f"24 App. V.S.A. ch. 123B (Town of "
             f"Jamaica charter): {phrase}")


def charter124(phrase):
    return S(CHARTER_124, f"24 App. V.S.A. ch. 124 (Town of "
             f"Jericho charter): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 12); issue #163 "
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
                  f"# municipal fan-out batch 12; issue #163 "
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
    }
    if holders:
        d["holders"] = list(holders)
    d.update(kw)
    return d


SPECS = {}
ORDER = ["jacksonville", "jamaica", "jay", "jeffersonville",
         "jericho", "jericho-village", "johnson-37075", "johnson",
         "killington", "kirby"]

# ------------------------------------------------------------ Jacksonville
JEC_BOARD = {
    "url": "https://www.jec.energy/board/",
    "note": "PLACEHOLDER",
}


def jacksonville_spec():
    offices = [
        office("village-trustee", "Village Trustee",
               "Jacksonville Board of Trustees", 5,
               [charter227("section 3(a), as amended by 2005 No. "
                           "M-15: five trustees are elected at the "
                           "annual meeting and serve until their "
                           "successors are elected; section 3(b) "
                           "the trustees elect one of themselves "
                           "President, so no president post is "
                           "created"),
                S(JEC_BOARD, "Village of Jacksonville (official "
                             "site of the Jacksonville Electric "
                             "Company, the village's municipal "
                             "utility), 'Board of Trustees' page: "
                             "the page styles the body 'The "
                             "Village of Jacksonville's Board of "
                             "Trustee[s]' and lists the current "
                             "trustees as Kenneth Bernard (term "
                             "to 2027), Laura Allen, Interim "
                             "(2028), John Doty, Treasurer (2029), "
                             "Jenepher Burnell, President (2030), "
                             "and Tyler Colford, Clerk (2031); "
                             "the parenthetical roles are board "
                             "offices, not separate posts. Allen "
                             "is styled 'Interim'; the charter "
                             "fills vacancies only at special "
                             "meetings called for that purpose "
                             "(section 3(a)), so she is recorded "
                             "as a seated trustee with the "
                             "styling disclosed")],
               [holder("Kenneth Bernard", "kenneth-bernard"),
                holder("Laura Allen", "laura-allen"),
                holder("John Doty", "john-doty"),
                holder("Jenepher Burnell", "jenepher-burnell"),
                holder("Tyler Colford", "tyler-colford")]),
        office("village-clerk", "Village Clerk",
               "Jacksonville Village Clerk", 1,
               [charter227("section 3(a): a clerk is elected at "
                           "the annual meeting; no official "
                           "source publishes the current holder, "
                           "so the post is created without a "
                           "membership. The electric board's "
                           "'Clerk' annotation is a board role "
                           "and is not shown to be this office")]),
        office("village-treasurer", "Village Treasurer",
               "Jacksonville Village Treasurer", 1,
               [charter227("section 3(a): a treasurer is elected "
                           "at the annual meeting; no official "
                           "source publishes the current holder, "
                           "so the post is created without a "
                           "membership. The electric board's "
                           "'Treasurer' annotation is a board "
                           "role and is not shown to be this "
                           "office")]),
        office("village-collector", "Village Collector",
               "Jacksonville Village Collector", 1,
               [charter227("section 3(a): a collector is "
                           "elected at the annual meeting; no "
                           "official source publishes the "
                           "current holder, so the post is "
                           "created without a membership")]),
    ]
    return spec("jacksonville", "Jacksonville", offices)


SPECS["jacksonville"] = jacksonville_spec()

# ------------------------------------------------------------ Jamaica
JAM_REPORT = {
    "url": "https://jamaicavermont.org/wp-content/uploads/2026/02/Town-Report-Fixed.pdf",
    "note": "PLACEHOLDER",
}
JAM_ORG = {
    "url": "https://www.jamaicavermont.org/wp-content/uploads/2026/03/Jamaica-Selectboard-Organizational-Meeting-Minutes-030926-1.pdf",
    "note": "PLACEHOLDER",
}


def jam_report(what):
    return S(JAM_REPORT, f"Town of Jamaica, 2026 Town Report "
             f"(official town website), town officers table: {what}")


def jamaica_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Jamaica Selectboard", 5,
               [charter123b("section 7: the selectboard has five "
                            "members (three elected for staggered "
                            "three-year terms and two for one-year "
                            "terms)"),
                jam_report("the officers table seats Jessica "
                           "Pollack (term to 2027), Greg "
                           "Meulemans (to 2028), and Kate Ullman; "
                           "Robert Brooks is listed 'Appointed "
                           "until March 2026' and Christina "
                           "Robinson's one-year term expired "
                           "March 2026"),
                S(JAM_ORG, "Town of Jamaica, Selectboard "
                           "organizational meeting minutes, "
                           "March 9, 2026: the board seated "
                           "after the 2026 town meeting is "
                           "Jessica Pollack (Chair), Greg "
                           "Meulemans, Kate Ullman, Robert "
                           "Brooks, and Jason Kass; Christina "
                           "Robinson is not seated. The "
                           "organizational minutes print "
                           "Pollack once as 'Pollock' and Kass "
                           "once as 'Kaas'; the town report and "
                           "the board's later minutes print "
                           "Pollack and Kass")],
               [holder("Jessica Pollack", "jessica-pollack"),
                holder("Greg Meulemans", "greg-meulemans"),
                holder("Kate Ullman", "kate-ullman"),
                holder("Robert Brooks", "robert-brooks"),
                holder("Jason Kass", "jason-kass")]),
        office("moderator", "Moderator", "Jamaica Moderator", 1,
               [charter123b("section 7: a moderator is elected "
                            "for a one-year term"),
                jam_report("the officers table seats Tom "
                           "Tolbert as Moderator; his "
                           "re-election at the March 2026 town "
                           "meeting was reported by Magic 967 "
                           "(WTSA) local news -- newspaper-class "
                           "evidence, disclosed on issue #163")],
               [holder("Tom Tolbert", "tom-tolbert")]),
        office("town-clerk", "Town Clerk", "Jamaica Town Clerk", 1,
               [charter123b("section 8: the selectboard appoints "
                            "the Town Clerk"),
                guide("lists Tom Tolbert as Jamaica's town "
                      "clerk"),
                clerk_xlsx("lists Tom Tolbert as Jamaica's town "
                           "clerk contact"),
                jam_report("the officers table lists Tom Tolbert "
                           "as 'Town Clerk/Town Admin'")],
               [holder("Tom Tolbert", "tom-tolbert",
                       how_seated="appointed")]),
        office("town-treasurer", "Town Treasurer",
               "Jamaica Town Treasurer", 1,
               [charter123b("section 8: the selectboard appoints "
                            "the Town Treasurer"),
                guide("lists Sara Wiswall as Jamaica's town "
                      "treasurer"),
                jam_report("the town offices page lists Sara "
                           "Wiswall as Treasurer")],
               [holder("Sara Wiswall", "sara-wiswall",
                       how_seated="appointed")]),
        office("lister", "Lister", "Jamaica Board of Listers", 3,
               [charter123b("section 7: three listers are "
                            "elected for staggered three-year "
                            "terms, one term ending each year"),
                jam_report("the officers table seats Karen "
                           "Ameden (term to 2028) and April "
                           "Green (to 2028); Patricia "
                           "Meulemans's term expired March 2026 "
                           "and no official source publishes "
                           "the 2026 outcome, so the third seat "
                           "is left unfilled")],
               [holder("Karen Ameden", "karen-ameden"),
                holder("April Green", "april-green")]),
        office("first-constable", "First Constable",
               "Jamaica First Constable", 1,
               [statute2646_structure("a first constable is "
                                      "elected; the 2026 town "
                                      "report seats Robert "
                                      "Willis with a term "
                                      "expiring March 2026 and "
                                      "the 2026 outcome is "
                                      "unpublished")]),
        office("second-constable", "Second Constable",
               "Jamaica Second Constable", 1,
               [statute2646_structure("a second constable is "
                                      "elected; the 2026 town "
                                      "report seats Ben Williams "
                                      "with a term expiring "
                                      "March 2026 and the 2026 "
                                      "outcome is unpublished")]),
        office("grand-juror", "Grand Juror", "Jamaica Grand Juror",
               1,
               [statute2646_structure("a grand juror is elected; "
                                      "the 2026 town report "
                                      "seats Robert Willis with "
                                      "a term expiring March "
                                      "2026 and the 2026 outcome "
                                      "is unpublished")]),
        office("town-agent", "Town Agent", "Jamaica Town Agent", 1,
               [statute2646_structure("a town agent is elected; "
                                      "the 2026 town report "
                                      "seats Peter Andrus with a "
                                      "term expiring March 2026 "
                                      "and the 2026 outcome is "
                                      "unpublished")]),
        office("trustee-of-public-funds", "Trustee of Public Funds",
               "Jamaica Trustees of Public Funds", 1,
               [jam_report("the officers table carries a single "
                           "Trustee of Public Funds seat "
                           "(Robert Willis, term expiring "
                           "March 2026); the 2026 outcome is "
                           "unpublished, so the post is created "
                           "without a membership")]),
        office("agent-to-deed-town-owned-property",
               "Agent to Deed Town-Owned Property",
               "Jamaica Agent to Deed Town-Owned Property", 1,
               [jam_report("the officers table seats an Agent "
                           "to Deed Land (Andy Coyne, term "
                           "expiring March 2026); the 2026 "
                           "outcome is unpublished, so the post "
                           "is created without a membership")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Jamaica Collector of Delinquent Taxes", 1,
               [charter123b("section 8: the selectboard appoints "
                            "the collector of delinquent taxes; "
                            "no official source publishes the "
                            "current appointee, so the post is "
                            "created without a membership")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Jamaica Justices of the Peace", 5,
               [jp_src("names five justices of the peace for "
                       "Jamaica: Karen Ameden, Greg Joly, Rob "
                       "Willis, Tom Tolbert, and Clara "
                       "Robinson")],
               [holder("Karen Ameden", "karen-ameden"),
                holder("Greg Joly", "greg-joly"),
                holder("Rob Willis", "rob-willis"),
                holder("Tom Tolbert", "tom-tolbert"),
                holder("Clara Robinson", "clara-robinson")]),
    ]
    jp = jp_election(
        "jamaica-vt", "Jamaica", 5,
        "names five winners for Jamaica: Karen Ameden, Greg "
        "Joly, Rob Willis, Tom Tolbert, and Clara Robinson. "
        "Clara Robinson the justice of the peace is not "
        "Christina Robinson, whose one-year selectboard term "
        "expired in March 2026")
    return spec("jamaica", "Jamaica", offices, jp)


SPECS["jamaica"] = jamaica_spec()

# ------------------------------------------------------------ Jay
JAY_MINUTES = {
    "url": "https://www.jayvt.com/vertical/sites/%7BD46CBAAF-C206-4678-BD37-4293256D9148%7D/uploads/MINUTES2026.docx",
    "note": "PLACEHOLDER",
}
JAY_BOOK = {
    "url": "https://www.jayvt.com/vertical/sites/%7BD46CBAAF-C206-4678-BD37-4293256D9148%7D/uploads/Combined_and_Numbered_Final_2025_Book.pdf",
    "note": "PLACEHOLDER",
}


def jay_minutes(what):
    return S(JAY_MINUTES, f"Town of Jay, minutes of the annual "
             f"town meeting, March 3, 2026 (official town "
             f"website): {what}")


def jay_spec():
    offices = [
        office("selectboard", "Selectboard Member", "Jay Selectboard",
               3,
               [sb_dir("lists Jay's three selectboard members as "
                       "Tara Morse, David Sanders, and Le-Ann "
                       "Tetrault (Chair)"),
                jay_minutes("Le-Ann Tetrault was re-elected to a "
                            "three-year selectboard term at the "
                            "2026 meeting; Morse and Sanders "
                            "hold over")],
               [holder("Tara Morse", "tara-morse"),
                holder("David Sanders", "david-sanders"),
                holder("Le-Ann Tetrault", "le-ann-tetrault")]),
        office("moderator", "Moderator", "Jay Moderator", 1,
               [jay_minutes("Janet Butler was re-elected "
                            "moderator for a one-year term at "
                            "the 2026 meeting, which she chaired")],
               [holder("Janet Butler", "janet-butler")]),
        office("town-clerk", "Town Clerk", "Jay Town Clerk", 1,
               [guide("lists Lynnette Deaette as Jay's town "
                      "clerk"),
                clerk_xlsx("lists Lynnette Deaette as Jay's town "
                           "clerk contact")],
               [holder("Lynnette Deaette", "lynnette-deaette")]),
        office("town-treasurer", "Town Treasurer",
               "Jay Town Treasurer", 1,
               [guide("lists Lynnette Deaette as Jay's town "
                      "treasurer"),
                treas_xlsx("lists Lynnette Deaette as Jay's town "
                           "treasurer contact")],
               [holder("Lynnette Deaette", "lynnette-deaette")]),
        office("constable", "Constable", "Jay Constable", 1,
               [S(JAY_BOOK, "Town of Jay, 2025 Book (official "
                            "town website), Warning for the "
                            "March 3, 2026 annual meeting, "
                            "Article 3: the meeting elects "
                            "'all necessary town officials "
                            "required by law,' specifying only "
                            "a selectboard member (three years) "
                            "and a constable (one year)"),
                jay_minutes("Dorran Dougherty was elected "
                            "constable for a one-year term at "
                            "the 2026 meeting. The warning and "
                            "minutes are Jay's comprehensive "
                            "elective list for 2026: no lister "
                            "(the town employs a hired "
                            "assessor), auditor, grand juror, "
                            "town agent, or collector of "
                            "delinquent taxes was elected, so "
                            "no posts are created for those "
                            "offices")],
               [holder("Dorran Dougherty", "dorran-dougherty")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Jay Justices of the Peace", 5,
               [jp_src("names five justices of the peace for "
                       "Jay: Arnold Cota Jr, Hailey Morse, "
                       "Elizabeth Sargent, Benjamin Zev, and "
                       "Le-Ann Tetrault")],
               [holder("Arnold Cota Jr", "arnold-cota-jr"),
                holder("Hailey Morse", "hailey-morse"),
                holder("Elizabeth Sargent", "elizabeth-sargent"),
                holder("Benjamin Zev", "benjamin-zev"),
                holder("Le-Ann Tetrault", "le-ann-tetrault")]),
    ]
    jp = jp_election(
        "jay-vt", "Jay", 5,
        "names five winners for Jay: Arnold Cota Jr, Hailey "
        "Morse, Elizabeth Sargent, Benjamin Zev, and Le-Ann "
        "Tetrault")
    return spec("jay", "Jay", offices, jp)


SPECS["jay"] = jay_spec()

# ------------------------------------------------------------ Jeffersonville
JEFF_MIN_MAY = {
    "url": "https://www.jeffvillagevt.com/s/May112026.pdf",
    "note": "PLACEHOLDER",
}
JEFF_MIN_APR = {
    "url": "https://www.jeffvillagevt.com/s/April132026.pdf",
    "note": "PLACEHOLDER",
}
JEFF_MIN_FEB = {
    "url": "https://www.jeffvillagevt.com/s/February092026.pdf",
    "note": "PLACEHOLDER",
}
JEFF_BYLAWS = {
    "url": "https://www.jeffvillagevt.com/s/By-laws3-1-2004-OCR.pdf",
    "note": "PLACEHOLDER",
}


def jeff_bylaws(phrase):
    return S(JEFF_BYLAWS, f"Village of Jeffersonville, By-Laws "
             f"(2004; official village website): {phrase}")


def jeffersonville_spec():
    offices = [
        office("village-trustee", "Village Trustee",
               "Jeffersonville Board of Trustees", 5,
               [jeff_bylaws("Article 3: the annual meeting "
                            "elects the number of trustees "
                            "needed to maintain a total of five "
                            "trustees, for three-year terms"),
                S(JEFF_MIN_FEB, "Village of Jeffersonville, "
                                "trustee meeting minutes, "
                                "February 9, 2026: James "
                                "Sergeant, Fred Bauer, Nathan "
                                "Mascolino, Donald Lange, and "
                                "Tom Wyckoff sit as trustees"),
                S(JEFF_MIN_APR, "Village of Jeffersonville, "
                                "trustee meeting minutes, "
                                "April 13, 2026: the same board "
                                "sits (Lange absent) and signs "
                                "the annual meeting warning"),
                S(JEFF_MIN_MAY, "Village of Jeffersonville, "
                                "trustee meeting minutes, May "
                                "11, 2026, the first meeting "
                                "after the annual meeting: all "
                                "five trustees sit -- Sergeant, "
                                "Bauer, Mascolino, Lange, and "
                                "Wyckoff")],
               [holder("James Sergeant", "james-sergeant"),
                holder("Fred Bauer", "fred-bauer"),
                holder("Nathan Mascolino", "nathan-mascolino"),
                holder("Donald Lange", "donald-lange"),
                holder("Tom Wyckoff", "tom-wyckoff")]),
        office("moderator", "Moderator",
               "Jeffersonville Moderator", 1,
               [jeff_bylaws("Article 3: the annual meeting "
                            "elects a moderator; no official "
                            "source publishes the current "
                            "holder, so the post is created "
                            "without a membership")]),
        office("village-clerk", "Village Clerk",
               "Jeffersonville Village Clerk", 1,
               [jeff_bylaws("Article 3: the annual meeting "
                            "elects a combined Clerk/Treasurer; "
                            "the two offices are modeled as "
                            "two posts on the Hardwick "
                            "combined-office pattern. No "
                            "official source publishes the "
                            "current holder, so the post is "
                            "created without a membership")]),
        office("village-treasurer", "Village Treasurer",
               "Jeffersonville Village Treasurer", 1,
               [jeff_bylaws("Article 3: the annual meeting "
                            "elects a combined Clerk/Treasurer; "
                            "the two offices are modeled as "
                            "two posts on the Hardwick "
                            "combined-office pattern. No "
                            "official source publishes the "
                            "current holder, so the post is "
                            "created without a membership")]),
    ]
    return spec("jeffersonville", "Jeffersonville", offices)


SPECS["jeffersonville"] = jeffersonville_spec()

# ------------------------------------------------------------ Johnson (town)
JT_CERT = {
    "url": "https://storage.googleapis.com/juniper-media-library/237/2026/03/Town%20Meeting%20Results.pdf",
    "note": "PLACEHOLDER",
}
JT_REPORT = {
    "url": "https://storage.googleapis.com/juniper-media-library/237/2026/02/Town%20Report%202025.pdf",
    "note": "PLACEHOLDER",
}
JT_DIR = {
    "url": "https://townofjohnson.com/municipal-directory",
    "note": "PLACEHOLDER",
}
JT_CLERK = {
    "url": "https://townofjohnson.com/departments/town-clerk",
    "note": "PLACEHOLDER",
}
JT_LIB = {
    "url": "https://townofjohnson.com/library-board-of-trustees",
    "note": "PLACEHOLDER",
}


def jt_cert(what):
    return S(JT_CERT, f"Town of Johnson, Certificate of Votes for "
             f"Town and LNMUU District Officers, annual town "
             f"meeting, March 3, 2026 (official town website): "
             f"{what}")


def jt_report(what):
    return S(JT_REPORT, f"Town of Johnson, 2025 Town Report "
             f"(official town website), 'Town Officers - 2025' "
             f"table: {what}")


def johnson_town_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Johnson Selectboard", 5,
               [sb_dir("lists Johnson's five selectboard members "
                       "as Michael Dunham, Peter Hammond, "
                       "Adrienne Parker, Eben Patch, and Paul "
                       "Warden (Chair)"),
                jt_cert("Michael Dunham (three-year term, 187 "
                        "votes), Paul Warden (two-year term, "
                        "216), and Eben Patch (one-year term, "
                        "215) were elected at the March 3, 2026 "
                        "meeting; Hammond and Parker hold over"),
                jt_report("the pre-meeting board was Patch, "
                          "Dunham, Hammond, Parker, and Duncan "
                          "Hastings (resigned) with Warden "
                          "sitting as an appointee; the 2026 "
                          "election seated the five members "
                          "above")],
               [holder("Michael Dunham", "michael-dunham"),
                holder("Peter Hammond", "peter-hammond"),
                holder("Adrienne Parker", "adrienne-parker"),
                holder("Eben Patch", "eben-patch"),
                holder("Paul Warden", "paul-warden")]),
        office("moderator", "Moderator", "Johnson Moderator", 1,
               [jt_cert("Beth Foy was elected Town Moderator "
                        "for a one-year term at the March 3, "
                        "2026 meeting (23 votes, from the "
                        "floor); David Williams held the office "
                        "in 2025 per the town report")],
               [holder("Beth Foy", "beth-foy")]),
        office("town-clerk", "Town Clerk", "Johnson Town Clerk", 1,
               [S(JT_CLERK, "Town of Johnson (official website), "
                            "Town Clerk page: 'The Town Clerk "
                            "is appointed by the Selectboard,' "
                            "and the page names Susan Tinker as "
                            "Town Clerk/Assistant Treasurer"),
                S(JT_DIR, "Town of Johnson, Municipal Directory: "
                          "'Town Clerk's Office -- Susan "
                          "Tinker, Town Clerk/Assistant "
                          "Treasurer'"),
                clerk_xlsx("lists Susan Tinker as Johnson's "
                           "town clerk contact. The January "
                           "2026 Guide still lists Rosemary "
                           "Audibert, who attested the March 4, "
                           "2026 certificate of votes as Town "
                           "Clerk; Tinker succeeded her in "
                           "spring 2026")],
               [holder("Susan Tinker", "susan-tinker",
                       how_seated="appointed")]),
        office("town-treasurer", "Town Treasurer",
               "Johnson Town Treasurer", 1,
               [S(JT_DIR, "Town of Johnson, Municipal Directory: "
                          "Lydia Beach Putvain is 'Treasurer/"
                          "Assistant Town Clerk'"),
                treas_xlsx("lists Lydia Beach Putvain as "
                           "Johnson's town treasurer contact. "
                           "The January 2026 Guide still lists "
                           "Rosemary Audibert for both clerk "
                           "and treasurer; she held both "
                           "offices until spring 2026")],
               [holder("Lydia Beach Putvain",
                       "lydia-beach-putvain")]),
        office("library-trustee", "Library Trustee",
               "Johnson Library Trustees", 5,
               [S(JT_LIB, "Town of Johnson (official website), "
                          "Library Board of Trustees page: the "
                          "board is Kelly Vandorn (Chair), "
                          "Jasmine Yuris (Vice-chair), Eric "
                          "Schulz, Suzanne Dodge, and Trista "
                          "Tallman"),
                jt_cert("Trista Tallman (five-year term, 213 "
                        "votes) and Eric Schulz (three-year "
                        "term, 225) were elected library "
                        "trustees at the March 3, 2026 "
                        "meeting"),
                jt_report("the pre-meeting board was Sabrina "
                          "Rossi (term expired March 2026), "
                          "Vandorn, Yuris, Schulz, and Dodge "
                          "on staggered five-year terms")],
               [holder("Kelly Vandorn", "kelly-vandorn"),
                holder("Jasmine Yuris", "jasmine-yuris"),
                holder("Eric Schulz", "eric-schulz"),
                holder("Suzanne Dodge", "suzanne-dodge"),
                holder("Trista Tallman", "trista-tallman")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Johnson Collector of Delinquent Taxes", 1,
               [jt_cert("the delinquent tax collector contest "
                        "at the March 3, 2026 meeting returned "
                        "'NO WINNER,' and Article 7 of the "
                        "warning was adopted: 'Voted to have "
                        "the Selectboard appoint a collector "
                        "of delinquent taxes.' The appointee "
                        "is not published, so the post is "
                        "created without a membership"),
                jt_report("Rosemary Audibert held the elected "
                          "office ('Tax Collector') to March "
                          "2026")]),
        office("trustee-of-public-funds", "Trustee of Public Money",
               "Johnson Trustees of Public Funds", 1,
               [jt_report("the officers table seats a single "
                          "'Trustee of Public Money,' Rosemary "
                          "Audibert; she left town office in "
                          "spring 2026 and no official source "
                          "publishes a successor, so the post "
                          "is created without a membership")]),
        office("first-constable", "First Constable",
               "Johnson First Constable", 1,
               [jt_report("the APPOINTMENTS section of the "
                          "officers table names Dean Locke as "
                          "First Constable, an appointment of "
                          "the selectboard")],
               [holder("Dean Locke", "dean-locke",
                       how_seated="appointed")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Johnson Justices of the Peace", 12,
               [jp_src("names twelve justices of the peace for "
                       "Johnson: Jennifer Burton, Michael "
                       "Dunham, Jan Gearhart, Bari Gladstone, "
                       "Martha Leonard, Randy Manning, Kyle "
                       "Nuse, Eric Osgood, Shayne Spence, "
                       "Margaret Warden, Jasmine Yuris, and "
                       "Molly Zapp. The 2025 town report's "
                       "Board of Civil Authority roster for "
                       "the same term shares only seven of "
                       "these names (and adds five others); "
                       "the certified Secretary of State "
                       "listing governs the slate, and the "
                       "divergence is flagged on issue #163"),
                jt_report("the Board of Civil Authority roster "
                          "(term February 1, 2025 to January "
                          "31, 2027) names Janice Gearhart, "
                          "Bari Gladstone, Margo Warden, "
                          "Cynthia Hennard, Diane Lehouiller, "
                          "Eric Osgood, Martha Leonard, Gary "
                          "Underwood, Kyle Nuse, Jasmine "
                          "Yuris, Helen McElroy, and Gregory "
                          "Hill; Michael Dunham sits on the "
                          "board ex officio as a selectboard "
                          "member")],
               [holder("Jennifer Burton", "jennifer-burton"),
                holder("Michael Dunham", "michael-dunham"),
                holder("Jan Gearhart", "jan-gearhart",
                       ballot_name="Jan Gearhart"),
                holder("Bari Gladstone", "bari-gladstone"),
                holder("Martha Leonard", "martha-leonard"),
                holder("Randy Manning", "randy-manning"),
                holder("Kyle Nuse", "kyle-nuse"),
                holder("Eric Osgood", "eric-osgood"),
                holder("Shayne Spence", "shayne-spence"),
                holder("Margaret Warden", "margaret-warden"),
                holder("Jasmine Yuris", "jasmine-yuris"),
                holder("Molly Zapp", "molly-zapp")]),
    ]
    jp = jp_election(
        "johnson-37075-vt", "Johnson", 12,
        "names twelve winners for Johnson: Jennifer Burton, "
        "Michael Dunham, Jan Gearhart, Bari Gladstone, Martha "
        "Leonard, Randy Manning, Kyle Nuse, Eric Osgood, "
        "Shayne Spence, Margaret Warden, Jasmine Yuris, and "
        "Molly Zapp. Jennifer Burton of Johnson is a different "
        "person from Jennifer Burton of Jericho, who was also "
        "elected a justice of the peace in 2024; the office is "
        "town-bound")
    return spec("johnson-37075", "Johnson", offices, jp)


SPECS["johnson-37075"] = johnson_town_spec()

# ------------------------------------------------------------ Johnson Village
JV_ANNUAL26 = {
    "url": "https://villageofjohnson.com/wp-content/uploads/2026/04/Annual-Village-Meeting-4-7-26.pdf",
    "note": "PLACEHOLDER",
}
JV_MINUTES_PAGE = {
    "url": "https://villageofjohnson.com/minutes-agendas/",
    "note": "PLACEHOLDER",
}
JV_REPORT24 = {
    "url": "https://villageofjohnson.com/wp-content/uploads/2025/03/villagereport2024.pdf",
    "note": "PLACEHOLDER",
}
JV_STAFF = {
    "url": "https://villageofjohnson.com/village-staff/",
    "note": "PLACEHOLDER",
}


def johnson_village_spec():
    offices = [
        office("village-trustee", "Village Trustee",
               "Johnson Village Board of Trustees", 5,
               [S(JV_ANNUAL26, "Village of Johnson, minutes of "
                               "the annual village meeting, "
                               "April 7, 2026: Will Jennison "
                               "was elected trustee for a "
                               "three-year term and BJ Putvain "
                               "for a two-year term; the "
                               "meeting seated trustees Ellis "
                               "O'Hear, Ken Tourangeau, and "
                               "Darrell Wescom as well"),
                S(JV_MINUTES_PAGE, "Village of Johnson "
                                   "(official website), "
                                   "Minutes & Agendas page: "
                                   "the Board of Trustees "
                                   "minutes of September 14, "
                                   "2026 seat the same five "
                                   "trustees -- O'Hear, "
                                   "Jennison, Putvain, "
                                   "Tourangeau, and Wescom. "
                                   "Steven Hatfield, carried "
                                   "in some directories, "
                                   "retired at the April 1, "
                                   "2025 annual meeting")],
               [holder("Ellis O'Hear", "ellis-ohear"),
                holder("Will Jennison", "will-jennison"),
                holder("BJ Putvain", "bj-putvain"),
                holder("Ken Tourangeau", "ken-tourangeau"),
                holder("Darrell Wescom", "darrell-wescom")]),
        office("village-president", "Village President",
               "Johnson Village President", 1,
               [S(JV_ANNUAL26, "Village of Johnson, minutes of "
                               "the annual village meeting, "
                               "April 7, 2026: Eric Osgood was "
                               "re-elected Village President "
                               "for a one-year term (Australian "
                               "ballot, uncontested)")],
               [holder("Eric Osgood", "eric-osgood",
                       person_scope="johnson-37075")]),
        office("village-clerk", "Village Clerk",
               "Johnson Village Clerk", 1,
               [S(JV_STAFF, "Village of Johnson (official "
                            "website), Village Staff page: "
                            "Rosemary Audibert is 'Clerk / "
                            "Treasurer ... Clerk and Treasurer: "
                            "1993 - present'"),
                S(JV_REPORT24, "Village of Johnson, 2024 "
                               "Village Report, officers page: "
                               "the Village Clerk is listed "
                               "under APPOINTMENTS (Assistant "
                               "Clerk & Treasurer: Susan "
                               "Tinker)")],
               [holder("Rosemary Audibert", "rosemary-audibert",
                       how_seated="appointed")]),
        office("village-treasurer", "Village Treasurer",
               "Johnson Village Treasurer", 1,
               [S(JV_STAFF, "Village of Johnson (official "
                            "website), Village Staff page: "
                            "Rosemary Audibert is 'Clerk / "
                            "Treasurer ... Clerk and Treasurer: "
                            "1993 - present'"),
                S(JV_REPORT24, "Village of Johnson, 2024 "
                               "Village Report, officers page: "
                               "the Village Treasurer is "
                               "listed under APPOINTMENTS")],
               [holder("Rosemary Audibert", "rosemary-audibert",
                       how_seated="appointed")]),
        office("auditor", "Village Auditor",
               "Johnson Village Auditors", 3,
               [S(JV_REPORT24, "Village of Johnson, 2024 "
                               "Village Report, officers page: "
                               "the village elects three "
                               "auditors (one named holder, "
                               "Bobbie Moulton to April 2025, "
                               "and two seats already vacant); "
                               "the April 7, 2026 annual "
                               "meeting minutes record that "
                               "'no one was elected to the "
                               "other positions,' so the post "
                               "is created without "
                               "memberships")]),
        office("tax-collector", "Tax Collector",
               "Johnson Village Tax Collector", 1,
               [S(JV_REPORT24, "Village of Johnson, 2024 "
                               "Village Report, officers page: "
                               "a Tax Collector office is "
                               "carried (last named holder "
                               "Rosemary Audibert, term shown "
                               "expired April 2024); no "
                               "current holder is published, "
                               "so the post is created "
                               "without a membership")]),
    ]
    return spec("johnson", "Johnson Village", offices)


SPECS["johnson"] = johnson_village_spec()

# ------------------------------------------------------------ Killington
KILL_PAGE = {
    "url": "https://www.killingtontown.com/elected-officials",
    "note": "PLACEHOLDER",
}


def kill_page(what):
    return S(KILL_PAGE, f"Town of Killington (official website), "
             f"'Elected Officials' page (page updated August "
             f"12, 2026): {what}")


def killington_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Killington Selectboard", 5,
               [kill_page("the Select Board is Jim Haff "
                          "(Chair, term to 2027), Bill Vines "
                          "(2027), Vito Rasenas (2028), Jon T. "
                          "Wysocki (Vice Chair, 2028), and "
                          "Celia Clancy (2029). The Secretary "
                          "of State's June 2026 directory names "
                          "Ricky Bowen instead of Clancy and "
                          "is stale for Killington; the town's "
                          "own page governs")],
               [holder("Jim Haff", "jim-haff"),
                holder("Bill Vines", "bill-vines"),
                holder("Vito Rasenas", "vito-rasenas"),
                holder("Jon Wysocki", "jon-wysocki",
                       ballot_name="Jon T. Wysocki"),
                holder("Celia Clancy", "celia-clancy")]),
        office("moderator", "Moderator", "Killington Moderator", 1,
               [kill_page("Charles 'Chuck' Hughes is Moderator "
                          "(term to 2027)")],
               [holder("Charles Hughes", "charles-hughes")]),
        office("town-clerk", "Town Clerk",
               "Killington Town Clerk", 1,
               [kill_page("Margaret (Peggy) L. Neisner is Town "
                          "Clerk (term to 2029)"),
                guide("lists Margaret Neisner as Killington's "
                      "town clerk"),
                clerk_xlsx("lists Margaret Neisner as "
                           "Killington's town clerk contact")],
               [holder("Margaret Neisner", "margaret-neisner")]),
        office("town-treasurer", "Town Treasurer",
               "Killington Town Treasurer", 1,
               [kill_page("Monika Legayada is Town Treasurer "
                          "(term to 2028)"),
                guide("lists Monika Legayada as Killington's "
                      "town treasurer"),
                treas_xlsx("lists Monika Legayada as "
                           "Killington's town treasurer "
                           "contact")],
               [holder("Monika Legayada", "monika-legayada")]),
        office("lister", "Lister", "Killington Board of Listers",
               3,
               [kill_page("the Listers are Merisa J. Sherman "
                          "(term to 2027), Walter J. Findeisen "
                          "(2028), and Krista Mosher (2029)")],
               [holder("Merisa Sherman", "merisa-sherman"),
                holder("Walter Findeisen", "walter-findeisen"),
                holder("Krista Mosher", "krista-mosher")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Killington Cemetery Commission", 3,
               [kill_page("the Cemetery Commissioners are "
                          "Ronald J. Kish, Sr. (term to 2027), "
                          "Connie Barbash (2028), and Truman "
                          "Bates (2029)")],
               [holder("Ronald Kish", "ronald-kish"),
                holder("Constance Barbash", "constance-barbash"),
                holder("Truman Bates", "truman-bates")]),
        office("library-trustee", "Library Trustee",
               "Killington Library Trustees", 5,
               [kill_page("the Sherburne Memorial Library "
                          "Trustees are Nan Salamon (term to "
                          "2027), Beth Weinberg Sarandrea "
                          "(2028), Laura Djordjalian-McComb "
                          "(2029), Nancy Sherman (2030), and "
                          "Gerrie Russell (2031) -- five "
                          "staggered seats, one expiring each "
                          "year")],
               [holder("Nan Salamon", "nan-salamon"),
                holder("Beth Weinberg Sarandrea",
                       "beth-weinberg-sarandrea"),
                holder("Laura Djordjalian-McComb",
                       "laura-djordjalian-mccomb"),
                holder("Nancy Sherman", "nancy-sherman"),
                holder("Gerrie Russell", "gerrie-russell")]),
        office("trustee-of-public-funds", "Trustee of Public Funds",
               "Killington Trustees of Public Funds", 3,
               [kill_page("the Trustees of Public Funds block "
                          "lists all three seats 'Vacant' "
                          "(terms to 2025, 2026, and 2027), so "
                          "the post is created without "
                          "memberships")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Killington Justices of the Peace", 1,
               [jp_src("names one justice of the peace for "
                       "Killington: Patrick Cushing. The town "
                       "website's 'Elected Officials' page "
                       "carries a seven-name justice block "
                       "dated 2026 that omits Cushing; that "
                       "block is a pre-November-2024 "
                       "carryover and the certified listing "
                       "governs (flagged on issue #163)"),
                kill_page("the page's Justice of the Peace "
                          "block names Constance 'Connie' A. "
                          "Barbash, Paul DiMascio, Chuck "
                          "Hughes, Chris Karr, Margaret "
                          "'Peggy' Neisner, Judy Storch, and "
                          "Nancy J. Sherman, each dated 2026 "
                          "-- not used for the slate, for the "
                          "reason stated in the listing note")],
               [holder("Patrick Cushing", "patrick-cushing")]),
    ]
    jp = jp_election(
        "killington-vt", "Killington", 1,
        "names one winner for Killington: Patrick Cushing")
    return spec("killington", "Killington", offices, jp)


SPECS["killington"] = killington_spec()

# ------------------------------------------------------------ Kirby
KIRBY_GOV = {
    "url": "https://www.kirbyvt.gov/government",
    "note": "PLACEHOLDER",
}
KIRBY_REPORT = {
    "url": "https://irp.cdn-website.com/47bd5126/files/uploaded/2025townreport.pdf",
    "note": "PLACEHOLDER",
}


def kirby_gov(what):
    return S(KIRBY_GOV, f"Town of Kirby (official website), "
             f"Government page: {what}")


def kirby_report(what):
    return S(KIRBY_REPORT, f"Town of Kirby, 2025 Town Report "
             f"(official town website): {what}")


def kirby_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Kirby Selectboard", 3,
               [sb_dir("lists Kirby's three selectboard members "
                       "as Michael Bickford, Jeffrey Hayes, and "
                       "Keith Isham (Chair)"),
                kirby_gov("the Selectboard is Keith Isham "
                          "(Chair, term to 2027), Michael "
                          "Bickford (2029), and Jeffrey Hayes "
                          "(2028)")],
               [holder("Keith Isham", "keith-isham"),
                holder("Jeffrey Hayes", "jeffrey-hayes"),
                holder("Michael Bickford", "michael-bickford")]),
        office("road-commissioner", "Road Commissioner",
               "Kirby Road Commissioner", 1,
               [kirby_gov("Michael Bickford is styled "
                          "'(Road Commissioner, 2029)' on the "
                          "Selectboard listing"),
                kirby_report("'Town Officials' table: a "
                             "separate Road Commissioner row "
                             "names Michael Bickford")],
               [holder("Michael Bickford", "michael-bickford")]),
        office("moderator", "Moderator", "Kirby Moderator", 1,
               [kirby_report("'Town Officials' table: John "
                             "McClaughry is Moderator. His "
                             "re-election at the March 3, 2026 "
                             "meeting -- his 60th consecutive "
                             "year in the office -- was "
                             "reported by VTDigger's town "
                             "meeting results coverage and "
                             "WCAX (newspaper-class evidence, "
                             "disclosed on issue #163)")],
               [holder("John McClaughry", "john-mcclaughry")]),
        office("town-clerk", "Town Clerk", "Kirby Town Clerk", 1,
               [kirby_gov("Erin Patoine is Town Clerk/Treasurer "
                          "(term to 2027)"),
                guide("lists Erin Patoine as Kirby's town "
                      "clerk"),
                clerk_xlsx("lists Erin Patoine as Kirby's town "
                           "clerk contact")],
               [holder("Erin Patoine", "erin-patoine")]),
        office("town-treasurer", "Town Treasurer",
               "Kirby Town Treasurer", 1,
               [kirby_gov("Erin Patoine is Town Clerk/Treasurer "
                          "(term to 2027)"),
                guide("lists Erin Patoine as Kirby's town "
                      "treasurer"),
                treas_xlsx("lists Erin Patoine as Kirby's town "
                           "treasurer contact")],
               [holder("Erin Patoine", "erin-patoine")]),
        office("lister", "Lister", "Kirby Board of Listers", 3,
               [kirby_gov("the Listers are Marla Waring, Merle "
                          "Thompson, and Mike Wood, each shown "
                          "to 2028"),
                kirby_report("'Town Officials' table: Listers "
                             "Michael Wood, Marla Waring, and "
                             "Merle Thompson, each to 2028")],
               [holder("Marla Waring", "marla-waring"),
                holder("Merle Thompson", "merle-thompson"),
                holder("Michael Wood", "michael-wood")]),
        office("auditor", "Auditor", "Kirby Town Auditors", 3,
               [kirby_report("'Town Officials' table: Auditors "
                             "Emily Hartsock (term to 2027), "
                             "Leslie Peters (to 2028), and "
                             "Cheryl McMahon (to 2026). The "
                             "Warning for the March 3, 2026 "
                             "meeting (Article 4) stood a "
                             "three-year auditor seat; no "
                             "official source publishes the "
                             "2026 outcome, so McMahon's seat "
                             "is left unfilled")],
               [holder("Emily Hartsock", "emily-hartsock"),
                holder("Leslie Peters", "leslie-peters")]),
        office("collector-of-delinquent-taxes",
               "Delinquent Tax Collector",
               "Kirby Collector of Delinquent Taxes", 1,
               [kirby_report("the Warning for the March 3, 2026 "
                             "meeting (Article 4) elects a "
                             "Delinquent Tax Collector; the "
                             "'Town Officials' table's 'Tax "
                             "Collector' (Erin Patoine) held a "
                             "term expiring 2026 and the 2026 "
                             "outcome is unpublished, so the "
                             "post is created without a "
                             "membership")]),
        office("agent-to-deed-town-owned-property",
               "Agent to Convey Town Real Estate",
               "Kirby Agent to Convey Town Real Estate", 1,
               [kirby_report("the Warning for the March 3, 2026 "
                             "meeting (Article 4) elects an "
                             "Agent to Convey Town Real Estate; "
                             "the 'Town Officials' table "
                             "records the office held by the "
                             "Selectboard collectively in "
                             "2025, so the post is created "
                             "without a membership")]),
        office("trustee-of-cemetery-funds",
               "Trustee of Cemetery Funds",
               "Kirby Trustee of Cemetery Funds", 1,
               [kirby_report("the Warning for the March 3, 2026 "
                             "meeting (Article 4) elects a "
                             "Trustee of Cemetery Funds; the "
                             "'Town Officials' table names "
                             "Erin Patoine with a term "
                             "expiring 2026 and the 2026 "
                             "outcome is unpublished, so the "
                             "post is created without a "
                             "membership")]),
        office("cemetery-sexton", "Cemetery Sexton",
               "Kirby Cemetery Sexton", 1,
               [kirby_report("the Warning for the March 3, 2026 "
                             "meeting (Article 4) elects a "
                             "Sexton; the 'Town Officials' "
                             "table records the office held by "
                             "the Selectboard collectively in "
                             "2025, so the post is created "
                             "without a membership")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Kirby Justices of the Peace", 5,
               [jp_src("names five justices of the peace for "
                       "Kirby: Timothy Peters, Flower Toomey, "
                       "Tracy Sherbrook, Karen Moore, and Anne "
                       "McClaughry"),
                kirby_gov("the 'Justices of the Peace' block "
                          "names the same five: Karen Moore, "
                          "Timothy Peters, Tracy Sherbrook, "
                          "Anne McClaughry, and Flower Toomey. "
                          "Anne McClaughry is a different "
                          "person from Moderator John "
                          "McClaughry; no relationship is "
                          "asserted")],
               [holder("Timothy Peters", "timothy-peters"),
                holder("Flower Toomey", "flower-toomey"),
                holder("Tracy Sherbrook", "tracy-sherbrook"),
                holder("Karen Moore", "karen-moore"),
                holder("Anne McClaughry", "anne-mcclaughry")]),
    ]
    jp = jp_election(
        "kirby-vt", "Kirby", 5,
        "names five winners for Kirby: Timothy Peters, "
        "Flower Toomey, Tracy Sherbrook, Karen Moore, and "
        "Anne McClaughry")
    return spec("kirby", "Kirby", offices, jp)


SPECS["kirby"] = kirby_spec()

# ------------------------------------------------------------ Jericho (town)
JER_RESULTS = {
    "url": "https://www.jerichovt.gov/DocumentCenter/View/1321/2026-03-03-Jericho-Election-Results",
    "note": "PLACEHOLDER",
}
JER_REPORT = {
    "url": "https://www.jerichovt.gov/DocumentCenter/View/1295/2024-25-Jericho-Town-Report-PDF",
    "note": "PLACEHOLDER",
}
JER_CEM = {
    "url": "https://www.jerichovt.gov/208/Cemetery-Commission",
    "note": "PLACEHOLDER",
}
JER_LIST = {
    "url": "https://www.jerichovt.gov/255/Lister-and-Assessor",
    "note": "PLACEHOLDER",
}


def jer_results(what):
    return S(JER_RESULTS, f"Town of Jericho, official "
             f"election-night results, annual town meeting, "
             f"March 3, 2026 (official town website): {what}")


def jer_report(what):
    return S(JER_REPORT, f"Town of Jericho, 2024-25 Town "
             f"Report (official town website), 'Elected/"
             f"Appointed Town Officials' pages: {what}")


def jericho_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Jericho Selectboard", 5,
               [charter124("section 3 and section 4: "
                           "selectboard members are elected "
                           "by Australian ballot; the board "
                           "has five members"),
                jer_report("the pre-meeting board was Peter "
                           "Booth (term to 2028), Catherine "
                           "McMains (2026), Erik Johnson "
                           "(2027), Amy Kapitan (interim, "
                           "2026), and Laura Crain (interim, "
                           "2026)"),
                jer_results("Amy Kapitan was elected to a "
                            "three-year term (903 votes), "
                            "Laura Crain to a two-year term "
                            "(911), and Chris Brown to a "
                            "one-year term (610, defeating "
                            "Joseph Flynn, 485). The seated "
                            "board is Booth, Johnson, "
                            "Kapitan, Crain, and Brown; "
                            "McMains is no longer a member. "
                            "Kapitan and Crain sat as interim "
                            "appointees before the 2026 "
                            "meeting and were then elected. "
                            "Jericho's Chris Brown is not "
                            "Chris Brown of Rutland-3, the "
                            "former state representative")],
               [holder("Peter Booth", "peter-booth"),
                holder("Erik Johnson", "erik-johnson"),
                holder("Amy Kapitan", "amy-kapitan"),
                holder("Laura Crain", "laura-crain"),
                holder("Chris Brown", "chris-brown")]),
        office("moderator", "Moderator", "Jericho Moderator", 1,
               [jer_results("David Barrington was re-elected "
                            "Moderator for a one-year term "
                            "(1,026 votes)"),
                jer_report("David Barrington is Town "
                           "Moderator")],
               [holder("David Barrington", "david-barrington")]),
        office("town-clerk", "Town Clerk", "Jericho Town Clerk",
               1,
               [jer_results("Jessica R. Alexander was "
                            "re-elected Town Clerk for a "
                            "one-year term (1,115 votes)"),
                guide("lists Jessica Alexander as Jericho's "
                      "town clerk"),
                clerk_xlsx("lists Jessica Alexander as "
                           "Jericho's town clerk contact")],
               [holder("Jessica Alexander", "jessica-alexander",
                       ballot_name="Jessica R. Alexander")]),
        office("town-treasurer", "Town Treasurer",
               "Jericho Town Treasurer", 1,
               [charter124("section 5: the selectboard "
                           "appoints the Town Treasurer"),
                guide("lists Brian Stevens as Jericho's town "
                      "treasurer. The Secretary of State's "
                      "treasurer spreadsheet carries no "
                      "Jericho data and no town source "
                      "publishes a different holder")],
               [holder("Brian Stevens", "brian-stevens",
                       how_seated="appointed")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Jericho Collector of Delinquent Taxes", 1,
               [charter124("section 5: the selectboard "
                           "appoints the collector of "
                           "delinquent taxes"),
                jer_report("the appointed town officers table "
                           "names Amy Morse as Delinquent Tax "
                           "Collector")],
               [holder("Amy Morse", "amy-morse",
                       how_seated="appointed")]),
        office("lister", "Lister", "Jericho Board of Listers", 3,
               [charter124("section 5: the selectboard "
                           "appoints three listers"),
                S(JER_LIST, "Town of Jericho (official "
                            "website), Lister and Assessor "
                            "page: the page's contact block "
                            "names Lori Dykema, Martha "
                            "Prince, and Nathan Zwynenburg, "
                            "each styled 'Lister'")],
               [holder("Lori Dykema", "lori-dykema",
                       how_seated="appointed"),
                holder("Martha Prince", "martha-prince",
                       how_seated="appointed"),
                holder("Nathan Zwynenburg", "nathan-zwynenburg",
                       how_seated="appointed")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Jericho Cemetery Commission", 3,
               [S(JER_CEM, "Town of Jericho (official "
                           "website), Cemetery Commission "
                           "page: the page's members list "
                           "names Isabella Martin (term "
                           "expires 2027), Jim Adams (2028), "
                           "and Terry Hook (2029); it also "
                           "still carries Robert Grandchamp "
                           "(term expires 2026), whose seat "
                           "was the three-year seat filled "
                           "at the 2026 meeting"),
                jer_results("Terence B. Hook was elected to "
                            "a three-year cemetery "
                            "commissioner term (1,005 "
                            "votes), succeeding Grandchamp. "
                            "The two-year seat (an unexpired "
                            "term expiring 2028) drew no "
                            "ballot candidate and only "
                            "scattered write-ins, led by Jim "
                            "Adams; the town's commission "
                            "page seats Adams for that term, "
                            "so the write-in leader holds "
                            "the seat on the roster's "
                            "concurrence")],
               [holder("Jim Adams", "jim-adams"),
                holder("Isabella Martin", "isabella-martin"),
                holder("Terence Hook", "terence-hook",
                       ballot_name="Terence B. Hook")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Jericho Justices of the Peace", 12,
               [jp_src("names twelve justices of the peace "
                       "for Jericho: Peter Booth, Tom Cheney, "
                       "Kathleen Bassett Cramer, Tom Joslin, "
                       "Cathy Paris, Carly Schuckers, Carol "
                       "Kanter Smith, Megan Sullivan, Michael "
                       "Sweeney, Michele Tulis, Mike "
                       "Weinberg, and Jennifer Burton"),
                jer_report("the town report's justices of the "
                           "peace block names the same "
                           "twelve, 'elected November 2024 "
                           "to a 2-year term beginning Feb. "
                           "1 2025'")],
               [holder("Peter Booth", "peter-booth"),
                holder("Tom Cheney", "tom-cheney"),
                holder("Kathleen Bassett Cramer",
                       "kathleen-bassett-cramer"),
                holder("Tom Joslin", "tom-joslin"),
                holder("Cathy Paris", "cathy-paris"),
                holder("Carly Schuckers", "carly-schuckers"),
                holder("Carol Kanter Smith",
                       "carol-kanter-smith"),
                holder("Megan Sullivan", "megan-sullivan"),
                holder("Michael Sweeney", "michael-sweeney"),
                holder("Michele Tulis", "michele-tulis"),
                holder("Mike Weinberg", "mike-weinberg"),
                holder("Jennifer Burton", "jennifer-burton")]),
    ]
    jp = jp_election(
        "jericho-vt", "Jericho", 12,
        "names twelve winners for Jericho: Peter Booth, Tom "
        "Cheney, Kathleen Bassett Cramer, Tom Joslin, Cathy "
        "Paris, Carly Schuckers, Carol Kanter Smith, Megan "
        "Sullivan, Michael Sweeney, Michele Tulis, Mike "
        "Weinberg, and Jennifer Burton. Jennifer Burton of "
        "Jericho is a different person from Jennifer Burton "
        "of Johnson, also elected a justice of the peace in "
        "2024; the office is town-bound")
    return spec("jericho", "Jericho", offices, jp)


SPECS["jericho"] = jericho_spec()

# Jericho Village is HELD (nothing minted): no Title 24
# Appendix chapter, a factory gap, and no official source
# names any village officer -- the Albany Village pattern.
# See vt_muni_batch12_research.md.

# ------------------------------------------------------------ emit
for slug in ORDER:
    if slug == "jericho-village":
        continue
    s = SPECS[slug]
    p = OUT / f"{s['place_slug']}.json"
    p.write_text(json.dumps(s, indent=1) + "\n")
    n_off = len(s["offices"])
    n_hold = sum(len(o.get("holders", ())) for o in s["offices"])
    print(f"{s['place_slug']}: {n_off} offices, {n_hold} holders")
print(f"TOTAL: {len(SPECS)} specs (jericho-village held)")
