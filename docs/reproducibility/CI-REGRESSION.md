# CI and Regression Operations

Status reviewed: **2026-10-25**.

| Capability | Status | Evidence / limitation |
|---|---|---|
| P0 offline inventory and selection | GITHUB VERIFIED | `P0 contract regression #1` completed successfully for commit `fc4f6b3`; this did not call Mealie. |
| Legacy TC-01..TC-21 offline inventory | STATIC VALIDATED | Workflow is present on `main`; no GitHub run was visible during this review. |
| GitHub-hosted authenticated P0 (TC-01..TC-11) | GITHUB VERIFIED | [Run #2](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/40087491627) completed startup, ephemeral authentication, and all 11 items: 4 PASS, 7 known-defect FAIL, 0 SKIP, 0 ERROR. |
| GitHub-hosted disposable P1 (TC-12..TC-21) | GITHUB VERIFIED | [Run #40154237009](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/40154237009) completed 10 items: 9 PASS, 1 DEF-04 FAIL, 0 SKIP, 0 ERROR. Its four-collection pre/post audit was empty and job-only container/volume teardown completed. |
| GitHub-hosted disposable expansion (TC-22..TC-37) | GITHUB VERIFIED | [Run #40155534891](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/40155534891) completed 16 items: 10 PASS, 6 known-defect FAIL, 0 SKIP, 0 ERROR; its four-collection pre/post audit was empty and job-only teardown completed. |
| Authenticated P0 on self-hosted QA | RETIRED / NOT VERIFIED | The ACER runner was removed because this public repository must not rely on a persistent workstation runner. |
| Legacy self-hosted P1 on disposable QA | RETIRED / NOT VERIFIED | The legacy self-hosted path remains retired; this does not alter the separately verified GitHub-hosted P1 run. |

`IMPLEMENTED` means the configuration exists. `STATIC VALIDATED` means local syntax/inventory checks passed. `GITHUB VERIFIED` requires an actual GitHub Actions run. An offline green job is not evidence that authenticated API tests ran.

## Workflows

### P0 contract regression

[p0-regression.yml](../../.github/workflows/p0-regression.yml) has two jobs:

1. `offline-contract-check` runs on relevant pushes and pull requests on `ubuntu-24.04`. It installs pinned dependencies, collects the repository inventory, checks P0 operation selection, and uploads JUnit evidence.
2. `qa-p0-contract-campaign` runs only after manual dispatch with `run_qa_p0=true`, on the protected Windows runner labels `self-hosted`, `windows`, `mealie-qa`, and with GitHub Environment `qa`.

### GitHub-hosted Mealie P0 regression

[mealie-p0-hosted.yml](../../.github/workflows/mealie-p0-hosted.yml) is the authenticated API campaign for **TC-01..TC-11 only**. It has no `push` or `pull_request` trigger and its sole job is guarded by `github.ref == 'refs/heads/main'`; consequently, an unreviewed pull request cannot start a container with credentials or execute API tests.

The `ubuntu-24.04` job pulls the immutable Linux/amd64 digest selected from `ghcr.io/mealie-recipes/mealie:v3.28.0`, creates a job-unique Docker volume mounted at `/app/data`, and starts Mealie with SQLite and `ALLOW_SIGNUP=true`. It waits, with a finite timeout, for `/api/app/about` and `/openapi.json`, verifies runtime `3.28.0`/`v3.28.0` and OpenAPI `3.1.0`, then removes both container and job-created volume in an `always()` cleanup step.

The job creates a random user/password only in the runner, registers it through the documented snapshot endpoint `POST /api/users/register`, obtains a short-lived bearer token from `POST /api/auth/token`, masks the values, and verifies `GET /api/users/self`. No personal token, DPAPI data, GitHub secret, or credential file is used or retained in an artifact. It then runs the fixed eleven P0 pytest items and writes:

- `reports/ci/hosted-p0.xml` — JUnit evidence for TC-01..TC-11.
- `reports/ci/hosted-p0-summary.txt` — PASS/FAIL/SKIP/ERROR totals shown in the run summary.
- `reports/ci/hosted-p0-metadata.txt` — run SHA, time, image digest/tag, runtime version, API version, and non-sensitive bootstrap statuses.

All artifacts upload even after pytest failures. Known DEF-01..DEF-03 failures remain red; the workflow restores the genuine pytest failure status after collecting evidence. This is P0 read-only only: it never runs TC-12..TC-21 or any P1 write operation.

The digest is immutable deployment evidence for the published `v3.28.0` manifest. It does not independently prove that the published image was built from source commit `0552eaa4a80031b8572849cca0ed95d07f1be001`; the workflow records that expected baseline as metadata and treats source-commit provenance as a documented limitation.

### GitHub-hosted execution evidence — run #2

[GitHub-hosted Mealie P0 regression #2](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/40087491627) ran on `main` commit `b949e09c0a08e21792c80b00a343ae39a4d3c2dc` at `2026-10-24T10:50:40Z`. Its `mealie-hosted-p0-40087491627` artifact records a fresh SQLite volume, successful immutable-image resolution/pull, runtime `v3.28.0`, OpenAPI `3.1.0`, registration `201`, and authenticated self-check `200` before pytest.

| Result | P0 testcase(s) | Interpretation |
|---|---|---|
| PASS | Snapshot selection; meal-plan `today`; shopping-list detail; shopping-item detail | Four items completed without a detected contract failure. |
| FAIL (2 items) | Recipe collection fuzz and recipe smoke | DEF-01: the same schema-generated `GET /api/recipes` input with empty `foods` returned undocumented `500`; two test items are one defect family, not two new defects. |
| FAIL (3 items) | Shopping-list, shopping-item, and meal-plan collections | DEF-02: `orderBy=null` returned undocumented `400` where the snapshot documents `200`/`422`. |
| FAIL (2 items) | Meal-plan detail `/0` and recipe detail `/0` | DEF-03: nonexistent resources returned undocumented `404` where the snapshot documents `200`/`422`. |

JUnit totals are **4 PASS, 7 FAIL, 0 SKIP, 0 ERROR**. The red workflow conclusion reflects known SUT/API-contract detections, not CI infrastructure: image pull, service startup, bootstrap, bearer authentication, and test execution all completed. The run adds no defect family and does not change the controlled-reproduction counts in the defect log.

### GitHub-hosted P1 regression

[mealie-p1-hosted.yml](../../.github/workflows/mealie-p1-hosted.yml) is a separate, manual TC-12..TC-21 campaign. It is guarded by the default branch and `confirm_disposable_p1=true`; it never runs on `push` or `pull_request`. The workflow uses a job-unique SQLite Docker volume, requires the four P1 resource collections to be empty before the campaign, checks those collections again after pytest, records that evidence, and then removes only the exact job-created container and volume.

The ten historical P1 items retain their existing assertions, including the intentional DEF-04 reproduction. Their `finally` handlers clean tracked resource identifiers; the workflow's fresh-volume teardown provides an additional isolation boundary if a test cleanup path fails. A test or cleanup failure remains a failed job after artifact upload.

[GitHub-hosted Mealie P1 regression #40154237009](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/40154237009) executed the ten historical P1 items against a fresh, job-only SQLite volume. Its `mealie-hosted-p1-40154237009` artifact records release `v3.28.0`, OpenAPI `3.1.0`, successful ephemeral registration/token/self-check (`201`/`200`/`200`), and the following independent P1 result: **9 PASS, 1 FAIL, 0 SKIP, 0 ERROR**.

The only failure was `test_recipe_empty_name_def04_reproduction`: the empty recipe-name request returned HTTP `500` in all three test attempts. This is the already tracked **DEF-04** reproduction. The run conclusion was therefore **FAILURE because pytest correctly preserved DEF-04**, not because of CI setup, Docker startup, bootstrap, authentication, JUnit generation, or artifact upload.

The artifact's pre-campaign and post-campaign audit each report zero Recipes, Shopping Lists, Shopping Items, and Meal Plans. It also records removal of the job-named Docker container and volume. This verifies cleanup only for the audited four collections and the run-owned Docker state; it does not establish general cleanup correctness for resources outside that audit. This one run is execution evidence, not a new controlled-reproduction series, so it does not increase DEF-04's reproduction count. P0's 11-item results and this P1 10-item campaign remain separate evidence sets; they are not presented as a combined 21-test run.

### GitHub-hosted TC-22 through TC-37 expansion

[mealie-tc22-tc37-hosted.yml](../../.github/workflows/mealie-tc22-tc37-hosted.yml) is a separate manual workflow for the sixteen expansion tests only. It runs solely from reviewed `main` code after `confirm_disposable_expansion=true`, creates a job-unique SQLite volume, registers a temporary QA user in the runner, and enables `MEALIE_RUN_P1_EXPANSION=1` only for the pytest step. It rejects non-empty pre/post audits for Recipes, Shopping Lists, Shopping Items, and Meal Plans; uploads JUnit, metadata, collection, and cleanup evidence even when tests fail; and then removes only its exact job-named container and volume.

The workflow deliberately retains any reproduction of the six historical expansion failures associated with DEF-03, DEF-05, DEF-06, and DEF-07. [Run #40155534891](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/40155534891), using workflow commit `ab00ba13a6c809d38b37aa007e8ba349d6dd06f9`, is **GITHUB VERIFIED**: immutable-image resolution/pull, runtime `v3.28.0`, OpenAPI `3.1.0`, temporary registration/token/self-check (`201`/`200`/`200`), all 16 items, and the cleanup evidence completed.

Its JUnit artifact records **10 PASS, 6 FAIL, 0 SKIP, 0 ERROR**. TC-24, TC-25, and TC-28 returned undocumented `404` (DEF-03 extension); TC-31 returned `500` (DEF-05); TC-34 returned `500 ValidationError` (DEF-06); and TC-36 returned undocumented `400` (DEF-07). The red GitHub Actions conclusion is therefore the retained pytest/test verdict, not a Docker startup, bootstrap, authentication, JUnit, artifact, or cleanup failure. Pre- and post-campaign audits each recorded zero Recipes, Shopping Lists, Shopping Items, and Meal Plans; the job-named container and volume were removed. This proves cleanup only for those audited collections and run-owned Docker state.

### GitHub-hosted evidence ledger

These are three independently executed campaigns, not one synthetic 37-item pytest run:

| Campaign | Run | Items | PASS | FAIL | SKIP | ERROR |
|---|---|---:|---:|---:|---:|---:|
| P0 (TC-01..TC-11) | [#40087491627](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/40087491627) | 11 | 4 | 7 | 0 | 0 |
| P1 (TC-12..TC-21) | [#40154237009](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/40154237009) | 10 | 9 | 1 | 0 | 0 |
| Expansion (TC-22..TC-37) | [#40155534891](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/40155534891) | 16 | 10 | 6 | 0 | 0 |
| **Cross-campaign total** | — | **37** | **23** | **14** | **0** | **0** |

The total is an evidence ledger only. It does not replace retained local JUnit files, treat all tests as one shared database campaign, or convert repeated testcase failures into new defect IDs.

### Legacy TC-01 through TC-21 API regression

[legacy-tc01-tc21.yml](../../.github/workflows/legacy-tc01-tc21.yml) keeps the historical suite separate from TC-22..TC-37:

- `legacy-inventory` runs on relevant pushes and pull requests on `ubuntu-24.04`, compiles the legacy modules, requires exactly 21 collected items, and rejects TC-22..TC-37 leakage.
- `legacy-p0` is manual, read-only, and targets TC-01..TC-11 on `mealie-qa`.
- `legacy-p1` is manual and targets TC-12..TC-21 only on `mealie-qa-disposable`. It also requires the dispatch confirmation and protected variable gate.
- `legacy-21-summary` combines P0/P1 JUnit only when both campaigns were requested.

Test failures remain failures. Each API job captures JUnit first and then restores the failed verdict; known DEF-01..DEF-03 behavior is not converted to `xfail` or a false-green result.

## Node 24 action baseline

All third-party actions are pinned to verified 40-character release SHAs:

| Action | Release | SHA | Runtime note |
|---|---|---|---|
| `actions/checkout` | `v7.0.1` | `3d3c42e5aac5ba805825da76410c181273ba90b1` | Node 24; current v7 checkout behavior. |
| `actions/setup-python` | `v7.0.0` | `5fda3b95a4ea91299a34e894583c3862153e4b97` | Node 24; v7 migrated internals to ESM. |
| `actions/upload-artifact` | `v7.0.2` | `cf430e030ddbb5b0abf93d22962f4752f3646cd9` | Node 24 artifact client. |
| `actions/download-artifact` | `v8.0.2` | `9000827ccba6bdab643e8b6fd33ac0654aef8333` | Node 24 artifact client. |

Node 24 actions require Actions Runner `v2.327.1` or later. GitHub-hosted `ubuntu-24.04` runners are managed by GitHub. Before enabling either self-hosted job, verify its installed runner version in **Settings > Actions > Runners** and upgrade it if it is below the minimum. Re-verify the SHAs against official GitHub releases during the next dependency update; do not replace them with moving major tags.

## Protected `qa` environment (legacy self-hosted workflows)

The GitHub-hosted P0 workflow above does **not** use this environment or any secret. The following configuration belongs only to retained legacy self-hosted workflows; do not recreate the removed ACER runner merely to use it.

If those legacy workflows are ever reconsidered, create **Settings > Environments > New environment > `qa`**, then configure:

| Type | Name | Required value / purpose |
|---|---|---|
| Secret | `MEALIE_QA_API_TOKEN` | Dedicated QA service token; never a personal token or DPAPI blob. |
| Variable | `MEALIE_QA_BASE_URL` | `http://localhost:9091` or `http://127.0.0.1:9091` as seen by the runner. |
| Variable | `MEALIE_QA_SOURCE_DIR` | Absolute path to the read-only Mealie source checkout used by the commit gate. |
| Variable | `MEALIE_QA_DISPOSABLE` | `true` only for an independently verified disposable P1 environment. |

Add required reviewers and restrict deployment branches to reviewed branches. Keep `permissions: contents: read`. Environment approval protects secrets, but it does not make a persistent runner clean or safe by itself.

## Self-hosted runner security (retired path)

This repository is publicly readable. GitHub warns that persistent self-hosted runners can be compromised by untrusted pull-request code. Do not install either runner on a primary workstation containing other projects, browser sessions, DPAPI material, SSH keys, cloud credentials, or personal data.

Use a dedicated VM or machine, a non-administrator service account, an allowlisted runner group, outbound access limited to GitHub and the local QA service, and no production credentials only if this retired path is formally approved again. The jobs are manual and do not run on pull requests, but workflow files must still be reviewed before dispatch because they execute repository code.

### P0 runner checklist

1. Create a dedicated Windows QA VM and install the runner from **Settings > Actions > Runners > New self-hosted runner**. Use the short-lived registration command only in the VM console; never store or paste the registration token into the repository or logs.
2. Confirm runner version `>= 2.327.1`, then assign labels `self-hosted`, `windows`, `mealie-qa` and restrict its runner group to this repository.
3. Install Git and Python 3.11; confirm `python --version`, `git --version`, and access to the pinned Mealie source checkout.
4. Run Mealie v3.28.0 locally at port 9091 and verify source commit `0552eaa4a80031b8572849cca0ed95d07f1be001`.
5. Configure the protected `qa` environment, approve the reviewed workflow, and dispatch P0. The current `mealie:dev` image lacks a provenance label, so a matching source checkout is evidence of the configured baseline, not cryptographic proof of the image contents.

### P1 disposable runner checklist

Do not enable P1 until isolation is independently established. `MEALIE_QA_DISPOSABLE=true`, a runner label, or a human checkbox alone is not proof.

Use a separate ephemeral VM and a fresh Mealie database/volume that contains no user or cross-project data. Record the provisioned instance identity and empty baseline, run only TC-12..TC-21, verify test-owned resource cleanup, retain JUnit, then destroy only the resources created for that isolated instance under an approved teardown procedure. Never run `docker compose down -v`, reset a database, or delete a volume based only on its name.

## Dispatch and evidence

After these workflow files reach the default branch (`main`):

1. Open **Actions**, select the workflow, and choose **Run workflow**.
2. For GitHub-hosted P0, select **GitHub-hosted Mealie P0 regression** and select `main`. Its branch guard skips any other branch; it needs no environment approval or secret. Download `mealie-hosted-p0-<run-id>` from **Artifacts** and inspect `hosted-p0.xml` to prove the eleven items ran.
3. For GitHub-hosted P1, select **GitHub-hosted Mealie P1 regression**, select `main`, and set `confirm_disposable_p1=true`. Download `mealie-hosted-p1-<run-id>` and inspect `hosted-p1.xml` plus `hosted-p1-cleanup.txt`; do not treat a red DEF-04/P1 contract result as an infrastructure pass.
4. For the expansion, select **GitHub-hosted Mealie TC-22 to TC-37 regression**, select `main`, and set `confirm_disposable_expansion=true`. Download `mealie-hosted-tc22-tc37-<run-id>` and inspect JUnit plus cleanup evidence; known defects must remain red.
5. The remaining P0/P1 dispatch inputs (`run_qa_p0`, `run_p0`, `run_p1`, and `confirm_disposable_qa`) describe the retained self-hosted workflows, which are not enabled by the GitHub-hosted campaigns.

If the workflow is red because a known defect reproduces, keep the red verdict, attach the JUnit artifact to the defect evidence, compare endpoint/status/schema with the pinned OpenAPI snapshot, and update reproduction counts without duplicating the defect.

## Current integration blockers

- Default branch is `main`; this branch is not merged into it.
- GitHub CLI authentication was invalid during the review, so Environment, runner online state, branch protection, and a Draft PR could not be inspected or changed.
- GitHub-hosted run #1 failed before Mealie startup with Docker exit 125 (`manifest unknown`) because the workflow had `...d06ef7e7...` instead of `...d06ef7a7...`; run #2 verified the correction and retained the expected known-defect verdicts in JUnit.
- The release image digest was resolved from the `v3.28.0` manifest, but release-image-to-source-commit provenance was not independently established.
- P1 and expansion isolation are GitHub-verified only for their audited collections and job-owned Docker resources; no evidence here covers unaudited Mealie resources, authorization boundaries, or production-like shared data.
- The release image digest proves the deployed manifest, not independent source-commit provenance for the pinned Mealie commit.
