#!/usr/bin/env python3
"""Addison County -- worked example for the VT county tier (#163).

County build-order shape (set by this example): one county at a
time, all four elected offices with full membership and election
information. State's Attorney, Sheriff, and the two Assistant
Judges trace to the county's 2022 general election record;
the High Bailiff traces to the 2024 general election record
(high bailiffs are elected biennially, Vt. Const. Ch. II s.43;
the other three offices serve four-year terms from February 1
under s.50). Person keys are county-scoped (vt|addison-county|..).

Verified (retrieved 2026-10-16), official sources:
- Vermont Elections Database (Secretary of State), Addison County
  contest pages (county totals; each page cites the official
  return PDF as its official source):
  * 2022 State's Attorney (listed as District Attorney):
    Eva P. Vekos (Democratic) 9,029; Peter M. Bevere
    (Independent) 6,546; write-ins 68.
  * 2022 Sheriff (listed as County Sheriff): Michael R. Elmore
    (Democratic/Republican) 8,177; Gerald Grant (Independent)
    3,807; Mark A. Stacey (Independent) 3,106; write-ins 138.
  * 2022 Assistant Judge (vote for 2): Patricia Ross
    (Democratic) 12,242; Nicole Wilkerson (Democratic) 11,685;
    write-ins 214 -- the only two candidates for the two seats.
  * 2024 High Bailiff: Dave Silberman (Democratic) 11,793;
    Ron Holmes (Republican) 9,355; write-ins 93.
- Current-holder corroboration for State's Attorney and Sheriff:
  the Department of State's Attorneys and Sheriffs' Addison
  County office page lists Vekos and Elmore in office.

No term dates are recorded as fields. All five winners are new
person records (collision check over the VT tree was clear).
Dry run by default; pass --write to create files.
"""
import sys
import uuid
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "vt"
RETRIEVED = "2026-10-16"

NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")

JURISDICTION_ID = "ocd-jurisdiction/country:us/state:vt/county:addison/government"
ELECTION_2022 = "addison-vt-county/2022-11-08/general"
ELECTION_2024 = "addison-vt-county/2024-11-05/general"

TERM_4YR = (
    " The office serves a four-year term beginning February 1 "
    "after the election (Vermont Constitution, Chapter II, "
    "section 50); the November 3, 2026 general election decides "
    "the next term."
)
RETURN_2022 = (
    " The contest page's cited official source is the official "
    "return vt-2022_11_08_General_ALL.pdf."
)
DEPT_URL = "https://prosecutors.vermont.gov/offices/addison"
DEPT_SOURCE = {
    "url": DEPT_URL,
    "note": (
        "Vermont Department of State's Attorneys and Sheriffs, "
        "Addison County office page: lists Eva Vekos as Addison "
        "County State's Attorney and Michael Elmore as Addison "
        "County Sheriff -- the sitting holders as of the "
        "retrieval date."
    ),
    "retrieved": RETRIEVED,
}

OFFICES = [
    {
        "post_id": "addison-vt-county/states-attorney",
        "org_id": "ocd-organization/a1df21c8-5dc9-5a00-bf37-45b46bd9c2d7",
        "role": "State's Attorney",
        "election": ELECTION_2022,
        "contest_id": "addison-vt-county/2022-11-08/states-attorney",
        "vote_for": 1,
        "db_url": "https://electionarchive.vermont.gov/contest/158032",
        "db_note": (
            "Vermont Elections Database (Vermont Secretary of "
            "State), contest page '2022 Nov 8, General Election, "
            "State's Attorney (listed as District Attorney), "
            "Addison County' (county totals): Eva P. Vekos "
            "(Democratic) 9,029 votes; Peter M. Bevere "
            "(Independent) 6,546; write-ins 68." + RETURN_2022 + TERM_4YR
        ),
        "holder_source": DEPT_SOURCE,
        "people": [
            {"slug": "eva-p-vekos", "name": "Eva P. Vekos",
             "party": "Democratic"},
        ],
    },
    {
        "post_id": "addison-vt-county/sheriff",
        "org_id": "ocd-organization/ac38f3da-7916-5b42-89f2-a968d9a36f01",
        "role": "Sheriff",
        "election": ELECTION_2022,
        "contest_id": "addison-vt-county/2022-11-08/sheriff",
        "vote_for": 1,
        "db_url": "https://electionarchive.vermont.gov/contest/157892",
        "db_note": (
            "Vermont Elections Database (Vermont Secretary of "
            "State), contest page '2022 Nov 8, General Election, "
            "Sheriff (listed as County Sheriff), Addison County' "
            "(county totals): Michael R. Elmore "
            "(Democratic/Republican) 8,177 votes; Gerald Grant "
            "(Independent) 3,807; Mark A. Stacey (Independent) "
            "3,106; write-ins 138." + RETURN_2022 + TERM_4YR
        ),
        "holder_source": DEPT_SOURCE,
        "people": [
            {"slug": "michael-r-elmore", "name": "Michael R. Elmore",
             "party": "Democratic/Republican"},
        ],
    },
    {
        "post_id": "addison-vt-county/assistant-judge",
        "org_id": "ocd-organization/ad7ae168-63a0-5413-8fb5-2067ee192157",
        "role": "Assistant Judge",
        "election": ELECTION_2022,
        "contest_id": "addison-vt-county/2022-11-08/assistant-judge",
        "vote_for": 2,
        "db_url": "https://electionarchive.vermont.gov/elections/view/157844/",
        "db_note": (
            "Vermont Elections Database (Vermont Secretary of "
            "State), contest page '2022 Nov 8, General Election, "
            "Assistant Judge, Addison County' (vote for 2; "
            "county totals): Patricia Ross (Democratic) 12,242 "
            "votes and Nicole Wilkerson (Democratic) 11,685; "
            "write-ins 214. Ross and Wilkerson were the only "
            "two candidates for the two seats." + RETURN_2022 + TERM_4YR
        ),
        "holder_source": None,
        "people": [
            {"slug": "patricia-ross", "name": "Patricia Ross",
             "party": "Democratic"},
            {"slug": "nicole-wilkerson", "name": "Nicole Wilkerson",
             "party": "Democratic"},
        ],
    },
    {
        "post_id": "addison-vt-county/high-bailiff",
        "org_id": "ocd-organization/f4c043bf-c65e-55ff-aa7d-3fb4aac85afe",
        "role": "High Bailiff",
        "election": ELECTION_2024,
        "contest_id": "addison-vt-county/2024-11-05/high-bailiff",
        "vote_for": 1,
        "db_url": "https://electionarchive.vermont.gov/contest/160973",
        "db_note": (
            "Vermont Elections Database (Vermont Secretary of "
            "State), contest page '2024 Nov 5, General Election, "
            "High Bailiff, Addison County' (county totals): "
            "Dave Silberman (Democratic) 11,793 votes; Ron "
            "Holmes (Republican) 9,355; write-ins 93. The "
            "contest page's cited official source is the "
            "Secretary of State's 'November 5, 2024 General "
            "Official Results.pdf'. High bailiffs are elected "
            "biennially (Vermont Constitution, Chapter II, "
            "section 43); the November 3, 2026 general election "
            "decides the next term."
        ),
        "holder_source": None,
        "people": [
            {"slug": "dave-silberman", "name": "Dave Silberman",
             "party": "Democratic"},
        ],
    },
]


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
    header = ("# Addison County -- worked example for the VT county "
              "tier (posts + holders + elections together);\n"
              "# issue #163 (VT master tracking).\n")

    elections = {
        ELECTION_2022: {
            "id": ELECTION_2022,
            "name": "Addison County 2022-11-08 general election",
            "date": "2022-11-08",
            "election_type": "general",
            "status": "official",
            "contests": [],
            "sources": [],
        },
        ELECTION_2024: {
            "id": ELECTION_2024,
            "name": "Addison County 2024-11-05 general election",
            "date": "2024-11-05",
            "election_type": "general",
            "status": "official",
            "contests": [],
            "sources": [],
        },
    }

    for office in OFFICES:
        db_source = {"url": office["db_url"], "note": office["db_note"],
                     "retrieved": RETRIEVED}
        sources = [db_source]
        if office["holder_source"]:
            sources.append(office["holder_source"])
        candidate_ids = []
        winners = []
        for person in office["people"]:
            pid = oid("person", f"vt|addison-county|{person['slug']}")
            candidate_ids.append(pid)
            winners.append({"person_id": pid, "name": person["name"]})
            doc = {
                "id": pid,
                "name": person["name"],
                "identifiers": [],
                "candidacies": [
                    {
                        "contest_id": office["contest_id"],
                        "election_id": office["election"],
                        "jurisdiction_id": JURISDICTION_ID,
                        "office_id": office["post_id"],
                        "party": person["party"],
                        "ballot_name": person["name"],
                        "status": "active",
                    }
                ],
                "verification": {
                    "status": "machine-extracted",
                    "reviewed_on": RETRIEVED,
                    "pipeline": "build_vt_addison_county",
                },
                "sources": sources,
            }
            created += dump(
                DATA_DIR / "people" / "county" / f"{person['slug']}.yaml",
                doc, header, write)
            membership_id = (office["post_id"].replace("/", "-")
                             + "-" + person["slug"])
            membership = {
                "id": membership_id,
                "person_id": pid,
                "organization_id": office["org_id"],
                "post_id": office["post_id"],
                "role": office["role"],
                "how_seated": "elected",
                "sources": sources,
            }
            created += dump(
                DATA_DIR / "memberships" / "county"
                / f"{membership_id}.yaml",
                membership, header, write)
        elections[office["election"]]["contests"].append({
            "id": office["contest_id"],
            "jurisdiction_id": JURISDICTION_ID,
            "office_id": office["post_id"],
            "vote_for": office["vote_for"],
            "candidate_ids": candidate_ids,
            "result_status": "certified",
            "winners": winners,
        })
        elections[office["election"]]["sources"].append(db_source)

    for election_id, doc in elections.items():
        date = "2022-11-08" if "2022" in election_id else "2024-11-05"
        created += dump(
            DATA_DIR / "elections"
            / f"addison-vt-county--{date}--general.yaml",
            doc, header, write)

    print(f"{'Created' if write else 'Would create'} {created} files "
          f"(5 people, 5 memberships, 2 elections; 4 posts already "
          f"existed from PR #165).")


if __name__ == "__main__":
    main()
