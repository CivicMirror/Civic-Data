#!/usr/bin/env python3
"""VT #163 school pass -- batch 2 specs (districts 11-20).
Research: ~/workspace/vt163_school_work/batch2_research_{a,b}.md;
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

# ---- 11. Burlington ----------------------------------------------------
BUR_PAGE = S(
    "https://www.bsdvt.org/school-board/members/",
    "Burlington School District board members page (official): "
    "the twelve current school commissioners with their wards/"
    "districts and term-end years -- the eight ward seats end "
    "2028, the four city-district seats end 2027.")
BUR_CHARTER = S(
    "https://legislature.vermont.gov/statutes/section/24APPENDIX/003/00163",
    "Burlington city charter, 24 App. V.S.A. ch. 3 section 163: "
    "'The Board of School Commissioners of said City shall be "
    "composed of 12 school commissioners. One commissioner from "
    "Ward One through Eight inclusive and one commissioner from "
    "each of the four districts shall be elected...' Section 4 "
    "provides each seat is elected only by the voters of its own "
    "ward or city district, and section 164 sets two-year terms "
    "(district seats in odd years, ward seats in even years). "
    "Charter section 165 fills vacancies by election only -- "
    "this board has no appointed members.")
BUR_RESULTS = S(
    "https://www.burlingtonvt.gov/179/Election-Results",
    "City of Burlington published election results (clerk's "
    "summary reports): the March 3, 2026 report names the eight "
    "ward winners (Golden 591, Vanderputten 815, Amato 576, "
    "Zygmant 1,285, Campriello 1,197, Wool 947, Ericksen 1,294, "
    "O'Toole 365) and the March 4, 2025 report the four district "
    "winners (Price 1,126, Waltz 1,415, Sowers 2,630, Wick "
    "2,507) -- all twelve match the district's board page with "
    "no mismatches.")
BUR_SRC = [BUR_PAGE, BUR_CHARTER, BUR_RESULTS]
_bur_posts = ([{"key": f"school-commissioner-ward-{n}",
                "title": f"School Commissioner - Ward {n}",
                "seats": 1} for n in range(1, 9)] +
              [{"key": f"school-commissioner-{d}-district",
                "title": f"School Commissioner - {d} District",
                "seats": 1}
               for d in ["central", "east", "north", "south"]])
_bur_dirs = []
for _n, _name, _slug in [
        (1, "Gary Golden", "gary-golden"),
        (2, "Polly Vanderputten", "polly-vanderputten"),
        (3, "Heather Amato", "heather-amato"),
        (4, "Melissa Zygmant", "melissa-zygmant"),
        (5, "Lucia Campriello", "lucia-campriello"),
        (6, "Clare Wool", "clare-wool"),
        (7, "Polly Ericksen", "polly-ericksen"),
        (8, "Jacqueline \"Nikki\" O'Toole", "jacqueline-nikki-otoole")]:
    _bur_dirs.append(H(_name, _slug,
                       post=f"school-commissioner-ward-{_n}",
                       sources=BUR_SRC))
for _d, _name, _slug in [
        ("central", "Jean Waltz", "jean-waltz"),
        ("east", "Matthew Price", "matthew-price"),
        ("north", "Kendra Sowers", "kendra-sowers"),
        ("south", "Jeff Wick", "jeff-wick")]:
    _bur_dirs.append(H(_name, _slug,
                       post=f"school-commissioner-{_d}-district",
                       sources=BUR_SRC))
emit(
    "burlington", "Burlington School District",
    [S(ST, "16 V.S.A. section 603(a) inventory: the Burlington "
           "Supervisory District is its own supervisory district, "
           "its district the Burlington School District (sole "
           "municipality: the City of Burlington)."),
     S("https://www.bsdvt.org",
       "Burlington School District (official district website).")],
    "Burlington Board of School Commissioners",
    [BUR_CHARTER, BUR_PAGE], _bur_posts, _bur_dirs)

# ---- 12. Cabot ----------------------------------------------------------
CAB_PAGE = S(
    "https://cabot.ccsuvt.net/204905_3",
    "Cabot School District board members page (official): five "
    "directors -- Chris Tormey (Chair, term expires 2028), "
    "Ellen Cairns (2029), Alicia Heber (Clerk, 2027), Jason "
    "Monaco (2028), Melissa Pratt (Vice-Chair, 2027). The same "
    "five sit in the March 23, June 22 and September 28, 2026 "
    "board minutes with none absent.")
CAB_RESULTS = S(
    "https://cabot.ccsuvt.net/budget",
    "Cabot School District official ballot results (district "
    "budget page): March 4, 2025 -- Chris Tormey elected to the "
    "3-year seat (301) and Melissa M. Pratt to the 2-year seat "
    "(307); March 3, 2026 -- Ellen Cairns to the 3-year seat "
    "(326) and Jason Monaco to the 2-year seat (303). The board "
    "is five directors at-large (16 V.S.A. section 423(a)-(b): "
    "three 3-year seats, two 2-year seats).")
emit(
    "cabot", "Cabot School District",
    [S(ST, "16 V.S.A. section 603(a)(6)(A) inventory: Cabot "
           "School District, a town school district in the "
           "Caledonia Central Supervisory Union (member town: "
           "Cabot)."),
     S("https://cabot.ccsuvt.net",
       "Cabot School (official district website).")],
    "Cabot School Board", [CAB_PAGE, CAB_RESULTS],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H("Chris Tormey", "chris-tormey", sources=[CAB_PAGE, CAB_RESULTS]),
     H("Ellen Cairns", "ellen-cairns", sources=[CAB_PAGE, CAB_RESULTS]),
     H("Jason Monaco", "jason-monaco", sources=[CAB_PAGE, CAB_RESULTS]),
     H("Melissa Pratt", "melissa-pratt",
       sources=[CAB_PAGE, CAB_RESULTS])],
)
# HELD: Alicia Heber -- verified current holder of the fifth seat
# (expires 2027, the seat Frank Kampf stepped down from in 2024),
# but no fetched document shows appointment vs. an August 2024
# primary election. Missing: the August 2024 primary results or a
# 2024 appointment minute.

# ---- 13. Caledonia Cooperative ------------------------------------------
CAL_ART = S(
    "http://barnetvt.org/wp-content/uploads/2014/04/Final-Report-Revised-Barnet-Walden-Waterford-Final-Version-for-AOE.pdf",
    "Caledonia Cooperative articles of agreement (study "
    "committee final report, 'Final Version for AOE', hosted on "
    "the Town of Barnet's official site), Article 8: 'The "
    "Unified District Board of Directors shall be composed of "
    "nine (9) individuals elected by Australian ballot by the "
    "voters of the municipalities in which they reside' -- three "
    "directors per member town (Barnet, Walden, Waterford), "
    "elected by that town's voters only, with weighted board "
    "votes for proportionality (16 V.S.A. section 730(a)(1) "
    "pattern); Article 9 sets three-year terms.")
CAL_PAGE = S(
    "https://www.ccsuvt.net/188124_3",
    "Caledonia Cooperative School District board page "
    "(Caledonia Central SU, official): the nine current "
    "directors by town with term expirations; all nine also "
    "appear in the June 8, 2026 board minutes.")
CAL_RES = S(
    "https://drive.google.com/file/d/1qpuWJbdufc24qD0esClnTSkjlPg-MJFp/view?usp=sharing",
    "Caledonia Cooperative certified results, March 3, 2026 "
    "(district document): Allison Gulka (Walden) and Erin "
    "Quatrini-Hill (Waterford) elected; the Barnet 3-year race "
    "is recorded 'No Elected Official'. Certified totals in the "
    "district's 2025-26 Annual Report (pp. 42-43) record the "
    "March 4, 2025 elections of Brittany Korsh (Barnet), Jason "
    "Miller (Waterford) and Dana Maxfield (Walden, write-in).")
emit(
    "caledonia-cooperative", "Caledonia Cooperative School District",
    [S(ST, "16 V.S.A. section 603(a)(6)(A) inventory: the "
           "Caledonia Cooperative School District, a unified "
           "union district in the Caledonia Central Supervisory "
           "Union (member towns Barnet, Walden, Waterford)."),
     S("https://www.ccsuvt.net",
       "Caledonia Central Supervisory Union (official site "
       "hosting the district's pages).")],
    "Caledonia Cooperative School Board", [CAL_ART, CAL_PAGE],
    [{"key": "school-director-barnet",
      "title": "School Director - Barnet", "seats": 3},
     {"key": "school-director-walden",
      "title": "School Director - Walden", "seats": 3},
     {"key": "school-director-waterford",
      "title": "School Director - Waterford", "seats": 3}],
    [H("Brittany Korsh", "brittany-korsh",
       post="school-director-barnet", sources=[CAL_PAGE, CAL_RES]),
     H("Marciel Greene", "marciel-greene",
       post="school-director-barnet", how_seated="appointed",
       sources=[S("https://docs.google.com/document/d/1_-sWRXzOo21kL-gCQI7k3Y3ltntRR172/edit?usp=sharing",
                  "Caledonia Cooperative board minutes, May 11, "
                  "2026: the board voted to add Marciel Greene "
                  "as a Barnet school member, filling the seat "
                  "the March 3, 2026 election left with 'No "
                  "Elected Official' (Heather Mulligan's term "
                  "expired and no candidate qualified). She "
                  "sits on the district's board page with a term "
                  "expiring 2027.")]),
     H("Dana Maxfield", "dana-maxfield",
       post="school-director-walden", sources=[CAL_PAGE, CAL_RES]),
     H("Allison Gulka", "allison-gulka",
       post="school-director-walden",
       existing_person_id="ocd-person/504da38b-2309-5163-9e81-844c471d952b",
       sources=[CAL_PAGE, CAL_RES]),
     H("Victoria Atwood", "victoria-atwood",
       post="school-director-walden",
       existing_person_id="ocd-person/6ab31eb4-cbdc-5f57-8ef2-0b1fbfdcd710",
       sources=[CAL_PAGE, CAL_RES]),
     H("Jason Miller", "jason-miller",
       post="school-director-waterford", sources=[CAL_PAGE, CAL_RES]),
     H("Erin Quatrini-Hill", "erin-quatrini-hill",
       post="school-director-waterford", sources=[CAL_PAGE, CAL_RES])],
)
# HELD: Bobbie Roy (Barnet) and Daniel Gingue (Waterford) -- both
# verified current (term exp. 2027), but their current terms rest
# on the April 2, 2024 election whose certified totals sit in a
# 2024-25 annual report whose district link now 404s.

# ---- 14. Cambridge -------------------------------------------------------
CAM_MIN = S(
    "https://drive.google.com/file/d/1GD-TOQu46V0zP7K567_J_fFB9rDirf7u/view?usp=sharing",
    "Cambridge School District board minutes, October 7, 2026 "
    "(district document): 'School Board Members: Rachael "
    "Mascolino, Brendan McCarthy, Jan Sander, Mark Stebbins, "
    "Denise Webster' -- the full five-member board, none absent; "
    "the board is five directors elected at-large (16 V.S.A. "
    "section 423(a)-(b)).")
CAM_ELECT = S(
    "https://ces.lnsd.org/news/details/~board/ces-news/post/annualmeeting-results-2026",
    "Cambridge School District official results notice, March "
    "3, 2026 annual meeting: Jan Sander elected to the 3-year "
    "seat and Rachael Mascolino to the 2-year seat. The March 4, "
    "2025 annual meeting minutes elect Mark Stebbins (3-year "
    "seat) and Denise Webster (warned 2-year seat -- the "
    "minutes' motion text saying '3 years' is a boilerplate slip "
    "the district repeats for 2-year seats; the warned article "
    "controls).")
emit(
    "cambridge", "Cambridge School District",
    [S(ST, "16 V.S.A. section 603(a)(7)(E) inventory: Cambridge "
           "School District, a town school district in the "
           "Lamoille North Supervisory Union (member town: "
           "Cambridge). The district operates PK-6; grades 7-12 "
           "sit with the Lamoille North Modified Unified Union "
           "School District, a separate district."),
     S("https://ces.lnsd.org",
       "Cambridge Elementary School (official district site, "
       "under the Lamoille North SU).")],
    "Cambridge School Board", [CAM_MIN, CAM_ELECT],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H("Mark Stebbins", "mark-stebbins", sources=[CAM_MIN, CAM_ELECT]),
     H("Jan Sander", "jan-sander",
       existing_person_id="ocd-person/d8fb8770-72f7-53a1-896b-1304d90b8300",
       sources=[CAM_MIN, CAM_ELECT]),
     H("Rachael Mascolino", "rachael-mascolino",
       sources=[CAM_MIN, CAM_ELECT]),
     H("Denise Webster", "denise-webster",
       existing_person_id="ocd-person/5b191fce-0428-5384-9f5d-e92356babb9d",
       sources=[CAM_MIN, CAM_ELECT]),
     H("Lori Hébert", "lori-hebert", end="2026",
       sources=[S("https://drive.google.com/file/d/1Bz-MLaxKLPnzBYkVQao00MGyaNq_GshU/view?usp=sharing",
                  "Cambridge board minutes, June 3, 2026: Lori "
                  "Hebert [sic] 'submitted a letter of "
                  "resignation effective June 30' on taking a "
                  "teaching job at the school. She had been "
                  "elected March 5, 2024 to a 3-year term and "
                  "served on the board through the March 4, 2026 "
                  "reorganization; her membership is ended in "
                  "2026. The district's canonical spelling is "
                  "Hebert with an accented e (Hébert).")]),
     H("Brendan McCarthy", "brendan-mccarthy", how_seated="appointed",
       sources=[S("https://drive.google.com/file/d/1t2YAZl5F14MoGm3vY-kHDM0A49d4zNjG/view?usp=drive_link",
                  "Cambridge board minutes, July 8, 2026: 'J. "
                  "Sander moved to appoint Brendan McCarthy to "
                  "the vacancy on the school board... the motion "
                  "was passed.' The vacancy was Lori Hebert's "
                  "(resigned effective June 30, 2026), whose "
                  "elected term runs to 2027; the appointment "
                  "minute states no end date.")])],
)

# ---- 15. Canaan ------------------------------------------------------------
CAN_RET = S(
    "https://canaan-vt.org/images/Australian_Ballot_Official_Return_Of_Votes.pdf",
    "Town of Canaan Official Return of Votes, March 3, 2026 "
    "annual town and school district election (official, posted "
    "by the town): Raelene Begin elected to the 3-year SCHOOL "
    "DIRECTOR seat (95 votes); Renee Marchesseault (98) and "
    "Martha Vanderwolk (85) elected to the two 2-year seats.")
CAN_ROSTER = S(
    "https://canaan-vt.org/images/2025_Town_Report.Reduced.pdf",
    "Town of Canaan 2025 Town Report, officers list: five School "
    "Directors in the section 423(a)-(b) shape (three 3-year "
    "seats, two 2-year seats) -- Raelene Begin, Terrie Herr "
    "(3-year term ending 2027), Kristie Begin (2028), Martha "
    "Vanderwolk, Renee Marchesseault. The district's March 9, "
    "2026 reorganization minutes seat the same five (with "
    "Kristie Begin's membership held in this build -- see the "
    "district report on issue #163).")
emit(
    "canaan", "Canaan School District",
    [S(ST, "16 V.S.A. section 603(a)(6)(B) inventory: Canaan "
           "School District, a town school district in the Essex "
           "North Supervisory Union (member town: Canaan)."),
     S("https://www.ensuvt.org",
       "Essex North Supervisory Union (official site hosting "
       "the district's board page).")],
    "Canaan School Board", [CAN_RET, CAN_ROSTER],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H("Renee Marchesseault", "renee-marchesseault",
       existing_person_id="ocd-person/4dda18ed-037f-5224-bc82-e223dba19f6a",
       sources=[CAN_RET, CAN_ROSTER]),
     H("Martha Vanderwolk", "martha-vanderwolk",
       sources=[CAN_RET, CAN_ROSTER]),
     H("Raelene Begin", "raelene-begin", sources=[CAN_RET, CAN_ROSTER]),
     H("Terrie Herr", "terrie-herr",
       sources=[S("https://canaan-vt.org/images/2025_Town_Report.Reduced.pdf",
                  "Terrie Herr's current 3-year term (ending "
                  "2027) rests on the Town of Canaan 2025 Town "
                  "Report officers list; no certified results "
                  "for her term were posted by the town. Her "
                  "continuous service is documented in district "
                  "minutes from September 2023 through October "
                  "2026. (One warning signature block prints "
                  "'Therese Herr'; the ballot, minutes, board "
                  "page and town report all read Terrie Herr.)")])],
)
# HELD: Kristie Begin -- verified current director (3-year seat
# to 2028, seated at the March 10, 2025 reorganization), but the
# March 4, 2025 ballot seat was write-in-only and no appointment
# vote exists; the March 4, 2025 Official Return of Votes (the
# settling document) is not posted by the town.
print("part 1 done")

# ---- 16. Champlain Islands UUSD -------------------------------------------
CI_RET = S(
    "https://grandisle.ecopixel.com/fileadmin/files/Archive/2026/03/2026-Grand-Isle-Results-030326.pdf",
    "Town of Grand Isle official return of votes, March 3, 2026: "
    "'UNIFIED UNION BOARD MEMBER - 3 YEARS -- ANDREW BAHRENBURG, "
    "GRAND ISLE, 408'. Directors are elected by each member town "
    "on its own ballot (the Town of North Hero's March 2026 "
    "warning likewise warns a district 'representative for a "
    "term of three years'), the proportional-to-town pattern "
    "(16 V.S.A. section 730(a)(1)).")
CI_FLAG = S(
    "https://www.gisu.org",
    "Grand Isle Supervisory Union (official). The district's "
    "2016 articles of agreement could not be retrieved (the AOE "
    "study-committee copies return 403 and the SU document "
    "library is script-driven), so the board's size and "
    "allocation -- six seats, observed as two per member town "
    "across 2020-2024 district minutes -- are modeled as "
    "OBSERVED, not articles-confirmed, and all memberships "
    "except the one certified 2026 winner are held: the last "
    "complete official roster is from 2023-24 minutes and two "
    "election cycles have intervened.")
CI_POST_SRC = [CI_RET, CI_FLAG]
emit(
    "champlain-islands-unified-union",
    "Champlain Islands Unified Union School District",
    [S(ST, "16 V.S.A. section 603(a)(1)(C) inventory: the "
           "Champlain Islands Unified Union School District, a "
           "unified union district in the Grand Isle Supervisory "
           "Union (member towns Grand Isle, Isle La Motte, North "
           "Hero)."),
     S("https://www.gisu.org",
       "Grand Isle Supervisory Union (official site).")],
    "Champlain Islands Unified Union School Board",
    [CI_RET, CI_FLAG],
    [{"key": "school-director-grand-isle",
      "title": "School Director - Grand Isle", "seats": 2,
      "sources": CI_POST_SRC},
     {"key": "school-director-isle-la-motte",
      "title": "School Director - Isle La Motte", "seats": 2,
      "sources": CI_POST_SRC},
     {"key": "school-director-north-hero",
      "title": "School Director - North Hero", "seats": 2,
      "sources": CI_POST_SRC}],
    [H("Andrew Bahrenburg", "andrew-bahrenburg",
       post="school-director-grand-isle", sources=[CI_RET])],
)

# ---- 17. Champlain Valley ---------------------------------------------------
CV_PAGE = S(
    "https://www.cvsdvt.org/school-board-ab/school-board-members",
    "Champlain Valley School District board members page "
    "(official): the twelve current directors by town with term "
    "expirations -- Charlotte: Meghan Metzler (2027), Meghan "
    "Siket (2029); Hinesburg: Keith Roberts (2028), Cassandra "
    "Townshend (2029); Shelburne: Dave Connery (2029), Erika "
    "Lea (2028), Kate Webb (2027); St. George: Lindsay Colf "
    "(2028); Williston: Erin Henderson (2029), Brendan McMahon "
    "(2027), Jean Sanchez (2028), Sarah Showalter-Feuillette "
    "(2027).")
CV_ALLOC = S(
    "https://www.hinesburgrecord.org/api/v1/file/f0c949ab-9870-4c26-ae13-734d5b6194b2.pdf",
    "The district's twelve seats are allocated by town and "
    "elected by each town's voters only (Charlotte 2, Hinesburg "
    "2, Shelburne 3, St. George 1, Williston 4), per the CSSU "
    "study committee's own presentation ('12-Member Board. Board "
    "members elected by town based on 2010 census') and "
    "confirmed by the Town of Hinesburg's March 3, 2026 warning, "
    "whose ballot carries only Hinesburg's own 'Champlain "
    "Valley School District Director for a term of 3 years'. "
    "The verbatim 2016 articles of agreement were not "
    "retrieved; the composition sources agree.")
CV_SRC = [CV_PAGE, CV_ALLOC]
emit(
    "champlain-valley", "Champlain Valley School District",
    [S(ST, "16 V.S.A. section 603(a)(3)(C) inventory: the "
           "Champlain Valley Supervisory District's district is "
           "the Champlain Valley School District (member towns "
           "Charlotte, Hinesburg, Shelburne, St. George, "
           "Williston)."),
     S("https://www.cvsdvt.org",
       "Champlain Valley School District (official district "
       "website).")],
    "Champlain Valley School Board", CV_SRC,
    [{"key": "school-director-charlotte",
      "title": "School Director - Charlotte", "seats": 2},
     {"key": "school-director-hinesburg",
      "title": "School Director - Hinesburg", "seats": 2},
     {"key": "school-director-shelburne",
      "title": "School Director - Shelburne", "seats": 3},
     {"key": "school-director-st-george",
      "title": "School Director - St. George", "seats": 1},
     {"key": "school-director-williston",
      "title": "School Director - Williston", "seats": 4}],
    [H("Meghan Metzler", "meghan-metzler",
       post="school-director-charlotte", sources=CV_SRC),
     H("Meghan Siket", "meghan-siket",
       post="school-director-charlotte", sources=CV_SRC),
     H("Keith Roberts", "keith-roberts",
       post="school-director-hinesburg", sources=CV_SRC),
     H("Cassandra Townshend", "cassandra-townshend",
       post="school-director-hinesburg", sources=CV_SRC),
     H("Dave Connery", "dave-connery",
       post="school-director-shelburne", sources=CV_SRC),
     H("Erika Lea", "erika-lea",
       post="school-director-shelburne", sources=CV_SRC),
     H("Kate Webb", "kate-webb",
       post="school-director-shelburne", sources=CV_SRC),
     H("Lindsay Colf", "lindsay-colf",
       post="school-director-st-george", sources=CV_SRC),
     H("Erin Henderson", "erin-henderson",
       post="school-director-williston", sources=CV_SRC),
     H("Brendan McMahon", "brendan-mcmahon",
       post="school-director-williston", sources=CV_SRC),
     H("Jean Sanchez", "jean-sanchez",
       post="school-director-williston", sources=CV_SRC),
     H("Sarah Showalter-Feuillette", "sarah-showalter-feuillette",
       post="school-director-williston", sources=CV_SRC)],
)

# ---- 18. Charleston ----------------------------------------------------------
CHA_PAGE = S(
    "https://www.ncsuvt.org/47188_2",
    "Charleston School Board page (North Country SU, official), "
    "2026-2027 block: Mary Esposito (Chair), Sarah Jenness (Vice "
    "Chair), Rebecca Midthun (Clerk) -- the same three sit in "
    "the board's October 14, 2026 and March 11, 2026 minutes. "
    "The board is three directors elected at-large (16 V.S.A. "
    "section 423(a)). Published terms (town annual reports): "
    "Esposito to 2027, Jenness to 2025 as last published in 2024 "
    "(her current term, on the section 423(a) stagger and "
    "continuous service, runs to 2028).")
emit(
    "charleston", "Charleston School District",
    [S(ST, "16 V.S.A. section 603(a) inventory: Charleston "
           "School District, a town school district in the North "
           "Country Supervisory Union (member town: "
           "Charleston)."),
     S("https://www.ncsuvt.org",
       "North Country Supervisory Union (official site hosting "
       "the district's board page).")],
    "Charleston School Board", [CHA_PAGE],
    [{"key": "school-director", "title": "School Director",
      "seats": 3}],
    [H("Mary Esposito", "mary-esposito", sources=[CHA_PAGE]),
     H("Sarah Jenness", "sarah-jenness", sources=[CHA_PAGE]),
     H("Rebecca Midthun", "rebecca-midthun",
       sources=[S("https://www.ncsuvt.org/47188_2",
                  "Rebecca Midthun sits as a Charleston director "
                  "from the March 13, 2024 reorganization meeting "
                  "onward (NCSU board page; October 14, 2026 "
                  "minutes). Ryan Besaw, who held the third seat "
                  "into early 2024, is absent from the February "
                  "14, 2024 minutes and no appointment motion for "
                  "Midthun appears in any minutes from February "
                  "2024 to February 2026 -- she is recorded as "
                  "elected at the March 5, 2024 annual meeting on "
                  "that minutes chain. Her exact term end is "
                  "UNRESOLVED (2026-remainder vs. fresh term; "
                  "the March 2024 warning/results and a March "
                  "2026 Charleston return are not posted), so "
                  "no term end is stated for her seat.")])],
)

# ---- 19. Colchester ------------------------------------------------------------
COL_DIR = S(
    "https://www.csdvt.org/district/schoolboard/members.php",
    "Colchester School District School Board Member Directory "
    "(official): five directors -- Lindsey Cox (Chair, 3-year "
    "term expiring March 2029), Nic Longo (Vice Chair, 3-year, "
    "2028), Ben Yousey-Hindes (Clerk, 2-year, 2027), Laurie "
    "Kigonya (3-year, 2027), Jennifer Fath (2-year, 2028). The "
    "same five are in attendance in the October 6, 2026 board "
    "minutes. The mix (three 3-year seats, two 2-year seats) is "
    "the 16 V.S.A. section 423(a)-(b) town-district shape.")
emit(
    "colchester", "Colchester School District",
    [S(ST, "16 V.S.A. section 603(a)(2)(B) inventory: the "
           "Colchester Supervisory District's district is the "
           "Colchester School District (member town: "
           "Colchester)."),
     S("https://www.csdvt.org",
       "Colchester School District (official district "
       "website).")],
    "Colchester School Board", [COL_DIR],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H("Lindsey Cox", "lindsey-cox", sources=[COL_DIR]),
     H("Nic Longo", "nic-longo", sources=[COL_DIR]),
     H("Ben Yousey-Hindes", "ben-yousey-hindes", sources=[COL_DIR]),
     H("Laurie Kigonya", "laurie-kigonya", sources=[COL_DIR]),
     H("Jennifer Fath", "jennifer-fath", sources=[COL_DIR])],
)

# ---- 20. Coventry ----------------------------------------------------------------
COV_PAGE = S(
    "https://www.ncsuvt.org/47189_2",
    "Coventry School Board page (North Country SU, official), "
    "2026-2027 block: Praneet Menon (Chair), Sarah Bathalon "
    "(Vice Chair), Amanda Hussey (Clerk), Charles Conn, Jaime "
    "Stenger -- the same five in the September 16, 2026 "
    "full-board minutes and the March 18, 2026 reorganization "
    "minutes (which record Conn's and Hussey's March 2026 "
    "re-elections). The board is five directors at-large (16 "
    "V.S.A. section 423(a)-(b)); per-member term expirations "
    "are published nowhere reachable, so none are stated.")
emit(
    "coventry", "Coventry School District",
    [S(ST, "16 V.S.A. section 603(a) inventory: Coventry School "
           "District, a town school district in the North "
           "Country Supervisory Union (member town: Coventry)."),
     S("https://www.ncsuvt.org",
       "North Country Supervisory Union (official site hosting "
       "the district's board page).")],
    "Coventry School Board", [COV_PAGE],
    [{"key": "school-director", "title": "School Director",
      "seats": 5}],
    [H("Praneet Menon", "praneet-menon",
       existing_person_id="ocd-person/fab074aa-22dc-58ef-a7a8-7dd83880ff46",
       sources=[COV_PAGE]),
     H("Sarah Bathalon", "sarah-bathalon", sources=[COV_PAGE]),
     H("Amanda Hussey", "amanda-hussey",
       existing_person_id="ocd-person/85b0a866-eab8-5d5c-bccd-9acf850707c6",
       sources=[COV_PAGE]),
     H("Charles Conn", "charles-conn", sources=[COV_PAGE]),
     H("Jaime Stenger", "jaime-stenger", sources=[COV_PAGE])],
)
print("part 2 done")
