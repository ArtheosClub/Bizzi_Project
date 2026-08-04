"""Task persistence round-trip against a real database — WP15, A-04.

Requires Postgres with migrations applied — CI provides both (the backend
job runs a postgres service and `alembic upgrade head` before pytest).
Locally, `docker compose up -d postgres-test` plus `alembic upgrade head`
gives the same.

Skipped rather than failed when no database is reachable. The tests that
matter most here are the ones the model tests *cannot* prove: that the
CHECK constraint and both foreign keys are enforced by the database
rather than merely declared in Python, and that `server_default` (not
just the Python-level `default`) actually resolves `phase` to `active`
on a row Postgres itself defaults, not one the ORM defaulted first.
"""

import uuid

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import EnterpriseObject, Task, User, Workspace
from app.models.task import TASK_PHASES


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
    workspace = Workspace(name="Test Workspace", owner_id=user.id)
    session.add(workspace)
    session.flush()
    return workspace


@pytest.fixture()
def enterprise_object(session, workspace, user):  # type: ignore[no-untyped-def]
    """A real parent row for `source_object_id` — the FK under test needs one."""
    obj = EnterpriseObject(
        workspace_id=workspace.id,
        type="business_request",
        owner_id=user.id,
    )
    session.add(obj)
    session.flush()
    return obj


def test_migration_created_the_table(engine) -> None:  # type: ignore[no-untyped-def]
    """Proves `alembic upgrade head` actually ran and created the table."""
    assert "tasks" in inspect(engine).get_table_names()


def test_migration_applied_the_naming_convention(engine) -> None:  # type: ignore[no-untyped-def]
    """The convention must reach real DDL, not just ORM metadata."""
    inspector = inspect(engine)

    assert inspector.get_pk_constraint("tasks")["name"] == "pk_tasks"

    fk_names = {fk["name"] for fk in inspector.get_foreign_keys("tasks")}
    assert "fk_tasks_workspace_id_workspaces" in fk_names
    assert "fk_tasks_source_object_id_enterprise_objects" in fk_names


def test_round_trip_defaults_phase_to_active_via_orm(session, workspace) -> None:  # type: ignore[no-untyped-def]
    """The Python-level `default` — `phase` is not passed."""
    task = Task(workspace_id=workspace.id)
    session.add(task)
    session.flush()
    session.refresh(task)

    assert task.phase == "active"
    assert task.id is not None
    assert task.created_at is not None
    assert task.updated_at is not None
    assert task.source_object_id is None


def test_server_default_resolves_phase_to_active(session, workspace) -> None:  # type: ignore[no-untyped-def]
    """The `server_default`, proven by a direct INSERT bypassing the ORM default.

    An ORM-level round-trip alone would pass even if `server_default`
    were silently missing from the migration — the Python `default`
    would mask its absence. This inserts via raw SQL, naming no `phase`
    value at all, so only the database's own default can produce one.
    """
    task_id = uuid.uuid4()
    session.execute(
        text(
            "INSERT INTO tasks (id, workspace_id) VALUES (:id, :workspace_id)"
        ),
        {"id": task_id, "workspace_id": workspace.id},
    )
    session.flush()

    row = session.execute(
        text("SELECT phase FROM tasks WHERE id = :id"), {"id": task_id}
    ).one()
    assert row.phase == "active"


@pytest.mark.parametrize("phase", TASK_PHASES)
def test_database_accepts_every_permitted_phase(session, workspace, phase) -> None:  # type: ignore[no-untyped-def]
    """D10 §6/§8 Invariant 6 — all five, enforced by the real CHECK constraint."""
    task = Task(workspace_id=workspace.id, phase=phase)
    session.add(task)
    session.flush()

    assert task.phase == phase


@pytest.mark.parametrize("phase", ["draft", "in_progress", "blocked", "rework", ""])
def test_database_rejects_a_phase_outside_the_permitted_set(  # type: ignore[no-untyped-def]
    session, workspace, phase
) -> None:
    """The CHECK constraint enforces the value domain — not the transition
    graph. This test proves rejection of unknown *values*; it does not
    and cannot prove rejection of a disallowed *transition* between two
    permitted values, since a CHECK has no access to a row's prior state.
    """
    task = Task(workspace_id=workspace.id, phase=phase)
    session.add(task)

    with pytest.raises(IntegrityError):
        session.flush()


def test_database_rejects_an_unknown_workspace(session) -> None:  # type: ignore[no-untyped-def]
    """ADR-0004 / D01, enforced by the foreign key."""
    task = Task(workspace_id=uuid.uuid4())
    session.add(task)

    with pytest.raises(IntegrityError):
        session.flush()


def test_source_object_id_is_optional(session, workspace) -> None:  # type: ignore[no-untyped-def]
    """D09 R9's cardinality includes zero — a Task with no reference is valid."""
    task = Task(workspace_id=workspace.id)
    session.add(task)
    session.flush()

    assert task.source_object_id is None


def test_database_accepts_a_real_source_object(  # type: ignore[no-untyped-def]
    session, workspace, enterprise_object
) -> None:
    task = Task(workspace_id=workspace.id, source_object_id=enterprise_object.id)
    session.add(task)
    session.flush()

    assert task.source_object_id == enterprise_object.id


def test_database_rejects_an_unknown_source_object(session, workspace) -> None:  # type: ignore[no-untyped-def]
    """The `source_object_id` FK, enforced by the database."""
    task = Task(workspace_id=workspace.id, source_object_id=uuid.uuid4())
    session.add(task)

    with pytest.raises(IntegrityError):
        session.flush()


def test_workspace_id_is_required(session: Session) -> None:
    session.add(Task())

    with pytest.raises(SQLAlchemyError):
        session.flush()
