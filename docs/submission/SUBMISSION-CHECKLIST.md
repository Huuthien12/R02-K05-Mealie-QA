# Submission Checklist

## Ledger chốt để đối chiếu trước khi nộp

- [ ] Báo đúng ba campaign GitHub-hosted độc lập: P0 11 items (4 PASS/7 FAIL), P1 10 (9 PASS/1 FAIL), expansion 16 (10 PASS/6 FAIL).
- [ ] Báo đúng tổng ledger: **37 items, 23 PASS, 14 FAIL, 0 SKIP, 0 ERROR, 7 defect families**; không gọi đây là một run chung.
- [ ] Giữ FAIL là SUT/contract detection; không đổi expected hoặc `xfail` để làm xanh.
- [ ] Để trống peer evaluation/cá nhân khi chưa có bằng chứng; không tạo review, commit hoặc task giả.

## Trước khi nộp

- [ ] `main` đồng bộ và chứa PR được review.
- [ ] Có setup, snapshot, tests, `tests/requirements.txt`, defect log, evidence và summaries.
- [ ] Có reproducibility guide, `reports/final/`, demo script, outline và defense Q&A.
- [ ] Có architecture diagram, 3–5 business/data flows, evidence cho ít nhất 3 flows và module/dependency explanation.
- [ ] Có project-workflow evidence; peer evaluation template đã được nhóm hoàn thành trung thực.
- [ ] Final Word/PDF và PowerPoint đã export/kiểm tra theo yêu cầu giảng viên.
- [ ] Chạy `pip check`, P0 selection, pytest collection, `git diff --check`, link/secret scan.
- [ ] `.venv`, `__pycache__`, `.schemathesis` và runtime evidence được ignore.
- [ ] Nếu cần screenshot, sanitize trước khi thêm; export report Word/PDF theo template môn học.
- [ ] Archive commit/branch đã review cùng artefact list.

## DO NOT SUBMIT

- `.venv`, caches, temporary files, Docker volume/image data.
- API token thật, JWT, password, `.env`, Authorization header value hoặc local secret.
- Runtime report chưa sanitize, evidence/history bị xóa, hoặc assertion DEF-04 bị sửa để pass.
- Screenshot có credentials hoặc dữ liệu ngoài QA scope.
