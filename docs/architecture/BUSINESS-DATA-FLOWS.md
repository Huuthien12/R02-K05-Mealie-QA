# Business / Data Flows

## FLOW-01 Recipe lifecycle

Actor: QA harness. Precondition: local authenticated QA context. Input: unique valid recipe name. Sequence: POST recipe → GET by returned slug → DELETE → GET after delete. Invariant: only created recipe is deleted; normal evidence returns 201/200/200/404. Test: `test_p1_recipe_lifecycle.py`; evidence: Phase-3-P1 summary.

```mermaid
flowchart LR
  C[Create unique recipe] --> R[GET by slug] --> D[Delete same recipe] --> V[Verify 404]
```

## FLOW-02 Shopping List lifecycle

Actor: QA harness. Input: unique list name. Sequence: POST → GET → PUT with server representation → GET verify → DELETE → GET after delete. Cleanup deletes only the created list. Test: `test_p1_shopping_list_lifecycle.py`; evidence: Phase-3-P1 summary.

```mermaid
flowchart LR
  C[POST list] --> G[GET list] --> U[PUT list] --> V[GET verify] --> D[DELETE list]
```

## FLOW-03 Shopping Item lifecycle

Actor: QA harness. Precondition/input: create temporary parent shopping list and item payload referencing its returned ID. Sequence: POST parent → POST item → GET → PUT → GET verify → DELETE item → DELETE parent. Cleanup child precedes parent. Test: `test_p1_shopping_item_lifecycle.py`; evidence: Phase-3-P1 summary.

```mermaid
flowchart LR
  P[Create parent] --> C[Create item] --> U[Read/update/verify] --> D[Delete item] --> X[Delete parent]
```

## FLOW-04 Meal Plan lifecycle

Actor: QA harness. Input: controlled entry; server-returned representation supplies fields needed for update. Sequence: POST → GET → PUT → GET verify → DELETE → GET after delete. Cleanup deletes the created entry. Test: `test_p1_mealplan_lifecycle.py`; evidence: Phase-3-P1 summary.

```mermaid
flowchart LR
  C[POST entry] --> G[GET entry] --> U[PUT entry] --> V[GET verify] --> D[DELETE entry]
```

Các flow là retained historical evidence; tài liệu không tuyên bố rerun trong compliance pass.
