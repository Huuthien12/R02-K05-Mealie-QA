import os
import uuid

import pytest
import requests


BASE_URL = os.getenv("MEALIE_BASE_URL", "http://localhost:9091")
TOKEN = os.getenv("MEALIE_API_TOKEN")


@pytest.mark.skipif(not TOKEN, reason="MEALIE_API_TOKEN is not set")
def test_p1_shopping_list_lifecycle():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

    unique = uuid.uuid4().hex[:8]
    original_name = f"K05-P1-SHOPPING-LIST-{unique}"
    updated_name = f"{original_name}-UPDATED"

    resource_id = None
    deleted = False

    try:
        # 1. CREATE
        create_response = requests.post(
            f"{BASE_URL}/api/households/shopping/lists",
            headers=headers,
            json={"name": original_name},
            timeout=10,
        )

        assert create_response.status_code == 201, (
            f"CREATE expected 201, got {create_response.status_code}: "
            f"{create_response.text}"
        )

        created = create_response.json()
        resource_id = created["id"]

        assert resource_id
        assert created.get("name") == original_name

        # 2. READ
        get_response = requests.get(
            f"{BASE_URL}/api/households/shopping/lists/{resource_id}",
            headers=headers,
            timeout=10,
        )

        assert get_response.status_code == 200, (
            f"GET expected 200, got {get_response.status_code}: "
            f"{get_response.text}"
        )

        current = get_response.json()

        assert current["id"] == resource_id
        assert current.get("name") == original_name

        # 3. UPDATE
        #
        # ShoppingListUpdate requires groupId, userId and id.
        # Reuse the server-returned representation instead of inventing IDs.
        update_payload = dict(current)
        update_payload["name"] = updated_name

        update_response = requests.put(
            f"{BASE_URL}/api/households/shopping/lists/{resource_id}",
            headers=headers,
            json=update_payload,
            timeout=10,
        )

        assert update_response.status_code == 200, (
            f"UPDATE expected 200, got {update_response.status_code}: "
            f"{update_response.text}"
        )

        # 4. VERIFY UPDATE
        verify_response = requests.get(
            f"{BASE_URL}/api/households/shopping/lists/{resource_id}",
            headers=headers,
            timeout=10,
        )

        assert verify_response.status_code == 200

        updated = verify_response.json()

        assert updated["id"] == resource_id
        assert updated.get("name") == updated_name

        # 5. DELETE
        delete_response = requests.delete(
            f"{BASE_URL}/api/households/shopping/lists/{resource_id}",
            headers=headers,
            timeout=10,
        )

        assert delete_response.status_code == 200, (
            f"DELETE expected 200, got {delete_response.status_code}: "
            f"{delete_response.text}"
        )

        deleted = True

        # 6. VERIFY CLEANUP
        after_delete = requests.get(
            f"{BASE_URL}/api/households/shopping/lists/{resource_id}",
            headers=headers,
            timeout=10,
        )

        # Runtime may reasonably return 404 here even though the current
        # OpenAPI contract does not document 404 for this operation.
        assert after_delete.status_code == 404, (
            f"Expected deleted resource to return 404, "
            f"got {after_delete.status_code}: {after_delete.text}"
        )

    finally:
        # Safety cleanup:
        # only attempt to delete the resource created by THIS test.
        if resource_id and not deleted:
            try:
                requests.delete(
                    f"{BASE_URL}/api/households/shopping/lists/{resource_id}",
                    headers=headers,
                    timeout=10,
                )
            except requests.RequestException:
                pass