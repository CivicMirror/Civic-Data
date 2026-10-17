#!/usr/bin/env python3
"""Generalized VT county builder (#163 county-tier fan-out).

Builds one county per invocation from its verified data file
(scripts/vt_county_data/<county>.json) and the post/org map
(scripts/vt_county_postmap.json), following the shape locked by
the Addison County worked example (build_vt_addison_county.py):
State's Attorney, Sheriff, and Assistant Judges trace to the
county's 2022 general election; the High Bailiff traces to 2024
(biennial, Vt. Const. Ch. II s.43; the other offices serve
four-year terms from Feb 1 under s.50).

Data-file conventions:
- Every office lists the ballot candidates exactly as the VT
  Elections Database prints them, with "winner": true on the
  winners. Losers are not modeled as people (repo convention).
- A "sa_transition" block means the 2022 SA winner no longer
  holds the office: the winner gets a person + candidacy + the
  contest winner entry but NO membership; the named successor
  gets a person + an appointed membership sourced to the
  transition sources.
- A High Bailiff block with "no_candidates": true records the
  contest with no candidates and no winner -- the database
  states 'No qualifying candidates in this contest' and names
  no write-in winner, so no holder is minted for the seat.

Usage: build_vt_county.py <county-slug> [--write]
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

TERM_4YR = (
    " The office serves a four-year term beginning February 1 "
    "after the election (Vermont Constitution, Chapter II, "
    "section 50); the November 3, 2026 general election decides "
    "the next term."
)
TERM_HB = (
    " High bailiffs are elected biennially (Vermont "
    "Constitution, Chapter II, section 43); the November 3, "
    "2026 general election decides the next term."
)
RETURN_2022 = (
    " The contest page's cited official source is the official "
    "return vt-2022_11_08_General_ALL.pdf."
)
RETURN_2024 = (
    " The contest page's cited official source is the Secretary "
    "of State's 'November 5, 2024 General Official Results.pdf'."
)
LABELS = {
    "states-attorney": "State's Attorney (listed as District Attorney)",
    "sheriff": "Sheriff (listed as County Sheriff)",
    "assistant-judge": "Assistant Judge",
    "high-bailiff": "High Bailiff",
}
ROLES = {
    "states-attorney": "State's Attorney",
    "sheriff": "Sheriff",
    "assistant-judge": "Assistant Judge",
    "high-bailiff": "High Bailiff",
}


def oid(kind, key):
    return f"ocd-{kind}/{uuid.uuid5(NS, kind + '|' + key)}"


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def contest_note(county_name, office_key, office):
    year = office["election"]
    date_label = "2022 Nov 8" if year == "2022" else "2024 Nov 5"
    label = LABELS[office_key]
    head = (f"Vermont Elections Database (Vermont Secretary of "
            f"State), contest page '{date_label}, General "
            f"Election, {label}, {county_name} County'")
    cands = office.get("candidates", [])
    wi = office.get("write_ins")
    if office_key == "assistant-judge":
        head += f" (vote for {office.get('vote_for', 2)}; county totals): "
    else:
        head += " (county totals): "
    if office.get("write_in_winner"):
        w = office["candidates"][0]
        body = (f"no candidates qualified for the ballot; the "
                f"only votes recorded are write-ins: {wi:,}. "
                f"The canvass certified a write-in winner: "
                f"{w['name']}, {w['votes']:,} write-in votes.")
    elif office.get("no_candidates"):
        body = (f"the contest page states 'No qualifying "
                f"candidates in this contest'; the only votes "
                f"recorded are write-ins: {wi:,}. No winner is "
                f"named in the database and none is recorded "
                f"here, and no holder is minted for the seat.")
    else:
        parts = []
        for i, c in enumerate(cands):
            suffix = " votes" if i == 0 else ""
            parts.append(f"{c['name']} ({c['party']}) "
                         f"{c['votes']:,}{suffix}")
        body = "; ".join(parts) + f"; write-ins {wi:,}"
        if (office_key == "assistant-judge" and len(cands) == 2
                and office.get("vote_for", 2) == 2):
            body += (f". {cands[0]['name']} and {cands[1]['name']} "
                     f"were the only two candidates for the two "
                     f"seats")
        body += "."
    note = head + body
    note += RETURN_2022 if year == "2022" else RETURN_2024
    note += TERM_HB if office_key == "high-bailiff" else TERM_4YR
    if office.get("note_extra"):
        note += " " + office["note_extra"]
    if office.get("final_note"):
        note += " " + office["final_note"]
    return note


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
    print(f"{'WRITE' if write else 'WOULD WRITE'}: "
          f"{path.relative_to(REPO)}")
    return 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    write = "--write" in sys.argv
    if len(args) != 1:
        print("usage: build_vt_county.py <county-slug> [--write]")
        return
    slug = args[0]
    data = json.loads(
        (SCRIPTS / "vt_county_data" / f"{slug}.json").read_text())
    postmap = json.loads(
        (SCRIPTS / "vt_county_postmap.json").read_text())
    if slug == "addison" or slug not in postmap:
        print(f"no postmap entry for {slug}")
        return
    county_name = data["name"].replace(" County", "")
    prefix = f"{slug}-vt-county"
    jurisdiction_id = (f"ocd-jurisdiction/country:us/state:vt/"
                       f"county:{slug}/government")
    header = (f"# {county_name} County -- VT county tier fan-out "
              f"(posts + holders + elections together);\n"
              f"# issue #163 (VT master tracking).\n")
    transition = data.get("sa_transition")

    dept_source = {
        "url": data["dept_url"],
        "note": (
            f"Vermont Department of State's Attorneys and "
            f"Sheriffs, {county_name} County office page: lists "
            f"{data['dept_sa']} as State's Attorney and "
            f"{data['dept_sheriff']} as Sheriff -- the sitting "
            f"holders as of the retrieval date."
        ),
        "retrieved": RETRIEVED,
    }

    elections = {}
    for year, edate in (("2022", "2022-11-08"), ("2024", "2024-11-05")):
        eid = f"{prefix}/{edate}/general"
        elections[year] = {
            "id": eid,
            "name": f"{county_name} County {edate} general election",
            "date": edate,
            "election_type": "general",
            "status": "official",
            "contests": [],
            "sources": [],
            "_file": f"{prefix}--{edate}--general.yaml",
        }

    created = 0
    people_count = 0
    membership_count = 0

    for office_key in ("states-attorney", "sheriff",
                       "assistant-judge", "high-bailiff"):
        office = data["offices"][office_key]
        post = postmap[slug][office_key]
        year = office["election"]
        election = elections[year]
        contest_id = (f"{prefix}/{election['date']}/"
                      f"{office_key}")
        db_source = {"url": office["db_url"],
                     "note": contest_note(county_name, office_key,
                                          office),
                     "retrieved": RETRIEVED}
        election["sources"].append(db_source)

        cands = office.get("candidates", [])
        winners = [c for c in cands if c.get("winner")]
        vote_for = office.get("vote_for", 1)
        if cands:
            assert len(winners) == vote_for, (
                f"{slug} {office_key}: {len(winners)} winners "
                f"!= vote_for {vote_for}")

        candidate_ids = []
        winner_entries = []
        is_transition_sa = (office_key == "states-attorney"
                            and transition)
        for cand in winners:
            pslug = slugify(cand["name"])
            pid = oid("person", f"vt|{slug}-county|{pslug}")
            candidate_ids.append(pid)
            winner_entries.append({"person_id": pid,
                                   "name": cand["name"]})
            sources = [db_source]
            if office_key in ("states-attorney", "sheriff") \
                    and not is_transition_sa:
                sources = sources + [dept_source]
            for extra in office.get("extra_sources", []):
                sources = sources + [{**extra,
                                      "retrieved": RETRIEVED}]
            person = {
                "id": pid,
                "name": cand["name"],
                "identifiers": [],
                "candidacies": [{
                    "contest_id": contest_id,
                    "election_id": election["id"],
                    "jurisdiction_id": jurisdiction_id,
                    "office_id": post["post_id"],
                    "party": cand["party"],
                    "ballot_name": cand["name"],
                    "status": "active",
                }],
                "verification": {
                    "status": "machine-extracted",
                    "reviewed_on": RETRIEVED,
                    "pipeline": "build_vt_county",
                },
                "sources": sources,
            }
            created += dump(
                DATA_DIR / "people" / "county" / f"{pslug}.yaml",
                person, header, write)
            people_count += 1
            if is_transition_sa:
                continue  # winner no longer holds; no membership
            mid = post["post_id"].replace("/", "-") + "-" + pslug
            membership = {
                "id": mid,
                "person_id": pid,
                "organization_id": post["org_id"],
                "post_id": post["post_id"],
                "role": ROLES[office_key],
                "how_seated": "elected",
                "sources": sources,
            }
            created += dump(
                DATA_DIR / "memberships" / "county" / f"{mid}.yaml",
                membership, header, write)
            membership_count += 1

        if is_transition_sa:
            succ_name = transition["interim_and_current"]
            pslug = slugify(succ_name)
            pid = oid("person", f"vt|{slug}-county|{pslug}")
            succ_sources = [
                {**s, "retrieved": RETRIEVED}
                for s in transition["sources"]
            ]
            person = {
                "id": pid,
                "name": succ_name,
                "identifiers": [],
                "candidacies": [],
                "verification": {
                    "status": "machine-extracted",
                    "reviewed_on": RETRIEVED,
                    "pipeline": "build_vt_county",
                },
                "sources": succ_sources,
            }
            created += dump(
                DATA_DIR / "people" / "county" / f"{pslug}.yaml",
                person, header, write)
            people_count += 1
            mid = post["post_id"].replace("/", "-") + "-" + pslug
            membership = {
                "id": mid,
                "person_id": pid,
                "organization_id": post["org_id"],
                "post_id": post["post_id"],
                "role": ROLES[office_key],
                "how_seated": "appointed",
                "sources": succ_sources,
            }
            created += dump(
                DATA_DIR / "memberships" / "county" / f"{mid}.yaml",
                membership, header, write)
            membership_count += 1

        # A no-candidate contest with no certified write-in
        # winner has no winner to certify; its figures are the
        # official results, so it is recorded with
        # result_status "official" (a certified contest
        # requires at least one winner under repo validation).
        status = "official" if (office.get("no_candidates")
                                and not winner_entries) \
            else "certified"
        election["contests"].append({
            "id": contest_id,
            "jurisdiction_id": jurisdiction_id,
            "office_id": post["post_id"],
            "vote_for": vote_for,
            "candidate_ids": candidate_ids,
            "result_status": status,
            "winners": winner_entries,
        })

    for year in ("2022", "2024"):
        election = elections[year]
        fname = election.pop("_file")
        created += dump(DATA_DIR / "elections" / fname, election,
                        header, write)

    print(f"{'Created' if write else 'Would create'} {created} "
          f"files for {county_name} County ({people_count} people, "
          f"{membership_count} memberships, 2 elections).")


if __name__ == "__main__":
    main()
