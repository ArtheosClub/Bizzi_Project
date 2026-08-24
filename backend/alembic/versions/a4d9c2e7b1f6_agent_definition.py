"""agent definition

Creates the standalone `agent_definitions` table for WP14, as authorized by
Amendment A-10 and ADR-0015. The table carries exactly the six-field schema
foundation: id, workspace_id, phase, owner_id, created_at, updated_at.

No corresponding `enterprise_objects` row is created. Runtime/configuration
concerns remain deferred.

Revision ID: a4d9c2e7b1f6
Revises: f7c3a92e1d5b
Create Date: 2026-08-24
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "a4d9c2e7b1f6"
down_revision: str | Sequence[str] | None = "f7c3a92e1d5b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "agent_definitions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "phase",
            sa.String(length=32),
            server_default="active",
            nullable=False,
        ),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "phase IN ('active', 'archived', 'superseded')",
            name=op.f("ck_agent_definitions_phase_is_known"),
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspaces.id"],
            name=op.f("fk_agent_definitions_workspace_id_workspaces"),
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
            name=op.f("fk_agent_definitions_owner_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_agent_definitions")),
    )
    op.create_index(
        op.f("ix_agent_definitions_workspace_id"),
        "agent_definitions",
        ["workspace_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_agent_definitions_owner_id"),
        "agent_definitions",
        ["owner_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_agent_definitions_owner_id"), table_name="agent_definitions")
    op.drop_index(op.f("ix_agent_definitions_workspace_id"), table_name="agent_definitions")
    op.drop_table("agent_definitions")
