"""Owner policy rejects forged context, wrong resource and stale membership."""

from dataclasses import replace
from uuid import uuid4

import pytest

from app.core.errors import AccessDeniedError
from app.services.identity_service import IdentityService


def test_owner_access(identity_db, owner_graph, verifier):
    _, workspace, _ = owner_graph
    service = IdentityService(identity_db, verifier)
    context = service.resolve_actor_context("synthetic-test-token", "req")
    service.authorize(context, workspace.id)


@pytest.mark.parametrize("field", ["actor_id", "workspace_id", "membership_id"])
def test_forged_context_rejected(field, identity_db, owner_graph, verifier):
    _, workspace, _ = owner_graph
    service = IdentityService(identity_db, verifier)
    context = service.resolve_actor_context("synthetic-test-token", "req")
    with pytest.raises(AccessDeniedError):
        service.authorize(replace(context, **{field: uuid4()}), workspace.id)


def test_other_workspace_rejected(identity_db, owner_graph, verifier):
    service = IdentityService(identity_db, verifier)
    context = service.resolve_actor_context("synthetic-test-token", "req")
    with pytest.raises(AccessDeniedError):
        service.authorize(context, uuid4())


def test_removed_membership_rejected(identity_db, owner_graph, verifier):
    _, workspace, member = owner_graph
    service = IdentityService(identity_db, verifier)
    context = service.resolve_actor_context("synthetic-test-token", "req")
    identity_db.delete(member)
    identity_db.flush()
    with pytest.raises(AccessDeniedError):
        service.authorize(context, workspace.id)


def test_workspace_owner_mismatch_rejected(identity_db, owner_graph, verifier):
    from app.models import User

    _, workspace, _ = owner_graph
    other = User(auth_issuer="synthetic-issuer", auth_subject="synthetic-other")
    identity_db.add(other)
    identity_db.flush()
    workspace.owner_id = other.id
    identity_db.flush()
    with pytest.raises(AccessDeniedError):
        IdentityService(identity_db, verifier).resolve_actor_context("synthetic-test-token", "req")


def test_new_denial_contract():
    from app.core.errors import UnauthenticatedError

    assert (UnauthenticatedError.http_status, UnauthenticatedError.code) == (401, "unauthenticated")
    assert (AccessDeniedError.http_status, AccessDeniedError.code) == (404, "not_found")
