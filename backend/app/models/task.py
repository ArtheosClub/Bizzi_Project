"""Task — a Work Item specialization and aggregate root (D03, D08).

`docs/adr/DOMAIN_REVIEW_TASK_LIFECYCLE.md` derives this shape from
D01-D10 and WP02 directly, then Amendment A-04
(`MVP_WORK_PACKAGE_PLAN.md` Section Gate C -- Amendments) fixes it as
WP15's scope. Two conclusions carry the most weight:

- Task is an entity, not an association between EnterpriseObject and an
  Actor (Domain Review Section 1) -- D08 calls Task a "separate
  aggregate root," D10 Section 8 Invariant 6 gives it terminal states
  independent of what it relates to, and D09 R9's cardinality (0..N,
  lower bound zero) means a Task can exist with nothing to relate to at
  all. Section 1a confirms this survives the field cuts below.
- `phase`'s five values are derived from D10 (Section 3), but the
  *transition graph* among them required a separate decision --
  `docs/adr/0011-task-phase-transition-graph.md` -- because the sources
  left it genuinely open, not merely unstated. That ADR is the
  normative source for the graph; this migration enforces only the
  value domain (see the migration's own docstring for why a CHECK
  constraint cannot enforce a transition graph).

Excluded, each with a reason (Domain Review Sections 4-8): `progress`
(D07 Section 6.4 defines the dimension, nothing shapes its values);
`priority` (no approved source, no demonstrated need -- WP02 is one
task, nothing to prioritize against); `assignee_id` / `owner_id` (a
column that can only reference `users` would be a false contract, since
WP02's actual assignee is an agent, not a human, and AgentDefinition
does not exist yet); `title` / `description` (not attested by WP02 --
that content belongs to the EnterpriseObject being analyzed, not the
Task performing work on it).
"""

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

#: The five permitted `phase` values (D10 Section 6 + Section 8 Invariant 6).
#:
#: Derived in `docs/adr/DOMAIN_REVIEW_TASK_LIFECYCLE.md` Section 3, not from
#: WP02's scenario. `active` is the creation value -- every other value
#: presupposes a prior condition. The transition graph among these five
#: (which of them reach which others) is fixed normatively by ADR-0011,
#: not by this value list -- see the migration docstring.
PHASE_ACTIVE = "active"
PHASE_ARCHIVED = "archived"
PHASE_SUPERSEDED = "superseded"
PHASE_CANCELLED = "cancelled"
PHASE_COMPLETED = "completed"

TASK_PHASES = (
    PHASE_ACTIVE,
    PHASE_ARCHIVED,
    PHASE_SUPERSEDED,
    PHASE_CANCELLED,
    PHASE_COMPLETED,
)


class Task(Base):
    __tablename__ = "tasks"

    __table_args__ = (
        # Value domain only -- ADR-0011's transition graph (which values
        # may follow which) is not and cannot be expressed by a CHECK,
        # which sees only the row being written, never its prior value.
        CheckConstraint(
            "phase IN ('active', 'archived', 'superseded', 'cancelled', "
            "'completed')",
            name="phase_is_known",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ADR-0004: every Gate C entity is workspace-scoped. Real FK --
    # `workspaces` exists as of WP12a.
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("workspaces.id"),
        nullable=False,
        index=True,
    )

    # ADR-0011. Created directly `active` (Domain Review Section 3: every
    # other value presupposes a prior condition). CHECK enforces the value
    # domain only; ADR-0011's transition graph is enforced by the eventual
    # audited service (WP19), not here.
    #
    # server_default exists only because inserts may bypass SQLAlchemy.
    # The authoritative semantic default is ADR-0011, not this column --
    # if the Python `default` and `server_default` ever drift apart,
    # ADR-0011 is what settles which one is right.
    phase: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default=PHASE_ACTIVE,
        server_default=PHASE_ACTIVE,
    )

    # D09 R9: Work Item `relates_to` Enterprise Object, cardinality
    # 1 Work Item : 0..N Enterprise Objects. Nullable single FK ships the
    # N<=1 subset of that approved 0..N range -- a recorded simplification
    # (Domain Review Section 7), not a domain invariant. A second reference
    # from the same Task would require a join table, not a wider column.
    # Service code must not assume a Task can by nature relate to only one
    # EnterpriseObject.
    source_object_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("enterprise_objects.id"),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<Task id={self.id!r} phase={self.phase!r}>"
