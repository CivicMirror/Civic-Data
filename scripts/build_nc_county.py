#!/usr/bin/env python3
"""NC county pass for Civic-Data issue #172 (reconciliation pass).

Builds election records for all county-office contests in the NC SBE
2024 + 2022 general election files: Boards of Commissioners (reconciled
against the existing build_nc_counties tier), Sheriff, Clerk of Superior
Court, Register of Deeds, and Coroner (offices not previously modeled --
posts, orgs, and winner memberships created here).

'Town of ... Board of Commissioners' contests in the county files are
MUNICIPAL contests and are excluded (municipal pass). The Watauga
structure referendum is not an office contest and is excluded.

Membership reconciliation fixes applied (each sourced in the record):
- continuous-service start corrections where a holder won the same post
  in both 2022 and 2024 but the merged build kept only the 2024 start;
- ended memberships for 2022 winners displaced by the 2024 cycle whose
  service the merged build dropped (Mecklenburg at-large turnover,
  Watauga old-map districts, Buncombe District 3, and the 2022
  unexpired-term winners in Orange/Rockingham/Halifax/Union);
- memberships for 2024 unexpired-term winners, ending the departed
  incumbents' records at the successor's start (Pender, Dare,
  Pasquotank, Union);
- Watauga: Hodges and Greene corrected to appointed (Dec 2024 consent-
  order appointments under SL 2023-147, per Watauga County BOC minutes).
Two 2024 unexpired winners (Wilkes, Transylvania) are recorded as
election winners with candidacies but no membership: the at-large posts
already carry a full complement of open memberships and the departed
incumbent cannot be identified from the SBE files alone.

Party values: the schema requires a party on every candidacy. Candidates
coded UNA in the SBE file are Unaffiliated. Named write-in candidates
(the file gives them no party designation) are recorded with party
'Write-In' (Walter's ruling, 2026-10-23) -- it describes how they
appeared rather than asserting an affiliation the source does not give.
"""
import json, re, sys, uuid
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from county_map import norm_name, cslug, map_commissioner_post  # noqa: E402

TREE = Path(__file__).resolve().parent.parent
NC = TREE / "data/us/nc"
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
TODAY = "2026-10-23"
ZIP24 = "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2024_11_05/results_pct_20241105.zip"
ZIP22 = "https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2022_11_08/results_pct_20221108.zip"
ZIPS = {"2024": ZIP24, "2022": ZIP22}
START = {"2022": "2022-12-05", "2024": "2024-12-02"}
PARTY = {"DEM": "Democratic", "REP": "Republican", "LIB": "Libertarian",
         "CST": "Constitution", "GRE": "Green", "UNA": "Unaffiliated", "WTP": "We The People", "": "Unaffiliated"}

county = json.loads((Path.home() / "workspace/nc172/county.json").read_text())
plan = json.loads((Path.home() / "workspace/nc172/county_plan.json").read_text())
K_OVERRIDE = {("2022", "CLAY COUNTY BOARD OF COMMISSIONERS"): 3,
              ("2022", "UNION COUNTY BOARD OF COMMISSIONERS"): 3}

def party_for(c):
    if "(Write-In)" in c["choice"]:
        return "Write-In"
    return PARTY.get(c["party"] or "")

def slugify(name):
    s = re.sub(r"\([^)]*\)", "", name).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)

# ---------------- load existing ----------------
people = {}
for p in sorted(NC.glob("people/*/*.yaml")):
    d = yaml.safe_load(p.read_text())
    people[d["id"]] = {"name": d["name"], "path": p, "doc": d, "tier": p.parent.name}
by_norm = {}
for pid, info in people.items():
    by_norm.setdefault(norm_name(info["name"]), []).append(pid)

posts = {}
for p in sorted(NC.glob("posts/county/*.yaml")):
    d = yaml.safe_load(p.read_text())
    posts[d["id"]] = {"path": p, "doc": d}
posts_by_county = {}
for post_id in posts:
    posts_by_county.setdefault(post_id.split("/")[0], []).append(post_id)

orgs = {}
for p in sorted(NC.glob("organizations/county/*.yaml")):
    d = yaml.safe_load(p.read_text())
    orgs[d["id"]] = {"path": p, "doc": d}

memberships = {}
for p in sorted(NC.glob("memberships/county/*.yaml")):
    d = yaml.safe_load(p.read_text())
    memberships[p] = d
memb_by_post = {}
for p, d in memberships.items():
    memb_by_post.setdefault(d["post_id"], []).append((p, d))

county_jur = {}
for p in sorted(NC.glob("jurisdictions/county/*.yaml")):
    d = yaml.safe_load(p.read_text())
    county_jur[p.stem.replace("-government", "")] = d["id"]

touched_people = set()
new_people = []
reused_log = []

def get_or_mint(name, county_slug):
    hits = by_norm.get(norm_name(name), [])
    chosen = None
    for pid in hits:
        info = people[pid]
        if info["tier"] == "county":
            # prefer a person whose memberships are in this county (or none)
            mine = [d for _, d in memb_by_post_all if d["person_id"] == pid]
            if not mine or any(d["post_id"].startswith(county_slug + "/") for d in mine):
                chosen = pid
                break
    if chosen is None:
        for pid in hits:
            if len(name.split()) >= 3:  # distinctive multi-token name outside county tier
                chosen = pid
                reused_log.append((name, people[pid]["name"], "cross-tier"))
                break
    if chosen is not None:
        if people[chosen]["tier"] == "county":
            reused_log.append((name, people[chosen]["name"], "county"))
        return chosen, False
    slug = slugify(name)
    path = NC / f"people/county/{slug}.yaml"
    if path.exists() or any(people[pid]["path"] == path for pid in people):
        slug = f"{slug}-{uuid.uuid5(NS, 'collision|nc|county|' + slug + '|' + name).hex[:8]}"
        path = NC / f"people/county/{slug}.yaml"
    pid = "ocd-person/" + str(uuid.uuid5(NS, f"person|nc|county|{slug}"))
    doc = {"id": pid, "name": name, "identifiers": [], "candidacies": [],
           "verification": {"status": "unverified", "pipeline": "build_nc_county"},
           "sources": []}
    people[pid] = {"name": name, "path": path, "doc": doc, "tier": "county", "new": True}
    by_norm.setdefault(norm_name(name), []).append(pid)
    new_people.append(pid)
    return pid, True

memb_by_post_all = [(p, d) for p, d in memberships.items()]

def add_candidacy(pid, contest_id, election_id, jur_id, office_id, party, ballot_name, zip_url, note):
    doc = people[pid]["doc"]
    assert all(x["contest_id"] != contest_id for x in doc.get("candidacies", [])), (pid, contest_id)
    doc.setdefault("candidacies", []).append({
        "contest_id": contest_id, "election_id": election_id, "jurisdiction_id": jur_id,
        "office_id": office_id, **({"party": party} if party else {}),
        "ballot_name": ballot_name, "status": "active"})
    if not any(s["url"] == zip_url and note in s.get("note", "") for s in doc.get("sources", [])):
        doc.setdefault("sources", []).append({"url": zip_url, "note": note, "retrieved": TODAY})
    touched_people.add(pid)

# ---------------- membership fix machinery ----------------
fix_log = []
new_membership_files = {}

def county_org_id(county_slug):
    for oid, info in orgs.items():
        if info["doc"].get("jurisdiction_id") == county_jur[county_slug] and "Board of Commissioners" in info["doc"]["name"]:
            return oid
    raise KeyError(county_slug)

def add_membership(person_pid, post_id, start, end, how, note, zip_url, role):
    name = people[person_pid]["name"]
    post_slug = post_id.replace("/", "-")
    fn = NC / f"memberships/county/{post_slug}-{slugify(name)}.yaml"
    assert fn not in new_membership_files and not fn.exists(), fn
    doc = {"id": f"{post_slug}-{slugify(name)}", "person_id": person_pid,
           "organization_id": ORG_FOR_POST[post_id], "post_id": post_id, "role": role,
           "start": start, **({"end": end} if end else {}), "how_seated": how,
           "sources": [{"url": zip_url, "note": note, "retrieved": TODAY}]}
    new_membership_files[fn] = doc
    fix_log.append(("add-membership", post_id, name, start, end, how))
    return doc

def pretty(cn):
    s = cn.title()
    for a, b in ((" Of ", " of "), (" At-Large", " At-Large"), (" Dist ", " District ")):
        s = s.replace(a, b)
    return s

def sbe_note(yr, contest_name, winner_name, extra=""):
    zf = "results_pct_20241105.txt" if yr == "2024" else "results_pct_20221108.txt"
    return (f"North Carolina State Board of Elections, official precinct-level results file for the "
            f"{'November 5, 2024' if yr=='2024' else 'November 8, 2022'} general election ({zf}): "
            f"{winner_name} won the {pretty(contest_name)} contest. {extra}").strip()

ORG_FOR_POST = {}
for post_id, info in posts.items():
    ORG_FOR_POST[post_id] = info["doc"]["organization_id"]

# ---------------- adjudicated fixes ----------------
# winners by post for both cycles (commissioner), for start-fix detection
win_by_post = {}
for yr in ("2022", "2024"):
    for e in county[yr]:
        if e["kind"] != "commissioner" or e["contest"].startswith("TOWN OF") or " REFERENDUM" in e["contest"]:
            continue
        cs = cslug(e["county"])
        post = map_commissioner_post(posts_by_county.get(cs, []), e["contest"])
        if not post:
            continue
        K = K_OVERRIDE.get((yr, e["contest"]), plan.get(f"{yr}|{e['contest']}", {}).get("K", int(e["vote_for"])))
        cands = [c for c in e["cands"] if c["choice"] != "Write-In (Miscellaneous)"]
        win_by_post.setdefault(post, {}).setdefault(yr, []).extend(c["choice"] for c in cands[:K])

# 1. continuous-service start corrections
for post, yrs in win_by_post.items():
    if "2022" not in yrs or "2024" not in yrs:
        continue
    both = {norm_name(n) for n in yrs["2022"]} & {norm_name(n) for n in yrs["2024"]}
    for path, d in memb_by_post.get(post, []):
        nm = people[d["person_id"]]["name"]
        if norm_name(nm) in both and d.get("start") == "2024-12-02" and "end" not in d:
            d["start"] = "2022-12-05"
            d.setdefault("sources", []).append({
                "url": ZIP22, "note": "Start corrected in the #172 county reconciliation pass: SBE results show this holder also won this post in the November 8, 2022 general election, so service on the post began December 5, 2022 (the merged county build had kept only the latest cycle's start).",
                "retrieved": TODAY})
            fix_log.append(("start-fix", post, nm))

ROLE_FOR_POST = {}
for post_id, info in posts.items():
    ROLE_FOR_POST[post_id] = info["doc"]["title"]

def find_person_id(name, county_slug):
    pid, _ = get_or_mint(name, county_slug)
    return pid

# 2. ended memberships for dropped 2022 winners
ENDED_ADDS = [
    ("Patricia (Pat) Cotham", "mecklenburg/commissioner-at-large", "MECKLENBURG COUNTY BOARD OF COMMISSIONERS AT-LARGE"),
    ("Todd Castle", "watauga/commissioner-district-1", "WATAUGA COUNTY BOARD OF COMMISSIONERS DISTRICT 01"),
    ("Larry Turnbow", "watauga/commissioner-district-4", "WATAUGA COUNTY BOARD OF COMMISSIONERS DISTRICT 04"),
    ("Amanda Edwards", "buncombe/commissioner-district-3", "BUNCOMBE COUNTY BOARD OF COMMISSIONERS DISTRICT 03"),
    ("Anna Richards", "orange/commissioner-district-1", "ORANGE COUNTY BOARD OF COMMISSIONERS DISTRICT 01 (UNEXPIRED)"),
    ("Don Powell", "rockingham/commissioner-at-large", "ROCKINGHAM COUNTY BOARD OF COMMISSIONERS (UNEXPIRED)"),
    ("John Smith", "halifax/commissioner-district-2", "HALIFAX COUNTY BOARD OF COMMISSIONERS DIST 02 (UNEXPIRED)"),
    ("Brian W. Helms", "union/commissioner-at-large", "UNION COUNTY BOARD OF COMMISSIONERS"),
]
for name, post, contest_name in ENDED_ADDS:
    cs = post.split("/")[0]
    pid = find_person_id(name, cs)
    yr = "2022"
    extra = ("Unexpired-term winner; the remainder ran to the seat's next regular election, whose winner "
             "took office December 2, 2024." if "UNEXPIRED" in contest_name else
             "The merged county build carried no membership for this 2022 winner; service ended when the "
             "2024 cycle's winners took office December 2, 2024.")
    add_membership(pid, post, "2022-12-05", "2024-12-02", "elected",
                   sbe_note(yr, contest_name, name, extra), ZIP22, ROLE_FOR_POST[post])

# 3. open memberships: dropped winners + 2024 unexpired winners (with incumbent ends)
add_membership(find_person_id("Scotty Penland", "clay"), "clay/commissioner-at-large",
               "2022-12-05", None, "elected",
               sbe_note("2022", "CLAY COUNTY BOARD OF COMMISSIONERS", "Scotty Penland",
                        "Top finisher (3,519) in the vote-for-3 contest; the merged county build minted his person record but carried no membership."),
               ZIP22, ROLE_FOR_POST["clay/commissioner-at-large"])

UNEXP_OPEN = [
    ("Brad George", "pender/commissioner-district-1", "Jimmy T. Tate", "PENDER COUNTY BOARD OF COMMISSIONERS DISTRICT 01 (UNEXPIRED)"),
    ("Randy Burton", "pender/commissioner-district-2", "Wendy Fletcher-Hardee", "PENDER COUNTY BOARD OF COMMISSIONERS DISTRICT 02 (UNEXPIRED)"),
    ("Mike Burrus", "dare/commissioner-district-1", "Jim Tobin", "DARE COUNTY BOARD OF COMMISSIONERS DISTRICT 01 (UNEXPIRED)"),
    ("Clancy Baucom", "union/commissioner-at-large", None, "UNION COUNTY BOARD OF COMMISSIONERS (UNEXPIRED)"),
    ("Clifford Shaw", "pasquotank/commissioner-southern-inside", "Cecil Perry", "PASQUOTANK COUNTY COMMISSIONERS SOUTHERN INSIDE (UNEXPIRED)"),
]
for name, post, incumbent, contest_name in UNEXP_OPEN:
    cs = post.split("/")[0]
    pid = find_person_id(name, cs)
    add_membership(pid, post, "2024-12-02", None, "elected",
                   sbe_note("2024", contest_name, name,
                            "Unexpired-term winner in the November 5, 2024 general election, serving the remainder of the term."),
                   ZIP24, ROLE_FOR_POST[post])
    if incumbent:
        for path, d in memb_by_post.get(post, []):
            if people[d["person_id"]]["name"] == incumbent and "end" not in d:
                d["end"] = "2024-12-02"
                d.setdefault("sources", []).append({
                    "url": ZIP24, "note": f"End added in the #172 county reconciliation pass: this seat was filled for the unexpired remainder at the November 5, 2024 general election ({name} won); service is modeled to the successor's December 2, 2024 start.",
                    "retrieved": TODAY})
                fix_log.append(("end-fix", post, incumbent))

# 4. Watauga appointed corrections
WATAUGA_MINUTES = "https://wataugacounty.org/App_Pages/Dept/BOC/viewminutes.aspx?id=1065"
for post, nm, old_district in (("watauga/commissioner-district-1", "Tim Hodges", "Old Residency District 3"),
                               ("watauga/commissioner-district-2", "Emily Greene", "Old Residency District 1")):
    for path, d in memb_by_post.get(post, []):
        if people[d["person_id"]]["name"] == nm:
            d["how_seated"] = "appointed"
            d["start"] = "2024-12-17"
            d.setdefault("sources", []).append({
                "url": WATAUGA_MINUTES,
                "note": (f"Corrected in the #172 county reconciliation pass: Watauga County Board of Commissioners minutes, December 17, 2024 -- under Session Law 2023-147 (SB 759) and the consent order in 23-CVS-591, the seats vacated when the 2024 winners were sworn in were filled by appointment from the old residency districts; {nm} was appointed to the {old_district} seat and sworn in at that meeting. The earlier county build had recorded this appointment as a 2022 election win."),
                "retrieved": TODAY})
            fix_log.append(("appointed-fix", post, nm))

# ---------------- new officer offices ----------------
OFFICES = {
    "sheriff": ("Sheriff", "County Sheriff's Office"),
    "clerk": ("Clerk of Superior Court", "County Clerk of Superior Court"),
    "register": ("Register of Deeds", "County Register of Deeds"),
    "coroner": ("Coroner", "County Coroner"),
}
officer_posts = {}  # (county_slug, kind) -> post_id
new_org_files, new_post_files = {}, {}
for yr in ("2022", "2024"):
    for e in county[yr]:
        if e["kind"] not in OFFICES:
            continue
        cs = cslug(e["county"])
        if (cs, e["kind"]) in officer_posts:
            continue
        title, org_suffix = OFFICES[e["kind"]]
        cname = e["county"].title()
        kind_slug = {"clerk": "clerk-of-superior-court", "register": "register-of-deeds"}.get(e["kind"], e["kind"])
        org_slug = f"{cs}-{kind_slug}"
        org_id = "ocd-organization/" + str(uuid.uuid5(NS, f"org|nc|county|{org_slug}"))
        org_doc = {"id": org_id, "name": f"{cname} {org_suffix}", "jurisdiction_id": county_jur[cs],
                   "identifiers": [],
                   "sources": [{"url": ZIPS[yr], "note": f"Office established in the #172 county pass from the NC SBE {'2024' if yr=='2024' else '2022'} general election results: the {title} of {cname} County is elected by the county's voters.",
                                "retrieved": TODAY}]}
        new_org_files[NC / f"organizations/county/{org_slug}.yaml"] = org_doc
        post_id = f"{cs}/{kind_slug}"
        post_doc = {"id": post_id, "organization_id": org_id, "title": title, "seats": 1,
                    "identifiers": [],
                    "sources": [{"url": ZIPS[yr], "note": f"Post created in the #172 county pass; the office is filled at the {'November 5, 2024' if yr=='2024' else 'November 8, 2022'} general election per the NC SBE results file.",
                                 "retrieved": TODAY}]}
        post_slug = kind_slug
        new_post_files[NC / f"posts/county/{cs}-{post_slug}.yaml"] = post_doc
        officer_posts[(cs, e["kind"])] = post_id
        ORG_FOR_POST[post_id] = org_id
        ROLE_FOR_POST[post_id] = title

# ---------------- contest records ----------------
contests_by_year = {"2022": [], "2024": []}
residual = []
for yr in ("2022", "2024"):
    for e in county[yr]:
        cn = e["contest"]
        if cn.startswith("TOWN OF") or " REFERENDUM" in cn:
            continue
        cs = cslug(e["county"])
        jur_id = county_jur[cs]
        cands = [c for c in e["cands"] if c["choice"] != "Write-In (Miscellaneous)"]
        if e["kind"] == "commissioner":
            post = map_commissioner_post(posts_by_county.get(cs, []), cn)
            assert post, (yr, cn)
            K = K_OVERRIDE.get((yr, cn), plan.get(f"{yr}|{cn}", {}).get("K", int(e["vote_for"])))
            office_slug = post.split("/", 1)[1]
        else:
            post = officer_posts[(cs, e["kind"])]
            K = 1
            office_slug = post.split("/", 1)[1]
        contest_id = f"nc/{'2022-11-08' if yr=='2022' else '2024-11-05'}/{cs}-{office_slug}" + ("-unexpired" if "(UNEXPIRED)" in cn else "")
        election_id = f"nc/{'2022-11-08' if yr=='2022' else '2024-11-05'}/general"
        zf = "results_pct_20241105.txt" if yr == "2024" else "results_pct_20221108.txt"
        parts = "; ".join(f"{c['choice']} ({c['party']}) {c['total']:,}" if c["party"] else f"{c['choice']} {c['total']:,}" for c in cands)
        limited = ""
        if K != int(e["vote_for"]):
            limited = (f" The ballot instructs voters to vote for {e['vote_for']}, but {K} seats were filled "
                       f"(limited voting / seats up this cycle per the county's election method), so the top {K} finishers are the winners.")
        unexp = ""
        if "(UNEXPIRED)" in cn:
            unexp = " This is an unexpired-term contest: the winner serves the remainder of the term."
        note = (f"North Carolina State Board of Elections, official precinct-level results file for the "
                f"{'November 5, 2024' if yr=='2024' else 'November 8, 2022'} general election ({zf}), aggregated "
                f"across the county's precincts: {cn.title()} -- {parts}.{limited}{unexp}")
        cand_pids = []
        seen_pids = set()
        for c in sorted(cands, key=lambda x: " (Write-In)" in x["choice"]):
            ballot = c["choice"]
            name = ballot.replace(" (Write-In)", "")
            pid, _ = get_or_mint(name, cs)
            if pid in seen_pids:
                continue
            seen_pids.add(pid)
            add_candidacy(pid, contest_id, election_id, jur_id, post,
                          party_for(c), ballot, ZIPS[yr], note)
            cand_pids.append(pid)
        winners = []
        for i in range(K):
            w = {"person_id": cand_pids[i], "name": people[cand_pids[i]]["name"], "votes": cands[i]["total"]}
            wp = party_for(cands[i])
            if wp:
                w["party"] = wp
            winners.append(w)
        contests_by_year[yr].append({
            "id": contest_id, "jurisdiction_id": jur_id, "office_id": post,
            "vote_for": int(e["vote_for"]), "candidate_ids": cand_pids,
            "result_status": "certified", "winners": winners})
        # officer winner memberships
        if e["kind"] != "commissioner":
            w = winners[0]
            # skip if a membership already exists for this person+post (2024 clerk unexpired after a 2022 win is a new post anyway)
            exists = any(d["person_id"] == w["person_id"] for _, d in memb_by_post.get(post, [])) or \
                     any(d["person_id"] == w["person_id"] and d["post_id"] == post for d in new_membership_files.values())
            if not exists:
                add_membership(w["person_id"], post, START[yr], None, "elected",
                               sbe_note(yr, cn, w["name"]), ZIPS[yr], ROLE_FOR_POST[post])

# append contests to election files
for yr, datestr in (("2024", "2024-11-05"), ("2022", "2022-11-08")):
    efile = NC / f"elections/nc--{datestr}--general.yaml"
    edoc = yaml.safe_load(efile.read_text())
    have = {c["id"] for c in edoc["contests"]}
    add = [c for c in contests_by_year[yr] if c["id"] not in have]
    edoc["contests"].extend(add)
    if yr == "2024":
        edoc["sources"][0]["note"] = edoc["sources"][0]["note"].replace(
            "and the 14 U.S. House contests;",
            "the 14 U.S. House contests, and the county contests (commissioners, register of deeds, and two unexpired-term clerks of superior court);")
        edoc["sources"].append({
            "url": ZIP24, "note": ("County pass (issue #172): the county contests were aggregated from the same SBE file, "
                                    "reconciled against the existing county tier (built from these files by the earlier county pipeline): "
                                    "every contest's winners were checked against the seated memberships, and the divergences found -- dropped "
                                    "unexpired-term winners, two-year-term boards carrying only the latest cycle, and one county's consent-order "
                                    "appointments -- were corrected in the membership records with the corrections sourced there. Town-board "
                                    "contests that appear in the county files ('TOWN OF ... BOARD OF COMMISSIONERS') are municipal and are not recorded here."),
            "retrieved": TODAY})
    else:
        edoc["sources"][0]["note"] = edoc["sources"][0]["note"].replace(
            "This record currently carries the U.S. Senate (Class III) contest, built for the federal pass of issue #172 (the 2022 county contests join this file in the county pass);",
            "This record carries the U.S. Senate (Class III) contest (federal pass) and the 2022 county contests (county pass: commissioners, sheriffs, clerks of superior court, registers of deeds, and one coroner), all from the same SBE file;")
        edoc["sources"].append({
            "url": ZIP22, "note": ("County pass (issue #172): the county contests were aggregated from the same SBE file and reconciled "
                                    "against the existing county tier as described in the 2024 record's county-pass note."),
            "retrieved": TODAY})
    header = efile.read_text().split("id: ")[0]
    efile.write_text(header + yaml.safe_dump(edoc, sort_keys=False, allow_unicode=True, width=1000))
    print(yr, "contests added:", len(add), "| file total:", len(edoc["contests"]))

# ---------------- write people / memberships / orgs / posts ----------------
HEADER_NEW = ("# Minted from the NC State Board of Elections official general\n"
              "# election results (county pass, Civic-Data issue #172).\n")
for pid in touched_people:
    info = people[pid]
    txt = yaml.safe_dump(info["doc"], sort_keys=False, allow_unicode=True, width=1000)
    if info.get("new"):
        info["path"].write_text(HEADER_NEW + txt)
    else:
        orig = info["path"].read_text()
        i = orig.find("id: ")
        info["path"].write_text(orig[:i] + txt if i > 0 else txt)
for path, d in memberships.items():
    orig = path.read_text()
    if yaml.safe_load(orig) != d:
        i = orig.find("id: ")
        path.write_text((orig[:i] if i > 0 else "") + yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=1000))
MHDR = ("# Created in the NC county reconciliation pass (Civic-Data issue\n"
        "# #172) from NC SBE official general election results.\n")
for fn, doc in new_membership_files.items():
    fn.write_text(MHDR + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=1000))
for fn, doc in new_org_files.items():
    fn.write_text(MHDR + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=1000))
for fn, doc in new_post_files.items():
    fn.write_text(MHDR + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=1000))

print("people touched:", len(touched_people), "| new people:", len(new_people))
print("officer orgs:", len(new_org_files), "| officer posts:", len(new_post_files))
print("membership fixes:", len(fix_log))
for f in fix_log:
    print("  ", f)
print("cross-tier/county reuses:", len(reused_log))
