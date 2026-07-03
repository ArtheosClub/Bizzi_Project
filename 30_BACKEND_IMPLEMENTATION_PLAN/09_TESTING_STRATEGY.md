# 09_TESTING_STRATEGY.md

# Bizzi Platform

## Testing Strategy

**Layer:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Component Type:** Implementation Planning Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Previous Document:** 08_REPOSITORY_IMPLEMENTATION_GUIDE.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the backend testing strategy for Bizzi Platform MVP implementation.

It translates the service and repository implementation guides into a practical test approach covering unit tests, service tests, repository tests, API tests, transaction tests, security tests, audit/event tests and MVP acceptance tests.

Core question:

```text
How should Bizzi test backend implementation so that each module is reliable, workspace-scoped, auditable, transaction-safe and ready for expansion?
```

---

# 2. Testing Thesis

```text
Bizzi testing must prove architecture guarantees, not only happy-path functionality. The MVP backend is not accepted until workspace isolation, authorization, validation, transactions, audit events, runtime events and canonical errors are tested.
```

Testing protects:

```text
workspace boundaries
business lifecycle rules
audit evidence
runtime coordination
transaction consistency
API contract behavior
implementation discipline
```

---

# 3. Testing Stack

Recommended MVP testing stack:

```text
Jest
Supertest
Prisma test database
Docker Compose PostgreSQL
Test data factories
NestJS testing utilities
```

Optional later:

```text
Testcontainers
Playwright for frontend later
k6 for load testing later
OpenAPI contract testing later
```

---

# 4. Test Layers

Bizzi backend tests should be organized into:

```text
unit tests
service tests
repository tests
API / e2e tests
transaction tests
security tests
audit and runtime event tests
contract smoke tests
```

Each layer has a distinct purpose and should not replace the others.

---

# 5. Unit Tests

Unit tests cover pure logic and small policies.

Targets:

```text
status transition policies
validation helpers
error mappers
pagination helpers
DTO mappers
authorization decision helpers
business rule validators
```

Examples:

```text
TaskStatusPolicy allows open → completed
TaskStatusPolicy rejects completed → open
DecisionStatusPolicy allows draft → confirmed
ErrorMapper maps ForbiddenError to forbidden response
Pagination helper enforces page_size maximum
```

Rule:

```text
Unit tests should be fast and should not require a database.
```

---

# 6. Service Tests

Service tests cover business behavior.

Targets:

```text
WorkspaceService
TaskService
TaskLifecycleService
DecisionService
DecisionConfirmationService
MemoryService
MemoryActivationService
AuthorizationService
ValidationService
AuditService
RuntimeEventService
DashboardService
```

Service tests should verify:

```text
authorization is called
validation is enforced
repositories are used correctly
transactions wrap mutations
audit events are recorded
runtime events are emitted
canonical errors are raised
```

---

# 7. Repository Tests

Repository tests cover database access and workspace scoping.

Targets:

```text
UserRepository
WorkspaceRepository
WorkspaceSettingsRepository
TaskRepository
DecisionRepository
MemoryRepository
AuditEventRepository
RuntimeEventRepository
```

Repository tests must verify:

```text
create record
find by id and workspace
reject cross-workspace lookup
list by workspace
filter behavior
sort behavior
pagination behavior
archive/update behavior
```

Rule:

```text
Every workspace-scoped repository must have a cross-workspace isolation test.
```

---

# 8. API / E2E Tests

API tests verify route behavior through HTTP.

MVP API tests:

```text
GET /api/v1/me returns current actor
POST /api/v1/workspaces creates workspace
GET /api/v1/workspaces lists actor workspaces
POST /api/v1/workspaces/{workspace_id}/tasks creates task
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/complete completes task
POST /api/v1/workspaces/{workspace_id}/decisions creates decision
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm confirms decision
GET /api/v1/workspaces/{workspace_id}/audit-events returns audit events
GET /api/v1/workspaces/{workspace_id}/runtime-events returns runtime events
GET /api/v1/workspaces/{workspace_id}/dashboard returns counts
```

Rule:

```text
API tests must assert response shape, status code and canonical error shape.
```

---

# 9. Transaction Tests

Transaction tests prove state consistency.

Required transaction tests:

```text
workspace creation creates settings, audit event and runtime event atomically
task completion updates task and creates events atomically
decision confirmation updates decision and creates events atomically
failure in required audit write rolls back mutation
failure in required runtime event write rolls back mutation
```

Rule:

```text
No meaningful state change should be accepted without required audit evidence.
```

---

# 10. Authorization Tests

Authorization tests prove server-side access control.

Required tests:

```text
owner can access workspace
non-owner cannot access workspace
unauthenticated request is rejected
archived workspace blocks mutations
workspace-scoped reads require ownership
workspace-scoped writes require ownership
```

Expansion tests later:

```text
admin role can manage workspace
member role has limited access
auditor can read audit events
export manager can create export jobs
agent authority restrictions are enforced
```

---

# 11. Validation Tests

Validation tests prove input and business rules.

Required tests:

```text
missing required field returns validation_error
invalid UUID returns validation_error
invalid enum returns validation_error
cross-workspace object reference returns invalid_object_reference
invalid task status transition returns invalid_status_transition
invalid decision confirmation returns invalid_status_transition
archived memory cannot be activated
```

Rule:

```text
Validation errors should include structured detail when useful.
```

---

# 12. Audit Event Tests

Audit tests verify evidence creation.

Required tests:

```text
workspace.created audit event is recorded
task.created audit event is recorded
task.completed audit event is recorded
decision.created audit event is recorded
decision.confirmed audit event is recorded
memory.created audit event is recorded
memory.activated audit event is recorded
audit event includes actor context
audit event includes correlation_id
audit event excludes secrets
```

Rule:

```text
Audit tests must verify both existence and meaningful payload fields.
```

---

# 13. Runtime Event Tests

Runtime event tests verify coordination records.

Required tests:

```text
workspace.created runtime event is emitted
task.created runtime event is emitted
task.completed runtime event is emitted
dashboard.refresh_requested event is emitted after task completion
decision.confirmed runtime event is emitted
memory.activated runtime event is emitted
runtime event includes source object
runtime event includes correlation_id
runtime event excludes secrets
```

---

# 14. Dashboard Tests

Dashboard tests verify visible operating state.

Required tests:

```text
dashboard counts open tasks
dashboard counts completed tasks
dashboard counts confirmed decisions
dashboard counts active memory entries
dashboard excludes archived records
dashboard is workspace-scoped
dashboard updates after task completion and decision confirmation
```

MVP rule:

```text
Dashboard tests may use live counts instead of persisted dashboard_metrics.
```

---

# 15. Error Contract Tests

Error contract tests verify canonical response shape.

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

Test assertions:

```text
HTTP status code
error code
message
request_id or correlation_id when included
validation details when applicable
```

---

# 16. Test Data Strategy

Use factories for test data.

Recommended factories:

```text
UserFactory
WorkspaceFactory
TaskFactory
DecisionFactory
MemoryEntryFactory
AuditEventFactory
RuntimeEventFactory
```

Rules:

```text
test data must be isolated per test
test data must use unique ids and emails
cross-workspace tests must create at least two workspaces
seed data must not be required for deterministic tests unless explicitly loaded
```

---

# 17. Test Database Strategy

MVP approach:

```text
local PostgreSQL test database
Prisma migrations applied before test run
clean database between tests or test suites
```

Options:

```text
truncate tables between tests
transaction rollback per test where practical
recreate schema for e2e suite
```

Rule:

```text
Repository and API tests must not run against development or production databases.
```

---

# 18. Mocking Strategy

Mock only where useful.

Use mocks for:

```text
external providers
object storage
job queue
AI provider calls
email or notification providers
```

Do not over-mock:

```text
repositories in repository tests
HTTP layer in API tests
transaction behavior in transaction tests
```

Rule:

```text
Critical architecture guarantees should be tested with real integration paths where possible.
```

---

# 19. Coverage Expectations

MVP coverage target should focus on critical paths.

Minimum expectation:

```text
all P1 API routes tested
all MVP services tested
all MVP repositories tested
all lifecycle transitions tested
all authorization failure paths tested
all audit/runtime event side effects tested
```

Numeric coverage targets may be introduced later, but should not replace meaningful scenario coverage.

---

# 20. CI Testing Gates

Initial CI gates:

```text
install dependencies
lint
typecheck
unit tests
repository tests
API tests
build
```

Later CI gates:

```text
migration validation
OpenAPI generation
contract diff
security scan
coverage threshold
performance smoke test
```

Rule:

```text
main branch should not accept changes that break MVP test gates.
```

---

# 21. MVP Acceptance Test Scenario

Canonical MVP scenario:

```text
create user context
create workspace
create task
complete task
create decision
confirm decision
create memory entry
activate memory entry
read audit events
read runtime events
read dashboard
verify counts and event evidence
```

This scenario should be implemented as an API/e2e test.

---

# 22. Regression Testing

Regression tests should be added for every fixed bug.

Rule:

```text
A bug is not fixed until a test prevents it from returning.
```

Regression categories:

```text
workspace isolation bugs
authorization bypasses
invalid lifecycle transitions
missing audit events
missing runtime events
incorrect dashboard counts
canonical error shape regressions
```

---

# 23. Security Testing Baseline

MVP security tests:

```text
non-owner cannot access workspace data
cross-workspace object id is rejected
raw secrets are not returned in API responses
raw secrets are not stored in audit/runtime payloads
runtime events are owner-restricted
```

Expansion security tests:

```text
RBAC role permissions
security policy enforcement
integration credential_ref rules
export scope authorization
rate limit behavior
```

---

# 24. Performance Smoke Tests

MVP performance testing is light.

Smoke checks:

```text
dashboard returns within acceptable local threshold
list endpoints are paginated
audit/runtime event list queries use workspace filters
unbounded list queries are not allowed
```

Rule:

```text
Do not optimize prematurely, but prevent obviously unbounded API behavior.
```

---

# 25. Test Completion Checklist

A module is test-complete when:

```text
unit tests cover policies and validators
service tests cover success and failures
repository tests cover workspace scope and pagination
API tests cover route behavior if API-facing
audit/runtime event side effects are tested for mutations
canonical error responses are tested
cross-workspace access is tested
```

---

# 26. Anti-Patterns

Avoid:

```text
only testing happy paths
testing services only through controllers
mocking the database in repository tests
skipping cross-workspace tests
skipping audit/runtime event assertions
asserting only HTTP 200 without response shape
using production-like secrets in tests
depending on test order
```

---

# 27. Acceptance Criteria

Testing Strategy is accepted when:

- testing stack is defined;
- test layers are defined;
- unit, service, repository and API testing scope is documented;
- transaction tests are specified;
- authorization and validation tests are specified;
- audit and runtime event tests are specified;
- dashboard tests are specified;
- error contract tests are specified;
- test data and test database strategies are defined;
- CI gates are proposed;
- MVP acceptance scenario is defined;
- module test completion checklist is provided;
- anti-patterns are documented.

Status:

```text
Accepted for Local Development Workflow
```

---

# 28. Final Statement

```text
Bizzi Testing Strategy defines how backend implementation proves not only feature behavior, but also architecture guarantees: workspace isolation, authorization, validation, transaction safety, auditability and runtime coordination.
```

This strategy makes the MVP backend testable, trustworthy and safe to extend.