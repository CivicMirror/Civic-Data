#!/usr/bin/env python3
"""Batch 11 of the VT #163 municipal fan-out (alphabetical positions
100-109): Highgate, Hinesburg, Holland, Hubbardton, Huntington,
Hyde Park (town), Hyde Park (village), Ira, Irasburg, Isle La
Motte. Emits one JSON spec per municipality for
build_vt_municipality.py.
Research: vt_muni_batch11_research.md.

Identity calls baked into this batch (all flagged on #163):
- Highgate's Selectboard is minted from the town's own live
  page: the June 2026 SOS directory is stale for Highgate (it
  seats Flint as Chair and Brosky, both gone; the town page
  seats Souza as Chair with Rainville and Chevalier, and
  Carr's 2029 expiry proves the page is post-March-2026).
- Hinesburg's Heather Roberts (clerk/treasurer/library/Peck)
  is a NEW person: the existing heather-roberts record is
  Charlotte's JP, a different person (JP residency is
  town-bound); the builder's collision suffix keeps them apart.
- Huntington JP Beverly Little Thunder was elected in Nov
  2024 but has died; Barrett Grimm was appointed by the
  Governor in April 2026 on the BCA's recommendation. The
  election record carries the six living winners (vote_for 7)
  with the story in its note; Grimm's membership is
  how_seated "appointed" with holder flag no_candidacy (the
  builder was patched this batch to honor it).
- Isle La Motte's town officers table seats FIVE JPs
  (incl. Karen Brunner) where the SOS listing names four;
  Brunner is minted as the fifth winner (the Bolton
  treatment) with the discrepancy in the election note.
- Hyde Park village's Bliss trustee Edward French is the
  town's cemetery commissioner/JP -- one person record
  scoped to the town (person_scope), the village built after
  the town in the same run.
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
CHARTER_225 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/225",
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


def charter225(phrase):
    return S(CHARTER_225, "Charter of the Village of Hyde Park, "
             f"24 App. V.S.A. ch. 225 (official text, Vermont "
             f"General Assembly): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 11); issue #163 "
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
                  f"# municipal fan-out batch 11; issue #163 "
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

# ------------------------------------------------------------ Highgate
HG_PAGE = {
    "url": "https://www.highgatevt.org/board-members",
    "note": "PLACEHOLDER",
}
HG_REPORT = {
    "url": "https://www.highgatevt.org/vertical/sites/%7B27DD8364-9602-460E-9A11-4C6436D74153%7D/uploads/2025_HIGHGATE_TOWN_REPORT.pdf",
    "note": "PLACEHOLDER",
}


def hg_page(what):
    return S(HG_PAGE, f"Town of Highgate (official website, "
             f"Selectboard page): {what}")


def hg_report(what):
    return S(HG_REPORT, f"Town of Highgate, 2025 Annual Report "
             f"(official town website): {what}")


def highgate_spec():
    sb = [
        hg_page("the town's Selectboard page seats Merry Souza "
                "(Chair, term expires March 2027), Henry Rainville "
                "(2027), Claude Chevalier (2027), Christopher LaPan "
                "(Vice-Chair, 2028), and Chad Carr (2029). Carr's "
                "2029 expiry proves the page postdates the March "
                "2026 meeting (his seat stood and he was re-elected "
                "to a three-year term)"),
        hg_report("the pre-meeting officers table seats Souza as "
                  "Chair with Vern Brosky III as Vice-Chair, "
                  "Richard Flint, Carr (term expired March 2026), "
                  "and a fifth seat vacant (to 2028)"),
        sb_dir("the directory seats Carr, Lapan, and Souza but "
               "also Richard Flint as Chair and Vern Brosky III, "
               "both absent from the town's current page -- the "
               "directory is stale for Highgate and the town's "
               "own page governs"),
    ]
    offices = [
        office("selectboard", "Selectboard Member",
               "Highgate Selectboard", 5, sb, [
                   holder("Merry Souza", "merry-souza"),
                   holder("Henry Rainville", "henry-rainville"),
                   holder("Claude Chevalier", "claude-chevalier"),
                   holder("Christopher LaPan", "christopher-lapan"),
                   holder("Chad Carr", "chad-carr"),
               ]),
        office("town-clerk", "Town Clerk", "Highgate Town Clerk", 1,
               [hg_report("the town officers table prints Town "
                          "Clerk Wendi Dusablon's term expiring "
                          "March 2026"),
                statute2646_structure("a town clerk"),
                guide("Highgate Town Clerk is Wendi Dusablon; her "
                      "printed term expired in March 2026 and no "
                      "official source publishes the outcome of "
                      "the 2026 clerk election, so the seat is "
                      "left unfilled rather than guessed")]),
        office("town-treasurer", "Town Treasurer",
               "Highgate Town Treasurer", 1,
               [hg_report("the town officers table prints Town "
                          "Treasurer Shelley Laroche's term "
                          "running to March 2028"),
                guide("Highgate Treasurer is Shelley Laroche"),
                treas_xlsx("Highgate Treasurer is Shelley "
                           "Laroche")],
               [holder("Shelley Laroche", "shelley-laroche")]),
        office("moderator", "Town Moderator", "Highgate Moderator",
               1,
               [hg_report("the town officers table prints Town "
                          "Moderator Phillip Ladue's term "
                          "expiring March 2026"),
                statute2646_structure("a moderator")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Highgate Cemetery Commission", 5,
               [hg_report("the town officers table lists five "
                          "elected Cemetery Commissioners: Kevin "
                          "Spears (Chair, term expired March "
                          "2026), Benjamin Nye (2027), Douglas "
                          "Nye (2028), Keith Ploof (2029), and "
                          "Dennis Nolan (2030). Spears's seat "
                          "stood in 2026 with no published "
                          "outcome and is left unfilled")],
               [holder("Benjamin Nye", "benjamin-nye"),
                holder("Douglas Nye", "douglas-nye"),
                holder("Keith Ploof", "keith-ploof"),
                holder("Dennis Nolan", "dennis-nolan")]),
        office("library-trustee", "Library Trustee",
               "Highgate Library Trustees", 5,
               [hg_report("the town officers table lists five "
                          "elected Library Trustees: Rebecca "
                          "Manning (Chair, term expired March "
                          "2026), Amber Machia (2027), Virginia "
                          "Holiman (2028), Chelsea Pigeon (2029), "
                          "and one seat already vacant (to 2030). "
                          "The two open seats are left unfilled")],
               [holder("Amber Machia", "amber-machia"),
                holder("Virginia Holiman", "virginia-holiman"),
                holder("Chelsea Pigeon", "chelsea-pigeon")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Highgate Collector of Delinquent Taxes", 1,
               [hg_report("the town officers table classes the "
                          "Delinquent Tax Collector among the "
                          "town's appointed miscellaneous "
                          "officials (Shelley Laroche, "
                          "appointment term expired March 2026). "
                          "Structure only: the office is filled "
                          "by appointment and no current appointee "
                          "is published")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Highgate Justices of the Peace", 6,
               [jp_src("the listing names six justices of the "
                       "peace for Highgate")],
               [holder("Claude Chevalier", "claude-chevalier"),
                holder("Donna Chevalier", "donna-chevalier"),
                holder("John Ferland", "john-ferland"),
                holder("Bruce Gagne", "bruce-gagne"),
                holder("Patty Rainville", "patty-rainville"),
                holder("Dennis Nolan", "dennis-nolan")]),
    ]
    jp = jp_election(
        "highgate-vt", "Highgate", 6,
        "the winners were Claude Chevalier, Donna Chevalier, "
        "John Ferland, Bruce Gagne, Patty Rainville, and Dennis "
        "Nolan (six seats). The town's 2025 Annual Report JP "
        "block concurs, printing terms expiring January 2027",
        [hg_report("the report's Justices of the Peace block "
                   "names the same six")])
    return spec("highgate", "Highgate", offices, jp)


SPECS.append(highgate_spec())

# ------------------------------------------------------------ Hinesburg
HIN_RESULTS = {
    "url": "https://hinesburg.org/DocumentCenter/View/3676/Annual-Town-and-School-District-Meeting-Results-03-03-26",
    "note": "PLACEHOLDER",
}
HIN_REPORT = {
    "url": "https://hinesburg.org/DocumentCenter/View/3679/Hinesburg-Annual-Report-FY2025",
    "note": "PLACEHOLDER",
}


def hin_results(what):
    return S(HIN_RESULTS, "Town of Hinesburg, official marked "
             "ballot results, Annual Town and School District "
             f"Meeting, March 3, 2026: {what}")


def hin_report(what):
    return S(HIN_REPORT, f"Town of Hinesburg, FY2025 Annual "
             f"Report, 'Elected Officials' table: {what}")


def hinesburg_spec():
    sb = [
        hin_results("Merrily Lovell (835 votes) was re-elected "
                    "to a three-year Selectboard seat and Paul "
                    "Lamberson (824) to a two-year seat"),
        hin_report("the Selectboard table seats Maggie Gordon "
                   "(2027), Paul Lamberson, Michael Loner "
                   "(2028), Merrily Lovell (Chair), and Dennis "
                   "Place (2027)"),
        sb_dir("the directory seats Gordon (Vice-Chair), "
               "Lamberson, Loner, Lovell (Chair), and Place"),
    ]
    rob = [
        hin_report("the Elected Officials table prints Heather "
                   "J Roberts as Clerk & Treasurer (three-year "
                   "term)"),
        guide("Hinesburg Town Clerk and Treasurer are both "
              "Heather Roberts"),
        clerk_xlsx("Hinesburg Town Clerk is Heather Roberts"),
        treas_xlsx("Hinesburg Treasurer is Heather Roberts"),
    ]
    offices = [
        office("selectboard", "Selectboard Member",
               "Hinesburg Selectboard", 5, sb, [
                   holder("Merrily Lovell", "merrily-lovell"),
                   holder("Paul Lamberson", "paul-lamberson"),
                   holder("Maggie Gordon", "maggie-gordon"),
                   holder("Mike Loner", "mike-loner"),
                   holder("Dennis Place", "dennis-place"),
               ]),
        office("town-clerk", "Town Clerk", "Hinesburg Town Clerk",
               1,
               [hin_results("Heather J Roberts was re-elected "
                            "Town Clerk on March 3, 2026 with "
                            "951 votes (three-year term)")] + rob,
               [holder("Heather Roberts", "heather-roberts")]),
        office("town-treasurer", "Town Treasurer",
               "Hinesburg Town Treasurer", 1,
               [hin_results("Heather Roberts was re-elected "
                            "Town Treasurer on March 3, 2026 "
                            "with 906 votes (three-year term)")]
               + rob,
               [holder("Heather Roberts", "heather-roberts")]),
        office("moderator", "Town Moderator",
               "Hinesburg Moderator", 1,
               [hin_results("Frank Twarog was re-elected Town "
                            "Moderator on March 3, 2026 with "
                            "896 votes (one-year term)"),
                hin_report("the table prints Frank Twarog as "
                           "Town Moderator")],
               [holder("Frank Twarog", "frank-twarog")]),
        office("cemetery-trustee", "Cemetery Trustee",
               "Hinesburg Cemetery Trustees", 3,
               [hin_results("Glenn Place was re-elected Cemetery "
                            "Trustee on March 3, 2026 with 883 "
                            "votes (three-year term)"),
                hin_report("the table lists three Cemetery "
                           "Trustees on staggered three-year "
                           "terms: Mary Jo Brace (2027), Tom "
                           "Giroux (2028), and Glenn Place")],
               [holder("Glenn Place", "glenn-place"),
                holder("Mary Jo Brace", "mary-jo-brace"),
                holder("Tom Giroux", "tom-giroux")]),
        office("library-trustee", "Library Trustee",
               "Hinesburg Library Trustees", 9,
               [hin_results("Catherine Moller (827 votes) and "
                            "Kathleen Rivard (808) were elected "
                            "Library Trustees on March 3, 2026 in "
                            "a vote-for-three contest for "
                            "three-year terms; a separate one-year "
                            "remainder seat drew no ballot "
                            "candidate"),
                hin_report("the table lists Library Trustees "
                           "Aimee Frost (2027) and Heather "
                           "Roberts (2027); Victoria Burns, "
                           "Paula Haskell, and Katie Bailey "
                           "Martin (2028); and Katherine "
                           "Kjelleren (Chair), Catherine Moller, "
                           "and Kathleen Rivard on the class "
                           "expiring 2026. The board sits in "
                           "three classes of three on three-year "
                           "terms (nine seats); Kjelleren did "
                           "not stand in 2026 and her seat and "
                           "the remainder seat are left "
                           "unfilled (write-in outcomes "
                           "unpublished)")],
               [holder("Catherine Moller", "catherine-moller"),
                holder("Kathleen Rivard", "kathleen-rivard"),
                holder("Aimee Frost", "aimee-frost"),
                holder("Heather Roberts", "heather-roberts"),
                holder("Victoria Burns", "victoria-burns"),
                holder("Paula Haskell", "paula-haskell"),
                holder("Katie Bailey Martin",
                       "katie-bailey-martin")]),
        office("peck-estate-trustee", "Peck Estate Trustee",
               "Hinesburg Peck Estate Trustees", 3,
               [hin_results("Jenny Wilkinson was elected Peck "
                            "Estate Trustee on March 3, 2026 "
                            "with 845 votes (three-year term)"),
                hin_report("the table lists three Peck Estate "
                           "Trustees: Heather Roberts (2028), "
                           "Frank Twarog (2027), and Jennifer "
                           "Wilkinson")],
               [holder("Jennifer Wilkinson", "jennifer-wilkinson",
                       ballot_name="Jenny Wilkinson"),
                holder("Frank Twarog", "frank-twarog"),
                holder("Heather Roberts", "heather-roberts")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Hinesburg Justices of the Peace", 12,
               [jp_src("the listing names twelve justices of "
                       "the peace for Hinesburg")],
               [holder("Lanny Dennison", "lanny-dennison"),
                holder("Sheila Dodd", "sheila-dodd"),
                holder("Kitty Frazier", "kitty-frazier"),
                holder("Lynn E Gardner", "lynn-e-gardner"),
                holder("Marie A Gardner", "marie-a-gardner"),
                holder("Tom Giroux", "tom-giroux"),
                holder("Andy Johnstone", "andy-johnstone"),
                holder("Katherine Levasseur",
                       "katherine-levasseur"),
                holder("Bill Lippert", "bill-lippert"),
                holder("Enrique Peredo", "enrique-peredo"),
                holder("Missy Ross", "missy-ross"),
                holder("Sarah Toscano", "sarah-toscano")]),
    ]
    jp = jp_election(
        "hinesburg-vt", "Hinesburg", 12,
        "the winners were Lanny Dennison, Sheila Dodd, Kitty "
        "Frazier, Lynn E Gardner, Marie A Gardner, Tom Giroux, "
        "Andy Johnstone, Katherine Levasseur, Bill Lippert, "
        "Enrique Peredo, Missy Ross, and Sarah Toscano (twelve "
        "seats). The FY2025 Annual Report's JP table omits "
        "Dennison; the certified listing governs",
        [hin_report("the report's Justice of the Peace table "
                    "names eleven of the twelve")])
    return spec("hinesburg", "Hinesburg", offices, jp)


SPECS.append(hinesburg_spec())

# ------------------------------------------------------------ Holland
HOL_REPORT = {
    "url": "https://hollandvt.gov/assets/documents/HOLLAND_AnnualReport_25.F.pdf",
    "note": "PLACEHOLDER",
}


def hol_report(what):
    return S(HOL_REPORT, f"Town of Holland, 2025 Annual Report "
             f"(official town website): {what}")


def holland_spec():
    tbl = hol_report("the report's Town Officers table prints "
                     "the office, its term, the holder, and the "
                     "term's expiry")
    offices = [
        office("selectboard", "Selectboard Member",
               "Holland Selectboard", 3,
               [tbl,
                sb_dir("the directory seats Dave Jacobs, Hugh "
                       "Flynn, and Trevor Gray (Chair) after the "
                       "March 2026 meeting; the report table "
                       "seats the same three (Flynn's term "
                       "printed expiring 2026)")],
               [holder("Hugh Flynn", "hugh-flynn"),
                holder("Dave Jacobs", "dave-jacobs"),
                holder("Trevor Gray", "trevor-gray")]),
        office("town-clerk", "Town Clerk", "Holland Town Clerk",
               1,
               [tbl, guide("Holland Town Clerk is Diane Judd"),
                clerk_xlsx("Holland Town Clerk is Diane Judd")],
               [holder("Diane Judd", "diane-judd")]),
        office("town-treasurer", "Town Treasurer",
               "Holland Town Treasurer", 1,
               [tbl, guide("Holland Treasurer is Diane Judd"),
                treas_xlsx("Holland Treasurer is Diane Judd")],
               [holder("Diane Judd", "diane-judd")]),
        office("lister", "Lister", "Holland Board of Listers", 3,
               [hol_report("the Town Officers table lists three "
                           "Listers: Heather Dowland (term "
                           "expired 2026), Gaetane Patenaude "
                           "(2027), and Diane Judd (2028). "
                           "Dowland's seat stood at the March "
                           "2026 floor meeting with no published "
                           "outcome and is left unfilled")],
               [holder("Gaetane Patenaude", "gaetane-patenaude"),
                holder("Diane Judd", "diane-judd")]),
        office("auditor", "Town Auditor", "Holland Town Auditors",
               3,
               [hol_report("the Town Officers table lists three "
                           "Auditors: Heather Dowland (term "
                           "expired 2026), Gaetane Patenaude "
                           "(2027), and Suzanne Moulton (2028). "
                           "Dowland's seat is left unfilled")],
               [holder("Gaetane Patenaude", "gaetane-patenaude"),
                holder("Suzanne Moulton", "suzanne-moulton")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Holland Cemetery Commission", 5,
               [hol_report("the Town Officers table lists five "
                           "Cemetery Commissioners on five-year "
                           "terms: Diana Emmerson (term expired "
                           "2026), Helen Flynn (2027), Kenric "
                           "Gonyaw (2028), Heather Dowland "
                           "(2029), and Laurie Gray (2030). "
                           "Emmerson's seat is left unfilled")],
               [holder("Helen Flynn", "helen-flynn"),
                holder("Kenric Gonyaw", "kenric-gonyaw"),
                holder("Heather Dowland", "heather-dowland"),
                holder("Laurie Gray", "laurie-gray")]),
        office("constable", "Constable", "Holland Constable", 1,
               [hol_report("the Town Officers table lists one "
                           "Constable (one-year term): Greg "
                           "Bronson, marked '(resigned)', term "
                           "2026. Structure only: no successor "
                           "is published")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Holland Collector of Delinquent Taxes", 1,
               [hol_report("the Town Officers table lists the "
                           "Delinquent Tax Collector as a "
                           "separately elected one-year office "
                           "(Diane Judd, term expired 2026). "
                           "The 2026 outcome is unpublished, so "
                           "the seat is left unfilled")]),
        office("moderator", "Town Moderator", "Holland Moderator",
               1,
               [hol_report("the Town Officers table prints Town "
                           "Moderator Michael (Mitch) Wonson "
                           "(one-year term expiring 2026) and "
                           "the 2026 warning's Article 1 elects "
                           "a Moderator at the floor meeting"),
                statute2646_structure("a moderator")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Holland Justices of the Peace", 5,
               [jp_src("the listing names five justices of the "
                       "peace for Holland")],
               [holder("Diane Judd", "diane-judd"),
                holder("Brian Currier", "brian-currier"),
                holder("Thomas Adams", "thomas-adams"),
                holder("Kenric Gonyaw", "kenric-gonyaw"),
                holder("Lucy Neel", "lucy-neel")]),
    ]
    jp = jp_election(
        "holland-vt", "Holland", 5,
        "the winners were Diane Judd, Brian Currier, Thomas "
        "Adams, Kenric Gonyaw, and Lucy Neel (five seats). "
        "The town report's JP block concurs",
        [tbl])
    return spec("holland", "Holland", offices, jp)


SPECS.append(holland_spec())

# ------------------------------------------------------------ Hubbardton
def hubbardton_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Hubbardton Selectboard", 5,
               [sb_dir("the directory seats James Casey, Dwayne "
                       "Gibbs, Robert Gibbs (Chairman), Richard "
                       "Grabowski, and Michael Wetmore. "
                       "Hubbardton has no reachable official "
                       "town website; this is a spine build")],
               [holder("James Casey", "james-casey"),
                holder("Dwayne Gibbs", "dwayne-gibbs"),
                holder("Robert Gibbs", "robert-gibbs"),
                holder("Richard Grabowski", "richard-grabowski"),
                holder("Michael Wetmore", "michael-wetmore")]),
        office("town-clerk", "Town Clerk",
               "Hubbardton Town Clerk", 1,
               [guide("Hubbardton Town Clerk is Kathleen Hewes"),
                clerk_xlsx("Hubbardton Town Clerk is Kathleen "
                           "Hewes")],
               [holder("Kathleen Hewes", "kathleen-hewes")]),
        office("town-treasurer", "Town Treasurer",
               "Hubbardton Town Treasurer", 1,
               [guide("Hubbardton Treasurer is Kathleen Hewes"),
                treas_xlsx("Hubbardton Treasurer is Kathleen "
                           "Hewes")],
               [holder("Kathleen Hewes", "kathleen-hewes")]),
        office("moderator", "Town Moderator",
               "Hubbardton Moderator", 1,
               [statute2646_structure("a moderator")]),
        office("lister", "Lister", "Hubbardton Board of Listers",
               3, [statute2646_structure("three listers")]),
        office("auditor", "Town Auditor",
               "Hubbardton Town Auditors", 3,
               [statute2646_structure("three auditors")]),
        office("grand-juror", "Grand Juror",
               "Hubbardton Grand Juror", 1,
               [statute2646_structure("a grand juror")]),
        office("town-agent", "Town Agent", "Hubbardton Town Agent",
               1, [statute2646_structure("a town agent")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Hubbardton Justices of the Peace", 5,
               [jp_src("the listing names five justices of the "
                       "peace for Hubbardton")],
               [holder("George W Davis Jr", "george-w-davis-jr"),
                holder("Jacquelyn Frost", "jacquelyn-frost"),
                holder("Raymond McLaughlin",
                       "raymond-mclaughlin"),
                holder("Elaine Nordmeyer", "elaine-nordmeyer"),
                holder("Michael Wetmore", "michael-wetmore")]),
    ]
    jp = jp_election(
        "hubbardton-vt", "Hubbardton", 5,
        "the winners were George W Davis Jr, Jacquelyn Frost, "
        "Raymond McLaughlin, Elaine Nordmeyer, and Michael "
        "Wetmore (five seats)")
    return spec("hubbardton", "Hubbardton", offices, jp)


SPECS.append(hubbardton_spec())

# ------------------------------------------------------------ Huntington
HUN_SB = {
    "url": "https://www.huntingtonvt.org/selectboard/",
    "note": "PLACEHOLDER",
}
HUN_AUD = {
    "url": "https://www.huntingtonvt.org/board-of-auditors/",
    "note": "PLACEHOLDER",
}
HUN_LIS = {
    "url": "https://www.huntingtonvt.org/board-of-listers/",
    "note": "PLACEHOLDER",
}
HUN_CLERK = {
    "url": "https://www.huntingtonvt.org/town-clerk/",
    "note": "PLACEHOLDER",
}
HUN_TREAS = {
    "url": "https://www.huntingtonvt.org/town-treasurer/",
    "note": "PLACEHOLDER",
}
HUN_HOME = {
    "url": "https://www.huntingtonvt.org/",
    "note": "PLACEHOLDER",
}


def huntington_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Huntington Selectboard", 5,
               [S(HUN_SB, "Town of Huntington (official website), "
                          "Selectboard page: Dori Barton (Chair, "
                          "term expires 2027), Landel Cochran "
                          "(Vice Chair, 2027), Troy Liberty "
                          "(2029), Roman Livak (2028), and Karen "
                          "Barber (2028). The page postdates the "
                          "March 2026 meeting (Liberty's 2029 "
                          "term)"),
                sb_dir("the directory seats the same five")],
               [holder("Dori Barton", "dori-barton"),
                holder("Landel Cochran", "landel-cochran"),
                holder("Troy Liberty", "troy-liberty"),
                holder("Roman Livak", "roman-livak"),
                holder("Karen Barber", "karen-barber")]),
        office("town-clerk", "Town Clerk",
               "Huntington Town Clerk", 1,
               [S(HUN_CLERK, "Town of Huntington (official "
                             "website), Town Clerk page: the "
                             "Town Clerk is Heidi Racht, elected "
                             "to a three-year term expiring "
                             "2027"),
                guide("Huntington Town Clerk is Heidi Racht"),
                clerk_xlsx("Huntington Town Clerk is Heidi "
                           "Racht")],
               [holder("Heidi Racht", "heidi-racht")]),
        office("town-treasurer", "Town Treasurer",
               "Huntington Town Treasurer", 1,
               [S(HUN_TREAS, "Town of Huntington (official "
                             "website), Town Treasurer page: "
                             "the Town Treasurer is Andrea "
                             "Ogilvie, who also serves as the "
                             "town's tax collector (no separate "
                             "Collector of Delinquent Taxes "
                             "post)"),
                guide("Huntington Treasurer is Andrea Ogilvie"),
                treas_xlsx("Huntington Treasurer is Andrea "
                           "Ogilvie")],
               [holder("Andrea Ogilvie", "andrea-ogilvie")]),
        office("auditor", "Town Auditor",
               "Huntington Town Auditors", 3,
               [S(HUN_AUD, "Town of Huntington (official "
                           "website), Board of Auditors page: "
                           "Dan Towle (term expires 2027), "
                           "Patricia Quinn Baumann (Chair), and "
                           "Marilyn Hinsdale (2028). Baumann's "
                           "printed term expired in 2026; the "
                           "town's maintained page -- on the "
                           "same site whose Selectboard page is "
                           "post-meeting current -- continues to "
                           "seat her as Chair, so she is minted "
                           "as re-elected with the stale expiry "
                           "field disclosed")],
               [holder("Dan Towle", "dan-towle"),
                holder("Patricia Quinn Baumann",
                       "patricia-quinn-baumann"),
                holder("Marilyn Hinsdale", "marilyn-hinsdale")]),
        office("lister", "Lister", "Huntington Board of Listers",
               3,
               [S(HUN_LIS, "Town of Huntington (official "
                           "website), Board of Listers page: "
                           "the town has elected listers; the "
                           "page seats Diane Coles (three-year "
                           "term, 2028) and Elizabeth Cote "
                           "(2029). The third seat is absent "
                           "from the page and is left unfilled")],
               [holder("Diane Coles", "diane-coles"),
                holder("Elizabeth Cote", "elizabeth-cote")]),
        office("moderator", "Town Moderator",
               "Huntington Moderator", 1,
               [statute2646_structure("a moderator")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Huntington Justices of the Peace", 7,
               [jp_src("the listing names seven justices of "
                       "the peace for Huntington"),
                S(HUN_HOME, "Town of Huntington (official "
                            "website), homepage post: Justice "
                            "of the Peace Beverly Little "
                            "Thunder died in office; the Board "
                            "of Civil Authority recommended "
                            "Barrett Grimm and the Governor "
                            "appointed him in mid-April 2026 "
                            "to fill the vacancy. Huntington "
                            "has seven JPs")],
               [holder("Heidi Racht", "heidi-racht"),
                holder("Mary Taft", "mary-taft"),
                holder("Don Dresser", "don-dresser"),
                holder("Patricia Quinn Baumann",
                       "patricia-quinn-baumann"),
                holder("Shelley McSweeney", "shelley-mcsweeney"),
                holder("Pam Alexander", "pam-alexander"),
                holder("Barrett Grimm", "barrett-grimm",
                       how_seated="appointed", no_candidacy=True,
                       sources=[S(HUN_HOME,
                                  "Town of Huntington (official "
                                  "website), homepage post: "
                                  "after JP Beverly Little "
                                  "Thunder's death, the Board "
                                  "of Civil Authority sent "
                                  "Barrett Grimm's name to the "
                                  "Governor, who appointed him "
                                  "in mid-April 2026 to fill "
                                  "the JP vacancy")])]),
    ]
    jp = jp_election(
        "huntington-vt", "Huntington", 7,
        "the winners were Heidi Racht, Mary Taft, Don Dresser, "
        "Patricia Quinn Baumann, Shelley McSweeney, Beverly "
        "Little Thunder, and Pam Alexander (seven seats). "
        "Little Thunder died in office in 2025-26 and is not "
        "minted as a current holder; the Governor appointed "
        "Barrett Grimm in mid-April 2026 to fill her seat "
        "(see the membership record), so the winners array "
        "carries the six living elected justices",
        [S(HUN_HOME, "the town's homepage post records Little "
                     "Thunder's death and Grimm's "
                     "gubernatorial appointment")])
    return spec("huntington", "Huntington", offices, jp)


SPECS.append(huntington_spec())

# ------------------------------------------------------------ Hyde Park town
HP_SB = {
    "url": "https://hydeparkvt.com/boardscommissions/selectboard/index.php",
    "note": "PLACEHOLDER",
}
HP_CLERK = {
    "url": "https://hydeparkvt.com/department/town_clerk/index.php",
    "note": "PLACEHOLDER",
}
HP_CEM = {
    "url": "https://hydeparkvt.com/boardscommissions/cemeteries/index.php",
    "note": "PLACEHOLDER",
}
HP_NEWS = {
    "url": "https://webgen1files1.revize.com/hydeparkvt/Documents/Community/Newsletters/Newsletter 20251011 Final.pdf",
    "note": "PLACEHOLDER",
}


def hyde_park_town_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Hyde Park Selectboard", 5,
               [S(HP_SB, "Town of Hyde Park (official website), "
                         "Selectboard page: Chasity Fagnant "
                         "(three-year term, expires 2027), "
                         "Savannah Droney (2029), Matt Morin "
                         "(2027), Russell Jones (2028), and "
                         "Lance Van Vogelpoel (2028)"),
                sb_dir("the directory seats the same five "
                       "(Fagnant as Chair, Droney as "
                       "Vice-Chair)")],
               [holder("Chasity Fagnant", "chasity-fagnant"),
                holder("Savannah Droney", "savannah-droney"),
                holder("Matt Morin", "matt-morin"),
                holder("Russell Jones", "russell-jones"),
                holder("Lance Van Vogelpoel",
                       "lance-van-vogelpoel")]),
        office("town-clerk", "Town Clerk", "Hyde Park Town Clerk",
               1,
               [S(HP_CLERK, "Town of Hyde Park (official "
                            "website), Town Clerk page: "
                            "'Elected Town Clerk: Kimberly J. "
                            "Moulton, Term Expires March "
                            "2028'"),
                guide("Hyde Park Town Clerk is Kimberly "
                      "Moulton"),
                clerk_xlsx("Hyde Park Town Clerk is Kimberly "
                           "Moulton")],
               [holder("Kimberly Moulton", "kimberly-moulton")]),
        office("town-treasurer", "Town Treasurer",
               "Hyde Park Town Treasurer", 1,
               [S(HP_NEWS, "Town of Hyde Park, official monthly "
                           "newsletter (October-November "
                           "2025): 'Town Clerk, Town Treasurer, "
                           "and Delinquent Tax Collector: "
                           "Kimberly Moulton' -- the clerk also "
                           "serves as treasurer and, under the "
                           "17 V.S.A. section 2651d default, as "
                           "delinquent tax collector, so no "
                           "separate DTC post is created"),
                guide("Hyde Park Treasurer is Kimberly "
                      "Moulton"),
                treas_xlsx("Hyde Park Treasurer is Kimberly "
                           "Moulton")],
               [holder("Kimberly Moulton", "kimberly-moulton")]),
        office("lister", "Lister", "Hyde Park Board of Listers",
               3,
               [S(HP_NEWS, "Town of Hyde Park, official monthly "
                           "newsletter (October-November "
                           "2025), 'Town Board of Listers: "
                           "Deanna Judkins, Chair; Leslie "
                           "Rollins, Vice-Chair; Krista Jones'. "
                           "The Listers' February 5, 2026 "
                           "meeting agenda names the same "
                           "three")],
               [holder("Deanna Judkins", "deanna-judkins"),
                holder("Leslie Rollins", "leslie-rollins"),
                holder("Krista Jones", "krista-jones")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Hyde Park Cemetery Commission", 5,
               [S(HP_CEM, "Town of Hyde Park (official "
                          "website), Cemeteries page (updated "
                          "September 25, 2026): 'five elected "
                          "Cemetery Commissioners' -- Christine "
                          "Cooney (term expires 2028), Kim "
                          "Lambert (2029), Edward French "
                          "(2030), Kylah Jones (2031), and "
                          "Sarrah Patch (2027)")],
               [holder("Christine Cooney", "christine-cooney"),
                holder("Kim Lambert", "kim-lambert"),
                holder("Edward French", "edward-french"),
                holder("Kylah Jones", "kylah-jones"),
                holder("Sarrah Patch", "sarrah-patch")]),
        office("moderator", "Town Moderator", "Hyde Park Moderator",
               1, [statute2646_structure("a moderator")]),
        office("auditor", "Town Auditor", "Hyde Park Town Auditors",
               3, [statute2646_structure("three auditors")]),
        office("grand-juror", "Grand Juror",
               "Hyde Park Grand Juror", 1,
               [statute2646_structure("a grand juror")]),
        office("town-agent", "Town Agent", "Hyde Park Town Agent",
               1, [statute2646_structure("a town agent")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Hyde Park Justices of the Peace", 10,
               [jp_src("the listing names ten justices of the "
                       "peace for Hyde Park")],
               [holder("Vicki Emerson", "vicki-emerson"),
                holder("Richard Bailey", "richard-bailey"),
                holder("Pixie Loomis", "pixie-loomis"),
                holder("Charles Brickett Bailey",
                       "charles-brickett-bailey"),
                holder("Virginia Wiffy Brooks",
                       "virginia-wiffy-brooks"),
                holder("Malcolm Mac Teale", "malcolm-mac-teale"),
                holder("Edward French", "edward-french",
                       ballot_name="Edward Ed B French"),
                holder("Brian Jones", "brian-jones"),
                holder("Greg Paus", "greg-paus"),
                holder("Maxine Adams", "maxine-adams")]),
    ]
    jp = jp_election(
        "hyde-park-35050-vt", "Hyde Park", 10,
        "the winners were Vicki Emerson, Richard Bailey, "
        "Pixie Loomis, Charles Brickett Bailey, Virginia "
        "Wiffy Brooks, Malcolm Mac Teale, Edward Ed B French, "
        "Brian Jones, Greg Paus, and Maxine Adams (ten seats)")
    return spec("hyde-park-35050", "Hyde Park", offices, jp)


SPECS.append(hyde_park_town_spec())

# ------------------------------------------------------------ Hyde Park village
HPV_MEETING = {
    "url": "https://www.villageofhydepark.com/_files/ugd/e53882_0f1c6ee71f104474a23fbd9ea01e5ebe.pdf",
    "note": "PLACEHOLDER",
}
HPV_MINUTES = {
    "url": "https://www.villageofhydepark.com/_files/ugd/e53882_3490f56713384566b244e178d887018d.pdf",
    "note": "PLACEHOLDER",
}
HPV_MINUTES_OCT = {
    "url": "https://www.villageofhydepark.com/_files/ugd/e53882_9750eef6702542d79c99f5637c765367.pdf",
    "note": "PLACEHOLDER",
}


def hyde_park_village_spec():
    trustee_srcs = [
        charter225("section 51(a)(1) and section 52: five "
                   "trustees are elected (three for three-year "
                   "terms, two for two-year terms)"),
        S(HPV_MEETING, "Village of Hyde Park, 'A Summary of "
                       "the May 5, 2026 Annual Village "
                       "Meeting': Peter Gallo was elected "
                       "Trustee for three years (ending 2029) "
                       "and David Whitesell for the remaining "
                       "one year of a three-year term (ending "
                       "2027); Article 4 elected a trustee for "
                       "two years ending 2028 whose name the "
                       "summary leaves blank"),
        S(HPV_MINUTES, "Village of Hyde Park, Board of "
                       "Trustees minutes, May 7, 2026: the "
                       "sitting trustees are Frederika French, "
                       "Peter Gallo, Susan Trainor, and David "
                       "Whitesell; Trainor was chosen Chair "
                       "and Gallo Clerk of the Board"),
        S(HPV_MINUTES_OCT, "Village of Hyde Park, Board of "
                            "Trustees minutes, October 1, "
                            "2026: the same four trustees sit "
                            "(Trainor, Chair). The fifth "
                            "charter seat is unfilled"),
    ]
    offices = [
        office("village-trustee", "Village Trustee",
               "Hyde Park Board of Trustees", 5, trustee_srcs, [
                   holder("Frederika French", "frederika-french"),
                   holder("Peter Gallo", "peter-gallo"),
                   holder("Susan Trainor", "susan-trainor"),
                   holder("David Whitesell", "david-whitesell"),
               ]),
        office("village-president", "Village President",
               "Hyde Park Village President", 1,
               [charter225("section 51(a)(2) and section 55: "
                           "one President is elected for a "
                           "one-year term; the President "
                           "presides at Village meetings as "
                           "Moderator, so no separate moderator "
                           "post is created"),
                S(HPV_MEETING, "Village of Hyde Park, 'A Summary "
                               "of the May 5, 2026 Annual "
                               "Village Meeting', Article 1: "
                               "Susan Bartlett was elected "
                               "Village President and Moderator "
                               "for a term of one year")],
               [holder("Susan Bartlett", "susan-bartlett")]),
        office("bliss-fund-trustee", "Bliss Fund Trustee",
               "Hyde Park Bliss Fund Trustees", 3,
               [charter225("section 51(a)(3) and section 54: "
                           "three Bliss Fund trustees, one "
                           "elected each year for a three-year "
                           "term"),
                S(HPV_MEETING, "Village of Hyde Park, 'A Summary "
                               "of the May 5, 2026 Annual "
                               "Village Meeting', Article 3: "
                               "Gary Anderson was elected "
                               "Trustee of the Bliss Library "
                               "fund for three years (ending "
                               "2029)"),
                S(HP_NEWS, "Town of Hyde Park, official monthly "
                           "newsletter (October-November "
                           "2025), Village update: 'Bliss "
                           "Library Fund: Edward French, Jack "
                           "Anderson, and Adam Lory'. Gary "
                           "Anderson's 2026 election fills the "
                           "seat that stood that year; if Jack "
                           "Anderson is a distinct person, his "
                           "is the seat Gary Anderson took")],
               [holder("Edward French", "edward-french",
                       person_scope="hyde-park-35050"),
                holder("Adam Lory", "adam-lory"),
                holder("Gary Anderson", "gary-anderson")]),
        office("village-clerk", "Village Clerk",
               "Hyde Park Village Clerk", 1,
               [charter225("section 71(a)(1) and section 72: "
                           "the Village Clerk is appointed by "
                           "the Board of Trustees for a one-year "
                           "term"),
                S(HPV_MINUTES, "Village of Hyde Park, Board of "
                               "Trustees minutes, May 7, 2026: "
                               "Karen Wescom was appointed "
                               "Village Clerk")],
               [holder("Karen Wescom", "karen-wescom",
                       how_seated="appointed")]),
        office("village-treasurer", "Village Treasurer",
               "Hyde Park Village Treasurer", 1,
               [charter225("section 71(a)(2) and section 73: "
                           "the Village Treasurer is appointed "
                           "by the Board of Trustees for a "
                           "one-year term"),
                S(HPV_MINUTES, "Village of Hyde Park, Board of "
                               "Trustees minutes, May 7, 2026: "
                               "Karen Wescom was appointed "
                               "Village Treasurer")],
               [holder("Karen Wescom", "karen-wescom",
                       how_seated="appointed")]),
        office("auditor", "Village Auditor",
               "Hyde Park Village Auditors", 3,
               [charter225("section 51(a)(4) and section 53: "
                           "three auditors are elected for "
                           "three-year terms, one each year. "
                           "Structure only: no official source "
                           "names the current village auditors")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Hyde Park Collector of Delinquent Taxes", 1,
               [charter225("section 71(a)(3): a Delinquent Tax "
                           "Collector is appointed by the Board "
                           "of Trustees. Structure only: the "
                           "2026 organizational minutes record "
                           "no appointment to the office")]),
        office("constable", "Constable", "Hyde Park Constable",
               1,
               [charter225("section 71(a)(4): a Constable is "
                           "appointed by the Board of "
                           "Trustees. Structure only: the 2026 "
                           "organizational minutes record no "
                           "appointment to the office")]),
    ]
    return spec("hyde-park", "Hyde Park Village", offices)


SPECS.append(hyde_park_village_spec())

# ------------------------------------------------------------ Ira
IRA_RESULTS = {
    "url": "https://img1.wsimg.com/blobby/go/630ba3dc-3b66-416f-813c-e6ad9997a9cb/downloads/282206fd-8c5d-4efc-8859-7e27986c1fa7/2026%20Town%20Election%20Results.pdf?ver=1792249420681",
    "note": "PLACEHOLDER",
}
IRA_OFFICERS = {
    "url": "https://img1.wsimg.com/blobby/go/630ba3dc-3b66-416f-813c-e6ad9997a9cb/downloads/d8260db4-9647-47c5-9ead-4daf8c623e1f/2025%20Elections%20Officers.pdf?ver=1792249420681",
    "note": "PLACEHOLDER",
}


def ira_results(what):
    return S(IRA_RESULTS, f"Town of Ira, '2026 Town & School "
             f"Election Results' (official town website): {what}")


def ira_officers(what):
    return S(IRA_OFFICERS, f"Town of Ira, 'Town Officers as of "
             f"March 2025 Election' (official town website): "
             f"{what}")


def ira_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Ira Selectboard", 3,
               [ira_results("Nathan Hewitt was elected to a "
                            "three-year Selectboard term"),
                ira_officers("the Selectboard seats Darin May "
                             "(term ends 2028) and Tim Carter "
                             "(2027) alongside Hewitt"),
                sb_dir("the directory seats Timothy Carter, "
                       "Nathan Hewitt (Chair), and Darin May")],
               [holder("Nathan Hewitt", "nathan-hewitt"),
                holder("Darin May", "darin-may"),
                holder("Tim Carter", "tim-carter")]),
        office("moderator", "Town Moderator", "Ira Moderator", 1,
               [ira_results("Mary Richthammer was elected Town "
                            "Moderator (one-year term)")],
               [holder("Mary Richthammer", "mary-richthammer")]),
        office("town-clerk", "Town Clerk", "Ira Town Clerk", 1,
               [ira_officers("Town Clerk Bobbi Raiche was "
                             "elected in March 2025 to a term "
                             "running past the March 2026 "
                             "meeting"),
                guide("Ira Town Clerk is Bobbi Raiche"),
                clerk_xlsx("Ira Town Clerk is Bobbi Raiche")],
               [holder("Bobbi Raiche", "bobbi-raiche")]),
        office("town-treasurer", "Town Treasurer",
               "Ira Town Treasurer", 1,
               [ira_officers("Town Treasurer Deborah Perry's "
                             "term runs to 2027"),
                guide("Ira Treasurer is Deborah J Perry"),
                treas_xlsx("Ira Treasurer is Deborah Perry")],
               [holder("Deborah Perry", "deborah-perry")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Ira Collector of Delinquent Taxes", 1,
               [ira_results("Deborah J Perry was elected "
                            "Delinquent Tax Collector (one-year "
                            "term)")],
               [holder("Deborah Perry", "deborah-perry")]),
        office("auditor", "Town Auditor", "Ira Town Auditors", 3,
               [ira_results("Christine Tyminski was elected "
                            "Auditor (three-year term); an "
                            "auditor contest for the remaining "
                            "two years of another term declared "
                            "no winner"),
                ira_officers("Auditor Tina Graves's term runs "
                             "to 2027; the third auditor seat "
                             "has been vacant since March "
                             "2025")],
               [holder("Tina Graves", "tina-graves"),
                holder("Christine Tyminski",
                       "christine-tyminski")]),
        office("lister", "Lister", "Ira Board of Listers", 3,
               [ira_results("Janine Peterson was elected "
                            "Lister (three-year term); a lister "
                            "contest for a remaining one-year "
                            "term declared no winner"),
                ira_officers("Lister Karen Davis's term runs "
                             "to 2028; the third lister seat "
                             "has been vacant since 2024")],
               [holder("Karen Davis", "karen-davis"),
                holder("Janine Peterson", "janine-peterson")]),
        office("first-constable", "First Constable",
               "Ira First Constable", 1,
               [ira_results("Francis Lloyd was elected First "
                            "Constable"),
                ira_officers("First Constable Fran Lloyd's "
                             "prior two-year term ran to 2026")],
               [holder("Francis Lloyd", "francis-lloyd")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Ira Justices of the Peace", 4,
               [jp_src("the listing names four justices of the "
                       "peace for Ira")],
               [holder("Mary Ann Black", "mary-ann-black"),
                holder("Robert Toppin", "robert-toppin"),
                holder("Larry Taggart", "larry-taggart"),
                holder("Madeline Kerstetter",
                       "madeline-kerstetter")]),
    ]
    jp = jp_election(
        "ira-vt", "Ira", 4,
        "the winners were Mary Ann Black, Robert Toppin, "
        "Larry Taggart, and Madeline Kerstetter (four seats). "
        "The town's March 2025 officers sheet confirms the "
        "same four",
        [ira_officers("the officers sheet lists the same four "
                      "justices")])
    return spec("ira", "Ira", offices, jp)


SPECS.append(ira_spec())

# ------------------------------------------------------------ Irasburg
def irasburg_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Irasburg Selectboard", 3,
               [sb_dir("the directory seats Michael Booth, "
                       "Patrick Cartee, and Dave Lahar "
                       "(Chair). Irasburg's former town domain "
                       "now redirects to a web host's page; "
                       "this is a spine build")],
               [holder("Michael Booth", "michael-booth"),
                holder("Patrick Cartee", "patrick-cartee"),
                holder("Dave Lahar", "dave-lahar")]),
        office("town-clerk", "Town Clerk", "Irasburg Town Clerk",
               1,
               [guide("Irasburg Town Clerk is Danielle Ingalls"),
                clerk_xlsx("Irasburg Town Clerk is Danielle "
                           "Ingalls")],
               [holder("Danielle Ingalls", "danielle-ingalls")]),
        office("town-treasurer", "Town Treasurer",
               "Irasburg Town Treasurer", 1,
               [guide("Irasburg Treasurer is Danielle Ingalls"),
                treas_xlsx("Irasburg Treasurer is Danielle "
                           "Ingalls")],
               [holder("Danielle Ingalls", "danielle-ingalls")]),
        office("moderator", "Town Moderator",
               "Irasburg Moderator", 1,
               [statute2646_structure("a moderator")]),
        office("lister", "Lister", "Irasburg Board of Listers",
               3, [statute2646_structure("three listers")]),
        office("auditor", "Town Auditor", "Irasburg Town Auditors",
               3, [statute2646_structure("three auditors")]),
        office("grand-juror", "Grand Juror",
               "Irasburg Grand Juror", 1,
               [statute2646_structure("a grand juror")]),
        office("town-agent", "Town Agent", "Irasburg Town Agent",
               1, [statute2646_structure("a town agent")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Irasburg Justices of the Peace", 1,
               [jp_src("the listing names one justice of the "
                       "peace for Irasburg")],
               [holder("Robert Booth", "robert-booth")]),
    ]
    jp = jp_election(
        "irasburg-vt", "Irasburg", 1,
        "the listing names one winner for Irasburg: Robert "
        "Booth (one seat as listed)")
    return spec("irasburg", "Irasburg", offices, jp)


SPECS.append(irasburg_spec())

# ------------------------------------------------------------ Isle La Motte
ILM_OFFICERS = {
    "url": "https://islelamotte.us/elected-appointed-town-officers/",
    "note": "PLACEHOLDER",
}


def ilm(what):
    return S(ILM_OFFICERS, "Town of Isle La Motte, 'Elected & "
             f"Appointed Town Officers' table (official town "
             f"website): {what}")


def isle_la_motte_spec():
    offices = [
        office("selectboard", "Selectboard Member",
               "Isle La Motte Selectboard", 5,
               [ilm("the Selectboard seats Cary Sandvig "
                    "(Chair, term 2029), Peter Brzozowy "
                    "(Vice-Chair, 2027), Joseph Deller (2027), "
                    "Mary Catherine Graziano (2028), and "
                    "Meredith Vincent (2028). The SOS "
                    "Selectboard directory carries no Isle La "
                    "Motte roster, so the town table is the "
                    "roster of record")],
               [holder("Cary Sandvig", "cary-sandvig"),
                holder("Peter Brzozowy", "peter-brzozowy"),
                holder("Joseph Deller", "joseph-deller"),
                holder("Mary Catherine Graziano",
                       "mary-catherine-graziano"),
                holder("Meredith Vincent", "meredith-vincent")]),
        office("moderator", "Town Moderator",
               "Isle La Motte Moderator", 1,
               [ilm("Moderator (Town) is Peter Brzozowy (term "
                    "2027)")],
               [holder("Peter Brzozowy", "peter-brzozowy")]),
        office("town-clerk", "Town Clerk",
               "Isle La Motte Town Clerk", 1,
               [ilm("Town Clerk is Vickie Buswell (term 2028)"),
                guide("Isle La Motte Town Clerk is Vickie "
                      "Buswell"),
                clerk_xlsx("Isle La Motte Town Clerk is Vickie "
                           "Buswell")],
               [holder("Vickie Buswell", "vickie-buswell")]),
        office("town-treasurer", "Town Treasurer",
               "Isle La Motte Town Treasurer", 1,
               [ilm("Town Treasurer is Mary Labrecque (term "
                    "2028)"),
                guide("Isle La Motte Treasurer is Mary "
                      "Labrecque")],
               [holder("Mary Labrecque", "mary-labrecque")]),
        office("lister", "Lister",
               "Isle La Motte Board of Listers", 3,
               [ilm("the Board of Listers seats Louise Koss "
                    "(2029), Selby Turner (2027), and Mary "
                    "Labrecque (Chair, 2028)")],
               [holder("Louise Koss", "louise-koss"),
                holder("Selby Turner", "selby-turner"),
                holder("Mary Labrecque", "mary-labrecque")]),
        office("constable", "Constable",
               "Isle La Motte Constable", 1,
               [ilm("the elected Constable is Lyle Andrews "
                    "(term 2027)")],
               [holder("Lyle Andrews", "lyle-andrews")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes",
               "Isle La Motte Collector of Delinquent Taxes", 1,
               [ilm("the elected Delinquent Tax Collector is "
                    "Mary Labrecque (term 2027)")],
               [holder("Mary Labrecque", "mary-labrecque")]),
        office("town-agent", "Town Agent",
               "Isle La Motte Town Agent", 1,
               [ilm("the Town Agent row reads 'Open'. "
                    "Structure only")]),
        office("grand-juror", "Grand Juror",
               "Isle La Motte Grand Juror", 1,
               [ilm("the Grand Juror row reads 'Open'. "
                    "Structure only")]),
        office("cemetery-commissioner", "Cemetery Commissioner",
               "Isle La Motte Cemetery Commission", 3,
               [ilm("the Cemetery Commission seats Allen Hall "
                    "(2028) and Cathy Tudhope (2029); the "
                    "third seat reads 'Open' and is left "
                    "unfilled")],
               [holder("Allen Hall", "allen-hall"),
                holder("Cathy Tudhope", "cathy-tudhope")]),
        office("trustee-of-public-funds",
               "Trustee of Public Funds",
               "Isle La Motte Trustees of Public Funds", 3,
               [ilm("the Trustees of Public Funds are William "
                    "Henne (2029), Sylvia Jensen (Chair, "
                    "2027), and Barbara Callahan (2028)")],
               [holder("William Henne", "william-henne"),
                holder("Sylvia Jensen", "sylvia-jensen"),
                holder("Barbara Callahan", "barbara-callahan")]),
        office("justice-of-the-peace", "Justice of the Peace",
               "Isle La Motte Justices of the Peace", 5,
               [jp_src("the listing names four justices of the "
                       "peace for Isle La Motte"),
                ilm("the town's officers table seats five "
                    "justices on February 2027 terms, adding "
                    "Karen Brunner to the listing's four; the "
                    "table distinguishes 'Open' seats "
                    "elsewhere, so Brunner is minted as the "
                    "fifth holder with the discrepancy "
                    "disclosed")],
               [holder("Allen Hall", "allen-hall"),
                holder("Sarah Peacock", "sarah-peacock"),
                holder("Cathy Tudhope", "cathy-tudhope"),
                holder("Sylvia Jensen", "sylvia-jensen"),
                holder("Karen Brunner", "karen-brunner")]),
    ]
    jp = jp_election(
        "isle-la-motte-vt", "Isle La Motte", 5,
        "the listing names four winners for Isle La Motte: "
        "Allen Hall, Syvia Jensen [sic], Sarah Peacock, and "
        "Cathy Tudhope. The town's own officers table seats "
        "five justices on February 2027 terms, adding Karen "
        "Brunner, and marks other vacant offices 'Open' -- "
        "Brunner is therefore carried as the fifth winner "
        "with the listing discrepancy disclosed (vote_for 5 "
        "per the town table)",
        [ilm("the officers table's Justice of the Peace block "
             "names Hall, Peacock, Tudhope, Sylvia Jensen, "
             "and Karen Brunner, each 'FEB 2027'")])
    return spec("isle-la-motte", "Isle La Motte", offices, jp)


SPECS.append(isle_la_motte_spec())

# ------------------------------------------------------------ emit
for s in SPECS:
    p = OUT / f"{s['place_slug']}.json"
    p.write_text(json.dumps(s, indent=1) + "\n")
    n_off = len(s["offices"])
    n_hold = sum(len(o.get("holders", ())) for o in s["offices"])
    print(f"{s['place_slug']}: {n_off} offices, {n_hold} holders")
print(f"TOTAL: {len(SPECS)} specs")
