#!/usr/bin/env python3
"""Circuit Court reconciliation -> build plan (issue #170).
Classifies every parsed race as deciding / indecisive-primary, composes the
people table from certified ballot names, and assigns each of the 186 OJD
directory seats a disposition: BUILD membership now, or HOLD for research.
Prints the full plan for eyeball review; writes circuit_plan.json.
"""
import json, re, unicodedata
from pathlib import Path

STAGE = Path.home() / "workspace/or170"
FILES = {"2020P": "jud2020-primary.json", "2020G": "jud2020.json",
         "2022P": "jud2022-primary.json", "2022G": "jud2022.json",
         "2024P": "jud2024-primary.json", "2024G": "jud2024.json"}
CYCLE_DATE = {"2020P": "2020-05-19", "2020G": "2020-11-03", "2022P": "2022-05-17",
              "2022G": "2022-11-08", "2024P": "2024-05-21", "2024G": "2024-11-05"}
CLASS_OF = {"2020P": 2027, "2020G": 2027, "2022P": 2029, "2022G": 2029, "2024P": 2031, "2024G": 2031}
TERM_START = {2027: "2021-01-04", 2029: "2023-01-02", 2031: "2025-01-06"}

# Hand-read overrides (printed Total lines read from the abstract pages;
# the bbox parser absorbed an extra column for these three races).
OVERRIDES = {  # (cycle, seat): (winner_name_as_printed, winner_votes, misc_votes)
    ("2020P", "27-2"): ("Trevino Mari G", 6914, 80),
    ("2022P", "27-1"): ("Hill Jonathan R", 5533, 149),
    ("2024P", "25-2"): ("Chapman Jennifer K", 16259, 153),
}

JUD = {}
for cyc, fn in FILES.items():
    JUD[cyc] = json.load(open(STAGE / fn)).get("circuit", {})
    for (c, seat), (nm, wv, mv) in OVERRIDES.items():
        if c == cyc and seat in JUD[cyc]:
            for cand in JUD[cyc][seat]:
                if cand["misc"]: cand["votes"] = mv
                elif cand["winner"]: cand["votes"] = wv

RACES = json.load(open(STAGE / "circuit_races.json"))
for (c, seat), (nm, wv, mv) in OVERRIDES.items():
    for e in RACES[seat]:
        if e["cycle"] == c:
            named_total = sum(x["votes"] for x in JUD[c][seat] if not x["misc"])
            e["votes"] = wv
            e["share"] = round(100.0 * wv / (named_total + mv), 1) if named_total + mv else 0

DIRECTORY = json.load(open(STAGE / "ojd_directory.json"))

HOLD_SEATS = {  # the 16 research items (Walter: hold to the end)
    "2-14", "2-16", "2-17", "4-2", "4-6", "4-14", "4-18", "4-34",
    "5-5", "5-6", "5-12", "5-13", "11-3", "13-2", "16-6", "20-1",
}

def race_field(cyc, seat):
    return JUD[cyc].get(seat, [])

def winner_entry(cyc, seat):
    for c in race_field(cyc, seat):
        if c["winner"] and not c["misc"]:
            return c
    return None

# --- classify races: deciding vs indecisive primary ---
deciding = {}   # (seat, cycle) -> True
anomalies = []
for seat, evs in RACES.items():
    by_year = {}
    for e in evs:
        by_year.setdefault(e["cycle"][:4], []).append(e)
    for year, lst in by_year.items():
        p = next((e for e in lst if e["cycle"].endswith("P")), None)
        g = next((e for e in lst if e["cycle"].endswith("G")), None)
        if p and g:
            if p["share"] >= 50.0:
                anomalies.append(f"{seat} {year}: primary winner {p['winner']} had {p['share']}% yet a general race exists (won by {g['winner']})")
                deciding[(seat, p["cycle"])] = True
                deciding[(seat, g["cycle"])] = True
            else:
                deciding[(seat, p["cycle"])] = False
                deciding[(seat, g["cycle"])] = True
        elif p:
            if p["share"] < 50.0:
                anomalies.append(f"{seat} {year}: primary winner {p['winner']} only {p['share']}% and NO general race parsed")
            deciding[(seat, p["cycle"])] = True
        elif g:
            deciding[(seat, g["cycle"])] = True

# --- people table from deciding-race winners ---
def clean(s):
    return re.sub(r"\s+", " ", s.replace(".", "")).strip()

people = {}  # key: normalized composed name -> record
def compose(entry):
    """jud JSON entry -> (display, ballot). name is printed surname-first;
    given/surname fields are parser-derived and garble multiword surnames."""
    given, surname = entry["given"], entry["surname"]
    return clean(f"{given} {surname}"), clean(f"{given} {surname}")

for seat, evs in sorted(RACES.items()):
    for e in evs:
        if not deciding.get((seat, e["cycle"])):
            continue
        w = winner_entry(e["cycle"], seat)
        disp, ballot = compose(w)
        key = unicodedata.normalize("NFKD", disp.lower()).encode("ascii", "ignore").decode()
        rec = people.setdefault(key, {"display": disp, "ballot": ballot, "wins": [], "raw": w["name"]})
        rec["wins"].append((seat, e["cycle"]))

# directory-only holders (appointees with no deciding win)
dir_people = {}
for seat, info in DIRECTORY.items():
    if info["name"] == "VACANT":
        continue
    nm = clean(info["name"])
    key = unicodedata.normalize("NFKD", nm.lower()).encode("ascii", "ignore").decode()
    dir_people.setdefault(key, {"display": nm, "seats": []})["seats"].append(seat)

print("=== ANOMALIES ===")
for a in anomalies: print(" !", a)
print(f"\n=== PEOPLE from deciding wins: {len(people)} ===")
for key, rec in sorted(people.items()):
    wins = ", ".join(f"{s}@{c}" for s, c in rec["wins"])
    indir = "DIR" if key in dir_people else "   "
    print(f" {indir} {rec['display']:<32} raw='{rec['raw']}'  wins: {wins}")
print(f"\n=== DIRECTORY holders with NO deciding win (appointee candidates): ===")
for key, rec in sorted(dir_people.items()):
    if key not in people:
        print(f"   {rec['display']:<32} seats: {rec['seats']}")
print("\n=== SEAT DISPOSITIONS ===")
nbuild = nhold = 0
seat_plan = {}
for seat in sorted(DIRECTORY, key=lambda s: (int(s.split('-')[0]), int(s.split('-')[1]))):
    info = DIRECTORY[seat]
    evs = RACES.get(seat, [])
    dec = [(e["cycle"], e["winner"]) for e in evs if deciding.get((seat, e["cycle"]))]
    if seat in HOLD_SEATS:
        disp = "HOLD"
        nhold += 1
    elif info["name"] == "VACANT":
        disp = "HOLD(vacant-not-in-16?)"
        nhold += 1
    else:
        cls = info["term_expires"]
        match = [c for c, w in dec if CLASS_OF[c] == cls]
        disp = f"BUILD start={TERM_START[cls]} via {match}" if match else "HOLD(no class-aligned win!)"
        if match: nbuild += 1
        else: nhold += 1
    seat_plan[seat] = {"holder": info["name"], "term_expires": info["term_expires"],
                       "deciding": dec, "disposition": disp}
    print(f" {seat:>6} holder={info['name']:<28} exp={info['term_expires']}  {disp}   deciding={dec}")
print(f"\nBUILD memberships: {nbuild}  HOLD seats: {nhold}  total seats: {len(DIRECTORY)}")
json.dump({"people": people, "dir_only": {k: v for k, v in dir_people.items() if k not in people},
           "seats": seat_plan, "anomalies": anomalies, "deciding": {f"{s}|{c}": v for (s, c), v in deciding.items()}},
          open(STAGE / "circuit_plan.json", "w"), indent=1)
print("plan written to circuit_plan.json")
