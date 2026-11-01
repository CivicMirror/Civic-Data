#!/usr/bin/env python3
"""Build KY legislative pass for Civic-Data issue #195.

Seats the current Kentucky General Assembly from certified results:
- Senate odd districts + all 100 House districts: November 5, 2024 general
  election, SBE "2024 General Election Certification as Amended on
  December 9th 2024" (text PDF, read firsthand; Senate District 29's
  write-in-only contest additionally verified against the printed page).
- Senate even districts: November 8, 2022 general election, SBE certified
  results book (certified January 17, 2023; the book is a scanned image
  PDF, so its Senate pages were OCR'd and every district's county rows
  were checksum-verified against the printed Total Votes row; district
  totals were also cross-checked against the Board's official 2022
  General Recap Sheets -- 32 county-candidate figures from the
  text-searchable county recaps matched the book exactly).

The November 3, 2026 winners are appended to these records after the
State Board of Elections certifies that election (CivicMirror-API carries
the live unofficial results meanwhile).

Identity handling (pre-push person check):
- Pamela Stevenson (House District 43 winner, 2024) is the 2023 Democratic
  Attorney General candidate minted in the executive pass: same name,
  same party, Kentucky -- her existing person file is reused and the
  candidacy appended, never overwritten.
- Robert M. "Robby" Mills (Senate District 4 winner, 2022) is the 2023
  Republican lieutenant-governor candidate minted in the executive pass
  as "Robby Mills": the certified books give the same distinctive
  nickname in both races and SD4 is his Henderson-based district. His
  existing person file (slug robby-mills) is reused; the 2022 candidacy
  keeps its certified ballot name.
- All 211 candidates were slug-audited: no two name strings share a slug,
  and no other candidate slug hits an existing KY person file.

Memberships: one per current holder, year precision only (2024 winners
start '2025', 2022 Senate winners start '2023'); no term ends inferred.
"""
import json, re, uuid
from pathlib import Path

TREE = Path(__file__).resolve().parent.parent
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
TODAY = "2026-11-01"
DATA = Path.home() / "workspace/ky195/ky_leg_contests.json"

CERT24 = "https://elect.ky.gov/results/2020-2029/Documents/2024%20General%20Election%20Certification%20as%20Amended%20on%20December%209th%202024.pdf"
CERT22 = "https://elect.ky.gov/results/2020-2029/Documents/1.17.2023%20Certified%20General%20Election%20Results.pdf"

UNIFY = {  # legislative-pool slug -> (existing slug, canonical name)
    "robert-m-robby-mills": ("robby-mills", "Robby Mills"),
}

def slugify(name):
    s = name.lower().replace("(", "").replace(")", "").replace(".", "").replace('"', "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)

def canon(name):
    s = slugify(name)
    if s in UNIFY:
        return UNIFY[s]
    return s, name

def person_id_for(slug):
    return "ocd-person/" + str(uuid.uuid5(NS, f"person|ky|state|{slug}"))

def fmt(n):
    return f"{n:,}"

def q(s):
    return s.replace("'", "''")

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"

CH = {
    "senate": dict(div="sldu", body="Kentucky Senate", jur_name="Kentucky Senate delegation",
                   role="State Senator", post_seg="state-senator"),
    "house": dict(div="sldl", body="Kentucky House of Representatives",
                  jur_name="Kentucky House of Representatives delegation",
                  role="State Representative", post_seg="state-representative"),
}

contests = json.loads(DATA.read_text())
by_key = {(c["chamber"], c["district"], c["date"]): c for c in contests}
assert sorted(d for (ch, d, dt) in by_key if ch == "senate" and dt == "2024-11-05") == list(range(1, 38, 2))
assert sorted(d for (ch, d, dt) in by_key if ch == "senate" and dt == "2022-11-08") == list(range(2, 39, 2))
assert sorted(d for (ch, d, dt) in by_key if ch == "house") == list(range(1, 101))

def winner(c):
    return max(c["candidates"], key=lambda x: x["votes"])

def contest_note(c):
    cfg = CH[c["chamber"]]
    parts = "; ".join(f"{x['name']} ({x['party']}) {fmt(x['votes'])}" for x in
                      sorted(c["candidates"], key=lambda z: -z["votes"]))
    w = winner(c)
    if c["date"] == "2024-11-05":
        extra = ""
        if c["chamber"] == "senate" and c["district"] == 29:
            extra = (" No candidate was listed on the ballot for this contest; "
                     "all candidates were write-in candidates.")
        return (f"Commonwealth of Kentucky, State Board of Elections / Secretary of State, "
                f"'2024 General Election Certification as Amended on December 9th 2024' -- official "
                f"certified results for the November 5, 2024 general election, {cfg['role']} "
                f"{ordinal(c['district'])} District contest, county tables with district totals: "
                f"{parts}. {w['name']} won with {fmt(w['votes'])} votes.{extra}")
    return (f"Commonwealth of Kentucky, State Board of Elections / Secretary of State, 'Certified "
            f"General Election Results' for the November 8, 2022 general election (certified "
            f"January 17, 2023) -- {cfg['role']} {ordinal(c['district'])} District contest, county "
            f"tables with district totals: {parts}. {w['name']} won with {fmt(w['votes'])} votes.")

def source_yaml(c, indent=""):
    url = CERT24 if c["date"] == "2024-11-05" else CERT22
    note = q(contest_note(c))
    return (f"{indent}- url: {url}\n"
            f"{indent}  note: '{note}'\n"
            f"{indent}  retrieved: '{TODAY}'\n")

def jur_id(cfg, d):
    return f"ocd-jurisdiction/country:us/state:ky/{cfg['div']}:{d}/legislature"

def org_id(ch, d):
    return "ocd-organization/" + str(uuid.uuid5(NS, f"organization|ky|{ch}-district-{d}"))

def post_id(ch, d):
    return f"ky-{ch}-{d}/{CH[ch]['post_seg']}"

def post_file(ch, d):
    return f"ky-{ch}-{d}-{CH[ch]['post_seg']}.yaml"

# People registry
people = {}
def get_person(name):
    slug, cname = canon(name)
    if slug not in people:
        path = TREE / "data/us/ky/people/state" / f"{slug}.yaml"
        people[slug] = {"name": cname, "pid": person_id_for(slug), "file": path,
                        "existing": path.exists(), "candidacies": [], "sources": []}
    return people[slug]

for c in contests:
    cfg = CH[c["chamber"]]
    for x in c["candidates"]:
        p = get_person(x["name"])
        p["candidacies"].append({
            "contest_id": f"ky/{c['date']}/{c['chamber']}-{c['district']}",
            "election_id": f"ky/{c['date']}/general",
            "jurisdiction_id": jur_id(cfg, c["district"]), "office_id": post_id(c["chamber"], c["district"]),
            "party": x["party"], "ballot_name": x["ballot_name"], "date": c["date"]})
        p["sources"].append(source_yaml(c))

counts = {"jur": 0, "org": 0, "post": 0, "new_people": 0, "reused_people": 0, "memberships": 0}

# 1. Jurisdictions, orgs, posts -- one district set from its most recent contest
districts = sorted({(c["chamber"], c["district"]) for c in contests})
for ch, d in districts:
    cfg = CH[ch]
    c_latest = by_key.get((ch, d, "2024-11-05")) or by_key[(ch, d, "2022-11-08")]
    jdir = TREE / "data/us/ky/jurisdictions/state"
    jf = jdir / f"{d}-{ch}.yaml"
    assert not jf.exists(), jf
    jf.write_text(
        "# Built for the KY legislative pass (Civic-Data issue #195) from the\n"
        "# State Board of Elections' certified general election results.\n"
        f"id: {jur_id(cfg, d)}\n"
        f"name: District {d} ({cfg['jur_name']})\n"
        "state: ky\n"
        f"division_id: ocd-division/country:us/state:ky/{cfg['div']}:{d}\n"
        "classification: legislature\n"
        f"government_form: single-member district ({cfg['body']})\n"
        "sources:\n" + source_yaml(c_latest))
    counts["jur"] += 1
    odir = TREE / "data/us/ky/organizations/state"
    of = odir / post_file(ch, d)
    assert not of.exists(), of
    of.write_text(
        "# Built for the KY legislative pass (Civic-Data issue #195).\n"
        f"id: {org_id(ch, d)}\n"
        f"name: {cfg['body']} -- District {d}\n"
        f"jurisdiction_id: {jur_id(cfg, d)}\n"
        "identifiers: []\n"
        "sources:\n" + source_yaml(c_latest))
    counts["org"] += 1
    pdir = TREE / "data/us/ky/posts/state"
    pf = pdir / post_file(ch, d)
    assert not pf.exists(), pf
    pf.write_text(
        "# Built for the KY legislative pass (Civic-Data issue #195).\n"
        f"id: {post_id(ch, d)}\n"
        f"organization_id: {org_id(ch, d)}\n"
        f"title: {cfg['role']}\n"
        "seats: 1\n"
        "identifiers: []\n"
        "sources:\n" + source_yaml(c_latest))
    counts["post"] += 1

# 2. People
ppl_dir = TREE / "data/us/ky/people/state"
for slug, p in sorted(people.items()):
    cand_lines = []
    for cd in sorted(p["candidacies"], key=lambda z: z["date"]):
        cand_lines += [f"- contest_id: {cd['contest_id']}",
                       f"  election_id: {cd['election_id']}",
                       f"  jurisdiction_id: {cd['jurisdiction_id']}",
                       f"  office_id: {cd['office_id']}",
                       f"  party: {cd['party']}",
                       f"  ballot_name: '{q(cd['ballot_name'])}'",
                       "  status: active"]
    if p["existing"]:
        txt = p["file"].read_text()
        assert "candidacies:" in txt and "verification:" in txt, p["file"]
        block = "\n".join(cand_lines) + "\n"
        txt = txt.replace("verification:", block + "verification:", 1)
        if not txt.endswith("\n"):
            txt += "\n"
        txt += "".join(p["sources"])
        p["file"].write_text(txt)
        counts["reused_people"] += 1
        print("REUSED", p["file"].name)
    else:
        body = ("# Minted from the Kentucky State Board of Elections certified\n"
                "# general election results (legislative pass, Civic-Data\n"
                "# issue #195).\n"
                f"id: {p['pid']}\nname: {p['name']}\nidentifiers: []\ncandidacies:\n"
                + "\n".join(cand_lines) + "\n"
                "verification:\n  status: unverified\n  pipeline: build_ky_legislative\nsources:\n"
                + "".join(p["sources"]))
        p["file"].write_text(body)
        counts["new_people"] += 1

# 3. Memberships -- current holders only
mem_dir = TREE / "data/us/ky/memberships/state"
for ch, d in districts:
    cfg = CH[ch]
    c_latest = by_key.get((ch, d, "2024-11-05")) or by_key[(ch, d, "2022-11-08")]
    w = winner(c_latest)
    slug, _ = canon(w["name"])
    p = people[slug]
    start = "2025" if c_latest["date"] == "2024-11-05" else "2023"
    surname = slug.split("-")[-1]
    mid = f"ky-{ch}-{d}-{cfg['post_seg']}-{surname}"
    mf = mem_dir / f"{mid}.yaml"
    assert not mf.exists(), mf
    body = ("# Minted from the Kentucky State Board of Elections certified\n"
            "# general election results (legislative pass, Civic-Data\n"
            "# issue #195).\n"
            f"id: {mid}\n"
            f"person_id: {p['pid']}\n"
            f"organization_id: {org_id(ch, d)}\n"
            f"post_id: {post_id(ch, d)}\n"
            f"role: {cfg['role']}\n"
            "seat: At-Large\n"
            f"start: '{start}'\n"
            "how_seated: elected\n"
            "sources:\n" + source_yaml(c_latest))
    mf.write_text(body)
    counts["memberships"] += 1

# 4. Election files
def contest_block(c):
    cfg = CH[c["chamber"]]
    lines = [f"- id: ky/{c['date']}/{c['chamber']}-{c['district']}",
             f"  jurisdiction_id: {jur_id(cfg, c['district'])}",
             f"  office_id: {post_id(c['chamber'], c['district'])}",
             "  vote_for: 1",
             "  candidate_ids:"]
    for x in c["candidates"]:
        slug, _ = canon(x["name"])
        lines.append(f"  - {people[slug]['pid']}")
    w = winner(c)
    wslug, _ = canon(w["name"])
    lines += ["  result_status: certified",
              "  winners:",
              f"  - person_id: {people[wslug]['pid']}",
              f"    name: '{q(people[wslug]['name'])}'",
              f"    party: {w['party']}",
              f"    votes: {w['votes']}"]
    return lines

elec_dir = TREE / "data/us/ky/elections"
lines = ["# Built from the Kentucky State Board of Elections certified",
         "# results for the November 5, 2024 general election ('2024 General",
         "# Election Certification as Amended on December 9th 2024'). This",
         "# record covers the legislative contests (19 Senate districts, 100",
         "# House districts); other tiers of the 2024 general are appended by",
         "# later passes. Legislative pass, Civic-Data issue #195.",
         "id: ky/2024-11-05/general",
         "name: Kentucky 2024-11-05 general election",
         "date: '2024-11-05'",
         "election_type: general",
         "status: certified",
         "contests:"]
for c in sorted((c for c in contests if c["date"] == "2024-11-05"),
                key=lambda z: (z["chamber"], z["district"])):
    lines += contest_block(c)
lines += ["sources:",
          f"- url: {CERT24}",
          "  note: 'Commonwealth of Kentucky, State Board of Elections / Secretary of State, ''2024 General Election Certification as Amended on December 9th 2024'' -- the official certified results book for the November 5, 2024 general election; legislative contest totals are its per-district Total Votes rows.'",
          f"  retrieved: '{TODAY}'"]
f24 = elec_dir / "ky--2024-11-05--general.yaml"
assert not f24.exists(), f24
f24.write_text("\n".join(lines) + "\n")
print("ELECTION 2024 written")

lines = ["# Built from the Kentucky State Board of Elections certified",
         "# results for the November 8, 2022 general election (certified",
         "# January 17, 2023). This record covers the legislative contests",
         "# decided in 2022: the 19 even-numbered Senate districts (Kentucky",
         "# Senate terms are staggered; odd-numbered districts were decided",
         "# in 2024). Other tiers of the 2022 general are appended by later",
         "# passes. Legislative pass, Civic-Data issue #195.",
         "id: ky/2022-11-08/general",
         "name: Kentucky 2022-11-08 general election",
         "date: '2022-11-08'",
         "election_type: general",
         "status: certified",
         "contests:"]
for c in sorted((c for c in contests if c["date"] == "2022-11-08"), key=lambda z: z["district"]):
    lines += contest_block(c)
lines += ["sources:",
          f"- url: {CERT22}",
          "  note: 'Commonwealth of Kentucky, State Board of Elections / Secretary of State, ''Certified General Election Results'' for the November 8, 2022 general election (certified January 17, 2023). The book is a scanned image PDF; its Senate pages were read by OCR and every district''s county rows were checksum-verified against the printed Total Votes row. District figures were also cross-checked against the Board''s official 2022 General Recap Sheets (elect.ky.gov): all 32 county-candidate figures available in the text-searchable county recaps matched this book exactly.'",
          f"  retrieved: '{TODAY}'"]
f22 = elec_dir / "ky--2022-11-08--general.yaml"
assert not f22.exists(), f22
f22.write_text("\n".join(lines) + "\n")
print("ELECTION 2022 written")
print("COUNTS", counts)
