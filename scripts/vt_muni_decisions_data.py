#!/usr/bin/env python3
"""VT #163 -- sweep decision items decided by Walter 2026-10-22.
Emits vt_muni_data/<place>__decisions.json for build_vt_municipality.py.
Every mint below rests on Walter's verdict in the VT tracking chat plus
the official document named in its note."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "vt_muni_data"
RETRIEVED = "2026-10-22"


def S(url, note):
    return {"url": url, "note": note, "retrieved": RETRIEVED}


def holder(name, slug, how_seated=None, **kw):
    h = {"name": name, "slug": slug}
    if how_seated:
        h["how_seated"] = how_seated
    h.update(kw)
    return h


def office(slug, title, org_name, seats, sources, holders,
           post_sources=None):
    o = {"slug": slug, "title": title, "org_name": org_name,
         "seats": seats, "sources": sources, "holders": holders}
    if post_sources:
        o["post_sources"] = post_sources
    return o


SPECS = {}


def spec(place_slug, offices):
    orig = json.loads((DATA / f"{place_slug}.json").read_text())
    SPECS[place_slug] = {
        "label": orig["label"],
        "place_slug": place_slug,
        "jurisdiction_id": orig["jurisdiction_id"],
        "header": ("# " + orig["label"] +
                   " -- sweep decisions applied 2026-10-22; "
                   "issue #163 (VT master tracking).\n"),
        "offices": offices,
    }


W = "Walter's ruling, 2026-10-22, on the sweep report's decision items."

# ------------------------------------------------------------------
# 1. Morrisville -- mint from MWL's UNOFFICIAL results (Walter: use it)
MWL = "https://www.mwlvt.com"
MWL_NOTE = (
    "Morrisville Water & Light (the village's utility), "
    "'UNOFFICIAL RESULTS - ANNUAL VILLAGE MEETING, APRIL 13, "
    "2026' (self-labeled unofficial; the direct file link has "
    "since rotated off the site): {who}. Minted from this "
    "unofficial sheet at " + W)
spec("morrisville", [
    office("moderator", "Village Moderator",
           "Morrisville Village Moderator", 1,
           [S(MWL, MWL_NOTE.format(
               who="Richard Craig was elected Moderator. Craig's "
                   "Morristown person record is reused -- the "
                   "village lies within Morristown and he is its "
                   "selectboard member and a justice of the peace"))],
           [holder("Richard Craig", "richard-craig",
                   person_scope="morristown")]),
    office("village-clerk", "Village Clerk",
           "Morrisville Village Clerk", 1,
           [S(MWL, MWL_NOTE.format(
               who="Sara Haskins was elected Village Clerk. "
                   "Haskins's Morristown person record is reused "
                   "-- she is Morristown's town clerk, treasurer "
                   "and delinquent tax collector"))],
           [holder("Sara Haskins", "sara-haskins",
                   person_scope="morristown")]),
    office("village-treasurer", "Village Treasurer",
           "Morrisville Village Treasurer", 1,
           [S(MWL, MWL_NOTE.format(
               who="Sara Haskins was elected Village Treasurer. "
                   "Haskins's Morristown person record is reused "
                   "-- she is Morristown's town clerk, treasurer "
                   "and delinquent tax collector"))],
           [holder("Sara Haskins", "sara-haskins",
                   person_scope="morristown")]),
])

# ------------------------------------------------------------------
# 2. Mendon -- mint from the UNOFFICIAL tally (Walter: use it)
spec("mendon", [
    office("moderator", "Moderator", "Mendon Moderator", 1,
           [S("https://www.mendonvt.gov",
              "Town of Mendon, '2026 Town Meeting Ballot Results' "
              "tally sheet (town-posted; hand-labeled 'UNOFFICIAL "
              "RESULTS'): Christopher Corsones, the sole printed "
              "candidate for Moderator, received 170 of 181 votes. "
              "Corroborated by the draft Town Meeting minutes, "
              "March 2, 2026, signed 'Chris Corsones, Moderator.' "
              "Minted from the unofficial tally at " + W)],
           [holder("Christopher Corsones", "christopher-corsones")]),
])

# ------------------------------------------------------------------
# 3. Georgia library -- Walter's March 18 packet settles the board.
RESULTS = ("https://www.townofgeorgia.com/elections-voting/page/"
           "election-results")
PACKET = ("https://mccmeetings.blob.core.usgovcloudapi.net/"
          "georgiavt-pubu/MEET-Packet-b3f9d3b6099441c0be6096609b70fbaf"
          ".pdf")
spec("georgia", [
    office("library-trustee", "Library Trustee",
           "Georgia Public Library Trustees", 5,
           [S(RESULTS,
              "Town of Georgia, official election results page: "
              "'Library Trustee - 1 year (Vote for 3) -- Ben "
              "Chiappinelli 555; Heather Dunsmore 432; Sarah "
              "Savich 392; Nicole Jamison 380; Deborah Mann 217.' "
              "Chiappinelli and Heather Dunsmore were elected "
              "March 3, 2026 (Savich's membership already stands)."),
            S(PACKET,
              "Georgia Public Library, Trustee Meeting packet for "
              "March 18, 2026 (supplied by Walter 2026-10-22), "
              "item B: Special Meeting minutes, March 10, 2026 -- "
              "the reorganized board is Ben Chiappinelli (Chair), "
              "Sarah Savich (Vice Chair), Kollene Caspers "
              "(Secretary), Terry Cleveland (Treasurer) and "
              "Heather Dunsmore, all present and voting. Item A "
              "(minutes, February 18, 2026) shows Cleveland and "
              "Caspers as trustees before the election -- they "
              "are the continuing members. The library website "
              "roster the sweep relied on was stale (it still "
              "listed Mann, who lost, and a 'Harvey' who appears "
              "in no minutes). Heather Dunsmore's election also "
              "corrects the sweep, which seated Brian Dunsmore "
              "on the surname alone -- his library membership is "
              "removed in the same push; his other records "
              "stand.")],
           [holder("Ben Chiappinelli", "ben-chiappinelli"),
            holder("Heather Dunsmore", "heather-dunsmore"),
            holder("Terry Cleveland", "terry-cleveland")]),
])

# ------------------------------------------------------------------
# 4. Guilford -- "Flip": Ohrstrom + Hallowell are ELECTED. (They were
#    never in the repo -- the sweep report's premise that batch 10 had
#    recorded them appointed was wrong; no post existed. Post created
#    now, modeling the town-elected seats.)
GUILFORD_TM = ("https://guilfordvt.gov/wp-content/uploads/2026/03/"
               "Town-Meeting-Minutes-2.28.26.pdf")
spec("guilford", [
    office("library-trustee", "Library Trustee",
           "Guilford Free Library Trustees", 2,
           [S(GUILFORD_TM,
              "Town of Guilford, Annual Town Meeting minutes, "
              "February 28, 2026, Article 4 (as amended): Meghan "
              "Ohrstrom was nominated 'to fill Sandra's 3 year "
              "term' as Library Trustee and Emma Hallowell to "
              "the 4-year Library Trustee seat; both had been "
              "serving as interim trustees and both were elected "
              "by the Article 4 voice vote ('All in Favor'). "
              "Recorded elected at " + W + " The sweep report "
              "misstated that an earlier batch had recorded them "
              "appointed; in fact no Guilford library post or "
              "membership existed.")],
           [holder("Meghan Ohrstrom", "meghan-ohrstrom"),
            holder("Emma Hallowell", "emma-hallowell")],
           post_sources=[S(
               GUILFORD_TM,
               "The Guilford Free Library board has nine trustees "
               "mixing town-elected and association trustees; "
               "this post models the town-elected seats filled "
               "at town meeting (two, at the February 28, 2026 "
               "meeting).")]),
])

# ------------------------------------------------------------------
# 7. Vergennes -- Austin seated APPOINTED (Walter).
spec("vergennes", [
    office("auditor", "Auditor", "City of Vergennes Auditors", 3,
           [S("https://www.vergennes.org/government/city_council/"
              "index.php",
              "City of Vergennes, City Council minutes (DRAFT), "
              "May 12, 2026: David Austin sits as a member of the "
              "Board of Auditors. Austin was appointed in "
              "December 2025 to serve only until the March 2026 "
              "annual meeting; no election or reappointment is "
              "recorded, but the draft minutes present him as "
              "sitting. Seated as appointed at " + W)],
           [holder("David Austin", "david-austin",
                   how_seated="appointed")]),
])

# ------------------------------------------------------------------
# 8. Alburgh Village -- "Delinquent Collector" IS the charter
#    Collector (Walter: same office/person).
spec("alburgh", [
    office("collector", "Collector", "Alburgh Village Collector", 1,
           [S("https://villageofalburgh.org/",
              "Village of Alburgh, official homepage (live): "
              "under 'Village Delinquent Collector' the village "
              "lists Cheryl Dunn. The charter office is titled "
              "Collector (24 App. V.S.A. ch. 203 sec. 301(a)); "
              "the homepage label is the same office in "
              "practice, per " + W + " Dunn's existing person "
              "record (Alburgh town scope -- she is the town "
              "lister and the village clerk and treasurer) is "
              "reused."),
            S("https://legislature.vermont.gov/statutes/"
              "fullchapter/24APPENDIX/203",
              "Village of Alburgh charter, 24 App. V.S.A. ch. "
              "203, sec. 301(a): the Collector is among the "
              "village officers elected at the annual meeting.")],
           [holder("Cheryl Dunn", "cheryl-dunn",
                   person_scope="alburgh-00860")]),
])

for place, s in SPECS.items():
    out = DATA / f"{place}__decisions.json"
    out.write_text(json.dumps(s, indent=1))
    print("emitted", out.name)
