#!/usr/bin/env python3
"""Batch 2 of the VT #163 municipal fan-out (alphabetical positions
11-20): Barnard, Barnet, Barre City, Barre Town, Barton Town,
Barton Village, Bellows Falls Village, Belvidere, Bennington,
Benson. Emits one JSON spec per municipality for
build_vt_municipality.py. Research: vt_muni_batch2_research.md.
Build order matters: Barton Town before Barton Village (Shelia
Martin's person record is created by the town build).
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
CLERK_SS = {
    "url": "https://outside.vermont.gov/dept/sos/Elections_Division/voters/vermont_town_clerk_contact_information.xlsx",
    "note": "PLACEHOLDER",
}
TREAS_SS = {
    "url": "https://outside.vermont.gov/dept/sos/Elections_Division/voters/vermont_town_treasurer_contact_information.xlsx",
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


def sb_dir(place_label, roster_note):
    return S(SB_DIR, f"Vermont Secretary of State, Elections Division, "
             f"'Vermont Selectboard Members' directory (updated "
             f"June 5, 2026): {roster_note}")


def jp_src(place_label, count_note):
    return S(JP_PDF, f"Vermont Secretary of State, Elections Division, "
             f"'2025-2026 Vermont Justices of the Peace' listing "
             f"(updated December 4, 2025): {count_note}")


def guide(place_label, what):
    return S(GUIDE, f"Vermont Secretary of State, Elections Division, "
             f"'Guide to Vermont's Town Clerks, Treasurers, & County "
             f"Clerks' (January 2026): {what}")


def clerk_ss(place_label, what):
    return S(CLERK_SS, f"Vermont Secretary of State, Elections Division, "
             f"town clerk contact information spreadsheet (updated "
             f"June 12, 2026): {what}")


def treas_ss(place_label, what):
    return S(TREAS_SS, f"Vermont Secretary of State, Elections Division, "
             f"town treasurer contact information spreadsheet (updated "
             f"June 12, 2026): {what}")


def statute2646(office_phrase):
    return S(STATUTE_2646, f"17 V.S.A. section 2646 (official text, "
             f"Vermont General Assembly) provides for the election of "
             f"{office_phrase} at annual town meeting.")


def jp_election(place, prefix, label, vote_for, winners_note):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(label, winners_note)],
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 2); issue #163 "
                  f"(VT master tracking).",
    }


def holder(name, slug, **kw):
    d = {"name": name, "slug": slug}
    d.update(kw)
    return d


SPECS = []

# ---------------------------------------------------------------- Barnard
BARNARD_SB_PAGE = {
    "url": "https://barnardvt.us/selectboard",
    "note": "Town of Barnard official website, Selectboard page: "
            "'Current Selectboard members are Rock Webster, Richard "
            "Lancaster, and Kurt Lessard.' The Secretary of State's "
            "Selectboard Members directory publishes no Barnard "
            "roster ('Contact the Town Clerk for more information').",
}
BARNARD_REPORT = {
    "url": "https://barnardvt.us/",
    "note": "PLACEHOLDER",
}

def barnard_report(what):
    return S(BARNARD_REPORT, f"Town of Barnard, 2026 Town Report "
             f"(FY25 Annual Report, July 1, 2024 - June 30, 2025), "
             f"'TOWN OFFICERS ELECTED' table (report page 4): {what}")

SPECS.append({
    "label": "Town of Barnard",
    "place": "barnard",
    "charter_note": "The Town of Barnard has no municipal charter in "
                    "Title 24 Appendix V.S.A.; it is a general-law "
                    "town whose officers are elected under "
                    "17 V.S.A. section 2646.",
    "offices": [
        {"slug": "selectboard", "title": "Selectboard Member",
         "org_name": "Barnard Selectboard", "seats": 3,
         "sources": [BARNARD_SB_PAGE,
                     barnard_report("lists Selectboard members Kurt "
                                    "Lessard, Richard Lancaster, and "
                                    "Rock Webster.")],
         "holders": [holder("Rock Webster", "rock-webster"),
                     holder("Richard Lancaster", "richard-lancaster"),
                     holder("Kurt Lessard", "kurt-lessard")]},
        {"slug": "town-clerk", "title": "Town Clerk",
         "org_name": "Barnard Town Clerk", "seats": 1,
         "sources": [guide("Barnard", "lists Diane Rainey as Town "
                            "Clerk of Barnard."),
                     clerk_ss("Barnard", "lists Diane Rainey as Town "
                              "Clerk of Barnard."),
                     barnard_report("lists 'Town Clerk (3-year): Diane "
                                    "L. Rainey.'")],
         "holders": [holder("Diane Rainey", "diane-rainey")]},
        {"slug": "town-treasurer", "title": "Town Treasurer",
         "org_name": "Barnard Town Treasurer", "seats": 1,
         "sources": [guide("Barnard", "lists Diane Rainey as Town "
                            "Treasurer of Barnard."),
                     barnard_report("lists 'Treasurer (3-year): Diane "
                                    "L. Rainey.' The Secretary of "
                                    "State's treasurer contact "
                                    "spreadsheet prints no Barnard "
                                    "treasurer ('Contact Town Clerk "
                                    "for more information').")],
         "holders": [holder("Diane Rainey", "diane-rainey")]},
        {"slug": "moderator", "title": "Moderator",
         "org_name": "Barnard Town Moderator", "seats": 1,
         "sources": [statute2646("a moderator"),
                     barnard_report("lists 'Moderator (1-year): Paul "
                                    "Doton' with a term expiring in "
                                    "2026; he was elected at the "
                                    "March 4, 2025 annual meeting. No "
                                    "official source publishes the "
                                    "outcome of the 2026 annual "
                                    "meeting's moderator election, so "
                                    "no holder is recorded.")]},
        {"slug": "auditor", "title": "Auditor",
         "org_name": "Barnard Town Auditors", "seats": 3,
         "sources": [barnard_report("lists Auditors (3-year) Beth "
                                    "Finlayson (term expiring 2027) "
                                    "and Tom Morse (term expiring "
                                    "2028); Patricia Hasson is "
                                    "listed with a term expiring in "
                                    "2026. Finlayson is the justice "
                                    "of the peace listing's "
                                    "'Elizabeth Finlayson.'"),
                     {"url": "https://barnardvt.us/vertical/sites/%7B5E566B10-782A-4449-B2FB-B76A35FC79A5%7D/uploads/March_4_2026_SB_Minutes.pdf",
                      "note": "Town of Barnard Selectboard minutes, "
                              "March 4, 2026 (the board's first "
                              "meeting after the 2026 annual Town "
                              "Meeting), item 8A: 'Chip Davis was "
                              "elected at Town Meeting to be one "
                              "of three auditors.'"}],
         "holders": [holder("Elizabeth Finlayson",
                            "elizabeth-finlayson"),
                     holder("Tom Morse", "tom-morse"),
                     holder("Chip Davis", "chip-davis",
                            sources=[{"url": "https://barnardvt.us/vertical/sites/%7B5E566B10-782A-4449-B2FB-B76A35FC79A5%7D/uploads/March_4_2026_SB_Minutes.pdf",
                                      "note": "Town of Barnard "
                                              "Selectboard minutes, "
                                              "March 4, 2026, item "
                                              "8A: 'Chip Davis was "
                                              "elected at Town "
                                              "Meeting to be one of "
                                              "three auditors.'"}])]},
        {"slug": "collector-of-delinquent-taxes",
         "title": "Collector of Delinquent Taxes",
         "org_name": "Barnard Collector of Delinquent Taxes",
         "seats": 1,
         "sources": [barnard_report("lists 'Delinquent Tax Collector "
                                    "(1-year): Diane L. Rainey' with "
                                    "a term expiring in 2026 — the "
                                    "town elects the office separately "
                                    "(17 V.S.A. section 2651d). No "
                                    "official source publishes the "
                                    "outcome of the 2026 annual "
                                    "meeting, so no holder is "
                                    "recorded.")]},
        {"slug": "first-constable", "title": "First Constable",
         "org_name": "Barnard First Constable", "seats": 1,
         "sources": [barnard_report("lists 'Constables (1-year): 1st "
                                    "Wes Hennig' with a term expiring "
                                    "in 2026. No official source "
                                    "publishes the outcome of the "
                                    "2026 annual meeting, so no "
                                    "holder is recorded.")]},
        {"slug": "second-constable", "title": "Second Constable",
         "org_name": "Barnard Second Constable", "seats": 1,
         "sources": [barnard_report("lists 'Constables (1-year): 2nd "
                                    "Edwin Cole' with a term expiring "
                                    "in 2026. No official source "
                                    "publishes the outcome of the "
                                    "2026 annual meeting, so no "
                                    "holder is recorded.")]},
        {"slug": "grand-juror", "title": "Grand Juror",
         "org_name": "Barnard Grand Juror", "seats": 1,
         "sources": [statute2646("a grand juror"),
                     barnard_report("names no grand juror in its "
                                    "elected or appointed officers "
                                    "tables, and no other official "
                                    "source publishes the holder.")]},
        {"slug": "town-agent", "title": "Town Agent",
         "org_name": "Barnard Town Agent", "seats": 1,
         "sources": [statute2646("a town agent to prosecute and "
                                 "defend suits"),
                     barnard_report("names no town agent in its "
                                    "elected or appointed officers "
                                    "tables, and no other official "
                                    "source publishes the holder.")]},
        {"slug": "justice-of-the-peace", "title": "Justice of the Peace",
         "org_name": "Barnard Justices of the Peace", "seats": 4,
         "sources": [jp_src("Barnard", "lists four Barnard justices "
                             "of the peace: Paul Doton, Patricia "
                             "Hasson, Elizabeth Finlayson, and Ellen "
                             "Miles.")],
         "holders": [holder("Paul Doton", "paul-doton"),
                     holder("Patricia Hasson", "patricia-hasson"),
                     holder("Elizabeth Finlayson",
                            "elizabeth-finlayson"),
                     holder("Ellen Miles", "ellen-miles")]},
    ],
    "jp_election": jp_election(
        "barnard", "barnard-vt", "Town of Barnard", 4,
        "lists four Barnard justices of the peace for the "
        "2025-2026 term (Paul Doton, Patricia Hasson, Elizabeth "
        "Finlayson, Ellen Miles); they are the winners of the "
        "November 5, 2024 election for the office. The listing "
        "publishes no vote totals and no party designations for "
        "justices of the peace."),
})

# ----------------------------------------------------------------- Barnet
BARNET_REPORT = {
    "url": "https://barnetvt.org/",
    "note": "PLACEHOLDER",
}

def barnet_report(what):
    return S(BARNET_REPORT, f"Town of Barnet, 2025 Town Report (for "
             f"the year ending December 31, 2025; Town Meeting "
             f"March 7, 2026), 'Town Elected Officers' table (report "
             f"page 10): {what}")

SPECS.append({
    "label": "Town of Barnet",
    "place": "barnet",
    "charter_note": "The Town of Barnet has no municipal charter in "
                    "Title 24 Appendix V.S.A.; it is a general-law "
                    "town whose officers are elected under "
                    "17 V.S.A. section 2646.",
    "offices": [
        {"slug": "selectboard", "title": "Selectboard Member",
         "org_name": "Barnet Selectboard", "seats": 3,
         "sources": [sb_dir("Barnet", "lists three Barnet Selectboard "
                            "members: Benjamin Adams, Dylan Ford, "
                            "and Benjamin Gates.")],
         "holders": [holder("Benjamin Adams", "benjamin-adams"),
                     holder("Dylan Ford", "dylan-ford"),
                     holder("Benjamin Gates", "benjamin-gates")]},
        {"slug": "town-clerk", "title": "Town Clerk",
         "org_name": "Barnet Town Clerk", "seats": 1,
         "sources": [guide("Barnet", "lists Benjamin Heisholt as "
                            "Town Clerk of Barnet."),
                     clerk_ss("Barnet", "lists Benjamin Heisholt as "
                              "Town Clerk of Barnet."),
                     barnet_report("lists 'Town Clerk & Treasurer: "
                                   "Benjamin Heisholt' with a term "
                                   "expiring March 2027; Barnet "
                                   "combines the clerk and treasurer "
                                   "offices in one position.")],
         "holders": [holder("Benjamin Heisholt", "benjamin-heisholt")]},
        {"slug": "town-treasurer", "title": "Town Treasurer",
         "org_name": "Barnet Town Treasurer", "seats": 1,
         "sources": [guide("Barnet", "lists Benjamin Heisholt as "
                            "Town Treasurer of Barnet."),
                     treas_ss("Barnet", "lists Benjamin Heisholt as "
                              "Town Treasurer of Barnet."),
                     barnet_report("lists 'Town Clerk & Treasurer: "
                                   "Benjamin Heisholt' with a term "
                                   "expiring March 2027; Barnet "
                                   "combines the clerk and treasurer "
                                   "offices in one position.")],
         "holders": [holder("Benjamin Heisholt", "benjamin-heisholt")]},
        {"slug": "moderator", "title": "Moderator",
         "org_name": "Barnet Town Moderator", "seats": 1,
         "sources": [statute2646("a moderator"),
                     barnet_report("lists 'Moderator: Dennis McLam' "
                                   "with a term expiring March 2026. "
                                   "No official source publishes the "
                                   "outcome of the March 2026 town "
                                   "meeting's moderator election, so "
                                   "no holder is recorded.")]},
        {"slug": "lister", "title": "Lister",
         "org_name": "Barnet Board of Listers", "seats": 3,
         "sources": [barnet_report("lists Listers John Fairchild "
                                   "(term expiring March 2027) and "
                                   "Nancy Bishop (term expiring March "
                                   "2028). A third lister, Celina "
                                   "Wright, is listed with a term "
                                   "expiring March 2026; no official "
                                   "source publishes the outcome of "
                                   "the March 2026 town meeting, so "
                                   "her seat is not recorded as "
                                   "filled.")],
         "holders": [holder("John Fairchild", "john-fairchild"),
                     holder("Nancy Bishop", "nancy-bishop")]},
        {"slug": "auditor", "title": "Auditor",
         "org_name": "Barnet Town Auditors", "seats": 3,
         "sources": [barnet_report("lists Auditors Dennis Kauppila "
                                   "(term expiring March 2027) and "
                                   "Jeffery Riley (term expiring "
                                   "March 2028). A third auditor, "
                                   "Joseph Breidenstein, is listed "
                                   "with a term expiring March 2026; "
                                   "no official source publishes the "
                                   "outcome of the March 2026 town "
                                   "meeting, so his seat is not "
                                   "recorded as filled.")],
         "holders": [holder("Dennis Kauppila", "dennis-kauppila"),
                     holder("Jeffery Riley", "jeffery-riley")]},
        {"slug": "first-constable", "title": "First Constable",
         "org_name": "Barnet First Constable", "seats": 1,
         "sources": [barnet_report("lists '1st Constable: Steve "
                                   "Mosher' with a term expiring "
                                   "March 2027.")],
         "holders": [holder("Steve Mosher", "steve-mosher")]},
        {"slug": "second-constable", "title": "Second Constable",
         "org_name": "Barnet Second Constable", "seats": 1,
         "sources": [barnet_report("lists '2nd Constable: David "
                                   "Stevenson' with a term expiring "
                                   "March 2027.")],
         "holders": [holder("David Stevenson", "david-stevenson")]},
        {"slug": "trustee-of-public-funds",
         "title": "Trustee of Public Funds",
         "org_name": "Barnet Trustees of Public Funds", "seats": 3,
         "sources": [barnet_report("lists Trustees of Public Funds "
                                   "George Coppenrath (term expiring "
                                   "March 2027) and William Graves "
                                   "(term expiring March 2028) among "
                                   "the town's elected officers. A "
                                   "third trustee, Merle Fitzgerald, "
                                   "is listed with a term expiring "
                                   "March 2026; no official source "
                                   "publishes the outcome of the "
                                   "March 2026 town meeting, so his "
                                   "seat is not recorded as filled.")],
         "holders": [holder("George Coppenrath", "george-coppenrath"),
                     holder("William Graves", "william-graves")]},
        {"slug": "collector-of-delinquent-taxes",
         "title": "Collector of Delinquent Taxes",
         "org_name": "Barnet Collector of Delinquent Taxes",
         "seats": 1,
         "sources": [barnet_report("lists 'Delinquent Tax Collector: "
                                   "Jeremy Roberts' with a term "
                                   "expiring March 2026 — the town "
                                   "elects the office separately "
                                   "(17 V.S.A. section 2651d). No "
                                   "official source publishes the "
                                   "outcome of the March 2026 town "
                                   "meeting, so no holder is "
                                   "recorded.")]},
        {"slug": "grand-juror", "title": "Grand Juror",
         "org_name": "Barnet Grand Juror", "seats": 1,
         "sources": [statute2646("a grand juror"),
                     barnet_report("names no grand juror in its "
                                   "elected or appointed officers "
                                   "tables, and no other official "
                                   "source publishes the holder.")]},
        {"slug": "town-agent", "title": "Town Agent",
         "org_name": "Barnet Town Agent", "seats": 1,
         "sources": [statute2646("a town agent to prosecute and "
                                 "defend suits"),
                     barnet_report("names no town agent in its "
                                   "elected or appointed officers "
                                   "tables, and no other official "
                                   "source publishes the holder.")]},
        {"slug": "justice-of-the-peace", "title": "Justice of the Peace",
         "org_name": "Barnet Justices of the Peace", "seats": 7,
         "sources": [jp_src("Barnet", "lists seven Barnet justices "
                             "of the peace.")],
         "holders": [holder("Shellie Samuels", "shellie-samuels"),
                     holder("William Graves", "william-graves"),
                     holder("Susan Coppenrath", "susan-coppenrath"),
                     holder("Stanley Robinson", "stanley-robinson"),
                     holder("Rebecca Boardman", "rebecca-boardman"),
                     holder("Dennis McLam", "dennis-mclam"),
                     holder("Maurice Roberts", "maurice-roberts")]},
    ],
    "jp_election": jp_election(
        "barnet", "barnet-vt", "Town of Barnet", 7,
        "lists seven Barnet justices of the peace for the 2025-2026 "
        "term (Shellie Samuels, William Graves, Susan Coppenrath, "
        "Stanley Robinson, Rebecca Boardman, Dennis McLam, Maurice "
        "Roberts); they are the winners of the November 5, 2024 "
        "election for the office. The listing publishes no vote "
        "totals and no party designations for justices of the peace."),
})

# -------------------------------------------------------------- Barre City
CH001 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/001",
    "note": "PLACEHOLDER",
}
BARRE_CITY_PAGE = {
    "url": "https://www.barrecity.org/council-and-mayor/",
    "note": "PLACEHOLDER",
}

def ch001(what):
    return S(CH001, f"City of Barre charter, 24 App. V.S.A. ch. 1 "
             f"(official text, Vermont General Assembly): {what}")

def barre_city_page(what):
    return S(BARRE_CITY_PAGE, f"City of Barre official website, "
             f"'Council and Mayor' page: {what}")

COUNCIL_SOURCES = [
    ch001("section 205(a) provides that the legal voters of each "
          "ward elect one councilor annually for a term of two "
          "years, so each of the City's three wards (section 103) "
          "has two councilors serving staggered terms."),
    barre_city_page("lists the Mayor and the six councilors by "
                    "ward."),
]

SPECS.append({
    "label": "City of Barre",
    "place": "barre",
    "charter_note": "The City of Barre is governed by its charter, "
                    "24 App. V.S.A. ch. 1: the voters elect a Mayor "
                    "and a City Clerk biennially and one councilor "
                    "per ward annually to two-year terms (section "
                    "205), for a council of six. No other city "
                    "offices are elective under the charter.",
    "offices": [
        {"slug": "mayor", "title": "Mayor",
         "org_name": "Barre City Mayor", "seats": 1,
         "sources": [ch001("section 205(a)(1) provides that the "
                           "legal voters elect biennially a Mayor."),
                     barre_city_page("lists 'Mayor Thom Lauzon.'")],
         "holders": [holder("Thom Lauzon", "thom-lauzon")]},
        {"slug": "councilor-ward-1", "title": "Councilor, Ward 1",
         "org_name": "Barre City Council", "seats": 2,
         "org_key": "barre-vt/city-council",
         "org_sources": COUNCIL_SOURCES,
         "sources": COUNCIL_SOURCES,
         "holders": [holder("Beth Hilgartner", "beth-hilgartner"),
                     holder("Sonya Spaulding", "sonya-spaulding")]},
        {"slug": "councilor-ward-2", "title": "Councilor, Ward 2",
         "org_name": "Barre City Council", "seats": 2,
         "org_key": "barre-vt/city-council",
         "org_sources": COUNCIL_SOURCES,
         "sources": COUNCIL_SOURCES,
         "holders": [holder("Jeff Bergeron", "jeff-bergeron"),
                     holder("Amanda Gustin", "amanda-gustin")]},
        {"slug": "councilor-ward-3", "title": "Councilor, Ward 3",
         "org_name": "Barre City Council", "seats": 2,
         "org_key": "barre-vt/city-council",
         "org_sources": COUNCIL_SOURCES,
         "sources": COUNCIL_SOURCES,
         "holders": [holder("Don Routhier", "don-routhier"),
                     holder("Michael Deering II",
                            "michael-deering-ii")]},
        {"slug": "city-clerk", "title": "City Clerk",
         "org_name": "Barre City Clerk", "seats": 1,
         "sources": [ch001("section 205(a)(1) provides that the "
                           "legal voters elect biennially a Clerk."),
                     guide("Barre City", "lists Cheryl Metivier as "
                           "City Clerk of Barre."),
                     clerk_ss("Barre City", "lists Cheryl Metivier "
                              "as City Clerk of Barre.")],
         "holders": [holder("Cheryl Metivier", "cheryl-metivier")]},
        {"slug": "justice-of-the-peace", "title": "Justice of the Peace",
         "org_name": "Barre City Justices of the Peace", "seats": 15,
         "sources": [jp_src("Barre City", "lists fifteen Barre City "
                             "justices of the peace.")],
         "holders": [holder("Peter D. Anthony", "peter-d-anthony"),
                     holder("Rosemary Averill", "rosemary-averill"),
                     holder("Patti Bisson", "patti-bisson"),
                     holder("Michael Boutin", "michael-boutin",
                            existing_person_id="ocd-person/8f50fe40-1322-53f1-ac77-00c4f23f0009"),
                     holder("Carol Dawes", "carol-dawes"),
                     holder("Amanda Gustin", "amanda-gustin"),
                     holder("Sarah Helman", "sarah-helman"),
                     holder("Thomas Kelly", "thomas-kelly"),
                     holder("E. John Lepage", "e-john-lepage"),
                     holder("Chrysta Murray", "chrysta-murray"),
                     holder("Sonya Spaulding", "sonya-spaulding"),
                     holder("Tabitha Tant", "tabitha-tant"),
                     holder("Tess Taylor", "tess-taylor"),
                     holder("Sharon Toborg", "sharon-toborg"),
                     holder("Teddy Waszazak", "teddy-waszazak")]},
    ],
    "jp_election": jp_election(
        "barre", "barre-vt", "City of Barre", 15,
        "lists fifteen Barre City justices of the peace for the "
        "2025-2026 term; they are the winners of the November 5, "
        "2024 election for the office. The listing publishes no "
        "vote totals and no party designations for justices of "
        "the peace."),
})

# -------------------------------------------------------------- Barre Town
CH101 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/101",
    "note": "PLACEHOLDER",
}
BARRE_TOWN_SITE = {
    "url": "https://barretown.org/",
    "note": "PLACEHOLDER",
}

def ch101(what):
    return S(CH101, f"Town of Barre charter, 24 App. V.S.A. ch. 101 "
             f"(official text, Vermont General Assembly): {what}")

def barre_town_site(what):
    return S(BARRE_TOWN_SITE, f"Town of Barre official website "
             f"(barretown.org): {what}")

SPECS.append({
    "label": "Town of Barre",
    "place": "barre-03250",
    "charter_note": "The Town of Barre is governed by its charter, "
                    "24 App. V.S.A. ch. 101: the elected officers "
                    "are five Selectboard members, one Clerk, and "
                    "one Moderator (section 10). The charter's "
                    "former elected Treasurer provision has been "
                    "repealed, and the town elects no listers or "
                    "auditors.",
    "offices": [
        {"slug": "selectboard", "title": "Selectboard Member",
         "org_name": "Barre Town Selectboard", "seats": 5,
         "sources": [ch101("section 10(a)(1) provides for the "
                           "election of five Selectboard members."),
                     barre_town_site("the Selectboard page, headed "
                                     "'Election Year 2026-2027', "
                                     "lists Justin Bolduc (Chair), "
                                     "Bob Nelson (Vice Chair), David "
                                     "Soucy, Todd Provencher, and "
                                     "Tracy Ennis. The Secretary of "
                                     "State's Selectboard Members "
                                     "directory (June 5, 2026) lists "
                                     "the same members except that "
                                     "it still shows Norma Malone "
                                     "where the town's current page "
                                     "shows Ennis (term expiring "
                                     "2029); the town's page "
                                     "governs.")],
         "holders": [holder("Justin Bolduc", "justin-bolduc"),
                     holder("Bob Nelson", "bob-nelson"),
                     holder("David Soucy", "david-soucy",
                            existing_person_id="ocd-person/17b13103-76da-5965-bbe5-ecd4606fb0d5"),
                     holder("Todd Provencher", "todd-provencher"),
                     holder("Tracy Ennis", "tracy-ennis")]},
        {"slug": "town-clerk", "title": "Town Clerk",
         "org_name": "Barre Town Clerk", "seats": 1,
         "sources": [ch101("section 10(a)(3) provides for the "
                           "election of one Clerk."),
                     barre_town_site("the Elected Officials page "
                                     "lists 'Town Clerk (3 year "
                                     "term): Tina Lunt', term "
                                     "expiring May 2027."),
                     guide("Barre Town", "lists Tina Lunt as Town "
                           "Clerk of Barre Town."),
                     clerk_ss("Barre Town", "lists Tina Lunt as Town "
                              "Clerk of Barre Town.")],
         "holders": [holder("Tina Lunt", "tina-lunt")]},
        {"slug": "moderator", "title": "Moderator",
         "org_name": "Barre Town Moderator", "seats": 1,
         "sources": [ch101("section 10(a)(4) provides for the "
                           "election of one Moderator."),
                     barre_town_site("the Elected Officials page "
                                     "lists 'Town Moderator (1 year "
                                     "term): Thomas F. Koch.'")],
         "holders": [holder("Thomas F. Koch", "thomas-f-koch",
                            ballot_name="Thomas Koch")]},
        {"slug": "justice-of-the-peace", "title": "Justice of the Peace",
         "org_name": "Barre Town Justices of the Peace", "seats": 15,
         "sources": [jp_src("Barre Town", "lists fifteen Barre Town "
                             "justices of the peace."),
                     barre_town_site("the Elected Officials page "
                                     "lists a sixteenth name, Randy "
                                     "Treis, who does not appear in "
                                     "the Secretary of State's "
                                     "listing; the listing governs "
                                     "the elected roster and Treis "
                                     "is not recorded.")],
         "holders": [holder("Melissa Battah", "melissa-battah"),
                     holder("Tracy Ennis", "tracy-ennis"),
                     holder("J. Guy Isabelle", "j-guy-isabelle"),
                     holder("Donna Kelty", "donna-kelty"),
                     holder("Thomas F. Koch", "thomas-f-koch",
                            ballot_name="Thomas Koch"),
                     holder("Paul Malone", "paul-malone"),
                     holder("Dan Morrison", "dan-morrison"),
                     holder("Chris Parker", "chris-parker"),
                     holder("Dean Preston", "dean-preston"),
                     holder("Virginia Poplawski",
                            "virginia-poplawski"),
                     holder("Emily Wheeler Reynolds",
                            "emily-wheeler-reynolds"),
                     holder("Frederick Thumm", "frederick-thumm"),
                     holder("R. Lee Walther", "r-lee-walther"),
                     holder("Sheila Walther", "sheila-walther"),
                     holder("Jackie Wheeler", "jackie-wheeler")]},
    ],
    "jp_election": jp_election(
        "barre-03250", "barre-03250-vt", "Town of Barre", 15,
        "lists fifteen Barre Town justices of the peace for the "
        "2025-2026 term; they are the winners of the November 5, "
        "2024 election for the office. The listing publishes no "
        "vote totals and no party designations for justices of "
        "the peace."),
})

# ------------------------------------------------------------- Barton Town
BARTON_REPORT = {
    "url": "https://www.bartonvermont.com/",
    "note": "PLACEHOLDER",
}

def barton_report(what):
    return S(BARTON_REPORT, f"Town of Barton, Annual Report for the "
             f"year ending December 31, 2025, 'Elected Town "
             f"Officers -- For the Year 2025' table (report page "
             f"12), published on the town's official website: {what}")

BARTON_WARNING = {
    "url": "https://www.bartonvermont.com/",
    "note": "PLACEHOLDER",
}

def barton_warning(what):
    return S(BARTON_WARNING, f"Town of Barton, Warning for the "
             f"annual town meeting of March 3, 2026 (dated "
             f"January 23, 2026), published on the town's official "
             f"website: {what}")

SPECS.append({
    "label": "Town of Barton",
    "place": "barton-03550",
    "charter_note": "The Town of Barton has no municipal charter "
                    "in Title 24 Appendix V.S.A.; it is a "
                    "general-law town whose officers are elected "
                    "under 17 V.S.A. section 2646. The town's "
                    "annual report lists no elected listers or "
                    "auditors.",
    "offices": [
        {"slug": "selectboard", "title": "Selectboard Member",
         "org_name": "Barton Selectboard", "seats": 3,
         "sources": [barton_report("lists Selectboard members "
                                   "Denise 'Dee' McDowell (term "
                                   "expiring 2026), Jeff Cota (2027), "
                                   "and Ted Gattino (2028)."),
                     barton_warning("Article 1 lists the three-year "
                                    "selectboard seat held by "
                                    "McDowell for election at the "
                                    "March 3, 2026 annual meeting. "
                                    "No official source publishes "
                                    "the outcome, so her seat is "
                                    "not recorded as filled.")],
         "holders": [holder("Jeff Cota", "jeff-cota"),
                     holder("Ted Gattino", "ted-gattino")]},
        {"slug": "town-clerk", "title": "Town Clerk",
         "org_name": "Barton Town Clerk", "seats": 1,
         "sources": [guide("Barton", "lists Kristin Atwood as Town "
                            "Clerk of Barton."),
                     clerk_ss("Barton", "lists Kristin Atwood as "
                              "Town Clerk of Barton."),
                     barton_report("lists 'Clerk: Kristin M. Atwood' "
                                   "with a term expiring 2028; the "
                                   "town's Report of Annual Meeting "
                                   "2025 records her elected to a "
                                   "three-year term as Town Clerk.")],
         "holders": [holder("Kristin Atwood", "kristin-atwood")]},
        {"slug": "town-treasurer", "title": "Town Treasurer",
         "org_name": "Barton Town Treasurer", "seats": 1,
         "sources": [guide("Barton", "lists Kristin Atwood as Town "
                            "Treasurer of Barton."),
                     barton_report("lists 'Treasurer: Kristin M. "
                                   "Atwood' with a term expiring "
                                   "2028; the town's Report of "
                                   "Annual Meeting 2025 records her "
                                   "elected to a three-year term as "
                                   "Treasurer, separately from the "
                                   "clerkship. The Secretary of "
                                   "State's treasurer contact "
                                   "spreadsheet prints no Barton "
                                   "treasurer ('Contact Town Clerk "
                                   "for more information').")],
         "holders": [holder("Kristin Atwood", "kristin-atwood")]},
        {"slug": "collector-of-taxes", "title": "Tax Collector",
         "org_name": "Barton Tax Collector", "seats": 1,
         "sources": [barton_report("lists 'Tax Collector: Shelia "
                                   "Martin' with a term expiring "
                                   "2028 among the town's elected "
                                   "officers.")],
         "holders": [holder("Shelia Martin", "shelia-martin")]},
        {"slug": "moderator", "title": "Moderator",
         "org_name": "Barton Town Moderator", "seats": 1,
         "sources": [statute2646("a moderator"),
                     barton_report("lists 'Moderator: Jesse Coe' "
                                   "with a term expiring 2026."),
                     barton_warning("Article 1 lists the moderator "
                                    "election at the March 3, 2026 "
                                    "annual meeting with Coe as "
                                    "incumbent. No official source "
                                    "publishes the outcome, so no "
                                    "holder is recorded.")]},
        {"slug": "first-constable", "title": "First Constable",
         "org_name": "Barton First Constable", "seats": 1,
         "sources": [barton_report("lists 'First Constable: Tom "
                                   "Lowell' with a term expiring "
                                   "2026."),
                     barton_warning("Article 1 lists the first "
                                    "constable election at the "
                                    "March 3, 2026 annual meeting "
                                    "with Lowell as incumbent. No "
                                    "official source publishes the "
                                    "outcome, so no holder is "
                                    "recorded.")]},
        {"slug": "grand-juror", "title": "Grand Juror",
         "org_name": "Barton Grand Juror", "seats": 1,
         "sources": [statute2646("a grand juror"),
                     barton_report("shows the grand juror office "
                                   "as 'Vacant.'"),
                     barton_warning("Article 1 lists the grand "
                                    "juror office as vacant for the "
                                    "March 3, 2026 annual meeting.")]},
        {"slug": "town-agent", "title": "Town Agent",
         "org_name": "Barton Town Agent", "seats": 1,
         "sources": [statute2646("a town agent to prosecute and "
                                 "defend suits"),
                     barton_report("shows the town agent office "
                                   "with no name (vacant)."),
                     barton_warning("Article 1 lists the town agent "
                                    "office as vacant for the "
                                    "March 3, 2026 annual meeting.")]},
        {"slug": "justice-of-the-peace", "title": "Justice of the Peace",
         "org_name": "Barton Justices of the Peace", "seats": 8,
         "sources": [jp_src("Barton", "lists eight Barton justices "
                             "of the peace. The listing spells the "
                             "name 'Sheila Martin'; the Barton "
                             "Village officers page and the town "
                             "report spell the same officeholder's "
                             "name 'Shelia Martin,' which is the "
                             "form recorded for the person.")],
         "holders": [holder("Lawrence Burdick", "lawrence-burdick"),
                     holder("Gerry Cahill", "gerry-cahill"),
                     holder("Cassandra Griffin",
                            "cassandra-griffin"),
                     holder("Beth Martin", "beth-martin"),
                     holder("Shelia Martin", "shelia-martin",
                            ballot_name="Sheila Martin"),
                     holder("Jodi Morley", "jodi-morley"),
                     holder("Anthony Pallotta", "anthony-pallotta"),
                     holder("Eliza Walters", "eliza-walters")]},
    ],
    "jp_election": jp_election(
        "barton-03550", "barton-03550-vt", "Town of Barton", 8,
        "lists eight Barton justices of the peace for the "
        "2025-2026 term; they are the winners of the November 5, "
        "2024 election for the office. The listing publishes no "
        "vote totals and no party designations for justices of "
        "the peace."),
})

# ---------------------------------------------------------- Barton Village
BARTON_VILLAGE_PAGE = {
    "url": "https://www.bartonvillagevt.gov/village-officers/",
    "note": "PLACEHOLDER",
}

def barton_village_page(what):
    return S(BARTON_VILLAGE_PAGE, f"Village of Barton official "
             f"website, Village Officers page: {what}")

MARTIN_VILLAGE_SOURCES = [barton_village_page(
    "lists Shelia Martin as Village Clerk, Village Treasurer, "
    "and Delinquent Tax Collector, each with a term expiring "
    "March 2027.")]

SPECS.append({
    "label": "Village of Barton",
    "place": "barton",
    "charter_note": "The Village of Barton has no municipal "
                    "charter chapter in Title 24 Appendix V.S.A.; "
                    "it is a general-law incorporated village.",
    "offices": [
        {"slug": "trustee", "title": "Trustee",
         "org_name": "Barton Village Board of Trustees", "seats": 3,
         "sources": [barton_village_page("lists the Board of "
                                   "Trustees: Regina Lyon (Chair), "
                                   "Marilyn Prue, and Ellis "
                                   "Merchant.")],
         "holders": [holder("Regina Lyon", "regina-lyon"),
                     holder("Marilyn Prue", "marilyn-prue"),
                     holder("Ellis Merchant", "ellis-merchant")]},
        {"slug": "village-clerk", "title": "Village Clerk",
         "org_name": "Barton Village Clerk", "seats": 1,
         "sources": MARTIN_VILLAGE_SOURCES,
         "holders": [holder("Shelia Martin", "shelia-martin",
                            person_scope="barton-03550")]},
        {"slug": "village-treasurer", "title": "Village Treasurer",
         "org_name": "Barton Village Treasurer", "seats": 1,
         "sources": MARTIN_VILLAGE_SOURCES,
         "holders": [holder("Shelia Martin", "shelia-martin",
                            person_scope="barton-03550")]},
        {"slug": "collector-of-delinquent-taxes",
         "title": "Collector of Delinquent Taxes",
         "org_name": "Barton Village Collector of Delinquent Taxes",
         "seats": 1,
         "sources": MARTIN_VILLAGE_SOURCES,
         "holders": [holder("Shelia Martin", "shelia-martin",
                            person_scope="barton-03550")]},
    ],
})

# ------------------------------------------------------------ Bellows Falls
CH207 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/207",
    "note": "PLACEHOLDER",
}
BF_TRUSTEES_PAGE = {
    "url": "https://www.rockinghamvt.org/villagetrustees",
    "note": "PLACEHOLDER",
}
BF_MINUTES = {
    "url": "https://www.rockinghamvt.org/",
    "note": "PLACEHOLDER",
}

def ch207(what):
    return S(CH207, f"Village of Bellows Falls charter, 24 App. "
             f"V.S.A. ch. 207 (official text, Vermont General "
             f"Assembly): {what}")

def bf_minutes(what):
    return S(BF_MINUTES, f"Village of Bellows Falls annual meeting "
             f"minutes, May 18, 2026, published on the Town of "
             f"Rockingham / Village of Bellows Falls website "
             f"(Agendas and Minutes, 2026): {what}")

BF_BOARD_SOURCES = [
    ch207("section 5 provides for a President and four Trustees, "
          "elected at the annual meeting; by section 7 the "
          "President is a member of the Board of Trustees and "
          "presides over it."),
    bf_minutes("the 'Present' list names Paul Obuchowski, "
               "Village President, and Wade Masure, Taylor "
               "Pichette, Samantha Snow, and Jonathan Wright, "
               "Trustees."),
    S(BF_TRUSTEES_PAGE, "Village of Bellows Falls, Village "
                        "Trustees page (Town of Rockingham "
                        "website): lists Wade Masure, Taylor "
                        "Pichette, and Samantha Snow as Trustees "
                        "but still shows Wendy M. Levy as Village "
                        "President and Jeff Dunbar as a Trustee. "
                        "The attested minutes of the May 18, 2026 "
                        "annual meeting govern; Levy and Dunbar "
                        "are not recorded."),
]

SPECS.append({
    "label": "Village of Bellows Falls",
    "place": "bellows-falls",
    "charter_note": "The Village of Bellows Falls is governed by "
                    "its charter, 24 App. V.S.A. ch. 207: the "
                    "officers are a Moderator, a President, a "
                    "Clerk, a Treasurer, a Collector of Taxes, "
                    "four Trustees, and three Auditors of "
                    "Accounts, all elected at the annual meeting "
                    "except the Collector of Taxes, whom the "
                    "Trustees appoint (section 5). The village "
                    "lies within the Town of Rockingham.",
    "offices": [
        {"slug": "president", "title": "Village President",
         "org_name": "Bellows Falls Village Board of Trustees",
         "seats": 1, "org_key": "bellows-falls-vt/board-of-trustees",
         "org_sources": BF_BOARD_SOURCES,
         "sources": BF_BOARD_SOURCES,
         "holders": [holder("Paul Obuchowski", "paul-obuchowski")]},
        {"slug": "trustee", "title": "Trustee",
         "org_name": "Bellows Falls Village Board of Trustees",
         "seats": 4, "org_key": "bellows-falls-vt/board-of-trustees",
         "org_sources": BF_BOARD_SOURCES,
         "sources": BF_BOARD_SOURCES,
         "holders": [holder("Wade Masure", "wade-masure"),
                     holder("Taylor Pichette", "taylor-pichette"),
                     holder("Samantha Snow", "samantha-snow"),
                     holder("Jonathan Wright", "jonathan-wright")]},
        {"slug": "village-clerk", "title": "Village Clerk",
         "org_name": "Bellows Falls Village Clerk", "seats": 1,
         "sources": [ch207("section 5 provides for a Clerk, "
                           "elected at the annual meeting."),
                     bf_minutes("the 'Present' list names Kathleen "
                                "Kelly, Village Clerk; she attests "
                                "the minutes as Village Clerk. "
                                "Kelly is also the Rockingham Town "
                                "Clerk.")],
         "holders": [holder("Kathleen Kelly", "kathleen-kelly")]},
        {"slug": "moderator", "title": "Moderator",
         "org_name": "Bellows Falls Village Moderator", "seats": 1,
         "sources": [ch207("section 5 provides for a Moderator, "
                           "elected at the annual meeting; section "
                           "9 states the Moderator's duties."),
                     bf_minutes("the 'Present' list names Dennis "
                                "Harty, Moderator, and the minutes "
                                "are approved over his name as "
                                "Moderator.")],
         "holders": [holder("Dennis Harty", "dennis-harty")]},
        {"slug": "village-treasurer", "title": "Village Treasurer",
         "org_name": "Bellows Falls Village Treasurer", "seats": 1,
         "sources": [ch207("section 5 provides for a Treasurer, "
                           "elected at the annual meeting. No "
                           "village page names the current "
                           "Treasurer, so no holder is recorded.")]},
        {"slug": "auditor", "title": "Auditor of Accounts",
         "org_name": "Bellows Falls Village Auditors of Accounts",
         "seats": 3,
         "sources": [ch207("section 5 provides for three Auditors "
                           "of Accounts, elected at the annual "
                           "meeting; section 11 states their "
                           "duties. No village page names the "
                           "current auditors, so no holders are "
                           "recorded.")]},
        {"slug": "collector-of-taxes", "title": "Collector of Taxes",
         "org_name": "Bellows Falls Village Collector of Taxes",
         "seats": 1,
         "sources": [ch207("section 5 provides for a Collector of "
                           "Taxes, appointed by the Board of "
                           "Trustees under section 5(b). No village "
                           "page names the current Collector, so "
                           "no holder is recorded.")]},
    ],
})

# --------------------------------------------------------------- Belvidere
BELV_HOME = {
    "url": "https://townofbelviderevt.com/",
    "note": "PLACEHOLDER",
}
BELV_SB = {
    "url": "https://townofbelviderevt.com/select-board/",
    "note": "PLACEHOLDER",
}
BELV_LISTERS = {
    "url": "https://townofbelviderevt.com/listers-and-appraisals/",
    "note": "PLACEHOLDER",
}
BELV_MINUTES = {
    "url": "https://townofbelviderevt.com/wp-content/uploads/2026/03/03-04-26-Signed-TM-Minutes.pdf",
    "note": "PLACEHOLDER",
}

def belv_home(what):
    return S(BELV_HOME, f"Town of Belvidere official website, "
             f"homepage 'Elected Town Positions' listing: {what}")

SPECS.append({
    "label": "Town of Belvidere",
    "place": "belvidere",
    "charter_note": "The Town of Belvidere has no municipal "
                    "charter in Title 24 Appendix V.S.A.; it is a "
                    "general-law town whose officers are elected "
                    "under 17 V.S.A. section 2646.",
    "offices": [
        {"slug": "selectboard", "title": "Selectboard Member",
         "org_name": "Belvidere Selectboard", "seats": 3,
         "sources": [sb_dir("Belvidere", "lists three Belvidere "
                            "Selectboard members: Kenneth Adams, "
                            "Jr., Earl Domina, Jr. (Chair), and "
                            "Kevin Leavitt."),
                     S(BELV_SB, "Town of Belvidere official "
                                "website, Select Board page: lists "
                                "Earl Domina, Jr. (Chair), Ken "
                                "Adams, Jr., and Kevin Leavitt.")],
         "holders": [holder("Earl Domina Jr.", "earl-domina-jr"),
                     holder("Kenneth Adams Jr.", "kenneth-adams-jr"),
                     holder("Kevin Leavitt", "kevin-leavitt")]},
        {"slug": "town-clerk", "title": "Town Clerk",
         "org_name": "Belvidere Town Clerk", "seats": 1,
         "sources": [guide("Belvidere", "lists Cathy Mander-Adams "
                            "as Town Clerk of Belvidere."),
                     clerk_ss("Belvidere", "lists Cathy "
                              "Mander-Adams as Town Clerk of "
                              "Belvidere."),
                     belv_home("lists 'Town Clerk & Treasurer / "
                               "Cathy Mander-Adams' among the "
                               "town's elected positions."),
                     S(BELV_MINUTES, "Town of Belvidere, Town "
                                     "Meeting minutes, March 3, "
                                     "2026: record Cathy "
                                     "Mander-Adams elected Town "
                                     "Clerk by voice vote.")],
         "holders": [holder("Cathy Mander-Adams",
                            "cathy-mander-adams")]},
        {"slug": "town-treasurer", "title": "Town Treasurer",
         "org_name": "Belvidere Town Treasurer", "seats": 1,
         "sources": [guide("Belvidere", "lists Cathy Mander-Adams "
                            "as Town Treasurer of Belvidere."),
                     belv_home("lists 'Town Clerk & Treasurer / "
                               "Cathy Mander-Adams' among the "
                               "town's elected positions."),
                     S(BELV_MINUTES, "Town of Belvidere, Town "
                                     "Meeting minutes, March 3, "
                                     "2026: record Cathy "
                                     "Mander-Adams elected Town "
                                     "Treasurer by voice vote. The "
                                     "Secretary of State's "
                                     "treasurer contact spreadsheet "
                                     "prints no Belvidere treasurer "
                                     "('Contact Town Clerk for more "
                                     "information').")],
         "holders": [holder("Cathy Mander-Adams",
                            "cathy-mander-adams")]},
        {"slug": "moderator", "title": "Moderator",
         "org_name": "Belvidere Town Moderator", "seats": 1,
         "sources": [belv_home("lists 'Moderator / Pamela McKenna' "
                               "among the town's elected "
                               "positions.")],
         "holders": [holder("Pamela McKenna", "pamela-mckenna")]},
        {"slug": "lister", "title": "Lister",
         "org_name": "Belvidere Board of Listers", "seats": 3,
         "sources": [S(BELV_LISTERS, "Town of Belvidere official "
                                "website, Listers and Appraisals "
                                "page: lists Stacey Chase, "
                                "Stephanie Domina, and Richard "
                                "Schoon as the town's listers.")],
         "holders": [holder("Stacey Chase", "stacey-chase"),
                     holder("Stephanie Domina", "stephanie-domina"),
                     holder("Richard Schoon", "richard-schoon")]},
        {"slug": "auditor", "title": "Auditor",
         "org_name": "Belvidere Town Auditors", "seats": 3,
         "sources": [belv_home("lists 'Auditors / William McLean; "
                               "Gary Edmonds; Pamela McKenna' among "
                               "the town's elected positions.")],
         "holders": [holder("William McLean", "william-mclean"),
                     holder("Gary Edmonds", "gary-edmonds"),
                     holder("Pamela McKenna", "pamela-mckenna")]},
        {"slug": "road-commissioner", "title": "Road Commissioner",
         "org_name": "Belvidere Road Commissioner", "seats": 1,
         "sources": [belv_home("lists 'Road Commissioner / Kevin "
                               "Leavitt' among the town's elected "
                               "positions.")],
         "holders": [holder("Kevin Leavitt", "kevin-leavitt")]},
        {"slug": "collector-of-delinquent-taxes",
         "title": "Collector of Delinquent Taxes",
         "org_name": "Belvidere Collector of Delinquent Taxes",
         "seats": 1,
         "sources": [belv_home("lists 'Collector of Delinquent "
                               "Taxes / Mary Hysick' among the "
                               "town's elected positions (17 V.S.A. "
                               "section 2651d).")],
         "holders": [holder("Mary Hysick", "mary-hysick")]},
        {"slug": "first-constable", "title": "First Constable",
         "org_name": "Belvidere First Constable", "seats": 1,
         "sources": [belv_home("lists 'First Constable / Stacey "
                               "Chase' among the town's elected "
                               "positions.")],
         "holders": [holder("Stacey Chase", "stacey-chase")]},
        {"slug": "second-constable", "title": "Second Constable",
         "org_name": "Belvidere Second Constable", "seats": 1,
         "sources": [belv_home("lists 'Second Constable / Stephen "
                               "Brown' among the town's elected "
                               "positions.")],
         "holders": [holder("Stephen Brown", "stephen-brown")]},
        {"slug": "grand-juror", "title": "Grand Juror",
         "org_name": "Belvidere Grand Juror", "seats": 1,
         "sources": [statute2646("a grand juror"),
                     belv_home("does not list a grand juror, and "
                               "no other official source publishes "
                               "the holder.")]},
        {"slug": "town-agent", "title": "Town Agent",
         "org_name": "Belvidere Town Agent", "seats": 1,
         "sources": [statute2646("a town agent to prosecute and "
                                 "defend suits"),
                     belv_home("does not list a town agent, and "
                               "no other official source publishes "
                               "the holder.")]},
        {"slug": "justice-of-the-peace", "title": "Justice of the Peace",
         "org_name": "Belvidere Justices of the Peace", "seats": 5,
         "sources": [jp_src("Belvidere", "lists five Belvidere "
                             "justices of the peace. The town "
                             "website's own justice listing names "
                             "three of them with variant forms "
                             "('Andy Iwaskiewicz', 'Stephanie "
                             "Draper', 'Thad Tallman'); the "
                             "Secretary of State's listing governs, "
                             "and its 'Stephanie Domina' is the "
                             "town lister of that name (the town "
                             "site's 'Draper' is her other "
                             "surname).")],
         "holders": [holder("Cathy Mander-Adams",
                            "cathy-mander-adams"),
                     holder("Stephanie Domina", "stephanie-domina"),
                     holder("Thad Tallman", "thad-tallman"),
                     holder("Stephen Brown", "stephen-brown"),
                     holder("Andrew Iwaskiewicz",
                            "andrew-iwaskiewicz")]},
    ],
    "jp_election": jp_election(
        "belvidere", "belvidere-vt", "Town of Belvidere", 5,
        "lists five Belvidere justices of the peace for the "
        "2025-2026 term (Cathy Mander-Adams, Stephanie Domina, "
        "Thad Tallman, Stephen Brown, Andrew Iwaskiewicz); they "
        "are the winners of the November 5, 2024 election for the "
        "office. The listing publishes no vote totals and no "
        "party designations for justices of the peace."),
})

# -------------------------------------------------------------- Bennington
CH103 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/103",
    "note": "PLACEHOLDER",
}
BENN_PAGE = {
    "url": "https://benningtonvt.org/government/index.php",
    "note": "PLACEHOLDER",
}

def ch103(what):
    return S(CH103, f"Town of Bennington charter, 24 App. V.S.A. "
             f"ch. 103 (official text, Vermont General Assembly): "
             f"{what}")

def benn_page(what):
    return S(BENN_PAGE, f"Town of Bennington official website, "
             f"'Elected Officials' page: {what}")

SPECS.append({
    "label": "Town of Bennington",
    "place": "bennington",
    "charter_note": "The Town of Bennington is governed by its "
                    "charter, 24 App. V.S.A. ch. 103: the elective "
                    "officers are seven Select Board members, a "
                    "Town Clerk, a Treasurer, and a Moderator "
                    "(section 201), each for a three-year term. "
                    "The charter makes the Constable and the "
                    "Listers appointive (section 202), assigns "
                    "the delinquent-tax collector's duties to "
                    "the Town Manager (section 404), and the "
                    "Town Agent's duties to the Select Board "
                    "(section 303), so no posts are created for "
                    "those offices.",
    "offices": [
        {"slug": "selectboard", "title": "Selectboard Member",
         "org_name": "Bennington Select Board", "seats": 7,
         "sources": [ch103("section 201(a) provides for seven "
                           "Select Board members elected from the "
                           "Town at large."),
                     benn_page("lists the Select Board: Tom Haley "
                               "(Chair), Jim Sullivan (Vice "
                               "Chair), Clark Adams, Jackie Matts, "
                               "Sarah Perrin, Nancy White, and Ed "
                               "Woods. The Secretary of State's "
                               "Selectboard Members directory "
                               "publishes no Bennington roster.")],
         "holders": [holder("Tom Haley", "tom-haley",
                            ballot_name="Tom Haley III"),
                     holder("Jim Sullivan", "jim-sullivan"),
                     holder("Clark Adams", "clark-adams"),
                     holder("Jackie Matts", "jackie-matts"),
                     holder("Sarah Perrin", "sarah-perrin"),
                     holder("Nancy White", "nancy-white"),
                     holder("Ed Woods", "ed-woods")]},
        {"slug": "town-clerk", "title": "Town Clerk",
         "org_name": "Bennington Town Clerk", "seats": 1,
         "sources": [ch103("section 201(a) makes the Town Clerk an "
                           "elective officer."),
                     benn_page("lists 'Town of Bennington: "
                               "Cassandra Barbeau' as Town Clerk. "
                               "The Secretary of State's Guide "
                               "(January 2026) and clerk contact "
                               "spreadsheet (June 12, 2026) list "
                               "Kayla Thompson, whom the town's "
                               "current page supersedes; Thompson "
                               "is not recorded.")],
         "holders": [holder("Cassandra Barbeau",
                            "cassandra-barbeau")]},
        {"slug": "town-treasurer", "title": "Town Treasurer",
         "org_name": "Bennington Town Treasurer", "seats": 1,
         "sources": [ch103("section 201(a) makes the Treasurer an "
                           "elective officer."),
                     benn_page("lists 'Town of Bennington: Joan "
                               "Pinsonneault' as Town Treasurer."),
                     guide("Bennington", "lists Joan Pinsonneault "
                           "as Town Treasurer of Bennington. The "
                           "Secretary of State's treasurer contact "
                           "spreadsheet prints no Bennington "
                           "treasurer ('Contact Town Clerk for more "
                           "information').")],
         "holders": [holder("Joan Pinsonneault",
                            "joan-pinsonneault")]},
        {"slug": "moderator", "title": "Moderator",
         "org_name": "Bennington Town Moderator", "seats": 1,
         "sources": [ch103("section 201(a) makes the Moderator an "
                           "elective officer. No town page names "
                           "the current Moderator (the town's "
                           "Government, Town Meetings, Elections, "
                           "and Election Results pages were all "
                           "checked), so no holder is recorded.")]},
        {"slug": "justice-of-the-peace", "title": "Justice of the Peace",
         "org_name": "Bennington Justices of the Peace", "seats": 15,
         "sources": [jp_src("Bennington", "lists fifteen "
                             "Bennington justices of the peace.")],
         "holders": [holder("Barbara Bluto", "barbara-bluto"),
                     holder("William Greer", "william-greer",
                            ballot_name="William Greer",
                            existing_person_id="ocd-person/a1feb2f2-1ca5-500e-b1bd-09e02781839c"),
                     holder("Tom Haley", "tom-haley",
                            ballot_name="Tom Haley III"),
                     holder("Michele Hogan", "michele-hogan"),
                     holder("Jeannie Jenkins", "jeannie-jenkins"),
                     holder("Albert Krawczyk", "albert-krawczyk"),
                     holder("Vickie Lampron", "vickie-lampron"),
                     holder("Bruce Lee-Clark", "bruce-lee-clark"),
                     holder("Brian \"BJ\" Maroney Jr",
                            "brian-bj-maroney-jr",
                            ballot_name="Brian \"BJ\" Maroney Jr"),
                     holder("James H. Marsden", "james-h-marsden"),
                     holder("Mary A. Morrissey", "mary-a-morrissey",
                            existing_person_id="ocd-person/0a067bcb-48c5-5972-9775-83b809d15cf0"),
                     holder("Cindy Murray", "cindy-murray"),
                     holder("Joan Pinsonneault",
                            "joan-pinsonneault"),
                     holder("Justine Scanlon", "justine-scanlon"),
                     holder("David Shaffe", "david-shaffe")]},
    ],
    "jp_election": jp_election(
        "bennington", "bennington-vt", "Town of Bennington", 15,
        "lists fifteen Bennington justices of the peace for the "
        "2025-2026 term; they are the winners of the November 5, "
        "2024 election for the office. The listing publishes no "
        "vote totals and no party designations for justices of "
        "the peace."),
})

# ------------------------------------------------------------------ Benson
BENSON_SITE = {
    "url": "https://bensonvermont.gov/",
    "note": "PLACEHOLDER",
}

def benson_site(what):
    return S(BENSON_SITE, f"Town of Benson official website "
             f"(bensonvermont.gov): {what}")

SPECS.append({
    "label": "Town of Benson",
    "place": "benson",
    "charter_note": "The Town of Benson has no municipal charter "
                    "in Title 24 Appendix V.S.A.; it is a "
                    "general-law town whose officers are elected "
                    "under 17 V.S.A. section 2646.",
    "offices": [
        {"slug": "selectboard", "title": "Selectboard Member",
         "org_name": "Benson Selectboard", "seats": 5,
         "sources": [sb_dir("Benson", "lists five Benson "
                            "Selectboard members: Brad Barrett "
                            "(Chair), Benjamin Bartholomew, Daryl "
                            "Burlett, Guy Charlton (Vice Chair), "
                            "and James Pritchard.")],
         "holders": [holder("Brad Barrett", "brad-barrett"),
                     holder("Benjamin Bartholomew",
                            "benjamin-bartholomew"),
                     holder("Daryl Burlett", "daryl-burlett"),
                     holder("Guy Charlton", "guy-charlton"),
                     holder("James Pritchard", "james-pritchard")]},
        {"slug": "town-clerk", "title": "Town Clerk",
         "org_name": "Benson Town Clerk", "seats": 1,
         "sources": [guide("Benson", "lists Heidi Chandler as Town "
                            "Clerk of Benson."),
                     clerk_ss("Benson", "lists Heidi Chandler as "
                              "Town Clerk of Benson."),
                     benson_site("'Town Office Notes' post "
                                 "(December 30, 2025) is signed "
                                 "'Heidi Chandler, Clerk/Treasurer.' "
                                 "Benson combines the clerk and "
                                 "treasurer offices in one elected "
                                 "position.")],
         "holders": [holder("Heidi Chandler", "heidi-chandler")]},
        {"slug": "town-treasurer", "title": "Town Treasurer",
         "org_name": "Benson Town Treasurer", "seats": 1,
         "sources": [guide("Benson", "lists Heidi Chandler as Town "
                            "Treasurer of Benson."),
                     treas_ss("Benson", "lists Heidi Chandler as "
                              "Town Treasurer of Benson."),
                     benson_site("'Town Office Notes' post "
                                 "(December 30, 2025) is signed "
                                 "'Heidi Chandler, Clerk/Treasurer.' "
                                 "Benson combines the clerk and "
                                 "treasurer offices in one elected "
                                 "position.")],
         "holders": [holder("Heidi Chandler", "heidi-chandler")]},
        {"slug": "moderator", "title": "Moderator",
         "org_name": "Benson Town Moderator", "seats": 1,
         "sources": [statute2646("a moderator"),
                     benson_site("the 'Benson Open Seats 2025' "
                                 "post (December 28, 2024) lists "
                                 "John Hill as the incumbent "
                                 "Moderator, and the 'Offices and "
                                 "Candidates for March 3, 2026' "
                                 "post (February 20, 2026) lists "
                                 "him as the candidate for the "
                                 "office. The town publishes no "
                                 "results for the March 2026 town "
                                 "meeting, so no holder is "
                                 "recorded.")]},
        {"slug": "lister", "title": "Lister",
         "org_name": "Benson Board of Listers", "seats": 3,
         "sources": [benson_site("the Municipal Administration "
                                 "page names 'Lois Trenn, Gina "
                                 "Parker and Ed Peltier' as the "
                                 "town's listers. The 'Benson Open "
                                 "Seats 2025' post marks Gina "
                                 "Parker's lister seat '(Appointed)'; "
                                 "her membership is recorded as "
                                 "appointed, the others as elected.")],
         "holders": [holder("Lois Trenn", "lois-trenn"),
                     holder("Gina Parker", "gina-parker",
                            how_seated="appointed"),
                     holder("Ed Peltier", "ed-peltier")]},
        {"slug": "auditor", "title": "Auditor",
         "org_name": "Benson Town Auditors", "seats": 3,
         "sources": [statute2646("auditors"),
                     benson_site("the 'Benson Open Seats 2025' "
                                 "post lists Robert Bizek as the "
                                 "incumbent auditor for the seat "
                                 "filled in 2025, and the February "
                                 "2026 candidates post lists Lynn "
                                 "Bowen as the candidate for the "
                                 "seat filled in 2026. The town "
                                 "publishes no town-meeting "
                                 "results, so no holders are "
                                 "recorded.")]},
        {"slug": "collector-of-delinquent-taxes",
         "title": "Collector of Delinquent Taxes",
         "org_name": "Benson Collector of Delinquent Taxes",
         "seats": 1,
         "sources": [benson_site("the 'Benson Open Seats 2025' "
                                 "post lists Barbara Burlett as "
                                 "the incumbent Delinquent Tax "
                                 "Collector, and the February 2026 "
                                 "candidates post lists her as "
                                 "the candidate for the office "
                                 "(17 V.S.A. section 2651d). The "
                                 "town publishes no results for "
                                 "the March 2026 town meeting, so "
                                 "no holder is recorded.")]},
        {"slug": "trustee-of-public-funds",
         "title": "Trustee of Public Funds",
         "org_name": "Benson Trustees of Public Funds", "seats": 3,
         "sources": [benson_site("the town's open-seats posts "
                                 "show one Trustee of Public Funds "
                                 "seat filled each year for a "
                                 "three-year term (incumbents "
                                 "Jayme Van Noort Purdy in 2024 "
                                 "and Brad Barrett in 2025; Carrie "
                                 "Lafond was the candidate in "
                                 "2026). The town publishes no "
                                 "town-meeting results, so no "
                                 "holders are recorded.")]},
        {"slug": "grand-juror", "title": "Grand Juror",
         "org_name": "Benson Grand Juror", "seats": 1,
         "sources": [statute2646("a grand juror"),
                     benson_site("lists no grand juror, and no "
                                 "other official source publishes "
                                 "the holder.")]},
        {"slug": "town-agent", "title": "Town Agent",
         "org_name": "Benson Town Agent", "seats": 1,
         "sources": [statute2646("a town agent to prosecute and "
                                 "defend suits"),
                     benson_site("lists no town agent, and no "
                                 "other official source publishes "
                                 "the holder.")]},
        {"slug": "justice-of-the-peace", "title": "Justice of the Peace",
         "org_name": "Benson Justices of the Peace", "seats": 5,
         "sources": [jp_src("Benson", "lists five Benson justices "
                             "of the peace.")],
         "holders": [holder("Lynn Bowen", "lynn-bowen"),
                     holder("John Hill", "john-hill"),
                     holder("Lauren Mohan", "lauren-mohan"),
                     holder("Ed Peltier", "ed-peltier"),
                     holder("Eric L. Shaw", "eric-l-shaw")]},
    ],
    "jp_election": jp_election(
        "benson", "benson-vt", "Town of Benson", 5,
        "lists five Benson justices of the peace for the 2025-2026 "
        "term (Lynn Bowen, John Hill, Lauren Mohan, Ed Peltier, "
        "Eric L. Shaw); they are the winners of the November 5, "
        "2024 election for the office. The listing publishes no "
        "vote totals and no party designations for justices of "
        "the peace."),
})


def main():
    for spec in SPECS:
        place = spec["place"]
        out = {
            "label": spec["label"],
            "place_slug": place,
            "jurisdiction_id": "ocd-jurisdiction/country:us/state:vt/"
                               f"place:{place}/government",
            "header": f"# {spec['label']} municipal roster backfill "
                      f"-- Vermont\n# municipal fan-out batch 2; "
                      f"issue #163 (VT master tracking).\n",
            "offices": spec["offices"],
        }
        if "jp_election" in spec:
            out["jp_election"] = spec["jp_election"]
        path = OUT / f"{place}.json"
        path.write_text(json.dumps(out, indent=1, ensure_ascii=False))
        print("wrote", path)


if __name__ == "__main__":
    main()
