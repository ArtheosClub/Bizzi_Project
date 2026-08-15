"""WP22 error taxonomy and FastAPI exception handlers (ADR-0012 §2-§6).

A standardized error-only envelope, FastAPI-native 422 for validation
failures, the four-code generic vocabulary, the no-leak invariant for
unexpected exceptions, and an extension point future WPs use to add
error codes without changing this module or the envelope contract.
"""

import logging
from collections.abc import Sequence
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)

_LOCATION_MARKERS = {"body", "query", "path", "header"}

_HTTP_EXCEPTION_CODES = {
    status.HTTP_404_NOT_FOUND: "not_found",
    status.HTTP_405_METHOD_NOT_ALLOWED: "method_not_allowed",
}


class AppError(Exception):
    """Base for application-raised errors this module's handler maps
    generically. Future WPs extend the error-code vocabulary by
    subclassing this — adding a code requires no change to this module
    or the envelope contract (ADR-0012 §4).

    No `details` parameter: ADR-0012 §2 selects structured `details` for
    `validation_error` only. A future WP that genuinely needs structured
    details on a domain error should decide that against a real case,
    not inherit an unrequested capability from this base class.
    """

    code: str = "internal_error"
    http_status: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def _error_body(
    code: str, message: str, details: Sequence[dict[str, Any]] | None = None
) -> dict[str, Any]:
    error: dict[str, Any] = {"code": code, "message": message}
    if details is not None:
        error["details"] = details
    return {"error": error}


def _field_path(loc: Sequence[str | int]) -> str:
    parts = [str(part) for part in loc if part not in _LOCATION_MARKERS]
    return ".".join(parts) if parts else str(loc[-1])


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.http_status,
        content=_error_body(exc.code, exc.message),
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    details = [
        {
            "field": _field_path(error["loc"]),
            "issue": str(error["type"]),
            "message": error["msg"],
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_error_body("validation_error", "Request validation failed", details),
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    code = _HTTP_EXCEPTION_CODES.get(exc.status_code)
    if code is not None:
        message = (
            exc.detail if isinstance(exc.detail, str) else "Request could not be processed"
        )
        # Starlette's HTTPException carries response headers of its own
        # (e.g. the router's 405 sets Allow) — preserving them is
        # existing HTTP semantics, not a new envelope field or contract
        # decision.
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body(code, message),
            headers=exc.headers,
        )

    # Defensive fallback only — not an ADR-0012 policy. Nothing in
    # backend/app/ raises HTTPException with any status besides the
    # framework-generated 404/405 this module already maps (confirmed by
    # repository search). ADR-0012 §4 fixes exactly four generic codes
    # and doesn't decide what an unmapped status should become; the
    # sanctioned way for a future WP to add a real status is an AppError
    # subclass (app_error_handler above), which never reaches this
    # branch. If a genuine caller ever hits this, that's the trigger to
    # decide the policy properly, not to treat this fallback as settled.
    logger.warning(
        "Unmapped HTTPException status %s reached the fallback handler",
        exc.status_code,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body("internal_error", "Request could not be processed."),
        headers=exc.headers,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # No exception text, traceback, or internal attribute reaches the
    # client — only the internal log line carries that detail
    # (13_BACKEND_CODING_STANDARDS.md §15, §21; ADR-0012 §5). request_id
    # reaches this log line via RequestIDLogFilter, the single owner of
    # log-side propagation — not a second, independently generated
    # identifier.
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_error_body("internal_error", "Unexpected server error."),
    )


def register_error_handlers(app: FastAPI) -> None:
    # Starlette's add_exception_handler stub declares handlers against the
    # base Exception type; ours are correctly typed against the specific
    # subclass Starlette actually dispatches to at runtime (it looks up
    # handlers by the exact registered class). The mismatch is a stub
    # narrowness limitation, not a real type error.
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)
