"""Architecture boundary -- `audit_record_repository` has exactly one
production consumer.

The five `subject_*` columns on `audit_records` carry no foreign key.
Accepted Q2-RI admits that only where durable correctness, validation and
historical subject resolvability are established through another
explicit, recorded mechanism; A-11 supplies that mechanism as the
write-time validation contract in `AuditService.record(...)`. That
substitution only holds while every production write goes through the
service. A second caller reaching `audit_record_repository.add(...)`
directly would produce records whose subject reference was never
validated against a loaded subject -- records the database cannot
reject, because there is no foreign key to reject them with.

So this file is not a style rule. It is the static guard around the
supported repository write path. It does not claim to detect direct
Session use or raw SQL; those remain outside this repository boundary
and are governed by the architectural contract and review.

It asserts both directions:

- positively, that the one authorized consumer (`app/services/
  audit_service.py`) exists, imports the repository as a module with no
  alias, and calls `add` on it;
- negatively, that no other file under `app/` -- other than the
  repository module and that one authorized consumer -- **statically**
  reaches the module or the function. Dynamic reach through `getattr`,
  `importlib`, or similar is not detectable by AST analysis and is not
  covered by this test.

The positive half is what makes the negative half meaningful. A pure
absence scan passes trivially while no consumer exists at all -- which
is exactly the state of this branch before `audit_service.py` is
written; every test here that needs the service file to exist asserts
that first, with a message naming what's missing, so that state produces
a deliberate assertion failure rather than an uncontrolled
`FileNotFoundError` from `ast.parse`.

The scan covers `app/` only. `tests/` is deliberately out of scope: the
persistence suite (`tests/test_audit_record_persistence.py`) is required
to call `audit_record_repository.add(...)` directly, because that is the
only way to demonstrate that the repository accepts an unvalidated
record and that `add()` itself does not commit. A later reader must not
"fix" this scan to include `tests/`, since that would fail on -- and
invite deleting -- the very tests that prove those two properties.

Nothing here imports application code. Everything is read from source
with `ast`, so the test reports honestly on a tree where
`audit_service.py` is missing or does not yet import correctly.

This intentionally makes `audit_service.py` the repository module's sole
production importer for the current A-11 slice. A future authorized
reader (e.g. a read-only reporting service) would require a deliberate
change to this test, not a silent bypass of it.

Detecting direct `AuditRecord(...)` construction in production code was
considered and is deliberately not covered here. The boundary this file
enforces stops at the repository write path.
"""

import ast
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / "app"
BACKEND = APP.parent

REPOSITORY_PATH = APP / "repositories" / "audit_record_repository.py"
SERVICE_PATH = APP / "services" / "audit_service.py"

REPOSITORY_PACKAGE = "app.repositories"
REPOSITORY_MODULE = "audit_record_repository"
REPOSITORY_DOTTED = "app.repositories.audit_record_repository"
WRITE_FUNCTION = "add"

#: The repository file defines `add`; scanning it for references to itself
#: would report a violation that is not one. The service is excluded
#: because it is the one authorized consumer, asserted separately by the
#: positive tests below.
EXCLUDED_FROM_CONSUMER_SCAN = frozenset({REPOSITORY_PATH, SERVICE_PATH})


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _scanned_files() -> list[Path]:
    """Every production file the negative consumer scan covers."""
    return sorted(
        p for p in APP.rglob("*.py") if p not in EXCLUDED_FROM_CONSUMER_SCAN
    )


def _render_import(node: ast.ImportFrom | ast.Import) -> str:
    """The import statement as written, with every name it binds.

    Rendering the whole node rather than the one matching alias is what
    makes a second imported name visible to the caller's comparison, and
    what keeps a failure message truthful about the source line.
    """
    names = ", ".join(
        a.name + (f" as {a.asname}" if a.asname else "") for a in node.names
    )
    if isinstance(node, ast.Import):
        return f"import {names}"
    return f"from {'.' * node.level}{node.module or ''} import {names}"


def _repository_imports(tree: ast.Module) -> list[tuple[int, str]]:
    """Every import in a file that reaches the repository module or its
    write function, as `(lineno, statement as written)`.

    One entry per import statement, not per name: a statement binding a
    second name renders differently and so cannot pass a comparison that
    expects the exact single-name form.

    Relative forms are matched too. `from . import audit_record_repository`
    and `from .audit_record_repository import add` are how a re-export
    inside `app/repositories/__init__.py` would actually be written, and
    that file is precisely where the append-only public API forbids one.
    """
    found: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            absolute = node.module == REPOSITORY_DOTTED or (
                node.module == REPOSITORY_PACKAGE
                and any(a.name == REPOSITORY_MODULE for a in node.names)
            )
            relative = node.level > 0 and (
                node.module == REPOSITORY_MODULE
                or any(a.name == REPOSITORY_MODULE for a in node.names)
            )
            if absolute or relative:
                found.append((node.lineno, _render_import(node)))
        elif isinstance(node, ast.Import):
            if any(a.name == REPOSITORY_DOTTED for a in node.names):
                found.append((node.lineno, _render_import(node)))
    return sorted(found)


def _is_repository_add_call(func: ast.expr) -> bool:
    """`audit_record_repository.add(...)`, whether the module was reached by
    name (`audit_record_repository.add(...)`) or through a dotted package
    path such as `app.repositories.audit_record_repository.add(...)` or
    `repositories.audit_record_repository.add(...)`.
    """
    if not (isinstance(func, ast.Attribute) and func.attr == WRITE_FUNCTION):
        return False
    owner = func.value
    if isinstance(owner, ast.Name):
        return owner.id == REPOSITORY_MODULE
    if isinstance(owner, ast.Attribute):
        return owner.attr == REPOSITORY_MODULE
    return False


def _calls_repository_add(tree: ast.Module) -> bool:
    return any(
        isinstance(node, ast.Call) and _is_repository_add_call(node.func)
        for node in ast.walk(tree)
    )


def _repository_references(tree: ast.Module) -> list[tuple[int, str]]:
    """Every way a file reaches the repository module or its write function.

    Returns `(lineno, description)` pairs so a failure message can name
    both the location and the kind of violation. Rests on the same
    `_repository_imports` detector the positive test uses, so the two
    sides of the contract cannot silently drift apart under a later edit.
    """
    found: list[tuple[int, str]] = [
        (lineno, f"imports the repository via `{form}`")
        for lineno, form in _repository_imports(tree)
    ]
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _is_repository_add_call(node.func):
            found.append((node.lineno, "calls audit_record_repository.add(...)"))
    return sorted(found)


def test_the_repository_module_exists() -> None:
    assert REPOSITORY_PATH.is_file(), f"missing: {REPOSITORY_PATH.relative_to(BACKEND)}"


def test_exactly_one_production_consumer_exists() -> None:
    """Fails informatively while the service is absent, rather than letting
    a later test's bare `ast.parse` raise an uncontrolled
    `FileNotFoundError`."""
    assert SERVICE_PATH.is_file(), (
        f"missing: {SERVICE_PATH.relative_to(BACKEND)} -- the write-time "
        "validation contract A-11 requires has no home, so the absent "
        "subject foreign keys are traded for nothing"
    )


def test_the_consumer_imports_the_repository_exactly_once_unaliased() -> None:
    """One import statement, of one exact form. A list comparison rejects an
    alias, a direct `add` import, the dotted form, a relative form, a
    second name bound alongside the repository, a duplicate import, and
    absence -- all in a single assertion.
    """
    assert SERVICE_PATH.is_file(), f"missing: {SERVICE_PATH.relative_to(BACKEND)}"
    imports = _repository_imports(_parse(SERVICE_PATH))
    expected = f"from {REPOSITORY_PACKAGE} import {REPOSITORY_MODULE}"
    assert [form for _, form in imports] == [expected], (
        f"{SERVICE_PATH.relative_to(BACKEND)} must reach the repository through "
        f"exactly one import, `{expected}`; found:\n"
        + "\n".join(f"  line {n}: {f}" for n, f in imports)
    )


def test_the_consumer_calls_the_repository_add() -> None:
    """Importing the module without calling `add` would leave the service
    a validation layer over nothing."""
    assert SERVICE_PATH.is_file(), f"missing: {SERVICE_PATH.relative_to(BACKEND)}"
    assert _calls_repository_add(_parse(SERVICE_PATH)), (
        f"{SERVICE_PATH.relative_to(BACKEND)} must call "
        f"`{REPOSITORY_MODULE}.{WRITE_FUNCTION}(...)`"
    )


def test_no_other_production_file_reaches_the_repository() -> None:
    """The negative scan. Excludes the repository itself and the one
    authorized consumer; everything else under `app/` must not reach
    either the module or its write function."""
    offenders = [
        f"  {path.relative_to(BACKEND)}:{lineno}: {violation}"
        for path in _scanned_files()
        for lineno, violation in _repository_references(_parse(path))
    ]
    assert not offenders, (
        "only app/services/audit_service.py may reach the audit repository "
        "write API; found:\n" + "\n".join(offenders)
    )


def test_the_consumer_scan_excludes_the_repository_and_covers_real_files() -> None:
    """The exclusion alone is not worth a test. What is worth a test is that
    the scan above is not running over an empty or near-empty set -- an
    exclusion bug that dropped every file would leave
    `test_no_other_production_file_reaches_the_repository` green and
    meaningless.
    """
    scanned = _scanned_files()
    assert REPOSITORY_PATH not in scanned
    assert SERVICE_PATH not in scanned
    assert APP / "models" / "audit_record.py" in scanned
    assert APP / "repositories" / "__init__.py" in scanned
    assert len(scanned) >= 10, f"consumer scan covers only {len(scanned)} files"


def test_neither_the_repository_nor_the_service_ends_the_transaction() -> None:
    """A-11 requires the business mutation and its audit record to commit
    or fail together, which makes the caller the only party entitled to
    end the transaction.

    Asserted statically because it cannot be asserted from the database:
    under an outer transaction a stray `session.commit()` is a savepoint
    release, and whether a later rollback hides it depends on savepoint
    semantics, not on the property under test. Both words also appear in
    both modules' docstrings, so a text search cannot answer this either
    -- only executable `Call` nodes count.
    """
    assert REPOSITORY_PATH.is_file(), f"missing: {REPOSITORY_PATH.relative_to(BACKEND)}"
    assert SERVICE_PATH.is_file(), f"missing: {SERVICE_PATH.relative_to(BACKEND)}"
    offenders = []
    for path in (REPOSITORY_PATH, SERVICE_PATH):
        for node in ast.walk(_parse(path)):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in {"commit", "rollback"}
            ):
                offenders.append(
                    f"  {path.relative_to(BACKEND)}:{node.lineno}: "
                    f"calls .{node.func.attr}()"
                )
    assert not offenders, (
        "neither module may end the caller's transaction; found:\n"
        + "\n".join(offenders)
    )
