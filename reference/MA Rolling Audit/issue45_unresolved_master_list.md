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

## 1. Structural seat-count mismatches (post's `seats` value conflicts with
   the real roster — a post-record fix, not a membership-research gap)
| Town / District | Filled | Notes/Reason |
|---|---:|---|
| Uxbridge | 0/5 | Official roster shows 7 members against a `seats: 5` post |
| Bolton (Nashoba Regional) | 0/2 | Named members found during research exceed the post's seat count |
| Lancaster (Nashoba Regional) | 0/3 | 4 named members found against `seats: 3` |
| Tisbury | 0/3 | 4 names found against `seats: 3` — may partly belong to a different (MVYPS-wide) committee |
| Holden (Wachusett Regional) | 0/10 | `seats: 10` looks too high — district is ~16 members across 5 towns; Princeton's mirrored agreement PDF was corrupted, couldn't confirm the real per-town split |

## 2. No working source found (dead links / blocked / 404s)
| Town / District | Filled | Notes/Reason |
|---|---:|---|
| Clinton | 0/5 | 404, no source found across two attempts |
| Sandwich | 0/7 | 404, no source found across two attempts |
| Oak Bluffs | 0/3 | Page 404'd |
| Richmond | 0/5 | Page 404'd |
| Hanson (Regional Vocational seat) | 0/1 | 403s / corrupted PDFs each attempt |
| Hatfield | 0/3 | 403s / corrupted PDFs each attempt |
| Halifax (Elementary) | 0/5 | 403s / corrupted PDFs each attempt |
| Barre (Quabbin Regional) | 0/5 | masscivics/mytowngovernment both bot-blocked; only the chair (David Deschamps) confirmed by name, not minted |
| North Adams | 0/6 | Committee reported mid-turnover, no stable roster to source |

## 3. Still-open partials (genuine remaining seats — not confirmed
   vacancies, which are a resolved state and excluded here)
| Town / District | Filled | Notes/Reason |
|---|---:|---|
| Holbrook | 2/5 | Remaining 3 seats not yet found |
| Sharon | 2/6 | Remaining 4 seats not yet found |
| Warren (Quaboag Regional) | 1/6 | Remaining 5 seats not yet found |
| West Brookfield (Quaboag) | 2/6 | Remaining 4 seats not yet found |
| Deerfield | 1/5 | Remaining 4 seats not yet found |
| Oakham | 1/2 | Remaining 1 seat not yet found |
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

## 4. Identity collisions flagged for human merge review (data is minted;
   this is a data-quality question, not a fill gap)
| Person | Notes/Reason |
|---|---|
| James K. Poore (Attleboro) | Disambiguated as `james-k-poore-attleboro`, separate from an existing `james-k-poore` record elsewhere in the dataset — likely the same person |
| Stephen Bannon (Great Barrington) | Disambiguated as `stephen-bannon-great-barrington`, separate from an existing `stephen-bannon` record |
| Sheila Vaughn (Kingston) | Disambiguated as `sheila-vaughn-kingston`, separate from an existing `sheila-vaughn` record sourced from a general staff/board directory page |
| James B. DuPont (Raynham) | Minted and filled (4/4 Raynham seats complete) — flagged only because he may be the same person as an existing OCPF-sourced record (ran for State Senate, Third Bristol and Plymouth, 2024, which covers Raynham); insufficient confirmation to merge |

## 5. Sourcing conflict between two primary sources (data is minted; flagged
   for a human look, not a fill gap)
| Town / District | Filled | Notes/Reason |
|---|---:|---|
| Wales (Tantasqua Regional) | 1/1 | Town's own directory names Michael Valanzola; Tantasqua's own official committee page names Christine Randall. Minted as Randall (the district's own page is more authoritative for its own committee) but the conflict is unresolved |

## 6. Structural/scope issues requiring restructuring before further minting
| Town / District | Filled | Notes/Reason |
|---|---:|---|
| Holyoke | 3/8 | Ward-based (7 wards + at-large) — needs ward-specific posts before the remaining seats can be minted correctly; same "ward-hybrid" trap as issue #43 |

## 7. Elected-vs-appointed ambiguity (verify, don't infer — data is minted,
   the `how_seated` value is what's in question)
| Town / District | Filled | Notes/Reason |
|---|---:|---|
| Chilmark (Up-Island) | 1/1 | Recorded as elected, but the regional agreement's own Section I(b) is ambiguous on whether this seat is directly elected or Select-Board-appointed. **Update 2026-09-17:** user checked Chilmark's own 2024/2025/2026 Annual Town Election results AND West Tisbury's 2024/2025/2026 results directly — across all 6 documents (3 years × 2 towns) there is no candidate race for any Up-Island Regional School Committee seat, only a couple of unrelated UIRSD budget-override *questions*. This is much stronger evidence for appointment-in-practice than before, but still not a direct confirmation. User has emailed the district superintendent for the actual Up-Island Regional Agreement text (not found online) and is awaiting a reply — do not change `how_seated` until that lands. |

## 8. Seat-to-specific-post assignment unresolved despite having names
| Town / District | Filled | Notes/Reason |
|---|---:|---|
| Aquinnah's own Up-Island seat | 0/1 (was 1/1) | **Update 2026-09-17:** the on-file holder, Marsha Shurrin, has an already-elapsed term (`end: 2026`) and does not appear in chilmarkschool.org's current 4-name roster (Lionette, Manter, Newman, Salop) — her seat looks to have turned over with no identified successor yet. Treat as vacant/unknown rather than still-Shurrin. |
| West Tisbury's own Up-Island seat | 0/1 | chilmarkschool.org's current roster gives 4 names for the district's 5 seats (Lionette confirmed as Chilmark's own); of the remaining 3 (Manter, Newman, Salop), Jeffrey "Skipper" Manter is independently confirmed as a West Tisbury elected official in the same period (won West Tisbury Select Board 2024, West Tisbury Finance Committee 2025) — circumstantial support he holds this seat, not a direct source naming him to it |
| Up-Island at-large seats | 0/2 | Newman and Salop are the 2 remaining known names (assuming Manter is West Tisbury's own rep above), but neither is confirmed to a specific at-large seat vs. the alternative pairing |

## 9. Confirmed out of scope (documented, no further action)
| Town / District | Notes/Reason |
|---|---|
| Boston | Committee's one nominally-elected member is elected only by the student body, not the general public (2022 Home Rule Petition) |
| New Ashford | No seat allocation on the Mount Greylock regional committee, no usable source for its own committee |

## 10. Athol-Royalston — broader dispute, called off in an earlier pass
Contested committee-member identities (Duquette's town assignment
contradicted by the primary 2022 ballot; Newman/Wehmeyer unconfirmed) plus
a dead source document. Royalston's specific 2026 vacancy (section 3 above)
is a separate, newer wrinkle on top of this older dispute. Not tabled with
a seat count since the whole roster is in dispute, not just missing.
