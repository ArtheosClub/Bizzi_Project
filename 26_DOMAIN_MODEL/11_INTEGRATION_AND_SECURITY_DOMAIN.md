# 11_INTEGRATION_AND_SECURITY_DOMAIN.md

# Bizzi Platform

## Integration and Security Domain

**Layer:** 26_DOMAIN_MODEL  
**Component Type:** Domain Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 11_INTEGRATION_RUNTIME.md, 12_RUNTIME_SECURITY.md  
**Previous Documents:** 00_DOMAIN_MODEL_VISION.md, 01_ENTITY_CATALOG.md, 02_WORKSPACE_DOMAIN.md, 03_OPERATING_MAP_DOMAIN.md, 04_FUNCTION_AND_RESPONSIBILITY_DOMAIN.md, 05_AGENT_DOMAIN.md, 06_PROCESS_DOMAIN.md, 07_TASK_DOMAIN.md, 08_DECISION_DOMAIN.md, 09_MEMORY_DOMAIN.md, 10_AUDIT_AND_EVENT_DOMAIN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Integration and Security Domain for Bizzi Platform.

The domain describes how Bizzi represents external connections, credentials, access control, workspace isolation, permissions, security events and governed integration boundaries as structured product objects.

Core question:

```text
How does Bizzi connect to external systems and protect workspace operating data without losing governance, auditability, security and AI context control?
```

---

# 2. Domain Role

The Integration and Security Domain is the controlled boundary domain of Bizzi.

It provides:

- external system connections;
- integration lifecycle;
- credential references;
- import and export scopes;
- security policies;
- user access rules;
- workspace isolation;
- AI security boundaries;
- agent authority protection;
- audit and event linkage;
- dashboard visibility for risks and connected systems.

---

# 3. Domain Principles

## 3.1 Integrate Carefully, Govern Always

External tools should never bypass Bizzi governance.

## 3.2 Secure by Default

Company operating data must be treated as sensitive by default.

## 3.3 Workspace Isolation First

Every integration, permission, credential reference and security event must be scoped to a workspace where applicable.

## 3.4 No Secrets in Runtime Objects

Runtime objects may reference credentials, but must not expose raw secrets.

---

# 4. Aggregate Boundaries

Primary aggregate roots:

```text
Integration
SecurityPolicy
WorkspaceAccess
```

Supporting entities:

```text
IntegrationConnection
IntegrationCredentialReference
IntegrationScope
IntegrationSyncJob
IntegrationMapping
Role
Permission
AccessDecision
SecurityEvent
Session
CredentialReference
```

Related external entities:

```text
CompanyWorkspace
User
Agent
Task
Decision
MemoryEntry
AuditEvent
RuntimeEvent
ExportJob
DashboardMetric
```

---

# 5. Core Integration Entities

## 5.1 Integration

Represents an external system connected to a workspace.

Minimum domain attributes:

```text
id
workspace_id
provider
name
status
created_by
created_at
updated_at
```

Optional domain attributes:

```text
connection_type
scopes
last_sync_at
credential_ref
configuration
mapping_rules
rate_limit_policy
error_state
revoked_at
```

Domain responsibility:

```text
Integration defines a governed external system boundary for import, export or runtime support.
```

---

## 5.2 IntegrationScope

Represents what the integration is allowed to access or perform.

Potential attributes:

```text
id
workspace_id
integration_id
scope_name
scope_type
allowed_actions
status
created_at
updated_at
```

Domain responsibility:

```text
IntegrationScope makes integration access explicit, limited and auditable.
```

---

## 5.3 IntegrationCredentialReference

Represents a safe reference to credentials without exposing the credential value.

Potential attributes:

```text
id
workspace_id
integration_id
credential_ref
credential_type
status
created_at
updated_at
revoked_at
```

Domain responsibility:

```text
IntegrationCredentialReference protects secrets while allowing integrations to operate.
```

---

## 5.4 IntegrationSyncJob

Represents an import or export synchronization attempt.

Minimum domain attributes:

```text
id
workspace_id
integration_id
sync_type
status
started_at
created_at
```

Optional domain attributes:

```text
completed_at
items_processed
items_failed
error_message
source_reference
destination_reference
```

Domain responsibility:

```text
IntegrationSyncJob preserves traceability of data movement between Bizzi and external systems.
```

---

# 6. Core Security Entities

## 6.1 SecurityPolicy

Represents security and access rules for runtime behavior.

Minimum domain attributes:

```text
id
workspace_id
name
status
created_at
updated_at
```

Optional domain attributes:

```text
policy_type
rules
default_role
audit_required
ai_context_rules
integration_rules
```

Domain responsibility:

```text
SecurityPolicy defines protected behavior for workspace access, AI context, integrations and governed actions.
```

---

## 6.2 WorkspaceAccess

Represents user access to a workspace.

Minimum domain attributes:

```text
id
workspace_id
user_id
role
status
created_at
updated_at
```

Domain responsibility:

```text
WorkspaceAccess determines whether a user may access workspace operating data.
```

MVP simplification:

```text
Workspace owner has full MVP access inside own workspace.
```

---

## 6.3 Role

Represents a named access role.

Potential attributes:

```text
id
workspace_id
name
description
status
created_at
updated_at
```

MVP role:

```text
Owner
```

Future roles:

```text
Admin
Manager
Member
Viewer
Consultant
Auditor
```

---

## 6.4 Permission

Represents an allowed action or access category.

Potential attributes:

```text
id
workspace_id
name
description
category
status
created_at
updated_at
```

Permission examples:

```text
workspace.read
workspace.update
agent.manage
task.manage
decision.manage
memory.manage
audit.read
integration.manage
export.generate
security.manage
```

---

## 6.5 Session

Represents authenticated access state.

Minimum domain attributes:

```text
id
user_id
status
created_at
expires_at
last_seen_at
```

Domain responsibility:

```text
Session represents authenticated access and supports runtime security enforcement.
```

---

## 6.6 SecurityEvent

Represents an important security-related runtime event.

Potential attributes:

```text
id
workspace_id
user_id
event_type
severity
object_type
object_id
metadata
created_at
```

Domain responsibility:

```text
SecurityEvent preserves evidence of access, denial, policy changes and sensitive security activity.
```

---

# 7. Integration Types

Initial integration types:

```text
AI Provider Integration
File Export Integration
Manual Data Import
Email Import Integration
Calendar Import Integration
Webhook Input
```

MVP should prioritize:

```text
AI Provider Integration
File Export Integration
Manual Data Import
```

---

# 8. Integration Lifecycle

Recommended lifecycle:

```text
available
↓
requested
↓
configured
↓
connected
↓
active
↓
paused
↓
revoked
↓
archived
```

MVP lifecycle:

```text
configured
active
paused
revoked
error
```

---

# 9. Security Lifecycle Concepts

Security-related objects should support:

```text
active
paused
revoked
expired
archived
```

Examples:

- session may expire;
- workspace access may be revoked;
- credential reference may be revoked;
- integration may be paused;
- security policy may be archived.

---

# 10. Domain Relationships

## 10.1 Workspace to Integration

```text
CompanyWorkspace 1 → many Integrations
```

## 10.2 Integration to Credential Reference

```text
Integration 1 → 0 or many IntegrationCredentialReferences
```

## 10.3 Integration to Sync Job

```text
Integration 1 → many IntegrationSyncJobs
```

## 10.4 Workspace to SecurityPolicy

```text
CompanyWorkspace 1 → many SecurityPolicies
```

## 10.5 User to WorkspaceAccess

```text
User 1 → many WorkspaceAccess records
```

## 10.6 Role to Permission

```text
Role many → many Permissions
```

---

# 11. Domain Invariants

The Integration and Security Domain must enforce:

```text
Integration must belong to one workspace.
Active integration must have explicit scope.
Credential values must not be stored in normal runtime objects.
Revoked integrations cannot sync data.
WorkspaceAccess must reference a valid user and workspace.
Authenticated actions require valid session or equivalent identity.
AI context must be workspace-scoped.
AI must not receive raw secrets.
Security-sensitive actions must be auditable.
Access denied events should be recorded.
```

---

# 12. AI Security Rules

AI may use:

- scoped workspace context;
- approved memory entries;
- integration-derived data within allowed scope;
- user-provided inputs;
- confirmed runtime objects.

AI may not use:

- raw credentials;
- revoked integration data;
- data from another workspace;
- archived memory as active context;
- security policy internals beyond what is needed;
- unauthorized audit records.

MVP rule:

```text
AI can assist inside the workspace boundary, but cannot bypass security, permissions, audit or confirmation rules.
```

---

# 13. Integration Flow

```text
User selects integration
↓
Integration scope defined
↓
Credential reference created if required
↓
Connection validated
↓
Integration becomes active
↓
Data import or export occurs
↓
Runtime event emitted
↓
Audit event recorded
↓
Dashboard updated
```

---

# 14. Access Decision Flow

```text
User requests action
↓
Authentication checked
↓
WorkspaceAccess checked
↓
Role and permission evaluated
↓
Object workspace_id checked
↓
Action allowed or denied
↓
Security event and audit recorded if needed
```

---

# 15. Domain Events

Integration events:

```text
integration.configured
integration.connected
integration.activated
integration.paused
integration.revoked
integration.error
integration.sync_started
integration.sync_completed
integration.sync_failed
integration.data_imported
integration.data_exported
```

Security events:

```text
security.user_authenticated
security.session_created
security.session_expired
security.access_granted
security.access_denied
security.role_assigned
security.permission_checked
security.integration_scope_changed
security.credential_reference_created
security.export_authorized
security.export_denied
```

---

# 16. Audit Requirements

Audited actions:

```text
integration.configured
integration.connected
integration.scope_changed
integration.paused
integration.revoked
integration.sync_completed
integration.sync_failed
integration.data_exported
security.access_denied
security.role_assigned
security.permission_changed
security.credential_reference_created
security.export_authorized
```

Audit must answer:

```text
Who connected or accessed what, under which scope or permission, and what data or object was affected?
```

---

# 17. Memory Requirements

Memory may be created from:

- confirmed integration context;
- recurring integration errors;
- imported business context;
- security lessons;
- repeated access problems;
- integration setup decisions.

Memory types:

```text
integration_context
imported_context
integration_lesson
sync_issue
security_lesson
access_issue
```

---

# 18. Dashboard Requirements

Dashboard should show:

- active integrations;
- paused integrations;
- integration errors;
- last sync time;
- imported items pending review;
- export activity;
- access warnings;
- security events;
- AI context safety status.

Dashboard question:

```text
Which external systems are connected, what data moved, and are the workspace boundaries protected?
```

---

# 19. Security Requirements

Security requirements:

```text
All integration data must be workspace-scoped.
Credentials must be referenced, not exposed.
Integration scopes must be explicit.
Security policies must be auditable.
Access checks must enforce workspace_id.
Exports require authorization.
AI context must respect permissions and integration scope.
Revoked access must block future operations.
```

---

# 20. MVP Domain Behavior

MVP should support:

```text
Create integration
Configure integration scope
Store credential reference
Activate integration
Pause integration
Revoke integration
Create sync job
Record sync error
Authenticate user
Validate workspace access
Authorize owner actions
Record access denied event
Prevent cross-workspace access
Protect AI context scope
Create audit events
Show integration and security status on dashboard
```

---

# 21. Out of Scope for MVP

The Integration and Security Domain does not need in MVP:

- public integration marketplace;
- complex OAuth for many providers;
- enterprise SSO;
- MFA enforcement;
- complex RBAC UI;
- attribute-based access control;
- external SIEM integration;
- real-time bidirectional sync;
- payment execution;
- external write actions without approval.

---

# 22. Data Model Implications

Future Data Model should include tables or collections for:

```text
integrations
integration_sync_jobs
security_policies
workspace_access
sessions
```

Potential later tables:

```text
integration_scopes
integration_credential_references
integration_mappings
roles
permissions
role_permissions
security_events
```

Recommended indexes later:

```text
integrations.workspace_id
integrations.provider
integrations.status
integration_sync_jobs.workspace_id
integration_sync_jobs.integration_id
integration_sync_jobs.status
workspace_access.workspace_id
workspace_access.user_id
sessions.user_id
sessions.status
security_events.workspace_id
security_events.event_type
security_events.created_at
```

---

# 23. API Implications

Future API contracts should support:

```text
GET /workspaces/{workspace_id}/integrations
POST /workspaces/{workspace_id}/integrations
GET /workspaces/{workspace_id}/integrations/{integration_id}
PATCH /workspaces/{workspace_id}/integrations/{integration_id}
POST /workspaces/{workspace_id}/integrations/{integration_id}/pause
POST /workspaces/{workspace_id}/integrations/{integration_id}/revoke
POST /workspaces/{workspace_id}/integrations/{integration_id}/sync
GET /workspaces/{workspace_id}/security/access
GET /workspaces/{workspace_id}/security/events
POST /workspaces/{workspace_id}/security/check-access
```

---

# 24. Traceability Pattern

Integration and security traceability chain:

```text
User / System / Agent Request
↓
Access Decision / Integration Action
↓
Runtime Event
↓
Audit Event
↓
Sync Job / Security Event
↓
Memory Entry if useful
↓
Dashboard Metric
```

---

# 25. Acceptance Criteria

Integration and Security Domain is ready when:

- Integration is defined as aggregate root;
- SecurityPolicy and WorkspaceAccess are defined;
- credential reference boundaries are explicit;
- integration lifecycle is clear;
- access decision rules are defined;
- AI security rules are defined;
- audit and event behavior is defined;
- dashboard role is defined;
- data model and API implications are identified.

Status:

```text
Ready for Data Model and API Design
```

---

# 26. Architecture Alignment

| Integration and Security Domain Area | Reference |
|---|---|
| Integration | 11_INTEGRATION_RUNTIME.md |
| Integration Scope | Integration Runtime / Runtime Security |
| Credential Reference | Runtime Security |
| Sync Job | Integration Runtime |
| SecurityPolicy | 12_RUNTIME_SECURITY.md |
| WorkspaceAccess | Workspace Runtime / Runtime Security |
| Role and Permission | Governance Baseline |
| Security Events | Event Runtime |
| Integration Audit | Audit Runtime |
| AI Security | Agent Runtime / Runtime Security |
| Dashboard | Core User Journey |

---

# 27. Final Integration and Security Domain Statement

```text
Integration and Security Domain defines how Bizzi connects to external systems and protects workspace operating data through scoped integrations, credential references, access control, security policies, audit events and AI-safe boundaries.
```

This domain ensures Bizzi can become connected without becoming uncontrolled.