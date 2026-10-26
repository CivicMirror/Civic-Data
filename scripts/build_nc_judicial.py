#!/usr/bin/env python3
"""Build the NC judicial tier (issue #172) from judicial_plan.json.

Model (MS #41 / OR #170 judicial-district precedent):
- jurisdictions/judicial-district/<system>-district-<d>.yaml per district
  (superior court, district court, prosecutorial) + a statewide judiciary
  jurisdiction for the appellate courts.
- one org per court/office per district; one single-seat post per
  (district, seat); appellate posts per numbered seat.
- contests appended to the 2020/2022/2024 election files; winners seated
  with Jan-1 starts (unexpired-term winners: December, month precision);
  a superseded holder ends the day the successor's term starts.
People are reused on a unique statewide name match, else minted under
people/judicial-district/.
"""
import json, re, sys, uuid
from pathlib import Path
import yaml

TREE = Path.home() / "workspace/civic-data-nc172"
WS = Path.home() / "workspace/nc172"
PLAN = json.loads((WS / "judicial_plan.json").read_text())
NC = TREE / "data/us/nc"
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
RETR = "2026-10-26"
PARTY = {"DEM": "Democratic", "REP": "Republican", "LIB": "Libertarian",
         "UNA": "Unaffiliated", "GRE": "Green", "CST": "Constitution",
         "WTP": "We The People"}
ZIPS = {"2020-11-03": "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2020_11_03/results_pct_20201103.zip",
        "2022-11-08": "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2022_11_08/results_pct_20221108.zip",
        "2024-11-05": "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2024_11_05/results_pct_20241105.zip"}
BUCKETS = {"Write-In (Miscellaneous)", "Write-In", "WRITE-IN (MISCELLANEOUS)"}
stats = {"jurisdictions": 0, "orgs": 0, "posts": 0, "memberships": 0,
         "ended": 0, "people_new": 0, "people_reused": 0, "contests": 0}

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
people = {}          # pid -> (path, data)
by_name = {}         # norm name -> [pid]
for tier in ("county", "federal", "municipal", "state", "judicial-district"):
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
    pid = "ocd-person/" + str(uuid.uuid5(NS, f"person|nc|judicial-district|{slug}"))
    path = NC / "people/judicial-district" / f"{slug}.yaml"
    if pid in people or path.exists():
        if path.exists() and pid not in people:
            data = load_yaml(path)
            people[data["id"]] = (path, data)
            return data["id"]
        slug2 = slug + "-" + uuid.uuid5(NS, f"person|nc|judicial-district|{slug}|{norm(name)}").hex[:8]
        pid = "ocd-person/" + str(uuid.uuid5(NS, f"person|nc|judicial-district|{slug2}"))
        path = NC / "people/judicial-district" / f"{slug2}.yaml"
    data = {"id": pid, "name": name, "identifiers": [], "candidacies": [],
            "sources": [],
            "verification": {"status": "unverified",
                             "pipeline": "build_nc_judicial"}}
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

# ---------- structure ----------
SYS = {  # kind -> (jur slug prefix, org name fmt, post office slug, title)
    "superior": ("superior-court-district", "North Carolina Superior Court, District {}",
                 "judge", "Superior Court Judge"),
    "dc": ("district-court-district", "North Carolina District Court, District {}",
           "judge", "District Court Judge"),
    "da": ("prosecutorial-district", "Office of the District Attorney, District {}",
           "district-attorney", "District Attorney"),
}
jurisdictions = {}   # slug -> jid
orgs = {}            # key -> (oid, file slug)
posts = {}           # post id -> (path, data)

def ensure_jurisdiction(slug, name, dates, sample):
    if slug in jurisdictions:
        return jurisdictions[slug]
    jid = f"ocd-jurisdiction/country:us/state:nc/judicial_district:{slug}/judiciary"
    srcs = [{"url": ZIPS[d], "note":
             f"NC SBE {d} results (Election Results series): the district "
             f"appears on the ballot as '{sample}'." , "retrieved": RETR}
            for d in sorted(set(dates))]
    data = {"id": jid, "name": name, "state": "nc",
            "division_id": f"ocd-division/country:us/state:nc/judicial_district:{slug}",
            "classification": "judiciary", "sources": srcs}
    dump_yaml(NC / f"jurisdictions/judicial-district/{slug}.yaml", data,
              "# Built for issue #172 (North Carolina master tracking) from NC SBE results.\n")
    jurisdictions[slug] = jid
    stats["jurisdictions"] += 1
    return jid

def ensure_org(key, file_slug, name, jid, note_url, note):
    if key in orgs:
        return orgs[key][0]
    oid = "ocd-organization/" + str(uuid.uuid5(NS, f"org|nc|judicial-district|{file_slug}"))
    data = {"id": oid, "name": name, "jurisdiction_id": jid, "identifiers": [],
            "sources": [{"url": note_url, "note": note, "retrieved": RETR}]}
    dump_yaml(NC / f"organizations/judicial-district/{file_slug}.yaml", data,
              "# Built for issue #172 (North Carolina master tracking) from NC SBE results.\n")
    orgs[key] = (oid, file_slug)
    stats["orgs"] += 1
    return oid

def ensure_post(post_id, file_slug, oid, title, src_note, src_url):
    if post_id in posts:
        return
    data = {"id": post_id, "organization_id": oid, "title": title, "seats": 1,
            "identifiers": [],
            "sources": [{"url": src_url, "note": src_note, "retrieved": RETR}]}
    path = NC / f"posts/judicial-district/{file_slug}.yaml"
    dump_yaml(path, data,
              "# Built for issue #172 (North Carolina master tracking) from NC SBE results.\n")
    posts[post_id] = (path, data)
    stats["posts"] += 1

# statewide judiciary jurisdiction + appellate orgs (MS judiciary precedent:
# ocd-jurisdiction/country:us/state:<st>/judiciary, file in jurisdictions/state/)
app_jid = "ocd-jurisdiction/country:us/state:nc/judiciary"
app_path = NC / "jurisdictions/state/nc-judiciary.yaml"
if not app_path.exists():
    dump_yaml(app_path, {
        "id": app_jid, "name": "North Carolina (Judiciary)", "state": "nc",
        "division_id": "ocd-division/country:us/state:nc",
        "classification": "judiciary",
        "sources": [{"url": ZIPS[d], "note":
                     f"NC SBE {d} results (Election Results series): the "
                     f"statewide appellate contests (Supreme Court, Court of "
                     f"Appeals) appear on the ballot in this file.",
                     "retrieved": RETR}
                    for d in ("2020-11-03", "2022-11-08", "2024-11-05")]},
        "# Built for issue #172 (North Carolina master tracking) from NC SBE results.\n")
    stats["jurisdictions"] += 1
sup_org = ensure_org("supreme", "nc-supreme-court", "North Carolina Supreme Court",
                     app_jid, ZIPS["2024-11-05"],
                     "The court appears on the ballot statewide in the NC SBE results (Supreme Court associate justice and chief justice contests).")
coa_org = ensure_org("coa", "nc-court-of-appeals", "North Carolina Court of Appeals",
                     app_jid, ZIPS["2024-11-05"],
                     "The court appears on the ballot statewide in the NC SBE results (Court of Appeals judge contests, seats 1-15).")

def appellate_post(kind, seat):
    if kind == "supreme_chief":
        pid, slug, title = ("supreme-court/chief-justice",
                            "nc-supreme-court-chief-justice", "Chief Justice")
        oid = sup_org
    elif kind == "supreme":
        pid = f"supreme-court/associate-justice-seat-{seat}"
        slug = f"nc-supreme-court-associate-justice-seat-{seat}"
        title = f"Associate Justice, Seat {seat}"
        oid = sup_org
    else:
        pid = f"court-of-appeals/judge-seat-{seat}"
        slug = f"nc-court-of-appeals-judge-seat-{seat}"
        title = f"Judge, Seat {seat}"
        oid = coa_org
    return pid, slug, title, oid

# ---------- contests ----------
contests = [c for c in PLAN["contests"] if not c.get("excluded")]
contests.sort(key=lambda c: (c["date"], c["kind"], c["sbe"]))
elections = {}
for dt in ("2020-11-03", "2022-11-08", "2024-11-05"):
    elections[dt] = load_yaml(NC / f"elections/nc--{dt}--general.yaml")

memberships = {}     # post_id -> list of (path, data)
def load_memberships():
    d = NC / "memberships/judicial-district"
    if d.exists():
        for f in d.glob("*.yaml"):
            data = load_yaml(f)
            memberships.setdefault(data["post_id"], []).append((f, data))
load_memberships()
changed_memberships = set()

def seat_winner(post_id, pid, start, note, url):
    lst = memberships.setdefault(post_id, [])
    for path, m in lst:
        if m["person_id"] == pid and "end" not in m:
            return  # continuous service
    for path, m in lst:
        if "end" not in m:
            m["end"] = start
            changed_memberships.add(path)
            stats["ended"] += 1
    slug = slugify(people[pid][1]["name"])
    fname = f"{post_id.replace('/', '-')}-{slug}.yaml"
    path = NC / f"memberships/judicial-district/{fname}"
    n = 2
    while path.exists() or any(p == path for p, _ in lst):
        path = NC / f"memberships/judicial-district/{fname[:-5]}-{n}.yaml"
        n += 1
    pdata = posts[post_id][1]
    role = re.sub(r", Seat \d+$", "", pdata["title"])
    data = {"id": path.stem, "person_id": pid,
            "organization_id": pdata["organization_id"],
            "post_id": post_id, "role": role, "start": start,
            "how_seated": "elected",
            "sources": [{"url": url, "note": note, "retrieved": RETR}]}
    memberships[post_id].append((path, data))
    changed_memberships.add(path)
    stats["memberships"] += 1

def party_for(row, has_code):
    if "(Write-In)" in row["choice"]:
        return "Write-In"
    if row["party"]:
        return PARTY.get(row["party"], row["party"])
    return "Unaffiliated" if has_code else "Nonpartisan"

# group contests by district for jurisdiction creation
by_struct = {}
for c in contests:
    by_struct.setdefault(c["kind"], {}).setdefault(
        c.get("district"), []).append(c)

for kind in ("superior", "dc", "da"):
    prefix, orgfmt, _, _ = SYS[kind]
    for dist, cs in sorted(by_struct.get(kind, {}).items()):
        slug = f"{prefix}-{dist.lower()}"
        ensure_jurisdiction(slug, f"District {dist} (North Carolina "
                            f"{'Superior Court' if kind=='superior' else 'District Court' if kind=='dc' else 'Prosecutorial District'})",
                            [c["date"] for c in cs], cs[0]["sbe"])

for c in contests:
    dt = c["date"]
    rows = [r for r in c["cands"] if r["choice"] not in BUCKETS
            and re.search(r"[A-Za-z]", r["choice"])]
    has_code = any(r["party"] for r in rows if "(Write-In)" not in r["choice"])
    if c["kind"] in ("supreme_chief", "supreme", "coa"):
        post_id, pslug, title, oid = appellate_post(c["kind"], c["seat"])
        jid = app_jid
        cid_part = pslug[len("nc-"):]
        org_note = ZIPS[dt]
    else:
        prefix, orgfmt, office, title0 = SYS[c["kind"]]
        dist = c["district"]
        jslug = f"{prefix}-{dist.lower()}"
        jid = jurisdictions[jslug]
        oslug = f"nc-{jslug}"
        oid = ensure_org(jslug, oslug, orgfmt.format(dist), jid, ZIPS[dt],
                         f"Office/court for {jslug.replace('-', ' ')}; contests "
                         f"appear in the NC SBE results for this district.")
        if c["kind"] == "da":
            post_id = f"{jslug}/district-attorney"
            pslug = f"{oslug}-district-attorney"
            title = "District Attorney"
        else:
            post_id = f"{jslug}/judge-seat-{c['seat']}"
            pslug = f"{oslug}-judge-seat-{c['seat']}"
            title = f"{title0}, Seat {c['seat']}"
        cid_part = post_id.replace("/", "-")
    note = (f"NC SBE {dt} results (Election Results series): {c['sbe']} -- " +
            "; ".join(f"{r['choice']} ({party_for(r, has_code)}) {r['total']:,}"
                      for r in rows) +
            ". Winner is the top vote-getter (single-seat contest).")
    ensure_post(post_id, pslug,
                oid, title, note, ZIPS[dt])
    # candidates + winner
    cand_ids, winner = [], None
    for r in rows:
        nm = clean(r["choice"])
        pid = find_person(nm)
        if pid not in cand_ids:
            cand_ids.append(pid)
        add_candidacy(pid, {"contest_id": f"nc/{dt}/{cid_part}",
                            "election_id": f"nc/{dt}/general",
                            "jurisdiction_id": jid, "office_id": post_id,
                            "party": party_for(r, has_code),
                            "ballot_name": nm, "status": "active"})
        add_source(pid, ZIPS[dt], note)
        if winner is None:
            winner = (pid, r)
    ef = elections[dt]
    if not any(x["id"] == f"nc/{dt}/{cid_part}" for x in ef["contests"]):
        w = {"person_id": winner[0], "name": people[winner[0]][1]["name"],
             "votes": winner[1]["total"],
             "party": party_for(winner[1], has_code)}
        ef["contests"].append({"id": f"nc/{dt}/{cid_part}",
                               "jurisdiction_id": jid, "office_id": post_id,
                               "vote_for": 1, "candidate_ids": cand_ids,
                               "result_status": "certified", "winners": [w]})
        stats["contests"] += 1
    start = f"{dt[:4]}-12" if c["unexpired"] else f"{int(dt[:4]) + 1}-01-01"
    seat_winner(post_id, winner[0], start, note, ZIPS[dt])

# structure-only appellate seats (election predates the pulled files)
for kind, seat in (("supreme", 7), ("coa", 1), ("coa", 2), ("coa", 3)):
    post_id, pslug, title, oid = appellate_post(kind, seat)
    ensure_post(post_id, pslug, oid, title,
                "Seat in the court's numbered seats (SBE contest names run "
                "Seat 1-15 for the Court of Appeals and Chief Justice + "
                "Associate Justice Seats 2-7 for the Supreme Court). This "
                "seat's current term was filled at an election before the "
                "2020-2024 SBE files pulled for issue #172 (2018 class; "
                "next election 2026), so no contest or holder is built "
                "from those files.", ZIPS["2024-11-05"])

# ---------- write-out ----------
for dt, ef in elections.items():
    if not any(s.get("note", "").startswith("Judicial pass (issue #172)")
               for s in ef["sources"]):
        ef["sources"].append({
            "url": ZIPS[dt],
            "note": "Judicial pass (issue #172): Supreme Court, Court of "
                    "Appeals, Superior Court, District Court and District "
                    "Attorney contests appended from this same NC SBE "
                    "results file; see the 'kept contests' in the pass "
                    "plan (District Court 2020 contests excluded -- 4-year "
                    "terms, that class was re-elected in 2024).",
            "retrieved": RETR})
    hdr = (NC / f"elections/nc--{dt}--general.yaml").read_text().split("id: ")[0]
    dump_yaml(NC / f"elections/nc--{dt}--general.yaml", ef, hdr)
for pid in changed_people:
    path, data = people[pid]
    hdr = ""
    if path.exists():
        hdr = path.read_text().split("id: ")[0]
    dump_yaml(path, data, hdr)
for path in changed_memberships:
    for lst in memberships.values():
        for p, m in lst:
            if p == path:
                dump_yaml(p, m)
print(stats)
print("people touched:", len(changed_people))
