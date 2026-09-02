#!/usr/bin/env python3
"""
Mint the one joint jurisdiction the TX CAD structure pass needs: Potter/
Randall CAD is a single legal entity spanning two counties (Tax Code
6.01(a) normally establishes one CAD per county, but Potter and Randall
share one), so it doesn't fit either county's own jurisdiction file the
way the other 48 elected-seat CADs do. See issue #28 and
scripts/seed_tx_cad_organizations_posts.py, which depends on this having
already run.

Follows the same "mint a new division type subordinate to state when no
existing county/place id fits" precedent as the ISD/CCD jurisdiction
seeds (opencivicdata/ocd-division-ids#195):

  id:          ocd-jurisdiction/country:us/state:tx/appraisal_district:potter-randall/government
  division_id: ocd-division/country:us/state:tx/appraisal_district:potter-randall

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_cad_potter_randall_jurisdiction.py [--write]
"""
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx" / "jurisdictions" / "appraisal"
RETRIEVED = "2026-09-02"

DOC = {
    "id": "ocd-jurisdiction/country:us/state:tx/appraisal_district:potter-randall/government",
    "name": "Potter/Randall Appraisal District",
    "state": "tx",
    "division_id": "ocd-division/country:us/state:tx/appraisal_district:potter-randall",
    "classification": "government",
    "website": "http://www.prad.org",
    "sources": [
        {
            "url": "https://taad.org/resources/texas-cad-websites/",
            "note": (
                "TAAD's Texas CAD website directory lists \"Potter/Randall "
                "CAD\" as a single entity serving both counties (Tax Code "
                "6.01(a) normally establishes one appraisal district per "
                "county; Potter and Randall are the one pair that shares "
                "a joint district). Both counties individually cross the "
                "75,000-population elected-seat threshold (Tax Code "
                "6.0301): Potter 118,525, Randall 140,753 (2020 Census)."
            ),
            "retrieved": RETRIEVED,
        }
    ],
}

HEADER = (
    "# Seeded from the TX Appraisal District rolling audit (issue #28) by\n"
    "# scripts/seed_tx_cad_potter_randall_jurisdiction.py. The one CAD in\n"
    "# the elected-seat scope that spans two counties, so it doesn't fit\n"
    "# either county's own jurisdiction file the way the other 48 do.\n"
)


def main():
    write = "--write" in sys.argv[1:]
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / "potter-randall-appraisal-government.yaml"
    if path.exists():
        print("already exists, not overwriting:", path)
        return
    if write:
        path.write_text(
            HEADER + yaml.safe_dump(DOC, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
        )
        print("wrote", path)
    else:
        print("(dry run -- pass --write to create the file)")
        print(yaml.safe_dump(DOC, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000))


if __name__ == "__main__":
    main()
