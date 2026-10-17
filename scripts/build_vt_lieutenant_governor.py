#!/usr/bin/env python3
"""Vermont Lieutenant Governor -- step 2 of the new build order (#163).

Build order (Walter, 2026-10-16): one post at a time, holder built in
the same step, Governor first, working down. The vt/lieutenant-governor
post already exists (PR #165). Walter first directed the seat be held
vacant, then released the hold the same day; this script completes the
unit: person + Lieutenant Governor contest on the 2024 general
election record + membership.

The election file is renamed from vt--2024-11-05--governor.yaml to
vt--2024-11-05--general.yaml: the election (id vt/2024-11-05/general)
accumulates one statewide contest per build-order step.

Verified (retrieved 2026-10-16), official sources:
- SOS Official Report of the Canvassing Committee, 2024 general
  election: for Lieutenant Governor, John S. Rodgers 171,854 votes
  (46.09%, a plurality), David Zuckerman 165,876, Ian Diamondstone
  13,671, write-in 1,013. No candidate received the major part of the
  votes, so under Chapter II, section 47 of the Vermont Constitution
  the General Assembly elected the office by joint ballot on
  January 9, 2025, choosing Rodgers 158-18; he was sworn in the
  same day.
- The official site of the Office of the Lieutenant Governor
  (ltgov.vermont.gov) names Rodgers as the sitting holder.
- Party (Republican) is as printed in the Elections Division's
  Official Returns of Votes; the canvass report prints no labels.

Membership how_seated is "elected": Rodgers was elected -- by the
General Assembly in joint ballot after winning the plurality -- and
the mechanism is spelled out in the source notes. No term dates are
recorded as fields. The November 3, 2026 election decides the next
term. Factory concordance: the factory has no state tier.

Idempotent for the person/membership; the election contest is added
only if absent. Dry run by default; pass --write to create files.
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
POST_ID = "vt/lieutenant-governor"
ORG_ID = "ocd-organization/ecf43b7b-7bce-5471-8101-1238665f0096"
ELECTION_ID = "vt/2024-11-05/general"
CONTEST_ID = "vt/2024-11-05/lieutenant-governor"

CANVASS_URL = (
    "https://outside.vermont.gov/dept/sos/Elections_Division/"
    "election_info_resources/elections_results_data/"
    "2024_general_election_official_report_canvassing_committee_"
    "united_states_vermont_statewide_offices.pdf"
)
OFFICE_URL = "https://ltgov.vermont.gov/about/john-rodgers"

CANVASS_SOURCE = {
    "url": CANVASS_URL,
    "note": (
        "Vermont Secretary of State, Elections Division, Official "
        "Report of the Canvassing Committee -- United States and "
        "Vermont Statewide Offices, General Election, November 5, "
        "2024 (canvassed under 17 V.S.A. sections 2368-2371). For "
        "Lieutenant Governor: John S. Rodgers 171,854 votes "
        "(46.09%, a plurality); David Zuckerman 165,876; Ian "
        "Diamondstone 13,671; write-in 1,013. No candidate received "
        "the major part of the votes, so under Chapter II, section "
        "47 of the Vermont Constitution the General Assembly "
        "elected the office by joint ballot on January 9, 2025, "
        "choosing Rodgers 158-18 over Zuckerman; Rodgers was sworn "
        "in the same day. Party labels are not printed in the "
        "canvass report; Rodgers' Republican affiliation is as "
        "printed in the Elections Division's Official Returns of "
        "Votes for the same election. The November 3, 2026 general "
        "election decides the next term."
    ),
    "retrieved": RETRIEVED,
}

OFFICE_SOURCE = {
    "url": OFFICE_URL,
    "note": (
        "Official site of the Office of the Lieutenant Governor "
        "(ltgov.vermont.gov), 'About John Rodgers': names John "
        "Rodgers of Glover as Vermont's Lieutenant Governor -- "
        "confirms him as the sitting holder as of the retrieval "
        "date."
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
    person_id = oid("person", "vt|state|john-s-rodgers")

    header = ("# Vermont Lieutenant Governor -- step 2 of the build "
              "order (post + holder together);\n# issue #163 (VT "
              "master tracking).\n")

    person = {
        "id": person_id,
        "name": "John S. Rodgers",
        "identifiers": [],
        "candidacies": [
            {
                "contest_id": CONTEST_ID,
                "election_id": ELECTION_ID,
                "jurisdiction_id": JURISDICTION_ID,
                "office_id": POST_ID,
                "party": "Republican",
                "ballot_name": "John S. Rodgers",
                "status": "active",
            }
        ],
        "verification": {
            "status": "machine-extracted",
            "reviewed_on": RETRIEVED,
            "pipeline": "build_vt_lieutenant_governor",
        },
        "sources": [CANVASS_SOURCE, OFFICE_SOURCE],
    }
    created += dump(DATA_DIR / "people" / "state" / "john-s-rodgers.yaml",
                    person, header, write)

    # Election: carry the existing record forward under the general
    # filename, adding the Lieutenant Governor contest if absent.
    old_path = DATA_DIR / "elections" / "vt--2024-11-05--governor.yaml"
    new_path = DATA_DIR / "elections" / "vt--2024-11-05--general.yaml"
    src_path = new_path if new_path.exists() else old_path
    election = yaml.safe_load(src_path.read_text(encoding="utf-8"))
    assert election["id"] == ELECTION_ID
    if not any(c["id"] == CONTEST_ID for c in election["contests"]):
        election["contests"].append({
            "id": CONTEST_ID,
            "jurisdiction_id": JURISDICTION_ID,
            "office_id": POST_ID,
            "vote_for": 1,
            "candidate_ids": [person_id],
            "result_status": "certified",
            "winners": [{"person_id": person_id, "name": "John S. Rodgers"}],
        })
        if write:
            new_path.write_text(
                "# Vermont general election, November 5, 2024 -- "
                "statewide contests\n# are added one office at a time "
                "under the build order;\n# issue #163 (VT master "
                "tracking).\n"
                + yaml.safe_dump(election, sort_keys=False,
                                 allow_unicode=True),
                encoding="utf-8")
            if src_path != new_path:
                src_path.unlink()
        print(f"{'WRITE' if write else 'WOULD WRITE'}: "
              f"{new_path.relative_to(REPO)} (contest added; "
              f"renamed from {old_path.name})")
        created += 1
    else:
        print(f"SKIP contest exists: {CONTEST_ID}")

    membership = {
        "id": "vt-lieutenant-governor-john-s-rodgers",
        "person_id": person_id,
        "organization_id": ORG_ID,
        "post_id": POST_ID,
        "role": "Lieutenant Governor",
        "how_seated": "elected",
        "sources": [CANVASS_SOURCE, OFFICE_SOURCE],
    }
    created += dump(
        DATA_DIR / "memberships" / "state"
        / "vt-lieutenant-governor-john-s-rodgers.yaml",
        membership, header, write)

    print(f"{'Created' if write else 'Would create'} {created} files "
          f"(1 person, 1 election contest, 1 membership; post "
          f"{POST_ID} already existed from PR #165).")


if __name__ == "__main__":
    main()
