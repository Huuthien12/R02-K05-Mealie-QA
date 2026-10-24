# CI and Regression Operations

Status reviewed: **2026-10-23**.

| Capability | Status | Evidence / limitation |
|---|---|---|
| P0 offline inventory and selection | GITHUB VERIFIED | `P0 contract regression #1` completed successfully for commit `fc4f6b3`; this did not call Mealie. |
| Legacy TC-01..TC-21 offline inventory | STATIC VALIDATED | Workflow exists on `test/expand-tc22-tc37`; no GitHub run was visible during this review. |
| Authenticated P0 on self-hosted QA | NOT VERIFIED / BLOCKED | No local runner installation or online runner could be verified. |
| Legacy P1 on disposable QA | NOT VERIFIED / BLOCKED | No independently isolated disposable instance or runner could be verified. |

`IMPLEMENTED` means the configuration exists. `STATIC VALIDATED` means local syntax/inventory checks passed. `GITHUB VERIFIED` requires an actual GitHub Actions run. An offline green job is not evidence that authenticated API tests ran.

## Workflows

### P0 contract regression

[p0-regression.yml](../../.github/workflows/p0-regression.yml) has two jobs:

1. `offline-contract-check` runs on relevant pushes and pull requests on `ubuntu-24.04`. It installs pinned dependencies, collects the repository inventory, checks P0 operation selection, and uploads JUnit evidence.
2. `qa-p0-contract-campaign` runs only after manual dispatch with `run_qa_p0=true`, on the protected Windows runner labels `self-hosted`, `windows`, `mealie-qa`, and with GitHub Environment `qa`.

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

## Protected `qa` environment

Create **Settings > Environments > New environment > `qa`**, then configure:

| Type | Name | Required value / purpose |
|---|---|---|
| Secret | `MEALIE_QA_API_TOKEN` | Dedicated QA service token; never a personal token or DPAPI blob. |
| Variable | `MEALIE_QA_BASE_URL` | `http://localhost:9091` or `http://127.0.0.1:9091` as seen by the runner. |
| Variable | `MEALIE_QA_SOURCE_DIR` | Absolute path to the read-only Mealie source checkout used by the commit gate. |
| Variable | `MEALIE_QA_DISPOSABLE` | `true` only for an independently verified disposable P1 environment. |

Add required reviewers and restrict deployment branches to reviewed branches. Keep `permissions: contents: read`. Environment approval protects secrets, but it does not make a persistent runner clean or safe by itself.

## Self-hosted runner security

This repository is publicly readable. GitHub warns that persistent self-hosted runners can be compromised by untrusted pull-request code. Do not install either runner on a primary workstation containing other projects, browser sessions, DPAPI material, SSH keys, cloud credentials, or personal data.

Use a dedicated VM or machine, a non-administrator service account, an allowlisted runner group, outbound access limited to GitHub and the local QA service, and no production credentials. The jobs are manual and do not run on pull requests, but workflow files must still be reviewed before dispatch because they execute repository code.

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
2. Select the reviewed branch. For P0, set `run_qa_p0=true` or `run_p0=true`. For P1, set `run_p1=true` and `confirm_disposable_qa=true` only after the disposable checklist is independently satisfied.
3. Approve the `qa` Environment deployment when prompted.
4. Open the completed run's **Artifacts** section. Download `p0-offline-junit`, `p0-qa-junit`, `legacy-tc01-tc11-p0-*`, `legacy-tc12-tc21-p1-*`, or the combined summary as applicable.

If the workflow is red because a known defect reproduces, keep the red verdict, attach the JUnit artifact to the defect evidence, compare endpoint/status/schema with the pinned OpenAPI snapshot, and update reproduction counts without duplicating the defect.

## Current integration blockers

- Default branch is `main`; this branch is not merged into it.
- GitHub CLI authentication was invalid during the review, so Environment, runner online state, branch protection, and a Draft PR could not be inspected or changed.
- No self-hosted runner installation was detected locally, and no GitHub-side runner version was available for verification.
- P0 and P1 authenticated jobs have not run on GitHub. P1 remains blocked until a disposable environment is demonstrated.
