#!/usr/bin/env python3
"""Vermont Governor -- step 1 of the new build order (issue #163).

Walter's build order for Vermont (2026-10-16): build one post at a
time and backfill its holder (person + membership) in the same step,
starting at the state level with the Governor and working down --
instead of the MA/MS pattern of standing up all structure first and
backfilling people in a separate later phase.

The Governor post and organization already exist (PR #165, built
structure-first before this order). This step completes the unit:
person + 2024 general election record + membership.

Verified (retrieved 2026-10-16), official sources only:
- Vermont Secretary of State, Elections Division, Official Report of
  the Canvassing Committee for United States and Vermont Statewide
  Offices, General Election November 5, 2024 (canvassed under
  17 V.S.A. sections 2368-2371): for Governor, Phil Scott* 266,439
  votes, ahead of Esther Charlestin (79,217), Kevin Hoyt (9,368),
  June Goodband (4,512), Eli "Poa" Mutino (2,414) and write-ins
  (891). The asterisk marks the winner in the report.
- The official site of the Office of Governor Phil Scott
  (governor.vermont.gov) confirms Scott as the sitting Governor.
- Scott's party (Republican) is as printed in the Elections
  Division's Official Returns of Votes for the same election; the
  canvass report itself does not print party labels.

Conventions follow the VT municipal build: person id uuid5 under the
project namespace scoped "vt|state|<slug>", membership id = post
file slug + person slug, candidacy status "active" for the seated
winner (the win itself is recorded on the election contest). No term
starts or ends are recorded; no source consulted states them as
fields -- the 2024 election year lives in the source notes. The
November 3, 2026 general election decides the next term.

Factory concordance: the VT Jurisdiction Factory covers municipal
jurisdictions only -- it has no state tier, so there is no factory
record to reconcile for this step.

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

JURISDICTION_ID = "ocd-jurisdiction/country:us/state:vt/executive"
POST_ID = "vt/governor"
ORG_ID = "ocd-organization/1fa187c6-d72f-5de7-b718-d3f69bcb5133"
ELECTION_ID = "vt/2024-11-05/general"
CONTEST_ID = "vt/2024-11-05/governor"

CANVASS_URL = (
    "https://outside.vermont.gov/dept/sos/Elections_Division/"
    "election_info_resources/elections_results_data/"
    "2024_general_election_official_report_canvassing_committee_"
    "united_states_vermont_statewide_offices.pdf"
)
OFFICE_URL = "http://governor.vermont.gov/contact-us-requests"

CANVASS_SOURCE = {
    "url": CANVASS_URL,
    "note": (
        "Vermont Secretary of State, Elections Division, Official "
        "Report of the Canvassing Committee -- United States and "
        "Vermont Statewide Offices, General Election, November 5, "
        "2024 (canvassed under 17 V.S.A. sections 2368-2371). For "
        "Governor: Phil Scott* 266,439 votes; Esther Charlestin "
        "79,217; Kevin Hoyt 9,368; June Goodband 4,512; Eli \"Poa\" "
        "Mutino 2,414; write-in 891. The asterisk marks the winner "
        "in the report. Party labels are not printed in the canvass "
        "report; Scott's Republican affiliation is as printed in "
        "the Elections Division's Official Returns of Votes for "
        "the same election. The 2024 winners took office at the "
        "January 2025 inauguration; the November 3, 2026 general "
        "election decides the next term."
    ),
    "retrieved": RETRIEVED,
}

OFFICE_SOURCE = {
    "url": OFFICE_URL,
    "note": (
        "Official site of the Office of Governor Phil Scott "
        "(governor.vermont.gov): 'Executive Office of Governor "
        "Phil Scott', Pavilion Building, 109 State Street, "
        "Montpelier -- confirms Scott as the sitting Governor as "
        "of the retrieval date."
    ),
    "retrieved": RETRIEVED,
}


def oid(kind, key):
    return f"ocd-{kind}/{uuid.uuid5(NS, kind + '|' + key)}"


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
    person_id = oid("person", "vt|state|phil-scott")

    header = ("# Vermont Governor -- step 1 of the build order "
              "(post + holder together);\n# issue #163 (VT master "
              "tracking).\n")

    person = {
        "id": person_id,
        "name": "Phil Scott",
        "identifiers": [],
        "candidacies": [
            {
                "contest_id": CONTEST_ID,
                "election_id": ELECTION_ID,
                "jurisdiction_id": JURISDICTION_ID,
                "office_id": POST_ID,
                "party": "Republican",
                "ballot_name": "Phil Scott",
                "status": "active",
            }
        ],
        "verification": {
            "status": "machine-extracted",
            "reviewed_on": RETRIEVED,
            "pipeline": "build_vt_governor",
        },
        "sources": [CANVASS_SOURCE, OFFICE_SOURCE],
    }
    created += dump(DATA_DIR / "people" / "state" / "phil-scott.yaml",
                    person, header, write)

    election = {
        "id": ELECTION_ID,
        "name": "Vermont 2024-11-05 general election",
        "date": "2024-11-05",
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
                "winners": [{"person_id": person_id, "name": "Phil Scott"}],
            }
        ],
        "sources": [CANVASS_SOURCE],
    }
    created += dump(
        DATA_DIR / "elections" / "vt--2024-11-05--governor.yaml",
        election,
        "# Vermont Governor election, November 5, 2024;\n"
        "# issue #163 (VT master tracking).\n",
        write)

    membership = {
        "id": "vt-governor-phil-scott",
        "person_id": person_id,
        "organization_id": ORG_ID,
        "post_id": POST_ID,
        "role": "Governor",
        "how_seated": "elected",
        "sources": [CANVASS_SOURCE, OFFICE_SOURCE],
    }
    created += dump(
        DATA_DIR / "memberships" / "state" / "vt-governor-phil-scott.yaml",
        membership, header, write)

    print(f"{'Created' if write else 'Would create'} {created} files "
          f"(1 person, 1 election, 1 membership; post {POST_ID} "
          f"already existed from PR #165).")


if __name__ == "__main__":
    main()
