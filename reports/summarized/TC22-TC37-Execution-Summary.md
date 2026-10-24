# TC-22…TC-37 Runtime Execution Summary

## Evidence boundary

Evidence is retained by campaign and is not combined into a synthetic run:

| Evidence session | Inventory | PASS | FAIL | SKIP | ERROR | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| Historical `reports/test-results.xml` | TC-01…TC-21 (21 items) | 13 | 8 | 0 | 0 | Preserved historical evidence. |
| Expansion `tc22-tc37-20261022-164618-697.xml` | TC-22…TC-37 (16 items) | 9 | 7 | 0 | 0 | Pre-TEST-07-fix campaign. |
| Post-fix expansion `tc22-tc37-20261023-215442-705.xml` | TC-22…TC-37 (16 items) | 10 | 6 | 0 | 0 | Current expansion verdict; TC-35 PASS. |
| Current source collection | TC-01…TC-37 (37 items) | N/A | N/A | N/A | N/A | Static inventory verification, not an execution campaign. |

The current expansion JUnit suite started at `2026-10-23T21:54:57.118918+07:00`, completed in 6.738 seconds, and was written at 21:55:03 local time. The paired P0 suite started at `2026-10-23T21:54:44.929716+07:00`, completed in 9.757 seconds, and records 4 PASS / 7 FAIL / 0 SKIP / 0 ERROR.

## Current results by owner and function

| Owner / function | Tests | PASS | FAIL | Test failure rate | SUT/contract failures | Software-observation rate | Finding interpretation |
|---|---:|---:|---:|---:|---:|---:|---|
| Lương Hữu Thiện / Shopping Lists | TC-22…TC-25 | 2 | 2 | 50.00% | 2 | 50.00% | TC-24/25 extend DEF-03. |
| Nguyễn Minh Long / Meal Plans | TC-26…TC-29 | 3 | 1 | 25.00% | 1 | 25.00% | TC-28 extends DEF-03. |
| Hoàng Bình Quân / Shopping Items | TC-30…TC-33 | 3 | 1 | 25.00% | 1 | 25.00% | TC-31 reproduces DEF-05. |
| Nguyễn Hồng Phúc Thọ / Recipes | TC-34…TC-37 | 2 | 2 | 50.00% | 2 | 50.00% | TC-34/36 reproduce DEF-06/07; TC-35 PASS. |

The current raw test failure rate is 6/16 (37.50%). All six failures are SUT or published-contract observations; there is no current harness failure. This is not a “unique defect rate”: the six failed tests map to four defect families because TC-24, TC-25, and TC-28 are all DEF-03.

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
- Authenticated P0 remains manual on the protected self-hosted QA runner and intentionally reports DEF-01…DEF-03 as failures.
- P1 TC-22…TC-37 remains manual and disposable-QA only.
- GitHub Actions offline checks are **GITHUB VERIFIED** after the successful Node 24 workflow run; authenticated P0 and disposable P1 remain **NOT VERIFIED / BLOCKED** until their protected QA runners execute them.
- Runtime source was pinned to Mealie `v3.28.0` / commit `0552eaa4a80031b8572849cca0ed95d07f1be001`; the local `mealie:dev` image has no revision label, so independent image provenance is not established.
