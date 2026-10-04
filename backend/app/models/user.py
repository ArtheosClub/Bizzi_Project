"""Human identity/Actor shared realization, Owner ADW-02 records 4/5.

Historic bare identities remain unbound, not fabricated into authenticated
Actors. No passwords/email anchor; four existing FK contracts preserved.
"""

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint("auth_issuer", "auth_subject", name="uq_users_auth_issuer_auth_subject"),
        CheckConstraint(
            "(auth_issuer IS NULL AND auth_subject IS NULL) OR "
            "(auth_issuer IS NOT NULL AND auth_subject IS NOT NULL "
            "AND auth_issuer <> '' AND auth_subject <> '')",
            name="auth_binding_is_complete",
        ),
    )

    auth_issuer: Mapped[str | None] = mapped_column(String(512), nullable=True)
    auth_subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    deactivated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

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
