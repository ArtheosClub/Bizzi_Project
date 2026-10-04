"""Pending Workspace creation for the single Owner bootstrap only."""

from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.models.workspace import Workspace


def create_for_bootstrap(db: Session, *, name: str, owner_id: UUID) -> Workspace:
    obj = Workspace(id=uuid4(), name=name, owner_id=owner_id)
    db.add(obj)
    return obj
