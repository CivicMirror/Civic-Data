#!/usr/bin/env python3
"""
Merged pipeline: unitedstates/congress-legislators (current + historical +
district-offices) as the primary source, FEC + Congress.gov APIs used only
to fill or cross-check what that source doesn't carry.

Produces schema-valid `person` + `membership` (+ `post`/`organization` where
new) records for the CURRENT (post-migration) Civic-Data schema -- no
roles[] on person, officeholding lives in memberships.

Before emitting anything, it indexes the *existing* repo (data/us/**) so it
never mints a duplicate person for someone already on file, never collides
with an existing membership id, and resolves organization_id from the real
organizations/federal/*.yaml records instead of leaving it UNRESOLVED.

Usage: python3 build_federal_records.py <bioguide_id> [--write] [--fec-key KEY] [--cg-key KEY]

Without --write, prints what it would do (dry run). With --write, creates
new person/membership files under data/us/<state>/{people,memberships}/federal/
-- but only for records that don't already exist; it never overwrites.
"""
import json
import os
import re
import sys
import uuid
import urllib.request
import urllib.error
from pathlib import Path

import yaml
try:
    from yaml import CSafeLoader as _YamlLoader
except ImportError:
    from yaml import SafeLoader as _YamlLoader

FEC_KEY = os.environ.get("FEC_API_KEY", "DEMO_KEY")
CG_KEY = os.environ.get("CONGRESS_API_KEY", "")

LEGISLATORS_CURRENT = "/tmp/legislators-current.yaml"
LEGISLATORS_HISTORICAL = "/tmp/legislators-historical.yaml"
DISTRICT_OFFICES = "/tmp/district_offices.yaml"

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us"

ROMAN = {1: "I", 2: "II", 3: "III"}


def uid(seed):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))


def get_json(url):
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"_error": e.code}
    except Exception as e:
        return {"_error": str(e)}


_cache = {}


def load_legislators():
    if "current" not in _cache:
        _cache["current"] = yaml.load(open(LEGISLATORS_CURRENT), Loader=_YamlLoader)
        _cache["historical"] = yaml.load(open(LEGISLATORS_HISTORICAL), Loader=_YamlLoader)
        _cache["offices"] = yaml.load(open(DISTRICT_OFFICES), Loader=_YamlLoader)
    return _cache["current"], _cache["historical"], _cache["offices"]


def find_legislator(bioguide_id):
    current, historical, offices = load_legislators()
    for leg in current:
        if leg["id"]["bioguide"] == bioguide_id:
            return leg, "current"
    for leg in historical:
        if leg["id"]["bioguide"] == bioguide_id:
            return leg, "historical"
    raise ValueError(f"{bioguide_id} not found in current or historical legislators file")


def find_district_offices(bioguide_id):
    _, _, offices = load_legislators()
    for entry in offices:
        if entry["id"].get("bioguide") == bioguide_id:
            return entry["offices"]
    return []


# --------------------------------------------------------------------------
# Repo indexing: never duplicate a person, never collide a membership id,
# always resolve organization_id from what's actually on disk.
# --------------------------------------------------------------------------

def normalize_name(name):
    name = name.lower()
    name = re.sub(r"[.,'’]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def index_people():
    """id -> record, plus lookup by bioguide identifier and by normalized name."""
    by_bioguide = {}
    by_name = {}
    by_path = {}
    for path in DATA_DIR.glob("*/people/**/*.yaml"):
        doc = yaml.safe_load(path.read_text())
        if not doc or "id" not in doc:
            continue
        by_path[doc["id"]] = path
        for ident in doc.get("identifiers", []):
            if ident.get("scheme") == "bioguide":
                by_bioguide[ident["identifier"]] = doc
        by_name.setdefault(normalize_name(doc["name"]), doc)
    return by_bioguide, by_name, by_path


def index_memberships():
    """
    membership id -> path, across every state, PLUS a (person_id, post_id,
    start) -> path index so a differently-named file for the same span
    (e.g. the "-historical" suffix convention) still counts as a match.
    """
    ids = {}
    spans = {}
    for path in DATA_DIR.glob("*/memberships/**/*.yaml"):
        doc = yaml.safe_load(path.read_text())
        if not doc or "id" not in doc:
            continue
        ids[doc["id"]] = path
        span_key = (doc.get("person_id"), doc.get("post_id"), doc.get("start"))
        spans[span_key] = path
    return ids, spans


def index_organizations():
    """
    (state, 'house', district) -> org id
    (state, 'senate', None)    -> org id   (one Senate org per state, both classes)
    """
    house = {}
    senate = {}
    for path in DATA_DIR.glob("*/organizations/federal/*.yaml"):
        doc = yaml.safe_load(path.read_text())
        if not doc:
            continue
        state = path.parts[path.parts.index("us") + 1]
        jur = doc.get("jurisdiction_id", "")
        m = re.search(r"/cd:(\d+)/", jur)
        if m:
            house[(state, m.group(1))] = doc["id"]
        elif jur.endswith("/legislature") and "cd:" not in jur:
            senate[state] = doc["id"]
    return house, senate


def slugify(name):
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def cd_jurisdiction(state, district):
    return f"ocd-jurisdiction/country:us/state:{state.lower()}/cd:{district}/legislature"


def house_post_id(state, district):
    return f"{state.lower()}-{district}/us-representative"


def collapse_terms(terms, key_fn):
    """Collapse consecutive terms with the same key into one span."""
    spans = []
    for t in terms:
        k = key_fn(t)
        if spans and spans[-1][0] == k:
            spans[-1][2] = t  # extend end
        else:
            spans.append([k, t, t])
    return spans  # list of [key, first_term, last_term]


def build(bioguide_id, people_by_bioguide, people_by_name):
    leg, source_file = find_legislator(bioguide_id)
    ids = leg["id"]
    name = leg["name"].get("official_full") or f"{leg['name']['first']} {leg['name']['last']}"
    terms = leg["terms"]
    district_offices = find_district_offices(bioguide_id)

    # --- resolve against existing repo people first ---
    existing = people_by_bioguide.get(bioguide_id) or people_by_name.get(normalize_name(name))
    person_is_new = existing is None
    person_uuid = existing["id"].split("/", 1)[1] if existing else uid(f"bioguide:{bioguide_id}")
    person_id = existing["id"] if existing else f"ocd-person/{person_uuid}"

    # --- gap-fill / cross-check via Congress.gov (current-member flag, portrait) ---
    cg = get_json(f"https://api.congress.gov/v3/member/{bioguide_id}?api_key={CG_KEY}&format=json") if CG_KEY else {"_error": "no key"}
    cg_member = cg.get("member") if isinstance(cg, dict) and "member" in cg else None
    image = cg_member["depiction"]["imageUrl"] if cg_member and cg_member.get("depiction") else None
    current_member_flag = cg_member.get("currentMember") if cg_member else None

    # --- gap-fill / cross-check via FEC (candidate status), using the FEC ID(s)
    #     congress-legislators ALREADY bundles -- no search needed ---
    fec_notes = []
    for fec_id in ids.get("fec", []):
        fec = get_json(f"https://api.open.fec.gov/v1/candidate/{fec_id}/?api_key={FEC_KEY}")
        if isinstance(fec, dict) and fec.get("results"):
            r = fec["results"][0]
            fec_notes.append(f"{fec_id}: candidate_status={r.get('candidate_status')}, "
                              f"incumbent_challenge={r.get('incumbent_challenge')}, "
                              f"active_through={r.get('active_through')}")

    identifiers = []
    for scheme in ["bioguide", "govtrack", "wikidata", "wikipedia", "ballotpedia",
                   "opensecrets", "votesmart", "icpsr", "lis", "thomas", "cspan", "maplight"]:
        if ids.get(scheme):
            identifiers.append({"scheme": scheme, "identifier": str(ids[scheme])})
    for fec_id in ids.get("fec", []):
        identifiers.append({"scheme": "fec-candidate-id", "identifier": fec_id})

    last_term = terms[-1]
    contact = {"phone": last_term.get("phone", ""), "profile_url": last_term.get("url", "")}
    contact = {k: v for k, v in contact.items() if v}

    addresses = []
    if last_term.get("office") or last_term.get("address"):
        capitol_addr = {
            "classification": "capitol",
            "name": "Washington, D.C. Office",
            "address": last_term.get("address", last_term.get("office", "")),
        }
        if last_term.get("phone"):
            capitol_addr["phone"] = last_term["phone"]
        addresses.append(capitol_addr)
    for off in district_offices:
        parts = [off.get("building"), off.get("address"), off.get("suite")]
        street = ", ".join(p for p in parts if p)
        district_addr = {
            "classification": "district",
            "name": f"{off['city']} Office",
            "address": f"{street};{off['city']}, {off['state']} {off['zip']}",
        }
        if off.get("phone"):
            district_addr["phone"] = off["phone"]
        if off.get("fax"):
            district_addr["fax"] = off["fax"]
        addresses.append(district_addr)

    sources = [{
        "url": f"https://github.com/unitedstates/congress-legislators/blob/main/legislators-{source_file}.yaml",
        "note": f"unitedstates/congress-legislators ({source_file}), bioguide {bioguide_id} -- primary source for identity, terms, class, dates.",
    }]
    if district_offices:
        sources.append({
            "url": "https://github.com/unitedstates/congress-legislators/blob/main/legislators-district-offices.yaml",
            "note": "District office addresses/phones.",
        })
    if cg_member:
        sources.append({
            "url": f"https://api.congress.gov/v3/member/{bioguide_id}",
            "note": f"Congress.gov cross-check -- currentMember={current_member_flag}, portrait image.",
        })
    elif CG_KEY:
        sources.append({
            "url": f"https://api.congress.gov/v3/member/{bioguide_id}",
            "note": f"Congress.gov lookup returned no record (common for pre-modern historical members): {cg.get('_error')}",
        })
    if fec_notes:
        sources.append({
            "url": "https://api.open.fec.gov/v1/candidate/",
            "note": "FEC cross-check -- " + "; ".join(fec_notes),
        })

    person = {
        "id": person_id,
        "name": name,
        "identifiers": identifiers,
        "candidacies": [],
        **({"image": image} if image else {}),
        **({"contact": contact} if contact else {}),
        **({"addresses": addresses} if addresses else {}),
        "verification": {
            "status": "machine-extracted",
            "pipeline": "congress-legislators+fec-api+congress-gov-api",
        },
        "sources": sources,
    }

    # --- memberships: one per contiguous chamber+seat span ---
    def seat_key(t):
        if t["type"] == "rep":
            return ("house", t["state"], t.get("district"))
        return ("sen", t["state"], t.get("class"))

    house_org, senate_org = index_organizations()

    memberships = []
    for key, first_t, last_t in collapse_terms(terms, seat_key):
        chamber, state, seat = key
        still_serving = source_file == "current" and last_t is terms[-1]

        if chamber == "house":
            org_id = house_org.get((state.lower(), str(seat)))
            post_id = house_post_id(state, seat)
            role = "U.S. Representative"
            mem_id = f"cd-{seat}-us-representative-{leg['name']['last'].lower()}"
        else:
            org_id = senate_org.get(state.lower())
            cls_roman = ROMAN.get(seat, str(seat))
            post_id = f"{state.lower()}/us-senator-class-{seat}"
            role = f"U.S. Senator (Class {cls_roman})"
            mem_id = f"{state.lower()}-us-senate-class-{seat}-{leg['name']['last'].lower()}"

        mem = {
            "id": mem_id,
            "person_id": person_id,
            "organization_id": org_id or "UNRESOLVED -- no organization record exists yet for this jurisdiction in the live repo",
            "post_id": post_id,
            "role": role,
            "seat": (f"Class {ROMAN.get(seat,seat)}" if chamber == "sen" else "At-Large"),
            "start": first_t["start"],
            **({} if still_serving else {"end": last_t["end"]}),
            "how_seated": "elected",
            "sources": [{
                "url": f"https://github.com/unitedstates/congress-legislators/blob/main/legislators-{source_file}.yaml",
                "note": f"Term span for bioguide {bioguide_id}, {chamber} seat.",
            }],
        }
        memberships.append(mem)

    return person, memberships, person_is_new


def main():
    args = sys.argv[1:]
    write = "--write" in args
    args = [a for a in args if a != "--write"]
    bioguide_id = args[0]

    global FEC_KEY, CG_KEY
    for i, a in enumerate(args):
        if a == "--fec-key":
            FEC_KEY = args[i + 1]
        if a == "--cg-key":
            CG_KEY = args[i + 1]

    people_by_bioguide, people_by_name, people_by_path = index_people()
    membership_ids, membership_spans = index_memberships()

    person, memberships, person_is_new = build(bioguide_id, people_by_bioguide, people_by_name)

    state = None
    for m in memberships:
        state = m["post_id"].split("/")[0].split("-")[0]
        break

    if person_is_new:
        print(f"# person {person['id']} is NEW -- not previously on file")
        if write:
            state_dir = DATA_DIR / state / "people" / "federal"
            state_dir.mkdir(parents=True, exist_ok=True)
            out = state_dir / f"{slugify(person['name'])}.yaml"
            if out.exists():
                print(f"# REFUSING to overwrite existing file {out}")
            else:
                out.write_text(yaml.safe_dump(person, sort_keys=False, allow_unicode=True,
                                                default_flow_style=False, width=1000))
                print(f"# wrote {out}")
        else:
            print(yaml.safe_dump(person, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000))
    else:
        existing_path = people_by_path[person["id"]]
        print(f"# person {person['id']} ALREADY EXISTS at {existing_path} -- skipping (no overwrite)")

    for m in memberships:
        if m["id"] in membership_ids:
            print(f"# membership {m['id']} ALREADY EXISTS at {membership_ids[m['id']]} -- skipping (no overwrite)")
            continue
        span_key = (m["person_id"], m["post_id"], m["start"])
        if span_key in membership_spans:
            print(f"# membership {m['id']} matches an existing span at {membership_spans[span_key]} "
                  f"(different filename, same person/post/start) -- skipping (no overwrite)")
            continue
        if not str(m["organization_id"]).startswith("ocd-organization/"):
            print(f"# membership {m['id']}: organization_id UNRESOLVED -- not written, needs a real organizations/federal/*.yaml record first")
            print(yaml.safe_dump(m, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000))
            continue
        print(f"# membership {m['id']} is NEW")
        if write:
            state_dir = DATA_DIR / state / "memberships" / "federal"
            state_dir.mkdir(parents=True, exist_ok=True)
            out = state_dir / f"{m['id']}.yaml"
            if out.exists():
                print(f"# REFUSING to overwrite existing file {out}")
            else:
                out.write_text(yaml.safe_dump(m, sort_keys=False, allow_unicode=True,
                                                default_flow_style=False, width=1000))
                print(f"# wrote {out}")
        else:
            print(yaml.safe_dump(m, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000))


if __name__ == "__main__":
    main()
