import os
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.authentication import VerifiedIdentity
from app.core.errors import UnauthenticatedError
from app.core.preproduction_guard import require_test_destination
from app.models import User, Workspace, WorkspaceMembership

load_dotenv(Path(__file__).resolve().parent.parent / ".env.test")

# Record 5: fail closed BEFORE importing/collecting database test modules.
require_test_destination(os.environ.get("DATABASE_URL", ""))


class SyntheticClaimsVerifier:
    """Opaque test-token lookup plus claims checks; NO signature verification."""

    def __init__(self, claims: dict[str, object]) -> None:
        self.claims = dict(claims)

    def verify(self, token: str) -> VerifiedIdentity:
        claims = self.claims
        now = datetime.now(UTC).timestamp()
        expiry = claims.get("exp")
        if (
            token != "synthetic-test-token"
            or claims.get("iss") != "synthetic-issuer"
            or claims.get("aud") != "synthetic-audience"
            or not isinstance(expiry, (int, float))
            or isinstance(expiry, bool)
            or not now < expiry < float("inf")
            or not isinstance(claims.get("sub"), str)
            or not claims["sub"]
        ):
            raise UnauthenticatedError()
        return VerifiedIdentity("synthetic-issuer", str(claims["sub"]))


@pytest.fixture
def verifier() -> SyntheticClaimsVerifier:
    return SyntheticClaimsVerifier(
        {
            "iss": "synthetic-issuer",
            "aud": "synthetic-audience",
            "exp": datetime.now(UTC).timestamp() + 300,
            "sub": "synthetic-owner",
        }
    )


@pytest.fixture
def identity_db():  # type: ignore[no-untyped-def]
    engine = create_engine(os.environ["DATABASE_URL"])
    with engine.connect() as connection:
        transaction = connection.begin()
        with Session(bind=connection) as db:
            yield db
        transaction.rollback()
    engine.dispose()


@pytest.fixture
def owner_graph(identity_db: Session):  # type: ignore[no-untyped-def]
    user = User(id=uuid4(), auth_issuer="synthetic-issuer", auth_subject="synthetic-owner")
    identity_db.add(user)
    identity_db.flush()
    workspace = Workspace(id=uuid4(), name="Synthetic workspace", owner_id=user.id)
    identity_db.add(workspace)
    identity_db.flush()
    membership = WorkspaceMembership(
        id=uuid4(),
        user_id=user.id,
        workspace_id=workspace.id,
        role="owner",
    )
    identity_db.add(membership)
    identity_db.flush()
    return user, workspace, membership
