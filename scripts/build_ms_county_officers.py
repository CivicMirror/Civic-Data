#!/usr/bin/env python3
"""
Build MS county-level elected officer records from the Mississippi Secretary
of State's "County Offices and Directory (2026)" PDF into
data/us/ms/{organizations,posts,memberships,people}/county/. See issue #36.

Source: reference/MS Rolling Audit/MS_SOS_County_Offices_and_Directory_2026.pdf
(https://www.sos.ms.gov/sites/default/files/publications/County%20Offices%20
and%20Directory_2026.pdf), converted with `pdftotext -layout` and parsed by
scripts/parse_ms_county_offices_pdf.py (imported here as a module).

Scope: only offices the document's own section structure marks elected
(COUNTYWIDE/COUNTY DISTRICT OFFICES), and only single-county offices.
Deliberately NOT seeded here (held back pending a multi-county jurisdiction
decision, mirroring TX's judicial-district/appellate-district pattern under
issue #26): Chancery Court Judges, Circuit Court Judges, District Attorney --
these serve multi-county districts and modeling them as a per-county office
would misrepresent seat counts (one judge/DA serving N counties would become
N organizations/posts/memberships for one actual seat). Also not seeded:
every office the document itself lists under COUNTY APPOINTED OFFICES
(Board Attorney, Justice Court Clerk(s), County Engineer, Superintendent of
Education, County Administrator, County Comptroller, County Road Manager,
Justice Court Administrator, County Court Clerk) -- appointed, out of scope.

PERSON IDENTITY: person_id is namespaced by (county, office, name), not by
name alone. A name-only key would incorrectly merge distinct people who
happen to share a name across counties -- confirmed present in this dataset
(e.g. "Tony Morgan" is a Calhoun County supervisor and, separately, a Marion
County supervisor; different addresses, different people). The tradeoff:
the handful of officials who genuinely do serve two counties in the same
county-modeled office (e.g. a shared County Prosecuting Attorney or
Chancery Clerk district spanning county lines) get a separate Person record
per county rather than being recognized as the same individual. That is a
strictly safer failure mode than a false merge and can be reconciled later.

VACANT seats: the document explicitly marks some seats "Vacant." (e.g.
Sunflower Supervisors District 3, Warren Justice Court Judges Central
District, Jefferson County Surveyor). These get a Post with the correct
seat count but no Person/Membership for that seat -- the seat exists and is
unfilled, not absent.

Idempotent by id AND by filename -- never overwrites. Dry run by default;
pass --write to create files.
"""
import re
import subprocess
import sys
import unicodedata
import uuid
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_ms_county_offices_pdf as pdf_parser

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "ms"
SOURCE_PDF = REPO / "reference" / "MS Rolling Audit" / "MS_SOS_County_Offices_and_Directory_2026.pdf"

SOURCE_URL = "https://www.sos.ms.gov/sites/default/files/publications/County%20Offices%20and%20Directory_2026.pdf"
SOURCE_NOTE = "Mississippi Secretary of State, County Offices and Directory (2026)"
RETRIEVED = "2026-09-06"

NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")

HEADER = (
    "# Imported from the Mississippi Secretary of State's \"County Offices\n"
    "# and Directory (2026)\" PDF by scripts/build_ms_county_officers.py.\n"
    "# See issue #36. Chancery/Circuit Court Judges and District Attorney are\n"
    "# deliberately excluded -- multi-county offices held for a future\n"
    "# judicial-district jurisdiction pass. Appointed offices are excluded\n"
    "# per the document's own COUNTY APPOINTED OFFICES section.\n"
)

# office_key -> (title, [parsed.json keys to merge], role label)
OFFICES = [
    ("chancery-clerk", "Chancery Clerk", ["Chancery Clerk"]),
    ("circuit-clerk", "Circuit Clerk", ["Circuit Clerk"]),
    ("tax-assessor", "Tax Assessor", ["Tax Assessor"]),
    ("tax-collector", "Tax Collector", ["Tax Collector"]),
    ("coroner", "Coroner", ["Coroner"]),
    ("county-court-judge", "County Court Judge", ["County Court Judge", "County Court Judges"]),
    ("county-prosecuting-attorney", "County Prosecuting Attorney", ["County Prosecuting Attorney"]),
    ("sheriff", "Sheriff", ["Sheriff"]),
    ("county-surveyor", "County Surveyor", ["County Surveyor"]),
    ("constable", "Constable", ["Constables"]),
    ("election-commissioner", "Election Commissioner", ["Election Commissioners"]),
    ("justice-court-judge", "Justice Court Judge", ["Justice Court Judges"]),
    ("supervisor", "County Supervisor", ["Supervisors"]),
]


def slugify(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def titlecase_county(raw):
    return " ".join(w.capitalize() for w in raw.split())


def oid(kind, key):
    return f"ocd-{kind}/{uuid.uuid5(NS, kind + '|' + key)}"


def load_known_counties():
    known = {}
    for f in (DATA_DIR / "jurisdictions" / "county").glob("*-government.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        slug = f.stem[: -len("-government")]
        known[slug] = doc["id"]
    return known


class Recorder:
    def __init__(self, write):
        self.write = write
        self.stats = {}

    def emit(self, kind, doc, filename):
        singular = kind.rstrip("s")
        path = DATA_DIR / kind / "county" / filename
        if path.exists():
            existing = yaml.safe_load(path.read_text()) or {}
            if existing.get("id") == doc["id"]:
                self.stats[f"{singular}_existing"] = self.stats.get(f"{singular}_existing", 0) + 1
            else:
                self.stats[f"{singular}_skipped_filename_conflict"] = (
                    self.stats.get(f"{singular}_skipped_filename_conflict", 0) + 1
                )
            return False
        self.stats[f"{singular}_new"] = self.stats.get(f"{singular}_new", 0) + 1
        if self.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            text = HEADER + yaml.safe_dump(
                doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000
            )
            path.write_text(text)
        return True


def main():
    write = "--write" in sys.argv[1:]

    known_counties = load_known_counties()
    text = subprocess.run(
        ["pdftotext", "-layout", str(SOURCE_PDF), "-"],
        check=True, capture_output=True, text=True,
    ).stdout
    parsed = pdf_parser.parse(text)

    rec = Recorder(write)
    unknown_counties = {}

    orgs = {}
    posts = {}
    people = []
    memberships = []

    for county_upper in sorted(parsed):
        county_title = titlecase_county(county_upper)
        slug = slugify(county_title)
        if slug not in known_counties:
            unknown_counties[county_upper] = unknown_counties.get(county_upper, 0) + 1
            continue
        jurisdiction_id = known_counties[slug]

        for office_key, title, src_keys in OFFICES:
            entries = []
            for k in src_keys:
                entries.extend(parsed[county_upper].get(k, []))
            if not entries:
                continue

            org_key = (slug, office_key)
            post_id = f"{slug}-ms-county/{office_key}"
            org_id = oid("organization", f"ms-county|{slug}|{office_key}")
            orgs[org_key] = {
                "id": org_id,
                "name": title,
                "jurisdiction_id": jurisdiction_id,
                "identifiers": [{"scheme": "civicmirror-office", "identifier": post_id}],
                "status": "active",
                "sources": [{"url": SOURCE_URL, "note": SOURCE_NOTE, "retrieved": RETRIEVED}],
            }
            posts[org_key] = {
                "id": post_id,
                "organization_id": org_id,
                "title": title,
                "seats": len(entries),
                "sources": [{"url": SOURCE_URL, "note": SOURCE_NOTE, "retrieved": RETRIEVED}],
            }

            for entry in entries:
                name = entry["name"]
                seat = entry.get("seat")
                if name == "Vacant":
                    continue

                person_id = oid("person", f"ms-county|{slug}|{office_key}|{name}")
                addr = entry.get("address") or None
                phone = entry.get("phone") or None
                person = {
                    "id": person_id,
                    "name": name,
                    "candidacies": [],
                    "verification": {
                        "status": "machine-extracted",
                        "reviewed_on": RETRIEVED,
                        "pipeline": "build_ms_county_officers",
                    },
                    "sources": [{"url": SOURCE_URL, "note": SOURCE_NOTE, "retrieved": RETRIEVED}],
                }
                if phone:
                    person["contact"] = {"phone": phone}
                if addr:
                    entry_addr = {"classification": "district", "address": addr}
                    if phone:
                        entry_addr["phone"] = phone
                    person["addresses"] = [entry_addr]
                people.append((slug, person))

                seat_suffix = slugify(seat) if seat else slugify(name.split()[-1])
                mem_key = f"{slug}-ms-county-{office_key}-{seat_suffix}"
                membership = {
                    "id": mem_key,
                    "person_id": person_id,
                    "organization_id": org_id,
                    "post_id": post_id,
                    "role": title,
                    "how_seated": "elected",
                    "sources": [{"url": SOURCE_URL, "note": SOURCE_NOTE, "retrieved": RETRIEVED}],
                }
                if seat:
                    membership["seat"] = seat
                memberships.append((mem_key, membership))

    for org_key, org in orgs.items():
        slug, office_key = org_key
        rec.emit("organizations", org, f"{slug}-ms-county-{office_key}.yaml")
    for org_key, post in posts.items():
        slug, office_key = org_key
        rec.emit("posts", post, f"{slug}-ms-county-{office_key}.yaml")

    people_dir = DATA_DIR / "people" / "county"
    existing_id_by_slug = {}
    if people_dir.exists():
        for p in people_dir.glob("*.yaml"):
            doc = yaml.safe_load(p.read_text()) or {}
            existing_id_by_slug[p.stem] = doc.get("id")
    taken_people_slugs = set(existing_id_by_slug)

    for slug, person in people:
        base_slug = slugify(person["name"])
        # Re-running against an already-seeded slug should land on the same
        # file (idempotent), not treat the person's own prior file as a
        # collision with itself and mint a new, differently-named duplicate.
        if existing_id_by_slug.get(base_slug) == person["id"]:
            candidate = base_slug
        else:
            candidate = base_slug
            if candidate in taken_people_slugs:
                candidate = f"{base_slug}-{slug}"
            if existing_id_by_slug.get(candidate) == person["id"]:
                pass
            elif candidate in taken_people_slugs:
                suffix = person["id"].rsplit("/", 1)[-1][:8]
                candidate = f"{base_slug}-{slug}-{suffix}"
        taken_people_slugs.add(candidate)
        rec.emit("people", person, f"{candidate}.yaml")

    for mem_key, membership in memberships:
        rec.emit("memberships", membership, f"{mem_key}.yaml")

    print(f"Counties parsed: {len(parsed)}")
    print(f"Organizations: {len(orgs)}  Posts: {len(posts)}  People: {len(people)}  Memberships: {len(memberships)}")
    print()
    print("==================== SUMMARY ====================")
    for k in sorted(rec.stats):
        print(f"{k}: {rec.stats[k]}")
    if unknown_counties:
        print("\nERROR: unresolved county names (no matching jurisdiction slug):")
        for k in sorted(unknown_counties):
            print(f"  {k!r}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


if __name__ == "__main__":
    main()
