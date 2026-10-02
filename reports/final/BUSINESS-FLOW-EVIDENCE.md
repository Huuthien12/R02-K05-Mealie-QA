# Evidence cho business flows

Tất cả kết quả bên dưới là **RETAINED HISTORICAL EVIDENCE**, không phải rerun của compliance pass. Normal P1 total vẫn là `9 passed`; DEF-04 không được trộn vào business-flow success evidence.

| Flow | Test module | Precondition / sequence | Historical result / cleanup | Evidence |
| --- | --- | --- | --- | --- |
| Shopping List | `test_p1_shopping_list_lifecycle.py` | QA token; POST→GET→PUT→GET→DELETE→GET. | PASS; deletes created list only. | Phase-3-P1 summary. |
| Shopping Item | `test_p1_shopping_item_lifecycle.py` | Temporary parent; POST item→GET→PUT→GET→DELETE item→DELETE parent. | PASS; child cleanup before parent. | Phase-3-P1 summary. |
| Meal Plan | `test_p1_mealplan_lifecycle.py` | Controlled entry; POST→GET→PUT→GET→DELETE→GET. | PASS; deletes created entry. | Phase-3-P1 summary. |
| Recipe | `test_p1_recipe_lifecycle.py` | Unique recipe; POST→GET slug→DELETE→GET. | PASS; deletes created recipe. | Phase-3-P1 summary. |
