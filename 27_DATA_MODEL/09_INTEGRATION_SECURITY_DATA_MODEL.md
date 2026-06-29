# 09_INTEGRATION_SECURITY_DATA_MODEL.md

# Bizzi Platform

## Integration and Security Data Model

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Model Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 11_INTEGRATION_RUNTIME.md, 12_RUNTIME_SECURITY.md  
**Domain Reference:** 26_DOMAIN_MODEL / 11_INTEGRATION_AND_SECURITY_DOMAIN.md  
**Previous Documents:** 00_DATA_MODEL_VISION.md, 01_DATABASE_PRINCIPLES.md, 02_ENTITY_TO_TABLE_MAPPING.md, 03_CORE_TABLES.md, 04_WORKSPACE_DATA_MODEL.md, 05_OPERATING_MAP_DATA_MODEL.md, 06_FUNCTION_RESPONSIBILITY_DATA_MODEL.md, 07_AGENT_PROCESS_TASK_DECISION_DATA_MODEL.md, 08_MEMORY_AUDIT_EVENT_DATA_MODEL.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Integration and Security Data Model for Bizzi Platform.

It translates the Integration and Security Domain into database tables, columns, relationships, constraints and indexing rules that support external connections, workspace access, security policy, integration lifecycle, safe credential references and governed data movement.

Core question:

```text
How does Bizzi persist external integrations and security boundaries while protecting workspace data, AI context and auditability?
```

---

# 2. Data Model Role

This data model defines the controlled boundary layer of Bizzi.

It supports:

- external integration records;
- integration status and configuration;
- integration sync jobs;
- credential references without storing secret values;
- workspace access control;
- security policies;
- sessions and access decisions;
- audit and runtime event linkage;
- dashboard visibility for connected systems and security warnings.

---

# 3. Tables in Scope

Priority 1 / existing core tables:

```text
users
sessions
company_workspaces
```

Priority 2 governed runtime tables:

```text
integrations
integration_sync_jobs
security_policies
workspace_access
```

Expansion tables:

```text
integration_scopes
integration_credential_references
integration_mappings
roles
permissions
role_permissions
security_events
workspace_invitations
```

Recommended MVP implementation:

```text
company_workspaces.owner_user_id
sessions
integrations
integration_sync_jobs
security_policies
```

Recommended near-MVP implementation:

```text
workspace_access
```

---

# 4. Workspace Scope Rule

All integration and workspace security records that belong to company operating data must include:

```text
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
```

This applies to:

- integrations;
- integration sync jobs;
- integration scopes;
- security policies;
- workspace access;
- security events;
- export authorization context.

---

# 5. integrations Table

## Purpose

Stores external systems connected to a workspace.

## Domain Entity

```text
Integration
```

## Table

```text
integrations
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
provider TEXT NOT NULL
name TEXT NOT NULL
connection_type TEXT NULL
status TEXT NOT NULL
scopes JSONB NULL
credential_ref TEXT NULL
configuration JSONB NULL
mapping_rules JSONB NULL
rate_limit_policy JSONB NULL
last_sync_at TIMESTAMPTZ NULL
error_state TEXT NULL
created_by UUID NULL REFERENCES users(id)
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
revoked_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## Status Values

Initial values:

```text
configured
active
paused
revoked
error
```

Expansion values:

```text
available
requested
connected
archived
```

## Notes

`credential_ref` must be a reference to secure secret storage, not the actual credential value.

---

# 6. integration_sync_jobs Table

## Purpose

Stores import or export synchronization attempts for integrations.

## Domain Entity

```text
IntegrationSyncJob
```

## Table

```text
integration_sync_jobs
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
integration_id UUID NOT NULL REFERENCES integrations(id)
sync_type TEXT NOT NULL
status TEXT NOT NULL
started_at TIMESTAMPTZ NULL
completed_at TIMESTAMPTZ NULL
items_processed INTEGER NOT NULL DEFAULT 0
items_failed INTEGER NOT NULL DEFAULT 0
error_message TEXT NULL
source_reference TEXT NULL
destination_reference TEXT NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
created_by UUID NULL REFERENCES users(id)
metadata JSONB NULL
```

## Sync Type Values

Initial values:

```text
import
export
validation
```

Expansion values:

```text
full_sync
incremental_sync
webhook_event
```

## Status Values

Initial values:

```text
queued
running
completed
failed
cancelled
```

---

# 7. security_policies Table

## Purpose

Stores workspace-level security and AI context rules.

## Domain Entity

```text
SecurityPolicy
```

## Table

```text
security_policies
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
name TEXT NOT NULL
policy_type TEXT NOT NULL
status TEXT NOT NULL
rules JSONB NOT NULL
default_role TEXT NULL
audit_required BOOLEAN NOT NULL DEFAULT true
ai_context_rules JSONB NULL
integration_rules JSONB NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
created_by UUID NULL REFERENCES users(id)
metadata JSONB NULL
```

## Policy Type Values

Initial values:

```text
workspace_access
ai_context
integration_access
export_control
audit_policy
```

## Status Values

```text
draft
active
paused
archived
```

---

# 8. workspace_access Table

## Purpose

Stores user access to workspaces.

## Domain Entity

```text
WorkspaceAccess
```

## MVP Status

```text
Priority 2 / Near-MVP
```

## Table

```text
workspace_access
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
user_id UUID NOT NULL REFERENCES users(id)
role TEXT NOT NULL
status TEXT NOT NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
created_by UUID NULL REFERENCES users(id)
revoked_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## Role Values

MVP value:

```text
owner
```

Expansion values:

```text
admin
manager
member
viewer
consultant
auditor
```

## Status Values

```text
active
invited
revoked
archived
```

## Constraint

Recommended:

```text
UNIQUE(workspace_id, user_id)
```

## MVP Simplification

MVP may rely on:

```text
company_workspaces.owner_user_id
```

before fully enabling `workspace_access`.

---

# 9. integration_scopes Table

## Purpose

Stores normalized integration access scopes.

## Domain Entity

```text
IntegrationScope
```

## MVP Status

```text
Expansion
```

## Table

```text
integration_scopes
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
integration_id UUID NOT NULL REFERENCES integrations(id)
scope_name TEXT NOT NULL
scope_type TEXT NULL
allowed_actions JSONB NULL
status TEXT NOT NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## MVP Simplification

Use this field on `integrations` first:

```text
scopes JSONB
```

---

# 10. integration_credential_references Table

## Purpose

Stores safe references to credentials without storing secret values.

## Domain Entity

```text
IntegrationCredentialReference
```

## MVP Status

```text
Expansion
```

## Table

```text
integration_credential_references
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
integration_id UUID NOT NULL REFERENCES integrations(id)
credential_ref TEXT NOT NULL
credential_type TEXT NOT NULL
status TEXT NOT NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
revoked_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## MVP Simplification

Use this field on `integrations` first:

```text
credential_ref TEXT
```

Rule:

```text
Do not store raw credentials in Bizzi runtime tables.
```

---

# 11. roles, permissions and role_permissions Tables

## Purpose

Support future role-based access control.

## MVP Status

```text
Expansion
```

## roles

```text
id UUID PRIMARY KEY
workspace_id UUID NULL REFERENCES company_workspaces(id)
name TEXT NOT NULL
description TEXT NULL
status TEXT NOT NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## permissions

```text
id UUID PRIMARY KEY
name TEXT NOT NULL UNIQUE
description TEXT NULL
category TEXT NULL
status TEXT NOT NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## role_permissions

```text
id UUID PRIMARY KEY
role_id UUID NOT NULL REFERENCES roles(id)
permission_id UUID NOT NULL REFERENCES permissions(id)
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
```

## MVP Simplification

Use simple role values in `workspace_access.role` before implementing full RBAC tables.

---

# 12. security_events Table

## Purpose

Stores security-related events when a dedicated security event table becomes necessary.

## Domain Entity

```text
SecurityEvent
```

## MVP Status

```text
Expansion
```

## Table

```text
security_events
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NULL REFERENCES company_workspaces(id)
user_id UUID NULL REFERENCES users(id)
event_type TEXT NOT NULL
severity TEXT NOT NULL
object_type TEXT NULL
object_id UUID NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## MVP Simplification

Use `audit_events` and `runtime_events` for initial access and security signals.

---

# 13. Relationships

## Workspace to Integration

```text
company_workspaces.id → integrations.workspace_id
```

Relationship:

```text
CompanyWorkspace 1 → many Integrations
```

## Integration to Sync Job

```text
integrations.id → integration_sync_jobs.integration_id
```

Relationship:

```text
Integration 1 → many IntegrationSyncJobs
```

## Workspace to Security Policy

```text
company_workspaces.id → security_policies.workspace_id
```

Relationship:

```text
CompanyWorkspace 1 → many SecurityPolicies
```

## Workspace to Access

```text
company_workspaces.id → workspace_access.workspace_id
users.id → workspace_access.user_id
```

Relationship:

```text
CompanyWorkspace many ↔ many Users through workspace_access
```

---

# 14. Credential Safety Pattern

Allowed data:

```text
credential_ref
credential_type
provider
scopes
status
revoked_at
```

Not allowed in normal runtime tables:

```text
raw access tokens
raw API keys
plain text passwords
private secret values
```

Credential values should live in a secure secret manager or external provider, referenced only by `credential_ref`.

---

# 15. Access Decision Pattern

Access checks should use:

```text
user_id
workspace_id
role
status
requested_action
object_workspace_id
```

MVP access rule:

```text
User may access workspace if user_id = company_workspaces.owner_user_id.
```

Near-MVP access rule:

```text
User may access workspace if workspace_access has active record for user and workspace.
```

---

# 16. Indexing Requirements

## integrations

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, provider)
INDEX(created_by)
INDEX(last_sync_at)
```

## integration_sync_jobs

```text
INDEX(workspace_id)
INDEX(integration_id)
INDEX(workspace_id, status)
INDEX(workspace_id, sync_type)
INDEX(started_at)
INDEX(completed_at)
```

## security_policies

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, policy_type)
```

## workspace_access

```text
UNIQUE(workspace_id, user_id)
INDEX(user_id)
INDEX(workspace_id, status)
INDEX(workspace_id, role)
```

## security_events

```text
INDEX(workspace_id)
INDEX(user_id)
INDEX(event_type)
INDEX(severity)
INDEX(created_at)
```

---

# 17. Data Integrity Rules

Database-level rules:

```text
integrations.workspace_id IS NOT NULL
integrations.provider IS NOT NULL
integrations.name IS NOT NULL
integrations.status IS NOT NULL
integration_sync_jobs.workspace_id IS NOT NULL
integration_sync_jobs.integration_id IS NOT NULL
integration_sync_jobs.sync_type IS NOT NULL
integration_sync_jobs.status IS NOT NULL
security_policies.workspace_id IS NOT NULL
security_policies.name IS NOT NULL
security_policies.policy_type IS NOT NULL
security_policies.status IS NOT NULL
workspace_access.workspace_id IS NOT NULL
workspace_access.user_id IS NOT NULL
workspace_access.role IS NOT NULL
workspace_access.status IS NOT NULL
```

Service-level rules:

```text
Revoked integrations cannot run sync jobs.
Integration scope must be checked before data movement.
Workspace access must be active before operating data is returned.
AI context assembly must respect workspace scope and security policy.
Credential references must not expose secret values.
Exports require authorization and audit.
```

---

# 18. Audit Requirements

Audited actions include:

```text
integration.configured
integration.connected
integration.scope_changed
integration.paused
integration.revoked
integration.sync_started
integration.sync_completed
integration.sync_failed
security.policy_created
security.policy_updated
workspace_access.granted
workspace_access.revoked
access.denied
export.authorized
export.denied
```

Audit target examples:

```text
object_type = 'integration'
object_id = integrations.id
```

```text
object_type = 'workspace_access'
object_id = workspace_access.id
```

---

# 19. Runtime Event Requirements

Runtime events include:

```text
integration.configured
integration.connected
integration.activated
integration.paused
integration.revoked
integration.sync_started
integration.sync_completed
integration.sync_failed
security.policy_updated
access.granted
access.denied
```

Event source pattern:

```text
source_object_type = 'integration'
source_object_id = integrations.id
```

---

# 20. Dashboard Requirements

Dashboard queries should support:

- active integrations;
- paused integrations;
- integrations in error state;
- last sync time;
- failed sync jobs;
- active security policies;
- access warnings;
- recent access denied events;
- connected provider overview.

Core query support:

```text
integrations.workspace_id, status
integration_sync_jobs.workspace_id, status
security_policies.workspace_id, status
workspace_access.workspace_id, status
```

---

# 21. AI Security Requirements

AI context assembly must check:

```text
workspace_id
security_policies
memory status
integration scope
user authorization
agent authority scope
```

AI may use:

```text
approved workspace context
active memory entries
integration-derived data within allowed scope
confirmed runtime objects
```

AI may not use:

```text
credential values
revoked integration data
data from another workspace
archived memory as active context
unauthorized audit records
```

---

# 22. MVP Simplifications

For MVP, Bizzi may simplify by:

- using `company_workspaces.owner_user_id` for access control;
- storing integration scopes as JSONB on `integrations`;
- storing credential references as `credential_ref` on `integrations`;
- using audit_events instead of dedicated security_events;
- using simple role strings before full RBAC;
- using service-level validation for authorization.

These simplifications must preserve workspace isolation, auditability and credential safety.

---

# 23. Future Expansion

Future tables may include:

```text
integration_scopes
integration_credential_references
integration_mappings
roles
permissions
role_permissions
security_events
workspace_invitations
access_decisions
policy_versions
```

These should be introduced when product behavior requires multi-user access, enterprise security or richer integration governance.

---

# 24. Acceptance Criteria

This data model is ready when:

- integrations table is defined;
- integration_sync_jobs table is defined;
- security_policies table is defined;
- workspace_access expansion path is defined;
- credential reference rules are explicit;
- workspace scoping is explicit;
- indexes are identified;
- audit and event requirements are defined;
- AI security rules are documented;
- MVP simplifications are documented.

Status:

```text
Accepted for Implementation Planning
```

---

# 25. Final Statement

```text
Bizzi Integration and Security Data Model defines how the platform persists external system connections, sync activity, workspace access and security policy as workspace-scoped, credential-safe, auditable and AI-safe database records.
```

This model allows Bizzi to connect with external systems without losing governance or control.