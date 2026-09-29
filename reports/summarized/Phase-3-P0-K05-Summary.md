# Phase 3 P0 — K05 Schema-Based API Testing Summary

## Baseline

- SUT: Mealie v3.28.0
- Commit: `0552eaa4a80031b8572849cca0ed95d07f1be001`
- OpenAPI: 3.1.0
- Schemathesis: 4.28.0
- Scope: 9 authenticated read-only GET operations

## Method

OpenAPI snapshot → Schemathesis schema-derived generation → authenticated local requests → invariant/status/schema checks → manual reproduction/minimization → defect-family classification.

Checks:

- `not_a_server_error`
- `status_code_conformance`
- `response_schema_conformance`

## Coverage

**9/9 selected P0 operations were exercised.**

Collection campaign: `4 failed, 1 passed`.

Detail campaign: `2 failed, 2 passed`.

Raw pytest failures were consolidated by root behavior/pattern; they are not counted one-for-one as unique defects.

## Reproducible P0 defect families

### DEF-01 — Empty `foods` query causes server failure

`GET /api/recipes?foods=` → HTTP 500.

Control `GET /api/recipes` → HTTP 200.

OpenAPI documents 200 and 422. Minimal failure reproduced 3/3.

### DEF-02 — `orderBy=null` returns undocumented 400

Affected:

- `GET /api/households/shopping/lists`
- `GET /api/households/shopping/items`
- `GET /api/households/mealplans`

Without `orderBy` → HTTP 200.

With `?orderBy=null` → HTTP 400.

OpenAPI declares `orderBy` as `string | null` and documents responses 200/422, not 400.

Classification: API contract inconsistency / undocumented error response.

### DEF-03 — Nonexistent detail resource returns undocumented 404

Affected minimal requests:

- `GET /api/recipes/0` → 404
- `GET /api/households/mealplans/0` → 404

OpenAPI documents 200/422, not 404.

HTTP 404 itself is reasonable for a missing resource; the finding is the missing 404 response in the API contract.

## Retained out-of-scope candidate

DEF-04: accidental `POST /api/recipes` with `{"name": ""}` returned HTTP 500 / AssertionError during an earlier CLI-filtering issue. It has not yet received controlled P1 triage and is not counted as a confirmed P0 finding.

## Phase conclusion

- Selected P0 operations: 9
- Exercised: 9/9
- Reproducible P0 defect families: 3
- Server-error families: 1
- Contract/status mismatch families: 2
- Out-of-scope candidate retained: 1

**Phase 3 P0 K05 proof of concept is complete for the bounded selected scope.**

This conclusion means the K05 testing pipeline worked and all selected P0 operations were exercised. It does not mean the entire Mealie API has been exhaustively tested.

## Before P1

Preserve evidence, update the testing README, validate repository hygiene, commit the P0 artifacts, and define cleanup/rollback rules before controlled write/lifecycle testing.
