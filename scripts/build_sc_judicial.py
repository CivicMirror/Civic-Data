#!/usr/bin/env python3
"""SC judicial pass (probate judges) builder — Civic-Data issue #177.

Builds, for all 46 SC counties, the Probate Judge post from the SC State
Election Commission Election History Probate Judge export
(~/workspace/sc177/probate_raw.json, precinct rows aggregated — this
export carries precinct rows only). Scope per county: the two most
recent general elections. Shape approved by Walter 2026-10-28 on the
Charleston worked example. Idempotent: regenerates the Charleston
example files byte-identically.
"""
import json, re, sys, uuid
from pathlib import Path

REPO = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/home/hatch/workspace/civic-data-sc177-judicial')
RAW = json.load(open('/home/hatch/workspace/sc177/probate_raw.json'))
NS = uuid.UUID('6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e')
RETRIEVED = '2026-10-28'
PSEUDO = {'Total Votes Cast', 'Total Ballots Cast', 'Overvotes/Undervotes', 'Write-In', 'Unknown Candidate'}
SC = REPO / 'data/us/sc'

# Hand-verified name-variant unifications (county, ballot form) -> canonical.
CANON = {
    ('Allendale', 'D. Keith Smith'): 'D Keith Smith',
    ('Calhoun', 'Kathy S. Brown'): 'Kathryn Strickland Brown',
    ('Calhoun', 'Kathy Strickland Brown'): 'Kathryn Strickland Brown',
    ('Charleston', 'Irv Condon'): 'Irvin Gerard Condon',
    ('Charleston', 'Irv Gerard Condon'): 'Irvin Gerard Condon',
    ('Chesterfield', 'Gail Ingram'): 'Gail B Ingram',
    ('Clarendon', 'Margaret "Peggi" Jackson Sorrell'): 'Margaret Jackson Sorrell',
    ('Colleton', 'Ashley H. Amundson'): 'Ashley Heaton Amundson',
    ('Greenville', 'Debora Faulkner'): 'Debora A Faulkner',
    ('Laurens', 'Kay W. Fridy'): 'Kaye W Fridy',
    ('McCormick', 'Kathryne "Kitty" Butler'): 'Kathryne P Butler',
    ('McCormick', 'Kathryne "Kitty" P. Butler'): 'Kathryne P Butler',
    ('McCormick', 'Kathryne P. Kitty Butler'): 'Kathryne P Butler',
    ('Oconee', 'Kenny Johns, Jr.'): 'Kenneth E Kenny Johns Jr',
    ('Sumter', 'Dale Atkinson'): 'Dale W Atkinson',
    ('Sumter', 'Dale W. Atkinson'): 'Dale W Atkinson',
    ('Dillon', 'Teresa Campbell'): 'Teresa W Campbell',
    ('Union', 'William D. All, III'): 'William D All III',
}

def slugify(name):
    s = name.lower().replace('.', '').replace(',', '').replace('"', '')
    s = re.sub(r"['’]", '', s)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s

def q(s):
    return "'" + s.replace("'", "''") + "'"

def org_uuid(county_slug):
    return 'ocd-organization/' + str(uuid.uuid5(NS, f'organization|sc|county|{county_slug}-probate-court'))

def person_uuid(person_slug):
    return 'ocd-person/' + str(uuid.uuid5(NS, f'person|sc|county|{person_slug}'))

def named(c):
    return [k for k in c['cands'] if k['name'] not in PSEUDO]

def tally_note(c, county):
    parts = []
    for k in named(c):
        parts.append(f"{k['name']} ({k['party']}) {k['votes']:,}" if k['party'] else f"{k['name']} {k['votes']:,}")
    note = (f"South Carolina State Election Commission, Election History (ElectionStats) results for the "
            f"{datename(c['date'])} general election, {county} County Probate Judge contest "
            f"(ElectionStats contest {c['contest_id']}), precinct rows aggregated: " + '; '.join(parts) + '.')
    if all(not k['party'] for k in named(c)):
        note += f" The {c['date'][:4]} export reports no party for any candidate."
    elif any(not k['party'] for k in named(c)):
        note += ' The export reports no party for one or more candidates in this contest.'
    return note

MONTHS = {'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}
def datename(d):
    y, m, day = d.split('-')
    return f"{MONTHS[m]} {int(day)}, {y}"

# county scaffolds
counties = {}
for p in sorted((SC / 'jurisdictions/county').glob('*-government.yaml')):
    slug = p.name[: -len('-government.yaml')]
    counties[slug] = p

by_county = {}
for c in RAW:
    if c['etype'] == 'General':
        by_county.setdefault(c['county'], []).append(c)

report = {'counties': {}, 'people': 0, 'contests': 0}
election_appends = {}  # date -> [contest blocks]

for county_name in sorted(by_county):
    county_slug = county_name.lower().replace(' ', '-')
    assert county_slug in counties, f'no scaffold for {county_name}'
    jur_id = f'ocd-jurisdiction/country:us/state:sc/county:{county_slug}/government'
    contests = sorted(by_county[county_name], key=lambda c: c['date'])
    dates = sorted({c['date'] for c in contests})[-2:]
    contests = [c for c in contests if c['date'] in dates]
    org_id = org_uuid(county_slug)
    post_id = f'{county_slug}/probate-judge'
    post_file = f'{county_slug}-probate-judge'

    # ballot forms across ALL of the county's generals, per canonical person
    forms = {}
    for c_all in sorted(by_county[county_name], key=lambda c: c['date']):
        for k in named(c_all):
            canon = CANON.get((county_name, k['name']), k['name'])
            forms.setdefault(canon, {}).setdefault(k['name'], []).append(c_all['date'][:4])

    # people: canonical identities across the two contests
    persons = {}  # canonical -> {'slug':, 'cands': [(contest, ballot, party)]}
    for c in contests:
        for k in named(c):
            canon = CANON.get((county_name, k['name']), k['name'])
            persons.setdefault(canon, {'slug': slugify(canon), 'cands': []})
            persons[canon]['cands'].append((c, k['name'], k['party']))

    # winners per contest
    winners = {}
    for c in contests:
        winners[c['contest_id']] = max(named(c), key=lambda k: k['votes'])

    # ---- organization ----
    dlist = ' and '.join(datename(d) for d in dates)
    org = f"""# Minted from the SC State Election Commission Election History
# official general election results (judicial pass, Civic-Data
# issue #177).

id: {org_id}
name: {county_name} County Probate Court
jurisdiction_id: {jur_id}
identifiers: []
sources:
- url: https://electionhistory.scvotes.gov/contest/{contests[0]['contest_id']}
  note: {q(f'{county_name} County Probate Court, built from the SC State Election Commission Election History results for the {dlist} general elections (Probate Judge contests) in the ElectionStats Probate Judge export, precinct rows aggregated (this export carries precinct rows only).')}
  retrieved: '{RETRIEVED}'
"""
    (SC / f'organizations/county/{post_file}.yaml').write_text(org)

    # ---- post ----
    clist = ' and '.join(f"{datename(c['date'])} (ElectionStats contest {c['contest_id']})" for c in contests)
    post = f"""# Minted from the SC State Election Commission Election History
# official general election results (judicial pass, Civic-Data
# issue #177).

id: {post_id}
organization_id: {org_id}
title: Probate Judge
seats: 1
identifiers: []
sources:
- url: https://electionhistory.scvotes.gov/contest/{contests[0]['contest_id']}
  note: {q(f'Probate Judge of {county_name} County, elected county-wide to a four-year term. Contests in scope: {clist}.')}
  retrieved: '{RETRIEVED}'
"""
    (SC / f'posts/county/{post_file}.yaml').write_text(post)

    # ---- people ----
    for canon, info in persons.items():
        pid = person_uuid(info['slug'])
        cand_lines = []
        src_lines = []
        for c, ballot, party in sorted(info['cands'], key=lambda t: t[0]['date']):
            cand_lines.append(f"""- ballot_name: {ballot}
  contest_id: sc/{c['date']}/{post_id.replace('/', '-')}
  election_id: sc/{c['date']}/general
  jurisdiction_id: {jur_id}
  office_id: {post_id}
  party: {party if party else 'null'}
  status: active""")
            note = tally_note(c, county_name)
            if len(src_lines) == 0 and len(forms.get(canon, {})) > 1:
                flist = ', '.join(f"{fname} ({', '.join(years)})" for fname, years in forms[canon].items())
                note += f' Ballot name forms across cycles: {flist} - one officeholder, unified under the fullest certified form.'
            src_lines.append(f"""- note: {q(note)}
  retrieved: '{RETRIEVED}'
  url: https://electionhistory.scvotes.gov/contest/{c['contest_id']}""")
        person = f"""candidacies:
{chr(10).join(cand_lines)}
id: {pid}
identifiers: []
name: {canon}
sources:
{chr(10).join(src_lines)}
verification:
  pipeline: build_sc_judicial
  status: unverified
"""
        (SC / f"people/county/{info['slug']}.yaml").write_text(person)
        report['people'] += 1

    # ---- memberships ----
    seq = [(c, winners[c['contest_id']]) for c in contests]  # oldest -> newest
    (c_old, w_old), (c_new, w_new) = seq[0], seq[-1]
    canon_old = CANON.get((county_name, w_old['name']), w_old['name'])
    canon_new = CANON.get((county_name, w_new['name']), w_new['name'])
    def membership(canon, start, end=None, note_contests=seq):
        pid = person_uuid(slugify(canon))
        notes = []
        for c, w in note_contests:
            notes.append(tally_note(c, county_name))
        note = ' '.join(notes)
        if end is None and len(note_contests) > 1:
            note += f" One continuous membership from the {note_contests[0][0]['date'][:4]} win."
        endline = f"\nend: '{end}'" if end else ''
        return f"""how_seated: elected
id: {post_file}-{slugify(canon)}
organization_id: {org_id}
person_id: {pid}
post_id: {post_id}
role: Probate Judge{endline}
sources:
- note: {q(note)}
  retrieved: '{RETRIEVED}'
  url: https://electionhistory.scvotes.gov/contest/{note_contests[0][0]['contest_id']}
start: '{start}'
"""
    if canon_old == canon_new:
        (SC / f'memberships/county/{post_file}-{slugify(canon_new)}.yaml').write_text(
            membership(canon_new, str(int(c_old['date'][:4]) + 1)))
    else:
        (SC / f'memberships/county/{post_file}-{slugify(canon_old)}.yaml').write_text(
            membership(canon_old, str(int(c_old['date'][:4]) + 1), end=c_new['date'][:4], note_contests=[seq[0]]))
        (SC / f'memberships/county/{post_file}-{slugify(canon_new)}.yaml').write_text(
            membership(canon_new, str(int(c_new['date'][:4]) + 1), note_contests=[seq[-1]]))

    # ---- election contest blocks ----
    for c in contests:
        w = winners[c['contest_id']]
        wcanon = CANON.get((county_name, w['name']), w['name'])
        cand_ids = []
        for k in named(c):
            canon = CANON.get((county_name, k['name']), k['name'])
            cand_ids.append(person_uuid(slugify(canon)))
        party_line = f"\n    party: {w['party']}" if w['party'] else ''
        block = f"""- id: sc/{c['date']}/{post_id.replace('/', '-')}
  jurisdiction_id: {jur_id}
  office_id: {post_id}
  vote_for: 1
  candidate_ids:
{chr(10).join('  - ' + i for i in cand_ids)}
  result_status: certified
  winners:
  - name: {w['name']}{party_line}
    person_id: {person_uuid(slugify(wcanon))}
    votes: {w['votes']}
"""
        election_appends.setdefault(c['date'], []).append((county_slug, block))
        report['contests'] += 1
    report['counties'][county_name] = {'dates': dates, 'people': len(persons)}

# ---- election files: append contest blocks + judicial sources entry ----
SRC_ENTRY = """- url: https://electionhistory.scvotes.gov/search?gf=e
  note: {note}
  retrieved: '2026-10-28'
"""
for date, blocks in sorted(election_appends.items()):
    p = SC / f'elections/sc--{date}--general.yaml'
    s = p.read_text()
    insert = ''.join(b for slug, b in sorted(blocks) if f'sc/{date}/{slug}-probate-judge' not in s)
    assert '\nsources:' in s, date
    if insert:
        s = s.replace('\nsources:', '\n' + insert + 'sources:', 1)
    if 'judicial pass' not in s:
        note = (f"'Probate Judge contests appended by the SC judicial pass (Civic-Data issue #177): the Probate Judge "
                f"contests of the {datename(date)} general election, aggregated from the Election History Probate Judge "
                f"CSV export (precinct rows only; this export carries no county-division rows).'")
        if not s.endswith('\n'):
            s += '\n'
        s += SRC_ENTRY.format(note=note)
    p.write_text(s)

print(json.dumps({'counties': len(report['counties']), 'people': report['people'], 'contests': report['contests']}, indent=1))
