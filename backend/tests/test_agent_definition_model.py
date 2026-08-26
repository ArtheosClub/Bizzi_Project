"""AgentDefinition schema tests — WP14 / Amendment A-10."""

from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import CheckConstraint

from app.db.base import Base
from app.models import AgentDefinition
from app.models.agent_definition import AGENT_DEFINITION_PHASES

AGENT_DEFINITION_REVISION = "a4d9c2e7b1f6"
TASK_REVISION = "f7c3a92e1d5b"
ALEMBIC_INI = Path(__file__).resolve().parent.parent / "alembic.ini"


def test_agent_definition_is_registered_on_base_metadata() -> None:
    assert "agent_definitions" in Base.metadata.tables


def test_agent_definition_has_exactly_the_a10_columns() -> None:
    assert set(AgentDefinition.__table__.columns.keys()) == {
        "id",
        "workspace_id",
        "phase",
        "owner_id",
        "created_at",
        "updated_at",
    }


def test_runtime_and_configuration_fields_are_absent() -> None:
    columns = AgentDefinition.__table__.columns.keys()
    for excluded in (
        "type",
        "name",
        "description",
        "role",
        "status",
        "capabilities",
        "permissions",
        "provider_id",
        "model_id",
        "prompt",
        "config",
        "runtime_session_id",
        "created_by",
    ):
        assert excluded not in columns


def test_phase_permits_exactly_three_values() -> None:
    assert AGENT_DEFINITION_PHASES == (
        "active",
        "archived",
        "superseded",
    )


def test_phase_has_a_check_constraint_naming_those_values() -> None:
    checks = [
        c
        for c in AgentDefinition.__table__.constraints
        if isinstance(c, CheckConstraint)
    ]
    assert len(checks) == 1
    condition = str(checks[0].sqltext)
    for phase in AGENT_DEFINITION_PHASES:
        assert f"'{phase}'" in condition


def test_phase_defaults_to_active() -> None:
    phase = AgentDefinition.__table__.columns["phase"]
    assert phase.server_default is not None
    assert "active" in str(phase.server_default.arg)
    assert phase.default is not None
    assert phase.default.arg == "active"


def test_workspace_id_is_required_indexed_and_a_real_foreign_key() -> None:
    workspace_id = AgentDefinition.__table__.columns["workspace_id"]
    assert workspace_id.nullable is False
    assert {fk.target_fullname for fk in workspace_id.foreign_keys} == {
        "workspaces.id"
    }
    assert any(
        list(index.columns) == [workspace_id]
        for index in AgentDefinition.__table__.indexes
    )


def test_owner_id_is_required_indexed_and_a_real_foreign_key() -> None:
    owner_id = AgentDefinition.__table__.columns["owner_id"]
    assert owner_id.nullable is False
    assert {fk.target_fullname for fk in owner_id.foreign_keys} == {"users.id"}
    assert any(
        list(index.columns) == [owner_id]
        for index in AgentDefinition.__table__.indexes
    )


def test_required_columns_are_not_nullable() -> None:
    for name in (
        "id",
        "workspace_id",
        "phase",
        "owner_id",
        "created_at",
        "updated_at",
    ):
        assert AgentDefinition.__table__.columns[name].nullable is False


def test_timestamps_have_server_defaults() -> None:
    for name in ("created_at", "updated_at"):
        assert AgentDefinition.__table__.columns[name].server_default is not None


def test_constraints_use_the_naming_convention() -> None:
    table = AgentDefinition.__table__
    assert table.primary_key.name == "pk_agent_definitions"

    checks = [c for c in table.constraints if isinstance(c, CheckConstraint)]
    assert checks[0].name == "ck_agent_definitions_phase_is_known"

    workspace_fk = list(table.columns["workspace_id"].foreign_keys)[0]
    assert (
        workspace_fk.constraint.name
        == "fk_agent_definitions_workspace_id_workspaces"
    )

    owner_fk = list(table.columns["owner_id"].foreign_keys)[0]
    assert owner_fk.constraint.name == "fk_agent_definitions_owner_id_users"


def test_migration_is_wired_into_the_revision_chain() -> None:
    script = ScriptDirectory.from_config(Config(str(ALEMBIC_INI)))
    assert script.get_heads() == [AGENT_DEFINITION_REVISION]
    revision = script.get_revision(AGENT_DEFINITION_REVISION)
    assert revision.down_revision == TASK_REVISION
