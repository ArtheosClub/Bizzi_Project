"""EnterpriseObject model tests — WP13.

No database needed. These assert the things that are cheap to get wrong and
expensive to discover later: that the model's shape matches WP13 as amended
by A-01, that the constitutional prohibitions are actually absent from the
schema rather than merely absent from the author's intent, and that the
migration is wired into the revision chain.

`test_enterprise_object_persistence.py` covers the real round-trip against
Postgres in CI.
"""

from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import CheckConstraint

from app.db.base import Base
from app.models import EnterpriseObject
from app.models.enterprise_object import ENTERPRISE_OBJECT_PHASES

ENTERPRISE_OBJECT_REVISION = "c3e8b5d1f704"
WORKSPACE_REVISION = "b1c4f7a2e9d3"
ALEMBIC_INI = Path(__file__).resolve().parent.parent / "alembic.ini"


def test_enterprise_object_is_registered_on_base_metadata() -> None:
    """The P1 aggregation guard.

    If `app.models` stops importing EnterpriseObject, this fails here rather
    than silently letting a later autogenerate emit DROP TABLE for a real
    table.
    """
    assert "enterprise_objects" in Base.metadata.tables


def test_enterprise_object_has_exactly_the_wp13_columns() -> None:
    """WP13 as amended by A-01: id, workspace_id, type, phase, owner, timestamps.

    Asserting the exact set rather than mere presence is what catches scope
    creep — a `name`, a `description`, or a relationship column added without
    an approved basis fails here.
    """
    assert set(EnterpriseObject.__table__.columns.keys()) == {
        "id",
        "workspace_id",
        "type",
        "phase",
        "owner_id",
        "created_at",
        "updated_at",
    }


def test_no_status_column() -> None:
    """D07 §6 / LAW-D07-15, asserted rather than assumed.

    Phase, Status, Outcome, Progress and Health may not be collapsed into one
    universal authoritative `status` field. Amendment A-01 renamed WP13's
    field to `phase` for exactly this reason; this test is what stops it
    drifting back under a future edit.
    """
    assert "status" not in EnterpriseObject.__table__.columns


def test_no_generic_deletion_flag() -> None:
    """D10 §12 (Binding consequence 3) makes a generic flag a defect.

    "Bizzi never uses an undifferentiated `deleted = true` flag as an
    authoritative lifecycle state" (D10 Lifecycle Principle 2). Disappearance
    is expressed through the named phase, not a boolean.
    """
    columns = EnterpriseObject.__table__.columns.keys()
    for forbidden in ("deleted", "is_deleted", "deleted_at", "archived"):
        assert forbidden not in columns


def test_no_superseded_by_column() -> None:
    """ADR-0009, "A constraint on future work".

    D10 §12 (Binding consequence 4) requires supersession to record a
    D09-typed relationship. Modelling that as a direct self-FK would commit
    to a representation before the general relationship mechanism is
    designed, so it is deliberately absent — Architecture Review question 4.
    """
    assert "superseded_by_id" not in EnterpriseObject.__table__.columns


def test_no_relationship_columns_to_referencing_concepts() -> None:
    """D09 Prohibition 5.

    Enterprise Object "must never hold an authoritative (non-derived)
    collection of every Business Operation, Decision, or Work Item that
    references it." R7/R8/R9 all point *toward* Enterprise Object and are
    owned by the other side, so no column here may point back.
    """
    columns = EnterpriseObject.__table__.columns.keys()
    for forbidden in (
        "decision_id",
        "business_operation_id",
        "work_item_id",
        "task_id",
    ):
        assert forbidden not in columns


def test_phase_permits_exactly_three_values() -> None:
    """ADR-0009 §2. Not four, and not `draft`."""
    assert ENTERPRISE_OBJECT_PHASES == ("active", "archived", "superseded")


def test_phase_has_a_check_constraint_naming_those_values() -> None:
    """ADR-0009 §6: a CHECK, not a Postgres ENUM — because CHECK is reversible."""
    checks = [
        c
        for c in EnterpriseObject.__table__.constraints
        if isinstance(c, CheckConstraint)
    ]
    assert len(checks) == 1

    condition = str(checks[0].sqltext)
    for phase in ENTERPRISE_OBJECT_PHASES:
        assert f"'{phase}'" in condition
    assert "'draft'" not in condition
    assert "'deprecated'" not in condition


def test_phase_defaults_to_active() -> None:
    """Domain Review §1a: `active` is the only admissible initial phase.

    `archived` and `superseded` are each defined relative to a prior active
    condition, so neither is coherent at creation. Checked on the server
    default so a row inserted by a migration or by psql behaves the same as
    one inserted through the ORM.
    """
    phase = EnterpriseObject.__table__.columns["phase"]
    assert phase.server_default is not None
    assert "active" in str(phase.server_default.arg)
    assert phase.default is not None
    assert phase.default.arg == "active"


def test_type_is_not_constrained_to_an_enumerated_set() -> None:
    """Architecture Review question 2, asserted as a guard.

    No approved source enumerates Enterprise Object's specializations, so
    constraining `type` here would invent domain concepts inside a frozen
    domain model (DECISION_0003 §7). The single CHECK on the table is
    `phase`'s; a second one appearing on `type` means someone enumerated
    them.
    """
    checks = [
        c
        for c in EnterpriseObject.__table__.constraints
        if isinstance(c, CheckConstraint)
    ]
    assert len(checks) == 1
    assert "type" not in str(checks[0].sqltext)


def test_workspace_id_is_required_indexed_and_a_real_foreign_key() -> None:
    """ADR-0004 / D01. Unlike `owner_id`, `workspaces` exists to point at."""
    workspace_id = EnterpriseObject.__table__.columns["workspace_id"]

    assert workspace_id.nullable is False
    assert {fk.target_fullname for fk in workspace_id.foreign_keys} == {
        "workspaces.id"
    }
    assert any(
        list(index.columns) == [workspace_id]
        for index in EnterpriseObject.__table__.indexes
    )


def test_owner_id_is_indexed_but_has_no_foreign_key() -> None:
    """Deliberate until WP16 creates the `users` table — same as WP12a."""
    owner_id = EnterpriseObject.__table__.columns["owner_id"]

    assert owner_id.foreign_keys == set()
    assert any(
        list(index.columns) == [owner_id]
        for index in EnterpriseObject.__table__.indexes
    )


def test_required_columns_are_not_nullable() -> None:
    for name in (
        "id",
        "workspace_id",
        "type",
        "phase",
        "owner_id",
        "created_at",
        "updated_at",
    ):
        assert EnterpriseObject.__table__.columns[name].nullable is False


def test_timestamps_have_server_defaults() -> None:
    """The database is the clock, not the application."""
    for name in ("created_at", "updated_at"):
        assert EnterpriseObject.__table__.columns[name].server_default is not None


def test_constraints_use_the_naming_convention() -> None:
    """P2 applied, not merely declared."""
    table = EnterpriseObject.__table__

    assert table.primary_key.name == "pk_enterprise_objects"

    checks = [c for c in table.constraints if isinstance(c, CheckConstraint)]
    assert checks[0].name == "ck_enterprise_objects_phase_is_known"

    foreign_keys = list(table.columns["workspace_id"].foreign_keys)
    assert (
        foreign_keys[0].constraint.name
        == "fk_enterprise_objects_workspace_id_workspaces"
    )


def test_migration_is_wired_into_the_revision_chain() -> None:
    """This migration must follow WP12a's, and be the single head.

    Resolved through Alembic's own ScriptDirectory rather than by importing
    the migration module — that is how Alembic itself walks the chain, so a
    chain Alembic cannot resolve fails here too. It also catches a second
    head appearing, which would make `upgrade head` ambiguous.
    """
    script = ScriptDirectory.from_config(Config(str(ALEMBIC_INI)))

    assert script.get_heads() == [ENTERPRISE_OBJECT_REVISION]

    revision = script.get_revision(ENTERPRISE_OBJECT_REVISION)
    assert revision.down_revision == WORKSPACE_REVISION
