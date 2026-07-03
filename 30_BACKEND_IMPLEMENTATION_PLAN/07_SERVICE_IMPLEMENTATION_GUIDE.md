# 07_SERVICE_IMPLEMENTATION_GUIDE.md

# Bizzi Platform

## Service Implementation Guide

**Layer:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Component Type:** Implementation Planning Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Previous Document:** 06_MODULE_IMPLEMENTATION_SEQUENCE.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the implementation guide for backend services in Bizzi Platform.

It translates the accepted backend service design into practical coding rules for NestJS services, method structure, transaction boundaries, authorization, validation, repository usage, audit events, runtime events, DTO mapping, error handling and testing.

Core question:

```text
How should Bizzi backend services be written so that implementation remains consistent, testable, workspace-scoped, transactional, auditable and AI-safe?
```

---

# 2. Service Implementation Thesis

```text
Bizzi services are the application layer where business behavior becomes official: controllers route requests, repositories persist data, but services authorize, validate, coordinate transactions, emit audit evidence and return canonical DTOs.
```

Services must protect:

```text
workspace isolation
authorization boundaries
business lifecycle rules
auditability
runtime coordination
AI confirmation rules
canonical errors
```

---

# 3. Service Responsibilities

A Bizzi service is responsible for:

```text
receiving service context
checking authorization
performing service-level validation
loading required state
checking business rules
coordinating repositories
wrapping mutations in transactions
recording audit events
emitting runtime events
mapping results to response DTOs
raising structured service errors
```

A service is not responsible for:

```text
HTTP routing
raw request parsing
low-level SQL details
frontend-specific formatting
external provider secrets outside secure boundary
```

---

# 4. Canonical Service Method Shape

Recommended method shape:

```typescript
async createTask(
  context: ServiceContext,
  input: CreateTaskInput,
): Promise<TaskDto> {
  await this.authorization.requireWorkspaceOwner(context);
  this.validation.validateCreateTaskInput(input);

  const workspace = await this.workspaceRepository.findById(context.workspaceId);
  this.validation.requireActiveWorkspace(workspace);

  return this.transactionManager.runInTransaction(context, async (tx) => {
    const task = await this.taskRepository.create(tx, {
      workspaceId: context.workspaceId,
      title: input.title,
      status: 'open',
    });

    await this.auditService.record(tx, context, {
      action: 'task.created',
      objectType: 'task',
      objectId: task.id,
      afterState: task,
    });

    await this.runtimeEventService.emit(tx, context, {
      eventType: 'task.created',
      sourceObjectType: 'task',
      sourceObjectId: task.id,
    });

    return TaskMapper.toDto(task);
  });
}
```

Rule:

```text
Every service method should be readable as a business operation, not as a database script.
```

---

# 5. Service Context

Every service method should receive a `ServiceContext`.

Required fields:

```text
actor_id
actor_type
workspace_id optional for non-workspace routes
request_id
correlation_id
```

Optional fields:

```text
agent_id
source_event_id
idempotency_key
ai_assisted
human_confirmed
```

Rule:

```text
Do not reconstruct actor or workspace context independently inside feature services when it is already available in ServiceContext.
```

---

# 6. Authorization Pattern

Authorization must run before mutation and before returning sensitive data.

MVP pattern:

```typescript
await this.authorization.requireWorkspaceOwner(context);
```

Expansion pattern:

```typescript
await this.authorization.requirePermission(context, 'task.complete', {
  objectType: 'task',
  objectId: taskId,
});
```

Rules:

```text
controllers must not be the only authorization layer
services must call AuthorizationService for protected operations
workspace-scoped services must enforce workspace access
internal-only operations must require internal actor context
```

---

# 7. Validation Pattern

Validation has three levels:

```text
DTO validation at controller boundary
service input validation
business rule validation
```

Service validation examples:

```typescript
this.validation.requireNonEmpty(input.title, 'title');
await this.objectReferenceValidator.requireTaskInWorkspace(context.workspaceId, taskId);
this.statusTransitionValidator.requireTaskCompletionAllowed(task.status);
```

Rule:

```text
DTO validation does not replace service-level business validation.
```

---

# 8. Repository Usage Pattern

Services use repositories for persistence.

Rules:

```text
controllers must not call repositories
repositories must not call services
services must not use Prisma directly unless inside infrastructure services
feature services should call repositories with workspace_id
repository return values should be mapped before API response
```

Required repository method style:

```text
findByIdAndWorkspace(id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
updateByIdAndWorkspace(id, workspace_id, patch)
```

---

# 9. Transaction Pattern

Mutations that affect official state must use a transaction.

Canonical transaction content:

```text
primary state change
related state change if needed
audit event
runtime event
idempotency result if applicable
```

Rule:

```text
No meaningful mutation should commit without required audit evidence.
```

---

# 10. Audit Event Pattern

Services must record audit events for meaningful state changes.

Examples:

```text
workspace.created
task.created
task.completed
decision.created
decision.confirmed
memory.created
memory.activated
```

Audit event must include:

```text
workspace_id
actor_id
actor_type
action
object_type
object_id
before_state optional
after_state optional
correlation_id
```

Rule:

```text
Audit events are business evidence and must not be replaced by logs or runtime events.
```

---

# 11. Runtime Event Pattern

Services emit runtime events for coordination.

Examples:

```text
task.created
task.completed
decision.confirmed
dashboard.refresh_requested
memory.created
```

Runtime events must include:

```text
workspace_id
event_type
source_object_type
source_object_id
actor context
correlation_id
```

Rule:

```text
Runtime events coordinate platform behavior; they are not audit evidence.
```

---

# 12. Error Handling Pattern

Services must raise structured service errors.

Allowed service errors:

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
```

Rules:

```text
never throw raw Prisma errors to controllers
never expose provider errors directly
map service errors to 28_API_CONTRACTS/10_ERROR_AND_VALIDATION_CONTRACTS.md
include validation details where useful
```

---

# 13. DTO Mapping Pattern

Services return DTOs, not raw persistence objects.

Recommended pattern:

```typescript
return TaskMapper.toDto(task);
```

Rules:

```text
DTOs must not include raw secrets
DTOs should use API field naming consistently
DTOs should preserve id, workspace_id, status and timestamps
internal metadata should be excluded unless API contract allows it
```

---

# 14. Service File Naming

File names:

```text
task.service.ts
task-lifecycle.service.ts
decision.service.ts
decision-confirmation.service.ts
memory-activation.service.ts
```

Class names:

```text
TaskService
TaskLifecycleService
DecisionConfirmationService
MemoryActivationService
```

Rule:

```text
Split lifecycle services when lifecycle behavior becomes materially different from CRUD behavior.
```

---

# 15. Service Dependency Rules

Allowed dependencies:

```text
repositories
authorization services
validation services
audit service
runtime event service
transaction manager
shared mappers/policies
```

Avoid:

```text
circular service dependencies
feature service importing another feature repository directly
service calling controller
service using raw request object
```

Cross-module business action rule:

```text
Call another module's service only when that module owns the resulting business behavior.
```

---

# 16. Lifecycle Policy Pattern

Lifecycle transitions should be centralized in policies or validators.

Example:

```typescript
TaskStatusPolicy.canComplete(task.status)
DecisionStatusPolicy.canConfirm(decision.status)
MemoryStatusPolicy.canActivate(memory.status)
```

Rule:

```text
Do not scatter status transition logic across controllers, repositories and services.
```

---

# 17. AI-Assisted Service Rules

AI-assisted service operations must preserve:

```text
agent_id when applicable
ai_assisted flag
human_confirmed flag
source recommendation or draft reference
result object reference
correlation_id
```

Rules:

```text
AI recommendations are not official state until service applies them
human confirmation is required for sensitive official effects
agent authority must be checked before mutation
AI-generated memory must be activated before active context use
```

---

# 18. Idempotency Pattern

Idempotency applies to retryable mutation operations.

Candidate operations:

```text
export job creation
integration sync trigger
operating map generation
AI recommendation application
```

Service rule:

```text
Check idempotency before mutation and store result reference after successful transaction.
```

MVP note:

```text
Idempotency can be deferred for simple task and decision operations unless retry behavior becomes user-visible.
```

---

# 19. Logging Pattern

Services may log operational information.

Required log context:

```text
correlation_id
request_id
workspace_id when available
actor_id when available
operation name
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

---

# 20. Testing Pattern

Every service must have tests for:

```text
happy path
authorization failure
validation failure
not_found behavior
workspace isolation
status transition rules
transaction side effects
audit event creation
runtime event creation
canonical error mapping
```

Service tests should mock repositories when unit-level and use real database when integration-level.

---

# 21. MVP Service Implementation Order

Recommended order:

```text
WorkspaceService
WorkspaceSettingsService
AuthorizationService
ValidationService
AuditService
RuntimeEventService
TaskService
TaskLifecycleService
DecisionService
DecisionConfirmationService
MemoryService
MemoryActivationService
DashboardService
```

Rule:

```text
Feature services should not be considered complete until audit and runtime event behavior is wired.
```

---

# 22. Service Completion Checklist

A service is complete when:

```text
method signatures are explicit
ServiceContext is used
authorization is enforced
validation is enforced
repositories are workspace-scoped
mutations use transactions
audit events are emitted where required
runtime events are emitted where required
DTO mapping exists
canonical errors are raised
tests cover success and failure paths
```

---

# 23. Anti-Patterns

Avoid:

```text
fat controllers
services returning raw Prisma records
business rules inside repositories
repository calls from controllers
mutation without audit event
runtime event without correlation_id
workspace_id from request body overriding path workspace_id
hardcoded actor identity inside services
try/catch that hides service errors
```

---

# 24. Acceptance Criteria

Service Implementation Guide is accepted when:

- service responsibilities are defined;
- canonical method shape is documented;
- ServiceContext is defined;
- authorization and validation patterns are documented;
- repository usage pattern is documented;
- transaction, audit and runtime event patterns are defined;
- error handling and DTO mapping are defined;
- dependency rules are documented;
- lifecycle, AI and idempotency rules are defined;
- testing expectations are documented;
- service completion checklist is provided;
- anti-patterns are documented.

Status:

```text
Accepted for Repository Implementation Guide
```

---

# 25. Final Statement

```text
Bizzi Service Implementation Guide defines the practical coding discipline for turning backend service design into safe, transactional, auditable and testable application services.
```

This guide ensures that each implemented service preserves Bizzi's workspace isolation, business integrity, auditability and AI governance guarantees.