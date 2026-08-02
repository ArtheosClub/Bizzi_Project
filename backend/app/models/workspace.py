"""Workspace — the primary tenancy boundary.

D01 (`APPROVED — CLOSED`) makes Workspace the primary ownership,
authorization, governance, and isolation boundary for business state.
ADR-0004 requires every other Gate C table to carry a `workspace_id`
pointing here.

Workspace itself therefore carries no `workspace_id`: it *is* the
boundary, not something scoped by one. It is the FK target for
WP13–WP22, not a participant in their scoping.

Fields are exactly those specified by WP12a in
`50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md` — `id`, `name`, `owner_id`,
timestamps. Nothing else is added. In particular there is no status or
lifecycle column: D07 treats Phase, Status, Outcome, Progress and Health
as distinct semantic dimensions, and no approved ADW-01 decision defines a
Workspace lifecycle. Inventing one here would create domain semantics
outside the Architecture Freeze (DECISION_0003 §7).
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Indexed but deliberately *not* a ForeignKey: the `users` table does
    # not exist until WP16 (Minimal Identity and Authentication). The
    # constraint is added by WP16's own migration, not fabricated here
    # against a table that isn't there. Indexed now because owner lookup
    # is the expected access path and adding the index later would mean a
    # second migration over a populated table.
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    # server_default so the database is the clock, not the application —
    # rows created by a migration, a fixture, or psql all get consistent
    # timestamps. timezone=True keeps these as timestamptz.
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
        return f"<Workspace id={self.id!r} name={self.name!r}>"
