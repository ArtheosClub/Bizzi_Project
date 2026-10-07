"""Reject destinations and libpq query overrides before any connection."""

import pytest

from app.core.preproduction_guard import ScopeViolationError, require_test_destination


def test_exact_test_destination_allowed():
    require_test_destination("postgresql+psycopg://bizzi@localhost:5433/bizzi_test")


@pytest.mark.parametrize(
    "url",
    [
        "postgresql+psycopg://bizzi@localhost:5432/bizzi_dev",
        "postgresql+psycopg://remote:5433/bizzi_test",
        "postgresql+psycopg://127.0.0.1:5433/bizzi_test",
        "postgresql+psycopg://localhost/bizzi_test",
        "postgresql+psycopg://bizzi@localhost:5433/bizzi_test?host=remote",
        "not-a-url",
    ],
)
def test_other_destinations_rejected_without_values(url):
    with pytest.raises(ScopeViolationError) as caught:
        require_test_destination(url)
    assert str(caught.value) == "Database destination is outside record-5 scope"


CI_NAMES = (
    "GITHUB_REPOSITORY", "GITHUB_REPOSITORY_OWNER", "GITHUB_WORKFLOW_REF",
    "GITHUB_JOB", "GITHUB_EVENT_NAME", "GITHUB_REF", "GITHUB_BASE_REF",
    "GITHUB_HEAD_REF", "BIZZI_PR_HEAD_REPOSITORY", "BIZZI_PR_HEAD_SHA",
    "BIZZI_CHECKOUT_SHA", "GITHUB_ACTIONS", "RUNNER_ENVIRONMENT",
)
CI_VALUES = (
    "ArtheosClub/Bizzi_Project", "ArtheosClub",
    "ArtheosClub/Bizzi_Project/.github/workflows/backend-ci.yml@refs/pull/1/merge",
    "backend", "pull_request", "refs/pull/1/merge", "main",
    "feat/wp15-bounded-task-service", "ArtheosClub/Bizzi_Project",
    "a" * 40, "a" * 40, "true", "github-hosted",
)


def test_exact_ci_context_and_destination_without_connection(monkeypatch):
    from app.core.preproduction_guard import resolve_policy

    for name, value in zip(CI_NAMES, CI_VALUES, strict=True):
        monkeypatch.setenv(name, value)
    policy = resolve_policy("ci_test")
    require_test_destination("postgresql+psycopg://bizzi@localhost:5432/bizzi_test", policy)
    with pytest.raises(ScopeViolationError):
        require_test_destination("postgresql+psycopg://bizzi@localhost:5433/bizzi_test", policy)
    with pytest.raises(ScopeViolationError):
        require_test_destination("postgresql+psycopg://bizzi@postgres-test:5432/bizzi_test", policy)


@pytest.mark.parametrize("name", CI_NAMES)
def test_missing_or_changed_ci_context_refused(monkeypatch, name):
    from app.core.preproduction_guard import resolve_policy

    for key, value in zip(CI_NAMES, CI_VALUES, strict=True):
        monkeypatch.setenv(key, value)
    monkeypatch.delenv(name)
    with pytest.raises(ScopeViolationError):
        resolve_policy("ci_test")
    monkeypatch.setenv(name, "unadmitted")
    with pytest.raises(ScopeViolationError):
        resolve_policy("ci_test")
