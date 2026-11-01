#!/usr/bin/env python3
"""SC school districts pass (Civic-Data #177) — Phase 1 worked example.

Builds ONE district (Jasper County) from the SC State Election Commission
Election History (ElectionStats) school-board contest data extracted via the
ElectionStats search API into ~/workspace/sc177/schools_raw.json. (Totals
verified equivalent to the per-office CSV export aggregation on control
contest 2531, Soil-Water District Commissioner, Charleston: Barr 62,720 /
Hanvey 50,175 / Write-In 953 / Total Votes Cast 113,848 — exact match.)

Shape (house conventions from the county / soil & water passes):
- Jurisdiction: jurisdictions/school/<slug>-school.yaml,
  id ocd-jurisdiction/country:us/state:sc/school_district:<slug>/school,
  classification 'school' (MA/TX pattern).
- Organization: the district's governing board (multi-post body, so the org
  filename names the body: <slug>-school-board.yaml).
- Posts: one single-seat post per single-member district
  ('<slug>/school-board-district-<n>', title 'School Board District <n>').
- Scope: the district's two most recent general-election cycles in the data.
  Winners = top `number_seats` named candidates by contest totals; the
  unnamed Write-In aggregate never seats anyone. Cross-check per contest:
  named + Write-In == Total Votes Cast.
- Memberships: start = year after the win (quoted string); repeat winners get
  one continuous membership; replaced holders end at the successor's election
  year. Party: blank in a nonpartisan contest -> 'Nonpartisan'.
- Person identity: county-pass rules (disk-owner + claim registry, token-key
  variant clustering, strict suffix guard, same-contest co-occurrence guard).
"""
import json, re, sys, uuid
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
SC = ROOT / 'data/us/sc'
RAW = Path.home() / 'workspace/sc177/schools_raw.json'
NS = uuid.UUID('6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e')
RETRIEVED = '2026-10-28'
TIER = 'school'
PSEUDO = {'Total Votes Cast', 'Total Ballots Cast', 'Overvotes', 'Undervotes',
          'Write-In', 'Unknown Candidate', 'Overvotes/Undervotes'}
MONTHS = {'01': 'January', '02': 'February', '03': 'March', '04': 'April',
          '05': 'May', '06': 'June', '07': 'July', '08': 'August',
          '09': 'September', '10': 'October', '11': 'November', '12': 'December'}

HEADER = ("# Minted from the SC State Election Commission Election History\n"
          "# official general election results (schools pass, Civic-Data\n"
          "# issue #177).\n\n")

DISTRICTS = [
    {
        'slug': 'jasper-county',
        'name': 'Jasper County School District',
        'board_name': 'Jasper County Board of Education',
        'county': 'Jasper',
        'division_prefix': 'Jasper County School District',
        'office_label': 'School Board Member',
        'structure_note': ("The Jasper County Board of Education is, ex officio, the board of "
                           "trustees of the Jasper County School District (Act 278 of 1985, as "
                           "amended by Act 476 of 1998): nine members elected in nonpartisan "
                           "elections at the general election from nine single-member districts "
                           "to staggered four-year terms (Districts 2, 4, 6, and 8 elected in "
                           "midterm cycles; Districts 1, 3, 5, 7, and 9 in presidential cycles). "
                           "The single-member districts were reapportioned by Act 240 of 2024 "
                           "beginning with the 2024 general election."),
        'jur_sources': [
            ('http://www.scstatehouse.gov/sess112_1997-1998/bills/964.htm',
             "Act 476 of 1998 (amending Act 278 of 1985): the Jasper County Board of Education "
             "is ex officio the board of trustees of the Jasper County School District; nine "
             "members elected from single-member districts to four-year terms."),
            ('https://www.scstatehouse.gov/sess125_2023-2024/bills/782.htm',
             "Act 240 of 2024: the nine single-member districts from which members of the "
             "Jasper County School Board of Trustees must be elected beginning with the 2024 "
             "general election."),
        ],
    },
]


def datename(d):
    y, m, day = d.split('-')
    return f"{MONTHS[m]} {int(day)}, {y}"


def slugify(name):
    s = name.lower().replace('.', '').replace(',', '').replace('"', '')
    s = re.sub(r"['’]", '', s)
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def q(s):
    return "'" + s.replace("'", "''") + "'"


def person_uuid(seed_slug, scope=None):
    if scope is None:
        return 'ocd-person/' + str(uuid.uuid5(NS, f'person|sc|{TIER}|{seed_slug}'))
    return 'ocd-person/' + str(uuid.uuid5(NS, f'person|sc|{TIER}|{scope}|{seed_slug}'))


def org_uuid(district_slug):
    return 'ocd-organization/' + str(uuid.uuid5(NS, f'organization|sc|{TIER}|{district_slug}'))


# ---------------------------------------------------------------- clustering
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
    n = re.sub(r'"[^"]*"', ' ', name)
    return frozenset(t for t in (t.strip('.,').lower() for t in n.split())
                     if len(t) > 1 and t not in NICK_TOKENS)


def _clean(name):
    return re.sub(r'\s+', ' ', name.replace('"', '').replace('.', '').replace(',', '')).strip()


def _core(name):
    n = re.sub(r'"[^"]*"', ' ', name)
    out = []
    for t in (t.strip('.,').lower() for t in n.split()):
        if len(t) <= 1 or t in SUFFIXES:
            continue
        out.append(DIMIN.get(t, t))
    return out


def build_canon(forms_by_scope, cooccur):
    canon, clusters_of = {}, {}
    for scope, forms in forms_by_scope.items():
        groups = defaultdict(set)
        for f in forms:
            groups[_surname(f)].add(f)
        for surname, fs in groups.items():
            if len(fs) < 2:
                continue
            clusters = []
            for f in sorted(fs):
                placed = False
                for cl in clusters:
                    rep = cl[0]
                    if _suffix(f) != _suffix(rep):
                        continue
                    if any(m in cooccur[f] for m in cl):
                        continue
                    kf, kr = _key(f), _key(rep)
                    cf, cr = _core(f), _core(rep)
                    same = False
                    if kf == kr:
                        same = True
                    elif cf and cr and cf[0] == cr[0]:
                        mf = cf[1:-1] if len(cf) > 2 else []
                        mr = cr[1:-1] if len(cr) > 2 else []
                        if not mf or not mr or any(a[0] == b[0] for a in mf for b in mr):
                            same = True
                    elif cf and cr and (set(cf) <= set(cr) or set(cr) <= set(cf)):
                        same = True
                    if same:
                        cl.append(f)
                        placed = True
                        break
                if not placed:
                    clusters.append([f])
            for cl in clusters:
                if len(cl) < 2:
                    continue
                canonical = _clean(max(cl, key=lambda f: (len(_tokens(f)), len(f))))
                clusters_of[(scope, canonical)] = sorted(cl)
                for f in cl:
                    if f != canonical:
                        canon[(scope, f)] = canonical
    return canon, clusters_of


# ---------------------------------------------------------------- extraction
def load_contests():
    raw = json.load(open(RAW))
    contests = {}
    for oid, rows in raw.items():
        for c in rows:
            if c['office'] is not None:
                contests[c['id']] = c
    return contests


def named(c):
    return sorted([(k['name'], k['votes'], k['party']) for k in c['cands']
                   if k['name'] not in PSEUDO and not k['pseudo']],
                  key=lambda x: -x[1])


def writein(c):
    return sum(k['votes'] for k in c['cands'] if k['name'] == 'Write-In')


def tvc(c):
    return sum(k['votes'] for k in c['cands'] if k['name'] == 'Total Votes Cast')


def check(c):
    return sum(v for _, v, _ in named(c)) + writein(c) == tvc(c)


def seat_of(cfg, c):
    """Single-member district number for a contest, or None."""
    div = c['division'] or ''
    pre = cfg['division_prefix']
    if div == pre:
        return None
    m = re.fullmatch(re.escape(pre) + r' (\d+)', div)
    if m:
        return int(m.group(1))
    return 'UNKNOWN:' + div


def tally_note(c, cfg, seat):
    parts = [f"{n} ({p}) {v:,}" if p else f"{n} {v:,}" for n, v, p in named(c)]
    seat_txt = f"District {seat} " if seat else ""
    return (f"South Carolina State Election Commission, Election History (ElectionStats) results "
            f"for the {datename(c['date'])} general election, {cfg['name']} {seat_txt}contest "
            f"(ElectionStats contest {c['id']}), contest totals: " + '; '.join(parts) + '.')


# ---------------------------------------------------------------- people index
import yaml as _yaml
import csv as _csv


def load_people_index():
    town_county = {}
    muni_csv = Path.home() / 'workspace/sc177/inputs/city_council.csv'
    if muni_csv.exists():
        for r in _csv.DictReader(open(muni_csv)):
            if r['division_type'] == 'County':
                town_county[r['district_name']] = r['division_name']
    index = defaultdict(list)
    for tierdir in sorted((SC / 'people').iterdir()):
        for f in sorted(tierdir.glob('*.yaml')):
            try:
                d = _yaml.safe_load(f.read_text())
            except Exception:
                continue
            counties = set()
            for c in d.get('candidacies') or []:
                jid = c.get('jurisdiction_id', '')
                m = re.search(r'/county:([a-z-]+)/', jid)
                if m:
                    counties.add(m.group(1).replace('-', ' ').title())
                m = re.search(r'/place:([a-z-]+)/', jid)
                if m:
                    town = m.group(1).replace('-', ' ').title()
                    if town in town_county:
                        counties.add(town_county[town])
                for s in d.get('sources') or []:
                    mm = re.search(r'\(([A-Z][a-z]+(?: [A-Z][a-z]+)?) County\)', s.get('note', ''))
                    if mm:
                        counties.add(mm.group(1))
            index[d['name']].append({'tier': tierdir.name, 'slug': f.stem, 'id': d['id'],
                                     'path': f, 'counties': counties, 'data': d})
    return index


FILE_OWNER = {}
CLAIMED = {}


def main():
    contests = load_contests()
    people_index = load_people_index()
    for f in (SC / f'people/{TIER}').glob('*.yaml') if (SC / f'people/{TIER}').exists() else []:
        FILE_OWNER[f.stem] = _yaml.safe_load(f.read_text()).get('name', '')

    report = {'districts': []}
    election_appends = defaultdict(list)
    merges = []
    people_touched = {}

    for cfg in DISTRICTS:
        dslug = cfg['slug']
        jur_id = f'ocd-jurisdiction/country:us/state:sc/school_district:{dslug}/school'
        div_id = f'ocd-division/country:us/state:sc/school_district:{dslug}'
        oid = org_uuid(dslug)
        org_stem = f'{dslug}-school-board'
        scoped = [c for c in contests.values()
                  if c['office'] == cfg['office_label'] and c['etype'] == 'General'
                  and (c['division'] or '') == cfg['division_prefix']
                  or c['office'] == cfg['office_label'] and c['etype'] == 'General'
                  and (c['division'] or '').startswith(cfg['division_prefix'] + ' ')]
        dates = sorted({c['date'] for c in scoped})[-2:]
        scoped = [c for c in scoped if c['date'] in dates]
        assert scoped, f"no scoped contests for {cfg['name']}"
        bad = [c['id'] for c in scoped if not check(c)]
        assert not bad, f"Total Votes Cast cross-check failed: {bad}"

        # variant clustering within this district's scope
        forms_by_scope = defaultdict(set)
        cooccur = defaultdict(set)
        per_contest = defaultdict(set)
        for c in scoped:
            for n, v, p in named(c):
                per_contest[c['id']].add(n)
        for cid, names in per_contest.items():
            for n in names:
                forms_by_scope[dslug].add(n)
                for m in names:
                    if m != n:
                        cooccur[n].add(m)
        canon, clusters_of = build_canon(forms_by_scope, cooccur)

        drep = {'district': cfg['name'], 'cycles': dates, 'people_new': 0, 'people_merged': 0,
                'memberships': 0, 'contests': 0, 'unifications': [], 'seats_unfilled': []}

        def resolve_person(canonical):
            for e in people_index.get(canonical, []):
                if e['tier'] == TIER:
                    return ('new', e['slug'], e['id'], e)
                if cfg['county'] in e['counties']:
                    return ('existing', e['slug'], e['id'], e)
            base = slugify(canonical)
            owner = FILE_OWNER.get(base)
            if owner is not None and owner != canonical:
                slug = base + '-' + str(uuid.uuid5(NS, f'person|sc|{TIER}|{dslug}|{base}'))[:8]
                return ('new', slug, person_uuid(base, dslug), None)
            claim = CLAIMED.get(base)
            if claim is None or claim == (dslug, canonical):
                CLAIMED[base] = (dslug, canonical)
                FILE_OWNER[base] = canonical
                return ('new', base, person_uuid(base), None)
            slug = base + '-' + str(uuid.uuid5(NS, f'person|sc|{TIER}|{dslug}|{base}'))[:8]
            return ('new', slug, person_uuid(base, dslug), None)

        # organize contests by seat
        by_seat = defaultdict(list)
        for c in sorted(scoped, key=lambda c: c['date']):
            by_seat[seat_of(cfg, c)].append(c)
        seats_sorted = sorted(by_seat, key=lambda s: (s is None, s))

        cycles_txt = ' and '.join(f"{datename(d)}" for d in dates)
        org_note = (f"{cfg['name']}, built from the SC State Election Commission Election History "
                    f"results for the {cycles_txt} general elections ({cfg['office_label']} "
                    f"contests) in the ElectionStats school board data. {cfg['structure_note']}")
        first_cid = sorted(scoped, key=lambda c: c['date'])[0]['id']

        # jurisdiction
        jur_src = '\n'.join(
            f"- url: {u}\n  note: {q(n)}\n  retrieved: '{RETRIEVED}'" for u, n in cfg['jur_sources'])
        (SC / f'jurisdictions/{TIER}').mkdir(exist_ok=True)
        (SC / f'jurisdictions/{TIER}/{dslug}-school.yaml').write_text(HEADER + f"""id: {jur_id}
name: {cfg['name']}
state: sc
division_id: {div_id}
classification: school
sources:
{jur_src}
""")
        # organization
        (SC / f'organizations/{TIER}').mkdir(exist_ok=True)
        (SC / f'organizations/{TIER}/{org_stem}.yaml').write_text(HEADER + f"""id: {oid}
name: {cfg['board_name']}
jurisdiction_id: {jur_id}
identifiers: []
sources:
- url: https://electionhistory.scvotes.gov/contest/{first_cid}
  note: {q(org_note)}
  retrieved: '{RETRIEVED}'
""")

        for seat in seats_sorted:
            cs = by_seat[seat]
            if seat is None:
                post_id = f'{dslug}/trustee-at-large'
                post_stem = f'{org_stem}-trustee-at-large'
                title = 'School Board Trustee At-Large'
                n_seats = cs[0]['seats']
            else:
                post_id = f'{dslug}/school-board-district-{seat}'
                post_stem = f'{org_stem}-district-{seat}'
                title = f'School Board District {seat}'
                n_seats = 1
            (SC / f'posts/{TIER}').mkdir(exist_ok=True)
            (SC / f'posts/{TIER}/{post_stem}.yaml').write_text(HEADER + f"""id: {post_id}
organization_id: {oid}
title: {title}
seats: {n_seats}
identifiers: []
sources:
- url: https://electionhistory.scvotes.gov/contest/{cs[0]['id']}
  note: {q(org_note)}
  retrieved: '{RETRIEVED}'
""")
            # people + candidacies + election blocks
            seat_winners = {}   # canonical -> (first_win_contest, [contests won])
            prev_winners = None
            for c in cs:
                note = tally_note(c, cfg, seat)
                cands = named(c)
                winners = cands[:c['seats']]
                cand_ids = []
                for raw, votes, party in cands:
                    canonical = canon.get((dslug, raw), raw)
                    kind, pslug, pid, entry = resolve_person(canonical)
                    cand_ids.append(pid)
                    cand = {'ballot_name': raw, 'contest_id': f"sc/{c['date']}/{post_id.replace('/', '-')}",
                            'election_id': f"sc/{c['date']}/general", 'jurisdiction_id': jur_id,
                            'office_id': post_id, 'party': party or 'Nonpartisan'}
                    if kind == 'existing':
                        merges.append((entry, cand, note, c['id']))
                    else:
                        acc = people_touched.setdefault((pslug, pid), {
                            'name': canonical, 'slug': pslug, 'pid': pid, 'cands': [], 'sources': [],
                            'cluster_forms': clusters_of.get((dslug, canonical))})
                        if cand not in acc['cands']:
                            acc['cands'].append(cand)
                        if (note, c['id']) not in acc['sources']:
                            acc['sources'].append((note, c['id']))
                # winners bookkeeping for membership continuity
                cur = {}
                for raw, votes, party in winners:
                    canonical = canon.get((dslug, raw), raw)
                    cur[canonical] = c
                    if canonical in seat_winners:
                        seat_winners[canonical][1].append(c)
                    else:
                        seat_winners[canonical] = (c, [c])
                if prev_winners is not None:
                    for old_canonical in prev_winners:
                        if old_canonical not in cur:
                            pass  # handled at membership emit via seat_winners + last-win check
                prev_winners = cur
                # election block
                if cand_ids:
                    wlines = []
                    for raw, votes, party in winners:
                        canonical = canon.get((dslug, raw), raw)
                        _, _, pid, _ = resolve_person(canonical)
                        wlines.append(f"""  - name: {raw}
    party: {party or 'Nonpartisan'}
    person_id: {pid}
    votes: {votes}""")
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
                else:
                    block = f"""- id: sc/{c['date']}/{post_id.replace('/', '-')}
  jurisdiction_id: {jur_id}
  office_id: {post_id}
  vote_for: {c['seats']}
  candidate_ids: []
  result_status: official
  winners: []
"""
                    drep['seats_unfilled'].append((c['date'], seat))
                election_appends[c['date']].append((post_id, block))
                drep['contests'] += 1
            # memberships: one per winner; start at first in-scope win; a winner
            # whose seat was later won by someone else ends at that election year
            last_date = cs[-1]['date']
            final_winners = {canon.get((dslug, raw), raw) for raw, v, p in named(cs[-1])[:cs[-1]['seats']]}
            for canonical, (first_c, won_cs) in seat_winners.items():
                kind, pslug, pid, entry = resolve_person(canonical)
                stem = f'{post_stem}-{pslug}'
                start = str(int(first_c['date'][:4]) + 1)
                notes = [tally_note(c, cfg, seat) for c in won_cs]
                end = None
                if canonical not in final_winners:
                    end = last_date[:4]
                note = ' '.join(notes)
                if len(won_cs) > 1:
                    note += f" One continuous membership from the {first_c['date'][:4]} win."
                endline = f"\nend: '{end}'" if end else ''
                (SC / f'memberships/{TIER}').mkdir(exist_ok=True)
                (SC / f'memberships/{TIER}/{stem}.yaml').write_text(f"""how_seated: elected
id: {stem}
organization_id: {oid}
person_id: {pid}
post_id: {post_id}
role: {title}{endline}
sources:
- note: {q(note)}
  retrieved: '{RETRIEVED}'
  url: https://electionhistory.scvotes.gov/contest/{first_c['id']}
start: '{start}'
""")
                drep['memberships'] += 1
        report['districts'].append(drep)

    # emit new people
    (SC / f'people/{TIER}').mkdir(exist_ok=True)
    for (pslug, pid), acc in sorted(people_touched.items()):
        path = SC / f'people/{TIER}/{pslug}.yaml'
        if path.exists():
            continue
        cand_lines = []
        for cd in sorted(acc['cands'], key=lambda e: e['election_id']):
            cand_lines.append(f"""- ballot_name: {cd['ballot_name']}
  contest_id: {cd['contest_id']}
  election_id: {cd['election_id']}
  jurisdiction_id: {cd['jurisdiction_id']}
  office_id: {cd['office_id']}
  party: {cd['party']}
  status: active""")
        src_lines = []
        for note, cid in sorted(acc['sources']):
            src_lines.append(f"""- note: {q(note)}
  retrieved: '{RETRIEVED}'
  url: https://electionhistory.scvotes.gov/contest/{cid}""")
        if acc['cluster_forms'] and len({_clean(f) for f in acc['cluster_forms']}) > 1:
            forms_txt = '; '.join(acc['cluster_forms'])
            src_lines.append(f"""- note: {q("Ballot-name forms in the Election History data for this school district treated as one person: " + forms_txt + '. Canonical name is the fullest certified form.')}
  retrieved: '{RETRIEVED}'
  url: https://electionhistory.scvotes.gov/""")
            for drep in report['districts']:
                drep['unifications'].append((acc['name'], acc['cluster_forms']))
        path.write_text(f"""candidacies:
{chr(10).join(cand_lines)}
id: {pid}
identifiers: []
name: {acc['name']}
sources:
{chr(10).join(src_lines)}
verification:
  pipeline: build_sc_schools
  status: unverified
""")
        for drep in report['districts']:
            drep['people_new'] += 1

    # apply merges into existing files (host-style textual append, as in the
    # soil & water builder)
    merged_done = set()
    for entry, cand, note, cid in merges:
        path = entry['path']
        text = path.read_text()
        if cand['contest_id'] in text:
            continue
        style = entry['data'].get('verification', {}).get('pipeline', '')
        if style == 'build_sc_municipal':
            cand_block = f"""- contest_id: {cand['contest_id']}
  election_id: {cand['election_id']}
  jurisdiction_id: {cand['jurisdiction_id']}
  office_id: {cand['office_id']}
  party: {cand['party']}
  ballot_name: {q(cand['ballot_name'])}
  status: active
"""
            text = text.replace('verification:', cand_block + 'verification:', 1)
            text = text.rstrip('\n') + f"""
- url: https://electionhistory.scvotes.gov/contest/{cid}
  note: {q(note)}
  retrieved: '{RETRIEVED}'
"""
        else:
            cand_block = f"""- ballot_name: {cand['ballot_name']}
  contest_id: {cand['contest_id']}
  election_id: {cand['election_id']}
  jurisdiction_id: {cand['jurisdiction_id']}
  office_id: {cand['office_id']}
  party: {cand['party']}
  status: active
"""
            idx = text.index('\nid: ')
            text = text[:idx] + '\n' + cand_block.rstrip('\n') + text[idx:]
            text = text.rstrip('\n') + f"""
- note: {q(note)}
  retrieved: '{RETRIEVED}'
  url: https://electionhistory.scvotes.gov/contest/{cid}
"""
        path.write_text(text)
        if str(path) not in merged_done:
            merged_done.add(str(path))
            for drep in report['districts']:
                drep['people_merged'] += 1

    # election file appends (textual, before top-level 'sources:')
    for date, blocks in election_appends.items():
        fn = SC / f"elections/sc--{date}--general.yaml"
        text = fn.read_text()
        new_blocks = [b for _, b in sorted(blocks) if b.split('\n')[0].split(': ', 1)[1] not in text]
        if new_blocks:
            marker = '\nsources:\n'
            idx = text.index(marker)
            text = text[:idx] + '\n' + ''.join(new_blocks).rstrip('\n') + text[idx:]
        src_note = (f'School board contests appended by the SC schools pass (Civic-Data issue '
                    f'#177): the school board contests of the {datename(date)} general election '
                    f'for the worked-example district, from the Election History (ElectionStats) '
                    f'school board data. Write-In rows are unnamed aggregates and seat no one.')
        if src_note not in text:
            text = text.rstrip('\n') + f"""
- url: https://electionhistory.scvotes.gov/
  note: {q(src_note)}
  retrieved: '{RETRIEVED}'
"""
        fn.write_text(text)

    print(json.dumps(report, indent=1, default=str))


if __name__ == '__main__':
    main()
