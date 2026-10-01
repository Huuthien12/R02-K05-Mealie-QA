# DEF-03 — Missing detail resources return undocumented 404

## Baseline and classification

- Mealie: `v3.28.0`, commit `0552eaa4a80031b8572849cca0ed95d07f1be001`.
- Contract: `schema/snapshots/mealie-v3.28.0-openapi.json` (OpenAPI 3.1.0).
- Classification: confirmed reproducible OpenAPI/runtime response-contract defect; **CONFIRMED ROOT CAUSE**.

## Reproduction

With local authenticated access, each request was made three times:

- `GET /api/recipes/0`: 3/3 `404`, body detail reports `No Entry Found`.
- `GET /api/households/mealplans/0`: 3/3 `404`, body detail reports `Not found.`

The snapshot lists `200` and `422` for both operations and does not list `404`. Reproduction rate: 6/6 (100%). Requests are read-only; no resource was created or cleaned up.

## RCA evidence

For recipes, `mealie/routes/recipe/recipe_crud_routes.py` maps `NoEntryFound` to a 404 response before returning the detail resource. For meal plans, `mealie/routes/households/controller_mealplan.py` calls the shared `get_one` mixin; `mealie/routes/_base/mixins.py` explicitly raises a 404 when no item is found. The snapshot response mappings omit 404 for both endpoints. This confirms an intentionally emitted runtime response absent from the published OpenAPI contract.

## Security and references

- Execution was restricted to `localhost:9091`; tokens and headers were not saved.
- Related tests: `tests/schemathesis/test_p0_details.py`.
- Living record: `docs/defects/R02-K05-Mealie-QA-Issue-Defect-Log.md`.
