"""Actual synthetic database identity resolution, immutable request context."""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.core.errors import AccessDeniedError
from app.models import Workspace, WorkspaceMembership
from app.services.identity_service import IdentityService


def test_context_is_resolved_from_membership(identity_db, owner_graph, verifier):
    user, workspace, member = owner_graph
    context = IdentityService(identity_db, verifier).resolve_actor_context(
        "synthetic-test-token", "req-1"
    )
    assert (context.actor_id, context.workspace_id, context.membership_id) == (
        user.id,
        workspace.id,
        member.id,
    )
    assert context.request_id == "req-1"
    with pytest.raises(FrozenInstanceError):
        context.workspace_id = uuid4()


def test_unknown_identity_rejected(identity_db, verifier):
    with pytest.raises(AccessDeniedError):
        IdentityService(identity_db, verifier).resolve_actor_context("synthetic-test-token", "req")


def test_deactivated_identity_rejected(identity_db, owner_graph, verifier):
    user, _, _ = owner_graph
    user.deactivated_at = datetime.now(UTC)
    identity_db.flush()
    with pytest.raises(AccessDeniedError):
        IdentityService(identity_db, verifier).resolve_actor_context("synthetic-test-token", "req")


def test_no_membership_rejected(identity_db, owner_graph, verifier):
    _, _, member = owner_graph
    identity_db.delete(member)
    identity_db.flush()
    with pytest.raises(AccessDeniedError):
        IdentityService(identity_db, verifier).resolve_actor_context("synthetic-test-token", "req")


def test_multiple_memberships_rejected(identity_db, owner_graph, verifier):
    user, _, _ = owner_graph
    workspace = Workspace(id=uuid4(), name="Synthetic second", owner_id=user.id)
    identity_db.add(workspace)
    identity_db.flush()
    identity_db.add(WorkspaceMembership(user_id=user.id, workspace_id=workspace.id, role="owner"))
    identity_db.flush()
    with pytest.raises(AccessDeniedError):
        IdentityService(identity_db, verifier).resolve_actor_context("synthetic-test-token", "req")
