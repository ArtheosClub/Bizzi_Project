"""EnterpriseObject persistence round-trip against a real database — WP13.

Requires Postgres with migrations applied — CI provides both (the backend
job runs a postgres service and `alembic upgrade head` before pytest).
Locally, `docker compose up -d postgres-test` plus `alembic upgrade head`
gives the same.

Skipped rather than failed when no database is reachable, so the suite still
runs in environments without one. The skip is deliberately loud: a green run
that silently skipped every persistence test would prove nothing.

The tests that matter most here are the ones the model tests *cannot* prove:
that the CHECK constraint and the foreign key are enforced by the database
rather than merely declared in Python.
"""

import uuid

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import EnterpriseObject, User, Workspace


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

    Keeps the test database clean without needing per-test truncation, and
    means these tests can run against a shared database safely.
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


@pytest.fixture()
def user(session):  # type: ignore[no-untyped-def]
    """A real parent row — WP16's owner_id FK backfill requires one to exist."""
    user = User()
    session.add(user)
    session.flush()
    return user


@pytest.fixture()
def workspace(session, user):  # type: ignore[no-untyped-def]
    """A real parent row — the FK under test requires one to exist."""
    workspace = Workspace(name="Test Workspace", owner_id=user.id)
    session.add(workspace)
    session.flush()
    return workspace


def test_migration_created_the_table(engine) -> None:  # type: ignore[no-untyped-def]
    """Proves `alembic upgrade head` actually ran and created the table."""
    assert "enterprise_objects" in inspect(engine).get_table_names()


def test_migration_applied_the_naming_convention(engine) -> None:  # type: ignore[no-untyped-def]
    """The convention must reach the database, not just the ORM metadata."""
    inspector = inspect(engine)

    assert (
        inspector.get_pk_constraint("enterprise_objects")["name"]
        == "pk_enterprise_objects"
    )

    fk_names = {
        fk["name"] for fk in inspector.get_foreign_keys("enterprise_objects")
    }
    assert "fk_enterprise_objects_workspace_id_workspaces" in fk_names


def test_round_trip_defaults_phase_to_active(session, workspace, user) -> None:  # type: ignore[no-untyped-def]
    """Domain Review §1a: an EnterpriseObject comes into being `active`.

    The server default is what is under test — `phase` is not passed.
    """
    obj = EnterpriseObject(
        workspace_id=workspace.id,
        type="business_request",
        owner_id=user.id,
    )
    session.add(obj)
    session.flush()
    session.refresh(obj)

    assert obj.phase == "active"
    assert obj.id is not None
    assert obj.created_at is not None
    assert obj.updated_at is not None


@pytest.mark.parametrize("phase", ["active", "archived", "superseded"])
def test_database_accepts_every_permitted_phase(session, workspace, user, phase) -> None:  # type: ignore[no-untyped-def]
    """ADR-0009 §2 — all three, enforced by the real CHECK constraint."""
    obj = EnterpriseObject(
        workspace_id=workspace.id,
        type="business_request",
        owner_id=user.id,
        phase=phase,
    )
    session.add(obj)
    session.flush()

    assert obj.phase == phase


@pytest.mark.parametrize("phase", ["draft", "deprecated", "deleted", "approved", ""])
def test_database_rejects_a_phase_outside_the_permitted_set(  # type: ignore[no-untyped-def]
    session, workspace, user, phase
) -> None:
    """The CHECK constraint must be enforced by Postgres, not just declared.

    The rejected values are the specific ones the Domain Review ruled out:
    `draft` (no approved pre-active phase), `deprecated` (orthogonal to
    Phase, D10 §5.8), `deleted` (D10 §5.1), and `approved` (a Decision
    Outcome, not an EnterpriseObject phase — Domain Review §4a).
    """
    obj = EnterpriseObject(
        workspace_id=workspace.id,
        type="business_request",
        owner_id=user.id,
        phase=phase,
    )
    session.add(obj)

    with pytest.raises(IntegrityError):
        session.flush()


def test_database_rejects_an_unknown_workspace(session, user) -> None:  # type: ignore[no-untyped-def]
    """ADR-0004 / D01, enforced by the foreign key rather than by convention.

    `owner_id` is a real user here so the only violated constraint is the
    `workspace_id` FK under test — otherwise this would pass for an
    ambiguous reason now that `owner_id` is also foreign-keyed.
    """
    obj = EnterpriseObject(
        workspace_id=uuid.uuid4(),
        type="business_request",
        owner_id=user.id,
    )
    session.add(obj)

    with pytest.raises(IntegrityError):
        session.flush()


def test_database_rejects_an_unknown_owner(session, workspace) -> None:  # type: ignore[no-untyped-def]
    """WP16's `owner_id` FK backfill, enforced by the database.

    `workspace_id` is real here for the same isolation reason as above.
    """
    obj = EnterpriseObject(
        workspace_id=workspace.id,
        type="business_request",
        owner_id=uuid.uuid4(),
    )
    session.add(obj)

    with pytest.raises(IntegrityError):
        session.flush()


def test_database_accepts_any_type_string(session, workspace, user) -> None:  # type: ignore[no-untyped-def]
    """No approved source enumerates the specializations, so none is enforced.

    Deliberately uses a value no scenario mentions: if someone later adds a
    CHECK constraint enumerating types, this fails and forces the question
    back through the Architecture Review rather than letting an invented
    domain vocabulary ship quietly.
    """
    obj = EnterpriseObject(
        workspace_id=workspace.id,
        type="a_type_no_approved_document_names",
        owner_id=user.id,
    )
    session.add(obj)
    session.flush()

    assert obj.type == "a_type_no_approved_document_names"


@pytest.mark.parametrize("missing", ["workspace_id", "type", "owner_id"])
def test_required_columns_are_rejected_when_null(session, workspace, user, missing) -> None:  # type: ignore[no-untyped-def]
    values = {
        "workspace_id": workspace.id,
        "type": "business_request",
        "owner_id": user.id,
    }
    values[missing] = None

    session.add(EnterpriseObject(**values))

    with pytest.raises(IntegrityError):
        session.flush()
