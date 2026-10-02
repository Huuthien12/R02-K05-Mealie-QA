# Submission Checklist

## Trước khi nộp

- [ ] `main` đồng bộ và chứa PR được review.
- [ ] Có setup, snapshot, tests, `tests/requirements.txt`, defect log, evidence và summaries.
- [ ] Có reproducibility guide, `reports/final/`, demo script, outline và defense Q&A.
- [ ] Chạy `pip check`, P0 selection, pytest collection, `git diff --check`, link/secret scan.
- [ ] `.venv`, `__pycache__`, `.schemathesis` và runtime evidence được ignore.
- [ ] Nếu cần screenshot, sanitize trước khi thêm; export report Word/PDF theo template môn học.
- [ ] Archive commit/branch đã review cùng artefact list.

## DO NOT SUBMIT

- `.venv`, caches, temporary files, Docker volume/image data.
- API token thật, JWT, password, `.env`, Authorization header value hoặc local secret.
- Runtime report chưa sanitize, evidence/history bị xóa, hoặc assertion DEF-04 bị sửa để pass.
- Screenshot có credentials hoặc dữ liệu ngoài QA scope.
