# 11_CREATE_AUDIT_SOURCE.md

# Bizzi Platform

## Create Audit Source

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Implementation Plan  
**Previous Layer:** 32_BACKEND_CODEBASE_BUILD  
**Module:** Audit  
**Status:** Draft v0.1

---

# 1. Purpose

This document defines the concrete source-code creation plan for the Bizzi Audit module.

The goal is to materialize the audit implementation from the previous architecture layers into real backend source files under:

```text
backend/src/modules/audit/
```

The Audit module records append-only business evidence for meaningful state changes across workspace, task, decision, memory and future runtime modules.

---

# 2. Source Files To Create

Target files:

```text
backend/src/modules/audit/audit.module.ts
backend/src/modules/audit/controllers/audit-event.controller.ts
backend/src/modules/audit/services/audit.service.ts
backend/src/modules/audit/services/audit-query.service.ts
backend/src/modules/audit/services/audit-event-factory.service.ts
backend/src/modules/audit/repositories/audit-event.repository.ts
backend/src/modules/audit/dto/create-audit-event.input.ts
backend/src/modules/audit/dto/audit-event-query.dto.ts
backend/src/modules/audit/dto/audit-event-response.dto.ts
backend/src/modules/audit/mappers/audit-event.mapper.ts
backend/src/modules/audit/policies/audit-payload.policy.ts
backend/src/modules/audit/tests/audit.service.spec.ts
backend/src/modules/audit/tests/audit-event.repository.spec.ts
backend/test/e2e/audit-event.e2e-spec.ts
```

---

# 3. AuditModule

File:

```text
backend/src/modules/audit/audit.module.ts
```

Responsibilities:

```text
register AuditService
register AuditQueryService
register AuditEventFactoryService
register AuditEventRepository
register AuditEventController
export AuditService for feature modules
```

Required imports:

```text
SharedModule
DatabaseModule or PrismaModule
AuthorizationModule
```

Rule:

```text
Feature modules must depend on AuditService, not directly on AuditEventRepository.
```

---

# 4. AuditEventRepository

File:

```text
backend/src/modules/audit/repositories/audit-event.repository.ts
```

Required methods:

```text
create(db, data)
findByIdAndWorkspace(db, auditEventId, workspaceId)
listByWorkspace(db, workspaceId, filters, pagination)
countByWorkspace(db, workspaceId, filters)
countRecentByWorkspace(db, workspaceId, since)
```

Rules:

```text
all read queries must include workspace_id
repository returns persistence records
repository supports transaction client
repository must not expose cross-workspace events
```

---

# 5. AuditService

File:

```text
backend/src/modules/audit/services/audit.service.ts
```

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

Rules:

```text
record must require workspace_id in ServiceContext
record must copy actor context from ServiceContext
record must require correlation_id
record must use AuditEventFactoryService
record must write through AuditEventRepository
record must run inside the same transaction client passed by feature service
```

---

# 6. AuditQueryService

File:

```text
backend/src/modules/audit/services/audit-query.service.ts
```

Required methods:

```text
listAuditEvents(context, workspaceId, query)
getAuditEvent(context, workspaceId, auditEventId)
```

Responsibilities:

```text
require workspace owner
normalize pagination
validate filters
query repository
map records to response DTOs
```

Rule:

```text
Audit read APIs are owner-restricted in MVP.
```

---

# 7. AuditEventFactoryService

File:

```text
backend/src/modules/audit/services/audit-event-factory.service.ts
```

Responsibilities:

```text
build canonical audit event payload
derive workspace_id from context
copy actor_type, actor_id and agent_id from context
copy correlation_id from context
sanitize before_state
after_state and metadata
normalize severity
normalize action and object_type
```

Default values:

```text
severity = info
ai_assisted = context.aiAssisted ?? false
human_confirmed = context.humanConfirmed ?? true
```

---

# 8. DTOs

## 8.1 CreateAuditEventInput

File:

```text
backend/src/modules/audit/dto/create-audit-event.input.ts
```

Fields:

```text
action
object_type
object_id
source_event_id optional
before_state optional
after_state optional
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

## 8.2 AuditEventQueryDto

File:

```text
backend/src/modules/audit/dto/audit-event-query.dto.ts
```

Fields:

```text
page
page_size
action
object_type
object_id
actor_id
correlation_id
severity
from_timestamp
to_timestamp
```

## 8.3 AuditEventResponseDto

File:

```text
backend/src/modules/audit/dto/audit-event-response.dto.ts
```

Fields:

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

---

# 9. AuditEventMapper

File:

```text
backend/src/modules/audit/mappers/audit-event.mapper.ts
```

Required methods:

```text
toDto(record)
toDtoList(records)
```

Rules:

```text
map database names to API names
preserve sanitized JSON fields
never expose internal ORM metadata
```

---

# 10. AuditEventController

File:

```text
backend/src/modules/audit/controllers/audit-event.controller.ts
```

Routes:

```text
GET /api/v1/workspaces/:workspace_id/audit-events
GET /api/v1/workspaces/:workspace_id/audit-events/:audit_event_id
```

Responsibilities:

```text
extract workspace_id from route
extract query DTO
extract RequestContext through decorator
call AuditQueryService
return paginated response or single event
```

Rule:

```text
Controller must not contain authorization logic directly; it delegates to AuditQueryService.
```

---

# 11. Payload Safety

Audit payloads must be sanitized before persistence.

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

Rule:

```text
Audit event payloads are business evidence, not raw database dumps.
```

---

# 12. Transaction Pattern

Feature services must call AuditService inside the same mutation transaction.

Pattern:

```text
await transaction.run(async (tx) => {
  const record = await featureRepository.create(tx, data)
  await auditService.record(tx, context, auditInput)
  return record
})
```

Rule:

```text
If required audit creation fails, the primary mutation must rollback.
```

---

# 13. Required Audit Events For MVP

```text
workspace.created
workspace.updated
workspace_settings.updated
task.created
task.completed
decision.created
decision.confirmed
memory.created
memory.activated
```

Object types:

```text
workspace
workspace_settings
task
decision
memory_entry
```

---

# 14. Tests To Create

## 14.1 Unit Tests

```text
AuditEventFactoryService builds canonical payload
AuditEventFactoryService sanitizes forbidden fields
AuditEventMapper maps record to DTO
AuditService rejects missing workspace_id
AuditService preserves correlation_id
```

## 14.2 Repository Tests

```text
create audit event
list audit events by workspace
find audit event by id and workspace
reject cross-workspace lookup
filter by action
filter by object_type
filter by correlation_id
paginate results
```

## 14.3 E2E Tests

```text
GET /audit-events returns workspace events
non-owner cannot read audit events
filters work
pagination works
canonical error returned for invalid query
```

---

# 15. Acceptance Criteria

Audit source implementation is accepted when:

- Audit module files are created;
- AuditEventRepository is implemented;
- AuditService is implemented;
- AuditQueryService is implemented;
- AuditEventFactoryService is implemented;
- DTOs are implemented;
- mapper is implemented;
- controller routes are implemented;
- payload sanitization is enforced;
- transaction pattern is followed;
- unit, repository and e2e tests are defined;
- workspace isolation is preserved;
- audit writes are append-only.

---

# 16. Final Statement

```text
The Audit source implementation creates the append-only business evidence layer for Bizzi backend source code.
```

This module is required before business mutations can be considered governance-safe and AI-auditable.