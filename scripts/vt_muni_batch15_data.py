#!/usr/bin/env python3
"""Batch 15 of the VT #163 municipal fan-out (alphabetical positions
140-149): Milton, Monkton, Montgomery, Montpelier (city),
Moretown, Morgan, Morristown, Morrisville (village), Mount
Holly, Mount Tabor. Emits one JSON spec per municipality for
build_vt_municipality.py. Research: vt_muni_batch15_research.md.

Identity calls baked into this batch (all flagged on #163):
- Milton's Leland Morgan and Michael R. Morgan (Selectboard +
  JP) ARE the two Grand Isle-Chittenden state representatives
  (Leland's legislature bio gives his address as 23 Morgan
  Rd., Milton -- the JP listing's address -- and Michael's
  profile lists the Milton Select Board and JP seats); Milton
  JP Brenda Steady IS the Chittenden-25 representative
  (Milton's own district); Montpelier JP Conor Casey IS the
  Washington-4 representative (Montpelier's district); Morgan
  Selectboard member Larry Labor IS the Essex-Orleans
  representative (his bio: elected to the Morgan select board
  in 2009 and continues in the role); Moretown Selectboard
  member Callie Streeter IS Berlin's appointed treasurer in
  the existing municipal record (hired Nov 1, 2023, while
  serving on Moretown's board since 2018). All five reuse the
  existing person records; JP candidacies for the four JP
  reuses are appended by hand.
- Monkton's JP slate is the town's TEN (its Directory of Town
  Officials, in both the 2025 town report and the Aug 24, 2026
  standalone directory), not the SOS listing's partial five;
  Moretown's JP slate is the town report's SEVEN (a superset
  of the listing's four). Both divergences are stated in the
  election notes.
- Montgomery rests on the town's official Elected & Appointed
  Officer List updated March 11, 2026 (its two cemetery
  commissions are modeled as separate posts; its elected Fire
  Commissioners join the standing fire-officers scope
  question and are not modeled).
- Montpelier District 1 Councilor Paul Costello was APPOINTED
  by the Council on August 12, 2026 to fill Adrienne Gil's
  vacancy (charter sec. 303; Gil not minted); its Green Mount
  Cemetery Commission is structure-only (the commission page's
  roster is inconsistent with the three cemetery seats that
  stood in March 2026 and the outcomes are unpublished).
- Morristown's lister Kevin Petrochko was appointed May 5,
  2025 (the town report's officers page), and its DTC Sara
  Haskins is a Selectboard appointee (the report's Appointed
  Officers page); its JP roster divergence (the report's Jane
  Foster / Aimee Towne vs the listing's Charles Burnham /
  Roland Billings) is held as a straggler -- the listing
  governs the election.
- Mount Holly's Treasurer Marc Miller was appointed May 20,
  2026 to complete resigned Treasurer Liz Karle's term (Karle
  not minted).
- Mount Tabor is an SOS-spine build (no town website): its
  Selectboard is structure-only because the June 2026 SOS
  directory carries a single row, "R. Gasperetti", that does
  not distinguish Robert Gasperetti from R. Matthew
  Gasperetti III, and its Treasurer is structure-only because
  the Guide's William Basso II is superseded as clerk by the
  June 2026 spreadsheet's Noel Weeks.
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
CHARTER_129 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/129",
    "note": "PLACEHOLDER",
}
CHARTER_005 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/005",
    "note": "PLACEHOLDER",
}
CHARTER_245 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/245",
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


def charter129(phrase):
    return S(CHARTER_129, f"24 App. V.S.A. ch. 129 (Town of "
             f"Milton): {phrase}")


def charter005(phrase):
    return S(CHARTER_005, f"24 App. V.S.A. ch. 005 (City of "
             f"Montpelier): {phrase}")


def charter245(phrase):
    return S(CHARTER_245, f"24 App. V.S.A. ch. 245 (Village of "
             f"Morrisville): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 15); issue #163 "
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
                  f"# municipal fan-out batch 15; issue #163 "
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
ORDER = ["milton", "monkton", "montgomery", "montpelier",
         "moretown", "morgan", "morristown", "morrisville",
         "mount-holly", "mount-tabor"]

# ------------------------------------------------------------ Milton
MILTON_SB = {
    "url": "https://www.miltonvt.gov/259/Selectboard",
    "note": "PLACEHOLDER",
}
MILTON_DIR = {
    "url": "https://www.miltonvt.gov/Directory.aspx",
    "note": "PLACEHOLDER",
}
MILTON_LIB_JUN = {
    "url": "https://miltonvt.gov/AgendaCenter/ViewFile/Minutes/_06022026-1364",
    "note": "PLACEHOLDER",
}
MILTON_LIB_MAR = {
    "url": "https://www.miltonvt.gov/AgendaCenter/ViewFile/Minutes/_03242026-1334",
    "note": "PLACEHOLDER",
}
CWD_PACKET = {
    "url": "https://www.champlainwater.org/DocumentCenter/View/565/February-17-2026-Regular-Meeting-Packet?bidId=",
    "note": "PLACEHOLDER",
}
CWD_AR = {
    "url": "https://www.champlainwater.org/ArchiveCenter/ViewFile/Item/96",
    "note": "PLACEHOLDER",
}
LELAND_BIO = {
    "url": "https://legislature.vermont.gov/people/single/2022/30960",
    "note": "PLACEHOLDER",
}


def milton_sb(what):
    return S(MILTON_SB, "Town of Milton (official website), "
             f"Selectboard page: {what}")


def milton_dir(what):
    return S(MILTON_DIR, "Town of Milton (official website), staff "
             f"directory: {what}")


def milton_lib_jun(what):
    return S(MILTON_LIB_JUN, "Milton Public Library Board of "
             "Trustees minutes, June 2, 2026 (Town of Milton "
             f"AgendaCenter): {what}")


def milton_lib_mar(what):
    return S(MILTON_LIB_MAR, "Milton Public Library Board of "
             "Trustees minutes, March 24, 2026 (Town of Milton "
             f"AgendaCenter): {what}")


def cwd_packet(what):
    return S(CWD_PACKET, "Champlain Water District, February 17, "
             f"2026 regular meeting packet (including the January "
             f"20, 2026 meeting minutes): {what}")


def cwd_ar(what):
    return S(CWD_AR, "Champlain Water District, 2021-2022 Annual "
             f"Report: {what}")


def leland_bio(what):
    return S(LELAND_BIO, "Vermont General Assembly, Representative "
             f"Leland Morgan's member page and biography: {what}")


def milton_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Milton Selectboard", 5,
               [milton_sb("lists the five selectboard members as "
                          "Darren Adams (Chair), Michael Morgan "
                          "(Vice Chair), Diane Barrows (Clerk of "
                          "the board), Leland Morgan, and Betsy "
                          "Paret"),
                sb_dir("lists Milton's selectboard as Darren Adams "
                       "(Chair), Diane Barrows, Leland Morgan, and "
                       "Michael Morgan (Vice Chair), with one "
                       "further member"),
                charter129("section 202(a)(1) provides for five "
                           "selectpersons elected at the annual "
                           "meeting")],
               [holder("Darren Adams", "darren-adams"),
                holder("Michael R. Morgan", "michael-r-morgan",
                       existing_person_id="ocd-person/e9596971-4e07-5be8-a234-56f1d050fa57"),
                holder("Diane Barrows", "diane-barrows"),
                holder("Leland Morgan", "leland-morgan",
                       existing_person_id="ocd-person/33cec211-04ab-525a-b7b7-391704133e10"),
                holder("Betsy Paret", "betsy-paret")]),
        office("town-clerk", "Town Clerk",
               "Milton Town Clerk", 1,
               [charter129("sections 202(a)(2) and 203(b) provide "
                           "for a Town Clerk elected for a "
                           "three-year term"),
                milton_dir("lists Kristin Beers as Town Clerk"),
                clerk_xlsx("lists Kristin Beers as Milton's town "
                           "clerk"),
                guide("names Kristin Beers as Milton's town clerk")],
               [holder("Kristin Beers", "kristin-beers")]),
        office("town-treasurer", "Town Treasurer",
               "Milton Town Treasurer", 1,
               [charter129("sections 202(a)(3) and 203(c) provide "
                           "for a Town Treasurer elected for a "
                           "three-year term"),
                milton_dir("lists John Gifford as Town Treasurer"),
                treas_xlsx("lists John C. Gifford as Milton's town "
                           "treasurer"),
                guide("names John C. Gifford as Milton's town "
                      "treasurer")],
               [holder("John C. Gifford", "john-gifford")]),
        office("library-trustee", "Library Trustee",
               "Milton Public Library", 5,
               [charter129("sections 202(a)(4) and 203(d) provide "
                           "for five elected Library Trustees"),
                milton_lib_jun("lists the trustees as Cathy "
                               "Vadnais (Chair), Henry Bonges "
                               "(Vice Chair), Beth Bouchard "
                               "(Treasurer), Gillian Taylor "
                               "(Secretary), and Joe Duquette"),
                milton_lib_mar("lists the same five trustees: "
                               "Vadnais, Bonges, Bouchard, Taylor, "
                               "and Duquette")],
               [holder("Cathy Vadnais", "cathy-vadnais"),
                holder("Henry Bonges", "henry-bonges"),
                holder("Beth Bouchard", "beth-bouchard"),
                holder("Gillian Taylor", "gillian-taylor"),
                holder("Joe Duquette", "joe-duquette")]),
        office("champlain-water-district-representative",
               "Champlain Water District Representative",
               "Champlain Water District", 1,
               [charter129("sections 202(a)(6) and 203(f) provide "
                           "for a Champlain Water District "
                           "Representative elected for a three-year "
                           "term"),
                cwd_packet("the District's January 20, 2026 "
                           "regular meeting minutes list John "
                           "Gifford, Milton, among the "
                           "commissioners present"),
                cwd_ar("the report's board table names John "
                       "Gifford as the Town of Milton's "
                       "commissioner (Lisa Schaeffler, alternate)")],
               [holder("John C. Gifford", "john-gifford")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Milton Justices of the Peace", 15,
               [jp_src("lists fifteen Milton justices of the peace "
                       "elected November 5, 2024"),
                leland_bio("Representative Leland Morgan's "
                           "biography gives his mailing address as "
                           "23 Morgan Rd., Milton -- the address "
                           "the justice of the peace listing prints "
                           "for Leland Morgan -- and states he is "
                           "presently a Justice of the Peace; the "
                           "Milton justice of the peace membership "
                           "reuses his existing person record")],
               [holder("Charles Barsalow", "charles-barsalow"),
                holder("Jean Ann Branch", "jean-ann-branch"),
                holder("Steve Burke", "steve-burke"),
                holder("Kevin Endres", "kevin-endres"),
                holder("Mary Ann Duffy Godin",
                       "mary-ann-duffy-godin"),
                holder("Reginald Godin", "reginald-godin"),
                holder("Denise Hughes", "denise-hughes"),
                holder("Jon P. Hughes", "jon-p-hughes"),
                holder("Leland Morgan", "leland-morgan",
                       existing_person_id="ocd-person/33cec211-04ab-525a-b7b7-391704133e10"),
                holder("Michael R. Morgan", "michael-r-morgan",
                       ballot_name="Michael Morgan",
                       existing_person_id="ocd-person/e9596971-4e07-5be8-a234-56f1d050fa57"),
                holder("Wendell Noble", "wendell-noble"),
                holder("Lonnie Poland", "lonnie-poland"),
                holder("Brenda Steady", "brenda-steady",
                       existing_person_id="ocd-person/13210973-ba5b-581d-9bc9-16e0e5f10e07"),
                holder("Kary Towne", "kary-towne"),
                holder("Robin Woods-Brisson",
                       "robin-woods-brisson")]),
    ]
    jp = jp_election(
        "milton-vt", "Town of Milton", 15,
        "lists fifteen Milton justices of the peace elected "
        "November 5, 2024: Charles Barsalow, Jean Ann Branch, "
        "Steve Burke, Kevin Endres, Mary Ann Duffy Godin, "
        "Reginald Godin, Denise Hughes, Jon P. Hughes, Leland "
        "Morgan, Michael Morgan, Wendell Noble, Lonnie Poland, "
        "Brenda Steady, Kary Towne, and Robin Woods-Brisson. "
        "The listing publishes no vote totals or party labels "
        "and none are recorded")
    return spec("milton", "Town of Milton", offices, jp)


SPECS["milton"] = milton_spec()

# ------------------------------------------------------------ Monkton
MONKTON_DIR_PDF = {
    "url": "https://monktonvt.com/wp-content/uploads/2026/08/Monkton-Directory-of-Town-Officials-08-24-26.xlsx-List-for-Town-Website.pdf",
    "note": "PLACEHOLDER",
}
MONKTON_RESULTS = {
    "url": "https://monktonvt.com/2026/03/03/march-3-2026-monkton-municipal-election-results/",
    "note": "PLACEHOLDER",
}
MONKTON_REPORT = {
    "url": "https://monktonvt.com/wp-content/uploads/2026/02/75775c60d785ff48f0ea1c6a9120958d.pdf",
    "note": "PLACEHOLDER",
}


def monkton_dir(what):
    return S(MONKTON_DIR_PDF, "Town of Monkton (official website), "
             "Directory of Town Officials (updated August 24, "
             f"2026): {what}")


def monkton_results(what):
    return S(MONKTON_RESULTS, "Town of Monkton (official website), "
             f"March 3, 2026 municipal election results: {what}")


def monkton_report(what):
    return S(MONKTON_REPORT, "Town of Monkton, 2025 Annual Town "
             f"Report, Directory of Town Officials: {what}")


def monkton_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Monkton Selectboard", 5,
               [monkton_dir("lists the five selectboard members as "
                            "Sam Peisch (Chair), John Dunham "
                            "(Vice Chair), Walter Crandall, Sarah "
                            "Bouchard, and Joseph Szarejko, all "
                            "elected"),
                monkton_results("Sam Peisch was re-elected with "
                                "371 votes and Walter Crandall "
                                "with 357 votes"),
                sb_dir("lists Sam Peisch among Monkton's "
                       "selectboard members")],
               [holder("Sam Peisch", "sam-peisch"),
                holder("John Dunham", "john-dunham"),
                holder("Walter Crandall", "walter-crandall"),
                holder("Sarah Bouchard", "sarah-bouchard"),
                holder("Joseph Szarejko", "joseph-szarejko")]),
        office("town-clerk", "Town Clerk",
               "Monkton Town Clerk", 1,
               [monkton_dir("lists Sharon Gomez as Town Clerk, "
                            "elected to a one-year term"),
                monkton_results("Sharon Gomez was elected Town "
                                "Clerk with 415 votes"),
                clerk_xlsx("lists Sharon Gomez as Monkton's town "
                           "clerk"),
                guide("names Sharon Gomez as Monkton's town "
                      "clerk")],
               [holder("Sharon Gomez", "sharon-gomez")]),
        office("town-treasurer", "Town Treasurer",
               "Monkton Town Treasurer", 1,
               [monkton_dir("lists Kim Barbour as Town Treasurer, "
                            "appointed by the Selectboard"),
                treas_xlsx("lists Kim Barbour as Monkton's town "
                           "treasurer"),
                monkton_report("lists William Joos as the "
                               "appointed Town Treasurer for "
                               "2025-2026; the August 2026 "
                               "directory shows Barbour succeeded "
                               "him in the appointed office, and "
                               "the membership is recorded as "
                               "appointed")],
               [holder("Kim Barbour", "kim-barbour",
                       how_seated="appointed")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Monkton Collector of Delinquent Taxes", 1,
               [monkton_dir("lists Kim Barbour as Collector of "
                            "Delinquent Taxes, appointed by the "
                            "Selectboard")],
               [holder("Kim Barbour", "kim-barbour",
                       how_seated="appointed")]),
        office("moderator", "Moderator",
               "Monkton Moderator", 1,
               [monkton_dir("lists Jerry Schwarz as Town "
                            "Moderator, elected"),
                monkton_results("Jerry Schwarz was elected "
                                "Moderator with 384 votes")],
               [holder("Jerry Schwarz", "jerry-schwarz")]),
        office("auditor", "Auditor",
               "Monkton Auditors", 3,
               [monkton_dir("lists the three auditors as Janet "
                            "Cassarino, Robin Huizenga, and "
                            "Randall Charboneau, all elected"),
                monkton_results("Janet Cassarino was elected "
                                "auditor with 380 votes")],
               [holder("Janet Cassarino", "janet-cassarino"),
                holder("Robin Huizenga", "robin-huizenga"),
                holder("Randall Charboneau",
                       "randall-charboneau")]),
        office("constable", "Constable",
               "Monkton Constable", 1,
               [monkton_dir("lists the constable office as "
                            "elected to a one-year term and "
                            "marked '** Open **' -- no holder is "
                            "published, so the post is created "
                            "without a membership"),
                monkton_results("the 2026 results post shows the "
                                "constable line blank")]),
        office("planning-commissioner", "Planning Commissioner",
               "Monkton Planning Commission", 7,
               [monkton_dir("lists the seven planning "
                            "commissioners as Ivor Hughes, Debra "
                            "Sprague, Stephen Pilcher, Sam Burr, "
                            "Adam Miller, Marilyn Cargill, and "
                            "Wendy Sue Harper, all elected to "
                            "three-year terms"),
                monkton_results("Marilyn Cargill (372 votes) and "
                                "Wendy Sue Harper (370) were "
                                "elected to three-year terms and "
                                "Stephen Pilcher (354) to a "
                                "two-year remainder")],
               [holder("Ivor Hughes", "ivor-hughes"),
                holder("Debra Sprague", "debra-sprague"),
                holder("Stephen Pilcher", "stephen-pilcher"),
                holder("Sam Burr", "sam-burr"),
                holder("Adam Miller", "adam-miller"),
                holder("Marilyn Cargill", "marilyn-cargill"),
                holder("Wendy Sue Harper", "wendy-sue-harper")]),
        office("library-trustee", "Library Trustee",
               "Russell Memorial Library", 5,
               [monkton_dir("lists the five Russell Memorial "
                            "Library trustees as Cynthia Walcott, "
                            "Ashley Haefele, Samuel Ludwig, Janet "
                            "Fairchild, and Theresa Schwegel, all "
                            "elected to three-year terms"),
                monkton_results("Janet Fairchild (367 votes) and "
                                "Theresa Schwegel (369) were "
                                "elected library trustees"),
                monkton_report("lists Adam McGowan as a library "
                               "trustee for 2025-2028; the "
                               "August 2026 directory seats "
                               "Haefele in the current five")],
               [holder("Cynthia Walcott", "cynthia-walcott"),
                holder("Ashley Haefele", "ashley-haefele"),
                holder("Samuel Ludwig", "samuel-ludwig"),
                holder("Janet Fairchild", "janet-fairchild"),
                holder("Theresa Schwegel", "theresa-schwegel")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Monkton Justices of the Peace", 10,
               [monkton_dir("lists ten justices of the peace, "
                            "each marked 'Elected (November "
                            "Election)' for a two-year term "
                            "February 2025 - January 2027: Kristen "
                            "Blanchette, Lynne Caulfield, Jane "
                            "Low, Kathy Malzac, Renee McGuiness, "
                            "Amy Moody, Norma Norris, Jerry "
                            "Schwarz, Gail Vansteamberg, and "
                            "William Vansteamberg"),
                monkton_report("the 2025 Annual Town Report's "
                               "Directory of Town Officials lists "
                               "the same ten justices of the "
                               "peace, all elected, two-year "
                               "terms 2/25 - 1/27"),
                jp_src("the Monkton block lists only five "
                       "justices of the peace (Jane B. Low, "
                       "Kathy Malzac, Jerry Schwarz, Kenneth "
                       "Wheeling, and Valerie Mullin); the "
                       "town's two concordant directories "
                       "govern -- see the election note")],
               [holder("Kristen Blanchette",
                       "kristen-blanchette"),
                holder("Lynne Caulfield", "lynne-caulfield"),
                holder("Jane Low", "jane-low"),
                holder("Kathy Malzac", "kathy-malzac"),
                holder("Renee McGuiness", "renee-mcguiness"),
                holder("Amy Moody", "amy-moody"),
                holder("Norma Norris", "norma-norris"),
                holder("Jerry Schwarz", "jerry-schwarz"),
                holder("Gail Vansteamberg",
                       "gail-vansteamberg"),
                holder("William Vansteamberg",
                       "william-vansteamberg")]),
    ]
    jp = jp_election(
        "monkton-vt", "Town of Monkton", 10,
        "the Monkton block lists only five justices of the "
        "peace: Jane B. Low, Kathy Malzac, Jerry Schwarz, "
        "Kenneth Wheeling, and Valerie Mullin. The Town of "
        "Monkton's own Directory of Town Officials -- in both "
        "the 2025 Annual Town Report and the standalone "
        "directory updated August 24, 2026 -- lists TEN "
        "justices of the peace, each marked 'Elected (November "
        "Election)' for the two-year term February 2025 to "
        "January 2027: Kristen Blanchette, Lynne Caulfield, "
        "Jane Low, Kathy Malzac, Renee McGuiness, Amy Moody, "
        "Norma Norris, Jerry Schwarz, Gail Vansteamberg, and "
        "William Vansteamberg. The town's two concordant "
        "directories govern and the ten are recorded as the "
        "winners; Wheeling and Mullin appear in no town source "
        "and are not recorded as holders. The listing "
        "publishes no vote totals or party labels and none "
        "are recorded",
        [monkton_dir("lists the ten justices of the peace "
                     "named in the election note, each marked "
                     "elected at the November election"),
         monkton_report("the 2025 Annual Town Report's "
                        "directory lists the same ten justices "
                        "of the peace")])
    return spec("monkton", "Town of Monkton", offices, jp)


SPECS["monkton"] = monkton_spec()

# ------------------------------------------------------------ Montgomery
MONTG_OFFICERS = {
    "url": "https://montgomeryvt.us/wp-content/uploads/2026/03/Officer-List.-updated-as-of-3.11.26.pdf",
    "note": "PLACEHOLDER",
}


def montg_officers(what):
    return S(MONTG_OFFICERS, "Town of Montgomery (official "
             "website), 'Elected & Appointed Officer List' "
             f"(updated March 11, 2026): {what}")


def montgomery_spec():
    offices = [
        office("moderator", "Moderator",
               "Montgomery Moderator", 1,
               [montg_officers("lists Jacob Racusin as Moderator, "
                               "elected to a one-year term")],
               [holder("Jacob Racusin", "jacob-racusin")]),
        office("selectboard", "Selectboard Member",
               "Montgomery Selectboard", 5,
               [montg_officers("lists the five selectboard members "
                               "as Charlie Hancock, Dennis Himes, "
                               "Mark Brouillette, Christopher "
                               "Dixson-Boles, and Daniel Khan, all "
                               "elected"),
                sb_dir("lists Charles Hancock (Chair) among "
                       "Montgomery's selectboard members")],
               [holder("Charles Hancock", "charles-hancock"),
                holder("Dennis Himes", "dennis-himes"),
                holder("Mark Brouillette", "mark-brouillette"),
                holder("Christopher Dixson-Boles",
                       "christopher-dixson-boles"),
                holder("Daniel Khan", "daniel-khan")]),
        office("town-clerk", "Town Clerk",
               "Montgomery Town Clerk", 1,
               [clerk_xlsx("lists Elizabeth Reighley as "
                           "Montgomery's town clerk"),
                guide("names Elizabeth Reighley as Montgomery's "
                      "town clerk")],
               [holder("Elizabeth Reighley",
                       "elizabeth-reighley")]),
        office("town-treasurer", "Town Treasurer",
               "Montgomery Town Treasurer", 1,
               [guide("names Erin Kopacz as Montgomery's town "
                      "treasurer; the treasurer contact "
                      "spreadsheet carries no Montgomery entry")],
               [holder("Erin Kopacz", "erin-kopacz")]),
        office("lister", "Lister",
               "Montgomery Board of Listers", 3,
               [montg_officers("lists the three listers as James "
                               "Walsh, Marlene Hambleton, and "
                               "Kenny Miller, all elected")],
               [holder("James Walsh", "james-walsh"),
                holder("Marlene Hambleton",
                       "marlene-hambleton"),
                holder("Kenny Miller", "kenny-miller")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Montgomery Collector of Delinquent Taxes", 1,
               [montg_officers("lists Katherine Barnard as "
                               "Collector of Delinquent Taxes, "
                               "elected to a three-year term; the "
                               "Collector of Current Taxes is the "
                               "Treasurer ex officio and has no "
                               "separate post")],
               [holder("Katherine Barnard",
                       "katherine-barnard")]),
        office("first-constable", "First Constable",
               "Montgomery First Constable", 1,
               [montg_officers("lists Brent Godin as First "
                               "Constable, elected to a two-year "
                               "term")],
               [holder("Brent Godin", "brent-godin")]),
        office("cemetery-commissioner-village",
               "Village Cemetery Commissioner",
               "Montgomery Village Cemetery Commission", 5,
               [montg_officers("lists the five Village Cemetery "
                               "Commissioners as George Gabuzda, "
                               "JoAnne Lanphear, Lois Lumbra, "
                               "Penny Lumbra, and Tim Murphy, all "
                               "elected")],
               [holder("George Gabuzda", "george-gabuzda"),
                holder("JoAnne Lanphear", "joanne-lanphear"),
                holder("Lois Lumbra", "lois-lumbra"),
                holder("Penny Lumbra", "penny-lumbra"),
                holder("Tim Murphy", "tim-murphy")]),
        office("cemetery-commissioner-center",
               "Center Cemetery Commissioner",
               "Montgomery Center Cemetery Commission", 5,
               [montg_officers("lists the Center Cemetery "
                               "Commission as Jade Dixson-Boles, "
                               "Cindy Gilchrist, Charlie Purrier, "
                               "and Lyndol Elkins elected, with "
                               "the fifth seat printed Vacant; "
                               "the vacant seat is left unfilled")],
               [holder("Jade Dixson-Boles",
                       "jade-dixson-boles"),
                holder("Cindy Gilchrist", "cindy-gilchrist"),
                holder("Charlie Purrier", "charlie-purrier"),
                holder("Lyndol Elkins", "lyndol-elkins")]),
        office("library-trustee", "Library Trustee",
               "Montgomery Library Trustees", 9,
               [montg_officers("lists nine Library Trustees, all "
                               "elected to three-year terms: "
                               "Chris Dixson-Boles, Deanna "
                               "Robitaille, Shana Schaberg, Remi "
                               "Gratton, Carmen Carroll, Nicole "
                               "Landreman, Patty Hathaway, Cindy "
                               "Gilchrist, and Daniel Khan")],
               [holder("Christopher Dixson-Boles",
                       "christopher-dixson-boles"),
                holder("Deanna-Dee Robitaille",
                       "deanna-dee-robitaille"),
                holder("Shana Schaberg", "shana-schaberg"),
                holder("Remi Gratton", "remi-gratton"),
                holder("Carmen Carroll", "carmen-carroll"),
                holder("Nicole Landreman", "nicole-landreman"),
                holder("Patty Hathaway", "patty-hathaway"),
                holder("Cindy Gilchrist", "cindy-gilchrist"),
                holder("Daniel Khan", "daniel-khan")]),
        office("planning-commissioner", "Planning Commissioner",
               "Montgomery Planning Commission", 5,
               [montg_officers("lists the five Planning "
                               "Commissioners in the elected "
                               "section of the table: Alissa "
                               "Hardy, Amy Sekol, Diane Sherman, "
                               "Kim Morrill, and Patrick Calecas")],
               [holder("Alissa Hardy", "alissa-hardy"),
                holder("Amy Sekol", "amy-sekol"),
                holder("Diane Sherman", "diane-sherman"),
                holder("Kim Morrill", "kim-morrill"),
                holder("Patrick Calecas", "patrick-calecas")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Montgomery Justices of the Peace", 7,
               [jp_src("lists seven Montgomery justices of the "
                       "peace elected November 5, 2024"),
                montg_officers("the officer list's justice of "
                               "the peace block names the same "
                               "seven justices")],
               [holder("Tosca Smith", "tosca-smith"),
                holder("Suzanne Wilson", "suzanne-wilson"),
                holder("Deanna-Dee Robitaille",
                       "deanna-dee-robitaille"),
                holder("Christina Suarez-Pratt",
                       "christina-suarez-pratt"),
                holder("Gabrielle Lumbra", "gabrielle-lumbra"),
                holder("Parma Jewett", "parma-jewett"),
                holder("Darren Drevik", "darren-drevik")]),
    ]
    jp = jp_election(
        "montgomery-vt", "Town of Montgomery", 7,
        "lists seven Montgomery justices of the peace elected "
        "November 5, 2024: Tosca Smith, Suzanne Wilson, "
        "Deanna-Dee Robitaille, Christina Suarez-Pratt, "
        "Gabrielle Lumbra, Parma Jewett, and Darren Drevik. "
        "The listing publishes no vote totals or party labels "
        "and none are recorded",
        [montg_officers("the officer list names the same seven "
                        "justices of the peace")])
    return spec("montgomery", "Town of Montgomery", offices, jp)


SPECS["montgomery"] = montgomery_spec()

# ------------------------------------------------------------ Montpelier
MONTP_COUNCIL = {
    "url": "https://www.montpelier-vt.org/258/City-Council-Mayor",
    "note": "PLACEHOLDER",
}
MONTP_DIR = {
    "url": "https://www.montpelier-vt.org/directory",
    "note": "PLACEHOLDER",
}
MONTP_WEEKLY = {
    "url": "http://www.montpelier-vt.org/Archive.aspx?ADID=6964",
    "note": "PLACEHOLDER",
}
MONTP_PARKS = {
    "url": "https://www.montpelier-vt.org/464/Parks-Commission",
    "note": "PLACEHOLDER",
}
MONTP_CEM = {
    "url": "https://www.montpelier-vt.org/160/Cemetery-Commission",
    "note": "PLACEHOLDER",
}


def montp_council(what):
    return S(MONTP_COUNCIL, "City of Montpelier (official "
             f"website), City Council & Mayor page: {what}")


def montp_dir(what):
    return S(MONTP_DIR, "City of Montpelier (official website), "
             f"staff directory: {what}")


def montp_weekly(what):
    return S(MONTP_WEEKLY, "City of Montpelier, City Manager's "
             f"Weekly Report (July 31, 2026): {what}")


def montp_parks(what):
    return S(MONTP_PARKS, "City of Montpelier (official website), "
             f"Parks Commission page: {what}")


def montp_cem(what):
    return S(MONTP_CEM, "City of Montpelier (official website), "
             f"Cemetery Commission page: {what}")


def montpelier_spec():
    offices = [
        office("mayor", "Mayor",
               "Montpelier Mayor", 1,
               [charter005("section 401 provides for a Mayor "
                           "elected citywide to a two-year term"),
                montp_council("lists Marc Gwinn as Mayor")],
               [holder("Marc Gwinn", "marc-gwinn")]),
        office("councilor-district-1", "City Councilor, District 1",
               "Montpelier City Council", 2,
               [charter005("section 302 provides for two council "
                           "members from each of the three voting "
                           "districts, serving staggered two-year "
                           "terms; section 303 provides that the "
                           "Council appoints a replacement when a "
                           "council vacancy has more than 90 days "
                           "of unexpired term remaining"),
                montp_council("lists the District 1 councilors as "
                              "Ben Doyle (term 2025-2027) and "
                              "Paul Costello (term August 12, "
                              "2026 to March 2, 2027)"),
                montp_weekly("announces that the District 1 seat "
                             "was recently vacated by "
                             "Councilmember Adrienne Gil and that "
                             "the City Council would appoint a "
                             "replacement on August 12, 2026 to "
                             "serve until March 2, 2027; Costello "
                             "holds the seat by that appointment "
                             "and Gil, who departed, is not "
                             "recorded")],
               [holder("Ben Doyle", "ben-doyle"),
                holder("Paul Costello", "paul-costello",
                       how_seated="appointed")]),
        office("councilor-district-2", "City Councilor, District 2",
               "Montpelier City Council", 2,
               [charter005("section 302 provides for two council "
                           "members from each of the three voting "
                           "districts, serving staggered two-year "
                           "terms"),
                montp_council("lists the District 2 councilors as "
                              "Pelin Kohn (term 2025-2027) and "
                              "Sal Alfano (term 2026-2028)")],
               [holder("Pelin Kohn", "pelin-kohn"),
                holder("Sal Alfano", "sal-alfano")]),
        office("councilor-district-3", "City Councilor, District 3",
               "Montpelier City Council", 2,
               [charter005("section 302 provides for two council "
                           "members from each of the three voting "
                           "districts, serving staggered two-year "
                           "terms"),
                montp_council("lists the District 3 councilors as "
                              "Cary Brown (term 2026-2028) and "
                              "Jim Sheridan (term 2025-2027)")],
               [holder("Cary Brown", "cary-brown"),
                holder("Jim Sheridan", "jim-sheridan")]),
        office("city-clerk", "City Clerk",
               "Montpelier City Clerk", 1,
               [charter005("sections 509(a) and 905 provide for a "
                           "City Clerk elected to a three-year "
                           "term"),
                clerk_xlsx("lists John Odum as Montpelier's city "
                           "clerk"),
                guide("names John Odum as Montpelier's city "
                      "clerk")],
               [holder("John Odum", "john-odum")]),
        office("city-treasurer", "City Treasurer",
               "Montpelier City Treasurer", 1,
               [charter005("section 906 provides that the City "
                           "Council appoints the City Treasurer; "
                           "the membership is recorded as "
                           "appointed"),
                montp_dir("lists Crystal Lamell in the Finance "
                          "Department as 'Payroll and Accounting "
                          "Specialist, Treasurer'")],
               [holder("Crystal Lamell", "crystal-lamell",
                       how_seated="appointed")]),
        office("parks-commissioner", "Parks Commissioner",
               "Montpelier Parks Commission", 5,
               [charter005("section 802 establishes the Parks "
                           "Commission"),
                montp_parks("states that each Parks Commissioner "
                            "is elected at Town Meeting Day to a "
                            "staggered five-year term and lists "
                            "the five commissioners as Emily "
                            "Donaldson (term expires 2027), "
                            "Andrew Brewer (2028), Kassia Randzio "
                            "(Chair, 2029), Jessa Barnard (2030), "
                            "and Rebecca Copans (2031)")],
               [holder("Emily Donaldson", "emily-donaldson"),
                holder("Andrew Brewer", "andrew-brewer"),
                holder("Kassia Randzio", "kassia-randzio"),
                holder("Jessa Barnard", "jessa-barnard"),
                holder("Rebecca Copans", "rebecca-copans")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Green Mount Cemetery Commission", 5,
               [charter005("section 801 establishes the Green "
                           "Mount Cemetery Commission"),
                montp_cem("states the Cemetery Commission "
                          "consists of five members and lists "
                          "Jason Kass (Chair, term expires 2027), "
                          "Linda Hogan (2029), Darragh Ellerson "
                          "(2026), Barbara Smith (2028), and "
                          "Danielle Harris-Burnett (2030); but "
                          "three cemetery seats stood at the "
                          "March 3, 2026 city election (a "
                          "five-year term, a one-year remainder, "
                          "and a four-year remainder), which is "
                          "inconsistent with the page's stagger, "
                          "and the city's published 2026 "
                          "cemetery results were not located -- "
                          "no current holder is verified, so "
                          "the post is created without "
                          "memberships")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Montpelier Justices of the Peace", 15,
               [jp_src("lists fifteen Montpelier justices of the "
                       "peace elected November 5, 2024")],
               [holder("Conor Casey", "conor-casey",
                       existing_person_id="ocd-person/6d5b1b0a-3cde-540e-ba64-55887a708145"),
                holder("Elaine Ball", "elaine-ball"),
                holder("Dona Bate", "dona-bate"),
                holder("Thomas Abdelnour", "thomas-abdelnour"),
                holder("Mary S. Hooper", "mary-s-hooper"),
                holder("Kimberly B. Cheney",
                       "kimberly-b-cheney"),
                holder("Page Guertin", "page-guertin"),
                holder("Cary Brown", "cary-brown"),
                holder("John J. McCullough III",
                       "john-j-mccullough-iii",
                       ballot_name="John J. Mccullough III"),
                holder("Valerie Lewis", "valerie-lewis"),
                holder("Sarah Carter", "sarah-carter"),
                holder("Judith Newman", "judith-newman"),
                holder("Ron Wild", "ron-wild"),
                holder("Robert Gross", "robert-gross"),
                holder("Rosie Kruger", "rosie-kruger")]),
    ]
    jp = jp_election(
        "montpelier-vt", "City of Montpelier", 15,
        "lists fifteen Montpelier justices of the peace "
        "elected November 5, 2024: Conor Casey, Elaine Ball, "
        "Dona Bate, Thomas Abdelnour, Mary S. Hooper, Kimberly "
        "B. Cheney, Page Guertin, Cary Brown, John J. "
        "Mccullough III, Valerie Lewis, Sarah Carter, Judith "
        "Newman, Ron Wild, Robert Gross, and Rosie Kruger. "
        "The listing publishes no vote totals or party labels "
        "and none are recorded")
    return spec("montpelier", "City of Montpelier", offices, jp)


SPECS["montpelier"] = montpelier_spec()

# ------------------------------------------------------------ Moretown
MORE_BALLOT = {
    "url": "https://www.moretownvt.org/wp-content/uploads/2026/01/MORETOWN-VT-BALLOT-PROOF-030326.pdf",
    "note": "PLACEHOLDER",
}
MORE_REPORT = {
    "url": "https://www.moretownvt.org/wp-content/uploads/2026/02/Moretown-Town-Report-2025.pdf",
    "note": "PLACEHOLDER",
}
MORE_SBMIN_IDX = {
    "url": "https://www.moretownvt.org/minutes-and-agendas/selectboard-minutes-agendas/",
    "note": "PLACEHOLDER",
}
MORE_TAX = {
    "url": "https://www.moretownvt.org/town-departments/administration/tax-collector/",
    "note": "PLACEHOLDER",
}


def more_ballot(what):
    return S(MORE_BALLOT, "Town of Moretown (official website), "
             f"official ballot for the March 3, 2026 town "
             f"meeting: {what}")


def more_report(what):
    return S(MORE_REPORT, "Town of Moretown, 2025 Town Report, "
             f"officers table submitted by the Town Clerk: {what}")


def more_sbmin(what):
    return S(MORE_SBMIN_IDX, "Town of Moretown (official website), "
             f"Selectboard minutes: {what}")


def more_tax(what):
    return S(MORE_TAX, "Town of Moretown (official website), Tax "
             f"Collectors page: {what}")


def moretown_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Moretown Selectboard", 5,
               [more_sbmin("the Selectboard minutes of October "
                           "5, 2026 list as members present Tom "
                           "Martin, Mike Brown, Sam Rosenberg, "
                           "Callie Streeter, and Don Wexler"),
                sb_dir("lists Michael Brown and Thomas Martin "
                       "among Moretown's selectboard members"),
                more_report("the officers table lists the "
                            "selectboard before the 2026 "
                            "meeting as Tom Martin, Michael "
                            "Brown, Robin Campbell, Don Wexler, "
                            "and Callie Streeter; Campbell's "
                            "three-year term expired in 2026 "
                            "and the October 2026 minutes seat "
                            "Rosenberg in the current five")],
               [holder("Thomas Martin", "thomas-martin"),
                holder("Michael Brown", "michael-brown"),
                holder("Sam Rosenberg", "sam-rosenberg"),
                holder("Callie Streeter", "callie-streeter",
                       existing_person_id="ocd-person/167a0236-5552-50d3-8ca8-ee0e802d575c"),
                holder("Donald Wexler", "donald-wexler")]),
        office("town-clerk", "Town Clerk",
               "Moretown Town Clerk", 1,
               [more_ballot("prints Cherilyn Brown as the "
                            "candidate for Town Clerk for a "
                            "three-year term"),
                more_report("lists Cherilyn Brown as Town Clerk"),
                clerk_xlsx("lists Cherilyn Brown as Moretown's "
                           "town clerk"),
                guide("names Cherilyn Brown as Moretown's town "
                      "clerk")],
               [holder("Cherilyn Brown", "cherilyn-brown")]),
        office("town-treasurer", "Town Treasurer",
               "Moretown Town Treasurer", 1,
               [more_ballot("prints Cherilyn Brown as the "
                            "candidate for Town Treasurer for a "
                            "three-year term"),
                more_report("lists Cherilyn Brown as Town "
                            "Treasurer"),
                treas_xlsx("lists Cherilyn Brown as Moretown's "
                           "town treasurer"),
                guide("names Cherilyn Brown as Moretown's town "
                      "treasurer")],
               [holder("Cherilyn Brown", "cherilyn-brown")]),
        office("trustee-of-public-funds", "Trustee of Public Money",
               "Moretown Trustees of Public Money", 1,
               [more_ballot("prints Cherilyn Brown as the "
                            "candidate for Trustee of Public "
                            "Money for a one-year term"),
                more_report("lists Cherilyn Brown as Trustee of "
                            "Public Money")],
               [holder("Cherilyn Brown", "cherilyn-brown")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Moretown Collector of Delinquent Taxes", 1,
               [more_ballot("prints Craig Eilers as the candidate "
                            "for Delinquent Tax Collector for a "
                            "one-year term"),
                more_tax("names Craig Eilers as the Delinquent Tax "
                         "Collector"),
                more_report("lists Craig Eilers as Delinquent Tax "
                            "Collector")],
               [holder("Craig Eilers", "craig-eilers")]),
        office("first-constable", "First Constable",
               "Moretown First Constable", 1,
               [more_ballot("offers the First Constable two-year "
                            "seat by write-in only; no outcome is "
                            "published, so the post is created "
                            "without a membership"),
                more_report("lists the outgoing First Constable "
                            "as Tom Chenette, two-year term "
                            "expiring 2026; he is not recorded "
                            "as a current holder")]),
        office("second-constable", "Second Constable",
               "Moretown Second Constable", 1,
               [more_ballot("prints Clarence Wood as the "
                            "candidate for Second Constable"),
                more_report("lists Clarence Wood as Second "
                            "Constable, one-year term expiring "
                            "2026 -- the incumbent standing "
                            "again in 2026")],
               [holder("Clarence Wood", "clarence-wood")]),
        office("moderator", "Moderator",
               "Moretown Moderator", 1,
               [more_report("lists Steve Magill as Moderator, "
                            "one-year term expiring 2026; the "
                            "2026 floor outcome is not "
                            "published, so the post is created "
                            "without a membership")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Moretown Cemetery Commission", 3,
               [more_report("lists the three Cemetery "
                            "Commissioners on staggered "
                            "three-year terms: Mary Murphy-Blake "
                            "(expiring 2026), John S. Fulton "
                            "(2027), and Mark Austin (2028)"),
                more_ballot("offers one Cemetery Commissioner "
                            "three-year seat, printing Mary "
                            "Murphy-Blake as the candidate -- "
                            "the incumbent for the expiring "
                            "seat")],
               [holder("Mary Murphy-Blake",
                       "mary-murphy-blake"),
                holder("John Fulton", "john-fulton",
                       ballot_name="John S. Fulton"),
                holder("Mark Austin", "mark-austin")]),
        office("library-trustee", "Library Trustee",
               "Moretown Library Trustees", 5,
               [more_report("lists five Library Trustees: Pam "
                            "Barnes (one-year term expiring "
                            "2026, marked appointed), Sybil "
                            "Schlesinger (one-year, 2026), Dan "
                            "Zucker (three-year, 2026, marked "
                            "appointed), Bridget Harty "
                            "(three-year, 2027), and Erin Hunt "
                            "(three-year, 2028); the table's "
                            "note states an appointee must run "
                            "at the next town meeting for the "
                            "remaining term"),
                more_ballot("offers a Library Trustee "
                            "three-year seat printing Sybil "
                            "Schlesinger, and two one-year "
                            "seats printing Pam Barnes and "
                            "April Shaw; Zucker did not stand "
                            "in 2026 and Shaw, a non-incumbent "
                            "candidate with no published "
                            "outcome, is not recorded, so one "
                            "seat is left unfilled")],
               [holder("Bridget Harty", "bridget-harty"),
                holder("Erin Hunt", "erin-hunt"),
                holder("Pam Barnes", "pam-barnes"),
                holder("Sybil Schlesinger",
                       "sybil-schlesinger")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Moretown Justices of the Peace", 7,
               [more_report("lists seven justices of the peace: "
                            "Steve Magill, Ron Shems, Bridget "
                            "Harty, Sam Rosenberg, William "
                            "Nowlan, Sybil Schlesinger, and "
                            "Kate O'Neill"),
                jp_src("the Moretown block lists only four of "
                       "the seven (Bridget Harty, Stephen "
                       "Magill, William Nowlan, and Kathryn "
                       "O'Neill); the town report's superset "
                       "governs -- see the election note")],
               [holder("Bridget Harty", "bridget-harty"),
                holder("Stephen Magill", "stephen-magill"),
                holder("William Nowlan", "william-nowlan"),
                holder("Kathryn O'Neill", "kathryn-oneill",
                       ballot_name="Kate O'Neill"),
                holder("Ron Shems", "ron-shems"),
                holder("Sam Rosenberg", "sam-rosenberg"),
                holder("Sybil Schlesinger",
                       "sybil-schlesinger")]),
    ]
    jp = jp_election(
        "moretown-vt", "Town of Moretown", 7,
        "the Moretown block lists four justices of the peace "
        "elected November 5, 2024: Bridget Harty, Stephen "
        "Magill, William Nowlan, and Kathryn O'Neill. The Town "
        "of Moretown's 2025 Town Report officers table lists "
        "SEVEN justices of the peace -- the same four plus Ron "
        "Shems, Sam Rosenberg, and Sybil Schlesinger -- a "
        "superset of the listing, and the table proved "
        "seat-accurate for the selectboard, cemetery "
        "commission, and library trustees against the town's "
        "2026 ballot. The town report governs and the seven "
        "are recorded as the winners. The listing publishes "
        "no vote totals or party labels and none are "
        "recorded",
        [more_report("lists the seven justices of the peace "
                     "named in the election note")])
    return spec("moretown", "Town of Moretown", offices, jp)


SPECS["moretown"] = moretown_spec()

# ------------------------------------------------------------ Morgan
MORGAN_GOV = {
    "url": "https://townofmorgan.com/town-government/",
    "note": "PLACEHOLDER",
}
MORGAN_CLERK = {
    "url": "https://townofmorgan.com/town-clerk/",
    "note": "PLACEHOLDER",
}
LARRY_BIO = {
    "url": "https://legislature.vermont.gov/people/single/2021.1/36152",
    "note": "PLACEHOLDER",
}


def morgan_gov(what):
    return S(MORGAN_GOV, "Town of Morgan (official website), "
             f"Town Government page (2025-2026 officers): {what}")


def morgan_clerk(what):
    return S(MORGAN_CLERK, "Town of Morgan (official website), "
             f"Town Clerk page: {what}")


def larry_bio(what):
    return S(LARRY_BIO, "Vermont General Assembly, Representative "
             f"Larry Labor's member page and biography: {what}")


def morgan_spec():
    offices = [
        office("moderator", "Moderator",
               "Morgan Moderator", 1,
               [morgan_gov("lists Kathy Austin as Moderator, "
                           "one-year term to 2027")],
               [holder("Kathy Austin", "kathy-austin")]),
        office("town-clerk", "Town Clerk",
               "Morgan Town Clerk", 1,
               [morgan_gov("lists TammyLee Morin as Town Clerk, "
                           "three-year term to 2029"),
                morgan_clerk("styles the office 'TammyLee Morin, "
                             "Town Clerk & Treasurer'"),
                clerk_xlsx("lists TammyLee Morin as Morgan's "
                           "town clerk"),
                guide("names TammyLee Morin as Morgan's town "
                      "clerk")],
               [holder("TammyLee Morin", "tammylee-morin")]),
        office("town-treasurer", "Town Treasurer",
               "Morgan Town Treasurer", 1,
               [morgan_gov("lists TammyLee Morin as Town "
                           "Treasurer, three-year term to 2029"),
                morgan_clerk("styles the office 'TammyLee Morin, "
                             "Town Clerk & Treasurer'"),
                guide("names TammyLee Morin as Morgan's town "
                      "treasurer; the treasurer contact "
                      "spreadsheet carries no Morgan entry")],
               [holder("TammyLee Morin", "tammylee-morin")]),
        office("selectboard", "Selectboard Member",
               "Morgan Selectboard", 3,
               [morgan_gov("lists the three selectmen as Eric "
                           "Pope (Chair, to 2029), Larry Labor "
                           "(to 2027), and Bruce Remick -- "
                           "Remick's row prints a stale '2025' "
                           "expiry year on the town's 2025-2026 "
                           "officers page, and the June 2026 "
                           "Secretary of State directory also "
                           "seats him, so he is recorded as a "
                           "current member"),
                sb_dir("lists Bruce Remick among Morgan's "
                       "selectboard members"),
                larry_bio("Representative Larry Labor's "
                          "biography states he 'was elected to "
                          "the Morgan select board in 2009 and "
                          "continues in the role of select "
                          "board member'; the Morgan membership "
                          "reuses his existing person record")],
               [holder("Eric Pope", "eric-pope"),
                holder("Larry Labor", "larry-labor",
                       existing_person_id="ocd-person/21ad5645-d4cc-52ab-9f4c-62bc4f75397d"),
                holder("Bruce Remick", "bruce-remick")]),
        office("road-commissioner", "Road Commissioner",
               "Morgan Road Commissioner", 1,
               [morgan_gov("lists Shawn Austin as Road "
                           "Commissioner in the elected "
                           "officers, three-year term to 2029")],
               [holder("Shawn Austin", "shawn-austin")]),
        office("first-constable", "First Constable",
               "Morgan First Constable", 1,
               [morgan_gov("lists Robert Cain as First "
                           "Constable, one-year term to 2027")],
               [holder("Robert Cain", "robert-cain")]),
        office("second-constable", "Second Constable",
               "Morgan Second Constable", 1,
               [morgan_gov("lists Ric Pare as Second Constable, "
                           "one-year term to 2027")],
               [holder("Ric Paré", "ric-pare")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Morgan Collector of Delinquent Taxes", 1,
               [morgan_gov("lists James Judd as Collector of "
                           "Delinquent Taxes, one-year term to "
                           "2027")],
               [holder("James Judd", "james-judd")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Morgan Cemetery Commission", 5,
               [morgan_gov("lists the five Cemetery "
                           "Commissioners on staggered "
                           "five-year terms: Deanna Keenan "
                           "(2027), Ric Pare (2028), Doug Garon "
                           "(2029), Kenneth Whitehill (2030), "
                           "and Robert Guyer (2031)")],
               [holder("Deanna Keenan", "deanna-keenan"),
                holder("Ric Paré", "ric-pare"),
                holder("Doug Garon", "doug-garon"),
                holder("Kenneth Whitehill",
                       "kenneth-whitehill"),
                holder("Robert Guyer", "robert-guyer")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Morgan Justices of the Peace", 5,
               [jp_src("lists five Morgan justices of the peace "
                       "elected November 5, 2024")],
               [holder("Jane Malgeri", "jane-malgeri"),
                holder("Donna Young", "donna-young"),
                holder("Julia Norton", "julia-norton"),
                holder("Debra Bevins", "debra-bevins"),
                holder("Meredith Augustoni",
                       "meredith-augustoni")]),
    ]
    jp = jp_election(
        "morgan-vt", "Town of Morgan", 5,
        "lists five Morgan justices of the peace elected "
        "November 5, 2024: Jane Malgeri, Donna Young, Julia "
        "Norton, Debra Bevins, and Meredith Augustoni. The "
        "listing publishes no vote totals or party labels and "
        "none are recorded")
    return spec("morgan", "Town of Morgan", offices, jp)


SPECS["morgan"] = morgan_spec()

# ------------------------------------------------------------ Morristown
MORRISTOWN_DIR = {
    "url": "https://www.morristownvt.gov/directory",
    "note": "PLACEHOLDER",
}
MORRISTOWN_REPORT = {
    "url": "https://www.morristownvt.gov/media/6656",
    "note": "PLACEHOLDER",
}


def morristown_dir(what):
    return S(MORRISTOWN_DIR, "Town of Morristown (official "
             f"website), staff and boards directory: {what}")


def morristown_report(what):
    return S(MORRISTOWN_REPORT, "Town of Morristown, 2025 Annual "
             f"Town Report: {what}")


def morristown_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Morristown Selectboard", 5,
               [morristown_dir("lists the five selectboard "
                               "members as Donald McDowell "
                               "(Chair), Richard Craig, George "
                               "Cormier, Leah Hollenberger, and "
                               "Rose Belanger"),
                sb_dir("lists Donald McDowell (Chair), Rose "
                       "Belanger, and George Cormier among "
                       "Morristown's selectboard members"),
                morristown_report("the certified results of the "
                                  "March 4, 2025 annual town "
                                  "meeting re-elected Richard "
                                  "Craig (836 votes, three-year "
                                  "term) and Donald McDowell "
                                  "(1,120 votes, two-year term)")],
               [holder("Donald McDowell", "donald-mcdowell"),
                holder("Richard Craig", "richard-craig"),
                holder("George Cormier", "george-cormier"),
                holder("Leah Hollenberger",
                       "leah-hollenberger"),
                holder("Rose Belanger", "rose-belanger")]),
        office("town-clerk", "Town Clerk",
               "Morristown Town Clerk", 1,
               [morristown_dir("lists Sara Haskins as Town Clerk"),
                morristown_report("the Elected Town Officers "
                                  "page lists Sara Haskins as "
                                  "Town Clerk"),
                clerk_xlsx("lists Sara Haskins as Morristown's "
                           "town clerk"),
                guide("names Sara Haskins as Morristown's town "
                      "clerk")],
               [holder("Sara Haskins", "sara-haskins")]),
        office("town-treasurer", "Town Treasurer",
               "Morristown Town Treasurer", 1,
               [morristown_dir("lists Sara Haskins as Town "
                               "Treasurer"),
                morristown_report("the Elected Town Officers "
                                  "page lists Sara Haskins as "
                                  "Town Treasurer"),
                treas_xlsx("lists Sara Haskins as Morristown's "
                           "town treasurer"),
                guide("names Sara Haskins as Morristown's town "
                      "treasurer")],
               [holder("Sara Haskins", "sara-haskins")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Morristown Collector of Delinquent Taxes", 1,
               [morristown_report("the Appointed Officers page "
                                  "lists 'Delinquent Tax "
                                  "Collector -- Sara Haskins, "
                                  "3 Year Term' among the "
                                  "officers appointed by the "
                                  "Selectboard; the membership "
                                  "is recorded as appointed")],
               [holder("Sara Haskins", "sara-haskins",
                       how_seated="appointed")]),
        office("moderator", "Moderator",
               "Morristown Moderator", 1,
               [morristown_report("the certified results of the "
                                  "March 4, 2025 annual town "
                                  "meeting elected Shapleigh "
                                  "Smith, Jr. Moderator with "
                                  "1,318 votes for a one-year "
                                  "term expiring in 2026; the "
                                  "March 2026 outcome is not "
                                  "published in any source "
                                  "located, so the post is "
                                  "created without a membership")]),
        office("lister", "Lister",
               "Morristown Board of Listers", 3,
               [morristown_dir("lists the Board of Listers as "
                               "Grant Wieler (Chair) and Kevin "
                               "Petrochko, with the third seat "
                               "vacant"),
                morristown_report("the certified March 4, 2025 "
                                  "results mark write-in "
                                  "candidate Grant Wieler the "
                                  "winner of both the three-year "
                                  "lister seat (38 write-ins) "
                                  "and the two-year remainder "
                                  "seat (40); he holds one "
                                  "seat. The Elected Town "
                                  "Officers page marks Kevin "
                                  "Petrochko's seat '(Appointed "
                                  "5/5/25)'; his membership is "
                                  "recorded as appointed. Brian "
                                  "Yeaton, listed in the "
                                  "report, has departed and the "
                                  "third seat is vacant")],
               [holder("Grant Wieler", "grant-wieler"),
                holder("Kevin Petrochko", "kevin-petrochko",
                       how_seated="appointed")]),
        office("trustee-of-public-funds", "Trustee of Public Funds",
               "Morristown Trustees of Public Funds", 3,
               [morristown_report("the Elected Town Officers "
                                  "page lists three Trustees of "
                                  "Public Funds on staggered "
                                  "terms: Sara Haskins "
                                  "(expiring 2026), Mitzi "
                                  "Fleming (2027), and Julia "
                                  "Compagna (2028); the "
                                  "certified March 4, 2025 "
                                  "results mark write-in "
                                  "candidate Julia Compagna "
                                  "the winner with 121 votes. "
                                  "Haskins's seat expired in "
                                  "2026 and its outcome is "
                                  "unpublished, so it is left "
                                  "unfilled")],
               [holder("Mitzi Fleming", "mitzi-fleming"),
                holder("Julia Compagna", "julia-compagna")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Morristown Justices of the Peace", 15,
               [jp_src("lists fifteen Morristown justices of "
                       "the peace elected November 5, 2024"),
                morristown_report("the report's justice of the "
                                  "peace page lists Jane Foster "
                                  "and Aimee Towne, who are not "
                                  "in the Secretary of State's "
                                  "listing, and omits the "
                                  "listing's Charles Burnham "
                                  "and Roland Billings; the "
                                  "certified listing governs -- "
                                  "see the election note")],
               [holder("Darcie Abbene", "darcie-abbene"),
                holder("Judy Bickford", "judy-bickford"),
                holder("Donald Blake Jr.", "donald-blake-jr"),
                holder("Julia Compagna", "julia-compagna"),
                holder("Richard Craig", "richard-craig"),
                holder("Leah Hollenberger",
                       "leah-hollenberger"),
                holder("Urban Martin", "urban-martin"),
                holder("Monte Mason", "monte-mason"),
                holder("Yvette Mason", "yvette-mason"),
                holder("Shelley Nolan", "shelley-nolan"),
                holder("Siri Rooney", "siri-rooney"),
                holder("Shapleigh Smith Jr.",
                       "shapleigh-smith-jr"),
                holder("Edward Wilson", "edward-wilson"),
                holder("Charles Burnham", "charles-burnham"),
                holder("Roland Billings", "roland-billings")]),
    ]
    jp = jp_election(
        "morristown-vt", "Town of Morristown", 15,
        "lists fifteen Morristown justices of the peace "
        "elected November 5, 2024: Darcie Abbene, Judy "
        "Bickford, Donald Blake, Jr, Julia Compagna, Richard "
        "Craig, Leah Hollenberger, Urban Martin, Monte Mason, "
        "Yvette Mason, Shelley Nolan, Siri Rooney, Shapleigh "
        "Smith, Jr, Edward Wilson, Charles Burnham, and "
        "Roland Billings. The Town of Morristown's 2025 "
        "Annual Town Report lists Jane Foster and Aimee "
        "Towne as justices of the peace instead of Burnham "
        "and Billings; the certified listing governs the "
        "election record, and Foster and Towne (possible "
        "mid-term appointees) are not recorded as holders. "
        "The listing publishes no vote totals or party "
        "labels and none are recorded",
        [morristown_report("the report's justice of the peace "
                           "page carries the Foster/Towne "
                           "divergence described in the "
                           "election note")])
    return spec("morristown", "Town of Morristown", offices, jp)


SPECS["morristown"] = morristown_spec()

# ------------------------------------------------------------ Morrisville
MWL_TRUSTEES = {
    "url": "https://www.mwlvt.com/trustees",
    "note": "PLACEHOLDER",
}
MWL_ABOUT = {
    "url": "https://www.mwlvt.com/about",
    "note": "PLACEHOLDER",
}


def mwl_trustees(what):
    return S(MWL_TRUSTEES, "Morrisville Water & Light (the "
             "Village of Morrisville's municipal utility), "
             f"Trustees page: {what}")


def mwl_about(what):
    return S(MWL_ABOUT, "Morrisville Water & Light, About page: "
             f"{what}")


def morrisville_spec():
    offices = [
        office("village-trustee", "Village Trustee",
               "Morrisville Village Trustees", 5,
               [charter245("section 6(a) provides for five "
                           "trustees elected at the annual "
                           "meeting to five-year terms"),
                mwl_trustees("names the Village's five-member "
                             "Board of Trustees as Carl Fortune, "
                             "Thomas Snipp, Travis Knapp, Robert "
                             "Heanue, and Bradley Limoge"),
                mwl_about("states the trustees serve five-year "
                          "terms and are elected at the annual "
                          "Village Meeting, and names the same "
                          "five current trustees")],
               [holder("Carl Fortune", "carl-fortune"),
                holder("Thomas Snipp", "thomas-snipp"),
                holder("Travis Knapp", "travis-knapp"),
                holder("Robert Heanue", "robert-heanue"),
                holder("Bradley Limoge", "bradley-limoge")]),
        office("moderator", "Village Moderator",
               "Morrisville Village Moderator", 1,
               [charter245("section 6(a) provides for a "
                           "Moderator elected at the annual "
                           "meeting to a one-year term; no "
                           "published source located names the "
                           "current holder, so the post is "
                           "created without a membership")]),
        office("village-clerk", "Village Clerk",
               "Morrisville Village Clerk", 1,
               [charter245("section 6(a) provides for a Clerk "
                           "elected at the annual meeting to a "
                           "one-year term; no published source "
                           "located names the current holder, so "
                           "the post is created without a "
                           "membership. The 'Clerk' named beside "
                           "individual trustees on the utility's "
                           "pages is clerk of the board of "
                           "trustees, a different role")]),
        office("village-treasurer", "Village Treasurer",
               "Morrisville Village Treasurer", 1,
               [charter245("section 6(a) provides for a "
                           "Treasurer elected at the annual "
                           "meeting to a one-year term; no "
                           "published source located names the "
                           "current holder, so the post is "
                           "created without a membership")]),
    ]
    return spec("morrisville", "Village of Morrisville", offices)


SPECS["morrisville"] = morrisville_spec()

# ------------------------------------------------------------ Mount Holly
MTHOLLY_SB = {
    "url": "https://www.mounthollyvt.org/town-services/selectboard/",
    "note": "PLACEHOLDER",
}
MTHOLLY_LISTERS = {
    "url": "https://www.mounthollyvt.org/town-services/board-of-listers/",
    "note": "PLACEHOLDER",
}
MTHOLLY_AUD = {
    "url": "https://www.mounthollyvt.org/town-services/auditors/",
    "note": "PLACEHOLDER",
}
MTHOLLY_OFFICE = {
    "url": "https://www.mounthollyvt.org/town-office/",
    "note": "PLACEHOLDER",
}
MTHOLLY_MIN_APR29 = {
    "url": "https://www.mounthollyvt.org/wp-content/uploads/2026/05/Select-Board-2026-04-29-Special-Meeting-Minutes.pdf",
    "note": "PLACEHOLDER",
}
MTHOLLY_MIN_MAY20 = {
    "url": "https://mounthollyvt.org/wp-content/uploads/2026/06/Select-Board-2026-05-20-Special-Meeting-Minutes.pdf",
    "note": "PLACEHOLDER",
}
MTHOLLY_MIN_MAR10 = {
    "url": "https://www.mounthollyvt.org/wp-content/uploads/2026/03/Select-Board-2026-03-10-Regular-Meeting-Minutes.pdf",
    "note": "PLACEHOLDER",
}


def mtholly_sb(what):
    return S(MTHOLLY_SB, "Town of Mount Holly (official website), "
             f"Select Board page: {what}")


def mtholly_listers(what):
    return S(MTHOLLY_LISTERS, "Town of Mount Holly (official "
             f"website), Board of Listers page: {what}")


def mtholly_aud(what):
    return S(MTHOLLY_AUD, "Town of Mount Holly (official website), "
             f"Auditors page: {what}")


def mtholly_office(what):
    return S(MTHOLLY_OFFICE, "Town of Mount Holly (official "
             f"website), Town Office page: {what}")


def mtholly_apr29(what):
    return S(MTHOLLY_MIN_APR29, "Town of Mount Holly, Select Board "
             f"special meeting minutes, April 29, 2026: {what}")


def mtholly_may20(what):
    return S(MTHOLLY_MIN_MAY20, "Town of Mount Holly, Select Board "
             f"special meeting minutes, May 20, 2026: {what}")


def mtholly_mar10(what):
    return S(MTHOLLY_MIN_MAR10, "Town of Mount Holly, Select Board "
             f"regular meeting minutes, March 10, 2026: {what}")


def mount_holly_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Mount Holly Selectboard", 3,
               [mtholly_sb("lists the three selectboard members "
                           "as Mark Turco (Chair), Jeff Chase, "
                           "and Diana Garrow, elected to "
                           "three-year terms with one expiring "
                           "every year"),
                sb_dir("carries no Mount Holly roster (it directs "
                       "readers to contact the town clerk)")],
               [holder("Mark Turco", "mark-turco"),
                holder("Jeff Chase", "jeff-chase"),
                holder("Diana Garrow", "diana-garrow")]),
        office("town-clerk", "Town Clerk",
               "Mount Holly Town Clerk", 1,
               [mtholly_office("lists Carol Garrow-Woolley as Town "
                               "Clerk"),
                clerk_xlsx("lists Carol Garrow-Woolley as Mount "
                           "Holly's town clerk"),
                guide("names Carol A. Garrow-Woolley as Mount "
                      "Holly's town clerk")],
               [holder("Carol Garrow-Woolley",
                       "carol-garrow-woolley")]),
        office("town-treasurer", "Town Treasurer",
               "Mount Holly Town Treasurer", 1,
               [mtholly_may20("the Select Board voted "
                              "unanimously to appoint Marc "
                              "Miller as Treasurer, to complete "
                              "the term until March 2027"),
                mtholly_apr29("announces the resignation of Liz "
                              "Karle as Town Treasurer and that "
                              "the Select Board would appoint a "
                              "new Treasurer to complete the "
                              "term; Karle, the elected "
                              "treasurer named in the Guide, "
                              "has departed and is not "
                              "recorded"),
                guide("names Elizabeth Karle as Mount Holly's "
                      "town treasurer (superseded by her April "
                      "2026 resignation)")],
               [holder("Marc Miller", "marc-miller",
                       how_seated="appointed")]),
        office("lister", "Lister",
               "Mount Holly Board of Listers", 3,
               [mtholly_listers("states the position of Lister "
                                "is an elected office and lists "
                                "the three listers as Ann "
                                "Hansen, Tiffany Austin, and "
                                "Mary Surething"),
                mtholly_mar10("the minutes welcome Tiffany "
                              "Austin as a newly elected Lister")],
               [holder("Ann Hansen", "ann-hansen"),
                holder("Tiffany Austin", "tiffany-austin"),
                holder("Mary Surething", "mary-surething")]),
        office("auditor", "Auditor",
               "Mount Holly Auditors", 3,
               [mtholly_aud("states each auditor is elected to "
                            "serve a three-year term and lists "
                            "the three auditors as Lori Norton, "
                            "Tiffany Norton, and Christine "
                            "Pratt")],
               [holder("Lori Norton", "lori-norton"),
                holder("Tiffany Norton", "tiffany-norton"),
                holder("Christine Pratt", "christine-pratt")]),
        office("moderator", "Moderator",
               "Mount Holly Moderator", 1,
               [statute2646_structure("one moderator for a "
                                      "one-year term")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Mount Holly Justices of the Peace", 7,
               [jp_src("lists seven Mount Holly justices of the "
                       "peace elected November 5, 2024")],
               [holder("Diana Garrow", "diana-garrow"),
                holder("David Johnson", "david-johnson"),
                holder("Millicent Johnson",
                       "millicent-johnson"),
                holder("Robert Herbst", "robert-herbst"),
                holder("Marc Miller", "marc-miller"),
                holder("Brigid Sullivan", "brigid-sullivan"),
                holder("Linda Miller", "linda-miller")]),
    ]
    jp = jp_election(
        "mount-holly-vt", "Town of Mount Holly", 7,
        "lists seven Mount Holly justices of the peace elected "
        "November 5, 2024: Diana Garrow, David Johnson, "
        "Millicent Johnson, Robert Herbst, Marc Miller, "
        "Brigid Sullivan, and Linda Miller. The listing "
        "publishes no vote totals or party labels and none "
        "are recorded")
    return spec("mount-holly", "Town of Mount Holly", offices, jp)


SPECS["mount-holly"] = mount_holly_spec()

# ------------------------------------------------------------ Mount Tabor
def mount_tabor_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Mount Tabor Selectboard", 3,
               [sb_dir("carries a single Mount Tabor row naming "
                       "one member only as 'R. Gasperetti' of "
                       "420 Troll Hill Rd, which does not "
                       "distinguish Robert Gasperetti from R. "
                       "Matthew Gasperetti III (both are Mount "
                       "Tabor justices of the peace); no holder "
                       "is recorded rather than guess"),
                statute2646_structure("selectboard members "
                                       "elected for staggered "
                                       "three-year terms")]),
        office("town-clerk", "Town Clerk",
               "Mount Tabor Town Clerk", 1,
               [clerk_xlsx("lists Noel Weeks as Mount Tabor's "
                           "town clerk (townclerk@mounttaborvt.gov)"),
                guide("names William Basso II as Mount Tabor's "
                      "town clerk; the June 2026 clerk contact "
                      "spreadsheet is the later source and "
                      "governs")],
               [holder("Noel Weeks", "noel-weeks")]),
        office("town-treasurer", "Town Treasurer",
               "Mount Tabor Town Treasurer", 1,
               [guide("names William Basso II as Mount Tabor's "
                      "town treasurer; he is superseded as town "
                      "clerk by the June 2026 clerk contact "
                      "spreadsheet, which carries no Mount "
                      "Tabor treasurer entry, so no current "
                      "treasurer is verified and the post is "
                      "created without a membership")]),
        office("moderator", "Moderator",
               "Mount Tabor Moderator", 1,
               [statute2646_structure("one moderator for a "
                                      "one-year term")]),
        office("lister", "Lister",
               "Mount Tabor Board of Listers", 3,
               [statute2646_structure("three listers on "
                                      "staggered three-year "
                                      "terms")]),
        office("auditor", "Auditor",
               "Mount Tabor Auditors", 3,
               [statute2646_structure("three auditors on "
                                      "staggered three-year "
                                      "terms")]),
        office("grand-juror", "Grand Juror",
               "Mount Tabor Grand Juror", 1,
               [statute2646_structure("one grand juror")]),
        office("town-agent", "Town Agent",
               "Mount Tabor Town Agent", 1,
               [statute2646_structure("one town agent")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Mount Tabor Justices of the Peace", 5,
               [jp_src("lists five Mount Tabor justices of the "
                       "peace elected November 5, 2024")],
               [holder("R. Matthew Gasperetti III",
                       "r-matthew-gasperetti-iii"),
                holder("Noel Weeks", "noel-weeks"),
                holder("David Langsett", "david-langsett"),
                holder("William Beauregard",
                       "william-beauregard"),
                holder("Robert Gasperetti",
                       "robert-gasperetti")]),
    ]
    jp = jp_election(
        "mount-tabor-vt", "Town of Mount Tabor", 5,
        "lists five Mount Tabor justices of the peace elected "
        "November 5, 2024: R Matthew Gasperetti III, Noel "
        "Weeks, David Langsett, William Beauregard, and "
        "Robert Gasperetti. The listing publishes no vote "
        "totals or party labels and none are recorded")
    return spec("mount-tabor", "Town of Mount Tabor", offices, jp)


SPECS["mount-tabor"] = mount_tabor_spec()

# ------------------------------------------------------------ emit
for slug in ORDER:
    s = SPECS[slug]
    p = OUT / f"{s['place_slug']}.json"
    p.write_text(json.dumps(s, indent=1) + "\n")
    n_off = len(s["offices"])
    n_hold = sum(len(o.get("holders", ())) for o in s["offices"])
    print(f"{s['place_slug']}: {n_off} offices, {n_hold} holders")
print(f"TOTAL: {len(SPECS)} specs")
