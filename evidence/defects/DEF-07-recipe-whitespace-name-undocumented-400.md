# DEF-07 — Whitespace Recipe name returns undocumented 400

## Evidence

- Baseline: Mealie `v3.28.0`, commit `0552eaa4a80031b8572849cca0ed95d07f1be001`.
- Contract: `schema/snapshots/mealie-v3.28.0-openapi.json`.
- Test evidence: `reports/local-runs/tc22-tc37-20261022-164618-697.xml` and `reports/local-runs/tc22-tc37-20261023-215442-705.xml`, TC-36.
- Endpoint: `POST /api/recipes`.
- Minimal JSON request: `{"name":"   "}`.

## Expected and actual

`CreateRecipe` requires a string `name` but the snapshot does not publish a minimum length or non-whitespace constraint. The operation documents `201` and `422`.

TC-36 received `400` with `Unable to generate recipe slug` in both controlled campaigns. No recipe slug was returned, therefore no test-created recipe required cleanup.

## Classification and RCA status

- Classification: **OpenAPI/runtime response-contract defect candidate**.
- Severity / priority proposal: Medium / Medium — the server rejected invalid business input, but with an undocumented status despite schema acceptance.
- Reproduction: **2/2 (100%)** across the 2026-10-22 and 2026-10-23 authenticated expansion campaigns.
- RCA: **ROOT CAUSE NOT ESTABLISHED**. The response indicates slug generation rejected whitespace; no exact implementation exception or OpenAPI-generation cause was captured.

## Security and cleanup

Only the local QA API was used. No token or Authorization data is retained. Since creation failed, no cleanup was necessary.
