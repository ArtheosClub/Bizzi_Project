# 09_MEMORY_DASHBOARD_EXECUTION.md

# Bizzi Platform

## Memory Dashboard Execution

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
**Previous Document:** 08_TASK_DECISION_EXECUTION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch III — Backend Execution

---

# 1. Purpose

This document defines the Memory and Dashboard execution plan for Bizzi Platform backend MVP.

It specifies how to implement minimal workspace memory and dashboard visibility after the workspace, authorization, audit, task and decision foundations are in place.

Core question:

```text
How should Bizzi implement memory and dashboard modules so the MVP can preserve reusable business knowledge and show workspace operating state?
```

---

# 2. Memory Dashboard Thesis

```text
Memory turns confirmed business knowledge into reusable context, while Dashboard turns workspace execution data into visible operating state.
```

This execution must prove:

```text
memory candidate creation
memory activation
workspace-scoped memory access
memory lifecycle validation
audit evidence for memory changes
dashboard summary counts
dashboard workspace isolation
dashboard read authorization
MVP visibility for task, decision, memory and audit state
```

---

# 3. Target Directory Structure

Target structure:

```text
backend/src/modules/memory/
├── memory.module.ts
├── controllers/
│   └── memory.controller.ts
├── services/
│   ├── memory.service.ts
│   └── memory-activation.service.ts
├── repositories/
│   └── memory.repository.ts
├── dto/
│   ├── create-memory-entry.dto.ts
│   ├── activate-memory-entry.dto.ts
│   ├── memory-entry.response.dto.ts
│   └── memory-entry-query.dto.ts
├── mappers/
│   └── memory-entry.mapper.ts
└── tests/
    ├── memory.service.spec.ts
    ├── memory.repository.spec.ts
    └── memory.e2e-spec.ts

backend/src/modules/dashboard/
├── dashboard.module.ts
├── controllers/
│   └── dashboard.controller.ts
├── services/
│   └── dashboard.service.ts
├── dto/
│   └── dashboard-summary.response.dto.ts
└── tests/
    ├── dashboard.service.spec.ts
    └── dashboard.e2e-spec.ts
```

---

# 4. Execution Non-Scope

This step does not implement:

```text
semantic vector memory
embedding generation
memory similarity search
long-term memory ranking
AI automatic memory activation
advanced dashboard widgets
custom dashboard layouts
stored dashboard metrics
real-time dashboard refresh
analytics warehouse
```

These are later runtime, AI and analytics expansions.

---

# 5. Required API Routes

Memory MVP routes:

```text
POST /api/v1/workspaces/{workspace_id}/memory-entries
GET /api/v1/workspaces/{workspace_id}/memory-entries
GET /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/activate
```

Dashboard MVP route:

```text
GET /api/v1/workspaces/{workspace_id}/dashboard
```

Rule:

```text
All routes must be workspace-scoped and owner-authorized in MVP.
```

---

# 6. Data Models Used

Primary models:

```text
MemoryEntry
Task
Decision
AuditEvent
RuntimeEvent later
CompanyWorkspace
```

Dashboard reads from:

```text
tasks
decisions
memory_entries
audit_events
runtime_events later
```

Rule:

```text
Dashboard MVP should use live counts rather than stored dashboard_metrics.
```

---

# 7. Memory DTOs

`CreateMemoryEntryDto` should include:

```text
title required
summary optional
content required
memory_type optional
task_id optional
decision_id optional
source_object_type optional
source_object_id optional
valid_from optional
valid_until optional
confidence optional
metadata optional
```

`ActivateMemoryEntryDto` may include:

```text
activation_note optional
metadata optional
```

`MemoryEntryResponseDto` should include:

```text
id
workspace_id
task_id
decision_id
memory_type
title
summary
content
status
confidence
source_object_type
source_object_id
valid_from
valid_until
confirmed_by
confirmed_at
metadata
created_at
updated_at
archived_at
```

---

# 8. Dashboard Summary DTO

`DashboardSummaryResponseDto` should include:

```text
workspace_id
open_tasks_count
completed_tasks_count
draft_decisions_count
confirmed_decisions_count
candidate_memory_count
active_memory_count
recent_audit_events_count
recent_runtime_events_count optional
last_activity_at optional
```

MVP rule:

```text
Dashboard response should remain small and count-based until real dashboard product requirements are defined.
```

---

# 9. MemoryRepository

Required methods:

```text
create(db, data)
findByIdAndWorkspace(db, memoryEntryId, workspaceId)
listByWorkspace(db, workspaceId, filters, pagination)
updateByIdAndWorkspace(db, memoryEntryId, workspaceId, patch)
archiveByIdAndWorkspace(db, memoryEntryId, workspaceId, archiveData)
countByWorkspaceAndStatus(db, workspaceId, status)
```

Rules:

```text
all memory reads/writes must include workspace_id
list methods must be paginated
repository must support transaction client
repository returns records, not DTOs
```

---

# 10. Dashboard Read Strategy

DashboardService should use repositories or direct read adapters for count queries.

MVP count sources:

```text
TaskRepository.countByWorkspaceAndStatus
DecisionRepository.countByWorkspaceAndStatus
MemoryRepository.countByWorkspaceAndStatus
AuditEventRepository.countRecentByWorkspace
RuntimeEventRepository.countRecentByWorkspace later
```

Rule:

```text
DashboardService must not return cross-workspace data under any condition.
```

---

# 11. MemoryService

Required methods:

```text
createMemoryEntry(context, workspaceId, input)
listMemoryEntries(context, workspaceId, query)
getMemoryEntry(context, workspaceId, memoryEntryId)
```

Responsibilities:

```text
attach workspace_id to context
require workspace owner
require active workspace for mutation
validate input
validate task_id belongs to workspace when provided
validate decision_id belongs to workspace when provided
validate source object reference when provided
create candidate memory entry
record memory.created audit event
return MemoryEntryResponseDto
```

---

# 12. MemoryActivationService

Required method:

```text
activateMemoryEntry(context, workspaceId, memoryEntryId, input)
```

Canonical flow:

```text
require workspace owner
require active workspace
load memory entry by id and workspace_id
validate activation allowed
begin transaction
update memory status to active
set confirmed_by from actor_id
set confirmed_at
record memory.activated audit event with before/after state
emit memory.activated runtime event later
return MemoryEntryResponseDto
```

Rule:

```text
Only candidate memory entries can be activated.
```

---

# 13. DashboardService

Required method:

```text
getDashboardSummary(context, workspaceId)
```

Canonical flow:

```text
require workspace owner
load workspace-scoped counts
compute last_activity_at if practical
return DashboardSummaryResponseDto
```

MVP rule:

```text
Dashboard should not persist derived metrics yet; live counts are acceptable for MVP.
```

---

# 14. Lifecycle Rules

Memory transitions:

```text
candidate → active
candidate → archived later
active → archived later
```

Forbidden MVP transitions:

```text
active → candidate
archived → active
active → active
```

Rule:

```text
Memory activation must reject active or archived entries.
```

---

# 15. Authorization Integration

Both modules must use:

```text
AuthorizationService.requireWorkspaceOwner(context)
AuthorizationService.requireWorkspaceMutationAllowed(context)
```

Rules:

```text
memory mutation routes require active workspace
dashboard reads require workspace owner
dashboard does not mutate state in MVP
```

---

# 16. Validation Integration

Memory operations use:

```text
ValidationService
ObjectReferenceValidator.requireTaskInWorkspace
ObjectReferenceValidator.requireDecisionInWorkspace
ObjectReferenceValidator.requireSourceObjectInWorkspace
StatusTransitionValidator.requireMemoryActivationAllowed
BusinessRuleValidator
```

Dashboard operations use:

```text
ValidationService.requireUuid
AuthorizationService.requireWorkspaceOwner
```

Rule:

```text
Memory linked to a task or decision must reference objects in the same workspace.
```

---

# 17. Audit Integration

Required audit events:

```text
memory.created
memory.activated
```

Audit object type:

```text
memory_entry
```

Rules:

```text
audit writes happen inside transaction
before/after state must be sanitized
audit event must include actor context and correlation_id
mutation fails if required audit write fails
```

---

# 18. Runtime Event Readiness

Runtime event emission may be wired after runtime event module execution.

Required future runtime events:

```text
memory.created
memory.activated
dashboard.refresh_requested
```

Dashboard refresh events should be emitted later after:

```text
task.completed
decision.confirmed
memory.activated
```

---

# 19. Error Handling

Required errors:

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

Examples:

```text
missing title → validation_error
missing content → validation_error
cross-workspace task_id → invalid_object_reference
cross-workspace decision_id → invalid_object_reference
active memory activation → invalid_status_transition
non-owner dashboard read → forbidden or safe not_found
```

---

# 20. Mapper Rules

`MemoryEntryMapper.toDto(record)` maps persistence shape to API shape.

Dashboard mapping should be explicit:

```text
raw counts → DashboardSummaryResponseDto
```

Rules:

```text
repositories return records/counts
services return DTOs
DTOs must not expose internal secrets
metadata must be sanitized before audit/event usage
```

---

# 21. Tests Required

Memory repository tests:

```text
create memory entry
find by id and workspace
return null for cross-workspace lookup
list by workspace
filter by status
filter by memory_type
paginate results
update by id and workspace
count by workspace and status
```

Memory service/API tests:

```text
create memory succeeds
create memory records audit event
create memory rejects missing title
create memory rejects missing content
create memory rejects cross-workspace task_id
create memory rejects cross-workspace decision_id
activate memory succeeds
activate memory records audit event
activate memory rejects already active memory
non-owner cannot access memory
```

Dashboard tests:

```text
dashboard returns task counts
dashboard returns decision counts
dashboard returns memory counts
dashboard returns recent audit count
dashboard is workspace-scoped
dashboard excludes archived records where applicable
non-owner cannot read dashboard
```

---

# 22. Execution Order

Recommended execution order:

```text
1. Create MemoryModule folders
2. Create memory DTOs and mapper
3. Create MemoryRepository
4. Create MemoryService
5. Create MemoryActivationService
6. Create MemoryController
7. Add memory tests
8. Create DashboardModule folders
9. Create DashboardSummaryResponseDto
10. Create DashboardService
11. Create DashboardController
12. Add dashboard tests
13. Wire modules into AppModule
14. Verify vertical flow with workspace + task + decision + memory + audit + dashboard
15. Verify typecheck/test/build
```

---

# 23. Verification Commands

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
GET /api/v1/me
POST /api/v1/workspaces
POST /api/v1/workspaces/{workspace_id}/tasks
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/complete
POST /api/v1/workspaces/{workspace_id}/decisions
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm
POST /api/v1/workspaces/{workspace_id}/memory-entries
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/activate
GET /api/v1/workspaces/{workspace_id}/dashboard
GET /api/v1/workspaces/{workspace_id}/audit-events
```

Expected result:

```text
dashboard reflects task, decision and memory state; audit events include memory.created and memory.activated
```

---

# 24. Risks and Controls

## Risk 1 — Memory Becomes Semantic Search Too Early

Mitigation:

```text
Keep MVP memory as structured records only; defer embeddings and vector search.
```

## Risk 2 — Dashboard Becomes Product UI Too Early

Mitigation:

```text
Keep dashboard backend as count-based summary API.
```

## Risk 3 — Cross-Workspace Memory References

Mitigation:

```text
Validate task_id, decision_id and source references with ObjectReferenceValidator.
```

## Risk 4 — Dashboard Leaks Data

Mitigation:

```text
All dashboard queries must be workspace-scoped and authorization checked.
```

---

# 25. Acceptance Criteria

Memory Dashboard Execution is accepted when:

- target directory structure is defined;
- execution non-scope is documented;
- required API routes are defined;
- data models and dashboard read sources are documented;
- memory and dashboard DTOs are defined;
- MemoryRepository is defined;
- Dashboard read strategy is defined;
- MemoryService and MemoryActivationService are defined;
- DashboardService is defined;
- lifecycle rules are documented;
- authorization and validation integration is documented;
- audit integration is documented;
- runtime event readiness is documented;
- error handling is defined;
- mapper rules are defined;
- tests are specified;
- execution order and verification commands are documented;
- risks and controls are documented.

Status:

```text
Accepted for Test Suite Execution
```

---

# 26. Final Statement

```text
Bizzi Memory Dashboard Execution defines the MVP knowledge and visibility layer: reusable memory entries, memory activation and workspace dashboard summary.
```

This prepares Bizzi for full MVP test suite execution and CI workflow validation.