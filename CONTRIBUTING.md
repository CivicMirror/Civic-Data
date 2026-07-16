# Contributing to Civic-Data

There are two kinds of contributors here: **pipelines** (bots) and **people**
(reviewers). Both matter; they do different jobs.

## How data flows

```
scraper / pipeline  →  bot-authored PR  →  CI validation  →  human review  →  merge
```

No one — bot or human — pushes directly to `main`.

## If you're a volunteer reviewer

You're the merge gate. Your job on any PR touching `data/`:

1. **Open the Files Changed tab.** Each entity is one YAML file, so the diff
   is the review. CI has already checked schemas, references, and duplicates —
   you're reviewing *truth*, not syntax.
2. **Check the validation report** in the PR's Checks summary. Pay attention
   to `CROSS[...]` warnings:
   - `name-disagreement` — almost always a data error. Fix or request changes.
   - `winner-not-seated` — the certified election winner isn't in the
     officials directory. Check the municipal website: did someone resign,
     get appointed, or lose a recall? If it's a real event, the fix is
     updating the official record (with a source), not deleting the warning.
   - `no-election-trace` — an "elected" official with no election on record.
     Either the linkage is missing (CivicMirror gap) or `how_seated` is
     miscoded (should be `appointed`/`succeeded`/`acting`).
3. **Verify against the official source.** Every record lists `sources`.
   Open the URL. Names, emails, and phones should match the municipal site
   **verbatim** — we record what governments publish, not what we think they
   meant.
4. **Fix small errors in the PR directly** (suggest a change or push to the
   branch). If something can't be verified, do not merge it — leave a review
   comment and tag a maintainer.
5. **Promote verification status.** If you verified an official record
   against its source, update `verification` to `volunteer-verified` with
   your GitHub handle and today's date. That promotion is the whole point of
   human review.

## If you're a pipeline author

- PRs must be **small and thematic**: one jurisdiction (or one election) per
  PR, not "resync everything."
- Set `verification.status` honestly: `machine-extracted` for scraper/LLM
  output. Never emit `volunteer-verified` from a pipeline.
- Always include `sources` with a `retrieved` date.
- Run `python scripts/validate.py` locally before opening the PR.
- If your PR triggers a `CROSS[...]` warning, say so in the PR description
  and include what you know — reviewers shouldn't have to rediscover it.

## Local setup

```bash
pip install -r scripts/requirements.txt
python scripts/validate.py            # warnings pass, errors fail
python scripts/validate.py --strict   # warnings fail too
```

## Adding a new state

1. Create `data/us/<state>/` with `jurisdictions/`, `officials/`, `elections/`.
2. Start with jurisdiction files — offices are embedded there, and nothing
   else validates until its jurisdiction and office exist.
3. Fill `site_intelligence` even if partial: the CMS platform and results
   vendor fields are how the two projects share scraping knowledge.

## Conventions

- **IDs**: OCD Division IDs for places; `ocd-person/<uuid4>` for people;
  never reuse or recycle an ID.
- **Filenames**: `officials/<jurisdiction>--<name-slug>.yaml`,
  `elections/<jurisdiction>--<date>--<office-slug>.yaml`.
- **License**: contributions are dedicated to the public domain under
  [CC0 1.0](LICENSE). Don't contribute data you can't dedicate.
