# MA TRẬN TRUY VẾT ĐẶC TẢ – TEST CASE – KẾT QUẢ KIỂM THỬ

> **Mã tài liệu:** R02-K05-RTM-01 · **Phiên bản:** 1.0  
> **Dự án:** R02-K05-Mealie-QA  
> **Tài liệu đặc tả đi kèm:** [`../specification/MEALIE-FUNCTIONAL-SPECIFICATION.md`](../specification/MEALIE-FUNCTIONAL-SPECIFICATION.md)  
> **SUT:** Mealie v3.28.0 (`0552eaa4a80031b8572849cca0ed95d07f1be001`) · **OpenAPI:** 3.1.0  
> **Nguồn kết quả:** `reports/test-results.xml`, `reports/final/FINAL-RESULTS.md`, các bản P0/P1 summary và `evidence/defects/`.  
> **Lưu ý:** bảng dưới đây là **truy vết hồi cứu từ lần chạy đã lưu**, không phải kết quả chạy lại hôm nay. Không khẳng định hai tài liệu mới đã tồn tại trước các test lịch sử.

---

## 1. Mục đích và cách sử dụng

Ma trận này trả lời trực tiếp những câu hỏi của giảng viên: **(1) Đặc tả yêu cầu nói gì? (2) Test nào kiểm tra yêu cầu đó? (3) Input/expected là gì? (4) Hệ thống đã trả gì? (5) Chênh lệch nằm ở ứng dụng, hợp đồng API hay bộ test?**

### 1.1 Quy ước

| Ký hiệu | Ý nghĩa |
|---|---|
| `REQ-COM/REC/LST/ITM/MLP-*` | Yêu cầu thuộc tài liệu đặc tả chức năng đi kèm |
| `TC-01` … `TC-21` | **21 mục pytest** được thu thập trong `reports/test-results.xml`; ID do tài liệu này gán để theo dõi |
| `C` | Expected theo snapshot OpenAPI / oracle O1–O7 |
| `T` | Kỳ vọng thử nghiệm/bài toán dữ liệu do nhóm chọn; không đồng nghĩa với OpenAPI |
| `O` | Actual từ execution/evidence lịch sử |
| `PASS`, `FAIL` | Verdict của một mục pytest, không phải kết luận toàn bộ chức năng |
| `DEF-xx` | Họ sai lệch đã lập hồ sơ; nhiều TC có thể cùng liên hệ một DEF |
| `OBS-xx`, `TEST-xx` | Quan sát về schema hoặc lỗi giả định của bộ test (không được tính SUT defect) |

**Quy tắc định lượng:** 21 mục pytest **không phải 21 API endpoints** cũng **không đồng nghĩa 21 HTTP requests**. P0 có 9 GET operations khác nhau, nhưng GET Recipes được chạy thêm smoke; P1 có test lặp nhiều payload trong cùng một hàm. Một lần chạy test P0 có thể sinh nhiều examples từ Hypothesis/Schemathesis.

### 1.2 Phương pháp tính verdict

- **PASS** nếu *mọi assertion thực sự được triển khai* trong mục test đều đạt; PASS chỉ có giá trị trong phạm vi những assertion đó.
- **FAIL** nếu một trong các assertion vi phạm (ví dụ undocumented 400/404, HTTP 500); không tự động kết luận do test harness hay có defect độc lập.
- **SKIP** nếu biến `MEALIE_API_TOKEN` chưa được cung cấp; đây là điều kiện chạy, không phải kết quả kiểm thử API.
- **Contract mismatch** (DEF-02/DEF-03) khác **server-error** (DEF-01/DEF-04). HTTP 404 cho tài nguyên không tồn tại có thể hợp lý về nghiệp vụ nhưng vẫn chưa được **contract** công bố.
- Kết quả lưu tại XML có **13 PASS, 8 FAIL, 0 SKIP**. P0: 4 PASS/7 FAIL; P1: 9 PASS/1 FAIL.

---

## 2. Ma trận tổng hợp toàn bộ 21 test case

| ID | Priority | Requirement IDs chính | Thao tác / kỹ thuật | File test / định danh | Historical | Finding |
|---|---|---|---|---|---|---|
| TC-01 | P0 | REQ-LST-01, COM-02/03/04 | GET Shopping Lists collection; schema fuzz | `test_p0_collections.py` · `GET /api/households/shopping/lists` | **FAIL** | DEF-02 |
| TC-02 | P0 | REQ-ITM-01, COM-02/03/04 | GET Shopping Items collection; schema fuzz | `test_p0_collections.py` · `GET /api/households/shopping/items` | **FAIL** | DEF-02 |
| TC-03 | P0 | REQ-MLP-01, COM-02/03/04 | GET Meal Plans collection; schema fuzz | `test_p0_collections.py` · `GET /api/households/mealplans` | **FAIL** | DEF-02 |
| TC-04 | P0 | REQ-MLP-02, COM-02/03/04 | GET Today's Meal Plans; schema fuzz | `test_p0_collections.py` · `GET /api/households/mealplans/today` | **PASS** | — |
| TC-05 | P0 | REQ-REC-01/06, COM-02/03/04 | GET Recipes collection; schema fuzz | `test_p0_collections.py` · `GET /api/recipes` | **FAIL** | DEF-01 |
| TC-06 | P0 | REQ-LST-02, COM-02/03/04 | GET Shopping List detail; schema fuzz | `test_p0_details.py` · `GET /api/households/shopping/lists/{item_id}` | **PASS** | — |
| TC-07 | P0 | REQ-ITM-02, COM-02/03/04 | GET Shopping Item detail; schema fuzz | `test_p0_details.py` · `GET /api/households/shopping/items/{item_id}` | **PASS** | — |
| TC-08 | P0 | REQ-MLP-03, COM-02/03/04 | GET Meal Plan detail; schema fuzz | `test_p0_details.py` · `GET /api/households/mealplans/{item_id}` | **FAIL** | DEF-03 |
| TC-09 | P0 | REQ-REC-02, COM-02/03/04 | GET Recipe detail; schema fuzz | `test_p0_details.py` · `GET /api/recipes/{slug}` | **FAIL** | DEF-03 |
| TC-10 | P0 | REQ-COM-08 | Snapshot operation selection; offline | `test_p0_selection.py` · `test_snapshot_selects_only_p0_read_operations` | **PASS** | — |
| TC-11 | P0 | REQ-REC-01/06, COM-02/03/04 | GET Recipes smoke; schema fuzz giới hạn | `test_p0_smoke.py` · `GET /api/recipes` | **FAIL** | DEF-01 |
| TC-12 | P1 | REQ-MLP-07, COM-02/06 | POST Meal Plan; 7 boundary payloads | `test_p1_mealplan_boundaries.py` | **PASS** | OBS-01 |
| TC-13 | P1 | REQ-MLP-03/04/05/06, COM-06/07 | Meal Plan lifecycle | `test_p1_mealplan_lifecycle.py` | **PASS** | 404 post-delete thuộc T |
| TC-14 | P1 | REQ-REC-05, COM-02/04 | POST Recipe empty name; 3 lần | `test_p1_recipe_empty_name.py` | **FAIL** | DEF-04 |
| TC-15 | P1 | REQ-REC-02/03/04, COM-06/07 | Recipe create/read/delete | `test_p1_recipe_lifecycle.py` | **PASS** | 404 post-delete thuộc T; TEST-06 đã xử lý |
| TC-16 | P1 | REQ-ITM-06, COM-02/06 | POST Shopping Item; 6 boundary payloads | `test_p1_shopping_item_boundaries.py` | **PASS** | Chỉ kiểm mã 201/422 |
| TC-17 | P1 | REQ-ITM-02/03/04/05, COM-06/07 | Shopping Item lifecycle + parent list | `test_p1_shopping_item_lifecycle.py` | **PASS** | 404 post-delete thuộc T; TEST-05 đã xử lý |
| TC-18 | P1 | REQ-LST-06, COM-02/06 | POST Shopping List `{}` | `test_p1_shopping_list_boundaries.py` · `empty_object` | **PASS** | — |
| TC-19 | P1 | REQ-LST-06, COM-02/06 | POST Shopping List `{"name":null}` | `test_p1_shopping_list_boundaries.py` · `null_name` | **PASS** | — |
| TC-20 | P1 | REQ-LST-06, COM-02/06 | POST Shopping List `{"name":""}` | `test_p1_shopping_list_boundaries.py` · `empty_name` | **PASS** | — |
| TC-21 | P1 | REQ-LST-02/03/04/05, COM-06/07 | Shopping List lifecycle | `test_p1_shopping_list_lifecycle.py` | **PASS** | 404 post-delete thuộc T |

**Vì sao có đúng 21?** `test_p0_collections.py` = 5; `test_p0_details.py` = 4; `test_p0_selection.py` = 1; `test_p0_smoke.py` = 1; tám file P1: Meal Plan boundaries 1, Meal Plan lifecycle 1, Recipe empty name 1, Recipe lifecycle 1, Shopping Item boundaries 1, Shopping Item lifecycle 1, Shopping List boundaries **3** do `@pytest.mark.parametrize`, Shopping List lifecycle 1. Tổng `5+4+1+1+1+1+1+1+1+1+3+1=21`.

---

## 3. Chi tiết test case P0 (TC-01 đến TC-11)

**Preconditions chung:** SUT `localhost:9091` hoạt động; token Bearer hợp lệ; snapshot đúng version. Các test P0 không ghi dữ liệu. Với các mục fuzzing, case cụ thể được **Schemathesis sinh từ schema**, vì vậy query/path có thể thay đổi qua lần chạy. Không bịa một bộ tham số duy nhất áp dụng cho mọi example; các request ở phần actual là **minimized reproductions** được nhóm giữ lại.

### TC-01 — Shopping Lists collection

- **API:** `GET /api/households/shopping/lists`.
- **Mục đích:** xác minh truy vấn collection và các tham số pagination/sort theo OpenAPI.
- **Thiết kế:** Schemathesis sinh GET query; giới hạn `max_examples=3`.
- **Expected (C):** `200` hoặc `422`; JSON body nếu có schema phải hợp lệ, không undocumented 5xx.
- **Actual (O):** case tái hiện `GET .../lists?orderBy=null` trả `400`, body cho biết `Invalid order_by statement "null"`; baseline không có query trả 200.
- **Verdict:** **FAIL**, do status `400` không thuộc `{200,422}`; **DEF-02**.
- **Lưu ý:** không diễn giải `orderBy=null` là JSON null thực; đây là literal string trong query.

### TC-02 — Shopping Items collection

- **API:** `GET /api/households/shopping/items`.
- **Mục đích:** kiểm hợp đồng GET item collection, filter/sort và pagination.
- **Expected (C):** `{200,422}`; body 200 phù hợp `ShoppingListItemPagination` và trường `items`.
- **Actual (O):** `?orderBy=null` → 400 undocumented; baseline GET không query → 200.
- **Verdict:** **FAIL**; **DEF-02**.

### TC-03 — Meal Plans collection

- **API:** `GET /api/households/mealplans`.
- **Mục đích:** GET collection, thử tham số query `start_date`/`end_date`/`orderBy`.
- **Expected (C):** `{200,422}`, schema-conformant response nếu mô tả.
- **Actual (O):** `?orderBy=null` → 400 undocumented; baseline GET không query → 200.
- **Verdict:** **FAIL**; **DEF-02**.

### TC-04 — Today's Meal Plans

- **API:** `GET /api/households/mealplans/today`.
- **Mục đích:** đọc endpoint theo ngày hiện tại, không làm thay đổi dữ liệu.
- **Expected (C):** `{200,422}`; dùng ba Schemathesis checks, kiểm schema nếu response có schema cụ thể.
- **Actual (O):** mục test hoàn tất không vi phạm assertion.
- **Verdict:** **PASS**. **Không khẳng định** dữ liệu meal plan hôm nay có số lượng cụ thể vì test không assert điều đó.

### TC-05 — Recipes collection

- **API:** `GET /api/recipes`.
- **Mục đích:** fuzz query/filter recipe, đặc biệt các giá trị rỗng và kết hợp tham số.
- **Expected (C):** `{200,422}`; không undocumented 5xx.
- **Actual (O):** tái hiện độc lập `GET /api/recipes?foods=` → 500 (3/3 trong Phase 4). Mục pytest fuzzing gặp 500 với query do công cụ sinh.
- **Verdict:** **FAIL**; **DEF-01** (RCA: **likely implementation path**, chưa xác nhận bằng stack trace trực tiếp).

### TC-06 — Shopping List detail

- **API:** `GET /api/households/shopping/lists/{item_id}`.
- **Mục đích:** kiểm path parameter chuỗi và response detail.
- **Expected (C):** `{200,422}` và schema khi được khai báo.
- **Actual (O):** test schema fuzzing hoàn tất đạt checks đã bật.
- **Verdict:** **PASS**. Không tự kết luận mọi ID không tồn tại đều được xử lý đúng.

### TC-07 — Shopping Item detail

- **API:** `GET /api/households/shopping/items/{item_id}`.
- **Mục đích:** kiểm path parameter và chi tiết mặt hàng.
- **Expected (C):** `{200,422}`, schema khi có.
- **Actual (O):** test schema fuzzing hoàn tất đạt checks đã bật.
- **Verdict:** **PASS**.

### TC-08 — Meal Plan detail

- **API:** `GET /api/households/mealplans/{item_id}`; `item_id` integer.
- **Mục đích:** kiểm kiểu ID, đặc biệt tài nguyên không tìm thấy.
- **Expected (C):** OpenAPI GET khai báo `{200,422}`, **không khai báo 404**.
- **Actual (O):** `GET /api/households/mealplans/0` → 404, tái hiện 3/3.
- **Verdict:** **FAIL** đối với *contract coverage*, không phải vì 404 luôn sai về nghiệp vụ; **DEF-03**.

### TC-09 — Recipe detail

- **API:** `GET /api/recipes/{slug}`; `slug` string.
- **Mục đích:** kiểm tra get recipe theo slug do schema sinh.
- **Expected (C):** `{200,422}`, **không khai báo 404**.
- **Actual (O):** `GET /api/recipes/0` → 404, tái hiện 3/3.
- **Verdict:** **FAIL** đối với *contract coverage*; **DEF-03**.

### TC-10 — P0 selection (offline)

- **Đối tượng:** snapshot JSON, không gọi API và không cần token.
- **Mục đích:** khóa phạm vi ở đúng **9 GET operations** để tránh Schemathesis tác động các method ghi hoặc endpoint nhạy cảm.
- **Expected (T):** set chọn được bằng `schema.include(..., method="GET")` trùng đúng set 9 path trong code.
- **Actual (O):** so sánh set thành công.
- **Verdict:** **PASS**. Đây là bài kiểm tra **cấu hình lựa chọn scope**, không phải kiểm tra nghiệp vụ runtime.

### TC-11 — Recipe smoke

- **API:** `GET /api/recipes`.
- **Mục đích:** kiểm tra nhanh đường đi schema → request → validation của Recipe; `max_examples=1`.
- **Expected (C):** response nằm trong `{200,422}`, không 5xx undocumented, body theo schema khi có.
- **Actual (O):** vi phạm trong pha smoke; DEF-01 có minimal case độc lập `?foods=` → 500.
- **Verdict:** **FAIL**, **DEF-01**. Đây là cùng operation/họ defect với TC-05, **không đếm thành lỗi mới**.

---

## 4. Chi tiết test case P1 (TC-12 đến TC-21)

**Preconditions chung:** tài khoản và token hợp lệ; quyền thao tác dữ liệu QA trong household; cleanup chỉ được tác động tài nguyên do test tạo. P1 dùng `requests`, assertion thủ công; **không phải** toàn bộ P1 chạy ba Schemathesis checks của P0.

### TC-12 — Meal Plan create boundaries (1 mục pytest, 7 payload)

- **API:** `POST /api/households/mealplans`.
- **Mục tiêu:** quan sát validation với những biến thể của `CreatePlanEntry`.
- **Expected (C, assertion thực tế):** status nằm trong `{201,422}`; nếu nhận 201, body phải có `id` để cleanup.
- **Actual tổng hợp P1 (O):** cả 7 payload lần lưu bằng chứng đều trả `422`; test PASS vì `422` đã khai báo.
- **Verdict:** **PASS**; **OBS-01** về validation liên trường.

| Case | Payload | Expected status theo assertion | Historical status |
|---|---|---|---|
| `minimal_valid` | `{ "date": "<future-date>" }` | 201 hoặc 422 | 422 |
| `empty_title` | `{ "date": "<future-date>", "title": "" }` | 201 hoặc 422 | 422 |
| `null_recipe_id` | `{ "date": "<future-date>", "recipeId": null }` | 201 hoặc 422 | 422 |
| `missing_required_date` | `{}` | 201 hoặc 422 | 422 |
| `invalid_date_format` | `{ "date": "not-a-date" }` | 201 hoặc 422 | 422 |
| `invalid_recipe_uuid` | `{ "date": "<future-date>", "recipeId": "not-a-uuid" }` | 201 hoặc 422 | 422 |
| `invalid_entry_type` | `{ "date": "<future-date>", "entryType": "not-a-meal-type" }` | 201 hoặc 422 | 422 |

**Giới hạn:** tên `minimal_valid` chỉ có nghĩa *đủ required field trên schema*, không đảm bảo hợp lệ theo business validation. Sau khi thầy duyệt, có thể tách các case thành các ID con `TC-12.1`...`TC-12.7` và xác định cụ thể expected per payload; **không thay đổi số 21 mục pytest của lần chạy hiện có**.

### TC-13 — Meal Plan lifecycle

- **API:** `POST /api/households/mealplans` → `GET/PUT/GET/DELETE/GET /api/households/mealplans/{item_id}`.
- **Test data:** `date=today+30 days`, `entryType="breakfast"`, tên `K05-P1-MEALPLAN-<unique>`, `text` gắn nhãn QA.
- **Expected:** POST 201 và trả `id`, `date`, `title`; GET 200 đúng id/title; PUT 200 (body dùng `id`, `groupId`, `userId`, `date` đã lấy từ GET); GET verify 200 có title/text mới; DELETE 200; GET hậu xóa **404 theo T**.
- **Actual (O):** 201 → 200 → 200 → 200 → 200 → 404; so khớp dữ liệu theo assertion.
- **Verdict:** **PASS**, cleanup entry tạm. **Không dùng HTTP 404 này làm bằng chứng rằng 404 đã được OpenAPI khai báo.**

### TC-14 — DEF-04: Recipe empty name

- **API:** `POST /api/recipes`.
- **Input:** `{"name":""}`, gửi **3 lần trong một mục test**.
- **Expected (C):** code hợp đồng `{201,422}`, không 500. `CreateRecipe.name` là trường string required nhưng không có `minLength`.
- **Actual (O):** `[500, 500, 500]`; body có `Unknown Error` và `AssertionError`.
- **Verdict:** **FAIL**; **DEF-04**, tái hiện 3/3. Đây là một kiểm thử có chủ đích bắt sai lệch; **không sửa assertion thành `==500` để biến thành PASS**. Test có nhánh cleanup nếu bất ngờ trả 201.

### TC-15 — Recipe lifecycle

- **API:** `POST /api/recipes` → `GET /api/recipes/{slug}` → `DELETE /api/recipes/{slug}` → GET lại.
- **Input:** `{"name":"K05 P1 Recipe <unique>"}`.
- **Expected:** POST 201 trả **chuỗi slug** không rỗng; GET 200 có `slug` và `name` khớp; DELETE 200; GET sau DELETE 404 (**T**).
- **Actual (O):** chuỗi trạng thái 201 → 200 → 200 → 404, tên/slug nhất quán.
- **Verdict:** **PASS**. `TEST-06` là lỗi giả định cũ của harness (tưởng POST trả object), đã được sửa; **không phải defect Mealie**. **Không nói test đã update/patch Recipe** — mã hiện tại không làm thao tác này.

### TC-16 — Shopping Item boundaries (1 mục pytest, 6 payload)

- **API:** `POST /api/households/shopping/items` với một list cha tạm đã tạo qua POST Shopping Lists.
- **Expected (C, assertion thực tế):** status `{201,422}`; nếu 201, liệt kê `createdItems[]` để lấy `id` và cleanup child trước parent.
- **Actual (O):** mục pytest PASS cho cả vòng lặp; bằng chứng tổng hợp không liệt kê status **từng payload**, do đó không tự ghi 201/422 cụ thể cho mỗi dòng.
- **Verdict:** **PASS** về điều kiện status; không kết luận chính sách business với số lượng âm.

| Subcase | Request body cốt lõi | Tại sao chọn |
|---|---|---|
| `minimal_valid` | `{"shoppingListId":"<parent-uuid>"}` | Chỉ có required field |
| `null_optional_fields` | Parent UUID + nullable `food`, `unit`, `note`, `foodId`, `labelId`, `unitId` | Kiểm null trên optional |
| `zero_quantity` | Parent UUID + `quantity:0` | Biên số 0 |
| `negative_quantity` | Parent UUID + `quantity:-1` | Biên số âm |
| `missing_required_shopping_list_id` | `{}` | Thiếu required field |
| `invalid_uuid` | `{"shoppingListId":"not-a-uuid"}` | Sai định dạng UUID |

**Điểm nên cải tiến:** đối với subcase thiếu required/UUID sai, thêm explicit expected 422 sau khi được thầy phê duyệt; hiện test chỉ bảo đảm response thuộc **tập mã được khai báo**.

### TC-17 — Shopping Item lifecycle

- **API:** tạo parent list, `POST /api/households/shopping/items`, `GET/PUT/GET/DELETE/GET` theo item, cuối cùng DELETE parent list.
- **Input:** item ban đầu `quantity:1`, `checked:false`, `display` và `note` có `K05-P1-ITEM-<unique>`.
- **Expected:** parent POST 201; item POST 201 và `createdItems` có **đúng 1** phần tử; GET 200 xác minh `id`/`shoppingListId`; PUT 200 với `quantity:2`, `checked:true`, `note` updated; GET 200 xác minh các field; DELETE item 200; GET sau delete 404 (**T**); DELETE parent 200.
- **Actual (O):** tất cả assertion đạt, test PASS.
- **Verdict:** **PASS**. `TEST-05` là lỗi harness cũ (nhầm `createdItems[0].id` thành top-level id), đã được khắc phục, không phải defect của SUT.

### TC-18 — Shopping List empty object

- **API:** `POST /api/households/shopping/lists`; body `{}`.
- **Expected (C):** `{201,422}`; nếu `201`, response có `id` để cleanup. `ShoppingListCreate` **không có required fields**.
- **Actual (O):** assertion đạt, testcase PASS; XML chỉ xác nhận PASS, không cung cấp status riêng cho payload trong nội dung tổng hợp.
- **Verdict:** **PASS**. Không thể nói chắc test yêu cầu từ chối `{}`.

### TC-19 — Shopping List null name

- **API:** `POST /api/households/shopping/lists`; body `{"name":null}`.
- **Expected (C):** `{201,422}`; nullable theo schema; cleanup nếu tạo.
- **Actual (O):** testcase PASS.
- **Verdict:** **PASS**; không tự gán cụ thể 201 hay 422 khi log riêng không có.

### TC-20 — Shopping List empty name

- **API:** `POST /api/households/shopping/lists`; body `{"name":""}`.
- **Expected (C):** `{201,422}`; schema cho phép type string mà không có minLength.
- **Actual (O):** testcase PASS.
- **Verdict:** **PASS**; điều đó không chứng minh tên rỗng đã được chấp nhận hay phải bị từ chối.

### TC-21 — Shopping List lifecycle

- **API:** `POST /api/households/shopping/lists` → `GET/PUT/GET/DELETE/GET /api/households/shopping/lists/{item_id}`.
- **Input:** `{"name":"K05-P1-SHOPPING-LIST-<unique>"}`, PUT đổi tên thêm `-UPDATED` và giữ các server IDs trong current representation.
- **Expected:** POST 201 và có `id`; GET 200 đúng name; PUT 200; GET 200 với tên mới; DELETE 200; GET hậu xóa 404 theo **T**.
- **Actual (O):** tất cả assertion đạt.
- **Verdict:** **PASS**; cleanup thông qua DELETE và `finally` dự phòng.

---

## 5. Ma trận ngược: từ Requirement đến Test (Requirement Coverage)

Một requirement có thể được thử bởi nhiều test và một test có thể kiểm chứng nhiều requirement. **Coverage dưới đây là mức liên kết với bộ test**, không đồng nghĩa với coverage đầy đủ branch, dòng mã hay dữ liệu biên.

| Requirement | Mô tả rút gọn | Test liên kết | Mức bằng chứng hiện có |
|---|---|---|---|
| REQ-COM-01 | Method/path/body/required/schema | TC-01…09, 11…21 | P0 schema-generated + P1 directed; một số ràng buộc chưa có assertion chi tiết |
| REQ-COM-02 | Documented response status | TC-01…09, 11…21 | Có assertion/check; phát hiện DEF-01…04 |
| REQ-COM-03 | Response schema conformance | TC-01…09, 11 | **Có explicit Schemathesis check P0**; P1 phần lớn chỉ assert trường liên quan |
| REQ-COM-04 | Không undocumented 5xx | TC-01…09, 11, 14 | Có kiểm tra; gặp DEF-01/04 |
| REQ-COM-05 | Bearer authentication | TC-01…09, 11…21 | Token là precondition, **không phải test bảo mật** |
| REQ-COM-06 | Dữ liệu test-only và cleanup | TC-12…21 | Có trong code các P1 write scenarios |
| REQ-COM-07 | Post-delete absence, kỳ vọng 404 mức nhóm | TC-13,15,17,21 | Có direct assertion, **không có OpenAPI 404** |
| REQ-COM-08 | Đúng 9 GET và giới hạn P0 | TC-10; TC-01…09,11 | Có offline selection; smoke trùng GET Recipes |
| REQ-REC-01 | Recipe collection contract | TC-05,11 | FAIL/DEF-01 |
| REQ-REC-02 | Recipe detail contract | TC-09,15 | P0 FAIL/DEF-03; P1 GET tài nguyên thật PASS |
| REQ-REC-03 | Recipe create/read happy path | TC-15 | PASS |
| REQ-REC-04 | Recipe delete & post-delete verify | TC-15 | PASS, hậu xóa kỳ vọng T |
| REQ-REC-05 | Recipe empty name không trả undocumented 500 | TC-14 | FAIL/DEF-04 |
| REQ-REC-06 | Recipe filters, empty foods không gây 5xx | TC-05,11 | FAIL/DEF-01 |
| REQ-LST-01 | Shopping List collection | TC-01 | FAIL/DEF-02 |
| REQ-LST-02 | Shopping List detail | TC-06,21 | PASS theo cases đã thử |
| REQ-LST-03 | Shopping List create | TC-21 | PASS |
| REQ-LST-04 | Shopping List update | TC-21 | PASS |
| REQ-LST-05 | Shopping List delete | TC-21 | PASS, hậu xóa kỳ vọng T |
| REQ-LST-06 | Shopping List `{}`, null, empty name | TC-18,19,20 | 3 PASS về contract response set |
| REQ-ITM-01 | Shopping Item collection | TC-02 | FAIL/DEF-02 |
| REQ-ITM-02 | Shopping Item detail | TC-07,17 | PASS theo cases đã thử |
| REQ-ITM-03 | Item create trong parent list | TC-17 | PASS |
| REQ-ITM-04 | Item update quantity/checked/note | TC-17 | PASS |
| REQ-ITM-05 | Item delete + parent cleanup | TC-17 | PASS, hậu xóa kỳ vọng T |
| REQ-ITM-06 | Item create boundary 6 payloads | TC-16 | PASS về contract response set, **chưa biết acceptance từng input** |
| REQ-MLP-01 | Meal Plan collection | TC-03 | FAIL/DEF-02 |
| REQ-MLP-02 | Meal Plan today | TC-04 | PASS |
| REQ-MLP-03 | Meal Plan detail | TC-08,13 | P0 FAIL/DEF-03; lifecycle GET hợp lệ PASS |
| REQ-MLP-04 | Meal Plan create | TC-13 | PASS |
| REQ-MLP-05 | Meal Plan update | TC-13 | PASS |
| REQ-MLP-06 | Meal Plan delete | TC-13 | PASS, hậu xóa kỳ vọng T |
| REQ-MLP-07 | Meal Plan boundary 7 payloads | TC-12 | PASS; OBS-01 |

### 5.1 Coverage theo phạm vi

| Chỉ số | Giá trị | Cách hiểu |
|---|---:|---|
| Paths trong OpenAPI snapshot | 182 | Toàn hệ thống, **không** phải các path đã kiểm thử hết |
| Operations trong OpenAPI snapshot | 266 | Toàn hệ thống, **không** phải 266 cases |
| P0 GET operations được chọn và lịch sử có thực thi | **9/9** | Đúng phạm vi 9 operation GET; không phải full API coverage |
| P0 pytest items | **11** | 5 collection + 4 detail + 1 offline selection + 1 smoke |
| P1 pytest items | **10** | 4 lifecycle + 3 shopping-list boundary + 1 item boundary + 1 meal-plan boundary + 1 recipe defect reproducer |
| Tổng pytest items | **21** | 13 PASS, 8 FAIL, 0 SKIP |
| Miền nghiệp vụ P1 lifecycle | **4** | Lists, items, meal plans, recipes |
| Boundary/test reproducer payload groups | **4** | Meal Plan, Shopping Item, Shopping List, Recipe empty name |
| Defect families có hồ sơ | **4** | DEF-01…04, **không phải 8 defect độc lập** |

### 5.2 Những chức năng chưa được kiểm thử đầy đủ

- `PUT`/`PATCH` recipe dù có ở contract: `test_p1_recipe_lifecycle.py` hiện chỉ **create/read/delete**.
- Xác thực âm, quyền sở hữu và phân quyền household chưa nằm trong test campaign.
- Kiểm trường hợp invalid path ID có status dự kiến **404** được mô tả như contract extension cần phê duyệt; OpenAPI hiện chưa có.
- Shopping Item negative quantity/missing parent ID mới kiểm **status set** `{201,422}`; chưa có oracle nghiệp vụ chuyên biệt.
- Meal Plan title/recipeId cross-field validation ghi là **OBS-01**; cần tài liệu kinh doanh/chủ sở hữu xác nhận nếu biến thành REQ.
- Các endpoint ngoài bốn nhóm chính, bulk/asset/admin/auth/external vẫn ngoài scope.

---

## 6. Ma trận sai lệch: Expected → Actual → Defect

| Defect | Test liên quan | Minimal input / request | Expected theo snapshot | Actual lưu trong evidence | Phân loại / số lần tái hiện |
|---|---|---|---|---|---|
| **DEF-01** | TC-05, TC-11 | `GET /api/recipes?foods=` | `200` hoặc `422`; không 500 | `500 Internal Server Error` | Server error; **3/3**; RCA **LIKELY IMPLEMENTATION PATH**, chưa khẳng định chính xác exception bằng stack trace |
| **DEF-02** | TC-01, TC-02, TC-03 | `GET .../lists?orderBy=null`; tương tự items và mealplans | `200` hoặc `422`; không 400 | `400`, `Invalid order_by statement "null"` | OpenAPI/runtime mismatch; **9/9** trên 3 endpoint; RCA confirmed |
| **DEF-03** | TC-08, TC-09 | `GET /api/households/mealplans/0`; `GET /api/recipes/0` | `200` hoặc `422`; **404 không document** | `404` cho ID/slug không tồn tại | Omission trong response map; **6/6**; RCA confirmed |
| **DEF-04** | TC-14 | `POST /api/recipes` + `{"name":""}` | `201` hoặc `422`; không 500 | `500` + `AssertionError` | Invalid input/server error; **3/3**; RCA confirmed |

**Chú giải:** “Root cause confirmed” dựa trên hồ sơ source inspection đã có tại `evidence/defects`. Đây không phải bằng chứng rằng nhóm đã fix mã Mealie; đề tài kiểm thử và báo cáo lỗi, **không tuyên bố đã sửa lỗi trong sản phẩm**.

### 6.1 Sai lệch giữa oracle tổng quát và assertion lifecycle

| Điểm khác nhau | Oracle tổng quát hiện có | Mã lifecycle P1 | Hướng xử lý khi trình bày |
|---|---|---|---|
| GET tài nguyên sau khi xóa | `invariants-and-oracles.md`: không assert status 404 vì 404 chưa document | `test_p1_*_lifecycle.py` assert `after_delete.status_code == 404` | Ghi **T**: xác minh việc xóa qua runtime behavior, khác **C**: contract status map. Không che giấu mâu thuẫn |
| Recipe update/patch | Scenario gợi ý có thể update/patch | Recipe lifecycle thực tế không gọi PUT/PATCH | Trình bày đúng đã thử create/read/delete; đánh dấu gap |
| Item POST response | `ShoppingListItemsCollectionOut` là wrapper | Code lấy `createdItems[0].id` | Đã sửa TEST-05, không ghi SUT defect |
| Recipe POST response | `201` JSON string slug | Code nhận `response.json()` là string | Đã sửa TEST-06, không ghi SUT defect |

---

## 7. Mẫu thực thi và thu thập bằng chứng cho lần chạy kế tiếp

> Chỉ sử dụng trên môi trường QA local. Không ghi token vào log/README/commit. Các lệnh dưới đây là **hướng dẫn**, không khẳng định đã chạy lại khi tạo tài liệu này.

```powershell
cd D:\R02-K05-Mealie-QA
.\.venv\Scripts\Activate.ps1

# Nhập ở terminal riêng, không ghi vào repository
$env:MEALIE_API_TOKEN = Read-Host "Nhap API Token"
$env:MEALIE_BASE_URL = "http://localhost:9091"

# Kiem tra cau hinh offline (TC-10)
python -m pytest tests/schemathesis/test_p0_selection.py -v

# Chay P0 doc du lieu
python -m pytest tests/schemathesis/test_p0_collections.py tests/schemathesis/test_p0_details.py tests/schemathesis/test_p0_smoke.py -v -rs

# Chay P1 co kiem soat; can QA data rieng va cleanup
python -m pytest tests/schemathesis/test_p1_mealplan_boundaries.py tests/schemathesis/test_p1_mealplan_lifecycle.py tests/schemathesis/test_p1_recipe_lifecycle.py tests/schemathesis/test_p1_shopping_item_boundaries.py tests/schemathesis/test_p1_shopping_item_lifecycle.py tests/schemathesis/test_p1_shopping_list_boundaries.py tests/schemathesis/test_p1_shopping_list_lifecycle.py -v -rs

# Reproducer DEF-04 co chu dich - expected FAIL theo baseline cu
python -m pytest tests/schemathesis/test_p1_recipe_empty_name.py -v -s

# Full run va xuat bao cao JUnit
python -m pytest tests -v -rs --junitxml=reports/test-results.xml
```

**Cảnh báo thao tác:** lệnh `--junitxml=reports/test-results.xml` **ghi đè** file báo cáo lịch sử. Trước khi chạy, hãy lưu/đổi tên baseline evidence cũ (ví dụ `test-results-baseline-20261002.xml`) rồi mới tạo báo cáo phiên mới. Nếu FAIL vì không có token, Docker dừng, cleanup lỗi hay timeout, ghi đó là **BLOCKED/ENV** trước khi kết luận sai lệch SUT.

### 7.1 Mẫu nhật ký thực thi mới

| Execution ID | Test ID | Timestamp / snapshot | Input hash hoặc request rút gọn | Expected (C/T) | Actual | Verdict | Evidence | Reviewer |
|---|---|---|---|---|---|---|---|---|
| RUN-YYYYMMDD-01 | TC-14 | *Điền khi chạy* | `POST /api/recipes` + `name=""` | `{201,422}` | *Điền khi chạy* | *Chưa xác định* | File log/JUnit mới | *Nhóm điền* |

Không copy cột actual `500` từ evidence lịch sử vào dòng chạy mới nếu chưa thực thi thật. Chỉ có thể ghi **historical baseline = 500 (3/3)** trong một cột riêng.

### 7.2 Phân loại sau khi chạy

1. So khớp version/snapshot và token: không đúng → ENV/CFG hoặc BLOCKED.
2. Kiểm lại test input, assertions, dữ liệu QA và cấu trúc JSON: nếu test hiểu sai contract → TEST issue (như TEST-05/TEST-06).
3. Nếu response status/schema không đúng C → contract mismatch hoặc server defect tùy bằng chứng.
4. Nếu response đúng C nhưng khác team rule T → business expectation review, chưa gọi là defect của API contract.
5. Rút gọn input tối thiểu; chạy lại có kiểm soát; ghi số lần tái hiện, log, source-level RCA mức phù hợp.
6. Liên kết vào một **defect family duy nhất** và ghi các test cùng bị ảnh hưởng.

---

## 8. Các câu cần giải thích trong buổi báo cáo

**Hỏi: Vì sao nhóm chọn 21 test?**  
Vì bốn chức năng tạo một chuỗi sử dụng điển hình của Mealie (công thức – danh sách – mặt hàng – kế hoạch). Bộ test cân bằng P0 GET contract/schema fuzz, P1 vòng đời nghiệp vụ và boundary validation. Con số 21 xuất phát từ số pytest items thực sự thu thập, **không phải một số được quy định sẵn**.

**Hỏi: Dùng tài liệu nào làm expected?**  
Dùng snapshot OpenAPI và oracle có căn cứ làm lớp **C**. Một số giá trị kỳ vọng ở vòng đời (đặc biệt GET sau DELETE trả 404) là **T**, cần báo rõ là giả định kiểm thử bổ sung của nhóm và có thể xin thầy phê duyệt.

**Hỏi: Tại sao 8 FAIL nhưng chỉ có 4 lỗi?**  
Nhiều test kích hoạt cùng một họ lỗi. Ba collection cùng liên hệ DEF-02; hai detail cùng DEF-03; Recipe collection/smoke cùng DEF-01; test empty-name riêng DEF-04. Vì thế **không lấy số FAIL làm số defect**.

**Hỏi: PASS của boundary có chứng minh đầu vào bị từ chối đúng chưa?**  
Chưa chắc. Với Item/Meal Plan/List, một số test chỉ khẳng định status nằm trong `{201,422}` và dữ liệu tạo được dọn sạch. Muốn chứng minh một dữ liệu cụ thể nhất định phải bị từ chối, cần đặc tả nghiệp vụ rõ ràng + assertion chặt cho từng subcase.

**Hỏi: Nhóm đã có đặc tả rồi mới kiểm thử chưa?**  
Nhóm đã có **OpenAPI snapshot và oracle O1–O8** làm cơ sở ban đầu; hai file đặc tả và ma trận này là bước **chuẩn hóa tài liệu** sau khi có triển khai/đợt thực thi đã lưu. Để chứng minh quy trình đúng ý thầy, từ lần tới hãy **chốt version đặc tả trước**, duyệt expected, chạy tests, ghi actual vào cột riêng và quản lý thay đổi bằng Git.

---

## 9. Checklist chất lượng trước khi nộp/đi gặp thầy

- [ ] Đặc tả `MEALIE-FUNCTIONAL-SPECIFICATION.md` và RTM cùng version; mở trực tiếp được các link tương đối sau khi chép vào đúng folder.
- [ ] Có đủ TC-01…TC-21; tên bài test, method/path và kết quả khớp JUnit XML.
- [ ] Phân biệt rõ source-of-truth OpenAPI (**C**), kỳ vọng tự đặt của nhóm (**T**) và hành vi thực tế (**O**).
- [ ] Báo đúng 13 PASS, 8 FAIL, 0 SKIP ở **historical run**; không tuyên bố chạy lại nếu không có bằng chứng mới.
- [ ] Bốn DEF-ID liên kết đúng bằng chứng tái hiện, không đếm trùng.
- [ ] Công khai test gaps: Recipe PUT/PATCH, negative auth, expected từng boundary case, thiếu 404 trong contract.
- [ ] Không lưu bearer token/credentials; cleanup child trước parent.
- [ ] Chốt những quy tắc nghiệp vụ bổ sung với giảng viên nếu được yêu cầu, rồi mới đóng băng expected để chạy lại.

---

## 10. Tài liệu liên quan

- [Đặc tả chức năng cho bốn module](../specification/MEALIE-FUNCTIONAL-SPECIFICATION.md)
- [OpenAPI snapshot](../../schema/snapshots/mealie-v3.28.0-openapi.json)
- [Phạm vi kiểm thử](test-scope.md)
- [Oracle O1–O8](invariants-and-oracles.md)
- [Test scenarios](test-scenarios.md)
- [Business flows](business-flows.md)
- [Test Inventory and Coverage](../../reports/summarized/Test-Inventory-and-Coverage.md)
- [P1 lifecycle summary](../../reports/summarized/Phase-3-P1-Lifecycle-Summary.md)
- [Báo cáo JUnit XML](../../reports/test-results.xml)
- [Evidence DEF-01](../../evidence/defects/DEF-01-recipe-empty-foods-500.md)
- [Evidence DEF-02](../../evidence/defects/DEF-02-orderby-null-undocumented-400.md)
- [Evidence DEF-03](../../evidence/defects/DEF-03-undocumented-404.md)
- [Evidence DEF-04](../../evidence/defects/DEF-04-empty-recipe-name-500.md)

**Kết luận:** Mọi test ID đều có đích truy vết về REQ, và mọi kết quả FAIL đều có nhóm defect/evidence tương ứng. Những điều chưa chứng minh được đánh dấu rõ là *test gap, contract gap hoặc team-level expectation*, thay vì bị trình bày là chức năng đã được kiểm thử toàn diện.

---

## 11. Bổ sung TC-22…TC-37 – implementation tracking

Phụ lục này bổ sung traceability cho 16 pytest item mới. Nó không sửa dữ liệu historical TC-01…TC-21. Expected **C** là response map trong snapshot `mealie-v3.28.0-openapi.json`; Expected **T** chỉ được assert có điều kiện sau một response thành công theo C.

| Test ID | Requirement IDs | File pytest | Implementation | Actual / Verdict |
|---|---|---|---|---|
| TC-22 | REQ-LST-03/06, REQ-COM-02/06 | `test_tc22_tc25_shopping_lists.py` | IMPLEMENTED | PASS |
| TC-23 | REQ-LST-03, REQ-COM-02/03/06 | `test_tc22_tc25_shopping_lists.py` | IMPLEMENTED | PASS |
| TC-24 | REQ-LST-02/04, REQ-COM-02/06 | `test_tc22_tc25_shopping_lists.py` | IMPLEMENTED | FAIL — 404, DEF-03 extension |
| TC-25 | REQ-LST-05, REQ-COM-02/06/07 | `test_tc22_tc25_shopping_lists.py` | IMPLEMENTED | FAIL — second DELETE 404, DEF-03 extension |
| TC-26 | REQ-MLP-01, REQ-COM-02/03/04 | `test_tc26_tc29_mealplans.py` | IMPLEMENTED | PASS |
| TC-27 | REQ-MLP-05, REQ-COM-06 | `test_tc26_tc29_mealplans.py` | IMPLEMENTED | PASS |
| TC-28 | REQ-MLP-06, REQ-COM-02/06 | `test_tc26_tc29_mealplans.py` | IMPLEMENTED | FAIL — DELETE missing ID 404, DEF-03 extension |
| TC-29 | REQ-MLP-05/07, REQ-COM-02/06 | `test_tc26_tc29_mealplans.py` | IMPLEMENTED | PASS |
| TC-30 | REQ-ITM-04/06, REQ-COM-02/06 | `test_tc30_tc33_shopping_items.py` | IMPLEMENTED | PASS |
| TC-31 | REQ-ITM-03/06, REQ-COM-02/06 | `test_tc30_tc33_shopping_items.py` | IMPLEMENTED | FAIL — 500, DEF-05 candidate |
| TC-32 | REQ-ITM-04, REQ-COM-06 | `test_tc30_tc33_shopping_items.py` | IMPLEMENTED | PASS |
| TC-33 | REQ-ITM-03/04/05, REQ-COM-06 | `test_tc30_tc33_shopping_items.py` | IMPLEMENTED | PASS |
| TC-34 | REQ-REC-03/04, REQ-COM-02/06 | `test_tc34_tc37_recipes.py` | IMPLEMENTED | FAIL — partial PUT 500, DEF-06 candidate |
| TC-35 | REQ-REC-03/04, REQ-COM-02/06 | `test_tc34_tc37_recipes.py` | FIXED, VERIFIED | PASS — returned slug used after PATCH; TEST-07 resolved |
| TC-36 | REQ-REC-05, REQ-COM-02/04/06 | `test_tc34_tc37_recipes.py` | IMPLEMENTED | FAIL — whitespace POST 400, DEF-07 candidate |
| TC-37 | REQ-REC-03/05, REQ-COM-02/04/06 | `test_tc34_tc37_recipes.py` | IMPLEMENTED | PASS |

`pytest --collect-only -q` verified 37 items (21 historical + 16 new). The retained 2026-10-22 expansion JUnit records 9 PASS / 7 FAIL. The post-fix JUnit `reports/local-runs/tc22-tc37-20261023-215442-705.xml` records 10 PASS, 6 FAIL, 0 SKIP, 0 ERROR and verifies TC-35. These campaigns do not replace historical TC-01…TC-21 evidence. A post-run marker audit found two historical TC-35 recipes, deleted only those verified test resources with HTTP 200, and confirmed zero remaining `K05-TC-` resources across the four expansion areas.
