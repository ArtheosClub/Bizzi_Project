"""ADR-0012 §1/§8 — request-ID response propagation and structured logging."""

import logging

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.errors import register_error_handlers
from app.core.request_context import REQUEST_ID_HEADER, RequestIDMiddleware
from app.main import app as real_app


def _test_app() -> tuple[RequestIDMiddleware, FastAPI]:
    """Same composition as app.main: fastapi_app wrapped by
    RequestIDMiddleware outside ServerErrorMiddleware, not via
    add_middleware() — matching the real app exactly, since that
    distinction is the whole point of what's under test.
    """
    fastapi_app = FastAPI()
    register_error_handlers(fastapi_app)
    return RequestIDMiddleware(fastapi_app), fastapi_app


def test_request_id_present_on_success() -> None:
    with TestClient(real_app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert REQUEST_ID_HEADER in response.headers
    assert response.headers[REQUEST_ID_HEADER]


def test_request_id_present_on_framework_404() -> None:
    with TestClient(real_app) as client:
        response = client.get("/this-route-does-not-exist")

    assert response.status_code == 404
    assert REQUEST_ID_HEADER in response.headers


def test_request_id_present_on_framework_405() -> None:
    with TestClient(real_app) as client:
        response = client.post("/health")

    assert response.status_code == 405
    assert REQUEST_ID_HEADER in response.headers


def test_request_id_present_on_validation_422() -> None:
    wrapped, fastapi_app = _test_app()

    @fastapi_app.get("/echo")
    def echo(required: str) -> dict[str, str]:
        return {"required": required}

    with TestClient(wrapped) as client:
        response = client.get("/echo")

    assert response.status_code == 422
    assert REQUEST_ID_HEADER in response.headers


def test_request_id_present_on_unexpected_500() -> None:
    wrapped, fastapi_app = _test_app()

    @fastapi_app.get("/boom")
    def boom() -> dict[str, str]:
        raise RuntimeError("boom")

    # raise_server_exceptions=False is mandatory here: TestClient
    # re-raises unhandled exceptions to the test process by default, so
    # without it no real 500 response would exist to inspect, and this
    # test would prove nothing about the ServerErrorMiddleware path that
    # originally bypassed an add_middleware()-installed RequestIDMiddleware.
    with TestClient(wrapped, raise_server_exceptions=False) as client:
        response = client.get("/boom")

    assert response.status_code == 500
    assert REQUEST_ID_HEADER in response.headers


def test_request_id_differs_per_request() -> None:
    with TestClient(real_app) as client:
        first = client.get("/health")
        second = client.get("/health")

    assert first.headers[REQUEST_ID_HEADER] != second.headers[REQUEST_ID_HEADER]


def test_no_duplicate_request_id_header() -> None:
    with TestClient(real_app) as client:
        response = client.get("/health")

    assert len(response.headers.get_list(REQUEST_ID_HEADER)) == 1


def test_request_id_matches_logged_value(caplog: pytest.LogCaptureFixture) -> None:
    """ADR-0012 §8: the same logical request-ID value must appear in both
    the response header and structured logs for that request — not two
    independently-created identifiers. Equality, not mere presence.
    """
    wrapped, fastapi_app = _test_app()
    logger = logging.getLogger("app.test_request_id_matches_logged_value")

    @fastapi_app.get("/logged")
    def logged() -> dict[str, bool]:
        logger.info("handling /logged")
        return {"ok": True}

    with caplog.at_level(logging.INFO):
        with TestClient(wrapped) as client:
            response = client.get("/logged")

    assert response.status_code == 200
    response_request_id = response.headers[REQUEST_ID_HEADER]

    matching_records = [r for r in caplog.records if r.getMessage() == "handling /logged"]
    assert matching_records, "expected log record was not captured"
    # request_id is set dynamically by RequestIDLogFilter at runtime;
    # logging.LogRecord's stub has no such field, so this is expected.
    assert matching_records[0].request_id == response_request_id  # type: ignore[attr-defined]
