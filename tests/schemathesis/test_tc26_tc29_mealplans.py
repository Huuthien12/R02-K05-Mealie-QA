"""Directed Meal Plan expansion cases TC-26…TC-29."""

import requests

from tc22_tc37_helpers import (
    BASE_URL,
    HEADERS,
    TOKEN,
    assert_status,
    create_mealplan,
    delete,
    get,
    mealplan_update_payload,
    require_p1,
    unique,
)


def test_tc26_reversed_mealplan_date_range():
    """TC-26 | REQ-MLP-01 | C: GET returns 200 or 422, never an undocumented 5xx."""
    if not TOKEN:
        import pytest

        pytest.skip("MEALIE_API_TOKEN is not set")
    response = requests.get(
        f"{BASE_URL}/api/households/mealplans",
        headers=HEADERS,
        params={"start_date": "2026-11-20", "end_date": "2026-11-01"},
        timeout=10,
    )
    assert_status(response, {200, 422}, "TC-26")
    if response.status_code == 200:
        payload = response.json()
        assert isinstance(payload, dict) and isinstance(payload.get("items"), list), (
            "TC-26: PlanEntryPagination requires an items array"
        )


def test_tc27_mealplan_second_update_is_final_state():
    """TC-27 | REQ-MLP-05 | C: PUT 200/422; T: second successful write is readable."""
    require_p1()
    item = None
    try:
        item = create_mealplan("22-27")
        current = get(f"/api/households/mealplans/{item['id']}")
        assert current.status_code == 200
        first_title = unique("22-27-first")
        first = requests.put(
            f"{BASE_URL}/api/households/mealplans/{item['id']}",
            headers=HEADERS,
            json=mealplan_update_payload(current.json(), title=first_title),
            timeout=10,
        )
        assert_status(first, {200, 422}, "TC-27 first PUT")
        if first.status_code == 422:
            return
        after_first = get(f"/api/households/mealplans/{item['id']}")
        assert after_first.status_code == 200
        final_title = unique("22-27-final")
        second = requests.put(
            f"{BASE_URL}/api/households/mealplans/{item['id']}",
            headers=HEADERS,
            json=mealplan_update_payload(after_first.json(), title=final_title),
            timeout=10,
        )
        assert_status(second, {200, 422}, "TC-27 second PUT")
        if second.status_code == 200:
            assert get(f"/api/households/mealplans/{item['id']}").json().get("title") == final_title
    finally:
        if item:
            delete(f"/api/households/mealplans/{item['id']}")


def test_tc28_delete_missing_mealplan_integer_id():
    """TC-28 | REQ-MLP-06 | C: DELETE valid missing ID returns 200 or 422."""
    require_p1()
    if get("/api/households/mealplans/0").status_code == 200:
        import pytest

        pytest.skip("TC-28 requires 0 to remain a missing meal plan id")
    response = requests.delete(f"{BASE_URL}/api/households/mealplans/0", headers=HEADERS, timeout=10)
    assert_status(response, {200, 422}, "TC-28")


def test_tc29_invalid_mealplan_date_preserves_data_on_rejection():
    """TC-29 | REQ-MLP-05/07 | C: PUT 200/422; T: rejected update preserves data."""
    require_p1()
    item = None
    try:
        item = create_mealplan("22-29")
        current_response = get(f"/api/households/mealplans/{item['id']}")
        assert current_response.status_code == 200
        current = current_response.json()
        response = requests.put(
            f"{BASE_URL}/api/households/mealplans/{item['id']}",
            headers=HEADERS,
            json=mealplan_update_payload(current, date="not-a-date"),
            timeout=10,
        )
        assert_status(response, {200, 422}, "TC-29")
        if response.status_code == 422:
            after = get(f"/api/households/mealplans/{item['id']}")
            assert after.status_code == 200
            assert after.json().get("date") == current.get("date")
            assert after.json().get("title") == current.get("title")
    finally:
        if item:
            delete(f"/api/households/mealplans/{item['id']}")
