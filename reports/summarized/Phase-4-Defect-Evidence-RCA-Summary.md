# Phase 4 — Defect Evidence and RCA Summary

## Scope and safety

Controlled authenticated checks were limited to `http://localhost:9091` on Mealie `v3.28.0` (`0552eaa4a80031b8572849cca0ed95d07f1be001`). The comparison contract was `schema/snapshots/mealie-v3.28.0-openapi.json`. Tokens were supplied at runtime only; no credentials or Authorization headers were saved. No Mealie source was changed.

## Results

| Defect | Controlled result | Reproduction | RCA status |
| --- | --- | --- | --- |
| DEF-01 | `GET /api/recipes?foods=` returned undocumented `500` | 3/3 | LIKELY IMPLEMENTATION PATH |
| DEF-02 | Three `orderBy=null` collection requests returned undocumented `400` | 9/9 | CONFIRMED ROOT CAUSE |
| DEF-03 | Two nonexistent detail resources returned undocumented `404` | 6/6 | CONFIRMED ROOT CAUSE |
| DEF-04 | `POST /api/recipes` with an empty name returned undocumented `500` / `AssertionError` | 3/3 | CONFIRMED ROOT CAUSE |

DEF-01 has a source-supported filter path but lacks a runtime stack trace, so its exact failing expression is not claimed. DEF-02 has a nullable schema parameter that runtime parsing rejects as the string `null`. DEF-03 has deliberate 404 paths omitted from response mappings. DEF-04 accepts the empty API input model, then reaches a persistence assertion and generic 500 handler.

## Validation and disposition

All reproductions used bounded counts and the only state-changing request, DEF-04, returned no `201`; no cleanup was required. Existing intentional defect assertions were not changed. No new defect family was discovered; Phase 4 revalidates DEF-01 through DEF-04 and preserves P0/P1 history. See the four files in `evidence/defects/` and the living defect log for detail.

## Limitations

The snapshot establishes the documented contract, not every intended application behavior. DEF-01 RCA remains limited without a server-side stack trace or database diagnostic. This phase reports evidence and does not patch Mealie.
