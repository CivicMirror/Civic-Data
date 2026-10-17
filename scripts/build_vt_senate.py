#!/usr/bin/env python3
"""VT Senate builder (#163 legislative pass, Senate chamber).

Builds one Senate district per invocation from the verified data
file (scripts/vt_senate_data.json): sldu jurisdiction + district
organization + State Senator post (1-3 seats) + the district's
2024 winners (people + memberships) + the district's 2024
election record, together, following Walter's VT build order and
the repo's MA legislative precedent (sldu divisions,
jurisdiction .../legislature, classification legislature).

Districts are those of Act 89 of 2022 (H.722), the current
apportionment: 16 districts, 30 seats. Winners trace to the
November 5, 2024 general election (Vermont Elections Database;
figures verified against the database's own contest CSVs).
Current-holder check: the General Assembly's All Senators
directory (2025-2026 session). Two seats turned over mid-term
and carry a "transition" block in the data file: the 2024
winner keeps the win (person + candidacy + contest winner, no
membership) and the Governor's appointee holds the seat
(person + appointed membership).

Usage: build_vt_senate.py <district-slug> [--write]
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

REAPPORTIONMENT_SOURCE = {
    "url": ("https://legislature.vermont.gov/reports-and-research/"
            "research/reapportionment/"),
    "note": ("Vermont General Assembly, Reapportionment research "
             "page: the current Senate and House districts are "
             "those of the 2022 reapportionment -- H.722, enacted "
             "as 2022 Acts and Resolves No. 89 (signed April 6, "
             "2022) under Title 17, chapter 34A."),
    "retrieved": RETRIEVED,
}
ROSTER_URL = "https://legislature.vermont.gov/people/all/2026/Senate"
TERM = (" State senators serve two-year terms; the November 3, "
        "2026 general election decides the next term.")
RETURN_2024 = (" The contest page's cited official source is "
               "the Secretary of State's 'November 5, 2024 "
               "General Official Results.pdf'.")
SEAT_WORDS = {1: "single-member", 2: "two-member", 3: "three-member"}


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
        print("usage: build_vt_senate.py <district-slug> [--write]")
        return
    slug = args[0]
    data = json.loads((SCRIPTS / "vt_senate_data.json").read_text())
    if slug not in data:
        print(f"no senate data for {slug}")
        return
    d = data[slug]
    district = d["district"]
    seats = d["seats"]
    prefix = f"vt-senate-{slug}"
    post_id = f"{prefix}/state-senator"
    stem = post_id.replace("/", "-")
    jurisdiction_id = (f"ocd-jurisdiction/country:us/state:vt/"
                       f"sldu:{slug}/legislature")
    division_id = f"ocd-division/country:us/state:vt/sldu:{slug}"
    org_id = oid("organization", f"vt|senate|{post_id}")
    header = (f"# {district} Senate District -- VT legislative "
              f"pass (district + post + members + election "
              f"together);\n# issue #163 (VT master tracking).\n")

    db_url = (f"https://electionarchive.vermont.gov/contest/"
              f"{d['contest_id']}")
    cands = d["candidates"]
    winners = [c for c in cands if c.get("winner")]
    parts = []
    for i, c in enumerate(cands):
        suffix = " votes" if i == 0 else ""
        parts.append(f"{c['name']} ({c['party']}) "
                     f"{c['votes']:,}{suffix}")
    note = (f"Vermont Elections Database (Vermont Secretary of "
            f"State), contest page '2024 Nov 5, General Election, "
            f"State Senate, {district} District' (district "
            f"totals): " + "; ".join(parts)
            + f"; write-ins {d['write_ins']:,}.")
    note += RETURN_2024 + TERM
    transition = d.get("transition")
    if transition:
        # Both Senate transitions are in single-seat districts;
        # the membership skip below applies to the district's
        # only winner. (The House builder keys transitions per
        # winner instead.)
        assert seats == 1 and len(winners) == 1, \
            f"{slug}: transition in a multi-seat district"
        note += " " + transition["note"]
    db_source = {"url": db_url, "note": note,
                 "retrieved": RETRIEVED}
    roster_source = {
        "url": ROSTER_URL,
        "note": (f"Vermont General Assembly, All Senators "
                 f"directory (2025-2026 session): lists the "
                 f"sitting senator(s) for the {district} "
                 f"District."),
        "retrieved": RETRIEVED,
    }

    created = 0

    # 1. Jurisdiction
    jurisdiction = {
        "id": jurisdiction_id,
        "name": f"{district} district (Vermont Senate delegation)",
        "state": "vt",
        "division_id": division_id,
        "classification": "legislature",
        "government_form": (f"{SEAT_WORDS[seats]} district "
                            f"(Vermont Senate)"),
        "sources": [REAPPORTIONMENT_SOURCE, db_source],
    }
    created += dump(
        DATA_DIR / "jurisdictions" / "state" / f"{slug}-senate.yaml",
        jurisdiction, header, write)

    # 2. Organization
    org = {
        "id": org_id,
        "name": f"Vermont Senate -- {district} District",
        "jurisdiction_id": jurisdiction_id,
        "identifiers": [{"scheme": "civicmirror-office",
                         "identifier": post_id}],
        "status": "active",
        "sources": [REAPPORTIONMENT_SOURCE, db_source],
    }
    created += dump(
        DATA_DIR / "organizations" / "state" / f"{stem}.yaml",
        org, header, write)

    # 3. Post
    post = {
        "id": post_id,
        "organization_id": org_id,
        "title": "State Senator",
        "seats": seats,
        "sources": [REAPPORTIONMENT_SOURCE, db_source],
    }
    created += dump(
        DATA_DIR / "posts" / "state" / f"{stem}.yaml",
        post, header, write)

    # 4. Election + people + memberships
    contest_id = f"{prefix}/2024-11-05/state-senator"
    election_id = f"{prefix}/2024-11-05/general"
    winner_ids = []
    memberships_made = 0
    for w in winners:
        pslug = slugify(w["name"])
        pid = oid("person", f"vt|senate|{pslug}")
        winner_ids.append(pid)
        if transition:
            w_sources = [db_source] + [
                {**s, "retrieved": RETRIEVED}
                for s in transition["sources"]]
        else:
            w_sources = [db_source, roster_source]
        person = {
            "id": pid,
            "name": w["name"],
            "identifiers": [],
            "candidacies": [{
                "contest_id": contest_id,
                "election_id": election_id,
                "jurisdiction_id": jurisdiction_id,
                "office_id": post_id,
                "party": w["party"],
                "ballot_name": w["name"],
                "status": "active",
            }],
            "verification": {
                "status": "machine-extracted",
                "reviewed_on": RETRIEVED,
                "pipeline": "build_vt_senate",
            },
            "sources": w_sources,
        }
        created += dump(
            DATA_DIR / "people" / "state" / f"{pslug}.yaml",
            person, header, write)
        if not transition:
            mid = stem + "-" + pslug
            membership = {
                "id": mid,
                "person_id": pid,
                "organization_id": org_id,
                "post_id": post_id,
                "role": "State Senator",
                "how_seated": "elected",
                "sources": w_sources,
            }
            created += dump(
                DATA_DIR / "memberships" / "state" / f"{mid}.yaml",
                membership, header, write)
            memberships_made += 1

    if transition:
        sslug = slugify(transition["successor"])
        spid = oid("person", f"vt|senate|{sslug}")
        s_sources = [{**s, "retrieved": RETRIEVED}
                     for s in transition["sources"]]
        person = {
            "id": spid,
            "name": transition["successor"],
            "identifiers": [],
            "candidacies": [],
            "verification": {
                "status": "machine-extracted",
                "reviewed_on": RETRIEVED,
                "pipeline": "build_vt_senate",
            },
            "sources": s_sources,
        }
        created += dump(
            DATA_DIR / "people" / "state" / f"{sslug}.yaml",
            person, header, write)
        mid = stem + "-" + sslug
        membership = {
            "id": mid,
            "person_id": spid,
            "organization_id": org_id,
            "post_id": post_id,
            "role": "State Senator",
            "how_seated": "appointed",
            "sources": s_sources,
        }
        created += dump(
            DATA_DIR / "memberships" / "state" / f"{mid}.yaml",
            membership, header, write)
        memberships_made += 1

    election = {
        "id": election_id,
        "name": (f"{district} Senate District 2024-11-05 "
                 f"general election"),
        "date": "2024-11-05",
        "election_type": "general",
        "status": "official",
        "contests": [{
            "id": contest_id,
            "jurisdiction_id": jurisdiction_id,
            "office_id": post_id,
            "vote_for": seats,
            "candidate_ids": winner_ids,
            "result_status": "certified",
            "winners": [{"person_id": oid("person", f"vt|senate|{slugify(w['name'])}"),
                         "name": w["name"]} for w in winners],
        }],
        "sources": [db_source],
    }
    created += dump(
        DATA_DIR / "elections"
        / f"{prefix}--2024-11-05--general.yaml",
        election, header, write)

    print(f"{'Created' if write else 'Would create'} {created} "
          f"files for {district} Senate District "
          f"({len(winners)} winner(s), {memberships_made} "
          f"membership(s)).")


if __name__ == "__main__":
    main()
