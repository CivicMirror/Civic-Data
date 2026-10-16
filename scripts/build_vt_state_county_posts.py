#!/usr/bin/env python3
"""Build Vermont state-executive and county posts for issue #163.

Structure only -- no officeholders are imported by this script.
Model: scripts/build_ms_county_officers.py (issue #36) and the
Mississippi state-office pass (issue #68).

Vermont scope decisions (see reference/VT Rolling Audit/
VT_State_and_County_Offices.md):
- Statewide executive: the six offices elected statewide every two
  years (Governor, Lieutenant Governor, Secretary of State, Attorney
  General, State Treasurer, Auditor of Accounts).
- County: the offices elected per county every four years --
  State's Attorney, Sheriff, Assistant Judge (2 seats), High Bailiff.
- HELD: Judge of Probate. Vermont has 18 probate districts, not 14;
  they do not map 1:1 onto counties, so probate posts wait for the
  official district enumeration from the Vermont Judiciary.
- EXCLUDED as appointed: County Clerk (24 V.S.A. section 171,
  appointment), County Treasurer (24 V.S.A. section 211, appointment),
  and all state judges other than Assistant Judges / Probate Judges
  (appointed by the Governor with Senate consent; retention by the
  General Assembly -- Vt. Const. Ch. II sections 32-34).
- Legislative districts (House 150 seats, Senate 30 seats) are a
  separate pass from the official apportionment lists.

Idempotent: never overwrites an existing file. Dry run by default;
pass --write to create files.
"""
import sys
import uuid
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "vt"
RETRIEVED = "2026-10-16"

NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")

HEADER = (
    "# State and county elected office structure; issue #163\n"
    "# (VT master tracking). No officeholders imported.\n"
)

MEMO_URL = (
    "https://legislature.Vermont.gov/Documents/2024/WorkGroups/Senate%20Judiciary/"
    "Bills/PR.1/Drafts,%20Amendments,%20Legal%20Documents/PR.1~Tim%20Devlin~"
    "Memorandum-%20Removal%20of%20Elected%20County%20Officers%20from%20Office~2-20-2024.pdf"
)
MEMO_NOTE = (
    "Legislative Counsel memorandum (2024-02-20) enumerating Vermont's "
    "constitutional officers: Governor, Lieutenant Governor, Secretary of "
    "State, Treasurer, Auditor of Accounts, State's Attorneys, Sheriffs, "
    "High Bailiffs, Judges of Probate, and Assistant Judges."
)
INTRO_URL = (
    "https://legislature.Vermont.gov/Documents/2022/WorkGroups/House%20"
    "Government%20Operations/Introduction%20to%20Government%20Operations/"
    "W~Amerin%20Aborjaily~Introduction%20to%20Government%20Operations~1-8-2021.pdf"
)
INTRO_NOTE = (
    "Vermont General Assembly, House Government Operations introduction: "
    "constitutional officers and the biennial election cycle."
)
COUNTY_STATUTE_URL = "https://legislature.Vermont.gov/statutes/chapter/24/005"
COUNTY_STATUTE_NOTE = (
    "Vermont Statutes Online, Title 24 chapter 5 (County Officers): "
    "Assistant Judges at subchapter 1, Sheriffs at subchapter 5. County "
    "Clerk (subchapter 2, section 171) and County Treasurer (subchapter 3, "
    "section 211) are appointed, not elected, and are excluded."
)

EXEC_SOURCES = [
    {"url": MEMO_URL, "note": MEMO_NOTE, "retrieved": RETRIEVED},
    {"url": INTRO_URL, "note": INTRO_NOTE, "retrieved": RETRIEVED},
]
COUNTY_SOURCES = [
    {"url": COUNTY_STATUTE_URL, "note": COUNTY_STATUTE_NOTE, "retrieved": RETRIEVED},
    {"url": MEMO_URL, "note": MEMO_NOTE, "retrieved": RETRIEVED},
]

# (slug, org name, post title)
EXEC_OFFICES = [
    ("governor", "Vermont Office of the Governor", "Governor"),
    ("lieutenant-governor", "Vermont Office of the Lieutenant Governor", "Lieutenant Governor"),
    ("secretary-of-state", "Vermont Office of the Secretary of State", "Secretary of State"),
    ("attorney-general", "Vermont Office of the Attorney General", "Attorney General"),
    ("state-treasurer", "Vermont Office of the State Treasurer", "State Treasurer"),
    ("auditor-of-accounts", "Vermont Office of the Auditor of Accounts", "Auditor of Accounts"),
]

# (slug, post title, seats)
COUNTY_OFFICES = [
    ("states-attorney", "State's Attorney", 1),
    ("sheriff", "Sheriff", 1),
    ("assistant-judge", "Assistant Judge", 2),
    ("high-bailiff", "High Bailiff", 1),
]

EXEC_JURISDICTION_ID = "ocd-jurisdiction/country:us/state:vt/executive"


def oid(kind, key):
    return f"ocd-{kind}/{uuid.uuid5(NS, kind + '|' + key)}"


def dump(path, doc, write):
    if path.exists():
        print(f"SKIP exists: {path.relative_to(REPO)}")
        return False
    print(f"{'WRITE' if write else 'WOULD WRITE'}: {path.relative_to(REPO)}")
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(HEADER + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))
    return True


def main():
    write = "--write" in sys.argv
    created = 0

    # Statewide executive jurisdiction (pattern: ms-executive.yaml)
    jur = {
        "id": EXEC_JURISDICTION_ID,
        "name": "Vermont Executive Branch",
        "state": "vt",
        "division_id": "ocd-division/country:us/state:vt",
        "classification": "executive",
        "sources": EXEC_SOURCES,
    }
    created += dump(DATA_DIR / "jurisdictions" / "state" / "vt-executive.yaml", jur, write)

    for slug, org_name, title in EXEC_OFFICES:
        org_id = oid("organization", f"vt|state|{slug}")
        org = {
            "id": org_id,
            "name": org_name,
            "jurisdiction_id": EXEC_JURISDICTION_ID,
            "identifiers": [],
            "sources": EXEC_SOURCES,
        }
        created += dump(DATA_DIR / "organizations" / "state" / f"vt-{slug}.yaml", org, write)
        post = {
            "id": f"vt/{slug}",
            "organization_id": org_id,
            "title": title,
            "seats": 1,
            "sources": EXEC_SOURCES,
        }
        created += dump(DATA_DIR / "posts" / "state" / f"vt-{slug}.yaml", post, write)

    county_dir = DATA_DIR / "jurisdictions" / "county"
    counties = []
    for f in sorted(county_dir.glob("*-government.yaml")):
        doc = yaml.safe_load(f.read_text()) or {}
        slug = f.stem[: -len("-government")]
        counties.append((slug, doc["id"], doc["name"]))
    if len(counties) != 14:
        sys.exit(f"Expected 14 county jurisdictions, found {len(counties)}")

    for slug, jur_id, county_name in counties:
        for office_slug, title, seats in COUNTY_OFFICES:
            post_id = f"{slug}-vt-county/{office_slug}"
            org_id = oid("organization", f"vt|county|{post_id}")
            org_name = f"{county_name} {title}"
            org = {
                "id": org_id,
                "name": org_name,
                "jurisdiction_id": jur_id,
                "identifiers": [{"scheme": "civicmirror-office", "identifier": post_id}],
                "status": "active",
                "sources": COUNTY_SOURCES,
            }
            created += dump(
                DATA_DIR / "organizations" / "county" / f"{slug}-vt-county-{office_slug}.yaml",
                org, write)
            post = {
                "id": post_id,
                "organization_id": org_id,
                "title": title,
                "seats": seats,
                "sources": COUNTY_SOURCES,
            }
            created += dump(
                DATA_DIR / "posts" / "county" / f"{slug}-vt-county-{office_slug}.yaml",
                post, write)

    print(f"{'Created' if write else 'Would create'} {created} files "
          f"(1 jurisdiction, {len(EXEC_OFFICES)} state orgs + {len(EXEC_OFFICES)} state posts, "
          f"{len(counties) * len(COUNTY_OFFICES)} county orgs + "
          f"{len(counties) * len(COUNTY_OFFICES)} county posts).")


if __name__ == "__main__":
    main()
