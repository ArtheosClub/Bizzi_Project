# 08_TASK_DECISION_EXECUTION.md

# Bizzi Platform

## Task Decision Execution

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
**Previous Document:** 07_AUDIT_EVENT_EXECUTION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch III — Backend Execution

---

# 1. Purpose

This document defines the Task and Decision execution plan for Bizzi Platform backend MVP.

It specifies how to implement the first business execution modules after workspace, authorization, validation and audit foundations are in place: task creation, task completion, decision creation, decision confirmation, lifecycle policies, repositories, services, routes, DTOs, audit integration and runtime-event readiness.

Core question:

```text
How should Bizzi implement tasks and decisions so the platform can execute work, confirm business decisions and preserve auditable evidence inside a workspace?
```

---

# 2. Task Decision Thesis

```text
Task and Decision modules form the first executable business loop of Bizzi: tasks represent actionable work, while decisions represent confirmed business intent and evidence.
```

This execution must prove:

```text
workspace-scoped business objects
owner-authorized operations
validated lifecycle transitions
transactional mutations
audit evidence for every meaningful mutation
runtime event readiness
canonical errors
repository isolation
API route behavior
testable MVP business flow
```

---

# 3. Target Directory Structure

Target structure:

```text
backend/src/modules/task/
├── task.module.ts
├── controllers/
│   └── task.controller.ts
├── services/
│   ├── task.service.ts
│   └── task-lifecycle.service.ts
├── repositories/
│   └── task.repository.ts
├── dto/
│   ├── create-task.dto.ts
│   ├── complete-task.dto.ts
│   ├── task.response.dto.ts
│   └── task-query.dto.ts
├── mappers/
│   └── task.mapper.ts
└── tests/
    ├── task.service.spec.ts
    ├── task.repository.spec.ts
    └── task.e2e-spec.ts

backend/src/modules/decision/
├── decision.module.ts
├── controllers/
│   └── decision.controller.ts
├── services/
│   ├── decision.service.ts
│   └── decision-confirmation.service.ts
├── repositories/
│   └── decision.repository.ts
├── dto/
│   ├── create-decision.dto.ts
│   ├── confirm-decision.dto.ts
│   ├── decision.response.dto.ts
│   └── decision-query.dto.ts
├── mappers/
│   └── decision.mapper.ts
└── tests/
    ├── decision.service.spec.ts
    ├── decision.repository.spec.ts
    └── decision.e2e-spec.ts
```

---

# 4. Execution Non-Scope

This step does not implement:

```text
advanced task assignment
comments
attachments
recurring tasks
Kanban views
approval workflows
multi-person decision voting
legal signing
AI autonomous task completion
agent authority
dashboard aggregation beyond events/count readiness
```

These are later expansion layers.

---

# 5. Required API Routes

Task MVP routes:

```text
POST /api/v1/workspaces/{workspace_id}/tasks
GET /api/v1/workspaces/{workspace_id}/tasks
GET /api/v1/workspaces/{workspace_id}/tasks/{task_id}
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/complete
```

Decision MVP routes:

```text
POST /api/v1/workspaces/{workspace_id}/decisions
GET /api/v1/workspaces/{workspace_id}/decisions
GET /api/v1/workspaces/{workspace_id}/decisions/{decision_id}
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm
```

Rule:

```text
workspace_id must come from path and ServiceContext, never from request body.
```

---

# 6. Data Models Used

Primary models:

```text
Task
Decision
AuditEvent
RuntimeEvent later
CompanyWorkspace
User
```

Relations:

```text
Task.workspace_id → CompanyWorkspace.id
Decision.workspace_id → CompanyWorkspace.id
Decision.task_id → Task.id optional
```

Rule:

```text
If a decision references a task, the task must belong to the same workspace.
```

---

# 7. Task DTOs

`CreateTaskDto` should include:

```text
title required
description optional
priority optional
due_date optional
owner_user_id optional later
source_object_type optional
source_object_id optional
metadata optional
```

`CompleteTaskDto` may include:

```text
completion_note optional
metadata optional
```

`TaskResponseDto` should include:

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

# 8. Decision DTOs

`CreateDecisionDto` should include:

```text
title required
description optional
decision_type optional
task_id optional
decision_date optional
source_object_type optional
source_object_id optional
metadata optional
```

`ConfirmDecisionDto` may include:

```text
confirmation_note optional
metadata optional
```

`DecisionResponseDto` should include:

```text
id
workspace_id
task_id
owner_user_id
title
description
decision_type
status
decision_date
confirmed_by
confirmed_at
source_object_type
source_object_id
metadata
created_at
updated_at
archived_at
```

---

# 9. TaskRepository

Required methods:

```text
create(db, data)
findByIdAndWorkspace(db, taskId, workspaceId)
listByWorkspace(db, workspaceId, filters, pagination)
updateByIdAndWorkspace(db, taskId, workspaceId, patch)
archiveByIdAndWorkspace(db, taskId, workspaceId, archiveData)
```

Rules:

```text
all task reads/writes must include workspace_id
list methods must be paginated
repository returns records, not DTOs
repository must support transaction client
```

---

# 10. DecisionRepository

Required methods:

```text
create(db, data)
findByIdAndWorkspace(db, decisionId, workspaceId)
listByWorkspace(db, workspaceId, filters, pagination)
updateByIdAndWorkspace(db, decisionId, workspaceId, patch)
archiveByIdAndWorkspace(db, decisionId, workspaceId, archiveData)
```

Rules:

```text
all decision reads/writes must include workspace_id
decision.task_id must be validated by service before persistence
repository returns records, not DTOs
repository must support transaction client
```

---

# 11. TaskService

Required methods:

```text
createTask(context, workspaceId, input)
listTasks(context, workspaceId, query)
getTask(context, workspaceId, taskId)
```

Responsibilities:

```text
attach workspace_id to context
require workspace owner
require active workspace for mutation
validate input
validate source object reference when provided
create task in transaction
record task.created audit event
return TaskResponseDto
```

---

# 12. TaskLifecycleService

Required method:

```text
completeTask(context, workspaceId, taskId, input)
```

Canonical flow:

```text
require workspace owner
require active workspace
load task by id and workspace_id
validate completion allowed
begin transaction
update task status to completed
set completed_at
record task.completed audit event with before/after state
emit task.completed runtime event later
return TaskResponseDto
```

Rule:

```text
Completed or archived tasks must not be completed again.
```

---

# 13. DecisionService

Required methods:

```text
createDecision(context, workspaceId, input)
listDecisions(context, workspaceId, query)
getDecision(context, workspaceId, decisionId)
```

Responsibilities:

```text
attach workspace_id to context
require workspace owner
require active workspace for mutation
validate input
validate task_id belongs to workspace when provided
validate source object reference when provided
create decision in draft status
record decision.created audit event
return DecisionResponseDto
```

---

# 14. DecisionConfirmationService

Required method:

```text
confirmDecision(context, workspaceId, decisionId, input)
```

Canonical flow:

```text
require workspace owner
require active workspace
load decision by id and workspace_id
validate confirmation allowed
begin transaction
update decision status to confirmed
set confirmed_by from actor_id
set confirmed_at
record decision.confirmed audit event with before/after state
emit decision.confirmed runtime event later
return DecisionResponseDto
```

Rule:

```text
Confirmed or archived decisions must not be confirmed again.
```

---

# 15. Lifecycle Rules

Task transitions:

```text
open → completed
in_progress → completed
completed → archived later
open/in_progress → archived later
```

Decision transitions:

```text
draft → confirmed
draft → archived later
confirmed → archived later
```

MVP forbidden transitions:

```text
completed → open
archived → completed
confirmed → draft
archived → confirmed
```

---

# 16. Authorization Integration

Both modules must use:

```text
AuthorizationService.requireWorkspaceOwner(context)
AuthorizationService.requireWorkspaceMutationAllowed(context)
```

Rules:

```text
read routes require workspace owner in MVP
mutation routes require active workspace
controllers are not the only authorization layer
```

---

# 17. Validation Integration

Task operations use:

```text
ValidationService
ObjectReferenceValidator
StatusTransitionValidator
BusinessRuleValidator
```

Decision operations use:

```text
ValidationService
ObjectReferenceValidator.requireTaskInWorkspace for task_id
StatusTransitionValidator.requireDecisionConfirmationAllowed
BusinessRuleValidator
```

Rule:

```text
Cross-workspace references must fail before mutation.
```

---

# 18. Audit Integration

Required audit events:

```text
task.created
task.completed
decision.created
decision.confirmed
```

Audit object types:

```text
task
decision
```

Rules:

```text
audit writes happen inside transaction
before/after state must be sanitized
audit event must include actor context and correlation_id
mutation fails if required audit write fails
```

---

# 19. Runtime Event Readiness

Runtime event emission may be wired after runtime event module execution.

Required future runtime events:

```text
task.created
task.completed
decision.created
decision.confirmed
dashboard.refresh_requested
```

Rule:

```text
Service methods should be structured so runtime event emission can be added without changing public APIs.
```

---

# 20. Error Handling

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
invalid task_id → invalid_object_reference
non-owner workspace access → forbidden or safe not_found
completed task completion → invalid_status_transition
confirmed decision confirmation → invalid_status_transition
```

---

# 21. Mapper Rules

`TaskMapper.toDto(record)` maps persistence shape to API shape.

`DecisionMapper.toDto(record)` maps persistence shape to API shape.

Rules:

```text
repositories return records
services return DTOs
DTOs must not expose internal secrets
metadata must be sanitized before audit/event usage
```

---

# 22. Tests Required

Task repository tests:

```text
create task
find by id and workspace
return null for cross-workspace lookup
list by workspace
filter by status
paginate results
update by id and workspace
```

Task service/API tests:

```text
create task succeeds
create task records audit event
create task rejects missing title
complete task succeeds
complete task records audit event
complete task rejects completed task
non-owner cannot access task
cross-workspace access rejected
```

Decision repository tests:

```text
create decision
find by id and workspace
return null for cross-workspace lookup
list by workspace
filter by status
paginate results
update by id and workspace
```

Decision service/API tests:

```text
create decision succeeds
create decision records audit event
create decision rejects cross-workspace task_id
confirm decision succeeds
confirm decision records audit event
confirm decision rejects confirmed decision
non-owner cannot access decision
```

---

# 23. Execution Order

Recommended execution order:

```text
1. Create TaskModule folders
2. Create Task DTOs and mapper
3. Create TaskRepository
4. Create TaskService
5. Create TaskLifecycleService
6. Create TaskController
7. Add task tests
8. Create DecisionModule folders
9. Create Decision DTOs and mapper
10. Create DecisionRepository
11. Create DecisionService
12. Create DecisionConfirmationService
13. Create DecisionController
14. Add decision tests
15. Wire modules into AppModule
16. Verify vertical flow with workspace + audit
17. Verify typecheck/test/build
```

---

# 24. Verification Commands

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
GET /api/v1/workspaces/{workspace_id}/audit-events
```

Expected result:

```text
task.created, task.completed, decision.created and decision.confirmed audit events exist
```

---

# 25. Risks and Controls

## Risk 1 — Task/Decision Without Workspace Scope

Mitigation:

```text
Require repository methods with workspace_id and cross-workspace tests.
```

## Risk 2 — Lifecycle Rules Scattered

Mitigation:

```text
Use StatusTransitionValidator and lifecycle services.
```

## Risk 3 — Mutations Without Audit Evidence

Mitigation:

```text
Record audit events inside transactions and test event creation.
```

## Risk 4 — Decision References Foreign Workspace Task

Mitigation:

```text
Validate task_id with ObjectReferenceValidator.requireTaskInWorkspace.
```

---

# 26. Acceptance Criteria

Task Decision Execution is accepted when:

- target directory structure is defined;
- execution non-scope is documented;
- required API routes are defined;
- data models and relations are documented;
- task and decision DTOs are defined;
- repositories are defined;
- services and lifecycle services are defined;
- lifecycle rules are documented;
- authorization integration is documented;
- validation integration is documented;
- audit integration is documented;
- runtime event readiness is documented;
- error handling is defined;
- mapper rules are defined;
- tests are specified;
- execution order and verification commands are documented;
- risks and controls are documented.

Status:

```text
Accepted for Memory Dashboard Execution
```

---

# 27. Final Statement

```text
Bizzi Task Decision Execution defines the first real business execution loop for the backend MVP: create work, complete work, create decisions and confirm decisions with workspace scope, authorization, validation and audit evidence.
```

This prepares Bizzi for memory activation, dashboard visibility and runtime event coordination.