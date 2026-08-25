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
    "judge); stisd.net's board page (checked 2026-08-25) names only 12 of "
    "24 seats, so even manual sourcing is incomplete -- not a standard "
    "elected structure and not fully rosterable from what's public.",
    "101912": "Houston ISD -- single-member district numbers given as roman "
    "numerals (I, II, ... IX), not arabic numerals. Also: TEA suspended the "
    "elected board's governance in June 2023 (HB 1842) in favor of a "
    "Commissioner-appointed Board of Managers -- seeding the 9 elected "
    "trustees as current officeholders would be actively false. Needs a "
    "user decision on how to model an elected-board-in-name-only district, "
    "not mechanical templating.",
    "232903": "Uvalde CISD -- hybrid with 4 SMD seats but only two named "
    "districts ('East' and 'West', not 4 numbered districts); ucisd.net's "
    "board page (checked 2026-08-25) doesn't resolve the East/West to "
    "4-seat mapping either -- still needs individual sourcing.",
}

# Districts where BBB(LOCAL) alone under- or misclassifies the structure but
# a hand-verified secondary source resolves it completely. Kept separate
# from parse_district()'s regex path (rather than loosening the regexes) so
# a one-off documented exception can't silently change classification for
# any of the other 862 at-large districts.
MANUAL_OVERRIDES = {
    "235902": {  # Victoria ISD
        "board_size": 7,
        "at_large_seats": 2,
        "smd_seats": 5,
        "smd_district_numbers": [1, 2, 3, 4, 5],
        "note": (
            "BBB(LOCAL)'s Method of Election sentence says only 'by "
            "single-member districts' (the pure-SMD regex path then failed "
            "on a district-number-count mismatch), but the Terms and "
            "Election Schedule immediately below it explicitly names "
            "'Districts 2 and 4', 'District 1', and 'Districts 3 and 5' for "
            "5 SMD seats plus 2 at-large seats -- verified by hand against "
            "https://pol.tasb.org/PolicyOnline?key=1191, re-fetched "
            "2026-08-25, text unchanged from the 2026-08-24 committed row."
        ),
    },
    "057912": {  # Irving ISD
        "board_size": 7,
        "at_large_seats": 0,
        "smd_seats": 7,
        "smd_district_numbers": [1, 2, 3, 4, 5, 6, 7],
        "note": (
            "BBB(LOCAL) confirms a 7-member, pure single-member-district "
            "board but never states the district numbers in its own text. "
            "Numbers verified against "
            "https://www.irvingisd.net/board-of-trustees/map-of-trustee-districts "
            "(checked 2026-08-25), which shows districts 1-7 each with a "
            "named current trustee."
        ),
    },
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
    """Union of all district/area numbers mentioned anywhere in the text.

    Caught via San Antonio ISD (015907): its text reads "Districts 1, 3, 4,
    & 7 2021, 2025, 2029, 2033, and so forth" -- the election-year list runs
    on immediately after the district list with only a space between them,
    so DISTRICT_NUMS_RE's greedy digit/separator class swept the years into
    the same capture. No real district has 3-digit numbering, so tokens >=
    100 are dropped as year-list bleed rather than genuine district numbers.
    """
    nums = set()
    for m in DISTRICT_NUMS_RE.finditer(text):
        chunk = m.group(1)
        # Split on whitespace too, not just [,&]/"and" -- San Antonio's text
        # runs a district number straight into the following year with only
        # a space ("& 7 2021, 2025, ..."), so a comma/and-only split leaves
        # "7 2021" as one non-digit token and silently drops the 7.
        for tok in re.split(r"[,&\s]+|\band\b", chunk):
            tok = tok.strip()
            if tok.isdigit() and int(tok) < 100:
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
    if cdn in MANUAL_OVERRIDES:
        return dict(MANUAL_OVERRIDES[cdn])

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
