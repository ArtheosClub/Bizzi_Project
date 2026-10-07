"""Per-path counter evidence; fake destinations NEVER connected."""

import asyncio
import runpy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.core.actor_context import ActorContext
from app.core.authentication import VerifiedIdentity
from app.core.preproduction_guard import (
    LOCAL_TEST_POLICY,
    POLICY_KEY,
    ExecutionPolicy,
    ScopeViolationError,
    require_engine,
    require_session,
)

PATHS = [
    "identity_resolve",
    "identity_authorize",
    "audit_record",
    "audit_bootstrap",
    "actor_validation",
    "bootstrap_service",
    "bootstrap_wrapper",
    "eo_create",
    "eo_archive",
    "eo_unarchive",
    "task_create",
    "intake_service",
    "intake_handler",
    "task_repository",
    "eo_repository",
    "audit_repository",
]
CASES = [
    "disabled",
    "unknown",
    "ci_test",
    "missing_policy",
    "remote",
    "port",
    "database",
    "role",
    "query",
    "PGHOSTADDR",
]


@pytest.mark.parametrize("path", PATHS)
@pytest.mark.parametrize("case", CASES)
def test_named_path_refuses_before_query_add_flush(monkeypatch, path, case):
    from app.api.business_request_intake import create_business_request
    from app.cli.bootstrap_owner import bootstrap_owner
    from app.models import AuditRecord, EnterpriseObject, Task, User, Workspace, WorkspaceMembership
    from app.repositories import (
        audit_record_repository,
        enterprise_object_repository,
        task_repository,
    )
    from app.services.audit_service import AuditService, validate_actor
    from app.services.bootstrap_service import BootstrapService
    from app.services.business_request_intake_service import BusinessRequestIntakeService
    from app.services.enterprise_object_service import EnterpriseObjectService
    from app.services.identity_service import IdentityService
    from app.services.task_service import TaskService

    url = "postgresql+psycopg://bizzi@localhost:5433/bizzi_test"
    url = {
        "remote": url.replace("localhost", "remote"),
        "port": url.replace("5433", "5432"),
        "database": url.replace("bizzi_test", "other"),
        "role": url.replace("bizzi@", "other@"),
        "query": url + "?hostaddr=remote",
    }.get(case, url)
    engine = create_engine(url)  # construction only, NEVER connection
    connect = Mock(side_effect=AssertionError("Unexpected connection"))
    monkeypatch.setattr(engine, "connect", connect)
    db = Mock()
    db.info = {
        POLICY_KEY: ExecutionPolicy(case)
        if case in {"disabled", "unknown", "ci_test"}
        else LOCAL_TEST_POLICY
    }
    if case == "missing_policy":
        db.info = {}
    if case == "PGHOSTADDR":
        monkeypatch.setenv("PGHOSTADDR", "remote")
    db.get_bind.return_value = engine
    db.deleted = set()
    ctx = ActorContext(uuid4(), uuid4(), uuid4(), "synthetic-request")
    verifier = Mock()
    verifier.verify.return_value = VerifiedIdentity("synthetic-issuer", "synthetic-owner")
    calls = {
        "identity_resolve": lambda: IdentityService(db, verifier).resolve_actor_context(
            "synthetic", "req"
        ),
        "identity_authorize": lambda: IdentityService(db, verifier).authorize(
            ctx, ctx.workspace_id
        ),
        "actor_validation": lambda: validate_actor(db, ctx, ctx.workspace_id),
        "audit_bootstrap": lambda: AuditService.record_bootstrap(
            db, user=User(), workspace=Workspace(), membership=WorkspaceMembership()
        ),
        "bootstrap_service": lambda: BootstrapService.create_owner(
            db, identity=verifier.verify.return_value, workspace_name="synthetic"
        ),
        "bootstrap_wrapper": lambda: bootstrap_owner(
            db, token="synthetic", verifier=verifier, workspace_name="synthetic"
        ),
        "eo_create": lambda: EnterpriseObjectService.create(
            db,
            workspace_id=ctx.workspace_id,
            owner_id=ctx.actor_id,
            type="business_request",
            actor_context=ctx,
        ),
        "eo_archive": lambda: EnterpriseObjectService.archive(
            db, workspace_id=ctx.workspace_id, object_id=uuid4(), actor_context=ctx
        ),
        "eo_unarchive": lambda: EnterpriseObjectService.unarchive(
            db, workspace_id=ctx.workspace_id, object_id=uuid4(), actor_context=ctx
        ),
        "task_create": lambda: TaskService.create(
            db, workspace_id=ctx.workspace_id, actor_context=ctx
        ),
        "intake_service": lambda: BusinessRequestIntakeService.create(db, actor_context=ctx),
        "task_repository": lambda: task_repository.add(db, Task()),
        "eo_repository": lambda: enterprise_object_repository.add(db, EnterpriseObject()),
        "audit_repository": lambda: audit_record_repository.add(db, AuditRecord()),
    }
    if path == "audit_record":
        import app.services.audit_service as audit_module

        subject = Task(id=uuid4(), workspace_id=ctx.workspace_id, phase="active")
        # Instrument a already-loaded subject to reach the pre-query actor gate.
        monkeypatch.setattr(
            audit_module, "sa_inspect", lambda obj: SimpleNamespace(deleted=False, persistent=True)
        )
        monkeypatch.setattr(audit_module, "object_session", lambda obj: db)
        calls[path] = lambda: AuditService.record(
            db,
            subject=subject,
            action="task.created",
            content={"phase": [None, "active"]},
            actor_context=ctx,
        )
    if path == "intake_handler":
        request = Mock()
        request.headers = {"authorization": "Bearer synthetic"}
        calls[path] = lambda: asyncio.run(create_business_request(request, db, verifier))
    with pytest.raises(ScopeViolationError):
        calls[path]()
    for method in ("execute", "scalar", "scalars", "query", "add", "add_all", "flush"):
        getattr(db, method).assert_not_called()
    connect.assert_not_called()
    engine.dispose()


@pytest.mark.parametrize("case", ["disabled", "ci_test", "unknown", "remote", "PGHOSTADDR"])
def test_provider_and_external_fixture_refuse_before_connection(monkeypatch, case):
    import sqlalchemy

    import app.db.session as provider

    policy = (
        ExecutionPolicy(case) if case in {"disabled", "ci_test", "unknown"} else LOCAL_TEST_POLICY
    )
    url = "postgresql+psycopg://bizzi@localhost:5433/bizzi_test"
    if case == "remote":
        url = url.replace("localhost", "remote")
    if case == "PGHOSTADDR":
        monkeypatch.setenv("PGHOSTADDR", "remote")
    monkeypatch.setattr(provider, "get_settings", lambda: SimpleNamespace(database_url=url))
    constructor = Mock(side_effect=AssertionError("Must refuse before Engine creation"))
    monkeypatch.setattr(provider, "create_engine", constructor)
    with pytest.raises(ScopeViolationError):
        next(provider.get_db_for_policy(policy))
    constructor.assert_not_called()
    engine = sqlalchemy.create_engine(url)
    connect = Mock(side_effect=AssertionError("Must not connect"))
    monkeypatch.setattr(engine, "connect", connect)
    with pytest.raises(ScopeViolationError):
        require_engine(engine, policy)
    connect.assert_not_called()
    engine.dispose()


@pytest.mark.parametrize("case", ["remote", "PGHOSTADDR", "disabled", "ci_test"])
def test_collection_gate_before_module_engine_construction(monkeypatch, case):
    import sqlalchemy

    import app.core.preproduction_guard as guard

    if case == "remote":
        monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://bizzi@remote:5433/bizzi_test")
    if case == "PGHOSTADDR":
        monkeypatch.setenv("PGHOSTADDR", "remote")
    if case in {"disabled", "ci_test"}:
        monkeypatch.setattr(guard, "LOCAL_TEST_POLICY", ExecutionPolicy(case))
    factory = Mock(side_effect=AssertionError("Collection must refuse first"))
    monkeypatch.setattr(sqlalchemy, "create_engine", factory)
    with pytest.raises(ScopeViolationError):
        runpy.run_path(str(Path(__file__).with_name("conftest.py")))
    factory.assert_not_called()


@pytest.mark.parametrize("mode", ["online", "offline"])
@pytest.mark.parametrize("profile", ["disabled", "unknown", "ci_test"])
def test_alembic_refusal_before_engine_or_sql_generation(monkeypatch, mode, profile):
    import alembic.context as context
    import sqlalchemy

    import app.core.config as config_module

    config = SimpleNamespace(config_file_name=None, set_main_option=Mock())
    monkeypatch.setattr(context, "config", config, raising=False)
    monkeypatch.setattr(context, "is_offline_mode", lambda: mode == "offline", raising=False)
    configure = Mock()
    monkeypatch.setattr(context, "configure", configure, raising=False)
    factory = Mock()
    monkeypatch.setattr(sqlalchemy, "engine_from_config", factory)
    monkeypatch.setattr(
        config_module,
        "get_settings",
        lambda: SimpleNamespace(
            database_url="postgresql+psycopg://bizzi@localhost:5433/bizzi_test",
            synthetic_execution_profile=profile,
        ),
    )
    with pytest.raises(ScopeViolationError):
        runpy.run_path(str(Path(__file__).parents[1] / "alembic/env.py"))
    factory.assert_not_called()
    configure.assert_not_called()
    config.set_main_option.assert_not_called()


def test_actual_connection_bound_session_refuses_before_mutation(identity_db, monkeypatch):
    # Connection was already admitted/opened by fixture. Claim BEFORE QUERY, not BEFORE CONNECTION.
    identity_db.info[POLICY_KEY] = ExecutionPolicy("disabled")
    execute = Mock()
    monkeypatch.setattr(identity_db, "execute", execute)
    with pytest.raises(ScopeViolationError):
        require_session(identity_db)
    execute.assert_not_called()


def test_default_app_absent_route_and_health():
    from app.main import app

    with TestClient(app) as client:
        response = client.post("/business-requests", json={})
        assert response.status_code == 404 and response.json()["error"]["code"] == "not_found"
        assert response.headers["X-Request-Id"]
        assert client.get("/health").status_code == 200


@pytest.mark.parametrize("mode", ["online", "offline"])
def test_alembic_checks_resolved_engine_or_offline_url(monkeypatch, mode):
    import alembic.context as context
    import sqlalchemy

    import app.core.config as config_module

    config = Mock()
    config.config_file_name = None
    config.config_ini_section = "alembic"
    config.get_section.return_value = {}
    config.get_main_option.return_value = "postgresql+psycopg://bizzi@remote:5433/bizzi_test"
    monkeypatch.setattr(context, "config", config, raising=False)
    monkeypatch.setattr(context, "is_offline_mode", lambda: mode == "offline", raising=False)
    configure = Mock()
    monkeypatch.setattr(context, "configure", configure, raising=False)
    monkeypatch.setattr(
        config_module,
        "get_settings",
        lambda: SimpleNamespace(
            database_url="postgresql+psycopg://bizzi@localhost:5433/bizzi_test",
            synthetic_execution_profile="local_test",
        ),
    )
    wrong_engine = sqlalchemy.create_engine("postgresql+psycopg://bizzi@remote:5433/bizzi_test")
    connect = Mock(side_effect=AssertionError("wrong destination must not connect"))
    monkeypatch.setattr(wrong_engine, "connect", connect)
    monkeypatch.setattr(sqlalchemy, "engine_from_config", lambda *a, **k: wrong_engine)
    with pytest.raises(ScopeViolationError):
        runpy.run_path(str(Path(__file__).parents[1] / "alembic/env.py"))
    connect.assert_not_called()
    configure.assert_not_called()
    wrong_engine.dispose()
