# 08_CREATE_TASK_SOURCE.md

# Bizzi Platform

## Create Task Source

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Implementation Plan  
**Previous Layer Reference:** 32_BACKEND_CODEBASE_BUILD  
**Product:** Bizzi Platform  
**Status:** Draft v0.1

---

# 1. Purpose

This document defines the concrete source-code creation plan for the Task module in the Bizzi backend.

The goal is to materialize the Task implementation described in:

```text
32_BACKEND_CODEBASE_BUILD/07_TASK_MODULE_IMPLEMENTATION.md
```

into real backend source files under:

```text
backend/src/modules/task/
```

---

# 2. Source Files To Create

Target files:

```text
backend/src/modules/task/task.module.ts
backend/src/modules/task/task.controller.ts
backend/src/modules/task/task.service.ts
backend/src/modules/task/task-lifecycle.service.ts
backend/src/modules/task/task.repository.ts
backend/src/modules/task/dto/create-task.dto.ts
backend/src/modules/task/dto/update-task.dto.ts
backend/src/modules/task/dto/complete-task.dto.ts
backend/src/modules/task/dto/task-query.dto.ts
backend/src/modules/task/dto/task-response.dto.ts
backend/src/modules/task/mappers/task.mapper.ts
backend/src/modules/task/policies/task-status.policy.ts
backend/src/modules/task/__tests__/task.service.spec.ts
backend/src/modules/task/__tests__/task-lifecycle.service.spec.ts
backend/src/modules/task/__tests__/task.repository.spec.ts
backend/test/e2e/task.e2e-spec.ts
```

---

# 3. Module Responsibilities

The Task source code must implement:

```text
workspace-scoped task creation
workspace-scoped task listing
workspace-scoped task detail retrieval
task metadata update
task completion lifecycle transition
task archive lifecycle transition
authorization checks
validation checks
audit event emission
canonical error handling
DTO mapping
tests
```

---

# 4. API Routes

The controller must expose:

```text
POST /api/v1/workspaces/:workspace_id/tasks
GET /api/v1/workspaces/:workspace_id/tasks
GET /api/v1/workspaces/:workspace_id/tasks/:task_id
PATCH /api/v1/workspaces/:workspace_id/tasks/:task_id
POST /api/v1/workspaces/:workspace_id/tasks/:task_id/complete
POST /api/v1/workspaces/:workspace_id/tasks/:task_id/archive
```

---

# 5. TaskModule

`task.module.ts` must import required infrastructure and provide:

```text
TaskController
TaskService
TaskLifecycleService
TaskRepository
TaskMapper
TaskStatusPolicy
```

Required dependencies:

```text
AuthorizationModule
ValidationModule
AuditModule
PrismaModule / DatabaseModule
SharedModule
```

---

# 6. TaskRepository

`task.repository.ts` must contain persistence-only methods.

Required methods:

```text
createTask(db, data)
findByIdAndWorkspace(db, taskId, workspaceId)
listByWorkspace(db, workspaceId, query)
countByWorkspace(db, workspaceId, query)
updateTask(db, taskId, workspaceId, data)
changeStatus(db, taskId, workspaceId, data)
archiveTask(db, taskId, workspaceId, data)
```

Rules:

```text
repository methods must always include workspace_id for workspace-scoped records
repository must not perform authorization logic
repository must not return DTOs
repository must support transaction client
```

---

# 7. TaskService

`task.service.ts` must implement standard task behavior:

```text
createTask(context, workspaceId, dto)
listTasks(context, workspaceId, query)
getTask(context, workspaceId, taskId)
updateTask(context, workspaceId, taskId, dto)
```

Required behavior:

```text
attach workspace_id to service context
require workspace owner
require active workspace for mutations
validate DTO inputs
call repository with workspace_id
map records to TaskResponseDto
record audit events for create/update
```

---

# 8. TaskLifecycleService

`task-lifecycle.service.ts` must implement lifecycle transitions:

```text
completeTask(context, workspaceId, taskId, dto)
archiveTask(context, workspaceId, taskId)
```

Completion flow:

```text
require workspace owner
require active workspace
load task by task_id and workspace_id
validate completion transition
open transaction
update task status to completed
set completed_at
record task.completed audit event with before/after state
return TaskResponseDto
```

Archive flow:

```text
require workspace owner
require active workspace
load task by task_id and workspace_id
validate archive transition
open transaction
update task status to archived
set archived_at
record task.archived audit event
return TaskResponseDto
```

---

# 9. DTOs

Required DTOs:

```text
CreateTaskDto
UpdateTaskDto
CompleteTaskDto
TaskQueryDto
TaskResponseDto
```

`CreateTaskDto` fields:

```text
title required
description optional
priority optional
due_date optional
source_object_type optional
source_object_id optional
metadata optional
```

`TaskResponseDto` fields:

```text
id
workspace_id
owner_user_id
title
description
status
priority
due_date
completed_at
source_object_type
source_object_id
metadata
created_at
updated_at
archived_at
```

---

# 10. TaskStatusPolicy

Allowed lifecycle transitions:

```text
draft → open
open → in_progress
open → completed
in_progress → completed
open → archived
in_progress → archived
completed → archived
```

Forbidden transitions:

```text
completed → open
archived → open
archived → completed
completed → completed
```

---

# 11. Audit Events

The Task source code must emit:

```text
task.created
task.updated
task.completed
task.archived
```

Audit rules:

```text
audit event must include workspace_id
audit event must include actor context
audit event must include correlation_id
audit event must include object_type = task
audit event must include object_id = task.id
mutation and audit write must be transactional
```

---

# 12. Error Handling

Required canonical errors:

```text
unauthenticated
forbidden
not_found
workspace_archived
validation_error
invalid_status_transition
business_rule_violation
internal_error
```

Rules:

```text
missing title returns validation_error
missing task returns not_found
cross-workspace task access returns not_found or forbidden-safe not_found
completed task cannot be completed again
archived task cannot be mutated
```

---

# 13. Tests

Required unit tests:

```text
TaskStatusPolicy validates allowed transitions
TaskStatusPolicy rejects invalid transitions
TaskMapper maps persistence record to DTO
```

Required service tests:

```text
createTask creates task
createTask records audit event
createTask rejects missing title
listTasks is workspace-scoped
getTask rejects cross-workspace access
completeTask changes status to completed
completeTask records task.completed audit event
completeTask rejects completed task
archiveTask records task.archived audit event
```

Required e2e tests:

```text
POST /tasks creates task
GET /tasks lists workspace tasks
GET /tasks/:task_id returns detail
PATCH /tasks/:task_id updates task
POST /tasks/:task_id/complete completes task
POST /tasks/:task_id/archive archives task
non-owner cannot access task
```

---

# 14. Execution Order

Recommended order:

```text
1. Create task module folder
2. Create DTOs
3. Create TaskStatusPolicy
4. Create TaskMapper
5. Create TaskRepository
6. Create TaskService
7. Create TaskLifecycleService
8. Create TaskController
9. Register TaskModule in AppModule
10. Add unit tests
11. Add service/repository tests
12. Add e2e tests
13. Run typecheck/test/build
```

---

# 15. Acceptance Criteria

Task source implementation is accepted when:

- all task source files are created;
- task routes are implemented;
- workspace scoping is enforced;
- authorization is enforced;
- lifecycle transitions are validated;
- audit events are emitted transactionally;
- DTOs and mapper are implemented;
- repository methods use workspace_id;
- tests are implemented;
- typecheck, tests and build pass.

---

# 16. Final Statement

```text
Task Source implementation creates the first executable operational work module for the Bizzi backend.
```

This module must preserve the core Bizzi guarantees: workspace isolation, service-level authorization, lifecycle validation, transactional audit evidence and canonical API behavior.