# 10_CREATE_MEMORY_SOURCE.md

# Bizzi Platform

## Create Memory Source

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Implementation Plan  
**Previous Layer Reference:** 32_BACKEND_CODEBASE_BUILD  
**Product:** Bizzi Platform  
**Status:** Draft v0.1

---

# 1. Purpose

This document defines the source-code implementation plan for the Bizzi Memory module.

It translates the canonical memory specification into real backend source files for managing workspace-scoped memory entries, memory activation and audit-backed knowledge lifecycle operations.

---

# 2. Source Files To Create

Target directory:

```text
backend/src/modules/memory/
```

Files:

```text
memory.module.ts
memory.controller.ts
memory.service.ts
memory-activation.service.ts
memory.repository.ts
dto/create-memory-entry.dto.ts
dto/update-memory-entry.dto.ts
dto/activate-memory-entry.dto.ts
dto/memory-entry-response.dto.ts
mappers/memory.mapper.ts
policies/memory-status.policy.ts
```

Tests:

```text
backend/src/modules/memory/__tests__/memory.service.spec.ts
backend/src/modules/memory/__tests__/memory.repository.spec.ts
backend/test/e2e/memory.e2e-spec.ts
```

---

# 3. Module Responsibilities

The Memory module must:

```text
create candidate memory entries
list memory entries by workspace
read memory entry by id and workspace
update candidate memory entries
activate candidate memory entries
archive memory entries
reject invalid lifecycle transitions
reject cross-workspace references
record audit events transactionally
return safe DTO responses
```

---

# 4. API Routes

Required routes:

```text
POST /api/v1/workspaces/{workspace_id}/memory-entries
GET /api/v1/workspaces/{workspace_id}/memory-entries
GET /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}
PATCH /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/activate
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/archive
```

---

# 5. DTOs

## CreateMemoryEntryDto

Fields:

```text
title
content
summary optional
memory_type optional
task_id optional
decision_id optional
source_object_type optional
source_object_id optional
metadata optional
```

Validation:

```text
title required
content required
optional references must be valid UUIDs
metadata must be object-like if provided
```

## UpdateMemoryEntryDto

Fields:

```text
title optional
content optional
summary optional
metadata optional
```

Rule:

```text
Archived memory entries cannot be updated.
```

## ActivateMemoryEntryDto

Fields:

```text
activation_note optional
metadata optional
```

Rule:

```text
Only candidate memory entries can be activated.
```

## MemoryEntryResponseDto

Fields:

```text
id
workspace_id
title
summary
content
memory_type
status
task_id
decision_id
source_object_type
source_object_id
confirmed_by
confirmed_at
metadata
created_at
updated_at
archived_at
```

---

# 6. Repository Contract

`MemoryRepository` must expose:

```text
createMemoryEntry(db, data)
findByIdAndWorkspace(db, memoryEntryId, workspaceId)
listByWorkspace(db, workspaceId, query)
listActiveByWorkspace(db, workspaceId, query)
updateMemoryEntry(db, memoryEntryId, workspaceId, data)
activateMemoryEntry(db, memoryEntryId, workspaceId, data)
archiveMemoryEntry(db, memoryEntryId, workspaceId, data)
countByWorkspaceAndStatus(db, workspaceId, status)
```

Repository rules:

```text
all reads and writes must include workspace_id
repositories return persistence records, not DTOs
repository methods must support transaction clients
cross-workspace access must return null or no-op result
```

---

# 7. Service Contract

`MemoryService` must expose:

```text
createMemoryEntry(context, workspaceId, dto)
listMemoryEntries(context, workspaceId, query)
getMemoryEntry(context, workspaceId, memoryEntryId)
updateMemoryEntry(context, workspaceId, memoryEntryId, dto)
archiveMemoryEntry(context, workspaceId, memoryEntryId)
```

`MemoryActivationService` must expose:

```text
activateMemoryEntry(context, workspaceId, memoryEntryId, dto)
```

Service rules:

```text
attach workspace_id to service context
require workspace owner
require active workspace for mutations
validate object references
validate lifecycle transitions
wrap mutation and audit event in one transaction
return DTOs only
```

---

# 8. Lifecycle Policy

Allowed transitions:

```text
candidate -> active
candidate -> archived
active -> archived
```

Forbidden transitions:

```text
active -> candidate
archived -> active
archived -> candidate
active -> active
```

Policy file:

```text
policies/memory-status.policy.ts
```

Required functions:

```text
canActivate(status)
canArchive(status)
canMutate(status)
assertActivationAllowed(status)
assertMutationAllowed(status)
```

---

# 9. Audit Events

Required audit actions:

```text
memory.created
memory.updated
memory.activated
memory.archived
```

Audit rules:

```text
audit events must be created in the same transaction as the mutation
before_state and after_state must be sanitized
actor_id and correlation_id must come from ServiceContext
mutation must fail if required audit event fails
```

---

# 10. Authorization And Validation

The module must use:

```text
AuthorizationService.requireWorkspaceOwner
AuthorizationService.requireWorkspaceMutation
ObjectReferenceValidator.requireTaskInWorkspace
ObjectReferenceValidator.requireDecisionInWorkspace
StatusTransitionValidator.requireMemoryActivationAllowed
BusinessRuleValidator
```

Validation failures map to:

```text
validation_error
invalid_object_reference
invalid_status_transition
workspace_archived
forbidden
not_found
```

---

# 11. Mapper

`MemoryMapper.toDto(record)` maps persistence fields to API response fields.

Rules:

```text
no raw internal database metadata
no secret metadata leakage
snake_case API fields preserved
null values handled consistently
```

---

# 12. Tests

Required unit tests:

```text
candidate memory can be activated
active memory cannot be activated again
archived memory cannot be activated
archived memory cannot be mutated
mapper returns safe DTO
```

Required repository tests:

```text
create memory entry
find by id and workspace
return null for cross-workspace lookup
list by workspace
list active by workspace
update by id and workspace
count by status
```

Required e2e tests:

```text
POST memory entry succeeds
GET memory list succeeds
GET memory detail succeeds
POST activate succeeds
activation creates audit event
cross-workspace access is rejected
invalid transition returns canonical error
```

---

# 13. Implementation Order

```text
1. Create DTOs
2. Create memory status policy
3. Create memory mapper
4. Create memory repository
5. Create memory service
6. Create memory activation service
7. Create memory controller
8. Wire memory module into AppModule
9. Add unit tests
10. Add repository tests
11. Add e2e tests
12. Run typecheck, tests and build
```

---

# 14. Acceptance Criteria

Memory source implementation is accepted when:

- all source files are created;
- memory routes are implemented;
- memory lifecycle is enforced;
- workspace isolation is enforced;
- task and decision references are validated;
- audit events are emitted transactionally;
- DTO responses are safe and canonical;
- unit, repository and e2e tests pass;
- backend typecheck and build pass.

---

# 15. Final Statement

```text
Bizzi Memory Source Implementation creates the backend knowledge lifecycle module that turns workspace knowledge into auditable, activatable and reusable organizational memory.
```
