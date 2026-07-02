# 04_DATABASE_MIGRATION_PLAN.md

# Bizzi Platform

## Database Migration Plan

**Layer:** 30_BACKEND_IMPLEMENTATION_PLAN  
**Component Type:** Implementation Planning Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**API Contracts Reference:** 28_API_CONTRACTS  
**Backend Service Reference:** 29_BACKEND_SERVICE_DESIGN  
**Previous Document:** 03_REPOSITORY_STRUCTURE.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the database migration plan for Bizzi Platform backend implementation.

It translates the accepted data model and MVP vertical slice into a safe, staged, versioned and testable database migration sequence using PostgreSQL and Prisma Migrate for the MVP backend.

Core question:

```text
How should Bizzi create and evolve its database schema so that MVP implementation is fast, safe, workspace-scoped, auditable and ready for future expansion?
```

---

# 2. Migration Thesis

```text
Bizzi database migrations should start with the smallest schema required for the MVP vertical slice, while preserving canonical workspace scoping, auditability, runtime events, timestamps, status fields and future expansion paths.
```

Migrations should prove:

```text
workspace persistence
task lifecycle persistence
decision evidence persistence
memory persistence
audit event persistence
runtime event persistence
dashboard-readable state
```

---

# 3. Migration Tool Decision

MVP migration tool:

```text
Prisma Migrate
```

Primary files:

```text
backend/prisma/schema.prisma
backend/prisma/migrations/
backend/prisma/seed.ts
```

Rules:

```text
all schema changes must be migration-backed
no manual production schema changes
migration files must be committed
seed data must be separate from migrations
schema changes must pass local migration reset during MVP
```

---

# 4. Database Platform

Canonical database:

```text
PostgreSQL
```

Required PostgreSQL capabilities:

```text
UUID identifiers
timestamp with timezone
JSONB metadata fields
transactions
foreign keys
indexes for workspace-scoped queries
future full-text search
future vector extension path
```

MVP rule:

```text
Do not use database-specific complexity unless it supports clear MVP requirements.
```

---

# 5. Migration Principles

## 5.1 Workspace Scope First

Every workspace-scoped table must include:

```text
workspace_id
```

## 5.2 Stable IDs

Primary keys should use:

```text
UUID
```

## 5.3 Timestamp Standardization

Core tables should include:

```text
created_at
updated_at
```

Lifecycle tables may include:

```text
archived_at
completed_at
confirmed_at
processed_at
```

## 5.4 Status Fields

Lifecycle entities must include status fields aligned with `27_DATA_MODEL/11_ENUMS_AND_STATUSES.md`.

## 5.5 Audit and Runtime Events From Day One

MVP migrations must include:

```text
audit_events
runtime_events
```

---

# 6. MVP Migration Scope

Required MVP tables:

```text
users
company_workspaces
workspace_settings
tasks
decisions
memory_entries
audit_events
runtime_events
```

Optional early table:

```text
workspace_access
```

Recommendation:

```text
Create workspace_access in the early schema if it does not delay MVP, but implement owner-only authorization first.
```

---

# 7. Deferred Tables

Deferred until after MVP vertical slice:

```text
operating_maps
operating_gaps
operating_recommendations
functions
responsibilities
ownership_gaps
agents
agent_authority_scopes
agent_recommendations
agent_action_drafts
processes
process_steps
integrations
integration_sync_jobs
security_policies
dashboard_metrics
export_jobs
export_files
```

Rule:

```text
Do not create unused tables unless they are needed for the first backend slice or a near-term implementation dependency.
```

---

# 8. Migration Phase Overview

Recommended migration phases:

```text
MIG-001 — Core identity and workspace
MIG-002 — Workspace settings and optional access
MIG-003 — Task execution
MIG-004 — Decision evidence
MIG-005 — Memory entries
MIG-006 — Audit events
MIG-007 — Runtime events
MIG-008 — Dashboard helper indexes
MIG-009 — Export job skeleton optional
MIG-010 — Seed development data
```

---

# 9. MIG-001 — Core Identity and Workspace

Creates:

```text
users
company_workspaces
```

Purpose:

```text
support authenticated actor identity and workspace ownership
```

Required fields for `users`:

```text
id
email
name
status
created_at
updated_at
```

Required fields for `company_workspaces`:

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

Indexes:

```text
users.email unique
company_workspaces.owner_user_id
company_workspaces.slug unique
company_workspaces.status
```

---

# 10. MIG-002 — Workspace Settings and Access

Creates:

```text
workspace_settings
workspace_access optional
```

Required fields for `workspace_settings`:

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

Optional fields for `workspace_access`:

```text
id
workspace_id
user_id
role
status
created_at
updated_at
revoked_at
```

Indexes:

```text
workspace_settings.workspace_id unique
workspace_access.workspace_id
workspace_access.user_id
workspace_access.workspace_id + user_id
workspace_access.workspace_id + role + status
```

MVP rule:

```text
Even if workspace_access exists, owner_user_id remains the MVP authorization source of truth until RBAC expansion is implemented.
```

---

# 11. MIG-003 — Task Execution

Creates:

```text
tasks
```

Required fields:

```text
id
workspace_id
function_id optional later
process_id optional later
owner_user_id optional
agent_id optional later
title
description
status
priority
due_date
completed_at
source_object_type
source_object_id
metadata
created_at
updated_at
archived_at
```

Indexes:

```text
tasks.workspace_id
tasks.workspace_id + status
tasks.workspace_id + owner_user_id
tasks.workspace_id + due_date
tasks.workspace_id + created_at
```

MVP statuses:

```text
open
in_progress
completed
archived
```

---

# 12. MIG-004 — Decision Evidence

Creates:

```text
decisions
```

Required fields:

```text
id
workspace_id
task_id optional
function_id optional later
owner_user_id optional
agent_id optional later
title
description
decision_type
status
decision_date
confirmed_by
confirmed_at
source_object_type
source_object_id
metadata
created_at
updated_at
archived_at
```

Indexes:

```text
decisions.workspace_id
decisions.workspace_id + status
decisions.workspace_id + task_id
decisions.workspace_id + confirmed_at
decisions.workspace_id + created_at
```

MVP statuses:

```text
draft
confirmed
archived
```

---

# 13. MIG-005 — Memory Entries

Creates:

```text
memory_entries
```

Required fields:

```text
id
workspace_id
memory_type
title
summary
content
status
confidence
source_object_type
source_object_id
function_id optional later
process_id optional later
task_id optional
decision_id optional
agent_id optional later
valid_from
valid_until
confirmed_by
confirmed_at
metadata
created_at
updated_at
archived_at
```

Indexes:

```text
memory_entries.workspace_id
memory_entries.workspace_id + status
memory_entries.workspace_id + memory_type
memory_entries.workspace_id + source_object_type + source_object_id
memory_entries.workspace_id + decision_id
memory_entries.workspace_id + task_id
```

MVP statuses:

```text
candidate
active
archived
```

---

# 14. MIG-006 — Audit Events

Creates:

```text
audit_events
```

Required fields:

```text
id
workspace_id
timestamp
actor_type
actor_id
agent_id optional
action
object_type
object_id
source_event_id optional
before_state jsonb optional
after_state jsonb optional
ai_assisted
human_confirmed
severity
correlation_id
metadata jsonb optional
```

Indexes:

```text
audit_events.workspace_id + timestamp
audit_events.workspace_id + action
audit_events.workspace_id + object_type + object_id
audit_events.workspace_id + actor_id
audit_events.workspace_id + correlation_id
```

Rule:

```text
Audit events are append-oriented and should not be updated by normal service flows.
```

---

# 15. MIG-007 — Runtime Events

Creates:

```text
runtime_events
```

Required fields:

```text
id
workspace_id
event_type
status
source_object_type
source_object_id
actor_type
actor_id
agent_id optional
payload jsonb optional
correlation_id
causation_id optional
timestamp
processed_at
failed_at
failure_reason optional
attempt_count
```

Indexes:

```text
runtime_events.workspace_id + timestamp
runtime_events.workspace_id + event_type
runtime_events.workspace_id + status
runtime_events.workspace_id + source_object_type + source_object_id
runtime_events.workspace_id + correlation_id
```

MVP statuses:

```text
pending
processed
failed
ignored
```

---

# 16. MIG-008 — Dashboard Helper Indexes

Dashboard MVP uses live counts, not persisted dashboard metrics.

Required support:

```text
task status count by workspace
decision status count by workspace
memory status count by workspace
recent audit events by workspace
recent runtime events by workspace
```

This phase verifies or adds indexes for:

```text
tasks.workspace_id + status
decisions.workspace_id + status
memory_entries.workspace_id + status
audit_events.workspace_id + timestamp
runtime_events.workspace_id + timestamp
```

Rule:

```text
Do not create dashboard_metrics table until metrics persistence is needed.
```

---

# 17. MIG-009 — Export Job Skeleton Optional

Optional table if export MVP is included early:

```text
export_jobs
```

Required fields:

```text
id
workspace_id
export_type
format
status
requested_by
export_scope jsonb
created_at
updated_at
started_at
completed_at
failed_at
cancelled_at
error_message
```

MVP may defer export jobs until after dashboard slice passes.

---

# 18. MIG-010 — Seed Development Data

Seed data should include:

```text
development user
development workspace
default workspace settings
sample task
sample decision
sample memory entry optional
```

Rules:

```text
seed data is for local development only
seed data must not include real secrets
seed script should be repeatable or reset-aware
```

---

# 19. Prisma Schema Organization

Initial Prisma schema may be single-file for MVP:

```text
backend/prisma/schema.prisma
```

Future split options:

```text
schema.prisma with generated sections
module-specific Prisma schema fragments if tooling supports it
SQL migration files for complex changes
```

MVP rule:

```text
Keep Prisma schema simple and readable until module count requires refactoring.
```

---

# 20. Enum Strategy

MVP may use either:

```text
Prisma enums
text fields with service-level validation
```

Recommended MVP:

```text
Use Prisma enums for stable core statuses and text fields for fast-evolving categories when needed.
```

Stable MVP enums:

```text
workspace_status
task_status
decision_status
memory_status
runtime_event_status
```

Rule:

```text
Enum values must align with 27_DATA_MODEL/11_ENUMS_AND_STATUSES.md.
```

---

# 21. Foreign Key Strategy

Use foreign keys for stable, direct relations:

```text
workspace_settings.workspace_id → company_workspaces.id
tasks.workspace_id → company_workspaces.id
decisions.workspace_id → company_workspaces.id
memory_entries.workspace_id → company_workspaces.id
audit_events.workspace_id → company_workspaces.id
runtime_events.workspace_id → company_workspaces.id
```

Polymorphic references use:

```text
source_object_type
source_object_id
object_type
object_id
```

Rule:

```text
Polymorphic references require service-level validation because database-level foreign keys cannot enforce all object types.
```

---

# 22. Metadata JSONB Strategy

Metadata fields are allowed for extension.

Rules:

```text
metadata is optional
metadata must not replace canonical fields
metadata must not contain raw secrets
metadata should be sanitized before audit/event storage
metadata fields should not be used for high-frequency indexed queries without later schema promotion
```

---

# 23. Migration Naming Rules

Recommended migration names:

```text
001_core_identity_workspace
002_workspace_settings_access
003_task_execution
004_decision_evidence
005_memory_entries
006_audit_events
007_runtime_events
008_dashboard_indexes
009_export_jobs_optional
```

Prisma-generated migration folders may include timestamps, but the descriptive suffix should remain clear.

---

# 24. Rollback Strategy

MVP rollback approach:

```text
local development may use prisma migrate reset
staging rollback should restore database backup or apply forward-fix migration
production rollback should prefer forward-only fixes after launch
```

Rules:

```text
never edit applied production migrations
create new migrations for fixes
backup before destructive changes
avoid destructive migrations during MVP unless reset environment only
```

---

# 25. Migration Verification

Every migration phase must pass:

```text
prisma format
prisma validate
prisma migrate dev locally
prisma migrate reset in local test database
seed script execution
repository tests for affected tables
workspace isolation tests for workspace-scoped tables
```

---

# 26. Data Safety Rules

Safety rules:

```text
no hard delete for confirmed business records in normal service flows
archived_at preferred for historical records
raw secrets must not be stored in audit_events or runtime_events
credential_ref only for future integrations
signed URLs must not be stored in audit payloads when avoidable
```

---

# 27. MVP Acceptance Criteria

Database migration plan is accepted when:

- migration tool is selected;
- PostgreSQL target is defined;
- MVP tables are identified;
- deferred tables are identified;
- migration phases are documented;
- table field expectations are defined;
- workspace indexes are defined;
- audit and runtime event tables are included;
- enum strategy is defined;
- foreign key strategy is defined;
- metadata strategy is defined;
- rollback and verification rules are documented;
- seed data expectations are defined.

Status:

```text
Accepted for API Route Implementation Plan
```

---

# 28. Final Statement

```text
Bizzi Database Migration Plan defines the staged PostgreSQL schema path required to implement the first backend vertical slice while preserving workspace isolation, lifecycle integrity, auditability, runtime coordination and future expansion readiness.
```

This plan gives backend implementation a safe database foundation before API routes and services are coded.