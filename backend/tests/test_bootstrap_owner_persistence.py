"""Record 4b linkage, fresh-subject refusal and six-row atomic rollback."""

from uuid import uuid4

import pytest
from sqlalchemy import event, func, select
from sqlalchemy.exc import IntegrityError

from app.core.authentication import authenticate
from app.models import AuditRecord, User, Workspace, WorkspaceMembership
from app.services.audit_actions import (
    BOOTSTRAP_ACTIONS,
    MEMBERSHIP_BOOTSTRAP_CREATED,
    USER_BOOTSTRAP_CREATED,
    WORKSPACE_BOOTSTRAP_CREATED,
)
from app.services.audit_service import AuditService
from app.services.bootstrap_service import BootstrapService


def _counts(db):
    return [
        db.scalar(select(func.count()).select_from(m))
        for m in (User, Workspace, WorkspaceMembership, AuditRecord)
    ]


def _create(db, verifier):
    if not db.in_transaction():
        db.begin()  # caller explicitly opens Session transaction within fixture rollback
    return BootstrapService.create_owner(
        db,
        identity=authenticate("synthetic-test-token", verifier),
        workspace_name="Synthetic bootstrap",
    )


def test_saved_record_linkage_query(identity_db, verifier):
    result = _create(identity_db, verifier)
    # Verification query of stored records; no reliance on returned ORM objects.
    rows = list(
        identity_db.scalars(
            select(AuditRecord).where(
                AuditRecord.workspace_id == result.workspace_id,
                AuditRecord.action.in_(BOOTSTRAP_ACTIONS),
            )
        )
    )
    assert len(rows) == 3
    by_action = {x.action: x for x in rows}
    u, w, m = [
        by_action[a]
        for a in (USER_BOOTSTRAP_CREATED, WORKSPACE_BOOTSTRAP_CREATED, MEMBERSHIP_BOOTSTRAP_CREATED)
    ]
    assert u.subject_user_id == result.user_id
    assert w.subject_workspace_id == w.workspace_id == result.workspace_id
    assert w.content["owner_id"] == [None, str(u.subject_user_id)]
    assert m.content["user_id"] == [None, str(u.subject_user_id)]
    assert m.content["workspace_id"] == [None, str(result.workspace_id)]
    assert m.content["role"] == [None, "owner"]
    assert len({x.created_at for x in rows}) == 1  # auxiliary only, NOT xact-id proof
    assert all(x.actor_id is None for x in rows)
    assert _counts(identity_db) == [1, 1, 1, 3]


@pytest.mark.parametrize("step", range(1, 7))
def test_failure_each_insert_rolls_back_all_six_rows(identity_db, step, verifier):
    seen = 0

    def fail(mapper, connection, target):
        nonlocal seen
        seen += 1
        if seen == step:
            raise ValueError("synthetic injected failure")

    models = (User, Workspace, WorkspaceMembership, AuditRecord)
    for model in models:
        event.listen(model, "before_insert", fail)
    try:
        with pytest.raises(ValueError, match="synthetic injected"):
            with identity_db.begin_nested():
                _create(identity_db, verifier)
    finally:
        for model in models:
            event.remove(model, "before_insert", fail)
    assert _counts(identity_db) == [0, 0, 0, 0]


@pytest.mark.parametrize("kind", ["user", "workspace", "membership"])
def test_preexisting_subject_refused_even_without_audit(identity_db, owner_graph, kind):
    old_user, old_workspace, old_member = owner_graph
    before = _counts(identity_db)
    with pytest.raises(ValueError, match="existed before"):
        with identity_db.begin_nested():
            user = User(id=uuid4(), auth_issuer="synthetic-issuer", auth_subject="new")
            workspace = Workspace(id=uuid4(), name="New", owner_id=user.id)
            member = WorkspaceMembership(
                id=uuid4(), user_id=user.id, workspace_id=workspace.id, role="owner"
            )
            objects = {"user": user, "workspace": workspace, "membership": member}
            objects[kind] = {
                "user": old_user,
                "workspace": old_workspace,
                "membership": old_member,
            }[kind]
            identity_db.add_all(
                [x for x in objects.values() if x not in (old_user, old_workspace, old_member)]
            )
            AuditService.record_bootstrap(identity_db, **objects)
    assert _counts(identity_db) == before


def test_partial_unique_index_refuses_duplicate_action(identity_db, verifier):
    result = _create(identity_db, verifier)
    row = identity_db.scalar(
        select(AuditRecord).where(AuditRecord.action == USER_BOOTSTRAP_CREATED)
    )
    with pytest.raises(IntegrityError):
        with identity_db.begin_nested():
            identity_db.add(
                AuditRecord(
                    workspace_id=result.workspace_id,
                    action=row.action,
                    subject_user_id=result.user_id,
                    content={"id": [None, str(result.user_id)]},
                )
            )
            identity_db.flush()
    assert _counts(identity_db) == [1, 1, 1, 3]
