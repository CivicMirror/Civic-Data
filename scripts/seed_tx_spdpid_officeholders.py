#!/usr/bin/env python3
"""
Seed Person/Membership records for TX special-purpose district board
members (issue #32, Phase 1) from the Texas Comptroller's SPDPID
"related party" self-report data -- the annual board-member disclosure
required by Gov't Code Sec. 403.0241(c), joined by spd_publ_id (the same
`tx-spdpid` identifier already stored on every jurisdiction seeded in
Phase 1).

Source: reference/TX Rolling Audit/spdpid_related_party_boardmembers_2026-09-28.csv
-- a copy of the Comptroller's own raw "related-party" export (one of six
CSVs the Comptroller publishes, joined by spd_publ_id) trimmed to
rp_ty_cd == 'BrdMem' rows and to the 352 districts already seeded
anywhere in data/us/tx/jurisdictions/ (all types, not just the 8 covered
here, so this file stays usable as later phases mint more types).
Retrieved 2026-09-28.

This is a validated pilot, not a blind trust of the source: a 15-district
random sample (2 per completed Phase 1 type) was checked against
independent web sources before writing this importer (see issue #32).
Findings: the data is directionally reliable (headcounts mostly matched
independently-confirmed seat counts; one district matched an outside
source exactly, name-for-name) but has three concrete failure modes for
self-reported annual data:
  - staleness within the reporting year (a board reshuffle isn't
    reflected until the next annual filing)
  - un-pruned departed members inflating the reported headcount
  - complete non-reporting for some real, active districts

Because of this, the import discipline is stricter than the ISD/CCD
precedent (seed_tx_isd_people_atlarge.py, seed_tx_ccd_people.py), which
treats an under-count as a trustworthy vacancy. Here, BOTH over- and
under-counts are routed to manual review rather than imported, since the
pilot found real, non-vacancy discrepancies in both directions:

  AUTO-IMPORT only when ALL of:
    - the district has at least one BrdMem row
    - the latest reported year is 2025 or 2026 (i.e. not stale)
    - the reported headcount for that year exactly matches the number
      of Posts already minted for that district's board
    - no duplicate normalized name within that district/year

  FLAG for manual review otherwise, with a reason code:
    - no_data          -- zero BrdMem rows for this district at all
    - stale             -- latest reported year <= 2024
    - headcount_over    -- reported count > minted seat count
    - headcount_under   -- reported count < minted seat count
    - duplicate_name    -- same normalized name appears 2+ times
    - site_roster_mismatch -- (SUD batch onward) SPDPID names a person
                          absent from the district's own current roster;
                          see SITE_ROSTER_MISMATCH

Flagged rows are written to a CSV under reference/TX Rolling Audit/ (not
imported) for manual research, and that file is meant to be attached to
issue #32.

Assignment of reported people to numbered Posts (e.g. "Director,
Position 2") is positional only (sorted by last/first name for a stable,
reproducible order) -- the Posts are an undifferentiated at-large pool in
every Phase 1 type except EAA's single-member districts, and this
dataset never states which named person holds which numbered slot, so
position numbers carry no real-world meaning beyond satisfying the
schema's post_id requirement.

Idempotent: keyed by (spd_publ_id, normalized name) for person ids, and
by (org slug, person slug) for membership ids -- re-running after adding
a later year's data will not duplicate existing records for people who
already have one for this district (it also won't retroactively update
an existing membership if the person's title changed; that is future
work, not silently overwritten here).

Multi-ID districts: BrdMem rows are merged across all of a jurisdiction's
tx-spdpid identifiers (fixed 2026-09-30; before that only the last ID's
rows were read, which mis-flagged Ables Springs SUD as stale off its
INACTIVE ID's 2023 filing). Plum Creek Conservation District (WCID, two
IDs) was processed under the old behavior in the 2026-09-28 batch and was
not re-run.

"sud" was added 2026-09-30 after scripts/seed_tx_sud_orgs_posts.py
minted SUD boards; that batch was run as
  --types=sud --flagged-out=tx_spdpid_officeholders_manual_review_sud_2026-09-30.csv
so the original 2026-09-28 review queue was not overwritten.

Usage: python3 seed_tx_spdpid_officeholders.py [--write] [--types=a,b] [--flagged-out=FILE.csv]
"""
import csv
import glob
import re
import sys
import unicodedata
import uuid
from collections import Counter, defaultdict
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "tx"
SRC_CSV = REPO / "reference" / "TX Rolling Audit" / "spdpid_related_party_boardmembers_2026-09-28.csv"
FLAGGED_OUT = REPO / "reference" / "TX Rolling Audit" / "tx_spdpid_officeholders_manual_review_2026-09-28.csv"

RETRIEVED = "2026-09-28"
CURRENT_YEAR = 2026
STALE_CUTOFF_YEAR = 2025  # latest report must be >= this to auto-import

PHASE1_TYPES = [
    "wcid", "fwsd", "wid", "irrigation", "gcd", "drainage",
    "conservation_reclamation", "eaa", "sud",
]

# SUD batch (2026-09-30): each district's own current board page was
# fetched while confirming seat counts, and SPDPID names were checked
# against it. A headcount match is not a roster match -- these districts'
# SPDPID self-report matches the seat count but names at least one person
# absent from the district's own current roster (spelling variants such as
# Prewitt/Prewett or Padelecki/Padalecki were cleared by hand first). They
# are routed to review with the site roster attached, not imported.
SITE_ROSTER_MISMATCH = {
    "103228131": "AGUA SUD board page (District 1-7): Gerardo Perez (Sec, D1); Alex Moreno (D2); Roel De Hoyos (VP, D3); Jose Luis Ochoa Jr. (Pres, D4); Ana Maria Perez (D5); Ricardo Perez (Treas, D6); Dr. Adriana Villarreal (D7) -- SPDPID's Adolfo Mendez not listed",
    "103227274": "Maurice Pittman (Pres); Thomas King (VP); Ann King (Sec-Treas); Chad Berberich; Bob Schmidtke; Paul Cauley; Rick Taylor -- SPDPID's Pete Slocum not listed",
    "103225542": "Andy Yates (Pres); Allen Powers (VP); Ward Guffey (Sec/Treas); Bobby Sanders (Employee Relations Rep); Paul Cantrell -- SPDPID's Larry Ensor not listed",
    "103226409": "board-elections page: Pos 1 Cheryl Patterson; Pos 2 Joseph Benavides; Pos 3 Jamie Trant; Pos 4 Nick Reininger; Pos 5 Ben Raska; Pos 6 Andrea Velasquez; Pos 7 VACANT. board-members page lists Pamela Kraft (Pres) instead of Reininger -- site pages disagree; SPDPID's Cynthia Cash not listed on either",
    "103226559": "Roger Hankey (Pres); Bob Skipwith (VP); Bill Collins (Sec/Treas); Wayne Chumley; Pat Duval -- SPDPID's Mark Burnett not listed",
    "103226896": "Ken Bonzo (Pres); Curt Deatrich (VP); William (Bill) Richey (Sec); Ed Cooke (Treas); Gary O'Dell (Asst Treas); Justin Fraley; Joseph Anselmo -- SPDPID's Bruce McDonald not listed",
    "103226468": "Max Owens (Pres); Charles Nash (VP); Charles Ives (Treas/Sec); Margaret Avard; Bryan Wilson -- SPDPID's Scott Johnson, Albert Ellis, Glenn Vargas not listed",
    "103228120": "maxwellwsc.com (page carries a 2022 alert, may be stale): Doug Spillmann (Pres); Valentin Yanez Jr. (VP); Liralen Canion (Treas); Doris Steubing (Asst Treas); Mabel Vaughn (Sec); Carol Thornton; Leah Gibson; Jess Stephens -- SPDPID's Roy Duran not listed; 9 seats confirmed by 2022 election order",
    "103227550": "Michael Walker (Pres, Place 1); Matt Gauntt (VP, Place 2); Kim Lehere (Sec); Rob Adams; Michael Skelton (Place 3); Michael Bolton; Jeff Stafford; Mark Millar; Angela Zarallo -- SPDPID's Ken Mitchell not listed",
    "103227789": "James Massey (Pres, 5/27); Brent Paterson (VP, 5/28); John Himmel (Treas, 5/29); Gwen Hattaway (Sec, 5/29); Travis Miller (5/27); Susan Lightfoot (5/28); David Ernstes (5/27); Perry Barboza (5/28); Dave Nutt (5/29) -- SPDPID 2025's Larry Michalcheck not listed",
}

PERSON_NS = uuid.UUID("2b8f6e2a-9c1d-4f7e-9a3b-6d5c4e3f2a1b")

ROMAN_SUFFIXES = {"II", "III", "IV"}


def to_name_case(raw):
    words = raw.strip().split()
    out = []
    for w in words:
        core = re.sub(r"[^A-Za-z]", "", w)
        if core.upper() in ROMAN_SUFFIXES and core.upper() == core:
            out.append(w.upper())
            continue
        out.append(w[:1].upper() + w[1:].lower() if w.isupper() or w.islower() else w)
    return " ".join(out)


def normalize_name(first, mid, last):
    parts = [p.strip() for p in (first, mid, last) if p and p.strip()]
    raw = " ".join(parts)
    return to_name_case(raw)


def normalize_title(raw):
    raw = (raw or "").strip()
    if not raw:
        return "Director"
    if raw.isupper() or raw.islower():
        return raw.title()
    return raw


def slugify(name):
    text = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text


def person_id(spd_publ_id, name):
    return f"ocd-person/{uuid.uuid5(PERSON_NS, f'person|{spd_publ_id}|{name}')}"


def unique_filename(taken, base_slug):
    slug = base_slug
    n = 2
    while slug in taken:
        slug = f"{base_slug}-{n}"
        n += 1
    taken.add(slug)
    return slug


def load_districts():
    """Load every Phase 1 district: jurisdiction, its org, its posts."""
    districts = {}
    for t in PHASE1_TYPES:
        jdir = DATA_DIR / "jurisdictions" / t
        odir = DATA_DIR / "organizations" / t
        pdir = DATA_DIR / "posts" / t
        if not jdir.is_dir():
            continue
        for jf in sorted(jdir.glob("*.yaml")):
            jdoc = yaml.safe_load(jf.read_text()) or {}
            spd_ids = [i["identifier"] for i in jdoc.get("identifiers", []) if i.get("scheme") == "tx-spdpid"]
            if not spd_ids:
                continue
            # Keyed by the LAST identifier, as before 2026-09-30, so person ids
            # already minted for multi-ID districts stay stable.
            spd_id = spd_ids[-1]
            jur_id = jdoc["id"]
            org_doc = None
            for of in odir.glob("*.yaml"):
                od = yaml.safe_load(of.read_text()) or {}
                if od.get("jurisdiction_id") == jur_id:
                    org_doc = od
                    break
            if not org_doc:
                continue
            posts = []
            for pf in pdir.glob("*.yaml"):
                pd_ = yaml.safe_load(pf.read_text()) or {}
                if pd_.get("organization_id") == org_doc["id"]:
                    posts.append(pd_)
            posts.sort(key=lambda p: p["id"])
            if not posts:
                continue
            districts[spd_id] = {
                "type": t,
                "name": jdoc["name"],
                "jurisdiction_id": jur_id,
                "org_id": org_doc["id"],
                "org_source_url": (org_doc.get("sources") or [{}])[0].get("url", ""),
                "posts": posts,
                "slug_base": jf.stem,
                "spd_ids": spd_ids,
            }
    return districts


def load_boardmember_rows():
    by_spd = defaultdict(list)
    with SRC_CSV.open(newline="", encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            by_spd[row["spd_publ_id"]].append(row)
    return by_spd


def main():
    global PHASE1_TYPES, FLAGGED_OUT
    write = "--write" in sys.argv[1:]
    for arg in sys.argv[1:]:
        # --types=sud restricts a run to later-minted types; --flagged-out=NAME
        # keeps that run from overwriting an earlier run's review queue.
        if arg.startswith("--types="):
            PHASE1_TYPES = arg.split("=", 1)[1].split(",")
        elif arg.startswith("--flagged-out="):
            FLAGGED_OUT = FLAGGED_OUT.parent / arg.split("=", 1)[1]

    districts = load_districts()
    rows_by_spd = load_boardmember_rows()

    people_taken = {}
    membership_taken = {}
    existing_person_ids = {}
    existing_membership_ids = {}
    for t in PHASE1_TYPES:
        pdir = DATA_DIR / "people" / t
        mdir = DATA_DIR / "memberships" / t
        people_taken[t] = {p.stem for p in pdir.glob("*.yaml")} if pdir.is_dir() else set()
        membership_taken[t] = {p.stem for p in mdir.glob("*.yaml")} if mdir.is_dir() else set()
        existing_person_ids[t] = set()
        if pdir.is_dir():
            for f in pdir.glob("*.yaml"):
                d = yaml.safe_load(f.read_text()) or {}
                if "id" in d:
                    existing_person_ids[t].add(d["id"])
        existing_membership_ids[t] = set()
        if mdir.is_dir():
            for f in mdir.glob("*.yaml"):
                d = yaml.safe_load(f.read_text()) or {}
                if "id" in d:
                    existing_membership_ids[t].add(d["id"])

    stats = Counter()
    flagged = []

    for spd_id, dist in sorted(districts.items()):
        t = dist["type"]
        # Merge BrdMem rows across every SPD ID on the jurisdiction (ACTIVE/
        # INACTIVE re-registration pairs); latest year wins below.
        rows = [r for i in dist["spd_ids"] for r in rows_by_spd.get(i, [])]
        if not rows:
            stats["flag_no_data"] += 1
            flagged.append({
                "reason": "no_data", "type": t, "spd_publ_id": spd_id,
                "district_name": dist["name"], "minted_seats": len(dist["posts"]),
                "reported_count": 0, "latest_year": "", "names": "",
            })
            continue

        years = sorted({r["rpt_yr"] for r in rows}, key=int)
        latest_year = years[-1]
        latest_rows = [r for r in rows if r["rpt_yr"] == latest_year]

        names_titles = []
        for r in latest_rows:
            name = normalize_name(r["rp_frst_nm"], r["rp_mid_nm"], r["rp_lst_nm"])
            title = normalize_title(r["rp_titl_tx"])
            names_titles.append((name, title))

        name_counts = Counter(n for n, _ in names_titles)
        dupes = [n for n, c in name_counts.items() if c > 1]

        reported_count = len(names_titles)
        minted_count = len(dist["posts"])

        reason = None
        if int(latest_year) < STALE_CUTOFF_YEAR:
            reason = "stale"
        elif spd_id in SITE_ROSTER_MISMATCH:
            reason = "site_roster_mismatch"
        elif dupes:
            reason = "duplicate_name"
        elif reported_count > minted_count:
            reason = "headcount_over"
        elif reported_count < minted_count:
            reason = "headcount_under"

        if reason:
            stats[f"flag_{reason}"] += 1
            flagged.append({
                "reason": reason, "type": t, "spd_publ_id": spd_id,
                "district_name": dist["name"], "minted_seats": minted_count,
                "reported_count": reported_count, "latest_year": latest_year,
                "names": "; ".join(f"{n} ({ti})" for n, ti in names_titles)
                + (f" | SITE: {SITE_ROSTER_MISMATCH[spd_id]}" if reason == "site_roster_mismatch" else ""),
            })
            continue

        # Auto-import: stable order by (last-token, full name), assign
        # positionally to posts sorted by post id.
        ordered = sorted(names_titles, key=lambda nt: (nt[0].split()[-1], nt[0]))
        filed_spd_id = latest_rows[0]["spd_publ_id"]  # the ID that actually filed latest_year
        source_url = f"https://spdpid.comptroller.texas.gov/view/{latest_year}/{filed_spd_id}"
        source_note = (
            f"{dist['name']} (SPD Public ID {filed_spd_id}) -- self-reported board "
            f"member disclosure to the Texas Comptroller's Special Purpose "
            f"District Public Information Database (SPDPID), required by "
            f"Gov't Code Sec. 403.0241(c), report year {latest_year}. "
            f"Self-reported by the district and not independently verified "
            f"by the Comptroller; see issue #32's officeholder-sourcing pilot "
            f"comment for the accuracy spot-check this import relies on."
        )

        for (name, title), post in zip(ordered, dist["posts"]):
            pid = person_id(spd_id, name)
            if pid not in existing_person_ids[t]:
                stats["person_new"] += 1
                filename = unique_filename(people_taken[t], f"{dist['slug_base']}-{slugify(name)}")
                person_doc = {
                    "id": pid,
                    "name": name,
                    "candidacies": [],
                    "verification": {
                        "status": "machine-extracted",
                        "reviewed_on": RETRIEVED,
                        "pipeline": "TX SPDPID officeholder import (issue #32)",
                    },
                    "sources": [{"url": source_url, "note": source_note, "retrieved": RETRIEVED}],
                }
                if write:
                    (DATA_DIR / "people" / t).mkdir(parents=True, exist_ok=True)
                    (DATA_DIR / "people" / t / f"{filename}.yaml").write_text(
                        yaml.safe_dump(person_doc, sort_keys=False, allow_unicode=True,
                                       default_flow_style=False, width=1000)
                    )
                existing_person_ids[t].add(pid)

            mem_base = f"{dist['slug_base']}-{slugify(name)}"
            if mem_base in existing_membership_ids[t]:
                stats["skip_membership_exists"] += 1
                continue
            mem_slug = unique_filename(membership_taken[t], mem_base)
            membership_doc = {
                "id": mem_slug,
                "person_id": pid,
                "organization_id": dist["org_id"],
                "post_id": post["id"],
                "role": title,
                "sources": [{"url": source_url, "note": source_note, "retrieved": RETRIEVED}],
            }
            stats["membership_new"] += 1
            if write:
                (DATA_DIR / "memberships" / t).mkdir(parents=True, exist_ok=True)
                (DATA_DIR / "memberships" / t / f"{mem_slug}.yaml").write_text(
                    yaml.safe_dump(membership_doc, sort_keys=False, allow_unicode=True,
                                   default_flow_style=False, width=1000)
                )
            existing_membership_ids[t].add(mem_slug)

        stats["district_imported"] += 1

    if flagged:
        with FLAGGED_OUT.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=[
                "reason", "type", "spd_publ_id", "district_name",
                "minted_seats", "reported_count", "latest_year", "names",
            ])
            w.writeheader()
            w.writerows(flagged)
        print(f"Wrote {len(flagged)} flagged districts to {FLAGGED_OUT}")

    print("==================== SUMMARY ====================")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    if not write:
        print("\n(dry run -- pass --write to create files)")


if __name__ == "__main__":
    main()
