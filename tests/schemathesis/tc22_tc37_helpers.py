"""Shared, deliberately small helpers for the directed TC-22…TC-37 tests."""

import os
import uuid
from datetime import date, timedelta

import pytest
import requests


BASE_URL = os.getenv("MEALIE_BASE_URL", "http://localhost:9091")
TOKEN = os.getenv("MEALIE_API_TOKEN")
P1_ENABLED = TOKEN and os.getenv("MEALIE_RUN_P1_EXPANSION") == "1"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}


def unique(label):
    return f"K05-TC-{label}-{uuid.uuid4().hex[:8]}"


def assert_status(response, allowed, test_id):
    assert response.status_code in allowed, (
        f"{test_id}: documented status {sorted(allowed)}, got "
        f"{response.status_code}: {response.text[:500]}"
    )


def get(path):
    return requests.get(f"{BASE_URL}{path}", headers=HEADERS, timeout=10)


def delete(path):
    try:
        requests.delete(f"{BASE_URL}{path}", headers=HEADERS, timeout=10)
    except requests.RequestException:
        pass


def create_list(label):
    response = requests.post(
        f"{BASE_URL}/api/households/shopping/lists",
        headers=HEADERS,
        json={"name": unique(label)},
        timeout=10,
    )
    assert response.status_code == 201, f"Parent list create failed: {response.status_code}"
    item = response.json()
    assert item.get("id"), "Shopping list create response has no id"
    return item


def create_item(list_id, label, **overrides):
    payload = {
        "shoppingListId": list_id,
        "quantity": 1,
        "display": unique(label),
        "checked": False,
    }
    payload.update(overrides)
    response = requests.post(
        f"{BASE_URL}/api/households/shopping/items",
        headers=HEADERS,
        json=payload,
        timeout=10,
    )
    assert response.status_code == 201, f"Shopping item create failed: {response.status_code}"
    created = response.json().get("createdItems", [])
    assert len(created) == 1 and created[0].get("id"), "Expected one created shopping item"
    return created[0]


def create_mealplan(label):
    title = unique(label)
    response = requests.post(
        f"{BASE_URL}/api/households/mealplans",
        headers=HEADERS,
        json={
            "date": (date.today() + timedelta(days=30)).isoformat(),
            "entryType": "breakfast",
            "title": title,
            "text": "Controlled TC-22…TC-37 QA data",
        },
        timeout=10,
    )
    assert response.status_code == 201, f"Meal plan create failed: {response.status_code}"
    item = response.json()
    assert item.get("id") is not None, "Meal plan create response has no id"
    return item


def mealplan_update_payload(current, **overrides):
    payload = {
        "date": current["date"],
        "id": current["id"],
        "groupId": current["groupId"],
        "userId": current["userId"],
        "entryType": current.get("entryType", "breakfast"),
        "title": current.get("title"),
        "text": current.get("text"),
        "recipeId": current.get("recipeId"),
    }
    payload.update(overrides)
    return payload


def create_recipe(label):
    response = requests.post(
        f"{BASE_URL}/api/recipes",
        headers=HEADERS,
        json={"name": unique(label)},
        timeout=10,
    )
    assert response.status_code == 201, f"Recipe create failed: {response.status_code}"
    slug = response.json()
    assert isinstance(slug, str) and slug, "Recipe create response must be a slug string"
    return slug


def require_p1():
    if not TOKEN:
        pytest.skip("MEALIE_API_TOKEN is not set")
    if not P1_ENABLED:
        pytest.skip("Set MEALIE_RUN_P1_EXPANSION=1 to enable controlled P1 writes")
