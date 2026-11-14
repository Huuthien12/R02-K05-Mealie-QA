# Kịch bản demo lớp học (8–12 phút)

| Thời lượng | Hành động/trang | Điều trình bày | Fallback |
| --- | --- | --- | --- |
| 0:00–0:45 | `README.md` | Mục tiêu R02-K05, local-only, evidence-based. | README committed. |
| 0:45–1:30 | `setup/SETUP.md`, `schema/README.md` | Baseline v3.28.0/commit, snapshot OpenAPI. | Không cần runtime. |
| 1:30–2:15 | `docs/analysis/api-analysis.md` | 182 paths/266 operations, scope có chủ đích. | Analysis committed. |
| 2:15–3:00 | `test_p0_selection.py` | Chín GET P0 được chọn trước khi request. | Mở P3 summary. |
| 3:00–4:00 | `tests/README.md` | Schemathesis + status/schema/5xx oracles. | Không chạy nếu token không có. |
| 4:00–5:00 | P1 + expansion | P1 `9 PASS / 1 FAIL`; expansion `10 PASS / 6 FAIL`; cleanup audit. | Three independent hosted campaigns, not one run. |
| 5:00–6:15 | DEF-01 evidence | Safe demo bằng evidence: empty foods 500, 3/3. | Đây là fallback chính. |
| 6:15–7:15 | DEF-04 evidence/test | Intentional FAIL là regression detector, không sửa assertion. | Không gửi POST mới. |
| 7:15–8:15 | Phase 4 RCA summary | DEF-02/03 confirmed; DEF-01 likely. | Evidence committed. |
| 8:15–9:15 | Reproducibility guide | Clone/health/token safety/commands/cleanup. | Không hiển thị token. |
| 9:15–10:00 | `FINAL-RESULTS.md` | 37 items; 23 PASS; 14 FAIL; 7 defect families. | Explain SUT vs contract vs harness; do not hide FAIL. |

Chỉ hiển thị health/OpenAPI GET nếu runtime có sẵn; không demo destructive action và không hiển thị credential.
