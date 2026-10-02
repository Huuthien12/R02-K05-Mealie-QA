# Kết quả cuối cùng

| Baseline | Giá trị |
| --- | --- |
| SUT | Mealie `v3.28.0` / `0552eaa4a80031b8572849cca0ed95d07f1be001` |
| Contract | OpenAPI 3.1.0; 182 paths; 266 operations |
| Scope | local `http://localhost:9091` only |
| Tooling | Python 3.11.9; Schemathesis 4.28.0 |

| Campaign | Kết quả | Ý nghĩa |
| --- | --- | --- |
| P0 | 9/9 GET historically exercised; collection `4 failed, 1 passed`; detail `2 failed, 2 passed` | Known detections, không all-pass. |
| P1 normal | `9 passed` | Lifecycle/boundary có cleanup. |
| DEF-04 regression | Intentional failing test | Detects observed 500 versus contract. |
| P4 | DEF-01 3/3; DEF-02 9/9; DEF-03 6/6; DEF-04 3/3 | Controlled reproduction. |

| ID | RCA status | Evidence |
| --- | --- | --- |
| DEF-01 | LIKELY IMPLEMENTATION PATH | `evidence/defects/DEF-01-recipe-empty-foods-500.md` |
| DEF-02 | CONFIRMED ROOT CAUSE | `evidence/defects/DEF-02-orderby-null-undocumented-400.md` |
| DEF-03 | CONFIRMED ROOT CAUSE | `evidence/defects/DEF-03-undocumented-404.md` |
| DEF-04 | CONFIRMED ROOT CAUSE | `evidence/defects/DEF-04-empty-recipe-name-500.md` |

Totals: 4 defects; 2 server-error; 2 contract/documentation. Tested API areas: recipes, shopping lists/items, meal plans. Excluded: auth/token/password, admin, backups, maintenance, import/export, bulk, assets/uploads, streams, webhooks, external utilities and public targets.
