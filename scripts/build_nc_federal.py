#!/usr/bin/env python3
"""Build the NC federal pass for Civic-Data issue #172:
- 14 U.S. House contests (2024) appended to the 2024 general election record;
- U.S. Senate Class II contest (2020, Tillis) as a new election file;
- U.S. Senate Class III contest (2022, Budd) as a new election file.
All from NC SBE official precinct-level results files. The two ended
pre-2023-map House memberships (Budd CD13, Hudson CD8, both ended
2023-01-03) are NOT traced to these contests: their last elections ran
in the pre-2023 districts, and the repo's posts are the current-map
districts. Their traces remain, disclosed.
Presidential contests are not modeled anywhere in Civic-Data (no
president post exists in the repo) and are not built.
"""
import json, re, uuid, unicodedata
from pathlib import Path

import yaml

TREE = Path(__file__).resolve().parent.parent
NC = TREE / "data/us/nc"
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
TODAY = "2026-10-23"
ZIP24 = "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2024_11_05/results_pct_20241105.zip"
ZIP20 = "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2020_11_03/results_pct_20201103.zip"
ZIP22 = "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2022_11_08/results_pct_20221108.zip"
PARTY = {"DEM": "Democratic", "REP": "Republican", "LIB": "Libertarian",
         "CST": "Constitution", "GRE": "Green", "UNA": "Unaffiliated",
         "WTP": "We The People", "": None}

fed = json.loads((Path.home() / "workspace/nc172/fed.json").read_text())

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"[^a-z ]", "", s.lower())
    return re.sub(r"\s+", " ", s).strip()

def slugify(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)

people = {}
for p in sorted(NC.glob("people/*/*.yaml")):
    d = yaml.safe_load(p.read_text())
    people[d["id"]] = {"name": d["name"], "path": p, "doc": d}
by_norm = {}
for pid, info in people.items():
    by_norm.setdefault(norm(info["name"]), []).append(pid)

holders = {}
for p in sorted(NC.glob("memberships/federal/*.yaml")):
    d = yaml.safe_load(p.read_text())
    if "end" not in d:
        holders[d["post_id"]] = (d["person_id"], p)

touched = set()
new_people = []

def get_or_mint(name, tier="federal"):
    hits = by_norm.get(norm(name), [])
    if hits:
        assert len(hits) == 1, (name, hits)
        return hits[0], False
    slug = slugify(name)
    path = NC / f"people/{tier}/{slug}.yaml"
    if path.exists():
        slug = f"{slug}-{uuid.uuid5(NS, 'collision|nc|' + slug + '|' + name).hex[:8]}"
        path = NC / f"people/{tier}/{slug}.yaml"
    pid = "ocd-person/" + str(uuid.uuid5(NS, f"person|nc|{tier}|{slug}"))
    doc = {"id": pid, "name": name, "identifiers": [], "candidacies": [],
           "verification": {"status": "unverified", "pipeline": "build_nc_federal"},
           "sources": []}
    people[pid] = {"name": name, "path": path, "doc": doc, "new": True}
    by_norm.setdefault(norm(name), []).append(pid)
    new_people.append(pid)
    return pid, True

def add_candidacy(pid, contest_id, election_id, jur_id, office_id, party, ballot_name, zip_url, note):
    doc = people[pid]["doc"]
    assert all(x["contest_id"] != contest_id for x in doc.get("candidacies", [])), (pid, contest_id)
    doc.setdefault("candidacies", []).append({
        "contest_id": contest_id, "election_id": election_id, "jurisdiction_id": jur_id,
        "office_id": office_id, **({"party": party} if party else {}),
        "ballot_name": ballot_name, "status": "active"})
    if not any(s["url"] == zip_url and note in s.get("note", "") for s in doc.get("sources", [])):
        doc.setdefault("sources", []).append({"url": zip_url, "note": note, "retrieved": TODAY})
    touched.add(pid)

def note_for(title, cands, zipname, datestr):
    parts = "; ".join(f"{c['choice']} ({c['party']}) {c['total']:,}" if c["party"] else f"{c['choice']} {c['total']:,}" for c in cands)
    w = cands[0]
    return (f"North Carolina State Board of Elections, official precinct-level results file for the "
            f"{datestr} general election ({zipname}), aggregated across the district's precincts: "
            f"{title} -- {parts}. {w['choice']} won with {w['total']:,} votes.")

membership_sources = []

def run_contest(cands, contest_id, election_id, jur_id, office_id, title, zip_url, zipname, datestr,
                winner_holder_post):
    cands = [c for c in cands if "Write-In" not in c["choice"]]
    note = note_for(title, cands, zipname, datestr)
    cand_pids = []
    for i, c in enumerate(cands):
        party = PARTY.get(c["party"] or "")
        if i == 0 and winner_holder_post:
            pid, mpath = holders[winner_holder_post]
            assert norm(people[pid]["name"]).split()[-1] == norm(c["choice"]).split()[-1], (c, people[pid]["name"])
            membership_sources.append((mpath, zip_url, note))
        else:
            pid, _ = get_or_mint(c["choice"])
        add_candidacy(pid, contest_id, election_id, jur_id, office_id, party, c["choice"], zip_url, note)
        cand_pids.append(pid)
    w = cands[0]
    return {"id": contest_id, "jurisdiction_id": jur_id, "office_id": office_id, "vote_for": 1,
            "candidate_ids": cand_pids, "result_status": "certified",
            "winners": [{"person_id": cand_pids[0], "name": people[cand_pids[0]]["name"],
                         "party": PARTY.get(w["party"] or ""), "votes": w["total"]}]}

# ---- Senate 2020 (Class II) ----
sen_jur = "ocd-jurisdiction/country:us/state:nc/legislature"
c2020 = run_contest(fed["senate2020"], "nc/2020-11-03/us-senate", "nc/2020-11-03/general",
                    sen_jur, "nc/us-senator-class-2", "US Senate",
                    ZIP20, "results_pct_20201103.txt", "November 3, 2020", "nc/us-senator-class-2")
e2020 = {"id": "nc/2020-11-03/general", "name": "North Carolina 2020-11-03 general election",
         "date": "2020-11-03", "election_type": "general", "status": "certified", "contests": [c2020],
         "sources": [
             {"url": "https://www.ncsbe.gov/results-data/election-results/historical-election-results-data",
              "note": "NCSBE Historical Election Results Data page: the November 3, 2020 general election Results (ZIP) file (results_pct_20201103.txt) is the official precinct-level results file for the election. This record currently carries the U.S. Senate (Class II) contest, built for the federal pass of issue #172; each candidate's method columns (Election Day + one-stop early + absentee by mail + provisional) sum to the file's total-votes column on every precinct row.",
              "retrieved": TODAY},
             {"url": ZIP20, "note": "Direct download of the November 3, 2020 general election results file used for the contest totals in this record.", "retrieved": TODAY}]}
hdr = ("# Built from the North Carolina State Board of Elections official\n"
       "# precinct-level results file for the November 3, 2020 general\n"
       "# election (results_pct_20201103.txt). Federal pass, issue #172.\n")
(NC / "elections/nc--2020-11-03--general.yaml").write_text(
    hdr + yaml.safe_dump(e2020, sort_keys=False, allow_unicode=True, width=1000))

# ---- Senate 2022 (Class III) ----
c2022 = run_contest(fed["senate2022"], "nc/2022-11-08/us-senate", "nc/2022-11-08/general",
                    sen_jur, "nc/us-senator-class-3", "US Senate",
                    ZIP22, "results_pct_20221108.txt", "November 8, 2022", "nc/us-senator-class-3")
e2022 = {"id": "nc/2022-11-08/general", "name": "North Carolina 2022-11-08 general election",
         "date": "2022-11-08", "election_type": "general", "status": "certified", "contests": [c2022],
         "sources": [
             {"url": "https://www.ncsbe.gov/results-data/election-results/historical-election-results-data",
              "note": "NCSBE Historical Election Results Data page: the November 8, 2022 general election Results (ZIP) file (results_pct_20221108.txt) is the official precinct-level results file for the election. This record currently carries the U.S. Senate (Class III) contest, built for the federal pass of issue #172 (the 2022 county contests join this file in the county pass); each candidate's method columns (Election Day + one-stop early + absentee by mail + provisional) sum to the file's total-votes column on every precinct row. Write-in rows in the file are not ballot candidates and are not recorded as candidates here.",
              "retrieved": TODAY},
             {"url": ZIP22, "note": "Direct download of the November 8, 2022 general election results file used for the contest totals in this record.", "retrieved": TODAY}]}
hdr = ("# Built from the North Carolina State Board of Elections official\n"
       "# precinct-level results file for the November 8, 2022 general\n"
       "# election (results_pct_20221108.txt). Federal pass, issue #172.\n")
(NC / "elections/nc--2022-11-08--general.yaml").write_text(
    hdr + yaml.safe_dump(e2022, sort_keys=False, allow_unicode=True, width=1000))

# ---- House 2024 ----
house_contests = []
for n_s, cands in sorted(fed["house2024"].items(), key=lambda kv: int(kv[0])):
    n = int(n_s)
    post_id = f"nc-{n}/us-representative"
    jur_id = f"ocd-jurisdiction/country:us/state:nc/cd:{n}/legislature"
    house_contests.append(run_contest(
        cands, f"nc/2024-11-05/us-representative-{n}", "nc/2024-11-05/general",
        jur_id, post_id, f"US House of Representatives District {n}",
        ZIP24, "results_pct_20241105.txt", "November 5, 2024", post_id))
for c in house_contests:
    c["winners"][0]  # sanity
efile = NC / "elections/nc--2024-11-05--general.yaml"
edoc = yaml.safe_load(efile.read_text())
assert len(edoc["contests"]) == 180
edoc["contests"].extend(house_contests)
edoc["sources"][0]["note"] = edoc["sources"][0]["note"].replace(
    "and all 170 General Assembly contests (50 State Senate + 120 State House districts);",
    "all 170 General Assembly contests (50 State Senate + 120 State House districts), and the 14 U.S. House contests;")
edoc["sources"].append({
    "url": ZIP24,
    "note": ("Federal pass (issue #172): the 14 U.S. House contests were aggregated from the same SBE file "
             "(7,270 precinct rows; method columns sum to total votes on every row). The two U.S. Senate seats "
             "were not on the 2024 ballot; their contests live in the 2020 (Class II) and 2022 (Class III) "
             "election records. Presidential contests are not modeled in Civic-Data (no president post exists "
             "in the repo) and are not recorded here."),
    "retrieved": TODAY})
header = ("# Built from the North Carolina State Board of Elections official\n"
          "# precinct-level results file for the November 5, 2024 general\n"
          "# election (results_pct_20241105.txt), aggregated by contest across\n"
          "# all 100 counties. Council of State worked example, issue #172.\n")
efile.write_text(header + yaml.safe_dump(edoc, sort_keys=False, allow_unicode=True, width=1000))

# ---- write people ----
HEADER_NEW = ("# Minted from the NC State Board of Elections official general\n"
              "# election results (federal pass, Civic-Data issue #172).\n")
for pid in touched:
    info = people[pid]
    txt = yaml.safe_dump(info["doc"], sort_keys=False, allow_unicode=True, width=1000)
    if info.get("new"):
        info["path"].write_text(HEADER_NEW + txt)
    else:
        orig = info["path"].read_text()
        i = orig.find("id: ")
        info["path"].write_text(orig[:i] + txt if i > 0 else txt)

# ---- winner membership sources ----
for mpath, zip_url, note in membership_sources:
    d = yaml.safe_load(mpath.read_text())
    d.setdefault("sources", []).append({"url": zip_url, "note": note, "retrieved": TODAY})
    orig = mpath.read_text(); i = orig.find("id: ")
    mpath.write_text((orig[:i] if i > 0 else "") + yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=1000))

print("touched people:", len(touched), "| new people:", len(new_people),
      "| winner memberships sourced:", len(membership_sources))
print("new:", [people[p]["name"] for p in new_people])
