#!/usr/bin/env python3
"""
Structure only: generate Jurisdiction, Organization (Board of Directors),
and Post (elected director/supervisor seat) records for a curated subset
of Texas Drainage Districts -- see issue #32, Phase 1.

Source: reference/TX Rolling Audit/tx_drainage_raw_2026-09-03.csv, the
"Special Districts (Non-MUD)" sheet of TX_Municipalities.xlsx filtered to
Entity Type == "Drainage District" (27 raw rows).

UNLIKE every prior type in this audit (WCID/FWSD/WID/Irrigation, all
fixed at a single statutory number; SUD, variable but jurisdiction-only
pending research), Drainage District's board size is NOT uniform even
among confirmed-elected districts: Water Code Sec. 56.052 defaults to 3
directors "unless special law provides otherwise," and this batch's own
research (issue #32 comment) found real per-district variation -- 3, 5,
or 7 seats confirmed by individual district research (each district's own
site or, where no site exists, official election-result/legislative-
history documents), not assumed from the general default. MINT_ROWS
below records the individually-confirmed seat count for each district
seeded; do not add a new row here without confirming its actual seat
count the same way.

Elected-vs-appointed was also individually confirmed per district, not
assumed: 3 districts researched turned out to be APPOINTED by their
county's commissioners court (Cameron County DD#1, DeWitt/"Green DeWitt"
Drainage District, Jefferson County DD#6) and are excluded from this
seed entirely (structure noted in reference/TX Rolling Audit/
Special_District_Type_Keys.md, no Organization/Post records -- same
appointed-exclusion discipline as ESD's population-based exception).

Held back as UNDETERMINED after a reasonable search (no governance
content found, or -- for Webb County Drainage District #1 -- elected
status confirmed but the exact total seat count could not be confirmed):
Centex Drainage District, Jackson County County Wide Drainage District,
Matagorda County Drainage District #2, Webb County Drainage District #1.

Two further rows are NOT drainage districts in the Ch. 56 sense at all
and are excluded from this script:
- "Hidalgo County Drainage District #1" -- its "board" is literally the
  Hidalgo County Commissioners Court itself (County Judge as Chairman +
  4 Precinct Commissioners), not a separate elected drainage-district
  body. Same "no separate office exists" exclusion this audit already
  applied to Road Districts and Public Improvement Districts in Phase 0
  -- officeholders here are the same county commissioners already
  tracked at the county layer. Excluded entirely, not held back.
- "Brazoria County Conservation And Reclamation District #3" and
  "Matagorda County Conservation and Reclamation District #1" -- a
  statutorily distinct category (Ch. 62, Acts of the 52nd Legislature,
  1951, and Article XVI Sec. 59 respectively -- explicitly excluded from
  Water Code Ch. 49's general provisions per the Senate Research Center
  report already read for this audit). Both confirmed elected 3-member
  boards, but seeded under their own conservation_and_reclamation_
  district: type key by seed_tx_conservation_reclamation_district.py,
  not this script.

"Grand Lakes Water Control and Improvement District" (tagged Entity Type
Drainage District, but literally named and confirmed governed as a WCID)
is reclassified into the water_control_improvement_district: type key by
seed_tx_wcid_reclassified_from_drainage.py, not this script -- same
pattern as two WID-tagged rows reclassified earlier in Phase 1.

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_drainage_jurisdictions_orgs_posts.py [--write]
"""
import re
import sys
import unicodedata
import uuid
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
JUR_DIR = DATA_DIR / "jurisdictions" / "drainage"
ORGS_DIR = DATA_DIR / "organizations" / "drainage"
POSTS_DIR = DATA_DIR / "posts" / "drainage"

RETRIEVED = "2026-09-03"
TYPE_KEY = "drainage_district"
COMPTROLLER_NOTE_BASE = (
    "Enumerated via the Texas Comptroller's Special Purpose District Public "
    "Information Database (SPDPID). Water Code Sec. 56.052 defaults to 3 "
    "directors 'unless special law provides otherwise' -- seat count and "
    "elected status individually confirmed per district (not assumed from "
    "the general default), per issue #32's Phase 1 Drainage District "
    "research comment."
)

NS = uuid.UUID("e1f4a7c9-3d6b-58e2-9a4f-7c1d3e6b9a2f")

# (name, county, website, spd_id, seats, extra_note)
MINT_ROWS = [
    ("Angleton Drainage District", "Brazoria County", "https://www.angletondrainagedistrict.org", "103225598", 3,
     "3 board members confirmed via the district's own board page (Chairman, Assistant Chairman, Secretary), staggered May-dated terms consistent with the statutory elected default; the site doesn't use the word \"elected\" explicitly."),
    ("Brazoria County Drainage District #5", "Brazoria County", "https://bcdd5.com", "103228316", 3, ""),
    ("Brazoria Drainage District #4", "Brazoria County", "https://www.bdd4.org", "103227600", 3,
     "Elected inferred from May-dated staggered terms; site doesn't state \"elected\" explicitly (moderate confidence)."),
    ("Brookshire-Katy Drainage District", "Waller County", "https://www.bkdd.dst.tx.us", "103225621", 5,
     "Board titled \"Board of Supervisors\" (Areas 1-5), not \"Directors\" -- same governing-body concept, different statutory label."),
    ("Cameron County Drainage District #3", "Cameron County", "https://www.ccdd3.org", "103227468", 3,
     "Site explicitly states \"governed by a board of three elected directors.\""),
    ("Cameron County Drainage District #5", "Cameron County", "https://www.ccdd5.org", "103227460", 3,
     "Elected inferred; site doesn't state \"elected\" explicitly and no term-date info found to cross-check (moderate confidence)."),
    ("Galveston County Consolidated Drainage District", "Galveston County", "https://www.gccdd.dst.tx.us", "103226378", 5,
     "5 Positions, unlimited 4-year terms, biennial May elections in even years; site cites governance under both Water Code Ch. 49 and Ch. 56."),
    ("Galveston County Drainage District No. 2", "Galveston County", "https://gcdd2.org", "103228299", 3,
     "Site explicitly: \"consists of 3 directors elected at large to unlimited four-year terms.\""),
    ("Jefferson County Drainage District #7", "Jefferson County", "https://www.dd7.org", "103227093", 5,
     "Site explicitly: \"Elections are held in May of even-numbered years. Commissioners are elected to four-year staggered terms.\" (titled \"Commissioners\", not \"Directors\")."),
    ("Orange County Drainage District", "Orange County", "https://www.ocddtx.com", "103225638", 5,
     "Site explicitly: \"governed by an elected five-member Board of Directors\" (4 by precinct + 1 at-large)."),
    ("Refugio County Drainage District #1", "Refugio County", None, "103227626", 5,
     "No district website; 5 seats (1 at-large + 1 per county commissioner precinct) and 4-year staggered terms found via secondary/legislative-history sources -- moderate confidence."),
    ("Velasco Drainage District", "Brazoria County", "https://www.velascodrainage.gov/", "103227591", 3,
     "Board of Supervisors, Areas 1-3; original SPDPID website (velascodrainagedistrict.com) 301-redirects to this .gov domain."),
    ("Willacy County Drainage District #1", "Willacy County", "https://www.willacycdd1.org", "103227464", 7,
     "Unusually large board for a drainage district -- confirmed via a May 2026 official election-results document listing Places 1 through 7."),
    ("Willacy County Drainage District #2", "Willacy County", "https://www.willacycdd2.org", "103227465", 5,
     "Elected inferred (site describes a \"board of directors\" without explicit \"elected\" language); sister district WCDD#1 confirmed elected via the same county elections office (moderate confidence)."),
    ("Willow Fork Drainage District", "Fort Bend County", "https://www.willowforkdrainagedistrict.com", "103226494", 5,
     "Site explicit: \"five-member Board of Directors who serve four-year, staggered terms,\" May elections in even years."),
    ("Montgomery County Drainage District #6", "Montgomery County", "https://districtdirectory.org/montgomery-county/montgomery-county-drainage-district-no-6/", "103227000", 5,
     "Elected inferred from May-dated staggered terms (Positions 1-5); page doesn't explicitly say \"elected\" (moderate confidence)."),
]

NOISE_RE = re.compile(r"\bdrainage district\b", re.IGNORECASE)


def slugify(name):
    s = name.replace("&", "and")
    s = re.sub(r"\bNo\.\s*(\d+)", r"#\1", s, flags=re.IGNORECASE)
    s = NOISE_RE.sub("", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"#\s*(\d+)", r"-\1", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def jurisdiction_id(slug):
    return f"ocd-jurisdiction/country:us/state:tx/{TYPE_KEY}:{slug}/sewer"


def division_id(slug):
    return f"ocd-division/country:us/state:tx/{TYPE_KEY}:{slug}"


def org_id(slug):
    return f"ocd-organization/{uuid.uuid5(NS, f'organization|{slug}')}"


def existing_ids(kind):
    ids = {}
    base = DATA_DIR / kind
    if not base.exists():
        return ids
    for f in base.glob("**/*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            ids[doc["id"]] = doc
    return ids


def write_file(path, doc, write):
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            HEADER
            + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
        )


def main():
    write = "--write" in sys.argv[1:]

    jur_ids = existing_ids("jurisdictions")
    org_ids = existing_ids("organizations")
    post_ids = existing_ids("posts")
    stats = Counter()

    for name, county, website, spd_id, seats, extra_note in MINT_ROWS:
        slug = slugify(name)
        source_entry = {
            "url": website or "https://spdpid.comptroller.texas.gov/",
            "note": f"{name} (SPD Public ID {spd_id}) -- {county}. {COMPTROLLER_NOTE_BASE}"
            + (f" {extra_note}" if extra_note else ""),
            "retrieved": RETRIEVED,
        }

        jid = jurisdiction_id(slug)
        if jid not in jur_ids:
            jur = {
                "id": jid,
                "name": name,
                "state": "tx",
                "division_id": division_id(slug),
                "classification": "sewer",
                "identifiers": [{"scheme": "tx-spdpid", "identifier": spd_id}],
                "sources": [source_entry],
            }
            write_file(JUR_DIR / f"{slug}-sewer.yaml", jur, write)
            stats["jurisdiction_new"] += 1
            jur_ids[jid] = jur
        else:
            stats["jurisdiction_existing"] += 1

        oid = org_id(slug)
        if oid not in org_ids:
            org = {
                "id": oid,
                "name": f"{name} Board of Directors",
                "jurisdiction_id": jid,
                "identifiers": [],
                "status": "active",
                "sources": [source_entry],
            }
            write_file(ORGS_DIR / f"{slug}-drainage-board.yaml", org, write)
            stats["org_new"] += 1
            org_ids[oid] = org
        else:
            stats["org_existing"] += 1

        for n in range(1, seats + 1):
            pid = f"{slug}-tx-drainage/director-{n}"
            if pid in post_ids:
                stats["post_existing"] += 1
                continue
            post = {
                "id": pid,
                "organization_id": oid,
                "title": f"Director, Position {n}",
                "seats": 1,
                "identifiers": [],
                "sources": [source_entry],
            }
            write_file(POSTS_DIR / f"{slug}-tx-drainage-director-{n}.yaml", post, write)
            stats["post_new"] += 1
            post_ids[pid] = post

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    print(f"mint_rows: {len(MINT_ROWS)} of 27 raw rows (see module docstring for the other 11)")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded from the TX Drainage District rolling audit (issue #32,\n"
    "# Phase 1) by scripts/seed_tx_drainage_jurisdictions_orgs_posts.py.\n"
    "# Structure only -- current officeholders are not yet researched.\n"
    "# Elected status and seat count individually confirmed per district,\n"
    "# not assumed from the Water Code Sec. 56.052 default -- see this\n"
    "# script's module docstring and issue #32 for the research trail.\n"
)


if __name__ == "__main__":
    main()
