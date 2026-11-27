"""Offline TC-34 cleanup checks, separate from the 37 business items."""
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tests" / "schemathesis"))
import test_tc34_tc37_recipes as tc34


def response(status, body=None):
    return Mock(status_code=status, text="diagnostic", json=Mock(return_value=body))


def listing(items):
    return response(200, {"items": items, "totalPages": 1})


@pytest.mark.parametrize("status", [200, 404])
def test_deleted_or_404_confirmed_absent(monkeypatch, status):
    item = {"id": "ours", "slug": "old", "name": "unique"}
    get = Mock(side_effect=[listing([item]), response(200, item), listing([])])
    delete = Mock(return_value=response(status))
    monkeypatch.setattr(tc34, "get", get)
    monkeypatch.setattr(tc34.requests, "delete", delete)
    tc34._tc34_cleanup("ours", {"unique"})
    assert delete.call_count == 1


def test_changed_slug_and_other_recipe(monkeypatch):
    item = {"id": "ours", "slug": "changed", "name": "updated"}
    other = {"id": "other", "slug": "old", "name": "unrelated"}
    monkeypatch.setattr(tc34, "get", Mock(side_effect=[listing([other, item]), response(200, item), listing([other])]))
    delete = Mock(return_value=response(200))
    monkeypatch.setattr(tc34.requests, "delete", delete)
    tc34._tc34_cleanup("ours", {"original", "updated"})
    assert delete.call_args.args[0].endswith("/changed")


def test_404_with_resource_remaining_fails(monkeypatch):
    item = {"id": "ours", "slug": "old", "name": "unique"}
    monkeypatch.setattr(tc34, "get", Mock(side_effect=[listing([item]), response(200, item), listing([item])]))
    monkeypatch.setattr(tc34.requests, "delete", Mock(return_value=response(404)))
    with pytest.raises(AssertionError, match="still exists"):
        tc34._tc34_cleanup("ours", {"unique"})


def test_cleanup_failure_preserves_put_failure(monkeypatch):
    monkeypatch.setattr(tc34, "require_p1", lambda: None)
    monkeypatch.setattr(tc34.requests, "post", Mock(return_value=response(201, "old")))
    monkeypatch.setattr(tc34.requests, "put", Mock(return_value=response(500)))
    monkeypatch.setattr(tc34, "get", lambda path: response(200, {"name": tc34.requests.post.call_args.kwargs["json"]["name"], "id": "ours"}))
    monkeypatch.setattr(tc34, "_tc34_cleanup", Mock(side_effect=AssertionError("cleanup failed")))
    with pytest.raises(AssertionError, match="got 500") as error:
        tc34.test_tc34_put_recipe_name_update()
    assert "cleanup failed" in str(error.value.__cause__)


def test_absent_without_deleting(monkeypatch):
    monkeypatch.setattr(tc34, "get", Mock(return_value=listing([])))
    delete = Mock()
    monkeypatch.setattr(tc34.requests, "delete", delete)
    tc34._tc34_cleanup("ours", {"unique"})
    delete.assert_not_called()
