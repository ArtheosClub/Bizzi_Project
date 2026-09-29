"""WP13/A-12 persistence only; the caller owns the session and transaction.

Reads always constrain workspace_id. No update/delete API: the service mutates
a loaded instance and AuditService's flush persists it in the same transaction.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enterprise_object import EnterpriseObject

DEFAULT_LIST_LIMIT = 100


def add(session: Session, obj: EnterpriseObject) -> None:
    """Flush an already-formed instance without returning a mutable record."""
    session.add(obj)
    session.flush()


def get_by_id(
    session: Session,
    workspace_id: uuid.UUID,
    object_id: uuid.UUID,
    *,
    for_update: bool = False,
) -> EnterpriseObject | None:
    """Return None for missing and cross-workspace identities alike.

    A transition requests a row lock held until the caller ends the transaction.
    Refreshing the identity map after acquiring it avoids validating stale phase
    state when this session loaded the object before another writer committed.
    """
    statement = select(EnterpriseObject).where(
        EnterpriseObject.workspace_id == workspace_id,
        EnterpriseObject.id == object_id,
    )
    if for_update:
        statement = statement.with_for_update().execution_options(populate_existing=True)
    return session.scalar(statement)


def list_by_workspace(
    session: Session,
    workspace_id: uuid.UUID,
    *,
    limit: int = DEFAULT_LIST_LIMIT,
) -> list[EnterpriseObject]:
    """Bounded, deterministic read ordered by created_at DESC, id DESC."""
    if type(limit) is not int or limit <= 0:
        raise ValueError(f"limit must be a positive int, got {limit!r}")
    statement = (
        select(EnterpriseObject)
        .where(EnterpriseObject.workspace_id == workspace_id)
        .order_by(EnterpriseObject.created_at.desc(), EnterpriseObject.id.desc())
        .limit(limit)
    )
    return list(session.scalars(statement))
