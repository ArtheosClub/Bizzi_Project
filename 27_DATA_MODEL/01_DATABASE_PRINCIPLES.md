# 01_DATABASE_PRINCIPLES.md

# Bizzi Platform

## Database Principles

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Architecture Principles  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Previous Document:** 00_DATA_MODEL_VISION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the database principles for Bizzi Platform.

These principles guide how the Domain Model is translated into relational database structures, ensuring that Bizzi remains workspace-scoped, secure, traceable, auditable and ready for MVP implementation.

Core question:

```text
What database design rules must Bizzi follow so that product architecture becomes reliable, maintainable and implementation-ready storage?
```

---

# 2. Database Role

The database is the durable operating memory of Bizzi.

It stores:

- users;
- workspaces;
- operating maps;
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
- security policies;
- dashboard metrics;
- export jobs.

The database must preserve the governance rules already defined by Runtime Platform and Domain Model.

---

# 3. Primary Database Choice

Recommended database for MVP:

```text
PostgreSQL
```

PostgreSQL is selected because it supports:

- relational integrity;
- foreign keys;
- transactions;
- UUIDs;
- JSONB;
- indexing strategies;
- full-text search options;
- mature ORM support;
- SaaS-ready workspace scoping.

---

# 4. Principle 1 — Workspace Scope First

Most Bizzi tables must include:

```text
workspace_id
```

Rule:

```text
All operating data must be scoped to one workspace unless explicitly global.
```

Applies to:

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
- exports.

---

# 5. Principle 2 — UUID Primary Keys

All primary domain tables should use UUID identifiers.

Standard pattern:

```sql
id UUID PRIMARY KEY
```

Reasons:

- stable API references;
- safe object creation;
- future distributed compatibility;
- no sequential ID leakage;
- clean cross-table references.

---

# 6. Principle 3 — Relational Integrity for Core Links

Core relationships should use explicit foreign keys.

Examples:

```sql
workspace_id UUID REFERENCES company_workspaces(id)
owner_user_id UUID REFERENCES users(id)
function_id UUID REFERENCES functions(id)
process_id UUID REFERENCES processes(id)
decision_id UUID REFERENCES decisions(id)
agent_id UUID REFERENCES agents(id)
```

Relational integrity should protect the platform from orphaned core records.

---

# 7. Principle 4 — Common Columns for Operating Tables

Most operating tables should follow a common column pattern:

```text
id
workspace_id
status
created_at
updated_at
created_by
```

Optional common fields:

```text
archived_at
source_object_type
source_object_id
metadata
```

Consistency across tables makes API, backend and dashboard implementation simpler.

---

# 8. Principle 5 — Statuses Must Be Controlled

Statuses should be represented through controlled values.

Possible implementation options:

```text
PostgreSQL ENUM
CHECK constraints
reference tables
application-level enums plus database validation
```

MVP recommendation:

```text
Use clear enum-like values and document them in 11_ENUMS_AND_STATUSES.md.
```

Statuses should not become arbitrary text.

---

# 9. Principle 6 — JSONB Is Allowed, But Not for Core Meaning

JSONB may be used for flexible metadata.

Good uses:

```text
metadata
payload
configuration
before_state
after_state
mapping_rules
suggested_object_payload
```

Bad uses:

```text
hiding core relationships
storing all task fields
storing all decision fields
replacing proper indexes
bypassing validation
```

Rule:

```text
Use JSONB for flexibility, not for avoiding data modeling.
```

---

# 10. Principle 7 — Audit and Events Are First-Class Tables

Audit and runtime events are not log files only.

They are product data.

Core tables:

```text
audit_events
runtime_events
```

They support:

- traceability;
- debugging;
- dashboard updates;
- memory source tracking;
- security review;
- export history;
- AI accountability.

---

# 11. Principle 8 — Source Traceability Must Be Preserved

Many records should support:

```text
source_object_type
source_object_id
```

This allows Bizzi to answer:

```text
Where did this object come from?
```

Applies especially to:

- operating gaps;
- recommendations;
- agent outputs;
- tasks;
- decisions;
- memory entries;
- dashboard insights;
- export jobs.

---

# 12. Principle 9 — AI Output Must Stay Reviewable

AI-generated objects must not automatically become official operating records.

Recommended pattern:

```text
candidate
suggested
draft
confirmed
rejected
```

Tables supporting this include:

```text
agent_recommendations
agent_action_drafts
operating_recommendations
memory_entries
tasks
decisions
```

Rule:

```text
AI output should be persisted with status and confirmation metadata.
```

---

# 13. Principle 10 — Human Confirmation Must Be Queryable

For sensitive AI-assisted actions, data should support:

```text
confirmed_by
confirmed_at
human_confirmed
```

This is important for:

- agent outputs;
- decisions;
- memory entries;
- operating map confirmation;
- exports;
- authority changes.

---

# 14. Principle 11 — Archived Records Are Retained

Bizzi should prefer archival over deletion for important operating records.

Standard field:

```text
archived_at
```

Optional fields:

```text
archived_by
archive_reason
```

Rule:

```text
Important business objects should be archived, not silently deleted.
```

---

# 15. Principle 12 — Security Data Must Not Expose Secrets

Credential values must not be stored in ordinary application tables.

Allowed:

```text
credential_ref
credential_reference_id
provider
scope
status
```

Not allowed:

```text
raw_access_token
raw_api_key
raw_secret
password_plaintext
```

Secrets must be handled through secure secret storage outside normal runtime objects.

---

# 16. Principle 13 — Index for Runtime Queries

Indexes should support the most common product queries.

Common patterns:

```text
workspace_id
workspace_id + status
workspace_id + created_at
workspace_id + updated_at
workspace_id + owner_user_id
source_object_type + source_object_id
```

Dashboard and audit queries should be considered early.

---

# 17. Principle 14 — MVP Schema Before Perfect Schema

The first implementation should not over-normalize every optional concept.

Supporting entities may start as:

- columns;
- JSONB metadata;
- simple references;
- application-level structures.

Later they can become dedicated tables when product behavior proves they are needed.

Rule:

```text
Normalize core objects. Simplify supporting objects.
```

---

# 18. Principle 15 — Migrations Must Be Safe

Future schema changes must be reversible where practical and safe for data.

Migration principles:

- avoid destructive changes without backup;
- add columns before requiring them;
- backfill before enforcing constraints;
- preserve audit history;
- document enum changes;
- avoid breaking existing API contracts unexpectedly.

---

# 19. Principle 16 — Naming Must Be Consistent

Recommended table naming:

```text
snake_case_plural
```

Examples:

```text
company_workspaces
workspace_settings
operating_maps
agent_recommendations
memory_entries
audit_events
runtime_events
```

Recommended column naming:

```text
snake_case
```

Examples:

```text
workspace_id
owner_user_id
created_at
source_object_type
```

---

# 20. Principle 17 — Data Model Must Support API Filtering

API filtering should be supported by the database.

Common API filters:

```text
workspace_id
status
owner_user_id
function_id
process_id
agent_id
created_at
updated_at
due_date
memory_type
event_type
action
```

Indexes should be aligned with these access patterns.

---

# 21. Principle 18 — Data Model Must Support Dashboard Performance

Dashboard is a first-hour value surface.

The schema must support fast queries for:

- open tasks;
- ownership gaps;
- active functions;
- recent decisions;
- active agents;
- memory count;
- recent audit events;
- security warnings;
- integration status.

This may require targeted indexes and future materialized views.

---

# 22. Principle 19 — Data Model Must Support Export Control

Exports must be represented as governed jobs.

Core table:

```text
export_jobs
```

Export data should include:

```text
workspace_id
requested_by
export_type
export_scope
status
file_reference
created_at
completed_at
```

Exports must be auditable and workspace-scoped.

---

# 23. Principle 20 — Database Is Not the Only Guardrail

The database enforces structure.

Backend services enforce business rules.

Example:

```text
Database stores task.status.
TaskService validates allowed status transitions.
AuditService records the change.
EventService emits task.status_changed.
```

The database should not carry all domain logic alone.

---

# 24. MVP Database Standard

For MVP, Bizzi should prioritize:

```text
PostgreSQL
UUID primary keys
workspace_id on operating tables
created_at / updated_at timestamps
explicit foreign keys for core relations
JSONB for metadata and event payloads
controlled status values
basic indexes for workspace and status queries
audit_events and runtime_events as first-class tables
```

---

# 25. Anti-Patterns to Avoid

Avoid:

```text
single giant JSON table
chat-history-only persistence
unscoped workspace records
raw secrets in tables
missing audit trail
unindexed dashboard queries
arbitrary status text
hard deletes of important objects
AI outputs becoming official without confirmation
foreign keys omitted for core relationships
```

---

# 26. Acceptance Criteria

Database Principles are accepted when they:

- support the Domain Model;
- preserve workspace isolation;
- define primary key strategy;
- define relationship strategy;
- define audit and event strategy;
- define JSONB usage limits;
- define status control;
- define indexing direction;
- protect secrets;
- support MVP implementation.

Status:

```text
Accepted for Data Model Design
```

---

# 27. Final Database Principles Statement

```text
Bizzi database design must transform the Domain Model into durable, relational, workspace-scoped, traceable, auditable and implementation-ready storage while preserving MVP simplicity and future scalability.
```

These principles guide all following files in the `27_DATA_MODEL` layer.