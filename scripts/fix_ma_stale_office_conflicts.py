#!/usr/bin/env python3
"""
Resolve MA municipal offices where a later rolling-audit package re-researched
an office that the v20 import had already seeded.

The import scripts never overwrite, so for these offices the *organization*
record kept its v20 identity while the newer package's persons and memberships
were still imported -- and those memberships reference the newer organization
id, which was never written. The result is a dangling reference: 38 membership
records pointing at organizations that do not exist.

This script adopts the newer research for exactly those offices:

  * the organization record is replaced with the newer package's version
    (new id, title and sources),
  * the post record is replaced too -- its id is the office id and therefore
    unchanged, but its organization_id is repointed at the new organization,
    and any revised title/seat count comes along with it.

Nothing else is touched. Persons and memberships already on disk resolve
cleanly once the organization exists under its newer id; no repo membership
referenced the superseded organization ids (verified before writing).

Idempotent: once the newer records are in place there are no conflicts left
to resolve and a re-run reports zero changes.

Usage: python3 fix_ma_stale_office_conflicts.py [--write]
"""
import importlib.util
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "us" / "ma"

HEADER_TMPL = (
    "# Imported from reference/MA Rolling Audit/ ({version} MA municipal\n"
    "# charter/elected-office rolling audit preservation package, generated\n"
    "# 2026-08-25) by scripts/fix_ma_stale_office_conflicts.py. This office was\n"
    "# originally seeded by the v20 import; {version} re-researched it, and the\n"
    "# newer record supersedes the v20 one. Source rows were machine-extracted\n"
    "# from municipal government sites; see the record's sources for provenance.\n"
)


def load_batches():
    """Reuse the import scripts' own batch lists and loaders."""
    batches = []
    for name in ("import_ma_charter_audit_v32_v49", "import_ma_charter_audit_v56_v58"):
        spec = importlib.util.spec_from_file_location(name, REPO / "scripts" / f"{name}.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for version, src_dir in mod.BATCHES:
            batches.append((version, src_dir, mod))
    return batches


def main():
    write = "--write" in sys.argv[1:]

    new_org, new_post, version_of = {}, {}, {}
    for version, src_dir, mod in load_batches():
        for org in mod.load(src_dir, version, "organizations"):
            office_id = next(
                i["identifier"] for i in org["identifiers"]
                if i["scheme"] == "civicmirror-office"
            )
            new_org[office_id] = org
            version_of[office_id] = version
        for post in mod.load(src_dir, version, "posts"):
            new_post[post["id"]] = post

    # Offices whose repo organization record disagrees with the newer package.
    conflicts = []
    for office_id, org in new_org.items():
        path = DATA_DIR / "organizations" / "municipal" / f"{office_id.replace('/', '-')}.yaml"
        if not path.exists():
            continue
        existing = yaml.safe_load(path.read_text()) or {}
        if existing.get("id") != org["id"]:
            conflicts.append((office_id, existing["id"], org["id"]))

    if not conflicts:
        print("No stale office conflicts remain -- nothing to do.")
        return

    # Safety check: refuse to strand anything that still points at the old ids.
    superseded = {old for _, old, _ in conflicts}
    referencing = []
    for f in (DATA_DIR / "memberships").glob("*/*.yaml"):
        doc = yaml.safe_load(f.read_text()) or {}
        if doc.get("organization_id") in superseded:
            referencing.append(f.name)
    if referencing:
        print(f"ERROR: {len(referencing)} membership(s) still reference the superseded")
        print("organization ids; replacing them would strand those records:")
        for n in referencing[:10]:
            print(f"  {n}")
        sys.exit(1)

    written = 0
    for office_id, old_id, new_id in sorted(conflicts):
        version = version_of[office_id]
        header = HEADER_TMPL.format(version=version)
        stem = office_id.replace("/", "-")

        for kind, doc in (("organizations", new_org[office_id]),
                          ("posts", new_post.get(office_id))):
            if doc is None:
                continue
            path = DATA_DIR / kind / "municipal" / f"{stem}.yaml"
            if write:
                path.write_text(header + yaml.safe_dump(
                    doc, sort_keys=False, allow_unicode=True,
                    default_flow_style=False, width=1000))
            written += 1

        print(f"[{version}] {office_id}")
        print(f"          {old_id}  ->  {new_id}")

    print(f"\n{len(conflicts)} office(s), {written} record(s) "
          f"{'rewritten' if write else 'to rewrite'}.")
    if not write:
        print("\n(dry run -- pass --write to apply)")


if __name__ == "__main__":
    main()
