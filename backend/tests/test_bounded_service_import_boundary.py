"""Bounded common import gate retained under record 5, not approved by A-13.
Relaxation requires explicit Owner-approved integration review.

This is a source-import gate, not a runtime sandbox: computed reflection and
arbitrary ORM construction still need explicit review. Tests are outside app.
"""

import ast
import importlib.util
from pathlib import Path

import pytest

APP = Path(__file__).resolve().parents[1] / "app"
MATRIX = {
    "app.services.task_service": {
        "app.services.task_service",
        "app.services.business_request_intake_service",
    },
    "app.services.enterprise_object_service": {
        "app.services.enterprise_object_service",
        "app.services.business_request_intake_service",
    },
    "app.repositories.task_repository": {"app.services.task_service"},
    "app.repositories.enterprise_object_repository": {"app.services.enterprise_object_service"},
}


def targets(source, module, *, package=False):
    """Resolve import surfaces, aliases, attribute access and literal dynamic calls."""
    tree = ast.parse(source)
    context = module if package else module.rpartition(".")[0]
    aliases = {}
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                found.add(name.name)
                aliases[name.asname or name.name.split(".")[0]] = (
                    name.name if name.asname else name.name.split(".")[0]
                )
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                base = importlib.util.resolve_name("." * node.level + base, context)
            found.add(base)
            for name in node.names:
                target = base + "." + name.name
                found.add(target)
                aliases[name.asname or name.name] = target
                if name.name == "*":
                    # Package star imports could expose either protected child.
                    found.update(t for t in MATRIX if t.rpartition(".")[0] == base)

    def dotted(node):
        if isinstance(node, ast.Name):
            return aliases.get(node.id, node.id)
        if isinstance(node, ast.Attribute):
            prefix = dotted(node.value)
            return prefix + "." + node.attr if prefix else None
        return None

    # Resolve straightforward alias assignments as well as import aliases.
    for _ in range(len(tree.body) + 1):
        changed = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                value = dotted(node.value)
                if value:
                    for target in node.targets:
                        if isinstance(target, ast.Name) and aliases.get(target.id) != value:
                            aliases[target.id] = value
                            changed = True
        if not changed:
            break
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            value = dotted(node)
            if value:
                found.add(value)
        if isinstance(node, ast.Call) and dotted(node.func) in {
            "importlib.import_module",
            "__import__",
            "builtins.__import__",
        }:
            if node.args and isinstance(node.args[0], ast.Constant):
                name = node.args[0].value
                if isinstance(name, str):
                    if name.startswith("."):
                        supplied = next(
                            (k.value for k in node.keywords if k.arg == "package"), None
                        )
                        if supplied is None and len(node.args) > 1:
                            supplied = node.args[1]
                        if isinstance(supplied, ast.Constant) and isinstance(supplied.value, str):
                            name = importlib.util.resolve_name(name, supplied.value)
                        else:
                            continue
                    found.add(name)
                    fromlist = next((k.value for k in node.keywords if k.arg == "fromlist"), None)
                    if fromlist is None and len(node.args) > 3:
                        fromlist = node.args[3]
                    if isinstance(fromlist, (ast.List, ast.Tuple)):
                        for item in fromlist.elts:
                            if isinstance(item, ast.Constant) and isinstance(item.value, str):
                                found.add(name + "." + item.value)
    return {
        target
        for target in MATRIX
        if any(value == target or value.startswith(target + ".") for value in found)
    }


def violations(source, module, *, package=False):
    if not (module == "app" or module.startswith("app.")):
        return set()
    return {t for t in targets(source, module, package=package) if module not in MATRIX[t]}


def test_production_import_boundary_and_required_target_presence():
    for module in MATRIX:
        assert (APP.parent / (module.replace(".", "/") + ".py")).is_file(), module
    failures = []
    for path in sorted(APP.rglob("*.py")):
        parts = path.relative_to(APP.parent).with_suffix("").parts
        package = parts[-1] == "__init__"
        module = ".".join(parts[:-1] if package else parts)
        for target in sorted(violations(path.read_text(), module, package=package)):
            failures.append(f"{path.relative_to(APP.parent)} imports {target}")
    assert not failures, "\n".join(failures)


@pytest.mark.parametrize("pair", ["task", "enterprise_object"])
def test_allowed_own_service_repository_and_external_tests(pair):
    source = f"from app.repositories import {pair}_repository as repository"
    assert not violations(source, f"app.services.{pair}_service")
    assert not violations(source, "tests.consumer")
    assert not violations(f"import app.services.{pair}_service", "tests.consumer")
    assert violations(source, "app.services.unrelated")
    other = "task" if pair == "enterprise_object" else "enterprise_object"
    assert violations(source, f"app.services.{other}_service")


@pytest.mark.parametrize(
    "source,module,package",
    [
        ("import app.services.task_service as s", "app.consumer", False),
        ("from app.services.task_service import TaskService as S", "app.consumer", False),
        ("from app.services import task_service", "app.consumer", False),
        ("from . import task_service", "app.services.consumer", False),
        ("from .task_service import TaskService", "app.services", True),
        ("from ..repositories import task_repository", "app.services.consumer", False),
        ("from app.repositories.task_repository import add", "app.consumer", False),
        ("from app.repositories.task_repository import get_by_id", "app.consumer", False),
        ("import app.repositories as r\nr.task_repository.add()", "app.consumer", False),
        ("import app.services as s\nx = s\nx.task_service", "app.consumer", False),
        (
            'import importlib as i\ni.import_module("app.services.task_service")',
            "app.consumer",
            False,
        ),
        (
            'from importlib import import_module as load\nload("app.repositories.task_repository")',
            "app.consumer",
            False,
        ),
        (
            'from importlib import import_module\nimport_module(".task_service", "app.services")',
            "app.consumer",
            False,
        ),
        ('__import__("app.repositories", fromlist=["task_repository"])', "app.consumer", False),
        ('import builtins as b\nb.__import__("app.services.task_service")', "app.consumer", False),
        ("from app.services import *", "app.consumer", False),
    ],
)
def test_forbidden_import_forms(source, module, package):
    assert violations(source, module, package=package)
    # Apply every fixture equally to the existing EnterpriseObject pair.
    assert violations(source.replace("task", "enterprise_object"), module, package=package)


def test_intake_has_only_create_calls_and_no_transaction_or_orm_mutation():
    path = APP / "services/business_request_intake_service.py"
    tree = ast.parse(path.read_text())
    imported = targets(path.read_text(), "app.services.business_request_intake_service")
    assert imported == {"app.services.task_service", "app.services.enterprise_object_service"}
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    ]
    for call in calls:
        assert call.func.attr not in {
            "commit",
            "rollback",
            "close",
            "add",
            "flush",
            "execute",
            "archive",
            "unarchive",
            "get_by_id",
            "list_by_workspace",
        }
    primitive_calls = [
        (call.func.value.id, call.func.attr)
        for call in calls
        if isinstance(call.func.value, ast.Name)
        and call.func.value.id in {"TaskService", "EnterpriseObjectService"}
    ]
    assert sorted(primitive_calls) == [
        ("EnterpriseObjectService", "create"),
        ("TaskService", "create"),
    ]
    assert not any(
        isinstance(node, ast.Assign) and any(isinstance(t, ast.Attribute) for t in node.targets)
        for node in ast.walk(tree)
    )
    # Router imports neither primitive nor protected repository.
    router_source = (APP / "api/business_request_intake.py").read_text()
    assert not targets(router_source, "app.api.business_request_intake")


def test_intake_matrix_does_not_admit_direct_repositories():
    consumer = "app.services.business_request_intake_service"
    for pair in ("task", "enterprise_object"):
        assert not violations(f"from app.services.{pair}_service import X", consumer)
        assert violations(f"from app.repositories import {pair}_repository", consumer)
