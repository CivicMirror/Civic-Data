#!/usr/bin/env python3
"""Held-straggler sweep for the VT #163 municipal fan-out.

After batches 1-28 completed all 278 municipalities, 837 posts still
had unfilled seats (1,282 seats, 226 places; JP posts excluded --
their certified slates are complete and the extra seats are genuine
vacancies). This script emits one JSON spec per municipality touched
by the sweep for build_vt_municipality.py, carrying ONLY the offices
and holders the sweep resolved from official sources (every claim
firsthand-verified by the operator against the cited document;
research and per-item dispositions are in
scripts/vt_muni_sweep_research.md and the #163 sweep report).

Existing org/post files are left untouched by the builder (SKIP);
the specs therefore create only new person and membership files,
plus the one genuinely new post (Danville delinquent tax collector).
Structural corrections (post removals, membership endings, seat-count
fixes, source-note replacements) are NOT done here -- they are
hand-applied edits listed in the sweep research notes.

Marshfield Village is not touched (held for the maintainer's own
clarification). Albany Village and Jericho Village remain held (no
official roster exists). Items resting on self-labeled UNOFFICIAL
results (Morrisville, Mendon) are NOT minted here -- they are
decision items in the sweep report.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "vt_muni_data"


def S(url, note):
    return {"url": url, "note": note}


def holder(name, slug, **kw):
    d = {"name": name, "slug": slug}
    d.update(kw)
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
ORDER = []


def spec(place_slug, offices):
    orig = json.loads((DATA_DIR / f"{place_slug}.json").read_text())
    SPECS[place_slug] = {
        "label": orig["label"],
        "place_slug": place_slug,
        "jurisdiction_id": orig["jurisdiction_id"],
        "header": f"# {orig['label']} municipal roster backfill -- "
                  f"Vermont\n# held-straggler sweep; issue #163 "
                  f"(VT master tracking).\n",
        "offices": offices,
    }
    ORDER.append(place_slug)


# ================================================================
# V2 -- Enosburg Falls (village), Hyde Park (village)
# ================================================================
ENOSBURG_MINUTES = "https://enosburghvt.org/village-of-enosburg-falls/"
spec("enosburg-falls", [
    office("village-clerk", "Village Clerk",
           "Village of Enosburg Falls Village Clerk", 1,
           [S(ENOSBURG_MINUTES,
              "Village of Enosburg Falls, Board of Trustees minutes, "
              "March 31, 2026 (draft), item 6: the trustees appointed "
              "Roberta Morin village clerk for a one-year term; she is "
              "again styled 'Village Clerk' in the trustees' minutes "
              "of September 22, 2026. Draft status disclosed.")],
           [holder("Roberta Morin", "roberta-morin",
                   how_seated="appointed")]),
    office("village-treasurer", "Village Treasurer",
           "Village of Enosburg Falls Village Treasurer", 1,
           [S(ENOSBURG_MINUTES,
              "Village of Enosburg Falls, Board of Trustees minutes, "
              "March 31, 2026 (draft), item 6: the trustees appointed "
              "Roberta Morin village treasurer for a one-year term. "
              "Draft status disclosed.")],
           [holder("Roberta Morin", "roberta-morin",
                   how_seated="appointed")]),
])

spec("hyde-park", [
    office("village-trustee", "Village Trustee",
           "Hyde Park Village Board of Trustees", 5,
           [S("https://www.hydeparkvt.com/village",
              "Village of Hyde Park: Annual Village Meeting summary, "
              "May 5, 2026, Article 4 elects a trustee for the two-year "
              "term ending 2028 but prints the winner's name blank. "
              "Amy O'Toole held the only two-year trustee seat "
              "expiring in 2026, and the trustees' minutes of "
              "June 4, 2026 and five later 2026 sets list her as a "
              "sitting trustee, with no vacancy appointment recorded; "
              "she is minted elected on this identification by "
              "elimination, disclosed here and on issue #163.")],
           [holder("Amy O'Toole", "amy-otoole")]),
])

# ================================================================
# C8 -- Lincoln, Ludlow (town), Lyndon, Manchester, Middletown Springs
# ================================================================
LINCOLN_RETURN = ("https://lincolnvermont.org/uploads/dm/7597/"
                  "Mar_3_2026_Official_Return_Of_Votes")
spec("lincoln", [
    office("library-trustee", "Library Trustee",
           "Town of Lincoln Library Trustees", 5,
           [S(LINCOLN_RETURN,
              "Town of Lincoln, Official Return of Votes, Annual Town "
              "Meeting, March 3, 2026 (certified, Vermont Secretary "
              "of State, Elections Division): 'LINCOLN LIBRARY "
              "TRUSTEE - 3 YEARS -- Vote for not more than TWO -- "
              "JENNY BATES 230; SUZANNE GERMAIN 230' (one write-in "
              "for Stephen Teach, 1).")],
           [holder("Jenny Bates", "jenny-bates"),
            holder("Suzanne Germain", "suzanne-germain")]),
])

LUDLOW_SB = ("https://ludlow.vt.us/vertical/sites/"
             "%7B78E8DA21-0D46-4486-AF59-9D2B5A1048F3%7D/uploads/"
             "Select_Board_Minutes_-_April_6_2026.pdf")
LUDLOW_CEM = ("https://ludlow.vt.us/vertical/sites/"
              "%7B78E8DA21-0D46-4486-AF59-9D2B5A1048F3%7D/uploads/"
              "Cemetery_Meeting_Minutes_-_July_15_2026.pdf")
spec("ludlow-41275", [
    office("first-constable", "First Constable",
           "Town of Ludlow First Constable", 1,
           [S(LUDLOW_SB,
              "Town of Ludlow, Board of Selectmen minutes, April 6, "
              "2026, item VI.G (under 'Appoint Non-Elected Town "
              "Officers'): motion to appoint Jeff Billings to the "
              "First Constable position, passed unanimously.")],
           [holder("Jeff Billings", "jeff-billings",
                   how_seated="appointed")]),
    office("lister", "Lister", "Town of Ludlow Listers", 3,
           [S(LUDLOW_SB,
              "Town of Ludlow, Board of Selectmen minutes, April 6, "
              "2026, item VI.B ('Board of Listers - non-elected (2) "
              "Positions'): motion to appoint Doug Sheehan as Lister, "
              "passed unanimously (a reappointment; his prior "
              "appointed term had expired in 2025). Only one of the "
              "two non-elected lister positions was filled at that "
              "meeting.")],
           [holder("Doug Sheehan", "doug-sheehan",
                   how_seated="appointed")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Ludlow Trustees of Public Funds", 3,
           [S(LUDLOW_SB,
              "Town of Ludlow, Board of Selectmen minutes, April 6, "
              "2026, item VI.T: motion to appoint Doug Sheehan as "
              "Trustee of Public Funds, passed unanimously.")],
           [holder("Doug Sheehan", "doug-sheehan",
                   how_seated="appointed")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Ludlow Cemetery Commissioners", 5,
           [S(LUDLOW_CEM,
              "Town of Ludlow, Board of Cemetery Commissioners "
              "minutes, July 15, 2026 (confirmed identical in the "
              "minutes of September 16, 2026): 'Board Members "
              "Present: Bob Brandt, Bruce Schmidt, Scott Baitz, "
              "George Tucker, Jr.' Brandt was elected Chair at the "
              "commission's reorganization of March 18, 2026. No "
              "fetched document states the mechanism by which each "
              "holds his seat; the seating bases recorded here are "
              "the operator's disclosed adjudication (Brandt elected "
              "-- seated by the March 2026 reorganization past a "
              "printed 2025 term expiry; Baitz appointed -- "
              "continuity of his prior appointed seat; Tucker "
              "appointed -- he joined between March 18 and July 15, "
              "2026, when no election exists, i.e. a vacancy "
              "appointment, though no selectboard appointment minute "
              "was located in the April 6, June 1, or July 6, 2026 "
              "minutes). See issue #163 sweep report.")],
           [holder("Bob Brandt", "bob-brandt"),
            holder("Scott Baitz", "scott-baitz", how_seated="appointed"),
            holder("George Tucker, Jr.", "george-tucker-jr",
                   how_seated="appointed")]),
])

spec("lyndon", [
    office("library-trustee", "Library Trustee",
           "Town of Lyndon Library Trustees", 5,
           [S("https://cobleighlibrary.org/wp-content/uploads/2026/03/"
              "Trustee-Minutes-March-2026.pdf",
              "Cobleigh Public Library (Lyndon), Board of Trustees "
              "minutes, March 24, 2026: 'Recognize and thank former "
              "trustee Paula Pearce... Welcome new trustee, Susan "
              "Kuecker.' The trustees are elected at town meeting; "
              "Kuecker took the seat at the first trustees' meeting "
              "after the March 3, 2026 election. The minutes print "
              "no vote counts.")],
           [holder("Susan Kuecker", "susan-kuecker")]),
])

spec("manchester-42850", [
    office("moderator", "Moderator", "Town of Manchester Moderator", 1,
           [S("https://manchester-vt.gov/vertical/sites/"
              "%7BCE718C6D-0EC0-43CE-B71E-5A023B5D13EA%7D/uploads/"
              "OfficialAnnualTownMeeting2026Results.pdf",
              "Town of Manchester, '2026 Annual Town Meeting "
              "Results,' March 3, 2026 (official results): "
              "'Moderator - 1-year term -- Mike Nawrath -- 481 "
              "(DECLARED ELECTED)'. The full name form W. Michael "
              "Nawrath is from the town's Annual Town Meeting "
              "minutes of February 28, 2026.")],
           [holder("W. Michael Nawrath", "w-michael-nawrath")]),
])

spec("middletown-springs", [
    office("moderator", "Moderator",
           "Town of Middletown Springs Moderator", 1,
           [S("https://storage.googleapis.com/juniper-media-library/"
              "359/2026/03/2026%20Town%20Meeting%20Results%20for%20"
              "web%20rev%203.5.26.pdf",
              "Town of Middletown Springs, '2026 Town Meeting "
              "Results' (rev. 3.5.26), Town Officers: 'Moderator -- "
              "Andrew Hayes 202 -- Write In 0 -- Blank 29'. Hayes "
              "was previously seated by appointment until Town "
              "Meeting 2025 and was elected at the March 3, 2026 "
              "vote.")],
           [holder("Andrew Hayes", "andrew-hayes")]),
])

spec("middlebury", [
    office("library-trustee", "Library Trustee",
           "Ilsley Public Library Trustees", 5,
           [S("https://www.ilsleypubliclibrary.org/",
              "Ilsley Public Library (Middlebury), Board of "
              "Trustees minutes, April 13 and September 14, "
              "2026: Claire Tebbs sits as a trustee, completing "
              "the five-member board. The board is elected at "
              "town meeting. The town's March 2026 results PDF "
              "could not be fetched (townofmiddlebury.org "
              "returns a bot wall to both direct fetches and "
              "the agent browser), so the mint rests on the "
              "library's own minutes chain, disclosed on issue "
              "#163. The moderator and the third lister seat "
              "stay unresolved behind the same block.")],
           [holder("Claire Tebbs", "claire-tebbs")]),
])

# ================================================================
# C1 -- Barnet, Baltimore, Andover, Athens, Bennington
# ================================================================
BARNET_TM = ("https://barnetvt.org/wp-content/uploads/2026/05/"
             "2026_TownMeeting_Minutes-1.pdf")
BARNET_SB = ("https://barnetvt.org/wp-content/uploads/2026/03/"
             "2026_03_09_SelBMinRegularDraft.pdf")
BARNET_TM_NOTE = ("Town of Barnet, Annual Town Meeting minutes, "
                  "March 3, 2026 (floor elections): ")
spec("barnet", [
    office("auditor", "Auditor", "Town of Barnet Auditors", 3,
           [S(BARNET_TM, BARNET_TM_NOTE +
              "Joseph Breidenstein was elected auditor.")],
           [holder("Joseph Breidenstein", "joseph-breidenstein")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Barnet Collector of Delinquent Taxes", 1,
           [S(BARNET_TM, BARNET_TM_NOTE +
              "Jeremy Roberts was elected Collector of Delinquent "
              "Taxes.")],
           [holder("Jeremy Roberts", "jeremy-roberts")]),
    office("lister", "Lister", "Town of Barnet Listers", 3,
           [S(BARNET_TM, BARNET_TM_NOTE +
              "Celina Wright was elected lister.")],
           [holder("Celina Wright", "celina-wright")]),
    office("moderator", "Moderator", "Town of Barnet Moderator", 1,
           [S(BARNET_TM, BARNET_TM_NOTE +
              "Dennis McLam was elected moderator.")],
           [holder("Dennis McLam", "dennis-mclam")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Barnet Trustees of Public Funds", 3,
           [S(BARNET_TM, BARNET_TM_NOTE +
              "David Warden was elected Trustee of Public Funds, "
              "taking the seat whose term expired in 2026.")],
           [holder("David Warden", "david-warden")]),
    office("grand-juror", "Grand Juror", "Town of Barnet Grand Juror",
           1,
           [S(BARNET_SB,
              "Town of Barnet, Selectboard organizational meeting "
              "minutes, March 9, 2026 (marked DRAFT, disclosed): "
              "David Willis was appointed Grand Juror.")],
           [holder("David Willis", "david-willis",
                   how_seated="appointed")]),
])

BALTIMORE_TM = "https://www.baltimorevt.org/minutes.htm"
BALTIMORE_NOTE = ("Town of Baltimore, Annual Town Meeting minutes, "
                  "March 3, 2026 (floor elections; served from the "
                  "town's minutes page): ")
spec("baltimore", [
    office("moderator", "Moderator", "Town of Baltimore Moderator", 1,
           [S(BALTIMORE_TM, BALTIMORE_NOTE +
              "Joan Whaley was elected moderator.")],
           [holder("Joan Whaley", "joan-whaley")]),
    office("grand-juror", "Grand Juror",
           "Town of Baltimore Grand Juror", 1,
           [S(BALTIMORE_TM, BALTIMORE_NOTE +
              "Steve Waldo was elected Grand Juror.")],
           [holder("Steve Waldo", "steve-waldo")]),
    office("town-agent", "Town Agent", "Town of Baltimore Town Agent",
           1,
           [S(BALTIMORE_TM, BALTIMORE_NOTE +
              "Derek Bruce was elected Town Agent.")],
           [holder("Derek Bruce", "derek-bruce")]),
    office("auditor", "Auditor", "Town of Baltimore Auditors", 3,
           [S(BALTIMORE_TM, BALTIMORE_NOTE +
              "Sheila Patch was elected auditor for the term ending "
              "2029.")],
           [holder("Sheila Patch", "sheila-patch")]),
])

ANDOVER_REPORT = "https://www.andovervt.org/s/2025-Town-Report-from-Repro.pdf"
ANDOVER_NOTE = ("Town of Andover, 2025.26 Annual Town Report, elected "
                "officers table (term-continuity: the printed terms "
                "run past the March 2026 meeting): ")
spec("andover", [
    office("auditor", "Auditor", "Town of Andover Auditors", 3,
           [S(ANDOVER_REPORT, ANDOVER_NOTE +
              "Auditors Wendell Perkins (term to 2027) and Cindy "
              "Ingersoll (term to 2028).")],
           [holder("Wendell Perkins", "wendell-perkins"),
            holder("Cindy Ingersoll", "cindy-ingersoll")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Andover Cemetery Commissioners", 3,
           [S(ANDOVER_REPORT, ANDOVER_NOTE +
              "Cemetery Commissioner Hank Mauti (term to 2028).")],
           [holder("Hank Mauti", "hank-mauti")]),
])

spec("athens", [
    office("moderator", "Moderator", "Town of Athens Moderator", 1,
           [S("https://www.athensvt.com/officials.html",
              "Town of Athens, Officials page (live): David Bemis is "
              "named Moderator under 'Elected Boards and Officials'.")],
           [holder("David Bemis", "david-bemis")]),
])

spec("bennington", [
    office("moderator", "Moderator", "Town of Bennington Moderator", 1,
           [S("https://benningtonvt.org/government/town_meetings.php",
              "Town of Bennington moderator chain: the 2024 Annual "
              "Town Report's officers table gives Jason Morrissey a "
              "three-year moderator term to March 2025; the 2025 "
              "Warning placed the three-year moderator election on "
              "the March 2025 ballot; and the Select Board minutes "
              "of March 2, 2026 style him 'MODERATOR: Jason "
              "Morrissey' presiding. Minted elected on this chain, "
              "disclosed on issue #163.")],
           [holder("Jason Morrissey", "jason-morrissey")]),
])

# ================================================================
# C2 -- Benson, Bolton, Braintree, Bridgewater, Bethel, Bradford
# ================================================================
BENSON_TM = "https://bensonvermont.gov/"
BENSON_NOTE = ("Town of Benson, Annual Town Meeting minutes, "
               "February 28 and March 3, 2026 (floor elections): ")
spec("benson", [
    office("moderator", "Moderator", "Town of Benson Moderator", 1,
           [S(BENSON_TM, BENSON_NOTE +
              "John Hill was elected Moderator.")],
           [holder("John Hill", "john-hill")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Benson Collector of Delinquent Taxes", 1,
           [S(BENSON_TM, BENSON_NOTE +
              "Barbara Burlett was elected Collector of Delinquent "
              "Taxes.")],
           [holder("Barbara Burlett", "barbara-burlett")]),
    office("auditor", "Auditor", "Town of Benson Auditors", 3,
           [S(BENSON_TM, BENSON_NOTE +
              "Lynn Bowen was elected auditor."),
            S(BENSON_TM,
              "Town of Benson, 2024-2025 Annual Report, elected "
              "officers table (term-continuity): auditors Cheryl "
              "Murray (term to 2027) and Robert Bizek (term to "
              "2028).")],
           [holder("Lynn Bowen", "lynn-bowen"),
            holder("Cheryl Murray", "cheryl-murray"),
            holder("Robert Bizek", "robert-bizek")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Benson Trustees of Public Funds", 3,
           [S(BENSON_TM, BENSON_NOTE +
              "Carrie LaFond was elected Trustee of Public Funds."),
            S(BENSON_TM,
              "Town of Benson, 2024-2025 Annual Report, elected "
              "officers table (term-continuity): Trustees of Public "
              "Funds Jayme Van Noordt Purdy (term to 2027) and Brad "
              "Barrett (term to 2028).")],
           [holder("Carrie LaFond", "carrie-lafond"),
            holder("Jayme Van Noordt Purdy", "jayme-van-noordt-purdy"),
            holder("Brad Barrett", "brad-barrett")]),
])

spec("bolton", [
    office("moderator", "Moderator", "Town of Bolton Moderator", 1,
           [S("https://boltonvt.com/",
              "Town of Bolton, Official Return of Votes, Annual Town "
              "Meeting, March 3, 2026 (certified): Leslie Pelch was "
              "elected Moderator with 204 votes as the sole "
              "candidate. (The 2026 Town Report's 'Petch' spelling "
              "is a misprint; the certified return governs.)")],
           [holder("Leslie Pelch", "leslie-pelch")]),
])

BRAINTREE_REPORT = "https://braintreevt.gov/"
BRAINTREE_NOTE = ("Town of Braintree, 2025 Annual Report, elected "
                  "officers table (term-continuity: the seats below "
                  "did not stand at the March 2026 meeting): ")
spec("braintree", [
    office("lister", "Lister", "Town of Braintree Listers", 3,
           [S(BRAINTREE_REPORT, BRAINTREE_NOTE +
              "Listers Jackson Evans (term to 2027) and Lydia Evans "
              "(term to 2028); Grace Persons, whose term expired "
              "in 2026, already holds the third seat's record.")],
           [holder("Jackson Evans", "jackson-evans"),
            holder("Lydia Evans", "lydia-evans")]),
    office("auditor", "Auditor", "Town of Braintree Auditors", 3,
           [S(BRAINTREE_REPORT, BRAINTREE_NOTE +
              "Auditors Colin Evans (term to 2027) and Tori Vinton "
              "(term to 2028).")],
           [holder("Colin Evans", "colin-evans"),
            holder("Tori Vinton", "tori-vinton")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Braintree Cemetery Commissioners", 3,
           [S(BRAINTREE_REPORT, BRAINTREE_NOTE +
              "Cemetery Commissioners Karl Jassen (term to 2027) "
              "and Cal Poulin (term to 2028).")],
           [holder("Karl Jassen", "karl-jassen"),
            holder("Cal Poulin", "cal-poulin")]),
])

BRIDGEWATER_REPORT = "https://www.bridgewater.vt.gov/"
BRIDGEWATER_NOTE = ("Town of Bridgewater, FY2025 Annual Town Report, "
                    "elected officers table: ")
spec("bridgewater", [
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Bridgewater Cemetery Commissioners", 3,
           [S(BRIDGEWATER_REPORT, BRIDGEWATER_NOTE +
              "'Cemetery: Gregory Jenne 2023-2026 / Owen Astbury "
              "2024-2027 / Roy (Butch) Wardwell 2025-2028'.")],
           [holder("Roy Wardwell", "roy-wardwell")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Bridgewater Trustees of Public Funds", 1,
           [S(BRIDGEWATER_REPORT, BRIDGEWATER_NOTE +
              "Trustee of Public Funds Mary Oldenburg, 2025-2028 "
              "(her line carries no resignation mark; the table's "
              "'*Resigned' marks attach to the lister lines).")],
           [holder("Mary Oldenburg", "mary-oldenburg")]),
])

spec("bethel", [
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Bethel Trustees of Public Funds", 3,
           [S("https://townofbethelvt.com/",
              "Town of Bethel, Trustees of Public Funds Annual "
              "Meeting minutes, September 10, 2026: 'Board Members "
              "Attending: Scott Putney, Chair; Yaroslav Stanchak; "
              "Rick Benson, Scribe' -- Putney and Stanchak sit as "
              "trustees alongside the already-recorded Eric Benson. "
              "The minutes also style Eric Benson as 'E. Benson' in "
              "one motion; same person, no separate record.")],
           [holder("Scott Putney", "scott-putney"),
            holder("Yaroslav Stanchak", "yaroslav-stanchak")]),
])

BRADFORD_TAX = "https://bradford-vt.us/"
spec("bradford", [
    office("collector-of-taxes", "Collector of Taxes",
           "Bradford Collector of Taxes", 1,
           [S(BRADFORD_TAX,
              "Town of Bradford, Tax Collection page (live): "
              "'Town Treasurer / Jessica Chase / Current Tax "
              "Collector' and 'Nikki Tomlinson / Delinquent Tax "
              "Collector' -- Chase, the sitting Town Treasurer "
              "(seated in batch 3), also holds the Collector of "
              "Taxes office; Tomlinson, the Town Clerk, is the "
              "Delinquent Tax Collector. (An earlier sweep "
              "research pass misread Tomlinson as the treasurer; "
              "the repo state and this page agree she is not.)")],
           [holder("Jessica Chase", "jessica-chase")]),
])

# ================================================================
# C3 -- Cabot, Cavendish
# ================================================================
spec("cabot", [
    office("lister", "Lister", "Town of Cabot Listers", 3,
           [S("https://cabotvt.us/listers/",
              "Town of Cabot, Listers page (live): 'Jeanne Johnson, "
              "Chair; Jacqueline Lumbra; Brittany Butler' are the "
              "town's three sitting listers. Butler is also the "
              "Town Clerk.")],
           [holder("Jeanne Johnson", "jeanne-johnson"),
            holder("Jacqueline Lumbra", "jacqueline-lumbra"),
            holder("Brittany Butler", "brittany-butler")]),
])

CAVENDISH_REPORT = "https://www.cavendishvt.com/boards-and-committees"
CAVENDISH_NOTE = ("Town of Cavendish, 2025 Annual Town Report, "
                  "'Elected Officials' (p. 4): ")
spec("cavendish", [
    office("library-trustee", "Library Trustee",
           "Cavendish Fletcher Community Library Trustees", 5,
           [S(CAVENDISH_REPORT, CAVENDISH_NOTE +
              "Library Trustees Claire Berkman (term to 2027), "
              "Sara Stowell (2028), David Gallagher (2029), and "
              "Ashley Newton (2030). The fifth seat (Christopher "
              "Saylor, term expired 2026) is unresolved and stays "
              "open.")],
           [holder("Claire Berkman", "claire-berkman"),
            holder("Sara Stowell", "sara-stowell"),
            holder("David Gallagher", "david-gallagher"),
            holder("Ashley Newton", "ashley-newton")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Cavendish Trustees of Public Funds", 3,
           [S(CAVENDISH_REPORT, CAVENDISH_NOTE +
              "Trustee of Public Funds Jane Pixley (term to 2027). "
              "The seat whose term expired in 2026 (Doris Eddy) "
              "stays open.")],
           [holder("Jane Pixley", "jane-pixley")]),
])

# ================================================================
# C4 -- Chelsea, Charlotte, Chester
# ================================================================
CHELSEA_RETURN = "https://www.chelseavt.org/voting-elections/"
CHELSEA_NOTE = ("Town of Chelsea, Official Return of Votes Entry, "
                "Annual Town Meeting, March 3, 2026 (certified): ")
spec("chelsea", [
    office("moderator", "Moderator", "Town of Chelsea Moderator", 1,
           [S(CHELSEA_RETURN, CHELSEA_NOTE +
              "Emily Marshia was elected Moderator on write-in "
              "votes, 36 of 52 cast. She is also the Town Clerk.")],
           [holder("Emily Marshia", "emily-marshia")]),
    office("lister", "Lister", "Town of Chelsea Listers", 3,
           [S(CHELSEA_RETURN, CHELSEA_NOTE +
              "Cindy Allen was elected lister on write-in votes, "
              "18 cast, in the contest that also re-elected Susan "
              "Elder (133).")],
           [holder("Cindy Allen", "cindy-allen")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Chelsea Trustees of Public Funds", 3,
           [S(CHELSEA_RETURN, CHELSEA_NOTE +
              "Edwin Coburn was elected Trustee of Public Funds "
              "with 131 votes.")],
           [holder("Edwin Coburn", "edwin-coburn")]),
])

CHARLOTTE_SB = ("https://charlottevt.org/vertical/sites/"
                "%7B797C5C63-8973-48DF-A5F9-82DC6FAE7EDF%7D/uploads/"
                "3-March_9_2026_DRAFT_SELECTBOARD__MEETING_MINUTES_.pdf")
spec("charlotte", [
    office("auditor", "Auditor", "Town of Charlotte Auditors", 3,
           [S(CHARLOTTE_SB,
              "Town of Charlotte, Auditors meeting minutes, "
              "April 23, 2026 (draft): Richard Mintzer and Alexa "
              "Lewis sit as auditors alongside Patrice Machavern, "
              "whose April 13, 2026 appointment is already recorded. "
              "The auditors' minutes of January 22, 2026 style the "
              "trio 'Elected Auditors'; Mintzer and Lewis are "
              "therefore recorded as elected. Mintzer had planned "
              "to step down around August 31, 2026; no later "
              "record was found, so he is minted on the April "
              "record, disclosed on issue #163.")],
           [holder("Richard Mintzer", "richard-mintzer"),
            holder("Alexa Lewis", "alexa-lewis")]),
])

spec("chester", [
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Chester Trustees of Public Funds", 3,
           [S("https://www.chestervt.gov/",
              "Town of Chester, Trustees of Public Funds meeting "
              "minutes, June 25, 2026: Shirley Barrett, Susan "
              "Willis, and Courtlandt Pennell sit as the town's "
              "three Trustees of Public Funds (the office is "
              "elected). An April 2, 2025 note spells the first "
              "name 'Barret' and the second 'Sue Willis'; the "
              "2026 minutes' forms govern.")],
           [holder("Shirley Barrett", "shirley-barrett"),
            holder("Susan Willis", "susan-willis"),
            holder("Courtlandt Pennell", "courtlandt-pennell")]),
])

# ================================================================
# C5 -- East Montpelier, Eden, Essex, Fair Haven, Fairfield,
#       Fairlee, Fletcher, Franklin
# ================================================================
spec("east-montpelier", [
    office("planning-commissioner", "Planning Commissioner",
           "Town of East Montpelier Planning Commission", 9,
           [S("https://eastmontpeliervt.org/boards-commision/"
              "planning-commission/",
              "Town of East Montpelier, Planning Commission page "
              "(live): the commission's nine members are Alexander "
              "Rob, Clarice Cutler, and Rebecca Schrader (already "
              "recorded) and Ben McCall, Glenn Weyant, Kim Watson, "
              "Erica Zimmerman, Zoe Christiansen, and Dillan Cabe. "
              "The commission is elected.")],
           [holder("Ben McCall", "ben-mccall"),
            holder("Glenn Weyant", "glenn-weyant"),
            holder("Kim Watson", "kim-watson"),
            holder("Erica Zimmerman", "erica-zimmerman"),
            holder("Zoe Christiansen", "zoe-christiansen"),
            holder("Dillan Cabe", "dillan-cabe")]),
])

EDEN_TM = ("https://www.edenvt.org/wp-content/uploads/2026/03/"
           "Town-Meeting-Minutes-2026.pdf")
EDEN_NOTE = ("Town of Eden, Annual Town Meeting minutes, March 3, "
             "2026 (marked Unapproved -- draft tier, disclosed; "
             "floor elections, each by one unanimous ballot cast): ")
spec("eden", [
    office("moderator", "Moderator", "Town of Eden Moderator", 1,
           [S(EDEN_TM, EDEN_NOTE +
              "H. Bruce Burnor was elected Moderator.")],
           [holder("H. Bruce Burnor", "h-bruce-burnor")]),
    office("auditor", "Auditor", "Town of Eden Auditors", 3,
           [S(EDEN_TM, EDEN_NOTE +
              "Julie Gates was elected auditor for a three-year "
              "term and Sandy Reen for a one-year term.")],
           [holder("Julie Gates", "julie-gates"),
            holder("Sandy Reen", "sandy-reen")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Eden Cemetery Commissioners", 5,
           [S(EDEN_TM, EDEN_NOTE +
              "Faye Cochran was elected Cemetery Commissioner for "
              "a five-year term.")],
           [holder("Faye Cochran", "faye-cochran")]),
    office("road-commissioner", "Road Commissioner",
           "Town of Eden Road Commissioner", 1,
           [S(EDEN_TM, EDEN_NOTE +
              "Ricky Morin was elected Road Commissioner.")],
           [holder("Ricky Morin", "ricky-morin")]),
    office("first-constable", "First Constable",
           "Town of Eden First Constable", 1,
           [S(EDEN_TM, EDEN_NOTE +
              "Bert Manning was elected First Constable.")],
           [holder("Bert Manning", "bert-manning")]),
    office("second-constable", "Second Constable",
           "Town of Eden Second Constable", 1,
           [S(EDEN_TM, EDEN_NOTE +
              "Dan Lathrop was elected Second Constable.")],
           [holder("Dan Lathrop", "dan-lathrop")]),
    office("agent-to-convey-real-estate", "Agent to Convey Real Estate",
           "Town of Eden Agent to Convey Real Estate", 1,
           [S(EDEN_TM, EDEN_NOTE +
              "Monique Morway was elected Agent to Convey Real "
              "Estate.")],
           [holder("Monique Morway", "monique-morway")]),
])

spec("essex", [
    office("town-treasurer", "Town Treasurer",
           "Town of Essex Town Treasurer", 1,
           [S("https://essexvt.gov/1578/Board-of-Abatement",
              "Town of Essex, Board of Abatement page (live): "
              "Tatsiana Bussiere is styled 'Town Clerk & "
              "Treasurer'. She already holds the appointed Town "
              "Clerk membership; the treasurer's office is "
              "appointed in Essex and she is recorded the same "
              "way.")],
           [holder("Tatsiana Bussiere", "tatsiana-bussiere",
                   how_seated="appointed")]),
])

spec("fair-haven", [
    office("auditor", "Auditor", "Town of Fair Haven Auditors", 3,
           [S("https://fairhavenvt.gov/",
              "Town of Fair Haven, Auditors page (live, modified "
              "March 23, 2026): Cindy Pritchard is the only auditor "
              "named; the other two seats stay open.")],
           [holder("Cindy Pritchard", "cindy-pritchard")]),
])

FAIRFIELD_REPORT = ("https://img1.wsimg.com/blobby/go/"
                    "bcfe7f6a-21a0-4365-83b2-ca876176b0e8/downloads/"
                    "101344a1-c178-43ad-bb8c-2b9f3c2de500/12.17.2025.pdf")
spec("fairfield", [
    office("moderator", "Moderator", "Town of Fairfield Moderator", 1,
           [S("https://www.fairfieldvt.org/",
              "Town of Fairfield, Annual Town Meeting minutes, "
              "March 3, 2026, item 1: Vanessa Kittell was nominated "
              "for Moderator and elected, one ballot cast by the "
              "clerk.")],
           [holder("Vanessa Kittell", "vanessa-kittell")]),
    office("auditor", "Auditor", "Town of Fairfield Auditors", 3,
           [S("https://www.fairfieldvt.org/",
              "Town of Fairfield, 2025 Annual Report, 'Elected Town "
              "Officers' table (p. 5): Auditors Mary Schreindorfer "
              "(term to 2027) and Diane Tracy (term to 2028); the "
              "minutes of March 3, 2026 (item 4.e) elect Jeanne "
              "Persons auditor for the term standing in 2026.")],
           [holder("Jeanne Persons", "jeanne-persons"),
            holder("Mary Schreindorfer", "mary-schreindorfer"),
            holder("Diane Tracy", "diane-tracy")]),
])

FAIRLEE_SB = ("https://fairleevt.gov/uploads/dm/7775/"
              "Selectboard_Meeting_Minutes_20260309_Final")
spec("fairlee", [
    office("auditor", "Auditor", "Town of Fairlee Auditors", 3,
           [S("https://fairleevt.gov/board-auditors",
              "Town of Fairlee, Board of Auditors page (live): "
              "Sandra Smith-Ordway (Chair) and Jane Chambers "
              "(already recorded) sit as auditors, one seat "
              "printed vacant."),
            S(FAIRLEE_SB,
              "Town of Fairlee, Selectboard minutes, March 9, "
              "2026: on motion, Deborah Stender was appointed "
              "auditor for one year, filling the vacancy.")],
           [holder("Sandra Smith-Ordway", "sandra-smith-ordway"),
            holder("Deborah Stender", "deborah-stender",
                   how_seated="appointed")]),
    office("budget-committee", "Budget Committee Member",
           "Town of Fairlee Budget Committee", 3,
           [S("https://fairleevt.gov/budget-committee",
              "Town of Fairlee, Budget Committee page (live): "
              "Richard Kenney and Dan Ludwig sit on the committee "
              "alongside Keri Gelenian (already recorded). The "
              "committee is elected at town meeting.")],
           [holder("Richard Kenney", "richard-kenney"),
            holder("Dan Ludwig", "dan-ludwig")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Fairlee Cemetery Commissioners", 5,
           [S("https://fairleevt.gov/cemetery-commission",
              "Town of Fairlee, Cemetery Commission page (live): "
              "Larry Farnham, Eric C. Sleeper, Lance V. Mills, "
              "and Chad Pierson sit as commissioners alongside "
              "Chaz Hinsley (already recorded).")],
           [holder("Larry Farnham", "larry-farnham"),
            holder("Eric C. Sleeper", "eric-c-sleeper"),
            holder("Lance Mills", "lance-mills"),
            holder("Chad Pierson", "chad-pierson")]),
    office("library-trustee", "Library Trustee",
           "Town of Fairlee Library Trustees", 5,
           [S("https://fairleevt.gov/library-trustees",
              "Town of Fairlee, Library Trustees page (live): "
              "Jennifer Johnson, Cyrie Lange, Stacey Dunham, and "
              "Richard Bibeau sit as trustees alongside Charlotte "
              "Williams (already recorded).")],
           [holder("Jennifer Johnson", "jennifer-johnson"),
            holder("Cyrie Lange", "cyrie-lange"),
            holder("Stacey Dunham", "stacey-dunham"),
            holder("Richard Bibeau", "richard-bibeau")]),
    office("lister", "Lister", "Town of Fairlee Listers", 3,
           [S("https://fairleevt.gov/listers",
              "Town of Fairlee, Listers page (live): 'Noel Walker, "
              "Chair' (the page prints the name with a diaeresis, "
              "No&euml;l) and Dan Ludwig sit as listers alongside "
              "Russ Collins (already recorded).")],
           [holder("Noël Walker", "noel-walker"),
            holder("Dan Ludwig", "dan-ludwig")]),
])

FLETCHER_RETURN = ("https://fletchervt.net/wp-content/uploads/2026/03/"
                   "DOC030326-03032026200740.pdf")
FLETCHER_NOTE = ("Town of Fletcher, Official Return of Votes, "
                 "Annual Town Meeting, March 3, 2026 (certified by "
                 "Town Clerk Aimee Tinker): ")
spec("fletcher", [
    office("moderator", "Moderator", "Town of Fletcher Moderator", 1,
           [S(FLETCHER_RETURN, FLETCHER_NOTE +
              "David Clark was elected Moderator, 227 votes.")],
           [holder("David Clark", "david-clark")]),
    office("town-clerk", "Town Clerk", "Town of Fletcher Town Clerk", 1,
           [S(FLETCHER_RETURN, FLETCHER_NOTE +
              "Karrie Sweet was elected to the combined ballot "
              "office 'TOWN CLERK/TREASURER', 233 votes; she is "
              "recorded on both of the town's separate clerk and "
              "treasurer posts.")],
           [holder("Karrie Sweet", "karrie-sweet")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Fletcher Town Treasurer", 1,
           [S(FLETCHER_RETURN, FLETCHER_NOTE +
              "Karrie Sweet was elected to the combined ballot "
              "office 'TOWN CLERK/TREASURER', 233 votes; she is "
              "recorded on both of the town's separate clerk and "
              "treasurer posts.")],
           [holder("Karrie Sweet", "karrie-sweet")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Fletcher Collector of Delinquent Taxes", 1,
           [S(FLETCHER_RETURN, FLETCHER_NOTE +
              "Fred Fletcher was elected Collector of Delinquent "
              "Taxes, 217 votes.")],
           [holder("Fred Fletcher", "fred-fletcher")]),
    office("lister", "Lister", "Town of Fletcher Listers", 3,
           [S(FLETCHER_RETURN, FLETCHER_NOTE +
              "Andrew Davis was elected lister for the two-year "
              "remainder of a term, 220 votes, and Charles Tinker "
              "for a three-year term, 220 votes.")],
           [holder("Andrew Davis", "andrew-davis"),
            holder("Charles Tinker", "charles-tinker")]),
    office("auditor", "Auditor", "Town of Fletcher Auditors", 3,
           [S(FLETCHER_RETURN, FLETCHER_NOTE +
              "Aimee Cardinal was elected auditor, 220 votes.")],
           [holder("Aimee Cardinal", "aimee-cardinal")]),
])

spec("franklin", [
    office("lister", "Lister", "Town of Franklin Listers", 3,
           [S("https://www.franklinvermont.org/boards-commissions-"
              "departments/listers",
              "Town of Franklin, Listers page (live): Jean Richard "
              "(term to 2029), Pierrette Bouchard (2028), and "
              "Howard Deuso (2027) sit as listers. All three are "
              "interim appointees: the annual meeting of March 3, "
              "2026 declined to elect successors after the three "
              "prior listers resigned effective that day, and the "
              "selectboard appointed the three named here.")],
           [holder("Jean Richard", "jean-richard",
                   how_seated="appointed"),
            holder("Pierrette Bouchard", "pierrette-bouchard",
                   how_seated="appointed"),
            holder("Howard Deuso", "howard-deuso",
                   how_seated="appointed")]),
])

# ================================================================
# C6 -- Georgia, Goshen, Grafton, Grand Isle, Greensboro,
#       Guilford, Granby, Halifax, Hardwick
# ================================================================
GEORGIA_RESULTS = ("https://www.townofgeorgia.com/elections-voting/"
                   "page/election-results")
GEORGIA_NOTE = ("Town of Georgia, official election results page, "
                "Annual Town Meeting, March 3, 2026: ")
spec("georgia", [
    office("moderator", "Moderator", "Town of Georgia Moderator", 1,
           [S(GEORGIA_RESULTS, GEORGIA_NOTE +
              "Carolyn Branagan was elected Moderator, 707 votes.")],
           [holder("Carolyn Branagan", "carolyn-branagan")]),
    office("town-clerk", "Town Clerk", "Town of Georgia Town Clerk", 1,
           [S(GEORGIA_RESULTS, GEORGIA_NOTE +
              "Cheryl Letourneau was elected Town Clerk, 712 votes, "
              "for a term ending March 2029. The results page "
              "misspells the surname 'Letorunaeu'; the form here is "
              "the town clerk block's own spelling.")],
           [holder("Cheryl Letourneau", "cheryl-letourneau")]),
    office("first-constable", "First Constable",
           "Town of Georgia First Constable", 1,
           [S(GEORGIA_RESULTS, GEORGIA_NOTE +
              "Kevin Webster was elected First Constable, 697 "
              "votes.")],
           [holder("Kevin Webster", "kevin-webster")]),
    office("second-constable", "Second Constable",
           "Town of Georgia Second Constable", 1,
           [S(GEORGIA_RESULTS, GEORGIA_NOTE +
              "Jamie Cota was elected Second Constable, 695 "
              "votes.")],
           [holder("Jamie Cota", "jamie-cota")]),
    office("library-trustee", "Library Trustee",
           "Georgia Public Library Trustees", 5,
           [S(GEORGIA_RESULTS, GEORGIA_NOTE +
              "the March 3, 2026 vote elected three trustees to "
              "one-year seats, among them Sarah Savich (392) and "
              "Brian Dunsmore (432)."),
            S("https://georgiapubliclibraryvt.org/staff--trustees.html",
              "Georgia Public Library, Staff & Trustees page "
              "(live): the sitting trustees include Brian Dunsmore "
              "(Chair), Sarah Savich (Vice Chair), and Kollene "
              "Caspers (Secretary, a continuing trustee). Dunsmore "
              "and Savich are resolved by both sources and "
              "Caspers by the roster; the third elected trustee, "
              "Ben Chiappinelli (555), does not appear on the "
              "current roster, and two roster trustees (Julia "
              "Harvey, Deborah Mann) have no published seating "
              "mechanism -- all three are held as a decision item "
              "on issue #163 and are not minted here.")],
           [holder("Brian Dunsmore", "brian-dunsmore"),
            holder("Sarah Savich", "sarah-savich"),
            holder("Kollene Caspers", "kollene-caspers")]),
])

spec("goshen", [
    office("second-constable", "Second Constable",
           "Town of Goshen Second Constable", 1,
           [S("https://goshenvt.org/constables/",
              "Town of Goshen, Constables page (live): David "
              "McKinnon is named Second Constable. The page does "
              "not state the seating mechanism; the entry follows "
              "the post's elected pattern and the omission is "
              "disclosed on issue #163.")],
           [holder("David McKinnon", "david-mckinnon")]),
])

spec("grafton", [
    office("town-clerk", "Town Clerk", "Town of Grafton Town Clerk", 1,
           [S("https://graftonvt.org/departments/town-clerktreasurer/",
              "Town of Grafton, Town Clerk/Treasurer page (live): "
              "'Clerk & Treasurer Kimberly Record'.")],
           [holder("Kimberly Record", "kimberly-record")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Grafton Town Treasurer", 1,
           [S("https://graftonvt.org/departments/town-clerktreasurer/",
              "Town of Grafton, Town Clerk/Treasurer page (live): "
              "'Clerk & Treasurer Kimberly Record'.")],
           [holder("Kimberly Record", "kimberly-record")]),
    office("lister", "Lister", "Town of Grafton Listers", 3,
           [S("https://graftonvt.org/boards-committees/listers/",
              "Town of Grafton, Listers page (live): 'Hardy "
              "Merrill, Lister, Chair' and Gail Ann Fisher sit as "
              "listers alongside Nancy Merrill (already recorded). "
              "The listers page spells the second name 'GailAnn "
              "Fisher'; the Public Funds page's 'Gail Ann Fisher' "
              "governs the single person record.")],
           [holder("Hardy Merrill", "hardy-merrill"),
            holder("Gail Ann Fisher", "gail-ann-fisher")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Grafton Trustees of Public Funds", 3,
           [S("https://graftonvt.org/departments/public-funds/",
              "Town of Grafton, Public Funds page (live): Gail "
              "Ann Fisher and Wendy Martin sit as Trustees of "
              "Public Funds alongside Kimberly Record (already "
              "recorded).")],
           [holder("Gail Ann Fisher", "gail-ann-fisher"),
            holder("Wendy Martin", "wendy-martin")]),
    office("auditor", "Auditor", "Town of Grafton Auditors", 3,
           [S("https://graftonvt.org/boards-committees/auditors/",
              "Town of Grafton, Auditors page (live, rendered "
              "read): the 'PRESENT BOARD OF AUDITORS' cards name "
              "Arlene Carey (already recorded), Heather Gregory, "
              "and Deborah Plummer, with no vacancy language.")],
           [holder("Heather Gregory", "heather-gregory"),
            holder("Deborah Plummer", "deborah-plummer")]),
])

spec("grand-isle", [
    office("moderator", "Moderator", "Town of Grand Isle Moderator", 1,
           [S("https://grandislevt.org/wp-content/uploads/2026/03/"
              "2026-Grand-Isle-Results-030326.pdf",
              "Town of Grand Isle, Official Return of Votes, "
              "March 3, 2026 (certified): Ronnie Bushway was "
              "elected Moderator, 367 votes. The return's "
              "'Ronnie' is the selectboard member Ron Bushway "
              "(diminutive) -- the same person record is reused. "
              "The lister contest on the same return named no "
              "candidate and produced only scattered write-ins, "
              "so that seat stays open.")],
           [holder("Ron Bushway", "ron-bushway")]),
])

GREENSBORO_RESULTS = "https://greensborovt.gov/town-election-results/"
GREENSBORO_NOTE = ("Town of Greensboro, official Town Meeting "
                   "election results page, March 3, 2026: ")
spec("greensboro", [
    office("moderator", "Moderator", "Town of Greensboro Moderator", 1,
           [S(GREENSBORO_RESULTS, GREENSBORO_NOTE +
              "Mavis MacNeil was elected Moderator, 153 votes.")],
           [holder("Mavis MacNeil", "mavis-macneil")]),
    office("town-clerk", "Town Clerk", "Town of Greensboro Town Clerk",
           1,
           [S(GREENSBORO_RESULTS, GREENSBORO_NOTE +
              "Kim Greaves was elected Town Clerk, 155 votes.")],
           [holder("Kim Greaves", "kim-greaves")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Greensboro Collector of Delinquent Taxes", 1,
           [S(GREENSBORO_RESULTS, GREENSBORO_NOTE +
              "Mike Cloutier was elected Collector of Delinquent "
              "Taxes, 165 votes.")],
           [holder("Mike Cloutier", "mike-cloutier")]),
    office("library-trustee", "Library Trustee",
           "Greensboro Free Library Trustees", 6,
           [S(GREENSBORO_RESULTS, GREENSBORO_NOTE +
              "Carol Reynolds (157) and Jan Terwiesch (147) were "
              "elected Library Trustees, completing the six-member "
              "board.")],
           [holder("Carol Reynolds", "carol-reynolds"),
            holder("Jan Terwiesch", "jan-terwiesch")]),
])

GUILFORD_TM = ("https://guilfordvt.gov/wp-content/uploads/2026/03/"
               "Town-Meeting-Minutes-2.28.26.pdf")
spec("guilford", [
    office("moderator", "Moderator", "Town of Guilford Moderator", 1,
           [S(GUILFORD_TM,
              "Town of Guilford, Annual Town Meeting minutes, "
              "February 28, 2026, Article 1: Rick Zamore presided "
              "as the elected Moderator.")],
           [holder("Rick Zamore", "rick-zamore")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Guilford Cemetery Commissioners", 5,
           [S(GUILFORD_TM,
              "Town of Guilford, Annual Town Meeting minutes, "
              "February 28, 2026, Article 4: Nancy Detra was "
              "elected Cemetery Commissioner for the five-year "
              "term standing in 2026 (the nomination is labeled "
              "with the office in the minutes).")],
           [holder("Nancy Detra", "nancy-detra")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Guilford Trustees of Public Funds", 5,
           [S(GUILFORD_TM,
              "Town of Guilford, Annual Town Meeting minutes, "
              "February 28, 2026, Article 4 (as amended) elects "
              "exactly four officers -- a Cemetery Commissioner "
              "(5-year), two Library Trustees (4-year and 3-year), "
              "and a Trustee of Public Funds (3-year) -- and names "
              "four nominees, elected by one voice vote ('All in "
              "Favor'). Three nominees are assigned in the minutes "
              "to the cemetery and library seats; the fourth, Elly "
              "Majonen, takes the only unassigned office, Trustee "
              "of Public Funds. 'Elly' is the diminutive of Ellen "
              "Majonen, the town's treasurer and delinquent tax "
              "collector -- her existing person record is reused. "
              "Minted elected with this "
              "elimination chain disclosed; see the sweep report "
              "on issue #163, which also flags that two library "
              "trustees from this same vote were recorded "
              "differently in an earlier batch.")],
           [holder("Ellen Majonen", "ellen-majonen")]),
])

spec("granby", [
    office("auditor", "Auditor", "Town of Granby Auditors", 3,
           [S("https://d7f1a76e-ba04-4548-a2ef-e736581ff60f.usrfiles."
              "com/ugd/d7f1a7_ffe3404c24574db4b06c8e02424d9627.pdf",
              "Town of Granby, Selectboard meeting agenda, "
              "February 24, 2026 (Town Clerk's report item): "
              "'Record the action of the board to appoint Mark "
              "Fulton as auditor to replace Shelly Houde who "
              "resigned.' Agenda-tier sourcing (the agenda records "
              "a prior board action; no minutes were located), "
              "disclosed on issue #163.")],
           [holder("Mark Fulton", "mark-fulton",
                   how_seated="appointed")]),
])

spec("halifax", [
    office("first-constable", "First Constable",
           "Town of Halifax First Constable", 1,
           [S("https://halifaxvt.com/draft-march-17-2026-selectboard-"
              "regular-meeting-minutes/",
              "Town of Halifax, Selectboard minutes, March 17, "
              "2026: on motion, Kyle Farnsworth was appointed First "
              "Constable 'with citation ticket responsibility', "
              "carried 4-0.")],
           [holder("Kyle Farnsworth", "kyle-farnsworth",
                   how_seated="appointed")]),
])

HARDWICK_TM = ("https://hardwickvt.gov/wp-content/uploads/2026/03/"
               "2026-Town-Meeting-minutes.pdf")
HARDWICK_NOTE = ("Town of Hardwick, Annual Town Meeting minutes, "
                 "March 3, 2026 (floor elections): ")
spec("hardwick", [
    office("moderator", "Moderator", "Town of Hardwick Moderator", 1,
           [S(HARDWICK_TM, HARDWICK_NOTE +
              "Article 1: Audrey Grant was elected Moderator.")],
           [holder("Audrey Grant", "audrey-grant")]),
    office("first-constable", "First Constable",
           "Town of Hardwick First Constable", 1,
           [S(HARDWICK_TM, HARDWICK_NOTE +
              "Lindsay O'Steen was elected First Constable.")],
           [holder("Lindsay O'Steen", "lindsay-osteen")]),
    office("second-constable", "Second Constable",
           "Town of Hardwick Second Constable", 1,
           [S(HARDWICK_TM, HARDWICK_NOTE +
              "Charlie Bartlett was elected Second Constable.")],
           [holder("Charlie Bartlett", "charlie-bartlett")]),
    office("town-agent", "Town Agent", "Town of Hardwick Town Agent", 1,
           [S(HARDWICK_TM, HARDWICK_NOTE +
              "Dave Shepard was elected Town Agent.")],
           [holder("Dave Shepard", "dave-shepard")]),
    office("surveyor-of-wood-bark-and-lumber",
           "Surveyor of Wood, Bark and Lumber",
           "Town of Hardwick Surveyor of Wood, Bark and Lumber", 1,
           [S(HARDWICK_TM, HARDWICK_NOTE +
              "Levi Chase was elected Surveyor of Wood, Bark and "
              "Lumber.")],
           [holder("Levi Chase", "levi-chase")]),
    office("tree-warden", "Tree Warden", "Town of Hardwick Tree Warden",
           1,
           [S(HARDWICK_TM, HARDWICK_NOTE +
              "Geoffrey Fehrs was elected Tree Warden, winning a "
              "hand count over Michael Deering.")],
           [holder("Geoffrey Fehrs", "geoffrey-fehrs")]),
    office("grand-juror", "Grand Juror", "Town of Hardwick Grand Juror",
           1,
           [S(HARDWICK_TM, HARDWICK_NOTE +
              "Eric Remick was elected Grand Juror. He is also the "
              "Selectboard Chair.")],
           [holder("Eric Remick", "eric-remick")]),
    office("library-trustee", "Library Trustee",
           "Jeudevine Memorial Library Trustees", 7,
           [S(HARDWICK_TM, HARDWICK_NOTE +
              "Beth McIntyre was elected Library Trustee for a "
              "three-year term and Myles Tandy for a one-year "
              "remainder. The minutes print 'Myles Tandy'; the "
              "Hardwick Electric Department page prints a 'Myles "
              "Kamisher-Koch' -- possibly the same person, but the "
              "records are NOT merged (identity rule); both "
              "records stand and the question is flagged on issue "
              "#163.")],
           [holder("Beth McIntyre", "beth-mcintyre"),
            holder("Myles Tandy", "myles-tandy")]),
    office("electric-commissioner", "Electric Commissioner",
           "Hardwick Electric Department Commissioners", 5,
           [S("https://hardwickelectric.com/board-of-commissioners/",
              "Hardwick Electric Department, Board of "
              "Commissioners page (live): Michael Ambrosino "
              "(Chair, term to 2027), Renaud Demers (2027), Jake "
              "Lester (2027) -- already recorded -- and Myles "
              "Kamisher-Koch (Vice Chair, term to June 30, 2029). "
              "The fifth seat stays open. Charter ch. 123 sec. 904 "
              "speaks of selectboard appointment effective July 1 "
              "while the post is modeled elected -- a pre-existing "
              "modeling question flagged on issue #163; this entry "
              "follows the roster presentation.")],
           [holder("Myles Kamisher-Koch", "myles-kamisher-koch")]),
])

# ================================================================
# C7 -- Jamaica, Johnson Village
# ================================================================
spec("jamaica", [
    office("lister", "Lister", "Town of Jamaica Listers", 3,
           [S("https://www.jamaicavermont.org/wp-content/uploads/"
              "2026/06/GrievanceWarning2026.pdf",
              "Town of Jamaica, Listers' Grievance Warning, "
              "posted June 24, 2026, headed 'KAREN AMEDEN / PAT "
              "MEULEMANS / APRIL GREEN', and the Listers' "
              "Grievance Appeals minutes of July 8, 2026, which "
              "present Pat Meulemans sitting as a lister: "
              "Meulemans fills the third lister seat. The 2026 "
              "documents print 'Pat Meulemans' (not 'Patricia').")],
           [holder("Pat Meulemans", "pat-meulemans")]),
])

JOHNSON_MINUTES = ("https://villageofjohnson.com/wp-content/uploads/"
                   "2026/05/Johnson-Village-Trustee-Board-Minutes-"
                   "5-11-26.pdf")
JOHNSON_NOTE = ("Village of Johnson, Trustee Board minutes, "
                "May 11, 2026, item 12: 'Appoint Ashley Isabell "
                "as Village Treasurer and Tax Collector -- Will "
                "moved to appoint Ashley Isabell as village "
                "treasurer and tax collector effective May 28, "
                "2026, Ellis seconded and the motion was passed.' "
                "The trustees' minutes of June 17, 2026 introduce "
                "'Ashley Isabell, the new village treasurer' in "
                "corroboration. ")
spec("johnson", [
    office("tax-collector", "Tax Collector",
           "Village of Johnson Tax Collector", 1,
           [S(JOHNSON_MINUTES, JOHNSON_NOTE +
              "Isabell takes the Tax Collector office under the "
              "same appointment.")],
           [holder("Ashley Isabell", "ashley-isabell",
                   how_seated="appointed")]),
    office("village-treasurer", "Village Treasurer",
           "Village of Johnson Village Treasurer", 1,
           [S(JOHNSON_MINUTES, JOHNSON_NOTE +
              "Isabell succeeds Rosemary Audibert as Village "
              "Treasurer; Audibert's treasurer membership is "
              "ended in the same sweep (she remains Village "
              "Clerk).")],
           [holder("Ashley Isabell", "ashley-isabell",
                   how_seated="appointed")]),
])

# ================================================================
# C9 -- Moretown, Newbury (town), Newfane
# ================================================================
spec("moretown", [
    office("library-trustee", "Library Trustee",
           "Moretown Memorial Library Trustees", 5,
           [S("https://www.moretownvt.org/wp-content/uploads/"
              "minutes-agendas-newsletters/libminutes_2026-03-17.pdf",
              "Moretown Memorial Library, Board of Trustees "
              "minutes, March 17, 2026: 'Pam Barnes and April Shaw "
              "were elected to one-year terms. Sybil Schlesinger "
              "was elected to a 3-year term.' Barnes and "
              "Schlesinger already hold memberships (renewals); "
              "Shaw, who also acts as trustee/chair in the "
              "minutes of May 12, 2026, is the one new holder, "
              "completing the five-member board.")],
           [holder("April Shaw", "april-shaw")]),
])

spec("newbury-48175", [
    office("moderator", "Moderator", "Town of Newbury Moderator", 1,
           [S("https://www.newburyvt.org/",
              "Town of Newbury, Annual Town Meeting Minutes, "
              "March 3, 2026, Article 1: Jan Cole was nominated by "
              "Marvin Harrison and 'unanimously elected by voice "
              "vote' as Moderator. The minutes print 'Jan Cole'; "
              "the town's 2025 Annual Report officers table prints "
              "'Janet Cole' for the same office, and the fuller "
              "form is used for the person record.")],
           [holder("Janet Cole", "janet-cole")]),
])

NEWFANE_RESULTS = "https://newfanevt.com/"
spec("newfane-48400", [
    office("moderator", "Moderator", "Town of Newfane Moderator", 1,
           [S(NEWFANE_RESULTS,
              "Town of Newfane, official 2026 Town Meeting "
              "Election Results page: Kim Friedman was elected "
              "Moderator, 133 votes.")],
           [holder("Kim Friedman", "kim-friedman")]),
    office("lister", "Lister", "Town of Newfane Listers", 3,
           [S(NEWFANE_RESULTS,
              "Town of Newfane, official 2026 Town Meeting "
              "Election Results page: Doris Knechtel was elected "
              "lister, 131 votes, completing the three-member "
              "board.")],
           [holder("Doris Knechtel", "doris-knechtel")]),
])

# ================================================================
# C10 -- Norwich, Old Bennington, Orwell, Pittsfield, Pittsford,
#        Plainfield, Pomfret, Proctor, Putney
# ================================================================
NORWICH_LISTERS = "https://norwich.vt.us/"
spec("norwich", [
    office("lister", "Lister", "Town of Norwich Listers", 3,
           [S(NORWICH_LISTERS,
              "Town of Norwich, Board of Listers page (live): "
              "Ernie Ciccotelli (term to 2027) and Pamela Smith "
              "(term to 2027) sit as listers alongside Chair "
              "('Ernie' is the diminutive of Ernest Ciccotelli, "
              "whose existing person record is reused) "
              "Cheryl Lindberg (already recorded); both act in "
              "the listers' minutes of July 30, 2026."),
            S(NORWICH_LISTERS,
              "Seating-basis disclosure for Smith: the town's "
              "pre-election candidate-forms page described her "
              "seat as 'Lister (2 year unexpired term - Smith, "
              "appointed)' -- she first held the seat by "
              "appointment going into March 2026, and no election "
              "result naming her was located; she is recorded as "
              "appointed on that documented basis, still "
              "presented as a sitting lister on the town's live "
              "listers page.")],
           [holder("Ernest Ciccotelli", "ernest-ciccotelli"),
            holder("Pamela T. Smith", "pamela-t-smith",
                   how_seated="appointed")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Norwich Trustees of Public Funds", 3,
           [S("https://norwich.vt.us/wp-content/uploads/2026/03/"
              "2026-03-25-DRAFT-Selectboard-Minutes.pdf",
              "Town of Norwich, Selectboard minutes, March 25, "
              "2026 (file labeled DRAFT, disclosed): Megan "
              "Anderson was appointed Trustee of Public Funds for "
              "an interim term expiring March 2, 2027, by "
              "unanimous vote.")],
           [holder("Megan Anderson", "megan-anderson",
                   how_seated="appointed")]),
])

spec("old-bennington", [
    office("moderator", "Moderator",
           "Village of Old Bennington Moderator", 1,
           [S("https://oldbennington.org/",
              "Village of Old Bennington, Annual Village Meeting "
              "Minutes, May 12, 2026 (read from the village site's "
              "Board of Trustees page): the officials-present "
              "list names 'Moderator Pat Winburn', and the "
              "election item (p. 8) records the four incumbent "
              "officers unanimously re-elected to one-year terms, "
              "the Moderator nominated by Galen Jones and "
              "seconded by E.W.")],
           [holder("Pat Winburn", "pat-winburn")]),
])

spec("orwell", [
    office("lister", "Lister", "Town of Orwell Listers", 3,
           [S("https://townoforwellvt.org/wp-content/uploads/2026/"
              "04/sb-min-04132026.pdf",
              "Town of Orwell, Selectboard minutes, April 13, "
              "2026 (scanned, marked NOT APPROVED -- draft tier, "
              "disclosed), p. 2: Kay Firth-Butterfield was "
              "appointed lister for a one-year term until the "
              "next election, passed 5 yes, 0 no. The second "
              "open lister seat stays unresolved: the live "
              "Listers page still shows the retiring holders and "
              "fails the currency check.")],
           [holder("Kay Firth-Butterfield", "kay-firth-butterfield",
                   how_seated="appointed")]),
])

spec("pittsfield", [
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Pittsfield Trustees of Public Funds", 3,
           [S("https://pittsfieldvt.com/elected-officials.html",
              "Town of Pittsfield, Elected Officials page "
              "(live): Sandy Begin and Mark Stugart sit as "
              "Trustees of Public Funds alongside Henry Hotchkiss "
              "(already recorded, term to 2029). The page's year "
              "column could not be paired to the three names "
              "reliably, so no individual terms are recorded.")],
           [holder("Sandy Begin", "sandy-begin"),
            holder("Mark Stugart", "mark-stugart")]),
])

spec("pittsford", [
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Pittsford Trustees of Public Funds", 3,
           [S("https://www.pittsfordvermont.com/wp-content/uploads/"
              "2026/03/FY2025-Annual-Report-Final.pdf",
              "Town of Pittsford, FY2025 Annual Report, 'ELECTED "
              "TOWN OFFICERS' table (p. 56): Trustees of Public "
              "Funds Thomas Hooker (term to 2027) and Charles "
              "'Butch' Shaw (term to 2028); the third trustee, "
              "Helen McKinlay (term expired 2026), is the seat "
              "Dolores Gecha won and already holds. Continuing "
              "terms; neither seat stood in 2026.")],
           [holder("Tom Hooker", "tom-hooker"),
            holder("Charles Shaw", "charles-shaw")]),
])

PLAINFIELD_ORG = ("https://www.plainfieldvt.gov/uploads/8/1/0/6/"
                  "81063668/2026-03-09_selectboard_organizational_"
                  "meeting_minutes_-_approved.pdf")
spec("plainfield", [
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Plainfield Cemetery Commissioners", 5,
           [S(PLAINFIELD_ORG,
              "Town of Plainfield, Cemetery Commission "
              "organizational minutes, March 9, 2026: the "
              "selectboard appointed Andy Hebert (seat 2026-2031), "
              "Judy Hammack (2025-2030), and Mary Morton "
              "(2025-2029), each 5-0, and noted 'for the record' "
              "Lydia Vitale (elected 2025, term to 2027) and "
              "Nancy Ellen (elected 2025, term to 2028). The "
              "commission is FIVE members; the post's seat count "
              "is corrected from 3 to 5 in this sweep, disclosed "
              "on issue #163.")],
           [holder("Andy Hebert", "andy-hebert",
                   how_seated="appointed"),
            holder("Judy Hammack", "judy-hammack",
                   how_seated="appointed"),
            holder("Mary Morton", "mary-morton",
                   how_seated="appointed"),
            holder("Lydia Vitale", "lydia-vitale"),
            holder("Nancy Ellen", "nancy-ellen")]),
    office("lister", "Lister", "Town of Plainfield Listers", 3,
           [S("https://www.plainfieldvt.gov/listers--reappraisal.html",
              "Town of Plainfield, Listers page (live): the "
              "October 5, 2026 Annual Lister's Meeting notice "
              "names Sandy Ross, Kayle Hope, and Jeffrey Slaton "
              "(already recorded) as the town's listers. Hope's "
              "page biography states she was 'elected in 2024'; "
              "Ross's basis is the page presentation.")],
           [holder("Sandy Ross", "sandy-ross"),
            holder("Kayle Hope", "kayle-hope")]),
])

spec("pomfret", [
    office("library-trustee", "Library Trustee",
           "Abbott Memorial Library Trustees", 6,
           [S("https://www.Pomfretvt.us/files/4817/7428/0217/"
              "03_18_2026_draft_minutes_v2.pdf",
              "Town of Pomfret, Selectboard minutes, March 18, "
              "2026 (draft, disclosed): Jan Salstrom and Katie "
              "Brickner were appointed Library Trustees until the "
              "next annual town meeting.")],
           [holder("Jan Salstrom", "jan-salstrom",
                   how_seated="appointed"),
            holder("Katie Brickner", "katie-brickner",
                   how_seated="appointed")]),
])

spec("proctor", [
    office("moderator", "Moderator", "Town of Proctor Moderator", 1,
           [S("https://proctorvermont.com/",
              "Town of Proctor, town homepage, '2026 Election "
              "Results' posting dated March 3, 2026 (rendered "
              "read; the homepage refuses direct fetches): "
              "'Moderator: Andrew Maass'.")],
           [holder("Andrew Maass", "andrew-maass")]),
])

spec("putney", [
    office("library-trustee", "Library Trustee",
           "Putney Public Library Trustees", 9,
           [S("https://putneylibrary.org/about-the-library/"
              "library-board-governance/",
              "Putney Public Library, Board page (live): the "
              "nine current trustees include Susan McMahon, Jim "
              "Olivier, Ben Lord, and Penny Weingarten alongside "
              "the five already recorded. The office is "
              "floor-elected at town meeting.")],
           [holder("Susan McMahon", "susan-mcmahon"),
            holder("Jim Olivier", "jim-olivier"),
            holder("Ben Lord", "ben-lord"),
            holder("Penny Weingarten", "penny-weingarten")]),
])

# ================================================================
# C11 -- Reading, Randolph, Richford, Richmond, Royalton, Salisbury
# ================================================================
READING_TABLE = ("https://readingvt.govoffice.com/vertical/sites/"
                 "%7B29D76170-2CBD-4DB0-A089-6F91F5BED766%7D/uploads/"
                 "20260407131936802.pdf")
READING_NOTE = ("Town of Reading, 'Elected Officials March 2026' "
                "table (the town's official post-meeting officers "
                "table): ")
spec("reading", [
    office("moderator", "Moderator", "Town of Reading Moderator", 1,
           [S(READING_TABLE, READING_NOTE +
              "Moderator Rayna Bishop, term to 2027, elected.")],
           [holder("Rayna Bishop", "rayna-bishop")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Reading Trustees of Public Funds", 3,
           [S(READING_TABLE, READING_NOTE +
              "Trustees of Public Funds are Gary Vittum (2027, "
              "already recorded), an open seat (2028), and Curt "
              "Allen (2029). Allen is minted elected.")],
           [holder("Curt Allen", "curt-allen")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Reading Cemetery Commissioners", 3,
           [S(READING_TABLE, READING_NOTE +
              "Cemetery Commissioners are Adam Kozlowski (2027, "
              "already recorded), Susan Goodhouse (2028), and an "
              "open seat (2029). Goodhouse is minted elected.")],
           [holder("Susan Goodhouse", "susan-goodhouse")]),
    office("library-trustee", "Library Trustee",
           "Reading Public Library Trustees", 5,
           [S(READING_TABLE, READING_NOTE +
              "the library table's legend reads '( R) = Resigned "
              "( A) = Appointed': Libbet Downs (2026), Vanessa "
              "Maxham - R (2027), Rich Grogan - A (2027), Janet "
              "Malcolm - R (2028), Kristen Hurd - A (2028), "
              "Heather Evans (2029, already recorded), Bill "
              "Bakker (2030). Grogan and Hurd are the appointed "
              "successors to the resigned Maxham and Malcolm "
              "seats (the departed members' memberships are ended "
              "in this sweep, disclosed); Bakker is minted "
              "elected to the 2030 seat. Downs's expired 2026 "
              "seat has no published successor and stays open.")],
           [holder("Bill Bakker", "bill-bakker"),
            holder("Rich Grogan", "rich-grogan",
                   how_seated="appointed"),
            holder("Kristen Hurd", "kristen-hurd",
                   how_seated="appointed")]),
    office("town-clerk", "Town Clerk", "Town of Reading Town Clerk", 1,
           [S(READING_TABLE, READING_NOTE +
              "the same table lists the Town Clerk and Town "
              "Treasurer under 'Town of Reading Hired Positions': "
              "Calista Brennan holds both offices as an appointee "
              "(the town converted both offices to appointed "
              "under 17 V.S.A. sections 2651e/2651f).")],
           [holder("Calista Brennan", "calista-brennan",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer",
           "Town of Reading Town Treasurer", 1,
           [S(READING_TABLE, READING_NOTE +
              "Calista Brennan holds the Town Treasurer office "
              "as an appointee under 'Town of Reading Hired "
              "Positions' (see the clerk entry).")],
           [holder("Calista Brennan", "calista-brennan",
                   how_seated="appointed")]),
])

RANDOLPH_SITE = "https://www.randolphtownvt.org/"
spec("randolph", [
    office("budget-committee", "Budget Committee Member",
           "Town of Randolph Budget Committee", 5,
           [S(RANDOLPH_SITE,
              "Town of Randolph, Budget Committee page (live; "
              "read via browser -- the site serves an "
              "interstitial to direct fetches): the page lists "
              "all five members verbatim -- Christine Settles "
              "(term to 2029), Scott Frew (2028), Tamara Morgan "
              "(2027), Ken Hafner (Chair, 2027), and Scott Berkey "
              "(2027) -- and states members are elected annually "
              "at Town Meeting (vacancies by selectboard "
              "appointment).")],
           [holder("Christine Settles", "christine-settles"),
            holder("Scott Frew", "scott-frew"),
            holder("Tamara Morgan", "tamara-morgan"),
            holder("Ken Hafner", "ken-hafner"),
            holder("Scott Berkey", "scott-berkey")]),
    office("lister", "Lister", "Town of Randolph Listers", 3,
           [S(RANDOLPH_SITE,
              "Town of Randolph, Listers page (live; browser "
              "read): the Staff section names Dennis Brown "
              "(Chair, term to 2028) and Mimi Burstein (2027, "
              "already recorded); corroborated by the listers' "
              "minutes of July 30, 2026. The third (2026) lister "
              "seat stays open -- the page names only Brown and "
              "Burstein.")],
           [holder("Dennis Brown", "dennis-brown")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Randolph Trustees of Public Funds", 3,
           [S(RANDOLPH_SITE,
              "Town of Randolph, Trustees of Public Funds "
              "minutes, March 11, 2026, attendance line: 'Board "
              "Members Present: Joyce Mazzucco, Cliff Rankin, "
              "and Bruce Butler' -- Butler completes the "
              "three-member board alongside the two already "
              "recorded.")],
           [holder("Bruce Butler", "bruce-butler")]),
])

spec("richford", [
    office("first-constable", "First Constable",
           "Town of Richford First Constable", 1,
           [S("https://www.richfordvt.org/municipal-directory.html",
              "Town of Richford, Municipal Directory (live): "
              "'Town Constable / Jeremy Paquette'.")],
           [holder("Jeremy Paquette", "jeremy-paquette")]),
])

spec("richmond", [
    office("constable", "Constable", "Town of Richmond Constable", 1,
           [S("https://www.richmondvt.gov/boards-meetings/"
              "all-committee-board-members",
              "Town of Richmond, 'All Committee & Board Members' "
              "roster (live): Andy Squires is listed as Constable, "
              "Type: Elected, 2026-2027.")],
           [holder("Andy Squires", "andy-squires")]),
    office("moderator", "Moderator", "Town of Richmond Moderator", 1,
           [S("https://www.richmondvt.gov/boards-meetings/"
              "all-committee-board-members",
              "Town of Richmond, 'All Committee & Board Members' "
              "roster (live): Clint Buxton is listed as "
              "Moderator, Type: Elected, 2026-2027. The roster "
              "prints 'Clint'; earlier batch research used "
              "'Clinton Buxton' -- the roster form governs.")],
           [holder("Clint Buxton", "clint-buxton")]),
])

spec("royalton", [
    office("first-constable", "First Constable",
           "Town of Royalton First Constable", 1,
           [S("https://royaltonvt.gov",
              "Town of Royalton, Selectboard minutes, April 28, "
              "2026: 'Tim moved to appoint Todd Balentine as "
              "First Constable... Motion passed unanimously.' "
              "The appointing minutes' spelling 'Balentine' "
              "governs (the minutes of September 22, 2026 print "
              "'Ballentine' twice).")],
           [holder("Todd Balentine", "todd-balentine",
                   how_seated="appointed")]),
])

spec("salisbury", [
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Salisbury Collector of Delinquent Taxes", 1,
           [S("https://www.townofsalisbury.org",
              "Town of Salisbury, Selectboard minutes, August 4, "
              "2026 (approved; browser read of the town's posted "
              "minutes): the Correspondence item styles her "
              "'Mindy Goodrich, Delinquent Tax Collector'. The "
              "office is elective by Australian ballot under the "
              "town's 2026 Warning.")],
           [holder("Mindy Goodrich", "mindy-goodrich")]),
    office("lister", "Lister", "Town of Salisbury Listers", 3,
           [S("https://www.townofsalisbury.org",
              "Town of Salisbury, Selectboard minutes, March 10, "
              "2026 (approved; browser read): 'appoint Brenda "
              "Burchard as interim lister until May 1st... passed "
              "unanimously: 5/0'; the minutes of May 12, 2026 "
              "still report 'Lister - Brenda Burchard', acting "
              "past the May 1 lapse. Minted appointed with the "
              "full chain and the lapse disclosed on issue #163. "
              "The other two lister seats stay open.")],
           [holder("Brenda Burchard", "brenda-burchard",
                   how_seated="appointed")]),
])

# ================================================================
# C12 -- Shaftsbury, Shrewsbury, Shoreham, Stamford, Starksboro,
#        Sheffield
# ================================================================
SHAFTSBURY_RESULTS = "https://shaftsburyvt.gov"
spec("shaftsbury", [
    office("first-constable", "First Constable",
           "Town of Shaftsbury First Constable", 1,
           [S(SHAFTSBURY_RESULTS,
              "Town of Shaftsbury, certified ballot results, "
              "March 3, 2026 (attested March 4, 2026): Robert "
              "Perry was elected First Constable, 329 votes; "
              "corroborated by the town's live constables page "
              "(term to 2027).")],
           [holder("Robert Perry", "robert-perry")]),
    office("second-constable", "Second Constable",
           "Town of Shaftsbury Second Constable", 1,
           [S(SHAFTSBURY_RESULTS,
              "Town of Shaftsbury, certified ballot results, "
              "March 3, 2026 (attested March 4, 2026): Francis "
              "Buck was elected Second Constable (the only named "
              "candidate; the PDF's printed total line for the "
              "contest is internally inconsistent -- the town's "
              "arithmetic slip, disclosed); corroborated by the "
              "town's live constables page (term to 2027).")],
           [holder("Francis Buck", "francis-buck")]),
])

spec("shrewsbury", [
    office("first-constable", "First Constable",
           "Town of Shrewsbury First Constable", 1,
           [S("https://shrewsburyvt.org",
              "Town of Shrewsbury, Selectboard organizational "
              "minutes, March 4, 2026: on motion, Robert Littmann "
              "was appointed First Constable (the ballot contest "
              "had failed on write-ins only).")],
           [holder("Robert Littmann", "robert-littmann",
                   how_seated="appointed")]),
])

SHOREHAM_AUD = "https://shorehamvt.us"
spec("shoreham", [
    office("auditor", "Auditor", "Town of Shoreham Auditors", 3,
           [S(SHOREHAM_AUD,
              "Town of Shoreham, Auditors page (live, headed "
              "'Elected Auditors'): the three current auditors "
              "are Tamra Hawley-House, Karen Jarboe-Singletary, "
              "and Michelle Treadway. Mapping adjudication "
              "(disclosed on issue #163): Hawley-House and "
              "Jarboe-Singletary are recorded elected on the "
              "page's presentation -- they fill the second open "
              "seat and the seat of Maureen Gour, who no longer "
              "appears on the page (her membership is ended in "
              "this sweep; no election or appointment record for "
              "either woman appears in the selectboard minutes "
              "January-September 2026)."),
            S(SHOREHAM_AUD,
              "Town of Shoreham, Selectboard minutes, March 11, "
              "2026 (repeated March 25, 2026): on motion, "
              "Michelle Treadway was appointed to fill a vacant "
              "auditor seat for 2026 until the March 2027 "
              "elections.")],
           [holder("Tamra Hawley-House", "tamra-hawley-house"),
            holder("Karen Jarboe-Singletary",
                   "karen-jarboe-singletary"),
            holder("Michelle Treadway", "michelle-treadway",
                   how_seated="appointed")]),
    office("planning-commissioner", "Planning Commissioner",
           "Town of Shoreham Planning Commission", 7,
           [S(SHOREHAM_AUD,
              "Town of Shoreham, Planning Commission page "
              "(live): the commission's seven current members "
              "include Heather Stafford, Linda Larrabee, and "
              "Kevin Fox alongside the four already recorded. "
              "The commission is elected; no per-person terms "
              "are published.")],
           [holder("Heather Stafford", "heather-stafford"),
            holder("Linda Larrabee", "linda-larrabee"),
            holder("Kevin Fox", "kevin-fox")]),
])

spec("stamford", [
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Stamford Cemetery Commissioners", 3,
           [S("https://stamfordvt.net",
              "Town of Stamford, Cemetery Commission page "
              "(live): 'current Cemetery Commission members "
              "serving are: David McKay / Luke McKay / Sheila "
              "Lawrence'. Luke McKay's presence matches his "
              "March 3, 2026 election, proving post-election "
              "currency.")],
           [holder("David McKay", "david-mckay"),
            holder("Sheila Lawrence", "sheila-lawrence")]),
    office("library-trustee", "Library Trustee",
           "Stamford Community Library Trustees", 5,
           [S("https://stamfordvt.net",
              "Town of Stamford, joint Selectboard/School/"
              "Library minutes, May 5, 2026 (UNAPPROVED -- "
              "draft tier, disclosed): the attendance line names "
              "Library Trustees Caroline Burch (Chair), Amy "
              "Johns, Tyna Senecal, and Linda Rodovick. The "
              "fifth seat stays unresolved: the library page "
              "lists Victoria Jefferies as a trustee, but the "
              "May 5 minutes place her under Visitors.")],
           [holder("Caroline Burch", "caroline-burch"),
            holder("Amy Johns", "amy-johns"),
            holder("Tyna Senecal", "tyna-senecal"),
            holder("Linda Rodovick", "linda-rodovick")]),
])

spec("starksboro", [
    office("planning-commissioner", "Planning Commissioner",
           "Town of Starksboro Planning Commission", 7,
           [S("https://starksborovt.org",
              "Town of Starksboro, Planning Commission minutes, "
              "September 3, 2026 (approved): members present "
              "include Dennis Casey (Chair), Luke McCarthy, "
              "David Schmidt, and Dan Kuzio, alongside Dan "
              "Nugent (already recorded, absent that day). Two "
              "of the seven seats are named nowhere and stay "
              "open.")],
           [holder("Dennis Casey", "dennis-casey"),
            holder("Luke McCarthy", "luke-mccarthy"),
            holder("David Schmidt", "david-schmidt"),
            holder("Dan Kuzio", "dan-kuzio")]),
])

spec("sheffield", [
    office("planning-commissioner", "Planning Commissioner",
           "Town of Sheffield Planning Commission", 5,
           [S("https://sheffieldvt.org",
              "Town of Sheffield, Planning Commission minutes, "
              "April 15, 2026: Keith Ballek (attendee) and Brian "
              "'Biff' Mahoney (absent member) sit on the "
              "commission six weeks after the March 2026 annual "
              "meeting; their seats stood in 2026 and the "
              "commission is elected per the 2025 Town Report "
              "officers table. Minted elected on continuity "
              "presentation, mechanism unstated, disclosed on "
              "issue #163.")],
           [holder("Keith Ballek", "keith-ballek"),
            holder("Brian Mahoney", "brian-mahoney")]),
])

# ================================================================
# C13 -- Strafford, Sutton, Swanton (town), Tinmouth, Vernon,
#        Stockbridge
# ================================================================
STRAFFORD_REPORT = "https://www.straffordvt.org/"
STRAFFORD_NOTE = ("Town of Strafford, 2024 Annual Town Report, "
                  "officers table (p. 3) -- term-continuity: each "
                  "term below runs to March 2027, past the March "
                  "2026 meeting: ")
spec("strafford", [
    office("lister", "Lister", "Town of Strafford Listers", 3,
           [S(STRAFFORD_REPORT, STRAFFORD_NOTE +
              "Lister Tom Jacobs. (The seats of the other two "
              "listers named in research could not be verified "
              "to the same standard and stay open.)")],
           [holder("Tom Jacobs", "tom-jacobs")]),
    office("auditor", "Auditor", "Town of Strafford Auditors", 3,
           [S(STRAFFORD_REPORT, STRAFFORD_NOTE +
              "Auditor Nellie Pennington.")],
           [holder("Nellie Pennington", "nellie-pennington")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Strafford Trustees of Public Funds", 3,
           [S(STRAFFORD_REPORT, STRAFFORD_NOTE +
              "Trustee of Public Funds Therese Linehan.")],
           [holder("Therese Linehan", "therese-linehan")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Strafford Cemetery Commissioners", 5,
           [S(STRAFFORD_REPORT, STRAFFORD_NOTE +
              "Cemetery Commissioners David Harris and Andrew "
              "Behrens, both corroborated on the town's current "
              "board pages.")],
           [holder("David Harris", "david-harris"),
            holder("Andrew Behrens", "andrew-behrens")]),
])

spec("sutton", [
    office("auditor", "Auditor", "Town of Sutton Auditors", 3,
           [S("https://www.suttonvt.org/government",
              "Town of Sutton, Government page (live): "
              "'Auditors: Danielle Fortin - 2027 / Melanie "
              "Miller-Hanson - 2028 / Elaine Bandy - 2029' -- "
              "Bandy is already recorded; Fortin and "
              "Miller-Hanson complete the board.")],
           [holder("Danielle Fortin", "danielle-fortin"),
            holder("Melanie Miller-Hanson",
                   "melanie-miller-hanson")]),
])

SWANTON_MINUTES = ("https://www.swantonvt.gov/fileadmin/files/town/"
                   "Selectboard/Meetings/2026/03/2026_0304_SLB_"
                   "Organizational_Meeting_Approved_Minutes.pdf")
SWANTON_NOTE = ("Town of Swanton, official 2026 election results "
                "memorandum appended to the approved Selectboard "
                "organizational minutes of March 4, 2026: ")
spec("swanton-71725", [
    office("moderator", "Moderator", "Town of Swanton Moderator", 1,
           [S(SWANTON_MINUTES, SWANTON_NOTE +
              "Brian K. Savage was elected Moderator, 868 "
              "votes.")],
           [holder("Brian K. Savage", "brian-k-savage")]),
    office("lister", "Lister", "Town of Swanton Listers", 3,
           [S(SWANTON_MINUTES, SWANTON_NOTE +
              "Amy Giroux was elected lister, 859 votes.")],
           [holder("Amy Giroux", "amy-giroux")]),
    office("auditor", "Auditor", "Town of Swanton Auditors", 3,
           [S(SWANTON_MINUTES, SWANTON_NOTE +
              "Amy Giroux was elected auditor, 814 votes.")],
           [holder("Amy Giroux", "amy-giroux")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Swanton Collector of Delinquent Taxes", 1,
           [S(SWANTON_MINUTES, SWANTON_NOTE +
              "Betty L. Cheney was elected Collector of "
              "Delinquent Taxes, 881 votes.")],
           [holder("Betty L. Cheney", "betty-l-cheney")]),
    office("library-trustee", "Library Trustee",
           "Swanton Public Library Trustees", 5,
           [S(SWANTON_MINUTES, SWANTON_NOTE +
              "Rebecca Rupp was elected Library Trustee, 856 "
              "votes, completing the five-member board.")],
           [holder("Rebecca Rupp", "rebecca-rupp")]),
])

TINMOUTH_CONTACTS = "https://tinmouthvt.gov/town-contacts"
spec("tinmouth", [
    office("auditor", "Auditor", "Town of Tinmouth Auditors", 3,
           [S(TINMOUTH_CONTACTS,
              "Town of Tinmouth, Town Contacts page (live, "
              "post-election terms): Auditor Ann Czar (term to "
              "2029) completes the board. The page prints 'Cat "
              "Yoder' for the tax collector; the 2025 Town Report "
              "gives 'Catherine Yoder', used as the canonical "
              "form.")],
           [holder("Ann Czar", "ann-czar")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Tinmouth Collector of Delinquent Taxes", 1,
           [S(TINMOUTH_CONTACTS,
              "Town of Tinmouth, Town Contacts page (live): "
              "Catherine Yoder ('Cat Yoder' on the page) is "
              "Collector of Delinquent Taxes, one-year term to "
              "2027.")],
           [holder("Catherine Yoder", "catherine-yoder")]),
    office("lister", "Lister", "Town of Tinmouth Listers", 3,
           [S(TINMOUTH_CONTACTS,
              "Town of Tinmouth, Town Contacts page (live): "
              "Lister Gail Fallar (term to 2029) completes the "
              "board.")],
           [holder("Gail Fallar", "gail-fallar")]),
    office("selectboard", "Selectboard Member",
           "Town of Tinmouth Selectboard", 3,
           [S(TINMOUTH_CONTACTS,
              "Town of Tinmouth, Town Contacts page (live): "
              "Selectboard member Judy Gilmore (term to 2029) "
              "completes the board.")],
           [holder("Judy Gilmore", "judy-gilmore")]),
    office("moderator", "Moderator", "Town of Tinmouth Moderator", 1,
           [S(TINMOUTH_CONTACTS,
              "Town of Tinmouth, Town Contacts page (live): "
              "Moderator Holly Ross, term to 2027.")],
           [holder("Holly Ross", "holly-ross")]),
])

spec("vernon", [
    office("lister", "Lister", "Town of Vernon Listers", 3,
           [S("https://vernonvt.org/board-of-listers",
              "Town of Vernon, Board of Listers page (live, raw "
              "HTML callout): 'Lister ( Appointed-unexpired "
              "term) - Amy Garrison'. Currency flag (issue "
              "#163): Jesse Jobin, minted as a 2026 winner in "
              "the municipal fan-out, does not appear on the "
              "page; his record is not changed on a page "
              "omission alone.")],
           [holder("Amy Garrison", "amy-garrison",
                   how_seated="appointed")]),
])

STOCKBRIDGE_MINUTES = "https://stockbridgevt.gov/agendas-minutes"
STOCKBRIDGE_NOTE = ("Town of Stockbridge, DRAFT Annual Town "
                    "Meeting Minutes, March 3, 2026 (draft tier, "
                    "disclosed; the official minutes are served "
                    "only through the town's HeyGov meetings app) "
                    "-- Article 1 floor elections, each by a "
                    "single ballot cast by the clerk: ")
spec("stockbridge", [
    office("moderator", "Moderator", "Town of Stockbridge Moderator",
           1,
           [S(STOCKBRIDGE_MINUTES, STOCKBRIDGE_NOTE +
              "Kent Butterfield was elected Moderator for a "
              "one-year term ending 2027.")],
           [holder("Kent Butterfield", "kent-butterfield")]),
    office("auditor", "Auditor", "Town of Stockbridge Auditors", 3,
           [S(STOCKBRIDGE_MINUTES, STOCKBRIDGE_NOTE +
              "Sharon Pavlik was elected auditor for the "
              "remainder of a three-year term ending 2028 (she "
              "had been appointed to the seat the prior year), "
              "and Doris Laing for a three-year term ending 2029 "
              "(the minutes' clarification passage notes Laing "
              "had been appointed to the term vacated by Sylvan "
              "Groth before the meeting; a later passage prints "
              "the diminutive 'Dory Laing' -- the election "
              "line's form governs). Jenny Austin, elected "
              "until 2028, already holds the third seat.")],
           [holder("Sharon Pavlik", "sharon-pavlik"),
            holder("Doris Laing", "doris-laing")]),
    office("lister", "Lister", "Town of Stockbridge Listers", 3,
           [S(STOCKBRIDGE_MINUTES, STOCKBRIDGE_NOTE +
              "Lori Scott was elected lister for a three-year "
              "term ending 2029.")],
           [holder("Lori Scott", "lori-scott")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Stockbridge Trustees of Public Funds", 3,
           [S(STOCKBRIDGE_MINUTES, STOCKBRIDGE_NOTE +
              "Kim Moore was elected Trustee of Public Funds "
              "for a three-year term ending 2029.")],
           [holder("Kim Moore", "kim-moore")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Stockbridge Cemetery Commissioners", 3,
           [S(STOCKBRIDGE_MINUTES, STOCKBRIDGE_NOTE +
              "Joanne Mills was elected Cemetery Commissioner "
              "for a three-year term ending 2029, and Holly "
              "Thompson for the remainder of a term ending "
              "2027.")],
           [holder("Joanne Mills", "joanne-mills"),
            holder("Holly Thompson", "holly-thompson")]),
])

# ================================================================
# C14 -- Waitsfield, Wardsboro, Warren, Waterbury, Waterford,
#        Waterville
# ================================================================
spec("waitsfield", [
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Waitsfield Cemetery Commissioners", 5,
           [S("https://waitsfieldvt.gov/",
              "Town of Waitsfield, Cemeteries page (live): under "
              "'Elected:' the page lists Valerie Capels with "
              "'March 2031' -- the five-year seat that stood in "
              "2026 -- alongside the four commissioners already "
              "recorded. Commission minutes of November 24, 2025 "
              "and March 12, 2026 corroborate her joining.")],
           [holder("Valerie Capels", "valerie-capels")]),
])

spec("wardsboro", [
    office("library-trustee", "Library Trustee",
           "Wardsboro Public Library Trustees", 7,
           [S("https://wardsborovt.gov/",
              "Wardsboro Public Library, About page (live): the "
              "full seven-name trustee roster includes Martin "
              "Loftus and Mark Fernandes alongside the five "
              "already recorded. Both seats were warned for "
              "election at the March 3, 2026 meeting and both "
              "men sit in the trustees' minutes of March 26, "
              "2026 (Loftus re-elected Treasurer). The page "
              "states trustees are elected at town meeting, "
              "vacant seats may be appointed; no per-person "
              "mechanism document was found -- disclosed on "
              "issue #163.")],
           [holder("Martin Loftus", "martin-loftus"),
            holder("Mark Fernandes", "mark-fernandes")]),
])

WARREN_DIR = "https://www.warrenvt.org/"
spec("warren", [
    office("lister", "Lister", "Town of Warren Listers", 3,
           [S(WARREN_DIR,
              "Town of Warren, Board Members directory (live): "
              "the three listers are Sandra Brodeur, Julie "
              "Burns, and Carolyn Adams. Adams was the sole "
              "printed candidate on the 2026 ballot. Minted "
              "elected on the directory presentation, disclosed "
              "on issue #163.")],
           [holder("Sandra Brodeur", "sandra-brodeur"),
            holder("Julie Burns", "julie-burns"),
            holder("Carolyn Adams", "carolyn-adams")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Warren Cemetery Commissioners", 5,
           [S(WARREN_DIR,
              "Town of Warren, Board Members directory (live): "
              "Cemetery Commissioners Charles Snow, Julie Burns, "
              "and Brent Adams sit alongside Jeff Campbell "
              "(already recorded)."),
            S(WARREN_DIR,
              "Town of Warren, Selectboard minutes, March 10, "
              "2026 (DRAFT, disclosed): on motion, 'appoint Ms. "
              "Behn as a Cemetery Commissioner... approved "
              "unanimously' -- Camilla Behn completes the "
              "five-member commission as an appointee. Behn "
              "also sits on the selectboard.")],
           [holder("Charles Snow", "charles-snow"),
            holder("Julie Burns", "julie-burns"),
            holder("Brent Adams", "brent-adams"),
            holder("Camilla Behn", "camilla-behn",
                   how_seated="appointed")]),
])

spec("waterbury", [
    office("moderator", "Moderator", "Town of Waterbury Moderator", 1,
           [S("https://www.waterburyvt.com/",
              "Town of Waterbury, Annual Town Meeting minutes, "
              "March 3, 2026, Article 1: on motion, Rebecca Ellis "
              "was elected Moderator by floor vote, the clerk to "
              "cast one ballot.")],
           [holder("Rebecca Ellis", "rebecca-ellis")]),
])

spec("waterford", [
    office("moderator", "Moderator", "Town of Waterford Moderator", 1,
           [S("https://waterfordvt.gov/",
              "Town of Waterford, Town Personnel page (live): "
              "'Moderator - Maurice Chaloux / Town - 2027', "
              "corroborated by the pre-town-meeting minutes of "
              "February 24, 2026, which he opened as Moderator.")],
           [holder("Maurice Chaloux", "maurice-chaloux")]),
])

WATERVILLE_MINUTES = "http://www.watervillevt.org/boards/"
WATERVILLE_NOTE = ("Town of Waterville, 'Resume of the 2026 Annual "
                   "Town Meeting', March 3, 2026 (official minutes, "
                   "scanned; read page by page): ")
spec("waterville", [
    office("moderator", "Moderator", "Town of Waterville Moderator", 1,
           [S(WATERVILLE_MINUTES, WATERVILLE_NOTE +
              "Heather Thomas was elected Moderator, 56-13 over "
              "Rebecca Pitre.")],
           [holder("Heather Thomas", "heather-thomas")]),
    office("road-commissioner", "Road Commissioner",
           "Town of Waterville Road Commissioner", 1,
           [S(WATERVILLE_MINUTES, WATERVILLE_NOTE +
              "Hunter Locke was elected Road Commissioner.")],
           [holder("Hunter Locke", "hunter-locke")]),
    office("lister", "Lister", "Town of Waterville Listers", 3,
           [S(WATERVILLE_MINUTES, WATERVILLE_NOTE +
              "Linda Ward was elected lister, completing the "
              "three-member board.")],
           [holder("Linda Ward", "linda-ward")]),
    office("auditor", "Auditor", "Town of Waterville Auditors", 3,
           [S(WATERVILLE_MINUTES, WATERVILLE_NOTE +
              "Donna Barry was elected auditor, completing the "
              "three-member board.")],
           [holder("Donna Barry", "donna-barry")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Waterville Collector of Delinquent Taxes", 1,
           [S(WATERVILLE_MINUTES, WATERVILLE_NOTE +
              "Brandi Broe was elected Collector of Delinquent "
              "Taxes. The same minutes elect her Town Clerk and "
              "Treasurer (not sweep items).")],
           [holder("Brandi Broe", "brandi-broe")]),
    office("first-constable", "First Constable",
           "Town of Waterville First Constable", 1,
           [S(WATERVILLE_MINUTES, WATERVILLE_NOTE +
              "Robin Genetti was elected First Constable.")],
           [holder("Robin Genetti", "robin-genetti")]),
    office("second-constable", "Second Constable",
           "Town of Waterville Second Constable", 1,
           [S(WATERVILLE_MINUTES, WATERVILLE_NOTE +
              "Warren Lyon was elected Second Constable.")],
           [holder("Warren Lyon", "warren-lyon")]),
    office("grand-juror", "Grand Juror",
           "Town of Waterville Grand Juror", 1,
           [S(WATERVILLE_MINUTES, WATERVILLE_NOTE +
              "Lucas Tilton was elected Grand Juror.")],
           [holder("Lucas Tilton", "lucas-tilton")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Waterville Trustees of Public Funds", 1,
           [S(WATERVILLE_MINUTES, WATERVILLE_NOTE +
              "Diane Schwarm was elected Trustee of Public "
              "Funds.")],
           [holder("Diane Schwarm", "diane-schwarm")]),
    office("agent-to-convey-real-estate", "Agent to Convey Real Estate",
           "Town of Waterville Agent to Convey Real Estate", 1,
           [S(WATERVILLE_MINUTES, WATERVILLE_NOTE +
              "Diane Schwarm was elected Agent to Convey Real "
              "Estate.")],
           [holder("Diane Schwarm", "diane-schwarm")]),
    office("town-agent", "Town Agent", "Town of Waterville Town Agent",
           1,
           [S(WATERVILLE_MINUTES, WATERVILLE_NOTE +
              "Shawn LaRose was elected Town Agent.")],
           [holder("Shawn LaRose", "shawn-larose")]),
    office("library-trustee", "Library Trustee",
           "Waterville Town Library Trustees", 7,
           [S(WATERVILLE_MINUTES, WATERVILLE_NOTE +
              "Lisa Towery was elected Library Trustee; "
              "corroborated by the town's live Boards page, "
              "whose other names match the trustees already "
              "recorded. Three library seats stay unresolved.")],
           [holder("Lisa Towery", "lisa-towery")]),
])

# ================================================================
# C15 -- Westford, Westminster (town)
# ================================================================
WESTFORD_RETURN = ("https://westfordvt.us/wp-content/uploads/2026/"
                   "03/Official-Return-of-Votes-2026.pdf")
spec("westford", [
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Town of Westford Collector of Delinquent Taxes", 1,
           [S("https://westfordvt.us/",
              "Town of Westford, Selectboard minutes, January "
              "22, 2026: 'Marge McIntosh had retired... J. "
              "Andrews moved to appoint Tommy O'Connor the "
              "Delinquent Tax Collector. P. Haller seconded. "
              "Motion passed 5-0.' The office is charter-"
              "appointed in Westford; O'Connor is also the Town "
              "Administrator (staff) -- the same person.")],
           [holder("Tommy O'Connor", "tommy-oconnor",
                   how_seated="appointed")]),
    office("library-trustee", "Library Trustee",
           "Westford Public Library Trustees", 5,
           [S(WESTFORD_RETURN,
              "Town of Westford, Official Return of Votes, "
              "March 3, 2026 (signed): Sarah Yeager was elected "
              "Library Trustee, 229 votes to Hannah Assefa's "
              "200, taking the full five-year seat that stood "
              "in 2026 (Patricia Hechmer's term expired); "
              "Charles Cavanaugh was elected, 430 votes, to the "
              "five-year seat with one year remaining -- the "
              "seat Kelsi Cross had filled by appointment (her "
              "appointed membership is ended in this sweep, "
              "disclosed on issue #163).")],
           [holder("Sarah Yeager", "sarah-yeager"),
            holder("Charles Cavanaugh", "charles-cavanaugh")]),
])

WESTMINSTER_SB = "https://www.westminstervt.org/selectboard/"
WESTMINSTER_NOTE = ("Town of Westminster, Selectboard minutes, "
                    "April 14, 2026 (draft/unapproved, disclosed; "
                    "each motion carried 3-0 for a one-year term "
                    "ending March 2027): ")
spec("westminster-81400", [
    office("commissioner-of-campbell-fund",
           "Commissioner of Campbell Fund",
           "Town of Westminster Commissioners of Campbell Fund", 3,
           [S(WESTMINSTER_SB, WESTMINSTER_NOTE +
              "Pete Harrison was appointed 'Commissioner of the "
              "Public Fund and Campbell fund'. He had resigned "
              "as a fund trustee effective February 28, 2026, "
              "then was appointed commissioner. One commissioner "
              "seat stays open.")],
           [holder("Pete Harrison", "pete-harrison",
                   how_seated="appointed")]),
    office("trustee-of-campbell-fund", "Trustee of Campbell Fund",
           "Town of Westminster Trustees of Campbell Fund", 3,
           [S(WESTMINSTER_SB, WESTMINSTER_NOTE +
              "Barbara Taylor was appointed 'Trustee of the "
              "Campbell and Public Fund', filling her own seat, "
              "which had drawn only write-ins at the March 3, "
              "2026 election. The single bundled motion names "
              "her trustee of BOTH funds, so she is recorded on "
              "both trustee posts (modeling call disclosed on "
              "issue #163).")],
           [holder("Barbara Taylor", "barbara-taylor",
                   how_seated="appointed")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Town of Westminster Trustees of Public Funds", 3,
           [S(WESTMINSTER_SB, WESTMINSTER_NOTE +
              "Barbara Taylor was appointed 'Trustee of the "
              "Campbell and Public Fund' under the same bundled "
              "motion (see the Campbell Fund entry). One Public "
              "Funds seat stays open.")],
           [holder("Barbara Taylor", "barbara-taylor",
                   how_seated="appointed")]),
])

# ================================================================
# C16 -- Woodstock Village, Worcester, Wolcott
# (Wilmington's only sweep actions are structural: the Staib
# cemetery win was already minted in batch 27 from the same
# certificate, and the Haynes Fund post removal is a hand edit.)
# ================================================================
WVILLAGE_MINUTES = ("https://www.townofwoodstock.org/fileadmin/"
                    "files/Boards_and_Committees/Village_Trustees/"
                    "Meetings/2026/03/VillageMeetingMinutes"
                    "03.17.26.pdf")
WVILLAGE_NOTE = ("Village of Woodstock, Annual Village Meeting "
                 "minutes, March 17, 2026, Article 1: ")
spec("woodstock", [
    office("moderator", "Moderator",
           "Village of Woodstock Moderator", 1,
           [S(WVILLAGE_MINUTES, WVILLAGE_NOTE +
              "Greg Camp was elected Moderator.")],
           [holder("Greg Camp", "greg-camp")]),
    office("village-clerk", "Village Clerk",
           "Village of Woodstock Village Clerk", 1,
           [S(WVILLAGE_MINUTES, WVILLAGE_NOTE +
              "Don Wheeler was elected Village Clerk (full form "
              "Donald R. Wheeler per the Village Report 2026 "
              "officers table).")],
           [holder("Donald R. Wheeler", "donald-r-wheeler")]),
    office("village-treasurer", "Village Treasurer",
           "Village of Woodstock Village Treasurer", 1,
           [S(WVILLAGE_MINUTES, WVILLAGE_NOTE +
              "F. Charles Degener was 'elected to another term' "
              "as Village Treasurer (full form F. Charles "
              "Degener III). His person record is held under "
              "the Town of Woodstock scope, where he serves as "
              "town clerk/treasurer; the same record is reused "
              "here.")],
           [holder("F. Charles Degener III", "f-charles-degener-iii",
                   person_scope="woodstock-85975")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Village of Woodstock Trustees of Public Funds", 1,
           [S(WVILLAGE_MINUTES, WVILLAGE_NOTE +
              "Michael Green was elected Trustee of Public "
              "Funds. His person record is held under the Town "
              "of Woodstock scope, where he also holds a town "
              "TPF seat; the same record is reused here.")],
           [holder("Michael Green", "michael-green",
                   person_scope="woodstock-85975")]),
])

spec("worcester", [
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Worcester Cemetery Commissioners", 3,
           [S("https://worcestervt.org/wp/directory",
              "Town of Worcester, town Directory (live): "
              "'CEMETERY COMMISSION / Chair: Julia Shedd / "
              "Treasurer/Secretary: Francette Cerulli' -- both "
              "corroborated acting in the commission's minutes "
              "of April 27 and July 15, 2026 (styled 'Julie' and "
              "'Fran'). Minted elected on this presentation, "
              "disclosed on issue #163."),
            S("https://worcestervt.org/wp/public_html/wp/wp-content/"
              "uploads/2026/09/Cemetery-Minutes-9.9.26.pdf",
              "Town of Worcester, Cemetery Commission minutes, "
              "September 9, 2026, item 7: 'Fran moved to appoint "
              "John Meninger to the commission to fill the "
              "remainder of Heather Pagel's open position. Julie "
              "seconded. John accepted.' Pagel's cemetery "
              "membership is ended in this sweep (her separate "
              "Treasurer record is untouched). Noted on issue "
              "#163: 24 V.S.A. section 963 ordinarily vests "
              "vacancy appointments in the selectboard; the "
              "appointment here is recorded in the commission's "
              "own minutes and no selectboard minute was "
              "found.")],
           [holder("Julia Shedd", "julia-shedd"),
            holder("Francette Cerulli", "francette-cerulli"),
            holder("John Meninger", "john-meninger",
                   how_seated="appointed")]),
])

WOLCOTT_TM = "https://wolcottvt.org/"
WOLCOTT_NOTE = ("Town of Wolcott, Annual Town Meeting minutes, "
                "March 3, 2026 (read from the town's official "
                "site; the site serves a captcha interstitial "
                "to direct fetches, so the minutes were read in "
                "the browser): ")
spec("wolcott", [
    office("moderator", "Moderator", "Town of Wolcott Moderator", 1,
           [S(WOLCOTT_TM, WOLCOTT_NOTE +
              "Joe Hester-Ingram 'was elected as Moderator for "
              "a one year term'. He was a batch-28 straggler; "
              "the minutes resolve the seat.")],
           [holder("Joe Hester-Ingram", "joe-hester-ingram")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Town of Wolcott Cemetery Commissioners", 5,
           [S(WOLCOTT_TM, WOLCOTT_NOTE +
              "Lucien Gravel was elected Cemetery Commissioner "
              "for a five-year term and Derrick Lowell for a "
              "four-year term, completing the five-member "
              "commission. The commission's own page lists six "
              "names, including Belinda Clegg (the town clerk); "
              "the minutes' elected set and the five-seat count "
              "leave no seat for her and she is not minted.")],
           [holder("Lucien Gravel", "lucien-gravel"),
            holder("Derrick Lowell", "derrick-lowell")]),
    office("library-trustee", "Library Trustee",
           "Wolcott Town Library Trustees", 5,
           [S(WOLCOTT_TM, WOLCOTT_NOTE +
              "Edith Duff was elected Library Trustee for a "
              "five-year term and Nicolette LeRiche for a "
              "two-year term (the library's own site styles "
              "them 'Edie Duff' and 'Nikki LeRiche'; the "
              "minutes' forms govern). The third seat standing "
              "in 2026 (one-year) elected no one per the "
              "minutes and stays open.")],
           [holder("Edith Duff", "edith-duff"),
            holder("Nicolette LeRiche", "nicolette-leriche")]),
])

# ================================================================
# Danville corrections (audit of the batch-6 build; the phantom
# source document cited by the suspect records does not exist --
# see scripts/vt_muni_sweep_research.md). Membership deletions
# (auditor Grout, constable Choate, moderator Bach, listers
# Woodward/Langford), the SB source-note replacements, and the
# lister seat-count fix are hand edits; the JP slate was verified
# concordant (10 winners = 10 memberships) and needs no change.
# ================================================================
DANVILLE_REPORT = "https://danvillevt.gov"
DANVILLE_NOTE = ("Town of Danville, 2025 Annual Town Report, "
                 "elected officers tables (pp. 10-12): ")
spec("danville", [
    office("moderator", "Moderator", "Town of Danville Moderator", 1,
           [S(DANVILLE_REPORT, DANVILLE_NOTE +
              "Moderator Ernest Tobias Balivet (term to 2026)."),
            S(DANVILLE_REPORT,
              "Town of Danville, DRAFT Annual Town Meeting "
              "minutes, March 3, 2026: Balivet was re-elected "
              "Moderator. This record corrects the batch-6 "
              "build, which seated Eric Bach as moderator on a "
              "cited 'Results of Officers Elected' document "
              "that does not exist; Bach's moderator membership "
              "is removed in this sweep (his selectboard and JP "
              "records are verified and stand).")],
           [holder("Ernest Tobias Balivet",
                   "ernest-tobias-balivet")]),
    office("lister", "Lister", "Town of Danville Listers", 3,
           [S(DANVILLE_REPORT, DANVILLE_NOTE +
              "Listers J. Timothy Ide (term to 2028), John "
              "Blackmore (2027), and Marcia Pettigrew (2026)."),
            S(DANVILLE_REPORT,
              "Town of Danville, DRAFT Annual Town Meeting "
              "minutes, March 3, 2026: Pettigrew was re-elected "
              "lister (new term to 2029). This corrects the "
              "batch-6 build, which seated two listers who "
              "appear in no Danville document (their memberships "
              "are removed) and carried the post at two seats; "
              "the post is corrected to three seats.")],
           [holder("J. Timothy Ide", "j-timothy-ide"),
            holder("John Blackmore", "john-blackmore"),
            holder("Marcia Pettigrew", "marcia-pettigrew")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Danville Collector of Delinquent Taxes", 1,
           [S(DANVILLE_REPORT, DANVILLE_NOTE +
              "Collector of Delinquent Taxes Edward Ledo (term "
              "to 2026)."),
            S(DANVILLE_REPORT,
              "Town of Danville, 2026 Annual Town Meeting "
              "Warning (January 15, 2026) and DRAFT minutes, "
              "March 3, 2026: the warning carries a Delinquent "
              "Tax Collector article and the minutes record Ed "
              "Ledo re-elected. The batch-6 build created no "
              "DTC post for Danville; it is created here.")],
           [holder("Edward Ledo", "edward-ledo")]),
])

# ================================================================
# Emit
# ================================================================
for place in ORDER:
    out = DATA_DIR / f"{place}__sweep.json"
    out.write_text(json.dumps(SPECS[place], indent=1) + "\n")
    print("wrote", out.name)
