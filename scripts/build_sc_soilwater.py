#!/usr/bin/env python3
"""SC soil and water conservation district commissioners pass (Civic-Data #177).

Builds the 46 county soil and water conservation districts from the SC State
Election Commission Election History (ElectionStats) Soil-Water District
Commissioner CSV export. The Charleston district was the worked example
(2026-10-28, Walter-approved shape); this script builds the remaining 45 and
is idempotent: districts whose jurisdiction file already exists are skipped,
person merges and election appends are guarded by contest id.

Shape (approved):
- One special_district jurisdiction + organization + single post
  ('<district>/commissioner', seats: 3) per county district. The board has
  five commissioners: three elected under S.C. Code 48-9-1220 (nonpartisan,
  staggered four-year terms) and two appointed under 48-9-1210; only the
  three elected seats are modeled.
- Scope: the two most recent general cycles in the export (2022 + 2024 for
  every district). Winners = top `number_seats` named candidates by summed
  precinct-row votes; the unnamed Write-In aggregate never seats anyone.
- Cross-check per contest: named candidates + Write-In aggregate must equal
  the export's Total Votes Cast row.
- Person identity: county-pass rules (disk-owner + claim registry, token-key
  variant clustering with a strict suffix guard and a same-contest
  co-occurrence guard; exact name + county-scope matches merge into the
  existing person file in its own tier, appended in the host file's style).
"""
import csv, json, re, sys, uuid
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
SC = ROOT / 'data/us/sc'
CSV_PATH = Path.home() / 'workspace/sc177/inputs/soil_water_commissioner.csv'
NS = uuid.UUID('6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e')
RETRIEVED = '2026-10-28'
TIER = 'special-district'
PSEUDO = {'Total Votes Cast', 'Total Ballots Cast', 'Overvotes', 'Undervotes',
          'Write-In', 'Unknown Candidate', 'Overvotes/Undervotes'}
MONTHS = {'01': 'January', '02': 'February', '03': 'March', '04': 'April',
          '05': 'May', '06': 'June', '07': 'July', '08': 'August',
          '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
SCOPED_DATES = ('2022-11-08', '2024-11-05')
TITLE = 'Soil and Water Conservation District Commissioner'

HEADER = ("# Minted from the SC State Election Commission Election History\n"
          "# official general election results (soil and water pass, Civic-Data\n"
          "# issue #177).\n\n")
JUR_NOTE = ("South Carolina Code of Laws, Title 48, Chapter 9 (Soil and Water Conservation "
            "Districts Law): one district for each county. Per Section 48-9-1220, three of the "
            "district's five commissioners are elected on a nonpartisan basis at the general "
            "election; the remaining two are appointed by the state board (Section 48-9-1210) "
            "and are not modeled here. Only the elected seats are built (Civic-Data issue #177).")


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


def build_canon(forms_by_county, cooccur):
    """Return {(county, raw_form): canonical} and {(county, canonical): [all forms]}."""
    canon, clusters_of = {}, {}
    for county, forms in forms_by_county.items():
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
                clusters_of[(county, canonical)] = sorted(cl)
                for f in cl:
                    if f != canonical:
                        canon[(county, f)] = canonical
    return canon, clusters_of


# ---------------------------------------------------------------- extraction
def extract():
    rows = list(csv.DictReader(open(CSV_PATH)))
    meta, agg = {}, defaultdict(int)
    forms_by_county, cooccur = defaultdict(set), defaultdict(set)
    per_contest_names = defaultdict(set)
    for r in rows:
        cid = int(r['contest_id'])
        meta.setdefault(cid, {'date': r['election_date'][:10],
                              'district': r['district_name'],
                              'seats': int(r['number_seats'])})
        agg[(cid, r['candidate_name'])] += int(r['votes'] or 0)
        if r['candidate_name'] not in PSEUDO:
            per_contest_names[cid].add(r['candidate_name'])
    for cid, names in per_contest_names.items():
        county = meta[cid]['district']
        for n in names:
            forms_by_county[county].add(n)
            for m in names:
                if m != n:
                    cooccur[n].add(m)
    contests = {}
    for cid, m in meta.items():
        cands = [(n, v) for (c, n), v in agg.items() if c == cid]
        named = sorted([(n, v) for n, v in cands if n not in PSEUDO], key=lambda x: -x[1])
        wi = sum(v for n, v in cands if n == 'Write-In')
        tvc = sum(v for n, v in cands if n == 'Total Votes Cast')
        contests[cid] = {**m, 'contest_id': cid, 'named': named, 'writein': wi,
                         'tvc': tvc, 'check': sum(v for _, v in named) + wi == tvc}
    return contests, forms_by_county, cooccur


def tally_note(c, county):
    parts = [f"{n} {v:,}" for n, v in c['named']]
    return (f"South Carolina State Election Commission, Election History (ElectionStats) results "
            f"for the {datename(c['date'])} general election, {county} Soil-Water District "
            f"Commissioner contest (ElectionStats contest {c['contest_id']}), precinct rows "
            f"aggregated: " + '; '.join(parts) + '.')


# ---------------------------------------------------------------- people index
import yaml as _yaml


def load_people_index():
    """name -> list of dicts for every existing SC person file."""
    town_county = {}
    muni_csv = Path.home() / 'workspace/sc177/inputs/city_council.csv'
    if muni_csv.exists():
        for r in csv.DictReader(open(muni_csv)):
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


FILE_OWNER = {}   # slug -> name, within the special-district tier
CLAIMED = {}      # base slug -> (county, canonical)


def main():
    contests, forms_by_county, cooccur = extract()
    bad = [cid for cid, c in contests.items() if c['date'] in SCOPED_DATES and not c['check']]
    assert not bad, f'Total Votes Cast cross-check failed for contests {bad}'
    canon, clusters_of = build_canon(forms_by_county, cooccur)
    for f in (SC / f'people/{TIER}').glob('*.yaml'):
        FILE_OWNER[f.stem] = _yaml.safe_load(f.read_text()).get('name', '')
    people_index = load_people_index()

    # scoped contests per district
    scoped = defaultdict(dict)
    for cid, c in contests.items():
        if c['date'] in SCOPED_DATES:
            scoped[c['district']][c['date']] = c

    report = {'districts_built': 0, 'districts_skipped': 0, 'people_new': 0, 'people_merged': 0,
              'memberships': 0, 'contests_appended': 0, 'suffixed_slugs': [], 'unifications': [],
              'seated': defaultdict(int)}
    election_appends = defaultdict(list)   # date -> [(post_id, block)]
    people_touched = {}                    # key -> accumulator for NEW special-district people
    merges = []                            # (existing entry, candidacy dict, note, cid)

    def resolve_person(county, canonical):
        """Return (kind, slug, pid, entry) — kind 'new' (special-district file to
        create/accumulate) or 'existing' (file in another tier to merge into)."""
        for e in people_index.get(canonical, []):
            if e['tier'] == TIER:
                return ('new', e['slug'], e['id'], e)
            if county in e['counties']:
                return ('existing', e['slug'], e['id'], e)
        base = slugify(canonical)
        owner = FILE_OWNER.get(base)
        if owner is not None and owner != canonical:
            slug = base + '-' + str(uuid.uuid5(NS, f'person|sc|{TIER}|{county}|{base}'))[:8]
            return ('new', slug, person_uuid(base, county), None)
        claim = CLAIMED.get(base)
        if claim is None or claim == (county, canonical):
            CLAIMED[base] = (county, canonical)
            FILE_OWNER[base] = canonical
            return ('new', base, person_uuid(base), None)
        slug = base + '-' + str(uuid.uuid5(NS, f'person|sc|{TIER}|{county}|{base}'))[:8]
        report['suffixed_slugs'].append((county, canonical, slug))
        return ('new', slug, person_uuid(base, county), None)

    for county in sorted(scoped):
        cslug = slugify(county)
        dslug = f'{cslug}-soil-and-water-conservation-district'
        jur_path = SC / f'jurisdictions/{TIER}/{dslug}.yaml'
        if jur_path.exists():
            report['districts_skipped'] += 1
            continue
        pair = [scoped[county][d] for d in SCOPED_DATES]
        jur_id = f'ocd-jurisdiction/country:us/state:sc/special_district:{dslug}/government'
        div_id = f'ocd-division/country:us/state:sc/special_district:{dslug}'
        oid = org_uuid(dslug)
        post_id = f'{dslug}/commissioner'
        org_note = (f"{county} Soil and Water Conservation District, built from the SC State Election "
                    f"Commission Election History results for the November 8, 2022 and November 5, 2024 "
                    f"general elections (Soil-Water District Commissioner contests) in the ElectionStats "
                    f"Soil-Water District Commissioner export, precinct rows aggregated. The district "
                    f"board has five commissioners: three elected under S.C. Code Section 48-9-1220 "
                    f"(nonpartisan, staggered four-year terms) and two appointed under Section 48-9-1210; "
                    f"only the three elected seats are modeled.")
        first_cid = pair[0]['contest_id']
        jur_path.write_text(HEADER + f"""id: {jur_id}
name: {county} Soil and Water Conservation District
state: sc
division_id: {div_id}
classification: government
sources:
- url: https://www.scstatehouse.gov/code/t48c009.php
  note: {q(JUR_NOTE)}
  retrieved: '{RETRIEVED}'
""")
        (SC / f'organizations/{TIER}/{dslug}.yaml').write_text(HEADER + f"""id: {oid}
name: {county} Soil and Water Conservation District
jurisdiction_id: {jur_id}
identifiers: []
sources:
- url: https://electionhistory.scvotes.gov/contest/{first_cid}
  note: {q(org_note)}
  retrieved: '{RETRIEVED}'
""")
        (SC / f'posts/{TIER}/{dslug}-commissioner.yaml').write_text(HEADER + f"""id: {post_id}
organization_id: {oid}
title: {TITLE}
seats: 3
identifiers: []
sources:
- url: https://electionhistory.scvotes.gov/contest/{first_cid}
  note: {q(org_note)}
  retrieved: '{RETRIEVED}'
""")
        report['districts_built'] += 1

        for c in pair:
            contest_ref = f"sc/{c['date']}/{dslug}-commissioner"
            note = tally_note(c, county)
            winners = c['named'][:c['seats']]
            cand_ids = []
            for raw, votes in c['named']:
                canonical = canon.get((county, raw), raw)
                kind, pslug, pid, entry = resolve_person(county, canonical)
                cand_ids.append(pid)
                cand = {'ballot_name': raw, 'contest_id': contest_ref,
                        'election_id': f"sc/{c['date']}/general", 'jurisdiction_id': jur_id,
                        'office_id': post_id, 'party': 'Nonpartisan'}
                if kind == 'existing':
                    merges.append((entry, cand, note, c['contest_id']))
                else:
                    acc = people_touched.setdefault((pslug, pid), {
                        'name': canonical, 'slug': pslug, 'pid': pid, 'cands': [], 'sources': [],
                        'cluster_forms': clusters_of.get((county, canonical))})
                    if cand not in acc['cands']:
                        acc['cands'].append(cand)
                    if (note, c['contest_id']) not in acc['sources']:
                        acc['sources'].append((note, c['contest_id']))
                if (raw, votes) in winners:
                    pass
            # memberships for winners
            for raw, votes in winners:
                canonical = canon.get((county, raw), raw)
                kind, pslug, pid, entry = resolve_person(county, canonical)
                stem = f'{dslug}-commissioner-{pslug}'
                mpath = SC / f'memberships/{TIER}/{stem}.yaml'
                if not mpath.exists():
                    mpath.write_text(f"""how_seated: elected
id: {stem}
organization_id: {oid}
person_id: {pid}
post_id: {post_id}
role: {TITLE}
sources:
- note: {q(note)}
  retrieved: '{RETRIEVED}'
  url: https://electionhistory.scvotes.gov/contest/{c['contest_id']}
start: '{int(c['date'][:4]) + 1}'
""")
                    report['memberships'] += 1
                report['seated'][county] += 1
            # election contest block
            if cand_ids:
                wlines = []
                for raw, votes in winners:
                    canonical = canon.get((county, raw), raw)
                    _, _, pid, _ = resolve_person(county, canonical)
                    wlines.append(f"""  - name: {raw}
    party: Nonpartisan
    person_id: {pid}
    votes: {votes}""")
                block = f"""- id: {contest_ref}
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
                block = f"""- id: {contest_ref}
  jurisdiction_id: {jur_id}
  office_id: {post_id}
  vote_for: {c['seats']}
  candidate_ids: []
  result_status: official
  winners: []
"""
            election_appends[c['date']].append((post_id, block))

    # emit new people
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
            src_lines.append(f"""- note: {q(f"Ballot-name forms in the Election History export for {acc['name']}'s district treated as one person: " + forms_txt + '. Canonical name is the fullest certified form.')}
  retrieved: '{RETRIEVED}'
  url: https://electionhistory.scvotes.gov/""")
            report['unifications'].append((acc['name'], acc['cluster_forms']))
        path.write_text(f"""candidacies:
{chr(10).join(cand_lines)}
id: {pid}
identifiers: []
name: {acc['name']}
sources:
{chr(10).join(src_lines)}
verification:
  pipeline: build_sc_soilwater
  status: unverified
""")
        report['people_new'] += 1

    # apply merges into existing files (host-style textual append)
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
            # county-style files: candidacies list at top, sources note-first
            text = text.replace('id: ' + entry['id'], cand_block + 'id: ' + entry['id'], 1) \
                if False else text
            # insert candidacy before the 'id:' line that follows 'candidacies:'
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
            report['people_merged'] += 1

    # election file appends (textual, before top-level 'sources:')
    for date, blocks in election_appends.items():
        fn = SC / f"elections/sc--{date}--general.yaml"
        text = fn.read_text()
        new_blocks = [b for _, b in sorted(blocks) if b.split('\n')[0].split(': ', 1)[1] not in text]
        if new_blocks:
            marker = '\nsources:\n'
            idx = text.index(marker)
            text = text[:idx] + '\n' + ''.join(new_blocks).rstrip('\n') + text[idx:]
            report['contests_appended'] += len(new_blocks)
        src_marker = f"for the 45 remaining conservation districts, aggregated from the Election History Soil-Water District Commissioner CSV export"
        if src_marker not in text:
            text = text.rstrip('\n') + f"""
- url: https://electionhistory.scvotes.gov/
  note: {q(f'Soil and water conservation district contests appended by the SC soil and water pass (Civic-Data issue #177): the Soil-Water District Commissioner contests of the {datename(date)} general election ' + src_marker + ' (precinct rows only; this export carries no county-division rows). Write-In rows are unnamed aggregates and seat no one.')}
  retrieved: '{RETRIEVED}'
"""
        fn.write_text(text)

    report['seated'] = dict(report['seated'])
    print(json.dumps(report, indent=1, default=str))


if __name__ == '__main__':
    main()
