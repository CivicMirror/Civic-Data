#!/usr/bin/env python3
"""KY legislative pass, roster-diff successions (Civic-Data issue #195).

The certified-results memberships were diffed against the Legislative
Research Commission's current rosters (House members-by-district page,
crawled 2026-11-01; Senate Resolution 1, 2026 RS, establishing the 2026
Senate membership). All 100 House seats and 36 of 38 Senate seats are
held by their last general-election winners. Two Senate successions:

- District 28: Ralph Alvarado (elected 2022) resigned in January 2023 to
  become Tennessee's Commissioner of Health. Greg Elkins (R) won the
  May 16, 2023 special election for the unexpired term -- SBE, 'Official
  2023 Special Election 28th Senatorial District Results' (certification
  PDF, elect.ky.gov): Elkins 7,899; Robert Sainte (D) 4,968; Richard
  Henderson (Independent) 3,001 (county rows checksum-verified against
  the printed totals and read firsthand). Elkins was sworn in June 8,
  2023, so his membership starts '2023'; Alvarado's ends '2023'.
- District 37: David Yates (elected 2024) resigned in October 2025 after
  appointment as interim Jefferson County Clerk. Gary Clemons (D) won
  the December 16, 2025 special election -- Jefferson County Electionware
  totals (county summary hosted by the State Board of Elections;
  identical figures in the county's Official Results Report of
  December 18, 2025): Clemons 3,752; Calvin Leach (R) 1,297; Wendy
  Higdon (Libertarian) 121; 8 unnamed write-in votes (note only).
  Results were certified January 5, 2026 and the Senate seated Clemons
  by SR1 on January 6, 2026, so his membership starts '2026'; Yates's
  ends '2025'.

Calvin Leach was also the 2024 District 37 Republican candidate; his
existing person file is reused and the special-election candidacy
appended.
"""
import re, uuid
from pathlib import Path

TREE = Path(__file__).resolve().parent.parent
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
TODAY = "2026-11-01"

CERT28 = "https://elect.ky.gov/results/2020-2029/Documents/5-16-23%20Certification%20of%20Election%20Results%20for%2028th%20Senatorial%20District%20State%20Senate%20Special%20Election.pdf"
JEFF37 = "https://elect.ky.gov/Documents/Jefferson%20Special%20Cumulative.pdf"
SR1 = "https://apps.legislature.ky.gov/recorddocuments/bill/26RS/sr1/orig_bill.pdf"

def slugify(name):
    s = name.lower().replace("(", "").replace(")", "").replace(".", "").replace('"', "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)

def pid(slug):
    return "ocd-person/" + str(uuid.uuid5(NS, f"person|ky|state|{slug}"))

def org_id(ch, d):
    return "ocd-organization/" + str(uuid.uuid5(NS, f"organization|ky|{ch}-district-{d}"))

def q(s):
    return s.replace("'", "''")

NOTE28 = ("Commonwealth of Kentucky, State Board of Elections / Secretary of State, 'Official 2023 "
          "Special Election 28th Senatorial District Results' -- certified results for the May 16, 2023 "
          "special election (State Senator, 28th Senatorial District, unexpired term), county tables "
          "with district totals: Greg Elkins (Republican) 7,899; Robert Sainte (Democratic) 4,968; "
          "Richard Henderson (Independent) 3,001. Greg Elkins won with 7,899 votes. The special "
          "election filled the vacancy left by Ralph Alvarado's January 2023 resignation.")
NOTE37 = ("Jefferson County Board of Elections, Electionware Special Election Summary for the "
          "37th Senatorial District, December 16, 2025 (hosted by the Kentucky State Board of "
          "Elections) -- district totals: Gary Clemons (Democratic) 3,752; Calvin Leach (Republican) "
          "1,297; Wendy Higdon (Libertarian) 121; Write-In 8 (unnamed aggregate). Gary Clemons won "
          "with 3,752 votes. The same candidate totals appear in Jefferson County's Official Results "
          "Report of December 18, 2025; the State Board of Elections certified the results on "
          "January 5, 2026. The special election filled the vacancy left by David Yates's October "
          "2025 resignation to become Jefferson County Clerk.")
NOTE37_SR1 = ("Kentucky Senate Resolution 1 (2026 Regular Session), adopted January 6, 2026, "
              "establishing the 2026 membership of the Kentucky State Senate on the certificates of "
              "election transmitted by the Secretary of State: Gary Clemons is listed as the Senator "
              "for District 37.")

def src(url, note, indent=""):
    return (f"{indent}- url: {url}\n"
            f"{indent}  note: '{q(note)}'\n"
            f"{indent}  retrieved: '{TODAY}'\n")

SRC28 = src(CERT28, NOTE28)
SRC37 = src(JEFF37, NOTE37) + src(SR1, NOTE37_SR1)

SPECIALS = [
    dict(date="2023-05-16", district=28, note=NOTE28, source=SRC28,
         cert_url=CERT28,
         candidates=[("Greg Elkins", "Republican", 7899),
                     ("Robert Sainte", "Democratic", 4968),
                     ("Richard Henderson", "Independent", 3001)],
         winner_start="2023", prev_slug="ralph-alvarado", prev_end="2023",
         header=("# Built from the Kentucky State Board of Elections certified",
                 "# results for the May 16, 2023 special election (28th",
                 "# Senatorial District, unexpired term). Legislative pass,",
                 "# Civic-Data issue #195.")),
    dict(date="2025-12-16", district=37, note=NOTE37, source=SRC37,
         cert_url=JEFF37,
         candidates=[("Gary Clemons", "Democratic", 3752),
                     ("Calvin Leach", "Republican", 1297),
                     ("Wendy Higdon", "Libertarian", 121)],
         winner_start="2026", prev_slug="david-yates", prev_end="2025",
         header=("# Built for the December 16, 2025 special election (37th",
                 "# Senatorial District, unexpired term): candidate totals from",
                 "# the Jefferson County Electionware summary hosted by the",
                 "# State Board of Elections (identical in the county's",
                 "# Official Results Report of December 18, 2025); results",
                 "# certified January 5, 2026. Legislative pass, Civic-Data",
                 "# issue #195.")),
]

ppl_dir = TREE / "data/us/ky/people/state"
mem_dir = TREE / "data/us/ky/memberships/state"
elec_dir = TREE / "data/us/ky/elections"

for sp in SPECIALS:
    d = sp["district"]
    date = sp["date"]
    jur = f"ocd-jurisdiction/country:us/state:ky/sldu:{d}/legislature"
    office = f"ky-senate-{d}/state-senator"
    # 1. People: create or append the special-election candidacy
    for name, party, votes in sp["candidates"]:
        slug = slugify(name)
        path = ppl_dir / f"{slug}.yaml"
        cand = [f"- contest_id: ky/{date}/senate-{d}",
                f"  election_id: ky/{date}/special",
                f"  jurisdiction_id: {jur}",
                f"  office_id: {office}",
                f"  party: {party}",
                f"  ballot_name: '{q(name)}'",
                "  status: active"]
        if path.exists():
            txt = path.read_text()
            assert "verification:" in txt, path
            txt = txt.replace("verification:", "\n".join(cand) + "\nverification:", 1)
            if not txt.endswith("\n"):
                txt += "\n"
            txt += sp["source"]
            path.write_text(txt)
            print("APPENDED", path.name)
        else:
            body = ("# Minted from official Kentucky special election results\n"
                    "# (legislative pass, Civic-Data issue #195).\n"
                    f"id: {pid(slug)}\nname: {name}\nidentifiers: []\ncandidacies:\n"
                    + "\n".join(cand) + "\n"
                    "verification:\n  status: unverified\n  pipeline: build_ky_legislative_successions\nsources:\n"
                    + sp["source"])
            path.write_text(body)
            print("CREATED", path.name)
    # 2. Predecessor membership: add end year + the special-election source
    prev_files = sorted(mem_dir.glob(f"ky-senate-{d}-state-senator-*.yaml"))
    prev = next(f for f in prev_files if not any(s in f.name for s in ("elkins", "clemons")))
    txt = prev.read_text()
    assert "\nend:" not in txt, prev
    txt = txt.replace("how_seated: elected\n", f"end: '{sp['prev_end']}'\nhow_seated: elected\n", 1)
    if not txt.endswith("\n"):
        txt += "\n"
    txt += sp["source"]
    prev.write_text(txt)
    print("ENDED", prev.name, sp["prev_end"])
    # 3. Winner membership
    wname, wparty, wvotes = max(sp["candidates"], key=lambda x: x[2])
    wslug = slugify(wname)
    surname = wslug.split("-")[-1]
    mid = f"ky-senate-{d}-state-senator-{surname}"
    mf = mem_dir / f"{mid}.yaml"
    assert not mf.exists(), mf
    mf.write_text(
        "# Minted from official Kentucky special election results\n"
        "# (legislative pass, Civic-Data issue #195).\n"
        f"id: {mid}\n"
        f"person_id: {pid(wslug)}\n"
        f"organization_id: {org_id('senate', d)}\n"
        f"post_id: {office}\n"
        "role: State Senator\n"
        "seat: At-Large\n"
        f"start: '{sp['winner_start']}'\n"
        "how_seated: elected\n"
        "sources:\n" + sp["source"])
    print("MEMBERSHIP", mf.name)
    # 4. Election file
    lines = list(sp["header"]) + [
        f"id: ky/{date}/special",
        f"name: Kentucky {date} special election",
        f"date: '{date}'",
        "election_type: special",
        "status: certified",
        "contests:",
        f"- id: ky/{date}/senate-{d}",
        f"  jurisdiction_id: {jur}",
        f"  office_id: {office}",
        "  vote_for: 1",
        "  candidate_ids:"]
    for name, party, votes in sp["candidates"]:
        lines.append(f"  - {pid(slugify(name))}")
    lines += ["  result_status: certified",
              "  winners:",
              f"  - person_id: {pid(wslug)}",
              f"    name: '{q(wname)}'",
              f"    party: {wparty}",
              f"    votes: {wvotes}",
              "sources:"]
    lines.append(sp["source"].rstrip("\n"))
    ef = elec_dir / f"ky--{date}--special.yaml"
    assert not ef.exists(), ef
    ef.write_text("\n".join(lines) + "\n")
    print("ELECTION", ef.name)
print("DONE")
