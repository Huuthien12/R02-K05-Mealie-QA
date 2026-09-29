import os
import uuid

import pytest
import requests


BASE_URL = os.getenv("MEALIE_BASE_URL", "http://localhost:9091")
TOKEN = os.getenv("MEALIE_API_TOKEN")


@pytest.mark.skipif(not TOKEN, reason="MEALIE_API_TOKEN is not set")
def test_p1_shopping_item_create_boundaries():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

    unique = uuid.uuid4().hex[:8]
    list_id = None
    created_item_ids = []

    try:
        # Create isolated parent list
        parent = requests.post(
            f"{BASE_URL}/api/households/shopping/lists",
            headers=headers,
            json={"name": f"K05-P1-BOUNDARY-{unique}"},
            timeout=10,
        )

        assert parent.status_code == 201
        list_id = parent.json()["id"]

        cases = [
            (
                "minimal_valid",
                {"shoppingListId": list_id},
            ),
            (
                "null_optional_fields",
                {
                    "shoppingListId": list_id,
                    "food": None,
                    "unit": None,
                    "note": None,
                    "foodId": None,
                    "labelId": None,
                    "unitId": None,
                },
            ),
            (
                "zero_quantity",
                {
                    "shoppingListId": list_id,
                    "quantity": 0,
                },
            ),
            (
                "negative_quantity",
                {
                    "shoppingListId": list_id,
                    "quantity": -1,
                },
            ),
            (
                "missing_required_shopping_list_id",
                {},
            ),
            (
                "invalid_uuid",
                {
                    "shoppingListId": "not-a-uuid",
                },
            ),
        ]

        for case_name, payload in cases:
            response = requests.post(
                f"{BASE_URL}/api/households/shopping/items",
                headers=headers,
                json=payload,
                timeout=10,
            )

            print(
                f"{case_name}: "
                f"status={response.status_code}, "
                f"body={response.text[:500]}"
            )

            # OpenAPI documents POST responses as 201 or 422.
            assert response.status_code in {201, 422}, (
                f"{case_name}: undocumented status "
                f"{response.status_code}: {response.text}"
            )

            # Track anything successfully created for cleanup.
            if response.status_code == 201:
                body = response.json()

                for item in body.get("createdItems", []):
                    item_id = item.get("id")
                    if item_id:
                        created_item_ids.append(item_id)

    finally:
        # Child resources first
        for item_id in created_item_ids:
            try:
                requests.delete(
                    f"{BASE_URL}/api/households/shopping/items/{item_id}",
                    headers=headers,
                    timeout=10,
                )
            except requests.RequestException:
                pass

        # Parent resource last
        if list_id:
            try:
                requests.delete(
                    f"{BASE_URL}/api/households/shopping/lists/{list_id}",
                    headers=headers,
                    timeout=10,
                )
            except requests.RequestException:
                pass