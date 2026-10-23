# P0 Regression CI

Status: **IMPLEMENTED NOT VERIFIED**.

The workflow [p0-regression.yml](../../.github/workflows/p0-regression.yml) contains two deliberately separate jobs:

1. `offline-contract-check` runs on every push and pull request. It installs the pinned Python dependencies, collects the 37-item inventory, verifies the offline P0 operation selection, and uploads its JUnit XML.
2. `qa-p0-contract-campaign` runs only through manual dispatch on a protected self-hosted Windows runner labelled `mealie-qa`. It needs the QA environment approval and never runs P1.

## Required GitHub configuration

Configure the protected `qa` environment before manual dispatch:

| Configuration | Purpose |
|---|---|
| Secret `MEALIE_QA_API_TOKEN` | Dedicated disposable-QA API token; never a DPAPI file or personal token |
| Variable `MEALIE_QA_BASE_URL` | `http://localhost:9091` or `http://127.0.0.1:9091` on the self-hosted runner |
| Variable `MEALIE_QA_SOURCE_DIR` | Local Mealie source checkout used for the pinned-commit gate |
| Self-hosted label `mealie-qa` | Runner isolated from real data and able to reach the local QA instance |

The workflow checks the source commit `0552eaa4a80031b8572849cca0ed95d07f1be001`, `/api/app/about`, and `/openapi.json` before running P0. It cannot establish image provenance if `mealie:dev` has no revision label; record that limitation with each campaign.

## Failure policy

P0 currently detects retained defect families DEF-01…DEF-03. The workflow uploads JUnit even when assertions fail, then leaves the job failed. This preserves the contract verdict instead of hiding it with changed assertions or a green-only allowlist.

P1 TC-22…TC-37 is intentionally excluded. It remains a manual run using `Run-MealieQA.ps1 -Mode Expansion -ConfirmDisposableQA` after a human confirms that QA data is disposable.
