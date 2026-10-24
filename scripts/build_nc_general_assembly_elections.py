#!/usr/bin/env python3
"""Build the NC General Assembly 2024 pass for Civic-Data issue #172:
append all 170 GA contests (50 Senate + 120 House) from the NC SBE
Nov. 5, 2024 precinct results file to the existing 2024 general
election record; add the candidacy to every candidate's person record;
add the SBE source to the 162 continuing winners' memberships; and
model the 8 districts where the 2024 winner has since departed and an
appointee now sits (ended elected membership for the winner +
successor's seeded membership corrected to how_seated: appointed).

Write-in rows in the SBE file (named write-ins and the miscellaneous
buckets in SD31/HD18/HD84) are not persons and are excluded; none won.
"""
import json, re, uuid, unicodedata
from pathlib import Path

import yaml

TREE = Path(__file__).resolve().parent.parent
NC = TREE / "data/us/nc"
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
TODAY = "2026-10-23"
SBE_ZIP = "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2024_11_05/results_pct_20241105.zip"
PARTY = {"DEM": "Democratic", "REP": "Republican", "LIB": "Libertarian",
         "CST": "Constitution", "GRE": "Green", "UNA": "Unaffiliated", "WTP": "We The People", "": None}

# Extraction artifact (contest totals aggregated from the SBE file):
data = json.loads((Path.home() / "workspace/nc172/ga_2024.json").read_text())

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.replace("Mrs.", "")
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"[^a-z ]", "", s.lower())
    return re.sub(r"\s+", " ", s).strip()

def slugify(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)

def last_token(name):
    toks = [t for t in norm(name).split() if t not in ("jr", "sr", "ii", "iii", "iv")]
    return toks[-1] if toks else ""

# ---------- people index ----------
people = {}   # pid -> dict(name, path, doc)
by_slug = {}  # people/state filename slug -> pid
for p in sorted(NC.glob("people/*/*.yaml")):
    d = yaml.safe_load(p.read_text())
    people[d["id"]] = {"name": d["name"], "path": p, "doc": d}
    if p.parent.name == "state":
        by_slug[p.stem] = d["id"]
by_norm = {}
for pid, info in people.items():
    by_norm.setdefault(norm(info["name"]), []).append(pid)

# ---------- posts / jurisdictions / holders ----------
posts = {}
for p in sorted(NC.glob("posts/state/*.yaml")):
    d = yaml.safe_load(p.read_text())
    posts[d["id"]] = d
holders = {}       # post_id -> membership path
holder_pid = {}
for p in sorted(NC.glob("memberships/state/*.yaml")):
    d = yaml.safe_load(p.read_text())
    if d["post_id"].startswith(("nc-house-", "nc-senate-")):
        holders[d["post_id"]] = p
        holder_pid[d["post_id"]] = d["person_id"]

# ---------- successions (sourced 2026-10-23; see #172 comment) ----------
SOG = "https://lrs.sog.unc.edu/sites/default/files/supp_content/2025%20General%20Assembly.pdf"
SUCCESSIONS = {
    "nc-senate-18/state-senator": dict(
        winner="Terence Everitt", start="2025-01-01", end="2026-05-01",
        note="Elected Nov. 5, 2024; resigned effective May 1, 2026 to work full time with the North Carolina Voter Protection Alliance. Haseeb Fatmi was appointed to finish the term, taking office May 21, 2026.",
        succ_note="Appointed to finish Terence Everitt's term after Everitt resigned effective May 1, 2026; took office May 21, 2026. (The seeded record said how_seated: elected; corrected -- Fatmi was appointed, not elected.)",
        urls=["https://en.wikipedia.org/wiki/North_Carolina%27s_18th_Senate_district",
              "https://en.wikipedia.org/wiki/Terence_Everitt"]),
    "nc-senate-23/state-senator": dict(
        winner="Graig Meyer", start="2023-01-01", end="2026-03-31",
        note="Re-elected Nov. 5, 2024 (in the Senate since Jan. 1, 2023); resigned March 31, 2026 to become executive director of the North Carolina Justice Center. Jonah Garson was appointed to finish the term, taking office April 10, 2026.",
        succ_note="Appointed by Gov. Stein to finish Graig Meyer's term after Meyer resigned March 31, 2026; took office April 10, 2026. (The seeded record said how_seated: elected; corrected.)",
        urls=["https://en.wikipedia.org/wiki/North_Carolina%27s_23rd_Senate_district", SOG]),
    "nc-senate-34/state-senator": dict(
        winner="Paul Newton", start="2023-01-01", end="2025-03-26",
        note="Re-elected Nov. 5, 2024 (in the Senate since Jan. 1, 2023); resigned March 26, 2025 to become vice chancellor and general counsel at UNC-Chapel Hill. Chris Measmer was appointed to finish the term, taking office April 10, 2025.",
        succ_note="Appointed to finish Paul Newton's term after Newton resigned March 26, 2025; took office April 10, 2025. (The seeded record said how_seated: elected; corrected.)",
        urls=["https://en.wikipedia.org/wiki/North_Carolina%27s_34th_Senate_district", SOG]),
    "nc-house-40/state-representative": dict(
        winner="Joe John", start="2017-01-01", end="2025-01-21",
        note="Re-elected Nov. 5, 2024 (in the House since Jan. 1, 2017); resigned in January 2025 after announcing a terminal diagnosis (district roster: service ended January 21, 2025; the UNC SOG 2025 General Assembly summary records that he died January 20, 2025). Phil Rubin was appointed to finish the term, taking office January 29, 2025.",
        succ_note="Appointed to finish Joe John's term after John resigned in January 2025; took office January 29, 2025. (The seeded record said how_seated: elected; corrected.)",
        urls=["https://en.wikipedia.org/wiki/North_Carolina%27s_40th_House_district", SOG]),
    "nc-house-47/state-representative": dict(
        winner="Jarrod Lowery", start="2023-01-01", end="2025-10-07",
        note="Re-elected Nov. 5, 2024 (in the House since Jan. 1, 2023); resigned October 7, 2025 to take a position in the U.S. Department of the Interior. His brother John Lowery was appointed to finish the term and sworn in October 17, 2025.",
        succ_note="Appointed to finish his brother Jarrod Lowery's term after Jarrod resigned October 7, 2025; sworn in October 17, 2025. (The seeded record said how_seated: elected; corrected.)",
        urls=["https://en.wikipedia.org/wiki/North_Carolina%27s_47th_House_district",
              "https://en.wikipedia.org/wiki/John_Lowery_(politician)"]),
    "nc-house-60/state-representative": dict(
        winner="Cecil Brockman", start="2015-01-01", end="2025-10-31",
        note="Re-elected Nov. 5, 2024 (in the House since Jan. 1, 2015); resigned October 31, 2025 after being charged with felonies in Guilford County. Amanda Cook was appointed to finish the term, taking office November 18, 2025.",
        succ_note="Appointed to finish Cecil Brockman's term after Brockman resigned October 31, 2025; took office November 18, 2025. (The seeded record said how_seated: elected; corrected.)",
        urls=["https://en.wikipedia.org/wiki/North_Carolina%27s_60th_House_district",
              "https://www.publicradioeast.org/2025-11-15/high-point-council-member-amanda-cook-to-replace-brockman-in-nc-house"]),
    "nc-house-90/state-representative": dict(
        winner="Sarah Stevens", start="2009-01-01", end="2026-06-16",
        note="Re-elected Nov. 5, 2024 (in the House since Jan. 1, 2009); resigned June 16, 2026 to run for the North Carolina Supreme Court. Dan Kiger was appointed to finish the term, taking office June 23, 2026.",
        succ_note="Appointed to finish Sarah Stevens' term after Stevens resigned June 16, 2026 to run for the state Supreme Court; took office June 23, 2026. (The seeded record said how_seated: elected; corrected.)",
        urls=["https://en.wikipedia.org/wiki/North_Carolina%27s_90th_House_district",
              "https://nctribune.com/stevens-leaves-the-house-focuses-on-supreme-court-race/"]),
    "nc-house-119/state-representative": dict(
        winner="Mike Clampitt", start="2021-01-01", end="2026-03-18",
        note="Re-elected Nov. 5, 2024 (current House service since Jan. 1, 2021; also served 2017-2019); died in office March 18, 2026. Anna Ferguson was appointed to finish the term, taking office April 16, 2026.",
        succ_note="Appointed to finish Mike Clampitt's term after Clampitt died in office March 18, 2026; took office April 16, 2026. (The seeded record said how_seated: elected; corrected.)",
        urls=["https://en.wikipedia.org/wiki/North_Carolina%27s_119th_House_district",
              "https://www.nchouserepublicans.com/post/anna-ferguson-selected-to-fill-rep-mike-clampitt-s-seat-in-north-carolina-house-district-119"]),
}
TARE_PID = "ocd-person/e709ca66-bc25-5c45-9cf3-2ec542153db0"  # SD2 loser reuse (Warren Co. commissioner, identical distinctive ballot name)

CH = {
    "senate": dict(pre="nc-senate-", role="state-senator", title="State Senator",
                   role_title="State Senator", jur="sldu", contest="NC STATE SENATE DISTRICT %d",
                   cslug="state-senate-%d"),
    "house": dict(pre="nc-house-", role="state-representative", title="State Representative",
                  role_title="State Representative", jur="sldl", contest="NC HOUSE OF REPRESENTATIVES DISTRICT %d",
                  cslug="state-house-%d"),
}

def new_person(name, contest_id, election_id, jur_id, office_id, party, pipeline):
    slug = slugify(name)
    if slug in by_slug or (NC / f"people/state/{slug}.yaml").exists():
        slug = f"{slug}-{uuid.uuid5(NS, 'collision|nc|' + slug + '|' + name).hex[:8]}"
    pid = "ocd-person/" + str(uuid.uuid5(NS, f"person|nc|state|{slug}"))
    doc = {
        "id": pid, "name": name, "identifiers": [],
        "candidacies": [],
        "verification": {"status": "unverified", "pipeline": pipeline},
        "sources": [],
    }
    people[pid] = {"name": name, "path": NC / f"people/state/{slug}.yaml", "doc": doc, "new": True}
    by_slug[slug] = pid
    return pid

def contest_note(cands, chamber, n):
    title = (CH[chamber]["contest"] % n).title().replace("Nc ", "NC ")
    parts = "; ".join(f"{c['choice']} ({c['party']}) {c['total']:,}" if c["party"]
                      else f"{c['choice']} {c['total']:,}" for c in cands)
    w = cands[0]
    return (f"North Carolina State Board of Elections, official precinct-level results file for the "
            f"November 5, 2024 general election (results_pct_20241105.txt), aggregated across the "
            f"district's precincts: {title} -- {parts}. {w['choice']} won with {w['total']:,} votes.")

contests = []
touched_people = set()
new_people = 0
succ_memberships = []   # (path, doc, header)
succ_fixes = []         # membership paths to correct
membership_sources = [] # continuing-winner membership paths

for chamber in ("senate", "house"):
    cfg = CH[chamber]
    for n_s, cands_all in sorted(data[chamber].items(), key=lambda kv: int(kv[0])):
        n = int(n_s)
        cands = [c for c in cands_all if "Write-In" not in c["choice"]]
        post_id = f"{cfg['pre']}{n}/{cfg['role']}"
        post = posts[post_id]
        jur_id = f"ocd-jurisdiction/country:us/state:nc/{cfg['jur']}:{n}/legislature"
        contest_id = f"nc/2024-11-05/{cfg['cslug'] % n}"
        election_id = "nc/2024-11-05/general"
        note = contest_note(cands, chamber, n)
        hp = holder_pid[post_id]
        succession = SUCCESSIONS.get(post_id)
        cand_pids = []
        for i, c in enumerate(cands):
            party = PARTY.get(c["party"] or "")
            if i == 0 and succession:
                strip_mid = lambda s: " ".join(x for x in norm(s).split() if len(x) > 1)
                assert strip_mid(c["choice"]) == strip_mid(succession["winner"]), (post_id, c)
                pid = new_person(c["choice"], contest_id, election_id, jur_id, post_id, party,
                                 "build_nc_general_assembly")
                new_people += 1
                # ended elected membership for the departed winner
                wslug = slugify(c["choice"])
                mfile = NC / f"memberships/state/{cfg['pre']}{n}-{cfg['role']}-{wslug}.yaml"
                mdoc = {"id": mfile.stem, "person_id": pid, "organization_id": post["organization_id"],
                        "post_id": post_id, "role": cfg["role_title"], "seat": "At-Large",
                        "start": succession["start"], "end": succession["end"], "how_seated": "elected",
                        "sources": [
                            {"url": SBE_ZIP, "note": note, "retrieved": TODAY},
                            *[{"url": u, "note": succession["note"], "retrieved": TODAY} for u in succession["urls"]],
                        ]}
                succ_memberships.append((mfile, mdoc))
                spath = holders[post_id]
                succ_fixes.append((spath, succession))
            elif i == 0:
                pid = hp
                assert norm(people[pid]["name"]).split()[-1] == last_token(c["choice"]), (post_id, c, people[pid]["name"])
                membership_sources.append((holders[post_id], note))
            elif chamber == "senate" and n == 2 and c["choice"] == "Tare (T) Davis":
                pid = TARE_PID
            else:
                hits = by_norm.get(norm(c["choice"]), [])
                state_hits = [h for h in hits if people[h]["path"].parent.name == "state"]
                assert not state_hits, (post_id, c, state_hits)
                pid = new_person(c["choice"], contest_id, election_id, jur_id, post_id, party,
                                 "build_nc_general_assembly")
                new_people += 1
                people[pid]["doc"]["candidacies"].append({
                    "contest_id": contest_id, "election_id": election_id, "jurisdiction_id": jur_id,
                    "office_id": post_id, **({"party": party} if party else {}),
                    "ballot_name": c["choice"], "status": "active"})
                people[pid]["doc"]["sources"].append({"url": SBE_ZIP, "note": note, "retrieved": TODAY})
                touched_people.add(pid)
                cand_pids.append(pid)
                continue
            # existing or succession-winner person: append candidacy + source
            doc = people[pid]["doc"]
            assert all(x["contest_id"] != contest_id for x in doc.get("candidacies", [])), pid
            entry = {"contest_id": contest_id, "election_id": election_id, "jurisdiction_id": jur_id,
                     "office_id": post_id, **({"party": party} if party else {}),
                     "ballot_name": c["choice"], "status": "active"}
            doc.setdefault("candidacies", []).append(entry)
            if not any(s["url"] == SBE_ZIP and note in s.get("note", "") for s in doc.get("sources", [])):
                doc.setdefault("sources", []).append({"url": SBE_ZIP, "note": note, "retrieved": TODAY})
            touched_people.add(pid)
            cand_pids.append(pid)
        w = cands[0]
        winner_pid = cand_pids[0]
        contests.append({
            "id": contest_id, "jurisdiction_id": jur_id, "office_id": post_id, "vote_for": 1,
            "candidate_ids": cand_pids, "result_status": "certified",
            "winners": [{"person_id": winner_pid, "name": people[winner_pid]["name"],
                         "party": PARTY.get(w["party"] or ""), "votes": w["total"]}],
        })

print("contests:", len(contests), "new people:", new_people, "touched people:", len(touched_people))
print("succession winner memberships:", len(succ_memberships), "successor fixes:", len(succ_fixes),
      "continuing winner memberships:", len(membership_sources))
assert len(contests) == 170 and len(succ_memberships) == 8 and len(membership_sources) == 162

# ---------- write people ----------
HEADER_NEW = ("# Minted from the NC State Board of Elections official Nov. 5, 2024\n"
              "# general election results (General Assembly pass, Civic-Data\n"
              "# issue #172).\n")
for pid in touched_people:
    info = people[pid]
    txt = yaml.safe_dump(info["doc"], sort_keys=False, allow_unicode=True, width=1000)
    if info.get("new"):
        info["path"].write_text(HEADER_NEW + txt)
    else:
        orig = info["path"].read_text()
        i = orig.find("id: ")
        info["path"].write_text(orig[:i] + txt if i > 0 else txt)

# ---------- succession winner memberships ----------
for mfile, mdoc in succ_memberships:
    assert not mfile.exists(), mfile
    mfile.write_text(yaml.safe_dump(mdoc, sort_keys=False, allow_unicode=True, width=1000))

# ---------- successor fixes ----------
for spath, s in succ_fixes:
    d = yaml.safe_load(spath.read_text())
    assert d["how_seated"] == "elected"
    d["how_seated"] = "appointed"
    for u in s["urls"]:
        d["sources"].append({"url": u, "note": s["succ_note"], "retrieved": TODAY})
    orig = spath.read_text(); i = orig.find("id: ")
    spath.write_text((orig[:i] if i > 0 else "") + yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=1000))

# ---------- continuing winner membership sources ----------
for mpath, note in membership_sources:
    d = yaml.safe_load(mpath.read_text())
    d.setdefault("sources", []).append({"url": SBE_ZIP, "note": note, "retrieved": TODAY})
    orig = mpath.read_text(); i = orig.find("id: ")
    mpath.write_text((orig[:i] if i > 0 else "") + yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=1000))

# ---------- election file: append contests + GA source ----------
efile = NC / "elections/nc--2024-11-05--general.yaml"
edoc = yaml.safe_load(efile.read_text())
assert len(edoc["contests"]) == 10
edoc["contests"].extend(contests)
edoc["sources"][0]["note"] = edoc["sources"][0]["note"].replace(
    "This election record covers the ten Council of State contests;",
    "This election record covers the ten Council of State contests and all 170 General Assembly contests (50 State Senate + 120 State House districts);")
edoc["sources"].append({
    "url": SBE_ZIP,
    "note": ("General Assembly pass (issue #172): the 170 legislative contests were aggregated from the same "
             "SBE file (13,516 precinct rows; method columns sum to total votes on every row). Write-in rows in "
             "the file (named write-in candidates and the miscellaneous write-in buckets in Senate District 31 "
             "and House Districts 18 and 84) are not ballot candidates and are not recorded as candidates here; "
             "no write-in won. Eight districts' 2024 winners have since departed and been succeeded by "
             "appointees (Senate 18, 23, 34; House 40, 47, 60, 90, 119); those successions are modeled on the "
             "membership records with their own sources."),
    "retrieved": TODAY})
header = ("# Built from the North Carolina State Board of Elections official\n"
          "# precinct-level results file for the November 5, 2024 general\n"
          "# election (results_pct_20241105.txt), aggregated by contest across\n"
          "# all 100 counties. Council of State worked example, issue #172.\n")
efile.write_text(header + yaml.safe_dump(edoc, sort_keys=False, allow_unicode=True, width=1000))
print("election file contests now:", len(edoc["contests"]))
