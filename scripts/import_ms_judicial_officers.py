#!/usr/bin/env python3
"""Import current Mississippi Chancery and Circuit Court judges.

The Mississippi Secretary of State's County Offices and Directory (2026)
lists judges under every county they serve.  Its county presentation is useful
corroboration, but cannot safely be used as the identity record: it repeats
the same judge in every served county and sometimes varies suffixes or names.

The SOS's companion Chancery Court and Terms (2026) and Circuit Court and
Terms (2026) publications list each judge once under the applicable judicial
district.  This script imports those district-level listings into the
judicial-district organizations and posts established for Issue #41.

Download the two PDFs from the URLs below and pass their local paths.  The
script is a dry run by default; use --write to create records.
"""
import argparse
import re
import unicodedata
import uuid
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "ms"
RETRIEVED = "2026-09-17"
NS = uuid.UUID("5d092e1b-baa4-554d-bd29-313f35d15ad3")

SOURCES = {
    "chancery": {
        "url": "https://www.sos.ms.gov/sites/default/files/publications/Chancery%20Court%20and%20Terms%202026.pdf",
        "note": "Mississippi Secretary of State, Chancery Court and Terms 2026: current chancery court judges by judicial district.",
    },
    "circuit": {
        "url": "https://www.sos.ms.gov/sites/default/files/publications/Circuit%20Court%20and%20Terms%202026.pdf",
        "note": "Mississippi Secretary of State, Circuit Court and Terms 2026: current circuit court judges by judicial district.",
    },
}

ORDINALS = {
    "FIRST": 1, "SECOND": 2, "THIRD": 3, "FOURTH": 4, "FIFTH": 5,
    "SIXTH": 6, "SEVENTH": 7, "EIGHTH": 8, "NINTH": 9, "TENTH": 10,
    "ELEVENTH": 11, "TWELFTH": 12, "THIRTEENTH": 13, "FOURTEENTH": 14,
    "FIFTEENTH": 15, "SIXTEENTH": 16, "SEVENTEENTH": 17,
    "EIGHTEENTH": 18, "NINETEENTH": 19, "TWENTIETH": 20,
    "TWENTY-FIRST": 21, "TWENTY-SECOND": 22, "TWENTY-THIRD": 23,
}


def slugify(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def oid(kind, key):
    return f"ocd-{kind}/{uuid.uuid5(NS, kind + '|' + key)}"


def source(kind):
    return [{**SOURCES[kind], "retrieved": RETRIEVED}]


def pdf_text(path):
    # pdftotext is deliberately invoked through the standard library so this
    # script remains usable in the repository's existing import environment.
    import subprocess

    return subprocess.run(["pdftotext", "-layout", str(path), "-"], check=True, capture_output=True, text=True).stdout


def parse_judges(pdf_path, kind):
    """Return {district_number: [{name, address, phone}, ...]} from an SOS PDF."""
    heading = re.compile(rf"^([A-Z-]+) {kind.upper()} DISTRICT")
    judge = re.compile(r"^Judge\s*[. ]+(.+)$")
    # In a few rows the PDF omits the normal dot leader between a judge's
    # name and an address (for example, ``Hollowell III.2535 Highway``).
    # Every court-office address begins with either a street number or P.O.,
    # so use that stable boundary rather than spacing or dot-leader width.
    address_start = re.compile(r"\.?(?=(?:P\.O\.|\d{1,5}\s))")
    districts = {}
    current = None

    for raw in pdf_text(pdf_path).splitlines():
        line = raw.strip()
        match = heading.match(line)
        if match:
            current = ORDINALS[match.group(1)]
            districts.setdefault(current, [])
            continue
        match = judge.match(line)
        if not match or current is None:
            continue
        body = match.group(1)
        split = address_start.search(body)
        if not split:
            raise ValueError(f"Could not locate address boundary for {kind} judge: {raw}")
        name = body[:split.start()].strip(" .")
        if not name:
            raise ValueError(f"Could not parse {kind} judge name: {raw}")
        districts[current].append({"name": name})
    return districts


def load_post(kind, district):
    path = DATA_DIR / "posts" / "judicial-district" / f"{kind}-district-{district}.yaml"
    if not path.exists():
        raise ValueError(f"No {kind} post for district {district}: {path}")
    return yaml.safe_load(path.read_text()) or {}


def emit(path, document, write):
    if path.exists():
        existing = yaml.safe_load(path.read_text()) or {}
        if existing.get("id") != document["id"]:
            raise ValueError(f"Filename conflict with a different record: {path}")
        return "existing"
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=1000))
    return "new"


def build(kind, pdf_path, write):
    districts = parse_judges(pdf_path, kind)
    expected_districts = 20 if kind == "chancery" else 23
    if len(districts) != expected_districts:
        raise ValueError(f"Parsed {len(districts)} {kind} districts, expected {expected_districts}")

    results = {"people_new": 0, "people_existing": 0, "memberships_new": 0, "memberships_existing": 0}
    for district, judges in sorted(districts.items()):
        post = load_post(kind, district)
        if len(judges) != post["seats"]:
            raise ValueError(
                f"{kind} district {district}: parsed {len(judges)} judges, post has {post['seats']} seats"
            )
        court_title = "Chancery Court Judge" if kind == "chancery" else "Circuit Court Judge"
        organization_id = post["organization_id"]
        post_id = post["id"]
        for judge_number, judge in enumerate(judges, start=1):
            key = f"ms-{kind}-district-{district}|{judge['name']}"
            person_id = oid("person", key)
            person = {
                "id": person_id,
                "name": judge["name"],
                "candidacies": [],
                "verification": {"status": "machine-extracted", "reviewed_on": RETRIEVED, "pipeline": "import_ms_judicial_officers"},
                "sources": source(kind),
            }
            slug = slugify(judge["name"])
            person_path = DATA_DIR / "people" / "judicial-district" / f"{slug}-{kind}-district-{district}.yaml"
            result = emit(person_path, person, write)
            results[f"people_{result}"] += 1

            membership = {
                "id": f"{kind}-district-{district}-{slug}",
                "person_id": person_id,
                "organization_id": organization_id,
                "post_id": post_id,
                "role": court_title,
                "how_seated": "elected",
                "sources": source(kind),
            }
            membership_path = DATA_DIR / "memberships" / "judicial-district" / f"{membership['id']}.yaml"
            result = emit(membership_path, membership, write)
            results[f"memberships_{result}"] += 1
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chancery-pdf", type=Path, required=True)
    parser.add_argument("--circuit-pdf", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    results = {}
    for kind, path in (("chancery", args.chancery_pdf), ("circuit", args.circuit_pdf)):
        if not path.is_file():
            parser.error(f"missing {kind} PDF: {path}")
        results[kind] = build(kind, path, args.write)
    for kind, counts in results.items():
        print(kind, ", ".join(f"{key}={value}" for key, value in counts.items()))
    if not args.write:
        print("dry run; pass --write to create records")


if __name__ == "__main__":
    main()
