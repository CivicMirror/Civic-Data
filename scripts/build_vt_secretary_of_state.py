#!/usr/bin/env python3
"""Vermont Secretary of State -- step 3 of the new build order (#163).

Build order (Walter, 2026-10-16): one post at a time, holder built in
the same step, Governor first, working down. The vt/secretary-of-state
post already exists (PR #165). This step completes the unit: person +
Secretary of State contest on the 2024 general election record +
membership.

Verified (retrieved 2026-10-16), official sources:
- SOS Official Report of the Canvassing Committee, 2024 general
  election, section 7 (For Secretary of State): Sarah Copeland
  Hanzas* 205,378 votes; H. Brooke Paige 138,673; write-in 473 --
  an outright majority of the votes cast for the office, read
  firsthand from the report.
- The Secretary of State's own site (sos.vermont.gov) names her as
  the sitting Secretary of State in current office releases.
- Party (Democratic) is as printed in the Elections Division's
  Official Returns of Votes; the canvass report prints no labels.

No term dates are recorded as fields; the November 3, 2026 general
election decides the next term. Factory concordance: the factory
has no state tier.

Idempotent: person/membership are skipped if present; the election
contest is added only if absent. Dry run by default; --write to
create files.
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
POST_ID = "vt/secretary-of-state"
ORG_ID = "ocd-organization/f490bbac-a53d-5617-a525-a0534a7f706b"
ELECTION_ID = "vt/2024-11-05/general"
CONTEST_ID = "vt/2024-11-05/secretary-of-state"

CANVASS_URL = (
    "https://outside.vermont.gov/dept/sos/Elections_Division/"
    "election_info_resources/elections_results_data/"
    "2024_general_election_official_report_canvassing_committee_"
    "united_states_vermont_statewide_offices.pdf"
)
OFFICE_URL = ("https://sos.vermont.gov/secretarys-desk/"
              "commentary-press/archives-month-2026")

CANVASS_SOURCE = {
    "url": CANVASS_URL,
    "note": (
        "Vermont Secretary of State, Elections Division, Official "
        "Report of the Canvassing Committee -- United States and "
        "Vermont Statewide Offices, General Election, November 5, "
        "2024 (canvassed under 17 V.S.A. sections 2368-2371), "
        "section 7, For Secretary of State: Sarah Copeland "
        "Hanzas* 205,378 votes; H. Brooke Paige 138,673; write-in "
        "473. The asterisk marks the winner; Hanzas won an outright "
        "majority of the votes cast for the office. Party labels "
        "are not printed in the canvass report; Copeland Hanzas' "
        "Democratic affiliation is as printed in the Elections "
        "Division's Official Returns of Votes for the same "
        "election. The November 3, 2026 general election decides "
        "the next term."
    ),
    "retrieved": RETRIEVED,
}

OFFICE_SOURCE = {
    "url": OFFICE_URL,
    "note": (
        "Official site of the Vermont Secretary of State "
        "(sos.vermont.gov), office press release for Archives "
        "Month (October 2026): quotes 'Secretary Sarah Copeland "
        "Hanzas' -- names her as the sitting Secretary of State "
        "as of the retrieval date."
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
    person_id = oid("person", "vt|state|sarah-copeland-hanzas")

    header = ("# Vermont Secretary of State -- step 3 of the build "
              "order (post + holder together);\n# issue #163 (VT "
              "master tracking).\n")

    person = {
        "id": person_id,
        "name": "Sarah Copeland Hanzas",
        "identifiers": [],
        "candidacies": [
            {
                "contest_id": CONTEST_ID,
                "election_id": ELECTION_ID,
                "jurisdiction_id": JURISDICTION_ID,
                "office_id": POST_ID,
                "party": "Democratic",
                "ballot_name": "Sarah Copeland Hanzas",
                "status": "active",
            }
        ],
        "verification": {
            "status": "machine-extracted",
            "reviewed_on": RETRIEVED,
            "pipeline": "build_vt_secretary_of_state",
        },
        "sources": [CANVASS_SOURCE, OFFICE_SOURCE],
    }
    created += dump(
        DATA_DIR / "people" / "state" / "sarah-copeland-hanzas.yaml",
        person, header, write)

    election_path = DATA_DIR / "elections" / "vt--2024-11-05--general.yaml"
    election = yaml.safe_load(election_path.read_text(encoding="utf-8"))
    assert election["id"] == ELECTION_ID
    if not any(c["id"] == CONTEST_ID for c in election["contests"]):
        election["contests"].append({
            "id": CONTEST_ID,
            "jurisdiction_id": JURISDICTION_ID,
            "office_id": POST_ID,
            "vote_for": 1,
            "candidate_ids": [person_id],
            "result_status": "certified",
            "winners": [{"person_id": person_id,
                         "name": "Sarah Copeland Hanzas"}],
        })
        if write:
            election_path.write_text(
                "# Vermont general election, November 5, 2024 -- "
                "statewide contests\n# are added one office at a time "
                "under the build order;\n# issue #163 (VT master "
                "tracking).\n"
                + yaml.safe_dump(election, sort_keys=False,
                                 allow_unicode=True),
                encoding="utf-8")
        print(f"{'WRITE' if write else 'WOULD WRITE'}: "
              f"{election_path.relative_to(REPO)} (contest added)")
        created += 1
    else:
        print(f"SKIP contest exists: {CONTEST_ID}")

    membership = {
        "id": "vt-secretary-of-state-sarah-copeland-hanzas",
        "person_id": person_id,
        "organization_id": ORG_ID,
        "post_id": POST_ID,
        "role": "Secretary of State",
        "how_seated": "elected",
        "sources": [CANVASS_SOURCE, OFFICE_SOURCE],
    }
    created += dump(
        DATA_DIR / "memberships" / "state"
        / "vt-secretary-of-state-sarah-copeland-hanzas.yaml",
        membership, header, write)

    print(f"{'Created' if write else 'Would create'} {created} files "
          f"(1 person, 1 election contest, 1 membership; post "
          f"{POST_ID} already existed from PR #165).")


if __name__ == "__main__":
    main()
