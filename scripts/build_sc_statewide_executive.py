#!/usr/bin/env python3
"""Build SC 2022 statewide executive worked example for Civic-Data issue #177.

Source: SC State Election Commission, Election History (ElectionStats,
electionhistory.scvotes.gov) per-office Search Results CSV exports, 2022-11-08
general election contests, county-division rows aggregated across all 46
counties (the export duplicates every vote in county + precinct rows; only
county rows are summed). Winners derived from totals; "Write-In" is an unnamed
aggregate and is never seated; the export's lone "Unknown Candidate" row
(Superintendent, 0 votes) is an artifact and is excluded.

Governor/Lieutenant Governor run as a joint ticket in SC since 2018: the
ElectionStats candidate string names both ("Henry McMaster and Pamela
Evette"). The ticket is modeled as two contests (governor,
lieutenant-governor) over the same ElectionStats contest 2183, each person
carrying the full ticket string as ballot_name.

Comptroller General: Richard Eckstrom won the 2022 election and resigned
effective April 30, 2023 (Governor's office, Executive Order 2023-12 release,
May 12, 2023). His membership carries that end date; his appointed successor
is a separate succession pass and is NOT built here.

No existing SC person files are touched: all 18 candidates are new people
(slugs checked against data/us/sc/people/ -- zero collisions; Attorney
General Alan Wilson is not U.S. Rep. Joe Wilson).
"""
import json, re, uuid
from pathlib import Path

TREE = Path(__file__).resolve().parent.parent
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
TODAY = "2026-10-25"
JUR = "ocd-jurisdiction/country:us/state:sc/executive"
ELEC_ID = "sc/2022-11-08/general"
HIST = "https://electionhistory.scvotes.gov"

data = json.loads((Path.home() / "workspace/sc177/exec2022.json").read_text())

# post slug -> (title, ElectionStats office name)
POSTS = {
    "governor": ("Governor", "Governor"),
    "lieutenant-governor": ("Lieutenant Governor", "Governor"),
    "secretary-of-state": ("Secretary of State", "Secretary of State"),
    "attorney-general": ("Attorney General", "Attorney General"),
    "state-treasurer": ("State Treasurer", "State Treasurer"),
    "comptroller-general": ("Comptroller General", "Comptroller General"),
    "commissioner-of-agriculture": ("Commissioner of Agriculture", "Commissioner of Agriculture"),
    "superintendent-of-education": ("State Superintendent of Education", "State Superintendent of Public Education"),
}
ORG_ID = "ocd-organization/" + str(uuid.uuid5(NS, "organization|sc|executive-branch"))
SKIP = {"Total Votes Cast", "Total Ballots Cast", "Write-In", "Overvotes/Undervotes", "Unknown Candidate"}

def slugify(name):
    s = name.lower().replace("(", "").replace(")", "").replace(".", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)

def person_id_for(slug):
    return "ocd-person/" + str(uuid.uuid5(NS, f"person|sc|state|{slug}"))

def fmt(n):
    return f"{n:,}"

def named_candidates(office_name):
    return [c for c in data[office_name]["candidates"] if c["name"] not in SKIP]

def write_in_votes(office_name):
    for c in data[office_name]["candidates"]:
        if c["name"] == "Write-In":
            return c["votes"]
    return 0

def contest_url(office_name):
    return f"{HIST}/contest/{data[office_name]['contest_id']}"

def contest_note(office_name, title):
    parts = "; ".join(f"{c['name']} ({c['party']}) {fmt(c['votes'])}" for c in named_candidates(office_name))
    wi = write_in_votes(office_name)
    if wi:
        parts += f"; Write-In {fmt(wi)}"
    w = named_candidates(office_name)[0]
    return (f"South Carolina State Election Commission, Election History (ElectionStats) results for the "
            f"November 8, 2022 general election, {title} contest (ElectionStats contest "
            f"{data[office_name]['contest_id']}), county-division rows aggregated across all 46 counties: "
            f"{parts}. {w['name']} won with {fmt(w['votes'])} votes.")

def source_yaml(office_name, title, indent=""):
    note = contest_note(office_name, title).replace("'", "''")
    return (f"{indent}- url: {contest_url(office_name)}\n"
            f"{indent}  note: '{note}'\n"
            f"{indent}  retrieved: '{TODAY}'\n")

# Resolve people: office post slug -> list of candidate dicts (+person fields)
# Governor ticket: split combined strings into (person_name, ballot_name, party, votes, post_slug)
people = {}   # slug -> dict(name, pid, file, candidacies[])
contests = {} # post slug -> list of candidate entries {slug, name, ballot_name, party, votes}

def add_person(name, ballot_name, party, post_slug, office_name):
    slug = slugify(name)
    if slug not in people:
        path = TREE / "data/us/sc/people/state" / f"{slug}.yaml"
        assert not path.exists(), f"slug collision: {path}"
        people[slug] = {"name": name, "pid": person_id_for(slug), "file": path, "candidacies": []}
    people[slug]["candidacies"].append({
        "contest_id": f"sc/2022-11-08/{post_slug}",
        "office_id": f"sc/{post_slug}",
        "party": party, "ballot_name": ballot_name,
        "office_name": office_name, "post_slug": post_slug,
    })
    contests.setdefault(post_slug, []).append({**people[slug], "ballot_name": ballot_name,
                                               "party": party, "slug": slug})

for post_slug, (title, office_name) in POSTS.items():
    if post_slug == "lieutenant-governor":
        continue  # handled from the Governor ticket strings below
    if post_slug == "governor":
        for c in named_candidates("Governor"):
            top, mate = [p.strip() for p in c["name"].replace(" and ", "/").split("/")]
            add_person(top, c["name"], c["party"], "governor", "Governor")
            add_person(mate, c["name"], c["party"], "lieutenant-governor", "Governor")
        continue
    for c in named_candidates(office_name):
        add_person(c["name"], c["name"], c["party"], post_slug, office_name)
# votes for ticket contests
for post_slug in ("governor", "lieutenant-governor"):
    for e in contests[post_slug]:
        cand = next(x for x in named_candidates("Governor") if x["name"] == e["ballot_name"])
        e["votes"] = cand["votes"]
for post_slug, (title, office_name) in POSTS.items():
    if post_slug in ("governor", "lieutenant-governor"):
        continue
    for e in contests[post_slug]:
        cand = next(x for x in named_candidates(office_name) if x["name"] == e["ballot_name"])
        e["votes"] = cand["votes"]

winners = {ps: max(es, key=lambda e: e["votes"]) for ps, es in contests.items()}

# 1. Jurisdiction
jur_dir = TREE / "data/us/sc/jurisdictions/state"
jur_dir.mkdir(parents=True, exist_ok=True)
(jur_dir / "sc-executive.yaml").write_text(
    "# Built for the SC statewide executive worked example (Civic-Data issue\n"
    "# #177) from the SC State Election Commission Election History results.\n"
    f"id: {JUR}\n"
    "name: South Carolina (statewide executive branch)\n"
    "state: sc\n"
    "division_id: ocd-division/country:us/state:sc\n"
    "classification: executive\n"
    "sources:\n"
    f"- url: {HIST}/search?gf=e\n"
    "  note: SC State Election Commission Election History (ElectionStats) search -- the official results system whose per-office CSV exports source the November 8, 2022 general election contests built under this jurisdiction.\n"
    f"  retrieved: '{TODAY}'\n")
print("JURISDICTION sc-executive.yaml")

# 2. Organization
org_dir = TREE / "data/us/sc/organizations/state"
org_dir.mkdir(parents=True, exist_ok=True)
(org_dir / "sc-executive-branch.yaml").write_text(
    "# Built for the SC statewide executive worked example (Civic-Data issue #177).\n"
    f"id: {ORG_ID}\n"
    "name: South Carolina Executive Branch\n"
    f"jurisdiction_id: {JUR}\n"
    "identifiers: []\n"
    "sources:\n"
    f"- url: {HIST}/search?gf=e\n"
    "  note: SC State Election Commission Election History (ElectionStats) search; the organization's posts are the state's elected executive offices as contested in the November 8, 2022 general election.\n"
    f"  retrieved: '{TODAY}'\n")
print("ORG sc-executive-branch.yaml")

# 3. Posts
post_dir = TREE / "data/us/sc/posts/state"
post_dir.mkdir(parents=True, exist_ok=True)
for post_slug, (title, office_name) in POSTS.items():
    (post_dir / f"sc-{post_slug}.yaml").write_text(
        "# Built for the SC statewide executive worked example (Civic-Data issue #177).\n"
        f"id: sc/{post_slug}\n"
        f"organization_id: {ORG_ID}\n"
        f"title: {title}\n"
        "seats: 1\n"
        "identifiers: []\n"
        "sources:\n"
        + source_yaml(office_name, title))
    print("POST", post_slug)

# 4. People
ppl_dir = TREE / "data/us/sc/people/state"
ppl_dir.mkdir(parents=True, exist_ok=True)
for slug, p in people.items():
    lines = ["# Minted from the SC State Election Commission Election History",
             "# official Nov. 8, 2022 general election results (statewide",
             "# executive worked example, Civic-Data issue #177).",
             f"id: {p['pid']}", f"name: {p['name']}", "identifiers: []", "candidacies:"]
    srcs = []
    for cd in p["candidacies"]:
        lines += [f"- contest_id: {cd['contest_id']}",
                  f"  election_id: {ELEC_ID}",
                  f"  jurisdiction_id: {JUR}",
                  f"  office_id: {cd['office_id']}",
                  f"  party: {cd['party']}",
                  f"  ballot_name: '{cd['ballot_name']}'",
                  "  status: active"]
        srcs.append(source_yaml(cd["office_name"], POSTS[cd["post_slug"]][0]))
    lines += ["verification:", "  status: unverified", "  pipeline: build_sc_statewide_executive", "sources:"]
    body = "\n".join(lines) + "\n" + "".join(srcs)
    p["file"].write_text(body)
    print("PERSON", p["file"].name, p["pid"])

# 5. Memberships (winners)
mem_dir = TREE / "data/us/sc/memberships/state"
mem_dir.mkdir(parents=True, exist_ok=True)
for post_slug, (title, office_name) in POSTS.items():
    w = winners[post_slug]
    surname = w["slug"].split("-")[-1]
    mid = f"sc-{post_slug}-{surname}"
    body = ("# Minted from the SC State Election Commission Election History\n"
            "# official Nov. 8, 2022 general election results (Civic-Data issue #177).\n"
            f"id: {mid}\n"
            f"person_id: {w['pid']}\n"
            f"organization_id: {ORG_ID}\n"
            f"post_id: sc/{post_slug}\n"
            f"role: {title}\n"
            "seat: At-Large\n"
            "start: '2023'\n"
            "how_seated: elected\n")
    if post_slug == "comptroller-general":
        body += "end: '2023-04-30'\n"
    body += "sources:\n" + source_yaml(office_name, title)
    if post_slug == "comptroller-general":
        body += ("- url: https://governor.sc.gov/news/2023-05/gov-henry-mcmaster-appoints-brian-gaines-comptroller-general\n"
                 "  note: 'Office of the Governor, May 12, 2023: Governor McMaster issued Executive Order 2023-12 appointing Brian Gaines as Comptroller General following the April 30, 2023 resignation of Richard Eckstrom. Eckstrom''s elected membership therefore ends 2023-04-30; the appointed succession is a separate pass and is not built in this worked example.'\n"
                 f"  retrieved: '{TODAY}'\n")
    (mem_dir / f"{mid}.yaml").write_text(body)
    print("MEMBERSHIP", mid)

# 6. Election file
lines = ["# Built from the SC State Election Commission Election History",
         "# (ElectionStats) official results for the November 8, 2022 general",
         "# election, per-office CSV exports aggregated from county-division",
         "# rows across all 46 counties. Statewide executive worked example,",
         "# Civic-Data issue #177.",
         f"id: {ELEC_ID}",
         "name: South Carolina 2022-11-08 general election",
         "date: '2022-11-08'",
         "election_type: general",
         "status: certified",
         "contests:"]
for post_slug, (title, office_name) in POSTS.items():
    lines += [f"- id: sc/2022-11-08/{post_slug}",
              f"  jurisdiction_id: {JUR}",
              f"  office_id: sc/{post_slug}",
              "  vote_for: 1",
              "  candidate_ids:"]
    for e in contests[post_slug]:
        lines.append(f"  - {e['pid']}")
    w = winners[post_slug]
    lines += ["  result_status: certified",
              "  winners:",
              f"  - person_id: {w['pid']}",
              f"    name: '{w['name']}'",
              f"    party: {w['party']}",
              f"    votes: {w['votes']}"]
lines += ["sources:",
          f"- url: {HIST}/search?gf=e",
          "  note: 'SC State Election Commission Election History (ElectionStats): the official historical results system. This record covers the eight statewide executive contests of the November 8, 2022 general election; totals are aggregated from the per-office Search Results CSV exports using county-division rows only (the exports duplicate each vote in county and precinct rows). Write-In rows are unnamed aggregates and seat no one; the Superintendent of Education export also carries an \"Unknown Candidate\" artifact row with 0 votes, which is excluded. Governor and Lieutenant Governor are a joint ticket: both contests rest on ElectionStats contest 2183 and share the ticket vote totals.'",
          f"  retrieved: '{TODAY}'"]
elec_dir = TREE / "data/us/sc/elections"
elec_dir.mkdir(parents=True, exist_ok=True)
(elec_dir / "sc--2022-11-08--general.yaml").write_text("\n".join(lines) + "\n")
print("ELECTION written")
print(f"COUNTS people={len(people)} posts={len(POSTS)} memberships={len(POSTS)} contests={len(POSTS)}")
