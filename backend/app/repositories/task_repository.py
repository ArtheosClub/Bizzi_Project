"""WP15 candidate persistence; only add is admitted in record-5 Stage 3.

The caller owns the session and transaction.

Reads always constrain workspace_id. No update/delete API: the service mutates
a loaded instance and AuditService's flush persists it in the same transaction.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task

DEFAULT_LIST_LIMIT = 100


def add(session: Session, obj: Task) -> None:
    """Flush an already-formed instance without returning a mutable record."""
    session.add(obj)
    session.flush()


def get_by_id(
    session: Session,
    workspace_id: uuid.UUID,
    task_id: uuid.UUID,
    *,
    for_update: bool = False,
) -> Task | None:
    """Return None for missing and cross-workspace identities alike.

    A transition requests a row lock held until the caller ends the transaction.
    Refreshing the identity map after acquiring it avoids validating stale phase
    state when this session loaded the object before another writer committed.
    """
    statement = select(Task).where(
        Task.workspace_id == workspace_id,
        Task.id == task_id,
    )
    if for_update:
        statement = statement.with_for_update().execution_options(populate_existing=True)
    return session.scalar(statement)


def list_by_workspace(
    session: Session,
    workspace_id: uuid.UUID,
    *,
    limit: int = DEFAULT_LIST_LIMIT,
) -> list[Task]:
    """Bounded, deterministic read ordered by created_at DESC, id DESC."""
    if type(limit) is not int or limit <= 0:
        raise ValueError(f"limit must be a positive int, got {limit!r}")
    statement = (
        select(Task)
        .where(Task.workspace_id == workspace_id)
        .order_by(Task.created_at.desc(), Task.id.desc())
        .limit(limit)
    )
    return list(session.scalars(statement))
