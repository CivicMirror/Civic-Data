# Issue #70 — Tracking Responses to Email (per-town findings)

Town clerk email responses land as comments on
https://github.com/CivicMirror/Civic-Data/issues/70 — this file tracks what
was found/applied per town so a later session doesn't re-derive it.

## Hinsdale (2026-09-17)

Source: https://github.com/CivicMirror/Civic-Data/issues/70#issuecomment-5714381443
— hand-annotated "SAMPLE" ballots (not clean tally sheets) for the May 17,
2025 and May 23, 2026 Annual Town Elections. Submitter flagged these need
care with OCR/transcription; several entries are genuinely ambiguous
handwriting.

### Applied
- **Select Board**: no data changes needed. On-file roster (Gregory, Collins,
  Huntoon) already matches both elections -- Collins confirmed via 2025
  write-in win (40 votes, no one had taken out papers that year), Huntoon
  confirmed via 2026 re-election (77 votes). Added both election results as
  corroborating sources. The 2026 write-in runner-up line reads as "Julie
  Dostie / Monica Newferrett" combined ~4 votes -- doesn't change the
  outcome so left unresolved, but per a Facebook post
  (https://www.facebook.com/groups/233194110200840/posts/3045600722293484/)
  Julie Dostie publicly said she forgot to file papers and would accept
  write-ins; the second name is **Monica Montferret**, Chair of Hinsdale's
  Lake Management Committee -- likely herself, not a data-entry error. Note:
  she is a different person from **Chris Montferret**, the current Planning
  Board Chair (same surname, small-town family, easy to conflate -- don't
  merge these two people).
- **Town Moderator** (was a full gap -- no membership record existed at all):
  added David Stuart, elected/re-elected 2025, 106 votes unopposed. Reused
  his existing `ocd-person` id from his separate Hinsdale Regional School
  Committee record (`hinsdale-ma-regional-school-committee-member-david-stuart.yaml`)
  since it's the same person holding two different elected offices.
- **Tree Warden** (also a full gap): added new person Barry O'Keefe, elected/
  re-elected 2025, 136 votes unopposed.
- **Board of Assessors**: no changes needed -- already fully reconciled in an
  earlier pass (Galliher's file already cites this same 2026 result).
  Mason (2025, 117 votes) and Galliher (2026, 67 votes) account for 2 of 3
  seats; the 3rd (2025 "Assessor - 3 years") shows "no one elected" --
  confirmed genuine vacancy, not a sourcing gap.
- **Finance Committee** (9 seats): no changes needed -- all 9 already on file
  from a June 2026 minutes doc (post-dates the election). The election
  corroborates 6 of the 9: Galeucia + Conner (2025, incl. Conner's write-in
  win), Chivers/Lussier/Rice re-elected + Goddard's write-in win of the
  2-year unexpired seat (2026, 15 votes).

### Flagged, not applied -- needs town confirmation
- **Planning Board** (5 seats, only 3 on file: Harrison, Longdyke,
  Montferret [Chris]): the 2026 ballot shows **William Goddard winning two
  separate unexpired seats by write-in in the same election** -- "4 years
  unexpired" (1 vote) and "3 years unexpired" (1 vote). Checked the town's
  live Planning Board page 2026-09-17: still only lists Montferret (Chair),
  Harrison (Secretary), Longdyke -- no Goddard. A single person can't
  actually occupy two seats on the same 5-member board, so this is either a
  transcription/OCR misread, an uncontested write-in the town hasn't
  processed/sworn in yet, or he accepted only one seat and the other stays
  vacant. **Did not add Goddard to Planning Board data pending clarification.**
  Also unresolved from 2025: "Planning Board - 5 years" and "Planning Board -
  1 year" both read "no one elected" that year -- likely superseded by the
  2026 results above but left as background context.

See also [[ma_issue34_conventions]], [[ma_waf_gated_sites_fetch_technique]].
