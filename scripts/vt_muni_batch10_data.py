#!/usr/bin/env python3
"""Batch 10 of the VT #163 municipal fan-out (alphabetical positions
90-99): Granville, Greensboro, Groton, Guildhall, Guilford, Halifax,
Hancock, Hardwick, Hartford, Hartland. Emits one JSON spec per
municipality for build_vt_municipality.py.
Research: vt_muni_batch10_research.md.

Identity calls baked into this batch (all flagged on #163):
- Hartford Treasurer Joe Major, Hartford JP Rebecca White, and
  Hartland JP John Bartholomew are the sitting Windsor-district
  state senator, Windsor-district state senator, and Windsor-1
  state representative respectively -- their legislature bios
  place all three in these towns (Major's bio names his Hartford
  treasurership; Bartholomew's bio lists his Hartland JP seat).
  Their existing state-tier person records are REUSED via
  existing_person_id; the JP candidacies are appended by hand.
- Hancock's JP listing form "Maurice Eaton Jr" and its town-table
  "Maurice Eaton" (cemetery commissioner + budget committee) are
  one person record: a single slug carries all three seats, with
  the JP ballot_name carrying the listing's form.
- Greensboro's Selectboard chair, styled only "MacNeil" in every
  official source, is HELD as a straggler -- the seat is unfilled
  in the data rather than minted on a partial name.
- Hartland is built from the SOS spine only (Bloomfield shape):
  its town website was unreachable on every path tried.
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
CHARTER_123 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/123",
    "note": "PLACEHOLDER",
}
CHARTER_123A = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/123A",
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


def charter123(phrase):
    return S(CHARTER_123, "Charter of the Town of Hardwick, 24 App. "
             f"V.S.A. ch. 123 (official text, Vermont General "
             f"Assembly): {phrase}")


def charter123a(phrase):
    return S(CHARTER_123A, "Charter of the Town of Hartford, 24 App. "
             f"V.S.A. ch. 123A (official text, Vermont General "
             f"Assembly): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 10); issue #163 "
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
                  f"# municipal fan-out batch 10; issue #163 "
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

# ------------------------------------------------------------ Granville
GRV_REPORT = {
    "url": "https://granvillevermont.org/wp-content/uploads/2026/02/Town-Report-for-Website.pdf",
    "note": "PLACEHOLDER",
}
GRV_MIN26 = {
    "url": "https://granvillevermont.org/wp-content/uploads/2026/03/Annual-Town-Meeting-Minutes-2026.pdf",
    "note": "PLACEHOLDER",
}
GRV_MIN25 = {
    "url": "https://granvillevermont.org/wp-content/uploads/2025/03/Annual-Town-Meeting-2025-Minutes.pdf",
    "note": "PLACEHOLDER",
}


def grv_report(what):
    return S(GRV_REPORT, "Town of Granville 2026 Town Report "
             f"(granvillevermont.org): {what}")


def grv_min26(what):
    return S(GRV_MIN26, "Town of Granville, Minutes of the Annual "
             f"Town Meeting, March 3, 2026 (granvillevermont.org): "
             f"{what}")


def grv_min25(what):
    return S(GRV_MIN25, "Town of Granville, Minutes of the Annual "
             f"Town Meeting, March 4, 2025 (granvillevermont.org): "
             f"{what}")


def granville_spec():
    label = "Town of Granville"
    offices = [
        office("selectboard", "Selectboard Member",
               "Granville Selectboard", 3,
               [grv_min26("Robert Readie was elected to a three-year "
                          "term (26 votes to Kevin Bagley's 10) and "
                          "Jared Rouleau to the two years remaining "
                          "on a term ending 2028 (24 votes); the "
                          "board is Readie, Rouleau, and Michael "
                          "Eramo, whose term runs to 2027."),
                sb_dir("lists Granville's three selectboard members "
                       "as Michael Eramo, Robert Readie (Chair), and "
                       "Jared Rouleau -- concordant with the town's "
                       "own 2026 meeting minutes.")],
               [holder("Robert Readie", "robert-readie"),
                holder("Jared Rouleau", "jared-rouleau"),
                holder("Michael Eramo", "michael-eramo")]),
        office("moderator", "Moderator", "Granville Moderator", 1,
               [grv_min26("Kelli Eckroth was elected Moderator for "
                          "the ensuing year and presided over the "
                          "March 3, 2026 meeting.")],
               [holder("Kelli Eckroth", "kelli-eckroth")]),
        office("town-clerk", "Town Clerk", "Granville Town Clerk", 1,
               [guide("lists Cheryl Sargeant as Granville town "
                      "clerk."),
                clerk_xlsx("lists Cheryl Sargeant as Granville town "
                           "clerk."),
                grv_report("the March 3, 2026 Warning is attested by "
                           "Cheryl L. Sargeant as Town Clerk; no "
                           "clerk election stood in 2026.")],
               [holder("Cheryl Sargeant", "cheryl-sargeant")]),
        office("town-treasurer", "Town Treasurer",
               "Granville Town Treasurer", 1,
               [guide("lists Nancy Needham as Granville town "
                      "treasurer."),
                treas_xlsx("lists Nancy Needham as Granville town "
                           "treasurer."),
                grv_report("no treasurer election stood at the "
                           "March 2026 meeting.")],
               [holder("Nancy Needham", "nancy-needham")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Granville Collector of Delinquent Taxes", 1,
               [grv_min26("Nancy Needham was re-elected Collector of "
                          "Delinquent Taxes for the ensuing year.")],
               [holder("Nancy Needham", "nancy-needham")]),
        office("first-constable", "First Constable",
               "Granville First Constable", 1,
               [grv_min26("Mark Belisle was re-elected First "
                          "Constable for a two-year term ending "
                          "2028.")],
               [holder("Mark Belisle", "mark-belisle")]),
        office("second-constable", "Second Constable",
               "Granville Second Constable", 1,
               [grv_min26("Jennifer Stickney was elected Second "
                          "Constable, 13 votes to Jeffrey Lumbra's "
                          "10."),
                grv_min25("Jennifer Stickney was likewise elected "
                          "Second Constable in 2025.")],
               [holder("Jennifer Stickney", "jennifer-stickney")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Granville Cemetery Commission", 3,
               [grv_min26("Veronica Parrish was elected Cemetery "
                          "Commissioner to a three-year term ending "
                          "2029 (the Second seat in the commission's "
                          "First/Second/Third rotation)."),
                grv_min25("Kate Stauss was elected Cemetery "
                          "Commissioner to the two years remaining "
                          "on a term ending 2027, and William "
                          "Brokof to a three-year term ending "
                          "2028. The commission's First, Second, "
                          "and Third seats rotate on the pattern "
                          "the two meetings' minutes fix.")],
               [holder("Kate Stauss", "kate-stauss"),
                holder("Veronica Parrish", "veronica-parrish"),
                holder("William Brokof", "william-brokof")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Granville Justices of the Peace", 5,
               [jp_src("lists five justices of the peace for "
                       "Granville.")],
               [holder("Janet Brown", "janet-brown"),
                holder("Nancy Demers", "nancy-demers"),
                holder("Kristina Fuller", "kristina-fuller"),
                holder("Robin Hagerman", "robin-hagerman"),
                holder("James Parrish", "james-parrish")]),
    ]
    return spec("granville", label, offices,
                jp_election("granville-vt", label, 5,
                            "the SOS listing names the five "
                            "Granville winners of the November 5, "
                            "2024 justice of the peace election."))


SPECS.append(granville_spec())

# ----------------------------------------------------------- Greensboro
GBO_REPORT = {
    "url": "https://greensborovt.gov/wp-content/uploads/town-office-documents/Town-Report/2026-Town-Report.pdf",
    "note": "PLACEHOLDER",
}
GBO_SB_PAGE = {
    "url": "https://greensborovt.gov/selectboard/",
    "note": "PLACEHOLDER",
}
GBO_MINUTES = {
    "url": "https://greensborovt.gov/wp-content/uploads/documents/Minutes/Selectboard/2026-0909-SB-meeting/2026-0909-SB-minutes.pdf",
    "note": "PLACEHOLDER",
}


def gbo_report(what):
    return S(GBO_REPORT, "Town of Greensboro 2026 Town Report "
             f"(greensborovt.gov): {what}")


def gbo_sb(what):
    return S(GBO_SB_PAGE, "Town of Greensboro Selectboard page "
             f"(greensborovt.gov): {what}")


def greensboro_spec():
    label = "Town of Greensboro"
    offices = [
        office("selectboard", "Selectboard Member",
               "Greensboro Selectboard", 5,
               [gbo_sb("lists the sitting board with terms: Ellen "
                       "Celnik to 2028, Tim Brennan to 2028, Mike "
                       "Metcalf to 2027, Judy Carpenter to 2029, "
                       "and the Chair, whose term runs to 2027 and "
                       "who is styled only by the surname MacNeil "
                       "in every official source -- the town "
                       "report's officers table, the board's "
                       "minutes, and the town contact page alike. "
                       "The Chair's seat is left unfilled rather "
                       "than minted on a partial name; the 2026 "
                       "Warning stood exactly the two seats "
                       "(Celnik's and Carpenter's) whose printed "
                       "terms the page updates."),
                S(GBO_MINUTES, "Town of Greensboro Selectboard "
                    "minutes, September 9, 2026 (greensborovt.gov): "
                    "the board sits as MacNeil (Chair), Ellen "
                    "Celnik, Tim Brennan, Mike Metcalf, and Judy "
                    "Carpenter.")],
               [holder("Ellen Celnik", "ellen-celnik"),
                holder("Tim Brennan", "tim-brennan"),
                holder("Mike Metcalf", "mike-metcalf"),
                holder("Judy Carpenter", "judy-carpenter")]),
        office("moderator", "Moderator", "Greensboro Moderator", 1,
               [gbo_report("the officers table seats Timothy Nisbet "
                           "as Moderator on a one-year term that "
                           "expired at the March 2026 meeting, and "
                           "the 2026 Warning stood the office for "
                           "one year. Structure only: the outcome "
                           "is published in no official source read. "
                           "Nisbet is minted below as a justice of "
                           "the peace on the SOS listing.")]),
        office("town-clerk", "Town Clerk", "Greensboro Town Clerk",
               1,
               [guide("lists Kim Greaves as Greensboro town clerk."),
                gbo_report("the 2026 Warning, Article 1, stood the "
                           "clerkship for a three-year term at the "
                           "March 2026 meeting and Greaves signed "
                           "the warning as Town Clerk; she also "
                           "appears in the Selectboard's September "
                           "9, 2026 minutes. Structure only: the "
                           "town publishes no outcome for a seat its "
                           "own warning stood, so the incumbent is "
                           "not minted on directory currency "
                           "alone.")]),
        office("town-treasurer", "Town Treasurer",
               "Greensboro Town Treasurer", 1,
               [guide("lists Brett Stanciu as Greensboro town "
                      "treasurer."),
                gbo_report("the treasurer appears in neither the "
                           "2026 Warning's elective articles nor "
                           "the report's elected-officers table; "
                           "the clerk's report welcomes Stanciu "
                           "back 'as Zoning Administrator and "
                           "Treasurer,' and the town contact page "
                           "names her to the office. Recorded as "
                           "an appointment to a town office.")],
               [holder("Brett Stanciu", "brett-stanciu",
                       how_seated="appointed")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Greensboro Collector of Delinquent Taxes", 1,
               [gbo_report("the officers table seats Mike Cloutier "
                           "as Collector of Delinquent Taxes on a "
                           "one-year term that expired at the "
                           "March 2026 meeting (Warning Article 17 "
                           "proposed making the Treasurer the "
                           "collector; its outcome is likewise "
                           "unpublished). Structure only.")]),
        office("constable", "Town Constable",
               "Greensboro Town Constable", 1,
               [gbo_report("the town's Selectboard Appointments "
                           "list names Mark Snyder as Constable. "
                           "Recorded as an appointment; the "
                           "constable is not in the warning's "
                           "elective articles.")],
               [holder("Mark Snyder", "mark-snyder",
                       how_seated="appointed")]),
        office("trustee-of-public-funds", "Trustee of Public Funds",
               "Greensboro Trustees of Public Funds", 3,
               [gbo_report("the officers table seats Peggy Lipscomb "
                           "to 2027 and Sherral Lumsden to 2028; "
                           "no 2026 article stood a third seat, and "
                           "the third seat is left unfilled.")],
               [holder("Peggy Lipscomb", "peggy-lipscomb"),
                holder("Sherral Lumsden", "sherral-lumsden")]),
        office("library-trustee", "Library Trustee",
               "Greensboro Library Trustees", 6,
               [gbo_report("the officers table seats six elected "
                           "trustees of the Greensboro Free "
                           "Library: Valerie Carter to 2028, Galen "
                           "Fisher to 2028, Jennifer Lucas to 2027, "
                           "and Fan Watkinson to 2027 are minted; "
                           "the seats of Carol Reynolds (one-year) "
                           "and Jan Terwiesch (three-year) stood at "
                           "the March 2026 meeting under the "
                           "warning's library articles and their "
                           "outcomes are unpublished, so those "
                           "seats are unfilled. The table's two "
                           "alternates are not trustees.")],
               [holder("Valerie Carter", "valerie-carter"),
                holder("Galen Fisher", "galen-fisher"),
                holder("Jennifer Lucas", "jennifer-lucas"),
                holder("Fan Watkinson", "fan-watkinson")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Greensboro Cemetery Commission", 3,
               [gbo_report("the officers table seats Patsy Mercier "
                           "to 2027 and Wayne Young to 2028; the "
                           "third seat (MacNeil's) stood in 2026 "
                           "and is unfilled.")],
               [holder("Patsy Mercier", "patsy-mercier"),
                holder("Wayne Young", "wayne-young")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Greensboro Justices of the Peace", 5,
               [jp_src("lists five justices of the peace for "
                       "Greensboro."),
                gbo_report("the report's Board of Civil Authority "
                           "block names the same five.")],
               [holder("Tim Nisbet", "tim-nisbet"),
                holder("Mike Metcalf", "mike-metcalf"),
                holder("Stew Arnold", "stew-arnold"),
                holder("Maya McCoy", "maya-mccoy"),
                holder("Judy Carpenter", "judy-carpenter")]),
    ]
    return spec("greensboro", label, offices,
                jp_election("greensboro-vt", label, 5,
                            "the SOS listing names the five "
                            "Greensboro winners of the November 5, "
                            "2024 justice of the peace election."))


SPECS.append(greensboro_spec())

# --------------------------------------------------------------- Groton
GRO_REPORTS = {
    "url": "https://grotonvt.com/town-reports",
    "note": "PLACEHOLDER",
}


def gro_report(what):
    return S(GRO_REPORTS, "Town of Groton 2025 Town Report, "
             f"published at the town's reports page "
             f"(grotonvt.com/town-reports): {what}")


def groton_spec():
    label = "Town of Groton"
    offices = [
        office("selectboard", "Selectboard Member",
               "Groton Selectboard", 3,
               [gro_report("the ELECTED OFFICERS table seats Larry "
                           "Daniels (Chair) to 2027 and Mike "
                           "Nahmias to 2028; Tom Page's term "
                           "expired in 2026 and no successor is "
                           "published, so the third seat is "
                           "unfilled. (A companion roster that "
                           "seats Dawn Evans on this board is not "
                           "followed: in the town's own table "
                           "Evans is an appointed planning "
                           "commissioner and an elected library "
                           "trustee.)")],
               [holder("Larry Daniels", "larry-daniels"),
                holder("Mike Nahmias", "mike-nahmias")]),
        office("moderator", "Moderator", "Groton Moderator", 1,
               [gro_report("the elected table seats Wayne Dyer as "
                           "Moderator on a one-year term that "
                           "expired in 2026. Structure only: no "
                           "successor is published.")]),
        office("town-clerk", "Town Clerk", "Groton Town Clerk", 1,
               [guide("lists Carrie Peters as Groton town clerk."),
                gro_report("the town's officers table and contact "
                           "page seat Carrie Peters as Town Clerk "
                           "on a term that expired in 2026. "
                           "Structure only: the town publishes no "
                           "outcome for the seat. Peters is "
                           "minted below as a justice of the peace "
                           "on the SOS listing.")]),
        office("town-treasurer", "Town Treasurer",
               "Groton Town Treasurer", 1,
               [guide("lists Lisa Hart as Groton town treasurer."),
                gro_report("the elected table seats Lisa Hart as "
                           "Town Treasurer to 2027.")],
               [holder("Lisa Hart", "lisa-hart")]),
        office("road-commissioner", "Road Commissioner",
               "Groton Road Commissioner", 1,
               [gro_report("the elected table seats Harold Hatch "
                           "as Road Commissioner to 2027.")],
               [holder("Harold Hatch", "harold-hatch")]),
        office("constable", "Town Constable",
               "Groton Town Constable", 1,
               [gro_report("the elected table seats Dan Webster as "
                           "Town Constable on a one-year term that "
                           "expired in 2026. Structure only.")]),
        office("library-trustee", "Library Trustee",
               "Groton Library Trustees", 5,
               [gro_report("the elected table seats Dawn Evans to "
                           "2028, Jennifer Gaiss to 2027, Donna "
                           "Russo-Savage to 2027, and Wayne Knott "
                           "to 2028; Deborah Jurist's term expired "
                           "in 2026 and that seat is unfilled.")],
               [holder("Dawn Evans", "dawn-evans"),
                holder("Jennifer Gaiss", "jennifer-gaiss"),
                holder("Donna Russo-Savage", "donna-russo-savage"),
                holder("Wayne Knott", "wayne-knott")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Groton Cemetery Commission", 3,
               [gro_report("the elected table seats Brent Smith "
                           "to 2028 and Susan Plant to 2027 (the "
                           "contact page's 'Sue Plant'); Steven "
                           "Batchelder's term expired in 2026 and "
                           "that seat is unfilled.")],
               [holder("Brent Smith", "brent-smith"),
                holder("Susan Plant", "susan-plant")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Groton Justices of the Peace", 7,
               [jp_src("lists seven justices of the peace for "
                       "Groton."),
                gro_report("the report's Board of Civil Authority "
                           "block names the same seven (printing "
                           "the second as Tirone 'Toni' Dyer; the "
                           "SOS listing's Toni Dyer is used).")],
               [holder("Carrie Peters", "carrie-peters"),
                holder("Brent Smith", "brent-smith"),
                holder("Toni Dyer", "toni-dyer"),
                holder("Tim Dailey Sr", "tim-dailey-sr"),
                holder("Dorothy Knott", "dorothy-knott"),
                holder("Linda Nunn", "linda-nunn"),
                holder("Deborah Jurist", "deborah-jurist")]),
    ]
    return spec("groton", label, offices,
                jp_election("groton-vt", label, 7,
                            "the SOS listing names the seven "
                            "Groton winners of the November 5, 2024 "
                            "justice of the peace election."))


SPECS.append(groton_spec())

# ------------------------------------------------------------ Guildhall
GHD = "https://guildhallvt.org"


def ghd_page(page, what):
    return {"url": f"{GHD}/{page}",
            "note": f"Town of Guildhall {page.split('.')[0].replace('-', ' ')} "
                    f"page (guildhallvt.org): {what}"}


def guildhall_spec():
    label = "Town of Guildhall"
    offices = [
        office("selectboard", "Selectboard Member",
               "Guildhall Selectboard", 3,
               [sb_dir("lists Guildhall's three selectboard "
                       "members as Gary Brown (Chair), John "
                       "Orlowski (Vice-Chair), and Jason "
                       "Sterling."),
                ghd_page("select-board.html",
                         "the town's selectboard page names the "
                         "same three.")],
               [holder("Gary Brown", "gary-brown"),
                holder("John Orlowski", "john-orlowski"),
                holder("Jason Sterling", "jason-sterling")]),
        office("town-clerk", "Town Clerk", "Guildhall Town Clerk",
               1,
               [guide("lists George Blakeslee as Guildhall town "
                      "clerk."),
                ghd_page("town-clerk.html",
                         "the town's clerk page names George "
                         "Blakeslee as Town Clerk with a term "
                         "running to 2028.")],
               [holder("George Blakeslee", "george-blakeslee")]),
        office("town-treasurer", "Town Treasurer",
               "Guildhall Town Treasurer", 1,
               [guide("lists George Blakeslee as Guildhall town "
                      "treasurer."),
                ghd_page("town-treasurer.html",
                         "the town's treasurer page names George "
                         "Blakeslee as Town Treasurer with a term "
                         "running to 2028; the treasurer also "
                         "acts as the town's tax collector, so no "
                         "separate delinquent-tax-collector post "
                         "is created.")],
               [holder("George Blakeslee", "george-blakeslee")]),
        office("moderator", "Moderator", "Guildhall Moderator", 1,
               [statute2646_structure("a moderator")]),
        office("auditor", "Auditor", "Guildhall Auditors", 3,
               [ghd_page("auditors.html",
                         "the town's auditors page names Ed Clark "
                         "(term to 2029), Kelly McLain (to 2027), "
                         "and Bill Ghelli (to 2028).")],
               [holder("Ed Clark", "ed-clark"),
                holder("Kelly McLain", "kelly-mclain"),
                holder("Bill Ghelli", "bill-ghelli")]),
        office("lister", "Lister", "Guildhall Listers", 3,
               [ghd_page("lister-board.html",
                         "the town's lister page names George "
                         "Blakeslee (to 2027), Eileen Thietten "
                         "(to 2028), and Patricia Brown (to 2029; "
                         "the page's 'Patrica' is corrected to the "
                         "form the town's cemetery page prints).")],
               [holder("George Blakeslee", "george-blakeslee"),
                holder("Eileen Thietten", "eileen-thietten"),
                holder("Patricia Brown", "patricia-brown")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Guildhall Cemetery Commission", 3,
               [ghd_page("cemetery-commission.html",
                         "the town's cemetery page names Gary "
                         "Brown (to 2028), Patricia Brown (to "
                         "2029), and Rich Schiller (to 2027).")],
               [holder("Gary Brown", "gary-brown"),
                holder("Patricia Brown", "patricia-brown"),
                holder("Rich Schiller", "rich-schiller")]),
        office("road-commissioner", "Road Commissioner",
               "Guildhall Road Commissioner", 1,
               [ghd_page("road-commission.html",
                         "the town's road commission page names "
                         "Gary Brown as Road Commissioner. The "
                         "page does not state the mode of "
                         "selection; the office is a town office "
                         "under 17 V.S.A. section 2646 and the "
                         "holder is recorded as elected.")],
               [holder("Gary Brown", "gary-brown")]),
        office("grand-juror", "Grand Juror",
               "Guildhall Grand Juror", 1,
               [statute2646_structure("a grand juror")]),
        office("town-agent", "Town Agent", "Guildhall Town Agent",
               1,
               [statute2646_structure("a town agent")]),
        office("trustee-of-public-funds", "Trustee of Public Funds",
               "Guildhall Trustees of Public Funds", 3,
               [statute2646_structure("trustees of public funds")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Guildhall Justices of the Peace", 5,
               [jp_src("lists five justices of the peace for "
                       "Guildhall.")],
               [holder("Rebecca Bacon", "rebecca-bacon"),
                holder("Casey Dowland", "casey-dowland"),
                holder("Valerie Foy", "valerie-foy"),
                holder("Kelly McLain", "kelly-mclain"),
                holder("Sarah Sterling", "sarah-sterling")]),
    ]
    return spec("guildhall", label, offices,
                jp_election("guildhall-vt", label, 5,
                            "the SOS listing names the five "
                            "Guildhall winners of the November 5, "
                            "2024 justice of the peace election."))


SPECS.append(guildhall_spec())

# -------------------------------------------------------------- Guilford
GUI_REPORT = {
    "url": "https://guilfordvt.gov/wp-content/uploads/2026/02/Guilford-Town-Report-FY2025-FINAL.pdf",
    "note": "PLACEHOLDER",
}
GUI_RESULTS = {
    "url": "https://guilfordvt.gov/march-3rd-official-election-results/",
    "note": "PLACEHOLDER",
}
GUI_SB = {
    "url": "https://guilfordvt.gov/boards-and-commissions/selectboard/",
    "note": "PLACEHOLDER",
}
GUI_DTC = {
    "url": "https://guilfordvt.gov/collector-of-delinquent-taxes/",
    "note": "PLACEHOLDER",
}
GUI_CEM = {
    "url": "https://guilfordvt.gov/boards-and-commissions/cemetery-commission/",
    "note": "PLACEHOLDER",
}


def gui_report(what):
    return S(GUI_REPORT, "Town of Guilford FY2025 Town Report "
             f"(guilfordvt.gov): {what}")


def gui_results(what):
    return S(GUI_RESULTS, "Town of Guilford, 'March 3rd Official "
             f"Election Results' (guilfordvt.gov): {what}")


def guilford_spec():
    label = "Town of Guilford"
    offices = [
        office("selectboard", "Selectboard Member",
               "Guilford Selectboard", 5,
               [S(GUI_SB, "Town of Guilford Selectboard page "
                    "(guilfordvt.gov): lists Sheila Morse (Chair), "
                    "Tara Cheney (Vice-Chair), Michael Szostak, "
                    "Kimberly Frost, and Chip Carter."),
                gui_report("the March 4, 2025 town meeting "
                           "minutes in the report record Morse "
                           "elected to a three-year term and "
                           "Cheney to a two-year term."),
                gui_results("the town's official March 3, 2026 "
                            "results elect Kimberly M. Frost to a "
                            "three-year term and Michael Szostak "
                            "to a two-year term."),
                sb_dir("lists no Guilford roster; the town's own "
                       "pages carry the board.")],
               [holder("Sheila Morse", "sheila-morse"),
                holder("Tara Cheney", "tara-cheney"),
                holder("Michael Szostak", "michael-szostak"),
                holder("Kimberly Frost", "kimberly-frost"),
                holder("Chip Carter", "chip-carter")]),
        office("moderator", "Moderator", "Guilford Moderator", 1,
               [gui_report("the moderator is elected at the floor "
                           "town meeting (February 28, 2026 for "
                           "this cycle); the winner is published "
                           "in no official source read. Structure "
                           "only.")]),
        office("town-clerk", "Town Clerk", "Guilford Town Clerk", 1,
               [gui_results("the town's official March 3, 2026 "
                            "results re-elect Uriel Najera Town "
                            "Clerk to a three-year term."),
                gui_report("Najera won the remaining one year of "
                           "the clerk's term at the March 4, 2025 "
                           "meeting with 500 votes."),
                guide("lists Uriel Najera as Guilford town "
                      "clerk.")],
               [holder("Uriel Najera", "uriel-najera")]),
        office("town-treasurer", "Town Treasurer",
               "Guilford Town Treasurer", 1,
               [guide("lists Ellen Majonen as Guilford town "
                      "treasurer."),
                gui_report("calls Ellen 'Elly' Majonen 'our "
                           "Treasurer' in the treasurer's report; "
                           "the office appears in neither the 2025 "
                           "meeting's elective business nor the "
                           "2026 ballot warning's elective list. "
                           "Recorded as an appointment to a town "
                           "office.")],
               [holder("Ellen Majonen", "ellen-majonen",
                       how_seated="appointed")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Guilford Collector of Delinquent Taxes", 1,
               [S(GUI_DTC, "Town of Guilford Collector of "
                    "Delinquent Taxes page (guilfordvt.gov): the "
                    "office 'is appointed each year by the Town "
                    "Selectboard' and Ellen (Elly) Majonen holds "
                    "it.")],
               [holder("Ellen Majonen", "ellen-majonen",
                       how_seated="appointed")]),
        office("lister", "Lister", "Guilford Listers", 3,
               [gui_report("the March 4, 2025 minutes elect "
                           "Richard 'Dick' Smith lister to a "
                           "three-year term, and the listers' own "
                           "report is signed by Smith, Shaun "
                           "Murphy, and Steve Soszynski."),
                gui_results("the official March 3, 2026 results "
                            "elect Shaun Murphy lister to a "
                            "three-year term.")],
               [holder("Richard Smith", "richard-smith"),
                holder("Shaun Murphy", "shaun-murphy"),
                holder("Steve Soszynski", "steve-soszynski")]),
        office("auditor", "Auditor", "Guilford Auditors", 3,
               [gui_report("the March 4, 2025 minutes elect "
                           "Lyndsey Mitchell auditor to a "
                           "three-year term (the third seat, "
                           "Reita Lashway's one-year remainder, "
                           "expired in 2026 with no successor in "
                           "the 2026 warning, so it is unfilled)."),
                gui_results("the official March 3, 2026 results "
                            "elect Skye Morse auditor to a "
                            "three-year term.")],
               [holder("Lyndsey Mitchell", "lyndsey-mitchell"),
                holder("Skye Morse", "skye-morse")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Guilford Cemetery Commission", 5,
               [S(GUI_CEM, "Town of Guilford Cemetery Commission "
                    "page (guilfordvt.gov): the commissioners "
                    "serve five-year staggered terms with one "
                    "seat elected at each annual floor meeting, "
                    "which fixes five seats."),
                gui_report("the March 4, 2025 floor meeting "
                           "elected Carol Schnabel a cemetery "
                           "commissioner; the February 28, 2026 "
                           "floor winner and the remaining seats "
                           "are published nowhere official, so "
                           "they are unfilled.")],
               [holder("Carol Schnabel", "carol-schnabel")]),
        office("trustee-of-public-funds", "Trustee of Public Funds",
               "Guilford Trustees of Public Funds", 5,
               [gui_report("the trustees of public funds serve "
                           "five-year staggered terms with one "
                           "seat elected at each annual floor "
                           "meeting, which fixes five seats; the "
                           "March 4, 2025 floor meeting elected "
                           "Todd Mandell. The 2026 floor winner "
                           "and the remaining seats are "
                           "unpublished and unfilled.")],
               [holder("Todd Mandell", "todd-mandell")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Guilford Justices of the Peace", 10,
               [jp_src("lists ten justices of the peace for "
                       "Guilford.")],
               [holder("Roberta Bremmer", "roberta-bremmer"),
                holder("Sara Coffey", "sara-coffey"),
                holder("Pat Haine", "pat-haine"),
                holder("Doug Hunt", "doug-hunt"),
                holder("Skye Morse", "skye-morse"),
                holder("Wallace Don McLean", "wallace-don-mclean"),
                holder("Todd Mandell", "todd-mandell"),
                holder("Lori Nelson", "lori-nelson"),
                holder("Anna Klein", "anna-klein"),
                holder("Catherine Wilken", "catherine-wilken")]),
    ]
    return spec("guilford", label, offices,
                jp_election("guilford-vt", label, 10,
                            "the SOS listing names the ten "
                            "Guilford winners of the November 5, "
                            "2024 justice of the peace election. "
                            "No library-trustee post is created: "
                            "the Guilford Free Library's nine-"
                            "trustee board mixes town-elected and "
                            "association trustees with no fixed "
                            "elected count in any official source."))


SPECS.append(guilford_spec())

# --------------------------------------------------------------- Halifax
HAL_BOOK = {
    "url": "https://halifaxvt.com/wp-content/uploads/2026/02/Halifax-VT-TOWN-MEETING-BOOK-FY2025-Final-20260202.pdf",
    "note": "PLACEHOLDER",
}
HAL_RETURN = {
    "url": "https://halifaxvt.com/wp-content/uploads/2026/03/Official-Return-of-Votes-March-3-2026.pdf",
    "note": "PLACEHOLDER",
}
HAL_OFFICIALS = {
    "url": "https://halifaxvt.com/contact/town-officials/",
    "note": "PLACEHOLDER",
}


def hal_book(what):
    return S(HAL_BOOK, "Town of Halifax FY2025 Town Meeting Book "
             f"(halifaxvt.com): {what}")


def hal_return(what):
    return S(HAL_RETURN, "Town of Halifax, Official Return of Votes, "
             f"March 3, 2026 (halifaxvt.com): {what}")


def halifax_spec():
    label = "Town of Halifax"
    offices = [
        office("selectboard", "Selectboard Member",
               "Halifax Selectboard", 5,
               [hal_book("the ELECTED OFFICERS table seats Edee "
                         "Edwards (Chair) to 2028, Rhonda Ashcraft "
                         "to 2027, and Lori Marchegiani to 2027."),
                hal_return("the certified March 3, 2026 return "
                           "re-elects Randy Pike to a three-year "
                           "term (124 votes) and Karen "
                           "Christofferson to a two-year term (114)."),
                sb_dir("lists Halifax's five selectboard members "
                       "as Rhonda Ashcraft, Karen Christofferson, "
                       "Edee Edwards, Lori Marchegiani, and Randy "
                       "Pike -- concordant.")],
               [holder("Edee Edwards", "edee-edwards"),
                holder("Rhonda Ashcraft", "rhonda-ashcraft"),
                holder("Lori Marchegiani", "lori-marchegiani"),
                holder("Randy Pike", "randy-pike"),
                holder("Karen Christofferson",
                       "karen-christofferson")]),
        office("moderator", "Moderator", "Halifax Moderator", 1,
               [hal_return("the certified March 3, 2026 return "
                           "elects Paul G. Blais Moderator with "
                           "126 votes.")],
               [holder("Paul Blais", "paul-blais")]),
        office("town-clerk", "Town Clerk", "Halifax Town Clerk", 1,
               [hal_return("the certified March 3, 2026 return "
                           "re-elects Patricia Dow Town Clerk with "
                           "127 votes."),
                guide("lists Patricia Dow as Halifax town clerk.")],
               [holder("Patricia Dow", "patricia-dow")]),
        office("town-treasurer", "Town Treasurer",
               "Halifax Town Treasurer", 1,
               [hal_return("the certified March 3, 2026 return "
                           "re-elects Patricia Dow Town Treasurer "
                           "with 124 votes."),
                guide("lists Patricia Dow as Halifax town "
                      "treasurer.")],
               [holder("Patricia Dow", "patricia-dow")]),
        office("lister", "Lister", "Halifax Listers", 3,
               [hal_book("the elected table seats Mary L. Brewster "
                         "to 2028 and Patricia Dow to 2027."),
                hal_return("the certified March 3, 2026 return "
                           "re-elects Tina Blais lister with 124 "
                           "votes.")],
               [holder("Tina Blais", "tina-blais"),
                holder("Mary Brewster", "mary-brewster"),
                holder("Patricia Dow", "patricia-dow")]),
        office("auditor", "Auditor", "Halifax Auditors", 3,
               [hal_book("the elected table seats Erin L. Lovern "
                         "as an auditor to 2027 and shows the "
                         "other two seats already vacant; the "
                         "town's Auditors page names Lovern as "
                         "the town's auditor. Flagged: the March "
                         "3, 2026 meeting's Article 6 proposed "
                         "eliminating the auditor office under "
                         "17 V.S.A. section 2651b and its outcome "
                         "is published in no source read."),
                hal_return("both 2026 auditor contests drew no "
                           "ballot candidate and only scattered "
                           "write-ins (top counts 3 and 2 against "
                           "126 and 122 blanks); a write-in "
                           "plurality alone does not seat a "
                           "holder, so both seats are unfilled.")],
               [holder("Erin Lovern", "erin-lovern")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Halifax Collector of Delinquent Taxes", 1,
               [hal_return("the certified March 3, 2026 return "
                           "re-elects Mary Brewster Collector of "
                           "Delinquent Taxes with 126 votes.")],
               [holder("Mary Brewster", "mary-brewster")]),
        office("trustee-of-public-funds", "Trustee of Public Funds",
               "Halifax Trustees of Public Funds", 3,
               [hal_book("the elected table seats Steven M. Cohen "
                         "to 2028 and Laurel A. Copeland to 2027."),
                hal_return("the certified March 3, 2026 return "
                           "re-elects Patrick McAllister a "
                           "trustee of public funds with 122 votes "
                           "(the return prints 'Patric').")],
               [holder("Steven Cohen", "steven-cohen"),
                holder("Laurel Copeland", "laurel-copeland"),
                holder("Patrick McAllister", "patrick-mcallister")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Halifax Cemetery Commission", 3,
               [hal_book("the elected table seats Gary Rand to "
                         "2027 and Linda M. Swanson to 2028."),
                hal_return("the certified March 3, 2026 return "
                           "re-elects Laurel A. Copeland a "
                           "cemetery commissioner with 126 votes.")],
               [holder("Laurel Copeland", "laurel-copeland"),
                holder("Gary Rand", "gary-rand"),
                holder("Linda Swanson", "linda-swanson")]),
        office("first-constable", "First Constable",
               "Halifax First Constable", 1,
               [hal_book("constables in Halifax are appointed by "
                         "the Selectboard (the meeting book's "
                         "appointments section names Kyle "
                         "Farnsworth as First Constable for the "
                         "March 2025 cycle). Structure only: the "
                         "2026 appointment is unpublished.")]),
        office("second-constable", "Second Constable",
               "Halifax Second Constable", 1,
               [hal_book("the appointments section names Roy "
                         "Richardson as Second Constable for the "
                         "March 2025 cycle. Structure only: the "
                         "2026 appointment is unpublished.")]),
        office("library-trustee", "Library Trustee",
               "Halifax Whitingham Library Trustees", 1,
               [hal_book("the elected table seats one town-elected "
                         "Trustee to the Whitingham Library: Mark "
                         "Halverson, to 2027.")],
               [holder("Mark Halverson", "mark-halverson")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Halifax Justices of the Peace", 5,
               [jp_src("lists five justices of the peace for "
                       "Halifax."),
                hal_book("the elected table names the same five "
                         "(printing the fifth as Malcolm K. "
                         "Sumner).")],
               [holder("Joan Wonsey-Courser", "joan-wonsey-courser"),
                holder("Patricia Pusey", "patricia-pusey"),
                holder("Kaitlin Stone", "kaitlin-stone"),
                holder("Craig J. Stone", "craig-j-stone"),
                holder("Malcolm Sumner", "malcolm-sumner")]),
    ]
    return spec("halifax", label, offices,
                jp_election("halifax-vt", label, 5,
                            "the SOS listing names the five "
                            "Halifax winners of the November 5, "
                            "2024 justice of the peace election."))


SPECS.append(halifax_spec())

# --------------------------------------------------------------- Hancock
HAN_REPORT = {
    "url": "https://www.hancockvt.org/wp-content/uploads/2026/02/Town-Report-2026-Hancock.pdf",
    "note": "PLACEHOLDER",
}
HAN_MINUTES = {
    "url": "https://www.hancockvt.org/wp-content/uploads/2026/03/Town-Meeting-Minutes-2026.docx",
    "note": "PLACEHOLDER",
}


def han_report(what):
    return S(HAN_REPORT, "Town of Hancock 2026 Town Report "
             f"(hancockvt.org): {what}")


def han_minutes(what):
    return S(HAN_MINUTES, "Town of Hancock, Minutes of the Annual "
             f"Town Meeting, March 3, 2026 (hancockvt.org): {what}")


def hancock_spec():
    label = "Town of Hancock"
    offices = [
        office("selectboard", "Selectboard Member",
               "Hancock Selectboard", 3,
               [han_report("the officers table seats Dan Perera to "
                           "2027 and James Leno to 2028."),
                han_minutes("Scott Gillette was re-elected to the "
                            "Selectboard at the March 3, 2026 "
                            "floor meeting."),
                sb_dir("lists Hancock's three selectboard "
                       "members as Scott Gillette (Chair), James "
                       "Leno, and Dan Perera -- concordant.")],
               [holder("Scott Gillette", "scott-gillette"),
                holder("Dan Perera", "dan-perera"),
                holder("James Leno", "james-leno")]),
        office("moderator", "Moderator", "Hancock Moderator", 1,
               [han_minutes("Scott Gillette was re-elected "
                            "Moderator at the March 3, 2026 "
                            "meeting.")],
               [holder("Scott Gillette", "scott-gillette")]),
        office("town-clerk", "Town Clerk", "Hancock Town Clerk", 1,
               [han_report("the town's current officers table "
                           "names Wendy Stender Town Clerk; the "
                           "office did not stand at the March 2026 "
                           "meeting."),
                guide("lists Wendy Stender as Hancock town "
                      "clerk."),
                clerk_xlsx("lists Wendy Stender as Hancock town "
                           "clerk.")],
               [holder("Wendy Stender", "wendy-stender")]),
        office("town-treasurer", "Town Treasurer",
               "Hancock Town Treasurer", 1,
               [han_report("the officers table names Wendy Stender "
                           "Town Treasurer."),
                guide("lists Wendy Stender as Hancock town "
                      "treasurer.")],
               [holder("Wendy Stender", "wendy-stender")]),
        office("auditor", "Auditor", "Hancock Auditors", 3,
               [han_report("the officers table seats Rose Juliano "
                           "to 2027 and Janet Roth to 2028."),
                han_minutes("Geraldine K. Twitchell was "
                            "re-elected an auditor at the March "
                            "3, 2026 meeting.")],
               [holder("Geraldine Twitchell", "geraldine-twitchell"),
                holder("Rose Juliano", "rose-juliano"),
                holder("Janet Roth", "janet-roth")]),
        office("constable", "Town Constable",
               "Hancock Town Constable", 1,
               [han_minutes("Thomas Patterson was re-elected "
                            "Constable at the March 3, 2026 "
                            "meeting.")],
               [holder("Thomas Patterson", "thomas-patterson")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Hancock Collector of Delinquent Taxes", 1,
               [han_minutes("Wendy Stender was re-elected "
                            "Collector of Delinquent Taxes at the "
                            "March 3, 2026 meeting.")],
               [holder("Wendy Stender", "wendy-stender")]),
        office("road-commissioner", "Road Commissioner",
               "Hancock Road Commissioner", 1,
               [han_minutes("James Leno was re-elected Road "
                            "Commissioner at the March 3, 2026 "
                            "meeting.")],
               [holder("James Leno", "james-leno")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Hancock Cemetery Commission", 3,
               [han_report("the officers table seats Larry Bettis "
                           "to 2027 and Geraldine K. Twitchell to "
                           "2028."),
                han_minutes("Maurice Eaton was re-elected a "
                            "cemetery commissioner at the March 3, "
                            "2026 meeting.")],
               [holder("Maurice Eaton", "maurice-eaton"),
                holder("Larry Bettis", "larry-bettis"),
                holder("Geraldine Twitchell",
                       "geraldine-twitchell")]),
        office("library-trustee", "Library Trustee",
               "Hancock Library Trustees", 5,
               [han_report("the officers table seats Garvi "
                           "Jessa-White to 2027, Margi Rogal to "
                           "2028, Gretchen Perera to 2029, and "
                           "Rose Juliano to 2030."),
                han_minutes("Linda Straley was re-elected a "
                            "library trustee to a five-year term "
                            "at the March 3, 2026 meeting.")],
               [holder("Linda Straley", "linda-straley"),
                holder("Garvi Jessa-White", "garvi-jessa-white"),
                holder("Margi Rogal", "margi-rogal"),
                holder("Gretchen Perera", "gretchen-perera"),
                holder("Rose Juliano", "rose-juliano")]),
        office("budget-committee", "Budget Committee Member",
               "Hancock Budget Committee", 3,
               [han_report("the officers table seats Maurice Eaton "
                           "to 2027 and Marjorie Ross to 2028 on "
                           "the town's elected Advisory Budget "
                           "Committee."),
                han_minutes("Linda Straley was re-elected to the "
                            "Budget Committee at the March 3, "
                            "2026 meeting.")],
               [holder("Linda Straley", "linda-straley"),
                holder("Maurice Eaton", "maurice-eaton"),
                holder("Marjorie Ross", "marjorie-ross")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Hancock Justices of the Peace", 3,
               [jp_src("lists three justices of the peace for "
                       "Hancock (the third as Maurice Eaton "
                       "Jr).")],
               [holder("Monica Collins", "monica-collins"),
                holder("Roger Comes", "roger-comes"),
                holder("Maurice Eaton", "maurice-eaton",
                       ballot_name="Maurice Eaton Jr")]),
    ]
    return spec("hancock", label, offices,
                jp_election("hancock-vt", label, 3,
                            "the SOS listing names the three "
                            "Hancock winners of the November 5, "
                            "2024 justice of the peace election. "
                            "The listers' office carries no post: "
                            "the town's officers table records "
                            "'OFFICE ELIMINATED TM 2022.'"))


SPECS.append(hancock_spec())

# -------------------------------------------------------------- Hardwick
HDK_REPORT = {
    "url": "https://hardwickvt.gov/wp-content/uploads/2026/02/WEB_Hardwick-2025-report.pdf",
    "note": "PLACEHOLDER",
}


def hdk_report(what):
    return S(HDK_REPORT, "Town of Hardwick 2025 Town Report "
             f"(hardwickvt.gov): {what}")


def hardwick_spec():
    label = "Town of Hardwick"
    offices = [
        office("selectboard", "Selectboard Member",
               "Hardwick Selectboard", 5,
               [sb_dir("lists Hardwick's five selectboard members "
                       "as Shari Cornish, Larry Fliegelman, Ceilidh "
                       "Galoway-Kane (Chair), Tim Ricciardello, "
                       "and Derek Richardson. The directory's "
                       "'Galoway-Kane' is a misprint: the town "
                       "report prints Ceilidh Galloway-Kane "
                       "throughout, as does her town email "
                       "address."),
                hdk_report("the pre-meeting officers table seats "
                           "Cornish to 2027 and Ricciardello to "
                           "2028 and shows the three seats that "
                           "stood in March 2026 (two one-year "
                           "seats and Galloway-Kane's three-year "
                           "seat); the post-meeting directory "
                           "board is the five minted here."),
                charter123("section 302(a)(1) makes the five "
                           "selectboard members elective, on the "
                           "section 303 rotation of three "
                           "three-year and two one-year seats, by "
                           "Australian ballot.")],
               [holder("Ceilidh Galloway-Kane",
                       "ceilidh-galloway-kane"),
                holder("Shari Cornish", "shari-cornish"),
                holder("Larry Fliegelman", "larry-fliegelman"),
                holder("Tim Ricciardello", "tim-ricciardello"),
                holder("Derek Richardson", "derek-richardson")]),
        office("moderator", "Moderator", "Hardwick Moderator", 1,
               [charter123("section 302(a)(2) makes the moderator "
                           "elective."),
                hdk_report("the officers table seats Orise "
                           "Ainsworth as Moderator on a one-year "
                           "term that expired at the March 2026 "
                           "meeting, and the 2026 Warning stood "
                           "the office. Structure only: the "
                           "outcome is published in no official "
                           "source read.")]),
        office("town-clerk", "Town Clerk", "Hardwick Town Clerk",
               1,
               [charter123("section 302(a)(5) establishes ONE "
                           "combined elected office of Town Clerk "
                           "and Treasurer on a three-year term "
                           "(section 304(c)); it is modeled as "
                           "the standard two posts with the same "
                           "holder minted to both."),
                hdk_report("the officers table seats Tonia Chase "
                           "as Town Clerk & Town Treasurer on a "
                           "three-year term expiring 2028."),
                guide("lists Tonia Chase as Hardwick town "
                      "clerk.")],
               [holder("Tonia Chase", "tonia-chase")]),
        office("town-treasurer", "Town Treasurer",
               "Hardwick Town Treasurer", 1,
               [charter123("section 302(a)(5): the combined "
                           "Clerk and Treasurer office (see the "
                           "clerk post's note)."),
                hdk_report("Tonia Chase, three-year term expiring "
                           "2028."),
                guide("lists Tonia Chase as Hardwick town "
                      "treasurer.")],
               [holder("Tonia Chase", "tonia-chase")]),
        office("town-agent", "Town Agent", "Hardwick Town Agent",
               1,
               [hdk_report("the officers table seats David "
                           "Shepard as Town Agent on a one-year "
                           "term that expired at the March 2026 "
                           "meeting, and the town's March 3, 2026 "
                           "Warning, Article 3, stands the Town "
                           "Agent for one year. Structure only: "
                           "the outcome is unpublished.")]),
        office("surveyor-of-wood-bark-and-lumber",
               "Surveyor of Wood, Bark and Lumber",
               "Hardwick Surveyor of Wood, Bark and Lumber", 1,
               [hdk_report("the town's 2026 Warning elects a "
                           "Surveyor of Wood, Bark and Lumber for "
                           "one year, and the officers table seats "
                           "Levi Chase on a term that expired at "
                           "that meeting. Structure only: the "
                           "outcome is unpublished. The office is "
                           "not a 17 V.S.A. section 2646 office; "
                           "Hardwick's own warning carries it.")]),
        office("tree-warden", "Tree Warden",
               "Hardwick Tree Warden", 1,
               [charter123("section 302(a)(13) makes the tree "
                           "warden elective in Hardwick."),
                hdk_report("the officers table seats Geoffrey "
                           "Fehrs as Tree Warden on a term that "
                           "expired at the March 2026 meeting. "
                           "Structure only.")]),
        office("grand-juror", "Grand Juror",
               "Hardwick Grand Juror", 1,
               [charter123("section 302(a)(15) makes one or more "
                           "grand jurors elective."),
                hdk_report("the officers table seats Raymond "
                           "Bellavance as Town Grand Juror on a "
                           "term that expired at the March 2026 "
                           "meeting, and the warning stood one "
                           "grand juror. Structure only.")]),
        office("first-constable", "First Constable",
               "Hardwick First Constable", 1,
               [charter123("section 302(a)(11) makes a First "
                           "Constable elective."),
                hdk_report("the officers table seats Lawrence "
                           "Hamel as First Constable on a term "
                           "that expired at the March 2026 "
                           "meeting, which stood the office. "
                           "Structure only.")]),
        office("second-constable", "Second Constable",
               "Hardwick Second Constable", 1,
               [charter123("section 302(a)(11) provides for a "
                           "Second Constable if needed."),
                hdk_report("the officers table seats Lindsay "
                           "O'Steen as Second Constable on a term "
                           "that expired at the March 2026 "
                           "meeting, which stood the office. "
                           "Structure only.")]),
        office("library-trustee", "Library Trustee",
               "Hardwick Jeudevine Memorial Library Trustees", 7,
               [hdk_report("the officers table seats seven "
                           "elected trustees of the Jeudevine "
                           "Memorial Library: Lauren Honican to "
                           "2027, Abrah Griggs to 2027, Vincent "
                           "Razionale to 2028, Solomon Lew to "
                           "2028, and Mary Meyer to 2028 are "
                           "minted; the 2026 Warning stood a "
                           "three-year seat and a one-year "
                           "remainder whose outcomes are "
                           "unpublished, so two seats are "
                           "unfilled."),
                charter123("section 302(a)(9) makes library "
                           "trustees elective.")],
               [holder("Lauren Honican", "lauren-honican"),
                holder("Abrah Griggs", "abrah-griggs"),
                holder("Vincent Razionale", "vincent-razionale"),
                holder("Solomon Lew", "solomon-lew"),
                holder("Mary Meyer", "mary-meyer")]),
        office("electric-commissioner", "Electric Commissioner",
               "Hardwick Electric Commissioners", 5,
               [hdk_report("the town's officials table lists five "
                           "Hardwick Electric Commissioners -- the "
                           "elected board of the town's municipal "
                           "electric department: Renaud Demers to "
                           "2027, Michael Ambrosino to 2027, and "
                           "Jake Lester to 2027 are minted; the "
                           "two seats expiring in 2026 (Myles "
                           "Kamisher-Koch's and Roger Prevot's) "
                           "are unfilled, their outcomes "
                           "unpublished.")],
               [holder("Renaud Demers", "renaud-demers"),
                holder("Michael Ambrosino", "michael-ambrosino"),
                holder("Jake Lester", "jake-lester")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Hardwick Justices of the Peace", 10,
               [jp_src("lists ten justices of the peace for "
                       "Hardwick.")],
               [holder("Jean Hackett", "jean-hackett"),
                holder("Lenore Renaud", "lenore-renaud"),
                holder("Robin Leslie", "robin-leslie"),
                holder("Ken Leslie", "ken-leslie"),
                holder("Amy Rosenthal", "amy-rosenthal"),
                holder("Tracy Martin", "tracy-martin"),
                holder("Abrah Griggs", "abrah-griggs"),
                holder("Paul Fixx", "paul-fixx"),
                holder("Mary Whitaker", "mary-whitaker"),
                holder("Alexandra Jump", "alexandra-jump")]),
    ]
    return spec("hardwick", label, offices,
                jp_election("hardwick-vt", label, 10,
                            "the SOS listing names the ten "
                            "Hardwick winners of the November 5, "
                            "2024 justice of the peace election. "
                            "No cemetery-trustee post is created: "
                            "the town's table seats the Selectboard "
                            "itself as trustee of all seven town "
                            "cemeteries, an ex officio trusteeship. "
                            "No delinquent-tax-collector post: the "
                            "Town Manager holds the function. The "
                            "charter's fire-department officers "
                            "(section 302(a)(10)) are not modeled "
                            "pending a scope ruling."))


SPECS.append(hardwick_spec())

# -------------------------------------------------------------- Hartford
HTF_RES26 = {
    "url": "https://www.hartford-vt.org/DocumentCenter/View/13225/2026-OFFICIAL-TOWN-RESULTS",
    "note": "PLACEHOLDER",
}
HTF_RES25 = {
    "url": "https://www.hartford-vt.org/DocumentCenter/View/12114/TOWN-OFFICIAL-RESULTS-March-4-2025",
    "note": "PLACEHOLDER",
}


def htf_res26(what):
    return S(HTF_RES26, "Town of Hartford, Certificate of Results, "
             f"Annual Town Meeting, March 3, 2026 "
             f"(hartford-vt.org): {what}")


def htf_res25(what):
    return S(HTF_RES25, "Town of Hartford, Official Ballot Results, "
             f"Annual Town Meeting, March 4, 2025 "
             f"(hartford-vt.org): {what}")


def hartford_spec():
    label = "Town of Hartford"
    offices = [
        office("selectboard", "Selectboard Member",
               "Hartford Selectboard", 7,
               [sb_dir("lists Hartford's seven selectboard members "
                       "as Ashley Andreas, Miranda Dupre, Mike "
                       "Eigenbrode, Mary Erdei, Tim Fariel, Ida "
                       "Griesemer (Chair), and Erik Krauss."),
                htf_res26("the certified 2026 results re-elect "
                          "Ashley Andreas (821) and Tim Fariel "
                          "(828) to two-year seats over Janet "
                          "Sharkey Potter (638), and Mike "
                          "Eigenbrode (1,005) to a three-year "
                          "seat."),
                htf_res25("the official 2025 results elect Mary "
                          "Erdei (1,191) and Miranda Dupre (807) "
                          "and Erik Krauss (1,068)."),
                charter123a("section 202(e)(1) fixes a "
                            "seven-member elected selectboard.")],
               [holder("Ida Griesemer", "ida-griesemer"),
                holder("Erik Krauss", "erik-krauss"),
                holder("Ashley Andreas", "ashley-andreas"),
                holder("Miranda Dupre", "miranda-dupre"),
                holder("Mike Eigenbrode", "mike-eigenbrode"),
                holder("Mary Erdei", "mary-erdei"),
                holder("Tim Fariel", "tim-fariel")]),
        office("moderator", "Moderator", "Hartford Moderator", 1,
               [htf_res25("Chuck Wooster was elected Town "
                          "Moderator for three years on March 4, "
                          "2025, with 1,416 votes; the seat did not "
                          "stand in 2026."),
                charter123a("section 202(e)(2) makes one "
                            "moderator elective on a three-year "
                            "term.")],
               [holder("Chuck Wooster", "chuck-wooster")]),
        office("town-treasurer", "Town Treasurer",
               "Hartford Town Treasurer", 1,
               [htf_res26("Joe Major was re-elected Town Treasurer "
                          "for three years on March 3, 2026, with "
                          "1,189 votes."),
                guide("lists Joseph Major as Hartford town "
                      "treasurer."),
                charter123a("section 202(e)(3) makes a town "
                            "treasurer elective on a three-year "
                            "term. The holder is the sitting "
                            "Windsor-district state senator; his "
                            "existing person record is reused.")],
               [holder("Joe Major", "joe-major",
                       existing_person_id="ocd-person/f4a8369e-abe1-5e57-b20c-e647496745af")]),
        office("town-clerk", "Town Clerk", "Hartford Town Clerk",
               1,
               [charter123a("the charter provides that the Town "
                            "Clerk is appointed by and serves at "
                            "the pleasure of the Selectboard."),
                guide("lists Lisa O'Neil as Hartford town clerk."),
                htf_res26("the 2026 certificate of results is "
                          "recorded and signed by Lisa O'Neil as "
                          "Town Clerk.")],
               [holder("Lisa O'Neil", "lisa-oneil",
                       how_seated="appointed")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Hartford Justices of the Peace", 15,
               [jp_src("lists fifteen justices of the peace for "
                       "Hartford."),
                charter123a("section 202(g) fixes fifteen "
                            "justices of the peace for Hartford.")],
               [holder("Rebecca White", "rebecca-white",
                       existing_person_id="ocd-person/5a9558bd-bb54-592f-bc91-6849096172b5"),
                holder("Scott Farnsworth", "scott-farnsworth"),
                holder("Nancy Howe", "nancy-howe"),
                holder("Lynn Bohi", "lynn-bohi"),
                holder("Linda Simon Miller", "linda-simon-miller"),
                holder("Jo Alexander", "jo-alexander"),
                holder("Adam Ricker", "adam-ricker"),
                holder("Brett Mayfield", "brett-mayfield"),
                holder("Jennifer Horn", "jennifer-horn"),
                holder("Susan Kirincich", "susan-kirincich"),
                holder("Don Foster", "don-foster"),
                holder("Ryan Walther", "ryan-walther"),
                holder("Sara Blood", "sara-blood"),
                holder("Mark McNamee", "mark-mcnamee"),
                holder("Pat Cook", "pat-cook")]),
    ]
    return spec("hartford", label, offices,
                jp_election("hartford-vt", label, 15,
                            "the SOS listing names the fifteen "
                            "Hartford winners of the November 5, "
                            "2024 justice of the peace election; "
                            "the first-listed, Rebecca White, is "
                            "the sitting Windsor-district state "
                            "senator and her existing person "
                            "record is reused. No lister post: "
                            "the charter's contracted assessor "
                            "performs the listers' functions. No "
                            "delinquent-tax-collector post: the "
                            "Town Manager holds the duties (ch. "
                            "123A section 203(c)). No West Hartford "
                            "Library trustee post: its trustees "
                            "are town-elected on five-year terms "
                            "but no official source fixes the "
                            "board's size (verified elected: Karen "
                            "Powell and Mary Smith, 2025; Torrelee "
                            "F. 'Fisher-Sass' Sass, 2026)."))


SPECS.append(hartford_spec())

# -------------------------------------------------------------- Hartland
def hartland_spec():
    label = "Town of Hartland"
    offices = [
        office("selectboard", "Selectboard Member",
               "Hartland Selectboard", 5,
               [sb_dir("lists Hartland's five selectboard members "
                       "as Phil Hobbie, Clyde Jenne, Thomas "
                       "Kennedy, James Rielly, and Trace Tancreti. "
                       "Hartland's own town website was "
                       "unreachable from every path tried, so "
                       "this roster rests on the Secretary of "
                       "State's directories (the Bloomfield "
                       "posture).")],
               [holder("Phil Hobbie", "phil-hobbie"),
                holder("Clyde Jenne", "clyde-jenne"),
                holder("Thomas Kennedy", "thomas-kennedy"),
                holder("James Rielly", "james-rielly"),
                holder("Trace Tancreti", "trace-tancreti")]),
        office("moderator", "Moderator", "Hartland Moderator", 1,
               [statute2646_structure("a moderator")]),
        office("town-clerk", "Town Clerk", "Hartland Town Clerk",
               1,
               [guide("lists John Paulette as Hartland town "
                      "clerk."),
                clerk_xlsx("lists John Paulette as Hartland town "
                           "clerk.")],
               [holder("John Paulette", "john-paulette")]),
        office("town-treasurer", "Town Treasurer",
               "Hartland Town Treasurer", 1,
               [guide("lists Karen Clark as Hartland town "
                      "treasurer."),
                treas_xlsx("lists Karen Clark as Hartland town "
                           "treasurer.")],
               [holder("Karen Clark", "karen-clark")]),
        office("lister", "Lister", "Hartland Listers", 3,
               [statute2646_structure("three listers on staggered "
                                      "three-year terms")]),
        office("auditor", "Auditor", "Hartland Auditors", 3,
               [statute2646_structure("three auditors on staggered "
                                      "three-year terms")]),
        office("grand-juror", "Grand Juror",
               "Hartland Grand Juror", 1,
               [statute2646_structure("a grand juror")]),
        office("town-agent", "Town Agent", "Hartland Town Agent",
               1,
               [statute2646_structure("a town agent")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Hartland Justices of the Peace", 12,
               [jp_src("lists twelve justices of the peace for "
                       "Hartland.")],
               [holder("Barbara Barbour", "barbara-barbour"),
                holder("John Bartholomew", "john-bartholomew",
                       existing_person_id="ocd-person/f9b68094-d3f5-5f7c-b9e3-7963aa0c9b37"),
                holder("Molly Delaney", "molly-delaney"),
                holder("Bill Donahue", "bill-donahue"),
                holder("Matt Dunne", "matt-dunne"),
                holder("Clyde Jenne", "clyde-jenne"),
                holder("Thomas Kennedy", "thomas-kennedy"),
                holder("Jo Knowles", "jo-knowles"),
                holder("Bettina Read", "bettina-read"),
                holder("Patricia Richardson",
                       "patricia-richardson"),
                holder("Brian Stroffolino", "brian-stroffolino"),
                holder("Andrea Farrington", "andrea-farrington")]),
    ]
    return spec("hartland", label, offices,
                jp_election("hartland-vt", label, 12,
                            "the SOS listing names the twelve "
                            "Hartland winners of the November 5, "
                            "2024 justice of the peace election; "
                            "John Bartholomew is the sitting "
                            "Windsor-1 state representative -- his "
                            "legislature biography lists his "
                            "Hartland justice of the peace seat -- "
                            "and his existing person record is "
                            "reused. No constable post is created "
                            "(the seat count is a per-town vote, "
                            "unverifiable here) and no delinquent-"
                            "tax-collector post (the treasurer "
                            "holds the function by default)."))


SPECS.append(hartland_spec())

# ---------------------------------------------------------------- run
for s in SPECS:
    p = OUT / f"{s['place_slug']}.json"
    p.write_text(json.dumps(s, indent=1))
    n_off = len(s["offices"])
    n_hold = sum(len(o.get("holders", ())) for o in s["offices"])
    print(f"{s['place_slug']}: {n_off} offices, {n_hold} holders")
print(f"wrote {len(SPECS)} specs")
