# Issue #45 batch 2 findings (research only, no YAML written)

Retrieved 2026-09-16 unless noted.

## erving-ma/school-committee-member (seats=5, need 1)
Existing on file: Mackensey Bailey, Mark Blatchley, Daniel Hammock, Kelly Sykes.
Official page https://www.erving-ma.gov/231/School-Committee (direct fetch + r.jina.ai confirmation) lists only these same 4 as the local School Committee; Jacquelyn Boyden is listed separately as "Franklin County Technical School Committee Representative" (a different regional post, not this one).
**UNRESOLVED — no 5th name found.** Page shows only 4 local members despite seats=5 on file. Could be a genuine vacancy or a stale seat count; leave open, do not guess.
Source: https://www.erving-ma.gov/231/School-Committee, retrieved 2026-09-16.

## fairhaven-ma/school-committee-member (seats=6, need 3)
Existing on file: Erik Baumann, Donna McKenna, Michael Sherman.
Official page https://www.fairhaven-ma.gov/school-committee (via r.jina.ai, direct fetch 403'd) lists all 6 current members with terms:
Nicole Pacheco (Chair, term expires 2027), Erik Andersen (Vice Chair, term expires 2028), Donna McKenna (term expires 2029), Kelly Ochoa (term expires 2028), Erik Baumann (term expires 2029), Michael Sherman (term expires 2027).
**NEW, ready to mint:** Nicole Pacheco (elected, term-end 2027), Erik Andersen (elected, term-end 2028), Kelly Ochoa (elected, term-end 2028). Fills all 3 open seats.
Source: https://www.fairhaven-ma.gov/school-committee (via r.jina.ai), retrieved 2026-09-16.

## grafton-ma/regional-vocational-school-committee-member (Blackstone Valley Regional Vocational Technical, seats=1, need 1)
Existing on file: none.
Official page https://www.valleytech.k12.ma.us/about/district/schoolcommittee (direct fetch) lists all 13 district members by town; Grafton's is Anthony M. Yitts (Secretary).
**NEW, ready to mint:** Anthony M. Yitts, elected (district-wide, per BVT district structure), no term-end stated. Fills the 1 open seat.
Source: https://www.valleytech.k12.ma.us/about/district/schoolcommittee, retrieved 2026-09-16.

## greenfield-ma/school-committee-member (seats=6, need 6)
Existing on file: none.
Official page https://gpsk12.org/school-committee/ (direct fetch) lists 7 total members "including the Mayor and six elected officials": Stacey Sexton (Chair, term ends 12/31/2027), Ann Childs (Vice Chair, term ends 12/31/2027), M. Mckenzie Webb (Secretary, term ends 12/31/2027), Virginia DeSorgher (Mayor, term ends 12/31/2027), Elizabeth DeNeeve (term ends 12/31/2029), Jeffrey Diteman (term ends 12/31/2029), Melodie Goodwin (term ends 12/31/2029).
Confirmed via data/us/ma/posts/municipal/: Greenfield has separate `greenfield-ma-mayor.yaml`/`greenfield-mayor.yaml` posts, so the Mayor's ex-officio school-committee seat is out of scope for this post -- the remaining 6 elected members exactly fill seats=6.
**NEW, ready to mint (all 6):** Stacey Sexton (elected, term-end 2027), Ann Childs (elected, term-end 2027), M. Mckenzie Webb (elected, term-end 2027), Elizabeth DeNeeve (elected, term-end 2029), Jeffrey Diteman (elected, term-end 2029), Melodie Goodwin (elected, term-end 2029).
Source: https://gpsk12.org/school-committee/, retrieved 2026-09-16.

## hadley-ma/school-committee-member (seats=5, need 3)
Existing on file: Tara Brugger, Ethan Percy.
Official page https://www.hadleyschools.org/district/school-committee (direct fetch) lists all 5 current members: Tara Brugger, Humera Fasihuddin, Ethan Percy, Paul Phifer, Christine Pipczynski.
**NEW, ready to mint:** Humera Fasihuddin, Paul Phifer, Christine Pipczynski. Elected, no term-end stated on page. Fills all 3 open seats.
Source: https://www.hadleyschools.org/district/school-committee, retrieved 2026-09-16.

## hanover-ma/school-committee-member (seats=5, need 1)
Existing on file: Libby Corbo, Ryan Hall, Jaclyn Jorgenson, Pete Miraglia.
Official page https://www.hanover-ma.gov/school-committee (via r.jina.ai, direct fetch 403'd) lists all 5 current members with terms: Pete Miraglia (Chair, term expires May 2029), Ryan Hall (Vice Chair, term expires May 2027), Libby Corbo (term expires May 2027), Jaclyn Jorgenson (term expires May 2029), Christopher Tracy (term expires May 2028).
Note: an initial WebSearch surfaced different names (Ruth Lynch, Kristen Cervantes) with no clear sourcing -- superseded by the direct official-page fetch above, which is internally consistent with the 4 already-on-file names. Treat the WebSearch names as unreliable/stale and disregard.
**NEW, ready to mint:** Christopher Tracy, elected, term-end May 2028. Fills the 1 open seat.
Source: https://www.hanover-ma.gov/school-committee (via r.jina.ai), retrieved 2026-09-16.

## hingham-ma/school-committee-member (seats=6, need 4)
Existing on file: Jennifer A. Benham, Nina Theresa Villanova.
Official page https://www.hinghamschools.org/o/hps/page/school-committee (via r.jina.ai) lists 7 names against a 6-seat post: Jen Benham (Chair, 2025-2027), Michelle Ayer (Vice Chair, 2023-2026), Kerry Ni (Secretary, 2022-2025 -- expired), John Mooney (2024-2027), Tim Dempsey (2024-2027), Nina Villanova (2023-2026), Matt Cosman (2022-2025 -- expired).
A separate WebSearch pass surfaced yet another, partly conflicting set: "Tim Dempsey, Alyson Anderson, Michelle Ayer, Nes Correnti (Chair), Jen Benham (Secretary), Kerry Ni, and Matt Cosman" -- plus news of a March 2026 town election (Benham and Villanova both pulled re-election papers; a "Henry Randolph Buckley" also filed; Ayer reportedly did NOT pull papers for re-election).
**DO NOT MINT — unresolved.** Two of the official page's listed terms (Ni, Cosman) had already expired as of the page's own dates, and a documented March 2026 election likely changed the roster, but no single source gives a clean, current, internally-consistent 6-name list. Needs Hingham town clerk certified election results (same class of gap flagged for Bridgewater-Raynham in batch 1), not scraped school/town pages.
Sources checked: https://www.hinghamschools.org/o/hps/page/school-committee (via r.jina.ai); WebSearch of hinghamschools.org/about/school-committee/, hingham-ma.gov appointments doc, hinghamanchor.com election coverage, southshore.news.

## hinsdale-ma/regional-school-committee-member (Central Berkshire Regional, seats=2, need 1)
Existing on file: Richard Peters.
Official page https://www.cbrsd.org/school-committee/members (direct fetch) lists Hinsdale's 2 representatives: Richard Peters (Chair, term ends 11/2028) and David Stuart (term ends 11/2026).
**NEW, ready to mint:** David Stuart, elected, term-end 11/2026 (i.e. 2026). Fills the 1 open seat.
Source: https://www.cbrsd.org/school-committee/members, retrieved 2026-09-16.

---
## Summary for parent — ready to mint now (high confidence, direct-fetched official sources)
- fairhaven-ma/school-committee-member: Nicole Pacheco (2027), Erik Andersen (2028), Kelly Ochoa (2028) — fills all 3 open seats
- grafton-ma/regional-vocational-school-committee-member: Anthony M. Yitts — fills the 1 open seat
- greenfield-ma/school-committee-member: Stacey Sexton (2027), Ann Childs (2027), M. Mckenzie Webb (2027), Elizabeth DeNeeve (2029), Jeffrey Diteman (2029), Melodie Goodwin (2029) — fills all 6 open seats (Mayor DeSorgher excluded, has own post)
- hadley-ma/school-committee-member: Humera Fasihuddin, Paul Phifer, Christine Pipczynski — fills all 3 open seats
- hanover-ma/school-committee-member: Christopher Tracy (2028) — fills the 1 open seat
- hinsdale-ma/regional-school-committee-member: David Stuart (2026) — fills the 1 open seat

## Do NOT mint — needs more work or is not a gap
- erving-ma/school-committee-member: only 4 names found on official page against seats=5; possible stale seat count or genuine vacancy, not a sourcing failure. Leave open.
- hingham-ma/school-committee-member: conflicting rosters across sources (7 names vs 6 seats, 2 with expired terms, a separate WebSearch turning up different names entirely, and an active March 2026 election cycle). Needs certified town-clerk election results.
