#!/usr/bin/env python3
"""Build the 2024 Texas General Election record for the county and judicial imports.

The two TX 2024 officer importers create person candidacies and membership
records from the Texas Secretary of State's Winner Listing Report.  A
candidacy must have a reciprocal contest in an Election document, so this
script collects those source-backed winner candidacies into the single
statewide election identity used by both importers.

The report identifies winners, not every candidate on each local ballot.
Accordingly, every candidate and winner in the generated contests is a
reported winner; this script does not infer unreported opponents or votes.
"""

import sys
from collections import defaultdict
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
ELECTION_ID = "us-tx/2024-11-05/general"
OUTPUT = DATA_DIR / "elections" / "us-tx--2024-11-05--general.yaml"
RESULTS_URL = "https://results.texas-election.com/reports"
RETRIEVED = "2026-09-01"
KINDS = ("county", "judicial")

HEADER = (
    "# Generated from the Texas Secretary of State's 2024 General Election\n"
    "# Winner Listing Report by scripts/build_tx_2024_general_election.py.\n"
    "# The report identifies winners; it does not supply a complete local\n"
    "# ballot or vote totals for every county contest. See issue #33.\n"
)


def load_documents(kind):
    """Yield YAML documents from the scoped import directory."""
    for path in sorted((DATA_DIR / kind).rglob("*.yaml")):
        yield path, yaml.safe_load(path.read_text())


def load_people():
    people = {}
    for kind in KINDS:
        for path in sorted((DATA_DIR / "people" / kind).glob("*.yaml")):
            document = yaml.safe_load(path.read_text())
            person_id = document["id"]
            if person_id in people:
                raise ValueError(f"duplicate person id {person_id!r}: {path}")
            people[person_id] = document
    return people


def load_winner_memberships():
    """Return imported winning memberships, keyed by person and post."""
    winners = set()
    for kind in KINDS:
        for path in sorted((DATA_DIR / "memberships" / kind).glob("*.yaml")):
            document = yaml.safe_load(path.read_text())
            if document.get("how_seated") == "elected":
                winners.add((document["person_id"], document["post_id"]))
    return winners


def build_election(people, winner_memberships):
    contests = defaultdict(list)
    for person_id, person in people.items():
        for candidacy in person["candidacies"]:
            if candidacy["election_id"] != ELECTION_ID:
                continue
            contests[candidacy["contest_id"]].append((person_id, person, candidacy))

    generated = []
    for contest_id in sorted(contests):
        candidates = sorted(contests[contest_id], key=lambda entry: entry[0])
        first_candidacy = candidates[0][2]
        jurisdiction_id = first_candidacy["jurisdiction_id"]
        office_id = first_candidacy["office_id"]
        for person_id, _, candidacy in candidates:
            if (candidacy["jurisdiction_id"], candidacy["office_id"]) != (jurisdiction_id, office_id):
                raise ValueError(f"contest {contest_id!r} mixes jurisdictions or offices")
            if (person_id, office_id) not in winner_memberships:
                raise ValueError(
                    f"contest {contest_id!r} candidate {person_id!r} has no elected membership for {office_id!r}"
                )

        winners = []
        for person_id, person, candidacy in candidates:
            winner = {"person_id": person_id, "name": person["name"]}
            if candidacy["party"] is not None:
                winner["party"] = candidacy["party"]
            winners.append(winner)

        generated.append({
            "id": contest_id,
            "jurisdiction_id": jurisdiction_id,
            "office_id": office_id,
            "vote_for": len(winners),
            "candidate_ids": [person_id for person_id, _, _ in candidates],
            "result_status": "official",
            "winners": winners,
        })

    return {
        "id": ELECTION_ID,
        "name": "2024 Texas General Election",
        "date": "2024-11-05",
        "election_type": "general",
        "status": "official",
        "contests": generated,
        "sources": [{
            "url": RESULTS_URL,
            "note": "Texas SOS 2024 General Election Winner Listing Report; contest candidates and winners are limited to the report's winner records.",
            "retrieved": RETRIEVED,
        }],
    }


def render(document):
    return HEADER + yaml.safe_dump(
        document, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000
    )


def main():
    write = "--write" in sys.argv[1:]
    unexpected = set(sys.argv[1:]) - {"--write"}
    if unexpected:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} [--write]")

    people = load_people()
    election = build_election(people, load_winner_memberships())
    text = render(election)
    print(f"People: {len(people)}  Contests: {len(election['contests'])}  Winners: {sum(len(c['winners']) for c in election['contests'])}")
    if not write:
        print("(dry run -- pass --write to create or update the election record)")
        return

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(text)
    print(f"Wrote {OUTPUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
