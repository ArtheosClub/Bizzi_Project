"""Central owner-only policy, ADR-0006 and Owner record 4 Q07.

IdentityService obtains fresh persisted facts. The policy never trusts a
client-supplied Workspace or role; request context alone is insufficient.
"""

from uuid import UUID

from app.core.actor_context import ActorContext
from app.core.errors import AccessDeniedError


class AuthorizationService:
    def assert_owner(
        self,
        context: ActorContext,
        *,
        membership_id: UUID,
        member_id: UUID,
        workspace_id: UUID,
        workspace_owner_id: UUID,
        role: str,
        resource_workspace_id: UUID,
    ) -> None:
        if (
            context.membership_id != membership_id
            or context.actor_id != member_id
            or context.actor_id != workspace_owner_id
            or context.workspace_id != workspace_id
            or resource_workspace_id != workspace_id
            or role != "owner"
        ):
            raise AccessDeniedError()
