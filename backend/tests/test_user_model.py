"""WP16 identity schema, original foundation plus Owner records 4/5.

No passwords or email anchor. Identity binding/deactivation are now approved
for the bounded synthetic scope; historical migration contracts are retained.
"""

from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory

from app.db.base import Base
from app.models import User

USER_AND_MEMBERSHIP_REVISION = "d21a6f4c9e8b"
ENTERPRISE_OBJECT_REVISION = "c3e8b5d1f704"
ALEMBIC_INI = Path(__file__).resolve().parent.parent / "alembic.ini"


def test_user_is_registered_on_base_metadata() -> None:
    """The P1 aggregation guard.

    If `app.models` stops importing User, this fails here rather than
    silently letting a later autogenerate emit DROP TABLE for a real
    table.
    """
    assert "users" in Base.metadata.tables


def test_user_has_exactly_approved_identity_columns() -> None:
    """Pin only the Owner-approved shared identity realization."""
    assert set(User.__table__.columns.keys()) == {
        "id",
        "created_at",
        "updated_at",
        "auth_issuer",
        "auth_subject",
        "deactivated_at",
    }


def test_required_columns_are_not_nullable() -> None:
    for name in ("id", "created_at", "updated_at"):
        assert User.__table__.columns[name].nullable is False


def test_timestamps_have_server_defaults() -> None:
    """The database is the clock, not the application."""
    for name in ("created_at", "updated_at"):
        assert User.__table__.columns[name].server_default is not None


def test_primary_key_uses_the_naming_convention() -> None:
    """P2 applied, not merely declared."""
    assert User.__table__.primary_key.name == "pk_users"


def test_migration_is_wired_into_the_revision_chain() -> None:
    """Must follow WP13's migration.

    The single-head assertion lives in
    `test_workspace_membership_model.py`, since that model's migration is
    the same one that creates `users` and is the current chain head —
    exactly one test owns it, per the convention established when the
    head moved from WP12a's migration to WP13's.
    """
    script = ScriptDirectory.from_config(Config(str(ALEMBIC_INI)))

    revision = script.get_revision(USER_AND_MEMBERSHIP_REVISION)
    assert revision.down_revision == ENTERPRISE_OBJECT_REVISION


def test_identity_revision_is_the_single_head() -> None:
    script = ScriptDirectory.from_config(Config(str(ALEMBIC_INI)))
    assert "adw02_01" in {
        revision.revision for revision in script.walk_revisions(base="base", head="heads")
    }
    assert script.get_revision("adw02_01").down_revision == "ea58e0c4ee4d"
