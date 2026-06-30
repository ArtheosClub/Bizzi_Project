# 08_INTEGRATION_SECURITY_API.md

# Bizzi Platform

## Integration Security API

**Layer:** 28_API_CONTRACTS  
**Component Type:** API Contract Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 11_INTEGRATION_RUNTIME.md, 12_RUNTIME_SECURITY.md  
**Domain Reference:** 26_DOMAIN_MODEL / 11_INTEGRATION_AND_SECURITY_DOMAIN.md  
**Data Model Reference:** 27_DATA_MODEL / 09_INTEGRATION_SECURITY_DATA_MODEL.md  
**Previous Document:** 07_MEMORY_AUDIT_EVENT_API.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Integration and Security API contracts for Bizzi Platform.

These APIs expose controlled external connectivity, integration lifecycle, sync jobs, workspace access and security policy management.

Core question:

```text
How should Bizzi expose integrations and security controls through stable, workspace-scoped, auditable and safe API contracts?
```

---

# 2. API Scope

This document covers:

```text
integrations
integration-sync-jobs
security-policies
workspace-access
```

Primary data model references:

```text
integrations
integration_sync_jobs
security_policies
workspace_access
```

MVP scope:

```text
workspace-access read/owner model
security-policies baseline read
```

Near-MVP / P2 scope:

```text
integrations
integration-sync-jobs
security-policies management
workspace-access management
```

---

# 3. Design Principles Applied

This API follows:

```text
Workspace First
Resource-Oriented Contracts
Least Privilege Authorization
Audit-Aware Mutations
Runtime Event Awareness
Safe Defaults
Credential Reference Only
OpenAPI Readiness
```

---

# 4. Base Paths

Workspace-scoped paths:

```text
/api/v1/workspaces/{workspace_id}/integrations
/api/v1/workspaces/{workspace_id}/integration-sync-jobs
/api/v1/workspaces/{workspace_id}/security-policies
/api/v1/workspaces/{workspace_id}/workspace-access
```

Rule:

```text
Integration and security resources are workspace-scoped unless explicitly global identity infrastructure.
```

---

# 5. Security Boundary

APIs in this document must never expose raw secrets.

Allowed:

```text
credential_ref
provider
status
scopes
last_sync_at
revoked_at
```

Not allowed:

```text
access_token
refresh_token
api_key
client_secret
password
private_key
raw credential payload
```

Rule:

```text
Secret values belong in secure secret storage, not API responses or normal runtime tables.
```

---

# 6. Resource: Integrations

## Resource Name

```text
integrations
```

## Purpose

Represent external provider connections configured for a workspace.

## Data Model Reference

```text
integrations
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "provider": "github",
  "integration_type": "repository",
  "name": "GitHub Repository Integration",
  "status": "active",
  "credential_ref": "secret_ref",
  "scopes": ["repo:read", "repo:write"],
  "configuration": {},
  "last_sync_at": "2026-07-01T12:00:00Z",
  "revoked_at": null,
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

---

# 7. Endpoint: List Integrations

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/integrations
```

## Query Parameters

```text
status optional
provider optional
integration_type optional
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
      "workspace_id": "uuid",
      "provider": "github",
      "integration_type": "repository",
      "name": "GitHub Repository Integration",
      "status": "active",
      "scopes": ["repo:read", "repo:write"],
      "last_sync_at": "2026-07-01T12:00:00Z",
      "created_at": "2026-07-01T09:00:00Z"
    }
  ],
  "next_page_token": null
}
```

## Authorization

```text
Workspace owner, admin or authorized integration manager.
```

---

# 8. Endpoint: Create Integration

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/integrations
```

## Request Body

```json
{
  "provider": "github",
  "integration_type": "repository",
  "name": "GitHub Repository Integration",
  "credential_ref": "secret_ref",
  "scopes": ["repo:read", "repo:write"],
  "configuration": {
    "repository_full_name": "ArtheosClub/Bizzi_Project"
  }
}
```

## Required Fields

```text
provider
integration_type
name
credential_ref
```

## Response: 201 Created

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "provider": "github",
  "integration_type": "repository",
  "name": "GitHub Repository Integration",
  "status": "active",
  "scopes": ["repo:read", "repo:write"],
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

## Validation Rules

```text
provider must be supported
integration_type must be valid
credential_ref must refer to secure secret storage
scopes must be allowed for provider and workspace
configuration must match provider schema
raw credentials must not be accepted in request body
```

## Audit Events

```text
integration.created
```

## Runtime Events

```text
integration.created
```

---

# 9. Endpoint: Get Integration

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/integrations/{integration_id}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "provider": "github",
  "integration_type": "repository",
  "name": "GitHub Repository Integration",
  "status": "active",
  "credential_ref": "secret_ref",
  "scopes": ["repo:read", "repo:write"],
  "configuration": {
    "repository_full_name": "ArtheosClub/Bizzi_Project"
  },
  "last_sync_at": "2026-07-01T12:00:00Z",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

## Rule

```text
Responses must not include raw secret values.
```

---

# 10. Endpoint: Update Integration

## Method and Path

```text
PATCH /api/v1/workspaces/{workspace_id}/integrations/{integration_id}
```

## Request Body

```json
{
  "name": "Primary GitHub Integration",
  "configuration": {
    "repository_full_name": "ArtheosClub/Bizzi_Project"
  },
  "scopes": ["repo:read", "repo:write"]
}
```

## Mutable Fields

```text
name
configuration
scopes
metadata
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "name": "Primary GitHub Integration",
  "status": "active",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

## Audit Events

```text
integration.updated
```

## Runtime Events

```text
integration.updated
```

---

# 11. Endpoint: Trigger Integration Sync

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/integrations/{integration_id}/sync
```

## Request Body

```json
{
  "sync_type": "manual",
  "idempotency_key": "client-generated-key"
}
```

## Response: 202 Accepted

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "integration_id": "uuid",
  "sync_type": "manual",
  "status": "queued",
  "created_at": "2026-07-01T12:00:00Z"
}
```

## Validation Rules

```text
integration must belong to workspace
integration must be active
sync_type must be valid
caller must have integration sync permission
idempotency key should prevent duplicate sync jobs when supplied
```

## Audit Events

```text
integration.sync_requested
```

## Runtime Events

```text
integration.sync_requested
integration.sync_queued
```

---

# 12. Endpoint: Revoke Integration

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/integrations/{integration_id}/revoke
```

## Request Body

```json
{
  "revocation_reason": "Integration no longer required"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "revoked",
  "revoked_at": "2026-07-01T12:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

## Audit Events

```text
integration.revoked
```

## Runtime Events

```text
integration.revoked
```

---

# 13. Resource: Integration Sync Jobs

## Resource Name

```text
integration-sync-jobs
```

## Purpose

Represent integration synchronization jobs and their execution state.

## Data Model Reference

```text
integration_sync_jobs
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "integration_id": "uuid",
  "sync_type": "manual",
  "status": "completed",
  "started_at": "2026-07-01T12:00:00Z",
  "completed_at": "2026-07-01T12:01:00Z",
  "error_message": null,
  "created_at": "2026-07-01T12:00:00Z",
  "updated_at": "2026-07-01T12:01:00Z"
}
```

---

# 14. Endpoint: List Integration Sync Jobs

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/integration-sync-jobs
```

## Query Parameters

```text
integration_id optional
status optional
sync_type optional
from_timestamp optional
to_timestamp optional
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
      "workspace_id": "uuid",
      "integration_id": "uuid",
      "sync_type": "manual",
      "status": "completed",
      "started_at": "2026-07-01T12:00:00Z",
      "completed_at": "2026-07-01T12:01:00Z"
    }
  ],
  "next_page_token": null
}
```

---

# 15. Endpoint: Get Integration Sync Job

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/integration-sync-jobs/{sync_job_id}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "integration_id": "uuid",
  "sync_type": "manual",
  "status": "completed",
  "started_at": "2026-07-01T12:00:00Z",
  "completed_at": "2026-07-01T12:01:00Z",
  "error_message": null,
  "metadata": {}
}
```

---

# 16. Resource: Security Policies

## Resource Name

```text
security-policies
```

## Purpose

Represent workspace-level security and AI action policies.

## Data Model Reference

```text
security_policies
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "policy_type": "ai_action_policy",
  "name": "Human Confirmation Required",
  "status": "active",
  "rules": {
    "requires_human_confirmation": true,
    "restricted_actions": ["delete", "external_send"]
  },
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

---

# 17. Endpoint: List Security Policies

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/security-policies
```

## Query Parameters

```text
status optional
policy_type optional
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
      "workspace_id": "uuid",
      "policy_type": "ai_action_policy",
      "name": "Human Confirmation Required",
      "status": "active",
      "created_at": "2026-07-01T09:00:00Z"
    }
  ],
  "next_page_token": null
}
```

---

# 18. Endpoint: Create Security Policy

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/security-policies
```

## Request Body

```json
{
  "policy_type": "ai_action_policy",
  "name": "Human Confirmation Required",
  "rules": {
    "requires_human_confirmation": true,
    "restricted_actions": ["delete", "external_send"]
  }
}
```

## Required Fields

```text
policy_type
name
rules
```

## Response: 201 Created

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "policy_type": "ai_action_policy",
  "name": "Human Confirmation Required",
  "status": "active",
  "created_at": "2026-07-01T09:00:00Z"
}
```

## Validation Rules

```text
policy_type must be valid
rules must match policy schema
policy must not weaken mandatory platform safety rules
```

## Audit Events

```text
security_policy.created
```

## Runtime Events

```text
security_policy.created
```

---

# 19. Endpoint: Update Security Policy

## Method and Path

```text
PATCH /api/v1/workspaces/{workspace_id}/security-policies/{policy_id}
```

## Request Body

```json
{
  "name": "Updated Human Confirmation Policy",
  "rules": {
    "requires_human_confirmation": true,
    "restricted_actions": ["delete", "external_send", "credential_change"]
  }
}
```

## Audit Events

```text
security_policy.updated
```

## Runtime Events

```text
security_policy.updated
```

---

# 20. Endpoint: Archive Security Policy

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/security-policies/{policy_id}/archive
```

## Request Body

```json
{
  "archive_reason": "Superseded by stricter policy"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "archived",
  "archived_at": "2026-07-01T12:00:00Z"
}
```

## Audit Events

```text
security_policy.archived
```

## Runtime Events

```text
security_policy.archived
```

---

# 21. Resource: Workspace Access

## Resource Name

```text
workspace-access
```

## Purpose

Represent user access to a workspace and the role assigned to that user.

## Data Model Reference

```text
workspace_access
```

## Note

Workspace Access also appears in `03_WORKSPACE_API.md`. This section focuses on security governance and authorization behavior.

---

# 22. Workspace Access Endpoints

Key endpoints:

```text
GET /api/v1/workspaces/{workspace_id}/workspace-access
POST /api/v1/workspaces/{workspace_id}/workspace-access
PATCH /api/v1/workspaces/{workspace_id}/workspace-access/{workspace_access_id}
POST /api/v1/workspaces/{workspace_id}/workspace-access/{workspace_access_id}/revoke
```

Required security rules:

```text
only owner/admin can grant access
role must be valid
user must exist
access changes must be audited
revoked access must preserve access history
last owner cannot be revoked without ownership transfer
```

Audit events:

```text
workspace_access.granted
workspace_access.updated
workspace_access.revoked
```

Runtime events:

```text
access.granted
access.updated
access.revoked
```

---

# 23. Common Error Codes

Integration Security API may return:

```text
unauthenticated
forbidden
not_found
validation_error
conflict
workspace_archived
invalid_provider
invalid_scope
invalid_policy
invalid_credential_ref
credential_value_not_allowed
integration_revoked
sync_already_running
last_owner_protected
```

Example:

```json
{
  "error": {
    "code": "credential_value_not_allowed",
    "message": "Raw credential values are not allowed in this API contract. Use credential_ref instead.",
    "correlation_id": "uuid"
  }
}
```

---

# 24. Authorization Matrix

| Operation | MVP Rule | Expansion Rule |
|---|---|---|
| List integrations | workspace owner | owner/admin/integration manager |
| Create integration | workspace owner | owner/admin/integration manager |
| Update integration | workspace owner | owner/admin/integration manager |
| Trigger sync | workspace owner | owner/admin/integration manager |
| Revoke integration | workspace owner | owner/admin |
| List sync jobs | workspace owner | owner/admin/integration manager/auditor |
| List policies | workspace owner | owner/admin/security manager/auditor |
| Create policy | workspace owner | owner/admin/security manager |
| Update policy | workspace owner | owner/admin/security manager |
| Archive policy | workspace owner | owner/admin/security manager |
| Grant access | workspace owner | owner/admin |
| Revoke access | workspace owner | owner/admin with last-owner protection |

---

# 25. Audit and Runtime Event Summary

| API Operation | Audit Event | Runtime Event |
|---|---|---|
| Create integration | integration.created | integration.created |
| Update integration | integration.updated | integration.updated |
| Sync integration | integration.sync_requested | integration.sync_requested |
| Revoke integration | integration.revoked | integration.revoked |
| Create policy | security_policy.created | security_policy.created |
| Update policy | security_policy.updated | security_policy.updated |
| Archive policy | security_policy.archived | security_policy.archived |
| Grant access | workspace_access.granted | access.granted |
| Update access | workspace_access.updated | access.updated |
| Revoke access | workspace_access.revoked | access.revoked |

---

# 26. MVP Simplifications

For MVP, Bizzi may simplify by:

- using workspace owner authorization before full RBAC;
- storing only credential references, not secrets;
- supporting read-only baseline security policies;
- deferring public API keys;
- deferring webhooks;
- supporting manual integration sync only;
- using audit events as security change history.

These simplifications must preserve secret safety, workspace scope and auditability.

---

# 27. Future Expansion

Future Integration Security API may add:

```text
api-keys
service-accounts
public-api-clients
webhooks
webhook-deliveries
integration-scopes
integration-mappings
security-events
access-reviews
policy-versions
rate-limit-policies
security-policy-simulation
```

---

# 28. Acceptance Criteria

Integration Security API is accepted when:

- integration endpoints are defined;
- integration sync endpoints are defined;
- security policy endpoints are defined;
- workspace access security rules are defined;
- request and response shapes are documented;
- raw secret exposure is explicitly prohibited;
- validation rules are identified;
- authorization rules are defined;
- audit and runtime event expectations are defined;
- MVP simplifications are documented.

Status:

```text
Accepted for Dashboard Export API Design
```

---

# 29. Final Statement

```text
Bizzi Integration Security API defines how the platform exposes external connectivity, sync lifecycle, workspace access and security policies through secure, workspace-scoped, auditable and implementation-ready API contracts.
```

This API protects Bizzi while allowing it to connect safely to external systems.