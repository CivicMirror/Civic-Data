#!/usr/bin/env python3
"""
Mint jurisdiction files for TX's numbered judicial districts (District
Courts) and appellate districts (Courts of Appeals), for issue #26.

Follows the per-entity jurisdiction pattern issue #27 established for Soil &
Water Conservation Districts (a sub-state entity that doesn't map onto a
single county gets its own jurisdiction, keyed to a stable slug), using the
`judiciary` classification added to jurisdiction.schema.json for #26.

Two sources, both committed under `reference/TX Rolling Audit/OCA Judicial
Directory/`:
  - district-courts-by-county-2026-05-01.json -- parsed from the Texas
    Office of Court Administration's "District Judges by Judicial District"
    directory PDF (txcourts.gov, retrieved 2026-09-01, reflects the district
    court structure as of 2026-05-01).
  - appellate-districts-by-county-govcode-22.201.json -- parsed from Texas
    Government Code Sec. 22.201, current through the 2023 88th Legislature
    amendment (S.B. 1045, eff. 2023-09-01) that redrew several districts and
    created the 15th Court of Appeals. A 2005 OCA county-map PDF was found
    first and rejected as a source for this reason -- it predates both the
    redistricting and the 15th court's creation.

Scope decision, single- vs multi-county judicial districts:
  A single-county judicial district (400 of 497) doesn't need a new
  jurisdiction record at all -- its Organization can attach directly to that
  county's existing jurisdiction file, the same way County Court at Law
  judges were handled in #29. Only the 97 multi-county judicial districts
  need one, and several numbered districts serve the *identical* county set
  (e.g. the 18th and 249th both serve only Johnson & Somervell) -- those
  share ONE jurisdiction file, keyed to the county combination rather than
  to either district number, since jurisdiction represents the geography,
  not the court. That collapses 97 multi-county district rows to 83 distinct
  jurisdiction files.

  All 14 numbered Courts of Appeals districts are multi-county and each get
  their own jurisdiction file. The 15th Court of Appeals is excluded here --
  Gov't Code 22.201(p) makes it explicitly statewide ("all counties in this
  state"), so it belongs under the existing state:tx/judiciary jurisdiction
  (data/us/tx/jurisdictions/state/tx-judiciary.yaml, minted for SCOTX/CCA),
  not a new appellate-district jurisdiction.

This script mints jurisdiction files only. It does NOT import officers or
create organizations/posts -- that's follow-up work once the officer-side
2024 winner data is joined against these jurisdictions.

Idempotent by id and filename. Dry run by default; pass --write to persist.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
SRC_DIR = REPO / "reference" / "TX Rolling Audit" / "OCA Judicial Directory"
RETRIEVED = "2026-09-01"

DISTRICT_COURT_SOURCE = {
    "url": "https://www.txcourts.gov/media/1462770/district-judges-by-judicial-district.pdf",
    "note": "Texas Office of Court Administration, \"District Judges by Judicial District\" directory, dated 2026-05-01.",
    "retrieved": RETRIEVED,
}
APPELLATE_SOURCE = {
    "url": "https://statutes.capitol.texas.gov/Docs/GV/htm/GV.22.htm#22.201",
    "note": "Texas Government Code Sec. 22.201 (Courts of Appeals Districts), current through Acts 2023, 88th Leg., R.S., Ch. 459 (S.B. 1045), eff. 2023-09-01.",
    "retrieved": RETRIEVED,
}

FIXUPS = {"dewitt": "de-witt", "lasalle": "la-salle"}


def slugify(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def county_slug(raw):
    key = raw.strip().lower().replace(" ", "")
    return FIXUPS.get(key, slugify(raw))


def _ordinal(n):
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def ordinal_district_label(num):
    """'18' -> '18th Judicial District'; '1A' -> '1A Judicial District'
    (letter suffix kept as-is, no ordinal added); '2nd 25' -> '2nd 25th
    Judicial District' (a real duplicate-number court with concurrent
    jurisdiction over the same counties as the 25th)."""
    m = re.match(r"^(\d+)([A-Za-z]*)$", num)
    if m:
        digits, suffix = m.groups()
        label = f"{digits}{suffix}" if suffix else _ordinal(int(digits))
        return f"{label} Judicial District"
    m = re.match(r"^(2nd)\s+(\d+)$", num)
    if m:
        return f"2nd {_ordinal(int(m.group(2)))} Judicial District"
    return f"{num} Judicial District"


def oxford(items):
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} & {items[1]}"
    return ", ".join(items[:-1]) + f" & {items[-1]}"


ORDINAL_SLUG = {
    1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th", 7: "7th",
    8: "8th", 9: "9th", 10: "10th", 11: "11th", 12: "12th", 13: "13th", 14: "14th",
}
ORDINAL_NAME = {
    1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth", 6: "Sixth", 7: "Seventh",
    8: "Eighth", 9: "Ninth", 10: "Tenth", 11: "Eleventh", 12: "Twelfth", 13: "Thirteenth", 14: "Fourteenth",
}


class Recorder:
    def __init__(self, write):
        self.write = write
        self.stats = {}

    def emit(self, subdir, doc, filename, header):
        path = DATA_DIR / "jurisdictions" / subdir / filename
        if path.exists():
            existing = yaml.safe_load(path.read_text()) or {}
            if existing.get("id") == doc["id"]:
                self.stats[f"{subdir}_existing"] = self.stats.get(f"{subdir}_existing", 0) + 1
            else:
                self.stats[f"{subdir}_skipped_filename_conflict"] = (
                    self.stats.get(f"{subdir}_skipped_filename_conflict", 0) + 1
                )
            return
        self.stats[f"{subdir}_new"] = self.stats.get(f"{subdir}_new", 0) + 1
        if self.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            text = header + yaml.safe_dump(
                doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000
            )
            path.write_text(text)


def build_judicial_district_jurisdictions(rec, known_counties):
    raw = json.loads((SRC_DIR / "district-courts-by-county-2026-05-01.json").read_text())

    from collections import defaultdict
    combos = defaultdict(list)
    for entry in raw:
        counties = entry["counties"]
        if len(counties) < 2:
            continue  # single-county: reuses the existing county jurisdiction, no new file
        for c in counties:
            if county_slug(c) not in known_counties:
                raise SystemExit(f"Unresolved county {c!r} in judicial district {entry['num']}")
        combos[tuple(counties)].append(entry["num"])

    header = (
        "# Added for issue #26: a multi-county judicial district jurisdiction.\n"
        "# One or more numbered District Courts (see `identifiers`) sit inside this\n"
        "# exact county combination -- jurisdiction represents the shared geography,\n"
        "# not any single numbered court. Source: OCA's \"District Judges by\n"
        "# Judicial District\" directory (see script docstring for the currency\n"
        "# caveat on which source was and wasn't used).\n"
    )

    for counties, nums in sorted(combos.items()):
        slug = "-".join(county_slug(c) for c in counties)
        jid = f"ocd-jurisdiction/country:us/state:tx/judicial_district:{slug}/judiciary"
        did = f"ocd-division/country:us/state:tx/judicial_district:{slug}"
        doc = {
            "id": jid,
            "name": f"{oxford(list(counties))} Counties Judicial District",
            "state": "tx",
            "division_id": did,
            "classification": "judiciary",
            "identifiers": [
                {"scheme": "tx-judicial-district", "identifier": ordinal_district_label(n)} for n in nums
            ],
            "sources": [DISTRICT_COURT_SOURCE],
        }
        rec.emit("judicial-district", doc, f"{slug}.yaml", header)

    return len(combos), sum(len(v) for v in combos.values())


def build_appellate_district_jurisdictions(rec, known_counties):
    raw = json.loads((SRC_DIR / "appellate-districts-by-county-govcode-22.201.json").read_text())

    header = (
        "# Added for issue #26: a Texas Court of Appeals district. Source: Tex.\n"
        "# Gov't Code Sec. 22.201, current through the 2023 redistricting -- see\n"
        "# the script docstring for why a 2005 OCA county map was rejected as a\n"
        "# source. The 15th Court of Appeals is deliberately excluded: Sec.\n"
        "# 22.201(p) makes it statewide, so it belongs under\n"
        "# data/us/tx/jurisdictions/state/tx-judiciary.yaml instead of a new\n"
        "# per-district jurisdiction.\n"
    )

    count = 0
    for num_str, counties in raw.items():
        num = int(num_str)
        if num == 15:
            continue
        for c in counties:
            if county_slug(c) not in known_counties:
                raise SystemExit(f"Unresolved county {c!r} in Court of Appeals district {num}")
        slug = ORDINAL_SLUG[num]
        jid = f"ocd-jurisdiction/country:us/state:tx/appellate_district:{slug}/judiciary"
        did = f"ocd-division/country:us/state:tx/appellate_district:{slug}"
        doc = {
            "id": jid,
            "name": f"{ORDINAL_NAME[num]} Court of Appeals District",
            "state": "tx",
            "division_id": did,
            "classification": "judiciary",
            "identifiers": [
                {"scheme": "tx-appellate-district", "identifier": f"{ORDINAL_NAME[num]} Court of Appeals District"}
            ],
            "website": (f"https://www.txcourts.gov/{slug}coa" if num in (3, 13)
                        else f"https://www.txcourts.gov/{slug}coa.aspx"),
            "sources": [APPELLATE_SOURCE],
        }
        rec.emit("appellate-district", doc, f"{slug}.yaml", header)
        count += 1
    return count


# Multi-county judicial/prosecutorial entities that don't align with any
# numbered judicial district's own county set, discovered while parsing the
# 2024 SOS Winner Listing Report for issue #26's officer import (or, for
# the multicounty court-at-law, while filling in TX_Municipalities.xlsx's
# Judiciary sheet).
EXTRA_MULTICOUNTY_ENTITIES = [
    {
        # "DISTRICT ATTORNEY FOR KLEBERG AND KENEDY COUNTIES" covers only 2 of
        # the 3 counties the 105th Judicial District (Kenedy, Kleberg, Nueces)
        # serves -- Nueces elects its own separate 105th Judicial District DA.
        "slug": "kenedy-kleberg", "counties": ["Kenedy", "Kleberg"],
        "scheme": "tx-prosecutorial-district",
        "identifier": "District Attorney for Kleberg and Kenedy Counties",
        "sources": [
            {"url": "https://statutes.capitol.texas.gov/Docs/GV/htm/GV.43.htm#43.182",
             "note": "Tex. Gov't Code Sec. 43.182 (District Attorney for Kleberg and Kenedy Counties): "
                     "\"The voters of Kleberg and Kenedy Counties elect a district attorney... "
                     "and serves the district courts of Kleberg and Kenedy Counties.\""},
            {"url": "https://results.texas-election.com/reports",
             "note": "Texas SOS 2024 General Election Winner Listing Report, office title "
                     "\"District Attorney for Kleberg and Kenedy Counties\"."},
        ],
    },
    {
        # "2ND MULTICOUNTY COURT AT LAW" -- a Chapter 25 multicounty statutory
        # county court. Bee is the administrative county; Government Code
        # Chapter 25's per-county subchapters don't restate this court's own
        # creation/county list the way single-county courts get one, so this
        # is confirmed instead via two Texas Legislature documents that name
        # the court and all three counties together: SB1260 (89R, "relating
        # to the jurisdiction of the 2nd Multicounty Court at Law and the
        # composition of the juvenile boards of Bee, Live Oak, and McMullen
        # Counties") and SB2878's bill analysis (89R), which amends Human
        # Resources Code Secs. 152.0191(a) [Bee], 152.1551(a) [Live Oak], and
        # 152.1621(a) [McMullen] to each seat "the judge of the 2nd
        # Multicounty Court at Law" on that county's juvenile board.
        "slug": "bee-live-oak-mcmullen", "counties": ["Bee", "Live Oak", "McMullen"],
        "scheme": "tx-multicounty-court-at-law",
        "identifier": "2nd Multicounty Court at Law",
        "sources": [
            {"url": "https://trackbill.com/bill/texas-senate-bill-1260-relating-to-the-jurisdiction-of-the-2nd-multicounty-court-at-law-and-the-composition-of-the-juvenile-boards-of-bee-live-oak-and-mcmullen-counties/2660513/",
             "note": "TX SB1260 (89R), \"relating to the jurisdiction of the 2nd Multicounty Court at Law and "
                     "the composition of the juvenile boards of Bee, Live Oak, and McMullen Counties.\""},
            {"url": "https://capitol.texas.gov/tlodocs/89R/analysis/html/SB02878S.HTM",
             "note": "TX SB2878 (89R) bill analysis, Article 10 (Juvenile Boards): amends Human Resources Code "
                     "Secs. 152.0191(a), 152.1551(a), 152.1621(a) to seat \"the judge of the 2nd Multicounty "
                     "Court at Law\" on the Bee, Live Oak, and McMullen County juvenile boards respectively. "
                     "The court's own creating/jurisdiction-defining provision (likely Gov't Code Ch. 25, "
                     "Subchapter -- see 25.2601-.2607's generic \"Multicounty Statutory County Courts\" "
                     "template) was not independently pinned to an exact section number; flagged for anyone "
                     "who wants to firm up the citation further."},
            {"url": "https://results.texas-election.com/reports",
             "note": "Texas SOS 2024 General Election Winner Listing Report, office title "
                     "\"2ND MULTICOUNTY COURT AT LAW\"."},
        ],
    },
]


def build_extra_multicounty_jurisdictions(rec, known_counties):
    header = (
        "# Added for issue #26: a multi-county judicial/prosecutorial entity\n"
        "# whose county set does not match any numbered judicial district's own\n"
        "# territory -- see EXTRA_MULTICOUNTY_ENTITIES in the script for sourcing.\n"
    )
    for entry in EXTRA_MULTICOUNTY_ENTITIES:
        for c in entry["counties"]:
            if county_slug(c) not in known_counties:
                raise SystemExit(f"Unresolved county {c!r} in {entry['identifier']}")
        jid = f"ocd-jurisdiction/country:us/state:tx/judicial_district:{entry['slug']}/judiciary"
        did = f"ocd-division/country:us/state:tx/judicial_district:{entry['slug']}"
        doc = {
            "id": jid,
            "name": f"{oxford(entry['counties'])} Counties Judicial District",
            "state": "tx",
            "division_id": did,
            "classification": "judiciary",
            "identifiers": [{"scheme": entry["scheme"], "identifier": entry["identifier"]}],
            "sources": [{**s, "retrieved": RETRIEVED} for s in entry["sources"]],
        }
        rec.emit("judicial-district", doc, f"{entry['slug']}.yaml", header)
    return len(EXTRA_MULTICOUNTY_ENTITIES)


def load_known_counties():
    known = {}
    for f in (DATA_DIR / "jurisdictions" / "county").glob("*-government.yaml"):
        slug = f.stem[: -len("-government")]
        known[slug] = True
    return known


def main():
    write = "--write" in sys.argv[1:]
    known_counties = load_known_counties()
    rec = Recorder(write)

    n_combos, n_districts_covered = build_judicial_district_jurisdictions(rec, known_counties)
    n_appellate = build_appellate_district_jurisdictions(rec, known_counties)
    n_extra = build_extra_multicounty_jurisdictions(rec, known_counties)

    print(f"Judicial district jurisdictions: {n_combos} distinct multi-county combinations "
          f"covering {n_districts_covered} numbered District Courts")
    print(f"Appellate district jurisdictions: {n_appellate} (15th excluded -- statewide)")
    print(f"Extra multicounty jurisdictions (prosecutorial/court-at-law): {n_extra}")
    print()
    print("==================== SUMMARY ====================")
    for k in sorted(rec.stats):
        print(f"{k}: {rec.stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


if __name__ == "__main__":
    main()
