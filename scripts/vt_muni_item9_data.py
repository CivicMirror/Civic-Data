#!/usr/bin/env python3
"""VT #163 -- Item 9 (disclosed judgment calls) follow-up mints, from
documents Walter supplied 2026-10-22. Emits __item9.json specs.
Ended memberships get their end via the hand-edits step."""
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


def office(slug, title, org_name, seats, sources, holders):
    return {"slug": slug, "title": title, "org_name": org_name,
            "seats": seats, "sources": sources, "holders": holders}


SPECS = {}


def spec(place_slug, offices):
    orig = json.loads((DATA / f"{place_slug}.json").read_text())
    SPECS[place_slug] = {
        "label": orig["label"],
        "place_slug": place_slug,
        "jurisdiction_id": orig["jurisdiction_id"],
        "header": ("# " + orig["label"] +
                   " -- item-9 follow-up, 2026-10-22; "
                   "issue #163 (VT master tracking).\n"),
        "offices": offices,
    }


LUDLOW_FY25 = ("https://ludlow.vt.us/vertical/sites/"
               "%7B78E8DA21-0D46-4486-AF59-9D2B5A1048F3%7D/uploads/"
               "FY25_Town_Appointed__Elected_Officers.pdf")
spec("ludlow-41275", [
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Ludlow Cemetery Commission", 5,
           [S(LUDLOW_FY25,
              "Town of Ludlow, 'FY25 Town Appointed & Elected "
              "Officers' list: the Board of Cemetery "
              "Commissioners is Robert Brandt (elected), Bruce "
              "Schmidt, Chair (elected, term to 2029), Shannon "
              "Stark (elected, 2028), Scott Baitz (appointed) "
              "and Ludwig Gabranski (elected, term to 2026). "
              "Gabranski was missed by the earlier builds; he "
              "no longer sits -- George Tucker, Jr. joined the "
              "commission between March 18 and July 15, 2026, "
              "consistent with a vacancy appointment to "
              "Gabranski's seat -- so this membership is ended "
              "in 2026 (the hand-edits step adds the end).")],
           [holder("Ludwig Gabranski", "ludwig-gabranski")]),
])

spec("salisbury", [
    office("lister", "Lister", "Salisbury Board of Listers", 3,
           [S("https://www.townofsalisbury.org/listers",
              "Town of Salisbury, Board of Listers page (live): "
              "'At present, the Board of Listers has 2 members. "
              "There is a need of a 3rd lister. Current members "
              "and their terms: Kim Cunnigham 2020; Dan "
              "Kuczynski 2018.' Cunningham and Kuczynski are "
              "the sitting elected listers (name spellings as "
              "the page prints them); the third seat is vacant "
              "per the page itself. Neither was captured by "
              "the earlier builds.")],
           [holder("Kim Cunnigham", "kim-cunnigham"),
            holder("Dan Kuczynski", "dan-kuczynski")]),
])

SHOREHAM_RPT = ("https://www.shorehamvt.us/_files/ugd/"
                "d53131_3cbc693352124fb6b0ad0141c1edd153.pdf")
spec("shoreham", [
    office("auditor", "Auditor", "Shoreham Auditors", 3,
           [S(SHOREHAM_RPT,
              "Town of Shoreham, 2025 Annual Town Report, "
              "officers table: Auditors -- Timothy Steady, 3 "
              "years (2023-2026); Sarah Gosselin (APPOINTED), "
              "3 years (2024-2027); Tamra Hawley-House, 3 years "
              "(2025-2028). Steady's term expired in 2026 and "
              "Gosselin no longer sits (the town's current "
              "auditors page lists Hawley-House, "
              "Jarboe-Singletary and Treadway); both "
              "memberships are ended in 2026 in the hand-edits "
              "step. Gosselin is recorded appointed, as the "
              "report tags her.")],
           [holder("Timothy Steady", "timothy-steady"),
            holder("Sarah Gosselin", "sarah-gosselin",
                   how_seated="appointed")]),
])

for place, s in SPECS.items():
    out = DATA / f"{place}__item9.json"
    out.write_text(json.dumps(s, indent=1))
    print("emitted", out.name)
