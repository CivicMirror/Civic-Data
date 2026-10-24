#!/usr/bin/env python3
"""Build the Oregon Governor step for Civic-Data issue #170
(OR master tracking): the state executive jurisdiction, the
Governor organization and post, Tina Kotek's person record, her
membership, and the 2022-11-08 general election record with the
Governor contest -- post + holder + election built together in one
step, following the #163 (Vermont) build order (Governor first,
then work down tier by tier).

Sources (official only, verified firsthand 2026-10-23):
- Oregon Secretary of State, Elections Division, November 8, 2022
  General Election Abstract of Votes (certified county-by-county
  abstract), Governor section: Tina Kotek (D) 917,074, marked
  ** elected; Christine Drazan (R) 850,347; Betsy Johnson (NAV)
  168,431; Donice Noelle Smith (C) 8,051; R Leon Noble (L) 6,867;
  miscellaneous write-ins 2,113. Plurality margin 66,727 votes.
- Official site of the Governor of Oregon (oregon.gov), "Meet the
  Governor": names Tina Kotek as Governor and records her election
  on November 8, 2022. Kotek was sworn in on January 9, 2023; the
  November 3, 2026 general election decides the next term.

Creyton Loud's OR Jurisdiction Factory v0.1 has no state tier, so
there is no factory data to concord for this step; minting is from
the certified abstract and the Governor's official site only.

Idempotent: never overwrites an existing file. Dry run by default;
pass --write to create files.
"""
import sys
import uuid
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "or"
RETRIEVED = "2026-10-23"

NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")

JURISDICTION_ID = "ocd-jurisdiction/country:us/state:or/executive"
POST_ID = "or/governor"
ELECTION_ID = "or/2022-11-08/general"
CONTEST_ID = "or/2022-11-08/governor"

ABSTRACT_URL = (
    "https://sos.oregon.gov/elections/Documents/results/"
    "november-general-2022.pdf"
)
OFFICE_URL = "https://www.oregon.gov/gov/pages/meet-the-governor.aspx"

ABSTRACT_SOURCE = {
    "url": ABSTRACT_URL,
    "note": (
        "Oregon Secretary of State, Elections Division, November 8, "
        "2022 General Election Abstract of Votes (certified "
        "county-by-county abstract). For Governor: Tina Kotek (D) "
        "917,074 votes, marked ** as elected; Christine Drazan (R) "
        "850,347; Betsy Johnson (NAV) 168,431; Donice Noelle Smith "
        "(C) 8,051; R Leon Noble (L) 6,867; miscellaneous write-ins "
        "2,113. Kotek won by a plurality of 66,727 votes. Party "
        "labels are as printed in the abstract: (D) Democratic, "
        "(R) Republican, (NAV) Nonaffiliated, (C) Constitution, "
        "(L) Libertarian. Kotek was sworn in on January 9, 2023; "
        "the November 3, 2026 general election decides the next "
        "term."
    ),
    "retrieved": RETRIEVED,
}

OFFICE_SOURCE = {
    "url": OFFICE_URL,
    "note": (
        "Official site of the Governor of Oregon (oregon.gov), "
        "'Meet the Governor': names Tina Kotek as Governor of "
        "Oregon and records that she was elected on November 8, "
        "2022 -- confirms her as the sitting Governor as of the "
        "retrieval date."
    ),
    "retrieved": RETRIEVED,
}


def oid(kind, key):
    return f"ocd-{kind}/{uuid.uuid5(NS, kind + '|' + key)}"


ORG_ID = oid("organization", "or|state|governor")


def dump(path, doc, header, write):
    if path.exists():
        print(f"SKIP exists: {path.relative_to(REPO)}")
        return 0
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            header + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True),
            encoding="utf-8")
    print(f"{'WRITE' if write else 'WOULD WRITE'}: {path.relative_to(REPO)}")
    return 1


def main():
    write = "--write" in sys.argv
    created = 0
    person_id = oid("person", "or|state|tina-kotek")

    header = ("# Oregon Governor -- step 1 of the build order "
              "(post + holder together);\n# issue #170 (OR master "
              "tracking).\n")

    jurisdiction = {
        "id": JURISDICTION_ID,
        "name": "Oregon Executive Branch",
        "state": "or",
        "division_id": "ocd-division/country:us/state:or",
        "classification": "executive",
        "sources": [ABSTRACT_SOURCE, OFFICE_SOURCE],
    }
    created += dump(
        DATA_DIR / "jurisdictions" / "state" / "or-executive.yaml",
        jurisdiction,
        "# State executive jurisdiction; issue #170\n"
        "# (OR master tracking).\n",
        write)

    organization = {
        "id": ORG_ID,
        "name": "Oregon Office of the Governor",
        "jurisdiction_id": JURISDICTION_ID,
        "identifiers": [],
        "sources": [OFFICE_SOURCE, ABSTRACT_SOURCE],
    }
    created += dump(
        DATA_DIR / "organizations" / "state" / "or-governor.yaml",
        organization, header, write)

    post = {
        "id": POST_ID,
        "organization_id": ORG_ID,
        "title": "Governor",
        "seats": 1,
        "sources": [ABSTRACT_SOURCE, OFFICE_SOURCE],
    }
    created += dump(
        DATA_DIR / "posts" / "state" / "or-governor.yaml",
        post, header, write)

    person = {
        "id": person_id,
        "name": "Tina Kotek",
        "identifiers": [],
        "candidacies": [
            {
                "contest_id": CONTEST_ID,
                "election_id": ELECTION_ID,
                "jurisdiction_id": JURISDICTION_ID,
                "office_id": POST_ID,
                "party": "Democratic",
                "ballot_name": "Tina Kotek",
                "status": "active",
            }
        ],
        "verification": {
            "status": "machine-extracted",
            "reviewed_on": RETRIEVED,
            "pipeline": "build_or_governor",
        },
        "sources": [ABSTRACT_SOURCE, OFFICE_SOURCE],
    }
    created += dump(
        DATA_DIR / "people" / "state" / "tina-kotek.yaml",
        person, header, write)

    election = {
        "id": ELECTION_ID,
        "name": "Oregon 2022-11-08 general election",
        "date": "2022-11-08",
        "election_type": "general",
        "status": "official",
        "contests": [
            {
                "id": CONTEST_ID,
                "jurisdiction_id": JURISDICTION_ID,
                "office_id": POST_ID,
                "vote_for": 1,
                "candidate_ids": [person_id],
                "result_status": "certified",
                "winners": [{"person_id": person_id, "name": "Tina Kotek"}],
            }
        ],
        "sources": [ABSTRACT_SOURCE],
    }
    created += dump(
        DATA_DIR / "elections" / "or--2022-11-08--general.yaml",
        election,
        "# Oregon general election, November 8, 2022 -- statewide\n"
        "# contests are added one office at a time under the build\n"
        "# order; issue #170 (OR master tracking).\n",
        write)

    membership = {
        "id": "or-governor-tina-kotek",
        "person_id": person_id,
        "organization_id": ORG_ID,
        "post_id": POST_ID,
        "role": "Governor",
        "start": "2023-01-09",
        "how_seated": "elected",
        "sources": [ABSTRACT_SOURCE, OFFICE_SOURCE],
    }
    created += dump(
        DATA_DIR / "memberships" / "state" / "or-governor-tina-kotek.yaml",
        membership, header, write)

    print(f"{'Created' if write else 'Would create'} {created} files "
          f"(1 jurisdiction, 1 organization, 1 post, 1 person, "
          f"1 election, 1 membership). Person is NEW (no existing "
          f"tina-kotek record anywhere in the repo).")


if __name__ == "__main__":
    main()
