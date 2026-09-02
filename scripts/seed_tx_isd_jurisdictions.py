#!/usr/bin/env python3
"""
Seed data/us/tx/jurisdictions/school/ from the TX ISD rolling audit's TEA
enumeration (see issue #13 and reference/TX Rolling Audit/Audit_Instructions.md
Phase 3).

This is the blocking prerequisite flagged in #13: office/Post research for
Texas ISDs cannot mint IDs against an unseeded jurisdiction slug, and no ISD
jurisdiction files exist yet (data/us/tx/jurisdictions/ currently only has
county/, municipal/, federal/).

Source: the two TEA-derived CSVs already committed to this branch from the
TASB<->TEA crosswalk work --
  tx_isd_tasb_tea_crosswalk_2026-08-23.csv   (1,002 districts matched to a
                                               TASB Policy Online page)
  tx_isd_tea_unmatched_2026-08-23.csv        (11 districts verified as real,
                                               independently-elected ISDs
                                               with no TASB page found)
together these are the full ~1,014 "real Texas ISD" universe established in
that work (TEA's raw INDEPENDENT-type export, minus the 6 rows independently
confirmed to be non-ISD entities -- university lab schools, TDCJ's Windham
School District -- see tx_isd_tea_excluded_non_isd_2026-08-23.csv).

This script seeds ENUMERATION ONLY: id, name, division_id, classification,
sources. It deliberately does NOT set `government_form`, `website`, or
`election_authority` -- board size/structure (statutory default vs.
single-member/hybrid plan) and each district's official site are individual
per-district verification, the actual Phase 3 office-research work this
jurisdiction seed unblocks, not something to assert in bulk here.

Division/jurisdiction ID: ISDs are not coextensive with any place or county
boundary (a district can serve parts of several), so there is no existing
OCD place/county id to key off of -- same situation as MA's district-attorney
jurisdictions (see data/us/ma/jurisdictions/*/*.yaml for that precedent).
Following that precedent (mint a new division type subordinate to state when
no county/place id fits; opencivicdata/ocd-division-ids#195), this mints:

  id:          ocd-jurisdiction/country:us/state:tx/school_district:<slug>/school
  division_id: ocd-division/country:us/state:tx/school_district:<slug>

<slug> is derived from the TEA district name with its trailing district-type
acronym (ISD, CISD, or MSD) stripped. 11 district names are not unique across
the 1,013 (e.g. two "Big Sandy ISD"); those are disambiguated by appending the
district's TEA CDN (County-District Number, itself unique) rather than
guessing county names -- the committed crosswalk CSVs don't carry a county
column through to the final output.

Idempotent by id -- never overwrites an existing file with the same id.
Note this idempotency is batch-relative: "no name collision" is computed from
the current run's CSVs, not from what's already on disk. If a future TEA pull
introduces a same-named district that wasn't in this batch, its slug won't
collide with anything seen this run, so it gets a bare slug even though an
existing file might already claim a different disambiguated slug for the
"other" same-named district -- re-check for new collisions by name (not just
by id) before re-running against an updated source. The schema has no field
to store the CDN, so idempotency can't be keyed on it directly.

Usage: python3 seed_tx_isd_jurisdictions.py [--write]
"""
import csv
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx" / "jurisdictions" / "school"
SRC_DIR = REPO / "reference" / "TX Rolling Audit"
RETRIEVED = "2026-08-23"

TEA_ASKTED_URL = "https://tealprod.tea.state.tx.us/Tea.AskTed.Web/Forms/SearchScreen.aspx?orgType=District"


def slugify(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def load_csv(name):
    with (SRC_DIR / name).open(newline="") as f:
        return list(csv.DictReader(f))


ACRONYMS = {"ISD", "CISD", "MSD"}


def strip_district_type(tea_name):
    words = tea_name.split()
    while words and words[-1] in ACRONYMS:
        words.pop()
    return " ".join(words)


def display_name(tea_name):
    # TEA names are ALL CAPS (e.g. "ELKHART ISD", "BURNET CISD", "STAFFORD
    # MSD"); title-case them but keep district-type acronyms as acronyms
    # (not "Isd"/"Cisd"/"Msd"), and fix str.title()'s Mc/Mac mangling
    # ("MCALLEN" -> "Mcallen" -> "McAllen").
    words = []
    for w in tea_name.split():
        if w in ACRONYMS:
            words.append(w)
            continue
        cased = w.title()
        # "Mac"-prefix capitalization (e.g. "MacGregor") isn't handled here --
        # no TX ISD name in this dataset starts with MAC (verified against the
        # source CSVs), only genuine "Mc" surnames, so a "Mac" rule would just
        # be an untested guess (and a wrong one for a name like "Mack").
        m = re.match(r"^Mc([a-z])(.*)$", cased)
        if m:
            cased = "Mc" + m.group(1).upper() + m.group(2)
        words.append(cased)
    return " ".join(words)


def main():
    write = "--write" in sys.argv[1:]

    matched = load_csv("tx_isd_tasb_tea_crosswalk_2026-08-23.csv")
    unmatched = load_csv("tx_isd_tea_unmatched_2026-08-23.csv")

    districts = [
        {"cdn": r["tea_cdn"], "name": r["tea_district_name"], "tasb_url": r["tasb_url"]}
        for r in matched
    ] + [
        {"cdn": r["tea_cdn"], "name": r["tea_district_name"], "tasb_url": None}
        for r in unmatched
    ]

    base_slugs = Counter(slugify(strip_district_type(d["name"])) for d in districts)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    existing_ids = set()
    for f in DATA_DIR.glob("*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            existing_ids.add(doc["id"])

    stats = Counter()
    for d in districts:
        base_slug = slugify(strip_district_type(d["name"]))
        slug = base_slug if base_slugs[base_slug] == 1 else f"{base_slug}-{d['cdn']}"

        doc_id = f"ocd-jurisdiction/country:us/state:tx/school_district:{slug}/school"
        if doc_id in existing_ids:
            stats["existing"] += 1
            continue

        sources = [
            {
                "url": TEA_ASKTED_URL,
                "note": (
                    f"Texas Education Agency AskTED district directory -- "
                    f"District Staff export, County-District Number {d['cdn']}, "
                    f"\"{d['name']}\". Enumeration only; board size/structure "
                    f"and official site not yet individually verified."
                ),
                "retrieved": RETRIEVED,
            }
        ]
        if d["tasb_url"]:
            sources.append(
                {
                    "url": d["tasb_url"],
                    "note": (
                        f"TASB Policy Online page for this district (matched to "
                        f"TEA CDN {d['cdn']} via this repo's TASB<->TEA crosswalk); "
                        f"source for the district's BBB(LOCAL) election-method "
                        f"policy in later Phase 3 office research."
                    ),
                    "retrieved": RETRIEVED,
                }
            )

        doc = {
            "id": doc_id,
            "name": display_name(d["name"]),
            "state": "tx",
            "division_id": f"ocd-division/country:us/state:tx/school_district:{slug}",
            "classification": "school",
            "sources": sources,
        }

        stats["new"] += 1
        if write:
            path = DATA_DIR / f"{slug}-school.yaml"
            header = (
                "# Seeded from the TX ISD rolling audit's TEA enumeration by\n"
                "# scripts/seed_tx_isd_jurisdictions.py (see issue #13). Board\n"
                "# size/structure and official site are individually verified in\n"
                "# later Phase 3 office research, not asserted here.\n"
            )
            text = header + yaml.safe_dump(
                doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000
            )
            path.write_text(text)

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


if __name__ == "__main__":
    main()
