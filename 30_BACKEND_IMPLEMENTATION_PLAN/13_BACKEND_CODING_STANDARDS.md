# 13_BACKEND_CODING_STANDARDS.md

# Bizzi Platform

## Backend Coding Standards

**Layer:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Component Type:** Implementation Planning Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Previous Document:** 12_IMPLEMENTATION_RISK_REGISTER.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines backend coding standards for Bizzi Platform MVP implementation.

It establishes the practical code rules for TypeScript, NestJS modules, controllers, services, repositories, DTOs, errors, transactions, audit events, runtime events, tests, logging and AI-assisted code contributions.

Core question:

```text
How should Bizzi backend code be written so that it remains readable, testable, workspace-scoped, auditable, secure and consistent across human and AI-assisted implementation?
```

---

# 2. Coding Standards Thesis

```text
Bizzi backend code must make architecture visible in code. Folder names, class names, method names, tests and service flows should clearly show controller-service-repository separation, workspace scope, authorization, validation, transactions, auditability and runtime coordination.
```

Coding standards protect:

```text
implementation consistency
readability
maintainability
workspace isolation
testability
security
auditability
AI-assisted code review
```

---

# 3. Language Standard

Backend language:

```text
TypeScript
```

Rules:

```text
strict typing should be enabled
avoid implicit any
prefer explicit input and output types for public methods
use readonly where useful for DTO-like structures
avoid type assertions unless justified
avoid suppressing TypeScript errors
```

Forbidden patterns:

```text
any as default escape hatch
// @ts-ignore without documented reason
untyped service method inputs
untyped repository results
```

---

# 4. Framework Standard

Backend framework:

```text
NestJS
```

Core constructs:

```text
Module
Controller
Service
Repository provider
DTO
Guard
Pipe
Interceptor later
Exception filter
```

Rules:

```text
controllers route HTTP only
services own business behavior
repositories own persistence
shared modules expose cross-cutting utilities
feature modules own feature-specific behavior
```

---

# 5. File Naming Standard

File names must use:

```text
kebab-case
```

Examples:

```text
task.controller.ts
task.service.ts
task-lifecycle.service.ts
task.repository.ts
create-task.dto.ts
task.response.dto.ts
task-status.policy.ts
```

Test files:

```text
task.service.spec.ts
task.repository.spec.ts
task.e2e-spec.ts
```

---

# 6. Class Naming Standard

Class names must use:

```text
PascalCase
```

Examples:

```text
TaskController
TaskService
TaskLifecycleService
TaskRepository
CreateTaskDto
TaskResponseDto
TaskStatusPolicy
```

Rule:

```text
Class name should clearly reflect architectural role.
```

---

# 7. Method Naming Standard

Method names must use:

```text
camelCase
```

Recommended verbs:

```text
create
get
list
update
archive
complete
confirm
activate
record
emit
require
validate
map
```

Examples:

```text
createTask
completeTask
confirmDecision
activateMemoryEntry
findByIdAndWorkspace
listByWorkspace
requireWorkspaceOwner
validateTaskCompletion
```

Rule:

```text
Method names should describe business intent, not implementation mechanics.
```

---

# 8. Database Naming Standard

Database names should use:

```text
snake_case
```

Examples:

```text
workspace_id
created_at
updated_at
completed_at
confirmed_at
source_object_type
source_object_id
```

TypeScript field names may use camelCase when Prisma maps database fields.

Rule:

```text
Database naming must align with 27_DATA_MODEL/16_DATABASE_NAMING_CONVENTIONS.md.
```

---

# 9. Module Coding Standard

Each feature module should use this structure:

```text
module/
├── controllers/
├── services/
├── repositories/
├── dto/
├── policies/
├── constants/
└── tests/
```

Module file:

```text
module-name.module.ts
```

Rules:

```text
export only what other modules are allowed to use
hide repositories from controllers
avoid circular module imports
keep feature-specific constants inside feature module
```

---

# 10. Controller Coding Standard

Controllers should:

```text
map routes
extract path/query/body parameters
receive authenticated request context
call service methods
return DTOs
```

Controllers should not:

```text
call Prisma
call repositories directly
contain business rules
perform lifecycle transitions directly
emit audit events
emit runtime events
```

Controller method shape:

```typescript
@Post()
async createTask(
  @Param('workspace_id') workspaceId: string,
  @Body() body: CreateTaskDto,
  @ReqContext() context: RequestContext,
): Promise<TaskResponseDto> {
  return this.taskService.createTask(
    context.withWorkspace(workspaceId),
    body,
  );
}
```

---

# 11. Service Coding Standard

Services should:

```text
receive ServiceContext
check authorization
validate input and business rules
load state through repositories
coordinate transactions
record audit events
emit runtime events
return DTOs
raise structured service errors
```

Services should not:

```text
return raw Prisma records to controllers
perform HTTP-specific formatting
ignore workspace_id
write directly to unrelated tables without transaction context
swallow errors without mapping
```

Rule:

```text
Every meaningful mutation must be readable as a business unit of work.
```

---

# 12. Repository Coding Standard

Repositories should:

```text
wrap Prisma queries
support transaction client
include workspace_id in workspace-scoped queries
apply pagination for list methods
use explicit filters
return persistence records
```

Repositories should not:

```text
perform authorization
own business lifecycle rules
emit audit events
emit runtime events
return API DTOs
call services
```

Required method pattern:

```text
findByIdAndWorkspace
listByWorkspace
updateByIdAndWorkspace
archiveByIdAndWorkspace
```

---

# 13. DTO Coding Standard

DTOs should define API boundary shapes.

Request DTOs:

```text
CreateWorkspaceDto
CreateTaskDto
CompleteTaskDto
CreateDecisionDto
ConfirmDecisionDto
CreateMemoryEntryDto
```

Response DTOs:

```text
WorkspaceResponseDto
TaskResponseDto
DecisionResponseDto
MemoryEntryResponseDto
AuditEventResponseDto
RuntimeEventResponseDto
DashboardSummaryResponseDto
```

Rules:

```text
request DTOs validate API input shape
response DTOs expose stable API output shape
DTOs must not expose raw secrets
DTOs should not expose internal-only fields unless contract requires them
```

---

# 14. Mapper Standard

Mapping should be explicit.

Recommended pattern:

```text
TaskMapper.toDto(record)
DecisionMapper.toDto(record)
MemoryEntryMapper.toDto(record)
```

Rules:

```text
services return DTOs after mapping
repositories return records
mapping should sanitize sensitive fields
mapping should normalize API field naming
```

---

# 15. Error Coding Standard

Use structured service errors.

Canonical errors:

```text
UnauthenticatedError
ForbiddenError
NotFoundError
WorkspaceArchivedError
ValidationError
InvalidObjectReferenceError
InvalidStatusTransitionError
BusinessRuleViolationError
ConflictError
InternalServiceError
```

Rules:

```text
never expose raw Prisma errors to API clients
never expose provider stack traces to API clients
error responses must follow 28_API_CONTRACTS/10_ERROR_AND_VALIDATION_CONTRACTS.md
validation errors should include details when useful
```

---

# 16. Transaction Coding Standard

Use TransactionManager for meaningful mutations.

Transaction should include:

```text
primary state mutation
related state mutation if needed
audit event
runtime event
idempotency result when applicable
```

Rules:

```text
required audit event failure should rollback mutation
required runtime event failure should rollback mutation in MVP
external provider calls should not run inside core transaction
```

---

# 17. Audit Coding Standard

Audit events must be recorded through AuditService.

Rules:

```text
do not write audit_events manually from feature services
include actor context
include object reference
include correlation_id
include before_state and after_state when useful
sanitize payloads
exclude secrets
```

Audit actions should use constants:

```text
AuditActions.TASK_CREATED
AuditActions.TASK_COMPLETED
AuditActions.DECISION_CONFIRMED
```

---

# 18. Runtime Event Coding Standard

Runtime events must be emitted through RuntimeEventService.

Rules:

```text
include workspace_id
include event_type
include source object reference
include actor context
include correlation_id
sanitize payloads
exclude secrets
```

Runtime event names should use constants:

```text
RuntimeEvents.TASK_CREATED
RuntimeEvents.TASK_COMPLETED
RuntimeEvents.DASHBOARD_REFRESH_REQUESTED
```

---

# 19. Authorization Coding Standard

Authorization must be service-level.

Rules:

```text
all workspace-scoped service methods require authorization
MVP uses owner-only rules
future RBAC should not require rewriting feature services
controllers may use guards, but services remain enforcement layer
```

Forbidden:

```text
frontend-only authorization
route-only authorization without service check
repository-level authorization as primary control
```

---

# 20. Validation Coding Standard

Validation is layered.

Layers:

```text
DTO validation
service input validation
object reference validation
status transition validation
business rule validation
```

Rules:

```text
validate object belongs to workspace
validate lifecycle transition before mutation
validate enum values
validate pagination bounds
reject unknown unsafe filters
```

---

# 21. Logging Coding Standard

Logs should be structured and safe.

Required context when available:

```text
correlation_id
request_id
workspace_id
actor_id
operation
```

Forbidden in logs:

```text
raw secrets
access tokens
refresh tokens
API keys
passwords
private keys
signed URLs when avoidable
```

Rule:

```text
Logs are operational diagnostics, not audit evidence.
```

---

# 22. Test Coding Standard

Each module should include:

```text
unit tests for policies and validators
service tests for business behavior
repository tests for workspace scoping
API/e2e tests for routes
```

Test naming:

```text
should create task
should reject non-owner workspace access
should reject cross-workspace task lookup
should record audit event when task is completed
```

Rule:

```text
Tests must cover failure paths, not only successful behavior.
```

---

# 23. Import and Dependency Standard

Allowed dependency direction:

```text
controller → service
service → repository
service → authorization/validation/audit/event
repository → database
feature → shared
```

Forbidden:

```text
repository → service
shared → feature
controller → repository
feature modules importing each other's repositories directly
```

---

# 24. Comments and Documentation Standard

Code should be self-explanatory where possible.

Use comments for:

```text
non-obvious business rules
security-sensitive decisions
transaction rationale
temporary MVP simplifications
future expansion notes
```

Avoid comments that:

```text
repeat obvious code
hide unclear naming
justify architecture violations
```

---

# 25. AI-Assisted Coding Standard

AI-generated code must:

```text
reference relevant architecture document
follow module structure
include or update tests
preserve workspace scope
not invent fields, routes or statuses
not bypass authorization or validation
not expose secrets
```

Recommended prompt format:

```text
Implement <module/service/repository> according to <document path>. Preserve workspace_id scoping, use AuthorizationService and ValidationService, add tests for success and failure paths.
```

Rule:

```text
AI-generated code is not accepted until tests pass and architecture alignment is reviewed.
```

---

# 26. MVP Simplifications Standard

MVP simplifications must be explicit.

Allowed MVP simplifications:

```text
owner-only authorization
simple live dashboard counts
simple memory records without semantic search
inline runtime event persistence
Prisma migrations only
local development auth stub
```

Forbidden simplifications:

```text
skip workspace isolation
skip audit events
skip validation
skip tests
store raw secrets
return raw database errors
```

---

# 27. Code Review Checklist

Every backend code review should check:

```text
Does the code follow module structure?
Are controllers thin?
Are services responsible for business behavior?
Are repositories workspace-scoped?
Is authorization enforced?
Is validation enforced?
Are mutations transactional?
Are audit events recorded?
Are runtime events emitted where needed?
Are DTOs used at API boundary?
Are canonical errors used?
Are tests included?
Are secrets excluded?
```

---

# 28. Anti-Patterns

Avoid:

```text
fat controllers
services using Prisma directly everywhere
repositories containing business rules
findById without workspace_id for workspace data
unbounded list queries
raw request filters passed to database
mutation without audit event
runtime event without correlation_id
DTOs exposing internal secrets
AI-generated code merged without tests
```

---

# 29. Acceptance Criteria

Backend Coding Standards are accepted when:

- TypeScript and NestJS standards are defined;
- file, class, method and database naming rules are documented;
- module, controller, service and repository standards are defined;
- DTO, mapper and error standards are defined;
- transaction, audit and runtime event standards are defined;
- authorization and validation standards are defined;
- logging and testing standards are defined;
- import and dependency rules are documented;
- AI-assisted coding rules are defined;
- MVP simplification boundaries are documented;
- review checklist and anti-patterns are provided.

Status:

```text
Accepted for Implementation Checklist
```

---

# 30. Final Statement

```text
Bizzi Backend Coding Standards define the implementation discipline required for consistent, secure, auditable and AI-safe backend code.
```

These standards ensure that the Bizzi backend remains aligned with the architecture while becoming real, testable and maintainable software.