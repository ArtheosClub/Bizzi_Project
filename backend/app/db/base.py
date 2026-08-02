"""Declarative base for ORM models.

The naming convention below is deliberately established before the first
table exists. Postgres auto-names any constraint it is not given a name
for (`workspaces_pkey`, `workspaces_owner_id_key`, …), and those generated
names are exactly what a later migration must target in
`DROP CONSTRAINT` / `ALTER CONSTRAINT`. Adding a convention after tables
exist forces a rename-churn migration against live schema; adding it now,
against zero tables, changes no existing DDL and costs nothing.

Models are deliberately not imported here. `app.models` owns aggregation
(see its docstring) — importing it from this module would create a cycle,
since `app.models.workspace` imports `Base` from here.
"""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# Standard SQLAlchemy convention set. Note `ck` uses `%(constraint_name)s`,
# which requires every CheckConstraint to be given an explicit name.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)
