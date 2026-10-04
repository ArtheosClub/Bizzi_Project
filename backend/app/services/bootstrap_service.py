"""Owner-only synthetic bootstrap; record 4b and record-5 amendment 1.

No subject IDs accepted. CLI invocation is not admitted outside pytest.
Caller owns the transaction; failures must propagate to its rollback boundary.
Bootstrap RuntimeEvent is retained under the sixth bounded deferral.
"""

from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.authentication import VerifiedIdentity
from app.repositories import user_repository, workspace_membership_repository, workspace_repository
from app.services.audit_service import AuditService


@dataclass(frozen=True, slots=True)
class BootstrapResult:
    user_id: UUID
    workspace_id: UUID
    membership_id: UUID


class BootstrapService:
    @staticmethod
    def create_owner(
        db: Session, *, identity: VerifiedIdentity, workspace_name: str
    ) -> BootstrapResult:
        if (
            not isinstance(identity, VerifiedIdentity)
            or not identity.issuer
            or not identity.subject
            or not workspace_name
        ):
            raise ValueError("bootstrap identity and Workspace name required")
        if not db.in_transaction():
            raise ValueError("bootstrap requires a caller-owned transaction")
        with db.no_autoflush:
            user = user_repository.create_for_bootstrap(
                db, issuer=identity.issuer, subject=identity.subject
            )
            workspace = workspace_repository.create_for_bootstrap(
                db, name=workspace_name, owner_id=user.id
            )
            membership = workspace_membership_repository.create_for_bootstrap(
                db, user_id=user.id, workspace_id=workspace.id
            )
            AuditService.record_bootstrap(db, user=user, workspace=workspace, membership=membership)
        return BootstrapResult(user.id, workspace.id, membership.id)
