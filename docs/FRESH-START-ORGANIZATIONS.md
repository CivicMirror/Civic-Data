# Fresh-start organization model

Issue #5 intentionally rebuilds the small sample dataset rather than migrating
its old division-shaped jurisdiction IDs. Data loss is acceptable for this
development reset.

Use this order when adding data:

1. Register the geographic `ocd-division/...` and jurisdiction
   `ocd-jurisdiction/.../<classification>` records.
2. Create one immutable `ocd-organization/<uuid>` record for each government
   body.
3. Put CivicPatch and other source IDs in `identifiers[]`.
4. Create Posts for positions and Memberships for people holding them.
5. Run `python3 scripts/validate.py` before committing.

CivicPatch compatibility is explicit: normalize county-qualified Millbury
division IDs, retain `post_id` values as external identifiers, and map labels
such as Chair, Vice Chair, Clerk, and the generic Council Member label to the
formal Select Board Post rather than inventing separate elected offices.
