# Kết quả cuối cùng

| Baseline | Giá trị |
| --- | --- |
| SUT | Mealie `v3.28.0` / `0552eaa4a80031b8572849cca0ed95d07f1be001` |
| Contract | OpenAPI 3.1.0; 182 paths; 266 operations |
| Scope | local `http://localhost:9091` only |
| Tooling | Python 3.11.9; Schemathesis 4.28.0 |

| Campaign GitHub-hosted | Items | PASS | FAIL | Ý nghĩa |
| --- | ---: | ---: | ---: | --- |
| P0 (TC-01..TC-11) | 11 | 4 | 7 | Read-only contract detections DEF-01..03. |
| P1 (TC-12..TC-21) | 10 | 9 | 1 | Controlled lifecycle; DEF-04 remains red. |
| Expansion (TC-22..TC-37) | 16 | 10 | 6 | Controlled disposable writes; DEF-03/05/06/07 remain red. |
| **Evidence ledger total** | **37** | **23** | **14** | Three independent disposable campaigns; not one shared-database run. |

| ID | Classification / RCA status | Evidence |
| --- | --- | --- |
| DEF-01 | LIKELY IMPLEMENTATION PATH | `evidence/defects/DEF-01-recipe-empty-foods-500.md` |
| DEF-02 | CONFIRMED ROOT CAUSE | `evidence/defects/DEF-02-orderby-null-undocumented-400.md` |
| DEF-03 | CONFIRMED ROOT CAUSE | `evidence/defects/DEF-03-undocumented-404.md` |
| DEF-04 | CONFIRMED ROOT CAUSE | `evidence/defects/DEF-04-empty-recipe-name-500.md` |
| DEF-05 | SUT invalid-reference handling; LIKELY implementation path | `evidence/defects/DEF-05-shopping-item-missing-parent-500.md` |
| DEF-06 | SUT/contract; exact validator NOT established | `evidence/defects/DEF-06-recipe-partial-put-500.md` |
| DEF-07 | Contract response mismatch; root cause NOT established | `evidence/defects/DEF-07-recipe-whitespace-name-undocumented-400.md` |

Totals: **7 defect families**. The 14 failed items are retained SUT/contract detections, not harness or environment failures. Tested API areas: recipes, shopping lists/items, meal plans. Excluded: auth/token/password, admin, backups, maintenance, import/export, bulk, assets/uploads, streams, webhooks, external utilities and public targets.
