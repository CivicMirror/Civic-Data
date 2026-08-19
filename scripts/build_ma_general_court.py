#!/usr/bin/env python3
"""
Generate jurisdiction/organization/post triples for the Massachusetts
General Court (House + Senate), driven by openstates/people's MA legislature
bulk data (github.com/openstates/people/tree/main/data/ma/legislature) --
itself sourced from malegislature.gov's official API. This plays the same
role for MA's state legislature that unitedstates/congress-legislators plays
for federal Congress.

Unlike Mayor's offices, House/Senate districts are geographic and don't
already have a jurisdiction on file (the existing Census-sourced municipal/
county jurisdictions are place- and county-based, not legislative-district-
based), so this DOES create new jurisdictions, under a new "state" tier
(data/us/ma/{jurisdictions,organizations,posts}/state/) alongside the
existing federal/municipal/county tiers.

One jurisdiction+organization+post per CURRENT district (158 House + 40
Senate seats as of the source snapshot -- 2 House seats show no current
occupant in the source and are skipped, same as any other current-only,
officeholder-driven generator in this repo). District ids use the OCD
convention for state legislative districts (sldl = state legislative
district, lower; sldu = upper) since these are geographic single-member
districts, structurally the same shape as build_federal_orgs.py's House
districts -- NOT modeled like the federal Senate's per-state/per-class
posts, since MA Senate seats are elected by district, not statewide.

Idempotent by id AND by filename -- never overwrites.

Usage: python3 build_ma_general_court.py [--write]
Without --write, prints a dry-run summary only.
"""
import json
import re
import sys
import urllib.request
import uuid
from datetime import UTC, datetime
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "ma"

GITHUB_LISTING_URL = "https://api.github.com/repos/openstates/people/contents/data/ma/legislature"
CACHE_DIR = Path("/tmp/ma_openstates_legislature")

TODAY = datetime.now(UTC).date().isoformat()

HEADER = (
    "# Machine-generated from openstates/people's MA legislature bulk data\n"
    "# (github.com/openstates/people/tree/main/data/ma/legislature, itself sourced\n"
    "# from malegislature.gov's official API) by scripts/build_ma_general_court.py.\n"
)

CHAMBER_INFO = {
    "lower": {
        "division_type": "sldl",
        "org_name": "Massachusetts House of Representatives",
        "title": "State Representative",
        "post_prefix": "ma-house",
        "file_suffix": "house",
    },
    "upper": {
        "division_type": "sldu",
        "org_name": "Massachusetts State Senate",
        "title": "State Senator",
        "post_prefix": "ma-senate",
        "file_suffix": "senate",
    },
}

SOURCES = [
    {
        "url": "https://malegislature.gov/api/GeneralCourts/193/LegislativeMembers",
        "note": "Official Massachusetts General Court API -- primary source openstates/people cites for current membership.",
        "retrieved": TODAY,
    },
    {
        "url": "https://github.com/openstates/people/tree/main/data/ma/legislature",
        "note": "openstates/people bulk legislator data -- used here for current district enumeration.",
        "retrieved": TODAY,
    },
]


def uid(seed):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))


def slugify(name):
    s = name.lower()
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

    jurisdiction_id = f"ocd-jurisdiction/country:us/state:ma/{info['division_type']}:{slug}/legislature"
    jurisdiction = {
        "id": jurisdiction_id,
        "name": f"{district} district ({info['org_name']} delegation)",
        "state": "ma",
        "division_id": f"ocd-division/country:us/state:ma/{info['division_type']}:{slug}",
        "classification": "legislature",
        "government_form": f"single-member district ({info['org_name']})",
        "sources": SOURCES,
    }

    org_seed = f"{info['post_prefix']}:{slug}"
    org_id = f"ocd-organization/{uid(org_seed)}"
    organization = {
        "id": org_id,
        "name": f"{info['org_name']} -- {district} District",
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
        for district in sorted(districts[chamber]):
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
