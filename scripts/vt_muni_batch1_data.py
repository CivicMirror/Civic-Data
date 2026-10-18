#!/usr/bin/env python3
"""Batch 1 data for the VT municipal fan-out (issue #163): Addison,
Albany (town), Alburgh (town), Alburgh (village), Andover, Arlington,
Athens, Bakersfield, Baltimore -- strict alphabetical positions 1-10
(Albany Village is position 3 but is HELD: no charter chapter, no
official website, and the VT Jurisdiction Factory holds it too, so
no records are minted for it this pass).

Writes one JSON spec per municipality into scripts/vt_muni_data/ for
scripts/build_vt_municipality.py. All rosters were verified against
official sources on 2026-10-17; see vt_muni_batch1_research.md for
the working notes and the divergence log.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "vt_muni_data"
OUT.mkdir(exist_ok=True)

SEL = ("https://outside.vermont.gov/dept/sos/Elections_Division/"
       "election_info_resources/town_meeting_local_elections/"
       "selectboardinformation.pdf")
JP = ("https://outside.vermont.gov/dept/sos/Elections_Division/"
      "election_info_resources/candidates/local_office_descriptions/"
      "vermont_justices_of_the_peace.pdf")
CLERKX = ("https://outside.vermont.gov/dept/sos/Elections_Division/"
          "voters/vermont_town_clerk_contact_information.xlsx")
TREASX = ("https://outside.vermont.gov/dept/sos/Elections_Division/"
          "voters/vermont_town_treasurer_contact_information.xlsx")
GUIDE = ("https://outside.vermont.gov/dept/sos/Elections_Division/"
         "voters/guide_vermonts_town_clerks_treasurers_county.pdf")
STATUTE = "https://legislature.vermont.gov/statutes/section/17/055/02646"
CHARTER203 = ("https://legislature.vermont.gov/statutes/"
              "fullchapter/24APPENDIX/203")


def sel_src(town, names):
    return {"url": SEL, "note": (
        "Vermont Secretary of State, Elections Division, 'Vermont "
        f"Selectboard Members' directory (last updated June 5, 2026), "
        f"{town} entry: {names}.")}


def clerk_src(town, name):
    return {"url": CLERKX, "note": (
        "Vermont Secretary of State, Elections Division, town clerk "
        "contact information spreadsheet (last updated June 12, "
        f"2026), {town} row: {name}, Town Clerk.")}


def treas_src(town, name):
    return {"url": TREASX, "note": (
        "Vermont Secretary of State, Elections Division, town "
        "treasurer contact information spreadsheet (last updated "
        f"June 12, 2026), {town} row: {name}, Town Treasurer.")}


def guide_src(town, text):
    return {"url": GUIDE, "note": (
        "Vermont Secretary of State, Elections Division, 'Guide to "
        "Vermont's Town Clerks, Treasurers & County Clerks' (January "
        f"2026), {town} entry: {text}.")}


def jp_src(town, county, names):
    return {"url": JP, "note": (
        "Vermont Secretary of State, Elections Division, '2025-2026 "
        "Vermont Justices of the Peace' listing (last updated "
        f"December 4, 2025), {town} ({county} County): {names}. The "
        "listing presents the justices elected November 5, 2024.")}


def jp_election_src():
    return {"url": JP, "note": (
        "Winners per the Vermont Secretary of State's official "
        "'2025-2026 Vermont Justices of the Peace' listing (last "
        "updated December 4, 2025). Vote totals and party labels are "
        "not published in that listing and are not recorded here.")}


def structure_src(town, descriptor):
    return {"url": STATUTE, "note": (
        "Office established for Vermont towns by 17 V.S.A. section "
        f"2646 ({descriptor}). No official source found as of "
        f"2026-10-17 publishes the current {town} holder; the post "
        "is created as structure only and the membership awaits the "
        "printed annual town report or a clerk records reply.")}


STRUCTURE5 = [
    ("moderator", "Moderator", 1, "Moderator",
     "moderator, elected annually"),
    ("lister", "Lister", 3, "Listers",
     "board of listers elected at annual meeting; three members "
     "serve staggered three-year terms under section 2649"),
    ("auditor", "Auditor", 3, "Auditors",
     "auditors elected at annual meeting; three serve staggered "
     "three-year terms under section 2651. A town may vote to "
     "eliminate the office and engage a public accountant under "
     "section 2651b; whether this town has done so is not "
     "determinable from published sources"),
    ("grand-juror", "Grand Juror", 1, "Grand Juror",
     "grand juror, elected annually"),
    ("town-agent", "Town Agent", 1, "Town Agent",
     "town agent, elected annually"),
]


def structure_offices(place_name, town, skip=()):
    out = []
    for slug, title, seats, org_suffix, descriptor in STRUCTURE5:
        if slug in skip:
            continue
        out.append({
            "slug": slug, "title": title, "seats": seats,
            "org_name": f"{place_name} {org_suffix}",
            "sources": [structure_src(town, descriptor)],
            "holders": [],
        })
    return out


def office(slug, title, seats, org_name, sources, holders):
    return {"slug": slug, "title": title, "seats": seats,
            "org_name": org_name, "sources": sources,
            "holders": holders}


def holder(slug, name, **kw):
    h = {"slug": slug, "name": name}
    h.update(kw)
    return h


def jp_block(place, town_label, seats):
    return {
        "election_id": f"{place}-vt/2024-11-05/general",
        "contest_id": f"{place}-vt/2024-11-05/justice-of-the-peace",
        "name": f"{town_label} 2024-11-05 general election",
        "filename": f"{place}-vt--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": seats,
        "sources": [jp_election_src()],
        "header": (f"# {town_label} Justice of the Peace election, "
                   "November 5, 2024;\n# issue #163 (VT master "
                   "tracking).\n"),
    }


def header(kind, label):
    return (f"# {kind} of {label} municipal roster backfill -- "
            "Vermont\n# municipal fan-out batch 1; issue #163 "
            "(VT master tracking).\n")


SPECS = []

# ---------------------------------------------------------------- Addison
ADD_OFFICERS = "https://addisonvt.gov/election-voter-information/elected-appointed-officers/"
addison_sel = sel_src("Addison",
                      "Peter Briggs; Chris Carella; Geoffrey Grant "
                      "(Vice-Chair); Jeff Kauffman (Chair); Roger Waterman")
addison_jp = jp_src("Addison", "Addison",
                    "Tom Fisher, William Munoff, Starr Phillips, Jane "
                    "Spencer, Jennifer Barrett, Vincent Paradis, Jason "
                    "Sampson")
SPECS.append({
    "place_slug": "addison",
    "jurisdiction_id": "ocd-jurisdiction/country:us/state:vt/place:addison/government",
    "label": "Town of Addison",
    "header": header("Town", "Addison"),
    "offices": [
        office("selectboard-member", "Selectboard Member", 5,
               "Addison Selectboard", [addison_sel], [
                   holder("peter-briggs", "Peter Briggs"),
                   holder("chris-carella", "Chris Carella"),
                   holder("geoffrey-grant", "Geoffrey Grant"),
                   holder("jeff-kauffman", "Jeff Kauffman"),
                   holder("roger-waterman", "Roger Waterman"),
               ]),
        office("town-clerk", "Town Clerk", 1, "Addison Town Clerk",
               [clerk_src("Addison", "Cheri Waterman"),
                guide_src("Addison", "Cheri Waterman, Clerk")],
               [holder("cheri-waterman", "Cheri Waterman")]),
        office("town-treasurer", "Town Treasurer", 1,
               "Addison Town Treasurer",
               [treas_src("Addison", "Cheri Waterman"),
                guide_src("Addison", "Cheri Waterman, Treasurer")],
               [holder("cheri-waterman", "Cheri Waterman")]),
        office("justice-of-the-peace", "Justice of the Peace", 7,
               "Addison Justices of the Peace", [addison_jp], [
                   holder("tom-fisher", "Tom Fisher"),
                   holder("william-munoff", "William Munoff"),
                   holder("starr-phillips", "Starr Phillips"),
                   holder("jane-spencer", "Jane Spencer"),
                   holder("jennifer-barrett", "Jennifer Barrett"),
                   holder("vincent-paradis", "Vincent Paradis"),
                   holder("jason-sampson", "Jason Sampson"),
               ]),
        office("moderator", "Moderator", 1, "Addison Moderator",
               [{"url": ADD_OFFICERS, "note": (
                   "Town of Addison official website, 'Elected & "
                   "Appointed Officers' page (information updated as "
                   "of October 2026): Moderator Tim Buskey.")}],
               [holder("tim-buskey", "Tim Buskey")]),
        office("lister", "Lister", 3, "Addison Listers",
               [{"url": ADD_OFFICERS, "note": (
                   "Town of Addison official website, 'Elected & "
                   "Appointed Officers' page (information updated as "
                   "of October 2026): Listers John Spencer, Terry "
                   "Cutich, William Munoff.")}],
               [holder("john-spencer", "John Spencer"),
                holder("terry-cutich", "Terry Cutich"),
                holder("william-munoff", "William Munoff")]),
        office("auditor", "Auditor", 3, "Addison Auditors",
               [{"url": ADD_OFFICERS, "note": (
                   "Town of Addison official website, 'Elected & "
                   "Appointed Officers' page (information updated as "
                   "of October 2026): Auditors Kathy Clark, Sid "
                   "Everest, Tim Buskey.")}],
               [holder("kathy-clark", "Kathy Clark"),
                holder("sid-everest", "Sid Everest"),
                holder("tim-buskey", "Tim Buskey")]),
        office("grand-juror", "Grand Juror", 1, "Addison Grand Juror",
               [{"url": ADD_OFFICERS, "note": (
                   "Town of Addison official website, 'Elected & "
                   "Appointed Officers' page (information updated as "
                   "of October 2026): Town Grand Juror Robert "
                   "Barrows. The page notes the Grand Juror became "
                   "an appointed position in Addison in 2021.")}],
               [holder("robert-barrows", "Robert Barrows",
                       how_seated="appointed")]),
        office("town-agent", "Town Agent", 1, "Addison Town Agent",
               [{"url": ADD_OFFICERS, "note": (
                   "Town of Addison official website, 'Elected & "
                   "Appointed Officers' page (information updated as "
                   "of October 2026): Town Agent Robert Barrows. "
                   "The page notes the Town Agent became an "
                   "appointed position in Addison in 2021.")}],
               [holder("robert-barrows", "Robert Barrows",
                       how_seated="appointed")]),
        office("first-constable", "First Constable", 1,
               "Addison First Constable",
               [{"url": ADD_OFFICERS, "note": (
                   "Town of Addison official website, 'Elected & "
                   "Appointed Officers' page (information updated as "
                   "of October 2026): First Constable Robert "
                   "Barrows.")}],
               [holder("robert-barrows", "Robert Barrows")]),
        office("second-constable", "Second Constable", 1,
               "Addison Second Constable",
               [{"url": ADD_OFFICERS, "note": (
                   "Town of Addison official website, 'Elected & "
                   "Appointed Officers' page (information updated as "
                   "of October 2026): Second Constable Gerald "
                   "Grant.")}],
               [holder("gerald-grant", "Gerald Grant")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes", 1,
               "Addison Collector of Delinquent Taxes",
               [{"url": ADD_OFFICERS, "note": (
                   "Town of Addison official website, 'Elected & "
                   "Appointed Officers' page (information updated as "
                   "of October 2026): Collector of Delinquent Taxes "
                   "Alden Harwood. The office is filled separately "
                   "from the Town Treasurer in Addison (17 V.S.A. "
                   "section 2651d).")}],
               [holder("alden-harwood", "Alden Harwood")]),
    ],
    "jp_election": jp_block("addison", "Addison", 7),
})

# ------------------------------------------------------------- Albany town
albany_jp = jp_src("Albany", "Orleans",
                   "Chad Tollman, Anthony Daniels, Vicki Strong, "
                   "Cheryl Dewees, Kelsey Crelin")
albany_sb_structure = {"url": STATUTE, "note": (
    "Office established for Vermont towns by 17 V.S.A. section 2646 "
    "(a selectboard of three members unless the town votes five). "
    "The Secretary of State's selectboard directory publishes no "
    "Albany roster ('Note: Contact the Town Clerk for more "
    "information'), and the Town of Albany has no official website, "
    "so no official source found as of 2026-10-17 publishes the "
    "board's current members; the post is created as structure only "
    "with the statutory three seats, and the memberships await the "
    "printed annual town report or a clerk records reply.")}
SPECS.append({
    "place_slug": "albany-00475",
    "jurisdiction_id": "ocd-jurisdiction/country:us/state:vt/place:albany-00475/government",
    "label": "Town of Albany",
    "header": header("Town", "Albany"),
    "offices": [
        office("selectboard-member", "Selectboard Member", 3,
               "Albany Selectboard", [albany_sb_structure], []),
        office("town-clerk", "Town Clerk", 1, "Albany Town Clerk",
               [clerk_src("Albany", "Tonya Coderre"),
                guide_src("Albany", "Tonya Coderre, Clerk")],
               [holder("tonya-coderre", "Tonya Coderre")]),
        office("town-treasurer", "Town Treasurer", 1,
               "Albany Town Treasurer",
               [guide_src("Albany", "Tonya Coderre, Treasurer")],
               [holder("tonya-coderre", "Tonya Coderre")]),
        office("justice-of-the-peace", "Justice of the Peace", 5,
               "Albany Justices of the Peace", [albany_jp], [
                   holder("chad-tollman", "Chad Tollman"),
                   holder("anthony-daniels", "Anthony Daniels"),
                   holder("vicki-strong", "Vicki Strong"),
                   holder("cheryl-dewees", "Cheryl Dewees"),
                   holder("kelsey-crelin", "Kelsey Crelin"),
               ]),
    ] + structure_offices("Albany", "Albany"),
    "jp_election": jp_block("albany-00475", "Albany", 5),
})

# ------------------------------------------------------------ Alburgh town
ALB_SB = "https://alburghvt.org/alburgh-select-board/"
ALB_CLERK = "https://alburghvt.org/town-clerk/"
ALB_LISTERS = "https://alburghvt.org/listers/"
ALB_AUDITORS = "https://alburghvt.org/auditors/"
ALB_OFFICERS = "https://alburghvt.org/alburgh-town-officers/"
alburgh_sb = {"url": ALB_SB, "note": (
    "Town of Alburgh official website, Selectboard page (read "
    "October 17, 2026): Alex McCracken, Jim Hokenberg, Russell "
    "Duchaine, Walter Kane, Tom Ward. The Secretary of State's "
    "selectboard directory publishes no Alburgh roster. Terms "
    "printed on the page are not recorded as membership dates.")}
alburgh_jp = jp_src("Alburgh", "Grand Isle",
                    "Christopher Higgins, Gina Lewis, Loretta Knight, "
                    "Lisa Arnold, Constance Boutin, John Goodrich")
james_src = {"url": ALB_AUDITORS, "note": (
    "Town of Alburgh official website, Auditors page (read October "
    "17, 2026): Joanne James, serving 2026-2027 for the remaining "
    "term 2025-2028. The page does not state whether she was "
    "appointed or elected to the remainder; she is recorded as "
    "elected, the office's ordinary mode, with the uncertainty "
    "noted here and flagged on issue #163.")}
SPECS.append({
    "place_slug": "alburgh-00860",
    "jurisdiction_id": "ocd-jurisdiction/country:us/state:vt/place:alburgh-00860/government",
    "label": "Town of Alburgh",
    "header": header("Town", "Alburgh"),
    "offices": [
        office("selectboard-member", "Selectboard Member", 5,
               "Alburgh Selectboard", [alburgh_sb], [
                   holder("alex-mccracken", "Alex McCracken"),
                   holder("jim-hokenberg", "Jim Hokenberg"),
                   holder("russell-duchaine", "Russell Duchaine"),
                   holder("walter-kane", "Walter Kane"),
                   holder("tom-ward", "Tom Ward"),
               ]),
        office("town-clerk", "Town Clerk", 1, "Alburgh Town Clerk",
               [clerk_src("Alburgh", "Danielle James Choiniere"),
                guide_src("Alburgh", "Danielle James Choiniere, Clerk"),
                {"url": ALB_CLERK, "note": (
                    "Town of Alburgh official website, Town Clerk "
                    "page (read October 17, 2026): Town Clerk "
                    "Danielle James Choiniere, elected on a "
                    "three-year cycle.")}],
               [holder("danielle-james-choiniere",
                       "Danielle James Choiniere")]),
        office("town-treasurer", "Town Treasurer", 1,
               "Alburgh Town Treasurer",
               [guide_src("Alburgh", "Margret Brescia, Treasurer"),
                {"url": ALB_CLERK, "note": (
                    "Town of Alburgh official website, Town Clerk "
                    "page (read October 17, 2026): Town Treasurer "
                    "Margret Brescia, appointed by the selectboard. "
                    "The Secretary of State's treasurer spreadsheet "
                    "publishes no Alburgh treasurer.")}],
               [holder("margret-brescia", "Margret Brescia",
                       how_seated="appointed")]),
        office("justice-of-the-peace", "Justice of the Peace", 6,
               "Alburgh Justices of the Peace", [alburgh_jp], [
                   holder("christopher-higgins", "Christopher Higgins"),
                   holder("gina-lewis", "Gina Lewis"),
                   holder("loretta-knight", "Loretta Knight"),
                   holder("lisa-arnold", "Lisa Arnold"),
                   holder("constance-boutin", "Constance Boutin"),
                   holder("john-goodrich", "John Goodrich"),
               ]),
        office("lister", "Lister", 3, "Alburgh Listers",
               [{"url": ALB_LISTERS, "note": (
                   "Town of Alburgh official website, Listers page "
                   "(read October 17, 2026): Cheryl Dunn, Donna "
                   "Boumil, and one seat shown as Vacancy.")}],
               [holder("cheryl-dunn", "Cheryl Dunn"),
                holder("donna-boumil", "Donna Boumil")]),
        office("auditor", "Auditor", 3, "Alburgh Auditors",
               [{"url": ALB_AUDITORS, "note": (
                   "Town of Alburgh official website, Auditors page "
                   "(read October 17, 2026): Kristy Taylor (term "
                   "2024-2027), Alton Bruso (term 2026-2029), "
                   "Joanne James (serving the remainder of a "
                   "2025-2028 term). Terms printed on the page are "
                   "not recorded as membership dates.")}],
               [holder("kristy-taylor", "Kristy Taylor"),
                holder("alton-bruso", "Alton Bruso"),
                holder("joanne-james", "Joanne James",
                       sources=[james_src])]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes", 1,
               "Alburgh Collector of Delinquent Taxes",
               [{"url": ALB_OFFICERS, "note": (
                   "Town of Alburgh official website, Town Officers "
                   "page (read October 17, 2026): Delinquent Tax "
                   "Collector Danielle James Choiniere. The office "
                   "is held separately from the Town Treasurer in "
                   "Alburgh (17 V.S.A. section 2651d); the page does "
                   "not state the mode of selection, and the holder "
                   "is recorded as elected, the office's ordinary "
                   "mode when a town fills it separately.")}],
               [holder("danielle-james-choiniere",
                       "Danielle James Choiniere")]),
    ] + structure_offices("Alburgh", "Alburgh",
                           skip=("lister", "auditor")),
    "jp_election": jp_block("alburgh-00860", "Alburgh", 6),
})

# --------------------------------------------------------- Alburgh village
ALBV_HOME = "https://villageofalburgh.org/"
albv_trustees = {"url": ALBV_HOME, "note": (
    "Village of Alburgh official website, home page (read October "
    "17, 2026), 'Village Trustees': Robert Savage; Herbert Durham, "
    "Chairman; Heath Bovat; Walter Kane; Aidan Poquette. The same "
    "page carries an August 5, 2026 notice of a Board of Trustees "
    "vacancy while listing five trustees; the roster is recorded "
    "as printed.")}
albv_charter_board = {"url": CHARTER203, "note": (
    "Village of Alburgh charter, 24 Appendix V.S.A. chapter 203, "
    "section 301(a)-(b): one trustee is elected at each annual "
    "meeting to a five-year term (five staggered seats); section "
    "303 authorizes the trustees to fill vacancies by appointment.")}
albv_charter_appt = {"url": CHARTER203, "note": (
    "Village of Alburgh charter, 24 Appendix V.S.A. chapter 203, "
    "section 301(c): the Board of Trustees appoints the Village "
    "Clerk and the Village Treasurer.")}
albv_dunn = {"url": ALBV_HOME, "note": (
    "Village of Alburgh official website, home page (read October "
    "17, 2026): 'Village Clerk / Treasurer' Cheryl Dunn.")}
SPECS.append({
    "place_slug": "alburgh",
    "jurisdiction_id": "ocd-jurisdiction/country:us/state:vt/place:alburgh/government",
    "label": "Village of Alburgh",
    "header": header("Village", "Alburgh"),
    "offices": [
        office("trustee", "Trustee", 5,
               "Alburgh Village Board of Trustees",
               [albv_trustees, albv_charter_board], [
                   holder("robert-savage", "Robert Savage"),
                   holder("herbert-durham", "Herbert Durham"),
                   holder("heath-bovat", "Heath Bovat"),
                   holder("walter-kane", "Walter Kane",
                          person_scope="alburgh-00860"),
                   holder("aidan-poquette", "Aidan Poquette"),
               ]),
        office("village-clerk", "Village Clerk", 1,
               "Alburgh Village Clerk",
               [albv_dunn, albv_charter_appt],
               [holder("cheryl-dunn", "Cheryl Dunn",
                       how_seated="appointed",
                       person_scope="alburgh-00860")]),
        office("village-treasurer", "Village Treasurer", 1,
               "Alburgh Village Treasurer",
               [albv_dunn, albv_charter_appt],
               [holder("cheryl-dunn", "Cheryl Dunn",
                       how_seated="appointed",
                       person_scope="alburgh-00860")]),
        office("collector", "Collector", 1,
               "Alburgh Village Collector",
               [{"url": CHARTER203, "note": (
                   "Office established by the Village of Alburgh "
                   "charter, 24 Appendix V.S.A. chapter 203, "
                   "section 301(a)(2) (one Collector elected at "
                   "each annual meeting, one-year term). No "
                   "official source found as of 2026-10-17 "
                   "publishes the current holder; the post is "
                   "created as structure only.")}],
               []),
        office("auditor", "Auditor", 3,
               "Alburgh Village Auditors",
               [{"url": CHARTER203, "note": (
                   "Office established by the Village of Alburgh "
                   "charter, 24 Appendix V.S.A. chapter 203, "
                   "section 301(a)(3) (one auditor elected at each "
                   "annual meeting to a three-year term; three "
                   "staggered seats). No official source found as "
                   "of 2026-10-17 publishes the current holders; "
                   "the post is created as structure only.")}],
               []),
    ],
})

# ----------------------------------------------------------------- Andover
AND_SB = "https://www.andovervt.org/selectboard"
AND_OFFICE = "https://www.andovervt.org/town-office"
andover_sb = {"url": AND_SB, "note": (
    "Town of Andover official website, Selectboard page (read "
    "October 17, 2026): Richard Pierce (Chair), Robin Trask (Vice "
    "Chair), Melissa Gates-Perry, Susan Leader, Chris Walker. The "
    "Secretary of State's selectboard directory publishes no "
    "Andover roster.")}
andover_jp = jp_src("Andover", "Windsor",
                    "Linda Bargfrede, Jonathan Bliss, Donna Faturos, "
                    "Jean Petraska, Ron Theissen")
andover_cemetery = {"url": STATUTE, "note": (
    "The Town of Andover's official 2024 Town Officers list shows "
    "three elected Cemetery Commissioners; no official source "
    "found as of 2026-10-17 publishes the current holders (the "
    "2024 list is superseded for the other offices it names), so "
    "the post is created as structure only.")}
SPECS.append({
    "place_slug": "andover",
    "jurisdiction_id": "ocd-jurisdiction/country:us/state:vt/place:andover/government",
    "label": "Town of Andover",
    "header": header("Town", "Andover"),
    "offices": [
        office("selectboard-member", "Selectboard Member", 5,
               "Andover Selectboard", [andover_sb], [
                   holder("richard-pierce", "Richard Pierce"),
                   holder("robin-trask", "Robin Trask"),
                   holder("melissa-gates-perry", "Melissa Gates-Perry"),
                   holder("susan-leader", "Susan Leader"),
                   holder("chris-walker", "Chris Walker"),
               ]),
        office("town-clerk", "Town Clerk", 1, "Andover Town Clerk",
               [clerk_src("Andover", "Jeanette Hazeltine"),
                guide_src("Andover", "Jeanette Hazeltine, Clerk"),
                {"url": AND_OFFICE, "note": (
                    "Town of Andover official website, Town Office "
                    "page (read October 17, 2026): Town Clerk, "
                    "Treasurer & Tax Collector Jeanette "
                    "Hazeltine.")}],
               [holder("jeanette-hazeltine", "Jeanette Hazeltine")]),
        office("town-treasurer", "Town Treasurer", 1,
               "Andover Town Treasurer",
               [guide_src("Andover", "Jeanette Hazeltine, Treasurer"),
                {"url": AND_OFFICE, "note": (
                    "Town of Andover official website, Town Office "
                    "page (read October 17, 2026): Town Clerk, "
                    "Treasurer & Tax Collector Jeanette "
                    "Hazeltine.")}],
               [holder("jeanette-hazeltine", "Jeanette Hazeltine")]),
        office("justice-of-the-peace", "Justice of the Peace", 5,
               "Andover Justices of the Peace", [andover_jp], [
                   holder("linda-bargfrede", "Linda Bargfrede"),
                   holder("jonathan-bliss", "Jonathan Bliss"),
                   holder("donna-faturos", "Donna Faturos"),
                   holder("jean-petraska", "Jean Petraska"),
                   holder("ron-theissen", "Ron Theissen"),
               ]),
        office("cemetery-commissioner", "Cemetery Commissioner", 3,
               "Andover Cemetery Commission", [andover_cemetery], []),
    ] + structure_offices("Andover", "Andover", skip=("lister",)),
    "jp_election": jp_block("andover", "Andover", 5),
    # NOTE: no lister post -- Andover's official 2024 Town Officers
    # list shows the Lister/Assessor as an appointed position, so
    # the town has no elected board of listers to model.
})

# -------------------------------------------------------------- Arlington
ARL_INFO = "https://arlingtonvermont.org/town-clerk/arlington-town-information/"
arlington_sel = sel_src("Arlington",
                        "Matthew Bykowski (Vice-Chair); Daniel Harvey "
                        "(Chairperson); Sebastian Massey; James "
                        "Paustian; Glenn Sherman")
arlington_jp = jp_src("Arlington", "Bennington",
                      "Judy Bryan, Susan Jennings, Karen Krulikowski, "
                      "Keith Squires, Chelsea Thompson, Susan Wirkki, "
                      "Ali Elwell Zaiac")
paustian_src = {"url": ARL_INFO, "note": (
    "Town of Arlington official website, 'Arlington Town "
    "Information' page (read October 17, 2026), lists the "
    "selectboard with the name form 'Jamie Paustian'; the "
    "Secretary of State selectboard directory form 'James "
    "Paustian' is recorded.")}
SPECS.append({
    "place_slug": "arlington",
    "jurisdiction_id": "ocd-jurisdiction/country:us/state:vt/place:arlington/government",
    "label": "Town of Arlington",
    "header": header("Town", "Arlington"),
    "offices": [
        office("selectboard-member", "Selectboard Member", 5,
               "Arlington Selectboard", [arlington_sel], [
                   holder("matthew-bykowski", "Matthew Bykowski"),
                   holder("daniel-harvey", "Daniel Harvey"),
                   holder("sebastian-massey", "Sebastian Massey"),
                   holder("james-paustian", "James Paustian",
                          sources=[arlington_sel, paustian_src]),
                   holder("glenn-sherman", "Glenn Sherman"),
               ]),
        office("town-clerk", "Town Clerk", 1, "Arlington Town Clerk",
               [clerk_src("Arlington", "Susan Paustian"),
                guide_src("Arlington", "Susan Paustian, Clerk")],
               [holder("susan-paustian", "Susan Paustian")]),
        office("town-treasurer", "Town Treasurer", 1,
               "Arlington Town Treasurer",
               [treas_src("Arlington", "Christian Dickinson"),
                guide_src("Arlington", "Christian Dickinson, "
                          "Treasurer")],
               [holder("christian-dickinson", "Christian Dickinson")]),
        office("justice-of-the-peace", "Justice of the Peace", 7,
               "Arlington Justices of the Peace", [arlington_jp], [
                   holder("judy-bryan", "Judy Bryan"),
                   holder("susan-jennings", "Susan Jennings"),
                   holder("karen-krulikowski", "Karen Krulikowski"),
                   holder("keith-squires", "Keith Squires"),
                   holder("chelsea-thompson", "Chelsea Thompson"),
                   holder("susan-wirkki", "Susan Wirkki"),
                   holder("ali-elwell-zaiac", "Ali Elwell Zaiac"),
               ]),
        office("lister", "Lister", 3, "Arlington Listers",
               [{"url": ARL_INFO, "note": (
                   "Town of Arlington official website, 'Arlington "
                   "Town Information' page (read October 17, 2026), "
                   "'Board of Listers (Elected)': Joseph Garger, "
                   "Lee Cross, Collette Galusha.")}],
               [holder("joseph-garger", "Joseph Garger"),
                holder("lee-cross", "Lee Cross"),
                holder("collette-galusha", "Collette Galusha")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes", 1,
               "Arlington Collector of Delinquent Taxes",
               [{"url": ARL_INFO, "note": (
                   "Town of Arlington official website, 'Arlington "
                   "Town Information' page (read October 17, 2026): "
                   "'Delinquent Tax Collector (Elected)': Kendell "
                   "Jennings.")}],
               [holder("kendell-jennings", "Kendell Jennings")]),
        office("cemetery-commissioner", "Cemetery Commissioner", 3,
               "Arlington Cemetery Commission",
               [{"url": ARL_INFO, "note": (
                   "Town of Arlington official website, 'Arlington "
                   "Town Information' page (read October 17, 2026), "
                   "'Cemetery Commissioners (Elected)': Nathalie "
                   "Caler, William Bryan, Ali Zaiac. The page "
                   "prints the short form 'Ali Zaiac' for the "
                   "justice of the peace Ali Elwell Zaiac.")}],
               [holder("nathalie-caler", "Nathalie Caler"),
                holder("william-bryan", "William Bryan"),
                holder("ali-elwell-zaiac", "Ali Elwell Zaiac")]),
    ] + structure_offices("Arlington", "Arlington", skip=("lister",)),
    "jp_election": jp_block("arlington", "Arlington", 7),
})

# ----------------------------------------------------------------- Athens
ATH = "https://www.athensvt.com/officials.html"
athens_sb = {"url": ATH, "note": (
    "Town of Athens official website, Officials page (read October "
    "17, 2026): Selectboard David Bemis, Denise Randall, Janet "
    "Perry, Krista Gay, Danny Taylor. The Secretary of State's "
    "selectboard directory publishes no Athens roster.")}
athens_jp = jp_src("Athens", "Windham",
                   "Kate Bova, April Lyman, David Bemis, Sandi "
                   "Capponcelli, Janet Perry")
athens_moderator = {"url": ATH, "note": (
    "The Town of Athens official website's Officials page (read "
    "October 17, 2026) lists the Moderator office with no name "
    "shown; the post is created as structure only (17 V.S.A. "
    "section 2646, moderator elected annually) and the membership "
    "awaits a source that names the holder.")}
SPECS.append({
    "place_slug": "athens",
    "jurisdiction_id": "ocd-jurisdiction/country:us/state:vt/place:athens/government",
    "label": "Town of Athens",
    "header": header("Town", "Athens"),
    "offices": [
        office("selectboard-member", "Selectboard Member", 5,
               "Athens Selectboard", [athens_sb], [
                   holder("david-bemis", "David Bemis"),
                   holder("denise-randall", "Denise Randall"),
                   holder("janet-perry", "Janet Perry"),
                   holder("krista-gay", "Krista Gay"),
                   holder("danny-taylor", "Danny Taylor"),
               ]),
        office("town-clerk", "Town Clerk", 1, "Athens Town Clerk",
               [clerk_src("Athens", "Amber Stevens"),
                guide_src("Athens", "Amber Stevens, Clerk"),
                {"url": ATH, "note": (
                    "Town of Athens official website, Officials "
                    "page (read October 17, 2026): Town Clerk & "
                    "Treasurer Amber Stevens.")}],
               [holder("amber-stevens", "Amber Stevens")]),
        office("town-treasurer", "Town Treasurer", 1,
               "Athens Town Treasurer",
               [guide_src("Athens", "Amber Stevens, Treasurer"),
                {"url": ATH, "note": (
                    "Town of Athens official website, Officials "
                    "page (read October 17, 2026): Town Clerk & "
                    "Treasurer Amber Stevens.")}],
               [holder("amber-stevens", "Amber Stevens")]),
        office("justice-of-the-peace", "Justice of the Peace", 5,
               "Athens Justices of the Peace", [athens_jp], [
                   holder("kate-bova", "Kate Bova"),
                   holder("april-lyman", "April Lyman"),
                   holder("david-bemis", "David Bemis"),
                   holder("sandi-capponcelli", "Sandi Capponcelli"),
                   holder("janet-perry", "Janet Perry"),
               ]),
        office("moderator", "Moderator", 1, "Athens Moderator",
               [athens_moderator], []),
        office("lister", "Lister", 3, "Athens Listers",
               [{"url": ATH, "note": (
                   "Town of Athens official website, Officials "
                   "page (read October 17, 2026): Listers Amber "
                   "Stevens, Carol Bingham. Two of the board's "
                   "three seats are named on the page.")}],
               [holder("amber-stevens", "Amber Stevens"),
                holder("carol-bingham", "Carol Bingham")]),
        office("auditor", "Auditor", 3, "Athens Auditors",
               [{"url": ATH, "note": (
                   "Town of Athens official website, Officials "
                   "page (read October 17, 2026): Auditors Mike "
                   "Bates, Jimmy Trimble, Amanda Alsvig.")}],
               [holder("mike-bates", "Mike Bates"),
                holder("jimmy-trimble", "Jimmy Trimble"),
                holder("amanda-alsvig", "Amanda Alsvig")]),
        office("grand-juror", "Grand Juror", 1, "Athens Grand Juror",
               [{"url": ATH, "note": (
                   "Town of Athens official website, Officials "
                   "page (read October 17, 2026), elected "
                   "officials: 'Town Grand Juror and Agent' James "
                   "Trimble.")}],
               [holder("james-trimble", "James Trimble")]),
        office("town-agent", "Town Agent", 1, "Athens Town Agent",
               [{"url": ATH, "note": (
                   "Town of Athens official website, Officials "
                   "page (read October 17, 2026), elected "
                   "officials: 'Town Grand Juror and Agent' James "
                   "Trimble.")}],
               [holder("james-trimble", "James Trimble")]),
        office("collector-of-delinquent-taxes",
               "Collector of Delinquent Taxes", 1,
               "Athens Collector of Delinquent Taxes",
               [{"url": ATH, "note": (
                   "Town of Athens official website, Officials "
                   "page (read October 17, 2026): Delinquent Tax "
                   "Collector Hannah Regier, listed among the "
                   "town's elected officials.")}],
               [holder("hannah-regier", "Hannah Regier")]),
        office("cemetery-commissioner", "Cemetery Commissioner", 5,
               "Athens Cemetery Commission",
               [{"url": ATH, "note": (
                   "Town of Athens official website, Officials "
                   "page (read October 17, 2026): Cemetery "
                   "Commission Harold Noyes, Steve Oakes, Don "
                   "Capponcelli, David Bemis, James Neathawk, "
                   "listed among the town's elected boards.")}],
               [holder("harold-noyes", "Harold Noyes"),
                holder("steve-oakes", "Steve Oakes"),
                holder("don-capponcelli", "Don Capponcelli"),
                holder("david-bemis", "David Bemis"),
                holder("james-neathawk", "James Neathawk")]),
    ] + structure_offices("Athens", "Athens",
                          skip=("moderator", "lister", "auditor",
                                "grand-juror", "town-agent")),
    "jp_election": jp_block("athens", "Athens", 5),
})

# ------------------------------------------------------------- Bakersfield
BAK = "https://www.townofbakersfield.org/officials-commissions"
bakersfield_sel = sel_src("Bakersfield",
                          "Todd Cosgrove; Nicola Cribb; Amber Foote; "
                          "Lance Lawyer; John West (Chair)")
bakersfield_jp = jp_src("Bakersfield", "Franklin",
                        "Pauline Cosgrove, Patrick Evans, Brenda "
                        "Churchill, Arlene O'Rourke, Sarah Willey "
                        "Marcotte, Janice Ketchum Marcotte, Mark "
                        "Doremus")
SPECS.append({
    "place_slug": "bakersfield",
    "jurisdiction_id": "ocd-jurisdiction/country:us/state:vt/place:bakersfield/government",
    "label": "Town of Bakersfield",
    "header": header("Town", "Bakersfield"),
    "offices": [
        office("selectboard-member", "Selectboard Member", 5,
               "Bakersfield Selectboard", [bakersfield_sel], [
                   holder("todd-cosgrove", "Todd Cosgrove"),
                   holder("nicola-cribb", "Nicola Cribb"),
                   holder("amber-foote", "Amber Foote"),
                   holder("lance-lawyer", "Lance Lawyer"),
                   holder("john-west", "John West"),
               ]),
        office("town-clerk", "Town Clerk", 1,
               "Bakersfield Town Clerk",
               [clerk_src("Bakersfield", "Katherine Westcom"),
                guide_src("Bakersfield", "Katherine Westcom, Clerk")],
               [holder("katherine-westcom", "Katherine Westcom")]),
        office("town-treasurer", "Town Treasurer", 1,
               "Bakersfield Town Treasurer",
               [guide_src("Bakersfield", "Thomas Jamison, "
                          "Treasurer"),
                {"url": BAK, "note": (
                    "Town of Bakersfield official website, "
                    "'Officials & Commissions' page (read October "
                    "17, 2026), prints the treasurer as 'Tom "
                    "Jamison'; the Secretary of State Guide form "
                    "'Thomas Jamison' is recorded. The Secretary "
                    "of State's treasurer spreadsheet publishes "
                    "no Bakersfield treasurer.")}],
               [holder("thomas-jamison", "Thomas Jamison")]),
        office("justice-of-the-peace", "Justice of the Peace", 7,
               "Bakersfield Justices of the Peace", [bakersfield_jp], [
                   holder("pauline-cosgrove", "Pauline Cosgrove"),
                   holder("patrick-evans", "Patrick Evans"),
                   holder("brenda-churchill", "Brenda Churchill"),
                   holder("arlene-orourke", "Arlene O'Rourke"),
                   holder("sarah-willey-marcotte",
                          "Sarah Willey Marcotte"),
                   holder("janice-ketchum-marcotte",
                          "Janice Ketchum Marcotte"),
                   holder("mark-doremus", "Mark Doremus"),
               ]),
        office("lister", "Lister", 3, "Bakersfield Listers",
               [{"url": BAK, "note": (
                   "Town of Bakersfield official website, "
                   "'Officials & Commissions' page (read October "
                   "17, 2026): Town Listers Tamera Brennan "
                   "(Co-Chair), Sharon Evans (Co-Chair). Two of "
                   "the board's three seats are named on the "
                   "page.")}],
               [holder("tamera-brennan", "Tamera Brennan"),
                holder("sharon-evans", "Sharon Evans")]),
    ] + structure_offices("Bakersfield", "Bakersfield",
                          skip=("lister",)),
    "jp_election": jp_block("bakersfield", "Bakersfield", 7),
})

# --------------------------------------------------------------- Baltimore
BAL_PDF = ("https://www.baltimorevt.org/index_htm_files/"
           "Baltimore%20Town%20Officials%20-%20Website.pdf")
baltimore_sel = sel_src("Baltimore",
                        "Walter Rich; David Sigl; George Wheeler")
baltimore_pdf_sb = {"url": BAL_PDF, "note": (
    "Town of Baltimore official website, 'Baltimore Town "
    "Officials' list (read October 17, 2026), lists the "
    "selectboard as George Bay Wheeler (Chair), Walter Rich, "
    "David Sigl -- the same three members as the Secretary of "
    "State directory, which prints 'George Wheeler'.")}
baltimore_jp = jp_src("Baltimore", "Windsor",
                      "Kevin Gould, Martha J Jewett, Robert L "
                      "Metcalf, Kathy Muther, Lowell W Wheelock")
SPECS.append({
    "place_slug": "baltimore",
    "jurisdiction_id": "ocd-jurisdiction/country:us/state:vt/place:baltimore/government",
    "label": "Town of Baltimore",
    "header": header("Town", "Baltimore"),
    "offices": [
        office("selectboard-member", "Selectboard Member", 3,
               "Baltimore Selectboard", [baltimore_sel], [
                   holder("walter-rich", "Walter Rich"),
                   holder("david-sigl", "David Sigl"),
                   holder("george-wheeler", "George Wheeler",
                          sources=[baltimore_sel, baltimore_pdf_sb]),
               ]),
        office("town-clerk", "Town Clerk", 1, "Baltimore Town Clerk",
               [clerk_src("Baltimore", "Deborah Bean"),
                guide_src("Baltimore", "Deborah Bean, Clerk")],
               [holder("deborah-bean", "Deborah Bean")]),
        office("town-treasurer", "Town Treasurer", 1,
               "Baltimore Town Treasurer",
               [treas_src("Baltimore", "Deborah Bean"),
                guide_src("Baltimore", "Deborah Bean, Treasurer")],
               [holder("deborah-bean", "Deborah Bean")]),
        office("justice-of-the-peace", "Justice of the Peace", 5,
               "Baltimore Justices of the Peace", [baltimore_jp], [
                   holder("kevin-gould", "Kevin Gould"),
                   holder("martha-j-jewett", "Martha J Jewett"),
                   holder("robert-l-metcalf", "Robert L Metcalf"),
                   holder("kathy-muther", "Kathy Muther"),
                   holder("lowell-w-wheelock", "Lowell W Wheelock"),
               ]),
        office("lister", "Lister", 3, "Baltimore Listers",
               [{"url": BAL_PDF, "note": (
                   "Town of Baltimore official website, 'Baltimore "
                   "Town Officials' list (read October 17, 2026): "
                   "Town Listers Joan Whaley, Kathy Muther, "
                   "Michael Muther.")}],
               [holder("joan-whaley", "Joan Whaley"),
                holder("kathy-muther", "Kathy Muther"),
                holder("michael-muther", "Michael Muther")]),
    ] + structure_offices("Baltimore", "Baltimore", skip=("lister",)),
    "jp_election": jp_block("baltimore", "Baltimore", 5),
})

for spec in SPECS:
    path = OUT / f"{spec['place_slug']}.json"
    path.write_text(json.dumps(spec, indent=1) + "\n")
    print("wrote", path)
print(f"{len(SPECS)} specs (Albany Village held -- no spec).")
