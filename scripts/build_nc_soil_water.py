#!/usr/bin/env python3
"""Build the NC Soil & Water Conservation District tier (issue #172)
from soil.json (NC SBE Election Results extracts).

Scope (Walter's ruling 2026-11-01, completing the county-pass flag):
Soil & Water supervisor contests ride every even-year SBE general file
(100 county contests per cycle) and the office is general-public
elected, so the tier is built -- as an add-on to PR #202 alongside the
school pass, at Walter's direction.

Model (SC #177 soil & water precedent, adapted to NC law):
- G.S. 139-6/139-7: each district board has five supervisors -- three
  ELECTED (nonpartisan, at the general election, staggered four-year
  terms: a class of two and a class of one) and two appointed by the NC
  Soil and Water Conservation Commission. Only the elected seats are
  modeled (SC Bamberg-style: build the elected seats of a hybrid body).
- 96 districts (NC Dept. of Agriculture & Consumer Services): 95 follow
  county lines; the Albemarle district spans Camden, Chowan, Currituck,
  Pasquotank and Perquimans, each county electing its own three
  supervisors to the shared board (15 elected + 2 appointed = 17).
- jurisdictions/special-district/<slug>.yaml, classification
  'government', id .../special_district:<slug>/government
- one org per district, one post per county delegation
  (<slug>/supervisor, seats 3), title 'Soil and Water Conservation
  District Supervisor'
- contests appended to the existing 2022 and 2024 general election
  files (202 contests minus none: 100 per cycle x 2). The 2020 class
  was superseded in 2024 and is evidence only.
- memberships start '<year>-12' (supervisors take office the first
  Monday in December, G.S. 139-6); classes sit side by side.
- named write-in winners are seated with party 'Write-In' (standing
  rule); the miscellaneous write-in bucket is not a candidate.
People are reused on a unique statewide name match, else minted under
people/special-district/.
"""
import json, re, uuid
from pathlib import Path
import yaml

TREE = Path.home() / "workspace/civic-data-nc172"
WS = Path.home() / "workspace/nc172"
SOIL = json.loads((WS / "soil.json").read_text())
NC = TREE / "data/us/nc"
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
RETR = "2026-11-01"
TIER = "special-district"
BASE = "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS"
ZIPS = {d: f"{BASE}/{d.replace('-', '_')}/results_pct_{d.replace('-', '')}.zip"
        for d in ("2022-11-08", "2024-11-05")}
BUCKETS = {"Write-In (Miscellaneous)", "Write-In", "WRITE-IN (MISCELLANEOUS)"}
ALBEMARLE = {"CAMDEN", "CHOWAN", "CURRITUCK", "PASQUOTANK", "PERQUIMANS"}
TITLE_FIX = {"MCDOWELL": "McDowell"}
STATUTE_URL = "https://www.ncleg.gov/EnactedLegislation/Statutes/HTML/ByChapter/Chapter_139.html"
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


def county_name(raw):
    return TITLE_FIX.get(raw, raw.title())


# ---------- people registry (all tiers, unique-name reuse) ----------
people = {}
by_name = {}
for tier in ("county", "federal", "municipal", "state", "judicial-district",
             "school", "special-district"):
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
                             "pipeline": "build_nc_soil_water"}}
    people[pid] = (path, data)
    by_name.setdefault(norm(name), []).append(pid)
    stats["people_new"] += 1
    return pid


resolved = {}


def find_person(name):
    # Resolution must be idempotent within the run: for a name with
    # multiple existing records (e.g. two 'Mike Barbee' files from
    # earlier passes) the first call mints a fresh record; without this
    # cache, later calls (winners list, seating) mint phantom records
    # whose files are never written, leaving dangling references.
    key = norm(name)
    if key in resolved:
        return resolved[key]
    hits = by_name.get(key, [])
    if len(hits) == 1:
        stats["people_reused"] += 1
        pid = hits[0]
    else:
        pid = new_person(name)
    resolved[key] = pid
    return pid


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


def party_for(row):
    return "Write-In" if "(Write-In)" in row["choice"] else "Nonpartisan"


# ---------- structure ----------
HDR = "# Built for issue #172 (North Carolina master tracking) from NC SBE results.\n"
jurisdictions, orgs, posts = {}, {}, {}

STATUTE_NOTE = ("N.C. General Statutes Chapter 139 (Soil and Water Conservation "
                "Districts Law), Sections 139-6 and 139-7: the district board "
                "of supervisors has five members -- three elected on a "
                "nonpartisan basis at the general election for staggered "
                "four-year terms (a class of two and a class of one, taking "
                "office the first Monday in December) and two appointed by "
                "the NC Soil and Water Conservation Commission. Only the "
                "three elected seats are modeled here.")


def ensure_district(county_raw):
    """Return (jurisdiction_id, org_id, post_id, district_slug, name)
    for the district serving this county."""
    if county_raw in ALBEMARLE:
        slug = "albemarle-soil-and-water-conservation-district"
        name = "Albemarle Soil and Water Conservation District"
        post_key = slugify(county_name(county_raw))
        post_id = f"{slug}/supervisor-{post_key}"
        post_file = f"{slug}-supervisor-{post_key}"
        post_title = (f"Soil and Water Conservation District Supervisor "
                      f"({county_name(county_raw)} County)")
    else:
        slug = f"{slugify(county_name(county_raw))}-soil-and-water-conservation-district"
        name = f"{county_name(county_raw)} Soil and Water Conservation District"
        post_id = f"{slug}/supervisor"
        post_file = f"{slug}-supervisor"
        post_title = "Soil and Water Conservation District Supervisor"
    if slug not in jurisdictions:
        jid = (f"ocd-jurisdiction/country:us/state:nc/"
               f"special_district:{slug}/government")
        srcs = [{"url": STATUTE_URL, "note": STATUTE_NOTE, "retrieved": RETR}]
        if slug.startswith("albemarle"):
            srcs.append({
                "url": "https://www.ncagr.gov/divisions/soil-water-conservation/division-districts/about-districts",
                "note": ("NC Department of Agriculture & Consumer Services, "
                         "Division of Soil and Water Conservation: North "
                         "Carolina has 96 soil and water conservation "
                         "districts; all follow county lines except the "
                         "Albemarle district, which encompasses Camden, "
                         "Chowan, Currituck, Pasquotank and Perquimans "
                         "counties and is governed by a board of 17 "
                         "supervisors (three elected in each county plus two "
                         "appointed)."),
                "retrieved": RETR})
        data = {"id": jid, "name": name, "state": "nc",
                "division_id": f"ocd-division/country:us/state:nc/special_district:{slug}",
                "classification": "government", "sources": srcs}
        dump_yaml(NC / f"jurisdictions/special-district/{slug}.yaml", data, HDR)
        jurisdictions[slug] = jid
        stats["jurisdictions"] += 1
        oid = "ocd-organization/" + str(uuid.uuid5(NS, f"org|nc|{TIER}|{slug}"))
        odata = {"id": oid, "name": name, "jurisdiction_id": jid,
                 "identifiers": [],
                 "sources": [{"url": STATUTE_URL, "note": STATUTE_NOTE,
                              "retrieved": RETR}]}
        dump_yaml(NC / f"organizations/special-district/{slug}.yaml", odata, HDR)
        orgs[slug] = oid
        stats["orgs"] += 1
    if post_id not in posts:
        pdata = {"id": post_id, "organization_id": orgs[slug],
                 "title": post_title, "seats": 3, "identifiers": [],
                 "sources": [{"url": STATUTE_URL, "note": STATUTE_NOTE,
                              "retrieved": RETR}]}
        dump_yaml(NC / f"posts/special-district/{post_file}.yaml", pdata, HDR)
        posts[post_id] = (orgs[slug], pdata)
        stats["posts"] += 1
    return jurisdictions[slug], orgs[slug], post_id


# ---------- memberships (classes sit side by side) ----------
memberships = {}
mdir = NC / "memberships/special-district"
changed_memberships = set()


def seat(post_id, oid, pid, start, note, url):
    lst = memberships.setdefault(post_id, [])
    if any(m["person_id"] == pid and "end" not in m for _, m in lst):
        return
    slug = slugify(people[pid][1]["name"])
    fname = f"{post_id.replace('/', '-')}-{slug}.yaml"
    path = NC / f"memberships/special-district/{fname}"
    n = 2
    while path.exists() or any(p == path for p, _ in lst):
        path = NC / f"memberships/special-district/{fname[:-5]}-{n}.yaml"
        n += 1
    data = {"id": path.stem, "person_id": pid, "organization_id": oid,
            "post_id": post_id, "role": "Supervisor", "start": start,
            "how_seated": "elected",
            "sources": [{"url": url, "note": note, "retrieved": RETR}]}
    lst.append((path, data))
    changed_memberships.add(path)
    stats["memberships"] += 1


# ---------- elections ----------
elections = {}


def election_file(dt):
    if dt not in elections:
        path = NC / f"elections/nc--{dt}--general.yaml"
        data = load_yaml(path)
        hdr = path.read_text().split("id: ")[0]
        elections[dt] = (path, data, hdr)
    return elections[dt]


# ---------- main ----------
DATE_OF = {"20221108": "2022-11-08", "20241105": "2024-11-05"}
for dkey, dt in DATE_OF.items():
    for key, c in sorted(SOIL[dkey].items()):
        county_raw, contest_name = key.split("|", 1)
        jid, oid, post_id = ensure_district(county_raw)
        cslug = f"{slugify(county_name(county_raw))}-soil-and-water-conservation-district-supervisor"
        cid = f"nc/{dt}/{cslug}"
        vf = int(c["vf"][0])
        rows = [r for r in c["cands"] if r["choice"] not in BUCKETS
                and re.search(r"[A-Za-z]", r["choice"])]
        rows.sort(key=lambda r: -r["total"])
        if len(rows) > vf and rows[vf]["total"] == rows[vf - 1]["total"]:
            flags.append(f"TIE at cutoff: {dt} {contest_name}")
        winners = rows[:vf]
        alb_note = ""
        if county_raw in ALBEMARLE:
            alb_note = (f" {county_name(county_raw)} County elects three "
                        f"supervisors to the shared Albemarle district board "
                        f"under G.S. 139-6 (election held in each county of "
                        f"the district).")
        note = (f"NC SBE {dt} results (Election Results series): {contest_name} -- "
                + "; ".join(f"{clean(r['choice'])} ({party_for(r)}) "
                            f"{r['total']:,}" for r in rows)
                + f". Winners are the top {vf} by total votes. The board's "
                  f"two remaining seats are appointed (G.S. 139-7) and are "
                  f"not modeled.{alb_note}")
        cand_ids = []
        for r in rows:
            nm = clean(r["choice"])
            pid = find_person(nm)
            if pid not in cand_ids:
                cand_ids.append(pid)
            add_candidacy(pid, {"contest_id": cid,
                                "election_id": f"nc/{dt}/general",
                                "jurisdiction_id": jid, "office_id": post_id,
                                "party": party_for(r),
                                "ballot_name": nm, "status": "active"})
            add_source(pid, ZIPS[dt], note)
        path_ef, ef, hdr = election_file(dt)
        if not any(x["id"] == cid for x in ef["contests"]):
            ef["contests"].append({
                "id": cid, "jurisdiction_id": jid, "office_id": post_id,
                "vote_for": vf, "candidate_ids": cand_ids,
                "result_status": "certified",
                # winners carry the person record's canonical name (CoS
                # pass precedent: 'Elaine F. Marshall', not the ballot
                # name); the ballot name lives in candidacies.ballot_name
                # and in the contest note
                "winners": [{"person_id": (pid := find_person(clean(r["choice"]))),
                             "name": people[pid][1]["name"],
                             "votes": r["total"],
                             "party": party_for(r)} for r in winners]})
            stats["contests"] += 1
        for r in winners:
            seat(post_id, oid, find_person(clean(r["choice"])),
                 f"{dt[:4]}-12", note, ZIPS[dt])

# ---------- write-out ----------
for dt, (path, ef, hdr) in elections.items():
    if not any(s.get("note", "").startswith("Soil and Water pass (issue #172)")
               for s in ef["sources"]):
        ef["sources"].append({
            "url": ZIPS[dt],
            "note": ("Soil and Water pass (issue #172): Soil and Water "
                     "Conservation District supervisor contests appended "
                     "from this same NC SBE results file."),
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
