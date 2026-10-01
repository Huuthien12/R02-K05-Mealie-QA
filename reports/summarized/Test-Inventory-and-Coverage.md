# Test Inventory and Coverage

Status below is based on retained Phase 3/4 evidence, not a new authenticated replay.

| Module | Phase | API area / mode | Purpose and expected behavior | Defect / cleanup | Evidence status |
| --- | --- | --- | --- | --- |
| `test_p0_selection.py` | P0 | Snapshot, offline/read-only selection | Confirms exactly the nine selected GET operations. | None; no requests. | Passed. |
| `test_p0_smoke.py` | P0 | Recipes, read-only | Bounded schema-derived recipe GET smoke. | DEF-01 candidate path; no cleanup. | P0 evidence retained. |
| `test_p0_collections.py` | P0 | Recipes, lists, items, meal plans; read-only | Exercises five collection/today GET operations with contract checks. | DEF-01 and DEF-02; no cleanup. | `4 failed, 1 passed` (known detections). |
| `test_p0_details.py` | P0 | Recipe/list/item/meal-plan detail; read-only | Exercises four detail GET operations with contract checks. | DEF-03; no cleanup. | `2 failed, 2 passed` (known detections). |
| `test_p1_shopping_list_lifecycle.py` | P1 | Shopping lists, write | Create/read/update/delete an isolated list. | Deletes created list. | Passed. |
| `test_p1_shopping_list_boundaries.py` | P1 | Shopping lists, write | Tests `{}`, null name, and empty name against documented statuses. | Deletes any created list. | 3 passed. |
| `test_p1_shopping_item_lifecycle.py` | P1 | Shopping items, write | Creates parent list then creates/reads/updates/deletes item. | Deletes item, then parent. | Passed. |
| `test_p1_shopping_item_boundaries.py` | P1 | Shopping items, write | Controlled valid/invalid item payloads. | Deletes created items, then parent. | Passed. |
| `test_p1_mealplan_lifecycle.py` | P1 | Meal plans, write | Create/read/update/delete disposable entry. | Deletes created entry. | Passed. |
| `test_p1_mealplan_boundaries.py` | P1 | Meal plans, write | Controlled boundary inputs, expecting documented validation outcomes. | No intentional persistence. | Passed. |
| `test_p1_recipe_lifecycle.py` | P1 | Recipes, write | Create/read/delete a uniquely named recipe. | Deletes created recipe. | Passed. |
| `test_p1_recipe_empty_name.py` | P1 | Recipes, write boundary | Reproduces empty-name contract/server-error behavior. | No resource created in retained evidence. | Intentionally fails for DEF-04. |

## Coverage summary

- P0 selected/exercised: 9/9 authenticated GET operations: recipe collection/detail; shopping-list collection/detail; shopping-item collection/detail; meal-plan collection/detail/today.
- P1 lifecycle areas: shopping lists, shopping items, meal plans, and recipes.
- P1 boundary areas: shopping list, shopping item, meal plan, plus the isolated DEF-04 recipe boundary reproducer.
- Known-defect regressions: DEF-01 through DEF-03 are P0 detections; DEF-04 is a separate expected failing P1 test.
- Intentionally excluded: auth/token/password routes; admin, backup, maintenance, import/export, bulk, upload/assets, streaming, webhooks, external utilities, and all public targets. No claim is made for untested endpoints.
