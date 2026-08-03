"""WorkspaceMembership model tests — WP16 Amendment A-03 (schema foundation).

No database needed. These assert the `C3_COMPONENT.md`-resolved shape
exactly, the ADR-0010 role constraint (ships, but not GC-004's answer),
and that this migration is the current chain head.

`test_workspace_membership_persistence.py` covers the real round-trip
against Postgres in CI.
"""

from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import CheckConstraint, UniqueConstraint

from app.db.base import Base
from app.models import WorkspaceMembership
from app.models.workspace_membership import WORKSPACE_MEMBERSHIP_ROLES

USER_AND_MEMBERSHIP_REVISION = "d21a6f4c9e8b"
ENTERPRISE_OBJECT_REVISION = "c3e8b5d1f704"
ALEMBIC_INI = Path(__file__).resolve().parent.parent / "alembic.ini"


def test_workspace_membership_is_registered_on_base_metadata() -> None:
    """The P1 aggregation guard."""
    assert "workspace_memberships" in Base.metadata.tables


def test_workspace_membership_has_exactly_the_c3_component_columns() -> None:
    """`C3_COMPONENT.md`: id, workspace_id, user_id, role, created_at.

    Five columns, no more — in particular no `updated_at`, asserted
    explicitly below so the omission reads as a decision, not a gap this
    test failed to catch.
    """
    assert set(WorkspaceMembership.__table__.columns.keys()) == {
        "id",
        "workspace_id",
        "user_id",
        "role",
        "created_at",
    }


def test_no_updated_at_column() -> None:
    """Deliberate fidelity to the already-resolved C3_COMPONENT.md shape.

    Every other Gate C table carries `updated_at`; this one doesn't,
    because the resolved shape doesn't. Revisiting this is tied to GC-004
    reopening, not to this table's own convenience.
    """
    assert "updated_at" not in WorkspaceMembership.__table__.columns


def test_role_permits_exactly_one_value() -> None:
    """ADR-0010: `owner` only. GC-004 stays unapproved."""
    assert WORKSPACE_MEMBERSHIP_ROLES == ("owner",)


def test_role_has_a_check_constraint_naming_that_value() -> None:
    """ADR-0010 / ADR-0009 §6 reasoning: CHECK, not ENUM — reversible."""
    checks = [
        c
        for c in WorkspaceMembership.__table__.constraints
        if isinstance(c, CheckConstraint)
    ]
    assert len(checks) == 1

    condition = str(checks[0].sqltext)
    assert "'owner'" in condition


def test_workspace_id_is_required_indexed_and_a_real_foreign_key() -> None:
    """ADR-0004 / D01."""
    workspace_id = WorkspaceMembership.__table__.columns["workspace_id"]

    assert workspace_id.nullable is False
    assert {fk.target_fullname for fk in workspace_id.foreign_keys} == {
        "workspaces.id"
    }
    assert any(
        list(index.columns) == [workspace_id]
        for index in WorkspaceMembership.__table__.indexes
    )


def test_user_id_is_required_indexed_and_a_real_foreign_key() -> None:
    """`users` is created in this same migration, so a real FK is possible."""
    user_id = WorkspaceMembership.__table__.columns["user_id"]

    assert user_id.nullable is False
    assert {fk.target_fullname for fk in user_id.foreign_keys} == {"users.id"}
    assert any(
        list(index.columns) == [user_id]
        for index in WorkspaceMembership.__table__.indexes
    )


def test_unique_on_workspace_id_and_user_id() -> None:
    """One membership row per (workspace, user) pair."""
    unique_constraints = [
        c
        for c in WorkspaceMembership.__table__.constraints
        if isinstance(c, UniqueConstraint)
    ]
    assert len(unique_constraints) == 1
    assert [c.name for c in unique_constraints[0].columns] == [
        "workspace_id",
        "user_id",
    ]


def test_required_columns_are_not_nullable() -> None:
    for name in ("id", "workspace_id", "user_id", "role", "created_at"):
        assert WorkspaceMembership.__table__.columns[name].nullable is False


def test_created_at_has_a_server_default() -> None:
    """The database is the clock, not the application."""
    assert WorkspaceMembership.__table__.columns["created_at"].server_default is not None


def test_constraints_use_the_naming_convention() -> None:
    """P2 applied, not merely declared."""
    table = WorkspaceMembership.__table__

    assert table.primary_key.name == "pk_workspace_memberships"

    checks = [c for c in table.constraints if isinstance(c, CheckConstraint)]
    assert checks[0].name == "ck_workspace_memberships_role_is_known"

    workspace_fks = list(table.columns["workspace_id"].foreign_keys)
    assert (
        workspace_fks[0].constraint.name
        == "fk_workspace_memberships_workspace_id_workspaces"
    )

    user_fks = list(table.columns["user_id"].foreign_keys)
    assert user_fks[0].constraint.name == "fk_workspace_memberships_user_id_users"


def test_migration_is_wired_into_the_revision_chain() -> None:
    """This migration must follow WP13's, and be the single head.

    Resolved through Alembic's own ScriptDirectory, same as every prior
    migration test — a chain Alembic cannot resolve fails here too, and a
    second head appearing (making `upgrade head` ambiguous) fails here.
    """
    script = ScriptDirectory.from_config(Config(str(ALEMBIC_INI)))

    assert script.get_heads() == [USER_AND_MEMBERSHIP_REVISION]

    revision = script.get_revision(USER_AND_MEMBERSHIP_REVISION)
    assert revision.down_revision == ENTERPRISE_OBJECT_REVISION
