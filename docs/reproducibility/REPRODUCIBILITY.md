# Reproducibility Guide

## Purpose and supported baseline

This guide reproduces the bounded R02-K05 QA campaign, not unrestricted fuzzing. It supports Mealie `v3.28.0` at `0552eaa4a80031b8572849cca0ed95d07f1be001`, the saved OpenAPI 3.1.0 snapshot, Python 3.11.9, and Schemathesis 4.28.0. Test only `http://localhost:9091`.

## Fresh clone and prerequisites

Install Git, Docker 29.8.0 with Docker Compose v5.5.1, and Python 3.11.9. Clone the QA repository, then create the isolated test environment:

```powershell
git clone https://github.com/Huuthien12/R02-K05-Mealie-QA.git
Set-Location R02-K05-Mealie-QA
git switch main
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tests/requirements.txt
```

To obtain the SUT, follow [the setup guide](../../setup/SETUP.md): clone Mealie outside this repository (for example `D:\mealie`), detach `v3.28.0`, verify the pinned SHA, then run `docker compose build mealie` and `docker compose up -d` from `D:\mealie\docker`. Do not modify the SUT source or pin a different version.

## Environment and contract checks

```powershell
(Invoke-WebRequest http://localhost:9091/api/app/about -UseBasicParsing).StatusCode
(Invoke-WebRequest http://localhost:9091/openapi.json -UseBasicParsing).StatusCode
Test-Path schema/snapshots/mealie-v3.28.0-openapi.json
.\.venv\Scripts\python.exe -c "import schemathesis; s=schemathesis.openapi.from_path('schema/snapshots/mealie-v3.28.0-openapi.json'); print(type(s).__name__)"
.\.venv\Scripts\python.exe -m pytest tests/schemathesis/test_p0_selection.py -q --capture=no
```

Expected: HTTP `200`, `200`, `True`, `OpenApiSchema`, and `1 passed`. The saved snapshot is the test contract; the runtime schema check establishes availability, not a replacement baseline.

## Safe authentication

Use an authorized local QA token only in the active shell. Never add it to a command file, evidence, report, `.env`, Git history, or an Authorization header example.

```powershell
$env:MEALIE_BASE_URL = 'http://localhost:9091'
$env:MEALIE_API_TOKEN = '<YOUR_LOCAL_QA_TOKEN>'
if (-not $env:MEALIE_API_TOKEN) { throw 'MEALIE_API_TOKEN is required for authenticated tests' }
```

## Campaign commands and interpretation

P0 is authenticated read-only GET testing. It may reproduce DEF-01 through DEF-03; failures are known defect detections, not a harness failure.

```powershell
.\.venv\Scripts\python.exe -m pytest tests/schemathesis/test_p0_smoke.py tests/schemathesis/test_p0_collections.py tests/schemathesis/test_p0_details.py -q
```

P1 normal regression is controlled write testing. It creates only uniquely marked resources and performs cleanup. Run it only in the local QA environment:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/schemathesis/test_p1_shopping_list_lifecycle.py tests/schemathesis/test_p1_shopping_list_boundaries.py tests/schemathesis/test_p1_shopping_item_lifecycle.py tests/schemathesis/test_p1_shopping_item_boundaries.py tests/schemathesis/test_p1_mealplan_lifecycle.py tests/schemathesis/test_p1_mealplan_boundaries.py tests/schemathesis/test_p1_recipe_lifecycle.py -q
```

Historical normal P1 evidence is `9 passed`. Reproduce DEF-04 separately; a failing assertion is expected when the defect remains present:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/schemathesis/test_p1_recipe_empty_name.py -q
```

Do not alter the DEF-04 assertion to accept `500`. Known defect reproducers and their expected outcomes are summarized in [Final Defect Summary](../../reports/summarized/Final-Defect-Summary.md).

## Result categories

| Category | Meaning | Action |
| --- | --- | --- |
| NORMAL TEST PASS | Test completes with its documented expected result and cleanup. | Record as normal regression evidence. |
| KNOWN DEFECT REPRODUCTION | Existing DEF-01 through DEF-04 behavior recurs. | Keep its assertion/evidence; do not relabel as a harness failure. |
| ENVIRONMENT FAILURE | Local SUT, Docker, Python, dependency, or token setup prevents execution. | Check setup, health endpoints, and `pip check`; do not create a SUT defect. |
| TEST-HARNESS FAILURE | Test implementation/assumption fails independently of a supported SUT result. | Triage separately as TEST; preserve SUT defect history. |
| UNEXPECTED NEW FAILURE | A new, repeatable supported result is outside known evidence. | Stop broad expansion, minimize safely, and append the correct log category. |

## Cleanup, boundaries, and troubleshooting

Only P1 tests may write. They must target local QA data, use their generated identifiers, delete child resources before parents, and never modify baseline fixtures. Do not run authentication mutation, administration, backup, import/export, asset/upload, bulk, external, or public-server campaigns.

If Docker is unavailable, restore it using [setup instructions](../../setup/SETUP.md); do not rewrite Docker configuration. If the token is absent, authenticated tests should be skipped or deferred, not run anonymously. If dependency validation fails, recreate `.venv` and reinstall `tests/requirements.txt`. `pip check` and the offline P0 selection test require no token.

## Evidence and success definition

Use [Phase 3 P0](../../reports/summarized/Phase-3-P0-K05-Summary.md), [Phase 3 P1](../../reports/summarized/Phase-3-P1-Lifecycle-Summary.md), [Phase 4](../../reports/summarized/Phase-4-Defect-Evidence-RCA-Summary.md), [defect evidence](../../evidence/defects/), and the [living defect log](../defects/R02-K05-Mealie-QA-Issue-Defect-Log.md) to interpret results.

Reproduction succeeds when the pinned baseline, snapshot, dependencies, local health checks, offline selection test, and intended bounded campaign can be run with results classified using the table above, without persisting credentials or leaving test-created resources.
