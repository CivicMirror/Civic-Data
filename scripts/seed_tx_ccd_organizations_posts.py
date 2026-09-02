#!/usr/bin/env python3
"""
Structure only: generate Organization (Board of Trustees) and Post (trustee
seat) records for TX community college districts from the seat plan each
district's sourced BBB(LOCAL) text implies (see issue #14).

Reuses tx_isd_parse_structure.parse_district() as-is (see issue #13) --
its regexes operate purely on the BBB(LOCAL) text and a district key, with
no ISD-specific vocabulary; its CDN-keyed MANUAL_OVERRIDES/MANUAL_REVIEW_CDNS/
EXCLUDED_CURRENTLY_APPOINTED_CDNS dicts simply never match a THECB FICE code,
so nothing ISD-specific leaks in. Verified against all 43 TASB-matched CCDs
before writing this script: 31 parse cleanly (27 pure at-large, 4 pure SMD),
12 do not -- 6 hybrid districts whose "Membership"/"Method of Election"
wording doesn't match the ISD-derived hybrid-count regex closely enough
(CCD BBB(LOCAL) text phrases the split differently district to district),
2 with no BBB(LOCAL) policy on file at all (Galveston, San Jacinto), 3 SMD
district-number-count mismatches (Houston City, McLennan, South Texas), 1
with no board-size sentence found (South Texas College). Combined with the
7 CCDs no TASB page exists for at all (Alamo, Central Texas, Cisco, Del Mar,
Howard County, Lone Star, Navarro), that's 19 of 50 districts needing
individual per-district research -- same two-tier shape as the ISD Phase 3
pass, not seeded here.

Seat modeling: identical convention to seed_tx_isd_organizations_posts.py
(one shared Post for an at-large bloc, one Post per SMD seat).

Excludes: nothing yet at the exclusion level (no CCD has been individually
confirmed appointed-not-elected the way Houston ISD was) -- the 19 unparsed
districts are simply not templated, not excluded.

ID collisions checked globally across every existing
data/us/tx/organizations/**/*.yaml and posts/**/*.yaml id, same as the ISD
script (this repo already has *-tx-isd/... ids that could theoretically
share a base slug with a same-named CCD, e.g. no known case yet but not
assumed collision-free either).

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_ccd_organizations_posts.py [--write]
"""
import csv
import re
import sys
import uuid
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
JURISDICTIONS_DIR = DATA_DIR / "jurisdictions" / "school"
ORGS_DIR = DATA_DIR / "organizations" / "school"
POSTS_DIR = DATA_DIR / "posts" / "school"

sys.path.insert(0, str(REPO / "reference" / "TX Rolling Audit"))
from tx_isd_parse_structure import parse_district  # noqa: E402

BBB_CSV = REPO / "reference" / "TX Rolling Audit" / "tx_ccd_bbb_local_2026-09-02.csv"

# Districts whose BBB(LOCAL) text is fully sourced (see tx_ccd_bbb_local_2026-
# 09-02.csv) but didn't clear the ISD-derived parse_district() regexes --
# read by hand instead, verified against the same committed local_text these
# regexes failed on, not fetched fresh. Not code bugs to fix generically:
# each is a genuinely different phrasing (Roman-numeral district lists,
# "combination of at large and by single-member districts" without the exact
# count sentence parse_district()'s hybrid regex expects, or a board_size
# stated as a word ("seven single-member districts") outside the "consist of
# N members" sentence the regex anchors on).
CCD_MANUAL_OVERRIDES = {
    "003628": {  # Texarkana College -- 4 SMD (Bowie Co. commissioner precincts) + 3 at-large
        "board_size": 7, "at_large_seats": 3, "smd_seats": 4,
        "smd_district_numbers": [1, 2, 3, 4],
        "note": "SMD = Places 1-4 (aligned to Bowie County commissioner precincts), at-large = Places 5-7.",
    },
    "003596": {  # Odessa College -- 7 SMD (places 1-7) + 2 at-large (places 8-9)
        "board_size": 9, "at_large_seats": 2, "smd_seats": 7,
        "smd_district_numbers": [1, 2, 3, 4, 5, 6, 7],
        "note": "9 members: 7 single-member districts (places 1-7) + 2 at-large (places 8-9).",
    },
    "007096": {  # College of the Mainland -- 5 SMD (positions 1-5) + 2 at-large (positions 6-7)
        "board_size": 7, "at_large_seats": 2, "smd_seats": 5,
        "smd_district_numbers": [1, 2, 3, 4, 5],
        "note": "5 single-member districts (positions 1-5) + 2 at-large (positions 6-7).",
    },
    "010633": {  # Houston City College -- 9 pure SMD, districts numbered with Roman numerals I-IX
        "board_size": 9, "at_large_seats": 0, "smd_seats": 9,
        "smd_district_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "note": "9 single-member districts, numbered I-IX in the source text (Roman numerals -- "
                "parse_district()'s district-number regex only catches Arabic numerals).",
    },
    "031034": {  # South Texas College -- 7 pure SMD (Hidalgo/Starr counties), no explicit "consist of N members" sentence
        "board_size": 7, "at_large_seats": 0, "smd_seats": 7,
        "smd_district_numbers": [1, 2, 3, 4, 5, 6, 7],
        "note": "\"Election of Board members shall be from each of the seven single-member "
                "districts in Hidalgo and Starr counties\" -- board size stated as a word "
                "outside the regex's anchor sentence; district numbers 1-7 confirmed via the "
                "Terms and Election Schedule list.",
    },
    "003590": {  # McLennan Community College -- 7 pure SMD, Roman numerals I-VII
        "board_size": 7, "at_large_seats": 0, "smd_seats": 7,
        "smd_district_numbers": [1, 2, 3, 4, 5, 6, 7],
        "note": "7 single-member districts, numbered I-VII in the source text (Roman numerals).",
    },
    "003662": {  # Victoria College -- 4 SMD + 2 "super districts" (each a combination of 2 SMDs, still single-member) + 1 at-large
        "board_size": 7, "at_large_seats": 1, "smd_seats": 6,
        "smd_district_numbers": [1, 2, 3, 4, 5, 6],
        "note": "Districts 1-4 align to Victoria County commissioner precincts; districts 5 "
                "(=1+3 combined territory) and 6 (=2+4) are \"super districts\" but still "
                "single-member seats, just a larger elected area -- not multi-member posts. "
                "District 7 is at-large.",
    },
    "003549": {  # Blinn College District -- 4 SMD (Washington Co. commissioner precincts) + 3 at-large
        "board_size": 7, "at_large_seats": 3, "smd_seats": 4,
        "smd_district_numbers": [1, 2, 3, 4],
        "note": "One member from each of the 4 Washington County commissioner precincts (SMD) "
                "+ 3 at-large positions.",
    },
    # -- Districts with no TASB page at all (see tx_ccd_tasb_unmatched_ccds_
    # 2026-09-02.csv) or a TASB page but no BBB(LOCAL) text on file (Galveston,
    # San Jacinto) -- resolved instead from each district's own official
    # website, fetched fresh (see commit message for URLs/dates).
    "003553": {  # Cisco College -- 9 members, at-large by position
        "board_size": 9, "at_large_seats": 9, "smd_seats": 0,
        "smd_district_numbers": [],
        "source_url": "https://www.eastlandcounty.gov/DocumentCenter/View/958/Cisco-College-Resolution-2026-001-PDF",
        "note": "Board of Regents Resolution 2026-001 (approved 2/9/2026) orders the election "
                "\"by the qualified voters of the Cisco College District\" (district-wide, not "
                "a sub-district precinct) for numbered Places (1, 2, 4, 5, 6 in this cycle) -- "
                "at-large by position. Board size (9) confirmed separately via "
                "cisco.edu/about/board-of-regents (9 current regents listed) and the college's "
                "own policy manual (\"a Board of Regents of nine members, duly elected by the "
                "registered voters of the Cisco College District\"), fetched 2026-09-02.",
    },
    "003607": {  # Alamo Community College District -- 9 pure SMD, districts 1-9
        "board_size": 9, "at_large_seats": 0, "smd_seats": 9,
        "smd_district_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "source_url": "https://www.alamo.edu/about-us/leadership/board-of-trustees/",
        "note": "9 single-member districts (alamo.edu/about-us/leadership/board-of-trustees/, "
                "fetched 2026-09-02); a non-voting student trustee seat exists separately and "
                "is out of scope (elected boards only).",
    },
    "004003": {  # Central Texas College -- 7 members, at-large
        "board_size": 7, "at_large_seats": 7, "smd_seats": 0,
        "smd_district_numbers": [],
        "source_url": "https://www.ctcd.edu/about-ctc/leadership/board-of-trustees/",
        "note": "7 members elected at-large, six-year terms (ctcd.edu/about-ctc/leadership/"
                "board-of-trustees/, fetched 2026-09-02).",
    },
    "003563": {  # Del Mar College -- 5 SMD (districts 1-5) + 4 at-large
        "board_size": 9, "at_large_seats": 4, "smd_seats": 5,
        "smd_district_numbers": [1, 2, 3, 4, 5],
        "source_url": "https://www.delmar.edu/regents-and-community/board-of-regents/",
        "note": "5 single-member districts (1-5) + 4 at-large seats, 9 total "
                "(delmar.edu/regents-and-community/board-of-regents/, fetched 2026-09-02).",
    },
    "103574": {  # Howard County Junior College District -- 7 members, at-large
        "board_size": 7, "at_large_seats": 7, "smd_seats": 0,
        "smd_district_numbers": [],
        "source_url": "https://www.howardcollege.edu/about/board-of-trustees/",
        "note": "7 members elected countywide (no district/precinct subdivision found) "
                "(howardcollege.edu/about/board-of-trustees/, fetched 2026-09-02).",
    },
    "011145": {  # Lone Star College System -- 9 pure SMD, districts 1-9
        "board_size": 9, "at_large_seats": 0, "smd_seats": 9,
        "smd_district_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "source_url": "https://www.lonestar.edu/trustees.htm",
        "note": "\"Board Members are elected as representatives of nine single-member "
                "districts\" (lonestar.edu/trustees.htm, fetched 2026-09-02).",
    },
    "003593": {  # Navarro College -- 4 SMD (county commissioner precincts) + 3 at-large
        "board_size": 7, "at_large_seats": 3, "smd_seats": 4,
        "smd_district_numbers": [1, 2, 3, 4],
        "source_url": "https://www.navarrocollege.edu/trustees/elections.html",
        "note": "\"One trustee from each Navarro County Commissioner's Precinct and three by "
                "place (at-large)\" (navarrocollege.edu/trustees/elections.html, fetched 2026-09-02).",
    },
    "006662": {  # Galveston College -- 9 members, at-large by position
        "board_size": 9, "at_large_seats": 9, "smd_seats": 0,
        "smd_district_numbers": [],
        "source_url": "https://gc.edu/about-gc/administration/board-of-regents/index.php",
        "note": "\"Nine members elected at large by the qualified voters of the College "
                "District,\" numbered Position 1-9 (gc.edu/about-gc/administration/"
                "board-of-regents/, fetched 2026-09-02).",
    },
    "029137": {  # San Jacinto Community College District -- 7 members, at-large by position
        "board_size": 7, "at_large_seats": 7, "smd_seats": 0,
        "smd_district_numbers": [],
        "source_url": "https://www.sanjac.edu/about/board-trustees/board-election/",
        "note": "7 members, numbered at-large positions 1-7 (sanjac.edu/about/board-trustees/"
                "board-election/, fetched 2026-09-02).",
    },
}

# Paris Junior College (003601): Education Code 130.0829 elects 2 members
# from EACH of 4 commissioner precincts (8 seats total, precinct is the
# electorate not a 1-seat district) plus 1 at-large seat -- a genuinely
# different shape than parse_district()'s "1 seat per numbered district"
# model, so it isn't a MANUAL_OVERRIDES entry; built directly as its own
# multi-member Posts below (same precedent as Uvalde CISD's 2-seat zone
# Posts in the ISD audit).
PARIS_JC_FICE = "003601"

# Hill College (003573): 12 single-member seats under Texas Education Code
# 130.083, each a "district" named for a town rather than numbered 1-N --
# Hillsboro (4 places), Whitney (3), Itasca (2), Abbott/Bynum/Covington (1
# each). Globally-unique place numbers don't exist (Hillsboro Place 1 and
# Whitney Place 1 are different seats), so this can't use
# build_records()'s numbered-district model either -- built directly, same
# reasoning as Paris JC above.
HILL_COLLEGE_FICE = "003573"
HILL_COLLEGE_DISTRICTS = {
    "Hillsboro": 4, "Whitney": 3, "Itasca": 2,
    "Abbott": 1, "Bynum": 1, "Covington": 1,
}

# Fixed namespace for this script's deterministic organization ids -- distinct
# from the ISD script's namespace so a same-FICE/same-CDN coincidence (never
# expected, THECB FICE and TEA CDN are different numbering spaces entirely)
# can't collide organization ids.
NS = uuid.UUID("6b6f5e1d-6a8e-5b2a-8b0e-1c9d7a4f2e33")

FICE_RE = re.compile(r"FICE (\d{6})")
SLUG_RE = re.compile(r"community_college_district:([a-z0-9-]+)/school$")


def load_jurisdictions():
    """FICE -> {slug, jurisdiction_id, name} for every seeded CCD jurisdiction."""
    by_fice = {}
    for f in JURISDICTIONS_DIR.glob("*-ccd-school.yaml"):
        doc = yaml.safe_load(f.read_text())
        slug_match = SLUG_RE.search(doc["id"])
        fice_match = None
        for src in doc["sources"]:
            m = FICE_RE.search(src.get("note", ""))
            if m:
                fice_match = m.group(1)
                break
        if not slug_match or not fice_match:
            raise ValueError(f"could not parse slug/fice from {f}")
        by_fice[fice_match] = {
            "slug": slug_match.group(1),
            "jurisdiction_id": doc["id"],
            "name": doc["name"],
        }
    return by_fice


def load_bbb_rows():
    with BBB_CSV.open(newline="") as f:
        return list(csv.DictReader(f))


def org_id(fice):
    return f"ocd-organization/{uuid.uuid5(NS, f'organization|{fice}')}"


def existing_ids(kind):
    ids = {}
    for f in (DATA_DIR / kind).glob("*/*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            ids[doc["id"]] = doc
    return ids


def bbb_source_entry(bbb_row):
    return {
        "url": bbb_row["source_url"],
        "note": (
            f"{bbb_row['policy_name']} ({bbb_row['source']}, "
            f"{bbb_row['update_name']}, issued {bbb_row['date_issued']}) -- "
            f"election-method/board-size source. Full text in "
            f"reference/TX Rolling Audit/tx_ccd_bbb_local_2026-09-02.csv."
        ),
        "retrieved": "2026-09-02",
    }


def build_records(fice, jur, source_entry, plan):
    slug = jur["slug"]

    org = {
        "id": org_id(fice),
        "name": f"{jur['name']} Board of Trustees",
        "jurisdiction_id": jur["jurisdiction_id"],
        "identifiers": [{"scheme": "thecb-fice", "identifier": fice}],
        "status": "active",
        "sources": [source_entry],
    }

    posts = []
    if plan["at_large_seats"]:
        posts.append(
            {
                "id": f"{slug}-tx-ccd/trustee-at-large" if plan["smd_seats"] else f"{slug}-tx-ccd/trustee",
                "organization_id": org["id"],
                "title": "Trustee, At-Large" if plan["smd_seats"] else "Trustee",
                "seats": plan["at_large_seats"],
                "identifiers": [],
                "sources": [source_entry],
            }
        )
    for n in plan["smd_district_numbers"]:
        posts.append(
            {
                "id": f"{slug}-tx-ccd/trustee-district-{n}",
                "organization_id": org["id"],
                "title": f"Trustee, District {n}",
                "seats": 1,
                "identifiers": [],
                "sources": [source_entry],
            }
        )
    return org, posts


def build_paris_jc_records(fice, jur, bbb_row):
    """Paris Junior College: Education Code 130.0829 elects 2 members from
    EACH of 4 commissioner precincts (a 2-seat post per precinct, not 1 seat
    per numbered district) plus 1 at-large seat. Hand-built rather than
    forced through build_records()'s 1-seat-per-district model."""
    slug = jur["slug"]
    source_entry = {
        "url": bbb_row["source_url"],
        "note": (
            f"{bbb_row['policy_name']} ({bbb_row['source']}, "
            f"{bbb_row['update_name']}, issued {bbb_row['date_issued']}) -- "
            f"election-method/board-size source (Education Code 130.0829: 2 "
            f"members per commissioner precinct + 1 at-large). Full text in "
            f"reference/TX Rolling Audit/tx_ccd_bbb_local_2026-09-02.csv."
        ),
        "retrieved": "2026-09-02",
    }
    org = {
        "id": org_id(fice),
        "name": f"{jur['name']} Board of Trustees",
        "jurisdiction_id": jur["jurisdiction_id"],
        "identifiers": [{"scheme": "thecb-fice", "identifier": fice}],
        "status": "active",
        "sources": [source_entry],
    }
    posts = [
        {
            "id": f"{slug}-tx-ccd/trustee-at-large",
            "organization_id": org["id"],
            "title": "Trustee, At-Large",
            "seats": 1,
            "identifiers": [],
            "sources": [source_entry],
        }
    ]
    for n in (1, 2, 3, 4):
        posts.append(
            {
                "id": f"{slug}-tx-ccd/trustee-precinct-{n}",
                "organization_id": org["id"],
                "title": f"Trustee, Precinct {n}",
                "seats": 2,
                "identifiers": [],
                "sources": [source_entry],
            }
        )
    return org, posts


def build_hill_college_records(fice, jur, bbb_row):
    """Hill College: 12 single-member seats named by town, not a global
    number -- see HILL_COLLEGE_DISTRICTS above."""
    slug = jur["slug"]
    source_entry = {
        "url": bbb_row["source_url"],
        "note": (
            f"{bbb_row['policy_name']} ({bbb_row['source']}, "
            f"{bbb_row['update_name']}, issued {bbb_row['date_issued']}) -- "
            f"election-method/board-size source (Texas Education Code "
            f"130.083: 12 single-member seats, named by town). Full text in "
            f"reference/TX Rolling Audit/tx_ccd_bbb_local_2026-09-02.csv."
        ),
        "retrieved": "2026-09-02",
    }
    org = {
        "id": org_id(fice),
        "name": f"{jur['name']} Board of Trustees",
        "jurisdiction_id": jur["jurisdiction_id"],
        "identifiers": [{"scheme": "thecb-fice", "identifier": fice}],
        "status": "active",
        "sources": [source_entry],
    }
    posts = []
    for town, place_count in HILL_COLLEGE_DISTRICTS.items():
        town_slug = town.lower()
        for n in range(1, place_count + 1):
            title = f"Trustee, {town} Place {n}" if place_count > 1 else f"Trustee, {town}"
            post_id = (
                f"{slug}-tx-ccd/trustee-{town_slug}-place-{n}"
                if place_count > 1 else f"{slug}-tx-ccd/trustee-{town_slug}"
            )
            posts.append(
                {
                    "id": post_id,
                    "organization_id": org["id"],
                    "title": title,
                    "seats": 1,
                    "identifiers": [],
                    "sources": [source_entry],
                }
            )
    return org, posts


def main():
    write = "--write" in sys.argv[1:]

    jurisdictions = load_jurisdictions()
    bbb_by_fice = {r["thecb_fice"]: r for r in load_bbb_rows()}

    org_ids = existing_ids("organizations")
    post_ids = existing_ids("posts")

    stats = Counter()
    ORGS_DIR.mkdir(parents=True, exist_ok=True)
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    for fice, jur in sorted(jurisdictions.items()):
        bbb_row = bbb_by_fice.get(fice)
        header = HEADER

        if fice == PARIS_JC_FICE:
            org, posts = build_paris_jc_records(fice, jur, bbb_row)
        elif fice == HILL_COLLEGE_FICE:
            org, posts = build_hill_college_records(fice, jur, bbb_row)
        elif fice in CCD_MANUAL_OVERRIDES:
            plan = dict(CCD_MANUAL_OVERRIDES[fice])
            if "source_url" in plan:
                # Resolved from the district's own website, not BBB(LOCAL)
                # text (no TASB page, or a page with no local text on file).
                source_entry = {
                    "url": plan["source_url"],
                    "note": plan["note"],
                    "retrieved": "2026-09-02",
                }
                header = HEADER_OWN_SITE
            else:
                if bbb_row is None:
                    stats["skip_no_bbb_row"] += 1
                    continue
                source_entry = bbb_source_entry(bbb_row)
            org, posts = build_records(fice, jur, source_entry, plan)
        else:
            if bbb_row is None:
                stats["skip_no_bbb_row"] += 1
                continue
            plan = parse_district(fice, bbb_row["local_text"])
            if "skip_reason" in plan:
                stats["skip_unparsed"] += 1
                continue
            org, posts = build_records(fice, jur, bbb_source_entry(bbb_row), plan)

        if org["id"] in org_ids:
            stats["org_existing"] += 1
        else:
            stats["org_new"] += 1
            path = ORGS_DIR / f"{jur['slug']}-tx-ccd-board.yaml"
            if write:
                path.write_text(
                    header + yaml.safe_dump(org, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
                )
            org_ids[org["id"]] = org

        for post in posts:
            existing_doc = post_ids.get(post["id"])
            if existing_doc is not None:
                if existing_doc.get("organization_id") == post["organization_id"]:
                    stats["post_existing"] += 1
                else:
                    stats["post_skipped_id_conflict"] += 1
                    print(f"ID CONFLICT: {post['id']} already claimed by "
                          f"organization_id={existing_doc.get('organization_id')}")
                continue
            stats["post_new"] += 1
            fname = post["id"].replace("/", "-") + ".yaml"
            path = POSTS_DIR / fname
            if write:
                path.write_text(
                    header + yaml.safe_dump(post, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
                )
            post_ids[post["id"]] = post

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded from the TX CCD rolling audit's sourced BBB(LOCAL) election-\n"
    "# structure text by scripts/seed_tx_ccd_organizations_posts.py\n"
    "# (structure only -- see issue #14). Current officeholders are not yet\n"
    "# researched; this covers board size and seat structure only.\n"
)

# For the 8 districts with no TASB/BBB(LOCAL) source at all (see
# CCD_MANUAL_OVERRIDES entries carrying a "source_url"): sourced from each
# district's own official website instead, fetched fresh 2026-09-02.
HEADER_OWN_SITE = (
    "# Seeded from each district's own official website (no TASB/BBB(LOCAL)\n"
    "# source exists for this district) by scripts/seed_tx_ccd_organizations_posts.py\n"
    "# (structure only -- see issue #14). Current officeholders are not yet\n"
    "# researched; this covers board size and seat structure only.\n"
)


if __name__ == "__main__":
    main()
