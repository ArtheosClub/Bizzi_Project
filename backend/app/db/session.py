"""SQLAlchemy engine and session factory.

Sync engine/session (not async) — MVP simplicity per principle B15; nothing
in Gate B needs async DB access, and Alembic's autogenerate tooling is most
straightforward against a sync engine. Revisit only if a real need for
async DB access is demonstrated.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

engine = create_engine(get_settings().database_url, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
