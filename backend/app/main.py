import logging

from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Bizzi Platform Backend")
app.include_router(health_router)


@app.on_event("startup")
def on_startup() -> None:
    # Reading settings here (not deferring to first use) is what makes a
    # missing required env var (e.g. DATABASE_URL) fail fast at startup
    # instead of surfacing later as a confusing runtime error.
    settings = get_settings()
    logger.info("Bizzi backend starting up", extra={"env": settings.env})
