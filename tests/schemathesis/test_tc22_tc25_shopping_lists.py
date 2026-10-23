"""Directed Shopping List expansion cases TC-22…TC-25 (P1, opt-in)."""

import uuid

import pytest
import requests

from tc22_tc37_helpers import BASE_URL, HEADERS, assert_status, create_list, delete, get, require_p1, unique


def test_tc22_whitespace_shopping_list_name():
    """TC-22 | REQ-LST-03/06 | C: POST returns 201 or 422; T: clean test-only data."""
    require_p1()
    created_id = None
    try:
        response = requests.post(
            f"{BASE_URL}/api/households/shopping/lists",
            headers=HEADERS,
            json={"name": "   "},
            timeout=10,
        )
        assert_status(response, {201, 422}, "TC-22")
        if response.status_code == 201:
            created_id = response.json().get("id")
            assert created_id, "TC-22: successful create must return an id"
    finally:
        if created_id:
            delete(f"/api/households/shopping/lists/{created_id}")


def test_tc23_unicode_shopping_list_name_round_trip():
    """TC-23 | REQ-LST-03 | C: 201/422; T: successful value round-trips through GET."""
    require_p1()
    created_id = None
    name = f"K05-QA-Mua sắm Đà Lạt-{uuid.uuid4().hex[:8]}"
    try:
        response = requests.post(
            f"{BASE_URL}/api/households/shopping/lists",
            headers=HEADERS,
            json={"name": name},
            timeout=10,
        )
        assert_status(response, {201, 422}, "TC-23")
        if response.status_code == 201:
            created_id = response.json().get("id")
            assert created_id, "TC-23: successful create must return an id"
            current = get(f"/api/households/shopping/lists/{created_id}")
            assert current.status_code == 200, "TC-23: created list must be readable"
            assert current.json().get("name") == name
    finally:
        if created_id:
            delete(f"/api/households/shopping/lists/{created_id}")


def test_tc24_update_missing_shopping_list_uuid():
    """TC-24 | REQ-LST-02/04 | C: PUT returns 200 or 422 for a valid missing UUID."""
    require_p1()
    source = None
    missing_id = str(uuid.uuid4())
    target_created = False
    try:
        source = create_list("22-24-source")
        if get(f"/api/households/shopping/lists/{missing_id}").status_code == 200:
            pytest.skip("TC-24 generated UUID unexpectedly identifies an existing list")
        source_current = get(f"/api/households/shopping/lists/{source['id']}")
        assert source_current.status_code == 200
        payload = {
            "id": missing_id,
            "groupId": source_current.json()["groupId"],
            "userId": source_current.json()["userId"],
            "name": unique("22-24-missing"),
        }
        response = requests.put(
            f"{BASE_URL}/api/households/shopping/lists/{missing_id}",
            headers=HEADERS,
            json=payload,
            timeout=10,
        )
        assert_status(response, {200, 422}, "TC-24")
        target_created = response.status_code == 200
        assert get(f"/api/households/shopping/lists/{source['id']}").status_code == 200
    finally:
        if target_created:
            delete(f"/api/households/shopping/lists/{missing_id}")
        if source:
            delete(f"/api/households/shopping/lists/{source['id']}")


def test_tc25_delete_shopping_list_twice():
    """TC-25 | REQ-LST-05 | C: both DELETEs return 200 or 422; T: no test data remains."""
    require_p1()
    item = None
    deleted = False
    try:
        item = create_list("22-25")
        first = requests.delete(
            f"{BASE_URL}/api/households/shopping/lists/{item['id']}", headers=HEADERS, timeout=10
        )
        assert_status(first, {200, 422}, "TC-25 first DELETE")
        deleted = first.status_code == 200
        second = requests.delete(
            f"{BASE_URL}/api/households/shopping/lists/{item['id']}", headers=HEADERS, timeout=10
        )
        assert_status(second, {200, 422}, "TC-25 second DELETE")
        assert get(f"/api/households/shopping/lists/{item['id']}").status_code != 200
    finally:
        if item and not deleted:
            delete(f"/api/households/shopping/lists/{item['id']}")
