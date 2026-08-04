"""Task model tests — WP15, as amended by A-04.

No database needed. These assert the schema-level value domain WP15
actually delivers — not the transition graph ADR-0011 fixes normatively
but this WP does not enforce. No test here is named as though it
verifies a transition, because none does: a `CHECK` constraint sees only
the row being written, never its prior value.

`test_task_persistence.py` covers the real round-trip against Postgres
in CI, including the value-domain rejection cases.
"""

from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import CheckConstraint

from app.db.base import Base
from app.models import Task
from app.models.task import TASK_PHASES

TASK_REVISION = "f7c3a92e1d5b"
USER_AND_MEMBERSHIP_REVISION = "d21a6f4c9e8b"
ALEMBIC_INI = Path(__file__).resolve().parent.parent / "alembic.ini"


def test_task_is_registered_on_base_metadata() -> None:
    """The P1 aggregation guard.

    If `app.models` stops importing Task, this fails here rather than
    silently letting a later autogenerate emit DROP TABLE for a real
    table.
    """
    assert "tasks" in Base.metadata.tables


def test_task_has_exactly_the_a04_columns() -> None:
    """WP15 as amended by A-04: id, workspace_id, phase, source_object_id,
    timestamps — and nothing else.

    Asserting the exact set is what catches scope creep: `priority`,
    `assignee_id`, `title`, or any of the other examined-and-excluded
    fields reappearing without amending A-04 fails here.
    """
    assert set(Task.__table__.columns.keys()) == {
        "id",
        "workspace_id",
        "phase",
        "source_object_id",
        "created_at",
        "updated_at",
    }


def test_no_excluded_fields() -> None:
    """Domain Review §4–§6, §8 — each of these was considered and excluded.

    Named individually so a future re-addition of any one of them is a
    visible, deliberate diff against this test, not a silent column add.
    """
    columns = Task.__table__.columns.keys()
    for excluded in (
        "progress",
        "priority",
        "assignee_id",
        "owner_id",
        "title",
        "description",
        "created_by",
    ):
        assert excluded not in columns


def test_phase_permits_exactly_five_values() -> None:
    """D10 §6 + §8 Invariant 6, derived in the Domain Review §3."""
    assert TASK_PHASES == (
        "active",
        "archived",
        "superseded",
        "cancelled",
        "completed",
    )


def test_phase_has_a_check_constraint_naming_those_values() -> None:
    """A CHECK, not a Postgres ENUM — ADR-0009 §6's reversibility reasoning.

    This constraint is the value domain only. It does not, and cannot,
    express ADR-0011's transition graph — see the migration's own
    docstring.
    """
    checks = [
        c for c in Task.__table__.constraints if isinstance(c, CheckConstraint)
    ]
    assert len(checks) == 1

    condition = str(checks[0].sqltext)
    for phase in TASK_PHASES:
        assert f"'{phase}'" in condition


def test_phase_defaults_to_active() -> None:
    """ADR-0011: creation → active. Checked on both defaults.

    Python-level `default` covers ORM-created rows; `server_default`
    covers direct inserts. Both are asserted here; only a persistence
    test against a real database proves the `server_default` actually
    reaches Postgres (see `test_task_persistence.py`).
    """
    phase = Task.__table__.columns["phase"]
    assert phase.server_default is not None
    assert "active" in str(phase.server_default.arg)
    assert phase.default is not None
    assert phase.default.arg == "active"


def test_workspace_id_is_required_indexed_and_a_real_foreign_key() -> None:
    """ADR-0004 / D01."""
    workspace_id = Task.__table__.columns["workspace_id"]

    assert workspace_id.nullable is False
    assert {fk.target_fullname for fk in workspace_id.foreign_keys} == {
        "workspaces.id"
    }
    assert any(
        list(index.columns) == [workspace_id] for index in Task.__table__.indexes
    )


def test_source_object_id_is_nullable_indexed_and_a_real_foreign_key() -> None:
    """D09 R9's N≤1 simplification (Domain Review §7) — nullable, not required."""
    source_object_id = Task.__table__.columns["source_object_id"]

    assert source_object_id.nullable is True
    assert {fk.target_fullname for fk in source_object_id.foreign_keys} == {
        "enterprise_objects.id"
    }
    assert any(
        list(index.columns) == [source_object_id]
        for index in Task.__table__.indexes
    )


def test_required_columns_are_not_nullable() -> None:
    for name in ("id", "workspace_id", "phase", "created_at", "updated_at"):
        assert Task.__table__.columns[name].nullable is False


def test_timestamps_have_server_defaults() -> None:
    """The database is the clock, not the application."""
    for name in ("created_at", "updated_at"):
        assert Task.__table__.columns[name].server_default is not None


def test_constraints_use_the_naming_convention() -> None:
    """P2 applied, not merely declared."""
    table = Task.__table__

    assert table.primary_key.name == "pk_tasks"

    checks = [c for c in table.constraints if isinstance(c, CheckConstraint)]
    assert checks[0].name == "ck_tasks_phase_is_known"

    workspace_fks = list(table.columns["workspace_id"].foreign_keys)
    assert workspace_fks[0].constraint.name == "fk_tasks_workspace_id_workspaces"

    source_object_fks = list(table.columns["source_object_id"].foreign_keys)
    assert (
        source_object_fks[0].constraint.name
        == "fk_tasks_source_object_id_enterprise_objects"
    )


def test_migration_is_wired_into_the_revision_chain() -> None:
    """This migration must follow WP16's, and be the single head.

    Resolved through Alembic's own ScriptDirectory, same as every prior
    migration test — a chain Alembic cannot resolve fails here too, and a
    second head appearing (making `upgrade head` ambiguous) fails here.
    """
    script = ScriptDirectory.from_config(Config(str(ALEMBIC_INI)))

    assert script.get_heads() == [TASK_REVISION]

    revision = script.get_revision(TASK_REVISION)
    assert revision.down_revision == USER_AND_MEMBERSHIP_REVISION
