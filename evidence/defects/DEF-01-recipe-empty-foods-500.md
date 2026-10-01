# DEF-01 — Empty `foods` query returns 500

## Baseline and classification

- Mealie: `v3.28.0`, commit `0552eaa4a80031b8572849cca0ed95d07f1be001`.
- Contract: `schema/snapshots/mealie-v3.28.0-openapi.json` (OpenAPI 3.1.0).
- Classification: confirmed reproducible server-error defect; RCA is **LIKELY IMPLEMENTATION PATH**.

## Reproduction

- Endpoint: `GET /api/recipes?foods=`.
- Preconditions: local Mealie is available at `http://localhost:9091`; an authorized test token is supplied only at runtime.
- Minimal request: authenticated `GET` to the endpoint above. No Authorization value is retained here.
- OpenAPI responses: `200`, `422`; no `500` is documented.
- Actual result: `500 Internal Server Error` with body `Internal Server Error`.
- Attempts: 3; reproduction rate: 3/3 (100%).

Steps: issue the minimal local authenticated request, record its status, and repeat twice. The request is read-only; no cleanup is needed.

## RCA evidence

`mealie/routes/recipe/recipe_crud_routes.py` accepts `foods` as `list[UUID4 | str] | None` and passes it to the recipe repository. `mealie/repos/repository_recipes.py` builds a food filter and passes each supplied value to a UUID-oriented ingredient-food predicate. This establishes a plausible empty-value-to-filter path, but no server stack trace or database exception was captured. The exact failing operation is therefore not established.

## Security and references

- Scope was only `localhost:9091`; no public system was contacted.
- No credentials, tokens, or Authorization header values were saved.
- Related regression selection: `tests/schemathesis/test_p0_smoke.py`.
- Living record: `docs/defects/R02-K05-Mealie-QA-Issue-Defect-Log.md`.
