#!/usr/bin/env python3
"""
Seed current-officeholder person + membership records for MA's 45 Mayor's
offices (built by build_ma_mayors.py), from OCPF's filer registry.

For each incumbent mayor (isIncumbent=true, officeSought startswith
"Mayoral,") in the /filers/listings/C registry, fetches full filer detail
via /filer/payload/{cpfId} to get their legal name and the most recent
"Winner" tag for the Mayoral office (year + district) -- the term-start
signal. Term start is approximated as January 1 of the year after the win
(MA mayors are inaugurated in early January; the exact charter-specified
date isn't in OCPF's data) -- flagged as approximate in a source note
rather than guessed silently, per this repo's schema-over-precision norm.

Deliberately NOT full Phase C: no candidacies, no party, no losing/past
candidates -- those come from the full historical OCPF sweep (Phase C),
which will reuse the same per-filer "tags" data this script only reads
the latest Winner entry from.

Idempotent by id AND by filename -- never overwrites.

Usage: python3 build_ma_mayors_people.py [--write]
"""
import json
import re
import sys
import unicodedata
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_federal_records as bfr

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "ma"
FILERS_C_CACHE = Path("/tmp/ocpf_filers_c.json")
PAYLOAD_CACHE_DIR = Path("/tmp/ocpf_filer_payloads")

TODAY = datetime.now(UTC).date().isoformat()

HEADER = (
    "# Machine-generated from OCPF's filer registry (api.ocpf.us/filer/payload/{cpfId})\n"
    "# by scripts/build_ma_mayors_people.py. Term start is approximated as Jan 1 of the\n"
    "# year after the OCPF 'Winner' tag's year -- the exact charter-specified inauguration\n"
    "# date is not in OCPF's data and should be verified/corrected by hand.\n"
)


def slugify(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def normalize_name(name):
    name = name.lower()
    name = re.sub(r"[.,'’]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def load_filers():
    return json.loads(FILERS_C_CACHE.read_text())


def load_payload(cpf_id):
    PAYLOAD_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = PAYLOAD_CACHE_DIR / f"{cpf_id}.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text())
    url = f"https://api.ocpf.us/filer/payload/{cpf_id}"
    with urllib.request.urlopen(url, timeout=20) as r:
        data = json.load(r)
    cache_path.write_text(json.dumps(data))
    return data


def latest_mayoral_winner_year(tags):
    years = [t["year"] for t in tags
             if t.get("tagTypeDescription") == "Winner" and t.get("officeType") == "Mayoral"]
    return max(years) if years else None


def load_org_post(slug):
    org_path = DATA_DIR / "organizations" / "municipal" / f"{slug}-mayor-office.yaml"
    post_path = DATA_DIR / "posts" / "municipal" / f"{slug}-mayor.yaml"
    if not org_path.exists() or not post_path.exists():
        return None, None
    org = yaml.safe_load(org_path.read_text())
    post = yaml.safe_load(post_path.read_text())
    return org["id"], post["id"]


def main():
    write = "--write" in sys.argv[1:]

    filers = load_filers()
    incumbents = [f for f in filers if f.get("isIncumbent")
                  and (f.get("officeSought") or "").startswith("Mayoral,")]

    people_by_bioguide, people_by_name, people_by_path = bfr.index_people()
    membership_ids, membership_spans = bfr.index_memberships()

    stats = {}
    skipped = []

    for filer in incumbents:
        city = filer["officeSought"].split(",", 1)[1].strip()
        slug = slugify(city)
        cpf_id = filer["cpfId"]

        org_id, post_id = load_org_post(slug)
        if not org_id:
            skipped.append((city, f"no org/post on file for slug {slug!r}"))
            continue

        detail = load_payload(cpf_id)
        f = detail.get("filer") or {}
        winner_year = latest_mayoral_winner_year(f.get("tags") or [])
        if not winner_year:
            skipped.append((city, f"no Mayoral 'Winner' tag found for cpfId {cpf_id}"))
            continue

        name = (f.get("fullName") or filer.get("filerName") or "").strip()
        if not name:
            skipped.append((city, f"no name for cpfId {cpf_id}"))
            continue

        existing = people_by_name.get(normalize_name(name))
        person_id = existing["id"] if existing else f"ocd-person/{bfr.uid(f'ocpf-filer:{cpf_id}')}"
        person_is_new = existing is None

        photo = f.get("filerPhotoUrl") or filer.get("filerThumbnailPhotoUrl") or ""
        candidate_info = f.get("candidate") or {}

        source = {
            "url": f"https://ocpf.us/filers?q={cpf_id}",
            "note": f"OCPF filer profile for {name} (cpfId {cpf_id})",
            "retrieved": TODAY,
        }

        person = {
            "id": person_id,
            "name": name,
            "identifiers": [{"scheme": "ocpf-filer-id", "identifier": str(cpf_id)}],
            "candidacies": [],
            **({"image": photo} if photo else {}),
            **({"contact": {"profile_url": f"https://ocpf.us/filers?q={cpf_id}"}}),
            # OCPF's "candidate" address is the filer's own registered mailing
            # address (often residential), not a government office -- "district"
            # is the closer fit of the schema's two allowed classifications.
            **({"addresses": [{
                "classification": "district",
                "name": "OCPF Filer Address",
                "address": candidate_info["fullAddress"].strip(),
            }]} if candidate_info.get("fullAddress") else {}),
            "verification": {
                "status": "machine-extracted",
                "pipeline": "ocpf-filer-registry",
            },
            "sources": [source],
        }

        family_name = f.get("candidateLastName") or name.split()[-1]
        membership = {
            "id": f"{slug}-mayor-{slugify(family_name)}",
            "person_id": person_id,
            "organization_id": org_id,
            "post_id": post_id,
            "role": "Mayor",
            "seat": "At-Large",
            "start": f"{winner_year + 1}-01-01",
            "how_seated": "elected",
            "sources": [source],
        }

        if person_is_new:
            stats["person_new"] = stats.get("person_new", 0) + 1
            if write:
                out = DATA_DIR / "people" / "municipal" / f"{slugify(name)}.yaml"
                out.parent.mkdir(parents=True, exist_ok=True)
                if out.exists():
                    stats["person_skipped_filename_conflict"] = stats.get("person_skipped_filename_conflict", 0) + 1
                else:
                    out.write_text(HEADER + yaml.safe_dump(person, sort_keys=False, allow_unicode=True,
                                                             default_flow_style=False, width=1000))
                    people_by_name[normalize_name(name)] = person
        else:
            stats["person_existing"] = stats.get("person_existing", 0) + 1

        if membership["id"] in membership_ids:
            stats["membership_existing_by_id"] = stats.get("membership_existing_by_id", 0) + 1
            continue
        span_key = (membership["person_id"], membership["post_id"], membership["start"])
        if span_key in membership_spans:
            stats["membership_existing_by_span"] = stats.get("membership_existing_by_span", 0) + 1
            continue

        stats["membership_new"] = stats.get("membership_new", 0) + 1
        if write:
            out = DATA_DIR / "memberships" / "municipal" / f"{membership['id']}.yaml"
            out.parent.mkdir(parents=True, exist_ok=True)
            if out.exists():
                stats["membership_skipped_filename_conflict"] = stats.get("membership_skipped_filename_conflict", 0) + 1
            else:
                out.write_text(HEADER + yaml.safe_dump(membership, sort_keys=False, allow_unicode=True,
                                                         default_flow_style=False, width=1000))
                membership_ids[membership["id"]] = out
                membership_spans[span_key] = out

    print("==================== SUMMARY ====================")
    print(f"Incumbent mayors in OCPF: {len(incumbents)}")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    print(f"\nSkipped: {len(skipped)}")
    for city, why in skipped:
        print(f"  {city}: {why}")


if __name__ == "__main__":
    main()
