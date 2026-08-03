"""WorkspaceMembership — the join entity for workspace-scoped identity.

`docs/c4/C3_COMPONENT.md`'s "Multi-tenancy" section resolves this shape,
project-owner-confirmed before any Gate C model was written: identity is
the one exception to ADR-0004's flat `workspace_id` pattern.
`ActorContext` for a request resolves to a role by looking up
`(user_id, workspace_id)` here, never by reading a field off `User`
directly.

ADR-0010 governs `role`: the column ships now, `CHECK`-constrained to the
one value currently authorized (`owner`). GC-004 (Membership Role Model —
single scalar `role` column vs. a role-assignment join table) is *not*
approved by this — it stays open, deliberately, until a second role
exists to force the real choice. Widening the `CHECK` is the signal that
GC-004 needs an actual decision, not an assumption carried forward.

No `WorkspaceInvitation`. ADR-0010 resolves GC-003 as deferred / not
applicable to the MVP: the MVP scenario has no invitation at all, so
storage-shape questions for one don't apply.

Deliberately no `updated_at`, matching `C3_COMPONENT.md`'s resolved shape
exactly (`id, workspace_id, user_id, role, created_at` — five fields, no
more). `role` could in principle change later, and every other Gate C
table carries `updated_at`, but this table's shape was already
project-owner-confirmed at exactly five fields; adding a sixth here would
be this file quietly re-opening a question ADR-0010 didn't reopen. Worth
revisiting only if GC-004 itself reopens (a second role would make
`role` mutable in a way that matters).
"""

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

#: The one `role` value currently authorized (ADR-0010).
ROLE_OWNER = "owner"

WORKSPACE_MEMBERSHIP_ROLES = (ROLE_OWNER,)


class WorkspaceMembership(Base):
    __tablename__ = "workspace_memberships"

    __table_args__ = (
        # CHECK, not ENUM, same reasoning as EnterpriseObject.phase
        # (ADR-0009 §6): alterable in one migration when GC-004 reopens
        # and a second role is added, where an ENUM makes value removal
        # effectively irreversible.
        CheckConstraint(
            "role IN ('owner')",
            name="role_is_known",
        ),
        UniqueConstraint("workspace_id", "user_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ADR-0004: workspace-scoped, real FK — `workspaces` exists.
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("workspaces.id"),
        nullable=False,
        index=True,
    )

    # Real FK — `users` is created in this same migration.
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # ADR-0010: ships now, CHECK-constrained to the single value
    # currently authorized. GC-004 (scalar vs. join) stays unapproved.
    role: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    def __repr__(self) -> str:
        return (
            f"<WorkspaceMembership workspace_id={self.workspace_id!r} "
            f"user_id={self.user_id!r} role={self.role!r}>"
        )
