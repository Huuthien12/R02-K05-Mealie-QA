# BÁO CÁO CUỐI KỲ: R02-K05 Mealie QA

## 1. Trang thông tin đề tài

Đề tài kiểm thử REST API Mealie bằng Schema-Based API Testing / Fuzz Testing. SUT là Mealie `v3.28.0`, commit `0552eaa4a80031b8572849cca0ed95d07f1be001`; tool chính là Schemathesis `4.28.0` trên Python `3.11.9`.

## 2. Tóm tắt

Nhóm xây dựng pipeline từ OpenAPI snapshot đến test design, execution, triage, RCA và reproducibility. Ba campaign GitHub-hosted dùng database disposable độc lập ghi nhận 37 pytest items, 23 PASS, 14 FAIL và 7 defect families; báo cáo không khẳng định full API coverage.

## 3. Giới thiệu

Mealie là hệ thống recipe/meal planning có REST API. Đề tài áp dụng K05 để kiểm tra sự phù hợp giữa runtime và OpenAPI trong phạm vi kiểm soát.

## 4. Mục tiêu

Pin baseline, lưu contract, chọn scope an toàn, dùng oracle có căn cứ, tái hiện finding và tạo artefact tái lập cho báo cáo/demo.

## 5. Phạm vi

Snapshot có OpenAPI 3.1.0, **182 paths và 266 operations**. Campaign chỉ chọn recipe, shopping list/item và meal plan; không suy diễn coverage toàn bộ API.

## 6. Đối tượng kiểm thử – Mealie

Target duy nhất là `http://localhost:9091`. Baseline theo tag/commit, không theo version string runtime có thể là `develop`.

## 7. Cơ sở lý thuyết

API testing kiểm tra request/response. Schema-based testing sinh/kiểm tra theo OpenAPI. Fuzz/property-based testing thăm dò input, đặc biệt input biên. Schemathesis đọc schema, sinh case và áp dụng checks.

## 8. Môi trường và công cụ

Docker `29.8.0`, Docker Compose `v5.5.1`, Python `3.11.9`, Schemathesis `4.28.0`, pytest và snapshot `schema/snapshots/mealie-v3.28.0-openapi.json`. Credentials chỉ ở runtime environment, không nằm trong Git.

## 9. Kiến trúc / API surface

Luồng là snapshot → analysis/scope → invariants/oracles → Schemathesis/pytest → local Mealie → evidence → triage/RCA. GET là P0; POST/PUT/PATCH/DELETE là P1 state-changing candidates.

Kiến trúc, testing boundary và module liên quan được trace trong [SYSTEM-ARCHITECTURE.md](../../docs/architecture/SYSTEM-ARCHITECTURE.md) và [MODULE-DEPENDENCY-SUMMARY.md](../../docs/analysis/MODULE-DEPENDENCY-SUMMARY.md).

## 10. Phương pháp kiểm thử

Oracle kiểm tra documented status, response schema, absence of undocumented 5xx và cleanup của resource test-created. Snapshot không đủ để khẳng định 401/403, ownership, idempotency hay rollback.

## 11. Thiết kế kiểm thử

P0 chọn 9 authenticated GET operations vì liên quan QA data và read-only. P1 dùng directed lifecycle/boundary tests với unique marker, cleanup child trước parent và không broad-fuzz write endpoints.

Các business/data flows thực tế là recipe, shopping list, shopping item và meal plan; sequence/test/evidence nằm tại [BUSINESS-DATA-FLOWS.md](../../docs/architecture/BUSINESS-DATA-FLOWS.md). Ba flow P1 tối thiểu có retained historical evidence được map tại [BUSINESS-FLOW-EVIDENCE.md](BUSINESS-FLOW-EVIDENCE.md).

## 12. P0 – Read-only schema-based campaign

9/9 selected operations đã được thực thi trong evidence lịch sử. Collection có `4 failed, 1 passed`; detail có `2 failed, 2 passed`. Failure là known-defect detection DEF-01–DEF-03, không phải “all passed” hay harness hỏng.

## 13. P1 – Controlled lifecycle/boundary campaign

Campaign P1 historical có 9 PASS và 1 FAIL DEF-04; expansion có 10 PASS và 6 FAIL đã phân loại. Các FAIL được giữ nguyên để phát hiện SUT/contract, không sửa assertion để nhận `500` hay `400`.

## 14. Quy trình triage và reproduction

Triage tách SUT/API-contract defect khỏi ENV/CFG/TEST/OBS. Phase 4 dùng minimal local request, repeat count hữu hạn, và source inspection chỉ để RCA; không sửa Mealie.

## 15. Kết quả kiểm thử

| ID | Observed | Reproduction | Classification | RCA |
| --- | --- | --- | --- | --- |
| DEF-01 | `GET /api/recipes?foods=` → 500 | 3/3 | Server error / undocumented status | LIKELY IMPLEMENTATION PATH |
| DEF-02 | `orderBy=null` trên 3 collections → 400 | 9/9 | Contract/documentation mismatch | CONFIRMED ROOT CAUSE |
| DEF-03 | Missing recipe/meal-plan detail → 404 | 6/6 | Contract/documentation mismatch | CONFIRMED ROOT CAUSE |
| DEF-04 | Empty recipe name → 500 / AssertionError | 3/3 | Input-validation server error | CONFIRMED ROOT CAUSE |
| DEF-05 | Shopping item with missing parent → 500 | 2/2 | Invalid-reference server error | LIKELY implementation path |
| DEF-06 | Partial recipe PUT → 500 / ValidationError | 2/2 | SUT/contract mismatch | Exact validator not established |
| DEF-07 | Whitespace recipe name → undocumented 400 | 2/2 | Contract response mismatch | Root cause not established |

## 16. Phân tích DEF-01

Contract chỉ có `200/422`; runtime trả 500. Source cho thấy đường đi khả dĩ từ `foods` rỗng vào UUID-oriented repository filter, nhưng không có stack trace/database diagnostic; vì vậy RCA không được nâng thành confirmed.

## 17. Phân tích DEF-02

Schema cho `orderBy` nullable và response map `200/422`; runtime parser nhận literal `null` rồi trả 400. Đây là contract/documentation mismatch có confirmed root cause.

## 18. Phân tích DEF-03

404 cho resource không tồn tại là hợp lý. Defect là response 404 do routes phát ra không có trong OpenAPI response mappings; RCA confirmed.

## 19. Phân tích DEF-04

`{"name":""}` qua API input model, thất bại ở persistence assertion và generic handler trả 500 thay vì documented `201/422`; RCA confirmed. Không có resource thành công để cleanup trong reproduction này.

## 20. Tổng hợp defect

Tổng độc quyền là **7 defect families** (DEF-01…DEF-07). **14 FAIL không phải 14 defect**; DEF-03 được tái hiện trên nhiều operation và không được double-count.

## 21. Reproducibility

Phase 5 cung cấp clone/setup/health/snapshot/token-safe/P0/P1/cleanup guide. P5 không chạy authenticated replay mới vì process thiếu token; kết quả chỉ dùng P3/P4 evidence đã xác minh.

Traceability đến yêu cầu bài tập nằm tại [ASSIGNMENT-COMPLIANCE.md](../../docs/compliance/ASSIGNMENT-COMPLIANCE.md). Workflow Git/evidence preservation được mô tả tại [PROJECT-WORKFLOW-EVIDENCE.md](../../docs/project-management/PROJECT-WORKFLOW-EVIDENCE.md); peer evaluation là template trống và phải do nhóm hoàn thành trung thực.

## 22. Giới hạn

Scope bounded, phụ thuộc local runtime/token, không full coverage; DEF-01 không có diagnostic để xác nhận root cause. Route auth/admin/backup/import/export/bulk/upload/stream/webhook/external/public bị loại trừ.

## 23. Bài học / đánh giá kỹ thuật

Snapshot ổn định, lifecycle cleanup và evidence map giúp tránh claim vượt dữ liệu. Known defect regression failure là signal kiểm thử hữu ích, không phải lý do sửa test cho xanh.

## 24. Kết luận

Pipeline P0/P1/expansion/triage/RCA/reproducibility hoàn thành cho scope đã chọn. Ledger chính thức là ba campaign GitHub-hosted độc lập: 11 (4/7), 10 (9/1), và 16 (10/6), tổng 37 items, 23 PASS, 14 FAIL, 0 SKIP, 0 ERROR.

## 25. Hướng phát triển

Cập nhật OpenAPI response maps, chuyển invalid input sang validation có chủ đích, bổ sung diagnostic an toàn cho DEF-01, và chỉ mở rộng scope cùng strategy/cleanup tương ứng.

## 26. Tài liệu tham khảo

`README.md`; `setup/`; `schema/`; `docs/analysis/`; `docs/test-design/`; `docs/reproducibility/`; `reports/summarized/`; defect log và `evidence/defects/`.

## 27. Phụ lục: commands / evidence map

Xem [REPRODUCIBILITY.md](../../docs/reproducibility/REPRODUCIBILITY.md) và [EVIDENCE-MAP.md](EVIDENCE-MAP.md).
