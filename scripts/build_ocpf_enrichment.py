#!/usr/bin/env python3
"""
Phase C: full historical OCPF enrichment for MA General Court (House/Senate)
and Mayor's offices -- candidacies (winners AND losers) plus historical
officeholder membership backfill, from OCPF's complete filer registry.

Source: cached /filer/payload/{cpfId} responses (fetched separately into
/tmp/ocpf_filer_payloads/*.json -- see fetch_ocpf_payloads.py) for every
filer whose officeSought starts with House/Senate/Mayoral. Each payload's
`tags[]` array is the ballot-history record: one "On Ballot" (or
occasionally "On Ballot - General Election") entry per contest they
appeared in, one "Winner" entry if they won it.

Key design decisions (see conversation / advisor review before this was
written):

- Only regular (non-special) elections are modeled. isSpecialElection tags
  are skipped and counted -- computing an exact historical special-election
  date isn't possible from OCPF's year-only tag data, and guessing one
  would be worse than omitting it.
- Not-yet-held (future) elections are skipped too -- out of scope for a
  historical-enrichment pass, and OCPF can't have result data for them yet.
- "On Ballot" is treated as GENERAL election ballot placement. Empirically
  validated against the 197 already-seeded current General Court members:
  matching each person's most recent non-special Winner-tag year against
  their real openstates start date confirms the general-election
  interpretation (93/113 checked matched winner_year+1; the remainder were
  all explained by isSpecialElection=True same-year seating, not a
  mismatch).
- A CONTEST is built by aggregating every filer with a matching
  (officeType, districtDescription, year, isSpecialElection=False) tag --
  not just the one filer being processed -- so each contest's candidate_ids
  reflects the real field, not a single person's view of it. This must
  happen before any file is written (election/contest and every
  candidate's reciprocal candidacy have to land together).
- Person matching, in order, to avoid minting a duplicate of someone
  already seeded (this was the single biggest failure mode found in
  earlier phases of this pipeline):
    1. ocpf-filer-id identifier already on a person (Mayor's Phase B people
       have this).
    2. The person currently holding the matching post, IF this tag's
       (year+1) equals that membership's real start year -- i.e. this tag
       *is* their current term.
    3. Exact normalized full-name match against every person already in
       the repo.
    4. Otherwise: new person.
- Membership backfill for a Winner tag only happens if the person has NO
  membership at all on file for that post_id yet (never overwrites or
  duplicates an existing span, current or historical). Historical span
  start is approximated as Jan 1 of (winner_year + 1); end date is not
  modeled in this pass (flagged in the source note).

Usage: python3 build_ocpf_enrichment.py [--write] [--district "7th Hampden"] [--city Somerville]
Without --write, dry run only. --district/--city restrict to one contest
group per office type, for sample review before the full sweep.
"""
import json
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_federal_records as bfr
import build_ma_general_court as gc

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "ma"
PAYLOAD_CACHE_DIR = Path("/tmp/ocpf_filer_payloads")

HEADER = (
    "# Machine-generated from OCPF's filer registry (api.ocpf.us/filer/payload/{cpfId})\n"
    "# by scripts/build_ocpf_enrichment.py. Only regular (non-special), already-held\n"
    "# elections are modeled; see the script's module docstring for the full set of\n"
    "# judgment calls.\n"
)

OFFICE_TYPES = {"House", "Senate", "Mayoral"}


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


def election_date(year):
    """First Tuesday after the first Monday in November."""
    d = date(year, 11, 1)
    while d.weekday() != 0:  # Monday
        d += timedelta(days=1)
    return d + timedelta(days=1)


def load_payloads():
    payloads = {}
    for p in PAYLOAD_CACHE_DIR.glob("*.json"):
        doc = json.loads(p.read_text())
        f = doc.get("filer") or {}
        if f:
            payloads[int(p.stem)] = f
    return payloads


ORDINAL_WORDS = {"1st": "First", "2nd": "Second", "3rd": "Third", "4th": "Fourth", "5th": "Fifth"}


def normalize_ocpf_district(district, office_type):
    """
    OCPF spells districts differently than openstates/people (the source
    build_ma_general_court.py used): "&" instead of "and", and for Senate
    districts specifically, numeral ordinals ("1st Essex & Middlesex")
    instead of spelled-out ones ("First Essex and Middlesex") -- an
    inconsistency in openstates' own data (House districts there DO use
    numerals). Normalize OCPF's spelling to match before slugifying.
    """
    d = district.replace("&", "and")
    if office_type == "Senate":
        for num, word in ORDINAL_WORDS.items():
            if d.startswith(num + " "):
                d = word + d[len(num):]
                break
    return d


def resolve_jurisdiction_org_post(office_type, district):
    """Returns (jurisdiction_id, organization_id, post_id) or None if unmappable."""
    if office_type in ("House", "Senate"):
        chamber = "lower" if office_type == "House" else "upper"
        district = normalize_ocpf_district(district, office_type)
        slug = gc.slugify(district)
        suffix = gc.CHAMBER_INFO[chamber]["file_suffix"]
        jpath = DATA_DIR / "jurisdictions" / "state" / f"{slug}-{suffix}.yaml"
        opath = DATA_DIR / "organizations" / "state" / f"{slug}-{suffix}.yaml"
        ppath = DATA_DIR / "posts" / "state" / f"{slug}-{suffix}.yaml"
    elif office_type == "Mayoral":
        slug = slugify(district)
        jpath = DATA_DIR / "jurisdictions" / "municipal" / f"{slug}-government.yaml"
        opath = DATA_DIR / "organizations" / "municipal" / f"{slug}-mayor-office.yaml"
        ppath = DATA_DIR / "posts" / "municipal" / f"{slug}-mayor.yaml"
    else:
        return None

    if not (jpath.exists() and opath.exists() and ppath.exists()):
        return None
    jur = yaml.safe_load(jpath.read_text())
    org = yaml.safe_load(opath.read_text())
    post = yaml.safe_load(ppath.read_text())
    return jur["id"], org["id"], post["id"]


def build_contest_groups(payloads, district_filter=None, city_filter=None):
    """
    (office_type, district, year) -> {
        'candidates': {cpf_id: {'filer': f, 'tag': tag}},
        'winners': {cpf_id},
    }
    Only non-special tags. Filters (if given) restrict to one district/city
    per office type family for sample runs.
    """
    groups = defaultdict(lambda: {"candidates": {}, "winners": set()})
    special_count = 0

    for cpf_id, f in payloads.items():
        for t in f.get("tags") or []:
            office_type = t.get("officeType")
            if office_type not in OFFICE_TYPES:
                continue
            if t.get("isSpecialElection"):
                special_count += 1
                continue
            district = t.get("districtDescription")
            if office_type in ("House", "Senate") and district_filter and district != district_filter:
                continue
            if office_type == "Mayoral" and city_filter and district != city_filter:
                continue

            key = (office_type, district, t["year"])
            desc = t.get("tagTypeDescription")
            if desc in ("On Ballot", "On Ballot - General Election"):
                groups[key]["candidates"][cpf_id] = {"filer": f, "tag": t}
            elif desc == "Winner":
                groups[key]["winners"].add(cpf_id)

    return groups, special_count


def surname_of(name):
    name = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode("ascii")
    parts = name.split()
    return parts[-1].lower() if parts else ""


def preresolve_person_identities(payloads, people_by_ocpf_id, people_by_post_current, people_by_name):
    """
    OCPF's cpfId is a lifetime identifier for ONE person's candidate
    committee, stable across every office they've ever run for -- so a
    person who moved between offices over their career (e.g. MA House
    2002-2008, then Senate 2010-present) must resolve to the SAME person
    record no matter which of their contests gets processed first.

    Resolving identity per-contest-group (checking only that one group's
    post) breaks this: processing their OLD House candidacies first (before
    their CURRENT Senate ones, since "House" < "Senate" alphabetically)
    finds no match against the House seat's current occupant (someone
    unrelated, since they moved on), mints a new person, and that wrong
    match then poisons every later lookup for the same cpfId.

    So identity is resolved ONCE per cpfId here, before any contest group
    is processed, checking every office they've ever run for -- not just
    whichever happens to be processed first.
    """
    for cpf_id, filer in payloads.items():
        if cpf_id in people_by_ocpf_id:
            continue

        full_name = (filer.get("fullName") or "").strip()
        fn, ln = filer.get("candidateFirstName", ""), filer.get("candidateLastName", "")
        for name in [full_name, f"{fn} {ln}".strip()]:
            if name:
                match = people_by_name.get(normalize_name(name))
                if match:
                    people_by_ocpf_id[cpf_id] = match["id"]
                    break
        if cpf_id in people_by_ocpf_id:
            continue

        # Surname fallback against the current occupant of ANY office this
        # cpfId has ever run for. OCPF's fullName often carries a middle
        # initial or formal first name a seeded record doesn't ("Daniel F.
        # Cahill" vs "Dan Cahill"), which the exact-name tier above can't
        # bridge. Scoped to "same specific single-member seat, same
        # surname" -- a strong signal for the same person; the residual
        # risk (a true, rare same-surname succession, e.g. parent-then-
        # child at the same seat years apart) is judged far less likely
        # than the systematic duplicate-minting this fixes, which otherwise
        # hits nearly every currently-serving GC member and mayor whose
        # OCPF fullName isn't their seeded record's exact display name.
        ocpf_last = ln.strip().lower()
        if not ocpf_last:
            continue
        seen_posts = set()
        for t in filer.get("tags") or []:
            office_type = t.get("officeType")
            if office_type not in OFFICE_TYPES:
                continue
            resolved = resolve_jurisdiction_org_post(office_type, t.get("districtDescription"))
            if not resolved:
                continue
            post_id = resolved[2]
            if post_id in seen_posts:
                continue
            seen_posts.add(post_id)
            current = people_by_post_current.get(post_id)
            if current and surname_of(current.get("name")) == ocpf_last:
                people_by_ocpf_id[cpf_id] = current["person_id"]
                break


def find_person_match(cpf_id, filer, people_by_ocpf_id, people_by_name):
    if cpf_id in people_by_ocpf_id:
        return people_by_ocpf_id[cpf_id], False

    full_name = (filer.get("fullName") or "").strip()
    candidates_names = [full_name] if full_name else []
    fn, ln = filer.get("candidateFirstName", ""), filer.get("candidateLastName", "")
    if fn and ln:
        candidates_names.append(f"{fn} {ln}")
    for name in candidates_names:
        match = people_by_name.get(normalize_name(name))
        if match:
            return match["id"], False

    return None, True


def main():
    args = sys.argv[1:]
    write = "--write" in args
    district_filter = args[args.index("--district") + 1] if "--district" in args else None
    city_filter = args[args.index("--city") + 1] if "--city" in args else None

    payloads = load_payloads()
    groups, special_count = build_contest_groups(payloads, district_filter, city_filter)

    # --- indices for person matching ---
    people_by_bioguide, people_by_name_raw, people_by_path = bfr.index_people()
    people_by_name = {k: {"id": v["id"], "name": v["name"]} for k, v in people_by_name_raw.items()}

    people_by_ocpf_id = {}
    for path in DATA_DIR.glob("people/**/*.yaml"):
        doc = yaml.safe_load(path.read_text())
        if not doc:
            continue
        for ident in doc.get("identifiers", []):
            if ident.get("scheme") == "ocpf-filer-id":
                people_by_ocpf_id[int(ident["identifier"])] = doc["id"]

    people_by_id_name = {v["id"]: v["name"] for v in people_by_name_raw.values()}

    people_by_post_current = {}
    post_membership_years = defaultdict(list)  # post_id -> [(start_year, person_id, is_current)]
    for path in DATA_DIR.glob("memberships/**/*.yaml"):
        doc = yaml.safe_load(path.read_text())
        if not doc or "post_id" not in doc:
            continue
        start_year = int(doc["start"][:4])
        is_current = "end" not in doc
        post_membership_years[doc["post_id"]].append((start_year, doc["person_id"], is_current))
        if is_current:
            existing = people_by_post_current.get(doc["post_id"])
            if not existing or start_year > existing["start_year"]:
                people_by_post_current[doc["post_id"]] = {
                    "start_year": start_year,
                    "person_id": doc["person_id"],
                    "name": people_by_id_name.get(doc["person_id"], ""),
                }

    preresolve_person_identities(payloads, people_by_ocpf_id, people_by_post_current, people_by_name)

    stats = defaultdict(int)
    no_current_membership_posts = set()
    unmapped_districts = set()
    person_cache = {}  # person_id -> (doc, path)
    dirty_people = {}

    def load_person(person_id, path_hint=None):
        if person_id in person_cache:
            return person_cache[person_id]
        path = path_hint or people_by_path.get(person_id)
        if path is None:
            for p in DATA_DIR.glob("people/**/*.yaml"):
                doc = yaml.safe_load(p.read_text())
                if doc and doc.get("id") == person_id:
                    path = p
                    break
        doc = yaml.safe_load(Path(path).read_text()) if path else None
        person_cache[person_id] = (doc, path)
        return person_cache[person_id]

    for (office_type, district, year), group in sorted(groups.items(), key=lambda x: (x[0][0], x[0][1], x[0][2])):
        resolved = resolve_jurisdiction_org_post(office_type, district)
        if not resolved:
            unmapped_districts.add((office_type, district))
            stats["contest_skipped_unmapped"] += 1
            continue
        jurisdiction_id, organization_id, post_id = resolved

        edate = election_date(year)
        if edate >= date.today():
            # Not yet held -- out of scope for this historical-enrichment pass
            # (and OCPF can't have a Winner tag for it yet anyway).
            stats["contest_skipped_future"] += 1
            continue

        election_id = f"{post_id.split('/')[0]}/{edate.isoformat()}/general"
        contest_id = f"{post_id.split('/')[0]}/{edate.isoformat()}/{post_id.split('/')[1]}"

        candidate_person_ids = {}
        for cpf_id, entry in group["candidates"].items():
            filer = entry["filer"]
            person_id, is_new = find_person_match(cpf_id, filer, people_by_ocpf_id, people_by_name)
            if is_new:
                name = (filer.get("fullName") or "").strip() or f"{filer.get('candidateFirstName','')} {filer.get('candidateLastName','')}".strip()
                person_id = f"ocd-person/{bfr.uid(f'ocpf-filer:{cpf_id}')}"
                new_person = {
                    "id": person_id,
                    "name": name,
                    "identifiers": [{"scheme": "ocpf-filer-id", "identifier": str(cpf_id)}],
                    "candidacies": [],
                    **({"image": filer.get("filerPhotoUrl")} if filer.get("filerPhotoUrl") else {}),
                    "verification": {"status": "machine-extracted", "pipeline": "ocpf-filer-registry"},
                    "sources": [{"url": f"https://ocpf.us/filers?q={cpf_id}"}],
                }
                person_cache[person_id] = (new_person, None)
                dirty_people[person_id] = True
                stats["person_new"] += 1
                people_by_name[normalize_name(name)] = {"id": person_id, "name": name}
                people_by_ocpf_id[cpf_id] = person_id
            candidate_person_ids[cpf_id] = person_id

        if not candidate_person_ids:
            continue

        if not group["winners"]:
            # OCPF's own Winner-tag backfill is incomplete for some older
            # elections (e.g. a mayor who served continuously 2004-2020 but
            # only has Winner tags from 2017 on) -- a certified contest
            # can't be written without a winner, and guessing one would be
            # worse than not recording this race at all.
            stats["contest_skipped_no_winner_data"] += 1
            continue

        winners = []
        for winner_cpf_id in group["winners"]:
            if winner_cpf_id not in candidate_person_ids:
                continue
            filer = group["candidates"][winner_cpf_id]["filer"]
            winner_person_id = candidate_person_ids[winner_cpf_id]
            # validate.py's winner-not-seated/name-disagreement checks compare
            # this name field against the linked person's canonical `name` by
            # exact normalized string, not by person_id -- use the person's own
            # name here (OCPF's fullName often carries a middle initial the
            # person record doesn't) so a correctly-matched person doesn't
            # trigger a false mismatch warning.
            person_doc, _ = load_person(winner_person_id)
            canonical_name = person_doc["name"] if person_doc else (filer.get("fullName") or "").strip()
            winners.append({
                "cpf_id": winner_cpf_id,
                "person_id": winner_person_id,
                "name": canonical_name,
                "party": (filer.get("partyAffiliation") or "").strip() or "Unenrolled",
            })

        if not winners:
            # group["winners"] was non-empty, but none of those cpfIds had a
            # matching "On Ballot" candidate entry (the rare case where a
            # Winner tag exists without one) -- same "can't certify without
            # a winner" situation as the group["winners"] check above.
            stats["contest_skipped_no_winner_data"] += 1
            continue

        election_source = {
            "url": f"https://api.ocpf.us/reports/legislative/race/depository/{year}"
                   if office_type in ("House", "Senate") else "https://api.ocpf.us/filers/listings/C",
            "note": f"OCPF filer registry -- {office_type} race, {district}, {year}",
        }

        election_path = DATA_DIR / "elections" / f"{post_id.split('/')[0]}--{edate.isoformat()}--{post_id.split('/')[1]}.yaml"
        if election_path.exists():
            stats["election_existing"] += 1
        else:
            stats["election_new"] += 1
            if write:
                election_doc = {
                    "id": election_id,
                    "name": f"{post_id.split('/')[0]} {edate.isoformat()} general election",
                    "date": edate.isoformat(),
                    "election_type": "general",
                    "status": "certified",
                    "contests": [{
                        "id": contest_id,
                        "jurisdiction_id": jurisdiction_id,
                        "office_id": post_id,
                        "vote_for": 1,
                        "candidate_ids": sorted(set(candidate_person_ids.values())),
                        "result_status": "certified",
                        "winners": [{k: v for k, v in w.items() if k != "cpf_id"} for w in winners] or None,
                        "seat": "At-Large",
                    }],
                    "sources": [election_source],
                }
                election_path.parent.mkdir(parents=True, exist_ok=True)
                election_path.write_text(HEADER + yaml.safe_dump(election_doc, sort_keys=False, allow_unicode=True,
                                                                    default_flow_style=False, width=1000))

        for cpf_id, person_id in candidate_person_ids.items():
            filer = group["candidates"][cpf_id]["filer"]
            doc, path = load_person(person_id)
            if doc is None:
                continue
            existing_contest_ids = {c["contest_id"] for c in doc.get("candidacies", [])}
            if contest_id in existing_contest_ids:
                stats["candidacy_existing"] += 1
                continue
            party = (filer.get("partyAffiliation") or "").strip() or "Unenrolled"
            candidacy = {
                "contest_id": contest_id,
                "election_id": election_id,
                "jurisdiction_id": jurisdiction_id,
                "office_id": post_id,
                "party": party,
                "ballot_name": (filer.get("fullName") or doc["name"]).strip(),
                "status": "active",
                "sources": [{"url": f"https://ocpf.us/filers?q={cpf_id}"}],
            }
            doc.setdefault("candidacies", []).append(candidacy)
            dirty_people[person_id] = True
            stats["candidacy_new"] += 1

        # Deliberately NOT backfilling membership records here (an earlier
        # version of this script did, with no end date). That produced a
        # real bug: Gardner's mayor post had no Phase-B-seeded current
        # officeholder (OCPF's isIncumbent flag was false for everyone there
        # at fetch time), so this fired on the earliest available Winner
        # year (2017) and wrote an open-ended membership for a mayor who
        # was clearly no longer serving (OCPF's own data shows a different
        # winner in 2025) -- a fabricated-looking "still in office" record
        # for someone who wasn't. Candidacies (the actual ask -- historical
        # candidates, wins and losses) are unaffected by this; only
        # officeholder-span backfill was removed. If a post has no current
        # membership at all, that's a real gap worth surfacing by hand
        # rather than guessing at with an unbounded span.
        has_any_membership = bool(post_membership_years.get(post_id))
        if not has_any_membership and winners:
            stats["contest_no_current_membership_on_post"] += 1
            no_current_membership_posts.add(post_id)

    # --- write back dirty person files ---
    if write:
        for person_id in dirty_people:
            doc, path = person_cache[person_id]
            if path is None:
                out = DATA_DIR / "people" / "municipal" / f"{slugify(doc['name'])}.yaml"
                out.parent.mkdir(parents=True, exist_ok=True)
                if out.exists():
                    stats["person_skipped_filename_conflict"] += 1
                    continue
                out.write_text(HEADER + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True,
                                                          default_flow_style=False, width=1000))
            else:
                text = Path(path).read_text()
                header_lines = []
                for line in text.splitlines(keepends=True):
                    if line.startswith("#"):
                        header_lines.append(line)
                    else:
                        break
                existing_header = "".join(header_lines)
                Path(path).write_text(existing_header + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True,
                                                                          default_flow_style=False, width=1000))

    print("==================== SUMMARY ====================")
    print(f"Contest groups found: {len(groups)}")
    print(f"Special-election tags skipped: {special_count}")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    print(f"\nUnmapped districts/cities (no matching jurisdiction/org/post): {len(unmapped_districts)}")
    for office_type, district in sorted(unmapped_districts):
        print(f"  {office_type}: {district!r}")
    print(f"\nPosts with OCPF winner data but NO current membership on file "
          f"(real gap, not backfilled -- needs human follow-up): {len(no_current_membership_posts)}")
    for post_id in sorted(no_current_membership_posts):
        print(f"  {post_id}")


if __name__ == "__main__":
    main()
