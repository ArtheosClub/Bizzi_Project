"""Trusted request context, bounded ADW-02 records 4/5; not a runtime session."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ActorContext:
    actor_id: UUID
    workspace_id: UUID
    membership_id: UUID
    request_id: str
