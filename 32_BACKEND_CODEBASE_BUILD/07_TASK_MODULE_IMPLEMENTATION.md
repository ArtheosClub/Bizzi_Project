# 07_TASK_MODULE_IMPLEMENTATION.md

# Bizzi Platform

## Task Module Implementation

**Layer:** 32_BACKEND_CODEBASE_BUILD

### Purpose

Define the concrete implementation of the Task module, responsible for managing the lifecycle of executable work items within a workspace.

### Module Scope

The Task module provides creation, retrieval, lifecycle transitions and audit-aware execution of tasks.

### Directory Structure

```text
backend/src/modules/task/
 ├── task.module.ts
 ├── task.controller.ts
 ├── task.service.ts
 ├── task-lifecycle.service.ts
 ├── task.repository.ts
 ├── dto/
 ├── mappers/
 └── policies/
```

### API Routes

```text
POST /api/v1/workspaces/{workspace_id}/tasks
GET /api/v1/workspaces/{workspace_id}/tasks
GET /api/v1/workspaces/{workspace_id}/tasks/{task_id}
PATCH /api/v1/workspaces/{workspace_id}/tasks/{task_id}
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/complete
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/archive
```

### Responsibilities

- Create workspace-scoped tasks.
- Retrieve and list tasks.
- Update task metadata.
- Execute lifecycle transitions.
- Emit audit events for meaningful mutations.
- Enforce authorization and validation.

### Lifecycle

```text
draft → open → in_progress → completed → archived
```

Only valid transitions are permitted.

### Repository Methods

```text
createTask()
findByIdAndWorkspace()
listByWorkspace()
updateTask()
changeStatus()
archiveTask()
```

### Acceptance Criteria

- Tasks are workspace-scoped.
- Lifecycle transitions are validated.
- Audit events are created transactionally.
- Cross-workspace access is rejected.
- Unit, integration and e2e tests cover lifecycle behavior.

### Outcome

The Task module becomes the primary execution engine for operational work inside Bizzi workspaces.