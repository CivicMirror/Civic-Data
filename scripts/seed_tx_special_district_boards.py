#!/usr/bin/env python3
"""
Structure only: Jurisdiction, Organization (governing board) and Post
records for five TX special-district types from issue #32's "not started"
list -- Emergency Services, Hospital, Levee Improvement, Library and
Municipal Management Districts.

Input: reference/TX Rolling Audit/tx_special_district_seat_specs_2026-09-30.csv
-- one row per district that research confirmed has an elected board
chosen by general-public election, with its seat structure. Every row's
`basis` and `source_url` say where the elected status and seat count come
from. Research trail (type-level statutes, per-district holds/exclusions)
is in reference/TX Rolling Audit/Special_District_Type_Keys.md and the
issue #32 comment for 2026-09-30.

Seat counts come from the enabling statute wherever one fixes them (ESD
Health & Safety Code Sec. 775.0345/775.035 = 5; library Local Gov't Code
Sec. 326.041 = 5; levee Water Code Sec. 57.058 = 5 when elected; each
hospital district's and MMD's own Special District Local Laws Code
chapter) and from the district's own site only where no statute does.
They are never taken from the SPDPID board-member headcount, so the
officeholder importer's headcount gate stays meaningful.

seat_spec mini-language (terms joined by "+"):
  pool:N          N undifferentiated at-large seats   -> <kind>-1..N
  places:N        numbered places 1..N                -> place-1..N
  positions:A-B   numbered positions A..B             -> position-A..B
                  (Knox County HD: only elected positions 5-7 exist here)
  smd:N           single-member districts 1..N        -> district-1..N
  precinct:PxK    K seats in each of P precincts      -> precinct-P[-seat-K]
  al:N            N at-large seats beside other kinds -> at-large[-N]

Mixed boards (Gateway Park MMD, Viridian MMD, Knox County HD) mint only
the elected seats, same as the Edwards Aquifer Authority precedent.

Idempotent by id -- never overwrites an existing file.

Usage: python3 seed_tx_special_district_boards.py [--write]
"""
import csv
import re
import sys
import unicodedata
import uuid
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
SPEC_CSV = REPO / "reference" / "TX Rolling Audit" / "tx_special_district_seat_specs_2026-09-30.csv"
RETRIEVED = "2026-09-30"

NS = uuid.UUID("8c4e2a7f-3b9d-5e1c-a6f2-7d9b3c5e1a8f")

# type -> (type key, directory, post-id qualifier, member title, board name)
TYPES = {
    "esd": ("emergency_services_district", "esd", "tx-esd", "Emergency Services Commissioner", "Board of Emergency Services Commissioners"),
    "hospital": ("hospital_district", "hospital", "tx-hd", "Director", "Board of Directors"),
    "levee": ("levee_improvement_district", "levee", "tx-lid", "Director", "Board of Directors"),
    "library": ("library_district", "library", "tx-lib", "Trustee", "Board of Trustees"),
    "mmd": ("municipal_management_district", "mmd", "tx-mmd", "Director", "Board of Directors"),
}

HEADER = (
    "# Seeded from the TX special-district rolling audit (issue #32) by\n"
    "# scripts/seed_tx_special_district_boards.py. Structure only. Elected\n"
    "# status and seat structure from the enabling statute or the district's\n"
    "# own site -- see the source note and the script docstring.\n"
)


def slugify(name):
    s = name.replace("&", "and")
    s = re.sub(r"\bNo\.\s*(\d+)", r"#\1", s, flags=re.IGNORECASE)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii").lower()
    s = re.sub(r"#\s*(\d+)", r"-\1", s)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def seats(spec, member):
    """Expand a seat_spec into [(post suffix, title)]."""
    out = []
    for term in spec.split("+"):
        kind, arg = term.split(":")
        if kind == "pool":
            out += [(f"{member.lower().replace(' ', '-')}-{n}", f"{member}, Position {n}") for n in range(1, int(arg) + 1)]
        elif kind == "places":
            out += [(f"place-{n}", f"{member}, Place {n}") for n in range(1, int(arg) + 1)]
        elif kind == "positions":
            a, b = (int(x) for x in arg.split("-"))
            out += [(f"position-{n}", f"{member}, Position {n}") for n in range(a, b + 1)]
        elif kind == "smd":
            out += [(f"district-{n}", f"{member}, District {n}") for n in range(1, int(arg) + 1)]
        elif kind == "precinct":
            p, k = (int(x) for x in arg.split("x"))
            for i in range(1, p + 1):
                label = chr(64 + i) if spec.startswith("precinct:2x") else str(i)
                if k == 1:
                    out.append((f"precinct-{label.lower()}", f"{member}, Precinct {label}"))
                else:
                    out += [(f"precinct-{label.lower()}-seat-{j}", f"{member}, Precinct {label}, Seat {j}") for j in range(1, k + 1)]
        elif kind == "al":
            n = int(arg)
            out += [("at-large", f"{member}, At Large")] if n == 1 else [
                (f"at-large-{j}", f"{member}, At Large, Seat {j}") for j in range(1, n + 1)]
        else:
            raise ValueError(f"unknown seat_spec term {term!r}")
    return out


def existing_ids(kind):
    ids = set()
    for f in (DATA_DIR / kind).glob("**/*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if "id" in doc:
            ids.add(doc["id"])
    return ids


def write_file(path, doc, write):
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(HEADER + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000))


def main():
    write = "--write" in sys.argv[1:]
    only = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--types=")), list(TYPES))
    have = {k: existing_ids(k) for k in ("jurisdictions", "organizations", "posts")}
    stats = Counter()
    slugs = set()

    for row in csv.DictReader(SPEC_CSV.open(newline="")):
        t = row["type"]
        if t not in only:
            continue
        type_key, d, qual, member, board = TYPES[t]
        slug = slugify(row["name"])
        if (t, slug) in slugs:
            sys.exit(f"slug collision: {t} {slug}")
        slugs.add((t, slug))

        note = (
            f"{row['name']} (SPD Public ID {row['spd_id']}) -- {row['county']}. Enumerated via the Texas "
            f"Comptroller's Special Purpose District Public Information Database (SPDPID). Elected board and "
            f"seat structure: {row['basis']}." + (f" {row['note']}" if row["note"] else "")
        )
        src = [{"url": row["source_url"], "note": note, "retrieved": RETRIEVED}]
        if row["website"] and row["website"] != row["source_url"] and "spdpid" not in row["website"]:
            src.append({"url": row["website"], "note": f"{row['name']} website as listed in SPDPID.", "retrieved": RETRIEVED})

        jid = f"ocd-jurisdiction/country:us/state:tx/{type_key}:{slug}/government"
        if jid not in have["jurisdictions"]:
            write_file(DATA_DIR / "jurisdictions" / d / f"{slug}-government.yaml", {
                "id": jid, "name": row["name"], "state": "tx",
                "division_id": f"ocd-division/country:us/state:tx/{type_key}:{slug}",
                "classification": "government",
                "identifiers": [{"scheme": "tx-spdpid", "identifier": row["spd_id"]}],
                "sources": src,
            }, write)
            stats[f"{t}_jurisdiction_new"] += 1

        oid = f"ocd-organization/{uuid.uuid5(NS, f'organization|{t}|{slug}')}"
        if oid not in have["organizations"]:
            write_file(DATA_DIR / "organizations" / d / f"{slug}-board.yaml", {
                "id": oid, "name": f"{row['name']} {board}", "jurisdiction_id": jid,
                "identifiers": [], "status": "active", "sources": src,
            }, write)
            stats[f"{t}_org_new"] += 1

        for suffix, title in seats(row["seat_spec"], member):
            pid = f"{slug}-{qual}/{suffix}"
            if pid in have["posts"]:
                continue
            write_file(DATA_DIR / "posts" / d / f"{slug}-{qual}-{suffix}.yaml", {
                "id": pid, "organization_id": oid, "title": title, "seats": 1,
                "identifiers": [], "sources": src,
            }, write)
            stats[f"{t}_post_new"] += 1

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


if __name__ == "__main__":
    main()
