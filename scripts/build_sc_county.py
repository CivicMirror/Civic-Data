#!/usr/bin/env python3
"""SC county pass builder — Civic-Data issue #177.

Builds county row offices (Sheriff, Clerk of Court, County Coroner,
County Auditor, County Treasurer, Register of Deeds), County Council
(districts / at-large / separately-elected chairman), County Supervisor,
and circuit Solicitors from the SEC Election History per-office exports
(~/workspace/sc177/county_raw.json). Scope per office+county (or
circuit): the two most recent general elections. Shape follows the
approved probate worked example (PR #185).

Usage: build_sc_county.py [repo] [--counties Charleston,...] [--circuits 9,...]
Default: all counties and circuits.
"""
import json, re, sys, uuid, csv
from pathlib import Path
from collections import defaultdict

ARGS = sys.argv[1:]
REPO = Path(ARGS[0]) if ARGS and not ARGS[0].startswith('--') else Path('/home/hatch/workspace/civic-data-sc177-county')
ONLY_COUNTIES = None
ONLY_CIRCUITS = None
for a in ARGS:
    if a.startswith('--counties='):
        ONLY_COUNTIES = set(a.split('=', 1)[1].split(','))
    if a.startswith('--circuits='):
        ONLY_CIRCUITS = {int(x) for x in a.split('=', 1)[1].split(',')}

RAW = json.load(open('/home/hatch/workspace/sc177/county_raw.json'))
NS = uuid.UUID('6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e')
RETRIEVED = '2026-10-28'
PSEUDO = {'Total Votes Cast', 'Total Ballots Cast', 'Overvotes/Undervotes', 'Write-In', 'Unknown Candidate'}
SC = REPO / 'data/us/sc'
MONTHS = {'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}

def datename(d):
    y, m, day = d.split('-')
    return f"{MONTHS[m]} {int(day)}, {y}"

def slugify(name):
    s = name.lower().replace('.', '').replace(',', '').replace('"', '')
    s = re.sub(r"['’]", '', s)
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def q(s):
    return "'" + s.replace("'", "''") + "'"

def org_uuid(seed):
    return 'ocd-organization/' + str(uuid.uuid5(NS, seed))

def person_uuid(tier, slug):
    return 'ocd-person/' + str(uuid.uuid5(NS, f'person|sc|{tier}|{slug}'))

# Person identity resolution: a base slug belongs to the person whose
# file already carries it (probate pass / worked example) when the name
# matches; a different person with the same slug in another scope gets
# a scope-seeded suffixed file + UUID (filename-standards collision rule).
import yaml as _yaml
FILE_OWNER = {}
for _tier in ('county', 'judicial-district'):
    _dir = SC / f'people/{_tier}'
    if _dir.exists():
        for _f in _dir.glob('*.yaml'):
            try:
                _d = _yaml.safe_load(_f.read_text())
                FILE_OWNER[(_tier, _f.stem)] = _d.get('name', '')
            except Exception:
                pass
CLAIMED = {}
def person_ref(tier, scope, canon_name):
    base = slugify(canon_name)
    owner = FILE_OWNER.get((tier, base))
    if owner is not None and owner == canon_name:
        return base, person_uuid(tier, base)
    if owner is not None and owner != canon_name:
        seed = f'person|sc|{tier}|{scope}|{base}'
        return base + '-' + str(uuid.uuid5(NS, seed))[:8], 'ocd-person/' + str(uuid.uuid5(NS, seed))
    claim = CLAIMED.get((tier, base))
    if claim is None or claim == (scope, canon_name):
        CLAIMED[(tier, base)] = (scope, canon_name)
        return base, person_uuid(tier, base)
    seed = f'person|sc|{tier}|{scope}|{base}'
    return base + '-' + str(uuid.uuid5(NS, seed))[:8], 'ocd-person/' + str(uuid.uuid5(NS, seed))

def named(c):
    return [k for k in c['cands'] if k['name'] not in PSEUDO]

def winners_of(c):
    n = named(c)
    return sorted(n, key=lambda k: -k['votes'])[: c['seats']]

# Name-variant unifications, computed from the exports themselves:
# group ballot forms by (office, county-scope) + token key (initials and
# known nickname tokens dropped, quotes stripped); forms sharing a
# surname and key are one officeholder; canonical = fullest form with
# quotes/periods/commas removed. Council groups are split if two forms
# co-occur in the same election in different districts (two people).
NICK_TOKENS = {'gravedigger', 'buddy', 'billie', 'gene', 'sonny', 'kitty', 'peggi'}
SUFFIXES = {'jr', 'sr', 'ii', 'iii', 'iv'}
DIMIN = {}
for _root, _forms in [('james', ('jim', 'jamie')), ('jeffrey', ('jeff',)), ('christopher', ('chris',)),
                      ('timothy', ('tim',)), ('michael', ('mike',)), ('philip', ('phil',)),
                      ('steven', ('steve',)), ('joseph', ('joe',)), ('ronald', ('ron',)),
                      ('thomas', ('tom',)), ('william', ('bill',)), ('edward', ('ed',)),
                      ('deborah', ('debra', 'debbie')), ('lawrence', ('larry',)), ('daniel', ('dan',)),
                      ('gwendolyn', ('gwen',)), ('kenneth', ('ken',)), ('douglas', ('doug',)),
                      ('anthony', ('tony',)), ('robert', ('bob', 'bobby')), ('richard', ('rick',)),
                      ('charles', ('chuck',)), ('john', ('johnny',)), ('samuel', ('sam',)),
                      ('benjamin', ('ben',)), ('nicholas', ('nick',)), ('andrew', ('andy',)),
                      ('matthew', ('matt',)), ('jonathan', ('jon',)), ('patricia', ('pat', 'patti'))]:
    for _f in _forms:
        DIMIN[_f] = _root
    DIMIN[_root] = _root

def _tokens(name):
    toks = [t.strip('.,').lower() for t in name.replace('"', ' ').split()]
    return [t for t in toks if t]
def _surname(name):
    toks = [t for t in _tokens(name) if t not in SUFFIXES]
    return toks[-1] if toks else ''
def _suffix(name):
    toks = _tokens(name)
    return toks[-1] if toks and toks[-1] in SUFFIXES else ''
def _key(name):
    # quoted nickname tokens and initials dropped
    n = re.sub(r'"[^"]*"', ' ', name)
    toks = [t for t in (t.strip('.,').lower() for t in n.split()) if len(t) > 1 and t not in NICK_TOKENS]
    return frozenset(toks)
def _clean(name):
    return re.sub(r'\s+', ' ', name.replace('"', '').replace('.', '').replace(',', '')).strip()
def _core(name):
    """tokens minus initials and suffix, diminutives rooted, quotes dropped."""
    n = re.sub(r'"[^"]*"', ' ', name)
    out = []
    for t in (t.strip('.,').lower() for t in n.split()):
        if len(t) <= 1 or t in SUFFIXES:
            continue
        out.append(DIMIN.get(t, t))
    return out

CANON = {}
HAND_CANON = {
    ('Bamberg', 'Clerk of Court', 'J. B. "Pedie" Hiers'): 'James Pedie Hiers',
    ('Bamberg', 'Clerk of Court', 'Pedie James Hiers'): 'James Pedie Hiers',
    ('Circuit 3', 'Solicitor', 'Ernest Chip Finney'): 'Ernest Chip Finney III',
    ('Circuit 3', 'Solicitor', 'Ernest "Chip" Finney, III'): 'Ernest Chip Finney III',
    ('Circuit 12', 'Solicitor', 'Ed Clements'): 'Ed Clements III',
    ('Circuit 15', 'Solicitor', 'Jimmy A. Richardson'): 'Jimmy A Richardson II',
}
def _build_canon():
    groups = {}
    for office, cs_all in RAW.items():
        if office == 'Register of Mesne Conveyance':
            continue
        for c in cs_all:
            if c['etype'] != 'General':
                continue
            if office == 'County Council Member':
                county = c['county'] or re.sub(r' \{dt\}.*$', '', c['district_name'])
                if county == 'Chesterfied':
                    county = 'Chesterfield'
            elif office == 'Solicitor':
                county = f"Circuit {c['district_name']}"
            else:
                county = c['district_name']
            for k in named(c):
                groups.setdefault((office, county, _surname(k['name'])), set()).add(k['name'])
    for (office, county, surname), forms in groups.items():
        if len(forms) < 2:
            continue
        # cluster forms: same token key, OR middle spelled/initial match,
        # OR subset with equal suffix status
        forms = sorted(forms)
        clusters = []
        for f in forms:
            placed = False
            for cl in clusters:
                rep = cl[0]
                if _suffix(f) != _suffix(rep):
                    # suffix guard: Jr/Sr/III successions are different
                    # people unless the suffix matches exactly
                    continue
                kf, kr = _key(f), _key(rep)
                cf, cr = _core(f), _core(rep)
                same = False
                if kf == kr:
                    same = True
                elif cf and cr and cf[0] == cr[0]:
                    # first names match (diminutive-rooted); middles must be
                    # initial-compatible or one side absent
                    mf = [t for t in cf[1:-1]] if len(cf) > 2 else []
                    mr = [t for t in cr[1:-1]] if len(cr) > 2 else []
                    if not mf or not mr or any(a[0] == b[0] for a in mf for b in mr):
                        same = True
                elif cf and cr and set(cf) <= set(cr) or (cf and cr and set(cr) <= set(cf)):
                    same = True
                if same:
                    cl.append(f); placed = True; break
            if not placed:
                clusters.append([f])
        for cl in clusters:
            if len(cl) < 2:
                continue
            if office == 'County Council Member':
                # two-people guard: forms in same election, different districts -> split
                seen, split = {}, False
                for c in RAW[office]:
                    if c['etype'] != 'General':
                        continue
                    cc = c['county'] or re.sub(r' \{dt\}.*$', '', c['district_name'])
                    if cc != county:
                        continue
                    for k in named(c):
                        if k['name'] in cl:
                            prev = seen.get((c['date'], k['name']))
                            if prev is not None and prev != c['district_name']:
                                split = True
                            seen[(c['date'], k['name'])] = c['district_name']
                if split:
                    continue
            canonical = _clean(max(cl, key=lambda f: (len(_tokens(f)), len(f))))
            for f in cl:
                if f != canonical:
                    CANON[(county, office, f)] = canonical
    CANON.update(HAND_CANON)
_build_canon()

def canon(county, office, name):
    return CANON.get((county, office, name), name)
def tally_note(c, context, office_label):
    parts = []
    for k in named(c):
        parts.append(f"{k['name']} ({k['party']}) {k['votes']:,}" if k['party'] else f"{k['name']} {k['votes']:,}")
    note = (f"South Carolina State Election Commission, Election History (ElectionStats) results for the "
            f"{datename(c['date'])} general election, {context} {office_label} contest "
            f"(ElectionStats contest {c['contest_id']}), {c['agg'].lower()} rows aggregated: " + '; '.join(parts) + '.')
    if named(c) and all(not k['party'] for k in named(c)):
        note += f" The {c['date'][:4]} export reports no party for any candidate."
    elif any(not k['party'] for k in named(c)):
        note += ' The export reports no party for one or more candidates in this contest.'
    return note

ROW_OFFICES = [
    # export office, post slug, title, org name template
    ('Sheriff', 'sheriff', 'Sheriff', "{C} County Sheriff's Office"),
    ('Clerk of Court', 'clerk-of-court', 'Clerk of Court', '{C} County Clerk of Court'),
    ('County Coroner', 'coroner', 'Coroner', "{C} County Coroner's Office"),
    ('County Auditor', 'county-auditor', 'County Auditor', "{C} County Auditor's Office"),
    ('County Treasurer', 'county-treasurer', 'County Treasurer', "{C} County Treasurer's Office"),
    ('Register of Deeds', 'register-of-deeds', 'Register of Deeds', '{C} County Register of Deeds'),
    ('County Supervisor', 'county-supervisor', 'County Supervisor', "{C} County Supervisor's Office"),
]

for _d in ('organizations/judicial-district', 'posts/judicial-district', 'people/judicial-district',
           'memberships/judicial-district', 'jurisdictions/judicial-district'):
    (SC / _d).mkdir(parents=True, exist_ok=True)

report = {'orgs': 0, 'posts': 0, 'people_new': 0, 'people_merged': 0, 'memberships': 0, 'contests': 0}
election_appends = defaultdict(list)   # date -> [(sortkey, block)]
people_touched = {}                    # (tier, slug) -> dict accumulator

def add_person(tier, county, office, cslug_name, ballot, party, c, contest_id, jur_id, post_id, note):
    slug, pid = person_ref(tier, county, cslug_name)
    key = (tier, slug)
    p = people_touched.setdefault(key, {'name': cslug_name, 'pid': pid, 'cands': [], 'sources': []})
    p['cands'].append({
        'ballot_name': ballot, 'contest_id': contest_id, 'election_id': f"sc/{c['date']}/general",
        'jurisdiction_id': jur_id, 'office_id': post_id, 'party': party, 'date': c['date']})
    p['sources'].append((c['date'], note, c['contest_id']))

def emit_people():
    for (tier, slug), p in sorted(people_touched.items()):
        pid = p['pid']
        path = SC / f'people/{tier}/{slug}.yaml'
        existing = None
        if path.exists():
            import yaml as _y
            _e = _y.safe_load(path.read_text())
            if _e.get('name') == p['name'] or FILE_OWNER.get((tier, slug)) == p['name']:
                existing = _e
        cand_lines, src_lines, seen_c, seen_s = [], [], set(), set()
        all_cands = []
        if existing:
            all_cands.extend(existing.get('candidacies', []))
        for cd in p['cands']:
            entry = {'ballot_name': cd['ballot_name'], 'contest_id': cd['contest_id'],
                     'election_id': cd['election_id'], 'jurisdiction_id': cd['jurisdiction_id'],
                     'office_id': cd['office_id'], 'party': cd['party'], 'status': 'active'}
            if entry['contest_id'] not in {e['contest_id'] for e in all_cands}:
                all_cands.append(entry)
        all_cands.sort(key=lambda e: e['election_id'])
        for e in all_cands:
            cand_lines.append(f"""- ballot_name: {e['ballot_name']}
  contest_id: {e['contest_id']}
  election_id: {e['election_id']}
  jurisdiction_id: {e['jurisdiction_id']}
  office_id: {e['office_id']}
  party: {e['party'] if e['party'] else 'null'}
  status: active""")
        all_srcs = []
        if existing:
            for s in existing.get('sources', []):
                all_srcs.append((s.get('note', ''), s.get('url', '')))
        for date, note, cid in sorted(p['sources']):
            if note not in {n for n, _ in all_srcs}:
                all_srcs.append((note, f'https://electionhistory.scvotes.gov/contest/{cid}'))
        for note, url in all_srcs:
            src_lines.append(f"""- note: {q(note)}
  retrieved: '{RETRIEVED}'
  url: {url}""")
        name = existing['name'] if existing else p['name']
        text = f"""candidacies:
{chr(10).join(cand_lines)}
id: {pid}
identifiers: []
name: {name}
sources:
{chr(10).join(src_lines)}
verification:
  pipeline: build_sc_county
  status: unverified
"""
        if existing:
            report['people_merged'] += 1
        else:
            report['people_new'] += 1
        path.write_text(text)

def membership(path_stem, tier, org_id, pid, post_id, title, start, note, cid, end=None):
    endline = f"\nend: '{end}'" if end else ''
    text = f"""how_seated: elected
id: {path_stem}
organization_id: {org_id}
person_id: {pid}
post_id: {post_id}
role: {title}{endline}
sources:
- note: {q(note)}
  retrieved: '{RETRIEVED}'
  url: https://electionhistory.scvotes.gov/contest/{cid}
start: '{start}'
"""
    (SC / f'memberships/{tier}/{path_stem}.yaml').write_text(text)
    report['memberships'] += 1

def seat_memberships(tier, org_id, post_id, post_stem, title, cycles, county, office_label):
    """cycles: [(contest, [winner candidate dicts])] oldest->newest, single-seat posts."""
    if len(cycles) == 1:
        c, ws = cycles[0]
        for w in ws:
            cn = canon(county, office_label, w['name'])
            fslug, pid = person_ref(tier, county, cn)
            membership(f'{post_stem}-{fslug}', tier, org_id, pid,
                       post_id, title, str(int(c['date'][:4]) + 1), tally_note(c, county, office_label), c['contest_id'])
        return
    (c_old, w_old), (c_new, w_new) = cycles[0], cycles[-1]
    old_names = {canon(county, office_label, w['name']) for w in w_old}
    new_names = {canon(county, office_label, w['name']) for w in w_new}
    for w in w_new:
        cn = canon(county, office_label, w['name'])
        fslug, pid = person_ref(tier, county, cn)
        if cn in old_names:
            note = tally_note(c_old, county, office_label) + ' ' + tally_note(c_new, county, office_label) + \
                   f" One continuous membership from the {c_old['date'][:4]} win."
            membership(f'{post_stem}-{fslug}', tier, org_id, pid,
                       post_id, title, str(int(c_old['date'][:4]) + 1), note, c_old['contest_id'])
        else:
            membership(f'{post_stem}-{fslug}', tier, org_id, pid,
                       post_id, title, str(int(c_new['date'][:4]) + 1), tally_note(c_new, county, office_label), c_new['contest_id'])
    for w in w_old:
        cn = canon(county, office_label, w['name'])
        fslug, pid = person_ref(tier, county, cn)
        if cn not in new_names:
            membership(f'{post_stem}-{fslug}', tier, org_id, pid,
                       post_id, title, str(int(c_old['date'][:4]) + 1), tally_note(c_old, county, office_label),
                       c_old['contest_id'], end=c_new['date'][:4])

def contest_block(c, jur_id, post_id, tier_county, office_label, county_for_canon):
    ws = winners_of(c)
    cand_ids = []
    for k in named(c):
        cn = canon(county_for_canon, office_label, k['name'])
        cand_ids.append(person_ref(tier_county, county_for_canon, cn)[1])
    wlines = []
    for w in ws:
        cn = canon(county_for_canon, office_label, w['name'])
        pl = f"\n    party: {w['party']}" if w['party'] else ''
        wlines.append(f"""  - name: {w['name']}{pl}
    person_id: {person_ref(tier_county, county_for_canon, cn)[1]}
    votes: {w['votes']}""")
    block = f"""- id: sc/{c['date']}/{post_id.replace('/', '-')}
  jurisdiction_id: {jur_id}
  office_id: {post_id}
  vote_for: {c['seats']}
  candidate_ids:
{chr(10).join('  - ' + i for i in cand_ids)}
  result_status: certified
  winners:
{chr(10).join(wlines)}
"""
    election_appends[c['date']].append((post_id, block))
    report['contests'] += 1

def two_recent(contests):
    dates = sorted({c['date'] for c in contests})[-2:]
    return [c for c in sorted(contests, key=lambda c: c['date']) if c['date'] in dates]

def org_and_post(tier, org_file, org_name, org_seed, jur_id, post_id, post_file, title, seats, note, first_cid):
    oid = org_uuid(org_seed)
    org = f"""# Minted from the SC State Election Commission Election History
# official general election results (county pass, Civic-Data
# issue #177).

id: {oid}
name: {org_name}
jurisdiction_id: {jur_id}
identifiers: []
sources:
- url: https://electionhistory.scvotes.gov/contest/{first_cid}
  note: {q(note)}
  retrieved: '{RETRIEVED}'
"""
    (SC / f'organizations/{tier}/{org_file}.yaml').write_text(org)
    report['orgs'] += 1
    post = f"""# Minted from the SC State Election Commission Election History
# official general election results (county pass, Civic-Data
# issue #177).

id: {post_id}
organization_id: {oid}
title: {title}
seats: {seats}
identifiers: []
sources:
- url: https://electionhistory.scvotes.gov/contest/{first_cid}
  note: {q(note)}
  retrieved: '{RETRIEVED}'
"""
    (SC / f'posts/{tier}/{post_file}.yaml').write_text(post)
    report['posts'] += 1
    return oid

# ---------------- county row offices ----------------
counties_seen = set()
for export_office, pslug, title, org_tpl in ROW_OFFICES:
    by_county = defaultdict(list)
    for c in RAW.get(export_office, []):
        if c['etype'] == 'General':
            by_county[c['district_name']].append(c)
    for county, cs in sorted(by_county.items()):
        if ONLY_COUNTIES and county not in ONLY_COUNTIES:
            continue
        counties_seen.add(county)
        cs = two_recent(cs)
        cslug = county.lower().replace(' ', '-')
        jur_id = f'ocd-jurisdiction/country:us/state:sc/county:{cslug}/government'
        post_id = f'{cslug}/{pslug}'
        post_stem = f'{cslug}-{pslug}'
        org_name = org_tpl.format(C=county)
        dlist = ' and '.join(datename(c['date']) for c in cs)
        note = (f'{org_name}, built from the SC State Election Commission Election History results for the '
                f'{dlist} general elections ({title} contests) in the ElectionStats {export_office} export, '
                f'{cs[0]["agg"].lower()} rows aggregated.')
        oid = org_and_post('county', post_stem, org_name, f'organization|sc|county|{post_stem}',
                           jur_id, post_id, post_stem, title, 1, note, cs[0]['contest_id'])
        for c in cs:
            contest_id = f"sc/{c['date']}/{post_id.replace('/', '-')}"
            for k in named(c):
                add_person('county', county, export_office, canon(county, export_office, k['name']),
                           k['name'], k['party'], c, contest_id, jur_id, post_id,
                           tally_note(c, f'{county} County', title))
            contest_block(c, jur_id, post_id, 'county', export_office, county)
        seat_memberships('county', oid, post_id, post_stem, title,
                         [(c, winners_of(c)) for c in cs], county, export_office)

# ---------------- county council (+ chairman) ----------------
COUNTY_NAMES = {p.name[: -len('-government.yaml')].replace('-', ' ').title()
                for p in (SC / 'jurisdictions/county').glob('*-government.yaml')}
COUNTY_NAMES = {n.replace('Mccormick', 'McCormick') for n in COUNTY_NAMES}
def council_county(c):
    county = c['county'] or re.sub(r' \{dt\}.*$', '', c['district_name'])
    if county == 'Chesterfied':
        county = 'Chesterfield'
    return county if county in COUNTY_NAMES else None
council_by_county = defaultdict(list)
for c in RAW.get('County Council Member', []):
    if c['etype'] != 'General':
        continue
    county = council_county(c)
    if county is None:
        continue  # sub-county labels with no county attribution (Jasper's 2012 township contests)
    council_by_county[county].append(c)
chair_by_county = defaultdict(list)
for c in RAW.get('County Council Chairman', []):
    if c['etype'] == 'General':
        chair_by_county[c['district_name']].append(c)

for county, cs_all in sorted(council_by_county.items()):
    if ONLY_COUNTIES and county not in ONLY_COUNTIES:
        continue
    if county == 'Jasper':
        # HELD: Jasper elects council county-wide by residency seat, but
        # the export's contests carry no seat label (2 indistinguishable
        # seats=1 contests in 2022, 4 in 2024) - cannot model posts from
        # this source alone. Flagged to Walter 2026-10-28.
        print('HOLD: Jasper County Council skipped (unlabeled residency-seat contests)')
        continue
    counties_seen.add(county)
    cs = cs_all
    cslug = county.lower().replace(' ', '-')
    jur_id = f'ocd-jurisdiction/country:us/state:sc/county:{cslug}/government'
    org_id = org_uuid(f'organization|sc|county|{cslug}-county-council')
    _scope_dates = sorted({c['date'] for c in cs_all if c['date'] in
                           {cc['date'] for cc in two_recent(cs_all)} or True})
    dlist = ' and '.join(datename(d) for d in sorted({c['date'] for c in cs_all})[-2:])
    note = (f'{county} County Council, built from the SC State Election Commission Election History results for the '
            f'{dlist} general elections (County Council Member contests) in the ElectionStats County Council '
            f'Member export, county rows aggregated where present, otherwise precinct rows.')
    org = f"""# Minted from the SC State Election Commission Election History
# official general election results (county pass, Civic-Data
# issue #177).

id: {org_id}
name: {county} County Council
jurisdiction_id: {jur_id}
identifiers: []
sources:
- url: https://electionhistory.scvotes.gov/contest/{cs[0]['contest_id']}
  note: {q(note)}
  retrieved: '{RETRIEVED}'
"""
    (SC / f'organizations/county/{cslug}-county-council.yaml').write_text(org)
    report['orgs'] += 1

    # group contests by post, then take each post's two most recent dates
    by_post = defaultdict(list)
    for c in cs:
        if c['district_type'] == 'County':
            label, pslug2, ttl = 'At-Large', 'county-council-at-large', 'County Council At-Large'
        else:
            dn = c['district_name'].replace('Chesterfied', 'Chesterfield')
            num = re.sub(r'^.* \{dt\} ', '', dn)
            label, pslug2, ttl = f'District {num}', f'county-council-district-{slugify(num)}', f'County Council District {num}'
        by_post[(pslug2, ttl)].append(c)
    county_dates = sorted({c['date'] for c in cs_all})
    era_floor = county_dates[-2] if len(county_dates) >= 2 else county_dates[-1]
    for (pslug2, ttl), pcs_all in sorted(by_post.items()):
        if max(c['date'] for c in pcs_all) < era_floor:
            continue  # post from an older era (e.g. pre-redistricting district), not a current seat
        pcs = two_recent(pcs_all)
        if pslug2 == 'county-council-at-large' and len(pcs) == 2:
            w_old = {canon(county, 'County Council Member', w['name']) for w in winners_of(pcs[0])}
            w_new = {canon(county, 'County Council Member', w['name']) for w in winners_of(pcs[1])}
            seats = len(w_old) + len(w_new) if not (w_old & w_new) else max(len(w_old), len(w_new))
        elif pslug2 == 'county-council-at-large':
            seats = pcs[0]['seats']
        else:
            seats = 1
        post_id = f'{cslug}/{pslug2}'
        post_stem = f'{cslug}-{pslug2}'
        pnote = (f'{ttl}, {county} County Council, elected to a four-year term. Contests in scope: ' +
                 ' and '.join(f"{datename(c['date'])} (ElectionStats contest {c['contest_id']})" for c in pcs) + '.')
        post = f"""# Minted from the SC State Election Commission Election History
# official general election results (county pass, Civic-Data
# issue #177).

id: {post_id}
organization_id: {org_id}
title: {ttl}
seats: {seats}
identifiers: []
sources:
- url: https://electionhistory.scvotes.gov/contest/{pcs[0]['contest_id']}
  note: {q(pnote)}
  retrieved: '{RETRIEVED}'
"""
        (SC / f'posts/county/{post_stem}.yaml').write_text(post)
        report['posts'] += 1
        for c in pcs:
            contest_id = f"sc/{c['date']}/{post_id.replace('/', '-')}"
            for k in named(c):
                add_person('county', county, 'County Council Member', canon(county, 'County Council Member', k['name']),
                           k['name'], k['party'], c, contest_id, jur_id, post_id,
                           tally_note(c, f'{county} County', ttl))
            contest_block(c, jur_id, post_id, 'county', 'County Council Member', county)
        seat_memberships('county', org_id, post_id, post_stem, ttl,
                         [(c, winners_of(c)) for c in pcs], county, 'County Council Member')

    # separately elected chairman
    if county in chair_by_county:
        chs = two_recent(chair_by_county[county])
        post_id = f'{cslug}/county-council-chairman'
        post_stem = f'{cslug}-county-council-chairman'
        pnote = (f'County Council Chairman of {county} County, elected county-wide separately from the council '
                 f'membership. Contests in scope: ' +
                 ' and '.join(f"{datename(c['date'])} (ElectionStats contest {c['contest_id']})" for c in chs) + '.')
        post = f"""# Minted from the SC State Election Commission Election History
# official general election results (county pass, Civic-Data
# issue #177).

id: {post_id}
organization_id: {org_id}
title: County Council Chairman
seats: 1
identifiers: []
sources:
- url: https://electionhistory.scvotes.gov/contest/{chs[0]['contest_id']}
  note: {q(pnote)}
  retrieved: '{RETRIEVED}'
"""
        (SC / f'posts/county/{post_stem}.yaml').write_text(post)
        report['posts'] += 1
        for c in chs:
            contest_id = f"sc/{c['date']}/{post_id.replace('/', '-')}"
            for k in named(c):
                add_person('county', county, 'County Council Chairman', canon(county, 'County Council Chairman', k['name']),
                           k['name'], k['party'], c, contest_id, jur_id, post_id,
                           tally_note(c, f'{county} County', 'County Council Chairman'))
            contest_block(c, jur_id, post_id, 'county', 'County Council Chairman', county)
        seat_memberships('county', org_id, post_id, post_stem, 'County Council Chairman',
                         [(c, winners_of(c)) for c in chs], county, 'County Council Chairman')

# ---------------- solicitors ----------------
# circuit composition from the CSV's county-division rows (most recent general)
comp = defaultdict(set)
for r in csv.DictReader(open('/home/hatch/workspace/sc177/inputs/solicitor.csv')):
    if r['division_type'] == 'County' and r['election_type'] == 'General':
        comp[int(r['district_name'])].add(r['division_name'])
ORDINALS = {1:'1st',2:'2nd',3:'3rd',4:'4th',5:'5th',6:'6th',7:'7th',8:'8th',9:'9th',10:'10th',11:'11th',12:'12th',13:'13th',14:'14th',15:'15th',16:'16th'}
sol_by_circuit = defaultdict(list)
for c in RAW.get('Solicitor', []):
    if c['etype'] == 'General':
        sol_by_circuit[int(c['district_name'])].append(c)
for circuit, cs_all in sorted(sol_by_circuit.items()):
    if ONLY_CIRCUITS and circuit not in ONLY_CIRCUITS:
        continue
    cs = two_recent(cs_all)
    jur_slug = f'circuit-{circuit}'
    jur_id = f'ocd-jurisdiction/country:us/state:sc/judicial_district:{jur_slug}/judiciary'
    counties_list = ', '.join(sorted(comp[circuit]))
    # jurisdiction scaffold (create only if missing)
    jpath = SC / f'jurisdictions/judicial-district/{jur_slug}.yaml'
    if not jpath.exists():
        jpath.write_text(f"""# Judicial circuit structure for the elected Solicitor; built for
# the SC county pass, Civic-Data issue #177.

id: {jur_id}
name: {ORDINALS[circuit]} Judicial Circuit of South Carolina
state: sc
division_id: ocd-division/country:us/state:sc/judicial_district:{jur_slug}
classification: judiciary
sources:
- url: https://electionhistory.scvotes.gov/contest/{cs[-1]['contest_id']}
  note: 'South Carolina State Election Commission, Election History (ElectionStats): the {ORDINALS[circuit]} Judicial Circuit Solicitor contests are voted in {counties_list} Counties, per the county-division rows of the ElectionStats Solicitor export.'
  retrieved: '{RETRIEVED}'
""")
    post_id = f'{jur_slug}/solicitor'
    post_stem = f'{jur_slug}-solicitor'
    org_name = f"Solicitor, {ORDINALS[circuit]} Judicial Circuit"
    dlist = ' and '.join(datename(c['date']) for c in cs)
    note = (f'{org_name}, built from the SC State Election Commission Election History results for the {dlist} '
            f'general elections (Solicitor contests) in the ElectionStats Solicitor export, county rows '
            f'aggregated. The circuit comprises {counties_list} Counties.')
    oid = org_and_post('judicial-district', post_stem, org_name, f'organization|sc|judicial-district|{post_stem}',
                       jur_id, post_id, post_stem, 'Solicitor', 1, note, cs[0]['contest_id'])
    for c in cs:
        contest_id = f"sc/{c['date']}/{post_id.replace('/', '-')}"
        for k in named(c):
            add_person('judicial-district', f'Circuit {circuit}', 'Solicitor', canon(f'Circuit {circuit}', 'Solicitor', k['name']),
                       k['name'], k['party'], c, contest_id, jur_id, post_id,
                       tally_note(c, f'{ORDINALS[circuit]} Judicial Circuit', 'Solicitor'))
        contest_block(c, jur_id, post_id, 'judicial-district', 'Solicitor', f'Circuit {circuit}')
    seat_memberships('judicial-district', oid, post_id, post_stem, 'Solicitor',
                     [(c, winners_of(c)) for c in cs], f'Circuit {circuit}', 'Solicitor')

emit_people()

# ---------------- election files ----------------
for date, blocks in sorted(election_appends.items()):
    p = SC / f'elections/sc--{date}--general.yaml'
    if not p.exists():
        p.write_text(f"""# Built from the SC State Election Commission Election History
# (ElectionStats) official results for the {datename(date)} general
# election, per-office CSV exports. County pass, Civic-Data
# issue #177.

id: sc/{date}/general
name: South Carolina {date} general election
date: '{date}'
election_type: general
status: certified
contests:
sources:
- url: https://electionhistory.scvotes.gov/search?gf=e
  note: 'SC State Election Commission Election History (ElectionStats): the official historical results system. This record was created by the SC county pass for contests of the {datename(date)} general election.'
  retrieved: '{RETRIEVED}'
""")
    s = p.read_text()
    insert = ''.join(b for pid_, b in sorted(blocks) if f"sc/{date}/{pid_.replace('/', '-')}" not in s)
    if insert:
        assert '\nsources:' in s, date
        s = s.replace('\nsources:', '\n' + insert + 'sources:', 1)
    if 'county pass' not in s:
        note = (f"'County-office contests appended by the SC county pass (Civic-Data issue #177): county row "
                f"offices, county council, and circuit solicitor contests of the {datename(date)} general "
                f"election, aggregated from the Election History per-office CSV exports.'")
        if not s.endswith('\n'):
            s += '\n'
        s += f"""- url: https://electionhistory.scvotes.gov/search?gf=e
  note: {note}
  retrieved: '{RETRIEVED}'
"""
    p.write_text(s)

print(json.dumps({**report, 'counties': len(counties_seen)}, indent=1))
