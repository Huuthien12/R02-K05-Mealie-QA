# ĐẶC TẢ CHỨC NĂNG VÀ HỢP ĐỒNG API PHỤC VỤ KIỂM THỬ MEALIE

> **Mã tài liệu:** R02-K05-FS-01  
> **Dự án:** R02-K05-Mealie-QA · **Phiên bản tài liệu:** 1.0 (bản lập từ baseline đã lưu)  
> **Hệ thống được kiểm thử (SUT):** Mealie v3.28.0; commit `0552eaa4a80031b8572849cca0ed95d07f1be001`  
> **Hợp đồng gốc:** `schema/snapshots/mealie-v3.28.0-openapi.json`, OpenAPI 3.1.0  
> **Môi trường tham chiếu:** `http://localhost:9091` · **Kỹ thuật:** API contract testing, schema-based/property-based testing, kiểm thử luồng và giá trị biên  
> **Trạng thái tài liệu:** *Đặc tả kiểm thử do nhóm tổng hợp*, không phải tài liệu yêu cầu chính thức do tác giả Mealie phê duyệt.

---

## 1. Mục đích, nguyên tắc và giới hạn

Tài liệu này xác định **các điều kiện và hành vi mong đợi dùng làm căn cứ kiểm thử trước khi đối chiếu với kết quả thực thi**. Nội dung được xây dựng từ snapshot OpenAPI đã lưu, tài liệu phân tích của nhóm, kịch bản P0/P1 và các assertion tồn tại trong mã kiểm thử. Báo cáo kết quả chạy và defect **không được dùng để sửa ngược tiêu chí mong đợi nhằm biến FAIL thành PASS**.

**Phân biệt ba tầng căn cứ:**

| Ký hiệu | Mức căn cứ | Được hiểu là | Ví dụ |
|---|---|---|---|
| **C** | Contract / OpenAPI | Ràng buộc có thể xác minh trực tiếp bằng operation, parameter, schema hoặc response map trong snapshot | `POST /api/recipes` khai báo `201`, `422`; body `CreateRecipe.name` là chuỗi bắt buộc |
| **T** | Team / Test rule | Quy tắc thử nghiệm bổ sung do nhóm xác định, chỉ áp dụng cho những scenario chỉ định; không mạo nhận là OpenAPI | Dữ liệu tạo bởi test phải được dọn; GET sau DELETE kỳ vọng không tìm lại tài nguyên và test hiện tại assert `404` |
| **O** | Observation / Actual | Hành vi quan sát trong lần thực thi được lưu làm bằng chứng; **không tự động thành đặc tả đúng** | `GET /api/recipes?foods=` đã trả `500` |

**Quy tắc ưu tiên:** (1) kiểm tra đúng version và đúng operation; (2) xác nhận chuẩn C; (3) nêu rõ T nếu cần xác minh trạng thái nghiệp vụ; (4) ghi O và phân loại sai lệch. Nếu OpenAPI chưa nói rõ giá trị nào phải được chấp nhận, **không tự gán** HTTP 422 cho mọi dữ liệu lạ; trước tiên so với các response có khai báo và xem lại yêu cầu nghiệp vụ.

### 1.1 Phạm vi

Bốn miền chức năng trong phạm vi: **Recipe (công thức), Shopping List (danh sách mua sắm), Shopping Item (mặt hàng), Meal Plan (kế hoạch bữa ăn)**. P0 bao phủ 9 operation `GET` được phép đọc; P1 bao phủ những đường dẫn `POST`, `GET`, `PUT`, `DELETE` có dữ liệu tạm do test tạo. Snapshot có **182 paths, 266 operations**, nhưng tài liệu này **không tuyên bố** bao phủ mọi operation.

Ngoài phạm vi: xác thực/đổi mật khẩu/tạo token, quản trị, sao lưu, import/export, image/upload, bulk, webhook, luồng stream, dịch vụ ngoài, hệ thống public và các hành động có nguy cơ phá hủy dữ liệu không do test tạo. Mục đích giới hạn là tránh can thiệp tài khoản, dữ liệu nền và tài nguyên ngoài.

### 1.2 Thuật ngữ

- **SUT:** System Under Test — hệ thống Mealie đang được kiểm thử.
- **Contract:** hợp đồng API mô tả cách gửi yêu cầu và các đáp ứng được khai báo.
- **Schema:** cấu trúc/kiểu dữ liệu JSON, không đồng nghĩa với toàn bộ quy tắc nghiệp vụ.
- **Oracle:** quy tắc dùng đánh giá PASS/FAIL.
- **P0/P1:** nhóm ưu tiên kiểm thử; P0 đọc không thay đổi dữ liệu, P1 ghi có kiểm soát.
- **Collection/Detail:** API lấy nhiều bản ghi / lấy một bản ghi theo định danh.
- **Lifecycle:** chuỗi tạo → đọc → cập nhật (nếu test có) → xác minh → xóa.
- **Boundary:** đầu vào ở biên như `{}`, `null`, `""`, số 0, số âm, định dạng sai.
- **Defect:** sai lệch đã điều tra có bằng chứng; **một FAIL chưa mặc nhiên là một defect mới**.

---

## 2. Nguồn đặc tả và khả năng truy vết

| Mã nguồn | File trong repository | Sử dụng để |
|---|---|---|
| SRC-01 | `schema/snapshots/mealie-v3.28.0-openapi.json` | Source of truth cho các operation, required fields, kiểu dữ liệu, response codes và JSON schema (**C**) |
| SRC-02 | `docs/analysis/system-analysis.md`, `docs/analysis/api-analysis.md` | Lựa chọn chức năng chính, sơ đồ phạm vi, phân tích rủi ro |
| SRC-03 | `docs/test-design/test-scope.md` | Mức ưu tiên P0/P1 và loại trừ API không an toàn |
| SRC-04 | `docs/test-design/invariants-and-oracles.md` | O1–O8 làm chuẩn hợp đồng và dọn dữ liệu |
| SRC-05 | `docs/test-design/test-scenarios.md`, `docs/test-design/business-flows.md` | Luồng đọc dữ liệu, vòng đời danh sách, mặt hàng, kế hoạch và công thức |
| SRC-06 | `tests/schemathesis/test_p0_*.py`, `tests/schemathesis/test_p1_*.py` | Kỹ thuật triển khai và assertion hiện có; dùng để xác định **mức thực sự đã kiểm thử** |
| SRC-07 | `reports/test-results.xml`, `reports/final/FINAL-RESULTS.md` | Bằng chứng thực tế (O), **không phải** nguồn của expected result |
| SRC-08 | `evidence/defects/DEF-01-*.md` … `DEF-04-*.md` | Tái hiện và phân loại sai lệch so với contract |

**Kiểm soát thay đổi đặc tả:** Khi phát hiện quy tắc nghiệp vụ mới, đề xuất thay đổi với lý do + nguồn, người duyệt và version; không thay quy tắc cũ chỉ vì kết quả không đạt. Nếu thầy yêu cầu đặc tả tiên nghiệm nghiêm ngặt, cần ghi rõ tài liệu này được **chuẩn hóa sau khi dự án đã có các test và evidence**, và dùng nó làm baseline cho **các lần chạy tiếp theo**. Không tuyên bố hai file này đã tồn tại trước lần test lịch sử.

---

## 3. Môi trường, tiền điều kiện và dữ liệu test

### 3.1 Baseline

- Mealie **v3.28.0** (source pinned bằng tag/commit), triển khai local bằng Docker/Compose.
- API base URL mặc định `http://localhost:9091` (biến môi trường `MEALIE_BASE_URL`).
- Python 3.11.9, pytest và Schemathesis 4.28.0 theo hồ sơ dự án; file `tests/requirements.txt` quyết định dependency của bộ test.
- Token Bearer cung cấp qua `MEALIE_API_TOKEN` tại thời điểm chạy. Không ghi token vào tài liệu, commit, screenshot hoặc artifact.
- Snapshot OpenAPI dùng **bản đã chốt** tại SRC-01 thay vì lấy schema thay đổi bất ngờ từ máy chủ.
- Thực thi P0 trước; P1 chỉ trên cơ sở dữ liệu QA có thể dọn sạch.

### 3.2 Dữ liệu chuẩn bị

1. Có tài khoản thử nghiệm hợp lệ có quyền truy cập household chứa dữ liệu QA.
2. P0 dùng các truy vấn có thể gọi ngay, không tạo dữ liệu; test GET detail được phép thử định danh không tồn tại để đánh giá xử lý lỗi.
3. P1 tạo tên duy nhất theo tiền tố `K05-P1-*` cộng chuỗi ngẫu nhiên; **không sửa/xóa fixture hoặc dữ liệu thật**.
4. Item phải có một Shopping List cha được tạo tạm; dọn item trước, sau đó dọn list.
5. Meal Plan tạo tại ngày tương lai để giảm va chạm với kế hoạch hiện hành; lấy các trường ID cần thiết từ response máy chủ.
6. Khi chạy lại suite, xác nhận trạng thái fixture và chụp bằng chứng environment/command/summary trước và sau.

### 3.3 Điều kiện đầu vào và đầu ra chung

| Mã | Đặc tả kiểm thử | Căn cứ |
|---|---|---|
| REQ-COM-01 | Gọi đúng method/path, đúng loại path/query/body; các trường required phải tuân theo schema; khi không tuân thủ phải được ghi nhận là negative/boundary test | C |
| REQ-COM-02 | Mỗi API trong phạm vi có response status thuộc response map được khai báo; kiểm tra theo từng operation, không áp đặt tất cả là HTTP 200 | C / oracle O1 |
| REQ-COM-03 | Khi response có JSON schema được khai báo, body phải thỏa schema tương ứng; không yêu cầu schema đối với response không khai báo một kiểu JSON cụ thể | C / O2 |
| REQ-COM-04 | Các bài schema fuzzing không được gặp lỗi máy chủ 5xx không có trong hợp đồng; `422` chỉ được coi hợp lệ khi operation khai báo `422` | C / O3–O4 |
| REQ-COM-05 | Các protected endpoints được gọi bằng OAuth2 Bearer hợp lệ. Thiếu token được coi là **SKIP/cấu hình không đủ**, không phải test chức năng PASS/FAIL | C / O6 / T |
| REQ-COM-06 | Chỉ cập nhật/xóa dữ liệu do chính test tạo; lưu `id`/`slug` và chạy cleanup trong `finally` nếu có thể | T / O8 |
| REQ-COM-07 | Đối với các kịch bản lifecycle đã triển khai, các lần GET sau DELETE được nhóm kỳ vọng `404` như xác nhận tài nguyên không còn; đây là **assertion bổ sung T**, **không phải response được OpenAPI GET công bố** | T, cần tách khỏi C |
| REQ-COM-08 | Test P0 dùng giới hạn số ví dụ; tập P0 có đúng 9 GET operations; không fuzz ngẫu nhiên các operation có side effect | T / SRC-03/06 |

**Lưu ý quan trọng về `null` trong URL:** Query parameter có `string | null` không đồng nghĩa với chuỗi ký tự `"null"` được máy chủ hiểu như JSON `null`. Trong DEF-02, literal `orderBy=null` bị parser coi là chuỗi giá trị sắp xếp và trả 400. Tài liệu ghi **sai lệch response map** và chênh lệch diễn giải serialization, không khẳng định máy chủ bắt buộc phải chấp nhận literal `null` làm giá trị sắp xếp.

---

## 4. Đặc tả chức năng Recipes

**Chức năng:** truy vấn danh sách công thức, truy vấn bằng slug, tạo công thức từ tên, đọc lại và xóa công thức thử nghiệm. `PUT`/`PATCH` có mặt trong OpenAPI nhưng **bài lifecycle hiện tại không thực hiện cập nhật Recipe**.

### 4.1 API và contract

| Operation | Đầu vào then chốt | Response khai báo | Ghi chú |
|---|---|---|---|
| `GET /api/recipes` | Các filter `categories`, `tags`, `foods`, `households`, `search`, `orderBy`...; `page` mặc định 1, `perPage` mặc định 50 | `200`, `422` | P0 collection, schema fuzz và smoke |
| `GET /api/recipes/{slug}` | `slug` là string path bắt buộc | `200`, `422` | P0 detail và P1 GET |
| `POST /api/recipes` | Body `CreateRecipe`, bắt buộc `name: string`; schema **không đặt `minLength: 1`** | `201`, `422` | 201 body là **JSON string slug**, không phải full Recipe object |
| `DELETE /api/recipes/{slug}` | `slug` string path | `200`, `422` | P1 cleanup |
| `PUT/PATCH /api/recipes/{slug}` | `Recipe-Input` | `200`, `422` | Trong phạm vi quan sát contract, **chưa có case thực thi tương ứng** |

### 4.2 Yêu cầu chức năng

| Mã | Nội dung expected result | Căn cứ | Test liên quan |
|---|---|---|---|
| REQ-REC-01 | GET collection theo các tham số do OpenAPI mô tả phải cho response phù hợp với mã trạng thái đã khai báo và, nếu có, schema JSON 200/422; không có 5xx undocumented | C | TC-05, TC-11 |
| REQ-REC-02 | GET recipe bằng slug string; response phải đúng contract GET. Không tự giả định 404 là status được khai báo | C | TC-09, TC-15 |
| REQ-REC-03 | POST với `name` là chuỗi có nội dung và duy nhất; trong happy path nhóm mong `201`, response là chuỗi slug không rỗng; GET theo slug trả recipe có `name` và `slug` khớp | C + T (happy path) | TC-15 |
| REQ-REC-04 | DELETE recipe do test tạo trả mã thành công được khai báo; test xác nhận không tìm lại recipe bằng GET sau xóa và kỳ vọng 404 trong runtime hiện tại | C + T (post-delete) | TC-15 |
| REQ-REC-05 | POST body `{"name":""}` phải không phát sinh status `500` undocumented; theo snapshot response phải thuộc `{201,422}`. **Không khẳng định 422 bắt buộc**, vì schema chỉ yêu cầu string mà không có `minLength` | C / O3–O4 | TC-14 |
| REQ-REC-06 | Các filter `foods` rỗng hoặc biến thể query do Schemathesis sinh không được gây 5xx undocumented; các response khác phải được phân loại theo contract | C | TC-05, TC-11 |

### 4.3 Ví dụ minh họa đặc tả

```http
POST /api/recipes
Authorization: Bearer <TEST_TOKEN>
Content-Type: application/json

{"name":"K05 P1 Recipe <unique>"}
```

**Expected (REQ-REC-03):** `201`, JSON string như `"k05-p1-recipe-..."`; tiếp theo `GET /api/recipes/{slug}` nhận `200`, tên recipe bằng tên vừa tạo. Chuỗi slug minh họa, không phải giá trị cố định.

```http
POST /api/recipes
Authorization: Bearer <TEST_TOKEN>
Content-Type: application/json

{"name":""}
```

**Expected theo hợp đồng:** response thuộc `{201,422}` và không có `500` undocumented; nên **đề xuất** tác giả Mealie quy định rõ empty name bị từ chối, nhưng đó là **kiến nghị ngoài OpenAPI hiện tại**, không áp đặt là yêu cầu chính thức. Actual và DEF-04 nằm ở ma trận, **không đưa vào expected**.

---

## 5. Đặc tả chức năng Shopping Lists

**Chức năng:** liệt kê shopping lists, xem một list theo ID, tạo list, đổi tên, xóa list; thử payload rỗng/null để xác minh response contract.

### 5.1 API và contract

| Operation | Đầu vào | Response khai báo | Đặc điểm |
|---|---|---|---|
| `GET /api/households/shopping/lists` | `orderBy`, `orderDirection`, `page`, `perPage`, ... | `200`, `422` | Collection có pagination/filter |
| `GET /api/households/shopping/lists/{item_id}` | `item_id` string path, required | `200`, `422` | Detail |
| `POST /api/households/shopping/lists` | `ShoppingListCreate`: `name` là `string | null`, **không required**; `extras` optional | `201`, `422` | Trả `ShoppingListOut` |
| `PUT /api/households/shopping/lists/{item_id}` | `ShoppingListUpdate` yêu cầu `groupId`, `userId`, `id` | `200`, `422` | Nên dùng representation GET để dựng body |
| `DELETE /api/households/shopping/lists/{item_id}` | `item_id` | `200`, `422` | Chỉ xóa list test-created |

`ShoppingListOut` yêu cầu các trường `groupId`, `userId`, `id`, `householdId`; không đặt giả định rằng `name` luôn khác null hoặc khác rỗng vì schema không có ràng buộc đó.

### 5.2 Yêu cầu

| Mã | Nội dung expected result | Căn cứ | Test |
|---|---|---|---|
| REQ-LST-01 | GET collection thỏa documented status/response schema; các query bất thường như `orderBy` sẽ được kiểm tra đúng contract | C | TC-01 |
| REQ-LST-02 | GET detail nhận path `item_id` kiểu chuỗi; response đáp ứng contract GET, không tự gắn 404 là documented | C | TC-06, TC-21 |
| REQ-LST-03 | POST list tên duy nhất thành công trả `201 ShoppingListOut`; `id` và các field required có mặt, `name` khớp giá trị tạo | C + T | TC-21 |
| REQ-LST-04 | PUT chỉ trên list do test tạo; cập nhật tên bằng payload có `groupId`, `userId`, `id`; GET sau PUT phản ánh tên mới | C + T | TC-21 |
| REQ-LST-05 | DELETE list thử nghiệm trả documented success, GET sau xóa không còn tài nguyên, nhóm assert `404` (**team rule**) | C + T | TC-21 |
| REQ-LST-06 | `POST {}`, `POST {"name":null}` và `POST {"name":""}` phải trả documented `201` hoặc `422`; nếu `201`, response có `id` để cleanup | C | TC-18/19/20 |

### 5.3 Dữ liệu ranh giới

| Payload | Tại sao thử | Expected theo test hiện tại |
|---|---|---|
| `{}` | `ShoppingListCreate` không có required fields | Status `201` hoặc `422`; nếu tạo thành công phải có `id` |
| `{"name":null}` | Kiểm tra nullable field | Status `201` hoặc `422`; nếu tạo thành công phải có `id` |
| `{"name":""}` | Kiểm tra chuỗi rỗng không bị ép là tên hợp lệ | Status `201` hoặc `422`; nếu tạo thành công phải có `id` |

**Không quy định** ba payload bắt buộc phải nhận `422`, bởi đó sẽ vượt quá ràng buộc schema gốc. Thử nghiệm kiểm tra tính nhất quán với response map, không kiểm chứng đầy đủ chính sách nghiệp vụ về tên list.

---

## 6. Đặc tả chức năng Shopping Items

**Chức năng:** lấy tập item, xem chi tiết, thêm item vào list đã tồn tại, cập nhật số lượng/trạng thái và xóa item.

### 6.1 API và contract

| Operation | Đầu vào | Response khai báo | Chú ý |
|---|---|---|---|
| `GET /api/households/shopping/items` | Query/filter/page/order | `200`, `422` | 200 có dạng pagination `ShoppingListItemPagination`, yêu cầu `items` |
| `GET /api/households/shopping/items/{item_id}` | `item_id` required string | `200`, `422` | Detail |
| `POST /api/households/shopping/items` | `ShoppingListItemCreate`; **required** `shoppingListId: uuid4`; `quantity` number mặc định 1; `checked` boolean mặc định false; `display` string mặc định `""` | `201`, `422` | Body thành công: `ShoppingListItemsCollectionOut`; item tạo ra nằm trong `createdItems[]` |
| `PUT /api/households/shopping/items/{item_id}` | `ShoppingListItemUpdate`; **required** `shoppingListId` | `200`, `422` | Update trạng thái/quantity/note |
| `DELETE /api/households/shopping/items/{item_id}` | ID | `200`, `422` | Xóa child trước parent |

### 6.2 Yêu cầu

| Mã | Nội dung expected result | Căn cứ | Test |
|---|---|---|---|
| REQ-ITM-01 | GET collection trả response phù hợp contract, body nếu `200` có cấu trúc pagination và `items` | C | TC-02 |
| REQ-ITM-02 | GET detail theo item ID trả documented status/schema; nếu truy vấn item QA vừa tạo, `id` và `shoppingListId` phải khớp | C + T | TC-07, TC-17 |
| REQ-ITM-03 | Tạo list cha trước; `POST` item chứa `shoppingListId` của cha, mong `201`; lấy item vừa tạo từ `createdItems[0]` với `id` và parent đúng | C + T | TC-17 |
| REQ-ITM-04 | PUT item QA với `quantity=2`, `checked=true`, `note` mới; GET xác minh các trường được lưu đúng | C + T | TC-17 |
| REQ-ITM-05 | DELETE item QA trước khi delete list; trong testcase nhóm kiểm tra GET sau xóa là 404 (**team rule**), sau đó cleanup list cha | C + T | TC-17 |
| REQ-ITM-06 | Payload biên: tối thiểu hợp lệ, optional null, zero/negative quantity, thiếu `shoppingListId`, UUID sai — kết quả thuộc `{201,422}`; nếu 201 phải dọn `createdItems` | C (status), T (cleanup) | TC-16 |

### 6.3 Sáu trường hợp con của TC-16

| Case | Body minh họa | Ý nghĩa | Quy tắc kiểm tra |
|---|---|---|---|
| `minimal_valid` | `{"shoppingListId":"<uuid-cha>"}` | Required field | 201/422 |
| `null_optional_fields` | `shoppingListId` hợp lệ, `food`, `unit`, `note`, `foodId`, `labelId`, `unitId` = null | Nullability | 201/422 |
| `zero_quantity` | `shoppingListId`, `quantity:0` | Ranh giới số 0 | 201/422 |
| `negative_quantity` | `shoppingListId`, `quantity:-1` | Ranh giới số âm | 201/422 |
| `missing_required_shopping_list_id` | `{}` | Thiếu required | 201/422 theo assertion đang dùng; nên mở rộng để xác định riêng 422 nếu chuẩn hóa negative validation |
| `invalid_uuid` | `{"shoppingListId":"not-a-uuid"}` | Sai định dạng UUID | 201/422 theo assertion hiện tại; nên bổ sung schema-response checks |

**Giới hạn của test hiện tại:** `test_p1_shopping_item_create_boundaries.py` chỉ assert status thuộc `{201,422}`; **không chứng minh** `quantity=-1` bị từ chối, cũng không khẳng định `missing_required_shopping_list_id` chắc chắn trả 422. Tránh diễn giải PASS thành “nghiệp vụ giá trị biên hoàn toàn đúng”.

---

## 7. Đặc tả chức năng Meal Plans

**Chức năng:** liệt kê kế hoạch, xem kế hoạch hôm nay, xem detail theo ID số nguyên, tạo/cập nhật/xóa entry và thử biên request tạo.

### 7.1 API và contract

| Operation | Đầu vào | Response khai báo | Đặc điểm |
|---|---|---|---|
| `GET /api/households/mealplans` | `start_date`, `end_date`, filter/page/order | `200`, `422` | P0 collection |
| `GET /api/households/mealplans/today` | Không có required query riêng | `200`, `422` | P0 hôm nay |
| `GET /api/households/mealplans/{item_id}` | Path `item_id: integer` required | `200`, `422` | P0 detail; ID `0` là case không tồn tại của nhóm |
| `POST /api/households/mealplans` | `CreatePlanEntry`, required `date` định dạng `date`; `entryType` mặc định `breakfast`, `title`/`text` mặc định chuỗi rỗng, `recipeId` nullable UUID | `201`, `422` | `201 ReadPlanEntry` |
| `PUT /api/households/mealplans/{item_id}` | `UpdatePlanEntry`, required `date`, `id`, `groupId`, `userId` | `200`, `422` | Không tự bịa group/user ID |
| `DELETE /api/households/mealplans/{item_id}` | `item_id` integer | `200`, `422` | Cleanup |

`ReadPlanEntry` required: `date`, `id`, `groupId`, `userId`, `householdId`.

### 7.2 Yêu cầu

| Mã | Nội dung expected result | Căn cứ | Test |
|---|---|---|---|
| REQ-MLP-01 | GET collection kiểm tra response status/schema được khai báo, với các tham số thời gian và sắp xếp | C | TC-03 |
| REQ-MLP-02 | GET today trả documented status; nếu 200 phải theo content contract khi có schema tương ứng; không ép giả định số bữa ăn | C | TC-04 |
| REQ-MLP-03 | GET detail với integer `item_id` trả documented status; đặc biệt khi không tìm thấy, response 404 hiện **chưa nằm trong response map** | C | TC-08, TC-13 |
| REQ-MLP-04 | POST entry QA có `date` trong tương lai + tiêu đề có nội dung, mong `201`, response `ReadPlanEntry` chứa `id`, `date`, `title` như tạo | C + T | TC-13 |
| REQ-MLP-05 | PUT entry QA bằng các ID máy chủ trả; mong 200; GET lại phải phản ánh `title`/`text` cập nhật | C + T | TC-13 |
| REQ-MLP-06 | DELETE entry QA, GET sau DELETE được nhóm kỳ vọng `404` như xác minh xóa thành công, **team rule không có trong response map GET** | C + T | TC-13 |
| REQ-MLP-07 | POST thử 7 payload biên; response phải thuộc `{201,422}`; nếu 201 cần `id` để cleanup | C | TC-12 |

### 7.3 Bảy trường hợp con của TC-12

| Case | Dữ liệu | Rủi ro cần kiểm tra |
|---|---|---|
| `minimal_valid` | `{"date":"<ngày tương lai>"}` | Dù đạt schema-required, có thể thiếu điều kiện nghiệp vụ liên trường |
| `empty_title` | `{"date":"...","title":""}` | Chuỗi trống và kiểm tra liên trường |
| `null_recipe_id` | `{"date":"...","recipeId":null}` | Giá trị nullable |
| `missing_required_date` | `{}` | Thiếu ngày bắt buộc |
| `invalid_date_format` | `{"date":"not-a-date"}` | Sai ISO date |
| `invalid_recipe_uuid` | `{"date":"...","recipeId":"not-a-uuid"}` | Sai UUID |
| `invalid_entry_type` | `{"date":"...","entryType":"not-a-meal-type"}` | Enum không hợp lệ |

**OBS-01 (không tính defect):** bản báo cáo P1 ghi nhận dù `date` là trường bắt buộc duy nhất ở schema `CreatePlanEntry`, runtime còn xác minh quan hệ giữa `recipeId` và `title`, khiến case `minimal_valid` nhận 422. Đây là *hạn chế khả năng biểu diễn quy tắc nghiệp vụ* của snapshot, chưa chứng minh sai lệch response map vì `422` có khai báo.

---

## 8. Bộ quy tắc đánh giá và chiến lược kiểm thử

### 8.1 Oracle O1–O8 — diễn giải theo repository

| Oracle | Kiểm tra | Phạm vi/điều kiện |
|---|---|---|
| O1 | `status_code_conformance`: status có trong response map | P0 dùng Schemathesis; P1 direct assertions |
| O2 | `response_schema_conformance`: JSON body theo schema khai báo | P0; P1 một số test chỉ kiểm tra trường cần thiết, **không tự nhận đã validate toàn schema** |
| O3 | Dữ liệu schema-invalid có thể nhận `422` nếu được khai báo; không nhận 5xx undocumented | P0 và boundary P1 |
| O4 | `not_a_server_error`: không chấp nhận 5xx | P0; DEF-04 dùng documented statuses |
| O5 | Path parameter phải có và đúng kiểu (như integer `item_id` cho Meal Plans) | Contract |
| O6 | Bearer authentication hợp lệ; không suy diễn cụ thể HTTP 401/403 vì thiếu trong một số maps | Thiết lập chạy |
| O7 | Khi create thành công, body/field theo output schema | P1; mức kiểm tra thực tế tùy test |
| O8 | Chỉ update/delete tài nguyên do test tạo và cleanup có trật tự | P1 |

### 8.2 P0 — schema-derived read-only

- File lựa chọn: `test_p0_selection.py` xác nhận **đúng 9 GET operations**.
- `test_p0_collections.py` chạy **5 phép GET collection/today**, Hypothesis `max_examples=3` cho mỗi operation.
- `test_p0_details.py` chạy **4 GET detail**, `max_examples=3` cho mỗi operation.
- `test_p0_smoke.py` chạy thêm **1 mục pytest** trên Recipe GET với `max_examples=1`; đây là chạy trùng operation theo **mục đích smoke**, **không phải operation thứ 10**.
- Ba Schemathesis checks được bật trong fuzz/smoke: `not_a_server_error`, `status_code_conformance`, `response_schema_conformance`.

### 8.3 P1 — case có dữ liệu kiểm soát

- Happy-path Shopping List: POST → GET → PUT → GET verify → DELETE → GET verify absence.
- Happy-path Shopping Item: tạo list cha → POST item → GET → PUT → GET verify → DELETE item → GET absence → DELETE list cha.
- Happy-path Meal Plan: POST → GET → PUT → GET verify → DELETE → GET absence.
- Happy-path Recipe: POST → GET → DELETE → GET absence (**không có PUT/PATCH trong test hiện tại**).
- Boundary Shopping List: 3 **pytest parameters**, mỗi tham số tạo ra **một mục test**.
- Boundary Shopping Item: 6 payload **bên trong một mục pytest**.
- Boundary Meal Plan: 7 payload **bên trong một mục pytest**.
- DEF-04: cùng body `{"name":""}` gửi **3 lần bên trong một mục pytest** để kiểm tra tính tái hiện.

### 8.4 Tiêu chí PASS/FAIL và quản lý ngoại lệ

- **PASS:** các assertion đã được bật đều đạt, không có chênh lệch theo từng oracle áp dụng.
- **FAIL–contract:** mã status hoặc schema thực tế không khớp response khai báo; trường hợp 404 hợp lý về nghiệp vụ vẫn là khoảng trống contract nếu không được khai báo.
- **FAIL–server error:** response 5xx trái documented behavior.
- **FAIL–test/harness:** lỗi do giả định sai về payload/response hoặc bug trong test, cần sửa test dựa trên contract và ghi lịch sử (như TEST-05/TEST-06).
- **SKIPPED / BLOCKED:** token thiếu, container không chạy, dữ liệu hoặc mạng không sẵn sàng — **không tính là đã kiểm thử thành công**.
- **OBS:** hành vi bổ sung của runtime nhưng chưa đủ cơ sở gọi là defect (ví dụ OBS-01).
- **Đã biết:** một nhóm lỗi có thể xuất hiện trong nhiều test; không tính số FAIL làm số defect độc lập.

**Sự căng thẳng cần giải thích với giảng viên:** Oracle chung `invariants-and-oracles.md` cố ý **không assert 404 hậu xóa là một yêu cầu OpenAPI**, trong khi test lifecycle dùng `assert after_delete.status_code == 404`. Tài liệu này giữ nguyên cả hai nhưng phân loại hậu xóa là **team-level business expectation (T)**. Trong lần nâng cấp tiếp theo, có thể hoặc (a) bổ sung 404 vào contract chuẩn và dùng nhất quán, hoặc (b) điều chỉnh kiểm tra xóa để không áp đặt một status chưa document. Việc sửa phải có review/phê duyệt; không thay ngay trong bộ test lịch sử.

---

## 9. Mẫu đặc tả test case có thể dùng cho các lần chạy mới

| Trường | Nội dung bắt buộc |
|---|---|
| Test ID / Requirement ID | Ví dụ `TC-14` ↔ `REQ-REC-05` |
| Mục tiêu | Tính năng và điều cần xác minh |
| Độ ưu tiên | P0/P1 |
| Preconditions | SUT/version/token/fixture |
| API & method | Ví dụ `POST /api/recipes` |
| Input | Query/body/path cụ thể; không lưu token |
| Expected | Theo lớp C hoặc T, ghi rõ nguồn; **không lấy từ actual** |
| Actual | Status, response body được rút gọn, thời điểm |
| Verdict | PASS/FAIL/SKIP/BLOCKED và diễn giải |
| Evidence | XML, log, ảnh terminal, request tối giản |
| Defect | DEF-ID hoặc TEST-ID/OBS-ID nếu áp dụng |
| Cleanup | Tên/ID tài nguyên QA đã dọn |

**Ví dụ TC-14:** Request `POST /api/recipes` + `{"name":""}`; expected contract status `{201,422}` và không có 5xx; actual lịch sử `500` + `AssertionError` trong 3 lần; verdict FAIL; liên kết DEF-04. Kỳ vọng *về mặt nghiệp vụ* từ chối tên rỗng bằng 422 có thể đề xuất làm yêu cầu mới, nhưng **hiện không phải một assertion suy ra được từ CreateRecipe schema**.

---

## 10. Tiêu chí chấp nhận tài liệu và quy tắc cập nhật

1. Mỗi yêu cầu có ID duy nhất; ít nhất một test hoặc ghi rõ chưa được bao phủ.
2. Mỗi test có API, input, expected, actual, verdict, evidence và defect link trong ma trận đi kèm.
3. Expected phải có căn cứ SRC-01…06, phân biệt Contract (C) và Test rule (T).
4. Không đổi snapshot khi so sánh hai lần chạy; nếu nâng Mealie, tạo baseline và revision mới.
5. Một defect family có thể mapping nhiều test; tránh nhân số lỗi theo số FAIL.
6. Test có side effect phải có cleanup; nếu phát hiện còn dữ liệu QA, xử lý trước lần chạy mới.
7. Không lưu tài khoản, mật khẩu, token, header Authorization trong repository.
8. Các điểm chưa được OpenAPI biểu diễn đầy đủ phải được công khai là **hạn chế/đề xuất**, không trình bày như nghiệp vụ đã được xác minh.
9. Bản đặc tả này là **baseline hóa sau thời điểm triển khai P0/P1 lịch sử**, dùng để kiểm soát lần test kế tiếp; bất kỳ khẳng định “viết trước rồi mới test” phải đi kèm bằng chứng Git/version thực sự tương ứng.

---

## 11. Danh sách 21 test đã liên kết với tài liệu

| Nhóm | ID | Nội dung | Yêu cầu chính |
|---|---|---|---|
| P0 | TC-01…TC-05 | Năm GET collection/today | REQ-LST-01, ITM-01, MLP-01/02, REC-01/06 |
| P0 | TC-06…TC-09 | Bốn GET detail | REQ-LST-02, ITM-02, MLP-03, REC-02 |
| P0 | TC-10 | Chọn 9 GET operations | REQ-COM-08 |
| P0 | TC-11 | Recipe smoke | REQ-REC-01/06 |
| P1 | TC-12…TC-13 | Meal Plan boundaries/lifecycle | REQ-MLP-04…07 |
| P1 | TC-14…TC-15 | Recipe empty name/lifecycle | REQ-REC-03…05 |
| P1 | TC-16…TC-17 | Shopping Item boundaries/lifecycle | REQ-ITM-03…06 |
| P1 | TC-18…TC-21 | Shopping List boundaries/lifecycle | REQ-LST-03…06 |

Chi tiết **tên test pytest thực tế, từng input, kết quả và defect** xem file song hành: [`../test-design/REQUIREMENTS-TRACEABILITY-MATRIX.md`](../test-design/REQUIREMENTS-TRACEABILITY-MATRIX.md).

---

## 12. Tài liệu tham chiếu nội bộ

- [OpenAPI snapshot](../../schema/snapshots/mealie-v3.28.0-openapi.json)
- [Phân tích hệ thống](../analysis/system-analysis.md)
- [Phân tích API](../analysis/api-analysis.md)
- [Phạm vi kiểm thử](../test-design/test-scope.md)
- [Oracle O1–O8](../test-design/invariants-and-oracles.md)
- [Các scenario P0/P1](../test-design/test-scenarios.md)
- [Business flows](../test-design/business-flows.md)
- [Kết quả kiểm thử hiện có](../../reports/test-results.xml)
- [Inventory và coverage](../../reports/summarized/Test-Inventory-and-Coverage.md)
- [Evidence DEF-01…DEF-04](../../evidence/defects/)

**Mốc duyệt nội bộ đề xuất:** Trước kỳ chạy kiểm thử tiếp theo, nhóm và giảng viên xác nhận các quy tắc mức T, nhất là kỳ vọng GET sau DELETE và empty recipe name. Những nội dung này phải ghi thành quyết định sửa đổi, không lẫn với OpenAPI gốc.
