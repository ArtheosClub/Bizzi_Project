"""Explicit local policy: not authority, provenance or a general ORM sandbox."""

import os
import re
from dataclasses import dataclass

from sqlalchemy.engine import URL, Connection, Engine, make_url
from sqlalchemy.orm import Session

PG_OVERRIDES = (
    "PGHOST",
    "PGHOSTADDR",
    "PGPORT",
    "PGDATABASE",
    "PGUSER",
    "PGSERVICE",
    "PGSERVICEFILE",
    "PGSYSCONFDIR",
    "PGOPTIONS",
    "PGPASSFILE",
)
POLICY_KEY = "execution_policy"


class ScopeViolationError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class CIContext:
    repository: str
    owner: str
    workflow_ref: str
    job: str
    event: str
    ref: str
    base_ref: str
    head_ref: str
    head_repository: str
    head_sha: str
    checkout_sha: str
    actions: str
    runner_environment: str


@dataclass(frozen=True, slots=True)
class ExecutionPolicy:
    profile: str
    context: CIContext | None = None


LOCAL_TEST_POLICY = ExecutionPolicy("local_test")


def _require_ci_context(context: CIContext | None, job: str = "backend") -> None:
    if type(context) is not CIContext:
        raise ScopeViolationError("Synthetic CI context is outside admitted policy")
    valid = (
        context.repository == "ArtheosClub/Bizzi_Project"
        and context.owner == "ArtheosClub"
        and context.job == job
        and context.event == "pull_request"
        and context.base_ref == "main"
        and context.head_ref == "feat/wp15-bounded-task-service"
        and context.head_repository == context.repository
        and context.actions == "true"
        and context.runner_environment == "github-hosted"
        and re.fullmatch(r"refs/pull/[1-9][0-9]*/merge", context.ref) is not None
        and context.workflow_ref
        == f"{context.repository}/.github/workflows/backend-ci.yml@{context.ref}"
        and re.fullmatch(r"[0-9a-f]{40}", context.head_sha) is not None
        and context.checkout_sha == context.head_sha
    )
    if not valid:
        raise ScopeViolationError("Synthetic CI context is outside admitted policy")


def resolve_policy(profile: str) -> ExecutionPolicy:
    """Context corroborates the job; it is not Owner authority or provenance."""
    if profile in {"ci_test", "ci_compose"}:
        names = (
            "GITHUB_REPOSITORY", "GITHUB_REPOSITORY_OWNER", "GITHUB_WORKFLOW_REF",
            "GITHUB_JOB", "GITHUB_EVENT_NAME", "GITHUB_REF", "GITHUB_BASE_REF",
            "GITHUB_HEAD_REF", "BIZZI_PR_HEAD_REPOSITORY", "BIZZI_PR_HEAD_SHA",
            "BIZZI_CHECKOUT_SHA", "GITHUB_ACTIONS", "RUNNER_ENVIRONMENT",
        )
        policy = ExecutionPolicy(profile, CIContext(*(os.environ.get(n, "") for n in names)))
    else:
        policy = ExecutionPolicy(profile)
    return require_policy(policy)


def require_policy(policy: object) -> ExecutionPolicy:
    if type(policy) is not ExecutionPolicy:
        raise ScopeViolationError("Synthetic execution is outside admitted local policy")
    if policy.profile == "local_test" and policy.context is None:
        return policy
    if policy.profile in {"ci_test", "ci_compose"}:
        _require_ci_context(
            policy.context, "compose-e2e" if policy.profile == "ci_compose" else "backend"
        )
        return policy
    raise ScopeViolationError("Synthetic execution is outside admitted local policy")


def require_test_destination(database_url: str | URL, policy: object = LOCAL_TEST_POLICY) -> None:
    selected = require_policy(policy)
    if any(os.environ.get(name) for name in PG_OVERRIDES):
        raise ScopeViolationError("Inherited connection override is outside local policy")
    try:
        url = make_url(database_url)
        valid = (
            url.drivername == "postgresql+psycopg"
            and url.host == ("postgres-test" if selected.profile == "ci_compose" else "localhost")
            and url.port == (5433 if selected.profile == "local_test" else 5432)
            and url.database == "bizzi_test"
            and url.username == "bizzi"
            and not url.query
        )
    except Exception:
        raise ScopeViolationError("Database destination is outside record-5 scope") from None
    if not valid:
        raise ScopeViolationError("Database destination is outside record-5 scope")


def require_engine(engine: Engine, policy: object) -> None:
    require_test_destination(engine.url, policy)


def require_business_policy(policy: object) -> ExecutionPolicy:
    """Compose admits migrations/health, never a domain Session or intake."""
    selected = require_policy(policy)
    if selected.profile == "ci_compose":
        raise ScopeViolationError("Compose business execution is outside admitted policy")
    return selected


def require_session(session: Session) -> None:
    policy = require_business_policy(session.info.get(POLICY_KEY))
    bind = session.get_bind()
    engine = bind.engine if isinstance(bind, Connection) else bind
    require_engine(engine, policy)
