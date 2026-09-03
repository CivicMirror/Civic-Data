#!/usr/bin/env python3
"""
Structure only: districts tagged Entity Type == "Underground Water
Conservation District" in the Comptroller's SPDPID, individually
researched and confirmed to be governed the same way as the
groundwater_conservation_district: type key's other 39 entities (see
seed_tx_gcd_jurisdictions_orgs_posts.py) -- folded into that same type
key rather than creating a redundant new one, since the Entity Type
bucket distinction turned out to carry no statutory meaning (several
districts in the "Groundwater Conservation District" bucket are
legacy-named "...Underground Water Conservation District" and vice
versa -- see issue #32 comments for both research passes).

Two districts from this same 19-row raw batch are NOT included here:
- Edwards Aquifer Authority -- its own unique enabling act, given its own
  edwards_aquifer_authority: type key (seed_tx_edwards_aquifer_authority.py).
- Real-Edwards Conservation and Reclamation District -- confirmed part of
  the distinct conservation_and_reclamation_district: lineage (Art. XVI
  Sec. 59 / a district-specific special act), added to
  seed_tx_conservation_reclamation_district.py instead.

One district is EXCLUDED entirely, not seeded: Permian Basin Underground
Water Conservation District (Martin County, SPD 103227233). Its own
current website (pbuwcd.com/board-members) uses "Appointing Authority"
column headers naming Martin/Howard counties for all listed seats -- no
"elected" language found there -- even though an older (2005) legislative
bill-analysis document describes an elected structure. Per this audit's
source-priority rule (the entity's own current site over older secondary
documents), treated as APPOINTED and excluded. Flagged for a follow-up
statute check (the enabling act may have been amended since 2005) before
this exclusion is treated as final.

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_gcd_from_uwcd_bucket.py [--write]
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
JUR_DIR = DATA_DIR / "jurisdictions" / "gcd"
ORGS_DIR = DATA_DIR / "organizations" / "gcd"
POSTS_DIR = DATA_DIR / "posts" / "gcd"

RETRIEVED = "2026-09-03"
TYPE_KEY = "groundwater_conservation_district"
COMPTROLLER_NOTE_BASE = (
    "Enumerated via the Texas Comptroller's SPDPID under Entity Type "
    "'Underground Water Conservation District' -- folded into the "
    "groundwater_conservation_district: type key alongside the 39 "
    "districts enumerated under the separate 'Groundwater Conservation "
    "District' Entity Type, since research confirmed that bucket "
    "distinction carries no statutory meaning. Elected status and exact "
    "seat count individually confirmed via this district's own website."
)

NS = uuid.UUID("e6a3c9f2-8d4b-57e1-a2c6-9f3e8b1d5a7c")  # same namespace as the original GCD script

# (name, county, website, spd_id, elected_seats, extra_note)
MINT_ROWS = [
    ("Evergreen Underground Water Conservation District", "Atascosa County", "https://evergreenuwcd.org", "103227003", 8,
     "9-member board total: 8 elected (2 each from Wilson, Frio, Atascosa, Karnes counties) + 1 Governor-appointed. Only the 8 elected seats get a Post here."),
    ("Guadalupe County Groundwater Conservation District", "Guadalupe County", "https://www.gcgcd.org", "103225782", 7, ""),
    ("Hickory Underground Water Conservation District #1", "Mcculloch County", "https://www.hickoryuwcd.org", "103225532", 5, ""),
    ("Hill Country Underground Water Conservation District", "Gillespie County", "https://hcuwcd.org", "103226753", 5, ""),
    ("Live Oak Underground Water Conservation District", "Live Oak County", "https://louwcd.org", "103226388", 5,
     "District's website throws a certificate hostname-mismatch error as of this research -- content confirmed via search/cache; worth a human check that hosting is correctly configured."),
    ("Llano Estacado Underground Water Conservation District", "Gaines County", None, "103226385", 5, ""),
    ("McMullen Groundwater Conservation District", "Mcmullen County", "https://mcmullengcd.org", "103226463", 5,
     "Elected status high-confidence but not 100% textually confirmed (the site's Directors page did not load directly; inferred from management-plan/precinct-term data)."),
    ("Menard County Underground Water District", "Menard County", "https://www.menardcountyuwd.org", "103226936", 5, ""),
    ("Mesa Underground Water Conservation District", "Dawson County", "https://mesauwcd.org", "103225693", 5,
     "Official domain 301-redirects permanently to a Google Sites page (sites.google.com/view/mesa-uwcd/home) -- content confirmed there, but worth noting the domain no longer serves its own content."),
    ("San Patricio County Groundwater Conservation District", "San Patricio County", "https://spcgcd.org", "103226464", 7,
     "District's website throws a certificate hostname-mismatch error as of this research -- content confirmed via search/cache; worth a human check that hosting is correctly configured."),
    ("Sandy Land Underground Water Conservation District", "Yoakum County", "https://www.sandylandwater.com", "103225531", 5,
     "Created under Art. XVI Sec. 59, Texas Constitution per a 71st Legislature act, but confirmed to follow the standard Ch. 36-style elected GCD governance pattern despite the constitutional citation."),
    ("Santa Rita Underground Water Conservation District", "Reagan County", "https://www.santaritauwcd.org", "103225654", 5, ""),
    ("South Plains Underground Water Conservation District", "Terry County", "https://www.spuwcd.org", "103225729", 5, ""),
    ("Sterling County Underground Water Conservation District", "Sterling County", "http://www.sterlinguwcd.org/", "103225548", 5, ""),
    ("Sutton County Underground Water Conservation District", "Sutton County", "https://www.suttoncountyuwcd.org", "103225521", 5, "Part of Groundwater Management Area (GMA) 7."),
    ("Wes-Tex Groundwater Conservation District", "Nolan County", "http://www.westexgcd.org/", "103226850", 9,
     "Moderate confidence on elected status: the site's own director-listing header ('Date Elected/Appt.') is ambiguous and doesn't unambiguously confirm the method per seat, though no seat names an appointing authority and the precinct-based structure matches the standard elected pattern seen across other Ch. 36-style districts."),
]

NOISE_RE = re.compile(
    r"\b(groundwater conservation district|underground water( conservation( and supply)?)? district)\b",
    re.IGNORECASE,
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

    slug_seen = {}
    for name, county, website, spd_id, seats, extra_note in MINT_ROWS:
        slug = slugify(name)
        if slug in slug_seen:
            stats["skip_slug_collision"] += 1
            print(f"SKIPPED (slug collision with {slug_seen[slug]!r}, needs manual resolution): {name!r}")
            continue
        slug_seen[slug] = name

        source_entry = {
            "url": website or "https://spdpid.comptroller.texas.gov/",
            "note": f"{name} (SPD Public ID {spd_id}) -- {county}. {COMPTROLLER_NOTE_BASE}"
            + (f" {extra_note}" if extra_note else ""),
            "retrieved": RETRIEVED,
        }

        jid = f"ocd-jurisdiction/country:us/state:tx/{TYPE_KEY}:{slug}/sewer"
        if jid not in jur_ids:
            jur = {
                "id": jid,
                "name": name,
                "state": "tx",
                "division_id": f"ocd-division/country:us/state:tx/{TYPE_KEY}:{slug}",
                "classification": "sewer",
                "identifiers": [{"scheme": "tx-spdpid", "identifier": spd_id}],
                "sources": [source_entry],
            }
            write_file(JUR_DIR / f"{slug}-sewer.yaml", jur, write)
            stats["jurisdiction_new"] += 1
            jur_ids[jid] = jur
        else:
            stats["jurisdiction_existing"] += 1

        oid = f"ocd-organization/{uuid.uuid5(NS, f'organization|{slug}')}"
        if oid not in org_ids:
            org = {
                "id": oid,
                "name": f"{name} Board of Directors",
                "jurisdiction_id": jid,
                "identifiers": [],
                "status": "active",
                "sources": [source_entry],
            }
            write_file(ORGS_DIR / f"{slug}-gcd-board.yaml", org, write)
            stats["org_new"] += 1
            org_ids[oid] = org
        else:
            stats["org_existing"] += 1

        for n in range(1, seats + 1):
            pid = f"{slug}-tx-gcd/director-{n}"
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
            write_file(POSTS_DIR / f"{slug}-tx-gcd-director-{n}.yaml", post, write)
            stats["post_new"] += 1
            post_ids[pid] = post

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    print(f"mint_rows: {len(MINT_ROWS)} of 19 raw rows in this bucket (Edwards Aquifer Authority + Real-Edwards seeded separately; Permian Basin excluded -- see module docstring)")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded from the TX GCD rolling audit's Underground-Water-Conservation-\n"
    "# District-bucket follow-up (issue #32, Phase 1) by\n"
    "# scripts/seed_tx_gcd_from_uwcd_bucket.py. Structure only -- current\n"
    "# officeholders are not yet researched. Folded into the same\n"
    "# groundwater_conservation_district: type key as the districts seeded\n"
    "# by seed_tx_gcd_jurisdictions_orgs_posts.py -- see this script's\n"
    "# module docstring.\n"
)


if __name__ == "__main__":
    main()
