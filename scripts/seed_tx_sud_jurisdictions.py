#!/usr/bin/env python3
"""
Jurisdiction only: generate Jurisdiction records for Texas Special Utility
Districts (SUD) -- see issue #32, Phase 1.

Source: reference/TX Rolling Audit/tx_sud_raw_2026-09-03.csv, the "Special
Districts (Non-MUD)" sheet of TX_Municipalities.xlsx filtered to Entity
Type == "Special Utility District" (66 raw rows from the Texas
Comptroller's SPDPID enumeration).

Unlike WCID (issue #32's first seeded type, Water Code Sec. 51.071's fixed
5-director board), Water Code Sec. 65.101 sets an SUD board at "not less
than five and not more than 11 directors" -- the exact number is set
per-district (at creation, per Sec. 65.022/65.103) and is NOT recoverable
from the general chapter alone. Terms may be concurrent or staggered but
cannot exceed three years (Sec. 65.103), also set per district. Because
guessing a specific number would silently assert something unverified
(see feedback_verify_elected_status_claims / the WCID lesson in issue #32),
this script mints ONLY the Jurisdiction record for each confirmed SUD --
NOT the Board of Directors Organization or its Posts. Organization/Post
creation is separate future work, gated on finding each district's actual
board size (most likely from the district's own site or its TCEQ
creation order), same "flag the gap, don't work around it" discipline
Audit_Instructions.md sets for missing jurisdiction prerequisites.

Franchise/scope already confirmed elected + general-public (not a
restricted landowner franchise) via the same Sec. 49 family provisions
checked for WCID.

Same name-vs-Entity-Type check run before templating (per the WCID
lesson): of 66 raw rows, 9 have a name containing no
"special ut(i)lity district"/"SUD" token at all and are held back,
including "Sabine River Authority of Texas" (a River Authority, a
wholly different type the user is researching separately) and several
that read as their own utility/authority special-act entities rather
than Ch. 65 SUDs. "Lilly Grove Speciality Utility District" is a
spelling variant of "Special" (not a real type mismatch) and IS included.

Three exact-duplicate names (Ables Springs, Talty, West Gregg) each
appear twice in the raw sheet as an ACTIVE/INACTIVE pair with the same
name/county/website but different SPD Public IDs -- a Comptroller
re-registration artifact, not a genuine multi-entity split like WCID's
Plum Creek case. Resolved by preferring the ACTIVE row and recording
both SPD IDs as identifiers.

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_sud_jurisdictions.py [--write]
"""
import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
JUR_DIR = DATA_DIR / "jurisdictions" / "sud"
RAW_CSV = REPO / "reference" / "TX Rolling Audit" / "tx_sud_raw_2026-09-03.csv"

RETRIEVED = "2026-09-03"
TYPE_KEY = "special_utility_district"
COMPTROLLER_NOTE = (
    "Enumerated via the Texas Comptroller's Special Purpose District Public "
    "Information Database (SPDPID). Water Code Sec. 65.101 sets the board "
    "at 5-11 directors but the exact number is set per-district, not by "
    "the general chapter -- NOT asserted here. This jurisdiction record is "
    "structure-prerequisite only; Board of Directors Organization/Post "
    "records are separate future work gated on finding this district's "
    "actual board size."
)

HELD_BACK_NAMES = {
    "Clear Lake City Water Authority",
    "Commodore Cove Improvement District",
    "Cypresswood Utility District",
    "Dallas County Utility and Reclamation District",
    "Greater Texoma Utility Authority",
    "Irving Flood Control District Section #1",
    "Irving Flood Control District Section #3",
    "Robstown Utility System",
    "Sabine River Authority of Texas",  # a River Authority -- user researching that type separately
}

NOISE_RE = re.compile(r"\bspecial ut(?:i|)lity district\b", re.IGNORECASE)


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

    with RAW_CSV.open(newline="") as f:
        rows = list(csv.DictReader(f))

    jur_ids = existing_ids("jurisdictions")
    stats = Counter()

    by_name = defaultdict(list)
    for r in rows:
        by_name[r["name"]].append(r)

    for r in rows:
        if r["name"] in HELD_BACK_NAMES:
            stats["anomaly_held_back"] += 1
            continue

    slug_seen = {}
    for name, group in by_name.items():
        if name in HELD_BACK_NAMES:
            print(f"HELD BACK (needs individual research, not seeded): {name} -- {group[0]['county']}")
            continue

        if len(group) > 1:
            active = [g for g in group if g["status"] == "ACTIVE"]
            primary = active[0] if active else max(group, key=lambda g: g["report_year"] or "")
            spd_ids = sorted({g["spd_id"] for g in group})
            stats["dedup_active_inactive_pair"] += 1
        else:
            primary = group[0]
            spd_ids = [primary["spd_id"]]

        slug = slugify(name)
        if slug in slug_seen:
            stats["skip_slug_collision"] += 1
            print(f"SKIPPED (slug collision with {slug_seen[slug]!r}, needs manual resolution): {name!r}")
            continue
        slug_seen[slug] = name

        jid = jurisdiction_id(slug)
        if jid in jur_ids:
            stats["jurisdiction_existing"] += 1
            continue

        source_entry = {
            "url": primary["website"] or "https://spdpid.comptroller.texas.gov/",
            "note": f"{name} (SPD Public ID {', '.join(spd_ids)}) -- {primary['county']}. {COMPTROLLER_NOTE}",
            "retrieved": RETRIEVED,
        }
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

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded from the TX SUD rolling audit (issue #32, Phase 1) by\n"
    "# scripts/seed_tx_sud_jurisdictions.py. Jurisdiction only -- Board of\n"
    "# Directors Organization/Post records are NOT created here because\n"
    "# Water Code Sec. 65.101 sets the board at 5-11 directors per-district,\n"
    "# not a fixed number, and this district's actual board size has not\n"
    "# yet been individually verified.\n"
)


if __name__ == "__main__":
    main()
