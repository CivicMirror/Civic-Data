#!/usr/bin/env python3
"""
Structure only: generate Jurisdiction, Organization (Board of Directors),
and Post (elected director seat) records for a curated subset of Texas
Groundwater Conservation Districts (GCD) -- see issue #32, Phase 1.

Source: 59 raw rows from the "Special Districts (Non-MUD)" sheet of
TX_Municipalities.xlsx, Entity Type == "Groundwater Conservation
District", individually researched via each district's own website
(background agent, issue #32 comment) because Water Code Ch. 36's
elected-5-to-11-director default is frequently overridden by individual
GCDs' own special acts -- unlike WCID/FWSD/WID/Irrigation's unconditional
statutory defaults. GCD names are frequently legacy/aquifer-based
("...Underground Water Conservation District" predating a 1995 renaming,
or a purely regional/watershed name) rather than literally saying
"Groundwater Conservation District" -- that's normal for this type, not
a red flag, so (unlike WCID/FWSD/WID/Irrigation) no name-vs-Entity-Type
regex filter was applied here; every one of the 59 raw rows was
individually researched instead.

Research found 39 of 59 districts ELECTED (seat counts individually
confirmed, ranging from 5 to 12 -- do not assume a uniform number for
this type) and 20 APPOINTED by one or more counties'/cities' governing
bodies -- excluded from this seed entirely (structure noted in
reference/TX Rolling Audit/Special_District_Type_Keys.md, no
Organization/Post records, same discipline as the 3 appointed Drainage
Districts and the ESD population-based appointed default). 0 districts
were left undetermined.

NOTE ON VERIFYING SUBAGENT OUTPUT: the research agent's own summary line
mis-stated the split as "34 elected / 25 appointed" -- counting its own
per-district table directly gives 39 elected / 20 appointed instead
(59 total either way). MINT_ROWS below is built from the per-district
table, not the (wrong) summary line -- always verify a subagent's
top-line summary against its own detailed data before building on it.

APPOINTED_EXCLUDED (not seeded, listed here for the commit/registry
record only): Blanco Pedernales GCD (5, County Judge/Commissioners Court
-- ambiguous per its own research note, originally elected via a 2001
confirmation election but currently tagged appointed), Bluebonnet GCD
(16, Austin/Grimes/Walker/Waller County Commissioners Courts), Brazos
Valley GCD (8, Robertson/Brazos County Commissioners Courts + Bryan/
College Station City Councils), Brush Country GCD (9, Jim Hogg/Jim
Wells/Brooks County Commissioners Courts), Gateway GCD (12, Hardeman/
Childress/Cottle/Foard/King/Motley County Commissioners Courts), Lost
Pines GCD (10, Bastrop/Lee County Judges/Commissioners Courts), Lower
Trinity GCD (5, Polk/San Jacinto County Commissioners Courts +
municipalities -- district also covers part of Liberty County per the
research, though the raw sheet lists only Polk), Mid-East Texas GCD (9,
Madison/Leon/Freestone County Commissioners Courts), North Texas GCD (9,
Denton/Cooke + a third county's Commissioners Courts), Northern Trinity
GCD (5, Tarrant County Commissioners Court + County Judge), Pineywoods
GCD (7, Angelina/Nacogdoches County Commissioners Courts + Lufkin/
Nacogdoches City Councils), Post Oak Savannah GCD (10, Milam/Burleson
County Commissioners Courts), Prairielands GCD (8, 4 member counties'
Commissioners Courts including Johnson County), Presidio County UWCD (5,
Presidio County Commissioners Court), Red River GCD (7, Fannin County
Commissioners Court + City of Sherman + other Grayson municipalities/
special districts), Reeves County GCD (7, Reeves County Commissioners
Court), Rolling Plains GCD (9, 3 member counties' Commissioners Courts),
Southeast Texas GCD (13, multiple counties'/cities' governing bodies),
Southern Trinity GCD (5, McLennan County Commissioners Court + County
Judge), Upper Trinity GCD (8, Hood/Montague/Parker/Wise County
Commissioners Courts).

Two anomalies noted but not blocking: "Uvalde County Underground
Conservation District" in the raw sheet is missing "Water" from its
official name ("...Underground Water Conservation District") -- the
full official name is used below. "Hays Trinity GCD"'s 2024 annual
report lists 6 named board members against its 5-seat statutory board;
seeded with the statutory 5, noted for a future roster check.

Idempotent by id -- never overwrites an existing file with the same id.

Usage: python3 seed_tx_gcd_jurisdictions_orgs_posts.py [--write]
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
    "Enumerated via the Texas Comptroller's Special Purpose District Public "
    "Information Database (SPDPID). Water Code Ch. 36 sets a default "
    "elected board of 5-11 directors, but individual GCDs frequently "
    "override this by special act -- elected status and exact seat count "
    "individually confirmed via this district's own website, not assumed "
    "from the chapter default."
)

NS = uuid.UUID("e6a3c9f2-8d4b-57e1-a2c6-9f3e8b1d5a7c")

# (name, county, website, spd_id, seats, extra_note)
MINT_ROWS = [
    ("Barton Springs/Edwards Aquifer Conservation District", "Travis County", "https://www.bseacd.org", "103226372", 5, ""),
    ("Bee Groundwater Conservation District", "Bee County", "https://beegcd.com", "103226461", 7, ""),
    ("Brazoria County Groundwater Conservation District", "Brazoria County", "https://www.bcgroundwater.org", "103227175", 5, ""),
    ("Calhoun County Groundwater Conservation District", "Calhoun County", "https://www.calhouncountygcd.org", "103226663", 5,
     "Initially appointed as temporary directors; converted to elected after confirmation election."),
    ("Central Texas Groundwater Conservation District", "Burnet County", "https://www.centraltexasgcd.org", "103225632", 5, ""),
    ("Clearwater Underground Water Conservation District", "Bell County", "https://cuwcd.org", "103225793", 5, ""),
    ("Coastal Bend Groundwater Conservation District", "Wharton County", "https://www.cbgcd.com", "103226386", 5, ""),
    ("Coastal Plains Groundwater Conservation District", "Matagorda County", "https://www.coastalplainsgcd.com", "103226384", 7, ""),
    ("Colorado County Groundwater Conservation District", "Colorado County", "https://www.ccgcd.net", "103225544", 7, ""),
    ("Cow Creek Groundwater Conservation District", "Kendall County", "https://www.ccgcd.org", "103225595", 5, ""),
    ("Crockett County Groundwater Conservation District", "Crockett County", "https://www.crockettcountygcd.com", "103227502", 5, ""),
    ("Duval County Groundwater Conservation District", "Duval County", "https://duvalgcd.com", "103226716", 5, ""),
    ("Fayette County Groundwater Conservation District", "Fayette County", "https://www.fayettecountygroundwater.com", "103225529", 5, ""),
    ("Goliad County Groundwater Conservation District", "Goliad County", "https://www.goliadcogcd.org", "103227523", 7, ""),
    ("Gonzales County Underground Water Conservation District", "Gonzales County", "https://www.gcuwcd.org", "103226410", 5, ""),
    ("Hays Trinity Groundwater Conservation District", "Hays County", "https://www.haysgroundwater.com", "103225820", 5,
     "2024 annual report lists 6 named board members against this 5-seat statutory board -- seeded with the statutory 5 director posts; worth a future roster check."),
    ("Headwaters Groundwater Conservation District #8", "Kerr County", "https://hgcd.org", "103225652", 5, ""),
    ("Hemphill County Underground Water Conservation District", "Hemphill County", "https://www.hemphiluwcd.org", "103227001", 5, ""),
    ("High Plains Underground Water Conversation District #1", "Lubbock County", "https://www.hpwd.org", "103227365", 5, ""),
    ("Irion County Water Conservation District", "Irion County", "http://www.irionwcd.org", "103225597", 5, ""),
    ("Kimble County Groundwater Conservation District", "Kimble County", "https://www.kimblecountygcd.org", "103228221", 5, ""),
    ("Lipan-Kickapoo Water Conservation District", "Tom Green County", "https://www.lipan-kickapoo.org", "103225584", 7,
     "Multi-county district (Concho, Runnels, Tom Green counties)."),
    ("Lone Star Groundwater Conservation District", "Montgomery County", "https://www.lonestargcd.org", "103225613", 7,
     "Converted from a 9-member appointed board to a 7-member elected board via HB 1982 (2017)."),
    ("Lone Wolf Groundwater Conservation District", "Mitchell County", "https://lonewolfgwcd.org", "103226209", 5, ""),
    ("Mesquite Groundwater Conservation District", "Collingsworth County", "https://mesquitegcd.gov", "103227893", 8,
     "Legacy name predates current branding (formerly 'Collingsworth County Underground Water...'); covers Collingsworth, Hall, and part of Childress counties."),
    ("Middle Pecos Groundwater Conservation District", "Pecos County", "https://middlepecosgcd.org", "103225577", 11, ""),
    ("Middle Trinity Groundwater Conservation District", "Erath County", "https://middletrinitygcd.org", "103225522", 12,
     "Multi-county district (Bosque, Comanche, Coryell, Erath counties, 3 seats each) -- the raw sheet attributes it to Erath County alone."),
    ("North Plains Groundwater Conservation District", "Moore County", "https://www.northplainsgcd.org", "103225872", 7, ""),
    ("Panhandle Groundwater Conservation District", "Carson County", "https://www.pgcd.us/", "103226191", 9, ""),
    ("Panola County Groundwater Conservation District", "Panola County", "https://www.pcgcd.org", "103225883", 9, ""),
    ("Pecan Valley Groundwater Conservation District", "Dewitt County", "https://www.pvgcd.org", "103226367", 5, ""),
    ("Plateau Underground Water Conservation and Supply District", "Schleicher County", "https://www.plateauuwcsd.com", "103225610", 5, ""),
    ("Refugio Groundwater Conservation District", "Refugio County", "https://www.rgcd.org", "103226391", 5, ""),
    ("Rusk County Groundwater Conservation District", "Rusk County", "https://www.rcgcd.org", "103225709", 9, ""),
    ("Southwestern Travis County Groundwater Conservation District", "Travis County", "https://swtcgcd.com", "103228313", 7, ""),
    ("Texana Groundwater Conservation District", "Jackson County", "https://www.texanagcd.org", "103226382", 7, ""),
    ("Trinity Glen Rose Groundwater Conservation District", "Bexar County", "https://www.trinityglenrose.com", "103226160", 5,
     "District also extends into Kendall and Comal counties -- the raw sheet attributes it to Bexar County alone."),
    ("Uvalde County Underground Water Conservation District", "Uvalde County", "https://uvaldecountyuwcd.org", "103226090", 8,
     "Raw SPDPID sheet lists this district's name as 'Uvalde County Underground Conservation District' (missing 'Water'); the official name, used here, is 'Uvalde County Underground Water Conservation District'."),
    ("Victoria County Groundwater Conservation District", "Victoria County", "https://www.vcgcd.org", "103225904", 5, ""),
]

NOISE_RE = re.compile(
    r"\b(groundwater conservation district|underground water conservation( and supply)? district|"
    r"water conservation district)\b",
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

    slug_seen = {}
    for name, county, website, spd_id, seats, extra_note in MINT_ROWS:
        slug = slugify(name)
        if slug in slug_seen:
            stats["skip_slug_collision"] += 1
            print(f"SKIPPED (slug collision with {slug_seen[slug]!r}, needs manual resolution): {name!r}")
            continue
        slug_seen[slug] = name

        source_entry = {
            "url": website,
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
    print(f"mint_rows: {len(MINT_ROWS)} of 59 raw rows (20 confirmed appointed, excluded -- see module docstring)")
    if not write:
        print("\n(dry run -- pass --write to create files)")


HEADER = (
    "# Seeded from the TX GCD rolling audit (issue #32, Phase 1) by\n"
    "# scripts/seed_tx_gcd_jurisdictions_orgs_posts.py. Structure only --\n"
    "# current officeholders are not yet researched. Elected status and\n"
    "# seat count individually confirmed per district via its own website,\n"
    "# not assumed from the Water Code Ch. 36 default -- see this script's\n"
    "# module docstring and issue #32 for the research trail.\n"
)


if __name__ == "__main__":
    main()
