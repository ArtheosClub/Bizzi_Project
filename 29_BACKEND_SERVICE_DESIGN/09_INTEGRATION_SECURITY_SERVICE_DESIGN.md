# 09_INTEGRATION_SECURITY_SERVICE_DESIGN.md

# Bizzi Platform

## Integration Security Service Design

**Layer:** 29_BACKEND_SERVICE_DESIGN  
**Component Type:** Backend Service Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 11_INTEGRATION_RUNTIME.md, 12_RUNTIME_SECURITY.md  
**Domain Reference:** 26_DOMAIN_MODEL / 11_INTEGRATION_AND_SECURITY_DOMAIN.md  
**Data Model Reference:** 27_DATA_MODEL / 09_INTEGRATION_SECURITY_DATA_MODEL.md  
**API Contracts Reference:** 28_API_CONTRACTS / 08_INTEGRATION_SECURITY_API.md  
**Previous Document:** 08_MEMORY_AUDIT_EVENT_SERVICE_DESIGN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the backend service design for integration and security behavior in Bizzi Platform.

It specifies the services, repositories, validation rules, authorization rules, transaction patterns, audit events and runtime events required to implement the Integration Security API.

Core question:

```text
How should Bizzi backend services connect to external systems and enforce security controls without exposing secrets, weakening workspace isolation or bypassing auditability?
```

---

# 2. Service Scope

This design covers:

```text
IntegrationService
IntegrationSyncService
ProviderAdapterService
SecretReferenceService
SecurityPolicyService
WorkspaceAccessSecurityService
AuthorizationPolicyService
```

Primary API references:

```text
GET /api/v1/workspaces/{workspace_id}/integrations
POST /api/v1/workspaces/{workspace_id}/integrations
GET /api/v1/workspaces/{workspace_id}/integrations/{integration_id}
PATCH /api/v1/workspaces/{workspace_id}/integrations/{integration_id}
POST /api/v1/workspaces/{workspace_id}/integrations/{integration_id}/sync
POST /api/v1/workspaces/{workspace_id}/integrations/{integration_id}/revoke
GET /api/v1/workspaces/{workspace_id}/integration-sync-jobs
GET /api/v1/workspaces/{workspace_id}/integration-sync-jobs/{sync_job_id}
GET /api/v1/workspaces/{workspace_id}/security-policies
POST /api/v1/workspaces/{workspace_id}/security-policies
PATCH /api/v1/workspaces/{workspace_id}/security-policies/{policy_id}
POST /api/v1/workspaces/{workspace_id}/security-policies/{policy_id}/archive
GET /api/v1/workspaces/{workspace_id}/workspace-access
POST /api/v1/workspaces/{workspace_id}/workspace-access
POST /api/v1/workspaces/{workspace_id}/workspace-access/{workspace_access_id}/revoke
```

Primary data references:

```text
integrations
integration_sync_jobs
security_policies
workspace_access
audit_events
runtime_events
```

---

# 3. Module Ownership

Integration and security behavior belongs to:

```text
IntegrationModule
SecurityModule
AuthorizationModule
SecretReferenceModule
```

Supporting modules:

```text
WorkspaceModule
AuditModule
EventModule
JobQueueModule
IdempotencyModule
TransactionModule
```

Rule:

```text
IntegrationModule owns external connection lifecycle. SecurityModule owns security policy and workspace access governance. SecretReferenceModule owns secret resolution boundaries.
```

---

# 4. Service Responsibilities

## IntegrationService

Responsibilities:

```text
list integrations
get integration
create integration
update integration
revoke integration
validate provider and integration_type
validate scopes and configuration
store credential_ref only
emit integration audit and runtime events
```

## IntegrationSyncService

Responsibilities:

```text
trigger integration sync
create sync job records
validate integration is active
validate sync permission
coordinate provider adapter execution
record sync status
emit sync audit and runtime events
```

## ProviderAdapterService

Responsibilities:

```text
route provider-specific operations
validate provider configuration schema
execute provider sync through secure boundary
normalize provider results
hide provider implementation details from API services
```

## SecretReferenceService

Responsibilities:

```text
validate credential_ref format
resolve secrets only inside secure execution boundary
prevent raw secrets from entering DTOs
support future rotation and revocation
protect secrets from audit and runtime payloads
```

## SecurityPolicyService

Responsibilities:

```text
list security policies
create security policies
update security policies
archive security policies
validate policy_type and rules schema
prevent weakening mandatory platform safety rules
emit security policy audit and runtime events
```

## WorkspaceAccessSecurityService

Responsibilities:

```text
list workspace access
grant workspace access
revoke workspace access
validate role and target user
protect last active owner
emit workspace access audit and runtime events
```

## AuthorizationPolicyService

Responsibilities:

```text
centralize workspace permission checks
check integration manager permissions
check security manager permissions
check auditor and runtime event visibility
check export and AI policy restrictions later
```

---

# 5. Repository Responsibilities

## IntegrationRepository

Methods:

```text
createIntegration(data)
findByIdAndWorkspace(integration_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
updateByIdAndWorkspace(integration_id, workspace_id, patch)
revokeByIdAndWorkspace(integration_id, workspace_id, revoke_data)
findActiveByProvider(workspace_id, provider, integration_type optional)
```

## IntegrationSyncJobRepository

Methods:

```text
createSyncJob(data)
findByIdAndWorkspace(sync_job_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
updateStatus(sync_job_id, workspace_id, status_data)
markStarted(sync_job_id, workspace_id, started_data)
markCompleted(sync_job_id, workspace_id, completed_data)
markFailed(sync_job_id, workspace_id, failure_data)
findRunningForIntegration(workspace_id, integration_id)
```

## SecurityPolicyRepository

Methods:

```text
createPolicy(data)
findByIdAndWorkspace(policy_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
updateByIdAndWorkspace(policy_id, workspace_id, patch)
archiveByIdAndWorkspace(policy_id, workspace_id, archive_data)
findActiveByType(workspace_id, policy_type)
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

Every service method must receive:

```text
workspace_id
actor_id
actor_type
correlation_id
request_id
idempotency_key optional
```

Provider execution may additionally receive internal-only context:

```text
integration_id
sync_job_id
credential_ref
provider
scopes
internal_service_actor
```

Rule:

```text
Raw secret values must never be included in public service context, response DTOs, audit payloads or runtime event payloads.
```

---

# 7. Create Integration Flow

## Service Method

```text
IntegrationService.createIntegration(context, input)
```

## Input

```text
provider
integration_type
name
credential_ref
scopes
configuration
metadata optional
```

## Flow

```text
validate authenticated actor
load workspace
check workspace is active
check create integration permission
validate provider
validate integration_type
validate name
reject raw credential fields
validate credential_ref through SecretReferenceService
validate scopes for provider
validate configuration against provider schema
begin transaction
create integration with active status
record integration.created audit event
emit integration.created runtime event
commit transaction
return integration DTO without raw secrets
```

---

# 8. Integration Validation Rules

Validation rules:

```text
provider must be supported
integration_type must be valid
name is required
credential_ref is required for credentialed integrations
credential_ref must reference secure secret storage
scopes must be allowed for provider
configuration must match provider schema
raw credentials must be rejected
workspace must be active for mutations
```

Forbidden raw fields:

```text
access_token
refresh_token
api_key
client_secret
password
private_key
raw credential payload
```

Error mappings:

```text
invalid provider → invalid_provider
invalid scope → invalid_scope
invalid credential_ref → invalid_credential_ref
raw credential supplied → credential_value_not_allowed
workspace archived → workspace_archived
```

---

# 9. List and Get Integration Flow

## List Method

```text
IntegrationService.listIntegrations(context, filters, pagination)
```

Supported filters:

```text
status
provider
integration_type
```

Flow:

```text
validate authenticated actor
check integration read permission
validate filters
call IntegrationRepository.listByWorkspace
return paginated integration DTOs without raw secrets
```

## Get Method

```text
IntegrationService.getIntegration(context, integration_id)
```

Flow:

```text
validate authenticated actor
check integration read permission
load integration by id and workspace_id
return integration DTO without raw secrets
```

---

# 10. Update Integration Flow

## Service Method

```text
IntegrationService.updateIntegration(context, integration_id, input)
```

Mutable fields:

```text
name
configuration
scopes
metadata
```

Flow:

```text
validate authenticated actor
load workspace
check workspace is active
check update integration permission
load integration by id and workspace_id
check integration is not revoked
reject raw credential fields
validate scopes if supplied
validate configuration if supplied
capture before_state
begin transaction
update integration
record integration.updated audit event
emit integration.updated runtime event
commit transaction
return integration DTO
```

---

# 11. Revoke Integration Flow

## Service Method

```text
IntegrationService.revokeIntegration(context, integration_id, input)
```

Input:

```text
revocation_reason optional
```

Flow:

```text
validate authenticated actor
load workspace
check revoke integration permission
load integration by id and workspace_id
check integration is not already revoked
capture before_state
begin transaction
set status revoked
set revoked_at
record integration.revoked audit event
emit integration.revoked runtime event
commit transaction
return revoked integration DTO
```

Rule:

```text
Revoked integrations cannot be used for sync jobs.
```

---

# 12. Trigger Integration Sync Flow

## Service Method

```text
IntegrationSyncService.triggerSync(context, integration_id, input)
```

Input:

```text
sync_type
idempotency_key optional
```

Flow:

```text
validate authenticated actor
load workspace
check workspace is active
check sync permission
load integration by id and workspace_id
check integration status is active
validate sync_type
check idempotency if key supplied
check duplicate running sync policy
begin transaction
create integration_sync_job with queued status
record integration.sync_requested audit event
emit integration.sync_requested runtime event
emit integration.sync_queued runtime event
commit transaction
enqueue sync job if JobQueueModule is available
return sync job DTO
```

---

# 13. Execute Integration Sync Flow

## Internal Service Method

```text
IntegrationSyncService.executeSync(internal_context, sync_job_id)
```

Flow:

```text
load sync job
load integration by id and workspace_id
check integration is active
resolve credential_ref through SecretReferenceService
mark sync job started
call ProviderAdapterService.executeSync
normalize provider result
mark sync job completed or failed
record integration.sync_completed or integration.sync_failed audit event when appropriate
emit integration.sync_completed or integration.sync_failed runtime event
```

Security rule:

```text
Resolved secrets must exist only in the provider execution boundary and must not be stored in sync job records, logs, audit events or runtime events.
```

---

# 14. Integration Sync Job Query Flow

## List Method

```text
IntegrationSyncService.listSyncJobs(context, filters, pagination)
```

Supported filters:

```text
integration_id
status
sync_type
from_timestamp
to_timestamp
```

Flow:

```text
validate authenticated actor
check sync job read permission
validate filters
call IntegrationSyncJobRepository.listByWorkspace
return paginated sync job DTOs
```

## Get Method

```text
IntegrationSyncService.getSyncJob(context, sync_job_id)
```

Flow:

```text
validate authenticated actor
check sync job read permission
load sync job by id and workspace_id
return sync job DTO
```

---

# 15. Create Security Policy Flow

## Service Method

```text
SecurityPolicyService.createPolicy(context, input)
```

Input:

```text
policy_type
name
rules
metadata optional
```

Flow:

```text
validate authenticated actor
load workspace
check workspace is active
check create security policy permission
validate policy_type
validate name
validate rules schema
validate policy does not weaken mandatory platform safety rules
begin transaction
create security policy with active status
record security_policy.created audit event
emit security_policy.created runtime event
commit transaction
return policy DTO
```

---

# 16. Update Security Policy Flow

## Service Method

```text
SecurityPolicyService.updatePolicy(context, policy_id, input)
```

Flow:

```text
validate authenticated actor
load workspace
check workspace is active
check update security policy permission
load policy by id and workspace_id
check policy is not archived
validate mutable fields
validate rules schema
validate policy does not weaken mandatory platform rules
capture before_state
begin transaction
update policy
record security_policy.updated audit event
emit security_policy.updated runtime event
commit transaction
return policy DTO
```

---

# 17. Archive Security Policy Flow

## Service Method

```text
SecurityPolicyService.archivePolicy(context, policy_id, input)
```

Flow:

```text
validate authenticated actor
check archive security policy permission
load policy by id and workspace_id
check policy is not already archived
check policy is not mandatory baseline policy unless replacement exists
capture before_state
begin transaction
set status archived
set archived_at
record security_policy.archived audit event
emit security_policy.archived runtime event
commit transaction
return policy DTO
```

---

# 18. Workspace Access Security Flow

Workspace access behavior is shared with `04_WORKSPACE_SERVICE_DESIGN.md` but SecurityModule defines governance rules.

Grant access flow:

```text
validate actor
check owner/admin permission
validate target user
validate role
check duplicate active access
create workspace_access
record workspace_access.granted audit event
emit access.granted runtime event
```

Revoke access flow:

```text
validate actor
check owner/admin permission
load access record
if target is owner, check last-owner protection
set status revoked
record workspace_access.revoked audit event
emit access.revoked runtime event
```

Rule:

```text
The last active owner cannot be revoked without ownership transfer or replacement owner creation.
```

---

# 19. Authorization Rules

Integration and security authorization matrix:

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

# 20. Audit Events

Services should emit:

```text
integration.created
integration.updated
integration.revoked
integration.sync_requested
integration.sync_completed
integration.sync_failed
security_policy.created
security_policy.updated
security_policy.archived
workspace_access.granted
workspace_access.updated
workspace_access.revoked
```

Audit payload rules:

```text
include workspace_id
include actor_id and actor_type
include object reference
include before_state and after_state when useful
include correlation_id
exclude raw secrets
exclude provider tokens
exclude private keys
```

---

# 21. Runtime Events

Services should emit:

```text
integration.created
integration.updated
integration.revoked
integration.sync_requested
integration.sync_queued
integration.sync_completed
integration.sync_failed
security_policy.created
security_policy.updated
security_policy.archived
access.granted
access.updated
access.revoked
```

Runtime events may trigger:

```text
sync worker execution
access cache invalidation
security policy cache invalidation
notification later
dashboard refresh later
```

---

# 22. DTOs

Integration DTO:

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
  "revoked_at": null
}
```

Sync Job DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "integration_id": "uuid",
  "sync_type": "manual",
  "status": "queued",
  "started_at": null,
  "completed_at": null,
  "error_message": null
}
```

Security Policy DTO:

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
  }
}
```

---

# 23. Error Mapping

Integration and security service errors:

```text
Unauthenticated → unauthenticated
WorkspaceNotFound → not_found
WorkspaceArchived → workspace_archived
IntegrationNotFound → not_found
SyncJobNotFound → not_found
SecurityPolicyNotFound → not_found
WorkspaceAccessNotFound → not_found
AccessDenied → forbidden
InvalidProvider → invalid_provider
InvalidScope → invalid_scope
InvalidPolicy → invalid_policy
InvalidCredentialRef → invalid_credential_ref
CredentialValueNotAllowed → credential_value_not_allowed
IntegrationRevoked → integration_revoked
SyncAlreadyRunning → sync_already_running
LastOwnerProtected → business_rule_violation
IdempotencyConflict → idempotency_conflict
```

---

# 24. Security Rules

Mandatory rules:

```text
raw credentials are never accepted by normal API contracts
raw credentials are never returned by services
credential_ref is the only normal credential field
secrets are resolved only by SecretReferenceService
provider errors are sanitized before API exposure
audit and runtime event payloads must not contain secrets
revoked integrations cannot sync
security policies must not weaken mandatory platform safety rules
last owner must be protected
```

---

# 25. MVP Simplifications

MVP may simplify by:

```text
owner-only authorization
manual integration sync only
credential_ref stored without full rotation workflow
read-only baseline security policies
basic workspace access governance
simple provider support for GitHub first
sync jobs without advanced retry strategy
```

MVP must preserve:

```text
workspace scope
secret safety
audit events for security-sensitive changes
runtime events for sync coordination
last-owner protection
structured error mapping
```

---

# 26. Future Expansion

Future service expansion may add:

```text
API keys
service accounts
OAuth provider flows
webhook subscriptions
webhook deliveries
secret rotation
secret revocation workflow
integration mappings
provider-specific adapters
access reviews
policy versions
security event stream
rate limit policies
security policy simulation
```

---

# 27. Testing Expectations

Service tests should cover:

```text
create integration rejects raw credentials
create integration validates credential_ref
create integration validates provider scope
update integration rejects revoked integration
trigger sync rejects revoked integration
trigger sync creates queued sync job
sync execution never stores raw secrets
security policy creation validates rules
policy update cannot weaken mandatory safety rules
workspace access revoke protects last owner
all security-sensitive mutations emit audit events
all integration mutations emit runtime events
workspace archived blocks mutations
```

Repository tests should cover:

```text
list integrations by workspace and filters
find integration by id and workspace
find running sync jobs
list sync jobs by integration
list policies by workspace and type
find active workspace access
count active owners
pagination and sorting behavior
```

---

# 28. Acceptance Criteria

Integration Security Service Design is accepted when:

- IntegrationService responsibilities are defined;
- IntegrationSyncService responsibilities are defined;
- ProviderAdapterService responsibilities are defined;
- SecretReferenceService responsibilities are defined;
- SecurityPolicyService responsibilities are defined;
- WorkspaceAccessSecurityService responsibilities are defined;
- repository methods are identified;
- integration lifecycle and sync flows are documented;
- security policy flows are documented;
- workspace access governance is documented;
- authorization matrix is defined;
- audit and runtime event expectations are defined;
- DTOs, error mappings and security rules are documented;
- MVP simplifications and test expectations are documented.

Status:

```text
Accepted for Dashboard Export Service Design
```

---

# 29. Final Statement

```text
Bizzi Integration Security Service Design defines how backend services connect Bizzi to external systems while preserving secret safety, workspace isolation, authorization, auditability and secure runtime coordination.
```

This service layer protects Bizzi while allowing the platform to integrate safely with external tools and data sources.