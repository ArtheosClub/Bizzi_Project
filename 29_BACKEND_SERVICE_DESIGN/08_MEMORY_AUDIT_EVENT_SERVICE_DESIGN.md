# 08_MEMORY_AUDIT_EVENT_SERVICE_DESIGN.md

# Bizzi Platform

## Memory Audit Event Service Design

**Layer:** 29_BACKEND_SERVICE_DESIGN  
**Component Type:** Backend Service Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 08_MEMORY_RUNTIME.md, 09_AUDIT_RUNTIME.md, 10_EVENT_RUNTIME.md  
**Domain Reference:** 26_DOMAIN_MODEL / 09_MEMORY_DOMAIN.md, 10_AUDIT_AND_EVENT_DOMAIN.md  
**Data Model Reference:** 27_DATA_MODEL / 08_MEMORY_AUDIT_EVENT_DATA_MODEL.md  
**API Contracts Reference:** 28_API_CONTRACTS / 07_MEMORY_AUDIT_EVENT_API.md  
**Previous Document:** 07_AGENT_PROCESS_TASK_DECISION_SERVICE_DESIGN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the backend service design for memory, audit and runtime event behavior in Bizzi Platform.

It specifies the services, repositories, validation rules, authorization rules, transaction patterns, audit behavior and runtime event behavior required to implement the Memory Audit Event API.

Core question:

```text
How should Bizzi backend services preserve enterprise memory, create audit evidence and coordinate runtime events safely and consistently?
```

---

# 2. Service Scope

This design covers:

```text
MemoryService
MemoryActivationService
MemoryContextService later
AuditService
AuditQueryService
RuntimeEventService
RuntimeEventQueryService
EventDispatchService later
```

Primary API references:

```text
GET /api/v1/workspaces/{workspace_id}/memory-entries
POST /api/v1/workspaces/{workspace_id}/memory-entries
GET /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}
PATCH /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/activate
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/archive
GET /api/v1/workspaces/{workspace_id}/audit-events
GET /api/v1/workspaces/{workspace_id}/audit-events/{audit_event_id}
GET /api/v1/workspaces/{workspace_id}/runtime-events
GET /api/v1/workspaces/{workspace_id}/runtime-events/{runtime_event_id}
```

Primary data references:

```text
memory_entries
audit_events
runtime_events
users
agents
functions
processes
tasks
decisions
```

---

# 3. Module Ownership

Memory, audit and runtime event behavior is distributed across:

```text
MemoryModule
AuditModule
EventModule
```

Supporting modules:

```text
WorkspaceModule
AuthorizationModule
ValidationModule
AgentModule
TaskModule
DecisionModule
DashboardModule via runtime event
TransactionModule
```

Rule:

```text
AuditModule owns canonical evidence. EventModule owns coordination events. MemoryModule owns reusable knowledge and AI context eligibility.
```

---

# 4. Service Responsibilities

## MemoryService

Responsibilities:

```text
list memory entries
get memory entry
create memory entry
update memory entry
archive memory entry
validate memory source traceability
validate memory validity periods
emit memory audit events
emit memory runtime events
```

## MemoryActivationService

Responsibilities:

```text
activate memory entries
validate activation status
validate human confirmation for AI-generated memory
set confirmed_by and confirmed_at
ensure expired memory cannot become active
ensure archived memory is excluded from active context
```

## MemoryContextService later

Responsibilities:

```text
assemble active memory context for AI orchestration
filter by workspace, object, function, process, task and decision
exclude archived and expired memory
track memory usage later
```

## AuditService

Responsibilities:

```text
record audit events for meaningful state changes
standardize audit action names
capture actor context
capture object reference
capture before_state and after_state when needed
capture ai_assisted and human_confirmed flags
capture correlation_id
preserve append-oriented audit behavior
```

## AuditQueryService

Responsibilities:

```text
list audit events for authorized users
get audit event detail
apply audit filters
protect audit visibility
prevent audit mutation through public API
```

## RuntimeEventService

Responsibilities:

```text
emit runtime events
persist event payloads safely
link source object
assign correlation_id and causation_id
record processing status
support outbox or dispatch later
```

## RuntimeEventQueryService

Responsibilities:

```text
list runtime events for authorized users
get runtime event detail
restrict operational visibility
filter runtime events by source, actor, agent and correlation_id
```

---

# 5. Repository Responsibilities

## MemoryRepository

Methods:

```text
createMemoryEntry(data)
findByIdAndWorkspace(memory_entry_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
updateByIdAndWorkspace(memory_entry_id, workspace_id, patch)
activateByIdAndWorkspace(memory_entry_id, workspace_id, activation_data)
archiveByIdAndWorkspace(memory_entry_id, workspace_id, archive_data)
listActiveForContext(workspace_id, context_filters)
```

## AuditEventRepository

Methods:

```text
createAuditEvent(data)
findByIdAndWorkspace(audit_event_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
listByObject(workspace_id, object_type, object_id, pagination)
listByCorrelationId(workspace_id, correlation_id, pagination)
```

## RuntimeEventRepository

Methods:

```text
createRuntimeEvent(data)
findByIdAndWorkspace(runtime_event_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
listBySourceObject(workspace_id, source_object_type, source_object_id, pagination)
listByCorrelationId(workspace_id, correlation_id, pagination)
markProcessed(runtime_event_id, processing_data)
markFailed(runtime_event_id, failure_data)
```

---

# 6. Service Context

Every service method should receive:

```text
workspace_id
actor_id
actor_type
correlation_id
request_id
agent_id optional
source_event_id optional
ai_assisted boolean optional
human_confirmed boolean optional
```

Rule:

```text
Memory, audit and runtime event services must preserve correlation across requests, state changes, audit evidence and downstream coordination.
```

---

# 7. Create Memory Entry Flow

## Service Method

```text
MemoryService.createMemoryEntry(context, input)
```

## Input

```text
memory_type
title
summary optional
content optional
source_object_type optional
source_object_id optional
function_id optional
process_id optional
task_id optional
decision_id optional
agent_id optional
valid_from optional
valid_until optional
metadata optional
```

## Flow

```text
validate authenticated actor
load workspace
check workspace is active
check create memory permission
validate memory_type
validate title
validate content or summary exists
validate source object if provided
validate linked object references
validate valid_from and valid_until
begin transaction
create memory entry with candidate status
record memory.created audit event
emit memory.created runtime event
emit dashboard.refresh_requested optional runtime event
commit transaction
return memory DTO
```

---

# 8. Memory Validation Rules

Validation rules:

```text
memory_type must be valid
title is required
content or summary is required
source_object_type must be valid if supplied
source_object_id must exist if supplied
source object must belong to same workspace when workspace-scoped
function_id must belong to workspace if supplied
process_id must belong to workspace if supplied
task_id must belong to workspace if supplied
decision_id must belong to workspace if supplied
agent_id must belong to workspace if supplied
valid_until must be after valid_from when both are supplied
```

Error mappings:

```text
missing title → validation_error
missing content and summary → validation_error
invalid source object → invalid_source_object
invalid reference → invalid_object_reference
invalid validity range → validation_error
workspace archived → workspace_archived
```

---

# 9. List and Get Memory Flow

## List Method

```text
MemoryService.listMemoryEntries(context, filters, pagination)
```

Supported filters:

```text
status
memory_type
confidence
source_object_type
source_object_id
function_id
process_id
task_id
decision_id
agent_id
valid_on
```

Flow:

```text
validate authenticated actor
check workspace access
validate filters
call MemoryRepository.listByWorkspace
return paginated memory DTOs
```

## Get Method

```text
MemoryService.getMemoryEntry(context, memory_entry_id)
```

Flow:

```text
validate authenticated actor
check workspace access
load memory entry by id and workspace_id
return memory DTO
```

---

# 10. Update Memory Entry Flow

## Service Method

```text
MemoryService.updateMemoryEntry(context, memory_entry_id, input)
```

Mutable fields:

```text
title
summary
content
valid_from
valid_until
metadata
```

Flow:

```text
validate authenticated actor
load workspace
check workspace is active
check update memory permission
load memory entry by id and workspace_id
check memory is not archived
validate mutable fields
capture before_state
begin transaction
update memory entry
record memory.updated audit event
emit memory.updated runtime event
commit transaction
return memory DTO
```

---

# 11. Activate Memory Entry Flow

## Service Method

```text
MemoryActivationService.activateMemoryEntry(context, memory_entry_id, input)
```

Input:

```text
confirmation_note optional
```

Flow:

```text
validate authenticated actor
load workspace
check workspace is active
check activate memory permission
load memory entry by id and workspace_id
validate memory is not archived or rejected
validate memory is not expired
if AI-generated, validate human confirmation or automation authority
capture before_state
begin transaction
set status active
set confidence confirmed when applicable
set confirmed_by
set confirmed_at
record memory.activated audit event
emit memory.activated runtime event
commit transaction
return memory DTO
```

Rule:

```text
Only active, non-expired, non-archived memory may be used for AI context assembly.
```

---

# 12. Archive Memory Entry Flow

## Service Method

```text
MemoryService.archiveMemoryEntry(context, memory_entry_id, input)
```

Input:

```text
archive_reason optional
```

Flow:

```text
validate authenticated actor
load workspace
check archive memory permission
load memory entry by id and workspace_id
check memory is not already archived
capture before_state
begin transaction
set status archived
set archived_at
record memory.archived audit event
emit memory.archived runtime event
commit transaction
return memory DTO
```

Rule:

```text
Archived memory must not be used as active AI context.
```

---

# 13. Audit Event Creation Pattern

## Service Method

```text
AuditService.record(context, input)
```

Input:

```text
action
object_type
object_id
before_state optional
after_state optional
source_event_id optional
ai_assisted optional
human_confirmed optional
severity optional
metadata optional
```

Flow:

```text
validate workspace_id
validate action name
validate object_type and object_id
build audit event payload
attach actor context
attach agent_id when applicable
attach correlation_id
persist audit event
return audit event id
```

Rule:

```text
Feature services should use AuditService instead of handcrafting audit records.
```

---

# 14. Audit Event Query Flow

## List Method

```text
AuditQueryService.listAuditEvents(context, filters, pagination)
```

Supported filters:

```text
action
actor_type
actor_id
agent_id
object_type
object_id
ai_assisted
human_confirmed
severity
from_timestamp
to_timestamp
correlation_id
```

Flow:

```text
validate authenticated actor
check audit read permission
validate filters
call AuditEventRepository.listByWorkspace
return paginated audit event DTOs
```

## Get Method

```text
AuditQueryService.getAuditEvent(context, audit_event_id)
```

Flow:

```text
validate authenticated actor
check audit read permission
load audit event by id and workspace_id
return audit event DTO
```

Rule:

```text
Audit events are read-oriented through public APIs and must not be updated or deleted by normal service flows.
```

---

# 15. Runtime Event Creation Pattern

## Service Method

```text
RuntimeEventService.emit(context, input)
```

Input:

```text
event_type
source_object_type
source_object_id
payload optional
causation_id optional
agent_id optional
```

Flow:

```text
validate workspace_id
validate event_type
validate source object reference where required
sanitize payload
attach actor context
attach agent_id when applicable
attach correlation_id
attach causation_id when applicable
create runtime event with pending or processed status according to implementation
return runtime event id
```

Rule:

```text
Runtime events coordinate downstream behavior and are not substitutes for audit events.
```

---

# 16. Runtime Event Query Flow

## List Method

```text
RuntimeEventQueryService.listRuntimeEvents(context, filters, pagination)
```

Supported filters:

```text
event_type
status
source_object_type
source_object_id
actor_type
actor_id
agent_id
correlation_id
from_timestamp
to_timestamp
```

Flow:

```text
validate authenticated actor
check runtime event read permission
validate filters
call RuntimeEventRepository.listByWorkspace
return paginated runtime event DTOs
```

## Get Method

```text
RuntimeEventQueryService.getRuntimeEvent(context, runtime_event_id)
```

Flow:

```text
validate authenticated actor
check runtime event read permission
load runtime event by id and workspace_id
return runtime event DTO
```

Rule:

```text
Runtime events may expose operational details and should be restricted by default.
```

---

# 17. Transaction Pattern

Memory mutations should include:

```text
memory state change
audit event
runtime event
```

Feature mutations in other services should include:

```text
primary state change
AuditService.record call
RuntimeEventService.emit call
```

Recommended pattern:

```text
begin transaction
write primary business state
write audit event
write runtime event or outbox record
commit transaction
```

Rule:

```text
Do not commit meaningful business changes while losing the associated audit evidence.
```

---

# 18. Authorization Rules

Memory, audit and event authorization matrix:

| Operation | MVP Rule | Expansion Rule |
|---|---|---|
| List memory | workspace owner | active workspace access |
| Create memory | workspace owner | owner/admin/manager |
| Update memory | workspace owner | owner/admin/manager |
| Activate memory | workspace owner | owner/admin with confirmation |
| Archive memory | workspace owner | owner/admin/manager |
| List audit events | workspace owner | owner/admin/auditor |
| Get audit event | workspace owner | owner/admin/auditor |
| List runtime events | workspace owner | owner/admin/internal service |
| Get runtime event | workspace owner | owner/admin/internal service |
| Emit audit event | internal service | internal service only |
| Emit runtime event | internal service | internal service only |

---

# 19. Audit Events

Memory services should emit:

```text
memory.created
memory.updated
memory.activated
memory.archived
```

Audit read operations may optionally emit security-sensitive read events:

```text
audit_event.read
runtime_event.read
```

AuditService itself creates events for other modules and should standardize:

```text
workspace_id
actor_type
actor_id
agent_id optional
action
object_type
object_id
source_event_id optional
ai_assisted
human_confirmed
severity
correlation_id
before_state optional
after_state optional
```

---

# 20. Runtime Events

Memory and event services should emit:

```text
memory.created
memory.updated
memory.activated
memory.archived
dashboard.refresh_requested optional
memory.candidate_created from other modules optional
```

RuntimeEventService supports events from other modules:

```text
workspace.created
task.completed
decision.confirmed
integration.sync_requested
export.requested
```

---

# 21. DTOs

Memory DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "memory_type": "decision_summary",
  "title": "Supplier approval rule",
  "summary": "Suppliers above a threshold require owner confirmation",
  "status": "active",
  "confidence": "confirmed",
  "source_object_type": "decision",
  "source_object_id": "uuid",
  "valid_from": "2026-07-01",
  "valid_until": null,
  "confirmed_by": "uuid",
  "confirmed_at": "2026-07-01T12:00:00Z"
}
```

Audit Event DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "timestamp": "2026-07-01T12:00:00Z",
  "actor_type": "user",
  "actor_id": "uuid",
  "agent_id": null,
  "action": "decision.confirmed",
  "object_type": "decision",
  "object_id": "uuid",
  "ai_assisted": false,
  "human_confirmed": true,
  "severity": "info",
  "correlation_id": "uuid"
}
```

Runtime Event DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "event_type": "task.completed",
  "status": "processed",
  "source_object_type": "task",
  "source_object_id": "uuid",
  "correlation_id": "uuid",
  "causation_id": "uuid",
  "timestamp": "2026-07-01T12:00:00Z",
  "processed_at": "2026-07-01T12:00:05Z"
}
```

---

# 22. Error Mapping

Memory, audit and event service errors:

```text
Unauthenticated → unauthenticated
WorkspaceNotFound → not_found
WorkspaceArchived → workspace_archived
MemoryEntryNotFound → not_found
AuditEventNotFound → not_found
RuntimeEventNotFound → not_found
AccessDenied → forbidden
InvalidMemoryType → validation_error
InvalidSourceObject → invalid_source_object
InvalidObjectReference → invalid_object_reference
InvalidValidityRange → validation_error
InvalidStatusTransition → invalid_status_transition
HumanConfirmationRequired → human_confirmation_required
AuditEventReadOnly → audit_event_read_only
RuntimeEventRestricted → runtime_event_restricted
```

---

# 23. Retention and Safety Rules

Memory rules:

```text
candidate memory is not active AI context
active memory may be used for AI context
archived memory must not be used for AI context
expired memory must not be used for AI context
AI-generated memory requires review unless automation policy allows activation
```

Audit rules:

```text
audit events are append-oriented
audit events should not be hard-deleted through normal service flows
audit payloads must not contain raw secrets
audit events should preserve correlation_id
```

Runtime event rules:

```text
runtime event payloads must avoid raw secrets
processed runtime events may follow retention windows
failed runtime events may be retained longer
runtime event access should be restricted by default
```

---

# 24. MVP Simplifications

MVP may simplify by:

```text
memory entries only, without memory sources and usage tracking
owner-only audit visibility
simple runtime event persistence without async dispatcher
manual memory activation
simple candidate → active → archived lifecycle
basic filtering and pagination
```

MVP must preserve:

```text
workspace scope
active memory safety rules
audit event creation for meaningful mutations
runtime event creation for coordination
correlation_id propagation
raw secret exclusion from audit and event payloads
structured error mapping
```

---

# 25. Future Expansion

Future service expansion may add:

```text
memory sources
memory reviews
memory usage tracking
semantic memory search
memory embeddings
memory context assembly policies
audit exports
audit redaction request workflow
event dispatcher
event handler runs
event retry strategy
event failure diagnostics
runtime event replay internal only
```

---

# 26. Testing Expectations

Service tests should cover:

```text
create memory validates required fields
create memory validates source object workspace
activate memory rejects archived or expired memory
activate AI-generated memory requires confirmation
archive memory excludes it from active context
audit service records actor, object and correlation_id
runtime event service records source object and correlation_id
audit query enforces auditor permission
runtime event query enforces restricted permission
raw secrets are not stored in audit or event payloads
workspace archived blocks memory mutations
```

Repository tests should cover:

```text
list memory by workspace and filters
find memory by id and workspace
list active memory for context
list audit events by object
list audit events by correlation_id
list runtime events by source object
mark runtime event processed
pagination and sorting behavior
```

---

# 27. Acceptance Criteria

Memory Audit Event Service Design is accepted when:

- MemoryService responsibilities are defined;
- MemoryActivationService responsibilities are defined;
- AuditService responsibilities are defined;
- AuditQueryService responsibilities are defined;
- RuntimeEventService responsibilities are defined;
- RuntimeEventQueryService responsibilities are defined;
- repository methods are identified;
- memory create, update, activate and archive flows are documented;
- audit event creation and query flows are documented;
- runtime event creation and query flows are documented;
- authorization matrix is defined;
- DTOs and error mappings are documented;
- retention, safety, MVP and testing expectations are documented.

Status:

```text
Accepted for Integration Security Service Design
```

---

# 28. Final Statement

```text
Bizzi Memory Audit Event Service Design defines how backend services preserve workspace knowledge, create audit evidence and coordinate runtime activity through secure, traceable and AI-safe service behavior.
```

This service layer makes Bizzi explainable, governable and capable of preserving enterprise memory.