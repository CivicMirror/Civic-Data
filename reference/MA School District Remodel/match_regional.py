#!/usr/bin/env python3
import csv, re, os, yaml, json

REPO = "/data/Projects/Civic/Civic-Data"

def slugify(name):
    s = name.lower().replace(chr(39), '')
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

STOP = {'regional', 'school', 'committee', 'member', 'the', 'of', 'and', 'district', 'technical',
        'vocational', 'county', 'agricultural', 'reg', 'representative'}

def tokens(s):
    return set(w for w in re.findall(r'[a-z]+', s.lower()) if w not in STOP and len(w) > 2)

DONE = {'06030000','06150000','06200000','07120000','06650000','06730000','06950000','07400000','07740000',
        '06000000','06100000','06160000','06180000','06220000','06250000','06450000','06500000','06550000',
        '06700000','06740000','06800000','07100000','07150000','07200000','07300000','07630000','07670000','07780000'}

rows = list(csv.DictReader(open(f'{REPO}/reference/MA School District Remodel/dese_district_town_manifest.csv')))
regional = [r for r in rows if r['town_count'] != '1' and r['dist_code'] not in DONE]

org_dir = f'{REPO}/data/us/ma/organizations/municipal'
org_files = os.listdir(org_dir)
org_name_cache = {}
def get_name(fname):
    if fname not in org_name_cache:
        with open(f'{org_dir}/{fname}') as f:
            text = ''.join(l for l in f if not l.startswith('#'))
        org_name_cache[fname] = yaml.safe_load(text).get('name', '')
    return org_name_cache[fname]

results = []
for r in regional:
    towns = r['towns'].split(';')
    town_tokens = set()
    for t in towns:
        town_tokens |= tokens(t)
    dist_tokens = tokens(r['dist_name']) - town_tokens
    per_town = {}
    for t in towns:
        slug = slugify(t)
        cands = [f for f in org_files if f.startswith(slug + '-ma-')]
        scored = []
        for c in cands:
            name = get_name(c)
            score = len(tokens(name) & dist_tokens) if dist_tokens else 0
            scored.append((score, c, name))
        scored.sort(key=lambda x: -x[0])
        per_town[t] = scored
    results.append({'dist_code': r['dist_code'], 'dist_name': r['dist_name'], 'towns': towns, 'per_town': per_town})

with open(f'{REPO}/reference/MA School District Remodel/regional_matched.json', 'w') as f:
    json.dump(results, f, indent=2)

# Summary: how many districts have a unique top-score match (score>0, not tied) for every town
clean, ambiguous = [], []
for r in results:
    ok = True
    for t, scored in r['per_town'].items():
        if not scored or scored[0][0] == 0:
            ok = False
            break
        if len(scored) > 1 and scored[1][0] == scored[0][0]:
            ok = False
            break
    (clean if ok else ambiguous).append(r)

print(f'{len(clean)} clean (unique top match every town), {len(ambiguous)} ambiguous, out of {len(results)}')
print('\n--- CLEAN ---')
for r in clean:
    print(r['dist_code'], r['dist_name'], len(r['towns']), 'towns')

print('\n--- AMBIGUOUS (need manual review) ---')
for r in ambiguous:
    print(r['dist_code'], r['dist_name'])
