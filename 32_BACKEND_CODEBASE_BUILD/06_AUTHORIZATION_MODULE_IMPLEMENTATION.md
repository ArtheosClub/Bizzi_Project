# 06_AUTHORIZATION_MODULE_IMPLEMENTATION.md

# Bizzi Platform

## Authorization Module Implementation

**Layer:** 32_BACKEND_CODEBASE_BUILD

### Purpose

Define the concrete implementation of the Authorization module for Bizzi Platform.

### Module Scope

The Authorization module enforces workspace ownership, mutation permissions, archived workspace restrictions and future role-based access boundaries.

### Directory Structure

```text
backend/src/modules/authorization/
 ├── authorization.module.ts
 ├── authorization.service.ts
 ├── workspace-permission.service.ts
 ├── role-resolution.service.ts
 ├── policies/
 │   ├── workspace-permission.policy.ts
 │   └── permission.constants.ts
 └── dto/
     └── authorization-result.dto.ts
```

### Responsibilities

- Require authenticated actor context.
- Require workspace ownership.
- Require active workspace for mutations.
- Provide reusable permission checks.
- Prepare future RBAC extension points.
- Prevent cross-workspace access.

### Core Methods

```text
requireAuthenticated(context)
requireWorkspaceOwner(context, workspaceId)
requireWorkspaceRead(context, workspaceId)
requireWorkspaceMutation(context, workspaceId)
canReadWorkspace(context, workspaceId)
canMutateWorkspace(context, workspaceId)
```

### MVP Authorization Model

```text
owner_user_id === actor_id
```

This means:

- workspace owner can read workspace data;
- workspace owner can mutate active workspace data;
- non-owner is denied;
- archived workspace blocks mutations.

### Future RBAC Extension

The module must allow future roles:

- owner
- admin
- manager
- auditor
- agent_operator
- viewer

### Integration Points

Authorization is required by:

- Workspace module
- Task module
- Decision module
- Memory module
- Audit module
- Dashboard module
- Export module later

### Error Contracts

Authorization failures must map to canonical errors:

```text
unauthenticated
forbidden
not_found
workspace_archived
```

### Acceptance Criteria

- Non-authenticated requests fail.
- Non-owner workspace access fails.
- Owner access succeeds.
- Archived workspace mutation fails.
- Services use AuthorizationService instead of local ad hoc checks.
- Unit tests cover owner and non-owner scenarios.

### Outcome

The Authorization module becomes the central enforcement layer for Bizzi workspace security and prepares the codebase for future role-based access control.