# R02-K05 Mealie QA — Issue & Defect Log

## 1. Thông tin tài liệu

- **Dự án:** R02-K05-Mealie-QA
- **SUT:** Mealie
- **Kỹ thuật kiểm thử:** Schema-Based API / Fuzz Testing
- **Công cụ chính:** Schemathesis, pytest, requests
- **Baseline SUT:** Mealie `v3.28.0`
- **Commit SHA:** `0552eaa4a80031b8572849cca0ed95d07f1be001`
- **Mục đích:** Lưu tập trung các lỗi môi trường, lỗi cấu hình, vấn đề test harness, quan sát về contract và defect của SUT trong suốt dự án.
- **Nguyên tắc:** Không coi lỗi của test code/tooling là defect của Mealie. Chỉ nâng thành defect khi có bằng chứng runtime/contract phù hợp và có thể tái hiện.

---

## 2. Quy ước phân loại

| Mã | Nhóm | Ý nghĩa |
|---|---|---|
| ENV | Environment | Lỗi môi trường chạy, Docker, hệ điều hành |
| CFG | Configuration | Sai URL/cấu hình/baseline |
| TEST | Test Harness / Tooling | Lỗi hoặc giới hạn của code kiểm thử/công cụ |
| OBS | Observation | Hành vi đáng chú ý nhưng chưa đủ cơ sở gọi là defect |
| DEF | SUT Defect | Lỗi/không nhất quán của Mealie hoặc API contract đã có bằng chứng |

Trạng thái sử dụng:

- **RESOLVED:** Đã xử lý.
- **OPEN:** Còn cần xử lý.
- **OBSERVED:** Đã quan sát, chưa phân loại thành defect.
- **CANDIDATE:** Nghi ngờ defect, cần triage/tái hiện.
- **CONFIRMED / REPRODUCIBLE:** Đã tái hiện ổn định trong môi trường kiểm thử hiện tại.

---

# 3. Environment / Configuration Issues

## ENV-01 — Windows CRLF làm shell script trong container không chạy

**Trạng thái:** RESOLVED

### Hiện tượng
Trong quá trình build/run Mealie trên Windows, các shell script như `setup_nltk_data.sh`, `run.sh` hoặc entry script gặp lỗi do line ending CRLF.

### Nguyên nhân
Repository/source được checkout trên Windows với line ending không phù hợp cho shell script chạy trong Linux container.

### Xử lý
Chuẩn hóa line ending và cấu hình Git phù hợp, sau đó rebuild image không dùng cache.

### Kết quả
Mealie chạy thành công và container đạt trạng thái healthy.

### Phân loại
Environment issue, **không phải defect của Mealie API**.

---

## ENV-02 — Docker daemon / named pipe tạm thời không khả dụng

**Trạng thái:** RESOLVED

### Hiện tượng
Docker command không kết nối được daemon/named pipe.

### Xử lý
Khởi động/khôi phục Docker Desktop và xác minh lại Docker daemon.

### Phân loại
Local environment issue.

---

## ENV-03 — Docker config Access Denied

**Trạng thái:** RESOLVED / LOCAL

### Hiện tượng
Có thời điểm thao tác Docker gặp lỗi quyền truy cập cấu hình.

### Phân loại
Local permission issue, không phải SUT defect.

---

## CFG-01 — Sử dụng sai OpenAPI URL

**Trạng thái:** RESOLVED

### Sai
`/api/openapi.json`

Endpoint này trả nội dung frontend HTML, không phải OpenAPI schema.

### Đúng
`/openapi.json`

### Kết quả
Đã lưu snapshot OpenAPI chính xác tại:

`schema/snapshots/mealie-v3.28.0-openapi.json`

---

## CFG-02 — Runtime báo version `develop`

**Trạng thái:** DOCUMENTED

### Hiện tượng
`/api/app/about` báo runtime version là `develop` vì hệ thống được build từ source/image phát triển.

### Baseline kiểm thử chính thức
- Git tag: `v3.28.0`
- Commit: `0552eaa4a80031b8572849cca0ed95d07f1be001`

### Quyết định
Dùng Git tag + commit SHA làm baseline có thể tái lập thay vì chỉ dựa vào runtime version string.

---

# 4. Test Harness / Tooling Issues

## TEST-01 — Process Codex không nhận `MEALIE_API_TOKEN`

**Trạng thái:** RESOLVED / WORKAROUND

### Hiện tượng
Token đã tồn tại trong PowerShell hiện tại nhưng process riêng không nhìn thấy biến môi trường.

### Xử lý
Chạy test trực tiếp trong PowerShell/pytest environment đang chứa `MEALIE_API_TOKEN`.

### Bảo mật
Không lưu token vào Git và không ghi token vào evidence.

---

## TEST-02 — Schemathesis CLI filtering không giới hạn đúng P0 như dự kiến

**Trạng thái:** WORKAROUND APPLIED

### Hiện tượng
Một số thử nghiệm CLI với filter path/method vẫn chọn nhiều operation ngoài P0 và từng thực thi `POST /api/recipes`.

### Xử lý
Dùng Schemathesis Python API `.include()` và selection test để giới hạn chính xác 9 P0 operations.

### Ghi chú
Chưa kết luận đây là bug của Schemathesis vì semantics của CLI filter chưa được xác minh đầy đủ.

---

## TEST-03 — Schemathesis examples phase sinh 0 case

**Trạng thái:** DOCUMENTED

### Hiện tượng
Chạy examples phase không thực thi test case.

### Nguyên nhân quan sát được
OpenAPI snapshot không cung cấp examples phù hợp cho campaign này.

### Phân loại
Tool/schema limitation, không phải SUT defect.

---

## TEST-04 — pytest không nhận `--hypothesis-max-examples=1`

**Trạng thái:** RESOLVED

### Xử lý
Chuyển sang cấu hình Hypothesis trực tiếp:

`@settings(max_examples=1, deadline=None)`

---

## TEST-05 — Shopping Item POST response bị giả định sai cấu trúc

**Trạng thái:** RESOLVED

### Hiện tượng
P1 Shopping Item lifecycle ban đầu giả định response của POST chứa:

`created["id"]`

Dẫn tới `KeyError`.

### Runtime response thực tế
POST trả wrapper gồm:

- `createdItems`
- `updatedItems`
- `deletedItems`

ID của item mới nằm tại:

`created["createdItems"][0]["id"]`

### Xử lý
Test harness được sửa để đọc `createdItems[0]`.

### Ghi chú bổ sung
Trong quá trình chỉnh sửa từng xuất hiện `TabError` do trộn tabs/spaces. Đây là lỗi formatting của test code, không phải defect của SUT.

---

## TEST-06 — Recipe POST response là slug string, không phải recipe object

**Trạng thái:** RESOLVED

### Hiện tượng
P1 Recipe lifecycle ban đầu giả định:

`created.get("slug")`

nhưng `create_response.json()` trả về một chuỗi.

### Runtime response thực tế
Ví dụ:

`"k05-p1-recipe-1328bc78"`

Đây là slug của recipe vừa tạo.

### Xử lý
Test harness dùng trực tiếp JSON string làm `slug`, sau đó GET resource để xác minh `slug` và `name`.

### Kết quả
Recipe lifecycle PASS sau khi sửa harness.

---

# 5. Observations / Contract Limitations

## OBS-01 — Meal Plan có validation liên trường không thể hiện đầy đủ bằng danh sách `required`

**Trạng thái:** OBSERVED

### OpenAPI schema
`CreatePlanEntry` yêu cầu trường `date`.

### Runtime observation
Các payload sau đều trả `422`:

- chỉ có `date`
- `date` + `title=""`
- `date` + `recipeId=null`

Response chứa thông báo:

`Value error, recipe_id=None or title= must be provided`

Trong khi happy-path trước đó với `date` + `title` có nội dung tạo resource thành công (`201`).

### Diễn giải
Runtime áp dụng validation liên trường giữa `recipeId` và `title` mà việc chỉ nhìn vào danh sách `required` của schema không thể hiện đầy đủ.

### Quyết định
Ghi nhận là **contract/schema limitation observation**, chưa nâng thành defect riêng vì API vẫn trả `422`, là status đã được OpenAPI document cho validation failure.

---

# 6. Confirmed SUT Defects

## DEF-01 — Empty `foods` query gây HTTP 500

**Trạng thái:** CONFIRMED / REPRODUCIBLE

### Endpoint
`GET /api/recipes?foods=`

### Actual
HTTP `500`.

### Contract
OpenAPI document các response phù hợp của operation là `200` / `422`.

### Kiểm tra cô lập
Các empty query parameter khác được thử không tạo cùng lỗi; `foods=` là trường hợp gây 500 trong campaign đã thực hiện.

### Reproducibility
Đã tái hiện nhiều lần trong P0.

### Phân loại
- Unexpected server-side failure
- Undocumented HTTP status
- Schema-based/fuzz finding

### Root cause
Chưa xác định trong phạm vi kiểm thử hiện tại.

---

## DEF-02 — `orderBy=null` trả HTTP 400 nhưng OpenAPI không document 400

**Trạng thái:** CONFIRMED / REPRODUCIBLE

### Các endpoint đã tái hiện
- `GET /api/households/shopping/lists?orderBy=null`
- `GET /api/households/shopping/items?orderBy=null`
- `GET /api/households/mealplans?orderBy=null`

### Actual
HTTP `400`.

Response điển hình:

`{"detail":"Invalid order_by statement \"null\": \"null\" is invalid"}`

### Control
Khi bỏ `orderBy`, các collection endpoint tương ứng trả `200`.

### Contract
Schema cho phép `orderBy` ở dạng `string | null`, trong khi operation document response `200` / `422`, không document `400`.

### Phân loại
- API contract inconsistency
- Undocumented HTTP status

### Quyết định grouping
Ba endpoint có cùng pattern được ghi thành **một defect family DEF-02**.

---

## DEF-03 — Nonexistent detail resource trả 404 nhưng OpenAPI không document 404

**Trạng thái:** CONFIRMED / REPRODUCIBLE

### Endpoint đã quan sát
- `GET /api/recipes/0`
- `GET /api/households/mealplans/0`

### Actual
HTTP `404`.

### Contract
Các operation tương ứng chỉ document `200` / `422`.

### Diễn giải
`404 Not Found` là hành vi runtime hợp lý khi resource không tồn tại. Defect ở đây **không phải việc server trả 404**, mà là OpenAPI contract không khai báo response 404 mà client thực tế có thể nhận.

### Phân loại
- API documentation / contract mismatch
- Undocumented response status

### Quyết định grouping
Các detail endpoint có cùng pattern được nhóm thành DEF-03.

---

## DEF-04 — Empty recipe name gây HTTP 500 / `AssertionError`

**Trạng thái:** CONFIRMED / REPRODUCIBLE

### Endpoint
`POST /api/recipes`

### Input
```json
{
  "name": ""
}
```

### Contract
`CreateRecipe` yêu cầu `name` kiểu string.

POST `/api/recipes` document response:

- `201`
- `422`

### Discovery ban đầu
Finding xuất hiện ngoài ý muốn trong quá trình Schemathesis CLI filtering, khi request `{"name": ""}` được gửi và server trả `500`.

Ban đầu defect được giữ ở trạng thái candidate để tránh kết luận từ một lần chạy ngoài P0.

### Controlled reproduction trong P1
Đã chạy test riêng ba lần với cùng payload:

| Attempt | Status | Response |
|---|---:|---|
| 1 | 500 | `Unknown Error`, `AssertionError` |
| 2 | 500 | `Unknown Error`, `AssertionError` |
| 3 | 500 | `Unknown Error`, `AssertionError` |

Kết quả:

`[500, 500, 500]`

### Reproducibility
**3/3 trong controlled reproduction.**

### Actual response
```json
{
  "detail": {
    "message": "Unknown Error",
    "error": true,
    "exception": "AssertionError"
  }
}
```

### Expected contract behavior
Theo responses được OpenAPI document, request phải dẫn tới một status thuộc contract hiện có, ví dụ validation failure `422`, hoặc contract phải document behavior khác. HTTP `500` hiện tại nằm ngoài response contract đã công bố.

### Phân loại
- Unexpected server-side failure
- Undocumented HTTP status
- Input-validation robustness defect
- Schema-based/fuzz finding

### Test behavior
`test_p1_recipe_empty_name.py` **FAILED có chủ đích** vì assertion yêu cầu status thuộc `{201, 422}` nhưng server trả `500`.

Không đổi assertion thành `500` chỉ để test xanh, vì failure này là regression/evidence cho defect.

### Root cause
Chưa thực hiện source-level RCA. Runtime chỉ cho thấy exception `AssertionError`.

---

# 7. Phase 3 P0 Checkpoint

## P0 scope

9 authenticated GET operations:

1. `/api/recipes`
2. `/api/recipes/{slug}`
3. `/api/households/shopping/lists`
4. `/api/households/shopping/lists/{item_id}`
5. `/api/households/shopping/items`
6. `/api/households/shopping/items/{item_id}`
7. `/api/households/mealplans`
8. `/api/households/mealplans/{item_id}`
9. `/api/households/mealplans/today`

### Coverage
Selected: **9**

Exercised: **9/9**

### P0 confirmed defect families
- DEF-01
- DEF-02
- DEF-03

### P0 out-of-scope candidate
- DEF-04, sau đó được controlled reproduction và xác nhận trong P1.

---

# 8. Phase 3 P1 Checkpoint

## P1-A — Shopping List

### Lifecycle
- POST create → PASS
- GET → PASS
- PUT update → PASS
- GET verify → PASS
- DELETE → PASS
- GET after delete → runtime 404

### Boundary
Các payload `{}`, `name=null`, `name=""` đều nằm trong behavior phù hợp với contract quan sát được.

### New defects
0

---

## P1-B — Shopping Item

### Lifecycle
- Tạo parent shopping list tạm
- POST item → PASS
- GET → PASS
- PUT → PASS
- GET verify → PASS
- DELETE item → PASS
- GET after delete → 404
- Cleanup parent → hoàn tất

### Boundary
Campaign PASS theo contract responses `201/422`.

### Harness correction
TEST-05: POST response dùng `createdItems[]`.

### New defects
0

---

## P1-C — Meal Plan

### Lifecycle
- POST → 201
- GET → 200
- PUT → 200
- GET verify → 200
- DELETE → 200
- GET after delete → 404

Result: PASS.

### Boundary
7 boundary cases đã thực thi; tất cả trả `422`, nằm trong documented response set.

Quan sát quan trọng: runtime có cross-field validation giữa `recipeId` và `title` → OBS-01.

### New defects
0

---

## P1-D — Recipe

### Happy-path lifecycle
- POST valid name → 201
- POST response → slug string
- GET by slug → 200
- DELETE → 200
- GET after delete → 404

Result: PASS sau khi sửa TEST-06.

### DEF-04 reproduction
`POST /api/recipes` với `{"name": ""}`:

- Attempt 1 → 500
- Attempt 2 → 500
- Attempt 3 → 500

Result: DEF-04 confirmed/reproducible.

---

# 9. Tổng hợp defect hiện tại

| ID | Mô tả ngắn | Loại | Trạng thái |
|---|---|---|---|
| DEF-01 | `foods=` gây HTTP 500 | Server failure / contract | CONFIRMED |
| DEF-02 | `orderBy=null` gây undocumented 400 | Contract mismatch | CONFIRMED |
| DEF-03 | Missing resource trả undocumented 404 | Documentation / contract | CONFIRMED |
| DEF-04 | Recipe `name=""` gây HTTP 500 + AssertionError | Validation / server failure | CONFIRMED |

**Tổng confirmed defect families hiện tại: 4.**

---

# 10. Tổng hợp non-SUT issues

| Nhóm | IDs |
|---|---|
| Environment | ENV-01, ENV-02, ENV-03 |
| Configuration | CFG-01, CFG-02 |
| Test/tooling | TEST-01, TEST-02, TEST-03, TEST-04, TEST-05, TEST-06 |
| Observation | OBS-01 |

Các mục trên không được tính vào số defect của Mealie.

---

# 11. Nguyên tắc tiếp tục cập nhật

Tài liệu này là **living defect log**. Ở các phase tiếp theo:

1. Mỗi finding mới phải được phân biệt rõ giữa environment/tooling và SUT.
2. Không nâng candidate thành confirmed chỉ từ một failure chưa triage.
3. Với destructive/write test, chỉ thao tác resource do test tạo và phải cleanup.
4. Không commit API token, password hoặc secret.
5. Giữ reproducer tối thiểu cho defect đã xác nhận.
6. Không sửa regression assertion để “làm xanh” một defect đang tồn tại.
7. Khi defect được fix ở phiên bản SUT khác, bổ sung baseline mới và kết quả retest thay vì xóa lịch sử cũ.
