#!/usr/bin/env python3
"""Vermont statewide executive steps 4-6 of the build order (#163).

One parameterized builder for the three remaining statewide offices,
run once per office (Walter's order: Attorney General, State
Treasurer, Auditor of Accounts):

    build_vt_statewide_office.py attorney-general --write
    build_vt_statewide_office.py state-treasurer --write
    build_vt_statewide_office.py auditor-of-accounts --write

Each run completes the office's build-order unit: person + contest
on the 2024 general election record + membership. The posts already
exist (PR #165).

Verified (retrieved 2026-10-16), official sources:
- SOS Official Report of the Canvassing Committee, 2024 general
  election, read firsthand: Attorney General (s.9) Charity R.
  Clark* 200,711, Ture Nelson 128,798, Kevin Gustafson 17,159,
  write-in 490; State Treasurer (s.6) Mike Pieciak* 211,134,
  Joshua Bechhoefer 135,763, write-in 415; Auditor of Accounts
  (s.8) Doug Hoffer* 207,195, H. Brooke Paige 134,066, write-in
  532. All three winners took outright majorities.
- Party labels are as printed in the Elections Division's Official
  Returns of Votes (the canvass prints none): Clark DEMOCRATIC,
  Pieciak DEMOCRATIC, Hoffer DEM/PROG (Democratic/Progressive
  fusion nomination).
- Current-holder corroboration from each office's own official
  site/documents (see OFFICES below).

No term dates are recorded as fields; the November 3, 2026 general
election decides the next terms. Factory concordance: the factory
has no state tier. Idempotent per office. Dry run by default.
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
ELECTION_ID = "vt/2024-11-05/general"

CANVASS_URL = (
    "https://outside.vermont.gov/dept/sos/Elections_Division/"
    "election_info_resources/elections_results_data/"
    "2024_general_election_official_report_canvassing_committee_"
    "united_states_vermont_statewide_offices.pdf"
)

CANVASS_HEAD = (
    "Vermont Secretary of State, Elections Division, Official "
    "Report of the Canvassing Committee -- United States and "
    "Vermont Statewide Offices, General Election, November 5, "
    "2024 (canvassed under 17 V.S.A. sections 2368-2371), "
)
CANVASS_TAIL = (
    " The asterisk marks the winner, who took an outright "
    "majority of the votes cast for the office. Party labels are "
    "not printed in the canvass report; the affiliation recorded "
    "here is as printed in the Elections Division's Official "
    "Returns of Votes for the same election. The November 3, "
    "2026 general election decides the next term."
)

OFFICES = {
    "attorney-general": {
        "step": 4,
        "title": "Attorney General",
        "post_id": "vt/attorney-general",
        "org_id": "ocd-organization/b6bf5638-c99c-5fdb-b3ff-eabc7f0155b3",
        "contest_id": "vt/2024-11-05/attorney-general",
        "slug": "charity-r-clark",
        "name": "Charity R. Clark",
        "party": "Democratic",
        "membership_id": "vt-attorney-general-charity-r-clark",
        "canvass_note": (
            CANVASS_HEAD
            + "section 9, For Attorney General: Charity R. "
              "Clark* 200,711 votes; Ture Nelson 128,798; Kevin "
              "Gustafson 17,159; write-in 490."
            + CANVASS_TAIL
            + " The office of Attorney General is statutory "
              "(3 V.S.A. section 151)."
        ),
        "office_url": (
            "https://ago.vermont.gov/blog/2026/07/17/"
            "attorney-general-clark-and-secretary-state-copeland-"
            "hanzas-release-joint-statement-reaffirming"
        ),
        "office_note": (
            "Official site of the Vermont Attorney General "
            "(ago.vermont.gov), office release dated July 17, "
            "2026: 'Attorney General Charity Clark and Secretary "
            "of State Sarah Copeland Hanzas today released a "
            "joint statement...' -- names Clark as the sitting "
            "Attorney General as of the retrieval date."
        ),
    },
    "state-treasurer": {
        "step": 5,
        "title": "State Treasurer",
        "post_id": "vt/state-treasurer",
        "org_id": "ocd-organization/59e4138f-16ef-5d77-90e4-ccf6b17ca392",
        "contest_id": "vt/2024-11-05/state-treasurer",
        "slug": "mike-pieciak",
        "name": "Mike Pieciak",
        "party": "Democratic",
        "membership_id": "vt-state-treasurer-mike-pieciak",
        "canvass_note": (
            CANVASS_HEAD
            + "section 6, For State Treasurer: Mike Pieciak* "
              "211,134 votes; Joshua Bechhoefer 135,763; "
              "write-in 415."
            + CANVASS_TAIL
        ),
        "office_url": (
            "https://legislature.vermont.gov/assets/Legislative-"
            "Reports/Vermont-Treasurers-2025-Annual-Report-1.pdf"
        ),
        "office_note": (
            "Office of the State Treasurer, Vermont Treasurer's "
            "2025 Annual Report (submitted January 15, 2026), "
            "signed 'Mike Pieciak, State Treasurer' -- names him "
            "as the sitting Treasurer as of the retrieval date."
        ),
    },
    "auditor-of-accounts": {
        "step": 6,
        "title": "Auditor of Accounts",
        "post_id": "vt/auditor-of-accounts",
        "org_id": "ocd-organization/df9ec026-5b93-5a6e-a168-077346a76204",
        "contest_id": "vt/2024-11-05/auditor-of-accounts",
        "slug": "doug-hoffer",
        "name": "Doug Hoffer",
        "party": "Democratic/Progressive",
        "membership_id": "vt-auditor-of-accounts-doug-hoffer",
        "canvass_note": (
            CANVASS_HEAD
            + "section 8, For Auditor of Accounts: Doug Hoffer* "
              "207,195 votes; H. Brooke Paige 134,066; write-in "
              "532."
            + CANVASS_TAIL.replace(
                "the affiliation recorded here is as printed",
                "Hoffer's affiliation is printed as DEM/PROG in "
                "the returns (a Democratic/Progressive fusion "
                "nomination); the affiliation recorded here is "
                "as printed")
        ),
        "office_url": (
            "https://auditor.vermont.gov/sites/auditor/files/"
            "Peer%20Review%20Press%20Release.pdf"
        ),
        "office_note": (
            "Official site of the Vermont Auditor of Accounts "
            "(auditor.vermont.gov), office press release dated "
            "June 12, 2026: 'State Auditor Doug Hoffer "
            "announced...' -- names Hoffer as the sitting "
            "Auditor as of the retrieval date."
        ),
    },
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
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    write = "--write" in sys.argv
    if len(args) != 1 or args[0] not in OFFICES:
        print("usage: build_vt_statewide_office.py "
              "<attorney-general|state-treasurer|auditor-of-accounts> "
              "[--write]")
        raise SystemExit(2)
    o = OFFICES[args[0]]
    created = 0
    person_id = oid("person", f"vt|state|{o['slug']}")

    header = (f"# Vermont {o['title']} -- step {o['step']} of the "
              f"build order (post + holder together);\n# issue #163 "
              f"(VT master tracking).\n")

    canvass_source = {"url": CANVASS_URL, "note": o["canvass_note"],
                      "retrieved": RETRIEVED}
    office_source = {"url": o["office_url"], "note": o["office_note"],
                     "retrieved": RETRIEVED}

    person = {
        "id": person_id,
        "name": o["name"],
        "identifiers": [],
        "candidacies": [
            {
                "contest_id": o["contest_id"],
                "election_id": ELECTION_ID,
                "jurisdiction_id": JURISDICTION_ID,
                "office_id": o["post_id"],
                "party": o["party"],
                "ballot_name": o["name"],
                "status": "active",
            }
        ],
        "verification": {
            "status": "machine-extracted",
            "reviewed_on": RETRIEVED,
            "pipeline": "build_vt_statewide_office",
        },
        "sources": [canvass_source, office_source],
    }
    created += dump(DATA_DIR / "people" / "state" / f"{o['slug']}.yaml",
                    person, header, write)

    election_path = DATA_DIR / "elections" / "vt--2024-11-05--general.yaml"
    election = yaml.safe_load(election_path.read_text(encoding="utf-8"))
    assert election["id"] == ELECTION_ID
    if not any(c["id"] == o["contest_id"] for c in election["contests"]):
        election["contests"].append({
            "id": o["contest_id"],
            "jurisdiction_id": JURISDICTION_ID,
            "office_id": o["post_id"],
            "vote_for": 1,
            "candidate_ids": [person_id],
            "result_status": "certified",
            "winners": [{"person_id": person_id, "name": o["name"]}],
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
        print(f"SKIP contest exists: {o['contest_id']}")

    membership = {
        "id": o["membership_id"],
        "person_id": person_id,
        "organization_id": o["org_id"],
        "post_id": o["post_id"],
        "role": o["title"],
        "how_seated": "elected",
        "sources": [canvass_source, office_source],
    }
    created += dump(
        DATA_DIR / "memberships" / "state" / f"{o['membership_id']}.yaml",
        membership, header, write)

    print(f"{'Created' if write else 'Would create'} {created} files "
          f"for {o['title']} (post {o['post_id']} already existed "
          f"from PR #165).")


if __name__ == "__main__":
    main()
