#!/usr/bin/env python3
"""
Parse the MS Secretary of State's "County Offices and Directory (2026)"
PDF text dump into structured per-county officeholder records.

Elected vs appointed classification comes directly from the document's
own explicit section headers ("COUNTYWIDE OFFICES" / "COUNTY DISTRICT
OFFICES" = elected; "COUNTY APPOINTED OFFICES" = appointed: Board
Attorney, Justice Court Clerk, County Engineer, Superintendent of
Education). Appointed offices are parsed but flagged, not used for
elected-office records.

Three line shapes seen in the pdftotext -layout dump, all handled
generically by tracking a "current office" label:
  1. Inline single-entry: "Chancery Clerk...... Brandi B. Lewis...... address"
  2. Header-only line ("Chancery Court Judges" / "Supervisors" / etc.)
     followed by "District N... NAME... address" or "Post N... NAME...
     address" sub-lines (multi-seat district offices).
  3. Header-only line for a normally-single office in one of the 10
     counties with two judicial-district county seats, followed by
     "First Judicial... NAME... address" / "Second Judicial... NAME...
     address" sub-lines -- same officeholder, two courthouse addresses.
     Collapsed back to one entry per person in post-processing.
"""
import json
import re
import sys

SINGLE_OFFICES = [
    "Tax Assessor and/or Tax Collector",
    "Board Attorney",
    "Chancery Clerk",
    "Circuit Clerk",
    "Tax Assessor",
    "Tax Collector",
    "Coroner",
    "County Administrator",
    "County Court Judge",
    "County Prosecuting Attorney",
    "District Attorney",
    "Justice Court Clerk",
    "Sheriff",
    "Superintendent of Education",
    "County Surveyor",
    "County Engineer",
    "County Comptroller",
    "County Road Manager",
    "Justice Court Administrator",
    "County Court Clerk",
]
SINGLE_OFFICES.sort(key=len, reverse=True)

DISTRICT_OFFICE_HEADERS = [
    "Chancery Court Judges",
    "Circuit Court Judges",
    "Chancery Court Judge",
    "Circuit Court Judge",
    "County Court Judges",
    "Constables",
    "Election Commissioners",
    "Justice Court Judges",
    "Justice Court Clerks",
    "Supervisors",
]

ALL_HEADERS = SINGLE_OFFICES + DISTRICT_OFFICE_HEADERS
APPOINTED = {
    "Board Attorney", "Justice Court Clerk", "Justice Court Clerks", "County Engineer",
    "Superintendent of Education", "County Administrator", "County Comptroller",
    "County Road Manager", "Justice Court Administrator", "County Court Clerk",
}

COUNTY_RE = re.compile(r"^\s{15,}([A-Z][A-Z ]+) COUNTY\s*$")
SUBENTRY_RE = re.compile(
    r"^\s*(District\s+\d+|Post\s+\d+|Beat\s+\d+|Place\s+\d+|Subdistrict\s+\d+|"
    r"First Judicial|Second Judicial|First and Second Judicial|"
    r"First District|Second District|Third District|"
    r"Northern District|Southern District|Eastern District|Western District|"
    r"North District|South District|East District|West District|"
    r"Southeast District|Southwest District|Northeast District|Northwest District|"
    r"Northern|Southern|Eastern|Western)"
    r"[.\s]*?\.{2,}\s*(.+?)\.{2,}\s*(.*)$"
)
SINGLE_LINE_RE = re.compile(
    r"^(" + "|".join(re.escape(l) for l in SINGLE_OFFICES) + r")[.\s]*?\.{2,}\s*(.+?)\.{2,}\s*(.*)$"
)


def clean(s):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\.+$", "", s).strip()
    return s


NAME_ADDR_SPLIT_RE = re.compile(r"^(.*?)[.\s]+((?:P\.O\.|Box\b).*)$")
PHONE_RE = re.compile(r"(\d{3}-\d{3}-\d{4})\s*$")
DOTLEADER_RE = re.compile(r"[.\s]*\.{2,}[.\s]*")


def clean_address(entry):
    addr = entry["address"]
    phone = None
    pm = PHONE_RE.search(addr)
    if pm:
        phone = pm.group(1)
        addr = addr[: pm.start()]
    addr = DOTLEADER_RE.sub(" ", addr)
    entry["address"] = clean(addr)
    entry["phone"] = phone


def fix_merged_name_address(entry):
    """A handful of source lines use a single dot (not the usual 2+ dot
    leader) between name and address, so SINGLE_LINE_RE/SUBENTRY_RE's
    dot-leader split fails and the address gets swallowed into the name.
    Detect and re-split those on the P.O./Box marker."""
    m = NAME_ADDR_SPLIT_RE.match(entry["name"])
    if m:
        entry["name"] = clean(m.group(1))
        entry["address"] = clean(m.group(2)) + (
            (" " + entry["address"]) if entry["address"] else ""
        )
    return entry


def parse(text):
    lines = text.split("\n")
    counties = {}
    current_county = None
    current_office = None

    for raw in lines:
        m = COUNTY_RE.match(raw)
        if m:
            current_county = m.group(1).strip()
            counties.setdefault(current_county, {})  # a repeated header is a "(CONTINUED)" page, not a new county -- never wipe
            current_office = None
            continue
        if current_county is None:
            continue

        stripped = raw.strip()
        if not stripped:
            continue

        # Most specific first: an inline single-entry line carries both the
        # label AND a name/address on one line -- must be checked before the
        # bare-header check, since e.g. "Chancery Clerk....Name...addr" also
        # starts with "Chancery Clerk." and would otherwise be misread as a
        # bare header with no data.
        sm = SINGLE_LINE_RE.match(stripped)
        if sm:
            label, name, addr = sm.group(1), sm.group(2), sm.group(3)
            current_office = label
            counties[current_county].setdefault(label, [])
            counties[current_county][label].append({
                "seat": None,
                "name": clean(name),
                "address": clean(addr),
            })
            continue

        sub = SUBENTRY_RE.match(stripped)
        if sub and current_office:
            seat_label, name, addr = sub.group(1), sub.group(2), sub.group(3)
            counties[current_county][current_office].append({
                "seat": clean(seat_label),
                "name": clean(name),
                "address": clean(addr),
            })
            continue

        header_match = None
        for hdr in ALL_HEADERS:
            if stripped == hdr or re.match(re.escape(hdr) + r"\.\s*$", stripped) or re.match(re.escape(hdr) + r"[.\s]*\.{2,}", stripped):
                header_match = hdr
                break
        if header_match:
            current_office = header_match
            counties[current_county].setdefault(current_office, [])
            continue

    for offices in counties.values():
        for entries in offices.values():
            for entry in entries:
                fix_merged_name_address(entry)
                clean_address(entry)

    # Collapse "First Judicial"/"Second Judicial" duplicates for offices
    # that are structurally single-holder (same name, two courthouses).
    # Runs after cleaning so the joined address/phone are already tidy.
    for offices in counties.values():
        for office in list(offices.keys()):
            entries = offices[office]
            if office in SINGLE_OFFICES and all(
                e["seat"] in ("First Judicial", "Second Judicial", "First District", "Second District") for e in entries
            ):
                names = {e["name"] for e in entries}
                if len(names) == 1:
                    phones = {e["phone"] for e in entries if e["phone"]}
                    offices[office] = [{
                        "seat": None,
                        "name": next(iter(names)),
                        "address": "; ".join(e["address"] for e in entries),
                        "phone": next(iter(phones)) if len(phones) == 1 else "; ".join(sorted(phones)),
                    }]
                # else: leave as-is (genuinely different people per sub-district) -- rare/flagged downstream

    return counties


def main():
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    with open(in_path, encoding="utf-8") as f:
        text = f.read()
    data = parse(text)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Parsed {len(data)} counties -> {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
