#!/usr/bin/env python3
"""Batch 9 of the VT #163 municipal fan-out (alphabetical positions
80-89): Fayston, Ferrisburgh, Fletcher, Franklin, Georgia, Glover,
Goshen, Grafton, Granby, Grand Isle. Emits one JSON spec per
municipality for build_vt_municipality.py.
Research: vt_muni_batch9_research.md.

Identity calls baked into this batch (all flagged on #163):
- Glover JP Leanne Harple is the sitting Orleans-4 state
  representative; her existing state-tier person record is REUSED
  via existing_person_id and the JP candidacy is appended by hand.
- Grand Isle Clerk/Treasurer Melissa Boutin is a NEW person: the
  batch-2 Boutin records are Constance Boutin and Michael Boutin,
  different people in other counties.
- Granby's SB member R. Terry Williams (the factory's Raymond
  "Terry" Williams) and its Clerk/Treasurer Terri (Lynn) Williams
  are DISTINCT people -- different full names and roles.
- Franklin's SOS Selectboard directory entry is stale: the town's
  own March 3, 2026 meeting minutes seat Magnant and Dandurand
  where the directory (and factory) carry Grant and Hartman. The
  minutes govern. Likewise Lisa Larivee DECLINED the Franklin
  clerkship at the meeting (Pauline Gadbois was elected to fill
  the term) while remaining Treasurer -- the SOS Guide still
  lists her for both offices.
- Fayston, Fletcher, and Grafton clerk/treasurer seats are
  structure-only: in each town the offices affirmatively stood
  at the March 2026 meeting and no outcome is published (the
  Fayston rule), even though SOS directories still list the
  incumbents.
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


def clerk_xlsx(what):
    return S(CLERK_XLSX, "Vermont Secretary of State, Elections "
             "Division, '2026 VT Town Clerk Contact Info' spreadsheet: "
             f"{what}")


def treas_xlsx(what):
    return S(TREAS_XLSX, "Vermont Secretary of State, Elections "
             "Division, '2026 VT Treasurers' Contact Info' "
             f"spreadsheet: {what}")


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
                  f"(VT municipal batch 9); issue #163 "
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
                  f"# municipal fan-out batch 9; issue #163 "
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

# ------------------------------------------------------------- Fayston
FAYSTON_REPORT = {
    "url": "https://faystonvt.com/wp-content/uploads/2026/02/PDF-Fayston-Town-Report.pdf",
    "note": "PLACEHOLDER",
}


def fayston_report(note):
    return S(FAYSTON_REPORT, "Town of Fayston 2026 Town Report "
             "(faystonvt.com), printing the minutes of the March 4, "
             f"2025 annual meeting and the 2026 Warning: {note}")


def fayston_spec():
    label = "Town of Fayston"
    offices = [
        office("selectboard", "Selectboard Member", "Fayston Selectboard", 3,
               [sb_dir("lists three Fayston Selectboard members: Chuck "
                       "Martel (Chair), Mike Jordan (Vice Chair), and "
                       "Ron Graves."),
                fayston_report("the March 2025 minutes record Martel "
                               "re-elected to a three-year term; the "
                               "June 2026 directory seats all three "
                               "after the March 2026 meeting.")],
               [holder("Chuck Martel", "chuck-martel"),
                holder("Mike Jordan", "mike-jordan"),
                holder("Ron Graves", "ron-graves")]),
        office("town-clerk", "Town Clerk", "Fayston Town Clerk", 1,
               [fayston_report("Madison Vasseur was elected in March "
                               "2025 to fill the remainder of Patti "
                               "Lewis's term, ending 2026; the 2026 "
                               "Warning (Art. 3) stood the office for "
                               "a new three-year term and no outcome "
                               "is published. Structure only."),
                guide("lists Madison Vasseur as Fayston Town Clerk "
                      "(January 2026).")]),
        office("town-treasurer", "Town Treasurer", "Fayston Town Treasurer", 1,
               [fayston_report("Sarah Stavraky was elected in March "
                               "2025 to fill a term ending 2026; the "
                               "office stood in 2026 and no outcome is "
                               "published. Structure only."),
                guide("lists Sarah Stavraky as Fayston Town "
                      "Treasurer (January 2026).")]),
        office("collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
               "Fayston Collector of Delinquent Taxes", 1,
               [fayston_report("Sarah Stavraky was re-elected "
                               "Collector of Delinquent Taxes in "
                               "March 2025 for one year; the office "
                               "stood in 2026 and no outcome is "
                               "published. Structure only.")]),
        office("moderator", "Moderator", "Fayston Moderator", 1,
               [fayston_report("Rick Rayfield was re-elected "
                               "Moderator in March 2025 for one year; "
                               "the office stood in 2026 and no "
                               "outcome is published. Structure "
                               "only.")]),
        office("lister", "Lister", "Fayston Listers", 3,
               [fayston_report("the 2025 minutes record Kim Laidlaw "
                               "re-elected to a three-year term; "
                               "Doug Mosle's seat appears in neither "
                               "the 2025 nor the 2026 Warning, so he "
                               "continues; Kirsten Andreae's seat "
                               "stood in 2026 and its outcome is "
                               "unpublished, so it is left "
                               "unfilled.")],
               [holder("Doug Mosle", "doug-mosle"),
                holder("Kim Laidlaw", "kim-laidlaw")]),
        office("second-constable", "Second Constable", "Fayston Second Constable", 1,
               [fayston_report("Chris Griffin was re-elected Second "
                               "Constable in March 2025 for one year; "
                               "the office stood in 2026 and no "
                               "outcome is published. Structure only. "
                               "No First Constable article appears in "
                               "either the 2025 minutes or the 2026 "
                               "Warning, so no First Constable post "
                               "is created.")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Fayston Cemetery Commission", 3,
               [fayston_report("the town elects one cemetery "
                               "commissioner yearly to a three-year "
                               "term, fixing the commission at three "
                               "seats: David Koepele was re-elected "
                               "in March 2025 and Karen Sauther was "
                               "elected in March 2025 to a remainder "
                               "ending 2027; Candace Porter's seat "
                               "stood in 2026, outcome unpublished, "
                               "left unfilled.")],
               [holder("David Koepele", "david-koepele"),
                holder("Karen Sauther", "karen-sauther")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Fayston Justices of the Peace", 5,
               [jp_src("lists five Fayston justices of the peace: "
                       "Peter Forbes, Jared Cadwell, Cynthia "
                       "Seckler, Fedrick Rayfield, and Danielle "
                       "Dukette.")],
               [holder("Peter Forbes", "peter-forbes"),
                holder("Jared Cadwell", "jared-cadwell"),
                holder("Cynthia Seckler", "cynthia-seckler"),
                holder("Fedrick Rayfield", "fedrick-rayfield"),
                holder("Danielle Dukette", "danielle-dukette")]),
    ]
    return spec("fayston", label, offices,
                jp_election("fayston-vt", label, 5,
                            "the SOS listing names the five Fayston "
                            "winners of the November 5, 2024 justice "
                            "of the peace election. The listing's "
                            "'Fedrick Rayfield' is NOT merged with "
                            "Fayston's Moderator Rick Rayfield: the "
                            "name form alone is not a second fact."))


SPECS.append(fayston_spec())

# --------------------------------------------------------- Ferrisburgh
FERR_OFFICIALS = {
    "url": "https://www.ferrisburghvt.org/vertical/Sites/{B16C9BC8-6A0C-4814-B183-6F54A75E8A13}/uploads/FERRSIBURGH_2026_ELECTED_AND_APPOINTED_OFFICERS_LIST.pdf",
    "note": "PLACEHOLDER",
}
FERR_CH119 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/119",
    "note": "PLACEHOLDER",
}


def ferr_officials(note):
    return S(FERR_OFFICIALS, "Town of Ferrisburgh, '2026 Elected & "
             f"Appointed Officials' list (ferrisburghvt.org): {note}")


def ferr_charter(note):
    return S(FERR_CH119, "Ferrisburgh town charter, 24 App. V.S.A. "
             f"ch. 119 (2017 No. M-13): {note}")


def ferrisburgh_spec():
    label = "Town of Ferrisburgh"
    offices = [
        office("selectboard", "Selectboard Member", "Ferrisburgh Selectboard", 5,
               [ferr_officials("lists five elected Selectboard "
                               "members: Chris Campbell (Chair), "
                               "Walter E. Reed II (Vice Chair), Rick "
                               "Ebel (Clerk), James Benoit, and Liz "
                               "Markowski."),
                sb_dir("confirms the Ferrisburgh roster, including "
                       "Liz Markowski; the pre-meeting chair, Clark "
                       "Hinsdale, rotated off at the February 28, "
                       "2026 town meeting and is not seated.")],
               [holder("Christopher Campbell", "christopher-campbell"),
                holder("James Benoit", "james-benoit"),
                holder("Liz Markowski", "liz-markowski"),
                holder("Rick Ebel", "rick-ebel"),
                holder("Walter E. Reed II", "walter-e-reed-ii")]),
        office("moderator", "Moderator", "Ferrisburgh Moderator", 1,
               [ferr_officials("lists Kyle Rowe as elected Town "
                               "Moderator.")],
               [holder("Kyle Rowe", "kyle-rowe")]),
        office("lister", "Lister", "Ferrisburgh Listers", 3,
               [ferr_officials("lists three elected Listers: Brian "
                               "Goodyear (Chair), Roderick Cole, and "
                               "Tim Davis.")],
               [holder("Brian Goodyear", "brian-goodyear"),
                holder("Roderick Cole", "roderick-cole"),
                holder("Tim Davis", "tim-davis")]),
        office("auditor", "Auditor", "Ferrisburgh Auditors", 3,
               [ferr_officials("lists three elected Auditors: "
                               "Andrew Dombek, Eric McEntee, and "
                               "Jarad Roach.")],
               [holder("Andrew Dombek", "andrew-dombek"),
                holder("Eric McEntee", "eric-mcentee"),
                holder("Jarad Roach", "jarad-roach")]),
        office("first-constable", "First Constable", "Ferrisburgh First Constable", 1,
               [ferr_officials("lists Jessy James Amblo as elected "
                               "First Constable; no second constable "
                               "appears anywhere in the town's list, "
                               "so no Second Constable post is "
                               "created.")],
               [holder("Jessy James Amblo", "jessy-james-amblo")]),
        office("town-clerk", "Town Clerk", "Ferrisburgh Town Clerk", 1,
               [ferr_charter("section 3 provides that the Town Clerk "
                             "is appointed by the Selectboard."),
                ferr_officials("lists Jessica James as appointed "
                               "Town Clerk."),
                guide("lists Jessica James as Ferrisburgh Town "
                      "Clerk (January 2026).")],
               [holder("Jessica James", "jessica-james",
                       how_seated="appointed")]),
        office("town-treasurer", "Town Treasurer", "Ferrisburgh Town Treasurer", 1,
               [ferr_charter("section 3 provides that the Town "
                             "Treasurer is appointed by the "
                             "Selectboard."),
                ferr_officials("lists Lydia Sabourin as appointed "
                               "Town Treasurer."),
                guide("lists Lydia Sabourin as Ferrisburgh Town "
                      "Treasurer (January 2026).")],
               [holder("Lydia Sabourin", "lydia-sabourin",
                       how_seated="appointed")]),
        office("collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
               "Ferrisburgh Collector of Delinquent Taxes", 1,
               [ferr_officials("places the Collector of Delinquent "
                               "Taxes under Appointed Officials: Tom "
                               "Steadman.")],
               [holder("Tom Steadman", "tom-steadman",
                       how_seated="appointed")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Ferrisburgh Justices of the Peace", 10,
               [jp_src("lists ten Ferrisburgh justices of the peace: "
                       "Joseph Baker, Robert North, Judy Chaves, "
                       "Chris Kayhart, Art Cohn, Chris McClain, "
                       "Jon-Taylor Vincent, Jean Richardson, Lissa "
                       "Gebo, and Silas Towler. The town's officials "
                       "list concurs (printing 'Judith Chaves'); the "
                       "listing form governs the JP record.")],
               [holder("Joseph Baker", "joseph-baker"),
                holder("Robert North", "robert-north"),
                holder("Judy Chaves", "judy-chaves"),
                holder("Chris Kayhart", "chris-kayhart"),
                holder("Art Cohn", "art-cohn"),
                holder("Chris McClain", "chris-mcclain"),
                holder("Jon-Taylor Vincent", "jon-taylor-vincent"),
                holder("Jean Richardson", "jean-richardson"),
                holder("Lissa Gebo", "lissa-gebo"),
                holder("Silas Towler", "silas-towler")]),
    ]
    return spec("ferrisburgh", label, offices,
                jp_election("ferrisburgh-vt", label, 10,
                            "the SOS listing names the ten "
                            "Ferrisburgh winners of the November 5, "
                            "2024 justice of the peace election."))


SPECS.append(ferrisburgh_spec())

# ------------------------------------------------------------ Fletcher
FLETCHER_REPORT = {
    "url": "https://fletchervt.net/wp-content/uploads/2026/02/2025-Fletcher-Annual-Report.pdf",
    "note": "PLACEHOLDER",
}


def fletcher_report(note):
    return S(FLETCHER_REPORT, "Town of Fletcher 2025 Annual Report "
             "(fletchervt.net), printing the TOWN/SCHOOL OFFICERS "
             f"table and the 2026 Warning: {note}")


def fletcher_spec():
    label = "Town of Fletcher"
    offices = [
        office("selectboard", "Selectboard Member", "Fletcher Selectboard", 5,
               [sb_dir("lists five Fletcher Selectboard members: "
                       "Jennifer Getty (Chair), Matt Gillilan, Alex "
                       "Sargent, Rob Schukei, and Matt Swartz; the "
                       "directory seats all five after the March "
                       "2026 meeting, including the two whose seats "
                       "stood."),
                fletcher_report("the officers table prints Getty, "
                                "Gillilan, Sargent, Schukei, and "
                                "Swartz with terms running to 2027 "
                                "and 2028.")],
               [holder("Matt Gillilan", "matt-gillilan"),
                holder("Jennifer Getty", "jennifer-getty"),
                holder("Alex Sargent", "alex-sargent"),
                holder("Rob Schukei", "rob-schukei"),
                holder("Matt Swartz", "matt-swartz")]),
        office("moderator", "Moderator", "Fletcher Moderator", 1,
               [fletcher_report("the officers table lists David "
                                "Clark as Moderator on a one-year "
                                "term expired 2026; the 2026 Warning "
                                "stood the office and no outcome is "
                                "published. Structure only. Clark is "
                                "seated as a justice of the peace "
                                "below.")]),
        office("town-clerk", "Town Clerk", "Fletcher Town Clerk", 1,
               [fletcher_report("Fletcher elects its Town Clerk and "
                                "Town Treasurer as ONE combined "
                                "ballot office ('Town Clerk & "
                                "Treasurer', three-year term); the "
                                "two standard posts are modeled with "
                                "the combination stated here. Karrie "
                                "Sweet's term expired in 2026, the "
                                "office stood, and no outcome is "
                                "published. Structure only."),
                guide("lists Karrie Sweet as both Fletcher Town "
                      "Clerk and Town Treasurer (January 2026).")]),
        office("town-treasurer", "Town Treasurer", "Fletcher Town Treasurer", 1,
               [fletcher_report("Fletcher elects its Town Treasurer "
                                "jointly with the Town Clerk as one "
                                "combined ballot office ('Town Clerk "
                                "& Treasurer'); see the Town Clerk "
                                "post. Karrie Sweet's term expired in "
                                "2026, the office stood, and no "
                                "outcome is published. Structure "
                                "only."),
                guide("lists Karrie Sweet as both Fletcher Town "
                      "Treasurer and Town Clerk (January 2026).")]),
        office("lister", "Lister", "Fletcher Listers", 3,
               [fletcher_report("the officers table lists Sharon "
                                "Tinker (term to 2027), Andrew Davis, "
                                "and Charles E. Tinker; the Davis "
                                "and C. E. Tinker seats both expired "
                                "in 2026 and stood at the meeting "
                                "(a three-year seat and a two-year "
                                "remainder on the 2026 Warning) with "
                                "no published outcome, so they are "
                                "left unfilled.")],
               [holder("Sharon Tinker", "sharon-tinker")]),
        office("auditor", "Auditor", "Fletcher Auditors", 3,
               [fletcher_report("the officers table lists Nancy "
                                "Cardinal and Andrea Zamuda (terms "
                                "to 2028) and Kathryn Towle; "
                                "Towle's seat stood in 2026 with no "
                                "published outcome, so it is left "
                                "unfilled.")],
               [holder("Nancy Cardinal", "nancy-cardinal"),
                holder("Andrea Zamuda", "andrea-zamuda")]),
        office("first-constable", "First Constable", "Fletcher First Constable", 1,
               [fletcher_report("the officers table lists Bill "
                                "Stygles as First Constable on a "
                                "two-year term running to 2027.")],
               [holder("Bill Stygles", "bill-stygles")]),
        office("collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
               "Fletcher Collector of Delinquent Taxes", 1,
               [fletcher_report("the officers table lists Fred "
                                "Fletcher as Collector of Delinquent "
                                "Taxes on a three-year term expired "
                                "2026; the office stood at the 2026 "
                                "meeting and no outcome is published. "
                                "Structure only.")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Fletcher Justices of the Peace", 3,
               [jp_src("lists three Fletcher justices of the peace: "
                       "Todd Baumeister, Jeremy Ayotte, and David "
                       "Clark; the town's officers table concurs.")],
               [holder("Todd Baumeister", "todd-baumeister"),
                holder("Jeremy Ayotte", "jeremy-ayotte"),
                holder("David Clark", "david-clark")]),
    ]
    return spec("fletcher", label, offices,
                jp_election("fletcher-vt", label, 3,
                            "the SOS listing names the three Fletcher "
                            "winners of the November 5, 2024 justice "
                            "of the peace election."))


SPECS.append(fletcher_spec())

# ------------------------------------------------------------ Franklin
FRANKLIN_SITE = {
    "url": "https://www.franklinvermont.org",
    "note": "PLACEHOLDER",
}
FRANKLIN_OFFICERS = {
    "url": "https://www.franklinvermont.org/other-resources",
    "note": "PLACEHOLDER",
}


def franklin_minutes(note):
    return S(FRANKLIN_SITE, "Town of Franklin official website "
             "(franklinvermont.org), minutes of the March 3, 2026 "
             f"annual town meeting: {note}")


def franklin_spec():
    label = "Town of Franklin"
    offices = [
        office("selectboard", "Selectboard Member", "Franklin Selectboard", 5,
               [franklin_minutes("the meeting elected five "
                                 "Selectboard members by Australian "
                                 "ballot: Peter Magnant, Brooks "
                                 "Sturtevant, Yvon Dandurand, Dave "
                                 "Bennion, and Justin Rainville. "
                                 "DIVERGENCE: the June 2026 SOS "
                                 "directory and the factory carry "
                                 "Michael Grant and Jay Hartman in "
                                 "place of Dandurand and Magnant -- "
                                 "the directory's Franklin entry is "
                                 "stale and the town's own certified "
                                 "meeting record governs.")],
               [holder("Peter Magnant", "peter-magnant"),
                holder("Brooks Sturtevant", "brooks-sturtevant"),
                holder("Yvon Dandurand", "yvon-dandurand"),
                holder("Dave Bennion", "dave-bennion"),
                holder("Justin Rainville", "justin-rainville")]),
        office("town-clerk", "Town Clerk", "Franklin Town Clerk", 1,
               [franklin_minutes("Lisa Larivee was returned on the "
                                 "ballot but DECLINED the clerkship "
                                 "at the meeting; the meeting elected "
                                 "Pauline Gadbois to fill the "
                                 "unexpired term. The SOS Guide "
                                 "(January 2026) still lists Larivee; "
                                 "the town's minutes govern."),
                guide("lists Lisa Larivee as Franklin Town Clerk "
                      "(January 2026) -- superseded by the March 3, "
                      "2026 meeting minutes.")],
               [holder("Pauline Gadbois", "pauline-gadbois")]),
        office("town-treasurer", "Town Treasurer", "Franklin Town Treasurer", 1,
               [franklin_minutes("the meeting re-elected Lisa "
                                 "Larivee Town Treasurer (she "
                                 "declined only the clerkship), and "
                                 "she signs town documents as Town "
                                 "Treasurer in May 2026."),
                guide("lists Lisa Larivee as Franklin Town "
                      "Treasurer (January 2026).")],
               [holder("Lisa Larivee", "lisa-larivee")]),
        office("moderator", "Moderator", "Franklin Moderator", 1,
               [franklin_minutes("the meeting elected Peter Magnant "
                                 "Moderator; the incumbent, Eric "
                                 "Paradee, lost the March 2026 floor "
                                 "election and is not seated.")],
               [holder("Peter Magnant", "peter-magnant")]),
        office("auditor", "Auditor", "Franklin Auditors", 3,
               [franklin_minutes("the meeting elected three "
                                 "auditors: Irene Garceau "
                                 "(re-elected), Emily Felker-"
                                 "Johnston, and Marjorie Taylor (the "
                                 "latter two to one-year terms); "
                                 "the February 2026 budget minutes "
                                 "name the same three as the town's "
                                 "auditors.")],
               [holder("Irene Garceau", "irene-garceau"),
                holder("Emily Felker-Johnston", "emily-felker-johnston"),
                holder("Marjorie Taylor", "marjorie-taylor")]),
        office("constable", "Constable", "Franklin Constable", 1,
               [S(FRANKLIN_OFFICERS, "Town of Franklin Town Officers "
                  "page (franklinvermont.org): lists Burt Maynard as "
                  "Constable."),
                franklin_minutes("no constable was elected at the "
                                  "March 2026 meeting; the "
                                  "Selectboard's April 2026 minutes "
                                  "and the town's appointment "
                                  "announcement record Maynard's "
                                  "appointment to a two-year term. "
                                  "Franklin has a single constable "
                                  "post (no first/second split).")],
               [holder("Burt Maynard", "burt-maynard",
                       how_seated="appointed")]),
        office("lister", "Lister", "Franklin Listers", 3,
               [franklin_minutes("all three listers resigned "
                                 "effective March 3, 2026 and the "
                                 "meeting declined to elect "
                                 "successors; the Selectboard was to "
                                 "appoint interim listers by April "
                                 "15, 2026, but no appointee is named "
                                 "in any source read. Structure "
                                 "only.")]),
        office("trustee-of-public-funds", "Trustee of Public Funds",
               "Franklin Trustees of Public Funds", 3,
               [franklin_minutes("the meeting declined to fill the "
                                 "three Trustee of Public Funds "
                                 "seats and no holders are named in "
                                 "any source read. Structure "
                                 "only.")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Franklin Justices of the Peace", 5,
               [jp_src("lists five Franklin justices of the peace: "
                       "Pauline Gadbois, Kimberly Gates Maynard, "
                       "Peter Magnant, George Godin, and Matthew "
                       "Rainville.")],
               [holder("Pauline Gadbois", "pauline-gadbois"),
                holder("Kimberly Gates Maynard", "kimberly-gates-maynard"),
                holder("Peter Magnant", "peter-magnant"),
                holder("George Godin", "george-godin"),
                holder("Matthew Rainville", "matthew-rainville")]),
    ]
    return spec("franklin", label, offices,
                jp_election("franklin-vt", label, 5,
                            "the SOS listing names the five Franklin "
                            "winners of the November 5, 2024 justice "
                            "of the peace election. Peter Magnant "
                            "also holds the Selectboard and Moderator "
                            "offices, and Pauline Gadbois the Town "
                            "Clerk office, on single person records."))


SPECS.append(franklin_spec())

# ------------------------------------------------------------- Georgia
GEORGIA_ELECTIONS = {
    "url": "https://www.townofgeorgia.com/elections-voting",
    "note": "PLACEHOLDER",
}
GEORGIA_SB_PAGE = {
    "url": "https://www.townofgeorgia.com/selectboard",
    "note": "PLACEHOLDER",
}
GPL_MINUTES = {
    "url": "https://www.georgiapubliclibraryvt.org/uploads/1/3/1/6/131684128/gplbot_01212026.pdf",
    "note": "PLACEHOLDER",
}


def georgia_elections(note):
    return S(GEORGIA_ELECTIONS, "Town of Georgia Elections & Voting "
             "page (townofgeorgia.com), 'Local Offices Open for "
             f"2026': {note}")


def georgia_spec():
    label = "Town of Georgia"
    offices = [
        office("selectboard", "Selectboard Member", "Georgia Selectboard", 5,
               [sb_dir("lists five Georgia Selectboard members: "
                       "Kellie Bosenberg (Chair), Brian Dunsmore "
                       "(Vice Chair), Tammy Hardy, Judith Nasca, and "
                       "Carl Rosenquist."),
                S(GEORGIA_SB_PAGE, "Town of Georgia Selectboard page "
                  "(townofgeorgia.com): the board has five members "
                  "-- three elected to three-year terms and two to "
                  "one-year terms on a staggered basis.")],
               [holder("Kellie Bosenberg", "kellie-bosenberg"),
                holder("Brian Dunsmore", "brian-dunsmore"),
                holder("Tammy Hardy", "tammy-hardy"),
                holder("Judith Nasca", "judith-nasca"),
                holder("Carl Rosenquist", "carl-rosenquist")]),
        office("town-treasurer", "Town Treasurer", "Georgia Town Treasurer", 1,
               [guide("lists Lori Hobart as Georgia Town Treasurer "
                      "(January 2026)."),
                treas_xlsx("lists Lori Hobart as Georgia's "
                           "Treasurer."),
                georgia_elections("the Town Treasurer's office is "
                                  "NOT among the local offices open "
                                  "in 2026, so Hobart's term did not "
                                  "stand at the March 2026 meeting.")],
               [holder("Lori Hobart", "lori-hobart")]),
        office("town-clerk", "Town Clerk", "Georgia Town Clerk", 1,
               [georgia_elections("the Town Clerk's office stood in "
                                  "2026 for a three-year term; no "
                                  "outcome is published. Structure "
                                  "only."),
                guide("lists Cheryl Letourneau as Georgia Town "
                      "Clerk (January 2026).")]),
        office("moderator", "Moderator", "Georgia Moderator", 1,
               [georgia_elections("the Town Moderator's office stood "
                                  "in 2026 for one year; the holder "
                                  "is named in no source read. "
                                  "Structure only.")]),
        office("first-constable", "First Constable", "Georgia First Constable", 1,
               [georgia_elections("the First Constable's office stood "
                                  "in 2026 for one year; the holder "
                                  "is named in no source read. "
                                  "Structure only.")]),
        office("second-constable", "Second Constable", "Georgia Second Constable", 1,
               [georgia_elections("the Second Constable's office "
                                  "stood in 2026 for one year; the "
                                  "holder is named in no source "
                                  "read. Structure only.")]),
        office("library-trustee", "Library Trustee", "Georgia Public Library Trustees", 5,
               [georgia_elections("three Library Trustee seats stood "
                                  "in 2026 for one year -- the seats "
                                  "are elected."),
                S(GPL_MINUTES, "Georgia Public Library trustee "
                  "minutes, January 21, 2026 "
                  "(georgiapubliclibraryvt.org): the board has five "
                  "trustees (Nicole Jamison, Chair; Debbie Mann; "
                  "Kollene Caspers; Terry Cleveland; Craig "
                  "Volatile-Wood). That roster predates the March "
                  "2026 meeting at which three seats stood, so no "
                  "holders are minted. Structure only.")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Georgia Justices of the Peace", 12,
               [jp_src("lists twelve Georgia justice of the peace "
                       "seats, eleven named and one printed 'Open': "
                       "Alan Parent, Jacqui Hood, Ed Ballantyne, "
                       "Karen Brigham, Linda Cramer, Brian Dunsmore, "
                       "Justin Holmes, Paul Jansen, Jen Kale, Craig "
                       "Volatile-Wood, and Tony Heinlein.")],
               [holder("Alan Parent", "alan-parent"),
                holder("Jacqui Hood", "jacqui-hood"),
                holder("Ed Ballantyne", "ed-ballantyne"),
                holder("Karen Brigham", "karen-brigham"),
                holder("Linda Cramer", "linda-cramer"),
                holder("Brian Dunsmore", "brian-dunsmore"),
                holder("Justin Holmes", "justin-holmes"),
                holder("Paul Jansen", "paul-jansen"),
                holder("Jen Kale", "jen-kale"),
                holder("Craig Volatile-Wood", "craig-volatile-wood"),
                holder("Tony Heinlein", "tony-heinlein")]),
    ]
    return spec("georgia", label, offices,
                jp_election("georgia-vt", label, 12,
                            "the SOS listing names eleven Georgia "
                            "winners of the November 5, 2024 justice "
                            "of the peace election and prints the "
                            "twelfth seat as 'Open'; the contest "
                            "carries vote_for 12 with eleven winners "
                            "and the vacancy is the listing's own. "
                            "Georgia elects its Planning "
                            "Commissioners (a four-year seat and a "
                            "one-year remainder stood in 2026), but "
                            "no source read fixes the commission's "
                            "size, so no post is created; the town "
                            "has an appointed Town Assessor (no "
                            "listers) and its audits are performed "
                            "by an outside firm (no auditor post)."))


SPECS.append(georgia_spec())

# -------------------------------------------------------------- Glover
GLOVER_REPORT = {
    "url": "https://townofglover.com/wp-content/uploads/2025-Annual-Town-Report-from-Memphremagog-Press.pdf",
    "note": "PLACEHOLDER",
}
GLOVER_CEMETERY_PAGE = {
    "url": "https://townofglover.com/cemetery-commission/",
    "note": "PLACEHOLDER",
}
GLOVER_SB_MIN = {
    "url": "https://townofglover.com/wp-content/uploads/9-10-26.pdf",
    "note": "PLACEHOLDER",
}


def glover_report(note):
    return S(GLOVER_REPORT, "Town of Glover 2025 Annual Town Report "
             "(townofglover.com), printing the TOWN OFFICERS 2025 "
             "table, the March 4, 2025 meeting minutes, and the "
             f"2026 Warning: {note}")


def glover_spec():
    label = "Town of Glover"
    epinette_srcs = [
        glover_report("the March 2025 minutes record Cynthia "
                      "Epinette elected Town Clerk (Art. 2) and "
                      "Town Treasurer (Art. 4, one-year term)."),
        S(GLOVER_SB_MIN, "Town of Glover Selectboard minutes, "
          "September 10, 2026 (townofglover.com): the agenda "
          "carries Cindy Epinette's 'Town Clerk/Treasurer's "
          "Update' -- she holds both offices after the March 2026 "
          "meeting."),
        guide("lists Cynthia Epinette as both Glover Town Clerk "
              "and Town Treasurer (January 2026)."),
    ]
    offices = [
        office("selectboard", "Selectboard Member", "Glover Selectboard", 3,
               [S(GLOVER_SB_MIN, "Town of Glover Selectboard minutes, "
                  "September 2026 (townofglover.com): Adam "
                  "Heuslein, Anne Eldridge, and Tabitha Armstrong "
                  "sit as the board. The SOS directory publishes no "
                  "Glover roster; the town's own minutes govern."),
                glover_report("the Selectboard turned over "
                              "repeatedly in 2025 (Phil Young "
                              "resigned; Justin Mason and Glenn "
                              "Gage held seats part-year); the "
                              "2026 Warning was signed by Eldridge "
                              "(Chair), Mason, and Heuslein on "
                              "January 22, 2026.")],
               [holder("Adam Heuslein", "adam-heuslein"),
                holder("Anne Eldridge", "anne-eldridge"),
                holder("Tabitha Armstrong", "tabitha-armstrong")]),
        office("town-clerk", "Town Clerk", "Glover Town Clerk", 1,
               epinette_srcs,
               [holder("Cynthia Epinette", "cynthia-epinette")]),
        office("town-treasurer", "Town Treasurer", "Glover Town Treasurer", 1,
               epinette_srcs,
               [holder("Cynthia Epinette", "cynthia-epinette")]),
        office("moderator", "Moderator", "Glover Moderator", 1,
               [glover_report("Nicholas Ecker-Racz was elected "
                              "Moderator in March 2025 (one-year "
                              "term); the office stood in 2026 and "
                              "no outcome is published. Structure "
                              "only.")]),
        office("auditor", "Auditor", "Glover Auditors", 3,
               [glover_report("the 2025 officers table lists "
                              "auditors Andrea Carpentier, Deb "
                              "Clark, and Jonathan Gilbert (who "
                              "served March only), with Theresa "
                              "Daigle appearing October-December; "
                              "the 2026 Warning stood TWO auditor "
                              "seats (a three-year seat and "
                              "Gilbert's two-year remainder) and no "
                              "outcome is published, so no auditor "
                              "is mintable to the currency "
                              "standard. Structure only.")]),
        office("lister", "Lister", "Glover Listers", 3,
               [glover_report("the March 2025 minutes record David "
                              "Olsen elected Lister for three years; "
                              "the 2026 Warning stood the other "
                              "three-year seat and Jason Kennedy's "
                              "two-year remainder, outcomes "
                              "unpublished, left unfilled.")],
               [holder("David Olsen", "david-olsen")]),
        office("library-trustee", "Library Trustee", "Glover Public Library Trustees", 5,
               [glover_report("the town elects one library trustee "
                              "yearly to a five-year term, fixing "
                              "the board at five seats: Andrea Neil "
                              "was elected in March 2025. The other "
                              "four incumbents (Cynthia Epinette, "
                              "Michelle Brouseau, Nancy Rodgers, "
                              "Becky Galloway) hold rotation seats "
                              "one of which stood in 2026; the "
                              "sources do not say whose, so they "
                              "are left unfilled.")],
               [holder("Andrea Neil", "andrea-neil")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Glover Cemetery Commission", 5,
               [S(GLOVER_CEMETERY_PAGE, "Town of Glover Cemetery "
                  "Commission page (townofglover.com, current): "
                  "lists the commission as Joan Alexander, Nick "
                  "Ecker-Racz, Deb McKay, Amy Wright, and Sandy "
                  "Kepler."),
                glover_report("the 2025 officers table lists the "
                              "same five commissioners (printing "
                              "'Deb (McKay) Wesoja'); two seats "
                              "stood in 2026 and the town's live "
                              "page shows the same five, who are "
                              "minted on that concordance.")],
               [holder("Joan Alexander", "joan-alexander"),
                holder("Nicholas Ecker-Racz", "nicholas-ecker-racz"),
                holder("Deb Wesoja", "deb-wesoja"),
                holder("Amy Wright", "amy-wright"),
                holder("Sandy Kepler", "sandy-kepler")]),
        office("cemetery-sexton", "Cemetery Sexton", "Glover Cemetery Sexton", 1,
               [S(GLOVER_CEMETERY_PAGE, "Town of Glover Cemetery "
                  "Commission page (townofglover.com, current): "
                  "names Cindy Epinette as Sexton."),
                glover_report("Cynthia Epinette was elected "
                              "Cemetery Sexton in March 2025 (one-"
                              "year term); the office stood in 2026 "
                              "and the town's live page names her "
                              "in the role.")],
               [holder("Cynthia Epinette", "cynthia-epinette")]),
        office("collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
               "Glover Collector of Delinquent Taxes", 1,
               [glover_report("Cynthia Epinette was elected "
                              "Collector of Delinquent Taxes in "
                              "March 2025 (one-year term); the "
                              "office stood in 2026 and no outcome "
                              "is published. Structure only.")]),
        office("first-constable", "First Constable", "Glover First Constable", 1,
               [glover_report("Job Breitmeyer was elected First "
                              "Constable in March 2025 (one-year "
                              "term); the office stood in 2026 and "
                              "no outcome is published. Structure "
                              "only.")]),
        office("second-constable", "Second Constable", "Glover Second Constable", 1,
               [glover_report("Cynthia Epinette was elected Second "
                              "Constable in March 2025 (one-year "
                              "term); the office stood in 2026 and "
                              "no outcome is published. Structure "
                              "only.")]),
        office("agent-to-deed-town-owned-property", "Agent to Deed Town-Owned Property",
               "Glover Agent to Deed Town-Owned Property", 1,
               [glover_report("Cynthia Epinette was elected Agent "
                              "to deed town-owned property in March "
                              "2025 (one-year term); the office "
                              "stood in 2026 and no outcome is "
                              "published. Structure only.")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Glover Justices of the Peace", 5,
               [jp_src("lists five Glover justices of the peace: "
                       "Carol Borland, Sarah Becky Galloway, Leanne "
                       "Harple, Elizabeth Nelson, and Carmella "
                       "Young. Harple is the sitting Orleans-4 state "
                       "representative; her existing state-tier "
                       "person record is reused.")],
               [holder("Carol Borland", "carol-borland"),
                holder("Sarah Becky Galloway", "sarah-becky-galloway"),
                holder("Leanne Harple", "leanne-harple",
                       existing_person_id="ocd-person/bd050ca5-369a-531e-8530-8d39ab1a1aa7"),
                holder("Elizabeth Nelson", "elizabeth-nelson"),
                holder("Carmella Young", "carmella-young")]),
    ]
    return spec("glover", label, offices,
                jp_election("glover-vt", label, 5,
                            "the SOS listing names the five Glover "
                            "winners of the November 5, 2024 justice "
                            "of the peace election."))


SPECS.append(glover_spec())

# -------------------------------------------------------------- Goshen
GOSHEN_MODES = {
    "url": "https://goshenvt.org/elected-officials/",
    "note": "PLACEHOLDER",
}
GOSHEN_SB_PAGE = {
    "url": "https://goshenvt.org/selectboard/",
    "note": "PLACEHOLDER",
}
GOSHEN_AUDITORS = {
    "url": "https://goshenvt.org/auditors/",
    "note": "PLACEHOLDER",
}
GOSHEN_CONSTABLES = {
    "url": "https://goshenvt.org/constables/",
    "note": "PLACEHOLDER",
}
GOSHEN_TPF = {
    "url": "https://goshenvt.org/trustee-of-public-funds/",
    "note": "PLACEHOLDER",
}
GOSHEN_CEMETERY = {
    "url": "https://goshenvt.org/cemetery-commission/",
    "note": "PLACEHOLDER",
}
GOSHEN_LISTERS = {
    "url": "https://goshenvt.org/listers/",
    "note": "PLACEHOLDER",
}


def goshen_modes(note):
    return S(GOSHEN_MODES, "Town of Goshen Elected Officials page "
             "(goshenvt.org), the town's own map of its elected "
             f"offices: {note}")


def goshen_spec():
    label = "Town of Goshen"
    offices = [
        office("selectboard", "Selectboard Member", "Goshen Selectboard", 3,
               [sb_dir("lists three Goshen Selectboard members: "
                       "Thomasina Magoon (Chair), Jasmine Hoffman, "
                       "and Timothee Moffi."),
                S(GOSHEN_SB_PAGE, "Town of Goshen Selectboard page "
                  "(goshenvt.org): names Thomasina Magoon (Chair) "
                  "and Timmi Moffi; the town's familiar 'Timmi' "
                  "form is noted, and the SOS directory's "
                  "'Timothee Moffi' governs the person record.")],
               [holder("Thomasina Magoon", "thomasina-magoon"),
                holder("Jasmine Hoffman", "jasmine-hoffman"),
                holder("Timothee Moffi", "timothee-moffi")]),
        office("town-clerk", "Town Clerk", "Goshen Town Clerk", 1,
               [clerk_xlsx("lists Martin Fjeld as Goshen Town "
                           "Clerk."),
                guide("lists Martin Fjeld as Goshen Town Clerk "
                      "(January 2026).")],
               [holder("Martin Fjeld", "martin-fjeld")]),
        office("town-treasurer", "Town Treasurer", "Goshen Town Treasurer", 1,
               [treas_xlsx("lists Heidi Larson as Goshen's "
                           "Treasurer."),
                guide("lists Heidi Larson as Goshen Town Treasurer "
                      "(January 2026).")],
               [holder("Heidi Larson", "heidi-larson")]),
        office("moderator", "Moderator", "Goshen Moderator", 1,
               [goshen_modes("lists the Moderator as an elected "
                             "office in Goshen."),
                statute2646_structure("a town moderator")]),
        office("lister", "Lister", "Goshen Listers", 3,
               [goshen_modes("lists the Listers as an elected office "
                             "in Goshen."),
                S(GOSHEN_LISTERS, "Town of Goshen Listers page "
                  "(goshenvt.org): prints surnames only (Brown, "
                  "Fjeld, Reider, Walsh, Walsh-Viko), which do not "
                  "identify the three listers to the standard for "
                  "minting. Structure only.")]),
        office("auditor", "Auditor", "Goshen Auditors", 3,
               [S(GOSHEN_AUDITORS, "Town of Goshen Auditors page "
                  "(goshenvt.org): names the town's three auditors "
                  "-- Barbara Walsh, Fran Viko, and Charlotte "
                  "Reider-Smith.")],
               [holder("Barbara Walsh", "barbara-walsh"),
                holder("Fran Viko", "fran-viko"),
                holder("Charlotte Reider-Smith", "charlotte-reider-smith")]),
        office("first-constable", "First Constable", "Goshen First Constable", 1,
               [S(GOSHEN_CONSTABLES, "Town of Goshen Constables page "
                  "(goshenvt.org): the town has two active "
                  "constables and names Marci Hayes as First "
                  "Constable. The page does not state the mode of "
                  "appointment or election; the office is recorded "
                  "as elected under the 17 V.S.A. section 2646 "
                  "default.")],
               [holder("Marci Hayes", "marci-hayes")]),
        office("second-constable", "Second Constable", "Goshen Second Constable", 1,
               [S(GOSHEN_CONSTABLES, "Town of Goshen Constables page "
                  "(goshenvt.org): confirms a second constable "
                  "serves, but the holder's name does not appear "
                  "in the page's published text. Structure only.")]),
        office("collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
               "Goshen Collector of Delinquent Taxes", 1,
               [goshen_modes("lists the Collector of Delinquent "
                             "Taxes as an elected office in "
                             "Goshen."),
                statute2646_structure("a collector of delinquent "
                                      "taxes where the town elects "
                                      "one")]),
        office("trustee-of-public-funds", "Trustee of Public Funds",
               "Goshen Trustees of Public Funds", 3,
               [goshen_modes("lists the Trustees of Public Funds as "
                             "an elected office in Goshen (three "
                             "trustees)."),
                S(GOSHEN_TPF, "Town of Goshen Trustee of Public "
                  "Funds page (goshenvt.org): names two of the "
                  "three trustees -- Diane O'Classen and Vickee "
                  "Whiting; the third seat is left unfilled.")],
               [holder("Diane O'Classen", "diane-oclassen"),
                holder("Vickee Whiting", "vickee-whiting")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Goshen Cemetery Commission", 3,
               [S(GOSHEN_CEMETERY, "Town of Goshen Cemetery "
                  "Commission page (goshenvt.org): the commission "
                  "maintains the town's three cemeteries and its "
                  "contact block names three commissioners -- Ken "
                  "Brown, Diane O'Classen, and Tammy Walsh. The "
                  "page does not state the mode; a standalone town "
                  "cemetery commission is an elected body under "
                  "18 V.S.A. section 5373, and the three are "
                  "recorded as elected on that basis (flagged on "
                  "issue #163).")],
               [holder("Ken Brown", "ken-brown"),
                holder("Diane O'Classen", "diane-oclassen"),
                holder("Tammy Walsh", "tammy-walsh")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Goshen Justices of the Peace", 5,
               [jp_src("lists five Goshen justices of the peace: "
                       "Ken Brown, Marci Hayes, Jasmine Hoffman, "
                       "Diane O'Classen, and Barbara Walsh.")],
               [holder("Ken Brown", "ken-brown"),
                holder("Marci Hayes", "marci-hayes"),
                holder("Jasmine Hoffman", "jasmine-hoffman"),
                holder("Diane O'Classen", "diane-oclassen"),
                holder("Barbara Walsh", "barbara-walsh")]),
    ]
    return spec("goshen", label, offices,
                jp_election("goshen-vt", label, 5,
                            "the SOS listing names the five Goshen "
                            "winners of the November 5, 2024 justice "
                            "of the peace election. No Grand Juror "
                            "or Town Agent posts are created "
                            "(absent from the town's own "
                            "elective-office map)."))


SPECS.append(goshen_spec())

# ------------------------------------------------------------- Grafton
GRAFTON_TABLE = {
    "url": "https://graftonvt.org/wp-content/uploads/2025/01/Town-Report-2024-Digital-2025.pdf",
    "note": "PLACEHOLDER",
}


def grafton_table(note):
    return S(GRAFTON_TABLE, "Town of Grafton 2024 Town Report, "
             "OFFICERS table as of June 30, 2024 (graftonvt.org): "
             f"{note}")


def grafton_spec():
    label = "Town of Grafton"
    offices = [
        office("selectboard", "Selectboard Member", "Grafton Selectboard", 5,
               [sb_dir("lists five Grafton Selectboard members: "
                       "Cathy Goodwin-Siano (Chair), Anna Keegan "
                       "(Vice Chair), John Gregory, Warren Fisher, "
                       "and Peter Richardson. The factory prints "
                       "the chair's surname as 'Siano-Goodwin'; "
                       "the directory's order governs.")],
               [holder("Cathy Goodwin-Siano", "cathy-goodwin-siano"),
                holder("Anna Keegan", "anna-keegan"),
                holder("John Gregory", "john-gregory"),
                holder("Warren Fisher", "warren-fisher"),
                holder("Peter Richardson", "peter-richardson")]),
        office("town-clerk", "Town Clerk", "Grafton Town Clerk", 1,
               [grafton_table("Kim Record holds the clerkship on a "
                              "2023 three-year term expiring 2026; "
                              "the seat stood at the March 2026 "
                              "meeting and no outcome is published, "
                              "so the seat is left unfilled (the "
                              "Fayston rule)."),
                clerk_xlsx("lists Kim Record as Grafton Town Clerk "
                           "(2026 contact directory).")]),
        office("town-treasurer", "Town Treasurer", "Grafton Town Treasurer", 1,
               [grafton_table("Kim Record holds the treasurership "
                              "on a 2023 three-year term expiring "
                              "2026; the seat stood in March 2026 "
                              "and no outcome is published. "
                              "Structure only."),
                treas_xlsx("lists Kim Record as Grafton's "
                           "Treasurer (2026 contact directory).")]),
        office("auditor", "Auditor", "Grafton Auditors", 3,
               [grafton_table("lists auditors Arlene Carey (term to "
                              "2027), Heather Gregory (term to "
                              "2025), and Debe Plummer (term to "
                              "2026); Carey's printed term runs "
                              "past the March 2026 meeting, while "
                              "the other two seats stood in 2025 "
                              "and 2026 with no published outcomes "
                              "and are left unfilled.")],
               [holder("Arlene Carey", "arlene-carey")]),
        office("lister", "Lister", "Grafton Listers", 3,
               [grafton_table("lists listers Nancy Merrill (term to "
                              "2027), GailAnn Fisher (term to 2025), "
                              "and Hardy Merrill (term to 2026); "
                              "only Nancy Merrill's printed term "
                              "runs past the March 2026 meeting.")],
               [holder("Nancy Merrill", "nancy-merrill")]),
        office("trustee-of-public-funds", "Trustee of Public Funds",
               "Grafton Trustees of Public Funds", 3,
               [grafton_table("lists Trustees of Public Funds "
                              "Kimberly Record (term to 2027), "
                              "GailAnn Fisher (term to 2025), and "
                              "Wendy Martin (term to 2026); only "
                              "Record's printed term runs past the "
                              "March 2026 meeting.")],
               [holder("Kimberly Record", "kimberly-record")]),
        office("trustee-of-campbell-and-woolson-funds",
               "Trustee of Campbell & Woolson Funds",
               "Grafton Trustees of Campbell & Woolson Funds", 3,
               [grafton_table("Grafton elects a separate three-"
                              "member board of Trustees of Campbell "
                              "& Woolson Funds on the same rotation "
                              "as the Trustees of Public Funds: "
                              "Kimberly Record (term to 2027) is "
                              "minted; the seats expiring in 2025 "
                              "and 2026 stood with no published "
                              "outcomes and are left unfilled.")],
               [holder("Kimberly Record", "kimberly-record")]),
        office("collector-of-delinquent-taxes", "Collector of Delinquent Taxes",
               "Grafton Collector of Delinquent Taxes", 1,
               [grafton_table("Grafton elects its Collector of "
                              "Delinquent Taxes: Michelle Dolloph "
                              "held a three-year term expiring 2026; "
                              "the seat stood in March 2026 and no "
                              "outcome is published. Structure "
                              "only.")]),
        office("town-agent", "Town Agent", "Grafton Town Agent", 1,
               [grafton_table("lists Kimberly Record as Town Agent "
                              "on a one-year term; the office stood "
                              "in 2026 and no outcome is published. "
                              "Structure only.")]),
        office("moderator", "Moderator", "Grafton Moderator", 1,
               [grafton_table("lists David Culver as Moderator on a "
                              "one-year term; the office stood in "
                              "2026 and no outcome is published. "
                              "Structure only.")]),
        office("constable", "Constable", "Grafton Constable", 1,
               [grafton_table("places the Constable under "
                              "'Appointed by Select Board' (Mike "
                              "Waysville, as of June 30, 2024): the "
                              "office is filled by appointment in "
                              "Grafton, and the only named appointee "
                              "is of 2024 vintage, too stale to "
                              "mint. Structure only.")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Grafton Justices of the Peace", 5,
               [jp_src("lists five Grafton justices of the peace: "
                       "Christopher Wallace, Wendy Martin, Mary "
                       "Feder, David Hall, and Samuel Battaglino. "
                       "The town's 2024 report prints the November "
                       "2022 slate (with David Whittall); the "
                       "November 2024 listing governs.")],
               [holder("Christopher Wallace", "christopher-wallace"),
                holder("Wendy Martin", "wendy-martin"),
                holder("Mary Feder", "mary-feder"),
                holder("David Hall", "david-hall"),
                holder("Samuel Battaglino", "samuel-battaglino")]),
    ]
    return spec("grafton", label, offices,
                jp_election("grafton-vt", label, 5,
                            "the SOS listing names the five Grafton "
                            "winners of the November 5, 2024 justice "
                            "of the peace election."))


SPECS.append(grafton_spec())

# ---------------------------------------------------------- Grand Isle
GI_SB_PAGE = {
    "url": "https://grandislevt.org/boards-minutes-agendas/selectboard/",
    "note": "PLACEHOLDER",
}


def gi_sb(note):
    return S(GI_SB_PAGE, "Town of Grand Isle Selectboard page "
             f"(grandislevt.org): {note}")


def grand_isle_spec():
    label = "Town of Grand Isle"
    offices = [
        office("selectboard", "Selectboard Member", "Grand Isle Selectboard", 5,
               [gi_sb("lists five Selectboard members with printed "
                      "term expirations, all running past the March "
                      "2026 meeting: Jennifer Morway (Chair, to "
                      "2027), Aimee Cochran (Vice Chair, to 2028), "
                      "Ron Bushway (to 2029 -- the seat filled in "
                      "March 2026), Ellen Howrigan (to 2027), and "
                      "Jeff Parizo (to 2028). The SOS directory "
                      "publishes no Grand Isle roster; the town's "
                      "own page governs and the factory concurs "
                      "5/5.")],
               [holder("Jennifer Morway", "jennifer-morway"),
                holder("Aimee Cochran", "aimee-cochran"),
                holder("Ron Bushway", "ron-bushway"),
                holder("Ellen Howrigan", "ellen-howrigan"),
                holder("Jeff Parizo", "jeff-parizo")]),
        office("town-clerk", "Town Clerk", "Grand Isle Town Clerk", 1,
               [clerk_xlsx("lists Melissa Boutin as Grand Isle Town "
                           "Clerk."),
                guide("lists Melissa Boutin as Grand Isle Town "
                      "Clerk (January 2026).")],
               [holder("Melissa Boutin", "melissa-boutin")]),
        office("town-treasurer", "Town Treasurer", "Grand Isle Town Treasurer", 1,
               [guide("lists Melissa Boutin as both Grand Isle Town "
                      "Clerk and Town Treasurer (January 2026)."),
                treas_xlsx("refers Grand Isle's treasurer contact to "
                           "the Town Clerk.")],
               [holder("Melissa Boutin", "melissa-boutin")]),
        office("moderator", "Moderator", "Grand Isle Moderator", 1,
               [statute2646_structure("a town moderator")]),
        office("lister", "Lister", "Grand Isle Listers", 3,
               [statute2646_structure("town listers")]),
        office("auditor", "Auditor", "Grand Isle Auditors", 3,
               [statute2646_structure("town auditors")]),
        office("grand-juror", "Grand Juror", "Grand Isle Grand Juror", 1,
               [statute2646_structure("a grand juror")]),
        office("town-agent", "Town Agent", "Grand Isle Town Agent", 1,
               [statute2646_structure("a town agent")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Grand Isle Justices of the Peace", 3,
               [jp_src("lists three Grand Isle justices of the "
                       "peace: Susan Lawrence, AnnaMarie DeMars, "
                       "and Howard DeMars.")],
               [holder("Susan Lawrence", "susan-lawrence"),
                holder("AnnaMarie DeMars", "annamarie-demars"),
                holder("Howard DeMars", "howard-demars")]),
    ]
    return spec("grand-isle", label, offices,
                jp_election("grand-isle-vt", label, 3,
                            "the SOS listing names the three Grand "
                            "Isle winners of the November 5, 2024 "
                            "justice of the peace election. No "
                            "Constable post is created (seat count "
                            "unverifiable) and no Collector of "
                            "Delinquent Taxes post (the treasurer is "
                            "collector ex officio unless the town "
                            "votes otherwise). Grand Isle drafted a "
                            "town charter in August 2026 that is NOT "
                            "adopted; the town is built under "
                            "general law."))


SPECS.append(grand_isle_spec())

# -------------------------------------------------------------- Granby
def granby_spec():
    label = "Town of Granby"
    offices = [
        office("selectboard", "Selectboard Member", "Granby Selectboard", 3,
               [sb_dir("lists three Granby Selectboard members: "
                       "Reginald Bunnell (Chair), Tyler Fournier, "
                       "and R. Terry Williams. Granby has no "
                       "official website in any source read; this "
                       "is a Bloomfield-shape SOS build. The "
                       "factory prints 'Raymond \"Terry\" Williams'; "
                       "the directory form governs.")],
               [holder("Reginald Bunnell", "reginald-bunnell"),
                holder("Tyler Fournier", "tyler-fournier"),
                holder("R. Terry Williams", "r-terry-williams")]),
        office("town-clerk", "Town Clerk", "Granby Town Clerk", 1,
               [clerk_xlsx("lists Terri Williams as Granby Town "
                           "Clerk."),
                guide("lists Terri Lynn Williams as Granby Town "
                      "Clerk (January 2026). She is a distinct "
                      "person from Selectboard member R. Terry "
                      "(Raymond) Williams: different full names and "
                      "roles.")],
               [holder("Terri Williams", "terri-williams")]),
        office("town-treasurer", "Town Treasurer", "Granby Town Treasurer", 1,
               [treas_xlsx("lists Terri Williams as Granby's "
                           "Treasurer."),
                guide("lists Terri Lynn Williams as Granby Town "
                      "Treasurer (January 2026).")],
               [holder("Terri Williams", "terri-williams")]),
        office("moderator", "Moderator", "Granby Moderator", 1,
               [statute2646_structure("a town moderator")]),
        office("lister", "Lister", "Granby Listers", 3,
               [statute2646_structure("town listers")]),
        office("auditor", "Auditor", "Granby Auditors", 3,
               [statute2646_structure("town auditors")]),
        office("grand-juror", "Grand Juror", "Granby Grand Juror", 1,
               [statute2646_structure("a grand juror")]),
        office("town-agent", "Town Agent", "Granby Town Agent", 1,
               [statute2646_structure("a town agent")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Granby Justices of the Peace", 5,
               [jp_src("lists five Granby justices of the peace: "
                       "Robert Peters, Sonia Peters, Reginald "
                       "Bunnell, Bruce Berryman, and John Noble.")],
               [holder("Robert Peters", "robert-peters"),
                holder("Sonia Peters", "sonia-peters"),
                holder("Reginald Bunnell", "reginald-bunnell"),
                holder("Bruce Berryman", "bruce-berryman"),
                holder("John Noble", "john-noble")]),
    ]
    return spec("granby", label, offices,
                jp_election("granby-vt", label, 5,
                            "the SOS listing names the five Granby "
                            "winners of the November 5, 2024 justice "
                            "of the peace election. No Constable "
                            "post is created (seat count "
                            "unverifiable) and no Collector of "
                            "Delinquent Taxes post (treasurer ex "
                            "officio default)."))


SPECS.append(granby_spec())

# ---------------------------------------------------------------- run
for s in SPECS:
    p = OUT / f"{s['place_slug']}.json"
    p.write_text(json.dumps(s, indent=1))
    n_off = len(s["offices"])
    n_hold = sum(len(o.get("holders", ())) for o in s["offices"])
    print(f"{s['place_slug']}: {n_off} offices, {n_hold} holders")
print(f"wrote {len(SPECS)} specs")
