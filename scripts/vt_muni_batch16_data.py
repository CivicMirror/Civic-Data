#!/usr/bin/env python3
"""Batch 16 of the VT #163 municipal fan-out (alphabetical positions
150-159): New Haven, Newark, Newbury (town), Newbury (village),
Newfane (town), Newfane (village), Newport (town), Newport (city),
North Bennington (village), North Hero. Emits one JSON spec per
municipality for build_vt_municipality.py. Research:
vt_muni_batch16_research.md.

Identity calls baked into this batch (all flagged on #163):
- New Haven Justice of the Peace and Moderator Pam Marsh IS the
  Addison Probate District's Judge of Probate already in the
  repo (ocd-person/2ffc7639-ae1f-55ab-bdac-a5601b516a20) --
  Addison County's probate judge resident in New Haven, which is
  in Addison County; her record is reused and her JP candidacy
  appended by hand.
- Newfane Town Treasurer/Collector Melissa Brown is a THIRD
  person of that name in the build (Windham County), distinct
  from Brookline's treasurer and Londonderry's justice of the
  peace; her person file takes the collision suffix.
- Newport City Council President Alissa Finegan is recorded
  under that name per the Secretary of State's directory; the
  city report and her city email use her used name "Carter
  Finegan" (stated in the note).
- Newport City council member John Monette is recorded
  re-elected: his seat stood at the March 2026 election and the
  post-election city council page and June 2026 SOS directory
  both present him as seated. Council member Sharon Pare, who
  appears in the same listings in the departed Kevin
  Charboneau's place, is NOT minted -- no official source
  states how she was seated (election outcome and any
  appointment are both unpublished).
- North Bennington trustee David Shaughnessey's spelling
  follows the village's March 19, 2026 oath minutes (the June
  minutes print "Shaughnessy"; the factory prints
  "Shughnessey"); Village Clerk Lori Elwell's full name is
  Lorine Elwell (the oath line and her signature).
- North Hero selectboard member Claire Lavoie's spelling
  follows the SOS directory and the town's term table (the
  town's selectboard page prints "Clair LaVoie"); its
  selectboard member recorded as Joe Latimer is listed in the
  town's term table as "Roland (Joe) Latimer II."
- Newbury Village and Newfane Village are structure-only
  charter builds (ch. 247 and ch. 249): no official source
  publishes their current holders, and the factory's Newfane
  Village roster is lead-only and insufficiently corroborated.
- Newport Town's site (townofnewport.org) is intermittently
  unreachable firsthand (repeated origin timeouts); its spec
  rests on a scoped read of the town's own pages (selectboard
  page, 2026 warning, 2024 annual report) cross-checked
  against the SOS spine, as disclosed in the research file.
  The town page's Jerry Waterman governs the selectboard's
  third seat over the June directory's Karen Camber.
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
CHARTER_007 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/007",
    "note": "PLACEHOLDER",
}
CHARTER_247 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/247",
    "note": "PLACEHOLDER",
}
CHARTER_249 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/249",
    "note": "PLACEHOLDER",
}
CHARTER_251 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/251",
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


def charter007(phrase):
    return S(CHARTER_007, f"24 App. V.S.A. ch. 007 (City of "
             f"Newport): {phrase}")


def charter247(phrase):
    return S(CHARTER_247, f"24 App. V.S.A. ch. 247 (Village of "
             f"Newbury): {phrase}")


def charter249(phrase):
    return S(CHARTER_249, f"24 App. V.S.A. ch. 249 (Village of "
             f"Newfane): {phrase}")


def charter251(phrase):
    return S(CHARTER_251, f"24 App. V.S.A. ch. 251 (Village of "
             f"North Bennington): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 16); issue #163 "
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
                  f"# municipal fan-out batch 16; issue #163 "
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
ORDER = ["new-haven", "newark", "newbury-48175", "newbury",
         "newfane-48400", "newfane", "newport-48925", "newport",
         "north-bennington", "north-hero"]

# ------------------------------------------------------------ New Haven
NH_SB = {
    "url": "https://www.newhavenvt.com/selectboard",
    "note": "PLACEHOLDER",
}
NH_REPORTS = {
    "url": "https://www.newhavenvt.com/town-reports",
    "note": "PLACEHOLDER",
}
NH_ELECTIONS = {
    "url": "https://www.newhavenvt.com/elections",
    "note": "PLACEHOLDER",
}


def nh_sb(what):
    return S(NH_SB, "Town of New Haven (official website), "
             f"Selectboard page: {what}")


def nh_reports(what):
    return S(NH_REPORTS, "Town of New Haven (official website), "
             f"Town Reports page: {what}")


def nh_elections(what):
    return S(NH_ELECTIONS, "Town of New Haven (official website), "
             f"Elections page: {what}")


def new_haven_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "New Haven Selectboard", 5,
               [nh_sb("lists the five-member selectboard as John "
                      "Roleau (Chair), Marie Jewett, Mike Audy, "
                      "Bruce Many (Vice Chair), and Shauntell "
                      "Barnum, printing a two-year term ending "
                      "2028 for Barnum"),
                nh_elections("publishes the official marked ballot "
                             "for the March 3, 2026 annual town "
                             "meeting (364 ballots cast), recording "
                             "John Roleau re-elected with 319 votes "
                             "and Marie Jewett re-elected with 343 "
                             "votes; the selectboard page's printed "
                             "term expiries for Roleau and Jewett "
                             "are stale and the certified results "
                             "govern"),
                sb_dir("carries a single New Haven row naming "
                       "Shauntell Barnum; the directory is "
                       "incomplete for this town and the town's own "
                       "sources govern. The 2025 annual report "
                       "seated Chris Bataille on the board in "
                       "Barnum's place; the transition is not "
                       "explained in any official source located, "
                       "and Barnum is recorded as the elected "
                       "member the current pages present")],
               [holder("John Roleau", "john-roleau"),
                holder("Marie Jewett", "marie-jewett"),
                holder("Mike Audy", "mike-audy"),
                holder("Bruce Many", "bruce-many"),
                holder("Shauntell Barnum", "shauntell-barnum")]),
        office("town-clerk", "Town Clerk",
               "New Haven Town Clerk", 1,
               [guide("names Pamela Kingman as New Haven's town "
                      "clerk"),
                nh_reports("the 2025 annual report's officers table "
                           "and the 2026 warning (Art. 6) carry "
                           "Kingman as town clerk for a term to "
                           "2028")],
               [holder("Pamela Kingman", "pamela-kingman")]),
        office("town-treasurer", "Town Treasurer",
               "New Haven Town Treasurer", 1,
               [guide("names Julie Bessette as New Haven's town "
                      "treasurer"),
                nh_reports("the 2025 annual report's officers table "
                           "carries Bessette as town treasurer for "
                           "a term to 2028")],
               [holder("Julie Bessette", "julie-bessette")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "New Haven Collector of Delinquent Taxes", 1,
               [nh_reports("the town's officers table and warning "
                           "elect a collector of delinquent taxes "
                           "separately; Julie Bessette holds the "
                           "office for a term to 2028")],
               [holder("Julie Bessette", "julie-bessette")]),
        office("lister", "Lister",
               "New Haven Board of Listers", 3,
               [nh_reports("the 2025 annual report's officers table "
                           "lists listers Ted Foster (to 2028), "
                           "Julie Bessette, and Jay Best, Jr."),
                nh_elections("the official March 3, 2026 ballot "
                             "records Julie Bessette elected to "
                             "the three-year lister seat with 349 "
                             "votes (she had been appointed to fill "
                             "a vacancy) and Jay Best, Jr. elected "
                             "to the one-year lister seat with 323 "
                             "votes")],
               [holder("Ted Foster", "ted-foster"),
                holder("Julie Bessette", "julie-bessette"),
                holder("Jay Best, Jr.", "jay-best-jr")]),
        office("auditor", "Auditor",
               "New Haven Auditors", 3,
               [nh_reports("the 2025 annual report's officers table "
                           "lists auditors Ted Foster (to 2028), "
                           "Mary Pratt (to 2027), and Ellie de "
                           "Villiers (to 2028)")],
               [holder("Ted Foster", "ted-foster"),
                holder("Mary Pratt", "mary-pratt"),
                holder("Ellie de Villiers", "ellie-de-villiers")]),
        office("moderator", "Moderator",
               "New Haven Moderator", 1,
               [nh_elections("the official March 3, 2026 ballot "
                             "records Pam Marsh elected moderator "
                             "with 315 votes, to the new three-year "
                             "term; Marsh is the Addison Probate "
                             "District's judge of probate and her "
                             "existing person record is reused")],
               [holder("Pam Marsh", "pam-marsh",
                       existing_person_id="ocd-person/2ffc7639-ae1f-55ab-bdac-a5601b516a20")]),
        office("library-trustee", "Library Trustee",
               "New Haven Library Trustees", 5,
               [nh_reports("the 2025 annual report's officers table "
                           "lists five library trustees: Kristen "
                           "Swartzentruber (to 2028), Darcy "
                           "Cummings (to 2028), Kim Callahan, Erika "
                           "Smith, and Sujata Moorti (appointed "
                           "after Leanne Gund resigned)"),
                nh_elections("the official March 3, 2026 ballot "
                             "records Kim Callahan re-elected with "
                             "333 votes, Molly Bull elected with 332 "
                             "votes (Erika Smith's seat), and "
                             "Sujata Moorti elected to the one-year "
                             "remainder with 335 votes")],
               [holder("Kristen Swartzentruber",
                       "kristen-swartzentruber"),
                holder("Darcy Cummings", "darcy-cummings"),
                holder("Kim Callahan", "kim-callahan"),
                holder("Molly Bull", "molly-bull"),
                holder("Sujata Moorti", "sujata-moorti")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "New Haven Justices of the Peace", 5,
               [jp_src("lists seven New Haven justices of the "
                       "peace elected November 5, 2024; two have "
                       "since resigned (see the election note), "
                       "leaving five serving")],
               [holder("Kathleen Barrett", "kathleen-barrett"),
                holder("Tim Bouton", "tim-bouton"),
                holder("Marie Jewett", "marie-jewett"),
                holder("Al Karnatz", "al-karnatz"),
                holder("Pam Marsh", "pam-marsh",
                       existing_person_id="ocd-person/2ffc7639-ae1f-55ab-bdac-a5601b516a20")]),
    ]
    jp = jp_election(
        "new-haven-vt", "Town of New Haven", 7,
        "lists seven New Haven justices of the peace elected "
        "November 5, 2024: Kathleen Barrett, Tim Bouton, Gail "
        "Freidin, Al Karnatz, Marie Jewett, Pam Marsh, and Susan "
        "Smiley. The town's 2025 annual report records that Gail "
        "Freidin (printed there as 'Gail Byers'; the listing's form "
        "governs) resigned in November 2025 and Susan Smiley "
        "resigned in January 2026, so five of the seven winners "
        "currently serve and are the winners recorded here; "
        "Freidin and Smiley, as departed winners, are named in "
        "this note only (the Enosburgh/Maidstone pattern). The "
        "listing publishes no vote totals or "
        "party labels and none are recorded",
        [nh_reports("the 2025 annual report's officers table "
                    "records the resignations of justices of the "
                    "peace Gail Freidin (November 2025) and Susan "
                    "Smiley (January 2026)")])
    return spec("new-haven", "Town of New Haven", offices, jp)


SPECS["new-haven"] = new_haven_spec()

# ------------------------------------------------------------ Newark
def newark_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Newark Selectboard", 3,
               [sb_dir("lists Newark's selectboard as Kevin "
                       "Aucoin, Mark Ellingwood (Chair), and Nancy "
                       "McDermott. The Town of Newark has no "
                       "official website (no domain resolves to "
                       "one); the Secretary of State's directory "
                       "is the roster source")],
               [holder("Kevin Aucoin", "kevin-aucoin"),
                holder("Mark Ellingwood", "mark-ellingwood"),
                holder("Nancy McDermott", "nancy-mcdermott")]),
        office("town-clerk", "Town Clerk",
               "Newark Town Clerk", 1,
               [clerk_xlsx("lists Amber Holden as Newark's town "
                           "clerk"),
                guide("names Amber Holden as Newark's town clerk")],
               [holder("Amber Holden", "amber-holden")]),
        office("town-treasurer", "Town Treasurer",
               "Newark Town Treasurer", 1,
               [guide("names Amber Holden as Newark's town "
                      "treasurer; no treasurer contact spreadsheet "
                      "entry covers Newark, and nothing located "
                      "shows the Guide entry stale")],
               [holder("Amber Holden", "amber-holden")]),
        office("moderator", "Moderator",
               "Newark Moderator", 1,
               [statute2646_structure("one moderator for a "
                                      "one-year term")]),
        office("lister", "Lister",
               "Newark Board of Listers", 3,
               [statute2646_structure("three listers on staggered "
                                      "three-year terms")]),
        office("auditor", "Auditor",
               "Newark Auditors", 3,
               [statute2646_structure("three auditors on staggered "
                                      "three-year terms")]),
        office("grand-juror", "Grand Juror",
               "Newark Grand Juror", 1,
               [statute2646_structure("one grand juror")]),
        office("town-agent", "Town Agent",
               "Newark Town Agent", 1,
               [statute2646_structure("one town agent")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Newark Justices of the Peace", 3,
               [jp_src("lists three Newark justices of the peace "
                       "elected November 5, 2024")],
               [holder("Lisa Grout", "lisa-grout"),
                holder("Linda Barksdale", "linda-barksdale"),
                holder("Mary Ann Riggie", "mary-ann-riggie")]),
    ]
    jp = jp_election(
        "newark-vt", "Town of Newark", 3,
        "lists three Newark justices of the peace elected "
        "November 5, 2024: Lisa Grout, Linda Barksdale, and Mary "
        "Ann Riggie. The listing publishes no vote totals or "
        "party labels and none are recorded")
    return spec("newark", "Town of Newark", offices, jp)


SPECS["newark"] = newark_spec()

# ------------------------------------------------------------ Newbury (town)
NB_REPORT = {
    "url": "https://vt-newbury.civicplus.com/DocumentCenter/View/934",
    "note": "PLACEHOLDER",
}
NB_LISTERS_MIN = {
    "url": "https://www.newburyvt.org/AgendaCenter/ViewFile/Minutes/_03042026-390",
    "note": "PLACEHOLDER",
}


def nb_report(what):
    return S(NB_REPORT, "Town of Newbury (official website), 2025 "
             f"Annual Report: {what}")


def nb_listers_min(what):
    return S(NB_LISTERS_MIN, "Town of Newbury Board of Listers, "
             f"minutes of March 4, 2026: {what}")


def newbury_town_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Newbury Selectboard", 3,
               [sb_dir("lists Newbury's selectboard as Andrew Lee, "
                       "Shauna Prime, and Susan Culp (Chair)"),
                nb_report("the 2025 annual report's '2025 Town "
                          "Officers' table seated Jeff McKelvey "
                          "instead of Lee, and marks Prime appointed "
                          "to a seat expiring 2026; Prime holds by "
                          "the March 2026 election and is recorded "
                          "elected with that appointment history "
                          "noted. McKelvey is not recorded")],
               [holder("Susan Culp", "susan-culp"),
                holder("Shauna Prime", "shauna-prime"),
                holder("Andrew Lee", "andrew-lee")]),
        office("town-clerk", "Town Clerk",
               "Newbury Town Clerk", 1,
               [guide("names Chuck Schulze as Newbury's town "
                      "clerk"),
                nb_report("the officers table carries Schulze as "
                          "town clerk for a term to 2027")],
               [holder("Chuck Schulze", "chuck-schulze")]),
        office("town-treasurer", "Town Treasurer",
               "Newbury Town Treasurer", 1,
               [guide("names Mary Collins as Newbury's town "
                      "treasurer"),
                nb_report("the officers table carries Collins as "
                          "town treasurer for a term to 2028")],
               [holder("Mary Collins", "mary-collins")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Newbury Collector of Delinquent Taxes", 1,
               [nb_report("the officers table marks the collector "
                          "of delinquent taxes an appointed office "
                          "in Newbury, held by Mary Collins, the "
                          "town treasurer")],
               [holder("Mary Collins", "mary-collins",
                       how_seated="appointed")]),
        office("lister", "Lister",
               "Newbury Board of Listers", 3,
               [nb_report("the officers table lists listers Amanda "
                          "Beaulieu (Chair), Janis Moore, and "
                          "Dustin Putnam; Moore's printed expiry "
                          "is 2026"),
                nb_listers_min("the listers' own minutes of "
                               "March 4, 2026 (the day after town "
                               "meeting) seat all three listers, "
                               "which carries Moore's incumbency "
                               "past the printed expiry")],
               [holder("Amanda Beaulieu", "amanda-beaulieu"),
                holder("Janis Moore", "janis-moore"),
                holder("Dustin Putnam", "dustin-putnam")]),
        office("auditor", "Auditor",
               "Newbury Auditors", 3,
               [nb_report("the officers table lists auditors Jean "
                          "Welch (elected), and Huntoon and Butler "
                          "(appointed to vacancies), all with terms "
                          "expiring 2026; the March 2026 outcome is "
                          "published in no official source located, "
                          "so the post is created without "
                          "memberships and the three are held as "
                          "stragglers")]),
        office("moderator", "Moderator",
               "Newbury Moderator", 1,
               [nb_report("the officers table lists Moderator "
                          "Janet Cole on a one-year term expiring "
                          "2026; the March 2026 outcome is "
                          "published in no official source located, "
                          "so the post is created without a "
                          "membership and Cole is held as a "
                          "straggler")]),
        office("constable", "Constable",
               "Newbury Constable", 1,
               [nb_report("the officers table lists Constable Glen "
                          "Godfrey with a term expiring 2026; the "
                          "March 2026 outcome is published in no "
                          "official source located, so the post is "
                          "created without a membership and Godfrey "
                          "is held as a straggler")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Newbury Justices of the Peace", 10,
               [jp_src("lists ten Newbury justices of the peace "
                       "elected November 5, 2024")],
               [holder("Amanda Beaulieu", "amanda-beaulieu"),
                holder("Catherine Kidder", "catherine-kidder"),
                holder("Patsy Cole", "patsy-cole"),
                holder("Jean Welch", "jean-welch"),
                holder("Sarah Putnam", "sarah-putnam"),
                holder("Art Morris", "art-morris"),
                holder("Ian Clark", "ian-clark"),
                holder("Virginia Fuller", "virginia-fuller"),
                holder("Mary Burnham", "mary-burnham"),
                holder("Scott Labun", "scott-labun")]),
    ]
    jp = jp_election(
        "newbury-48175-vt", "Town of Newbury", 10,
        "lists ten Newbury justices of the peace elected "
        "November 5, 2024: Amanda Beaulieu, Catherine Kidder, "
        "Patsy Cole, Jean Welch, Sarah Putnam, Art Morris, Ian "
        "Clark, Virginia Fuller, Mary Burnham, and Scott Labun. "
        "The town report prints 'Patsy Spear Cole'; the listing's "
        "form governs. The listing publishes no vote totals or "
        "party labels and none are recorded")
    return spec("newbury-48175", "Town of Newbury", offices, jp)


SPECS["newbury-48175"] = newbury_town_spec()

# ------------------------------------------------------------ Newbury (village)
def newbury_village_spec():
    offices = [
        office("moderator", "Village Moderator",
               "Newbury Village Moderator", 1,
               [charter247("section 401 provides for a Moderator "
                           "elected at the village annual meeting; "
                           "the village has no website and no "
                           "official source located publishes its "
                           "current officers, so the post is "
                           "created without a membership")]),
        office("village-trustee", "Village Trustee",
               "Newbury Village Trustees", 3,
               [charter247("section 401 provides for three "
                           "Trustees; no official source located "
                           "publishes the current trustees, so the "
                           "post is created without memberships. "
                           "Section 701 sets the annual meeting on "
                           "the fourth Tuesday of May")]),
        office("village-clerk", "Village Clerk",
               "Newbury Village Clerk", 1,
               [charter247("section 401 provides for a Clerk "
                           "elected at the annual meeting; no "
                           "holder is published in any official "
                           "source located")]),
        office("village-treasurer", "Village Treasurer",
               "Newbury Village Treasurer", 1,
               [charter247("section 401 provides for a Treasurer "
                           "elected at the annual meeting; no "
                           "holder is published in any official "
                           "source located")]),
        office("village-auditor", "Village Auditor",
               "Newbury Village Auditors", 3,
               [charter247("section 401 provides for three "
                           "Auditors elected at the annual meeting; "
                           "no holders are published in any "
                           "official source located")]),
    ]
    return spec("newbury", "Village of Newbury", offices)


SPECS["newbury"] = newbury_village_spec()

# ------------------------------------------------------------ Newfane (town)
NF_SB = {
    "url": "https://newfanevt.com/government/selectboard/",
    "note": "PLACEHOLDER",
}
NF_TREAS = {
    "url": "https://newfanevt.com/government/offices/treasurer-tax-collector/",
    "note": "PLACEHOLDER",
}
NF_REPORT = {
    "url": "https://newfanevt.com/pdf/2025-town-report.pdf",
    "note": "PLACEHOLDER",
}


def nf_sb(what):
    return S(NF_SB, "Town of Newfane (official website), "
             f"Selectboard page: {what}")


def nf_treas(what):
    return S(NF_TREAS, "Town of Newfane (official website), "
             f"Treasurer / Tax Collector office page: {what}")


def nf_report(what):
    return S(NF_REPORT, "Town of Newfane, 2025 Annual Town Report: "
             f"{what}")


def newfane_town_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Newfane Selectboard", 5,
               [nf_sb("lists the five-member selectboard as Todd "
                      "Lawley (Chair), Marion Dowling (Vice "
                      "Chair), Michael Fitzpatrick, Christopher "
                      "Cleverly, and Katy Johnson-Aplin; printed "
                      "expiries of 2026 for Lawley, Dowling, and "
                      "Fitzpatrick are stale against the "
                      "maintained page, which is current")],
               [holder("Todd Lawley", "todd-lawley"),
                holder("Marion Dowling", "marion-dowling"),
                holder("Michael Fitzpatrick",
                       "michael-fitzpatrick"),
                holder("Christopher Cleverly",
                       "christopher-cleverly"),
                holder("Katy Johnson-Aplin",
                       "katy-johnson-aplin")]),
        office("town-clerk", "Town Clerk",
               "Newfane Town Clerk", 1,
               [clerk_xlsx("lists Wannetta Powling as Newfane's "
                           "town clerk"),
                nf_report("the officers table carries Powling as "
                          "town clerk on the town's one-year "
                          "cycle")],
               [holder("Wannetta Powling", "wannetta-powling")]),
        office("town-treasurer", "Town Treasurer",
               "Newfane Town Treasurer", 1,
               [guide("names Melissa Brown as Newfane's town "
                      "treasurer"),
                nf_treas("presents Melissa Brown as the town's "
                         "current treasurer")],
               [holder("Melissa Brown", "melissa-brown")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Newfane Collector of Delinquent Taxes", 1,
               [nf_treas("presents the treasurer / tax collector "
                         "as one elected office held by Melissa "
                         "Brown"),
                nf_report("the elected officers table lists the "
                          "collector of delinquent taxes separately "
                          "among the elected offices")],
               [holder("Melissa Brown", "melissa-brown")]),
        office("lister", "Lister",
               "Newfane Board of Listers", 3,
               [nf_report("the officers table lists listers Frank "
                          "Suponski (to 2027) and Mary F. "
                          "Hildebrandt (to 2028); the third seat, "
                          "held by Doris Knechtel on a one-year "
                          "term expiring 2026, stood at the March "
                          "2026 meeting with no published outcome "
                          "and is left unfilled, Knechtel held as "
                          "a straggler")],
               [holder("Frank Suponski", "frank-suponski"),
                holder("Mary F. Hildebrandt",
                       "mary-f-hildebrandt")]),
        office("constable", "Constable",
               "Newfane Constable", 1,
               [nf_report("the officers table lists Constable Eric "
                          "Durocher with a term expiring 2026; the "
                          "March 2026 outcome is published in no "
                          "official source located, so the post is "
                          "created without a membership and "
                          "Durocher is held as a straggler")]),
        office("moderator", "Moderator",
               "Newfane Moderator", 1,
               [nf_report("the officers table lists Moderator Kim "
                          "Friedman with a term expiring 2026; the "
                          "post is created without a membership "
                          "and Friedman is held as a straggler")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Newfane Justices of the Peace", 7,
               [jp_src("lists seven Newfane justices of the peace "
                       "elected November 5, 2024; the town "
                       "report's justice column names a partly "
                       "different seven (see the election note) "
                       "and the listing governs")],
               [holder("Priscilla Cottron", "priscilla-cottron"),
                holder("Gloria Cristelli", "gloria-cristelli"),
                holder("Fiona Chevalier", "fiona-chevalier"),
                holder("Lynn Forrest", "lynn-forrest"),
                holder("Caroline Apple Gifford",
                       "caroline-apple-gifford"),
                holder("Steve Levine", "steve-levine"),
                holder("Kate Gehring", "kate-gehring")]),
    ]
    jp = jp_election(
        "newfane-48400-vt", "Town of Newfane", 7,
        "lists seven Newfane justices of the peace elected "
        "November 5, 2024: Priscilla Cottron, Gloria Cristelli, "
        "Fiona Chevalier, Lynn Forrest, Caroline Apple Gifford, "
        "Steve Levine, and Kate Gehring. The town report's "
        "justice column names Cottron (spelled 'Cotton'), "
        "Cristelli, Gifford, and Levine, plus Sandra Dadik, "
        "Abigail Dillon, and Evelyn Sirois, omitting Chevalier, "
        "Forrest, and Gehring -- an equal-count name swap, so the "
        "certified listing governs and Dadik, Dillon, and Sirois "
        "(possible mid-term Board of Civil Authority appointees) "
        "are held as stragglers in this note. The listing "
        "publishes no vote totals or party labels and none are "
        "recorded",
        [nf_report("the officers table's justice of the peace "
                   "column names a partly different set of seven "
                   "(see the election note)")])
    return spec("newfane-48400", "Town of Newfane", offices, jp)


SPECS["newfane-48400"] = newfane_town_spec()

# ------------------------------------------------------------ Newfane (village)
def newfane_village_spec():
    offices = [
        office("village-trustee", "Village Trustee",
               "Newfane Village Trustees", 3,
               [charter249("section 201 provides for three "
                           "Trustees chosen by ballot at the "
                           "annual meeting; the village has no "
                           "website and no official source located "
                           "publishes its current officers, so the "
                           "post is created without memberships")]),
        office("village-clerk", "Village Clerk",
               "Newfane Village Clerk", 1,
               [charter249("section 201 provides for a Clerk "
                           "chosen by ballot at the annual "
                           "meeting; no holder is published in any "
                           "official source located")]),
        office("village-treasurer", "Village Treasurer",
               "Newfane Village Treasurer", 1,
               [charter249("section 201 provides for a Treasurer "
                           "chosen by ballot at the annual "
                           "meeting; no holder is published in any "
                           "official source located")]),
        office("collector-of-taxes", "Collector of Taxes",
               "Newfane Village Collector of Taxes", 1,
               [charter249("section 201 provides for a Collector "
                           "of Taxes chosen by ballot at the "
                           "annual meeting; section 305 makes the "
                           "Collector ex officio Chief of Police. "
                           "No holder is published in any official "
                           "source located")]),
        office("village-auditor", "Village Auditor",
               "Newfane Village Auditor", 1,
               [charter249("section 201 provides for an Auditor "
                           "chosen by ballot at the annual meeting; "
                           "no holder is published in any official "
                           "source located")]),
        office("fire-marshal", "Fire Marshal",
               "Newfane Village Fire Marshal", 1,
               [charter249("section 201 provides for a Fire "
                           "Marshal chosen by ballot at the annual "
                           "meeting; no holder is published in any "
                           "official source located. The post is "
                           "flagged with the standing fire-officers "
                           "scope question on issue #163")]),
    ]
    return spec("newfane", "Village of Newfane", offices)


SPECS["newfane"] = newfane_village_spec()

# ------------------------------------------------------------ Newport (city)
NC_REPORT = {
    "url": "https://www.newportvermont.org/wp-content/uploads/2026/02/2025-Newport-City-Annual-Report.pdf",
    "note": "PLACEHOLDER",
}
NC_COUNCIL = {
    "url": "https://www.newportvermont.org/city-information/city-council-mayor/",
    "note": "PLACEHOLDER",
}


def nc_report(what):
    return S(NC_REPORT, "City of Newport, 2025 Annual Report: "
             f"{what}")


def nc_council(what):
    return S(NC_COUNCIL, "City of Newport (official website), City "
             f"Council & Mayor page: {what}")


def newport_city_spec():
    offices = [
        office("mayor", "Mayor",
               "Newport City Mayor", 1,
               [charter007("section 6 provides for a Mayor "
                           "elected in city election"),
                nc_report("the City Government roster carries "
                          "Mayor Rick Ufford-Chase for a term to "
                          "2027; the March 2026 warning does not "
                          "stand the mayor"),
                nc_council("lists Rick Ufford-Chase as Mayor")],
               [holder("Rick Ufford-Chase", "rick-ufford-chase")]),
        office("alderman", "Alderman",
               "Newport City Council", 4,
               [charter007("section 6 provides for four Aldermen "
                           "elected in city election; section 7 "
                           "makes the Mayor and Aldermen the City "
                           "Council. The city styles its council "
                           "members 'Council Members'"),
                nc_report("the City Government roster carries "
                          "Council Members Kevin Charboneau "
                          "(President; to 2026), John Monette (to "
                          "2026), Carter Finegan (to 2027), and "
                          "Andrew Touchette (to 2027), and the "
                          "March 2026 warning (Art. 1) stood two "
                          "council seats for two years"),
                nc_council("the post-election council page lists "
                           "Carter Finegan, John Monette, Andrew "
                           "Touchette, and Sharon Pare"),
                sb_dir("the June 2026 directory's Newport City row "
                       "names Council President Alissa Finegan, "
                       "John Monette, Sharon Pare, and Andrew "
                       "Touchette. Finegan's given name per the "
                       "directory is Alissa; the report and her "
                       "city email use her used name, Carter "
                       "Finegan. Monette, the exp.-2026 incumbent, "
                       "is recorded re-elected on the two "
                       "post-election listings. Pare, who appears "
                       "in the departed Charboneau's place, is NOT "
                       "recorded: no official source located "
                       "states how she was seated, so the fourth "
                       "seat is unfilled here and she is held as "
                       "a straggler")],
               [holder("Alissa Finegan", "alissa-finegan"),
                holder("John Monette", "john-monette"),
                holder("Andrew Touchette", "andrew-touchette")]),
        office("city-clerk", "City Clerk",
               "Newport City Clerk", 1,
               [charter007("section 6 provides for a City Clerk "
                           "elected in city election"),
                nc_report("the roster carries James D. Johnson as "
                          "Clerk/Treasurer for a term to 2028")],
               [holder("James D. Johnson", "james-d-johnson")]),
        office("city-treasurer", "City Treasurer",
               "Newport City Treasurer", 1,
               [charter007("section 6 provides for a City "
                           "Treasurer elected in city election"),
                nc_report("the roster carries James D. Johnson as "
                          "Clerk/Treasurer for a term to 2028")],
               [holder("James D. Johnson", "james-d-johnson")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Newport Collector of Delinquent Taxes", 1,
               [charter007("section 8 provides for a Collector of "
                           "Taxes appointed by the City Council"),
                nc_report("the Special Appointments column carries "
                          "Francis Cheney, III as Delinquent Tax "
                          "Collector (he is also the appointed Tax "
                          "Assessor); the post is created with an "
                          "appointed membership")],
               [holder("Francis Cheney, III",
                       "francis-cheney-iii",
                       how_seated="appointed")]),
        office("constable", "Constable",
               "Newport Constable", 1,
               [charter007("section 6 provides for one Constable "
                           "elected in city election"),
                nc_report("the March 2026 warning (Art. 1) elects "
                          "a Constable for one year ensuing, but "
                          "the report names no constable and no "
                          "outcome is published in any official "
                          "source located, so the post is created "
                          "without a membership")]),
        office("grand-juror", "Grand Juror",
               "Newport Grand Jurors", 3,
               [charter007("section 6 provides for three Grand "
                           "Jurors elected in city election"),
                nc_report("the City Government roster prints "
                          "Grand Jurors Andrew Touchette, Laurie "
                          "Grimm, and Clark Curtis with terms to "
                          "2027, but the March 2026 warning (Art. "
                          "1) in the same report stands three Grand "
                          "Jurors for three years ensuing; the "
                          "seats stood with no published outcome, "
                          "so the post is created without "
                          "memberships and the three roster names "
                          "are held as stragglers (Touchette is "
                          "recorded as Alderman)")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Newport Justices of the Peace", 5,
               [jp_src("lists five City of Newport justices of the "
                       "peace elected November 5, 2024; the city "
                       "report's justice list names four, omitting "
                       "Carl King, and the listing governs")],
               [holder("Ruth Ann Fletcher", "ruth-ann-fletcher"),
                holder("Carl King", "carl-king"),
                holder("Pamela Ladds", "pamela-ladds"),
                holder("Stephen Laurie", "stephen-laurie"),
                holder("Jacques Roberge", "jacques-roberge")]),
    ]
    jp = jp_election(
        "newport-vt", "City of Newport", 5,
        "lists five City of Newport justices of the peace elected "
        "November 5, 2024: Ruth Ann Fletcher, Carl King, Pamela "
        "Ladds, Stephen Laurie, and Jacques Roberge. The city's "
        "2025 annual report justice list names four of them "
        "(omitting Carl King) and spells 'Pam Ladds' and 'Steven "
        "Laurie'; the listing's forms govern. The listing "
        "publishes no vote totals or party labels and none are "
        "recorded",
        [nc_report("the justice of the peace list names Ruth Ann "
                   "Fletcher, Pam Ladds, Steven Laurie, and "
                   "Jacques Roberge")])
    return spec("newport", "City of Newport", offices, jp)


SPECS["newport"] = newport_city_spec()

# ------------------------------------------------------------ North Bennington
NB_MIN_JAN = {
    "url": "https://www.villagenorthbennington.org/s/Minutes-January-13-2026.pdf",
    "note": "PLACEHOLDER",
}
NB_MIN_MAR = {
    "url": "https://www.villagenorthbennington.org/s/Minutes-Special-Meeting-March-19-2026.pdf",
    "note": "PLACEHOLDER",
}
NB_MIN_JUN = {
    "url": "https://www.villagenorthbennington.org/s/Minutes-June-9-2026.pdf",
    "note": "PLACEHOLDER",
}


def nb_min_jan(what):
    return S(NB_MIN_JAN, "Village of North Bennington, Board of "
             f"Trustees minutes, January 13, 2026: {what}")


def nb_min_mar(what):
    return S(NB_MIN_MAR, "Village of North Bennington, Board of "
             f"Trustees special (reorganization) meeting minutes, "
             f"March 19, 2026: {what}")


def nb_min_jun(what):
    return S(NB_MIN_JUN, "Village of North Bennington, Board of "
             f"Trustees minutes, June 9, 2026: {what}")


def north_bennington_spec():
    offices = [
        office("village-trustee", "Village Trustee",
               "North Bennington Village Trustees", 5,
               [charter251("section 203(a) provides for trustees "
                           "elected at the annual meeting to make "
                           "a full board of five trustees; section "
                           "301 staggers trustee terms at three "
                           "years"),
                nb_min_jan("seat Trustees Rogers, Creedy, and "
                           "Mullineaux in person and Trustees "
                           "Patterson and Lowary via Zoom"),
                nb_min_mar("record the oaths administered after "
                           "the March 17, 2026 annual meeting: Tara "
                           "Lowary re-elected trustee (three-year "
                           "term) and David Shaughnessey newly "
                           "elected trustee (three-year term), and "
                           "Mary Rogers nominated Chair. Matthew "
                           "Patterson, seated in January, departed "
                           "at the annual meeting and is not "
                           "recorded. The June 9, 2026 minutes print "
                           "the surname 'Shaughnessy'; the oath "
                           "minutes' spelling governs"),
                nb_min_jun("seat Trustees Rogers, Shaughnessey, "
                           "Creedy, Lowary, and Mullineaux in "
                           "person, with Rogers as Chair")],
               [holder("Mary Rogers", "mary-rogers"),
                holder("Scott Creedy", "scott-creedy"),
                holder("Tara Lowary", "tara-lowary"),
                holder("David Shaughnessey", "david-shaughnessey"),
                holder("Ray Mullineaux", "ray-mullineaux")]),
        office("village-clerk", "Village Clerk",
               "North Bennington Village Clerk", 1,
               [charter251("section 203(a) provides for a Clerk "
                           "elected at every annual meeting"),
                nb_min_mar("record the oath administered to "
                           "re-elected Village Clerk Lorine Elwell "
                           "(the form of her name in the oath line "
                           "and her signature; the minutes' running "
                           "text uses Lori Elwell, the name "
                           "recorded here)")],
               [holder("Lori Elwell", "lori-elwell")]),
        office("village-treasurer", "Village Treasurer",
               "North Bennington Village Treasurer", 1,
               [charter251("section 203(a) provides for a "
                           "Treasurer elected at every annual "
                           "meeting; section 305 makes the "
                           "Treasurer also perform the duties of a "
                           "collector of town taxes, so no separate "
                           "collector post is created although the "
                           "village's older annual meetings elected "
                           "a Collector of Taxes as a separate "
                           "article"),
                nb_min_mar("record the oath administered to "
                           "re-elected Treasurer Doug Buggee")],
               [holder("Doug Buggee", "doug-buggee")]),
        office("moderator", "Village Moderator",
               "North Bennington Village Moderator", 1,
               [charter251("section 203(a) provides for a "
                           "Moderator elected at every annual "
                           "meeting; the March 2026 outcome is "
                           "published in no official source "
                           "located, so the post is created without "
                           "a membership. John Ulrich, elected "
                           "moderator at the annual meeting recorded "
                           "in the village's 2024 annual report, is "
                           "held as a straggler")]),
        office("village-auditor", "Village Auditor",
               "North Bennington Village Auditors", 3,
               [charter251("section 203(a) provides for three "
                           "auditors elected at every annual "
                           "meeting; the annual meeting recorded in "
                           "the village's 2024 annual report left "
                           "all three auditor seats vacant (no "
                           "nominations) and the March 2026 "
                           "outcome is unpublished, so the post is "
                           "created without memberships")]),
    ]
    return spec("north-bennington", "Village of North Bennington",
                offices)


SPECS["north-bennington"] = north_bennington_spec()

# ------------------------------------------------------------ North Hero
NHERO_TERMS = {
    "url": "https://northherovt.com/document/554",
    "note": "PLACEHOLDER",
}
NHERO_SB = {
    "url": "https://northherovt.com/33/selectboard",
    "note": "PLACEHOLDER",
}
NHERO_OFFICE = {
    "url": "https://northherovt.com/16/town-office",
    "note": "PLACEHOLDER",
}
NHERO_LISTERS = {
    "url": "https://northherovt.com/28/listers",
    "note": "PLACEHOLDER",
}
NHERO_CONSTABLE = {
    "url": "https://northherovt.com/8/constable-delinquent-tax-collector",
    "note": "PLACEHOLDER",
}
NHERO_JP = {
    "url": "https://northherovt.com/13/justice-of-the-peace",
    "note": "PLACEHOLDER",
}


def nhero_terms(what):
    return S(NHERO_TERMS, "Town of North Hero (official website), "
             f"'North Hero Elected Officials Term Lengths' table "
             f"(linked from the Elections page): {what}")


def nhero_sb(what):
    return S(NHERO_SB, "Town of North Hero (official website), "
             f"Selectboard page: {what}")


def nhero_office(what):
    return S(NHERO_OFFICE, "Town of North Hero (official website), "
             f"Town Office page: {what}")


def nhero_listers(what):
    return S(NHERO_LISTERS, "Town of North Hero (official website), "
             f"Listers page: {what}")


def nhero_constable(what):
    return S(NHERO_CONSTABLE, "Town of North Hero (official "
             f"website), Constable / Delinquent Tax Collector page: "
             f"{what}")


def nhero_jp(what):
    return S(NHERO_JP, "Town of North Hero (official website), "
             f"Justice of the Peace page: {what}")


def north_hero_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "North Hero Selectboard", 5,
               [nhero_sb("lists the selectboard as Karl Raacke "
                         "(Chair), Joe Latimer (Vice Chair), Harry "
                         "Parker, Clair LaVoie, and Frank Codey; "
                         "the page's 'Clair LaVoie' is a typo "
                         "against the town's term table and the "
                         "Secretary of State's directory, which "
                         "both give Claire (the table prints the "
                         "surname LaVoie)"),
                nhero_terms("prints selectboard terms: Harry C. "
                            "Parker to 2027, Karl Raacke to 2027, "
                            "Roland (Joe) Latimer II to 2028, "
                            "Claire LaVoie to 2028, and Frank Codey "
                            "to 2029"),
                sb_dir("lists North Hero's selectboard as Frank "
                       "Codey, Joe Latimer (Vice Chair), Claire "
                       "Lavoie, Harry Parker, and Karl Raacke "
                       "(Chair)")],
               [holder("Karl Raacke", "karl-raacke"),
                holder("Harry C. Parker", "harry-c-parker"),
                holder("Joe Latimer", "joe-latimer"),
                holder("Claire Lavoie", "claire-lavoie"),
                holder("Frank Codey", "frank-codey")]),
        office("town-clerk", "Town Clerk",
               "North Hero Town Clerk", 1,
               [nhero_office("names Corinn Julow as Town Clerk"),
                nhero_terms("prints Town Clerk Corinn Julow, "
                            "three-year term to 2027"),
                guide("names Corinn Julow as North Hero's town "
                      "clerk")],
               [holder("Corinn Julow", "corinn-julow")]),
        office("town-treasurer", "Town Treasurer",
               "North Hero Town Treasurer", 1,
               [nhero_office("names Lisa Keyworth as Treasurer"),
                nhero_terms("prints Town Treasurer Lisa Keyworth, "
                            "three-year term to 2027")],
               [holder("Lisa Keyworth", "lisa-keyworth")]),
        office("moderator", "Moderator",
               "North Hero Moderator", 1,
               [nhero_terms("prints Town Moderator Andy Julow, "
                            "one-year term to 2027")],
               [holder("Andy Julow", "andy-julow")]),
        office("lister", "Lister",
               "North Hero Board of Listers", 3,
               [nhero_terms("prints Listers Jim Kilbride (to "
                            "2027), Lisa Keyworth (to 2028, two "
                            "years remaining in a three-year term), "
                            "and Kathy Finck (to 2029)"),
                nhero_listers("names Listers Kathy Finck and Jim "
                              "Kilbride and 'Lisa Keyworth "
                              "(Assessor)'; the elected-officials "
                              "term table lists Keyworth as an "
                              "elected lister holding a term and "
                              "governs")],
               [holder("Jim Kilbride", "jim-kilbride"),
                holder("Lisa Keyworth", "lisa-keyworth"),
                holder("Kathy Finck", "kathy-finck")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "North Hero Cemetery Commissioners", 5,
               [nhero_terms("prints five Cemetery Commissioners on "
                            "five-year terms: Michael Tranby (to "
                            "2027), Tracy Giroux (to 2028), Jim "
                            "Tudhope (to 2029), Majken Tranby (to "
                            "2030), and Frank Dattilio (to 2031)")],
               [holder("Michael Tranby", "michael-tranby"),
                holder("Tracy Giroux", "tracy-giroux"),
                holder("Jim Tudhope", "jim-tudhope"),
                holder("Majken Tranby", "majken-tranby"),
                holder("Frank Dattilio", "frank-dattilio")]),
        office("library-trustee", "Library Trustee",
               "North Hero Library Trustees", 7,
               [nhero_terms("prints seven elected Library "
                            "Trustees: Elizabeth (Betsy) Jaffe "
                            "(to 2027), Roberta Gilmour (to 2027), "
                            "Linda Darrow (to 2028), Angie Marano "
                            "(to 2028), Diane Bahrenburg (to 2029), "
                            "Helen McCarthy (to 2029), and Melissa "
                            "Cronin (to 2030). The table fixes both "
                            "the board's size and its elected "
                            "status")],
               [holder("Betsy Jaffe", "betsy-jaffe"),
                holder("Roberta Gilmour", "roberta-gilmour"),
                holder("Linda Darrow", "linda-darrow"),
                holder("Angie Marano", "angie-marano"),
                holder("Diane Bahrenburg", "diane-bahrenburg"),
                holder("Helen McCarthy", "helen-mccarthy"),
                holder("Melissa Cronin", "melissa-cronin")]),
        office("first-constable", "First Constable",
               "North Hero First Constable", 1,
               [nhero_terms("prints First Constable Jim Benson, "
                            "one-year term to 2027"),
                nhero_constable("names Jim Benson as Constable")],
               [holder("Jim Benson", "jim-benson")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "North Hero Collector of Delinquent Taxes", 1,
               [nhero_terms("prints Delinquent Tax Collector Lisa "
                            "Keyworth, three-year term to 2027, "
                            "among the elected officials"),
                nhero_constable("names Lisa Keyworth as Delinquent "
                                "Tax Collector")],
               [holder("Lisa Keyworth", "lisa-keyworth")]),
        office("planning-commissioner", "Planning Commissioner",
               "North Hero Planning Commission", 7,
               [nhero_terms("prints seven Planning Commissioners "
                            "among the town's elected officials: "
                            "Andy Alling (to 2027), David "
                            "Bahrenburg (to 2027), Warren Wright "
                            "(to 2028), Patricia Sainsbury (to "
                            "2028), George Salembier (to 2028), Jan "
                            "Peterson (to 2029), and Jeff Van den "
                            "Noort (to 2029); towns may elect "
                            "planning commissioners under 24 V.S.A. "
                            "section 4322")],
               [holder("Andy Alling", "andy-alling"),
                holder("David Bahrenburg", "david-bahrenburg"),
                holder("Warren Wright", "warren-wright"),
                holder("Patricia Sainsbury", "patricia-sainsbury"),
                holder("George Salembier", "george-salembier"),
                holder("Jan Peterson", "jan-peterson"),
                holder("Jeff Van den Noort", "jeff-van-den-noort")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "North Hero Justices of the Peace", 5,
               [jp_src("lists five North Hero justices of the "
                       "peace elected November 5, 2024"),
                nhero_jp("names the town's five justices of the "
                         "peace as Robert Ayers, Diane Bahrenburg, "
                         "Susan Davis, Leisa Fearing, and Mary Jo "
                         "McCarthy"),
                nhero_terms("prints the five justices of the peace "
                            "with terms expiring January 31, "
                            "2027")],
               [holder("Robert Ayers", "robert-ayers"),
                holder("Diane Bahrenburg", "diane-bahrenburg"),
                holder("Susan Davis", "susan-davis"),
                holder("Leisa Fearing", "leisa-fearing"),
                holder("Mary Jo McCarthy", "mary-jo-mccarthy")]),
    ]
    jp = jp_election(
        "north-hero-vt", "Town of North Hero", 5,
        "lists five North Hero justices of the peace elected "
        "November 5, 2024: Robert Ayers, Diane Bahrenburg, Susan "
        "Davis, Leisa Fearing, and Mary Jo McCarthy. The listing "
        "publishes no vote totals or party labels and none are "
        "recorded",
        [nhero_jp("names the same five justices of the peace"),
         nhero_terms("prints the five justices of the peace with "
                     "terms expiring January 31, 2027")])
    return spec("north-hero", "Town of North Hero", offices, jp)


SPECS["north-hero"] = north_hero_spec()

# ------------------------------------------------------------ Newport (town)
NT_SB = {
    "url": "https://townofnewport.org/town-departments/selectboard/",
    "note": "PLACEHOLDER",
}
NT_WARNING = {
    "url": "https://townofnewport.org/wp-content/uploads/2026/01/2026-Town-Meeting-Warning.pdf",
    "note": "PLACEHOLDER",
}
NT_REPORT = {
    "url": "https://townofnewport.org/wp-content/uploads/2025/03/ANNUAL-REPORT-2024.pdf",
    "note": "PLACEHOLDER",
}
NT_HOME = {
    "url": "https://townofnewport.org",
    "note": "PLACEHOLDER",
}


def nt_sb(what):
    return S(NT_SB, "Town of Newport (official website), "
             f"Selectboard page: {what}")


def nt_warning(what):
    return S(NT_WARNING, "Town of Newport, 2026 Town Meeting "
             f"Warning (annual meeting March 3, 2026): {what}")


def nt_report(what):
    return S(NT_REPORT, "Town of Newport, 2024 Annual Report, "
             f"'Town Officers' roster: {what}")


def nt_home(what):
    return S(NT_HOME, f"Town of Newport (official website): {what}")


def newport_town_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Newport Selectboard", 3,
               [nt_sb("lists the selectboard as Steve Barrup, "
                      "Richard Gosselin, and Jerry Waterman"),
                sb_dir("lists Newport's selectboard as Steven "
                       "Barrup (Chair), Karen Camber, and Richard "
                       "Gosselin. The directory and the factory "
                       "diverge from the town's own current page "
                       "on the third seat: the 2024 annual report "
                       "seats Waterman with a term expiring 2026, "
                       "the 2026 warning elects a selectperson for "
                       "a three-year term, and the town's current "
                       "page presents Waterman as seated, so he is "
                       "recorded re-elected and the town page "
                       "governs; Camber is held as a straggler"),
                nt_report("lists selectboard members Richard "
                          "Gosselin (to 2025), Jerry Waterman (to "
                          "2026), and Steve Barrup (to 2027)")],
               [holder("Steve Barrup", "steve-barrup"),
                holder("Richard Gosselin", "richard-gosselin"),
                holder("Jerry Waterman", "jerry-waterman")]),
        office("town-clerk", "Town Clerk",
               "Newport Town Clerk", 1,
               [nt_home("the site's contact footer names Hannah "
                        "Roberts as Town Clerk"),
                clerk_xlsx("lists Hannah Roberts as Newport's "
                           "town clerk"),
                guide("names Hannah Roberts as Newport's town "
                      "clerk"),
                nt_report("lists Denise Daigle as town clerk with "
                          "a term to 2027; she has departed and "
                          "Roberts is the clerk the current "
                          "sources present"),
                nt_warning("elects a Town Clerk for a three-year "
                           "term at the March 3, 2026 meeting")],
               [holder("Hannah Roberts", "hannah-roberts")]),
        office("town-treasurer", "Town Treasurer",
               "Newport Town Treasurer", 1,
               [treas_xlsx("lists Hannah Roberts as Newport's town "
                           "treasurer"),
                guide("names Hannah Roberts as Newport's town "
                      "treasurer"),
                nt_report("lists Denise Daigle as town/school "
                          "treasurer with a term to 2027; she has "
                          "departed"),
                nt_warning("elects a Town Treasurer for a "
                           "three-year term at the March 3, 2026 "
                           "meeting")],
               [holder("Hannah Roberts", "hannah-roberts")]),
        office("moderator", "Moderator",
               "Newport Moderator", 1,
               [nt_warning("elects a Moderator at the March 3, "
                           "2026 meeting; no outcome is published "
                           "in any official source located, so the "
                           "post is created without a membership"),
                nt_report("lists Moderator Richard Tetreault "
                          "with a term to 2025; he is held as a "
                          "straggler")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Newport Collector of Delinquent Taxes", 1,
               [nt_warning("elects a delinquent tax collector for "
                           "a one-year term at the March 3, 2026 "
                           "meeting; no outcome is published, so "
                           "the post is created without a "
                           "membership"),
                nt_report("lists Delinquent Tax Collector Denise "
                          "Daigle with a term to 2025")]),
        office("first-constable", "First Constable",
               "Newport First Constable", 1,
               [nt_warning("elects a First Constable for a "
                           "one-year term at the March 3, 2026 "
                           "meeting; no outcome is published, so "
                           "the post is created without a "
                           "membership"),
                nt_report("lists First Constable Anthony Glover "
                          "with a term to 2025; he is held as a "
                          "straggler")]),
        office("second-constable", "Second Constable",
               "Newport Second Constable", 1,
               [nt_warning("elects a Second Constable for a "
                           "one-year term at the March 3, 2026 "
                           "meeting; no outcome is published, so "
                           "the post is created without a "
                           "membership"),
                nt_report("lists Second Constable Terry Dillon "
                          "with a term to 2025; he is held as a "
                          "straggler")]),
        office("planning-commissioner", "Planning Commissioner",
               "Newport Planning Board", 7,
               [nt_warning("elects three planning board members "
                           "for three-year terms at the March 3, "
                           "2026 meeting; the board is an elected "
                           "body in Newport"),
                nt_report("lists seven planning board members: "
                          "Mike Beaumier and Bruce Sargent (to "
                          "2025), Ernest Choquette, Becky "
                          "Therrien, and Linda Curtis (to 2026), "
                          "and Ed Champine and Joanne Guyette-Worth "
                          "(to 2027). Only Champine and "
                          "Guyette-Worth, whose printed terms still "
                          "run, are recorded; the five whose seats "
                          "stood in 2025 or 2026 with unpublished "
                          "outcomes are held as stragglers")],
               [holder("Ed Champine", "ed-champine"),
                holder("Joanne Guyette-Worth",
                       "joanne-guyette-worth")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Newport Justices of the Peace", 7,
               [jp_src("lists seven Town of Newport justices of "
                       "the peace elected November 5, 2024; the "
                       "2024 annual report names six, omitting "
                       "William Bursey, and the listing governs")],
               [holder("Stephen Lowell", "stephen-lowell"),
                holder("Jim Hilliker", "jim-hilliker"),
                holder("Robert Hilliker", "robert-hilliker"),
                holder("Linda Waterman", "linda-waterman"),
                holder("Maureen McGuire", "maureen-mcguire"),
                holder("Steve Edgerley", "steve-edgerley"),
                holder("William Bursey", "william-bursey")]),
    ]
    jp = jp_election(
        "newport-48925-vt", "Town of Newport", 7,
        "lists seven Town of Newport justices of the peace "
        "elected November 5, 2024: Stephen Lowell, Jim Hilliker, "
        "Robert Hilliker, Linda Waterman, Maureen McGuire, Steve "
        "Edgerley, and William Bursey. The town's 2024 annual "
        "report names six of them, omitting Bursey; the listing "
        "governs. The listing publishes no vote totals or party "
        "labels and none are recorded",
        [nt_report("names justices of the peace Stephen Lowell, "
                   "Jim Hilliker, Linda Waterman, Robert Hilliker, "
                   "Steve Edgerley, and Maureen McGuire")])
    return spec("newport-48925", "Town of Newport", offices, jp)


SPECS["newport-48925"] = newport_town_spec()

# ------------------------------------------------------------ emit
for slug in ORDER:
    s = SPECS[slug]
    p = OUT / f"{s['place_slug']}.json"
    p.write_text(json.dumps(s, indent=1) + "\n")
    n_off = len(s["offices"])
    n_hold = sum(len(o.get("holders", ())) for o in s["offices"])
    print(f"{s['place_slug']}: {n_off} offices, {n_hold} holders")
print(f"TOTAL: {len(SPECS)} specs")
