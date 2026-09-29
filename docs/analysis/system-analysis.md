# System analysis

## Baseline

| Item | Value |
| --- | --- |
| SUT | Mealie v3.28.0 |
| Source commit | `0552eaa4a80031b8572849cca0ed95d07f1be001` |
| Test target | local `http://localhost:9091` only |
| Contract analysed | `schema/snapshots/mealie-v3.28.0-openapi.json` |
| OpenAPI version | 3.1.0 |

This phase analyses the saved contract only. It neither changes Mealie nor runs API automation.

## Relevant domain model

The prepared local data supplies one recipe (**QA Test Fried Rice**), one shopping list (**QA Test Shopping List**), and a meal-plan entry referring to the recipe. The contract exposes their household-scoped resources through authenticated APIs:

| Domain | Collection | Item | Contract evidence |
| --- | --- | --- | --- |
| Recipe | `GET`, `POST`, `PUT`, `PATCH /api/recipes` | `GET`, `PUT`, `PATCH`, `DELETE /api/recipes/{slug}` | `Recipe: CRUD` |
| Shopping list | `GET`, `POST /api/households/shopping/lists` | `GET`, `PUT`, `DELETE /api/households/shopping/lists/{item_id}` | `Households: Shopping Lists` |
| Shopping item | `GET`, `POST`, `PUT`, `DELETE /api/households/shopping/items` | `GET`, `PUT`, `DELETE /api/households/shopping/items/{item_id}` | `Households: Shopping List Items` |
| Meal plan | `GET`, `POST /api/households/mealplans` | `GET`, `PUT`, `DELETE /api/households/mealplans/{item_id}` | `Households: Meal Plans` |

All four areas declare `OAuth2PasswordBearer` on the operations above. The single declared security scheme is OAuth2 password flow with token URL `/api/auth/token`.

## State boundary

`GET` operations are read-only candidates. `POST`, `PUT`, `PATCH`, and `DELETE` are state-changing candidates even when the operation name is not explicit. The POC must use a dedicated QA account and uniquely prefixed disposable resources for create/update/delete checks. It must not mutate the three baseline fixtures unless their identifiers were explicitly recorded for restoration.

## Contract limitations

- The snapshot declares response contracts and validation responses, but does not define authorization-role outcomes such as 401/403 for every protected operation.
- Most resource operations list `200` and `422`, but do not document a 404 response; absence from the contract is not evidence that a missing resource succeeds.
- The schema cannot prove persistence, household isolation, idempotency, or rollback behaviour. Those are follow-up observations, not contract-only oracles.
- Authentication token acquisition requires local credentials, which must remain outside Git.
