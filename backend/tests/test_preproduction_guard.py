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
    "GITHUB_HEAD_REF", "BIZZI_EVENT_HEAD_REPOSITORY", "BIZZI_EVENT_HEAD_SHA",
    "BIZZI_CHECKOUT_SHA", "GITHUB_ACTIONS", "RUNNER_ENVIRONMENT",
)
CI_VALUES = (
    "ArtheosClub/Bizzi_Project", "ArtheosClub",
    "ArtheosClub/Bizzi_Project/.github/workflows/backend-ci.yml@refs/pull/1/merge",
    "backend", "pull_request", "refs/pull/1/merge", "main",
    "feat/wp15-bounded-task-service", "ArtheosClub/Bizzi_Project",
    "a" * 40, "a" * 40, "true", "github-hosted",
)



def install_ci_environment(monkeypatch, values):
    # Real main-push CI also runs PR-negative fixtures: do not inherit its context.
    for key in (*CI_NAMES, "GITHUB_SHA", "BIZZI_PUSH_BEFORE", "BIZZI_PUSH_AFTER",
                "BIZZI_PUSH_FORCED", "BIZZI_PUSH_DELETED", "BIZZI_PR_HEAD_SHA",
                "BIZZI_PR_HEAD_REPOSITORY"):
        monkeypatch.delenv(key, raising=False)
    for key, value in values.items():
        monkeypatch.setenv(key, value)


def test_exact_ci_context_and_destination_without_connection(monkeypatch):
    from app.core.preproduction_guard import resolve_policy

    install_ci_environment(monkeypatch, dict(zip(CI_NAMES, CI_VALUES, strict=True)))
    policy = resolve_policy("ci_test")
    require_test_destination("postgresql+psycopg://bizzi@localhost:5432/bizzi_test", policy)
    with pytest.raises(ScopeViolationError):
        require_test_destination("postgresql+psycopg://bizzi@localhost:5433/bizzi_test", policy)
    with pytest.raises(ScopeViolationError):
        require_test_destination("postgresql+psycopg://bizzi@postgres-test:5432/bizzi_test", policy)


@pytest.mark.parametrize("name", CI_NAMES)
def test_missing_or_changed_ci_context_refused(monkeypatch, name):
    from app.core.preproduction_guard import resolve_policy

    install_ci_environment(monkeypatch, dict(zip(CI_NAMES, CI_VALUES, strict=True)))
    monkeypatch.delenv(name)
    with pytest.raises(ScopeViolationError):
        resolve_policy("ci_test")
    monkeypatch.setenv(name, "unadmitted")
    with pytest.raises(ScopeViolationError):
        resolve_policy("ci_test")


@pytest.mark.parametrize("name", CI_NAMES)
def test_compose_context_missing_or_changed_refused(monkeypatch, name):
    from app.core.preproduction_guard import resolve_policy

    values = list(CI_VALUES)
    values[3] = "compose-e2e"
    install_ci_environment(monkeypatch, dict(zip(CI_NAMES, values, strict=True)))
    monkeypatch.delenv(name)
    with pytest.raises(ScopeViolationError):
        resolve_policy("ci_compose")
    monkeypatch.setenv(name, "unadmitted")
    with pytest.raises(ScopeViolationError):
        resolve_policy("ci_compose")


def test_compose_migration_policy_never_business_policy(monkeypatch):
    from app.core.preproduction_guard import require_business_policy, resolve_policy

    env = dict(zip(CI_NAMES, CI_VALUES, strict=True))
    env["GITHUB_JOB"] = "compose-e2e"
    install_ci_environment(monkeypatch, env)
    policy = resolve_policy("ci_compose")
    require_test_destination("postgresql+psycopg://bizzi@postgres-test:5432/bizzi_test", policy)
    with pytest.raises(ScopeViolationError):
        require_business_policy(policy)
    for url in (
        "postgresql+psycopg://bizzi@localhost:5432/bizzi_test",
        "postgresql+psycopg://bizzi@postgres:5432/bizzi_dev",
        "postgresql+psycopg://bizzi@postgres-test:5433/bizzi_test",
        "postgresql+psycopg://other@postgres-test:5432/bizzi_test",
        "postgresql+psycopg://bizzi@postgres-test:5432/bizzi_test?host=remote",
    ):
        with pytest.raises(ScopeViolationError):
            require_test_destination(url, policy)
    monkeypatch.setenv("PGHOST", "unadmitted")
    with pytest.raises(ScopeViolationError):
        require_test_destination("postgresql+psycopg://bizzi@postgres-test:5432/bizzi_test", policy)


def push_context(job="backend", *, empty=True):
    values = dict(zip(CI_NAMES, CI_VALUES, strict=True))
    values.update(GITHUB_JOB=job, GITHUB_EVENT_NAME="push", GITHUB_REF="refs/heads/main",
                  GITHUB_WORKFLOW_REF="ArtheosClub/Bizzi_Project/.github/workflows/backend-ci.yml@refs/heads/main",
                  GITHUB_SHA="a" * 40, BIZZI_PUSH_BEFORE="b" * 40,
                  BIZZI_PUSH_AFTER="a" * 40, BIZZI_PUSH_FORCED="false", BIZZI_PUSH_DELETED="false")
    for key in ("GITHUB_BASE_REF", "GITHUB_HEAD_REF", "BIZZI_EVENT_HEAD_REPOSITORY"):
        if empty:
            values[key] = ""
        else:
            values.pop(key)
    return values


@pytest.mark.parametrize("empty", [False, True])
@pytest.mark.parametrize("profile,job", [("ci_test", "backend"), ("ci_compose", "compose-e2e")])
def test_main_push_accepts_absent_or_empty_pr_fields(monkeypatch, profile, job, empty):
    from app.core.preproduction_guard import require_business_policy, resolve_policy

    env = push_context(job, empty=empty)
    install_ci_environment(monkeypatch, env)
    policy = resolve_policy(profile)
    host = "postgres-test" if profile == "ci_compose" else "localhost"
    require_test_destination(f"postgresql+psycopg://bizzi@{host}:5432/bizzi_test", policy)
    if profile == "ci_compose":
        with pytest.raises(ScopeViolationError):
            require_business_policy(policy)


@pytest.mark.parametrize("key,value", [
    ("GITHUB_REF", "refs/heads/other"), ("GITHUB_SHA", "c" * 40),
    ("BIZZI_PUSH_AFTER", "c" * 40), ("BIZZI_PUSH_BEFORE", "bad"),
    ("BIZZI_PUSH_FORCED", "1"), ("BIZZI_PUSH_DELETED", "true"),
    ("GITHUB_BASE_REF", "main"), ("GITHUB_HEAD_REF", "feature"),
    ("BIZZI_EVENT_HEAD_REPOSITORY", "ArtheosClub/Bizzi_Project"),
    ("GITHUB_EVENT_NAME", "workflow_dispatch"), ("GITHUB_JOB", "other"),
    ("GITHUB_REPOSITORY", "other/repo"), ("RUNNER_ENVIRONMENT", "self-hosted"),
    ("BIZZI_PR_HEAD_SHA", ""), ("BIZZI_PR_HEAD_REPOSITORY", ""),
])
def test_bad_or_mixed_push_metadata_refuses(monkeypatch, key, value):
    from app.core.preproduction_guard import resolve_policy

    install_ci_environment(monkeypatch, push_context())
    monkeypatch.setenv(key, value)
    with pytest.raises(ScopeViolationError):
        resolve_policy("ci_test")


def test_forced_push_is_evidence_not_rewrite_authority(monkeypatch):
    from app.core.preproduction_guard import resolve_policy

    install_ci_environment(monkeypatch, push_context())
    monkeypatch.setenv("BIZZI_PUSH_FORCED", "true")
    assert resolve_policy("ci_test").context.push_forced == "true"


@pytest.mark.parametrize("profile,job", [("ci_test", "backend"), ("ci_compose", "compose-e2e")])
def test_pr_fixture_isolated_from_inherited_main_push(monkeypatch, profile, job):
    from app.core.preproduction_guard import resolve_policy

    for key, value in push_context(job).items():
        monkeypatch.setenv(key, value)
    env = dict(zip(CI_NAMES, CI_VALUES, strict=True))
    env["GITHUB_JOB"] = job
    install_ci_environment(monkeypatch, env)
    assert resolve_policy(profile).context.event == "pull_request"
