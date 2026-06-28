# 04_WORKSPACE_DATA_MODEL.md

# Bizzi Platform

## Workspace Data Model

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Model Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 03_WORKSPACE_RUNTIME.md  
**Domain Reference:** 26_DOMAIN_MODEL / 02_WORKSPACE_DOMAIN.md  
**Previous Documents:** 00_DATA_MODEL_VISION.md, 01_DATABASE_PRINCIPLES.md, 02_ENTITY_TO_TABLE_MAPPING.md, 03_CORE_TABLES.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Workspace Data Model for Bizzi Platform.

It translates the Workspace Domain into database tables, columns, relationships, constraints and indexing rules that support workspace creation, ownership, settings, context, isolation, audit and future multi-user expansion.

Core question:

```text
How does Bizzi persist company workspaces as the root data boundary for all operating objects?
```

---

# 2. Workspace Data Model Role

The Workspace Data Model is the persistence foundation for tenant-like company boundaries inside Bizzi.

It supports:

- workspace creation;
- workspace ownership;
- workspace settings;
- onboarding state;
- profile context;
- workspace isolation;
- future access control;
- audit and event references;
- dashboard and AI context assembly.

---

# 3. Tables in Scope

MVP tables:

```text
users
sessions
company_workspaces
workspace_settings
```

Near-MVP / expansion tables:

```text
workspace_access
workspace_members
workspace_profiles
```

Recommended MVP implementation:

```text
users
sessions
company_workspaces
workspace_settings
```

---

# 4. Workspace Boundary Rule

`company_workspaces` is the root boundary table.

All major operating tables must reference:

```text
workspace_id UUID REFERENCES company_workspaces(id)
```

This rule applies to:

- operating maps;
- operating gaps;
- functions;
- responsibilities;
- agents;
- processes;
- tasks;
- decisions;
- memory entries;
- audit events;
- runtime events;
- integrations;
- dashboard metrics;
- export jobs.

---

# 5. users Table

## Purpose

Stores human identity records.

## Domain Entity

```text
User
```

## Table

```text
users
```

## Columns

```text
id UUID PRIMARY KEY
email TEXT NOT NULL UNIQUE
name TEXT NULL
status TEXT NOT NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## Status Values

Initial values:

```text
active
inactive
blocked
archived
```

## Notes

The `users` table is global, not workspace-scoped.

A user may own or access multiple workspaces later.

---

# 6. sessions Table

## Purpose

Stores authenticated session references or security-related session records.

## Domain Entity

```text
Session
```

## Table

```text
sessions
```

## Columns

```text
id UUID PRIMARY KEY
user_id UUID NOT NULL REFERENCES users(id)
status TEXT NOT NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
expires_at TIMESTAMPTZ NULL
last_seen_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## Status Values

Initial values:

```text
active
expired
revoked
```

## Notes

Actual authentication may be handled by an external provider, but Bizzi may keep session records for audit, security events and runtime correlation.

---

# 7. company_workspaces Table

## Purpose

Stores company workspace records as root operating boundaries.

## Domain Entity

```text
CompanyWorkspace
```

## Table

```text
company_workspaces
```

## Columns

```text
id UUID PRIMARY KEY
owner_user_id UUID NOT NULL REFERENCES users(id)
name TEXT NOT NULL
slug TEXT UNIQUE NULL
industry TEXT NULL
business_type TEXT NULL
company_size TEXT NULL
country TEXT NULL
language TEXT NULL
timezone TEXT NULL
default_currency TEXT NULL
status TEXT NOT NULL
onboarding_status TEXT NULL
operating_pain_points TEXT NULL
control_level TEXT NULL
ai_usage_level TEXT NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
archived_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## Status Values

Initial workspace status values:

```text
created
onboarding
active
paused
archived
```

## Onboarding Status Values

Initial onboarding values:

```text
not_started
in_progress
completed
skipped
```

## Notes

This table may store basic profile fields directly in MVP.

A separate `workspace_profiles` table can be added later if profile data becomes large or versioned.

---

# 8. workspace_settings Table

## Purpose

Stores configuration for a workspace.

## Domain Entity

```text
WorkspaceSettings
```

## Table

```text
workspace_settings
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
language TEXT NULL
timezone TEXT NULL
default_currency TEXT NULL
ai_assistance_enabled BOOLEAN NOT NULL DEFAULT true
memory_enabled BOOLEAN NOT NULL DEFAULT true
audit_enabled BOOLEAN NOT NULL DEFAULT true
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## Constraints

Recommended:

```text
UNIQUE(workspace_id)
```

## Notes

Each workspace should normally have exactly one settings record.

---

# 9. workspace_access Table

## Purpose

Stores user access to workspaces for future multi-user collaboration.

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
metadata JSONB NULL
```

## Constraints

Recommended:

```text
UNIQUE(workspace_id, user_id)
```

## Notes

MVP may rely on `company_workspaces.owner_user_id` before enabling this table fully.

---

# 10. workspace_profiles Table

## Purpose

Stores extended structured company profile context.

## MVP Status

```text
Optional / Expansion
```

## Table

```text
workspace_profiles
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
company_description TEXT NULL
business_model TEXT NULL
primary_customers TEXT NULL
main_products_or_services TEXT NULL
main_operating_challenges TEXT NULL
strategic_goals TEXT NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## MVP Simplification

These fields may initially live in:

```text
company_workspaces.metadata
```

or as selected direct columns on `company_workspaces`.

---

# 11. Relationships

## User to Workspace

```text
users.id → company_workspaces.owner_user_id
```

Relationship:

```text
User 1 → many CompanyWorkspaces
```

## Workspace to Settings

```text
company_workspaces.id → workspace_settings.workspace_id
```

Relationship:

```text
CompanyWorkspace 1 → 1 WorkspaceSettings
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

# 12. Workspace Creation Flow Persistence

```text
Create user or identify existing user
↓
Insert company_workspaces
↓
Insert workspace_settings
↓
Emit workspace.created runtime event
↓
Insert audit_events record
↓
Create initial dashboard metrics
```

Required tables:

```text
users
company_workspaces
workspace_settings
runtime_events
audit_events
dashboard_metrics
```

---

# 13. Workspace Context Assembly

Workspace context is usually derived from multiple tables:

```text
company_workspaces
workspace_settings
operating_maps
functions
responsibilities
tasks
decisions
memory_entries
agents
integrations
dashboard_metrics
```

Recommended implementation:

```text
Do not persist WorkspaceContext as a core table in MVP.
Assemble context through backend services and scoped queries.
```

---

# 14. Workspace Isolation Requirements

Every operating query must include:

```text
WHERE workspace_id = :workspace_id
```

This protects:

- tenant isolation;
- AI context safety;
- dashboard accuracy;
- export security;
- audit filtering;
- memory retrieval.

---

# 15. Indexing Requirements

## users

```text
UNIQUE(email)
INDEX(status)
```

## sessions

```text
INDEX(user_id)
INDEX(status)
INDEX(expires_at)
```

## company_workspaces

```text
INDEX(owner_user_id)
UNIQUE(slug)
INDEX(status)
INDEX(owner_user_id, status)
```

## workspace_settings

```text
UNIQUE(workspace_id)
```

## workspace_access

```text
UNIQUE(workspace_id, user_id)
INDEX(user_id)
INDEX(workspace_id, status)
```

---

# 16. Security Rules

Database-level and service-level rules should ensure:

```text
workspace must have owner_user_id
workspace settings must belong to valid workspace
workspace access must reference valid user and workspace
archived workspaces cannot be modified through normal service flows
AI context assembly must use one workspace_id only
exports must use one workspace_id only
```

---

# 17. Audit Requirements

Workspace actions that should create audit records:

```text
workspace.created
workspace.updated
workspace.settings_updated
workspace.owner_changed
workspace.status_changed
workspace.archived
workspace.access_granted
workspace.access_revoked
workspace.access_denied
```

Audit target pattern:

```text
object_type = 'company_workspace'
object_id = company_workspaces.id
```

---

# 18. Runtime Event Requirements

Workspace events:

```text
workspace.created
workspace.initialized
workspace.profile_updated
workspace.settings_updated
workspace.owner_assigned
workspace.status_changed
workspace.archived
workspace.context_loaded
```

Runtime event source pattern:

```text
source_object_type = 'company_workspace'
source_object_id = company_workspaces.id
```

---

# 19. Data Integrity Rules

Recommended integrity rules:

```text
company_workspaces.owner_user_id IS NOT NULL
company_workspaces.name IS NOT NULL
workspace_settings.workspace_id IS UNIQUE
workspace_access.workspace_id + user_id IS UNIQUE
workspace status must be controlled
session status must be controlled
```

Service-level validation should also enforce:

```text
cannot archive workspace without authorization
cannot update archived workspace through normal flows
cannot load workspace context for unauthorized user
```

---

# 20. MVP Simplifications

For MVP, Bizzi may simplify by:

- using `owner_user_id` instead of full `workspace_access`;
- storing profile fields on `company_workspaces`;
- creating one `workspace_settings` record automatically;
- supporting one active workspace per user initially;
- using simple text statuses before formal PostgreSQL ENUM migration.

These simplifications must not break future expansion.

---

# 21. Future Expansion

Future Workspace Data Model may add:

```text
workspace_access
workspace_profiles
workspace_members
roles
permissions
role_permissions
workspace_invitations
workspace_activity_summary
workspace_billing_profile
```

These should be introduced only when product behavior requires them.

---

# 22. Acceptance Criteria

Workspace Data Model is ready when:

- users table is defined;
- sessions table is defined;
- company_workspaces table is defined;
- workspace_settings table is defined;
- workspace access expansion path is defined;
- workspace scoping rules are explicit;
- indexes are identified;
- audit and event requirements are defined;
- MVP simplifications are documented.

Status:

```text
Accepted for Implementation Planning
```

---

# 23. Final Workspace Data Model Statement

```text
Bizzi Workspace Data Model defines the durable database foundation for company workspaces as the root operating boundary of the platform, preserving ownership, settings, isolation, auditability and future collaboration readiness.
```

This model anchors all other workspace-scoped Bizzi data.