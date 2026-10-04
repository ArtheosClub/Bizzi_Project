"""Synthetic claims verifier boundary; no cryptography or provider calls."""

import pytest

from app.core.authentication import RejectingTokenVerifier, authenticate
from app.core.errors import UnauthenticatedError


def test_valid_synthetic_identity(verifier):
    identity = authenticate("synthetic-test-token", verifier)
    assert identity.subject == "synthetic-owner"


@pytest.mark.parametrize("token", [None, "", "unknown-token"])
def test_missing_or_invalid_token_rejected(token, verifier):
    with pytest.raises(UnauthenticatedError):
        authenticate(token, verifier)


@pytest.mark.parametrize(
    "field,value",
    [
        ("iss", "wrong"),
        ("aud", "wrong"),
        ("exp", 0),
        ("exp", "future"),
        ("exp", float("nan")),
        ("exp", float("inf")),
        ("sub", ""),
        ("sub", None),
    ],
)
def test_invalid_claims_rejected(field, value, verifier):
    verifier.claims[field] = value
    with pytest.raises(UnauthenticatedError):
        authenticate("synthetic-test-token", verifier)


def test_default_verifier_has_no_fallback():
    with pytest.raises(UnauthenticatedError):
        authenticate("synthetic-test-token", RejectingTokenVerifier())
