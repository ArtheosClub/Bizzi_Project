"""AuditRecord — the persisted ADR-0014 Q2 subject-reference representation.

This file implements the model portion of A-11's approved bounded operational
core. A-11 also requires the migration, tests, an append-only repository, a
minimal `AuditService.record(...)`, the write-time validation contract, and the
one-session/one-transaction atomicity guarantee; this file alone does not
complete WP19.

The persisted shape itself is
`00_ARCHITECTURE/07_AUDIT/ADW07_Q2_PERSISTED_REPRESENTATION_DECISION.md`:
BR3/N3 with accepted Q2-EX-O1 -- five typed subject-reference columns, one
per current D1 subject kind, with a database-enforced exactly-one
guarantee and no separate persisted kind token.

Deliberate choices, recorded here so they read as decisions rather than
omissions:

- **The five `subject_*` columns carry no FOREIGN KEY.** Accepted Q2-RI
  admits absent database FK enforcement only "where durable correctness,
  validation, and historical subject resolvability are established
  through another explicit, recorded mechanism" -- here, the write-time
  validation contract A-11 also requires. The write-time validation
  contract is implemented by the service portion of this same WP19
  bounded implementation and must be present before that implementation
  is complete or merge-ready. Separately, the accepted Q2
  persisted-representation decision Section 8 selects no FK delete
  behavior for these columns and pre-approves none; D3 Section 5 leaves
  FK action expressly undecided. Adding a real FK now would force an
  undecided delete-behavior choice as a side effect of a column
  definition -- exactly what those two records declined to do.

- **`workspace_id` does carry a real FOREIGN KEY, with no `ondelete`.**
  This is the opposite choice from the five subject columns, and it is a
  separate decision, not a consequence of the same reasoning applied
  twice. ADR-0004 requires the column and workspace-scoped access, but no
  foreign key -- A-11-CLAR-01 records the FK itself as a Project Owner
  implementation choice, matching every other implemented workspace-scoped
  Gate C table (`enterprise_objects`, `tasks`, `agent_definitions`,
  `workspace_memberships`). No explicit `ON DELETE` is specified, matching
  those same tables -- the resulting behavior is PostgreSQL's `NO ACTION`,
  and A-11-CLAR-01 accepts explicitly that a `workspaces` row cannot be
  physically deleted while audit records scoped to it exist.

- **No `subject_type` or other kind-token column.** Accepted Q2-EX-O1: the
  audited subject kind is determined structurally by which of the five
  `subject_*` columns is populated, not by a separately stored value. A
  stored kind token is the shape Q2-EX-O2 rejected -- carrying the kind in
  two places would make one historical fact a pair of statements that must
  agree for every committed record, forever.

- **`content` is JSONB, not text.** A-11's Deliverables record content as
  "a field-level diff," a structured value, not a serialized blob to be
  re-parsed on every read. JSONB additionally allows Postgres-side
  indexing and containment queries later, without requiring a schema
  change now -- an availability, not a commitment; no such query is
  authorized or implemented here.

- **No `updated_at`.** A committed AuditRecord is immutable (D10 Section
  7.4: audit records are Historical Record, permanent) and A-11's
  Deliverables specify an append-only repository exposing no update path.
  An `updated_at` column would assert a capability -- that a row can
  change after creation -- that this record's own governing decisions
  deny it. Its absence is the decision, not an oversight.

- **Exactly one of the five `subject_*` columns is populated, enforced by
  a single named CHECK.** This is Q2-EX-O1's exactly-one guarantee,
  "enforced at the database persistence boundary." The accepted Q2
  decision §9 deliberately leaves exact column names, the SQL and
  check-constraint syntax for the exactly-one guarantee, and index
  definitions to implementation. The sum-of-casts expression is this
  implementation's choice, not a normative requirement of Q2-EX-O1 or of
  the final Q2 decision.
"""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

#: Named per `app/db/base.py`'s convention (`ck_%(table_name)s_%(constraint_name)s`).
#: Sum of five `IS NOT NULL` casts equalling 1 -- Q2-EX-O1's exactly-one
#: guarantee, expressed directly over this table's own persisted columns.
EXACTLY_ONE_SUBJECT_REFERENCE = (
    "(CAST(subject_workspace_id IS NOT NULL AS INTEGER) + "
    "CAST(subject_enterprise_object_id IS NOT NULL AS INTEGER) + "
    "CAST(subject_user_id IS NOT NULL AS INTEGER) + "
    "CAST(subject_workspace_membership_id IS NOT NULL AS INTEGER) + "
    "CAST(subject_task_id IS NOT NULL AS INTEGER)) = 1"
)


class AuditRecord(Base):
    __tablename__ = "audit_records"

    __table_args__ = (
        CheckConstraint(
            EXACTLY_ONE_SUBJECT_REFERENCE,
            name="exactly_one_subject_reference",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ADR-0004 scoping, with a real FK as a Project Owner implementation
    # choice recorded in A-11-CLAR-01 -- not a consequence of ADR-0004
    # itself, which requires the column and workspace-scoped access but
    # not a foreign key. No `ondelete`: NO ACTION, accepted explicitly.
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("workspaces.id"),
        nullable=False,
        index=True,
    )

    # ADR-0005 `AuditActions.*` named-constant vocabulary (A-11
    # Deliverables). The vocabulary itself belongs to this WP19 bounded
    # implementation's service layer; this column only carries the value.
    action: Mapped[str] = mapped_column(String(64), nullable=False)

    # A-11 Deliverables: "content as a field-level diff," not a full
    # snapshot -- WP19's own conservative interim choice.
    content: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    # The columns intentionally carry no ForeignKey. A-11 requires their
    # referential correctness through the service-layer write-time validation
    # contract. No subject-column index is added because A-11 authorizes no
    # subject-specific query workload, and the accepted Q2 decision §9 leaves
    # index definitions to implementation; indexes may be proposed later from
    # demonstrated read patterns.
    subject_workspace_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    subject_enterprise_object_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    subject_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    subject_workspace_membership_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    subject_task_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    def __repr__(self) -> str:
        return f"<AuditRecord id={self.id!r} action={self.action!r}>"
