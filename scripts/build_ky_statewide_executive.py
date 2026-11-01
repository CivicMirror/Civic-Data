#!/usr/bin/env python3
"""Build KY 2023 statewide executive pass for Civic-Data issue #195.

Source: Commonwealth of Kentucky, State Board of Elections / Secretary of
State, "Certification of Election Results for 2023 General Election Final"
(official certified results book for the November 7, 2023 general election,
county-by-county tables with statewide Total Votes rows, read firsthand
2026-11-01). Winners derived from the certified totals.

Governor/Lieutenant Governor run as a joint ticket in Kentucky (Ky. Const.
sec. 70): the certified book lists the ticket's two names together. The
ticket is modeled as two contests (governor, lieutenant-governor) sharing
the ticket vote totals, one candidacy per person carrying the full ticket
string as ballot_name.

Named write-in candidates shown in the certified book (the Fishback ticket
for Governor, 83 votes; Kenneth C. Moellman Jr. for Secretary of State, 518
votes) are modeled as candidacies with party "Write-In". The State
Treasurer contest's 155 write-in votes are an unnamed aggregate: noted in
the contest source note, never a candidacy, and they seat no one.

Membership start years are the constitutional term-start years, given as
partial (year-only) dates: the Governor and Lieutenant Governor were
inaugurated December 12, 2023 (second Tuesday after the election), and the
other five officers took office January 1, 2024 (first Monday of January).
No day-level start is asserted beyond the year.

No existing KY person files are touched: all 17 candidates are new people
(slugs checked against data/us/ky/people/ -- zero collisions, 2026-11-01;
KY's only built tier was federal: Barr, Guthrie, McGarvey, Massie, Rogers,
Comer, McConnell, Paul).
"""
import re, uuid
from pathlib import Path

TREE = Path(__file__).resolve().parent.parent
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
TODAY = "2026-11-01"
JUR = "ocd-jurisdiction/country:us/state:ky/executive"
ELEC_ID = "ky/2023-11-07/general"
CERT = ("https://elect.ky.gov/results/2020-2029/Documents/"
        "Certification%20of%20Election%20Results%20for%202023%20General%20Election%20Final.pdf")

# post slug -> (title, certified office heading, term-start year)
POSTS = {
    "governor": ("Governor", "Governor", "2023"),
    "lieutenant-governor": ("Lieutenant Governor", "Governor", "2023"),
    "secretary-of-state": ("Secretary of State", "Secretary of State", "2024"),
    "attorney-general": ("Attorney General", "Attorney General", "2024"),
    "auditor-of-public-accounts": ("Auditor of Public Accounts", "Auditor of Public Accounts", "2024"),
    "state-treasurer": ("State Treasurer", "State Treasurer", "2024"),
    "commissioner-of-agriculture": ("Commissioner of Agriculture", "Commissioner of Agriculture", "2024"),
}
ORG_ID = "ocd-organization/" + str(uuid.uuid5(NS, "organization|ky|executive-branch"))

# Candidates per certified contest:
# (person name, ballot_name, party, votes) -- governor entries are tickets:
# (gov name, lt gov name, ticket ballot string, party, ticket votes)
GOV_TICKETS = [
    ("Andy Beshear", "Jacqueline Coleman", 'Andy Beshear and Jacqueline Coleman', "Democratic", 694482),
    ("Daniel Cameron", "Robby Mills", 'Daniel Cameron and Robert M. "Robby" Mills', "Republican", 627457),
    ("Brian Fishback", "William Fishback", 'Brian Fishback and William Fishback', "Write-In", 83),
]
CONTESTS = {
    "secretary-of-state": [
        ("Michael Adams", "Michael Adams", "Republican", 785237),
        ("Charles Wheatley", 'Charles "Buddy" Wheatley', "Democratic", 510090),
        ("Kenneth C. Moellman Jr.", "Kenneth C. Moellman Jr.", "Write-In", 518),
    ],
    "attorney-general": [
        ("Russell Coleman", "Russell Coleman", "Republican", 752692),
        ("Pamela Stevenson", "Pamela Stevenson", "Democratic", 544748),
    ],
    "auditor-of-public-accounts": [
        ("Allison Ball", "Allison Ball", "Republican", 783217),
        ("Kim Reeder", 'Kimberley "Kim" Reeder', "Democratic", 505924),
    ],
    "state-treasurer": [
        ("Mark Metcalf", "Mark H. Metcalf", "Republican", 735522),
        ("Michael Bowman", "Michael Bowman", "Democratic", 549461),
    ],
    "commissioner-of-agriculture": [
        ("Jonathan Shell", "Jonathan Shell", "Republican", 763468),
        ("Sierra Enlow", "Sierra Enlow", "Democratic", 522521),
    ],
}
UNNAMED_WRITEIN = {"state-treasurer": 155}  # aggregate only, in note text


def slugify(name):
    s = name.lower().replace("(", "").replace(")", "").replace(".", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)


def person_id_for(slug):
    return "ocd-person/" + str(uuid.uuid5(NS, f"person|ky|state|{slug}"))


def fmt(n):
    return f"{n:,}"


people = {}    # slug -> dict(name, pid, candidacies[])
contests = {}  # post slug -> list of entries {slug, name, ballot_name, party, votes}


def add_person(name, ballot_name, party, post_slug, votes):
    slug = slugify(name)
    if slug not in people:
        path = TREE / "data/us/ky/people/state" / f"{slug}.yaml"
        assert not path.exists(), f"slug collision: {path}"
        people[slug] = {"name": name, "pid": person_id_for(slug), "candidacies": []}
    people[slug]["candidacies"].append({
        "contest_id": f"ky/2023-11-07/{post_slug}",
        "office_id": f"ky/{post_slug}",
        "party": party, "ballot_name": ballot_name, "post_slug": post_slug,
    })
    contests.setdefault(post_slug, []).append({**people[slug], "ballot_name": ballot_name,
                                               "party": party, "slug": slug, "votes": votes})


for gov, ltg, ticket, party, votes in GOV_TICKETS:
    add_person(gov, ticket, party, "governor", votes)
    add_person(ltg, ticket, party, "lieutenant-governor", votes)
for post_slug, cands in CONTESTS.items():
    for name, ballot, party, votes in cands:
        add_person(name, ballot, party, post_slug, votes)

winners = {ps: max(es, key=lambda e: e["votes"]) for ps, es in contests.items()}


def contest_note(post_slug):
    title, office_name, _ = POSTS[post_slug]
    es = contests[post_slug]
    parts = "; ".join(f"{e['ballot_name']} ({e['party']}) {fmt(e['votes'])}" for e in es)
    if post_slug in UNNAMED_WRITEIN:
        parts += f"; Write-In {fmt(UNNAMED_WRITEIN[post_slug])} (unnamed aggregate)"
    w = winners[post_slug]
    return (f"Commonwealth of Kentucky, State Board of Elections / Secretary of State, "
            f"'Certification of Election Results for 2023 General Election Final' -- official "
            f"certified results for the November 7, 2023 general election, {office_name} contest, "
            f"county tables with statewide totals: {parts}. {w['name']} won with {fmt(w['votes'])} votes.")


def source_yaml(post_slug, indent=""):
    note = contest_note(post_slug).replace("'", "''")
    return (f"{indent}- url: {CERT}\n"
            f"{indent}  note: '{note}'\n"
            f"{indent}  retrieved: '{TODAY}'\n")


HDR = ("# Built for the KY statewide executive pass (Civic-Data issue #195)\n"
       "# from the State Board of Elections' certified 2023 general\n"
       "# election results.\n")

# 1. Jurisdiction
jur_dir = TREE / "data/us/ky/jurisdictions/state"
jur_dir.mkdir(parents=True, exist_ok=True)
(jur_dir / "ky-executive.yaml").write_text(
    HDR +
    f"id: {JUR}\n"
    "name: Kentucky (statewide executive branch)\n"
    "state: ky\n"
    "division_id: ocd-division/country:us/state:ky\n"
    "classification: executive\n"
    "sources:\n"
    f"- url: {CERT}\n"
    "  note: Commonwealth of Kentucky, State Board of Elections certification of the November 7, 2023 general election -- the official certified results book whose per-office contests source the statewide executive records built under this jurisdiction.\n"
    f"  retrieved: '{TODAY}'\n")
print("JURISDICTION ky-executive.yaml")

# 2. Organization
org_dir = TREE / "data/us/ky/organizations/state"
org_dir.mkdir(parents=True, exist_ok=True)
(org_dir / "ky-executive-branch.yaml").write_text(
    "# Built for the KY statewide executive pass (Civic-Data issue #195).\n"
    f"id: {ORG_ID}\n"
    "name: Kentucky Executive Branch\n"
    f"jurisdiction_id: {JUR}\n"
    "identifiers: []\n"
    "sources:\n"
    f"- url: {CERT}\n"
    "  note: Commonwealth of Kentucky, State Board of Elections certification of the November 7, 2023 general election; the organization's posts are the state's elected executive offices as contested in that election.\n"
    f"  retrieved: '{TODAY}'\n")
print("ORG ky-executive-branch.yaml")

# 3. Posts
post_dir = TREE / "data/us/ky/posts/state"
post_dir.mkdir(parents=True, exist_ok=True)
for post_slug, (title, office_name, _yr) in POSTS.items():
    (post_dir / f"ky-{post_slug}.yaml").write_text(
        "# Built for the KY statewide executive pass (Civic-Data issue #195).\n"
        f"id: ky/{post_slug}\n"
        f"organization_id: {ORG_ID}\n"
        f"title: {title}\n"
        "seats: 1\n"
        "identifiers: []\n"
        "sources:\n"
        + source_yaml(post_slug))
    print("POST", post_slug)

# 4. People
ppl_dir = TREE / "data/us/ky/people/state"
ppl_dir.mkdir(parents=True, exist_ok=True)
for slug, p in people.items():
    lines = ["# Minted from the Kentucky State Board of Elections certified",
             "# Nov. 7, 2023 general election results (statewide executive",
             "# pass, Civic-Data issue #195).",
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
        srcs.append(source_yaml(cd["post_slug"]))
    lines += ["verification:", "  status: unverified", "  pipeline: build_ky_statewide_executive", "sources:"]
    body = "\n".join(lines) + "\n" + "".join(srcs)
    (ppl_dir / f"{slug}.yaml").write_text(body)
    print("PERSON", slug, p["pid"])

# 5. Memberships (winners)
mem_dir = TREE / "data/us/ky/memberships/state"
mem_dir.mkdir(parents=True, exist_ok=True)
for post_slug, (title, office_name, start_year) in POSTS.items():
    w = winners[post_slug]
    surname = w["slug"].split("-")[-1]
    mid = f"ky-{post_slug}-{surname}"
    body = ("# Minted from the Kentucky State Board of Elections certified\n"
            "# Nov. 7, 2023 general election results (Civic-Data issue #195).\n"
            f"id: {mid}\n"
            f"person_id: {w['pid']}\n"
            f"organization_id: {ORG_ID}\n"
            f"post_id: ky/{post_slug}\n"
            f"role: {title}\n"
            "seat: At-Large\n"
            f"start: '{start_year}'\n"
            "how_seated: elected\n"
            "sources:\n" + source_yaml(post_slug))
    (mem_dir / f"{mid}.yaml").write_text(body)
    print("MEMBERSHIP", mid)

# 6. Election file
lines = ["# Built from the Kentucky State Board of Elections certified",
         "# results for the November 7, 2023 general election",
         "# ('Certification of Election Results for 2023 General Election",
         "# Final'). Statewide executive pass, Civic-Data issue #195.",
         f"id: {ELEC_ID}",
         "name: Kentucky 2023-11-07 general election",
         "date: '2023-11-07'",
         "election_type: general",
         "status: certified",
         "contests:"]
for post_slug in POSTS:
    lines += [f"- id: ky/2023-11-07/{post_slug}",
              f"  jurisdiction_id: {JUR}",
              f"  office_id: ky/{post_slug}",
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
          f"- url: {CERT}",
          "  note: 'Commonwealth of Kentucky, State Board of Elections, \"Certification of Election Results for 2023 General Election Final\": the official certified results for the November 7, 2023 general election. This record covers the seven statewide executive contests; totals are the certification book''s statewide Total Votes rows. Governor and Lieutenant Governor are elected on a joint ticket (Ky. Const. sec. 70): both contests share the ticket vote totals. Named write-in candidates in the book (the Fishback ticket, Governor; Kenneth C. Moellman Jr., Secretary of State) are modeled as candidates with party Write-In; the State Treasurer write-in total of 155 is an unnamed aggregate and is carried in that contest''s source note only.'",
          f"  retrieved: '{TODAY}'"]
elec_dir = TREE / "data/us/ky/elections"
elec_dir.mkdir(parents=True, exist_ok=True)
(elec_dir / "ky--2023-11-07--general.yaml").write_text("\n".join(lines) + "\n")
print("ELECTION written")
print(f"COUNTS people={len(people)} posts={len(POSTS)} memberships={len(POSTS)} contests={len(POSTS)}")
