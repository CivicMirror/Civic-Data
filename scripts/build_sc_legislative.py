#!/usr/bin/env python3
"""Build SC legislative pass for Civic-Data issue #177 (Senate 2024; House 2024 + 2022).

Source: SC State Election Commission, Election History (ElectionStats)
per-office Search Results CSV exports (State Senate, State House), general
elections of 2024-11-05 and 2022-11-08, county-division rows aggregated
(SC Senate sits only in presidential-cycle generals: zero 2022 contests,
confirmed from the export). Winners derived from totals; "Write-In" is an
unnamed aggregate and is never seated (no write-in outpolled a named
candidate in any of the 294 contests).

Identity handling (pre-push person check):
- Chris Nelums (Senate District 19, 2024) is the same person as the 2022
  Commissioner of Agriculture candidate minted in the executive pass: same
  name, same distinctive United Citizens party in both candidacies, same
  official source. His existing person file is reused; the candidacy is
  appended, never overwritten. Same for Sarah E Work: the Alliance-party
  2022 State Treasurer candidate and the Alliance-party Senate District 15
  candidate of 2024 ("Sarah Work") are one person; her file is reused.
- Thirteen name-variant pairs across cycles are one person each (same
  district, or House->Senate move), unified under the fuller certified
  form: Bobby J. Cox, Carl L. Anderson, Joe H. Jefferson, Marvin Rashad
  Pendarvis, Roger Allen Nutt (House 34 2022 -> Senate 12 2024),
  Russell L. Ott (House 93 2022 -> Senate 26 2024), David Davey Hiott,
  Richard Richie Yow, Christopher J Murphy, Kirkman Finlay, III,
  Marvin Mark Smith (2024 ballot name "Mark Smith"), and
  J. Fritz Wiebel (2022 ballot name was simply "Fritz"). Each candidacy
  keeps its own cycle's exact ballot_name. NOT unified: Chardale Murray
  (House 116, 2022) and Charlie Murray (House 116, 2024) are different
  people, as are Audrey Hopkins Williams and Shedron Hook Williams
  (House 122).
- Luke Rankin (House District 14, 2024) and Luke A. Rankin (Senate
  District 33, 2024) are DIFFERENT people: both appear on the same 2024
  ballot for different offices in different districts. Separate records.

Memberships: one per (person, post) win-span. A 2022+2024 winner on the
same post holds one open membership from '2023'; a 2022-only winner's
membership ends '2024'; a 2024 winner's starts '2025'. Year precision only
-- no term days are inferred.
"""
import json, re, uuid
from pathlib import Path

TREE = Path(__file__).resolve().parent.parent
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
TODAY = "2026-10-25"
HIST = "https://electionhistory.scvotes.gov"
SKIP = {"Total Votes Cast", "Total Ballots Cast", "Write-In", "Overvotes/Undervotes", "Unknown Candidate"}

UNIFY = {  # variant slug -> (canonical slug, canonical name)
    "bobby-cox": ("bobby-j-cox", "Bobby J. Cox"),
    "carl-anderson": ("carl-l-anderson", "Carl L. Anderson"),
    "joe-jefferson": ("joe-h-jefferson", "Joe H. Jefferson"),
    "marvin-r-pendarvis": ("marvin-rashad-pendarvis", "Marvin Rashad Pendarvis"),
    "roger-a-nutt": ("roger-allen-nutt", "Roger Allen Nutt"),
    "russell-ott": ("russell-l-ott", "Russell L. Ott"),
    "davey-hiott": ("david-davey-hiott", "David Davey Hiott"),
    "richie-yow": ("richard-richie-yow", "Richard Richie Yow"),
    "chris-murphy": ("christopher-j-murphy", "Christopher J Murphy"),
    "kirkman-finlay": ("kirkman-finlay-iii", "Kirkman Finlay, III"),
    "fritz": ("j-fritz-wiebel", "J. Fritz Wiebel"),
    "sarah-work": ("sarah-e-work", "Sarah E Work"),
    "mark-smith": ("marvin-mark-smith", "Marvin Mark Smith"),
}
CANON_NAME = {v[0]: v[1] for v in UNIFY.values()}

def slugify(name):
    s = name.lower().replace("(", "").replace(")", "").replace(".", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)

def canon(name):
    s = slugify(name)
    if s in UNIFY:
        return UNIFY[s]
    return s, CANON_NAME.get(s, name)

def person_id_for(slug):
    return "ocd-person/" + str(uuid.uuid5(NS, f"person|sc|state|{slug}"))

def fmt(n):
    return f"{n:,}"

def q(s):
    """Escape a string for a single-quoted YAML scalar (apostrophes double)."""
    return s.replace("'", "''")

raw = json.loads((Path.home() / "workspace/sc177/legislative_raw.json").read_text())

CH = {  # chamber config
    "State Senate": dict(key="senate", div="sldu", body="South Carolina Senate",
                         jur_name="South Carolina Senate delegation", role="State Senator",
                         post_seg="state-senator", cycles=["2024-11-05"]),
    "State House": dict(key="house", div="sldl", body="South Carolina House of Representatives",
                        jur_name="South Carolina House of Representatives delegation", role="State Representative",
                        post_seg="state-representative", cycles=["2024-11-05", "2022-11-08"]),
}

# Organize contests: (chamber_key, district int) -> {date: contest}
contests = {}
for office, cs in raw.items():
    cfg = CH[office]
    for c in cs:
        if c["date"] not in cfg["cycles"]:
            continue
        d = int(c["district_name"])
        contests.setdefault((cfg["key"], d), {})[c["date"]] = c

def named(c):
    return [x for x in c["candidates"] if x["name"] not in SKIP]

def winner(c):
    return max(named(c), key=lambda x: x["votes"])

def contest_note(c, cfg, d):
    parts = "; ".join(f"{x['name']} ({x['party']}) {fmt(x['votes'])}" for x in named(c))
    wi = next((x["votes"] for x in c["candidates"] if x["name"] == "Write-In"), 0)
    if wi:
        parts += f"; Write-In {fmt(wi)}"
    w = winner(c)
    when = "November 5, 2024" if c["date"] == "2024-11-05" else "November 8, 2022"
    return (f"South Carolina State Election Commission, Election History (ElectionStats) results for the "
            f"{when} general election, {cfg['body']} District {d} contest (ElectionStats contest "
            f"{c['contest_id']}), county-division rows aggregated across the district's counties: "
            f"{parts}. {w['name']} won with {fmt(w['votes'])} votes.")

def source_yaml(c, cfg, d, indent=""):
    note = contest_note(c, cfg, d).replace("'", "''")
    return (f"{indent}- url: {HIST}/contest/{c['contest_id']}\n"
            f"{indent}  note: '{note}'\n"
            f"{indent}  retrieved: '{TODAY}'\n")

def jur_id(cfg, d):
    return f"ocd-jurisdiction/country:us/state:sc/{cfg['div']}:{d}/legislature"

def org_id(cfg, d):
    return "ocd-organization/" + str(uuid.uuid5(NS, f"organization|sc|{cfg['key']}-district-{d}"))

def post_id(cfg, d):
    return f"sc-{cfg['key']}-{d}/{cfg['post_seg']}"

# People registry
people = {}  # slug -> {name, pid, file, candidacies[], sources[]}
def get_person(name):
    slug, cname = canon(name)
    if slug not in people:
        path = TREE / "data/us/sc/people/state" / f"{slug}.yaml"
        people[slug] = {"name": cname, "pid": person_id_for(slug), "file": path,
                        "existing": path.exists(), "candidacies": [], "sources": []}
    return people[slug]

# Register candidacies
for (ckey, d), bydate in contests.items():
    cfg = next(v for v in CH.values() if v["key"] == ckey)
    for date, c in bydate.items():
        yr = date[:4]
        for x in named(c):
            p = get_person(x["name"])
            p["candidacies"].append({
                "contest_id": f"sc/{date}/{ckey}-{d}", "election_id": f"sc/{date}/general",
                "jurisdiction_id": jur_id(cfg, d), "office_id": post_id(cfg, d),
                "party": x["party"], "ballot_name": x["name"], "date": date})
            p["sources"].append(source_yaml(c, cfg, d))

counts = {"jur": 0, "org": 0, "post": 0, "new_people": 0, "reused_people": 0, "memberships": 0}

# 1. Jurisdictions, orgs, posts
for (ckey, d), bydate in sorted(contests.items()):
    cfg = next(v for v in CH.values() if v["key"] == ckey)
    c24 = bydate.get("2024-11-05") or bydate.get("2022-11-08")
    jdir = TREE / "data/us/sc/jurisdictions/state"; jdir.mkdir(parents=True, exist_ok=True)
    (jdir / f"{d}-{ckey}.yaml").write_text(
        "# Built for the SC legislative pass (Civic-Data issue #177) from the\n"
        "# SC State Election Commission Election History results.\n"
        f"id: {jur_id(cfg, d)}\n"
        f"name: District {d} ({cfg['jur_name']})\n"
        "state: sc\n"
        f"division_id: ocd-division/country:us/state:sc/{cfg['div']}:{d}\n"
        "classification: legislature\n"
        f"government_form: single-member district ({cfg['body']})\n"
        "sources:\n" + source_yaml(c24, cfg, d))
    counts["jur"] += 1
    odir = TREE / "data/us/sc/organizations/state"; odir.mkdir(parents=True, exist_ok=True)
    (odir / f"{d}-{ckey}.yaml").write_text(
        "# Built for the SC legislative pass (Civic-Data issue #177).\n"
        f"id: {org_id(cfg, d)}\n"
        f"name: {cfg['body']} -- District {d}\n"
        f"jurisdiction_id: {jur_id(cfg, d)}\n"
        "identifiers: []\n"
        "sources:\n" + source_yaml(c24, cfg, d))
    counts["org"] += 1
    pdir = TREE / "data/us/sc/posts/state"; pdir.mkdir(parents=True, exist_ok=True)
    (pdir / f"{d}-{ckey}.yaml").write_text(
        "# Built for the SC legislative pass (Civic-Data issue #177).\n"
        f"id: {post_id(cfg, d)}\n"
        f"organization_id: {org_id(cfg, d)}\n"
        f"title: {cfg['role']}\n"
        "seats: 1\n"
        "identifiers: []\n"
        "sources:\n" + source_yaml(c24, cfg, d))
    counts["post"] += 1

# 2. People (new files, or append candidacies+sources to the one reuse)
ppl_dir = TREE / "data/us/sc/people/state"
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
        assert "candidacies:" in txt and txt.rstrip().endswith("'"), p["file"]
        # append candidacies after the existing candidacy block: insert before "verification:"
        block = "\n".join(cand_lines) + "\n"
        txt = txt.replace("verification:", block + "verification:", 1)
        if not txt.endswith("\n"):
            txt += "\n"
        txt += "".join(p["sources"])
        p["file"].write_text(txt)
        counts["reused_people"] += 1
        print("REUSED", p["file"].name)
    else:
        body = ("# Minted from the SC State Election Commission Election History\n"
                "# official general election results (legislative pass,\n"
                "# Civic-Data issue #177).\n"
                f"id: {p['pid']}\nname: {p['name']}\nidentifiers: []\ncandidacies:\n"
                + "\n".join(cand_lines) + "\n"
                "verification:\n  status: unverified\n  pipeline: build_sc_legislative\nsources:\n"
                + "".join(p["sources"]))
        p["file"].write_text(body)
        counts["new_people"] += 1

# 3. Memberships
mem_dir = TREE / "data/us/sc/memberships/state"; mem_dir.mkdir(parents=True, exist_ok=True)
seen_files = set()
for (ckey, d), bydate in sorted(contests.items()):
    cfg = next(v for v in CH.values() if v["key"] == ckey)
    wins = {}  # slug -> [dates]
    for date, c in bydate.items():
        w = winner(c)
        slug, _ = canon(w["name"])
        wins.setdefault(slug, []).append(date)
    for slug, dates in wins.items():
        p = people[slug]
        start = str(int(min(dates)[:4]) + 1)
        end = None
        if max(dates) == "2022-11-08":
            end = "2024"
        surname = slug.split("-")[-1]
        mid = f"sc-{ckey}-{d}-{cfg['post_seg']}-{surname}"
        assert mid not in seen_files, f"membership filename collision: {mid}"
        seen_files.add(mid)
        body = ("# Minted from the SC State Election Commission Election History\n"
                "# official general election results (Civic-Data issue #177).\n"
                f"id: {mid}\n"
                f"person_id: {p['pid']}\n"
                f"organization_id: {org_id(cfg, d)}\n"
                f"post_id: {post_id(cfg, d)}\n"
                f"role: {cfg['role']}\n"
                "seat: At-Large\n"
                f"start: '{start}'\n")
        if end:
            body += f"end: '{end}'\n"
        body += "how_seated: elected\nsources:\n"
        for date in sorted(dates):
            body += source_yaml(bydate[date], cfg, d)
        (mem_dir / f"{mid}.yaml").write_text(body)
        counts["memberships"] += 1

# 4a. New 2024 election file (legislative contests)
def contest_block(date, ckey, d, c, cfg):
    yr = date[:4]
    lines = [f"- id: sc/{date}/{ckey}-{d}",
             f"  jurisdiction_id: {jur_id(cfg, d)}",
             f"  office_id: {post_id(cfg, d)}",
             "  vote_for: 1",
             "  candidate_ids:"]
    for x in named(c):
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

lines = ["# Built from the SC State Election Commission Election History",
         "# (ElectionStats) official results for the November 5, 2024 general",
         "# election, per-office CSV exports aggregated from county-division",
         "# rows. This record covers the legislative contests (46 Senate, 124",
         "# House); other tiers of the 2024 general are appended by later",
         "# passes. Civic-Data issue #177.",
         "id: sc/2024-11-05/general",
         "name: South Carolina 2024-11-05 general election",
         "date: '2024-11-05'",
         "election_type: general",
         "status: certified",
         "contests:"]
for (ckey, d), bydate in sorted(contests.items()):
    if "2024-11-05" in bydate:
        cfg = next(v for v in CH.values() if v["key"] == ckey)
        lines += contest_block("2024-11-05", ckey, d, bydate["2024-11-05"], cfg)
lines += ["sources:",
          f"- url: {HIST}/search?gf=e",
          "  note: 'SC State Election Commission Election History (ElectionStats): the official historical results system. Contest totals here are aggregated from the per-office Search Results CSV exports (State Senate, State House) using county-division rows only (the exports duplicate each vote in county and precinct rows). Write-In rows are unnamed aggregates and seat no one.'",
          f"  retrieved: '{TODAY}'"]
elec_dir = TREE / "data/us/sc/elections"
(elec_dir / "sc--2024-11-05--general.yaml").write_text("\n".join(lines) + "\n")
print("ELECTION 2024 written")

# 4b. Append 124 House contests + a source to the existing 2022 election file
f22 = elec_dir / "sc--2022-11-08--general.yaml"
txt = f22.read_text()
head, sep, tail = txt.partition("\nsources:")
assert sep, "2022 election file: sources block not found"
blocks = []
for (ckey, d), bydate in sorted(contests.items()):
    if ckey == "house" and "2022-11-08" in bydate:
        cfg = CH["State House"]
        blocks += contest_block("2022-11-08", ckey, d, bydate["2022-11-08"], cfg)
new_txt = head + "\n" + "\n".join(blocks) + "\nsources:" + tail
if not new_txt.endswith("\n"):
    new_txt += "\n"
new_txt += (f"- url: {HIST}/search?gf=e\n"
            "  note: 'Legislative contests appended by the SC legislative pass (Civic-Data issue #177): the 124 State House contests of the November 8, 2022 general election, aggregated from the Election History State House CSV export, county-division rows only. SC Senate seats are not contested in midterm generals (zero 2022 Senate contests in the export).'\n"
            f"  retrieved: '{TODAY}'\n")
f22.write_text(new_txt)
print("ELECTION 2022 appended (124 house contests)")
print("COUNTS", counts)
