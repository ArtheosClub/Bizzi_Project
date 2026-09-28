"""WP13/A-12: create, archive and unarchive in the caller's transaction.

RuntimeEvent emission is deferred by A-12. ADR-0005's post-commit obligation
is neither discharged nor reinterpreted: it passes to the work package that
delivers RuntimeEventService after ADW-07 defines event semantics.

Supersession is permitted by ADR-0009 but cannot be implemented until its
D09-typed relationship exists (D10 section 12). No API, actor attribution,
authorization policy, type/owner mutation or deletion is added here. Workspace
and owner identifiers come from the trusted caller; scoping is not authorization.

The caller must roll back on mutation or audit failure. Neither this module nor
its repository ends the transaction, and neither can enforce correct recovery
by a caller that catches an exception and commits anyway. The model's schema
is unchanged.

LookupError means not found within the requested workspace, ValueError means
an invalid phase transition. No HTTP status is selected in this API-free slice.
"""

import uuid

from sqlalchemy.orm import Session

from app.models.enterprise_object import PHASE_ACTIVE, PHASE_ARCHIVED, EnterpriseObject
from app.repositories import enterprise_object_repository
from app.services.audit_actions import ENTERPRISE_OBJECT_CREATED, ENTERPRISE_OBJECT_UPDATED
from app.services.audit_service import AuditService


def _transition(
    session: Session,
    workspace_id: uuid.UUID,
    object_id: uuid.UUID,
    before: str,
    after: str,
) -> None:
    obj = enterprise_object_repository.get_by_id(session, workspace_id, object_id, for_update=True)
    if obj is None:
        raise LookupError("EnterpriseObject not found in workspace")
    if obj.phase != before:
        raise ValueError(f"cannot transition EnterpriseObject from {obj.phase!r} to {after!r}")
    obj.phase = after
    AuditService.record(
        session,
        subject=obj,
        action=ENTERPRISE_OBJECT_UPDATED,
        content={"phase": [before, after]},
        expected_workspace_id=workspace_id,
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
    ) -> uuid.UUID:
        """Create active, flush for audit identity, and return only that identity."""
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
        )
        return obj.id

    @staticmethod
    def archive(session: Session, *, workspace_id: uuid.UUID, object_id: uuid.UUID) -> None:
        """Only active -> archived; repeated archive fails before audit."""
        _transition(session, workspace_id, object_id, PHASE_ACTIVE, PHASE_ARCHIVED)

    @staticmethod
    def unarchive(session: Session, *, workspace_id: uuid.UUID, object_id: uuid.UUID) -> None:
        """Only archived -> active; superseded is terminal."""
        _transition(session, workspace_id, object_id, PHASE_ARCHIVED, PHASE_ACTIVE)
