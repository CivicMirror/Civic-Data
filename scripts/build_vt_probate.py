#!/usr/bin/env python3
"""VT probate district builder (#163 probate tier).

Builds one probate district per invocation from the verified data
file (scripts/vt_probate_data.json): jurisdiction + organization +
post + the elected Judge of Probate (person + membership) + the
2022 election record, together, following Walter's VT build order
(post and holder in the same step).

Structure: 4 V.S.A. section 272 provides ONE probate district per
county, designated by the county's name, each electing one
Probate judge. (An earlier note in this project said 18 districts
with four counties split; that was wrong -- the statute, the
Vermont Judiciary's 14 county Probate Division pages, and the
Elections Database's 14 Probate Judge contests in the 2022
general election all agree on 14.) Districts are modeled as
judicial-district jurisdictions on the repo precedent (MA Middle
District DA, TX judicial districts): division type
judicial_district, classification judiciary.

Holders: every 2022 winner was checked against the Judiciary's
Probate Division court page for the county, whose Court Staff
list names the elected probate judge as the division's
"Superior Judge" (probate judges sit as judges of the Superior
Court's Probate Division), and -- where applicable -- against
the August 11, 2026 primary record (incumbents seeking
re-election) and Judiciary committee rosters. All 14 winners
still hold their seats; there are no mid-term transitions in
this tier.

Data-file conventions: candidates exactly as the VT Elections
Database prints them (county totals read from the database's own
contest CSVs); losers are not modeled as people (repo
convention).

Usage: build_vt_probate.py <county-slug> [--write]
Dry run by default.
"""
import json
import re
import sys
import uuid
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "vt"
SCRIPTS = REPO / "scripts"
RETRIEVED = "2026-10-17"

NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")

STATUTE_URL = ("https://legislature.vermont.gov/statutes/"
               "section/04/007/00272")
STATUTE_SOURCE = {
    "url": STATUTE_URL,
    "note": ("Vermont Statutes Online, 4 V.S.A. section 272 "
             "(Probate districts; Probate judges): 'There shall "
             "be one Probate district in each county, which "
             "shall be designated by the name of the county. "
             "Each Probate district shall elect one Probate "
             "judge.' (Added 2009, No. 154 (Adj. Sess.), "
             "section 17; amended 2021, No. 147.)"),
    "retrieved": RETRIEVED,
}
TERM = (" Probate judges serve four-year terms beginning "
        "February 1 after the election (Vermont Constitution, "
        "Chapter II, sections 50-51); the November 3, 2026 "
        "general election decides the next term.")
RETURN_2022 = (" The contest page's cited official source is "
               "the official return "
               "vt-2022_11_08_General_ALL.pdf.")


def oid(kind, key):
    return f"ocd-{kind}/{uuid.uuid5(NS, kind + '|' + key)}"


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def dump(path, doc, header, write):
    if path.exists():
        print(f"SKIP exists: {path.relative_to(REPO)}")
        return 0
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            header + yaml.safe_dump(doc, sort_keys=False,
                                    allow_unicode=True),
            encoding="utf-8")
        print(f"WRITE: {path.relative_to(REPO)}")
        return 1
    print(f"WOULD WRITE: {path.relative_to(REPO)}")
    return 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    write = "--write" in sys.argv
    if len(args) != 1:
        print("usage: build_vt_probate.py <county-slug> [--write]")
        return
    slug = args[0]
    data = json.loads((SCRIPTS / "vt_probate_data.json").read_text())
    if slug not in data:
        print(f"no probate data for {slug}")
        return
    d = data[slug]
    county = d["county"]
    prefix = f"{slug}-vt-judicial-district"
    post_id = f"{prefix}/judge-of-probate"
    stem = post_id.replace("/", "-")
    jurisdiction_id = (f"ocd-jurisdiction/country:us/state:vt/"
                       f"judicial_district:{slug}/judiciary")
    division_id = (f"ocd-division/country:us/state:vt/"
                   f"judicial_district:{slug}")
    org_id = oid("organization", f"vt|judicial-district|{post_id}")
    judiciary_url = (f"https://www.vtcourts.gov/court-locations/"
                     f"{slug}-probate-division")
    header = (f"# {county} Probate District -- VT probate tier "
              f"(jurisdiction + post + holder + election "
              f"together);\n# issue #163 (VT master tracking).\n")

    judiciary_source = {
        "url": judiciary_url,
        "note": (f"Vermont Judiciary, {county} Probate Division "
                 f"court page: the court's location and staff "
                 f"listing for the {county} Probate District."),
        "retrieved": RETRIEVED,
    }

    created = 0

    # 1. Jurisdiction
    jurisdiction = {
        "id": jurisdiction_id,
        "name": f"{county} Probate District",
        "state": "vt",
        "division_id": division_id,
        "classification": "judiciary",
        "sources": [STATUTE_SOURCE, judiciary_source],
    }
    created += dump(
        DATA_DIR / "jurisdictions" / "judicial-district"
        / f"{slug}.yaml",
        jurisdiction, header, write)

    # 2. Organization (the district's Probate Division court)
    org = {
        "id": org_id,
        "name": f"{county} Probate Division",
        "jurisdiction_id": jurisdiction_id,
        "identifiers": [{"scheme": "civicmirror-office",
                         "identifier": post_id}],
        "status": "active",
        "sources": [STATUTE_SOURCE, judiciary_source],
    }
    created += dump(
        DATA_DIR / "organizations" / "judicial-district"
        / f"{stem}.yaml",
        org, header, write)

    # 3. Post
    post = {
        "id": post_id,
        "organization_id": org_id,
        "title": "Judge of Probate",
        "seats": 1,
        "sources": [STATUTE_SOURCE, judiciary_source],
    }
    created += dump(
        DATA_DIR / "posts" / "judicial-district" / f"{stem}.yaml",
        post, header, write)

    # 4. Election + winner person + membership
    contest_id = (f"{prefix}/2022-11-08/judge-of-probate")
    election_id = f"{prefix}/2022-11-08/general"
    db_url = (f"https://electionarchive.vermont.gov/contest/"
              f"{d['contest_id']}")
    cands = d["candidates"]
    winners = [c for c in cands if c.get("winner")]
    assert len(winners) == 1, f"{slug}: expected exactly 1 winner"
    winner = winners[0]

    parts = []
    for i, c in enumerate(cands):
        suffix = " votes" if i == 0 else ""
        parts.append(f"{c['name']} ({c['party']}) "
                     f"{c['votes']:,}{suffix}")
    note = (f"Vermont Elections Database (Vermont Secretary of "
            f"State), contest page '2022 Nov 8, General Election, "
            f"Probate Judge, {county} County' (county totals): "
            + "; ".join(parts)
            + f"; write-ins {d['write_ins']:,}.")
    note += RETURN_2022 + TERM
    if d.get("note_extra"):
        note += " " + d["note_extra"]
    db_source = {"url": db_url, "note": note,
                 "retrieved": RETRIEVED}

    holder_source = {
        "url": judiciary_url,
        "note": (f"Vermont Judiciary, {county} Probate Division "
                 f"court page, Court Staff list: names "
                 f"{winner['name']} as the division's Superior "
                 f"Judge -- probate judges sit as judges of the "
                 f"Superior Court's Probate Division -- the "
                 f"sitting holder as of the retrieval date."),
        "retrieved": RETRIEVED,
    }
    sources = [db_source, holder_source]
    for extra in d.get("extra_holder_sources", []):
        sources = sources + [{**extra, "retrieved": RETRIEVED}]

    pslug = slugify(winner["name"])
    pid = oid("person", f"vt|{slug}-judicial-district|{pslug}")
    person = {
        "id": pid,
        "name": winner["name"],
        "identifiers": [],
        "candidacies": [{
            "contest_id": contest_id,
            "election_id": election_id,
            "jurisdiction_id": jurisdiction_id,
            "office_id": post_id,
            "party": winner["party"],
            "ballot_name": winner["name"],
            "status": "active",
        }],
        "verification": {
            "status": "machine-extracted",
            "reviewed_on": RETRIEVED,
            "pipeline": "build_vt_probate",
        },
        "sources": sources,
    }
    created += dump(
        DATA_DIR / "people" / "judicial-district"
        / f"{pslug}.yaml",
        person, header, write)

    mid = stem + "-" + pslug
    membership = {
        "id": mid,
        "person_id": pid,
        "organization_id": org_id,
        "post_id": post_id,
        "role": "Judge of Probate",
        "how_seated": "elected",
        "sources": sources,
    }
    created += dump(
        DATA_DIR / "memberships" / "judicial-district"
        / f"{mid}.yaml",
        membership, header, write)

    election = {
        "id": election_id,
        "name": (f"{county} Probate District 2022-11-08 "
                 f"general election"),
        "date": "2022-11-08",
        "election_type": "general",
        "status": "official",
        "contests": [{
            "id": contest_id,
            "jurisdiction_id": jurisdiction_id,
            "office_id": post_id,
            "vote_for": 1,
            "candidate_ids": [pid],
            "result_status": "certified",
            "winners": [{"person_id": pid,
                         "name": winner["name"]}],
        }],
        "sources": [db_source],
    }
    created += dump(
        DATA_DIR / "elections"
        / f"{prefix}--2022-11-08--general.yaml",
        election, header, write)

    print(f"{'Created' if write else 'Would create'} {created} "
          f"files for {county} Probate District.")


if __name__ == "__main__":
    main()
