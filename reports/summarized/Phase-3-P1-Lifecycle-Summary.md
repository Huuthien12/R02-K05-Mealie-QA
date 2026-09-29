# Phase 3 P1 — Controlled Lifecycle Testing Summary

## 1. Tổng quan

- **Project:** R02-K05-Mealie-QA
- **SUT:** Mealie
- **Baseline:** `v3.28.0`
- **Commit SHA:** `0552eaa4a80031b8572849cca0ed95d07f1be001`
- **Phase:** Phase 3 — P1 Controlled Lifecycle / Write Testing
- **Approach:** Schema-Based API Testing kết hợp controlled lifecycle tests
- **Tools:** pytest, requests, Schemathesis/OpenAPI analysis
- **Safety principle:** Chỉ tạo/sửa/xóa resource do test tạo; cleanup sau test; không broad-fuzz write endpoints.

---

## 2. Mục tiêu P1

P1 mở rộng từ P0 read-only sang các API có side effect một cách có kiểm soát.

Mục tiêu:

- Kiểm tra create/read/update/delete trên các resource QA.
- Xác minh response status so với OpenAPI contract.
- Thử các boundary payload có kiểm soát.
- Cleanup dữ liệu test.
- Triage finding ngoài scope đã phát hiện ở P0.
- Tái hiện có kiểm soát DEF-04.

Các resource chính:

1. Shopping List
2. Shopping Item
3. Meal Plan
4. Recipe

---

# 3. P1-A — Shopping List

## 3.1 Lifecycle test

Test:

`tests/schemathesis/test_p1_shopping_list_lifecycle.py`

Luồng:

`POST → GET → PUT → GET verify → DELETE → GET after delete`

Kết quả:

- Create → PASS
- Read → PASS
- Update → PASS
- Verify update → PASS
- Delete → PASS
- GET sau delete → runtime `404`

### Kết luận
Shopping List happy-path lifecycle hoạt động đúng trong phạm vi test.

---

## 3.2 Boundary test

Test:

`tests/schemathesis/test_p1_shopping_list_boundaries.py`

Các trường hợp:

- empty object `{}`
- `name=null`
- `name=""`

Kết quả:

`3 passed`

Các trường hợp trên không tạo undocumented status trong campaign.

### New defect
**0**

---

# 4. P1-B — Shopping Item

## 4.1 Lifecycle test

Test:

`tests/schemathesis/test_p1_shopping_item_lifecycle.py`

Luồng:

1. Tạo parent Shopping List tạm.
2. Tạo Shopping Item.
3. GET item.
4. PUT update.
5. GET verify.
6. DELETE item.
7. GET sau delete.
8. Cleanup parent.

Final result:

`1 passed`

### Harness finding
POST Shopping Item không trả item trực tiếp mà trả wrapper:

```json
{
  "createdItems": [],
  "updatedItems": [],
  "deletedItems": []
}
```

Item mới nằm trong:

`createdItems[0]`

Test harness ban đầu giả định top-level `id`, sau đó được sửa.

Mục này được ghi là **TEST-05**, không phải SUT defect.

---

## 4.2 Boundary test

Test:

`tests/schemathesis/test_p1_shopping_item_boundaries.py`

Các nhóm case đã kiểm tra:

- minimal valid payload
- nullable optional fields
- zero quantity
- negative quantity
- missing required `shoppingListId`
- invalid UUID

Final pytest result:

`1 passed`

Assertion chấp nhận các response đã được contract document cho POST campaign (`201` hoặc `422`).

### New defect
**0**

---

# 5. P1-C — Meal Plan

## 5.1 Lifecycle test

Test:

`tests/schemathesis/test_p1_mealplan_lifecycle.py`

`UpdatePlanEntry` yêu cầu:

- `date`
- `id`
- `groupId`
- `userId`

Do đó test không tự tạo các identifier này. Sau POST, test GET representation hiện tại từ server và dùng các server-provided fields cho PUT.

Luồng và kết quả:

| Step | Result |
|---|---:|
| POST create | 201 |
| GET | 200 |
| PUT update | 200 |
| GET verify | 200 |
| DELETE | 200 |
| GET after delete | 404 |

Final result:

`1 passed`

### Kết luận
Controlled Meal Plan lifecycle PASS.

---

## 5.2 Boundary test

Test:

`tests/schemathesis/test_p1_mealplan_boundaries.py`

Các case và actual status:

| Case | Actual |
|---|---:|
| minimal_valid | 422 |
| empty_title | 422 |
| null_recipe_id | 422 |
| missing_required_date | 422 |
| invalid_date_format | 422 |
| invalid_recipe_uuid | 422 |
| invalid_entry_type | 422 |

Final pytest result:

`1 passed`

Tất cả status đều nằm trong documented response set của operation.

---

## 5.3 OBS-01 — Cross-field validation

OpenAPI `CreatePlanEntry` thể hiện `date` là required field, nhưng runtime còn áp dụng validation liên trường liên quan `recipeId` và `title`.

Runtime message quan sát được:

`Value error, recipe_id=None or title= must be provided`

Trong khi lifecycle với `date` + title có nội dung tạo thành công.

### Classification
**OBS-01 — contract/schema limitation observation**

Không tính là defect mới vì validation failure trả `422`, là status đã được contract document.

---

# 6. P1-D — Recipe

## 6.1 Happy-path lifecycle

Test:

`tests/schemathesis/test_p1_recipe_lifecycle.py`

Valid payload:

```json
{
  "name": "K05 P1 Recipe <unique>"
}
```

Runtime POST response là JSON string chứa slug, ví dụ:

`"k05-p1-recipe-1328bc78"`

Do đó test harness được sửa để dùng slug string trực tiếp.

Luồng:

| Step | Result |
|---|---:|
| POST valid recipe | 201 |
| GET by slug | 200 |
| DELETE | 200 |
| GET after delete | 404 |

Final result:

`1 passed`

### Harness issue
**TEST-06:** Ban đầu test giả định POST trả recipe object. Runtime thực tế trả slug string. Test đã được sửa và lifecycle PASS.

---

# 7. DEF-04 — Controlled Reproduction

## 7.1 Mục tiêu

Trong P0, một Schemathesis CLI run ngoài intended P0 selection đã gửi:

```json
{
  "name": ""
}
```

tới:

`POST /api/recipes`

và nhận HTTP `500`.

Finding được giữ ở trạng thái candidate cho đến khi có controlled reproduction.

---

## 7.2 Reproducer

Test:

`tests/schemathesis/test_p1_recipe_empty_name.py`

Payload:

```json
{
  "name": ""
}
```

Test gửi cùng request **3 lần**.

### Actual results

| Attempt | Status |
|---|---:|
| 1 | 500 |
| 2 | 500 |
| 3 | 500 |

Status results:

`[500, 500, 500]`

Response:

```json
{
  "detail": {
    "message": "Unknown Error",
    "error": true,
    "exception": "AssertionError"
  }
}
```

### OpenAPI contract
POST `/api/recipes` document response:

- `201`
- `422`

HTTP `500` không nằm trong documented response set.

---

## 7.3 Classification

DEF-04 được nâng từ:

`CANDIDATE`

thành:

`CONFIRMED / REPRODUCIBLE`

Reproducibility:

**3/3**

Phân loại:

- Unexpected server-side failure
- Undocumented HTTP status
- Input-validation robustness defect
- Schema-based/fuzz finding

Root cause source-level chưa được phân tích; runtime chỉ expose `AssertionError`.

---

## 7.4 Ý nghĩa của pytest FAILED

Test DEF-04 kết thúc với:

`FAILED`

Đây là **expected defect-detection failure**, không phải lỗi của test harness.

Assertion yêu cầu status thuộc:

`{201, 422}`

nhưng server trả:

`500`

Do đó failure được giữ làm regression/evidence cho defect.

Không thay assertion thành `status == 500` chỉ để suite xanh.

---

# 8. Tổng kết P1

## Functional lifecycle results

| Area | Lifecycle | Boundary | New SUT defect |
|---|---|---|---:|
| Shopping List | PASS | PASS | 0 |
| Shopping Item | PASS | PASS | 0 |
| Meal Plan | PASS | PASS | 0 |
| Recipe | PASS | DEF-04 reproducer intentionally fails | 1 confirmed |

### Additional findings
- TEST-05: Shopping Item response wrapper assumption — fixed.
- TEST-06: Recipe POST slug-string response assumption — fixed.
- OBS-01: Meal Plan cross-field validation not obvious from required-field list.

---

# 9. Defect state after P1

Confirmed defect families for the project:

| ID | Finding | State |
|---|---|---|
| DEF-01 | Empty `foods` query → 500 | CONFIRMED |
| DEF-02 | `orderBy=null` → undocumented 400 | CONFIRMED |
| DEF-03 | Missing detail resource → undocumented 404 | CONFIRMED |
| DEF-04 | Empty recipe name → 500 / AssertionError | CONFIRMED |

**Total confirmed defect families: 4**

P1 itself confirms **DEF-04** and adds no other confirmed SUT defect family.

---

# 10. Cleanup / Safety

P1 follows các nguyên tắc:

- Chỉ thao tác dữ liệu test.
- Dùng unique marker/prefix cho resource tạm.
- Child resource được cleanup trước parent khi cần.
- `finally` cleanup được sử dụng cho destructive tests.
- Không commit `MEALIE_API_TOKEN`.
- Không broad-fuzz write endpoints.
- Không dùng dữ liệu người dùng thật.
- Resource được tạo trong happy-path lifecycle được xóa sau test.

---

# 11. Files chính của P1

```text
tests/schemathesis/
├── test_p1_shopping_list_lifecycle.py
├── test_p1_shopping_list_boundaries.py
├── test_p1_shopping_item_lifecycle.py
├── test_p1_shopping_item_boundaries.py
├── test_p1_mealplan_lifecycle.py
├── test_p1_mealplan_boundaries.py
├── test_p1_recipe_lifecycle.py
└── test_p1_recipe_empty_name.py
```

Living defect log:

`docs/defects/R02-K05-Mealie-QA-Issue-Defect-Log.md`

P1 summary:

`reports/summarized/Phase-3-P1-Lifecycle-Summary.md`

---

# 12. P1 Exit Assessment

P1 controlled lifecycle work is functionally complete for the selected resource scope:

- Shopping List lifecycle verified.
- Shopping Item lifecycle verified.
- Meal Plan lifecycle verified.
- Recipe create/read/delete lifecycle verified.
- Controlled boundary tests executed.
- Write operations constrained to QA-created resources.
- Cleanup strategy verified.
- DEF-04 reproduced 3/3 and promoted to confirmed/reproducible.
- Harness issues separated from SUT defects.
- Contract limitation OBS-01 documented.

## Final P1 status

**P1 CONTROLLED LIFECYCLE / WRITE TESTING: COMPLETE**

Known intentional failing regression:

`test_p1_recipe_empty_name.py`

Failure reason:

**DEF-04 — existing confirmed SUT defect.**

---

# 13. Recommended Closeout Gate

Before merging the P1 branch:

1. Run syntax/collection checks.
2. Run normal P1 lifecycle and boundary tests.
3. Run DEF-04 reproducer separately and preserve its intentional failure output.
4. Run `git diff --check`.
5. Confirm no secrets are staged.
6. Review `git status`.
7. Commit and push `test/schemathesis-p1-lifecycle`.
8. Open PR with P1 results and DEF-04 explicitly documented.
