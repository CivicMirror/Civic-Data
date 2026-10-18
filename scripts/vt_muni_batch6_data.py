#!/usr/bin/env python3
"""Batch 6 of the VT #163 municipal fan-out (alphabetical positions
51-60): Chittenden, Clarendon, Colchester, Concord, Corinth, Cornwall,
Coventry, Craftsbury, Danby, Danville.
Emits one JSON spec per municipality for build_vt_municipality.py.
Research: vt_muni_batch6_research.md.

Process note: three delegated reads in this batch were FABRICATED or
irreconcilable (the first Corinth sweep, the first Craftsbury sweep,
and three mutually conflicting Colchester Selectboard accounts). All
were caught pre-build and discarded; every roster below rests on the
corrected adjudications recorded in the research file (town officers
pages, certified results, signed warnings, and the SOS spine, with
firsthand PDF verification for Concord and Cornwall).
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
             "'2025-2026 Vermont Justices of the Peace' listing "
             f"(updated December 4, 2025): {count_note}")


def guide(what):
    return S(GUIDE, "Vermont Secretary of State, Elections Division, "
             "'Guide to Vermont's Town Clerks, Treasurers, & County "
             f"Clerks' (January 2026): {what}")


def statute2646(office_phrase):
    return S(STATUTE_2646, "17 V.S.A. section 2646 (official text, "
             "Vermont General Assembly) provides for the election of "
             f"{office_phrase} at annual town meeting.")


def statute2646_structure(office_phrase):
    return S(STATUTE_2646, "17 V.S.A. section 2646 (official text, "
             "Vermont General Assembly) provides for the election of "
             f"{office_phrase} at annual town meeting. Structure only: "
             "no official source publishes the current holder; the "
             "seat is left unfilled rather than guessed.")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 6); issue #163 "
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
                  f"# municipal fan-out batch 6; issue #163 "
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


SPECS = []

# ---------------------------------------------------------------- Chittenden
CHI_DOCS = {
    "url": "https://sites.google.com/townofchittenden.com/chittenden-vt/meeting-documents-reports",
    "note": "PLACEHOLDER",
}
CHI_SITE = {
    "url": "https://sites.google.com/townofchittenden.com/chittenden-vt/home",
    "note": "PLACEHOLDER",
}


def chi_docs(what):
    return S(CHI_DOCS, "Town of Chittenden (Rutland County) official "
             "website, Meeting Documents & Reports page (town documents "
             f"hosted on the town's Google Drive): {what}")


def chittenden_spec():
    label = "Town of Chittenden"
    offices = [
        office(
            "selectboard", "Selectboard Member", "Chittenden Selectboard", 5,
            [chi_docs("the 2025 Chittenden Town Report (132nd Annual "
                      "Report), 'Chittenden Town Officers -- Terms of "
                      "Office for March 2026' table, lists five "
                      "Selectboard members: Kathleen Pratt (3-year term, "
                      "2024-2027), Andrew Quint (3-year, 2025-2028), "
                      "Brenda Flower (2-year, 2025-2027), Dave Sargent "
                      "(2-year, 2026-2028), and Gary Congdon (3-year, "
                      "2026-2029)."),
             chi_docs("the approved Selectboard reorganization minutes "
                      "of March 9, 2026 record the board appointing "
                      "Kathie Pratt as Chair; Selectboard minutes of "
                      "September 14 and September 28, 2026 list the "
                      "same five members.")],
            [holder("Kathleen Pratt", "kathleen-pratt"),
             holder("Andrew Quint", "andrew-quint"),
             holder("David Sargent", "david-sargent"),
             holder("Gary Congdon", "gary-congdon"),
             holder("Brenda Flower", "brenda-flower")]),
        office(
            "moderator", "Moderator", "Chittenden Moderator", 1,
            [chi_docs("the 2025 Chittenden Town Report officers table "
                      "('Terms of Office for March 2026') lists the "
                      "Moderator (1-year term, 2026-2027) as Bob Baird; "
                      "the 2026 annual town meeting warning, Article 1, "
                      "warned a Moderator election for a 1-year term.")],
            [holder("Bob Baird", "bob-baird")]),
        office(
            "town-clerk", "Town Clerk", "Chittenden Town Clerk", 1,
            [chi_docs("the 2025 Chittenden Town Report officers table "
                      "lists the Town Clerk under 'Office by Election' "
                      "with a 3-year term (2024-2027): Alyssa Reynolds."),
             guide("lists Alyssa Reynolds as Town Clerk of Chittenden.")],
            [holder("Alyssa Reynolds", "alyssa-reynolds")]),
        office(
            "town-treasurer", "Town Treasurer", "Chittenden Town Treasurer", 1,
            [chi_docs("the 2025 Chittenden Town Report officers table "
                      "lists the Town Treasurer under 'Office by "
                      "Election' with a 3-year term (2024-2027): "
                      "Alyssa Reynolds."),
             guide("lists Alyssa Reynolds as Town Treasurer of "
                   "Chittenden.")],
            [holder("Alyssa Reynolds", "alyssa-reynolds")]),
        office(
            "auditor", "Auditor", "Chittenden Auditors", 3,
            [chi_docs("the 2025 Chittenden Town Report officers table "
                      "lists three Auditor seats: Jeff Spaulding "
                      "(3-year term, 2026-2029), Jean Higgins (3-year, "
                      "2024-2027), and one seat (term 2025-2028) printed "
                      "as Vacant; that seat is left unfilled. Article 9 "
                      "of the 2026 warning proposed eliminating the "
                      "office of Town Auditor under 17 V.S.A. section "
                      "2651b; no posted source records the article's "
                      "outcome, and the post-election officers table "
                      "continues to seat elected auditors, so the "
                      "office stands.")],
            [holder("Jeffrey Spaulding", "jeffrey-spaulding"),
             holder("Jean Higgins", "jean-higgins")]),
        office(
            "cemetery-commissioner", "Cemetery Commissioner",
            "Chittenden Cemetery Commission", 3,
            [chi_docs("the 2025 Chittenden Town Report officers table "
                      "lists three Cemetery Commissioners: Bob Case "
                      "(2025-2028), Herb Pelkey (2026-2029), and David "
                      "Sargent (2024-2027); the 2026 warning, Article 1, "
                      "warned a Cemetery Commissioner election for a "
                      "3-year term, and the 2026 sample ballot prints "
                      "Herbert Pelkey as the candidate.")],
            [holder("Bob Case", "bob-case"),
             holder("Herb Pelkey", "herb-pelkey"),
             holder("David Sargent", "david-sargent")]),
        office(
            "collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
            "Chittenden Collector of Delinquent Taxes", 1,
            [chi_docs("the 2025 Chittenden Town Report officers table "
                      "lists the Delinquent Tax Collector under 'Office "
                      "by Appointment' (3-year term, 2024-2027): "
                      "Alyssa Reynolds. The holder is recorded as "
                      "appointed.")],
            [holder("Alyssa Reynolds", "alyssa-reynolds",
                    how_seated="appointed")]),
        office(
            "trustees-of-public-funds", "Trustee of Public Funds",
            "Chittenden Trustees of Public Funds", 1,
            [chi_docs("the 2025 Chittenden Town Report officers table "
                      "lists a single Trustee of Public Funds among the "
                      "town's appointments: Alyssa Reynolds. The holder "
                      "is recorded as appointed.")],
            [holder("Alyssa Reynolds", "alyssa-reynolds",
                    how_seated="appointed")]),
        office(
            "road-commissioner", "Road Commissioner",
            "Chittenden Road Commissioner", 1,
            [chi_docs("the approved Selectboard reorganization minutes "
                      "of March 9, 2026 record the board appointing "
                      "Gary Congdon as Road Commissioner (the "
                      "pre-reorganization officers table had listed "
                      "Dave Sargent). The holder is recorded as "
                      "appointed.")],
            [holder("Gary Congdon", "gary-congdon",
                    how_seated="appointed")]),
        office(
            "justice-of-the-peace", "Justice of the Peace",
            "Chittenden Justices of the Peace", 7,
            [jp_src("lists seven Chittenden (Rutland County) justices "
                    "of the peace: Alison Briggs, Katherine Hall, "
                    "Charles Ogg, Linda Reis, David Sargent, Jeffrey "
                    "Spaulding, and Bradford White."),
             chi_docs("the 2025 Chittenden Town Report officers table "
                      "lists the same seven justices of the peace "
                      "(2-year terms, February 1, 2025 - January 31, "
                      "2027).")],
            [holder("Alison Briggs", "alison-briggs"),
             holder("Katherine Hall", "katherine-hall"),
             holder("Charles Ogg", "charles-ogg"),
             holder("Linda Reis", "linda-reis"),
             holder("David Sargent", "david-sargent"),
             holder("Jeffrey Spaulding", "jeffrey-spaulding"),
             holder("Bradford White", "bradford-white")]),
    ]
    jp = jp_election(
        "chittenden-vt", label, 7,
        "lists seven Chittenden (Rutland County) justices of the "
        "peace elected November 5, 2024: Alison Briggs, Katherine "
        "Hall, Charles Ogg, Linda Reis, David Sargent, Jeffrey "
        "Spaulding, and Bradford White. The listing publishes no "
        "vote totals or party labels and none are recorded.")
    return spec("chittenden", label, offices, jp)


SPECS.append(chittenden_spec())

# ---------------------------------------------------------------- Clarendon
CLA_SITE = {
    "url": "https://www.clarendonvt.gov",
    "note": "PLACEHOLDER",
}
CLA_MINUTES = {
    "url": "https://www.clarendonvt.gov/category/town-minutes-agenda/",
    "note": "PLACEHOLDER",
}


def cla_site(what):
    return S(CLA_SITE, "Town of Clarendon official website "
             f"(clarendonvt.gov): {what}")


def cla_minutes(what):
    return S(CLA_MINUTES, "Town of Clarendon official website, Town "
             f"Minutes & Agenda archive: {what}")


def clarendon_spec():
    label = "Town of Clarendon"
    offices = [
        office(
            "selectboard", "Selectboard Member", "Clarendon Selectboard", 5,
            [sb_dir("lists five Clarendon Selectboard members: George "
                    "Ambrose, Robert Congdon, Michael Klopchin, Don "
                    "Pratt, and Cash Ruane."),
             cla_minutes("Selectboard minutes, September-October 2026, "
                         "seat the same five, with Mike Klopchin as "
                         "Chair; the March 2026 annual-meeting returns "
                         "re-elected Klopchin (475 votes, 3-year term) "
                         "and Ruane (472 votes, 2-year term).")],
            [holder("Michael Klopchin", "michael-klopchin"),
             holder("George Ambrose", "george-ambrose"),
             holder("Robert Congdon", "robert-congdon"),
             holder("Cash Ruane", "cash-ruane"),
             holder("Don Pratt", "don-pratt")]),
        office(
            "town-clerk", "Town Clerk", "Clarendon Town Clerk", 1,
            [cla_site("the town's contacts page styles the office 'Town "
                      "Clerk/Administrator' and names Kimberly Young as "
                      "the appointed Town Clerk/Administrator; she signs "
                      "the town's 2026 minutes as Town Clerk. The "
                      "holder is recorded as appointed. The Secretary "
                      "of State Guide (January 2026) still names Gloria "
                      "Menard, who appears on the town's current "
                      "contacts page as Assistant Town Clerk -- a 2026 "
                      "succession; the town's current page governs.")],
            [holder("Kimberly Young", "kimberly-young",
                    how_seated="appointed")]),
        office(
            "town-treasurer", "Town Treasurer", "Clarendon Town Treasurer", 1,
            [cla_site("the March 2026 annual-meeting returns re-elected "
                      "Heidi Congdon as Town Treasurer (505 votes, "
                      "1-year term); Selectboard minutes, September "
                      "2026, list her as Treasurer."),
             guide("lists Heidi Congdon as Town Treasurer of "
                   "Clarendon.")],
            [holder("Heidi Congdon", "heidi-congdon")]),
        office(
            "collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
            "Clarendon Collector of Delinquent Taxes", 1,
            [cla_site("the March 2026 annual-meeting returns elected "
                      "Heidi Congdon as Collector of Delinquent Taxes "
                      "as a separate office (507 votes, 1-year term).")],
            [holder("Heidi Congdon", "heidi-congdon")]),
        office(
            "moderator", "Moderator", "Clarendon Moderator", 1,
            [cla_site("the March 2026 annual-meeting returns elected "
                      "David A. Potter Jr. as Moderator (elected "
                      "annually; recorded as the 2026 write-in winner "
                      "with 2 votes).")],
            [holder("David A. Potter Jr.", "david-potter-jr")]),
        office(
            "lister", "Lister", "Clarendon Listers", 3,
            [cla_site("the town's lister records and the 2025 Annual "
                      "Report officers table list three Lister seats: "
                      "Danielle Jewell (term expiring 2027) and David "
                      "Kelly (term expiring 2028) are seated; the "
                      "third seat (Patricia Kent, term expiring 2026) "
                      "stood for election in 2026 and no official "
                      "source publishes its outcome, so it is left "
                      "unfilled.")],
            [holder("Danielle Jewell", "danielle-jewell"),
             holder("David Kelly", "david-kelly")]),
        office(
            "constable", "Constable", "Clarendon Constable", 1,
            [cla_site("the March 2026 annual-meeting returns elected "
                      "Edward Babic as Constable (505 votes, 1-year "
                      "term); Clarendon elects a single constable.")],
            [holder("Edward Babic", "edward-babic")]),
        office(
            "library-trustee", "Library Trustee",
            "Clarendon Bailey Memorial Library Trustees", 5,
            [cla_site("the Bailey Memorial Library trustee roster "
                      "lists five seats on 5-year staggered terms: "
                      "Carol Stewart (term expiring 2030), Jan Baker "
                      "(2029), and Tina Sherman (2028) are seated; "
                      "one seat is printed as vacant (2027) and the "
                      "seat expiring in 2026 has no published outcome, "
                      "so both are left unfilled.")],
            [holder("Carol Stewart", "carol-stewart"),
             holder("Jan Baker", "jan-baker"),
             holder("Tina Sherman", "tina-sherman")]),
        office(
            "cemetery-commissioner", "Cemetery Commissioner",
            "Clarendon Cemetery Commission", 3,
            [cla_site("the town's cemetery records list three "
                      "Cemetery Commissioner seats: Ashley Page "
                      "(term expiring 2027) and Joseph Carrara (2028) "
                      "are seated; the third seat stood in 2026 and "
                      "is vacant, so it is left unfilled.")],
            [holder("Ashley Page", "ashley-page"),
             holder("Joseph Carrara", "joseph-carrara")]),
        office(
            "justice-of-the-peace", "Justice of the Peace",
            "Clarendon Justices of the Peace", 8,
            [jp_src("lists eight Clarendon justices of the peace: "
                    "George Ambrose, David Bosch, Robert Congdon, "
                    "John Colvin, Deborah Dougherty, Kevin Dougherty, "
                    "Arthur Menard, and Brownson Spencer.")],
            [holder("George Ambrose", "george-ambrose"),
             holder("David Bosch", "david-bosch"),
             holder("Robert Congdon", "robert-congdon"),
             holder("John Colvin", "john-colvin"),
             holder("Deborah Dougherty", "deborah-dougherty"),
             holder("Kevin Dougherty", "kevin-dougherty"),
             holder("Arthur Menard", "arthur-menard"),
             holder("Brownson Spencer", "brownson-spencer")]),
    ]
    jp = jp_election(
        "clarendon-vt", label, 8,
        "lists eight Clarendon justices of the peace elected "
        "November 5, 2024: George Ambrose, David Bosch, Robert "
        "Congdon, John Colvin, Deborah Dougherty, Kevin Dougherty, "
        "Arthur Menard, and Brownson Spencer. The listing publishes "
        "no vote totals or party labels and none are recorded.")
    return spec("clarendon", label, offices, jp)


SPECS.append(clarendon_spec())

# ---------------------------------------------------------------- Colchester
COL_SB = {
    "url": "https://colchestervt.gov/401/Selectboard",
    "note": "PLACEHOLDER",
}
COL_DIR = {
    "url": "https://colchestervt.gov/directory.aspx",
    "note": "PLACEHOLDER",
}
COL_BOARDS = {
    "url": "https://colchestervt.gov/369/Boards-Commissions",
    "note": "PLACEHOLDER",
}
COL_TRUSTEES = {
    "url": "https://colchestervt.gov/409/Library-Board-of-Trustees",
    "note": "PLACEHOLDER",
}
COL_CH202 = {
    "url": "https://legislature.vermont.gov/statutes/section/24APPENDIX/113/00202",
    "note": "PLACEHOLDER",
}


def col_sb(what):
    return S(COL_SB, "Town of Colchester official website, "
             f"Selectboard page: {what}")


def col_ch202(what):
    return S(COL_CH202, "Colchester town charter, 24 Appendix "
             f"V.S.A. chapter 113, section 202 (official text): {what}")


def colchester_spec():
    label = "Town of Colchester"
    offices = [
        office(
            "selectboard", "Selectboard Member", "Colchester Selectboard", 5,
            [sb_dir("lists five Colchester Selectboard members: "
                    "Maureen Dakin, Pam Loranger, Jacki Murphy, "
                    "Charlie Papillo, and Paul Pecor."),
             col_sb("lists 'Pam Loranger, Chair', 'Charlie Papillo, "
                    "Vice Chair', 'Jacki Murphy, Clerk', 'Maureen "
                    "Dakin', and 'Paul Pecor' -- the same five.")],
            [holder("Pam Loranger", "pam-loranger"),
             holder("Charlie Papillo", "charlie-papillo"),
             holder("Jacki Murphy", "jacki-murphy"),
             holder("Maureen Dakin", "maureen-dakin"),
             holder("Paul Pecor", "paul-pecor")]),
        office(
            "moderator", "Moderator", "Colchester Moderator", 1,
            [col_ch202("provides for the election of a Moderator at "
                       "the annual meeting. Structure only: no "
                       "official source read publishes the current "
                       "holder; the seat is left unfilled rather "
                       "than guessed.")]),
        office(
            "town-clerk", "Town Clerk", "Colchester Town Clerk", 1,
            [col_ch202("the Town Clerk is not an elected officer "
                       "under the charter; under section 404(k) the "
                       "Town Manager appoints the Town Clerk (a 2018 "
                       "charter amendment, Act M-17, converted the "
                       "office from elected to appointed)."),
             guide("lists Julie Graeter as Town Clerk of Colchester."),
             S(COL_DIR, "Town of Colchester official website, staff "
                        "directory: Julie Graeter serves as Town "
                        "Clerk/Treasurer. The holder is recorded as "
                        "appointed.")],
            [holder("Julie Graeter", "julie-graeter",
                    how_seated="appointed")]),
        office(
            "town-treasurer", "Town Treasurer", "Colchester Town Treasurer", 1,
            [col_ch202("the Town Treasurer is not an elected officer "
                       "under the charter; under section 404(k) the "
                       "Town Manager appoints the Town Treasurer (a "
                       "2018 charter amendment, Act M-17, converted "
                       "the office from elected to appointed)."),
             guide("lists Julie Graeter as Town Treasurer of "
                   "Colchester."),
             S(COL_DIR, "Town of Colchester official website, staff "
                        "directory: Julie Graeter serves as Town "
                        "Clerk/Treasurer. The holder is recorded as "
                        "appointed.")],
            [holder("Julie Graeter", "julie-graeter",
                    how_seated="appointed")]),
        office(
            "lister", "Lister", "Colchester Listers", 3,
            [col_ch202("provides for the election of one Lister each "
                       "year to a 3-year term (a board of three); "
                       "the elected listers sit as the Board of "
                       "Assessment under section 501."),
             S(COL_BOARDS, "Town of Colchester official website, "
                           "Boards & Commissions page, lists the "
                           "listers among the town's elected boards. "
                           "The three listers' own signed statutory "
                           "notice of June 12, 2026 (32 V.S.A. section "
                           "4111, published in Seven Days legal "
                           "notices) is signed by Geri Barrows, "
                           "Charlotte Gardner, and Angela MacDonald.")],
            [holder("Geri Barrows", "geri-barrows"),
             holder("Charlotte Gardner", "charlotte-gardner"),
             holder("Angela MacDonald", "angela-macdonald")]),
        office(
            "library-trustee", "Library Trustee",
            "Colchester Burnham Memorial Library Trustees", 5,
            [col_ch202("provides for the election of one Library "
                       "Trustee each year to a 5-year term (a board "
                       "of five)."),
             S(COL_TRUSTEES, "Town of Colchester official website, "
                             "Burnham Memorial Library Board of "
                             "Trustees page: lists Toni Josey "
                             "(Chair), Leora Black, Carol Anderson, "
                             "Rebecca McMahon, and Brent Litterer.")],
            [holder("Toni Josey", "toni-josey"),
             holder("Leora Black", "leora-black"),
             holder("Carol Anderson", "carol-anderson"),
             holder("Rebecca McMahon", "rebecca-mcmahon"),
             holder("Brent Litterer", "brent-litterer")]),
        office(
            "justice-of-the-peace", "Justice of the Peace",
            "Colchester Justices of the Peace", 15,
            [jp_src("lists fifteen Colchester justices of the peace: "
                    "Carol Anderson, Sarita Austin, Leora Black, "
                    "Ruth Blauwiekel, Mary Brennan, Patrick Brennan, "
                    "Wendy Critchlow, Maureen Dakin, Peg Gillard, "
                    "Julie Hulburd, Marie-Reine Pepin, Curt Taylor, "
                    "Tom Yasewicz, Jeanette Berry, and Robby Mazza.")],
            [holder("Carol Anderson", "carol-anderson"),
             holder("Sarita Austin", "sarita-austin",
                    existing_person_id="ocd-person/3c6795d8-abaf-5bb8-997e-5190455b9c42"),
             holder("Leora Black", "leora-black"),
             holder("Ruth Blauwiekel", "ruth-blauwiekel"),
             holder("Mary Brennan", "mary-brennan"),
             holder("Patrick Brennan", "patrick-brennan"),
             holder("Wendy Critchlow", "wendy-critchlow",
                    existing_person_id="ocd-person/53ddd42b-b0c4-53b4-85ec-a658595096d7"),
             holder("Maureen Dakin", "maureen-dakin"),
             holder("Peg Gillard", "peg-gillard"),
             holder("Julie Hulburd", "julie-hulburd"),
             holder("Marie-Reine Pepin", "marie-reine-pepin"),
             holder("Curt Taylor", "curt-taylor"),
             holder("Tom Yasewicz", "tom-yasewicz"),
             holder("Jeanette Berry", "jeanette-berry"),
             holder("Robby Mazza", "robby-mazza")]),
    ]
    jp = jp_election(
        "colchester-vt", label, 15,
        "lists fifteen Colchester justices of the peace elected "
        "November 5, 2024: Carol Anderson, Sarita Austin, Leora "
        "Black, Ruth Blauwiekel, Mary Brennan, Patrick Brennan, "
        "Wendy Critchlow, Maureen Dakin, Peg Gillard, Julie "
        "Hulburd, Marie-Reine Pepin, Curt Taylor, Tom Yasewicz, "
        "Jeanette Berry, and Robby Mazza. The listing publishes "
        "no vote totals or party labels and none are recorded. "
        "Sarita Austin and Wendy Critchlow are the sitting State "
        "Representatives for the Chittenden-19 district "
        "(Colchester); their existing person records carry this "
        "candidacy.")
    return spec("colchester", label, offices, jp)


SPECS.append(colchester_spec())

# ---------------------------------------------------------------- Concord
CON_REPORT = {
    "url": "https://www.concordvt.us/wp-content/uploads/2026/02/Town-of-Concord-Report-2025.zip",
    "note": "PLACEHOLDER",
}
CON_RESULTS = {
    "url": "https://www.concordvt.us/wp-content/uploads/2026/03/2026-Annual-Town-Meeting-Results.pdf",
    "note": "PLACEHOLDER",
}


def con_report(what):
    return S(CON_REPORT, "Town of Concord, 'Town of Concord Report "
             "2025' (annual report archive posted on the town's "
             f"official website, concordvt.us): {what}")


def con_results(what):
    return S(CON_RESULTS, "Town of Concord, March 3, 2026 Annual "
             "Town Meeting results (certified tally sheets of Town "
             f"Clerk Linda A. Blakslee, posted on concordvt.us): {what}")


def concord_spec():
    label = "Town of Concord"
    offices = [
        office(
            "selectboard", "Selectboard Member", "Concord Selectboard", 5,
            [sb_dir("lists five Concord Selectboard members: Richard "
                    "Casavant, James Gochie, Denis Lamadeleine "
                    "(Vice Chair), George Morehouse, and Jason Payeur "
                    "(Chair)."),
             con_results("certify the March 3, 2026 re-election of "
                         "James Gochie (2-year term) and Richard "
                         "Casavant (3-year term)."),
             con_report("'Elected Town Officials as of December 31, "
                        "2025' lists the board before the 2026 "
                        "meeting as Payeur, Lamadeleine, Morehouse, "
                        "Chris Fournier, and Bill Humphrey; Fournier "
                        "and Humphrey rotated off at the 2026 "
                        "meeting.")],
            [holder("Jason Payeur", "jason-payeur"),
             holder("Denis Lamadeleine", "denis-lamadeleine"),
             holder("James Gochie", "james-gochie"),
             holder("Richard Casavant", "richard-casavant"),
             holder("George Morehouse", "george-morehouse")]),
        office(
            "moderator", "Moderator", "Concord Moderator", 1,
            [con_results("certify Chris Fournier's election as Town "
                         "Moderator for a 1-year term on March 3, "
                         "2026 (116 votes)."),
             con_report("'Elected Town Officials as of December 31, "
                        "2025' lists Chris Fournier as Moderator.")],
            [holder("Chris Fournier", "chris-fournier")]),
        office(
            "town-clerk", "Town Clerk", "Concord Town Clerk", 1,
            [con_results("certify Linda A. Blakslee's re-election as "
                         "Town Clerk for a 3-year term on March 3, "
                         "2026."),
             guide("lists Linda A. Blakslee as Town Clerk of "
                   "Concord.")],
            [holder("Linda Blakslee", "linda-blakslee")]),
        office(
            "town-treasurer", "Town Treasurer", "Concord Town Treasurer", 1,
            [con_results("certify Audra Girouard's re-election as "
                         "Town Treasurer for a 3-year term on "
                         "March 3, 2026. The town collects its taxes "
                         "by its Treasurer (warning Article 2), so "
                         "no separate collector office exists."),
             guide("lists Audra Girouard as Town Treasurer of "
                   "Concord.")],
            [holder("Audra Girouard", "audra-girouard")]),
        office(
            "auditor", "Auditor", "Concord Auditors", 3,
            [con_report("'Elected Town Officials as of December 31, "
                        "2025' lists three Auditors: Donna Berry "
                        "(term expiring 2026), Laura Goldshein "
                        "(remainder of a term expiring 2027), and "
                        "Theresa Hovey (term expiring 2028)."),
             con_results("certify Donna Berry's re-election as "
                         "Auditor for a 3-year term on March 3, 2026 "
                         "(157 votes).")],
            [holder("Donna Berry", "donna-berry"),
             holder("Laura Goldshein", "laura-goldshein"),
             holder("Theresa Hovey", "theresa-hovey")]),
        office(
            "library-trustee", "Library Trustee",
            "Concord Library Trustees", 5,
            [con_report("'Elected Town Officials as of December 31, "
                        "2025' lists five Library Trustees on 5-year "
                        "terms: Jill Abetti (expiring 2026), Mary "
                        "Gochie (remainder, 2028), Nancy LaPotin "
                        "(2029), Elaine Stasny (remainder, 2027), "
                        "and Eileen Wilson (2028)."),
             con_results("certify the March 3, 2026 election of "
                         "Jill Abetti (5-year term, 162 votes) and "
                         "Mary Gochie (remainder of a 5-year term "
                         "to 2028, 176 votes).")],
            [holder("Jill Abetti", "jill-abetti"),
             holder("Mary Gochie", "mary-gochie"),
             holder("Nancy LaPotin", "nancy-lapotin"),
             holder("Elaine Stasny", "elaine-stasny"),
             holder("Eileen Wilson", "eileen-wilson")]),
        office(
            "justice-of-the-peace", "Justice of the Peace",
            "Concord Justices of the Peace", 5,
            [jp_src("lists five Concord justices of the peace: "
                    "Danielle Balch, Linda Blakslee, Paula "
                    "Christopher, Christopher Fournier, and Arlene "
                    "Hovey."),
             con_report("'Elected Town Officials as of December 31, "
                        "2025' lists the same five justices of the "
                        "peace (terms expiring February 2027).")],
            [holder("Danielle Balch", "danielle-balch"),
             holder("Linda Blakslee", "linda-blakslee"),
             holder("Paula Christopher", "paula-christopher"),
             holder("Chris Fournier", "chris-fournier",
                    ballot_name="Christopher Fournier"),
             holder("Arlene Hovey", "arlene-hovey")]),
    ]
    jp = jp_election(
        "concord-vt", label, 5,
        "lists five Concord justices of the peace elected "
        "November 5, 2024: Danielle Balch, Linda Blakslee, Paula "
        "Christopher, Christopher Fournier, and Arlene Hovey. "
        "The listing publishes no vote totals or party labels "
        "and none are recorded.")
    return spec("concord", label, offices, jp)


SPECS.append(concord_spec())

# ---------------------------------------------------------------- Corinth
COR_PAGE = {
    "url": "https://corinthvt.org/town-govt/town-officers/",
    "note": "PLACEHOLDER",
}
COR_RESULTS = {
    "url": "https://corinthvt.org/wp-content/uploads/2026/03/Corinth-Annual-Town-Meeting-Voting-Results-3-03-2026.pdf",
    "note": "PLACEHOLDER",
}
COR_REPORT = {
    "url": "https://corinthvt.org/wp-content/uploads/2026/02/CORINTH-Annual-Report-2025.pdf",
    "note": "PLACEHOLDER",
}


def cor_page(what):
    return S(COR_PAGE, "Town of Corinth official website, Town "
             f"Officers page: {what}")


def cor_results(what):
    return S(COR_RESULTS, "Town of Corinth, March 3, 2026 Town "
             f"Meeting voting results (posted on corinthvt.org): {what}")


def corinth_spec():
    label = "Town of Corinth"
    offices = [
        office(
            "selectboard", "Selectboard Member", "Corinth Selectboard", 3,
            [sb_dir("lists three Corinth Selectboard members: Carl "
                    "Demrow, Stephen Devoto, and Holly Groschner."),
             cor_page("lists the Selectboard as Carl Demrow (term "
                      "ends 2029), Stephen Devoto (2027), and Holly "
                      "Groschner (2028), with Groschner marked as "
                      "Chair; the March 3, 2026 Town Meeting minutes "
                      "are signed by her as Selectboard Chair.")],
            [holder("Holly Groschner", "holly-groschner"),
             holder("Carl Demrow", "carl-demrow"),
             holder("Stephen Devoto", "stephen-devoto")]),
        office(
            "moderator", "Moderator", "Corinth Moderator", 1,
            [cor_page("lists the Moderator (1-year term, ends 2027) "
                      "as Gary Apfel."),
             cor_results("record 'Town Moderator for 1 year -- "
                         "WINNER: Gary Apfel'.")],
            [holder("Gary Apfel", "gary-apfel")]),
        office(
            "town-clerk", "Town Clerk", "Corinth Town Clerk", 1,
            [cor_page("lists the Town Clerk (3-year term, ends 2029) "
                      "as Martha Brough."),
             guide("lists Martha Brough as Town Clerk of Corinth.")],
            [holder("Martha Brough", "martha-brough")]),
        office(
            "town-treasurer", "Town Treasurer", "Corinth Town Treasurer", 1,
            [S(COR_REPORT, "Town of Corinth, Annual Report 2025 "
                           "(FY2025): the officers table prints "
                           "'TREASURER -vacant-', and the town's "
                           "Town Officers page directs treasurer "
                           "matters to an Interim Assistant "
                           "Treasurer (a staff position). Structure "
                           "only: the office is vacant; no holder is "
                           "recorded rather than guessed."),
             guide("lists the Corinth Town Treasurer position as "
                   "vacant.")]),
        office(
            "lister", "Lister", "Corinth Listers", 3,
            [cor_page("lists three Listers: KellyAnn Donahue (Chair, "
                      "term ends 2028), Marsha Blake (2028), and "
                      "Mary B. Martin (2027)."),
             cor_results("record the March 3, 2026 winners: 'Lister "
                         "for 1 year -- WINNER: Mary B Martin' and "
                         "'Lister for 2 years -- WINNER: Marsha R "
                         "Blake'.")],
            [holder("KellyAnn Donahue", "kellyann-donahue"),
             holder("Marsha Blake", "marsha-blake"),
             holder("Mary B. Martin", "mary-b-martin")]),
        office(
            "collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
            "Corinth Collector of Delinquent Taxes", 1,
            [cor_page("lists the Collector of Delinquent Taxes "
                      "(1-year term, ends 2027) as Raymond Moulton."),
             cor_results("record 'Delinquent Tax Collector for 1 "
                         "year -- WINNER: Raymond Moulton'.")],
            [holder("Raymond Moulton", "raymond-moulton")]),
        office(
            "cemetery-commissioner", "Cemetery Commissioner",
            "Corinth Cemetery Commission", 3,
            [cor_page("lists three Cemetery Commissioners (3-year "
                      "terms): Luke Campbell (ends 2027), Norman "
                      "Collette (Chair, 2029), and Raymond Moulton "
                      "(2028)."),
             cor_results("record 'Cemetery Commissioner for 3 years "
                         "-- WINNER: Norm Collette'.")],
            [holder("Luke Campbell", "luke-campbell"),
             holder("Norman Collette", "norman-collette"),
             holder("Raymond Moulton", "raymond-moulton")]),
        office(
            "constable", "Constable", "Corinth Constable", 1,
            [cor_page("lists the Constable office (1-year term) as "
                      "vacant. Structure only: no official source "
                      "publishes a current holder; the seat is left "
                      "unfilled rather than guessed.")]),
        office(
            "road-commissioner", "Road Commissioner",
            "Corinth Road Commissioner", 1,
            [cor_page("lists the Road Commissioner (3-year term, "
                      "ends 2027) as Lee Porter among the town's "
                      "appointed officers. The holder is recorded "
                      "as appointed.")],
            [holder("Lee Porter", "lee-porter",
                    how_seated="appointed")]),
        office(
            "justice-of-the-peace", "Justice of the Peace",
            "Corinth Justices of the Peace", 7,
            [jp_src("lists seven Corinth justices of the peace: "
                    "Kathy Chapman, Jane Conner, Anne Margolis, "
                    "Tim O'Dell, Russ Pazdro, Amy Peberdy, and "
                    "Allegra Shumway."),
             cor_page("lists the same seven justices of the peace "
                      "(2-year terms expiring January 31, 2027).")],
            [holder("Kathy Chapman", "kathy-chapman"),
             holder("Jane Conner", "jane-conner"),
             holder("Anne Margolis", "anne-margolis"),
             holder("Tim O'Dell", "tim-odell"),
             holder("Russ Pazdro", "russ-pazdro"),
             holder("Amy Peberdy", "amy-peberdy"),
             holder("Allegra Shumway", "allegra-shumway")]),
    ]
    jp = jp_election(
        "corinth-vt", label, 7,
        "lists seven Corinth justices of the peace elected "
        "November 5, 2024: Kathy Chapman, Jane Conner, Anne "
        "Margolis, Tim O'Dell, Russ Pazdro, Amy Peberdy, and "
        "Allegra Shumway. The listing publishes no vote totals "
        "or party labels and none are recorded.")
    return spec("corinth", label, offices, jp)


SPECS.append(corinth_spec())

# ---------------------------------------------------------------- Cornwall
CRN_REPORT = {
    "url": "https://www.cornwallvt.gov/media/5896",
    "note": "PLACEHOLDER",
}
CRN_BALLOT = {
    "url": "https://www.cornwallvt.gov/media/5926",
    "note": "PLACEHOLDER",
}
CRN_MINUTES = {
    "url": "https://www.cornwallvt.gov/media/6321",
    "note": "PLACEHOLDER",
}


def crn_report(what):
    return S(CRN_REPORT, "Town of Cornwall, 2025 Town Report "
             "(147th Annual Report, year ending December 31, "
             f"2025; cornwallvt.gov): {what}")


def crn_ballot(what):
    return S(CRN_BALLOT, "Town of Cornwall, Official Annual Town "
             f"Meeting Ballot, March 3, 2026 (cornwallvt.gov): {what}")


def cornwall_spec():
    label = "Town of Cornwall"
    offices = [
        office(
            "selectboard", "Selectboard Member", "Cornwall Selectboard", 5,
            [sb_dir("lists five Cornwall Selectboard members: Tanya "
                    "Byker (Chair), Don Burns (Vice Chair), Barbara "
                    "Greenwood, Brian Kemp, and John Roberts."),
             crn_report("'Elected Town Officers 2025' lists the "
                        "board before the 2026 meeting as Byker, "
                        "Burns, Kemp, Roberts, and Shawn Fetterolf."),
             crn_ballot("prints Brian Kemp as the only candidate "
                        "for the 3-year seat and Shawn Fetterolf "
                        "and Barbara Greenwood for the 2-year seat; "
                        "the Secretary of State directory seats "
                        "Greenwood, establishing that she won the "
                        "2-year seat. No official tally for the "
                        "March 3, 2026 ballot is posted on the "
                        "town's website.")],
            [holder("Tanya Byker", "tanya-byker"),
             holder("Don Burns", "don-burns"),
             holder("Brian Kemp", "brian-kemp"),
             holder("John Roberts", "john-roberts"),
             holder("Barbara Greenwood", "barbara-greenwood")]),
        office(
            "moderator", "Moderator", "Cornwall Moderator", 1,
            [crn_report("'Elected Town Officers 2025' lists the "
                        "Moderator as Cy Day Tall."),
             crn_ballot("prints Cy Day Tall as the only candidate "
                        "for Moderator (1-year term) at the March 3, "
                        "2026 meeting.")],
            [holder("Cy Day Tall", "cy-day-tall")]),
        office(
            "town-clerk", "Town Clerk", "Cornwall Town Clerk", 1,
            [crn_ballot("prints Laura Fetterolf as the only "
                        "candidate 'For Town Clerk, For 3 Years' at "
                        "the March 3, 2026 meeting -- the first "
                        "election for the office after the March "
                        "2025 meeting voted (Article 8) to return "
                        "the clerkship from appointed to elected "
                        "for a 3-year term starting Town Meeting "
                        "2026."),
             S(CRN_MINUTES, "Town of Cornwall, approved Town "
                            "Meeting Minutes of February 28, 2026 "
                            "(cornwallvt.gov): the minutes are "
                            "submitted by Laura Fetterolf as Town "
                            "Clerk; the 2025 Town Report's appointed "
                            "officers table had listed her as the "
                            "appointed Town Clerk.")],
            [holder("Laura Fetterolf", "laura-fetterolf")]),
        office(
            "town-treasurer", "Town Treasurer", "Cornwall Town Treasurer", 1,
            [crn_report("'Appointed Town Officers 2025' lists the "
                        "Town Treasurer as Susan Johnson."),
             S(CRN_MINUTES, "Town of Cornwall, approved Town "
                            "Meeting Minutes of February 28, 2026: "
                            "'Sue Johnson has been appointed "
                            "Treasurer to fulfill the statutorily "
                            "required position.' The holder is "
                            "recorded as appointed.")],
            [holder("Susan Johnson", "susan-johnson",
                    how_seated="appointed")]),
        office(
            "collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
            "Cornwall Collector of Delinquent Taxes", 1,
            [crn_report("'Elected Town Officers 2025' lists the "
                        "Delinquent Tax Collector as Nicholas Elder "
                        "(appointed)."),
             S(CRN_MINUTES, "Town of Cornwall, approved Town "
                            "Meeting Minutes of February 28, 2026: "
                            "Article 7, moving the Delinquent Tax "
                            "Collector from elected to an appointed "
                            "position with a 1-year term, carried; "
                            "the minutes identify Nicholas Elder "
                            "(formerly Gill) as the current appointed "
                            "delinquent tax collector. The holder "
                            "is recorded as appointed.")],
            [holder("Nicholas Elder", "nicholas-elder",
                    how_seated="appointed")]),
        office(
            "lister", "Lister", "Cornwall Listers", 3,
            [crn_report("'Elected Town Officers 2025' lists three "
                        "Listers: Jordan Young (term expiring "
                        "2026), William Johnson (2027), and Todd "
                        "Kincaid (2028)."),
             crn_ballot("prints Jordan Young as the only candidate "
                        "for Lister (3-year term) at the March 3, "
                        "2026 meeting.")],
            [holder("Jordan Young", "jordan-young"),
             holder("William Johnson", "william-johnson"),
             holder("Todd Kincaid", "todd-kincaid")]),
        office(
            "auditor", "Auditor", "Cornwall Auditors", 3,
            [crn_report("'Elected Town Officers 2025' lists three "
                        "Auditors: Caroline Mellish (term expiring "
                        "2026), Ian Gill (2027), and Katie Gieges "
                        "(2028)."),
             crn_ballot("the March 3, 2026 ballot's Auditor contest "
                        "(3-year term) printed no candidate's name "
                        "(write-in only), and no official tally is "
                        "posted; the seat that stood in 2026 is "
                        "left unfilled.")],
            [holder("Ian Gill", "ian-gill"),
             holder("Katie Gieges", "katie-gieges")]),
        office(
            "trustees-of-public-funds", "Trustee of Public Funds",
            "Cornwall Trustees of Public Funds", 3,
            [crn_report("'Elected Town Officers 2025' lists three "
                        "Trustees of Public Funds: David Anderson "
                        "(appointed; term expiring 2026), Elizabeth "
                        "Toder (2026), and Magna Dodge (2027)."),
             crn_ballot("prints Elizabeth Toder as the only "
                        "candidate for the 3-year term and David "
                        "Anderson as the only candidate for the "
                        "2-year unexpired term at the March 3, "
                        "2026 meeting.")],
            [holder("Magna Dodge", "magna-dodge"),
             holder("Elizabeth Toder", "elizabeth-toder"),
             holder("David Anderson", "david-anderson")]),
        office(
            "cemetery-commissioner", "Cemetery Commissioner",
            "Cornwall Cemetery Commission", 5,
            [crn_report("'Elected Town Officers 2025' lists five "
                        "Cemetery Commissioners: Anne Collins "
                        "(term expiring 2026), Janet Franklin "
                        "(appointed, 2027), Roth 'T' Tall (2028), "
                        "Jim Pugh (2029), and Sue Johnson (2030)."),
             crn_ballot("prints Anne Collins as the only candidate "
                        "for Cemetery Commissioner (5-year term) "
                        "at the March 3, 2026 meeting.")],
            [holder("Anne Collins", "anne-collins"),
             holder("Janet Franklin", "janet-franklin",
                    how_seated="appointed"),
             holder("Roth Tall", "roth-tall"),
             holder("Jim Pugh", "jim-pugh"),
             holder("Susan Johnson", "susan-johnson")]),
        office(
            "first-constable", "First Constable", "Cornwall First Constable", 1,
            [crn_report("'Elected Town Officers 2025' lists the "
                        "First Constable as Gary Margolis."),
             crn_ballot("prints Gary Margolis as the only "
                        "candidate for First Constable at the "
                        "March 3, 2026 meeting.")],
            [holder("Gary Margolis", "gary-margolis")]),
        office(
            "second-constable", "Second Constable",
            "Cornwall Second Constable", 1,
            [crn_report("'Elected Town Officers 2025' lists the "
                        "Second Constable as Luke Jerome."),
             crn_ballot("prints Luke Jerome as the only candidate "
                        "for Second Constable at the March 3, 2026 "
                        "meeting.")],
            [holder("Luke Jerome", "luke-jerome")]),
        office(
            "library-trustee", "Library Trustee",
            "Cornwall Library Trustees", 7,
            [crn_report("'Elected Town Officers 2025' lists seven "
                        "Library Trustee seats on 2-year terms: "
                        "three expiring in 2026 (one printed "
                        "vacant) and Laura Fetterolf, Rich "
                        "Isenberg, Patty McCormick, and Kristina "
                        "Simmons expiring in 2027."),
             crn_ballot("the March 3, 2026 ballot warned three "
                        "Library Trustee seats; the candidates "
                        "printed (Tobi Andrews, Barbara Kinkead, "
                        "Amanda Payne) are not recorded as holders "
                        "because no official tally is posted -- "
                        "candidates are not winners. The three "
                        "2026 seats are left unfilled.")],
            [holder("Laura Fetterolf", "laura-fetterolf"),
             holder("Rich Isenberg", "rich-isenberg"),
             holder("Patty McCormick", "patty-mccormick"),
             holder("Kristina Simmons", "kristina-simmons")]),
        office(
            "road-commissioner", "Road Commissioner",
            "Cornwall Road Commissioner", 1,
            [crn_report("'Appointed Town Officers 2025' lists the "
                        "Road Commissioner as Brian Kemp, with the "
                        "appointment term expiring in 2026. "
                        "Structure only: no official source "
                        "publishes the current appointee; the seat "
                        "is left unfilled rather than guessed.")]),
        office(
            "justice-of-the-peace", "Justice of the Peace",
            "Cornwall Justices of the Peace", 5,
            [jp_src("lists five Cornwall justices of the peace: "
                    "David Anderson, Marjorie Drexler, Susan "
                    "Johnson, Gary Margolis, and Jordan Young."),
             crn_report("'Elected Town Officers 2025' lists the "
                        "town's justices of the peace as Marjorie "
                        "Drexler, Susan Johnson, Gary Margolis, "
                        "Jordan Young, and Annie Wilson, with two "
                        "further seats printed vacant -- the town "
                        "table's variance from the Secretary of "
                        "State's certified listing is noted; the "
                        "listing governs the election record.")],
            [holder("David Anderson", "david-anderson"),
             holder("Marjorie Drexler", "marjorie-drexler"),
             holder("Susan Johnson", "susan-johnson"),
             holder("Gary Margolis", "gary-margolis"),
             holder("Jordan Young", "jordan-young")]),
    ]
    jp = jp_election(
        "cornwall-vt", label, 5,
        "lists five Cornwall justices of the peace elected "
        "November 5, 2024: David Anderson, Marjorie Drexler, "
        "Susan Johnson, Gary Margolis, and Jordan Young. The "
        "listing publishes no vote totals or party labels and "
        "none are recorded.")
    return spec("cornwall", label, offices, jp)


SPECS.append(cornwall_spec())

# ---------------------------------------------------------------- Coventry
COV_SB = {
    "url": "https://coventryvt.org/select-board/",
    "note": "PLACEHOLDER",
}
COV_MINUTES = {
    "url": "https://coventryvt.org/wp-content/uploads/2026/03/2026-Town-Meeting-Minutes.pdf",
    "note": "PLACEHOLDER",
}
COV_REPORT = {
    "url": "https://coventryvt.org/wp-content/uploads/2024/02/web-coventry.pdf",
    "note": "PLACEHOLDER",
}


def cov_minutes(what):
    return S(COV_MINUTES, "Town of Coventry, 2026 Town Annual "
             f"Meeting Minutes (coventryvt.org): {what}")


def cov_report(what):
    return S(COV_REPORT, "Town of Coventry, 2023 Annual Report, "
             f"'Elected Officials' table (coventryvt.org): {what}")


def coventry_spec():
    label = "Town of Coventry"
    offices = [
        office(
            "selectboard", "Selectboard Member", "Coventry Selectboard", 3,
            [S(COV_SB, "Town of Coventry official website, Select "
                       "Board page: 'Select Board members: Kerry "
                       "Keement, Chair; Dan Webster; Matt Maxwell.' "
                       "The town's Town Contacts page prints the "
                       "same three."),
             cov_minutes("record the March 3, 2026 election of "
                         "Matthew Maxwell to a 3-year Selectboard "
                         "term (51 votes). A 2026 article to "
                         "increase the board from three to five "
                         "members failed (37-35), so the board "
                         "remains three. The Secretary of State "
                         "directory (June 5, 2026) publishes only "
                         "Maxwell's name for Coventry; the town's "
                         "own roster governs.")],
            [holder("Kerry Keement", "kerry-keement"),
             holder("Dan Webster", "dan-webster"),
             holder("Matthew Maxwell", "matthew-maxwell")]),
        office(
            "moderator", "Moderator", "Coventry Moderator", 1,
            [cov_minutes("record 'Town Moderator -- Matthew Maxwell "
                         "-- Elected' at the March 3, 2026 annual "
                         "meeting (1-year term).")],
            [holder("Matthew Maxwell", "matthew-maxwell")]),
        office(
            "town-clerk", "Town Clerk", "Coventry Town Clerk", 1,
            [cov_report("lists the Town Clerk, Deb Tanguay (term "
                        "to 2025), among the town's elected "
                        "officials."),
             guide("lists Deb Tanguay as Town Clerk of Coventry."),
             S({"url": "https://coventryvt.org/town-clerk/",
                "note": "PLACEHOLDER"},
               "Town of Coventry official website, Town Clerk "
               "page: 'Deb Tanguay, CMC, CVC -- Coventry Town "
               "Clerk.'")],
            [holder("Deb Tanguay", "deb-tanguay")]),
        office(
            "town-treasurer", "Town Treasurer", "Coventry Town Treasurer", 1,
            [S({"url": "https://coventryvt.org/town-treasurer/",
                "note": "PLACEHOLDER"},
               "Town of Coventry official website, Town Treasurer "
               "page: 'The Town Treasurer is hired by the Select "
               "Board' and names David Barlow as Treasurer. The "
               "holder is recorded as appointed."),
             guide("lists David Barlow as Town Treasurer of "
                   "Coventry.")],
            [holder("David Barlow", "david-barlow",
                    how_seated="appointed")]),
        office(
            "collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
            "Coventry Collector of Delinquent Taxes", 1,
            [cov_minutes("record the March 3, 2026 election of Deb "
                         "Tanguay as Delinquent Tax Collector "
                         "(68 votes, 1-year term).")],
            [holder("Deb Tanguay", "deb-tanguay")]),
        office(
            "first-constable", "First Constable", "Coventry First Constable", 1,
            [cov_minutes("record the March 3, 2026 election of "
                         "Donald Grondin as First Constable "
                         "(1-year term)."),
             S({"url": "https://coventryvt.org/constables/",
                "note": "PLACEHOLDER"},
               "Town of Coventry official website, Constables "
               "page: 'First Constable -- Donald \"Pedro\" "
               "Grondin.'")],
            [holder("Donald Grondin", "donald-grondin")]),
        office(
            "second-constable", "Second Constable",
            "Coventry Second Constable", 1,
            [cov_minutes("record the March 3, 2026 election of "
                         "Israel Sanville as Second Constable "
                         "(1-year term)."),
             S({"url": "https://coventryvt.org/constables/",
                "note": "PLACEHOLDER"},
               "Town of Coventry official website, Constables "
               "page: 'Second Constable -- Israel Sanville.'")],
            [holder("Israel Sanville", "israel-sanville")]),
        office(
            "cemetery-commissioner", "Cemetery Commissioner",
            "Coventry Cemetery Commission", 3,
            [S({"url": "https://coventryvt.org/cemetery-commission/",
                "note": "PLACEHOLDER"},
               "Town of Coventry official website, Cemetery "
               "Commission page ('2025 Cemetery Commission "
               "Members'): 'Chair -- Daniel Rondeau; Vice-Chair "
               "-- Renee Fortin; Secretary -- Alyssa Conn.'"),
             cov_minutes("record the March 3, 2026 election of "
                         "Alyssa Conn as Cemetery Commissioner "
                         "(2-year term).")],
            [holder("Daniel Rondeau", "daniel-rondeau"),
             holder("Renee Fortin", "renee-fortin"),
             holder("Alyssa Conn", "alyssa-conn")]),
        office(
            "trustee-of-cemetery-funds", "Trustee of Cemetery Funds",
            "Coventry Trustee of Cemetery Funds", 1,
            [cov_minutes("record the March 3, 2026 election of "
                         "Praneet Menon as Trustee of Cemetery "
                         "Funds (1-year term); the office is "
                         "distinct from the Trustees of Public "
                         "Funds, for which Coventry elects no "
                         "officer."),
             cov_report("lists 'Trustee of Cemetery Funds -- "
                        "Praneet Menon' among the elected "
                        "officials.")],
            [holder("Praneet Menon", "praneet-menon")]),
        office(
            "planning-commission", "Planning Commission Member",
            "Coventry Planning Commission", 5,
            [S({"url": "https://coventryvt.org/wp-content/uploads/2026/02/2026-Coventry-Town-Warning.pdf",
                "note": "PLACEHOLDER"},
               "Town of Coventry, 2026 annual meeting warning, "
               "Article 3: elects two Planning Commission members "
               "by Australian ballot (2-year terms) -- Coventry's "
               "Planning Commission is an elected body."),
             S({"url": "https://coventryvt.org/planning-commission/",
                "note": "PLACEHOLDER"},
               "Town of Coventry official website, Planning "
               "Commission page: Amanda Hussey (Chair), "
               "Stephanie Rondeau, Pedro Grondin, Carver "
               "Maxwell, and Israel Sanville."),
             cov_minutes("record the March 3, 2026 election of "
                         "Amanda Hussey and Donald Grondin as "
                         "Planning Commission members.")],
            [holder("Amanda Hussey", "amanda-hussey"),
             holder("Stephanie Rondeau", "stephanie-rondeau"),
             holder("Donald Grondin", "donald-grondin"),
             holder("Carver Maxwell", "carver-maxwell"),
             holder("Israel Sanville", "israel-sanville")]),
        office(
            "justice-of-the-peace", "Justice of the Peace",
            "Coventry Justices of the Peace", 7,
            [jp_src("lists seven Coventry justices of the peace: "
                    "Anita Allen, Sherylin Bradley, Melissa "
                    "Gallup, Donald P Hunt, Kerry L Keement, "
                    "Edward R Lovejoy, and Richard Lussier.")],
            [holder("Anita Allen", "anita-allen"),
             holder("Sherylin Bradley", "sherylin-bradley"),
             holder("Melissa Gallup", "melissa-gallup"),
             holder("Donald P. Hunt", "donald-p-hunt"),
             holder("Kerry Keement", "kerry-keement",
                    ballot_name="Kerry L Keement"),
             holder("Edward Lovejoy", "edward-lovejoy",
                    ballot_name="Edward R Lovejoy"),
             holder("Richard Lussier", "richard-lussier")]),
    ]
    jp = jp_election(
        "coventry-vt", label, 7,
        "lists seven Coventry justices of the peace elected "
        "November 5, 2024: Anita Allen, Sherylin Bradley, "
        "Melissa Gallup, Donald P Hunt, Kerry L Keement, Edward "
        "R Lovejoy, and Richard Lussier. The listing publishes "
        "no vote totals or party labels and none are recorded.")
    return spec("coventry", label, offices, jp)


SPECS.append(coventry_spec())

# ---------------------------------------------------------------- Craftsbury
CRA_REPORT = {
    "url": "https://craftsbury.gov/wp-content/uploads/sites/39/2026/02/final-town-report-1-27-2026-version5.pdf",
    "note": "PLACEHOLDER",
}
CRA_SB = {
    "url": "https://craftsbury.gov/boards/selectboard/",
    "note": "PLACEHOLDER",
}


def cra_report(what):
    return S(CRA_REPORT, "Town of Craftsbury, 2025 Annual Town "
             "Report, '2025 Craftsbury Elected Positions' roster "
             f"(craftsbury.gov): {what}")


def craftsbury_spec():
    label = "Town of Craftsbury"
    offices = [
        office(
            "selectboard", "Selectboard Member", "Craftsbury Selectboard", 3,
            [S(CRA_SB, "Town of Craftsbury official website, "
                       "Selectboard page: lists Bruce Urie "
                       "(Co-Chair), Jim Jones (Co-Chair), and "
                       "Alison Blaney, all elected to 3-year "
                       "terms."),
             cra_report("lists 'SELECT BOARD (3 year term): "
                        "James Jones (2026), Alison Blaney "
                        "(2027), Bruce Urie (2028)'; the town's "
                        "Certification of Votes for March 3, 2026 "
                        "records James Jones re-elected to the "
                        "3-year seat (114 votes). The Secretary "
                        "of State directory publishes no Craftsbury "
                        "roster.")],
            [holder("Alison Blaney", "alison-blaney"),
             holder("Bruce Urie", "bruce-urie"),
             holder("James Jones", "james-jones")]),
        office(
            "town-clerk", "Town Clerk", "Craftsbury Town Clerk", 1,
            [cra_report("lists 'TOWN CLERK & TREASURER (3 year "
                        "term): Michelle Warren (2028)' -- the "
                        "clerk and treasurer are elected as "
                        "combined offices."),
             guide("lists Michelle Warren as Town Clerk of "
                   "Craftsbury.")],
            [holder("Michelle Warren", "michelle-warren")]),
        office(
            "town-treasurer", "Town Treasurer", "Craftsbury Town Treasurer", 1,
            [cra_report("lists 'TOWN CLERK & TREASURER (3 year "
                        "term): Michelle Warren (2028)' -- the "
                        "clerk and treasurer are elected as "
                        "combined offices."),
             guide("lists Michelle Warren as Town Treasurer of "
                   "Craftsbury.")],
            [holder("Michelle Warren", "michelle-warren")]),
        office(
            "moderator", "Moderator", "Craftsbury Moderator", 1,
            [cra_report("lists 'MODERATOR (1 year term): Jeannine "
                        "Young (2026)'."),
             S({"url": "https://craftsbury.gov/departments/town-government-info/",
                "note": "PLACEHOLDER"},
               "Town of Craftsbury official website, Elected and "
               "Appointed Officers page, lists Jeannine Young as "
               "Moderator; the official Town Meeting Minutes of "
               "March 3, 2026 record her election as Moderator "
               "for 2026.")],
            [holder("Jeannine Young", "jeannine-young")]),
        office(
            "lister", "Lister", "Craftsbury Listers", 3,
            [S({"url": "https://craftsbury.gov/departments/listers/",
                "note": "PLACEHOLDER"},
               "Town of Craftsbury official website, Listers "
               "page: lists three elected Listers on 3-year "
               "terms: Harry Miller, Jeremiah McCann, and Tom "
               "Boyle."),
             cra_report("lists 'LISTER (3 year term): Tom Boyle "
                        "(2026), Harry Miller (2027), Jeremiah "
                        "McCann (2028)'.")],
            [holder("Tom Boyle", "tom-boyle"),
             holder("Harry Miller", "harry-miller"),
             holder("Jeremiah McCann", "jeremiah-mccann")]),
        office(
            "justice-of-the-peace", "Justice of the Peace",
            "Craftsbury Justices of the Peace", 5,
            [jp_src("lists five Craftsbury justices of the "
                    "peace: Yvette Brown, Timothy Fritz, Harry "
                    "H. Miller, David Rowell, and Allison Van "
                    "Akkeren.")],
            [holder("Yvette Brown", "yvette-brown"),
             holder("Timothy Fritz", "timothy-fritz"),
             holder("Harry Miller", "harry-miller",
                    ballot_name="Harry H. Miller"),
             holder("David Rowell", "david-rowell"),
             holder("Allison Van Akkeren", "allison-van-akkeren")]),
    ]
    jp = jp_election(
        "craftsbury-vt", label, 5,
        "lists five Craftsbury justices of the peace elected "
        "November 5, 2024: Yvette Brown, Timothy Fritz, Harry "
        "H. Miller, David Rowell, and Allison Van Akkeren. The "
        "listing publishes no vote totals or party labels and "
        "none are recorded.")
    return spec("craftsbury", label, offices, jp)


SPECS.append(craftsbury_spec())

# ---------------------------------------------------------------- Danby
DAN_REPORT = {
    "url": "https://www.danbyvt.org/_files/ugd/f9b078_998234b13f6048af95a8694db8088898.pdf",
    "note": "PLACEHOLDER",
}
DAN_CONTACT = {
    "url": "https://www.danbyvt.org/contact-us",
    "note": "PLACEHOLDER",
}


def dan_report(what):
    return S(DAN_REPORT, "Town of Danby, Annual Report 2025 "
             f"(danbyvt.org): {what}")


def danby_spec():
    label = "Town of Danby"
    offices = [
        office(
            "selectboard", "Selectboard Member", "Danby Selectboard", 5,
            [dan_report("the 'TOWN OFFICERS 2025' roster and the "
                        "Selectboard's own minutes (January-March "
                        "2026) seat five members: Bradley J. "
                        "Bender (Chairman), Greg Heaton, Kenneth "
                        "Abbott Jr., Steve Haines, and Tom Fuller "
                        "Jr. The Secretary of State directory "
                        "(June 5, 2026) publishes only Heaton for "
                        "Danby and styles him Chairman; the town's "
                        "minutes show Bender chairing, and the "
                        "directory entry is stale in that respect.")],
            [holder("Bradley J. Bender", "bradley-bender"),
             holder("Greg Heaton", "greg-heaton"),
             holder("Kenneth Abbott Jr.", "kenneth-abbott-jr"),
             holder("Steve Haines", "steve-haines"),
             holder("Tom Fuller Jr.", "tom-fuller-jr")]),
        office(
            "town-clerk", "Town Clerk", "Danby Town Clerk", 1,
            [guide("lists Janice Arnold as Town Clerk of Danby."),
             dan_report("the 'TOWN OFFICERS 2025' roster reads "
                        "'TOWN CLERK -- Janice Arnold -- 3 year "
                        "term exp 2026'."),
             S(DAN_CONTACT, "Town of Danby official website, "
                            "Contact Us page (current): 'Janice "
                            "Arnold, Town Clerk.' No published "
                            "2026 clerk tally was located; the "
                            "town's live page presents Arnold as "
                            "the sitting clerk.")],
            [holder("Janice Arnold", "janice-arnold")]),
        office(
            "town-treasurer", "Town Treasurer", "Danby Town Treasurer", 1,
            [dan_report("the signed 2026 annual meeting warning "
                        "(printed in the report) warned a Town "
                        "Treasurer election for a 3-year term; "
                        "the official March 3, 2026 ballot printed "
                        "Katlyn Parker as the only candidate, and "
                        "the town's 2026 results tally records "
                        "her elected."),
             S(DAN_CONTACT, "Town of Danby official website, "
                            "Contact Us page: 'Katlyn Parker, "
                            "Town Treasurer.' Selectboard minutes "
                            "of April 9 and June 11, 2026 carry "
                            "'Treasurer's Report -- Katlyn "
                            "Parker.' The Secretary of State Guide "
                            "(January 2026) names Michelle Bushee, "
                            "who no longer holds the office.")],
            [holder("Katlyn Parker", "katlyn-parker")]),
        office(
            "moderator", "Moderator", "Danby Moderator", 1,
            [dan_report("the 'TOWN OFFICERS 2025' roster lists "
                        "the Moderator as Dan Garceau (1-year "
                        "term), and the town's March 3, 2026 "
                        "results tally records him elected "
                        "Moderator for 2026.")],
            [holder("Daniel Garceau", "daniel-garceau")]),
        office(
            "lister", "Lister", "Danby Listers", 3,
            [dan_report("the 'TOWN OFFICERS 2025' roster lists "
                        "three elected Listers: Maureen Staples "
                        "(term expiring 2027), Marvin Gates "
                        "(2028), and Byron Battease (2026); the "
                        "official March 3, 2026 ballot and "
                        "results tally record Battease re-elected."),
             S(DAN_CONTACT, "Town of Danby official website, "
                            "Contact Us page: 'Board of Listers "
                            "(Assessors) ... Maureen Staples-Lead "
                            "Lister; Marvin Gates; Byron "
                            "Battease.'")],
            [holder("Byron Battease", "byron-battease"),
             holder("Maureen Staples", "maureen-staples"),
             holder("Marvin Gates", "marvin-gates")]),
        office(
            "auditor", "Auditor", "Danby Auditors", 3,
            [dan_report("the 'TOWN OFFICERS 2025' roster lists "
                        "Auditors Lonna Burden (3-year term "
                        "expiring 2029), Sarah Wilde (expiring "
                        "2028), and Tara Goodell (1-year "
                        "appointed seat, 2026). Selectboard "
                        "minutes of April 9, 2026 record the "
                        "board accepting Wilde's resignation "
                        "(effective March 17, 2026) and "
                        "appointing Bill Payne and Tom Johnston "
                        "as Town Auditors until Town Meeting "
                        "2027; the two appointed holders are "
                        "recorded as appointed, and Goodell's "
                        "superseded one-year roster line is not "
                        "carried forward.")],
            [holder("Lonna Burden", "lonna-burden"),
             holder("Bill Payne", "bill-payne", how_seated="appointed"),
             holder("Tom Johnston", "tom-johnston",
                    how_seated="appointed")]),
        office(
            "collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
            "Danby Collector of Delinquent Taxes", 1,
            [dan_report("the 'TOWN OFFICERS 2025' roster lists "
                        "the Delinquent Tax Collector as Douglas "
                        "R. White (1-year term); the official "
                        "March 3, 2026 ballot printed his name "
                        "for the office and the results tally "
                        "records him elected.")],
            [holder("Douglas R. White", "douglas-r-white")]),
        office(
            "trustees-of-public-funds", "Trustee of Public Funds",
            "Danby Trustees of Public Funds", 3,
            [dan_report("the 'TOWN OFFICERS 2025' roster lists "
                        "three Trustees of Public Funds: Shelley "
                        "Taylor (term expiring 2026), Bradley J. "
                        "Bender (2027), and Hilda Haines (2028); "
                        "the town's March 3, 2026 results tally "
                        "records Taylor re-elected.")],
            [holder("Shelley Taylor", "shelley-taylor"),
             holder("Bradley J. Bender", "bradley-bender"),
             holder("Hilda Haines", "hilda-haines")]),
        office(
            "cemetery-commissioner", "Cemetery Commissioner",
            "Danby Cemetery Commission", 5,
            [dan_report("the 'TOWN OFFICERS 2025' roster lists "
                        "five Cemetery Commissioners on 5-year "
                        "terms: Netanel Crispe (expiring 2028), "
                        "James Viscusi (2028), Roger Bromley "
                        "(2029), Hilda Haines (2029), and "
                        "Shelley Taylor (2030). No commissioner's "
                        "term expired in 2026.")],
            [holder("Netanel Crispe", "netanel-crispe"),
             holder("Roger Bromley", "roger-bromley"),
             holder("Hilda Haines", "hilda-haines"),
             holder("James Viscusi", "james-viscusi"),
             holder("Shelley Taylor", "shelley-taylor")]),
        office(
            "justice-of-the-peace", "Justice of the Peace",
            "Danby Justices of the Peace", 5,
            [jp_src("lists five Danby justices of the peace: "
                    "Bradley J. Bender, Zachary Fuller, Daniel "
                    "Garceau, Terry J. Hosley II, and Collette "
                    "Yrsha.")],
            [holder("Bradley J. Bender", "bradley-bender"),
             holder("Zachary Fuller", "zachary-fuller"),
             holder("Daniel Garceau", "daniel-garceau"),
             holder("Terry J. Hosley II", "terry-hosley"),
             holder("Collette Yrsha", "collette-yrsha")]),
    ]
    jp = jp_election(
        "danby-vt", label, 5,
        "lists five Danby justices of the peace elected "
        "November 5, 2024: Bradley J. Bender, Zachary Fuller, "
        "Daniel Garceau, Terry J. Hosley II, and Collette "
        "Yrsha. The listing publishes no vote totals or party "
        "labels and none are recorded.")
    return spec("danby", label, offices, jp)


SPECS.append(danby_spec())

# ---------------------------------------------------------------- Danville
DVL_SITE = {
    "url": "https://danvillevt.gov",
    "note": "PLACEHOLDER",
}
DVL_CH = {
    "url": "https://legislature.vermont.gov/statutes/section/24APPENDIX/114/00101",
    "note": "PLACEHOLDER",
}


def dvl_site(what):
    return S(DVL_SITE, "Town of Danville official website "
             f"(danvillevt.gov): {what}")


def danville_spec():
    label = "Town of Danville"
    offices = [
        office(
            "selectboard", "Selectboard Member", "Danville Selectboard", 5,
            [sb_dir("lists five Danville Selectboard members: Eric "
                    "Bach, Kristen Calkins, Matt Choate, Alison "
                    "Low, and Janice Ouellette (the directory "
                    "spells Calkins 'Kristin'; the town's own "
                    "records print Kristen)."),
             dvl_site("the clerk-signed 'Results of Officers "
                      "Elected' for March 3, 2026 and Selectboard "
                      "minutes, March-October 2026, seat the "
                      "same five, with Alison Low as Chair and "
                      "Eric Bach as Vice Chair; Bach and Calkins "
                      "were elected in 2026.")],
            [holder("Alison Low", "alison-low"),
             holder("Eric Bach", "eric-bach"),
             holder("Matt Choate", "matt-choate"),
             holder("Janice Ouellette", "janice-ouellette"),
             holder("Kristen Calkins", "kristen-calkins")]),
        office(
            "town-clerk", "Town Clerk", "Danville Town Clerk", 1,
            [dvl_site("the town clerk's page and the town roster "
                      "name Michelle Leclerc as Town Clerk, "
                      "elected to a term running to 2027."),
             guide("lists Michelle Leclerc as Town Clerk of "
                   "Danville.")],
            [holder("Michelle Leclerc", "michelle-leclerc")]),
        office(
            "town-treasurer", "Town Treasurer", "Danville Town Treasurer", 1,
            [dvl_site("the town roster names Michelle Leclerc as "
                      "Town Treasurer, elected to a term running "
                      "to 2027; the treasurer collects the "
                      "town's delinquent taxes, so no separate "
                      "collector office exists."),
             guide("lists Michelle Leclerc as Town Treasurer of "
                   "Danville.")],
            [holder("Michelle Leclerc", "michelle-leclerc")]),
        office(
            "moderator", "Moderator", "Danville Moderator", 1,
            [dvl_site("Selectboard minutes and the town roster "
                      "name Eric Bach as Moderator, elected "
                      "annually.")],
            [holder("Eric Bach", "eric-bach")]),
        office(
            "lister", "Lister", "Danville Listers", 2,
            [dvl_site("the town roster and the March 3, 2026 "
                      "'Results of Officers Elected' agree that "
                      "Danville's Board of Listers has TWO "
                      "members: Sharon Langford (term expiring "
                      "2029) and Ellen Woodward (term expiring "
                      "2028). The post is modeled with two "
                      "seats, as the town's own records fix "
                      "them.")],
            [holder("Sharon Langford", "sharon-langford"),
             holder("Ellen Woodward", "ellen-woodward")]),
        office(
            "auditor", "Auditor", "Danville Auditors", 3,
            [dvl_site("the clerk-signed 'Results of Officers "
                      "Elected' for March 3, 2026 records Andrew "
                      "Grout elected Auditor (term expiring "
                      "2029); the town roster prints a second "
                      "seat as 'Vacant' and the 2026 warning "
                      "carried a regular auditor seat and a "
                      "vacancy seat. The remaining seats are "
                      "left unfilled.")],
            [holder("Andrew Grout", "andrew-grout")]),
        office(
            "constable", "Constable", "Danville Constable", 1,
            [dvl_site("the town roster names Matt Choate as "
                      "Constable (term expiring 2029).")],
            [holder("Matt Choate", "matt-choate")]),
        office(
            "trustees-of-public-funds", "Trustee of Public Funds",
            "Danville Trustees of Public Funds", 3,
            [dvl_site("the office appears in the town's roster "
                      "and the 2026 warning. Structure only: no "
                      "official source publishes the current "
                      "holders; the seats are left unfilled "
                      "rather than guessed.")]),
        office(
            "cemetery-commissioner", "Cemetery Commissioner",
            "Danville Cemetery Commission", 5,
            [dvl_site("the office appears in the town's roster "
                      "and the 2026 warning (a five-member "
                      "commission). Structure only: no official "
                      "source publishes the current holders; "
                      "the seats are left unfilled rather than "
                      "guessed.")]),
        office(
            "library-trustee", "Library Trustee",
            "Danville Pope Memorial Library Trustees", 5,
            [dvl_site("the office (Pope Memorial Library "
                      "trustees, five seats) appears in the "
                      "town's roster and the 2026 warning. "
                      "Structure only: no official source "
                      "publishes the current holders; the seats "
                      "are left unfilled rather than guessed.")]),
        office(
            "grand-juror", "Grand Juror", "Danville Grand Juror", 1,
            [dvl_site("the office appears in the town's roster "
                      "and the 2026 warning. Structure only: no "
                      "official source publishes the current "
                      "holder; the seat is left unfilled rather "
                      "than guessed.")]),
        office(
            "justice-of-the-peace", "Justice of the Peace",
            "Danville Justices of the Peace", 10,
            [jp_src("lists ten Danville justices of the peace: "
                    "Eric Bach, Matthew Choate, Barbara Hawley, "
                    "Libby Hillhouse, Virginia Incerpi, Julie "
                    "Larrabee, Bruce Melendy, Jenny Rafuse, "
                    "Phyllis Kehley Sweeney, and Brittany "
                    "Larrabee Wilson.")],
            [holder("Eric Bach", "eric-bach"),
             holder("Matt Choate", "matt-choate",
                    ballot_name="Matthew Choate"),
             holder("Barbara Hawley", "barbara-hawley"),
             holder("Libby Hillhouse", "libby-hillhouse"),
             holder("Virginia Incerpi", "virginia-incerpi"),
             holder("Julie Larrabee", "julie-larrabee"),
             holder("Bruce Melendy", "bruce-melendy"),
             holder("Jenny Rafuse", "jenny-rafuse"),
             holder("Phyllis Kehley Sweeney", "phyllis-kehley-sweeney"),
             holder("Brittany Larrabee Wilson",
                    "brittany-larrabee-wilson")]),
    ]
    jp = jp_election(
        "danville-vt", label, 10,
        "lists ten Danville justices of the peace elected "
        "November 5, 2024: Eric Bach, Matthew Choate, Barbara "
        "Hawley, Libby Hillhouse, Virginia Incerpi, Julie "
        "Larrabee, Bruce Melendy, Jenny Rafuse, Phyllis Kehley "
        "Sweeney, and Brittany Larrabee Wilson. The listing "
        "publishes no vote totals or party labels and none are "
        "recorded.")
    return spec("danville", label, offices, jp)


SPECS.append(danville_spec())

# ---------------------------------------------------------------- emit
for s in SPECS:
    path = OUT / f"{s['place_slug']}.json"
    path.write_text(json.dumps(s, indent=2) + "\n")
    print(f"wrote {path.name}: {len(s['offices'])} offices")
print(f"{len(SPECS)} specs")
