import os

import pytest
import requests


BASE_URL = os.getenv("MEALIE_BASE_URL", "http://localhost:9091")
TOKEN = os.getenv("MEALIE_API_TOKEN")

CASES = [
    ("empty_object", {}),
    ("null_name", {"name": None}),
    ("empty_name", {"name": ""}),
]


@pytest.mark.skipif(not TOKEN, reason="MEALIE_API_TOKEN is not set")
@pytest.mark.parametrize("case_name,payload", CASES)
def test_p1_shopping_list_create_boundaries(case_name, payload):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

    resource_id = None

    try:
        response = requests.post(
            f"{BASE_URL}/api/households/shopping/lists",
            headers=headers,
            json=payload,
            timeout=10,
        )

        print(
            f"{case_name}: "
            f"status={response.status_code}, "
            f"body={response.text[:500]}"
        )

        # OpenAPI documents only 201 and 422.
        assert response.status_code in {201, 422}, (
            f"{case_name}: undocumented status "
            f"{response.status_code}: {response.text}"
        )

        if response.status_code == 201:
            body = response.json()
            resource_id = body.get("id")
            assert resource_id, (
                f"{case_name}: 201 response did not contain an id"
            )

    finally:
        # Delete only a resource created by this test.
        if resource_id:
            try:
                requests.delete(
                    f"{BASE_URL}/api/households/shopping/lists/{resource_id}",
                    headers=headers,
                    timeout=10,
                )
            except requests.RequestException:
                pass