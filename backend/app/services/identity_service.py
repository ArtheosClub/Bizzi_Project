"""Read-only WP16 authentication/context orchestration under record 5.

No bootstrap writes before reviewed WP19 audit integration; no provider
contact. Actor/User Account share physical realization only in this MVP.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.actor_context import ActorContext
from app.core.authentication import TokenVerifier, authenticate
from app.core.authorization import AuthorizationService
from app.core.errors import AccessDeniedError
from app.core.preproduction_guard import require_session
from app.repositories import user_repository, workspace_membership_repository


class IdentityService:
    def __init__(self, db: Session, verifier: TokenVerifier) -> None:
        self.db = db
        self.verifier = verifier
        self.authorization = AuthorizationService()

    def resolve_actor_context(self, token: str | None, request_id: str) -> ActorContext:
        identity = authenticate(token, self.verifier)
        require_session(self.db)
        user = user_repository.get_by_auth_identity(self.db, identity.issuer, identity.subject)
        if user is None or user.deactivated_at is not None or not request_id:
            raise AccessDeniedError()
        memberships = workspace_membership_repository.find_for_identity(self.db, user.id)
        if len(memberships) != 1:
            raise AccessDeniedError()
        membership, workspace = memberships[0]
        context = ActorContext(user.id, workspace.id, membership.id, request_id)
        self.authorization.assert_owner(
            context,
            membership_id=membership.id,
            member_id=membership.user_id,
            workspace_id=workspace.id,
            workspace_owner_id=workspace.owner_id,
            role=membership.role,
            resource_workspace_id=workspace.id,
        )
        return context

    def authorize(self, context: ActorContext, resource_workspace_id: UUID) -> None:
        # Re-read facts even when ORM identities already exist in this Session.
        require_session(self.db)
        user = user_repository.get_by_id(self.db, context.actor_id)
        if user is None or user.deactivated_at is not None:
            raise AccessDeniedError()
        memberships = workspace_membership_repository.find_for_identity(self.db, user.id)
        if len(memberships) != 1:
            raise AccessDeniedError()
        membership, workspace = memberships[0]
        self.authorization.assert_owner(
            context,
            membership_id=membership.id,
            member_id=membership.user_id,
            workspace_id=workspace.id,
            workspace_owner_id=workspace.owner_id,
            role=membership.role,
            resource_workspace_id=resource_workspace_id,
        )
