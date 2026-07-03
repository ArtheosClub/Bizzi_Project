# 05_WORKSPACE_MODULE_EXECUTION.md

# Bizzi Platform

## Workspace Module Execution

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
**Previous Document:** 04_IDENTITY_AUTH_EXECUTION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch III — Backend Execution

---

# 1. Purpose

This document defines the Workspace Module execution plan for Bizzi Platform backend MVP.

It specifies how to implement the first workspace-scoped product boundary: workspace creation, workspace listing, workspace details, workspace settings creation, owner-only access foundation and the first transactional mutation that will later emit audit and runtime events.

Core question:

```text
How should Bizzi implement the workspace module so every future backend feature has a safe tenant boundary and ownership context?
```

---

# 2. Workspace Module Thesis

```text
CompanyWorkspace is the primary tenant boundary of Bizzi. The workspace module must be implemented before task, decision, memory, audit, runtime and dashboard modules because every meaningful business object belongs to a workspace.
```

The module proves:

```text
workspace persistence
workspace ownership
workspace settings creation
owner-scoped listing
workspace detail read
workspace status handling
workspace_id path foundation
future authorization integration
transaction-ready creation flow
```

---

# 3. Target Directory Structure

Target structure:

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
│   ├── workspace.response.dto.ts
│   ├── workspace-settings.response.dto.ts
│   └── update-workspace-settings.dto.ts
├── mappers/
│   ├── workspace.mapper.ts
│   └── workspace-settings.mapper.ts
├── policies/
│   └── workspace-status.policy.ts
└── tests/
    ├── workspace.service.spec.ts
    ├── workspace.repository.spec.ts
    └── workspace.e2e-spec.ts
```

---

# 4. Execution Non-Scope

This execution step does not implement:

```text
full RBAC
workspace invitations
workspace members
billing ownership
organization hierarchy
team roles
workspace deletion
advanced onboarding workflow
operating map generation
agent setup
```

These belong to later modules.

---

# 5. Required API Routes

MVP routes:

```text
POST /api/v1/workspaces
GET /api/v1/workspaces
GET /api/v1/workspaces/{workspace_id}
```

P2 routes:

```text
PATCH /api/v1/workspaces/{workspace_id}
GET /api/v1/workspaces/{workspace_id}/workspace-settings
PATCH /api/v1/workspaces/{workspace_id}/workspace-settings
```

Rule:

```text
All workspace-scoped routes must receive workspace_id from path, not request body.
```

---

# 6. Data Models Used

Primary models:

```text
User
CompanyWorkspace
WorkspaceSettings
```

Relations:

```text
User.id → CompanyWorkspace.owner_user_id
CompanyWorkspace.id → WorkspaceSettings.workspace_id
```

Rule:

```text
Workspace ownership is determined by owner_user_id for MVP.
```

---

# 7. Create Workspace DTO

`CreateWorkspaceDto` should include:

```text
name required
slug optional
description optional
timezone optional
locale optional
```

Validation:

```text
name is required
slug must be URL-safe if provided
slug may be generated from name if absent
timezone must be valid if provided
locale must be valid if provided
```

Rule:

```text
owner_user_id must come from ServiceContext actor_id, not from request body.
```

---

# 8. Workspace Response DTO

`WorkspaceResponseDto` should include:

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

Must not include:

```text
internal database metadata
unvalidated settings payloads
future billing data
```

---

# 9. Workspace Settings DTO

`WorkspaceSettingsResponseDto` should include:

```text
id
workspace_id
timezone
locale
ai_assistance_enabled
memory_enabled
audit_enabled
created_at
updated_at
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

# 10. Workspace Repository

Required methods:

```text
create(db, data)
findById(db, id)
findByIdAndOwner(db, id, ownerUserId)
listByOwner(db, ownerUserId, pagination)
updateByIdAndOwner(db, id, ownerUserId, patch)
archiveByIdAndOwner(db, id, ownerUserId, data)
findBySlug(db, slug)
```

Rules:

```text
owner-scoped MVP reads must filter by owner_user_id
workspace-scoped feature repositories later must filter by workspace_id
repositories return records, not response DTOs
```

---

# 11. Workspace Settings Repository

Required methods:

```text
create(db, data)
findByWorkspaceId(db, workspaceId)
updateByWorkspaceId(db, workspaceId, patch)
```

Rules:

```text
settings are one-to-one with workspace
workspace_settings.workspace_id must be unique
settings creation should happen transactionally with workspace creation
```

---

# 12. Workspace Service

Required service methods:

```text
createWorkspace(context, input)
listWorkspaces(context, pagination)
getWorkspace(context, workspaceId)
updateWorkspace(context, workspaceId, input)
archiveWorkspace(context, workspaceId)
```

MVP methods:

```text
createWorkspace
listWorkspaces
getWorkspace
```

Service responsibilities:

```text
validate input
use actor_id as owner_user_id
create slug if needed
ensure slug uniqueness
create workspace and settings in transaction
return DTOs
raise canonical errors
```

---

# 13. Workspace Settings Service

Required service methods:

```text
getWorkspaceSettings(context, workspaceId)
updateWorkspaceSettings(context, workspaceId, input)
createDefaultSettingsForWorkspace(tx, workspaceId, input)
```

Rules:

```text
settings reads require workspace ownership
settings updates require workspace ownership
settings updates should record audit/runtime events after audit/event modules are available
```

---

# 14. Workspace Creation Flow

Canonical flow:

```text
POST /api/v1/workspaces
↓
WorkspaceController.createWorkspace
↓
WorkspaceService.createWorkspace
↓
validate ServiceContext actor
validate request input
normalize or generate slug
check slug uniqueness
begin transaction
create company_workspace
create workspace_settings
optional placeholder audit/event hooks
commit
return WorkspaceResponseDto
```

After audit/event execution is available, the flow becomes:

```text
create workspace
create settings
record workspace.created audit event
emit workspace.created runtime event
```

Rule:

```text
Workspace and default settings must be created atomically.
```

---

# 15. Workspace List Flow

Canonical flow:

```text
GET /api/v1/workspaces
↓
WorkspaceController.listWorkspaces
↓
WorkspaceService.listWorkspaces
↓
validate actor context
normalize pagination
WorkspaceRepository.listByOwner(actor_id)
map records to DTOs
return paginated response
```

Rule:

```text
MVP list must return only workspaces owned by the actor.
```

---

# 16. Workspace Detail Flow

Canonical flow:

```text
GET /api/v1/workspaces/{workspace_id}
↓
WorkspaceController.getWorkspace
↓
WorkspaceService.getWorkspace
↓
validate workspace_id
WorkspaceRepository.findByIdAndOwner(workspace_id, actor_id)
if missing → not_found or forbidden-safe not_found
map to DTO
return workspace
```

MVP security recommendation:

```text
Use not_found for unauthorized workspace id to reduce information leakage.
```

---

# 17. Workspace Status Policy

`WorkspaceStatusPolicy` should define:

```text
isActive(status)
canMutate(status)
canArchive(status)
```

Rules:

```text
active workspace allows normal mutation
archived workspace blocks mutations
archived workspace may still allow limited reads
```

---

# 18. Authorization Relationship

Before full AuthorizationModule is implemented, WorkspaceService may enforce owner-only access directly through repository filters.

After AuthorizationModule is implemented:

```text
WorkspaceService should use AuthorizationService.requireWorkspaceOwner(context)
```

Transition rule:

```text
Temporary owner filtering in WorkspaceService must be refactored into AuthorizationService once 06_AUTHORIZATION_VALIDATION_EXECUTION is implemented.
```

---

# 19. Audit and Runtime Event Hooks

Initial workspace module may define placeholders for later integration.

Required future events:

```text
workspace.created
workspace.updated
workspace.archived optional
workspace_settings.updated
```

Rules:

```text
audit/runtime event persistence is completed in 07_AUDIT_EVENT_EXECUTION.md
workspace creation flow must be designed so audit/event can be added without rewriting service boundaries
```

---

# 20. Error Handling

Required errors:

```text
unauthenticated
validation_error
conflict
not_found
workspace_archived
internal_error
```

Examples:

```text
missing name → validation_error
invalid slug → validation_error
duplicate slug → conflict
workspace not owned or missing → not_found
archived workspace mutation → workspace_archived
```

Rule:

```text
Raw Prisma unique constraint errors must be mapped to conflict.
```

---

# 21. Mapper Rules

`WorkspaceMapper.toDto(record)` should map:

```text
id
ownerUserId → owner_user_id
onboardingStatus → onboarding_status
createdAt → created_at
updatedAt → updated_at
archivedAt → archived_at
```

Rules:

```text
repositories return records
services return DTOs
controllers return DTOs from services
```

---

# 22. Tests Required

Repository tests:

```text
creates workspace
finds workspace by id and owner
returns null for non-owner
lists only owner workspaces
finds workspace by slug
updates workspace by owner
```

Service tests:

```text
createWorkspace creates workspace and settings
createWorkspace uses actor_id as owner_user_id
createWorkspace rejects missing name
createWorkspace handles duplicate slug
listWorkspaces returns only actor-owned workspaces
getWorkspace rejects non-owner access
archived workspace blocks mutation later
```

API tests:

```text
POST /api/v1/workspaces creates workspace
GET /api/v1/workspaces lists owned workspaces
GET /api/v1/workspaces/{workspace_id} returns detail
non-owner cannot read workspace
invalid input returns canonical validation_error
```

---

# 23. Execution Order

Recommended execution order:

```text
1. Create workspace module folders
2. Create DTOs
3. Create mappers
4. Create repositories
5. Create WorkspaceSettingsService
6. Create WorkspaceService
7. Create WorkspaceController
8. Create WorkspaceSettingsController optional P2
9. Wire WorkspaceModule into AppModule
10. Add repository tests
11. Add service tests
12. Add API/e2e tests
13. Verify typecheck/test/build
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
pnpm dev
```

Manual smoke sequence:

```text
GET /api/v1/me
POST /api/v1/workspaces
GET /api/v1/workspaces
GET /api/v1/workspaces/{workspace_id}
```

---

# 25. Risks and Controls

## Risk 1 — Workspace Creation Without Settings

Mitigation:

```text
Create workspace and settings in one transaction.
```

## Risk 2 — Owner ID Accepted From Request Body

Mitigation:

```text
Owner always comes from ServiceContext actor_id.
```

## Risk 3 — Workspace Access Leaks

Mitigation:

```text
Use owner-scoped repository reads and tests for non-owner access.
```

## Risk 4 — Slug Conflict Not Handled

Mitigation:

```text
Check uniqueness and map database conflict to canonical conflict error.
```

---

# 26. Acceptance Criteria

Workspace Module Execution is accepted when:

- target directory structure is defined;
- execution non-scope is documented;
- required API routes are defined;
- data models and relations are documented;
- DTOs are defined;
- repositories are defined;
- services are defined;
- workspace creation, list and detail flows are documented;
- workspace status policy is defined;
- authorization transition is documented;
- audit/runtime hooks are documented;
- error handling is defined;
- mapper rules are defined;
- tests are specified;
- execution order and verification commands are documented;
- risks and controls are documented.

Status:

```text
Accepted for Authorization Validation Execution
```

---

# 27. Final Statement

```text
Bizzi Workspace Module Execution defines the first tenant boundary implementation for the backend MVP.
```

This module establishes the workspace ownership and settings foundation required before task, decision, memory, audit, runtime and dashboard execution can safely proceed.