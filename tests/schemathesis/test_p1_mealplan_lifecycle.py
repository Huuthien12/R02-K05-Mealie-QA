import os
import uuid
from datetime import date, timedelta

import pytest
import requests


BASE_URL = os.getenv("MEALIE_BASE_URL", "http://localhost:9091")
TOKEN = os.getenv("MEALIE_API_TOKEN")


@pytest.mark.skipif(not TOKEN, reason="MEALIE_API_TOKEN is not set")
def test_p1_mealplan_lifecycle():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

    unique = uuid.uuid4().hex[:8]

    # Use a future date to avoid interfering with normal QA data.
    test_date = (date.today() + timedelta(days=30)).isoformat()

    original_title = f"K05-P1-MEALPLAN-{unique}"
    updated_title = f"{original_title}-UPDATED"

    item_id = None
    deleted = False

    try:
        # -------------------------------------------------
        # 1. CREATE
        # -------------------------------------------------
        create_payload = {
            "date": test_date,
            "entryType": "breakfast",
            "title": original_title,
            "text": "K05 P1 controlled lifecycle test",
        }

        create_response = requests.post(
            f"{BASE_URL}/api/households/mealplans",
            headers=headers,
            json=create_payload,
            timeout=10,
        )

        assert create_response.status_code == 201, (
            f"CREATE expected 201, got "
            f"{create_response.status_code}: {create_response.text}"
        )

        created = create_response.json()

        item_id = created["id"]

        assert item_id is not None
        assert created["date"] == test_date
        assert created["title"] == original_title

        # -------------------------------------------------
        # 2. READ
        # -------------------------------------------------
        get_response = requests.get(
            f"{BASE_URL}/api/households/mealplans/{item_id}",
            headers=headers,
            timeout=10,
        )

        assert get_response.status_code == 200, (
            f"GET expected 200, got "
            f"{get_response.status_code}: {get_response.text}"
        )

        current = get_response.json()

        assert current["id"] == item_id
        assert current["title"] == original_title

        # -------------------------------------------------
        # 3. UPDATE
        #
        # UpdatePlanEntry requires:
        # date, id, groupId, userId.
        # Reuse server representation and modify only
        # controlled business fields.
        # -------------------------------------------------
        update_payload = {
            "date": current["date"],
            "id": current["id"],
            "groupId": current["groupId"],
            "userId": current["userId"],
            "entryType": current.get("entryType", "breakfast"),
            "title": updated_title,
            "text": "K05 P1 controlled lifecycle test - updated",
            "recipeId": current.get("recipeId"),
        }

        update_response = requests.put(
            f"{BASE_URL}/api/households/mealplans/{item_id}",
            headers=headers,
            json=update_payload,
            timeout=10,
        )

        assert update_response.status_code == 200, (
            f"UPDATE expected 200, got "
            f"{update_response.status_code}: {update_response.text}"
        )

        # -------------------------------------------------
        # 4. VERIFY UPDATE
        # -------------------------------------------------
        verify_response = requests.get(
            f"{BASE_URL}/api/households/mealplans/{item_id}",
            headers=headers,
            timeout=10,
        )

        assert verify_response.status_code == 200

        updated = verify_response.json()

        assert updated["id"] == item_id
        assert updated["title"] == updated_title
        assert (
            updated["text"]
            == "K05 P1 controlled lifecycle test - updated"
        )

        # -------------------------------------------------
        # 5. DELETE
        # -------------------------------------------------
        delete_response = requests.delete(
            f"{BASE_URL}/api/households/mealplans/{item_id}",
            headers=headers,
            timeout=10,
        )

        assert delete_response.status_code == 200, (
            f"DELETE expected 200, got "
            f"{delete_response.status_code}: {delete_response.text}"
        )

        deleted = True

        # -------------------------------------------------
        # 6. VERIFY CLEANUP
        # -------------------------------------------------
        after_delete = requests.get(
            f"{BASE_URL}/api/households/mealplans/{item_id}",
            headers=headers,
            timeout=10,
        )

        assert after_delete.status_code == 404, (
            f"Deleted meal plan expected 404, got "
            f"{after_delete.status_code}: {after_delete.text}"
        )

    finally:
        # Delete only the entry created by this test.
        if item_id is not None and not deleted:
            try:
                requests.delete(
                    f"{BASE_URL}/api/households/mealplans/{item_id}",
                    headers=headers,
                    timeout=10,
                )
            except requests.RequestException:
                pass