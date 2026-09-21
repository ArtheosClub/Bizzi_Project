"""AuditActions — the ADR-0005 named-constant action vocabulary for WP19's
bounded AuditService scope.

ADR-0005 requires audit actions to be named constants, never ad-hoc
strings, precisely so a repository-wide search can find every place a
given business event is recorded.

The vocabulary is bounded to A-11's callable slice, not to every
mutation WP13/WP15 will eventually perform. A constant existing here
authorizes nothing by itself -- the create/update code paths on
EnterpriseObject and Task remain WP13/WP15 work; this module only names
what `AuditService.record(...)` accepts once those callers exist.

`TASK_COMPLETED` is deliberately absent. Completion is a phase
transition, and transition semantics belong to the ADR-0011 transition
service, which A-11 does not authorize as part of this bounded scope.
Adding it to the admissibility table would incorrectly allow
`AuditService.record(...)` to accept that action.

The compatibility mapping is immutable so ordinary runtime mutation cannot
widen the service-admissibility surface without review.
"""

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from app.models.enterprise_object import EnterpriseObject
from app.models.task import Task

ENTERPRISE_OBJECT_CREATED = "enterprise_object.created"
ENTERPRISE_OBJECT_UPDATED = "enterprise_object.updated"
TASK_CREATED = "task.created"
TASK_UPDATED = "task.updated"

#: The bounded service-admissibility surface: which actions may be recorded
#: against which subject type. A-11 grants the authorization; this table only
#: encodes the admissible pairs. `MappingProxyType` prevents accidental or
#: ordinary runtime widening by mutation -- it does not make the table
#: unreachable, since a module attribute can still be rebound, and `Final` is
#: enforced by static analysis only. `AuditService.record(...)` is what applies
#: the table.
ALLOWED_ACTIONS_BY_SUBJECT_TYPE: Final[Mapping[type, frozenset[str]]] = (
    MappingProxyType(
        {
            EnterpriseObject: frozenset(
                {ENTERPRISE_OBJECT_CREATED, ENTERPRISE_OBJECT_UPDATED}
            ),
            Task: frozenset({TASK_CREATED, TASK_UPDATED}),
        }
    )
)
