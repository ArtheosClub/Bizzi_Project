"""EnterpriseObject — the shared abstraction for durable business things.

D02 (`APPROVED`) defines Enterprise Object as "the stable platform
abstraction for a durable, workspace-owned, business-relevant thing with
identity, lifecycle, ownership, relationships, state, and governance
requirements."

Two consequences shape this model, both from
`docs/adr/DOMAIN_REVIEW_ENTERPRISE_OBJECT.md`:

- It is an *abstraction*, not an aggregate. D07 §7 assigns authoritative
  state ownership to the "Specialized Enterprise Object aggregate," so this
  table is the shared contract, not the owner of any specialized type's
  state.
- It is referenced, never owner-of. D09 R7/R8/R9 give Business Operation,
  Decision and Work Item each a Reference relationship *to* Enterprise
  Object with "neither owns the other," and D09 Prohibition 5 forbids
  Enterprise Object from holding an authoritative collection of what
  references it. There are therefore no relationship columns here and no
  ORM relationship() to any of them.

The field set is exactly WP13's, as amended by A-01 (`status` -> `phase`):
id, workspace_id, type, phase, owner_id, timestamps. Nothing else.
"""

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

#: The three permitted `phase` values (ADR-0009).
#:
#: Derived from D10 §6's Per-Concept Lifecycle Capability row for Enterprise
#: Object, read against D10 §5's definitions — not from any scenario.
#: `draft` is absent because no approved source gives Enterprise Object a
#: pre-active phase; `deprecated` is absent because D10 §5.8 makes it
#: forward-looking guidance orthogonal to Phase, so folding it in would
#: collapse two D07 §6 dimensions.
PHASE_ACTIVE = "active"
PHASE_ARCHIVED = "archived"
PHASE_SUPERSEDED = "superseded"

ENTERPRISE_OBJECT_PHASES = (PHASE_ACTIVE, PHASE_ARCHIVED, PHASE_SUPERSEDED)


class EnterpriseObject(Base):
    __tablename__ = "enterprise_objects"

    __table_args__ = (
        # A CHECK constraint rather than a Postgres ENUM, per ADR-0009 §6:
        # the value set is newly derived, and a CHECK is alterable in one
        # migration where an ENUM makes value removal effectively
        # irreversible.
        CheckConstraint(
            "phase IN ('active', 'archived', 'superseded')",
            name="phase_is_known",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ADR-0004: every Gate C entity is workspace-scoped. Unlike `owner_id`
    # below, this is a real ForeignKey — `workspaces` exists as of WP12a, so
    # there is a table to point at. D01 makes Workspace the isolation
    # boundary; the index exists because every query is scoped by it.
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("workspaces.id"),
        nullable=False,
        index=True,
    )

    # The specialization discriminator D02 implies ("specialized types retain
    # explicit contracts and invariants").
    #
    # Deliberately *not* constrained to an enumerated set. No approved source
    # enumerates Enterprise Object's specializations, so a CHECK constraint
    # here would invent domain concepts inside a frozen domain model
    # (DECISION_0003 §7). Constraining it later is one migration; un-inventing
    # a concept that has shipped is not.
    type: Mapped[str] = mapped_column(String(100), nullable=False)

    # ADR-0009. Named `phase`, not `status`: D07 §6.1 defines Phase as "where
    # is the subject in its governed lifecycle," and LAW-D07-15 prohibits
    # collapsing Phase, Status, Outcome, Progress and Health into one
    # universal authoritative `status` field.
    #
    # Created directly `active` — Domain Review §1a shows this is forced
    # rather than chosen, since `archived` and `superseded` are each defined
    # relative to a prior active condition.
    #
    # There is no `superseded_by_id` column. D10 §12 (Binding consequence 4)
    # requires supersession to record a D09-typed relationship, and modelling
    # that as a direct self-FK here would commit to a representation before
    # the general relationship mechanism is designed (ADR-0009,
    # "A constraint on future work"). Nothing in WP13 performs transitions,
    # so nothing here sets this to `superseded`.
    phase: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default=PHASE_ACTIVE,
        server_default=PHASE_ACTIVE,
    )

    # WP16 backfills this as a real ForeignKey now that `users` exists,
    # same as `Workspace.owner_id`.
    #
    # Note this is ownership (D02), not attribution: D09 R10 attributes an
    # Actor to {Decision, Business Operation, Work Item, Runtime Session},
    # a set that excludes Enterprise Object. Creation attribution belongs to
    # the audit record (ADW-07, deferred), not to a column here.
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
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
        return (
            f"<EnterpriseObject id={self.id!r} type={self.type!r} "
            f"phase={self.phase!r}>"
        )
