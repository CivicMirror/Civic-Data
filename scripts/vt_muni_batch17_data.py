#!/usr/bin/env python3
"""Batch 17 of the VT #163 municipal fan-out (alphabetical positions
160-169): North Troy (village), Northfield, Norton, Norwich, Old
Bennington (village), Orange, Orleans (village), Orwell, Panton,
Pawlet. Emits one JSON spec per municipality for
build_vt_municipality.py. Research: vt_muni_batch17_research.md.

Identity calls baked into this batch (all flagged on #163):
- Northfield's JP slate is the SOS listing's full FOURTEEN names:
  the listing's Northfield block crosses a page break and the
  local extract had truncated it at nine; the town report's
  party-tagged JP table names the same fourteen.
- Norwich Selectboard member Robert Gere is minted ELECTED as a
  write-in winner: the town's official marked ballot for
  March 3, 2026 tallies the 2-year seat's write-ins by hand as
  "GERE: 342 SMITH: 290."
- Orange's Town Clerk (Jonathan Danchik), Treasurer (Diane
  Hallenbeck), and Delinquent Tax Collector (John McNeil) are
  minted APPOINTED on the town officers page's own
  elected/appointed classification; the SOS Guide's Nikki
  Tomlinson has departed both the clerk's and treasurer's
  offices.
- Northfield's Water & Wastewater and Electric Utility
  commissioners are NOT modeled: ch. 129D sections 303-304 seat
  their elected members by a ratepayer franchise (restricted
  franchise, out of scope under the 2026-10-15 rule).
- North Troy: the charter (ch. 253 section 5) lists a Clerk,
  Treasurer, three Fire Wardens, and an Attorney as elected,
  but the village's March 17, 2026 annual meeting elected only
  a Moderator, one Trustee, two library trustees, and the
  Delinquent Tax Collector; the clerk/treasurer functions are
  an employee position. No posts for the unexercised charter
  offices. The Town/Village merger is pending a reconsideration
  revote on November 9, 2026 (effective July 1, 2027 if
  approved); the village is modeled as standing.
- Old Bennington's Ed Woods is minted as a NEW person distinct
  from the Town of Bennington Select Board member of the same
  name already in the repo: the identity is unproven (no source
  states the village trustee and the town selectman are the
  same person), so per the batch-8 Jessica Chase precedent the
  records stay separate and the possible identity is flagged.
- Northfield's Tim Davis (Selectboard) is a new person distinct
  from Ferrisburgh's lister Tim Davis; Panton's Kyle Rowe
  (Clerk/Treasurer) is a new person distinct from Ferrisburgh's
  moderator Kyle Rowe (the two hold concurrent resident offices
  in different towns). Both new files take collision suffixes.
- Pawlet First Constable Thomas Covino is minted on an
  elimination: the town report names Covino and Mark Gutel as
  the town's two constables and the only constable seat on the
  certified March 3, 2026 certificate was the Second Constable
  seat, won by Gutel, so Covino holds the First Constable seat,
  which did not stand.
- Panton's Water Commissioners ARE modeled: they are elected
  on the town ballot by the whole checklist (general
  franchise), three seats per the town report's officers table.
- Orleans Village is a structure-only charter build (ch. 261):
  no official source publishes its current holders and the
  factory holds it too. Its charter-elected fire engineers get
  no posts (fire-officers scope question).
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
CHARTER_253 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/253",
    "note": "PLACEHOLDER",
}
CHARTER_129D = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/129D",
    "note": "PLACEHOLDER",
}
CHARTER_261 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/261",
    "note": "PLACEHOLDER",
}
NT_TRUSTEES = {
    "url": "https://www.troyvt.gov/village/trustees",
    "note": "PLACEHOLDER",
}
NT_ANNUAL = {
    "url": "https://www.troyvt.gov/fileadmin/files/Village/Trustees/Meetings/2026/04/2026_Village_meeting_minutes.pdf",
    "note": "PLACEHOLDER",
}
NT_OFFICE = {
    "url": "https://www.troyvt.gov/village/village-office",
    "note": "PLACEHOLDER",
}
NF_SB = {
    "url": "https://www.northfield-vt.gov/select-board",
    "note": "PLACEHOLDER",
}
NF_REPORT = {
    "url": "https://www.northfield-vt.gov/_files/ugd/13fb68_7162d3578f974b7cb5dc9de55216c910.pdf",
    "note": "PLACEHOLDER",
}
NF_LISTERS = {
    "url": "https://www.northfield-vt.gov/board-of-listers",
    "note": "PLACEHOLDER",
}
NW_BALLOT = {
    "url": "https://norwich.vt.us/wp-content/uploads/2026/03/20260303210433.pdf",
    "note": "PLACEHOLDER",
}
NW_CEMETERY = {
    "url": "https://norwich.vt.us/boards-and-committees/cemetery-commission/",
    "note": "PLACEHOLDER",
}
NW_LISTERS = {
    "url": "https://norwich.vt.us/listers/",
    "note": "PLACEHOLDER",
}
OB_WARNING = {
    "url": "http://img1.wsimg.com/blobby/go/2bb07981-6db0-4f22-adf0-09e315e1afda/downloads/f507b438-ce3c-458a-898a-59ce25006338/Warning%2C%20annual%20meeting%2C%20May%2012%2C%202026.pdf?ver=1778930911888",
    "note": "PLACEHOLDER",
}
OB_MINUTES = {
    "url": "http://img1.wsimg.com/blobby/go/2bb07981-6db0-4f22-adf0-09e315e1afda/downloads/0ef67329-ccf9-4928-b2f5-5d896cf4cb92/Minutes%2C%20Trustees%20meeting%2C%20June%202%2C%202026.pdf?ver=1784223627565",
    "note": "PLACEHOLDER",
}
OB_REPORT = {
    "url": "http://img1.wsimg.com/blobby/go/2bb07981-6db0-4f22-adf0-09e315e1afda/downloads/ec5b6c34-c51d-457b-9096-f35704f78be6/Village%20of%20Old%20Bennington%2C%20Annual%20Report%2C%202026.pdf?ver=1783524059701",
    "note": "PLACEHOLDER",
}
OR_OFFICERS = {
    "url": "https://www.orangevt.org/town-office/",
    "note": "PLACEHOLDER",
}
OW_RESULTS = {
    "url": "https://townoforwellvt.org/election-results-2/",
    "note": "PLACEHOLDER",
}
OW_LISTERS = {
    "url": "https://townoforwellvt.org/listers/",
    "note": "PLACEHOLDER",
}
OW_AUDIT = {
    "url": "https://townoforwellvt.org/audit-committee/",
    "note": "PLACEHOLDER",
}
PA_RETURN = {
    "url": "https://pantonvt.gov/wp-content/uploads/sites/52/2026/08/2026-Panton-Town-Meeting-Results.pdf",
    "note": "PLACEHOLDER",
}
PA_REPORT = {
    "url": "https://pantonvt.gov/wp-content/uploads/sites/52/2026/08/2025-Town-Report.pdf",
    "note": "PLACEHOLDER",
}
PA_ASSESSOR = {
    "url": "https://pantonvt.gov/departments/assessor/",
    "note": "PLACEHOLDER",
}
PW_CERT = {
    "url": "https://pawlet.vt.gov/wp-content/uploads/2026/03/Certificate-of-vote-1.pdf",
    "note": "PLACEHOLDER",
}
PW_REPORT = {
    "url": "https://pawlet.vt.gov/wp-content/uploads/2026/02/Pawlet-Town-Report.pdf",
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


def charter253(phrase):
    return S(CHARTER_253, f"24 App. V.S.A. ch. 253 (Village of "
             f"North Troy): {phrase}")


def charter129d(phrase):
    return S(CHARTER_129D, f"24 App. V.S.A. ch. 129D (Town of "
             f"Northfield): {phrase}")


def charter261(phrase):
    return S(CHARTER_261, f"24 App. V.S.A. ch. 261 (Village of "
             f"Orleans): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 17); issue #163 "
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
                  f"# municipal fan-out batch 17; issue #163 "
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
# Village of North Troy (Orleans County) -- charter ch. 253.
SPECS["north-troy"] = spec("north-troy", "Village of North Troy", [
    office("moderator", "Village Moderator",
           "Village of North Troy Moderator", 1,
           [charter253("section 5 provides for a Moderator elected "
                       "at the annual meeting"),
            S(NT_ANNUAL, "Village of North Troy, Annual Village "
                         "Meeting Minutes, March 17, 2026: Helene "
                         "Croteau was nominated and elected "
                         "Moderator by voice vote")],
           [holder("Helene Croteau", "helene-croteau")]),
    office("village-trustee", "Village Trustee",
           "Village of North Troy Board of Trustees", 3,
           [charter253("section 5 provides for three trustees on "
                       "staggered three-year terms, one elected "
                       "each year"),
            S(NT_TRUSTEES, "Village of North Troy, Board of "
                           "Trustees page (troyvt.gov): lists "
                           "Terri Medley (Chair), Holly Ross, and "
                           "Helene Croteau as the village trustees"),
            S(NT_ANNUAL, "Village of North Troy, Annual Village "
                         "Meeting Minutes, March 17, 2026: Terri "
                         "Medley was re-elected trustee for a "
                         "three-year term")],
           [holder("Terri Medley", "terri-medley"),
            holder("Holly Ross", "holly-ross"),
            holder("Helene Croteau", "helene-croteau")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Village of North Troy Collector of Delinquent Taxes", 1,
           [charter253("section 5 provides for a Collector of "
                       "Taxes elected at the annual meeting; "
                       "village practice styles the office "
                       "Delinquent Tax Collector"),
            S(NT_ANNUAL, "Village of North Troy, Annual Village "
                         "Meeting Minutes, March 17, 2026: April "
                         "Descheneau was elected Delinquent Tax "
                         "Collector"),
            S(NT_OFFICE, "Village of North Troy, Village Office "
                         "page (troyvt.gov): lists April "
                         "Descheneau as Delinquent Tax Collector")],
           [holder("April Descheneau", "april-descheneau")]),
])

# ----------------------------------------------------------------
# Town of Northfield (Washington County) -- charter ch. 129D.
SPECS["northfield"] = spec("northfield", "Town of Northfield", [
    office("selectboard", "Selectboard Member",
           "Northfield Selectboard", 5,
           [charter129d("section 302 provides for a five-member "
                        "Select Board"),
            sb_dir("lists the Northfield selectboard: Tim Davis, "
                   "David Maxwell, Lydia Petty, Merry Shernock, "
                   "and John Stevens"),
            S(NF_SB, "Town of Northfield, Select Board page: "
                     "lists him as K. David Maxwell (Chair, term "
                     "to 2027), "
                     "Merry Shernock (Vice Chair, term to 2027), "
                     "Lydia Petty (term to 2028), Tim Davis (term "
                     "to 2028), and John B. Stevens (term to "
                     "2029); the board's former chair Charles L. "
                     "Morse's term ended in 2026 and he no longer "
                     "sits")],
           [holder("David Maxwell", "david-maxwell"),
            holder("Merry Shernock", "merry-shernock"),
            holder("Lydia Petty", "lydia-petty"),
            holder("Tim Davis", "tim-davis"),
            holder("John B. Stevens", "john-b-stevens")]),
    office("town-clerk", "Town Clerk", "Northfield Town Clerk", 1,
           [guide("names Kim Pedley as Northfield's town clerk"),
            S(NF_REPORT, "Town of Northfield, 2026 Town Report, "
                         "Elected Officers table: Kim Pedley, "
                         "Town Clerk, term to 2027")],
           [holder("Kim Pedley", "kim-pedley")]),
    office("town-treasurer", "Town Treasurer",
           "Northfield Town Treasurer", 1,
           [guide("names Kim Pedley as Northfield's town "
                  "treasurer"),
            S(NF_REPORT, "Town of Northfield, 2026 Town Report, "
                         "Elected Officers table: Kim Pedley, "
                         "Town Treasurer, term to 2028")],
           [holder("Kim Pedley", "kim-pedley")]),
    office("moderator", "Town Moderator", "Northfield Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term at the annual meeting"),
            S(NF_REPORT, "Town of Northfield, 2026 Town Report: "
                         "the March 2026 warning (Article 1) stood "
                         "a moderator for a one-year term; the "
                         "report's Elected Officers table carries "
                         "Cassie Morse as moderator for a term "
                         "ended in 2026, and no official source "
                         "publishes the 2026 outcome, so the post "
                         "is created without a membership")]),
    office("lister", "Lister", "Northfield Board of Listers", 3,
           [statute2646("towns elect a board of listers of three "
                        "members on staggered terms"),
            S(NF_LISTERS, "Town of Northfield, Board of Listers "
                          "page: names only the chair, Thomas "
                          "Alsheimer"),
            S(NF_REPORT, "Town of Northfield, 2026 Town Report, "
                         "Elected Officers table: Thomas "
                         "Alsheimer (Chair), term to 2027; the "
                         "other two seats stood at the March 2026 "
                         "election (a three-year seat and a "
                         "two-year remainder) and no official "
                         "source publishes their outcome, so two "
                         "seats are created without memberships")],
           [holder("Thomas Alsheimer", "thomas-alsheimer")]),
    office("library-trustee", "Library Trustee",
           "Northfield Brown Public Library Trustees", 7,
           [S(NF_REPORT, "Town of Northfield, 2026 Town Report, "
                         "Elected Officers table: the Brown "
                         "Public Library trustees are elected on "
                         "the town ballot to a seven-seat board: "
                         "Gail Hall (term to 2027), Denise "
                         "MacMartin (term to 2027), Maryann "
                         "Beaupre (Chair, term to 2028), John B. "
                         "Stevens (term to 2028), and Kellianne "
                         "Sutton-Bosley (term to 2028); the two "
                         "seats that stood in 2026 are unpublished "
                         "in outcome, so they are created without "
                         "memberships")],
           [holder("Gail Hall", "gail-hall"),
            holder("Denise MacMartin", "denise-macmartin"),
            holder("Maryann Beaupre", "maryann-beaupre"),
            holder("John B. Stevens", "john-b-stevens"),
            holder("Kellianne Sutton-Bosley",
                   "kellianne-sutton-bosley")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Northfield Justices of the Peace", 14,
           [jp_src("Northfield elects fourteen justices of the "
                   "peace; the listing names Anne Donahue, "
                   "Kenneth Goslant, Jessica Amell, Paul Bean, "
                   "Richard Wobby, Lea Hatch, Denise Macmartin, "
                   "Carolyn Stevens, Britta Eberle, Elizabeth "
                   "Ellsworth, Dexter Rowe, Merry Kay Shernock, "
                   "Lawrence Garland, and Scott Blanchard"),
            S(NF_REPORT, "Town of Northfield, 2026 Town Report, "
                         "Elected Officers table: the town's "
                         "party-tagged justice of the peace table "
                         "names the same fourteen justices")],
           [holder("Anne Donahue", "anne-donahue"),
            holder("Kenneth Goslant", "kenneth-goslant"),
            holder("Jessica Amell", "jessica-amell"),
            holder("Paul Bean", "paul-bean"),
            holder("Richard Wobby", "richard-wobby"),
            holder("Lea Hatch", "lea-hatch"),
            holder("Denise MacMartin", "denise-macmartin",
                   ballot_name="Denise Macmartin"),
            holder("Carolyn Stevens", "carolyn-stevens"),
            holder("Britta Eberle", "britta-eberle"),
            holder("Elizabeth Ellsworth", "elizabeth-ellsworth"),
            holder("Dexter Rowe", "dexter-rowe"),
            holder("Merry Shernock", "merry-shernock",
                   ballot_name="Merry Kay Shernock"),
            holder("Lawrence Garland", "lawrence-garland"),
            holder("Scott Blanchard", "scott-blanchard")]),
], jp=jp_election("northfield-vt", "Town of Northfield", 14,
                  "the certified listing names fourteen winners "
                  "for Northfield's fourteen justice of the peace "
                  "seats"))

# ----------------------------------------------------------------
# Town of Norton (Essex County) -- no official website; SOS spine.
SPECS["norton"] = spec("norton", "Town of Norton", [
    office("selectboard", "Selectboard Member", "Norton Selectboard",
           3,
           [sb_dir("lists the Norton selectboard: James Bronner, "
                   "Betsy Fontaine (Chair), and Stephane "
                   "Thibault")],
           [holder("James Bronner", "james-bronner"),
            holder("Betsy Fontaine", "betsy-fontaine"),
            holder("Stephane Thibault", "stephane-thibault")]),
    office("town-clerk", "Town Clerk", "Norton Town Clerk", 1,
           [guide("names Patricia O'Bin as Norton's town clerk"),
            clerk_xlsx("names Patricia O'Bin as Norton's town "
                       "clerk")],
           [holder("Patricia O'Bin", "patricia-obin")]),
    office("town-treasurer", "Town Treasurer",
           "Norton Town Treasurer", 1,
           [guide("names Patricia O'Bin as Norton's town "
                  "treasurer"),
            treas_xlsx("names Patricia O'Bin as Norton's town "
                       "treasurer")],
           [holder("Patricia O'Bin", "patricia-obin")]),
    office("moderator", "Town Moderator", "Norton Moderator", 1,
           [statute2646_structure("a moderator for a one-year "
                                  "term")]),
    office("lister", "Lister", "Norton Board of Listers", 3,
           [statute2646_structure("a board of listers of three "
                                  "members")]),
    office("auditor", "Town Auditor", "Norton Town Auditors", 3,
           [statute2646_structure("three town auditors")]),
    office("grand-juror", "Grand Juror", "Norton Grand Juror", 1,
           [statute2646_structure("a grand juror")]),
    office("town-agent", "Town Agent", "Norton Town Agent", 1,
           [statute2646_structure("a town agent to prosecute "
                                  "and defend suits")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Norton Justices of the Peace", 5,
           [jp_src("Norton elects five justices of the peace; the "
                   "listing names Christina Duffy, Betsy Fontaine, "
                   "Jocelyn \"Jody\" Gordon, Julie Lavallee, and "
                   "Gina Vigneault")],
           [holder("Christina Duffy", "christina-duffy"),
            holder("Betsy Fontaine", "betsy-fontaine"),
            holder("Jocelyn Gordon", "jocelyn-gordon",
                   ballot_name='Jocelyn "Jody" Gordon'),
            holder("Julie Lavallee", "julie-lavallee"),
            holder("Gina Vigneault", "gina-vigneault")]),
], jp=jp_election("norton-vt", "Town of Norton", 5,
                  "the certified listing names five winners for "
                  "Norton's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Norwich (Windsor County) -- official marked ballot.
NW_B = "Town of Norwich, official marked ballot, March 3, 2026 " \
       "town meeting election (954 voters)"
SPECS["norwich"] = spec("norwich", "Town of Norwich", [
    office("moderator", "Town Moderator", "Norwich Moderator", 1,
           [S(NW_BALLOT, f"{NW_B}: Peter Orner was elected "
                         "moderator with 851 votes")],
           [holder("Peter Orner", "peter-orner")]),
    office("town-clerk", "Town Clerk", "Norwich Town Clerk", 1,
           [S(NW_BALLOT, f"{NW_B}: Lily C. Trajman was elected "
                         "town clerk for a three-year term with "
                         "874 votes"),
            guide("names Lily Trajman as Norwich's town clerk")],
           [holder("Lily Trajman", "lily-trajman")]),
    office("town-treasurer", "Town Treasurer",
           "Norwich Town Treasurer", 1,
           [S(NW_BALLOT, f"{NW_B}: Cheryl A. Lindberg was elected "
                         "to the office the ballot titles 'Town "
                         "and School District Treasurer' for a "
                         "three-year term with 834 votes; it is "
                         "modeled here as the town treasurer"),
            guide("names Cheryl Lindberg as Norwich's town "
                  "treasurer")],
           [holder("Cheryl Lindberg", "cheryl-lindberg")]),
    office("selectboard", "Selectboard Member",
           "Norwich Selectboard", 5,
           [sb_dir("lists the Norwich selectboard: Brendan "
                   "Classon, Robert Gere, James Griggs, Mary "
                   "Layton, and Matthew Swett"),
            S(NW_BALLOT, f"{NW_B}: Brendan Classon was elected "
                         "to a three-year seat with 732 votes; "
                         "the two-year seat had no printed "
                         "candidate and the ballot's own "
                         "handwritten write-in tally reads "
                         "'GERE: 342 SMITH: 290', making Robert "
                         "Gere the certified write-in winner; "
                         "James Griggs, Mary Layton, and Matthew "
                         "Swett did not stand and continue")],
           [holder("Brendan Classon", "brendan-classon"),
            holder("Robert Gere", "robert-gere"),
            holder("James Griggs", "james-griggs"),
            holder("Mary Layton", "mary-layton"),
            holder("Matthew Swett", "matthew-swett")]),
    office("lister", "Lister", "Norwich Board of Listers", 3,
           [S(NW_BALLOT, f"{NW_B}: Cheryl Lindberg was elected "
                         "lister with 803 votes; the two-year "
                         "unexpired seat drew 41 write-in votes "
                         "with no winner declared, and no source "
                         "read names the third seat's holder, so "
                         "two seats are created without "
                         "memberships"),
            S(NW_LISTERS, "Town of Norwich, Listers page: names "
                          "only the chair, Cheryl Lindberg")],
           [holder("Cheryl Lindberg", "cheryl-lindberg")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Norwich Cemetery Commission", 5,
           [S(NW_CEMETERY, "Town of Norwich, Cemetery Commission "
                           "page: the commission has five "
                           "members, one elected each year: Bob "
                           "Pitiger (term to 2027), Ellen Terie "
                           "(term to 2028), Dan Goulet (term to "
                           "2029), Alix Manny (term to 2030), and "
                           "Bob Bristol (term to 2031)"),
            S(NW_BALLOT, f"{NW_B}: Bob Bristol was elected "
                         "cemetery commissioner with 813 "
                         "votes")],
           [holder("Robert E. Pitiger", "robert-e-pitiger"),
            holder("Ellen Terie", "ellen-terie"),
            holder("Dan Goulet", "dan-goulet"),
            holder("Alix Manny", "alix-manny"),
            holder("Bob Bristol", "bob-bristol")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Norwich Trustees of Public Funds", 3,
           [S(NW_BALLOT, f"{NW_B}: Christie James was elected "
                         "trustee of public funds for a two-year "
                         "unexpired term with 764 votes and "
                         "Pamela T Smith for a one-year unexpired "
                         "term with 675 votes; the three-year "
                         "seat drew 25 write-in votes with no "
                         "winner declared, so it is created "
                         "without a membership")],
           [holder("Christie James", "christie-james"),
            holder("Pamela T. Smith", "pamela-t-smith")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Norwich Justices of the Peace", 12,
           [jp_src("Norwich elects twelve justices of the peace; "
                   "the listing names Jedediah Baker, Frances R "
                   "De Gasta, Corlan Johnson, Suzanne Leiter, "
                   "Kristin Maffei, Alix Manny, Robert E. Pitiger, "
                   "Emily Scherer, Dianne Amme, David Krimmel, "
                   "Arline Rotman, and Ernest Ciccotelli")],
           [holder("Jedediah Baker", "jedediah-baker"),
            holder("Frances R. De Gasta", "frances-r-de-gasta",
                   ballot_name="Frances R De Gasta"),
            holder("Corlan Johnson", "corlan-johnson"),
            holder("Suzanne Leiter", "suzanne-leiter"),
            holder("Kristin Maffei", "kristin-maffei"),
            holder("Alix Manny", "alix-manny"),
            holder("Robert E. Pitiger", "robert-e-pitiger"),
            holder("Emily Scherer", "emily-scherer"),
            holder("Dianne Amme", "dianne-amme"),
            holder("David Krimmel", "david-krimmel"),
            holder("Arline Rotman", "arline-rotman"),
            holder("Ernest Ciccotelli", "ernest-ciccotelli")]),
], jp=jp_election("norwich-vt", "Town of Norwich", 12,
                  "the certified listing names twelve winners for "
                  "Norwich's twelve justice of the peace seats"))

# ----------------------------------------------------------------
# Village of Old Bennington (Bennington County) -- general law.
OB_W = "Village of Old Bennington, Warning for the annual " \
       "meeting, May 12, 2026"
OB_M = "Village of Old Bennington, Trustees' Meeting Minutes, " \
       "June 2, 2026 (the first meeting after the annual meeting)"
SPECS["old-bennington"] = spec("old-bennington",
                               "Village of Old Bennington", [
    office("village-trustee", "Village Trustee",
           "Village of Old Bennington Board of Trustees", 5,
           [S(OB_WARNING, f"{OB_W}: two trustees are elected to "
                          "two-year terms, on a five-member "
                          "board"),
            S(OB_MINUTES, f"{OB_M}: the trustees in office are "
                          "Jim Thatch (named Presiding Officer at "
                          "the reorganization), Renny Ponvert, "
                          "Kristin Roessner, Ed Woods, and Susan "
                          "Wright"),
            S(OB_REPORT, "Village of Old Bennington, Annual "
                         "Report 2026: the trustees served "
                         "through fiscal 2026, with Ed Woods as "
                         "Presiding Officer")],
           [holder("Jim Thatch", "jim-thatch"),
            holder("Renny Ponvert", "renny-ponvert"),
            holder("Kristin Roessner", "kristin-roessner"),
            holder("Ed Woods", "ed-woods"),
            holder("Susan Wright", "susan-wright")]),
    office("village-clerk", "Village Clerk",
           "Village of Old Bennington Clerk", 1,
           [S(OB_WARNING, f"{OB_W}: a village clerk is elected "
                          "for a one-year term"),
            S(OB_MINUTES, f"{OB_M}: Mary Walsh signs as Village "
                          "Clerk"),
            S(OB_REPORT, "Village of Old Bennington, Annual "
                         "Report 2026: Mary Walsh served as "
                         "Village Clerk through fiscal 2026; she "
                         "is recorded as re-elected on "
                         "incumbent continuity at the first "
                         "post-election meeting")],
           [holder("Mary Walsh", "mary-walsh")]),
    office("village-treasurer", "Village Treasurer",
           "Village of Old Bennington Treasurer", 1,
           [S(OB_WARNING, f"{OB_W}: a village treasurer is "
                          "elected for a one-year term"),
            S(OB_MINUTES, f"{OB_M}: Ron Rabidou presents the "
                          "treasurer's report"),
            S(OB_REPORT, "Village of Old Bennington, Annual "
                         "Report 2026: Ron Rabidou served as "
                         "Village Treasurer through fiscal 2026; "
                         "he is recorded as re-elected on "
                         "incumbent continuity at the first "
                         "post-election meeting")],
           [holder("Ron Rabidou", "ron-rabidou")]),
    office("village-auditor", "Village Auditor",
           "Village of Old Bennington Auditor", 1,
           [S(OB_WARNING, f"{OB_W}: a village auditor is elected "
                          "for a one-year term"),
            S(OB_MINUTES, f"{OB_M}: Kathy Wagenknecht presents "
                          "the audit report of the fiscal 2026 "
                          "books"),
            S(OB_REPORT, "Village of Old Bennington, Annual "
                         "Report 2026: Kathy Wagenknecht served "
                         "as auditor; she is recorded as "
                         "re-elected on incumbent continuity at "
                         "the first post-election meeting")],
           [holder("Kathy Wagenknecht", "kathy-wagenknecht")]),
    office("moderator", "Village Moderator",
           "Village of Old Bennington Moderator", 1,
           [S(OB_WARNING, f"{OB_W}: a moderator is elected for a "
                          "one-year term; the seat stood at the "
                          "May 12, 2026 annual meeting and no "
                          "official source publishes the "
                          "outcome, so the post is created "
                          "without a membership"),
            S(OB_REPORT, "Village of Old Bennington, Annual "
                         "Report 2026: Pat Winburn served as "
                         "moderator (Presiding Officer of the "
                         "annual meeting) through fiscal 2026")]),
])

# ----------------------------------------------------------------
# Town of Orange (Orange County) -- town officers page governs.
OR_O = "Town of Orange, Town Officers page (orangevt.org), which " \
       "classifies the roster as 'TOWN OFFICERS - ELECTED' and " \
       "'TOWN OFFICERS - APPOINTED' with term years"
SPECS["orange"] = spec("orange", "Town of Orange", [
    office("moderator", "Town Moderator", "Orange Moderator", 1,
           [S(OR_OFFICERS, f"{OR_O}: David Childs, Moderator "
                           "(one-year term)")],
           [holder("David Childs", "david-childs")]),
    office("selectboard", "Selectboard Member", "Orange Selectboard",
           3,
           [sb_dir("lists the Orange selectboard: Steve Simpson "
                   "(Chair), Kristin Paya, and Carmella Tucker"),
            S(OR_OFFICERS, f"{OR_O}: Steve Simpson (Chair, term "
                           "to 2027), Kristin Paya (term to "
                           "2028), and Carmella Tucker (term to "
                           "2029, re-elected in 2026)")],
           [holder("Steve Simpson", "steve-simpson"),
            holder("Kristin Paya", "kristin-paya"),
            holder("Carmella Tucker", "carmella-tucker")]),
    office("lister", "Lister", "Orange Board of Listers", 3,
           [S(OR_OFFICERS, f"{OR_O}: the elected listers are John "
                           "McNeil (term to 2027), Art McNeil "
                           "(term to 2028), and Ed Bedard (term "
                           "to 2029)")],
           [holder("John McNeil", "john-mcneil"),
            holder("Art McNeil", "art-mcneil"),
            holder("Ed Bedard", "ed-bedard")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Orange Cemetery Commission", 3,
           [S(OR_OFFICERS, f"{OR_O}: the elected cemetery "
                           "commissioners are Clark Agnew (term "
                           "to 2027), Rodney Coronado (term to "
                           "2028), and Nick Livingston (term to "
                           "2029)")],
           [holder("Clark Agnew", "clark-agnew"),
            holder("Rodney Coronado", "rodney-coronado"),
            holder("Nick Livingston", "nick-livingston")]),
    office("town-clerk", "Town Clerk", "Orange Town Clerk", 1,
           [S(OR_OFFICERS, f"{OR_O}: Jonathan Danchik is listed "
                           "under TOWN OFFICERS - APPOINTED as "
                           "Town Clerk, so his membership is "
                           "recorded as appointed; the SOS "
                           "Guide's town clerk Nikki Tomlinson "
                           "has departed the office")],
           [holder("Jonathan Danchik", "jonathan-danchik",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Orange Town Treasurer", 1,
           [S(OR_OFFICERS, f"{OR_O}: Diane Hallenbeck is listed "
                           "under TOWN OFFICERS - APPOINTED as "
                           "Town Treasurer, so her membership is "
                           "recorded as appointed; the SOS "
                           "Guide's interim treasurer Nikki "
                           "Tomlinson has departed the office")],
           [holder("Diane Hallenbeck", "diane-hallenbeck",
                   how_seated="appointed")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Orange Collector of Delinquent Taxes", 1,
           [S(OR_OFFICERS, f"{OR_O}: the Delinquent Tax Collector "
                           "is listed under TOWN OFFICERS - "
                           "APPOINTED as 'John McNeil - by "
                           "Selectboard', so his membership is "
                           "recorded as appointed; he also holds "
                           "an elected lister seat")],
           [holder("John McNeil", "john-mcneil",
                   how_seated="appointed")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Orange Justices of the Peace", 5,
           [jp_src("Orange elects five justices of the peace; "
                   "the listing names Tina Otis, Carl \"Lee\" "
                   "Martenson, Francis \"Fred\" Kidder, Kevin "
                   "Wilson, and Sue Perreault; the town's own "
                   "officers page names only four (it omits "
                   "Kidder), and the certified listing governs"),
            S(OR_OFFICERS, f"{OR_O}: the page's justice of the "
                           "peace list (the Board of Civil "
                           "Authority) prints JP terms expiring "
                           "January 31, 2027 (shown as 1/25/2027)")],
           [holder("Tina Otis", "tina-otis"),
            holder("Carl Martenson", "carl-martenson",
                   ballot_name='Carl "Lee" Martenson'),
            holder("Francis Kidder", "francis-kidder",
                   ballot_name='Francis "Fred" Kidder'),
            holder("Kevin Wilson", "kevin-wilson"),
            holder("Sue Perreault", "sue-perreault")]),
], jp=jp_election("orange-vt", "Town of Orange", 5,
                  "the certified listing names five winners for "
                  "Orange's five justice of the peace seats"))

# ----------------------------------------------------------------
# Village of Orleans (Orleans County) -- structure-only, ch. 261.
OL_S = "no official source publishes the village's current " \
       "holders (the village has no website and the VT " \
       "Jurisdiction Factory holds Orleans as unresolved), so " \
       "the post is created without a membership"
SPECS["orleans"] = spec("orleans", "Village of Orleans", [
    office("moderator", "Village Moderator",
           "Village of Orleans Moderator", 1,
           [charter261(f"section 8 provides for a Moderator "
                       f"elected annually; {OL_S}")]),
    office("village-clerk", "Village Clerk",
           "Village of Orleans Clerk", 1,
           [charter261(f"section 8 provides for a Clerk elected "
                       f"annually; {OL_S}")]),
    office("village-trustee", "Village Trustee",
           "Village of Orleans Board of Trustees", 3,
           [charter261(f"section 8 provides for three trustees "
                       f"elected by ballot on staggered "
                       f"three-year terms, one each year; "
                       f"{OL_S}")]),
    office("village-treasurer", "Village Treasurer",
           "Village of Orleans Treasurer", 1,
           [charter261(f"section 8 provides for a Treasurer "
                       f"elected annually; {OL_S}")]),
    office("collector-of-taxes", "Collector of Taxes",
           "Village of Orleans Collector of Taxes", 1,
           [charter261(f"section 8 provides for a Collector of "
                       f"Taxes elected annually; {OL_S}")]),
])

# ----------------------------------------------------------------
# Town of Orwell (Addison County) -- official 2026 results page.
OW_R = "Town of Orwell, Local Election Results 2026 page " \
       "(signed by the Town Clerk)"
SPECS["orwell"] = spec("orwell", "Town of Orwell", [
    office("moderator", "Town Moderator", "Orwell Moderator", 1,
           [S(OW_RESULTS, f"{OW_R}: Glen Cousineau was elected "
                          "moderator")],
           [holder("Glen Cousineau", "glen-cousineau")]),
    office("town-clerk", "Town Clerk", "Orwell Town Clerk", 1,
           [S(OW_RESULTS, f"{OW_R}: Anna Golann was elected town "
                          "clerk; the SOS Guide's Elizabeth "
                          "Walker now serves as assistant clerk"),
            clerk_xlsx("names Elizabeth Walker as Orwell's town "
                       "clerk (superseded by the town's 2026 "
                       "results: Walker is now assistant clerk)")],
           [holder("Anna Golann", "anna-golann")]),
    office("town-treasurer", "Town Treasurer",
           "Orwell Town Treasurer", 1,
           [S(OW_RESULTS, f"{OW_R}: Bryan S. Young was elected "
                          "town treasurer"),
            guide("names Bryan Young as Orwell's town "
                  "treasurer")],
           [holder("Bryan S. Young", "bryan-s-young")]),
    office("selectboard", "Selectboard Member", "Orwell Selectboard",
           5,
           [sb_dir("lists the Orwell selectboard: Andrea "
                   "Treadway (Chair), Mike Christian, Joe "
                   "Pouliot, Hans Tudhope, and Les Wood"),
            S(OW_RESULTS, f"{OW_R}: Mike Christian was "
                          "re-elected to a three-year seat and "
                          "Les Wood to a two-year seat in 2026")],
           [holder("Andrea Treadway", "andrea-treadway"),
            holder("Mike Christian", "mike-christian"),
            holder("Joe Pouliot", "joe-pouliot"),
            holder("Hans Tudhope", "hans-tudhope"),
            holder("Les Wood", "les-wood")]),
    office("lister", "Lister", "Orwell Board of Listers", 3,
           [S(OW_RESULTS, f"{OW_R}: Sharon Ronchetti was elected "
                          "lister for a two-year remainder of a "
                          "three-year term; the three-year seat "
                          "and the one-year remainder both "
                          "returned Vacant"),
            S(OW_LISTERS, "Town of Orwell, Listers page: names "
                          "Sharon Ronchetti and states one "
                          "vacancy; the second unfilled seat is "
                          "created without a membership and no "
                          "further holder is asserted")],
           [holder("Sharon Ronchetti", "sharon-ronchetti")]),
    office("auditor", "Town Auditor", "Orwell Town Auditors", 3,
           [S(OW_RESULTS, f"{OW_R}: both auditor seats that "
                          "stood in 2026 (a three-year seat and "
                          "a one-year remainder) returned "
                          "Vacant, so the post is created "
                          "without memberships"),
            S(OW_AUDIT, "Town of Orwell, Auditors page: names no "
                        "auditor and states 'Two Auditor "
                        "Vacancies Exist'")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Orwell Trustees of Public Funds", 1,
           [S(OW_RESULTS, f"{OW_R}: Bryan S. Young was elected "
                          "trustee of public funds")],
           [holder("Bryan S. Young", "bryan-s-young")]),
    office("first-constable", "First Constable",
           "Orwell First Constable", 1,
           [S(OW_RESULTS, f"{OW_R}: Gary Murdock was elected "
                          "first constable")],
           [holder("Gary Murdock", "gary-murdock")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Orwell Justices of the Peace", 5,
           [jp_src("Orwell elects five justices of the peace; "
                   "the listing names Stephanie Bruyneel Corey, "
                   "Glen Cousineau, Michael R Audet, Richard O "
                   "Buxton, Jr, and Lisa Limoge")],
           [holder("Stephanie Bruyneel Corey",
                   "stephanie-bruyneel-corey"),
            holder("Glen Cousineau", "glen-cousineau"),
            holder("Michael R. Audet", "michael-r-audet",
                   ballot_name="Michael R Audet"),
            holder("Richard O. Buxton, Jr.",
                   "richard-o-buxton-jr",
                   ballot_name="Richard O Buxton, Jr"),
            holder("Lisa Limoge", "lisa-limoge")]),
], jp=jp_election("orwell-vt", "Town of Orwell", 5,
                  "the certified listing names five winners for "
                  "Orwell's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Panton (Addison County) -- certified return + report.
PA_T = "Town of Panton, Official Return of Votes, March 3, 2026 " \
       "town meeting (certified by the Town Clerk/Treasurer; " \
       "138 voters)"
SPECS["panton"] = spec("panton", "Town of Panton", [
    office("moderator", "Town Moderator", "Panton Moderator", 1,
           [S(PA_RETURN, f"{PA_T}: Martha DeGraaf was elected "
                         "moderator with 128 votes")],
           [holder("Martha DeGraaf", "martha-degraaf")]),
    office("selectboard", "Selectboard Member", "Panton Selectboard",
           5,
           [sb_dir("lists the Panton selectboard: Zach Weaver "
                   "(Chair), Teresa Boucher (Vice Chair), Kirsten "
                   "De La Cruz, Robert Degraaf, and Reece Jaring"),
            S(PA_RETURN, f"{PA_T}: Zachary Weaver was "
                         "re-elected to a two-year seat with 122 "
                         "votes and Robert T. DeGraaf to a "
                         "three-year seat with 122 votes; Teresa "
                         "Boucher, Kirsten De La Cruz, and Reece "
                         "Jaring did not stand and continue")],
           [holder("Zachary Weaver", "zachary-weaver"),
            holder("Teresa Boucher", "teresa-boucher"),
            holder("Kirsten De La Cruz", "kirsten-de-la-cruz"),
            holder("Robert T. DeGraaf", "robert-t-degraaf"),
            holder("Reece Jaring", "reece-jaring")]),
    office("town-clerk", "Town Clerk", "Panton Town Clerk", 1,
           [guide("names Kyle Rowe as Panton's town clerk"),
            S(PA_RETURN, f"{PA_T}: the return is certified by "
                         "Kyle Rowe as Town Clerk/Treasurer; "
                         "neither the clerk's nor the treasurer's "
                         "office stood at the 2026 election")],
           [holder("Kyle Rowe", "kyle-rowe")]),
    office("town-treasurer", "Town Treasurer",
           "Panton Town Treasurer", 1,
           [guide("names Kyle Rowe as Panton's town treasurer"),
            S(PA_RETURN, f"{PA_T}: the return is certified by "
                         "Kyle Rowe as Town Clerk/Treasurer")],
           [holder("Kyle Rowe", "kyle-rowe")]),
    office("constable", "Constable", "Panton Constable", 1,
           [S(PA_RETURN, f"{PA_T}: Charles Cushman was elected "
                         "constable for a one-year term with 124 "
                         "votes; the return styles the office "
                         "simply 'Constable'")],
           [holder("Charles Cushman", "charles-cushman")]),
    office("water-commissioner", "Water Commissioner",
           "Panton Water District Commissioners", 3,
           [S(PA_REPORT, "Town of Panton, 2025 Town Report, Town "
                         "Officers table: the Panton Water "
                         "District commissioners are three seats "
                         "on staggered three-year terms: Chris "
                         "Cook (term to 2028), Kathy Kennett "
                         "(term to 2027), and John DeGraaf (term "
                         "to 2026)"),
            S(PA_RETURN, f"{PA_T}: John G. DeGraaf was "
                         "re-elected water commissioner with "
                         "121 votes, on the town ballot voted by "
                         "the whole checklist (general "
                         "franchise)")],
           [holder("Chris Cook", "chris-cook"),
            holder("Kathy Kennett", "kathy-kennett"),
            holder("John G. DeGraaf", "john-g-degraaf")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Panton Justices of the Peace", 5,
           [jp_src("Panton elects five justices of the peace; "
                   "the listing names Gretchen Bailey, Eileen "
                   "Brennan, James Dayton, Paula Moore, and "
                   "Diane Raphael; the town report's variants "
                   "('Jamie Dayton', 'Diana Raphael') do not "
                   "govern")],
           [holder("Gretchen Bailey", "gretchen-bailey"),
            holder("Eileen Brennan", "eileen-brennan"),
            holder("James Dayton", "james-dayton"),
            holder("Paula Moore", "paula-moore"),
            holder("Diane Raphael", "diane-raphael")]),
], jp=jp_election("panton-vt", "Town of Panton", 5,
                  "the certified listing names five winners for "
                  "Panton's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Pawlet (Rutland County) -- certificate of votes.
PW_C = "Town of Pawlet, Certificate of Votes, March 3, 2026 " \
       "Australian-ballot election (attested by Town Clerk " \
       "Debra A. Hawkins, March 4, 2026; 297 votes cast)"
SPECS["pawlet"] = spec("pawlet", "Town of Pawlet", [
    office("moderator", "Town Moderator", "Pawlet Moderator", 1,
           [S(PW_CERT, f"{PW_C}: John C. Thrasher was elected "
                       "moderator with 282 votes")],
           [holder("John C. Thrasher", "john-c-thrasher")]),
    office("selectboard", "Selectboard Member",
           "Pawlet Selectboard", 5,
           [sb_dir("lists the Pawlet selectboard: Michael "
                   "Beecher (Chair), Bob Jones (Vice Chair), Tom "
                   "Collard, Richard Hulett, and Jessica Van "
                   "Oort"),
            S(PW_CERT, f"{PW_C}: Robert Jones was elected to a "
                       "three-year seat with 257 votes, and Tom "
                       "Collard (241) and Jessica Van Oort (203) "
                       "to one-year seats; Michael Beecher and "
                       "Richard Hulett did not stand and "
                       "continue")],
           [holder("Michael Beecher", "michael-beecher"),
            holder("Robert Jones", "robert-jones"),
            holder("Tom Collard", "tom-collard"),
            holder("Richard Hulett", "richard-hulett"),
            holder("Jessica Van Oort", "jessica-van-oort")]),
    office("town-clerk", "Town Clerk", "Pawlet Town Clerk", 1,
           [S(PW_CERT, f"{PW_C}: Debra Hawkins was elected town "
                       "clerk for a three-year term with 286 "
                       "votes"),
            guide("names Debra Hawkins as Pawlet's town clerk")],
           [holder("Debra Hawkins", "debra-hawkins")]),
    office("town-treasurer", "Town Treasurer",
           "Pawlet Town Treasurer", 1,
           [S(PW_CERT, f"{PW_C}: Julie Mach was elected town "
                       "treasurer for a three-year term with "
                       "278 votes"),
            guide("names Julie Mach as Pawlet's town "
                  "treasurer")],
           [holder("Julie Mach", "julie-mach")]),
    office("first-constable", "First Constable",
           "Pawlet First Constable", 1,
           [S(PW_REPORT, "Town of Pawlet, 2025 Town Report: 'our "
                         "two constables: Thomas Covino ... or "
                         "Mark Gutel'; the only constable seat on "
                         "the certified 2026 certificate was the "
                         "Second Constable seat, so Covino holds "
                         "the First Constable seat, which did "
                         "not stand in 2026")],
           [holder("Thomas Covino", "thomas-covino")]),
    office("second-constable", "Second Constable",
           "Pawlet Second Constable", 1,
           [S(PW_CERT, f"{PW_C}: Mark Gutel was elected second "
                       "constable for a two-year term with 254 "
                       "votes")],
           [holder("Mark Gutel", "mark-gutel")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Pawlet Collector of Delinquent Taxes", 1,
           [S(PW_CERT, f"{PW_C}: Kimberly A. Ayers was elected "
                       "collector of delinquent taxes for a "
                       "one-year term with 281 votes")],
           [holder("Kimberly A. Ayers", "kimberly-a-ayers")]),
    office("library-trustee", "Library Trustee",
           "Pawlet Public Library Trustees", 5,
           [S(PW_CERT, f"{PW_C}: Phoebe McChesney (238 votes) "
                       "and Amy B. Miller (220 votes) were "
                       "elected library trustees to three-year "
                       "terms; the board's size is five under "
                       "22 V.S.A. section 143 per the library's "
                       "own meeting record, and the other three "
                       "seats' holders are published in no "
                       "current official source, so they are "
                       "created without memberships")],
           [holder("Phoebe McChesney", "phoebe-mcchesney"),
            holder("Amy B. Miller", "amy-b-miller")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Pawlet Justices of the Peace", 7,
           [jp_src("Pawlet elects seven justices of the peace; "
                   "the listing names Leon Corey, Beth Moser "
                   "Duquette, Raymond Duquette Sr., Sue LaPorte, "
                   "John Malcolm, Bradley Myerson, and Carol "
                   "Schoenwetter")],
           [holder("Leon Corey", "leon-corey"),
            holder("Beth Moser Duquette", "beth-moser-duquette"),
            holder("Raymond Duquette, Sr.",
                   "raymond-duquette-sr",
                   ballot_name="Raymond Duquette Sr."),
            holder("Sue LaPorte", "sue-laporte"),
            holder("John Malcolm", "john-malcolm"),
            holder("Bradley Myerson", "bradley-myerson"),
            holder("Carol Schoenwetter", "carol-schoenwetter")]),
], jp=jp_election("pawlet-vt", "Town of Pawlet", 7,
                  "the certified listing names seven winners for "
                  "Pawlet's seven justice of the peace seats"))

ORDER = ["north-troy", "northfield", "norton", "norwich",
         "old-bennington", "orange", "orleans", "orwell",
         "panton", "pawlet"]

for slug in ORDER:
    (OUT / f"{slug}.json").write_text(
        json.dumps(SPECS[slug], indent=1) + "\n")
print("wrote", len(ORDER), "specs")
