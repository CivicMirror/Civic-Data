#!/usr/bin/env python3
"""VT #163 school pass -- worked example: Lincoln School District.
Emits scripts/vt_school_data/lincoln.json for build_vt_school.py.
All facts firsthand-verified 2026-10-22 from the district's own site."""
import json
from pathlib import Path

OUT = (Path(__file__).resolve().parent / "vt_school_data" /
       "lincoln.json")
R = "2026-10-22"


def S(url, note):
    return {"url": url, "note": note, "retrieved": R}


STATUTE = S(
    "https://legislature.vermont.gov/statutes/section/16/010/00603",
    "16 V.S.A. section 603(a)(3)(D) (as amended, effective July 1, "
    "2026) names the 'Lincoln Supervisory District' in the official "
    "inventory of supervisory unions and districts: the Lincoln "
    "School District is a single-town school district designated its "
    "own supervisory district under 16 V.S.A. section 261(c) in "
    "November 2022, with full operations from July 1, 2023, after "
    "the town's withdrawal from the Mount Abraham Unified School "
    "District.")
SITE = S(
    "https://lincolnsd.org/",
    "Lincoln School District (official district website): the "
    "district operates the Lincoln Community School (K-6) and a "
    "grades 7-12 tuition/choice program.")
ROSTER = S(
    "https://lincolnsd.org/lincoln-school-board",
    "Lincoln School District, 'Lincoln School Board -- Meet the "
    "Board' (official roster, live): Jeanne Albert, Chair (term "
    "expires 3/2028); Deirdre Kelly, Vice Chair (3/2027); Mary "
    "Gemignani, Clerk (3/2027); Peg Sutlive; Deborah Lubar -- each "
    "with a district email address (jalbert@, dkelly@, "
    "mgemignani@, psutlive@, dlubar@lincolnsd.org). A town "
    "district's school board is elected under 16 V.S.A. section "
    "423 (three directors, or five as Lincoln's electorate has "
    "chosen); the board has five seats.")
JAN_AGENDA = S(
    "https://lincolnsd.org/s/2026-1-27-Jan-LSD-Board-Meeting-agenda-wd7j.pdf",
    "Lincoln School District Board meeting agenda, January 27, "
    "2026: 'Board members present: Chair Jeanne Albert, Rob "
    "Backlund, Deirdre Kelly, Peg Sutlive, Mary Gemignani' -- the "
    "five-member board before the March 2026 annual meeting.")
ANNUAL = S(
    "https://lincolnsd.org/s/Lincoln-School-District-Annual-Meeting-2026-Presentationpptx-1.pdf",
    "Lincoln School District Annual Meeting 2026 presentation: "
    "Article 8 elected, by Australian ballot on Tuesday, March 3, "
    "2026, one School Director for three years and one School "
    "Director for two years (plus a one-year School Meeting "
    "Moderator). The two expiring directorships were Peg "
    "Sutlive's (the roster page printed her term expiring "
    "3/2026) and Rob Backlund's.")
MAR_MINUTES = S(
    "https://lincolnsd.org/s/_2026-3-24-March-LSD-Board-Meeting-minutes.pdf",
    "Lincoln School District Board minutes, March 24, 2026 (the "
    "first regular meeting after the annual meeting): board "
    "members present include Deborah Lubar; Backlund does not "
    "appear, and the district's live roster no longer lists him.")
APR_MINUTES = S(
    "https://lincolnsd.org/s/2026-4-14-April-LSD-Board-Meeting.pdf",
    "Lincoln School District Board minutes, April 14, 2026: "
    "board members present include Peg Sutlive -- she held her "
    "seat through the March 2026 election.")

SPEC = {
    "district_slug": "lincoln",
    "district_name": "Lincoln School District",
    "jurisdiction_sources": [STATUTE, SITE],
    "board": {
        "org_name": "Lincoln School Board",
        "post_title": "School Director",
        "seats": 5,
        "sources": [ROSTER, JAN_AGENDA],
    },
    "directors": [
        {"name": "Jeanne Albert", "slug": "jeanne-albert",
         "sources": [ROSTER, JAN_AGENDA]},
        {"name": "Deirdre Kelly", "slug": "deirdre-kelly",
         "sources": [ROSTER, JAN_AGENDA]},
        {"name": "Mary Gemignani", "slug": "mary-gemignani",
         "sources": [ROSTER, JAN_AGENDA]},
        {"name": "Peg Sutlive", "slug": "peg-sutlive",
         "sources": [ROSTER, ANNUAL, APR_MINUTES]},
        {"name": "Deborah Lubar", "slug": "deborah-lubar",
         "sources": [S(
             "https://lincolnsd.org/lincoln-school-board",
             "Lincoln School District roster (live) lists Deborah "
             "Lubar as a current School Board member "
             "(dlubar@lincolnsd.org). She was seated at the March "
             "3, 2026 annual meeting: Article 8 of that meeting "
             "elected two directors (three-year and two-year "
             "terms) for the seats whose terms expired -- Peg "
             "Sutlive's and Rob Backlund's; Sutlive held her seat "
             "(April 14, 2026 minutes) and Lubar appears as a "
             "board member in the March 24, 2026 minutes, taking "
             "the seat Backlund vacated. Recorded elected on that "
             "chain; which of the two 2026 terms (three-year or "
             "two-year) is hers is not published."),
          MAR_MINUTES]},
        {"name": "Rob Backlund", "slug": "rob-backlund",
         "end": "2026",
         "sources": [S(
             "https://lincolnsd.org/s/2026-1-27-Jan-LSD-Board-Meeting-agenda-wd7j.pdf",
             "Lincoln School District Board agenda, January 27, "
             "2026, lists Rob Backlund as a board member present; "
             "his term expired at the March 3, 2026 annual "
             "meeting, where one of the two directorships on the "
             "ballot was his seat. He does not appear in the "
             "March 24, 2026 minutes and the district's live "
             "roster no longer lists him, so this membership is "
             "ended in 2026. Deborah Lubar holds the seat "
             "now."),
          MAR_MINUTES]},
    ],
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(SPEC, indent=1))
print("emitted", OUT.name)
