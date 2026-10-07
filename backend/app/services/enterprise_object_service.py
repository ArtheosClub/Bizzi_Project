"""WP13/A-12: create, archive and unarchive in the caller's transaction.

RuntimeEvent emission is deferred by A-12. ADR-0005's post-commit obligation
is neither discharged nor reinterpreted: it passes to the work package that
delivers RuntimeEventService after ADW-07 defines event semantics.

Supersession is permitted by ADR-0009 but cannot be implemented until its
D09-typed relationship exists (D10 section 12). Stage 2 adds actor/membership
attribution and checks the persisted owner
membership before writes under the prospective record-5 scope. No API,
type/owner mutation or deletion is added. Workspace scoping alone is not
authorization; trusted context is confirmed against persisted facts.

The caller must roll back on mutation or audit failure. Neither this module nor
its repository ends the transaction, and neither can enforce correct recovery
by a caller that catches an exception and commits anyway. The model's schema
is unchanged.

LookupError means not found within the requested workspace, ValueError means
an invalid phase transition. No HTTP status is selected in this API-free slice.
"""

import uuid

from sqlalchemy.orm import Session

from app.core.actor_context import ActorContext
from app.core.preproduction_guard import require_session
from app.models.enterprise_object import PHASE_ACTIVE, PHASE_ARCHIVED, EnterpriseObject
from app.repositories import enterprise_object_repository
from app.services.audit_actions import ENTERPRISE_OBJECT_CREATED, ENTERPRISE_OBJECT_UPDATED
from app.services.audit_service import AuditService, validate_actor


def _transition(
    session: Session,
    workspace_id: uuid.UUID,
    object_id: uuid.UUID,
    before: str,
    after: str,
    actor_context: ActorContext | None,
) -> None:
    require_session(session)
    obj = enterprise_object_repository.get_by_id(session, workspace_id, object_id, for_update=True)
    if obj is None:
        raise LookupError("EnterpriseObject not found in workspace")
    if obj.phase != before:
        raise ValueError(f"cannot transition EnterpriseObject from {obj.phase!r} to {after!r}")
    validate_actor(session, actor_context, workspace_id)
    obj.phase = after
    AuditService.record(
        session,
        subject=obj,
        action=ENTERPRISE_OBJECT_UPDATED,
        content={"phase": [before, after]},
        expected_workspace_id=workspace_id,
        actor_context=actor_context,
    )


class EnterpriseObjectService:
    """Stateless namespace for the three approved A-12 operations."""

    @staticmethod
    def create(
        session: Session,
        *,
        workspace_id: uuid.UUID,
        type: str,
        owner_id: uuid.UUID,
        actor_context: ActorContext | None = None,
    ) -> uuid.UUID:
        """Create active, flush for audit identity, and return only that identity."""
        validate_actor(session, actor_context, workspace_id)
        if actor_context is None or owner_id != actor_context.actor_id:
            raise ValueError("creation owner does not match trusted actor")
        obj = EnterpriseObject(
            workspace_id=workspace_id, type=type, owner_id=owner_id, phase=PHASE_ACTIVE
        )
        enterprise_object_repository.add(session, obj)
        AuditService.record(
            session,
            subject=obj,
            action=ENTERPRISE_OBJECT_CREATED,
            content={
                "workspace_id": [None, str(obj.workspace_id)],
                "type": [None, obj.type],
                "owner_id": [None, str(obj.owner_id)],
                "phase": [None, obj.phase],
            },
            expected_workspace_id=workspace_id,
            actor_context=actor_context,
        )
        return obj.id

    @staticmethod
    def archive(
        session: Session,
        *,
        workspace_id: uuid.UUID,
        object_id: uuid.UUID,
        actor_context: ActorContext | None = None,
    ) -> None:
        """Only active -> archived; repeated archive fails before audit."""
        _transition(session, workspace_id, object_id, PHASE_ACTIVE, PHASE_ARCHIVED, actor_context)

    @staticmethod
    def unarchive(
        session: Session,
        *,
        workspace_id: uuid.UUID,
        object_id: uuid.UUID,
        actor_context: ActorContext | None = None,
    ) -> None:
        """Only archived -> active; superseded is terminal."""
        _transition(session, workspace_id, object_id, PHASE_ARCHIVED, PHASE_ACTIVE, actor_context)
