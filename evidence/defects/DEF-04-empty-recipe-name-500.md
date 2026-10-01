# DEF-04 — Empty recipe name returns 500

## Baseline and classification

- Mealie: `v3.28.0`, commit `0552eaa4a80031b8572849cca0ed95d07f1be001`.
- Contract: `schema/snapshots/mealie-v3.28.0-openapi.json` (OpenAPI 3.1.0).
- Classification: confirmed reproducible invalid-input server-error defect; **CONFIRMED ROOT CAUSE**.

## Reproduction

- Endpoint: `POST /api/recipes`.
- Preconditions: local Mealie at `http://localhost:9091`; token supplied only at runtime.
- Minimal JSON body: `{"name":""}`.
- OpenAPI responses: `201`, `422`; no `500` is documented.
- Actual result: `500` with detail reporting `Unknown Error` and `AssertionError`.
- Attempts: 3; reproduction rate: 3/3 (100%).

Steps: submit the minimal local authenticated JSON request and repeat twice. No request returned `201`, so no recipe was created and no cleanup was required.

## RCA evidence

`mealie/schema/recipe/recipe.py` defines `CreateRecipe.name` as an unconstrained string, so an empty value passes API-model validation. `mealie/services/recipe/recipe_service.py` sends that name into the recipe model. `mealie/db/models/recipe/recipe.py` validates the model name with `assert name != ""`. `mealie/routes/recipe/recipe_crud_routes.py` maps unhandled exceptions to a 500 response containing the exception class. This source chain explains the observed `AssertionError` and the mismatch with the declared `201`/`422` responses.

## Security and references

- Only the local QA instance was used. No credentials or Authorization header values are recorded.
- The intentional defect regression assertion remains unchanged: `tests/schemathesis/test_p1_recipe_empty_name.py`.
- Living record: `docs/defects/R02-K05-Mealie-QA-Issue-Defect-Log.md`.
