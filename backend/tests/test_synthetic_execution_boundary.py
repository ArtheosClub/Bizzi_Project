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

    import app.core.config as config_module

    if case == "remote":
        monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://bizzi@remote:5433/bizzi_test")
    if case == "PGHOSTADDR":
        monkeypatch.setenv("PGHOSTADDR", "remote")
    if case in {"disabled", "ci_test"}:
        settings = config_module.get_settings()
        monkeypatch.setenv("SYNTHETIC_EXECUTION_PROFILE", case)
        monkeypatch.setattr(
            config_module,
            "get_settings",
            lambda: SimpleNamespace(
                database_url=settings.database_url,
                synthetic_execution_profile=case,
            ),
        )
        # ci_test must have missing context, never an accidentally inherited valid job.
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
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


@pytest.mark.parametrize("case", ["port", "database", "role", "remote", "query", "override"])
def test_ci_bind_refuses_before_sql_on_mock(monkeypatch, case):
    from app.core.preproduction_guard import PG_OVERRIDES, resolve_policy
    from tests.test_preproduction_guard import CI_NAMES, CI_VALUES, install_ci_environment

    install_ci_environment(monkeypatch, dict(zip(CI_NAMES, CI_VALUES, strict=True)))
    policy = resolve_policy("ci_test")
    urls = {
        "port": "postgresql+psycopg://bizzi@localhost:5433/bizzi_test",
        "database": "postgresql+psycopg://bizzi@localhost:5432/bizzi_dev",
        "role": "postgresql+psycopg://other@localhost:5432/bizzi_test",
        "remote": "postgresql+psycopg://bizzi@remote:5432/bizzi_test",
        "query": "postgresql+psycopg://bizzi@localhost:5432/bizzi_test?host=remote",
        "override": "postgresql+psycopg://bizzi@localhost:5432/bizzi_test",
    }
    db = Mock()
    db.info = {POLICY_KEY: policy}
    engine = create_engine(urls[case])
    db.get_bind.return_value = engine
    if case == "override":
        monkeypatch.setenv(PG_OVERRIDES[0], "unadmitted")
    with pytest.raises(ScopeViolationError):
        require_session(db)
    db.query.assert_not_called()
    db.execute.assert_not_called()
    db.add.assert_not_called()
    db.flush.assert_not_called()
    engine.dispose()


def test_compose_refuses_business_factory_provider_and_session(monkeypatch):
    import app.db.session as provider
    from app.core.preproduction_guard import resolve_policy
    from app.main import create_application
    from tests.test_preproduction_guard import CI_NAMES, CI_VALUES, install_ci_environment

    env = dict(zip(CI_NAMES, CI_VALUES, strict=True))
    env["GITHUB_JOB"] = "compose-e2e"
    install_ci_environment(monkeypatch, env)
    policy = resolve_policy("ci_compose")
    constructor = Mock(side_effect=AssertionError("Engine creation forbidden"))
    monkeypatch.setattr(provider, "create_engine", constructor)
    monkeypatch.setattr(provider, "get_settings", lambda: SimpleNamespace(
        database_url="postgresql+psycopg://bizzi@postgres-test:5432/bizzi_test"))
    with pytest.raises(ScopeViolationError):
        next(provider.get_db_for_policy(policy))
    constructor.assert_not_called()
    with pytest.raises(ScopeViolationError):
        create_application(policy)
    db = Mock()
    db.info = {POLICY_KEY: policy}
    with pytest.raises(ScopeViolationError):
        require_session(db)
    db.get_bind.assert_not_called()
    for name in ("execute", "query", "scalar", "scalars", "add", "flush", "commit", "delete"):
        getattr(db, name).assert_not_called()


# Fixed bounded corpus: any changed/new source must be reviewed, never silently classified.
CORPUS_SHA256 = {
    'backend/app/api/__init__.py': (
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    ),
    'backend/app/api/business_request_intake.py': (
        '7b15ca5d2a099f7561d051b5be3d8d886ecb586478fedaf86ca63a12d83950a4'
    ),
    'backend/app/api/health.py': (
        'fcc29735819fec8288d87103525ea5b9c3c07683b444b4716344ddb599bff4b3'
    ),
    'backend/app/cli/__init__.py': (
        'f4c0120ab70daf2f266725b1b98dc1711ed0bf9934a128408d3f5cd4a664909d'
    ),
    'backend/app/cli/bootstrap_owner.py': (
        'b3363e919907bf7e76a4b9c54f337cdfc597065d7b890983970125d7ee941702'
    ),
    'backend/app/repositories/__init__.py': (
        'a7f4ce28f14a68fbd25223aa964da9c5c36d7baeb669ec01caa424f6598c7dbd'
    ),
    'backend/app/repositories/audit_record_repository.py': (
        '1bedd743606efca51dafdec797af9dc338de00f18fa3df0d6af255b59396b00e'
    ),
    'backend/app/repositories/enterprise_object_repository.py': (
        '9870d0bd3fc7ea78eb360e7c881022a3a369f803749723f4fcb7bd2ffea2776e'
    ),
    'backend/app/repositories/task_repository.py': (
        '0000a67b089f3f1a4e7b970582a413120b85b08204b207714d0f1f7d239d49c7'
    ),
    'backend/app/repositories/user_repository.py': (
        '780ccdf2fdcd3bb912aa87f89ea3364ee5c0336fe775839b63949bd9d6c53007'
    ),
    'backend/app/repositories/workspace_membership_repository.py': (
        'c2e24c69c136abbecaa319c82e6aeb61c973bc2389f0352099908465241ec2da'
    ),
    'backend/app/repositories/workspace_repository.py': (
        '12836c803bca4942ba2644d3519c2f9f4981dee1a45ffc5b998bdad39ffc8678'
    ),
    'backend/app/services/__init__.py': (
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    ),
    'backend/app/services/audit_actions.py': (
        '4433d0eca5b6a23dc02da490fb704a7c14db711713f64b30b15ad5fe2a3a9c22'
    ),
    'backend/app/services/audit_service.py': (
        'b6071ede934df42423bd0e48a4b4eb23cd264e3bfaa455633b10c072606957d6'
    ),
    'backend/app/services/bootstrap_service.py': (
        'fcb2aa57ab322e3cc6f23accbedd7da6585f4ff66676a1764fbe4315b02acfb4'
    ),
    'backend/app/services/business_request_intake_service.py': (
        'd4c819325ab33576a2e995cd73294b964df6fdbd836d7bd170de46c6c1e15434'
    ),
    'backend/app/services/enterprise_object_service.py': (
        'a7a367ed10341f0c5f730bb37711b529091efbe242142358ba16476cc384cf9b'
    ),
    'backend/app/services/identity_service.py': (
        '18a5c2ede20bef2290caa7be6e68b95882d3537029e9d4c5aff5dc7aeabc7fa6'
    ),
    'backend/app/services/task_service.py': (
        '7171a7d5d5cbd432e1f73a6da3ba2356c4687a04c767703b9be15a77a4c1e7e5'
    ),
}
DELEGATED_CALLERS = {
    "user_repository.get_by_auth_identity": {
        "identity_service.IdentityService.resolve_actor_context"
    },
    "user_repository.get_by_id": {"identity_service.IdentityService.authorize"},
    "user_repository.create_for_bootstrap": {"bootstrap_service.BootstrapService.create_owner"},
    "workspace_repository.create_for_bootstrap": {
        "bootstrap_service.BootstrapService.create_owner"
    },
    "workspace_membership_repository.find_for_identity": {
        "identity_service.IdentityService.resolve_actor_context",
        "identity_service.IdentityService.authorize"
    },
    "workspace_membership_repository.create_for_bootstrap": {
        "bootstrap_service.BootstrapService.create_owner"},
    "enterprise_object_repository.get_by_id": {"enterprise_object_service._transition"},
    "enterprise_object_repository.list_by_workspace": set(),
    "audit_record_repository.list_by_workspace": set(),
}


def test_current_business_paths_reach_require_session():
    import ast
    import hashlib
    import json
    import os

    root = Path(__file__).parents[2]
    files = {p.relative_to(root).as_posix(): p for folder in
             ("services", "repositories", "api", "cli")
             for p in (root / "backend/app" / folder).rglob("*.py")}
    assert set(files) == set(CORPUS_SHA256), "new/missing static module requires review"
    observed = {key: set() for key in DELEGATED_CALLERS}
    evidence = []
    for name, path in files.items():
        source = path.read_bytes()
        assert hashlib.sha256(source).hexdigest() == CORPUS_SHA256[name], name
        tree = ast.parse(source)
        aliases = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    aliases[alias.asname or alias.name] = alias.name
        parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
        functions = [node for node in ast.walk(tree)
                     if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
        # The pins freeze all other service ordering/delegation; enumerate the unguarded
        # repository call sites explicitly rather than claiming a general Python sandbox.
        for function in functions:
            owner = parents.get(function)
            label = path.stem + "." + (
                owner.name + "." if isinstance(owner, ast.ClassDef) else "") + function.name
            guard_lines = [node.lineno for node in ast.walk(function)
                           if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                           and aliases.get(node.func.id, node.func.id) == "require_session"]
            for node in ast.walk(function):
                if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                    continue
                target = node.func
                if not isinstance(target.value, ast.Name):
                    continue
                key = aliases.get(target.value.id, target.value.id) + "." + target.attr
                if key not in DELEGATED_CALLERS:
                    continue
                observed[key].add(label)
                # In these pinned callers, require_session is a standalone preceding
                # statement. Check ancestor blocks, not merely textual line numbers.
                guards = [statement for statement in function.body
                          if isinstance(statement, ast.Expr)
                          and isinstance(statement.value, ast.Call)
                          and isinstance(statement.value.func, ast.Name)
                          and aliases.get(statement.value.func.id, statement.value.func.id)
                          == "require_session"]
                assert any(g.lineno < node.lineno for g in guards), (label, key)
                assert guard_lines
                evidence.append({"caller": label, "target": key,
                                 "guard_line": min(guard_lines), "call_line": node.lineno})
    assert observed == DELEGATED_CALLERS
    payload = {"scope": "bounded application delegation; direct repository entry excluded",
               "pins": CORPUS_SHA256, "delegated_calls": evidence,
               "test_only_outside_certification": [
                   key for key, value in observed.items() if not value
               ],
               "dynamic_external": "UNKNOWN", "non_session": [
                   "services/__init__.py", "services/audit_actions.py",
                   "repositories/__init__.py", "api/__init__.py", "cli/__init__.py",
                   "api/health.py"]}
    (Path(os.environ["BIZZI_EVIDENCE_DIR"]) / "STATIC_BUSINESS_PATH_INVENTORY.json").write_text(
        json.dumps(payload, indent=2) + "\n")
