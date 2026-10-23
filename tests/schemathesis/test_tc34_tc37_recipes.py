"""Directed Recipe expansion cases TC-34…TC-37 (P1, opt-in)."""

import uuid

import requests

from tc22_tc37_helpers import BASE_URL, HEADERS, assert_status, create_recipe, delete, get, require_p1


def test_tc34_put_recipe_name_update():
    """TC-34 | REQ-REC-03/04 | C: PUT 200/422; T: a successful name update is readable."""
    require_p1()
    slug = None
    name = f"K05-TC-34-updated-{uuid.uuid4().hex[:8]}"
    try:
        slug = create_recipe("22-34")
        response = requests.put(
            f"{BASE_URL}/api/recipes/{slug}",
            headers=HEADERS,
            json={"name": name},
            timeout=10,
        )
        assert_status(response, {200, 422}, "TC-34")
        if response.status_code == 200:
            current = get(f"/api/recipes/{slug}")
            assert current.status_code == 200
            assert current.json().get("name") == name
    finally:
        if slug:
            delete(f"/api/recipes/{slug}")


def test_tc35_patch_recipe_name_update():
    """TC-35 | REQ-REC-03/04 | C: PATCH 200/422; T: a successful patch is readable."""
    require_p1()
    slug = None
    name = f"K05-TC-35-patched-{uuid.uuid4().hex[:8]}"
    try:
        slug = create_recipe("22-35")
        response = requests.patch(
            f"{BASE_URL}/api/recipes/{slug}",
            headers=HEADERS,
            json={"name": name},
            timeout=10,
        )
        assert_status(response, {200, 422}, "TC-35")
        if response.status_code == 200:
            updated = response.json()
            assert isinstance(updated, dict) and updated.get("slug"), (
                "TC-35: successful PATCH must identify the updated recipe for verification"
            )
            # Recipe names generate slugs; use the response identifier for GET and cleanup.
            slug = updated["slug"]
            current = get(f"/api/recipes/{slug}")
            assert current.status_code == 200
            assert current.json().get("name") == name
    finally:
        if slug:
            delete(f"/api/recipes/{slug}")


def test_tc36_whitespace_recipe_name():
    """TC-36 | REQ-REC-05 | C: POST 201/422 and never an undocumented 5xx."""
    require_p1()
    slug = None
    try:
        response = requests.post(
            f"{BASE_URL}/api/recipes",
            headers=HEADERS,
            json={"name": "   "},
            timeout=10,
        )
        assert_status(response, {201, 422}, "TC-36")
        if response.status_code == 201:
            slug = response.json()
            assert isinstance(slug, str) and slug, "TC-36: successful create must return a slug"
    finally:
        if slug:
            delete(f"/api/recipes/{slug}")


def test_tc37_recipe_name_length_256():
    """TC-37 | REQ-REC-03/05 | C: POST 201/422; T: created value is readable."""
    require_p1()
    name = f"K05-QA-{uuid.uuid4().hex[:8]}-" + "A" * 240
    assert len(name) == 256
    slug = None
    try:
        response = requests.post(
            f"{BASE_URL}/api/recipes",
            headers=HEADERS,
            json={"name": name},
            timeout=10,
        )
        assert_status(response, {201, 422}, "TC-37")
        if response.status_code == 201:
            slug = response.json()
            assert isinstance(slug, str) and slug, "TC-37: successful create must return a slug"
            current = get(f"/api/recipes/{slug}")
            assert current.status_code == 200
            assert current.json().get("name") == name
    finally:
        if slug:
            delete(f"/api/recipes/{slug}")
