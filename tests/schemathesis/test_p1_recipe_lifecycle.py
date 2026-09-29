import os
import uuid

import pytest
import requests


BASE_URL = os.getenv("MEALIE_BASE_URL", "http://localhost:9091")
TOKEN = os.getenv("MEALIE_API_TOKEN")


@pytest.mark.skipif(not TOKEN, reason="MEALIE_API_TOKEN is not set")
def test_p1_recipe_lifecycle():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

    unique = uuid.uuid4().hex[:8]
    original_name = f"K05 P1 Recipe {unique}"

    slug = None
    deleted = False

    try:
        # -------------------------------------------------
        # 1. CREATE
        # -------------------------------------------------
        create_response = requests.post(
            f"{BASE_URL}/api/recipes",
            headers=headers,
            json={"name": original_name},
            timeout=10,
        )

        assert create_response.status_code == 201, (
            f"CREATE expected 201, got "
            f"{create_response.status_code}: {create_response.text}"
        )

        created = create_response.json()

        print("RECIPE CREATE:", created)

        # Mealie returns the created recipe slug directly
        # as a JSON string, not a recipe object.
        assert isinstance(created, str), (
            "Expected POST /api/recipes to return "
            f"a slug string, got: {created!r}"
        )

        slug = created

        assert slug, "Created recipe slug must not be empty"

        # -------------------------------------------------
        # 2. READ
        # -------------------------------------------------
        get_response = requests.get(
            f"{BASE_URL}/api/recipes/{slug}",
            headers=headers,
            timeout=10,
        )

        assert get_response.status_code == 200, (
            f"GET expected 200, got "
            f"{get_response.status_code}: {get_response.text}"
        )

        current = get_response.json()

        assert current["slug"] == slug
        assert current["name"] == original_name

        # -------------------------------------------------
        # 3. DELETE
        # -------------------------------------------------
        delete_response = requests.delete(
            f"{BASE_URL}/api/recipes/{slug}",
            headers=headers,
            timeout=10,
        )

        assert delete_response.status_code == 200, (
            f"DELETE expected 200, got "
            f"{delete_response.status_code}: {delete_response.text}"
        )

        deleted = True

        # -------------------------------------------------
        # 4. VERIFY CLEANUP
        # -------------------------------------------------
        after_delete = requests.get(
            f"{BASE_URL}/api/recipes/{slug}",
            headers=headers,
            timeout=10,
        )

        assert after_delete.status_code == 404, (
            f"Deleted recipe expected 404, got "
            f"{after_delete.status_code}: {after_delete.text}"
        )

    finally:
        # Cleanup only the recipe created by this test
        # if the test failed before normal deletion.
        if slug and not deleted:
            try:
                cleanup_response = requests.delete(
                    f"{BASE_URL}/api/recipes/{slug}",
                    headers=headers,
                    timeout=10,
                )

                print(
                    "RECIPE CLEANUP:",
                    cleanup_response.status_code,
                    cleanup_response.text[:200],
                )

            except requests.RequestException as exc:
                print(f"RECIPE CLEANUP FAILED: {exc}")