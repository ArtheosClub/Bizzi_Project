"""AgentDefinition — WP14 schema foundation.

ADR-0013 classifies AgentDefinition as a D02 EnterpriseObject. ADR-0015
establishes standalone persistence as the MVP default for D02 specializations,
and Amendment A-10 fixes WP14's minimum schema foundation to exactly six
fields: id, workspace_id, phase, owner_id, created_at, updated_at.

No corresponding `enterprise_objects` row is created. Capabilities,
permissions, Provider/Model references, RuntimeSession wiring, tool/context/
escalation policy, and runtime configuration remain deferred by A-10.
"""

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

PHASE_ACTIVE = "active"
PHASE_ARCHIVED = "archived"
PHASE_SUPERSEDED = "superseded"

AGENT_DEFINITION_PHASES = (PHASE_ACTIVE, PHASE_ARCHIVED, PHASE_SUPERSEDED)


class AgentDefinition(Base):
    __tablename__ = "agent_definitions"

    __table_args__ = (
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

    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("workspaces.id"),
        nullable=False,
        index=True,
    )

    phase: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default=PHASE_ACTIVE,
        server_default=PHASE_ACTIVE,
    )

    # D02 ownership, not actor attribution. Creation attribution belongs to
    # audit/provenance work, not to this column.
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
        return f"<AgentDefinition id={self.id!r} phase={self.phase!r}>"
