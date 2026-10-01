# Final Defect Summary

This is a concise reporting view. The canonical historical record is [the living defect log](../../docs/defects/R02-K05-Mealie-QA-Issue-Defect-Log.md).

| ID | Endpoint(s) and trigger | Contract / observed behavior | Reproduction | Classification and RCA | Evidence / test | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| DEF-01 | `GET /api/recipes?foods=` | Snapshot: `200`, `422`; observed: `500`. | 3/3 | Server-error / undocumented status; **LIKELY IMPLEMENTATION PATH**. | [evidence](../../evidence/defects/DEF-01-recipe-empty-foods-500.md); `test_p0_smoke.py`, `test_p0_collections.py` | Open; retain reproducer. |
| DEF-02 | Three shopping-list/item/meal-plan collections with `orderBy=null` | Snapshot permits nullable value and documents `200`, `422`; observed: `400`. | 9/9 | Contract/documentation defect; **CONFIRMED ROOT CAUSE**. | [evidence](../../evidence/defects/DEF-02-orderby-null-undocumented-400.md); `test_p0_collections.py` | Open; retain reproducer. |
| DEF-03 | `GET /api/recipes/0`; `GET /api/households/mealplans/0` | Snapshot: `200`, `422`; observed: `404`. | 6/6 | Contract/documentation defect; **CONFIRMED ROOT CAUSE**. | [evidence](../../evidence/defects/DEF-03-undocumented-404.md); `test_p0_details.py` | Open; retain reproducer. |
| DEF-04 | `POST /api/recipes` with `{"name":""}` | Snapshot: `201`, `422`; observed: `500` / `AssertionError`. | 3/3 | Input-validation server-error / undocumented status; **CONFIRMED ROOT CAUSE**. | [evidence](../../evidence/defects/DEF-04-empty-recipe-name-500.md); `test_p1_recipe_empty_name.py` | Open; expected failing regression. |

Totals: 4 confirmed defect families; 2 server-error families (DEF-01, DEF-04); 2 contract/documentation families (DEF-02, DEF-03). DEF-01 and DEF-04 also have undocumented status responses, but are counted in the server-error total to avoid double counting.
