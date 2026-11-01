#!/usr/bin/env python3
"""SC school districts pass (Civic-Data #177) — fan-out builder.

Builds all remaining elected SC school districts (Walter's rulings of
2026-10-30) from the SC State Election Commission Election History
(ElectionStats) school-board contest data in ~/workspace/sc177/schools_raw.json.
Jasper County (the Phase 1 worked example, scripts/build_sc_schools.py) is
NOT in this run — its org file carries a hand-added takeover note the
example builder does not reproduce.

House conventions (county / soil & water / Jasper passes):
- Jurisdiction: jurisdictions/school/<slug>-school.yaml,
  id ocd-jurisdiction/country:us/state:sc/school_district:<slug>/school.
- Organization: the district's governing board; org file <slug>-school-board.
- Winners = top `vote_for` named candidates by contest totals; the unnamed
  Write-In aggregate never seats anyone. Cross-check per contest:
  named + Write-In == Total Votes Cast (reported, not asserted, so one bad
  contest cannot sink the pass; failures are listed in the report).
- Majority runoffs (2022-11-22, Marlboro + Sumter): the initial Nov 8
  contest is recorded with winners [] and the runoff carries the winner.
- Memberships: start = year after the win (quoted string); repeat winners
  get one continuous membership; on single-seat posts a replaced holder
  ends at the successor's election year. Multi-seat posts use cohort
  logic (no ends within scope).
- Party: blank in a nonpartisan contest -> 'Nonpartisan'; Horry and Lee
  are partisan in the data and carry the export party as-is.
- Person identity: disk-owner + claim registry; school-tier reuse only
  within the same district; cross-tier merges require a county match;
  variant clustering as in the Jasper builder.
- Election files edited textually (contest blocks before the top-level
  'sources:' line, one fan-out sources entry appended per date).
"""
import json, re, sys, uuid
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
SC = ROOT / 'data/us/sc'
RAW = Path.home() / 'workspace/sc177/schools_raw.json'
NS = uuid.UUID('6f3f1c2a-6b2b-5a2b-9b8a-1e6a7f9c2d4e')
RETRIEVED = '2026-10-30'
TIER = 'school'
PSEUDO = {'Total Votes Cast', 'Total Ballots Cast', 'Overvotes', 'Undervotes',
          'Write-In', 'Unknown Candidate', 'Overvotes/Undervotes'}
SCHOOL_OFFICES = {'School Board Member', 'School Trustee', 'School Board Chairman',
                  'Member of the Board of Education', 'Board of Education Chair',
                  'Consolidated School Board', 'Constituent School Board'}
MONTHS = {'01': 'January', '02': 'February', '03': 'March', '04': 'April',
          '05': 'May', '06': 'June', '07': 'July', '08': 'August',
          '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
HEADER = ("# Minted from the SC State Election Commission Election History\n"
          "# official general election results (schools pass, Civic-Data\n"
          "# issue #177).\n\n")
STD = ['2022-11-08', '2024-11-05']
SPART = ['2021-11-02', '2023-11-07']
STD_R = ['2022-11-08', '2022-11-22', '2024-11-05']


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
    if tvc(c) == 0:
        return None
    return sum(v for _, v, _ in named(c)) + writein(c) == tvc(c)


def contest_label(c):
    lab = c['division'] or ''
    if c['modifier']:
        lab += ' ' + c['modifier']
    return lab


def tally_note(c, cfg):
    parts = [f"{n} ({p}) {v:,}" if p else f"{n} {v:,}" for n, v, p in named(c)]
    return (f"South Carolina State Election Commission, Election History (ElectionStats) results "
            f"for the {datename(c['date'])} general election, {contest_label(c)} contest "
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
            districts = set()
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
                m = re.search(r'school_district:([a-z0-9-]+)/', jid)
                if m:
                    districts.add(m.group(1))
                for s in d.get('sources') or []:
                    mm = re.search(r'\(([A-Z][a-z]+(?: [A-Z][a-z]+)?) County\)', s.get('note', ''))
                    if mm:
                        counties.add(mm.group(1))
            index[d['name']].append({'tier': tierdir.name, 'slug': f.stem, 'id': d['id'],
                                     'path': f, 'counties': counties, 'districts': districts,
                                     'data': d})
    return index


FILE_OWNER = {}
CLAIMED = {}


# ---------------------------------------------------------------- config helpers
def P(key, title, seats, note=None):
    return {'key': key, 'title': title, 'seats': seats, 'note': note}


def smd_posts(n, start=1):
    return [P(f'district-{i}', f'School Board District {i}', 1) for i in range(start, start + n)]


def R(post, division=None, dre=None, modifier=None, min_=None, office=None, dates=None):
    return {'post': post, 'division': division, 'dre': dre, 'modifier': modifier,
            'in': min_, 'office': office, 'dates': dates}


def smd_rules(prefix, n, start=1):
    return [R(f'district-{i}', division=f'{prefix} {i}') for i in range(start, start + n)]


def seatmod_rules(division, nums, atlarge_seats=None):
    rules = [R(f'district-{i}', division=division, modifier=f'Seat {i}') for i in nums]
    if atlarge_seats:
        rules.append(R('trustee-at-large', division=division, modifier='At Large'))
    return rules


def post_id_of(dslug, key):
    if key.startswith('trustee-'):
        return f'{dslug}/{key}'
    if key == 'chairman':
        return f'{dslug}/school-board-chairman'
    return f'{dslug}/school-board-{key}'


# ---------------------------------------------------------------- districts
# Structures and act cites: Phase 1 classification table
# (~/workspace/sc177/schools_classification.md, section 4), verified against
# the ElectionStats contest organization 2026-10-30.
DISTRICTS = [
    dict(slug='abbeville-county', name='Abbeville County School District',
         board_name='Abbeville County School District Board of Trustees',
         counties=['Abbeville'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general election "
                         "from nine single-member districts (Act 293 of 2012, as amended by "
                         "Act 247 of 2022)."),
         jur_sources=[('https://testweb.scstatehouse.gov/sess124_2021-2022/bills/1263.htm',
                       "Act 247 of 2022 (S.1263), amending Act 293 of 2012: the Abbeville County "
                       "school board elected from nine single-member districts.")],
         posts=smd_posts(9), rules=smd_rules('Abbeville County School District', 9),
         division_bases=['Abbeville County School District']),
    dict(slug='aiken-county', name='Aiken County Public School District',
         board_name='Aiken County Public School District Board of Trustees',
         counties=['Aiken', 'Saluda'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general election "
                         "from nine single-member districts to staggered four-year terms "
                         "(Act 588 of 1986, as amended; the districts were reapportioned by "
                         "Act 230 of 2024)."),
         jur_sources=[('https://www.scstatehouse.gov/sess125_2023-2024/bills/1025.htm',
                       "Act 230 of 2024 (S.1025): reapportionment of the nine single-member "
                       "districts of the Aiken County Public School District.")],
         posts=smd_posts(9), rules=smd_rules('Aiken County School District', 9),
         division_bases=['Aiken County School District']),
    dict(slug='allendale-county', name='Allendale County Schools',
         board_name='Allendale County Schools Board of Trustees',
         counties=['Allendale'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Five members elected in nonpartisan elections at the general election "
                         "from five single-member districts (the county council districts) to "
                         "staggered four-year terms (Act 174 of 1999). The board's selection has "
                         "remained elective throughout; state takeovers in 1999-2007 and 2017 "
                         "suspended its management authority, which the State Board of Education "
                         "recorded as restored in December 2022."),
         jur_sources=[('http://www.scstatehouse.gov/sess113_1999-2000/bills/3404.htm',
                       "Act 174 of 1999 (H.3404): five members of the board of trustees of "
                       "Allendale County Schools elected from single-member districts.")],
         posts=smd_posts(5), rules=smd_rules('Allendale County School District', 5),
         division_bases=['Allendale County School District']),
    dict(slug='anderson-1', name='Anderson School District One',
         board_name='Anderson School District One Board of Trustees',
         counties=['Anderson'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general election "
                         "to staggered four-year terms (Act 509 of 1982, Section 13A(A), as "
                         "amended by Act 231 of 2024). Members must reside in one of seven "
                         "residency areas but are elected by the voters of the whole district; "
                         "the posts are the residency areas."),
         jur_sources=[],
         posts=[P(f'area-{i}', f'School Board Area {i}', 1) for i in range(1, 8)],
         rules=[R(f'area-{i}', division=f'Anderson County School District 1 Area {i}')
                for i in range(1, 8)],
         division_bases=['Anderson County School District 1']),
    dict(slug='anderson-2', name='Anderson School District Two',
         board_name='Anderson School District Two Board of Trustees',
         counties=['Anderson', 'Greenville'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general election "
                         "to staggered four-year terms from residency areas, elected by the "
                         "voters of the whole district. Act 268 of 2026 converts the district to "
                         "six single-member districts plus one at-large seat beginning with the "
                         "2026 and 2028 elections; the contests built in this pass predate that "
                         "transition. In the ElectionStats data the in-scope contests are "
                         "organized as Area 1 (two seats), Area 2 (two seats), Areas 4, 5, and 6 "
                         "(one seat each), and one at-large contest; no Area 3 contest appears "
                         "in the two most recent cycles, and no Area 3 post is built."),
         jur_sources=[],
         posts=[P('area-1', 'School Board Area 1', 2), P('area-2', 'School Board Area 2', 2),
                P('area-4', 'School Board Area 4', 1), P('area-5', 'School Board Area 5', 1),
                P('area-6', 'School Board Area 6', 1),
                P('trustee-at-large', 'School Board Trustee At-Large', 1)],
         rules=[R('area-1', division='Anderson County School District 2 Area 1'),
                R('area-2', division='Anderson County School District 2 Area 2'),
                R('area-4', division='Anderson County School District 2 Area 4'),
                R('area-5', division='Anderson County School District 2 Area 5'),
                R('area-6', division='Anderson County School District 2 Area 6'),
                R('trustee-at-large', division='Anderson County School District 2',
                  modifier='At-Large'),
                R('trustee-at-large', division='Anderson County School District 2',
                  modifier='At Large')],
         division_bases=['Anderson County School District 2']),
    dict(slug='anderson-3', name='Anderson School District Three',
         board_name='Anderson School District Three Board of Trustees',
         counties=['Anderson'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Five members elected in nonpartisan elections at the general election "
                         "to staggered four-year terms: four from single-member districts and "
                         "one at large (Act 509 of 1982, Section 13A(C), as amended by Act 96 of "
                         "2015). The single-member districts are labeled Areas in the "
                         "ElectionStats data and are modeled as district posts."),
         jur_sources=[],
         posts=smd_posts(4) + [P('trustee-at-large', 'School Board Trustee At-Large', 1)],
         rules=[R(f'district-{i}', division=f'Anderson County School District 3 Area {i}')
                for i in range(1, 5)] +
               [R('trustee-at-large', division='Anderson County School District 3',
                  modifier='At Large'),
                R('trustee-at-large', division='Anderson County School District 3',
                  modifier='At-Large')],
         division_bases=['Anderson County School District 3']),
    dict(slug='anderson-4', name='Anderson School District Four',
         board_name='Anderson School District Four Board of Trustees',
         counties=['Anderson'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Five members elected in nonpartisan elections at the general election "
                         "from five single-member districts to staggered four-year terms "
                         "(Act 509 of 1982, Section 13A(D), added by Act 300 of 2014). The "
                         "districts are labeled Areas in the ElectionStats data."),
         jur_sources=[],
         posts=smd_posts(5),
         rules=[R(f'district-{i}', division=f'Anderson County School District 4 Area {i}')
                for i in range(1, 6)],
         division_bases=['Anderson County School District 4']),
    dict(slug='anderson-5', name='Anderson School District Five',
         board_name='Anderson School District Five Board of Trustees',
         counties=['Anderson'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general election "
                         "to staggered four-year terms: seven from single-member districts and "
                         "two at large (Act 509 of 1982, Section 13A(E), added by Act 300 of "
                         "2014). The single-member districts are labeled Areas in the "
                         "ElectionStats data and are modeled as district posts; the two "
                         "at-large seats are contested one per cycle."),
         jur_sources=[],
         posts=smd_posts(7) + [P('trustee-at-large', 'School Board Trustee At-Large', 2)],
         rules=[R(f'district-{i}', division=f'Anderson County School District 5 Area {i}')
                for i in range(1, 8)] +
               [R('trustee-at-large', division='Anderson County School District 5',
                  modifier='At Large'),
                R('trustee-at-large', division='Anderson County School District 5',
                  modifier='At-Large')],
         division_bases=['Anderson County School District 5']),
    dict(slug='barnwell-county', name='Barnwell County School District',
         board_name='Barnwell County School District Board of Trustees',
         counties=['Barnwell'], cycles=['2024-11-05'], party_mode='nonpartisan',
         structure_note=("Five members elected in nonpartisan elections at the general election "
                         "from five single-member districts (Act 92 of 2023). The consolidated "
                         "Barnwell County School District opened July 1, 2024, succeeding "
                         "Barnwell County Districts 45, 19, and 29; only the consolidated "
                         "district's 2024 contests are built in this pass — the 2022 contests "
                         "in the ElectionStats data at like-named divisions belong to the "
                         "predecessor Barnwell County Consolidated School District and are not "
                         "built."),
         jur_sources=[('https://www.scstatehouse.gov/sess125_2023-2024/bills/654.htm',
                       "Act 92 of 2023 (S.654): consolidation of the Barnwell County school "
                       "districts into the Barnwell County School District, governed by five "
                       "members elected from single-member districts.")],
         posts=smd_posts(5), rules=smd_rules('Barnwell County School District', 5),
         division_bases=['Barnwell County School District']),
    dict(slug='beaufort-county', name='Beaufort County School District',
         board_name='Beaufort County School District Board of Trustees',
         counties=['Beaufort'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Eleven members elected in nonpartisan elections at the general "
                         "election from eleven single-member districts to staggered four-year "
                         "terms (Act 589 of 1986)."),
         jur_sources=[('http://www.scstatehouse.gov/sess106_1985-1986/bills/3310.htm',
                       "Act 589 of 1986 (H.3310): the board of trustees of the Beaufort County "
                       "School District elected from single-member districts.")],
         posts=smd_posts(11), rules=smd_rules('Beaufort County School District', 11),
         division_bases=['Beaufort County School District']),
    dict(slug='berkeley-county', name='Berkeley County School District',
         board_name='Berkeley County School District Board of Trustees',
         counties=['Berkeley'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general election "
                         "to staggered four-year terms: eight from single-member districts (the "
                         "county council districts) and one at large (Act 518 of 1982, as "
                         "amended by Act 251 of 2022). Before 2022 the board had nine "
                         "single-member districts; the former District 9 was eliminated in the "
                         "2022 restructuring, and only contests of the current structure are "
                         "built."),
         jur_sources=[('https://www.scstatehouse.gov/sess124_2021-2022/prever/910_20220426.htm',
                       "Act 251 of 2022 (S.910): reapportionment of the Berkeley County School "
                       "District into eight single-member districts and one at-large seat.")],
         posts=smd_posts(8) + [P('trustee-at-large', 'School Board Trustee At-Large', 1)],
         rules=smd_rules('Berkeley County School District', 8) +
               [R('trustee-at-large', division='Berkeley County School District',
                  modifier='At Large')],
         division_bases=['Berkeley County School District']),
    dict(slug='calhoun-county', name='Calhoun County Public Schools',
         board_name='Calhoun County Public Schools Board of Trustees',
         counties=['Calhoun'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Five members elected in nonpartisan elections at the general election "
                         "from five single-member districts (the county council districts), to "
                         "terms co-terminous with the council districts (Act 585 of 1994)."),
         jur_sources=[('https://www.scstatehouse.gov/sess110_1993-1994/bills/4889.htm',
                       "Act 585 of 1994 (H.4889): five members of the Calhoun County school "
                       "board elected from single-member districts.")],
         posts=smd_posts(5), rules=smd_rules('Calhoun County School District', 5),
         division_bases=['Calhoun County School District']),
    dict(slug='charleston-county', name='Charleston County School District',
         board_name='Charleston County School District Board of Trustees',
         counties=['Charleston'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general election "
                         "from nine single-member districts (numbered to correspond to the "
                         "county council districts) to staggered four-year terms (Act 340 of "
                         "1967, as amended by Act 182 of 2020, which established the "
                         "single-member districts from 2022). The district's eight constituent "
                         "school boards were abolished July 1, 2025 by Act 77 of 2025 and are "
                         "not built."),
         jur_sources=[('https://www.scstatehouse.gov/sess123_2019-2020/bills/5034.htm',
                       "Act 182 of 2020 (H.5034): the Charleston County School District board "
                       "of trustees elected from nine single-member districts.")],
         posts=smd_posts(9), rules=smd_rules('Charleston County School District', 9),
         division_bases=['Charleston County School District']),
    dict(slug='cherokee-county', name='Cherokee County School District',
         board_name='Cherokee County School District Board of Trustees',
         counties=['Cherokee'], cycles=[], party_mode='nonpartisan', scaffold=True,
         structure_note=("Nine members elected in nonpartisan elections from nine "
                         "single-member districts to staggered four-year terms (Act 587 of "
                         "1992, as reapportioned by Act 252 of 2022); Cherokee County school "
                         "elections are held on the second Tuesday in August of even years "
                         "(Act 132 of 2007). Cherokee County school elections are not published "
                         "in the SEC Election History (ElectionStats) system, so no contests or "
                         "memberships are built in this pass; certified results for the "
                         "district's two most recent elections have been requested from the "
                         "Cherokee County elections office."),
         jur_sources=[('https://scsba.org/about-us/school-board-facts/',
                       "SC School Boards Association, School Board Facts: Cherokee County "
                       "School District — nine trustees elected from single-member districts.")],
         posts=smd_posts(9), rules=[], division_bases=['Cherokee County School District']),
    dict(slug='chester-county', name='Chester County School District',
         board_name='Chester County School District Board of Trustees',
         counties=['Chester'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election to staggered four-year terms: six from single-member "
                         "districts and one at large (Act 525 of 1982, as amended)."),
         jur_sources=[('https://www.scstatehouse.gov/sess124_2021-2022/bills/1180.htm',
                       "Chester County School District board legislation (S.1180 of 2021-2022), "
                       "under Act 525 of 1982, as amended: six single-member districts and one "
                       "at-large seat.")],
         posts=smd_posts(6) + [P('trustee-at-large', 'School Board Trustee At-Large', 1)],
         rules=smd_rules('Chester County School District', 6) +
               [R('trustee-at-large', division='Chester County School District',
                  modifier='At Large')],
         division_bases=['Chester County School District']),
    dict(slug='chesterfield-county', name='Chesterfield County School District',
         board_name='Chesterfield County School District Board of Trustees',
         counties=['Chesterfield'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general "
                         "election from nine single-member districts to staggered four-year "
                         "terms (Act 205 of 1993, as amended)."),
         jur_sources=[('https://www.scstatehouse.gov/sess117_2007-2008/bills/4233.htm',
                       "Act 205 of 1993, as amended (H.4233 of 2007-2008): nine members of the "
                       "Chesterfield County school board elected from single-member districts.")],
         posts=smd_posts(9), rules=smd_rules('Chesterfield County School District', 9),
         division_bases=['Chesterfield County School District']),
    dict(slug='clarendon-county', name='Clarendon County School District',
         board_name='Clarendon County School District Board of Trustees',
         counties=['Clarendon'], cycles=['2024-11-05'], party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general "
                         "election from nine single-member districts to staggered four-year "
                         "terms (Act 106 of 2021; districts as delineated by Act 234 of 2024). "
                         "The consolidated Clarendon County School District's board became "
                         "fully elected beginning with the 2024 general election; only the "
                         "2024 contests are built in this pass."),
         jur_sources=[('https://www.scstatehouse.gov/sess124_2021-2022/bills/648.htm',
                       "Act 106 of 2021 (S.648): consolidation of the Clarendon County school "
                       "districts under a nine-member board elected from single-member "
                       "districts.")],
         posts=smd_posts(9), rules=smd_rules('Clarendon County School District', 9),
         division_bases=['Clarendon County School District']),
    dict(slug='clover', name='Clover School District',
         board_name='Clover School District Board of Trustees',
         counties=['York'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election to staggered four-year terms: five from single-member "
                         "districts and two at large (Act 473 of 2002, as amended; the "
                         "single-member districts became true single-member electorates in "
                         "2022)."),
         jur_sources=[],
         posts=smd_posts(5) + [P('trustee-at-large', 'School Board Trustee At-Large', 2)],
         rules=seatmod_rules('Clover School District', range(1, 6), atlarge_seats=2),
         division_bases=['Clover School District']),
    dict(slug='colleton-county', name='Colleton County School District',
         board_name='Colleton County School District Board of Trustees',
         counties=['Colleton'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election from seven single-member districts to staggered four-year "
                         "terms (1991-92 Act, H.667; a former at-large seat was abolished)."),
         jur_sources=[('https://www.colleton.k12.sc.us/page/school-board/',
                       "Colleton County School District school board page: seven members "
                       "elected from single-member districts.")],
         posts=smd_posts(7), rules=smd_rules('Colleton County School District', 7),
         division_bases=['Colleton County School District']),
    dict(slug='darlington-county', name='Darlington County School District',
         board_name='Darlington County School District Board of Trustees',
         counties=['Darlington'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Eight members elected in nonpartisan elections at the general "
                         "election from eight election districts, by the electors of each "
                         "district, to staggered four-year terms (Act 748 of 1978, as amended)."),
         jur_sources=[('https://www.scstatehouse.gov/sess116_2005-2006/bills/4912.htm',
                       "Act 748 of 1978, as amended (H.4912 of 2005-2006): the board of "
                       "trustees of the Darlington County School District elected from eight "
                       "election districts.")],
         posts=smd_posts(8), rules=smd_rules('Darlington County School District', 8),
         division_bases=['Darlington County School District']),
    dict(slug='dorchester-2', name='Dorchester School District Two',
         board_name='Dorchester School District Two Board of Trustees',
         counties=['Dorchester'], cycles=['2024-11-05'], party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election from seven single-member districts to staggered four-year "
                         "terms (Act 535 of 1982, as amended by Act 96 of 2023). Before 2024 "
                         "the board was elected at large; only the 2024 contests, the first "
                         "under the single-member-district structure, are built in this pass — "
                         "the at-large contests of 2020 and 2022 belong to the prior structure "
                         "and do not map to the current seats."),
         jur_sources=[('https://www.scstatehouse.gov/sess125_2023-2024/bills/3961.htm',
                       "Act 96 of 2023 (H.3961): seven single-member districts for the "
                       "Dorchester School District Two board of trustees beginning with the "
                       "2024 general election.")],
         posts=smd_posts(7),
         rules=seatmod_rules('Dorchester County School District 2', range(1, 8)),
         division_bases=['Dorchester County School District 2']),
    dict(slug='dorchester-4', name='Dorchester School District Four',
         board_name='Dorchester School District Four Board of Trustees',
         counties=['Dorchester'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Five members elected in nonpartisan elections at the general "
                         "election from five single-member districts to staggered four-year "
                         "terms (1987 Act, H.3196)."),
         jur_sources=[('https://www.dorchester4.k12.sc.us/page/board-of-trustees',
                       "Dorchester School District Four board of trustees page: five members "
                       "elected from single-member districts.")],
         posts=smd_posts(5),
         rules=seatmod_rules('Dorchester County School District 4', range(1, 6)),
         division_bases=['Dorchester County School District 4']),
    dict(slug='edgefield-county', name='Edgefield County School District',
         board_name='Edgefield County School District Board of Trustees',
         counties=['Edgefield'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election from seven single-member districts to staggered four-year "
                         "terms (Act 595 of 1992, as amended; districts reapportioned by "
                         "Act 237 of 2024)."),
         jur_sources=[],
         posts=smd_posts(7), rules=smd_rules('Edgefield County School District', 7),
         division_bases=['Edgefield County School District']),
    dict(slug='fairfield-county', name='Fairfield County School District',
         board_name='Fairfield County School District Board of Trustees',
         counties=['Fairfield'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election from seven single-member districts (the county council "
                         "districts) to staggered four-year terms (Act 191 of 1991, as amended; "
                         "Act 255 of 2022). A circa-2010 expansion adding "
                         "delegation-appointed seats was blocked by a federal Voting Rights "
                         "Act objection and never took effect; the board is seven elected "
                         "members."),
         jur_sources=[('https://www.scstatehouse.gov/sess111_1995-1996/bills/4853.htm',
                       "Act 191 of 1991, as amended (H.4853 of 1995-1996): seven members of the "
                       "Fairfield County school board elected from single-member districts.")],
         posts=smd_posts(7), rules=smd_rules('Fairfield County School District', 7),
         division_bases=['Fairfield County School District']),
    dict(slug='florence-1', name='Florence 1 Schools',
         board_name='Florence 1 Schools Board of Trustees',
         counties=['Florence'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general "
                         "election from nine single-member districts to staggered four-year "
                         "terms (Act 256 of 2022, which consolidated Florence District Four "
                         "into Florence 1 Schools in 2022)."),
         jur_sources=[('https://www.scstatehouse.gov/sess124_2021-2022/bills/5339.htm',
                       "Act 256 of 2022 (H.5339): Florence 1 Schools governed by nine members "
                       "elected from single-member districts.")],
         posts=smd_posts(9),
         rules=seatmod_rules('Florence County School District 1', range(1, 10)),
         division_bases=['Florence County School District 1']),
    dict(slug='florence-2', name='Florence County School District Two',
         board_name='Florence County School District Two Board of Trustees',
         counties=['Florence'], cycles=[], party_mode='nonpartisan', scaffold=True,
         structure_note=("Seven members elected to staggered three-year terms from seven "
                         "numbered seats, elected by the voters of the whole district at an "
                         "annual election conducted by the district itself. Florence County "
                         "School District Two's elections are not published in the SEC "
                         "Election History (ElectionStats) system, so no contests or "
                         "memberships are built in this pass; certified results for the "
                         "district's two most recent elections have been requested from the "
                         "district office."),
         jur_sources=[('https://www.fsd2.org/school-board/board-members',
                       "Florence County School District Two board members page: seven "
                       "trustees holding numbered seats.")],
         posts=[P(f'seat-{i}', f'School Board Seat {i}', 1) for i in range(1, 8)],
         rules=[], division_bases=['Florence County School District 2']),
    dict(slug='florence-3', name='Florence County School District Three',
         board_name='Florence County School District Three Board of Trustees',
         counties=['Florence'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general "
                         "election to staggered four-year terms: five from single-member "
                         "districts and four from two multimember districts of two seats each "
                         "(Act 103 of 2017). The multimember districts are Districts 4 and 7; "
                         "in the ElectionStats data each holds a single-seat contest in every "
                         "cycle, its two seats staggered across cycles, and the contests are "
                         "labeled by seat number (Seat 1 through Seat 7)."),
         jur_sources=[('https://www.scstatehouse.gov/sess122_2017-2018/bills/4067.htm',
                       "Act 103 of 2017 (H.4067): Florence County School District Three "
                       "governed by nine members — five single-member districts and two "
                       "multimember districts of two seats each.")],
         posts=[P('district-1', 'School Board District 1', 1),
                P('district-2', 'School Board District 2', 1),
                P('district-3', 'School Board District 3', 1),
                P('district-4', 'School Board District 4', 2),
                P('district-5', 'School Board District 5', 1),
                P('district-6', 'School Board District 6', 1),
                P('district-7', 'School Board District 7', 2)],
         rules=seatmod_rules('Florence County School District 3', range(1, 8)),
         division_bases=['Florence County School District 3']),
    dict(slug='florence-5', name='Florence District Five',
         board_name='Florence District Five Board of Trustees',
         counties=['Florence'], cycles=['2022-11-08', '2023-11-07', '2024-11-05'],
         party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections to staggered "
                         "three-year terms at annual November elections: four from "
                         "single-member districts (Seats 1-4) and three at large (Act 250 of "
                         "1991, as amended). Three cycles (2022, 2023, and 2024) are built "
                         "because the district elects annually. One 2022 at-large contest "
                         "appears in the ElectionStats data at the division 'Florence School "
                         "District' (contest 2693); it is assigned to this district — the only "
                         "Florence district with at-large seats — and its vote totals are on "
                         "this district's scale."),
         jur_sources=[('http://www.scstatehouse.gov/sess109_1991-1992/bills/1010.htm',
                       "Act 250 of 1991 (H.1010): Florence District Five governed by members "
                       "elected from single-member districts and at large to three-year terms.")],
         posts=smd_posts(4) + [P('trustee-at-large', 'School Board Trustee At-Large', 3)],
         rules=seatmod_rules('Florence County School District 5', range(1, 5),
                             atlarge_seats=3) +
               [R('trustee-at-large', division='Florence School District',
                  modifier='At Large')],
         division_bases=['Florence County School District 5', 'Florence School District']),
]

DISTRICTS += [
    dict(slug='fort-mill', name='Fort Mill Schools',
         board_name='Fort Mill Schools Board of Trustees',
         counties=['York'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election at large to staggered four-year terms (Act 270 of 1981, as "
                         "amended)."),
         jur_sources=[('https://www.fortmillschools.org/leadership',
                       "Fort Mill Schools leadership page: seven-member board of trustees "
                       "elected at large.")],
         posts=[P('trustee-at-large', 'School Board Trustee At-Large', 7)],
         rules=[R('trustee-at-large', division='Fort Mill School District')],
         division_bases=['Fort Mill School District']),
    dict(slug='georgetown-county', name='Georgetown County School District',
         board_name='Georgetown County School District Board of Trustees',
         counties=['Georgetown'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general "
                         "election to staggered four-year terms: seven from single-member "
                         "districts and two at large (Act 107 of 2021; the structure follows a "
                         "2008 federal consent decree)."),
         jur_sources=[('https://www.scstatehouse.gov/billsearch.php?billnumbers=4241&session=124&summary=B&PRINT=1',
                       "Act 107 of 2021 (H.4241): Georgetown County School District board of "
                       "nine members — seven single-member districts and two at-large seats.")],
         posts=smd_posts(7) + [P('trustee-at-large', 'School Board Trustee At-Large', 2)],
         rules=smd_rules('Georgetown County School District', 7) +
               [R('trustee-at-large', division='Georgetown County School District',
                  modifier='At Large')],
         division_bases=['Georgetown County School District']),
    dict(slug='greenville-county', name='Greenville County Schools',
         board_name='Greenville County Schools Board of Trustees',
         counties=['Greenville', 'Laurens'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Twelve members elected in nonpartisan elections at the general "
                         "election from twelve single-member districts (numbered 17 through "
                         "28, continuing the county's district numbering) to staggered "
                         "four-year terms (Act 521 of 1992; districts reapportioned by Act 257 "
                         "of 2022)."),
         jur_sources=[],
         posts=[P(f'district-{i}', f'School Board District {i}', 1) for i in range(17, 29)],
         rules=[R(f'district-{i}', division=f'Greenville County School District {i}')
                for i in range(17, 29)] +
               [R('district-18', division='Greenville County School District Area 18')],
         division_bases=['Greenville County School District']),
    dict(slug='greenwood-50', name='Greenwood School District 50',
         board_name='Greenwood School District 50 Board of Trustees',
         counties=['Greenwood'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general "
                         "election from nine single-member districts to staggered four-year "
                         "terms (Act 595 of 1994, as amended; districts reapportioned by "
                         "Act 239 of 2024). No ElectionStats contest appears for Seat 5 in any "
                         "cycle in the system, and Seats 4 and 9 have no contest in the two "
                         "most recent cycles; those posts are built without memberships."),
         jur_sources=[],
         posts=smd_posts(9),
         rules=seatmod_rules('Greenwood County School District 50', range(1, 10)),
         division_bases=['Greenwood County School District 50']),
    dict(slug='greenwood-51', name='Greenwood School District 51',
         board_name='Greenwood School District 51 Board of Trustees',
         counties=['Greenwood'], cycles=[], party_mode='nonpartisan', scaffold=True,
         structure_note=("Five members elected at large to staggered three-year terms at "
                         "annual elections held on the second Tuesday in May (Act 546 of 1982, "
                         "as amended by Act 145 of 2001; Act 425 of 2006). The district's May "
                         "elections are not published in the SEC Election History "
                         "(ElectionStats) system, so no contests or memberships are built in "
                         "this pass; certified results for the district's two most recent "
                         "elections have been requested from the Greenwood County elections "
                         "office."),
         jur_sources=[('https://scsba.org/about-us/school-board-facts/',
                       "SC School Boards Association, School Board Facts: Greenwood School "
                       "District 51 (Ware Shoals) — five trustees elected at large.")],
         posts=[P('trustee-at-large', 'School Board Trustee At-Large', 5)],
         rules=[], division_bases=['Greenwood County School District 51']),
    dict(slug='greenwood-52', name='Greenwood School District 52',
         board_name='Greenwood School District 52 Board of Trustees',
         counties=['Greenwood'], cycles=[], party_mode='nonpartisan', scaffold=True,
         structure_note=("Five members elected at large to staggered three-year terms at "
                         "annual elections held on the second Tuesday in May (Act 546 of 1982, "
                         "as amended by Act 145 of 2001). The district's May elections are not "
                         "published in the SEC Election History (ElectionStats) system, so no "
                         "contests or memberships are built in this pass; certified results "
                         "for the district's two most recent elections have been requested "
                         "from the Greenwood County elections office."),
         jur_sources=[('https://scsba.org/about-us/school-board-facts/',
                       "SC School Boards Association, School Board Facts: Greenwood School "
                       "District 52 (Ninety Six) — five trustees elected at large.")],
         posts=[P('trustee-at-large', 'School Board Trustee At-Large', 5)],
         rules=[], division_bases=['Greenwood County School District 52']),
    dict(slug='hampton-county', name='Hampton County School District',
         board_name='Hampton County School District Board of Trustees',
         counties=['Hampton'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election from seven single-member districts to staggered four-year "
                         "terms (Act 184 of 2020, as amended by Act 259 of 2022). The "
                         "consolidated Hampton County School District's first elected board "
                         "was chosen in 2022. Act 184 of 2020 originally described the members "
                         "as elected at large; Act 259 of 2022 delineated the seven "
                         "single-member districts, and the county's ballots run separate "
                         "district contests, as built here."),
         jur_sources=[('https://www.scstatehouse.gov/sess124_2021-2022/bills/1264.htm',
                       "Act 259 of 2022 (H.1264): seven single-member districts for the "
                       "Hampton County School District board.")],
         posts=smd_posts(7), rules=smd_rules('Hampton County School District', 7),
         division_bases=['Hampton County School District']),
    dict(slug='horry-county', name='Horry County Schools',
         board_name='Horry County Board of Education',
         counties=['Horry'], cycles=STD, party_mode='asis',
         structure_note=("Twelve members elected in PARTISAN elections (with June primaries) "
                         "at the general election to staggered four-year terms: eleven from "
                         "single-member districts and a chairman elected countywide as a "
                         "separate office (Act 287 of 1989, as amended by Act 178 of 1997). "
                         "Horry is South Carolina's partisan school-board exception; party "
                         "labels are carried from the certified results."),
         jur_sources=[('http://www.horrycountyschools.net/boardofeducation',
                       "Horry County Schools board of education page: eleven district members "
                       "and a countywide chairman.")],
         posts=smd_posts(11) + [P('chairman', 'Board of Education Chairman', 1)],
         rules=[R(f'district-{i}', division=f'Horry County Board of Education District {i}',
                  office='Member of the Board of Education') for i in range(1, 12)] +
               [R('chairman', division='Horry County Board of Education District',
                  office='Board of Education Chair')],
         division_bases=['Horry County Board of Education']),
    dict(slug='kershaw-county', name='Kershaw County School District',
         board_name='Kershaw County School District Board of Trustees',
         counties=['Kershaw'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general "
                         "election from nine single-member districts to staggered four-year "
                         "terms (Act 930 of 1970, as amended)."),
         jur_sources=[],
         posts=smd_posts(9), rules=smd_rules('Kershaw County School District', 9),
         division_bases=['Kershaw County School District']),
    dict(slug='lancaster-county', name='Lancaster County School District',
         board_name='Lancaster County School District Board of Trustees',
         counties=['Lancaster'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election from seven single-member districts (the county council "
                         "districts) to staggered four-year terms (Act 607 of 1992)."),
         jur_sources=[('https://files-backend.assets.thrillshare.com/documents/asset/uploaded_file/4155/Lancaster_Csd/54803fc5-955f-4580-83f3-8bcf5c4a33c6/BAA-Board-MembershipElections1.pdf?disposition=inline',
                       "Lancaster County School District Policy BAA (Board "
                       "Membership/Elections): seven members elected from the county council "
                       "districts.")],
         posts=smd_posts(7), rules=smd_rules('Lancaster County School District', 7),
         division_bases=['Lancaster County School District']),
    dict(slug='laurens-55', name='Laurens County School District 55',
         board_name='Laurens County School District 55 Board of Trustees',
         counties=['Laurens'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election from seven single-member districts to staggered four-year "
                         "terms (Act 779 of 1988, as amended; districts reapportioned by "
                         "Act 87 of 2025)."),
         jur_sources=[],
         posts=smd_posts(7),
         rules=seatmod_rules('Laurens County School District 55', range(1, 8)),
         division_bases=['Laurens County School District 55']),
    dict(slug='laurens-56', name='Laurens County School District 56',
         board_name='Laurens County School District 56 Board of Trustees',
         counties=['Laurens'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election from seven single-member districts to staggered four-year "
                         "terms (Act 779 of 1988, as amended; districts reapportioned by "
                         "Act 88 of 2025)."),
         jur_sources=[],
         posts=smd_posts(7),
         rules=seatmod_rules('Laurens County School District 56', range(1, 8)),
         division_bases=['Laurens County School District 56']),
    dict(slug='lee-county', name='Lee County School District',
         board_name='Lee County School District Board of Trustees',
         counties=['Lee'], cycles=STD, party_mode='asis',
         structure_note=("Seven members elected at the general election from seven "
                         "single-member districts (the county council districts) to staggered "
                         "four-year terms (Act 843 of 1952, as amended; restated by Act 272 of "
                         "2026). In the ElectionStats data the district's general-election "
                         "candidates carry party labels and the district holds June primaries, "
                         "unlike most South Carolina school boards; party labels are carried "
                         "from the certified results. Act 272 of 2026 restates the cycle: "
                         "there is no Lee County school election in 2026; Districts 1, 2, 3, "
                         "and 7 next elect in 2028 and Districts 4, 5, and 6 in 2030."),
         jur_sources=[('https://www.scstatehouse.gov/sess126_2025-2026/bills/5653.htm',
                       "Act 272 of 2026 (H.5653), amending Act 843 of 1952: the Lee County "
                       "School District board elected from seven single-member districts.")],
         posts=smd_posts(7), rules=smd_rules('Lee County School District', 7),
         division_bases=['Lee County School District']),
    dict(slug='lexington-1', name='Lexington County School District One',
         board_name='Lexington County School District One Board of Trustees',
         counties=['Lexington'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election at large to staggered four-year terms (Act 176 of 1995, as "
                         "amended by Act 522 of 1996)."),
         jur_sources=[('https://www.scstatehouse.gov/sess123_2019-2020/bills/3343.htm',
                       "Act 176 of 1995, as amended (H.3343 of 2019-2020): seven members of "
                       "the Lexington County School District One board elected at large.")],
         posts=[P('trustee-at-large', 'School Board Trustee At-Large', 7)],
         rules=[R('trustee-at-large', division='Lexington County School District 1')],
         division_bases=['Lexington County School District 1']),
    dict(slug='lexington-2', name='Lexington County School District Two',
         board_name='Lexington County School District Two Board of Trustees',
         counties=['Lexington'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election at large to staggered four-year terms."),
         jur_sources=[('https://ed.sc.gov/sites/scdoe/assets/archive/reportCards/2012/district/c/D3202999.pdf',
                       "SC Department of Education district report card for Lexington County "
                       "School District Two.")],
         posts=[P('trustee-at-large', 'School Board Trustee At-Large', 7)],
         rules=[R('trustee-at-large', division='Lexington County School District 2')],
         division_bases=['Lexington County School District 2']),
    dict(slug='lexington-3', name='Lexington County School District Three',
         board_name='Lexington County School District Three Board of Trustees',
         counties=['Lexington', 'Saluda'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election at large to staggered four-year terms. The district spans "
                         "Lexington and Saluda counties."),
         jur_sources=[('http://ed.sc.gov/sites/scdoe/assets/archive/reportCards/2014/district/c/D3203999.pdf',
                       "SC Department of Education district report card for Lexington County "
                       "School District Three.")],
         posts=[P('trustee-at-large', 'School Board Trustee At-Large', 7)],
         rules=[R('trustee-at-large', division='Lexington County School District 3'),
                R('trustee-at-large', division='Lexington-Saluda Counties School District 3')],
         division_bases=['Lexington County School District 3',
                         'Lexington-Saluda Counties School District 3']),
    dict(slug='lexington-4', name='Lexington County School District Four',
         board_name='Lexington County School District Four Board of Trustees',
         counties=['Lexington'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election at large to staggered four-year terms."),
         jur_sources=[('https://ed.sc.gov/sites/scdoe/assets/archive/reportCards/2013/district/c/D3204999.pdf',
                       "SC Department of Education district report card for Lexington County "
                       "School District Four.")],
         posts=[P('trustee-at-large', 'School Board Trustee At-Large', 7)],
         rules=[R('trustee-at-large', division='Lexington County School District 4')],
         division_bases=['Lexington County School District 4']),
    dict(slug='lexington-richland-5', name='Lexington-Richland School District Five',
         board_name='Lexington-Richland School District Five Board of Trustees',
         counties=['Lexington', 'Richland'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election to staggered four-year terms from county-residency areas — "
                         "not single-member districts: four seats are elected by the voters "
                         "of the Lexington County portion of the district only, and three by "
                         "the voters of the Richland County portion only. The posts model the "
                         "two county portions."),
         jur_sources=[('https://www.lexrich5.org/our-district/board-of-trustees/board-of-trustees',
                       "Lexington-Richland School District Five board of trustees page: seven "
                       "members, four from the Lexington County portion and three from the "
                       "Richland County portion.")],
         posts=[P('trustee-lexington-county', 'School Board Trustee (Lexington County)', 4),
                P('trustee-richland-county', 'School Board Trustee (Richland County)', 3)],
         rules=[R('trustee-lexington-county', division='Lexington County School District 5'),
                R('trustee-richland-county', division='Richland County School District 5')],
         division_bases=['Lexington County School District 5',
                         'Richland County School District 5',
                         'Lexington-Richland Counties School District 5']),
    dict(slug='marion-county', name='Marion County School District',
         board_name='Marion County Board of Education',
         counties=['Marion'], cycles=[], party_mode='nonpartisan', scaffold=True,
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election from seven single-member districts (the county council "
                         "districts) to staggered four-year terms (Act 304 of 2012; Act 607 of "
                         "1986). The governing body is the Marion County Board of Education. "
                         "No Marion County school district contests appear in the SEC "
                         "Election History (ElectionStats) system, so no contests or "
                         "memberships are built in this pass; certified results for the "
                         "district's two most recent elections have been requested from the "
                         "Marion County elections office."),
         jur_sources=[('http://www.scstatehouse.gov/sess119_2011-2012/bills/4632.htm',
                       "Act 304 of 2012 (H.4632): the Marion County Board of Education "
                       "elected from seven single-member districts.")],
         posts=smd_posts(7), rules=[], division_bases=['Marion County School District']),
    dict(slug='marlboro-county', name='Marlboro County School District',
         board_name='Marlboro County School District Board of Trustees',
         counties=['Marlboro'], cycles=STD_R, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general "
                         "election to staggered four-year terms: eight from single-member "
                         "districts (the county council districts) and a chairman elected "
                         "countywide as a separate office (Act 256 of 1981, as amended by "
                         "Act 611 of 1992). Two 2022 district contests (Districts 3 and 8) "
                         "were decided in majority runoffs on November 22, 2022; the initial "
                         "November 8 contests are recorded with no winner and the runoff "
                         "contests carry the certified winners."),
         jur_sources=[('http://www.scstatehouse.gov/sess109_1991-1992/bills/4583.htm',
                       "Act 611 of 1992 (H.4583), amending Act 256 of 1981: eight "
                       "single-member districts and a countywide chairman for the Marlboro "
                       "County school board.")],
         extra_sources=[('https://ed.sc.gov/newsroom/news-releases/state-board-of-education-approves-state-of-education-emergency-declaration-in-marlboro-county-school-district/',
                         "STATE TAKEOVER DISCLOSURE: SCDE placed the district on Fiscal Watch "
                         "in 2022 and declared a Fiscal Emergency on February 18, 2025, "
                         "assuming control of district finances on July 18, 2025; following an "
                         "Inspector General report dated June 1, 2026, the State Board of "
                         "Education declared a state-of-education emergency on June 2, 2026 "
                         "and SCDE assumed full management of the district, with the elected "
                         "board dissolved. The memberships built in this pass are the board "
                         "as elected in 2022 and 2024; the district is currently governed by "
                         "SCDE, not by the elected board. The district is classified ELECTED "
                         "(SUSPENDED - state takeover 2026), parallel to Jasper County.")],
         posts=smd_posts(8) + [P('chairman', 'School Board Chairman', 1)],
         rules=smd_rules('Marlboro County School District', 8) +
               [R('chairman', division='Marlboro County School District',
                  office='School Board Chairman')],
         division_bases=['Marlboro County School District']),
    dict(slug='mccormick-county', name='McCormick County School District',
         board_name='McCormick County School District Board of Trustees',
         counties=['McCormick'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election at large (countywide) to staggered four-year terms (Act 185 "
                         "of 1997, as restated by Act 279 of 2018). A 2007 residency-district "
                         "act never became operative."),
         jur_sources=[],
         posts=[P('trustee-at-large', 'School Board Trustee At-Large', 7)],
         rules=[R('trustee-at-large', division='McCormick County School District',
                  modifier='At Large'),
                R('trustee-at-large', division='McCormick County School District',
                  modifier='')],
         division_bases=['McCormick County School District']),
    dict(slug='newberry-county', name='Newberry County School District',
         board_name='Newberry County Board of Education',
         counties=['Newberry'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election from seven single-member districts (the county council "
                         "districts) to staggered four-year terms (Act 485 of 1998)."),
         jur_sources=[('https://files-backend.assets.thrillshare.com/documents/asset/uploaded_file/1079/Sdnc/3598d99e-f1a6-4ba2-9099-dec6c6dd353b/March_24__2025_Board_Packet_-_Public.pdf?disposition=inline',
                       "School District of Newberry County board packet (March 24, 2025), "
                       "showing the seven district seats of the Newberry County Board of "
                       "Education.")],
         posts=smd_posts(7), rules=smd_rules('Newberry County School District', 7),
         division_bases=['Newberry County School District']),
    dict(slug='oconee-county', name='School District of Oconee County',
         board_name='School District of Oconee County Board of Trustees',
         counties=['Oconee'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Five members elected in nonpartisan elections at the general "
                         "election from five single-member districts (the county council "
                         "districts) to staggered four-year terms (Act 613 of 1992, Section 6, "
                         "as amended by Act 488 of 1998)."),
         jur_sources=[],
         posts=smd_posts(5), rules=smd_rules('Oconee County School District', 5),
         division_bases=['Oconee County School District']),
    dict(slug='orangeburg-county', name='Orangeburg County School District',
         board_name='Orangeburg County School District Board of Trustees',
         counties=['Orangeburg'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general "
                         "election to staggered four-year terms: seven from single-member "
                         "districts (the county council districts) and two at-large seats "
                         "with residency restrictions — Seat 8 for residents of council "
                         "Districts 1-4 and Seat 9 for residents of council Districts 5-7 "
                         "(Act 280 of 2017). In the ElectionStats data the two at-large seats "
                         "appear as bare-division 'At Large' contests; the district's first "
                         "contests (2018) tie the Seat 8 race to the division labeled "
                         "District 8 and the Seat 9 race to District 9, and the at-large "
                         "contests alternate cycles — the 2022 at-large contest is assigned "
                         "to Seat 9 and the 2024 contest to Seat 8 on that cycle evidence."),
         jur_sources=[('https://www.scstatehouse.gov/sess122_2017-2018/bills/662.htm',
                       "Act 280 of 2017 (S.662): consolidation of the Orangeburg County "
                       "school districts; seven single-member districts and two "
                       "residency-restricted at-large seats (Seats 8 and 9).")],
         posts=smd_posts(7) + [P('seat-8', 'School Board Seat 8', 1,
                                 note="At-large seat; candidates must reside in county council "
                                      "Districts 1-4 (Act 280 of 2017)."),
                               P('seat-9', 'School Board Seat 9', 1,
                                 note="At-large seat; candidates must reside in county council "
                                      "Districts 5-7 (Act 280 of 2017).")],
         rules=smd_rules('Orangeburg County School District', 7) +
               [R('seat-8', division='Orangeburg County School District',
                  modifier='At Large', dates=['2024-11-05']),
                R('seat-9', division='Orangeburg County School District',
                  modifier='At Large', dates=['2022-11-08'])],
         division_bases=['Orangeburg County School District']),
]

SPART_CYCLE_NOTE = (" Spartanburg County school districts elect in odd-year November elections; "
                    "the two most recent cycles in the ElectionStats system are 2021 and 2023 "
                    "(the November 2025 election is not yet loaded in the system).")
DISTRICTS += [
    dict(slug='pickens-county', name='Pickens County School District',
         board_name='Pickens County School District Board of Trustees',
         counties=['Pickens'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election from seven single-member districts to staggered four-year "
                         "terms (Act 260 of 1981, as amended). The Phase 1 classification "
                         "described six districts; the district's own board page (a "
                         "seven-member board, one member from each of seven districts) and "
                         "the ElectionStats contests both show seven — District 7 (the "
                         "Dacusville/Pickens area) was contested in 2018, in a 2021 "
                         "unexpired-term special election, and in 2022 — and the build "
                         "follows the contests and the district's published structure."),
         jur_sources=[('https://www.pickens.k12.sc.us/page/sdpc-school-board/',
                       "School District of Pickens County board of trustees page: a "
                       "seven-member board, one member elected from each of seven districts "
                       "to staggered four-year terms.")],
         posts=smd_posts(7), rules=smd_rules('Pickens County School District', 7),
         division_bases=['Pickens County School District']),
    dict(slug='richland-1', name='Richland County School District One',
         board_name='Richland One Board of School Commissioners',
         counties=['Richland'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election to staggered four-year terms: four from single-member "
                         "districts and three at large (Act 613 of 1986, as amended by Act 300 "
                         "of 2016). The governing body is styled the Board of School "
                         "Commissioners. On the ballot the single-member districts are labeled "
                         "Seat 1 through Seat 4; in the 2022 ElectionStats data the District 1 "
                         "and District 3 contests appear at the divisions 'Richland County "
                         "School District 11' and 'Richland County School District 13' (won "
                         "by Aaron Bishop and Robert Lominack, the Seat 1 and Seat 3 "
                         "incumbents) and are built as Districts 1 and 3."),
         jur_sources=[('https://www.scstatehouse.gov/sess121_2015-2016/bills/863.htm',
                       "Act 300 of 2016 (H.863), amending Act 613 of 1986: Richland County "
                       "School District One — four single-member districts and three at-large "
                       "seats.")],
         posts=smd_posts(4) + [P('trustee-at-large', 'School Board Trustee At-Large', 3)],
         rules=[R('district-1', division='Richland County School District 11'),
                R('district-3', division='Richland County School District 13'),
                R('district-2', division='Richland County School District 1',
                  modifier='Seat 2'),
                R('district-4', division='Richland County School District 1',
                  modifier='Seat 4'),
                R('trustee-at-large', division='Richland County School District 1',
                  modifier='At Large'),
                R('trustee-at-large', division='Richland County School District 1',
                  modifier='')],
         division_bases=['Richland County School District 1',
                         'Richland County School District 11',
                         'Richland County School District 13']),
    dict(slug='richland-2', name='Richland School District Two',
         board_name='Richland School District Two Board of Trustees',
         counties=['Richland'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election at large to staggered four-year terms (Act 613 of 1986, "
                         "Section 3)."),
         jur_sources=[('https://www.richland2.org/school-board/members',
                       "Richland School District Two board members page: seven trustees "
                       "elected at large.")],
         posts=[P('trustee-at-large', 'School Board Trustee At-Large', 7)],
         rules=[R('trustee-at-large', division='Richland County School District 2')],
         division_bases=['Richland County School District 2']),
    dict(slug='rock-hill', name='Rock Hill Schools',
         board_name='Rock Hill Schools Board of Trustees',
         counties=['York'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election to staggered four-year terms: five from single-member "
                         "districts and two at large (Act 470 of 2000; districts reapportioned "
                         "by Act 101 of 2023)."),
         jur_sources=[],
         posts=smd_posts(5) + [P('trustee-at-large', 'School Board Trustee At-Large', 2)],
         rules=seatmod_rules('Rock Hill School District', range(1, 6), atlarge_seats=2) +
               [R('trustee-at-large', division='Rock Hill School District',
                  modifier='At Large, Unexpired Term')],
         division_bases=['Rock Hill School District']),
    dict(slug='saluda-county', name='Saluda County Schools',
         board_name='Saluda County Schools Board of Trustees',
         counties=['Saluda'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election from seven single-member districts to staggered four-year "
                         "terms (2012 reapportionment act). Vacancies are filled by the "
                         "Governor on the legislative delegation's recommendation; all regular "
                         "seats are filled by election."),
         jur_sources=[('https://ed.sc.gov/sites/scdoe/assets/archive/reportCards/2013/district/c/D4101999.pdf',
                       "SC Department of Education district report card for Saluda County "
                       "Schools.")],
         posts=smd_posts(7),
         rules=seatmod_rules('Saluda County School District 1', range(1, 8)),
         division_bases=['Saluda County School District 1']),
    dict(slug='spartanburg-1', name='Spartanburg School District One',
         board_name='Spartanburg School District One Board of Trustees',
         counties=['Spartanburg'], cycles=SPART, party_mode='nonpartisan',
         cycle_note=SPART_CYCLE_NOTE,
         structure_note=("Nine members elected in nonpartisan elections at large to staggered "
                         "four-year terms at odd-year November elections (Act 612 of 1984). "
                         "No 2023 contest for this district appears in the ElectionStats "
                         "system; only the 2021 contests are built."),
         jur_sources=[],
         posts=[P('trustee-at-large', 'School Board Trustee At-Large', 9)],
         rules=[R('trustee-at-large', division='Spartanburg County School District 1')],
         division_bases=['Spartanburg County School District 1']),
    dict(slug='spartanburg-2', name='Spartanburg School District Two',
         board_name='Spartanburg School District Two Board of Trustees',
         counties=['Spartanburg', 'Cherokee'], cycles=SPART, party_mode='nonpartisan',
         cycle_note=SPART_CYCLE_NOTE,
         structure_note=("Ten members elected in nonpartisan elections to staggered four-year "
                         "terms at odd-year November elections: nine at large and one from "
                         "Trustee District 10, the district's Cherokee County portion (Act 612 "
                         "of 1984; Act 572 of 1982). The District 10 contest appears in the "
                         "ElectionStats data at the division 'Cherokee County School District "
                         "2'; its 2023 winner, Seth Breitenbach, holds the Cherokee County seat "
                         "(term December 1, 2023 - November 30, 2027 per the district's board "
                         "listing)."),
         jur_sources=[],
         posts=[P('trustee-at-large', 'School Board Trustee At-Large', 9),
                P('district-10', 'School Board District 10', 1)],
         rules=[R('trustee-at-large', division='Spartanburg County School District 2'),
                R('district-10', division='Cherokee County School District 2')],
         division_bases=['Spartanburg County School District 2',
                         'Cherokee County School District 2']),
    dict(slug='spartanburg-3', name='Spartanburg School District Three',
         board_name='Spartanburg School District Three Board of Trustees',
         counties=['Spartanburg'], cycles=SPART, party_mode='nonpartisan',
         cycle_note=SPART_CYCLE_NOTE,
         structure_note=("Nine members elected in nonpartisan elections at large to staggered "
                         "four-year terms at odd-year November elections (Act 612 of 1984)."),
         jur_sources=[],
         posts=[P('trustee-at-large', 'School Board Trustee At-Large', 9)],
         rules=[R('trustee-at-large', division='Spartanburg County School District 3')],
         division_bases=['Spartanburg County School District 3']),
    dict(slug='spartanburg-4', name='Spartanburg School District Four',
         board_name='Spartanburg School District Four Board of Trustees',
         counties=['Spartanburg'], cycles=SPART, party_mode='nonpartisan',
         cycle_note=SPART_CYCLE_NOTE,
         structure_note=("Nine members elected in nonpartisan elections at large to staggered "
                         "four-year terms at odd-year November elections (Act 612 of 1984)."),
         jur_sources=[],
         posts=[P('trustee-at-large', 'School Board Trustee At-Large', 9)],
         rules=[R('trustee-at-large', division='Spartanburg County School District 4')],
         division_bases=['Spartanburg County School District 4']),
    dict(slug='spartanburg-5', name='Spartanburg School District Five',
         board_name='Spartanburg School District Five Board of Trustees',
         counties=['Spartanburg'], cycles=SPART, party_mode='nonpartisan',
         cycle_note=SPART_CYCLE_NOTE,
         structure_note=("Nine members elected in nonpartisan elections to staggered four-year "
                         "terms at odd-year November elections from three multimember "
                         "residency districts — District 51 (one seat), District 52 (two "
                         "seats), and District 53 (six seats) — whose members are elected by "
                         "the voters of the whole district (Act 106 of 2015, as amended). No "
                         "contest for District 52 appears in the ElectionStats data in any "
                         "cycle; that post is built without memberships."),
         jur_sources=[],
         posts=[P('district-51', 'School Board District 51', 1),
                P('district-52', 'School Board District 52', 2),
                P('district-53', 'School Board District 53', 6)],
         rules=[R('district-51', division='Spartanburg County School District 51'),
                R('district-53', division='Spartanburg County School District 53')],
         division_bases=['Spartanburg County School District 5',
                         'Spartanburg County School District 51',
                         'Spartanburg County School District 52',
                         'Spartanburg County School District 53']),
    dict(slug='spartanburg-6', name='Spartanburg School District Six',
         board_name='Spartanburg School District Six Board of Trustees',
         counties=['Spartanburg'], cycles=SPART, party_mode='nonpartisan',
         cycle_note=SPART_CYCLE_NOTE,
         structure_note=("Nine members elected in nonpartisan elections at large to staggered "
                         "four-year terms at odd-year November elections (Act 612 of 1984)."),
         jur_sources=[],
         posts=[P('trustee-at-large', 'School Board Trustee At-Large', 9)],
         rules=[R('trustee-at-large', division='Spartanburg County School District 6')],
         division_bases=['Spartanburg County School District 6']),
    dict(slug='spartanburg-7', name='Spartanburg School District Seven',
         board_name='Spartanburg School District Seven Board of Trustees',
         counties=['Spartanburg'], cycles=SPART, party_mode='nonpartisan',
         cycle_note=SPART_CYCLE_NOTE,
         structure_note=("Nine members elected in nonpartisan elections to staggered four-year "
                         "terms at odd-year November elections from five election districts "
                         "(Act 98 of 2023): Districts 71-74 hold one seat each and District 75 "
                         "holds five, the allocation consistent with the act's district "
                         "populations and with the ElectionStats contest sizes (District 75 "
                         "elects three members in one odd-year cycle and two in the next)."),
         jur_sources=[],
         posts=[P('district-71', 'School Board District 71', 1),
                P('district-72', 'School Board District 72', 1),
                P('district-73', 'School Board District 73', 1),
                P('district-74', 'School Board District 74', 1),
                P('district-75', 'School Board District 75', 5)],
         rules=[R(f'district-{i}', division=f'Spartanburg County School District {i}')
                for i in (71, 72, 73, 74, 75)],
         division_bases=['Spartanburg County School District 7',
                         'Spartanburg County School District 71',
                         'Spartanburg County School District 72',
                         'Spartanburg County School District 73',
                         'Spartanburg County School District 74',
                         'Spartanburg County School District 75']),
    dict(slug='sumter-county', name='Sumter School District',
         board_name='Sumter School District Board of Trustees',
         counties=['Sumter'], cycles=STD_R, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general "
                         "election from nine single-member districts to staggered four-year "
                         "terms (Act 387 of 2008, as amended). The district's own board "
                         "materials and the SC Inspector General describe a nine-member "
                         "elected board, and the ElectionStats contests run in nine districts; "
                         "Districts 8 and 9 began as at-large seats under Act 321 of 2010 and "
                         "are now elected from districts. Four 2022 contests (Districts 1, 2, "
                         "4, and 8) were decided in majority runoffs on "
                         "November 22, 2022; the initial November 8 contests are recorded "
                         "with no winner and the runoffs carry the certified winners. A "
                         "fiscal emergency declared in 2019 did not dissolve the board."),
         jur_sources=[('http://www.scstatehouse.gov/sess118_2009-2010/bills/773.htm',
                       "Act 387 of 2008, as amended (H.773 of 2009-2010): the Sumter School "
                       "District board elected from single-member districts.")],
         posts=smd_posts(9), rules=smd_rules('Sumter County School District', 9),
         division_bases=['Sumter County School District']),
    dict(slug='union-county', name='Union County Schools',
         board_name='Union County Schools Board of Trustees',
         counties=['Union'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general "
                         "election from nine single-member districts to staggered four-year "
                         "terms (Act 304 of 1989, as reapportioned by Act 108 of 2015)."),
         jur_sources=[],
         posts=smd_posts(9), rules=smd_rules('Union County School District', 9),
         division_bases=['Union County School District']),
    dict(slug='williamsburg-county', name='Williamsburg County School District',
         board_name='Williamsburg County School District Board of Trustees',
         counties=['Williamsburg'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Nine members elected in nonpartisan elections at the general "
                         "election to staggered four-year terms: seven from single-member "
                         "districts (the county council districts) and two at large (Act 107 "
                         "of 2017). The district was under SCDE control from 2018, with "
                         "governance responsibilities returned to the elected board in stages "
                         "beginning in 2024; the board's selection has remained elective."),
         jur_sources=[('https://www.scstatehouse.gov/sess122_2017-2018/bills/568.htm',
                       "Act 107 of 2017 (S.568): Williamsburg County School District — seven "
                       "single-member districts and two at-large seats.")],
         posts=smd_posts(7) + [P('trustee-at-large', 'School Board Trustee At-Large', 2)],
         rules=smd_rules('Williamsburg County School District', 7) +
               [R('trustee-at-large', division='Williamsburg County School District',
                  modifier='At Large')],
         division_bases=['Williamsburg County School District']),
    dict(slug='york-1', name='York School District 1',
         board_name='York School District 1 Board of Trustees',
         counties=['York'], cycles=STD, party_mode='nonpartisan',
         structure_note=("Seven members elected in nonpartisan elections at the general "
                         "election to staggered four-year terms: five from single-member "
                         "districts and two at large (Act 469 of 2000)."),
         jur_sources=[],
         posts=smd_posts(5) + [P('trustee-at-large', 'School Board Trustee At-Large', 2)],
         rules=seatmod_rules('York County School District', range(1, 6), atlarge_seats=2),
         division_bases=['York County School District']),
    dict(slug='bamberg-county', name='Bamberg County School District',
         board_name='Bamberg County School District Board of Trustees',
         counties=['Bamberg'], cycles=['2024-11-05'], party_mode='nonpartisan',
         structure_note=("Nine seats: seven single-member districts and two at-large seats "
                         "designated Districts 8 and 9 (Act 104 of 2021, as rewritten by "
                         "Act 233 of 2024). Only the five seats elected in November 2024 are "
                         "seated in this pass."),
         jur_sources=[('https://www.scstatehouse.gov/sess125_2023-2024/bills/5231.htm',
                       "Act 233 of 2024 (H.5231): the Bamberg County School District "
                       "transition — five seats elected in November 2024, four "
                       "delegation-appointed holdovers until November 2026.")],
         extra_sources=[('https://www.scstatehouse.gov/sess125_2023-2024/bills/5231.htm',
                         "TRANSITION DISCLOSURE: Act 104 of 2021 consolidated Bamberg-Ehrhardt "
                         "District 1 and Denmark-Olar District 2 under an initially "
                         "delegation-appointed nine-member board (seven single-member "
                         "districts and two at-large seats, designated Districts 8 and 9). "
                         "Under Act 233 of 2024, five seats were elected in November 2024 "
                         "(Districts 1, 4, 5, 7, and at-large District 8) and are seated in "
                         "this pass; the remaining four seats (Districts 2, 3, 6, and 9) are "
                         "held by Bamberg County Legislative Delegation appointees who serve "
                         "until successors are elected November 3, 2026 — those posts are "
                         "built without memberships.")],
         posts=smd_posts(9),
         post_notes={'district-2': ("Seat held by a Bamberg County Legislative Delegation "
                                    "appointee under Act 233 of 2024 until a successor is "
                                    "elected November 3, 2026; no membership is built in this "
                                    "pass."),
                     'district-3': ("Seat held by a Bamberg County Legislative Delegation "
                                    "appointee under Act 233 of 2024 until a successor is "
                                    "elected November 3, 2026; no membership is built in this "
                                    "pass."),
                     'district-6': ("Seat held by a Bamberg County Legislative Delegation "
                                    "appointee under Act 233 of 2024 until a successor is "
                                    "elected November 3, 2026; no membership is built in this "
                                    "pass."),
                     'district-9': ("At-large seat held by a Bamberg County Legislative "
                                    "Delegation appointee under Act 233 of 2024 until a "
                                    "successor is elected November 3, 2026; no membership is "
                                    "built in this pass.")},
         rules=smd_rules('Bamberg County School District', 9),
         division_bases=['Bamberg County School District']),
]


# ---------------------------------------------------------------- engine
def rule_matches(rule, c):
    if rule['office'] is not None and c['office'] != rule['office']:
        return False
    if rule['dates'] is not None and c['date'] not in rule['dates']:
        return False
    div = c['division'] or ''
    if rule['dre'] is not None:
        if not re.fullmatch(rule['dre'], div):
            return False
    elif rule['division'] is not None and div != rule['division']:
        return False
    mod = c['modifier'] or ''
    if rule['in'] is not None:
        if mod not in rule['in']:
            return False
    elif rule['modifier'] is not None and mod != rule['modifier']:
        return False
    return True


def party_out(cfg, party):
    if cfg['party_mode'] == 'asis':
        return party  # may be None -> emitted as null
    return party or 'Nonpartisan'


def main():
    contests = load_contests()
    people_index = load_people_index()
    pdir = SC / f'people/{TIER}'
    if pdir.exists():
        for f in pdir.glob('*.yaml'):
            FILE_OWNER[f.stem] = _yaml.safe_load(f.read_text()).get('name', '')
    school_file_district = {}
    for entries in people_index.values():
        for e in entries:
            if e['tier'] == TIER:
                for d in e['districts']:
                    school_file_district[e['slug']] = d

    report = {'districts': [], 'unmapped': [], 'check_failures': [], 'ties': [],
              'party_anomalies': [], 'asis_missing_party': [], 'zero_candidate': [],
              'seats_exceed': [], 'succession_unknown': [], 'nocheck': [],
              'possible_duplicates': [], 'excluded_office_contests': 0,
              'totals': defaultdict(int)}
    election_appends = defaultdict(list)
    merges = []
    people_touched = {}

    for cfg in DISTRICTS:
        dslug = cfg['slug']
        jur_id = f'ocd-jurisdiction/country:us/state:sc/school_district:{dslug}/school'
        div_id = f'ocd-division/country:us/state:sc/school_district:{dslug}'
        oid = org_uuid(dslug)
        org_stem = f'{dslug}-school-board'
        scaffold = cfg.get('scaffold', False)
        drep = {'district': cfg['name'], 'slug': dslug, 'scaffold': scaffold,
                'posts': 0, 'posts_without_contests': [], 'contests': 0,
                'memberships': 0, 'people_new': 0, 'people_merged': 0,
                'unifications': []}

        # ---- select contests for this district
        assigned = defaultdict(list)   # post key -> [contest]
        for c in contests.values():
            if c['office'] not in SCHOOL_OFFICES or c['etype'] != 'General':
                continue
            if c['date'] not in cfg['cycles'] or c['is_special']:
                continue
            for rule in cfg['rules']:
                if rule_matches(rule, c):
                    assigned[rule['post']].append(c)
                    break
        scoped = [c for cs in assigned.values() for c in cs]
        scoped.sort(key=lambda c: (c['date'], c['id']))

        # ---- unmapped-contest audit for this district's divisions
        for c in contests.values():
            if c['office'] not in SCHOOL_OFFICES or c['etype'] != 'General':
                continue
            if c['date'] not in cfg['cycles']:
                continue
            div = c['division'] or ''
            if not any(div == b or div.startswith(b + ' ') or div.startswith(b)
                       for b in cfg['division_bases']):
                continue
            if c in scoped:
                continue
            if c['office'] in ('Constituent School Board', 'Consolidated School Board'):
                report['excluded_office_contests'] += 1
                continue
            report['unmapped'].append({'district': cfg['name'], 'id': c['id'],
                                       'date': c['date'], 'office': c['office'],
                                       'division': div, 'modifier': c['modifier'],
                                       'seats': c['seats'], 'special': c['is_special'],
                                       'ncands': len(named(c))})

        # ---- cross-checks + party anomalies
        for c in scoped:
            chk = check(c)
            if chk is False:
                report['check_failures'].append({'district': cfg['name'], 'id': c['id'],
                                                 'date': c['date'], 'division': c['division'],
                                                 'modifier': c['modifier']})
            elif chk is None:
                report['nocheck'].append({'district': cfg['name'], 'id': c['id'],
                                          'date': c['date'], 'division': c['division'],
                                          'modifier': c['modifier']})
            for n, v, p in named(c):
                if cfg['party_mode'] == 'nonpartisan' and p not in (None, 'Nonpartisan'):
                    report['party_anomalies'].append({'district': cfg['name'], 'id': c['id'],
                                                      'name': n, 'party': p})
                if cfg['party_mode'] == 'asis' and p is None:
                    report['asis_missing_party'].append({'district': cfg['name'],
                                                         'id': c['id'], 'name': n})

        # ---- variant clustering within this district
        forms_by_scope = defaultdict(set)
        cooccur = defaultdict(set)
        per_contest = defaultdict(set)
        for c in scoped:
            for n, v, p in named(c):
                per_contest[c['id']].add(n)
        for cid, names_ in per_contest.items():
            for n in names_:
                forms_by_scope[dslug].add(n)
                for m in names_:
                    if m != n:
                        cooccur[n].add(m)
        canon, clusters_of = build_canon(forms_by_scope, cooccur)

        def resolve_person(canonical):
            entries = people_index.get(canonical, [])
            for e in entries:
                if e['tier'] == TIER and dslug in e['districts']:
                    return ('new', e['slug'], e['id'], e)
            for e in entries:
                if e['tier'] != TIER and set(cfg['counties']) & e['counties']:
                    return ('existing', e['slug'], e['id'], e)
            for e in entries:
                if e['tier'] == TIER and set(cfg['counties']) & e['counties']:
                    report['possible_duplicates'].append(
                        {'name': canonical, 'district': cfg['name'],
                         'other_districts': sorted(e['districts'])})
            base = slugify(canonical)
            owner = FILE_OWNER.get(base)
            if owner is not None and owner != canonical:
                slug = base + '-' + str(uuid.uuid5(NS, f'person|sc|{TIER}|{dslug}|{base}'))[:8]
                return ('new', slug, person_uuid(base, dslug), None)
            if owner is not None and school_file_district.get(base) not in (None, dslug):
                slug = base + '-' + str(uuid.uuid5(NS, f'person|sc|{TIER}|{dslug}|{base}'))[:8]
                return ('new', slug, person_uuid(base, dslug), None)
            claim = CLAIMED.get(base)
            if claim is None or claim == (dslug, canonical):
                CLAIMED[base] = (dslug, canonical)
                FILE_OWNER[base] = canonical
                return ('new', base, person_uuid(base), None)
            slug = base + '-' + str(uuid.uuid5(NS, f'person|sc|{TIER}|{dslug}|{base}'))[:8]
            return ('new', slug, person_uuid(base, dslug), None)

        # ---- superseded (runoff) determination per post
        superseded = set()
        for key, cs in assigned.items():
            for c in cs:
                for c2 in cs:
                    if c2['is_runoff'] and c2['date'] > c['date']:
                        d1 = int(c['date'].replace('-', ''))
                        d2 = int(c2['date'].replace('-', ''))
                        if c2['date'][:4] == c['date'][:4] and d2 - d1 <= 21:
                            superseded.add(c['id'])

        # ---- org note
        if scaffold:
            org_note = cfg['structure_note']
            first_url = cfg['jur_sources'][0][0] if cfg['jur_sources'] \
                else 'https://electionhistory.scvotes.gov/'
        else:
            note_dates = sorted({c['date'] for c in scoped if not c['is_runoff']}) \
                or list(cfg['cycles'])
            if len(note_dates) == 1:
                cycles_txt = datename(note_dates[0])
            elif len(note_dates) == 2:
                cycles_txt = ' and '.join(datename(d) for d in note_dates)
            else:
                cycles_txt = ', '.join(datename(d) for d in note_dates[:-1]) \
                    + ', and ' + datename(note_dates[-1])
            offices_txt = ' and '.join(sorted({c['office'] for c in scoped}))
            org_note = (f"{cfg['name']}, built from the SC State Election Commission "
                        f"Election History results for the {cycles_txt} general elections "
                        f"({offices_txt} contests) in the ElectionStats school board data. "
                        f"{cfg['structure_note']}{cfg.get('cycle_note', '')}")
            first_url = f"https://electionhistory.scvotes.gov/contest/{scoped[0]['id']}"

        # ---- jurisdiction
        jur_src_lines = []
        jur_entries = list(cfg['jur_sources'])
        if not jur_entries:
            jur_entries = [(first_url, cfg['structure_note'])]
        jur_entries += cfg.get('extra_sources', [])
        for u, n in jur_entries:
            jur_src_lines.append(f"- url: {u}\n  note: {q(n)}\n  retrieved: '{RETRIEVED}'")
        (SC / f'jurisdictions/{TIER}').mkdir(exist_ok=True)
        (SC / f'jurisdictions/{TIER}/{dslug}-school.yaml').write_text(HEADER + f"""id: {jur_id}
name: {cfg['name']}
state: sc
division_id: {div_id}
classification: school
sources:
{chr(10).join(jur_src_lines)}
""")
        report['totals']['jurisdictions'] += 1

        # ---- organization
        org_src = [f"- url: {first_url}\n  note: {q(org_note)}\n  retrieved: '{RETRIEVED}'"]
        for u, n in cfg.get('extra_sources', []):
            org_src.append(f"- url: {u}\n  note: {q(n)}\n  retrieved: '{RETRIEVED}'")
        (SC / f'organizations/{TIER}').mkdir(exist_ok=True)
        (SC / f'organizations/{TIER}/{org_stem}.yaml').write_text(HEADER + f"""id: {oid}
name: {cfg['board_name']}
jurisdiction_id: {jur_id}
identifiers: []
sources:
{chr(10).join(org_src)}
""")
        report['totals']['organizations'] += 1

        # ---- posts, people, memberships, election blocks
        for post in cfg['posts']:
            key = post['key']
            pid_post = post_id_of(dslug, key)
            post_stem = f"{org_stem}-{key}"
            post_note = post.get('note') or cfg.get('post_notes', {}).get(key)
            cs = sorted(assigned.get(key, []), key=lambda c: (c['date'], c['id']))
            pnote = org_note + (f" {post_note}" if post_note else '')
            purl = f"https://electionhistory.scvotes.gov/contest/{cs[0]['id']}" if cs \
                else first_url
            (SC / f'posts/{TIER}').mkdir(exist_ok=True)
            (SC / f'posts/{TIER}/{post_stem}.yaml').write_text(HEADER + f"""id: {pid_post}
organization_id: {oid}
title: {post['title']}
seats: {post['seats']}
identifiers: []
sources:
- url: {purl}
  note: {q(pnote)}
  retrieved: '{RETRIEVED}'
""")
            drep['posts'] += 1
            report['totals']['posts'] += 1
            if not cs:
                drep['posts_without_contests'].append(key)
                continue

            seat_winners = {}   # canonical -> [deciding contests won]
            events = []         # (date, winner canonical or None) deciding, seats==1 use
            for c in cs:
                note = tally_note(c, cfg)
                cands = named(c)
                is_sup = c['id'] in superseded
                winners = []
                if not is_sup:
                    winners = cands[:c['seats']]
                    if len(cands) > c['seats'] and cands[c['seats'] - 1][1] == cands[c['seats']][1]:
                        boundary = cands[c['seats']][1]
                        winners = [w for w in cands[:c['seats']] if w[1] > boundary]
                        report['ties'].append({'district': cfg['name'], 'id': c['id'],
                                               'date': c['date'], 'division': c['division'],
                                               'modifier': c['modifier'], 'boundary_votes': boundary})
                cand_ids = []
                for raw, votes, party in cands:
                    canonical = canon.get((dslug, raw), raw)
                    kind, pslug, pid, entry = resolve_person(canonical)
                    cand_ids.append(pid)
                    cand = {'ballot_name': raw,
                            'contest_id': None,  # filled below
                            'election_id': f"sc/{c['date']}/general",
                            'jurisdiction_id': jur_id, 'office_id': pid_post,
                            'party': party_out(cfg, party)}
                    suffix = '-unexpired-term' if 'Unexpired Term' in (c['modifier'] or '') else ''
                    cand['contest_id'] = f"sc/{c['date']}/{pid_post.replace('/', '-')}{suffix}"
                    if kind == 'existing':
                        merges.append((dslug, entry, cand, note, c['id']))
                    else:
                        acc = people_touched.setdefault((pslug, pid), {
                            'name': canonical, 'slug': pslug, 'pid': pid, 'cands': [],
                            'sources': [], 'district': dslug,
                            'cluster_forms': clusters_of.get((dslug, canonical))})
                        if cand not in acc['cands']:
                            acc['cands'].append(cand)
                        if (note, c['id']) not in acc['sources']:
                            acc['sources'].append((note, c['id']))
                if not cands:
                    report['zero_candidate'].append({'district': cfg['name'], 'id': c['id'],
                                                     'date': c['date'],
                                                     'division': c['division'],
                                                     'modifier': c['modifier']})
                # election block
                suffix = '-unexpired-term' if 'Unexpired Term' in (c['modifier'] or '') else ''
                block_id = f"sc/{c['date']}/{pid_post.replace('/', '-')}{suffix}"
                if cand_ids and winners:
                    wlines = []
                    for raw, votes, party in winners:
                        canonical = canon.get((dslug, raw), raw)
                        _, _, wpid, _ = resolve_person(canonical)
                        pout = party_out(cfg, party)
                        wlines.append(f"""  - name: {raw}
    party: {pout if pout is not None else 'null'}
    person_id: {wpid}
    votes: {votes}""")
                    block = f"""- id: {block_id}
  jurisdiction_id: {jur_id}
  office_id: {pid_post}
  vote_for: {c['seats']}
  candidate_ids:
{chr(10).join('  - ' + i for i in cand_ids)}
  result_status: certified
  winners:
{chr(10).join(wlines)}
"""
                elif cand_ids:
                    block = f"""- id: {block_id}
  jurisdiction_id: {jur_id}
  office_id: {pid_post}
  vote_for: {c['seats']}
  candidate_ids:
{chr(10).join('  - ' + i for i in cand_ids)}
  result_status: official
  winners: []
"""
                else:
                    block = f"""- id: {block_id}
  jurisdiction_id: {jur_id}
  office_id: {pid_post}
  vote_for: {c['seats']}
  candidate_ids: []
  result_status: official
  winners: []
"""
                election_appends[c['date']].append((pid_post, block))
                drep['contests'] += 1
                report['totals']['contests'] += 1
                if not is_sup:
                    win_can = [canon.get((dslug, raw), raw) for raw, v, p in winners]
                    for wc in win_can:
                        seat_winners.setdefault(wc, []).append(c)
                    if post['seats'] == 1:
                        events.append((c['date'], win_can[0] if win_can else None))

            # memberships
            if post['seats'] > 1 and len(seat_winners) > post['seats']:
                report['seats_exceed'].append({'district': cfg['name'], 'post': key,
                                               'seats': post['seats'],
                                               'winners': len(seat_winners)})
            for canonical, won_cs in seat_winners.items():
                kind, pslug, pid, entry = resolve_person(canonical)
                stem = f'{post_stem}-{pslug}'
                first_c = won_cs[0]
                start = str(int(first_c['date'][:4]) + 1)
                end = None
                if post['seats'] == 1:
                    won_dates = {c['date'] for c in won_cs}
                    for edate, ewinner in events:
                        if edate in won_dates:
                            continue
                        if edate <= first_c['date']:
                            continue
                        if ewinner is None:
                            report['succession_unknown'].append(
                                {'district': cfg['name'], 'post': key,
                                 'person': canonical, 'contest_date': edate})
                            continue
                        if ewinner != canonical:
                            end = edate[:4]
                            break
                notes = [tally_note(c, cfg) for c in won_cs]
                note = ' '.join(notes)
                if len(won_cs) > 1:
                    note += f" One continuous membership from the {first_c['date'][:4]} win."
                endline = f"\nend: '{end}'" if end else ''
                (SC / f'memberships/{TIER}').mkdir(exist_ok=True)
                (SC / f'memberships/{TIER}/{stem}.yaml').write_text(f"""how_seated: elected
id: {stem}
organization_id: {oid}
person_id: {pid}
post_id: {pid_post}
role: {post['title']}{endline}
sources:
- note: {q(note)}
  retrieved: '{RETRIEVED}'
  url: https://electionhistory.scvotes.gov/contest/{first_c['id']}
start: '{start}'
""")
                drep['memberships'] += 1
                report['totals']['memberships'] += 1
        report['districts'].append(drep)

    # ---- emit new people
    (SC / f'people/{TIER}').mkdir(exist_ok=True)
    drep_by_slug = {d['slug']: d for d in report['districts']}
    for (pslug, pid), acc in sorted(people_touched.items()):
        path = SC / f'people/{TIER}/{pslug}.yaml'
        if path.exists():
            continue
        cand_lines = []
        for cd in sorted(acc['cands'], key=lambda e: e['election_id']):
            pout = cd['party']
            cand_lines.append(f"""- ballot_name: {cd['ballot_name']}
  contest_id: {cd['contest_id']}
  election_id: {cd['election_id']}
  jurisdiction_id: {cd['jurisdiction_id']}
  office_id: {cd['office_id']}
  party: {pout if pout is not None else 'null'}
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
            drep_by_slug[acc['district']]['unifications'].append(
                (acc['name'], acc['cluster_forms']))
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
        drep_by_slug[acc['district']]['people_new'] += 1
        report['totals']['people_new'] += 1

    # ---- merges into existing files (host-style textual append)
    merged_done = set()
    for dslug, entry, cand, note, cid in merges:
        path = entry['path']
        text = path.read_text()
        if cand['contest_id'] in text:
            continue
        pout = cand['party']
        party_txt = pout if pout is not None else 'null'
        style = entry['data'].get('verification', {}).get('pipeline', '')
        if style == 'build_sc_municipal':
            cand_block = f"""- contest_id: {cand['contest_id']}
  election_id: {cand['election_id']}
  jurisdiction_id: {cand['jurisdiction_id']}
  office_id: {cand['office_id']}
  party: {party_txt}
  ballot_name: {q(cand['ballot_name'])}
  status: active
"""
            text = text.replace('verification:', cand_block + 'verification:', 1)
            src_block = f"""- url: https://electionhistory.scvotes.gov/contest/{cid}
  note: {q(note)}
  retrieved: '{RETRIEVED}'
"""
        else:
            cand_block = f"""- ballot_name: {cand['ballot_name']}
  contest_id: {cand['contest_id']}
  election_id: {cand['election_id']}
  jurisdiction_id: {cand['jurisdiction_id']}
  office_id: {cand['office_id']}
  party: {party_txt}
  status: active
"""
            idx = text.index('\nid: ')
            text = text[:idx] + '\n' + cand_block.rstrip('\n') + text[idx:]
            src_block = f"""- note: {q(note)}
  retrieved: '{RETRIEVED}'
  url: https://electionhistory.scvotes.gov/contest/{cid}
"""
        # Append the source entry to the file's sources list — i.e. BEFORE a
        # trailing 'verification:' mapping when one is present. (Appending at
        # EOF after 'verification:' corrupts county-pass files; that bug in
        # the first fan-out run was repaired by ~/workspace/sc177/repair_merges.py.)
        if '\nverification:' in text:
            vi = text.index('\nverification:')
            text = text[:vi] + '\n' + src_block.rstrip('\n') + text[vi:] + (
                '' if text.endswith('\n') else '\n')
        else:
            text = text.rstrip('\n') + '\n' + src_block
        path.write_text(text)
        if str(path) not in merged_done:
            merged_done.add(str(path))
            drep_by_slug[dslug]['people_merged'] += 1
            report['totals']['people_merged_files'] += 1

    # ---- election file appends (textual, before top-level 'sources:')
    for date, blocks in election_appends.items():
        fn = SC / f"elections/sc--{date}--general.yaml"
        text = fn.read_text()
        new_blocks = [b for _, b in sorted(blocks)
                      if b.split('\n')[0].split(': ', 1)[1] not in text]
        if new_blocks:
            marker = '\nsources:\n'
            idx = text.index(marker)
            text = text[:idx] + '\n' + ''.join(new_blocks).rstrip('\n') + text[idx:]
        src_note = (f'School board contests appended by the SC schools fan-out (Civic-Data '
                    f'issue #177): school board contests of the {datename(date)} general '
                    f'election for the elected school districts of South Carolina, from the '
                    f'Election History (ElectionStats) school board data. Write-In rows are '
                    f'unnamed aggregates and seat no one.')
        if src_note not in text:
            text = text.rstrip('\n') + f"""
- url: https://electionhistory.scvotes.gov/
  note: {q(src_note)}
  retrieved: '{RETRIEVED}'
"""
        fn.write_text(text)

    report['totals'] = dict(report['totals'])
    out = Path.home() / 'workspace/sc177/schools_fanout_report.json'
    out.write_text(json.dumps(report, indent=1, default=str))
    print(json.dumps({k: report[k] for k in ('totals',)}, indent=1, default=str))
    print('districts:', len(report['districts']))
    for k in ('unmapped', 'check_failures', 'ties', 'party_anomalies', 'zero_candidate',
              'seats_exceed', 'succession_unknown', 'possible_duplicates'):
        print(k, len(report[k]))


if __name__ == '__main__':
    main()
