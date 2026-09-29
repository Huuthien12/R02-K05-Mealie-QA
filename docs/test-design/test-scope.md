# Test scope

## In scope

| Priority | Operations | Mode | Why |
| --- | --- | --- | --- |
| P0 | `GET /api/recipes`, `GET /api/recipes/{slug}` | read-only | Core prepared recipe; documented `200`/`422` contract. |
| P0 | `GET /api/households/shopping/lists`, `GET /api/households/shopping/lists/{item_id}`; equivalent shopping-item GETs | read-only | Covers prepared shopping-list data and path/query validation. |
| P0 | `GET /api/households/mealplans`, `GET /api/households/mealplans/{item_id}`, `GET /api/households/mealplans/today` | read-only | Covers prepared meal-plan data and typed integer item ID. |
| P1 | `POST`/`PUT`/`DELETE` for shopping lists/items and meal plans | controlled write | Clear request/response schemas and small disposable QA data. |
| P1 | `POST`/`PUT`/`PATCH`/`DELETE` recipe endpoints | controlled write | Relevant CRUD contract, but only against an independently created test recipe. |
| P2 | organizer categories/tags/tools CRUD | controlled write | Ordinary authenticated CRUD, not required by existing fixture flow. |

The first Phase 3 POC executes **P0 read-only only**. P1 disposable writes are deferred until that POC is stable; P2 is not part of the POC.

## Out of scope for the Schemathesis POC

- Authentication, OAuth, registration, password and API-token routes.
- User, group and household administration; backups, maintenance, email and debug endpoints.
- Webhooks, invitations, notifications, AI providers, migrations and seeders.
- Recipe scrape/import/AI/stream endpoints, multipart image/assets, bulk actions, exports, share tokens, merges and external download utilities.
- Public Explore/media routes: useful later for unauthenticated contract checks, but not required for the protected QA-data flow.

These exclusions minimise credential churn, external calls, long-running work, irreversible changes, and cross-member interference. They are risk exclusions, not claims that the endpoints are defective or unsupported.

## Execution guardrails

1. Target only `http://localhost:9091` with the snapshot version pinned above.
2. Obtain credentials/token locally; never write them to files tracked by Git.
3. Run read-only cases first. Enable write methods only with a unique prefix, recorded created IDs/slugs, and cleanup.
4. Do not use the known recipe, shopping list, or meal-plan fixture as a delete/update target.
