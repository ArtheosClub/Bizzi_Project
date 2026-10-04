"""Required ordinary attribution and dedicated bootstrap action separation."""

from dataclasses import replace
from uuid import uuid4

import pytest

from app.core.actor_context import ActorContext
from app.core.errors import AccessDeniedError
from app.models import AuditRecord, EnterpriseObject
from app.services.audit_actions import BOOTSTRAP_ACTIONS, ENTERPRISE_OBJECT_CREATED
from app.services.audit_service import AuditService


def test_attributed_mutation(identity_db, owner_graph):
    user, workspace, member = owner_graph
    obj = EnterpriseObject(workspace_id=workspace.id, owner_id=user.id, type="synthetic")
    identity_db.add(obj)
    identity_db.flush()
    ctx = ActorContext(user.id, workspace.id, member.id, "synthetic-req")
    AuditService.record(
        identity_db,
        subject=obj,
        action=ENTERPRISE_OBJECT_CREATED,
        content={"type": [None, "synthetic"]},
        actor_context=ctx,
    )
    from sqlalchemy import select

    audit = identity_db.scalar(
        select(AuditRecord).where(AuditRecord.subject_enterprise_object_id == obj.id)
    )
    assert audit.actor_id == user.id and audit.membership_id == member.id


def test_missing_actor_rejected_without_audit(identity_db, owner_graph):
    user, workspace, _ = owner_graph
    obj = EnterpriseObject(workspace_id=workspace.id, owner_id=user.id, type="synthetic")
    identity_db.add(obj)
    identity_db.flush()
    with pytest.raises(ValueError, match="requires actor"):
        AuditService.record(
            identity_db,
            subject=obj,
            action=ENTERPRISE_OBJECT_CREATED,
            content={"type": [None, "synthetic"]},
        )
    from sqlalchemy import select

    assert list(identity_db.scalars(select(AuditRecord))) == []


@pytest.mark.parametrize("action", sorted(BOOTSTRAP_ACTIONS))
def test_ordinary_record_refuses_bootstrap_action(action):
    with pytest.raises(ValueError, match="dedicated bootstrap"):
        AuditService.record(
            None, subject=EnterpriseObject(), action=action, content={"id": [None, "x"]}
        )


@pytest.mark.parametrize("field", ["actor_id", "workspace_id", "membership_id"])
def test_forged_attribution_rejected_without_audit(identity_db, owner_graph, field):
    from sqlalchemy import select

    user, workspace, member = owner_graph
    obj = EnterpriseObject(workspace_id=workspace.id, owner_id=user.id, type="synthetic")
    identity_db.add(obj)
    identity_db.flush()
    ctx = replace(
        ActorContext(user.id, workspace.id, member.id, "synthetic-req"), **{field: uuid4()}
    )
    with pytest.raises((ValueError, AccessDeniedError)):
        AuditService.record(
            identity_db,
            subject=obj,
            action=ENTERPRISE_OBJECT_CREATED,
            content={"type": [None, "synthetic"]},
            actor_context=ctx,
        )
    assert list(identity_db.scalars(select(AuditRecord))) == []
