#!/usr/bin/env python3
"""VT #163 -- Marshfield Village, minted as it currently stands at
Walter's direction 2026-10-22 (no clarification found; no new
information). The village publishes no roster and has no website;
the only roster is the Village Clerk/Treasurer's email reply as
logged in the VT Jurisdiction Factory. Emits marshfield__village.json."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "vt_muni_data"
RETRIEVED = "2026-10-22"
SOS_VILLAGES = ("https://sos.vermont.gov/vsara/learn/municipalities/"
                "incorporated-villages")

ROSTER = ("Roster as it currently stands, minted at Walter's direction "
          "2026-10-22 (no new information was found): the Village of "
          "Marshfield publishes no officer roster and has no website; "
          "the only roster is the reply of the Village Clerk/Treasurer "
          "(Meg Eberhardt) to a records inquiry, as logged in the VT "
          "Jurisdiction Factory workbook's source evidence "
          "(src-vt-reply-063-marshfield-clerk): President Arthur "
          "Gilman; Trustees Marie Olson-Badeau, Tamara McKee and "
          "Nicole Auerbach; the board totals five seats including the "
          "president, with one trustee seat vacant. Auerbach's role "
          "term is logged APPOINTED (2026-09-23), consistent with a "
          "mid-term vacancy appointment; the others are recorded "
          "elected. URL given is the Secretary of State's "
          "incorporated-villages list, which carries the village "
          "itself; the roster rests on the clerk's reply as stated.")


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


spec_out = {
    "label": "Village of Marshfield",
    "place_slug": "marshfield",
    "jurisdiction_id": ("ocd-jurisdiction/country:us/state:vt/place:"
                        "marshfield/government"),
    "header": ("# Village of Marshfield -- minted as it stands at "
               "Walter's direction, 2026-10-22; issue #163 (VT "
               "master tracking).\n"),
    "offices": [
        office("village-president", "Village President",
               "Village of Marshfield", 1,
               [S(SOS_VILLAGES, ROSTER)],
               [holder("Arthur Gilman", "arthur-gilman")]),
        office("village-trustee", "Village Trustee",
               "Marshfield Village Board of Trustees", 4,
               [S(SOS_VILLAGES, ROSTER +
                  " Trustee seats are modeled as four (five board "
                  "seats including the separately modeled "
                  "president), three filled and one vacant.")],
               [holder("Marie Olson-Badeau", "marie-olson-badeau"),
                holder("Tamara McKee", "tamara-mckee"),
                holder("Nicole Auerbach", "nicole-auerbach",
                       how_seated="appointed")]),
        office("village-clerk", "Village Clerk",
               "Village of Marshfield", 1,
               [S(SOS_VILLAGES,
                  "The clerk's reply logged in the VT Jurisdiction "
                  "Factory (src-vt-reply-063-marshfield-clerk) is "
                  "attributed to 'Village of Marshfield, Inc. -- "
                  "Clerk/Treasurer Meg Eberhardt'; she is recorded "
                  "as the village's Clerk on that attribution, "
                  "minted at Walter's direction 2026-10-22 as the "
                  "village currently stands. She is the Town of "
                  "Marshfield's lister and a justice of the peace "
                  "in this dataset; this membership reuses that "
                  "person record.")],
               [holder("Margaret Eberhardt", "margaret-eberhardt",
                       person_scope="marshfield-43600")]),
        office("village-treasurer", "Village Treasurer",
               "Village of Marshfield", 1,
               [S(SOS_VILLAGES,
                  "Same attribution as the village-clerk record: "
                  "the clerk's reply logged in the VT Jurisdiction "
                  "Factory is attributed to 'Village of Marshfield, "
                  "Inc. -- Clerk/Treasurer Meg Eberhardt'; she is "
                  "recorded as the village's Treasurer on that "
                  "attribution, minted at Walter's direction "
                  "2026-10-22.")],
               [holder("Margaret Eberhardt", "margaret-eberhardt",
                       person_scope="marshfield-43600")]),
    ],
}

out = DATA / "marshfield__village.json"
out.write_text(json.dumps(spec_out, indent=1))
print("emitted", out.name)
