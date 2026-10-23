#!/usr/bin/env python3
"""Batch 13 of the VT #163 municipal fan-out (alphabetical positions
120-129): Landgrove, Leicester, Lemington, Lincoln, Londonderry,
Lowell, Ludlow (town), Ludlow Village, Lunenburg, Lyndon. Emits one
JSON spec per municipality for build_vt_municipality.py.
Research: vt_muni_batch13_research.md.

Identity calls baked into this batch (all flagged on #163):
- Leicester's live official site is leicestervt.org (the address
  the vermont.gov Towns & Cities directory lists); leicestervt.gov
  does not resolve. Its signed March 3, 2026 results, its 2025
  town report officials table, and the SOS spine concur on every
  checkable name. Leicester has NO elected listers (a hired
  assessor function) and its constables are appointed.
- Lincoln's treasurer is Laurie Childers, appointed by the
  Selectboard (the report's appointed table settles the
  Guide-vs-spreadsheet divergence; Patricia Waugh is Town
  Administrator). Lincoln elected no listers in 2026 -- the
  Selectboard appointed a contracted assessor in October 2024.
- Londonderry's 3-year selectboard seat turned over in 2026:
  Leanne Alexander was elected (71-46) to the seat Martha Dale
  held; the June 2026 directory seats Alexander.
- Lowell's official 2026 officers page places its Town Clerk,
  Town Treasurer, and Delinquent Tax Collector under OFFICERS BY
  APPOINTMENT: Christy Pion and Marie Busch are minted appointed.
- Ludlow (town) is built on the town's own comprehensive
  officers documents (FY24 + FY25) plus the SOS spine and the
  factory; its Moderator and First Constable seats stood in
  2025 with no published outcome and are structure-only.
- Ludlow Village's voters APPROVED a plan of merger into the
  Town on March 24, 2026 (95-17); the merger still needs
  legislative approval, the village remains on the SOS list and
  keeps electing officers, and it is modeled as it stands.
  Village trustees/commissioners are certified from the
  village's own official results sheets for 2024, 2025, 2026.
- Lunenburg's Moderator Jacob Fournier is minted under the
  sole-candidate exception (incumbent; the only name on the
  town's published 2026 candidate list; the town meeting notes
  treat him as sitting), disclosed on #163. Its auditors are
  Robinson (2025 elected list) plus Colby and Moffitt (the
  sitting board per the auditors' own June 2026 minutes). Its
  Constable and Delinquent Tax Collector are now filled by
  appointment (March 16, 2026 reorganization notes; June 2026
  auditors' minutes).
- Lyndon's Kermit Fisher selectboard seat is held by Kevin
  Horner per the June 2026 SOS directory. Lyndon's JP
  Robert Gerrish IS Caledonia County's High Bailiff (the
  Hardwick Gazette styles the incumbent "Robert Gerrish
  (D-Lyndon)"): the Lyndon JP membership reuses the county
  person record and the JP candidacy is appended by hand.
- Londonderry's Melissa Brown (JP) is a different person from
  Brookline's treasurer Melissa Brown; the builder's
  collision-suffix filename applies.
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
CHARTER_125 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/125",
    "note": "PLACEHOLDER",
}
CHARTER_126 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/126",
    "note": "PLACEHOLDER",
}
CHARTER_235 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/235",
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


def charter125(phrase):
    return S(CHARTER_125, f"24 App. V.S.A. ch. 125 (Town of Ludlow): "
             f"{phrase}")


def charter126(phrase):
    return S(CHARTER_126, f"24 App. V.S.A. ch. 126 (Town of Lyndon): "
             f"{phrase}")


def charter235(phrase):
    return S(CHARTER_235, f"24 App. V.S.A. ch. 235 (Village of "
             f"Ludlow): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 13); issue #163 "
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
                  f"# municipal fan-out batch 13; issue #163 "
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
ORDER = ["landgrove", "leicester", "lemington", "lincoln",
         "londonderry", "lowell", "ludlow-41275", "ludlow",
         "lunenburg", "lyndon"]

# ------------------------------------------------------------ Landgrove
LAND_SITE = {
    "url": "https://landgrove.vermont.gov",
    "note": "PLACEHOLDER",
}
LAND_REPORT = {
    "url": "https://landgrove.vermont.gov/uploads/1/1/0/0/11002514/town_report2025_web.pdf",
    "note": "PLACEHOLDER",
}


def land_site(what):
    return S(LAND_SITE, f"Town of Landgrove (official website), "
             f"{what}")


def land_report(what):
    return S(LAND_REPORT, f"Town of Landgrove, 2025 Town Report: "
             f"{what}")


def landgrove_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Landgrove Selectboard", 3,
               [sb_dir("lists Landgrove's three selectboard "
                       "members as Benjamin Freeman, Steve Hall "
                       "(Chair), and Will Reed"),
                land_site("Town Gov't page, '2026 Elected Town "
                          "Officers' list: the Selectboard is "
                          "Steve Hall, Benjamin Freeman, and "
                          "Will Reed")],
               [holder("Steve Hall", "steve-hall"),
                holder("Benjamin Freeman", "benjamin-freeman"),
                holder("Will Reed", "will-reed")]),
        office("town-clerk", "Town Clerk", "Landgrove Town Clerk", 1,
               [land_site("Town Gov't page: Chrystal Cleary is "
                          "Town Clerk"),
                guide("lists Chrystal Cleary as Landgrove's town "
                      "clerk"),
                clerk_xlsx("lists Chrystal Cleary as Landgrove's "
                           "town clerk contact")],
               [holder("Chrystal Cleary", "chrystal-cleary")]),
        office("town-treasurer", "Town Treasurer",
               "Landgrove Town Treasurer", 1,
               [land_site("Town Gov't page: Andrea Ogden is Town "
                          "Treasurer"),
                guide("lists Andrea Ogden as Landgrove's "
                      "treasurer"),
                treas_xlsx("lists Andrea Ogden as Landgrove's "
                           "town treasurer contact")],
               [holder("Andrea Ogden", "andrea-ogden")]),
        office("moderator", "Moderator", "Landgrove Moderator", 1,
               [land_report("2026 Warning (Article 1) elects a "
                            "Moderator; the town's post-meeting "
                            "'2026 Elected Town Officers' page "
                            "omits the office, so the 2026 "
                            "outcome is unpublished and the post "
                            "is created without a membership. "
                            "Claudia Harris held the office "
                            "before 2026")]),
        office("lister", "Lister", "Landgrove Board of Listers", 3,
               [land_site("Lister Information page: the Listers "
                          "are Kevin Dommenge, Blair McCaw, and "
                          "Jonathan Bigelow"),
                land_report("'Town Officers Elected' table: "
                            "Listers Kevin Dommenge, Blair "
                            "McCaw, and Jonathan Bigelow "
                            "(Bigelow re-elected in 2026)")],
               [holder("Kevin Dommenge", "kevin-dommenge"),
                holder("Blair McCaw", "blair-mccaw"),
                holder("Jonathan Bigelow", "jonathan-bigelow")]),
        office("auditor", "Auditor", "Landgrove Town Auditors", 3,
               [land_report("'Town Officers Elected' table: "
                            "Auditors Elizabeth Dee (styled "
                            "'Liza Dee' in the table, to 2028), "
                            "Tove Stigum (re-elected to the "
                            "seat expiring 2029), and Brent "
                            "Johnson (elected to the one-year "
                            "seat expiring 2027)")],
               [holder("Elizabeth Dee", "elizabeth-dee"),
                holder("Tove Stigum", "tove-stigum"),
                holder("Brent Johnson", "brent-johnson")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Landgrove Cemetery Commission", 5,
               [land_site("Cemeteries page, '2026 Cemetery "
                          "Commission members': Jonathan "
                          "Bigelow, Mat Degan, Greg Eckhardt, "
                          "Jillian Joyce, and Jeremiah Evarts"),
                land_report("'Town Officers Elected' table: "
                            "five Cemetery Commissioners on "
                            "five-year staggered terms; the "
                            "2026 Warning carried two cemetery "
                            "articles (a five-year seat, won by "
                            "Bigelow, and the vacant seat's "
                            "four-year remainder to 2030, held "
                            "by Evarts)")],
               [holder("Jonathan Bigelow", "jonathan-bigelow"),
                holder("Mat Degan", "mat-degan"),
                holder("Greg Eckhardt", "greg-eckhardt"),
                holder("Jillian Joyce", "jillian-joyce"),
                holder("Jeremiah Evarts", "jeremiah-evarts")]),
        office("collector-of-delinquent-taxes",
               "Delinquent Tax Collector",
               "Landgrove Collector of Delinquent Taxes", 1,
               [land_site("Town Gov't page: Andrea Ogden is "
                          "Collector of Delinquent Taxes")],
               [holder("Andrea Ogden", "andrea-ogden")]),
        office("constable", "Constable", "Landgrove Constable", 1,
               [land_site("Town Gov't page: John Wiley is "
                          "Constable")],
               [holder("John Wiley", "john-wiley")]),
        office("trustee-of-public-funds", "Trustee of Public Funds",
               "Landgrove Trustees of Public Funds", 3,
               [land_report("'Town Officers Elected' table: "
                            "Trustees of Public Funds Jamie "
                            "Wiley (the table spells the name "
                            "'Wylie' once; 'Wiley' governs, to "
                            "2028), Andrea Ogden (re-elected), "
                            "and Sarah Waite (to 2027)")],
               [holder("Jamie Wiley", "jamie-wiley"),
                holder("Andrea Ogden", "andrea-ogden"),
                holder("Sarah Waite", "sarah-waite")]),
        office("grand-juror", "Grand Juror", "Landgrove Grand Juror",
               1,
               [land_report("2026 Warning (Article 1) elects a "
                            "Grand Juror; the town's "
                            "post-meeting '2026 Elected Town "
                            "Officers' page omits the office, "
                            "so the 2026 outcome is unpublished "
                            "and the post is created without a "
                            "membership. Claudia Harris held "
                            "the office before 2026")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Landgrove Justices of the Peace", 5,
               [jp_src("names five justices of the peace for "
                       "Landgrove: John Ogden, Chuck Sweetman, "
                       "Claudia Harris, Virginia LaPrade, and "
                       "Steve Hall"),
                land_report("'Town Officers Elected' table "
                            "prints the JP block as Charles "
                            "Sweetman (recorded so here) and "
                            "names Charlie Howard where the "
                            "certified listing names John "
                            "Ogden; the certified listing "
                            "governs")],
               [holder("John Ogden", "john-ogden"),
                holder("Charles Sweetman", "charles-sweetman",
                       ballot_name="Chuck Sweetman"),
                holder("Claudia Harris", "claudia-harris"),
                holder("Virginia LaPrade", "virginia-laprade"),
                holder("Steve Hall", "steve-hall")]),
    ]
    return spec("landgrove", "Landgrove", offices,
                jp=jp_election(
                    "landgrove-vt", "Landgrove", 5,
                    "the winners were John Ogden, Chuck "
                    "Sweetman, Claudia Harris, Virginia "
                    "LaPrade, and Steve Hall"))


SPECS["landgrove"] = landgrove_spec()

# ------------------------------------------------------------ Leicester
LEI_SITE = {
    "url": "https://www.leicestervt.org",
    "note": "PLACEHOLDER",
}
LEI_RESULTS = {
    "url": "https://www.leicestervt.org",
    "note": "PLACEHOLDER",
}


def lei_site(what):
    return S(LEI_SITE, f"Town of Leicester (official website, "
             f"leicestervt.org), {what}")


def lei_results(what):
    return S(LEI_RESULTS, f"Town of Leicester, official results "
             f"of the March 3, 2026 annual town meeting "
             f"(signed by Town Clerk Julie Delphia; declared "
             f"elected under 17 V.S.A. section 2682(f)): {what}")


def leicester_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Leicester Selectboard", 5,
               [sb_dir("lists Leicester's five selectboard "
                       "members as Thomas Barker, Diane Benware, "
                       "Brad Lawes, Diane Randall, and John "
                       "Rouse"),
                lei_results("Diane Randall was elected to the "
                            "three-year seat and John Rouse to "
                            "the two-year seat"),
                lei_site("Selectboard page: Diane Benware "
                         "(Chair, term to March 2028), Tom "
                         "Barker (2027), Brad Lawes (2027), "
                         "Diane Randall (2029), and John Rouse "
                         "(2028)")],
               [holder("Diane Benware", "diane-benware"),
                holder("Thomas Barker", "thomas-barker"),
                holder("Brad Lawes", "brad-lawes"),
                holder("Diane Randall", "diane-randall"),
                holder("John Rouse", "john-rouse")]),
        office("town-clerk", "Town Clerk", "Leicester Town Clerk", 1,
               [lei_results("Julie Delphia was elected Town "
                            "Clerk to a three-year term"),
                guide("lists Julie Delphia as Leicester's town "
                      "clerk"),
                clerk_xlsx("lists Julie Delphia as Leicester's "
                           "town clerk contact")],
               [holder("Julie Delphia", "julie-delphia")]),
        office("town-treasurer", "Town Treasurer",
               "Leicester Town Treasurer", 1,
               [lei_results("Julie Delphia was elected Town "
                            "Treasurer to a three-year term"),
                guide("lists Julie Delphia as Leicester's "
                      "treasurer"),
                treas_xlsx("lists Julie Delphia as Leicester's "
                           "town treasurer contact")],
               [holder("Julie Delphia", "julie-delphia")]),
        office("moderator", "Moderator", "Leicester Moderator", 1,
               [lei_results("Richard Reed was elected "
                            "Moderator")],
               [holder("Richard Reed", "richard-reed")]),
        office("auditor", "Auditor", "Leicester Town Auditors", 3,
               [lei_results("Lyndsay Davignon was elected "
                            "Auditor to a three-year term"),
                lei_site("Town Officials pages and the 2025 "
                         "Town Report 'Leicester Town "
                         "Officials' table: Auditors Lyndsay "
                         "D'Avignon (recorded with the "
                         "apostrophe, as the town styles her "
                         "name in its 2026 Town Plan), Deb "
                         "Miner (term to March 2027), and "
                         "Donna Pidgeon (to March 2028), on "
                         "staggered three-year terms")],
               [holder("Lyndsay D'Avignon", "lyndsay-davignon"),
                holder("Deb Miner", "deb-miner"),
                holder("Donna Pidgeon", "donna-pidgeon")]),
        office("collector-of-delinquent-taxes",
               "Delinquent Tax Collector",
               "Leicester Collector of Delinquent Taxes", 1,
               [lei_results("Dianne Harvey was elected "
                            "Delinquent Tax Collector"),
                lei_site("Town Officials pages: Dianne Harvey "
                         "is the current Delinquent Tax "
                         "Collector (Elizabeth Ripley held the "
                         "office before 2026)")],
               [holder("Dianne Harvey", "dianne-harvey")]),
        office("first-constable", "First Constable",
               "Leicester First Constable", 1,
               [lei_site("Town Officials pages and the 2025 "
                         "Town Report's appointed-officials "
                         "table: Jeff McDonough is First "
                         "Constable, appointed by the "
                         "Selectboard")],
               [holder("Jeff McDonough", "jeff-mcdonough",
                       how_seated="appointed")]),
        office("second-constable", "Second Constable",
               "Leicester Second Constable", 1,
               [lei_site("Town Officials pages and the 2025 "
                         "Town Report's appointed-officials "
                         "table: Mike Rakowitz is Second "
                         "Constable, appointed by the "
                         "Selectboard")],
               [holder("Mike Rakowitz", "mike-rakowitz",
                       how_seated="appointed")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Leicester Justices of the Peace", 5,
               [jp_src("names five justices of the peace for "
                       "Leicester: Diane Benware, Tom Barker, "
                       "Cheryl Morrison, Greg Bernhardt, and "
                       "Hilary Hatch"),
                lei_site("Justices of the Peace page and the "
                         "2025 Town Report table name the "
                         "same five")],
               [holder("Diane Benware", "diane-benware"),
                holder("Thomas Barker", "thomas-barker",
                       ballot_name="Tom Barker"),
                holder("Cheryl Morrison", "cheryl-morrison"),
                holder("Greg Bernhardt", "greg-bernhardt"),
                holder("Hilary Hatch", "hilary-hatch")]),
    ]
    return spec("leicester", "Leicester", offices,
                jp=jp_election(
                    "leicester-vt", "Leicester", 5,
                    "the winners were Diane Benware, Tom "
                    "Barker, Cheryl Morrison, Greg Bernhardt, "
                    "and Hilary Hatch"))


SPECS["leicester"] = leicester_spec()

# ------------------------------------------------------------ Lemington
def lemington_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Lemington Selectboard", 3,
               [sb_dir("lists Lemington's three selectboard "
                       "members as Scott Cooper, Joseph Daley "
                       "(Chair), and Edward Manemeit. Lemington "
                       "has no official town website; the "
                       "build follows the Bloomfield "
                       "SOS-spine pattern")],
               [holder("Scott Cooper", "scott-cooper"),
                holder("Joseph Daley", "joseph-daley"),
                holder("Edward Manemeit", "edward-manemeit")]),
        office("town-clerk", "Town Clerk", "Lemington Town Clerk", 1,
               [guide("lists Beth Ellingwood as Lemington's "
                      "town clerk"),
                clerk_xlsx("lists Beth Ellingwood as "
                           "Lemington's town clerk contact")],
               [holder("Beth Ellingwood", "beth-ellingwood")]),
        office("town-treasurer", "Town Treasurer",
               "Lemington Town Treasurer", 1,
               [guide("lists Lucie Daley as Lemington's "
                      "treasurer"),
                treas_xlsx("lists Lucie Daley as Lemington's "
                           "town treasurer contact")],
               [holder("Lucie Daley", "lucie-daley")]),
        office("moderator", "Moderator", "Lemington Moderator", 1,
               [statute2646_structure("a moderator is elected "
                                      "annually")]),
        office("lister", "Lister", "Lemington Board of Listers", 3,
               [statute2646_structure("three listers are "
                                      "elected on staggered "
                                      "three-year terms")]),
        office("auditor", "Auditor", "Lemington Town Auditors", 3,
               [statute2646_structure("three auditors are "
                                      "elected on staggered "
                                      "three-year terms")]),
        office("grand-juror", "Grand Juror", "Lemington Grand Juror",
               1,
               [statute2646_structure("a grand juror is "
                                      "elected annually")]),
        office("town-agent", "Town Agent", "Lemington Town Agent", 1,
               [statute2646_structure("a town agent is elected "
                                      "annually")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Lemington Justices of the Peace", 5,
               [jp_src("names five justices of the peace for "
                       "Lemington: Walter Noyes, Myra "
                       "Ellingwood, Mary Jane Walker, Linda "
                       "Young, and Sharon Ellingwood")],
               [holder("Walter Noyes", "walter-noyes"),
                holder("Myra Ellingwood", "myra-ellingwood"),
                holder("Mary Jane Walker", "mary-jane-walker"),
                holder("Linda Young", "linda-young"),
                holder("Sharon Ellingwood", "sharon-ellingwood")]),
    ]
    return spec("lemington", "Lemington", offices,
                jp=jp_election(
                    "lemington-vt", "Lemington", 5,
                    "the winners were Walter Noyes, Myra "
                    "Ellingwood, Mary Jane Walker, Linda "
                    "Young, and Sharon Ellingwood"))


SPECS["lemington"] = lemington_spec()

# ------------------------------------------------------------ Lincoln
LIN_DIR_PAGE = {
    "url": "https://lincolnvermont.org/directory",
    "note": "PLACEHOLDER",
}
LIN_REPORT = {
    "url": "https://lincolnvermont.org/vertical/sites/%7B53E9A1A8-33C4-4381-8550-24F9124297B8%7D/uploads/2025_Lincoln_Town_Report.pdf",
    "note": "PLACEHOLDER",
}
LIN_WARNING = {
    "url": "https://lincolnvermont.org/uploads/dm/7066/2026_Feb_28_Annual_Town_Meeting_Warning",
    "note": "PLACEHOLDER",
}


def lin_dir(what):
    return S(LIN_DIR_PAGE, f"Town of Lincoln (official website), "
             f"Town Directory page: {what}")


def lin_report(what):
    return S(LIN_REPORT, f"Town of Lincoln, 2025 Town Report: "
             f"{what}")


def lin_warning(what):
    return S(LIN_WARNING, f"Town of Lincoln, Warning for the "
             f"February 28, 2026 annual town meeting (officers "
             f"elected by Australian ballot March 3, 2026): "
             f"{what}")


def lincoln_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Lincoln Selectboard", 5,
               [sb_dir("lists Lincoln's five selectboard "
                       "members as Lori Atkins, Joe Martell, "
                       "Tim McGowan (Chair), Lisa Sargent, and "
                       "Ken Stockman"),
                lin_dir("the Selectboard is Tim McGowan "
                        "(Chair), Ken Stockman (Vice Chair), "
                        "Lisa Sargent, Joe Martell, and Lori "
                        "Atkins"),
                lin_report("'Elected Officials' table seats "
                           "the same board except Jessica "
                           "Erwin in the two-year seat "
                           "expiring March 2026; the current "
                           "directory and the SOS directory "
                           "seat Lori Atkins, who was elected "
                           "to that seat in 2026")],
               [holder("Tim McGowan", "tim-mcgowan"),
                holder("Ken Stockman", "ken-stockman"),
                holder("Lisa Sargent", "lisa-sargent"),
                holder("Joe Martell", "joe-martell"),
                holder("Lori Atkins", "lori-atkins")]),
        office("town-clerk", "Town Clerk", "Lincoln Town Clerk", 1,
               [lin_warning("Article 1 elects a Town Clerk "
                            "for a one-year term"),
                lin_report("'Elected Officials' table: Sally "
                           "Ober is Town Clerk"),
                lin_dir("Sally Ober is Town Clerk"),
                guide("lists Sally Ober as Lincoln's town "
                      "clerk")],
               [holder("Sally Ober", "sally-ober")]),
        office("town-treasurer", "Town Treasurer",
               "Lincoln Town Treasurer", 1,
               [lin_report("'Appointed by the Selectboard' "
                           "table: the Town Treasurer is "
                           "Laurie Childers (Assistant "
                           "Treasurer Patricia Waugh, who is "
                           "the Town Administrator). The "
                           "office does not appear on the "
                           "ballot; the January 2026 Guide's "
                           "Patricia Waugh entry is "
                           "superseded"),
                treas_xlsx("lists Laurie Childers as "
                           "Lincoln's town treasurer "
                           "contact")],
               [holder("Laurie Childers", "laurie-childers",
                       how_seated="appointed")]),
        office("moderator", "Moderator", "Lincoln Moderator", 1,
               [lin_warning("Article 1 elects a Town Meeting "
                            "Moderator"),
                lin_dir("Co'Relous Bryant is Town Meeting "
                        "Moderator"),
                lin_report("'Elected Officials' table: "
                           "Co'Relous Bryant is Moderator, "
                           "marked '(appointed to fill "
                           "vacancy)' for the pre-2026 term; "
                           "the 2026 warning warned the "
                           "office for election and the "
                           "current directory seats him")],
               [holder("Co'Relous Bryant", "corelous-bryant")]),
        office("first-constable", "First Constable",
               "Lincoln First Constable", 1,
               [lin_warning("Article 1 elects a First "
                            "Constable"),
                lin_report("'Elected Officials' table: Matt "
                           "Collins is First Constable"),
                lin_dir("Matt Collins is First Constable")],
               [holder("Matt Collins", "matt-collins")]),
        office("second-constable", "Second Constable",
               "Lincoln Second Constable", 1,
               [lin_warning("Article 1 elects a Second "
                            "Constable"),
                lin_report("'Elected Officials' table: Erika "
                           "French is Second Constable"),
                lin_dir("Erika French is Second Constable")],
               [holder("Erika French", "erika-french")]),
        office("collector-of-delinquent-taxes",
               "Delinquent Tax Collector",
               "Lincoln Collector of Delinquent Taxes", 1,
               [lin_warning("Article 1 elects a Collector of "
                            "Delinquent Taxes"),
                lin_report("'Elected Officials' table: Nancy "
                           "Stevens is Collector of Delinquent "
                           "Taxes"),
                lin_dir("Nancy Stevens is Collector of "
                        "Delinquent Taxes")],
               [holder("Nancy Stevens", "nancy-stevens")]),
        office("library-trustee", "Library Trustee",
               "Lincoln Library Trustees", 5,
               [lin_report("'Elected Officials' table lists "
                           "five elected Lincoln Library "
                           "Trustees (alongside four trustees "
                           "appointed by the Library Board "
                           "and one associate trustee, who "
                           "are not modeled): Anna Smith "
                           "(term to March 2028), Jacqueline "
                           "Olson, Chair (2028), and "
                           "Christine Dumond (2027) hold "
                           "over; the two seats expiring "
                           "March 2026 (Lonny Edwards's and "
                           "Jenny Lawson Bates's) were "
                           "warned for election in 2026 but "
                           "no official source publishes "
                           "the outcome, so they are left "
                           "unfilled"),
                lin_warning("Article 1 elects two Lincoln "
                            "Library Trustees for three-year "
                            "terms")],
               [holder("Anna Smith", "anna-smith"),
                holder("Jacqueline Olson", "jacqueline-olson"),
                holder("Christine Dumond", "christine-dumond")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Lincoln Justices of the Peace", 7,
               [jp_src("names six justices of the peace for "
                       "Lincoln and prints the seventh seat "
                       "'vacant': Mark Mulqueen, Nancy "
                       "Stevens, Ari Kirshenbaum, Harrison "
                       "Reynolds, Ilana Brett, and Sally "
                       "Taylor"),
                lin_report("'Elected Officials' table names "
                           "the same six (as 'Harry "
                           "Reynolds' for Harrison Reynolds; "
                           "the certified listing form is "
                           "recorded)")],
               [holder("Ilana Brett", "ilana-brett"),
                holder("Ari Kirshenbaum", "ari-kirshenbaum"),
                holder("Mark Mulqueen", "mark-mulqueen"),
                holder("Harrison Reynolds", "harrison-reynolds"),
                holder("Nancy Stevens", "nancy-stevens"),
                holder("Sally Taylor", "sally-taylor")]),
    ]
    return spec("lincoln", "Lincoln", offices,
                jp=jp_election(
                    "lincoln-vt", "Lincoln", 7,
                    "six winners were named -- Ilana Brett, "
                    "Ari Kirshenbaum, Mark Mulqueen, Harrison "
                    "Reynolds, Nancy Stevens, and Sally "
                    "Taylor -- and the seventh seat is "
                    "listed 'vacant'"))


SPECS["lincoln"] = lincoln_spec()

# ------------------------------------------------------------ Londonderry
LD_REPORT = {
    "url": "https://www.londonderryvt.gov/Documents/Departments/Town Clerk/Annual Town Meeting/2026 Town Report.pdf",
    "note": "PLACEHOLDER",
}
LD_MINUTES = {
    "url": "https://www.londonderryvt.gov/Documents/Departments/Town Clerk/Annual Town Meeting/2026 Town Meeting Minutes.pdf",
    "note": "PLACEHOLDER",
}


def ld_report(what):
    return S(LD_REPORT, f"Town of Londonderry, 2026 Town "
             f"Report: {what}")


def ld_minutes(what):
    return S(LD_MINUTES, f"Town of Londonderry, Minutes of the "
             f"March 3, 2026 annual town meeting (posted in "
             f"draft-final form): {what}")


def londonderry_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Londonderry Selectboard", 5,
               [sb_dir("lists Londonderry's five selectboard "
                       "members as Leanne Alexander, James "
                       "Ameden Jr., Tom Cavanagh, James "
                       "Fleming, and Taylor Prouty"),
                ld_minutes("James Fleming was re-elected to "
                           "the two-year seat and Leanne "
                           "Alexander was elected to the "
                           "three-year seat (paper ballot, "
                           "71-46 over Chad Stoddard). The "
                           "report's pre-2026 schedule seats "
                           "Martha Dale in the three-year "
                           "seat expiring 2026; Alexander "
                           "holds it now"),
                ld_report("'Town Elected Positions Schedule': "
                          "Taylor Prouty (term to 2027), "
                          "Thomas Cavanagh (2027), and James "
                          "Ameden Jr. (2028) hold over")],
               [holder("Leanne Alexander", "leanne-alexander"),
                holder("James Ameden Jr.", "james-ameden-jr"),
                holder("Thomas Cavanagh", "thomas-cavanagh",
                       ballot_name="Tom Cavanagh"),
                holder("James Fleming", "james-fleming"),
                holder("Taylor Prouty", "taylor-prouty")]),
        office("moderator", "Moderator", "Londonderry Moderator", 1,
               [ld_minutes("Doug Friant was elected "
                           "Moderator"),
                ld_report("'Town Elected Positions Schedule': "
                          "Doug Friant is Moderator")],
               [holder("Doug Friant", "doug-friant")]),
        office("town-clerk", "Town Clerk", "Londonderry Town Clerk",
               1,
               [ld_minutes("Allison Marino was re-elected "
                           "Town Clerk for a three-year "
                           "term"),
                guide("lists Allison Marino as Londonderry's "
                      "town clerk"),
                clerk_xlsx("lists Allison Marino as "
                           "Londonderry's town clerk "
                           "contact")],
               [holder("Allison Marino", "allison-marino")]),
        office("town-treasurer", "Town Treasurer",
               "Londonderry Town Treasurer", 1,
               [ld_minutes("Tina Labeau was re-elected Town "
                           "Treasurer for a three-year term"),
                guide("lists Tina Labeau as Londonderry's "
                      "treasurer"),
                treas_xlsx("lists Tina Labeau as "
                           "Londonderry's town treasurer "
                           "contact")],
               [holder("Tina Labeau", "tina-labeau")]),
        office("lister", "Lister", "Londonderry Board of Listers",
               3,
               [ld_minutes("Marge Fish was elected Lister "
                           "for a three-year term"),
                ld_report("'Town Elected Positions Schedule': "
                          "Listers Marge Fish (2026), Alex "
                          "Alberti (2027), and Sandra Clark "
                          "(2028)")],
               [holder("Marge Fish", "marge-fish"),
                holder("Alex Alberti", "alex-alberti"),
                holder("Sandra Clark", "sandra-clark")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Londonderry Cemetery Commission", 5,
               [ld_minutes("Maureen Cronin was elected "
                           "Cemetery Commissioner for a "
                           "five-year term"),
                ld_report("'Town Elected Positions Schedule': "
                          "Cemetery Commissioners Maureen "
                          "Cronin (2026), Laurie Kroos "
                          "Mullen (2027), Amanda Fusco "
                          "(2028), Christopher Blackey "
                          "(2029), and Gary Barton (2030), "
                          "on five-year terms")],
               [holder("Maureen Cronin", "maureen-cronin"),
                holder("Laurie Kroos Mullen",
                       "laurie-kroos-mullen"),
                holder("Amanda Fusco", "amanda-fusco"),
                holder("Christopher Blackey",
                       "christopher-blackey"),
                holder("Gary Barton", "gary-barton")]),
        office("trustee-of-public-funds", "Trustee of Public Funds",
               "Londonderry Trustees of Public Funds", 3,
               [ld_minutes("Katherine Mosenthal was elected "
                           "Trustee of Public Funds for a "
                           "three-year term"),
                ld_report("'Town Elected Positions Schedule': "
                          "Trustees of Public Funds "
                          "Katherine Mosenthal (2026), "
                          "Pauline Davison (2027), and "
                          "Michael Goodbody (2028)")],
               [holder("Katherine Mosenthal",
                       "katherine-mosenthal"),
                holder("Pauline Davison", "pauline-davison"),
                holder("Michael Goodbody", "michael-goodbody")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Londonderry Justices of the Peace", 7,
               [jp_src("names seven justices of the peace "
                       "for Londonderry: Georgianne (George) "
                       "Mora, Melvin Twitchell, Melissa "
                       "Brown, Julie Charlton, Elizabeth "
                       "Labeau, Maureen Cronin, and Helena "
                       "Wu")],
               [holder("Georgianne Mora", "georgianne-mora",
                       ballot_name="Georgianne (George) Mora"),
                holder("Melvin Twitchell", "melvin-twitchell"),
                holder("Melissa Brown", "melissa-brown"),
                holder("Julie Charlton", "julie-charlton"),
                holder("Elizabeth Labeau", "elizabeth-labeau"),
                holder("Maureen Cronin", "maureen-cronin"),
                holder("Helena Wu", "helena-wu")]),
    ]
    return spec("londonderry", "Londonderry", offices,
                jp=jp_election(
                    "londonderry-vt", "Londonderry", 7,
                    "the winners were Georgianne (George) "
                    "Mora, Melvin Twitchell, Melissa Brown, "
                    "Julie Charlton, Elizabeth Labeau, "
                    "Maureen Cronin, and Helena Wu"))


SPECS["londonderry"] = londonderry_spec()

# ------------------------------------------------------------ Lowell
LOW_OFFICERS = {
    "url": "https://townoflowell.org/town-officers-.html",
    "note": "PLACEHOLDER",
}


def low_officers(what):
    return S(LOW_OFFICERS, f"Town of Lowell (official website), "
             f"'2026 Town Officers' page: {what}")


def lowell_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Lowell Selectboard", 3,
               [sb_dir("lists Lowell's three selectboard "
                       "members as Jennifer Blay (Chair), "
                       "Darren Pion, and Wayne Richardson"),
                low_officers("under ELECTED OFFICIALS: "
                             "Selectboard Wayne Richardson "
                             "(term to 2027), Jennifer Blay "
                             "(2028), and Darren Pion "
                             "(2029)")],
               [holder("Jennifer Blay", "jennifer-blay"),
                holder("Darren Pion", "darren-pion"),
                holder("Wayne Richardson", "wayne-richardson")]),
        office("moderator", "Moderator", "Lowell Moderator", 1,
               [low_officers("under ELECTED OFFICIALS: "
                             "Moderator Alden Warner (term "
                             "to 2027)")],
               [holder("Alden Warner", "alden-warner")]),
        office("town-clerk", "Town Clerk", "Lowell Town Clerk", 1,
               [low_officers("under OFFICERS BY APPOINTMENT: "
                             "Town Clerk Christy M. Pion "
                             "(appointed)"),
                guide("lists Christy Pion as Lowell's town "
                      "clerk"),
                clerk_xlsx("lists Christy Pion as Lowell's "
                           "town clerk contact")],
               [holder("Christy Pion", "christy-pion",
                       how_seated="appointed")]),
        office("town-treasurer", "Town Treasurer",
               "Lowell Town Treasurer", 1,
               [low_officers("under OFFICERS BY APPOINTMENT: "
                             "Town Treasurer Marie Busch "
                             "(appointed)"),
                guide("lists Marie Busch as Lowell's "
                      "treasurer"),
                treas_xlsx("lists Marie Busch as Lowell's "
                           "town treasurer contact")],
               [holder("Marie Busch", "marie-busch",
                       how_seated="appointed")]),
        office("first-constable", "First Constable",
               "Lowell First Constable", 1,
               [low_officers("under ELECTED OFFICIALS: First "
                             "Constable Ashley Callahan "
                             "(term to 2027)")],
               [holder("Ashley Callahan", "ashley-callahan")]),
        office("auditor", "Auditor", "Lowell Town Auditors", 3,
               [low_officers("under ELECTED OFFICIALS: "
                             "Auditors Arlon Warner (2027), "
                             "Gordon Spencer (2028), and "
                             "Dorothy Spoerl (2029). Arlon "
                             "Warner is a different person "
                             "from Moderator Alden Warner; "
                             "the town's page prints the two "
                             "names distinctly")],
               [holder("Arlon Warner", "arlon-warner"),
                holder("Gordon Spencer", "gordon-spencer"),
                holder("Dorothy Spoerl", "dorothy-spoerl")]),
        office("lister", "Lister", "Lowell Board of Listers", 3,
               [low_officers("under ELECTED OFFICIALS: "
                             "Listers Christine Hager "
                             "(2027), Mark Higley (2028), "
                             "and Cheryl Clarke (2029)")],
               [holder("Christine Hager", "christine-hager"),
                holder("Mark Higley", "mark-higley"),
                holder("Cheryl Clarke", "cheryl-clarke")]),
        office("library-trustee", "Library Trustee",
               "Lowell Library Trustees", 5,
               [low_officers("under ELECTED OFFICIALS: "
                             "Library Trustees Katherine "
                             "Pion (term to 2027), Mckenna "
                             "Blay (2030; the page prints "
                             "'Mckenna', recorded as "
                             "printed), Debbie Manning "
                             "(2031), Jennifer Higgins "
                             "(2031), and Brenda Wesolow "
                             "(2031), five trustees on "
                             "staggered five-year terms")],
               [holder("Katherine Pion", "katherine-pion"),
                holder("Mckenna Blay", "mckenna-blay"),
                holder("Debbie Manning", "debbie-manning"),
                holder("Jennifer Higgins", "jennifer-higgins"),
                holder("Brenda Wesolow", "brenda-wesolow")]),
        office("collector-of-delinquent-taxes",
               "Delinquent Tax Collector",
               "Lowell Collector of Delinquent Taxes", 1,
               [low_officers("under OFFICERS BY APPOINTMENT: "
                             "Delinquent Tax Collector "
                             "Marie Busch (appointed)")],
               [holder("Marie Busch", "marie-busch",
                       how_seated="appointed")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Lowell Justices of the Peace", 4,
               [jp_src("names four justices of the peace for "
                       "Lowell: Jeffrey Parsons, Gordon "
                       "Spencer, Richard Pion, and William "
                       "Herrera"),
                low_officers("under ELECTED OFFICIALS: "
                             "Justices of the Peace Jeff "
                             "Parsons, William Herrera, "
                             "Richard Pion, and Gordon "
                             "Spencer")],
               [holder("Jeffrey Parsons", "jeffrey-parsons",
                       ballot_name="Jeff Parsons"),
                holder("Gordon Spencer", "gordon-spencer"),
                holder("Richard Pion", "richard-pion"),
                holder("William Herrera", "william-herrera")]),
    ]
    return spec("lowell", "Lowell", offices,
                jp=jp_election(
                    "lowell-vt", "Lowell", 4,
                    "the winners were Jeffrey Parsons, "
                    "Gordon Spencer, Richard Pion, and "
                    "William Herrera"))


SPECS["lowell"] = lowell_spec()

# ------------------------------------------------------------ Ludlow (town)
LUD_OFFICERS = {
    "url": "https://www.ludlow.vt.us/vertical/sites/%7B78E8DA21-0D46-4486-AF59-9D2B5A1048F3%7D/uploads/FY25_Town_Appointed__Elected_Officers.pdf",
    "note": "PLACEHOLDER",
}


def lud_officers(what):
    return S(LUD_OFFICERS, f"Town of Ludlow, 'Appointed and "
             f"Elected Officers' document (the town's official "
             f"FY25 officers sheet, the post-March 2024 state; "
             f"the FY24 sheet concurs on the office set): "
             f"{what}")


def ludlow_town_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Ludlow Selectboard", 5,
               [lud_officers("the Selectboard is Brett "
                             "Sanderson (Chair), George "
                             "Tucker Jr., Justin Hyjek, "
                             "Scott Baitz, and Noah Schmidt"),
                charter125("section 2: the Selectboard's "
                           "powers are exercised by ballot "
                           "as provided; the town's charter "
                           "carries no officer list, so town "
                           "offices follow general law. The "
                           "SOS selectboard directory "
                           "publishes no Ludlow roster "
                           "('Contact the Town Clerk'); the "
                           "town's own officers documents "
                           "for two cycles and the VT "
                           "Jurisdiction Factory concord on "
                           "the five")],
               [holder("Brett Sanderson", "brett-sanderson"),
                holder("George Tucker Jr.", "george-tucker-jr"),
                holder("Justin Hyjek", "justin-hyjek"),
                holder("Scott Baitz", "scott-baitz"),
                holder("Noah Schmidt", "noah-schmidt")]),
        office("town-clerk", "Town Clerk", "Ludlow Town Clerk", 1,
               [lud_officers("Ulla P. Cook is Town Clerk "
                             "(recorded Ulla Cook)"),
                guide("lists Ulla Cook as Ludlow's town "
                      "clerk"),
                clerk_xlsx("lists Ulla Cook as Ludlow's town "
                           "clerk contact")],
               [holder("Ulla Cook", "ulla-cook")]),
        office("town-treasurer", "Town Treasurer",
               "Ludlow Town Treasurer", 1,
               [lud_officers("Ulla P. Cook is Town Treasurer, "
                             "term to 2027"),
                guide("lists Ulla Cook as Ludlow's "
                      "treasurer"),
                treas_xlsx("lists no Ludlow treasurer; the "
                           "town's officers document and "
                           "the Guide concur on Ulla Cook")],
               [holder("Ulla Cook", "ulla-cook")]),
        office("moderator", "Moderator", "Ludlow Moderator", 1,
               [lud_officers("the Moderator line seats "
                             "Newton Rose with a term "
                             "expiring in 2025; no later town "
                             "document publishes the office's "
                             "outcome, so the post is created "
                             "without a membership. Rose is "
                             "certified elected Moderator of "
                             "Ludlow Village in 2026; his "
                             "person record is created by "
                             "the village build")]),
        office("first-constable", "First Constable",
               "Ludlow First Constable", 1,
               [lud_officers("the First Constable line seats "
                             "Jeffrey Billings (elected) "
                             "with a term expiring in 2025; "
                             "no later town document "
                             "publishes the outcome, so the "
                             "post is created without a "
                             "membership")]),
        office("collector-of-delinquent-taxes",
               "Delinquent Tax Collector",
               "Ludlow Collector of Delinquent Taxes", 1,
               [lud_officers("the Delinquent Tax Collector "
                             "is the Municipal Manager, "
                             "Brendan McNamara, holding the "
                             "office by appointment (both "
                             "officers documents)")],
               [holder("Brendan McNamara", "brendan-mcnamara",
                       how_seated="appointed")]),
        office("lister", "Lister", "Ludlow Board of Listers", 3,
               [lud_officers("the Listers line reads: 'None "
                             "(elected) March 2024 / Douglas "
                             "Sheehan (appointed) 2025 / "
                             "Jeanne Stasz (elected) 2027'. "
                             "Only Jeanne Stasz is minted; "
                             "Sheehan's appointed term has "
                             "expired and the third seat is "
                             "unfilled by election")],
               [holder("Jeanne Stasz", "jeanne-stasz")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Ludlow Cemetery Commission", 5,
               [lud_officers("the Cemetery Trustees line "
                             "carries five seats on "
                             "five-year terms: Bruce Schmidt, "
                             "Chair (to 2029), and Shannon "
                             "Stark (2028) hold current "
                             "elected terms; Robert Brandt's "
                             "term expired in 2025, Ludwig "
                             "Gabranski's in 2026, and Scott "
                             "Baitz's appointed term in "
                             "2025, and no official source "
                             "publishes those outcomes, so "
                             "those seats are unfilled")],
               [holder("Bruce Schmidt", "bruce-schmidt"),
                holder("Shannon Stark", "shannon-stark")]),
        office("trustee-of-public-funds", "Trustee of Public Funds",
               "Ludlow Trustees of Public Funds", 3,
               [lud_officers("the Trustees of Public Funds "
                             "line reads 'None (elected)'; "
                             "Ulla Cook's elected term "
                             "expired in 2025 and Douglas "
                             "Sheehan's appointed term "
                             "expired in 2025, so the post is "
                             "created without a "
                             "membership")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Ludlow Justices of the Peace", 10,
               [jp_src("names ten justices of the peace for "
                       "Ludlow: Laura Creaser, Theresa "
                       "Gurdak-Carter, Joe Josselyn, John "
                       "Merrow, Alice Nitka, Judy Pullinen, "
                       "Virginia Snyder, Jean Strong, John "
                       "Murphy, and Joyce Washburn. The "
                       "town officers document's JP block "
                       "is the prior (November 2022) slate "
                       "and does not govern")],
               [holder("Laura Creaser", "laura-creaser"),
                holder("Theresa Gurdak-Carter",
                       "theresa-gurdak-carter"),
                holder("Joe Josselyn", "joe-josselyn"),
                holder("John Merrow", "john-merrow"),
                holder("Alice Nitka", "alice-nitka"),
                holder("Judy Pullinen", "judy-pullinen"),
                holder("Virginia Snyder", "virginia-snyder"),
                holder("Jean Strong", "jean-strong"),
                holder("John Murphy", "john-murphy"),
                holder("Joyce Washburn", "joyce-washburn")]),
    ]
    return spec("ludlow-41275", "Ludlow", offices,
                jp=jp_election(
                    "ludlow-41275-vt", "Ludlow", 10,
                    "the winners were Laura Creaser, Theresa "
                    "Gurdak-Carter, Joe Josselyn, John "
                    "Merrow, Alice Nitka, Judy Pullinen, "
                    "Virginia Snyder, Jean Strong, John "
                    "Murphy, and Joyce Washburn"))


SPECS["ludlow-41275"] = ludlow_town_spec()

# ------------------------------------------------------------ Ludlow Village
LUDV_RES26 = {
    "url": "https://www.ludlow.vt.us/vertical/sites/%7B78E8DA21-0D46-4486-AF59-9D2B5A1048F3%7D/uploads/SKM_C550i26032511200.pdf",
    "note": "PLACEHOLDER",
}
LUDV_RES25 = {
    "url": "https://www.ludlow.vt.us/vertical/sites/%7B78E8DA21-0D46-4486-AF59-9D2B5A1048F3%7D/uploads/Village_Vote_Results-_March_25_2025.pdf",
    "note": "PLACEHOLDER",
}
LUDV_RES24 = {
    "url": "https://www.ludlow.vt.us/vertical/sites/%7B78E8DA21-0D46-4486-AF59-9D2B5A1048F3%7D/uploads/Village_Vote_Results_-_March_26_20241.pdf",
    "note": "PLACEHOLDER",
}


def ludv26(what):
    return S(LUDV_RES26, f"Village of Ludlow, official results "
             f"of the March 24, 2026 village meeting (scanned "
             f"return on the Town of Ludlow website): {what}")


def ludv25(what):
    return S(LUDV_RES25, f"Village of Ludlow, official results "
             f"of the March 25, 2025 village meeting: {what}")


def ludv24(what):
    return S(LUDV_RES24, f"Village of Ludlow, official results "
             f"of the March 26, 2024 village meeting: {what}")


def ludlow_village_spec():
    offices = [
        office("moderator", "Village Moderator",
               "Ludlow Village Moderator", 1,
               [ludv26("Newton J. Rose was elected Moderator "
                       "(108 votes); the village ballot has "
                       "carried a Moderator in 2024, 2025, "
                       "and 2026 although 24 App. V.S.A. "
                       "ch. 235 section 21 does not list the "
                       "office, and the post is created on "
                       "the ballot's authority"),
                ludv25("Newton J. Rose was elected Moderator "
                       "(51 votes)"),
                ludv24("Newton J. Rose was elected Moderator "
                       "(49 votes)")],
               [holder("Newton Rose", "newton-rose")]),
        office("village-trustee", "Village Trustee",
               "Ludlow Village Board of Trustees", 3,
               [charter235("section 21: three Trustees are "
                           "chosen by ballot for three-year "
                           "terms"),
                ludv26("Justin Hyjek was elected Trustee "
                       "for a three-year term (102 votes). "
                       "Article 1 of the same ballot, the "
                       "plan of merger of the Village into "
                       "the Town, passed 95-17; the merger "
                       "still requires legislative "
                       "approval, the village remains on "
                       "the Secretary of State's "
                       "incorporated-villages list, and it "
                       "is modeled as it stands"),
                ludv25("Robert Brandt was elected Trustee "
                       "for a three-year term (54 votes)"),
                ludv24("Julie G. Nicoll was elected Trustee "
                       "for a three-year term (48 votes)")],
               [holder("Julie Nicoll", "julie-nicoll"),
                holder("Robert Brandt", "robert-brandt"),
                holder("Justin Hyjek", "justin-hyjek",
                       person_scope="ludlow-41275")]),
        office("electric-light-commissioner",
               "Electric Light Commissioner",
               "Ludlow Village Board of Electric Light "
               "Commissioners", 3,
               [charter235("section 21: three Electric Light "
                           "Commissioners are chosen by "
                           "ballot for three-year terms"),
                ludv26("Logan Nicoll was elected Electric "
                       "Light Commissioner for a three-year "
                       "term (96 votes); in 2025 he filled "
                       "the final year of the same seat's "
                       "balance of term"),
                ludv25("Jean S. Strong was elected "
                       "Electric Light Commissioner for a "
                       "three-year term (57 votes)"),
                ludv24("Shannon Barton Stark was elected "
                       "Electric Light Commissioner for a "
                       "three-year term (43 votes); the "
                       "same person holds a Ludlow town "
                       "cemetery seat as Shannon Stark")],
               [holder("Shannon Stark", "shannon-stark",
                       person_scope="ludlow-41275"),
                holder("Jean Strong", "jean-strong",
                       person_scope="ludlow-41275"),
                holder("Logan Nicoll", "logan-nicoll")]),
        office("water-commissioner", "Water Commissioner",
               "Ludlow Village Board of Water Commissioners", 3,
               [charter235("section 21: three Water "
                           "Commissioners are chosen by "
                           "ballot for three-year terms"),
                ludv26("Logan Nicoll was elected Water "
                       "Commissioner for a three-year term "
                       "(94 votes)"),
                ludv25("William 'BJ' Donohue was elected "
                       "Water Commissioner for a "
                       "three-year term (55 votes)"),
                ludv24("Ronald G. Bixby was elected Water "
                       "Commissioner for a three-year "
                       "term (48 votes)")],
               [holder("Ronald Bixby", "ronald-bixby"),
                holder("William Donohue", "william-donohue",
                       ballot_name='William "BJ" Donohue'),
                holder("Logan Nicoll", "logan-nicoll")]),
        office("village-clerk", "Village Clerk",
               "Ludlow Village Clerk", 1,
               [charter235("section 21: a Clerk is chosen by "
                           "ballot for a one-year term; the "
                           "office appears on no recent "
                           "village ballot and no official "
                           "source publishes the holder, so "
                           "the post is created without a "
                           "membership")]),
        office("village-treasurer", "Village Treasurer",
               "Ludlow Village Treasurer", 1,
               [charter235("section 21: a Treasurer is "
                           "chosen by ballot for a one-year "
                           "term; the office appears on no "
                           "recent village ballot and no "
                           "official source publishes the "
                           "holder, so the post is created "
                           "without a membership")]),
        office("village-collector", "Village Collector",
               "Ludlow Village Collector", 1,
               [charter235("section 21: a Collector is "
                           "chosen by ballot for a one-year "
                           "term; the office appears on no "
                           "recent village ballot and no "
                           "official source publishes the "
                           "holder, so the post is created "
                           "without a membership")]),
        office("village-auditor", "Village Auditor",
               "Ludlow Village Auditor", 1,
               [charter235("section 21: an Auditor is chosen "
                           "by ballot for a one-year term; "
                           "the office appears on no recent "
                           "village ballot and no official "
                           "source publishes the holder, so "
                           "the post is created without a "
                           "membership")]),
    ]
    return spec("ludlow", "Ludlow Village", offices)


SPECS["ludlow"] = ludlow_village_spec()

# ------------------------------------------------------------ Lunenburg
LUN_REPORT = {
    "url": "https://irp.cdn-website.com/cefd8893/files/uploaded/2025+Annual+Auditors+Report+-+Lunenburg-+VT+-+FINAL.pdf",
    "note": "PLACEHOLDER",
}
LUN_TM = {
    "url": "https://irp.cdn-website.com/cefd8893/files/uploaded/Town+Meeting+2026+Notes.pdf",
    "note": "PLACEHOLDER",
}
LUN_REORG = {
    "url": "https://irp.cdn-website.com/cefd8893/files/uploaded/March+16+Select+Board+Reorganization+Meeting+Notes.pdf",
    "note": "PLACEHOLDER",
}
LUN_AUD = {
    "url": "https://irp.cdn-website.com/cefd8893/files/uploaded/Auditors-meeting-minutes-29jun2026.pdf",
    "note": "PLACEHOLDER",
}


def lun_report(what):
    return S(LUN_REPORT, f"Town of Lunenburg, 2025 Town Report: "
             f"{what}")


def lun_tm(what):
    return S(LUN_TM, f"Town of Lunenburg, notes of the "
             f"March 3, 2026 annual town meeting: {what}")


def lun_reorg(what):
    return S(LUN_REORG, f"Town of Lunenburg, Selectboard "
             f"reorganization meeting notes, March 16, 2026: "
             f"{what}")


def lun_aud(what):
    return S(LUN_AUD, f"Town of Lunenburg, Auditors meeting "
             f"minutes, June 29, 2026: {what}")


def lunenburg_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Lunenburg Selectboard", 3,
               [sb_dir("lists Lunenburg's three selectboard "
                       "members as Nancy Benoit, Nate Brown, "
                       "and Harry Williams (Chair)"),
                lun_reorg("the board is Harry Williams "
                          "(Chair), Nancy Benoit, and Nate "
                          "Brown")],
               [holder("Harry Williams", "harry-williams"),
                holder("Nancy Benoit", "nancy-benoit"),
                holder("Nate Brown", "nate-brown")]),
        office("town-clerk", "Town Clerk", "Lunenburg Town Clerk",
               1,
               [lun_report("'2025 Elected Town Officers' "
                           "list: Gary Briggs is Town Clerk "
                           "(one-year remainder of term); the "
                           "town's published 2026 candidate "
                           "list seats him for a full "
                           "three-year term"),
                guide("lists Gary Briggs as Lunenburg's "
                      "town clerk"),
                clerk_xlsx("lists Gary Briggs as "
                           "Lunenburg's town clerk "
                           "contact")],
               [holder("Gary Briggs", "gary-briggs")]),
        office("town-treasurer", "Town Treasurer",
               "Lunenburg Town Treasurer", 1,
               [lun_report("'2025 Elected Town Officers' "
                           "list: Gary Briggs is Town "
                           "Treasurer; the town's published "
                           "2026 candidate list seats him "
                           "for a full three-year term"),
                guide("lists Gary Briggs as Lunenburg's "
                      "treasurer"),
                treas_xlsx("lists Gary Briggs as "
                           "Lunenburg's town treasurer "
                           "contact")],
               [holder("Gary Briggs", "gary-briggs")]),
        office("moderator", "Moderator", "Lunenburg Moderator", 1,
               [lun_report("'2025 Elected Town Officers' "
                           "list: Jacob Fournier is "
                           "Moderator; the town's published "
                           "'2026 Town Officer Candidates' "
                           "list names him the only candidate "
                           "for Moderator"),
                lun_tm("the meeting notes record the Town "
                       "Clerk presiding only because "
                       "'Moderator Jacob was ill', treating "
                       "Fournier as the sitting Moderator. "
                       "Minted under the sole-candidate "
                       "exception (incumbent plus the only "
                       "name on the town's published "
                       "candidate list), disclosed on "
                       "issue #163")],
               [holder("Jacob Fournier", "jacob-fournier")]),
        office("auditor", "Auditor", "Lunenburg Town Auditors",
               3,
               [lun_report("'2025 Elected Town Officers' "
                           "list: Luke Robinson is Auditor "
                           "(three-year term elected "
                           "2025)"),
                lun_aud("the auditors' own minutes seat "
                        "Luke Robinson and Karla Colby, "
                        "with Jim Moffitt absent: the "
                        "sitting three-member board. Colby "
                        "was the published 2026 candidate "
                        "for the three-year seat; Moffitt's "
                        "seat is the second auditor seat "
                        "the 2025 warning carried, "
                        "unnamed in the report's elected "
                        "list")],
               [holder("Luke Robinson", "luke-robinson"),
                holder("Karla Colby", "karla-colby"),
                holder("Jim Moffitt", "jim-moffitt")]),
        office("lister", "Lister", "Lunenburg Board of Listers",
               3,
               [lun_report("'2025 Elected Town Officers' "
                           "list: Karen Danforth is Lister "
                           "(three-year term elected 2025). "
                           "The 2026 candidates for the "
                           "remaining seats (Linda Magoni, "
                           "three-year; Sonya Boulay, "
                           "one-year) are not minted: "
                           "candidates are not winners and "
                           "no outcome is published")],
               [holder("Karen Danforth", "karen-danforth")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Lunenburg Cemetery Commission", 3,
               [lun_report("'2025 Elected Town Officers' "
                           "list: Penny Nason is Cemetery "
                           "Commissioner (elected 2025). "
                           "One three-year seat is elected "
                           "per year, deriving a three-seat "
                           "commission; the 2026 candidate "
                           "(Deb Thomas) is not minted, as "
                           "no outcome is published")],
               [holder("Penny Nason", "penny-nason")]),
        office("first-constable", "First Constable",
               "Lunenburg First Constable", 1,
               [lun_report("'2025 Elected Town Officers' "
                           "list: Dan Comeau was elected "
                           "Constable in 2025"),
                lun_reorg("the Selectboard's annual "
                          "appointments list 'Constable: "
                          "Dan Comeau', and the board "
                          "recorded asking VLCT about "
                          "eliminating the position from "
                          "town appointments; the current "
                          "holder is recorded as "
                          "appointed")],
               [holder("Dan Comeau", "dan-comeau",
                       how_seated="appointed")]),
        office("collector-of-delinquent-taxes",
               "Delinquent Tax Collector",
               "Lunenburg Collector of Delinquent Taxes", 1,
               [lun_aud("the auditors' minutes name Cindi "
                        "Wilmoti the sitting Delinquent "
                        "Tax Collector (the town report "
                        "spells the name 'Cindy Wilmott' "
                        "once in a committee list; the "
                        "minutes spelling is recorded). "
                        "The office is filled by "
                        "appointment")],
               [holder("Cindi Wilmoti", "cindi-wilmoti",
                       how_seated="appointed")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Lunenburg Justices of the Peace", 3,
               [jp_src("names three justices of the peace "
                       "for Lunenburg: James Peyton, Diane "
                       "Peyton, and Wyatt Peyton")],
               [holder("James Peyton", "james-peyton"),
                holder("Diane Peyton", "diane-peyton"),
                holder("Wyatt Peyton", "wyatt-peyton")]),
    ]
    return spec("lunenburg", "Lunenburg", offices,
                jp=jp_election(
                    "lunenburg-vt", "Lunenburg", 3,
                    "the winners were James Peyton, Diane "
                    "Peyton, and Wyatt Peyton"))


SPECS["lunenburg"] = lunenburg_spec()

# ------------------------------------------------------------ Lyndon
LYN_REPORT = {
    "url": "https://www.lyndonvt.org/wp-content/uploads/2026/02/2025-Town-Report.pdf",
    "note": "PLACEHOLDER",
}
LYN_CLERK = {
    "url": "https://www.lyndonvt.org/?page_id=14",
    "note": "PLACEHOLDER",
}


def lyn_report(what):
    return S(LYN_REPORT, f"Town of Lyndon, 2025 Town Report: "
             f"{what}")


def lyn_clerk(what):
    return S(LYN_CLERK, f"Town of Lyndon (official website), "
             f"Town Clerk page: {what}")


def lyndon_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Lyndon Selectboard", 5,
               [sb_dir("lists Lyndon's five selectboard "
                       "members as Daniel Daley, Kevin "
                       "Horner, Christopher Hunter, Susan "
                       "Mills, and Christian Thompson"),
                charter126("sections 22 and 26: five "
                           "Selectboard members are elected "
                           "to three-year terms"),
                lyn_report("'Town Officers 2025' table "
                           "seats Kermit Fisher in the seat "
                           "expiring 2026 where the June "
                           "2026 SOS directory seats Kevin "
                           "Horner; the directory set (Dan "
                           "Daley III, Kevin Horner, "
                           "Christopher Hunter, Susan "
                           "Mills, Christian Thompson) is "
                           "the current board")],
               [holder("Dan Daley III", "dan-daley-iii"),
                holder("Kevin Horner", "kevin-horner"),
                holder("Christopher Hunter",
                       "christopher-hunter"),
                holder("Susan Mills", "susan-mills"),
                holder("Christian Thompson",
                       "christian-thompson")]),
        office("town-clerk", "Town Clerk", "Lyndon Town Clerk", 1,
               [charter126("section 22: a Town Clerk is "
                           "elected to a three-year term"),
                lyn_report("'Town Officers 2025' table: "
                           "Dawn R. Dwyer is Clerk and "
                           "Treasurer (term to 2027)"),
                lyn_clerk("Dawn Dwyer is Town Clerk"),
                guide("lists Dawn Dwyer as Lyndon's town "
                      "clerk")],
               [holder("Dawn Dwyer", "dawn-dwyer")]),
        office("town-treasurer", "Town Treasurer",
               "Lyndon Town Treasurer", 1,
               [charter126("section 22: a Town Treasurer is "
                           "elected to a three-year term "
                           "as a separate office from the "
                           "Clerk; the town report lists a "
                           "combined 'Clerk and Treasurer' "
                           "line, and the two posts carry "
                           "one holder"),
                lyn_report("'Town Officers 2025' table: "
                           "Dawn R. Dwyer is Clerk and "
                           "Treasurer"),
                guide("lists Dawn Dwyer as Lyndon's "
                      "treasurer")],
               [holder("Dawn Dwyer", "dawn-dwyer")]),
        office("moderator", "Moderator", "Lyndon Moderator", 1,
               [charter126("section 22: a Moderator is "
                           "elected to a one-year term. The "
                           "2025 town report seats Dan Daley "
                           "III with a term expiring in "
                           "2026 and no official source "
                           "publishes the 2026 outcome, so "
                           "the post is created without a "
                           "membership")]),
        office("lister", "Lister", "Lyndon Board of Listers", 3,
               [charter126("section 22: Listers are "
                           "elected to three-year terms, "
                           "their number (three, four, or "
                           "five) determined by the "
                           "Selectboard; Lyndon carries "
                           "three"),
                lyn_report("'Town Officers 2025' table: "
                           "Listers Carol Fisher (term to "
                           "2027) and Linda Lee (2028); "
                           "Lawrence Willey's term expired "
                           "in 2026 with no published "
                           "outcome, so his seat is "
                           "unfilled")],
               [holder("Carol Fisher", "carol-fisher"),
                holder("Linda Lee", "linda-lee")]),
        office("library-trustee", "Cobleigh Library Trustee",
               "Lyndon Cobleigh Library Trustees", 5,
               [charter126("section 22: five Cobleigh "
                           "Library Trustees are elected to "
                           "five-year terms"),
                lyn_report("'Town Officers 2025' table: "
                           "Sylvia Dodge (term to 2027), "
                           "Jessica Drew Simpson (2028), "
                           "Mary Thomas (2029), and Bruce "
                           "Starbuck (2030); Paula Pearce's "
                           "term expired in 2026 with no "
                           "published outcome, so her seat "
                           "is unfilled")],
               [holder("Sylvia Dodge", "sylvia-dodge"),
                holder("Jessica Drew Simpson",
                       "jessica-drew-simpson"),
                holder("Mary Thomas", "mary-thomas"),
                holder("Bruce Starbuck", "bruce-starbuck")]),
        office("sanborn-school-fund-trustee",
               "Trustee of the Sanborn School Fund",
               "Lyndon Sanborn School Fund Trustees", 3,
               [charter126("section 22: three Trustees of "
                           "the Sanborn School Fund are "
                           "elected to three-year terms"),
                lyn_report("'Town Officers 2025' table: "
                           "Kelly Harris (term to 2027) "
                           "and David Stahler Sr. (2028); "
                           "Eric Paris's term expired in "
                           "2026 with no published "
                           "outcome, so his seat is "
                           "unfilled")],
               [holder("Kelly Harris", "kelly-harris"),
                holder("David Stahler Sr.",
                       "david-stahler-sr")]),
        office("town-agent", "Town Agent", "Lyndon Town Agent", 1,
               [charter126("section 22: a Town Agent is "
                           "elected to a one-year term; the "
                           "town officers table lists no "
                           "holder, so the post is created "
                           "without a membership")]),
        office("collector-of-delinquent-taxes",
               "Delinquent Tax Collector",
               "Lyndon Collector of Delinquent Taxes", 1,
               [lyn_report("'Appointed by the Selectboard' "
                           "page: 'Delinquent Tax "
                           "Collector: Treasurer, Dawn "
                           "Dwyer'")],
               [holder("Dawn Dwyer", "dawn-dwyer",
                       how_seated="appointed")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Lyndon Justices of the Peace", 15,
               [jp_src("names fifteen justices of the peace "
                       "for Lyndon: Jeremiah Aiken, "
                       "Catherine Boykin, Kevin Calkins, Dan "
                       "Daley, Elizabeth Dronkert, Libre "
                       "Drouin, Reed Garfield, Robert "
                       "Gerrish, Bruce James, Sue Mason, "
                       "Sean McFeeley, Brenda Mitchell, "
                       "Beth Quimby, Susan Russell, and "
                       "Kelsey Stetson"),
                lyn_report("'Town Officers 2025' table's "
                           "JP block names Ashley Gerrish "
                           "where the certified listing "
                           "names Brenda Mitchell, and "
                           "prints 'Sue Russell' for Susan "
                           "Russell; the certified listing "
                           "governs")],
               [holder("Jeremiah Aiken", "jeremiah-aiken"),
                holder("Catherine Boykin", "catherine-boykin"),
                holder("Kevin Calkins", "kevin-calkins"),
                holder("Dan Daley III", "dan-daley-iii",
                       ballot_name="Dan Daley"),
                holder("Elizabeth Dronkert",
                       "elizabeth-dronkert"),
                holder("Libre Drouin", "libre-drouin"),
                holder("Reed Garfield", "reed-garfield"),
                holder("Robert Gerrish", "robert-gerrish",
                       existing_person_id="ocd-person/ea509170-829e-57a1-8b39-bc699fe38510"),
                holder("Bruce James", "bruce-james"),
                holder("Sue Mason", "sue-mason"),
                holder("Sean McFeeley", "sean-mcfeeley"),
                holder("Brenda Mitchell", "brenda-mitchell"),
                holder("Beth Quimby", "beth-quimby"),
                holder("Susan Russell", "susan-russell"),
                holder("Kelsey Stetson", "kelsey-stetson")]),
    ]
    return spec("lyndon", "Lyndon", offices,
                jp=jp_election(
                    "lyndon-vt", "Lyndon", 15,
                    "the winners were Jeremiah Aiken, "
                    "Catherine Boykin, Kevin Calkins, Dan "
                    "Daley, Elizabeth Dronkert, Libre "
                    "Drouin, Reed Garfield, Robert Gerrish, "
                    "Bruce James, Sue Mason, Sean McFeeley, "
                    "Brenda Mitchell, Beth Quimby, Susan "
                    "Russell, and Kelsey Stetson"))


SPECS["lyndon"] = lyndon_spec()

# ------------------------------------------------------------ emit
for slug in ORDER:
    s = SPECS[slug]
    p = OUT / f"{s['place_slug']}.json"
    p.write_text(json.dumps(s, indent=1) + "\n")
    n_off = len(s["offices"])
    n_hold = sum(len(o.get("holders", ())) for o in s["offices"])
    print(f"{s['place_slug']}: {n_off} offices, {n_hold} holders")
print(f"TOTAL: {len(SPECS)} specs")
