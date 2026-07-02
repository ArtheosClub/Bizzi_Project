# 02_MVP_VERTICAL_SLICE.md

# Bizzi Platform

## MVP Vertical Slice

**Layer:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Component Type:** Implementation Planning Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Previous Document:** 01_TECH_STACK_DECISION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the first MVP vertical slice for Bizzi Platform backend implementation.

It identifies the smallest complete backend flow that proves the platform can create a workspace, create work, confirm decisions, preserve audit evidence, emit runtime events and expose a dashboard summary through real API routes, services, repositories and database persistence.

Core question:

```text
What is the narrowest backend implementation slice that proves Bizzi can operate as a workspace-scoped, auditable and AI-ready business platform?
```

---

# 2. MVP Vertical Slice Thesis

```text
The first MVP slice should not implement every Bizzi module. It should implement one complete operating loop end-to-end, with real persistence, authorization, validation, transactions, audit events, runtime events and API responses.
```

The slice proves architecture before breadth.

---

# 3. MVP Slice Name

Recommended slice name:

```text
Workspace Execution Loop v0.1
```

Core flow:

```text
User
↓
Workspace
↓
Task
↓
Decision
↓
Memory Candidate / Memory Entry
↓
Audit Event
↓
Runtime Event
↓
Dashboard Summary
```

---

# 4. Business Scenario

The MVP should support this simple business scenario:

```text
A user creates a company workspace, creates a task, completes the task, records a decision, confirms the decision, stores a memory entry, and sees the resulting operating state on the dashboard.
```

This scenario demonstrates:

```text
workspace creation
workspace isolation
task lifecycle
decision confirmation
memory capture
auditability
runtime coordination
dashboard visibility
canonical API behavior
```

---

# 5. User Journey

MVP user journey:

```text
1. User calls /me and receives identity context.
2. User creates a workspace.
3. System creates default workspace settings.
4. User creates a task inside the workspace.
5. User completes the task.
6. User creates a decision linked to the workspace, task or function later.
7. User confirms the decision.
8. System records audit events for meaningful state changes.
9. System emits runtime events for coordination.
10. User opens the dashboard and sees counts for tasks, decisions, memory and recent activity.
```

---

# 6. Scope Included

The MVP vertical slice includes:

```text
Identity stub
WorkspaceModule minimal
WorkspaceSettings minimal
AuthorizationModule owner-only
ValidationModule basic
TaskModule minimal
DecisionModule minimal
MemoryModule minimal
AuditModule minimal
EventModule minimal
DashboardModule minimal
SharedKernel
Database migrations
API error mapping
Service tests
Repository tests
API smoke tests
```

---

# 7. Scope Excluded

The MVP vertical slice excludes:

```text
full user registration
full RBAC
agent recommendation application
process engine
operating map generation
function hierarchy
responsibility assignment
integration sync
security policy management
export file generation
semantic memory search
custom dashboards
advanced observability
production deployment automation
```

These features are intentionally deferred.

---

# 8. Required Backend Modules

Required modules for the first slice:

```text
SharedModule
AuthModule
IdentityModule
WorkspaceModule
AuthorizationModule
ValidationModule
TaskModule
DecisionModule
MemoryModule
AuditModule
EventModule
DashboardModule
DatabaseModule
```

Optional but useful:

```text
HealthModule
ConfigModule
LoggerModule
```

---

# 9. Required Database Tables

Required MVP tables:

```text
users
company_workspaces
workspace_settings
tasks
decisions
memory_entries
audit_events
runtime_events
```

Optional early table:

```text
workspace_access
```

Recommendation:

```text
For MVP, owner_user_id on company_workspaces is sufficient, but workspace_access may be created early to prepare RBAC expansion.
```

---

# 10. Required API Endpoints

MVP endpoints:

```text
GET /api/v1/me
GET /api/v1/workspaces
POST /api/v1/workspaces
GET /api/v1/workspaces/{workspace_id}
PATCH /api/v1/workspaces/{workspace_id}
GET /api/v1/workspaces/{workspace_id}/workspace-settings
PATCH /api/v1/workspaces/{workspace_id}/workspace-settings
GET /api/v1/workspaces/{workspace_id}/tasks
POST /api/v1/workspaces/{workspace_id}/tasks
GET /api/v1/workspaces/{workspace_id}/tasks/{task_id}
PATCH /api/v1/workspaces/{workspace_id}/tasks/{task_id}
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/complete
GET /api/v1/workspaces/{workspace_id}/decisions
POST /api/v1/workspaces/{workspace_id}/decisions
GET /api/v1/workspaces/{workspace_id}/decisions/{decision_id}
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm
GET /api/v1/workspaces/{workspace_id}/memory-entries
POST /api/v1/workspaces/{workspace_id}/memory-entries
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/activate
GET /api/v1/workspaces/{workspace_id}/audit-events
GET /api/v1/workspaces/{workspace_id}/runtime-events
GET /api/v1/workspaces/{workspace_id}/dashboard
```

---

# 11. Endpoint Priority

Priority order:

```text
P1 — GET /me
P1 — POST /workspaces
P1 — GET /workspaces
P1 — GET /workspaces/{workspace_id}
P1 — POST /workspaces/{workspace_id}/tasks
P1 — POST /workspaces/{workspace_id}/tasks/{task_id}/complete
P1 — POST /workspaces/{workspace_id}/decisions
P1 — POST /workspaces/{workspace_id}/decisions/{decision_id}/confirm
P1 — GET /workspaces/{workspace_id}/dashboard
P1 — GET /workspaces/{workspace_id}/audit-events
P1 — GET /workspaces/{workspace_id}/runtime-events
P2 — PATCH workspace/settings/task
P2 — memory entry create/activate
P2 — list endpoints with pagination
```

---

# 12. Service Interaction Flow

Canonical flow for the MVP slice:

```text
Controller
↓
DTO validation
↓
Service method
↓
AuthorizationService
↓
ValidationService
↓
Repository
↓
TransactionManager
↓
AuditService
↓
RuntimeEventService
↓
Response DTO
```

Rule:

```text
Even the MVP must avoid direct database writes from controllers.
```

---

# 13. Workspace Creation Flow

Implementation flow:

```text
POST /api/v1/workspaces
↓
WorkspaceController.createWorkspace
↓
WorkspaceService.createWorkspace
↓
validate actor
↓
begin transaction
↓
create company_workspace
create workspace_settings
create audit event workspace.created
create runtime event workspace.created
↓
commit
↓
return workspace DTO
```

Acceptance:

```text
Workspace creation proves database write, transaction, audit event, runtime event and response mapping.
```

---

# 14. Task Completion Flow

Implementation flow:

```text
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/complete
↓
TaskController.completeTask
↓
TaskLifecycleService.completeTask
↓
AuthorizationService.requireWorkspaceOwner
↓
TaskRepository.findByIdAndWorkspace
↓
StatusTransitionValidator.validateTaskCompletion
↓
begin transaction
↓
update task status to completed
set completed_at
record task.completed audit event
emit task.completed runtime event
emit dashboard.refresh_requested runtime event
↓
commit
↓
return task DTO
```

Acceptance:

```text
Task completion proves lifecycle transition, workspace scope, audit emission and runtime coordination.
```

---

# 15. Decision Confirmation Flow

Implementation flow:

```text
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm
↓
DecisionController.confirmDecision
↓
DecisionConfirmationService.confirmDecision
↓
AuthorizationService.requireWorkspaceOwner
↓
DecisionRepository.findByIdAndWorkspace
↓
StatusTransitionValidator.validateDecisionConfirmation
↓
begin transaction
↓
update decision status to confirmed
set confirmed_by
set confirmed_at
set decision_date
record decision.confirmed audit event
emit decision.confirmed runtime event
emit dashboard.refresh_requested runtime event
optional emit memory.candidate_created runtime event
↓
commit
↓
return decision DTO
```

Acceptance:

```text
Decision confirmation proves official business evidence creation.
```

---

# 16. Memory Flow

MVP memory flow:

```text
POST /api/v1/workspaces/{workspace_id}/memory-entries
↓
MemoryService.createMemoryEntry
↓
create candidate memory
record memory.created audit event
emit memory.created runtime event
```

Activation flow:

```text
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/activate
↓
MemoryActivationService.activateMemoryEntry
↓
validate candidate status
set status active
set confirmed_by
set confirmed_at
record memory.activated audit event
emit memory.activated runtime event
```

Acceptance:

```text
Memory flow proves reusable business knowledge can be captured and activated safely.
```

---

# 17. Dashboard Summary Flow

Implementation flow:

```text
GET /api/v1/workspaces/{workspace_id}/dashboard
↓
DashboardController.getSummary
↓
DashboardService.getDashboardSummary
↓
AuthorizationService.requireWorkspaceAccess
↓
TaskRepository count open/completed tasks
DecisionRepository count confirmed decisions
MemoryRepository count active memory entries
AuditEventRepository fetch recent activity summary optional
↓
return dashboard summary DTO
```

MVP summary fields:

```text
open_tasks
completed_tasks
confirmed_decisions
active_memory_entries
recent_audit_events_count
recent_runtime_events_count
```

---

# 18. Authorization Rules

MVP authorization model:

```text
Authenticated user only.
Workspace owner only for all workspace-scoped reads and writes.
```

Rules:

```text
actor_id must match company_workspaces.owner_user_id
all workspace-scoped repository reads include workspace_id
cross-workspace object references are rejected
archived workspace blocks mutations
```

---

# 19. Validation Rules

MVP validation includes:

```text
required fields
UUID format
workspace existence
workspace ownership
workspace active status
object belongs to workspace
status transition allowed
enum values valid
date values valid
pagination bounds where implemented
```

MVP validation excludes:

```text
custom RBAC policies
complex agent authority
advanced export scope validation
integration provider validation
```

---

# 20. Transaction Boundaries

Required transaction boundaries:

```text
workspace creation + settings + audit + runtime event
task creation + audit + runtime event
task completion + audit + runtime events
decision creation + audit + runtime event
decision confirmation + audit + runtime events
memory creation + audit + runtime event
memory activation + audit + runtime event
```

Rule:

```text
No meaningful MVP mutation should commit without its required audit event.
```

---

# 21. Audit Events Required

MVP audit events:

```text
workspace.created
workspace.updated
workspace_settings.updated
task.created
task.updated
task.completed
decision.created
decision.confirmed
memory.created
memory.activated
```

Audit event fields:

```text
workspace_id
actor_type
actor_id
action
object_type
object_id
before_state optional
after_state optional
correlation_id
```

---

# 22. Runtime Events Required

MVP runtime events:

```text
workspace.created
task.created
task.completed
decision.created
decision.confirmed
memory.created
memory.activated
dashboard.refresh_requested
```

Runtime event fields:

```text
workspace_id
event_type
source_object_type
source_object_id
actor_type
actor_id
status
correlation_id
```

---

# 23. Repository Coverage

MVP repositories:

```text
UserRepository
WorkspaceRepository
WorkspaceSettingsRepository
TaskRepository
DecisionRepository
MemoryRepository
AuditEventRepository
RuntimeEventRepository
```

Required repository pattern:

```text
findByIdAndWorkspace(id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
create(data)
updateByIdAndWorkspace(id, workspace_id, patch)
```

---

# 24. Error Contract Coverage

MVP must implement canonical errors:

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

Rule:

```text
Raw database errors must not leak to API clients.
```

---

# 25. Test Coverage Required

Minimum tests:

```text
workspace creation creates settings, audit event and runtime event
non-owner cannot access workspace
cross-workspace task access is rejected
task completion updates status and emits events
invalid task transition is rejected
decision confirmation updates status and emits events
memory activation rejects archived memory
workspace archived blocks mutations
dashboard counts reflect task and decision state
audit event list is workspace-scoped
runtime event list is workspace-scoped
```

---

# 26. MVP Exit Criteria

The MVP vertical slice is complete when:

```text
all required tables have migrations
all P1 endpoints return stable JSON responses
owner-only authorization works
workspace isolation is tested
task lifecycle works
decision confirmation works
memory create/activate works minimally
audit events are recorded for all meaningful mutations
runtime events are recorded for coordination
dashboard summary reflects current state
tests pass locally
API errors follow canonical shape
```

---

# 27. Implementation Order

Recommended order:

```text
1. Project scaffold
2. Config and database connection
3. Prisma schema for MVP tables
4. Shared errors and response DTOs
5. Auth identity stub
6. WorkspaceModule
7. AuthorizationModule owner-only
8. AuditModule
9. EventModule
10. TaskModule
11. DecisionModule
12. MemoryModule minimal
13. DashboardModule minimal
14. API tests
15. MVP slice audit
```

---

# 28. Risks and Mitigations

## Risk 1 — Slice Becomes Too Broad

Mitigation:

```text
Keep operating map, integrations, exports and full agents out of first slice.
```

## Risk 2 — Audit/Event Deferred

Mitigation:

```text
Require audit/runtime events in first workspace, task and decision flows.
```

## Risk 3 — Authorization Implemented Too Late

Mitigation:

```text
Implement owner-only AuthorizationService before TaskModule.
```

## Risk 4 — Dashboard Becomes Analytics Project

Mitigation:

```text
Dashboard MVP uses simple live counts only.
```

## Risk 5 — Memory Becomes Semantic Search Too Early

Mitigation:

```text
Memory MVP is simple records and active status only.
```

---

# 29. Future Expansion After Slice

After the vertical slice passes, expand into:

```text
operating map generation
function and responsibility ownership
ownership gaps
process definitions
agent recommendations
export jobs
integration sync
security policies
workspace_access RBAC
advanced dashboard metrics
```

---

# 30. Acceptance Criteria

MVP Vertical Slice is accepted when:

- business scenario is defined;
- user journey is defined;
- included and excluded scope are documented;
- required modules are listed;
- required tables are listed;
- required endpoints are listed;
- core service flows are documented;
- authorization and validation rules are defined;
- transaction boundaries are defined;
- audit and runtime events are defined;
- repository coverage is defined;
- error contract coverage is defined;
- test coverage and exit criteria are defined;
- implementation order is documented.

Status:

```text
Accepted for Repository Structure
```

---

# 31. Final Statement

```text
Bizzi MVP Vertical Slice defines the first complete backend operating loop: workspace creation, task execution, decision confirmation, memory capture, audit evidence, runtime coordination and dashboard visibility.
```

This slice proves Bizzi architecture through a narrow, testable and implementation-ready product path.