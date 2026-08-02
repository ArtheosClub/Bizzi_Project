"""Workspace persistence round-trip against a real database.

Requires Postgres with migrations applied — CI provides both (the backend
job runs a postgres service and `alembic upgrade head` before pytest).
Locally, `docker compose up -d postgres-test` plus `alembic upgrade head`
gives the same.

Skipped rather than failed when no database is reachable, so the suite
still runs in environments without one. The skip is deliberately loud:
a green run that silently skipped its only persistence test would prove
nothing, so the reason is reported.
"""

import uuid

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Workspace


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
    """Each test runs in a transaction that is always rolled back.

    Keeps the test database clean without needing per-test truncation,
    and means these tests can run against a shared database safely.
    """
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
    assert "workspaces" in inspect(engine).get_table_names()


def test_migration_applied_the_naming_convention(engine) -> None:  # type: ignore[no-untyped-def]
    """The convention must reach real DDL, not just ORM metadata."""
    inspector = inspect(engine)
    assert inspector.get_pk_constraint("workspaces")["name"] == "pk_workspaces"
    index_names = {i["name"] for i in inspector.get_indexes("workspaces")}
    assert "ix_workspaces_owner_id" in index_names


def test_workspace_round_trip(session: Session) -> None:
    """Create, flush, read back — the WP12a acceptance criterion."""
    owner_id = uuid.uuid4()
    workspace = Workspace(name="Acme Consulting", owner_id=owner_id)

    session.add(workspace)
    session.flush()

    assert workspace.id is not None
    assert workspace.created_at is not None
    assert workspace.updated_at is not None

    fetched = session.get(Workspace, workspace.id)
    assert fetched is not None
    assert fetched.name == "Acme Consulting"
    assert fetched.owner_id == owner_id


def test_name_is_required(session: Session) -> None:
    """Negative case — NOT NULL is enforced by the database, not just Python."""
    session.add(Workspace(owner_id=uuid.uuid4()))

    with pytest.raises(SQLAlchemyError):
        session.flush()


def test_owner_id_is_required(session: Session) -> None:
    session.add(Workspace(name="No Owner"))

    with pytest.raises(SQLAlchemyError):
        session.flush()
