"""Token verifier boundary. No provider, parsing, cryptography or fallback.

Record 5 permits only an injected claims-checking TEST double. A production
signature verifier needs its own Supabase/dependency scope. Default is deny.
"""

from dataclasses import dataclass
from typing import Protocol

from app.core.errors import UnauthenticatedError


@dataclass(frozen=True, slots=True)
class VerifiedIdentity:
    issuer: str
    subject: str


class TokenVerifier(Protocol):
    def verify(self, token: str) -> VerifiedIdentity:
        """Verify admitted claims or raise UnauthenticatedError."""
        ...


class RejectingTokenVerifier:
    def verify(self, token: str) -> VerifiedIdentity:
        raise UnauthenticatedError()


def authenticate(token: str | None, verifier: TokenVerifier) -> VerifiedIdentity:
    if not isinstance(token, str) or not token:
        raise UnauthenticatedError()
    identity = verifier.verify(token)
    if not isinstance(identity, VerifiedIdentity) or not identity.issuer or not identity.subject:
        raise UnauthenticatedError()
    return identity
