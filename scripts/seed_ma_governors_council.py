#!/usr/bin/env python3
"""
Structure only: generate Jurisdiction, Organization, and Post records for
the Massachusetts Governor's Council's 8 councillor districts (issue #103,
child of #63).

New classification/tier combination for this repo: classification
`executive` on a per-district Jurisdiction, mirroring the existing
Senate/House one-Jurisdiction-per-seat convention (see
jurisdictions/state/first-essex-senate.yaml et al.) rather than one
shared council-wide Organization -- the Organization schema's single
jurisdiction_id can't represent a body spanning 8 districts. Do not
"fix" this to classification `legislature` -- the Governor's Council is
constitutionally an executive-branch advice-and-consent body (Mass.
Const. Pt. 2, Ch. II, Sec. III), even though it is structured like a
legislature.

Composition: MGL c.57 Sec. 2 defines each councillor district as the
union of 5 whole state Senate districts. Verified (not assumed) by a
bijection check against this repo's 40 jurisdictions/state/*-senate.yaml
files before writing this script -- see issue #103's mapping-study
comment for the full derivation and the composition table.

Scope: 8 elected Posts only. The Governor presides over the Council but
has no vote; the Lieutenant Governor is a member ex officio, not
separately elected to the Council -- same exclusion rule already applied
to EAA's 2 appointed non-voting seats (#32) and the Nantucket
Select-Board-as-Commissioners case (#63). Neither is minted here.

Term/cycle citation note: councillors are elected biennially (2-year
term) per Amendments Art. LXXXII (which superseded Art. LXXX, which
superseded Art. LXIV -- verified against the live constitutional text,
not a secondary summary). This is DIFFERENT from the Governor,
Lieutenant Governor, and the other 4 constitutional officers, who are
quadrennial under that same article -- don't assume a uniform statewide
term when minting #63 Phase 1.

No officeholders in this pass, consistent with #63's overall sequencing.

Usage: python3 seed_ma_governors_council.py [--write]
"""
import sys
import uuid
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
JUR_DIR = REPO / "data" / "us" / "ma" / "jurisdictions" / "state"
ORG_DIR = REPO / "data" / "us" / "ma" / "organizations" / "state"
POST_DIR = REPO / "data" / "us" / "ma" / "posts" / "state"

RETRIEVED = "2026-09-29"

STATUTE_URL = "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleVIII/Chapter57/Section2"
CONST_URL = "https://malegislature.gov/Laws/Constitution"

# MGL c.57 Sec. 2, verbatim senatorial-district composition per councillor
# district (bijection-verified against jurisdictions/state/*-senate.yaml;
# see issue #103).
DISTRICTS = {
    "first": [
        "Cape and Islands", "First Bristol and Plymouth",
        "Second Bristol and Plymouth", "Third Bristol and Plymouth",
        "Plymouth and Barnstable",
    ],
    "second": [
        "Bristol and Norfolk", "Middlesex and Norfolk",
        "Norfolk, Plymouth and Bristol", "Norfolk, Worcester and Middlesex",
        "Second Plymouth and Norfolk",
    ],
    "third": [
        "Third Middlesex", "Fourth Middlesex", "Middlesex and Worcester",
        "Norfolk and Middlesex", "Suffolk and Middlesex",
    ],
    "fourth": [
        "Norfolk and Plymouth", "Norfolk and Suffolk",
        "First Plymouth and Norfolk", "First Suffolk", "Second Suffolk",
    ],
    "fifth": [
        "First Essex", "Second Essex", "First Essex and Middlesex",
        "Second Essex and Middlesex", "First Middlesex",
    ],
    "sixth": [
        "Third Essex", "Second Middlesex", "Fifth Middlesex",
        "Middlesex and Suffolk", "Third Suffolk",
    ],
    "seventh": [
        "First Worcester", "Second Worcester", "Worcester and Hampden",
        "Worcester and Hampshire", "Worcester and Middlesex",
    ],
    "eighth": [
        "Berkshire, Hampden, Franklin and Hampshire", "Hampden",
        "Hampden, Hampshire and Worcester", "Hampden and Hampshire",
        "Hampshire, Franklin and Worcester",
    ],
}

ORDINAL_NAMES = {
    "first": "First", "second": "Second", "third": "Third",
    "fourth": "Fourth", "fifth": "Fifth", "sixth": "Sixth",
    "seventh": "Seventh", "eighth": "Eighth",
}


def uid(seed):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))


def dump(doc):
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True,
                           default_flow_style=False, width=1000)


HEADER = (
    "# Structure only -- current officeholders not yet researched.\n"
    "# classification `executive` is deliberate, not a mistake: the\n"
    "# Governor's Council is a constitutionally executive-branch body\n"
    "# (Mass. Const. Pt. 2, Ch. II, Sec. III) even though it is\n"
    "# structured like a legislature. See issue #103's mapping-study\n"
    "# comment for the full derivation of this district's composition.\n"
)


def main():
    write = "--write" in sys.argv[1:]

    for key, senate_districts in DISTRICTS.items():
        ordinal = ORDINAL_NAMES[key]
        slug = f"{key}-councillor"

        senate_note = "; ".join(senate_districts)
        jur_id = f"ocd-jurisdiction/country:us/state:ma/councillor_district:{key}/executive"
        div_id = f"ocd-division/country:us/state:ma/councillor_district:{key}"
        org_id = f"ocd-organization/{uid(f'ma-governors-council|{key}')}"

        sources = [
            {
                "url": STATUTE_URL,
                "note": (
                    f"MGL c.57 Sec. 2 defines the {ordinal} Councillor District "
                    f"as the union of five contiguous Senate districts: "
                    f"{senate_note}. Verified via a bijection check against "
                    f"this repo's 40 jurisdictions/state/*-senate.yaml files "
                    f"-- see issue #103."
                ),
                "retrieved": RETRIEVED,
            },
            {
                "url": CONST_URL,
                "note": (
                    "Amendments Art. XVI establishes the 8 elected councillor "
                    "districts (one per district, each composed of 5 "
                    "contiguous senatorial districts once the commonwealth "
                    "has 40 such districts) and a 5-year MA residency "
                    "requirement for candidacy. Amendments Art. LXXXII "
                    "(superseding Arts. LXIV and LXXX) sets the councillor's "
                    "term: elected biennially, term begins at noon the "
                    "Thursday after the first Wednesday in January following "
                    "election and ends the same way in the third year "
                    "following election -- distinct from the Governor/Lt. "
                    "Governor/other 4 constitutional officers, who are "
                    "quadrennial under the same article. Const. Pt. 2, Ch. "
                    "II, Sec. III, Art. I: the Governor presides over the "
                    "Council without a vote; the Lieutenant Governor is "
                    "always a member ex officio -- neither is separately "
                    "elected to the Council, so neither is minted here."
                ),
                "retrieved": RETRIEVED,
            },
        ]

        jur_doc = {
            "id": jur_id,
            "name": f"{ordinal} Councillor District (Massachusetts Governor's Council)",
            "state": "ma",
            "division_id": div_id,
            "classification": "executive",
            "government_form": "single-member district (Massachusetts Governor's Council)",
            "sources": sources,
        }
        org_doc = {
            "id": org_id,
            "name": f"Massachusetts Governor's Council -- {ordinal} District",
            "jurisdiction_id": jur_id,
            "identifiers": [],
            "sources": sources,
        }
        post_doc = {
            "id": f"{slug}/councillor",
            "organization_id": org_id,
            "title": "Governor's Councillor",
            "seats": 1,
            "identifiers": [],
            "sources": sources,
        }

        if write:
            (JUR_DIR / f"{slug}.yaml").write_text(HEADER + dump(jur_doc))
            (ORG_DIR / f"{slug}.yaml").write_text(HEADER + dump(org_doc))
            (POST_DIR / f"{slug}.yaml").write_text(HEADER + dump(post_doc))
            print(f"wrote {slug}")
        else:
            print(f"(dry run) would write {slug}: {jur_id}")

    if not write:
        print("\n(dry run -- pass --write to create files)")


if __name__ == "__main__":
    main()
