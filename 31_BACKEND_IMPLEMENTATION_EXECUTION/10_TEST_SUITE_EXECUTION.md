# 10_TEST_SUITE_EXECUTION.md

# Bizzi Platform

## Test Suite Execution

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
**Previous Document:** 09_MEMORY_DASHBOARD_EXECUTION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch III — Backend Execution

---

# 1. Purpose

This document defines the Test Suite execution plan for Bizzi Platform backend MVP.

It specifies how to implement unit, repository, service, API/e2e, transaction, authorization, validation, audit evidence and dashboard tests for the first backend vertical slice.

Core question:

```text
How should Bizzi prove that backend execution is workspace-scoped, authorized, validated, transactional, auditable and ready for CI?
```

---

# 2. Test Suite Thesis

```text
Bizzi tests are architecture enforcement, not only feature checks.
```

The backend MVP is accepted only when tests prove:

```text
backend boot
schema validity
repository workspace isolation
service-level authorization
service-level validation
transaction rollback behavior
audit event creation
canonical API errors
MVP vertical slice behavior
```

---

# 3. Target Directory Structure

Recommended structure:

```text
backend/test/setup/test-app.ts
backend/test/setup/test-database.ts
backend/test/setup/test-context.ts
backend/test/factories/user.factory.ts
backend/test/factories/workspace.factory.ts
backend/test/factories/task.factory.ts
backend/test/factories/decision.factory.ts
backend/test/factories/memory-entry.factory.ts
backend/test/factories/audit-event.factory.ts
backend/test/e2e/health.e2e-spec.ts
backend/test/e2e/identity.e2e-spec.ts
backend/test/e2e/workspace.e2e-spec.ts
backend/test/e2e/task.e2e-spec.ts
backend/test/e2e/decision.e2e-spec.ts
backend/test/e2e/memory-dashboard.e2e-spec.ts
backend/test/e2e/mvp-vertical-slice.e2e-spec.ts
backend/src/modules/**/tests/*.spec.ts
```

Rule:

```text
Module-local tests cover internal behavior; e2e tests cover API flows.
```

---

# 4. Execution Non-Scope

This step does not implement:

```text
frontend tests
browser automation
mobile tests
load tests
production monitoring tests
formal compliance tests
```

---

# 5. Test Stack

Recommended stack:

```text
Jest
Supertest
NestJS TestingModule
Prisma test database
Docker Compose PostgreSQL test service
Test data factories
```

Required commands:

```text
pnpm test
pnpm test:unit
pnpm test:integration
pnpm test:e2e
pnpm db:test:reset
```

---

# 6. Test Database Strategy

Test database must be separated from development and production data.

Required behavior:

```text
migrations apply before integration/e2e tests
schema can reset deterministically
test data is isolated
test setup fails if environment is not test
```

Recommended reset options:

```text
truncate tables between tests
schema reset before e2e suite
transaction rollback where practical
```

---

# 7. Test Context Strategy

Test helpers should create:

```text
ActorContext
RequestContext
ServiceContext
workspace context
correlation_id
```

Required helpers:

```text
createTestActorContext
createTestServiceContext
createWorkspaceContext
createCorrelationIdForTest
```

---

# 8. Factories

Required factories:

```text
UserFactory
WorkspaceFactory
WorkspaceSettingsFactory
TaskFactory
DecisionFactory
MemoryEntryFactory
AuditEventFactory
RuntimeEventFactory later
```

Rules:

```text
use unique identifiers
support cross-workspace scenarios
avoid hidden global state
use safe placeholder data only
```

---

# 9. Unit Tests

Unit tests cover pure logic:

```text
pagination utilities
error mapper
payload sanitizer
workspace status policy
task status policy
decision status policy
memory status policy
business rule validators
DTO mappers
```

Rule:

```text
Unit tests must not require database access.
```

---

# 10. Repository Tests

Repository tests must cover:

```text
UserRepository
WorkspaceRepository
WorkspaceSettingsRepository
TaskRepository
DecisionRepository
MemoryRepository
AuditEventRepository
RuntimeEventRepository later
```

Every workspace-scoped repository must test:

```text
create record
find by id and workspace
return null for cross-workspace lookup
list by workspace
filter behavior
pagination behavior
update by id and workspace where applicable
archive behavior where applicable
```

---

# 11. Service Tests

Service tests must cover:

```text
IdentityService
WorkspaceService
AuthorizationService
ValidationService
AuditService
TaskService
TaskLifecycleService
DecisionService
DecisionConfirmationService
MemoryService
MemoryActivationService
DashboardService
```

Assertions:

```text
authorization enforced
validation enforced
workspace_id passed into repositories
transactions wrap mutations
audit events are recorded
DTOs are returned
canonical errors are raised
```

---

# 12. API / E2E Tests

Required route tests:

```text
GET /health
GET /api/v1/me
POST /api/v1/workspaces
GET /api/v1/workspaces
GET /api/v1/workspaces/{workspace_id}
POST /api/v1/workspaces/{workspace_id}/tasks
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/complete
POST /api/v1/workspaces/{workspace_id}/decisions
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm
POST /api/v1/workspaces/{workspace_id}/memory-entries
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/activate
GET /api/v1/workspaces/{workspace_id}/audit-events
GET /api/v1/workspaces/{workspace_id}/dashboard
```

API tests must assert:

```text
status code
response shape
canonical errors
workspace isolation
```

---

# 13. Transaction Tests

Required transaction tests:

```text
workspace creation rolls back if settings creation fails
workspace creation rolls back if required audit event fails
task creation rolls back if audit event fails
task completion rolls back if audit event fails
decision confirmation rolls back if audit event fails
memory activation rolls back if audit event fails
```

Rule:

```text
Meaningful state changes must not commit without required audit evidence.
```

---

# 14. Authorization Tests

Required tests:

```text
owner can access own workspace
non-owner cannot access workspace
non-owner cannot access task
non-owner cannot access decision
non-owner cannot access memory entry
non-owner cannot read audit events
non-owner cannot read dashboard
archived workspace blocks mutations
missing actor returns unauthenticated
```

---

# 15. Validation Tests

Required tests:

```text
invalid UUID returns validation_error
missing task title returns validation_error
missing decision title returns validation_error
missing memory title returns validation_error
missing memory content returns validation_error
invalid status transition returns invalid_status_transition
cross-workspace task reference returns invalid_object_reference
cross-workspace decision reference returns invalid_object_reference
page_size maximum is enforced
```

---

# 16. Audit Evidence Tests

Required tests:

```text
workspace.created audit event is recorded
task.created audit event is recorded
task.completed audit event is recorded
decision.created audit event is recorded
decision.confirmed audit event is recorded
memory.created audit event is recorded
memory.activated audit event is recorded
audit events include actor context
audit events include correlation_id
audit payload is sanitized
```

---

# 17. Dashboard Tests

Required tests:

```text
counts open tasks
counts completed tasks
counts draft decisions
counts confirmed decisions
counts candidate memory entries
counts active memory entries
counts recent audit events
is workspace-scoped
rejects non-owner read
updates after task, decision and memory lifecycle changes
```

---

# 18. MVP Vertical Slice Test

Canonical e2e flow:

```text
GET /api/v1/me
POST /api/v1/workspaces
POST /api/v1/workspaces/{workspace_id}/tasks
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/complete
POST /api/v1/workspaces/{workspace_id}/decisions
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm
POST /api/v1/workspaces/{workspace_id}/memory-entries
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/activate
GET /api/v1/workspaces/{workspace_id}/audit-events
GET /api/v1/workspaces/{workspace_id}/dashboard
```

Acceptance:

```text
audit contains all required actions
dashboard reflects final state
no cross-workspace data appears
all responses match API contracts
```

---

# 19. Error Contract Tests

Required error tests:

```text
unauthenticated
forbidden
not_found
workspace_archived
validation_error
invalid_object_reference
invalid_status_transition
business_rule_violation
conflict
internal_error
```

Assertions:

```text
HTTP status code
error.code
error.message
error.details when applicable
request_id or correlation_id when available
```

---

# 20. CI Readiness

CI expectations:

```text
fresh PostgreSQL test service
migrations applied
test database reset
unit tests run
repository/integration tests run
API/e2e tests run
build runs after tests
```

Rule:

```text
Tests must not depend on local developer state.
```

---

# 21. Execution Order

Recommended order:

```text
1. Create test setup utilities
2. Create database reset helper
3. Create factories
4. Add shared kernel unit tests
5. Add repository tests
6. Add service tests
7. Add identity and workspace e2e tests
8. Add task and decision tests
9. Add memory and dashboard tests
10. Add audit evidence tests
11. Add transaction rollback tests
12. Add MVP vertical slice e2e test
13. Add CI-compatible commands
```

---

# 22. Verification Commands

Expected commands:

```bash
cd backend
pnpm db:test:reset
pnpm test:unit
pnpm test:integration
pnpm test:e2e
pnpm test
pnpm build
```

Expected result:

```text
all MVP test suites pass locally and are ready for CI workflow execution
```

---

# 23. Risks and Controls

## Risk 1 — Happy Path Only Tests

Mitigation:

```text
Require failure-path tests for every module.
```

## Risk 2 — No Cross-Workspace Coverage

Mitigation:

```text
Every workspace-scoped repository and API route must have cross-workspace tests.
```

## Risk 3 — Tests Use Wrong Database

Mitigation:

```text
Test setup must validate test environment and test database URL.
```

## Risk 4 — Audit Evidence Not Tested

Mitigation:

```text
Mutation tests must assert audit event creation.
```

---

# 24. Acceptance Criteria

Test Suite Execution is accepted when:

- target test structure is defined;
- test stack and commands are defined;
- test database strategy is documented;
- test context and factories are defined;
- unit, repository, service and API/e2e scopes are defined;
- transaction tests are defined;
- authorization and validation tests are defined;
- audit evidence tests are defined;
- dashboard tests are defined;
- MVP vertical slice test is defined;
- error contract tests are defined;
- CI readiness is documented;
- execution order and verification commands are documented;
- risks and controls are documented.

Status:

```text
Accepted for CI Workflow Execution
```

---

# 25. Final Statement

```text
Bizzi Test Suite Execution defines the proof system for the backend MVP.
```

This suite ensures Bizzi backend execution is not accepted until workspace isolation, authorization, validation, transactions, audit evidence, dashboard visibility and the full MVP vertical slice are verified.