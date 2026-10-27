#!/usr/bin/env python3
"""SC municipal fan-out builder (Civic-Data issue #177).

Generalizes the Lodge worked example (build_sc_municipal_lodge.py, approved
by Walter 2026-10-26) to every municipality with contests in the SC State
Election Commission Election History (ElectionStats) per-office exports
(Town Council, City Council, Town Mayor, City Mayor), county-division rows
aggregated, input = ~/workspace/sc177/municipal_raw.json.

Scope: each town's two most recent general cycles per office family
(mayor / council), 2020-2025, general + special etypes. A follow-up date
within 45 days joins the cycle (tie-breaks, protest re-votes, runoffs).

Modeling rules (the Lodge shape, generalized):
- Winners by plurality among named candidates. The unnamed Write-In
  aggregate ranks as a pseudo-candidate: seats it would take stay
  unfilled in our record (its holder is not identifiable). A tie at the
  seat boundary leaves the tied seats unfilled unless a later contest in
  the same cycle decides them.
- Within a cycle, a later contest for the same seat class supersedes the
  earlier one for the candidates who re-contested: earlier winners who
  re-stood and lost are out; earlier winners who did not re-stand keep
  their seats.
- Council classes: if any older-cycle winner stood in the newer cycle,
  the body turned over (older class ends at the newer cycle's year);
  otherwise the classes are staggered and both stay current. Mayors are
  single-seat: an older mayoral winner ends when a newer cycle seats a
  successor. Wards and numbered seats get their own posts and their own
  class test.
- 'Unexpired Term' contests fill an existing seat: their winner joins
  the post with a membership, but they add no seats and end nobody.
- Contests with no named candidates at all are not recorded in election
  files; they are noted on the post and in the build report (held seats).
- Person identity is per-town: name variants within a town are unified
  (suffixes Jr/Sr/II/III are distinguishing and never dropped); the same
  name in a different town is a different person. An existing person
  file is never overwritten -- a slug taken by a different id gets the
  8-hex suffix form.
- Blank party in a nonpartisan contest is 'Nonpartisan'.
"""
import json, re, sys, uuid, collections
from datetime import date as ddate
from pathlib import Path
import yaml

TREE = Path(__file__).resolve().parent.parent
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
TODAY = "2026-10-26"
HIST = "https://electionhistory.scvotes.gov"
SKIP = {"Total Votes Cast", "Total Ballots Cast", "Write-In",
        "Overvotes/Undervotes", "Unknown Candidate"}
SCOPE_YEARS = {"2020", "2021", "2022", "2023", "2024", "2025"}
RAW = json.loads((Path.home() / "workspace/sc177/municipal_raw.json").read_text())
ONLY = sys.argv[1].split(",") if len(sys.argv) > 1 else None

# ---------------------------------------------------------------- scaffolds
scaffolds = {}
for f in sorted((TREE / "data/us/sc/jurisdictions/municipal").glob("*.yaml")):
    d = yaml.safe_load(f.read_text())
    scaffolds[f.stem] = {"name": d["name"], "jurisdiction_id": d["id"]}

def bare(jname):
    return re.sub(r"^(City|Town) of ", "", jname)

NAME_FIX = {"Burnet": "Burnettown", "Lake": "Lake City", "Surfside": "Surfside Beach",
            "6 Mile": "Six Mile", "96": "Ninety Six", "90 6": "Ninety Six"}

def normkey(s):
    s = NAME_FIX.get(s, s)
    s = s.lower().replace(".", "").replace("'", "")
    s = re.sub(r"^saint ", "st ", s)
    return re.sub(r"\s+", " ", s).strip()

by_key = {normkey(bare(s["name"])): slug for slug, s in scaffolds.items()}

WARD_RE = re.compile(r"^(.*?)\s*\{dt\}\s*(?:(Ward|District)\s*)?(\d+)\s*$", re.I)
WARD2_RE = re.compile(r"^(.*?)\s+(Ward|District)\s+(\d+)\s*$", re.I)
SEAT_RE = re.compile(r"^Seat (\d+)$")

def parse_ward(c):
    dn = c["district_name"]
    m = WARD_RE.match(dn)
    if m:
        word = m.group(2) or ("District" if "District" in c["district_type"] else "Ward")
        return m.group(1).strip(), (word.capitalize(), m.group(3))
    m = WARD2_RE.match(dn)
    if m:
        return m.group(1).strip(), (m.group(2).capitalize(), m.group(3))
    return dn.strip(), None

# ---------------------------------------------------------------- contests
def pdate(s):
    y, m, d = map(int, s.split("-"))
    return ddate(y, m, d)

def load_towns():
    towns = collections.defaultdict(list)
    unmatched = collections.Counter()
    for c in RAW:
        if c["etype"] not in ("General", "Special"):
            continue
        if c["date"][:4] not in SCOPE_YEARS:
            continue
        town_disp, ward = parse_ward(c)
        slug = by_key.get(normkey(town_disp))
        if not slug:
            unmatched[c["district_name"]] += 1
            continue
        named = [x for x in c["cands"] if x["name"] not in SKIP]
        wi = next((x["votes"] for x in c["cands"] if x["name"] == "Write-In"), 0)
        mod = c.get("modifier", "") or ""
        seat_m = SEAT_RE.match(mod)
        towns[slug].append({
            "contest_id": c["contest_id"], "date": c["date"], "etype": c["etype"],
            "office": c["office"], "family": "mayor" if "Mayor" in c["office"] else "council",
            "ward": ward, "seat_no": seat_m.group(1) if seat_m else None,
            "unexpired": "Unexpired" in mod,
            "term_class": mod if mod and not seat_m and "Unexpired" not in mod and mod != "At Large" else "",
            "modifier": mod, "district_raw": c["district_name"],
            "seats": c["seats"], "county": c["county"],
            "named": sorted(named, key=lambda x: -x["votes"]), "writein_votes": wi,
            "raw_cands": c["cands"],
        })
    return towns, unmatched

def cycle_groups(contests):
    groups = []
    for c in sorted(contests, key=lambda x: x["date"]):
        if groups and (pdate(c["date"]) - pdate(groups[-1][0]["date"])).days <= 45:
            groups[-1].append(c)
        else:
            groups.append([c])
    return groups

def seat_key(c):
    if c["family"] == "mayor":
        return "mayor"
    if c["ward"]:
        return f"ward:{c['ward'][0]} {c['ward'][1]}"
    if c["seat_no"]:
        return f"seat:{c['seat_no']}"
    return "at-large" + (f":{c['term_class']}" if c["term_class"] else "")

def rank_winners(c):
    """Winners among named candidates for ONE contest, the Write-In
    aggregate ranked as a pseudo-candidate. -> (winner_names, filled, flags)"""
    flags = []
    if not c["named"]:
        return [], 0, ["no-named-candidates"]
    entries = [(x["name"], x["votes"], False) for x in c["named"]]
    if c["writein_votes"] > 0:
        entries.append(("Write-In", c["writein_votes"], True))
    entries.sort(key=lambda e: -e[1])
    k = c["seats"]
    winners, filled, i = [], 0, 0
    while filled < k and i < len(entries):
        j = i
        while j < len(entries) and entries[j][1] == entries[i][1]:
            j += 1
        group = entries[i:j]
        if len(group) <= k - filled:
            for name, _, pseudo in group:
                if pseudo:
                    flags.append("writein-seat-unfilled")
                else:
                    winners.append(name)
                filled += 1
        else:
            flags.append("tie-at-cutoff")
            if any(p for _, _, p in group):
                flags.append("writein-in-tied-group")
            break
        i = j
    if len(c["named"]) < k and c["writein_votes"] == 0 and "tie-at-cutoff" not in flags:
        flags.append("short-ballot")
    return winners, filled, flags

def resolve_cycle(cycle):
    """Contests for one seat key, chronological, _pkeys attached.
    -> (winner_pkeys, seats_up, flags, per_contest)"""
    per, flags = {}, []
    cur = set()
    for c in cycle:
        w_names, filled, fl = rank_winners(c)
        w = {c["_pkeys"][n] for n in w_names}
        per[c["contest_id"]] = (w, filled)
        flags += [f"{c['contest_id']}:{f}" for f in fl]
        participants = set(c["_pkeys"].values())
        cur = {p for p in cur if p not in participants} | w
    seats_up = max([c["seats"] for c in cycle] + [len(cur)])
    return cur, seats_up, flags, per

# ---------------------------------------------------------------- people
SUFFIXES = {"jr", "sr", "ii", "iii", "iv"}
def name_tokens(name):
    s = name.lower().replace(".", "").replace(",", "")
    s = re.sub(r"[^a-z0-9\- ]", "", s)
    return [t for t in s.split() if t]

def variant_key(name):
    toks = name_tokens(name)
    if not toks:
        return ("", ""), ()
    if toks[-1] in SUFFIXES and len(toks) >= 2:
        return (toks[0], toks[-2] + " " + toks[-1]), tuple(toks[1:-2])
    return (toks[0], toks[-1]), tuple(toks[1:-1])

def slugify(name):
    s = name.lower().replace("(", "").replace(")", "").replace(".", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)

def display_of(name):
    return re.sub(r"\s+", " ", name.replace(".", "")).strip()


# Same-person ballot-name pairs the token clusterer cannot unify (nicknames,
# initial-vs-full forms, one-letter spelling variants). Each was verified
# against its contest context (same town, same seat/office across cycles)
# before being added -- see the 2026-10-26 fan-out work log.
ALIASES = {
    "abbeville": [("Benji Greeson", "Benjamin Greeson", "Benjamin Greeson")],
    "allendale": [("Portereshice Tibby Brabham", "Portershice Tibby Brabham",
                   "Portershice Tibby Brabham")],
    "duncan": [("Greg Rensberger", "Gregory Rensberger", "Gregory Rensberger")],
    "isle-of-palms": [("Josh Hooser", "Joshua Ryan Langdon Hooser",
                       "Joshua Ryan Langdon Hooser")],
    "mullins": [("M Edward Kitchen", "Malcolm E Kitchen", "Malcolm E Kitchen")],
    "pawleys-island": [("R Ashley Carter", "Robert Ashley Carter Sr",
                        "Robert Ashley Carter Sr")],
}

class Town:
    def __init__(self, slug, contests):
        self.slug = slug
        self.jname = scaffolds[slug]["name"]
        self.jurisdiction_id = scaffolds[slug]["jurisdiction_id"]
        self.kind = "City" if self.jname.startswith("City of") else "Town"
        self.contests = contests
        self.people = {}
        self.flags_split = []
        self._cluster()

    def _cluster(self):
        clusters = []
        for c in self.contests:
            for x in c["named"]:
                key, middle = variant_key(x["name"])
                hit = None
                for cl in clusters:
                    if cl["key"] == key and (not middle or not cl["middles"] or
                                             set(middle) <= cl["middles"] or cl["middles"] <= set(middle)):
                        hit = cl
                        break
                if hit is None:
                    hit = {"key": key, "middles": set(middle), "names": collections.Counter()}
                    clusters.append(hit)
                hit["middles"] |= set(middle)
                hit["names"][x["name"]] += 1
        pslug = self.slug[:-len("-government")] if self.slug.endswith("-government") else self.slug
        for a, b, canon in ALIASES.get(pslug, []):
            ca = next((cl for cl in clusters if a in cl["names"]), None)
            cb = next((cl for cl in clusters if b in cl["names"]), None)
            if ca is not None and cb is not None and ca is not cb:
                ca["names"] += cb["names"]
                ca["middles"] |= cb["middles"]
                ca["display_override"] = canon
                clusters.remove(cb)
        # split clusters whose bearer contests two seat keys in one cycle
        split_clusters = []
        for cl in clusters:
            mine = [c for c in self.contests
                    if any(n in cl["names"] for n in (x["name"] for x in c["named"]))]
            by_key = {}
            conflict = False
            for c in mine:
                k = seat_key(c)
                for (fam2, dt2, k2) in by_key:
                    if fam2 == c["family"] and k2 != k and \
                            abs((pdate(c["date"]) - pdate(dt2)).days) <= 45:
                        conflict = True
                by_key[(c["family"], c["date"], k)] = True
            if not conflict:
                split_clusters.append(cl)
                continue
            parts = {}
            for c in mine:
                parts.setdefault(seat_key(c), collections.Counter())
                for x in c["named"]:
                    if x["name"] in cl["names"]:
                        parts[seat_key(c)][x["name"]] += 1
            for k, names in parts.items():
                sub = {"key": cl["key"], "middles": set(cl["middles"]),
                       "names": names, "only_seat_key": k}
                if "display_override" in cl:
                    sub["display_override"] = cl["display_override"]
                split_clusters.append(sub)
            self.flags_split = getattr(self, "flags_split", []) + [
                f"name split by seat key: {sorted(cl['names'])}"]
        clusters = split_clusters
        for i, cl in enumerate(clusters):
            disp = cl.get("display_override") or max(cl["names"], key=lambda n: (len(name_tokens(n)), len(n)))
            pkey = f"p{i}"
            self.people[pkey] = {"display": display_of(disp), "variants": dict(cl["names"]),
                                 "slug": slugify(display_of(disp))}
            cl["pkey"] = pkey
        for c in self.contests:
            c["_pkeys"] = {}
            for x in c["named"]:
                for cl in clusters:
                    if x["name"] in cl["names"] and \
                            cl.get("only_seat_key", seat_key(c)) == seat_key(c):
                        c["_pkeys"][x["name"]] = cl["pkey"]
                        break

# ---------------------------------------------------------------- yaml out
def q(s):
    return str(s).replace("'", "''")

HDR = ("# Minted from the SC State Election Commission Election History\n"
       "# official general election results (municipal pass, Civic-Data\n"
       "# issue #177).\n")
ELEC_SRC = ("sources:\n"
            f"- url: {HIST}/search?gf=e\n"
            "  note: 'SC State Election Commission Election History (ElectionStats): the official historical results system. Contest totals here are aggregated from the per-office Search Results CSV exports (Town Council, City Council, Town Mayor, City Mayor) using county-division rows only (the exports duplicate each vote in county and precinct rows). Write-In rows are unnamed aggregates and seat no one.'\n"
            f"  retrieved: '{TODAY}'\n")
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

def dstr(iso):
    y, m, d = map(int, iso.split("-"))
    return f"{MONTHS[m-1]} {d}, {y}"

def results_str(c):
    named = [x for x in c["raw_cands"] if x["name"] not in SKIP]
    return "; ".join(f"{x['name']} {x['votes']:,}" for x in named) or "no named candidates"

def contest_note(town, c, extra=""):
    return (f"South Carolina State Election Commission, Election History (ElectionStats) "
            f"results for the {dstr(c['date'])} general election, {town.jname} {c['office']} "
            f"contest (ElectionStats contest {c['contest_id']}), county-division rows "
            f"aggregated ({c['county']} County): {results_str(c)}.{extra}")

POST_ROOT = {"salem": "salem-sc", "springfield": "springfield-sc"}  # bare roots taken (MA)

def post_for(slug, fam, skey):
    slug = POST_ROOT.get(slug, slug)
    if fam == "mayor":
        return (f"{slug}/mayor", "Mayor", f"{slug}-mayor", "At-Large",
                f"{slug}-mayor")
    if skey.startswith("ward:"):
        word, num = skey[5:].split(" ")
        return (f"{slug}/council-member-{word.lower()}-{num}",
                f"Council Member, {word} {num}",
                f"{slug}-council-member-{word.lower()}-{num}",
                f"{word} {num}", f"{slug}-council-{word.lower()}-{num}")
    if skey.startswith("seat:"):
        num = skey[5:]
        return (f"{slug}/council-member-seat-{num}", f"Council Member, Seat {num}",
                f"{slug}-council-member-seat-{num}", f"Seat {num}",
                f"{slug}-council-seat-{num}")
    return (f"{slug}/council-member", "Council Member", f"{slug}-council-member",
            "At-Large", f"{slug}-council")

# ---------------------------------------------------------------- main build
def main():
    towns_raw, unmatched = load_towns()
    print("unmatched:", dict(unmatched))
    report = {"towns": {}, "held_towns": [], "unmatched": dict(unmatched)}
    used_slugs = {}
    for p in (TREE / "data/us/sc/people").rglob("*.yaml"):
        try:
            used_slugs[p.stem] = yaml.safe_load(p.read_text()).get("id")
        except Exception:
            used_slugs[p.stem] = None

    claimed_slugs = set()
    org_dir = TREE / "data/us/sc/organizations/municipal"
    post_dir = TREE / "data/us/sc/posts/municipal"
    ppl_dir = TREE / "data/us/sc/people/municipal"
    mem_dir = TREE / "data/us/sc/memberships/municipal"
    for d in (org_dir, post_dir, ppl_dir, mem_dir):
        d.mkdir(parents=True, exist_ok=True)

    election_contests = collections.defaultdict(list)  # date -> [(seg, block)]

    for slug in sorted(towns_raw):
        if ONLY and slug not in ONLY:
            continue
        town = Town(slug, towns_raw[slug])
        pslug = slug[:-len("-government")] if slug.endswith("-government") else slug
        jname, kind = town.jname, town.kind
        place = bare(jname)
        JUR = town.jurisdiction_id
        org_id = "ocd-organization/" + str(uuid.uuid5(NS, f"organization|sc|municipal|{pslug}"))
        trep = {"families": {}, "flags": list(town.flags_split)}

        for pkey, person in town.people.items():
            base = person["slug"]
            pid = "ocd-person/" + str(uuid.uuid5(NS, f"person|sc|municipal|{base}"))
            fslug = base
            if base in claimed_slugs or (base in used_slugs and used_slugs[base] != pid):
                pid = "ocd-person/" + str(uuid.uuid5(NS, f"person|sc|municipal|{base}|{pslug}"))
                fslug = f"{base}-{str(uuid.uuid5(NS, f'person|sc|municipal|{base}|{slug}'))[:8]}"
                trep["flags"].append(f"person slug collision: {base} -> {fslug}")
            person["pid"], person["fslug"] = pid, fslug
            used_slugs[fslug] = pid
            claimed_slugs.add(base)
            claimed_slugs.add(fslug)

        # plan: (family, seat_key) -> cycles/unexpired
        by_key_map = collections.defaultdict(list)
        for c in town.contests:
            by_key_map[(c["family"], seat_key(c))].append(c)
        plan = {}
        for (fam, skey), cs in by_key_map.items():
            reg = [c for c in cs if not c["unexpired"]]
            unx = [c for c in cs if c["unexpired"]]
            groups = cycle_groups(reg)
            kept_groups = groups[-2:]
            kept = [c for g in kept_groups for c in g]
            if kept:
                unx_kept = [c for c in unx if c["date"] >= kept[0]["date"]]
            else:
                unx_kept = unx[-1:]
            plan[(fam, skey)] = {"cycles": kept_groups, "kept": kept, "unexpired": unx_kept}

        # posts aggregated by post_id (term-class keys share the at-large post)
        posts = {}
        mem_raw = []       # (pkey, post_id, start, end, dec_contest, kindflag)
        elec_blocks = []   # (date, seg, contest, winner_pkeys, status, post_id)
        held_notes = collections.defaultdict(list)

        for (fam, skey), pl in sorted(plan.items()):
            post_id, title, pfname, seat_label, segbase = post_for(pslug, fam, skey)
            cycles_out = []
            for g in pl["cycles"]:
                w, up, fl, per = resolve_cycle(g)
                cycles_out.append((g, w, up, per))
                trep["flags"] += [f"{skey} {f}" for f in fl]
                for c in g:
                    if not c["named"]:
                        held_notes[post_id].append(c)
            turnover = False
            if skey.startswith(("ward:", "seat:")):
                turnover = len(cycles_out) == 2  # single-seat post: newer cycle replaces
            elif len(cycles_out) == 2:
                new_parts = set()
                for c in cycles_out[1][0]:
                    new_parts |= set(c["_pkeys"].values())
                turnover = bool(cycles_out[0][1] & new_parts)
            last_yr = cycles_out[-1][0][0]["date"][:4] if cycles_out else None
            for idx, (g, w, up, per) in enumerate(cycles_out):
                yr = g[0]["date"][:4]
                is_last = idx == len(cycles_out) - 1
                for pkey in w:
                    end = None
                    if not is_last and (turnover or fam == "mayor"):
                        end = last_yr
                    dec = None
                    for c in g:
                        if pkey in per[c["contest_id"]][0]:
                            dec = c
                    mem_raw.append((pkey, post_id, yr, end, dec, ""))
            unx_groups = collections.defaultdict(list)
            for c in pl["unexpired"]:
                unx_groups[c["modifier"]].append(c)
            for mod, ucs in sorted(unx_groups.items()):
                for g in cycle_groups(ucs):
                    w, up, fl, per = resolve_cycle(g)
                    trep["flags"] += [f"{skey} {f}" for f in fl]
                    mm = re.search(r"(\d+) Month", mod)
                    for pkey in w:
                        dec = None
                        for c in g:
                            if pkey in per[c["contest_id"]][0]:
                                dec = c
                        end = None
                        if mm:
                            end = str(int(dec["date"][:4]) + round(int(mm.group(1)) / 12))
                        mem_raw.append((pkey, post_id, dec["date"][:4], end, dec, "unexpired"))
                    for c in g:
                        if c["named"]:
                            cw, _ = per[c["contest_id"]]
                            elec_blocks.append((c["date"], segbase + "-" + slugify(mod), c, cw,
                                                "certified" if cw else "official", post_id))
            # seats contribution of this seat key
            if fam == "mayor":
                contrib = 1
            elif skey.startswith(("ward:", "seat:")):
                contrib = max([up for _, _, up, _ in cycles_out] +
                              [c["seats"] for c in pl["unexpired"]] + [1])
            else:
                ups = [up for _, _, up, _ in cycles_out]
                if not ups:
                    contrib = max([c["seats"] for c in pl["unexpired"]] + [1])
                elif turnover or len(ups) == 1:
                    contrib = ups[-1]
                else:
                    contrib = sum(ups)
            if post_id in posts:
                posts[post_id]["seats"] += contrib
                posts[post_id]["cycles"] += cycles_out
                posts[post_id]["first_contest"] = min(
                    posts[post_id]["first_contest"], pl["kept"][0] if pl["kept"] else pl["unexpired"][0],
                    key=lambda c: c["date"])
            else:
                posts[post_id] = {"file": pfname, "title": title, "seats": contrib,
                                  "label": seat_label, "fam": fam, "cycles": cycles_out,
                                  "first_contest": (pl["kept"] or pl["unexpired"])[0]}
            trep["families"][skey] = {"turnover": turnover, "seats_contrib": contrib,
                                      "cycles": [[c["contest_id"] for c in g] for g, *_ in cycles_out]}
            for g, w, up, per in cycles_out:
                for c in g:
                    if not c["named"]:
                        continue
                    cw, _ = per[c["contest_id"]]
                    seg = segbase + (("-" + slugify(c["term_class"])) if c["term_class"] else "")
                    elec_blocks.append((c["date"], seg, c, cw,
                                        "certified" if cw else "official", post_id))

        if not any(c["named"] for c in town.contests):
            report["held_towns"].append(slug)
            continue

        # merge memberships per (person, post): earliest start; open if any
        # entry is open; deciding contest = latest entry's contest
        merged = {}
        for (pkey, post_id, start, end, dec, kindflag) in mem_raw:
            key = (pkey, post_id)
            if key not in merged:
                merged[key] = {"start": start, "end": end, "dec": dec, "kind": kindflag}
            else:
                m = merged[key]
                m["start"] = min(m["start"], start)
                if end is None:
                    m["end"] = None
                if dec["date"] >= m["dec"]["date"]:
                    m["dec"] = dec
                    if kindflag:
                        m["kind"] = kindflag
        memberships = [(pk, po, m["start"], m["end"], m["dec"], m["kind"])
                       for (pk, po), m in merged.items()]
        by_person = collections.defaultdict(list)
        for i, m in enumerate(memberships):
            by_person[m[0]].append(i)
        for pk, idxs in by_person.items():
            open_idxs = [i for i in idxs if memberships[i][3] is None]
            posts_seen = {memberships[i][1] for i in open_idxs}
            if len(open_idxs) > 1 and len(posts_seen) > 1:
                def rank(i):
                    dec = memberships[i][4]
                    return (dec["date"], 1 if dec["family"] == "mayor" else 0)
                open_sorted = sorted(open_idxs, key=rank)
                win = open_sorted[-1]
                if rank(open_sorted[-2]) != rank(win):
                    for i in open_sorted[:-1]:
                        pk2, po2, st2, _e, dec2, k2 = memberships[i]
                        memberships[i] = (pk2, po2, st2, memberships[win][4]["date"][:4], dec2, k2)
                        trep["flags"].append(
                            f"progression: {po2} ended {memberships[win][4]['date'][:4]} (later win: {memberships[win][1]})")

        # ---- organization
        all_dates = sorted({c["date"] for c in town.contests})
        org_note = (f"{jname} governing body, built from the SC State Election Commission "
                    f"Election History results for the {', '.join(dstr(d) for d in all_dates)} "
                    f"general elections (mayor and council contests) in the ElectionStats "
                    f"per-office exports, county-division rows aggregated.")
        first_c = min(town.contests, key=lambda c: c["date"])
        org = [HDR, f"id: {org_id}", f"name: {place} {kind} Council",
               f"jurisdiction_id: {JUR}", "identifiers: []", "sources:",
               f"- url: {HIST}/contest/{first_c['contest_id']}",
               f"  note: '{q(org_note)}'", f"  retrieved: '{TODAY}'", ""]
        (org_dir / f"{pslug}-council.yaml").write_text("\n".join(org))

        # ---- posts
        for post_id, P in posts.items():
            cyc_desc = []
            for g, w, up, per in P["cycles"]:
                cyc_desc.append(f"{dstr(g[0]['date'])} (ElectionStats contests "
                                f"{', '.join(c['contest_id'] for c in g)}): {up} seat(s) up")
            note = (f"{P['title']} of {place}, elected "
                    + ("town-wide." if P["fam"] == "mayor" or P["label"] == "At-Large"
                       else f"from {P['label']}.")
                    + " Contests in scope: " + "; ".join(cyc_desc) + ".")
            for c in held_notes.get(post_id, []):
                note += (f" The {dstr(c['date'])} contest (ElectionStats contest "
                         f"{c['contest_id']}) lists no named candidates -- write-in votes "
                         f"only ({c['writein_votes']}) -- so that seat's holder is not "
                         f"identifiable from the state system and is not recorded.")
            lines = [HDR, f"id: {post_id}", f"organization_id: {org_id}",
                     f"title: {P['title']}", f"seats: {P['seats']}", "identifiers: []",
                     "sources:", f"- url: {HIST}/contest/{P['first_contest']['contest_id']}",
                     f"  note: '{q(note)}'", f"  retrieved: '{TODAY}'", ""]
            (post_dir / f"{P['file']}.yaml").write_text("\n".join(lines))

        # ---- people
        person_cands = collections.defaultdict(list)
        for (date, seg, c, cw, status, post_id) in elec_blocks:
            for x in c["named"]:
                person_cands[c["_pkeys"][x["name"]]].append((c, post_id, x["name"], seg))
        for pkey, clist in person_cands.items():
            person = town.people[pkey]
            lines = [HDR, f"id: {person['pid']}", f"name: {person['display']}",
                     "identifiers: []", "candidacies:"]
            srcs = []
            for c, post_id, ballot, seg in sorted(clist, key=lambda t: t[0]["date"]):
                party = next(x["party"] for x in c["named"] if x["name"] == ballot) or "Nonpartisan"
                lines += [f"- contest_id: sc/{c['date']}/{seg}",
                          f"  election_id: sc/{c['date']}/general",
                          f"  jurisdiction_id: {JUR}",
                          f"  office_id: {post_id}",
                          f"  party: {party}",
                          f"  ballot_name: '{q(ballot)}'",
                          "  status: active"]
                srcs.append(c)
            lines += ["verification:", "  status: unverified",
                      "  pipeline: build_sc_municipal", "sources:"]
            for c in srcs:
                lines += [f"- url: {HIST}/contest/{c['contest_id']}",
                          f"  note: '{q(contest_note(town, c))}'",
                          f"  retrieved: '{TODAY}'"]
            lines.append("")
            (ppl_dir / f"{person['fslug']}.yaml").write_text("\n".join(lines))

        # ---- memberships
        for (pkey, post_id, start, end, dec, kindflag) in memberships:
            person = town.people[pkey]
            P = posts[post_id]
            fname = f"{P['file']}-{person['fslug']}"
            extra = ""
            if kindflag == "unexpired":
                extra = (f" Elected to an unexpired term (ElectionStats modifier "
                         f"'{dec['modifier']}').")
            lines = [HDR, f"id: {fname}", f"person_id: {person['pid']}",
                     f"organization_id: {org_id}", f"post_id: {post_id}",
                     f"role: {P['title']}", f"seat: {P['label']}", f"start: '{start}'"]
            if end:
                lines.append(f"end: '{end}'")
            lines += ["how_seated: elected", "sources:",
                      f"- url: {HIST}/contest/{dec['contest_id']}",
                      f"  note: '{q(contest_note(town, dec, extra))}'",
                      f"  retrieved: '{TODAY}'", ""]
            (mem_dir / f"{fname}.yaml").write_text("\n".join(lines))

        # ---- election blocks
        for (date, seg, c, cw, status, post_id) in elec_blocks:
            lines = [f"- id: sc/{date}/{seg}", f"  jurisdiction_id: {JUR}",
                     f"  office_id: {post_id}", f"  vote_for: {c['seats']}",
                     "  candidate_ids:"]
            lines += [f"  - {town.people[c['_pkeys'][x['name']]]['pid']}" for x in c["named"]]
            lines.append(f"  result_status: {status}")
            if cw:
                lines.append("  winners:")
                for x in c["named"]:
                    pk = c["_pkeys"][x["name"]]
                    if pk in cw:
                        lines += [f"  - person_id: {town.people[pk]['pid']}",
                                  f"    name: '{q(town.people[pk]['display'])}'",
                                  f"    party: {x['party'] or 'Nonpartisan'}",
                                  f"    votes: {x['votes']}"]
            else:
                lines.append("  winners: []")
            election_contests[date].append((seg, "\n".join(lines)))
        report["towns"][slug] = trep

    # ---- election files
    elec_dir = TREE / "data/us/sc/elections"
    for date, blocks in sorted(election_contests.items()):
        path = elec_dir / f"sc--{date}--general.yaml"
        blocks_sorted = [b for _, b in sorted(blocks, key=lambda t: t[0])]
        if path.exists():
            text = path.read_text()
            have = set(re.findall(r"^- id: sc/[^/]+/(\S+)$", text, re.M))
            blocks_sorted = [b for s2, b in sorted(blocks, key=lambda t: t[0]) if s2 not in have]
            if not blocks_sorted:
                continue
            idx = text.rfind("\nsources:")
            assert idx > 0, f"no trailing sources block in {path}"
            path.write_text(text[:idx] + "\n" + "\n".join(blocks_sorted) + text[idx:] +
                            ("" if text.endswith("\n") else "\n"))
        else:
            hdr = ("# Built from the SC State Election Commission Election History\n"
                   "# (ElectionStats) official results, per-office CSV exports aggregated\n"
                   "# from county-division rows. Municipal pass (Civic-Data issue #177).\n")
            lines = [hdr, f"id: sc/{date}/general",
                     f"name: South Carolina {date} general election",
                     f"date: '{date}'", "election_type: general", "status: certified",
                     "contests:"] + blocks_sorted + [ELEC_SRC]
            path.write_text("\n".join(lines) + "\n")

    out = Path.home() / "workspace/sc177/municipal_build_report.json"
    out.write_text(json.dumps(report, indent=1))
    print(f"towns built: {len(report['towns'])} | held: {report['held_towns']}")
    flagged = {s: t["flags"] for s, t in report["towns"].items() if t["flags"]}
    print(f"towns with flags: {len(flagged)}")
    for s, fl in sorted(flagged.items()):
        print(" ", s, "->", "; ".join(fl[:8]))

if __name__ == "__main__":
    main()
