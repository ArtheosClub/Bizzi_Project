# 05_WORKSPACE_MODULE_IMPLEMENTATION.md

# Bizzi Platform

## Workspace Module Implementation

**Layer:** 32_BACKEND_CODEBASE_BUILD

### Purpose

Define the concrete implementation of the Workspace module, the primary tenant boundary of Bizzi Platform.

### Module Scope

The Workspace module manages company workspaces, workspace settings and owner-scoped workspace access.

### Directory Structure

```text
backend/src/modules/workspace/
 ├── workspace.module.ts
 ├── workspace.controller.ts
 ├── workspace.service.ts
 ├── workspace.repository.ts
 ├── workspace-settings.service.ts
 ├── workspace-settings.repository.ts
 ├── dto/
 │   ├── create-workspace.dto.ts
 │   ├── update-workspace.dto.ts
 │   ├── workspace-response.dto.ts
 │   └── workspace-settings.dto.ts
 ├── mappers/
 │   ├── workspace.mapper.ts
 │   └── workspace-settings.mapper.ts
 └── policies/
     └── workspace-status.policy.ts
```

### API Routes

```text
POST /api/v1/workspaces
GET /api/v1/workspaces
GET /api/v1/workspaces/{workspace_id}
PATCH /api/v1/workspaces/{workspace_id}
GET /api/v1/workspaces/{workspace_id}/settings
PATCH /api/v1/workspaces/{workspace_id}/settings
```

### Responsibilities

- Create workspace from authenticated actor.
- Create default workspace settings.
- List actor-owned workspaces.
- Read workspace by ID.
- Update workspace metadata.
- Update workspace settings.
- Enforce workspace ownership.
- Prevent mutation of archived workspaces.

### Repository Methods

```text
createWorkspace(data)
findWorkspaceById(id)
findWorkspaceByIdAndOwner(id, ownerUserId)
listWorkspacesByOwner(ownerUserId, pagination)
updateWorkspace(id, data)
archiveWorkspace(id)
createWorkspaceSettings(data)
findSettingsByWorkspaceId(workspaceId)
updateSettings(workspaceId, data)
```

### Service Methods

```text
createWorkspace(context, dto)
listWorkspaces(context, query)
getWorkspace(context, workspaceId)
updateWorkspace(context, workspaceId, dto)
getWorkspaceSettings(context, workspaceId)
updateWorkspaceSettings(context, workspaceId, dto)
```

### Data Rules

- `owner_user_id` is derived from ActorContext.
- `workspace_id` is never accepted from request body for scoped routes.
- Workspace settings are created transactionally with workspace creation.
- Workspace status controls mutation access.

### Security Rules

- Only workspace owner can access workspace in MVP.
- Unauthorized workspace access returns safe error.
- Archived workspaces are read-only.
- Workspace settings updates require owner access.

### Acceptance Criteria

- Workspace can be created.
- Default settings are created automatically.
- Workspace list is owner-scoped.
- Workspace detail enforces ownership.
- Workspace settings can be read and updated.
- Archived workspace mutation is blocked.
- Unit and e2e tests cover ownership boundaries.

### Outcome

The Workspace module establishes the tenant boundary that all other Bizzi backend modules depend on.