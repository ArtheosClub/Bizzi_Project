"""baseline

Revision ID: e0aa881262f5
Revises: 
Create Date: 2026-07-17 18:17:19.177246

"""
from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = 'e0aa881262f5'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
