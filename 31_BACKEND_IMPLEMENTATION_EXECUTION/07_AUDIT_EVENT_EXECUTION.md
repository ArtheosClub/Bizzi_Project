# 07_AUDIT_EVENT_EXECUTION.md

# Bizzi Platform

## Audit Event Execution

**Layer:** 31_BACKEND_IMPLEMENTATION_EXECUTION  
**Component Type:** Execution Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Implementation Plan Reference:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Previous Document:** 06_AUTHORIZATION_VALIDATION_EXECUTION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch III — Backend Execution

---

# 1. Purpose

This document defines the Audit Event execution plan for Bizzi Platform backend MVP.

It specifies how to implement append-oriented audit evidence for meaningful state changes: audit repository, audit service, audit DTOs, audit controller, payload sanitization, actor context capture, correlation identifiers, transaction integration and read API.

Core question:

```text
How should Bizzi persist and expose audit evidence so business actions become traceable, reviewable and safe for AI-assisted operations?
```

---

# 2. Audit Event Thesis

```text
Audit events are business evidence, not logs. Every meaningful state-changing service operation should create a structured, workspace-scoped audit event inside the same transaction as the state change.
```

Audit execution proves:

```text
workspace-scoped evidence
actor attribution
object reference traceability
before/after state capture
AI-assisted flagging
human confirmation tracking
correlation_id propagation
payload sanitization
append-oriented persistence
read-only audit API
```

---

# 3. Target Directory Structure

Target structure:

```text
backend/src/modules/audit/
├── audit.module.ts
├── controllers/
│   └── audit-event.controller.ts
├── services/
│   ├── audit.service.ts
│   ├── audit-query.service.ts
│   └── audit-event-factory.service.ts
├── repositories/
│   └── audit-event.repository.ts
├── dto/
│   ├── audit-event.response.dto.ts
│   ├── create-audit-event.input.ts
│   └── audit-event-query.dto.ts
├── mappers/
│   └── audit-event.mapper.ts
├── policies/
│   └── audit-payload.policy.ts
└── tests/
    ├── audit.service.spec.ts
    ├── audit-event.repository.spec.ts
    └── audit-event.e2e-spec.ts
```

---

# 4. Execution Non-Scope

This execution step does not implement:

```text
external audit warehouse
immutable ledger technology
cryptographic event signing
SIEM integration
legal hold workflows
advanced audit analytics
cross-workspace audit reporting
long-term retention automation
```

These may be added in security, compliance or analytics layers later.

---

# 5. Audit Event Model Used

Primary model:

```text
AuditEvent
```

Required fields:

```text
id
workspace_id
timestamp
actor_type
actor_id
agent_id
action
object_type
object_id
source_event_id
before_state
after_state
ai_assisted
human_confirmed
severity
correlation_id
metadata
```

Rule:

```text
AuditEvent is append-oriented. Normal application flows must not update or delete audit_events.
```

---

# 6. AuditRepository

`AuditEventRepository` owns persistence for audit events.

Required methods:

```text
create(db, data)
listByWorkspace(db, workspaceId, filters, pagination)
findByIdAndWorkspace(db, id, workspaceId)
countByWorkspace(db, workspaceId, filters)
```

Rules:

```text
create must support transaction client
list queries must be workspace-scoped
list queries must be paginated
repository returns records, not API DTOs
repository must not sanitize payloads itself unless receiving already-sanitized data from service/factory
```

---

# 7. AuditService

`AuditService` records audit evidence for state changes.

Required methods:

```text
record(db, context, input)
recordWorkspaceCreated(db, context, workspace)
recordTaskCreated(db, context, task)
recordTaskCompleted(db, context, beforeTask, afterTask)
recordDecisionCreated(db, context, decision)
recordDecisionConfirmed(db, context, beforeDecision, afterDecision)
recordMemoryCreated(db, context, memoryEntry)
recordMemoryActivated(db, context, beforeMemory, afterMemory)
```

MVP rule:

```text
Generic record(db, context, input) is required; convenience methods are optional but useful.
```

---

# 8. AuditQueryService

`AuditQueryService` exposes read behavior.

Required methods:

```text
listAuditEvents(context, workspaceId, query)
getAuditEvent(context, workspaceId, auditEventId) optional
```

Required behavior:

```text
require workspace owner
normalize pagination
validate filters
query repository
map records to DTOs
```

Rule:

```text
Audit read API must be workspace-scoped and owner-restricted in MVP.
```

---

# 9. AuditEventFactory

`AuditEventFactoryService` prepares safe audit payloads.

Responsibilities:

```text
build standard audit event input
copy actor context
copy workspace_id
copy correlation_id
sanitize before_state
sanitize after_state
normalize action names
normalize object references
set severity
set ai_assisted and human_confirmed flags
```

Rule:

```text
Audit payload construction should be centralized so feature services do not assemble inconsistent event shapes.
```

---

# 10. Create Audit Event Input

`CreateAuditEventInput` should include:

```text
action
object_type
object_id
before_state optional
after_state optional
source_event_id optional
severity optional
metadata optional
ai_assisted optional
human_confirmed optional
```

Derived from context:

```text
workspace_id
actor_type
actor_id
agent_id
correlation_id
```

Rule:

```text
Feature services should not pass actor_id manually when it already exists in ServiceContext.
```

---

# 11. Audit Event Response DTO

`AuditEventResponseDto` should include:

```text
id
workspace_id
timestamp
actor_type
actor_id
agent_id
action
object_type
object_id
source_event_id
before_state
after_state
ai_assisted
human_confirmed
severity
correlation_id
metadata
```

Security rule:

```text
DTO output must contain sanitized payloads only.
```

---

# 12. Audit Query DTO

`AuditEventQueryDto` should support:

```text
page
page_size
action
object_type
object_id
actor_id
from_timestamp
to_timestamp
correlation_id
severity
```

Rules:

```text
unknown filters must be rejected or ignored according to API contract
page_size maximum must be enforced
sort should default to timestamp descending
```

---

# 13. Audit Action Names

MVP audit actions:

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

Rule:

```text
Audit action names should use shared constants from Shared Kernel.
```

---

# 14. Object Type Names

MVP object types:

```text
workspace
workspace_settings
task
decision
memory_entry
```

Rule:

```text
object_type and object_id must refer to the primary business object affected by the action.
```

---

# 15. Actor Attribution

Audit events must capture:

```text
actor_type
actor_id
agent_id optional
```

Rules:

```text
user actions use actor_type=user
system actions use actor_type=system
agent actions require future agent authority layer
agent_id should be present when actor_type=agent
```

MVP rule:

```text
Official user-facing mutations are performed by user actor context.
```

---

# 16. AI-assisted Flags

Audit events should support:

```text
ai_assisted
human_confirmed
```

MVP defaults:

```text
ai_assisted = false
human_confirmed = true
```

Future AI-assisted behavior:

```text
ai_assisted = true when AI produced recommendation or draft
human_confirmed = true only after human confirms official mutation
```

Rule:

```text
AI-generated recommendation is not official state until a service applies it and records audit evidence.
```

---

# 17. Before and After State

Audit events may capture:

```text
before_state
after_state
```

Recommended usage:

```text
create operations: before_state null, after_state new record summary
update operations: before_state previous summary, after_state updated summary
delete/archive operations: before_state previous summary, after_state archived summary
```

Rule:

```text
before_state and after_state should be summaries of business state, not raw full database records with secrets.
```

---

# 18. Payload Sanitization

Audit payloads must use shared sanitizer.

Forbidden fields:

```text
password
token
access_token
refresh_token
api_key
secret
private_key
credential
signed_url
```

Rules:

```text
sanitize before_state
sanitize after_state
sanitize metadata
never store provider tokens
never store credentials directly
```

---

# 19. Correlation and Source Events

Required:

```text
correlation_id
```

Optional:

```text
source_event_id
```

Use cases:

```text
correlation_id links request, audit events, runtime events and logs
source_event_id links audit event to a runtime event or prior cause
```

Rule:

```text
Every audit event must include correlation_id.
```

---

# 20. Transaction Integration

Audit writes for meaningful mutations should occur inside the same transaction as the mutation.

Pattern:

```text
TransactionManager.runInTransaction
↓
primary state mutation
↓
AuditService.record(tx, context, input)
↓
RuntimeEventService.emit(tx, context, input) later
↓
commit
```

Rule:

```text
If required audit event creation fails, the primary mutation should rollback.
```

---

# 21. API Route

Required MVP route:

```text
GET /api/v1/workspaces/{workspace_id}/audit-events
```

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
require workspace owner
support pagination
support core filters
return AuditEventResponseDto list
```

---

# 22. Pagination and Sorting

Default pagination:

```text
page = 1
page_size = 25
max_page_size = 100
```

Default sorting:

```text
timestamp desc
```

Allowed sort fields:

```text
timestamp
action
severity
```

Rule:

```text
Audit event list must never be unbounded.
```

---

# 23. Integration With Existing Modules

WorkspaceModule should record:

```text
workspace.created
workspace_settings.updated later
```

TaskModule later should record:

```text
task.created
task.completed
```

DecisionModule later should record:

```text
decision.created
decision.confirmed
```

MemoryModule later should record:

```text
memory.created
memory.activated
```

---

# 24. Tests Required

Repository tests:

```text
create audit event
list audit events by workspace
reject cross-workspace audit lookup
filter by action
filter by object_type/object_id
filter by correlation_id
paginate results
sort by timestamp descending
```

Service tests:

```text
record creates sanitized audit event
record copies actor context
record copies correlation_id
record rejects missing workspace_id
record rejects missing object reference
record excludes forbidden secret fields
```

API tests:

```text
GET /audit-events returns workspace audit events
non-owner cannot read audit events
pagination defaults are applied
filters work
canonical error returned for invalid query
```

Transaction tests:

```text
workspace creation rollback occurs if required audit write fails
```

---

# 25. Execution Order

Recommended execution order:

```text
1. Create AuditModule
2. Create AuditEventRepository
3. Create AuditEventFactoryService
4. Create AuditService
5. Create AuditEventMapper
6. Create AuditQueryService
7. Create AuditEventController
8. Wire GET /audit-events route
9. Integrate workspace.created audit event into WorkspaceService
10. Add repository tests
11. Add service tests
12. Add API tests
13. Add transaction test for required audit write
14. Verify typecheck/test/build
```

---

# 26. Verification Commands

Expected commands:

```bash
cd backend
pnpm typecheck
pnpm test
pnpm test:e2e
pnpm build
```

Manual smoke sequence:

```text
POST /api/v1/workspaces
GET /api/v1/workspaces/{workspace_id}/audit-events
```

Expected result:

```text
workspace.created audit event appears with actor context and correlation_id
```

---

# 27. Risks and Controls

## Risk 1 — Audit Treated as Logs

Mitigation:

```text
AuditService records structured business evidence; logs remain separate.
```

## Risk 2 — Missing Audit Events for Mutations

Mitigation:

```text
Mutation completion checklist requires audit event emission.
```

## Risk 3 — Sensitive Payload Leakage

Mitigation:

```text
Use AuditEventFactory and sanitizePayload for before_state, after_state and metadata.
```

## Risk 4 — Audit Write Outside Transaction

Mitigation:

```text
Feature services pass transaction client to AuditService.record.
```

---

# 28. Acceptance Criteria

Audit Event Execution is accepted when:

- target directory structure is defined;
- execution non-scope is documented;
- audit model usage is defined;
- AuditEventRepository is defined;
- AuditService is defined;
- AuditQueryService is defined;
- AuditEventFactory is defined;
- audit input and response DTOs are defined;
- query DTO is defined;
- action and object type rules are defined;
- actor attribution rules are defined;
- AI-assisted flags are defined;
- before/after state rules are defined;
- payload sanitization rules are defined;
- correlation/source event rules are defined;
- transaction integration is documented;
- audit read API is defined;
- pagination and sorting are defined;
- module integrations are documented;
- tests are specified;
- execution order and verification commands are documented;
- risks and controls are documented.

Status:

```text
Accepted for Task Decision Execution
```

---

# 29. Final Statement

```text
Bizzi Audit Event Execution defines the append-oriented business evidence layer for the backend MVP.
```

This layer ensures every meaningful state change can be traced by workspace, actor, object, action and correlation_id before Bizzi expands into runtime events, dashboards and AI-assisted execution.