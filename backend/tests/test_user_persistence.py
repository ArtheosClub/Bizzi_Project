"""User persistence round-trip against a real database — WP16 Amendment A-03.

Requires Postgres with migrations applied — CI provides both (the backend
job runs a postgres service and `alembic upgrade head` before pytest).
Locally, `docker compose up -d postgres-test` plus `alembic upgrade head`
gives the same.

Skipped rather than failed when no database is reachable, so the suite
still runs in environments without one.
"""

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import User


@pytest.fixture(scope="module")
def engine():  # type: ignore[no-untyped-def]
    engine = create_engine(get_settings().database_url, pool_pre_ping=True)
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        pytest.skip(f"no database reachable: {exc.__class__.__name__}")
    return engine


@pytest.fixture()
def session(engine):  # type: ignore[no-untyped-def]
    """Each test runs in a transaction that is always rolled back."""
    connection = engine.connect()
    transaction = connection.begin()
    db = Session(bind=connection)
    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()


def test_migration_created_the_table(engine) -> None:  # type: ignore[no-untyped-def]
    """Proves `alembic upgrade head` actually ran and created the table."""
    assert "users" in inspect(engine).get_table_names()


def test_migration_applied_the_naming_convention(engine) -> None:  # type: ignore[no-untyped-def]
    """The convention must reach real DDL, not just ORM metadata."""
    inspector = inspect(engine)
    assert inspector.get_pk_constraint("users")["name"] == "pk_users"


def test_user_round_trip(session: Session) -> None:
    """Create, flush, read back — bare identity only."""
    user = User()

    session.add(user)
    session.flush()

    assert user.id is not None
    assert user.created_at is not None
    assert user.updated_at is not None

    fetched = session.get(User, user.id)
    assert fetched is not None
    assert fetched.id == user.id
