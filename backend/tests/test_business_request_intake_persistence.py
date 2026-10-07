"""WP23 synthetic in-process verification; endpoint commits savepoint only."""

from contextlib import contextmanager

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event, func, select
from sqlalchemy.orm import Session

from app.api.business_request_intake import get_token_verifier
from app.core.preproduction_guard import LOCAL_TEST_POLICY, POLICY_KEY
from app.core.request_context import RequestIDMiddleware
from app.db.session import get_db
from app.main import create_application
from app.models import AuditRecord, EnterpriseObject, Task


@pytest.fixture
def intake_client(identity_db, owner_graph, verifier):
    connection = identity_db.connection()
    fastapi_app = create_application(LOCAL_TEST_POLICY)
    app = RequestIDMiddleware(fastapi_app)

    @contextmanager
    def client_session():
        with Session(
            bind=connection,
            join_transaction_mode="create_savepoint",
            info={POLICY_KEY: LOCAL_TEST_POLICY},
        ) as db:
            yield db

    def session_provider():
        with client_session() as db:
            yield db

    previous = dict(fastapi_app.dependency_overrides)
    fastapi_app.dependency_overrides[get_db] = session_provider
    fastapi_app.dependency_overrides[get_token_verifier] = lambda: verifier
    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            yield client
    finally:
        fastapi_app.dependency_overrides.clear()
        fastapi_app.dependency_overrides.update(previous)


def counts(db):
    return [
        db.scalar(select(func.count()).select_from(model))
        for model in (EnterpriseObject, Task, AuditRecord)
    ]


def post(client, body="{}", token="synthetic-test-token"):
    headers = {"Authorization": "Bearer " + token} if token else {}
    response = client.post("/business-requests", content=body, headers=headers)
    assert response.headers["X-Request-Id"]
    return response


def test_pair_created_and_attributed_after_savepoint_commit(
    intake_client, identity_db, owner_graph
):
    user, workspace, member = owner_graph
    response = post(intake_client)
    assert response.status_code == 201
    assert set(response.json()) == {"task_id"}
    assert counts(identity_db) == [1, 1, 2]
    task = identity_db.scalar(select(Task))
    obj = identity_db.scalar(select(EnterpriseObject))
    assert str(task.id) == response.json()["task_id"]
    assert task.phase == obj.phase == "active"
    assert task.source_object_id is None
    assert obj.type == "business_request" and obj.owner_id == user.id
    assert task.workspace_id == obj.workspace_id == workspace.id
    audits = list(identity_db.scalars(select(AuditRecord)))
    assert {a.action for a in audits} == {"task.created", "enterprise_object.created"}
    assert all(
        (a.actor_id, a.membership_id, a.workspace_id) == (user.id, member.id, workspace.id)
        for a in audits
    )
    assert any(a.subject_task_id == task.id for a in audits)
    assert any(a.subject_enterprise_object_id == obj.id for a in audits)


@pytest.mark.parametrize(
    "case,status",
    [
        ("no_token", 401),
        ("invalid_token", 401),
        ("expired", 401),
        ("wrong_issuer", 401),
        ("wrong_audience", 401),
        ("unbound", 404),
        ("deactivated", 404),
        ("extra", 422),
        ("malformed", 422),
        ("array", 422),
        ("empty", 422),
    ],
)
def test_denials_precede_validation_and_write_nothing(
    intake_client, identity_db, owner_graph, verifier, case, status
):
    token = "synthetic-test-token"
    body = "{"
    if case == "no_token":
        token = None
    if case == "invalid_token":
        token = "invalid"
    if case == "expired":
        verifier.claims["exp"] = 0
    if case == "wrong_issuer":
        verifier.claims["iss"] = "wrong-synthetic-issuer"
    if case == "wrong_audience":
        verifier.claims["aud"] = "wrong-synthetic-audience"
    if case == "unbound":
        verifier.claims["sub"] = "unbound-synthetic"
    if case == "deactivated":
        from datetime import UTC, datetime

        owner_graph[0].deactivated_at = datetime.now(UTC)
        identity_db.flush()
    if case == "extra":
        body = '{"workspace_id":"synthetic"}'
    if case == "array":
        body = "[]"
    if case == "empty":
        body = ""
    response = post(intake_client, body, token)
    assert response.status_code == status
    assert (
        response.json()["error"]["code"]
        == {401: "unauthenticated", 404: "not_found", 422: "validation_error"}[status]
    )
    assert counts(identity_db) == [0, 0, 0]


@pytest.mark.parametrize(
    "point", ["eo", "task", "eo_audit", "task_audit", "after_audits", "commit"]
)
def test_failure_rolls_back_pair_and_sanitizes_500(intake_client, identity_db, monkeypatch, point):
    def fail(mapper, connection, target):
        if (
            point in {"eo", "task"}
            or (point == "eo_audit" and target.action == "enterprise_object.created")
            or (point == "task_audit" and target.action == "task.created")
        ):
            raise ValueError("synthetic-private SQL database-identifier credential-marker")

    model = EnterpriseObject if point == "eo" else Task if point == "task" else AuditRecord
    if point == "after_audits":
        from app.services.business_request_intake_service import BusinessRequestIntakeService

        original = BusinessRequestIntakeService.create

        def after(*args, **kwargs):
            original(*args, **kwargs)
            raise ValueError("synthetic-private")

        monkeypatch.setattr(BusinessRequestIntakeService, "create", after)
    elif point == "commit":

        def before_commit(db):
            raise ValueError("synthetic-private")

        event.listen(Session, "before_commit", before_commit)
    else:
        event.listen(model, "before_insert", fail)
    try:
        response = post(intake_client)
    finally:
        if point == "commit":
            event.remove(Session, "before_commit", before_commit)
        elif point != "after_audits":
            event.remove(model, "before_insert", fail)
    assert response.status_code == 500
    assert response.json() == {
        "error": {"code": "internal_error", "message": "Unexpected server error."}
    }
    assert counts(identity_db) == [0, 0, 0]
