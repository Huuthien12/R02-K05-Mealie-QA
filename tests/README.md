# Schemathesis P0 read-only POC

## Baseline and scope

Use only the saved `schema/snapshots/mealie-v3.28.0-openapi.json` contract with local Mealie v3.28.0 (`0552eaa4a80031b8572849cca0ed95d07f1be001`). Do not target a public server.

The selected P0 operations are all authenticated `GET` routes:

- `/api/recipes` and `/api/recipes/{slug}`
- `/api/households/shopping/lists` and `/api/households/shopping/lists/{item_id}`
- `/api/households/shopping/items` and `/api/households/shopping/items/{item_id}`
- `/api/households/mealplans`, `/api/households/mealplans/{item_id}`, and `/api/households/mealplans/today`

P1 writes are opt-in only. They require `MEALIE_API_TOKEN` and `MEALIE_RUN_P1_EXPANSION=1`, and must target a disposable QA database; public/external targets and destructive operations are excluded.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tests/requirements.txt
```

`requirements.txt` is the exact dependency set resolved for Python 3.11.9. `.venv/`, `tests/.env`, and generated reports are ignored by Git.

## Schema-load check

```powershell
.\.venv\Scripts\python.exe -c "import schemathesis; s=schemathesis.openapi.from_path('schema/snapshots/mealie-v3.28.0-openapi.json'); print(type(s).__name__)"
```

Expected output: `OpenApiSchema`. The snapshot's JSON top-level `openapi` value is `3.1.0`.

The offline selection check exercises the installed Schemathesis API without sending a request:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/schemathesis/test_p0_selection.py -q --capture=no
```

## Safe runtime commands

Provide `MEALIE_API_TOKEN` only through the current shell or another ignored local configuration. Use the committed pytest selections below rather than the historical Schemathesis CLI filtering path; the selections hard-code the intended GET-only P0 scope.

```powershell
$env:MEALIE_BASE_URL = 'http://localhost:9091'
$env:MEALIE_API_TOKEN = '<YOUR_LOCAL_QA_TOKEN>'
.\.venv\Scripts\python.exe -m pytest tests/schemathesis/test_p0_smoke.py tests/schemathesis/test_p0_collections.py tests/schemathesis/test_p0_details.py -q
```

For P1 commands, known intentional failures, cleanup rules, and result interpretation, use [the reproducibility guide](../docs/reproducibility/REPRODUCIBILITY.md).

## Current execution status

Official execution evidence is the GitHub-hosted ledger: P0 11 items (4 PASS/7 FAIL), P1 10 (9 PASS/1 FAIL), and TC-22..37 expansion 16 (10 PASS/6 FAIL), for **37 items, 23 PASS, 14 FAIL, 0 SKIP, 0 ERROR and 7 defect families**. These are independent disposable-database campaigns. A new replay requires an authorized disposable target; no unauthenticated fallback is used.
