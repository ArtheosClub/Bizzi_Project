# 03_CONTROLLER_SERVICE_REPOSITORY_PATTERN.md

# Bizzi Platform

## Controller Service Repository Pattern

**Layer:** 29_BACKEND_SERVICE_DESIGN  
**Component Type:** Backend Architecture Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Previous Document:** 02_BACKEND_MODULE_CATALOG.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Controller-Service-Repository pattern for Bizzi Platform backend design.

It establishes how API requests should flow through controllers, application services, domain policies, repositories, audit emitters and runtime event emitters while preserving workspace isolation, authorization, validation, transaction integrity and AI safety.

Core question:

```text
How should Bizzi structure backend request handling so that API contracts become secure, auditable and consistent service behavior?
```

---

# 2. Pattern Role

The Controller-Service-Repository pattern defines separation of responsibilities between backend layers.

It prevents:

- fat controllers;
- business logic inside repositories;
- direct database access from API handlers;
- inconsistent authorization checks;
- inconsistent validation;
- missing audit events;
- missing runtime events;
- AI actions bypassing confirmation policy.

---

# 3. Canonical Request Flow

Canonical flow:

```text
HTTP Request
↓
Controller
↓
Request DTO / Schema Validation
↓
Application Service
↓
Authorization / Business Validation
↓
Transaction Boundary
↓
Repositories
↓
Audit Service
↓
Runtime Event Service
↓
Response DTO
↓
HTTP Response
```

Rule:

```text
Every state-changing request must pass through an application service.
```

---

# 4. Layer Responsibilities Summary

| Layer | Owns | Must Not Own |
|---|---|---|
| Controller | HTTP boundary, request parsing, response mapping | Business rules, direct DB writes |
| Application Service | Use case behavior, authorization, validation, orchestration | SQL details, HTTP serialization |
| Domain Policy | Reusable business decisions and lifecycle rules | API response formatting |
| Repository | Persistence and query details | Authorization, AI confirmation rules |
| Audit Service | Audit event standardization | Feature-specific business decisions |
| Runtime Event Service | Event creation and coordination | Audit evidence replacement |

---

# 5. Controller Layer

## Purpose

Controllers adapt API contracts into backend service calls.

## Responsibilities

Controllers should:

```text
read path parameters
read query parameters
read request body
extract authenticated actor
extract correlation_id
call request schema validation
call application service
map service result to API response
map service errors to API error shape
```

## Controllers Must Not

Controllers must not:

```text
perform business lifecycle decisions
call repositories directly for mutations
construct audit events manually
construct runtime events manually
apply AI recommendations directly
resolve secrets
perform cross-module orchestration
```

---

# 6. Controller Input Context

Each controller should build a request context.

Recommended context:

```text
actor_id
actor_type
workspace_id when path-scoped
correlation_id
request_id
idempotency_key optional
client_ip optional
user_agent optional
```

Rule:

```text
Context should be passed into application services explicitly.
```

---

# 7. Application Service Layer

## Purpose

Application services implement use cases.

## Responsibilities

Application services should:

```text
receive validated input DTOs
load workspace context
check authorization
validate business rules
coordinate repositories
open transactions when mutating state
call audit service
call runtime event service
return service DTOs
```

## Services Must Not

Application services should not:

```text
return raw database rows directly
expose raw secrets
format HTTP responses
throw raw database errors to controllers
ignore workspace_id checks
```

---

# 8. Service Method Shape

Recommended service method shape:

```text
service.method(context, input) → result
```

Example:

```text
TaskService.completeTask(context, input)
```

Where context includes:

```text
workspace_id
actor
correlation_id
idempotency_key optional
```

Where input includes business data:

```text
task_id
completion_note
result_summary
```

---

# 9. Domain Policy Layer

## Purpose

Domain policies encapsulate reusable business decisions.

Examples:

```text
TaskStatusPolicy
DecisionConfirmationPolicy
MemoryActivationPolicy
AgentAuthorityPolicy
WorkspaceAccessPolicy
ExportScopePolicy
IntegrationScopePolicy
```

Policy responsibilities:

```text
allow or reject lifecycle transitions
validate AI authority
validate human confirmation requirement
validate export scope
validate last-owner protection
```

Rule:

```text
Reusable business decisions should become policies instead of being duplicated across services.
```

---

# 10. Repository Layer

## Purpose

Repositories encapsulate data persistence and retrieval.

## Responsibilities

Repositories should:

```text
load records by id and workspace_id
insert records
update records
apply workspace filters
support pagination
support filtering and sorting
return domain/data objects
hide SQL or ORM details
```

## Repositories Must Not

Repositories must not:

```text
make authorization decisions
emit audit events
emit runtime events
apply AI authority policy
format API responses
implement cross-module business orchestration
```

Rule:

```text
Repositories protect data access consistency, but services protect business meaning.
```

---

# 11. Repository Workspace Pattern

Workspace-scoped repository methods should require workspace_id.

Preferred patterns:

```text
findByIdAndWorkspace(id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
updateByIdAndWorkspace(id, workspace_id, patch)
archiveByIdAndWorkspace(id, workspace_id)
```

Avoid:

```text
findById(id)
updateById(id, patch)
```

unless the table is explicitly global.

---

# 12. DTO Boundaries

Backend should distinguish DTO types.

Recommended DTO categories:

```text
Request DTO
Service Input DTO
Service Result DTO
Repository Entity / Record
Response DTO
Audit DTO
Runtime Event DTO
```

Rule:

```text
Do not let raw database records become public API responses by accident.
```

---

# 13. Mutation Pattern

Canonical mutation pattern:

```text
validate request schema
build context
call service
check authorization
load records by workspace_id
validate business rule
begin transaction
write state change
write audit event
write runtime event intent
commit transaction
return result DTO
```

Example operations:

```text
create task
complete task
confirm decision
activate memory
trigger integration sync
request export
```

---

# 14. Read Pattern

Canonical read pattern:

```text
validate query parameters
build context
call service
check authorization
call repository with workspace_id filters
apply pagination/filtering/sorting
map to result DTO
return response DTO
```

Read operations may skip audit unless security-sensitive.

Examples of security-sensitive reads:

```text
audit event detail
runtime event detail
export download link
security policy detail
```

---

# 15. Transaction Pattern

Transaction boundaries should wrap coherent business operations.

Transaction should include:

```text
primary state change
audit event write
runtime event write or outbox record
idempotency record update when relevant
```

Rule:

```text
Do not commit business state while losing audit evidence for the same operation.
```

---

# 16. Audit Emission Pattern

Application services should use AuditService.

Recommended call shape:

```text
AuditService.record(context, audit_input)
```

Audit input includes:

```text
action
object_type
object_id
before_state optional
after_state optional
ai_assisted
human_confirmed
source_event_id optional
```

Rule:

```text
Audit action names must match canonical audit vocabulary.
```

---

# 17. Runtime Event Emission Pattern

Application services should use RuntimeEventService.

Recommended call shape:

```text
RuntimeEventService.emit(context, event_input)
```

Event input includes:

```text
event_type
source_object_type
source_object_id
payload
correlation_id
causation_id optional
```

Runtime events may be persisted directly or through an outbox pattern.

---

# 18. Error Mapping Pattern

Application services should raise structured errors.

Error mapping:

```text
ValidationError → validation_error
AuthorizationError → forbidden
NotFoundError → not_found
WorkspaceArchivedError → workspace_archived
InvalidStatusTransition → invalid_status_transition
HumanConfirmationRequired → human_confirmation_required
InvalidAgentAuthority → invalid_agent_authority
CredentialValueNotAllowed → credential_value_not_allowed
```

Rule:

```text
Controllers map service errors to API error contracts consistently.
```

---

# 19. AI Action Pattern

AI-generated effects must follow governed flow:

```text
AI output
↓
recommendation or draft record
↓
human review or authority check
↓
service validation
↓
transactional application
↓
audit event
↓
runtime event
```

Rule:

```text
AI outputs cannot bypass application services.
```

---

# 20. Integration Secret Pattern

Integration services should use credential references.

Flow:

```text
IntegrationService receives credential_ref
↓
validates provider and scope
↓
stores credential_ref only
↓
Sync worker resolves secret through SecretReferenceService
↓
raw secret never appears in normal response DTO
```

Rule:

```text
Raw secrets must not cross controller, response DTO or audit boundaries.
```

---

# 21. Idempotency Pattern

Retryable operations may use IdempotencyService.

Flow:

```text
controller extracts Idempotency-Key
↓
service checks idempotency record
↓
if same request completed, return stored result
↓
if new request, execute operation
↓
store result reference
```

Candidate operations:

```text
export job creation
integration sync trigger
operating map generation
AI recommendation application
```

---

# 22. Example: Complete Task Flow

```text
POST /workspaces/{workspace_id}/tasks/{task_id}/complete
↓
TaskController.completeTask
↓
TaskService.completeTask(context, input)
↓
AuthorizationService.requireTaskCompletionPermission
↓
TaskRepository.findByIdAndWorkspace
↓
TaskStatusPolicy.canComplete
↓
Transaction begins
↓
TaskRepository.updateStatus(completed)
↓
AuditService.record(task.completed)
↓
RuntimeEventService.emit(task.completed)
↓
Transaction commits
↓
Response DTO returned
```

---

# 23. Example: Apply Agent Recommendation Flow

```text
POST /workspaces/{workspace_id}/agent-recommendations/{recommendation_id}/apply
↓
AgentRecommendationController.apply
↓
AgentRecommendationService.apply(context, input)
↓
AuthorizationService.requireRecommendationApplyPermission
↓
AgentAuthorityService.validateAuthority
↓
ConfirmationPolicy.validateHumanConfirmationOrAutomationAuthority
↓
Transaction begins
↓
Result object is created or updated
↓
Recommendation status becomes applied
↓
AuditService.record(agent_recommendation.applied)
↓
RuntimeEventService.emit(agent_recommendation.applied)
↓
Transaction commits
↓
Response DTO returned
```

---

# 24. Example: Request Export Flow

```text
POST /workspaces/{workspace_id}/export-jobs
↓
ExportController.createExportJob
↓
ExportService.requestExport(context, input)
↓
AuthorizationService.requireExportPermission
↓
ExportScopePolicy.validateScope
↓
IdempotencyService.check optional
↓
Transaction begins
↓
ExportJobRepository.create(queued)
↓
AuditService.record(export.requested)
↓
RuntimeEventService.emit(export.requested)
↓
Transaction commits
↓
JobQueueService.enqueueExportGeneration
↓
Response DTO returned
```

---

# 25. Testing Expectations

Each layer should be testable.

Controller tests:

```text
request parsing
response mapping
error mapping
```

Service tests:

```text
authorization called
validation rules enforced
status transitions enforced
audit event emitted
runtime event emitted
transaction behavior
```

Repository tests:

```text
workspace filters applied
pagination works
sorting works
queries return expected records
```

---

# 26. MVP Simplifications

MVP may simplify by:

```text
using owner-only AuthorizationService
using simple repositories
using simple transaction manager
using synchronous runtime event persistence
using minimal domain policy classes
using simple DTO mapping
```

But MVP must preserve:

```text
workspace isolation
audit events for important mutations
runtime event creation for coordination
AI confirmation rules
error contract mapping
secret safety
```

---

# 27. Anti-Patterns

Avoid:

```text
controller directly writing database
repository deciding if user may act
service returning raw ORM objects to API
AI action applied from controller
mutation without transaction where audit is required
runtime event emitted without correlation_id
secrets in audit payload
workspace_id accepted from body instead of path context
cross-workspace repository queries
```

---

# 28. Acceptance Criteria

Controller Service Repository Pattern is accepted when:

- controller responsibilities are defined;
- service responsibilities are defined;
- repository responsibilities are defined;
- DTO boundaries are defined;
- mutation and read flows are documented;
- transaction pattern is documented;
- audit and runtime event emission patterns are documented;
- AI action pattern is documented;
- integration secret pattern is documented;
- example flows are provided;
- MVP simplifications and anti-patterns are documented.

Status:

```text
Accepted for Workspace Service Design
```

---

# 29. Final Statement

```text
Bizzi Controller-Service-Repository Pattern defines how backend requests flow from API boundary to governed service behavior and persistent state while preserving workspace isolation, auditability, transaction safety and AI governance.
```

This pattern governs all detailed service design documents in the `29_BACKEND_SERVICE_DESIGN` layer.