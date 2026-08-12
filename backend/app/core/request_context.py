"""Per-HTTP-request identifier: generation and propagation (ADR-0012 §1, §8).

One opaque, request-scoped identifier per HTTP request, generated at the
ASGI boundary, exposed via a response header, and made available to
structured logging through the same ContextVar. Tier-6 API/runtime
observability only — per Amendment A-07, this does not define, implement,
alias, or constrain Domain Event correlation, causation, provenance,
distributed tracing, or cross-request workflow identity.

Must be composed by wrapping the FastAPI instance directly
(``app = RequestIDMiddleware(fastapi_app)``), not via
``fastapi_app.add_middleware(...)``. Starlette's ``build_middleware_stack``
special-cases a handler registered for the bare ``Exception`` class (the
ADR-0012 §5 no-leak catch-all): it is pulled out of ExceptionMiddleware and
given to ServerErrorMiddleware, which sits *outside* anything installed
via ``add_middleware`` and sends its response through the original,
unwrapped ``send`` — confirmed empirically (a middleware installed via
``add_middleware`` never even runs for that path). Wrapping the app
directly makes this the outermost layer, so it is the single mechanism
responsible for the header on every response path, including that one —
the catch-all handler itself must not duplicate this responsibility.
"""

import uuid
from contextvars import ContextVar

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

REQUEST_ID_HEADER = "X-Request-Id"

_request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)


def get_request_id() -> str | None:
    """The current request's ID, or None outside a request lifecycle."""
    return _request_id_ctx.get()


class RequestIDMiddleware:
    """Pure ASGI middleware, composed outside the FastAPI instance.

    Avoids BaseHTTPMiddleware's child-task indirection so the ContextVar
    set here is guaranteed visible to the route handler and to any
    exception handler that produces the final response.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = uuid.uuid4().hex
        token = _request_id_ctx.set(request_id)

        async def send_with_request_id(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers[REQUEST_ID_HEADER] = request_id
            await send(message)

        try:
            await self.app(scope, receive, send_with_request_id)
        finally:
            _request_id_ctx.reset(token)
