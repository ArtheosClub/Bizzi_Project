# 11_DASHBOARD_MODULE_IMPLEMENTATION.md

# Bizzi Platform

## Dashboard Module Implementation

**Layer:** 32_BACKEND_CODEBASE_BUILD

### Purpose

Define the concrete implementation of the Dashboard module, responsible for aggregating workspace metrics into a single operational view.

### Module Scope

The Dashboard module exposes read-only endpoints that summarize tasks, decisions, memory, audit activity and overall workspace health.

### Directory Structure

```text
backend/src/modules/dashboard/
 ├── dashboard.module.ts
 ├── dashboard.controller.ts
 ├── dashboard.service.ts
 ├── dashboard.repository.ts
 ├── dto/
 │   ├── dashboard-summary.dto.ts
 │   └── dashboard-query.dto.ts
 └── mappers/
     └── dashboard.mapper.ts
```

### API Routes

```text
GET /api/v1/workspaces/{workspace_id}/dashboard
GET /api/v1/workspaces/{workspace_id}/dashboard/summary
```

### Responsibilities

- Aggregate workspace KPIs.
- Count tasks by lifecycle state.
- Count confirmed decisions.
- Count active memory entries.
- Show recent audit activity.
- Return a single dashboard DTO.

### Data Sources

- Task repository
- Decision repository
- Memory repository
- Audit repository
- Workspace repository

### Dashboard Metrics

```text
workspace status
open tasks
completed tasks
confirmed decisions
active memory entries
recent audit events
last activity timestamp
```

### Security Rules

- Read access requires workspace authorization.
- Dashboard is workspace-scoped.
- Aggregates never expose data from other workspaces.

### Acceptance Criteria

- Dashboard returns consolidated metrics.
- Counts are transactionally consistent.
- Cross-workspace aggregation is impossible.
- Dashboard endpoint is covered by integration and e2e tests.

### Outcome

The Dashboard module provides the operational visibility layer for Bizzi Platform and serves as the primary backend endpoint for future web and AI interfaces.