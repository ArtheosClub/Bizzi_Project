"""WorkspaceMembership persistence round-trip against a real database.

WP16 Amendment A-03. Requires Postgres with migrations applied — CI
provides both (the backend job runs a postgres service and `alembic
upgrade head` before pytest). Locally, `docker compose up -d
postgres-test` plus `alembic upgrade head` gives the same.

Skipped rather than failed when no database is reachable. The tests that
matter most here are the ones the model tests *cannot* prove: that the
CHECK constraint, both foreign keys, and the UNIQUE constraint are
enforced by the database rather than merely declared in Python.
"""

import uuid

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import User, Workspace, WorkspaceMembership


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


@pytest.fixture()
def user(session):  # type: ignore[no-untyped-def]
    user = User()
    session.add(user)
    session.flush()
    return user


@pytest.fixture()
def workspace(session, user):  # type: ignore[no-untyped-def]
    """Owned by the same `user` fixture, so the two FKs under test agree."""
    workspace = Workspace(name="Test Workspace", owner_id=user.id)
    session.add(workspace)
    session.flush()
    return workspace


def test_migration_created_the_table(engine) -> None:  # type: ignore[no-untyped-def]
    """Proves `alembic upgrade head` actually ran and created the table."""
    assert "workspace_memberships" in inspect(engine).get_table_names()


def test_migration_applied_the_naming_convention(engine) -> None:  # type: ignore[no-untyped-def]
    """The convention must reach real DDL, not just ORM metadata."""
    inspector = inspect(engine)

    assert (
        inspector.get_pk_constraint("workspace_memberships")["name"]
        == "pk_workspace_memberships"
    )

    fk_names = {
        fk["name"] for fk in inspector.get_foreign_keys("workspace_memberships")
    }
    assert "fk_workspace_memberships_workspace_id_workspaces" in fk_names
    assert "fk_workspace_memberships_user_id_users" in fk_names


def test_round_trip(session, workspace, user) -> None:  # type: ignore[no-untyped-def]
    membership = WorkspaceMembership(
        workspace_id=workspace.id,
        user_id=user.id,
        role="owner",
    )
    session.add(membership)
    session.flush()
    session.refresh(membership)

    assert membership.id is not None
    assert membership.created_at is not None

    fetched = session.get(WorkspaceMembership, membership.id)
    assert fetched is not None
    assert fetched.role == "owner"


def test_database_accepts_the_owner_role(session, workspace, user) -> None:  # type: ignore[no-untyped-def]
    """ADR-0010's single authorized value, enforced by the real CHECK."""
    membership = WorkspaceMembership(
        workspace_id=workspace.id, user_id=user.id, role="owner"
    )
    session.add(membership)
    session.flush()

    assert membership.role == "owner"


@pytest.mark.parametrize("role", ["reviewer", "approver", "admin", ""])
def test_database_rejects_a_role_outside_the_permitted_set(  # type: ignore[no-untyped-def]
    session, workspace, user, role
) -> None:
    """GC-004 is unapproved — no second role may appear until it is."""
    membership = WorkspaceMembership(
        workspace_id=workspace.id, user_id=user.id, role=role
    )
    session.add(membership)

    with pytest.raises(IntegrityError):
        session.flush()


def test_database_rejects_an_unknown_workspace(session, user) -> None:  # type: ignore[no-untyped-def]
    membership = WorkspaceMembership(
        workspace_id=uuid.uuid4(), user_id=user.id, role="owner"
    )
    session.add(membership)

    with pytest.raises(IntegrityError):
        session.flush()


def test_database_rejects_an_unknown_user(session, workspace) -> None:  # type: ignore[no-untyped-def]
    membership = WorkspaceMembership(
        workspace_id=workspace.id, user_id=uuid.uuid4(), role="owner"
    )
    session.add(membership)

    with pytest.raises(IntegrityError):
        session.flush()


def test_database_rejects_a_duplicate_workspace_user_pair(  # type: ignore[no-untyped-def]
    session, workspace, user
) -> None:
    """UNIQUE(workspace_id, user_id) — one membership row per pair."""
    session.add(
        WorkspaceMembership(workspace_id=workspace.id, user_id=user.id, role="owner")
    )
    session.flush()

    session.add(
        WorkspaceMembership(workspace_id=workspace.id, user_id=user.id, role="owner")
    )

    with pytest.raises(IntegrityError):
        session.flush()


@pytest.mark.parametrize("missing", ["workspace_id", "user_id", "role"])
def test_required_columns_are_rejected_when_null(  # type: ignore[no-untyped-def]
    session, workspace, user, missing
) -> None:
    values = {
        "workspace_id": workspace.id,
        "user_id": user.id,
        "role": "owner",
    }
    values[missing] = None

    session.add(WorkspaceMembership(**values))

    with pytest.raises(IntegrityError):
        session.flush()
