#!/usr/bin/env python3
"""
Backfill MA executive-body (Select Board / Town or City Council / Mayor)
officeholders for issue #34's 246-town gap, using CivicPatch/open-data
(https://github.com/CivicPatch/open-data, CC0-1.0) as the source.

See reference/MA CivicPatch Comparison/ for the prior structural comparison
between this repo and CivicPatch that motivated this pass, and the raw
source files committed under
reference/MA CivicPatch Comparison/civicpatch-open-data-ma-local/.

SCOPE: only the 246 municipalities issue #34 lists as never covered by
issue #16's research (ISSUE_34_SLUGS below, frozen from the issue body as
filed). Re-verifying the 105 municipalities #16 already covered is out of
scope here, per #34's own non-goals.

SAFETY MODEL (see issue #34 discussion): the import is deliberately
conservative rather than a blind bulk load. Per town:

  1. Determine which family CivicPatch's role_ids for that town belong to:
     "board" (select-board-* and council-* are one family here -- a town
     can't have both as separate real bodies, so role_ids mixing the two
     are CivicPatch's own labeling noise, not a structural split; verified
     by checking every observed mixed-role-id town against this repo,
     where only one such post ever exists) or "mayor" (genuinely
     independent -- MA cities routinely elect both a Mayor and a Council).
  2. Resolve that family to an existing post under
     data/us/ma/posts/municipal/{slug}*.yaml by matching the post title
     (not by guessing a filename pattern -- title conventions vary:
     "Select Board Member", "Selectboard Member", "Board of Selectmen
     (Member)", "Town/City Council(l)or/Member", "Mayor of X", etc.). Zero
     or more-than-one matching post is a skip (structure gap or a genuine
     multi-seat-type ambiguity), not a create -- that's issue #34's own
     Stage 1 concern, and this import surfaces it for free rather than
     papering over it.
  3. A post that already has ANY existing memberships is skipped entirely,
     not diffed/merged -- CivicPatch and a prior partial import agreeing or
     disagreeing on names is a human call, not an auto-merge (a handful of
     the 246 have partial coverage from unrelated later work; see #34's
     note on Boston/Everett).
  4. A town where CivicPatch's holder count exceeds the post's `seats` is
     skipped -- that's a structure gap (the post is under-sized), not a
     reason to write more memberships than the post declares seats for.

Person identity is namespaced by (place, post, name) -- CivicPatch ships
its own UUIDs, which are a different id space and are not reused as
ocd-person ids.

Idempotent by id AND by filename -- never overwrites. Dry run by default;
pass --write to create files.
"""
import argparse
import re
import sys
import unicodedata
import uuid
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "ma"
CIVICPATCH_DIR = REPO / "reference" / "MA CivicPatch Comparison" / "civicpatch-open-data-ma-local"

NS = uuid.UUID("2f6f6a2f-2f9b-5c1a-9d6a-3e6f9c2a4b1d")

CIVICPATCH_SOURCE_NOTE = "CivicPatch/open-data (github.com/CivicPatch/open-data), MA local officeholder data, CC0-1.0"

HEADER = (
    "# Imported from CivicPatch/open-data (github.com/CivicPatch/open-data,\n"
    "# CC0-1.0) by scripts/import_ma_civicpatch_execboard.py. See issue #34.\n"
    "# Each person's own source_urls (an official town page) are carried as\n"
    "# this record's sources. Machine-extracted, pending human sign-off.\n"
)

# Extracted programmatically from issue #34's municipality-ledger table
# (regex over the "Jurisdiction Record" column's GitHub link, which names
# the actual data/us/ma/jurisdictions/municipal/{slug}-government.yaml file
# -- not the display name, which has inconsistent "City of X Town" noise
# that doesn't roundtrip through slugify cleanly).
ISSUE_34_SLUGS = set("""
agawam amesbury attleboro becket beverly boston braintree brockton
charlemont chicopee deerfield dover dracut dudley dunstable duxbury
east-bridgewater east-brookfield east-longmeadow eastham easthampton
edgartown egremont erving essex everett fairhaven fall-river fitchburg
florida foxborough framingham franklin freetown gardner georgetown gill
gloucester goshen gosnold grafton granby granville great-barrington
greenfield groton groveland hadley halifax hamilton hampden hancock hanover
hanson hardwick harvard harwich hatfield haverhill hawley heath hingham
hinsdale holbrook holden holliston holyoke hopedale hopkinton hudson hull
huntington ipswich kingston lakeville lancaster lanesborough lawrence lee
leicester lenox leominster lexington littleton longmeadow ludlow lunenburg
lynn lynnfield malden manchester-by-the-sea mansfield marblehead marion
marlborough marshfield mashpee mattapoisett maynard medfield medford medway
melrose mendon merrimac methuen middleborough middlefield middleton milford
millbury millis millville milton monroe monson montague monterey montgomery
mt-washington nahant nantucket natick needham new-bedford new-braintree
new-marlborough new-salem newbury newburyport newton norfolk north-adams
north-andover north-attleborough north-brookfield north-reading northampton
northborough northbridge northfield norwood oak-bluffs oakham orange orleans
otis oxford palmer paxton peabody pelham pembroke pepperell peru petersham
phillipston pittsfield plainfield plainville plymouth plympton princeton
provincetown quincy randolph raynham reading rehoboth revere richmond
rochester rockland rockport rowe rowley royalston russell rutland salem
salisbury sandisfield sandwich saugus savoy scituate seekonk sharon sherborn
shirley shrewsbury shutesbury somerset somerville south-hadley southampton
southborough southbridge spencer springfield sterling stockbridge stoneham
stoughton stow sturbridge sudbury sunderland sutton taunton templeton upton
waltham warren washington wayland wellesley wenham west-boylston
west-bridgewater west-brookfield west-newbury west-springfield
west-stockbridge west-tisbury westfield westford westhampton westminster
weston westport westwood weymouth whately whitman wilbraham williamsburg
williamstown wilmington winchester windsor winthrop woburn worcester
wrentham yarmouth
""".split())


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def normalize_person_name(name: str) -> str:
    name = re.sub(r"[.,]", "", name).strip().casefold()
    name = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", name).strip()
    return re.sub(r"\s+", " ", name)


# select-board-* and council-* are treated as ONE family ("board") for post
# lookup: a town can't have both a Select Board and a Town/City Council as
# separate real bodies (one supersedes the other under a charter change), so
# a file mixing the two role_id sets is CivicPatch's own labeling noise, not
# a genuine structural split -- confirmed by spot-checking every observed
# mixed-role-id town (sherborn, hanson, oxford) against this repo, where
# only ONE such post exists in each case. mayor is genuinely independent:
# MA cities routinely elect both a Mayor and a Council.
BOARD_ROLE_IDS = {
    "select-board-member", "select-board-chair", "select-board-vice-chair",
    "council-member", "council-president", "council-vice-president",
}
MAYOR_ROLE_IDS = {"mayor"}
GENERIC_ROLE_IDS = {"chair", "vice-chair", "clerk"}
EXCLUDED_ROLE_IDS = {"moderator", "unmatched"}

TITLE_PATTERNS = {
    # Covers every legacy/current naming this repo actually uses for the
    # town's single legislative/executive board: "Select Board Member",
    # "Selectboard Member", "Board of Selectmen (Member)", "Selectman",
    # "Town/City Council(l)or(Member)".
    "board": re.compile(
        r"select\s*board|board\s+of\s+select(?:men|wom[ae]n|persons?)|select(?:man|woman|person)|council(?:or|lor)?",
        re.IGNORECASE,
    ),
    "mayor": re.compile(r"\bmayor\b", re.IGNORECASE),
}


def classify_family(role_ids_in_file):
    families = set()
    if role_ids_in_file & BOARD_ROLE_IDS:
        families.add("board")
    if role_ids_in_file & MAYOR_ROLE_IDS:
        families.add("mayor")
    return families


def load_jurisdiction_index():
    index = {}
    for path in (DATA_DIR / "jurisdictions" / "municipal").glob("*-government.yaml"):
        doc = yaml.safe_load(path.read_text()) or {}
        if doc.get("id"):
            index[doc["id"]] = path.stem[: -len("-government")]
    return index


def find_matching_posts(slug, family):
    posts_dir = DATA_DIR / "posts" / "municipal"
    pattern = TITLE_PATTERNS[family]
    matches = []
    for path in posts_dir.glob(f"{slug}*.yaml"):
        doc = yaml.safe_load(path.read_text()) or {}
        title = doc.get("title", "")
        # Guard against a prefix collision (e.g. "west-newbury" matching a
        # "westborough*" glob) -- the post's own jurisdiction-scoped id must
        # start with this exact slug segment, not just the filename prefix.
        post_id = doc.get("id", "")
        post_slug = post_id.split("/")[0].removesuffix("-ma")
        if post_slug != slug:
            continue
        if pattern.search(title):
            matches.append(doc)
    return matches


def build_post_membership_counts():
    counts = Counter()
    for path in (DATA_DIR / "memberships" / "municipal").glob("*.yaml"):
        doc = yaml.safe_load(path.read_text()) or {}
        if doc.get("post_id"):
            counts[doc["post_id"]] += 1
    return counts


class Recorder:
    def __init__(self, write):
        self.write = write
        self.stats = Counter()

    def emit(self, kind, doc, filename):
        singular = kind.rstrip("s") if kind != "people" else "people"
        path = DATA_DIR / kind / "municipal" / filename
        if path.exists():
            existing = yaml.safe_load(path.read_text()) or {}
            if existing.get("id") == doc["id"]:
                self.stats[f"{singular}_existing"] += 1
            else:
                self.stats[f"{singular}_skipped_filename_conflict"] += 1
            return False
        self.stats[f"{singular}_new"] += 1
        if self.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            text = HEADER + yaml.safe_dump(
                doc, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000
            )
            path.write_text(text)
        return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    jurisdiction_index = load_jurisdiction_index()
    post_membership_counts = build_post_membership_counts()
    rec = Recorder(args.write)
    skips = Counter()
    skip_examples = {}
    imported_towns = []

    people_dir = DATA_DIR / "people" / "municipal"
    existing_id_by_slug = {}
    if people_dir.exists():
        for p in people_dir.glob("*.yaml"):
            doc = yaml.safe_load(p.read_text()) or {}
            existing_id_by_slug[p.stem] = doc.get("id")
    taken_people_slugs = set(existing_id_by_slug)

    for cp_path in sorted(CIVICPATCH_DIR.glob("*.yml")):
        people = yaml.safe_load(cp_path.read_text()) or []
        if not people:
            continue

        # Resolve jurisdiction: strip CivicPatch's optional county segment
        # before matching this repo's county-less municipal jurisdiction ids.
        first_role = next((r for p in people for r in p.get("roles", [])), None)
        if not first_role:
            continue
        jurisdiction_ocdid = re.sub(r"county:[a-z-]+/", "", first_role["jurisdiction_ocdid"])
        jurisdiction_ocdid = jurisdiction_ocdid.replace("_", "-")
        jurisdiction_ocdid = re.sub(r"-town/government$", "/government", jurisdiction_ocdid)
        slug = jurisdiction_index.get(jurisdiction_ocdid)
        if slug is None:
            skips["no_jurisdiction_match"] += 1
            skip_examples.setdefault("no_jurisdiction_match", []).append(jurisdiction_ocdid)
            continue
        if slug not in ISSUE_34_SLUGS:
            continue  # in scope for #16 already (or a name issue #34 didn't list) -- not this pass

        role_ids_in_file = {r["role_id"] for p in people for r in p.get("roles", []) if r["role_id"] not in EXCLUDED_ROLE_IDS}
        qualified_families = classify_family(role_ids_in_file - GENERIC_ROLE_IDS)

        if qualified_families:
            families_to_process = sorted(qualified_families)
            # Generic officer titles (chair/vice-chair/clerk) with no body
            # marker belong to "board" -- mayor is a singular office with
            # no "member"-style board seat, so it never carries these.
            generic_target = "board" if "board" in qualified_families else None
        else:
            # Every role in this file is generic (chair/vice-chair/clerk),
            # no qualified board-*/mayor marker at all -- CivicPatch's own
            # scrape lost the body name. Fall back to resolving via which
            # single family has exactly one matching post for this town.
            candidates = [fam for fam in ("board", "mayor") if len(find_matching_posts(slug, fam)) == 1]
            if len(candidates) != 1:
                skips["ambiguous_or_no_family"] += 1
                skip_examples.setdefault("ambiguous_or_no_family", []).append(
                    (slug, sorted(role_ids_in_file), "post-fallback:", candidates)
                )
                continue
            families_to_process = candidates
            generic_target = candidates[0] if candidates[0] == "board" else None

        for family in families_to_process:
            matches = find_matching_posts(slug, family)
            if len(matches) == 0:
                skips["no_post_match"] += 1
                skip_examples.setdefault("no_post_match", []).append((slug, family))
                continue
            if len(matches) > 1:
                skips["multiple_post_matches"] += 1
                skip_examples.setdefault("multiple_post_matches", []).append((slug, family, [m["title"] for m in matches]))
                continue
            post = matches[0]
            post_id = post["id"]
            organization_id = post["organization_id"]
            title = post["title"]
            seats = post["seats"]

            if post_membership_counts[post_id] > 0:
                skips["already_has_holders"] += 1
                continue

            family_role_ids = BOARD_ROLE_IDS if family == "board" else MAYOR_ROLE_IDS
            if family == generic_target:
                family_role_ids = family_role_ids | GENERIC_ROLE_IDS

            holders = [p for p in people
                       if family_role_ids & {r["role_id"] for r in p.get("roles", [])}]
            if len(holders) > seats:
                skips["seat_count_exceeds_post"] += 1
                skip_examples.setdefault("seat_count_exceeds_post", []).append((slug, family, len(holders), seats))
                continue
            if len(holders) == 0:
                skips["no_holders_in_file"] += 1
                continue

            town_people = []
            town_memberships = []
            for person in holders:
                name = person["name"]
                person_id = f"ocd-person/{uuid.uuid5(NS, f'ma-civicpatch|{slug}|{post_id}|{name}')}"
                source_urls = person.get("source_urls") or [cp_path.as_posix()]
                retrieved = (person.get("updated_at") or "")[:10] or "2026-09-06"
                sources = [{"url": u, "note": CIVICPATCH_SOURCE_NOTE, "retrieved": retrieved} for u in source_urls]

                person_doc = {
                    "id": person_id,
                    "name": name,
                    "candidacies": [],
                    "verification": {
                        "status": "machine-extracted",
                        "reviewed_on": "2026-09-06",
                        "pipeline": "import_ma_civicpatch_execboard",
                    },
                    "sources": sources,
                }
                if person.get("phones"):
                    person_doc["contact"] = {"phone": person["phones"][0]}

                role = next(iter(person.get("roles", [])))
                end = role.get("end_date")
                mem_id = f"{slug}-ma-{slugify(title)}-{slugify(name)}"
                mem_doc = {
                    "id": mem_id,
                    "person_id": person_id,
                    "organization_id": organization_id,
                    "post_id": post_id,
                    "role": title,
                    "how_seated": "elected",
                    "sources": sources,
                }
                if end:
                    mem_doc["end"] = str(end)
                town_people.append((slug, person_doc))
                town_memberships.append((mem_id, mem_doc))

            for slug_, person_doc in town_people:
                base_slug = slugify(person_doc["name"])
                if existing_id_by_slug.get(base_slug) == person_doc["id"]:
                    candidate = base_slug
                else:
                    candidate = base_slug
                    if candidate in taken_people_slugs:
                        candidate = f"{base_slug}-{slug_}"
                    if existing_id_by_slug.get(candidate) == person_doc["id"]:
                        pass
                    elif candidate in taken_people_slugs:
                        suffix = person_doc["id"].rsplit("/", 1)[-1][:8]
                        candidate = f"{base_slug}-{slug_}-{suffix}"
                taken_people_slugs.add(candidate)
                rec.emit("people", person_doc, f"{candidate}.yaml")

            for mem_id, mem_doc in town_memberships:
                rec.emit("memberships", mem_doc, f"{mem_id}.yaml")

            imported_towns.append((slug, family, title, len(holders), seats))

    print(f"Towns imported: {len(imported_towns)}")
    for slug, family, title, n, seats in imported_towns:
        print(f"  {slug}: {family} -> '{title}' ({n}/{seats} seats)")
    print()
    print("==================== SKIPS ====================")
    for k, v in sorted(skips.items()):
        print(f"{k}: {v}")
        for ex in skip_examples.get(k, [])[:8]:
            print(f"    {ex}")
    print()
    print("==================== WRITE SUMMARY ====================")
    for k in sorted(rec.stats):
        print(f"{k}: {rec.stats[k]}")
    if not args.write:
        print("\n(dry run -- pass --write to create files)")


if __name__ == "__main__":
    sys.exit(main())
