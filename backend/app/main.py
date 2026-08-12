import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import get_settings
from app.core.errors import register_error_handlers
from app.core.logging import configure_logging
from app.core.request_context import RequestIDMiddleware

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Reading settings here (not deferring to first use) is what makes a
    # missing required env var (e.g. DATABASE_URL) fail fast at startup
    # instead of surfacing later as a confusing runtime error.
    settings = get_settings()
    logger.info("Bizzi backend starting up", extra={"env": settings.env})
    yield


fastapi_app = FastAPI(title="Bizzi Platform Backend", lifespan=lifespan)
register_error_handlers(fastapi_app)
fastapi_app.include_router(health_router)

# `app` is the served ASGI callable — wrapped outside FastAPI's own
# ServerErrorMiddleware, not installed via fastapi_app.add_middleware().
# Starlette hoists the bare-Exception handler (ADR-0012 §5's no-leak
# catch-all) into ServerErrorMiddleware, which sits outside anything
# add_middleware() installs and sends its response through the original,
# unwrapped `send` — confirmed empirically: an add_middleware()-installed
# RequestIDMiddleware never even runs on that path. The §5 handler is
# therefore precisely the path that would otherwise silently violate
# ADR-0012 §1. Wrapping fastapi_app directly makes RequestIDMiddleware
# the single, outermost owner of the X-Request-Id invariant across every
# response — success, 404, 405, 422, and unexpected 500 alike.
#
# All FastAPI-specific access (`.router`, `.state`,
# `.dependency_overrides`, handler/router registration) belongs on
# `fastapi_app`, not on `app` — `app` is a plain ASGI callable from here
# on, which is all `uvicorn app.main:app` and the Docker entrypoint
# require.
app = RequestIDMiddleware(fastapi_app)
