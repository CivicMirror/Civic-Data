#!/usr/bin/env python3
"""Oregon Circuit Court build (issue #170): 27 judicial-district jurisdictions,
27 orgs, 186 posts (OJD directory denominator), people + candidacies for every
deciding-race winner in the six certified 2020-2024 abstracts, 200 contests
appended to the six election files, and elected memberships for the 169 seats
whose current holder's seating is fully determined by a class-aligned win.

HELD for the research step (Walter's direction, 2026-10-23): all memberships at
17 seats -- 2-14, 2-16, 2-17, 4-2, 4-6, 4-14, 4-18, 4-34, 5-5, 5-6, 5-12, 5-13,
11-3, 13-2, 16-6, 20-1, 20-14 -- covering new-judgeship appointees, departure->
appointment seats, four class contradictions, three vacancies, and one
surname-masked succession (20-14). The latest-winner-not-seated validator
warnings at 12 of those seats are the research queue, documented on #170.
"""
import json, re, unicodedata
from pathlib import Path
from uuid import uuid5, UUID

NS = UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
def uid(kind, slug): return str(uuid5(NS, f"{kind}|or|state|{slug}"))
def pid(slug): return f"ocd-person/{uid('person', slug)}"
def oid(slug): return f"ocd-organization/{uid('organization', slug)}"

REPO = Path.home() / "workspace/civic-data-or170"
STAGE = Path.home() / "workspace/or170"
ABS = {
    "2020-05-19": "https://records.sos.state.or.us/ORSOSCMSearch/Search/DocumentStream.ashx?uri=13735448",
    "2020-11-03": "https://records.sos.state.or.us/ORSOSCMSearch/Search/DocumentStream.ashx?uri=13735450",
    "2022-05-17": "https://records.sos.state.or.us/ORSOSCMSearch/Search/DocumentStream.ashx?uri=13735452",
    "2022-11-08": "https://records.sos.state.or.us/ORSOSCMSearch/Search/DocumentStream.ashx?uri=13735454",
    "2024-05-21": "https://records.sos.state.or.us/ORSOSCMSearch/Search/DocumentStream.ashx?uri=13735456",
    "2024-11-05": "https://records.sos.state.or.us/ORSOSCMSearch/Search/DocumentStream.ashx?uri=13735458",
}
ABS_NAME = {
    "2020-05-19": "Oregon Secretary of State, Abstract of Votes, May 19, 2020 Primary Election",
    "2020-11-03": "Oregon Secretary of State, Abstract of Votes, November 3, 2020 General Election",
    "2022-05-17": "Oregon Secretary of State, Abstract of Votes, May 17, 2022 Primary Election",
    "2022-11-08": "Oregon Secretary of State, Abstract of Votes, November 8, 2022 General Election",
    "2024-05-21": "Oregon Secretary of State, Abstract of Votes, May 21, 2024 Primary Election",
    "2024-11-05": "Oregon Secretary of State, Abstract of Votes, November 5, 2024 General Election",
}
CYCLE_DATE = {"2020P": "2020-05-19", "2020G": "2020-11-03", "2022P": "2022-05-17",
              "2022G": "2022-11-08", "2024P": "2024-05-21", "2024G": "2024-11-05"}
DATE_CYCLE = {v: k for k, v in CYCLE_DATE.items()}
CLASS_OF = {"2020P": 2027, "2020G": 2027, "2022P": 2029, "2022G": 2029, "2024P": 2031, "2024G": 2031}
TERM_START = {2027: "2021-01-04", 2029: "2023-01-02", 2031: "2025-01-06"}
ORS_URL = "https://www.oregonlegislature.gov/bills_laws/ors/ors003.html"
OJDD = "https://www.courts.oregon.gov/courts/pages/judges.aspx"
RET = "2026-10-23"

def yq(s): return s.replace("'", "''")
def ordn(n):
    if 10 <= n % 100 <= 20: return f"{n}th"
    return f"{n}" + {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
def clean(s): return re.sub(r"\s+", " ", s.replace(".", "")).strip()

PLAN = json.load(open(STAGE / "circuit_plan.json"))
DECIDING = {tuple(k.split("|")): v for k, v in PLAN["deciding"].items()}
DIRECTORY = json.load(open(STAGE / "ojd_directory.json"))
FILES = {"2020P": "jud2020-primary.json", "2020G": "jud2020.json", "2022P": "jud2022-primary.json",
         "2022G": "jud2022.json", "2024P": "jud2024-primary.json", "2024G": "jud2024.json"}
JUD = {c: json.load(open(STAGE / fn)).get("circuit", {}) for c, fn in FILES.items()}
OVERRIDES = {("2020P", "27-2"): 6914, ("2022P", "27-1"): 5533, ("2024P", "25-2"): 16259}
OVERRIDE_MISC = {("2020P", "27-2"): 80, ("2022P", "27-1"): 149, ("2024P", "25-2"): 153}
for (c, seat), wv in OVERRIDES.items():
    for cand in JUD[c][seat]:
        if cand["winner"]: cand["votes"] = wv
        if cand["misc"]: cand["votes"] = OVERRIDE_MISC[(c, seat)]

HOLD_SEATS = {"2-14", "2-16", "2-17", "4-2", "4-6", "4-14", "4-18", "4-34", "5-5",
              "5-6", "5-12", "5-13", "11-3", "13-2", "16-6", "20-1", "20-14"}

DISTRICTS = {  # ORS 3.010 composition
    1: "Jackson County", 2: "Lane County", 3: "Marion County", 4: "Multnomah County",
    5: "Clackamas County", 6: "Morrow and Umatilla Counties",
    7: "Gilliam, Hood River, Sherman, Wasco and Wheeler Counties", 8: "Baker County",
    9: "Malheur County", 10: "Union and Wallowa Counties", 11: "Deschutes County",
    12: "Polk County", 13: "Klamath County", 14: "Josephine County",
    15: "Coos and Curry Counties", 16: "Douglas County", 17: "Lincoln County",
    18: "Clatsop County", 19: "Columbia County", 20: "Washington County",
    21: "Benton County", 22: "Crook and Jefferson Counties", 23: "Linn County",
    24: "Grant and Harney Counties", 25: "Yamhill County", 26: "Lake County",
    27: "Tillamook County",
}

# raw printed name -> (display, ballot) fixes for winners; default = composed
NAME_FIX = {
    "Rowan Matthew A": ("Matt A Rowan", "Matthew A Rowan"),
    "Vlach-Ing Michelle": ("Michelle Vlach-Ing", "Michelle Vlach-Ing"),
    "Wolf John A": ("John A Wolf", "John A Wolf"),
    "Auxier Jeff": ("Jeffrey D Auxier", "Jeff Auxier"),
    "Bailey Jr D Charles": ("D Charles Bailey", "D Charles Bailey Jr"),
    "Rysselberghe Van Todd L": ("Todd L Van Rysselberghe", "Todd L Van Rysselberghe"),
    "von Stegge Ter Katharine": ("Katharine von Ter Stegge", "Katharine von Ter Stegge"),
    "Kittson- MaQatish Rachel": ("Rachel Kittson", "Rachel Kittson-MaQatish"),
    "Collins Jr Robert": ("Robert W Collins", "Robert Collins Jr"),
    "Torres Xiomara Y": ("Xiomara Torres", "Xiomara Y Torres"),
    "Zennache' Charles M": ("Charles M Zennaché", "Charles M Zennaché"),
    "Shirtcliff Matt": ("Matthew B Shirtcliff", "Matt Shirtcliff"),
    "Wetzel Mike": ("Michael C Wetzel", "Mike Wetzel"),
    "Raschio Rob": ("Robert S Raschio", "Rob Raschio"),
    "Brajcich Nick": ("Nickolas A Brajcich", "Nick Brajcich"),
    "McHill Tom": ("Thomas A McHill", "Tom McHill"),
    "Hart Tom": ("Thomas M Hart", "Tom Hart"),
    "Bennett Channing": ("J Channing Bennett", "Channing Bennett"),
    "Troy Francis": ("Francis G Troy", "Francis Troy"),
    "Moawad Heidi": ("Heidi H Moawad", "Heidi Moawad"),
    "Conover Robert C": ("Curtis Conover", "Robert C Conover"),
    "Hill Jonathan R": ("Jon R Hill", "Jonathan R Hill"),
    "Bloom Benjamin": ("Ben M Bloom", "Benjamin Bloom"),
    "Souede Ben N": ("Benjamin N Souede", "Ben N Souede"),
    "Long Morgan Wren": ("Morgan W Long", "Morgan Wren Long"),
    "Franco Lucero Angela M": ("Angela Franco Lucero", "Angela M Franco Lucero"),
    "Lininger Ann": ("Ann M Lininger", "Ann Lininger"),
    "Bushong Stephen K": ("Stephen Bushong", "Stephen K Bushong"),
    "Jacquot Megan L": ("Megan Jacquot", "Megan L Jacquot"),
}
FIELD_FIX = {  # losers appearing in source-note field strings
    "Berthelsen Caleb M": "Caleb M Berthelsen",
    "Carlson David L": "David L Carlson",
    "Myrick Jennifer L": "Jennifer L Myrick",
    "Rowan Matthew A": "Matthew A Rowan",
    "Vlach-Ing Michelle": "Michelle Vlach-Ing",
    "Wolf John A": "John A Wolf",
    "Auxier Jeff": "Jeff Auxier",
    "Bailey Jr D Charles": "D Charles Bailey Jr",
    "Rysselberghe Van Todd L": "Todd L Van Rysselberghe",
    "von Stegge Ter Katharine": "Katharine von Ter Stegge",
    "Kittson- MaQatish Rachel": "Rachel Kittson-MaQatish",
    "Collins Jr Robert": "Robert Collins Jr",
    "Zennache' Charles M": "Charles M Zennaché",
}
EXISTING = {  # slug -> existing person file (append candidacy, never overwrite)
    "stephen-bushong": "state/stephen-bushong.yaml",
    "megan-jacquot": "state/megan-jacquot.yaml",
    "mike-mclane": "state/mike-mclane.yaml",
}

def slugify(display):
    s = unicodedata.normalize("NFKD", display).encode("ascii", "ignore").decode().lower()
    toks = [t for t in re.split(r"[^a-z0-9]+", s) if t and len(t) > 1]
    return "-".join(toks)

def field_str(cyc, seat):
    cands = [dict(c) for c in JUD[cyc][seat]]
    named = sorted([c for c in cands if not c["misc"]], key=lambda c: -c["votes"])
    misc = next((c["votes"] for c in cands if c["misc"]), 0)
    parts = []
    for c in named:
        nm = FIELD_FIX.get(c["name"]) or clean(f"{c['given']} {c['surname']}")
        parts.append(f"{nm} {c['votes']:,}")
    return "; ".join(parts), misc

def jur_id(n): return f"ocd-jurisdiction/country:us/state:or/judicial_district:circuit-district-{n}/judiciary"
def org_slug(n): return f"or-circuit-court-district-{n}"
def post_stem(n, p): return f"or-circuit-court-district-{n}-judge-position-{p}"
def post_id(n, p): return f"or-circuit-court-district-{n}/judge-position-{p}"
def contest_id(date, n, p): return f"or/{date}/circuit-court-district-{n}-position-{p}"
def election_id(date): return f"or/{date}/{'primary' if date[5:] in ('05-19', '05-17', '05-21') else 'general'}"
def seat_np(seat):
    n, p = seat.split("-"); return int(n), int(p)

# ---------------- assemble people ----------------
# winners of deciding races: (seat, cycle) -> winner raw entry
win_races = {}   # (seat, cycle) -> raw winner dict entry
for (seat, cyc), is_dec in DECIDING.items():
    if not is_dec: continue
    w = next(c for c in JUD[cyc][seat] if c["winner"] and not c["misc"])
    win_races[(seat, cyc)] = w

people = {}  # slug -> {display, ballot_by_win: {(seat,cyc): ballot}, wins: [(seat,cyc)], dir_seats: []}
for (seat, cyc), w in sorted(win_races.items()):
    if w["name"] in NAME_FIX:
        disp, ballot = NAME_FIX[w["name"]]
    else:
        disp = ballot = clean(f"{w['given']} {w['surname']}")
    slug = slugify(disp)
    rec = people.setdefault(slug, {"display": disp, "wins": [], "ballots": {}, "dir_seats": []})
    assert rec["display"] == disp, f"slug collision with different names: {slug}: {rec['display']} vs {disp}"
    rec["wins"].append((seat, cyc))
    rec["ballots"][(seat, cyc)] = ballot

# directory-only holders (no deciding win): person file, no candidacy/membership yet
DIR_ALIAS = {  # directory display form -> winner slug (same person, name-form variant)
    "Angela F Lucero": "angela-franco-lucero",
    "Norm R Hill": "norman-hill",
    "Tim Barnack": "timothy-barnack",
    "Chris A Martin": "christine-martin",
}
win_displays = {rec["display"] for rec in people.values()}
for seat, info in DIRECTORY.items():
    if info["name"] == "VACANT": continue
    nm = clean(info["name"])
    if nm in win_displays: continue
    # name-form variants of winners (middle-initial differences etc.) resolve
    # through the seat's class-aligned winner; only true no-win holders remain:
    slug = DIR_ALIAS.get(nm) or slugify(nm)
    if slug in people: continue
    people.setdefault(slug, {"display": nm, "wins": [], "ballots": {}, "dir_seats": []})["dir_seats"].append(seat)

# ---------------- write jurisdictions / orgs / posts ----------------
created, edited = [], []
base = REPO / "data/us/or"
for sub in ["jurisdictions/judicial-district", "organizations/judicial-district",
            "posts/judicial-district", "people/judicial-district", "memberships/judicial-district"]:
    (base / sub).mkdir(parents=True, exist_ok=True)

for n in range(1, 28):
    counties = DISTRICTS[n]
    jur = f"""# Built for issue #170 (Oregon master tracking).
id: {jur_id(n)}
name: District {n} (Oregon Circuit Court)
state: or
division_id: ocd-division/country:us/state:or/judicial_district:circuit-district-{n}
classification: judiciary
sources:
- url: {ORS_URL}
  note: 'Oregon Revised Statutes, Chapter 3 (ORS 3.010 and 3.012): the {ordn(n)} judicial district comprises {counties}; its circuit court judges are elected by position to six-year terms.'
  retrieved: '{RET}'
"""
    (base / f"jurisdictions/judicial-district/circuit-district-{n}.yaml").write_text(jur)
    created.append(f"jurisdictions/judicial-district/circuit-district-{n}.yaml")
    org = f"""# Built for issue #170 (Oregon master tracking).
id: {oid(org_slug(n))}
name: Oregon Circuit Court -- District {n}
jurisdiction_id: {jur_id(n)}
identifiers: []
sources:
- url: {OJDD}
  note: 'Oregon Judicial Department, judges directory: the sitting judges of the {ordn(n)} judicial district ({counties}) are listed by position with their term expirations.'
  retrieved: '{RET}'
"""
    (base / f"organizations/judicial-district/{org_slug(n)}.yaml").write_text(org)
    created.append(f"organizations/judicial-district/{org_slug(n)}.yaml")

for seat in sorted(DIRECTORY, key=lambda s: (seat_np(s)[0], seat_np(s)[1])):
    n, p = seat_np(seat)
    info = DIRECTORY[seat]
    raced = [c for (s, c) in win_races if s == seat]
    if raced:
        latest = max(raced, key=lambda c: CYCLE_DATE[c])
        d = CYCLE_DATE[latest]
        src = f"""- url: {ABS[d]}
  note: '{yq(ABS_NAME[d])}: Judge of the Circuit Court, {n}th District, Position {p}, appears on the ballot in this election; circuit judges are elected in nonpartisan elections to six-year terms.'
  retrieved: '{RET}'"""
    else:
        src = f"""- url: {OJDD}
  note: 'Oregon Judicial Department, judges directory: a judgeship for District {n}, Position {p} is listed with a term expiring January {info["term_expires"]}; no race for this position appears in the certified 2020-2024 abstracts (a recently created judgeship, first elected in 2026).'
  retrieved: '{RET}'"""
    post = f"""# Built for issue #170 (Oregon master tracking).
id: {post_id(n, p)}
organization_id: {oid(org_slug(n))}
title: Judge, Position {p}
seats: 1
identifiers: []
sources:
{src}
- url: {ORS_URL}
  note: 'Oregon Revised Statutes 3.012: the Secretary of State designates position numbers for the circuit judgeships of each judicial district.'
  retrieved: '{RET}'
"""
    (base / f"posts/judicial-district/{post_stem(n, p)}.yaml").write_text(post)
    created.append(f"posts/judicial-district/{post_stem(n, p)}.yaml")
print(f"structure files: {len(created)}")
json.dump({"people_slugs": sorted(people)}, open(STAGE / "circuit_people_stage.json", "w"))
print(f"people records assembled: {len(people)} (existing-file merges: {[s for s in people if s in EXISTING]})")

# ---------------- people files ----------------
def person_sources(slug):
    rec = people[slug]
    out = []
    for seat, cyc in sorted(rec["wins"], key=lambda w: CYCLE_DATE[w[1]]):
        n, p = seat_np(seat)
        d = CYCLE_DATE[cyc]
        fl, misc = field_str(cyc, seat)
        note = (f"{ABS_NAME[d]}: for Judge of the Circuit Court, {ordn(n)} District, "
                f"Position {p}: {fl}; miscellaneous write-ins {misc:,}.")
        out.append((ABS[d], note))
    return out

def candidacy_block(seat, cyc, ballot):
    n, p = seat_np(seat)
    d = CYCLE_DATE[cyc]
    return [
        f"- contest_id: {contest_id(d, n, p)}",
        f"  election_id: {election_id(d)}",
        f"  jurisdiction_id: {jur_id(n)}",
        f"  office_id: {post_id(n, p)}",
        "  party: Nonpartisan",
        f"  ballot_name: {ballot}",
        "  status: active",
    ]

for slug, rec in sorted(people.items()):
    if slug in EXISTING:
        # append candidacy + source to the existing person file
        path = base / f"people/{EXISTING[slug]}"
        text = path.read_text()
        add_c, add_s = [], []
        for seat, cyc in sorted(rec["wins"], key=lambda w: CYCLE_DATE[w[1]]):
            if contest_id(CYCLE_DATE[cyc], *seat_np(seat)) in text:
                continue
            add_c += candidacy_block(seat, cyc, rec["ballots"][(seat, cyc)])
        for url, note in person_sources(slug):
            if url in text and note[:60] in text:
                continue
            add_s += [f"- url: {url}", f"  note: '{yq(note)}'", f"  retrieved: '{RET}'"]
        if add_c:
            idx = text.index("verification:")
            text = text[:idx] + "\n".join(add_c) + "\n" + text[idx:]
        if add_s:
            text = text.rstrip("\n") + "\n" + "\n".join(add_s) + "\n"
        path.write_text(text)
        edited.append(f"people/{EXISTING[slug]}")
        continue
    lines = ["# Built for issue #170 (Oregon master tracking).",
             f"id: {pid(slug)}", f"name: {rec['display']}", "identifiers: []",
             "candidacies:" if rec["wins"] else "candidacies: []"]
    for seat, cyc in sorted(rec["wins"], key=lambda w: CYCLE_DATE[w[1]]):
        lines += candidacy_block(seat, cyc, rec["ballots"][(seat, cyc)])
    lines += ["verification:", "  status: machine-extracted", f"  reviewed_on: '{RET}'",
              "  pipeline: build_or_circuit", "sources:"]
    for url, note in person_sources(slug):
        lines += [f"- url: {url}", f"  note: '{yq(note)}'", f"  retrieved: '{RET}'"]
    for seat in rec["dir_seats"]:
        n, p = seat_np(seat)
        info = DIRECTORY[seat]
        raced = [c for (s, c) in win_races if s == seat]
        if raced:
            note = (f"Oregon Judicial Department, judges directory (accessed October 23, 2026): "
                    f"{info['name']} is listed as the judge for District {n}, Position {p}, with a term "
                    f"expiring January {info['term_expires']}. The certified abstracts record a different "
                    f"winner for this position's most recent election; this holder's seating record is a "
                    f"held research item on issue #170.")
        else:
            note = (f"Oregon Judicial Department, judges directory (accessed October 23, 2026): "
                    f"{info['name']} is listed as the judge for District {n}, Position {p}, with a term "
                    f"expiring January {info['term_expires']}. No race for this position appears in the "
                    f"certified 2020-2024 abstracts; this holder's seating record is a held research item "
                    f"on issue #170.")
        lines += [f"- url: {OJDD}", f"  note: '{yq(note)}'", f"  retrieved: '{RET}'"]
    (base / f"people/judicial-district/{slug}.yaml").write_text("\n".join(lines) + "\n")
    created.append(f"people/judicial-district/{slug}.yaml")

# ---------------- memberships (BUILD seats only) ----------------
def holder_slug(seat):
    info = DIRECTORY[seat]
    cls = info["term_expires"]
    # class-aligned deciding races; if two share a class (2-11: a May primary
    # win that never seated, then a November election), the latest decides.
    cycs = [c for (s, c) in win_races if s == seat and CLASS_OF[c] == cls]
    cyc = max(cycs, key=lambda c: CYCLE_DATE[c])
    w = win_races[(seat, cyc)]
    disp = NAME_FIX[w["name"]][0] if w["name"] in NAME_FIX else clean(f"{w['given']} {w['surname']}")
    return slugify(disp), cyc, disp

mismatches = []
for seat in sorted(DIRECTORY, key=lambda s: (seat_np(s)[0], seat_np(s)[1])):
    if seat in HOLD_SEATS or DIRECTORY[seat]["name"] == "VACANT":
        continue
    n, p = seat_np(seat)
    slug, cyc, disp = holder_slug(seat)
    dname = clean(DIRECTORY[seat]["name"])
    dslug = DIR_ALIAS.get(dname) or slugify(dname)
    if dslug != slug:
        mismatches.append((seat, disp, dname))
        continue
    d = CYCLE_DATE[cyc]
    cls = DIRECTORY[seat]["term_expires"]
    start = TERM_START[cls]
    fl, misc = field_str(cyc, seat)
    if cyc.endswith("P"):
        how = (f"Won the {ABS_NAME[d].split('Abstract of Votes, ')[1]} with a majority of the "
               f"votes cast, elected outright; the term began {start}.")
    else:
        yr = cyc[:4]
        praw = JUD.get(yr + "P", {}).get(seat)
        if praw and not DECIDING.get((seat, yr + "P"), True):
            how = (f"No candidate won a majority at the May {yr} primary; won the "
                   f"{ABS_NAME[d].split('Abstract of Votes, ')[1]}; the term began {start}.")
        elif seat == "2-11":
            how = (f"Won the {ABS_NAME[d].split('Abstract of Votes, ')[1]} for the term beginning "
                   f"{start}. Lauren S Holland won the May 2022 primary for this position but did "
                   f"not take the seat; the circumstances are a held research item on issue #170.")
        else:
            how = (f"Won the {ABS_NAME[d].split('Abstract of Votes, ')[1]}; the term began {start}.")
    earlier = [(s2, c2) for (s2, c2) in win_races if s2 == seat and c2 != cyc]
    if earlier:
        es, ec = sorted(earlier, key=lambda w: CYCLE_DATE[w[1]])[-1]
        ew = win_races[(es, ec)]
        edisp = NAME_FIX[ew["name"]][0] if ew["name"] in NAME_FIX else clean(f"{ew['given']} {ew['surname']}")
        how += (f" An earlier winner at this position in the 2020-2024 abstracts, {edisp} "
                f"({CYCLE_DATE[ec]}), is recorded with a candidacy only; the succession is a "
                f"held research item on issue #170.")
    stem = f"{post_stem(n, p)}-{slug}"
    body = ["# Built for issue #170 (Oregon master tracking).",
            f"id: {stem}",
            f"person_id: {pid(slug)}",
            f"organization_id: {oid(org_slug(n))}",
            f"post_id: {post_id(n, p)}",
            "role: Judge",
            f"start: '{start}'",
            "how_seated: elected",
            "sources:",
            f"- url: {ABS[d]}",
            f"  note: '{yq(ABS_NAME[d] + ': for Judge of the Circuit Court, ' + ordn(n) + ' District, Position ' + str(p) + ': ' + fl + f'; miscellaneous write-ins {misc:,}. ' + how)}'",
            f"  retrieved: '{RET}'",
            f"- url: {OJDD}",
            f"  note: '{yq('Oregon Judicial Department, judges directory (accessed October 23, 2026): ' + DIRECTORY[seat]['name'] + f' is listed as the judge for District {n}, Position {p}, with a term expiring January {cls}.')}'",
            f"  retrieved: '{RET}'"]
    (base / f"memberships/judicial-district/{stem}.yaml").write_text("\n".join(body) + "\n")
    created.append(f"memberships/judicial-district/{stem}.yaml")
print("name mismatches (membership skipped):", mismatches)

# ---------------- elections: append deciding contests ----------------
by_date = {}
for (seat, cyc) in sorted(win_races, key=lambda w: (seat_np(w[0])[0], seat_np(w[0])[1])):
    by_date.setdefault(CYCLE_DATE[cyc], []).append(seat)
EFILE = {"2020-05-19": "or--2020-05-19--primary.yaml", "2020-11-03": "or--2020-11-03--general.yaml",
         "2022-05-17": "or--2022-05-17--primary.yaml", "2022-11-08": "or--2022-11-08--general.yaml",
         "2024-05-21": "or--2024-05-21--primary.yaml", "2024-11-05": "or--2024-11-05--general.yaml"}
ncontests = 0
for d, seats in sorted(by_date.items()):
    path = base / f"elections/{EFILE[d]}"
    text = path.read_text()
    add = ""
    for seat in seats:
        n, p = seat_np(seat)
        cid = contest_id(d, n, p)
        if cid in text: continue
        w = win_races[(seat, DATE_CYCLE[d])]
        disp = NAME_FIX[w["name"]][0] if w["name"] in NAME_FIX else clean(f"{w['given']} {w['surname']}")
        slug = slugify(disp)
        add += (f"- id: {cid}\n"
                f"  jurisdiction_id: {jur_id(n)}\n"
                f"  office_id: {post_id(n, p)}\n"
                f"  vote_for: 1\n"
                f"  candidate_ids:\n"
                f"  - {pid(slug)}\n"
                f"  result_status: certified\n"
                f"  winners:\n"
                f"  - person_id: {pid(slug)}\n"
                f"    name: {people[slug]['display']}\n")
        ncontests += 1
    if add:
        idx = text.rindex("\nsources:")
        path.write_text(text[:idx] + "\n" + add.rstrip("\n") + text[idx:] + "")
        edited.append(f"elections/{EFILE[d]}")
print(f"contests appended: {ncontests}")
print(f"TOTAL created: {len(created)}  edited: {len(edited)} {edited}")
