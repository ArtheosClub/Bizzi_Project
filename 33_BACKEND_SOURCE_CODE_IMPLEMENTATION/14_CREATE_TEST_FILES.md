# 14_CREATE_TEST_FILES.md

# Bizzi Platform

## Create Test Files

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Implementation Plan  
**Previous Layer Reference:** 32_BACKEND_CODEBASE_BUILD  
**Status:** Draft v0.1  
**Product:** Bizzi Platform

---

## 1. Purpose

This document defines the concrete test file creation plan for the Bizzi backend source code implementation layer.

The goal is to create the actual test files required to verify the backend MVP source code, including unit tests, integration tests, e2e tests, test factories, test helpers and the MVP vertical slice test.

---

## 2. Implementation Scope

This step creates the test structure for:

```text
backend/test/
backend/src/**/__tests__/
```

It covers:

```text
shared kernel tests
identity tests
workspace tests
authorization tests
task tests
decision tests
memory tests
audit tests
dashboard tests
API bootstrap tests
MVP vertical slice tests
```

---

## 3. Target Directory Structure

```text
backend/test/
├── setup/
│   ├── test-app.ts
│   ├── test-database.ts
│   ├── test-context.ts
│   └── jest-e2e.setup.ts
├── factories/
│   ├── user.factory.ts
│   ├── workspace.factory.ts
│   ├── task.factory.ts
│   ├── decision.factory.ts
│   ├── memory-entry.factory.ts
│   └── audit-event.factory.ts
├── helpers/
│   ├── auth-test.helper.ts
│   ├── request-test.helper.ts
│   └── assertion-test.helper.ts
└── e2e/
    ├── health.e2e-spec.ts
    ├── identity.e2e-spec.ts
    ├── workspace.e2e-spec.ts
    ├── task.e2e-spec.ts
    ├── decision.e2e-spec.ts
    ├── memory.e2e-spec.ts
    ├── audit.e2e-spec.ts
    ├── dashboard.e2e-spec.ts
    └── mvp-vertical-slice.e2e-spec.ts
```

Module-level tests:

```text
backend/src/shared/**/__tests__/*.spec.ts
backend/src/modules/identity/__tests__/*.spec.ts
backend/src/modules/workspace/__tests__/*.spec.ts
backend/src/modules/authorization/__tests__/*.spec.ts
backend/src/modules/task/__tests__/*.spec.ts
backend/src/modules/decision/__tests__/*.spec.ts
backend/src/modules/memory/__tests__/*.spec.ts
backend/src/modules/audit/__tests__/*.spec.ts
backend/src/modules/dashboard/__tests__/*.spec.ts
```

---

## 4. Test Setup Files

Required setup files:

```text
backend/test/setup/test-app.ts
backend/test/setup/test-database.ts
backend/test/setup/test-context.ts
backend/test/setup/jest-e2e.setup.ts
```

Responsibilities:

```text
create NestJS test application
connect to test database
reset database between suites
create test actor context
create test workspace context
configure global validation and filters
```

---

## 5. Test Factories

Factories must create deterministic records for:

```text
User
CompanyWorkspace
WorkspaceSettings
Task
Decision
MemoryEntry
AuditEvent
```

Rules:

```text
factories must not use production data
factories must generate unique emails and names
factories must support workspace-scoped records
factories must support cross-workspace isolation scenarios
```

---

## 6. Unit Test Files

Create unit tests for:

```text
shared errors
pagination helpers
request context helpers
workspace status policy
task status policy
decision status policy
memory status policy
DTO mappers
payload sanitizer
```

Expected examples:

```text
backend/src/shared/errors/__tests__/service-error.spec.ts
backend/src/shared/pagination/__tests__/pagination.util.spec.ts
backend/src/modules/task/__tests__/task-status.policy.spec.ts
backend/src/modules/decision/__tests__/decision-status.policy.spec.ts
backend/src/modules/memory/__tests__/memory-status.policy.spec.ts
```

---

## 7. Repository Test Files

Create repository tests for:

```text
UserRepository
WorkspaceRepository
TaskRepository
DecisionRepository
MemoryRepository
AuditRepository
DashboardRepository if used
```

Repository tests must verify:

```text
create
find by id
find by id and workspace
list by workspace
pagination
cross-workspace rejection
status filters
```

---

## 8. Service Test Files

Create service tests for:

```text
IdentityService
WorkspaceService
AuthorizationService
TaskService
DecisionService
MemoryService
AuditService
DashboardService
```

Service tests must verify:

```text
authorization enforcement
validation enforcement
transactional audit emission
canonical error behavior
DTO mapping
workspace isolation
```

---

## 9. E2E Test Files

Create e2e tests for the MVP API routes:

```text
GET /health
GET /api/v1/me
POST /api/v1/workspaces
GET /api/v1/workspaces
POST /api/v1/workspaces/:workspace_id/tasks
POST /api/v1/workspaces/:workspace_id/tasks/:task_id/complete
POST /api/v1/workspaces/:workspace_id/decisions
POST /api/v1/workspaces/:workspace_id/decisions/:decision_id/confirm
POST /api/v1/workspaces/:workspace_id/memory-entries
POST /api/v1/workspaces/:workspace_id/memory-entries/:memory_entry_id/activate
GET /api/v1/workspaces/:workspace_id/audit-events
GET /api/v1/workspaces/:workspace_id/dashboard
```

---

## 10. MVP Vertical Slice Test

Create:

```text
backend/test/e2e/mvp-vertical-slice.e2e-spec.ts
```

The test must execute:

```text
1. health check
2. current user read
3. workspace creation
4. task creation
5. task completion
6. decision creation
7. decision confirmation
8. memory entry creation
9. memory activation
10. audit event listing
11. dashboard summary read
```

Acceptance:

```text
all steps return expected status codes
all records are workspace-scoped
audit events exist for mutations
dashboard reflects final state
```

---

## 11. Test Commands

Required package scripts:

```text
pnpm test
pnpm test:unit
pnpm test:integration
pnpm test:e2e
pnpm test:watch
pnpm db:test:reset
```

---

## 12. Acceptance Criteria

This implementation step is complete when:

- test setup files are created;
- factories are created;
- helpers are created;
- unit tests are created;
- repository tests are created;
- service tests are created;
- e2e tests are created;
- MVP vertical slice test is created;
- test commands are defined;
- tests are ready for CI execution.

---

## 13. Final Statement

```text
33_BACKEND_SOURCE_CODE_IMPLEMENTATION/14_CREATE_TEST_FILES.md defines the concrete source-level test creation plan for Bizzi backend MVP.
```

This step prepares the backend codebase for reliable validation, CI execution and future automated code generation.