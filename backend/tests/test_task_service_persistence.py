"""Create/add verification; full-file execution under record-5 amendment 4."""

import uuid

import pytest
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

from app.models import AuditRecord, Task, User, Workspace
from app.services.audit_actions import TASK_CREATED
from app.services.audit_service import AuditService
from app.services.task_service import TaskService as Service


def _stage3_context(db, verifier):
    from app.services.identity_service import IdentityService

    return IdentityService(db, verifier).resolve_actor_context(
        "synthetic-test-token", "synthetic-stage3-request"
    )


def _stage3_counts(db):
    from sqlalchemy import func, select

    return [db.scalar(select(func.count()).select_from(model)) for model in (Task, AuditRecord)]


def test_create_one_object_and_one_valid_audit(identity_db, owner_graph, verifier):
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
    assert all(
        getattr(audit, column) is None
        for column in (
            "subject_workspace_id",
            "subject_user_id",
            "subject_workspace_membership_id",
            "subject_enterprise_object_id",
        )
    )
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
    from datetime import UTC, datetime

    user, workspace, _ = owner_graph
    ctx = _stage3_context(identity_db, verifier)
    user.deactivated_at = datetime.now(UTC)
    identity_db.flush()
    with pytest.raises(ValueError, match="actor attribution"):
        Service.create(identity_db, workspace_id=workspace.id, actor_context=ctx)
    assert _stage3_counts(identity_db) == [0, 0]


def test_non_null_source_does_not_persist_task_or_audit(identity_db, owner_graph, verifier):
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


def test_repository_add_flushes_without_ending_transaction(identity_db, owner_graph):
    from app.repositories.task_repository import add

    _, workspace, _ = owner_graph
    task = Task(workspace_id=workspace.id)
    assert add(identity_db, task) is None
    assert isinstance(task.id, uuid.UUID)
    assert identity_db.in_transaction()
    assert _stage3_counts(identity_db) == [1, 0]
