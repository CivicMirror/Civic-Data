#!/usr/bin/env python3
"""Batch 18 of the VT #163 municipal fan-out (alphabetical positions
170-179): Peacham, Peru, Pittsfield, Pittsford, Plainfield,
Plymouth, Pomfret, Town of Poultney, Village of Poultney, Pownal.
Emits one JSON spec per municipality for build_vt_municipality.py.
Research: vt_muni_batch18_research.md.

Identity calls baked into this batch (all flagged on #163):
- Pittsford's Selectboard chair Alicia Malay is the sitting State
  Representative for Rutland-8 (the district includes Pittsford):
  her SB membership reuses the state-tier person record
  ocd-person/5c402261-3cd7-5302-ada8-ee1b6afaad16.
- Pittsfield's Moderator Ian Sullivan is minted as a NEW person,
  distinct from Rutland County State's Attorney Ian Sullivan
  (different county, no linking fact; batch-8 Jessica Chase
  precedent).
- Pittsford's Town Clerk and Town Treasurer are APPOINTED:
  Dolores Gecha won both offices on the March 3, 2026 ballot,
  but the voters' floor Articles 6 and 7 (17 V.S.A. sections
  2651e and 2651f) authorized selectboard appointment, and the
  Selectboard appointed her to both offices effective April 17,
  2026 (March 4, 2026 minutes).
- Plainfield's Town Clerk (Jaime Hammack) and Town Treasurer
  (Tammy Martel) are minted APPOINTED on a disclosed inference:
  both succeeded departed incumbents (Bram Towbin, Josh Pitts)
  with no race warned or returned in 2026, leaving selectboard
  appointment as the only lawful seating mechanism.
- Plainfield's certified March 3, 2026 return was read from the
  Wayback Machine's March 5, 2026 capture: the live PDF on the
  town website now returns 404.
- Pomfret's Marjorie Wakefield (elected to the Selectboard, the
  Trustees of Public Funds, and as a Justice of the Peace) died
  in May 2026. Per the batch-8 Enosburgh (Avis Gervais) pattern
  she is minted nowhere: no person, no winner entry, no
  membership; the election and post notes tell her story. Her
  Selectboard seat is held by appointee Eric Chase; Steve
  Chamberlin's seat by appointee Kyle Hansen.
- Poultney Village is a partial mint: trustees DeBonis, Atwood,
  and Harrison are corroborated on the merger study's official
  steering-committee page; trustees Gray and Worthing, the
  Village President, and the Village Clerk/Treasurer rest only
  on a restricted clerk-reply roster and are NOT minted.
- Plymouth's JP slate follows the certified SOS listing over
  the town's own table (equal-count name-swap; the town-only
  names Pauley, Pingree, and Mary Morsey are held).
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
CHARTER_131 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/131",
    "note": "PLACEHOLDER",
}
CHARTER_133 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/133",
    "note": "PLACEHOLDER",
}
CHARTER_269 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/269",
    "note": "PLACEHOLDER",
}
PEACHAM_MIN = {
    "url": "https://peachamvt.org/wp-content/uploads/2026/04/Town-Meeting-minutes-2026-signed.pdf",
    "note": "PLACEHOLDER",
}
PEACHAM_WARN = {
    "url": "https://peachamvt.org/wp-content/uploads/2026/04/Town-Meeting-Warning-2026-signed.pdf",
    "note": "PLACEHOLDER",
}
PEACHAM_SB = {
    "url": "https://peachamvt.org/selectboard/",
    "note": "PLACEHOLDER",
}
PEACHAM_REPORTS = {
    "url": "https://peachamvt.org/documents/town-reports/",
    "note": "PLACEHOLDER",
}
PERU_GOV = {
    "url": "https://peruvt.org/government/",
    "note": "PLACEHOLDER",
}
PERU_WARN = {
    "url": "https://peruvt.org/wp-content/uploads/2026/01/Peru-Annual-Meeting-Warning-2026-1.pdf",
    "note": "PLACEHOLDER",
}
PF_ELECTED = {
    "url": "https://www.pittsfieldvt.com/elected-officials.html",
    "note": "PLACEHOLDER",
}
PF_MINUTES = {
    "url": "https://www.pittsfieldvt.com/town-meeting/draft-minutes-of-the-annual-pittsfield-town-and-school-meeting-tuesday-march-3-3036",
    "note": "PLACEHOLDER",
}
PF_CEM = {
    "url": "https://www.pittsfieldvt.com/cemetery-commission.html",
    "note": "PLACEHOLDER",
}
PF_LIB = {
    "url": "https://www.pittsfieldvt.com/roger-clark-memorial-library.html",
    "note": "PLACEHOLDER",
}
PFORD_WARN = {
    "url": "https://www.pittsfordvermont.com/wp-content/uploads/2026/01/Town-Meeting-Warning-2026.pdf",
    "note": "PLACEHOLDER",
}
PFORD_MIN = {
    "url": "https://www.pittsfordvermont.com/wp-content/uploads/2026/03/Selectboard-Minutes-3-4-2026.pdf",
    "note": "PLACEHOLDER",
}
PFORD_CLERK = {
    "url": "https://www.pittsfordvermont.com/town-clerk-treasurer/",
    "note": "PLACEHOLDER",
}
PLF_RETURN = {
    "url": "https://web.archive.org/web/20260305174110/https://www.plainfieldvt.gov/uploads/8/1/0/6/81063668/article_iii_australian_ballot_official_return_of_votes.pdf",
    "note": "PLACEHOLDER",
}
PLF_REPORT = {
    "url": "https://www.plainfieldvt.gov/uploads/8/1/0/6/81063668/plainfield_town_report_2025.pdf",
    "note": "PLACEHOLDER",
}
PLF_OFFICE = {
    "url": "https://www.plainfieldvt.gov/town-office.html",
    "note": "PLACEHOLDER",
}
PLY_OFFICIALS = {
    "url": "https://www.plymouthvt.org/elected-town-officials/",
    "note": "PLACEHOLDER",
}
PLY_OFFICERS = {
    "url": "https://www.plymouthvt.org/town-officers-appointments/",
    "note": "PLACEHOLDER",
}
PLY_WARNINGS = {
    "url": "https://www.plymouthvt.org/warnings/",
    "note": "PLACEHOLDER",
}
POM_REPORT = {
    "url": "https://pomfretvt.us/index.php/download_file/view/2818/225/",
    "note": "PLACEHOLDER",
}
POM_RESULTS = {
    "url": "https://pomfretvt.us/index.php/download_file/view/2830/225/",
    "note": "PLACEHOLDER",
}
POM_SB = {
    "url": "https://pomfretvt.us/index.php/boar/sel/",
    "note": "PLACEHOLDER",
}
POM_AUD = {
    "url": "https://pomfretvt.us/index.php/boar/auditors/",
    "note": "PLACEHOLDER",
}
POM_OT = {
    "url": "https://pomfretvt.us/index.php/boar/ot/",
    "note": "PLACEHOLDER",
}
POU_REPORT = {
    "url": "https://www.poultneyvt.gov/fileadmin/files/Selectboard/Town_Reports/2025_Poultney_Report.pdf",
    "note": "PLACEHOLDER",
}
POU_SB = {
    "url": "https://www.poultneyvt.gov/boards-meetings/selectboard",
    "note": "PLACEHOLDER",
}
POU_CLERK = {
    "url": "https://www.poultneyvt.gov/services/town-clerk-treasurer",
    "note": "PLACEHOLDER",
}
POU_VACANCY = {
    "url": "https://www.poultneyvt.gov/news/post/selectboard-notice-of-vacancy-september-2026",
    "note": "PLACEHOLDER",
}
CGR_STEERING = {
    "url": "https://www.cgr.org/poultneyvtstudy/project-steering-committee/",
    "note": "PLACEHOLDER",
}
POWNAL_REPORT = {
    "url": "https://www.townofpownal.org/uploads/1/3/7/4/137413037/town_report_2025.pdf",
    "note": "PLACEHOLDER",
}
POWNAL_CONTACTS = {
    "url": "https://www.townofpownal.org/town-contacts.html",
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


def charter131(phrase):
    return S(CHARTER_131, f"24 App. V.S.A. ch. 131 (Town of "
             f"Plainfield): {phrase}")


def charter133(phrase):
    return S(CHARTER_133, f"24 App. V.S.A. ch. 133 (Town of "
             f"Poultney): {phrase}")


def charter269(phrase):
    return S(CHARTER_269, f"24 App. V.S.A. ch. 269 (Village of "
             f"Poultney): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 18); issue #163 "
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
                  f"# municipal fan-out batch 18; issue #163 "
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
        "holders": list(holders),
    }
    d.update(kw)
    return d


SPECS = {}

# ----------------------------------------------------------------
# Town of Peacham (Caledonia County) -- general law.
PEACHAM_MIN_C = ("Town of Peacham, Town Meeting Minutes, March 3, "
                 "2026 (signed; peachamvt.org)")
SPECS["peacham"] = spec("peacham", "Town of Peacham", [
    office("moderator", "Town Moderator",
           "Town of Peacham Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(PEACHAM_MIN, f"{PEACHAM_MIN_C}: Article 1 -- Tim "
                           "McKay was re-elected Moderator for "
                           "the ensuing year; he announced it is "
                           "his fifteenth and final year")],
           [holder("Tim McKay", "tim-mckay")]),
    office("town-clerk", "Town Clerk",
           "Town of Peacham Town Clerk", 1,
           [statute2646("towns elect a town clerk; Peacham's "
                        "warning elects the clerk to a three-year "
                        "term"),
            S(PEACHAM_MIN, f"{PEACHAM_MIN_C}: Article 11 -- "
                           "Rebecca Washington was re-elected "
                           "Town Clerk for a three-year term"),
            guide("lists Rebecca Washington as Peacham's Town "
                  "Clerk")],
           [holder("Rebecca Washington", "rebecca-washington")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Peacham Town Treasurer", 1,
           [statute2646("towns elect a town treasurer; Peacham's "
                        "warning elects one officer as 'Town "
                        "Treasurer and Tax Collector'"),
            S(PEACHAM_MIN, f"{PEACHAM_MIN_C}: Article 12 -- "
                           "Rebecca Washington was re-elected "
                           "Town Treasurer and Tax Collector for "
                           "a three-year term. Peacham elects the "
                           "treasurer and the tax collector as one "
                           "combined office; it is modeled as this "
                           "single treasurer post, and Peacham's "
                           "separately warned Delinquent Tax "
                           "Collector (Article 20, a one-year "
                           "office) is a distinct post"),
            guide("lists Rebecca Washington as Peacham's Town "
                  "Treasurer")],
           [holder("Rebecca Washington", "rebecca-washington")]),
    office("selectboard", "Selectboard Member",
           "Town of Peacham Selectboard", 5,
           [sb_dir("lists Peacham's five selectboard members: "
                   "Alfred Dedam (Chair), Will Kempton, Andrea "
                   "Otto, Christina Rumery, and Christian Snow"),
            S(PEACHAM_MIN, f"{PEACHAM_MIN_C}: Article 13 -- "
                           "Andrea Otto was elected to a "
                           "three-year term (she had been filling "
                           "a vacancy; Peter Craig departed); "
                           "Article 14 -- Christian Snow was "
                           "re-elected to a two-year term; Article "
                           "15 -- Christina Rumery was elected to "
                           "a one-year term completing a vacated "
                           "term"),
            S(PEACHAM_SB, "Town of Peacham, Selectboard page "
                          "(peachamvt.org): lists the same five "
                          "members")],
           [holder("Alfred Dedam", "alfred-dedam"),
            holder("Will Kempton", "will-kempton"),
            holder("Andrea Otto", "andrea-otto"),
            holder("Christina Rumery", "christina-rumery"),
            holder("Christian Snow", "christian-snow")]),
    office("lister", "Lister",
           "Town of Peacham Board of Listers", 3,
           [statute2646("towns elect a board of listers of three "
                        "on staggered three-year terms"),
            S(PEACHAM_MIN, f"{PEACHAM_MIN_C}: Article 16 -- "
                           "Nathan Colpitts was elected Lister "
                           "for a three-year term"),
            S(PEACHAM_REPORTS, "Town of Peacham, 2025 Town Report "
                               "(posted on the town's town "
                               "reports page): the town officers "
                               "table lists listers Nathan "
                               "Colpitts, Clarissa Kendall (term "
                               "to 2027), and Jean Dedam (term to "
                               "2028)")],
           [holder("Nathan Colpitts", "nathan-colpitts"),
            holder("Clarissa Kendall", "clarissa-kendall"),
            holder("Jean Dedam", "jean-dedam")]),
    office("auditor", "Town Auditor",
           "Town of Peacham Auditors", 3,
           [statute2646("towns elect three auditors on staggered "
                        "three-year terms"),
            S(PEACHAM_MIN, f"{PEACHAM_MIN_C}: Article 17 -- Jill "
                           "Hurst was elected Auditor for a "
                           "three-year term"),
            S(PEACHAM_REPORTS, "Town of Peacham, 2025 Town Report "
                               "(posted on the town's town "
                               "reports page): the town officers "
                               "table lists auditors Jill Hurst, "
                               "Charlotte Mooney (term to 2027), "
                               "and Robert Starbuck (term to "
                               "2028)")],
           [holder("Jill Hurst", "jill-hurst"),
            holder("Charlotte Mooney", "charlotte-mooney"),
            holder("Robert Starbuck", "robert-starbuck")]),
    office("first-constable", "First Constable",
           "Town of Peacham First Constable", 1,
           [statute2646("towns elect a first constable"),
            S(PEACHAM_MIN, f"{PEACHAM_MIN_C}: Article 18 -- John "
                           "Sheehan was re-elected First "
                           "Constable for a one-year term")],
           [holder("John Sheehan", "john-sheehan")]),
    office("second-constable", "Second Constable",
           "Town of Peacham Second Constable", 1,
           [statute2646("towns may elect a second constable; "
                        "Peacham's warning elects one"),
            S(PEACHAM_MIN, f"{PEACHAM_MIN_C}: Article 19 -- Nate "
                           "Giroux was re-elected Second "
                           "Constable for a one-year term")],
           [holder("Nate Giroux", "nate-giroux")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Peacham Collector of Delinquent Taxes", 1,
           [statute2646("towns may elect a collector of "
                        "delinquent taxes; Peacham elects one "
                        "annually under Article 20, separately "
                        "from its combined Treasurer and Tax "
                        "Collector office"),
            S(PEACHAM_MIN, f"{PEACHAM_MIN_C}: Article 20 -- John "
                           "Sheehan was re-elected Collector of "
                           "Delinquent Taxes for a one-year term")],
           [holder("John Sheehan", "john-sheehan")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Peacham Justices of the Peace", 5,
           [jp_src("lists five Peacham justices of the peace: "
                   "Sam Kempton, Sabrina Kaufman, Diana Senturia, "
                   "Cynther Greene, and Rick Scholes")],
           [holder("Sam Kempton", "sam-kempton"),
            holder("Sabrina Kaufman", "sabrina-kaufman"),
            holder("Diana Senturia", "diana-senturia"),
            holder("Cynther Greene", "cynther-greene"),
            holder("Rick Scholes", "rick-scholes")]),
], jp=jp_election("peacham-vt", "Town of Peacham", 5,
                  "the certified listing names five winners for "
                  "Peacham's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Peru (Bennington County) -- general law.
PERU_GOV_C = ("Town of Peru, Government page (peruvt.org): the "
              "town's published elected-officials roster, with "
              "term years")
SPECS["peru"] = spec("peru", "Town of Peru", [
    office("moderator", "Town Moderator",
           "Town of Peru Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(PERU_GOV, f"{PERU_GOV_C} lists Gary Ameden as "
                        "Moderator, term to 2027; he was elected "
                        "at the March 3, 2026 town meeting")],
           [holder("Gary Ameden", "gary-ameden")]),
    office("town-clerk", "Town Clerk",
           "Town of Peru Town Clerk", 1,
           [S(PERU_WARN, "Town of Peru, Annual Meeting Warning "
                         "2026: Article 3 elects a Town Clerk "
                         "for a one-year term at the March 3, "
                         "2026 floor meeting"),
            S(PERU_GOV, f"{PERU_GOV_C} lists Melinda M. Beebe as "
                        "Town Clerk, term to 2027"),
            guide("lists Melinda Beebe as Peru's Town Clerk")],
           [holder("Melinda M. Beebe", "melinda-m-beebe")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Peru Town Treasurer", 1,
           [S(PERU_WARN, "Town of Peru, Annual Meeting Warning "
                         "2026: Article 3 elects a Town Treasurer "
                         "for a one-year term"),
            S(PERU_GOV, f"{PERU_GOV_C} lists Cheryl Fox as Town "
                        "Treasurer, term to 2027"),
            guide("lists Cheryl Fox as Peru's Town Treasurer")],
           [holder("Cheryl Fox", "cheryl-fox")]),
    office("selectboard", "Selectboard Member",
           "Town of Peru Selectboard", 3,
           [sb_dir("lists Peru's three selectboard members: Andy "
                   "Dahlstrom (Chair), Ben Foltz, and Laurie "
                   "Gayda"),
            S(PERU_GOV, f"{PERU_GOV_C} lists Andy Dahlstrom "
                        "(Chair, term to 2028), Ben Foltz (2027), "
                        "and Laurie Gayda (2029)")],
           [holder("Andy Dahlstrom", "andy-dahlstrom"),
            holder("Ben Foltz", "ben-foltz"),
            holder("Laurie Gayda", "laurie-gayda")]),
    office("lister", "Lister",
           "Town of Peru Board of Listers", 3,
           [statute2646("towns elect a board of listers of three "
                        "on staggered three-year terms"),
            S(PERU_GOV, f"{PERU_GOV_C} lists listers Jack "
                        "Pennypacker (Chair, term to 2027), Jim "
                        "Bowen (2028), and Richard Rockwell "
                        "(2029)")],
           [holder("Jack Pennypacker", "jack-pennypacker"),
            holder("Jim Bowen", "jim-bowen"),
            holder("Richard Rockwell", "richard-rockwell")]),
    office("auditor", "Town Auditor",
           "Town of Peru Auditors", 3,
           [statute2646("towns elect three auditors on staggered "
                        "three-year terms"),
            S(PERU_GOV, f"{PERU_GOV_C} lists auditors Heidi "
                        "Healy (term to 2029), Ruth Ann Barrick "
                        "(2028), and Jon Livingston (2027)")],
           [holder("Heidi Healy", "heidi-healy"),
            holder("Ruth Ann Barrick", "ruth-ann-barrick"),
            holder("Jon Livingston", "jon-livingston")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Peru Cemetery Commission", 5,
           [S(PERU_WARN, "Town of Peru, Annual Meeting Warning "
                         "2026: Article 3 elects a Cemetery "
                         "Commissioner for a five-year term; "
                         "Peru's commissioners serve staggered "
                         "five-year terms"),
            S(PERU_GOV, f"{PERU_GOV_C} lists cemetery "
                        "commissioners Will Crandall (Chair, term "
                        "to 2029), Carl Holcomb (2027), Jeremy "
                        "LaPan (2030), and Ivanna Reed (2031). "
                        "The fifth seat's holder is published in "
                        "no official source, so it is created "
                        "without a membership")],
           [holder("Will Crandall", "will-crandall"),
            holder("Carl Holcomb", "carl-holcomb"),
            holder("Jeremy LaPan", "jeremy-lapan"),
            holder("Ivanna Reed", "ivanna-reed")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Peru Collector of Delinquent Taxes", 1,
           [S(PERU_WARN, "Town of Peru, Annual Meeting Warning "
                         "2026: Article 3 elects a Collector of "
                         "Delinquent Taxes for a one-year term"),
            S(PERU_GOV, f"{PERU_GOV_C} lists Tracy Black as "
                        "Collector of Delinquent Taxes, term to "
                        "2027")],
           [holder("Tracy Black", "tracy-black")]),
    office("first-constable", "First Constable",
           "Town of Peru First Constable", 1,
           [S(PERU_WARN, "Town of Peru, Annual Meeting Warning "
                         "2026: Article 3 elects a First "
                         "Constable for a one-year term"),
            S(PERU_GOV, f"{PERU_GOV_C} lists Mike Gayda as First "
                        "Constable, term to 2027")],
           [holder("Mike Gayda", "mike-gayda")]),
    office("second-constable", "Second Constable",
           "Town of Peru Second Constable", 1,
           [S(PERU_WARN, "Town of Peru, Annual Meeting Warning "
                         "2026: Article 3 elects a Second "
                         "Constable for a one-year term"),
            S(PERU_GOV, f"{PERU_GOV_C} lists Josh Witkin as "
                        "Second Constable, term to 2027")],
           [holder("Josh Witkin", "josh-witkin")]),
    office("grand-juror", "Grand Juror",
           "Town of Peru Grand Juror", 1,
           [statute2646("towns elect a grand juror for a "
                        "one-year term"),
            S(PERU_GOV, f"{PERU_GOV_C} lists Ivanna Reed as "
                        "Grand Juror, term to 2027")],
           [holder("Ivanna Reed", "ivanna-reed")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Peru Trustees of Public Funds", 1,
           [statute2646("towns that hold trust funds elect a "
                        "trustee of public funds"),
            S(PERU_GOV, f"{PERU_GOV_C} lists Josh Witkin as "
                        "Trustee of Public Funds, term to 2027")],
           [holder("Josh Witkin", "josh-witkin")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Peru Justices of the Peace", 5,
           [jp_src("lists five Peru justices of the peace: Olivia "
                   "Rukat, Karen Utiger, Iwanna Reed, Gary "
                   "Ameden, and Tracy Black. The town's "
                   "government page names the same five and "
                   "styles her 'Ivanna Reed'; the person record "
                   "uses the town's form and the candidacy the "
                   "listing's")],
           [holder("Olivia Rukat", "olivia-rukat"),
            holder("Karen Utiger", "karen-utiger"),
            holder("Ivanna Reed", "ivanna-reed",
                   ballot_name="Iwanna Reed"),
            holder("Gary Ameden", "gary-ameden"),
            holder("Tracy Black", "tracy-black")]),
], jp=jp_election("peru-vt", "Town of Peru", 5,
                  "the certified listing names five winners for "
                  "Peru's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Pittsfield (Rutland County) -- general law.
PF_DRAFT = ("Town of Pittsfield, Draft Minutes of the Annual "
            "Pittsfield Town and School Meeting, Tuesday, March "
            "3, 2026 (posted on the town's town meeting page; "
            "DRAFT minutes -- the town's official posted record "
            "of the meeting)")
PF_ELECTED_C = ("Town of Pittsfield, Elected Officials page "
                "(pittsfieldvt.com)")
SPECS["pittsfield"] = spec("pittsfield", "Town of Pittsfield", [
    office("moderator", "Town Moderator",
           "Town of Pittsfield Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(PF_MINUTES, f"{PF_DRAFT}: Article 1 -- the outgoing "
                          "moderator, George Deblon, declined, "
                          "and Ian Sullivan was elected Moderator "
                          "for a one-year term. This Ian Sullivan "
                          "is a Pittsfield (Windsor County) town "
                          "officer and is not Rutland County "
                          "State's Attorney Ian Sullivan")],
           [holder("Ian Sullivan", "ian-sullivan")]),
    office("selectboard", "Selectboard Member",
           "Town of Pittsfield Selectboard", 3,
           [sb_dir("lists Joyce Stevens and AJ Ruben as "
                   "Pittsfield selectboard members and styles "
                   "Ann Kuendig 'Select Board Secretary'; she is "
                   "a member of the board -- 'Secretary' is a "
                   "board role"),
            S(PF_MINUTES, f"{PF_DRAFT}: Joyce Stevens was "
                          "re-elected to the Selectboard for a "
                          "three-year term"),
            S(PF_ELECTED, f"{PF_ELECTED_C}: lists Ann Kuendig, "
                          "AJ Ruben, and Joyce Stevens as the "
                          "town's selectboard members")],
           [holder("Ann Kuendig", "ann-kuendig"),
            holder("AJ Ruben", "aj-ruben"),
            holder("Joyce Stevens", "joyce-stevens")]),
    office("town-clerk", "Town Clerk",
           "Town of Pittsfield Town Clerk", 1,
           [S(PF_MINUTES, f"{PF_DRAFT}: Tricia Abbondelo was "
                          "elected Town Clerk for a three-year "
                          "term"),
            guide("lists Tricia Abbondelo as Pittsfield's Town "
                  "Clerk")],
           [holder("Tricia Abbondelo", "tricia-abbondelo")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Pittsfield Town Treasurer", 1,
           [S(PF_MINUTES, f"{PF_DRAFT}: Tricia Abbondelo was "
                          "elected Town Treasurer for a "
                          "three-year term, in a separate article "
                          "from the clerkship"),
            guide("lists Tricia Abbondelo as Pittsfield's Town "
                  "Treasurer")],
           [holder("Tricia Abbondelo", "tricia-abbondelo")]),
    office("lister", "Lister",
           "Town of Pittsfield Board of Listers", 3,
           [statute2646("towns elect a board of listers of three "
                        "on staggered three-year terms"),
            S(PF_MINUTES, f"{PF_DRAFT}: Jennifer Wall Howard "
                          "was elected Lister for a three-year "
                          "term and Jonathan Colton was elected "
                          "Lister for a one-year term"),
            S(PF_ELECTED, f"{PF_ELECTED_C}: lists listers "
                          "Jonathan Colton, Jeremy Rayner, and "
                          "Jennifer Howard")],
           [holder("Jonathan Colton", "jonathan-colton"),
            holder("Jeremy Rayner", "jeremy-rayner"),
            holder("Jennifer Wall Howard", "jennifer-wall-howard")]),
    office("auditor", "Town Auditor",
           "Town of Pittsfield Auditors", 3,
           [statute2646("towns elect three auditors on staggered "
                        "three-year terms"),
            S(PF_MINUTES, f"{PF_DRAFT}: Anne Muller was elected "
                          "Auditor for a three-year term"),
            S(PF_ELECTED, f"{PF_ELECTED_C}: lists auditors "
                          "Kadimik (printed 'Kadamik'), Beth "
                          "Stanton, and Ann Muller; the fuller "
                          "forms from the minutes and the "
                          "certified justice of the peace listing "
                          "(Candace Kadimik, Mary Elizabeth "
                          "Stanton, Anne Muller) are used for "
                          "the person records")],
           [holder("Candace Kadimik", "candace-kadimik"),
            holder("Mary Elizabeth Stanton",
                   "mary-elizabeth-stanton"),
            holder("Anne Muller", "anne-muller")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Pittsfield Collector of Delinquent Taxes", 1,
           [S(PF_MINUTES, f"{PF_DRAFT}: Janice Stumpf was elected "
                          "Collector of Delinquent Taxes for a "
                          "one-year term")],
           [holder("Janice Stumpf", "janice-stumpf")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Pittsfield Trustees of Public Funds", 3,
           [statute2646("towns that hold trust funds elect "
                        "trustees of public funds"),
            S(PF_MINUTES, f"{PF_DRAFT}: Henry Hotchkiss was "
                          "elected Trustee of Public Funds for a "
                          "three-year term. One three-year seat "
                          "stands each year, so the board has "
                          "three seats; the other two holders are "
                          "published in no current official "
                          "source, so those seats are created "
                          "without memberships")],
           [holder("Henry Hotchkiss", "henry-hotchkiss")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Pittsfield Cemetery Commission", 5,
           [S(PF_CEM, "Town of Pittsfield, Cemetery Commission "
                      "page (pittsfieldvt.com): lists five "
                      "commissioners -- Chuck Colton, Steve "
                      "Martin, George Deblon, Connie Martin, and "
                      "Martha Beyersdorf"),
            S(PF_MINUTES, f"{PF_DRAFT}: Martha Beyersdorf and "
                          "George Deblon were elected Cemetery "
                          "Commissioners for three-year terms "
                          "(the draft minutes print 'Marth "
                          "Beyersdorf'; the commission page and "
                          "the town's 2015 records spell Martha)")],
           [holder("Chuck Colton", "chuck-colton"),
            holder("Steve Martin", "steve-martin"),
            holder("George J. Deblon", "george-j-deblon"),
            holder("Connie Martin", "connie-martin"),
            holder("Martha Beyersdorf", "martha-beyersdorf")]),
    office("library-trustee", "Library Trustee",
           "Roger Clark Memorial Library Trustees", 5,
           [S(PF_LIB, "Roger Clark Memorial Library, Trustees "
                      "page (on the town website, "
                      "pittsfieldvt.com): lists five trustees -- "
                      "Micheline Bissell, Doreen Morin, Amanda "
                      "Barrett, Cynthia Bryant, and Katrina "
                      "Hotchkiss"),
            S(PF_MINUTES, f"{PF_DRAFT}: Katrina Hotchkiss was "
                          "elected a Roger Clark Memorial "
                          "Library Trustee for a three-year term")],
           [holder("Micheline Bissell", "micheline-bissell"),
            holder("Doreen Morin", "doreen-morin"),
            holder("Amanda Barrett", "amanda-barrett"),
            holder("Cynthia Bryant", "cynthia-bryant"),
            holder("Katrina Hotchkiss", "katrina-hotchkiss")]),
    office("second-constable", "Second Constable",
           "Town of Pittsfield Second Constable", 1,
           [S(PF_MINUTES, f"{PF_DRAFT}: Doug Mianulli was "
                          "elected Second Constable for a "
                          "two-year term. Pittsfield's 2026 "
                          "warning elected a Second Constable "
                          "only; the town elects no First "
                          "Constable, so no first-constable post "
                          "is created")],
           [holder("Doug Mianulli", "doug-mianulli")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Pittsfield Justices of the Peace", 5,
           [jp_src("lists five Pittsfield justices of the peace: "
                   "Candace Kadimik, Roger Stevens, George J. "
                   "Deblon, Mary Elizabeth Stanton, and Kim E. "
                   "Barber")],
           [holder("Candace Kadimik", "candace-kadimik"),
            holder("Roger Stevens", "roger-stevens"),
            holder("George J. Deblon", "george-j-deblon"),
            holder("Mary Elizabeth Stanton",
                   "mary-elizabeth-stanton"),
            holder("Kim E. Barber", "kim-e-barber")]),
], jp=jp_election("pittsfield-vt", "Town of Pittsfield", 5,
                  "the certified listing names five winners for "
                  "Pittsfield's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Pittsford (Rutland County) -- general law.
PFORD_MIN_C = ("Town of Pittsford, Selectboard Minutes, March 4, "
               "2026 (pittsfordvermont.com)")
SPECS["pittsford"] = spec("pittsford", "Town of Pittsford", [
    office("moderator", "Town Moderator",
           "Town of Pittsford Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(PFORD_MIN, f"{PFORD_MIN_C}: the March 3, 2026 "
                         "ballot results read into the minutes "
                         "record that Moderator Robb Spensley "
                         "'received enough votes to continue' in "
                         "the office")],
           [holder("Robb Spensley", "robb-spensley")]),
    office("selectboard", "Selectboard Member",
           "Town of Pittsford Selectboard", 5,
           [sb_dir("lists Pittsford's five selectboard members: "
                   "Daniel Adams, Tom Hooker, Alicia Malay "
                   "(Chair), David Mills, and Mark Winslow"),
            S(PFORD_MIN, f"{PFORD_MIN_C}: Mark Winslow was "
                         "elected to a three-year term with 262 "
                         "votes (Erin Eugair 216, write-ins 3) "
                         "and Dan Adams was re-elected to a "
                         "two-year term with 445 votes at the "
                         "March 3, 2026 election")],
           [holder("Daniel Adams", "daniel-adams"),
            holder("Tom Hooker", "tom-hooker"),
            holder("Alicia Malay", "alicia-malay",
                   existing_person_id="ocd-person/5c402261-3cd7-5302-ada8-ee1b6afaad16"),
            holder("David Mills", "david-mills"),
            holder("Mark Winslow", "mark-winslow")]),
    office("town-clerk", "Town Clerk",
           "Town of Pittsford Town Clerk", 1,
           [S(PFORD_WARN, "Town of Pittsford, Town Meeting "
                          "Warning 2026: floor Article 6 asked "
                          "whether the voters would authorize the "
                          "Selectboard to appoint the Town Clerk "
                          "under 17 V.S.A. section 2651e, and "
                          "ballot Article 9 elected a Town Clerk "
                          "for a three-year term"),
            S(PFORD_MIN, f"{PFORD_MIN_C}: the ballot results "
                         "read into the minutes give Dolores "
                         "Gecha 456 votes for Town Clerk; the "
                         "same minutes then record, after "
                         "executive session, that the Selectboard "
                         "appointed Dolores Gecha as Town Clerk "
                         "effective 45 days from the Town "
                         "Meeting election (April 17, 2026) for a "
                         "term of three years. The voters having "
                         "authorized appointment, she holds the "
                         "office by appointment, and she is "
                         "minted appointed; no separate election "
                         "record is created for the office")],
           [holder("Dolores Gecha", "dolores-gecha",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Pittsford Town Treasurer", 1,
           [S(PFORD_WARN, "Town of Pittsford, Town Meeting "
                          "Warning 2026: floor Article 7 asked "
                          "whether the voters would authorize the "
                          "Selectboard to appoint the Town "
                          "Treasurer under 17 V.S.A. section "
                          "2651f, and ballot Article 9 elected a "
                          "Town Treasurer for a three-year term"),
            S(PFORD_MIN, f"{PFORD_MIN_C}: the ballot results "
                         "read into the minutes give the Town "
                         "Treasurer race 457 votes (the results "
                         "line does not repeat the winner's "
                         "name); the same minutes record that "
                         "the Selectboard appointed Dolores Gecha "
                         "as Town Treasurer, with the clerkship, "
                         "effective 45 days from the Town Meeting "
                         "election (April 17, 2026) for a term of "
                         "three years. She is minted appointed")],
           [holder("Dolores Gecha", "dolores-gecha",
                   how_seated="appointed")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Pittsford Trustees of Public Funds", 3,
           [S(PFORD_WARN, "Town of Pittsford, Town Meeting "
                          "Warning 2026: ballot Article 9 elects "
                          "a Trustee of Public Funds for a "
                          "three-year term; one such seat stands "
                          "each year, so the board has three "
                          "seats"),
            S(PFORD_MIN, f"{PFORD_MIN_C}: Dolores Gecha was "
                         "elected Trustee of Public Funds with "
                         "450 votes. The other two seats' "
                         "holders are published in no current "
                         "official source, so they are created "
                         "without memberships")],
           [holder("Dolores Gecha", "dolores-gecha")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Pittsford Collector of Delinquent Taxes", 1,
           [S(PFORD_MIN, f"{PFORD_MIN_C}: the Selectboard's "
                         "annual appointments motion of March 4, "
                         "2026 appoints the Town Manager, Ann "
                         "Reed, as Collector of Delinquent "
                         "Taxes. The office is filled by "
                         "appointment in Pittsford")],
           [holder("Ann Reed", "ann-reed",
                   how_seated="appointed")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Pittsford Justices of the Peace", 12,
           [jp_src("lists twelve Pittsford justices of the "
                   "peace: Charles \"Butch\" Shaw, Matthew "
                   "Candon, Matthew Markowski, Ernie Clerihew, "
                   "Terry Poor, Sue Markowski, Jill Blanchard, "
                   "Bonnie Stewart, Brian Nolan, Bill Drummond, "
                   "Donna Wilson, and Elizabeth Simpson")],
           [holder("Charles Shaw", "charles-shaw",
                   ballot_name='Charles "Butch" Shaw'),
            holder("Matthew Candon", "matthew-candon"),
            holder("Matthew Markowski", "matthew-markowski"),
            holder("Ernie Clerihew", "ernie-clerihew"),
            holder("Terry Poor", "terry-poor"),
            holder("Sue Markowski", "sue-markowski"),
            holder("Jill Blanchard", "jill-blanchard"),
            holder("Bonnie Stewart", "bonnie-stewart"),
            holder("Brian Nolan", "brian-nolan"),
            holder("Bill Drummond", "bill-drummond"),
            holder("Donna Wilson", "donna-wilson"),
            holder("Elizabeth Simpson", "elizabeth-simpson")]),
], jp=jp_election("pittsford-vt", "Town of Pittsford", 12,
                  "the certified listing names twelve winners for "
                  "Pittsford's twelve justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Plainfield (Washington County) -- charter ch. 131.
PLF_RETURN_C = ("Town of Plainfield, Official Return of Votes, "
                "Article III (Election of Officers), Australian "
                "ballot, March 3, 2026, certified by Town Clerk "
                "Jaime Hammack (366 voters checked off the "
                "entrance checklist). The live PDF on the town "
                "website now returns a 404 error; this is the "
                "Wayback Machine's March 5, 2026 capture of the "
                "town's own official return")
SPECS["plainfield"] = spec("plainfield", "Town of Plainfield", [
    office("moderator", "Town Moderator",
           "Town of Plainfield Town Moderator", 1,
           [charter131("section 401 makes the town's officers "
                       "those provided by general law except as "
                       "the charter varies them; the moderator is "
                       "elected for a one-year term"),
            S(PLF_RETURN, f"{PLF_RETURN_C}: Moderator, one "
                          "year -- Donny Osman 298 votes, "
                          "write-ins 13, blanks 55")],
           [holder("Donny Osman", "donny-osman")]),
    office("selectboard", "Selectboard Member",
           "Town of Plainfield Selectboard", 5,
           [sb_dir("lists Plainfield's five selectboard members: "
                   "Karen Hatcher, Patti Jamele, Andy Robinson, "
                   "Frances Subbiondo (Vice Chair), and Peter "
                   "Youngbaer (Chair)"),
            S(PLF_RETURN, f"{PLF_RETURN_C}: Selectboard, three "
                          "years -- Karen Hatcher 194 votes; the "
                          "return itself tallies the write-ins by "
                          "name (Vicki McDonald 143 of 146 total "
                          "write-in votes), and Hatcher is the "
                          "winner. Selectboard, one year -- Andy "
                          "Robinson 290 votes. The other three "
                          "members did not stand in 2026")],
           [holder("Peter Youngbaer", "peter-youngbaer"),
            holder("Frances Rose Subbiondo",
                   "frances-rose-subbiondo"),
            holder("Karen Hatcher", "karen-hatcher"),
            holder("Patti Jamele", "patti-jamele"),
            holder("Andy Robinson", "andy-robinson")]),
    office("town-clerk", "Town Clerk",
           "Town of Plainfield Town Clerk", 1,
           [charter131("section 401 makes the town's officers "
                       "those provided by general law except as "
                       "the charter varies them"),
            S(PLF_OFFICE, "Town of Plainfield, Town Office page "
                          "(plainfieldvt.gov): lists Jaime "
                          "Hammack as Town Clerk"),
            S(PLF_RETURN, f"{PLF_RETURN_C}: the return is "
                          "certified by Jaime Hammack as Town "
                          "Clerk. No clerk race was warned or "
                          "appears on the return: the January "
                          "2026 Guide and the town's 2025 Town "
                          "Report name Bram Towbin as Town Clerk "
                          "(his report calls Hammack the new "
                          "Assistant Town Clerk), so Hammack "
                          "succeeded to a vacancy between the "
                          "report and March 3, 2026 without an "
                          "election; appointment by the "
                          "Selectboard is the only lawful seating "
                          "mechanism, and she is minted appointed "
                          "on that disclosed inference")],
           [holder("Jaime Hammack", "jaime-hammack",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Plainfield Town Treasurer", 1,
           [charter131("section 401 makes the town's officers "
                       "those provided by general law except as "
                       "the charter varies them"),
            S(PLF_OFFICE, "Town of Plainfield, Town Office page "
                          "(plainfieldvt.gov): lists Tammy "
                          "Martel as 'Town Treasurer & Finance "
                          "Director'"),
            S(PLF_RETURN, f"{PLF_RETURN_C}: no treasurer race "
                          "was warned or appears on the return. "
                          "The January 2026 Guide and the 2025 "
                          "Town Report name Josh Pitts as "
                          "Treasurer; Martel succeeded him "
                          "without an election, and she is "
                          "minted appointed on the same disclosed "
                          "inference as the clerkship")],
           [holder("Tammy Martel", "tammy-martel",
                   how_seated="appointed")]),
    office("lister", "Lister",
           "Town of Plainfield Board of Listers", 3,
           [statute2646("towns elect a board of listers of three "
                        "on staggered three-year terms"),
            S(PLF_RETURN, f"{PLF_RETURN_C}: Lister, three "
                          "years -- Jeffrey Slaton 294 votes. "
                          "The other two listers' holders are "
                          "published in no current official "
                          "source, so those seats are created "
                          "without memberships")],
           [holder("Jeffrey Slaton", "jeffrey-slaton")]),
    office("auditor", "Town Auditor",
           "Town of Plainfield Auditors", 3,
           [statute2646("towns elect three auditors"),
            S(PLF_RETURN, f"{PLF_RETURN_C}: Auditor, one year, "
                          "vote for not more than three -- the "
                          "race had NO declared candidates: 7 "
                          "scattered write-in votes and 1,091 "
                          "blank votes, so no winner can be "
                          "recorded and all three seats are "
                          "created without memberships")],
           []),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Plainfield Cemetery Commission", 3,
           [S(PLF_REPORT, "Town of Plainfield, 2025 Town Report, "
                          "Warning for Town Meeting, March 3, "
                          "2026: Article III elects Cemetery "
                          "Commissioners among the town officers"),
            S(PLF_RETURN, f"{PLF_RETURN_C}: Cemetery "
                          "Commissioner, five years, vote for "
                          "not more than three -- the race had "
                          "NO declared candidates: 29 scattered "
                          "write-in votes and 1,069 blank votes, "
                          "so no winner can be recorded and the "
                          "three seats are created without "
                          "memberships")],
           []),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Plainfield Collector of Delinquent Taxes", 1,
           [S(PLF_RETURN, f"{PLF_RETURN_C}: Collector of "
                          "Delinquent Taxes, one year -- George "
                          "C. Cushing 315 votes")],
           [holder("George C. Cushing", "george-c-cushing")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Plainfield Justices of the Peace", 7,
           [jp_src("lists seven Plainfield justices of the "
                   "peace: Carolyn \"Becky\" Atchinson, Dale "
                   "Bartlett, Charles Cogbill, Steven Farnham, "
                   "Mary R. Niebling, Anne Van Couvering, and "
                   "Peter Youngbaer")],
           [holder("Carolyn Atchinson", "carolyn-atchinson",
                   ballot_name='Carolyn "Becky" Atchinson'),
            holder("Dale Bartlett", "dale-bartlett"),
            holder("Charles Cogbill", "charles-cogbill"),
            holder("Steven Farnham", "steven-farnham"),
            holder("Mary R. Niebling", "mary-r-niebling"),
            holder("Anne Van Couvering", "anne-van-couvering"),
            holder("Peter Youngbaer", "peter-youngbaer")]),
], jp=jp_election("plainfield-vt", "Town of Plainfield", 7,
                  "the certified listing names seven winners for "
                  "Plainfield's seven justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Pomfret (Windsor County) -- general law.
POM_RESULTS_C = ("Town of Pomfret, Official Results, Australian "
                 "Ballot, March 3, 2026 (pomfretvt.us)")
POM_REPORT_C = ("Town of Pomfret, 2025 Town Report (pomfretvt.us): "
                "the report's town officers table")
SPECS["pomfret"] = spec("pomfret", "Town of Pomfret", [
    office("moderator", "Town Moderator",
           "Town of Pomfret Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(POM_RESULTS, f"{POM_RESULTS_C}: Moderator -- Kevin "
                           "Geiger 344 votes")],
           [holder("Kevin Geiger", "kevin-geiger")]),
    office("town-clerk", "Town Clerk",
           "Town of Pomfret Town Clerk", 1,
           [S(POM_RESULTS, f"{POM_RESULTS_C}: Town Clerk -- "
                           "Rebecca Fielder 356 votes"),
            guide("lists Rebecca Fielder as Pomfret's Town "
                  "Clerk")],
           [holder("Rebecca Fielder", "rebecca-fielder")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Pomfret Town Treasurer", 1,
           [S(POM_RESULTS, f"{POM_RESULTS_C}: 'Town Treasurer & "
                           "Tax Collector' -- Ellen DesMeules 337 "
                           "votes. Pomfret's delinquent-tax "
                           "collection is handled by an appointee "
                           "(see the town officers page), so no "
                           "separate collector post is created"),
            guide("lists Ellen DesMeules as Pomfret's Town "
                  "Treasurer")],
           [holder("Ellen DesMeules", "ellen-desmeules")]),
    office("selectboard", "Selectboard Member",
           "Town of Pomfret Selectboard", 5,
           [sb_dir("lists Pomfret's five selectboard members as "
                   "of June 2026: Benjamin Brickner, Steven "
                   "Chamberlin, Emily Grube, John Peters Jr., and "
                   "Marjorie Wakefield"),
            S(POM_RESULTS, f"{POM_RESULTS_C}: Selectboard, three "
                           "years -- Benjamin Brickner 318 "
                           "votes; Selectboard, two years -- "
                           "Marjorie Wakefield 327 votes"),
            S(POM_SB, "Town of Pomfret, Selectboard page "
                      "(pomfretvt.us): lists the current board "
                      "as Benjamin Brickner (Chair), John Peters "
                      "Jr. (Vice Chair), Emily Grube, Eric "
                      "Chase, and Kyle Hansen. Wakefield died in "
                      "May 2026 and the Selectboard appointed "
                      "Eric Chase to her seat; Steven Chamberlin "
                      "resigned effective June 18, 2026 and Kyle "
                      "Hansen was appointed to his seat. Neither "
                      "Wakefield nor Chamberlin holds a seat "
                      "now, and Wakefield is minted nowhere "
                      "(see the justice of the peace election "
                      "note)")],
           [holder("Benjamin Brickner", "benjamin-brickner"),
            holder("John Peters Jr.", "john-peters-jr"),
            holder("Emily Grube", "emily-grube"),
            holder("Eric Chase", "eric-chase",
                   how_seated="appointed"),
            holder("Kyle Hansen", "kyle-hansen",
                   how_seated="appointed")]),
    office("lister", "Lister",
           "Town of Pomfret Board of Listers", 3,
           [statute2646("towns elect a board of listers of three "
                        "on staggered three-year terms"),
            S(POM_RESULTS, f"{POM_RESULTS_C}: Lister, three "
                           "years -- Neil Lamson 329 votes; "
                           "Lister, to finish a term -- Norman "
                           "Buchanan 325 votes (Buchanan had been "
                           "appointed to the vacant seat in 2025 "
                           "and now holds it by election)"),
            S(POM_REPORT, f"{POM_REPORT_C} lists the third "
                          "lister as Rebecca Fielder, who also "
                          "serves as Town Clerk")],
           [holder("Neil Lamson", "neil-lamson"),
            holder("Norman Buchanan", "norman-buchanan"),
            holder("Rebecca Fielder", "rebecca-fielder")]),
    office("auditor", "Town Auditor",
           "Town of Pomfret Auditors", 3,
           [statute2646("towns elect three auditors on staggered "
                        "three-year terms"),
            S(POM_RESULTS, f"{POM_RESULTS_C}: the Auditor races "
                           "for three-year, two-year, and "
                           "one-year terms had NO declared "
                           "candidates (write-ins 8, 7, and 4; "
                           "blanks about 355 in each)"),
            S(POM_AUD, "Town of Pomfret, Auditors page "
                       "(pomfretvt.us): the page states the "
                       "auditor seats are 'VACANT - please contact "
                       "the Selectboard if you are interested in "
                       "serving the Town as an appointed "
                       "Auditor'. All three seats are created "
                       "without memberships")],
           []),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Pomfret Cemetery Commission", 3,
           [S(POM_RESULTS, f"{POM_RESULTS_C}: Cemetery "
                           "Commissioner, three years -- Susan "
                           "Burgess 338 votes"),
            S(POM_REPORT, f"{POM_REPORT_C} lists cemetery "
                          "commissioners Susan Burgess (Chair), "
                          "Greg Greene, and Bruce Tuthill")],
           [holder("Susan Burgess", "susan-burgess"),
            holder("Greg Greene", "greg-greene"),
            holder("Bruce Tuthill", "bruce-tuthill")]),
    office("library-trustee", "Library Trustee",
           "Pomfret Public Library Trustees", 6,
           [S(POM_REPORT, f"{POM_REPORT_C} lists six library "
                          "trustees; the 2026 warning stood two "
                          "three-year seats, one two-year seat to "
                          "finish a term, and the remaining seats"),
            S(POM_RESULTS, f"{POM_RESULTS_C}: Library Trustee, "
                           "two years to finish a term -- Heather "
                           "Durkel 325 votes. The two three-year "
                           "seats had NO declared candidates, so "
                           "they are created without memberships; "
                           "the seats were held by Douglas Abbott "
                           "and Betsy Rhodes")],
           [holder("Heather Durkel", "heather-durkel"),
            holder("James Robinson", "james-robinson"),
            holder("Mary Worrell", "mary-worrell"),
            holder("Jocelyn Randles", "jocelyn-randles")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Pomfret Trustees of Public Funds", 3,
           [statute2646("towns that hold trust funds elect "
                        "trustees of public funds"),
            S(POM_RESULTS, f"{POM_RESULTS_C}: Trustee of Public "
                           "Funds, three years -- Marjorie "
                           "Wakefield 326 votes. Wakefield died "
                           "in May 2026, so her seat is created "
                           "without a membership"),
            S(POM_REPORT, f"{POM_REPORT_C} lists trustees of "
                          "public funds Robert Coates, Michael "
                          "Doten, and Marjorie Wakefield")],
           [holder("Robert Coates", "robert-coates"),
            holder("Michael Doten", "michael-doten")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Pomfret Justices of the Peace", 5,
           [jp_src("lists five Pomfret justices of the peace: "
                   "Anne Bower, Michael Doten, Charles "
                   "Gundersen, James Robinson, and Marjorie "
                   "Wakefield. Four are minted; Wakefield died "
                   "in May 2026 (see the election note), so her "
                   "seat stands vacant. The town report's "
                   "officers table styles Gundersen 'Chuck "
                   "Gundersen' and Robinson 'Jim Robinson'")],
           [holder("Anne Bower", "anne-bower"),
            holder("Michael Doten", "michael-doten"),
            holder("Charles Gundersen", "charles-gundersen"),
            holder("James Robinson", "james-robinson")]),
], jp=jp_election("pomfret-vt", "Town of Pomfret", 5,
                  "the certified listing names five winners for "
                  "Pomfret's five justice of the peace seats: "
                  "Anne Bower, Michael Doten, Charles Gundersen, "
                  "James Robinson, and Marjorie Wakefield. The "
                  "listing publishes no vote totals or party "
                  "labels and none are recorded. Wakefield died "
                  "in May 2026 (she had also been elected to the "
                  "Selectboard and as a Trustee of Public Funds "
                  "in March 2026), so no person or membership is "
                  "minted for her and her seats stand vacant; "
                  "the four surviving winners are recorded here"))

# ----------------------------------------------------------------
# Town of Poultney (Rutland County) -- charter ch. 133.
POU_REPORT_C = ("Town of Poultney, 2025 Town Report "
                "(poultneyvt.gov), 'Elected Town Officers' table "
                "submitted by Betsy J. Wescott, Town Clerk")
POU_SB_C = ("Town of Poultney, Selectboard page (poultneyvt.gov): "
            "the current board roster with term expirations")
SPECS["poultney-56875"] = spec("poultney-56875", "Town of Poultney", [
    office("moderator", "Town Moderator",
           "Town of Poultney Town Moderator", 1,
           [charter133("section 304 provides for a Moderator "
                       "elected for a one-year term"),
            S(POU_REPORT, f"{POU_REPORT_C} lists Moderator Jaime "
                          "Lee with a one-year term expiring on "
                          "Town Meeting Day 2026. No official "
                          "source publishes the 2026 moderator "
                          "outcome, so the post is created "
                          "without a membership")],
           []),
    office("selectboard", "Selectboard Member",
           "Town of Poultney Selectboard", 5,
           [charter133("section 303: the Selectboard has five "
                       "members -- three on staggered three-year "
                       "terms and two on one-year terms"),
            sb_dir("lists Poultney's five selectboard members: "
                   "Valerie Broughton, Alan-Glen Burnell (Vice "
                   "Chair), John \"Jay\" Morgan, Sheryl Porrier "
                   "(Chair), and Abigail Teetor"),
            S(POU_SB, f"{POU_SB_C} lists Sheryl Porrier (Chair, "
                      "term to 2029 -- she won the three-year "
                      "seat in 2026), Alan-Glen Burnell (Vice "
                      "Chair, 2028), Abigail Teetor (2027), Jay "
                      "Morgan (2027), and one seat 'Vacant' "
                      "(2027)"),
            S(POU_VACANCY, "Town of Poultney, 'Selectboard Notice "
                           "of Vacancy -- September 2026': the "
                           "town sought letters of interest (due "
                           "September 21, 2026) to fill a "
                           "Selectboard vacancy 'for the remainder "
                           "of a term ending on March 2, 2027' -- "
                           "Valerie Broughton's three-year seat; "
                           "the seat was still shown vacant on "
                           "the board page when read, so it is "
                           "created without a membership")],
           [holder("Sheryl Porrier", "sheryl-porrier"),
            holder("Alan-Glen Burnell", "alan-glen-burnell"),
            holder("Jay Morgan", "jay-morgan"),
            holder("Abigail Teetor", "abigail-teetor")]),
    office("town-clerk", "Town Clerk",
           "Town of Poultney Town Clerk", 1,
           [charter133("section 304(a): the Town Clerk is "
                       "elected for a three-year term"),
            S(POU_REPORT, f"{POU_REPORT_C} lists Town Clerk "
                          "Betsy J. Wescott with a three-year "
                          "term expiring on Town Meeting Day "
                          "2026"),
            S(POU_CLERK, "Town of Poultney, Town Clerk & "
                         "Treasurer page (poultneyvt.gov): the "
                         "town's current page for the office "
                         "names Betsy Wescott. Her terms expired "
                         "in 2026 and the town presents her as "
                         "the sitting clerk; she is recorded as "
                         "re-elected on this incumbent-continuity "
                         "reading, disclosed on issue #163")],
           [holder("Betsy Wescott", "betsy-wescott")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Poultney Town Treasurer", 1,
           [charter133("section 304(d): the Town Treasurer is "
                       "elected for a three-year term"),
            S(POU_REPORT, f"{POU_REPORT_C} lists Town Treasurer "
                          "Betsy J. Wescott with a three-year "
                          "term expiring on Town Meeting Day "
                          "2026"),
            S(POU_CLERK, "Town of Poultney, Town Clerk & "
                         "Treasurer page (poultneyvt.gov): the "
                         "town's current page for the office "
                         "names Betsy Wescott; she is recorded "
                         "as re-elected on the same "
                         "incumbent-continuity reading as the "
                         "clerkship")],
           [holder("Betsy Wescott", "betsy-wescott")]),
    office("library-trustee", "Library Trustee",
           "Poultney Public Library Trustees", 5,
           [charter133("sections 302(1) and 304(c): five library "
                       "trustees on five-year terms, one elected "
                       "each year"),
            S(POU_REPORT, f"{POU_REPORT_C} lists library "
                          "trustees Jean S. Davis (term to "
                          "2027), D. Bruce Williams (2028), Ennis "
                          "Duling (2029), Nancy Luzer (2030), and "
                          "Emily Sosnoff (2026). The seat that "
                          "stood in 2026 (Sosnoff's) has no "
                          "published outcome, so it is created "
                          "without a membership")],
           [holder("Jean Davis", "jean-davis"),
            holder("Bruce Williams", "bruce-williams"),
            holder("Ennis Duling", "ennis-duling"),
            holder("Nancy Luzer", "nancy-luzer")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Poultney Justices of the Peace", 12,
           [jp_src("lists twelve Poultney justices of the peace: "
                   "Carol A. Bunce, Barbara Bunce Betit, Richard "
                   "Rupe, Eric Hier, Joseph DeBonis, Jr., Dick "
                   "Gray, Bonnie Gray, Mark Teetor, Andrew Ohl, "
                   "Alan-Glen Burnell, Susan Kasuba, and Kathleen "
                   "Hutson")],
           [holder("Carol A. Bunce", "carol-a-bunce"),
            holder("Barbara Bunce Betit", "barbara-bunce-betit"),
            holder("Richard Rupe", "richard-rupe"),
            holder("Eric Hier", "eric-hier"),
            holder("Joseph DeBonis Jr.", "joseph-debonis-jr",
                   ballot_name="Joseph DeBonis, Jr."),
            holder("Dick Gray", "dick-gray"),
            holder("Bonnie Gray", "bonnie-gray"),
            holder("Mark Teetor", "mark-teetor"),
            holder("Andrew Ohl", "andrew-ohl"),
            holder("Alan-Glen Burnell", "alan-glen-burnell"),
            holder("Susan Kasuba", "susan-kasuba"),
            holder("Kathleen Hutson", "kathleen-hutson")]),
], jp=jp_election("poultney-56875-vt", "Town of Poultney", 12,
                  "the certified listing names twelve winners "
                  "for Poultney's twelve justice of the peace "
                  "seats"))

# ----------------------------------------------------------------
# Village of Poultney (Rutland County) -- charter ch. 269.
SPECS["poultney"] = spec("poultney", "Village of Poultney", [
    office("village-president", "Village President",
           "Village of Poultney Village President", 1,
           [charter269("sections 302(a) and 303(b): a Village "
                       "President is elected at the annual "
                       "village meeting from among the trustees, "
                       "and under section 502(d) the President "
                       "is chairman of the Board of Trustees; "
                       "under section 302(d) the President also "
                       "serves as Village Moderator, so no "
                       "separate moderator post is created. The "
                       "only roster naming a president rests on "
                       "a restricted clerk reply and a second "
                       "public source styles the same man "
                       "Vice-Chair, so the post is created "
                       "without a membership")],
           []),
    office("village-trustee", "Village Trustee",
           "Village of Poultney Board of Trustees", 5,
           [charter269("section 303: five trustees, two elected "
                       "each year to two-year terms"),
            S(CGR_STEERING, "Town and Village of Poultney Merger "
                            "Study, Project Steering Committee "
                            "page (CGR, the municipalities' "
                            "merger-study consultant): lists 'Joe "
                            "DeBonis, Village Trustees, "
                            "Vice-Chair', 'Idris Atwood, Village "
                            "Trustees', and 'Gerri Harrison, "
                            "Village Trustees' as the village's "
                            "representatives, corroborating the "
                            "three as sitting trustees in 2026. "
                            "Two further trustees (Bonnie Gray "
                            "and Ben Worthing) rest only on a "
                            "restricted clerk-reply roster, so "
                            "their seats are created without "
                            "memberships; the minting of the "
                            "three corroborated trustees as "
                            "elected is flagged on issue #163")],
           [holder("Joseph DeBonis Jr.", "joseph-debonis-jr",
                   person_scope="poultney-56875"),
            holder("Idris Atwood", "idris-atwood"),
            holder("Gerri Harrison", "gerri-harrison")]),
    office("village-clerk-treasurer", "Village Clerk/Treasurer",
           "Village of Poultney Village Clerk/Treasurer", 1,
           [charter269("sections 302(a) and 304(a): a single "
                       "combined Village Clerk/Treasurer office, "
                       "elected for a one-year term. The only "
                       "source naming the current holder rests "
                       "on a restricted clerk reply, so the post "
                       "is created without a membership")],
           []),
    office("village-auditor", "Village Auditor",
           "Village of Poultney Auditors", 3,
           [charter269("section 304(b): three auditors on "
                       "staggered three-year terms, one elected "
                       "each year. No official source publishes "
                       "the current holders, so the post is "
                       "created without memberships")],
           []),
])

# ----------------------------------------------------------------
# Town of Pownal (Bennington County) -- general law.
POWNAL_REPORT_C = ("Town of Pownal, 2025 Town Report "
                   "(townofpownal.org)")
SPECS["pownal"] = spec("pownal", "Town of Pownal", [
    office("moderator", "Town Moderator",
           "Town of Pownal Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(POWNAL_REPORT, f"{POWNAL_REPORT_C}: the Elected "
                             "Officials table lists Moderator "
                             "Tim Holbrook with a term expiring "
                             "2026, and the 2026 Warning "
                             "(Article 4) stood a one-year "
                             "moderator seat. No official source "
                             "publishes the 2026 outcome, so the "
                             "post is created without a "
                             "membership")],
           []),
    office("selectboard", "Selectboard Member",
           "Town of Pownal Selectboard", 5,
           [sb_dir("lists Pownal's five selectboard members: "
                   "Jeanie Alexander, Michael Gardner, Harry "
                   "(Jamie) Percey, Karl Strohmaier, and Julie "
                   "Weber"),
            S(POWNAL_REPORT, f"{POWNAL_REPORT_C}: the Elected "
                             "Officials table lists Karl "
                             "Strohmaier (term to 2027), Mike "
                             "Gardner (2026), Bryan Haris (2026), "
                             "Jeannie Alexander (2026), and "
                             "Harry 'Jamie' Percy (2028); the "
                             "2026 Warning stood two one-year "
                             "seats and one three-year seat. Read "
                             "against the June 2026 directory, "
                             "Gardner took the three-year seat, "
                             "Alexander was re-elected, Bryan "
                             "Harris departed, and Town Clerk "
                             "Julie Weber took the second "
                             "one-year seat while remaining Town "
                             "Clerk. The directory's name forms "
                             "govern over the report's looser "
                             "spellings")],
           [holder("Jeanie Alexander", "jeanie-alexander"),
            holder("Michael Gardner", "michael-gardner"),
            holder("Harry (Jamie) Percey Jr",
                   "harry-jamie-percey-jr"),
            holder("Karl Strohmaier", "karl-strohmaier"),
            holder("Julie Weber", "julie-weber")]),
    office("town-clerk", "Town Clerk",
           "Town of Pownal Town Clerk", 1,
           [S(POWNAL_REPORT, f"{POWNAL_REPORT_C}: the Elected "
                            "Officials table lists Town Clerk "
                            "Julie Weber with a three-year term "
                            "expiring 2027; the seat did not stand "
                            "in 2026"),
            guide("lists Julie Weber as Pownal's Town Clerk"),
            S(POWNAL_CONTACTS, "Town of Pownal, Town Contacts "
                               "page (townofpownal.org): lists "
                               "Julie Weber as Town Clerk, 'term "
                               "expires in 2027'")],
           [holder("Julie Weber", "julie-weber")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Pownal Town Treasurer", 1,
           [S(POWNAL_REPORT, f"{POWNAL_REPORT_C}: the Elected "
                            "Officials table lists Treasurer "
                            "Ellen Strohmaier with a three-year "
                            "term expiring 2027; the seat did not "
                            "stand in 2026"),
            guide("lists Ellen Strohmaier as Pownal's Town "
                  "Treasurer")],
           [holder("Ellen Strohmaier", "ellen-strohmaier")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Pownal Collector of Delinquent Taxes", 1,
           [S(POWNAL_REPORT, f"{POWNAL_REPORT_C}: the Elected "
                            "Officials table lists Delinquent "
                            "Tax Collector Ellen Strohmaier with "
                            "a three-year term expiring 2026, "
                            "and the 2026 Warning (Article 4) "
                            "stood the office for a three-year "
                            "term"),
            S(POWNAL_CONTACTS, "Town of Pownal, Town Contacts "
                               "page (townofpownal.org): the "
                               "town's current page lists Ellen "
                               "Strohmaier as 'Treasurer/Del Tax "
                               "Collector'. Her term expired in "
                               "2026 and the town presents her as "
                               "the sitting collector; she is "
                               "recorded as re-elected on this "
                               "incumbent-continuity reading, "
                               "disclosed on issue #163")],
           [holder("Ellen Strohmaier", "ellen-strohmaier")]),
    office("constable", "Constable",
           "Town of Pownal Constable", 1,
           [S(POWNAL_REPORT, f"{POWNAL_REPORT_C}: the Elected "
                            "Officials table lists Constable "
                            "Eddie Pascucci with a term expiring "
                            "2027, and the report's March 2025 "
                            "local election results record his "
                            "election as Constable with 38 votes. "
                            "The office did not stand in 2026 "
                            "(the results print the term as three "
                            "years and the table as two; the "
                            "inconsistency is the town's and is "
                            "immaterial to the holding")],
           [holder("Eddie Pascucci", "eddie-pascucci")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Pownal Trustees of Public Funds", 2,
           [S(POWNAL_REPORT, f"{POWNAL_REPORT_C}: the 2026 "
                            "Warning (Article 4) elects two "
                            "Trustees of Public Monies to "
                            "one-year positions, and the report's "
                            "March 2025 results show the office "
                            "filled by an unnamed write-in (35 "
                            "votes). No holder's name is "
                            "published in any official source, so "
                            "both seats are created without "
                            "memberships")],
           []),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Pownal Cemetery Commission", 3,
           [S(POWNAL_REPORT, f"{POWNAL_REPORT_C}: at the 2025 "
                            "town meeting the voters approved "
                            "Article 5 (293-128), placing the "
                            "town's public burial grounds under "
                            "a cemetery commission of three "
                            "commissioners under 18 V.S.A. "
                            "section 5373; the 2026 Warning "
                            "(Article 4) stood the commission's "
                            "initial staggered seats (three-year, "
                            "two-year, and one-year terms). No "
                            "holder's name is published in any "
                            "official source, so all three seats "
                            "are created without memberships")],
           []),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Pownal Justices of the Peace", 12,
           [jp_src("lists twelve Pownal justices of the peace: "
                   "Alonzo Bisson, Cindy Brownell, Bryan Harris, "
                   "Harry Percey Sr., Megan Randall, Olden Dwyer, "
                   "Nelson Brownell, Leslie Morgenthal, Harry "
                   "(Jamie) Percey Jr, James (Jim) Winchester, "
                   "David Low, and Zachary (Zach) Rose. The "
                   "listing itself distinguishes Harry Percey Sr. "
                   "(a justice only) from Harry (Jamie) Percey Jr "
                   "(a justice and the selectboard member) -- two "
                   "people. Bryan Harris remains a justice "
                   "although he has left the Selectboard")],
           [holder("Alonzo Bisson", "alonzo-bisson"),
            holder("Cindy Brownell", "cindy-brownell"),
            holder("Bryan Harris", "bryan-harris"),
            holder("Harry Percey Sr.", "harry-percey-sr"),
            holder("Megan Randall", "megan-randall"),
            holder("Olden Dwyer", "olden-dwyer"),
            holder("Nelson Brownell", "nelson-brownell"),
            holder("Leslie Morgenthal", "leslie-morgenthal"),
            holder("Harry (Jamie) Percey Jr",
                   "harry-jamie-percey-jr"),
            holder("James Winchester", "james-winchester",
                   ballot_name="James (Jim) Winchester"),
            holder("David Low", "david-low"),
            holder("Zachary Rose", "zachary-rose",
                   ballot_name="Zachary (Zach) Rose")]),
], jp=jp_election("pownal-vt", "Town of Pownal", 12,
                  "the certified listing names twelve winners "
                  "for Pownal's twelve justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Plymouth (Windsor County) -- general law.
# The results URL was located on the town's own Elections page
# (via the site's WordPress API) and the certified return was read
# firsthand 2026-10-19; every officer figure in the delegated
# transcription matched it exactly.
PLY_RESULTS_URL = ("https://www.plymouthvt.org/wp-content/uploads"
                   "/2026/03/Local-Results-March-3-2026-1.pdf")
PLY_RESULTS_C = ("Town of Plymouth, 'Local Results - March 3, "
                 "2026', the official return of votes for the "
                 "March 3, 2026 local election, certified by Town "
                 "Clerk Angela Kissell (173 ballots counted), as "
                 "published on the town website")
PLY_OFFICIALS_C = ("Town of Plymouth, Elected Town Officials page "
                   "(plymouthvt.org)")
SPECS["plymouth"] = spec("plymouth", "Town of Plymouth", [
    office("moderator", "Town Moderator",
           "Town of Plymouth Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            {"url": PLY_RESULTS_URL,
             "note": f"{PLY_RESULTS_C}: Town Moderator, one "
                     "year -- Thomas W. Harris 152 votes"}],
           [holder("Thomas W. Harris", "thomas-w-harris")]),
    office("selectboard", "Selectboard Member",
           "Town of Plymouth Selectboard", 3,
           [{"url": PLY_RESULTS_URL,
             "note": f"{PLY_RESULTS_C}: Selectperson, three "
                     "years -- Jay Kullman 155 votes"},
            S(PLY_OFFICIALS, f"{PLY_OFFICIALS_C}: lists the "
                             "Selectmen as Jay Kullman (Chair, "
                             "term expiring 2026), Rick Kaminski "
                             "(2028), and KT Cappellini (2027). "
                             "The 2026 warning is signed Jay "
                             "Kullman, Chairman; Richard Kaminski, "
                             "Vice-Chair; and Keith Cappellini, "
                             "and the town homepage names the "
                             "board as Keith Cappellini, Rick "
                             "Kaminski, and Jay Kullman; the "
                             "fuller signature forms are used "
                             "for the person records"),
            S(PLY_WARNINGS, "Town of Plymouth, Warnings page "
                            "(plymouthvt.org): the 2026 annual "
                            "town meeting warning (signed January "
                            "20, 2026) warned the March 2, 2026 "
                            "meeting, with Australian ballot "
                            "polls on March 3, 2026")],
           [holder("Jay Kullman", "jay-kullman"),
            holder("Richard Kaminski", "richard-kaminski"),
            holder("Keith Cappellini", "keith-cappellini")]),
    office("town-clerk", "Town Clerk",
           "Town of Plymouth Town Clerk", 1,
           [S(PLY_OFFICERS, "Town of Plymouth, Town Officers / "
                            "Appointments page (plymouthvt.org): "
                            "lists 'Town Clerk & Treasurer: "
                            "Angela Kissell' among the town's "
                            "appointed/hired officers; no clerk "
                            "appears in the town's elected-"
                            "officials table and no clerk race "
                            "was warned in 2026, so she holds the "
                            "office by appointment"),
            guide("lists Angela Kissell as Plymouth's Town "
                  "Clerk")],
           [holder("Angela Kissell", "angela-kissell",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Plymouth Town Treasurer", 1,
           [S(PLY_OFFICERS, "Town of Plymouth, Town Officers / "
                            "Appointments page (plymouthvt.org): "
                            "lists the combined 'Town Clerk & "
                            "Treasurer' office, held by Angela "
                            "Kissell, among the appointed/hired "
                            "officers; the January 2026 Guide's "
                            "treasurer, Cherry Nicoll, no longer "
                            "holds the office"),
            guide("lists Cherry Nicoll as Plymouth's Town "
                  "Treasurer (January 2026); superseded by the "
                  "town's current officers page")],
           [holder("Angela Kissell", "angela-kissell",
                   how_seated="appointed")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Plymouth Trustees of Public Funds", 3,
           [statute2646("towns that hold trust funds elect "
                        "trustees of public funds"),
            {"url": PLY_RESULTS_URL,
             "note": f"{PLY_RESULTS_C}: Trustee of Public Funds, "
                     "three years -- Shawn W. Bemis 150 votes"},
            S(PLY_OFFICIALS, f"{PLY_OFFICIALS_C}: lists Trustees "
                             "of Public Funds Andrew Crossman "
                             "(term to 2027), Shawn Bemis (2026), "
                             "and Bobbie Jean Lambert-Lynds "
                             "(2028)")],
           [holder("Shawn Bemis", "shawn-bemis"),
            holder("Andrew Crossman", "andrew-crossman"),
            holder("Bobbie Jean Lambert-Lynds",
                   "bobbie-jean-lambert-lynds")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Plymouth Cemetery Commission", 3,
           [{"url": PLY_RESULTS_URL,
             "note": f"{PLY_RESULTS_C}: Cemetery Commissioner, "
                     "three years -- Andrew M. Crossman 163 "
                     "votes"},
            S(PLY_OFFICIALS, f"{PLY_OFFICIALS_C}: lists Cemetery "
                             "Commissioners Andrew Crossman (term "
                             "to 2026), William Lambert (2027), "
                             "and Michael Pierson (2028)")],
           [holder("Andrew Crossman", "andrew-crossman"),
            holder("William Lambert", "william-lambert"),
            holder("Michael Pierson", "michael-pierson")]),
    office("first-constable", "First Constable",
           "Town of Plymouth First Constable", 1,
           [{"url": PLY_RESULTS_URL,
             "note": f"{PLY_RESULTS_C}: First Constable, two "
                     "years -- Stephanie Seavy 138 votes"},
            S(PLY_OFFICIALS, f"{PLY_OFFICIALS_C}: lists First "
                             "Constable Stephanie Seavy (term to "
                             "2026)")],
           [holder("Stephanie Seavy", "stephanie-seavy")]),
    office("second-constable", "Second Constable",
           "Town of Plymouth Second Constable", 1,
           [{"url": PLY_RESULTS_URL,
             "note": f"{PLY_RESULTS_C}: Second Constable, two "
                     "years -- Josh Linton 135 votes. The "
                     "town's elected-officials table omits the "
                     "Second Constable, but the 2026 warning "
                     "warned 'Constables' and the certified "
                     "return elects one, so the post is "
                     "created"}],
           [holder("Josh Linton", "josh-linton")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Plymouth Justices of the Peace", 5,
           [jp_src("lists five Plymouth justices of the peace: "
                   "Steven Radonis, Karen Evans, Richard "
                   "Olmstead, Chase Morsey III, and Shawn Bemis. "
                   "The town's elected-officials table names a "
                   "different five (Bruce Pauley, Chase Morsey, "
                   "Karen Evans, Justus Pingree, and Mary "
                   "Morsey) -- an equal-count name-swap, so the "
                   "certified listing governs and the "
                   "town-only names are held")],
           [holder("Steven Radonis", "steven-radonis"),
            holder("Karen Evans", "karen-evans"),
            holder("Richard Olmstead", "richard-olmstead"),
            holder("Chase Morsey III", "chase-morsey-iii"),
            holder("Shawn Bemis", "shawn-bemis")]),
], jp=jp_election("plymouth-vt", "Town of Plymouth", 5,
                  "the certified listing names five winners for "
                  "Plymouth's five justice of the peace seats"))

ORDER = ["peacham", "peru", "pittsfield", "pittsford",
         "plainfield", "plymouth", "pomfret", "poultney-56875",
         "poultney", "pownal"]

for slug in ORDER:
    (OUT / f"{slug}.json").write_text(
        json.dumps(SPECS[slug], indent=1) + "\n")
print("wrote", len(ORDER), "specs")
