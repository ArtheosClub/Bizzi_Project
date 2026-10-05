"""Create-only pair primitive; endpoint alone owns the transaction.

No persisted EO-Task relationship or RuntimeEvent claim. Caller supplies
server-resolved ActorContext; primitives check persisted authorization facts.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.actor_context import ActorContext
from app.services.enterprise_object_service import EnterpriseObjectService
from app.services.task_service import TaskService


class BusinessRequestIntakeService:
    @staticmethod
    def create(db: Session, *, actor_context: ActorContext) -> UUID:
        if not db.in_transaction():
            raise ValueError("intake requires an endpoint-owned transaction")
        EnterpriseObjectService.create(
            db,
            workspace_id=actor_context.workspace_id,
            owner_id=actor_context.actor_id,
            type="business_request",
            actor_context=actor_context,
        )
        return TaskService.create(
            db, workspace_id=actor_context.workspace_id, actor_context=actor_context
        )
