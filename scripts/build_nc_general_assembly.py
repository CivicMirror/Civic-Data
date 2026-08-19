#!/usr/bin/env python3
"""
Generate jurisdiction/organization/post triples for the North Carolina
General Assembly (House + Senate), driven by openstates/people's NC
legislature bulk data (github.com/openstates/people/tree/main/data/nc/
legislature) -- itself sourced from ncleg.gov's official member data. Same
role for NC's state legislature that build_ma_general_court.py plays for
MA's.

Unlike Mayor's offices, House/Senate districts are geographic and don't
already have a jurisdiction on file (the existing Census-sourced municipal/
county jurisdictions are place- and county-based, not legislative-district-
based), so this DOES create new jurisdictions, under a new "state" tier
(data/us/nc/{jurisdictions,organizations,posts}/state/) alongside the
existing federal/municipal/county tiers.

NC districts are plain numbers ('38', '12', ...) -- no county-compound
naming the way MA's are ('10th Bristol'), so district slugs are just the
number itself.

One jurisdiction+organization+post per CURRENT district (120 House + 50
Senate seats as of the source snapshot).

Idempotent by id AND by filename -- never overwrites.

Usage: python3 build_nc_general_assembly.py [--write]
Without --write, prints a dry-run summary only.
"""
import json
import re
import sys
import unicodedata
import urllib.request
import uuid
from datetime import UTC, datetime
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "nc"

GITHUB_LISTING_URL = "https://api.github.com/repos/openstates/people/contents/data/nc/legislature"
CACHE_DIR = Path("/tmp/nc_openstates_legislature")

TODAY = datetime.now(UTC).date().isoformat()

HEADER = (
    "# Machine-generated from openstates/people's NC legislature bulk data\n"
    "# (github.com/openstates/people/tree/main/data/nc/legislature, itself sourced\n"
    "# from ncleg.gov's official member data) by scripts/build_nc_general_assembly.py.\n"
)

CHAMBER_INFO = {
    "lower": {
        "division_type": "sldl",
        "org_name": "North Carolina House of Representatives",
        "title": "State Representative",
        "post_prefix": "nc-house",
        "file_suffix": "house",
    },
    "upper": {
        "division_type": "sldu",
        "org_name": "North Carolina State Senate",
        "title": "State Senator",
        "post_prefix": "nc-senate",
        "file_suffix": "senate",
    },
}

SOURCES = [
    {
        "url": "https://www.ncleg.gov/Members/MemberTable/H",
        "note": "Official North Carolina General Assembly member directory -- primary source openstates/people cites for current membership.",
        "retrieved": TODAY,
    },
    {
        "url": "https://github.com/openstates/people/tree/main/data/nc/legislature",
        "note": "openstates/people bulk legislator data -- used here for current district enumeration.",
        "retrieved": TODAY,
    },
]


def uid(seed):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))


def slugify(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def fetch_legislature_files():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached = list(CACHE_DIR.glob("*.yml"))
    if cached:
        return cached

    req = urllib.request.Request(GITHUB_LISTING_URL, headers={"User-Agent": "civic-data-build-script"})
    with urllib.request.urlopen(req, timeout=30) as r:
        listing = json.load(r)

    for entry in listing:
        url = entry["download_url"]
        out = CACHE_DIR / entry["name"]
        with urllib.request.urlopen(url, timeout=30) as r:
            out.write_bytes(r.read())
    return list(CACHE_DIR.glob("*.yml"))


def current_districts():
    """{('lower'|'upper'): set of district names} from current (no end_date) roles."""
    districts = {"lower": set(), "upper": set()}
    for path in fetch_legislature_files():
        doc = yaml.safe_load(path.read_text())
        roles = [r for r in doc.get("roles", []) if not r.get("end_date")]
        if not roles:
            continue
        r = roles[-1]
        if r["type"] in districts:
            districts[r["type"]].add(r["district"])
    return districts


def build_records(chamber, district):
    info = CHAMBER_INFO[chamber]
    slug = slugify(district)

    jurisdiction_id = f"ocd-jurisdiction/country:us/state:nc/{info['division_type']}:{slug}/legislature"
    jurisdiction = {
        "id": jurisdiction_id,
        "name": f"District {district} ({info['org_name']} delegation)",
        "state": "nc",
        "division_id": f"ocd-division/country:us/state:nc/{info['division_type']}:{slug}",
        "classification": "legislature",
        "government_form": f"single-member district ({info['org_name']})",
        "sources": SOURCES,
    }

    org_seed = f"{info['post_prefix']}:{slug}"
    org_id = f"ocd-organization/{uid(org_seed)}"
    organization = {
        "id": org_id,
        "name": f"{info['org_name']} -- District {district}",
        "jurisdiction_id": jurisdiction_id,
        "identifiers": [],
        "sources": SOURCES,
    }

    post = {
        "id": f"{info['post_prefix']}-{slug}/state-{info['title'].lower().replace('state ', '')}",
        "organization_id": org_id,
        "title": info["title"],
        "seats": 1,
        "identifiers": [],
        "sources": SOURCES,
    }

    return {
        "jurisdictions": (jurisdiction, f"{slug}-{info['file_suffix']}.yaml"),
        "organizations": (organization, f"{slug}-{info['file_suffix']}.yaml"),
        "posts": (post, f"{slug}-{info['file_suffix']}.yaml"),
    }


class Recorder:
    def __init__(self, write):
        self.write = write
        self.stats = {}

    def handle(self, kind, doc, filename):
        path = DATA_DIR / kind / "state" / filename
        singular = kind.rstrip("s") if kind != "jurisdictions" else "jurisdiction"

        if path.exists():
            existing = yaml.safe_load(path.read_text()) or {}
            if existing.get("id") == doc["id"]:
                self.stats[f"{singular}_existing"] = self.stats.get(f"{singular}_existing", 0) + 1
            else:
                self.stats[f"{singular}_skipped_filename_conflict"] = (
                    self.stats.get(f"{singular}_skipped_filename_conflict", 0) + 1
                )
            return

        self.stats[f"{singular}_new"] = self.stats.get(f"{singular}_new", 0) + 1
        if self.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            text = HEADER + yaml.safe_dump(
                doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000
            )
            path.write_text(text)


def main():
    write = "--write" in sys.argv[1:]
    districts = current_districts()
    rec = Recorder(write)

    for chamber in ("lower", "upper"):
        for district in sorted(districts[chamber], key=lambda d: int(d) if d.isdigit() else d):
            triples = build_records(chamber, district)
            for kind, (doc, filename) in triples.items():
                rec.handle(kind, doc, filename)

    print("==================== SUMMARY ====================")
    print(f"House (lower) districts: {len(districts['lower'])}")
    print(f"Senate (upper) districts: {len(districts['upper'])}")
    for k in sorted(rec.stats):
        print(f"{k}: {rec.stats[k]}")


if __name__ == "__main__":
    main()
