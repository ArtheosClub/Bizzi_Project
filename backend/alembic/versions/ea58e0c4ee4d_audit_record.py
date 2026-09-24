"""audit_record

Creates the `audit_records` table -- WP19, Amendment A-11 (Approved
2026-09-06, `MVP_WORK_PACKAGE_PLAN.md` Section Gate C -- Amendments) and
A-11-CLAR-01 (Accepted 2026-09-07). This migration implements the
schema/migration portion of A-11's bounded operational core; the
repository, service, write-time validation contract, and atomicity tests
land as separate commits on the same branch before the WP19 PR is opened.

The persisted shape is
`00_ARCHITECTURE/07_AUDIT/ADW07_Q2_PERSISTED_REPRESENTATION_DECISION.md`:
BR3/N3 with accepted Q2-EX-O1.

Hand-written, same reason as the other Gate C migrations: no live database
connection in the authoring environment. Verified against `Base.metadata`
via `alembic upgrade --sql head` (offline mode) and by
`backend/tests/test_audit_record_model.py`, which asserts the emitted
schema matches the ORM model field-for-field.

Deliberate choices, recorded here so they read as decisions rather than
omissions:

- **The five `subject_*` columns are plain UUID columns, not foreign
  keys.** Accepted Q2-RI admits absent database FK enforcement only where
  another explicit, recorded mechanism supplies durable correctness,
  validation, and historical subject resolvability -- here, the
  write-time validation contract A-11 also requires, implemented in this
  same branch's service commit. The accepted Q2 persisted-representation
  decision Section 8 selects no FK delete behavior for these columns and
  pre-approves none; D3 Section 5 leaves FK action expressly undecided.
  A real FK now would force an undecided delete-behavior choice as a side
  effect of a column definition.

- **`workspace_id` is the opposite choice: a real FOREIGN KEY, with no
  `ON DELETE`.** This is not a consequence of ADR-0004 -- ADR-0004
  requires the column and workspace-scoped access, but no foreign key.
  A-11-CLAR-01 records the FK itself as a Project Owner implementation
  choice, matching every other implemented workspace-scoped Gate C table
  (`enterprise_objects`, `tasks`, `agent_definitions`,
  `workspace_memberships`). No `ON DELETE` clause is given, matching
  those same tables, where `ondelete` appears in no model and no
  migration -- the resulting behavior is PostgreSQL's `NO ACTION`.
  A-11-CLAR-01 accepts explicitly that a `workspaces` row cannot be
  physically deleted while audit records scoped to it exist.

- **No `subject_type` column.** Accepted Q2-EX-O1: subject kind is
  determined structurally by which of the five `subject_*` columns is
  populated, not by a separately stored value.

- **No `updated_at` column.** A committed AuditRecord is immutable (D10
  Section 7.4) and A-11's Deliverables specify an append-only repository
  exposing no update path. The column's absence is the decision.

- **The exactly-one CHECK's expression is this implementation's choice.**
  The accepted Q2 decision Section 9 deliberately leaves exact column
  names, the SQL and check-constraint syntax for the exactly-one
  guarantee, and index definitions to implementation. This migration
  expresses it as the sum of five `IS NOT NULL` casts equalling one; no
  cited record requires this particular syntax.

- **No index on any of the five `subject_*` columns.** A-11 authorizes no
  subject-specific query workload for this bounded scope; indexes may be
  proposed later from demonstrated read patterns, per the same accepted
  Q2 decision Section 9 that leaves index definitions to implementation.

Revision ID: ea58e0c4ee4d
Revises: a4d9c2e7b1f6
Create Date: 2026-09-07

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ea58e0c4ee4d"
down_revision: str | Sequence[str] | None = "a4d9c2e7b1f6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "audit_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("content", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "subject_workspace_id", postgresql.UUID(as_uuid=True), nullable=True
        ),
        sa.Column(
            "subject_enterprise_object_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column("subject_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "subject_workspace_membership_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column("subject_task_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "(CAST(subject_workspace_id IS NOT NULL AS INTEGER) + "
            "CAST(subject_enterprise_object_id IS NOT NULL AS INTEGER) + "
            "CAST(subject_user_id IS NOT NULL AS INTEGER) + "
            "CAST(subject_workspace_membership_id IS NOT NULL AS INTEGER) + "
            "CAST(subject_task_id IS NOT NULL AS INTEGER)) = 1",
            name=op.f("ck_audit_records_exactly_one_subject_reference"),
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspaces.id"],
            name=op.f("fk_audit_records_workspace_id_workspaces"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_audit_records")),
    )
    op.create_index(
        op.f("ix_audit_records_workspace_id"),
        "audit_records",
        ["workspace_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_audit_records_workspace_id"), table_name="audit_records")
    op.drop_table("audit_records")
