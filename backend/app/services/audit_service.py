"""AuditService -- the WP19 / A-11 write-time validation contract, and the
single production consumer of `audit_record_repository`.

The five `subject_*` columns on `audit_records` carry no foreign key.
Accepted Q2-RI admits that only where durable correctness, validation and
historical subject resolvability are established through another
explicit, recorded mechanism. This module implements the validating part
of that mechanism for the supported application write path. The
repository boundary and transactional tests complete the bounded
implementation; direct Session use and raw SQL remain outside what this
module can enforce. Without a validating write path, the exactly-one
CHECK on `audit_records` proves only that one UUID column is populated --
never that the UUID it holds ever denoted a real, loaded subject.

The contract, as A-11 approved it:

- The caller passes a **loaded subject instance**, never a bare UUID. A
  UUID argument is precisely what this contract exists to refuse: there
  is nothing to check it against.
- `workspace_id` and the subject's canonical identity are derived from
  the loaded subject, not accepted as free values from the caller.
- An unsupported subject kind, an inadmissible action, an invalid
  field-level diff, a deleted or deletion-scheduled subject, a subject
  with no persisted identity, a subject not attached to the caller's own
  session, or a workspace mismatch rejects the whole call before
  anything is added to `session`.
- The already-validated record is handed to `audit_record_repository`,
  which performs no validation of its own.

Bounded to A-11's initial callable slice: `EnterpriseObject` and `Task`,
the two kinds WP13 and WP15 need. The other three accepted D1 subject
kinds (`Workspace`, `User`, `WorkspaceMembership`) remain
schema-supported -- all five `subject_*` columns exist on the table --
but are deliberately absent from `SUBJECT_COLUMNS` below. `User` in
particular carries no `workspace_id` of its own, so the source of the
required `AuditRecord.workspace_id` is not established for it. Listing
any of the three here would assert a service authorization A-11
withholds.

Subject kind is matched on `type(subject)` exactly, never with
`isinstance`. A subclass of an authorized model is a different kind
until something authorizes it; silently inheriting the authorization is
the failure mode this exact-match check exists to prevent.

**The persistent/same-session requirement is a bounded implementation
choice, not something A-11's "trusted loaded subject" language compels
by itself.** `inspect(subject).persistent` and `object_session(subject)
is session` together are a stricter reading than the minimum text
requires, and that strictness binds future callers directly: a newly
created business object is *pending*, not *persistent*, so WP13 and WP15
must flush it before calling `record()` so that it has a persisted
identity. An already-persistent subject may carry pending changes and
needs no prior flush -- the repository's own `flush()` writes them in the
same transaction as the audit record. That is a stated contract this
module imposes on those future work packages, not an incidental detail to
discover later.

A deleted or deletion-scheduled subject is rejected explicitly, in two
parts, because SQLAlchemy's own state machine splits that condition in
two: `state.deleted` becomes true only after `flush()` completes a
`session.delete(...)`, while `subject in session.deleted` is what
reveals it beforehand, in the window between `session.delete(obj)` and
the next flush -- during which the instance is still `persistent` by
SQLAlchemy's own definition. A-11's callable slice records no deletion
actions, and a subject that is about to disappear cannot carry a
resolvable audit reference, which is exactly the resolvability guarantee
Q2-RI conditions the absent foreign keys on.

`AuditService` is a class of static methods rather than a module of
functions so the call site reads exactly as ADR-0005 and A-11 write it:
`AuditService.record(...)`. It holds no state and is never instantiated.

Rejections raise `TypeError` (an unsupported subject kind -- the wrong
kind of thing entirely) or `ValueError` (every other rejection -- the
right kind of thing, an inadmissible value), never an
`app.core.errors.AppError` subclass. `AppError` is the WP22 HTTP
envelope's extension point: it carries an HTTP status (`internal_error`
/ 500 by default) meant for a FastAPI exception handler to translate into
a response. A-11 authorizes no audit API surface in this bounded scope,
so choosing an HTTP status here would decide something this scope does
not own. When an audited endpoint eventually exists, an `AppError`
subclass is the sanctioned way to give these failures a code and a
status -- see `app/core/errors.py`.

Raising `TypeError`/`ValueError` here does not, by itself, stop a caller
from catching either and committing anyway -- no function in this module
can enforce that. What this module guarantees is narrower and honest:
every rejection happens before anything is added to `session`, so an
exception that is allowed to propagate out of the caller's transaction
boundary reaches that boundary's own transaction manager, which is what
performs the rollback. `record()` never commits and never rolls back
itself; ending the transaction, in either direction, is always the
caller's responsibility.

This module enforces membership in the closed named action vocabulary in
`app.services.audit_actions` -- it cannot, and does not claim to, prove
that an equal string a caller passed was written *through* one of the
exported constants rather than typed out ad hoc. Production call sites
are required, by convention, to use the exported constants; nothing here
can verify that mechanically.
"""

import json
import uuid
from collections.abc import Mapping
from types import MappingProxyType
from typing import Any, Final, cast

from sqlalchemy import inspect as sa_inspect
from sqlalchemy.orm import Session, object_session

from app.db.base import Base
from app.models.audit_record import AuditRecord
from app.models.enterprise_object import EnterpriseObject
from app.models.task import Task
from app.repositories import audit_record_repository
from app.services.audit_actions import ALLOWED_ACTIONS_BY_SUBJECT_TYPE

#: Which `subject_*` column carries each authorized subject kind's
#: canonical identity. Bounded to A-11's initial callable slice -- see the
#: module docstring for why the other three D1 kinds are absent. Its key
#: set must equal `ALLOWED_ACTIONS_BY_SUBJECT_TYPE`'s, so a kind cannot
#: become storable without also being admissible, or admissible without
#: being storable; `tests/test_audit_service.py` asserts that equality.
SUBJECT_COLUMNS: Final[Mapping[type, str]] = MappingProxyType(
    {
        EnterpriseObject: "subject_enterprise_object_id",
        Task: "subject_task_id",
    }
)


def _validate_and_detach_content(content: Mapping[str, Any]) -> dict[str, list[Any]]:
    """Validate a field-level diff and return a deep, detached copy.

    Form: `{"field_name": [before, after]}`. Validated and detached one
    field at a time, not with one whole-mapping `json.dumps` -- a single
    serialization of the entire content mapping cannot say which field
    failed, and every failure here must name the offending field.

    `json.dumps(..., allow_nan=False)` raises `TypeError` on a value that
    is not JSON-serializable and `ValueError` on a non-finite float
    (`nan`, `inf`, `-inf`); both are caught and re-raised as one
    `ValueError` naming the field, so this contract has exactly one
    failure type from the caller's perspective. The round trip through
    `json.dumps` then `json.loads` both validates and deeply detaches the
    pair in one operation -- the returned value shares no mutable
    structure with the caller's -- and normalizes a tuple pair into a
    list, since JSON has no tuple type. `before != after` is compared on
    the round-tripped values, so no stored record can carry a pair
    recording no change.
    """
    if not isinstance(content, Mapping) or not content:
        raise ValueError("content must be a non-empty mapping of field-level diffs")

    detached: dict[str, list[Any]] = {}
    for key, pair in content.items():
        if not isinstance(key, str) or key.strip() == "":
            raise ValueError(f"content key {key!r} must be a non-blank string")
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError(
                f"content[{key!r}] must be a two-element [before, after] pair"
            )
        try:
            roundtripped = cast(
                "list[Any]", json.loads(json.dumps(list(pair), allow_nan=False))
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"content[{key!r}] is not JSON-compatible: {exc}"
            ) from exc
        before, after = roundtripped
        if before == after:
            raise ValueError(
                f"content[{key!r}] records no change: before and after are equal"
            )
        detached[key] = [before, after]
    return detached


class AuditService:
    """Namespace for the audit write path. Never instantiated, holds no state."""

    @staticmethod
    def record(
        session: Session,
        *,
        subject: Base,
        action: str,
        content: Mapping[str, Any],
        expected_workspace_id: uuid.UUID | None = None,
    ) -> AuditRecord:
        """Record one audited mutation in the caller's open transaction.

        `session` must be the same session `subject` was loaded or
        flushed through -- A-11 requires the business mutation and its
        audit record to commit or fail together, and this method never
        commits or rolls back either one.

        `subject` is the persistent ORM instance that was mutated. A newly
        created one must have been flushed already, so that it has a
        persisted identity; an already-persistent one may still carry
        pending changes, which the repository's flush writes in the same
        transaction as the audit record. Its primary key is the canonical
        audited identity and its `workspace_id` is the ADR-0004 scope --
        both derived here, neither accepted from the caller.

        `expected_workspace_id` is a confirmation, never an override. A
        trusted mutation context that already knows which workspace it is
        operating in may pass it; if it disagrees with the subject's own
        `workspace_id`, the whole call is rejected. Passing it can never
        change which workspace the record is written under -- that value
        always comes from `subject.workspace_id`.

        Raises `TypeError` for an unsupported subject kind (the wrong
        kind of thing) and `ValueError` for every other rejection (the
        right kind of thing, an inadmissible value) -- before adding or
        flushing any `AuditRecord` in every case.
        """
        subject_type = type(subject)

        # 1. Exact authorized subject type. TypeError: the wrong kind of
        #    thing, not merely an inadmissible value of the right kind.
        column = SUBJECT_COLUMNS.get(subject_type)
        if column is None:
            raise TypeError(
                f"unsupported audit subject kind: {subject_type.__name__}; "
                "A-11's callable slice covers EnterpriseObject and Task only"
            )

        # 2. Action admissible for that exact type. `isinstance` guards the
        #    membership test: a non-string action (unhashable, e.g. a list
        #    or dict) must not reach `in` and raise TypeError there,
        #    which is reserved for check 1 alone.
        if not isinstance(action, str) or (
            action not in ALLOWED_ACTIONS_BY_SUBJECT_TYPE[subject_type]
        ):
            raise ValueError(
                f"action {action!r} is not an admissible action for subject "
                f"kind {subject_type.__name__}"
            )

        # 3. Field-level diff -- validated and detached before anything
        #    below touches `session`.
        detached_content = _validate_and_detach_content(content)

        # 4. Already deleted and flushed -- checked first, because such a
        #    subject is also non-persistent and would otherwise be
        #    reported as merely unflushed, pointing away from the real
        #    cause.
        state = sa_inspect(subject)
        if state.deleted:
            raise ValueError(
                f"{subject_type.__name__} has been deleted; A-11's callable "
                "slice records no deletion actions, and a deleted subject "
                "cannot carry a resolvable audit reference"
            )

        # 5. Transient, pending or detached.
        if not state.persistent:
            raise ValueError(
                f"{subject_type.__name__} is not persistent; a newly "
                "created subject must be flushed before calling record() "
                "so that it has a persisted identity"
            )

        # 6. Attached to the session performing this write, not a
        #    different one. Established before any of that session's own
        #    state is read.
        if object_session(subject) is not session:
            raise ValueError(
                "subject is not attached to the session performing this write"
            )

        # 7. Scheduled for deletion but not yet flushed: still persistent
        #    by SQLAlchemy's definition, so only `session.deleted` reveals
        #    it -- consulted only now that the session is confirmed to be
        #    the subject's own.
        if subject in session.deleted:
            raise ValueError(
                f"{subject_type.__name__} is scheduled for deletion; A-11's "
                "callable slice records no deletion actions, and a subject "
                "that is about to disappear cannot carry a resolvable audit "
                "reference"
            )

        # 8. Non-null canonical identity.
        subject_id = cast(Any, subject).id
        if subject_id is None:
            raise ValueError(f"{subject_type.__name__}.id must be set")

        # 9. Non-null workspace, derived from the subject.
        workspace_id = cast(Any, subject).workspace_id
        if workspace_id is None:
            raise ValueError(f"{subject_type.__name__}.workspace_id must be set")

        # 10. expected_workspace_id confirms; it never overrides.
        if (
            expected_workspace_id is not None
            and expected_workspace_id != workspace_id
        ):
            raise ValueError(
                "workspace mismatch: expected_workspace_id does not match "
                "the subject's own workspace_id"
            )

        # 11. Exactly the mapped subject column is populated.
        record = AuditRecord(
            workspace_id=workspace_id,
            action=action,
            content=detached_content,
            **{column: subject_id},
        )

        # 12. The validated record, and only the validated record, reaches
        #     the repository.
        return audit_record_repository.add(session, record)
