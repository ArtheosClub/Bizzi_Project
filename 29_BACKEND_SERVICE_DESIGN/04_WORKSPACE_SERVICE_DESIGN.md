# 04_WORKSPACE_SERVICE_DESIGN.md

# Bizzi Platform

## Workspace Service Design

**Layer:** 29_BACKEND_SERVICE_DESIGN  
**Component Type:** Backend Service Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 03_WORKSPACE_RUNTIME.md  
**Domain Reference:** 26_DOMAIN_MODEL / 02_WORKSPACE_DOMAIN.md  
**Data Model Reference:** 27_DATA_MODEL / 04_WORKSPACE_DATA_MODEL.md  
**API Contracts Reference:** 28_API_CONTRACTS / 03_WORKSPACE_API.md  
**Previous Document:** 03_CONTROLLER_SERVICE_REPOSITORY_PATTERN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the backend service design for workspace-related behavior in Bizzi Platform.

It specifies the service boundaries, repositories, validation rules, authorization rules, transaction patterns, audit events and runtime events required to implement the Workspace API.

Core question:

```text
How should Bizzi backend services implement workspace creation, configuration, access and lifecycle management safely and consistently?
```

---

# 2. Service Scope

This design covers:

```text
WorkspaceService
WorkspaceSettingsService
WorkspaceAccessService
Identity workspace discovery support
```

Primary API references:

```text
GET /api/v1/me
GET /api/v1/me/workspaces
GET /api/v1/workspaces
POST /api/v1/workspaces
GET /api/v1/workspaces/{workspace_id}
PATCH /api/v1/workspaces/{workspace_id}
POST /api/v1/workspaces/{workspace_id}/archive
GET /api/v1/workspaces/{workspace_id}/workspace-settings
PATCH /api/v1/workspaces/{workspace_id}/workspace-settings
GET /api/v1/workspaces/{workspace_id}/workspace-access
POST /api/v1/workspaces/{workspace_id}/workspace-access
POST /api/v1/workspaces/{workspace_id}/workspace-access/{workspace_access_id}/revoke
```

Primary data references:

```text
users
company_workspaces
workspace_settings
workspace_access
```

---

# 3. Module Ownership

Workspace behavior belongs to:

```text
WorkspaceModule
```

Supporting modules:

```text
IdentityModule
AuthorizationModule
ValidationModule
AuditModule
EventModule
TransactionModule
```

Rule:

```text
WorkspaceModule owns workspace lifecycle and settings. AuthorizationModule owns access decisions.
```

---

# 4. Service Responsibilities

## WorkspaceService

Responsibilities:

```text
create workspace
list accessible workspaces
get workspace details
update workspace mutable fields
archive workspace
validate workspace state
emit workspace audit events
emit workspace runtime events
```

## WorkspaceSettingsService

Responsibilities:

```text
create default workspace settings
read workspace settings
update workspace settings
validate settings values
emit settings audit and runtime events
```

## WorkspaceAccessService

Responsibilities:

```text
list workspace access records
grant workspace access
update workspace role later
revoke workspace access
protect last owner
support future role expansion
emit access audit and runtime events
```

---

# 5. Repository Responsibilities

## WorkspaceRepository

Methods:

```text
createWorkspace(data)
findById(workspace_id)
findByIdForActor(workspace_id, actor_id)
listForOwner(actor_id, filters, pagination)
listForActor(actor_id, filters, pagination)
updateById(workspace_id, patch)
archiveById(workspace_id, archive_data)
slugExists(slug)
```

## WorkspaceSettingsRepository

Methods:

```text
createDefaultSettings(workspace_id, settings)
findByWorkspaceId(workspace_id)
updateByWorkspaceId(workspace_id, patch)
```

## WorkspaceAccessRepository

Methods:

```text
listByWorkspace(workspace_id, filters, pagination)
findByIdAndWorkspace(workspace_access_id, workspace_id)
findActiveAccess(workspace_id, user_id)
createAccess(data)
updateAccess(workspace_access_id, patch)
revokeAccess(workspace_access_id, revoke_data)
countActiveOwners(workspace_id)
```

---

# 6. Service Context

Every workspace service method should receive a context object.

Recommended context:

```text
actor_id
actor_type
workspace_id optional for global workspace creation/listing
correlation_id
request_id
idempotency_key optional
```

Workspace creation is the main exception where `workspace_id` does not exist yet.

---

# 7. Workspace Creation Flow

## Service Method

```text
WorkspaceService.createWorkspace(context, input)
```

## Input

```text
name
slug optional
description optional
timezone optional
locale optional
```

## Flow

```text
validate authenticated actor
validate name
validate slug or generate slug
validate timezone if provided
validate locale if provided
begin transaction
create company_workspace
create default workspace_settings
create owner workspace_access record when access table is enabled
record workspace.created audit event
record workspace_settings.created audit event
emit workspace.created runtime event
commit transaction
return workspace DTO
```

## Transaction Boundary

The transaction should include:

```text
company_workspaces insert
workspace_settings insert
workspace_access owner insert when enabled
audit events
runtime event
```

---

# 8. Workspace Creation Validation

Validation rules:

```text
actor must be authenticated
name is required
name must not be empty
slug must be unique if supplied
slug may be generated from name if omitted
timezone must be valid if supplied
locale must be valid if supplied
initial status should be created or active according to implementation choice
onboarding_status should default to not_started
```

Error mappings:

```text
missing name → validation_error
invalid timezone → validation_error
invalid locale → validation_error
slug already exists → conflict
unauthenticated actor → unauthenticated
```

---

# 9. List Workspaces Flow

## Service Method

```text
WorkspaceService.listWorkspacesForActor(context, filters, pagination)
```

## Flow

```text
validate authenticated actor
resolve authorization mode
if MVP owner-only, list workspaces where owner_user_id = actor_id
if workspace_access enabled, list active workspace_access records for actor
apply filters
apply pagination
return workspace summary DTOs
```

## Authorization

```text
Authenticated user only.
```

## Notes

This flow may be used by:

```text
GET /api/v1/workspaces
GET /api/v1/me/workspaces
```

---

# 10. Get Workspace Flow

## Service Method

```text
WorkspaceService.getWorkspace(context, workspace_id)
```

## Flow

```text
validate authenticated actor
load workspace
check actor has workspace access
return workspace DTO
```

## Error Mappings

```text
workspace not found → not_found
actor lacks access → forbidden or not_found according to security mode
workspace archived → returned with status archived for read unless hidden by policy
```

---

# 11. Update Workspace Flow

## Service Method

```text
WorkspaceService.updateWorkspace(context, workspace_id, input)
```

## Mutable Fields

```text
name
description
onboarding_status
```

## Flow

```text
validate authenticated actor
load workspace by id
check workspace is not archived
check update permission
validate mutable fields
capture before_state
begin transaction
update workspace
record workspace.updated audit event
emit workspace.updated runtime event
commit transaction
return workspace DTO
```

## Authorization

MVP:

```text
workspace owner only
```

Expansion:

```text
owner or admin
```

---

# 12. Archive Workspace Flow

## Service Method

```text
WorkspaceService.archiveWorkspace(context, workspace_id, input)
```

## Input

```text
archive_reason optional
```

## Flow

```text
validate authenticated actor
load workspace
check archive permission
check workspace is not already archived
capture before_state
begin transaction
set status archived
set archived_at
record workspace.archived audit event
emit workspace.archived runtime event
commit transaction
return archived workspace DTO
```

## Rule

```text
Archiving a workspace must not hard-delete operating history.
```

---

# 13. Workspace Settings Read Flow

## Service Method

```text
WorkspaceSettingsService.getSettings(context, workspace_id)
```

## Flow

```text
validate authenticated actor
check workspace access
load settings by workspace_id
if missing, create default settings only through controlled repair flow
return settings DTO
```

---

# 14. Workspace Settings Update Flow

## Service Method

```text
WorkspaceSettingsService.updateSettings(context, workspace_id, input)
```

## Mutable Fields

```text
timezone
locale
ai_assistance_enabled
memory_enabled
audit_enabled
```

## Flow

```text
validate authenticated actor
load workspace
check workspace is not archived
check settings update permission
validate timezone if provided
validate locale if provided
validate boolean fields
capture before_state
begin transaction
update workspace_settings
record workspace_settings.updated audit event
emit workspace_settings.updated runtime event
commit transaction
return settings DTO
```

## Important Rule

```text
Disabling audit_enabled must not disable mandatory platform audit events unless a later compliance design explicitly allows scoped audit reduction.
```

---

# 15. Workspace Access List Flow

## Service Method

```text
WorkspaceAccessService.listAccess(context, workspace_id, filters, pagination)
```

## Flow

```text
validate authenticated actor
check workspace access management or admin permission
list access records by workspace
apply filters
apply pagination
return access DTOs
```

MVP may omit this endpoint or restrict to owner.

---

# 16. Grant Workspace Access Flow

## Service Method

```text
WorkspaceAccessService.grantAccess(context, workspace_id, input)
```

## Input

```text
user_id
role
```

## Flow

```text
validate authenticated actor
load workspace
check grant access permission
validate target user exists
validate role
check active access does not already exist
begin transaction
create workspace_access record
record workspace_access.granted audit event
emit access.granted runtime event
commit transaction
return access DTO
```

## Authorization

MVP:

```text
workspace owner only
```

Expansion:

```text
owner or admin
```

---

# 17. Revoke Workspace Access Flow

## Service Method

```text
WorkspaceAccessService.revokeAccess(context, workspace_id, workspace_access_id, input)
```

## Input

```text
revocation_reason optional
```

## Flow

```text
validate authenticated actor
load workspace access record by workspace_id
check revoke access permission
if target role is owner, check last-owner protection
begin transaction
set access status revoked
set revoked_at
record workspace_access.revoked audit event
emit access.revoked runtime event
commit transaction
return revoked access DTO
```

## Rule

```text
The last active owner cannot be revoked without ownership transfer or replacement owner creation.
```

---

# 18. Authorization Rules

Workspace service authorization matrix:

| Operation | MVP Rule | Expansion Rule |
|---|---|---|
| Create workspace | authenticated user | authenticated user |
| List workspaces | owner workspaces | active workspace_access |
| Get workspace | owner | active workspace_access |
| Update workspace | owner | owner/admin |
| Archive workspace | owner | owner/admin |
| Get settings | owner | active workspace_access |
| Update settings | owner | owner/admin |
| List access | owner | owner/admin |
| Grant access | owner | owner/admin |
| Revoke access | owner | owner/admin with last-owner protection |

---

# 19. Audit Events

Workspace services should emit:

```text
workspace.created
workspace.updated
workspace.archived
workspace_settings.created
workspace_settings.updated
workspace_access.granted
workspace_access.updated
workspace_access.revoked
```

Audit payload should include:

```text
workspace_id
actor_id
actor_type
object_type
object_id
action
before_state optional
after_state optional
correlation_id
```

---

# 20. Runtime Events

Workspace services should emit:

```text
workspace.created
workspace.updated
workspace.archived
workspace_settings.updated
access.granted
access.updated
access.revoked
```

Runtime events may trigger:

```text
dashboard refresh
access cache invalidation later
notification later
onboarding workflow later
```

---

# 21. Response DTOs

Workspace DTO:

```json
{
  "id": "uuid",
  "name": "Bizzi Demo Company",
  "slug": "bizzi-demo-company",
  "description": "Workspace description",
  "status": "active",
  "onboarding_status": "completed",
  "owner_user_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:15:00Z"
}
```

Settings DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "timezone": "Europe/Sofia",
  "locale": "en-US",
  "ai_assistance_enabled": true,
  "memory_enabled": true,
  "audit_enabled": true,
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:15:00Z"
}
```

Access DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "user_id": "uuid",
  "role": "owner",
  "status": "active",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:15:00Z"
}
```

---

# 22. Error Mapping

Workspace service errors:

```text
Unauthenticated → unauthenticated
WorkspaceNotFound → not_found
WorkspaceAccessDenied → forbidden
WorkspaceArchived → workspace_archived
InvalidWorkspaceName → validation_error
InvalidSlug → validation_error
SlugConflict → conflict
InvalidTimezone → validation_error
InvalidLocale → validation_error
InvalidRole → validation_error
AccessAlreadyExists → conflict
LastOwnerProtected → business_rule_violation
```

---

# 23. MVP Simplifications

MVP may simplify by:

```text
owner-only access control
single owner per workspace
automatic workspace settings creation
simple workspace statuses
omitting full workspace access management UI
using company_workspaces.owner_user_id for access checks
```

MVP must preserve:

```text
workspace isolation
audit events for create/update/archive
settings validation
no hard-delete of workspace history
structured error mapping
```

---

# 24. Future Expansion

Future service expansion may add:

```text
workspace invitations
workspace member management
role-based access control
ownership transfer
workspace deletion request workflow
workspace compliance settings
workspace billing profile
workspace data residency settings
access review workflows
workspace templates
```

---

# 25. Testing Expectations

Service tests should cover:

```text
workspace creation creates settings
workspace creation emits audit and runtime events
slug uniqueness validation
workspace update rejects archived workspace
archive preserves history
settings update validates timezone and locale
grant access prevents duplicate active access
revoke access protects last owner
authorization rejects non-owner in MVP
errors map to canonical API errors
```

Repository tests should cover:

```text
list workspaces for owner
list workspaces for access record
find workspace by id
update settings by workspace_id
count active owners
workspace access pagination
```

---

# 26. Acceptance Criteria

Workspace Service Design is accepted when:

- WorkspaceService responsibilities are defined;
- WorkspaceSettingsService responsibilities are defined;
- WorkspaceAccessService responsibilities are defined;
- repository methods are identified;
- create, read, update and archive flows are documented;
- settings flows are documented;
- access grant/revoke flows are documented;
- authorization matrix is defined;
- audit and runtime event expectations are defined;
- response DTOs and error mappings are documented;
- MVP simplifications and test expectations are documented.

Status:

```text
Accepted for Operating Map Service Design
```

---

# 27. Final Statement

```text
Bizzi Workspace Service Design defines how backend services create, configure, protect and govern workspaces through transactional, auditable and workspace-safe service behavior.
```

This service layer is the foundation for all workspace-scoped Bizzi operations.