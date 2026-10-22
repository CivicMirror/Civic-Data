#!/usr/bin/env python3
"""VT #163 school pass -- batch 1 specs (districts 1-10 alphabetical).
Emits scripts/vt_school_data/<slug>.json for build_vt_school.py.
Research: scripts/../vt163_school_work/batch1_research.md (in
~/workspace/vt163_school_work); adjudications by Boone 2026-10-22."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "vt_school_data"
R = "2026-10-22"


def S(url, note):
    return {"url": url, "note": note, "retrieved": R}


def H(name, slug, **kw):
    h = {"name": name, "slug": slug}
    h.update(kw)
    return h


def emit(slug, name, jsources, org_name, board_sources, posts, directors):
    spec = {"district_slug": slug, "district_name": name,
            "jurisdiction_sources": jsources,
            "board": {"org_name": org_name, "sources": board_sources},
            "posts": posts, "directors": directors}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{slug}.json").write_text(json.dumps(spec, indent=1))
    print("emitted", slug)


STATUTE603 = ("https://legislature.vermont.gov/statutes/section/"
              "16/010/00603")

# ---- 1. Addison Central --------------------------------------------
ACSD_PAGE = S(
    "https://www.acsdvt.org/domain/75",
    "Addison Central School District board page (official): 'The "
    "ACSD Board is made of 13 elected members who represent the "
    "citizens of Bridport, Cornwall, Middlebury, Ripton, Salisbury, "
    "Shoreham, and Weybridge' -- the current roster page, naming "
    "all thirteen directors.")
ACSD_ARTICLES = S(
    "https://education.vermont.gov/sites/aoe/files/documents/edu-study-committee-report-addison-central.pdf",
    "Addison Central articles of agreement, as reproduced in the "
    "AOE study committee report: 'The initial Board shall consist "
    "of thirteen Directors, seven being residents of Middlebury, "
    "and one each being a resident from Bridport, Cornwall, "
    "Ripton, Salisbury, Shoreham, and Weybridge... Directors "
    "shall be elected by the voters of all forming towns of the "
    "district.' Modified at-large model (16 V.S.A. section "
    "730(a)(2)): seats allocated by town of residence, all "
    "elected district-wide.")
emit(
    "addison-central", "Addison Central School District",
    [S(STATUTE603,
       "16 V.S.A. section 603(a) inventory: the Addison Central "
       "Supervisory District's sole district is the Addison "
       "Central School District (unified union; member towns "
       "Bridport, Cornwall, Middlebury, Ripton, Salisbury, "
       "Shoreham, Weybridge)."),
     S("https://www.acsdvt.org",
       "Addison Central School District (official district "
       "website).")],
    "Addison Central School Board",
    [ACSD_PAGE, ACSD_ARTICLES],
    [{"key": "school-director", "title": "School Director",
      "seats": 13}],
    [H(n, s, sources=[ACSD_PAGE]) for n, s in [
        ("Steve Cash", "steve-cash"), ("Jason Chance", "jason-chance"),
        ("James Clark", "james-clark"),
        ("Laura Harthan", "laura-harthan"),
        ("Ron Makleff", "ron-makleff"),
        ("Jamie McCallum", "jamie-mccallum"),
        ("Mary Heather Noble", "mary-heather-noble"),
        ("Steve Orzech", "steve-orzech"),
        ("Robyn Stattel", "robyn-stattel"),
        ("Jess Venable-Novak", "jess-venable-novak"),
        ("Ellen Whelan-Wuest", "ellen-whelan-wuest")]],
)
# HELD from this build (disclosed on #163): Ann Mason and Abby
# Murphy sit on the roster with partial/1-year term labels, absent
# from the March 2026 results, while the district anticipated
# appointing to the open Middlebury seat -- how_seated unresolved
# for both. Barbara Wilson (chair, term to 2027) left the roster
# with no documented departure.

# ---- 2. Addison Northwest ------------------------------------------
ANW_J = [S(STATUTE603,
           "16 V.S.A. section 603(a) inventory: the Addison "
           "Northwest Supervisory District's sole district is the "
           "Addison Northwest School District (unified union; "
           "member towns Addison, Ferrisburgh, Panton, Vergennes, "
           "Waltham)."),
         S("https://www.anwsd.org",
           "Addison Northwest School District (official district "
           "website).")]
ANW_MODEL = S(
    "https://pantonvt.gov/wp-content/uploads/sites/52/2026/08/2025-Town-Report.pdf",
    "Addison Northwest elects its directors proportional-to-town "
    "(16 V.S.A. section 730(a)(1)): each town elects its own "
    "allocated director(s) on its own ballot -- the Town of "
    "Panton 2025 Town Report (published 2026) lists a single "
    "'Addison Northwest School District Board Representative' "
    "among the town's elected officers. Seat counts confirmed "
    "from town sources: Vergennes 4, Panton 1, Waltham 1; the "
    "Addison and Ferrisburgh allocations could not be confirmed "
    "from an official source, so no posts are modeled for those "
    "towns yet.")
emit(
    "addison-northwest", "Addison Northwest School District",
    ANW_J, "Addison Northwest School Board", [ANW_MODEL],
    [{"key": "school-director-vergennes",
      "title": "School Director - Vergennes", "seats": 4},
     {"key": "school-director-panton",
      "title": "School Director - Panton", "seats": 1},
     {"key": "school-director-waltham",
      "title": "School Director - Waltham", "seats": 1}],
    [H("Martha DeGraaf", "martha-degraaf",
       existing_person_id="ocd-person/24f0ff68-dda3-542c-a723-6b1277ce4734",
       post="school-director-panton",
       sources=[S("https://pantonvt.gov/wp-content/uploads/sites/52/2026/08/2025-Town-Report.pdf",
                  "Town of Panton 2025 Town Report (published "
                  "2026): 'Addison Northwest School District Board "
                  "Representative -- Martha DeGraaf -- 2028 "
                  "(3-year term)'.")])],
)

# ---- 3. Alburgh -----------------------------------------------------
ALB_BALLOT = S(
    "https://alburghvt.org/wp-content/uploads/2024/02/ALBURGH-VT-BALLOT-PROOF-030524.pdf",
    "Alburgh Town School District official ballot, March 5, 2024 "
    "(posted by the Town of Alburgh): separate single-seat SCHOOL "
    "DIRECTOR races by term length, each voted by the whole town "
    "electorate -- the board is five directors elected at-large "
    "(16 V.S.A. section 423(b) size). The 2024 winners were Luke "
    "Richter and Jennifer Fenn.")
ALB_MINUTES = S(
    "https://core-docs.s3.us-east-1.amazonaws.com/documents/asset/uploaded_file/3270/GISU/4341977/Alburgh_Agenda_and_Packet_05.20.2024.pdf",
    "Alburgh School Board minutes in the Grand Isle Supervisory "
    "Union packet for May 20, 2024: the board sits as Whitney "
    "Maxham (Chair), Jennifer Fenn (Vice-Chair), Luke Richter "
    "(Clerk), Cheryl Dunn and Heather Darby.")
ALB_REPORT = S(
    "https://alburghvt.org/wp-content/uploads/2026/02/Alburgh-Town-Report-2025-FINAL.pdf",
    "Town of Alburgh Town Report 2025 (published February 2026), "
    "officers list: the district's directors are Whitney Maxham, "
    "Jennifer Fenn, Luke Richter, Cheryl Dunn and Heather Darby "
    "-- the roster's currency rests on this report; no district "
    "minutes after June 2024 were locatable.")
ALB_APPT = S(
    "https://5il.co/2ghf0",
    "Alburgh School Board reorganization minutes, March 11, 2024 "
    "(GISU document system): Stacey Gould and Tara Bessette "
    "resigned at the meeting and the minutes state the vacancies "
    "would be filled by appointment. Cheryl Dunn and Heather "
    "Darby sit as full board members from May 2024 (May 20, 2024 "
    "packet) and are recorded appointed on that chain; the "
    "appointment vote itself (April 2024) was not fetched.")
emit(
    "alburgh", "Alburgh School District",
    [S(STATUTE603,
       "16 V.S.A. section 603(a) inventory: Alburgh School "
       "District, a town school district in the Grand Isle "
       "Supervisory Union (member town: Alburgh)."),
     S("https://www.alburghschool.org",
       "Alburgh Community Education Center (official school "
       "website); board documents are posted through the Grand "
       "Isle Supervisory Union.")],
    "Alburgh School Board", [ALB_BALLOT, ALB_MINUTES, ALB_REPORT],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H("Whitney Maxham", "whitney-maxham",
       sources=[ALB_MINUTES, ALB_REPORT]),
     H("Jennifer Fenn", "jennifer-fenn",
       sources=[ALB_BALLOT, ALB_MINUTES, ALB_REPORT]),
     H("Luke Richter", "luke-richter",
       sources=[ALB_BALLOT, ALB_MINUTES, ALB_REPORT]),
     H("Cheryl Dunn", "cheryl-dunn",
       how_seated="appointed",
       existing_person_id="ocd-person/928b8830-b918-5a7c-9dc4-e56aef60a3cc",
       sources=[ALB_APPT, ALB_MINUTES,
                S("https://alburghvt.org/wp-content/uploads/2026/02/Alburgh-Town-Report-2025-FINAL.pdf",
                  "Identity: this is the Alburgh Cheryl Dunn who "
                  "holds the town lister, village clerk, village "
                  "treasurer and collector offices in this "
                  "dataset (same name, same town of Alburgh, same "
                  "civic-office profile); her existing person "
                  "record is reused.")]),
     H("Heather Darby", "heather-darby",
       how_seated="appointed", sources=[ALB_APPT, ALB_MINUTES])],
)

# ---- 4. Arlington ----------------------------------------------------
ARL_HANDBOOK = S(
    "https://4.files.edl.io/86f9/08/07/26/151911-444cad6f-f55e-44ef-9903-69dbc74cbad8.pdf",
    "Arlington School District Family Handbook 2026-27 (the "
    "board's own current listing): five directors -- Todd Wilkins "
    "(Chair), Dan Wood (Vice-Chair), Teresa Sweet (Clerk), Nicol "
    "Whalen, Chelsea Thompson -- with staggered terms expiring "
    "2026/2027/2028, the section 423(b) five-member town board, "
    "elected at-large by the town's voters.")
emit(
    "arlington", "Arlington School District",
    [S(STATUTE603,
       "16 V.S.A. section 603(a) inventory: Arlington School "
       "District, a town school district in the Southwest "
       "Vermont Supervisory Union (member town: Arlington)."),
     S("https://www.svsu.org",
       "Southwest Vermont Supervisory Union (official site "
       "hosting the district's documents).")],
    "Arlington School Board", [ARL_HANDBOOK],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H("Todd Wilkins", "todd-wilkins", sources=[ARL_HANDBOOK]),
     H("Dan Wood", "dan-wood", sources=[ARL_HANDBOOK]),
     H("Teresa Sweet", "teresa-sweet",
       sources=[S("https://4.files.edl.io/86f9/08/07/26/151911-444cad6f-f55e-44ef-9903-69dbc74cbad8.pdf",
                  "Arlington School District Family Handbook "
                  "2026-27 lists Teresa Sweet as a director and "
                  "the board's Clerk, but prints her term "
                  "expiring 2026 (at the March 2026 annual "
                  "meeting, before the handbook's own school "
                  "year). Her March 2026 outcome is not "
                  "documented in a fetched source; she is "
                  "recorded as the sitting director on the "
                  "current-year handbook, with the stale expiry "
                  "disclosed.")]),
     H("Nicol Whalen", "nicol-whalen", sources=[ARL_HANDBOOK]),
     H("Chelsea Thompson", "chelsea-thompson",
       sources=[ARL_HANDBOOK])],
)

# ---- 5. Athens Grafton ------------------------------------------------
AG_MINUTES = S(
    "http://wnesu.community.highbond.com/document/8152f4b7-dc2e-4533-b46e-f5162adef9fe/",
    "Athens Grafton School District board minutes, April 30, "
    "2026 (Windham Northeast SU document portal): 'Present: "
    "Cathy Siano-Goodwin, Lynn Morgan, Krista Gay, Hardy Merrill, "
    "Rachel Plummer, and Mark Berman' with none absent -- the "
    "full six-member board; identical full attendance in the "
    "November 13, 2025 minutes.")
AG_MODEL = S(
    "https://graftonvt.org/wp-content/uploads/2022/05/Warning-WNUESD-District-Meeting-05.24.2022.pdf",
    "Warning for the May 24, 2022 district meeting (Athens and "
    "Grafton, then the Windham Northeast Union Elementary School "
    "District), Article 6: the voters modified the articles of "
    "agreement to add one district-wide-elected resident seat "
    "per town, producing the current board of six -- three seats "
    "allocated to Athens residents, three to Grafton residents, "
    "all elected by the district's voters as a whole (modified "
    "at-large). The 2022 article framed the added seats as one "
    "term; the board has sat at six continuously since, and no "
    "fetched document makes the structure expressly permanent.")
emit(
    "athens-grafton", "Athens Grafton School District",
    [S(STATUTE603,
       "16 V.S.A. section 603(a) inventory: Athens Grafton "
       "School District, a union school district in the Windham "
       "Northeast Supervisory Union (member towns Athens and "
       "Grafton; formed as the Windham Northeast Union "
       "Elementary School District, renamed 2023 after "
       "Westminster's 2022 withdrawal)."),
     S("https://www.wnesu.org",
       "Windham Northeast Supervisory Union (official site; the "
       "district's documents post to its board portal).")],
    "Athens Grafton School Board", [AG_MODEL, AG_MINUTES],
    [{"key": "school-director", "title": "School Director",
      "seats": 6}],
    [H("Lynn Morgan", "lynn-morgan", sources=[AG_MINUTES]),
     H("Krista Gay", "krista-gay", existing_person_id="ocd-person/a759dc54-3630-5367-9f5e-b33ecbd345e4", sources=[AG_MINUTES]),
     H("Mark Berman", "mark-berman",
       sources=[S("http://wnesu.community.highbond.com/document/8152f4b7-dc2e-4533-b46e-f5162adef9fe/",
                  "Athens Grafton board minutes (April 30, 2026; "
                  "also November 13, 2025) seat Mark Berman as a "
                  "director, and he signed the district's January "
                  "2026 annual-meeting warning with a term to "
                  "2027. His allocation to the Athens seat-group "
                  "rests on residence evidence (Athens Selectboard "
                  "minutes, March 20, 2025, appoint him to the "
                  "Athens Planning Commission); no fetched school "
                  "source town-labels him.")]),
     H("Cathy Siano-Goodwin", "cathy-siano-goodwin",
       sources=[S("http://wnesu.community.highbond.com/document/8152f4b7-dc2e-4533-b46e-f5162adef9fe/",
                  "Athens Grafton board minutes (April 30, 2026; "
                  "also November 13, 2025) seat Cathy "
                  "Siano-Goodwin as a director. Her documented "
                  "two-year term (Grafton Town Report 2024) "
                  "expired in 2025 and no fetched election source "
                  "documents her re-election; she serves "
                  "continuously through April 2026 and is "
                  "recorded on that continuity.")]),
     H("Hardy Merrill", "hardy-merrill", existing_person_id="ocd-person/b2082476-2944-5009-90d9-79386b1dbdde", sources=[AG_MINUTES]),
     H("Rachel Plummer", "rachel-plummer", sources=[AG_MINUTES])],
)
print("part 1 done")

# ---- 6. Barre Unified -------------------------------------------------
BARRE_ARTICLES = S(
    "https://resources.finalsite.net/images/v1697666999/bsuvtorg/gjsrmmniaistgg4qj9ii/2019-03-12-AmendedArticlesofAgreementFINAL.pdf",
    "Barre Unified Union School District amended Articles of "
    "Agreement (voter-approved February 19, 2019): 'The Board of "
    "School Directors shall have nine (9) members, with four (4) "
    "residing in and representing Barre City; and four (4) "
    "residing in and representing Barre Town; and one (1) elected "
    "at-large by the voters of both municipalities.' The eight "
    "town seats are elected by that municipality's voters only; "
    "terms are three years, staggered. (The State Board's "
    "original November 2018 default articles, still hosted by "
    "the AOE, set a four-member board and are superseded.)")
BARRE_PAGE = S(
    "http://www.buusd.org/district/board",
    "Barre Unified Union School District, 'Our Board of "
    "Directors' (official, live): the nine current directors with "
    "their seats and term ends; the same nine are listed as "
    "present, none absent, in the board's March 9, 2026 and "
    "September 8, 2026 regular-meeting minutes.")
BARRE_CITY = [BARRE_ARTICLES, BARRE_PAGE]
emit(
    "barre-unified-union", "Barre Unified Union School District",
    [S(STATUTE603,
       "16 V.S.A. section 603(a) inventory: Barre Unified Union "
       "School District, a unified union district that is its "
       "own supervisory district (member municipalities Barre "
       "City and Barre Town)."),
     S("https://www.buusd.org",
       "Barre Unified Union School District (official district "
       "website).")],
    "Barre Unified Union School Board",
    [BARRE_ARTICLES, BARRE_PAGE],
    [{"key": "school-director-barre-city",
      "title": "School Director - Barre City", "seats": 4},
     {"key": "school-director-barre-town",
      "title": "School Director - Barre Town", "seats": 4},
     {"key": "school-director-at-large",
      "title": "School Director - At-Large", "seats": 1}],
    [H("Garrett Grant", "garrett-grant",
       post="school-director-barre-city", sources=BARRE_CITY),
     H("Giuliano Cecchinelli II", "giuliano-cecchinelli-ii",
       post="school-director-barre-city", sources=BARRE_CITY),
     H("Jeffrey Eddy", "jeffrey-eddy",
       post="school-director-barre-city", sources=BARRE_CITY),
     H("Samn Stockwell", "samn-stockwell",
       post="school-director-barre-city", sources=BARRE_CITY),
     H("Emily Wheeler Reynolds", "emily-wheeler-reynolds",
       post="school-director-barre-town", sources=BARRE_CITY),
     H("Lindsey Wells", "lindsey-wells",
       post="school-director-barre-town", sources=BARRE_CITY),
     H("Ian Campbell", "ian-campbell",
       post="school-director-barre-town", sources=BARRE_CITY),
     H("Catherine Whalen", "catherine-whalen",
       post="school-director-barre-town", sources=BARRE_CITY),
     H("Jackie Wheeler", "jackie-wheeler",
       post="school-director-at-large", sources=BARRE_CITY),
     H("Michael Boutin", "michael-boutin",
       post="school-director-barre-city", end="2026",
       sources=[S("https://resources.finalsite.net/images/v1778263581/bsuvtorg/cvrmlnd883nlr6dj5tqy/2026-04-06-Minutes.pdf",
                  "Michael Boutin chaired the Barre Unified board "
                  "as a Barre City director into February 2026 "
                  "(the district's April 16, 2025 press release "
                  "names him Chair; he chaired the February 12, "
                  "2026 meeting). He is absent from the March 9, "
                  "2026 reorganization minutes and the current "
                  "board page, and appears as a public attendee "
                  "in the April 6, 2026 minutes -- his "
                  "membership is ended in 2026; whether he lost "
                  "or did not seek re-election is not stated in "
                  "the fetched sources.")])],
)

# ---- 8. Bellows Falls Union High School -------------------------------
BF_WARNING = S(
    "https://wnesu.community.highbond.com/document/22308?lastModified=639165454326030000",
    "Bellows Falls Union High School District annual-meeting "
    "warning (board-approved February 16, 2026, in the June 8, "
    "2026 board agenda packet): the signature block lists all "
    "ten directors with term-end years -- Chris Hodsden (Chair), "
    "Jamie Storrow, June Streeter, Kim Keefe, Mary Howard Hall, "
    "Paul Obuchowski, Ginger Driscoll, Emily Bragonier, Ben "
    "Wallace, Emily Ferenc. Directors are elected by their "
    "member districts, not at the union meeting (16 V.S.A. "
    "section 706k(a)); the March 9, 2026 board minutes list the "
    "same ten in attendance. The current per-town allocation of "
    "the ten seats could not be re-verified (the last full "
    "allocation on record is 2020: Rockingham 5, Westminster 3, "
    "Grafton 1, Athens 1; only Bragonier = Westminster is "
    "confirmed current), so the board is modeled as one "
    "ten-seat post.")
emit(
    "bellows-falls-union-high-school",
    "Bellows Falls Union High School District",
    [S(STATUTE603,
       "16 V.S.A. section 603(a) inventory: Bellows Falls Union "
       "High School District (District No. 27), a union high "
       "school district in the Windham Northeast Supervisory "
       "Union (member districts Athens Grafton, Rockingham and "
       "Westminster)."),
     S("https://bfuhs.wnesu.org",
       "Bellows Falls Union High School (official school "
       "website); board materials post to the Windham Northeast "
       "SU document portal.")],
    "Bellows Falls Union High School Board", [BF_WARNING],
    [{"key": "school-director", "title": "School Director",
      "seats": 10}],
    [H("Chris Hodsden", "chris-hodsden", sources=[BF_WARNING]),
     H("Jamie Storrow", "jamie-storrow", sources=[BF_WARNING]),
     H("June Streeter", "june-streeter", sources=[BF_WARNING]),
     H("Kim Keefe", "kim-keefe", sources=[BF_WARNING]),
     H("Mary Howard Hall", "mary-howard-hall", sources=[BF_WARNING]),
     H("Paul Obuchowski", "paul-obuchowski",
       existing_person_id="ocd-person/6d6d72e1-192d-5297-9e70-0ca72fb41e6f",
       sources=[BF_WARNING]),
     H("Ginger Driscoll", "ginger-driscoll", sources=[BF_WARNING]),
     H("Emily Bragonier", "emily-bragonier", sources=[BF_WARNING]),
     H("Ben Wallace", "ben-wallace", sources=[BF_WARNING]),
     H("Emily Ferenc", "emily-ferenc", sources=[BF_WARNING])],
)

# ---- 9. Blue Mountain Union --------------------------------------------
BMU_PAGE = S(
    "https://www.oesu.org/fs/pages/359",
    "Blue Mountain Union School District board page (Orange "
    "East Supervisory Union, official): nine directors with "
    "towns and terms -- Ryegate: Shawn Burroughs, James Jobin, "
    "Daniel LaCoss (Vice-Chair), Anna Morrison; Groton: Sasha "
    "Emerson, Megan Foy, Willis Page; Wells River: Kelsey "
    "Root-Winchester (Chair), Alissa Smith. The same nine sign "
    "the district's March 12, 2026 budget-vote warning. "
    "Directors are elected by their own member towns (16 V.S.A. "
    "section 706k(a)); the member town is Wells River village "
    "(in Newbury), not the whole town of Newbury, per the "
    "district's 2026 warning.")
emit(
    "blue-mountain-union", "Blue Mountain Union School District",
    [S(STATUTE603,
       "16 V.S.A. section 603(a) inventory: Blue Mountain Union "
       "School District (District No. 21), a union (PK-12) "
       "district in the Orange East Supervisory Union (member "
       "towns Groton, Ryegate and Wells River village)."),
     S("https://www.oesu.org",
       "Orange East Supervisory Union (official site hosting the "
       "district's board page).")],
    "Blue Mountain Union School Board", [BMU_PAGE],
    [{"key": "school-director-ryegate",
      "title": "School Director - Ryegate", "seats": 4},
     {"key": "school-director-groton",
      "title": "School Director - Groton", "seats": 3},
     {"key": "school-director-wells-river",
      "title": "School Director - Wells River", "seats": 2}],
    [H("Shawn Burroughs", "shawn-burroughs",
       post="school-director-ryegate", sources=[BMU_PAGE]),
     H("James Jobin", "james-jobin",
       post="school-director-ryegate", sources=[BMU_PAGE]),
     H("Daniel LaCoss", "daniel-lacoss",
       post="school-director-ryegate", sources=[BMU_PAGE]),
     H("Anna Morrison", "anna-morrison",
       post="school-director-ryegate", sources=[BMU_PAGE]),
     H("Sasha Emerson", "sasha-emerson",
       post="school-director-groton", sources=[BMU_PAGE]),
     H("Megan Foy", "megan-foy",
       post="school-director-groton", sources=[BMU_PAGE]),
     H("Willis Page", "willis-page",
       post="school-director-groton", sources=[BMU_PAGE]),
     H("Kelsey Root-Winchester", "kelsey-root-winchester",
       post="school-director-wells-river", sources=[BMU_PAGE]),
     H("Alissa Smith", "alissa-smith",
       post="school-director-wells-river", sources=[BMU_PAGE])],
)

# ---- 10. Brighton -------------------------------------------------------
BRI_REPORT = S(
    "https://brightonvt.org/wp-content/uploads/2024/02/Town-of-Brighton-Annual-Report-2023.pdf",
    "Town of Brighton Annual Report 2023 (official town site), "
    "officers list: five School Directors (the electorate added "
    "two seats to the 16 V.S.A. section 423 default of three). "
    "No later district-sourced roster was obtainable: the "
    "district has no board page on the North Country SU site, "
    "and the town's 2024 report is flipbook-only. The post is "
    "modeled at five seats on the town's own last roster, with "
    "only the directors below verified as current.")
BRI_NCSU = S(
    "https://www.ncsuvt.org/33945_3",
    "North Country Supervisory Union 'Full Board' page "
    "(official): 'Brighton: Judy Castonguay, Moriah Gaboriault "
    "Alternate: Gayle Cornelius' -- the district's "
    "representatives to the supervisory union board, who are "
    "drawn from the district's own board (16 V.S.A. section "
    "266). Castonguay and Gaboriault are recorded as current "
    "Brighton directors on this listing; Cornelius, listed as "
    "the alternate, is held pending a district-source roster.")
emit(
    "brighton", "Brighton School District",
    [S(STATUTE603,
       "16 V.S.A. section 603(a) inventory: Brighton School "
       "District, a town school district in the North Country "
       "Supervisory Union (member town: Brighton)."),
     S("https://www.ncsuvt.org",
       "North Country Supervisory Union (official site).")],
    "Brighton School Board", [BRI_REPORT, BRI_NCSU],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H("Judy Castonguay", "judy-castonguay", existing_person_id="ocd-person/19317071-5f7a-52ad-bf08-f4a78f1ff89d", sources=[BRI_NCSU]),
     H("Moriah Gaboriault", "moriah-gaboriault",
       sources=[BRI_NCSU])],
)
print("part 2 done (Barstow appended separately)")

# ---- 7. Barstow Unified (added after the RNESU browser read) -----------
BAR_PAGE = S(
    "https://www.rnesu.org/page/district-information-school-boards-barstow-board",
    "Barstow Unified Union School District board page (Rutland "
    "Northeast Supervisory Union, official): 'School Board "
    "Officers' -- Tony Roberts (At-Large - Chittenden, 2027, "
    "Chair); Justine Calnan Cavacas (Chittenden, 2027, Clerk); "
    "Deborah Singiser (At-Large - Chittenden, 2029); Leo Pond "
    "(Chittenden, 2028); Gregory Smith (Mendon, 2028). The board "
    "is five directors -- Chittenden 2, Mendon 1, At-Large 2 -- "
    "the town seats elected by that town's voters only and the "
    "at-large seats by both towns, per the district's formation "
    "articles as amended November 6, 2018 (second at-large seat "
    "added). Corroborated by the board's October 5, 2026 "
    "special-meeting minutes (Roberts, Singiser, Pond and "
    "Cavacas present) and, for Cavacas and Singiser, by RNESU's "
    "official March 4, 2026 results post naming them elected on "
    "March 3, 2026.")
emit(
    "barstow-unified-union", "Barstow Unified Union School District",
    [S(STATUTE603,
       "16 V.S.A. section 603(a) inventory: Barstow Unified "
       "Union School District, a unified union district in the "
       "Rutland Northeast Supervisory Union (member towns "
       "Chittenden and Mendon)."),
     S("https://www.rnesu.org",
       "Rutland Northeast Supervisory Union (official site "
       "hosting the district's board page).")],
    "Barstow Unified Union School Board", [BAR_PAGE],
    [{"key": "school-director-chittenden",
      "title": "School Director - Chittenden", "seats": 2},
     {"key": "school-director-mendon",
      "title": "School Director - Mendon", "seats": 1},
     {"key": "school-director-at-large",
      "title": "School Director - At-Large", "seats": 2}],
    [H("Justine Calnan Cavacas", "justine-calnan-cavacas",
       post="school-director-chittenden", sources=[BAR_PAGE]),
     H("Leo Pond", "leo-pond",
       post="school-director-chittenden", sources=[BAR_PAGE]),
     H("Gregory Smith", "gregory-smith",
       post="school-director-mendon", sources=[BAR_PAGE]),
     H("Tony Roberts", "tony-roberts",
       post="school-director-at-large", sources=[BAR_PAGE]),
     H("Deborah Singiser", "deborah-singiser",
       post="school-director-at-large", sources=[BAR_PAGE])],
)
print("barstow appended")
