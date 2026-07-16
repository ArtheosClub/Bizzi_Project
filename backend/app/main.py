import logging

from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Bizzi Platform Backend")
app.include_router(health_router)


@app.on_event("startup")
def on_startup() -> None:
    logger.info("Bizzi backend starting up")
