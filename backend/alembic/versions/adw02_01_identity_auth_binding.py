"""WP16 identity binding; Owner records 4/5; no passwords or FK changes."""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "adw02_01"
down_revision: str | Sequence[str] | None = "ea58e0c4ee4d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Existing bare identities remain unbound and cannot authenticate.
    op.add_column("users", sa.Column("auth_issuer", sa.String(512), nullable=True))
    op.add_column("users", sa.Column("auth_subject", sa.String(255), nullable=True))
    op.add_column("users", sa.Column("deactivated_at", sa.DateTime(timezone=True), nullable=True))
    op.create_unique_constraint(
        "uq_users_auth_issuer_auth_subject", "users", ["auth_issuer", "auth_subject"]
    )
    op.create_check_constraint(
        op.f("ck_users_auth_binding_is_complete"),
        "users",
        "(auth_issuer IS NULL AND auth_subject IS NULL) OR "
        "(auth_issuer IS NOT NULL AND auth_subject IS NOT NULL "
        "AND auth_issuer <> '' AND auth_subject <> '')",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("ck_users_auth_binding_is_complete"), "users", type_="check")
    op.drop_constraint("uq_users_auth_issuer_auth_subject", "users", type_="unique")
    op.drop_column("users", "deactivated_at")
    op.drop_column("users", "auth_subject")
    op.drop_column("users", "auth_issuer")
