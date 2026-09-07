"""AuditRecord model tests — WP19, Amendment A-11 and A-11-CLAR-01.

No database needed. These assert the schema-level shape this migration
portion of A-11's bounded operational core actually delivers -- not the
write-time validation contract, which belongs to the service portion of
the same WP19 bounded implementation and must be present before the
implementation is merge-ready, and not any query workload against the
five subject columns, which A-11 does not authorize.
"""

from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base import Base
from app.models import AuditRecord
from app.models.audit_record import EXACTLY_ONE_SUBJECT_REFERENCE

AUDIT_RECORD_REVISION = "ea58e0c4ee4d"
AGENT_DEFINITION_REVISION = "a4d9c2e7b1f6"
ALEMBIC_INI = Path(__file__).resolve().parent.parent / "alembic.ini"

SUBJECT_COLUMNS = (
    "subject_workspace_id",
    "subject_enterprise_object_id",
    "subject_user_id",
    "subject_workspace_membership_id",
    "subject_task_id",
)


def test_audit_record_is_registered_on_base_metadata() -> None:
    """The aggregation guard (`app/models/__init__.py`'s own docstring).

    If `app.models` stops importing AuditRecord, this fails here rather
    than silently letting a later autogenerate emit DROP TABLE for a
    real table.
    """
    assert "audit_records" in Base.metadata.tables


def test_table_name_is_audit_records() -> None:
    """ADW07_Q2_PERSISTED_REPRESENTATION_DECISION.md — the table this
    decision's BR3/N3 shape is realized as."""
    assert AuditRecord.__tablename__ == "audit_records"


def test_audit_record_has_exactly_the_a11_columns() -> None:
    """The bounded implementation schema derived from A-11 and the
    existing model conventions -- A-11's Deliverables name the content
    the record must carry, not every column (e.g. `id`, `created_at`
    follow the existing model conventions, not an explicit A-11 list).

    Asserting the exact set is what catches scope creep: a `subject_type`
    column, an `updated_at` column, or any other field reappearing
    without amending A-11 fails here.
    """
    assert set(AuditRecord.__table__.columns.keys()) == {
        "id",
        "workspace_id",
        "action",
        "content",
        *SUBJECT_COLUMNS,
        "created_at",
    }


def test_required_columns_are_not_nullable() -> None:
    """A-11 Deliverables: workspace_id required; action, content, and
    created_at are the record's minimum content."""
    for name in ("id", "workspace_id", "action", "content", "created_at"):
        assert AuditRecord.__table__.columns[name].nullable is False


def test_subject_columns_are_nullable() -> None:
    """Q2-EX-O1: exactly one of the five is populated per record, so each
    column must individually admit NULL."""
    for name in SUBJECT_COLUMNS:
        assert AuditRecord.__table__.columns[name].nullable is True


def test_content_is_jsonb() -> None:
    """A-11 Deliverables: content as a field-level diff, a structured
    value -- asserting the type, not just the column's presence, so a
    later change to `Text` does not pass silently."""
    assert isinstance(AuditRecord.__table__.columns["content"].type, JSONB)


def test_workspace_id_is_a_real_foreign_key_with_no_ondelete() -> None:
    """A-11-CLAR-01: workspace_id carries a real FK to workspaces.id as a
    Project Owner implementation choice, with no ON DELETE -- the
    resulting behavior is NO ACTION, accepted explicitly."""
    workspace_id = AuditRecord.__table__.columns["workspace_id"]

    assert len(workspace_id.foreign_keys) == 1
    fk = next(iter(workspace_id.foreign_keys))
    assert fk.target_fullname == "workspaces.id"
    assert fk.ondelete is None
    assert any(
        list(index.columns) == [workspace_id]
        for index in AuditRecord.__table__.indexes
    )


def test_subject_columns_have_no_foreign_keys() -> None:
    """Accepted Q2-RI / the accepted Q2 decision §8 / D3 §5: no FK and no
    delete behavior is selected for the five subject-reference columns.

    This catches any later foreign key added without separate authority
    selecting that subject relation's FK and delete behavior. The
    service-layer validation contract does not itself authorize foreign
    keys — the five columns stay FK-free until a separate decision says
    otherwise, regardless of whether the service exists.
    """
    for name in SUBJECT_COLUMNS:
        assert len(AuditRecord.__table__.columns[name].foreign_keys) == 0


def test_no_subject_type_column() -> None:
    """Accepted Q2-EX-O1: subject kind is structural (which column is
    populated), not a separately stored token."""
    assert "subject_type" not in AuditRecord.__table__.columns.keys()


def test_no_updated_at_column() -> None:
    """D10 §7.4 (Historical Record permanence) / A-11's append-only
    repository: a committed AuditRecord is never updated."""
    assert "updated_at" not in AuditRecord.__table__.columns.keys()


def test_exactly_one_subject_reference_check_constraint_exists() -> None:
    """Q2-EX-O1's exactly-one guarantee, enforced at the database
    persistence boundary.

    Compares against the implementation's own `EXACTLY_ONE_SUBJECT_REFERENCE`
    constant rather than only checking the constraint's name and count --
    a constraint named correctly but expressing `1 = 1` would otherwise
    pass. The expression's exact syntax is this implementation's choice
    (the accepted Q2 decision §9 leaves it open); what is asserted is that
    the constraint carries the expression this implementation selected,
    not that any record mandates that form. Zero-, one-, and two-subject
    behavior against a real database belongs to the persistence tests
    that come later with the service.

    The constraint's resolved name is asserted in
    test_constraints_use_the_naming_convention, matching how the Task
    model tests split content from naming: once bound to the table,
    `app/db/base.py`'s convention resolves the name to
    ck_audit_records_exactly_one_subject_reference.
    """
    checks = [
        c
        for c in AuditRecord.__table__.constraints
        if isinstance(c, CheckConstraint)
    ]
    assert len(checks) == 1
    assert str(checks[0].sqltext) == EXACTLY_ONE_SUBJECT_REFERENCE


def test_constraints_use_the_naming_convention() -> None:
    """P2 applied, not merely declared (`app/db/base.py`)."""
    table = AuditRecord.__table__

    assert table.primary_key.name == "pk_audit_records"

    workspace_fks = list(table.columns["workspace_id"].foreign_keys)
    assert (
        workspace_fks[0].constraint.name
        == "fk_audit_records_workspace_id_workspaces"
    )

    checks = [c for c in table.constraints if isinstance(c, CheckConstraint)]
    assert checks[0].name == "ck_audit_records_exactly_one_subject_reference"


def test_migration_is_wired_into_the_revision_chain() -> None:
    """The audit_record migration must follow agent_definition directly.

    Later migrations may legitimately follow it; this guard verifies only
    its own predecessor.
    """
    script = ScriptDirectory.from_config(Config(str(ALEMBIC_INI)))

    revision = script.get_revision(AUDIT_RECORD_REVISION)
    assert revision.down_revision == AGENT_DEFINITION_REVISION
