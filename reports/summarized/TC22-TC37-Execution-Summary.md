# TC-22…TC-37 Runtime Execution Summary

## Evidence boundary

Evidence is retained by campaign and is not combined into a synthetic run:

| Evidence session | Inventory | PASS | FAIL | SKIP | ERROR | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| Historical `reports/test-results.xml` | TC-01…TC-21 (21 items) | 13 | 8 | 0 | 0 | Preserved historical evidence. |
| Expansion `tc22-tc37-20261022-164618-697.xml` | TC-22…TC-37 (16 items) | 9 | 7 | 0 | 0 | Pre-TEST-07-fix campaign. |
| Post-fix expansion `tc22-tc37-20261023-215442-705.xml` | TC-22…TC-37 (16 items) | 10 | 6 | 0 | 0 | Current expansion verdict; TC-35 PASS. |
| GitHub-hosted expansion [#40155534891](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/40155534891) | TC-22…TC-37 (16 items) | 10 | 6 | 0 | 0 | Disposable SQLite; runtime, temporary authentication, four-area cleanup, and teardown verified. |
| Current source collection | TC-01…TC-37 (37 items) | N/A | N/A | N/A | N/A | Static inventory verification, not an execution campaign. |

The local post-fix expansion JUnit suite started at `2026-10-23T21:54:57.118918+07:00`, completed in 6.738 seconds, and was written at 21:55:03 local time. The GitHub-hosted JUnit started at `2026-10-25T02:43:37Z`; its evidence records image pull, runtime `v3.28.0`, OpenAPI `3.1.0`, registration/token/self-check (`201`/`200`/`200`), and job-only cleanup. Both expansion campaigns have the same 10 PASS / 6 FAIL / 0 SKIP / 0 ERROR verdict. The paired local P0 suite records 4 PASS / 7 FAIL / 0 SKIP / 0 ERROR.

### GitHub-hosted campaign ledger

| Campaign | Items | PASS | FAIL | SKIP | ERROR |
|---|---:|---:|---:|---:|---:|
| [P0 #40087491627](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/40087491627) | 11 | 4 | 7 | 0 | 0 |
| [P1 #40154237009](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/40154237009) | 10 | 9 | 1 | 0 | 0 |
| [Expansion #40155534891](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/40155534891) | 16 | 10 | 6 | 0 | 0 |
| **Total across separate campaigns** | **37** | **23** | **14** | **0** | **0** |

These totals are a GitHub-hosted evidence ledger, not a replacement for historical JUnit or a claim that all 37 tests shared one Mealie database campaign.

## Current results by owner and function

| Owner / function | Tests | PASS | FAIL | Test failure rate | SUT/contract failures | Software-observation rate | Finding interpretation |
|---|---:|---:|---:|---:|---:|---:|---|
| Lương Hữu Thiện / Shopping Lists | TC-22…TC-25 | 2 | 2 | 50.00% | 2 | 50.00% | TC-24/25 extend DEF-03. |
| Nguyễn Minh Long / Meal Plans | TC-26…TC-29 | 3 | 1 | 25.00% | 1 | 25.00% | TC-28 extends DEF-03. |
| Hoàng Bình Quân / Shopping Items | TC-30…TC-33 | 3 | 1 | 25.00% | 1 | 25.00% | TC-31 reproduces DEF-05. |
| Nguyễn Hồng Phúc Thọ / Recipes | TC-34…TC-37 | 2 | 2 | 50.00% | 2 | 50.00% | TC-34/36 reproduce DEF-06/07; TC-35 PASS. |

The current raw test failure rate is 6/16 (37.50%) in both the post-fix local and GitHub-hosted campaigns. All six failures are SUT or published-contract observations; there is no current harness failure. This is not a “unique defect rate”: the six failed tests map to four defect families because TC-24, TC-25, and TC-28 are all DEF-03. The red GitHub Actions outcome is the retained pytest verdict, not Docker/bootstrap/authentication/cleanup infrastructure failure.

## Defect and harness mapping

| Tests | Actual | Classification | Severity / priority | Status |
|---|---|---|---|---|
| TC-24, TC-25, TC-28 | Undocumented `404` for missing-resource operations | OpenAPI/runtime contract mismatch; runtime behavior is semantically reasonable | Low / Medium | DEF-03 extension, each operation observed 2/2 across expansion campaigns. |
| TC-31 | `500` for a schema-valid request with a missing Shopping List parent | Server-side invalid-reference handling plus response-contract defect | High / High | DEF-05 reproduced 2/2. |
| TC-34 | `500 ValidationError` for partial Recipe PUT accepted by the published input schema | Server error plus request/response-contract defect | High / High | DEF-06 reproduced 2/2. |
| TC-36 | `400` for whitespace-only Recipe name while the operation documents `201/422` | Contract mismatch; business rejection itself is reasonable | Medium / Medium | DEF-07 reproduced 2/2. |
| TC-35 | PATCH `200`, new slug readable, testcase PASS | Harness regression verification | N/A | TEST-07 FIXED/VERIFIED. |

The paired P0 campaign reconfirms DEF-01…DEF-03: recipe collection paths produced the known `500`, collection `orderBy=null` paths produced undocumented statuses, and nonexistent recipe/meal-plan details produced undocumented `404` responses. It adds no new defect family.

## Cleanup assessment

The post-run authenticated audit scanned all current QA records (3 recipes, 1 Shopping List, 3 Shopping Items, and 1 Meal Plan). It found two recipes matching the exact test-only pattern `K05-TC-35-patched-<8 hex>` and no other `K05-TC-` resources. Both verified test recipes were deleted individually with HTTP 200; a follow-up scan confirmed zero remaining TC-35 markers.

The two leftovers are consistent with the two pre-fix TC-35 campaign executions, but the historical JUnit files do not record generated run IDs, so exact per-run attribution is not established. No non-test data was deleted.

## FS-01 coverage analysis

Coverage is expressed as exercised behavior, not as test count divided by requirement count:

| FS-01 area | Exercised evidence | Remaining boundary |
|---|---|---|
| Shopping Lists | Name boundaries, Unicode round-trip, missing-resource update, repeated delete. | Authorization, pagination and bulk behavior are not established. |
| Meal Plans | Date-range validation, repeated update final state, missing delete, invalid-date preservation. | Cross-user, schedule/import and broader date partitioning remain out of scope. |
| Shopping Items | Quantity update, missing-parent integrity, checked transition and controlled list move. | DEF-05 remains open; bulk and authorization behavior are not covered. |
| Recipes | PUT/PATCH name update, whitespace rejection and 256-character create. | DEF-06/07 remain open; import, assets, sharing and authorization are not covered. |
| Common API quality | Published status maps, bounded round-trips, local-only execution and marker-based cleanup audit. | Docker image provenance and independent cleanup telemetry inside JUnit remain limitations. |

## Regression and CI readiness

- The 37-item inventory, Python compilation, dependency integrity and offline P0 selection are suitable for push/PR regression.
- GitHub-hosted P0, P1, and TC-22…TC-37 expansion execution are each **GITHUB VERIFIED** in their own disposable campaigns. Their evidence ledger totals 37 items, 23 PASS, 14 FAIL, 0 SKIP, 0 ERROR; it is not a single shared-database test run.
- The expansion workflow remains manual and disposable-QA only; the explicit gate prevents P1 writes from running on pushes or pull requests.
- Runtime source was pinned to Mealie `v3.28.0` / commit `0552eaa4a80031b8572849cca0ed95d07f1be001`; the immutable release image digest verifies deployment identity, but independent release-image-to-source-commit provenance is not established.
