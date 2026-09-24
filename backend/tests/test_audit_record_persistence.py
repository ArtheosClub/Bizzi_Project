"""AuditRecord persistence and atomicity, against a real database -- WP19,
A-11 and A-11-CLAR-01.

Follows `tests/test_task_persistence.py`'s fixture pattern: a
module-scoped `engine` that `pytest.skip`s when no database is reachable,
and a function-scoped `session` bound to one connection whose outer
transaction is always rolled back at teardown. A "second session" below
always means a second `Session(bind=...)` on that *same* connection --
its own identity map, which is what proves a row reached the database
rather than living only in the first session's cache. It does not prove
durability after a real connection-level commit; the fixture deliberately
never commits its outer transaction, and no test here performs a durable
commit or adds a cleanup delete.

These tests cover what the model tests and the unit-level
`tests/test_audit_service.py` cannot: that `audit_records` carries
exactly one real foreign key (`workspace_id`, enforced by the database,
not merely declared) while the five `subject_*` columns are proven
genuinely FK-free, that `audit_record_repository.add()` flushes and never
itself ends the transaction, and -- the guarantee A-11 most needs
demonstrated -- that a business mutation and its audit record participate
in one caller-owned transaction and roll back together when either side
fails, with the caller, not the service or the repository, always the one
that ends the transaction.

WP13 and WP15's production mutation callers do not exist yet. The
atomicity tests below mutate `EnterpriseObject` and `Task` directly while
exercising the real `AuditService.record(...)` write path -- that is a
stand-in for those future callers, not a claim that they exist.
"""

import json
import uuid
from datetime import UTC, datetime

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import AuditRecord, EnterpriseObject, Task, User, Workspace
from app.repositories import audit_record_repository
from app.services.audit_actions import (
    ENTERPRISE_OBJECT_CREATED,
    ENTERPRISE_OBJECT_UPDATED,
    TASK_CREATED,
)
from app.services.audit_service import AuditService

SUBJECT_COLUMN_NAMES = (
    "subject_workspace_id",
    "subject_enterprise_object_id",
    "subject_user_id",
    "subject_workspace_membership_id",
    "subject_task_id",
)


@pytest.fixture(scope="module")
def engine():  # type: ignore[no-untyped-def]
    engine = create_engine(get_settings().database_url, pool_pre_ping=True)
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        pytest.skip(f"no database reachable: {exc.__class__.__name__}")
    return engine


@pytest.fixture()
def session(engine):  # type: ignore[no-untyped-def]
    """Each test runs in a transaction that is always rolled back.

    The teardown rollback is guarded, unlike the sibling persistence
    suites': several tests here end the outer transaction themselves via
    an explicit `session.rollback()` or a failed flush. A Session joining
    a plain external transaction runs in `rollback_only` mode, so its
    rollback reaches the enclosing transaction. Rolling back again would
    only emit `SAWarning: transaction already deassociated`.
    """
    connection = engine.connect()
    transaction = connection.begin()
    db = Session(bind=connection)
    try:
        yield db
    finally:
        db.close()
        if transaction.is_active:
            transaction.rollback()
        connection.close()


@pytest.fixture()
def user(session):  # type: ignore[no-untyped-def]
    user = User()
    session.add(user)
    session.flush()
    return user


@pytest.fixture()
def workspace(session, user):  # type: ignore[no-untyped-def]
    workspace = Workspace(name="Test Workspace", owner_id=user.id)
    session.add(workspace)
    session.flush()
    return workspace


@pytest.fixture()
def enterprise_object(session, workspace, user):  # type: ignore[no-untyped-def]
    obj = EnterpriseObject(
        workspace_id=workspace.id, type="business_request", owner_id=user.id
    )
    session.add(obj)
    session.flush()
    return obj


@pytest.fixture()
def task(session, workspace):  # type: ignore[no-untyped-def]
    task = Task(workspace_id=workspace.id)
    session.add(task)
    session.flush()
    return task


def _visible_in_a_second_session(session: Session, model: type, pk: object) -> bool:
    """A second identity map on the same connection -- proves a row reached
    the database rather than living only in the first session's cache. Not a
    proof of durable commit: the fixture's outer transaction is never
    committed.

    The fixture owns an external transaction on the shared Connection. The
    observer Session below is opened with a nested savepoint of its own, so
    its transactional lifecycle is explicitly isolated rather than depending
    on SQLAlchemy's conditional choice for a Session joining an
    already-active Connection transaction. This is an isolation guarantee
    for the observer, not a claim that rollback_only would necessarily
    propagate to close().
    """
    other = Session(
        bind=session.connection(),
        join_transaction_mode="create_savepoint",
    )
    try:
        return other.get(model, pk) is not None
    finally:
        other.close()


# --- (1)-(2): the migration reached real DDL -------------------------------


def test_audit_records_table_exists(engine) -> None:  # type: ignore[no-untyped-def]
    """Proves `alembic upgrade head` actually created the table."""
    assert "audit_records" in inspect(engine).get_table_names()


def test_check_constraint_naming_convention_reached_real_ddl(  # type: ignore[no-untyped-def]
    engine,
) -> None:
    """The convention must reach real DDL, not just ORM metadata."""
    checks = inspect(engine).get_check_constraints("audit_records")
    names = {c["name"] for c in checks}
    assert "ck_audit_records_exactly_one_subject_reference" in names


# --- (3)-(5): the exactly-one CHECK, enforced by the database --------------


def test_zero_subject_columns_rejected_by_check_constraint(  # type: ignore[no-untyped-def]
    session, workspace
) -> None:
    audit = AuditRecord(workspace_id=workspace.id, action="test.zero", content={"x": 1})
    session.add(audit)
    with pytest.raises(IntegrityError):
        session.flush()


def test_two_subject_columns_rejected_by_check_constraint(  # type: ignore[no-untyped-def]
    session, workspace
) -> None:
    audit = AuditRecord(
        workspace_id=workspace.id,
        action="test.two",
        content={"x": 1},
        subject_task_id=uuid.uuid4(),
        subject_enterprise_object_id=uuid.uuid4(),
    )
    session.add(audit)
    with pytest.raises(IntegrityError):
        session.flush()


def test_exactly_one_subject_column_accepted(  # type: ignore[no-untyped-def]
    session, workspace
) -> None:
    audit = AuditRecord(
        workspace_id=workspace.id,
        action="test.one",
        content={"x": 1},
        subject_task_id=uuid.uuid4(),
    )
    session.add(audit)
    session.flush()
    assert audit.id is not None


# --- (6): created_at server default -----------------------------------------


def test_created_at_resolves_from_server_default_on_direct_insert(  # type: ignore[no-untyped-def]
    session, workspace
) -> None:
    """Bypasses the ORM entirely, naming no `created_at` value at all, so
    only the database's own `server_default` can produce one -- mirrors
    `test_task_persistence.py`'s
    `test_server_default_resolves_phase_to_active`.
    """
    audit_id = uuid.uuid4()
    session.execute(
        text(
            "INSERT INTO audit_records "
            "(id, workspace_id, action, content, subject_task_id) "
            "VALUES (:id, :workspace_id, :action, CAST(:content AS JSONB), "
            ":subject_task_id)"
        ),
        {
            "id": audit_id,
            "workspace_id": workspace.id,
            "action": "test.server_default",
            "content": json.dumps({"x": 1}),
            "subject_task_id": uuid.uuid4(),
        },
    )
    session.flush()

    row = session.execute(
        text("SELECT created_at FROM audit_records WHERE id = :id"), {"id": audit_id}
    ).one()
    assert row.created_at is not None


# --- (7)-(8): the workspace_id FK is enforced; the subject columns are not -


def test_audit_records_has_exactly_one_foreign_key_and_it_is_workspace_id(
    engine,
) -> None:  # type: ignore[no-untyped-def]
    """The module docstring's FK claim, read from real DDL rather than
    inferred from a single behavioural insert.

    A-11-CLAR-01 records two decisions this asserts: `workspace_id` carries
    a real foreign key to `workspaces.id` as a Project Owner implementation
    choice, and no explicit `ON DELETE` is specified, so PostgreSQL's
    `NO ACTION` is the resulting behaviour -- absence of a clause is not
    absence of behaviour. The five `subject_*` columns carry none; that is
    the accepted Q2 shape, and the write-time validation contract in
    `audit_service.py` is what Q2-RI requires in place of the missing
    constraints.
    """
    foreign_keys = inspect(engine).get_foreign_keys("audit_records")
    assert len(foreign_keys) == 1

    fk = foreign_keys[0]
    assert fk["name"] == "fk_audit_records_workspace_id_workspaces"
    assert fk["constrained_columns"] == ["workspace_id"]
    assert fk["referred_table"] == "workspaces"
    assert fk["referred_columns"] == ["id"]
    assert (fk.get("options") or {}).get("ondelete") is None

    constrained = {c for f in foreign_keys for c in f["constrained_columns"]}
    assert constrained.isdisjoint(SUBJECT_COLUMN_NAMES)


def test_workspace_id_fk_is_enforced(session) -> None:  # type: ignore[no-untyped-def]
    """A-11-CLAR-01's choice actually enforced, not merely declared.

    Proves a different thing than the DDL test above: that DDL asserts
    the constraint exists and what shape it has; this proves that
    PostgreSQL actually rejects a non-existent `workspace_id` at insert
    time, behaviourally.
    """
    audit = AuditRecord(
        workspace_id=uuid.uuid4(),
        action="test.unknown_workspace",
        content={"x": 1},
        subject_task_id=uuid.uuid4(),
    )
    session.add(audit)
    with pytest.raises(IntegrityError):
        session.flush()


def test_subject_columns_carry_no_foreign_key(  # type: ignore[no-untyped-def]
    session, workspace
) -> None:
    """Confirms the absence behaviourally: a `subject_enterprise_object_id`
    pointing at no row inserts successfully. The structural claim -- that
    the table carries no foreign key on any of the five columns -- is
    asserted from DDL in
    `test_audit_records_has_exactly_one_foreign_key_and_it_is_workspace_id`
    above; the two tests prove different things.

    `AuditService.record(...)` can never produce such a record; it
    requires a loaded, persistent subject, so the UUID always denotes a
    real row when the service is the caller. This test calls
    `audit_record_repository.add(...)` directly, the way only
    `audit_service.py` is permitted to in production, which is exactly
    why `test_audit_repository_boundary.py`'s consumer scan is
    load-bearing. That scan covers `app/` only, so this direct call from
    `tests/` is permitted by design, not an oversight.
    """
    audit = AuditRecord(
        workspace_id=workspace.id,
        action="test.no_fk",
        content={"x": 1},
        subject_enterprise_object_id=uuid.uuid4(),
    )
    result = audit_record_repository.add(session, audit)
    assert result.id is not None


# --- (9): add() flushes; a caller-owned rollback removes the row -----------


def test_repository_add_flushes_a_row_that_caller_owned_rollback_removes(
    session, workspace
) -> None:  # type: ignore[no-untyped-def]
    """`add()` flushes -- a second session on the same connection sees the
    row immediately after -- and an explicit, caller-owned
    `session.rollback()` removes it. This establishes flush-and-rollback
    behaviour only. That neither `add()` nor `AuditService.record(...)`
    contains any transaction-ending call is proved separately and
    statically, in `test_audit_repository_boundary.py::
    test_neither_the_repository_nor_the_service_ends_the_transaction`.
    """
    audit = AuditRecord(
        workspace_id=workspace.id,
        action="test.flush_visible",
        content={"x": 1},
        subject_task_id=uuid.uuid4(),
    )
    audit_record_repository.add(session, audit)
    audit_id = audit.id

    assert _visible_in_a_second_session(session, AuditRecord, audit_id)

    session.rollback()

    assert not _visible_in_a_second_session(session, AuditRecord, audit_id)


# --- (10)-(12): list_by_workspace -------------------------------------------


def test_list_by_workspace_returns_only_the_requested_workspace(  # type: ignore[no-untyped-def]
    session, workspace, user
) -> None:
    other_user = User()
    session.add(other_user)
    session.flush()
    other_workspace = Workspace(name="Other Workspace", owner_id=other_user.id)
    session.add(other_workspace)
    session.flush()

    mine = AuditRecord(
        workspace_id=workspace.id,
        action="test.mine",
        content={"x": 1},
        subject_task_id=uuid.uuid4(),
    )
    theirs = AuditRecord(
        workspace_id=other_workspace.id,
        action="test.theirs",
        content={"x": 1},
        subject_task_id=uuid.uuid4(),
    )
    audit_record_repository.add(session, mine)
    audit_record_repository.add(session, theirs)

    results = audit_record_repository.list_by_workspace(session, workspace.id, limit=10)
    assert [r.id for r in results] == [mine.id]


def test_list_by_workspace_orders_chronologically(  # type: ignore[no-untyped-def]
    session, workspace
) -> None:
    """`now()` is transaction-start time -- rows in one transaction would
    otherwise share `created_at`. Explicit, differing values are what
    make this a genuine chronology test rather than an accidental
    insertion-order one.
    """
    older = AuditRecord(
        workspace_id=workspace.id,
        action="test.older",
        content={"x": 1},
        subject_task_id=uuid.uuid4(),
        created_at=datetime(2020, 1, 1, tzinfo=UTC),
    )
    newer = AuditRecord(
        workspace_id=workspace.id,
        action="test.newer",
        content={"x": 1},
        subject_task_id=uuid.uuid4(),
        created_at=datetime(2021, 1, 1, tzinfo=UTC),
    )
    audit_record_repository.add(session, older)
    audit_record_repository.add(session, newer)

    results = audit_record_repository.list_by_workspace(session, workspace.id, limit=10)
    assert [r.id for r in results] == [newer.id, older.id]


def test_list_by_workspace_breaks_equal_timestamps_by_id_desc(  # type: ignore[no-untyped-def]
    session, workspace
) -> None:
    """Postgres orders `uuid` bytewise; Python's `UUID` comparison is by
    `.int` -- the same 128-bit value in the same order, so the database's
    tiebreak and this assertion's `sorted(..., reverse=True)` agree."""
    same_time = datetime(2022, 1, 1, tzinfo=UTC)
    a = AuditRecord(
        workspace_id=workspace.id,
        action="test.a",
        content={"x": 1},
        subject_task_id=uuid.uuid4(),
        created_at=same_time,
    )
    b = AuditRecord(
        workspace_id=workspace.id,
        action="test.b",
        content={"x": 1},
        subject_task_id=uuid.uuid4(),
        created_at=same_time,
    )
    audit_record_repository.add(session, a)
    audit_record_repository.add(session, b)

    expected_order = sorted([a.id, b.id], reverse=True)
    results = audit_record_repository.list_by_workspace(session, workspace.id, limit=10)
    assert [r.id for r in results] == expected_order


@pytest.mark.parametrize("limit", [0, -1, True], ids=["zero", "negative", "bool-true"])
def test_list_by_workspace_rejects_invalid_limits(  # type: ignore[no-untyped-def]
    session, workspace, limit
) -> None:
    with pytest.raises(ValueError, match="positive int"):
        audit_record_repository.list_by_workspace(session, workspace.id, limit=limit)


# --- (13)-(14): AuditService.record accepts a persistent same-session subject


def test_record_accepts_a_persistent_same_session_enterprise_object(  # type: ignore[no-untyped-def]
    session, enterprise_object
) -> None:
    AuditService.record(
        session,
        subject=enterprise_object,
        action=ENTERPRISE_OBJECT_CREATED,
        content={"type": [None, "business_request"]},
    )

    records = audit_record_repository.list_by_workspace(session, enterprise_object.workspace_id)
    assert len(records) == 1
    record = records[0]
    assert record.id is not None
    assert record.subject_enterprise_object_id == enterprise_object.id


def test_record_accepts_a_persistent_same_session_task(  # type: ignore[no-untyped-def]
    session, task
) -> None:
    AuditService.record(
        session,
        subject=task,
        action=TASK_CREATED,
        content={"phase": [None, "active"]},
    )

    records = audit_record_repository.list_by_workspace(session, task.workspace_id)
    assert len(records) == 1
    record = records[0]
    assert record.id is not None
    assert record.subject_task_id == task.id


# --- (15): subject-state rejections, six cases ------------------------------


def test_transient_subject_is_rejected(  # type: ignore[no-untyped-def]
    session, workspace, user
) -> None:
    subject = EnterpriseObject(
        workspace_id=workspace.id, type="business_request", owner_id=user.id
    )
    with pytest.raises(ValueError, match="is not persistent"):
        AuditService.record(
            session,
            subject=subject,
            action=ENTERPRISE_OBJECT_CREATED,
            content={"type": [None, "business_request"]},
        )


def test_pending_subject_is_rejected(  # type: ignore[no-untyped-def]
    session, workspace, user
) -> None:
    subject = EnterpriseObject(
        workspace_id=workspace.id, type="business_request", owner_id=user.id
    )
    session.add(subject)
    with pytest.raises(ValueError, match="is not persistent"):
        AuditService.record(
            session,
            subject=subject,
            action=ENTERPRISE_OBJECT_CREATED,
            content={"type": [None, "business_request"]},
        )


def test_detached_subject_is_rejected(  # type: ignore[no-untyped-def]
    session, enterprise_object
) -> None:
    session.expunge(enterprise_object)
    with pytest.raises(ValueError, match="is not persistent"):
        AuditService.record(
            session,
            subject=enterprise_object,
            action=ENTERPRISE_OBJECT_UPDATED,
            content={"type": ["business_request", "process"]},
        )


def test_subject_from_a_different_session_is_rejected(  # type: ignore[no-untyped-def]
    session, workspace, user
) -> None:
    """The observer below is opened with the same nested-savepoint
    isolation as `_visible_in_a_second_session`, rather than depending on
    SQLAlchemy's conditional join choice."""
    other = Session(
        bind=session.connection(),
        join_transaction_mode="create_savepoint",
    )
    try:
        subject = EnterpriseObject(
            workspace_id=workspace.id, type="business_request", owner_id=user.id
        )
        other.add(subject)
        other.flush()

        with pytest.raises(ValueError, match="not attached to the session"):
            AuditService.record(
                session,
                subject=subject,
                action=ENTERPRISE_OBJECT_CREATED,
                content={"type": [None, "business_request"]},
            )
    finally:
        other.close()


def test_deleted_and_flushed_subject_is_rejected(  # type: ignore[no-untyped-def]
    session, enterprise_object
) -> None:
    session.delete(enterprise_object)
    session.flush()
    with pytest.raises(ValueError, match="has been deleted"):
        AuditService.record(
            session,
            subject=enterprise_object,
            action=ENTERPRISE_OBJECT_UPDATED,
            content={"type": ["business_request", "process"]},
        )


def test_scheduled_for_deletion_subject_is_rejected(  # type: ignore[no-untyped-def]
    session, enterprise_object
) -> None:
    session.delete(enterprise_object)
    with pytest.raises(ValueError, match="scheduled for deletion"):
        AuditService.record(
            session,
            subject=enterprise_object,
            action=ENTERPRISE_OBJECT_UPDATED,
            content={"type": ["business_request", "process"]},
        )


# --- (16)-(17): derived workspace/column, expected_workspace_id ------------


def test_record_derives_workspace_and_populates_exactly_one_column(  # type: ignore[no-untyped-def]
    session, task, workspace
) -> None:
    AuditService.record(
        session, subject=task, action=TASK_CREATED, content={"phase": [None, "active"]}
    )

    records = audit_record_repository.list_by_workspace(session, workspace.id)
    assert len(records) == 1
    record = records[0]
    assert record.workspace_id == workspace.id
    assert record.subject_task_id == task.id
    assert record.subject_enterprise_object_id is None
    assert record.subject_workspace_id is None
    assert record.subject_user_id is None
    assert record.subject_workspace_membership_id is None


def test_matching_expected_workspace_id_is_accepted(  # type: ignore[no-untyped-def]
    session, enterprise_object, workspace
) -> None:
    AuditService.record(
        session,
        subject=enterprise_object,
        action=ENTERPRISE_OBJECT_CREATED,
        content={"type": [None, "business_request"]},
        expected_workspace_id=workspace.id,
    )

    records = audit_record_repository.list_by_workspace(session, workspace.id)
    assert len(records) == 1
    record = records[0]
    assert record.workspace_id == workspace.id


def test_mismatched_expected_workspace_id_is_rejected(  # type: ignore[no-untyped-def]
    session, enterprise_object
) -> None:
    with pytest.raises(ValueError, match="workspace mismatch"):
        AuditService.record(
            session,
            subject=enterprise_object,
            action=ENTERPRISE_OBJECT_CREATED,
            content={"type": [None, "business_request"]},
            expected_workspace_id=uuid.uuid4(),
        )


# --- (18): deep detachment and tuple normalization --------------------------


def test_content_tuple_pairs_are_normalized_and_deeply_detached(  # type: ignore[no-untyped-def]
    session, task
) -> None:
    """A shallow copy would fail the mutation assertion below; a naive
    `dict(content)` would fail the list-normalization assertion -- the
    round trip through `json.dumps`/`json.loads` is what satisfies both
    at once."""
    caller_content = {"tags": (["a"], ["b"])}

    AuditService.record(
        session, subject=task, action=TASK_CREATED, content=caller_content
    )

    records = audit_record_repository.list_by_workspace(session, task.workspace_id)
    assert len(records) == 1
    record = records[0]

    assert record.content["tags"] == [["a"], ["b"]]
    assert isinstance(record.content["tags"][0], list)

    caller_content["tags"][0].append("mutated")
    assert record.content["tags"] == [["a"], ["b"]]


# --- (19)-(20): checks 8 and 9, unreachable from the unit suite ------------


def test_subject_with_id_nulled_in_memory_is_rejected(  # type: ignore[no-untyped-def]
    session, task
) -> None:
    """Reaches check 8, which the unit suite cannot exercise: nulling an
    attribute in memory leaves a persistent, same-session instance
    persistent and attached until the next flush.

    No query follows the mutation, and the transaction is rolled back
    explicitly: `Session(bind=connection)` here has autoflush ON (unlike
    `SessionLocal` in `app/db/session.py`), so a query would flush the
    null `id` straight into a NOT NULL violation unrelated to the branch
    under test.
    """
    task.id = None
    with pytest.raises(ValueError, match="id must be set"):
        AuditService.record(
            session, subject=task, action=TASK_CREATED, content={"phase": [None, "active"]}
        )
    session.rollback()


def test_subject_with_workspace_id_nulled_in_memory_is_rejected(  # type: ignore[no-untyped-def]
    session, task
) -> None:
    """Reaches check 9, for the same reason item 19 reaches check 8. No
    query follows the mutation; the transaction is rolled back
    explicitly, for the same autoflush reason."""
    task.workspace_id = None
    with pytest.raises(ValueError, match="workspace_id must be set"):
        AuditService.record(
            session, subject=task, action=TASK_CREATED, content={"phase": [None, "active"]}
        )
    session.rollback()


# --- Atomicity ---------------------------------------------------------


def test_atomicity_same_transaction_co_visibility(  # type: ignore[no-untyped-def]
    session, workspace, user
) -> None:
    """Business mutation and its audit record, flushed through one
    session and one transaction, are both visible from a second session
    on the same connection. Not a durable-commit proof: the fixture
    deliberately never commits its outer transaction -- see the module
    docstring.
    """
    obj = EnterpriseObject(
        workspace_id=workspace.id, type="business_request", owner_id=user.id
    )
    session.add(obj)
    session.flush()

    AuditService.record(
        session,
        subject=obj,
        action=ENTERPRISE_OBJECT_CREATED,
        content={"type": [None, "business_request"]},
    )

    records = audit_record_repository.list_by_workspace(session, workspace.id)
    assert len(records) == 1
    record = records[0]
    record_id = record.id

    assert _visible_in_a_second_session(session, EnterpriseObject, obj.id)
    assert _visible_in_a_second_session(session, AuditRecord, record_id)


def test_atomicity_audit_side_failure_rolls_back_both(  # type: ignore[no-untyped-def]
    session, workspace, user
) -> None:
    """The failure is induced at the database level, deliberately: a
    service-level rejection raises before anything is added to the
    session and is a different path, already covered by the check-8/9
    tests above and by `tests/test_audit_service.py`. Here the business
    mutation genuinely reaches the database, and the audit half fails the
    exactly-one CHECK -- a real, database-level all-or-nothing case.
    """
    obj = EnterpriseObject(
        workspace_id=workspace.id, type="business_request", owner_id=user.id
    )
    session.add(obj)
    session.flush()
    obj_id = obj.id

    bad_audit_id = uuid.uuid4()
    bad_audit = AuditRecord(
        id=bad_audit_id,
        workspace_id=workspace.id,
        action="test.atomicity_audit_failure",
        content={"x": 1},
    )

    with pytest.raises(IntegrityError):
        audit_record_repository.add(session, bad_audit)

    session.rollback()

    assert not _visible_in_a_second_session(session, EnterpriseObject, obj_id)
    assert not _visible_in_a_second_session(session, AuditRecord, bad_audit_id)


def test_atomicity_business_mutation_failure_after_audit_flush(  # type: ignore[no-untyped-def]
    session, workspace, user
) -> None:
    """A newly created object, not a pre-existing one: with a
    pre-existing row, rollback would only restore its previous phase, and
    the object would still exist rather than be gone. Using a freshly
    created object keeps this scenario's assertion -- neither the object
    nor the audit row exists after rollback -- literally true.
    """
    obj = EnterpriseObject(
        workspace_id=workspace.id, type="business_request", owner_id=user.id
    )
    session.add(obj)
    session.flush()
    obj_id = obj.id

    AuditService.record(
        session,
        subject=obj,
        action=ENTERPRISE_OBJECT_CREATED,
        content={"type": [None, "business_request"]},
    )

    records = audit_record_repository.list_by_workspace(session, workspace.id)
    assert len(records) == 1
    record = records[0]
    record_id = record.id

    obj.phase = "not-a-real-phase"
    with pytest.raises(IntegrityError):
        session.flush()

    session.rollback()

    assert not _visible_in_a_second_session(session, EnterpriseObject, obj_id)
    assert not _visible_in_a_second_session(session, AuditRecord, record_id)
