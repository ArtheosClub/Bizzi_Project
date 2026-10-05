"""WP15 prospective record-5 Stage 3: CREATE TASK ONLY, synthetic local scope.

A-13 remains unapproved; preservation of the earlier candidate is not authority.
RuntimeEvent emission is deferred by Owner record 4, not waived. All bounded
D07 deferrals expire before the first real user or authoritative use.

Create verifies persisted actor/membership/Workspace facts and carries trusted
ActorContext to AuditService. Caller owns the transaction and must roll back on
mutation/audit failure; no expected-version, idempotency or full history claim.
No source reference creation: D09 R9 needs a separately decided owner authority.

The original archive/unarchive candidate code below is preserved without
invocation, implementation permission or conformance claim. Repository reads
are likewise outside Stage 3's permitted operations. Their removal/redesign
requires another scope. No API or production exposure is introduced.
"""

import uuid

from sqlalchemy.orm import Session

from app.core.actor_context import ActorContext
from app.models.task import PHASE_ACTIVE, PHASE_ARCHIVED, Task
from app.repositories import task_repository
from app.services.audit_actions import TASK_CREATED, TASK_UPDATED
from app.services.audit_service import AuditService, _validate_actor


def _transition(
    session: Session,
    workspace_id: uuid.UUID,
    task_id: uuid.UUID,
    before: str,
    after: str,
) -> None:
    obj = task_repository.get_by_id(session, workspace_id, task_id, for_update=True)
    if obj is None:
        raise LookupError("Task not found in workspace")
    if obj.phase != before:
        raise ValueError(f"cannot transition Task from {obj.phase!r} to {after!r}")
    obj.phase = after
    AuditService.record(
        session,
        subject=obj,
        action=TASK_UPDATED,
        content={"phase": [before, after]},
        expected_workspace_id=workspace_id,
    )


class TaskService:
    """Create is prospectively authorized; other candidate operations are excluded."""

    @staticmethod
    def create(
        session: Session,
        *,
        workspace_id: uuid.UUID,
        source_object_id: uuid.UUID | None = None,
        actor_context: ActorContext | None = None,
    ) -> uuid.UUID:
        """Create active, flush for audit identity, and return only that identity."""
        if source_object_id is not None:
            raise ValueError("source_object_id creation requires separately approved R9 authority")
        _validate_actor(session, actor_context, workspace_id)
        obj = Task(workspace_id=workspace_id, phase=PHASE_ACTIVE, source_object_id=None)
        task_repository.add(session, obj)
        AuditService.record(
            session,
            subject=obj,
            action=TASK_CREATED,
            content={
                "workspace_id": [None, str(obj.workspace_id)],
                "phase": [None, obj.phase],
            },
            expected_workspace_id=workspace_id,
            actor_context=actor_context,
        )
        return obj.id

    @staticmethod
    def archive(session: Session, *, workspace_id: uuid.UUID, task_id: uuid.UUID) -> None:
        """Only active -> archived; repeated archive fails before audit."""
        _transition(session, workspace_id, task_id, PHASE_ACTIVE, PHASE_ARCHIVED)

    @staticmethod
    def unarchive(session: Session, *, workspace_id: uuid.UUID, task_id: uuid.UUID) -> None:
        """Only archived -> active; completed/cancelled/superseded are terminal."""
        _transition(session, workspace_id, task_id, PHASE_ARCHIVED, PHASE_ACTIVE)
