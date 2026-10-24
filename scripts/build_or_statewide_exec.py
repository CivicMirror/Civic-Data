#!/usr/bin/env python3
"""Build the remaining Oregon statewide executive offices for issue #170.

Step 2 of the #170 build order (posts + holders + elections together, the
Governor shape): Secretary of State, State Treasurer, Attorney General from
the certified November 5, 2024 abstract, and Commissioner of Labor and
Industries from the certified November 8, 2022 abstract.

Sources (official only):
- Oregon Secretary of State, Elections Division, Abstracts of Votes, now
  published through the Oregon State Archives records system and linked from
  the SOS "Election Results & History" page (the old
  sos.oregon.gov/elections/Documents/results/*.pdf paths are retired):
  2024: https://records.sos.state.or.us/ORSOSCMSearch/Search/DocumentStream.ashx?uri=13735458
  2022: https://records.sos.state.or.us/ORSOSCMSearch/Search/DocumentStream.ashx?uri=13735454
- Multnomah County official elected-officials page (holder confirmation).
- BOLI official commissioner page (holder + term confirmation).

Also repairs the retired abstract URL in the Governor-step files (same
document, current official location; notes otherwise unchanged).

All four people are NEW: no tobias-read / elizabeth-steiner / dan-rayfield /
christina-stephenson record exists anywhere in the repo (checked 2026-10-23).
"""
import sys, uuid
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
if "--write" not in sys.argv:
    DRY = True
else:
    DRY = False

NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
def pid(kind, key):
    return str(uuid.uuid5(NS, f"{kind}|{key}"))

EXEC_JUR = "ocd-jurisdiction/country:us/state:or/executive"
A2024 = "https://records.sos.state.or.us/ORSOSCMSearch/Search/DocumentStream.ashx?uri=13735458"
A2022 = "https://records.sos.state.or.us/ORSOSCMSearch/Search/DocumentStream.ashx?uri=13735454"
OLD2022 = "https://sos.oregon.gov/elections/Documents/results/november-general-2022.pdf"
MULTCO = "https://multco.us/info/federal-and-state-elected-officials"
HDR = "# Oregon {office} -- step 2 of the build order (post + holder together);\n# issue #170 (OR master tracking).\n"

ABSTRACT24_NOTE = ("Oregon Secretary of State, Elections Division, November 5, 2024 General Election "
    "Abstract of Votes (certified county-by-county abstract), published through the Oregon State Archives "
    "records system and linked from the Secretary of State's Election Results & History page. ")
ABSTRACT22_NOTE = ("Oregon Secretary of State, Elections Division, November 8, 2022 General Election "
    "Abstract of Votes (certified county-by-county abstract), published through the Oregon State Archives "
    "records system and linked from the Secretary of State's Election Results & History page. ")

OFFICES = [
    dict(slug="secretary-of-state", title="Secretary of State", org="Oregon Office of the Secretary of State",
         person="Tobias Read", pslug="tobias-read", ballot="Tobias Read", party="Democratic",
         start="2025-01-06", election="2024-11-05",
         note=ABSTRACT24_NOTE + "For Secretary of State: Tobias Read (D) 1,166,447 votes, marked ** as elected; "
              "Dennis Linthicum (R) 897,704; Nathalie Paravicini (PG) 76,170; miscellaneous write-ins 2,011. "
              "Read won by a plurality of 268,743 votes. Party labels are as printed in the abstract: (D) Democratic, "
              "(R) Republican, (PG) Pacific Green. Read was sworn in on January 6, 2025; the next election for the "
              "office is November 7, 2028.",
         holder=("Multnomah County official page, 'Federal and State Elected Officials' (multco.us): "
                 "names Tobias Read as Oregon Secretary of State -- confirms him as the sitting Secretary of State "
                 "as of the retrieval date.")),
    dict(slug="state-treasurer", title="State Treasurer", org="Oregon Office of the State Treasurer",
         person="Elizabeth Steiner", pslug="elizabeth-steiner", ballot="Elizabeth Steiner", party="Democratic",
         start="2025-01-06", election="2024-11-05",
         note=ABSTRACT24_NOTE + "For State Treasurer: Elizabeth Steiner (D) 1,050,119 votes, marked ** as elected; "
              "Brian J Boquist (R) 919,794; Mary King (WF) 155,473; miscellaneous write-ins 1,882. "
              "Steiner won by a plurality of 130,325 votes. Party labels are as printed in the abstract: (D) Democratic, "
              "(R) Republican, (WF) Working Families. Steiner was sworn in on January 6, 2025; the next election for "
              "the office is November 7, 2028.",
         holder=("Multnomah County official page, 'Federal and State Elected Officials' (multco.us): "
                 "names Elizabeth Steiner as Oregon State Treasurer -- confirms her as the sitting Treasurer "
                 "as of the retrieval date.")),
    dict(slug="attorney-general", title="Attorney General", org="Oregon Office of the Attorney General",
         person="Dan Rayfield", pslug="dan-rayfield", ballot="Dan Rayfield", party="Democratic",
         start="2024-12-31", election="2024-11-05",
         note=ABSTRACT24_NOTE + "For Attorney General: Dan Rayfield (D) 1,156,489 votes, marked ** as elected; "
              "Will Lathrop (R) 967,964; miscellaneous write-ins 2,612. Rayfield won by a plurality of 188,525 votes. "
              "Party labels are as printed in the abstract: (D) Democratic, (R) Republican. Rayfield was sworn in on "
              "December 31, 2024, a week before his elected term began, when Ellen Rosenblum resigned the office "
              "early; the next election for the office is November 7, 2028.",
         holder=("Multnomah County official page, 'Federal and State Elected Officials' (multco.us): "
                 "names Dan Rayfield as Oregon Attorney General -- confirms him as the sitting Attorney General "
                 "as of the retrieval date.")),
    dict(slug="labor-commissioner", title="Commissioner of Labor and Industries", org="Oregon Bureau of Labor and Industries",
         person="Christina Stephenson", pslug="christina-stephenson", ballot="Christina E Stephenson", party="Nonpartisan",
         start="2023-01-02", election="2022-11-08",
         note=ABSTRACT22_NOTE + "For Commissioner of the Bureau of Labor and Industries (a nonpartisan office; the "
              "abstract prints no party labels for this contest): Christina E Stephenson 916,455 votes, marked ** as "
              "elected; Cheri Helt 582,609; miscellaneous write-ins 9,826. Stephenson won by a plurality of 333,846 "
              "votes. She assumed office on January 2, 2023.",
         holder=None),  # BOLI page used instead of Multnomah
]

BOLI_URL = "https://www.oregon.gov/boli/about/Pages/about-the-commissioner.aspx"
BOLI_NOTE = ("Oregon Bureau of Labor and Industries official page (oregon.gov), 'Meet the Commissioner': "
             "names Christina Stephenson as Commissioner, term of office 2023-2027 -- confirms her as the "
             "sitting Commissioner as of the retrieval date.")

def src_block(url, note):
    return (f"- url: {url}\n  note: '{note}'\n  retrieved: '2026-10-23'\n")

def office_sources(o):
    url = A2024 if o["election"] == "2024-11-05" else A2022
    out = src_block(url, o["note"].replace("'", "''"))
    if o["holder"]:
        out += src_block(MULTCO, o["holder"].replace("'", "''"))
    else:
        out += src_block(BOLI_URL, BOLI_NOTE.replace("'", "''"))
    return out

files = {}
for o in OFFICES:
    org_id = "ocd-organization/" + pid("organization", f"or|state|{o['slug']}")
    per_id = "ocd-person/" + pid("person", f"or|state|{o['pslug']}")
    post_id = f"or/{o['slug']}"
    contest = f"or/{o['election']}/{o['slug']}"
    election_id = f"or/{o['election']}/general"
    hdr = HDR.format(office=o["title"])
    srcs = office_sources(o)

    files[f"data/us/or/organizations/state/or-{o['slug']}.yaml"] = (
        hdr + f"id: {org_id}\nname: {o['org']}\njurisdiction_id: {EXEC_JUR}\nidentifiers: []\nsources:\n" + srcs)
    files[f"data/us/or/posts/state/or-{o['slug']}.yaml"] = (
        hdr + f"id: {post_id}\norganization_id: {org_id}\ntitle: {o['title']}\nseats: 1\nsources:\n" + srcs)
    files[f"data/us/or/people/state/{o['pslug']}.yaml"] = (
        hdr + f"id: {per_id}\nname: {o['person']}\nidentifiers: []\ncandidacies:\n"
        f"- contest_id: {contest}\n  election_id: {election_id}\n  jurisdiction_id: {EXEC_JUR}\n"
        f"  office_id: {post_id}\n  party: {o['party']}\n  ballot_name: {o['ballot']}\n  status: active\n"
        "verification:\n  status: machine-extracted\n  reviewed_on: '2026-10-23'\n  pipeline: build_or_statewide_exec\nsources:\n" + srcs)
    files[f"data/us/or/memberships/state/or-{o['slug']}-{o['pslug']}.yaml"] = (
        hdr + f"id: or-{o['slug']}-{o['pslug']}\nperson_id: {per_id}\norganization_id: {org_id}\n"
        f"post_id: {post_id}\nrole: {o['title']}\nstart: '{o['start']}'\nhow_seated: elected\nsources:\n" + srcs)
    o["org_id"], o["per_id"], o["post_id"], o["contest"] = org_id, per_id, post_id, contest

# 2024 election file (3 new contests)
c24 = [o for o in OFFICES if o["election"] == "2024-11-05"]
contests = ""
for o in c24:
    contests += (f"- id: {o['contest']}\n  jurisdiction_id: {EXEC_JUR}\n  office_id: {o['post_id']}\n"
                 f"  vote_for: 1\n  candidate_ids:\n  - {o['per_id']}\n  result_status: certified\n"
                 f"  winners:\n  - person_id: {o['per_id']}\n    name: {o['person']}\n")
note24 = ABSTRACT24_NOTE + "Statewide contests built so far: Secretary of State, State Treasurer, Attorney General (see the office files for the certified totals)."
files["data/us/or/elections/or--2024-11-05--general.yaml"] = (
    "# Oregon general election, November 5, 2024 -- statewide\n# contests are added one office at a time under the build\n"
    "# order; issue #170 (OR master tracking).\n"
    "id: or/2024-11-05/general\nname: Oregon 2024-11-05 general election\ndate: '2024-11-05'\nelection_type: general\n"
    "status: official\ncontests:\n" + contests + "sources:\n" + src_block(A2024, note24.replace("'", "''")))

written = []
for rel, content in files.items():
    p = REPO / rel
    if DRY:
        print("WOULD WRITE:", rel)
    else:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        written.append(rel)
        print("WRITE:", rel)

# Append BOLI contest to the existing 2022 election file + add archives source entry
boli = [o for o in OFFICES if o["election"] == "2022-11-08"][0]
e22 = REPO / "data/us/or/elections/or--2022-11-08--general.yaml"
if e22.exists():
    text = e22.read_text()
    if "labor-commissioner" not in text:
        contest_yaml = (f"- id: {boli['contest']}\n  jurisdiction_id: {EXEC_JUR}\n  office_id: {boli['post_id']}\n"
                        f"  vote_for: 1\n  candidate_ids:\n  - {boli['per_id']}\n  result_status: certified\n"
                        f"  winners:\n  - person_id: {boli['per_id']}\n    name: {boli['person']}\n")
        text = text.replace("sources:\n", contest_yaml + "sources:\n", 1)
        text += src_block(A2022, boli["note"].replace("'", "''"))
        if DRY:
            print("WOULD EDIT:", e22.relative_to(REPO))
        else:
            e22.write_text(text)
            print("EDIT:", e22.relative_to(REPO))
    else:
        print("2022 election file already carries the BOLI contest; skipped")

# Repair the retired 2022 abstract URL in the Governor-step files
for rel in ["data/us/or/jurisdictions/state/or-executive.yaml",
            "data/us/or/organizations/state/or-governor.yaml",
            "data/us/or/posts/state/or-governor.yaml",
            "data/us/or/people/state/tina-kotek.yaml",
            "data/us/or/memberships/state/or-governor-tina-kotek.yaml",
            "data/us/or/elections/or--2022-11-08--general.yaml"]:
    p = REPO / rel
    if p.exists() and OLD2022 in p.read_text():
        if DRY:
            print("WOULD REPAIR URL:", rel)
        else:
            p.write_text(p.read_text().replace(OLD2022, A2022))
            print("REPAIR URL:", rel)

print(f"\n{'WOULD CREATE' if DRY else 'Created'} {len(files)} new files (4 organizations, 4 posts, 4 people, 4 memberships, 1 election). All 4 people are NEW.")
