#!/usr/bin/env python3
"""Bloomfield, Vermont municipal sweep -- worked example for the VT
municipal tier under issue #163 (VT master tracking).

Full roster backfill for one town, from official Vermont Secretary of
State Elections Division sources only, plus the election record for the
Justices of the Peace. This is the worked example for the municipal
pass: the same shape (SOS directories + SOS JP listing + Title 24
Appendix charter check) is intended to fan out to the other towns.

Verified for Bloomfield (retrieved 2026-10-16):
- Selectboard (3 seats): SOS "Vermont Selectboard Members" directory,
  last updated June 5, 2026.
- Town Treasurer: SOS treasurer contact spreadsheet, last updated
  June 12, 2026, corroborated by the SOS Guide to Vermont's Town
  Clerks, Treasurers & County Clerks (January 2026).
- Justices of the Peace (5 seats): SOS "2025-2026 Vermont Justices of
  the Peace" listing, last updated December 4, 2025; the Bloomfield
  row is marked valid as of 2024, i.e. the cohort elected at the
  November 5, 2024 general election. Election record built from the
  same listing; vote totals and party labels are not published in
  that listing and are not recorded.
- Charter: none. The Town of Bloomfield has no chapter in Title 24
  Appendix V.S.A. (full chapter index checked 2026-10-16); it is a
  general-law town under 17 V.S.A. section 2646. No official town
  website and no published municipal code were found.

HELD, deliberately not minted:
- Town Clerk: the SOS town clerk contact spreadsheet (June 12, 2026)
  names Ray Bowen. Two other official listings conflict but are
  stale vintages: the SOS Guide (January 2026) names Susan Robidas,
  who held the office into early 2026 (North Star Monthly's clerk
  directory, updated ~April 2026, agrees), and the vermont.gov
  explorer carries a ~2022 listing naming Paulette Routhier. A
  Vermont Attorneys Title directory pull (September 1, 2026) also
  names Bowen. Walter directed minting Bowen on 2026-10-16.
- Moderator, Listers, Auditors, Constables, Grand Juror, Town Agent,
  Collector of Delinquent Taxes: no official online source names
  Bloomfield's holders (no town website; the printed annual town
  report is not posted online). Posts are NOT created on speculation;
  they wait for the town report or a clerk records reply.

Conventions follow the VT state/county build (issue #163) and the MA
municipal files: post id "{town}-vt/{office}", org filename = post
filename for single-post bodies, membership id = post file slug +
person slug, person ids uuid5 under the project namespace scoped to
the town. No term starts or ends are recorded; no source states them.

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

JURISDICTION_ID = "ocd-jurisdiction/country:us/state:vt/place:bloomfield/government"
TOWN_PREFIX = "bloomfield-vt"

SEL_URL = (
    "https://outside.vermont.gov/dept/sos/Elections_Division/"
    "election_info_resources/town_meeting_local_elections/"
    "selectboardinformation.pdf"
)
SEL_SOURCE = {
    "url": SEL_URL,
    "note": (
        "Vermont Secretary of State, Elections Division, 'Vermont "
        "Selectboard Members' directory (last updated June 5, 2026), "
        "Bloomfield entry: Eric Brault, Josh Riley, Denault Routhier."
    ),
    "retrieved": RETRIEVED,
}
GUIDE_URL = (
    "https://outside.vermont.gov/dept/sos/Elections_Division/voters/"
    "guide_vermonts_town_clerks_treasurers_county.pdf"
)
TREAS_URL = (
    "https://outside.vermont.gov/dept/sos/Elections_Division/voters/"
    "vermont_town_treasurer_contact_information.xlsx"
)
TREAS_SOURCE = {
    "url": TREAS_URL,
    "note": (
        "Vermont Secretary of State, Elections Division, town "
        "treasurer contact information spreadsheet (last updated "
        "June 12, 2026), Bloomfield row: Sharon Belknap, Treasurer."
    ),
    "retrieved": RETRIEVED,
}
TREAS_GUIDE_SOURCE = {
    "url": GUIDE_URL,
    "note": (
        "Vermont Secretary of State, Elections Division, 'Guide to "
        "Vermont's Town Clerks, Treasurers & County Clerks' (January "
        "2026), Bloomfield entry: Sharon Belknap, Treasurer "
        "(corroborates the contact spreadsheet)."
    ),
    "retrieved": RETRIEVED,
}
CLERK_SOURCE = {
    "url": (
        "https://outside.vermont.gov/dept/sos/Elections_Division/"
        "voters/vermont_town_clerk_contact_information.xlsx"
    ),
    "note": (
        "Vermont Secretary of State, Elections Division, town clerk "
        "contact information spreadsheet (last updated June 12, "
        "2026), Bloomfield row: Ray Bowen, Town Clerk. Minted "
        "2026-10-16 at Walter's direction after a source check "
        "resolved the conflicting listings in the SOS Guide (January "
        "2026, Susan Robidas) and the Vermont.gov explorer (stale "
        "~2022 listing, Paulette Routhier) as older vintages; a "
        "Vermont Attorneys Title directory pull dated September 1, "
        "2026 also names Bowen."
    ),
    "retrieved": RETRIEVED,
}
CLERK_SOURCES = [
    CLERK_SOURCE,
    {
        "url": GUIDE_URL,
        "note": (
            "Vermont Secretary of State, Elections Division, 'Guide "
            "to Vermont's Town Clerks, Treasurers & County Clerks' "
            "(January 2026), Bloomfield entry: Susan Robidas, Clerk. "
            "Superseded: Robidas held the office into early 2026; "
            "the June 2026 SOS contact spreadsheet names Ray Bowen."
        ),
        "retrieved": RETRIEVED,
    },
    {
        "url": "https://www.vermont.gov/towns-and-Cities",
        "note": (
            "Vermont.gov Towns & Cities explorer, Town of Bloomfield "
            "entry: town clerk listed as Paulette Routhier. Stale "
            "listing (matches a ~2022 VPIRG clerk list); not the "
            "current holder."
        ),
        "retrieved": RETRIEVED,
    },
]
JP_URL = (
    "https://outside.vermont.gov/dept/sos/Elections_Division/"
    "election_info_resources/candidates/local_office_descriptions/"
    "vermont_justices_of_the_peace.pdf"
)
JP_SOURCE = {
    "url": JP_URL,
    "note": (
        "Vermont Secretary of State, Elections Division, '2025-2026 "
        "Vermont Justices of the Peace' listing (last updated "
        "December 4, 2025), Bloomfield (Essex County): Ray Bowen, "
        "Sharon Belknap, Bryant Wheeler, Suzanne Routhier, Steven "
        "Bunnell. The listing marks Bloomfield's information valid "
        "as of 2024, i.e. the cohort elected November 5, 2024."
    ),
    "retrieved": RETRIEVED,
}
JP_ELECTION_SOURCE = {
    "url": JP_URL,
    "note": (
        "Winners per the Vermont Secretary of State's official "
        "'2025-2026 Vermont Justices of the Peace' listing (last "
        "updated December 4, 2025), whose Bloomfield entry is marked "
        "valid as of 2024. Vote totals and party labels are not "
        "published in that listing and are not recorded here."
    ),
    "retrieved": RETRIEVED,
}

HEADER = (
    "# Town of Bloomfield municipal roster backfill -- worked example\n"
    "# for the Vermont municipal tier; issue #163 (VT master tracking).\n"
)
CLERK_HEADER = (
    "# Town Clerk: listings conflicted (SOS Guide Jan 2026 vs SOS\n"
    "# contact spreadsheet Jun 2026 vs the stale vermont.gov explorer\n"
    "# listing); resolved to Ray Bowen at Walter's direction,\n"
    "# 2026-10-16 -- see sources below and issue #163.\n"
    "# Issue #163 (VT master tracking).\n"
)
ELECTION_HEADER = (
    "# Bloomfield Justice of the Peace election, November 5, 2024;\n"
    "# issue #163 (VT master tracking).\n"
)

# slug, post title, seats, org name, post/org sources, holders
# holder: (name slug, display name, membership sources)
OFFICES = [
    (
        "selectboard-member", "Selectboard Member", 3, "Bloomfield Selectboard",
        [SEL_SOURCE],
        [
            ("eric-brault", "Eric Brault", [SEL_SOURCE]),
            ("josh-riley", "Josh Riley", [SEL_SOURCE]),
            ("denault-routhier", "Denault Routhier", [SEL_SOURCE]),
        ],
    ),
    (
        "town-clerk", "Town Clerk", 1, "Bloomfield Town Clerk",
        CLERK_SOURCES,
        [("ray-bowen", "Ray Bowen", [CLERK_SOURCE])],
    ),
    (
        "town-treasurer", "Town Treasurer", 1, "Bloomfield Town Treasurer",
        [TREAS_SOURCE, TREAS_GUIDE_SOURCE],
        [("sharon-belknap", "Sharon Belknap", [TREAS_SOURCE, TREAS_GUIDE_SOURCE])],
    ),
    (
        "justice-of-the-peace", "Justice of the Peace", 5,
        "Bloomfield Justices of the Peace",
        [JP_SOURCE],
        [
            ("ray-bowen", "Ray Bowen", [JP_SOURCE]),
            ("sharon-belknap", "Sharon Belknap", [JP_SOURCE]),
            ("bryant-wheeler", "Bryant Wheeler", [JP_SOURCE]),
            ("suzanne-routhier", "Suzanne Routhier", [JP_SOURCE]),
            ("steven-bunnell", "Steven Bunnell", [JP_SOURCE]),
        ],
    ),
]

ELECTION_ID = "bloomfield-vt/2024-11-05/general"
JP_CONTEST_ID = "bloomfield-vt/2024-11-05/justice-of-the-peace"


def oid(kind, key):
    return f"ocd-{kind}/{uuid.uuid5(NS, kind + '|' + key)}"


def person_id(name_slug):
    return oid("person", f"vt|bloomfield|{name_slug}")


def dump(path, doc, write, header=HEADER):
    if path.exists():
        print(f"SKIP exists: {path.relative_to(REPO)}")
        return False
    print(f"{'WRITE' if write else 'WOULD WRITE'}: {path.relative_to(REPO)}")
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            header + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True)
        )
    return True


def main():
    write = "--write" in sys.argv
    created = 0
    people = {}  # name slug -> (display name, [sources], is_jp)

    for office_slug, title, seats, org_name, office_sources, holders in OFFICES:
        post_id = f"{TOWN_PREFIX}/{office_slug}"
        org_id = oid("organization", f"vt|municipal|{post_id}")
        header = CLERK_HEADER if office_slug == "town-clerk" else HEADER
        org = {
            "id": org_id,
            "name": org_name,
            "jurisdiction_id": JURISDICTION_ID,
            "identifiers": [
                {"scheme": "civicmirror-office", "identifier": post_id}
            ],
            "status": "active",
            "sources": office_sources,
        }
        created += dump(
            DATA_DIR / "organizations" / "municipal" / f"{TOWN_PREFIX}-{office_slug}.yaml",
            org, write, header)
        post = {
            "id": post_id,
            "organization_id": org_id,
            "title": title,
            "seats": seats,
            "sources": office_sources,
        }
        created += dump(
            DATA_DIR / "posts" / "municipal" / f"{TOWN_PREFIX}-{office_slug}.yaml",
            post, write, header)

        for name_slug, display_name, member_sources in holders:
            membership = {
                "id": f"{TOWN_PREFIX}-{office_slug}-{name_slug}",
                "person_id": person_id(name_slug),
                "organization_id": org_id,
                "post_id": post_id,
                "role": title,
                "how_seated": "elected",
                "sources": member_sources,
            }
            created += dump(
                DATA_DIR / "memberships" / "municipal"
                / f"{TOWN_PREFIX}-{office_slug}-{name_slug}.yaml",
                membership, write)
            entry = people.setdefault(
                name_slug, (display_name, [], office_slug == "justice-of-the-peace"))
            for s in member_sources:
                if s not in entry[1]:
                    entry[1].append(s)
            if office_slug == "justice-of-the-peace":
                people[name_slug] = (entry[0], entry[1], True)

    for name_slug, (display_name, sources, is_jp) in sorted(people.items()):
        candidacies = []
        if is_jp:
            candidacies = [{
                "contest_id": JP_CONTEST_ID,
                "election_id": ELECTION_ID,
                "jurisdiction_id": JURISDICTION_ID,
                "office_id": f"{TOWN_PREFIX}/justice-of-the-peace",
                "party": None,  # required by schema; not published in the JP listing
                "ballot_name": display_name,
                "status": "active",
            }]
        person = {
            "id": person_id(name_slug),
            "name": display_name,
            "identifiers": [],
            "candidacies": candidacies,
            "verification": {
                "status": "machine-extracted",
                "reviewed_on": RETRIEVED,
                "pipeline": "build_vt_bloomfield_sweep",
            },
            "sources": sources,
        }
        created += dump(
            DATA_DIR / "people" / "municipal" / f"{name_slug}.yaml",
            person, write)

    jp_people = [
        (slug, name)
        for slug, (name, _srcs, is_jp) in sorted(people.items()) if is_jp
    ]
    election = {
        "id": ELECTION_ID,
        "name": "Bloomfield 2024-11-05 general election",
        "date": "2024-11-05",
        "election_type": "general",
        "status": "official",
        "contests": [{
            "id": JP_CONTEST_ID,
            "jurisdiction_id": JURISDICTION_ID,
            "office_id": f"{TOWN_PREFIX}/justice-of-the-peace",
            "vote_for": 5,
            "candidate_ids": [person_id(slug) for slug, _ in jp_people],
            "result_status": "official",
            "winners": [
                {"person_id": person_id(slug), "name": name}
                for slug, name in jp_people
            ],
        }],
        "sources": [JP_ELECTION_SOURCE],
    }
    created += dump(
        DATA_DIR / "elections" / "bloomfield-vt--2024-11-05--justice-of-the-peace.yaml",
        election, write, ELECTION_HEADER)

    print(f"{'Created' if write else 'Would create'} {created} files "
          f"({len(OFFICES)} orgs, {len(OFFICES)} posts, "
          f"{sum(len(o[5]) for o in OFFICES)} memberships, "
          f"{len(people)} people, 1 election).")


if __name__ == "__main__":
    main()
