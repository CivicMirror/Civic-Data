#!/usr/bin/env python3
"""Batch 22 of the VT #163 municipal fan-out (alphabetical positions
210-219): St. Albans Town, St. Albans City, St. George, St.
Johnsbury, Stamford, Stannard, Starksboro, Stockbridge, Stowe,
Strafford. Emits one JSON spec per municipality for
build_vt_municipality.py. Research: vt_muni_batch22_research.md.

Identity calls baked into this batch (all flagged on #163):
- St. Albans Town Selectboard Chair and JP John "Jack" Brigham is
  the sitting State Representative for Franklin-8 (the district is
  St. Albans Town and Swanton), appointed to the House seat by
  Governor Scott on February 20, 2026: both holder entries reuse
  the state-tier person record
  ocd-person/d351e830-660f-58d4-a8e8-3e61ced2d12d, and his JP
  candidacy is appended to that record by hand after the build
  (Emmons pattern).
- St. Albans City JP Joe Luneau is the sitting State
  Representative for Franklin-3 (St. Albans City and part of St.
  Albans Town): his JP holder entry reuses
  ocd-person/5e90b3cb-93f9-5d2d-abdc-70b8b70c2407, identity
  verified by the listing's jluneau@handycars.com address (his
  St. Albans dealership), and his JP candidacy is appended to
  that record by hand after the build.
- St. Albans City Ward 5 Councilor Erik Johnson is a DIFFERENT
  person from Jericho's selectboard member of the same name; the
  builder suffixes the new person file automatically.
- St. Albans Town elects FIFTEEN justices of the peace, not
  eight: the certified listing's town block continues across a
  page break (seven unlabeled rows), and the town's Board of
  Civil Authority page states the board consists of 15 justices
  and names 14 of them. Bryan Deslauriers, though a certified
  winner, is omitted from the town's BCA roster while remaining
  Selectboard Vice Chair; he is excluded from the JP holders
  entirely (departed-winner pattern) and the election note tells
  the story.
- St. Albans Town's Chelsea Mulheron holds the selectboard seat
  the FY 2025 report and the June 2026 SOS directory give to
  Amanda Headley (term to 2027): the town's current Selectboard
  page names Mulheron with the same 2027 expiry, a
  post-directory vacancy appointment; she is seated APPOINTED
  and Headley is not minted.
- St. Johnsbury Moderator David Reynolds is APPOINTED: the
  town's 2025 annual report files him under Appointed Officials,
  a classification ch. 151 sec. 201(a) permits when the town has
  so voted. The town's elected cemetery commissioners are built
  ELECTED although ch. 151 sec. 201 does not enumerate the
  office: the charter is silent on cemeteries, so 18 V.S.A.
  sec. 5373 and the town's continuing elected practice govern.
- Stockbridge Town Clerk and Town Treasurer Jill Gifford is
  APPOINTED to both offices (the town report's Appointed Town
  Officials table).
- St. George Town Clerk Lisa Laramee and Town Treasurer
  Adam Beach are seated APPOINTED: the town's 2025 town
  meeting minutes introduce both as hired staff ('hired
  September 2023' / 'hired October 2024'), and Beach also
  holds the delinquent tax collectorship as an appointee.
  St. George's Asher Menashe won the fifth selectboard seat
  on March 3, 2026, but the town's September 2026 contact
  list names only four members and the seat stands vacant;
  he is not seated.
- Starksboro Town Treasurer Alexandra Thompson is APPOINTED:
  the town's elected-officials listing and its 2026 ballot both
  omit the office while she serves in it.
- Starksboro elects its Planning Commission (24 V.S.A.
  sec. 4323): seven seats are derived from the 2022-2023 town
  report's seven roster lines (disclosed in the sources).
- Stamford Moderator John Paul Potvin and Lister Kristin
  Malachuk are write-in winners NAMED in the town's official
  March 3, 2026 results tally, minted ELECTED (the Norwich Gere
  pattern).
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
CHARTER_011 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/011",
    "note": "PLACEHOLDER",
}
CHARTER_150 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/150",
    "note": "PLACEHOLDER",
}
CHARTER_151 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/151",
    "note": "PLACEHOLDER",
}
CHARTER_153 = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/153",
    "note": "PLACEHOLDER",
}
SACITY_COUNCIL = {"url": "https://www.stalbansvt.com/government/mayor___city_council/index.php",
                  "note": "PLACEHOLDER"}
SACITY_CLERK = {"url": "https://www.stalbansvt.com/government/city_clerk/index.php",
                "note": "PLACEHOLDER"}
SATOWN_REPORT = {"url": "https://cms7files.revize.com/stalbansvt/Town%20Report%20FY%202025.pdf",
                 "note": "PLACEHOLDER"}
SATOWN_RESULTS = {"url": "https://cms7files.revize.com/stalbansvt/Town%20Meeting%20Day%20Results%203.3.26.pdf",
                  "note": "PLACEHOLDER"}
SATOWN_SB = {"url": "https://stalbanstown.com/government/selectboard/index.php",
             "note": "PLACEHOLDER"}
SATOWN_BCA = {"url": "https://stalbanstown.com/government/board_of_civil_authority.php",
              "note": "PLACEHOLDER"}
STJ_REPORT = {"url": "https://docs.stjvt.com",
              "note": "PLACEHOLDER"}
STJ_CEM_MIN = {"url": "https://docs.stjvt.com/index.php/town-government/public-meetings/cemetery-commission/2026-minutes-7/2119-cemetery-commission-minutes-2026-06-11/file",
               "note": "PLACEHOLDER"}
STAM_RESULTS = {"url": "https://stamfordvt.net",
                "note": "PLACEHOLDER"}
STAM_REPORT = {"url": "https://stamfordvt.net",
               "note": "PLACEHOLDER"}
STARKS_RESULTS = {"url": "https://starksborovt.org/sites/default/files/uploads/content/Town%20Meeting/starksboro-election-results-2026.pdf",
                  "note": "PLACEHOLDER"}
STARKS_WARNING = {"url": "https://starksborovt.org/sites/default/files/uploads/content/2026-town-meeting-warning.pdf",
                  "note": "PLACEHOLDER"}
STARKS_MINUTES = {"url": "https://starksborovt.org/sites/default/files/uploads/content/Town%20Meeting/town-meeting-minutes-2026.pdf",
                  "note": "PLACEHOLDER"}
STARKS_REPORT = {"url": "https://starksborovt.org/town-reports",
                 "note": "PLACEHOLDER"}
STARKS_CLERK = {"url": "https://starksborovt.org",
                "note": "PLACEHOLDER"}
STOCK_REPORT = {"url": "https://storage.googleapis.com/juniper-media-library/442/2026/02/97467-Stockbridge-Town-Report-Yr-end-2025-for-WEB.pdf",
                "note": "PLACEHOLDER"}
STRAF_REPORT = {"url": "https://www.straffordvt.org/_files/ugd/0580b2_20fb02af8c624b188777d4aa1f8652a2.pdf",
                "note": "PLACEHOLDER"}


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


def charter011(phrase):
    return S(CHARTER_011, f"24 App. V.S.A. ch. 11 (City of St. "
             f"Albans): {phrase}")


def charter150(phrase):
    return S(CHARTER_150, f"24 App. V.S.A. ch. 150 (Town of St. "
             f"Albans): {phrase}")


def charter151(phrase):
    return S(CHARTER_151, f"24 App. V.S.A. ch. 151 (Town of St. "
             f"Johnsbury): {phrase}")


def charter153(phrase):
    return S(CHARTER_153, f"24 App. V.S.A. ch. 153 (Town of "
             f"Stowe): {phrase}")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 22); issue #163 "
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
                  f"# municipal fan-out batch 22; issue #163 "
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
# Town of St. Albans (Franklin County) -- charter ch. 150 (village
# incorporation and planning provisions; town officers are governed
# by general law, ch. 150 sec. 2).
SATOWN_REP_C = ("Town of St. Albans, FY 2025 Town Report, 'ELECTED "
                "TOWN OFFICERS' table (officers with term lengths "
                "and expiry years) and the March 3, 2026 annual "
                "meeting warning printed in the report")
SATOWN_RES_C = ("Town of St. Albans, official ballot for the "
                "Annual Town Meeting of March 3, 2026 with the "
                "hand-tallied results, attested by Town Clerk Anna "
                "Bourdon (830 total votes)")
SPECS["st-albans-61750"] = spec("st-albans-61750", "Town of St. Albans", [
    office("selectboard", "Selectboard Member",
           "Town of St. Albans Selectboard", 5,
           [charter150("sec. 2 provides that the town's officers "
                       "are governed by general law"),
            S(SATOWN_SB, "Town of St. Albans official website, "
                         "Selectboard page (October 2026): Jack "
                         "Brigham, Chair (term expires 2028); Bryan "
                         "DesLauriers, Vice Chair (expires 2027); "
                         "Jeff Sanders (expires 2028); Cathy "
                         "Montagne (expires 2029); Chelsea Mulheron "
                         "(expires 2027). Mulheron holds the seat "
                         "the FY 2025 Town Report gives to Amanda "
                         "Headley on a two-year term to 2027, with "
                         "the same 2027 expiry -- a vacancy "
                         "appointment under 24 V.S.A. sec. 963, so "
                         "she is seated APPOINTED and Headley is "
                         "not seated"),
            S(SATOWN_RESULTS, f"{SATOWN_RES_C}: John 'Jack' "
                              "Brigham was elected to the two-year "
                              "seat with 692 votes and Cathy "
                              "Montagne to the three-year seat with "
                              "734 votes"),
            sb_dir("names Jack Brigham (Chair), Amanda Headley "
                   "(Vice Chair), Bryan Deslauriers, Cathy "
                   "Montagne, and Jeff Sanders; the town's own "
                   "current Selectboard page governs over the "
                   "directory for the fifth seat (see the Mulheron "
                   "note)")],
           [holder("John \"Jack\" Brigham", "john-jack-brigham",
                   existing_person_id="ocd-person/d351e830-660f-58d4-a8e8-3e61ced2d12d"),
            holder("Bryan Deslauriers", "bryan-deslauriers"),
            holder("Jeff Sanders", "jeff-sanders"),
            holder("Cathy Montagne", "cathy-montagne"),
            holder("Chelsea Mulheron", "chelsea-mulheron",
                   how_seated="appointed")]),
    office("town-clerk", "Town Clerk",
           "Town of St. Albans Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(SATOWN_REPORT, f"{SATOWN_REP_C}: 'Town Clerk & "
                             "Treasurer - Anna Bourdon - 3-year - "
                             "2027'"),
            guide("lists Anna Bourdon as St. Albans Town's Town "
                  "Clerk")],
           [holder("Anna Bourdon", "anna-bourdon")]),
    office("town-treasurer", "Town Treasurer",
           "Town of St. Albans Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(SATOWN_REPORT, f"{SATOWN_REP_C}: 'Town Clerk & "
                             "Treasurer - Anna Bourdon - 3-year - "
                             "2027'"),
            guide("lists Anna Bourdon as St. Albans Town's Town "
                  "Treasurer")],
           [holder("Anna Bourdon", "anna-bourdon")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of St. Albans Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes"),
            S(SATOWN_REPORT, f"{SATOWN_REP_C}: 'Delinquent Tax "
                             "Collector - Anna Bourdon - 3-year - "
                             "2027'; Bourdon also signs her town "
                             "report as 'St. Albans Town Clerk / "
                             "Treasurer, Delinquent Tax Collector'")],
           [holder("Anna Bourdon", "anna-bourdon")]),
    office("constable", "Town Constable",
           "Town of St. Albans Town Constable", 1,
           [S(SATOWN_REPORT, f"{SATOWN_REP_C}: Peter Hatfield "
                             "held the constable's one-year term "
                             "to 2026, and the warning in the "
                             "report elects a Town Constable for a "
                             "one-year term at the March 3, 2026 "
                             "meeting"),
            S(SATOWN_RESULTS, f"{SATOWN_RES_C}: the Town "
                              "Constable contest was write-in "
                              "only, with no printed candidate and "
                              "no total published, so the seat "
                              "stands unfilled here (Hatfield is "
                              "seated as a justice of the peace "
                              "below)")]),
    office("library-trustee", "Library Trustee",
           "Town of St. Albans Library Trustees", 3,
           [S(SATOWN_REPORT, f"{SATOWN_REP_C}: Library Trustees - "
                             "Charlie Brooks (3-year, 2028), "
                             "Meaghan Malbeouf (3-year, 2026), "
                             "Natalie Good (3-year, 2027)"),
            S(SATOWN_RESULTS, f"{SATOWN_RES_C}: Meaghan Malboeuf "
                              "was elected Library Trustee for "
                              "three years with 746 votes (the "
                              "ballot form of her name governs)")],
           [holder("Charlie Brooks", "charlie-brooks"),
            holder("Natalie Good", "natalie-good"),
            holder("Meaghan Malboeuf", "meaghan-malboeuf")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of St. Albans Justices of the Peace", 15,
           [jp_src("lists fifteen St. Albans Town justices of the "
                   "peace: John 'Jack' Brigham, Tina Brosky, Bruce "
                   "Cheeseman, Bryan Deslauriers, Stanley Dukas, "
                   "Jonathan Giroux, Peter Hatfield, Diane Lareau, "
                   "Roger Luneau, John McCarthy, Pamela McCarthy, "
                   "David McWilliams, Joseph Montcalm, Gerald "
                   "Morong, and Albin Voegele (the town's block in "
                   "the listing continues across a page break)"),
            S(SATOWN_BCA, "Town of St. Albans official website, "
                          "Board of Civil Authority page: states "
                          "the board 'consists of 15 Justices of "
                          "the Peace' and names fourteen of them "
                          "(all but Bryan Deslauriers)")],
           [holder("John \"Jack\" Brigham", "john-jack-brigham",
                   existing_person_id="ocd-person/d351e830-660f-58d4-a8e8-3e61ced2d12d"),
            holder("Tina Brosky", "tina-brosky"),
            holder("Bruce Cheeseman", "bruce-cheeseman"),
            holder("Stanley Dukas", "stanley-dukas"),
            holder("Jonathan Giroux", "jonathan-giroux"),
            holder("Peter Hatfield", "peter-hatfield"),
            holder("Diane Lareau", "diane-lareau"),
            holder("Roger Luneau", "roger-luneau"),
            holder("John McCarthy", "john-mccarthy"),
            holder("Pamela McCarthy", "pamela-mccarthy"),
            holder("David McWilliams", "david-mcwilliams"),
            holder("Joseph Montcalm", "joseph-montcalm"),
            holder("Gerald Morong", "gerald-morong"),
            holder("Albin Voegele", "albin-voegele")]),
], jp=jp_election("st-albans-61750-vt", "Town of St. Albans", 15,
                  "the certified listing names fifteen winners for "
                  "St. Albans Town's fifteen justice of the peace "
                  "seats. Bryan Deslauriers is among the certified "
                  "winners but the town's Board of Civil Authority "
                  "page, which states the board consists of 15 "
                  "justices, names only the other fourteen and "
                  "omits him, although he remains Selectboard Vice "
                  "Chair; he is held as a departed winner and no "
                  "person record, candidacy, or winner entry is "
                  "created for his justice seat (the election's "
                  "vote_for stays at the fifteen-seat slate size)",
                  extra_sources=[S(SATOWN_BCA, "Town of St. Albans "
                                   "official website, Board of "
                                   "Civil Authority page: names "
                                   "the fourteen serving justices "
                                   "of the peace")]))

# ----------------------------------------------------------------
# City of St. Albans (Franklin County) -- charter ch. 11.
SACITY_C = ("City of St. Albans official website, 'Mayor & City "
            "Council' contacts page (stalbansvt.com), which prints "
            "each member's term expiry")
SPECS["st-albans"] = spec("st-albans", "City of St. Albans", [
    office("mayor", "Mayor",
           "City of St. Albans Mayor", 1,
           [charter011("sec. 9 provides for a Mayor elected by the "
                       "City's legal voters for a two-year term"),
            S(SACITY_COUNCIL, f"{SACITY_C}: Mayor Trudy Cioffi "
                              "(term expires March 2028)")],
           [holder("Trudy Cioffi", "trudy-cioffi")]),
    office("councilor-ward-1", "Councilor, Ward 1",
           "City of St. Albans City Council", 1,
           [charter011("sec. 10 provides for six Council members, "
                       "one elected from each ward for staggered "
                       "three-year terms (the City styles the "
                       "office 'Ward N Alderperson')"),
            S(SACITY_COUNCIL, f"{SACITY_C}: Ward 1 - Timothy "
                              "Hawkins (term expires March 2028)")],
           [holder("Timothy Hawkins", "timothy-hawkins")]),
    office("councilor-ward-2", "Councilor, Ward 2",
           "City of St. Albans City Council", 1,
           [charter011("sec. 10 (one Council member per ward, "
                       "three-year staggered terms)"),
            S(SACITY_COUNCIL, f"{SACITY_C}: Ward 2 - Lindsay Hunn "
                              "(term expires March 2028)")],
           [holder("Lindsay Hunn", "lindsay-hunn")]),
    office("councilor-ward-3", "Councilor, Ward 3",
           "City of St. Albans City Council", 1,
           [charter011("sec. 10 (one Council member per ward, "
                       "three-year staggered terms)"),
            S(SACITY_COUNCIL, f"{SACITY_C}: Ward 3 - Elizabeth "
                              "Sato (term expires March 2029)")],
           [holder("Elizabeth Sato", "elizabeth-sato")]),
    office("councilor-ward-4", "Councilor, Ward 4",
           "City of St. Albans City Council", 1,
           [charter011("sec. 10 (one Council member per ward, "
                       "three-year staggered terms)"),
            S(SACITY_COUNCIL, f"{SACITY_C}: Ward 4 - Shannon "
                              "Smith (term expires March 2029)")],
           [holder("Shannon Smith", "shannon-smith")]),
    office("councilor-ward-5", "Councilor, Ward 5",
           "City of St. Albans City Council", 1,
           [charter011("sec. 10 (one Council member per ward, "
                       "three-year staggered terms)"),
            S(SACITY_COUNCIL, f"{SACITY_C}: Ward 5 - Erik Johnson "
                              "(term expires March 2027); Johnson "
                              "is a different person from Jericho's "
                              "selectboard member of the same name")],
           [holder("Erik Johnson", "erik-johnson")]),
    office("councilor-ward-6", "Councilor, Ward 6",
           "City of St. Albans City Council", 1,
           [charter011("sec. 10 (one Council member per ward, "
                       "three-year staggered terms)"),
            S(SACITY_COUNCIL, f"{SACITY_C}: Ward 6 - Chad "
                              "Boudreau (the contacts page prints "
                              "no expiry for his seat)")],
           [holder("Chad Boudreau", "chad-boudreau")]),
    office("city-clerk", "City Clerk",
           "City of St. Albans City Clerk", 1,
           [charter011("sec. 12 provides that the City Clerk is "
                       "appointed by the City Council"),
            S(SACITY_CLERK, "City of St. Albans official website, "
                            "City Clerk page: Nicole Robtoy is "
                            "the City Clerk"),
            guide("lists Nicole Robtoy as St. Albans City's City "
                  "Clerk")],
           [holder("Nicole Robtoy", "nicole-robtoy",
                   how_seated="appointed")]),
    office("city-treasurer", "City Treasurer",
           "City of St. Albans City Treasurer", 1,
           [charter011("sec. 13 provides that the City Treasurer "
                       "is appointed by the City Council (one "
                       "person may hold both the clerk's and "
                       "treasurer's offices)"),
            guide("lists Nicole Robtoy as St. Albans City's Town "
                  "Treasurer (the Guide's county table covers "
                  "cities as well)")],
           [holder("Nicole Robtoy", "nicole-robtoy",
                   how_seated="appointed")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "City of St. Albans Justices of the Peace", 15,
           [jp_src("lists fifteen St. Albans City justices of the "
                   "peace: Michael Boulerice, Helene Biggie, "
                   "Kathleen Keenan, Joe Beaudry, Marty Manahan, "
                   "Joe Luneau, Megan Manahan Bliss, David "
                   "Chambers, Richard Stahl, Helen Short, Suzanne "
                   "Kenyon, Linda Pacheco, Andrew Boomhower, Lynn "
                   "Fitzgerald, and Jeremy Allard")],
           [holder("Michael Boulerice", "michael-boulerice"),
            holder("Helene Biggie", "helene-biggie"),
            holder("Kathleen Keenan", "kathleen-keenan"),
            holder("Joe Beaudry", "joe-beaudry"),
            holder("Marty Manahan", "marty-manahan"),
            holder("Joe Luneau", "joe-luneau",
                   existing_person_id="ocd-person/5e90b3cb-93f9-5d2d-abdc-70b8b70c2407"),
            holder("Megan Manahan Bliss", "megan-manahan-bliss"),
            holder("David Chambers", "david-chambers"),
            holder("Richard Stahl", "richard-stahl"),
            holder("Helen Short", "helen-short"),
            holder("Suzanne Kenyon", "suzanne-kenyon"),
            holder("Linda Pacheco", "linda-pacheco"),
            holder("Andrew Boomhower", "andrew-boomhower"),
            holder("Lynn Fitzgerald", "lynn-fitzgerald"),
            holder("Jeremy Allard", "jeremy-allard")]),
], jp=jp_election("st-albans-vt", "City of St. Albans", 15,
                  "the certified listing names fifteen winners for "
                  "St. Albans City's fifteen justice of the peace "
                  "seats"))

# ----------------------------------------------------------------
# Town of St. Johnsbury (Caledonia County) -- charter ch. 151
# (2023, effective May 30, 2024).
STJ_REP_C = ("Town of St. Johnsbury, 2025 Annual Report, 'ELECTED "
             "OFFICIALS' and 'APPOINTED OFFICIALS' tables in the "
             "town officers section (officers with term-expiry "
             "years), published in the town's document center")
SPECS["st-johnsbury"] = spec("st-johnsbury", "Town of St. Johnsbury", [
    office("selectboard", "Selectboard Member",
           "Town of St. Johnsbury Select Board", 5,
           [charter151("sec. 201(a) provides for a five-member "
                       "Select Board elected on staggered terms "
                       "(three three-year seats and two one-year "
                       "seats)"),
            sb_dir("names Frank Empsall (Chair), Ellen Burt (Vice "
                   "Chair), Brendan Hughes, Steven Isham, and "
                   "Dennis Smith; the 2025 report's board predates "
                   "the March 2026 election, so the directory "
                   "governs the board's current composition")],
           [holder("Frank Empsall", "frank-empsall"),
            holder("Ellen Burt", "ellen-burt"),
            holder("Brendan Hughes", "brendan-hughes"),
            holder("Steven Isham", "steven-isham"),
            holder("Dennis Smith", "dennis-smith")]),
    office("town-clerk", "Town Clerk",
           "Town of St. Johnsbury Town Clerk", 1,
           [charter151("sec. 201(a) provides for an elected Town "
                       "Clerk on a three-year term"),
            S(STJ_REPORT, f"{STJ_REP_C}: Town Clerk Stacy Jewell, "
                          "term to 2028"),
            guide("lists Stacy Jewell as St. Johnsbury's Town "
                  "Clerk")],
           [holder("Stacy Jewell", "stacy-jewell")]),
    office("town-treasurer", "Town Treasurer",
           "Town of St. Johnsbury Town Treasurer", 1,
           [charter151("sec. 201(a) provides for an elected Town "
                       "Treasurer on a three-year term"),
            S(STJ_REPORT, f"{STJ_REP_C}: Town Treasurer Stacy "
                          "Jewell, term to 2028"),
            guide("lists Stacy Jewell as St. Johnsbury's Town "
                  "Treasurer")],
           [holder("Stacy Jewell", "stacy-jewell")]),
    office("moderator", "Town Moderator",
           "Town of St. Johnsbury Town Moderator", 1,
           [charter151("sec. 201(a) lists the Moderator among the "
                       "town's elective officers on a three-year "
                       "term, and provides that the Moderator is "
                       "appointed instead if the town so votes"),
            S(STJ_REPORT, f"{STJ_REP_C}: the report files "
                          "Moderator David Reynolds under "
                          "APPOINTED OFFICIALS, not among the "
                          "elected officials, so he is seated as "
                          "an appointee under the charter's town-"
                          "vote option")],
           [holder("David Reynolds", "david-reynolds",
                   how_seated="appointed")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of St. Johnsbury Cemetery Commissioners", 3,
           [S(STJ_REPORT, f"{STJ_REP_C}: the report's ELECTED "
                          "OFFICIALS table lists three Cemetery "
                          "Commissioners -- Lauren Jarvi (term to "
                          "2027), Tim Clouatre (to 2026), and Bryan "
                          "LeBlanc (to 2028). Chapter 151 neither "
                          "creates the office nor assigns its "
                          "appointment, so cemetery commissions "
                          "under 18 V.S.A. sec. 5373 and the town's "
                          "continuing elected practice govern "
                          "(flagged on issue #163)"),
            S(STJ_CEM_MIN, "Town of St. Johnsbury, Cemetery "
                           "Commission minutes of June 11, 2026 "
                           "(town document center): all three "
                           "commissioners -- Bryan LeBlanc, Tim "
                           "Clouatre, and Lauren Jarvi (her "
                           "surname carries a diacritic in the "
                           "minutes, Järvi) -- "
                           "are in attendance and serving after "
                           "the March 2026 meeting, which carries "
                           "Clouatre past his printed 2026 term "
                           "expiry")],
           [holder("Lauren Jarvi", "lauren-jarvi"),
            holder("Tim Clouatre", "tim-clouatre"),
            holder("Bryan LeBlanc", "bryan-leblanc")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of St. Johnsbury Justices of the Peace", 15,
           [jp_src("lists fifteen St. Johnsbury justices of the "
                   "peace: Brent Abare, Durward Ellis, Chase "
                   "Empsall, Frank Empsall, Stephanie Churchill, "
                   "Diane Holmes, Robert Holmes, William Y. Hyde, "
                   "Loraine Janowski, Tristan Lemieux, Kevin Oddy, "
                   "Jane Pompeo, Heather Whitemore, Lynn Wurzburg, "
                   "and Janssen Willhoit"),
            S(STJ_REPORT, f"{STJ_REP_C}: the report's justice of "
                          "the peace list matches the certified "
                          "listing name for name")],
           [holder("Brent Abare", "brent-abare"),
            holder("Durward Ellis", "durward-ellis"),
            holder("Chase Empsall", "chase-empsall"),
            holder("Frank Empsall", "frank-empsall"),
            holder("Stephanie Churchill", "stephanie-churchill"),
            holder("Diane Holmes", "diane-holmes"),
            holder("Robert Holmes", "robert-holmes"),
            holder("William Y. Hyde", "william-y-hyde"),
            holder("Loraine Janowski", "loraine-janowski"),
            holder("Tristan Lemieux", "tristan-lemieux"),
            holder("Kevin Oddy", "kevin-oddy"),
            holder("Jane Pompeo", "jane-pompeo"),
            holder("Heather Whitemore", "heather-whitemore"),
            holder("Lynn Wurzburg", "lynn-wurzburg"),
            holder("Janssen Willhoit", "janssen-willhoit")]),
], jp=jp_election("st-johnsbury-vt", "Town of St. Johnsbury", 15,
                  "the certified listing names fifteen winners for "
                  "St. Johnsbury's fifteen justice of the peace "
                  "seats"))

# ----------------------------------------------------------------
# Town of Stamford (Bennington County) -- general law.
STAM_RES_C = ("Town of Stamford, official marked results ballot "
              "for the annual meeting of March 3, 2026 (town "
              "website, stamfordvt.net)")
STAM_REP_C = ("Town of Stamford, 2023 Town Report, 'Elected Town "
              "Officers' and 'Appointed Town Officers' lists and "
              "the 2024 annual meeting warning printed in the "
              "report")
SPECS["stamford"] = spec("stamford", "Town of Stamford", [
    office("moderator", "Town Moderator",
           "Town of Stamford Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(STAM_RESULTS, f"{STAM_RES_C}: John Paul Potvin was "
                             "elected Moderator as a write-in "
                             "candidate NAMED in the official "
                             "tally (63 votes; he also won School "
                             "Moderator with 53) -- a certified "
                             "write-in outcome with the name "
                             "printed in the tally itself (flagged "
                             "on issue #163)")],
           [holder("John Paul Potvin", "john-paul-potvin")]),
    office("town-clerk", "Town Clerk",
           "Town of Stamford Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(STAM_RESULTS, f"{STAM_RES_C}: Lori A. Shepard was "
                             "elected Town Clerk with 108 votes "
                             "(three-year term to 2029)"),
            guide("lists Lori A. Shepard as Stamford's Town "
                  "Clerk")],
           [holder("Lori A. Shepard", "lori-a-shepard")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Stamford Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(STAM_RESULTS, f"{STAM_RES_C}: Lori A. Shepard was "
                             "elected Town Treasurer with 108 "
                             "votes"),
            guide("lists Lori A. Shepard as Stamford's Town "
                  "Treasurer")],
           [holder("Lori A. Shepard", "lori-a-shepard")]),
    office("selectboard", "Selectboard Member",
           "Town of Stamford Selectboard", 5,
           [sb_dir("names Nancy Bushika (Chair), Michael Denault, "
                   "John Dunn, Kurt Gamari, and Jedidiah Gramlin"),
            S(STAM_RESULTS, f"{STAM_RES_C}: Kurt Gamari was "
                             "elected to the three-year seat "
                             "with 99 votes and Jedidiah Gramlin "
                             "to the two-year seat with 84 votes "
                             "(Stamford elects its five members "
                             "on mixed two- and three-year terms)")],
           [holder("Nancy Bushika", "nancy-bushika"),
            holder("Michael Denault", "michael-denault"),
            holder("John Dunn", "john-dunn"),
            holder("Kurt Gamari", "kurt-gamari"),
            holder("Jedidiah Gramlin", "jedidiah-gramlin")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Stamford Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes"),
            S(STAM_RESULTS, f"{STAM_RES_C}: Sally A. Bohl was "
                             "elected Collector of Delinquent "
                             "Taxes with 89 votes"),
            S(STAM_REPORT, f"{STAM_REP_C}: Bohl also held the "
                            "office in 2023")],
           [holder("Sally A. Bohl", "sally-a-bohl")]),
    office("lister", "Lister",
           "Town of Stamford Listers", 3,
           [statute2646("towns elect three listers on staggered "
                        "three-year terms"),
            S(STAM_RESULTS, f"{STAM_RES_C}: Kristin Malachuk "
                             "was elected Lister as a write-in "
                             "candidate NAMED in the official "
                             "tally (21 votes, the three-year "
                             "seat) -- a certified write-in "
                             "outcome (flagged on issue #163). "
                             "The one-year remainder contest drew "
                             "no write-in votes and the third "
                             "seat is published nowhere, so two "
                             "seats stand unfilled")],
           [holder("Kristin Malachuk", "kristin-malachuk")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Stamford Cemetery Commissioners", 3,
           [S(STAM_RESULTS, f"{STAM_RES_C}: Luke McKay was "
                             "elected Cemetery Commissioner with "
                             "98 votes"),
            S(STAM_REPORT, f"{STAM_REP_C}: the 2023 roster (David "
                            "McKay, Sheila G. Lawrence, and one "
                            "further seat) predates two election "
                            "cycles and is stale, so the other "
                            "two seats stand unfilled")],
           [holder("Luke McKay", "luke-mckay")]),
    office("library-trustee", "Library Trustee",
           "Town of Stamford Library Trustees", 5,
           [S(STAM_REPORT, f"{STAM_REP_C}: the Stamford Free "
                            "Library's trustees are elected (the "
                            "2023 report's elected list shows "
                            "five trustees, although its term "
                            "labels conflict between three- and "
                            "five-year terms -- flagged on issue "
                            "#163)"),
            S(STAM_RESULTS, f"{STAM_RES_C}: the single 2026 "
                             "library seat drew no write-in "
                             "votes and the current trustees are "
                             "published nowhere official, so the "
                             "post is created without memberships "
                             "(straggler)")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Stamford Justices of the Peace", 5,
           [jp_src("lists five Stamford justices of the peace: "
                   "Sally A. Bohl, Marta Miller, Sheila Pecor, "
                   "Peter Greenbush, and Mary Lou Wright")],
           [holder("Sally A. Bohl", "sally-a-bohl"),
            holder("Marta Miller", "marta-miller"),
            holder("Sheila Pecor", "sheila-pecor"),
            holder("Peter Greenbush", "peter-greenbush"),
            holder("Mary Lou Wright", "mary-lou-wright")]),
], jp=jp_election("stamford-vt", "Town of Stamford", 5,
                  "the certified listing names five winners for "
                  "Stamford's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Stannard (Caledonia County) -- general law. No town
# website exists; the build runs on the SOS spine (Searsburg
# shape).
SPECS["stannard"] = spec("stannard", "Town of Stannard", [
    office("selectboard", "Selectboard Member",
           "Town of Stannard Selectboard", 3,
           [sb_dir("names Jan Lewandoski (Chair), Katy Knuth, and "
                   "Stephen Lyons for Stannard's three-member "
                   "board (the directory prints the third member "
                   "as 'Lyons Stephen'; the name order here "
                   "follows the directory's surname-first slip). "
                   "The town has no website, so the directory is "
                   "the roster of record")],
           [holder("Jan Lewandoski", "jan-lewandoski"),
            holder("Katy Knuth", "katy-knuth"),
            holder("Stephen Lyons", "stephen-lyons")]),
    office("town-clerk", "Town Clerk",
           "Town of Stannard Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            clerk_xlsx("names Connie Withers as Stannard's Town "
                       "Clerk (the June 2026 spreadsheet postdates "
                       "the March 2026 town meeting)"),
            guide("lists Connie Withers as Stannard's Town Clerk")],
           [holder("Connie Withers", "connie-withers")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Stannard Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            guide("lists Cynthia Wheeler as Stannard's Town "
                  "Treasurer; the June 2026 treasurer spreadsheet "
                  "carries no Stannard row ('contact Town Clerk'), "
                  "so she is seated on disclosed incumbency "
                  "continuity from the Guide, with no contrary "
                  "evidence in any official source")],
           [holder("Cynthia Wheeler", "cynthia-wheeler")]),
    office("moderator", "Town Moderator",
           "Town of Stannard Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term")]),
    office("lister", "Lister",
           "Town of Stannard Listers", 3,
           [statute2646_structure("towns elect three listers on "
                                  "staggered three-year terms")]),
    office("auditor", "Auditor",
           "Town of Stannard Auditors", 3,
           [statute2646_structure("towns elect auditors (three, "
                                  "staggered terms) unless the "
                                  "office is eliminated")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Stannard Collector of Delinquent Taxes", 1,
           [statute2646_structure("towns elect a collector of "
                                  "delinquent taxes")]),
    office("constable", "Constable",
           "Town of Stannard Constable", 1,
           [statute2646_structure("towns elect a constable")]),
    office("grand-juror", "Grand Juror",
           "Town of Stannard Grand Juror", 1,
           [statute2646_structure("towns elect a grand juror")]),
    office("town-agent", "Town Agent",
           "Town of Stannard Town Agent", 1,
           [statute2646_structure("towns elect a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Stannard Justices of the Peace", 5,
           [jp_src("lists five Stannard justices of the peace: "
                   "Christine Foster, Joseph Gresser, Johanna F. "
                   "Polsenberg, Joseph Chip Troiano, and Cynthia "
                   "Wheeler")],
           [holder("Christine Foster", "christine-foster"),
            holder("Joseph Gresser", "joseph-gresser"),
            holder("Johanna F. Polsenberg", "johanna-f-polsenberg"),
            holder("Joseph Chip Troiano", "joseph-chip-troiano"),
            holder("Cynthia Wheeler", "cynthia-wheeler")]),
], jp=jp_election("stannard-vt", "Town of Stannard", 5,
                  "the certified listing names five winners for "
                  "Stannard's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Starksboro (Addison County) -- general law.
STARKS_RES_C = ("Town of Starksboro, official results ballot for "
                "the annual meeting of March 3, 2026 (town website, "
                "starksborovt.org)")
STARKS_REP_C = ("Town of Starksboro, 2022-2023 Town Report, "
                "elected-officials list (officers with board "
                "sizes)")
SPECS["starksboro"] = spec("starksboro", "Town of Starksboro", [
    office("moderator", "Town Moderator",
           "Town of Starksboro Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(STARKS_RESULTS, f"{STARKS_RES_C}: Keegan Tierney "
                               "was elected Moderator with 328 "
                               "votes")],
           [holder("Keegan Tierney", "keegan-tierney")]),
    office("selectboard", "Selectboard Member",
           "Town of Starksboro Selectboard", 5,
           [sb_dir("names Koran Cousino (Chair), Eric Cota, Carin "
                   "Mccarthy, Tony Porter, and David Schmidt"),
            S(STARKS_RESULTS, f"{STARKS_RES_C}: Koran Cousino "
                               "was re-elected with 249 votes, "
                               "Carin H. McCarthy with 298, and "
                               "Tony Porter to a remainder seat "
                               "with 310")],
           [holder("Koran Cousino", "koran-cousino"),
            holder("Carin McCarthy", "carin-mccarthy"),
            holder("Tony Porter", "tony-porter"),
            holder("Eric Cota", "eric-cota"),
            holder("David Schmidt", "david-schmidt")]),
    office("town-clerk", "Town Clerk",
           "Town of Starksboro Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(STARKS_CLERK, "Town of Starksboro official website, "
                            "town clerk page: Amy McCormick is "
                            "the Town Clerk"),
            guide("lists Amy McCormick as Starksboro's Town "
                  "Clerk")],
           [holder("Amy McCormick", "amy-mccormick")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Starksboro Town Treasurer", 1,
           [S(STARKS_CLERK, "Town of Starksboro official website: "
                            "the clerk's page staff block shows "
                            "Alexandra ('Ali') Thompson serving "
                            "as Treasurer. The town's elected-"
                            "officials list and its March 2026 "
                            "ballot both omit a treasurer contest "
                            "although 17 V.S.A. sec. 2646 makes "
                            "the office elective, so she is "
                            "seated APPOINTED on the town's own "
                            "presentation (flagged on issue #163)"),
            guide("lists Alexandra Thompson as Starksboro's "
                  "Town Treasurer")],
           [holder("Alexandra Thompson", "alexandra-thompson",
                   how_seated="appointed")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Starksboro Collector of Delinquent Taxes", 1,
           [statute2646("towns elect a collector of delinquent "
                        "taxes"),
            S(STARKS_RESULTS, f"{STARKS_RES_C}: Amy McCormick "
                               "was elected Collector of "
                               "Delinquent Taxes with 330 votes")],
           [holder("Amy McCormick", "amy-mccormick")]),
    office("lister", "Lister",
           "Town of Starksboro Listers", 3,
           [statute2646("towns elect three listers on staggered "
                        "three-year terms"),
            S(STARKS_RESULTS, f"{STARKS_RES_C}: Charles Webber "
                               "was elected Lister with 297 "
                               "votes; the other two seats' "
                               "current holders are published "
                               "nowhere official")],
           [holder("Charles Webber", "charles-webber")]),
    office("auditor", "Auditor",
           "Town of Starksboro Auditors", 3,
           [statute2646("towns elect auditors (three, staggered "
                        "terms) unless the office is eliminated"),
            S(STARKS_RESULTS, f"{STARKS_RES_C}: both 2026 auditor "
                               "contests were write-in only and "
                               "no winner is named in the "
                               "official results, so the post is "
                               "created without memberships "
                               "(straggler)")]),
    office("first-constable", "First Constable",
           "Town of Starksboro First Constable", 1,
           [statute2646("towns elect a first constable"),
            S(STARKS_REPORT, f"{STARKS_REP_C}: the First "
                              "Constable is printed 'Vacant'"),
            S(STARKS_RESULTS, f"{STARKS_RES_C}: the 2026 "
                               "constable contest was write-in "
                               "only with no winner named, so "
                               "the seat stands unfilled")]),
    office("second-constable", "Second Constable",
           "Town of Starksboro Second Constable", 1,
           [statute2646("towns elect a second constable"),
            S(STARKS_RESULTS, f"{STARKS_RES_C}: the 2026 "
                               "constable contests were write-in "
                               "only with no winner named, so "
                               "the seat stands unfilled")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Starksboro Cemetery Commissioners", 3,
           [S(STARKS_RESULTS, f"{STARKS_RES_C}: Norman Cota was "
                               "elected Cemetery Commissioner "
                               "with 326 votes; the other two "
                               "seats' current holders are "
                               "published nowhere official")],
           [holder("Norman Cota", "norman-cota")]),
    office("library-trustee", "Library Trustee",
           "Town of Starksboro Library Trustees", 5,
           [S(STARKS_RESULTS, f"{STARKS_RES_C}: Emily Fisher was "
                               "elected Library Trustee with 293 "
                               "votes, Leah Hamilton with 284, "
                               "and Ellen Yount to a remainder "
                               "seat with 308")],
           [holder("Emily Fisher", "emily-fisher"),
            holder("Leah Hamilton", "leah-hamilton"),
            holder("Ellen Yount", "ellen-yount")]),
    office("planning-commissioner", "Planning Commissioner",
           "Town of Starksboro Planning Commission", 7,
           [S(STARKS_WARNING, "Town of Starksboro, Warning for "
                              "the annual meeting of March 3, "
                              "2026: Article elects Planning "
                              "Commissioners by ballot, so the "
                              "commission is an ELECTED body "
                              "under 24 V.S.A. sec. 4323, which "
                              "permits a town to elect its "
                              "planning commission"),
            S(STARKS_REPORT, f"{STARKS_REP_C}: the elected list "
                              "prints seven Planning Commission "
                              "roster lines (four members serving "
                              "and three seats resigned), fixing "
                              "the commission at seven seats "
                              "(disclosed in the sources)"),
            S(STARKS_RESULTS, f"{STARKS_RES_C}: Dan Nugent was "
                               "elected Planning Commissioner "
                               "with 287 votes; the other "
                               "current members are published "
                               "nowhere official")],
           [holder("Dan Nugent", "dan-nugent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Starksboro Justices of the Peace", 7,
           [jp_src("lists seven Starksboro justices of the peace: "
                   "Norman Cota, Margaret 'Peg' Casey, Luke "
                   "McCarthy, Laurie Webber, Edward 'Ben' Campbell, "
                   "Alan Quittner, and Brittany Peduzzi")],
           [holder("Norman Cota", "norman-cota"),
            holder("Margaret \"Peg\" Casey", "margaret-peg-casey",
                   ballot_name="Margaret 'Peg' Casey"),
            holder("Luke McCarthy", "luke-mccarthy"),
            holder("Laurie Webber", "laurie-webber"),
            holder("Edward \"Ben\" Campbell", "edward-ben-campbell",
                   ballot_name="Edward 'Ben' Campbell"),
            holder("Alan Quittner", "alan-quittner"),
            holder("Brittany Peduzzi", "brittany-peduzzi")]),
], jp=jp_election("starksboro-vt", "Town of Starksboro", 7,
                  "the certified listing names seven winners for "
                  "Starksboro's seven justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Stockbridge (Windsor County) -- general law.
STOCK_REP_C = ("Town of Stockbridge, Town Report for the year "
               "ending December 31, 2025, 'Elected Town Officials' "
               "and 'Appointed Town Officials' tables (terms with "
               "expiry years), and the 2026 annual meeting warning "
               "printed in the report (Article 1 elects the "
               "officers by Australian ballot)")
SPECS["stockbridge"] = spec("stockbridge", "Town of Stockbridge", [
    office("moderator", "Town Moderator",
           "Town of Stockbridge Town Moderator", 1,
           [S(STOCK_REPORT, f"{STOCK_REP_C}: the report runs "
                            "Moderator Kent Butterfield through "
                            "2026 and the 2026 warning elects a "
                            "moderator, but the outcome is "
                            "published nowhere official (the "
                            "town's 2026 minutes sit behind its "
                            "website's script-driven app), so the "
                            "post is created without a membership "
                            "(straggler)")]),
    office("town-clerk", "Town Clerk",
           "Town of Stockbridge Town Clerk", 1,
           [S(STOCK_REPORT, f"{STOCK_REP_C}: the report's "
                            "Appointed Town Officials table lists "
                            "'Town Clerk - Jill Gifford - Through "
                            "2026', so she is seated APPOINTED, "
                            "not elected (flagged on issue #163)"),
            guide("lists Jill Gifford as Stockbridge's Town "
                  "Clerk")],
           [holder("Jill Gifford", "jill-gifford",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Stockbridge Town Treasurer", 1,
           [S(STOCK_REPORT, f"{STOCK_REP_C}: the report's "
                            "Appointed Town Officials table lists "
                            "'Town Treasurer - Jill Gifford - "
                            "Through 2026', so she is seated "
                            "APPOINTED, not elected"),
            guide("lists Jill Gifford as Stockbridge's Town "
                  "Treasurer")],
           [holder("Jill Gifford", "jill-gifford",
                   how_seated="appointed")]),
    office("selectboard", "Selectboard Member",
           "Town of Stockbridge Selectboard", 3,
           [S(STOCK_REPORT, f"{STOCK_REP_C}: the elected table "
                            "runs Michael Ketchum and Carol "
                            "Taylor-Burke through 2027 and 2028, "
                            "with the third seat's term (Mark "
                            "Begin) ending in 2026; the 2026 "
                            "warning elects a three-year seat to "
                            "2029"),
            sb_dir("names Michael Ketchum, Carol Taylor-Burke, "
                   "and Christopher Bump for the third seat, so "
                   "Bump holds the seat the warning filled in "
                   "2026")],
           [holder("Michael Ketchum", "michael-ketchum"),
            holder("Carol Taylor-Burke", "carol-taylor-burke"),
            holder("Christopher Bump", "christopher-bump")]),
    office("lister", "Lister",
           "Town of Stockbridge Listers", 3,
           [S(STOCK_REPORT, f"{STOCK_REP_C}: the elected table "
                            "runs Beth Dawley and Richard Furman "
                            "through 2027 and 2028; the third "
                            "seat (Lori Scott) stood in 2026 and "
                            "its outcome is published nowhere, "
                            "so it stands unfilled")],
           [holder("Beth Dawley", "beth-dawley"),
            holder("Richard Furman", "richard-furman")]),
    office("auditor", "Auditor",
           "Town of Stockbridge Auditors", 3,
           [S(STOCK_REPORT, f"{STOCK_REP_C}: the elected table "
                            "runs Jenny Austin through 2028; two "
                            "further auditor seats were warned "
                            "for 2026 (one term had ended) and "
                            "their outcomes are published "
                            "nowhere, so they stand unfilled")],
           [holder("Jenny Austin", "jenny-austin")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Stockbridge Collector of Delinquent Taxes", 1,
           [S(STOCK_REPORT, f"{STOCK_REP_C}: the elected table "
                            "runs 'Collector of Delinquent Taxes "
                            "- Donna Bryan - Through 2027'")],
           [holder("Donna Bryan", "donna-bryan")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Stockbridge Trustees of Public Funds", 3,
           [S(STOCK_REPORT, f"{STOCK_REP_C}: the elected table "
                            "runs Teresa Newton and Julie Groppe "
                            "through 2027 and 2028; the third "
                            "seat (Kim Moore) stood in 2026 and "
                            "its outcome is published nowhere, "
                            "so it stands unfilled")],
           [holder("Teresa Newton", "teresa-newton"),
            holder("Julie Groppe", "julie-groppe")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Stockbridge Cemetery Commissioners", 3,
           [S(STOCK_REPORT, f"{STOCK_REP_C}: the elected table "
                            "runs Nancy McCoullough through 2028; "
                            "the other two seats' current "
                            "holders are published nowhere "
                            "official")],
           [holder("Nancy McCoullough", "nancy-mccoullough")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Stockbridge Justices of the Peace", 5,
           [jp_src("lists five Stockbridge justices of the peace: "
                   "Kathie Burns, Suzanne Butterfield, Patrick "
                   "Giordano, Ryan Knox, and Kelly "
                   "Mcdermott-Burns"),
            S(STOCK_REPORT, f"{STOCK_REP_C}: the report's justice "
                             "of the peace list matches the "
                             "certified listing (the listing's "
                             "form of the fifth name governs)")],
           [holder("Kathie Burns", "kathie-burns"),
            holder("Suzanne Butterfield", "suzanne-butterfield"),
            holder("Patrick Giordano", "patrick-giordano"),
            holder("Ryan Knox", "ryan-knox"),
            holder("Kelly Mcdermott-Burns", "kelly-mcdermott-burns")]),
], jp=jp_election("stockbridge-vt", "Town of Stockbridge", 5,
                  "the certified listing names five winners for "
                  "Stockbridge's five justice of the peace seats"))

# ----------------------------------------------------------------
# Town of Strafford (Orange County) -- general law. Strafford has
# voted its town officers by Australian ballot since abolishing
# its floor town meeting in 2022.
STRAF_REP_C = ("Town of Strafford, 2024 Town Report, 'Town "
               "Officers' table (officers with term-expiry "
               "columns)")
SPECS["strafford"] = spec("strafford", "Town of Strafford", [
    office("moderator", "Town Moderator",
           "Town of Strafford Town Moderator", 1,
           [statute2646_structure("towns elect a moderator for a "
                                  "one-year term; the 2024 "
                                  "report's Moderator is David "
                                  "Grant, but the office is "
                                  "annual and its 2025 and 2026 "
                                  "outcomes are published "
                                  "nowhere official")]),
    office("town-clerk", "Town Clerk",
           "Town of Strafford Town Clerk", 1,
           [statute2646("towns elect a town clerk"),
            S(STRAF_REPORT, f"{STRAF_REP_C}: 'Town Clerk and "
                             "Treasurer: Lisa Bragg', on the "
                             "combined term running to March 2027, "
                             "which spans the March 2026 meeting"),
            guide("lists Lisa Bragg as Strafford's Town Clerk")],
           [holder("Lisa Bragg", "lisa-bragg")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Strafford Town Treasurer", 1,
           [statute2646("towns elect a town treasurer"),
            S(STRAF_REPORT, f"{STRAF_REP_C}: 'Town Clerk and "
                             "Treasurer: Lisa Bragg', on the "
                             "combined term running to March 2027"),
            guide("lists Lisa Bragg as Strafford's Town "
                  "Treasurer")],
           [holder("Lisa Bragg", "lisa-bragg")]),
    office("selectboard", "Selectboard Member",
           "Town of Strafford Selectboard", 5,
           [sb_dir("names Jason Schumacher (Chair), Christopher "
                   "Behr, Matthew Christie, Mary Linehan, and "
                   "Marya Merriam; the 2024 report's board (Pippy, "
                   "Linehan, Duncklee, Harman, Solsaa) turned "
                   "over almost entirely across the 2025 and "
                   "2026 cycles, and the June 2026 directory "
                   "governs the current five")],
           [holder("Jason Schumacher", "jason-schumacher"),
            holder("Christopher Behr", "christopher-behr"),
            holder("Matthew Christie", "matthew-christie"),
            holder("Mary Linehan", "mary-linehan"),
            holder("Marya Merriam", "marya-merriam")]),
    office("lister", "Lister",
           "Town of Strafford Listers", 3,
           [statute2646_structure("towns elect three listers on "
                                  "staggered three-year terms; "
                                  "the 2024 report's roster "
                                  "(Jacobs, Denny, Gortner) "
                                  "predates two election cycles "
                                  "and its expiry column cannot "
                                  "be paired to names from the "
                                  "report's layout, and no "
                                  "current official roster "
                                  "exists")]),
    office("auditor", "Auditor",
           "Town of Strafford Auditors", 3,
           [statute2646_structure("towns elect auditors (three, "
                                  "staggered terms) unless the "
                                  "office is eliminated; the 2024 "
                                  "report's roster (Pennington, "
                                  "Liepmann, June Solsaa) is "
                                  "stale on the same terms as "
                                  "the listers above")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Strafford Collector of Delinquent Taxes", 1,
           [statute2646_structure("towns elect a collector of "
                                  "delinquent taxes; the 2024 "
                                  "report's holder is Jeanne "
                                  "Castro, but the office is "
                                  "annual and no post-2024 "
                                  "outcome is published")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Strafford Trustees of Public Funds", 3,
           [statute2646_structure("towns elect trustees of public "
                                  "funds (three); the 2024 "
                                  "report's roster (Therese "
                                  "Linehan, Cindy Stableford, "
                                  "Sarah North) predates two "
                                  "election cycles")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Strafford Cemetery Commissioners", 5,
           [S(STRAF_REPORT, f"{STRAF_REP_C}: the table names five "
                            "Cemetery Commissioners (David "
                            "Harris, Andrew Behrens, Lauri "
                            "Berkenkamp, Kate Siepmann, Sherm "
                            "Wilson), which fixes the board at "
                            "five seats under 18 V.S.A. sec. "
                            "5373, but the roster predates two "
                            "election cycles and no seat's "
                            "current holder is published, so "
                            "the post is created without "
                            "memberships (straggler)")]),
    office("constable", "Constable",
           "Town of Strafford Constable", 1,
           [statute2646_structure("towns elect a constable; the "
                                  "holder is published nowhere "
                                  "official")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Strafford Justices of the Peace", 7,
           [jp_src("lists seven Strafford justices of the peace: "
                   "Curt Albee, Shelby Coburn, Andrew Lane, Sean "
                   "Lewis, Victoria Lloyd, Sarah North, and Vince "
                   "Robinson")],
           [holder("Curt Albee", "curt-albee"),
            holder("Shelby Coburn", "shelby-coburn"),
            holder("Andrew Lane", "andrew-lane"),
            holder("Sean Lewis", "sean-lewis"),
            holder("Victoria Lloyd", "victoria-lloyd"),
            holder("Sarah North", "sarah-north"),
            holder("Vince Robinson", "vince-robinson")]),
], jp=jp_election("strafford-vt", "Town of Strafford", 7,
                  "the certified listing names seven winners for "
                  "Strafford's seven justice of the peace seats"))


# ----------------------------------------------------------------
# Town of St. George (Chittenden County) -- general law. The
# town HIRES its clerk and treasurer (2025 town meeting minutes:
# both introduced as hired staff), so both are seated APPOINTED.
STGEO_REPORT = {"url": "https://webgen1.revize.com/revize/stgeorgevt/2025%20Annual%20Report.pdf",
                "note": "PLACEHOLDER"}
STGEO_MIN25 = {"url": "https://webgen1.revize.com/revize/stgeorgevt/Minutes/Town%20Meeting/2025%20Town%20Meeting%20Minutes.pdf",
               "note": "PLACEHOLDER"}
STGEO_DOCS = {"url": "https://stgeorgevt.com",
              "note": "PLACEHOLDER"}
STGEO_REP_C = ("Town of St. George, 2025 Annual Report, '2025 "
               "ELECTED OFFICERS' and '2025 Town Officials / 2025 "
               "Appointed Officers' pages (officers with term "
               "lengths and expiry years)")
STGEO_MIN_C = ("Town of St. George, Minutes of the Annual Town "
               "Meeting of March 4, 2025")
SPECS["st-george"] = spec("st-george", "Town of St. George", [
    office("moderator", "Town Moderator",
           "Town of St. George Town Moderator", 1,
           [statute2646("towns elect a moderator for a one-year "
                        "term"),
            S(STGEO_MIN25, f"{STGEO_MIN_C}: Article 1 -- Charles "
                            "Scott nominated Steve Faust; "
                            "nominations closed and the vote for "
                            "Faust as Moderator passed "
                            "unanimously"),
            S(STGEO_DOCS, "Town of St. George official website, "
                          "Minutes of the Annual Town Meeting of "
                          "March 3, 2026 (town document center): "
                          "Faust was nominated by Phil Gingrow "
                          "and re-elected Moderator by unanimous "
                          "vote")],
           [holder("Steve Faust", "steve-faust")]),
    office("town-clerk", "Town Clerk",
           "Town of St. George Town Clerk", 1,
           [S(STGEO_MIN25, f"{STGEO_MIN_C}: the meeting's officer "
                            "reports introduce 'Lisa Laramee, "
                            "Town Clerk & Town Administrator, "
                            "hired October 2024' -- the town "
                            "hires its clerk, so she is seated "
                            "APPOINTED, not elected (flagged on "
                            "issue #163)"),
            S(STGEO_REPORT, f"{STGEO_REP_C}: the officials page "
                             "lists 'Town Clerk, Town "
                             "Administrator - Lisa Laramee' among "
                             "the town's officials, not on the "
                             "elected-officers page"),
            guide("lists Lisa Laramee as St. George's Town "
                  "Clerk")],
           [holder("Lisa Laramee", "lisa-laramee",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of St. George Town Treasurer", 1,
           [S(STGEO_MIN25, f"{STGEO_MIN_C}: the officer reports "
                            "introduce 'Adam Beach, Town "
                            "Treasurer & Delinquent Tax "
                            "Collector, hired September 2023' -- "
                            "the town hires its treasurer, so he "
                            "is seated APPOINTED, not elected"),
            S(STGEO_REPORT, f"{STGEO_REP_C}: the officials page "
                             "lists 'Town Treasurer - Adam "
                             "Beach' among the town's officials, "
                             "not on the elected-officers page"),
            guide("lists Adam Beach as St. George's Town "
                  "Treasurer")],
           [holder("Adam Beach", "adam-beach",
                   how_seated="appointed")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of St. George Collector of Delinquent Taxes", 1,
           [S(STGEO_MIN25, f"{STGEO_MIN_C}: Adam Beach serves as "
                            "'Town Treasurer & Delinquent Tax "
                            "Collector', hired September 2023, "
                            "and the annual report files the "
                            "delinquent tax collector among the "
                            "town's appointed officers on a "
                            "one-year term, so he is seated "
                            "APPOINTED")],
           [holder("Adam Beach", "adam-beach",
                   how_seated="appointed")]),
    office("selectboard", "Selectboard Member",
           "Town of St. George Selectboard", 5,
           [sb_dir("names Joel Colf (Chair), Adam Dantzscher, "
                   "Terri Hallenbeck, Asher Menashe, and Judith "
                   "Scott; the directory predates Menashe's "
                   "departure (see the town sources)"),
            S(STGEO_DOCS, "Town of St. George official website, "
                          "Minutes of the Annual Town Meeting of "
                          "March 3, 2026, and the town's Contact "
                          "List of September 24, 2026 (town "
                          "document center): Judy Scott and "
                          "Terri Hallenbeck each won two-year "
                          "terms to 2028 and Adam Dantzscher a "
                          "three-year term to 2029; Asher A.J. "
                          "Menashe won the remaining seat (a "
                          "three-year term's remainder to 2028) "
                          "but the September 2026 contact list "
                          "names only four members -- Colf, "
                          "Scott (Vice Chair), Dantzscher, and "
                          "Hallenbeck -- so Menashe's seat "
                          "stands vacant and he is not seated "
                          "(straggler)")],
           [holder("Joel Colf", "joel-colf"),
            holder("Judith Scott", "judith-scott"),
            holder("Terri Hallenbeck", "terri-hallenbeck"),
            holder("Adam Dantzscher", "adam-dantzscher")]),
    office("auditor", "Auditor",
           "Town of St. George Auditors", 3,
           [statute2646("towns elect auditors (three, staggered "
                        "three-year terms)"),
            S(STGEO_REPORT, f"{STGEO_REP_C}: Auditors -- Caroline "
                             "Jalbert (term expires 2028), Lisa "
                             "Hodgkins (2026), Sandra Jarvis "
                             "(2027)"),
            S(STGEO_DOCS, "Town of St. George official website, "
                          "Minutes of the Annual Town Meeting of "
                          "March 3, 2026: Lisa Hodgkins was "
                          "elected Auditor for a three-year term "
                          "expiring 2029")],
           [holder("Caroline Jalbert", "caroline-jalbert"),
            holder("Sandra Jarvis", "sandra-jarvis"),
            holder("Lisa Hodgkins", "lisa-hodgkins")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of St. George Cemetery Commissioners", 3,
           [S(STGEO_REPORT, f"{STGEO_REP_C}: Cemetery "
                            "Commissioners (three-year terms) -- "
                            "Adam Dantzscher (term expires "
                            "2028), Mary Alice Favro (2026), "
                            "Terri Hallenbeck (2027)"),
            S(STGEO_DOCS, "Town of St. George official website: "
                          "the March 2026 annual meeting warning "
                          "(Article 8, 'To elect a Cemetery "
                          "Commissioner for a 3-year term "
                          "expiring in 2029') and the March 3, "
                          "2026 minutes record Mary Alice Favro "
                          "elected to that term; the town's "
                          "cemetery bylaws describe the cemetery "
                          "as 'maintained by an elected board of "
                          "three cemetery commissioners', and "
                          "the contact list names Favro (Chair), "
                          "Dantzscher, and Hallenbeck")],
           [holder("Adam Dantzscher", "adam-dantzscher"),
            holder("Terri Hallenbeck", "terri-hallenbeck"),
            holder("Mary Alice Favro", "mary-alice-favro")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of St. George Justices of the Peace", 5,
           [jp_src("lists four St. George justices of the peace: "
                   "Kelly A. Bowen, Mary Alice Favro, Judith R. "
                   "Pillsbury, and Charles Scott"),
            S(STGEO_REPORT, f"{STGEO_REP_C}: the elected-officers "
                             "page prints five justice of the "
                             "peace lines -- the four winners "
                             "above plus one 'Vacant' -- so the "
                             "town's slate is five seats with "
                             "four filled")],
           [holder("Kelly A. Bowen", "kelly-a-bowen"),
            holder("Mary Alice Favro", "mary-alice-favro"),
            holder("Judith R. Pillsbury", "judith-r-pillsbury"),
            holder("Charles Scott", "charles-scott")]),
], jp=jp_election("st-george-vt", "Town of St. George", 5,
                  "the certified listing names four winners for "
                  "St. George; the town's 2025 annual report prints "
                  "five justice of the peace lines with the fifth "
                  "marked 'Vacant', so the election's vote_for is "
                  "the town's five-seat slate with four winners "
                  "seated"))


# ----------------------------------------------------------------
# Town of Stowe (Lamoille County) -- charter ch. 153. The town
# site bot-gates direct fetches; the roster was read in the
# browser from the town's own pages and documents.
STOWE_RESULTS = {"url": "https://www.stowevt.gov/Departments/Town-Clerk-Treasurer/Election-Information-Results",
                 "note": "PLACEHOLDER"}
STOWE_LISTERS = {"url": "https://www.stowevt.gov/Government/Listers",
                 "note": "PLACEHOLDER"}
STOWE_SB = {"url": "https://www.stowevt.gov/Government/Selectboard",
            "note": "PLACEHOLDER"}
STOWE_RES_C = ("Town of Stowe, 'Official Results - Annual Town "
               "and School Meeting, March 3, 2026', signed and "
               "certified by Penny A. Davis, Town Clerk (town "
               "website, Election Information & Results page)")
STOWE_REP_C = ("Town of Stowe, 2025 Annual Town Report, "
               "'ELECTED TOWN OFFICERS' list (report p. 1, "
               "pre-dating the March 2026 election) and the "
               "March 3, 2026 annual meeting warning printed in "
               "the report")
SPECS["stowe"] = spec("stowe", "Town of Stowe", [
    office("moderator", "Town Moderator",
           "Town of Stowe Town Moderator", 1,
           [charter153("sec. 401(a) lists the Moderator among "
                       "the town's elected officers"),
            S(STOWE_RESULTS, f"{STOWE_RES_C}: Article 1 (elect a "
                              "Moderator for a one-year term) "
                              "was decided by write-ins, and the "
                              "signed official tally names 'Drew "
                              "Clymer' with 75 votes, marked "
                              "ELECTED in the tally's own legend "
                              "(Leighton Detora received 20) -- a "
                              "certified write-in outcome with "
                              "the winner named in the official "
                              "results (flagged on issue #163)"),
            S(STOWE_RESULTS, f"{STOWE_REP_C}: the report names "
                              "Drew Clymer as Moderator on the "
                              "one-year term expiring 2026, so "
                              "the 2026 write-in result is his "
                              "re-election")],
           [holder("Drew Clymer", "drew-clymer")]),
    office("town-clerk", "Town Clerk",
           "Town of Stowe Town Clerk", 1,
           [charter153("sec. 401(a) lists only the Selectboard, "
                       "the Moderator, and the Listers as the "
                       "town's elected officers, and the "
                       "charter's manager provisions (sec. 502 "
                       "area) make the Town Clerk a "
                       "manager-appointed officer"),
            S(STOWE_RESULTS, "Town of Stowe official website: "
                             "the 2025 Annual Town Report lists "
                             "'Town Clerk & Treasurer - Penny "
                             "Davis' under Town Departments "
                             "(staff), and Davis certifies the "
                             "town's election results as Town "
                             "Clerk, so she is seated APPOINTED"),
            guide("lists Penny Davis as Stowe's Town Clerk")],
           [holder("Penny Davis", "penny-davis",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Stowe Town Treasurer", 1,
           [charter153("sec. 401(a) omits the Treasurer from the "
                       "town's elected officers, and the "
                       "charter's manager provisions make the "
                       "Town Treasurer a manager-appointed "
                       "officer"),
            S(STOWE_RESULTS, "Town of Stowe official website: "
                             "the 2025 Annual Town Report lists "
                             "'Town Clerk & Treasurer - Penny "
                             "Davis' under Town Departments, so "
                             "she is seated APPOINTED"),
            guide("lists Penny Davis as Stowe's Town "
                  "Treasurer")],
           [holder("Penny Davis", "penny-davis",
                   how_seated="appointed")]),
    office("selectboard", "Selectboard Member",
           "Town of Stowe Selectboard", 5,
           [charter153("sec. 401(a) lists the Selectboard among "
                       "the town's elected officers"),
            S(STOWE_SB, "Town of Stowe official website, "
                        "Selectboard page ('Elected "
                        "Officials'): Ethan Carlson, Chair "
                        "(term expires 2027); Beth Gadbois, Vice "
                        "Chair (2028); Paco Aumand (2029); Jo "
                        "Sabel Courtney (2027); Nick Donza "
                        "(2028)"),
            S(STOWE_RESULTS, f"{STOWE_RES_C}: Francis 'Paco' "
                              "Aumand was elected to the "
                              "three-year seat with 623 votes "
                              "and Nick Donza to the two-year "
                              "seat with 626 votes"),
            sb_dir("names Ethan Carlson (Chair), Francis "
                   "'Paco' Aumand, Jo Sabel Courtney, Nick "
                   "Donza, and Beth Gadbois (Vice Chair)")],
           [holder("Ethan Carlson", "ethan-carlson"),
            holder("Francis \"Paco\" Aumand", "francis-paco-aumand"),
            holder("Jo Sabel Courtney", "jo-sabel-courtney"),
            holder("Nick Donza", "nick-donza"),
            holder("Beth Gadbois", "beth-gadbois")]),
    office("lister", "Lister",
           "Town of Stowe Listers", 3,
           [charter153("sec. 401(a) lists the Listers among the "
                       "town's elected officers"),
            S(STOWE_LISTERS, "Town of Stowe official website, "
                             "Listers page ('Elected "
                             "Officials'): Paul Percy, Chair; "
                             "Adam Davis; Jeff Jackson"),
            S(STOWE_RESULTS, f"{STOWE_RES_C}: Adam Davis was "
                              "elected Lister for a three-year "
                              "term with 651 votes; the town's "
                              "Board of Listers minutes of June "
                              "3, 2026 record all three listers "
                              "sworn and serving")],
           [holder("Paul Percy", "paul-percy"),
            holder("Adam Davis", "adam-davis"),
            holder("Jeff Jackson", "jeff-jackson")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Town of Stowe Justices of the Peace", 12,
           [jp_src("lists twelve Stowe justices of the peace: "
                   "Mary S. Black, Suzanne Clark, Leighton "
                   "Detora, Lyndall Heyer, Liz Lackey, Charles "
                   "Lusk, Maura Mancini, Marina Meerburg, Janet "
                   "'Jan' Reynolds, Pall Spera, Sarah Sterner, "
                   "and Arnold Ziegel. The town's annual report "
                   "and Board of Civil Authority page print the "
                   "last name as 'Ziegler', but the listing's "
                   "form is corroborated by his own email "
                   "address in the listing and governs")],
           [holder("Mary S. Black", "mary-s-black"),
            holder("Suzanne Clark", "suzanne-clark"),
            holder("Leighton Detora", "leighton-detora"),
            holder("Lyndall Heyer", "lyndall-heyer"),
            holder("Liz Lackey", "liz-lackey"),
            holder("Charles Lusk", "charles-lusk"),
            holder("Maura Mancini", "maura-mancini"),
            holder("Marina Meerburg", "marina-meerburg"),
            holder("Janet \"Jan\" Reynolds", "janet-jan-reynolds",
                   ballot_name="Janet 'Jan' Reynolds"),
            holder("Pall Spera", "pall-spera"),
            holder("Sarah Sterner", "sarah-sterner"),
            holder("Arnold Ziegel", "arnold-ziegel")]),
], jp=jp_election("stowe-vt", "Town of Stowe", 12,
                  "the certified listing names twelve winners "
                  "for Stowe's twelve justice of the peace "
                  "seats. At the March 3, 2026 town meeting the "
                  "voters adopted a floor article increasing the "
                  "slate to fifteen for the next cycle; that "
                  "change takes effect with the November 2026 "
                  "election and does not alter the 2024 slate "
                  "recorded here"))

ORDER = ["st-albans-61750", "st-albans", "st-george",
         "st-johnsbury", "stamford", "stannard", "starksboro",
         "stockbridge", "stowe", "strafford"]

for slug in ORDER:
    (OUT / f"{slug}.json").write_text(
        json.dumps(SPECS[slug], indent=1) + "\n")
print("wrote", len(ORDER), "specs")
