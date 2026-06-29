# 17_DATABASE_MIGRATION_STRATEGY.md

# Bizzi Platform

## Database Migration Strategy

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Standard Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Previous Documents:** 00_DATA_MODEL_VISION.md through 16_DATABASE_NAMING_CONVENTIONS.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the database migration strategy for Bizzi Platform.

It establishes how schema changes should be planned, named, reviewed, applied, rolled back and governed as Bizzi moves from architecture into API contracts, backend services, ORM models and production-ready database implementation.

Core question:

```text
How should Bizzi evolve its database schema safely without breaking product behavior, workspace isolation, auditability or future implementation layers?
```

---

# 2. Migration Strategy Role

Database migrations are the controlled mechanism for changing the physical database schema.

They support:

- initial schema creation;
- table additions;
- column additions;
- index creation;
- constraint hardening;
- enum evolution;
- data backfills;
- compatibility between backend versions;
- audit-safe schema evolution;
- rollback planning;
- production deployment discipline.

---

# 3. Core Migration Principles

## 3.1 Migrations Are Product Changes

A migration is not just a technical operation.

It can affect:

- API behavior;
- backend validation;
- dashboard queries;
- audit records;
- memory retrieval;
- AI context assembly;
- export generation;
- integrations;
- security rules.

Rule:

```text
Every schema migration must be treated as a product-impacting change.
```

---

## 3.2 Prefer Additive Changes

Safe migrations should prefer:

```text
add table
add nullable column
add index
add optional constraint
add reference table
```

Avoid early destructive changes:

```text
drop table
drop column
rename column
change data type destructively
make nullable column NOT NULL without backfill
```

---

## 3.3 Backward Compatibility First

Migrations should support running old and new application versions during deployment.

Rule:

```text
Database changes should usually be backward-compatible before backend code depends on them.
```

---

## 3.4 Data Safety Before Schema Purity

Perfect schema is less important than preserving existing data.

Rule:

```text
Never destroy business data without explicit migration plan, backup and approval.
```

---

## 3.5 Workspace Isolation Must Be Preserved

Any new operating table must include:

```text
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
```

unless explicitly global.

Rule:

```text
No workspace_id, no operating record.
```

---

# 4. Migration File Naming

Migration files should use chronological ordering.

Recommended pattern:

```text
YYYYMMDDHHMMSS_<action>_<object>.sql
```

Examples:

```text
20260701090000_create_users.sql
20260701090500_create_company_workspaces.sql
20260701100000_add_workspace_id_to_tasks.sql
20260701110000_create_runtime_events.sql
20260701120000_add_task_status_index.sql
```

Naming rules:

- use UTC timestamp;
- use snake_case;
- describe the action clearly;
- avoid vague names like `update_schema.sql`;
- one migration should have one coherent purpose.

---

# 5. Migration Categories

## 5.1 Schema Creation Migrations

Used for creating new tables, constraints and indexes.

Examples:

```text
create_users
create_company_workspaces
create_tasks
create_audit_events
```

## 5.2 Additive Change Migrations

Used for adding optional fields or supporting tables.

Examples:

```text
add_review_date_to_memory_entries
add_workspace_access
add_export_scope_to_export_jobs
```

## 5.3 Constraint Migrations

Used for adding validation after data is clean.

Examples:

```text
add_not_null_to_tasks_status
add_unique_workspace_access_workspace_user
add_check_task_priority
```

## 5.4 Index Migrations

Used for performance and query optimization.

Examples:

```text
add_index_tasks_workspace_status
add_index_audit_events_workspace_timestamp
```

## 5.5 Data Backfill Migrations

Used for populating new fields from existing data.

Examples:

```text
backfill_workspace_settings
backfill_task_source_fields
backfill_memory_status
```

## 5.6 Destructive Migrations

Used for drops, renames or irreversible changes.

These require extra review.

Examples:

```text
drop_legacy_task_field
rename_memory_type_column
change_status_to_enum
```

---

# 6. Recommended Migration Order for MVP

Initial Bizzi MVP schema should be created in dependency order:

```text
users
sessions
company_workspaces
workspace_settings
operating_maps
functions
responsibilities
operating_gaps
agents
agent_authority_scopes
agent_recommendations
agent_action_drafts
processes
process_steps
tasks
decisions
memory_entries
runtime_events
audit_events
integrations
integration_sync_jobs
security_policies
workspace_access
dashboard_metrics
export_jobs
```

Notes:

- `audit_events` references `runtime_events`, so `runtime_events` should exist first if using strict FK.
- `tasks` and `decisions` may reference each other; use nullable references or add one FK later.
- `agents` and `processes` may reference each other; avoid circular FK dependency in first migration.

---

# 7. Circular Dependency Handling

Some Bizzi objects have natural circular relationships.

Examples:

```text
tasks.decision_id ↔ decisions.task_id
agents.process_id ↔ processes.agent_id
agents.authority_scope_id ↔ agent_authority_scopes.agent_id
```

Migration strategy:

```text
Create primary tables first with nullable reference columns.
Add foreign keys later only where necessary.
Use service-level validation where polymorphic or circular validation is complex.
```

Rule:

```text
Avoid forcing circular database constraints too early.
```

---

# 8. Expand and Contract Pattern

For potentially breaking schema changes, use the expand-and-contract approach.

## Phase 1 — Expand

Add new schema without removing old schema.

```text
add new nullable column
add new table
add new index
```

## Phase 2 — Dual Write or Backfill

Support old and new schema together.

```text
backend writes both old and new fields
migration backfills existing rows
```

## Phase 3 — Read New

Application starts reading from the new structure.

## Phase 4 — Contract

Remove old structure only after stability.

```text
drop old column
drop old table
remove old code path
```

---

# 9. Adding a New Table

Checklist before adding a table:

```text
Does it map to a Domain Model entity?
Is it MVP, governed runtime or expansion?
Does it require workspace_id?
What is the primary key?
What are required timestamps?
What status values apply?
What indexes are needed?
What audit events should changes create?
Does it require seed data?
```

Standard table foundation:

```text
id UUID PRIMARY KEY
workspace_id UUID REFERENCES company_workspaces(id)
status TEXT
created_at TIMESTAMPTZ DEFAULT now()
updated_at TIMESTAMPTZ DEFAULT now()
metadata JSONB
```

Not every table needs every field, but deviations should be intentional.

---

# 10. Adding a New Column

Safe column addition pattern:

```text
add nullable column
ship backend support
backfill if needed
add NOT NULL constraint later if required
add index only if query pattern needs it
```

Avoid:

```text
adding NOT NULL column without default on populated table
changing column meaning without rename or migration note
hiding core data inside metadata
```

---

# 11. Adding Constraints

Constraint addition should be staged.

Safe pattern:

```text
add column or table
backfill existing data
validate data quality
add constraint
monitor errors
```

Constraint candidates:

```text
NOT NULL
UNIQUE
CHECK
FOREIGN KEY
```

Rule:

```text
Do not add strict constraints before existing data satisfies them.
```

---

# 12. Index Migration Strategy

Indexes should follow `12_INDEXING_STRATEGY.md`.

MVP index rule:

```text
Add only indexes that support known product access patterns.
```

Recommended first indexes:

```text
workspace_id
workspace_id + status
workspace_id + type
workspace_id + timestamp
source_object_type + source_object_id
```

Production note:

```text
For large tables, indexes should be created using safe online or concurrent methods where supported.
```

---

# 13. Enum and Status Migration Strategy

MVP approach:

```text
TEXT columns with backend validation
```

Hardening approach:

```text
CHECK constraints for stable values
PostgreSQL ENUM for very stable lifecycle values
reference tables for admin-managed values
```

Recommended evolution:

```text
document values
validate in backend
clean existing data
add CHECK constraint or ENUM later
```

Avoid:

```text
using UI labels as enum values
renaming enum values without migration plan
hardcoding unstable categories as PostgreSQL ENUM too early
```

---

# 14. Data Backfill Strategy

Backfills should be explicit and reversible where possible.

Backfill checklist:

```text
Which rows are affected?
What source data is used?
Can the backfill be re-run safely?
Does it need batching?
Does it affect audit or runtime events?
Is there a validation query after backfill?
```

Recommended pattern:

```text
Add nullable field
Backfill in batches
Validate counts
Add constraint if needed
```

---

# 15. Rollback Strategy

Every migration should be classified by rollback safety.

## Safe Rollback

Examples:

```text
drop newly added unused table
drop newly added nullable column before usage
drop newly added index
```

## Risky Rollback

Examples:

```text
reverting data backfill
removing columns already used by application
undoing enum changes
```

## Irreversible Migration

Examples:

```text
drop table with data
drop column with data
merge multiple records destructively
```

Rule:

```text
Irreversible migrations require explicit approval and backup plan.
```

---

# 16. Migration Review Checklist

Before applying a migration, review:

```text
Does the migration preserve workspace isolation?
Does it preserve existing data?
Is it backward-compatible?
Does it require backend code changes?
Does it require API changes?
Does it require index updates?
Does it require audit/event changes?
Does it affect AI context or memory retrieval?
Does it need a backfill?
Does it need rollback plan?
```

---

# 17. Migration Testing

Migrations should be tested against:

```text
empty database
sample MVP database
database with realistic workspace data
rollback scenario where possible
backend integration tests
API contract tests where affected
```

Validation queries should confirm:

```text
row counts
foreign key consistency
workspace_id presence
status value validity
index existence
constraint validity
```

---

# 18. Seed Data Strategy

Seed data may include:

```text
initial function categories
default security policies
default workspace settings
default dashboard metric definitions
initial export templates
```

Seed rule:

```text
Seed data should be idempotent and safe to re-run.
```

Avoid seed data that creates user-specific workspace records unless explicitly part of onboarding.

---

# 19. Audit and Event Impact

Schema changes may affect audit and runtime events.

Migration should consider:

```text
new object_type values
new event_type values
new audit action names
new source_object_type references
new dashboard metrics
```

Rule:

```text
Schema evolution must keep audit and event vocabulary aligned with 11_ENUMS_AND_STATUSES.md.
```

---

# 20. Migration Deployment Sequence

Recommended deployment sequence:

```text
1. Apply backward-compatible database migration
2. Deploy backend code that can use new schema
3. Run backfill if needed
4. Enable new feature flag or behavior
5. Monitor audit, events and errors
6. Later remove old schema if necessary
```

For MVP local development, this may be simplified, but the sequence should remain the production target.

---

# 21. Migration Ownership

Each migration should have an owner.

Possible owner roles:

```text
Backend Engineer
Data Architect
Platform Engineer
Technical Lead
```

Approval should be required for:

```text
destructive migrations
security-related migrations
audit/event schema changes
data retention changes
workspace isolation changes
```

---

# 22. Migration Anti-Patterns

Avoid:

```text
manual database edits outside migration system
large destructive changes without backup
renaming columns without compatibility window
adding NOT NULL constraints before backfill
creating tables without workspace_id where required
storing raw secrets during migration
changing status values without code update
adding indexes without query purpose
using one giant migration for unrelated changes
```

---

# 23. Recommended Migration Tooling Direction

Bizzi may use any mature migration tool compatible with the chosen backend stack.

Possible options:

```text
Prisma Migrate
Knex migrations
TypeORM migrations
Flyway
Liquibase
Alembic
Rails migrations
```

Tool choice belongs to implementation architecture.

Data Model rule:

```text
Regardless of tool, migrations must remain versioned, reviewed, repeatable and auditable.
```

---

# 24. Acceptance Criteria

Database Migration Strategy is ready when:

- migration naming is defined;
- migration categories are defined;
- MVP creation order is documented;
- additive and destructive change rules are clear;
- expand-and-contract approach is defined;
- constraint, index and enum migration approaches are defined;
- backfill and rollback rules are documented;
- migration review checklist is provided;
- audit, event and workspace isolation impacts are covered.

Status:

```text
Accepted as Data Model Standard
```

---

# 25. Final Statement

```text
Bizzi Database Migration Strategy defines how the platform evolves its database schema safely, preserving workspace isolation, traceability, auditability, data integrity and implementation compatibility across product versions.
```

This strategy strengthens the `27_DATA_MODEL` layer as a reliable bridge from architecture to production-grade database implementation.