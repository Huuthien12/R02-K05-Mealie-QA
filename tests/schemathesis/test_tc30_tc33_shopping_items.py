"""Directed Shopping Item expansion cases TC-30…TC-33 (P1, opt-in)."""

import uuid

import pytest
import requests

from tc22_tc37_helpers import BASE_URL, HEADERS, assert_status, create_item, create_list, delete, get, require_p1, unique


def _item_update_payload(current, **overrides):
    payload = {
        "shoppingListId": current["shoppingListId"],
        "quantity": current.get("quantity", 1),
        "display": current.get("display"),
        "note": current.get("note"),
        "checked": current.get("checked", False),
        "position": current.get("position", 0),
    }
    payload.update(overrides)
    return payload


def test_tc30_negative_shopping_item_quantity():
    """TC-30 | REQ-ITM-04/06 | C: PUT 200/422; T: a rejected update preserves quantity."""
    require_p1()
    parent = None
    item = None
    try:
        parent = create_list("22-30-parent")
        item = create_item(parent["id"], "22-30-item")
        current = get(f"/api/households/shopping/items/{item['id']}")
        assert current.status_code == 200
        response = requests.put(
            f"{BASE_URL}/api/households/shopping/items/{item['id']}",
            headers=HEADERS,
            json=_item_update_payload(current.json(), quantity=-1),
            timeout=10,
        )
        assert_status(response, {200, 422}, "TC-30")
        if response.status_code == 422:
            assert get(f"/api/households/shopping/items/{item['id']}").json().get("quantity") == current.json().get("quantity")
    finally:
        if item:
            delete(f"/api/households/shopping/items/{item['id']}")
        if parent:
            delete(f"/api/households/shopping/lists/{parent['id']}")


def test_tc31_item_with_valid_missing_parent_uuid():
    """TC-31 | REQ-ITM-03/06 | C: POST returns 201 or 422 for a valid missing parent UUID."""
    require_p1()
    parent_id = str(uuid.uuid4())
    created_ids = []
    try:
        if get(f"/api/households/shopping/lists/{parent_id}").status_code == 200:
            pytest.skip("TC-31 generated UUID unexpectedly identifies an existing list")
        response = requests.post(
            f"{BASE_URL}/api/households/shopping/items",
            headers=HEADERS,
            json={"shoppingListId": parent_id, "display": unique("22-31-missing-parent")},
            timeout=10,
        )
        assert_status(response, {201, 422}, "TC-31")
        if response.status_code == 201:
            created_ids = [item["id"] for item in response.json().get("createdItems", []) if item.get("id")]
            assert created_ids, "TC-31: successful create must report an item id"
    finally:
        for item_id in created_ids:
            delete(f"/api/households/shopping/items/{item_id}")


def test_tc32_shopping_item_checked_true_to_false():
    """TC-32 | REQ-ITM-04 | C: each PUT returns 200/422; T: final success is false on GET."""
    require_p1()
    parent = None
    item = None
    try:
        parent = create_list("22-32-parent")
        item = create_item(parent["id"], "22-32-item")
        current = get(f"/api/households/shopping/items/{item['id']}")
        assert current.status_code == 200
        first = requests.put(
            f"{BASE_URL}/api/households/shopping/items/{item['id']}",
            headers=HEADERS,
            json=_item_update_payload(current.json(), checked=True),
            timeout=10,
        )
        assert_status(first, {200, 422}, "TC-32 first PUT")
        if first.status_code == 422:
            return
        after_first = get(f"/api/households/shopping/items/{item['id']}")
        assert after_first.status_code == 200
        second = requests.put(
            f"{BASE_URL}/api/households/shopping/items/{item['id']}",
            headers=HEADERS,
            json=_item_update_payload(after_first.json(), checked=False),
            timeout=10,
        )
        assert_status(second, {200, 422}, "TC-32 second PUT")
        if second.status_code == 200:
            assert get(f"/api/households/shopping/items/{item['id']}").json().get("checked") is False
    finally:
        if item:
            delete(f"/api/households/shopping/items/{item['id']}")
        if parent:
            delete(f"/api/households/shopping/lists/{parent['id']}")


def test_tc33_move_shopping_item_between_qa_lists():
    """TC-33 | REQ-ITM-03/04/05 | C: PUT 200/422; T: state agrees with the result."""
    require_p1()
    source = None
    target = None
    item = None
    try:
        source = create_list("22-33-source")
        target = create_list("22-33-target")
        item = create_item(source["id"], "22-33-item")
        current = get(f"/api/households/shopping/items/{item['id']}")
        assert current.status_code == 200
        response = requests.put(
            f"{BASE_URL}/api/households/shopping/items/{item['id']}",
            headers=HEADERS,
            json=_item_update_payload(current.json(), shoppingListId=target["id"]),
            timeout=10,
        )
        assert_status(response, {200, 422}, "TC-33")
        after = get(f"/api/households/shopping/items/{item['id']}")
        assert after.status_code == 200
        expected_parent = target["id"] if response.status_code == 200 else source["id"]
        assert after.json().get("shoppingListId") == expected_parent
    finally:
        if item:
            delete(f"/api/households/shopping/items/{item['id']}")
        if source:
            delete(f"/api/households/shopping/lists/{source['id']}")
        if target:
            delete(f"/api/households/shopping/lists/{target['id']}")
