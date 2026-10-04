"""Bootstrap authentication through synthetic verifier; rollback-bound pytest only."""

import pytest
from sqlalchemy import func, select

from app.cli.bootstrap_owner import bootstrap_owner
from app.core.errors import UnauthenticatedError
from app.models import AuditRecord, User, Workspace, WorkspaceMembership


def _counts(db):
    return [
        db.scalar(select(func.count()).select_from(model))
        for model in (User, Workspace, WorkspaceMembership, AuditRecord)
    ]


def test_cli_wrapper_creates_verified_owner(identity_db, verifier):
    result = bootstrap_owner(
        identity_db, token="synthetic-test-token", verifier=verifier, workspace_name="Synthetic CLI"
    )
    user = identity_db.get(User, result.user_id)
    assert (user.auth_issuer, user.auth_subject) == ("synthetic-issuer", "synthetic-owner")
    assert _counts(identity_db) == [1, 1, 1, 3]


@pytest.mark.parametrize("token", [None, "", "invalid-token"])
def test_missing_or_invalid_token_writes_nothing(identity_db, verifier, token):
    with pytest.raises(UnauthenticatedError):
        bootstrap_owner(identity_db, token=token, verifier=verifier, workspace_name="Synthetic")
    assert _counts(identity_db) == [0, 0, 0, 0]


@pytest.mark.parametrize(
    "field,value", [("exp", 0), ("iss", "wrong-issuer"), ("aud", "wrong-audience"), ("sub", "")]
)
def test_invalid_claims_write_nothing(identity_db, verifier, field, value):
    verifier.claims[field] = value
    with pytest.raises(UnauthenticatedError):
        bootstrap_owner(
            identity_db, token="synthetic-test-token", verifier=verifier, workspace_name="Synthetic"
        )
    assert _counts(identity_db) == [0, 0, 0, 0]


def test_default_verifier_rejects_without_writes(identity_db):
    with pytest.raises(UnauthenticatedError):
        bootstrap_owner(identity_db, token="synthetic-test-token", workspace_name="Synthetic")
    assert _counts(identity_db) == [0, 0, 0, 0]
