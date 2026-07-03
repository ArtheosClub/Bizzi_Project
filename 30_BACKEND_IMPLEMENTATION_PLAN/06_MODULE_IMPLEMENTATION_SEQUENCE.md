# 06_MODULE_IMPLEMENTATION_SEQUENCE.md

# Bizzi Platform

## Module Implementation Sequence

**Layer:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Component Type:** Implementation Planning Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Previous Document:** 05_API_ROUTE_IMPLEMENTATION_PLAN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the recommended module implementation sequence for Bizzi Platform backend MVP.

It translates the backend service design, repository structure, database migration plan and API route implementation plan into a staged order for building backend modules without breaking workspace isolation, service boundaries, auditability or runtime coordination.

Core question:

```text
In what order should Bizzi backend modules be implemented so that each module depends on stable foundations and contributes to the first working vertical slice?
```

---

# 2. Implementation Sequence Thesis

```text
Bizzi backend modules should be implemented from shared foundations upward: configuration, database, shared kernel, identity, workspace, authorization, validation, audit, events, then business execution modules.
```

This prevents:

```text
feature modules without context
routes without authorization
mutations without audit events
runtime effects without event records
repositories without workspace filters
```

---

# 3. Sequence Overview

Recommended MVP sequence:

```text
00 — Project Scaffold
01 — ConfigModule
02 — DatabaseModule
03 — SharedKernelModule
04 — AuthModule / IdentityModule
05 — WorkspaceModule
06 — AuthorizationModule
07 — ValidationModule
08 — AuditModule
09 — EventModule
10 — TaskModule
11 — DecisionModule
12 — MemoryModule minimal
13 — DashboardModule minimal
14 — ExportModule skeleton optional
15 — HealthModule / Operational Readiness
```

Expansion sequence after MVP:

```text
16 — OperatingMapModule
17 — FunctionResponsibilityModule
18 — ProcessModule
19 — AgentModule
20 — IntegrationModule
21 — SecurityModule
22 — Advanced ExportModule
23 — Advanced DashboardModule
```

---

# 4. Dependency Direction

Canonical dependency direction:

```text
Feature Controller
↓
Feature Service
↓
Authorization / Validation
↓
Feature Repository
↓
DatabaseModule
```

Cross-cutting services:

```text
AuditModule
EventModule
TransactionManager
```

Rule:

```text
Feature modules may depend on shared enforcement modules, but shared modules must not depend on feature modules.
```

---

# 5. Stage 00 — Project Scaffold

Purpose:

```text
Create the backend project foundation.
```

Deliverables:

```text
backend/package.json
backend/tsconfig.json
backend/nest-cli.json
backend/src/main.ts
backend/src/app.module.ts
backend/test setup
basic lint and typecheck commands
```

Acceptance criteria:

```text
backend starts locally
lint command exists
typecheck command exists
test command exists
```

---

# 6. Stage 01 — ConfigModule

Purpose:

```text
Provide validated runtime configuration.
```

Responsibilities:

```text
load environment variables
validate required config
expose typed configuration
separate local, test and production config
```

Required config:

```text
NODE_ENV
PORT
DATABASE_URL
DEV_AUTH_MODE or JWT_SECRET
```

Acceptance criteria:

```text
invalid config fails startup
.env.example documents required variables
config is injectable into modules
```

---

# 7. Stage 02 — DatabaseModule

Purpose:

```text
Provide database access and transaction handling.
```

Deliverables:

```text
PrismaService
DatabaseModule
TransactionManager
initial schema.prisma
migration commands
```

Dependencies:

```text
ConfigModule
```

Acceptance criteria:

```text
application connects to PostgreSQL
migration can run locally
repository tests can access test database
transaction manager supports service unit-of-work pattern
```

---

# 8. Stage 03 — SharedKernelModule

Purpose:

```text
Provide shared primitives used by all modules.
```

Deliverables:

```text
RequestContext
ActorContext
WorkspaceContext
CorrelationContext
ServiceError
ErrorCodes
ErrorMapper
Pagination DTOs
Object type constants
Audit action constants
Runtime event constants
```

Acceptance criteria:

```text
canonical error shape exists
correlation_id can be carried through request flow
pagination model exists
shared constants are available to services
```

---

# 9. Stage 04 — AuthModule / IdentityModule

Purpose:

```text
Provide authenticated actor context and /me route.
```

MVP behavior:

```text
development identity stub or JWT-compatible abstraction
```

Deliverables:

```text
AuthGuard or dev auth middleware
IdentityController
IdentityService
UserRepository
GET /api/v1/me
```

Acceptance criteria:

```text
/me returns actor DTO
authenticated actor_id is available in request context
unauthenticated access can be rejected where required
```

---

# 10. Stage 05 — WorkspaceModule

Purpose:

```text
Create the workspace foundation for all workspace-scoped behavior.
```

Deliverables:

```text
WorkspaceController
WorkspaceService
WorkspaceSettingsService
WorkspaceRepository
WorkspaceSettingsRepository
CreateWorkspaceDto
WorkspaceResponseDto
```

Routes:

```text
POST /api/v1/workspaces
GET /api/v1/workspaces
GET /api/v1/workspaces/{workspace_id}
```

Acceptance criteria:

```text
workspace can be created
workspace settings are created transactionally
workspace can be listed for owner
workspace detail can be read by owner
workspace.created audit/runtime events are emitted after Audit/Event modules are wired
```

Note:

```text
WorkspaceModule may initially use stub audit/event calls until AuditModule and EventModule are implemented, but final MVP must use real persisted events.
```

---

# 11. Stage 06 — AuthorizationModule

Purpose:

```text
Enforce server-side workspace access and owner-only MVP authorization.
```

Deliverables:

```text
AuthorizationService
WorkspacePermissionService
RoleResolutionService minimal
Permission constants
```

MVP rule:

```text
actor_id must equal company_workspaces.owner_user_id for workspace-scoped access.
```

Acceptance criteria:

```text
non-owner workspace access is rejected
workspace archived mutation is rejected
authorization failures map to canonical errors
```

---

# 12. Stage 07 — ValidationModule

Purpose:

```text
Provide reusable service-level validation.
```

Deliverables:

```text
ValidationService
ObjectReferenceValidator
StatusTransitionValidator
BusinessRuleValidator minimal
InputValidation helpers
```

Acceptance criteria:

```text
invalid UUID rejected
cross-workspace object reference rejected
invalid task status transition rejected
invalid decision confirmation rejected
validation failures map to canonical errors
```

---

# 13. Stage 08 — AuditModule

Purpose:

```text
Persist audit evidence for meaningful state changes.
```

Deliverables:

```text
AuditService
AuditQueryService
AuditEventRepository
AuditEventController
AuditEventResponseDto
```

Routes:

```text
GET /api/v1/workspaces/{workspace_id}/audit-events
```

Acceptance criteria:

```text
audit events can be recorded inside transactions
audit events are workspace-scoped
audit events can be listed by owner
audit payloads exclude secrets
```

---

# 14. Stage 09 — EventModule

Purpose:

```text
Persist runtime events for coordination.
```

Deliverables:

```text
RuntimeEventService
RuntimeEventQueryService
RuntimeEventRepository
RuntimeEventController
RuntimeEventResponseDto
```

Routes:

```text
GET /api/v1/workspaces/{workspace_id}/runtime-events
```

Acceptance criteria:

```text
runtime events can be emitted inside transactions
runtime events include correlation_id
runtime events can be listed by owner
runtime event payloads exclude secrets
```

---

# 15. Stage 10 — TaskModule

Purpose:

```text
Implement actionable work lifecycle.
```

Deliverables:

```text
TaskController
TaskService
TaskLifecycleService
TaskRepository
TaskStatusPolicy
CreateTaskDto
CompleteTaskDto
TaskResponseDto
```

Routes:

```text
POST /api/v1/workspaces/{workspace_id}/tasks
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/complete
GET /api/v1/workspaces/{workspace_id}/tasks
GET /api/v1/workspaces/{workspace_id}/tasks/{task_id}
```

Acceptance criteria:

```text
task can be created
task can be completed
invalid status transition is rejected
task operations emit audit events
task operations emit runtime events
tasks are workspace-scoped
```

---

# 16. Stage 11 — DecisionModule

Purpose:

```text
Implement official business decision evidence.
```

Deliverables:

```text
DecisionController
DecisionService
DecisionConfirmationService
DecisionRepository
DecisionStatusPolicy
CreateDecisionDto
ConfirmDecisionDto
DecisionResponseDto
```

Routes:

```text
POST /api/v1/workspaces/{workspace_id}/decisions
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm
GET /api/v1/workspaces/{workspace_id}/decisions
GET /api/v1/workspaces/{workspace_id}/decisions/{decision_id}
```

Acceptance criteria:

```text
decision can be created in draft status
decision can be confirmed
invalid confirmation is rejected
confirmed decision records confirmed_by and confirmed_at
decision operations emit audit and runtime events
decisions are workspace-scoped
```

---

# 17. Stage 12 — MemoryModule Minimal

Purpose:

```text
Capture and activate simple business memory records.
```

Deliverables:

```text
MemoryController
MemoryService
MemoryActivationService
MemoryRepository
MemoryStatusPolicy
CreateMemoryEntryDto
ActivateMemoryEntryDto
MemoryEntryResponseDto
```

Routes:

```text
GET /api/v1/workspaces/{workspace_id}/memory-entries
POST /api/v1/workspaces/{workspace_id}/memory-entries
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/activate
```

Acceptance criteria:

```text
memory entry can be created as candidate
memory entry can be activated
archived/invalid memory cannot be activated
memory operations emit audit and runtime events
active memory is workspace-scoped
```

---

# 18. Stage 13 — DashboardModule Minimal

Purpose:

```text
Expose current workspace operating state.
```

Deliverables:

```text
DashboardController
DashboardService
DashboardSummaryResponseDto
```

Route:

```text
GET /api/v1/workspaces/{workspace_id}/dashboard
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

Acceptance criteria:

```text
dashboard returns accurate counts
dashboard is workspace-scoped
dashboard excludes archived records where appropriate
```

---

# 19. Stage 14 — ExportModule Skeleton Optional

Purpose:

```text
Prepare export job lifecycle without full document rendering.
```

Optional deliverables:

```text
ExportController
ExportService
ExportJobRepository
CreateExportJobDto
ExportJobResponseDto
```

Routes:

```text
POST /api/v1/workspaces/{workspace_id}/export-jobs
GET /api/v1/workspaces/{workspace_id}/export-jobs
```

MVP optional behavior:

```text
create queued export_job
record export.requested audit event
emit export.queued runtime event
```

---

# 20. Stage 15 — HealthModule / Operational Readiness

Purpose:

```text
Provide basic operational checks for local and future deployment.
```

Deliverables:

```text
HealthController
GET /health
GET /ready optional
```

Checks:

```text
application boot
database connectivity
```

Acceptance criteria:

```text
health route returns OK
readiness fails if database is unavailable
```

---

# 21. Module Completion Definition

A backend module is complete when:

```text
controller exists when API-facing
service exists
repository exists when persistent
DTOs exist
authorization checks exist
validation checks exist
audit events are emitted for meaningful mutations
runtime events are emitted where coordination is needed
unit tests pass
repository tests pass
API tests pass for route modules
```

---

# 22. MVP Completion Definition

MVP module sequence is complete when:

```text
Project scaffold works
Config validates
Database migrations run
Identity works
Workspace creation works
Authorization works
Validation works
Audit events persist
Runtime events persist
Task lifecycle works
Decision confirmation works
Memory minimal works
Dashboard summary works
Tests pass locally
```

---

# 23. Dependency Matrix

| Module | Depends On | Required Before |
|---|---|---|
| ConfigModule | none | all runtime modules |
| DatabaseModule | ConfigModule | repositories |
| SharedKernelModule | none | all modules |
| Auth/Identity | SharedKernel, Database | Workspace |
| Workspace | Database, SharedKernel | Authorization, Task, Decision |
| Authorization | Workspace, Auth | all workspace modules |
| Validation | SharedKernel, repositories | Task, Decision, Memory |
| Audit | Database, SharedKernel | final mutations |
| Event | Database, SharedKernel | final mutations |
| Task | Workspace, Authz, Validation, Audit, Event | Dashboard |
| Decision | Workspace, Authz, Validation, Audit, Event | Dashboard, Memory |
| Memory | Workspace, Authz, Validation, Audit, Event | Dashboard |
| Dashboard | Task, Decision, Memory, Audit, Event | MVP demo |

---

# 24. Implementation Anti-Patterns

Avoid:

```text
building TaskModule before AuthorizationModule
building DashboardModule before source data modules
building FeatureModule without tests
adding AgentModule before Task and Decision are stable
creating repositories without workspace_id filters
emitting audit/runtime events inconsistently
hardcoding user identity in feature services
```

---

# 25. Future Expansion Sequence

After MVP vertical slice passes, recommended expansion:

```text
1. OperatingMapModule
2. FunctionResponsibilityModule
3. ProcessModule
4. AgentModule
5. IntegrationModule
6. SecurityModule
7. ExportModule full
8. DashboardModule advanced
```

Reason:

```text
Operating map and function responsibility extend workspace structure.
Process and agent modules extend execution intelligence.
Integration and security extend external connectivity and governance.
Export and dashboard advanced features extend visibility and portability.
```

---

# 26. Acceptance Criteria

Module Implementation Sequence is accepted when:

- MVP module order is defined;
- dependency direction is documented;
- each implementation stage has purpose, deliverables and acceptance criteria;
- core modules are sequenced before feature modules;
- audit and event modules are placed before final feature completion;
- task, decision, memory and dashboard sequencing is defined;
- module completion definition is documented;
- MVP completion definition is documented;
- dependency matrix is provided;
- anti-patterns are documented;
- future expansion sequence is defined.

Status:

```text
Accepted for Service Implementation Guide
```

---

# 27. Final Statement

```text
Bizzi Module Implementation Sequence defines the safe build order for turning backend architecture into working code: foundations first, workspace next, shared enforcement next, audit/runtime consistency next, and business execution modules after that.
```

This sequence protects Bizzi from implementation drift while enabling a narrow, testable and complete MVP backend loop.