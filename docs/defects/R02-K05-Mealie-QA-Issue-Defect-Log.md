# R02-K05-Mealie-QA — Issue & Defect Log

> Tài liệu theo dõi tập trung các lỗi, sự cố môi trường, vấn đề công cụ kiểm thử và defect candidate phát hiện trong quá trình thực hiện đồ án môn **Kiểm thử phần mềm**.
>
> **Quy ước:** Không phải mọi mục trong tài liệu này đều là lỗi của Mealie. Các mục được phân loại rõ để tránh nhầm lẫn khi viết báo cáo cuối kỳ.

## 1. Baseline

- **SUT:** Mealie
- **Release:** `v3.28.0`
- **Pinned commit:** `0552eaa4a80031b8572849cca0ed95d07f1be001`
- **API specification:** OpenAPI 3.1.0
- **OpenAPI snapshot:** `schema/snapshots/mealie-v3.28.0-openapi.json`
- **Local base URL:** `http://localhost:9091`
- **Testing approach:** Schema-Based API / Fuzz Testing
- **Main tool:** Schemathesis 4.28.0
- **Python:** 3.11.9

---

## 2. Tổng hợp issue/defect

| ID | Nhóm | Mô tả ngắn | Trạng thái | SUT defect? |
|---|---|---|---|---|
| ENV-01 | Environment | Windows CRLF/LF làm shell script/container khởi động lỗi | Resolved | Không |
| ENV-02 | Environment | Docker daemon/named pipe từng không khả dụng | Resolved | Không |
| ENV-03 | Environment | Docker config từng báo Access denied | Observed/Workaround | Không |
| CFG-01 | Configuration | Nhầm `/api/openapi.json`; schema đúng ở `/openapi.json` | Resolved | Không |
| CFG-02 | Configuration | Runtime báo `develop` dù baseline Git là `v3.28.0` | Understood | Không |
| TEST-01 | Test Infrastructure | Codex process không nhận `MEALIE_API_TOKEN` từ PowerShell | Workaround | Không |
| TEST-02 | Test Tooling | Schemathesis CLI filter chọn 118 operations và chạy POST ngoài P0 | Open | Không xác định là lỗi Schemathesis; hiện là tooling/config issue |
| TEST-03 | Test Design | Phase `examples` sinh 0 cases vì schema không có examples | Understood | Không |
| TEST-04 | Test Tooling | pytest không nhận `--hypothesis-max-examples=1` | Resolved | Không |
| DEF-01 | SUT | `GET /api/recipes?foods=` trả HTTP 500 | Reproducible 3/3 | Defect candidate |
| DEF-02 | SUT / API Contract | `orderBy=null` trả HTTP 400 không được OpenAPI document trên 3 GET endpoints | Reproduced across 3 endpoints | Reproducible contract defect candidate |
| DEF-03 | SUT / API Contract | Detail resource không tồn tại trả HTTP 404 nhưng OpenAPI không document 404 | Reproduced on 2 endpoints | Reproducible contract defect candidate |
| DEF-04 | SUT | `POST /api/recipes` với `{"name": ""}` trả HTTP 500 / AssertionError | Needs controlled triage | Defect candidate |

---

# 3. Environment / Setup Issues

## ENV-01 — Windows CRLF/LF làm Mealie container khởi động lỗi

### Hiện tượng

Trong quá trình build/chạy Mealie local trên Windows, shell scripts gặp vấn đề line endings. Container từng restart hoặc không chạy đúng, bao gồm lỗi liên quan đến script như:

```text
/app/run.sh: no such file
```

Các shell script khác cũng bị ảnh hưởng bởi CRLF/LF.

### Phân loại

**Environment / platform compatibility issue**

### Xử lý

- Kiểm tra line endings.
- Điều chỉnh Git/checkout để tránh CRLF phá shell scripts.
- Rebuild image/container không dùng cache khi cần.

### Kết quả

Mealie sau đó chạy healthy trên local Docker và API có thể truy cập tại port `9091`.

### Báo cáo

Có thể sử dụng trong phần **Khó khăn khi thiết lập môi trường** hoặc **Reproducibility**, không ghi là defect của Mealie API.

---

## ENV-02 — Docker daemon / named pipe không khả dụng

### Hiện tượng

Tại một thời điểm trong quá trình chuẩn bị Schemathesis POC, Docker daemon không hoạt động và Docker CLI không kết nối được tới Docker Engine/named pipe.

### Ảnh hưởng

- Mealie runtime không thể được xác minh.
- Schemathesis runtime smoke test bị block.

### Xử lý

Docker Desktop/runtime được khởi động lại và Mealie sau đó được xác minh:

```text
/api/app/about  -> HTTP 200
/openapi.json   -> HTTP 200
```

### Phân loại

**Environment issue**

### Báo cáo

Có thể nhắc trong phần troubleshooting; không phải SUT defect.

---

## ENV-03 — Docker configuration Access Denied

### Hiện tượng

Trong quá trình kiểm tra môi trường, cấu hình Docker tại máy local từng xuất hiện tình trạng `Access denied`.

### Phân loại

**Local environment / permissions issue**

### Ghi chú

Không tự động xóa hoặc thay đổi Docker configuration chỉ để vượt lỗi. Vấn đề được tách khỏi SUT.

---

# 4. Configuration / Baseline Issues

## CFG-01 — Xác định nhầm OpenAPI endpoint

### Hiện tượng

Ban đầu:

```text
/api/openapi.json
```

không phải OpenAPI schema mong muốn và có thể trả frontend HTML.

Endpoint đúng:

```text
/openapi.json
```

### Kết quả

OpenAPI snapshot hợp lệ được lưu tại:

```text
schema/snapshots/mealie-v3.28.0-openapi.json
```

Thông tin baseline:

```text
OpenAPI: 3.1.0
Paths: 182
Operations: 266
```

### Phân loại

**Configuration / API discovery issue**

---

## CFG-02 — Runtime version hiển thị `develop`

### Hiện tượng

`/api/app/about` có thể báo runtime version:

```text
develop
```

trong khi source đã được checkout tại release/tag:

```text
v3.28.0
```

và commit:

```text
0552eaa4a80031b8572849cca0ed95d07f1be001
```

### Quyết định

Baseline chính thức của project được xác định bằng **Git tag + pinned commit SHA**, không dùng duy nhất runtime version string.

### Phân loại

**Build/version metadata observation**

---

# 5. Test Infrastructure / Methodology Issues

## TEST-01 — Codex không nhận `MEALIE_API_TOKEN`

### Hiện tượng

PowerShell xác nhận:

```text
TOKEN SET
```

nhưng tiến trình Codex trả:

```text
TOKEN MISSING
```

### Nguyên nhân thực tế quan sát được

Token được đặt trong environment của PowerShell hiện tại nhưng tiến trình Codex không kế thừa environment đó.

### Workaround

Chạy authenticated test trực tiếp trong PowerShell chứa:

```text
MEALIE_API_TOKEN
```

Không hardcode token vào source code, README, evidence hoặc Git.

### Xác minh authentication

Authenticated request thủ công:

```text
GET /api/recipes -> HTTP 200
```

### Phân loại

**Test infrastructure / process environment issue**

---

## TEST-02 — Schemathesis CLI filtering không giới hạn đúng P0 operation

### Mục tiêu

Chỉ chạy:

```text
GET /api/recipes
```

### Các filter đã thử

Bao gồm các dạng:

```text
--include-path /api/recipes
--include-method GET
```

và path regex.

### Kết quả thực tế

Schemathesis báo:

```text
Operations: 118 selected / 266 total
```

và thậm chí thực thi:

```text
POST /api/recipes
```

ngoài phạm vi P0 read-only dự kiến.

Custom expression sau đó:

```text
method == "GET" and path == "/api/recipes"
```

lại chọn:

```text
0 selected / 266
```

### Workaround

Python Schemathesis API được sử dụng:

```python
schema.include(path=P0_PATHS, method="GET")
```

Offline selection test xác nhận chính xác 9 P0 GET operations.

Smoke test riêng cũng được pytest định danh đúng:

```text
test_p0_recipes_smoke[GET /api/recipes]
```

### Phân loại

**Testing-tool/configuration issue**

### Trạng thái

Chưa kết luận đây là bug của Schemathesis. Cần phân biệt giữa CLI semantics, cách sử dụng filter và tool behavior.

---

## TEST-03 — Schemathesis `examples` phase sinh 0 test cases

### Hiện tượng

POC ban đầu sử dụng:

```text
--phases examples
```

Kết quả:

```text
Selected: 118/266
Tested: 0
No test cases were generated
118 skipped - No examples in schema
```

### Giải thích

Phase `examples` phụ thuộc vào examples có trong API schema. Schema hiện tại không cung cấp examples phù hợp cho các operation được chọn.

### Quyết định

Không coi empty test suite là P0 PASS. Chuyển sang generated/fuzzing test với giới hạn chặt.

### Phân loại

**Test design / schema limitation**

---

## TEST-04 — pytest không hỗ trợ `--hypothesis-max-examples`

### Hiện tượng

Command:

```text
--hypothesis-max-examples=1
```

trả:

```text
unrecognized arguments: --hypothesis-max-examples=1
```

### Xử lý

Giới hạn số example trực tiếp trong Python test bằng Hypothesis:

```python
@settings(max_examples=1, deadline=None)
```

### Phân loại

**Test tooling/configuration issue**

---

# 6. SUT Defect Candidates

## DEF-01 — Empty `foods` query parameter causes HTTP 500

### Trạng thái

**Reproducible defect candidate**

### Endpoint

```text
GET /api/recipes
```

### Discovery

Schemathesis P0 test sinh request GET có nhiều query parameters và nhận:

```text
HTTP 500 Internal Server Error
```

Schemathesis báo:

1. Server error
2. Undocumented HTTP status code

Theo OpenAPI contract được test, operation này document:

```text
200
422
```

### Baseline request

Authenticated request không có query parameter:

```text
GET /api/recipes
```

Kết quả:

```text
HTTP 200
```

### Isolation

Các empty query parameters được thử riêng:

```text
categories=       -> 200
foods=            -> 500
households=       -> 200
orderBy=          -> 200
queryFilter=      -> 200
paginationSeed=   -> 200
cookbook=         -> 200
search=           -> 200
```

Failure được cô lập thành:

```text
GET /api/recipes?foods=
```

### Expected

API không nên gặp unexpected server-side failure khi nhận input biên này.

Theo contract hiện tại, documented responses được Schemathesis xác định là:

```text
200, 422
```

### Actual

```text
HTTP 500 Internal Server Error
```

### Reproducibility

Minimal request được chạy ba lần liên tiếp:

```text
Run 1 -> HTTP 500
Run 2 -> HTTP 500
Run 3 -> HTTP 500
```

**Reproduction rate: 3/3**

### Security

Không lưu API token hoặc credential trong evidence.

### Evidence

Evidence Markdown:

```text
evidence/test-runs/recipe-empty-foods-500.md
```

Schemathesis JSON reports của quá trình discovery cũng được giữ trong local evidence directory nếu còn tồn tại.

### Root cause

**Chưa xác định.**

Không gán root cause cho tới khi kiểm tra implementation/log/backend validation tương ứng.

### Giá trị đối với báo cáo

Đây hiện là finding mạnh nhất của project vì thể hiện đầy đủ:

```text
Schema-Based Testing
        ↓
Generated boundary input
        ↓
Unexpected HTTP 500
        ↓
Manual reproduction
        ↓
Parameter isolation
        ↓
Minimal failing request
        ↓
3/3 reproducibility
        ↓
Defect candidate
```

---

## DEF-02 — `orderBy=null` causes undocumented HTTP 400 across multiple endpoints

### Trạng thái

**Reproducible API contract defect candidate**

### Affected endpoints

```text
GET /api/households/shopping/lists
GET /api/households/shopping/items
GET /api/households/mealplans
```

### Discovery

Schemathesis schema-based fuzz testing sinh request có:

```text
?orderBy=null
```

và phát hiện:

```text
Undocumented HTTP status code

Received: 400
Documented: 200, 422
```

Response của server:

```text
Invalid order_by statement "null": "null" is invalid
```

Schemathesis reproducer ban đầu còn chứa:

```text
x-schemathesis-unknown-property=42
```

nên request sau đó được thu nhỏ thủ công để loại parameter này khỏi nguyên nhân.

### Manual reproduction

Các request tối thiểu sau vẫn trả HTTP 400:

```text
GET /api/households/shopping/lists?orderBy=null  -> 400
GET /api/households/shopping/items?orderBy=null  -> 400
GET /api/households/mealplans?orderBy=null        -> 400
```

### Control requests

Không truyền `orderBy`:

```text
GET /api/households/shopping/lists  -> 200
GET /api/households/shopping/items  -> 200
GET /api/households/mealplans        -> 200
```

Do đó pattern quan sát được:

```text
normal request   -> 200
?orderBy=null    -> 400
```

trên cả ba endpoint.

### OpenAPI contract

Snapshot OpenAPI khai báo `orderBy` giống nhau trên cả ba operation:

```json
{
  "name": "orderBy",
  "in": "query",
  "required": false,
  "schema": {
    "anyOf": [
      {
        "type": "string"
      },
      {
        "type": "null"
      }
    ],
    "title": "Orderby"
  }
}
```

Documented responses:

```text
200
422
```

Không có response `400`.

### Contract analysis

Query string:

```text
?orderBy=null
```

truyền chuỗi `"null"` qua HTTP. Chuỗi này phù hợp với nhánh:

```json
{"type": "string"}
```

của schema hiện tại, vì schema không khai báo `enum`, `pattern`, hoặc constraint khác để loại giá trị `"null"`.

Implementation lại từ chối giá trị này và trả:

```text
HTTP 400 Bad Request
```

trong khi `400` không được OpenAPI contract document.

### Finding

Có sự không đồng nhất quan sát được giữa OpenAPI contract và runtime behavior:

1. Schema cho phép Schemathesis sinh một string như `"null"`.
2. Runtime từ chối giá trị đó.
3. Runtime sử dụng HTTP 400.
4. OpenAPI chỉ document 200 và 422.

### Classification

**API contract inconsistency / undocumented error response**

Ba endpoint hiện được gom thành **một defect family**, không tính thành ba defect độc lập, vì chúng thể hiện cùng pattern `orderBy` và cùng response behavior.

### Security

Không credential hoặc bearer token nào được lưu trong evidence.

### Root cause

**Chưa xác định.**

Có khả năng các endpoint dùng chung sorting/order-by handling, nhưng chưa kiểm tra source/log nên không kết luận đây là root cause.

### Value for K05

Finding này minh họa Schema-Based API Testing phát hiện contract mismatch mà không cần server crash:

```text
OpenAPI
   ↓
Schemathesis generates orderBy input
   ↓
Runtime returns HTTP 400
   ↓
Status-code conformance oracle fails
   ↓
Manual minimization
   ↓
Control 200 vs orderBy=null 400
   ↓
Contract mismatch reproduced on 3 endpoints
```

---

## DEF-03 — Undocumented HTTP 404 for nonexistent detail resources

### Trạng thái

**Reproducible API contract defect candidate**

### Affected endpoints

```text
GET /api/recipes/{slug}
GET /api/households/mealplans/{item_id}
```

### Discovery

Trong P0 detail schema-based campaign, Schemathesis sinh path parameter `0` cho hai operation và nhận:

```text
GET /api/recipes/0
→ HTTP 404

GET /api/households/mealplans/0
→ HTTP 404
```

Schemathesis báo:

```text
Undocumented HTTP status code

Received: 404
Documented: 200, 422
```

### Runtime responses

Recipe detail:

```json
{"detail":{"message":"No Entry Found","error":true,"exception":null}}
```

Meal-plan detail:

```json
{"detail":{"message":"Not found.","error":true,"exception":null}}
```

### Manual reproduction

Các request tối giản, không chứa header `accept-language: {}` do Schemathesis sinh, vẫn trả:

```text
http://localhost:9091/api/recipes/0
→ HTTP 404

http://localhost:9091/api/households/mealplans/0
→ HTTP 404
```

Điều này loại header Schemathesis khỏi nguyên nhân của response 404.

### Expected / contract observation

HTTP 404 là hành vi runtime hợp lý khi resource được yêu cầu không tồn tại.

Finding không phải là việc server trả `404`; finding là **OpenAPI contract không document response 404 mà implementation thực tế có thể trả**.

OpenAPI documented responses:

```text
200
422
```

### Classification

**API contract / documentation inconsistency — undocumented 404 response**

Hai endpoint được gom thành một defect family vì cùng thể hiện một loại contract mismatch.

### Security

Không credential hoặc bearer token nào được lưu trong evidence.

### Root cause

**Chưa xác định.**

Không suy đoán root cause trước khi kiểm tra implementation hoặc schema-generation logic.

### Value for K05

```text
OpenAPI schema
      ↓
Schemathesis generates nonexistent identifier
      ↓
Runtime returns 404
      ↓
Status-code conformance oracle fails
      ↓
Manual minimal reproduction
      ↓
404 confirmed without generated auxiliary header
      ↓
OpenAPI/runtime contract mismatch
```

---

## DEF-04 — Empty recipe name produced HTTP 500 / AssertionError

### Trạng thái

**Potential defect candidate — requires controlled triage**

### Discovery

Trong lúc Schemathesis CLI filtering chưa hoạt động đúng như dự kiến, tool ngoài ý muốn thực thi:

```text
POST /api/recipes
```

với body:

```json
{
  "name": ""
}
```

### Actual

Server trả:

```text
HTTP 500 Internal Server Error
```

Response từng chứa thông tin:

```text
exception: AssertionError
```

Schemathesis báo hai failure:

1. Server error
2. Undocumented HTTP status code

### Contract observed by Schemathesis

Documented responses:

```text
201
422
```

### Important limitation

Finding này được phát hiện khi P0 campaign dự kiến read-only nhưng CLI filtering chọn sai phạm vi và chạy POST.

Vì vậy finding **không được coi là confirmed defect** chỉ dựa trên lần discovery đó.

### Next step

Cần triage có kiểm soát:

1. Xác nhận request contract.
2. Xác nhận request body tối thiểu hợp lệ/không hợp lệ.
3. Tái hiện trong môi trường QA.
4. Kiểm tra có tạo resource ngoài ý muốn hay không.
5. Cleanup nếu cần.
6. Lặp lại để xác định reproducibility.
7. Chỉ sau đó mới nâng trạng thái finding.

---

# 7. Các finding KHÔNG được coi là SUT defect

Các vấn đề sau không được đưa vào bảng defect của Mealie:

- Docker daemon không chạy.
- Docker permission/configuration trên máy local.
- CRLF/LF khi checkout/build trên Windows.
- Codex không kế thừa environment variable.
- pytest không hỗ trợ một CLI argument.
- Schemathesis examples phase không sinh case khi schema không có examples.
- Việc chọn sai OpenAPI URL trong quá trình setup.

Chúng vẫn có giá trị trong các phần:

- Environment setup
- Troubleshooting
- Testing limitations
- Lessons learned
- Reproducibility

---

# 8. Defect Status Definitions

| Trạng thái | Ý nghĩa |
|---|---|
| Observed | Đã quan sát thấy hiện tượng nhưng chưa tái hiện đủ |
| Potential defect candidate | Có dấu hiệu lỗi SUT nhưng cần triage |
| Reproducible defect candidate | Đã có minimal/controlled reproduction ổn định |
| Confirmed defect | Có đủ evidence và phân tích để kết luận implementation/contract có defect |
| Resolved | Đã có fix và retest PASS |
| Not a defect | Triage xác định nguyên nhân không thuộc SUT |

---

# 9. Quy trình cập nhật finding mới

Mỗi finding mới cần ghi:

```text
ID
Category
Date/phase discovered
SUT baseline
Endpoint/component
Preconditions
Input/request
Expected result
Actual result
Reproduction steps
Reproduction rate
Evidence
Severity/impact (chỉ khi có căn cứ)
Classification
Root cause (nếu đã xác định)
Status
Retest result
```

Không tự suy đoán root cause hoặc severity nếu chưa có evidence.

---

# 10. Current Defect Summary

Tại thời điểm tạo tài liệu:

### Reproducible SUT defect candidates

**DEF-01**

```text
GET /api/recipes?foods=
→ HTTP 500
→ Reproduced 3/3
```

### Reproducible API contract defect candidates

**DEF-02**

```text
GET /api/households/shopping/lists?orderBy=null  -> 400
GET /api/households/shopping/items?orderBy=null  -> 400
GET /api/households/mealplans?orderBy=null        -> 400

Control without orderBy                           -> 200
OpenAPI documented responses                     -> 200, 422
```

Classification: API contract inconsistency / undocumented HTTP 400 response.

### Reproducible API contract defect candidates

**DEF-03**

```text
GET /api/recipes/0                         -> 404
GET /api/households/mealplans/0           -> 404
OpenAPI documented responses              -> 200, 422
```

Classification: API contract / documentation inconsistency — undocumented 404 response.

### SUT findings requiring further triage

**DEF-04**

```text
POST /api/recipes
{"name": ""}
→ HTTP 500 / AssertionError
```

### Environment / configuration / tooling issues

```text
ENV-01
ENV-02
ENV-03
CFG-01
CFG-02
TEST-01
TEST-02
TEST-03
TEST-04
```

---

## Maintenance Note

Tài liệu này là **living issue/defect log** của project.

Khi phát hiện lỗi mới:

1. Không ghi đè finding cũ.
2. Cấp ID mới theo nhóm phù hợp.
3. Thêm evidence và reproduction.
4. Cập nhật trạng thái sau triage/retest.
5. Giữ nguyên lịch sử finding để phục vụ báo cáo cuối kỳ.

---

# 11. Phase 3 P0 — K05 Checkpoint Summary

## Scope exercised

P0 contained **9 authenticated read-only GET operations**:

```text
GET /api/recipes
GET /api/recipes/{slug}
GET /api/households/shopping/lists
GET /api/households/shopping/lists/{item_id}
GET /api/households/shopping/items
GET /api/households/shopping/items/{item_id}
GET /api/households/mealplans
GET /api/households/mealplans/{item_id}
GET /api/households/mealplans/today
```

**Coverage checkpoint: 9/9 P0 operations exercised.**

## K05 method used

```text
Saved OpenAPI 3.1.0 snapshot
        ↓
Schemathesis 4.28.0
        ↓
Schema-derived request generation
        ↓
Authenticated local GET requests
        ↓
Oracles:
- not_a_server_error
- status_code_conformance
- response_schema_conformance
        ↓
Failure reproduction and minimization
        ↓
Defect-family classification
```

Python Schemathesis API filtering was used for the controlled P0 campaign because earlier CLI filtering did not restrict execution as expected.

## Collection campaign

Five collection/read operations were exercised.

Observed pytest result:

```text
4 failed, 1 passed
```

Failures represented two unique defect families rather than four independent defects:

- **DEF-01:** `/api/recipes?foods=` -> HTTP 500.
- **DEF-02:** `orderBy=null` -> undocumented HTTP 400 across three endpoints.

`GET /api/households/mealplans/today` completed the bounded campaign without a detected failure.

## Detail campaign

Four detail operations were exercised.

Observed pytest result:

```text
2 failed, 2 passed
```

The two failures represented one shared defect family:

- **DEF-03:** nonexistent detail resource -> HTTP 404 while OpenAPI documents only 200/422.

The other two detail operations completed this bounded campaign without a detected failure.

## Confirmed P0 findings

### DEF-01 — Server-side failure

```text
GET /api/recipes?foods=
→ HTTP 500
→ OpenAPI: 200, 422
→ reproduced 3/3
```

Classification:

```text
Unexpected server-side failure + undocumented status
```

### DEF-02 — Undocumented HTTP 400

Affected:

```text
GET /api/households/shopping/lists?orderBy=null
GET /api/households/shopping/items?orderBy=null
GET /api/households/mealplans?orderBy=null
```

Control requests without `orderBy` returned HTTP 200.

Runtime:

```text
?orderBy=null → HTTP 400
```

OpenAPI:

```text
orderBy: string | null
responses: 200, 422
```

Classification:

```text
API contract inconsistency / undocumented error response
```

### DEF-03 — Undocumented HTTP 404

Affected:

```text
GET /api/recipes/0
GET /api/households/mealplans/0
```

Runtime:

```text
HTTP 404
```

OpenAPI:

```text
200, 422
```

Classification:

```text
API contract / documentation inconsistency
```

The runtime 404 itself is reasonable for a nonexistent resource; the finding is that the contract does not document it.

## Out-of-scope finding retained for later triage

**DEF-04**

```text
POST /api/recipes
{"name": ""}
→ HTTP 500 / AssertionError
```

This was discovered accidentally while CLI filtering executed a POST outside the intended P0 read-only scope. It remains a potential defect candidate and is not counted as a confirmed P0 defect family.

## Phase 3 P0 result

```text
P0 operations selected:                 9
P0 operations exercised:                9
Coverage of selected P0 operations:     9/9
Reproducible P0 defect families:        3
Out-of-scope candidates retained:       1
Server-error families:                  1
Contract/status mismatch families:      2
```

A pytest `FAILED` result is not interpreted as failure of the K05 POC itself. The testing harness successfully generated schema-derived inputs, exercised the SUT, applied contract/invariant checks, and exposed reproducible SUT/API-contract findings.

### Phase status

**Phase 3 P0 / K05 proof of concept: COMPLETE for the bounded selected scope.**

This does **not** mean the whole Mealie API has been fully tested. It means all 9 operations selected for the P0 read-only campaign were exercised and the resulting failure families were triaged.

## Gate before P1

Before opening P1 controlled write/lifecycle testing:

1. Preserve the P0 tests and evidence.
2. Update `tests/README.md` so it no longer recommends the misleading CLI filtering path.
3. Keep credentials out of Git.
4. Run `pip check`, selection test, and `git diff --check`.
5. Review `git status` and commit the coherent Phase 3 P0 artifacts.
6. Define P1 cleanup/rollback rules before executing POST/PUT/PATCH/DELETE operations.
