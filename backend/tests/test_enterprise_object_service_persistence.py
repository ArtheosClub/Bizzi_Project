"""A-12 acceptance against migrated PostgreSQL; caller-owned transactions.

No migrations are applied here. Connection failure fails these tests rather
than presenting skipped acceptance criteria as a successful delivery.
"""

import json
import os
import uuid
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine, delete, event, func, select, text
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.preproduction_guard import (
    POLICY_KEY,
    require_engine,
    require_session,
    resolve_policy,
)
from app.models import AuditRecord, EnterpriseObject, User, Workspace
from app.repositories import audit_record_repository
from app.repositories import enterprise_object_repository as repository
from app.services.audit_actions import ENTERPRISE_OBJECT_CREATED, ENTERPRISE_OBJECT_UPDATED
from app.services.audit_service import AuditService
from app.services.enterprise_object_service import EnterpriseObjectService as Service


@pytest.fixture(scope="module")
def engine():
    policy = resolve_policy(get_settings().synthetic_execution_profile)
    engine = create_engine(get_settings().database_url, pool_pre_ping=True)
    require_engine(engine, policy)
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    yield engine
    engine.dispose()


@pytest.fixture()
def db(engine, execution_policy):
    with engine.connect() as connection:
        transaction = connection.begin()
        with Session(bind=connection, info={POLICY_KEY: execution_policy}) as session:
            require_session(session)
            user = User()
            session.add(user)
            session.flush()
            workspace = Workspace(name="WP13 acceptance", owner_id=user.id)
            session.add(workspace)
            session.flush()
            yield session, workspace.id, user.id
        if transaction.is_active:
            transaction.rollback()


def create(db):
    session, workspace_id, owner_id = db
    return Service.create(
        session,
        workspace_id=workspace_id,
        type="example",
        owner_id=owner_id,
        actor_context=_test_context(session, workspace_id),
    )


def records(db):
    session, workspace_id, _ = db
    return audit_record_repository.list_by_workspace(session, workspace_id)


def test_create_one_object_and_one_valid_audit(db):
    session, workspace_id, owner_id = db
    object_id = create(db)
    assert isinstance(object_id, uuid.UUID)
    obj = repository.get_by_id(session, workspace_id, object_id)
    assert obj is not None and obj.phase == "active"
    assert obj.type == "example" and obj.owner_id == owner_id
    assert [row.id for row in repository.list_by_workspace(session, workspace_id)] == [object_id]
    audit = records(db)
    assert len(audit) == 1
    assert audit[0].action == ENTERPRISE_OBJECT_CREATED
    assert audit[0].subject_enterprise_object_id == object_id
    assert all(
        getattr(audit[0], name) is None
        for name in (
            "subject_workspace_id",
            "subject_user_id",
            "subject_workspace_membership_id",
            "subject_task_id",
        )
    )
    assert audit[0].content == {
        "workspace_id": [None, str(workspace_id)],
        "type": [None, "example"],
        "owner_id": [None, str(owner_id)],
        "phase": [None, "active"],
    }
    # A fresh identity map verifies that both rows reached the database.
    with Session(
        bind=session.connection(), join_transaction_mode="create_savepoint",
        info={POLICY_KEY: session.info[POLICY_KEY]},
    ) as observer:
        require_session(observer)
        assert observer.get(EnterpriseObject, object_id).phase == "active"
        assert observer.get(AuditRecord, audit[0].id).subject_enterprise_object_id == object_id


def test_archive_unarchive_diffs_in_call_order(db):
    session, workspace_id, _ = db
    object_id = create(db)
    initial_ids = {row.id for row in records(db)}
    assert (
        Service.archive(
            session,
            workspace_id=workspace_id,
            object_id=object_id,
            actor_context=_test_context(session, workspace_id),
        )
        is None
    )
    first = [row for row in records(db) if row.id not in initial_ids]
    assert len(first) == 1
    assert first[0].content == {"phase": ["active", "archived"]}
    assert repository.get_by_id(session, workspace_id, object_id).phase == "archived"
    initial_ids.add(first[0].id)
    assert (
        Service.unarchive(
            session,
            workspace_id=workspace_id,
            object_id=object_id,
            actor_context=_test_context(session, workspace_id),
        )
        is None
    )
    second = [row for row in records(db) if row.id not in initial_ids]
    assert len(second) == 1
    assert second[0].content == {"phase": ["archived", "active"]}
    assert first[0].action == second[0].action == ENTERPRISE_OBJECT_UPDATED
    assert len(records(db)) == 3
    assert repository.get_by_id(session, workspace_id, object_id).phase == "active"


@pytest.mark.parametrize("operation", ["archive", "unarchive"])
def test_cross_workspace_and_missing_identity_are_indistinguishable(db, operation):
    session, workspace_id, owner_id = db
    object_id = create(db)
    other = Workspace(name="Other workspace", owner_id=owner_id)
    session.add(other)
    session.flush()
    assert repository.get_by_id(session, other.id, object_id) is None
    assert repository.list_by_workspace(session, other.id) == []
    messages = []
    for target in (object_id, uuid.uuid4()):
        with pytest.raises(LookupError) as exc:
            getattr(Service, operation)(
                session,
                workspace_id=other.id,
                object_id=target,
                actor_context=_test_context(session, other.id),
            )
        messages.append(str(exc.value))
    assert messages[0] == messages[1]
    assert repository.get_by_id(session, workspace_id, object_id).phase == "active"
    assert len(records(db)) == 1
    assert audit_record_repository.list_by_workspace(session, other.id) == []


@pytest.mark.parametrize(
    "operation,phase",
    [
        ("archive", "archived"),
        ("archive", "superseded"),
        ("unarchive", "active"),
        ("unarchive", "superseded"),
    ],
)
def test_invalid_persisted_transition_has_no_audit(db, monkeypatch, operation, phase):
    session, workspace_id, owner_id = db
    obj = EnterpriseObject(
        workspace_id=workspace_id, owner_id=owner_id, type="example", phase=phase
    )
    assert repository.add(session, obj) is None
    record = Mock()
    monkeypatch.setattr(AuditService, "record", record)
    with pytest.raises(ValueError, match="cannot transition"):
        getattr(Service, operation)(
            session,
            workspace_id=workspace_id,
            object_id=obj.id,
            actor_context=_test_context(session, workspace_id),
        )
    record.assert_not_called()
    session.refresh(obj)
    assert obj.phase == phase and records(db) == []


def test_direct_sql_proves_server_default_without_python_default(db):
    session, workspace_id, owner_id = db
    phase = session.execute(
        text(
            "INSERT INTO enterprise_objects (id, workspace_id, type, owner_id) "
            "VALUES (:id, :workspace, :type, :owner) RETURNING phase"
        ),
        {"id": uuid.uuid4(), "workspace": workspace_id, "type": "example", "owner": owner_id},
    ).scalar_one()
    assert phase == "active"


def test_repository_list_order_and_limit(db):
    session, workspace_id, owner_id = db
    ids = sorted(uuid.uuid4() for _ in range(3))
    for object_id in ids:
        repository.add(
            session,
            EnterpriseObject(
                id=object_id, workspace_id=workspace_id, owner_id=owner_id, type="example"
            ),
        )
    assert [row.id for row in repository.list_by_workspace(session, workspace_id, limit=2)] == ids[
        :0:-1
    ]
    rows = repository.list_by_workspace(session, workspace_id)
    assert len({row.created_at for row in rows}) == 1
    assert [row.id for row in repository.list_by_workspace(session, workspace_id, limit=1)] == ids[
        -1:
    ]


def test_business_constraint_failure_precedes_audit(db, monkeypatch):
    session, workspace_id, owner_id = db
    record = Mock()
    monkeypatch.setattr(AuditService, "record", record)
    with pytest.raises(IntegrityError):
        with session.begin_nested():
            Service.create(
                session,
                workspace_id=workspace_id,
                type=None,  # NOT NULL business constraint after valid attribution
                owner_id=owner_id,
                actor_context=_test_context(session, workspace_id),
            )
    record.assert_not_called()
    assert repository.list_by_workspace(session, workspace_id) == []
    assert records(db) == []


@pytest.mark.parametrize("failure", ["audit_validation", "audit_database", "business_after_audit"])
def test_create_failure_then_caller_rollback_is_not_durable(
    engine, execution_policy, monkeypatch, failure
):
    observed = {}
    original = AuditService.record

    def record(session, **kwargs):
        observed["object_id"] = kwargs["subject"].id
        if failure == "audit_validation":
            kwargs["content"] = {"phase": ["active", "active"]}
        original(session, **kwargs)

    def corrupt_audit(_mapper, _connection, target):
        target.subject_enterprise_object_id = None  # real CHECK violation on flush

    monkeypatch.setattr(AuditService, "record", record)
    if failure == "audit_database":
        event.listen(AuditRecord, "before_insert", corrupt_audit)
    try:
        with Session(engine, info={POLICY_KEY: execution_policy}) as session:
            require_session(session)
            user = User()
            session.add(user)
            session.flush()
            workspace = Workspace(name="Rollback probe", owner_id=user.id)
            session.add(workspace)
            session.flush()
            workspace_id = workspace.id
            expected_error = ValueError if failure == "audit_validation" else IntegrityError
            with pytest.raises(expected_error):
                object_id = Service.create(
                    session,
                    workspace_id=workspace_id,
                    type="example",
                    owner_id=user.id,
                    actor_context=_test_context(session, workspace_id),
                )
                # Both rows have flushed before this subsequent business failure.
                assert len(audit_record_repository.list_by_workspace(session, workspace_id)) == 1
                obj = repository.get_by_id(session, workspace_id, object_id)
                obj.phase = "invalid"
                session.flush()
            session.rollback()
        # Independent connection and transaction: no reliance on the writer's cache.
        with Session(engine, info={POLICY_KEY: execution_policy}) as observer:
            require_session(observer)
            assert observer.get(EnterpriseObject, observed["object_id"]) is None
            assert audit_record_repository.list_by_workspace(observer, workspace_id) == []
    finally:
        if failure == "audit_database":
            event.remove(AuditRecord, "before_insert", corrupt_audit)


@pytest.mark.parametrize("operation,phase", [("archive", "active"), ("unarchive", "archived")])
@pytest.mark.parametrize("failure", ["audit", "business"])
def test_transition_rollback_restores_prior_phase(db, monkeypatch, operation, phase, failure):
    session, workspace_id, owner_id = db
    obj = EnterpriseObject(
        workspace_id=workspace_id, owner_id=owner_id, type="example", phase=phase
    )
    repository.add(session, obj)
    original = AuditService.record

    def fail_after_flush(*args, **kwargs):
        original(*args, **kwargs)
        raise ValueError("audit failure after flush")

    if failure == "audit":
        monkeypatch.setattr(AuditService, "record", fail_after_flush)
    # The caller's savepoint owns rollback, preserving fixture setup.
    with pytest.raises(ValueError):
        with session.begin_nested():
            getattr(Service, operation)(
                session,
                workspace_id=workspace_id,
                object_id=obj.id,
                actor_context=_test_context(session, workspace_id),
            )
            assert len(records(db)) == 1
            raise ValueError("business failure after audit flush")
    session.expire_all()
    assert repository.get_by_id(session, workspace_id, obj.id).phase == phase
    assert records(db) == []


def test_lock_refreshes_stale_loaded_phase(db):
    session, workspace_id, owner_id = db
    obj = EnterpriseObject(workspace_id=workspace_id, owner_id=owner_id, type="example")
    repository.add(session, obj)
    session.execute(
        text("UPDATE enterprise_objects SET phase='archived' WHERE id=:id"), {"id": obj.id}
    )
    assert obj.phase == "active"  # intentionally stale ORM identity map
    Service.unarchive(
        session,
        workspace_id=workspace_id,
        object_id=obj.id,
        actor_context=_test_context(session, workspace_id),
    )
    assert obj.phase == "active"
    assert records(db)[0].content == {"phase": ["archived", "active"]}


def _durable_record(directory_variable, name, value):
    directory = Path(os.environ[directory_variable])
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
                    "executor": "Codex", "requesting_owner": "Project Owner",
                    "authority": "MVP-B4-D-LOCAL-2026-10-07; Block G and Block I",
                    "decision_digest":
                        "30b02899692ad495bbab2f56df0c18bc1eaa51d984dbb28a05b2c7f6d5ded782",
                    "permission_digest":
                        "6dd6312d6125212c7cddc42b7a87a8d154363d27b134af624364a0e48bb195b5",
                    "scope_digest":
                        "ff90b638527a6addf0f86caabaafce950339022192bcaf76f2f60e265745935c",
                    "UTC": datetime.now(UTC).isoformat(), "identities": identity,
                    "destination": "localhost:5433/bizzi_test", "role": "bizzi",
                    "test_node": "test_two_connections_hold_repository_lock_timeout_then_rollback",
                    "verified_counts": counts, "audit_and_membership_count": 0,
                    "domain_attribution_added": False,
                })
                _durable_record("BIZZI_B4_LEDGER_DIR", "DELETION_INTENT.json", {
                    "UTC": datetime.now(UTC).isoformat(), "identities": identity,
                    "order": ["enterprise_objects", "workspaces", "users"],
                    "authority": "Block G Q1-Q4; Block I item 4", "status": "intent",
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


def test_repeated_archive_refused_with_one_pending_audit_then_rollback(db):
    session, workspace_id, owner_id = db
    obj = EnterpriseObject(workspace_id=workspace_id, owner_id=owner_id, type="example")
    repository.add(session, obj)
    context = _test_context(session, workspace_id)
    Service.archive(session, workspace_id=workspace_id, object_id=obj.id, actor_context=context)
    assert repository.get_by_id(session, workspace_id, obj.id).phase == "archived"
    assert len(records(db)) == 1
    assert records(db)[0].action == ENTERPRISE_OBJECT_UPDATED
    with pytest.raises(ValueError, match="cannot transition"):
        Service.archive(session, workspace_id=workspace_id, object_id=obj.id, actor_context=context)
    assert len(records(db)) == 1
    session.rollback()
    assert repository.get_by_id(session, workspace_id, obj.id) is None
    assert records(db) == []
    _durable_record("BIZZI_B4_EVIDENCE_DIR", "REPEATED_TRANSITION_EVIDENCE.json", {
        "archive_calls": 2, "pending_update_audits_before_rollback": 1,
        "second_call": "refused", "after_rollback_object_present": False,
        "after_rollback_audits": 0, "committed_archive": False,
    })


def _test_context(session, workspace_id):
    from app.core.actor_context import ActorContext
    from app.models import WorkspaceMembership

    workspace = session.get(Workspace, workspace_id)
    member = session.scalar(
        select(WorkspaceMembership).where(
            WorkspaceMembership.workspace_id == workspace_id,
            WorkspaceMembership.user_id == workspace.owner_id,
        )
    )
    if member is None:
        member = WorkspaceMembership(
            user_id=workspace.owner_id, workspace_id=workspace_id, role="owner"
        )
        session.add(member)
        session.flush()
    return ActorContext(workspace.owner_id, workspace_id, member.id, "synthetic-eo-test")
