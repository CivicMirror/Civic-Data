#!/usr/bin/env python3
"""Build the NC school tier (issue #172) from schools_plan.json.

Model (SC #177 schools precedent):
- jurisdictions/school/<root>-school.yaml per LEA (115), classification
  'school', id .../school_district:<root>/school
- one org per LEA (<root>-school-board.yaml, "<Name> Board of Education")
- one post per seat descriptor (<root>/school-board-<key>): single-seat
  descriptors (district/ward/township/named seat/chair) get succession
  seating; the multi-seat at-large class post seats the two most recent
  classes side by side (municipal council convention)
- contests appended to the existing general-election files (2022, 2023,
  2024, 2025), a new 2021 general file (cycle-shifted districts' fallback
  class), and new 2022-05-17 / 2024-03-05 primary files carrying ONLY
  the school board contests decided at the primary (nonpartisan final
  elections; partisan nominating primaries were excluded in the plan)
- 2020 contests are evidence only (4-year classes superseded in 2024)
- membership starts are '<year>-12' (December organization convention);
  a superseded single-seat holder ends when the successor starts
People are reused on a unique statewide name match, else minted under
people/school/.
"""
import json, re, uuid
from pathlib import Path
import yaml

TREE = Path.home() / "workspace/civic-data-nc172"
WS = Path.home() / "workspace/nc172"
PLAN = json.loads((WS / "schools_plan.json").read_text())
NC = TREE / "data/us/nc"
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
RETR = "2026-11-01"
TIER = "school"
PARTY = {"DEM": "Democratic", "REP": "Republican", "LIB": "Libertarian",
         "UNA": "Unaffiliated", "GRE": "Green", "CST": "Constitution",
         "WTP": "We The People"}
BASE = "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS"
ZIPS = {d: f"{BASE}/{d.replace('-', '_')}/results_pct_{d.replace('-', '')}.zip"
        for d in ("2021-11-02", "2022-05-17", "2022-11-08", "2023-11-07",
                  "2024-03-05", "2024-11-05", "2025-11-04")}
PRIMARY_DATES = {"2022-05-17", "2024-03-05"}
BUCKETS = {"Write-In (Miscellaneous)", "Write-In", "WRITE-IN (MISCELLANEOUS)"}
# Limited voting (county-pass K pattern): in these districts the SBE
# "Vote For" is the per-voter instruction (vote for ONE candidate), but
# the top K finishers fill the whole class. Session-law sourced:
# Sampson S.L. 1989-971 (7 members, classes 4/3 in 2022/2024), Perquimans
# S.L. 1993-21 (6 members, 3/3), Clinton City S.L. 1989-886 (6, 3/3),
# Tyrrell G.S. 115C-35(a) (5, classes 3/2). Winners verified against the
# districts' official rosters (2026).
K_OVERRIDE = {
    ("SAMPSON COUNTY", "at-large", "2022-05-17"): 4,
    ("SAMPSON COUNTY", "at-large", "2024-03-05"): 3,
    ("PERQUIMANS COUNTY", "at-large", "2022-05-17"): 3,
    ("PERQUIMANS COUNTY", "at-large", "2024-03-05"): 3,
    ("CLINTON CITY", "at-large", "2022-05-17"): 3,
    ("CLINTON CITY", "at-large", "2024-03-05"): 3,
    ("TYRRELL COUNTY", "at-large", "2022-05-17"): 3,
    ("TYRRELL COUNTY", "at-large", "2024-03-05"): 2,
}
K_LAW = {"SAMPSON COUNTY": "S.L. 1989-971", "PERQUIMANS COUNTY": "S.L. 1993-21",
         "CLINTON CITY": "S.L. 1989-886", "TYRRELL COUNTY": "G.S. 115C-35(a)"}
# Named posts that are multi-seat despite vote-for 1 in every contest
# (staggered one-seat classes): Gastonia Township elects TWO members of
# the Gaston County board (S.L. 1977-633; district roster confirms both
# the 2022 and 2024 winners sit).
POST_MULTI = {("GASTON COUNTY", "gastonia"),
              # Mount Airy City: 7-member board (S.L. 2019-63) = Districts
              # A/B with two staggered seats each + C/D one each + 1
              # at-large; the SBE arithmetic admits no other reading
              ("MOUNT AIRY CITY", "district-a"),
              ("MOUNT AIRY CITY", "district-b")}


def eff_vf(root, c):
    return K_OVERRIDE.get((root, c["post_key"], c["date"]), c["vote_for"])
# official-name overrides keyed by plan root (filled from the NC DPI roster)
NAME_OVERRIDES = {}
stats = {"jurisdictions": 0, "orgs": 0, "posts": 0, "memberships": 0,
         "ended": 0, "people_new": 0, "people_reused": 0, "contests": 0}
flags = []


def load_yaml(p):
    return yaml.safe_load(Path(p).read_text())


def dump_yaml(p, data, header=""):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(header + yaml.safe_dump(
        data, sort_keys=False, allow_unicode=True, width=1000))


def norm(name):
    n = name.lower()
    n = re.sub(r"\([^)]*\)", " ", n)
    n = re.sub(r'"[^"]*"', " ", n)
    n = re.sub(r"[^a-z0-9 ]", " ", n)
    return re.sub(r"\s+", " ", n).strip()


def clean(choice):
    return re.sub(r"\s+", " ", choice.replace(" (Write-In)", "")).strip()


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return re.sub(r"-+", "-", s)


# ---------- people registry (all tiers, unique-name reuse) ----------
people = {}
by_name = {}
for tier in ("county", "federal", "municipal", "state", "judicial-district", "school"):
    d = NC / "people" / tier
    if not d.exists():
        continue
    for f in d.glob("*.yaml"):
        data = load_yaml(f)
        people[data["id"]] = (f, data)
        by_name.setdefault(norm(data["name"]), []).append(data["id"])
changed_people = set()


def new_person(name):
    slug = slugify(name)
    pid = "ocd-person/" + str(uuid.uuid5(NS, f"person|nc|{TIER}|{slug}"))
    path = NC / "people" / TIER / f"{slug}.yaml"
    if pid in people or path.exists():
        if path.exists() and pid not in people:
            data = load_yaml(path)
            people[data["id"]] = (path, data)
            return data["id"]
        slug2 = slug + "-" + uuid.uuid5(NS, f"person|nc|{TIER}|{slug}|{norm(name)}").hex[:8]
        pid = "ocd-person/" + str(uuid.uuid5(NS, f"person|nc|{TIER}|{slug2}"))
        path = NC / "people" / TIER / f"{slug2}.yaml"
    data = {"id": pid, "name": name, "identifiers": [], "candidacies": [],
            "sources": [],
            "verification": {"status": "unverified",
                             "pipeline": "build_nc_schools"}}
    people[pid] = (path, data)
    by_name.setdefault(norm(name), []).append(pid)
    stats["people_new"] += 1
    return pid


def find_person(name):
    hits = by_name.get(norm(name), [])
    if len(hits) == 1:
        stats["people_reused"] += 1
        return hits[0]
    return new_person(name)


def add_candidacy(pid, cand):
    path, data = people[pid]
    if any(c["contest_id"] == cand["contest_id"] for c in data["candidacies"]):
        return
    data["candidacies"].append(cand)
    changed_people.add(pid)


def add_source(pid, url, note):
    path, data = people[pid]
    if not any(s.get("url") == url and s.get("note") == note for s in data["sources"]):
        data["sources"].append({"url": url, "note": note, "retrieved": RETR})
        changed_people.add(pid)


def party_for(row, has_code):
    if "(Write-In)" in row["choice"]:
        return "Write-In"
    if row["party"]:
        return PARTY.get(row["party"], row["party"])
    return "Unaffiliated" if has_code else "Nonpartisan"


# ---------- contest selection ----------
def select_contests(lea):
    """Apply the build window: drop 2020; multi-seat posts keep only
    their two most recent contest dates."""
    cs = [c for c in lea["contests"] if c["date"] != "2020-11-03"]
    multi_dates = {}
    for c in cs:
        if not c["single"]:
            multi_dates.setdefault(c["post_key"], set()).add(c["date"])
    keep_dates = {k: sorted(v)[-2:] for k, v in multi_dates.items()}
    return [c for c in cs if c["single"] or c["date"] in keep_dates[c["post_key"]]]


# ---------- structure ----------
HDR = "# Built for issue #172 (North Carolina master tracking) from NC SBE results.\n"
jurisdictions, orgs, posts = {}, {}, {}


def ensure_jurisdiction(root_slug, name, contests):
    if root_slug in jurisdictions:
        return jurisdictions[root_slug]
    jid = f"ocd-jurisdiction/country:us/state:nc/school_district:{root_slug}/school"
    dates = sorted({c["date"] for c in contests})
    srcs = [{"url": ZIPS[d],
             "note": (f"NC SBE {d} results (Election Results series): {name} "
                      f"board of education contests appear on the ballot in "
                      f"this file."),
             "retrieved": RETR} for d in dates]
    data = {"id": jid, "name": name, "state": "nc",
            "division_id": f"ocd-division/country:us/state:nc/school_district:{root_slug}",
            "classification": "school", "sources": srcs}
    dump_yaml(NC / f"jurisdictions/school/{root_slug}-school.yaml", data, HDR)
    jurisdictions[root_slug] = jid
    stats["jurisdictions"] += 1
    return jid


def ensure_org(root_slug, lea_name, jid):
    if root_slug in orgs:
        return orgs[root_slug][0]
    oid = "ocd-organization/" + str(uuid.uuid5(NS, f"org|nc|{TIER}|{root_slug}"))
    data = {"id": oid, "name": f"{lea_name} Board of Education",
            "jurisdiction_id": jid, "identifiers": [],
            "sources": [{"url": ZIPS["2024-11-05"],
                         "note": (f"The elected board of education for {lea_name}; "
                                  f"its contests appear in the NC SBE results files "
                                  f"used for issue #172."),
                         "retrieved": RETR}]}
    dump_yaml(NC / f"organizations/school/{root_slug}-school-board.yaml", data, HDR)
    orgs[root_slug] = (oid, f"{root_slug}-school-board")
    stats["orgs"] += 1
    return oid


def ensure_post(post_id, file_slug, oid, title, seats, note, url):
    if post_id in posts:
        return
    data = {"id": post_id, "organization_id": oid, "title": title,
            "seats": seats, "identifiers": [],
            "sources": [{"url": url, "note": note, "retrieved": RETR}]}
    path = NC / f"posts/school/{file_slug}.yaml"
    dump_yaml(path, data, HDR)
    posts[post_id] = (path, data)
    stats["posts"] += 1


# ---------- memberships ----------
memberships = {}
mdir = NC / "memberships/school"
if mdir.exists():
    for f in mdir.glob("*.yaml"):
        data = load_yaml(f)
        memberships.setdefault(data["post_id"], []).append((f, data))
changed_memberships = set()


def _write_membership(post_id, pid, start, note, url):
    pdata = posts[post_id][1]
    role = "School Board Chair" if post_id.endswith("/school-board-chair") \
        else "School Board Member"
    slug = slugify(people[pid][1]["name"])
    fname = f"{post_id.replace('/', '-')}-{slug}.yaml"
    path = NC / f"memberships/school/{fname}"
    n = 2
    lst = memberships.setdefault(post_id, [])
    while path.exists() or any(p == path for p, _ in lst):
        path = NC / f"memberships/school/{fname[:-5]}-{n}.yaml"
        n += 1
    data = {"id": path.stem, "person_id": pid,
            "organization_id": pdata["organization_id"],
            "post_id": post_id, "role": role, "start": start,
            "how_seated": "elected",
            "sources": [{"url": url, "note": note, "retrieved": RETR}]}
    lst.append((path, data))
    changed_memberships.add(path)
    stats["memberships"] += 1


def seat_single(post_id, pid, start, note, url):
    """Single-seat post: successor ends the open holder's membership."""
    lst = memberships.setdefault(post_id, [])
    for path, m in lst:
        if m["person_id"] == pid and "end" not in m:
            return
    for path, m in lst:
        if "end" not in m:
            m["end"] = start
            changed_memberships.add(path)
            stats["ended"] += 1
    _write_membership(post_id, pid, start, note, url)


def seat_multi(post_id, pid, start, note, url):
    """Multi-seat class post: classes sit side by side; a re-elected
    member's open membership simply continues."""
    lst = memberships.setdefault(post_id, [])
    for path, m in lst:
        if m["person_id"] == pid and "end" not in m:
            return
    _write_membership(post_id, pid, start, note, url)


# ---------- elections ----------
elections = {}


def election_file(dt):
    if dt in elections:
        return elections[dt]
    if dt in PRIMARY_DATES:
        path = NC / f"elections/nc--{dt}--primary.yaml"
        data = {"id": f"nc/{dt}/primary", "name": f"{dt[:4]} Primary Election",
                "date": dt, "election_type": "primary", "status": "certified",
                "contests": [],
                "sources": [{"url": ZIPS[dt],
                             "note": ("School pass (issue #172): this file carries "
                                      "only the NC school board contests that are "
                                      "DECIDED at the primary -- nonpartisan final "
                                      "elections held on the primary date under "
                                      "local acts (the winners take the seats; "
                                      "there is no November contest for them). "
                                      "Partisan nominating primaries for school "
                                      "boards are not modeled; those seats are "
                                      "built from the November general election."),
                             "retrieved": RETR}]}
        elections[dt] = (path, data, "")
    elif dt == "2021-11-02":
        path = NC / f"elections/nc--{dt}--general.yaml"
        data = {"id": f"nc/{dt}/general", "name": "2021 General Election",
                "date": dt, "election_type": "general", "status": "certified",
                "contests": [],
                "sources": [{"url": ZIPS[dt],
                             "note": ("School pass (issue #172): school board "
                                      "contests only -- the districts whose "
                                      "election cycle later shifted to even years "
                                      "(their 2021 classes are the fallback "
                                      "holders for seats not re-contested since)."),
                             "retrieved": RETR}]}
        elections[dt] = (path, data, "")
    else:
        path = NC / f"elections/nc--{dt}--general.yaml"
        data = load_yaml(path)
        hdr = path.read_text().split("id: ")[0]
        elections[dt] = (path, data, hdr)
    return elections[dt]


# ---------- main ----------
for lea in PLAN["leas"]:
    root = lea["root"]
    root_slug = slugify(root)
    name = NAME_OVERRIDES.get(root, lea["name"])
    contests = select_contests(lea)
    if not contests:
        flags.append(f"NO KEPT CONTESTS: {name}")
        continue
    jid = ensure_jurisdiction(root_slug, name, contests)
    oid = ensure_org(root_slug, name, jid)
    # posts first (seats need all kept fills)
    postmap = {}
    for p in lea["posts"]:
        kept = [c for c in contests if c["post_key"] == p["key"]]
        if not kept:
            continue
        # a named district can still be multi-member (e.g. Winston-Salem/
        # Forsyth District 2 elects 4): multi-seat posts seat their
        # classes side by side instead of by succession
        is_multi = ((not p["single"]) or (root, p["key"]) in POST_MULTI
                    or any(eff_vf(root, c) > 1 for c in kept))
        seats = 1 if (p["single"] and not is_multi) else sum(
            max(eff_vf(root, c) for c in contests
                if c["post_key"] == p["key"] and c["date"] == d)
            for d in {c["date"] for c in kept})
        post_id = f"{root_slug}/school-board-{p['key']}"
        postmap[p["key"]] = (post_id, is_multi)
        dates = sorted({c['date'] for c in kept})
        ensure_post(post_id, f"{root_slug}-school-board-{p['key']}", oid,
                    f"School Board {p['title']}", seats,
                    (f"{name}, built from the NC SBE results for the "
                     f"{' and '.join(dates)} elections (school board "
                     f"contests) in the Election Results series."),
                    ZIPS[dates[-1]])
    for c in sorted(contests, key=lambda c: c["date"]):
        dt = c["date"]
        post_id, is_multi = postmap[c["post_key"]]
        etype = "primary" if dt in PRIMARY_DATES else "general"
        cid = f"nc/{dt}/{root_slug}-school-board-{c['post_key']}"
        rows = [r for r in c["cands"] if r["choice"] not in BUCKETS
                and re.search(r"[A-Za-z]", r["choice"])]
        has_code = any(r["party"] for r in rows if "(Write-In)" not in r["choice"])
        vf = eff_vf(root, c)
        rows.sort(key=lambda r: -r["total"])
        # winners: top vf, with tie detection at the cutoff
        if len(rows) > vf and rows[vf]["total"] == rows[vf - 1]["total"]:
            t = rows[vf - 1]["total"]
            clear = [r for r in rows if r["total"] > t]
            tied = [r for r in rows if r["total"] == t]
            n_take = vf - len(clear)
            flags.append(f"TIE at cutoff: {dt} {c['name']} -- {len(tied)} "
                         f"tied for {n_take} seat(s) at {t} votes: "
                         f"{[r['choice'] for r in tied]}")
            winners = clear if len(tied) > n_take else clear + tied
        else:
            winners = rows[:vf]
        prim_note = (" This nonpartisan school board election is decided "
                     "at the primary; there is no November contest for "
                     "this seat.") if dt in PRIMARY_DATES else ""
        unexp_note = " Unexpired-term contest." if c["unexpired"] else ""
        lv_note = ""
        if (root, c["post_key"], dt) in K_OVERRIDE:
            lv_note = (f" Limited voting ({K_LAW[root]}): the ballot "
                       f"instructs each voter to vote for one candidate, "
                       f"and the top {vf} finishers fill the {vf}-seat class.")
        note = (f"NC SBE {dt} results (Election Results series): {c['name']} -- "
                + "; ".join(f"{clean(r['choice'])} ({party_for(r, has_code)}) "
                            f"{r['total']:,}" for r in rows)
                + f". Winners are the top {vf} by total votes.{prim_note}{unexp_note}{lv_note}")
        cand_ids = []
        for r in rows:
            nm = clean(r["choice"])
            pid = find_person(nm)
            if pid not in cand_ids:
                cand_ids.append(pid)
            add_candidacy(pid, {"contest_id": cid,
                                "election_id": f"nc/{dt}/{etype}",
                                "jurisdiction_id": jid, "office_id": post_id,
                                "party": party_for(r, has_code),
                                "ballot_name": nm, "status": "active"})
            add_source(pid, ZIPS[dt], note)
        path_ef, ef, hdr = election_file(dt)
        if not any(x["id"] == cid for x in ef["contests"]):
            ef["contests"].append({
                "id": cid, "jurisdiction_id": jid, "office_id": post_id,
                "vote_for": c["vote_for"], "candidate_ids": cand_ids,
                "result_status": "certified",
                "winners": [{"person_id": find_person(clean(r["choice"])),
                             "name": clean(r["choice"]), "votes": r["total"],
                             "party": party_for(r, has_code)} for r in winners]})
            stats["contests"] += 1
        start = f"{dt[:4]}-07" if dt in PRIMARY_DATES else f"{dt[:4]}-12"
        for r in winners:
            pid = find_person(clean(r["choice"]))
            if is_multi:
                seat_multi(post_id, pid, start, note, ZIPS[dt])
            else:
                seat_single(post_id, pid, start, note, ZIPS[dt])

# ---------- write-out ----------
for dt, (path, ef, hdr) in elections.items():
    if dt not in PRIMARY_DATES and dt != "2021-11-02":
        if not any(s.get("note", "").startswith("School pass (issue #172)")
                   for s in ef["sources"]):
            ef["sources"].append({
                "url": ZIPS[dt],
                "note": ("School pass (issue #172): school board contests "
                         "appended from this same NC SBE results file."),
                "retrieved": RETR})
    dump_yaml(path, ef, hdr)
for pid in changed_people:
    path, data = people[pid]
    dump_yaml(path, data)
for path in changed_memberships:
    for lst in memberships.values():
        for p, data in lst:
            if p == path:
                dump_yaml(p, data, HDR)
                break

print("STATS:", json.dumps(stats))
print("FLAGS:", len(flags))
for f in flags:
    print("  ", f)
