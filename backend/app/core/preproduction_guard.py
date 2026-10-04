"""Record-5 exact local destination gate; no payload or credential output."""

from sqlalchemy.engine import make_url


class ScopeViolationError(RuntimeError):
    pass


def require_test_destination(database_url: str) -> None:
    try:
        url = make_url(database_url)
        valid = (
            url.drivername == "postgresql+psycopg"
            and url.host == "localhost"
            and url.port == 5433
            and url.database == "bizzi_test"
            and not url.query
        )
    except Exception:
        raise ScopeViolationError("Database destination is outside record-5 scope") from None
    if not valid:
        raise ScopeViolationError("Database destination is outside record-5 scope")
