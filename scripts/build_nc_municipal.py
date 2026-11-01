"""Build the NC #172 municipal pass into the partial tree.

    python3 build_nc_municipal.py [--tree PATH] [--only slug,slug,...]

Data: muni_plan.json (NC SBE precinct results files, Election Results
series: 2022-11-08 and 2024-11-05 generals; 2023-10-10 / 2023-11-07 and
2025-10-07 / 2025-11-04 municipal cycles -- November generals plus the
October elections of municipalities that elect in October or use the
election-and-runoff method; see muni_plan.py for the selection rules).

Model (the repo's municipal seed convention):
- One organization per place ("<Place> Town Council", "<Place> Board of
  Commissioners", ...), file organizations/municipal/<slug>-council.yaml
  (the seed's filename even for boards).
- One MAYOR post (seats 1) and one governing-body post per place
  (<slug>/council-member | commissioner | alderman); ward / district /
  at-large structure lives in the membership `seat` label, as in the
  seed (posts/municipal/durham-council-member.yaml, seats 6, carries
  ward and at-large members alike). Post seats = seat slots observed
  across the 2022-2025 cycles (distinct qualified labels at their
  largest vote-for, plus the at-large component; when the at-large
  winner sets of two cycles are disjoint the cycles filled different
  seats and both count).
- Memberships start/end at month precision "YYYY-12": municipal terms
  turn over at the December organizational meeting after the election
  (no single statutory day, so no day is asserted). Seed memberships
  (start-less, from the CivicPatch hand-mapping) are never ended or
  re-dated from election data.
- A qualified seat (mayor, or a ward/district seat) that is on the
  ballot passes to its winner: another holder's earlier-cycle
  membership in that seat ends that December. At-large seats are a
  pool: a holder's membership ends only when the holder ran in that
  cycle's at-large contest for the post and lost -- an absent holder
  is not assumed to have left (their seat may not have been up).
- Party: coded values map as in the county pass; a named write-in
  candidate is 'Write-In' (Walter's ruling, 2026-10-23); a blank-party
  candidate in a contest with no coded candidates is 'Nonpartisan'
  (NC municipal elections are nonpartisan unless a charter provides
  otherwise); blank in a coded contest is 'Unaffiliated'.
"""
import json, re, sys, uuid
from collections import defaultdict
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TREE = HERE.parent
ONLY = None
for i, a in enumerate(sys.argv):
    if a == "--tree": TREE = Path(sys.argv[i + 1])
    if a == "--only": ONLY = set(sys.argv[i + 1].split(","))
NC = TREE / "data/us/nc"
PLAN = json.load(open(HERE / "muni_plan.json")) if (HERE / "muni_plan.json").exists() else json.load(open(Path.home() / "workspace/nc172/muni_plan.json"))
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
ZIPS = {"2022-11-08": "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2022_11_08/results_pct_20221108.zip",
        "2023-10-10": "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2023_10_10/results_pct_20231010.zip",
        "2023-11-07": "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2023_11_07/results_pct_20231107.zip",
        "2024-11-05": "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2024_11_05/results_pct_20241105.zip",
        "2025-10-07": "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2025_10_07/results_pct_20251007.zip",
        "2025-11-04": "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2025_11_04/results_pct_20251104.zip"}
RETR = "2026-10-25"
PARTY = {"DEM": "Democratic", "REP": "Republican", "LIB": "Libertarian",
         "UNA": "Unaffiliated", "GRE": "Green", "CST": "Constitution",
         "WTP": "We The People"}
SOURCES_COMMON = [{"url": "https://www.ncsbe.gov/results-data",
                   "note": "NC SBE election results data files (Election Results series).",
                   "retrieved": RETR}]


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return re.sub(r"-+", "-", s)


def clean_name(choice):
    return re.sub(r"\s+", " ", choice.replace(" (Write-In)", "")).strip()


def norm(name):
    s = re.sub(r"\([^)]*\)", "", name.lower())
    s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", s)
    return re.sub(r"\s+", " ", re.sub(r"[^a-z ]", "", s)).strip()


def dump_yaml(path, header, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(header + yaml.safe_dump(data, sort_keys=False,
                                            allow_unicode=True, width=1000))


# ---------- load current tree state ---------------------------------------
def load_all(sub):
    out = {}
    for f in (NC / sub).glob("*.yaml"):
        out[f.stem] = (f, yaml.safe_load(f.read_text()))
    return out


jur_info = {}   # slug -> {id, name, display, kind}
for f, d in load_all("jurisdictions/municipal").values():
    slug = d["id"].split("place:")[1].split("/")[0]
    name = d["name"]
    m = re.match(r"(City|Town|Village) of (.+)", name)
    jur_info[slug] = {"id": d["id"], "name": name,
                      "display": m.group(2) if m else name,
                      "kind": m.group(1) if m else "Town"}
orgs = {}       # slug -> (path, data)
for f, d in load_all("organizations/municipal").values():
    slug = d["jurisdiction_id"].split("place:")[1].split("/")[0]
    orgs[slug] = (f, d)
posts = {}      # post id -> (path, data)
for f, d in load_all("posts/municipal").values():
    posts[d["id"]] = (f, d)
people = {}     # person id -> (path, data)
people_files = {}
for tier in ("municipal", "county", "state", "federal"):
    for f, d in load_all(f"people/{tier}").values():
        people[d["id"]] = (f, d)
        people_files[d["id"]] = tier
memberships = load_all("memberships/municipal")  # stem -> (path, data)
memb_by_post = defaultdict(list)
for stem, (f, d) in memberships.items():
    memb_by_post[d["post_id"]].append((stem, d))

# person indexes. Municipal footprint: places (jurisdiction slugs) a person
# already appears in via candidacies/memberships in this tier.
footprint = defaultdict(set)
for pid, (f, d) in people.items():
    for c in d.get("candidacies", []):
        jid = c.get("jurisdiction_id", "")
        if "/place:" in jid:
            footprint[pid].add(jid.split("place:")[1].split("/")[0])
for stem, (f, d) in memberships.items():
    pid = d["person_id"]
    post = d["post_id"]
    footprint[pid].add(post.split("/")[0])

muni_by_name = defaultdict(list)
for pid, (f, d) in people.items():
    if people_files[pid] == "municipal":
        muni_by_name[norm(d["name"])].append(pid)
other_by_name = defaultdict(list)
for pid, (f, d) in people.items():
    if people_files[pid] != "municipal":
        other_by_name[norm(d["name"])].append(pid)


def find_person(name, slug):
    n = norm(name)
    for pid in muni_by_name.get(n, []):
        fp = footprint[pid]
        if not fp or slug in fp:
            return pid
    cands = [pid for pid in other_by_name.get(n, [])
             if len(n.split()) >= 3 and not (footprint[pid] - {slug})]
    if len(cands) == 1:
        return cands[0]
    return None


new_people = {}


def create_person(name):
    pslug = slugify(name)
    pid = f"ocd-person/{uuid.uuid5(NS, f'person|nc|municipal|{pslug}')}"
    if pid in people:  # slug collision between two different names
        pid = f"ocd-person/{uuid.uuid5(NS, f'person|nc|municipal|{pslug}|{norm(name)}')}"
    data = {"id": pid, "name": name, "identifiers": [], "candidacies": [],
            "verification": {"status": "unverified"}, "sources": []}
    path = NC / f"people/municipal/{pslug}.yaml"
    if path.exists():  # different UUID already on disk: reuse that file
        old = yaml.safe_load(path.read_text())
        people[old["id"]] = (path, old); people_files[old["id"]] = "municipal"
        muni_by_name[norm(old["name"])].append(old["id"])
        return old["id"]
    data["verification"] = {"status": "unverified",
                             "pipeline": "build_nc_municipal"}
    dump_yaml(path, "# Minted from the NC State Board of Elections official\n"
                    "# election results (municipal pass, Civic-Data issue #172).\n", data)
    people[pid] = (path, data); people_files[pid] = "municipal"
    new_people[pid] = name
    muni_by_name[norm(name)].append(pid)
    return pid


# ---------- place / post plan ----------------------------------------------
place_style = {}
place_bodyname = {}
for dt, contests in PLAN["elections"].items():
    for c in contests:
        if c["office"] != "body":
            continue
        cur = place_style.get(c["slug"])
        if cur is None or dt > cur[0] or (dt == cur[0] and False):
            place_style[c["slug"]] = (dt, c["style"])
        rem = c["rem"].upper()
        if "BOARD OF COMMISSIONERS" in rem:
            place_bodyname[c["slug"]] = "Board of Commissioners"
        elif "BOARD OF ALDERMEN" in rem:
            place_bodyname.setdefault(c["slug"], "Board of Aldermen")
for slug, (dt, style) in list(place_style.items()):
    if slug not in place_bodyname:
        if style == "commissioner":
            place_bodyname[slug] = "Board of Commissioners"
        elif style == "alderman":
            place_bodyname[slug] = "Board of Aldermen"
        else:
            place_bodyname[slug] = f"{jur_info[slug]['kind']} Council"

SUFFIX = {"council": "council-member", "commissioner": "commissioner",
          "alderman": "alderman"}
TITLE = {"council": "Council Member", "commissioner": "Commissioner",
         "alderman": "Alderman"}

# winners per contest (names) for the seats computation
contest_winners = {}
for dt, contests in PLAN["elections"].items():
    for idx, c in enumerate(contests):
        seen, ws = set(), []
        for cand in c["cands"]:
            nm = clean_name(cand["choice"])
            if cand["choice"] == "Write-In (Miscellaneous)" or nm in seen:
                continue
            seen.add(nm)
            ws.append((nm, cand["total"]))
        cutoff = ws[c["vote_for"] - 1][1] if len(ws) >= c["vote_for"] else 0
        contest_winners[(dt, idx)] = [nm for nm, t in ws if t >= cutoff and t > 0]

seats_calc = {}
for slug in {c["slug"] for v in PLAN["elections"].values() for c in v}:
    qual = defaultdict(int)
    atlarge = {}   # cycle -> (filled, winner names)
    for dt, contests in PLAN["elections"].items():
        for idx, c in enumerate(contests):
            if c["slug"] != slug or c["office"] != "body":
                continue
            if c["qualified"]:
                qual[c["seat"]] = max(qual[c["seat"]], c["vote_for"])
            else:
                f, names = atlarge.get(dt, (0, set()))
                atlarge[dt] = (f + len(contest_winners[(dt, idx)]),
                               names | set(contest_winners[(dt, idx)]))
    total = sum(qual.values())
    if atlarge:
        cycles = sorted(atlarge.items(), key=lambda kv: -kv[1][0])
        total += cycles[0][1][0]
        if len(cycles) > 1 and cycles[0][1][1].isdisjoint(cycles[1][1][1]):
            total += cycles[1][1][0]
    seats_calc[slug] = total

stats = defaultdict(int)
changed_people = set()
org_of = {}
post_of = {}


def ensure_org_post(slug):
    if slug in org_of:
        return org_of[slug], post_of[slug]
    disp = jur_info[slug]["display"]
    if slug in orgs:
        of, od = orgs[slug]
        org_id = od["id"]
    else:
        org_id = f"ocd-organization/{uuid.uuid5(NS, f'org|nc|{slug}-council')}"
        od = {"id": org_id, "name": f"{disp} {place_bodyname[slug]}",
              "jurisdiction_id": jur_info[slug]["id"], "identifiers": [],
              "sources": list(SOURCES_COMMON)}
        of = NC / f"organizations/municipal/{slug}-council.yaml"
        dump_yaml(of, "", od)
        orgs[slug] = (of, od)
        stats["orgs_created"] += 1
    made = {}
    for office in ("mayor", "body"):
        suffix = "mayor" if office == "mayor" else SUFFIX[place_style[slug][1]]
        post_id = f"{slug}/{suffix}"
        if post_id in posts:
            made[office] = post_id
            continue
        style = place_style[slug][1]
        pd_ = {"id": post_id, "organization_id": org_id,
               "title": "Mayor" if office == "mayor" else TITLE[style],
               "seats": 1 if office == "mayor" else max(seats_calc.get(slug, 1), 1),
               "identifiers": [], "sources": list(SOURCES_COMMON)}
        pf = NC / f"posts/municipal/{slug}-{suffix}.yaml"
        dump_yaml(pf, "", pd_)
        posts[post_id] = (pf, pd_)
        made[office] = post_id
        stats["posts_created"] += 1
    org_of[slug] = org_id
    post_of[slug] = made
    return org_id, made


def party_for(cand, contest_has_code):
    if "(Write-In)" in cand["choice"]:
        return "Write-In"
    if cand["party"]:
        return PARTY.get(cand["party"], cand["party"])
    return "Unaffiliated" if contest_has_code else "Nonpartisan"


def add_candidacy(pid, contest_id, election_id, jur_id, post_id, party, ballot):
    f, d = people[pid]
    if any(c["contest_id"] == contest_id for c in d["candidacies"]):
        return
    d["candidacies"].append(
        {"contest_id": contest_id, "election_id": election_id,
         "jurisdiction_id": jur_id, "office_id": post_id, "party": party,
         "ballot_name": ballot, "status": "active"})
    changed_people.add(pid)


def add_source(pid, url, note):
    f, d = people[pid]
    if any(s.get("url") == url and s.get("note") == note for s in d["sources"]):
        return
    d["sources"].append({"url": url, "note": note, "retrieved": RETR})
    changed_people.add(pid)


def membership_file(stem):
    return NC / f"memberships/municipal/{stem}.yaml"


def seat_membership(post_id, pid, seat, start, org_id, role, src_url, note):
    """Create (or reopen a new stint file for) a membership."""
    pslug = people[pid][1]["name"]
    base = f"{post_id.replace('/', '-')}-{slugify(pslug)}"
    stem, n = base, 1
    while stem in memberships and \
            not (memberships[stem][1]["person_id"] == pid and
                 memberships[stem][1].get("end") is None and
                 memberships[stem][1].get("seat") == seat):
        n += 1
        stem = f"{base}-{n}"
    if stem in memberships and memberships[stem][1]["person_id"] == pid:
        return stem
    data = {"id": f"{stem}-membership", "person_id": pid,
            "organization_id": org_id, "post_id": post_id, "role": role,
            "seat": seat, "how_seated": "elected", "start": start,
            "sources": [{"url": src_url, "note": note, "retrieved": RETR}]}
    memberships[stem] = (membership_file(stem), data)
    memb_by_post[post_id].append((stem, data))
    stats["memberships_created"] += 1
    return stem


def open_membership(post_id, pid, seat):
    for stem, d in memb_by_post[post_id]:
        if d["person_id"] == pid and d.get("end") is None and d.get("seat") == seat:
            return stem, d
    return None, None


def end_membership(stem, d, end, note):
    if d.get("end") is not None:
        return
    d["end"] = end
    stats["memberships_ended"] += 1


# ---------- elections --------------------------------------------------------
ELECTIONS = {"2022-11-08": ("nc/2022-11-08/general", "North Carolina 2022-11-08 general election"),
             "2023-10-10": ("nc/2023-10-10/general", "North Carolina 2023-10-10 general election"),
             "2023-11-07": ("nc/2023-11-07/general", "North Carolina 2023-11-07 general election"),
             "2024-11-05": ("nc/2024-11-05/general", "North Carolina 2024-11-05 general election"),
             "2025-10-07": ("nc/2025-10-07/general", "North Carolina 2025-10-07 general election"),
             "2025-11-04": ("nc/2025-11-04/general", "North Carolina 2025-11-04 general election")}
MUNI_NOTE = ("Municipal pass (issue #172): the municipal contests in this "
             "record (mayors and governing-body seats of NC cities, towns "
             "and villages) were aggregated from the same SBE file. "
             "Municipalities elect on different cycles and methods: most "
             "in the November odd-year generals, a set on the even-year "
             "general ballot, and a few in October (election-and-runoff "
             "method, or an October election date); September and the "
             "remaining October contests are primaries and are not "
             "recorded. School-board, sanitary-district, hospital and "
             "water-district contests and ballot questions in the file "
             "are not municipal offices and are not recorded here.")
efiles = {}
for dt, (eid, ename) in ELECTIONS.items():
    fn = f"nc--{dt}--general.yaml"
    f = NC / f"elections/{fn}"
    if f.exists():
        txt = f.read_text()
        d = yaml.safe_load(txt)
        if not any(s.get("note", "").startswith("Municipal pass (issue #172)")
                   for s in d.get("sources", [])):
            d.setdefault("sources", []).append(
                {"url": ZIPS[dt], "note": MUNI_NOTE, "retrieved": RETR})
        efiles[dt] = (f, txt.split("id: ")[0], d)
    else:
        efiles[dt] = (f, "", {"id": eid, "name": ename, "date": dt,
                              "election_type": "general", "status": "certified",
                              "contests": [],
                              "sources": [
                                  {"url": "https://www.ncsbe.gov/results-data/election-results/historical-election-results-data",
                                   "note": f"NCSBE Historical Election Results Data page: the {dt} election Results (ZIP) file is the official precinct-level results file for the election.",
                                   "retrieved": RETR},
                                  {"url": ZIPS[dt],
                                   "note": f"Direct download of the {dt} election results file used for the contest totals in this record.",
                                   "retrieved": RETR},
                                  {"url": ZIPS[dt], "note": MUNI_NOTE,
                                   "retrieved": RETR}]})

DATE_ORDER = ["2022-11-08", "2023-10-10", "2023-11-07", "2024-11-05",
              "2025-10-07", "2025-11-04"]
touched_elections = set()
contest_seen = set()
for dt in DATE_ORDER:
    eid, ename = ELECTIONS[dt]
    year = dt[:4]
    start = f"{year}-12"
    for idx, c in enumerate(PLAN["elections"].get(dt, [])):
        slug = c["slug"]
        if ONLY and slug not in ONLY:
            continue
        org_id, pmap = ensure_org_post(slug)
        post_id = pmap[c["office"]]
        disp = jur_info[slug]["display"]
        bodyname = "Mayor" if c["office"] == "mayor" else place_bodyname[slug]
        cname = f"{disp} {bodyname}"
        if c["qualified"] and c["office"] == "body":
            cname += f", {c['seat']}"
        elif c["office"] == "body":
            sib = [x for x in PLAN["elections"][dt]
                   if x["slug"] == slug and x["office"] == "body"]
            if any(x["qualified"] for x in sib):
                cname += " (At-Large)"
        if c["unexpired"]:
            cname += " (Unexpired Term)"
        suffix = "mayor" if c["office"] == "mayor" else SUFFIX[place_style[slug][1]]
        cid_part = slugify(f"{slug}-{suffix}" +
                           (f"-{c['seat']}" if c["qualified"] and c["office"] == "body" else "") +
                           ("-unexpired" if c["unexpired"] else ""))
        contest_id = f"nc/{dt}/{cid_part}"
        if contest_id in contest_seen:
            contest_id += "-2"
        contest_seen.add(contest_id)
        has_code = any(cand["party"] for cand in c["cands"]
                       if "(Write-In)" not in cand["choice"])
        seen, cand_ids, results, winners = set(), [], [], []
        _src_pending = []
        win_names = set(contest_winners[(dt, idx)])
        for cand in c["cands"]:
            if cand["choice"] == "Write-In (Miscellaneous)":
                continue
            nm = clean_name(cand["choice"])
            party = party_for(cand, has_code)
            results.append(f"{cand['choice']} ({party}) {cand['total']:,}")
            if nm in seen:
                continue
            seen.add(nm)
            pid = find_person(nm, slug) or create_person(nm)
            if pid in cand_ids:
                continue
            cand_ids.append(pid)
            _src_pending.append(pid)
            add_candidacy(pid, contest_id, eid, jur_info[slug]["id"], post_id,
                          party, nm)
            if nm in win_names and pid not in {x["person_id"] for x in winners}:
                w = {"person_id": pid, "name": people[pid][1]["name"],
                     "votes": cand["total"]}
                if party:
                    w["party"] = party
                winners.append(w)
        role = "Mayor" if c["office"] == "mayor" else TITLE[place_style[slug][1]]
        note = (f"NC SBE {dt} results (Election Results series): {cname} -- " +
                "; ".join(results) +
                f". Winners are the top {c['vote_for']} by total votes.")
        for pid in _src_pending:
            add_source(pid, ZIPS[dt], note)
        for w in winners:
            for other_post, lst in memb_by_post.items():
                if other_post == post_id:
                    continue
                if posts.get(other_post, (None, {}))[1].get("organization_id") != org_id:
                    continue
                for stem2, d2 in lst:
                    if d2["person_id"] == w["person_id"] and d2.get("end") is None \
                            and d2.get("start") is not None and d2["start"] < start:
                        end_membership(stem2, d2, start, note)
        for w in winners:
            pid = w["person_id"]
            stem, cur = open_membership(post_id, pid, c["seat"])
            if cur is None:
                seat_membership(post_id, pid, c["seat"], start, org_id, role,
                                ZIPS[dt], note)
        # seat succession within this contest
        win_pids = {w["person_id"] for w in winners}
        cand_pids = set(cand_ids)
        for stem, d in list(memb_by_post[post_id]):
            if d.get("end") is not None or d["person_id"] in win_pids:
                continue
            st = d.get("start")
            if st is None or st >= start:
                continue
            if c["qualified"] and d.get("seat") == c["seat"]:
                end_membership(stem, d, start, note)
            elif not c["qualified"] and d.get("seat") == "At-Large" \
                    and d["person_id"] in cand_pids:
                end_membership(stem, d, start, note)
        ef = efiles[dt][2]
        if not any(x["id"] == contest_id for x in ef["contests"]):
            ef["contests"].append(
                {"id": contest_id, "jurisdiction_id": jur_info[slug]["id"],
                 "office_id": post_id, "vote_for": c["vote_for"],
                 "candidate_ids": cand_ids, "result_status": "certified",
                 "winners": winners})
            touched_elections.add(dt)
        stats["contests"] += 1

# ---------- write out ---------------------------------------------------------
for dt in set(touched_elections) | {"2022-11-08", "2024-11-05"}:
    f, hdr, d = efiles[dt]
    if not hdr:
        hdr = (f"# NC SBE certified results, {dt} election (Election Results series).\n"
               "# Winners are the top vote-getters for the seats filled.\n")
    dump_yaml(f, hdr, d)
for pid in changed_people:
    f, d = people[pid]
    txt = f.read_text() if f.exists() else ""
    i = txt.find("id: ")
    hdr = txt[:i] if i > 0 else ""
    dump_yaml(f, hdr, d)
for stem, (f, d) in memberships.items():
    txt = f.read_text() if f.exists() else ""
    i = txt.find("id: ")
    hdr = txt[:i] if i > 0 else ""
    body = yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=1000)
    if txt != hdr + body:
        f.write_text(hdr + body)
print(dict(stats))
print("people touched:", len(changed_people), "| new people:", len(new_people))
