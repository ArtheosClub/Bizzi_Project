"""WP19 attribution and record-4b bootstrap uniqueness; no subject/FK rewrite."""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "adw02_02"
down_revision: str | Sequence[str] | None = "adw02_01"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "audit_records", sa.Column("actor_id", postgresql.UUID(as_uuid=True), nullable=True)
    )
    op.add_column(
        "audit_records", sa.Column("membership_id", postgresql.UUID(as_uuid=True), nullable=True)
    )
    op.create_index(
        "uq_audit_bootstrap_workspace_action",
        "audit_records",
        ["workspace_id", "action"],
        unique=True,
        postgresql_where=sa.text(
            "action IN ('user.bootstrap_created', 'workspace.bootstrap_created', "
            "'workspace_membership.bootstrap_created')"
        ),
    )


def downgrade() -> None:
    op.drop_index("uq_audit_bootstrap_workspace_action", table_name="audit_records")
    op.drop_column("audit_records", "membership_id")
    op.drop_column("audit_records", "actor_id")
