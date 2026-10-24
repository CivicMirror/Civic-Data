#!/usr/bin/env python3
"""Build the Oregon legislative tier for issue #170 (step 3 of the build order).

90 district jurisdictions + organizations + posts; holders from the certified
SOS Abstracts of Votes (2024: all 60 House districts + 15 Senate districts;
2022: the other 15 Senate districts, plus the District 18 two-year-term
contest created by redistricting). Winners were reconciled against the 83rd
Legislative Assembly roster; seven seats changed hands mid-term by appointment
and are modeled as an ended elected membership + an appointed membership:

  SD13 Woods (d. 2025-04-19) -> Courtney Neron Misslin (appt 2025-05-07)
  SD17 Steiner (res. 2024-11-06, elected Treasurer) -> Lisa Reynolds (appt, sworn 2024-12-09)
  SD26 Bonham (res. 2025-10-05) -> Christine Drazan (appt 2025-10-23)
  HD26 Neron Misslin (res. 2025-05-09, to Senate) -> Sue Rieke Smith (appt 2025-06-06, sworn 2025-06-09)
  HD34 Reynolds won in 2024 but resigned 2024-11-15 before the term began
       (CA AD32/Fong precedent: candidacy recorded, no membership) ->
       Mari Watanabe (appt 2025-01-15)
  HD48 Hoa Nguyen (d. 2025-10-09) -> Lamar Wise (appt 2025-11-05)
  HD51 Drazan (res. 2025-10-23, to Senate) -> Matt Bunch (appt 2025-11-17)

Extraction: parse_legislative2.py over pdftotext -bbox output of the two
abstract PDFs; every district's county rows were summed and cross-checked
against the printed totals (zero mismatches). Six blocks whose header layout
defeated the column clusterer were hand-verified against the printed pages
and are overridden below.
"""
import json, sys, uuid
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent / "civic-data-or170"
DRY = "--write" not in sys.argv
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
def uid(kind, key): return str(uuid.uuid5(NS, f"{kind}|{key}"))
A2024 = "https://records.sos.state.or.us/ORSOSCMSearch/Search/DocumentStream.ashx?uri=13735458"
A2022 = "https://records.sos.state.or.us/ORSOSCMSearch/Search/DocumentStream.ashx?uri=13735454"
PARTYNAME = {"D": "Democratic", "R": "Republican", "L": "Libertarian", "I": "Independent",
             "PG": "Pacific Green", "P": "Progressive", "WF": "Working Families",
             "C": "Constitution", "NAV": "Nonaffiliated", "NA": "Nonaffiliated", "WTP": "We The People"}

d24 = json.load(open(Path(__file__).parent / "leg2024.json"))
d22 = json.load(open(Path(__file__).parent / "leg2022senate.json"))

def C(given, surname, party, votes, winner=False):
    return {"given": given, "surname": surname, "party": party, "votes": votes, "winner": winner, "misc": False}
def MISC(votes): return {"given": "", "surname": "", "party": None, "votes": votes, "winner": False, "misc": True}

# Hand-verified blocks (printed pages read directly; see module docstring).
OVERRIDE = {
    ("house", 15): [C("Terrence", "Virnig", "D", 15566), C("Shelly", "Boshart Davis", "R", 22197, True), MISC(43)],
    ("house", 34): [C("John", "Verbeek", "R", 8973), C("Lisa", "Reynolds", "D", 22572, True), MISC(44)],
    ("house", 46): [C("John Mark", "Alexander", "R", 4414), C("Kevin", "Levy", "I", 1252), C("Willy", "Chotzen", "D", 25542, True), C("Austin", "Daniel", "L", 1040), MISC(58)],
    ("house", 48): [C("Hoa H", "Nguyen", "D", 14451, True), C("John", "Masterman", "R", 12773), MISC(69)],
    ("senate22", 8): [C("Sara", "Gelser Blouin", "D", 37815, True), C("Valerie", "Draper Woldeit", "R", 25375), MISC(97)],
    ("senate22", 17): [C("John", "Verbeek", "R", 12377), C("Elizabeth", "Steiner Hayward", "D", 46647, True), MISC(86)],
}

def parsed(chamber, dist, src):
    out = []
    for c in src[chamber][str(dist)]:
        party = c["party"]
        if party == "Mrk": party = "D"  # HD9: 'William (Mrk) Mrkvicka' -- nickname in parens, party (D)
        out.append({"given": c["given"], "surname": c["surname"], "party": party,
                    "votes": c["votes"], "winner": c["winner"], "misc": c["misc"]})
    return out

def ballot(c): return (c["given"] + " " + c["surname"]).strip()

DISPLAY = {  # ballot name -> person display name (middle initials dropped unless used)
    "Elizabeth Steiner Hayward": "Elizabeth Steiner",
    "Fred Frank Girod": "Fred Girod",
    "James I Manning Jr": "James Manning Jr.",
    "Lesly M Munoz": "Lesly Muñoz",
    "Courtney Neron": "Courtney Neron Misslin",
    "E Werner Reschke": "E. Werner Reschke",
    "Bruce W Starr": "Bruce Starr", "Cedric R Hayden": "Cedric Hayden",
    "Daniel G Bonham": "Daniel Bonham", "Wlnsvey E Campos": "Wlnsvey Campos",
    "Virgle J Osborne": "Virgle Osborne", "Kevin L Mannix": "Kevin Mannix",
    "Anna M Scharf": "Anna Scharf", "Lucetta A Elmer": "Lucetta Elmer",
    "Cyrus B Javadi": "Cyrus Javadi", "Mark F Gamba": "Mark Gamba",
    "Emily G McIntire": "Emily McIntire", "Hoa H Nguyen": "Hoa Nguyen",
}
def display(bname): return DISPLAY.get(bname, bname)
def slugify(name):
    s = name.lower().replace("ñ", "n").replace("ú", "u")
    s = "".join(ch if ch.isalnum() else "-" for ch in s)
    return "-".join(x for x in s.split("-") if x)

SENATE_2024 = {1, 2, 5, 9, 12, 14, 18, 21, 22, 23, 25, 27, 28, 29, 30}
# district -> (winner membership end, successor dict or None, extra note)
SUCCESSION = {
    ("senate", 13): ("2025-04-19", dict(name="Courtney Neron Misslin", party="Democratic", start="2025-05-07",
        note="Aaron Woods died in office on April 19, 2025. Courtney Neron Misslin, then the District 26 state representative, was appointed by the Clackamas, Washington and Yamhill county commissions on May 7, 2025, and serves the remainder of the term.",
        src=("https://gowestassociation.org/2025/05/12/oregon-capitol-update/", "GoWest Association, Oregon Capitol Update (May 12, 2025): county commissioners appointed Representative Courtney Neron to the Oregon State Senate following the passing of Senator Aaron Woods; Washington County's Board of Commissioners notice records the appointment meeting on May 7, 2025."))),
    ("senate", 17): ("2024-11-06", dict(name="Lisa Reynolds", party="Democratic", start="2024-12-09",
        note="Elizabeth Steiner resigned the seat on November 6, 2024, after her election as State Treasurer. Lisa Reynolds was appointed by the Multnomah and Washington county commissions on November 14, 2024, and was sworn in on December 9, 2024; she serves the remainder of the term.",
        src=("https://www.oregonlegislature.gov/senatedemocrats/Documents/Senator%20Lisa%20Reynolds%20Takes%20the%20Oath%20of%20Office.pdf", "Oregon State Senate Democratic Caucus (oregonlegislature.gov), 'Senator Lisa Reynolds Takes the Oath of Office' (December 9, 2024): Reynolds, appointed to succeed Treasurer-elect Elizabeth Steiner, was sworn in as the Senator for District 17."))),
    ("senate", 26): ("2025-10-05", dict(name="Christine Drazan", party="Republican", start="2025-10-23",
        note="Daniel Bonham resigned effective October 5, 2025. Christine Drazan, then the District 51 state representative and House Republican leader, was appointed by the Clackamas, Multnomah, Hood River and Wasco county commissions on October 23, 2025, and serves the remainder of the term.",
        src=("https://www.opb.org/article/2025/10/23/republican-christine-drazan-appointed-oregon-senate/", "Oregon Public Broadcasting (October 23, 2025): commissioners from Clackamas, Multnomah, Wasco and Hood River counties appointed Christine Drazan to the Oregon Senate seat vacated by Daniel Bonham's resignation."))),
    ("house", 26): ("2025-05-09", dict(name="Sue Rieke Smith", party="Democratic", start="2025-06-09",
        note="Courtney Neron Misslin resigned on May 9, 2025, after her appointment to the State Senate. Sue Rieke Smith was appointed by the Clackamas, Washington and Yamhill county commissions on June 6, 2025, and was sworn in on June 9, 2025; she serves the remainder of the term.",
        src=("https://www.washingtoncountyor.gov/bcc/news/2025/06/06/sue-rieke-smith-appointed-fill-vacancy-oregon-house-district-26", "Washington County Board of Commissioners media release (June 6, 2025): the Washington, Clackamas and Yamhill boards held a joint session on June 6 to appoint Sue Rieke Smith to fill the vacant House District 26 seat."))),
    ("house", 48): ("2025-10-09", dict(name="Lamar Wise", party="Democratic", start="2025-11-05",
        note="Hoa Nguyen died in office on October 9, 2025. Lamar Wise was appointed by the Multnomah and Clackamas county commissions on November 5, 2025, and serves the remainder of the term.",
        src=("https://multco.us/news/news-release-multnomah-and-clackamas-county-commissioners-appoint-lamar-wise-oregon-house", "Multnomah County news release (November 5, 2025): the Multnomah and Clackamas County Boards of Commissioners appointed Lamar Wise to Oregon House District 48, filling the seat vacated by the passing of Rep. Hoa Nguyen."))),
    ("house", 51): ("2025-10-23", dict(name="Matt Bunch", party="Republican", start="2025-11-17",
        note="Christine Drazan resigned on October 23, 2025, after her appointment to the State Senate. Matt Bunch was appointed by the Clackamas County Commission on November 17, 2025, and serves the remainder of the term.",
        src=("https://www.clackamas.us/news/2025-11-17/matt-bunch-appointed-to-house-district-51-vacant-seat", "Clackamas County news release (November 17, 2025): Matt Bunch was appointed to the Oregon House by Clackamas County Commissioners, filling the House District 51 seat vacated when Christine Drazan moved to the State Senate."))),
}
HD34_NOTE = ("Lisa Reynolds, re-elected in 2024, resigned the seat on November 15, 2024, before the new term began, "
    "after her appointment to the State Senate; she never served in the 2025 term, so no membership is recorded for "
    "her in this seat (candidacy recorded; compare the California AD32 precedent). Mari Watanabe was appointed by the "
    "Multnomah and Washington county commissions on January 15, 2025, and sworn in on January 19, 2025.")
WATANABE_SRC = ("https://multnomah.granicus.com/MetaViewer.php?clip_id=3093&meta_id=178777&view_id=2",
    "Multnomah and Washington County Boards of Commissioners, appointment order for State Representative District 34 (adopted January 15, 2025): the boards voted to appoint Mari Watanabe to fill the vacancy, for forwarding to the Secretary of State under ORS 171.060(3).")
HD32_NOTE = "Cyrus Javadi changed his party registration from Republican to Democratic on September 5, 2025; his 2024 candidacy is recorded as printed in the abstract."

def field_note(chamber_label, dist, cands):
    parts = []
    for c in cands:
        if c["misc"]:
            parts.append(f"miscellaneous write-ins {c['votes']:,}")
        elif c["winner"]:
            parts.append(f"{ballot(c)} ({c['party']}) {c['votes']:,} votes, marked ** as elected")
        else:
            parts.append(f"{ballot(c)} ({c['party']}) {c['votes']:,}")
    w = next(c for c in cands if c["winner"])
    runner = max((c for c in cands if not c["winner"] and not c["misc"]), key=lambda c: c["votes"], default=None)
    margin = w["votes"] - (runner["votes"] if runner else 0)
    codes = []
    for c in cands:
        if c["party"] and c["party"] not in codes: codes.append(c["party"])
    key = " Party labels are as printed in the abstract: " + ", ".join(f"({k}) {PARTYNAME.get(k, k)}" for k in codes) + "."
    return (f"For {chamber_label}, District {dist}: " + "; ".join(parts) +
            f". {ballot(w)} won by a plurality of {margin:,} votes." + key)

def src_block(url, note):
    return f"- url: {url}\n  note: '{note}'\n  retrieved: '2026-10-23'\n"

people = {}       # slug -> {name, candidacies: [..], sources: [..]}
memberships = []  # dicts
contests = {"2024-11-05": [], "2022-11-08": []}
files = {}

def add_candidacy(slug, contest_id, election_id, jur_id, office_id, party, bname, srcs):
    p = people.setdefault(slug, {"name": None, "candidacies": [], "sources": []})
    p["candidacies"].append(dict(contest_id=contest_id, election_id=election_id, jurisdiction_id=jur_id,
                                 office_id=office_id, party=party, ballot_name=bname, status="active"))
    for s in srcs:
        if s not in p["sources"]: p["sources"].append(s)

for chamber, label, role, divkind in [("senate", "State Senator", "State Senator", "sldu"),
                                      ("house", "State Representative", "State Representative", "sldl")]:
    for dist in range(1, (31 if chamber == "senate" else 61)):
        if chamber == "senate":
            elections = []
            if dist in SENATE_2024: elections.append(("2024-11-05", parsed("senate", dist, d24), A2024, "2025-01-13"))
            else: elections.append(("2022-11-08", parsed("senate", dist, d22), A2022, "2023-01-09"))
            if dist == 18: elections.append(("2022-11-08", OVERRIDE.get(("senate22", 18)) or parsed("senate", 18, d22), A2022, None))
        else:
            elections = [("2024-11-05", parsed("house", dist, d24), A2024, "2025-01-13")]
        if (chamber, dist) in OVERRIDE: elections = [(e[0], OVERRIDE[(chamber, dist)], e[2], e[3]) for e in elections]
        if chamber == "senate" and ("senate22", dist) in OVERRIDE:
            elections = [(e[0], OVERRIDE[("senate22", dist)] if e[0] == "2022-11-08" else e[1], e[2], e[3]) for e in elections]

        jur_id = f"ocd-jurisdiction/country:us/state:or/{divkind}:{dist}/legislature"
        org_id = "ocd-organization/" + uid("organization", f"or|state|{chamber}-district-{dist}")
        post_id = f"or-{chamber}-{dist}/{'state-senator' if chamber == 'senate' else 'state-representative'}"
        post_file = f"or-{chamber}-{dist}-{'state-senator' if chamber == 'senate' else 'state-representative'}"
        org_name = ("Oregon State Senate" if chamber == "senate" else "Oregon House of Representatives") + f" -- District {dist}"
        hdr = f"# Oregon {label} District {dist} -- step 3 of the build order (post + holder together);\n# issue #170 (OR master tracking).\n"

        # district sources from the most recent election
        edate, cands, aurl, _ = elections[0]
        a_short = "November 5, 2024" if edate == "2024-11-05" else "November 8, 2022"
        abstract_name = f"Oregon Secretary of State, Elections Division, {a_short} General Election Abstract of Votes (certified county-by-county abstract), published through the Oregon State Archives records system and linked from the Secretary of State's Election Results & History page. "
        note = abstract_name + field_note(label, dist, cands)
        if edate == "2024-11-05":
            note += " Members of the 83rd Legislative Assembly were sworn in on January 13, 2025."
        else:
            note += " Senators elected in 2022 were sworn in on January 9, 2023."
        if chamber == "senate" and dist == 18:
            note += " In 2022 the District 18 seat was on the ballot for a two-year term (redistricting): Wlnsvey E Campos (D) 30,534 votes, marked ** as elected; Kimberly Rice (R) 17,848; Rich Vial (NAV) 5,599; miscellaneous write-ins 59; Campos was re-elected to the full term in 2024."
        if (chamber, dist) in SUCCESSION:
            note += " " + SUCCESSION[(chamber, dist)][1]["note"]
        if chamber == "house" and dist == 34: note += " " + HD34_NOTE
        if chamber == "house" and dist == 32: note += " " + HD32_NOTE
        note = note.replace("'", "''")
        district_srcs = src_block(aurl, note)

        files[f"data/us/or/jurisdictions/state/{dist}-{chamber}.yaml"] = (
            hdr + f"id: {jur_id}\nname: District {dist} ({org_name.split(' -- ')[0]} delegation)\nstate: or\n"
            f"division_id: ocd-division/country:us/state:or/{divkind}:{dist}\nclassification: legislature\nsources:\n" + district_srcs)
        files[f"data/us/or/organizations/state/{dist}-{chamber}.yaml"] = (
            hdr + f"id: {org_id}\nname: {org_name}\njurisdiction_id: {jur_id}\nidentifiers: []\nsources:\n" + district_srcs)
        files[f"data/us/or/posts/state/{post_file}.yaml"] = (
            hdr + f"id: {post_id}\norganization_id: {org_id}\ntitle: {label}\nseats: 1\nidentifiers: []\nsources:\n" + district_srcs)

        for (edate, ecands, eaurl, class_start) in elections:
            w = next(c for c in ecands if c["winner"])
            bname = ballot(w)
            dname = display(bname)
            slug = "elizabeth-steiner" if dname == "Elizabeth Steiner" else slugify(dname)
            contest_id = f"or/{edate}/{chamber}-district-{dist}"
            election_id = f"or/{edate}/general"
            add_candidacy(slug, contest_id, election_id, jur_id, post_id, PARTYNAME.get(w["party"], w["party"]), bname,
                          [src_block(eaurl, (abstract_name + field_note(label, dist, ecands)).replace("'", "''"))])
            people[slug]["name"] = dname
            contests[edate].append(dict(id=contest_id, jurisdiction_id=jur_id, office_id=post_id,
                                        winner_slug=slug, winner_name=dname))
            if class_start:  # the seating election for the current term
                succ = SUCCESSION.get((chamber, dist))
                if chamber == "house" and dist == 34:
                    memberships.append(dict(post_file=post_file, post_id=post_id, org_id=org_id, role=role,
                        slug="mari-watanabe", start="2025-01-15", end=None, how="appointed",
                        srcs=district_srcs + src_block(*[x.replace("'", "''") if i == 1 else x for i, x in enumerate(WATANABE_SRC)])))
                    people.setdefault("mari-watanabe", {"name": "Mari Watanabe", "candidacies": [], "sources": []})
                    people["mari-watanabe"]["sources"].append(src_block(eaurl, note))
                    people["mari-watanabe"]["sources"].append(src_block(*[x.replace("'", "''") if i == 1 else x for i, x in enumerate(WATANABE_SRC)]))
                elif succ:
                    end, s = succ
                    memberships.append(dict(post_file=post_file, post_id=post_id, org_id=org_id, role=role,
                        slug=slug, start=class_start, end=end, how="elected", srcs=district_srcs))
                    sslug = slugify(s["name"])
                    memberships.append(dict(post_file=post_file, post_id=post_id, org_id=org_id, role=role,
                        slug=sslug, start=s["start"], end=None, how="appointed",
                        srcs=district_srcs + src_block(s["src"][0], s["src"][1].replace("'", "''"))))
                    people.setdefault(sslug, {"name": s["name"], "candidacies": [], "sources": []})
                    if not any(c["contest_id"].endswith(f"{chamber}-district-{dist}") and c["election_id"] == election_id for c in people[sslug]["candidacies"]):
                        pass  # successors who also won this seat keep their candidacy; appointees keep none
                    people[sslug]["sources"].append(src_block(s["src"][0], s["src"][1].replace("'", "''")))
                else:
                    memberships.append(dict(post_file=post_file, post_id=post_id, org_id=org_id, role=role,
                        slug=slug, start=class_start, end=None, how="elected", srcs=district_srcs))

# --- people files ---
for slug, p in sorted(people.items()):
    if slug == "elizabeth-steiner": continue  # edited separately below
    cand_yaml = ""
    if p["candidacies"]:
        cand_yaml = "candidacies:\n"
        for c in p["candidacies"]:
            cand_yaml += (f"- contest_id: {c['contest_id']}\n  election_id: {c['election_id']}\n"
                          f"  jurisdiction_id: {c['jurisdiction_id']}\n  office_id: {c['office_id']}\n"
                          f"  party: {c['party']}\n  ballot_name: {c['ballot_name']}\n  status: {c['status']}\n")
    else:
        cand_yaml = "candidacies: []\n"
    srcs = "".join(dict.fromkeys(p["sources"]))
    files[f"data/us/or/people/state/{slug}.yaml"] = (
        f"# Oregon Legislative Assembly -- issue #170 (OR master tracking).\n"
        f"id: ocd-person/{uid('person', 'or|state|' + slug)}\nname: {p['name']}\nidentifiers: []\n" + cand_yaml +
        "verification:\n  status: machine-extracted\n  reviewed_on: '2026-10-23'\n  pipeline: build_or_legislative\nsources:\n" + srcs)

# --- membership files ---
for m in memberships:
    mid = f"{m['post_file']}-{m['slug']}"
    end_yaml = f"end: '{m['end']}'\n" if m["end"] else ""
    files[f"data/us/or/memberships/state/{mid}.yaml"] = (
        f"# Oregon Legislative Assembly -- issue #170 (OR master tracking).\n"
        f"id: {mid}\nperson_id: ocd-person/{uid('person', 'or|state|' + m['slug'])}\norganization_id: {m['org_id']}\n"
        f"post_id: {m['post_id']}\nrole: {m['role']}\nstart: '{m['start']}'\n" + end_yaml +
        f"how_seated: {m['how']}\nsources:\n" + m["srcs"])

if DRY:
    print(f"WOULD WRITE {len(files)} new files; {len(people)} people ({sum(1 for p in people.values() if p['candidacies'])} with candidacies); {len(memberships)} memberships; contests 2024: {len(contests['2024-11-05'])}, 2022: {len(contests['2022-11-08'])}")
else:
    for rel, content in files.items():
        pth = REPO / rel
        pth.parent.mkdir(parents=True, exist_ok=True)
        pth.write_text(content)
    print(f"WROTE {len(files)} new files; {len(people)} people; {len(memberships)} memberships; contests 2024: {len(contests['2024-11-05'])}, 2022: {len(contests['2022-11-08'])}")

json.dump({"contests": contests}, open(Path(__file__).parent / "leg_contests.json", "w"), indent=1)
for edate in ("2024-11-05", "2022-11-08"):
    print(edate, len(contests[edate]), "contests")
