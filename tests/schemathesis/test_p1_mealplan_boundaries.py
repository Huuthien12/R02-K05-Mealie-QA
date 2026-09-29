import os
from datetime import date, timedelta

import pytest
import requests


BASE_URL = os.getenv("MEALIE_BASE_URL", "http://localhost:9091")
TOKEN = os.getenv("MEALIE_API_TOKEN")


@pytest.mark.skipif(not TOKEN, reason="MEALIE_API_TOKEN is not set")
def test_p1_mealplan_create_boundaries():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

    valid_date = (date.today() + timedelta(days=40)).isoformat()
    created_ids = []

    cases = [
        (
            "minimal_valid",
            {"date": valid_date},
        ),
        (
            "empty_title",
            {
                "date": valid_date,
                "title": "",
            },
        ),
        (
            "null_recipe_id",
            {
                "date": valid_date,
                "recipeId": None,
            },
        ),
        (
            "missing_required_date",
            {},
        ),
        (
            "invalid_date_format",
            {
                "date": "not-a-date",
            },
        ),
        (
            "invalid_recipe_uuid",
            {
                "date": valid_date,
                "recipeId": "not-a-uuid",
            },
        ),
        (
            "invalid_entry_type",
            {
                "date": valid_date,
                "entryType": "not-a-meal-type",
            },
        ),
    ]

    try:
        for case_name, payload in cases:
            response = requests.post(
                f"{BASE_URL}/api/households/mealplans",
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

            if response.status_code == 201:
                body = response.json()
                item_id = body.get("id")

                assert item_id is not None, (
                    f"{case_name}: 201 response missing id: {body}"
                )

                created_ids.append(item_id)

    finally:
        # Cleanup only entries created by this test.
        for item_id in created_ids:
            try:
                requests.delete(
                    f"{BASE_URL}/api/households/mealplans/{item_id}",
                    headers=headers,
                    timeout=10,
                )
            except requests.RequestException:
                pass