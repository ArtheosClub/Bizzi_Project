# 06_AUTHORIZATION_VALIDATION_EXECUTION.md

# Bizzi Platform

## Authorization Validation Execution

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
**Previous Document:** 05_WORKSPACE_MODULE_EXECUTION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch III — Backend Execution

---

# 1. Purpose

This document defines the Authorization and Validation execution plan for Bizzi Platform backend MVP.

It specifies how to implement the shared enforcement layer that protects workspace ownership, archived workspace rules, object reference validation, input validation, status transition validation and canonical failure handling before task, decision, memory, audit and dashboard modules are completed.

Core question:

```text
How should Bizzi enforce authorization and validation consistently so every workspace-scoped service remains safe, predictable and testable?
```

---

# 2. Authorization Validation Thesis

```text
Authorization and validation must be service-level enforcement layers, not controller-only checks. Controllers may guard routes, but services must protect business operations and workspace data.
```

This layer proves:

```text
workspace owner checks
active workspace checks
object reference validation
cross-workspace rejection
status transition validation
canonical error raising
reusable validation patterns
future RBAC compatibility
```

---

# 3. Target Directory Structure

Target structure:

```text
backend/src/modules/authorization/
├── authorization.module.ts
├── services/
│   ├── authorization.service.ts
│   ├── workspace-permission.service.ts
│   └── role-resolution.service.ts
├── policies/
│   └── workspace-permission.policy.ts
└── tests/
    ├── authorization.service.spec.ts
    └── workspace-permission.service.spec.ts

backend/src/modules/validation/
├── validation.module.ts
├── services/
│   ├── validation.service.ts
│   ├── object-reference-validator.service.ts
│   ├── status-transition-validator.service.ts
│   └── business-rule-validator.service.ts
├── policies/
│   ├── task-status.policy.ts
│   ├── decision-status.policy.ts
│   └── memory-status.policy.ts
└── tests/
    ├── object-reference-validator.service.spec.ts
    ├── status-transition-validator.service.spec.ts
    └── business-rule-validator.service.spec.ts
```

---

# 4. Execution Non-Scope

This execution step does not implement:

```text
full RBAC permission matrix
workspace invitations
team membership management
attribute-based access control
policy engine integration
external identity provider permissions
row-level security
advanced legal approval workflows
```

These are later platform security expansions.

---

# 5. MVP Authorization Model

MVP authorization model:

```text
owner-only workspace access
```

Rule:

```text
A user may access or mutate a workspace only when ServiceContext.actorId equals CompanyWorkspace.owner_user_id.
```

Authorized actor types for MVP:

```text
user
system for internal jobs later
agent only after agent authority layer exists
```

MVP rule:

```text
Agent-originated official mutations are not allowed until agent authority execution exists.
```

---

# 6. AuthorizationService

`AuthorizationService` should expose:

```text
requireAuthenticated(context)
requireWorkspaceOwner(context)
requireActiveWorkspace(context)
requireWorkspaceMutationAllowed(context)
```

Dependencies:

```text
WorkspaceRepository
WorkspacePermissionService
WorkspaceStatusPolicy
```

Required behavior:

```text
validate actor context exists
validate workspace_id exists for workspace-scoped operations
load workspace by id
verify owner_user_id equals actor_id
verify workspace is active for mutations
raise canonical errors
```

---

# 7. WorkspacePermissionService

`WorkspacePermissionService` should encapsulate owner permission checks.

Required methods:

```text
isWorkspaceOwner(actorId, workspace)
requireOwner(actorId, workspace)
canReadWorkspace(actorId, workspace)
canMutateWorkspace(actorId, workspace)
```

Future compatibility:

```text
role-based access can be introduced here without rewriting feature services
```

Rule:

```text
Feature services must not duplicate ownership logic manually once AuthorizationService exists.
```

---

# 8. RoleResolutionService

For MVP, `RoleResolutionService` may be minimal.

MVP behavior:

```text
owner_user_id implies owner role
no separate workspace_access table required for enforcement
```

Future behavior:

```text
load workspace_access rows
resolve roles
resolve permissions
support auditor/member/admin/export_manager roles
```

Rule:

```text
Do not overbuild RBAC before MVP workspace loop is complete.
```

---

# 9. Workspace Permission Policy

`WorkspacePermissionPolicy` defines permission names for future expansion.

Initial permissions:

```text
workspace.read
workspace.update
workspace.archive
workspace_settings.read
workspace_settings.update
task.create
task.read
task.update
task.complete
decision.create
decision.read
decision.confirm
memory.create
memory.read
memory.activate
audit_event.read
runtime_event.read
dashboard.read
```

MVP implementation:

```text
all permissions require workspace owner
```

---

# 10. ValidationService

`ValidationService` provides reusable simple validation.

Required methods:

```text
requireString(value, field)
requireNonEmpty(value, field)
requireUuid(value, field)
requireEnum(value, allowedValues, field)
requireBoolean(value, field)
requireDateRange(start, end)
requirePaginationBounds(page, pageSize)
```

Rule:

```text
DTO validation does not replace service-level validation for business operations.
```

---

# 11. ObjectReferenceValidator

`ObjectReferenceValidatorService` validates cross-object relationships.

Required methods:

```text
requireWorkspaceExists(workspaceId)
requireTaskInWorkspace(taskId, workspaceId)
requireDecisionInWorkspace(decisionId, workspaceId)
requireMemoryEntryInWorkspace(memoryEntryId, workspaceId)
requireSourceObjectInWorkspace(sourceObjectType, sourceObjectId, workspaceId)
```

Rules:

```text
optional references may be null
if reference exists, it must belong to the same workspace
invalid cross-workspace references raise invalid_object_reference
missing referenced objects raise invalid_object_reference or not_found according to contract
```

---

# 12. StatusTransitionValidator

`StatusTransitionValidatorService` validates lifecycle transitions.

Required methods:

```text
requireTaskCompletionAllowed(task)
requireDecisionConfirmationAllowed(decision)
requireMemoryActivationAllowed(memoryEntry)
requireWorkspaceMutationAllowed(workspace)
```

Canonical failures:

```text
invalid_status_transition
workspace_archived
business_rule_violation
```

---

# 13. BusinessRuleValidator

`BusinessRuleValidatorService` validates higher-level business rules.

MVP rules:

```text
task title required
decision title required
memory content required
workspace name required
workspace slug unique
archived records cannot be mutated
confirmed decisions cannot be reconfirmed
completed tasks cannot be completed again
active memory cannot be activated again
```

Rule:

```text
Business rules should remain explicit and testable, not hidden only in DTO decorators.
```

---

# 14. Task Status Policy

Task allowed transitions:

```text
open → in_progress
open → completed
in_progress → completed
open → archived
in_progress → archived
completed → archived
```

Disallowed MVP transitions:

```text
completed → open
archived → open
archived → completed
completed → completed
```

Rule:

```text
Task completion must reject already completed or archived tasks.
```

---

# 15. Decision Status Policy

Decision allowed transitions:

```text
draft → confirmed
draft → archived
confirmed → archived
```

Disallowed MVP transitions:

```text
confirmed → draft
archived → confirmed
confirmed → confirmed
```

Rule:

```text
Decision confirmation must be idempotency-aware later, but MVP should reject duplicate confirmation.
```

---

# 16. Memory Status Policy

Memory allowed transitions:

```text
candidate → active
candidate → archived
active → archived
```

Disallowed MVP transitions:

```text
active → candidate
archived → active
active → active
```

Rule:

```text
Only candidate memory entries can be activated.
```

---

# 17. Error Mapping

Authorization and validation failures must use shared canonical errors.

Mappings:

```text
missing actor → unauthenticated
non-owner workspace access → forbidden or safe not_found depending route
missing workspace → not_found
archived workspace mutation → workspace_archived
invalid UUID → validation_error
cross-workspace reference → invalid_object_reference
invalid lifecycle transition → invalid_status_transition
duplicate slug → conflict
```

Rule:

```text
Do not throw raw strings, raw Prisma errors or framework-specific exceptions from services.
```

---

# 18. Integration With WorkspaceModule

WorkspaceModule should transition from temporary owner filters to AuthorizationService.

Expected changes:

```text
WorkspaceService.getWorkspace calls AuthorizationService.requireWorkspaceOwner
WorkspaceSettingsService.getWorkspaceSettings calls AuthorizationService.requireWorkspaceOwner
WorkspaceSettingsService.updateWorkspaceSettings calls AuthorizationService.requireWorkspaceMutationAllowed
```

Rule:

```text
AuthorizationService becomes the canonical owner-check boundary after this execution step.
```

---

# 19. Integration With Future Modules

Future modules must call:

```text
AuthorizationService.requireWorkspaceOwner(context)
AuthorizationService.requireWorkspaceMutationAllowed(context)
ObjectReferenceValidator.requireTaskInWorkspace(...)
StatusTransitionValidator.requireTaskCompletionAllowed(...)
```

Feature modules affected:

```text
TaskModule
DecisionModule
MemoryModule
AuditModule read paths
RuntimeEventModule read paths
DashboardModule
ExportModule later
```

---

# 20. Tests Required

Authorization tests:

```text
owner can read workspace
non-owner cannot read workspace
owner can mutate active workspace
owner cannot mutate archived workspace
missing actor returns unauthenticated
missing workspace_id returns validation_error or business_rule_violation
```

Validation tests:

```text
invalid UUID rejected
missing required string rejected
invalid enum rejected
page_size maximum enforced
cross-workspace task reference rejected
missing referenced decision rejected
completed task cannot complete again
confirmed decision cannot confirm again
archived memory cannot activate
```

Integration tests:

```text
WorkspaceService uses AuthorizationService
TaskService later rejects cross-workspace task access
DecisionService later rejects cross-workspace task_id reference
```

---

# 21. Execution Order

Recommended execution order:

```text
1. Create AuthorizationModule
2. Create WorkspacePermissionService
3. Create RoleResolutionService minimal
4. Create AuthorizationService
5. Create workspace permission policy
6. Create ValidationModule
7. Create ValidationService
8. Create object reference validator
9. Create status transition validator
10. Create business rule validator
11. Create task/decision/memory status policies
12. Refactor WorkspaceModule owner checks through AuthorizationService
13. Add tests
14. Verify typecheck/test/build
```

---

# 22. Verification Commands

Expected commands:

```bash
cd backend
pnpm typecheck
pnpm test
pnpm test:e2e
pnpm build
```

Manual smoke checks:

```text
GET /api/v1/workspaces/{workspace_id} as owner → success
GET /api/v1/workspaces/{workspace_id} as non-owner → rejection
PATCH /api/v1/workspaces/{workspace_id}/workspace-settings on archived workspace → workspace_archived
```

---

# 23. Risks and Controls

## Risk 1 — Authorization Only in Controller

Mitigation:

```text
Require service-level AuthorizationService calls.
```

## Risk 2 — Cross-Workspace References

Mitigation:

```text
Use ObjectReferenceValidator for every optional object reference.
```

## Risk 3 — Status Rules Scattered Across Services

Mitigation:

```text
Centralize lifecycle rules in status policies and validators.
```

## Risk 4 — RBAC Overengineering

Mitigation:

```text
Implement owner-only MVP with future-compatible policy names.
```

---

# 24. Acceptance Criteria

Authorization Validation Execution is accepted when:

- target directory structure is defined;
- execution non-scope is documented;
- MVP authorization model is defined;
- AuthorizationService is defined;
- WorkspacePermissionService is defined;
- RoleResolutionService minimal behavior is defined;
- permission policy is defined;
- ValidationService is defined;
- ObjectReferenceValidator is defined;
- StatusTransitionValidator is defined;
- BusinessRuleValidator is defined;
- task, decision and memory status policies are defined;
- error mappings are documented;
- integration with WorkspaceModule is documented;
- future module integration is documented;
- tests are specified;
- execution order and verification commands are documented;
- risks and controls are documented.

Status:

```text
Accepted for Audit Event Execution
```

---

# 25. Final Statement

```text
Bizzi Authorization Validation Execution defines the enforcement layer that protects workspace boundaries, object references and lifecycle transitions before business execution modules are implemented.
```

This layer ensures that task, decision, memory, audit, runtime and dashboard modules can rely on consistent service-level authorization and validation guarantees.