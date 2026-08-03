"""Model aggregation — every ORM model must be imported here.

`Base.metadata` is populated as a side effect of a model class being
*defined*, which only happens when its module is imported. Alembic's
`env.py` imports this package precisely so that `target_metadata` reflects
every table before autogenerate runs.

**A model that is not imported here is invisible to autogenerate.** The
failure mode is not a missing migration — it is worse than that: once real
tables exist and metadata is empty (or partial), `alembic revision
--autogenerate` reads the difference as "these tables should not exist"
and emits `DROP TABLE` for them. That is data loss, not a style problem.

So: when you add a model, add it here in the same commit. The `__all__`
entry is what keeps the import from being removed as unused by a linter.
"""

from app.models.enterprise_object import EnterpriseObject
from app.models.workspace import Workspace

__all__ = ["EnterpriseObject", "Workspace"]
