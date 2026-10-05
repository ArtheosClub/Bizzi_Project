"""Prospective record-5 create-only verification; original excluded candidate tests retained.

No migrations are applied here. Connection failure fails these tests rather
than presenting skipped acceptance criteria as a successful delivery.
"""

import uuid
from datetime import UTC
from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine, delete, event, text
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import AuditRecord, EnterpriseObject, Task, User, Workspace
from app.repositories import audit_record_repository
from app.repositories import task_repository as repository
from app.services.audit_actions import TASK_CREATED, TASK_UPDATED
from app.services.audit_service import AuditService
from app.services.task_service import TaskService as Service


@pytest.fixture(scope="module")
def engine():
    engine = create_engine(get_settings().database_url, pool_pre_ping=True)
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    yield engine
    engine.dispose()


@pytest.fixture()
def db(engine):
    with engine.connect() as connection:
        transaction = connection.begin()
        with Session(bind=connection) as session:
            user = User()
            session.add(user)
            session.flush()
            workspace = Workspace(name="WP15 acceptance", owner_id=user.id)
            session.add(workspace)
            session.flush()
            yield session, workspace.id, user.id
        if transaction.is_active:
            transaction.rollback()


def create(db):
    session, workspace_id, owner_id = db
    return Service.create(session, workspace_id=workspace_id)


def records(db):
    session, workspace_id, _ = db
    return audit_record_repository.list_by_workspace(session, workspace_id)


def test_create_one_object_and_one_valid_audit(db):
    session, workspace_id, owner_id = db
    task_id = create(db)
    assert isinstance(task_id, uuid.UUID)
    obj = repository.get_by_id(session, workspace_id, task_id)
    assert obj is not None and obj.phase == "active"
    assert obj.source_object_id is None
    assert [row.id for row in repository.list_by_workspace(session, workspace_id)] == [task_id]
    audit = records(db)
    assert len(audit) == 1
    assert audit[0].action == TASK_CREATED
    assert audit[0].subject_task_id == task_id
    assert all(
        getattr(audit[0], name) is None
        for name in (
            "subject_workspace_id",
            "subject_user_id",
            "subject_workspace_membership_id",
            "subject_enterprise_object_id",
        )
    )
    assert audit[0].content == {
        "workspace_id": [None, str(workspace_id)],
        "phase": [None, "active"],
    }
    # A fresh identity map verifies that both rows reached the database.
    with Session(bind=session.connection(), join_transaction_mode="create_savepoint") as observer:
        assert observer.get(Task, task_id).phase == "active"
        assert observer.get(AuditRecord, audit[0].id).subject_task_id == task_id


def test_archive_unarchive_diffs_in_call_order(db):
    session, workspace_id, _ = db
    task_id = create(db)
    initial_ids = {row.id for row in records(db)}
    assert Service.archive(session, workspace_id=workspace_id, task_id=task_id) is None
    first = [row for row in records(db) if row.id not in initial_ids]
    assert len(first) == 1
    assert first[0].content == {"phase": ["active", "archived"]}
    assert repository.get_by_id(session, workspace_id, task_id).phase == "archived"
    initial_ids.add(first[0].id)
    assert Service.unarchive(session, workspace_id=workspace_id, task_id=task_id) is None
    second = [row for row in records(db) if row.id not in initial_ids]
    assert len(second) == 1
    assert second[0].content == {"phase": ["archived", "active"]}
    assert first[0].action == second[0].action == TASK_UPDATED
    assert len(records(db)) == 3
    assert repository.get_by_id(session, workspace_id, task_id).phase == "active"


@pytest.mark.parametrize("operation", ["archive", "unarchive"])
def test_cross_workspace_and_missing_identity_are_indistinguishable(db, operation):
    session, workspace_id, owner_id = db
    task_id = create(db)
    other = Workspace(name="Other workspace", owner_id=owner_id)
    session.add(other)
    session.flush()
    assert repository.get_by_id(session, other.id, task_id) is None
    assert repository.list_by_workspace(session, other.id) == []
    messages = []
    for target in (task_id, uuid.uuid4()):
        with pytest.raises(LookupError) as exc:
            getattr(Service, operation)(session, workspace_id=other.id, task_id=target)
        messages.append(str(exc.value))
    assert messages[0] == messages[1]
    assert repository.get_by_id(session, workspace_id, task_id).phase == "active"
    assert len(records(db)) == 1
    assert audit_record_repository.list_by_workspace(session, other.id) == []


@pytest.mark.parametrize(
    "operation,phase",
    [
        ("archive", "archived"),
        ("archive", "superseded"),
        ("unarchive", "active"),
        ("unarchive", "superseded"),
        ("archive", "completed"),
        ("archive", "cancelled"),
        ("unarchive", "completed"),
        ("unarchive", "cancelled"),
    ],
)
def test_invalid_persisted_transition_has_no_audit(db, monkeypatch, operation, phase):
    session, workspace_id, owner_id = db
    obj = Task(workspace_id=workspace_id, phase=phase)
    assert repository.add(session, obj) is None
    record = Mock()
    monkeypatch.setattr(AuditService, "record", record)
    with pytest.raises(ValueError, match="cannot transition"):
        getattr(Service, operation)(session, workspace_id=workspace_id, task_id=obj.id)
    record.assert_not_called()
    session.refresh(obj)
    assert obj.phase == phase and records(db) == []


def test_repository_list_order_and_limit(db):
    session, workspace_id, owner_id = db
    ids = sorted(uuid.uuid4() for _ in range(3))
    for task_id in ids:
        repository.add(
            session,
            Task(id=task_id, workspace_id=workspace_id),
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
    session, workspace_id, _ = db
    record = Mock()
    monkeypatch.setattr(AuditService, "record", record)
    with pytest.raises(IntegrityError):
        with session.begin_nested():
            Service.create(session, workspace_id=uuid.uuid4())
    record.assert_not_called()
    assert repository.list_by_workspace(session, workspace_id) == []
    assert records(db) == []


@pytest.mark.parametrize("failure", ["audit_validation", "audit_database", "business_after_audit"])
def test_create_failure_then_caller_rollback_is_not_durable(engine, monkeypatch, failure):
    observed = {}
    original = AuditService.record

    def record(session, **kwargs):
        observed["task_id"] = kwargs["subject"].id
        if failure == "audit_validation":
            kwargs["content"] = {"phase": ["active", "active"]}
        original(session, **kwargs)

    def corrupt_audit(_mapper, _connection, target):
        target.subject_task_id = None  # real CHECK violation on flush

    monkeypatch.setattr(AuditService, "record", record)
    if failure == "audit_database":
        event.listen(AuditRecord, "before_insert", corrupt_audit)
    try:
        with Session(engine) as session:
            user = User()
            session.add(user)
            session.flush()
            workspace = Workspace(name="Rollback probe", owner_id=user.id)
            session.add(workspace)
            session.flush()
            workspace_id = workspace.id
            expected_error = ValueError if failure == "audit_validation" else IntegrityError
            with pytest.raises(expected_error):
                task_id = Service.create(session, workspace_id=workspace_id)
                # Both rows have flushed before this subsequent business failure.
                assert len(audit_record_repository.list_by_workspace(session, workspace_id)) == 1
                obj = repository.get_by_id(session, workspace_id, task_id)
                obj.phase = "invalid"
                session.flush()
            session.rollback()
        # Independent connection and transaction: no reliance on the writer's cache.
        with Session(engine) as observer:
            assert observer.get(Task, observed["task_id"]) is None
            assert audit_record_repository.list_by_workspace(observer, workspace_id) == []
    finally:
        if failure == "audit_database":
            event.remove(AuditRecord, "before_insert", corrupt_audit)


@pytest.mark.parametrize("operation,phase", [("archive", "active"), ("unarchive", "archived")])
@pytest.mark.parametrize("failure", ["audit", "business"])
def test_transition_rollback_restores_prior_phase(db, monkeypatch, operation, phase, failure):
    session, workspace_id, owner_id = db
    obj = Task(workspace_id=workspace_id, phase=phase)
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
            getattr(Service, operation)(session, workspace_id=workspace_id, task_id=obj.id)
            assert len(records(db)) == 1
            raise ValueError("business failure after audit flush")
    session.expire_all()
    assert repository.get_by_id(session, workspace_id, obj.id).phase == phase
    assert records(db) == []


def test_lock_refreshes_stale_loaded_phase(db):
    session, workspace_id, owner_id = db
    obj = Task(workspace_id=workspace_id)
    repository.add(session, obj)
    session.execute(text("UPDATE tasks SET phase='archived' WHERE id=:id"), {"id": obj.id})
    assert obj.phase == "active"  # intentionally stale ORM identity map
    Service.unarchive(session, workspace_id=workspace_id, task_id=obj.id)
    assert obj.phase == "active"
    assert records(db)[0].content == {"phase": ["archived", "active"]}


def test_two_connections_serialize_archive_and_reject_repeated_transition(engine):
    # This test commits its own UUID-isolated setup; finally removes only those rows.
    user_id, workspace_id = uuid.uuid4(), uuid.uuid4()
    task_id = None
    try:
        with Session(engine) as setup:
            setup.add(User(id=user_id))
            setup.flush()
            setup.add(Workspace(id=workspace_id, name="WP15 lock probe", owner_id=user_id))
            setup.flush()
            task_id = Service.create(setup, workspace_id=workspace_id)
            setup.commit()
        with Session(engine) as first, Session(engine) as second:
            assert first.scalar(text("SELECT pg_backend_pid()")) != second.scalar(
                text("SELECT pg_backend_pid()")
            )
            Service.archive(first, workspace_id=workspace_id, task_id=task_id)
            second.execute(text("SET LOCAL lock_timeout = '200ms'"))
            with pytest.raises(OperationalError) as exc:
                Service.archive(second, workspace_id=workspace_id, task_id=task_id)
            assert exc.value.orig.sqlstate == "55P03"
            second.rollback()
            first.commit()
            with pytest.raises(ValueError, match="cannot transition"):
                Service.archive(second, workspace_id=workspace_id, task_id=task_id)
            second.rollback()
        with Session(engine) as observer:
            assert repository.get_by_id(observer, workspace_id, task_id).phase == "archived"
            audit = audit_record_repository.list_by_workspace(observer, workspace_id)
            assert len(audit) == 2
            assert sum(row.action == TASK_UPDATED for row in audit) == 1
    finally:
        with Session(engine) as cleanup:
            cleanup.execute(delete(AuditRecord).where(AuditRecord.workspace_id == workspace_id))
            cleanup.execute(delete(Task).where(Task.workspace_id == workspace_id))
            cleanup.execute(delete(Workspace).where(Workspace.id == workspace_id))
            cleanup.execute(delete(User).where(User.id == user_id))
            cleanup.commit()


def test_non_null_source_does_not_persist_task_or_audit(db):
    session, workspace_id, _ = db
    with pytest.raises(ValueError, match="R9 authority"):
        Service.create(session, workspace_id=workspace_id, source_object_id=uuid.uuid4())
    assert repository.list_by_workspace(session, workspace_id) == []
    assert records(db) == []


def test_existing_linked_task_remains_readable_and_phase_change_preserves_source(db):
    session, workspace_id, owner_id = db
    source = EnterpriseObject(workspace_id=workspace_id, owner_id=owner_id, type="historical")
    session.add(source)
    session.flush()
    task = Task(workspace_id=workspace_id, source_object_id=source.id)
    repository.add(session, task)
    assert repository.get_by_id(session, workspace_id, task.id).source_object_id == source.id
    assert repository.list_by_workspace(session, workspace_id)[0].id == task.id
    Service.archive(session, workspace_id=workspace_id, task_id=task.id)
    Service.unarchive(session, workspace_id=workspace_id, task_id=task.id)
    session.refresh(task)
    session.refresh(source)
    assert task.source_object_id == source.id and task.phase == "active"
    assert source.phase == "active"
    assert len(records(db)) == 2
    assert all(
        row.subject_task_id == task.id and set(row.content) == {"phase"} for row in records(db)
    )


# Stage 3 selects only the explicitly named create-only tests below.
# Never select the preserved archive/unarchive/read/list/committing tests above.
def _stage3_context(db, verifier):
    from app.services.identity_service import IdentityService

    return IdentityService(db, verifier).resolve_actor_context(
        "synthetic-test-token", "synthetic-stage3-request"
    )


def _stage3_counts(db):
    from sqlalchemy import func, select

    return [db.scalar(select(func.count()).select_from(model)) for model in (Task, AuditRecord)]


def test_stage3_create_has_phase_scope_and_attributed_audit(identity_db, owner_graph, verifier):
    from sqlalchemy import select

    user, workspace, member = owner_graph
    ctx = _stage3_context(identity_db, verifier)
    task_id = Service.create(identity_db, workspace_id=workspace.id, actor_context=ctx)
    # Stored-row assertions, not repository read/list or endpoint invocation.
    task = identity_db.get(Task, task_id)
    audit = identity_db.scalar(select(AuditRecord).where(AuditRecord.subject_task_id == task_id))
    assert isinstance(task_id, uuid.UUID)
    assert task.phase == "active" and task.workspace_id == workspace.id
    assert task.source_object_id is None
    assert (audit.actor_id, audit.membership_id, audit.workspace_id) == (
        user.id,
        member.id,
        workspace.id,
    )
    assert audit.action == TASK_CREATED and audit.subject_task_id == task_id
    assert audit.content == {"workspace_id": [None, str(workspace.id)], "phase": [None, "active"]}
    assert _stage3_counts(identity_db) == [1, 1]


@pytest.mark.parametrize(
    "field", ["missing", "actor_id", "workspace_id", "membership_id", "request_id"]
)
def test_stage3_missing_or_forged_actor_writes_nothing(identity_db, owner_graph, verifier, field):
    from dataclasses import replace

    from app.core.errors import AccessDeniedError

    _, workspace, _ = owner_graph
    ctx = _stage3_context(identity_db, verifier)
    bad = (
        None
        if field == "missing"
        else replace(ctx, **{field: "" if field == "request_id" else uuid.uuid4()})
    )
    with pytest.raises((ValueError, AccessDeniedError)):
        Service.create(identity_db, workspace_id=workspace.id, actor_context=bad)
    assert _stage3_counts(identity_db) == [0, 0]


def test_stage3_cross_workspace_create_refused(identity_db, owner_graph, verifier):
    from app.core.errors import AccessDeniedError

    ctx = _stage3_context(identity_db, verifier)
    other_user = User(auth_issuer="synthetic-issuer", auth_subject="other-synthetic-owner")
    identity_db.add(other_user)
    identity_db.flush()
    other = Workspace(name="Synthetic isolation fixture", owner_id=other_user.id)
    identity_db.add(other)
    identity_db.flush()
    with pytest.raises((ValueError, AccessDeniedError)):
        Service.create(identity_db, workspace_id=other.id, actor_context=ctx)
    assert _stage3_counts(identity_db) == [0, 0]


def test_stage3_deactivated_actor_refused(identity_db, owner_graph, verifier):
    from datetime import datetime

    user, workspace, _ = owner_graph
    ctx = _stage3_context(identity_db, verifier)
    user.deactivated_at = datetime.now(UTC)
    identity_db.flush()
    with pytest.raises(ValueError, match="actor attribution"):
        Service.create(identity_db, workspace_id=workspace.id, actor_context=ctx)
    assert _stage3_counts(identity_db) == [0, 0]


def test_stage3_source_reference_refused(identity_db, owner_graph, verifier):
    _, workspace, _ = owner_graph
    ctx = _stage3_context(identity_db, verifier)
    with pytest.raises(ValueError, match="R9 authority"):
        Service.create(
            identity_db, workspace_id=workspace.id, actor_context=ctx, source_object_id=uuid.uuid4()
        )
    assert _stage3_counts(identity_db) == [0, 0]


@pytest.mark.parametrize(
    "failure", ["task_insert", "audit_validation", "audit_insert", "after_audit"]
)
def test_stage3_failure_rolls_back_task_and_audit(
    identity_db, owner_graph, verifier, monkeypatch, failure
):
    _, workspace, _ = owner_graph
    ctx = _stage3_context(identity_db, verifier)
    original = AuditService.record

    def invalid_content(session, **kwargs):
        kwargs["content"] = {"phase": ["active", "active"]}
        return original(session, **kwargs)

    def fail_task(mapper, connection, target):
        raise ValueError("synthetic task insert failure")

    def fail_audit(mapper, connection, target):
        target.subject_task_id = None  # actual exactly-one CHECK failure

    if failure == "audit_validation":
        monkeypatch.setattr(AuditService, "record", invalid_content)
    if failure == "task_insert":
        event.listen(Task, "before_insert", fail_task)
    if failure == "audit_insert":
        event.listen(AuditRecord, "before_insert", fail_audit)
    try:
        expected = IntegrityError if failure == "audit_insert" else ValueError
        with pytest.raises(expected):
            with identity_db.begin_nested():
                Service.create(identity_db, workspace_id=workspace.id, actor_context=ctx)
                assert _stage3_counts(identity_db) == [1, 1]
                raise ValueError("synthetic caller failure after audit")
    finally:
        if failure == "task_insert":
            event.remove(Task, "before_insert", fail_task)
        if failure == "audit_insert":
            event.remove(AuditRecord, "before_insert", fail_audit)
    assert _stage3_counts(identity_db) == [0, 0]
