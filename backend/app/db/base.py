"""Declarative base for ORM models.

Empty of real models for now — Gate C (domain models: Object, Task, Event,
Agent) is explicitly out of scope for this Gate B pass. This exists now so
Alembic's env.py has a stable `target_metadata` to import from, instead of
being retrofitted when the first model lands.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
