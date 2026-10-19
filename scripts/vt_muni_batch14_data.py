#!/usr/bin/env python3
"""Batch 14 of the VT #163 municipal fan-out (alphabetical positions
130-139): Maidstone, Manchester (town), Manchester Village,
Marlboro, Marshfield (town), Marshfield Village, Mendon,
Middlebury, Middlesex, Middletown Springs. Emits one JSON spec
per municipality for build_vt_municipality.py. Marshfield
Village is HELD (no spec emitted): it has no website and no
published roster; the only roster is a factory clerk-email lead.
Research: vt_muni_batch14_research.md.

Identity calls baked into this batch (all flagged on #163):
- Maidstone HAS an official site (maidstone-vt.org) despite the
  workbook's "Needs Research"; its Town Officials Chart (Apr 20,
  2026) and certified March 3, 2026 results govern. Its
  moderator and constable are minted elected on roster
  concurrence over unnamed write-in pluralities, and JP winner
  Bruce Hobaugh is NOT minted (the town's current chart shows
  the seat vacant) -- the Enosburgh Gervais treatment, with the
  story in the election note.
- Manchester (town): the town's own Selectboard page seats
  Jackie Wilson, not the June 2026 SOS directory's Cynthia
  Kilburn (directory stale; Franklin/Highgate class). Its
  Trustee of Public Funds, Douglas Kilburn, was elected at the
  June 2, 2026 special election on the town-posted tally (the
  town labeled its own post "UNOFFICIAL ELECTION NIGHT
  RESULTS" -- disclosed). Its treasurer and constable are
  Selectboard appointees (June 9, 2026 agenda).
- Manchester Village: the July 2026 annual-meeting minutes and
  the trustees' July 13, 2026 minutes govern; the clerk and
  the treasurer/tax collector are appointed under the
  voter-authorized articles (17 V.S.A. ch. 55); its auditors
  moved to staggered 3-year terms in 2025.
- Mendon's clerk, treasurer, and constable are all appointed
  (the 2025 town report's own Appointed table).
- Middlebury's auditors were eliminated by prior town vote
  (no post); its treasurer is Selectboard-appointed (ch. 127
  sec. 305). The town's 2026 town meeting minutes/results
  documents were unreachable (the town site failed on every
  path, 2026-10-18), so the lister seat Gary Baker held and
  the Ilsley seat Claire Tebbs held, which stood in 2026, are
  left unfilled and the moderator structure-only -- stragglers,
  disclosed. Middlebury JP Dave Silberman IS Addison County's
  High Bailiff: the JP membership reuses the county person
  record and the JP candidacy is appended by hand.
- Middlesex's clerk is Brigid Browning (June 2026 spreadsheet
  and the town page over the Guide's Grandfield); its auditors
  are eliminated (outside CPA). Marshfield (town) rests on the
  Hardwick Gazette's account of the town's draft minutes
  (disclosed class); its Budget Committee is 5 seats DERIVED.
  Middletown Springs: Neil Russell was appointed to the
  Selectboard Sept. 10, 2026 (Carl Haynes departed); DTC
  Heather Grier is minted appointed on the FY2024 report's own
  footnote. Marshfield's Amy Monahan is a NEW person, distinct
  from Cabot's treasurer Amy Monahan.
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
CHARTER_127 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/127",
    "note": "PLACEHOLDER",
}
CHARTER_239 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/239",
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


def charter127(phrase):
    return S(CHARTER_127, f"24 App. V.S.A. ch. 127 (Town of "
             f"Middlebury): {phrase}")


def charter239(phrase):
    return S(CHARTER_239, f"24 App. V.S.A. ch. 239 (Village of "
             f"Manchester): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 14); issue #163 "
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
                  f"# municipal fan-out batch 14; issue #163 "
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
ORDER = ["maidstone", "manchester-42850", "manchester", "marlboro",
         "marshfield-43600", "mendon", "middlebury", "middlesex",
         "middletown-springs"]

# ------------------------------------------------------------ Maidstone
MAID_CHART = {
    "url": "https://maidstone-vt.org/wp-content/uploads/Town-Officials-Chart-current.pdf",
    "note": "PLACEHOLDER",
}
MAID_RESULTS = {
    "url": "https://maidstone-vt.org/wp-content/uploads/official-Annual-Town-Meeting-_2026.pdf",
    "note": "PLACEHOLDER",
}
MAID_LISTERS = {
    "url": "https://maidstone-vt.org/boards/board-of-listers/",
    "note": "PLACEHOLDER",
}


def maid_chart(what):
    return S(MAID_CHART, "Town of Maidstone (official website), "
             f"Town Officials Chart (updated April 20, 2026): {what}")


def maid_results(what):
    return S(MAID_RESULTS, "Town of Maidstone (official website), "
             f"official results of the March 3, 2026 annual town "
             f"meeting: {what}")


def maid_listers(what):
    return S(MAID_LISTERS, "Town of Maidstone (official website), "
             f"Board of Listers page: {what}")


def maidstone_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Maidstone Selectboard", 3,
               [sb_dir("lists Maidstone's three selectboard members "
                       "as Scott Lovell, Bruno McKenzie (Chair), and "
                       "Brad McVetty"),
                maid_chart("marks Bruno McKenzie (Chair), Brad "
                           "McVetty, and Scott Lovell as the "
                           "Selectboard"),
                maid_results("Scott Lovell was re-elected in 2026, "
                             "73 votes to 24 for Laurie Snowman")],
               [holder("Bruno McKenzie", "bruno-mckenzie"),
                holder("Brad McVetty", "brad-mcvetty"),
                holder("Scott Lovell", "scott-lovell")]),
        office("town-clerk", "Town Clerk",
               "Maidstone Town Clerk", 1,
               [maid_chart("marks Amy Pear Town Clerk, 'E 2026' "
                           "(elected 2026)"),
                clerk_xlsx("lists Amy Pear as Maidstone's town clerk"),
                guide("names Amy Pear as Maidstone's town clerk")],
               [holder("Amy Pear", "amy-pear")]),
        office("town-treasurer", "Town Treasurer",
               "Maidstone Town Treasurer", 1,
               [maid_chart("marks Robert 'Bob' Champagne-Willis "
                           "Town Treasurer, 'E 2024' (elected 2024 "
                           "to a term ending 2027); the recorded "
                           "name is the certified form Robert"),
                treas_xlsx("lists Robert Champagne-Willis as "
                           "Maidstone's town treasurer")],
               [holder("Robert Champagne-Willis",
                       "robert-champagne-willis")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Maidstone Collector of Delinquent Taxes", 1,
               [maid_chart("marks Robert Champagne-Willis Collector "
                           "of Delinquent Taxes, 'E 2026'"),
                maid_results("Robert Champagne-Willis was elected "
                             "Collector of Delinquent Taxes in 2026 "
                             "with 84 votes")],
               [holder("Robert Champagne-Willis",
                       "robert-champagne-willis")]),
        office("lister", "Lister",
               "Maidstone Board of Listers", 3,
               [maid_chart("marks the three listers Robert "
                           "Champagne-Willis ('E 2025'), Sam Graham "
                           "('E 2024'), and Sandy Gray ('E 2026')"),
                maid_listers("names the Board of Listers as Robert "
                             "Champagne-Willis, Sam Graham, and "
                             "Sandy Gray"),
                maid_results("Sandy Gray was elected lister in "
                             "2026 with 81 votes")],
               [holder("Robert Champagne-Willis",
                       "robert-champagne-willis"),
                holder("Sam Graham", "sam-graham"),
                holder("Sandy Gray", "sandy-gray")]),
        office("constable", "Constable",
               "Maidstone Constable", 1,
               [maid_chart("marks Raymond Lovell Constable, "
                           "'E 2026' (elected 2026) -- the town's "
                           "current roster seats him"),
                maid_results("the 2026 tally prints 'Ray Lovell' "
                             "with 16 named votes against 24 "
                             "unnamed write-ins; the plurality "
                             "write-ins are unnamed, and the "
                             "officials chart's concurrence seats "
                             "him (write-in rule)")],
               [holder("Raymond Lovell", "raymond-lovell")]),
        office("moderator", "Moderator",
               "Maidstone Moderator", 1,
               [maid_chart("marks Robert Champagne-Willis "
                           "Moderator, 'E 2026' (elected 2026) -- "
                           "the town's current roster seats him"),
                maid_results("the 2026 tally shows 36 unnamed "
                             "write-in votes against 14 named "
                             "votes for Robert Champagne-Willis; "
                             "the write-ins are unnamed, and the "
                             "officials chart's concurrence seats "
                             "him (write-in rule)")],
               [holder("Robert Champagne-Willis",
                       "robert-champagne-willis")]),
        office("auditor", "Auditor",
               "Maidstone Auditors", 3,
               [maid_chart("marks the three auditors Donna Brisbin "
                           "('E 2024'), Jack Donnelly ('E 2026'), "
                           "and Sandy Gray ('E 2025')"),
                maid_results("the 2026 auditor tally scattered "
                             "across candidates; the town's "
                             "officials chart is the roster of "
                             "record and marks Donnelly elected "
                             "2026")],
               [holder("Donna Brisbin", "donna-brisbin"),
                holder("Jack Donnelly", "jack-donnelly"),
                holder("Sandy Gray", "sandy-gray")]),
        office("town-agent", "Town Agent",
               "Maidstone Town Agent", 1,
               [maid_chart("marks Jim Mazzonna Town Agent, "
                           "'A 2026' (appointed 2026)")],
               [holder("Jim Mazzonna", "jim-mazzonna",
                       how_seated="appointed")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Maidstone Justices of the Peace", 5,
               [jp_src("lists five Maidstone justices of the "
                       "peace elected November 5, 2024: Andre A. "
                       "Champagne-Willis, Bruce Hobaugh, Cheryl "
                       "McVetty, Heather Monahan, and Laurie-Anne "
                       "Snowman"),
                maid_chart("lists four sitting justices of the "
                           "peace (Champagne-Willis, McVetty, "
                           "Monahan, Snowman) and one justice "
                           "seat VACANT; Bruce Hobaugh is not "
                           "named, so he is not minted (see the "
                           "election note)")],
               [holder("Andre A. Champagne-Willis",
                       "andre-champagne-willis"),
                holder("Cheryl McVetty", "cheryl-mcvetty"),
                holder("Heather Monahan", "heather-monahan"),
                holder("Laurie-Anne Snowman",
                       "laurie-anne-snowman")]),
    ]
    jp = jp_election(
        "maidstone-vt", "Town of Maidstone", 5,
        "lists five Maidstone justices of the peace elected "
        "November 5, 2024: Andre A. Champagne-Willis, Bruce "
        "Hobaugh, Cheryl McVetty, Heather Monahan, and "
        "Laurie-Anne Snowman. The listing publishes no vote "
        "totals or party labels and none are recorded. Bruce "
        "Hobaugh is not minted: the Town of Maidstone's Town "
        "Officials Chart (updated April 20, 2026) lists only "
        "four sitting justices and one vacant seat and does not "
        "name him, so no person or membership is created for "
        "him and the four verified winners are recorded here",
        [maid_chart("lists one justice of the peace seat VACANT "
                    "and does not name Bruce Hobaugh")])
    return spec("maidstone", "Town of Maidstone", offices, jp)


SPECS["maidstone"] = maidstone_spec()

# ------------------------------------------------------- Manchester (town)
MANCH_SB = {
    "url": "https://www.manchester-vt.gov/selectboard",
    "note": "PLACEHOLDER",
}
MANCH_BOARDS = {
    "url": "https://www.manchester-vt.gov/boards",
    "note": "PLACEHOLDER",
}
MANCH_ELEC = {
    "url": "https://www.manchester-vt.gov/elections",
    "note": "PLACEHOLDER",
}
MANCH_2022 = {
    "url": "https://manchester-vt.gov/vertical/sites/%7BCE718C6D-0EC0-43CE-B71E-5A023B5D13EA%7D/uploads/2022_Town_Meeting_Elections_Spreadsheet_-_Sheet1.pdf",
    "note": "PLACEHOLDER",
}


def manch_sb(what):
    return S(MANCH_SB, "Town of Manchester (official website), "
             f"Selectboard page: {what}")


def manch_boards(what):
    return S(MANCH_BOARDS, "Town of Manchester (official website), "
             f"Boards page: {what}")


def manch_elec(what):
    return S(MANCH_ELEC, "Town of Manchester (official website), "
             f"Elections page: {what}")


def manch_2022(what):
    return S(MANCH_2022, "Town of Manchester, 2022 Town Meeting "
             f"Elections spreadsheet (certified): {what}")


def manchester_town_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Manchester Selectboard", 5,
               [manch_sb("'Current Selectboard Members are: Ivan "
                         "Beattie (Chair), Heidi Chamberlain "
                         "(Vice Chair), Jonathan West (Clerk), "
                         "Laurie Kunz, Jackie Wilson' -- the "
                         "town's own page governs"),
                sb_dir("lists Manchester's selectboard as Ivan "
                       "Beattie, Heidi Chamberlain, Cynthia "
                       "Kilburn, Laurie Kunz, and Jonathan West; "
                       "the directory is stale on the fifth seat "
                       "-- the town page seats Jackie Wilson, "
                       "elected June 2, 2026, and Kilburn no "
                       "longer sits"),
                manch_elec("the town-posted tally of the June 2, "
                           "2026 special election: Jackie Wilson "
                           "288, Rebecca Nawrath 200, Karen "
                           "Dillon 84, Katie Stannard 78")],
               [holder("Ivan Beattie", "ivan-beattie"),
                holder("Heidi Chamberlain", "heidi-chamberlain"),
                holder("Jonathan West", "jonathan-west"),
                holder("Laurie Kunz", "laurie-kunz"),
                holder("Jackie Wilson", "jackie-wilson")]),
        office("town-clerk", "Town Clerk",
               "Manchester Town Clerk", 1,
               [guide("names Anita Sheldon as Manchester's town "
                      "clerk"),
                clerk_xlsx("lists Anita Sheldon as Manchester's "
                           "town clerk"),
                manch_boards("the town's Board of Civil Authority "
                             "listing styles Anita Sheldon Town "
                             "Clerk; she is elected -- the "
                             "Selectboard's June 9, 2026 agenda "
                             "re-appointed only the Treasurer "
                             "and the Constable")],
               [holder("Anita Sheldon", "anita-sheldon")]),
        office("town-treasurer", "Town Treasurer",
               "Manchester Town Treasurer", 1,
               [manch_sb("the Selectboard's June 9, 2026 agenda, "
                         "item 8, 'Possibly Re-Appoint Patrick "
                         "Owens as Town Constable and Brian Vogel "
                         "as Town Treasurer' -- the treasurer is "
                         "a Selectboard appointee"),
                treas_xlsx("lists Brian Vogel as Manchester's "
                           "town treasurer (name concordant; "
                           "mode is appointed per the agenda)")],
               [holder("Brian Vogel", "brian-vogel",
                       how_seated="appointed")]),
        office("constable", "Town Constable",
               "Manchester Town Constable", 1,
               [manch_sb("the Selectboard's June 9, 2026 agenda, "
                         "item 8, 'Possibly Re-Appoint Patrick "
                         "Owens as Town Constable and Brian Vogel "
                         "as Town Treasurer' -- the constable is "
                         "a Selectboard appointee")],
               [holder("Patrick Owens", "patrick-owens",
                       how_seated="appointed")]),
        office("trustee-of-public-funds",
               "Trustee of Public Funds",
               "Manchester Trustees of Public Funds", 1,
               [manch_elec("the town-posted tally of the June 2, "
                           "2026 special election: Douglas "
                           "Kilburn 572, write-ins 9, for Trustee "
                           "of Public Funds. The town labeled its "
                           "post 'UNOFFICIAL ELECTION NIGHT "
                           "RESULTS'; the Selectboard seated the "
                           "same election's selectboard winner on "
                           "June 9, corroborating effect. The "
                           "prior holder was Sarah McClintock"),
                manch_2022("the 2022 Article 25 ballot elected "
                           "a Trustee of Public Funds, "
                           "establishing the office as elective "
                           "with one seat")],
               [holder("Douglas Kilburn", "douglas-kilburn")]),
        office("moderator", "Moderator",
               "Manchester Moderator", 1,
               [statute2646_structure("elected town moderator, "
                                      "one-year term"),
                manch_2022("W. Michael Nawrath was elected "
                           "Moderator in 2022 (813 votes) and "
                           "held the office in 2024; the outcome "
                           "of the February 28, 2026 floor "
                           "meeting is published nowhere "
                           "reachable, so no holder is minted")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Manchester Justices of the Peace", 12,
               [jp_src("lists twelve Manchester justices of the "
                       "peace elected November 5, 2024")],
               [holder("Martha Heilemann", "martha-heilemann"),
                holder("Alison Hill", "alison-hill"),
                holder("Cynthia Kilburn", "cynthia-kilburn"),
                holder("Frank Kropa", "frank-kropa"),
                holder("Laurie Kunz", "laurie-kunz",
                       ballot_name="Laurie A. Kunz"),
                holder("Richard Long", "richard-long",
                       ballot_name="Richard M. Long"),
                holder("Charles Murphy", "charles-murphy",
                       ballot_name='Charles "Chic" Murphy'),
                holder("Rebecca Nawrath", "rebecca-nawrath",
                       ballot_name='Rebecca "Becky" Nawrath'),
                holder("Barbara Powers", "barbara-powers"),
                holder("Timothy Rhys", "timothy-rhys",
                       ballot_name="Timothy E. Rhys"),
                holder("Anita Sheldon", "anita-sheldon",
                       ballot_name="Anita L. Sheldon"),
                holder("Thomas West", "thomas-west")]),
    ]
    jp = jp_election(
        "manchester-42850-vt", "Town of Manchester", 12,
        "lists twelve Manchester justices of the peace elected "
        "November 5, 2024: Martha Heilemann, Alison Hill, "
        "Cynthia Kilburn, Frank Kropa, Laurie A. Kunz, Richard "
        "M. Long, Charles 'Chic' Murphy, Rebecca 'Becky' "
        "Nawrath, Barbara Powers, Timothy E. Rhys, Anita L. "
        "Sheldon, and Thomas West. The listing publishes no "
        "vote totals or party labels and none are recorded")
    return spec("manchester-42850", "Town of Manchester",
                offices, jp)


SPECS["manchester-42850"] = manchester_town_spec()

# ---------------------------------------------------- Manchester Village
MANCHV_ANNUAL = {
    "url": "https://www.villageofmanchester.com/wp-content/uploads/2026/07/2026_07_13-Board-of-Trustees-Annual-Minutes.pdf",
    "note": "PLACEHOLDER",
}
MANCHV_BOT = {
    "url": "https://www.villageofmanchester.com/wp-content/uploads/2026/08/2026_07_13-Board-of-Trustees-Minutes.pdf",
    "note": "PLACEHOLDER",
}
MANCHV_REPORT = {
    "url": "https://www.villageofmanchester.com/wp-content/uploads/2026/07/000.-2026-Annual-Report.pdf",
    "note": "PLACEHOLDER",
}


def manchv_annual(what):
    return S(MANCHV_ANNUAL, "Village of Manchester, minutes of "
             f"the July 2026 annual meeting: {what}")


def manchv_bot(what):
    return S(MANCHV_BOT, "Village of Manchester, minutes of the "
             f"Board of Trustees meeting of July 13, 2026: {what}")


def manchv_report(what):
    return S(MANCHV_REPORT, "Village of Manchester, 2026 Annual "
             f"Report: {what}")


def manchester_village_spec():
    offices = [
        office("village-president", "Village President",
               "Village of Manchester Board of Trustees", 1,
               [charter239("section 6: the village elects a "
                           "President at the annual meeting for "
                           "a one-year term; the President is ex "
                           "officio one of the trustees and "
                           "President of the Board"),
                manchv_annual("Article 5: Tom Deck was "
                              "re-elected President at the July "
                              "2026 annual meeting")],
               [holder("Tom Deck", "tom-deck")]),
        office("village-trustee", "Village Trustee",
               "Village of Manchester Board of Trustees", 4,
               [charter239("section 6: two trustees are elected "
                           "each year for two-year terms, so the "
                           "elected trustees number four (the "
                           "President sits ex officio as a "
                           "fifth)"),
                manchv_annual("Article 5: Jim Lewis and Anthony "
                              "MacLaurin were re-elected "
                              "trustees at the July 2026 annual "
                              "meeting (Lewis 10-1, MacLaurin "
                              "unanimous)"),
                manchv_report("the officers list seats Nina "
                              "Mooney and Scott Swinarton as "
                              "trustees to 2027")],
               [holder("Jim Lewis", "jim-lewis"),
                holder("Anthony MacLaurin", "anthony-maclaurin"),
                holder("Nina Mooney", "nina-mooney"),
                holder("Scott Swinarton", "scott-swinarton")]),
        office("village-auditor", "Village Auditor",
               "Village of Manchester Auditors", 3,
               [charter239("section 6: the village elects three "
                           "auditors at the annual meeting"),
                manchv_annual("the meeting's correction for the "
                              "record states the village adopted "
                              "staggered three-year auditor terms "
                              "in 2025 (Keld Alstrup three-year, "
                              "Ariel Rudiakov two-year, Amy "
                              "Swinarton one-year) and Amy "
                              "Swinarton was re-elected in 2026 "
                              "to the three-year seat"),
                manchv_report("the officers list names the "
                              "three auditors Keld Alstrup, Ariel "
                              "Rudiakov, and Amy Swinarton")],
               [holder("Keld Alstrup", "keld-alstrup"),
                holder("Ariel Rudiakov", "ariel-rudiakov"),
                holder("Amy Swinarton", "amy-swinarton")]),
        office("village-clerk", "Village Clerk",
               "Village of Manchester Clerk", 1,
               [charter239("section 6: the village elects a "
                           "Clerk at the annual meeting; the "
                           "voters have authorized the trustees "
                           "to appoint the clerk instead"),
                manchv_annual("Articles 6 and 7, passed in 2025 "
                              "and again in 2026, authorize the "
                              "Trustees to appoint the Clerk and "
                              "the Treasurer/Tax Collector under "
                              "17 V.S.A. chapter 55"),
                manchv_bot("motion carried: 'To appoint Donald "
                           "Brodie as Village Clerk'")],
               [holder("Donald Brodie", "donald-brodie",
                       how_seated="appointed")]),
        office("village-treasurer", "Village Treasurer",
               "Village of Manchester Treasurer", 1,
               [charter239("section 6: the village elects a "
                           "Treasurer at the annual meeting; "
                           "the voters have authorized the "
                           "trustees to appoint the treasurer "
                           "instead"),
                manchv_annual("Articles 6 and 7, passed in 2025 "
                              "and again in 2026, authorize the "
                              "Trustees to appoint the Clerk and "
                              "the Treasurer/Tax Collector under "
                              "17 V.S.A. chapter 55"),
                manchv_bot("motion carried: 'To appoint Sarah "
                           "McClintock as Treasurer and Tax "
                           "Collector'")],
               [holder("Sarah McClintock", "sarah-mcclintock",
                       how_seated="appointed")]),
        office("tax-collector", "Tax Collector",
               "Village of Manchester Tax Collector", 1,
               [charter239("section 6: the village elects a Tax "
                           "Collector at the annual meeting; "
                           "the voters have authorized the "
                           "trustees to appoint the collector "
                           "instead"),
                manchv_bot("motion carried: 'To appoint Sarah "
                           "McClintock as Treasurer and Tax "
                           "Collector'")],
               [holder("Sarah McClintock", "sarah-mcclintock",
                       how_seated="appointed")]),
    ]
    return spec("manchester", "Village of Manchester", offices)


SPECS["manchester"] = manchester_village_spec()

# ------------------------------------------------------------ Marlboro
MARL_RETURN = {
    "url": "https://marlborovt.us/wp-content/uploads/2026/03/Official-Return-of-Votes-3.3.2026-Town-School-Election.pdf",
    "note": "PLACEHOLDER",
}
MARL_RESULTS = {
    "url": "https://marlborovt.us/wp-content/uploads/2026/01/RESULTS-2026-Town-Meeting-Ballot.pdf",
    "note": "PLACEHOLDER",
}
MARL_REPORT = {
    "url": "https://marlborovt.us/wp-content/uploads/2026/01/Marlboro_2025_Vermont-Municipal-Report.pdf",
    "note": "PLACEHOLDER",
}
MARL_DIR = {
    "url": "https://marlborovt.us/government/municipal-directory/",
    "note": "PLACEHOLDER",
}


def marl_return(what):
    return S(MARL_RETURN, "Town of Marlboro, Official Return of "
             f"Votes, March 3, 2026 town election (certified): "
             f"{what}")


def marl_results(what):
    return S(MARL_RESULTS, "Town of Marlboro, official ballot "
             f"results, March 3, 2026: {what}")


def marl_report(what):
    return S(MARL_REPORT, "Town of Marlboro, 2025 Town Report: "
             f"{what}")


def marl_dir(what):
    return S(MARL_DIR, "Town of Marlboro (official website), "
             f"Municipal Directory: {what}")


def marlboro_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Marlboro Selectboard", 3,
               [sb_dir("lists Marlboro's three selectboard "
                       "members as Molly Welch (Chair), Jeffrey "
                       "Skramstad (Vice Chair), and Kate "
                       "Kirkwood"),
                marl_return("Jeff Skramstad was re-elected to "
                            "the Selectboard in 2026 with 314 "
                            "votes; town sources print 'Jeff', "
                            "and the recorded name is the "
                            "directory's full form Jeffrey"),
                marl_report("the 'Elected Officers' table seats "
                            "Molly Welch (Chair, to 2028), Jeff "
                            "Skramstad (to 2029), and Kate "
                            "Kirkwood (to 2027)")],
               [holder("Molly Welch", "molly-welch"),
                holder("Jeffrey Skramstad", "jeffrey-skramstad"),
                holder("Kate Kirkwood", "kate-kirkwood")]),
        office("town-clerk", "Town Clerk",
               "Marlboro Town Clerk", 1,
               [marl_return("Forrest Holzapfel was re-elected "
                            "Town Clerk in 2026 with 360 votes"),
                guide("names Forrest Holzapfel as Marlboro's "
                      "town clerk"),
                clerk_xlsx("lists Forrest Holzapfel as "
                           "Marlboro's town clerk")],
               [holder("Forrest Holzapfel", "forrest-holzapfel")]),
        office("town-treasurer", "Town Treasurer",
               "Marlboro Town Treasurer", 1,
               [marl_report("the 'Elected Officers' table seats "
                            "Rebecca Sevigny as Town Treasurer "
                            "(elected, term to 2028; her "
                            "three-year seat was filled in 2025 "
                            "and was not on the 2026 ballot)"),
                guide("names Rebecca Sevigny as Marlboro's town "
                      "treasurer"),
                treas_xlsx("lists Rebecca Sevigny as Marlboro's "
                           "town treasurer")],
               [holder("Rebecca Sevigny", "rebecca-sevigny")]),
        office("lister", "Lister",
               "Marlboro Board of Listers", 3,
               [marl_return("Eric Matt was re-elected lister in "
                            "2026 with 371 votes"),
                marl_report("the 'Elected Officers' table seats "
                            "the three listers Eric Matt (to "
                            "2029), Evan Wyse (Chair, to 2027), "
                            "and Forrest Holzapfel (to 2028)")],
               [holder("Eric Matt", "eric-matt"),
                holder("Evan Wyse", "evan-wyse"),
                holder("Forrest Holzapfel", "forrest-holzapfel")]),
        office("auditor", "Auditor",
               "Marlboro Auditors", 3,
               [marl_return("S. Rose Watson was re-elected "
                            "auditor in 2026 with 343 votes"),
                marl_report("the 'Elected Officers' table seats "
                            "the three auditors S. Rose Watson "
                            "(to 2029), Gail MacArthur (to "
                            "2027), and Andy Reichsman (to "
                            "2028)")],
               [holder("S. Rose Watson", "s-rose-watson"),
                holder("Gail MacArthur", "gail-macarthur"),
                holder("Andy Reichsman", "andy-reichsman")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Marlboro Cemetery Commission", 3,
               [marl_return("Sally M. White was re-elected "
                            "Cemetery Commissioner in 2026 with "
                            "354 votes"),
                marl_report("the 'Elected Officers' table seats "
                            "the three cemetery commissioners "
                            "Sally M. White (to 2029), Hollis "
                            "Burbank-Hammarlund (to 2027), and "
                            "Marcia L. Hamilton (to 2028)")],
               [holder("Sally White", "sally-white",
                       ballot_name="Sally M. White"),
                holder("Hollis Burbank-Hammarlund",
                       "hollis-burbank-hammarlund"),
                holder("Marcia Hamilton", "marcia-hamilton",
                       ballot_name="Marcia L. Hamilton")]),
        office("constable", "Constable",
               "Marlboro Constable", 1,
               [marl_report("the 'Elected Officers' table seats "
                            "Clarence Boston as Constable "
                            "(elected, term to 2027)")],
               [holder("Clarence Boston", "clarence-boston")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Marlboro Collector of Delinquent Taxes", 1,
               [marl_report("the 'Elected Officers' table seats "
                            "Evan Wyse as Collector of "
                            "Delinquent Taxes (elected, term to "
                            "2028)")],
               [holder("Evan Wyse", "evan-wyse")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Marlboro Justices of the Peace", 5,
               [jp_src("lists five Marlboro justices of the "
                       "peace elected November 5, 2024"),
                marl_report("the report's justice of the peace "
                            "block names the same five")],
               [holder("Mimi Brill", "mimi-brill"),
                holder("Marcia Hamilton", "marcia-hamilton",
                       ballot_name="Marcia L. Hamilton"),
                holder("David Holzapfel", "david-holzapfel"),
                holder("Andy Reichsman", "andy-reichsman"),
                holder("T. Hunter Wilson", "t-hunter-wilson")]),
    ]
    jp = jp_election(
        "marlboro-vt", "Town of Marlboro", 5,
        "lists five Marlboro justices of the peace elected "
        "November 5, 2024: Mimi Brill, Marcia L. Hamilton, David "
        "Holzapfel, Andy Reichsman, and T. Hunter Wilson. The "
        "listing publishes no vote totals or party labels and "
        "none are recorded",
        [marl_report("the report's justice of the peace block "
                     "names the same five")])
    return spec("marlboro", "Town of Marlboro", offices, jp)


SPECS["marlboro"] = marlboro_spec()

# ------------------------------------------------------ Marshfield (town)
MARSH_SB = {
    "url": "https://marshfieldvt.gov/selectboard",
    "note": "PLACEHOLDER",
}
GAZETTE_MARSH = {
    "url": "https://hardwickgazette.org/2026/03/24/everything-passes-at-marshfield-town-meeting/",
    "note": "PLACEHOLDER",
}


def marsh_sb(what):
    return S(MARSH_SB, "Town of Marshfield (official website), "
             f"Selectboard page: {what}")


def gazette_marsh(what):
    return S(GAZETTE_MARSH, "Hardwick Gazette, 'Everything Passes "
             f"at Marshfield Town Meeting' (March 24, 2026), "
             f"reporting the town's draft annual-meeting minutes "
             f"officer by officer: {what}")


def marshfield_town_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Marshfield Selectboard", 3,
               [marsh_sb("lists the Selectboard as Richard Baker "
                         "(Chair), Christopher Whalen, and Luke "
                         "Lampugnale; the Secretary of State's "
                         "directory publishes no Marshfield "
                         "roster"),
                gazette_marsh("Luke Lampugnale was re-elected "
                              "to the Selectboard in 2026 "
                              "(three-year term); Justin Campbell "
                              "retired")],
               [holder("Richard Baker", "richard-baker"),
                holder("Christopher Whalen", "christopher-whalen"),
                holder("Luke Lampugnale", "luke-lampugnale")]),
        office("town-clerk", "Town Clerk",
               "Marshfield Town Clerk", 1,
               [gazette_marsh("Bobbi Brimblecombe was elected "
                              "Town Clerk at the March 1, 2026 "
                              "annual meeting (one-year term)"),
                guide("names Bobbi Brimblecombe as Marshfield's "
                      "town clerk"),
                clerk_xlsx("lists Bobbi Brimblecombe as "
                           "Marshfield's town clerk")],
               [holder("Bobbi Brimblecombe",
                       "bobbi-brimblecombe")]),
        office("town-treasurer", "Town Treasurer",
               "Marshfield Town Treasurer", 1,
               [gazette_marsh("Bobbi Brimblecombe was elected "
                              "Town Treasurer at the March 1, "
                              "2026 annual meeting (one-year "
                              "term)"),
                guide("names Bobbi Brimblecombe as Marshfield's "
                      "town treasurer (the treasurer contact "
                      "spreadsheet carries no Marshfield entry)")],
               [holder("Bobbi Brimblecombe",
                       "bobbi-brimblecombe")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Marshfield Collector of Delinquent Taxes", 1,
               [gazette_marsh("Bobbi Brimblecombe was elected "
                              "Collector of Delinquent Taxes at "
                              "the March 1, 2026 annual meeting "
                              "(one-year term)")],
               [holder("Bobbi Brimblecombe",
                       "bobbi-brimblecombe")]),
        office("moderator", "Moderator",
               "Marshfield Moderator", 1,
               [gazette_marsh("Michael Caccavo was elected "
                              "Moderator at the March 1, 2026 "
                              "annual meeting (one-year term)")],
               [holder("Michael Caccavo", "michael-caccavo")]),
        office("auditor", "Auditor",
               "Marshfield Auditors", 3,
               [gazette_marsh("Marie Maclay was elected auditor "
                              "in 2026 (three-year term; the "
                              "Gazette prints 'Marie Marclay' -- "
                              "the certified justice of the peace "
                              "listing's 'Marie Maclay' is the "
                              "canonical form). The holders of "
                              "the other two auditor seats are "
                              "published nowhere reachable, so "
                              "they are left unfilled")],
               [holder("Marie Maclay", "marie-maclay")]),
        office("lister", "Lister",
               "Marshfield Board of Listers", 3,
               [gazette_marsh("Kathleen Hayes was elected "
                              "lister in 2026 (three-year term); "
                              "a second lister seat (two-year "
                              "remainder) drew no nominations "
                              "and stands vacant for Selectboard "
                              "appointment, so it is left "
                              "unfilled. The Gazette's "
                              "Selectboard-meeting reporting names "
                              "'Listers Meg Eberhardt and "
                              "Kathleen Hayes' as the sitting "
                              "board; Eberhardt's full name is "
                              "Margaret, per the justice of the "
                              "peace listing")],
               [holder("Kathleen Hayes", "kathleen-hayes"),
                holder("Margaret Eberhardt",
                       "margaret-eberhardt")]),
        office("constable", "Constable",
               "Marshfield Constable", 1,
               [gazette_marsh("Shawn Codling was elected "
                              "Constable at the March 1, 2026 "
                              "annual meeting (one-year term)")],
               [holder("Shawn Codling", "shawn-codling")]),
        office("budget-committee", "Budget Committee Member",
               "Marshfield Budget Committee", 5,
               [gazette_marsh("Betsy Brigham (five-year term), "
                              "Amy Monahan (four-year "
                              "remainder), and Beth Stern "
                              "(two-year remainder) were elected "
                              "to the Budget Committee in 2026. "
                              "The committee's size is DERIVED: "
                              "one seat is elected each year to "
                              "a five-year term, so the board "
                              "numbers five; the 2026 meeting "
                              "filled the regular five-year seat "
                              "plus two vacancy remainders. Two "
                              "seats' holders are unpublished "
                              "and left unfilled. Marshfield's "
                              "Amy Monahan is a different person "
                              "from Cabot's town treasurer Amy "
                              "Monahan")],
               [holder("Betsy Brigham", "betsy-brigham"),
                holder("Amy Monahan", "amy-monahan"),
                holder("Beth Stern", "beth-stern")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Marshfield Justices of the Peace", 7,
               [jp_src("lists seven Marshfield justices of the "
                       "peace elected November 5, 2024")],
               [holder("James Arisman", "james-arisman"),
                holder("Margaret Eberhardt",
                       "margaret-eberhardt"),
                holder("Ellen Halperin", "ellen-halperin"),
                holder("Judy Henkin", "judy-henkin"),
                holder("Mary Leahy", "mary-leahy"),
                holder("Marie Maclay", "marie-maclay"),
                holder("Michael Sabourin", "michael-sabourin")]),
    ]
    jp = jp_election(
        "marshfield-43600-vt", "Town of Marshfield", 7,
        "lists seven Marshfield justices of the peace elected "
        "November 5, 2024: James Arisman, Margaret Eberhardt, "
        "Ellen Halperin, Judy Henkin, Mary Leahy, Marie Maclay, "
        "and Michael Sabourin. The listing publishes no vote "
        "totals or party labels and none are recorded")
    return spec("marshfield-43600", "Town of Marshfield",
                offices, jp)


SPECS["marshfield-43600"] = marshfield_town_spec()

# ------------------------------------------------------------ Mendon
MENDON_REPORT = {
    "url": "https://www.mendonvt.gov/DocumentCenter/View/201/2025-Mendon-Town-Report-PDF",
    "note": "PLACEHOLDER",
}
MENDON_SB = {
    "url": "https://www.mendonvt.gov/209/Selectboard",
    "note": "PLACEHOLDER",
}
MENDON_DIR = {
    "url": "https://www.mendonvt.gov/directory.aspx",
    "note": "PLACEHOLDER",
}


def mendon_report(what):
    return S(MENDON_REPORT, "Town of Mendon, 2025 Town Report: "
             f"{what}")


def mendon_sb(what):
    return S(MENDON_SB, "Town of Mendon (official website), "
             f"Selectboard page: {what}")


def mendon_dir(what):
    return S(MENDON_DIR, "Town of Mendon (official website), "
             f"directory: {what}")


def mendon_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Mendon Selectboard", 3,
               [sb_dir("lists Mendon's three selectboard members "
                       "as Megan Smith (Chair), Seth Bridge, and "
                       "Sarah Buxton"),
                mendon_report("the 'Elected Town Officers' table "
                              "seats Megan Smith (Chair, to "
                              "2028), Sarah Buxton (to 2027), and "
                              "Seth Bridge (to 2029)"),
                mendon_sb("the town's current Selectboard page "
                          "seats Seth Bridge as Vice Chair; his "
                          "three-year seat was the one on the "
                          "2026 ballot, where he was the sole "
                          "printed candidate")],
               [holder("Megan Smith", "megan-smith"),
                holder("Seth Bridge", "seth-bridge"),
                holder("Sarah Buxton", "sarah-buxton")]),
        office("moderator", "Moderator",
               "Mendon Moderator", 1,
               [statute2646_structure("elected town moderator, "
                                      "one-year term"),
                mendon_report("Christopher Corsones held the "
                              "moderator's office in 2025 and "
                              "was the sole printed candidate on "
                              "the March 3, 2026 ballot, but no "
                              "post-meeting source reachable "
                              "seats him after March 2026, so he "
                              "is not minted")]),
        office("town-clerk", "Town Clerk",
               "Mendon Town Clerk", 1,
               [mendon_report("the 'Appointed Town Officers' "
                              "table lists the Town Clerk as an "
                              "appointed office (three-year "
                              "appointed term) held by Jesse "
                              "Bridge; Mendon has adopted an "
                              "appointed clerk under 17 V.S.A. "
                              "section 2651e, and the 2026 "
                              "warning elects no clerk"),
                mendon_dir("the town's current directory styles "
                           "Jesse Bridge Town Clerk"),
                clerk_xlsx("lists Jesse Bridge as Mendon's town "
                           "clerk (name concordant; mode is "
                           "appointed per the town report)")],
               [holder("Jesse Bridge", "jesse-bridge",
                       how_seated="appointed")]),
        office("town-treasurer", "Town Treasurer",
               "Mendon Town Treasurer", 1,
               [mendon_report("the 'Appointed Town Officers' "
                              "table lists the Town Treasurer "
                              "as an appointed office (three-year "
                              "appointed term) held by Jesse "
                              "Bridge; Mendon has adopted an "
                              "appointed treasurer under 17 "
                              "V.S.A. section 2651f, and the "
                              "2026 warning elects no treasurer"),
                mendon_dir("the town's current directory styles "
                           "Jesse Bridge Town Treasurer"),
                treas_xlsx("lists Jesse Bridge as Mendon's town "
                           "treasurer (name concordant; mode is "
                           "appointed per the town report)")],
               [holder("Jesse Bridge", "jesse-bridge",
                       how_seated="appointed")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Mendon Collector of Delinquent Taxes", 1,
               [mendon_report("the 'Elected Town Officers' table "
                              "seats Nancy Bridge Merrill as "
                              "Collector of Delinquent Taxes "
                              "(elected, three-year term to "
                              "2028); the 2025 ballot concurs")],
               [holder("Nancy Bridge Merrill",
                       "nancy-bridge-merrill")]),
        office("constable", "Constable",
               "Mendon Constable", 1,
               [mendon_report("the 'Appointed Town Officers' "
                              "table lists the Constable as an "
                              "appointed office held by Mark "
                              "Fiore (appointed January 2026, "
                              "succeeding Lema Carter, who "
                              "resigned January 2026)"),
                mendon_dir("styles Mark Fiore 'Mendon's "
                           "Constable/Director of Public "
                           "Safety'")],
               [holder("Mark Fiore", "mark-fiore",
                       how_seated="appointed")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Mendon Justices of the Peace", 7,
               [jp_src("lists seven Mendon justices of the peace "
                       "elected November 5, 2024"),
                mendon_report("the report's justice of the peace "
                              "block names the same seven (in "
                              "short forms: 'Betsy Reddy' for "
                              "Elizabeth Reddy and 'Al "
                              "Wakefield' for J. Alvin "
                              "Wakefield; the certified listing's "
                              "full forms are recorded)")],
               [holder("Rich Carlson", "rich-carlson"),
                holder("Susannah Loffredo", "susannah-loffredo"),
                holder("Lindsey MacCuaig", "lindsey-maccuaig"),
                holder("Elizabeth Reddy", "elizabeth-reddy"),
                holder("James Reddy", "james-reddy"),
                holder("Megan Smith", "megan-smith"),
                holder("J. Alvin Wakefield",
                       "j-alvin-wakefield")]),
    ]
    jp = jp_election(
        "mendon-vt", "Town of Mendon", 7,
        "lists seven Mendon justices of the peace elected "
        "November 5, 2024: Rich Carlson, Susannah Loffredo, "
        "Lindsey MacCuaig, Elizabeth Reddy, James Reddy, Megan "
        "Smith, and J. Alvin Wakefield. The listing publishes "
        "no vote totals or party labels and none are recorded",
        [mendon_report("the report's justice of the peace block "
                       "names the same seven")])
    return spec("mendon", "Town of Mendon", offices, jp)


SPECS["mendon"] = mendon_spec()

# ------------------------------------------------------------ Middlebury
MIDB_SB = {
    "url": "https://www.townofmiddlebury.org/government/selectboard/index.php",
    "note": "PLACEHOLDER",
}
MIDB_LISTERS = {
    "url": "https://www.townofmiddlebury.org/government/departments/assessor_and_listor/board_of_listers.php",
    "note": "PLACEHOLDER",
}
MIDB_BOARDS = {
    "url": "https://www.townofmiddlebury.org/government/boards_and_commissions/index.php",
    "note": "PLACEHOLDER",
}
ILSLEY = {
    "url": "https://www.ilsleypubliclibrary.org/about-us/board-of-trustees/",
    "note": "PLACEHOLDER",
}

MIDB_GAP = ("the town's 2026 town meeting minutes and results "
            "documents could not be retrieved (the town website "
            "failed on every path on 2026-10-18), so the outcome "
            "for the seat that stood in March 2026 is unpublished "
            "here and the seat is left unfilled as a straggler")


def midb_sb(what):
    return S(MIDB_SB, "Town of Middlebury (official website), "
             f"Selectboard page: {what}")


def midb_listers(what):
    return S(MIDB_LISTERS, "Town of Middlebury (official "
             f"website), Board of Listers page: {what}")


def midb_boards(what):
    return S(MIDB_BOARDS, "Town of Middlebury (official website), "
             f"Boards and Commissions page: {what}")


def ilsley(what):
    return S(ILSLEY, "Ilsley Public Library (the town's public "
             f"library), Board of Trustees page: {what}")


def middlebury_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Middlebury Selectboard", 7,
               [charter127("section 302(a) elects five "
                           "selectboard members and section "
                           "302(e) permits two more by town "
                           "vote; Middlebury carries seven"),
                midb_sb("the town's Selectboard page seats "
                        "seven members: Fred Dunnington "
                        "(Chair), Isabel Gogarty (Vice Chair), "
                        "Danielle Boyce, Dan Brown, Andy "
                        "Hooper, Megan James, and Farhad Khan. "
                        "The page's Andy Hooper governs over "
                        "the Secretary of State directory's "
                        "'Timothy Hooper'"),
                sb_dir("lists seven Middlebury selectboard "
                       "members, concordant except that it "
                       "prints 'Timothy Hooper' where the "
                       "town's own page seats Andy Hooper")],
               [holder("Fred Dunnington", "fred-dunnington"),
                holder("Isabel Gogarty", "isabel-gogarty"),
                holder("Danielle Boyce", "danielle-boyce"),
                holder("Dan Brown", "dan-brown"),
                holder("Andy Hooper", "andy-hooper"),
                holder("Megan James", "megan-james"),
                holder("Farhad Khan", "farhad-khan")]),
        office("town-clerk", "Town Clerk",
               "Middlebury Town Clerk", 1,
               [charter127("section 304(d): the Town Clerk is "
                           "elected for a three-year term"),
                guide("names Karin Mott as Middlebury's town "
                      "clerk"),
                clerk_xlsx("lists Karin Mott as Middlebury's "
                           "town clerk")],
               [holder("Karin Mott", "karin-mott")]),
        office("town-treasurer", "Town Treasurer",
               "Middlebury Town Treasurer", 1,
               [charter127("section 305: the Town Treasurer is "
                           "appointed by the Selectboard"),
                treas_xlsx("lists Elizabeth Dow as Middlebury's "
                           "town treasurer"),
                guide("names 'Beth Dow' as Middlebury's town "
                      "treasurer -- the same person as the "
                      "treasurer spreadsheet's Elizabeth Dow "
                      "and as the elected lister of the same "
                      "name")],
               [holder("Elizabeth Dow", "elizabeth-dow",
                       how_seated="appointed")]),
        office("lister", "Lister",
               "Middlebury Board of Listers", 3,
               [charter127("section 304(a): three listers are "
                           "elected"),
                midb_listers("heads the board 'ELECTED BOARD OF "
                             "LISTERS' and seats Gary Baker "
                             "(2023-2026), Hudson Tilford "
                             "(2024-2027), and Beth Dow "
                             "(2025-2028). Baker's seat stood "
                             "in 2026; " + MIDB_GAP)],
               [holder("Elizabeth Dow", "elizabeth-dow",
                       ballot_name="Beth Dow"),
                holder("Hudson Tilford", "hudson-tilford")]),
        office("library-trustee", "Library Trustee",
               "Ilsley Public Library", 5,
               [charter127("section 302(a)(3): five Trustees of "
                           "the Ilsley Library are elected"),
                ilsley("seats five trustees: Meg Baker "
                       "(President, to March 2027), Barbara "
                       "Doyle-Wilch (2027), Marita Bathe Schine "
                       "(2028), Natasha Sen (Treasurer, 2028), "
                       "and Claire Tebbs (term ended March "
                       "2026). Tebbs's seat stood in 2026; "
                       + MIDB_GAP)],
               [holder("Meg Baker", "meg-baker"),
                holder("Barbara Doyle-Wilch",
                       "barbara-doyle-wilch"),
                holder("Marita Bathe Schine",
                       "marita-bathe-schine"),
                holder("Natasha Sen", "natasha-sen")]),
        office("moderator", "Moderator",
               "Middlebury Moderator", 1,
               [charter127("section 304(c): the Town Meeting "
                           "Moderator is elected annually; the "
                           "post is created without a membership "
                           "because the 2026 outcome is "
                           "unpublished -- " + MIDB_GAP)]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Middlebury Justices of the Peace", 15,
               [jp_src("lists fifteen Middlebury justices of "
                       "the peace elected November 5, 2024")],
               [holder("Brian Bauer", "brian-bauer",
                       ballot_name="Brian J. Bauer"),
                holder("Craig Bingham", "craig-bingham"),
                holder("Peter Caldwell", "peter-caldwell"),
                holder("David Dorman", "david-dorman"),
                holder("Kerri Duquette-Hoffman",
                       "kerri-duquette-hoffman"),
                holder("Alice George", "alice-george"),
                holder("Dean George", "dean-george"),
                holder("Isabel Gogarty", "isabel-gogarty"),
                holder("Don Keeler", "don-keeler"),
                holder("Carolyn Kuebler", "carolyn-kuebler"),
                holder("Deborah Mack", "deborah-mack"),
                holder("Margaret Martin", "margaret-martin",
                       ballot_name='Margaret "Peg" Martin'),
                holder("John McAninch", "john-mcaninch"),
                holder("Michael Olinick", "michael-olinick"),
                holder("Dave Silberman", "dave-silberman",
                       existing_person_id="ocd-person/15cb002a-a10f-5009-8d80-3b41dbb695bd")]),
    ]
    jp = jp_election(
        "middlebury-vt", "Town of Middlebury", 15,
        "lists fifteen Middlebury justices of the peace "
        "elected November 5, 2024: Brian J. Bauer, Craig "
        "Bingham, Peter Caldwell, David Dorman, Kerri "
        "Duquette-Hoffman, Alice George, Dean George, Isabel "
        "Gogarty, Don Keeler, Carolyn Kuebler, Deborah Mack, "
        "Margaret 'Peg' Martin, John McAninch, Michael "
        "Olinick, and Dave Silberman. The listing publishes no "
        "vote totals or party labels and none are recorded. "
        "Dave Silberman is Addison County's High Bailiff; his "
        "justice of the peace membership reuses his county "
        "person record")
    return spec("middlebury", "Town of Middlebury", offices, jp)


SPECS["middlebury"] = middlebury_spec()

# ------------------------------------------------------------ Middlesex
MDX_ADMIN = {
    "url": "https://middlesexvermont.org/town-departments/administration/",
    "note": "PLACEHOLDER",
}


def mdx_admin(what):
    return S(MDX_ADMIN, "Town of Middlesex (official website), "
             f"Administration page (the town's maintained "
             f"officials directory): {what}")


def middlesex_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Middlesex Selectboard", 5,
               [mdx_admin("seats the five selectboard members: "
                          "Liz Scharf (Chair), Zara Vincent "
                          "(Vice Chair), Paul Cerminara, Stacey "
                          "Skadberg, and Larry Rooney; the "
                          "surname is Cerminara per the town"),
                sb_dir("lists Middlesex's selectboard as "
                       "Elizabeth Scharf, Paul Cerminara, "
                       "Lawrence Rooney, Stacey Skadberg, and "
                       "Zara Vincent -- the directory's full "
                       "forms of the town page's Liz Scharf and "
                       "Larry Rooney are recorded")],
               [holder("Elizabeth Scharf", "elizabeth-scharf"),
                holder("Zara Vincent", "zara-vincent"),
                holder("Paul Cerminara", "paul-cerminara"),
                holder("Stacey Skadberg", "stacey-skadberg"),
                holder("Lawrence Rooney", "lawrence-rooney")]),
        office("town-clerk", "Town Clerk",
               "Middlesex Town Clerk", 1,
               [mdx_admin("states the Town Clerk 'is elected at "
                          "Town Meeting for a three-year term' "
                          "and names Brigid Browning"),
                clerk_xlsx("lists Brigid Browning as "
                           "Middlesex's town clerk -- the June "
                           "2026 spreadsheet governs over the "
                           "January 2026 Guide's Cheryl "
                           "Grandfield, who is now the treasurer")],
               [holder("Brigid Browning", "brigid-browning")]),
        office("town-treasurer", "Town Treasurer",
               "Middlesex Town Treasurer", 1,
               [mdx_admin("states the Town Treasurer 'is elected "
                          "at Town Meeting to a one-year term' "
                          "and names Cheryl Grandfield"),
                treas_xlsx("lists Cheryl Grandfield as "
                           "Middlesex's town treasurer"),
                guide("names Cheryl Grandfield as Middlesex's "
                      "town treasurer")],
               [holder("Cheryl Grandfield", "cheryl-grandfield")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Middlesex Collector of Delinquent Taxes", 1,
               [mdx_admin("names Cheryl Grandfield Collector of "
                          "Delinquent Taxes (elected, one-year "
                          "term)")],
               [holder("Cheryl Grandfield", "cheryl-grandfield")]),
        office("lister", "Lister",
               "Middlesex Board of Listers", 3,
               [mdx_admin("states 'three listers, one elected "
                          "each year for staggered three-year "
                          "terms' and names Samantha Beaudoin, "
                          "Shelley DesJardin, and Sean McVeigh "
                          "(Sean McVeigh the lister is not Chris "
                          "McVeigh the justice of the peace)")],
               [holder("Samantha Beaudoin", "samantha-beaudoin"),
                holder("Shelley DesJardin", "shelley-desjardin"),
                holder("Sean McVeigh", "sean-mcveigh")]),
        office("budget-committee", "Budget Committee Member",
               "Middlesex Budget Committee", 5,
               [mdx_admin("states the Budget Committee's 'five "
                          "members are elected to staggered "
                          "three-year terms' and names Mark "
                          "Harris (Chair), Samantha Beaudoin, "
                          "Dorinda Crowell, Elias Gardner, and "
                          "Zara Vincent. The same page records "
                          "that Middlesex voters have chosen to "
                          "use a professional outside auditor, "
                          "so no auditor post exists")],
               [holder("Mark Harris", "mark-harris"),
                holder("Samantha Beaudoin", "samantha-beaudoin"),
                holder("Dorinda Crowell", "dorinda-crowell"),
                holder("Elias Gardner", "elias-gardner"),
                holder("Zara Vincent", "zara-vincent")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Middlesex Justices of the Peace", 6,
               [jp_src("lists six Middlesex justices of the "
                       "peace elected November 5, 2024"),
                mdx_admin("the page's partial justice block "
                          "concurs on Crowell, Demeter, Chris "
                          "McVeigh, and Thouron")],
               [holder("Dorinda Crowell", "dorinda-crowell"),
                holder("Jan Thouron", "jan-thouron"),
                holder("Chris McVeigh", "chris-mcveigh"),
                holder("Mary Just Skinner", "mary-just-skinner"),
                holder("John Demeter", "john-demeter"),
                holder("Tammy McCullough", "tammy-mccullough")]),
    ]
    jp = jp_election(
        "middlesex-vt", "Town of Middlesex", 6,
        "lists six Middlesex justices of the peace elected "
        "November 5, 2024: Dorinda Crowell, Jan Thouron, Chris "
        "McVeigh, Mary Just Skinner, John Demeter, and Tammy "
        "McCullough. The listing publishes no vote totals or "
        "party labels and none are recorded")
    return spec("middlesex", "Town of Middlesex", offices, jp)


SPECS["middlesex"] = middlesex_spec()

# ----------------------------------------------------- Middletown Springs
MTS_SB = {
    "url": "https://middletownsprings.vt.gov/selectboard/",
    "note": "PLACEHOLDER",
}
MTS_CLERK = {
    "url": "https://middletownsprings.vt.gov/town-clerks-office",
    "note": "PLACEHOLDER",
}
MTS_TREAS = {
    "url": "https://middletownsprings.vt.gov/treasurer-delinquent-tax-collector",
    "note": "PLACEHOLDER",
}
MTS_LISTERS = {
    "url": "https://middletownsprings.vt.gov/board-of-listers",
    "note": "PLACEHOLDER",
}
MTS_AUDITORS = {
    "url": "https://middletownsprings.vt.gov/auditors",
    "note": "PLACEHOLDER",
}
MTS_LIBRARY = {
    "url": "https://middletownsprings.vt.gov/public-library-trustees",
    "note": "PLACEHOLDER",
}
MTS_MONIES = {
    "url": "https://middletownsprings.vt.gov/trustees-of-public-monies",
    "note": "PLACEHOLDER",
}
MTS_REPORT = {
    "url": "https://storage.googleapis.com/juniper-media-library/359/2025/07/FY%202024%20Town%20Report.pdf",
    "note": "PLACEHOLDER",
}


def mts_sb(what):
    return S(MTS_SB, "Town of Middletown Springs (official "
             f"website), Selectboard page: {what}")


def mts_clerk(what):
    return S(MTS_CLERK, "Town of Middletown Springs (official "
             f"website), Town Clerk's Office page: {what}")


def mts_treas(what):
    return S(MTS_TREAS, "Town of Middletown Springs (official "
             f"website), Treasurer / Delinquent Tax Collector "
             f"page: {what}")


def mts_listers(what):
    return S(MTS_LISTERS, "Town of Middletown Springs (official "
             f"website), Board of Listers page: {what}")


def mts_auditors(what):
    return S(MTS_AUDITORS, "Town of Middletown Springs (official "
             f"website), Auditors page: {what}")


def mts_library(what):
    return S(MTS_LIBRARY, "Town of Middletown Springs (official "
             f"website), Public Library Trustees page: {what}")


def mts_monies(what):
    return S(MTS_MONIES, "Town of Middletown Springs (official "
             f"website), Trustees of Public Monies page: {what}")


def mts_report(what):
    return S(MTS_REPORT, "Town of Middletown Springs, FY2024 "
             f"Town Report: {what}")


def middletown_springs_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Middletown Springs Selectboard", 5,
               [mts_sb("seats Robin Chesnut-Tangerman (Chair), "
                       "Isaac Yackel (Vice Chair), Terry "
                       "Redfield, and Chris Fenton, and notes "
                       "Neil Russell was APPOINTED to the board "
                       "on September 10, 2026"),
                sb_dir("lists Middletown Springs' selectboard "
                       "as Robin Chesnut-Tangerman, Isaac "
                       "Yackel, Chris Fenton, Carl Haynes, and "
                       "Terry Redfield; the directory predates "
                       "Haynes's departure and Russell's "
                       "appointment, which the town's own page "
                       "records")],
               [holder("Robin Chesnut-Tangerman",
                       "robin-chesnut-tangerman"),
                holder("Isaac Yackel", "isaac-yackel"),
                holder("Terry Redfield", "terry-redfield"),
                holder("Chris Fenton", "chris-fenton"),
                holder("Neil Russell", "neil-russell",
                       how_seated="appointed")]),
        office("town-clerk", "Town Clerk",
               "Middletown Springs Town Clerk", 1,
               [mts_clerk("names Patty Kenyon Town Clerk "
                          "(three-year term ending March 2027) "
                          "and describes the clerk as 'an "
                          "independent official, answerable only "
                          "to the voters'"),
                guide("names Patty Kenyon as Middletown "
                      "Springs' town clerk"),
                clerk_xlsx("lists Patty Kenyon as Middletown "
                           "Springs' town clerk")],
               [holder("Patty Kenyon", "patty-kenyon")]),
        office("town-treasurer", "Town Treasurer",
               "Middletown Springs Town Treasurer", 1,
               [mts_treas("names Jenny Talke Munyak Town "
                          "Treasurer (elected, three-year term); "
                          "the full name form is the town "
                          "page's"),
                guide("names Jenny Talke Munyak as Middletown "
                      "Springs' town treasurer"),
                treas_xlsx("lists 'Jenny Munyak' as Middletown "
                           "Springs' town treasurer -- the same "
                           "person, shortened form")],
               [holder("Jenny Talke Munyak",
                       "jenny-talke-munyak")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Middletown Springs Collector of Delinquent Taxes",
               1,
               [mts_report("the FY2024 report's elected-officers "
                           "table carries Heather Grier as "
                           "Collector of Delinquent Taxes with "
                           "the footnote '* Appointed Until Town "
                           "Meeting 2025': the office is "
                           "elective (three-year term) but her "
                           "last verified mode is the "
                           "appointment and no published 2025 "
                           "outcome was reachable, so she is "
                           "minted appointed and flagged for "
                           "recheck")],
               [holder("Heather Grier", "heather-grier",
                       how_seated="appointed")]),
        office("lister", "Lister",
               "Middletown Springs Board of Listers", 3,
               [mts_listers("names the three listers: Sally "
                            "Achey (Chair), Patricia Hemenway, "
                            "and Randy Kniffin")],
               [holder("Sally Achey", "sally-achey"),
                holder("Patricia Hemenway", "patricia-hemenway"),
                holder("Randy Kniffin", "randy-kniffin")]),
        office("auditor", "Auditor",
               "Middletown Springs Auditors", 3,
               [mts_auditors("heads its roster 'Auditors as of "
                             "March 2025' on the town's current "
                             "page and names Juanita Burch-Clay, "
                             "Tracy Weatherhogg, and Meredith "
                             "Morgan; the roster's date is "
                             "disclosed here. The FY2024 report "
                             "prints 'Juanita Burch Clay'; the "
                             "page's hyphenated form governs")],
               [holder("Juanita Burch-Clay", "juanita-burch-clay"),
                holder("Tracy Weatherhogg", "tracy-weatherhogg"),
                holder("Meredith Morgan", "meredith-morgan")]),
        office("library-trustee", "Library Trustee",
               "Middletown Springs Public Library", 5,
               [mts_library("states the Public Library Trustees "
                            "are five, elected to staggered "
                            "three-year terms, and names Kristal "
                            "Haynes Hier (Chair, 2027), Glenn "
                            "Tarbell (2027), Mackenzie Floyd "
                            "(2028), Bree Gunter (2029), and "
                            "Linda Hurcomb (2029)")],
               [holder("Kristal Haynes Hier",
                       "kristal-haynes-hier"),
                holder("Glenn Tarbell", "glenn-tarbell"),
                holder("Mackenzie Floyd", "mackenzie-floyd"),
                holder("Bree Gunter", "bree-gunter"),
                holder("Linda Hurcomb", "linda-hurcomb")]),
        office("trustee-of-public-funds",
               "Trustee of Public Monies",
               "Middletown Springs Trustees of Public Monies", 3,
               [mts_monies("names Steven Harrington (to 2028) "
                           "as a Trustee of Public Monies and "
                           "shows the other two seats (2027 and "
                           "2029) VACANT, so only Harrington is "
                           "minted")],
               [holder("Steven Harrington", "steven-harrington")]),
        office("moderator", "Moderator",
               "Middletown Springs Moderator", 1,
               [statute2646_structure("elected town moderator, "
                                      "one-year term"),
                mts_report("the FY2024 report shows Andrew "
                           "Hayes held the moderator's office "
                           "by appointment until Town Meeting "
                           "2025; no current holder is "
                           "published, so no holder is minted")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Middletown Springs Justices of the Peace", 5,
               [jp_src("lists five Middletown Springs justices "
                       "of the peace elected November 5, 2024"),
                mts_report("the FY2024 report's justice of the "
                           "peace block names the same five")],
               [holder("Herb Childress", "herb-childress"),
                holder("Patricia Hemenway", "patricia-hemenway"),
                holder("Meredith Morgan", "meredith-morgan"),
                holder("Chris Fenton", "chris-fenton",
                       ballot_name="Christopher Fenton"),
                holder("Chere Tournet", "chere-tournet")]),
    ]
    jp = jp_election(
        "middletown-springs-vt", "Town of Middletown Springs", 5,
        "lists five Middletown Springs justices of the peace "
        "elected November 5, 2024: Herb Childress, Patricia "
        "Hemenway, Meredith Morgan, Christopher Fenton, and "
        "Chere Tournet. The listing publishes no vote totals or "
        "party labels and none are recorded",
        [mts_report("the FY2024 report's justice of the peace "
                    "block names the same five")])
    return spec("middletown-springs", "Town of Middletown Springs",
                offices, jp)


SPECS["middletown-springs"] = middletown_springs_spec()

# ------------------------------------------------------------ emit
for slug in ORDER:
    s = SPECS[slug]
    p = OUT / f"{s['place_slug']}.json"
    p.write_text(json.dumps(s, indent=1) + "\n")
    n_off = len(s["offices"])
    n_hold = sum(len(o.get("holders", ())) for o in s["offices"])
    print(f"{s['place_slug']}: {n_off} offices, {n_hold} holders")
print(f"TOTAL: {len(SPECS)} specs")
