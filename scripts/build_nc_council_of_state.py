#!/usr/bin/env python3
"""Build NC 2024 Council of State worked example for Civic-Data issue #172.

Source: NC SBE official precinct results file results_pct_20241105.txt
(tab-delimited, layout_results_pct.txt), aggregated by contest+choice.
Winners were cross-checked against the existing hand-seeded memberships
before building; the one candidate who already had a person record as a
county officeholder (Chad Brown, Gaston County Commissioner, Riverbend
Twp -- contemporaneously reported as the Republican SOS candidate and
Gaston commission chairman) is reused, never overwritten.
"""
import json, re, uuid
from pathlib import Path

TREE = Path(__file__).resolve().parent.parent
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
SBE_URL = "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2024_11_05/results_pct_20241105.zip"
HIST_URL = "https://www.ncsbe.gov/results-data/election-results/historical-election-results-data"
TODAY = "2026-10-23"
JUR = "ocd-jurisdiction/country:us/state:nc/executive"
ELEC_ID = "nc/2024-11-05/general"

PARTY = {"DEM": "Democratic", "REP": "Republican", "LIB": "Libertarian",
         "CST": "Constitution", "GRE": "Green"}

# contest -> (office_id, post title)
CONTESTS = {
    "NC GOVERNOR": ("nc/governor", "Governor"),
    "NC LIEUTENANT GOVERNOR": ("nc/lieutenant-governor", "Lieutenant Governor"),
    "NC SECRETARY OF STATE": ("nc/secretary-of-state", "Secretary of State"),
    "NC ATTORNEY GENERAL": ("nc/attorney-general", "Attorney General"),
    "NC AUDITOR": ("nc/state-auditor", "State Auditor"),
    "NC TREASURER": ("nc/state-treasurer", "State Treasurer"),
    "NC COMMISSIONER OF AGRICULTURE": ("nc/commissioner-of-agriculture", "Commissioner of Agriculture"),
    "NC COMMISSIONER OF INSURANCE": ("nc/commissioner-of-insurance", "Commissioner of Insurance"),
    "NC COMMISSIONER OF LABOR": ("nc/commissioner-of-labor", "Commissioner of Labor"),
    "NC SUPERINTENDENT OF PUBLIC INSTRUCTION": ("nc/superintendent-of-public-instruction", "Superintendent of Public Instruction"),
}

# existing person records: ballot choice name -> (relative file, person record name if different)
EXISTING = {
    "Josh Stein": "people/state/josh-stein.yaml",
    "Rachel Hunt": "people/state/rachel-hunt.yaml",
    "Elaine Marshall": "people/state/elaine-f-marshall.yaml",
    "Jeff Jackson": "people/state/jeff-jackson.yaml",
    "Dave Boliek": "people/state/dave-boliek.yaml",
    "Brad Briner": "people/state/brad-briner.yaml",
    "Steve Troxler": "people/state/steve-troxler.yaml",
    "Mike Causey": "people/state/mike-causey.yaml",
    "Luke Farley": "people/state/luke-farley.yaml",
    "Maurice (Mo) Green": "people/state/maurice-mo-green.yaml",
    "Chad Brown": "people/county/chad-brown.yaml",
}

def slugify(name: str) -> str:
    s = name.lower().replace("(", "").replace(")", "").replace(".", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)

def person_id_for(slug: str) -> str:
    return "ocd-person/" + str(uuid.uuid5(NS, f"person|nc|state|{slug}"))

def fmt(n: int) -> str:
    return f"{n:,}"

# Extraction artifact (contest totals aggregated from the SBE file):
data = json.loads((Path.home() / "workspace/nc172/cos_2024.json").read_text())

# Resolve every candidate to a person id + file
resolved = {}  # (contest, choice) -> dict
for contest, cands in data.items():
    for c in cands:
        choice = c["choice"]
        if choice in EXISTING:
            path = TREE / "data/us/nc" / EXISTING[choice]
            txt = path.read_text()
            pid = re.search(r"^id: (ocd-person/\S+)$", txt, re.M).group(1)
            pname = re.search(r"^name: (.+)$", txt, re.M).group(1).strip()
            resolved[(contest, choice)] = {"pid": pid, "file": path, "person_name": pname, "new": False}
        else:
            slug = slugify(choice)
            path = TREE / "data/us/nc/people/state" / f"{slug}.yaml"
            assert not path.exists(), f"slug collision: {path}"
            resolved[(contest, choice)] = {"pid": person_id_for(slug), "file": path,
                                           "person_name": choice, "new": True, "slug": slug}

def contest_note(contest: str) -> str:
    office_id, title = CONTESTS[contest]
    parts = "; ".join(f"{c['choice']} ({c['party']}) {fmt(c['total'])}" for c in data[contest])
    winner = data[contest][0]
    return (f"North Carolina State Board of Elections, official precinct-level results file for the "
            f"November 5, 2024 general election (results_pct_20241105.txt, linked from the NCSBE "
            f"Historical Election Results Data page), aggregated across all 100 counties: "
            f"{contest.title().replace('Nc ', 'NC ')} -- {parts}. "
            f"{winner['choice']} won with {fmt(winner['total'])} votes.")

def candidacy_yaml(contest: str, c: dict) -> str:
    office_id, _ = CONTESTS[contest]
    cslug = office_id.split("/")[1]
    return (f"- contest_id: nc/2024-11-05/{cslug}\n"
            f"  election_id: {ELEC_ID}\n"
            f"  jurisdiction_id: {JUR}\n"
            f"  office_id: {office_id}\n"
            f"  party: {PARTY[c['party']]}\n"
            f"  ballot_name: '{c['choice']}'\n"
            f"  status: active\n")

def source_yaml(contest: str, indent: str = "") -> str:
    note = contest_note(contest).replace("'", "''")
    return (f"{indent}- url: {SBE_URL}\n"
            f"{indent}  note: '{note}'\n"
            f"{indent}  retrieved: '{TODAY}'\n")

# 1. New person files
for (contest, choice), r in resolved.items():
    if not r["new"]:
        continue
    c = next(x for x in data[contest] if x["choice"] == choice)
    hdr = ("# Minted from the NC State Board of Elections official Nov. 5, 2024\n"
           "# general election results (Council of State worked example,\n"
           "# Civic-Data issue #172).\n")
    body = (hdr + f"id: {r['pid']}\nname: {choice}\nidentifiers: []\ncandidacies:\n"
            + candidacy_yaml(contest, c)
            + "verification:\n  status: unverified\n  pipeline: build_nc_council_of_state\nsources:\n"
            + source_yaml(contest))
    r["file"].write_text(body)
    print("NEW", r["file"].name, r["pid"])

# 2. Existing people: append candidacy + SBE source
for (contest, choice), r in resolved.items():
    if r["new"]:
        continue
    c = next(x for x in data[contest] if x["choice"] == choice)
    txt = r["file"].read_text()
    assert "candidacies: []" in txt, r["file"]
    txt = txt.replace("candidacies: []", "candidacies:\n" + candidacy_yaml(contest, c).rstrip("\n"), 1)
    if not txt.endswith("\n"):
        txt += "\n"
    txt += source_yaml(contest)
    r["file"].write_text(txt)
    print("UPDATED", r["file"].name)

# 3. Memberships: append SBE source to the 10 winners
for contest, cands in data.items():
    office_id, title = CONTESTS[contest]
    winner = cands[0]
    r = resolved[(contest, winner["choice"])]
    oslug = office_id.split("/")[1]
    # membership filename: nc-<office-slug>-<winner-last-slug>.yaml -- find by post_id + person
    found = None
    for mf in (TREE / "data/us/nc/memberships/state").glob("nc-*.yaml"):
        t = mf.read_text()
        if f"post_id: {office_id}" in t and r["pid"] in t:
            found = mf; break
    assert found, office_id
    txt = found.read_text()
    if SBE_URL not in txt:
        if not txt.endswith("\n"):
            txt += "\n"
        note = contest_note(contest).replace("'", "''")
        txt += (f"- url: {SBE_URL}\n  note: '{note}'\n  retrieved: '{TODAY}'\n")
        found.write_text(txt)
    print("MEMBERSHIP", found.name)

# 4. Election file
lines = []
lines.append("# Built from the North Carolina State Board of Elections official")
lines.append("# precinct-level results file for the November 5, 2024 general")
lines.append("# election (results_pct_20241105.txt), aggregated by contest across")
lines.append("# all 100 counties. Council of State worked example, issue #172.")
lines.append(f"id: {ELEC_ID}")
lines.append("name: North Carolina 2024-11-05 general election")
lines.append("date: '2024-11-05'")
lines.append("election_type: general")
lines.append("status: certified")
lines.append("contests:")
for contest in CONTESTS:
    office_id, title = CONTESTS[contest]
    oslug = office_id.split("/")[1]
    lines.append(f"- id: nc/2024-11-05/{oslug}")
    lines.append(f"  jurisdiction_id: {JUR}")
    lines.append(f"  office_id: {office_id}")
    lines.append("  vote_for: 1")
    lines.append("  candidate_ids:")
    for c in data[contest]:
        lines.append(f"  - {resolved[(contest, c['choice'])]['pid']}")
    lines.append("  result_status: certified")
    w = data[contest][0]
    wr = resolved[(contest, w["choice"])]
    lines.append("  winners:")
    lines.append(f"  - person_id: {wr['pid']}")
    lines.append(f"    name: '{wr['person_name']}'")
    lines.append(f"    party: {PARTY[w['party']]}")
    lines.append(f"    votes: {w['total']}")
lines.append("sources:")
lines.append(f"- url: {HIST_URL}")
lines.append("  note: 'NCSBE Historical Election Results Data page: the November 5, 2024 general election Results (ZIP) file (results_pct_20241105.txt) is the official precinct-level results file for the election, certified November 26, 2024. This election record covers the ten Council of State contests; vote totals here are aggregated from that file across all 100 counties and cross-checked so each candidate''s method columns (Election Day + early + absentee by mail + provisional) sum to the file''s total-votes column on every precinct row.'")
lines.append(f"  retrieved: '{TODAY}'")
lines.append(f"- url: {SBE_URL}")
lines.append("  note: 'Direct download of the November 5, 2024 general election results file (results_pct_20241105.txt, tab-delimited per layout_results_pct.txt) used for the contest totals in this record.'")
lines.append(f"  retrieved: '{TODAY}'")
elec_dir = TREE / "data/us/nc/elections"
elec_dir.mkdir(exist_ok=True)
(elec_dir / "nc--2024-11-05--general.yaml").write_text("\n".join(lines) + "\n")
print("ELECTION written")
