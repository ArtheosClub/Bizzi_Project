"""Read-only identity lookup; User is the ADR-0004 unscoped exception."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_by_auth_identity(db: Session, issuer: str, subject: str) -> User | None:
    return db.scalar(
        select(User)
        .execution_options(populate_existing=True)
        .where(User.auth_issuer == issuer, User.auth_subject == subject)
    )


def get_by_id(db: Session, user_id: UUID) -> User | None:
    return db.scalar(
        select(User).execution_options(populate_existing=True).where(User.id == user_id)
    )


def create_for_bootstrap(db: Session, *, issuer: str, subject: str) -> User:
    from uuid import uuid4

    obj = User(id=uuid4(), auth_issuer=issuer, auth_subject=subject)
    db.add(obj)
    return obj
