# Schemathesis POC scenarios

## S1 — anonymous contract-safe smoke

Run only schema-documented public information reads such as `GET /api/app/about`; validate documented `200` response shape. Do not include login/OAuth callbacks, public share-token guessing, or `/api/utils/download`.

## S2 — authenticated read-only contract campaign (P0)

Target the P0 recipe, shopping-list/item and meal-plan `GET` routes in [test-scope.md](test-scope.md). Generate path/query values from the snapshot, validate O1–O4, and set a finite example/case limit. No write method is enabled.

## S3 — validation-boundary probes (P0)

For selected P0 operations, generate invalid query/path/query combinations that the schema permits Schemathesis to exercise. Expected oracle is O3/O4: documented validation outcome when applicable, never 5xx. Do not assert undocumented 404/401/403 behaviour. Authentication-negative cases are not part of this POC.

## S4 — disposable shopping lifecycle (P1, deferred)

Create a prefixed shopping list and item, read/update them, then delete item followed by list. Validate O1, O2, O7 and O8. This is a directed stateful scenario, not unrestricted fuzzing of all household writes.

## S5 — disposable meal-plan lifecycle (P1, deferred)

Create/read/update/delete one prefixed or otherwise identifiable plan entry. Exercise integer `item_id` generation and `CreatePlanEntry`'s required `date`; validate O1, O2, O7 and O8.

## S6 — disposable recipe lifecycle (P1, pending API-verified request)

Use a newly created recipe only. Because the schema gives `Recipe-Input` no required fields, supply a team-approved minimal valid example before automation; do not infer that an empty generated body should be accepted. Retrieve/update/patch/delete only that resource.

## POC exit criteria

- The local target and snapshot version match the Phase 1 baseline.
- Each included operation has an explicit scope class and oracle.
- No credentials, token, baseline fixture, or uncleaned disposable data is retained in Git.
- A report distinguishes contract failure, server 5xx, undocumented response, and environment/authentication failure.
