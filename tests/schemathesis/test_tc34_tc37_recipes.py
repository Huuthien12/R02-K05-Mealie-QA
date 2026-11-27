"""Directed Recipe expansion cases TC-34…TC-37 (P1, opt-in)."""

import sys
import uuid

import requests

from tc22_tc37_helpers import BASE_URL, HEADERS, assert_status, create_recipe, delete, get, require_p1


def _tc34_find_recipe(recipe_id, names):
    """Find the test resource by ID (or its exact unique name before ID is known)."""
    page = 1
    matches = []
    while True:
        response = get(f"/api/recipes?page={page}&perPage=100")
        assert response.status_code == 200, f"TC-34 cleanup: list returned {response.status_code}: {response.text[:500]}"
        body = response.json()
        assert isinstance(body, dict) and isinstance(body.get("items"), list), "TC-34 cleanup: invalid list response"
        total_pages = body.get("totalPages", body.get("total_pages"))
        assert isinstance(total_pages, int) and total_pages >= 0, "TC-34 cleanup: missing pagination"
        for item in body["items"]:
            assert isinstance(item, dict) and item.get("id") and item.get("slug"), "TC-34 cleanup: invalid recipe identity"
            if (recipe_id and item["id"] == recipe_id) or (not recipe_id and item.get("name") in names):
                matches.append(item)
        if page >= total_pages:
            break
        page += 1
    assert len(matches) <= 1, "TC-34 cleanup: ambiguous recipe identity"
    return matches[0] if matches else None


def _tc34_cleanup(recipe_id, names):
    item = _tc34_find_recipe(recipe_id, names)
    if item is None:
        return
    # Recheck identity immediately before deletion; never delete by a guessed slug.
    current = get(f"/api/recipes/{item['slug']}")
    assert current.status_code == 200, f"TC-34 cleanup: identity GET returned {current.status_code}"
    assert current.json().get("id") == item["id"], "TC-34 cleanup: recipe identity changed"
    response = requests.delete(f"{BASE_URL}/api/recipes/{item['slug']}", headers=HEADERS, timeout=10)
    assert response.status_code in {200, 404}, f"TC-34 cleanup: DELETE returned {response.status_code}: {response.text[:500]}"
    remaining = _tc34_find_recipe(item["id"], names)
    assert remaining is None, f"TC-34 cleanup: recipe {item['id']} still exists after DELETE {response.status_code}"


def test_tc34_put_recipe_name_update():
    """TC-34 | REQ-REC-03/04 | C: PUT 200/422; T: a successful name update is readable."""
    require_p1()
    marker = uuid.uuid4().hex
    original_name = f"K05-TC-34-original-{marker}"
    name = f"K05-TC-34-updated-{marker}"
    slug = None
    recipe_id = None
    try:
        created = requests.post(f"{BASE_URL}/api/recipes", headers=HEADERS, json={"name": original_name}, timeout=10)
        assert created.status_code == 201, f"TC-34: create returned {created.status_code}"
        slug = created.json()
        assert isinstance(slug, str) and slug, "TC-34: create must return a slug"
        initial = get(f"/api/recipes/{slug}")
        assert initial.status_code == 200, f"TC-34: initial GET returned {initial.status_code}"
        initial = initial.json()
        assert initial.get("name") == original_name and initial.get("id"), "TC-34: initial identity mismatch"
        recipe_id = initial["id"]
        response = requests.put(
            f"{BASE_URL}/api/recipes/{slug}", headers=HEADERS, json={"name": name}, timeout=10,
        )
        assert_status(response, {200, 422}, "TC-34")
        if response.status_code == 200:
            updated = response.json()
            assert isinstance(updated, dict) and updated.get("slug"), "TC-34: successful PUT must identify the updated recipe"
            current = get(f"/api/recipes/{updated['slug']}")
            assert current.status_code == 200
            current = current.json()
            assert current.get("id") == recipe_id and current.get("slug") == updated["slug"], "TC-34: GET returned a different recipe"
            assert current.get("name") == name, "TC-34: successful PUT name did not persist"
    finally:
        if slug:
            primary = sys.exc_info()[1]
            try:
                _tc34_cleanup(recipe_id, {original_name, name})
            except Exception as cleanup_error:
                if primary is not None:
                    raise primary.with_traceback(primary.__traceback__) from cleanup_error
                raise


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
            current = current.json()
            assert current.get("slug") == slug, "TC-37: GET returned a different recipe"
            assert current.get("name") == name, "TC-37: 256-character name did not round-trip exactly"
    finally:
        if slug:
            delete(f"/api/recipes/{slug}")
