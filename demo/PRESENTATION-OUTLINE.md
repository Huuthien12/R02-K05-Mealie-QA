# Dàn ý trình chiếu — 14 slide chính + 2 dự phòng

Thời lượng chính dự kiến: **14 phút**; phân công theo chuyên môn, nhóm xác nhận trước khi bảo vệ.

| Slide | Nội dung cần nói | Người trình bày | Bằng chứng cần mở | Thời lượng |
| --- | --- | --- | --- | --- |
| 1 | Đề tài, nhóm và mục tiêu | Long | Trang tiêu đề | 0:30 |
| 2 | Bài toán và phạm vi kiểm thử | Quân | Scope, bốn nhóm chức năng | 1:00 |
| 3 | SUT Mealie v3.28.0 và môi trường | Thiện | Setup, baseline và health check | 1:00 |
| 4 | OpenAPI: 182 paths, 266 operations | Thiện | OpenAPI snapshot | 1:00 |
| 5 | Phân tích hệ thống và bốn luồng nghiệp vụ | Quân | Sơ đồ business/data flows | 1:00 |
| 6 | FS-01: 33 yêu cầu; RTM truy vết tới TC | Thiện | FS-01 và RTM-01 | 1:00 |
| 7 | Test design, contract C và quy tắc nhóm T | Quân | Scenarios, invariants và oracles | 1:00 |
| 8 | Schemathesis và kiểm thử có hướng; 37 pytest items, không phải tất cả do Schemathesis sinh | Thọ | Test inventory và mã kiểm thử | 1:00 |
| 9 | P0: 4 PASS / 7 FAIL; P1: 9 PASS / 1 FAIL | Thọ | Hai campaign P0 và P1 bên dưới | 1:15 |
| 10 | Expansion: 10 PASS / 6 FAIL; tổng 23 PASS / 14 FAIL | Thọ | Campaign Expansion và JUnit | 1:00 |
| 11 | Bảy defect families, phân biệt failure và defect | Long | Defect Log và bảng tổng hợp | 1:15 |
| 12 | RCA và ví dụ DEF-06: PUT trả 500 | Long | Request/response và RCA | 1:15 |
| 13 | Tái lập, kiểm soát dữ liệu và giới hạn phạm vi | Thiện | Reproducibility guide, audit cleanup | 1:00 |
| 14 | Kết luận, giới hạn và hướng phát triển | Long | Final results | 0:45 |
| Dự phòng 1 | Demo luồng kiểm thử trên môi trường QA disposable | Thọ | Workflow và kết quả chạy | Theo thời gian còn lại |
| Dự phòng 2 | Q&A: oracle, defect, phạm vi và phân công | Cả nhóm | RTM, Defect Log, evidence | Theo câu hỏi |

## Ba campaign ngày 27/11/2026

Cùng baseline repository commit `ca4099fa`; các số liệu trên là lịch sử, không dự đoán kết quả chạy mới.

- [P0 — run 45933810815](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/45933810815)
- [P1 — run 45933845930](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/45933845930)
- [Expansion — run 45933852065](https://github.com/Huuthien12/R02-K05-Mealie-QA/actions/runs/45933852065)

Không mặc định mọi 404 là bug: phân biệt hành vi nghiệp vụ và sai lệch contract; không nói P0 all-pass.
