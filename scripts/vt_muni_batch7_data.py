#!/usr/bin/env python3
"""Batch 7 of the VT #163 municipal fan-out (alphabetical positions
61-70): Albany Village (HELD - no spec), Derby, Derby Center, Derby
Line, Dorset, Dover, Dummerston, Duxbury, East Haven, East
Montpelier.
Emits one JSON spec per buildable municipality for
build_vt_municipality.py. Research: vt_muni_batch7_research.md.

Albany Village remains HELD (batch-1 ruling, re-verified 2026-10-18):
no charter chapter, no official website or roster in any official
channel, factory holds it too. Nothing is minted for it.
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
                  f"(VT municipal batch 7); issue #163 "
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
                  f"# municipal fan-out batch 7; issue #163 "
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

# ---------------------------------------------------------------- Derby (town)
DERBY_REPORT = {
    "url": "https://derbyvt.org/wp-content/uploads/2026/02/2025-Annual-Town-Report-1.pdf",
    "note": "PLACEHOLDER",
}
DERBY_MINUTES = {
    "url": "https://derbyvt.org/wp-content/uploads/2026/07/2026-Annual-Town-School-District-Meeting-Minutes.pdf",
    "note": "PLACEHOLDER",
}
DERBY_DIR_PAGE = {
    "url": "https://derbyvt.org/municipal-officers/",
    "note": "PLACEHOLDER",
}


def derby_report(note):
    return S(DERBY_REPORT, "Town of Derby 2025 Annual Town Report "
             f"(derbyvt.org, February 2026): {note}")


def derby_minutes(note):
    return S(DERBY_MINUTES, "Town of Derby Annual Town Meeting "
             f"Minutes, March 2, 2026 (derbyvt.org): {note}")


def derby_dir_page(note):
    return S(DERBY_DIR_PAGE, "Town of Derby Municipal Directory page "
             f"(derbyvt.org, current): {note}")


def derby_spec():
    label = "Town of Derby"
    offices = [
        office("selectboard", "Selectboard Member", "Derby Selectboard", 5,
               [sb_dir("lists five Derby Selectboard members: Grant "
                       "Spates (Chair), Gwen Bailey-Rowe, Steve Gendreau, "
                       "Bradley Shattuck, and Brian Smith."),
                derby_report("the ELECTED TOWN OFFICIALS table lists "
                             "Grant Spates (3-year term expiring 2028), "
                             "Brad Shattuck (2027), Stephen Gendreau "
                             "(2-year term expiring 2027), Brian Smith "
                             "(term expiring 2026), and Lindsay Brainard "
                             "in the 2-year seat expiring 2026."),
                derby_minutes("the March 2, 2026 annual meeting record "
                              "and the directory agree that Gwen "
                              "Bailey-Rowe won the 2026 two-year seat "
                              "(Brainard did not run again) and Brian "
                              "Smith remains seated for the seat that "
                              "stood in 2026.")],
               [holder("Grant Spates", "grant-spates"),
                holder("Bradley Shattuck", "bradley-shattuck"),
                holder("Stephen Gendreau", "stephen-gendreau"),
                holder("Brian Smith", "brian-smith"),
                holder("Gwen Bailey-Rowe", "gwen-bailey-rowe")]),
        office("town-clerk", "Town Clerk", "Derby Town Clerk", 1,
               [derby_report("the ELECTED TOWN OFFICIALS table lists "
                             "Faye C. Morin as Town Clerk, elected to a "
                             "3-year term expiring 2028."),
                guide("lists Faye Morin as Town Clerk of Derby.")],
               [holder("Faye Morin", "faye-morin")]),
        office("town-treasurer", "Town Treasurer", "Derby Town Treasurer", 1,
               [derby_report("the ELECTED TOWN OFFICIALS table lists "
                             "Faye C. Morin as Town Treasurer, elected "
                             "to a 3-year term expiring 2028."),
                guide("lists Faye Morin as Town Treasurer of Derby.")],
               [holder("Faye Morin", "faye-morin")]),
        office("moderator", "Moderator", "Derby Moderator", 1,
               [derby_report("the officer table lists Douglas Spates "
                             "as Moderator with his elected term expired "
                             "2025 and marks him '(appointed)'."),
                derby_minutes("Douglas Spates presided as Moderator at "
                              "the March 2, 2026 annual meeting. The "
                              "March 3, 2026 ballot outcome for the "
                              "moderator seat is published nowhere and "
                              "the town's current Municipal Directory "
                              "leaves the moderator name blank, so he "
                              "is recorded as the appointed holder.")],
               [holder("Douglas Spates", "douglas-spates",
                       how_seated="appointed")]),
        office("lister", "Lister", "Derby Listers", 3,
               [derby_report("the ELECTED TOWN OFFICIALS table lists "
                             "Mark Linton (expiring 2028), C. Michael "
                             "Marsh (2027), and Nancy P. Moore (term "
                             "expiring 2026)."),
                derby_dir_page("the current Municipal Directory seats "
                               "the same three listers (printing 'Mike "
                               "Marsh'), so Moore remains in the seat "
                               "that stood in 2026.")],
               [holder("Mark Linton", "mark-linton"),
                holder("C. Michael Marsh", "c-michael-marsh"),
                holder("Nancy P. Moore", "nancy-p-moore")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Derby Collector of Delinquent Taxes", 1,
               [derby_report("the 2026 Warning, Article 1, elects a "
                             "Collector of Delinquent Taxes for a "
                             "1-year term."),
                derby_dir_page("the current Municipal Directory names "
                               "Maryann Tetreault as Collector of "
                               "Delinquent Taxes.")],
               [holder("Maryann Tetreault", "maryann-tetreault")]),
        office("first-constable", "First Constable", "Derby First Constable", 1,
               [derby_report("the ELECTED TOWN OFFICIALS table prints "
                             "'Mathew R. Sheltra' as First Constable "
                             "(term expiring 2026)."),
                derby_dir_page("the current Municipal Directory seats "
                               "Matthew Sheltra as First Constable; the "
                               "directory spelling governs the name "
                               "recorded here.")],
               [holder("Matthew Sheltra", "matthew-sheltra")]),
        office("second-constable", "Second Constable",
               "Derby Second Constable", 1,
               [derby_report("the ELECTED TOWN OFFICIALS table prints "
                             "the Second Constable seat as Vacant."),
                derby_dir_page("the current Municipal Directory seats "
                               "Jerry Bosley Jr as Second Constable, "
                               "the winner of the 2026 ballot seat.")],
               [holder("Jerry Bosley Jr", "jerry-bosley-jr")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Derby Cemetery Commission", 5,
               [derby_report("the ELECTED TOWN OFFICIALS table lists "
                             "five Cemetery Commissioners on 5-year "
                             "terms: Elizabeth Bumps (2027), Scott "
                             "Bianchi (term expiring 2026), James "
                             "Buchanan (2029), and Valerie P. Glover "
                             "(2028), with the fifth seat shown as a "
                             "vacant remainder."),
                derby_dir_page("the current Municipal Directory seats "
                               "Bianchi in the seat that stood in 2026 "
                               "and names Karen Jenne as the fifth "
                               "commissioner.")],
               [holder("Elizabeth Bumps", "elizabeth-bumps"),
                holder("Scott Bianchi", "scott-bianchi"),
                holder("James Buchanan", "james-buchanan"),
                holder("Valerie P. Glover", "valerie-p-glover"),
                holder("Karen Jenne", "karen-jenne")]),
        office("town-agent", "Town Agent", "Derby Town Agent", 2,
               [derby_report("the report's appointed-officers column "
                             "names Grant Spates and Brad Shattuck as "
                             "Town Agent."),
                derby_dir_page("the current Municipal Directory pairs "
                               "the same two names as Town Agent. The "
                               "town fills this appointive office with "
                               "two agents jointly, so the post carries "
                               "two seats.")],
               [holder("Grant Spates", "grant-spates",
                       how_seated="appointed"),
                holder("Bradley Shattuck", "bradley-shattuck",
                       how_seated="appointed")]),
        office("road-commissioner", "Road Commissioner",
               "Derby Road Commissioner", 1,
               [derby_report("the report's appointed-officers column "
                             "names Stephen Gendreau as Road "
                             "Commissioner.")],
               [holder("Stephen Gendreau", "stephen-gendreau",
                       how_seated="appointed")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Derby Justices of the Peace", 12,
               [jp_src("lists twelve Derby justices of the peace: "
                       "Lindsay Brainard, Elizabeth Bumps, Roseanna "
                       "Cyr, Frank Davis, Sharron Greenwood, Allyson "
                       "Howell, Karen Jenne, Alson Loukes, Brian Smith, "
                       "Douglas Spates, Elia Spates, and Lona Stuart."),
                derby_report("the ELECTED TOWN OFFICIALS table lists "
                             "the same twelve justices of the peace.")],
               [holder("Lindsay Brainard", "lindsay-brainard"),
                holder("Elizabeth Bumps", "elizabeth-bumps"),
                holder("Roseanna Cyr", "roseanna-cyr"),
                holder("Frank Davis", "frank-davis"),
                holder("Sharron Greenwood", "sharron-greenwood"),
                holder("Allyson Howell", "allyson-howell"),
                holder("Karen Jenne", "karen-jenne"),
                holder("Alson Loukes", "alson-loukes"),
                holder("Brian Smith", "brian-smith"),
                holder("Douglas Spates", "douglas-spates"),
                holder("Elia Spates", "elia-spates"),
                holder("Lona Stuart", "lona-stuart")]),
    ]
    jp = jp_election(
        "derby-vt", label, 12,
        "lists twelve Derby justices of the peace elected "
        "November 5, 2024: Lindsay Brainard, Elizabeth Bumps, "
        "Roseanna Cyr, Frank Davis, Sharron Greenwood, Allyson "
        "Howell, Karen Jenne, Alson Loukes, Brian Smith, Douglas "
        "Spates, Elia Spates, and Lona Stuart. The listing "
        "publishes no vote totals or party labels and none are "
        "recorded.",
        [derby_report("the ELECTED TOWN OFFICIALS table lists the "
                      "same twelve justices of the peace.")])
    return spec("derby", label, offices, jp)


SPECS.append(derby_spec())

# ---------------------------------------------------------------- Derby Center
DC_REPORT = {
    "url": "https://derbyvt.org/wp-content/uploads/2025/03/Village-of-Derby-Center-Annual-Report.pdf",
    "note": "PLACEHOLDER",
}
DC_PAGE = {
    "url": "https://derbyvt.org/derby-center/",
    "note": "PLACEHOLDER",
}
DC_CHARTER = {
    "url": "https://legislature.vermont.gov/statutes/section/24APPENDIX/215/00202",
    "note": "PLACEHOLDER",
}


def dc_report(note):
    return S(DC_REPORT, "Village of Derby Center Annual Report for "
             f"the year ending February 28, 2025 (derbyvt.org): {note}")


def dc_page(note):
    return S(DC_PAGE, "Village of Derby Center office page "
             f"(derbyvt.org, current): {note}")


def dc_charter(note):
    return S(DC_CHARTER, "Title 24 Appendix V.S.A. chapter 215 "
             f"section 202 (official text, Vermont General Assembly): {note}")


def derby_center_spec():
    label = "Village of Derby Center"
    bumps_sources = [dc_page("lists Elizabeth Bumps as the "
                             "village's Clerk/Treasurer today."),
                     dc_report("the officers page lists Elizabeth "
                               "Bumps as Clerk, Treasurer, and Tax "
                               "Collector. The village publishes no "
                               "roster past February 2025; Bumps is "
                               "also a Derby town justice of the peace "
                               "and cemetery commissioner, and this "
                               "membership attaches to that same person "
                               "record.")]
    offices = [
        office("trustee", "Trustee", "Derby Center Board of Trustees", 3,
               [dc_charter("provides for the election of three "
                           "Trustees at the village annual meeting on "
                           "staggered 3-year terms."),
                dc_report("lists the trustees as Marcel Caron (term "
                          "expiring April 2025), Rosaire Fortin "
                          "(April 2026), and Stephen Mengel (April "
                          "2027). The village publishes no official "
                          "record of its April 2025 or April 2026 "
                          "annual-meeting outcomes, so only Mengel, "
                          "whose term runs past the most recent "
                          "meeting, is recorded; the other two seats "
                          "are left unfilled rather than guessed.")],
               [holder("Stephen Mengel", "stephen-mengel")]),
        office("village-clerk", "Village Clerk", "Derby Center Village Clerk", 1,
               [dc_charter("provides for the election of a Village "
                           "Clerk at the annual meeting.")] + bumps_sources,
               [holder("Elizabeth Bumps", "elizabeth-bumps",
                       person_scope="derby")]),
        office("village-treasurer", "Village Treasurer",
               "Derby Center Village Treasurer", 1,
               [dc_charter("provides for the election of a Village "
                           "Treasurer at the annual meeting.")] + bumps_sources,
               [holder("Elizabeth Bumps", "elizabeth-bumps",
                       person_scope="derby")]),
        office("collector-of-taxes", "Tax Collector",
               "Derby Center Tax Collector", 1,
               [dc_charter("provides for the election of a Collector "
                           "at the annual meeting.")] + bumps_sources,
               [holder("Elizabeth Bumps", "elizabeth-bumps",
                       person_scope="derby")]),
        office("moderator", "Moderator", "Derby Center Moderator", 1,
               [dc_charter("provides for the election of a Moderator "
                           "for a 1-year term at the annual meeting. "
                           "Structure only: the 2025 annual report "
                           "names William Gardyne, whose term expired "
                           "April 2025, and the village publishes no "
                           "record of its 2025 or 2026 annual-meeting "
                           "outcomes; the seat is left unfilled rather "
                           "than guessed.")]),
    ]
    return spec("derby-center", label, offices)


SPECS.append(derby_center_spec())

# ---------------------------------------------------------------- Derby Line
DL_REPORT = {
    "url": "https://derbyvt.org/wp-content/uploads/2026/03/Web-DLVillage-Annual-Rpt_2026.P.pdf",
    "note": "PLACEHOLDER",
}
DL_WARNING = {
    "url": "https://derbyvt.org/wp-content/uploads/2026/02/WARNING-ANNUAL-MEETING-2026.pdf",
    "note": "PLACEHOLDER",
}
DL_CHARTER = {
    "url": "https://legislature.vermont.gov/statutes/section/24APPENDIX/217/00202",
    "note": "PLACEHOLDER",
}
DL_MINUTES = {
    "url": "https://derbyvt.org/derby-line/derby-line-agenda/",
    "note": "PLACEHOLDER",
}


def dl_report(note):
    return S(DL_REPORT, "Village of Derby Line '2025 Officers' "
             "Annual Report for the year ending February 28, 2026 "
             f"(derbyvt.org): {note}")


def dl_warning(note):
    return S(DL_WARNING, "Village of Derby Line Warning for the "
             "annual meeting of April 7, 2026, attested February 24, "
             f"2026 by Peggy Kelley, Clerk (derbyvt.org): {note}")


def dl_charter(note):
    return S(DL_CHARTER, "Title 24 Appendix V.S.A. chapter 217 "
             f"section 202 (official text, Vermont General Assembly): {note}")


def dl_minutes(note):
    return S(DL_MINUTES, "Village of Derby Line trustee minutes, "
             f"posted on the village's agenda page (derbyvt.org): {note}")


def derby_line_spec():
    label = "Village of Derby Line"
    kelley_sources = [dl_report("lists Peggy Kelley as Clerk & "
                                 "Treasurer and as Delinquent Water, "
                                 "Sewer & Tax Collector, each on a "
                                 "3-year term expiring 2028."),
                      dl_warning("is attested by Peggy Kelley as "
                                 "village Clerk in February 2026.")]
    offices = [
        office("trustee", "Trustee", "Derby Line Board of Trustees", 3,
               [dl_charter("provides for the election of three "
                           "Trustees on staggered 3-year terms."),
                dl_report("lists Sarah Webster (Chair, term expiring "
                          "2027), Dustin Horne (Vice-Chairman, term "
                          "expiring 2026), and Brian Lemery (term "
                          "expiring 2028)."),
                dl_minutes("the April 21, 2026 reorganization minutes "
                           "seat Horne as Chair and Lemery as Vice "
                           "Chair (Horne's seat stood at the April 7, "
                           "2026 annual meeting); the May 28, 2026 "
                           "minutes accept Trustee Sarah Webster's "
                           "resignation; the June 2, 2026 minutes "
                           "appoint Tristan Ovitt as the third "
                           "trustee until the April 2027 annual "
                           "meeting; the August 4, 2026 minutes show "
                           "Horne, Lemery, and Ovitt sitting. Webster "
                           "is not recorded as a current holder.")],
               [holder("Dustin Horne", "dustin-horne"),
                holder("Brian Lemery", "brian-lemery"),
                holder("Tristan Ovitt", "tristan-ovitt",
                       how_seated="appointed")]),
        office("village-clerk", "Village Clerk", "Derby Line Village Clerk", 1,
               [dl_charter("provides for the election of a Village "
                           "Clerk.")] + kelley_sources,
               [holder("Peggy Kelley", "peggy-kelley")]),
        office("village-treasurer", "Village Treasurer",
               "Derby Line Village Treasurer", 1,
               [dl_charter("provides for the election of a Village "
                           "Treasurer.")] + kelley_sources,
               [holder("Peggy Kelley", "peggy-kelley")]),
        office("collector-of-taxes", "Tax Collector",
               "Derby Line Tax Collector", 1,
               [dl_charter("provides for the election of a Tax "
                           "Collector."),
                dl_report("styles the office held by Peggy Kelley "
                          "'Delinquent Water, Sewer & Tax Collector' "
                          "on a 3-year term expiring 2028; it is "
                          "recorded here under the charter's Tax "
                          "Collector title.")],
               [holder("Peggy Kelley", "peggy-kelley")]),
        office("moderator", "Moderator", "Derby Line Moderator", 1,
               [dl_charter("provides for the election of a Moderator "
                           "for a 1-year term. Structure only: Frank "
                           "Davis held the office to April 2026 per "
                           "the village's 2025 Officers report, and "
                           "no official source publishes the winner "
                           "of the April 7, 2026 election; the seat "
                           "is left unfilled rather than guessed.")]),
        office("auditor", "Auditor", "Derby Line Auditors", 3,
               [dl_report("lists three village Auditors on staggered "
                          "3-year terms: Charles Gross (expiring "
                          "2026), Roberta Pheiffer (2027), and "
                          "Madeleine Roy (2028)."),
                dl_warning("warns the election of one Auditor for a "
                           "3-year term at the April 7, 2026 annual "
                           "meeting; no official source publishes the "
                           "winner, so Gross's seat is left unfilled.")],
               [holder("Roberta Pheiffer", "roberta-pheiffer"),
                holder("Madeleine Roy", "madeleine-roy")]),
        office("water-commissioner", "Water Commissioner",
               "Derby Line Water Commissioner", 1,
               [dl_report("lists Karen Jenne as Water Commissioner "
                          "on a 1-year term expiring 2026."),
                dl_warning("warns the election of one Water Company "
                           "Commissioner for a 1-year term at the "
                           "April 7, 2026 annual meeting. Structure "
                           "only: no official source publishes the "
                           "winner; the seat is left unfilled rather "
                           "than guessed.")]),
    ]
    return spec("derby-line", label, offices)


SPECS.append(derby_line_spec())

# ---------------------------------------------------------------- Dorset
DORSET_REPORT = {
    "url": "https://dorsetvt.org/uploads/3/5/3/5/35356792/2025_town_report_final.pdf",
    "note": "PLACEHOLDER",
}


def dorset_report(note):
    return S(DORSET_REPORT, "Town of Dorset 2025 Town Report "
             f"(dorsetvt.org): {note}")


def dorset_spec():
    label = "Town of Dorset"
    offices = [
        office("selectboard", "Selectboard Member", "Dorset Selectboard", 5,
               [sb_dir("lists five Dorset Selectboard members: Megan "
                       "Thorn (Chair), Henry Chandler (Vice Chair), "
                       "Alison Clarke, Frank Parent, and Jim Salsgiver."),
                dorset_report("the elected-officers table (p. 6) lists "
                              "the same five, and the town's official "
                              "newsletter reported the March 3, 2026 "
                              "results re-electing Chandler (203 "
                              "votes), Salsgiver (153), and Parent "
                              "(268) to the three seats that stood.")],
               [holder("Megan Thörn", "megan-thorn"),
                holder("Henry Chandler", "henry-chandler"),
                holder("Alison Clarke", "alison-clarke"),
                holder("Frank Parent", "frank-parent"),
                holder("Jim Salsgiver", "jim-salsgiver")]),
        office("town-clerk", "Town Clerk", "Dorset Town Clerk", 1,
               [dorset_report("the APPOINTED officers table (p. 5) "
                              "lists Jennifer Comar as Town Clerk; "
                              "the town's official newsletter reports "
                              "she was appointed Town Clerk effective "
                              "January 1, 2026 after serving two years "
                              "as Assistant Clerk. The office is "
                              "appointive in Dorset.")],
               [holder("Jennifer Comar", "jennifer-comar",
                       how_seated="appointed")]),
        office("town-treasurer", "Town Treasurer", "Dorset Town Treasurer", 1,
               [dorset_report("the APPOINTED officers table (p. 5) "
                              "lists Jennifer Comar as Town "
                              "Treasurer, an appointive office in "
                              "Dorset.")],
               [holder("Jennifer Comar", "jennifer-comar",
                       how_seated="appointed")]),
        office("moderator", "Moderator", "Dorset Moderator", 1,
               [dorset_report("the elected-officers table lists Kevin "
                              "O'Toole as Moderator, and the 2026 "
                              "Warning placed the office on the "
                              "ballot. The town's official newsletter "
                              "reported the Journal's town-meeting "
                              "tally recording O'Toole re-elected "
                              "March 3, 2026 with 313 votes, "
                              "unopposed; no official tally sheet is "
                              "posted, and the result rests on that "
                              "reporting.")],
               [holder("Kevin O'Toole", "kevin-otoole")]),
        office("first-constable", "First Constable", "Dorset First Constable", 1,
               [dorset_report("the elected-officers table lists Ryan "
                              "Matteson as First Constable with a term "
                              "expiring March 2026, and the 2026 "
                              "Warning placed the office on the "
                              "ballot. Structure only: no official "
                              "source publishes the 2026 outcome; the "
                              "seat is left unfilled rather than "
                              "guessed.")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Dorset Collector of Delinquent Taxes", 1,
               [dorset_report("the signed Delinquent Tax Report "
                              "(p. 59) is executed by Robert Gaiotti "
                              "as 'Town Manager/Delinquent Tax "
                              "Collector': the Town Manager serves as "
                              "the town's collector of delinquent "
                              "taxes, an appointed holder.")],
               [holder("Robert Gaiotti", "robert-gaiotti",
                       how_seated="appointed")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Dorset Justices of the Peace", 10,
               [jp_src("lists ten Dorset justices of the peace: "
                       "Russell Appelman, Howard W Coolidge, Tom "
                       "Cooper, Lee Fox, Jennifer Halligan Comar, "
                       "Michelle Pagan, Sandra \"Sandy\" Pinsonault, "
                       "John \"Will\" Rucker, Roger Squire, and Bo "
                       "Thorn."),
                dorset_report("the elected-officers table lists the "
                              "same ten justices of the peace (the "
                              "report spells the tenth 'Roger "
                              "Squires'; the Secretary of State "
                              "listing's 'Roger Squire' governs).")],
               [holder("Russell Appelman", "russell-appelman"),
                holder("Howard W. Coolidge", "howard-w-coolidge"),
                holder("Tom Cooper", "tom-cooper"),
                holder("Lee Fox", "lee-fox"),
                holder("Jennifer Comar", "jennifer-comar",
                       ballot_name="Jennifer Halligan Comar"),
                holder("Michelle Pagan", "michelle-pagan"),
                holder("Sandra Pinsonault", "sandra-pinsonault",
                       ballot_name="Sandra \"Sandy\" Pinsonault"),
                holder("John Rucker", "john-rucker",
                       ballot_name="John \"Will\" Rucker"),
                holder("Roger Squire", "roger-squire"),
                holder("Bo Thorn", "bo-thorn")]),
    ]
    jp = jp_election(
        "dorset-vt", label, 10,
        "lists ten Dorset justices of the peace elected "
        "November 5, 2024: Russell Appelman, Howard W Coolidge, "
        "Tom Cooper, Lee Fox, Jennifer Halligan Comar, Michelle "
        "Pagan, Sandra \"Sandy\" Pinsonault, John \"Will\" Rucker, "
        "Roger Squire, and Bo Thorn. The listing publishes no "
        "vote totals or party labels and none are recorded.",
        [dorset_report("the elected-officers table lists the same "
                       "ten justices of the peace.")])
    return spec("dorset", label, offices, jp)


SPECS.append(dorset_spec())

# ---------------------------------------------------------------- Dover
DOVER_REPORT = {
    "url": "https://www.doververmont.com/media/11501",
    "note": "PLACEHOLDER",
}
DOVER_RESULTS = {
    "url": "https://www.doververmont.com/media/11696",
    "note": "PLACEHOLDER",
}
DOVER_APPTS = {
    "url": "https://www.doververmont.com/bc-toa",
    "note": "PLACEHOLDER",
}
DOVER_WARNING = {
    "url": "https://www.doververmont.com/media/11491",
    "note": "PLACEHOLDER",
}


def dover_report(note):
    return S(DOVER_REPORT, "Town of Dover 2026 Town Report (Annual "
             f"Report 2024-2025) (doververmont.com): {note}")


def dover_results(note):
    return S(DOVER_RESULTS, "Town of Dover official election "
             "results, Town Meeting March 3, 2026 (doververmont.com): "
             f"{note}")


def dover_appts(note):
    return S(DOVER_APPTS, "Town of Dover Town Officer Appointments "
             f"page (doververmont.com, current): {note}")


def dover_warning(note):
    return S(DOVER_WARNING, "Town of Dover Warning for the 2026 "
             f"Annual Town Meeting (doververmont.com): {note}")


def dover_spec():
    label = "Town of Dover"
    offices = [
        office("selectboard", "Selectboard Member", "Dover Selectboard", 5,
               [sb_dir("lists five Dover Selectboard members: "
                       "Victoria Capitani (Chair), Sarah Shippee "
                       "(Vice Chair), Daniel Baliotti, Patrick "
                       "Lagrange, and Joseph Mahon."),
                dover_report("the ELECTED TOWN OFFICERS table lists "
                             "the same five."),
                dover_results("records Patrick Lagrange re-elected "
                              "to a 3-year term (81 votes) and Daniel "
                              "S. Baliotti re-elected to a 2-year "
                              "term (79 votes) on March 3, 2026."),
                dover_appts("the current roster seats Capitani "
                            "(Chair, expiring 2027), Shippee (Vice "
                            "Chair, 2027), Baliotti (2028), Mahon "
                            "(2028), and Lagrange (2029).")],
               [holder("Victoria Capitani", "victoria-capitani"),
                holder("Sarah Shippee", "sarah-shippee"),
                holder("Daniel Baliotti", "daniel-baliotti"),
                holder("Joseph Mahon", "joseph-mahon"),
                holder("Patrick Lagrange", "patrick-lagrange")]),
        office("town-clerk", "Town Clerk", "Dover Town Clerk", 1,
               [dover_report("the ELECTED TOWN OFFICERS table lists "
                             "Andy McLean as Town Clerk, elected to a "
                             "3-year term expiring 2028."),
                guide("lists Andy McLean as Town Clerk of Dover.")],
               [holder("Andy McLean", "andy-mclean")]),
        office("town-treasurer", "Town Treasurer", "Dover Town Treasurer", 1,
               [dover_report("the ELECTED TOWN OFFICERS table lists "
                             "Marco Tallini as Town Treasurer, "
                             "elected to a 3-year term expiring 2028."),
                guide("lists Marco Tallini as Town Treasurer of "
                      "Dover.")],
               [holder("Marco Tallini", "marco-tallini")]),
        office("moderator", "Moderator", "Dover Moderator", 1,
               [dover_results("records Richard J Werner re-elected "
                              "Moderator for 1 year on March 3, 2026 "
                              "(83 votes)."),
                dover_appts("the current roster names Richard Werner "
                            "as Town Moderator.")],
               [holder("Richard Werner", "richard-werner")]),
        office("auditor", "Auditor", "Dover Auditors", 3,
               [dover_report("the ELECTED TOWN OFFICERS table lists "
                             "Tamara Allen (term expiring 2026), "
                             "Michelle Pinkham (2027), and Robert A. "
                             "McIntyre (2028)."),
                dover_results("records Tamara Allen re-elected "
                              "Auditor for a 3-year term on March 3, "
                              "2026 (90 votes)."),
                dover_appts("the current roster names the same three "
                            "auditors (printing 'Robert McIntyre "
                            "Jr.').")],
               [holder("Tamara Allen", "tamara-allen"),
                holder("Michelle Pinkham", "michelle-pinkham"),
                holder("Robert McIntyre", "robert-mcintyre")]),
        office("first-constable", "First Constable", "Dover First Constable", 1,
               [dover_results("records Andy McLean re-elected First "
                              "Constable for 1 year on March 3, 2026 "
                              "(89 votes)."),
                dover_report("the ELECTED TOWN OFFICERS table lists "
                             "Andy McLean as 1st Constable.")],
               [holder("Andy McLean", "andy-mclean")]),
        office("trustees-of-public-funds", "Trustee of Public Funds",
               "Dover Trustees of Public Funds", 1,
               [dover_results("records Marco Tallini re-elected "
                              "Trustee of Public Funds for a 1-year "
                              "term on March 3, 2026 (88 votes)."),
                dover_report("the ELECTED TOWN OFFICERS table lists "
                             "Marco Tallini as Trustee of Public "
                             "Funds. Dover fills the office with a "
                             "single trustee on 1-year terms, so the "
                             "post carries one seat.")],
               [holder("Marco Tallini", "marco-tallini")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Dover Collector of Delinquent Taxes", 1,
               [dover_appts("the current roster lists the Delinquent "
                            "Tax Collector among the town's APPOINTED "
                            "officers: Marco Tallini.")],
               [holder("Marco Tallini", "marco-tallini",
                       how_seated="appointed")]),
        office("grand-juror", "Grand Juror", "Dover Grand Juror", 1,
               [dover_report("the APPOINTED TOWN OFFICERS table lists "
                             "Andy McLean as Grand Juror."),
                dover_appts("the current roster likewise lists the "
                            "Grand Juror among the appointed "
                            "officers: Andy McLean.")],
               [holder("Andy McLean", "andy-mclean",
                       how_seated="appointed")]),
        office("town-agent", "Town Agent", "Dover Town Agent", 1,
               [dover_report("the APPOINTED TOWN OFFICERS table lists "
                             "Linda Holland as Town Agent."),
                dover_appts("the current roster likewise lists the "
                            "Town Agent among the appointed officers: "
                            "Linda Holland.")],
               [holder("Linda Holland", "linda-holland",
                       how_seated="appointed")]),
        office("library-trustee", "Library Trustee", "Dover Library Trustees", 5,
               [dover_report("the ELECTED TOWN OFFICERS table lists "
                             "five Library Trustees on 5-year terms: "
                             "Diane Guminak (expiring 2026), Laura "
                             "Maturo (2027), Kathleen Saccoccio "
                             "(2028), Richard Payan (2029), and Roger "
                             "Cardinal (2030)."),
                dover_results("records Debra Malloy elected to a "
                              "5-year Library Trustee term (86 votes) "
                              "and Shital Kinkhabwala elected to the "
                              "5-year term with two years remaining "
                              "(86 votes) on March 3, 2026."),
                dover_appts("the current roster seats Malloy, "
                            "Kinkhabwala (expiring 2028), Maturo, "
                            "Payan, and Cardinal; Guminak and "
                            "Saccoccio rotated off at the 2026 "
                            "meeting and are not recorded.")],
               [holder("Debra Malloy", "debra-malloy"),
                holder("Shital Kinkhabwala", "shital-kinkhabwala"),
                holder("Laura Maturo", "laura-maturo"),
                holder("Richard Payan", "richard-payan"),
                holder("Roger Cardinal", "roger-cardinal")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Dover Justices of the Peace", 5,
               [jp_src("lists five Dover justices of the peace: "
                       "Timothy Dolan, Linda Holland, Catherine "
                       "Kaufmann, Chelsea Samani, and Shannon "
                       "Wheeler."),
                dover_report("the ELECTED TOWN OFFICERS table lists "
                             "the same five justices of the peace "
                             "(printing Linda L. Holland and Catherine "
                             "D. Kaufmann).")],
               [holder("Timothy Dolan", "timothy-dolan"),
                holder("Linda Holland", "linda-holland",
                       ballot_name="Linda L. Holland"),
                holder("Catherine Kaufmann", "catherine-kaufmann"),
                holder("Chelsea Samani", "chelsea-samani"),
                holder("Shannon Wheeler", "shannon-wheeler")]),
    ]
    jp = jp_election(
        "dover-vt", label, 5,
        "lists five Dover justices of the peace elected "
        "November 5, 2024: Timothy Dolan, Linda Holland, Catherine "
        "Kaufmann, Chelsea Samani, and Shannon Wheeler. The "
        "listing publishes no vote totals or party labels and "
        "none are recorded.",
        [dover_report("the ELECTED TOWN OFFICERS table lists the "
                      "same five justices of the peace.")])
    return spec("dover", label, offices, jp)


SPECS.append(dover_spec())

# ---------------------------------------------------------------- Dummerston
DUMM_REPORT = {
    "url": "https://dummerston.org/gov/2025%20Town%20Report.pdf",
    "note": "PLACEHOLDER",
}
DUMM_SB_MINUTES = {
    "url": "https://dummerston.org/townclerk/sb-minutes/SM2026.03.04.PDF",
    "note": "PLACEHOLDER",
}
DUMM_SITE = {
    "url": "https://dummerston.org/",
    "note": "PLACEHOLDER",
}


def dumm_report(note):
    return S(DUMM_REPORT, "Town of Dummerston 'Town Meeting 2026: "
             f"Annual Report for 2025' (dummerston.org): {note}")


def dumm_minutes(note):
    return S(DUMM_SB_MINUTES, "Town of Dummerston Selectboard "
             f"minutes, March 4, 2026 (dummerston.org): {note}")


def dumm_site(note):
    return S(DUMM_SITE, "Town of Dummerston official website "
             f"(dummerston.org, current): {note}")


def dummerston_spec():
    label = "Town of Dummerston"
    offices = [
        office("selectboard", "Selectboard Member", "Dummerston Selectboard", 5,
               [sb_dir("lists five Dummerston Selectboard members: "
                       "Todd Davidson (Chair), Paul Adler (Vice "
                       "Chair), Maria Glabach, Theresa Chapman, and "
                       "Alexander Lockie."),
                dumm_minutes("the post-election reorganization "
                             "minutes of March 4, 2026 seat Todd "
                             "Davidson (Chair), Paul Adler (Vice "
                             "Chair), Maria Glabach (Clerk), Terry "
                             "Chapman, and Alex Lockie, welcoming "
                             "Chapman and Lockie as new members. The "
                             "town's pages print 'Terry Chapman' and "
                             "'Alex Lockie'; the directory prints "
                             "Theresa Chapman and Alexander Lockie.")],
               [holder("Todd Davidson", "todd-davidson"),
                holder("Paul Adler", "paul-adler"),
                holder("Maria Glabach", "maria-glabach"),
                holder("Terry Chapman", "terry-chapman"),
                holder("Alexander Lockie", "alexander-lockie")]),
        office("town-clerk", "Town Clerk", "Dummerston Town Clerk", 1,
               [dumm_report("the ELECTED OFFICERS table lists Laurie "
                            "Frechette as Town Clerk (1-year term)."),
                dumm_minutes("Laurie Frechette called the March 4, "
                             "2026 Selectboard meeting to order as "
                             "Town Clerk."),
                guide("lists Laurie Frechette as Town Clerk of "
                      "Dummerston.")],
               [holder("Laurie Frechette", "laurie-frechette")]),
        office("town-treasurer", "Town Treasurer", "Dummerston Town Treasurer", 1,
               [dumm_report("the ELECTED OFFICERS table lists "
                            "Christopher Brown as Town Treasurer "
                            "(1-year term)."),
                dumm_site("the current Municipal Staff listing names "
                         "Christopher Brown as Treasurer."),
                guide("lists Christopher Brown as Town Treasurer of "
                      "Dummerston.")],
               [holder("Christopher Brown", "christopher-brown")]),
        office("moderator", "Moderator", "Dummerston Moderator", 1,
               [dumm_report("the ELECTED OFFICERS table lists Cindy "
                            "Jerome as Moderator (1-year term), and "
                            "Article 2 of the 2026 Warning asked "
                            "voters to affirm her election as "
                            "Moderator despite her no longer being a "
                            "resident. Structure only: no official "
                            "source publishes the outcome of that "
                            "article or names a current moderator; "
                            "the seat is left unfilled rather than "
                            "guessed.")]),
        office("lister", "Lister", "Dummerston Listers", 3,
               [dumm_report("the ELECTED OFFICERS table lists "
                            "Charlotte Neer Annis (term expiring "
                            "2026), Michael Silberman (2027), and "
                            "Stephan Mindel (2028) as Listers."),
                dumm_site("the current Municipal Staff listing names "
                         "Mathew Leger as Lister alongside "
                         "Silberman and Mindel. No published tally "
                         "records the 2026 lister outcome; Leger is "
                         "recorded as the current holder of the "
                         "third seat on the town's listing, and "
                         "Annis is not recorded.")],
               [holder("Michael Silberman", "michael-silberman"),
                holder("Stephan Mindel", "stephan-mindel"),
                holder("Mathew Leger", "mathew-leger")]),
        office("auditor", "Auditor", "Dummerston Auditors", 3,
               [dumm_report("the ELECTED OFFICERS table lists Ray "
                            "Harris (term expiring 2026), Joe Little "
                            "(2027), and Ruth Hoffman (2028) as "
                            "Auditors."),
                dumm_site("the Town Clerk page names Ruth Hoffman, "
                         "Joe Little, and Ray Harris as the current "
                         "auditors.")],
               [holder("Ray Harris", "ray-harris"),
                holder("Joe Little", "joe-little"),
                holder("Ruth Hoffman", "ruth-hoffman")]),
        office("first-constable", "First Constable", "Dummerston First Constable", 1,
               [dumm_report("the APPOINTED OFFICERS table lists Lewis "
                            "White as First Constable: the office is "
                            "appointive in Dummerston and appears on "
                            "no election warning.")],
               [holder("Lewis White", "lewis-white",
                       how_seated="appointed")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Dummerston Collector of Delinquent Taxes", 1,
               [dumm_report("the APPOINTED OFFICERS table lists the "
                            "Delinquent Tax Collector as Laurie "
                            "Frechette (interim). Article 4 of the "
                            "2026 Warning asked voters to authorize "
                            "the Selectboard to appoint a receiver "
                            "of delinquent taxes; its outcome is not "
                            "published. Frechette is recorded as the "
                            "appointed holder per the town report.")],
               [holder("Laurie Frechette", "laurie-frechette",
                       how_seated="appointed")]),
        office("library-trustee", "Library Trustee",
               "Dummerston Library Trustees", 5,
               [dumm_report("the ELECTED OFFICERS table lists five "
                            "town-elected Library Trustees (Lydia "
                            "Taft Pratt Library) on 5-year terms: "
                            "Marvin Luna (expiring 2026), David "
                            "Schottland (2027), Lyle Holiday (2028), "
                            "Linda DeCarlo Burns (2029), and Stacy "
                            "Byrck (2030), and the 2026 Warning "
                            "placed a 5-year Library Trustee seat on "
                            "the ballot."),
                dumm_site("the library's current Board of Trustees "
                         "page lists Lyle Holiday, Dave Schottland, "
                         "Stacy Bryck, Linda DeCarlo Burns, and "
                         "Kate Jansak. Luna's term expired in 2026 "
                         "and he is not recorded; Jansak is "
                         "recorded as the current holder of the "
                         "seat that stood in 2026.")],
               [holder("David Schottland", "david-schottland"),
                holder("Lyle Holiday", "lyle-holiday"),
                holder("Linda DeCarlo Burns", "linda-decarlo-burns"),
                holder("Stacy Bryck", "stacy-bryck"),
                holder("Kate Jansak", "kate-jansak")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Dummerston Justices of the Peace", 7,
               [jp_src("lists seven Dummerston justices of the "
                       "peace: Paul Normandeau, Ruth Hoffman, Lew "
                       "Sorenson, Linda Hellus, Betsy Bates, Elizabeth "
                       "(Libby) Lafland, and Ezekiel Goodband."),
                dumm_report("the ELECTED OFFICERS table lists the "
                            "same seven justices of the peace, "
                            "elected November 2024.")],
               [holder("Paul Normandeau", "paul-normandeau"),
                holder("Ruth Hoffman", "ruth-hoffman"),
                holder("Lew Sorenson", "lew-sorenson"),
                holder("Linda Hellus", "linda-hellus"),
                holder("Betsy Bates", "betsy-bates"),
                holder("Elizabeth Lafland", "elizabeth-lafland",
                       ballot_name="Elizabeth (Libby) Lafland"),
                holder("Ezekiel Goodband", "ezekiel-goodband")]),
    ]
    jp = jp_election(
        "dummerston-vt", label, 7,
        "lists seven Dummerston justices of the peace elected "
        "November 5, 2024: Paul Normandeau, Ruth Hoffman, Lew "
        "Sorenson, Linda Hellus, Betsy Bates, Elizabeth (Libby) "
        "Lafland, and Ezekiel Goodband. The listing publishes no "
        "vote totals or party labels and none are recorded.",
        [dumm_report("the ELECTED OFFICERS table lists the same "
                     "seven justices of the peace.")])
    return spec("dummerston", label, offices, jp)


SPECS.append(dummerston_spec())

# ---------------------------------------------------------------- Duxbury
DUX_SB_PAGE = {
    "url": "https://www.duxburyvermont.org/town-government/selectboard",
    "note": "PLACEHOLDER",
}
DUX_CLERK_PAGE = {
    "url": "https://www.duxburyvermont.org/town-government/clerkandtreasurer",
    "note": "PLACEHOLDER",
}


def dux_sb(note):
    return S(DUX_SB_PAGE, "Town of Duxbury Selectboard page "
             f"(duxburyvermont.org, current): {note}")


def dux_report(note):
    return S(DUX_CLERK_PAGE, "Town of Duxbury 'Annual Election "
             "Report 2025' and 'Duxbury 2026 Town Meeting Tally' "
             "(March 3, 2026), reached through the Town Clerk and "
             f"Treasurer page (duxburyvermont.org): {note}")


def duxbury_spec():
    label = "Town of Duxbury"
    offices = [
        office("selectboard", "Selectboard Member", "Duxbury Selectboard", 5,
               [sb_dir("lists four Duxbury Selectboard members: "
                       "Patrick Zachary (Chair), Mari Pratt (Vice "
                       "Chair), Gwenna Peters, and Matt Schroeder."),
                dux_report("the report's Elected Offices table lists "
                           "FIVE members, adding Jamison Ervin (3-year "
                           "term expiring 2026); the official 2026 "
                           "tally records Mari Pratt (258 votes) and "
                           "Matt Schroeder (286) elected to 1-year "
                           "terms and Gwenna Peters (285) elected to "
                           "the remaining two years of her term, and "
                           "NO winner for the 3-year seat (write-ins "
                           "did not reach the required 12 votes). "
                           "Schroeder and Peters had been serving as "
                           "appointees and are recorded as elected "
                           "on the 2026 tally."),
                dux_sb("the current roster seats Zachary (Chair, "
                       "term expiring 2027), Pratt (Vice Chair), "
                       "Schroeder, and Peters, and posts the fifth "
                       "seat as Vacant. Ervin is not recorded.")],
               [holder("Patrick Zachary", "patrick-zachary"),
                holder("Mari Pratt", "mari-pratt"),
                holder("Matt Schroeder", "matt-schroeder"),
                holder("Gwenna Peters", "gwenna-peters")]),
        office("moderator", "Moderator", "Duxbury Moderator", 1,
               [dux_report("the official 2026 tally records Daniel "
                           "Senning re-elected Moderator (306 votes); "
                           "the report's table prints 'Dan "
                           "Senning'.")],
               [holder("Daniel Senning", "daniel-senning")]),
        office("town-clerk", "Town Clerk", "Duxbury Town Clerk", 1,
               [dux_report("the report's Elected Offices table lists "
                           "Maureen Harvey as Town Clerk, elected to "
                           "a 3-year term expiring 2028."),
                guide("lists Maureen Harvey as Town Clerk of "
                      "Duxbury.")],
               [holder("Maureen Harvey", "maureen-harvey")]),
        office("town-treasurer", "Town Treasurer", "Duxbury Town Treasurer", 1,
               [dux_report("the report's Elected Offices table lists "
                           "Maureen Harvey as Town Treasurer, elected "
                           "to a 3-year term expiring 2028."),
                guide("lists Maureen Harvey as Town Treasurer of "
                      "Duxbury.")],
               [holder("Maureen Harvey", "maureen-harvey")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Duxbury Collector of Delinquent Taxes", 1,
               [dux_report("the report's Elected Offices table lists "
                           "the Delinquent Tax Collector as an "
                           "ELECTED office held by Maureen Harvey "
                           "(3-year term expiring 2027).")],
               [holder("Maureen Harvey", "maureen-harvey")]),
        office("lister", "Lister", "Duxbury Listers", 3,
               [dux_report("the report's Elected Offices table lists "
                           "Alan Quackenbush (term expiring 2026), "
                           "Max Popowicz (2027), and Mo LaVarnway "
                           "(2028) as Listers; the official 2026 "
                           "tally records Quackenbush re-elected "
                           "(290 votes).")],
               [holder("Alan Quackenbush", "alan-quackenbush"),
                holder("Max Popowicz", "max-popowicz"),
                holder("Maurice Lavanway", "maurice-lavanway")]),
        office("budget-committee", "Budget Committee Member",
               "Duxbury Budget Committee", 5,
               [dux_report("the report's Elected Offices table lists "
                           "the town-elected Budget Committee on "
                           "5-year terms: Ben MacKinney (resigned), "
                           "Ann Harvey (expiring 2027), Mari Pratt "
                           "(2028), Jill Smith (2029), and Brenda "
                           "Clarkson (appointed in 2025, expiring "
                           "2030); the official 2026 tally records "
                           "no winner for either Budget Committee "
                           "seat that stood in 2026. MacKinney, "
                           "having resigned, is not recorded.")],
               [holder("Ann Harvey", "ann-harvey"),
                holder("Mari Pratt", "mari-pratt"),
                holder("Jill Smith", "jill-smith"),
                holder("Brenda Clarkson", "brenda-clarkson",
                       how_seated="appointed")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Duxbury Cemetery Commission", 3,
               [dux_report("the report's Elected Offices table lists "
                           "Jessica Engels (term expiring 2026), "
                           "Dwight Day (2027), and Naomi Alfini "
                           "(2028) as Cemetery Commissioners; the "
                           "official 2026 tally records Engels "
                           "re-elected (293 votes).")],
               [holder("Jessica Engels", "jessica-engels"),
                holder("Dwight Day", "dwight-day"),
                holder("Naomi Alfini", "naomi-alfini")]),
        office("first-constable", "First Constable", "Duxbury First Constable", 1,
               [dux_report("the official 2026 tally records Eric "
                           "Potter re-elected 1st Constable (300 "
                           "votes, 2-year term).")],
               [holder("Eric Potter", "eric-potter")]),
        office("second-constable", "Second Constable",
               "Duxbury Second Constable", 1,
               [dux_report("the official 2026 tally records James L. "
                           "Welch re-elected 2nd Constable (302 "
                           "votes, 2-year term); the report's table "
                           "prints 'James Welch'.")],
               [holder("James L. Welch", "james-l-welch")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Duxbury Justices of the Peace", 7,
               [jp_src("lists seven Duxbury justices of the peace: "
                       "Greg Trulson, Maurice Lavanway, Shawn Perry, "
                       "Dan Cardozo, Jill Smith, Lori Morse, and "
                       "Cindy Senning."),
                dux_report("the report's table lists the same seven "
                           "justices of the peace, elected November "
                           "5, 2024 (printing the lister as 'Mo "
                           "LaVarnway').")],
               [holder("Greg Trulson", "greg-trulson"),
                holder("Maurice Lavanway", "maurice-lavanway"),
                holder("Shawn Perry", "shawn-perry"),
                holder("Dan Cardozo", "dan-cardozo"),
                holder("Jill Smith", "jill-smith"),
                holder("Lori Morse", "lori-morse"),
                holder("Cindy Senning", "cindy-senning")]),
    ]
    jp = jp_election(
        "duxbury-vt", label, 7,
        "lists seven Duxbury justices of the peace elected "
        "November 5, 2024: Greg Trulson, Maurice Lavanway, Shawn "
        "Perry, Dan Cardozo, Jill Smith, Lori Morse, and Cindy "
        "Senning. The listing publishes no vote totals or party "
        "labels and none are recorded.",
        [dux_report("the report's table lists the same seven "
                    "justices of the peace.")])
    return spec("duxbury", label, offices, jp)


SPECS.append(duxbury_spec())

# ---------------------------------------------------------------- East Haven
EH_SITE = {
    "url": "https://sites.google.com/view/east-haven-vt",
    "note": "PLACEHOLDER",
}


def eh_site(note):
    return S(EH_SITE, "Town of East Haven official website "
             f"(sites.google.com/view/east-haven-vt): {note}")


def east_haven_spec():
    label = "Town of East Haven"
    offices = [
        office("selectboard", "Selectboard Member", "East Haven Selectboard", 3,
               [statute2646_structure("a selectboard of three "
                                      "members"),
                S(SB_DIR, "Vermont Secretary of State, Elections "
                          "Division, 'Vermont Selectboard Members' "
                          "directory (updated June 5, 2026): "
                          "publishes NO East Haven roster ('Contact "
                          "the Town Clerk'). The town's official "
                          "website names no current selectboard "
                          "members, so the seats are left unfilled "
                          "rather than guessed.")]),
        office("town-clerk", "Town Clerk", "East Haven Town Clerk", 1,
               [guide("lists Kerri Fillion as Town Clerk of East "
                      "Haven. The town's website advertises the "
                      "clerk's position as opening for hire in the "
                      "first quarter of 2027; Fillion is the "
                      "holder of record in the Secretary of "
                      "State's January 2026 Guide.")],
               [holder("Kerri Fillion", "kerri-fillion")]),
        office("town-treasurer", "Town Treasurer", "East Haven Town Treasurer", 1,
               [guide("lists Kerri Fillion as Town Treasurer of "
                      "East Haven; the same first-quarter-2027 hire "
                      "notice applies.")],
               [holder("Kerri Fillion", "kerri-fillion")]),
        office("moderator", "Moderator", "East Haven Moderator", 1,
               [statute2646_structure("a moderator")]),
        office("lister", "Lister", "East Haven Listers", 3,
               [statute2646_structure("three listers"),
                eh_site("a town announcement (September 8, 2026) "
                        "also advertises an open lister position; "
                        "the vacancy is noted and no holder is "
                        "recorded for any lister seat.")]),
        office("auditor", "Auditor", "East Haven Auditors", 3,
               [statute2646_structure("three auditors")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "East Haven Collector of Delinquent Taxes", 1,
               [statute2646_structure("a collector of delinquent "
                                      "taxes"),
                eh_site("a town announcement (September 8, 2026) "
                        "states the Delinquent Tax Collector "
                        "position is VACANT with an 'urgent need' "
                        "to fill it; the seat is recorded vacant, "
                        "not filled.")]),
        office("grand-juror", "Grand Juror", "East Haven Grand Juror", 1,
               [statute2646_structure("a grand juror")]),
        office("town-agent", "Town Agent", "East Haven Town Agent", 1,
               [statute2646_structure("a town agent")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "East Haven Justices of the Peace", 5,
               [jp_src("lists five East Haven justices of the peace: "
                       "Franklin Higgins, Rita Laferriere, R.J. "
                       "Burke, Delbert Reed, and Stephanie Wales.")],
               [holder("Franklin Higgins", "franklin-higgins"),
                holder("Rita Laferriere", "rita-laferriere"),
                holder("R.J. Burke", "r-j-burke"),
                holder("Delbert Reed", "delbert-reed"),
                holder("Stephanie Wales", "stephanie-wales")]),
    ]
    jp = jp_election(
        "east-haven-vt", label, 5,
        "lists five East Haven justices of the peace elected "
        "November 5, 2024: Franklin Higgins, Rita Laferriere, "
        "R.J. Burke, Delbert Reed, and Stephanie Wales. The "
        "listing publishes no vote totals or party labels and "
        "none are recorded.")
    return spec("east-haven", label, offices, jp)


SPECS.append(east_haven_spec())

# ---------------------------------------------------------------- East Montpelier
EM_REPORT = {
    "url": "https://eastmontpeliervt.org/wp-content/uploads/2026/02/2025-EMont-Town-Report.pdf",
    "note": "PLACEHOLDER",
}
EM_CHARTER = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/114E",
    "note": "PLACEHOLDER",
}
EM_SITE = {
    "url": "https://eastmontpeliervt.org/",
    "note": "PLACEHOLDER",
}


def em_report(note):
    return S(EM_REPORT, "Town of East Montpelier 176th Annual "
             f"Report (eastmontpeliervt.org): {note}")


def em_charter(note):
    return S(EM_CHARTER, "Title 24 Appendix V.S.A. chapter 114E "
             f"(official text, Vermont General Assembly): {note}")


def em_site(note):
    return S(EM_SITE, "Town of East Montpelier official website "
             f"(eastmontpeliervt.org, current): {note}")


def east_montpelier_spec():
    label = "Town of East Montpelier"
    offices = [
        office("selectboard", "Selectboard Member", "East Montpelier Selectboard", 5,
               [sb_dir("lists five East Montpelier Selectboard "
                       "members: Thomas Brazier, Joseph Brooks, Carl "
                       "Etnier, Seth Gardner, and Scott Hess."),
                em_report("the officer tables list the same five, "
                          "with Seth Gardner as Chair and Scott "
                          "Hess as Vice Chair (printing 'Tom "
                          "Brazier' and 'Joe Brooks').")],
               [holder("Seth Gardner", "seth-gardner"),
                holder("Scott Hess", "scott-hess"),
                holder("Carl Etnier", "carl-etnier"),
                holder("Thomas Brazier", "thomas-brazier"),
                holder("Joseph Brooks", "joseph-brooks")]),
        office("town-clerk", "Town Clerk", "East Montpelier Town Clerk", 1,
               [em_charter("section 5 provides that the Town Clerk "
                           "is APPOINTED by the Selectboard."),
                em_report("the appointed-officers table lists Rosie "
                          "Laquerre as Town Clerk."),
                em_site("the town's Town Clerk page confirms Rosie "
                        "Laquerre as the current Town Clerk."),
                guide("lists Rosie Laquerre as Town Clerk of East "
                      "Montpelier.")],
               [holder("Rosie Laquerre", "rosie-laquerre",
                       how_seated="appointed")]),
        office("town-treasurer", "Town Treasurer", "East Montpelier Town Treasurer", 1,
               [em_charter("section 3 provides that the Town "
                           "Treasurer is APPOINTED by the "
                           "Selectboard."),
                em_report("the appointed-officers table lists "
                          "Michele Pallas as Town Treasurer (titled "
                          "Business Manager)."),
                guide("lists Michele Pallas as Town Treasurer of "
                      "East Montpelier.")],
               [holder("Michele Pallas", "michele-pallas",
                       how_seated="appointed")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "East Montpelier Collector of Delinquent Taxes", 1,
               [em_charter("section 6 provides that the Collector of "
                           "Delinquent Taxes is APPOINTED by the "
                           "Selectboard."),
                em_report("the appointed-officers table lists "
                          "Michele Pallas as Collector of "
                          "Delinquent Taxes (she also serves as "
                          "Collector of Current Taxes under the same "
                          "section, which is not separately "
                          "modeled).")],
               [holder("Michele Pallas", "michele-pallas",
                       how_seated="appointed")]),
        office("moderator", "Moderator", "East Montpelier Moderator", 1,
               [em_report("the 2026 warning's Article 1 placed the "
                          "Moderator on the ballot, and the town's "
                          "2026 Town Meeting page records Michael "
                          "Duane elected Moderator for 2026.")],
               [holder("Michael Duane", "michael-duane")]),
        office("lister", "Lister", "East Montpelier Listers", 3,
               [em_report("the officer tables list three elected "
                          "Listers: Deborah Fillion (re-elected "
                          "2026, 3-year term), Ross Hazel (expiring "
                          "2027), and Richard Harrington (expiring "
                          "2028).")],
               [holder("Deborah Fillion", "deborah-fillion"),
                holder("Ross Hazel", "ross-hazel"),
                holder("Richard Harrington", "richard-harrington")]),
        office("auditor", "Auditor", "East Montpelier Auditors", 3,
               [em_report("the officer tables list three elected "
                          "Auditors: Carla Occaso (re-elected 2026, "
                          "3-year term; the report prints 'Carla "
                          "(Neary) Occaso'), Ed Deegan (expiring "
                          "2027), and Deborah Fillion (expiring "
                          "2028).")],
               [holder("Carla Occaso", "carla-occaso"),
                holder("Edward Deegan", "edward-deegan"),
                holder("Deborah Fillion", "deborah-fillion")]),
        office("first-constable", "First Constable", "East Montpelier First Constable", 1,
               [em_report("the officer tables record that the "
                          "constable office ceased to be elected "
                          "by vote of the 2022 Town Meeting and has "
                          "been appointed by the Selectboard since "
                          "March 2023; the report's appointee is "
                          "superseded by the town's current "
                          "Constables page, which lists the First "
                          "Constable position as 'TBD' with the "
                          "town recruiting. Structure only: the "
                          "seat is recorded vacant, not filled."),
                em_site("the Constables page lists 'TBD, First "
                        "Constable' and states the town is "
                        "recruiting a constable.")]),
        office("planning-commissioner", "Planning Commissioner",
               "East Montpelier Planning Commission", 9,
               [em_report("Article 1 of the 2026 warning placed "
                          "three Planning Commissioner seats (3-year "
                          "terms) on the ballot, fixing a nine-member "
                          "elected commission; the town's 2026 Town "
                          "Meeting page records Clarice Cutler, "
                          "Alexander Rob, and Rebecca Schrader "
                          "elected in 2026. The members elected in "
                          "2024 and 2025 are not named in the "
                          "report's tables, so their seats are left "
                          "unfilled rather than guessed.")],
               [holder("Clarice Cutler", "clarice-cutler"),
                holder("Alexander Rob", "alexander-rob"),
                holder("Rebecca Schrader", "rebecca-schrader")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "East Montpelier Justices of the Peace", 10,
               [jp_src("lists ten East Montpelier justices of the "
                       "peace: Janice Aldrich, Virginia \"Ginny\" "
                       "Burley, Edward Deegan, Richard \"Jez\" "
                       "Harrington, Edith \"Edie\" Miller, Jamie "
                       "O'Hare, Rebecca Reed, Charles \"Cort\" "
                       "Richardson, Elise Thorsen, and Janice "
                       "Waterman."),
                em_report("the officer tables list the same ten "
                          "justices of the peace, elected November "
                          "2024. The report's parenthetical party "
                          "labels are not carried; the Secretary of "
                          "State listing governs this slate.")],
               [holder("Janice Aldrich", "janice-aldrich"),
                holder("Virginia Burley", "virginia-burley",
                       ballot_name="Virginia \"Ginny\" Burley"),
                holder("Edward Deegan", "edward-deegan"),
                holder("Richard Harrington", "richard-harrington",
                       ballot_name="Richard \"Jez\" Harrington"),
                holder("Edith Miller", "edith-miller",
                       ballot_name="Edith \"Edie\" Miller"),
                holder("Jamie O'Hare", "jamie-ohare"),
                holder("Rebecca Reed", "rebecca-reed"),
                holder("Charles Richardson", "charles-richardson",
                       ballot_name="Charles \"Cort\" Richardson"),
                holder("Elise Thorsen", "elise-thorsen"),
                holder("Janice Waterman", "janice-waterman")]),
    ]
    jp = jp_election(
        "east-montpelier-vt", label, 10,
        "lists ten East Montpelier justices of the peace elected "
        "November 5, 2024: Janice Aldrich, Virginia \"Ginny\" "
        "Burley, Edward Deegan, Richard \"Jez\" Harrington, Edith "
        "\"Edie\" Miller, Jamie O'Hare, Rebecca Reed, Charles "
        "\"Cort\" Richardson, Elise Thorsen, and Janice Waterman. "
        "The listing publishes no vote totals or party labels and "
        "none are recorded.",
        [em_report("the officer tables list the same ten justices "
                   "of the peace.")])
    return spec("east-montpelier", label, offices, jp)


SPECS.append(east_montpelier_spec())

# ---------------------------------------------------------------- emit
for s in SPECS:
    path = OUT / f"{s['place_slug']}.json"
    path.write_text(json.dumps(s, indent=2) + "\n")
    print(f"wrote {path.name}: {len(s['offices'])} offices")
print(f"{len(SPECS)} specs")
