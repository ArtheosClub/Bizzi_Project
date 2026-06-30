# 05_FUNCTION_RESPONSIBILITY_API.md

# Bizzi Platform

## Function Responsibility API

**Layer:** 28_API_CONTRACTS  
**Component Type:** API Contract Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 05_PROCESS_RUNTIME.md  
**Domain Reference:** 26_DOMAIN_MODEL / 04_FUNCTION_AND_RESPONSIBILITY_DOMAIN.md  
**Data Model Reference:** 27_DATA_MODEL / 06_FUNCTION_RESPONSIBILITY_DATA_MODEL.md  
**Previous Document:** 04_OPERATING_MAP_API.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Function Responsibility API contract for Bizzi Platform.

The Function Responsibility API exposes operations for creating, reading, updating, archiving and governing business functions, responsibilities and ownership gaps inside a workspace.

Core question:

```text
How should Bizzi expose business functions and responsibility ownership through stable, workspace-scoped, auditable and implementation-ready API contracts?
```

---

# 2. API Scope

This document covers:

```text
functions
responsibilities
ownership-gaps
```

Primary data model references:

```text
functions
responsibilities
ownership_gaps
```

MVP scope:

```text
functions
responsibilities
```

Near-MVP / P2 scope:

```text
ownership-gaps
```

---

# 3. Design Principles Applied

The Function Responsibility API follows:

```text
Workspace First
Resource-Oriented Contracts
Explicit State Transitions
Audit-Aware Mutations
Runtime Event Awareness
Stable Field Names
Safe Defaults
OpenAPI Readiness
```

---

# 4. Base Paths

Workspace-scoped paths:

```text
/api/v1/workspaces/{workspace_id}/functions
/api/v1/workspaces/{workspace_id}/responsibilities
/api/v1/workspaces/{workspace_id}/ownership-gaps
```

Rule:

```text
All function and responsibility resources are workspace-scoped.
```

---

# 5. Resource: Functions

## Resource Name

```text
functions
```

## Purpose

Represent business functions and capabilities inside a workspace.

## Data Model Reference

```text
functions
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "parent_function_id": null,
  "name": "Finance",
  "description": "Financial management and reporting function",
  "category": "finance",
  "status": "active",
  "risk_level": "medium",
  "source_object_type": "operating_gap",
  "source_object_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:15:00Z",
  "metadata": {}
}
```

---

# 6. Endpoint: List Functions

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/functions
```

## Purpose

List workspace functions.

## Query Parameters

```text
status optional
category optional
parent_function_id optional
risk_level optional
page_size optional
page_token optional
sort optional
```

## Response: 200 OK

```json
{
  "items": [
    {
      "id": "uuid",
      "workspace_id": "uuid",
      "parent_function_id": null,
      "name": "Finance",
      "category": "finance",
      "status": "active",
      "risk_level": "medium",
      "created_at": "2026-07-01T09:00:00Z",
      "updated_at": "2026-07-01T09:15:00Z"
    }
  ],
  "next_page_token": null
}
```

## Authorization

```text
User must have access to workspace.
```

---

# 7. Endpoint: Create Function

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/functions
```

## Purpose

Create a new business function in a workspace.

## Request Body

```json
{
  "name": "Finance",
  "description": "Financial management and reporting function",
  "category": "finance",
  "parent_function_id": null,
  "risk_level": "medium",
  "source_object_type": "operating_gap",
  "source_object_id": "uuid"
}
```

## Required Fields

```text
name
```

## Optional Fields

```text
description
category
parent_function_id
risk_level
source_object_type
source_object_id
```

## Response: 201 Created

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "parent_function_id": null,
  "name": "Finance",
  "description": "Financial management and reporting function",
  "category": "finance",
  "status": "active",
  "risk_level": "medium",
  "source_object_type": "operating_gap",
  "source_object_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

## Validation Rules

```text
name is required
category must be valid if provided
risk_level must be valid if provided
parent_function_id must belong to same workspace if provided
source_object_type must be valid if provided
source_object_id must exist if provided
source object must belong to same workspace if workspace-scoped
```

## Authorization

```text
Workspace owner or authorized manager.
```

## Audit Events

```text
function.created
```

## Runtime Events

```text
function.created
dashboard.refresh_requested
```

---

# 8. Endpoint: Get Function

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/functions/{function_id}
```

## Purpose

Retrieve a single function.

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "parent_function_id": null,
  "name": "Finance",
  "description": "Financial management and reporting function",
  "category": "finance",
  "status": "active",
  "risk_level": "medium",
  "source_object_type": "operating_gap",
  "source_object_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:15:00Z",
  "metadata": {}
}
```

## Authorization

```text
User must have access to workspace.
```

---

# 9. Endpoint: Update Function

## Method and Path

```text
PATCH /api/v1/workspaces/{workspace_id}/functions/{function_id}
```

## Purpose

Update mutable function fields.

## Request Body

```json
{
  "name": "Finance and Reporting",
  "description": "Updated finance function description",
  "category": "finance",
  "risk_level": "high"
}
```

## Mutable Fields

```text
name
description
category
parent_function_id
risk_level
metadata
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "name": "Finance and Reporting",
  "category": "finance",
  "risk_level": "high",
  "status": "active",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

## Validation Rules

```text
function must belong to workspace
name cannot be empty if provided
category must be valid if provided
risk_level must be valid if provided
parent_function_id must belong to same workspace if provided
archived functions cannot be updated through normal update flow
```

## Authorization

```text
Workspace owner or authorized manager.
```

## Audit Events

```text
function.updated
```

## Runtime Events

```text
function.updated
dashboard.refresh_requested
```

---

# 10. Endpoint: Archive Function

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/functions/{function_id}/archive
```

## Purpose

Archive a function while preserving history.

## Request Body

```json
{
  "archive_reason": "Function merged into operations"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "archived",
  "archived_at": "2026-07-01T12:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

## Validation Rules

```text
function must belong to workspace
function must not already be archived
active responsibilities, processes or tasks may require review before archive
```

## Authorization

```text
Workspace owner or authorized manager.
```

## Audit Events

```text
function.archived
```

## Runtime Events

```text
function.archived
dashboard.refresh_requested
```

---

# 11. Resource: Responsibilities

## Resource Name

```text
responsibilities
```

## Purpose

Represent responsibility assignments for functions or other operating objects.

## Data Model Reference

```text
responsibilities
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "object_type": "function",
  "object_id": "uuid",
  "responsibility_type": "owner",
  "owner_user_id": "uuid",
  "status": "assigned",
  "assigned_by": "uuid",
  "assigned_at": "2026-07-01T09:00:00Z",
  "source_object_type": "operating_gap",
  "source_object_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

---

# 12. Endpoint: List Responsibilities

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/responsibilities
```

## Query Parameters

```text
status optional
object_type optional
object_id optional
owner_user_id optional
responsibility_type optional
page_size optional
page_token optional
sort optional
```

## Response: 200 OK

```json
{
  "items": [
    {
      "id": "uuid",
      "workspace_id": "uuid",
      "object_type": "function",
      "object_id": "uuid",
      "responsibility_type": "owner",
      "owner_user_id": "uuid",
      "status": "assigned",
      "created_at": "2026-07-01T09:00:00Z"
    }
  ],
  "next_page_token": null
}
```

## Authorization

```text
User must have access to workspace.
```

---

# 13. Endpoint: Create Responsibility

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/responsibilities
```

## Purpose

Assign responsibility for a workspace object.

## Request Body

```json
{
  "object_type": "function",
  "object_id": "uuid",
  "responsibility_type": "owner",
  "owner_user_id": "uuid",
  "source_object_type": "operating_gap",
  "source_object_id": "uuid"
}
```

## Required Fields

```text
object_type
object_id
responsibility_type
owner_user_id
```

## Response: 201 Created

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "object_type": "function",
  "object_id": "uuid",
  "responsibility_type": "owner",
  "owner_user_id": "uuid",
  "status": "assigned",
  "assigned_by": "uuid",
  "assigned_at": "2026-07-01T09:00:00Z",
  "source_object_type": "operating_gap",
  "source_object_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

## Validation Rules

```text
object_type must be valid
object_id must exist
object must belong to same workspace if workspace-scoped
responsibility_type must be valid
owner_user_id must exist
owner_user_id must have workspace access when workspace_access is enabled
active duplicate responsibility should be prevented where product rule requires uniqueness
```

## Authorization

```text
Workspace owner or authorized manager.
```

## Audit Events

```text
responsibility.assigned
```

## Runtime Events

```text
responsibility.assigned
dashboard.refresh_requested
operating_gap.resolution_candidate optional
```

---

# 14. Endpoint: Get Responsibility

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/responsibilities/{responsibility_id}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "object_type": "function",
  "object_id": "uuid",
  "responsibility_type": "owner",
  "owner_user_id": "uuid",
  "status": "assigned",
  "assigned_by": "uuid",
  "assigned_at": "2026-07-01T09:00:00Z",
  "source_object_type": "operating_gap",
  "source_object_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

---

# 15. Endpoint: Reassign Responsibility

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/responsibilities/{responsibility_id}/reassign
```

## Purpose

Change the owner of an assigned responsibility.

## Request Body

```json
{
  "owner_user_id": "uuid",
  "reassignment_reason": "New finance lead assigned"
}
```

## Required Fields

```text
owner_user_id
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "owner_user_id": "uuid",
  "status": "assigned",
  "updated_at": "2026-07-01T11:00:00Z"
}
```

## Validation Rules

```text
responsibility must belong to workspace
responsibility must not be archived
owner_user_id must exist
owner_user_id must have workspace access when workspace_access is enabled
```

## Audit Events

```text
responsibility.reassigned
```

## Runtime Events

```text
responsibility.reassigned
dashboard.refresh_requested
```

---

# 16. Endpoint: Archive Responsibility

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/responsibilities/{responsibility_id}/archive
```

## Purpose

Archive a responsibility assignment.

## Request Body

```json
{
  "archive_reason": "Responsibility no longer applies"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "archived",
  "archived_at": "2026-07-01T12:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

## Audit Events

```text
responsibility.archived
```

## Runtime Events

```text
responsibility.archived
dashboard.refresh_requested
```

---

# 17. Resource: Ownership Gaps

## Resource Name

```text
ownership-gaps
```

## Purpose

Represent missing, unclear or conflicting ownership for functions or operating objects.

## MVP Status

```text
P2 / Near-MVP
```

## Data Model Reference

```text
ownership_gaps
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "object_type": "function",
  "object_id": "uuid",
  "gap_type": "missing_owner",
  "title": "Missing owner for finance function",
  "description": "No owner has been assigned",
  "status": "detected",
  "recommended_owner_id": "uuid",
  "resolved_by_responsibility_id": null,
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

---

# 18. Endpoint: List Ownership Gaps

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/ownership-gaps
```

## Query Parameters

```text
status optional
gap_type optional
object_type optional
object_id optional
recommended_owner_id optional
page_size optional
page_token optional
sort optional
```

## Response: 200 OK

```json
{
  "items": [
    {
      "id": "uuid",
      "workspace_id": "uuid",
      "object_type": "function",
      "object_id": "uuid",
      "gap_type": "missing_owner",
      "title": "Missing owner for finance function",
      "status": "detected",
      "recommended_owner_id": "uuid",
      "created_at": "2026-07-01T09:00:00Z"
    }
  ],
  "next_page_token": null
}
```

---

# 19. Endpoint: Resolve Ownership Gap

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/ownership-gaps/{ownership_gap_id}/resolve
```

## Purpose

Resolve an ownership gap by linking it to a responsibility assignment.

## Request Body

```json
{
  "resolved_by_responsibility_id": "uuid",
  "resolution_note": "Owner assigned"
}
```

## Required Fields

```text
resolved_by_responsibility_id
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "resolved",
  "resolved_by_responsibility_id": "uuid",
  "resolved_at": "2026-07-01T11:00:00Z",
  "updated_at": "2026-07-01T11:00:00Z"
}
```

## Validation Rules

```text
ownership gap must belong to workspace
responsibility must belong to same workspace
responsibility must address the same object or compatible object
ownership gap must not already be resolved or archived
```

## Audit Events

```text
ownership_gap.resolved
```

## Runtime Events

```text
ownership_gap.resolved
dashboard.refresh_requested
```

---

# 20. Endpoint: Archive Ownership Gap

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/ownership-gaps/{ownership_gap_id}/archive
```

## Request Body

```json
{
  "archive_reason": "No longer relevant"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "archived",
  "archived_at": "2026-07-01T12:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

## Audit Events

```text
ownership_gap.archived
```

## Runtime Events

```text
ownership_gap.archived
```

---

# 21. Common Error Codes

Function Responsibility API may return:

```text
unauthenticated
forbidden
not_found
validation_error
conflict
workspace_archived
invalid_status_transition
invalid_object_reference
invalid_owner
```

Example:

```json
{
  "error": {
    "code": "invalid_object_reference",
    "message": "Referenced object does not belong to this workspace.",
    "correlation_id": "uuid"
  }
}
```

---

# 22. Authorization Matrix

| Operation | MVP Rule | Expansion Rule |
|---|---|---|
| List functions | workspace owner | active workspace access |
| Create function | workspace owner | owner/admin/manager |
| Update function | workspace owner | owner/admin/manager |
| Archive function | workspace owner | owner/admin/manager |
| List responsibilities | workspace owner | active workspace access |
| Assign responsibility | workspace owner | owner/admin/manager |
| Reassign responsibility | workspace owner | owner/admin/manager |
| Archive responsibility | workspace owner | owner/admin/manager |
| Resolve ownership gap | workspace owner | owner/admin/manager |

---

# 23. Audit and Runtime Event Summary

| API Operation | Audit Event | Runtime Event |
|---|---|---|
| Create function | function.created | function.created |
| Update function | function.updated | function.updated |
| Archive function | function.archived | function.archived |
| Assign responsibility | responsibility.assigned | responsibility.assigned |
| Reassign responsibility | responsibility.reassigned | responsibility.reassigned |
| Archive responsibility | responsibility.archived | responsibility.archived |
| Resolve ownership gap | ownership_gap.resolved | ownership_gap.resolved |
| Archive ownership gap | ownership_gap.archived | ownership_gap.archived |

---

# 24. MVP Simplifications

For MVP, Bizzi may simplify by:

- using a flat function list before full function hierarchy;
- supporting only `owner` responsibility type;
- deriving ownership gaps from operating gaps;
- limiting responsibility assignment to workspace owner;
- postponing responsibility assignment history;
- using audit events instead of a dedicated responsibility history table.

These simplifications must preserve workspace scope, ownership clarity and auditability.

---

# 25. Future Expansion

Future Function Responsibility API may add:

```text
function hierarchy management
function merge/split operations
responsibility assignment history
RACI roles
bulk owner assignment
ownership conflict review
function health score
responsibility review dates
ownership escalation rules
```

---

# 26. Acceptance Criteria

Function Responsibility API is accepted when:

- function endpoints are defined;
- responsibility endpoints are defined;
- ownership gap expansion endpoints are defined;
- request and response shapes are documented;
- validation rules are identified;
- authorization rules are defined;
- audit and runtime event expectations are defined;
- MVP simplifications are documented;
- ownership clarity is preserved.

Status:

```text
Accepted for Agent Process Task Decision API Design
```

---

# 27. Final Statement

```text
Bizzi Function Responsibility API defines how the platform exposes business functions, accountability and ownership gaps through workspace-scoped, auditable and implementation-ready API contracts.
```

This API turns operating structure into accountable business ownership.