import os

import pytest
import requests


BASE_URL = os.getenv("MEALIE_BASE_URL", "http://localhost:9091")
TOKEN = os.getenv("MEALIE_API_TOKEN")


@pytest.mark.skipif(not TOKEN, reason="MEALIE_API_TOKEN is not set")
def test_recipe_empty_name_def04_reproduction():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

    results = []

    # Repeat 3 times to establish reproducibility.
    for attempt in range(1, 4):
        response = requests.post(
            f"{BASE_URL}/api/recipes",
            headers=headers,
            json={"name": ""},
            timeout=10,
        )

        print()
        print(f"DEF-04 ATTEMPT {attempt}")
        print(f"STATUS: {response.status_code}")
        print(f"BODY: {response.text[:1000]}")

        results.append(response.status_code)

        # A successful creation would require cleanup.
        # At this stage we do not expect 201, but handle it safely.
        if response.status_code == 201:
            try:
                created = response.json()

                if isinstance(created, str) and created:
                    cleanup = requests.delete(
                        f"{BASE_URL}/api/recipes/{created}",
                        headers=headers,
                        timeout=10,
                    )

                    print(
                        "CLEANUP:",
                        cleanup.status_code,
                        cleanup.text[:200],
                    )

            except (ValueError, requests.RequestException) as exc:
                print(f"CLEANUP WARNING: {exc}")

    print()
    print("DEF-04 STATUS RESULTS:", results)

    # OpenAPI documents POST /api/recipes as 201 or 422.
    # Any other status is a contract / server-behavior candidate.
    assert all(status in {201, 422} for status in results), (
        "DEF-04 reproduced: POST /api/recipes with "
        f'{{"name": ""}} returned undocumented status codes: {results}'
    )