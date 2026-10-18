#!/usr/bin/env python3
"""Batch 8 of the VT #163 municipal fan-out (alphabetical positions
70-79): Eden, Elmore, Enosburg Falls (village), Enosburgh, Essex,
Essex Junction (city), Fair Haven, Fairfax, Fairfield, Fairlee.
Emits one JSON spec per municipality for build_vt_municipality.py.
Research: vt_muni_batch8_research.md.

Identity calls baked into this batch (all flagged on #163):
- Essex Town JPs Alyssa Black, Leonora Dodge, and Golrang "Rey"
  Garofano are the sitting Chittenden-24 / Chittenden-23 state
  representatives (each styled "of Essex" in the House Journal;
  Chittenden-23 and -24 are Essex Town districts). Their existing
  state-tier person records are REUSED via existing_person_id; the
  JP candidacies are appended to those records by hand.
- Fairlee Treasurer Jessica Chase is minted as a SEPARATE person
  from Bradford's appointed Treasurer Jessica Chase (batch 3):
  same name and office in adjacent towns, but no second fact
  proves identity (distinct-person default).
- Fair Haven's lister John (Jack) Adams is minted as a separate
  person from the JP of the same printed name (slug
  john-adams-lister): the town's JP slate itself distinguishes
  two John Adamses, and no source ties the lister to either.
- Enosburgh's JP election seated ten in November 2024, but Avis
  Gervais died July 26, 2025 (Village of Enosburg Falls 2025
  Annual Report dedication); she is recorded in the contest note,
  not minted, and her seat stands vacant.
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
                  f"(VT municipal batch 8); issue #163 "
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
                  f"# municipal fan-out batch 8; issue #163 "
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

# ---------------------------------------------------------------- Eden
EDEN_REPORT = {
    "url": "https://www.edenvt.org/wp-content/uploads/2026/02/Eden-Town-Report-24-25.pdf",
    "note": "PLACEHOLDER",
}
EDEN_OFFICERS = {
    "url": "https://www.edenvt.org/boards_commissions/102-2/",
    "note": "PLACEHOLDER",
}


def eden_report(note):
    return S(EDEN_REPORT, "Town of Eden 2024-25 Annual Town Report "
             f"(edenvt.org): {note}")


def eden_officers(note):
    return S(EDEN_OFFICERS, "Town of Eden official Officers page "
             f"(edenvt.org, current): {note}")


def eden_spec():
    label = "Town of Eden"
    offices = [
        office("selectboard", "Selectboard Member", "Eden Selectboard", 3,
               [sb_dir("lists three Eden Selectboard members: Timothy "
                       "Bullard (Chair), Ricky Morin, and Clayton "
                       "Whittemore."),
                eden_report("the TOWN OFFICERS table lists Tim Bullard "
                            "(term to 2028), Ricky Morin (2027), and "
                            "Clayton Whittemore (2026); the June 2026 "
                            "directory seats all three after the March "
                            "2026 meeting, so Whittemore holds the seat "
                            "that stood in 2026.")],
               [holder("Timothy Bullard", "timothy-bullard"),
                holder("Ricky Morin", "ricky-morin"),
                holder("Clayton Whittemore", "clayton-whittemore")]),
        office("town-clerk", "Town Clerk", "Eden Town Clerk", 1,
               [eden_report("the TOWN OFFICERS table lists Melissa "
                            "Whitcomb as Town Clerk on a 3-year term."),
                guide("lists Melissa Whitcomb as Town Clerk of Eden."),
                eden_officers("the current officers page names Melissa "
                              "Whitcomb as Town Clerk.")],
               [holder("Melissa Whitcomb", "melissa-whitcomb")]),
        office("town-treasurer", "Town Treasurer", "Eden Town Treasurer", 1,
               [eden_report("the TOWN OFFICERS table lists Melissa "
                            "Whitcomb as Town Treasurer on a 3-year term."),
                guide("lists Melissa Whitcomb as Town Treasurer of Eden.")],
               [holder("Melissa Whitcomb", "melissa-whitcomb")]),
        office("moderator", "Moderator", "Eden Moderator", 1,
               [statute2646_structure("a moderator for a one-year term"),
                eden_report("the TOWN OFFICERS table lists H. Bruce "
                            "Burnor as Moderator with his term expired "
                            "March 2026; no official source publishes "
                            "the 2026 outcome, so the seat is left "
                            "unfilled.")]),
        office("auditor", "Auditor", "Eden Auditors", 3,
               [eden_report("the TOWN OFFICERS table lists Leslie "
                            "White as Auditor (term to 2028), Julie "
                            "Gates appointed May 27, 2025 to a seat "
                            "expiring 2026, and Ronald Miller resigned "
                            "March 24, 2025 with no successor named; "
                            "only White's seat is filled here.")],
               [holder("Leslie White", "leslie-white")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Eden Cemetery Commission", 5,
               [eden_report("the TOWN OFFICERS table lists five "
                            "Cemetery Commissioners on 5-year terms: "
                            "David Deery (2027), Jubal Durivage "
                            "(President, 2028), Colleen Durivage (2029), "
                            "Adam Degree (2030), and Faye Cochran "
                            "(2026); Cochran's seat stood in 2026 with "
                            "no published outcome, so four are minted.")],
               [holder("David Deery", "david-deery"),
                holder("Jubal Durivage", "jubal-durivage"),
                holder("Colleen Durivage", "colleen-durivage"),
                holder("Adam Degree", "adam-degree")]),
        office("trustee-of-public-funds", "Trustee of Public Funds",
               "Eden Trustees of Public Funds", 3,
               [eden_report("the TOWN OFFICERS table lists Melissa "
                            "Whitcomb (2027), Trevor Bidwell (2028), "
                            "and Bruce Shields appointed May 13, 2025 "
                            "to a seat expiring 2026; Shields's seat "
                            "stood in 2026 with no published outcome, "
                            "so two are minted.")],
               [holder("Melissa Whitcomb", "melissa-whitcomb"),
                holder("Trevor Bidwell", "trevor-bidwell")]),
        office("grand-juror", "Grand Juror", "Eden Grand Juror", 1,
               [statute2646_structure("a grand juror for a one-year term"),
                eden_report("the TOWN OFFICERS table prints the grand "
                            "juror, David Whitcomb, as '(Deceased)'; "
                            "the seat stands vacant.")]),
        office("town-agent", "Town Agent", "Eden Town Agent", 1,
               [statute2646_structure("a town agent for a one-year term")]),
        office("agent-to-convey-real-estate", "Agent to Convey Real Estate",
               "Eden Agent to Convey Real Estate", 1,
               [eden_report("the TOWN OFFICERS table lists Monique "
                            "Morway as Agent to Convey Real Estate with "
                            "her term expired March 2026; no official "
                            "source publishes the 2026 outcome, so the "
                            "seat is left unfilled. Structure only.")]),
        office("first-constable", "First Constable", "Eden First Constable", 1,
               [eden_report("the TOWN OFFICERS table lists Matthew Hill "
                            "as First Constable with his term expired "
                            "March 2026; no official source publishes "
                            "the 2026 outcome, so the seat is left "
                            "unfilled. Structure only.")]),
        office("second-constable", "Second Constable",
               "Eden Second Constable", 1,
               [eden_report("the TOWN OFFICERS table lists Bert Manning "
                            "as Second Constable with his term expired "
                            "March 2026; no official source publishes "
                            "the 2026 outcome, so the seat is left "
                            "unfilled. Structure only.")]),
        office("road-commissioner", "Road Commissioner",
               "Eden Road Commissioner", 1,
               [eden_report("the TOWN OFFICERS table lists Ricky Morin "
                            "as Road Commissioner with his term expired "
                            "March 2026; no official source publishes "
                            "the 2026 outcome, so the seat is left "
                            "unfilled. Structure only.")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Eden Justices of the Peace", 7,
               [jp_src("lists seven Eden justices of the peace: "
                       "H. Bruce Burnor, Kelly Daige, Amy Fitzgerald, "
                       "Tracey Morin, Molly Morin, Steven Schmeltzer, "
                       "and Leslie White."),
                eden_report("the TOWN OFFICERS table lists the same "
                            "seven justices of the peace (printing "
                            "'Steve Schmelzer'; the listing's form "
                            "governs).")],
               [holder("H. Bruce Burnor", "h-bruce-burnor"),
                holder("Kelly Daige", "kelly-daige"),
                holder("Amy Fitzgerald", "amy-fitzgerald"),
                holder("Tracey Morin", "tracey-morin"),
                holder("Molly Morin", "molly-morin"),
                holder("Steven Schmeltzer", "steven-schmeltzer"),
                holder("Leslie White", "leslie-white")]),
    ]
    jp = jp_election(
        "eden-vt", label, 7,
        "lists seven Eden justices of the peace elected "
        "November 5, 2024: H. Bruce Burnor, Kelly Daige, Amy "
        "Fitzgerald, Tracey Morin, Molly Morin, Steven Schmeltzer, "
        "and Leslie White. The listing publishes no vote totals or "
        "party labels and none are recorded.",
        [eden_report("the TOWN OFFICERS table lists the same seven "
                     "justices of the peace.")])
    return spec("eden", label, offices, jp)


SPECS.append(eden_spec())

# ---------------------------------------------------------------- Elmore
ELMORE_DIR = {
    "url": "https://elmorevt.org/town/town-directory/",
    "note": "PLACEHOLDER",
}
ELMORE_CEM = {
    "url": "https://elmorevt.org/town/cemetery-commission/",
    "note": "PLACEHOLDER",
}


def elmore_dir(note):
    return S(ELMORE_DIR, "Town of Elmore official Town Directory page "
             f"(elmorevt.org, current): {note}")


def elmore_spec():
    label = "Town of Elmore"
    offices = [
        office("selectboard", "Selectboard Member", "Elmore Selectboard", 3,
               [sb_dir("lists three Elmore Selectboard members: Trevor "
                       "Braun, Sharon Fortune, and Glenn Schwartz."),
                elmore_dir("the LOCALLY ELECTED table lists Glenn "
                           "Schwartz (Chair, to 2027), Sharon Fortune "
                           "(2028), and Trevor Braun (2029).")],
               [holder("Glenn Schwartz", "glenn-schwartz"),
                holder("Sharon Fortune", "sharon-fortune"),
                holder("Trevor Braun", "trevor-braun")]),
        office("moderator", "Moderator", "Elmore Moderator", 1,
               [elmore_dir("the LOCALLY ELECTED table lists Bruce "
                           "Olsson as Moderator, term to 2027.")],
               [holder("Bruce Olsson", "bruce-olsson")]),
        office("town-clerk", "Town Clerk", "Elmore Town Clerk", 1,
               [elmore_dir("the Town Directory lists the Town Clerk "
                           "under its APPOINTED heading: Sandra "
                           "Lacasse. The office has moved to "
                           "appointment in Elmore; the holder is "
                           "recorded as appointed."),
                guide("lists Sandra Lacasse as Town Clerk of Elmore.")],
               [holder("Sandra Lacasse", "sandra-lacasse",
                       how_seated="appointed")]),
        office("town-treasurer", "Town Treasurer", "Elmore Town Treasurer", 1,
               [elmore_dir("the Town Directory lists the Town "
                           "Treasurer under its APPOINTED heading: "
                           "Sharon Draper. The office has moved to "
                           "appointment in Elmore; the holder is "
                           "recorded as appointed."),
                guide("lists Sharon Draper as Town Treasurer of "
                      "Elmore.")],
               [holder("Sharon Draper", "sharon-draper",
                       how_seated="appointed")]),
        office("lister", "Lister", "Elmore Listers", 3,
               [elmore_dir("the LOCALLY ELECTED table lists three "
                           "listers: June McKinley (2029), Jamie "
                           "Kollar (2028), and Carla Blood (2027).")],
               [holder("June McKinley", "june-mckinley"),
                holder("Jamie Kollar", "jamie-kollar"),
                holder("Carla Blood", "carla-blood")]),
        office("auditor", "Auditor", "Elmore Auditors", 3,
               [elmore_dir("the LOCALLY ELECTED table lists Jane "
                           "Nutting as Auditor (2029); its other two "
                           "auditor entries are stale-dated (Carla "
                           "Blood 2025, Diane Cote 2024), so only "
                           "Nutting's seat is filled here.")],
               [holder("Jane Nutting", "jane-nutting")]),
        office("constable", "Constable", "Elmore Constable", 1,
               [elmore_dir("the LOCALLY ELECTED table lists Eddie "
                           "Adams as Constable, term to 2027.")],
               [holder("Eddie Adams", "eddie-adams")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Elmore Justices of the Peace", 5,
               [jp_src("lists five Elmore justices of the peace: "
                       "Trevor Braun, Diane Cote, Sharon Fortune, "
                       "Bruce Olsson, and Connie Perlin."),
                elmore_dir("the Town Directory lists the same five "
                           "justices of the peace, printing the fuller "
                           "form Constance Perlin, which governs the "
                           "name recorded here.")],
               [holder("Trevor Braun", "trevor-braun"),
                holder("Diane Cote", "diane-cote"),
                holder("Sharon Fortune", "sharon-fortune"),
                holder("Bruce Olsson", "bruce-olsson"),
                holder("Constance Perlin", "constance-perlin",
                       ballot_name="Connie Perlin")]),
    ]
    jp = jp_election(
        "elmore-vt", label, 5,
        "lists five Elmore justices of the peace elected "
        "November 5, 2024: Trevor Braun, Diane Cote, Sharon "
        "Fortune, Bruce Olsson, and Connie Perlin. The listing "
        "publishes no vote totals or party labels and none are "
        "recorded.",
        [elmore_dir("the Town Directory lists the same five "
                    "justices of the peace.")])
    return spec("elmore", label, offices, jp)


SPECS.append(elmore_spec())

# ---------------------------------------------------------------- Enosburgh
ENOS_SB = {
    "url": "https://www.enosburghvt.org/selecboard",
    "note": "PLACEHOLDER",
}
ENOS_OFFICERS = {
    "url": "https://www.enosburghvt.org/town-officers",
    "note": "PLACEHOLDER",
}
EFALLS_REPORT = {
    "url": "https://villageofenosburgfalls.org/wp-content/uploads/2026/02/2025-ANNUAL-REPORT-VOEF-FINAL-COPY.pdf",
    "note": "PLACEHOLDER",
}


def enos_sb(note):
    return S(ENOS_SB, "Town of Enosburgh official Selectboard page "
             f"(enosburghvt.org, current): {note}")


def enos_officers(note):
    return S(ENOS_OFFICERS, "Town of Enosburgh official Town Officers "
             f"page (enosburghvt.org, current): {note}")


def enosburgh_spec():
    label = "Town of Enosburgh"
    offices = [
        office("selectboard", "Selectboard Member", "Enosburgh Selectboard", 5,
               [enos_sb("lists five Selectboard members with term "
                        "years: Dean Wright (Chair, 2026), Pierre "
                        "Letourneau (Vice Chair, 2028), Larry Gervais "
                        "(2027), Jessica Eagles (2026), and Nick "
                        "Aldrich (2027); the live page seats all five "
                        "after the March 2026 meeting. The Secretary "
                        "of State directory publishes no Enosburgh "
                        "roster.")],
               [holder("Dean Wright", "dean-wright"),
                holder("Pierre Letourneau", "pierre-letourneau"),
                holder("Larry Gervais", "larry-gervais"),
                holder("Jessica Eagles", "jessica-eagles"),
                holder("Nick Aldrich", "nick-aldrich")]),
        office("moderator", "Moderator", "Enosburgh Moderator", 1,
               [enos_officers("lists 'Moderator - Elected, Patrick "
                              "Hayes - 2026'.")],
               [holder("Patrick Hayes", "patrick-hayes")]),
        office("town-clerk", "Town Clerk", "Enosburgh Town Clerk", 1,
               [enos_officers("lists Billie Jo Draper as elected Town "
                              "Clerk, term to 2027."),
                guide("lists Billie Draper as Town Clerk of "
                      "Enosburgh; the town's fuller form governs.")],
               [holder("Billie Jo Draper", "billie-jo-draper")]),
        office("town-treasurer", "Town Treasurer",
               "Enosburgh Town Treasurer", 1,
               [enos_officers("lists Billie Jo Draper as elected Town "
                              "Treasurer, term to 2027."),
                guide("lists Billie Draper as Town Treasurer of "
                      "Enosburgh.")],
               [holder("Billie Jo Draper", "billie-jo-draper")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Enosburgh Collector of Delinquent Taxes", 1,
               [enos_officers("heads the office 'Collector of "
                              "Delinquent Taxes - Elected' but names "
                              "no holder, so the seat is left "
                              "unfilled. Structure only.")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Enosburgh Justices of the Peace", 10,
               [jp_src("lists ten Enosburgh justices of the peace: "
                       "Patricia Boucher, Timothy Stetson, Peter "
                       "Perley, Sandra Murphy, Lucien Robtoy, Robert "
                       "Young, Avis Gervais, Pierre Letourneau, Sarah "
                       "Downes, and Angela Wright. Nine are minted; "
                       "Avis Gervais died July 26, 2025 (see the "
                       "election note) and her seat stands vacant.")],
               [holder("Patricia Boucher", "patricia-boucher"),
                holder("Timothy Stetson", "timothy-stetson"),
                holder("Peter Perley", "peter-perley"),
                holder("Sandra Murphy", "sandra-murphy"),
                holder("Lucien Robtoy", "lucien-robtoy"),
                holder("Robert Young", "robert-young"),
                holder("Pierre Letourneau", "pierre-letourneau"),
                holder("Sarah Downes", "sarah-downes"),
                holder("Angela Wright", "angela-wright")]),
    ]
    jp = jp_election(
        "enosburgh-vt", label, 10,
        "lists ten Enosburgh justices of the peace elected "
        "November 5, 2024: Patricia Boucher, Timothy Stetson, "
        "Peter Perley, Sandra Murphy, Lucien Robtoy, Robert Young, "
        "Avis Gervais, Pierre Letourneau, Sarah Downes, and Angela "
        "Wright. The listing publishes no vote totals or party "
        "labels and none are recorded. Avis Gervais died July 26, "
        "2025 (the Village of Enosburg Falls 2025 Annual Report is "
        "dedicated in part to her memory), so no person or "
        "membership is minted for her and her seat stands vacant; "
        "the nine surviving winners are recorded here.",
        [S(EFALLS_REPORT, "Village of Enosburg Falls Annual Report "
           "for the year ending December 31, 2025 "
           "(villageofenosburgfalls.org): the report is dedicated "
           "in part to the memory of Justice of the Peace Avis "
           "Gervais, who passed away July 26, 2025.")])
    return spec("enosburgh", label, offices, jp)


SPECS.append(enosburgh_spec())

# ---------------------------------------------------------------- Enosburg Falls
EFALLS_MINUTES = {
    "url": "https://villageofenosburgfalls.org/wp-content/uploads/2026/09/DRAFT-Minute-09-22-26-6.pdf",
    "note": "PLACEHOLDER",
}
EFALLS_CHARTER = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/219",
    "note": "PLACEHOLDER",
}


def efalls_report(note):
    return S(EFALLS_REPORT, "Village of Enosburg Falls Annual Report "
             "for the year ending December 31, 2025 "
             f"(villageofenosburgfalls.org): {note}")


def efalls_minutes(note):
    return S(EFALLS_MINUTES, "Village of Enosburg Falls Board of "
             "Trustees DRAFT minutes, September 22, 2026 "
             f"(villageofenosburgfalls.org): {note}")


def efalls_charter(note):
    return S(EFALLS_CHARTER, "Charter of the Village of Enosburg "
             "Falls, 24 Appendix V.S.A. ch. 219 (official text, "
             f"Vermont General Assembly): {note}")


def enosburg_falls_spec():
    label = "Village of Enosburg Falls"
    offices = [
        office("village-trustee", "Village Trustee",
               "Enosburg Falls Board of Trustees", 5,
               [efalls_charter("section 4 provides a Board of five "
                               "Trustees on staggered 3-year terms."),
                efalls_report("the List of Principal Officials names "
                              "Eli Gabuzda (Chair, term printed 2026), "
                              "Heather Moore (Vice Chair, 2026), "
                              "Leonard Charron (2027), Jason Longway "
                              "(2027, appointed), and David Gervais "
                              "(2028)."),
                efalls_minutes("Gabuzda chairs the September 22, 2026 "
                               "trustees' meeting and Charron, "
                               "Gervais, and Longway sit; Moore is "
                               "absent from the roll. Gabuzda's seat "
                               "stood at the March 10, 2026 election "
                               "and he holds it; Moore's seat also "
                               "stood in March 2026, its outcome is "
                               "published nowhere, and she does not "
                               "sit in September 2026, so her seat is "
                               "left unfilled.")],
               [holder("Eli Gabuzda", "eli-gabuzda"),
                holder("Leonard Charron", "leonard-charron"),
                holder("David Gervais", "david-gervais"),
                holder("Jason Longway", "jason-longway",
                       how_seated="appointed")]),
        office("moderator", "Moderator", "Enosburg Falls Moderator", 1,
               [efalls_charter("section 3(a) provides that the annual "
                               "meeting elects a Moderator for one "
                               "year."),
                efalls_report("the List of Principal Officials names "
                              "Patrick Hayes as Moderator to 2026; "
                              "the March 10, 2026 election outcome is "
                              "published nowhere, so the seat is left "
                              "unfilled. Structure only.")]),
        office("village-clerk", "Village Clerk", "Enosburg Falls Village Clerk", 1,
               [efalls_charter("section 3(a) provides that the annual "
                               "meeting elects a Clerk for one year."),
                efalls_report("the List of Principal Officials names "
                              "Sandra Ferland as interim appointed "
                              "Clerk to 2026; the March 10, 2026 "
                              "election outcome is published nowhere, "
                              "so the seat is left unfilled. Structure "
                              "only.")]),
        office("village-treasurer", "Village Treasurer",
               "Enosburg Falls Village Treasurer", 1,
               [efalls_charter("section 3(a) provides that the annual "
                               "meeting elects a Treasurer for one "
                               "year."),
                efalls_report("the List of Principal Officials names "
                              "Laurie Stanley as interim appointed "
                              "Treasurer to 2026; the March 10, 2026 "
                              "election outcome is published nowhere, "
                              "so the seat is left unfilled. Structure "
                              "only.")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Enosburg Falls Collector of Delinquent Taxes", 1,
               [efalls_charter("section 3(b) permits the village to "
                               "elect such other officers as the "
                               "public interest requires."),
                efalls_report("the List of Principal Officials names "
                              "Laurie Stanley as appointed Collector "
                              "of Delinquent Taxes to 2026; the March "
                              "10, 2026 outcome is published nowhere, "
                              "so the seat is left unfilled. Structure "
                              "only.")]),
    ]
    return spec("enosburg-falls", label, offices)


SPECS.append(enosburg_falls_spec())

# ---------------------------------------------------------------- Essex
ESSEX_CHARTER = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/117",
    "note": "PLACEHOLDER",
}
ESSEX_RESULTS = {
    "url": "https://www.essexvt.gov/DocumentCenter/View/16344/Election-Official-results-3-3-26",
    "note": "PLACEHOLDER",
}
ESSEX_REPORT = {
    "url": "https://www.essexvt.gov/ArchiveCenter/ViewFile/Item/10415",
    "note": "PLACEHOLDER",
}


def essex_charter(note):
    return S(ESSEX_CHARTER, "Charter of the Town of Essex, "
             "24 Appendix V.S.A. ch. 117 (official text, Vermont "
             f"General Assembly): {note}")


def essex_results(note):
    return S(ESSEX_RESULTS, "Town of Essex OFFICIAL RESULTS, "
             f"March 3, 2026 election (essexvt.gov): {note}")


def essex_spec():
    label = "Town of Essex"
    offices = [
        office("selectboard", "Selectboard Member", "Essex Selectboard", 5,
               [essex_charter("section 201 provides that the elected "
                              "officers of the town are Selectboard "
                              "members and Moderator; section 202 "
                              "fixes a Selectboard of five."),
                sb_dir("lists Essex Selectboard members Kendall "
                       "Chamberlin, Shannon Jackson, and Ethan "
                       "Lawrence among the board."),
                essex_results("Andy Watts (977 votes) and Meg "
                              "Zimmerman (1,012) won the two 3-year "
                              "seats and Ethan Lawrence (760) won the "
                              "1-year remainder seat on March 3, 2026; "
                              "Chamberlin and Jackson won their seats "
                              "in 2025 and hold them to 2028. The "
                              "remainder seat opened when Chair "
                              "Tracey Delphia resigned January 19, "
                              "2026; she is not minted.")],
               [holder("Kendall Chamberlin", "kendall-chamberlin"),
                holder("Shannon Jackson", "shannon-jackson"),
                holder("Andy Watts", "andy-watts"),
                holder("Meg Zimmerman", "meg-zimmerman"),
                holder("Ethan Lawrence", "ethan-lawrence")]),
        office("moderator", "Moderator", "Essex Moderator", 1,
               [essex_charter("section 201 lists the Moderator among "
                              "the town's elected officers."),
                essex_results("John Sonnick was elected Moderator "
                              "with 1,286 votes on March 3, 2026.")],
               [holder("John Sonnick", "john-sonnick")]),
        office("town-clerk", "Town Clerk", "Essex Town Clerk", 1,
               [essex_charter("the charter's manager form of "
                              "government makes the Town Clerk an "
                              "appointed office."),
                essex_results("Tatsiana Bussiere attests the March 3, "
                              "2026 official results as Town Clerk; "
                              "she is recorded as the appointed "
                              "holder."),
                guide("lists Jennifer Booker as ACTING Town Clerk of "
                      "Essex (January 2026), superseded by Bussiere's "
                      "attestation of the March 2026 results.")],
               [holder("Tatsiana Bussiere", "tatsiana-bussiere",
                       how_seated="appointed")]),
        office("town-treasurer", "Town Treasurer", "Essex Town Treasurer", 1,
               [essex_charter("the charter's manager form of "
                              "government makes the Town Treasurer an "
                              "appointed office."),
                guide("lists Jennifer Booker as ACTING Town Treasurer "
                      "of Essex (January 2026); no official source "
                      "publishes a current holder, so the seat is "
                      "left unfilled. Structure only.")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Essex Justices of the Peace", 15,
               [jp_src("lists fifteen Town of Essex justices of the "
                       "peace: Alyssa Black, Iris Banks, Leonora "
                       "Dodge, Alexis Dubief, Betsy Dunn, Rey "
                       "Garofano, Dawn Hill-Fleury, Georgia Lavigne, "
                       "Erik Post, Cindy Seivwright, Ken Signorello, "
                       "Margaret Smith, Liz Subin, Laura Taylor, and "
                       "Irene Wrenner. Black, Dodge, and Garofano "
                       "are the sitting Chittenden-24 and "
                       "Chittenden-23 state representatives, each "
                       "styled 'of Essex' in the House Journal; "
                       "their existing state-tier person records are "
                       "reused.")],
               [holder("Alyssa Black", "alyssa-black",
                       existing_person_id="ocd-person/65bad7fd-3995-5891-a77d-58527653962b"),
                holder("Iris Banks", "iris-banks"),
                holder("Leonora Dodge", "leonora-dodge",
                       existing_person_id="ocd-person/448e710e-405d-570b-981b-51b59eb42a2a"),
                holder("Alexis Dubief", "alexis-dubief"),
                holder("Betsy Dunn", "betsy-dunn"),
                holder("Golrang \"Rey\" Garofano", "golrang-rey-garofano",
                       existing_person_id="ocd-person/77e098b4-f6a8-5e5f-8160-a94cc144c4a4",
                       ballot_name="Rey Garofano"),
                holder("Dawn Hill-Fleury", "dawn-hill-fleury"),
                holder("Georgia Lavigne", "georgia-lavigne"),
                holder("Erik Post", "erik-post"),
                holder("Cindy Seivwright", "cindy-seivwright"),
                holder("Ken Signorello", "ken-signorello"),
                holder("Margaret Smith", "margaret-smith"),
                holder("Liz Subin", "liz-subin"),
                holder("Laura Taylor", "laura-taylor"),
                holder("Irene Wrenner", "irene-wrenner")]),
    ]
    jp = jp_election(
        "essex-vt", label, 15,
        "lists fifteen Town of Essex justices of the peace elected "
        "November 5, 2024: Alyssa Black, Iris Banks, Leonora Dodge, "
        "Alexis Dubief, Betsy Dunn, Rey Garofano, Dawn Hill-Fleury, "
        "Georgia Lavigne, Erik Post, Cindy Seivwright, Ken "
        "Signorello, Margaret Smith, Liz Subin, Laura Taylor, and "
        "Irene Wrenner. The listing publishes no vote totals or "
        "party labels and none are recorded.")
    return spec("essex", label, offices, jp)


SPECS.append(essex_spec())

# ---------------------------------------------------------------- Essex Junction
EJ_CHARTER = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/004",
    "note": "PLACEHOLDER",
}


def ej_charter(note):
    return S(EJ_CHARTER, "Charter of the City of Essex Junction, "
             "24 Appendix V.S.A. ch. 004 (official text, Vermont "
             f"General Assembly): {note}")


def essex_junction_spec():
    label = "City of Essex Junction"
    offices = [
        office("city-council", "City Council Member",
               "Essex Junction City Council", 5,
               [ej_charter("sections 202-204 provide an elected City "
                           "Council of five; the Council elects its "
                           "own President, Vice President, and Clerk "
                           "from its members."),
                sb_dir("the directory's Essex Junction row lists the "
                       "five councilors: Raj Chawla, Bethany Clark, "
                       "Tim Miller (Clerk), Brian Shelden, and Amber "
                       "Thibeault (President). The city's council "
                       "minutes of May 13 and June 3, 2026 seat the "
                       "same five, with Miller as Vice President and "
                       "Clark as Council Clerk; Chawla and Clark "
                       "replaced Marcus Certa and Elaine Haney at "
                       "the spring 2026 annual meeting.")],
               [holder("Amber Thibeault", "amber-thibeault"),
                holder("Tim Miller", "tim-miller"),
                holder("Bethany Clark", "bethany-clark"),
                holder("Raj Chawla", "raj-chawla"),
                holder("Brian Shelden", "brian-shelden")]),
        office("moderator", "Moderator", "Essex Junction Moderator", 1,
               [ej_charter("section 302 provides that the Moderator "
                           "is appointed by the City Council for a "
                           "one-year term. Steve Eustis presided as "
                           "Moderator at the March 23, 2026 "
                           "informational hearing; he is recorded as "
                           "the appointed holder.")],
               [holder("Steve Eustis", "steve-eustis",
                       how_seated="appointed")]),
        office("city-clerk", "City Clerk", "Essex Junction City Clerk", 1,
               [ej_charter("section 602(o) provides that the City "
                           "Manager recommends the City Clerk's "
                           "appointment annually with Council "
                           "approval; the office is appointive."),
                guide("lists Susan McNamara-Hill as clerk for Essex "
                      "Junction; the city's June 3, 2026 council "
                      "minutes name her as City Clerk. She is "
                      "recorded as the appointed holder.")],
               [holder("Susan McNamara-Hill", "susan-mcnamara-hill",
                       how_seated="appointed")]),
        office("city-treasurer", "City Treasurer",
               "Essex Junction City Treasurer", 1,
               [ej_charter("section 602 provides for a Treasurer as "
                           "an employee appointed by the City "
                           "Manager; the office is appointive."),
                guide("lists Susan McNamara-Hill as treasurer for "
                      "Essex Junction, and the city's March 23, 2026 "
                      "minutes style her 'Clerk/Treasurer'. She is "
                      "recorded as the appointed holder.")],
               [holder("Susan McNamara-Hill", "susan-mcnamara-hill",
                       how_seated="appointed")]),
        office("library-trustee", "Library Trustee",
               "Essex Junction Brownell Library Trustees", 5,
               [ej_charter("section 301 provides five Brownell "
                           "Library Trustees elected for 5-year "
                           "terms, and section 705 adds five "
                           "permanent self-perpetuating trustees "
                           "alongside them. No official source "
                           "distinguishes which sitting trustees "
                           "hold the five elected seats, so the "
                           "post is created structure-only and no "
                           "holders are minted.")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Essex Junction Justices of the Peace", 15,
               [jp_src("lists fifteen City of Essex Junction justices "
                       "of the peace: Kelly McCutcheon Adams, Katie "
                       "Ballard, Rajan Chawla, Sandra Chittenden, "
                       "Diane Clemens, Cheri Davis, Dylan "
                       "Giambatista, Elaine Haney, Ryan Mclaren, "
                       "Stephanie Holden, Brian Shelden, Gibson "
                       "Smith, Carmon Verasamy, Jordan Verasamy, and "
                       "Elisa Ziglar. The city elects its own "
                       "justices of the peace. Rajan Chawla is City "
                       "Councilor Raj Chawla.")],
               [holder("Kelly McCutcheon Adams", "kelly-mccutcheon-adams"),
                holder("Katie Ballard", "katie-ballard"),
                holder("Raj Chawla", "raj-chawla",
                       ballot_name="Rajan Chawla"),
                holder("Sandra Chittenden", "sandra-chittenden"),
                holder("Diane Clemens", "diane-clemens"),
                holder("Cheri Davis", "cheri-davis"),
                holder("Dylan Giambatista", "dylan-giambatista"),
                holder("Elaine Haney", "elaine-haney"),
                holder("Ryan Mclaren", "ryan-mclaren"),
                holder("Stephanie Holden", "stephanie-holden"),
                holder("Brian Shelden", "brian-shelden"),
                holder("Gibson Smith", "gibson-smith"),
                holder("Carmon Verasamy", "carmon-verasamy"),
                holder("Jordan Verasamy", "jordan-verasamy"),
                holder("Elisa Ziglar", "elisa-ziglar")]),
    ]
    jp = jp_election(
        "essex-junction-vt", label, 15,
        "lists fifteen City of Essex Junction justices of the peace "
        "elected November 5, 2024: Kelly McCutcheon Adams, Katie "
        "Ballard, Rajan Chawla, Sandra Chittenden, Diane Clemens, "
        "Cheri Davis, Dylan Giambatista, Elaine Haney, Ryan "
        "Mclaren, Stephanie Holden, Brian Shelden, Gibson Smith, "
        "Carmon Verasamy, Jordan Verasamy, and Elisa Ziglar. The "
        "listing publishes no vote totals or party labels and none "
        "are recorded.")
    return spec("essex-junction", label, offices, jp)


SPECS.append(essex_junction_spec())

# ---------------------------------------------------------------- Fair Haven
FH_BALLOT26 = {
    "url": "https://fairhavenvt.gov/wp-content/uploads/2026/01/Sample-Ballot-Town-Meeting-March-3-2026.pdf",
    "note": "PLACEHOLDER",
}
FH_BALLOT25 = {
    "url": "https://fairhavenvt.gov/wp-content/uploads/2025/02/Town-Meeting-Ballot-March-4-2025.pdf",
    "note": "PLACEHOLDER",
}


def fh26(note):
    return S(FH_BALLOT26, "Town of Fair Haven official sample ballot, "
             f"Town Meeting March 3, 2026 (fairhavenvt.gov): {note}")


def fh25(note):
    return S(FH_BALLOT25, "Town of Fair Haven official sample ballot, "
             f"Town Meeting March 4, 2025 (fairhavenvt.gov): {note}")


def fair_haven_spec():
    label = "Town of Fair Haven"
    offices = [
        office("selectboard", "Selectboard Member", "Fair Haven Selectboard", 5,
               [sb_dir("lists five Fair Haven Selectboard members: "
                       "Keith Hier, Samuel Lucci (Board Clerk), "
                       "Dennis Reid, Richard Greenough, and Chadd "
                       "Viger (Chair)."),
                fh26("the 2026 ballot paired Dennis Reid against an "
                     "incumbent for the 3-year seat; the board's "
                     "post-election minutes seat Reid, and the "
                     "pre-election chair Glen Traverse no longer "
                     "sits.")],
               [holder("Chadd Viger", "chadd-viger"),
                holder("Keith Hier", "keith-hier"),
                holder("Samuel Lucci", "samuel-lucci"),
                holder("Dennis Reid", "dennis-reid"),
                holder("Richard Greenough", "richard-greenough")]),
        office("moderator", "Moderator", "Fair Haven Moderator", 1,
               [fh26("the 2026 moderator contest was write-in only, "
                     "and the town's published 2026 results could "
                     "not be obtained; Cecelia Hunt held the office "
                     "through 2025. The seat is left unfilled. "
                     "Structure only."),
                fh25("the 2025 ballot likewise carried the moderator "
                     "office.")]),
        office("town-clerk", "Town Clerk", "Fair Haven Town Clerk", 1,
               [fh25("Danielle Laramie was the printed candidate for "
                     "Town Clerk for a 3-year term in 2025 (ballot "
                     "prints 'Danielle (Dani Laramie) Roberts'); her "
                     "term runs to 2028, so the office was not on "
                     "the 2026 ballot."),
                guide("lists Danielle Laramie as Town Clerk of Fair "
                      "Haven; her form of name governs.")],
               [holder("Danielle Laramie", "danielle-laramie")]),
        office("town-treasurer", "Town Treasurer", "Fair Haven Town Treasurer", 1,
               [fh26("Sharon Adams was the sole printed candidate for "
                     "Town Treasurer in 2026 and is minted as the "
                     "elected holder on the official ballot and her "
                     "incumbency (sole-candidate pattern)."),
                guide("lists Sharon Adams as Town Treasurer of Fair "
                      "Haven.")],
               [holder("Sharon Adams", "sharon-adams")]),
        office("first-constable", "First Constable",
               "Fair Haven First Constable", 1,
               [fh25("Donald Proctor was the sole printed candidate "
                     "for First Constable in 2025 on the office's "
                     "2-year cycle and is minted as the elected "
                     "holder (sole-candidate pattern). The two "
                     "constable posts run on alternating cycles and "
                     "each appears only on its own year's ballot.")],
               [holder("Donald Proctor", "donald-proctor")]),
        office("second-constable", "Second Constable",
               "Fair Haven Second Constable", 1,
               [fh26("Sean Galvin was the sole printed candidate for "
                     "Second Constable in 2026 on the office's "
                     "2-year cycle and is minted as the elected "
                     "holder (sole-candidate pattern).")],
               [holder("Sean Galvin", "sean-galvin")]),
        office("lister", "Lister", "Fair Haven Listers", 3,
               [fh25("Sharon Adams (3-year term) and John (Jack) "
                     "Adams (2-year remainder) were the sole printed "
                     "lister candidates in 2025 and are minted as "
                     "elected (sole-candidate pattern). The lister "
                     "John (Jack) Adams is minted as a separate "
                     "person from the justice of the peace of the "
                     "same printed name: the town's JP slate itself "
                     "distinguishes two John Adamses and no source "
                     "ties the lister to either."),
                fh26("Peter M. Laramie was the sole printed "
                     "candidate for the 3-year lister seat in 2026 "
                     "and is minted as elected.")],
               [holder("Sharon Adams", "sharon-adams"),
                holder("John (Jack) Adams", "john-adams-lister"),
                holder("Peter M. Laramie", "peter-m-laramie")]),
        office("auditor", "Auditor", "Fair Haven Auditors", 3,
               [fh25("both auditor seats on the 2025 ballot were "
                     "write-in only."),
                fh26("the 2026 auditor contest was likewise write-in "
                     "only, and the town's published 2026 results "
                     "could not be obtained; no winners are "
                     "published in the sources read, so all three "
                     "seats are left unfilled. Structure only.")]),
        office("trustee-of-public-funds", "Trustee of Public Funds",
               "Fair Haven Trustees of Public Funds", 3,
               [fh26("Maureen Hall was the sole printed candidate "
                     "for the 3-year Trustee of Public Funds seat in "
                     "2026 and is minted as elected."),
                fh25("Peter M. Laramie (3-year term) and Judith "
                     "Gevry (2-year remainder) were the sole printed "
                     "candidates in 2025 and are minted as elected "
                     "(sole-candidate pattern).")],
               [holder("Maureen Hall", "maureen-hall"),
                holder("Peter M. Laramie", "peter-m-laramie"),
                holder("Judith Gevry", "judith-gevry")]),
        office("library-trustee", "Library Trustee",
               "Fair Haven Library Trustees", 5,
               [fh25("Christine Sheldon was the sole printed "
                     "candidate for a 3-year library trustee seat "
                     "in 2025 and is minted as elected. The town's "
                     "elected-officials tables fix the board at "
                     "five seats."),
                fh26("Cecelia Hunt was the sole printed candidate "
                     "for the 1-year library seat in 2026 (ballot "
                     "prints 'Cecelia \"Ceil\" Hunt') and is minted "
                     "as elected; two further 2026 seats were "
                     "write-in only with no published winners, and "
                     "the remaining seat's holder is not published "
                     "in current sources, so three seats are left "
                     "unfilled.")],
               [holder("Christine Sheldon", "christine-sheldon"),
                holder("Cecelia Hunt", "cecelia-hunt")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Fair Haven Justices of the Peace", 7,
               [jp_src("lists seven Fair Haven justices of the peace: "
                       "Cynthia Adams, John Adams, John (Jack) Adams, "
                       "Melissa (Katie) Adams-Sliva, Lorraine Brown, "
                       "Jason Scott Coupal, and Judith Gevry. The "
                       "slate itself distinguishes John Adams from "
                       "John (Jack) Adams; both are minted as listed.")],
               [holder("Cynthia Adams", "cynthia-adams"),
                holder("John Adams", "john-adams"),
                holder("John (Jack) Adams", "john-jack-adams"),
                holder("Melissa (Katie) Adams-Sliva",
                       "melissa-katie-adams-sliva"),
                holder("Lorraine Brown", "lorraine-brown"),
                holder("Jason Scott Coupal", "jason-scott-coupal"),
                holder("Judith Gevry", "judith-gevry")]),
    ]
    jp = jp_election(
        "fair-haven-vt", label, 7,
        "lists seven Fair Haven justices of the peace elected "
        "November 5, 2024: Cynthia Adams, John Adams, John (Jack) "
        "Adams, Melissa (Katie) Adams-Sliva, Lorraine Brown, Jason "
        "Scott Coupal, and Judith Gevry. The listing publishes no "
        "vote totals or party labels and none are recorded.")
    return spec("fair-haven", label, offices, jp)


SPECS.append(fair_haven_spec())

# ---------------------------------------------------------------- Fairfax
FFX_REPORT = {
    "url": "https://cms2.revize.com/revize/fairfax/2025%20Town%20Report%20Final.pdf",
    "note": "PLACEHOLDER",
}


def ffx(note):
    return S(FFX_REPORT, "Town of Fairfax FY2025 Town Report "
             f"(fairfax-vt.gov): {note}")


def fairfax_spec():
    label = "Town of Fairfax"
    offices = [
        office("selectboard", "Selectboard Member", "Fairfax Selectboard", 5,
               [ffx("the Elected Officers table and roster list five "
                    "Selectboard members: Lauri Fisher (Chair, to "
                    "2029), Kurt Magnan (Vice Chair, 2028), Tim Burns "
                    "(2027), Tim Germaine (2028), and Anna Hudson "
                    "(2027). The town's 2026 results corroborate: "
                    "Fisher won the 3-year seat (710 votes; results "
                    "print 'Lauri Bellows Fisher') and Germaine the "
                    "2-year seat (670). The Secretary of State "
                    "directory publishes no Fairfax roster.")],
               [holder("Lauri Fisher", "lauri-fisher"),
                holder("Kurt Magnan", "kurt-magnan"),
                holder("Tim Burns", "tim-burns"),
                holder("Tim Germaine", "tim-germaine"),
                holder("Anna Hudson", "anna-hudson")]),
        office("moderator", "Moderator", "Fairfax Moderator", 1,
               [ffx("the 2026 Warning, Article 1, elects a Town "
                    "Moderator for one year by Australian ballot, and "
                    "the town's 2026 results re-elect Roberta "
                    "Rodimer with 923 votes.")],
               [holder("Roberta Rodimer", "roberta-rodimer")]),
        office("town-clerk", "Town Clerk", "Fairfax Town Clerk", 1,
               [ffx("the Town Clerk is absent from the report's "
                    "Elected Officers table and from the 2026 "
                    "Warning; the clerkship has been a full-time "
                    "appointed staff position since 2023. Lynn Parah "
                    "is recorded as the appointed holder."),
                guide("lists Lynn Parah as Town Clerk of Fairfax.")],
               [holder("Lynn Parah", "lynn-parah",
                       how_seated="appointed")]),
        office("town-treasurer", "Town Treasurer", "Fairfax Town Treasurer", 1,
               [ffx("the report's records and the Selectboard minutes "
                    "of February 20, 2023 show Amy Sears appointed to "
                    "serve the remainder of a three-year treasurer "
                    "term; she is recorded as the appointed holder."),
                guide("lists Amy Sears as Town Treasurer of "
                      "Fairfax.")],
               [holder("Amy Sears", "amy-sears",
                       how_seated="appointed")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Fairfax Collector of Delinquent Taxes", 1,
               [ffx("the Elected Officers table lists Johanna R. "
                    "Blake as Collector of Delinquent Taxes, term to "
                    "2027; her signed FY2025 Collector's statement "
                    "appears in the report.")],
               [holder("Johanna R. Blake", "johanna-r-blake")]),
        office("library-trustee", "Library Trustee",
               "Fairfax Community Library Trustees", 5,
               [ffx("the Elected Officers table lists five elected "
                    "Community Library Trustees: Barbara Murphy "
                    "(Chair, 2027), Marti Sterin (2027), Elizabeth "
                    "Griffin (2028), Sarah Barnes (2029), and Amy "
                    "Palmer (2029); the 2026 results corroborate "
                    "Barnes (638 votes) and Palmer (502).")],
               [holder("Barbara Murphy", "barbara-murphy"),
                holder("Sarah Barnes", "sarah-barnes"),
                holder("Marti Sterin", "marti-sterin"),
                holder("Elizabeth Griffin", "elizabeth-griffin"),
                holder("Amy Palmer", "amy-palmer")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Fairfax Cemetery Commission", 5,
               [ffx("the Elected Officers table lists five elected "
                    "Cemetery Commissioners: Sally Sweet (Chair, "
                    "2030), Treavor Howard (2029), Tim Germaine "
                    "(2028), David Shea (2027), and Robin Chapman "
                    "(2026). Chapman's seat stood in 2026 and the "
                    "official results show write-ins only, with the "
                    "winner named in no town source, so four are "
                    "minted and that seat is left unfilled.")],
               [holder("Sally Sweet", "sally-sweet"),
                holder("Treavor Howard", "treavor-howard"),
                holder("Tim Germaine", "tim-germaine"),
                holder("David Shea", "david-shea")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Fairfax Justices of the Peace", 12,
               [jp_src("lists twelve Fairfax justices of the peace: "
                       "Barbara Murphy, Steve Cormier, Julie "
                       "Filiberti, Mary Kay Raymond, Jeffrey Bartley, "
                       "Marjorie Ellsworth, Peter Fitzgerald, Gregory "
                       "Hartmann, Robert Horr, Donna Meunier, James "
                       "Minor, and Susan Mitchell."),
                ffx("the report's table lists the same twelve "
                    "justices of the peace (printing 'Greg Hartman'; "
                    "the listing's Gregory Hartmann governs).")],
               [holder("Barbara Murphy", "barbara-murphy"),
                holder("Steve Cormier", "steve-cormier"),
                holder("Julie Filiberti", "julie-filiberti"),
                holder("Mary Kay Raymond", "mary-kay-raymond"),
                holder("Jeffrey Bartley", "jeffrey-bartley"),
                holder("Marjorie Ellsworth", "marjorie-ellsworth"),
                holder("Peter Fitzgerald", "peter-fitzgerald"),
                holder("Gregory Hartmann", "gregory-hartmann"),
                holder("Robert Horr", "robert-horr"),
                holder("Donna Meunier", "donna-meunier"),
                holder("James Minor", "james-minor"),
                holder("Susan Mitchell", "susan-mitchell")]),
    ]
    jp = jp_election(
        "fairfax-vt", label, 12,
        "lists twelve Fairfax justices of the peace elected "
        "November 5, 2024: Barbara Murphy, Steve Cormier, Julie "
        "Filiberti, Mary Kay Raymond, Jeffrey Bartley, Marjorie "
        "Ellsworth, Peter Fitzgerald, Gregory Hartmann, Robert "
        "Horr, Donna Meunier, James Minor, and Susan Mitchell. The "
        "listing publishes no vote totals or party labels and none "
        "are recorded.",
        [ffx("the report's table lists the same twelve justices of "
             "the peace.")])
    return spec("fairfax", label, offices, jp)


SPECS.append(fairfax_spec())

# ---------------------------------------------------------------- Fairfield
FFD_MIN_DEC = {
    "url": "https://img1.wsimg.com/blobby/go/bcfe7f6a-21a0-4365-83b2-ca876176b0e8/downloads/101344a1-c178-43ad-bb8c-2b9f3c2de500/12.17.2025.pdf?ver=1767630027661",
    "note": "PLACEHOLDER",
}
FFD_MIN_JUN = {
    "url": "http://img1.wsimg.com/blobby/go/bcfe7f6a-21a0-4365-83b2-ca876176b0e8/downloads/e3e0f061-fb62-426e-9e9d-596d284747db/06.22.2026%20Minutes.pdf?ver=1790365902710",
    "note": "PLACEHOLDER",
}
FFD_MIN_JUL = {
    "url": "http://img1.wsimg.com/blobby/go/bcfe7f6a-21a0-4365-83b2-ca876176b0e8/downloads/be24de6f-a4bb-4f6d-93d7-d7eea5a108b2/07.13.2026%20Minutes.pdf?ver=1785864394919",
    "note": "PLACEHOLDER",
}


def ffd_dec(note):
    return S(FFD_MIN_DEC, "Town of Fairfield Selectboard minutes, "
             f"December 17, 2025: {note}")


def ffd_jun(note):
    return S(FFD_MIN_JUN, "Town of Fairfield Selectboard minutes, "
             f"June 22, 2026: {note}")


def ffd_jul(note):
    return S(FFD_MIN_JUL, "Town of Fairfield Selectboard minutes, "
             f"July 13, 2026: {note}")


def fairfield_spec():
    label = "Town of Fairfield"
    offices = [
        office("selectboard", "Selectboard Member", "Fairfield Selectboard", 5,
               [sb_dir("lists five Fairfield Selectboard members: "
                       "Ronald Bocash, Damian Brannon, Brian Dubie, "
                       "Thomas Howrigan (Chair), and David Persons."),
                ffd_jul("the July 13, 2026 minutes seat the same "
                        "five (Howrigan chairing, Persons as "
                        "Secretary), printing 'Damian Branon'; the "
                        "town's own spelling governs the name "
                        "recorded here. Gavin Ryan sat in December "
                        "2025 but is not on the current board and is "
                        "not minted.")],
               [holder("Thomas Howrigan", "thomas-howrigan"),
                holder("Brian Dubie", "brian-dubie"),
                holder("Ronald Bocash", "ronald-bocash"),
                holder("Damian Branon", "damian-branon"),
                holder("David Persons", "david-persons")]),
        office("town-clerk", "Town Clerk", "Fairfield Town Clerk", 1,
               [ffd_jun("the June 22, 2026 minutes treat Demetrius "
                        "Bolduc as the sitting Town Clerk (the Town "
                        "Clerk's report was given in his absence), "
                        "and the town's clerk page lists him as "
                        "clerk. No source states whether the office "
                        "is filled by election or appointment in "
                        "Fairfield; he is recorded as elected, with "
                        "the mode unverified."),
                guide("lists Linda Hodet as Town Clerk of Fairfield "
                      "(January 2026); Hodet was still clerk on "
                      "December 17, 2025 and is superseded by "
                      "Bolduc.")],
               [holder("Demetrius Bolduc", "demetrius-bolduc")]),
        office("town-treasurer", "Town Treasurer", "Fairfield Town Treasurer", 1,
               [guide("lists Amanda Forbes as Town Treasurer of "
                      "Fairfield."),
                ffd_dec("the December 17, 2025 minutes header names "
                        "Amanda Forbes as Treasurer.")],
               [holder("Amanda Forbes", "amanda-forbes")]),
        office("moderator", "Moderator", "Fairfield Moderator", 1,
               [statute2646_structure("a moderator for a one-year term")]),
        office("lister", "Lister", "Fairfield Listers", 3,
               [statute2646_structure("listers for staggered "
                                      "three-year terms")]),
        office("auditor", "Auditor", "Fairfield Auditors", 3,
               [statute2646_structure("auditors for staggered "
                                      "three-year terms")]),
        office("grand-juror", "Grand Juror", "Fairfield Grand Juror", 1,
               [statute2646_structure("a grand juror for a one-year term")]),
        office("town-agent", "Town Agent", "Fairfield Town Agent", 1,
               [statute2646_structure("a town agent for a one-year term")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Fairfield Justices of the Peace", 7,
               [jp_src("lists seven Fairfield justices of the peace: "
                       "Jonathan Branon, Bridget Howrigan Rivet, "
                       "Julie Wolcott, Paula Boomhower, Marianne "
                       "Dubie, James Consentino, and Marty Hornick.")],
               [holder("Jonathan Branon", "jonathan-branon"),
                holder("Bridget Howrigan Rivet", "bridget-howrigan-rivet"),
                holder("Julie Wolcott", "julie-wolcott"),
                holder("Paula Boomhower", "paula-boomhower"),
                holder("Marianne Dubie", "marianne-dubie"),
                holder("James Consentino", "james-consentino"),
                holder("Marty Hornick", "marty-hornick")]),
    ]
    jp = jp_election(
        "fairfield-vt", label, 7,
        "lists seven Fairfield justices of the peace elected "
        "November 5, 2024: Jonathan Branon, Bridget Howrigan Rivet, "
        "Julie Wolcott, Paula Boomhower, Marianne Dubie, James "
        "Consentino, and Marty Hornick. The listing publishes no "
        "vote totals or party labels and none are recorded.")
    return spec("fairfield", label, offices, jp)


SPECS.append(fairfield_spec())

# ---------------------------------------------------------------- Fairlee
FRL_MIN26 = {
    "url": "https://fairleevt.gov/uploads/dm/2672/2025_Town_Meeting_Minutes.pdf",
    "note": "PLACEHOLDER",
}
FRL_SB25 = {
    "url": "https://fairleevt.gov/uploads/dm/3030/Selectboard_Meeting_Minutes_20250310_Final.pdf",
    "note": "PLACEHOLDER",
}
FRL_AUD = {
    "url": "https://fairleevt.gov/uploads/dm/2865/Fairlee_AuditorsMinutes12.19.24.pdf",
    "note": "PLACEHOLDER",
}


def frl26(note):
    return S(FRL_MIN26, "Town of Fairlee official Town Meeting "
             "Minutes, March 3, 2026 (fairleevt.gov; the file is "
             f"named 2025 but its contents are the 2026 minutes): {note}")


def frl_sb25(note):
    return S(FRL_SB25, "Town of Fairlee Selectboard minutes, "
             f"March 10, 2025 (fairleevt.gov): {note}")


def frl_aud(note):
    return S(FRL_AUD, "Town of Fairlee Auditors' minutes, "
             f"December 19, 2024 (fairleevt.gov): {note}")


def fairlee_spec():
    label = "Town of Fairlee"
    offices = [
        office("selectboard", "Selectboard Member", "Fairlee Selectboard", 3,
               [sb_dir("lists three Fairlee Selectboard members: Peter "
                       "Berger, Miranda Clemson (Chair), and Lance "
                       "Mills."),
                frl26("the March 3, 2026 town meeting re-elected "
                      "Clemson to a 3-year term unopposed; Berger "
                      "chaired the board before the 2026 "
                      "reorganization and Clemson chairs it in the "
                      "June 2026 directory.")],
               [holder("Peter Berger", "peter-berger"),
                holder("Miranda Clemson", "miranda-clemson"),
                holder("Lance Mills", "lance-mills")]),
        office("moderator", "Moderator", "Fairlee Moderator", 1,
               [frl26("Article 1 elected Chaz Hinsley Moderator for "
                      "one year, unopposed.")],
               [holder("Chaz Hinsley", "chaz-hinsley")]),
        office("town-clerk", "Town Clerk", "Fairlee Town Clerk", 1,
               [guide("lists Georgette Wolf-Ludwig as Town Clerk of "
                      "Fairlee."),
                frl26("the town's officers tables style the clerk "
                      "elected for a 3-year term; Wolf-Ludwig has "
                      "served continuously and no clerk election fell "
                      "in 2025 or 2026.")],
               [holder("Georgette Wolf-Ludwig", "georgette-wolf-ludwig")]),
        office("town-treasurer", "Town Treasurer", "Fairlee Town Treasurer", 1,
               [frl_sb25("the March 10, 2025 Selectboard minutes "
                         "handle the Treasurer inside the annual "
                         "Appointment Slate ('Jess Chase will be "
                         "working on the signatories tomorrow. As of "
                         "now, Lisa Hinsley is still the official "
                         "Fairlee Town Treasurer'), so the office is "
                         "filled by appointment and Jessica Chase is "
                         "recorded as the appointed holder. She is "
                         "minted as a person distinct from Bradford's "
                         "appointed Treasurer Jessica Chase: the "
                         "shared name and office in adjacent towns "
                         "do not by themselves prove identity."),
                frl_aud("the December 19, 2024 auditors' minutes "
                        "already style Jessica Chase as Treasurer, "
                        "and she presented as Treasurer at the March "
                        "3, 2026 town meeting."),
                guide("lists Lisa Hinsley as Town Treasurer of "
                      "Fairlee (January 2026), superseded by the "
                      "town's own records above.")],
               [holder("Jessica Chase", "jessica-chase",
                       how_seated="appointed")]),
        office("lister", "Lister", "Fairlee Listers", 3,
               [frl26("the March 3, 2026 meeting elected Russ Collins "
                      "Lister for a 3-year term, unopposed; the "
                      "other two seats are unnamed in the sources "
                      "read, so one is minted.")],
               [holder("Russ Collins", "russ-collins")]),
        office("auditor", "Auditor", "Fairlee Auditors", 3,
               [frl26("the March 3, 2026 meeting elected Jane "
                      "Chambers Auditor for a 1-year term; the 2-year "
                      "auditor seat drew no nominations and was "
                      "passed over, leaving it vacant, and the third "
                      "seat is unnamed in the sources read."),
                frl_aud("the auditors' minutes are signed by Jane "
                        "Wilson Chambers, her fuller form of name.")],
               [holder("Jane Chambers", "jane-chambers")]),
        office("budget-committee", "Budget Committee Member",
               "Fairlee Budget Committee", 3,
               [frl26("the town meeting elects one Budget Committee "
                      "member yearly to a 3-year term (three seats); "
                      "Keri Gelenian was elected March 3, 2026. The "
                      "other two seats are unnamed in the sources "
                      "read.")],
               [holder("Keri Gelenian", "keri-gelenian")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Fairlee Cemetery Commission", 5,
               [frl26("the town meeting elects one Cemetery "
                      "Commissioner yearly to a 5-year term (five "
                      "seats); Chaz Hinsley was elected March 3, "
                      "2026. The other four seats are unnamed in the "
                      "sources read.")],
               [holder("Chaz Hinsley", "chaz-hinsley")]),
        office("library-trustee", "Library Trustee",
               "Fairlee Library Trustees", 5,
               [frl26("the town meeting elects Library Trustees to "
                      "5-year terms (five seats); Charlotte Williams "
                      "was elected March 3, 2026. The other four "
                      "seats are unnamed in the sources read.")],
               [holder("Charlotte Williams", "charlotte-williams")]),
        office("first-constable", "First Constable",
               "Fairlee First Constable", 1,
               [frl_sb25("the March 10, 2025 Appointment Slate names "
                         "Dan Ludwig as appointed First Constable "
                         "for the ensuing year, so the office is "
                         "appointive in Fairlee; no 2026 slate "
                         "outcome was read, so the seat is left "
                         "unfilled. Structure only.")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Fairlee Collector of Delinquent Taxes", 1,
               [frl_sb25("the office of Collector of Delinquent Taxes "
                         "sits on the Selectboard's annual "
                         "Appointment Slate; the holder is unnamed "
                         "in the sources read, so the seat is left "
                         "unfilled. Structure only.")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Fairlee Justices of the Peace", 5,
               [jp_src("lists five Fairlee justices of the peace: "
                       "Peter Berger, Eric Brooks, Rita Temple "
                       "Brooks, Calista Diane, and Timothy Danen.")],
               [holder("Peter Berger", "peter-berger"),
                holder("Eric Brooks", "eric-brooks"),
                holder("Rita Temple Brooks", "rita-temple-brooks"),
                holder("Calista Diane", "calista-diane"),
                holder("Timothy Danen", "timothy-danen")]),
    ]
    jp = jp_election(
        "fairlee-vt", label, 5,
        "lists five Fairlee justices of the peace elected "
        "November 5, 2024: Peter Berger, Eric Brooks, Rita Temple "
        "Brooks, Calista Diane, and Timothy Danen. The listing "
        "publishes no vote totals or party labels and none are "
        "recorded.")
    return spec("fairlee", label, offices, jp)


SPECS.append(fairlee_spec())

# ---------------------------------------------------------------- emit
for s in SPECS:
    path = OUT / f"{s['place_slug']}.json"
    path.write_text(json.dumps(s, indent=2) + "\n")
    print(f"wrote {path.name}: {len(s['offices'])} offices")
print(f"{len(SPECS)} specs")
