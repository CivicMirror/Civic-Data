# Issue #45 batch 5 findings (research only, no YAML written)

Retrieved 2026-09-16 unless noted.

## rehoboth-ma/dighton-rehoboth-regional-school-committee-member (seats=5, need 3)
Existing on file: Lori Beth Lesniak, Aaron Morse.
The Sun Chronicle's April 2026 Rehoboth election coverage (direct fetch) confirms only Morse (3rd term, re-elected) and Lesniak (newly elected) won seats that cycle -- both already on file. It also confirms incumbent Richard Barrett lost his seat ("finished third... did not retain his seat") -- so Barrett is explicitly NOT a current member, ruling him out as a guess.
**UNRESOLVED -- no new names found for the remaining 3 seats.** Direct fetches of rehobothma.gov, town.rehoboth.ma.us, drregional.org/page/school-committee, sc.drregional.org/s_c_contact/full_committee_contact, and a Dighton town-clerk-stamped agenda PDF (dighton-ma.gov, March 2026) all either 403'd, 404'd, or contained no roster/roll-call text. Leave all 3 seats open; needs a working fetch of drregional.org's actual committee page or Rehoboth town clerk election results.

## rochester-ma/old-rochester-regional-school-committee-member (seats=3, need 1)
Existing on file: Damien McCann, Matthew Monteiro.
Official district page https://www.oldrochester.org/district/sc (direct fetch) lists Rochester's 3 representatives (2026-2027 section): Matthew Monteiro (term 2027, already on file), Peter Damien McCann (term 2029, already on file -- matches "Damien McCann"), and Robin Rounseville (appointed for the current school year by Rochester's own school committee).
Note: an earlier WebSearch surfaced a different, older name (Barbara Lee, per a Sippican Week article) for an appointed Rochester vacancy -- superseded by the district's own current 2026-2027 page naming Rounseville instead; treat Lee as stale/replaced.
**NEW, ready to mint:** Robin Rounseville, appointed (current school year), no end date stated. Fills the 1 open seat.
Source: https://www.oldrochester.org/district/sc, retrieved 2026-09-16.

## rowe-ma/school-committee-member (seats=3, need 2)
Existing on file: Matthew Stine.
Official page https://rowe-ma.gov/g/48/School-Committee (direct fetch) lists all 3 current members: Susan Zavotka (Chair, elected, term ends 2029), Patrick Gonder (term ends May 2027), Matt Stine (term ends May 2028, already on file). Page explicitly states "3 of 3 seats" filled.
**NEW, ready to mint:** Susan Zavotka (term-end 2029), Patrick Gonder (term-end 2027). Fills both open seats.
Source: https://rowe-ma.gov/g/48/School-Committee, retrieved 2026-09-16.

## salisbury-ma/triton-regional-school-committee-member-salisbury (seats=3, need 2)
Existing on file: Erin Berger.
Confirmed via a Triton Regional School District member-profile page slug (tritonschools.org/en-US/committee-members-31b11901/erin-berger-salisbury-572e5a17) that Berger is Salisbury's (matches file). FY26 budget PDF names 6 other committee members (Linda Litcofsky, Brian L. Forget, Nerissa Wallen, Paul Myette, Shannon Nolan -- Anna Bates is district curriculum staff, not a committee member) but with no town labels.
**UNRESOLVED -- could not confirm town assignment for the remaining 2 Salisbury seats.** tritonschools.org is bot-protected (Cloudflare-style challenge) on every URL tried, both direct and via r.jina.ai proxy; townofrowley.net's Triton page only covers Rowley. Leave both seats open; needs a working fetch of tritonschools.org's committee-members index or Salisbury's own town site.

## scituate-ma/school-committee-member (seats=5, need 1)
Existing on file: Carey Borkoski, Nicole Brandolini, Maria Fenwick, Janice Lindblom.
No official page fetch succeeded: scituatema.gov/scituate-school-committee 404'd (direct and via r.jina.ai), scituate.k12.ma.us has a DNS failure, scit.org pages not tried directly (blocked search access). WebSearch surfaced Michael Long (Chair) and Peter Gates as possible 5th/additional members, but both are independently dated with EXPIRED terms (Long "2024", Gates "2023") -- the same stale-secondary-source pattern flagged for Hingham in batch 2 (Ni/Cosman). Not reliable enough to mint.
**UNRESOLVED -- leave the 1 open seat open.** Needs a working scit.org fetch or Scituate town clerk election results.

## seekonk-ma/school-committee-member (seats=5, need 4)
Existing on file: Andrew J. Tessier.
Official page https://www.seekonkschools.org/school-committee (direct fetch) lists all 5 current members with terms: Dr. Robert J. Gerardi (Chair, term Apr 2025-Apr 2028), Emily E. Field (Vice Chair, term Apr 2025-Apr 2028), Lisa M. Rizzo (Secretary, term Apr 2024-Apr 2027), Alicia A. MacManus (term Apr 2024-Apr 2027), Andrew J. Tessier (term Apr 2026-Apr 2029, already on file).
**NEW, ready to mint (all 4):** Robert J. Gerardi (term-end 2028), Emily E. Field (term-end 2028), Lisa M. Rizzo (term-end 2027), Alicia A. MacManus (term-end 2027). Fills all 4 open seats.
Source: https://www.seekonkschools.org/school-committee, retrieved 2026-09-16.

## sherborn-ma/dover-sherborn-regional-school-committee-member (seats=4, need 1)
Existing on file: Toa Ashk, Maria Lowder, Angela Johnson.
**NOT A REAL GAP -- stale seat count, same bug class as the Lanesborough/Williamstown Mount Greylock case in batch 3.** The regional agreement (confirmed via WebSearch of the district's own governing document) states the Dover-Sherborn Regional School Committee "shall have three Dover members and three elected Sherborn members" -- 3 per town, not 4. The district's own site (doversherborn.org/school-committee/dover-sherborn-regional-school-committee) directly confirms Sherborn's current 3 representatives are exactly the 3 already on file: Angie Johnson (Vice-Chair, term ends 2029), Mary Lowder (Secretary, term ends 2028), Toa Ashk (term ends 2027).
**DO NOT MINT a 4th person.** Recommend correcting sherborn-ma/dover-sherborn-regional-school-committee-member's `seats` field from 4 to 3 -- the post is already fully and correctly filled at 3/3.
Sources: https://www.doversherborn.org/school-committee/dover-sherborn-regional-school-committee (direct fetch); WebSearch of the D-S regional agreement text. Retrieved 2026-09-16.

## shutesbury-ma/school-committee-member (seats=5, need 3)
Existing on file: Anna Cederberg Heard, Megan Lennon.
Official page https://www.shutesburyschool.org/school_committee/school_committee_members (direct fetch), titled "2026-2027," lists all 5 current members: Leah Jack (Chair), Nathaniel Longcope (Vice Chair), Katrina Catalano, Anna Heard (already on file), Megan Lennon (already on file).
**NEW, ready to mint (all 3):** Leah Jack, Nathaniel Longcope, Katrina Catalano. No individual term-end stated. Fills all 3 open seats.
Source: https://www.shutesburyschool.org/school_committee/school_committee_members, retrieved 2026-09-16.

---
## Summary for parent -- ready to mint now (high confidence, direct-fetched official sources)
- rochester-ma/old-rochester-regional-school-committee-member: Robin Rounseville (appointed) -- fills the 1 open seat
- rowe-ma/school-committee-member: Susan Zavotka (2029), Patrick Gonder (2027) -- fills both open seats
- seekonk-ma/school-committee-member: Robert J. Gerardi (2028), Emily E. Field (2028), Lisa M. Rizzo (2027), Alicia A. MacManus (2027) -- fills all 4 open seats
- shutesbury-ma/school-committee-member: Leah Jack, Nathaniel Longcope, Katrina Catalano -- fills all 3 open seats

## Not a gap -- recommend a data fix instead
- sherborn-ma/dover-sherborn-regional-school-committee-member: post's seats=4 is stale; the regional agreement and district's own site confirm only 3 Sherborn seats exist, and all 3 are already on file. Recommend correcting seats to 3 (post already fully filled, no minting needed).

## Do NOT mint -- needs more work
- rehoboth-ma/dighton-rehoboth-regional-school-committee-member: no new names found for 3 of 5 seats despite multiple source attempts (all blocked/empty); Barrett confirmed NOT a current member (lost re-election).
- salisbury-ma/triton-regional-school-committee-member-salisbury: Berger confirmed, but tritonschools.org is bot-protected on every URL tried; 2 seats' town assignment unconfirmed among 5 other district members.
- scituate-ma/school-committee-member: no working official-page fetch found; only candidate names (Long, Gates) carry expired term dates from secondary sources -- same stale-source pattern as Hingham (batch 2), not reliable enough to mint.
