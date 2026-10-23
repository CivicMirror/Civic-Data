#!/usr/bin/env python3
"""VT #163 school pass -- batch 3 specs (districts 21-30).
Research: ~/workspace/vt163_school_work/batch3_research_{a,b}.md;
adjudications by Boone 2026-10-22."""
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

# ---- 21. Craftsbury ------------------------------------------------------
CRA_SHEET = S(
    "https://docs.google.com/spreadsheets/d/1up_rRZ1yYimOPg3GmNH-fUQIlLBCHDy8edS35DtaTq0/edit?usp=sharing",
    "Craftsbury School Board roster sheet (district's own, "
    "linked from the Orleans Southwest SU board page): five "
    "directors -- Kasey Allen (Chair, 2-year seat, term end "
    "2027), Cedar Hannan (Vice Chair, 3-year, 2029), Isaac "
    "Jacobs (3-year, 2027), Michelle Menard (Clerk, 2-year, "
    "2028), Anna Schulz (3-year, 2028) -- the section 423(a)-(b) "
    "shape (three 3-year seats, two 2-year seats), elected "
    "at-large. The same five are present in the September 9 and "
    "October 14, 2026 board minutes, and the superintendent's "
    "April 2026 newsletter states 'everyone returned' at the "
    "March 3, 2026 election. (The town report's officers table "
    "once prints 'Cedrus Hannan' -- a typo; district sources "
    "uniformly read Cedar Hannan.)")
emit(
    "craftsbury", "Craftsbury School District",
    [S(ST, "16 V.S.A. section 603(a)(7)(I) inventory: "
           "Craftsbury School District, a town school district "
           "in the Orleans Southwest Supervisory Union (member "
           "town: Craftsbury)."),
     S("https://craftsbury.ossu.org",
       "Craftsbury Town School District (official district "
       "website).")],
    "Craftsbury School Board", [CRA_SHEET],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H(n, s, sources=[CRA_SHEET]) for n, s in [
        ("Kasey Allen", "kasey-allen"), ("Cedar Hannan", "cedar-hannan"),
        ("Isaac Jacobs", "isaac-jacobs"),
        ("Michelle Menard", "michelle-menard"),
        ("Anna Schulz", "anna-schulz")]],
)

# ---- 22. Danville ----------------------------------------------------------
DAN_PAGE = S(
    "https://danville.ccsuvt.net/185261_3",
    "Danville School District board members page (official): "
    "five directors -- Clayton Cargill (Chair, term expires "
    "2027), David Towle (Vice-Chair, 2027), Tim Sanborn (2027), "
    "Eric Hewitt (2028), Kay Freedy (2029). The March 3, 2026 "
    "annual meeting minutes elect Freedy (3-year seat) and "
    "Sanborn and Cargill (the two section 423(b) one-year "
    "seats) by voice vote; Towle and Hewitt are continuous "
    "incumbents on the section 423 stagger whose current-term "
    "election minutes (March 2024 / March 2025) were not "
    "fetched -- no appointment document exists for either in "
    "any fetched record. The board is five directors at-large "
    "(16 V.S.A. section 423(a)-(b)).")
emit(
    "danville", "Danville School District",
    [S(ST, "16 V.S.A. section 603(a)(6)(A) inventory: Danville "
           "School District, a town school district in the "
           "Caledonia Central Supervisory Union (member town: "
           "Danville)."),
     S("https://danville.ccsuvt.net",
       "Danville School (official district website).")],
    "Danville School Board", [DAN_PAGE],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H(n, s, sources=[DAN_PAGE]) for n, s in [
        ("Clayton Cargill", "clayton-cargill"),
        ("David Towle", "david-towle"), ("Tim Sanborn", "tim-sanborn"),
        ("Eric Hewitt", "eric-hewitt"), ("Kay Freedy", "kay-freedy")]],
)

# ---- 23. Derby ---------------------------------------------------------------
DER_PAGE = S(
    "https://www.ncsuvt.org/47190_2",
    "Derby School Board page (North Country SU, official), "
    "2026-2027 block: Michael Kiser (Chair), Robert Boskind "
    "(Vice Chair; the page misspells 'Boskin' -- district "
    "minutes uniformly read Boskind), Amber Roberge (Clerk), "
    "Jennifer Davis. The same four are the board in six "
    "post-election minutes sets (April-October 2026). The "
    "board is five directors at-large (16 V.S.A. section "
    "423(a)-(b)); the fifth seat has been VACANT since the "
    "March 3, 2026 annual meeting (see Brainard's ended "
    "membership) -- the August 18, 2026 minutes record the "
    "board still advertising the vacancy, and no appointment "
    "appears through October 6, 2026. No per-member term "
    "expirations are published anywhere reachable (the "
    "district's 2026 annual-meeting warning is not posted).")
emit(
    "derby", "Derby School District",
    [S(ST, "16 V.S.A. section 603(a) inventory: Derby School "
           "District, a town school district in the North "
           "Country Supervisory Union (member town: Derby)."),
     S("https://www.ncsuvt.org",
       "North Country Supervisory Union (official site hosting "
       "the district's board page).")],
    "Derby School Board", [DER_PAGE],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H("Michael Kiser", "michael-kiser", sources=[DER_PAGE]),
     H("Robert Boskind", "robert-boskind", sources=[DER_PAGE]),
     H("Amber Roberge", "amber-roberge", sources=[DER_PAGE]),
     H("Jennifer Davis", "jennifer-davis", sources=[DER_PAGE]),
     H("Nikole Brainard", "nikole-brainard", end="2026",
       sources=[S("https://drive.google.com/file/d/1IHJNc9VQyE_xXV5vbb38HF7E7dsMJlyh/view",
                  "Derby board minutes, January 6, 2026 ('Board "
                  "Terms'): Nikole Brainard (Chair) was up for "
                  "re-election at the March 2026 annual meeting "
                  "and 'will not be running again'. She chaired "
                  "the February 3, 2026 meeting and appears in "
                  "no minutes thereafter; her seat has been "
                  "vacant since the March 3, 2026 election. Her "
                  "membership is ended in 2026.")])],
)

# ---- 24. Dresden Interstate ---------------------------------------------------
DRE_ART = S(
    "http://norwich.vt.us/wp-content/uploads/2020/06/SB-packet-06-10-20.pdf",
    "Dresden Articles of Agreement (December 17, 2002, as "
    "reproduced in the Town of Norwich Selectboard packet of "
    "June 10, 2020), Article C: the Dresden board 'shall "
    "consist of eleven (11) members, seven (7) of whom shall be "
    "residents of Hanover and elected by the Hanover School "
    "District, and four (4) of whom shall be residents of "
    "Norwich and elected by the Norwich Town School District' "
    "-- directors are deemed elected to Dresden by their "
    "election to the member-district boards; the person elected "
    "to Norwich's two-year seat in even-numbered years sits on "
    "the Dresden board with 'all the rights of a member... "
    "except the right to vote'. The compact permits at-large "
    "seats (16 V.S.A. sections 774, 775) but Article C provides "
    "none. The seven Hanover (New Hampshire) seats are OUT OF "
    "SCOPE for this dataset (Walter's ruling, 2026-10-22) and "
    "no post is modeled for them; the Norwich seats are modeled "
    "here, and no separate Norwich School District board post "
    "is built.")
DRE_TALLY = S(
    "https://norwich.vt.us/wp-content/uploads/2026/08/20260303-results-on-ballot-scan.pdf",
    "Town of Norwich official ballot tallies: March 3, 2026 -- "
    "'For DRESDEN-NORWICH SCHOOL DIRECTOR, three years': Lisa "
    "Christie 798 and Michael K. Costa 754 elected (terms to "
    "2029); 'For NORWICH SCHOOL DIRECTOR, two years': Garrett "
    "Palm 796 re-elected (to 2028). March 4, 2025: Gina C. des "
    "Cognets elected (806, to 2028). March 5, 2024: Neil Odell "
    "elected (1,027, to 2027). The five are the Norwich side of "
    "the Dresden board per SAU 70's Annual Report 2025-26 "
    "officers list.")
emit(
    "dresden", "Dresden Interstate School District",
    [S("https://legislature.vermont.gov/statutes/fullchapter/16/015",
       "16 V.S.A. section 782 authorizes the Dresden School "
       "District (the Hanover-Norwich Interstate School "
       "District) under the New Hampshire-Vermont Interstate "
       "School Compact. 16 V.S.A. section 603(a) lists SAU 70 "
       "(the district's New Hampshire administrative unit) in "
       "the Northeast CESA rather than Dresden itself."),
     S("https://www.sau70.org",
       "SAU 70 (official site administering the Dresden "
       "district).")],
    "Dresden School Board", [DRE_ART, DRE_TALLY],
    [{"key": "school-director-norwich",
      "title": "School Director - Norwich", "seats": 4},
     {"key": "school-director-norwich-nonvoting",
      "title": "School Director - Norwich (Nonvoting)",
      "seats": 1}],
    [H("Lisa Christie", "lisa-christie",
       post="school-director-norwich", sources=[DRE_TALLY]),
     H("Michael K. Costa", "michael-k-costa",
       post="school-director-norwich", sources=[DRE_TALLY]),
     H("Neil Odell", "neil-odell",
       post="school-director-norwich", sources=[DRE_TALLY]),
     H("Gina C. des Cognets", "gina-c-des-cognets",
       post="school-director-norwich", sources=[DRE_TALLY]),
     H("Garrett Palm", "garrett-palm",
       post="school-director-norwich-nonvoting",
       sources=[DRE_ART, DRE_TALLY])],
)

# ---- 25. Echo Valley -----------------------------------------------------------
EV_ART = S(
    "https://drive.google.com/file/d/1_Ss90cWw0Yh4AndZ83vjvj0KBKVpJSqB/view",
    "Echo Valley (Orange Washington) articles of agreement, "
    "Article 8: the board 'shall be composed of six (6) "
    "individuals elected by Australian ballot by the voters of "
    "the municipalities in which they reside... three (3) "
    "representatives residing in and representing the town of "
    "Orange; three (3) representatives residing in and "
    "representing the Town of Washington' -- proportional-to-"
    "town (16 V.S.A. section 730(a)(1)); Article 9 sets "
    "three-year terms.")
EV_PAGE = S(
    "https://www.cvsu.org/school-boards/echo-valley-community-school-district-board",
    "Echo Valley Community School District board page "
    "(Central Vermont SU, official; updated July 24, 2026): six "
    "directors -- Washington: Dominique LaFond Copeland "
    "(Chair, term to 2027), Nick Marineau (Clerk, to 2028), "
    "Josh Bell (to 2029); Orange: Matthew Flinn (to 2027), "
    "Dane Deberville (to 2028), Don Mountford (Vice Chair, to "
    "2029). All six are accounted for in the September 9 and "
    "September 30, 2026 minutes.")
emit(
    "echo-valley", "Echo Valley Community School District",
    [S(ST, "16 V.S.A. section 603(a)(7)(C) inventory: Echo "
           "Valley Community School District, a unified union "
           "district in the Central Vermont Supervisory Union "
           "(member towns Orange and Washington)."),
     S("https://www.cvsu.org",
       "Central Vermont Supervisory Union (official site).")],
    "Echo Valley Community School Board", [EV_ART, EV_PAGE],
    [{"key": "school-director-orange",
      "title": "School Director - Orange", "seats": 3},
     {"key": "school-director-washington",
      "title": "School Director - Washington", "seats": 3}],
    [H("Matthew Flinn", "matthew-flinn",
       post="school-director-orange", sources=[EV_PAGE]),
     H("Don Mountford", "don-mountford",
       post="school-director-orange", sources=[EV_PAGE]),
     H("Dominique LaFond Copeland", "dominique-lafond-copeland",
       post="school-director-washington", sources=[EV_PAGE]),
     H("Josh Bell", "josh-bell",
       post="school-director-washington",
       existing_person_id="ocd-person/65ab7042-a270-5b56-a4ca-6302abf8f5f0",
       sources=[EV_PAGE]),
     H("Nick Marineau", "nick-marineau",
       post="school-director-washington",
       sources=[S("https://docs.google.com/document/d/1lilfhrQEV-IgHtUJaDy_zJMZAXRLG0nXGZJzv8Vl4j4/edit?usp=drive_web",
                  "Nick Marineau was APPOINTED February 5, 2026 "
                  "to fill the Washington vacancy (Brittany "
                  "Driscoll's resignation) expressly on an "
                  "interim basis 'through Town Meeting Day' "
                  "(Feb. 5, 2026 special-meeting minutes; Feb. "
                  "11, 2026 superintendent's report). The "
                  "district's board page then assigns him the "
                  "term March 2026-2028 -- exactly the two-year "
                  "remainder the January 19, 2026 minutes "
                  "identified as opening at the March 2026 "
                  "election for that seat. He is recorded "
                  "ELECTED to the remainder on that chain; the "
                  "Washington March 3, 2026 ballot results "
                  "naming him were not fetched (named gap).")])],
)
# HELD: Dane Deberville (Orange) -- first appears at the March
# 11, 2026 reorganization after Mike Concessi's undocumented
# departure; no appointment minute and no election record.
print("part 1 done")

# ---- 26. Elmore-Morristown ------------------------------------------------------
EM_PAGE = S(
    "https://www.lamoillesouth.org/lamoille-south-board",
    "Elmore-Morristown UUSD board page (Lamoille South SU, "
    "official): five directors -- David Bickford (Chair, "
    "Morristown resident, term expires 2028), Ann Marie Dryden "
    "(Elmore, 2028), David McAllister (Clerk, Morristown, "
    "2027), Richard Shanley (Morristown, 2029), Peggy Sprague "
    "(Elmore-or-Morristown seat, 2027). The board sits at five "
    "since the voters' 2023 expansion from four (the seat "
    "Sprague won March 5, 2024). All seats are elected "
    "DISTRICT-WIDE (modified at-large, 16 V.S.A. section "
    "730(a)(2)) -- proven arithmetically by the certified "
    "March 4, 2025 results: Dryden drew 1,336 votes for the "
    "Elmore-resident seat on only 257 Elmore ballots. Shanley's "
    "2026 re-election rests on the 2026 warning + the board "
    "page's 2029 expiry + his 2026 minutes service; no "
    "certified 2026 results sheet is posted. NOTE: the articles "
    "AOE hosts for 'Lamoille South' are the SUPERSEDED default "
    "articles of the dissolved LSUU (6 seats incl. Stowe) -- do "
    "not use them.")
emit(
    "elmore-morristown-unified-union",
    "Elmore-Morristown Unified Union School District",
    [S(ST, "16 V.S.A. section 603(a) inventory: Elmore-"
           "Morristown Unified Union School District, a unified "
           "union district in the Lamoille South Supervisory "
           "Union (member towns Elmore and Morristown)."),
     S("https://www.lamoillesouth.org",
       "Lamoille South Supervisory Union (official site).")],
    "Elmore-Morristown Unified Union School Board", [EM_PAGE],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H(n, s, sources=[EM_PAGE]) for n, s in [
        ("David Bickford", "david-bickford"),
        ("Ann Marie Dryden", "ann-marie-dryden"),
        ("David McAllister", "david-mcallister"),
        ("Richard Shanley", "richard-shanley"),
        ("Peggy Sprague", "peggy-sprague")]],
)

# ---- 27. Enosburgh-Richford -------------------------------------------------------
ER_PAGE = S(
    "https://www.fnesu.org/page/board-members",
    "Enosburgh-Richford UUSD board members page (Franklin "
    "Northeast SU, official): six directors -- Sara Hurtubise "
    "(Chair, Richford, term ends 2027), Rachael Tatro (Clerk, "
    "Enosburgh, 2027), Joshua Muir (Enosburgh, 2028), Devin "
    "Lumbra (Richford, 2028), Akua Smith (Vice Chair, "
    "Enosburgh, 2029), Gabrielle Elwood (Richford, 2029). All "
    "six are named across the September 8 and October 13, 2026 "
    "minutes. Seats are residency-allocated (Enosburgh 3 / "
    "Richford 3) but elected by the whole district (modified "
    "at-large; State Board default articles Art. 10(A) "
    "'Hybrid Model', expanded 4 to 6 seats in 2019 -- the 2019 "
    "amendment tally itself was not located in an official "
    "document). Lumbra's current membership is ELECTED: he was "
    "appointed March 11, 2025 to a vacant Richford seat and "
    "then elected March 3, 2026 to its remaining two years.")
emit(
    "enosburgh-richford-unified-union",
    "Enosburgh-Richford Unified Union School District",
    [S(ST, "16 V.S.A. section 603(a)(1)(A) inventory: "
           "Enosburgh-Richford Unified Union School District, "
           "a unified union district in the Franklin Northeast "
           "Supervisory Union (member towns Enosburgh and "
           "Richford)."),
     S("https://www.fnesu.org",
       "Franklin Northeast Supervisory Union (official site).")],
    "Enosburgh-Richford Unified Union School Board", [ER_PAGE],
    [{"key": "school-director", "title": "School Director",
      "seats": 6}],
    [H(n, s, sources=[ER_PAGE]) for n, s in [
        ("Sara Hurtubise", "sara-hurtubise"),
        ("Rachael Tatro", "rachael-tatro"),
        ("Joshua Muir", "joshua-muir"),
        ("Devin Lumbra", "devin-lumbra"),
        ("Akua Smith", "akua-smith"),
        ("Gabrielle Elwood", "gabrielle-elwood")]] +
    [H("Mort Greenwood", "mort-greenwood", end="2026",
       sources=[S("https://files-backend.assets.thrillshare.com/documents/asset/uploaded_file/4341/Fnesu/9d8562e8-8f14-4039-bc4c-2ab2e796529d/11%29-2_17_2026-ER-UUSD-Board-Meeting-Minutes.pdf?disposition=inline",
                  "Mort Greenwood chaired the Enosburgh-Richford "
                  "board through the February 17, 2026 meeting "
                  "and signed the March 2026 warning as Chair; "
                  "he is absent from the March 10, 2026 "
                  "reorganization minutes and the current "
                  "roster (his Richford seat passed to Gabrielle "
                  "Elwood at the March 3, 2026 election). "
                  "Whether he stood for re-election is not "
                  "stated in any fetched source. His membership "
                  "is ended in 2026. (Some minutes spell his "
                  "first name 'Morton'; the signed warnings read "
                  "Mort.)")])],
)

# ---- 28. Essex Westford -------------------------------------------------------------
EW_PAGE = S(
    "https://www.ewsd.org/page/schoolboard",
    "Essex Westford School District 'Meet the School Board' "
    "page (official): 'EWSD has 10 elected School Board "
    "members representing Essex Town, Essex Junction, and "
    "Westford... School Directors are elected by voters in the "
    "communities they represent. Board seats have three-year "
    "terms.' The allocation (Essex Town 4, Essex Junction 4, "
    "Westford 2) is from the Articles of Agreement (Art. 9) "
    "approved November 3, 2015 and is confirmed in every "
    "annual-meeting warning 2022-2026; no consolidated current "
    "articles document was located (the 2015 study-committee "
    "text controls, corroborated in current operation). "
    "Westford's two directors carry a 0.5 weighted board vote "
    "each under Art. 9; its current application is "
    "undocumented post-2022.")
EW_RES = S(
    "https://www.ewsd.org/article/2822090",
    "Essex Westford official results article, April 15, 2026: "
    "Scott Brown and Dawn Irwin (Essex Junction), Jemima "
    "Talbot (Essex Town) and Marilyn McConnell (Westford) "
    "elected April 14, 2026 -- matching the board page's "
    "term-end 2029 group. The April 9, 2025 results article "
    "likewise matches the 2028 group (Carpenter, Taylor, "
    "Verasamy). The same April 2026 vote moved the annual "
    "meeting to March from 2027; the board page's April "
    "term-end labels are minted as published.")
EW_SRC = [EW_PAGE, EW_RES]
emit(
    "essex-westford", "Essex Westford School District",
    [S(ST, "16 V.S.A. section 603(a)(2)(C) inventory: the "
           "Essex Westford Educational Community Unified Union "
           "Supervisory District's district is the Essex "
           "Westford School District (member communities: Town "
           "of Essex, City of Essex Junction, Westford)."),
     S("https://www.ewsd.org",
       "Essex Westford School District (official district "
       "website).")],
    "Essex Westford School Board", EW_SRC,
    [{"key": "school-director-essex-town",
      "title": "School Director - Essex Town", "seats": 4},
     {"key": "school-director-essex-junction",
      "title": "School Director - Essex Junction", "seats": 4},
     {"key": "school-director-westford",
      "title": "School Director - Westford", "seats": 2}],
    [H("Robert Carpenter", "robert-carpenter",
       post="school-director-essex-town", sources=EW_SRC),
     H("Laura Taylor", "laura-taylor",
       post="school-director-essex-town",
       existing_person_id="ocd-person/6cee6aab-2306-5c29-a5ce-06a0dff63b68",
       sources=EW_SRC),
     H("Gretchen Bates", "gretchen-bates",
       post="school-director-essex-town", sources=EW_SRC),
     H("Jemima Talbot", "jemima-talbot",
       post="school-director-essex-town", sources=EW_SRC),
     H("Marlon Verasamy", "marlon-verasamy",
       post="school-director-essex-junction", sources=EW_SRC),
     H("Christine Gaynor-Patterson", "christine-gaynor-patterson",
       post="school-director-essex-junction", sources=EW_SRC),
     H("Scott Brown", "scott-brown",
       post="school-director-essex-junction", sources=EW_SRC),
     H("Dawn Irwin", "dawn-irwin",
       post="school-director-essex-junction", sources=EW_SRC),
     H("Anne Marie Sharp", "anne-marie-sharp",
       post="school-director-westford", sources=EW_SRC),
     H("Marilyn McConnell", "marilyn-mcconnell",
       post="school-director-westford", sources=EW_SRC),
     H("Erin Kennedy Knox", "erin-kennedy-knox",
       post="school-director-essex-junction", end="2026",
       sources=[S("https://www.ewsd.org/page/schoolboard",
                  "Erin Kennedy Knox (Essex Junction) sat on "
                  "the board through the November 18, 2025 "
                  "minutes on a term expiring April 2026; she "
                  "is not among the April 14, 2026 winners and "
                  "not on the current board page (her seat "
                  "passed to Dawn Irwin). Whether she lost or "
                  "did not seek re-election is not stated. Her "
                  "membership is ended in 2026.")]),
     H("Andre Roy", "andre-roy",
       post="school-director-westford", end="2026",
       sources=[S("https://www.ewsd.org/page/schoolboard",
                  "Andre Roy (Westford) sat on the board "
                  "through the December 15, 2025 committee "
                  "minutes on a term expiring April 2026; he is "
                  "not among the April 14, 2026 winners and not "
                  "on the current board page (his seat passed "
                  "to Marilyn McConnell). Whether he lost or "
                  "did not seek re-election is not stated. His "
                  "membership is ended in 2026.")])],
)

# ---- 29. Fairfax ----------------------------------------------------------------------
FX_PAGE = S(
    "https://www.bfafairfax.com/o/bfa/page/fairfax-school-board",
    "Fairfax School Board page (official): five directors -- "
    "Emily Aiken (Chair), MacKenzie Geary (Clerk), Katie "
    "Haddock, Ed Nasta, Danielle Rothy. The board is five "
    "directors at-large (16 V.S.A. section 423(a)-(b): three "
    "3-year seats, two 2-year seats). Aiken was re-elected "
    "March 3, 2026 to the 2-year seat (sole printed candidate; "
    "the board's March 9, 2026 summary confirms); Geary holds "
    "a 3-year term to 2028 (March 10, 2025 reorganization "
    "summary); Haddock's term runs to 2027 (Town Report 2025 "
    "officers list).")
FX_APPT = S(
    "https://www.bfafairfax.com/o/bfa/page/fxboard-summary",
    "Fairfax board meeting summaries (official): the March 9, "
    "2026 summary records two open seats after the March 3, "
    "2026 election (the 3-year race and the 1-year-remainder "
    "race were write-in only and seated no winner) and that "
    "'Two new members will be appointed at the April meeting.' "
    "Ed Nasta and Danielle Rothy are the two members added to "
    "the board page after that date and are recorded "
    "APPOINTED. The April 2026 meeting minutes naming them and "
    "assigning the seats (one holds the 3-year seat to 2029, "
    "the other the 1-year remainder to 2027) were not posted "
    "-- the assignment is UNRESOLVED and no term is asserted "
    "for either.")
emit(
    "fairfax", "Fairfax School District",
    [S(ST, "16 V.S.A. section 603(a)(1)(B) inventory: Fairfax "
           "School District, a town school district in the "
           "Franklin West Supervisory Union (member town: "
           "Fairfax). The district operates Bellows Free "
           "Academy Fairfax; the separately-elected BFA "
           "Trustees are a distinct incorporated-school body "
           "and are NOT modeled here."),
     S("https://www.bfafairfax.com",
       "Bellows Free Academy Fairfax (official school site).")],
    "Fairfax School Board", [FX_PAGE],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H("Emily Aiken", "emily-aiken", sources=[FX_PAGE]),
     H("MacKenzie Geary", "mackenzie-geary", sources=[FX_PAGE]),
     H("Katie Haddock", "katie-haddock", sources=[FX_PAGE]),
     H("Ed Nasta", "ed-nasta", how_seated="appointed",
       sources=[FX_APPT]),
     H("Danielle Rothy", "danielle-rothy", how_seated="appointed",
       sources=[FX_APPT]),
     H("Matthew Hogan", "matthew-hogan", end="2026",
       sources=[S("https://www.bfafairfax.com/o/bfa/page/fxboard-summary",
                  "The Fairfax board's March 9, 2026 summary "
                  "records: 'Matthew Hogan has stepped down "
                  "from the board after six years of dedicated "
                  "service.' His term expired in 2026 (Town "
                  "Report 2025) and his 3-year seat was left "
                  "open by the March 3, 2026 election. Ended "
                  "2026.")]),
     H("Scott Mitchell", "scott-mitchell", end="2026",
       how_seated="appointed",
       sources=[S("https://www.bfafairfax.com/o/bfa/page/fxboard-summary",
                  "Fairfax board summary, December 8, 2025: the "
                  "board 'voted unanimously (3-0) to appoint "
                  "Scott Mitchell to serve the remainder of the "
                  "term through Town Meeting Day on March 3, "
                  "2026' (the Frechette vacancy). He signed the "
                  "February 2, 2026 warning as a director and "
                  "does not appear on the post-election board. "
                  "Ended 2026.")]),
     H("Jolie Frechette", "jolie-frechette", end="2025",
       sources=[S("https://www.bfafairfax.com/o/bfa/page/fxboard-summary",
                  "Fairfax board summaries, October 14 and "
                  "November 11, 2025: Jolie Frechette (elected "
                  "March 2025 to a 2-year term) resigned in fall "
                  "2025 on relocating to another town; the "
                  "vacancy was filled by appointment until the "
                  "March election. Ended 2025.")])],
)

# ---- 30. First Branch --------------------------------------------------------------------
FB_PAGE = S(
    "https://wrvsu.org/first-branch-unified-district-1b3a464d",
    "First Branch Unified School District board page (White "
    "River Valley SU, official): six directors -- Kathy "
    "Galluzzo (Chair, Tunbridge, term expires 2027), Susan Kay "
    "(Vice Chair, Chelsea, 2027), Stacy Dion (Tunbridge, "
    "2028), Rebecca Savidge (Chelsea, 2028 per the page), "
    "Jacqueline Garran (Tunbridge, 2029), Alan Ackerman "
    "(Chelsea, 2029). The six are corroborated across the "
    "August 25, September 8 and October 6, 2026 minutes. "
    "Seats are residency-allocated (Chelsea 3 / Tunbridge 3) "
    "but elected by the whole district at the annual meeting "
    "(modified at-large; AOE State Board Item Q-2, 2017, "
    "quotes the articles: members 'elected by the voters of "
    "the entire New Unified District'). The verbatim articles "
    "text itself was not located.")
emit(
    "first-branch-unified", "First Branch Unified School District",
    [S(ST, "16 V.S.A. section 603(a) inventory: First Branch "
           "Unified School District, a unified union district "
           "in the White River Valley Supervisory Union "
           "(member towns Chelsea and Tunbridge)."),
     S("https://firstbranchschool.org",
       "First Branch Unified School District (official "
       "district website).")],
    "First Branch Unified School Board", [FB_PAGE],
    [{"key": "school-director", "title": "School Director",
      "seats": 6}],
    [H("Kathy Galluzzo", "kathy-galluzzo", sources=[FB_PAGE]),
     H("Susan Kay", "susan-kay", sources=[FB_PAGE]),
     H("Stacy Dion", "stacy-dion", sources=[FB_PAGE]),
     H("Jacqueline Garran", "jacqueline-garran", sources=[FB_PAGE]),
     H("Alan Ackerman", "alan-ackerman", sources=[FB_PAGE]),
     H("Rebecca Savidge", "rebecca-savidge", how_seated="appointed",
       sources=[S("https://docs.google.com/document/d/1vx748oOsWuWvj8W4mspfjbyBlHBCgF5ZjF7lH5qKfas",
                  "First Branch board minutes, June 16, 2026: "
                  "'Kathy Galluzzo made a motion to appoint "
                  "Rebecca Savage [sic -- the board page and "
                  "later minutes read Savidge] for the open "
                  "Chelsea Board position until March 2027... "
                  "Motion passed.' She fills William Smith "
                  "Jr.'s resigned Chelsea seat; the board page "
                  "labels that seat 'expires 2028' but her "
                  "appointment runs only to March 2027.")]),
     H("William Smith Jr.", "william-smith-jr", end="2026",
       sources=[S("https://docs.google.com/document/d/1CbGT7VQ0fvBaIgI8jdfB8HGCkdVu0aF7CCAfAEN-Lnw",
                  "First Branch board minutes, May 26, 2026: "
                  "'Bill Smith has resigned from the Board "
                  "effective June 17th'. He had been elected to "
                  "a Chelsea 3-year term March 3, 2025 and "
                  "served as Clerk through the March 10, 2026 "
                  "reorganization. Ended 2026.")])],
)
print("part 2 done")
