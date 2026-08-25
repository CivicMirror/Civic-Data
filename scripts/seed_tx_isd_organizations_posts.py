#!/usr/bin/env python3
"""
Phase 3 (structure only): generate Organization (Board of Trustees) and Post
(trustee seat) records for TX ISDs from the seat plan
reference/TX Rolling Audit/tx_isd_parse_structure.py derives from each
district's sourced BBB(LOCAL) text.

Scope: this generates STRUCTURE ONLY -- board size and how seats split
between an at-large bloc and single-member-district seats. It does not
research or create People/Membership records for current officeholders;
that is separate future work requiring its own sourcing (TEA's officeholder
export, per the earlier BBB(LOCAL) extraction pass's notes), not something
derivable from the election-structure text this script reads.

Seat modeling, matching this repo's own precedent (data/us/ma/posts/state/
*-house.yaml: one Post per single-member state house district, `seats: 1`
each, all sharing one Organization for "the House"):
  - A seat is its own Post (seats: 1) when its ELECTORATE differs from every
    other seat's -- i.e. every single-member-district/area seat.
  - Seats share ONE Post (seats: N) when the electorate is the same for all
    of them -- i.e. any at-large bloc, regardless of whether ballot
    administration numbers them by position (at_large_by_position) or not
    (plain at_large, at_large_cumulative). post.schema.json has no field for
    election method or ballot numbering; membership.seat (see GLOSSARY.md)
    is where "Position 3" would be recorded per-officeholder later, not here.
  - Hybrid districts get one at-large Post (seats: k) plus one Post per SMD
    seat (seats: 1 each).

Excludes:
  - The 4 confirmed-appointed districts (tx_isd_appointed_exclusions_2026-08-25.csv)
    and Harris County Dept of Education (excluded_non_isd) -- neither has a
    jurisdiction file to hang an Organization off of; both already excluded
    upstream of this script.
  - The 5 districts tx_isd_parse_structure.py flags for individual research
    (South Texas, Houston, Uvalde, Irving, Victoria ISDs) -- no seat plan
    exists for these yet, so nothing to template.
Expected: 1,012 seeded ISD jurisdictions - 4 confirmed-appointed - 5 unparsed
= 1,003 districts get an Organization + Post set.

ID collisions: Audit_Instructions.md (lines 37-44) warns ISDs are not
guaranteed collision-free against county/place slugs sharing a name, and
that a bare `<slug>-tx/<office-slug>` post-id convention doesn't disambiguate
-- hence `<slug>-tx-isd/<office-slug>` (e.g. `houston-tx-isd/trustee-district-3`,
Audit_Instructions.md:198). This script builds a global id index over every
existing data/us/tx/organizations/**/*.yaml and posts/**/*.yaml id (same
fix as the Millbury Select Board collision found seeding MA v27) and skips
with a counter on collision rather than trusting the qualifier blindly.

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_isd_organizations_posts.py [--write]
"""
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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "reference" / "TX Rolling Audit"))
from tx_isd_parse_structure import parse_district, EXCLUDED_TAGS  # noqa: E402

import csv  # noqa: E402

BBB_CSV = REPO / "reference" / "TX Rolling Audit" / "tx_isd_bbb_local_2026-08-24.csv"

# Fixed namespace for this script's deterministic organization ids -- stable
# across re-runs as long as (namespace, cdn) doesn't change.
NS = uuid.UUID("2b3f6b0a-3f0a-5c1e-9f7a-3a7b6e8d9c10")

CDN_RE = re.compile(r"County-District Number (\d{6})")
SLUG_RE = re.compile(r"school_district:([a-z0-9-]+)/school$")


def load_jurisdictions():
    """CDN -> {slug, jurisdiction_id, name} for every seeded ISD jurisdiction."""
    by_cdn = {}
    for f in JURISDICTIONS_DIR.glob("*.yaml"):
        doc = yaml.safe_load(f.read_text())
        slug_match = SLUG_RE.search(doc["id"])
        cdn_match = None
        for src in doc["sources"]:
            m = CDN_RE.search(src.get("note", ""))
            if m:
                cdn_match = m.group(1)
                break
        if not slug_match or not cdn_match:
            raise ValueError(f"could not parse slug/cdn from {f}")
        by_cdn[cdn_match] = {
            "slug": slug_match.group(1),
            "jurisdiction_id": doc["id"],
            "name": doc["name"],
        }
    return by_cdn


def load_bbb_rows():
    with BBB_CSV.open(newline="") as f:
        return list(csv.DictReader(f))


def org_id(cdn):
    return f"ocd-organization/{uuid.uuid5(NS, f'organization|{cdn}')}"


def existing_ids(kind):
    """id -> doc, for every existing record. Storing the doc (not just the
    path) means a record registered mid-run (dry or not) can be collision-
    checked without reading a file that --write hasn't created yet."""
    ids = {}
    for f in (DATA_DIR / kind).glob("*/*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            ids[doc["id"]] = doc
    return ids


def build_records(cdn, jur, bbb_row, plan):
    slug = jur["slug"]
    source_entry = {
        "url": bbb_row["source_url"],
        "note": (
            f"{bbb_row['policy_name']} ({bbb_row['source']}, "
            f"{bbb_row['update_name']}, issued {bbb_row['date_issued']}) -- "
            f"election-method/board-size source. Full text in "
            f"reference/TX Rolling Audit/tx_isd_bbb_local_2026-08-24.csv."
        ),
        "retrieved": "2026-08-24",
    }

    org = {
        "id": org_id(cdn),
        "name": f"{jur['name']} Board of Trustees",
        "jurisdiction_id": jur["jurisdiction_id"],
        "identifiers": [{"scheme": "tea-cdn", "identifier": cdn}],
        "status": "active",
        "sources": [source_entry],
    }

    posts = []
    if plan["at_large_seats"]:
        posts.append(
            {
                "id": f"{slug}-tx-isd/trustee-at-large" if plan["smd_seats"] else f"{slug}-tx-isd/trustee",
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
                "id": f"{slug}-tx-isd/trustee-district-{n}",
                "organization_id": org["id"],
                "title": f"Trustee, District {n}",
                "seats": 1,
                "identifiers": [],
                "sources": [source_entry],
            }
        )
    return org, posts


def main():
    write = "--write" in sys.argv[1:]

    jurisdictions = load_jurisdictions()
    bbb_by_cdn = {r["tea_cdn"]: r for r in load_bbb_rows()}

    org_ids = existing_ids("organizations")
    post_ids = existing_ids("posts")

    stats = Counter()
    ORGS_DIR.mkdir(parents=True, exist_ok=True)
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    for cdn, jur in sorted(jurisdictions.items()):
        bbb_row = bbb_by_cdn.get(cdn)
        if bbb_row is None:
            stats["skip_no_bbb_row"] += 1
            continue
        if bbb_row["heuristic_structure"] in EXCLUDED_TAGS:
            stats["skip_excluded_tag"] += 1
            continue

        plan = parse_district(cdn, bbb_row["local_text"])
        if "skip_reason" in plan:
            stats["skip_unparsed"] += 1
            continue

        org, posts = build_records(cdn, jur, bbb_row, plan)

        # org["id"] is a uuid5 keyed to this CDN, so it's effectively
        # collision-proof by construction -- a plain existing-id check is
        # sufficient (still checked globally: existing_ids() indexes every
        # data/us/tx/organizations/**/*.yaml, not just this script's own
        # school/ subdir).
        if org["id"] in org_ids:
            stats["org_existing"] += 1
        else:
            stats["org_new"] += 1
            path = ORGS_DIR / f"{jur['slug']}-tx-isd-board.yaml"
            if write:
                path.write_text(
                    HEADER + yaml.safe_dump(org, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
                )
            org_ids[org["id"]] = org

        # Post ids are human-readable strings (<slug>-tx-isd/<office-slug>) --
        # this is the real collision surface Audit_Instructions.md warns
        # about (ISDs sharing a name with a city/county), same failure mode
        # as the Millbury Select Board Member collision found seeding MA v27.
        # Checked globally across every data/us/tx/posts/**/*.yaml, not just
        # this script's own school/ subdir.
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
                    HEADER + yaml.safe_dump(post, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
                )
            post_ids[post["id"]] = post

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded from the TX ISD rolling audit's sourced BBB(LOCAL) election-\n"
    "# structure text by scripts/seed_tx_isd_organizations_posts.py (Phase 3,\n"
    "# structure only -- see issue #13). Current officeholders are not yet\n"
    "# researched; this covers board size and seat structure only.\n"
)


if __name__ == "__main__":
    main()
