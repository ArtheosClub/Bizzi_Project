"""A-12 structural contract and unit-level rejection checks (no database)."""

import ast
import inspect
import uuid
from pathlib import Path
from typing import get_type_hints
from unittest.mock import Mock

import pytest
from sqlalchemy.dialects import postgresql

from app.models.enterprise_object import EnterpriseObject
from app.repositories import enterprise_object_repository as repository
from app.services.audit_service import AuditService
from app.services.enterprise_object_service import EnterpriseObjectService

APP = Path(__file__).resolve().parents[1] / "app"
MODULES = (
    APP / "services/enterprise_object_service.py",
    APP / "repositories/enterprise_object_repository.py",
)


def test_exact_service_operations_and_mutation_return_types():
    assert {
        name for name, _ in inspect.getmembers(EnterpriseObjectService, inspect.isfunction)
    } == {"create", "archive", "unarchive"}
    assert get_type_hints(EnterpriseObjectService.create)["return"] is uuid.UUID
    for operation in (
        EnterpriseObjectService.archive,
        EnterpriseObjectService.unarchive,
        repository.add,
    ):
        assert get_type_hints(operation)["return"] is type(None)
    assert list(inspect.signature(repository.add).parameters) == ["session", "obj"]
    for operation in (repository.get_by_id, repository.list_by_workspace):
        assert (
            inspect.signature(operation).parameters["workspace_id"].default
            is inspect.Parameter.empty
        )


def test_no_transaction_end_or_runtime_symbols_in_slice():
    forbidden = {"RuntimeEvent", "RuntimeEventService"}
    for path in MODULES:
        assert path.is_file()
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    assert node.func.attr not in {"commit", "rollback"} | forbidden
                if isinstance(node.func, ast.Name):
                    assert node.func.id not in forbidden | {"commit", "rollback"}
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [a.name for a in node.names]
                if isinstance(node, ast.ImportFrom):
                    names.append(node.module or "")
                assert not any(set(name.split(".")) & forbidden for name in names)
    assert "RuntimeEvent emission is deferred" in ast.get_docstring(
        ast.parse(MODULES[0].read_text(encoding="utf-8"))
    )


def test_repository_has_only_the_three_approved_operations():
    tree = ast.parse(MODULES[1].read_text(encoding="utf-8"))
    assert {n.name for n in tree.body if isinstance(n, ast.FunctionDef)} == {
        "add",
        "get_by_id",
        "list_by_workspace",
    }


def test_service_module_has_no_public_free_operations():
    tree = ast.parse(MODULES[0].read_text(encoding="utf-8"))
    assert {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and not node.name.startswith("_")
    } == set()
    assert {node.name for node in tree.body if isinstance(node, ast.ClassDef)} == {
        "EnterpriseObjectService"
    }


@pytest.mark.parametrize("limit", [None, 1, 100])
def test_list_limit_and_no_offset(limit):
    session = Mock()
    session.scalars.return_value = []
    kwargs = {} if limit is None else {"limit": limit}
    repository.list_by_workspace(session, uuid.uuid4(), **kwargs)
    statement = session.scalars.call_args.args[0]
    compiled = statement.compile(dialect=postgresql.dialect())
    assert "OFFSET" not in str(compiled)
    assert compiled.params["param_1"] == (100 if limit is None else limit)
    assert set(inspect.signature(repository.list_by_workspace).parameters) == {
        "session",
        "workspace_id",
        "limit",
    }


@pytest.mark.parametrize(
    "operation,phase",
    [
        ("archive", "archived"),
        ("archive", "superseded"),
        ("unarchive", "active"),
        ("unarchive", "superseded"),
    ],
)
def test_invalid_transition_precedes_mutation_and_audit(monkeypatch, operation, phase):
    obj = EnterpriseObject(phase=phase)
    get = Mock(return_value=obj)
    record = Mock()
    monkeypatch.setattr(repository, "get_by_id", get)
    monkeypatch.setattr(AuditService, "record", record)
    session = Mock()
    workspace_id, object_id = uuid.uuid4(), uuid.uuid4()
    with pytest.raises(ValueError, match="cannot transition"):
        getattr(EnterpriseObjectService, operation)(
            session, workspace_id=workspace_id, object_id=object_id
        )
    assert obj.phase == phase
    record.assert_not_called()
    get.assert_called_once_with(session, workspace_id, object_id, for_update=True)


@pytest.mark.parametrize("operation", ["create", "archive", "unarchive"])
def test_no_public_operation_accepts_superseded_target(operation):
    kwargs = {"workspace_id": uuid.uuid4(), "phase": "superseded"}
    if operation == "create":
        kwargs.update(type="example", owner_id=uuid.uuid4())
    else:
        kwargs["object_id"] = uuid.uuid4()
    with pytest.raises(TypeError, match="phase"):
        getattr(EnterpriseObjectService, operation)(Mock(), **kwargs)


@pytest.mark.parametrize("limit", [0, -1, True, 1.5, "1", None])
def test_invalid_list_limit_does_not_query(limit):
    session = Mock()
    with pytest.raises(ValueError, match="positive int"):
        repository.list_by_workspace(session, uuid.uuid4(), limit=limit)
    session.scalars.assert_not_called()


def test_locked_get_is_scoped_and_refreshes_identity_map():
    session = Mock()
    workspace_id, object_id = uuid.uuid4(), uuid.uuid4()
    repository.get_by_id(session, workspace_id, object_id, for_update=True)
    statement = session.scalar.call_args.args[0]
    compiled = statement.compile(dialect=postgresql.dialect())
    assert "FOR UPDATE" in str(compiled)
    assert "enterprise_objects.workspace_id =" in str(compiled)
    assert "enterprise_objects.id =" in str(compiled)
    assert set(compiled.params.values()) == {workspace_id, object_id}
    assert statement.get_execution_options()["populate_existing"] is True
