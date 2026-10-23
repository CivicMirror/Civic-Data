#!/usr/bin/env python3
"""Build one VT school district (issue #163 school pass): jurisdiction,
board organization, school-director post, people and memberships --
mirroring the MS #158 school layout and the VT house YAML shapes.
Idempotent: skips files that already exist. Usage:
  build_vt_school.py [--write] <spec.json> [<spec.json> ...]
Spec shape:
  {district_slug, district_name, jurisdiction_id (optional; derived),
   division_id (optional; derived), jurisdiction_sources: [S...],
   board: {org_name, post_title, seats, sources: [S...]},
   directors: [{name, slug, how_seated?, end?, sources?}]}
S = {url, note, retrieved}.
"""
import json
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NS = uuid.UUID("6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e")
TODAY = "2026-10-22"
WRITE = "--write" in sys.argv


def oid(kind, key):
    return f"ocd-{kind}/" + str(uuid.uuid5(NS, kind + "|" + key))


def q(s):
    return "'" + str(s).replace("'", "''") + "'"


def wrap(text, indent, first_prefix):
    import textwrap
    return textwrap.fill(text, width=76, initial_indent=first_prefix,
                         subsequent_indent=" " * indent)


def sources_yaml(sources, indent=0):
    pad = " " * indent
    out = []
    for s in sources:
        out.append(f"{pad}- url: {s['url']}")
        note = str(s["note"]).replace("'", "''")
        out.append(wrap(note, indent + 4, f"{pad}  note: '") + "'")
        out.append(f"{pad}  retrieved: {q(s.get('retrieved', TODAY))}")
    return "\n".join(out) + "\n"


def build(spec):
    dslug = spec["district_slug"]
    jid = spec.get("jurisdiction_id",
                   f"ocd-jurisdiction/country:us/state:vt/"
                   f"school_district:{dslug}/school")
    divid = spec.get("division_id",
                     f"ocd-division/country:us/state:vt/"
                     f"school_district:{dslug}")
    board = spec["board"]
    org_id = oid("organization", f"vt|school|{dslug}|school-board")
    post_id = f"{dslug}-school/school-director"
    files = {}

    jpath = f"data/us/vt/jurisdictions/school/{dslug}-school.yaml"
    files[jpath] = (
        "# School-district tier; issue #163 (VT master tracking).\n"
        f"id: {jid}\nname: {spec['district_name']}\nstate: vt\n"
        f"division_id: {divid}\nclassification: school\nsources:\n"
        + sources_yaml(spec["jurisdiction_sources"]))

    opath = (f"data/us/vt/organizations/school/"
             f"{dslug}-school-board.yaml")
    files[opath] = (
        "# School-district tier; issue #163 (VT master tracking).\n"
        f"id: {org_id}\nname: {board['org_name']}\n"
        f"jurisdiction_id: {jid}\nidentifiers:\n"
        "- scheme: civicmirror-office\n"
        f"  identifier: {dslug}-school/school-board\nsources:\n"
        + sources_yaml(board["sources"]))

    ppath = f"data/us/vt/posts/school/{dslug}-school-school-director.yaml"
    files[ppath] = (
        "# School-district tier; issue #163 (VT master tracking).\n"
        f"id: {post_id}\norganization_id: {org_id}\n"
        f"title: {board['post_title']}\nseats: {board['seats']}\n"
        "sources:\n" + sources_yaml(board["sources"]))

    for d in spec["directors"]:
        slug = d["slug"]
        pid = oid("person", f"vt|{dslug}-school|{slug}")
        pfile = f"data/us/vt/people/school/{slug}.yaml"
        dsrc = d.get("sources", board["sources"])
        files[pfile] = (
            f"id: {pid}\nname: {d['name']}\nidentifiers: []\n"
            "candidacies: []\nverification:\n"
            "  status: machine-extracted\n"
            f"  reviewed_on: {q(TODAY)}\n"
            "  pipeline: build_vt_school\nsources:\n"
            + sources_yaml(dsrc))
        mid = f"{dslug}-school-school-director-{slug}"
        mfile = f"data/us/vt/memberships/school/{mid}.yaml"
        body = (f"id: {mid}\nperson_id: {pid}\n"
                f"organization_id: {org_id}\npost_id: {post_id}\n"
                f"role: {board['post_title']}\n"
                f"how_seated: {d.get('how_seated', 'elected')}\n")
        if d.get("end"):
            body += f"end: {q(d['end'])}\n"
        body += "sources:\n" + sources_yaml(dsrc)
        files[mfile] = body

    created = 0
    for rel, content in files.items():
        p = ROOT / rel
        if p.exists():
            print(f"SKIP exists: {rel}")
            continue
        created += 1
        if WRITE:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
            print(f"WROTE: {rel}")
        else:
            print(f"WOULD WRITE: {rel}")
    print(f"{spec['district_name']}: "
          f"{'created' if WRITE else 'would create'} {created} files.")
    return created


def main():
    total = 0
    for arg in sys.argv[1:]:
        if arg == "--write":
            continue
        total += build(json.loads(Path(arg).read_text()))
    print(f"TOTAL: {total} files.")


if __name__ == "__main__":
    main()
