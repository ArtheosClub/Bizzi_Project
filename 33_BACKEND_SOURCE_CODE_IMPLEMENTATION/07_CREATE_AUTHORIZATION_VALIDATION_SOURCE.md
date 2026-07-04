# 07_CREATE_AUTHORIZATION_VALIDATION_SOURCE.md

# Bizzi Platform

## Create Authorization Validation Source

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Implementation Plan  
**Previous Layer Reference:** 32_BACKEND_CODEBASE_BUILD  
**Product:** Bizzi Platform  
**Status:** Draft v0.1

---

# 1. Purpose

This document defines the concrete source-code creation plan for the Authorization and Validation layer of the Bizzi backend.

It translates the prior architectural and codebase-build specifications into actual backend source files for:

```text
AuthorizationModule
AuthorizationService
WorkspacePermissionService
RoleResolutionService
ValidationModule
ValidationService
ObjectReferenceValidator
StatusTransitionValidator
BusinessRuleValidator
permission policies
status policies
unit tests
```

---

# 2. Source Code Objective

The objective is to create the backend source code that enforces:

```text
authenticated actor presence
workspace ownership
active workspace mutation rules
object reference safety
cross-workspace rejection
status transition rules
business rule validation
canonical error behavior
future RBAC extension points
```

This source layer becomes the reusable enforcement boundary for Workspace, Task, Decision, Memory, Audit and Dashboard modules.

---

# 3. Target Files

## Authorization files

```text
backend/src/modules/authorization/authorization.module.ts
backend/src/modules/authorization/authorization.service.ts
backend/src/modules/authorization/workspace-permission.service.ts
backend/src/modules/authorization/role-resolution.service.ts
backend/src/modules/authorization/policies/workspace-permission.policy.ts
backend/src/modules/authorization/policies/permission.constants.ts
backend/src/modules/authorization/dto/authorization-result.dto.ts
```

## Validation files

```text
backend/src/modules/validation/validation.module.ts
backend/src/modules/validation/validation.service.ts
backend/src/modules/validation/object-reference-validator.service.ts
backend/src/modules/validation/status-transition-validator.service.ts
backend/src/modules/validation/business-rule-validator.service.ts
backend/src/modules/validation/policies/task-status.policy.ts
backend/src/modules/validation/policies/decision-status.policy.ts
backend/src/modules/validation/policies/memory-status.policy.ts
```

## Tests

```text
backend/src/modules/authorization/__tests__/authorization.service.spec.ts
backend/src/modules/authorization/__tests__/workspace-permission.service.spec.ts
backend/src/modules/validation/__tests__/validation.service.spec.ts
backend/src/modules/validation/__tests__/object-reference-validator.service.spec.ts
backend/src/modules/validation/__tests__/status-transition-validator.service.spec.ts
backend/src/modules/validation/__tests__/business-rule-validator.service.spec.ts
```

---

# 4. AuthorizationModule

`AuthorizationModule` should provide and export:

```text
AuthorizationService
WorkspacePermissionService
RoleResolutionService
```

It should import only required dependencies, especially workspace repository access or workspace service read adapters.

Rule:

```text
Feature modules must import AuthorizationModule rather than duplicate workspace ownership logic.
```

---

# 5. AuthorizationService

Required public methods:

```typescript
requireAuthenticated(context: ServiceContext): void;
requireWorkspaceOwner(context: ServiceContext, workspaceId: string): Promise<void>;
requireWorkspaceRead(context: ServiceContext, workspaceId: string): Promise<void>;
requireWorkspaceMutation(context: ServiceContext, workspaceId: string): Promise<void>;
canReadWorkspace(context: ServiceContext, workspaceId: string): Promise<boolean>;
canMutateWorkspace(context: ServiceContext, workspaceId: string): Promise<boolean>;
```

Required behavior:

```text
validate actor exists
load workspace
verify owner_user_id equals actor_id
block mutation if workspace is archived
raise canonical errors
```

Canonical errors:

```text
unauthenticated
forbidden
not_found
workspace_archived
```

---

# 6. WorkspacePermissionService

Required methods:

```typescript
isOwner(actorId: string, ownerUserId: string): boolean;
canReadWorkspace(actorId: string, workspace: WorkspaceRecord): boolean;
canMutateWorkspace(actorId: string, workspace: WorkspaceRecord): boolean;
```

MVP rule:

```text
owner_user_id === actor_id
```

Future rule:

```text
Replace owner-only logic with RBAC and workspace membership tables without changing feature module APIs.
```

---

# 7. RoleResolutionService

MVP implementation:

```text
return owner role if actor is workspace owner
return empty permissions otherwise
```

Future extension:

```text
workspace roles
agent authority roles
viewer/auditor/admin roles
external policy engine
```

---

# 8. Permission Constants

Initial constants:

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
dashboard.read
```

Rule:

```text
Permission constants must be stable strings because they will later become policy and audit evidence identifiers.
```

---

# 9. ValidationModule

`ValidationModule` should provide and export:

```text
ValidationService
ObjectReferenceValidatorService
StatusTransitionValidatorService
BusinessRuleValidatorService
```

Rule:

```text
Validation must be reusable by all workspace-scoped modules.
```

---

# 10. ValidationService

Required methods:

```typescript
requireUuid(value: string, field: string): void;
requireString(value: unknown, field: string): void;
requireNonEmpty(value: unknown, field: string): void;
requireEnum<T extends string>(value: string, allowed: T[], field: string): void;
requireBoolean(value: unknown, field: string): void;
requireDateRange(start?: Date, end?: Date): void;
requirePagination(page: number, pageSize: number): void;
```

Errors:

```text
validation_error
business_rule_violation
```

---

# 11. ObjectReferenceValidatorService

Required methods:

```typescript
requireTaskInWorkspace(taskId: string, workspaceId: string): Promise<void>;
requireDecisionInWorkspace(decisionId: string, workspaceId: string): Promise<void>;
requireMemoryEntryInWorkspace(memoryEntryId: string, workspaceId: string): Promise<void>;
requireSourceObjectInWorkspace(type: string, id: string, workspaceId: string): Promise<void>;
```

Rule:

```text
Any object reference provided in a request must belong to the same workspace as the target mutation.
```

Error:

```text
invalid_object_reference
```

---

# 12. StatusTransitionValidatorService

Required methods:

```typescript
requireTaskTransition(current: TaskStatus, next: TaskStatus): void;
requireDecisionTransition(current: DecisionStatus, next: DecisionStatus): void;
requireMemoryTransition(current: MemoryStatus, next: MemoryStatus): void;
```

Invalid transitions raise:

```text
invalid_status_transition
```

---

# 13. BusinessRuleValidatorService

Required checks:

```text
task title required
decision title required
memory title required
memory content required
workspace name required
archived records immutable
confirmed decision cannot be confirmed again
completed task cannot be completed again
active memory cannot be activated again
```

Rule:

```text
Business rules must be explicit and testable, not hidden only in DTO decorators.
```

---

# 14. Status Policies

## Task

Allowed transitions:

```text
draft → open
open → in_progress
open → completed
in_progress → completed
open → archived
in_progress → archived
completed → archived
```

## Decision

Allowed transitions:

```text
draft → confirmed
draft → archived
confirmed → archived
```

## Memory

Allowed transitions:

```text
candidate → active
candidate → archived
active → archived
```

---

# 15. Testing Requirements

Authorization tests must prove:

```text
missing actor fails
owner can read workspace
non-owner cannot read workspace
owner can mutate active workspace
owner cannot mutate archived workspace
```

Validation tests must prove:

```text
invalid UUID fails
missing required values fail
invalid enum fails
invalid pagination fails
cross-workspace task reference fails
invalid task transition fails
invalid decision transition fails
invalid memory transition fails
```

---

# 16. Implementation Order

Recommended order:

```text
1. Create AuthorizationModule
2. Create permission constants
3. Create WorkspacePermissionService
4. Create RoleResolutionService
5. Create AuthorizationService
6. Create ValidationModule
7. Create ValidationService
8. Create status policies
9. Create StatusTransitionValidatorService
10. Create ObjectReferenceValidatorService
11. Create BusinessRuleValidatorService
12. Add tests
13. Export modules to feature modules
```

---

# 17. Acceptance Criteria

This source implementation is accepted when:

- authorization source files are defined;
- validation source files are defined;
- workspace owner enforcement is centralized;
- archived workspace mutation is blocked;
- object reference validation is centralized;
- lifecycle validation is centralized;
- business rules are explicit;
- tests are defined;
- feature modules can depend on these services without duplicating checks.

---

# 18. Final Statement

```text
The Authorization and Validation source implementation creates the enforcement layer that keeps Bizzi workspace data safe, consistent and ready for real module implementation.
```
