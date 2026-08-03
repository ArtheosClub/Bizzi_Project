"""User — bare identity only, per WP16 Amendment A-03.

ADW-02 (Identity and Workspace Boundary) is the domain workshop that owns
identity and credential mechanics (`ADW_01_CORE_DOMAIN_SEMANTICS.md` §10
lists it as deferred beyond ADW-01) and it is unwritten. No approved
source anywhere in this repository specifies what fields `User` should
carry beyond bare identity.

Shipping `email`, `password_hash`, or any other credential-shaped field
now would settle ADW-02's scope by migration rather than by decision —
Architecture Review Checklist question 4's exact concern. Same treatment
`EnterpriseObject.type` already got for its own unenumerated values: ship
what's decided, leave undecided what isn't.

Fields are exactly `id`, `created_at`, `updated_at` — nothing else. This
table exists now only because `WorkspaceMembership.user_id` and the
`owner_id` FK backfills on `Workspace`/`EnterpriseObject` need a real
table to point at (both prior migrations explicitly promised "WP16's own
migration adds it"). Login, auth middleware, and any credential field
wait on ADW-02.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
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
        return f"<User id={self.id!r}>"
