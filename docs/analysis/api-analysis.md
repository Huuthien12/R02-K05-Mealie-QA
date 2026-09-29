# OpenAPI analysis

## Contract statistics

The snapshot declares **182 paths** and **266 operations**.

| Method | Operations |
| --- | ---: |
| GET | 115 |
| POST | 82 |
| PUT | 36 |
| PATCH | 3 |
| DELETE | 30 |

## Endpoint groups

The tags form these useful families (operation counts in parentheses):

- Recipe: CRUD (25), Bulk Actions (8), Comments (11), Images and Assets (10), Timeline (6), Exports (2), Shared (2), Ingredient Parser (2).
- Household: Shopping Lists (18), Shopping List Items (16), Meal Plans (14), Self Service (14), Webhooks (14), Recipe Actions (12), Cookbooks (12), Event Notifications (12), Meal Plan Rules (10), Invitations (6).
- Organizer: Categories (16), Tags (16), Tools (12); Recipes: Foods (12), Units (12).
- Group: AI Providers (12), Self Service (12), Multi Purpose Labels (10), Reports (6), and smaller configuration/migration/seeder groups.
- User: CRUD (12), Authentication (7), Ratings (5), Tokens (4), Images (3), Passwords (2), Registration (1).
- Admin: user/household/group management, backups, maintenance, email, AI providers, debug, and about.
- Public/read families: Explore, media, shared recipes, app about, and utils.

Tags may occur more than once on one operation in the snapshot, so tag counts are not a unique-operation total.

## Authentication and sensitive endpoints

`POST /api/auth/token` has form input and declares `200`/`422`. `POST /api/auth/refresh` and `POST /api/auth/logout` require `OAuth2PasswordBearer`. OAuth callback/native endpoints, user registration, password reset, API-token creation/deletion, and `/api/users/password` are excluded from fuzzing because they can issue, invalidate, or alter credentials.

## CRUD and side effects

The resource CRUD endpoints listed in [system-analysis.md](system-analysis.md) are the core testable surface. They return documented success responses and `422` validation errors; for example, shopping-list create returns `201 ShoppingListOut`, meal-plan create returns `201 ReadPlanEntry`, and item routes require `item_id` as documented path input.

Side-effecting routes also include recipe scrape/import/AI/stream creation, image and asset upload/delete, bulk actions, exports, recipe duplication, `last-made`, list-to-recipe actions, category/tag merge, webhook/event configuration, and every admin write. They require controlled data or external services and are not an initial fuzz target.

## Suitability for fuzzing

| Class | Examples | Decision |
| --- | --- | --- |
| Safe read contract checks | list/get recipe, list/get shopping list/item, list/get meal plan | Include first |
| Controlled lifecycle writes | create/update/delete a prefixed shopping list/item or meal-plan entry | Defer until the P0 read-only POC is stable and cleanup is proven |
| Existing-fixture reads | `GET /api/recipes/{slug}`, list meal plans, list shopping lists | Include; do not alter fixture |
| External, streaming, upload, bulk, destructive or credential routes | `/api/recipes/create/*`, `/stream`, `/assets`, `/bulk-actions/*`, auth/admin/backups | Exclude from POC |

The schema supports validation and response-shape checks. It does not label operations as safe, idempotent, or externally costly; those classifications are risk decisions for this project.
