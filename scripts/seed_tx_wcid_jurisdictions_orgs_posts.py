#!/usr/bin/env python3
"""
Structure only: generate Jurisdiction, Organization (Board of Directors),
and Post (elected director seat) records for Texas Water Control and
Improvement Districts (WCID) -- see issue #32, Phase 1.

Source: reference/TX Rolling Audit/tx_wcid_raw_2026-09-03.csv, the "Special
Districts (Non-MUD)" sheet of TX_Municipalities.xlsx filtered to Entity
Type == "Water Control and Improvement District" (167 raw rows from the
Texas Comptroller's SPDPID enumeration).

Elected-vs-appointed and franchise scope already confirmed in issue #32's
Phase 0/Phase 1 comments: Water Code Sec. 51.071 fixes the board at five
directors unconditionally (no special-law override clause, unlike several
other special-district types in this audit); Sec. 49.103 (Provisions
Applicable to All Districts) sets staggered four-year terms; Sec. 49.1025
confirms the franchise is the district's general qualified (registered)
voters, not a restricted landowner franchise like SWCD's (issue #27,
closed out of scope). Seats are at-large -- no statutory subdivision into
precincts/places for this district type.

WCID districts do not map 1:1 onto an existing county the way CADs do (a
WCID's service area is a sub-county area determined by its own creation
petition, same situation ISDs and SWCDs already hit) -- every WCID gets
its own jurisdiction file, using the water_control_improvement_district:
type key (see reference/TX Rolling Audit/Special_District_Type_Keys.md;
full snake_case word, not the "WCID" abbreviation, per that registry's
naming rule). classification = "sewer" (the schema's water/utility-district
enum value, previously unused anywhere in the dataset).

Two known data anomalies, found and resolved during Phase 1 research
(see issue #32 comments) BEFORE this script runs -- do not attempt to
regenerate this resolution from the raw CSV automatically:

- "Plum Creek Conservation District" (Caldwell County) appears twice in
  the raw sheet under two different SPD Public IDs (103227489, 103228185)
  with otherwise identical name/county/website/status. Confirmed via the
  district's own site (pccd.org) to be ONE legal entity with a 6-member
  board apportioned 2 Hays County / 4 Caldwell County directors -- not
  the generic 5-director at-large template. Handled as a hand-authored
  override below, not the generic per-row loop.
- "Angelina and Nacogdoches Counties Water Control and Improvement
  District No. 1" is listed under "Rusk County" in the raw sheet, but its
  own reservoir (Lake Striker) straddles the Rusk/Cherokee county line --
  neither the row's county nor the district's own name reliably states
  its territory. HELD BACK from this pass entirely (not seeded with any
  jurisdiction) pending individual research; do not guess its boundary.

Officeholder research is separate future work, not started here.

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_wcid_jurisdictions_orgs_posts.py [--write]
"""
import csv
import re
import sys
import unicodedata
import uuid
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
JUR_DIR = DATA_DIR / "jurisdictions" / "wcid"
ORGS_DIR = DATA_DIR / "organizations" / "wcid"
POSTS_DIR = DATA_DIR / "posts" / "wcid"
RAW_CSV = REPO / "reference" / "TX Rolling Audit" / "tx_wcid_raw_2026-09-03.csv"

RETRIEVED = "2026-09-03"
TYPE_KEY = "water_control_improvement_district"
COMPTROLLER_NOTE = (
    "Enumerated via the Texas Comptroller's Special Purpose District Public "
    "Information Database (SPDPID); board structure per Water Code Sec. "
    "51.071 (5 directors, fixed, no special-law override clause found) and "
    "Sec. 49.103 (staggered 4-year terms, general public qualified-voter "
    "franchise per Sec. 49.1025). Not yet individually verified against this "
    "district's own governing documents beyond the name/county checks noted "
    "in issue #32; a district-specific special act overriding board size "
    "would not be caught by this pass."
)

# Fixed namespace for this script's deterministic organization ids.
NS = uuid.UUID("7a1c9e2d-4b6f-58a3-9c7e-2d5f8a1b4c9e")

ANOMALY_NAMES = {
    "Plum Creek Conservation District",  # hand-authored below, not held back
}

# Held back entirely (not seeded): names containing no "water control" /
# "WCID" / "water and control" / "improvment"[sic] token at all, found by
# systematically checking name-vs-type agreement across the whole raw sheet
# (issue #32 comment, 2026-09-03) after Angelina-Nacogdoches surfaced the
# first instance. ~20% of the raw 167 rows. Several are plausible Water
# Code Ch. 51/53 conversions that kept an old charter name (FWSD-named
# entries; Ch. 51 explicitly allows FWSD<->WCID conversion) and would very
# likely template fine -- but at least two ("...Municipal Utility
# District...") look like outright MUD misclassifications that must not be
# folded into this WCID/#32 batch at all (MUD is out of scope, tracked
# under #11), and "Montgomery County Drainage District #10" looks like an
# actual Drainage District (Water Code Ch. 56, 3-director default, not
# WCID's 5) misfiled under this Entity Type. Individual verification
# required per name before any of these get a structure record.
HELD_BACK_NAMES = {
    "Alpha Ranch Fresh Water Supply District #1",
    "Angelina and Nacogdoches Counties Water Control and Improvement District #1",  # cross-county boundary uncertain
    "Benbrook Water Authority",
    "Brookfield Fresh Water Supply District #1",
    "Castleman Creek Watershed Association",
    "Crane County Water District",
    "Denton County Fresh Water Supply District #1-H",
    "Denton County Fresh Water Supply District #10",
    "Denton County Fresh Water Supply District No. 12",
    "Far Hills Utility District",
    "Franklin County Water District",
    "Galveston Water Supply and Improvement District #19",
    "Harris County Improvement District #12",
    "Harris County Municipal Utility District #91",  # likely a MUD, out of #32's scope entirely -- verify
    "Hidalgo County Water Improvement District #3",
    "Inverness Forest Improvement District",
    "Kaufman County Fresh Water Supply District #1-A",
    "Kaufman County Fresh Water Supply District #1-D",
    "Kaufman County Fresh Water Supply District No. 1-E",
    "Kaufman County Fresh Water Supply District No. 1-F",
    "Lazy River Improvement District",
    "Lazy W Conservation District",
    "Midland County Utility District",
    "Montgomery County Drainage District #10",  # likely a Drainage District (Ch. 56), not WCID
    "Mustang Ridge Municipal Utility District",  # likely a MUD, out of #32's scope entirely -- verify
    "North Montague County Water Supply District",
    "Red Bluff Water Power Control District",
    "Southmost Regional Water Authority",
    "Tarrant Regional Water District",  # large regional entity, almost certainly its own special act
    "Tattor Road Municipal District",
    "Upper Jasper County Water Authority",
    "West Central Texas Municipal Water District",
    "Zavala-Dimmit Counties Improvement #1",
}

NOISE_RE = re.compile(
    r"\b(water control (?:and|&) improvement district|county)\b", re.IGNORECASE
)


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


def mint_district(slug, name, county_note, website, spd_ids, director_count, extra_note, write, stats, jur_ids, org_ids, post_ids):
    source_entry = {
        "url": website or "https://spdpid.comptroller.texas.gov/",
        "note": f"{name} (SPD Public ID {', '.join(spd_ids)}) -- {county_note}. {COMPTROLLER_NOTE}" + (f" {extra_note}" if extra_note else ""),
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
        write_file(ORGS_DIR / f"{slug}-wcid-board.yaml", org, write)
        stats["org_new"] += 1
        org_ids[oid] = org
    else:
        stats["org_existing"] += 1

    for n in range(1, director_count + 1):
        pid = f"{slug}-tx-wcid/director-{n}"
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
        write_file(POSTS_DIR / f"{slug}-tx-wcid-director-{n}.yaml", post, write)
        stats["post_new"] += 1
        post_ids[pid] = post


def main():
    write = "--write" in sys.argv[1:]

    with RAW_CSV.open(newline="") as f:
        rows = list(csv.DictReader(f))

    jur_ids = existing_ids("jurisdictions")
    org_ids = existing_ids("organizations")
    post_ids = existing_ids("posts")

    stats = Counter()

    # Plum Creek Conservation District -- hand-authored override (see module
    # docstring): one entity, two SPD IDs, 6-director board apportioned
    # 2 Hays / 4 Caldwell, not the generic 5-director at-large template.
    plum_creek_rows = [r for r in rows if r["name"] == "Plum Creek Conservation District"]
    if plum_creek_rows:
        spd_ids = sorted({r["spd_id"] for r in plum_creek_rows})
        slug = slugify(plum_creek_rows[0]["name"])
        mint_district(
            slug=slug,
            name=plum_creek_rows[0]["name"],
            county_note="spans Hays and Caldwell Counties (6-director board: 2 from Hays, 4 from Caldwell, per the district's own site)",
            website=plum_creek_rows[0]["website"],
            spd_ids=spd_ids,
            director_count=6,
            extra_note=(
                "Two SPD Public IDs in the Comptroller's raw enumeration resolved to "
                "this single entity after confirming via pccd.org that it is one "
                "legal district, not two -- both IDs recorded as identifiers rather "
                "than picking one arbitrarily. Board apportionment (2 Hays/4 Caldwell) "
                "means the generic Sec. 51.071 5-director at-large template does not "
                "apply here; posts are 6 undifferentiated director seats rather than "
                "county-apportioned Place seats because this repo doesn't yet have a "
                "source enumerating the county split by named seat -- a refinement "
                "for later officeholder research, not this structure pass."
            ),
            write=write,
            stats=stats,
            jur_ids=jur_ids,
            org_ids=org_ids,
            post_ids=post_ids,
        )
        stats["anomaly_plum_creek_handled"] += 1

    held_back = [r for r in rows if r["name"] in HELD_BACK_NAMES]
    for r in held_back:
        stats["anomaly_held_back"] += 1
        print(f"HELD BACK (needs individual research, not seeded): {r['name']} -- {r['county']}")

    generic_rows = [r for r in rows if r["name"] not in ANOMALY_NAMES and r["name"] not in HELD_BACK_NAMES]

    slug_seen = {}
    for r in generic_rows:
        slug = slugify(r["name"])
        if slug in slug_seen:
            stats["skip_slug_collision"] += 1
            print(f"SKIPPED (slug collision with {slug_seen[slug]!r}, needs manual resolution): {r['name']!r}")
            continue
        slug_seen[slug] = r["name"]

        mint_district(
            slug=slug,
            name=r["name"],
            county_note=r["county"],
            website=r["website"],
            spd_ids=[r["spd_id"]],
            director_count=5,
            extra_note=(
                "Status per Comptroller's latest filing: " + r["status"] + "."
                if r["status"] and r["status"] != "ACTIVE"
                else ""
            ),
            write=write,
            stats=stats,
            jur_ids=jur_ids,
            org_ids=org_ids,
            post_ids=post_ids,
        )

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded from the TX WCID rolling audit (issue #32, Phase 1) by\n"
    "# scripts/seed_tx_wcid_jurisdictions_orgs_posts.py. Structure only --\n"
    "# current officeholders are not yet researched. Board size/terms\n"
    "# templated from Water Code Sec. 51.071/49.103, not yet individually\n"
    "# verified against this district's own governing documents beyond the\n"
    "# name/county anomaly checks noted in issue #32.\n"
)


if __name__ == "__main__":
    main()
