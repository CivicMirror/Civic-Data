#!/usr/bin/env python3
"""
Parse each in-scope TX ISD's BBB(LOCAL) text (tx_isd_bbb_local_2026-08-24.csv)
into a structured seat plan: total board size, and how those seats split
between an at-large bloc and single-member-district/area seats (by actual
number, not assumed 1..N).

Report-only by design (--write does nothing here on purpose; see
tx_isd_generate_posts.py for the generator that consumes this module's
parse_district()). Every failure mode is a named, counted skip -- never a
guessed default -- because a wrong seat count or wrong district number
becomes a wrong Post id that Phase 3 memberships would then reference.

Classification is re-derived from ONLY the "Method of Election[:] ..."
sentence, not the whole document -- the original heuristic in
tx_isd_bbb_local_extract.py scanned the full text and false-positived on
generic "Method of Voting" boilerplate that mentions at-large/by-position/
single-member-district generically regardless of which one actually applies
to the district (caught via Rockspings ISD, tagged hybrid by the old
heuristic on boilerplate text, actually plain by-position). "Cumulative
voting" is a vote-counting detail of an at-large seat, not a different seat
structure, and collapses into the at_large bucket here.

Usage: python3 tx_isd_parse_structure.py
"""
import csv
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent / "tx_isd_bbb_local_2026-08-24.csv"

EXCLUDED_TAGS = {"appointed_special_district", "excluded_non_isd_separate_statute"}

# Districts confirmed by hand to need individual research, not mechanical
# templating -- do not add to this set without a documented reason.
MANUAL_REVIEW_CDNS = {
    "031916": "South Texas ISD -- 24-member board, mixed elected/appointed "
    "by county commissioner precinct (some seats appointed by the county "
    "judge), not a standard elected structure at all.",
    "101912": "Houston ISD -- single-member district numbers given as roman "
    "numerals (I, II, ... IX), not arabic numerals; not worth generalizing "
    "the parser for one district.",
    "232903": "Uvalde CISD -- hybrid with 4 SMD seats but only two named "
    "districts ('East' and 'West', not 4 numbered districts); the East/West "
    "to 4-seat mapping isn't stated and needs individual sourcing.",
    "057912": "Irving ISD -- BBB(LOCAL) confirms single-member districts and "
    "a 7-member board but never states the district numbers anywhere in the "
    "text (just 'the relevant single-member district', generically).",
    "235902": "Victoria ISD -- BBB(LOCAL)'s Method of Election sentence says "
    "only 'by single-member districts', omitting that the Terms and Election "
    "Schedule below it clearly describes a 2 at-large + 5 SMD hybrid; the "
    "district's own summary sentence is incomplete/inconsistent with its own "
    "schedule text.",
}

WORDS_TO_NUM = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
}

MOE_RE = re.compile(
    r"Method [Oo]f Election(?: [Aa]nd [Ss]election)?:?\s*(.*?)"
    r"(?=\s*(?:Ballot Statement|Election Date|Terms and Election Schedule|$))",
    re.S,
)
BOARD_SIZE_RE = re.compile(r"consist(?:s)?\s*(?:of)?\s+([\w-]+) members", re.I)
AT_LARGE_COUNT_RE = re.compile(
    r"([\w-]+) (?:Board members?|Trustees?) (?:shall be elected|shall be)? ?at large",
    re.I,
)
SMD_COUNT_RE = re.compile(
    r"([\w-]+) (?:Board members?|Trustees?) (?:shall be elected|shall be)? ?"
    r"(?:by|from) (?:single-member district|area)",
    re.I,
)
# "Districts 1, 3, 4, & 7" / "Areas 2 and 4" / "District 5" / "single-member
# district numbers 1 and 4" / "Places 1, 3, 6, and 7" / "Districts (Places) 3
# and 7" / "Districts (Wards) 1 and 7" -- capture the number list after the
# label, tolerating an optional "(Places)"/"(Wards)" alias in parens.
DISTRICT_NUMS_RE = re.compile(
    r"(?:[Dd]istricts?|[Aa]reas?|[Pp]laces?)(?:\s*\([A-Za-z]+\))?(?:\s+numbers?)?\s+"
    r"([0-9][0-9,\s&and]*[0-9]|[0-9])",
)


def to_int(word):
    word = word.strip().lower()
    if word.isdigit():
        return int(word)
    return WORDS_TO_NUM.get(word)


def extract_district_numbers(text):
    """Union of all district/area numbers mentioned anywhere in the text."""
    nums = set()
    for m in DISTRICT_NUMS_RE.finditer(text):
        chunk = m.group(1)
        for tok in re.split(r"[,&]|\band\b", chunk):
            tok = tok.strip()
            if tok.isdigit():
                nums.add(int(tok))
    return nums


def parse_district(cdn, local_text):
    """
    Returns a dict describing the seat plan, or {"skip_reason": "..."}.

    Shape on success:
      {"board_size": int, "at_large_seats": int, "smd_seats": int,
       "smd_district_numbers": sorted list of int}
    at_large_seats + smd_seats always == board_size. Pure at-large (any
    flavor) has smd_seats == 0 and smd_district_numbers == []. Pure SMD has
    at_large_seats == 0.
    """
    if cdn in MANUAL_REVIEW_CDNS:
        return {"skip_reason": f"manual_review: {MANUAL_REVIEW_CDNS[cdn]}"}

    moe_match = MOE_RE.search(local_text)
    moe_sentence = moe_match.group(1) if moe_match else ""

    size_match = BOARD_SIZE_RE.search(local_text)
    board_size = to_int(size_match.group(1)) if size_match else None

    t = moe_sentence.lower()
    has_smd = "single-member district" in t or "single member district" in t or "by area" in t
    has_at_large = "at large" in t or "at-large" in t
    has_by_position = "by position" in t or "by place" in t

    if not moe_sentence.strip():
        # San Antonio ISD's only known case: no Membership/Method-of-Election
        # restatement in BBB(LOCAL) at all, just the SMD assignment directly.
        # Board size must come from the SMD numbers themselves, which is only
        # trustworthy when the ENTIRE board is single-member (no way to
        # separately confirm an at-large portion exists without the sentence).
        nums = extract_district_numbers(local_text)
        if not nums:
            return {"skip_reason": "no_method_of_election_sentence_and_no_district_numbers"}
        return {
            "board_size": len(nums),
            "at_large_seats": 0,
            "smd_seats": len(nums),
            "smd_district_numbers": sorted(nums),
            "note": "board size inferred from SMD district-number count; no Method of Election sentence in source",
        }

    if board_size is None:
        return {"skip_reason": "no_board_size_match"}

    if has_smd and (has_at_large or has_by_position):
        al_match = AT_LARGE_COUNT_RE.search(local_text)
        smd_match = SMD_COUNT_RE.search(local_text)
        if not al_match or not smd_match:
            return {"skip_reason": "hybrid_but_at_large_or_smd_count_not_found"}
        at_large_seats = to_int(al_match.group(1))
        smd_seats = to_int(smd_match.group(1))
        if at_large_seats is None or smd_seats is None:
            return {"skip_reason": "hybrid_count_word_not_recognized"}
        if at_large_seats + smd_seats != board_size:
            return {
                "skip_reason": (
                    f"hybrid_sum_mismatch: at_large={at_large_seats} + "
                    f"smd={smd_seats} != board_size={board_size}"
                )
            }
        # "Places" numbers the AT-LARGE seats in some districts (e.g. Judson,
        # Stanton ISDs: "At Large Places 6 and 7") but the SMD seats in
        # others (e.g. Brownwood ISD: "single-member districts that are
        # designated as places"). Scanning the whole document for district
        # numbers conflates the two in hybrid docs -- scope the search to the
        # "Single-Member District(s)" subsection specifically, which every
        # hybrid district's Terms and Election Schedule uses as a subheading
        # before its SMD seat list.
        # "single-member district(s)" isn't a one-time heading -- it repeats
        # inside the per-seat list itself ("...district numbers 1 and 4...",
        # "...district numbers 2, 3, and 5...") and again in the trailing
        # Method of Voting boilerplate, so splitting on every occurrence
        # shreds the very list we want. Anchor on the END of the SMD_COUNT_RE
        # match instead (the "Five Board members shall be elected by
        # single-member districts for..." sentence that starts the per-seat
        # list) and read everything from there up to Method of Voting.
        smd_tail = local_text[smd_match.end():]
        smd_tail = re.split(r"Method [Oo]f Voting", smd_tail)[0]
        nums = extract_district_numbers(smd_tail)
        if len(nums) != smd_seats:
            return {
                "skip_reason": (
                    f"hybrid_district_number_count_mismatch: found {len(nums)} "
                    f"distinct numbers {sorted(nums)}, expected {smd_seats}"
                )
            }
        return {
            "board_size": board_size,
            "at_large_seats": at_large_seats,
            "smd_seats": smd_seats,
            "smd_district_numbers": sorted(nums),
        }

    if has_smd:
        nums = extract_district_numbers(local_text)
        if len(nums) != board_size:
            return {
                "skip_reason": (
                    f"smd_district_number_count_mismatch: found {len(nums)} "
                    f"distinct numbers {sorted(nums)}, expected board_size={board_size}"
                )
            }
        return {
            "board_size": board_size,
            "at_large_seats": 0,
            "smd_seats": board_size,
            "smd_district_numbers": sorted(nums),
        }

    # Plain at-large / at-large-by-position / at-large-cumulative: one Post,
    # seats == board_size, no SMD component. Cumulative voting is a
    # vote-counting detail of an at-large seat, not a different seat
    # structure -- deliberately not distinguished here (post.schema.json has
    # no field for it anyway).
    if has_at_large or has_by_position:
        return {
            "board_size": board_size,
            "at_large_seats": board_size,
            "smd_seats": 0,
            "smd_district_numbers": [],
        }

    return {"skip_reason": "method_of_election_sentence_unrecognized"}


def main():
    from collections import Counter

    rows = list(csv.DictReader(SRC.open(newline="")))
    scoped = [r for r in rows if r["heuristic_structure"] not in EXCLUDED_TAGS]

    ok = 0
    skip_reasons = Counter()
    shape_counts = Counter()
    for r in scoped:
        result = parse_district(r["tea_cdn"], r["local_text"])
        if "skip_reason" in result:
            reason_key = result["skip_reason"].split(":")[0]
            skip_reasons[reason_key] += 1
            print(f"SKIP  {r['tea_cdn']} {r['tea_district_name']:30s} {result['skip_reason']}")
            continue
        ok += 1
        if result["at_large_seats"] and result["smd_seats"]:
            shape_counts["hybrid"] += 1
        elif result["smd_seats"]:
            shape_counts["pure_smd"] += 1
        else:
            shape_counts["pure_at_large"] += 1

    print()
    print("==================== SUMMARY ====================")
    print(f"in scope: {len(scoped)}")
    print(f"parsed ok: {ok}")
    print(f"skipped: {len(scoped) - ok}")
    print("skip reasons:", dict(skip_reasons))
    print("shapes:", dict(shape_counts))


if __name__ == "__main__":
    main()
