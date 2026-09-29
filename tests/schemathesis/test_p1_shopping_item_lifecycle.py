import os
import uuid

import pytest
import requests


BASE_URL = os.getenv("MEALIE_BASE_URL", "http://localhost:9091")
TOKEN = os.getenv("MEALIE_API_TOKEN")


@pytest.mark.skipif(not TOKEN, reason="MEALIE_API_TOKEN is not set")
def test_p1_shopping_item_lifecycle():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

    unique = uuid.uuid4().hex[:8]

    list_id = None
    item_id = None
    item_deleted = False
    list_deleted = False

    try:
        # -------------------------------------------------
        # 1. CREATE TEMPORARY PARENT SHOPPING LIST
        # -------------------------------------------------
        list_response = requests.post(
            f"{BASE_URL}/api/households/shopping/lists",
            headers=headers,
            json={"name": f"K05-P1-ITEM-PARENT-{unique}"},
            timeout=10,
        )

        assert list_response.status_code == 201, (
            f"Parent CREATE expected 201, got "
            f"{list_response.status_code}: {list_response.text}"
        )

        list_id = list_response.json()["id"]
        assert list_id

        # -------------------------------------------------
        # 2. CREATE SHOPPING ITEM
        # -------------------------------------------------
        create_payload = {
            "shoppingListId": list_id,
            "quantity": 1,
            "note": f"K05-P1-ITEM-{unique}",
            "display": f"K05-P1-ITEM-{unique}",
            "checked": False,
        }

        create_response = requests.post(
            f"{BASE_URL}/api/households/shopping/items",
            headers=headers,
            json=create_payload,
            timeout=10,
        )

        assert create_response.status_code == 201, (
            f"Item CREATE expected 201, got "
            f"{create_response.status_code}: {create_response.text}"
        )

        created = create_response.json()

        created_items = created.get("createdItems", [])

        assert len(created_items) == 1, (
            f"Expected exactly 1 created item, got: {created}"
        )

        created_item = created_items[0]
        item_id = created_item["id"]

        assert item_id
        assert created_item["shoppingListId"] == list_id

        # -------------------------------------------------
        # 3. READ ITEM
        # -------------------------------------------------
        get_response = requests.get(
            f"{BASE_URL}/api/households/shopping/items/{item_id}",
            headers=headers,
            timeout=10,
        )

        assert get_response.status_code == 200, (
            f"Item GET expected 200, got "
            f"{get_response.status_code}: {get_response.text}"
        )

        current = get_response.json()

        assert current["id"] == item_id
        assert current["shoppingListId"] == list_id

        # -------------------------------------------------
        # 4. UPDATE ITEM
        # -------------------------------------------------
        update_payload = {
            "shoppingListId": list_id,
            "quantity": 2,
            "note": f"K05-P1-ITEM-{unique}-UPDATED",
            "display": f"K05-P1-ITEM-{unique}-UPDATED",
            "checked": True,
            "position": current.get("position", 0),
        }

        update_response = requests.put(
            f"{BASE_URL}/api/households/shopping/items/{item_id}",
            headers=headers,
            json=update_payload,
            timeout=10,
        )

        assert update_response.status_code == 200, (
            f"Item UPDATE expected 200, got "
            f"{update_response.status_code}: {update_response.text}"
        )

        # -------------------------------------------------
        # 5. VERIFY UPDATE
        # -------------------------------------------------
        verify_response = requests.get(
            f"{BASE_URL}/api/households/shopping/items/{item_id}",
            headers=headers,
            timeout=10,
        )

        assert verify_response.status_code == 200

        updated = verify_response.json()

        assert updated["id"] == item_id
        assert updated["shoppingListId"] == list_id
        assert updated["quantity"] == 2
        assert updated["checked"] is True
        assert updated.get("note") == f"K05-P1-ITEM-{unique}-UPDATED"

        # -------------------------------------------------
        # 6. DELETE ITEM
        # -------------------------------------------------
        delete_response = requests.delete(
            f"{BASE_URL}/api/households/shopping/items/{item_id}",
            headers=headers,
            timeout=10,
        )

        assert delete_response.status_code == 200, (
            f"Item DELETE expected 200, got "
            f"{delete_response.status_code}: {delete_response.text}"
        )

        item_deleted = True

        # -------------------------------------------------
        # 7. VERIFY ITEM CLEANUP
        # -------------------------------------------------
        after_delete = requests.get(
            f"{BASE_URL}/api/households/shopping/items/{item_id}",
            headers=headers,
            timeout=10,
        )

        assert after_delete.status_code == 404, (
            f"Deleted item expected 404, got "
            f"{after_delete.status_code}: {after_delete.text}"
        )

        # -------------------------------------------------
        # 8. DELETE TEMPORARY PARENT LIST
        # -------------------------------------------------
        parent_delete = requests.delete(
            f"{BASE_URL}/api/households/shopping/lists/{list_id}",
            headers=headers,
            timeout=10,
        )

        assert parent_delete.status_code == 200, (
            f"Parent DELETE expected 200, got "
            f"{parent_delete.status_code}: {parent_delete.text}"
        )

        list_deleted = True

    finally:
        # Cleanup child first.
        if item_id and not item_deleted:
            try:
                requests.delete(
                    f"{BASE_URL}/api/households/shopping/items/{item_id}",
                    headers=headers,
                    timeout=10,
                )
            except requests.RequestException:
                pass

        # Then cleanup temporary parent.
        if list_id and not list_deleted:
            try:
                requests.delete(
                    f"{BASE_URL}/api/households/shopping/lists/{list_id}",
                    headers=headers,
                    timeout=10,
                )
            except requests.RequestException:
                pass