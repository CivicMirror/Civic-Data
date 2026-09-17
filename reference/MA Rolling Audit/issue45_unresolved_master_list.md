# Issue #45 — Consolidated unresolved / flagged list

Compiled 2026-09-17, re-verified against current on-file state before
posting (several items from earlier comments turned out to already be
resolved by later batches — Belchertown, Berkley, Brockton, Bridgewater,
Raynham, Attleboro, East Bridgewater, Wendell's seat-count bug, and
Aquinnah's own Up-Island seat are all now complete and excluded below).

**Update 2026-09-17:** Bourne and Charlton resolved with user-supplied
sources (commit `2baf70430`) and removed from section 3 below. Bourne's
Upper Cape Cod Regional Vocational seats (2) came from the district's own
About page. Charlton's Regional School Committee seats (4) came from
Charlton's own certified 2024/2025/2026 election results, which also
corrected a town-attribution error on DCRSD's own website (it mislabels
4 Charlton-elected members as Dudley's).

Posted as a single comment to
https://github.com/CivicMirror/Civic-Data/issues/45 on 2026-09-17
(replacing two earlier separate comments, merged here). This file is the
durable backing copy.

## 1. No working source found (dead links / blocked / 404s)
| Town / District | Filled | Notes/Reason |
|---|---:|---|
| Clinton | 0/5 | 404, no source found across two attempts |
| Sandwich | 0/7 | 404, no source found across two attempts |
| Oak Bluffs | 0/3 | Page 404'd |
| Richmond | 0/5 | Page 404'd |
| Hanson (Regional Vocational seat) | 0/1 | 403s / corrupted PDFs each attempt |
| Hatfield | 0/3 | 403s / corrupted PDFs each attempt |
| Halifax (Elementary) | 0/5 | 403s / corrupted PDFs each attempt |
| Barre (Quabbin Regional) | 0/5 | Seat count now confirmed correct via the district's own regional agreement; masscivics/mytowngovernment both bot-blocked; only the chair (David Deschamps) confirmed by name, not minted |
| New Braintree (Quabbin Regional) | 0/1 | New gap found via the regional agreement -- New Braintree had no Quabbin post at all (only a Pathfinder Regional Vocational post existed); post now created, still needs a name |
| North Adams | 0/6 | Committee reported mid-turnover, no stable roster to source |

## 2. Still-open partials (genuine remaining seats — not confirmed
   vacancies, which are a resolved state and excluded here)
| Town / District | Filled | Notes/Reason |
|---|---:|---|
| West Brookfield (Quaboag) | 5/6 | Confirmed genuine vacancy, not a sourcing gap: West Brookfield's own certified 2024 and 2025 election results show Gregory S. Morse (2024, 3-year term) and Bryan S. Griffing (2025, 3-year term) both won seats that would still technically be running, but neither appears on the district's current roster page -- both have evidently left/resigned, leaving 1 of the 6 seats genuinely open. |
| Blackstone (regional district committee) | 0/4 | Separate Regional Vocational seat is fully filled (1/1); this 4-seat committee has no holders at all |
| Chicopee | 11/12 | 2nd at-large seat ambiguous — district page names a holder who reportedly resigned in 2024, not re-verified |
| Northampton | 0/9 | 8 of 9 seats were named during research (2 at-large + wards 1/2/3/5/6/7) but Ward 4 and whether the Mayor's ex-officio chair counts within the 9 were never nailed down, so nothing was minted |
| Bellingham (local) | 0/5 | WebSearch-derived list produced 6 names, unreconcilable to 5 seats |
| Sunderland (Frontier Regional) | 0/2 | Full 10-person committee roster found, but no per-town labels for the regional seats specifically |
| Whately (Frontier Regional) | 0/1 | Same source/issue as Sunderland above |
| Russell (Gateway Regional) | 0/1 | Seat-count/roster conflict, needs a regional-agreement check |
| Tyringham | 0/5 | Seat-count/roster conflict, needs a regional-agreement check |
| Royalston (Athol-Royalston Regional) | 0/3 | 2026 winner Kiley Hall resigned weeks after the election following a contested 5-4 superintendent-contract vote; seat left vacant pending a replacement/special-election source |
| Sutton (local + Regional Vocational) | 0/5, 0/1 | No confirmable full roster found |
| Waltham | 0/6 | Only fragmentary names from search snippets |
| Ware (local + Pathfinder Regional) | 0/5, 0/2 | Only fragmentary names from search snippets |
| West Boylston | 0/5 | Only fragmentary names from search snippets |
| West Bridgewater | 0/5 | Only fragmentary names from search snippets |
| Westfield | 0/6 | Only fragmentary names from search snippets |
| Wilmington (local + Shawsheen Valley Tech) | 0/7, 0/2 | Only fragmentary names from search snippets |
| Phillipston (Narragansett Regional) | 0/3 | Seat allocation confirmed, no individuals found |

## 3. Identity collisions flagged for human merge review (data is minted;
   this is a data-quality question, not a fill gap)
| Person | Notes/Reason |
|---|---|
| James K. Poore (Attleboro) | Disambiguated as `james-k-poore-attleboro`, separate from an existing `james-k-poore` record elsewhere in the dataset — likely the same person |
| Stephen Bannon (Great Barrington) | Disambiguated as `stephen-bannon-great-barrington`, separate from an existing `stephen-bannon` record |
| Sheila Vaughn (Kingston) | Disambiguated as `sheila-vaughn-kingston`, separate from an existing `sheila-vaughn` record sourced from a general staff/board directory page |
| James B. DuPont (Raynham) | Minted and filled (4/4 Raynham seats complete) — flagged only because he may be the same person as an existing OCPF-sourced record (ran for State Senate, Third Bristol and Plymouth, 2024, which covers Raynham); insufficient confirmation to merge |

## 4. Seat-to-specific-post assignment unresolved despite having names
| Town / District | Filled | Notes/Reason |
|---|---:|---|
| Aquinnah's own Up-Island seat | 0/1 | Chilmark's certified Nov 8, 2022 State Election results confirm Roxane Ackerman won this seat (458 votes, 4-year term), but she doesn't appear on chilmarkschool.org's current roster and the on-file Shurrin (sourced from a 2025 town report, matching term-end year) isn't confirmed either — likely a mid-term vacancy/appointment not yet identified. West Tisbury's own seat and both at-large seats are resolved (Manter, Newman, Salop) via that same certified election. |

## 5. Confirmed out of scope (documented, no further action)
| Town / District | Notes/Reason |
|---|---|
| Boston | Committee's one nominally-elected member is elected only by the student body, not the general public (2022 Home Rule Petition) |
| New Ashford | No seat allocation on the Mount Greylock regional committee, no usable source for its own committee |

## 6. Athol-Royalston — broader dispute, called off in an earlier pass
Contested committee-member identities (Duquette's town assignment
contradicted by the primary 2022 ballot; Newman/Wehmeyer unconfirmed) plus
a dead source document. Royalston's specific 2026 vacancy (section 3 above)
is a separate, newer wrinkle on top of this older dispute. Not tabled with
a seat count since the whole roster is in dispute, not just missing.
