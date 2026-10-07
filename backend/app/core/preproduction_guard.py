"""Explicit local policy: not authority, provenance or a general ORM sandbox."""

import os
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
class ExecutionPolicy:
    profile: str


LOCAL_TEST_POLICY = ExecutionPolicy("local_test")


def require_policy(policy: object) -> ExecutionPolicy:
    if type(policy) is not ExecutionPolicy or policy.profile != "local_test":
        raise ScopeViolationError("Synthetic execution is outside admitted local policy")
    return policy


def require_test_destination(database_url: str | URL, policy: object = LOCAL_TEST_POLICY) -> None:
    require_policy(policy)
    if any(os.environ.get(name) for name in PG_OVERRIDES):
        raise ScopeViolationError("Inherited connection override is outside local policy")
    try:
        url = make_url(database_url)
        valid = (
            url.drivername == "postgresql+psycopg"
            and url.host == "localhost"
            and url.port == 5433
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


def require_session(session: Session) -> None:
    policy = require_policy(session.info.get(POLICY_KEY))
    bind = session.get_bind()
    engine = bind.engine if isinstance(bind, Connection) else bind
    require_engine(engine, policy)
