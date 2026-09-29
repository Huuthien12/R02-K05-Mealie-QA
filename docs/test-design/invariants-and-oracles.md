# Invariants and oracles

All assertions below are bounded by the saved OpenAPI contract. They do not invent undocumented business rules.

| ID | Oracle | Contract basis |
| --- | --- | --- |
| O1 | A successful response must use a status code documented for that operation. | Every operation supplies a `responses` map. |
| O2 | If a documented JSON response schema is present, the response body must validate against that schema. | Examples: `ShoppingListOut`, `ShoppingListItemPagination`, `ReadPlanEntry`, `HTTPValidationError`. |
| O3 | A schema-invalid request may return documented `422` with `HTTPValidationError`; it must not yield an undocumented 5xx. | Core operations declare `422 HTTPValidationError`. |
| O4 | No response in the in-scope campaign may be 5xx. | 5xx is absent from all selected success/error response maps. |
| O5 | Requests omitting/altering a required path parameter are not valid route invocations; invalid values sent at that position must not produce 5xx. | `item_id` is required for shopping list/item and meal-plan item routes; meal-plan ID is integer, shopping IDs are strings. |
| O6 | Protected in-scope operations are run with OAuth2 bearer authentication; an unauthenticated probe, if approved, records observed behaviour rather than asserting a specific status. | Selected operations declare `OAuth2PasswordBearer`; 401/403 are not consistently declared. |
| O7 | A successful create response conforms to its documented output and supplies fields required by that output schema. | `ShoppingListOut` requires `groupId`, `userId`, `id`, `householdId`; `ReadPlanEntry` requires `date`, `id`, `groupId`, `userId`, `householdId`. |
| O8 | A resource created by the scenario is the only resource updated/deleted by that scenario, and cleanup result must have a documented success code/body. | Lifecycle routes and response maps in the snapshot. |

Not asserted: a specific 404/401/403 code, immutable fields, exact pagination semantics, ownership isolation, or post-delete nonexistence. The snapshot does not specify them sufficiently.
