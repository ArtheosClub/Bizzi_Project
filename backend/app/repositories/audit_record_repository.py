"""AuditRecord repository -- the append-only persistence surface for WP19's
A-11 bounded operational audit core.

A-11's approved Deliverables require an **append-only** repository: insert
and read only, with no update or delete path implemented. There is no
`update()`, no `delete()`, and no bulk write here. Their absence makes
this repository's public API append-only -- it does not make the table
immutable, since anything holding a `Session` (or issuing raw SQL) can
still write to it by other means. A database-level immutability guarantee
is not in A-11's scope and is not claimed here.

`add()` is an internal mechanism of `AuditService.record(...)`, not an
application-code entry point. It accepts an already-validated
`AuditRecord` and performs no validation of its own. The write-time
validation contract that accepted Q2-RI requires -- the explicit recorded
mechanism standing in for the absent foreign keys on the five `subject_*`
columns -- lives in `audit_service.py`, which is the only production
module permitted to import this one.
`tests/test_audit_repository_boundary.py` asserts that boundary
statically, in both directions.

`add()` never commits and never rolls back. A-11 requires the business
mutation and its audit record to be written through one SQLAlchemy
session and one transaction: whoever opened the transaction is the only
party entitled to end it, and this module is not that party. `flush()`
is called so the record's identity and server-side defaults are readable
inside the same transaction, and so a constraint violation surfaces at
the write rather than at some unrelated later point.

Read methods are workspace-scoped (ADR-0004).
"""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit_record import AuditRecord

DEFAULT_LIST_LIMIT = 100


def add(session: Session, record: AuditRecord) -> AuditRecord:
    """Insert one already-validated record into the caller's transaction.

    **Internal to `AuditService.record(...)`.** Calling this directly from
    application code bypasses the write-time validation contract that
    stands in for the absent foreign keys on the five `subject_*` columns
    -- the record this function inserts is trusted verbatim, not checked.

    Never commits, never rolls back -- see the module docstring. `flush()`
    sends the INSERT so `id` and `created_at` are readable within the
    same transaction.
    """
    session.add(record)
    session.flush()
    return record


def list_by_workspace(
    session: Session,
    workspace_id: uuid.UUID,
    *,
    limit: int = DEFAULT_LIST_LIMIT,
) -> list[AuditRecord]:
    """Records for one workspace ordered by timestamp and stable UUID tie-breaker.

    Workspace-scoped per ADR-0004: `workspace_id` is a required positional
    argument, not an optional filter, so an unscoped read cannot be
    written by accident.

    Ordered `created_at DESC, id DESC`. This ordering is deterministic,
    but chronological only across differing timestamps -- PostgreSQL
    `now()` is transaction-start time, so several records written within
    one transaction can share a `created_at`. `id DESC` is a stable
    tie-breaker for that case, not a claim about insertion order.

    `type(limit) is not int` rather than `not isinstance(limit, int)`:
    `bool` is a subclass of `int`, so `isinstance(True, int)` is `True`
    and `limit=True` would otherwise silently pass as `limit=1`.
    """
    if type(limit) is not int or limit <= 0:
        raise ValueError(f"limit must be a positive int, got {limit!r}")

    statement = (
        select(AuditRecord)
        .where(AuditRecord.workspace_id == workspace_id)
        .order_by(AuditRecord.created_at.desc(), AuditRecord.id.desc())
        .limit(limit)
    )
    return list(session.scalars(statement))
