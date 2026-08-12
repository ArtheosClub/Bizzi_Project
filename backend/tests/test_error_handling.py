"""WP22 error-handling tests (ADR-0012 §2-§6).

Exercises the shared exception-handler mechanism against the real
`app.main.app` where a real trigger already exists (/health's
framework-generated 404/405), and against a throwaway FastAPI app built
with the same production composition (fastapi_app + register_error_handlers
+ RequestIDMiddleware wrap) for cases with no real WP22 route yet
(validation, the AppError extension point, an unmapped HTTPException, and
an unexpected exception).
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.errors import AppError, register_error_handlers
from app.core.request_context import RequestIDMiddleware
from app.main import app as real_app


def _test_app() -> tuple[RequestIDMiddleware, FastAPI]:
    fastapi_app = FastAPI()
    register_error_handlers(fastapi_app)
    return RequestIDMiddleware(fastapi_app), fastapi_app


def test_framework_404_shape() -> None:
    with TestClient(real_app) as client:
        response = client.get("/this-route-does-not-exist")

    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "not_found"
    assert "details" not in body["error"]


def test_framework_405_shape() -> None:
    with TestClient(real_app) as client:
        response = client.post("/health")

    assert response.status_code == 405
    body = response.json()
    assert body["error"]["code"] == "method_not_allowed"
    assert "details" not in body["error"]


def test_validation_error_shape() -> None:
    wrapped, fastapi_app = _test_app()

    @fastapi_app.get("/echo")
    def echo(required: str) -> dict[str, str]:
        return {"required": required}

    with TestClient(wrapped) as client:
        response = client.get("/echo")

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "validation_error"
    assert body["error"]["details"]
    detail = body["error"]["details"][0]
    assert set(detail.keys()) == {"field", "issue", "message"}
    assert detail["field"] == "required"


def test_unexpected_exception_shape_and_no_leak() -> None:
    wrapped, fastapi_app = _test_app()

    @fastapi_app.get("/boom")
    def boom() -> dict[str, str]:
        raise RuntimeError("a very specific internal secret detail")

    with TestClient(wrapped, raise_server_exceptions=False) as client:
        response = client.get("/boom")

    assert response.status_code == 500
    body = response.json()
    assert body["error"]["code"] == "internal_error"
    assert "details" not in body["error"]
    assert "a very specific internal secret detail" not in response.text
    assert "RuntimeError" not in response.text
    assert "Traceback" not in response.text


def test_app_error_extension_point() -> None:
    """Proves ADR-0012 §4's extensibility principle: a future WP adds a
    code by subclassing AppError, with no change to this module's
    envelope or handler registration. Not itself a WP22-owned generic
    code — a demonstration of the mechanism future WPs use.
    """
    wrapped, fastapi_app = _test_app()

    class TeapotError(AppError):
        code = "im_a_teapot"
        http_status = 418

    @fastapi_app.get("/teapot")
    def teapot() -> dict[str, str]:
        raise TeapotError("no coffee here")

    with TestClient(wrapped) as client:
        response = client.get("/teapot")

    assert response.status_code == 418
    body = response.json()
    assert body["error"]["code"] == "im_a_teapot"
    assert "details" not in body["error"]


def test_unmapped_http_exception_is_defensive_fallback_only() -> None:
    """Guards today's implementation fallback, not a settled contract.

    Zero current repository consumers raise HTTPException with any
    status besides the framework-generated 404/405 this module already
    maps (confirmed by repository search during review). The handler
    still has to do *something* for this branch, so this test
    deliberately regression-guards today's minimal fallback — status
    preserved (409 stays 409), body code `internal_error` — against
    accidental breakage. That behavior remains non-normative: it is not
    an ADR-0012/WP22-approved status/code mapping, and may be
    reconsidered once a real consumer exists. A future WP that needs a
    genuine additional application status/code should use the AppError
    extension point (demonstrated above), governed by its own WP
    decision, rather than relying on this fallback as its contract.
    """
    wrapped, fastapi_app = _test_app()

    @fastapi_app.get("/conflict")
    def conflict() -> dict[str, str]:
        raise StarletteHTTPException(
            status_code=409, detail="raw HTTPException, not AppError"
        )

    with TestClient(wrapped) as client:
        response = client.get("/conflict")

    assert response.status_code == 409
    body = response.json()
    assert body["error"]["code"] == "internal_error"
    assert "details" not in body["error"]
    assert "raw HTTPException" not in response.text


def test_health_gate_b_contract_unchanged() -> None:
    with TestClient(real_app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body == {"status": "ok"}
    assert "error" not in body
