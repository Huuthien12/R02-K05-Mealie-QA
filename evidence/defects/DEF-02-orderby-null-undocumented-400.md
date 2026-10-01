# DEF-02 — `orderBy=null` returns undocumented 400

## Baseline and classification

- Mealie: `v3.28.0`, commit `0552eaa4a80031b8572849cca0ed95d07f1be001`.
- Contract: `schema/snapshots/mealie-v3.28.0-openapi.json` (OpenAPI 3.1.0).
- Classification: confirmed reproducible OpenAPI/runtime response-contract defect; **CONFIRMED ROOT CAUSE**.

## Reproduction

Precondition: local authenticated access to `http://localhost:9091`, with the token used only in process memory. The baseline endpoints all returned `200`:

- `GET /api/households/shopping/lists`
- `GET /api/households/shopping/items`
- `GET /api/households/mealplans`

Each of these was then called three times with `?orderBy=null`:

- `/api/households/shopping/lists?orderBy=null`: 3/3 `400`
- `/api/households/shopping/items?orderBy=null`: 3/3 `400`
- `/api/households/mealplans?orderBy=null`: 3/3 `400`

Actual body was `{"detail":"Invalid order_by statement \"null\": \"null\" is invalid"}`. The corresponding OpenAPI parameters permit `string | null`, while each operation documents only `200` and `422`, not `400`. Reproduction rate: 9/9 (100%). These are read-only requests and require no cleanup.

## RCA evidence

`mealie/repos/repository_generic.py`, `add_order_by_to_query`, treats a non-empty `order_by` string as an order expression. The literal string `null` reaches parsing, which raises a handled `ValueError`; the function explicitly maps that error to `HTTPException(400, "Invalid order_by statement ...")`. The route schema allows nullable input but does not declare that runtime 400 response. This directly establishes the implementation and contract mismatch.

## Security and references

- Only local test endpoints were used; no Authorization value was persisted.
- Related tests: `tests/schemathesis/test_p0_collections.py` and `tests/schemathesis/test_p0_smoke.py`.
- Living record: `docs/defects/R02-K05-Mealie-QA-Issue-Defect-Log.md`.
