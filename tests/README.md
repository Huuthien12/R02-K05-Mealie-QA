# Schemathesis P0 read-only POC

## Baseline and scope

Use only the saved `schema/snapshots/mealie-v3.28.0-openapi.json` contract with local Mealie v3.28.0 (`0552eaa4a80031b8572849cca0ed95d07f1be001`). Do not target a public server.

The selected P0 operations are all authenticated `GET` routes:

- `/api/recipes` and `/api/recipes/{slug}`
- `/api/households/shopping/lists` and `/api/households/shopping/lists/{item_id}`
- `/api/households/shopping/items` and `/api/households/shopping/items/{item_id}`
- `/api/households/mealplans`, `/api/households/mealplans/{item_id}`, and `/api/households/mealplans/today`

P1 writes, recipe lifecycle S6, authentication-negative tests, public/external targets, and destructive operations are excluded.

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

## One-operation smoke command

Provide `MEALIE_API_TOKEN` only through the current shell or another ignored local configuration; do not put it in a command history, a tracked file, or this repository.

```powershell
$env:MEALIE_BASE_URL = 'http://localhost:9091'
New-Item -ItemType Directory -Force evidence/test-runs | Out-Null
.\.venv\Scripts\schemathesis.exe run schema/snapshots/mealie-v3.28.0-openapi.json --url $env:MEALIE_BASE_URL --include-path /api/recipes --include-method GET --phases examples --max-examples 1 --checks not_a_server_error,status_code_conformance,response_schema_conformance --max-failures 1 --request-timeout 10 --rate-limit 10/m --header "Authorization: Bearer $env:MEALIE_API_TOKEN" --report json --report-dir evidence/test-runs
```

This verified CLI syntax limits the first POC to `GET /api/recipes`, uses the `examples` phase and at most one generated case, sends a bearer token only from the environment, and writes a sanitized Schemathesis JSON report to an ignored directory. Repeat the same command with one P0 path at a time only after the smoke is stable.

## Current execution status

The schema load check passes locally. Runtime execution is blocked until Docker/Mealie is restored at `localhost:9091` and a local token is supplied. No unauthenticated request is sent as a fallback.
