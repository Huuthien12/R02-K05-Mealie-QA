# KẾ HOẠCH MỞ RỘNG KIỂM THỬ MEALIE – TC-22…TC-37

> **Tình trạng:** IMPLEMENTED / EXECUTED — 10 PASS, 6 FAIL, 0 SKIP, 0 ERROR (23/10/2026).
> **Căn cứ:** FS-01 v1.0 và RTM-01 v1.0 do nhóm cung cấp; OpenAPI snapshot `mealie-v3.28.0-openapi.json` theo hai tài liệu.
> **Phạm vi:** Bốn miền Recipes, Shopping Lists, Shopping Items, Meal Plans.
> **Quy tắc:** 21 mục pytest lịch sử vẫn giữ nguyên. 16 mục này là ứng viên mới; mục tiêu sau khi viết và collect là **37 mục pytest**, không được ghi đã đạt 37 trước khi kiểm tra `pytest --collect-only`.

## 1. Kết quả rà soát tránh trùng lặp

- **Mức đã có:** 21 mục pytest, gồm 11 P0 và 10 P1; RTM-01 đã liên kết các REQ-COM/REC/LST/ITM/MLP đến bài test. **Truy vết yêu cầu không đồng nghĩa đã kiểm chứng toàn bộ biến thể dữ liệu, nhánh xử lý, hay logic nghiệp vụ.**
- **TC-12 Meal Plans:** đã thực hiện 7 payload POST, gồm `missing_required_date`, `invalid_date_format`, `invalid_recipe_uuid`, `invalid_entry_type`.
- **TC-16 Shopping Items:** đã thực hiện 6 payload POST gồm quantity 0, âm, thiếu shoppingListId và UUID sai cú pháp.
- **TC-17 Shopping Items:** đã PUT quantity=2, checked=true, note; không cần viết lại y chang.
- **TC-18…TC-20 Shopping Lists:** đã POST `{}`, `name:null`, `name:""`; không thêm lại.
- **TC-21 Shopping Lists:** đã một lần tạo/đọc/sửa/xóa và GET hậu xóa; test mới phải thay đổi điều kiện hoặc hành vi.
- **TC-14 Recipe:** đã POST `name:""` 3 lần; test whitespace là trường hợp khác.
- **TC-15 Recipe:** chỉ có POST/GET/DELETE, **chưa có PUT/PATCH**.
- **Nhận xét:** RTM phần 5.2 nêu test gap; đặc biệt phải phân biệt kỳ vọng **C** (OpenAPI) với **T** (quy tắc nghiệp vụ do nhóm đề xuất cần review), tránh coi một status `{201,422}` PASS là chứng minh validation đúng.

## 2. Bảng giao việc và trọng tâm

| Người phụ trách | Mã | Miền | Ưu tiên rủi ro | Công việc chính |
|---|---|---|---|---|
| Lương Hữu Thiện | TC-22 | Shopping Lists | Cao | POST tên chỉ có khoảng trắng |
| Lương Hữu Thiện | TC-23 | Shopping Lists | Trung bình | POST/GET tên Unicode tiếng Việt |
| Lương Hữu Thiện | TC-24 | Shopping Lists | Trung bình | PUT tới UUID không tồn tại |
| Lương Hữu Thiện | TC-25 | Shopping Lists | Trung bình | DELETE cùng list QA lần thứ hai |
| Nguyễn Minh Long | TC-26 | Meal Plans | Trung bình | GET khoảng ngày đảo ngược |
| Nguyễn Minh Long | TC-27 | Meal Plans | Cao | PUT hai lần và xác minh trạng thái cuối |
| Nguyễn Minh Long | TC-28 | Meal Plans | Trung bình | DELETE meal plan ID số nguyên không tồn tại |
| Nguyễn Minh Long | TC-29 | Meal Plans | Cao | PUT ngày sai định dạng và kiểm tra tính toàn vẹn |
| Hoàng Bình Quân | TC-30 | Shopping Items | Cao | PUT quantity âm và xác minh dữ liệu |
| Hoàng Bình Quân | TC-31 | Shopping Items | Cao | POST item với parent UUID hợp lệ nhưng không tồn tại |
| Hoàng Bình Quân | TC-32 | Shopping Items | Trung bình | Đổi checked true → false, GET xác minh |
| Hoàng Bình Quân | TC-33 | Shopping Items | Cao | Chuyển item giữa hai danh sách QA |
| Nguyễn Hồng Phúc Thọ | TC-34 | Recipes | Cao | PUT cập nhật Recipe QA (gap chính) |
| Nguyễn Hồng Phúc Thọ | TC-35 | Recipes | Cao | PATCH cập nhật từng phần Recipe QA |
| Nguyễn Hồng Phúc Thọ | TC-36 | Recipes | Cao | POST name chỉ có khoảng trắng |
| Nguyễn Hồng Phúc Thọ | TC-37 | Recipes | Trung bình | POST tên dài 256 ký tự |

> **Cân bằng công việc:** Mỗi người 4 test, nhưng công sức ước lượng không bằng nhau (Thiện 9h, Long 10h, Quân 12h, Thọ 13h; tổng 44h). Có thể dành 4h bổ sung cho review chung để khớp kế hoạch nguồn lực 48h, sau đó phân bổ lại theo khó khăn thực tế. Đây là **ước lượng đề xuất**, chưa phải giờ công đã ghi nhận.

## 3. Đặc tả thiết kế ban đầu TC-22…TC-37

Định nghĩa chung: **C** = điều kiện kiểm tra trực tiếp từ hợp đồng OpenAPI; **T** = kịch bản nghiệp vụ do nhóm chọn hoặc dự kiến cần xác nhận. Không sửa `Expected` theo `Actual`. Severity của defect chỉ được chốt **sau khi phát hiện và triage**; cột “rủi ro” dưới đây chỉ là **ưu tiên thiết kế test**. Nội dung các case bên dưới được giữ như thiết kế ban đầu; verdict hiện hành là JUnit post-fix ngày 23/10/2026 ở mục 7.

### TC-22 – POST tên chỉ có khoảng trắng

- **Người thực hiện / phạm vi:** Lương Hữu Thiện – Shopping Lists; rủi ro **Cao**; dự kiến 2 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-LST-03/06, REQ-COM-02/06; ID đề xuất QA-LST-01 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: TC-18/19/20 (chỉ {}, null và chuỗi rỗng).
- **Kỹ thuật / endpoint:** Boundary / contract; `POST /api/households/shopping/lists`.
- **Tiền điều kiện:** Bearer QA; Mealie local; không dùng danh sách người dùng thật.
- **Input:** `{"name":"   "}` với marker QA nếu tạo thành công.
- **Expected – C (hợp đồng):** Chỉ nhận status được OpenAPI công bố (`201` hoặc `422`); không có 5xx; nếu 201 phải có `id` hợp lệ..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** Nếu 201, GET để quan sát giá trị tên được lưu, rồi DELETE chính list đã tạo. Chính sách bắt buộc từ chối whitespace *chưa được xác nhận*..
- **Cleanup:** DELETE list QA nếu POST trả 201.
- **Bộ chạy đề xuất:** `P1-isolated`.
- **Lưu ý tránh trùng/rủi ro:** Mới so với TC-20: `""` khác `"   "`; không ép 422 nếu chưa được phê duyệt..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — PASS` theo JUnit post-fix 23/10/2026.

### TC-23 – POST/GET tên Unicode tiếng Việt

- **Người thực hiện / phạm vi:** Lương Hữu Thiện – Shopping Lists; rủi ro **Trung bình**; dự kiến 2 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-LST-03, REQ-COM-02/03/06; ID đề xuất QA-LST-02 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: TC-21 (tên ASCII thông thường).
- **Kỹ thuật / endpoint:** Positive / round-trip; `POST /api/households/shopping/lists; GET /{item_id}`.
- **Tiền điều kiện:** Token và list QA riêng; ID trả về từ POST.
- **Input:** `{"name":"K05-QA-Mua sắm Đà Lạt-<unique>"}`.
- **Expected – C (hợp đồng):** Response POST nằm trong `{201,422}`; khi 201 body theo ShoppingListOut và có `id`..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** Với happy path Unicode đã thống nhất, đề xuất kỳ vọng 201 và GET `name` khớp chính xác; nếu quy tắc chuẩn hóa Unicode khác phải xin duyệt..
- **Cleanup:** DELETE list QA trong finally.
- **Bộ chạy đề xuất:** `P1-isolated`.
- **Lưu ý tránh trùng/rủi ro:** Thêm kiểm tra tính toàn vẹn Unicode thay vì lặp happy path ASCII..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — PASS` theo JUnit post-fix 23/10/2026.

### TC-24 – PUT tới UUID không tồn tại

- **Người thực hiện / phạm vi:** Lương Hữu Thiện – Shopping Lists; rủi ro **Trung bình**; dự kiến 3 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-LST-02/04, REQ-COM-02/06; ID đề xuất QA-LST-03 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: TC-21 PUT đối tượng tồn tại; TC-06 GET detail.
- **Kỹ thuật / endpoint:** Negative path / contract; `PUT /api/households/shopping/lists/{item_id}`.
- **Tiền điều kiện:** Tạo trước một list QA làm nguồn ID hợp lệ; chắc chắn UUID mục tiêu chưa tồn tại.
- **Input:** UUID v4 mới không tồn tại, payload lấy `groupId`, `userId` từ list QA và đặt `id` tương ứng UUID mục tiêu.
- **Expected – C (hợp đồng):** So phản hồi với response map của PUT `{200,422}` và schema khi có; 404/400 là finding contract cần phân loại, không mặc định lỗi nghiệp vụ..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** List QA nguồn giữ nguyên; nếu API tạo tài nguyên ngoài ý muốn phải kiểm tra và dọn chính tài nguyên QA tạo bởi test..
- **Cleanup:** DELETE list QA nguồn; xử lý tài nguyên QA phát sinh nếu có.
- **Bộ chạy đề xuất:** `P1-isolated`.
- **Lưu ý tránh trùng/rủi ro:** Không thực hiện PUT lên ID của dữ liệu thật..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — FAIL`, documented-response mismatch `404` (DEF-03 extension) theo JUnit post-fix 23/10/2026.

### TC-25 – DELETE cùng list QA lần thứ hai

- **Người thực hiện / phạm vi:** Lương Hữu Thiện – Shopping Lists; rủi ro **Trung bình**; dự kiến 2 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-LST-05, REQ-COM-02/06/07; ID đề xuất QA-LST-04 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: TC-21 chỉ DELETE một lần rồi GET xác nhận.
- **Kỹ thuật / endpoint:** Repeat-delete / contract; `DELETE /api/households/shopping/lists/{item_id} lặp lại`.
- **Tiền điều kiện:** Đã tạo thành công list QA, xóa lần 1 được xác nhận.
- **Input:** `id` của list test tự tạo, DELETE lần 1 rồi DELETE lần 2.
- **Expected – C (hợp đồng):** Phản hồi DELETE thứ hai cần được đối chiếu documented `{200,422}`; 404 nếu xảy ra là contract gap, không tự tuyên bố lỗi nghiệp vụ..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** List không xuất hiện trở lại; không có dữ liệu ngoài phạm vi QA bị tác động..
- **Cleanup:** Đảm bảo list QA không tồn tại; nếu còn thì cleanup.
- **Bộ chạy đề xuất:** `P1-isolated`.
- **Lưu ý tránh trùng/rủi ro:** Khác TC-21: kiểm tra tính lặp của thao tác xóa..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — FAIL`, documented-response mismatch `404` (DEF-03 extension) theo JUnit post-fix 23/10/2026.

### TC-26 – GET khoảng ngày đảo ngược

- **Người thực hiện / phạm vi:** Nguyễn Minh Long – Meal Plans; rủi ro **Trung bình**; dự kiến 2 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-MLP-01, REQ-COM-02/03/04; ID đề xuất QA-MLP-01 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: TC-03 fuzz GET collection; chưa có case truy vấn ngày đảo được chốt.
- **Kỹ thuật / endpoint:** Boundary query / contract; `GET /api/households/mealplans`.
- **Tiền điều kiện:** Token QA; read-only.
- **Input:** `start_date=2026-11-20&end_date=2026-11-01` (hoặc hai ngày tham chiếu cố định theo baseline).
- **Expected – C (hợp đồng):** Kết quả chỉ thuộc response map `{200,422}`, JSON schema đúng nếu 200; không có undocumented 5xx..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** Ý nghĩa nghiệp vụ của start > end cần xác nhận; không bắt buộc 422 trước khi có chính sách được duyệt..
- **Cleanup:** Không cần (GET).
- **Bộ chạy đề xuất:** `P0-safe`.
- **Lưu ý tránh trùng/rủi ro:** Dữ liệu cụ thể có kiểm soát, khác dữ liệu random từ TC-03..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — PASS` theo JUnit post-fix 23/10/2026.

### TC-27 – PUT hai lần và xác minh trạng thái cuối

- **Người thực hiện / phạm vi:** Nguyễn Minh Long – Meal Plans; rủi ro **Cao**; dự kiến 3 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-MLP-05, REQ-COM-06; ID đề xuất QA-MLP-02 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: TC-13 chỉ PUT một lần.
- **Kỹ thuật / endpoint:** Stateful regression; `POST /api/households/mealplans; PUT /{item_id} ×2; GET`.
- **Tiền điều kiện:** Token QA; entry chỉ do test tạo; cập nhật qua body đủ trường bắt buộc.
- **Input:** Tạo entry QA ngày tương lai; lần lượt đổi `title` A → B → C với IDs lấy từ server.
- **Expected – C (hợp đồng):** POST 201, PUT phản hồi thuộc `{200,422}`, GET theo documented responses..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** Trong happy path đã thống nhất, cả hai PUT 200 và GET cuối cùng là C, giữ nguyên id, date; không mất bản ghi..
- **Cleanup:** DELETE entry QA trong finally.
- **Bộ chạy đề xuất:** `P1-isolated`.
- **Lưu ý tránh trùng/rủi ro:** Mới so với single-update TC-13..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — PASS` theo JUnit post-fix 23/10/2026.

### TC-28 – DELETE meal plan ID số nguyên không tồn tại

- **Người thực hiện / phạm vi:** Nguyễn Minh Long – Meal Plans; rủi ro **Trung bình**; dự kiến 2 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-MLP-06, REQ-COM-02/06; ID đề xuất QA-MLP-03 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: TC-08 GET id=0, TC-13 DELETE id thật.
- **Kỹ thuật / endpoint:** Negative delete / contract; `DELETE /api/households/mealplans/{item_id}`.
- **Tiền điều kiện:** Xác nhận ID không trỏ tới plan thật; dùng ID được chứng minh không tồn tại.
- **Input:** ID số nguyên không tồn tại đã xác minh qua GET, chỉ trên QA local.
- **Expected – C (hợp đồng):** Response DELETE chỉ được OpenAPI mô tả `{200,422}`; 404 nếu có là finding contract để review, không kết luận sai nghiệp vụ..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** Không thay đổi dữ liệu hay xóa nhầm plan đang tồn tại..
- **Cleanup:** Không cần, nhưng kiểm tra hậu điều kiện read-only đối với dữ liệu sẵn có.
- **Bộ chạy đề xuất:** `P1-isolated`.
- **Lưu ý tránh trùng/rủi ro:** Không sử dụng ID bất kỳ chưa chứng minh không tồn tại..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — FAIL`, documented-response mismatch `404` (DEF-03 extension) theo JUnit post-fix 23/10/2026.

### TC-29 – PUT ngày sai định dạng và kiểm tra tính toàn vẹn

- **Người thực hiện / phạm vi:** Nguyễn Minh Long – Meal Plans; rủi ro **Cao**; dự kiến 3 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-MLP-05/07, REQ-COM-02/06; ID đề xuất QA-MLP-04 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: TC-12 có POST date sai; TC-13 PUT hợp lệ.
- **Kỹ thuật / endpoint:** Negative update / invariant; `POST plan QA; PUT /{item_id} với `date="not-a-date"`; GET`.
- **Tiền điều kiện:** Entry QA đã tạo; lưu representation trước PUT.
- **Input:** Body PUT sao từ representation của QA entry, đổi `date` thành `not-a-date`.
- **Expected – C (hợp đồng):** PUT theo response map `{200,422}`; không 5xx undocumented; GET theo contract..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** Nếu PUT bị từ chối (422), entry còn nguyên dữ liệu cũ; nếu chấp nhận (200), ghi nhận để review validation, không gọi PASS nghiệp vụ khi thiếu quy tắc..
- **Cleanup:** DELETE entry QA.
- **Bộ chạy đề xuất:** `P1-isolated`.
- **Lưu ý tránh trùng/rủi ro:** Khác POST invalid-date đã kiểm thử trong TC-12..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — PASS` theo JUnit post-fix 23/10/2026.

### TC-30 – PUT quantity âm và xác minh dữ liệu

- **Người thực hiện / phạm vi:** Hoàng Bình Quân – Shopping Items; rủi ro **Cao**; dự kiến 3 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-ITM-04/06, REQ-COM-02/06; ID đề xuất QA-ITM-01 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: TC-16 thử POST negative quantity; TC-17 PUT quantity=2.
- **Kỹ thuật / endpoint:** Negative update / invariant; `POST QA list+item; PUT /items/{item_id}; GET`.
- **Tiền điều kiện:** Chỉ chỉnh item QA, lưu giá trị quantity cũ.
- **Input:** Bản cập nhật chứa `quantity=-1` và `shoppingListId` đúng.
- **Expected – C (hợp đồng):** PUT response `{200,422}`; không 5xx; nếu 200 body/schema hợp đồng..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** Nếu 422, GET quantity không thay đổi. Nếu 200, ghi nhận rằng runtime chấp nhận âm; cần phê duyệt rule nghiệp vụ mới được kết luận sai/đúng..
- **Cleanup:** Xóa item QA trước list QA.
- **Bộ chạy đề xuất:** `P1-isolated`.
- **Lưu ý tránh trùng/rủi ro:** POST âm và PUT âm là hai nghiệp vụ khác nhau..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — PASS` theo JUnit post-fix 23/10/2026.

### TC-31 – POST item với parent UUID hợp lệ nhưng không tồn tại

- **Người thực hiện / phạm vi:** Hoàng Bình Quân – Shopping Items; rủi ro **Cao**; dự kiến 3 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-ITM-03/06, REQ-COM-02/06; ID đề xuất QA-ITM-02 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: TC-16 có missing parent và UUID sai format, không có UUID valid-but-missing.
- **Kỹ thuật / endpoint:** Missing reference / contract; `POST /api/households/shopping/items`.
- **Tiền điều kiện:** Token QA; không đụng bất kỳ list người dùng thật.
- **Input:** `shoppingListId` là UUID v4 cú pháp hợp lệ đã xác minh không tồn tại.
- **Expected – C (hợp đồng):** POST chỉ có documented status `{201,422}`; 404 nếu có cần ghi là contract mismatch; response 201 phải có `createdItems[]`..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** Không sinh orphan item; nếu unexpectedly 201 cần dùng createdItems dọn tài nguyên và ghi observation..
- **Cleanup:** Nếu tạo ra item QA thì DELETE theo id; rà soát không để dữ liệu mồ côi.
- **Bộ chạy đề xuất:** `P1-isolated`.
- **Lưu ý tránh trùng/rủi ro:** Tách rõ invalid format và valid format nhưng thiếu record..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — FAIL`, HTTP `500` (DEF-05) theo JUnit post-fix 23/10/2026.

### TC-32 – Đổi checked true → false, GET xác minh

- **Người thực hiện / phạm vi:** Hoàng Bình Quân – Shopping Items; rủi ro **Trung bình**; dự kiến 2 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-ITM-04, REQ-COM-06; ID đề xuất QA-ITM-03 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: TC-17 chỉ cập nhật checked false → true.
- **Kỹ thuật / endpoint:** State transition / regression; `POST list+item; PUT checked=true; PUT checked=false; GET`.
- **Tiền điều kiện:** Item QA tồn tại, IDs lấy từ response.
- **Input:** Giữ cùng item QA, hai PUT liên tiếp và `shoppingListId` đúng.
- **Expected – C (hợp đồng):** Các PUT nằm trong response map `{200,422}`, GET trả schema được khai báo..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** Trong happy path đã duyệt cả hai PUT 200; GET cuối cho checked=false và id/parent không đổi..
- **Cleanup:** Xóa item trước list.
- **Bộ chạy đề xuất:** `P1-isolated`.
- **Lưu ý tránh trùng/rủi ro:** Khác chiều cập nhật checked trong TC-17..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — PASS` theo JUnit post-fix 23/10/2026.

### TC-33 – Chuyển item giữa hai danh sách QA

- **Người thực hiện / phạm vi:** Hoàng Bình Quân – Shopping Items; rủi ro **Cao**; dự kiến 4 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-ITM-03/04/05, REQ-COM-06; ID đề xuất QA-ITM-04 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: TC-17 chỉ giữ item trong một danh sách cha.
- **Kỹ thuật / endpoint:** Referential integrity / business review; `POST 2 list QA + 1 item; PUT shoppingListId list B; GET`.
- **Tiền điều kiện:** Hai list QA mới, ownership giống nhau; chỉ dùng item do test tạo.
- **Input:** Item ban đầu list A; thử PUT shoppingListId sang list B.
- **Expected – C (hợp đồng):** PUT phản hồi thuộc `{200,422}`; GET theo contract, không 5xx..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** Nếu 200, GET item trỏ B và không còn dưới A; nếu 422, GET giữ nguyên A. Quy tắc chuyển list có được hỗ trợ cần xem xét nghiệp vụ..
- **Cleanup:** DELETE item trước khi DELETE cả hai list QA.
- **Bộ chạy đề xuất:** `P1-isolated`.
- **Lưu ý tránh trùng/rủi ro:** Cần kiểm tra quyền/chính sách chuyển parent trước khi chốt assertion business..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — PASS` theo JUnit post-fix 23/10/2026.

### TC-34 – PUT cập nhật Recipe QA (gap chính)

- **Người thực hiện / phạm vi:** Nguyễn Hồng Phúc Thọ – Recipes; rủi ro **Cao**; dự kiến 4 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-REC-03/04, REQ-COM-02/06; ID đề xuất QA-REC-01 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: TC-15 chỉ POST/GET/DELETE, chưa PUT.
- **Kỹ thuật / endpoint:** Missing operation / lifecycle; `POST /api/recipes; PUT /api/recipes/{slug}; GET`.
- **Tiền điều kiện:** Bắt buộc kiểm tra `Recipe-Input` và payload hợp lệ trước khi code; slug QA; token.
- **Input:** Tạo recipe QA; body PUT theo schema Recipe-Input sau khi đối chiếu snapshot, sửa trường được hỗ trợ.
- **Expected – C (hợp đồng):** PUT documented `{200,422}`; nếu thành công response theo schema; không 5xx..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** Chỉ sau khi xác nhận field cập nhật được hỗ trợ, GET phản ánh đúng giá trị; nếu schema không cho phép hành vi giả định, chuyển test sang review..
- **Cleanup:** DELETE recipe QA.
- **Bộ chạy đề xuất:** `P1-isolated`.
- **Lưu ý tránh trùng/rủi ro:** RỦI RO TRIỂN KHAI: chưa cung cấp cấu trúc Recipe-Input chi tiết; tuyệt đối không bịa body..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — FAIL`, HTTP `500 ValidationError` (DEF-06) theo JUnit post-fix 23/10/2026.

### TC-35 – PATCH cập nhật từng phần Recipe QA

- **Người thực hiện / phạm vi:** Nguyễn Hồng Phúc Thọ – Recipes; rủi ro **Cao**; dự kiến 4 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-REC-03/04, REQ-COM-02/06; ID đề xuất QA-REC-02 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: Chưa có TC PATCH Recipes; TC-15 chỉ create/read/delete.
- **Kỹ thuật / endpoint:** Missing operation / partial update; `POST recipe QA; PATCH /api/recipes/{slug}; GET`.
- **Tiền điều kiện:** Xác minh PATCH operation và schema request cụ thể trong snapshot/implementation trước khi viết harness.
- **Input:** Body PATCH theo contract Recipe-Input; thay đổi một trường có thể cập nhật, giữ field khác làm baseline.
- **Expected – C (hợp đồng):** PATCH documented `{200,422}`; đúng response schema, không undocumented 5xx..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** Nếu PATCH thành công, trường được chỉnh đúng và các trường không chỉnh không bị thay đổi ngoài quy tắc định nghĩa..
- **Cleanup:** DELETE recipe QA.
- **Bộ chạy đề xuất:** `P1-isolated`.
- **Lưu ý tránh trùng/rủi ro:** Không giả định PATCH chấp nhận JSON Merge Patch nếu OpenAPI không quy định..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — PASS`; TEST-07 fixed/verified by using the slug returned by PATCH, theo JUnit post-fix 23/10/2026.

### TC-36 – POST name chỉ có khoảng trắng

- **Người thực hiện / phạm vi:** Nguyễn Hồng Phúc Thọ – Recipes; rủi ro **Cao**; dự kiến 2 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-REC-05, REQ-COM-02/04/06; ID đề xuất QA-REC-03 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: TC-14 chỉ `name=""`.
- **Kỹ thuật / endpoint:** Boundary / contract; `POST /api/recipes`.
- **Tiền điều kiện:** QA local, token hợp lệ, có phương án dọn slug nếu 201.
- **Input:** `{"name":"   "}`.
- **Expected – C (hợp đồng):** POST theo response map `{201,422}`; không trả 5xx chưa khai báo..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** Nếu 201, response JSON là string slug hợp lệ để dọn dữ liệu; reject whitespace chỉ là kiến nghị cho nghiệp vụ..
- **Cleanup:** Nếu 201, DELETE slug QA.
- **Bộ chạy đề xuất:** `P1-isolated`.
- **Lưu ý tránh trùng/rủi ro:** Không đồng nhất chuỗi rỗng với chuỗi chứa khoảng trắng..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — FAIL`, undocumented HTTP `400` (DEF-07) theo JUnit post-fix 23/10/2026.

### TC-37 – POST tên dài 256 ký tự

- **Người thực hiện / phạm vi:** Nguyễn Hồng Phúc Thọ – Recipes; rủi ro **Trung bình**; dự kiến 3 giờ viết/chạy/đối chiếu.
- **Tham chiếu:** REQ-REC-03/05, REQ-COM-02/04/06; ID đề xuất QA-REC-04 (chưa phải yêu cầu chính thức). Test có liên quan đã tồn tại: TC-14 rỗng; TC-15 tên bình thường; không có length stress.
- **Kỹ thuật / endpoint:** Boundary length / contract; `POST /api/recipes; GET nếu tạo thành công`.
- **Tiền điều kiện:** Token QA, local, không sử dụng tên của dữ liệu thật.
- **Input:** `name = "K05-QA-" + run_id_8 + "-" + "A"*240` (256 ký tự; run_id_8 gồm đúng 8 ký tự).
- **Expected – C (hợp đồng):** POST chỉ `{201,422}`; không undocumented 5xx; nếu 201, response theo kiểu JSON string slug..
- **Expected – T (quy tắc hoặc quan sát nghiệp vụ):** Nếu tạo thành công, GET đúng slug/name theo các ràng buộc được schema/ứng dụng công bố; nếu bị từ chối hợp đồng 422 thì vẫn cần ghi lý do nếu muốn kết luận nghiệp vụ..
- **Cleanup:** DELETE recipe QA nếu POST 201.
- **Bộ chạy đề xuất:** `P1-isolated`.
- **Lưu ý tránh trùng/rủi ro:** Không khẳng định schema đặt maxLength khi chưa có bằng chứng..
- **Bằng chứng cần lưu khi chạy:** ID, commit SUT+QA, request rút gọn đã ẩn token, status/body, assertion, cleanup, JUnit XML, defect hoặc OBS nếu có.
- **Trạng thái hiện hành:** `IMPLEMENTED / EXECUTED — PASS` theo JUnit post-fix 23/10/2026.

## 4. Điều kiện trước khi viết mã

1. Chốt OpenAPI snapshot/commit: bản tài liệu đang nói Mealie v3.28.0, nhưng cần xác nhận Docker image chạy đúng source baseline trước khi khẳng định reproducibility.
2. Kiểm tra chính xác schema request/response của các operation mới, đặc biệt **Recipe PUT/PATCH**; không đoán payload, không dùng dữ liệu GET làm request nếu schema không cho phép.
3. Trưởng nhóm và reviewer duyệt expected **T** (Unicode, repeated PUT, chuyển parent, reject whitespace). Còn thiếu căn cứ thì chỉ assert C và ghi `NEEDS_SPEC_REVIEW` cho kiểm chứng nghiệp vụ.
4. Chốt mỗi test mới thành **một pytest item riêng**, hoặc đổi mục tiêu 37 nếu parameterize khác; kiểm tra bằng `python -m pytest --collect-only -q`.
5. Chỉ chạy write/DELETE trên QA instance độc lập, marker riêng, cleanup đúng thứ tự.

## 5. Tiêu chí lựa chọn ưu tiên triển khai

- Đợt đầu: **TC-34/35** đóng gap operation Recipe PUT/PATCH và **TC-30/31/33** cho dữ liệu quan hệ; xác nhận feasibility trước.
- Đợt thứ hai: test truy vấn P0 **TC-26** và các boundary **TC-22/36/37** để tăng đa dạng input.
- Đợt thứ ba: các test trạng thái/hồi quy **TC-23/24/25/27/28/29/32** và tự động hóa CI sau khi local ổn định.
- Nếu phiên chạy **không phát hiện defect**: báo requirement coverage, operation coverage trong phạm vi, input class coverage, số example và thời gian chạy; đối chiếu ngưỡng QA **được phê duyệt trước**. Không tự nhận hết lỗi.
- Nếu bị BLOCKED (Docker/token/schema/môi trường): phân loại ENV/HARNESS, sửa blocker, chạy lại; không gọi là FAIL phần mềm.

## 6. Cách cập nhật FS-01 và RTM-01

- Giữ nguyên 33 yêu cầu FS-01 của baseline và 21 verdict lịch sử RTM-01.
- Đề xuất 16 ID mở rộng `QA-LST-01…04`, `QA-MLP-01…04`, `QA-ITM-01…04`, `QA-REC-01…04`: đây là **đề xuất kiểm thử** từ khoảng trống, không phải 16 yêu cầu chính thức mới của tác giả Mealie.
- Trong bản kế hoạch ban đầu, RTM dự kiến đánh dấu 16 dòng `PLANNED`, các cột ACTUAL/VERDICT/evidence là `CHƯA CHẠY`/`—`. Kế hoạch này đã được thay thế bởi kết quả thực thi lưu trong JUnit ngày 23/10/2026 và RTM hiện hành.
- Khi bản mới được duyệt: thêm mapping vào RTM bản mới và tăng version FS/RTM, không thay đổi dữ liệu baseline v1.0.

## 7. Cập nhật triển khai (TC-22…TC-37)

Ngày cập nhật: 2026-10-23. Phần này thay thế trạng thái thiết kế ban đầu của 16 case bằng trạng thái **mã nguồn và thực thi**; không thay thế kết quả lịch sử TC-01…TC-21.

| Tests | File pytest | Trạng thái mã | Trạng thái thực thi |
|---|---|---|---|
| TC-22…TC-25 | `tests/schemathesis/test_tc22_tc25_shopping_lists.py` | IMPLEMENTED | 2 PASS / 2 FAIL (DEF-03 extension) |
| TC-26…TC-29 | `tests/schemathesis/test_tc26_tc29_mealplans.py` | IMPLEMENTED | 3 PASS / 1 FAIL (DEF-03 extension) |
| TC-30…TC-33 | `tests/schemathesis/test_tc30_tc33_shopping_items.py` | IMPLEMENTED | 3 PASS / 1 FAIL (DEF-05 reproduced 2/2) |
| TC-34…TC-37 | `tests/schemathesis/test_tc34_tc37_recipes.py` | IMPLEMENTED; TEST-07 fixed/verified | 2 PASS / 2 FAIL (DEF-06/07 reproduced 2/2) |

- `pytest --collect-only -q` thu thập 37 items: 21 historical và đúng 16 item mới.
- Historical expansion evidence `reports/local-runs/tc22-tc37-20261022-164618-697.xml` ghi 9 PASS / 7 FAIL. Post-fix evidence `reports/local-runs/tc22-tc37-20261023-215442-705.xml` ghi 10 PASS, 6 FAIL, 0 SKIP, 0 ERROR. TC-24/25/28 tiếp tục là DEF-03; DEF-05/06/07 tái hiện 2/2; TC-35 PASS xác nhận TEST-07 đã sửa ở harness.
- TC-26 là read-only; 15 case còn lại chỉ chạy khi có `MEALIE_API_TOKEN` **và** đặt `MEALIE_RUN_P1_EXPANSION=1`. Mỗi fixture chỉ tạo dữ liệu có tiền tố `K05-TC-` và cleanup trong `finally`.
- Đối chiếu snapshot xác nhận mọi operation mới dùng response map C `{200,422}` cho GET/PUT/PATCH/DELETE hoặc `{201,422}` cho POST. Recipe `PUT`/`PATCH` dùng body tối thiểu `{"name": ...}` vì `Recipe-Input` không khai báo `required`; không suy đoán trường bắt buộc ngoài schema.
- Các assertion T (round-trip, integrity và trạng thái cuối) chỉ được đánh giá sau response thành công theo C; rejection `422` không bị gán thành vi phạm nghiệp vụ. TC-24 lấy `groupId`/`userId` từ GET resource do test tạo, không suy diễn từ response POST.
- Audit cleanup ngày 2026-10-23 tìm thấy hai recipe khớp chính xác marker `K05-TC-35-patched-<8 hex>` từ các campaign cũ. Chỉ hai test resources này được DELETE (`200` cho cả hai); quét lại xác nhận không còn marker `K05-TC-` trong Recipes, Shopping Lists, Shopping Items hoặc Meal Plans.
