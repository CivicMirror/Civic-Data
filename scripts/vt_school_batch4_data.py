#!/usr/bin/env python3
"""VT #163 school pass -- batch 4 specs (districts 31-40).
Research: ~/workspace/vt163_school_work/batch4_research_{a,b}.md;
adjudications by Boone 2026-10-22 (Georgia structure-only;
Green Mountain jurisdiction+org only; Hartland Swartz/Wilson/
Charland and Hazen's Holland held)."""
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


def emit(slug, name, jsources, org_name, board_sources, posts,
         directors):
    spec = {"district_slug": slug, "district_name": name,
            "jurisdiction_sources": jsources,
            "board": {"org_name": org_name, "sources": board_sources},
            "posts": posts, "directors": directors}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{slug}.json").write_text(json.dumps(spec, indent=1))
    print("emitted", slug)


ST = "https://legislature.vermont.gov/statutes/section/16/010/00603"
FWSU_APP = ("FWSU's official 2017 Alternative Structure Application "
            "to the State Board of Education states each Franklin "
            "West district 'maintains a 5-person board of school "
            "directors'.")

# ---- 31. Fletcher ---------------------------------------------------------
FL_PAGE = S(
    "https://www.fwsu.org/page/fletcher-school-board",
    "Fletcher School Board page (Franklin West SU, official): "
    "five directors -- Jess Graff (Chair), David Clark, "
    "Stephanie Sheldon-Purinton (Clerk), Allison Stafford, "
    "Morgan Lawton. The board is five directors at-large (16 "
    "V.S.A. section 423(a)-(b); " + FWSU_APP + ") No term "
    "expirations are published in any fetched official source "
    "(the missing document is the Fletcher FY27 Combined "
    "Warning / 2026 annual meeting record), so no ends are "
    "asserted. The one documented appointment (a 2024 vacancy) "
    "returned its seat to election in March 2025; there is no "
    "evidence any current member is an appointee, and all five "
    "are recorded elected on the district's own roster.")
emit(
    "fletcher", "Fletcher School District",
    [S(ST, "16 V.S.A. section 603(a) inventory: Fletcher "
           "School District, a town school district in the "
           "Franklin West Supervisory Union (member town: "
           "Fletcher)."),
     S("https://www.fwsu.org",
       "Franklin West Supervisory Union (official site).")],
    "Fletcher School Board", [FL_PAGE],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H("Jess Graff", "jess-graff", sources=[FL_PAGE]),
     H("David Clark", "david-clark",
       existing_person_id="ocd-person/9010f855-0789-5485-ba4f-fc3f53af94d4",
       sources=[FL_PAGE]),
     H("Stephanie Sheldon-Purinton", "stephanie-sheldon-purinton",
       sources=[FL_PAGE]),
     H("Allison Stafford", "allison-stafford", sources=[FL_PAGE]),
     H("Morgan Lawton", "morgan-lawton", sources=[FL_PAGE])],
)

# ---- 32. Georgia -- STRUCTURE ONLY (all memberships held) -------------------
GE_PAGE = S(
    "https://www.fwsu.org/page/gems-board",
    "Georgia (GEMS) School Board page (Franklin West SU, "
    "official): five directors -- Carl Laroe (Chair), J.C. "
    "Thouin (Clerk), Grady Ballard, Lisa Mattos, Richard "
    "Dickinson. NO MEMBERSHIPS ARE RECORDED for this district: "
    "two official FWSU vacancy notices show TWO seats filled "
    "by appointment on April 14, 2026 and ONE more on May 5, "
    "2026 (all to March 2027), and no fetched official source "
    "names the appointees or identifies which of the five "
    "page-listed members are elected and which appointed. The "
    "exact missing documents are the GEMS board minutes of "
    "April 14 and May 5, 2026. Laroe, Thouin and Ballard are "
    "documented as sitting directors on March 10, 2026 "
    "(signatures on the FY27 revote warning). The board is "
    "five directors at-large (16 V.S.A. section 423(a)-(b); "
    + FWSU_APP + ")")
emit(
    "georgia", "Georgia School District",
    [S(ST, "16 V.S.A. section 603(a) inventory: Georgia School "
           "District, a town school district in the Franklin "
           "West Supervisory Union (member town: Georgia)."),
     S("https://www.fwsu.org",
       "Franklin West Supervisory Union (official site).")],
    "Georgia School Board", [GE_PAGE],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [],
)

# ---- 33. Granville-Hancock ----------------------------------------------------
GH_WARN = S(
    "https://www.wrvsu.org/o/white-river-valley-su",
    "Granville-Hancock Unified District 2026 Annual Meeting "
    "Warning (the district's own document, White River Valley "
    "SU site): the district elects at its May annual meeting -- "
    "Granville 1 director for a 3-year term, Hancock 1 for a "
    "3-year term, Granville 1 for two years (remainder of a "
    "3-year term). The board is six directors, three per town, "
    "elected by town-only electorates (the section 730(a)(1) "
    "pattern; AOE State Board Item Q-3, 2017: members 'elected "
    "by the voters of each town... allocated at three members "
    "each').")
GH_MIN = S(
    "https://wrvsu.org/pages/2ec91ffc-bb89-4644-9398-82178a4d5a16",
    "Granville-Hancock board page and approved minutes (White "
    "River Valley SU, official): May 18, 2026 reorganization "
    "seats Peters (Chair), Sheehan (Vice Chair), Deering "
    "(Clerk) and Neale; Anderson seated and voting June 16, "
    "2026; August 25, 2026 minutes appoint Rachel Alberico to "
    "the vacant Granville seat. Term expirations are from the "
    "2026 warning's signature block and the Town of Granville "
    "officials page (Peters 2027, Neale 2027, Deering 2028, "
    "Sheehan 2029). Which Granville seat Anderson won on May "
    "12, 2026 (the 3-year seat vs. the 2-year remainder) is not "
    "stated in any fetched minutes -- the missing document is "
    "the May 12, 2026 annual meeting minutes -- so Anderson "
    "and Alberico carry no term end.")
emit(
    "granville-hancock-unified", "Granville-Hancock Unified District",
    [S(ST, "16 V.S.A. section 603(a) inventory: Granville-"
           "Hancock Unified District, a unified union district "
           "in the White River Valley Supervisory Union (member "
           "towns Granville and Hancock). Non-operating "
           "(tuitions all students)."),
     S("https://www.wrvsu.org",
       "White River Valley Supervisory Union (official site).")],
    "Granville-Hancock Unified School Board", [GH_WARN, GH_MIN],
    [{"key": "school-director-granville",
      "title": "School Director - Granville", "seats": 3},
     {"key": "school-director-hancock",
      "title": "School Director - Hancock", "seats": 3}],
    [H("Siobhan Neale", "siobhan-neale",
       post="school-director-granville", sources=[GH_WARN, GH_MIN]),
     H("Clayton Anderson", "clayton-anderson",
       post="school-director-granville",
       sources=[S("https://www.wrvsu.org/o/white-river-valley-su",
                  "Clayton Anderson was APPOINTED August 5, 2025 "
                  "to Tammi Beattie's vacant Granville seat "
                  "('for the remainder of the fiscal year', "
                  "approved minutes) and then ELECTED at the May "
                  "12, 2026 annual meeting; his current "
                  "membership is the elected one. Which warned "
                  "Granville seat he won (3-year vs. 2-year "
                  "remainder) is not stated in the fetched "
                  "minutes, so no term end is asserted.")]),
     H("Rachel Alberico", "rachel-alberico",
       post="school-director-granville", how_seated="appointed",
       sources=[GH_MIN]),
     H("Stacey Peters", "stacey-peters",
       post="school-director-hancock", sources=[GH_WARN, GH_MIN]),
     H("Sara Deering", "sara-deering",
       post="school-director-hancock", sources=[GH_WARN, GH_MIN]),
     H("Samantha Sheehan", "samantha-sheehan",
       post="school-director-hancock", sources=[GH_WARN, GH_MIN]),
     H("Tammi Beattie", "tammi-beattie",
       post="school-director-granville", end="2025",
       sources=[S("https://www.wrvsu.org/o/white-river-valley-su",
                  "Tammi Beattie's Granville seat fell vacant at "
                  "the May 13, 2025 annual meeting (no candidate "
                  "nominated) and stood vacant until Anderson's "
                  "August 5, 2025 appointment. Ended 2025.")]),
     H("Juli Reiderer", "juli-reiderer",
       post="school-director-granville", end="2026",
       sources=[S("https://www.wrvsu.org/o/white-river-valley-su",
                  "Juli Reiderer (Granville, Clerk; term "
                  "expiring 2026) was not returned at the May 12, "
                  "2026 annual meeting. Ended 2026.")])],
)

# ---- 34. Green Mountain -- JURISDICTION + ORG ONLY (posts held) ----------------
GM_SRC = S(
    "https://www.trsu.org/boards/gmusd-info",
    "Green Mountain Unified School District (Two Rivers SU, "
    "official info page; minutes in the district's Drive "
    "folders). The board has ELEVEN directors (roll calls, Feb. "
    "19 and Aug. 20, 2026 minutes), town-allocated and elected "
    "by town electorates -- proven for Andover by the Town of "
    "Andover 2023 Town Report's GMUSD director returns. NO "
    "POSTS OR MEMBERSHIPS ARE RECORDED: no fetched official "
    "source states the per-town seat allocation or any "
    "member's town or term, and the district's adopted "
    "Articles of Agreement were not obtained (the exact "
    "missing documents are the 2017 adopted articles and the "
    "2026 Annual Meeting Warning / March 3, 2026 town "
    "returns). Roster of record (Aug. 20, 2026, all eleven "
    "present): Lisa Sanders (Chair), Patricia Benelli, Anne "
    "Henshaw (APPOINTED Mar. 19, 2026), Shayna Kalnitsky, "
    "Donovan Nichols (Vice Chair), Lois Perlah (Clerk), "
    "Michael Ripley, Adrienne Williams, Caitlin Miller "
    "(APPOINTED Mar. 19, 2026), Katie Murphy, Jerry Ucci. "
    "Departed in 2026: Casey Leahy, Jeff Hance, Kate Lamphere, "
    "Scott Kendall, Rick Alexander.")
emit(
    "green-mountain-unified", "Green Mountain Unified School District",
    [S(ST, "16 V.S.A. section 603(a) inventory: Green Mountain "
           "Unified School District, a unified union district "
           "in the Two Rivers Supervisory Union (member towns "
           "Andover, Baltimore, Cavendish, Chester)."),
     S("https://www.trsu.org",
       "Two Rivers Supervisory Union (official site).")],
    "Green Mountain Unified School Board", [GM_SRC],
    [],
    [],
)

# ---- 35. Halifax ------------------------------------------------------------------
HX_PAGE = S(
    "https://www.wswsu49.org/Meeting-Calendar/halifax-board",
    "Halifax School Board page (Windham Southwest SU, "
    "official), terms verbatim: Paul Blais (Chair, 3-year term "
    "expires 2029), Wade Ryan (Vice Chair, expires 2028), "
    "Cassandra McLaren (Clerk, expires 2028). The same three "
    "reorganize the board in the March 11, 2026 minutes and "
    "sit in the June 17, 2026 minutes. The board is the "
    "section 423(a) default three directors at-large; the "
    "district's January 23, 2025 warning put two seats up "
    "together (the stagger), won by Ryan and McLaren.")
emit(
    "halifax", "Halifax School District",
    [S(ST, "16 V.S.A. section 603(a) inventory: Halifax School "
           "District, a town school district in the Windham "
           "Southwest Supervisory Union (member town: "
           "Halifax)."),
     S("https://www.wswsu49.org",
       "Windham Southwest Supervisory Union (official site).")],
    "Halifax School Board", [HX_PAGE],
    [{"key": "school-director", "title": "School Director",
      "seats": 3}],
    [H("Paul Blais", "paul-blais",
       existing_person_id="ocd-person/019668d4-289e-572d-871d-92b1633c9175",
       sources=[HX_PAGE]),
     H("Wade Ryan", "wade-ryan", sources=[HX_PAGE]),
     H("Cassandra McLaren", "cassandra-mclaren", sources=[HX_PAGE]),
     H("Homer Sumner", "homer-sumner", end="2025",
       sources=[S("https://www.wswsu49.org/Meeting-Calendar/halifax-board",
                  "Homer Sumner signed the district's January "
                  "23, 2025 warning as a director; his seat was "
                  "one of the two warned for March 4, 2025 and "
                  "passed to Wade Ryan at that election. Ended "
                  "2025.")]),
     H("Judy Anyan", "judy-anyan", end="2025",
       sources=[S("https://www.wswsu49.org/Meeting-Calendar/halifax-board",
                  "Judy Anyan signed the district's January 23, "
                  "2025 warning as a director; her seat was one "
                  "of the two warned for March 4, 2025 and "
                  "passed to Cassandra McLaren at that election. "
                  "Ended 2025.")])],
)
print("part 1 done")

# ---- 36. Hartford ------------------------------------------------------------------
HF_MIN = S(
    "https://docs.google.com/document/d/1Tyv_fLVltfoswx-ycZM7FxG9IxBp7XVZAL57LCExFfU",
    "Hartford Board of School Directors minutes, March 4, 2026 "
    "(reorganization): 'Board Members present: Nancy Russell, "
    "Cathy Lemire, Jeremy Warren, Colin Butler, Daniel "
    "Schapira' -- Butler and Schapira welcomed as 'new Board "
    "Directors' under 'Oath of Office for Newly Elected Board "
    "Directors'. Term expirations are from the Town and School "
    "District Annual Report 2025 officials list (Russell 2027, "
    "Lemire 2028, Warren 2027) and the warned 2026 seat "
    "lengths (Butler's 3-year seat to 2029; Schapira's 2-year "
    "seat to 2028). The board is five directors at-large (16 "
    "V.S.A. section 423(a)-(b): three 3-year seats, two 2-year "
    "seats; the town's March 3, 2026 positions notice warned "
    "exactly one of each). Butler's official write-in tally "
    "was not fetched (missing: the Town Clerk's March 3, 2026 "
    "return of votes); his election is established by the "
    "minutes' 'newly elected' oath language (the district's "
    "2025 precedent is Lemire's certified write-in win).")
emit(
    "hartford", "Hartford School District",
    [S(ST, "16 V.S.A. section 603(a)(6)(C) inventory: Hartford "
           "Supervisory District -- the Hartford School "
           "District is a town school district and its own "
           "supervisory district (member town: Hartford)."),
     S("https://www.hsdvt.com",
       "Hartford School District (official district website).")],
    "Hartford School Board", [HF_MIN],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H("Nancy Russell", "nancy-russell", sources=[HF_MIN]),
     H("Cathy Lemire", "cathy-lemire", sources=[HF_MIN]),
     H("Jeremy Warren", "jeremy-warren", sources=[HF_MIN]),
     H("Colin Butler", "colin-butler", sources=[HF_MIN]),
     H("Daniel Schapira", "daniel-schapira", sources=[HF_MIN]),
     H("Kevin Christie", "kevin-christie", end="2026",
       sources=[S("https://docs.google.com/document/d/1QE4jo28DwwEEGCcXgDhtZbo5gRritKUV",
                  "Hartford board resolution, June 3, 2026: "
                  "'Kevin \"Coach\" Christie has served on the "
                  "Hartford Board of School Directors, as an "
                  "Elected Member (March, 2007 - February, "
                  "2026).' His 3-year seat passed to Colin "
                  "Butler at the March 3, 2026 election. Ended "
                  "2026.")]),
     H("Garrett Wilson", "garrett-wilson", end="2026",
       sources=[S("https://www.hartford-vt.org/DocumentCenter/View/13209/2025-Hartford-Town-and-School-District-Annual-Report",
                  "Garrett Wilson held the 2-year seat expiring "
                  "2026 (Annual Report 2025 officials list); the "
                  "seat passed to Daniel Schapira, the only "
                  "filed candidate, at the March 3, 2026 "
                  "election. Whether Wilson sought re-election "
                  "is not stated. Ended 2026.")])],
)

# ---- 37. Hartland ---------------------------------------------------------------------
HL_PAGE = S(
    "https://wsesu.net/en-US/school-board-4e29b4d1/hartland-school-board-640e8aee",
    "Hartland School Board page (Windsor Southeast SU, "
    "official): five directors -- Heather Vonada (Chair, 2027), "
    "Ryan Pezanowski (Vice Chair, 2028), Bethann Swartz "
    "(Clerk, 2027), Anthony Wilson (2027), Amanda Charland "
    "(2027). The board is five directors at-large (16 V.S.A. "
    "section 423(a)-(b): three 3-year seats, two 2-year "
    "seats -- Town Report 2026 officials list). Vonada was "
    "elected March 4, 2025 to the 2-year seat (443 votes, "
    "official abstract in Town Report 2026); Pezanowski was "
    "re-elected March 3, 2026 to the 2-year seat (his printed "
    "end moves 2026 to 2028). HELD: Swartz, Wilson and "
    "Charland -- their seating mechanisms are not established "
    "by any fetched official document (missing: the district's "
    "March 3, 2026 warning/return and its March-September 2026 "
    "minutes). Charland's September 2026 appointment rests on "
    "a labeled lead (an AI meeting summary) only.")
emit(
    "hartland", "Hartland School District",
    [S(ST, "16 V.S.A. section 603(a) inventory: Hartland "
           "School District, a town school district in the "
           "Windsor Southeast Supervisory Union (member town: "
           "Hartland)."),
     S("https://www.wsesu.net",
       "Windsor Southeast Supervisory Union (official site).")],
    "Hartland School Board", [HL_PAGE],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H("Heather Vonada", "heather-vonada", sources=[HL_PAGE]),
     H("Ryan Pezanowski", "ryan-pezanowski", sources=[HL_PAGE]),
     H("Nicole Buck", "nicole-buck", end="2025",
       sources=[S("http://hartlandvt.gov/vertical/sites/%7B47DC8B4F-778B-408C-BB00-EA7AC4E090E5%7D/uploads/Hartland_Town_Report_2026(1).pdf",
                  "Nicole Buck (Chair; 3-year seat to 2027 per "
                  "Town Report 2025) departed during 2025 -- "
                  "she is absent from the Town Report 2026 "
                  "officials list, where Bethann Swartz appears "
                  "in her seat. Ended 2025.")]),
     H("Elizabeth Roy", "elizabeth-roy", end="2026",
       sources=[S("http://hartlandvt.gov/vertical/sites/%7B47DC8B4F-778B-408C-BB00-EA7AC4E090E5%7D/uploads/Hartland_Town_Report_2026(1).pdf",
                  "Elizabeth Roy held a 3-year seat expiring "
                  "2026 (Town Report 2026 officials list); she "
                  "is absent from the current SU board page. No "
                  "fetched document states why she left. Ended "
                  "2026.")]),
     H("Hannah Foote Bensihmon", "hannah-foote-bensihmon",
       end="2026",
       sources=[S("http://hartlandvt.gov/vertical/sites/%7B47DC8B4F-778B-408C-BB00-EA7AC4E090E5%7D/uploads/Hartland_Town_Report_2026(1).pdf",
                  "Hannah Foote Bensihmon was elected March 4, "
                  "2025 to a 3-year seat (426 votes, official "
                  "abstract); she is absent from the current SU "
                  "board page and departed in 2026, well before "
                  "her term's 2028 end. No fetched document "
                  "states why. (The abstract prints 'Hannah "
                  "Bensimhon'; the officials lists' form "
                  "governs.) Ended 2026.")])],
)

# ---- 38. Harwood ---------------------------------------------------------------------------
HW_ART = S(
    "https://drive.google.com/file/d/1kLO__EbjGspdLndF3-_DeDhrJwZarjpG/view",
    "Harwood Unified Union articles of agreement (revised "
    "October 24, 2018), art. 7: the board 'shall be composed of "
    "fourteen individuals elected by Australian ballot by the "
    "voters of the municipalities in which they reside' -- "
    "Duxbury 2, Fayston 2, Moretown 2, Waitsfield 2, Warren 2, "
    "Waterbury 4, with weighted votes for proportionality (the "
    "section 730(a)(1) proportional model; art. 8 sets "
    "3-year terms). NOTE: the district's 2016 draft articles "
    "(13 seats, Waterbury 3) are SUPERSEDED -- do not use.")
HW_PAGE = S(
    "https://huusd.org/board",
    "Harwood Unified Union board page (official): 14 members "
    "with towns and term expirations -- Duxbury: Cindy Senning "
    "(Vice Chair, 2029), Emily Dolloff (2028); Fayston: Karl "
    "Naden (2027), Langford Davidson (2028); Moretown: Steve "
    "Rosenberg (Chair, 2027), Caitlin Lovegrove (2027); "
    "Waitsfield: John Weir (2029), Alexina Cather (2027); "
    "Warren: Ashley Woods (2028), Macon Phillips (2027); "
    "Waterbury: Pamela Eaton (2029), Robert Dabrowski (2028), "
    "Theo Hanna (2027), Jillan Sackett (2027). (The page prints "
    "'Jillan Sackett'; news uses 'J.B. Weir' for John Weir.) "
    "The district's minutes archive is JavaScript-rendered and "
    "was not fetchable: the 2025-26 appointment outcomes rest "
    "on the district's own vacancy notices + this roster, "
    "which places each person in exactly the seat and "
    "expiration the reported outcome produces.")
HW_SRC = [HW_ART, HW_PAGE]
HW_DEP = ("https://faystonvt.com/wp-content/uploads/2025/10/School-Board-.pdf")
emit(
    "harwood-unified-union", "Harwood Unified Union School District",
    [S(ST, "16 V.S.A. section 603(a)(6) inventory: the Harwood "
           "Unified Union School District is its own "
           "supervisory district (member towns Duxbury, "
           "Fayston, Moretown, Waitsfield, Warren, Waterbury)."),
     S("https://huusd.org",
       "Harwood Unified Union School District (official "
       "district website).")],
    "Harwood Unified Union School Board", HW_SRC,
    [{"key": "school-director-duxbury",
      "title": "School Director - Duxbury", "seats": 2},
     {"key": "school-director-fayston",
      "title": "School Director - Fayston", "seats": 2},
     {"key": "school-director-moretown",
      "title": "School Director - Moretown", "seats": 2},
     {"key": "school-director-waitsfield",
      "title": "School Director - Waitsfield", "seats": 2},
     {"key": "school-director-warren",
      "title": "School Director - Warren", "seats": 2},
     {"key": "school-director-waterbury",
      "title": "School Director - Waterbury", "seats": 4}],
    [H("Cindy Senning", "cindy-senning",
       post="school-director-duxbury",
       existing_person_id="ocd-person/ca285d4d-2502-5076-8076-8827f9ed1b80",
       sources=HW_SRC),
     H("Emily Dolloff", "emily-dolloff",
       post="school-director-duxbury", sources=HW_SRC),
     H("Karl Naden", "karl-naden",
       post="school-director-fayston", sources=HW_SRC),
     H("Langford Davidson", "langford-davidson",
       post="school-director-fayston", sources=HW_SRC),
     H("Steve Rosenberg", "steve-rosenberg",
       post="school-director-moretown", sources=HW_SRC),
     H("Caitlin Lovegrove", "caitlin-lovegrove",
       post="school-director-moretown", how_seated="appointed",
       sources=[S(HW_PAGE["url"],
                  "Caitlin Lovegrove was appointed March 18, "
                  "2026 to the Moretown seat left vacant when no "
                  "candidate filed for the March 3, 2026 "
                  "election (Ben Clark's term ended), to serve "
                  "until Town Meeting Day March 2027 -- the "
                  "district's March 2026 vacancy notice + the "
                  "official roster; the appointment minutes "
                  "themselves were not fetchable (the district's "
                  "archive is JavaScript-rendered).")]),
     H("John Weir", "john-weir",
       post="school-director-waitsfield", sources=HW_SRC),
     H("Alexina Cather", "alexina-cather",
       post="school-director-waitsfield", how_seated="appointed",
       sources=[S(HW_PAGE["url"],
                  "Alexina Cather was appointed in fall 2026 to "
                  "the Waitsfield seat Bobbi Rood resigned "
                  "effective August 27, 2026 (district vacancy "
                  "notice, Aug. 28, 2026), to serve until Town "
                  "Meeting Day March 2027 -- the district's "
                  "notice + the official roster; the appointment "
                  "minutes were not fetchable.")]),
     H("Ashley Woods", "ashley-woods",
       post="school-director-warren", sources=HW_SRC),
     H("Macon Phillips", "macon-phillips",
       post="school-director-warren", sources=HW_SRC),
     H("Pamela Eaton", "pamela-eaton",
       post="school-director-waterbury", sources=HW_SRC),
     H("Robert Dabrowski", "robert-dabrowski",
       post="school-director-waterbury", sources=HW_SRC),
     H("Theo Hanna", "theo-hanna",
       post="school-director-waterbury", sources=HW_SRC),
     H("Jillan Sackett", "jillan-sackett",
       post="school-director-waterbury", how_seated="appointed",
       sources=[S(HW_PAGE["url"],
                  "Jillan Sackett holds the Waterbury seat Corey "
                  "Hackett resigned in March 2026 (district "
                  "vacancy advertised March 20, 2026) as an "
                  "appointee until Town Meeting Day March 2027 "
                  "-- the district's notice + the official "
                  "roster; the appointment minutes were not "
                  "fetchable. (Spelling as the district page "
                  "prints it.)")]),
     H("Mike Bishop", "mike-bishop",
       post="school-director-fayston", end="2025",
       sources=[S(HW_DEP,
                  "Mike Bishop (Fayston) resigned in fall 2025; "
                  "the district's Fayston vacancy notice (Oct. "
                  "2025, republished by the Town of Fayston) "
                  "advertised his seat. Ended 2025.")]),
     H("Rebecca Baruzzi", "rebecca-baruzzi",
       post="school-director-fayston", end="2025",
       sources=[S(HW_DEP,
                  "Rebecca Baruzzi (Fayston; elected March 2025 "
                  "to a term ending 2028) resigned in December "
                  "2025; the district's second Fayston vacancy "
                  "notice (Dec. 2025) advertised the seat, which "
                  "stayed open until the March 2026 election. "
                  "Ended 2025.")]),
     H("Jonathan Young", "jonathan-young",
       post="school-director-warren", end="2026",
       sources=[S("https://huusd.org/board",
                  "Jonathan Young (Warren) resigned in January "
                  "2026; the district's Warren vacancy notice "
                  "advertised his seat. Macon Phillips was "
                  "appointed Feb. 11, 2026 and then elected "
                  "March 3, 2026 to the remaining year. Ended "
                  "2026.")]),
     H("Ben Clark", "ben-clark",
       post="school-director-moretown", end="2026",
       sources=[S("https://huusd.org/board",
                  "Ben Clark's Moretown term ended at the March "
                  "3, 2026 election and he did not seek "
                  "re-election; no candidate filed, and the "
                  "seat was filled by appointment (Lovegrove). "
                  "Ended 2026.")]),
     H("Dan Roscioli", "dan-roscioli",
       post="school-director-waterbury", end="2026",
       how_seated="appointed",
       sources=[S("https://huusd.org/board",
                  "Dan Roscioli was appointed in 2025 to a "
                  "1-year unexpired Waterbury term and did not "
                  "run in March 2026; his seat passed to Theo "
                  "Hanna at that election. Ended 2026.")]),
     H("Corey Hackett", "corey-hackett",
       post="school-director-waterbury", end="2026",
       sources=[S("https://huusd.org/board",
                  "Corey Hackett (Waterbury; elected March 2025 "
                  "to the remaining two years of a term ending "
                  "2027) resigned in March 2026; the district "
                  "advertised the vacancy March 20, 2026 and "
                  "Jillan Sackett now holds the seat as an "
                  "appointee. Ended 2026.")]),
     H("Bobbi Rood", "bobbi-rood",
       post="school-director-waitsfield", end="2026",
       sources=[S("https://huusd.org/board",
                  "Bobbi Rood (Waitsfield) resigned effective "
                  "August 27, 2026 (district vacancy notice, "
                  "Aug. 28, 2026); Alexina Cather was appointed "
                  "to the seat. Ended 2026.")])],
)

# ---- 39. Hazen Union --------------------------------------------------------------------------
HZ_SHEET = S(
    "https://docs.google.com/spreadsheets/d/1vCuymb9bQ5aa7QSDGPhrWV8sEmGgbfTLpzznPeE_1bo",
    "Hazen Union School District board roster sheet (Orleans "
    "Southwest SU, official): eight directors -- Hardwick: "
    "Margaret Bledsoe (Vice Chair, term end 2029), Terri Vest "
    "(2029), Patrick Kane (2028), Sabrina Morrison (Clerk, "
    "2027); Greensboro: Jan Terwiesch (2028), Christian "
    "Holland (1-year term, 2027); Woodbury: Steven Freihofner "
    "(Chair, 2029), Laura Murphy (2028). The same eight are "
    "listed in the August 18, 2026 board agenda. Seats are "
    "town-allocated with TOWN-ONLY electorates (Union High "
    "School District No. 26, 16 V.S.A. section 748; "
    "Hardwick's official 2026 open-offices notice puts two "
    "Hazen 3-year seats on Hardwick's own Australian ballot). "
    "HELD: Christian Holland -- he holds a published 1-year "
    "term ending 2027, but whether he was elected to an "
    "unexpired remainder or appointed is not certified by any "
    "fetched document (missing: Greensboro's March 2026 Hazen "
    "ballot/warning and the board's appointment minutes). The "
    "district's articles of agreement were not fetched; the "
    "allocation rests on the roster sheet + town notices.")
emit(
    "hazen-union", "Hazen Union School District",
    [S(ST, "16 V.S.A. section 603(a) inventory: Hazen Union "
           "School District (Union High School District No. "
           "26), a union high school district in the Orleans "
           "Southwest Supervisory Union (member towns "
           "Greensboro, Hardwick, Woodbury)."),
     S("https://www.ossu.org",
       "Orleans Southwest Supervisory Union (official site).")],
    "Hazen Union School Board", [HZ_SHEET],
    [{"key": "school-director-hardwick",
      "title": "School Director - Hardwick", "seats": 4},
     {"key": "school-director-greensboro",
      "title": "School Director - Greensboro", "seats": 2},
     {"key": "school-director-woodbury",
      "title": "School Director - Woodbury", "seats": 2}],
    [H("Margaret Bledsoe", "margaret-bledsoe",
       post="school-director-hardwick", sources=[HZ_SHEET]),
     H("Terri Vest", "terri-vest",
       post="school-director-hardwick", sources=[HZ_SHEET]),
     H("Patrick Kane", "patrick-kane",
       post="school-director-hardwick", sources=[HZ_SHEET]),
     H("Sabrina Morrison", "sabrina-morrison",
       post="school-director-hardwick", sources=[HZ_SHEET]),
     H("Jan Terwiesch", "jan-terwiesch",
       post="school-director-greensboro",
       existing_person_id="ocd-person/3d22bf82-b5fd-5b24-b4b6-9accd1e0cbc2",
       sources=[HZ_SHEET]),
     H("Steven Freihofner", "steven-freihofner",
       post="school-director-woodbury", sources=[HZ_SHEET]),
     H("Laura Murphy", "laura-murphy",
       post="school-director-woodbury", sources=[HZ_SHEET])],
)

# ---- 40. Holland ---------------------------------------------------------------------------------
HO_PAGE = S(
    "https://www.ncsuvt.org/47191_2",
    "Holland School Board page (North Country SU, official), "
    "2026-2027 listing: Gina Miller (Chair), John Castle (Vice "
    "Chair), Heather Dowland (Clerk). The board is the section "
    "423(a) default three directors at-large on staggered "
    "3-year terms, elected from the floor of the annual "
    "meeting. Expirations are from the Town of Holland 2025 "
    "Annual Report officials list (Castle 2027, Dowland 2028) "
    "and Miller's March 3, 2026 re-election to the warned "
    "3-year seat (to 2029; the meeting minutes themselves are "
    "not yet published). NOTE: the district has been "
    "non-operating since July 1, 2025 (its school building was "
    "conveyed to the Town; it tuitions all grades) -- the "
    "district and board persist. (The same report shows "
    "Holland electing a Union School Director for the North "
    "Country union districts, correcting universe.md's frame; "
    "that seat belongs to the union districts' builds.)")
emit(
    "holland", "Holland School District",
    [S(ST, "16 V.S.A. section 603(a) inventory: Holland School "
           "District, a town school district in the North "
           "Country Supervisory Union (member town: Holland)."),
     S("https://www.ncsuvt.org",
       "North Country Supervisory Union (official site).")],
    "Holland School Board", [HO_PAGE],
    [{"key": "school-director", "title": "School Director",
      "seats": 3}],
    [H("Gina Miller", "gina-miller", sources=[HO_PAGE]),
     H("John Castle", "john-castle", sources=[HO_PAGE]),
     H("Heather Dowland", "heather-dowland",
       existing_person_id="ocd-person/cc1928f2-cd4a-5335-ab59-a09fd88894a5",
       sources=[HO_PAGE])],
)
print("part 2 done")
