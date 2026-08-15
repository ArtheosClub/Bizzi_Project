"""Structured logging setup.

MVP simplicity per Bizzi backend design principle B15: stdlib `logging`
with a JSON formatter, no extra dependency (e.g. structlog) until a real
need for one is demonstrated. Every log record carries a stable set of
fields so log lines are machine-parseable from day one.
"""

import json
import logging
import sys
from datetime import UTC, datetime

from app.core.request_context import get_request_id

_RESERVED_RECORD_ATTRS = frozenset(logging.LogRecord("", 0, "", 0, "", (), None).__dict__)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=UTC
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Surface fields passed via logger.info(..., extra={...}) — without
        # this, extra= is silently dropped and "structured logging" would
        # only be structured for the fixed fields above.
        for key, value in record.__dict__.items():
            if key not in _RESERVED_RECORD_ATTRS:
                payload[key] = value
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


class RequestIDLogFilter(logging.Filter):
    """Attaches the current request's ID (ADR-0012 §1/§8), if any, to
    every log record. Reads the same ContextVar RequestIDMiddleware
    populates — no independent identifier is generated here.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        request_id = get_request_id()
        if request_id is not None:
            record.request_id = request_id
        return True


def configure_logging(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    handler.addFilter(RequestIDLogFilter())

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)
