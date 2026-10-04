"""Bounded identity resolution, server-side membership/Workspace facts only."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workspace import Workspace
from app.models.workspace_membership import WorkspaceMembership


def find_for_identity(db: Session, user_id: UUID) -> list[tuple[WorkspaceMembership, Workspace]]:
    # Identity resolution precedes Workspace selection; no client scope accepted.
    rows = db.execute(
        select(WorkspaceMembership, Workspace)
        .execution_options(populate_existing=True)
        .join(Workspace, Workspace.id == WorkspaceMembership.workspace_id)
        .where(WorkspaceMembership.user_id == user_id)
        .limit(2)
    ).all()
    return [(membership, workspace) for membership, workspace in rows]
