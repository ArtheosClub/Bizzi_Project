"""AgentDefinition persistence round-trip against a real database — WP14/A-10."""

import uuid

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import AgentDefinition, User, Workspace
from app.models.agent_definition import AGENT_DEFINITION_PHASES

EXPECTED_COLUMNS = {
    "id",
    "workspace_id",
    "phase",
    "owner_id",
    "created_at",
    "updated_at",
}


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
    workspace = Workspace(name="Agent Definition Test", owner_id=user.id)
    session.add(workspace)
    session.flush()
    return workspace


def test_migration_created_the_table(engine) -> None:  # type: ignore[no-untyped-def]
    assert "agent_definitions" in inspect(engine).get_table_names()


def test_migration_created_exactly_the_a10_columns(engine) -> None:  # type: ignore[no-untyped-def]
    columns = {column["name"] for column in inspect(engine).get_columns("agent_definitions")}
    assert columns == EXPECTED_COLUMNS


def test_migration_applied_the_naming_convention(engine) -> None:  # type: ignore[no-untyped-def]
    inspector = inspect(engine)
    assert (
        inspector.get_pk_constraint("agent_definitions")["name"]
        == "pk_agent_definitions"
    )
    fk_names = {
        fk["name"] for fk in inspector.get_foreign_keys("agent_definitions")
    }
    assert "fk_agent_definitions_workspace_id_workspaces" in fk_names
    assert "fk_agent_definitions_owner_id_users" in fk_names


def test_round_trip_defaults_phase_to_active_via_orm(session, workspace, user) -> None:  # type: ignore[no-untyped-def]
    agent = AgentDefinition(workspace_id=workspace.id, owner_id=user.id)
    session.add(agent)
    session.flush()
    session.refresh(agent)

    assert agent.phase == "active"
    assert agent.id is not None
    assert agent.created_at is not None
    assert agent.updated_at is not None


def test_creating_agent_definition_does_not_create_enterprise_object_row(
    session, workspace, user
) -> None:  # type: ignore[no-untyped-def]
    agent = AgentDefinition(workspace_id=workspace.id, owner_id=user.id)
    session.add(agent)
    session.flush()

    count = session.execute(
        text("SELECT count(*) FROM enterprise_objects WHERE id = :id"),
        {"id": agent.id},
    ).scalar_one()
    assert count == 0


def test_server_default_resolves_phase_to_active(session, workspace, user) -> None:  # type: ignore[no-untyped-def]
    agent_id = uuid.uuid4()
    session.execute(
        text(
            "INSERT INTO agent_definitions (id, workspace_id, owner_id) "
            "VALUES (:id, :workspace_id, :owner_id)"
        ),
        {"id": agent_id, "workspace_id": workspace.id, "owner_id": user.id},
    )
    session.flush()
    row = session.execute(
        text("SELECT phase FROM agent_definitions WHERE id = :id"),
        {"id": agent_id},
    ).one()
    assert row.phase == "active"


@pytest.mark.parametrize("phase", AGENT_DEFINITION_PHASES)
def test_database_accepts_every_permitted_phase(session, workspace, user, phase) -> None:  # type: ignore[no-untyped-def]
    agent = AgentDefinition(
        workspace_id=workspace.id,
        owner_id=user.id,
        phase=phase,
    )
    session.add(agent)
    session.flush()
    assert agent.phase == phase


@pytest.mark.parametrize("phase", ["draft", "completed", "cancelled", "", "unknown"])
def test_database_rejects_a_phase_outside_the_permitted_set(  # type: ignore[no-untyped-def]
    session, workspace, user, phase
) -> None:
    session.add(
        AgentDefinition(
            workspace_id=workspace.id,
            owner_id=user.id,
            phase=phase,
        )
    )
    with pytest.raises(IntegrityError):
        session.flush()


def test_database_rejects_an_unknown_workspace(session, user) -> None:  # type: ignore[no-untyped-def]
    session.add(AgentDefinition(workspace_id=uuid.uuid4(), owner_id=user.id))
    with pytest.raises(IntegrityError):
        session.flush()


def test_database_rejects_an_unknown_owner(session, workspace) -> None:  # type: ignore[no-untyped-def]
    session.add(AgentDefinition(workspace_id=workspace.id, owner_id=uuid.uuid4()))
    with pytest.raises(IntegrityError):
        session.flush()


def test_workspace_id_is_required(session: Session, user) -> None:  # type: ignore[no-untyped-def]
    session.add(AgentDefinition(owner_id=user.id))
    with pytest.raises(SQLAlchemyError):
        session.flush()


def test_owner_id_is_required(session: Session, workspace) -> None:  # type: ignore[no-untyped-def]
    session.add(AgentDefinition(workspace_id=workspace.id))
    with pytest.raises(SQLAlchemyError):
        session.flush()
