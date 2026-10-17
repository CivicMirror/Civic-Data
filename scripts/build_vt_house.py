#!/usr/bin/env python3
"""VT House builder (#163 legislative pass, House chamber).

Builds one House district per invocation from the verified
data file (scripts/vt_house_data.json): sldl jurisdiction +
district organization + State Representative post (1-2 seats)
+ the district's 2024 winners (people + memberships) + the
district's 2024 election record, together, following Walter's
VT build order and the repo's MA legislative precedent
(sldl divisions, jurisdiction .../legislature, classification
legislature).

Districts are those of Act 89 of 2022 (H.722): 109 districts,
150 seats. Winners trace to the November 5, 2024 general
election (Vermont Elections Database; figures verified
against the database's own contest CSVs for all 109
districts). Current-holder check: the General Assembly's All
Representatives directory (2025-2026 session) -- 142 of 150
winners still hold their seats; 8 resigned and carry a
per-winner "transition" block in the data file: the departed
winner keeps the win (person + candidacy + contest winner,
no membership) and the Governor's appointee holds the seat
(person + appointed membership).

Two winners already exist as people in the county tier and
are REUSED (candidacy appended to the existing record, never
re-created): William "Will" Greer (Bennington County high
bailiff) and David Yacovone (Lamoille County assistant
judge). See REUSE below.

Usage: build_vt_house.py <district-slug> [--write]
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
ROSTER_URL = "https://legislature.vermont.gov/people/all/2026/House"
TERM = (" State representatives serve two-year terms; the "
        "November 3, 2026 general election decides the next "
        "term.")
RETURN_2024 = (" The contest page's cited official source is "
               "the Secretary of State's 'November 5, 2024 "
               "General Official Results.pdf'.")
SEAT_WORDS = {1: "single-member", 2: "two-member"}

# Person slugs that already exist in the county tier and must
# be reused (identity verified -- see module docstring).
REUSE = {
    "william-will-greer": "data/us/vt/people/county/"
                          "william-will-greer.yaml",
    "david-yacovone": "data/us/vt/people/county/"
                      "david-yacovone.yaml",
}


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


def reuse_person(pslug, candidacy, sources, write):
    """Append a candidacy + sources to an existing person file.
    Returns (person_id, changed)."""
    path = REPO / REUSE[pslug]
    text = path.read_text(encoding="utf-8")
    header_lines = []
    for line in text.splitlines(keepends=True):
        if line.startswith("#"):
            header_lines.append(line)
        else:
            break
    doc = yaml.safe_load(text)
    pid = doc["id"]
    changed = False
    have = {c["contest_id"] for c in doc.get("candidacies", [])}
    if candidacy["contest_id"] not in have:
        doc.setdefault("candidacies", []).append(candidacy)
        changed = True
    have_urls = {s["url"] for s in doc.get("sources", [])}
    for s in sources:
        if s["url"] not in have_urls:
            doc.setdefault("sources", []).append(s)
            changed = True
    if write and changed:
        path.write_text(
            "".join(header_lines)
            + yaml.safe_dump(doc, sort_keys=False,
                             allow_unicode=True),
            encoding="utf-8")
        print(f"REUSE+APPEND: {path.relative_to(REPO)}")
    elif changed:
        print(f"WOULD REUSE+APPEND: {path.relative_to(REPO)}")
    else:
        print(f"REUSE (already current): {path.relative_to(REPO)}")
    return pid, changed


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    write = "--write" in sys.argv
    if len(args) != 1:
        print("usage: build_vt_house.py <district-slug> [--write]")
        return
    slug = args[0]
    data = json.loads((SCRIPTS / "vt_house_data.json").read_text())
    if slug not in data:
        print(f"no house data for {slug}")
        return
    d = data[slug]
    district = d["district"]
    seats = d["seats"]
    prefix = f"vt-house-{slug}"
    post_id = f"{prefix}/state-representative"
    stem = post_id.replace("/", "-")
    jurisdiction_id = (f"ocd-jurisdiction/country:us/state:vt/"
                       f"sldl:{slug}/legislature")
    division_id = f"ocd-division/country:us/state:vt/sldl:{slug}"
    org_id = oid("organization", f"vt|house|{post_id}")
    header = (f"# {district} House District -- VT legislative "
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
            f"State Representative, {district} District' "
            f"(district totals): " + "; ".join(parts)
            + f"; write-ins {d['write_ins']:,}.")
    note += RETURN_2024 + TERM
    transition = d.get("transition")
    if transition:
        note += " " + transition["note"]
    db_source = {"url": db_url, "note": note,
                 "retrieved": RETRIEVED}
    roster_source = {
        "url": ROSTER_URL,
        "note": (f"Vermont General Assembly, All Representatives "
                 f"directory (2025-2026 session): lists the "
                 f"sitting representative(s) for the {district} "
                 f"District."),
        "retrieved": RETRIEVED,
    }

    created = 0

    # 1. Jurisdiction
    jurisdiction = {
        "id": jurisdiction_id,
        "name": (f"{district} district (Vermont House of "
                 f"Representatives delegation)"),
        "state": "vt",
        "division_id": division_id,
        "classification": "legislature",
        "government_form": (f"{SEAT_WORDS[seats]} district "
                            f"(Vermont House of "
                            f"Representatives)"),
        "sources": [REAPPORTIONMENT_SOURCE, db_source],
    }
    created += dump(
        DATA_DIR / "jurisdictions" / "state" / f"{slug}-house.yaml",
        jurisdiction, header, write)

    # 2. Organization
    org = {
        "id": org_id,
        "name": (f"Vermont House of Representatives -- "
                 f"{district} District"),
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
        "title": "State Representative",
        "seats": seats,
        "sources": [REAPPORTIONMENT_SOURCE, db_source],
    }
    created += dump(
        DATA_DIR / "posts" / "state" / f"{stem}.yaml",
        post, header, write)

    # 4. Election + people + memberships
    contest_id = f"{prefix}/2024-11-05/state-representative"
    election_id = f"{prefix}/2024-11-05/general"
    winner_ids = []
    memberships_made = 0
    departed = transition["winner"] if transition else None
    for w in winners:
        pslug = slugify(w["name"])
        candidacy = {
            "contest_id": contest_id,
            "election_id": election_id,
            "jurisdiction_id": jurisdiction_id,
            "office_id": post_id,
            "party": w["party"],
            "ballot_name": w["name"],
            "status": "active",
        }
        is_departed = (w["name"] == departed)
        if is_departed:
            w_sources = [db_source] + [
                {**s, "retrieved": RETRIEVED}
                for s in transition["sources"]]
        else:
            w_sources = [db_source, roster_source]
        if pslug in REUSE:
            pid, changed = reuse_person(pslug, candidacy,
                                        w_sources, write)
            created += 1 if changed else 0
        else:
            pid = oid("person", f"vt|house|{pslug}")
            person = {
                "id": pid,
                "name": w["name"],
                "identifiers": [],
                "candidacies": [candidacy],
                "verification": {
                    "status": "machine-extracted",
                    "reviewed_on": RETRIEVED,
                    "pipeline": "build_vt_house",
                },
                "sources": w_sources,
            }
            created += dump(
                DATA_DIR / "people" / "state" / f"{pslug}.yaml",
                person, header, write)
        winner_ids.append(pid)
        if not is_departed:
            mid = stem + "-" + pslug
            membership = {
                "id": mid,
                "person_id": pid,
                "organization_id": org_id,
                "post_id": post_id,
                "role": "State Representative",
                "how_seated": "elected",
                "sources": w_sources,
            }
            created += dump(
                DATA_DIR / "memberships" / "state" / f"{mid}.yaml",
                membership, header, write)
            memberships_made += 1

    if transition:
        sslug = slugify(transition["successor"])
        spid = oid("person", f"vt|house|{sslug}")
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
                "pipeline": "build_vt_house",
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
            "role": "State Representative",
            "how_seated": "appointed",
            "sources": s_sources,
        }
        created += dump(
            DATA_DIR / "memberships" / "state" / f"{mid}.yaml",
            membership, header, write)
        memberships_made += 1

    election = {
        "id": election_id,
        "name": (f"{district} House District 2024-11-05 "
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
            "winners": [{"person_id": pid, "name": w["name"]}
                        for pid, w in zip(winner_ids, winners)],
        }],
        "sources": [db_source],
    }
    created += dump(
        DATA_DIR / "elections"
        / f"{prefix}--2024-11-05--general.yaml",
        election, header, write)

    print(f"{'Created/updated' if write else 'Would create'} "
          f"{created} files for {district} House District "
          f"({len(winners)} winner(s), {memberships_made} "
          f"membership(s)).")


if __name__ == "__main__":
    main()
