"""AuditService write-time validation contract -- unit level, no database.

What these tests prove that the model tests cannot: that each rejection
branch in `AuditService.record(...)` fires for its own stated reason, not
merely "the call raised something." Every rejection test below pins its
branch with `pytest.raises(..., match=...)` on a fragment unique to the
intended message -- without that, a test would pass on any earlier
rejection, and the whole suite would become a set of assertions about the
wrong things.

Most rejection tests pass `session=None` deliberately. The `session=None`
technique can exercise every rejection path that terminates before the
scheduled-deletion membership check. In this unit suite that includes
subject-kind, action, content, and transient-subject rejections. It does
not prove persistent same-session, different-session, deleted, or
scheduled-for-deletion behavior; those belong to the persistence suite.

`None` is not a shortcut: if a check that should reject earlier ever
dereferences the session, the test fails with `AttributeError` instead of
the expected contract exception. The first check that dereferences
`session` is `subject in session.deleted`.

The canonical-identity, derived-workspace, and workspace-mismatch
branches require a persistent same-session subject and therefore belong
to the persistence suite. They are not exercised here with
`session=None`.

No test here calls `record()` successfully. A successful call requires a
persistent subject in a real session and belongs to
`tests/test_audit_record_persistence.py` -- a mock or a hand-assigned
`id` cannot demonstrate persistence or session ownership, and a test
claiming otherwise here would be false.
"""

import inspect
import uuid
from datetime import datetime

import pytest

from app.models.enterprise_object import EnterpriseObject
from app.models.user import User
from app.services.audit_actions import (
    ALLOWED_ACTIONS_BY_SUBJECT_TYPE,
    ENTERPRISE_OBJECT_CREATED,
    TASK_CREATED,
)
from app.services.audit_service import SUBJECT_COLUMNS, AuditService


@pytest.fixture()
def enterprise_object_subject() -> EnterpriseObject:
    """Clears checks 1 (type) and 2 (action) when used with
    `ENTERPRISE_OBJECT_CREATED`. No `id`, no session -- content
    validation (check 3) runs before any subject-state check, so this
    subject's transience never comes into play in the content tests
    below.
    """
    return EnterpriseObject(type="business_request")


# --- Check 1: subject kind -- TypeError -----------------------------------


def test_unsupported_model_subject_is_rejected() -> None:
    """`User` is schema-supported (the column exists on `audit_records`)
    but not service-authorized in A-11's callable slice -- check 1,
    `TypeError`, the wrong kind of thing entirely."""
    with pytest.raises(TypeError, match="unsupported audit subject kind"):
        AuditService.record(
            None,  # type: ignore[arg-type]
            subject=User(),
            action=ENTERPRISE_OBJECT_CREATED,
            content={"x": [None, 1]},
        )


def test_bare_uuid_subject_is_rejected() -> None:
    """The contract exists to refuse exactly this: an identifier with
    nothing loaded behind it to validate."""
    with pytest.raises(TypeError, match="unsupported audit subject kind"):
        AuditService.record(
            None,  # type: ignore[arg-type]
            subject=uuid.uuid4(),  # type: ignore[arg-type]
            action=ENTERPRISE_OBJECT_CREATED,
            content={"x": [None, 1]},
        )


# --- Check 2: action -- ValueError -----------------------------------------


def test_cross_type_action_is_rejected(
    enterprise_object_subject: EnterpriseObject,
) -> None:
    """`TASK_CREATED` is admissible for `Task`, not `EnterpriseObject` --
    this is what the per-type frozenset, not a flattened vocabulary,
    exists to catch."""
    with pytest.raises(ValueError, match="not an admissible action"):
        AuditService.record(
            None,  # type: ignore[arg-type]
            subject=enterprise_object_subject,
            action=TASK_CREATED,
            content={"x": [None, 1]},
        )


def test_unknown_action_string_is_rejected(
    enterprise_object_subject: EnterpriseObject,
) -> None:
    """ADR-0005 requires production call sites to use named constants.
    The service can enforce only membership in the closed vocabulary; it
    cannot distinguish an exported constant from an equal ad-hoc string
    literal. This test proves rejection of a value outside that
    vocabulary.
    """
    with pytest.raises(ValueError, match="not an admissible action"):
        AuditService.record(
            None,  # type: ignore[arg-type]
            subject=enterprise_object_subject,
            action="enterprise_object.deleted",
            content={"x": [None, 1]},
        )


def test_non_string_action_is_rejected_as_value_error_not_type_error(
    enterprise_object_subject: EnterpriseObject,
) -> None:
    """Regression test for the unhashable-action guard. `action not in
    frozenset` calls `hash(action)`; a list is unhashable. Without the
    `isinstance(action, str)` guard preceding the membership test, this
    call would raise `TypeError: unhashable type: 'list'` from `in`
    itself -- and `pytest.raises(ValueError)` alone correctly fails to
    catch a `TypeError`, since `TypeError` is not a subclass of
    `ValueError`. Do not relax this to
    `pytest.raises((TypeError, ValueError))`; that would silently accept
    the regression this test exists to catch.
    """
    with pytest.raises(ValueError, match="not an admissible action"):
        AuditService.record(
            None,  # type: ignore[arg-type]
            subject=enterprise_object_subject,
            action=["task.created"],  # type: ignore[arg-type]
            content={"x": [None, 1]},
        )


# --- Check 3: field-level diff -- ValueError -------------------------------


def test_non_mapping_content_is_rejected(
    enterprise_object_subject: EnterpriseObject,
) -> None:
    with pytest.raises(ValueError, match="non-empty mapping"):
        AuditService.record(
            None,  # type: ignore[arg-type]
            subject=enterprise_object_subject,
            action=ENTERPRISE_OBJECT_CREATED,
            content="not a mapping",  # type: ignore[arg-type]
        )


def test_empty_content_is_rejected(
    enterprise_object_subject: EnterpriseObject,
) -> None:
    with pytest.raises(ValueError, match="non-empty mapping"):
        AuditService.record(
            None,  # type: ignore[arg-type]
            subject=enterprise_object_subject,
            action=ENTERPRISE_OBJECT_CREATED,
            content={},
        )


def test_non_string_content_key_is_rejected(
    enterprise_object_subject: EnterpriseObject,
) -> None:
    with pytest.raises(ValueError, match="non-blank string"):
        AuditService.record(
            None,  # type: ignore[arg-type]
            subject=enterprise_object_subject,
            action=ENTERPRISE_OBJECT_CREATED,
            content={1: [None, "x"]},  # type: ignore[dict-item]
        )


def test_whitespace_only_content_key_is_rejected(
    enterprise_object_subject: EnterpriseObject,
) -> None:
    """A key of `" "` is non-empty but blank -- `key.strip() != ""` is
    what this test proves, distinctly from a merely-empty-string key."""
    with pytest.raises(ValueError, match="non-blank string"):
        AuditService.record(
            None,  # type: ignore[arg-type]
            subject=enterprise_object_subject,
            action=ENTERPRISE_OBJECT_CREATED,
            content={" ": [None, "x"]},
        )


def test_content_pair_that_is_not_a_list_or_tuple_is_rejected(
    enterprise_object_subject: EnterpriseObject,
) -> None:
    with pytest.raises(ValueError, match="two-element"):
        AuditService.record(
            None,  # type: ignore[arg-type]
            subject=enterprise_object_subject,
            action=ENTERPRISE_OBJECT_CREATED,
            content={"type": "not a pair"},
        )


@pytest.mark.parametrize(
    "pair",
    [["only-one"], ["a", "b", "c"]],
    ids=["length-1", "length-3"],
)
def test_content_pair_of_wrong_length_is_rejected(
    enterprise_object_subject: EnterpriseObject, pair: list[str]
) -> None:
    with pytest.raises(ValueError, match="two-element"):
        AuditService.record(
            None,  # type: ignore[arg-type]
            subject=enterprise_object_subject,
            action=ENTERPRISE_OBJECT_CREATED,
            content={"type": pair},
        )


@pytest.mark.parametrize(
    "bad_value",
    [datetime.now(), object()],
    ids=["datetime", "object"],
)
def test_non_json_serializable_content_value_is_rejected(
    enterprise_object_subject: EnterpriseObject, bad_value: object
) -> None:
    """`json.dumps` natively raises `TypeError` for a non-serializable
    value; the service catches that and re-raises `ValueError`, so this
    contract has exactly one failure type from the caller's perspective.
    """
    with pytest.raises(ValueError, match="not JSON-compatible"):
        AuditService.record(
            None,  # type: ignore[arg-type]
            subject=enterprise_object_subject,
            action=ENTERPRISE_OBJECT_CREATED,
            content={"type": [None, bad_value]},
        )


@pytest.mark.parametrize(
    "bad_value",
    [float("nan"), float("inf"), float("-inf")],
    ids=["nan", "inf", "neg-inf"],
)
def test_non_finite_float_content_value_is_rejected(
    enterprise_object_subject: EnterpriseObject, bad_value: float
) -> None:
    """`json.dumps(..., allow_nan=False)` raises `ValueError` natively for
    a non-finite float; the service catches that alongside the
    `TypeError` case above and re-raises one consistent `ValueError`.
    """
    with pytest.raises(ValueError, match="not JSON-compatible"):
        AuditService.record(
            None,  # type: ignore[arg-type]
            subject=enterprise_object_subject,
            action=ENTERPRISE_OBJECT_CREATED,
            content={"type": [0, bad_value]},
        )


def test_content_pair_with_equal_before_and_after_is_rejected(
    enterprise_object_subject: EnterpriseObject,
) -> None:
    """A pair recording no change is not a diff."""
    with pytest.raises(ValueError, match="records no change"):
        AuditService.record(
            None,  # type: ignore[arg-type]
            subject=enterprise_object_subject,
            action=ENTERPRISE_OBJECT_CREATED,
            content={"phase": ["active", "active"]},
        )


# --- Check 5: subject state (persistent) -- ValueError ---------------------


def test_a_subject_with_an_id_but_no_persistence_is_still_rejected() -> None:
    """Having an `id` does not make a subject persistent -- this is
    exactly the hole the persistent/same-session requirement exists to
    close. This instance is complete enough (a set `id`, `workspace_id`,
    `owner_id`, `type`) to clear checks 1-4 -- type, action, content, and
    "not deleted" (a transient instance is never `state.deleted`) -- and
    reach check 5, `not state.persistent`, failing there and nowhere
    else. `session=None` is safe up to and including this check: it is
    never dereferenced before it.
    """
    subject = EnterpriseObject(
        id=uuid.uuid4(),
        workspace_id=uuid.uuid4(),
        owner_id=uuid.uuid4(),
        type="business_request",
    )
    with pytest.raises(ValueError, match="is not persistent"):
        AuditService.record(
            None,  # type: ignore[arg-type]
            subject=subject,
            action=ENTERPRISE_OBJECT_CREATED,
            content={"type": [None, "business_request"]},
        )


# --- Structural ---------------------------------------------------------


def test_the_two_authorization_tables_cover_the_same_subject_kinds() -> None:
    """A kind that is storable but not admissible (or the reverse) is a
    silent hole in the bounded slice, not a harmless inconsistency."""
    assert set(SUBJECT_COLUMNS) == set(ALLOWED_ACTIONS_BY_SUBJECT_TYPE)


def test_record_signature_has_no_workspace_id_override() -> None:
    """`workspace_id` is derived from the subject, never accepted as a
    free parameter -- this is what makes that structural rather than a
    documentation claim."""
    signature = inspect.signature(AuditService.record)
    assert "workspace_id" not in signature.parameters


def test_record_signature_exposes_expected_workspace_id_as_optional_confirmation() -> (
    None
):
    signature = inspect.signature(AuditService.record)
    parameter = signature.parameters["expected_workspace_id"]
    assert parameter.kind == inspect.Parameter.KEYWORD_ONLY
    assert parameter.default is None
