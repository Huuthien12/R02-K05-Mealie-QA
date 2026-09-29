# Business flows

## 1. Read the prepared meal-planning dataset

1. Authenticate locally.
2. List recipes with `GET /api/recipes` and locate the prepared recipe by returned data.
3. List shopping lists with `GET /api/households/shopping/lists` and retrieve a returned list with `GET /api/households/shopping/lists/{item_id}`.
4. List meal plans with `GET /api/households/mealplans`; retrieve an entry through `GET /api/households/mealplans/{item_id}`.

This flow verifies contract-compatible reads without assuming undocumented field relationships.

## 2. Disposable shopping-list lifecycle

1. Create a uniquely named list with `POST /api/households/shopping/lists` (`ShoppingListCreate` → `201 ShoppingListOut`).
2. Read it by returned `id`, update it with `PUT`, then create a shopping item using `POST /api/households/shopping/items` (`ShoppingListItemCreate` requires `shoppingListId`).
3. Read/update/delete the created item, then delete the created list.

The cleanup order prevents an item from being left associated with a deleted disposable list.

## 3. Disposable meal-plan lifecycle

1. Create an entry through `POST /api/households/mealplans`; `CreatePlanEntry` requires `date` and the successful contract is `201 ReadPlanEntry`.
2. Read/update the returned integer `id`.
3. Delete the same entry; the documented success body is `ReadPlanEntry`.

Use a separate entry from the prepared meal plan.

## 4. Recipe lifecycle (P1)

Create an independently named recipe via `POST /api/recipes`, retrieve it by returned slug, exercise the documented update/patch route, and delete it. The snapshot exposes the operations but `Recipe-Input` declares no required properties; generated requests must therefore be treated as schema-valid candidates, not assumed business-valid recipes.
