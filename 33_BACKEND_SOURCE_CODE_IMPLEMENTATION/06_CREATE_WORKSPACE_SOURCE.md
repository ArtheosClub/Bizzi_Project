# 06_CREATE_WORKSPACE_SOURCE.md

# Bizzi Platform

## Create Workspace Source

**Layer:** 33_BACKEND_SOURCE_CODE_IMPLEMENTATION  
**Component Type:** Source Code Implementation Specification  
**Previous Layer:** 32_BACKEND_CODEBASE_BUILD  
**Product:** Bizzi Platform  
**Status:** Draft v0.1

---

# 1. Purpose

This document defines the concrete source-code implementation plan for the Workspace module in the Bizzi backend.

It translates the Workspace module specification from Layer 32 into actual NestJS/TypeScript source files, DTOs, services, repositories, mappers, policies and tests.

Core question:

```text
Which source files must be created so Bizzi can create, read, list and update workspace entities safely with owner-scoped authorization?
```

---

# 2. Source Implementation Scope

This implementation creates source files for:

```text
WorkspaceModule
WorkspaceController
WorkspaceService
WorkspaceRepository
WorkspaceSettingsService
WorkspaceSettingsRepository
Workspace DTOs
Workspace mappers
Workspace status policy
Workspace tests
```

---

# 3. Target Source Tree

```text
backend/src/modules/workspace/
├── workspace.module.ts
├── controllers/
│   ├── workspace.controller.ts
│   └── workspace-settings.controller.ts
├── services/
│   ├── workspace.service.ts
│   └── workspace-settings.service.ts
├── repositories/
│   ├── workspace.repository.ts
│   └── workspace-settings.repository.ts
├── dto/
│   ├── create-workspace.dto.ts
│   ├── update-workspace.dto.ts
│   ├── workspace-response.dto.ts
│   ├── update-workspace-settings.dto.ts
│   └── workspace-settings-response.dto.ts
├── mappers/
│   ├── workspace.mapper.ts
│   └── workspace-settings.mapper.ts
├── policies/
│   └── workspace-status.policy.ts
└── __tests__/
    ├── workspace.service.spec.ts
    ├── workspace.repository.spec.ts
    └── workspace.e2e-spec.ts
```

---

# 4. Required API Routes

```text
POST /api/v1/workspaces
GET /api/v1/workspaces
GET /api/v1/workspaces/:workspace_id
PATCH /api/v1/workspaces/:workspace_id
GET /api/v1/workspaces/:workspace_id/settings
PATCH /api/v1/workspaces/:workspace_id/settings
```

MVP priority:

```text
POST /api/v1/workspaces
GET /api/v1/workspaces
GET /api/v1/workspaces/:workspace_id
```

---

# 5. workspace.module.ts

Responsibilities:

```text
register WorkspaceController
register WorkspaceSettingsController
provide WorkspaceService
provide WorkspaceSettingsService
provide WorkspaceRepository
provide WorkspaceSettingsRepository
export WorkspaceService for other modules
```

Dependencies:

```text
PrismaModule
AuthorizationModule
AuditModule later
SharedModule
```

---

# 6. CreateWorkspaceDto

File:

```text
backend/src/modules/workspace/dto/create-workspace.dto.ts
```

Fields:

```text
name required string
slug optional string
description optional string
timezone optional string
locale optional string
```

Validation rules:

```text
name must not be empty
slug must be URL-safe if present
timezone defaults to UTC
locale defaults to en
```

---

# 7. WorkspaceResponseDto

File:

```text
backend/src/modules/workspace/dto/workspace-response.dto.ts
```

Fields:

```text
id
owner_user_id
name
slug
status
onboarding_status
description
created_at
updated_at
archived_at
```

Security rule:

```text
Response DTO must not expose raw internal database metadata.
```

---

# 8. WorkspaceRepository

File:

```text
backend/src/modules/workspace/repositories/workspace.repository.ts
```

Required methods:

```text
create(db, data)
findById(db, id)
findByIdAndOwner(db, id, ownerUserId)
findBySlug(db, slug)
listByOwner(db, ownerUserId, pagination)
updateByIdAndOwner(db, id, ownerUserId, patch)
archiveByIdAndOwner(db, id, ownerUserId, patch)
```

Repository rules:

```text
repository returns persistence records
repository does not return DTOs
repository supports transaction client
owner-scoped reads must include owner_user_id
```

---

# 9. WorkspaceSettingsRepository

File:

```text
backend/src/modules/workspace/repositories/workspace-settings.repository.ts
```

Required methods:

```text
create(db, data)
findByWorkspaceId(db, workspaceId)
updateByWorkspaceId(db, workspaceId, patch)
```

Rules:

```text
settings are one-to-one with workspace
workspace_id is unique
settings creation occurs in the same transaction as workspace creation
```

---

# 10. WorkspaceService

File:

```text
backend/src/modules/workspace/services/workspace.service.ts
```

Required methods:

```text
createWorkspace(context, input)
listWorkspaces(context, pagination)
getWorkspace(context, workspaceId)
updateWorkspace(context, workspaceId, input)
archiveWorkspace(context, workspaceId)
```

MVP implementation order:

```text
createWorkspace
listWorkspaces
getWorkspace
```

Service rules:

```text
owner_user_id comes from context.actorId
workspace_id is never accepted from request body
workspace and default settings are created transactionally
duplicate slug maps to conflict
missing workspace maps to not_found
```

---

# 11. WorkspaceSettingsService

File:

```text
backend/src/modules/workspace/services/workspace-settings.service.ts
```

Required methods:

```text
createDefaultSettingsForWorkspace(tx, workspaceId, input)
getWorkspaceSettings(context, workspaceId)
updateWorkspaceSettings(context, workspaceId, input)
```

Default settings:

```text
timezone = UTC
locale = en
ai_assistance_enabled = true
memory_enabled = true
audit_enabled = true
```

---

# 12. WorkspaceController

File:

```text
backend/src/modules/workspace/controllers/workspace.controller.ts
```

Responsibilities:

```text
read RequestContext using CurrentContext decorator
call WorkspaceService
return DTOs
not contain business logic
```

Controller methods:

```text
createWorkspace
listWorkspaces
getWorkspace
updateWorkspace
```

---

# 13. WorkspaceSettingsController

File:

```text
backend/src/modules/workspace/controllers/workspace-settings.controller.ts
```

Controller methods:

```text
getWorkspaceSettings
updateWorkspaceSettings
```

Rule:

```text
Settings routes must require workspace owner access.
```

---

# 14. WorkspaceMapper

File:

```text
backend/src/modules/workspace/mappers/workspace.mapper.ts
```

Mapping rules:

```text
ownerUserId → owner_user_id
onboardingStatus → onboarding_status
createdAt → created_at
updatedAt → updated_at
archivedAt → archived_at
```

---

# 15. WorkspaceStatusPolicy

File:

```text
backend/src/modules/workspace/policies/workspace-status.policy.ts
```

Required helpers:

```text
isActive(status)
isArchived(status)
canMutate(status)
canArchive(status)
```

Rules:

```text
active workspace allows mutation
archived workspace blocks mutation
archived workspace may allow limited read
```

---

# 16. Transaction Behavior

Workspace creation must be atomic:

```text
begin transaction
create CompanyWorkspace
create WorkspaceSettings
record workspace.created audit event later
commit
```

Rollback cases:

```text
workspace settings creation fails
slug conflict detected during persistence
audit write fails after audit module is wired
```

---

# 17. Authorization Behavior

MVP behavior:

```text
actor must be authenticated
actor can only access owned workspaces
owner_user_id equals context.actorId
```

After AuthorizationModule is wired:

```text
WorkspaceService uses AuthorizationService.requireWorkspaceOwner
WorkspaceSettingsService uses AuthorizationService.requireWorkspaceMutation
```

---

# 18. Error Mapping

Required mappings:

```text
missing actor → unauthenticated
invalid input → validation_error
duplicate slug → conflict
workspace not found → not_found
non-owner access → not_found or forbidden-safe response
archived workspace mutation → workspace_archived
unexpected persistence error → internal_error
```

---

# 19. Tests

Repository tests:

```text
creates workspace
finds workspace by id and owner
returns null for non-owner
lists only owner workspaces
finds by slug
updates by owner
```

Service tests:

```text
createWorkspace creates workspace and settings
createWorkspace uses actor_id as owner_user_id
createWorkspace rejects missing name
createWorkspace handles duplicate slug
listWorkspaces returns only actor-owned workspaces
getWorkspace rejects non-owner access
```

E2E tests:

```text
POST /api/v1/workspaces creates workspace
GET /api/v1/workspaces lists owned workspaces
GET /api/v1/workspaces/:workspace_id returns detail
non-owner cannot read workspace
invalid input returns canonical validation_error
```

---

# 20. Implementation Order

```text
1. Create directory tree
2. Create DTOs
3. Create mappers
4. Create repositories
5. Create WorkspaceStatusPolicy
6. Create WorkspaceSettingsService
7. Create WorkspaceService
8. Create controllers
9. Wire WorkspaceModule into AppModule
10. Add tests
11. Run typecheck/test/build
```

---

# 21. Verification Commands

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
GET /api/v1/workspaces
GET /api/v1/workspaces/:workspace_id
```

---

# 22. Acceptance Criteria

Workspace source implementation is accepted when:

- all workspace source files are defined;
- DTOs are defined;
- repositories are defined;
- services are defined;
- controllers are defined;
- transaction behavior is defined;
- authorization behavior is defined;
- error mappings are defined;
- tests are defined;
- implementation order is documented;
- verification commands are documented.

---

# 23. Final Statement

```text
Create Workspace Source defines the concrete source-code implementation plan for the Bizzi Workspace module.
```

This document authorizes creation of the actual Workspace source files in the backend codebase.