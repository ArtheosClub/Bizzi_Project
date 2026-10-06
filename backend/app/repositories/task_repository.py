"""WP15 candidate persistence; only add is admitted in record-5 Stage 3.

The caller owns the session and transaction.

Amendment 4 removes excluded read/list operations. No update/delete API.
"""

from sqlalchemy.orm import Session

from app.models.task import Task


def add(session: Session, obj: Task) -> None:
    """Flush an already-formed instance without returning a mutable record."""
    session.add(obj)
    session.flush()
