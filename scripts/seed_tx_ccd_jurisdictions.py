#!/usr/bin/env python3
"""
Seed data/us/tx/jurisdictions/school/ (community-college rows) from the TX
CCD rolling audit's THECB enumeration (see issue #14).

Blocking prerequisite for #14, same shape as #13's ISD jurisdiction seed:
office/Post research for Texas community/junior college districts cannot
mint IDs against an unseeded jurisdiction slug.

Source: reference/TX Rolling Audit/tx_ccd_thecb_enumeration_2026-09-02.csv,
the 50-district canonical list derived from THECB's 2025 almanac (2-Year
sheet), grouped by the almanac's "District" column (falling back to the
institution's own name for single-campus districts) with Texas State
Technical College's 7 statewide campuses and the 3 Lamar State/Lamar
Institute of Technology institutions excluded -- both are components of a
state university system (TSTC's own Board of Regents / the Texas State
University System Board of Regents), appointed rather than locally elected,
so they are not "community college districts" in the sense this issue
scopes (see feedback_verify_elected_status_claims: don't assume elected
without checking). This lands at exactly 50, matching the audit
instructions' "~50" estimate and reconciling closely against the 43/44-name
TASB Policy Online list already found in issue #14 (see
tx_ccd_tasb_crosswalk_2026-09-02.csv for the per-district TASB match, where
found).

This script seeds ENUMERATION ONLY: id, name, division_id, classification,
sources. It deliberately does NOT set `government_form`, `website`, or
`election_authority` -- board size/structure and each district's official
site are individual per-district verification, not asserted here (Texas
community college boards are NOT guaranteed to use ISD's 7-member default;
per the issue's own sourcing comment, confirm from the enabling
statute/election order, not by assumption).

Division/jurisdiction ID: CCDs are not coextensive with any place or county
boundary. Following the same precedent as TX ISDs (mint a new division type
subordinate to state when no county/place id fits; see
scripts/seed_tx_isd_jurisdictions.py and opencivicdata/ocd-division-ids#195):

  id:          ocd-jurisdiction/country:us/state:tx/community_college_district:<slug>/school
  division_id: ocd-division/country:us/state:tx/community_college_district:<slug>

<slug> comes from the CSV's own `slug` column (already stripped of
"Community College District" / "College" / etc. suffixes and disambiguated
by hand -- verified unique across all 50 rows before this script was
written).

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_ccd_jurisdictions.py [--write]
"""
import csv
import sys
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx" / "jurisdictions" / "school"
SRC_DIR = REPO / "reference" / "TX Rolling Audit"
CCD_CSV = SRC_DIR / "tx_ccd_thecb_enumeration_2026-09-02.csv"
TASB_CROSSWALK_CSV = SRC_DIR / "tx_ccd_tasb_crosswalk_2026-09-02.csv"
RETRIEVED = "2026-09-02"

THECB_ALMANAC_URL = "https://databridge.highered.texas.gov/almanac/"


def load_csv(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main():
    write = "--write" in sys.argv[1:]

    ccds = load_csv(CCD_CSV)
    tasb_by_fice = {}
    if TASB_CROSSWALK_CSV.exists():
        for r in load_csv(TASB_CROSSWALK_CSV):
            tasb_by_fice[r["thecb_fice"]] = r["tasb_url"]

    slugs = [r["slug"] for r in ccds]
    dupes = [s for s in slugs if slugs.count(s) > 1]
    if dupes:
        raise SystemExit(f"Duplicate slugs in {CCD_CSV}, fix before seeding: {sorted(set(dupes))}")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    existing_ids = set()
    for f in DATA_DIR.glob("*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            existing_ids.add(doc["id"])

    stats = Counter()
    for r in ccds:
        slug = r["slug"]
        doc_id = f"ocd-jurisdiction/country:us/state:tx/community_college_district:{slug}/school"
        if doc_id in existing_ids:
            stats["existing"] += 1
            continue

        sources = [
            {
                "url": THECB_ALMANAC_URL,
                "note": (
                    f"Texas Higher Education Coordinating Board 2025 Almanac "
                    f"(THECB_2025_almanac_data_01062026.xlsx, 2-Year sheet), "
                    f"FICE {r['thecb_fice']}, \"{r['name']}\" ({r['city']}). "
                    f"Enumeration only; board size/structure and official site "
                    f"not yet individually verified."
                ),
                "retrieved": RETRIEVED,
            }
        ]
        tasb_url = tasb_by_fice.get(r["thecb_fice"])
        if tasb_url:
            sources.append(
                {
                    "url": tasb_url,
                    "note": (
                        f"TASB Policy Online page for this district (matched to "
                        f"THECB FICE {r['thecb_fice']} via this repo's TASB<->THECB "
                        f"crosswalk); source for the district's BBB(LOCAL) "
                        f"election-method policy in later office research."
                    ),
                    "retrieved": RETRIEVED,
                }
            )

        doc = {
            "id": doc_id,
            "name": r["name"],
            "state": "tx",
            "division_id": f"ocd-division/country:us/state:tx/community_college_district:{slug}",
            "classification": "school",
            "sources": sources,
        }

        stats["new"] += 1
        if write:
            path = DATA_DIR / f"{slug}-ccd-school.yaml"
            header = (
                "# Seeded from the TX CCD rolling audit's THECB enumeration by\n"
                "# scripts/seed_tx_ccd_jurisdictions.py (see issue #14). Board\n"
                "# size/structure and official site are individually verified in\n"
                "# later office research, not asserted here.\n"
            )
            text = header + yaml.safe_dump(
                doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000
            )
            path.write_text(text)

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    print(f"tasb_matched: {sum(1 for r in ccds if r['thecb_fice'] in tasb_by_fice)}/{len(ccds)}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


if __name__ == "__main__":
    main()
