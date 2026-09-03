#!/usr/bin/env python3
"""
Structure only: generate Jurisdiction, Organization (Board of Directors),
and Post (elected director seat) records for a curated subset of Texas
Water Improvement Districts (WID) -- see issue #32, Phase 1.

Source: reference/TX Rolling Audit/tx_wid_raw_2026-09-03.csv, the "Special
Districts (Non-MUD)" sheet of TX_Municipalities.xlsx filtered to Entity
Type == "Water Improvement District" (22 raw rows).

Structure confirmed against statute before templating, same discipline as
WCID/FWSD: Water Code Sec. 55.101 fixes the board at "five directors"
unconditionally -- no special-law override clause found.

UNLIKE WCID/FWSD/SUD, this type's raw 22 rows are curated by hand rather
than filtered by a name-vs-Entity-Type regex, because this batch is far
messier than the other three (only ~23% of rows cleanly match "Water
Improvement District" by name) and includes a genuine data-integrity
anomaly (a row literally named "Rabhicks property management llc" -- not
a government entity at all) plus a real multi-district division that
needed individual research to resolve, not a mechanical regex. See issue
#32 comments for the full per-row reasoning. Only MINT_ROWS below are
seeded; every other raw row is deliberately excluded, for one of these
reasons:

- No "water" token in the name at all (Chambers County Improvement
  District No. 2; Harris County Improvement District #18; Meadow Road
  Improvement District; Port O'Connor Improvement District [+ its
  "Defined Area" sibling]; Waller County Improvement District #2) --
  ambiguous type, held back.
- Named as a Water Control and Improvement District (Chapter 51), not a
  Water Improvement District (Chapter 55) -- "Harris County Water
  Control and Improvement District #74" and "Travis County Water
  Control and Improvement District #18". Neither appears in the WCID
  raw sheet under its own Entity Type, so these are reclassified into
  the WCID type key and seeded by seed_tx_wcid_reclassified_from_wid.py
  instead of this script, using the water_control_improvement_district:
  jurisdiction type key.
- "Rabhicks property management llc" -- not a government entity, a
  clear Comptroller data-entry anomaly. Excluded entirely, not held for
  future research.
- "Comal County Master Water Improvement District" and its #1A/#2/
  No.1B/No.1D siblings -- relationship to each other (shared board? each
  independent?) could not be confirmed from a quick source check, unlike
  the "No. 3" cluster below. Held back pending individual research.
- "Comal County Water Improvement District no. 3" (lowercase, INACTIVE,
  2024) -- the pre-division predecessor entity, confirmed dissolved by
  its own 2024 Order Dividing District Into Three Districts (see the
  "No. 3 Master District" entry below). Historical, not currently
  governed; excluded.

Two rows in the raw sheet ARE included after individual research:
- "Comal County Water Improvement District No. 3 Master District"
  appears 3 times (one with an incorrect county, "Harris County" --
  a Comptroller data error, same underlying entity) -- confirmed via
  mayfairwids.org to be one active 5-director board, successor to the
  dissolved "No. 3" above. All 3 SPD Public IDs recorded as identifiers;
  the most current ACTIVE row's website used as the source.
- "Comal County Water Improvement District No. 3A" -- confirmed via the
  same source to be a SEPARATE legal entity from the Master District
  (created by the Master district's 2024 division order) with its own
  independent 5-director board, not a shared board with the Master
  district.

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_wid_jurisdictions_orgs_posts.py [--write]
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
JUR_DIR = DATA_DIR / "jurisdictions" / "wid"
ORGS_DIR = DATA_DIR / "organizations" / "wid"
POSTS_DIR = DATA_DIR / "posts" / "wid"

RETRIEVED = "2026-09-03"
TYPE_KEY = "water_improvement_district"
DIRECTOR_COUNT = 5
COMPTROLLER_NOTE = (
    "Enumerated via the Texas Comptroller's Special Purpose District Public "
    "Information Database (SPDPID); board structure per Water Code Sec. "
    "55.101 (5 directors, fixed, no special-law override clause found) and "
    "Sec. 49.103 (staggered 4-year terms, general public qualified-voter "
    "franchise per Sec. 49.1025). Not yet individually verified against "
    "this district's own governing documents beyond the research noted in "
    "issue #32."
)

NS = uuid.UUID("b8e2a4f6-1d9c-5e73-8a4b-3f6c9e1d5a8b")

# (name, county, website, [spd_ids], extra_note)
MINT_ROWS = [
    (
        "Brown County Water Improvement District #1",
        "Brown County",
        "https://bcwid.org",
        ["103225864"],
        "",
    ),
    (
        "El Paso County Tornillo Water Improvement District",
        "El Paso County",
        "https://www.epctwid.com",
        ["103227579"],
        "",
    ),
    (
        "Loving County Water Improvement District #1",
        "Loving County",
        "http://www.lovingcowid.org",
        ["103226772"],
        "",
    ),
    (
        "Comal County Water Improvement District No. 3 Master District",
        "Comal County",
        "https://www.mayfairwids.org/ccwid-3a/about/",
        ["103228488", "103228489", "103228681"],
        (
            "Successor to the dissolved 'Comal County Water Improvement "
            "District no. 3' (SPD ID 103228206, INACTIVE, excluded from this "
            "seed), per that district's own 2024 Order Dividing District "
            "Into Three Districts. One of the 3 raw SPD IDs (103228488) was "
            "filed under the wrong county ('Harris County') in the "
            "Comptroller's data -- a data-entry error, not a separate "
            "entity; the district is physically in Comal County per the "
            "other 2 filings and its own website."
        ),
    ),
    (
        "Comal County Water Improvement District No. 3A",
        "Comal County",
        "https://www.mayfairwids.org/ccwid-3a/about/",
        ["103228475"],
        (
            "Confirmed via mayfairwids.org to be a legally separate entity "
            "from 'Comal County Water Improvement District No. 3 Master "
            "District' (created by that district's 2024 division order), "
            "with its own independent 5-director board -- not shared "
            "governance with the Master district."
        ),
    ),
]

NOISE_RE = re.compile(r"\bwater improvement district\b", re.IGNORECASE)


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

    for name, county, website, spd_ids, extra_note in MINT_ROWS:
        slug = slugify(name)
        source_entry = {
            "url": website,
            "note": f"{name} (SPD Public ID {', '.join(spd_ids)}) -- {county}. {COMPTROLLER_NOTE}"
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
                "identifiers": [{"scheme": "tx-spdpid", "identifier": s} for s in spd_ids],
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
            write_file(ORGS_DIR / f"{slug}-wid-board.yaml", org, write)
            stats["org_new"] += 1
            org_ids[oid] = org
        else:
            stats["org_existing"] += 1

        for n in range(1, DIRECTOR_COUNT + 1):
            pid = f"{slug}-tx-wid/director-{n}"
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
            write_file(POSTS_DIR / f"{slug}-tx-wid-director-{n}.yaml", post, write)
            stats["post_new"] += 1
            post_ids[pid] = post

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    print(f"held_back_or_excluded: {22 - len(MINT_ROWS)} of 22 raw rows (see module docstring)")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded from the TX WID rolling audit (issue #32, Phase 1) by\n"
    "# scripts/seed_tx_wid_jurisdictions_orgs_posts.py. Structure only --\n"
    "# current officeholders are not yet researched. Board size/terms\n"
    "# templated from Water Code Sec. 55.101/49.103, not yet individually\n"
    "# verified against this district's own governing documents beyond the\n"
    "# research noted in issue #32.\n"
)


if __name__ == "__main__":
    main()
