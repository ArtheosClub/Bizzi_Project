"""Amendment 4 create/add-only surface; no A-13 approval implied."""

import ast
import inspect
import uuid
from pathlib import Path
from typing import get_type_hints
from unittest.mock import Mock

import pytest

from app.repositories import task_repository as repository
from app.services.audit_service import AuditService
from app.services.task_service import TaskService

APP = Path(__file__).resolve().parents[1] / "app"
MODULES = (APP / "services/task_service.py", APP / "repositories/task_repository.py")


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


def test_service_module_has_no_public_free_operations():
    tree = ast.parse(MODULES[0].read_text(encoding="utf-8"))
    assert {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and not node.name.startswith("_")
    } == set()
    assert {node.name for node in tree.body if isinstance(node, ast.ClassDef)} == {"TaskService"}


def test_non_null_source_rejected_before_any_write(monkeypatch):
    add, record = Mock(), Mock()
    monkeypatch.setattr(repository, "add", add)
    monkeypatch.setattr(AuditService, "record", record)
    session = Mock()
    with pytest.raises(ValueError, match="R9 authority"):
        TaskService.create(session, workspace_id=uuid.uuid4(), source_object_id=uuid.uuid4())
    add.assert_not_called()
    record.assert_not_called()
    assert session.mock_calls == []


def test_exact_create_add_surface():
    assert {name for name, _ in inspect.getmembers(TaskService, inspect.isfunction)} == {"create"}
    assert get_type_hints(TaskService.create)["return"] is uuid.UUID
    assert get_type_hints(repository.add)["return"] is type(None)
    assert list(inspect.signature(repository.add).parameters) == ["session", "obj"]
    tree = ast.parse(MODULES[1].read_text())
    assert {n.name for n in tree.body if isinstance(n, ast.FunctionDef)} == {"add"}
    assert not hasattr(repository, "get_by_id") and not hasattr(repository, "list_by_workspace")


def test_create_cannot_override_initial_phase():
    with pytest.raises(TypeError, match="phase"):
        TaskService.create(Mock(), workspace_id=uuid.uuid4(), phase="superseded")
