# DEF-05 — Shopping Item with a valid missing parent returns 500

## Evidence

- Baseline: Mealie `v3.28.0`, commit `0552eaa4a80031b8572849cca0ed95d07f1be001`.
- Contract: `schema/snapshots/mealie-v3.28.0-openapi.json`.
- Test evidence: `reports/local-runs/tc22-tc37-20261022-164618-697.xml` and `reports/local-runs/tc22-tc37-20261023-215442-705.xml`, TC-31.
- Endpoint: `POST /api/households/shopping/items`.
- Preconditions: local QA instance; authenticated request; a generated UUID first checked not to identify an existing Shopping List.
- Minimal request shape: `{"shoppingListId":"<valid-but-missing-uuid>","display":"K05-TC-22-31-missing-parent-<run-id>"}`.

## Expected and actual

The OpenAPI `ShoppingListItemCreate` request requires `shoppingListId`; the supplied UUID satisfies that type. The operation documents only `201` and `422`.

TC-31 received `500 Internal Server Error` in both controlled campaigns. No `201` response was received, so no item identifier was returned and no test-created item required cleanup.

## Classification and RCA status

- Classification: **SUT invalid-reference handling and response-contract defect candidate**.
- Severity / priority proposal: High / High — a schema-valid relational invalid input reached an undocumented server error instead of a client-validation response.
- Reproduction: **2/2 (100%)** across the 2026-10-22 and 2026-10-23 authenticated expansion campaigns.
- RCA: **LIKELY IMPLEMENTATION PATH**. `ShoppingListService.bulk_create_items` queries/creates items using the supplied list ID but the inspected path does not establish a parent-existence validation before persistence. No server stack trace was captured, so the exact database or service exception is not established.

## Security and cleanup

Only `localhost:9091` was used. No token, Authorization value, or generated UUID is persisted in this evidence. The test cleanup loop only deletes IDs returned by a successful create; there was no successful create in this result.
