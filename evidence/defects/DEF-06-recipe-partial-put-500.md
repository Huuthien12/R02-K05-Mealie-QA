# DEF-06 — Schema-valid partial Recipe PUT returns 500

## Evidence

- Baseline: Mealie `v3.28.0`, commit `0552eaa4a80031b8572849cca0ed95d07f1be001`.
- Contract: `schema/snapshots/mealie-v3.28.0-openapi.json`.
- Test evidence: `reports/local-runs/tc22-tc37-20261022-164618-697.xml` and `reports/local-runs/tc22-tc37-20261023-215442-705.xml`, TC-34.
- Endpoint: `PUT /api/recipes/{slug}` for a recipe created by TC-34.
- Minimal request shape: `{"name":"K05-TC-34-updated-<run-id>"}`.

## Expected and actual

`Recipe-Input` declares no required properties in the snapshot. The PUT operation documents `200` and `422`.

TC-34 received `500` with a response detail identifying `ValidationError` in both controlled campaigns. The test's `finally` cleanup targets the original test-created slug because the PUT did not return a successful replacement.

## Classification and RCA status

- Classification: **SUT error plus OpenAPI request/response-contract defect candidate**.
- Severity / priority proposal: High / High — a request accepted by the published input schema reached an undocumented server error.
- Reproduction: **2/2 (100%)** with a fresh QA recipe in each authenticated campaign.
- RCA: **LIKELY IMPLEMENTATION PATH**. The inspected recipe service treats PUT as a full replacement, while the published `Recipe-Input` exposes no required fields. The exact `ValidationError` source was not captured, so this is not asserted as a confirmed root cause.

## Security and cleanup

Execution was limited to local QA and retained no Authorization data. The test uses a unique recipe name and deletes the original recipe in `finally`; JUnit does not independently prove cleanup completion, so a post-run QA marker check remains required.
