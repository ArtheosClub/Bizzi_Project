# 11_PAGINATION_FILTERING_SORTING.md

# Bizzi Platform

## Pagination, Filtering and Sorting Contracts

**Layer:** 28_API_CONTRACTS  
**Component Type:** API Contract Standard  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**Previous Document:** 10_ERROR_AND_VALIDATION_CONTRACTS.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the canonical pagination, filtering and sorting contracts for Bizzi Platform APIs.

It standardizes how list endpoints return large result sets, apply filters, order records and expose stable navigation behavior across all workspace-scoped API resources.

Core question:

```text
How should Bizzi APIs expose list results consistently, safely and efficiently across all API resource families?
```

---

# 2. Contract Scope

This document applies to all list-style endpoints in `28_API_CONTRACTS`, including:

```text
workspaces
operating-maps
operating-gaps
functions
responsibilities
agents
agent-recommendations
processes
tasks
decisions
memory-entries
audit-events
runtime-events
integrations
integration-sync-jobs
security-policies
dashboard-metrics
export-jobs
```

It defines:

- pagination model;
- page size rules;
- page token rules;
- common response shape;
- filtering conventions;
- date and timestamp filters;
- polymorphic reference filters;
- sorting conventions;
- default ordering;
- error behavior;
- MVP simplifications;
- future expansion path.

---

# 3. Core Principles

## 3.1 No Unbounded Lists

List endpoints must not return unlimited result sets.

Rule:

```text
Any endpoint that can grow over time must support pagination.
```

## 3.2 Workspace Scope First

Workspace-scoped list endpoints must always filter by workspace context from the path.

Example:

```text
GET /api/v1/workspaces/{workspace_id}/tasks
```

Rule:

```text
workspace_id from path is mandatory and cannot be overridden by query parameters.
```

## 3.3 Stable Field Names

Query parameters should use Data Model and API field names.

Examples:

```text
status
owner_user_id
source_object_type
source_object_id
created_after
created_before
```

## 3.4 Predictable Defaults

Every list endpoint should define default ordering and default page size.

---

# 4. Pagination Model

Recommended model:

```text
cursor-based pagination using page_token
```

Standard query parameters:

```text
page_size
page_token
```

Example:

```text
GET /api/v1/workspaces/{workspace_id}/tasks?page_size=50&page_token=opaque-token
```

Standard response fields:

```text
items
next_page_token
```

---

# 5. Standard List Response Shape

Canonical response:

```json
{
  "items": [],
  "next_page_token": null
}
```

Example:

```json
{
  "items": [
    {
      "id": "uuid",
      "workspace_id": "uuid",
      "title": "Review supplier contract",
      "status": "open",
      "created_at": "2026-07-01T09:00:00Z"
    }
  ],
  "next_page_token": "opaque-token"
}
```

Rule:

```text
Clients must treat page_token as opaque and must not parse it.
```

---

# 6. Page Size Rules

Recommended defaults:

```text
default page_size: 50
maximum page_size: 100
minimum page_size: 1
```

Endpoint-specific exceptions may apply:

```text
audit-events may default to 100
runtime-events may default to 100
dashboard summary does not require pagination
```

Validation:

```text
page_size must be integer
page_size must be within allowed range
invalid page_size returns validation_error
```

---

# 7. Page Token Rules

Page tokens should encode enough information to continue a query safely.

Token may include:

```text
last seen sort key
last seen id
filters hash
sort definition
workspace scope
expiration timestamp optional
```

Rules:

```text
page_token must be opaque
page_token must be bound to the original filter and sort context
page_token must not allow cross-workspace access
expired or invalid tokens should return validation_error
```

---

# 8. Default Sorting

Default list ordering should be consistent by resource type.

Recommended defaults:

| Resource Family | Default Sort |
|---|---|
| tasks | created_at:desc |
| decisions | created_at:desc |
| memory-entries | updated_at:desc |
| audit-events | timestamp:desc |
| runtime-events | timestamp:desc |
| export-jobs | created_at:desc |
| integration-sync-jobs | created_at:desc |
| functions | name:asc |
| responsibilities | created_at:desc |
| operating-gaps | severity:desc,created_at:desc |
| workspaces | created_at:desc |

Rule:

```text
Default sorting must be documented per endpoint when it differs from created_at:desc.
```

---

# 9. Sorting Syntax

Recommended syntax:

```text
sort=<field>:<direction>
```

Examples:

```text
?sort=created_at:desc
?sort=name:asc
?sort=due_date:asc
?sort=priority:desc
```

Multiple sort fields may be supported later:

```text
?sort=status:asc,created_at:desc
```

MVP rule:

```text
Support one sort field per endpoint unless multiple ordering is required.
```

---

# 10. Allowed Sort Fields

Allowed sort fields should be endpoint-specific.

Common sort fields:

```text
created_at
updated_at
name
title
status
due_date
priority
confirmed_at
timestamp
completed_at
```

Rules:

```text
Only documented fields may be used for sorting.
Sorting by JSONB metadata fields is not supported in MVP.
Sorting must be backed by safe query patterns and indexes where needed.
```

---

# 11. Filtering Syntax

Recommended filtering style:

```text
?field=value
```

Examples:

```text
?status=open
?owner_user_id=uuid
?function_id=uuid
?memory_type=decision_summary
?provider=github
```

Rule:

```text
Simple equality filters should use direct query parameters.
```

---

# 12. Common Filters

Common filters across resources:

```text
status
created_after
created_before
updated_after
updated_before
owner_user_id
created_by
source_object_type
source_object_id
object_type
object_id
agent_id
function_id
process_id
task_id
decision_id
```

---

# 13. Status Filters

Status filters should use canonical status values from `11_ENUMS_AND_STATUSES.md`.

Example:

```text
GET /api/v1/workspaces/{workspace_id}/tasks?status=open
```

Multiple status values may be supported later:

```text
?status=open,in_progress
```

MVP rule:

```text
Support one status value per request unless endpoint specifically needs multi-status filtering.
```

---

# 14. Date and Timestamp Filters

Date-only filters should use:

```text
YYYY-MM-DD
```

Timestamp filters should use ISO 8601 UTC timestamps.

Examples:

```text
?due_before=2026-07-15
?created_after=2026-07-01T00:00:00Z
?from_timestamp=2026-07-01T00:00:00Z
?to_timestamp=2026-07-02T00:00:00Z
```

Rules:

```text
_after means exclusive or inclusive must be documented per endpoint
_before means exclusive or inclusive must be documented per endpoint
from_timestamp should be inclusive
to_timestamp should be exclusive by default
```

Recommended default:

```text
from_timestamp inclusive
to_timestamp exclusive
```

---

# 15. Polymorphic Reference Filters

Bizzi uses polymorphic references for source, object, result and resolution links.

Common filter pairs:

```text
source_object_type
source_object_id
object_type
object_id
result_object_type
result_object_id
resolved_by_object_type
resolved_by_object_id
```

Rule:

```text
If object_id is provided, object_type should also be required unless the endpoint context makes type unambiguous.
```

Example:

```text
GET /api/v1/workspaces/{workspace_id}/audit-events?object_type=task&object_id=uuid
```

---

# 16. Search Query Parameter

Some endpoints may support text search.

Recommended parameter:

```text
q
```

Examples:

```text
GET /api/v1/workspaces/{workspace_id}/tasks?q=supplier
GET /api/v1/workspaces/{workspace_id}/memory-entries?q=approval
```

MVP rule:

```text
Text search is optional and should be added only where product behavior requires it.
```

---

# 17. Include Parameters

Some endpoints may support optional embedded related data.

Recommended parameter:

```text
include
```

Examples:

```text
?include=owner,function
?include=steps
?include=recent_activity
```

Rules:

```text
include values must be explicitly documented
include should not bypass authorization
include should not expose sensitive metadata by default
```

MVP rule:

```text
Prefer simple resource responses before introducing complex include behavior.
```

---

# 18. Archived Records

Default behavior:

```text
Archived records should be excluded from normal list endpoints unless requested.
```

Recommended filter:

```text
include_archived=true
```

or:

```text
status=archived
```

Rule:

```text
If status filter is supplied, it overrides default active-only behavior where appropriate.
```

---

# 19. Security and Authorization Filtering

List endpoints must apply authorization filters before returning data.

Rules:

```text
users only see resources in workspaces they can access
workspace_id path scope must be enforced server-side
role-based visibility must be enforced before pagination
audit and runtime event visibility may be more restricted than normal resources
export visibility may depend on export scope
```

---

# 20. Error Behavior

Common errors:

```text
validation_error
forbidden
not_found
workspace_archived
invalid_object_reference
```

Invalid filter example:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [
      {
        "field": "status",
        "issue": "invalid_value",
        "message": "status is not valid for this endpoint"
      }
    ],
    "correlation_id": "uuid"
  }
}
```

Invalid sort example:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [
      {
        "field": "sort",
        "issue": "unsupported_sort_field",
        "message": "Sorting by metadata is not supported for this endpoint"
      }
    ],
    "correlation_id": "uuid"
  }
}
```

---

# 21. Endpoint Filter Examples

## Tasks

```text
GET /api/v1/workspaces/{workspace_id}/tasks?status=open&owner_user_id=uuid&sort=due_date:asc&page_size=50
```

## Decisions

```text
GET /api/v1/workspaces/{workspace_id}/decisions?status=confirmed&decision_date_from=2026-07-01&sort=decision_date:desc
```

## Memory Entries

```text
GET /api/v1/workspaces/{workspace_id}/memory-entries?status=active&memory_type=decision_summary&q=supplier
```

## Audit Events

```text
GET /api/v1/workspaces/{workspace_id}/audit-events?object_type=task&object_id=uuid&from_timestamp=2026-07-01T00:00:00Z
```

## Export Jobs

```text
GET /api/v1/workspaces/{workspace_id}/export-jobs?status=completed&export_type=workspace_summary
```

---

# 22. Performance Expectations

Pagination, filtering and sorting must align with `27_DATA_MODEL/12_INDEXING_STRATEGY.md`.

Rules:

```text
high-frequency filters should have supporting indexes
workspace_id should be part of operating resource indexes
sort fields used with filters should be index-aware
unbounded deep pagination should be avoided
```

---

# 23. MVP Simplifications

For MVP, Bizzi may simplify by:

- supporting page_size and page_token only;
- supporting one sort field per endpoint;
- supporting single-value filters only;
- excluding archived records by default;
- omitting include expansions;
- adding q search only for tasks and memory if needed;
- using created_at:desc as default for most resources.

These simplifications must preserve workspace scope and predictable list behavior.

---

# 24. Future Expansion

Future expansion may add:

```text
multi-value filters
advanced search
saved filters
cursor expiration metadata
include expansions
field selection
aggregation filters
faceted filtering
semantic search for memory
full-text search for tasks and decisions
```

---

# 25. Acceptance Criteria

Pagination, Filtering and Sorting Contracts are accepted when:

- standard list response shape is defined;
- page_size and page_token rules are defined;
- default sorting rules are documented;
- sorting syntax is standardized;
- common filters are documented;
- status, date and polymorphic filters are defined;
- archived record behavior is defined;
- error behavior is defined;
- endpoint examples are provided;
- MVP simplifications are documented.

Status:

```text
Accepted for API Contracts Milestone
```

---

# 26. Final Statement

```text
Bizzi Pagination, Filtering and Sorting Contracts define how all list endpoints expose scalable, predictable, workspace-scoped and implementation-ready collection access.
```

This standard completes the shared API behavior foundation for the `28_API_CONTRACTS` layer.