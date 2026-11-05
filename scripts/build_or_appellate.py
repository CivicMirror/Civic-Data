#!/usr/bin/env python3
"""Oregon appellate judiciary build (issue #170): Oregon Supreme Court (7),
Court of Appeals (13), Tax Court (1) -- jurisdictions/orgs/posts/people/
memberships + judicial contests in six election files (2020P, 2020G, 2022P,
2022G append, 2024P, 2024G append).

Election figures come from the certified SOS Abstracts of Votes (parsed in
jud*.json). Terms begin the first Monday in January after the election
(Ballotpedia's stated term-expiration dates Jan 4, 2021 and Jan 6, 2025
confirm the convention). Holders who first reached the court by gubernatorial
appointment within the current cycle get an appointed membership followed by
their elected one; departed 2020 winners (Balmer, Walters, DeVore) get ended
elected memberships.
"""
import json, re
from pathlib import Path
from uuid import uuid5, UUID

NS = UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
def uid(kind, slug): return str(uuid5(NS, f"{kind}|or|state|{slug}"))
def pid(slug): return f"ocd-person/{uid('person', slug)}"
def oid(slug): return f"ocd-organization/{uid('organization', slug)}"

REPO = Path.home() / "workspace/civic-data-or170"
STAGE = Path.home() / "workspace/or170"
JUR_ID = "ocd-jurisdiction/country:us/state:or/judiciary"
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

def yq(s):
    return s.replace("'", "''")

def loadj(fn):
    return json.load(open(STAGE / fn))

PARSED = {
    "2020-05-19": loadj("jud2020-primary.json"),
    "2020-11-03": loadj("jud2020.json"),
    "2022-05-17": loadj("jud2022-primary.json"),
    "2022-11-08": loadj("jud2022.json"),
    "2024-05-21": loadj("jud2024-primary.json"),
    "2024-11-05": loadj("jud2024.json"),
}
TAX2024 = loadj("jud2024-tax.json")

def field(date, court, pos):
    """Return parsed candidate list for a contest; court in supreme/appeals/tax."""
    src = TAX2024 if (date, court) == ("2024-05-21", "tax") else PARSED[date]
    cands = [dict(c) for c in src[court][str(pos)]]
    if (date, court, str(pos)) == ("2024-05-21", "appeals", "7"):
        # Parser absorbed the Tax Court table into this block; figures below are
        # the race's own printed Total line, read from the abstract page.
        for c in cands:
            if c["surname"] == "Powers": c["votes"] = 565143
            if c["misc"]: c["votes"] = 11600
    if (date, court, str(pos)) == ("2024-11-05", "supreme", "1"):
        # County rows sum the write-in column to 26,078; the abstract's printed
        # Total (and Ballotpedia's certified table) is 26,077. Printed wins.
        for c in cands:
            if c["misc"]: c["votes"] = 26077
    return cands

def fmt_field(cands):
    named = sorted([c for c in cands if not c["misc"]], key=lambda c: -c["votes"])
    misc = next((c["votes"] for c in cands if c["misc"]), 0)
    parts = []
    for c in named:
        nm = f"{c['given']} {c['surname']}".strip()
        parts.append(f"{nm} {c['votes']:,}")
    return "; ".join(parts), misc

# ---------------- people ----------------
# slug: (display name, [candidacies])  candidacy: (election_date, court, pos, ballot_name)
PEOPLE = {}
def add_person(slug, name):
    PEOPLE[slug] = {"name": name, "cands": []}

COURTS = {
    "supreme": {"org_slug": "or-supreme-court", "org_name": "Oregon Supreme Court",
                "post_prefix": "or-supreme-court", "office_word": "Justice",
                "contest_word": "Judge of the Supreme Court",
                "post_file": "or-supreme-court-justice-position-%d",
                "post_id": "or-supreme-court/justice-position-%d",
                "title": "Justice, Position %d", "role": "Associate Justice"},
    "appeals": {"org_slug": "or-court-of-appeals", "org_name": "Oregon Court of Appeals",
                "post_prefix": "or-court-of-appeals", "office_word": "Judge",
                "contest_word": "Judge of the Court of Appeals",
                "post_file": "or-court-of-appeals-judge-position-%d",
                "post_id": "or-court-of-appeals/judge-position-%d",
                "title": "Judge, Position %d", "role": "Judge"},
    "tax": {"org_slug": "or-tax-court", "org_name": "Oregon Tax Court",
            "post_prefix": "or-tax-court", "office_word": "Judge",
            "contest_word": "Judge of the Oregon Tax Court",
            "post_file": "or-tax-court-judge",
            "post_id": "or-tax-court/judge",
            "title": "Judge", "role": "Judge"},
}

# (court, pos, slug, display, ballot, win_date)
WINS = [
    ("supreme", 1, "thomas-balmer", "Thomas Balmer", "Thomas A Balmer", "2020-05-19"),
    ("supreme", 1, "stephen-bushong", "Stephen Bushong", "Stephen K Bushong", "2024-11-05"),
    ("supreme", 2, "rebecca-duncan", "Rebecca Duncan", "Rebecca A Duncan", "2024-05-21"),
    ("supreme", 3, "meagan-flynn", "Meagan Flynn", "Meagan A Flynn", "2024-05-21"),
    ("supreme", 4, "christopher-garrett", "Christopher Garrett", "Christopher L Garrett", "2020-11-03"),
    ("supreme", 5, "aruna-masih", "Aruna Masih", "Aruna Masih", "2024-05-21"),
    ("supreme", 6, "roger-dehoog", "Roger DeHoog", "Roger J DeHoog", "2022-05-17"),
    ("supreme", 7, "martha-walters", "Martha Walters", "Martha Walters", "2020-05-19"),
    ("supreme", 7, "bronson-james", "Bronson James", "Bronson D James", "2024-11-05"),
    ("appeals", 1, "josephine-mooney", "Josephine Mooney", "Josephine H Mooney", "2020-05-19"),
    ("appeals", 2, "megan-jacquot", "Megan Jacquot", "Megan L Jacquot", "2024-05-21"),
    ("appeals", 3, "darleen-ortega", "Darleen Ortega", "Darleen Ortega", "2022-05-17"),
    ("appeals", 4, "robyn-aoyagi", "Robyn Aoyagi", "Robyn Ridler Aoyagi", "2024-05-21"),
    ("appeals", 5, "scott-shorr", "Scott Shorr", "Scott A Shorr", "2022-05-17"),
    ("appeals", 6, "james-egan", "James Egan", "James C Egan", "2024-05-21"),
    ("appeals", 7, "steven-powers", "Steven Powers", "Steven R Powers", "2024-05-21"),
    ("appeals", 8, "ramon-pagan", "Ramón Pagán", "Ramón A Pagán", "2022-05-17"),
    ("appeals", 9, "jacqueline-kamins", "Jacqueline Kamins", "Jacqueline S Kamins", "2020-11-03"),
    ("appeals", 10, "kristina-hellman", "Kristina Hellman", "Kristina Hellman", "2022-11-08"),
    ("appeals", 11, "joel-devore", "Joel DeVore", "Joel DeVore", "2020-05-19"),
    ("appeals", 11, "anna-joyce", "Anna Joyce", "Anna M Joyce", "2022-11-08"),
    ("appeals", 12, "erin-lagesen", "Erin Lagesen", "Erin C Lagesen", "2020-05-19"),
    ("appeals", 13, "douglas-tookey", "Douglas Tookey", "Doug Tookey", "2020-05-19"),
    ("tax", 1, "robert-manicke", "Robert Manicke", "Robert Manicke", "2024-05-21"),
]
for court, pos, slug, disp, ballot, date in WINS:
    add_person(slug, disp)
    PEOPLE[slug]["cands"].append((date, court, pos, ballot))

# ---------------- memberships ----------------
OSB_RETIRE = ("https://capitolinsider.osbar.org/2022/11/10/november-9-2022/",
              "Oregon State Bar Capitol Insider, Nov. 9, 2022: Chief Justice Martha Walters and Justice Thomas Balmer both retired effective December 31, 2022.")
ADVOCATE = ("https://corvallisadvocate.com/oregons-second-female-chief-justice-takes-office/",
            "Oregon Capital Chronicle via Corvallis Advocate, Jan. 2023: Chief Justice Flynn swore in Governor Brown's appointees Stephen Bushong and Bronson James, replacing Balmer and Walters; both had to stand for election in 2024.")
VACANCY_NOTICE = ("https://apps.oregon.gov/oregon-newsroom/OR/GOV/Posts/Post/governor-kate-brown-announces-oregon-supreme-court-vacancy-14701",
                  "Office of the Governor: Justice Balmer's retirement was effective December 31, 2022, and the appointee would begin service immediately thereafter.")
LINCOLN_CHRON = ("https://lincolnchronicle.org/oregon-chief-justice-to-retire/",
                 "Oregon Capital Chronicle: Chief Justice Walters retired December 31, 2022 and was succeeded as Chief Justice by Justice Meagan Flynn.")
MASIH_REL = ("https://uat-oregon.egov.com/nova/OR/GOV/Posts/Post/governor-kotek-appoints-aruna-masih-to-oregon-supreme-court-59424",
             "Office of the Governor, Aug. 16, 2023: Governor Kotek announced the appointment of Aruna Masih to the Oregon Supreme Court.")
MASIH_WIKI = ("https://en.wikipedia.org/wiki/Aruna_Masih",
              "Masih was sworn in on September 1, 2023 (citing her Oregon Judicial Department biography), succeeding Adrienne Nelson, who had been confirmed to the federal bench.")
BP2024 = ("http://retrosearch.org/browse?url=https://ballotpedia.org/Oregon_Supreme_Court_elections,_2024",
          "Ballotpedia, Oregon Supreme Court elections, 2024: the terms of the justices in Positions 1, 2, 3, 5 and 7 expired January 6, 2025; Positions 1 and 7 were on the 2024 ballot due to retirement, with the primary canceled and the appointees advancing to the general election. DeHoog was appointed by Governor Brown in 2022.")
BP2020COA = ("https://www.non-stop.kr/BsTransOriginPage.php?tpv=&tplFileName=cntTpl250201053552-273236475&t_url=http%3A%2F%2Fballotpedia.org%2FOregon_intermediate_appellate_court_elections%2C_2020&isref=1",
             "Ballotpedia, Oregon intermediate appellate court elections, 2020: the terms of Judges DeVore, Lagesen, Mooney and Tookey expired January 4, 2021; Position 9 was a special election after Jacqueline Kamins was appointed on January 17, 2020.")
PAGAN_TENURE = ("https://www.shabupc.com/who-are-the-justices-on-the-oregon-supreme-court/",
                "Court roster summary: Judge Ramon Pagan's tenure on the Court of Appeals began January 19, 2022, appointed by Governor Kate Brown; Anna Joyce's appointment was likewise announced by Governor Brown on January 19, 2022 (Governor's appellate appointments announcement of that date, announcing DeHoog, Pagan and Joyce).")
OJP_JOYCE = ("https://www.oregonjournalismproject.org/appeals-judge-who-wrote-opinion-favorable-to-pacificorp-formerly-represented-the-utility-giant",
             "Oregon Journalism Project: Anna Joyce joined the Court of Appeals by gubernatorial appointment in January 2022, before her November 2022 election.")

# (court, pos, slug, [(how_seated, start, end_or_None, role_override, [extra sources], note)])
MEMBERSHIPS = [
    ("supreme", 1, "thomas-balmer", [("elected", "2021-01-04", "2022-12-31", None, [OSB_RETIRE], "Elected May 19, 2020; retired effective December 31, 2022.")]),
    ("supreme", 1, "stephen-bushong", [
        ("appointed", "2023-01-01", "2025-01-06", None, [VACANCY_NOTICE, ADVOCATE], "Appointed by Governor Kate Brown to the vacancy created by Justice Balmer's December 31, 2022 retirement; sworn in by Chief Justice Flynn in January 2023."),
        ("elected", "2025-01-06", None, None, [BP2024], "Won the November 5, 2024 general election (the primary was canceled, one candidate filed) for the term beginning January 6, 2025.")]),
    ("supreme", 2, "rebecca-duncan", [("elected", "2025-01-06", None, None, [], "Re-elected May 21, 2024. Justice Duncan was originally appointed to the court in 2017 and first elected in 2018; only the current term is modeled.")]),
    ("supreme", 3, "meagan-flynn", [("elected", "2025-01-06", None, "Chief Justice", [LINCOLN_CHRON], "Re-elected May 21, 2024. Justice Flynn, on the court since 2017, became Chief Justice in January 2023 on Chief Justice Walters's retirement.")]),
    ("supreme", 4, "christopher-garrett", [("elected", "2021-01-04", None, None, [], "Won the November 3, 2020 general election. Justice Garrett was originally appointed in 2018; the current term began January 4, 2021.")]),
    ("supreme", 5, "aruna-masih", [
        ("appointed", "2023-09-01", "2025-01-06", None, [MASIH_REL, MASIH_WIKI], "Appointed by Governor Tina Kotek (announced August 16, 2023) to the vacancy left by Justice Adrienne Nelson's move to the federal bench; sworn in September 1, 2023."),
        ("elected", "2025-01-06", None, None, [BP2024], "Won the May 21, 2024 primary with a majority, elected outright, for the term beginning January 6, 2025.")]),
    ("supreme", 6, "roger-dehoog", [
        ("appointed", "2022-01-19", "2023-01-02", None, [BP2024], "Appointed by Governor Kate Brown (announced January 19, 2022) to the vacancy created by Justice Lynn Nakamoto's December 31, 2021 retirement."),
        ("elected", "2023-01-02", None, None, [], "Won the May 17, 2022 primary with a majority, elected outright, for the term beginning January 2, 2023.")]),
    ("supreme", 7, "martha-walters", [("elected", "2021-01-04", "2022-12-31", None, [OSB_RETIRE], "Elected May 19, 2020; served as Chief Justice until her retirement effective December 31, 2022.")]),
    ("supreme", 7, "bronson-james", [
        ("appointed", "2023-01-01", "2025-01-06", None, [ADVOCATE], "Appointed by Governor Kate Brown to the vacancy created by Chief Justice Walters's December 31, 2022 retirement, moving up from the Court of Appeals; sworn in by Chief Justice Flynn in January 2023."),
        ("elected", "2025-01-06", None, None, [BP2024], "Won the November 5, 2024 general election (the primary was canceled, one candidate filed) for the term beginning January 6, 2025.")]),
    ("appeals", 1, "josephine-mooney", [("elected", "2021-01-04", None, None, [BP2020COA], "Won the May 19, 2020 primary with a majority, elected outright. Judge Mooney was originally appointed in 2019; only the current term is modeled.")]),
    ("appeals", 2, "megan-jacquot", [("elected", "2025-01-06", None, None, [], "Won the May 21, 2024 primary with a majority, elected outright.")]),
    ("appeals", 3, "darleen-ortega", [("elected", "2023-01-02", None, None, [], "Won the May 17, 2022 primary with a majority of the votes cast, elected outright.")]),
    ("appeals", 4, "robyn-aoyagi", [("elected", "2025-01-06", None, None, [], "Re-elected May 21, 2024. Judge Aoyagi was originally appointed in 2017; only the current term is modeled.")]),
    ("appeals", 5, "scott-shorr", [("elected", "2023-01-02", None, None, [], "Won the May 17, 2022 primary with a majority, elected outright.")]),
    ("appeals", 6, "james-egan", [("elected", "2025-01-06", None, None, [], "Re-elected May 21, 2024.")]),
    ("appeals", 7, "steven-powers", [("elected", "2025-01-06", None, None, [], "Won the May 21, 2024 primary with a majority, elected outright.")]),
    ("appeals", 8, "ramon-pagan", [
        ("appointed", "2022-01-19", "2023-01-02", None, [PAGAN_TENURE], "Appointed by Governor Kate Brown; tenure began January 19, 2022."),
        ("elected", "2023-01-02", None, None, [], "Won the May 17, 2022 primary with a majority, elected outright, for the term beginning January 2, 2023.")]),
    ("appeals", 9, "jacqueline-kamins", [
        ("appointed", "2020-01-17", "2021-01-04", None, [BP2020COA], "Appointed by Governor Kate Brown on January 17, 2020."),
        ("elected", "2021-01-04", None, None, [BP2020COA], "Won the November 3, 2020 special election for the seat, for the term beginning January 4, 2021.")]),
    ("appeals", 10, "kristina-hellman", [("elected", "2023-01-02", None, None, [], "Won the November 8, 2022 general election (no majority winner in the May primary, so the race was decided in November).")]),
    ("appeals", 11, "joel-devore", [("elected", "2021-01-04", "2022", None, [BP2020COA, OJP_JOYCE], "Re-elected May 19, 2020 for the term beginning January 4, 2021; left the court in 2022 -- Governor Brown announced his successor's appointment on January 19, 2022. Year-precision end: no exact departure date in the sources used.")]),
    ("appeals", 11, "anna-joyce", [
        ("appointed", "2022-01-19", "2023-01-02", None, [OJP_JOYCE, PAGAN_TENURE], "Appointed by Governor Kate Brown (announced January 19, 2022) to the vacancy left by Judge DeVore."),
        ("elected", "2023-01-02", None, None, [], "Won the November 8, 2022 general election for the term beginning January 2, 2023.")]),
    ("appeals", 12, "erin-lagesen", [("elected", "2021-01-04", None, None, [BP2020COA], "Won the May 19, 2020 primary with a majority, elected outright.")]),
    ("appeals", 13, "douglas-tookey", [("elected", "2021-01-04", None, None, [BP2020COA], "Won the May 19, 2020 primary with a majority, elected outright.")]),
    ("tax", 1, "robert-manicke", [("elected", "2025-01-06", None, None, [], "Re-elected May 21, 2024. Judge Manicke was appointed in January 2018 and first elected that November; only the current term is modeled.")]),
]

def contest_id(date, court, pos):
    if court == "tax": return f"or/{date}/tax-court"
    seg = "supreme-court" if court == "supreme" else "court-of-appeals"
    return f"or/{date}/{seg}-position-{pos}"

def post_file_stem(court, pos):
    c = COURTS[court]
    return c["post_file"] % pos if "%d" in c["post_file"] else c["post_file"]

def post_id(court, pos):
    c = COURTS[court]
    return c["post_id"] % pos if "%d" in c["post_id"] else c["post_id"]

def abs_source(date, extra_note):
    return {"url": ABS[date], "note": f"{ABS_NAME[date]}. {extra_note}", "retrieved": "2026-10-23"}

created, edited = [], []

# ---------- jurisdiction + orgs + posts ----------
jur = f"""# Built for issue #170 (Oregon master tracking): the statewide Oregon
# judiciary, hosting the Supreme Court, Court of Appeals and Tax Court.
# Circuit Court districts get their own judicial-district jurisdictions.
id: {JUR_ID}
name: Oregon Judiciary
state: or
division_id: ocd-division/country:us/state:or
classification: judiciary
sources:
- url: https://www.oregon.gov/oha/PH/ABOUT/Documents/Oregon%20Court%20System.pdf
  note: 'Placeholder source replaced below.'
  retrieved: '2026-10-23'
"""
# use SOS elections page as the jurisdiction-level source instead
jur = jur.replace("https://www.oregon.gov/oha/PH/ABOUT/Documents/Oregon%20Court%20System.pdf",
                  "https://sos.oregon.gov/elections/Pages/historical-data.aspx")
jur = jur.replace("Placeholder source replaced below.",
                  "Oregon Secretary of State, Election Results & History: the judges of the Oregon appellate courts and Tax Court are elected statewide in nonpartisan elections to six-year terms.")
(REPO / "data/us/or/jurisdictions/state/or-judiciary.yaml").write_text(jur)
created.append("jurisdictions/state/or-judiciary.yaml")

for key, c in COURTS.items():
    org = f"""# Built for issue #170 (Oregon master tracking).
id: {oid(c['org_slug'])}
name: {c['org_name']}
jurisdiction_id: {JUR_ID}
identifiers: []
sources:
- url: {ABS['2024-05-21']}
  note: '{yq(ABS_NAME['2024-05-21'])}: the {c['org_name']} judgeships are filled by statewide nonpartisan election to six-year terms.'
  retrieved: '2026-10-23'
"""
    (REPO / f"data/us/or/organizations/state/{c['org_slug']}.yaml").write_text(org)
    created.append(f"organizations/state/{c['org_slug']}.yaml")

for court, pos in sorted({(w[0], w[1]) for w in WINS} | {(m[0], m[1]) for m in MEMBERSHIPS}):
    c = COURTS[court]
    stem = post_file_stem(court, pos)
    title = c["title"] % pos if "%d" in c["title"] else c["title"]
    post = f"""# Built for issue #170 (Oregon master tracking).
id: {post_id(court, pos)}
organization_id: {oid(c['org_slug'])}
title: {title}
seats: 1
identifiers: []
sources:
- url: {ABS['2024-05-21']}
  note: '{yq(ABS_NAME['2024-05-21'])}: {c['contest_word']}, {"Position " + str(pos) if court != "tax" else "the court single judgeship"}, is a statewide nonpartisan office with a six-year term.'
  retrieved: '2026-10-23'
"""
    (REPO / f"data/us/or/posts/state/{stem}.yaml").write_text(post)
    created.append(f"posts/state/{stem}.yaml")

# ---------- people ----------
def person_yaml(slug):
    p = PEOPLE[slug]
    lines = [f"# Built for issue #170 (Oregon master tracking).",
             f"id: {pid(slug)}", f"name: {p['name']}", "identifiers: []", "candidacies:"]
    for date, court, pos, ballot in p["cands"]:
        lines += [
            f"- contest_id: {contest_id(date, court, pos)}",
            f"  election_id: or/{date}/{'primary' if date.endswith(('05-19', '05-17', '05-21')) else 'general'}",
            f"  jurisdiction_id: {JUR_ID}",
            f"  office_id: {post_id(court, pos)}",
            "  party: Nonpartisan",
            f"  ballot_name: {ballot}",
            "  status: active",
        ]
    lines += ["verification:", "  status: machine-extracted", "  reviewed_on: '2026-10-23'",
              "  pipeline: build_or_appellate", "sources:"]
    seen = set()
    for date, court, pos, ballot in p["cands"]:
        cands = field(date, court, pos)
        fl, misc = fmt_field(cands)
        seg = "Position " + str(pos) if court != "tax" else "the single judgeship"
        lines += [f"- url: {ABS[date]}",
                  f"  note: '{yq(ABS_NAME[date])}: for {COURTS[court]['contest_word']}, {seg}: {fl}; miscellaneous write-ins {misc:,}.'",
                  "  retrieved: '2026-10-23'"]
    return "\n".join(lines) + "\n"

for slug in PEOPLE:
    (REPO / f"data/us/or/people/state/{slug}.yaml").write_text(person_yaml(slug))
    created.append(f"people/state/{slug}.yaml")

# ---------- memberships ----------
for court, pos, slug, spans in MEMBERSHIPS:
    c = COURTS[court]
    ptitle = (c["title"] % pos if "%d" in c["title"] else c["title"])
    for how, start, end, role, extra_srcs, note in spans:
        fname = f"{post_file_stem(court, pos)}-{slug}"
        if len(spans) > 1:
            fname += f"-{start[:4]}"  # same person, two spans on one post (Millbury year-suffix precedent)
        srcs = []
        wdate = next(w[5] for w in WINS if w[0] == court and w[1] == pos and w[2] == slug)
        cands = field(wdate, court, pos)
        fl, misc = fmt_field(cands)
        srcs.append({"url": ABS[wdate], "note": yq(f"{ABS_NAME[wdate]}: for {c['contest_word']}, {'Position ' + str(pos) if court != 'tax' else 'the single judgeship'}: {fl}; miscellaneous write-ins {misc:,}. {note}")})
        for u, n in extra_srcs:
            srcs.append({"url": u, "note": yq(n)})
        body = [f"# Built for issue #170 (Oregon master tracking).",
                f"id: {fname}",
                f"person_id: {pid(slug)}",
                f"organization_id: {oid(c['org_slug'])}",
                f"post_id: {post_id(court, pos)}",
                f"role: {role or c['role']}"]
        if start: body.append(f"start: '{start}'")
        if end: body.append(f"end: '{end}'")
        body.append(f"how_seated: {how}")
        body.append("sources:")
        for s in srcs:
            body += [f"- url: {s['url']}", f"  note: '{s['note']}'", "  retrieved: '2026-10-23'"]
        (REPO / f"data/us/or/memberships/state/{fname}.yaml").write_text("\n".join(body) + "\n")
        created.append(f"memberships/state/{fname}.yaml")

# ---------- elections ----------
NEW_FILES = {
    "2020-05-19": ("primary", "May 19, 2020", "or--2020-05-19--primary.yaml"),
    "2020-11-03": ("general", "November 3, 2020", "or--2020-11-03--general.yaml"),
    "2022-05-17": ("primary", "May 17, 2022", "or--2022-05-17--primary.yaml"),
    "2024-05-21": ("primary", "May 21, 2024", "or--2024-05-21--primary.yaml"),
}
APPEND = {"2022-11-08": "or--2022-11-08--general.yaml", "2024-11-05": "or--2024-11-05--general.yaml"}
NAME2SLUG = {}
for court, pos, slug, disp, ballot, date in WINS:
    NAME2SLUG[(date, court, pos, ballot)] = slug

def contest_yaml(date, court, pos, indent=""):
    c = COURTS[court]
    cands = field(date, court, pos)
    fl, misc = fmt_field(cands)
    # winner slug: the WINS row for this date/court/pos
    wslug = next(w[2] for w in WINS if w[0] == court and w[1] == pos and w[5] == date)
    title = (f"{c['contest_word']}, Position {pos}" if court != "tax" else c["contest_word"])
    note = f"For {c['contest_word']}" + (f", Position {pos}" if court != "tax" else "") + f": {fl}; miscellaneous write-ins {misc:,}."
    decided = ("decided at the primary: under Oregon law a nonpartisan candidate who wins a majority of the votes cast at the primary is elected outright"
               if date.endswith(("05-19", "05-17", "05-21")) else
               "decided at the general election")
    lines = [f"{indent}- id: {contest_id(date, court, pos)}",
             f"{indent}  jurisdiction_id: {JUR_ID}",
             f"{indent}  office_id: {post_id(court, pos)}",
             f"{indent}  vote_for: 1",
             f"{indent}  candidate_ids:",
             f"{indent}  - {pid(wslug)}",
             f"{indent}  result_status: certified",
             f"{indent}  winners:",
             f"{indent}  - person_id: {pid(wslug)}",
             f"{indent}    name: {PEOPLE[wslug]['name']}"]
    return "\n".join(lines) + "\n"

CONTESTS = {}
for court, pos, slug, disp, ballot, date in WINS:
    CONTESTS.setdefault(date, []).append((court, pos))

for date, (etype, dlabel, fname) in NEW_FILES.items():
    body = f"""# Built for issue #170 (Oregon master tracking): judicial contests from the
# certified Abstract of Votes. Oregon nonpartisan judicial races are decided
# at the primary when a candidate wins a majority; only races without a
# primary majority (or with a canceled primary) reach the general election.
id: or/{date}/{etype}
name: Oregon {date} {etype} election
date: '{date}'
election_type: {etype}
status: official
contests:
"""
    for court, pos in sorted(CONTESTS[date]):
        body += contest_yaml(date, court, pos)
    body += f"""sources:
- url: {ABS[date]}
  note: '{yq(ABS_NAME[date])}.'
  retrieved: '2026-10-23'
"""
    (REPO / f"data/us/or/elections/{fname}").write_text(body)
    created.append(f"elections/{fname}")

for date, fname in APPEND.items():
    p = REPO / f"data/us/or/elections/{fname}"
    text = p.read_text()
    add = "".join(contest_yaml(date, court, pos) for court, pos in sorted(CONTESTS[date])
                  if f"- id: {contest_id(date, court, pos)}" not in text)
    idx = text.rindex("\nsources:")
    p.write_text(text[:idx] + "\n" + add.rstrip("\n") + text[idx:] + "")
    edited.append(f"elections/{fname}")

print(f"created {len(created)} files; edited {len(edited)}: {edited}")
for f in sorted(created): print(" +", f)
