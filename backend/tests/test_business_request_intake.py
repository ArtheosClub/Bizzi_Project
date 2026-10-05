"""Stage 4 default-deny and required empty-object DTO, no database calls."""

from contextlib import nullcontext
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.api.business_request_intake import router
from app.core.errors import register_error_handlers
from app.core.request_context import RequestIDMiddleware
from app.db.session import get_db
from app.schemas.business_request_intake import BusinessRequestInput


@pytest.mark.parametrize("body", ["{}", "{", "[]", '{"actor_id":"synthetic"}'])
@pytest.mark.parametrize("header", [None, "Bearer synthetic-test-token", "Basic synthetic"])
def test_default_verifier_rejects_before_body_and_database(body, header):
    api = FastAPI()
    register_error_handlers(api)
    api.include_router(router)
    db = Mock()
    db.begin.return_value = nullcontext()
    api.dependency_overrides[get_db] = lambda: db
    with TestClient(RequestIDMiddleware(api)) as client:
        response = client.post(
            "/business-requests", content=body, headers={"Authorization": header} if header else {}
        )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthenticated"
    assert response.headers["X-Request-Id"]
    db.execute.assert_not_called()
    db.scalar.assert_not_called()


@pytest.mark.parametrize("body", ['{"type":"other"}', "[]", "null", '"text"', "{"])
def test_input_requires_empty_object(body):
    with pytest.raises(ValidationError):
        BusinessRequestInput.model_validate_json(body)


def test_empty_input_is_valid():
    assert BusinessRequestInput.model_validate_json("{}").model_dump() == {}
