import os
from pathlib import Path

import pytest
import schemathesis
from hypothesis import settings

SCHEMA_PATH = (
    Path(__file__).parents[2]
    / "schema"
    / "snapshots"
    / "mealie-v3.28.0-openapi.json"
)

BASE_URL = os.getenv("MEALIE_BASE_URL", "http://localhost:9091")
TOKEN = os.getenv("MEALIE_API_TOKEN")

P0_DETAIL_PATHS = [
    "/api/recipes/{slug}",
    "/api/households/shopping/lists/{item_id}",
    "/api/households/shopping/items/{item_id}",
    "/api/households/mealplans/{item_id}",
]

schema = schemathesis.openapi.from_path(SCHEMA_PATH)

schema = schema.include(
    path=P0_DETAIL_PATHS,
    method="GET",
)


@pytest.mark.skipif(
    not TOKEN,
    reason="MEALIE_API_TOKEN is not set",
)
@settings(max_examples=3, deadline=None)
@schema.parametrize()
def test_p0_detail_schema_fuzz(case):
    response = case.call(
        base_url=BASE_URL,
        headers={
            "Authorization": f"Bearer {TOKEN}",
        },
    )

    case.validate_response(
        response,
        checks=(
            schemathesis.checks.not_a_server_error,
            schemathesis.checks.status_code_conformance,
            schemathesis.checks.response_schema_conformance,
        ),
    )
