from pathlib import Path

import schemathesis


P0_PATHS = [
    "/api/recipes",
    "/api/recipes/{slug}",
    "/api/households/shopping/lists",
    "/api/households/shopping/lists/{item_id}",
    "/api/households/shopping/items",
    "/api/households/shopping/items/{item_id}",
    "/api/households/mealplans",
    "/api/households/mealplans/{item_id}",
    "/api/households/mealplans/today",
]


def test_snapshot_selects_only_p0_read_operations():
    schema = schemathesis.openapi.from_path(
        Path(__file__).parents[2] / "schema/snapshots/mealie-v3.28.0-openapi.json"
    )
    selected = schema.include(path=P0_PATHS, method="GET")

    assert {
        f"{result.ok().method.upper()} {result.ok().path}"
        for result in selected.get_all_operations()
    } == {f"GET {path}" for path in P0_PATHS}
