#!/usr/bin/env python3
"""
Generate organization/post records for Massachusetts's mayoral offices,
driven entirely by OCPF's public filer registry (api.ocpf.us/filers/listings/C
-- category C is candidate committees). This is the same "self-bootstrapping"
approach as build_federal_orgs.py: the list of which MA cities even have a
mayor, and each office's canonical title, comes straight from OCPF's own
officeSought/officeHeld/officeDescription fields -- no external source needed.

Does NOT create jurisdictions -- every MA municipality already has a
jurisdiction record under data/us/ma/jurisdictions/municipal/*-government.yaml
(sourced from the Census Bureau's Census of Governments dataset), so this
only adds the organization+post pair on top of what's already there. If a
city OCPF lists a mayoral race for has no matching jurisdiction file, it's
reported and skipped rather than guessed.

Scope is Mayor only -- NOT City Council. A mayor is always a single at-large
citywide seat, so it's safe to infer structurally. City Council seat counts
and ward/district structure are NOT derivable from OCPF (or from the Census
jurisdiction records) and would need the same hand charter-research the NC
municipal data used.

Idempotent by id AND by filename -- never overwrites.

Usage: python3 build_ma_mayors.py [--write]
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
OCPF_FILERS_C_URL = "https://api.ocpf.us/filers/listings/C?loadRemaining=true"
CACHE_PATH = Path("/tmp/ocpf_filers_c.json")

TODAY = datetime.now(UTC).date().isoformat()

HEADER = (
    "# Machine-generated from OCPF's filer registry (api.ocpf.us/filers/listings/C)\n"
    "# by scripts/build_ma_mayors.py. Reuses the existing Census-sourced jurisdiction\n"
    "# record for this city rather than creating a new one.\n"
)


def uid(seed):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))


def slugify(name):
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def load_filers():
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text())
    with urllib.request.urlopen(OCPF_FILERS_C_URL, timeout=120) as r:
        data = json.load(r)
    CACHE_PATH.write_text(json.dumps(data))
    return data


def mayoral_cities(filers):
    cities = set()
    for f in filers:
        office_sought = f.get("officeSought") or ""
        if office_sought.startswith("Mayoral,"):
            cities.add(office_sought.split(",", 1)[1].strip())
    return sorted(cities)


def jurisdiction_exists(slug):
    return (DATA_DIR / "jurisdictions" / "municipal" / f"{slug}-government.yaml").exists()


def jurisdiction_id(slug):
    return f"ocd-jurisdiction/country:us/state:ma/place:{slug}/government"


def build_records(city, slug):
    jid = jurisdiction_id(slug)
    org_id = f"ocd-organization/{uid(f'ma-mayor-office:{slug}')}"

    source = {
        "url": "https://api.ocpf.us/filers/listings/C",
        "note": f"OCPF candidate-committee filer registry; confirms {city} has an elected Mayor's office",
        "retrieved": TODAY,
    }

    organization = {
        "id": org_id,
        "name": f"Office of the Mayor, {city}",
        "jurisdiction_id": jid,
        "identifiers": [],
        "sources": [source],
    }

    post = {
        "id": f"{slug}/mayor",
        "organization_id": org_id,
        "title": f"Mayor of {city}",
        "seats": 1,
        "identifiers": [],
        "sources": [source],
    }

    return organization, post


class Recorder:
    def __init__(self, write):
        self.write = write
        self.stats = {}

    def handle(self, kind, doc, filename):
        path = DATA_DIR / kind / "municipal" / filename
        singular = kind.rstrip("s")

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

    filers = load_filers()
    cities = mayoral_cities(filers)

    rec = Recorder(write)
    missing_jurisdiction = []

    for city in cities:
        slug = slugify(city)
        if not jurisdiction_exists(slug):
            missing_jurisdiction.append((city, slug))
            continue
        organization, post = build_records(city, slug)
        rec.handle("organizations", organization, f"{slug}-mayor-office.yaml")
        rec.handle("posts", post, f"{slug}-mayor.yaml")

    print("==================== SUMMARY ====================")
    print(f"OCPF cities with a Mayoral office: {len(cities)}")
    print(f"Missing jurisdiction (skipped): {len(missing_jurisdiction)}")
    for city, slug in missing_jurisdiction:
        print(f"  {city} -> expected data/us/ma/jurisdictions/municipal/{slug}-government.yaml")
    for k in sorted(rec.stats):
        print(f"{k}: {rec.stats[k]}")


if __name__ == "__main__":
    main()
