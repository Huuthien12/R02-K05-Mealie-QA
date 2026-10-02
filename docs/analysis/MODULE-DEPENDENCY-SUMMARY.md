# Module / Dependency Summary

| Component | Responsibility / interface | K05 relevance | Evidence |
| --- | --- | --- | --- |
| OpenAPI snapshot | Contract input for operation/parameter/response selection. | Sinh case và status/schema oracle. | `schema/snapshots/`; API analysis. |
| P0 Schemathesis tests | GET-only selected operations through `case.call`/validation. | Bounded schema-based detection. | `tests/schemathesis/test_p0_*`. |
| P1 pytest lifecycle tests | Directed REST requests and cleanup for QA-created resources. | Kiểm tra stateful flow an toàn. | `test_p1_*`; P1 summary. |
| Mealie REST API | Interface for recipes, shopping lists/items, meal plans. | Runtime under test. | system analysis; snapshot. |
| Evidence/defect layer | Summaries, minimal reproduction, RCA classification. | Chuyển test outcome thành claim auditable. | `evidence/defects/`; Phase 4 summary. |

Không cố mô tả toàn bộ Mealie codebase; chỉ liệt kê dependencies trực tiếp của selected test scope.
