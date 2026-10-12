"""Owner record L: explicitly admitted local-only lock verification, never CI."""

import hashlib
import json
import os
import re
import subprocess
import uuid
from datetime import UTC, datetime
from pathlib import Path

import pytest
from sqlalchemy import create_engine, delete, func, select, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.preproduction_guard import (
    POLICY_KEY,
    ScopeViolationError,
    require_engine,
    require_session,
    require_test_destination,
    resolve_policy,
)
from app.models import AuditRecord, EnterpriseObject, User, Workspace
from app.repositories import enterprise_object_repository as repository

PREPARATION_ID = "MVP-OPTION-L-IMPLEMENTATION-2026-10-08"
PREPARATION_SHA = "c758a1a01725262dc89e1c03d09df250d73dc0c741565e8bb1f2ff2b905f7fb9"
GATE_PREPARATION_ID = "MVP-OPTION-L-MERGE-GATE-IMPLEMENTATION-2026-10-10"
DEPENDENCY_PATHS = {"backend/pyproject.toml", "backend/uv.lock"}
EDIT_PATHS = {
    "backend/tests/test_enterprise_object_service_persistence.py",
    "backend/tests/test_enterprise_object_repository_lock_local.py",
    "backend/tests/local_only_manifest.json",
    "backend/tests/test_ci_verification.py",
    ".github/workflows/backend-ci.yml",
}


def _refuse(reason):
    raise RuntimeError("LOCAL_ADMISSION_REFUSED:" + reason)


def _hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(root, *args):
    try:
        return subprocess.check_output(
            ["git", "--no-optional-locks", *args], cwd=root
        )
    except (OSError, subprocess.SubprocessError):
        _refuse("git-observation")


def _index_snapshot(root):
    index = root / ".git/index"
    try:
        stat = index.stat()
        return {"sha256": _hash(index), "size": stat.st_size, "mtime_ns": stat.st_mtime_ns}
    except OSError:
        _refuse("index")


def _remote_main(root):
    try:
        result = subprocess.run(
            ["git", "--no-optional-locks", "-c", "credential.helper=", "ls-remote",
             "--exit-code", "https://github.com/ArtheosClub/Bizzi_Project.git", "refs/heads/main"],
            cwd=root, env=dict(os.environ, GIT_TERMINAL_PROMPT="0",
                               GIT_ASKPASS="/usr/bin/false", SSH_ASKPASS="/usr/bin/false"),
            capture_output=True, text=True, timeout=20,
        )
    except (OSError, subprocess.SubprocessError):
        _refuse("remote-main")
    if result.returncode != 0:
        _refuse("remote-main")
    match = re.fullmatch(r"([0-9a-f]{40})\s+refs/heads/main\n?", result.stdout)
    if match is None:
        _refuse("remote-main")
    return match[1]


def _merge_gate_checks(root, binding, index_before):
    if (root / ".env").exists() or (root / "backend/.env").exists():
        _refuse("env-file")
    for args in (("diff", "--name-only", "HEAD", "--", "backend", ".github"),
                 ("diff", "--cached", "--name-only", "--", "backend", ".github"),
                 ("ls-files", "--others", "--exclude-standard", "--", "backend", ".github")):
        if _git(root, *args).strip():
            _refuse("clean-tree")
    for name in EDIT_PATHS:
        if hashlib.sha256(_git(root, "show", "HEAD:" + name)).hexdigest() != binding[
            "source_sha256_by_path"
        ][name]:
            _refuse("committed-source")
    dependencies = binding.get("dependency_sha256_by_path", {})
    if not isinstance(dependencies, dict) or set(dependencies) != DEPENDENCY_PATHS:
        _refuse("dependency")
    for name, digest in dependencies.items():
        if _hash(root / name) != digest or hashlib.sha256(
            _git(root, "show", "HEAD:" + name)
        ).hexdigest() != digest:
            _refuse("dependency")
    values = _git(root, "rev-parse", "HEAD^{tree}", "HEAD:backend", "HEAD:.github",
                  "origin/main").decode().splitlines()
    if len(values) != 4:
        _refuse("tree")
    if values[:3] != [binding.get(k) for k in ("candidate_tree", "backend_tree", "github_tree")]:
        _refuse("tree")
    base = _git(root, "merge-base", "HEAD", "origin/main").decode().strip()
    if (values[3] != binding.get("origin_main")
            or base != binding.get("merge_base") or base != values[3]):
        _refuse("main-base")
    if _remote_main(root) != values[3]:
        _refuse("remote-main")
    if _index_snapshot(root) != index_before:
        _refuse("index")


def _load_admission():
    binding_path = os.environ.get("BIZZI_LOCAL_LOCK_BINDING_PATH", "")
    binding_sha = os.environ.get("BIZZI_LOCAL_LOCK_BINDING_SHA256", "")
    grant_path = os.environ.get("BIZZI_LOCAL_LOCK_PERMISSION_SOURCE_PATH", "")
    grant_sha = os.environ.get("BIZZI_LOCAL_LOCK_PERMISSION_SOURCE_SHA256", "")
    if not all((binding_path, binding_sha, grant_path, grant_sha)):
        _refuse("missing-optin")
    try:
        path, source_path = Path(binding_path), Path(grant_path)
        if _hash(path) != binding_sha:
            _refuse("binding-hash")
        if _hash(source_path) != grant_sha:
            _refuse("permission-hash")
        binding = json.loads(path.read_text())
        source = source_path.read_text()
    except (OSError, ValueError):
        _refuse("malformed-binding")
    if not isinstance(binding, dict):
        _refuse("malformed-binding")
    if len(re.findall(r"(?<![0-9a-f])" + re.escape(binding_sha) + r"(?![0-9a-f])", source)) != 1:
        _refuse("binding-occurrence")
    fields = {}
    for label in ("Permission ID", "Binding SHA-256", "Mode", "Collector",
                  "Valid from UTC", "Valid until UTC"):
        matches = re.findall(r"^" + re.escape(label) + r": (.+)$", source, re.M)
        if len(matches) != 1:
            _refuse("permission-field")
        fields[label] = matches[0]
    if fields["Binding SHA-256"] != binding_sha:
        _refuse("binding-field")
    mode = binding.get("mode")
    prefixes = {"WORKTREE_VALIDATION": "MVP-OPTION-L-WORKTREE-VALIDATION-",
                "MERGE_GATE": "MVP-OPTION-L-MERGE-GATE-RUN-"}
    prefix = prefixes.get(mode, "")
    if fields["Permission ID"] in (PREPARATION_ID, GATE_PREPARATION_ID) or not prefix or not fields[
        "Permission ID"
    ].startswith(prefix):
        _refuse("permission-id")
    if fields["Mode"] != mode:
        _refuse("mode")
    if not binding.get("collector") or fields["Collector"] != binding.get("collector"):
        _refuse("collector")
    if fields["Valid from UTC"] != binding.get("valid_from_utc") or fields[
        "Valid until UTC"
    ] != binding.get("valid_until_utc"):
        _refuse("window")
    try:
        start = datetime.fromisoformat(fields["Valid from UTC"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(fields["Valid until UTC"].replace("Z", "+00:00"))
        if start.utcoffset() != UTC.utcoffset(start) or end.utcoffset() != UTC.utcoffset(end):
            _refuse("window")
        if not start <= datetime.now(UTC) < end:
            _refuse("expired")
    except (ValueError, TypeError):
        _refuse("window")
    preparation_id = PREPARATION_ID if mode == "WORKTREE_VALIDATION" else GATE_PREPARATION_ID
    preparation_sha = binding.get("preparation_source_sha256", "")
    if binding.get("preparation_permission_id") != preparation_id or not re.fullmatch(
        r"[0-9a-f]{64}", str(preparation_sha)
    ) or (mode == "WORKTREE_VALIDATION" and preparation_sha != PREPARATION_SHA):
        _refuse("preparation")
    if any(key.startswith("execution_permission") for key in binding):
        _refuse("binding-run-fields")
    root = Path(__file__).resolve().parents[2]
    index_before = _index_snapshot(root) if mode == "MERGE_GATE" else None
    head = _git(root, "rev-parse", "HEAD").decode().strip()
    if binding.get("base_head") != head or binding.get("candidate_head") != head:
        _refuse("head")
    pins = binding.get("source_sha256_by_path", {})
    if not isinstance(pins, dict) or set(pins) != EDIT_PATHS:
        _refuse("source-pins")
    if any(_hash(root / name) != digest for name, digest in pins.items()):
        _refuse("source-pins")
    # Pure URL admission only: never create an Engine here.
    try:
        require_test_destination(get_settings().database_url)
    except ScopeViolationError:
        _refuse("bind")
    if get_settings().synthetic_execution_profile != "local_test":
        _refuse("profile")
    prep = Path(binding.get("preparation_source_path", ""))
    if not prep.is_file() or _hash(prep) != preparation_sha:
        _refuse("preparation")
    if mode == "MERGE_GATE":
        if re.findall(r"^Preparation permission ID: (.+)$", prep.read_text(), re.M) != [
            GATE_PREPARATION_ID
        ]:
            _refuse("preparation-field")
        _merge_gate_checks(root, binding, index_before)
    allowed = binding.get("allowed_initial_contents", {})
    destinations = []
    for key in ("evidence_dir", "ledger_dir", "scratch_dir"):
        directory = Path(binding.get(key, ""))
        if not directory.is_absolute() or not directory.is_dir():
            _refuse("directory")
        directory = directory.resolve()
        if directory == root or root in directory.parents:
            _refuse("directory")
        expected = allowed.get(key, [])
        if not isinstance(expected, list) or sorted(p.name for p in directory.iterdir()) != sorted(
            expected
        ):
            _refuse("directory")
        if not os.access(directory, os.W_OK):
            _refuse("writable")
        destinations.append(directory)
    if any(a == b or a in b.parents or b in a.parents
           for i, a in enumerate(destinations) for b in destinations[i + 1:]):
        _refuse("directory")
    binding["operative_permission_id"] = fields["Permission ID"]
    binding["operative_permission_sha256"] = grant_sha
    for key in ("evidence_dir", "ledger_dir"):
        _durable_record_at(Path(binding[key]), "LOCAL_ADMISSION.json", {
            "permission_id": fields["Permission ID"], "permission_sha256": grant_sha,
            "binding_sha256": binding_sha, "UTC": datetime.now(UTC).isoformat(),
        })
    return binding


def _durable_record_at(directory, name, value):
    with (directory / name).open("x") as output:
        json.dump(value, output, indent=2)
        output.write("\n")
        output.flush()
        os.fsync(output.fileno())
    descriptor = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


# Bare pytest without a run opt-in intentionally fails collection; never skips.
_ADMISSION = _load_admission()


@pytest.fixture(scope="module")
def engine():
    policy = resolve_policy(get_settings().synthetic_execution_profile)
    engine = create_engine(get_settings().database_url, pool_pre_ping=True)
    require_engine(engine, policy)
    with engine.connect() as connection:
        assert connection.execute(text("SELECT current_database(),current_user")).one() == (
            "bizzi_test", "bizzi"
        )
        revisions = connection.execute(text("SELECT version_num FROM alembic_version"))
        assert revisions.scalars().all() == ["adw02_02"]
        from app.models import AgentDefinition, Task, WorkspaceMembership

        for model in (User, Workspace, EnterpriseObject, WorkspaceMembership,
                      AuditRecord, Task, AgentDefinition):
            assert connection.scalar(select(func.count()).select_from(model)) == 0
    yield engine
    engine.dispose()


def _durable_record(directory_variable, name, value):
    directory = Path(os.environ[directory_variable])
    binding_key = "ledger_dir" if directory_variable == "BIZZI_B4_LEDGER_DIR" else "evidence_dir"
    if directory.resolve() != Path(_ADMISSION[binding_key]).resolve():
        _refuse("directory")
    # The Owner names fresh external destinations; never create or overwrite here.
    if not directory.is_dir():
        raise RuntimeError("Owner-named evidence destination is unavailable")
    with (directory / name).open("x") as output:
        json.dump(value, output, indent=2)
        output.write("\n")
        output.flush()
        os.fsync(output.fileno())
    descriptor = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _verify_lock_fixture(session, user_id, workspace_id, object_id):
    from app.models import AgentDefinition, Task, WorkspaceMembership

    require_session(session)
    models = [User, Workspace, EnterpriseObject, WorkspaceMembership, AuditRecord,
              Task, AgentDefinition]
    counts = {model.__tablename__: session.scalar(select(func.count()).select_from(model))
              for model in models}
    expected = {model.__tablename__: int(model in (User, Workspace, EnterpriseObject))
                for model in models}
    if counts != expected:
        raise RuntimeError("STOP: unexpected fixture rows or committed history")
    user = session.get(User, user_id)
    workspace = session.get(Workspace, workspace_id)
    obj = session.get(EnterpriseObject, object_id)
    if (
        user is None or workspace is None or obj is None
        or workspace.owner_id != user_id or obj.owner_id != user_id
        or obj.workspace_id != workspace_id or obj.phase != "active"
        or user.auth_issuer is not None or user.auth_subject is not None
    ):
        raise RuntimeError("STOP: fixture identities or recognition premises differ")
    return counts


def test_two_connections_hold_repository_lock_timeout_then_rollback(engine, execution_policy):
    user_id, workspace_id, object_id = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    identity = {"user_id": str(user_id), "workspace_id": str(workspace_id),
                "object_id": str(object_id)}
    committed_setup = False
    try:
        with Session(engine, info={POLICY_KEY: execution_policy}) as setup:
            require_session(setup)
            setup.add(User(id=user_id))
            setup.flush()
            setup.add(Workspace(
                id=workspace_id, name="B4 synthetic lock fixture", owner_id=user_id
            ))
            setup.flush()
            repository.add(setup, EnterpriseObject(
                id=object_id, workspace_id=workspace_id, owner_id=user_id,
                type="example", phase="active",
            ))
            _verify_lock_fixture(setup, user_id, workspace_id, object_id)
            setup.commit()
            committed_setup = True
        with Session(engine, info={POLICY_KEY: execution_policy}) as first, Session(
            engine, info={POLICY_KEY: execution_policy}
        ) as second:
            require_session(first)
            require_session(second)
            pids = [first.scalar(text("SELECT pg_backend_pid()")),
                    second.scalar(text("SELECT pg_backend_pid()"))]
            assert pids[0] != pids[1]
            obj = repository.get_by_id(first, workspace_id, object_id, for_update=True)
            assert obj is not None and obj.phase == "active"
            second.execute(text("SET LOCAL lock_timeout = '200ms'"))
            with pytest.raises(OperationalError) as exc:
                repository.get_by_id(second, workspace_id, object_id, for_update=True)
            assert exc.value.orig.sqlstate == "55P03"
            second.rollback()
            first.rollback()
        with Session(engine, info={POLICY_KEY: execution_policy}) as observer:
            counts = _verify_lock_fixture(observer, user_id, workspace_id, object_id)
            # Successful re-acquisition independently proves release after rollback.
            assert repository.get_by_id(
                observer, workspace_id, object_id, for_update=True
            ).phase == "active"
            observer.rollback()
        _durable_record("BIZZI_B4_EVIDENCE_DIR", "LOCK_AND_ROLLBACK_EVIDENCE.json", {
            "identities": identity, "backend_pids": pids, "sqlstate": "55P03",
            "first_transaction": "rolled back", "original_phase": "active",
            "counts": counts, "committed_archive": False,
        })
    finally:
        # No broad finally cleanup: any unknown row/reference prevents deletion.
        if committed_setup:
            with Session(engine, info={POLICY_KEY: execution_policy}) as cleanup:
                counts = _verify_lock_fixture(cleanup, user_id, workspace_id, object_id)
                _durable_record("BIZZI_B4_LEDGER_DIR", "B4_FIXTURE_LEDGER.json", {
                    "executor": _ADMISSION["collector"], "requesting_owner": "Project Owner",
                    "authority": _ADMISSION["operative_permission_id"],
                    "permission_digest": _ADMISSION["operative_permission_sha256"],
                    "preparation_permission": _ADMISSION["preparation_permission_id"],
                    "preparation_digest": _ADMISSION["preparation_source_sha256"],
                    "mode": _ADMISSION["mode"],
                    "candidate_head": _ADMISSION["candidate_head"],
                    "candidate_tree": _ADMISSION.get("candidate_tree"),
                    "decision_digest":
                        "30b02899692ad495bbab2f56df0c18bc1eaa51d984dbb28a05b2c7f6d5ded782",
                    "UTC": datetime.now(UTC).isoformat(), "identities": identity,
                    "destination": {"host": engine.url.host, "port": engine.url.port,
                                    "database": engine.url.database}, "role": engine.url.username,
                    "test_node": "test_two_connections_hold_repository_lock_timeout_then_rollback",
                    "verified_counts": counts, "audit_and_membership_count": 0,
                    "domain_attribution_added": False,
                })
                _durable_record("BIZZI_B4_LEDGER_DIR", "DELETION_INTENT.json", {
                    "UTC": datetime.now(UTC).isoformat(), "identities": identity,
                    "order": ["enterprise_objects", "workspaces", "users"],
                    "authority": _ADMISSION["operative_permission_id"], "status": "intent",
                })
                affected = []
                for model, row_id in [(EnterpriseObject, object_id),
                                      (Workspace, workspace_id), (User, user_id)]:
                    result = cleanup.execute(delete(model).where(model.id == row_id))
                    if result.rowcount != 1:
                        raise RuntimeError("STOP: exact fixture deletion count differs")
                    affected.append({"table": model.__tablename__, "count": result.rowcount})
                cleanup.commit()
                _durable_record("BIZZI_B4_LEDGER_DIR", "DELETION_OUTCOME.json", {
                    "UTC": datetime.now(UTC).isoformat(), "identities": identity,
                    "rows_deleted": affected, "status": "committed",
                })
