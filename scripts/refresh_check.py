#!/usr/bin/env python3
"""Refresh check for MA municipal officeholders (issue #116, built for #18 Phase 3).

Reads each town's site_intelligence.officials_directory_url, fetches the page,
and reports whether the currently-recorded officeholders still appear on it.

Read-only: changes no data. Produces a JSON detail log and a Markdown report.
With --open-issue, posts the report as a dated GitHub issue linked to #116.

Usage:
  refresh_check.py [--limit N] [--delay SECS] [--output DIR] [--label "July 2027"]
                   [--open-issue] [--quiet]
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')
TRACKING_ISSUE = 116

GOV_POST_PATTERNS = ('select-board', 'selectmen', 'city-council', 'town-council',
                     '/council', 'board-of-selectman')


def norm(s: str) -> str:
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9 ]', '', s.lower()).strip()


def load_yaml(path):
    import yaml
    with open(path, errors='ignore') as f:
        return yaml.safe_load(f)


def current_holders():
    """jurisdiction_id -> [(person_name, post_id)] for current memberships."""
    people = {}
    for f in glob.glob(f'{REPO}/data/us/ma/people/municipal/*.yaml'):
        d = load_yaml(f)
        if d and d.get('id'):
            people[d['id']] = d.get('name', '')
    org_jur = {}
    for f in glob.glob(f'{REPO}/data/us/ma/organizations/municipal/*.yaml'):
        d = load_yaml(f)
        if d and d.get('id') and d.get('jurisdiction_id'):
            org_jur[d['id']] = d['jurisdiction_id']
    today = date.today().isoformat()[:4]
    holders = defaultdict(list)
    for f in glob.glob(f'{REPO}/data/us/ma/memberships/municipal/*.yaml'):
        oid, pid, end, post = None, None, None, ''
        for line in open(f, errors='ignore'):
            if line.startswith('organization_id:'):
                oid = line.split(':', 1)[1].strip()
            elif line.startswith('person_id:'):
                pid = line.split(':', 1)[1].strip()
            elif line.startswith('post_id:'):
                post = line.split(':', 1)[1].strip()
            elif line.startswith('end:'):
                end = line.split(':', 1)[1].strip().strip("'\"")
        if end and end[:4] < today:
            continue
        jid = org_jur.get(oid)
        name = people.get(pid, '')
        if jid and name:
            holders[jid].append((name, post))
    return holders


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={'User-Agent': UA,
                                               'Accept': 'text/html,*/*'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(2_000_000).decode('utf-8', errors='replace')
            return ('ok', resp.status, body)
    except urllib.error.HTTPError as e:
        try:
            body = e.read(200_000).decode('utf-8', errors='replace')
        except Exception:
            body = ''
        if 'just a moment' in body.lower() or 'cf-chl' in body.lower():
            return ('challenge', e.code, body)
        return ('http_error', e.code, body)
    except Exception as e:
        return ('fetch_error', 0, str(e)[:200])


def check_town(place, url, holders, delay):
    time.sleep(delay)
    status, code, body = fetch(url)
    text = norm(re.sub(r'<[^>]+>', ' ', body)) if status == 'ok' else ''
    is_hub = 'elected' in url.lower() and 'official' in url.lower()
    if is_hub:
        expected = holders
    else:
        expected = [(n, p) for n, p in holders
                    if any(g in p.lower() for g in GOV_POST_PATTERNS)]
        if not expected:
            expected = holders  # fall back rather than check nobody
    found_full, found_last, missing = [], [], []
    for name, _post in expected:
        parts = norm(name).split()
        if not parts:
            continue
        full = ' '.join(parts)
        last = parts[-1]
        if full and full in text:
            found_full.append(name)
        elif len(last) > 2 and re.search(r'\b' + re.escape(last) + r'\b', text):
            found_last.append(name)
        else:
            missing.append(name)
    if status != 'ok':
        verdict = 'page_dead' if status != 'challenge' else 'challenge'
    elif missing:
        verdict = 'holders_missing'
    else:
        verdict = 'current'
    return {'place': place, 'url': url, 'fetch': status, 'http_code': code,
            'verdict': verdict, 'expected': len(expected),
            'found_full': found_full, 'found_last': found_last,
            'missing': missing}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--delay', type=float, default=1.5)
    ap.add_argument('--output', default=os.path.expanduser('~/workspace/issue18/runs'))
    ap.add_argument('--label', default='')
    ap.add_argument('--open-issue', action='store_true')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    holders = current_holders()
    towns = []
    for f in sorted(glob.glob(f'{REPO}/data/us/ma/jurisdictions/municipal/*.yaml')):
        d = load_yaml(f)
        if not d or not d.get('id'):
            continue
        si = d.get('site_intelligence') or {}
        url = si.get('officials_directory_url')
        place = d['id'].split('/place:')[1].split('/')[0]
        towns.append((place, url, holders.get(d['id'], [])))
    if args.limit:
        towns = towns[:args.limit]

    results = []
    for place, url, hs in towns:
        if not url:
            results.append({'place': place, 'url': None, 'verdict': 'no_url',
                            'expected': len(hs)})
            continue
        r = check_town(place, url, hs, args.delay)
        results.append(r)
        if not args.quiet:
            print(f"{r['verdict']:15} {place} ({r['expected']} holders, "
                  f"{len(r['missing'])} missing)", flush=True)

    os.makedirs(args.output, exist_ok=True)
    label = args.label or date.today().strftime('%B %Y')
    slug = re.sub(r'\W+', '-', label.lower()).strip('-')
    json_path = os.path.join(args.output, f'refresh-{slug}.json')
    with open(json_path, 'w') as f:
        json.dump({'label': label, 'generated': date.today().isoformat(),
                   'results': results}, f, indent=1)

    counts = defaultdict(int)
    for r in results:
        counts[r['verdict']] += 1
    lines = [f'# Officeholder refresh check — {label}', '',
             f'Checked {len(results)} municipal jurisdictions '
             f'({date.today().isoformat()}).', '',
             f"- current: {counts['current']}",
             f"- holders missing: {counts['holders_missing']}",
             f"- page dead: {counts['page_dead']}",
             f"- challenge/blocked: {counts['challenge']}",
             f"- no URL on file: {counts['no_url']}", '']
    problems = [r for r in results if r['verdict'] in ('holders_missing', 'page_dead', 'challenge')]
    if problems:
        lines.append('## Needs a look')
        for r in problems:
            if r['verdict'] == 'holders_missing':
                lines.append(f"- **{r['place']}** — holders missing: "
                             f"{', '.join(r['missing'])} ({r['url']})")
            elif r['verdict'] == 'challenge':
                lines.append(f"- **{r['place']}** — blocked by challenge page ({r['url']})")
            else:
                lines.append(f"- **{r['place']}** — page dead "
                             f"({r['fetch']}, {r['url']})")
        lines.append('')
    lines.append(f'Tracking issue: #{TRACKING_ISSUE}. Full per-town detail in the run log.')
    report = '\n'.join(lines)
    md_path = os.path.join(args.output, f'refresh-{slug}.md')
    with open(md_path, 'w') as f:
        f.write(report)
    if not args.quiet:
        print(f'\nwrote {json_path}\nwrote {md_path}')

    if args.open_issue:
        sys.path.insert(0, os.path.expanduser('~/workspace/skills/github/bin'))
        sys.path.insert(0, '/opt/hatch/skills/skill-creator/bin')
        from gh import api_request
        r = api_request('POST', '/repos/CivicMirror/Civic-Data/issues',
                        {'title': f'Officeholder refresh check — {label}',
                         'body': report})
        print('opened issue:', r['number'], r['html_url'])


if __name__ == '__main__':
    main()
