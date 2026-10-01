# Phase 5 — Reproducibility and Results Summary

## Baseline and methodology

The project uses Mealie `v3.28.0` at `0552eaa4a80031b8572849cca0ed95d07f1be001`, OpenAPI 3.1.0 snapshot `schema/snapshots/mealie-v3.28.0-openapi.json`, Python 3.11.9, and Schemathesis 4.28.0. The campaign is local-only (`http://localhost:9091`), uses environment-only authentication, bounded schema-derived P0 requests, and directed P1 lifecycle tests with cleanup.

## Completed work and results

- Phase 1: local environment, pinned SUT, snapshot, and QA data prepared.
- Phase 2: system/API analysis, scope, flows, invariants, and scenarios completed.
- Phase 3 P0: 9/9 selected authenticated read-only operations exercised. Collection result: `4 failed, 1 passed`; detail result: `2 failed, 2 passed`. These known detections form DEF-01 to DEF-03.
- Phase 3 P1: normal lifecycle/boundary regression: `9 passed`; separate DEF-04 reproducer intentionally failed against the observed `500`.
- Phase 4: controlled reproductions: DEF-01 3/3, DEF-02 9/9, DEF-03 6/6, DEF-04 3/3; source-backed RCA recorded.

## Consolidation

The inventory is [Test Inventory and Coverage](Test-Inventory-and-Coverage.md); defects are in [Final Defect Summary](Final-Defect-Summary.md). There are 4 confirmed defect families: 2 server-error families (DEF-01, DEF-04) and 2 contract/documentation families (DEF-02, DEF-03). These categories are exclusive for totals; undocumented statuses on the server-error defects are not counted twice.

## Reproducibility assessment

The repository now documents the fresh-clone path, exact dependency installation, SUT baseline/health checks, snapshot loading, safe token setup, P0/P1 commands, known-defect interpretation, cleanup, safety constraints, and evidence locations in [REPRODUCIBILITY.md](../../docs/reproducibility/REPRODUCIBILITY.md). The P0 selection test and `pip check` can run without a token. Authenticated replay requires a locally supplied QA token and must not be attempted anonymously.

## Exclusions, risks, and Phase 6 readiness

Excluded areas remain auth/token/password mutation, admin, backup/maintenance, imports/exports, bulk operations, assets/uploads, streams, external utilities, and public targets. Risks are limited contract coverage outside the selected scope, local environment availability, and DEF-01's RCA limitation without a server stack trace. The project is ready for Phase 6 final reporting/demonstration: evidence and results are consolidated, known failures are distinct from normal regressions, and no SUT change is required for this phase.
