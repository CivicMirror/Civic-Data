#!/usr/bin/env python3
"""
Generate jurisdiction/organization/post triples for federal House districts
and Senate seats, driven entirely by unitedstates/congress-legislators
(legislators-current.yaml) -- the same primary source build_federal_records.py
uses for person/membership records.

Scope is CURRENT seats only: one triple per district/state that a sitting
member currently occupies. Historical/defunct districts (e.g. MA's pre-2013
10th) are out of scope here -- those get added by hand as historical people
are seeded, the same way MA's cd-10 was.

What's fully automatable from this source: id, name, division_id,
classification, the GovTrack/Senate.gov website link, and sources. Two
enrichment fields present on MA's hand-built jurisdiction records are NOT
derivable from congress-legislators/FEC/Congress.gov and are deliberately
left blank here for human backfill:
  - election_authority (each state's Secretary of State / election board)
  - site_intelligence (election-results vendor, scraper notes)
Both are optional per schemas/jurisdiction.schema.json, so records validate
without them.

Idempotent: never overwrites a file that already exists (so MA, already
hand-built, is untouched -- this only fills in the other 49 states + DC +
territories).

Usage: python3 build_federal_orgs.py [--write] [--state XX]
Without --write, prints a dry-run summary only.
"""
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path

import yaml
try:
    from yaml import CSafeLoader as _YamlLoader
except ImportError:
    from yaml import SafeLoader as _YamlLoader

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us"
LEGISLATORS_CURRENT = "/tmp/legislators-current.yaml"

TODAY = datetime.now(UTC).date().isoformat()

ROMAN = {1: "I", 2: "II", 3: "III"}

# Non-voting delegate / resident-commissioner jurisdictions (no Senate seats).
DELEGATE_STATES = {"DC", "AS", "GU", "MP", "VI"}
RESIDENT_COMMISSIONER_STATES = {"PR"}

STATE_NAMES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming",
    "DC": "the District of Columbia", "PR": "Puerto Rico", "AS": "American Samoa",
    "GU": "Guam", "MP": "the Northern Mariana Islands", "VI": "the U.S. Virgin Islands",
}

HEADER = (
    "# Machine-generated from unitedstates/congress-legislators (current) by\n"
    "# scripts/build_federal_orgs.py. election_authority and site_intelligence\n"
    "# are deliberately left blank -- they require per-state research beyond\n"
    "# this pipeline's sources and should be backfilled by hand.\n"
)


def uid(seed):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))


def ordinal(n):
    n = int(n)
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


def govtrack_house_url(state, district):
    if str(district) == "0":
        return f"https://www.govtrack.us/congress/members/{state}"
    return f"https://www.govtrack.us/congress/members/{state}/{district}"


def load_current():
    return yaml.load(open(LEGISLATORS_CURRENT), Loader=_YamlLoader)


def existing_ids(state, kind):
    """Set of ids already on disk under data/us/<state>/<kind>/federal/*.yaml."""
    ids = set()
    d = DATA_DIR / state / kind / "federal"
    if d.exists():
        for path in d.glob("*.yaml"):
            doc = yaml.safe_load(path.read_text())
            if doc and "id" in doc:
                ids.add(doc["id"])
    return ids


def house_records(state_upper, district):
    state = state_upper.lower()
    d = str(district)
    is_at_large = d == "0"

    if state_upper in RESIDENT_COMMISSIONER_STATES:
        title = "Resident Commissioner"
        gov_form = "at-large non-voting resident commissioner district (U.S. House of Representatives)"
        org_role_name = "Resident Commissioner"
    elif state_upper in DELEGATE_STATES:
        title = "Delegate to the U.S. House of Representatives"
        gov_form = "at-large non-voting delegate district (U.S. House of Representatives)"
        org_role_name = "Delegate"
    else:
        title = "U.S. Representative"
        gov_form = (
            "at-large district (U.S. House of Representatives)" if is_at_large
            else "single-member district (U.S. House of Representatives)"
        )
        org_role_name = "U.S. Representative"

    state_name = STATE_NAMES[state_upper]
    district_label = "At-Large" if is_at_large else ordinal(d)
    url = govtrack_house_url(state_upper, d)

    jurisdiction_id = f"ocd-jurisdiction/country:us/state:{state}/cd:{d}/legislature"
    jurisdiction = {
        "id": jurisdiction_id,
        "name": f"{state_name}'s {district_label} congressional district (U.S. House delegation)",
        "state": state,
        "division_id": f"ocd-division/country:us/state:{state}/cd:{d}",
        "classification": "legislature",
        "government_form": gov_form,
        "website": url,
        "sources": [{
            "url": url,
            "note": "GovTrack district page; used because congressional districts have no official government website of their own",
            "retrieved": TODAY,
        }],
    }

    org_id = f"ocd-organization/{uid(f'us-house:{state}:{d}')}"
    org_name = (
        f"U.S. House of Representatives -- {state_name}'s {district_label} District"
        if org_role_name == "U.S. Representative"
        else f"U.S. House of Representatives -- {state_name} ({org_role_name})"
    )
    organization = {
        "id": org_id,
        "name": org_name,
        "jurisdiction_id": jurisdiction_id,
        "identifiers": [],
        "sources": [{"url": url, "retrieved": TODAY}],
    }

    post_id = f"{state}-{d}/us-representative"
    post = {
        "id": post_id,
        "organization_id": org_id,
        "title": title,
        "seats": 1,
        "identifiers": [],
        "sources": [{"url": url, "retrieved": TODAY}],
    }

    return {
        "jurisdictions": (jurisdiction, f"cd-{d}.yaml"),
        "organizations": (organization, f"cd-{d}-us-house.yaml"),
        "posts": (post, f"cd-{d}-us-representative.yaml"),
    }


def senate_records(state_upper, classes):
    state = state_upper.lower()
    state_name = STATE_NAMES[state_upper]
    url = f"https://www.senate.gov/{state_upper}/intro.htm"

    jurisdiction_id = f"ocd-jurisdiction/country:us/state:{state}/legislature"
    jurisdiction = {
        "id": jurisdiction_id,
        "name": f"{state_name} (U.S. Senate delegation)",
        "state": state,
        "division_id": f"ocd-division/country:us/state:{state}",
        "classification": "legislature",
        "sources": [{
            "url": url,
            "note": "Official U.S. Senate directory page for this state's two Senate seats",
            "retrieved": TODAY,
        }],
    }

    org_id = f"ocd-organization/{uid(f'us-senate:{state}')}"
    organization = {
        "id": org_id,
        "name": f"United States Senate -- {state_name}",
        "jurisdiction_id": jurisdiction_id,
        "identifiers": [],
        "sources": [{"url": url, "retrieved": TODAY}],
    }

    records = {
        "jurisdictions": [(jurisdiction, f"{state}-us-senate.yaml")],
        "organizations": [(organization, f"{state}-us-senate.yaml")],
        "posts": [],
    }
    for cls in sorted(classes):
        post_id = f"{state}/us-senator-class-{cls}"
        post = {
            "id": post_id,
            "organization_id": org_id,
            "title": f"U.S. Senator (Class {ROMAN[cls]})",
            "seats": 1,
            "identifiers": [],
            "sources": [{"url": url, "retrieved": TODAY}],
        }
        records["posts"].append((post, f"{state}-us-senator-class-{cls}.yaml"))
    return records


class Recorder:
    def __init__(self, write):
        self.write = write
        self.stats = {}
        self._existing_cache = {}

    def handle(self, state_upper, kind, doc, filename):
        state = state_upper.lower()
        cache_key = (state, kind)
        if cache_key not in self._existing_cache:
            self._existing_cache[cache_key] = existing_ids(state, kind)
        existing = self._existing_cache[cache_key]
        path = DATA_DIR / state / kind / "federal" / filename

        singular = kind.rstrip("s") if kind != "jurisdictions" else "jurisdiction"

        if doc["id"] in existing:
            self.stats[f"{singular}_existing_by_id"] = self.stats.get(f"{singular}_existing_by_id", 0) + 1
            return
        if path.exists():
            # Same filename already on disk under a different id -- a
            # naming collision with hand-built data, not a real duplicate.
            # Never write over it.
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
            self._existing_cache[cache_key].add(doc["id"])


def main():
    args = sys.argv[1:]
    write = "--write" in args
    args = [a for a in args if a != "--write"]
    only_state = None
    if "--state" in args:
        only_state = args[args.index("--state") + 1].upper()

    legislators = load_current()

    house_districts = {}  # state -> set of district strings
    senate_classes = {}   # state -> set of Senate class ints actually held

    for leg in legislators:
        t = leg["terms"][-1]
        st = t["state"]
        if only_state and st != only_state:
            continue
        if t["type"] == "rep":
            house_districts.setdefault(st, set()).add(str(t.get("district", "0")))
        elif t["type"] == "sen":
            senate_classes.setdefault(st, set()).add(t["class"])

    rec = Recorder(write)

    for state_upper, districts in sorted(house_districts.items()):
        for d in sorted(districts, key=lambda x: (len(x), x)):
            triples = house_records(state_upper, d)
            for kind, (doc, filename) in triples.items():
                rec.handle(state_upper, kind, doc, filename)

    for state_upper, classes in sorted(senate_classes.items()):
        groups = senate_records(state_upper, classes)
        for kind, items in groups.items():
            for doc, filename in items:
                rec.handle(state_upper, kind, doc, filename)

    print("==================== SUMMARY ====================")
    print(f"States/territories with House seats: {len(house_districts)}")
    print(f"States with Senate seats: {len(senate_classes)}")
    for k in sorted(rec.stats):
        print(f"{k}: {rec.stats[k]}")


if __name__ == "__main__":
    main()
