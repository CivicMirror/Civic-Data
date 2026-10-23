#!/usr/bin/env python3
"""Batch 3 of the VT #163 municipal fan-out (alphabetical positions
21-30; Bloomfield #24 already done): Berkshire, Berlin, Bethel,
Bolton, Bradford, Braintree, Brandon, Brattleboro, Bridgewater.
Emits one JSON spec per municipality for build_vt_municipality.py.
Research: vt_muni_batch3_research.md.
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


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 3); issue #163 "
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
                  f"# municipal fan-out batch 3; issue #163 "
                  f"(VT master tracking).\n",
        "offices": offices,
    }
    if jp:
        d["jp_election"] = jp
    return d


def office(slug, title, org_name, seats, sources, holders=()):
    d = {
        "slug": slug,
        "title": title,
        "org_name": org_name,
        "seats": seats,
        "sources": sources,
    }
    if holders:
        d["holders"] = list(holders)
    return d


SPECS = []

# ------------------------------------------------------------- Berkshire
BERK_OFFICERS = {
    "url": "https://www.berkshirevt.com/town-officers.html",
    "note": "PLACEHOLDER",
}


def berk_officers(what):
    return S(BERK_OFFICERS, f"Town of Berkshire official website, "
             f"'Town Officers' page: {what}")


SPECS.append(spec("berkshire", "Town of Berkshire", [
    office("selectboard", "Selectboard Member", "Berkshire Selectboard", 5,
           [berk_officers("lists the Selectboard as Jason Kittell "
                          "(Chair), Andrew Smith (Vice Chair), Todd "
                          "Kinney, Tony Archambault, and Mark Larivee. "
                          "The Secretary of State's Selectboard Members "
                          "directory publishes no Berkshire roster "
                          "('Contact the Town Clerk').")],
           [holder("Jason Kittell", "jason-kittell"),
            holder("Andrew Smith", "andrew-smith"),
            holder("Todd Kinney", "todd-kinney"),
            holder("Tony Archambault", "tony-archambault"),
            holder("Mark Larivee", "mark-larivee")]),
    office("town-clerk", "Town Clerk", "Berkshire Town Clerk", 1,
           [berk_officers("lists 'Town Clerk/Treasurer: Emily "
                          "Fecteau' (Berkshire combines the offices)."),
            guide("lists Emily Fecteau as Town Clerk of Berkshire "
                  "and as Town Treasurer of Berkshire.")],
           [holder("Emily Fecteau", "emily-fecteau")]),
    office("town-treasurer", "Town Treasurer", "Berkshire Town Treasurer", 1,
           [berk_officers("lists 'Town Clerk/Treasurer: Emily "
                          "Fecteau' (Berkshire combines the offices)."),
            guide("lists Emily Fecteau as Town Clerk of Berkshire "
                  "and as Town Treasurer of Berkshire.")],
           [holder("Emily Fecteau", "emily-fecteau")]),
    office("moderator", "Moderator", "Berkshire Town Moderator", 1,
           [statute2646("a moderator"),
            berk_officers("lists the Moderator office as 'Vacant', "
                          "so no holder is recorded.")]),
    office("lister", "Lister", "Berkshire Board of Listers", 3,
           [berk_officers("names one lister, Hilegard Jamka (the "
                          "page also lists an appointed assessor, "
                          "Justin Mason). The other two lister seats "
                          "are named in no official source, so only "
                          "Jamka is recorded.")],
           [holder("Hilegard Jamka", "hilegard-jamka")]),
    office("auditor", "Auditor", "Berkshire Town Auditors", 3,
           [berk_officers("lists the Auditors as Hilegard Jamka, "
                          "Breanna Thompson, and Linda Sweetser.")],
           [holder("Hilegard Jamka", "hilegard-jamka"),
            holder("Breanna Thompson", "breanna-thompson"),
            holder("Linda Sweetser", "linda-sweetser")]),
    office("collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
           "Berkshire Collector of Delinquent Taxes", 1,
           [berk_officers("lists 'Delinquent Tax Collector: Virginia "
                          "Messier'. Berkshire fills the office "
                          "separately from the treasurer (17 V.S.A. "
                          "section 2651d).")],
           [holder("Virginia Messier", "virginia-messier")]),
    office("road-commissioner", "Road Commissioner",
           "Berkshire Road Commissioner", 1,
           [berk_officers("lists Rony Archambault as Road "
                          "Commissioner among the town officers "
                          "(a distinct person from Selectboard "
                          "member Tony Archambault).")],
           [holder("Rony Archambault", "rony-archambault")]),
    office("first-constable", "First Constable", "Berkshire First Constable", 1,
           [statute2646("a first constable"),
            berk_officers("lists no constable, and no other "
                          "official source publishes the holder, so "
                          "none is recorded.")]),
    office("grand-juror", "Grand Juror", "Berkshire Grand Juror", 1,
           [statute2646("a grand juror"),
            berk_officers("lists no grand juror, and no other "
                          "official source publishes the holder, so "
                          "none is recorded.")]),
    office("town-agent", "Town Agent", "Berkshire Town Agent", 1,
           [statute2646("a town agent to prosecute and defend suits"),
            berk_officers("lists no town agent, and no other "
                          "official source publishes the holder, so "
                          "none is recorded.")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Berkshire Justices of the Peace", 6,
           [jp_src("lists six Berkshire justices of the peace: "
                   "Jerod Adams, Trish Adams, Meghan Corrigan, "
                   "Stacy Gregoire, Marilyn \"Lyn\" Lauffer, and "
                   "Ryan Roy."),
            berk_officers("lists the same six justices of the "
                          "peace.")],
           [holder("Jerod Adams", "jerod-adams"),
            holder("Trish Adams", "trish-adams"),
            holder("Meghan Corrigan", "meghan-corrigan"),
            holder("Stacy Gregoire", "stacy-gregoire"),
            holder("Marilyn Lauffer", "marilyn-lauffer",
                   ballot_name='Marilyn "Lyn" Lauffer'),
            holder("Ryan Roy", "ryan-roy")]),
], jp=jp_election(
    "berkshire-vt", "Town of Berkshire", 6,
    "lists six Berkshire justices of the peace for the 2025-2026 "
    "term (Jerod Adams, Trish Adams, Meghan Corrigan, Stacy "
    "Gregoire, Marilyn \"Lyn\" Lauffer, Ryan Roy); they are the "
    "winners of the November 5, 2024 election for the office. "
    "The listing publishes no vote totals and no party "
    "designations for justices of the peace.")))

# ------------------------------------------------------------- Berlin
CH105 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/105",
    "note": "PLACEHOLDER",
}
BERLIN_SB_PAGE = {
    "url": "https://www.berlinvt.gov/selectboard",
    "note": "PLACEHOLDER",
}
BERLIN_RESULTS = {
    "url": "https://www.berlinvt.gov/s/2026-Town-Official-Results.pdf",
    "note": "PLACEHOLDER",
}
BERLIN_CLERK_PAGE = {
    "url": "https://www.berlinvt.gov/town-clerk",
    "note": "PLACEHOLDER",
}
BERLIN_TREAS_PAGE = {
    "url": "https://www.berlinvt.gov/treasurer",
    "note": "PLACEHOLDER",
}


def ch105(what):
    return S(CH105, "Town of Berlin charter, 24 App. V.S.A. ch. 105 "
             f"(official text, Vermont General Assembly): {what}")


SPECS.append(spec("berlin", "Town of Berlin", [
    office("selectboard", "Selectboard Member", "Berlin Selectboard", 5,
           [S(BERLIN_SB_PAGE, "Town of Berlin official website, "
              "Selectboard page: lists Jared Felch (Chair), Brian "
              "Divelbliss (Vice-Chair), Karla Nuissl (Secretary), "
              "Florence \"Flo\" Smith, and Kris Hayward."),
            sb_dir("lists the same five Berlin Selectboard members."),
            S(BERLIN_RESULTS, "Town of Berlin, '2026 Town Meeting "
              "Official Results' (March 3, 2026): Florence \"Flo\" "
              "Smith (309) won the three-year seat, Kris Hayward "
              "(224) won the two-years-remaining seat, and Brian "
              "Divelbliss (364) won the one-year seat; the other "
              "two seats were not up in 2026.")],
           [holder("Jared Felch", "jared-felch"),
            holder("Brian Divelbliss", "brian-divelbliss"),
            holder("Karla Nuissl", "karla-nuissl"),
            holder("Florence Smith", "florence-smith"),
            holder("Kris Hayward", "kris-hayward")]),
    office("moderator", "Moderator", "Berlin Town Moderator", 1,
           [ch105("section 42(1) provides for the election of a "
                  "Moderator from the floor for a one-year term. "
                  "The town's 2024 annual report names Paul Gillies "
                  "with a term printed as expiring in 2025, and no "
                  "current official source publishes the holder, "
                  "so none is recorded.")]),
    office("town-clerk", "Town Clerk", "Berlin Town Clerk", 1,
           [ch105("section 44(b) makes the Town Clerk an office "
                  "appointed by the Selectboard; the membership "
                  "is recorded as appointed."),
            S(BERLIN_CLERK_PAGE, "Town of Berlin official website, "
              "Town Clerk page: 'Town Clerk: Rachel Giroux'."),
            guide("lists Rachel Giroux as Town Clerk of Berlin.")],
           [holder("Rachel Giroux", "rachel-giroux",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer", "Berlin Town Treasurer", 1,
           [ch105("section 44(b) makes the Treasurer an office "
                  "appointed by the Selectboard; the membership "
                  "is recorded as appointed."),
            S(BERLIN_TREAS_PAGE, "Town of Berlin official website, "
              "Treasurer page: 'Town Treasurer/Delinquent Tax "
              "Collector: Callie Streeter'."),
            guide("lists Callie Streeter as Town Treasurer of "
                  "Berlin.")],
           [holder("Callie Streeter", "callie-streeter",
                   how_seated="appointed")]),
    office("collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
           "Berlin Collector of Delinquent Taxes", 1,
           [ch105("section 44(b) makes the Collector of "
                  "Delinquent Taxes an office appointed by the "
                  "Selectboard; the membership is recorded as "
                  "appointed."),
            S(BERLIN_TREAS_PAGE, "Town of Berlin official website, "
              "Treasurer page: 'Town Treasurer/Delinquent Tax "
              "Collector: Callie Streeter'.")],
           [holder("Callie Streeter", "callie-streeter",
                   how_seated="appointed")]),
    office("auditor", "Auditor", "Berlin Town Auditors", 3,
           [ch105("sections 41 and 42(4) keep in office such "
                  "other town officers as are provided by law; "
                  "17 V.S.A. section 2646 provides for the "
                  "election of auditors. No official Berlin "
                  "source publishes the holders, so none are "
                  "recorded.")]),
    office("first-constable", "First Constable", "Berlin First Constable", 1,
           [ch105("sections 41 and 42(4) keep in office such "
                  "other town officers as are provided by law; "
                  "17 V.S.A. section 2646 provides for the "
                  "election of a first constable. No official "
                  "Berlin source publishes the holder, so none "
                  "is recorded.")]),
    office("town-agent", "Town Agent", "Berlin Town Agent", 1,
           [ch105("sections 41 and 42(4) keep in office such "
                  "other town officers as are provided by law; "
                  "17 V.S.A. section 2646 provides for the "
                  "election of a town agent. No official Berlin "
                  "source publishes the holder, so none is "
                  "recorded.")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Berlin Justices of the Peace", 10,
           [jp_src("lists ten Berlin justices of the peace: "
                   "Zachary Cockrum, Robert \"Joey\" Conner, "
                   "Matthew Levin, Alida Van Den Berg, Margaret "
                   "Monley, Muriel Morse, Colette Page, Guy Page, "
                   "Susan Rich, and Judith Wernecke.")],
           [holder("Zachary Cockrum", "zachary-cockrum"),
            holder("Robert Conner", "robert-conner",
                   ballot_name='Robert "Joey" Conner'),
            holder("Matthew Levin", "matthew-levin"),
            holder("Alida Van Den Berg", "alida-van-den-berg"),
            holder("Margaret Monley", "margaret-monley"),
            holder("Muriel Morse", "muriel-morse"),
            holder("Colette Page", "colette-page"),
            holder("Guy Page", "guy-page"),
            holder("Susan Rich", "susan-rich"),
            holder("Judith Wernecke", "judith-wernecke")]),
], jp=jp_election(
    "berlin-vt", "Town of Berlin", 10,
    "lists ten Berlin justices of the peace for the 2025-2026 "
    "term; they are the winners of the November 5, 2024 election "
    "for the office. The listing publishes no vote totals and "
    "no party designations for justices of the peace.")))

# ------------------------------------------------------------- Bethel
BETHEL_SB_PAGE = {
    "url": "https://townofbethelvt.com/selectboard",
    "note": "PLACEHOLDER",
}
BETHEL_OFFICIALS = {
    "url": "https://townofbethelvt.com/other-elected-officials",
    "note": "PLACEHOLDER",
}
BETHEL_REPORT = {
    "url": "https://townofbethelvt.com/vertical/sites/%7B46C5C479-45BC-4485-9BD0-06530D0ACFB2%7D/uploads/PDF_Town_Report.pdf",
    "note": "PLACEHOLDER",
}


def bethel_report(what):
    return S(BETHEL_REPORT, f"Town of Bethel FY2025 Town Report: "
             f"{what}")


SPECS.append(spec("bethel", "Town of Bethel", [
    office("selectboard", "Selectboard Member", "Bethel Selectboard", 5,
           [S(BETHEL_SB_PAGE, "Town of Bethel official website, "
              "Selectboard page: lists Denise Guilmette (Chair), "
              "David Eddy, Jordan Garrow, Jed Scott, and Ben "
              "Roberts, with term expirations running to 2027, "
              "2028, and 2029."),
            sb_dir("lists four of the five Bethel Selectboard "
                  "members (Guilmette, Eddy, Garrow, and Benjamin "
                  "Roberts); it omits Jed Scott, whom the town's "
                  "own Selectboard page lists as the fifth member.")],
           [holder("Denise Guilmette", "denise-guilmette"),
            holder("David Eddy", "david-eddy"),
            holder("Jordan Garrow", "jordan-garrow"),
            holder("Jed Scott", "jed-scott"),
            holder("Ben Roberts", "ben-roberts")]),
    office("town-clerk", "Town Clerk", "Bethel Town Clerk", 1,
           [guide("lists Pamela Brown as Town Clerk of Bethel "
                  "and as Town Treasurer of Bethel."),
            bethel_report("'Elected Officials' table (report "
                          "p. 52) lists Pamela Brown as Town Clerk "
                          "and Town Treasurer. The March 3, 2026 "
                          "Town Meeting Warning (report pp. 4-5) "
                          "elects the clerk and treasurer for "
                          "one-year terms; the town publishes no "
                          "2026 results.")],
           [holder("Pamela Brown", "pamela-brown")]),
    office("town-treasurer", "Town Treasurer", "Bethel Town Treasurer", 1,
           [guide("lists Pamela Brown as Town Clerk of Bethel "
                  "and as Town Treasurer of Bethel."),
            bethel_report("'Elected Officials' table (report "
                          "p. 52) lists Pamela Brown as Town Clerk "
                          "and Town Treasurer.")],
           [holder("Pamela Brown", "pamela-brown")]),
    office("moderator", "Moderator", "Bethel Town Moderator", 1,
           [S(BETHEL_OFFICIALS, "Town of Bethel official website, "
              "'Other Elected Officials' page: lists Dana "
              "Cole-Levesque as Moderator."),
            bethel_report("'Elected Officials' table lists Dana "
                          "Cole-Levesque as Moderator.")],
           [holder("Dana Cole-Levesque", "dana-cole-levesque")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Bethel Trustees of Public Funds", 3,
           [S(BETHEL_OFFICIALS, "Town of Bethel official website, "
              "'Other Elected Officials' page: lists the Trustees "
              "of Public Funds as Eric Benson (term expires "
              "2028), Sandy Farrell (term expires 2026), and "
              "Scott Putney (term expires 2026). The FY2025 Town "
              "Report prints 'Rick Benson' for the 2028 seat; "
              "the current website form is recorded. The Farrell "
              "and Putney seats stood for election in March "
              "2026 and the town publishes no results, so only "
              "Benson is recorded.")],
           [holder("Eric Benson", "eric-benson")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Bethel Justices of the Peace", 7,
           [jp_src("lists seven Bethel justices of the peace: "
                   "Lisa Campbell, Cathy Day, Eleanor Griffin, "
                   "Caleb Harwood, Mark Heckmann, D Gene Kraus, "
                   "and Kirk White."),
            S(BETHEL_OFFICIALS, "Town of Bethel official website, "
              "'Other Elected Officials' page: lists the same "
              "seven justices of the peace (in shortened forms: "
              "Gene Kraus, Ele Griffin, Mark Heckman).")],
           [holder("Lisa Campbell", "lisa-campbell"),
            holder("Cathy Day", "cathy-day"),
            holder("Eleanor Griffin", "eleanor-griffin"),
            holder("Caleb Harwood", "caleb-harwood"),
            holder("Mark Heckmann", "mark-heckmann"),
            holder("D Gene Kraus", "d-gene-kraus"),
            holder("Kirk White", "kirk-white",
                   existing_person_id="ocd-person/a62311b4-5514-531c-9143-281c700774cb")]),
], jp=jp_election(
    "bethel-vt", "Town of Bethel", 7,
    "lists seven Bethel justices of the peace for the 2025-2026 "
    "term; they are the winners of the November 5, 2024 election "
    "for the office. The listing publishes no vote totals and "
    "no party designations for justices of the peace.")))

# ------------------------------------------------------------- Bolton
BOLTON_SB_PAGE = {
    "url": "https://boltonvt.com/boards/selectboard/",
    "note": "PLACEHOLDER",
}
BOLTON_REPORT = {
    "url": "https://boltonvt.com/wp-content/uploads/2026/02/Bolton-2026-Town-Report.pdf",
    "note": "PLACEHOLDER",
}


def bolton_report(what):
    return S(BOLTON_REPORT, f"Town of Bolton 2026 Town Report: "
             f"{what}")


SPECS.append(spec("bolton", "Town of Bolton", [
    office("selectboard", "Selectboard Member", "Bolton Selectboard", 5,
           [S(BOLTON_SB_PAGE, "Town of Bolton official website, "
              "Select Board page: lists Victoria Raymond (Chair), "
              "Rich Reid (Vice-Chair), Paula Gervia, Ryan "
              "Farrell, and Mica Cassara, with term expirations "
              "running to 2027, 2028, and 2029. (The Secretary "
              "of State's directory publishes no Bolton roster.) "
              "The 2026 Town Report's officials table prints "
              "stale names ('Victoria Haler', 'Leah Scott') that "
              "the current Select Board page supersedes.")],
           [holder("Victoria Raymond", "victoria-raymond"),
            holder("Rich Reid", "rich-reid"),
            holder("Paula Gervia", "paula-gervia"),
            holder("Ryan Farrell", "ryan-farrell"),
            holder("Mica Cassara", "mica-cassara")]),
    office("town-clerk", "Town Clerk", "Bolton Town Clerk", 1,
           [guide("lists Michael Webber as Town Clerk of Bolton "
                  "and as Town Treasurer of Bolton."),
            bolton_report("'ELECTED TOWN OFFICIALS' table "
                          "(report p. 4) lists Michael Webber as "
                          "Town Clerk and Town Treasurer (elected "
                          "2024, three-year terms).")],
           [holder("Michael Webber", "michael-webber")]),
    office("town-treasurer", "Town Treasurer", "Bolton Town Treasurer", 1,
           [guide("lists Michael Webber as Town Clerk of Bolton "
                  "and as Town Treasurer of Bolton."),
            bolton_report("'ELECTED TOWN OFFICIALS' table "
                          "(report p. 4) lists Michael Webber as "
                          "Town Clerk and Town Treasurer (elected "
                          "2024, three-year terms).")],
           [holder("Michael Webber", "michael-webber")]),
    office("moderator", "Moderator", "Bolton Town Moderator", 1,
           [bolton_report("'ELECTED TOWN OFFICIALS' table lists "
                          "Leslie Petch as Town Moderator (elected "
                          "2025, one-year term expiring 2026). The "
                          "seat stood for election in March 2026 "
                          "and the town publishes no outcome, so "
                          "no holder is recorded.")]),
    office("collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
           "Bolton Collector of Delinquent Taxes", 1,
           [bolton_report("'Hired and Appointed Town Officials' "
                          "table (report p. 5) lists the "
                          "Delinquent Tax Collector as Michael "
                          "Webber, appointed 2024; the membership "
                          "is recorded as appointed.")],
           [holder("Michael Webber", "michael-webber",
                   how_seated="appointed")]),
    office("constable", "Town Constable", "Bolton Town Constable", 1,
           [bolton_report("'Hired and Appointed Town Officials' "
                          "table (report p. 5) lists the Town "
                          "Constable as a vacant appointed position; "
                          "the office is recorded with no holder.")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Bolton Cemetery Commission", 3,
           [bolton_report("'ELECTED TOWN OFFICIALS' table lists "
                          "the Cemetery Commission as Penny Tinker "
                          "(term expiring 2028) and Cheryl "
                          "Mendicino (term expiring 2027), with "
                          "the third seat vacant, so only Tinker "
                          "and Mendicino are recorded.")],
           [holder("Penny Tinker", "penny-tinker"),
            holder("Cheryl Mendicino", "cheryl-mendicino")]),
    office("grand-juror", "Grand Juror", "Bolton Grand Juror", 1,
           [statute2646("a grand juror"),
            bolton_report("the report's elected and appointed "
                          "officer tables list no grand juror, "
                          "and no other official source publishes "
                          "the holder, so none is recorded.")]),
    office("town-agent", "Town Agent", "Bolton Town Agent", 1,
           [statute2646("a town agent to prosecute and defend suits"),
            bolton_report("the report's elected and appointed "
                          "officer tables list no town agent, "
                          "and no other official source publishes "
                          "the holder, so none is recorded.")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Bolton Justices of the Peace", 5,
           [bolton_report("'ELECTED TOWN OFFICIALS' table lists "
                          "the Justices of the Peace elected in "
                          "2024 (two-year terms) as Paula Gervia, "
                          "Rich Reid, John Devine, Steve Diglio, "
                          "and Jane Agran."),
            jp_src("the listing's text prints only first names "
                   "for Bolton (Brenda, Paula, Richard, John, "
                   "Steve, with surnames not extractable). Four "
                   "match the town report's slate; the fifth "
                   "first name, 'Brenda', does not match the town "
                   "report's Jane Agran and is unexplained. The "
                   "town report, the official source publishing "
                   "full names, governs Bolton's slate.")],
           [holder("Paula Gervia", "paula-gervia"),
            holder("Rich Reid", "rich-reid"),
            holder("John Devine", "john-devine"),
            holder("Steve Diglio", "steve-diglio"),
            holder("Jane Agran", "jane-agran")]),
], jp=jp_election(
    "bolton-vt", "Town of Bolton", 5,
    "the listing's text prints only first names for Bolton, so "
    "the winners are recorded from the Town of Bolton 2026 Town "
    "Report (see the post's sources). They are the winners of "
    "the November 5, 2024 election for the office.",
    extra_sources=[bolton_report(
        "'ELECTED TOWN OFFICIALS' table lists the Justices of "
        "the Peace elected in 2024 as Paula Gervia, Rich Reid, "
        "John Devine, Steve Diglio, and Jane Agran.")])))

# ------------------------------------------------------------- Bradford
BRADFORD_RETURN = {
    "url": "https://cms2.revize.com/revize/bradford/documents/Departments/Town%20Clerk/Official%20Return%20of%20Votes%2003-03-2026%20Annual%20Town%20Meeting.pdf",
    "note": "PLACEHOLDER",
}
BRADFORD_TREAS_PAGE = {
    "url": "https://bradford-vt.us/government/departments/town_treasurer.php",
    "note": "PLACEHOLDER",
}
BRADFORD_CLERK_PAGE = {
    "url": "https://bradford-vt.us/government/departments/town_clerk.php",
    "note": "PLACEHOLDER",
}
BRADFORD_LISTERS = {
    "url": "https://bradford-vt.us/government/departments/listers.php",
    "note": "PLACEHOLDER",
}
BRADFORD_AUDITORS = {
    "url": "https://bradford-vt.us/government/departments/auditors.php",
    "note": "PLACEHOLDER",
}
BRADFORD_JP_PAGE = {
    "url": "https://bradford-vt.us/government/departments/justices_of_the_peace.php",
    "note": "PLACEHOLDER",
}
BRADFORD_TPF_PAGE = {
    "url": "https://bradford-vt.us/government/departments/trustees_of_public_funds.php",
    "note": "PLACEHOLDER",
}


def bradford_return(what):
    return S(BRADFORD_RETURN, "Town of Bradford, 'Official Return "
             "of Votes, Annual Town Meeting' (March 3, 2026, "
             f"certified): {what}")


SPECS.append(spec("bradford", "Town of Bradford", [
    office("selectboard", "Selectboard Member", "Bradford Selectboard", 5,
           [sb_dir("lists five Bradford Selectboard members: Josh "
                   "Allen (Vice Chair), Meroa Benjamin (Chair), "
                   "Jean Carlan, Jarrod Kosakowski, and Carole "
                   "Taylor."),
            bradford_return("Josh Allen (199), Jarrod Kosakowski "
                            "(208), and Jean Carlan (182) won the "
                            "three Selectboard seats filled in "
                            "2026.")],
           [holder("Josh Allen", "josh-allen"),
            holder("Meroa Benjamin", "meroa-benjamin"),
            holder("Jean Carlan", "jean-carlan"),
            holder("Jarrod Kosakowski", "jarrod-kosakowski"),
            holder("Carole Taylor", "carole-taylor")]),
    office("town-clerk", "Town Clerk", "Bradford Town Clerk", 1,
           [bradford_return("Nikki Tomlinson (224) won the Town "
                            "Clerk contest (three-year term)."),
            S(BRADFORD_CLERK_PAGE, "Town of Bradford official "
              "website (bradford-vt.us), Town Clerk page: lists "
              "'Nikki Tomlinson, Town Clerk'."),
            guide("lists Nikki Tomlinson as Town Clerk of "
                  "Bradford (and as interim Treasurer; see the "
                  "treasurer post's sources).")],
           [holder("Nikki Tomlinson", "nikki-tomlinson")]),
    office("town-treasurer", "Town Treasurer", "Bradford Town Treasurer", 1,
           [S(BRADFORD_TREAS_PAGE, "Town of Bradford official "
              "website (bradford-vt.us), 'Treasurer & Assistant "
              "Treasurer' page: 'Jessica Chase, Town Treasurer'. "
              "The Secretary of State's town treasurer contact "
              "spreadsheet (June 12, 2026) still lists Nikki "
              "Tomlinson; the town's current page governs."),
            bradford_return("the Treasurer contest had no ballot "
                            "candidate; the leading write-in was "
                            "Nikki Tomlinson (46), who did not "
                            "take the seat. Chase was seated after "
                            "the election; the membership is "
                            "recorded as appointed.")],
           [holder("Jessica Chase", "jessica-chase",
                   how_seated="appointed")]),
    office("moderator", "Moderator", "Bradford Town Moderator", 1,
           [bradford_return("the Moderator contest (one-year "
                            "term) was won by write-in candidate "
                            "Paul Hunt (76), the leading write-in; "
                            "the town identifies Hunt as its "
                            "current Moderator.")],
           [holder("Paul Hunt", "paul-hunt")]),
    office("lister", "Lister", "Bradford Board of Listers", 3,
           [S(BRADFORD_LISTERS, "Town of Bradford official "
              "website, Listers page: lists Blakelee Danforth "
              "(term expires March 2028) and Doug Miller (term "
              "expires March 2029), with the third seat vacant."),
            bradford_return("Doug Miller (216) won the Lister "
                            "contest filled in 2026. The second "
                            "2026 lister contest was led by "
                            "write-in Marcey Carver (4), whom the "
                            "town's listers page shows as not "
                            "seated (the seat is listed vacant), "
                            "so she is not recorded.")],
           [holder("Blakelee Danforth", "blakelee-danforth"),
            holder("Doug Miller", "doug-miller")]),
    office("auditor", "Auditor", "Bradford Town Auditors", 3,
           [S(BRADFORD_AUDITORS, "Town of Bradford official "
              "website, Auditors page: lists Brianna Haley (term "
              "expires March 2028), Alexandra Barlow "
              "('Appointed 2026', term expires March 2029), and "
              "Bess Friend (term expires March 2030 as "
              "printed). Barlow's membership is recorded as "
              "appointed, as the page states."),
            bradford_return("the 2026 Auditor contests were led "
                            "by write-ins Elizabeth Friend (20) "
                            "and Katelynn Pike (40). Friend is "
                            "the 'Bess Friend' of the town's "
                            "auditors page; Pike is not on the "
                            "town's roster and is not recorded.")],
           [holder("Brianna Haley", "brianna-haley"),
            holder("Alexandra Barlow", "alexandra-barlow",
                   how_seated="appointed"),
            holder("Bess Friend", "bess-friend")]),
    office("collector-of-taxes", "Collector of Taxes",
           "Bradford Collector of Taxes", 1,
           [bradford_return("the Collector of Current Taxes "
                            "contest (one-year term) was led by "
                            "write-in Nikki Tomlinson (49). No "
                            "town page names the holder, and "
                            "Tomlinson's write-in lead for "
                            "Treasurer did not seat her in that "
                            "office, so no holder is recorded "
                            "from the write-in tally alone.")]),
    office("collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
           "Bradford Collector of Delinquent Taxes", 1,
           [S(BRADFORD_TREAS_PAGE, "Town of Bradford official "
              "website, 'Treasurer & Assistant Treasurer' page: "
              "'Nikki Tomlinson, Delinquent Tax Collector'."),
            bradford_return("Tomlinson (44) was also the leading "
                            "write-in in the Collector of "
                            "Delinquent Taxes contest.")],
           [holder("Nikki Tomlinson", "nikki-tomlinson")]),
    office("grand-juror", "Grand Juror", "Bradford Grand Juror", 1,
           [bradford_return("Gary Moore (215) won the Grand "
                            "Juror contest (one-year term).")],
           [holder("Gary Moore", "gary-moore")]),
    office("town-agent", "Town Agent", "Bradford Town Agent", 1,
           [bradford_return("Gary Moore (202) won the Town "
                            "Agent contest (one-year term).")],
           [holder("Gary Moore", "gary-moore")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Bradford Trustees of Public Funds", 3,
           [bradford_return("one Trustee of Public Funds seat "
                            "(three-year term) was filled in 2026, "
                            "led by write-in Tony Brainerd (44)."),
            S(BRADFORD_TPF_PAGE, "Town of Bradford official "
              "website, Trustees of Public Funds page: names no "
              "trustees. No official source publishes the "
              "current holders, so none are recorded.")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Bradford Justices of the Peace", 10,
           [jp_src("lists ten Bradford justices of the peace: "
                   "Daniel Perry III, Heather Peets, Nathan "
                   "Peets, Carole Taylor, Gary Moore, Lawrence "
                   "Coffin, Patrick Harrigan, Monique Priestley, "
                   "Leonard Dobbins, and Jonathan Stimson."),
            S(BRADFORD_JP_PAGE, "Town of Bradford official "
              "website, Justices of the Peace page: lists eight "
              "of the ten (omitting Harrigan and Dobbins) for "
              "the term February 1, 2025 - January 31, 2027; "
              "the Secretary of State's listing governs the "
              "slate.")],
           [holder("Daniel Perry III", "daniel-perry-iii"),
            holder("Heather Peets", "heather-peets"),
            holder("Nathan Peets", "nathan-peets"),
            holder("Carole Taylor", "carole-taylor"),
            holder("Gary Moore", "gary-moore"),
            holder("Lawrence Coffin", "lawrence-coffin"),
            holder("Patrick Harrigan", "patrick-harrigan"),
            holder("Monique Priestley", "monique-priestley",
                   existing_person_id="ocd-person/f022c8ed-582e-5cae-9ab5-7118a0de9a51"),
            holder("Leonard Dobbins", "leonard-dobbins"),
            holder("Jonathan Stimson", "jonathan-stimson")]),
], jp=jp_election(
    "bradford-vt", "Town of Bradford", 10,
    "lists ten Bradford justices of the peace for the 2025-2026 "
    "term; they are the winners of the November 5, 2024 election "
    "for the office. The listing publishes no vote totals and "
    "no party designations for justices of the peace.")))

# ------------------------------------------------------------- Braintree
BRAINTREE_MINUTES = {
    "url": "https://braintreevt.gov/wp-content/uploads/2026/03/Braintree-Town-Meeting-Minutes-2026.pdf",
    "note": "PLACEHOLDER",
}
BRAINTREE_CLERK_PAGE = {
    "url": "https://braintreevt.gov/services/town-clerk/",
    "note": "PLACEHOLDER",
}


def braintree_minutes(what):
    return S(BRAINTREE_MINUTES, "Town of Braintree, Town Meeting "
             "Minutes (March 3, 2026; posted on the town's "
             "official website as draft/unapproved minutes of "
             f"the floor elections): {what}")


SPECS.append(spec("braintree", "Town of Braintree", [
    office("selectboard", "Selectboard Member", "Braintree Selectboard", 5,
           [sb_dir("lists five Braintree Selectboard members: "
                   "Loren Bent, Chelsie Brown, Daniel Burson "
                   "(Chair), Colin Evans, and Lou Helmuth."),
            braintree_minutes("Article 5 elected Colin Evans "
                              "(three-year term) and Loren Bent "
                              "(two-year term) to the Selectboard "
                              "in 2026.")],
           [holder("Loren Bent", "loren-bent"),
            holder("Chelsie Brown", "chelsie-brown"),
            holder("Daniel Burson", "daniel-burson"),
            holder("Colin Evans", "colin-evans"),
            holder("Lou Helmuth", "lou-helmuth")]),
    office("town-clerk", "Town Clerk", "Braintree Town Clerk", 1,
           [S(BRAINTREE_CLERK_PAGE, "Town of Braintree official "
              "website, Town Clerk page: 'Town Clerk & Treasurer: "
              "Jessica Brassard'."),
            guide("lists Jessica Brassard as Town Clerk of "
                  "Braintree and as Town Treasurer of Braintree.")],
           [holder("Jessica Brassard", "jessica-brassard")]),
    office("town-treasurer", "Town Treasurer", "Braintree Town Treasurer", 1,
           [S(BRAINTREE_CLERK_PAGE, "Town of Braintree official "
              "website, Town Clerk page: 'Town Clerk & Treasurer: "
              "Jessica Brassard'."),
            guide("lists Jessica Brassard as Town Clerk of "
                  "Braintree and as Town Treasurer of Braintree.")],
           [holder("Jessica Brassard", "jessica-brassard")]),
    office("moderator", "Moderator", "Braintree Town Moderator", 1,
           [braintree_minutes("Article 1 elected Jackson Evans "
                              "Moderator for 2026.")],
           [holder("Jackson Evans", "jackson-evans")]),
    office("lister", "Lister", "Braintree Board of Listers", 3,
           [braintree_minutes("Article 5 elected Grace Persons "
                              "Lister (three-year term) in 2026. "
                              "The other two lister seats' "
                              "holders are published in no "
                              "official source, so only Persons "
                              "is recorded.")],
           [holder("Grace Persons", "grace-persons")]),
    office("auditor", "Auditor", "Braintree Town Auditors", 3,
           [braintree_minutes("Article 5 elected Allison Jassen "
                              "Auditor (three-year term) in 2026. "
                              "The other two auditor seats' "
                              "holders are published in no "
                              "official source, so only Jassen "
                              "is recorded.")],
           [holder("Allison Jassen", "allison-jassen")]),
    office("collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
           "Braintree Collector of Delinquent Taxes", 1,
           [braintree_minutes("Article 5 elected Jessica "
                              "Brassard Delinquent Tax Collector "
                              "(one-year term) in 2026.")],
           [holder("Jessica Brassard", "jessica-brassard")]),
    office("first-constable", "First Constable", "Braintree First Constable", 1,
           [braintree_minutes("Article 5 elected Stephen "
                              "Brassard First Constable (one-year "
                              "term) in 2026 (a distinct person "
                              "from Town Clerk Jessica Brassard).")],
           [holder("Stephen Brassard", "stephen-brassard")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Braintree Cemetery Commission", 3,
           [braintree_minutes("Article 5 elected Nancy "
                              "Burchfield Cemetery Commissioner "
                              "(three-year term) in 2026. The "
                              "other seats' holders are "
                              "published in no official source, "
                              "so only Burchfield is recorded.")],
           [holder("Nancy Burchfield", "nancy-burchfield")]),
    office("grand-juror", "Grand Juror", "Braintree Grand Juror", 1,
           [statute2646("a grand juror"),
            braintree_minutes("the Article 5 officer elections "
                              "include no grand juror, and no "
                              "other official source publishes "
                              "the holder, so none is recorded. "
                              "(The same meeting eliminated the "
                              "Trustee of Public Funds office by "
                              "vote, Article 3; no post is "
                              "created for it.)")]),
    office("town-agent", "Town Agent", "Braintree Town Agent", 1,
           [statute2646("a town agent to prosecute and defend suits"),
            braintree_minutes("the Article 5 officer elections "
                              "include no town agent, and no "
                              "other official source publishes "
                              "the holder, so none is recorded.")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Braintree Justices of the Peace", 5,
           [jp_src("lists five Braintree justices of the peace: "
                   "Richard Bowen, Robert Moyer, Sherri "
                   "Richardson, Katja Evans, and Jackson Evans.")],
           [holder("Richard Bowen", "richard-bowen"),
            holder("Robert Moyer", "robert-moyer"),
            holder("Sherri Richardson", "sherri-richardson"),
            holder("Katja Evans", "katja-evans"),
            holder("Jackson Evans", "jackson-evans")]),
], jp=jp_election(
    "braintree-vt", "Town of Braintree", 5,
    "lists five Braintree justices of the peace for the "
    "2025-2026 term; they are the winners of the November 5, "
    "2024 election for the office. The listing publishes no "
    "vote totals and no party designations for justices of "
    "the peace.")))

# ------------------------------------------------------------- Brandon
BRANDON_RETURN = {
    "url": "https://www.brandonvermont.gov/DocumentCenter/View/713",
    "note": "PLACEHOLDER",
}
BRANDON_WARNING = {
    "url": "https://www.brandonvermont.gov/DocumentCenter/View/643/2026-03-03-Town-Meeting-Balloting",
    "note": "PLACEHOLDER",
}
BRANDON_TPF_PAGE = {
    "url": "https://www.brandonvermont.gov/1219/Trustees-of-Public-Funds",
    "note": "PLACEHOLDER",
}


def brandon_return(what):
    return S(BRANDON_RETURN, "Town of Brandon, 'Australian "
             "Ballot Official Return of Votes', Town Meeting "
             f"election (March 3, 2026, certified): {what}")


SPECS.append(spec("brandon", "Town of Brandon", [
    office("selectboard", "Selectboard Member", "Brandon Selectboard", 5,
           [sb_dir("lists five Brandon Selectboard members: Doug "
                   "Bailey, Brian Coolidge, Ralph Ethier, Jeff "
                   "Haylon, and Cecil Reniche-Smith."),
            brandon_return("Brian Coolidge (625) won the "
                           "three-year seat and Cecil "
                           "Reniche-Smith (584) and Jeff Haylon "
                           "(561) won the two one-year seats "
                           "filled in 2026.")],
           [holder("Doug Bailey", "doug-bailey"),
            holder("Brian Coolidge", "brian-coolidge"),
            holder("Ralph Ethier", "ralph-ethier"),
            holder("Jeff Haylon", "jeff-haylon"),
            holder("Cecil Reniche-Smith", "cecil-reniche-smith")]),
    office("town-clerk", "Town Clerk", "Brandon Town Clerk", 1,
           [brandon_return("Sue Gage (757) won the Town Clerk "
                           "contest (three-year term)."),
            guide("lists Susan Gage as Town Clerk of Brandon "
                  "and as Town Treasurer of Brandon.")],
           [holder("Susan Gage", "susan-gage")]),
    office("town-treasurer", "Town Treasurer", "Brandon Town Treasurer", 1,
           [brandon_return("Sue Gage (746) won the Town "
                           "Treasurer contest (three-year term)."),
            guide("lists Susan Gage as Town Clerk of Brandon "
                  "and as Town Treasurer of Brandon.")],
           [holder("Susan Gage", "susan-gage")]),
    office("moderator", "Moderator", "Brandon Town Moderator", 1,
           [brandon_return("Bill Moore (212) won the Moderator "
                           "contest (one-year term) as a write-in "
                           "candidate."),
            S(BRANDON_WARNING, "Town of Brandon, 2026 Town "
              "Meeting election warning (Article 1): the "
              "offices Brandon elects are Moderator, "
              "Selectboard, Town Clerk, Town Treasurer, and "
              "Trustees of Public Funds only.")],
           [holder("Bill Moore", "bill-moore")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Brandon Trustees of Public Funds", 3,
           [brandon_return("Faith Daya (550) won the three-year "
                           "seat; Devon Fuller (213) won the "
                           "two-years-remaining seat and Tracy "
                           "Wyman (257) the one-year-remaining "
                           "seat, both as write-in candidates."),
            S(BRANDON_TPF_PAGE, "Town of Brandon official "
              "website, Trustees of Public Funds page: lists "
              "Faith Daya (term to 2029), Devon Fuller (term "
              "to 2028), and Tracy Wyman (term to 2027).")],
           [holder("Faith Daya", "faith-daya"),
            holder("Devon Fuller", "devon-fuller"),
            holder("Tracy Wyman", "tracy-wyman")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Brandon Justices of the Peace", 12,
           [jp_src("lists twelve Brandon justices of the peace: "
                   "Doug Bailey, Del Cook, Sally Cook, Bud "
                   "Coolidge, Wendy Rowe-Feldman, Laura "
                   "Peterson, John Peterson, Kathy Clark, "
                   "Hillary Knapp, Bill Moore, Todd Nielsen, "
                   "and Patricia Welch. Bud Coolidge is a "
                   "distinct person from Selectboard member "
                   "Brian Coolidge.")],
           [holder("Doug Bailey", "doug-bailey"),
            holder("Del Cook", "del-cook"),
            holder("Sally Cook", "sally-cook"),
            holder("Bud Coolidge", "bud-coolidge"),
            holder("Wendy Rowe-Feldman", "wendy-rowe-feldman"),
            holder("Laura Peterson", "laura-peterson"),
            holder("John Peterson", "john-peterson"),
            holder("Kathy Clark", "kathy-clark"),
            holder("Hillary Knapp", "hillary-knapp"),
            holder("Bill Moore", "bill-moore"),
            holder("Todd Nielsen", "todd-nielsen",
                   existing_person_id="ocd-person/e8841634-b814-57af-91a4-6dc8bdbb97f6"),
            holder("Patricia Welch", "patricia-welch")]),
], jp=jp_election(
    "brandon-vt", "Town of Brandon", 12,
    "lists twelve Brandon justices of the peace for the "
    "2025-2026 term; they are the winners of the November 5, "
    "2024 election for the office. The listing publishes no "
    "vote totals and no party designations for justices of "
    "the peace.")))

# ------------------------------------------------------------- Brattleboro
CH107_22 = {
    "url": "https://legislature.vermont.gov/statutes/section/24APPENDIX/107/00002.02",
    "note": "PLACEHOLDER",
}
BRATT_REPORT = {
    "url": "https://drive.google.com/file/d/1dl_OO1Gj9xKwwTtYcjxR_LOjZBbHMNZg/view",
    "note": "PLACEHOLDER",
}
BRATT_RESULTS = {
    "url": "https://drive.google.com/file/d/1Cm-lMY13NZkT3fOYowYeCvY_-ECsXPU5/view",
    "note": "PLACEHOLDER",
}
BRATT_LOCAL = {
    "url": "https://brattleboro.gov/elections/locally-elected-offices",
    "note": "PLACEHOLDER",
}


def ch107(what):
    return S(CH107_22, "Town of Brattleboro charter, 24 App. "
             f"V.S.A. ch. 107, section 2.2 (official text): {what}")


def bratt_results(what):
    return S(BRATT_RESULTS, "Town of Brattleboro, official "
             "March 3, 2026 election results (published by the "
             f"Town Clerk): {what}")


def bratt_report(what):
    return S(BRATT_REPORT, f"Town of Brattleboro 2025-2026 "
             f"Annual Report, 'Town Officers' (report p. 6): "
             f"{what}")


SPECS.append(spec("brattleboro", "Town of Brattleboro", [
    office("selectboard", "Selectboard Member", "Brattleboro Selectboard", 5,
           [sb_dir("lists five Brattleboro Selectboard members: "
                   "Peter Case, Amanda Ellis-Thurber (Vice "
                   "Chair), Isaac Evans-Frantz, Oscar Heller "
                   "(Chair), and Eleanor Mayo."),
            bratt_results("Amanda Ellis-Thurber (1,556) won the "
                          "three-year seat and Isaac "
                          "Evans-Frantz (1,462) and Eleanor "
                          "Mayo (1,255) won the one-year seats "
                          "filled in 2026."),
            ch107("section 2.2(2) provides for a Selectboard of "
                  "five members elected at large.")],
           [holder("Peter Case", "peter-case"),
            holder("Amanda Ellis-Thurber", "amanda-ellis-thurber"),
            holder("Isaac Evans-Frantz", "isaac-evans-frantz"),
            holder("Oscar Heller", "oscar-heller"),
            holder("Eleanor Mayo", "eleanor-mayo")]),
    office("moderator", "Moderator", "Brattleboro Town Moderator", 1,
           [ch107("section 2.2(7) provides for the election of "
                  "a Moderator for a one-year term."),
            bratt_results("David Gartenstein (1,911) won the "
                          "Moderator contest in 2026.")],
           [holder("David Gartenstein", "david-gartenstein")]),
    office("lister", "Lister", "Brattleboro Board of Listers", 3,
           [ch107("section 2.2(5) provides for a Board of three "
                  "listers elected at large, one each year for "
                  "three-year terms."),
            bratt_report("lists the Board of Listers as "
                         "Katherine Dowd (term to 2027), Heidi "
                         "Fischer (term to 2028), and Tom Franks "
                         "(term to 2026)."),
            bratt_results("Thomas \"Tom\" Franks (1,749) was "
                          "re-elected Lister (three-year term) "
                          "in 2026.")],
           [holder("Katherine Dowd", "katherine-dowd"),
            holder("Heidi Fischer", "heidi-fischer"),
            holder("Thomas Franks", "thomas-franks")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Brattleboro Trustees of Public Funds", 3,
           [ch107("section 2.2(6) provides for three trustees "
                  "of public funds elected at large, one each "
                  "year for three-year terms."),
            bratt_report("lists the Trustees of Public Funds "
                         "as Deborah Zak (term to 2027), Pamela "
                         "Matweecha (term to 2028), and "
                         "Katherine \"Kate\" John (term to "
                         "2026)."),
            bratt_results("Catherine \"Kate\" John (1,698) was "
                          "re-elected Trustee of Public Funds "
                          "(three-year term) in 2026. The two "
                          "town sources differ on her full first "
                          "name (Katherine/Catherine); the "
                          "common form Kate John is recorded.")],
           [holder("Deborah Zak", "deborah-zak"),
            holder("Pamela Matweecha", "pamela-matweecha"),
            holder("Kate John", "kate-john")]),
    office("first-constable", "First Constable", "Brattleboro First Constable", 1,
           [ch107("section 2.2(7) provides for the election of "
                  "a First Constable for a one-year term."),
            bratt_results("Gary Corey (1,642) won the First "
                          "Constable contest in 2026 (the "
                          "2025-2026 Annual Report showed the "
                          "first constable seat vacant and Corey "
                          "as Second Constable before the "
                          "election).")],
           [holder("Gary Corey", "gary-corey")]),
    office("second-constable", "Second Constable", "Brattleboro Second Constable", 1,
           [ch107("section 2.2(7) provides for the election of "
                  "a Second Constable for a one-year term."),
            bratt_results("the 2026 Second Constable contest "
                          "had no candidate and no declared "
                          "write-in winner, so no holder is "
                          "recorded.")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Brattleboro Justices of the Peace", 15,
           [jp_src("lists fifteen Brattleboro justices of the "
                   "peace: Jane Buckingham, Franklin Chrisco, "
                   "Diane Cooke, Richard Cooke, Ian Goodnow, "
                   "Peter Gould, William \"Bill\" Harvey, "
                   "Martha Healey-Nelson, Thomas \"Tom\" "
                   "Kuralt, John Lightfoot, Lee Madden, Mary "
                   "\"Beverly\" Miller, Kate O'Connor, Robert "
                   "Oeser, and Veronica Wheelock.")],
           [holder("Jane Buckingham", "jane-buckingham"),
            holder("Franklin Chrisco", "franklin-chrisco"),
            holder("Diane Cooke", "diane-cooke"),
            holder("Richard Cooke", "richard-cooke"),
            holder("Ian Goodnow", "ian-goodnow",
                   existing_person_id="ocd-person/45c5b3d3-d4bb-526d-ac70-b80081cbc6e0"),
            holder("Peter Gould", "peter-gould"),
            holder("William Harvey", "william-harvey",
                   ballot_name='William "Bill" Harvey'),
            holder("Martha Healey-Nelson", "martha-healey-nelson"),
            holder("Thomas Kuralt", "thomas-kuralt",
                   ballot_name='Thomas "Tom" Kuralt'),
            holder("John Lightfoot", "john-lightfoot"),
            holder("Lee Madden", "lee-madden"),
            holder("Mary Miller", "mary-miller",
                   ballot_name='Mary "Beverly" Miller'),
            holder("Kate O'Connor", "kate-oconnor"),
            holder("Robert Oeser", "robert-oeser"),
            holder("Veronica Wheelock", "veronica-wheelock")]),
], jp=jp_election(
    "brattleboro-vt", "Town of Brattleboro", 15,
    "lists fifteen Brattleboro justices of the peace for the "
    "2025-2026 term; they are the winners of the November 5, "
    "2024 election for the office. The listing publishes no "
    "vote totals and no party designations for justices of "
    "the peace.")))

# ------------------------------------------------------------- Bridgewater
BRIDGE_SB_PAGE = {
    "url": "https://www.bridgewater.vt.gov/selectboard",
    "note": "PLACEHOLDER",
}
BRIDGE_MINUTES = {
    "url": "https://www.bridgewater.vt.gov/vertical/sites/%7B562C3348-6A49-4470-9BE0-69A4BB072D18%7D/uploads/Town_Meeting_Minutes_2026.pdf",
    "note": "PLACEHOLDER",
}
BRIDGE_REPORT = {
    "url": "https://www.bridgewater.vt.gov/vertical/sites/%7B562C3348-6A49-4470-9BE0-69A4BB072D18%7D/uploads/FY_2024_Town_Report.pdf",
    "note": "PLACEHOLDER",
}
BRIDGE_BCA = {
    "url": "https://www.bridgewater.vt.gov/index.asp?SEC=DDDFC09F-02A1-4831-B8B6-DC6F91A63616",
    "note": "PLACEHOLDER",
}


def bridge_minutes(what):
    return S(BRIDGE_MINUTES, "Town of Bridgewater, Town "
             f"Meeting Minutes (March 3, 2026): {what}")


def bridge_report(what):
    return S(BRIDGE_REPORT, f"Town of Bridgewater FY2024 Town "
             f"Report, 'ELECTED TOWN OFFICERS' (report p. 9): "
             f"{what}")


SPECS.append(spec("bridgewater", "Town of Bridgewater", [
    office("selectboard", "Selectboard Member", "Bridgewater Selectboard", 3,
           [S(BRIDGE_SB_PAGE, "Town of Bridgewater official "
              "website, Selectboard page: lists Owen Astbury "
              "(Chair), Steve Tarleton, and Norman (Nope) "
              "Martin."),
            sb_dir("lists the same three Bridgewater "
                   "Selectboard members (Norman Martin)."),
            bridge_minutes("Article 5 re-elected Stephen "
                           "Tarleton (three-year term) in 2026.")],
           [holder("Owen Astbury", "owen-astbury"),
            holder("Steve Tarleton", "steve-tarleton"),
            holder("Norman Martin", "norman-martin")]),
    office("town-clerk", "Town Clerk", "Bridgewater Town Clerk", 1,
           [guide("lists Nancy Robinson as Town Clerk of "
                  "Bridgewater."),
            bridge_report("lists Nancy Robinson as Town Clerk "
                          "(term printed 2022-2025; Bridgewater "
                          "elects its clerk for three-year "
                          "terms, and the Secretary of State's "
                          "January 2026 Guide lists her "
                          "currently).")],
           [holder("Nancy Robinson", "nancy-robinson")]),
    office("town-treasurer", "Town Treasurer", "Bridgewater Town Treasurer", 1,
           [guide("lists Melissa Spear as Town Treasurer of "
                  "Bridgewater."),
            bridge_report("lists Melissa Spear as Town "
                          "Treasurer (term printed 2022-2025; "
                          "see the clerk post's note).")],
           [holder("Melissa Spear", "melissa-spear")]),
    office("moderator", "Moderator", "Bridgewater Town Moderator", 1,
           [bridge_minutes("Article 1 elected Greg Jenne "
                           "Moderator by voice vote in 2026.")],
           [holder("Gregory Jenne", "gregory-jenne")]),
    office("lister", "Lister", "Bridgewater Board of Listers", 3,
           [bridge_report("lists the Listers as Marsha Fraser "
                          "(term printed 2024-2025), Victoria "
                          "Young (2023-2026), and Kaleb McIntire "
                          "(2024-2027). Only McIntire's printed "
                          "term runs past the March 2026 town "
                          "meeting; the other two seats' "
                          "outcomes are published in no official "
                          "source, so only McIntire is "
                          "recorded.")],
           [holder("Kaleb McIntire", "kaleb-mcintire")]),
    office("collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
           "Bridgewater Collector of Delinquent Taxes", 1,
           [bridge_report("lists Mary Oldenburg as Delinquent "
                          "Tax Collector (term printed "
                          "2024-2027).")],
           [holder("Mary Oldenburg", "mary-oldenburg")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Bridgewater Cemetery Commission", 3,
           [bridge_report("lists the Cemetery Commissioners as "
                          "Roy (Butch) Wardwell (term printed "
                          "2022-2025), Gregory Jenne "
                          "(2023-2026), and Owen Astbury "
                          "(2024-2027)."),
            bridge_minutes("Article 5 elected Gregory Jenne "
                           "Cemetery Commissioner (three-year "
                           "term) in 2026. Wardwell's seat's "
                           "outcome after 2025 is published in "
                           "no official source, so only Jenne "
                           "and Astbury are recorded.")],
           [holder("Gregory Jenne", "gregory-jenne"),
            holder("Owen Astbury", "owen-astbury")]),
    office("constable", "Town Constable", "Bridgewater Town Constable", 1,
           [bridge_minutes("Article 5 elected W. John Blanchard "
                           "Town Constable (one-year term) in "
                           "2026."),
            bridge_report("lists Warren John Blanchard as Town "
                          "Constable (term printed 2024-2025).")],
           [holder("W. John Blanchard", "w-john-blanchard")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Bridgewater Trustees of Public Funds", 1,
           [bridge_report("lists a single Trustee of Public "
                          "Funds, Mary Oldenburg (term printed "
                          "2022-2025). The seat's outcome after "
                          "2025 is published in no official "
                          "source, so no holder is recorded.")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Bridgewater Justices of the Peace", 5,
           [jp_src("lists five Bridgewater justices of the "
                   "peace: Gregory Jenne, Gloria Martin, Donna "
                   "Williamson, Justin Wardwell, and Jerry "
                   "Oppenheimber (the listing's spelling)."),
            S(BRIDGE_BCA, "Town of Bridgewater official "
              "website, Board of Civil Authority page: lists "
              "the justices of the peace as Greg Jenne, Gloria "
              "Martin, Jerry Oppenheimer, Justin Wardwell, "
              "and Donna Williamson. The town prints "
              "'Oppenheimer' (also in the FY2024 Town "
              "Report); that form is recorded, with the "
              "Secretary of State listing's 'Oppenheimber' "
              "kept as the ballot name.")],
           [holder("Gregory Jenne", "gregory-jenne"),
            holder("Gloria Martin", "gloria-martin"),
            holder("Donna Williamson", "donna-williamson"),
            holder("Justin Wardwell", "justin-wardwell"),
            holder("Jerry Oppenheimer", "jerry-oppenheimer",
                   ballot_name="Jerry Oppenheimber")]),
], jp=jp_election(
    "bridgewater-vt", "Town of Bridgewater", 5,
    "lists five Bridgewater justices of the peace for the "
    "2025-2026 term; they are the winners of the November 5, "
    "2024 election for the office. The listing publishes no "
    "vote totals and no party designations for justices of "
    "the peace.")))

# ------------------------------------------------------------- emit
for s in SPECS:
    path = OUT / f"{s['place_slug']}.json"
    path.write_text(json.dumps(s, indent=1, ensure_ascii=False))
    print(f"WROTE {path}")
print(f"{len(SPECS)} specs")
