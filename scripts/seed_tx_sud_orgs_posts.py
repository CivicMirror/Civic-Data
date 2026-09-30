#!/usr/bin/env python3
"""
Structure only: generate Organization (Board of Directors) and Post
(elected director seat) records for the Texas Special Utility Districts
(SUD) whose Jurisdiction records were already seeded by
scripts/seed_tx_sud_jurisdictions.py -- see issue #32, Phase 1.

That earlier script deliberately stopped at jurisdictions because Water
Code Sec. 65.101 sets an SUD board at "not less than five and not more
than 11" directors, fixed per district rather than by the general
chapter. This script supplies the missing per-district seat counts.

HOW SEAT COUNTS WERE DETERMINED (2026-09-30)

The Comptroller's SPDPID board-member self-report
(reference/TX Rolling Audit/spdpid_related_party_boardmembers_2026-09-28.csv)
covers 56 of the 57 SUD SPD IDs, but it is NOT used as the seat-count
source here: seed_tx_spdpid_officeholders.py only auto-imports a district
when the reported headcount equals the number of minted Posts, so deriving
the Post count from that same headcount would make its safety gate pass
by construction. It is also demonstrably incomplete for some SUDs (Diana
SUD reports 3 people, below Sec. 65.101's floor of 5).

Instead, every district's own website was checked for the board, in
this order of preference:
  1. an explicit seat statement ("governed by a seven-member Board",
     "comprised of nine Directors", numbered Places/Positions 1..N,
     "three seats up each year" x 3-year terms, an election order)
  2. the current published roster headcount
The SPDPID headcount was then compared only as a cross-check. Where the
site's count and SPDPID disagree, the site count is used and the
mismatch is left for the officeholder import to flag. Full per-district
working table (count, basis, SPDPID comparison) is in SEAT_COUNTS below.

Seat counts found range 5-9; boards of 6 and 8 are valid under Sec.
65.101 (5-11, no odd-number requirement).

AGUA SUD is the one district with single-member director districts
(Director - District 1..7 on its own board page); its posts are titled
and id'd by district rather than as an undifferentiated at-large pool.

HELD BACK (jurisdiction stays, no board/posts minted):
  - HMW Special Utility District -- no roster or seat statement found on
    its site or in its posted meeting notices.
  - Tyler County Special Utility District -- same; site's board page 404s
    and meeting notices don't name directors.
  - Wylie Northeast Special Utility District -- site roster shows 5, but
    SPDPID 2026 lists 6 including a different President (Jimmy Beach) who
    is absent from the site; can't tell a 5-seat board from a 6-seat board
    with a vacancy/stale page without another source.

EXCLUDED -- DEFUNCT:
  - Marilee Special Utility District -- consolidated into Mustang SUD by
    TCEQ on 2022-09-15 under Water Code Sec. 65.723-65.726 (consolidation
    election 2021-11-02; PUC Project No. 54131 updated CCN No. 10150 to
    Mustang SUD). Its jurisdiction file is removed in the same commit as
    this script; its last SPDPID filing is 2021 and marileewater.com now
    serves Mustang SUD's site.

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_sud_orgs_posts.py [--write]
"""
import sys
import uuid
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
JUR_DIR = DATA_DIR / "jurisdictions" / "sud"
ORGS_DIR = DATA_DIR / "organizations" / "sud"
POSTS_DIR = DATA_DIR / "posts" / "sud"

RETRIEVED = "2026-09-30"

NS = uuid.UUID("5d2b8e4f-7a1c-5b39-8e6d-4c2a9f1b3e7d")

# jurisdiction file stem -> (seats, basis, source url, spdpid latest-year headcount or None)
SEAT_COUNTS = {
    "ables-springs-sewer": (7, "current roster", "https://myh2odistrict.com/board-members", 7),
    "agua-sewer": (7, "single-member Director Districts 1-7 listed on the board page", "https://aguasud.com/about-us/board-of-directors/", 7),
    "bear-creek-sewer": (7, "current roster with term expirations", "https://www.bearcreeksud.com/board-members", 7),
    "bright-star-salem-sewer": (5, "current roster", "https://brightstarwater.com/board-members", 5),
    "buena-vista-bethel-sewer": (5, "seats up for election listed as 1 (2026) + 2 (2027) + 2 (2028), matching the roster", "https://bvbsud.com/board-members", 5),
    "caddo-basin-sewer": (7, "current roster with term expirations", "https://www.caddobasin.com/board-members", 7),
    "cash-sewer": (9, "current roster", "https://www.cashwater.org/board-members", 9),
    "chalk-hill-sewer": (7, "current roster", "https://www.chalkhillsud.org/board-members", 7),
    "college-mound-sewer": (7, "current roster", "https://www.collegemoundwater.com/board-members", 7),
    "combined-consumers-sewer": (5, "current roster", "https://www.ccsud.com/board-members", 5),
    "county-line-sewer": (7, "numbered Places 1-7 on the board page", "https://clsud.com/board-of-directors/", 7),
    "crystal-clear-sewer": (7, "numbered Positions 1-7 with terms on the board-elections page (one currently vacant)", "https://www.crystalclearsud.org/board-elections", 7),
    "diana-sewer": (7, "current roster (SPDPID 2025 self-report lists only 3 officers)", "https://www.dianasud.org/board-members", 3),
    "east-central-sewer": (9, "current roster with terms, three expiring each year", "https://www.eastcentralsudtx.gov/district/district.php", 9),
    "east-fork-sewer": (5, "current roster", "https://www.eastforksud.com/board-meetings/", 5),
    "east-medina-county-sewer": (7, "current roster", "https://www.emcsud.dst.tx.us/board-members", 7),
    "fort-griffin-sewer": (7, "current roster", "https://www.fortgriffinsud.net/board-members", 7),
    "four-way-sewer": (6, "current roster", "https://www.fourwaywater.com/board-members", 6),
    "gastonia-scurry-sewer": (7, "current roster with term expirations", "https://www.gssud.com/board-members", 7),
    "green-valley-sewer": (7, "district describes itself as governed by a seven-member Board of Directors", "https://gvsud.org/district/board-of-directors/", 7),
    "johnson-county-sewer": (7, "current roster", "https://www.jcsud.com/195/JCSUD-Board-of-Directors", 7),
    "jonah-water-sewer": (9, "board page states the Board is comprised of nine Directors, three elected annually", "https://www.jonahwater.com/board-members", 9),
    "lake-kiowa-sewer": (7, "current roster", "https://LKSUD.ORG/board-members", 7),
    "lilly-grove-speciality-utility-district-sewer": (7, "numbered Positions 1-7 with term expirations", "https://www.lillygrovesud.com/board-members", 7),
    "luella-sewer": (5, "current roster", "https://LuellaSUD.org/board-members-1", 5),
    "macbee-sewer": (9, "current roster", "https://macbeewater.com/board-members", 9),
    "maxwell-sud-sewer": (9, "2022 order calling a directors election elects three directors (Sec. 65.103 caps terms at 3 years -> 9 seats); matches SPDPID 2026 (9). District site roster shows 8 and carries a 2022 alert, likely stale", "https://maxwellwsc.com/board-members", 9),
    "mustang-sewer": (9, "current roster with term expirations", "https://www.mustangwater.com/board-of-directors", 9),
    "nevada-sewer": (5, "current roster", "https://nevadawater.org/board-members", 5),
    "new-hope-sewer": (5, "current roster", "https://newhopesud.myruralwater.com/board-members", 5),
    "parker-county-sewer": (7, "district describes itself as governed by a seven member Board of Directors", "https://www.parkercountywater.com/board-members", 7),
    "phelps-sewer": (5, "current roster", "https://PhelpsWater.net/board-members", 5),
    "porter-sewer": (7, "current roster", "https://portersud.com/board-members", 7),
    "riverside-sewer": (5, "current roster", "https://riversidewatersupply.com/board-members", 5),
    "rockett-sewer": (9, "three positions elected each year for three-year terms, matching the roster", "https://www.rockettwater.com/board-members", 9),
    "rose-hill-sewer": (5, "district describes itself as governed by a five-member Board of Directors", "https://www.rhsud.com/board-members", 5),
    "shady-grove-sewer": (5, "current roster", "https://www.shadygrovesud.com/board-members", 5),
    "south-rains-sewer": (7, "current roster", "https://www.southrainssud.com/board-members", 7),
    "southwest-fannin-sewer": (5, "current roster with terms", "https://www.swfanninsud.org/board-members", 5),
    "springs-hill-sewer": (6, "current roster", "https://springshill.org/board-members", 6),
    "stephens-regional-sewer": (7, "numbered Places 1-7 on the board page", "https://www.stephensregionalsud.com/board-members", 7),
    "talty-sewer": (5, "current roster with terms", "https://www.taltysud.com/Contact", 5),
    "tri-county-sewer": (7, "current roster", "https://tricountysud.com/board-members", 7),
    "tri-sewer": (9, "current roster", "https://www.trisud.com/directors.html", 9),
    "tryon-road-sewer": (6, "current roster", "https://www.tryonroadsud.org/board-members", 6),
    "two-way-sewer": (9, "current roster (SPDPID 2026 self-report lists 8)", "https://www.twowaysud.com/board-members", 8),
    "walnut-creek-sewer": (5, "current roster", "https://walnutcreeksud.org/board-members", 5),
    "wellborn-sewer": (9, "board page states nine at-large seats, three expiring each year", "https://www.wellbornsud.com/board-members-and-elections", 9),
    "west-gregg-sewer": (6, "current roster", "https://westgreggsud.com/board-members", 6),
    "west-wise-sewer": (7, "current roster (no SPDPID board-member rows at all)", "https://www.westwisesud.com/board-members", None),
}

SINGLE_MEMBER_DISTRICTS = {"agua-sewer"}

HELD_BACK = {
    "hmw-sewer": "no roster or seat statement found",
    "tyler-county-sewer": "no roster or seat statement found",
    "wylie-northeast-sewer": "site roster 5 vs SPDPID 6 with a different President -- ambiguous",
}

EXCLUDED_DEFUNCT = {"marilee-sewer"}


def org_id(slug):
    return f"ocd-organization/{uuid.uuid5(NS, f'organization|{slug}')}"


def existing_ids(kind):
    ids = set()
    base = DATA_DIR / kind
    if base.exists():
        for f in base.glob("**/*.yaml"):
            doc = yaml.safe_load(f.read_text()) or {}
            if "id" in doc:
                ids.add(doc["id"])
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
    org_ids = existing_ids("organizations")
    post_ids = existing_ids("posts")
    stats = Counter()

    stems = {f.stem for f in JUR_DIR.glob("*.yaml")}
    unaccounted = stems - set(SEAT_COUNTS) - set(HELD_BACK) - EXCLUDED_DEFUNCT
    missing = set(SEAT_COUNTS) - stems
    if unaccounted or missing:
        sys.exit(f"jurisdiction/table mismatch: unaccounted={sorted(unaccounted)} missing={sorted(missing)}")

    for stem, (seats, basis, url, spdpid_n) in sorted(SEAT_COUNTS.items()):
        if not 5 <= seats <= 11:
            sys.exit(f"{stem}: {seats} seats is outside Water Code Sec. 65.101's 5-11 range")
        jur = yaml.safe_load((JUR_DIR / f"{stem}.yaml").read_text())
        slug = stem[: -len("-sewer")]
        spd_id = next(i["identifier"] for i in jur["identifiers"] if i["scheme"] == "tx-spdpid")
        spdpid_txt = (
            f"SPDPID self-reported headcount for the latest report year: {spdpid_n}."
            if spdpid_n is not None else "No SPDPID board-member self-report rows exist for this district."
        )
        source_entry = {
            "url": url,
            "note": (
                f"{jur['name']} (SPD Public ID {spd_id}). Water Code Sec. 65.101 sets an SUD board at 5-11 "
                f"directors, fixed per district. Board size of {seats} taken from the district's own website "
                f"({basis}), not from the general chapter or the SPDPID self-report. {spdpid_txt}"
            ),
            "retrieved": RETRIEVED,
        }

        oid = org_id(slug)
        if oid not in org_ids:
            org = {
                "id": oid,
                "name": f"{jur['name']} Board of Directors",
                "jurisdiction_id": jur["id"],
                "identifiers": [],
                "status": "active",
                "sources": [source_entry],
            }
            write_file(ORGS_DIR / f"{slug}-sud-board.yaml", org, write)
            stats["org_new"] += 1
            org_ids.add(oid)
        else:
            stats["org_existing"] += 1

        smd = stem in SINGLE_MEMBER_DISTRICTS
        for n in range(1, seats + 1):
            kind, title = ("district", f"Director, District {n}") if smd else ("director", f"Director, Position {n}")
            pid = f"{slug}-tx-sud/{kind}-{n}"
            if pid in post_ids:
                stats["post_existing"] += 1
                continue
            post = {
                "id": pid,
                "organization_id": oid,
                "title": title,
                "seats": 1,
                "identifiers": [],
                "sources": [source_entry],
            }
            write_file(POSTS_DIR / f"{slug}-tx-sud-{kind}-{n}.yaml", post, write)
            stats["post_new"] += 1
            post_ids.add(pid)

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    print(f"minted: {len(SEAT_COUNTS)}, held back: {len(HELD_BACK)}, excluded defunct: {len(EXCLUDED_DEFUNCT)}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded from the TX SUD rolling audit (issue #32, Phase 1) by\n"
    "# scripts/seed_tx_sud_orgs_posts.py. Structure only. Board size\n"
    "# individually confirmed from the district's own website, not assumed\n"
    "# from Water Code Sec. 65.101's 5-11 range -- see the script docstring.\n"
)


if __name__ == "__main__":
    main()
