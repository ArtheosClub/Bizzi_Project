# 03_WORKSPACE_API.md

# Bizzi Platform

## Workspace API

**Layer:** 28_API_CONTRACTS  
**Component Type:** API Contract Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 03_WORKSPACE_RUNTIME.md  
**Domain Reference:** 26_DOMAIN_MODEL / 02_WORKSPACE_DOMAIN.md  
**Data Model Reference:** 27_DATA_MODEL / 04_WORKSPACE_DATA_MODEL.md  
**Previous Document:** 02_API_RESOURCE_CATALOG.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Workspace API contract for Bizzi Platform.

The Workspace API exposes the identity, workspace and workspace settings operations needed to create, read, configure, archive and access a Bizzi company workspace.

Core question:

```text
How should Bizzi expose workspace identity, workspace configuration and workspace access through stable, secure and implementation-ready API contracts?
```

---

# 2. API Scope

This document covers the following API resources:

```text
me
workspaces
workspace-settings
workspace-access
```

Primary data model references:

```text
users
sessions
company_workspaces
workspace_settings
workspace_access
```

MVP scope:

```text
me
workspaces
workspace-settings
```

Near-MVP scope:

```text
workspace-access
```

---

# 3. Design Principles Applied

The Workspace API follows:

```text
Workspace First
Resource-Oriented Contracts
Stable Field Names
Predictable CRUD
Audit-Aware Mutations
Least Privilege Authorization
Safe Defaults
OpenAPI Readiness
```

---

# 4. Base Paths

Global user and workspace discovery paths:

```text
/api/v1/me
/api/v1/workspaces
```

Workspace-scoped paths:

```text
/api/v1/workspaces/{workspace_id}
/api/v1/workspaces/{workspace_id}/workspace-settings
/api/v1/workspaces/{workspace_id}/workspace-access
```

---

# 5. Resource: Current User

## Resource Name

```text
me
```

## Purpose

Expose the authenticated user profile and workspace access summary.

## Data Model Reference

```text
users
workspace_access
company_workspaces
```

## Endpoint

```text
GET /api/v1/me
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "email": "user@example.com",
  "display_name": "Andrew",
  "status": "active",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

## Authorization

```text
Authenticated user only.
```

## Audit

No audit event required for normal read.

---

# 6. Resource: User Workspaces

## Endpoint

```text
GET /api/v1/me/workspaces
```

## Purpose

Return workspaces available to the authenticated user.

## Response: 200 OK

```json
{
  "items": [
    {
      "id": "uuid",
      "name": "Bizzi Demo Company",
      "slug": "bizzi-demo-company",
      "status": "active",
      "role": "owner",
      "onboarding_status": "completed",
      "created_at": "2026-07-01T09:00:00Z",
      "updated_at": "2026-07-01T09:15:00Z"
    }
  ],
  "next_page_token": null
}
```

## Authorization

```text
Authenticated user only.
```

## Notes

MVP may derive available workspaces from:

```text
company_workspaces.owner_user_id
```

Near-MVP may derive from:

```text
workspace_access
```

---

# 7. Resource: Workspaces

## Resource Name

```text
workspaces
```

## Purpose

Create and manage company workspace records.

## Data Model Reference

```text
company_workspaces
workspace_settings
workspace_access
```

---

# 8. Endpoint: List Workspaces

## Method and Path

```text
GET /api/v1/workspaces
```

## Purpose

List workspaces accessible to the authenticated user.

## Query Parameters

```text
status optional
page_size optional
page_token optional
sort optional
```

## Response: 200 OK

```json
{
  "items": [
    {
      "id": "uuid",
      "name": "Bizzi Demo Company",
      "slug": "bizzi-demo-company",
      "status": "active",
      "onboarding_status": "completed",
      "owner_user_id": "uuid",
      "created_at": "2026-07-01T09:00:00Z",
      "updated_at": "2026-07-01T09:15:00Z"
    }
  ],
  "next_page_token": null
}
```

## Authorization

```text
Authenticated user only.
```

---

# 9. Endpoint: Create Workspace

## Method and Path

```text
POST /api/v1/workspaces
```

## Purpose

Create a new company workspace for the authenticated user.

## Request Body

```json
{
  "name": "Bizzi Demo Company",
  "slug": "bizzi-demo-company",
  "description": "Workspace for company operating system design",
  "timezone": "Europe/Sofia",
  "locale": "en-US"
}
```

## Required Fields

```text
name
```

## Optional Fields

```text
slug
description
timezone
locale
```

## Response: 201 Created

```json
{
  "id": "uuid",
  "name": "Bizzi Demo Company",
  "slug": "bizzi-demo-company",
  "description": "Workspace for company operating system design",
  "status": "created",
  "onboarding_status": "not_started",
  "owner_user_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

## Validation Rules

```text
name is required
slug must be unique if provided
slug may be generated if omitted
timezone must be valid if provided
locale must be valid if provided
```

## Authorization

```text
Authenticated user only.
```

## Audit Events

```text
workspace.created
workspace_settings.created
```

## Runtime Events

```text
workspace.created
```

---

# 10. Endpoint: Get Workspace

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}
```

## Purpose

Retrieve workspace details.

## Response: 200 OK

```json
{
  "id": "uuid",
  "name": "Bizzi Demo Company",
  "slug": "bizzi-demo-company",
  "description": "Workspace for company operating system design",
  "status": "active",
  "onboarding_status": "completed",
  "owner_user_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:15:00Z"
}
```

## Authorization

```text
User must have access to workspace.
```

---

# 11. Endpoint: Update Workspace

## Method and Path

```text
PATCH /api/v1/workspaces/{workspace_id}
```

## Purpose

Update mutable workspace fields.

## Request Body

```json
{
  "name": "Bizzi Operating Company",
  "description": "Updated workspace description",
  "onboarding_status": "in_progress"
}
```

## Mutable Fields

```text
name
description
onboarding_status
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "name": "Bizzi Operating Company",
  "slug": "bizzi-demo-company",
  "description": "Updated workspace description",
  "status": "active",
  "onboarding_status": "in_progress",
  "owner_user_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

## Validation Rules

```text
name cannot be empty if provided
onboarding_status must be valid
archived workspaces cannot be updated through normal update flow
```

## Authorization

```text
Workspace owner or authorized admin.
```

## Audit Events

```text
workspace.updated
```

## Runtime Events

```text
workspace.updated
```

---

# 12. Endpoint: Archive Workspace

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/archive
```

## Purpose

Archive a workspace and remove it from active operation flows.

## Request Body

```json
{
  "archive_reason": "Company workspace no longer active"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "status": "archived",
  "archived_at": "2026-07-01T12:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

## Authorization

```text
Workspace owner only in MVP.
```

## Audit Events

```text
workspace.archived
```

## Runtime Events

```text
workspace.archived
```

## Notes

Archiving should not immediately delete workspace operating history.

---

# 13. Resource: Workspace Settings

## Resource Name

```text
workspace-settings
```

## Purpose

Manage workspace configuration such as locale, timezone, AI settings, memory settings and audit settings.

## Data Model Reference

```text
workspace_settings
```

---

# 14. Endpoint: Get Workspace Settings

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/workspace-settings
```

## Response: 200 OK

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
  "updated_at": "2026-07-01T09:00:00Z"
}
```

## Authorization

```text
User must have access to workspace.
```

---

# 15. Endpoint: Update Workspace Settings

## Method and Path

```text
PATCH /api/v1/workspaces/{workspace_id}/workspace-settings
```

## Request Body

```json
{
  "timezone": "Europe/Sofia",
  "locale": "en-US",
  "ai_assistance_enabled": true,
  "memory_enabled": true,
  "audit_enabled": true
}
```

## Mutable Fields

```text
timezone
locale
ai_assistance_enabled
memory_enabled
audit_enabled
```

## Response: 200 OK

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
  "updated_at": "2026-07-01T10:00:00Z"
}
```

## Validation Rules

```text
timezone must be valid if provided
locale must be valid if provided
boolean fields must be boolean
at least one field must be supplied
```

## Authorization

```text
Workspace owner or authorized admin.
```

## Audit Events

```text
workspace_settings.updated
```

## Runtime Events

```text
workspace_settings.updated
```

---

# 16. Resource: Workspace Access

## Resource Name

```text
workspace-access
```

## Purpose

Manage access records for users inside a workspace.

## MVP Status

```text
Near-MVP / P2
```

## Data Model Reference

```text
workspace_access
```

## Notes

MVP may use `company_workspaces.owner_user_id` before full workspace access management is enabled.

---

# 17. Endpoint: List Workspace Access

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/workspace-access
```

## Response: 200 OK

```json
{
  "items": [
    {
      "id": "uuid",
      "workspace_id": "uuid",
      "user_id": "uuid",
      "role": "owner",
      "status": "active",
      "created_at": "2026-07-01T09:00:00Z",
      "updated_at": "2026-07-01T09:00:00Z"
    }
  ],
  "next_page_token": null
}
```

## Authorization

```text
Workspace owner or authorized admin.
```

---

# 18. Endpoint: Grant Workspace Access

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/workspace-access
```

## Request Body

```json
{
  "user_id": "uuid",
  "role": "member"
}
```

## Response: 201 Created

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "user_id": "uuid",
  "role": "member",
  "status": "active",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

## Validation Rules

```text
user_id is required
role is required
role must be valid
user must exist
workspace access record must not already exist as active
```

## Authorization

```text
Workspace owner or authorized admin.
```

## Audit Events

```text
workspace_access.granted
```

## Runtime Events

```text
access.granted
```

---

# 19. Endpoint: Revoke Workspace Access

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/workspace-access/{workspace_access_id}/revoke
```

## Request Body

```json
{
  "revocation_reason": "User no longer works on this workspace"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "user_id": "uuid",
  "role": "member",
  "status": "revoked",
  "revoked_at": "2026-07-01T12:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

## Authorization

```text
Workspace owner or authorized admin.
```

## Audit Events

```text
workspace_access.revoked
```

## Runtime Events

```text
access.revoked
```

---

# 20. Common Error Codes

Workspace API may return:

```text
unauthenticated
forbidden
not_found
validation_error
conflict
workspace_archived
invalid_status_transition
```

Example:

```json
{
  "error": {
    "code": "workspace_archived",
    "message": "Archived workspaces cannot be modified through this endpoint.",
    "correlation_id": "uuid"
  }
}
```

---

# 21. Authorization Matrix

| Operation | MVP Rule | Expansion Rule |
|---|---|---|
| Get current user | authenticated user | authenticated user |
| List workspaces | owner workspaces | active workspace_access |
| Create workspace | authenticated user | authenticated user |
| Read workspace | owner | active workspace_access |
| Update workspace | owner | owner/admin |
| Archive workspace | owner | owner/admin with policy |
| Read settings | owner | active workspace_access |
| Update settings | owner | owner/admin |
| Manage access | owner | owner/admin |

---

# 22. Audit and Runtime Event Summary

| API Operation | Audit Event | Runtime Event |
|---|---|---|
| Create workspace | workspace.created | workspace.created |
| Update workspace | workspace.updated | workspace.updated |
| Archive workspace | workspace.archived | workspace.archived |
| Update settings | workspace_settings.updated | workspace_settings.updated |
| Grant access | workspace_access.granted | access.granted |
| Revoke access | workspace_access.revoked | access.revoked |

---

# 23. MVP Simplifications

For MVP, Bizzi may simplify by:

- using owner-only workspace access;
- creating default workspace settings automatically;
- omitting full workspace-access management UI;
- allowing only one owner per workspace;
- using simple status values;
- deferring invitations and role permissions.

These simplifications must preserve workspace isolation and auditability.

---

# 24. Future Expansion

Future Workspace API may add:

```text
workspace invitations
workspace members
role-based access control
workspace billing profile
workspace compliance settings
workspace data export settings
workspace deletion request workflow
workspace transfer ownership
```

---

# 25. Acceptance Criteria

Workspace API is accepted when:

- current user endpoint is defined;
- workspace list/create/read/update/archive endpoints are defined;
- workspace settings read/update endpoints are defined;
- workspace access expansion endpoints are defined;
- request and response shapes are documented;
- validation rules are identified;
- authorization rules are defined;
- audit and runtime event expectations are defined;
- MVP simplifications are documented.

Status:

```text
Accepted for Operating Map API Design
```

---

# 26. Final Statement

```text
Bizzi Workspace API defines how users create, access, configure and govern company workspaces through stable, workspace-aware, auditable and implementation-ready API contracts.
```

This API is the entry point for all Bizzi operating behavior.