# 05_API_ROUTE_IMPLEMENTATION_PLAN.md

# Bizzi Platform

## API Route Implementation Plan

**Layer:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Component Type:** Implementation Planning Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Previous Document:** 04_DATABASE_MIGRATION_PLAN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the API route implementation plan for Bizzi Platform backend MVP.

It translates the API contracts, backend service design, database migration plan and MVP vertical slice into a staged sequence for implementing REST routes, controllers, request DTOs, response DTOs, validation, authorization, error mapping and route tests.

Core question:

```text
Which API routes should Bizzi implement first, in what order, and with which controller/service/repository dependencies?
```

---

# 2. Route Implementation Thesis

```text
Bizzi API routes should be implemented in a vertical, testable order: identity, workspace, task, decision, memory, audit, runtime events and dashboard before broader platform modules.
```

Routes should prove:

```text
request validation
workspace authorization
service orchestration
repository persistence
transaction boundaries
audit event creation
runtime event creation
canonical error responses
stable JSON responses
```

---

# 3. API Style Decision

MVP API style:

```text
REST JSON
```

Base path:

```text
/api/v1
```

Implementation framework:

```text
NestJS controllers
```

Rules:

```text
controllers route requests
services own business behavior
repositories own persistence
errors map to canonical API error contracts
```

---

# 4. Route Implementation Principles

## 4.1 Contract First

Routes must follow `28_API_CONTRACTS`.

## 4.2 Workspace Path First

Workspace-scoped routes should use:

```text
/api/v1/workspaces/{workspace_id}/...
```

## 4.3 No Direct Repository Calls From Controllers

Controllers call services only.

## 4.4 Canonical Errors

All route errors must map to canonical API error shapes.

## 4.5 Test Each Route Family

Each implemented route family must include API smoke tests.

---

# 5. Route Priority Levels

Priority levels:

```text
P1 — required for MVP vertical slice
P2 — important for MVP completion but not first proof
P3 — expansion after vertical slice passes
```

Definitions:

```text
P1 proves platform operation end-to-end.
P2 completes MVP usability.
P3 expands to broader architecture surface.
```

---

# 6. P1 Route Set

P1 routes:

```text
GET /api/v1/me
POST /api/v1/workspaces
GET /api/v1/workspaces
GET /api/v1/workspaces/{workspace_id}
POST /api/v1/workspaces/{workspace_id}/tasks
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/complete
POST /api/v1/workspaces/{workspace_id}/decisions
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm
GET /api/v1/workspaces/{workspace_id}/dashboard
GET /api/v1/workspaces/{workspace_id}/audit-events
GET /api/v1/workspaces/{workspace_id}/runtime-events
```

P1 result:

```text
A user can create a workspace, create and complete work, confirm a decision, and view audit/runtime/dashboard evidence.
```

---

# 7. P2 Route Set

P2 routes:

```text
PATCH /api/v1/workspaces/{workspace_id}
GET /api/v1/workspaces/{workspace_id}/workspace-settings
PATCH /api/v1/workspaces/{workspace_id}/workspace-settings
GET /api/v1/workspaces/{workspace_id}/tasks
GET /api/v1/workspaces/{workspace_id}/tasks/{task_id}
PATCH /api/v1/workspaces/{workspace_id}/tasks/{task_id}
GET /api/v1/workspaces/{workspace_id}/decisions
GET /api/v1/workspaces/{workspace_id}/decisions/{decision_id}
GET /api/v1/workspaces/{workspace_id}/memory-entries
POST /api/v1/workspaces/{workspace_id}/memory-entries
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/activate
```

P2 result:

```text
The MVP becomes usable for basic workspace management, list/detail views and memory capture.
```

---

# 8. P3 Route Set

P3 routes:

```text
operating map routes
function and responsibility routes
agent recommendation routes
process routes
integration routes
security policy routes
export job routes
advanced dashboard metric routes
workspace access routes
```

P3 should start only after P1/P2 route tests pass.

---

# 9. Controller Families

MVP controller families:

```text
IdentityController
WorkspaceController
WorkspaceSettingsController
TaskController
DecisionController
MemoryController
AuditEventController
RuntimeEventController
DashboardController
```

Optional later:

```text
ExportController
HealthController
```

---

# 10. Identity Routes

## GET /api/v1/me

Controller:

```text
IdentityController.getMe
```

Service:

```text
IdentityService.getCurrentUser
```

Purpose:

```text
Return authenticated actor context.
```

MVP behavior:

```text
Use development identity stub or JWT-derived user.
```

Response includes:

```text
id
email
name
status
```

Tests:

```text
returns current user
rejects unauthenticated request when auth required
```

---

# 11. Workspace Routes

## POST /api/v1/workspaces

Controller:

```text
WorkspaceController.createWorkspace
```

Service:

```text
WorkspaceService.createWorkspace
```

Dependencies:

```text
WorkspaceRepository
WorkspaceSettingsRepository
AuditService
RuntimeEventService
TransactionManager
```

Required behavior:

```text
create workspace
create default settings
record workspace.created audit event
emit workspace.created runtime event
return workspace DTO
```

---

# 12. Workspace Read Routes

## GET /api/v1/workspaces

Purpose:

```text
List workspaces accessible to actor.
```

MVP rule:

```text
List workspaces where owner_user_id equals actor_id.
```

## GET /api/v1/workspaces/{workspace_id}

Purpose:

```text
Return workspace detail if actor is owner.
```

Required errors:

```text
not_found
forbidden
```

---

# 13. Workspace Settings Routes

## GET /api/v1/workspaces/{workspace_id}/workspace-settings

Purpose:

```text
Return workspace settings.
```

## PATCH /api/v1/workspaces/{workspace_id}/workspace-settings

Purpose:

```text
Update timezone, locale and feature toggles.
```

Required behavior:

```text
validate workspace ownership
validate timezone and locale
record workspace_settings.updated audit event
emit workspace_settings.updated runtime event
```

Priority:

```text
P2
```

---

# 14. Task Routes

## POST /api/v1/workspaces/{workspace_id}/tasks

Controller:

```text
TaskController.createTask
```

Service:

```text
TaskService.createTask
```

Required behavior:

```text
validate title
validate workspace ownership
create task with open status
record task.created audit event
emit task.created runtime event
emit dashboard.refresh_requested runtime event
```

## POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/complete

Service:

```text
TaskLifecycleService.completeTask
```

Required behavior:

```text
load task by id and workspace_id
validate status transition
set status completed
set completed_at
record task.completed audit event
emit task.completed runtime event
emit dashboard.refresh_requested runtime event
```

---

# 15. Task Read and Update Routes

## GET /api/v1/workspaces/{workspace_id}/tasks

Purpose:

```text
List tasks with pagination and status filter.
```

## GET /api/v1/workspaces/{workspace_id}/tasks/{task_id}

Purpose:

```text
Return task detail.
```

## PATCH /api/v1/workspaces/{workspace_id}/tasks/{task_id}

Purpose:

```text
Update task title, description, priority and due_date.
```

Priority:

```text
P2
```

---

# 16. Decision Routes

## POST /api/v1/workspaces/{workspace_id}/decisions

Controller:

```text
DecisionController.createDecision
```

Service:

```text
DecisionService.createDecision
```

Required behavior:

```text
validate title
validate optional task_id belongs to workspace
create decision with draft status
record decision.created audit event
emit decision.created runtime event
```

## POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm

Service:

```text
DecisionConfirmationService.confirmDecision
```

Required behavior:

```text
load decision by id and workspace_id
validate status allows confirmation
set status confirmed
set confirmed_by
set confirmed_at
record decision.confirmed audit event
emit decision.confirmed runtime event
emit dashboard.refresh_requested runtime event
```

---

# 17. Decision Read Routes

## GET /api/v1/workspaces/{workspace_id}/decisions

Purpose:

```text
List decisions with pagination and status filter.
```

## GET /api/v1/workspaces/{workspace_id}/decisions/{decision_id}

Purpose:

```text
Return decision detail.
```

Priority:

```text
P2
```

---

# 18. Memory Routes

## GET /api/v1/workspaces/{workspace_id}/memory-entries

Purpose:

```text
List memory entries by workspace.
```

## POST /api/v1/workspaces/{workspace_id}/memory-entries

Purpose:

```text
Create candidate memory entry.
```

## POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/activate

Purpose:

```text
Activate candidate memory entry for future AI context.
```

Priority:

```text
P2
```

---

# 19. Audit Event Routes

## GET /api/v1/workspaces/{workspace_id}/audit-events

Controller:

```text
AuditEventController.listAuditEvents
```

Service:

```text
AuditQueryService.listAuditEvents
```

Required behavior:

```text
validate workspace ownership
support pagination
support object_type/object_id/action filters later
return audit event DTOs
```

MVP rule:

```text
Audit events are read-only through public API.
```

---

# 20. Runtime Event Routes

## GET /api/v1/workspaces/{workspace_id}/runtime-events

Controller:

```text
RuntimeEventController.listRuntimeEvents
```

Service:

```text
RuntimeEventQueryService.listRuntimeEvents
```

Required behavior:

```text
validate workspace ownership
support pagination
support event_type/status filters later
return runtime event DTOs
```

MVP rule:

```text
Runtime events are read-only through public API and restricted to owner.
```

---

# 21. Dashboard Routes

## GET /api/v1/workspaces/{workspace_id}/dashboard

Controller:

```text
DashboardController.getDashboardSummary
```

Service:

```text
DashboardService.getDashboardSummary
```

Required behavior:

```text
validate workspace ownership
count open tasks
count completed tasks
count confirmed decisions
count active memory entries
count recent audit events
count recent runtime events
return dashboard summary DTO
```

Priority:

```text
P1
```

---

# 22. Route Implementation Order

Recommended order:

```text
1. IdentityController.getMe
2. WorkspaceController.createWorkspace
3. WorkspaceController.listWorkspaces
4. WorkspaceController.getWorkspace
5. TaskController.createTask
6. TaskController.completeTask
7. DecisionController.createDecision
8. DecisionController.confirmDecision
9. AuditEventController.listAuditEvents
10. RuntimeEventController.listRuntimeEvents
11. DashboardController.getDashboardSummary
12. WorkspaceSettingsController get/update
13. Task list/detail/update
14. Decision list/detail
15. Memory list/create/activate
```

---

# 23. Request DTO Requirements

Request DTOs must define:

```text
required fields
optional fields
field types
enum values
nested object shape when needed
```

MVP request DTOs:

```text
CreateWorkspaceDto
UpdateWorkspaceDto
UpdateWorkspaceSettingsDto
CreateTaskDto
UpdateTaskDto
CompleteTaskDto
CreateDecisionDto
ConfirmDecisionDto
CreateMemoryEntryDto
ActivateMemoryEntryDto
PaginationQueryDto
```

---

# 24. Response DTO Requirements

Response DTOs must define:

```text
stable id fields
workspace_id where relevant
status fields
created_at
updated_at
resource-specific fields
```

MVP response DTOs:

```text
UserResponseDto
WorkspaceResponseDto
WorkspaceSettingsResponseDto
TaskResponseDto
DecisionResponseDto
MemoryEntryResponseDto
AuditEventResponseDto
RuntimeEventResponseDto
DashboardSummaryResponseDto
PaginatedResponseDto
ErrorResponseDto
```

---

# 25. Error Mapping Requirements

MVP route errors:

```text
unauthenticated
forbidden
not_found
workspace_archived
validation_error
invalid_object_reference
invalid_status_transition
business_rule_violation
internal_error
```

Controller rule:

```text
Controllers must not return raw framework, Prisma or provider errors.
```

---

# 26. Route Test Requirements

Minimum API route tests:

```text
GET /me returns actor
POST /workspaces creates workspace and settings
GET /workspaces lists actor workspaces
POST /tasks creates task and events
POST /tasks/{id}/complete completes task and events
POST /decisions creates draft decision
POST /decisions/{id}/confirm confirms decision and events
GET /audit-events returns workspace-scoped events
GET /runtime-events returns workspace-scoped events
GET /dashboard returns expected counts
cross-workspace access is rejected
invalid status transition returns canonical error
```

---

# 27. OpenAPI Documentation Plan

MVP should prepare for:

```text
OpenAPI generation from NestJS decorators
Swagger UI in development
contract comparison against 28_API_CONTRACTS later
```

Rule:

```text
OpenAPI output must not become the source of truth until audited against architecture contracts.
```

---

# 28. Implementation Anti-Patterns

Avoid:

```text
implementing all endpoints before testing P1
controllers calling repositories directly
routes returning raw Prisma records
inconsistent error shape
workspace_id accepted from request body when path defines it
pagination omitted from list routes forever
route names diverging from API contracts
business logic hidden in DTO validators only
```

---

# 29. Acceptance Criteria

API Route Implementation Plan is accepted when:

- REST JSON style is confirmed;
- base path is defined;
- P1/P2/P3 route sets are defined;
- controller families are identified;
- route implementation order is documented;
- identity, workspace, task, decision, memory, audit, runtime and dashboard routes are specified;
- DTO requirements are defined;
- error mapping requirements are defined;
- route test requirements are defined;
- OpenAPI documentation plan is defined;
- anti-patterns are documented.

Status:

```text
Accepted for Module Implementation Sequence
```

---

# 30. Final Statement

```text
Bizzi API Route Implementation Plan defines the staged REST route path that turns backend service design into testable API behavior for the first workspace execution loop.
```

This plan lets implementation proceed route-by-route without losing workspace scope, service discipline, auditability or contract alignment.