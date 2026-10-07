"""Lazy synthetic Session provider; prepare policy and Engine before connection."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.preproduction_guard import (
    POLICY_KEY,
    ExecutionPolicy,
    require_engine,
    require_test_destination,
)


def get_db_for_policy(policy: ExecutionPolicy) -> Generator[Session]:
    url = get_settings().database_url
    require_test_destination(url, policy)
    engine = create_engine(url, pool_pre_ping=True)
    require_engine(engine, policy)
    try:
        with Session(bind=engine, info={POLICY_KEY: policy}) as db:
            yield db
    finally:
        engine.dispose()


def get_db() -> Generator[Session]:
    yield from get_db_for_policy(ExecutionPolicy(get_settings().synthetic_execution_profile))
