"""task

Creates the `tasks` table -- WP15, as amended by A-04
(`MVP_WORK_PACKAGE_PLAN.md` Section Gate C -- Amendments): a Work Item
specialization and aggregate root (D03, D08), workspace-scoped, with a
five-value governed `phase` and an optional reference to the
EnterpriseObject it's work on.

Hand-written, same reason as WP13's and WP16's migrations: no live
database connection in the authoring environment. Verified against
`Base.metadata` via `alembic upgrade --sql head` (offline mode) and by
`backend/tests/test_task_model.py`, which asserts the emitted schema
matches the ORM model field-for-field.

Deliberate choices, recorded here so they read as decisions rather than
omissions:

- **`phase` is a CHECK-constrained VARCHAR enumerating five values, not
  a Postgres ENUM.** Same reversibility reasoning as
  `enterprise_objects.phase` (ADR-0009 Section 6): the value set is
  newly derived (D10 Section 6 + Section 8 Invariant 6, see
  `docs/adr/DOMAIN_REVIEW_TASK_LIFECYCLE.md` Section 3), and a CHECK is
  alterable in one migration where an ENUM makes value removal
  effectively irreversible.

- **This CHECK enforces the value domain only -- it is not, and cannot
  be, the transition graph `docs/adr/0011-task-phase-transition-graph.md`
  fixes.** A SQL CHECK constraint evaluates only the row being written;
  it has no access to the row's prior value. It cannot reject
  `completed -> archived`, `cancelled -> active`, or any other
  disallowed transition -- every one of those is a plain UPDATE to a
  value the constraint permits in isolation. ADR-0011 is the normative
  source for which transitions are permitted. WP15 intentionally does
  not introduce database-level transition enforcement -- transition
  authority belongs to the audited service layer (WP19, ADR-0005), a
  scope boundary for this WP, not a permanent prohibition on ever
  enforcing transitions in the database.

- **The five phase values are duplicated here, deliberately, rather than
  imported from `app.models.task.TASK_PHASES`.** Migrations must not
  import model code: a migration is a snapshot of the schema at its own
  point in time, and importing a model that later changes would make
  replaying this migration against a clean database depend on code that
  has since moved on. Both this copy and the model's `TASK_PHASES`
  answer to the same normative source, ADR-0011 -- if they ever
  disagree, the ADR is what settles which one is stale.

- **`workspace_id` has a real FOREIGN KEY.** `workspaces` exists as of
  WP12a. ADR-0004 requires the scoping.

- **`source_object_id` is a nullable FOREIGN KEY to `enterprise_objects.id`,
  not a join table.** D09 R9's approved cardinality is 1 Work Item :
  0..N Enterprise Objects; this column ships the N<=1 subset as a
  recorded simplification (Domain Review Section 7), not a domain
  invariant. `enterprise_objects` exists as of WP13.

- **No `assignee_id`, `owner_id`, `priority`, `progress`, `title`, or
  `description`.** Each was examined and excluded with a reason in the
  Domain Review (Sections 4-6, 8) -- omissions here are decisions, not
  gaps.

Revision ID: f7c3a92e1d5b
Revises: d21a6f4c9e8b
Create Date: 2026-08-04

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f7c3a92e1d5b"
down_revision: str | Sequence[str] | None = "d21a6f4c9e8b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "phase",
            sa.String(length=32),
            server_default="active",
            nullable=False,
        ),
        sa.Column(
            "source_object_id", postgresql.UUID(as_uuid=True), nullable=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "phase IN ('active', 'archived', 'superseded', 'cancelled', "
            "'completed')",
            name=op.f("ck_tasks_phase_is_known"),
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspaces.id"],
            name=op.f("fk_tasks_workspace_id_workspaces"),
        ),
        sa.ForeignKeyConstraint(
            ["source_object_id"],
            ["enterprise_objects.id"],
            name=op.f("fk_tasks_source_object_id_enterprise_objects"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tasks")),
    )
    op.create_index(
        op.f("ix_tasks_workspace_id"),
        "tasks",
        ["workspace_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_tasks_source_object_id"),
        "tasks",
        ["source_object_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_tasks_source_object_id"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_workspace_id"), table_name="tasks")
    op.drop_table("tasks")
