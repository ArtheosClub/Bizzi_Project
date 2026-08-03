"""Workspace model tests.

These need no database. They assert things that are cheap to get wrong
and expensive to discover later: the model's shape matches WP12a exactly,
the naming convention is actually applied rather than merely configured,
and the migration is wired into the revision chain.

`test_workspace_persistence.py` covers the real round-trip against
Postgres in CI.
"""

from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import Column, MetaData, String, Table, UniqueConstraint

from app.db.base import Base
from app.models import Workspace

WORKSPACE_REVISION = "b1c4f7a2e9d3"
BASELINE_REVISION = "e0aa881262f5"
ALEMBIC_INI = Path(__file__).resolve().parent.parent / "alembic.ini"


def test_workspace_is_registered_on_base_metadata() -> None:
    """The P1 aggregation guard.

    If `app.models` stops importing Workspace, this fails here rather than
    silently letting a later autogenerate emit DROP TABLE for a real table.
    """
    assert "workspaces" in Base.metadata.tables


def test_workspace_has_exactly_the_wp12a_columns() -> None:
    """WP12a specifies id, name, owner_id, timestamps — and nothing else.

    Asserting the exact set rather than mere presence is what catches
    scope creep: a status column added without an approved lifecycle
    decision fails here.
    """
    assert set(Workspace.__table__.columns.keys()) == {
        "id",
        "name",
        "owner_id",
        "created_at",
        "updated_at",
    }


def test_workspace_carries_no_workspace_id() -> None:
    """ADR-0004: Workspace *is* the tenancy boundary, not a scoped entity."""
    assert "workspace_id" not in Workspace.__table__.columns


def test_required_columns_are_not_nullable() -> None:
    for name in ("id", "name", "owner_id", "created_at", "updated_at"):
        assert Workspace.__table__.columns[name].nullable is False


def test_timestamps_have_server_defaults() -> None:
    """The database is the clock, not the application."""
    for name in ("created_at", "updated_at"):
        assert Workspace.__table__.columns[name].server_default is not None


def test_owner_id_is_indexed_and_has_a_foreign_key_to_users() -> None:
    """WP16 backfills this now that `users` exists."""
    owner_id = Workspace.__table__.columns["owner_id"]
    assert {fk.target_fullname for fk in owner_id.foreign_keys} == {"users.id"}
    assert any(
        list(index.columns) == [owner_id] for index in Workspace.__table__.indexes
    )


def test_primary_key_uses_the_naming_convention() -> None:
    """P2 applied, not merely declared."""
    assert Workspace.__table__.primary_key.name == "pk_workspaces"


def test_naming_convention_applies_to_future_constraints() -> None:
    """Proves the convention is live on Base.metadata for tables not yet written.

    Built on a throwaway MetaData carrying the same convention, so running
    the suite registers nothing on Base.metadata as a side effect.
    """
    metadata = MetaData(naming_convention=Base.metadata.naming_convention)
    table = Table(
        "convention_probe",
        metadata,
        Column("id", String(36), primary_key=True),
        Column("email", String(255)),
        UniqueConstraint("email"),
    )

    assert table.primary_key.name == "pk_convention_probe"
    unique = [c for c in table.constraints if isinstance(c, UniqueConstraint)]
    assert unique[0].name == "uq_convention_probe_email"


def test_migration_is_wired_into_the_revision_chain() -> None:
    """The migration must follow the Gate B baseline, not float detached.

    Resolved through Alembic's own ScriptDirectory rather than by importing
    the migration module — that is how Alembic itself walks the chain, so
    a chain Alembic cannot resolve fails here too.

    This no longer asserts that WP12a's revision is the chain's head: WP13
    now follows it. The single-head assertion lives with whichever migration
    is currently last, in `test_enterprise_object_model.py`, so exactly one
    test owns it rather than every migration test needing an edit each time
    the head moves.
    """
    script = ScriptDirectory.from_config(Config(str(ALEMBIC_INI)))

    revision = script.get_revision(WORKSPACE_REVISION)
    assert revision.down_revision == BASELINE_REVISION
