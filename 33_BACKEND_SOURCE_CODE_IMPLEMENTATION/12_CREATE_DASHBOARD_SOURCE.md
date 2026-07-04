# 12_CREATE_DASHBOARD_SOURCE.md

# Bizzi Platform

## Create Dashboard Source

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Implementation Plan  
**Previous Layer:** 32_BACKEND_CODEBASE_BUILD  
**Source Target:** backend/src/modules/dashboard  
**Status:** Draft v0.1  
**Product:** Bizzi Platform

---

# 1. Purpose

This document defines the source-code implementation task for the Bizzi Dashboard module.

The goal is to create the actual backend source files that expose a workspace-scoped dashboard summary endpoint using the already defined Workspace, Task, Decision, Memory, Audit and Authorization foundations.

Core question:

```text
Which concrete source files must be created so Bizzi can return a safe workspace dashboard summary from the backend API?
```

---

# 2. Target Source Directory

Create the following directory:

```text
backend/src/modules/dashboard/
```

Target files:

```text
backend/src/modules/dashboard/dashboard.module.ts
backend/src/modules/dashboard/dashboard.controller.ts
backend/src/modules/dashboard/dashboard.service.ts
backend/src/modules/dashboard/dashboard.repository.ts
backend/src/modules/dashboard/dto/dashboard-summary.dto.ts
backend/src/modules/dashboard/dto/dashboard-query.dto.ts
backend/src/modules/dashboard/mappers/dashboard.mapper.ts
backend/src/modules/dashboard/__tests__/dashboard.service.spec.ts
backend/src/modules/dashboard/__tests__/dashboard.e2e-spec.ts
```

---

# 3. Dashboard Module

File:

```text
backend/src/modules/dashboard/dashboard.module.ts
```

Responsibilities:

```text
register DashboardController
register DashboardService
register DashboardRepository
import AuthorizationModule
import TaskModule or repository providers
import DecisionModule or repository providers
import MemoryModule or repository providers
import AuditModule or repository providers
```

Expected shape:

```typescript
@Module({
  imports: [AuthorizationModule],
  controllers: [DashboardController],
  providers: [DashboardService, DashboardRepository],
  exports: [DashboardService],
})
export class DashboardModule {}
```

---

# 4. Dashboard Controller

File:

```text
backend/src/modules/dashboard/dashboard.controller.ts
```

Route:

```text
GET /api/v1/workspaces/:workspaceId/dashboard
```

Responsibilities:

```text
receive workspaceId from route path
receive request/service context
call DashboardService.getDashboardSummary
return DashboardSummaryDto
```

Rules:

```text
controller must not perform direct database queries
controller must not implement authorization logic manually
workspace_id must come from route path, not request body
```

---

# 5. Dashboard Service

File:

```text
backend/src/modules/dashboard/dashboard.service.ts
```

Required method:

```typescript
getDashboardSummary(context: ServiceContext, workspaceId: string): Promise<DashboardSummaryDto>
```

Responsibilities:

```text
validate authenticated context
require workspace owner/read permission
request dashboard aggregate counts from repository
map aggregate data to DashboardSummaryDto
return safe workspace-scoped summary
```

Service flow:

```text
getDashboardSummary
↓
AuthorizationService.requireWorkspaceRead(context, workspaceId)
↓
DashboardRepository.getSummary(workspaceId)
↓
DashboardMapper.toSummaryDto(data)
↓
return dto
```

---

# 6. Dashboard Repository

File:

```text
backend/src/modules/dashboard/dashboard.repository.ts
```

Required method:

```typescript
getSummary(workspaceId: string): Promise<DashboardSummaryAggregate>
```

Repository responsibilities:

```text
count open tasks
count completed tasks
count draft decisions
count confirmed decisions
count candidate memory entries
count active memory entries
count recent audit events
calculate last_activity_at when possible
```

Repository rules:

```text
all queries must filter by workspace_id
repository returns aggregate records, not API DTOs
no cross-workspace joins without workspace filter
no authorization logic inside repository
```

---

# 7. Dashboard Summary DTO

File:

```text
backend/src/modules/dashboard/dto/dashboard-summary.dto.ts
```

Required fields:

```text
workspace_id
open_tasks_count
completed_tasks_count
draft_decisions_count
confirmed_decisions_count
candidate_memory_count
active_memory_count
recent_audit_events_count
last_activity_at
```

Recommended TypeScript shape:

```typescript
export class DashboardSummaryDto {
  workspace_id!: string;
  open_tasks_count!: number;
  completed_tasks_count!: number;
  draft_decisions_count!: number;
  confirmed_decisions_count!: number;
  candidate_memory_count!: number;
  active_memory_count!: number;
  recent_audit_events_count!: number;
  last_activity_at?: string | null;
}
```

---

# 8. Dashboard Query DTO

File:

```text
backend/src/modules/dashboard/dto/dashboard-query.dto.ts
```

MVP query fields:

```text
recent_window_days optional
```

Default:

```text
recent_window_days = 7
```

Rules:

```text
query values must be validated
large lookback windows should be capped
MVP dashboard can work without query parameters
```

---

# 9. Dashboard Mapper

File:

```text
backend/src/modules/dashboard/mappers/dashboard.mapper.ts
```

Required method:

```typescript
static toSummaryDto(aggregate: DashboardSummaryAggregate): DashboardSummaryDto
```

Mapper rules:

```text
convert internal camelCase values to API snake_case values
ensure missing counts default to 0
convert Date values to ISO strings
never expose internal database objects directly
```

---

# 10. Authorization Requirements

Dashboard reads must call:

```text
AuthorizationService.requireWorkspaceRead(context, workspaceId)
```

MVP behavior:

```text
workspace owner can read dashboard
non-owner cannot read dashboard
missing actor returns unauthenticated
missing workspace returns not_found
```

Rule:

```text
Dashboard must be read-only but still authorization-protected.
```

---

# 11. Data Sources

Dashboard source queries depend on:

```text
Task
Decision
MemoryEntry
AuditEvent
CompanyWorkspace
```

MVP count mapping:

```text
Task.status = open / in_progress / completed
Decision.status = draft / confirmed
MemoryEntry.status = candidate / active
AuditEvent.timestamp >= recent window
```

Rules:

```text
archived records should be excluded from active operational counts unless explicitly counted later
audit events are counted as recent activity
last_activity_at may be max updated_at/timestamp across supported models
```

---

# 12. Error Handling

Dashboard must use canonical errors:

```text
unauthenticated
forbidden
not_found
validation_error
internal_error
```

Rules:

```text
raw database errors must not leak
invalid workspaceId returns validation_error or not_found according to shared validation policy
unknown failures map to internal_error
```

---

# 13. Tests Required

Unit tests:

```text
DashboardMapper maps aggregate to DTO
missing aggregate counts default to zero
last_activity_at converts to ISO string
```

Service tests:

```text
getDashboardSummary requires workspace read authorization
getDashboardSummary calls repository with workspaceId
getDashboardSummary returns DashboardSummaryDto
non-owner access is rejected
```

Repository tests:

```text
counts open tasks by workspace
counts completed tasks by workspace
counts confirmed decisions by workspace
counts active memory entries by workspace
counts recent audit events by workspace
excludes data from other workspaces
```

E2E tests:

```text
GET /api/v1/workspaces/:workspaceId/dashboard returns summary
non-owner cannot read dashboard
summary updates after task completion
dashboard does not leak cross-workspace data
```

---

# 14. Acceptance Criteria

Dashboard source creation is accepted when:

- dashboard module file exists;
- dashboard controller exists;
- dashboard service exists;
- dashboard repository exists;
- dashboard DTOs exist;
- dashboard mapper exists;
- route `GET /api/v1/workspaces/:workspaceId/dashboard` is implemented;
- authorization is enforced through AuthorizationService;
- all repository queries are workspace-scoped;
- dashboard summary returns task, decision, memory and audit counts;
- tests are defined for service, repository and e2e behavior.

---

# 15. Final Statement

```text
Dashboard source implementation creates the operational visibility endpoint for Bizzi backend MVP.
```

This module gives the product a single workspace-scoped summary API that can later power the web dashboard, AI orchestrator status view and management reporting.