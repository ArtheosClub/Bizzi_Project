# 19_DATABASE_EVOLUTION_GUIDE.md

# Bizzi Platform

## Database Evolution Guide

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Governance and Evolution Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Previous Documents:** 00_DATA_MODEL_VISION.md through 18_DATA_RETENTION_POLICY.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines how the Bizzi Platform database model should evolve over time.

It connects the Data Model, Naming Conventions, Migration Strategy and Retention Policy into a practical guide for future schema changes, product growth, implementation phases and long-term platform maintainability.

Core question:

```text
How should Bizzi evolve its database architecture without breaking product coherence, workspace isolation, auditability or AI governance?
```

---

# 2. Evolution Guide Role

The Database Evolution Guide provides direction for:

- moving from MVP schema to production schema;
- deciding when to add new tables;
- deciding when to split JSONB into relational columns;
- introducing constraints safely;
- evolving enums and statuses;
- scaling indexes;
- adding search and vector capabilities;
- supporting multi-user workspaces;
- preserving audit and memory continuity;
- keeping database architecture aligned with product layers.

---

# 3. Evolution Principles

## 3.1 Product Behavior Drives Schema Evolution

Database changes should be triggered by real product behavior.

Rule:

```text
Do not add tables, indexes or abstractions before the product needs them.
```

## 3.2 Preserve Canonical Meaning

The Data Model must stay aligned with Domain Model and Runtime Platform meaning.

Rule:

```text
A table or field should represent a stable Bizzi concept, not a temporary UI workaround.
```

## 3.3 Evolve Additively First

Schema evolution should prefer additive changes before destructive changes.

Rule:

```text
Add first, migrate behavior, then remove later only when safe.
```

## 3.4 Keep Workspace Isolation Explicit

Every new operating table must preserve workspace scoping.

Rule:

```text
Any table containing business operating data must include workspace_id unless explicitly global.
```

## 3.5 Preserve Audit and Traceability

Schema changes must not break existing audit chains.

Rule:

```text
If a record can affect business meaning, its origin and changes should remain traceable.
```

---

# 4. Evolution Stages

Bizzi database evolution should proceed through stages.

## Stage 1 — MVP Durable Core

Goal:

```text
Support first runnable vertical slice.
```

Tables:

```text
users
sessions
company_workspaces
workspace_settings
operating_maps
operating_gaps
functions
responsibilities
tasks
decisions
memory_entries
audit_events
runtime_events
dashboard_metrics
```

Characteristics:

- simple text statuses;
- minimal constraints;
- core workspace indexes;
- JSONB for flexible metadata;
- service-level validation;
- dynamic dashboard where possible.

---

## Stage 2 — Governed Runtime

Goal:

```text
Add structured AI governance, processes, integrations, access and exports.
```

Tables:

```text
agents
agent_authority_scopes
agent_recommendations
agent_action_drafts
processes
process_steps
integrations
integration_sync_jobs
security_policies
workspace_access
export_jobs
```

Characteristics:

- AI outputs become reviewable records;
- process structure becomes persistent;
- integrations become governed;
- export lifecycle is tracked;
- workspace access expands beyond owner-only model.

---

## Stage 3 — Collaboration and Control

Goal:

```text
Support teams, roles, deeper governance and operating reviews.
```

Likely tables:

```text
roles
permissions
role_permissions
workspace_invitations
ownership_gaps
responsibility_assignments
process_reviews
task_comments
task_history
decision_reviews
```

Characteristics:

- multi-user access control;
- role-based permissions;
- richer collaboration history;
- responsibility lifecycle;
- process maturity tracking.

---

## Stage 4 — Intelligence and Search

Goal:

```text
Improve retrieval, AI context, recommendations and insight generation.
```

Likely tables or infrastructure:

```text
memory_sources
memory_usage
memory_reviews
memory_embeddings
search_indexes
recommendation_feedback
dashboard_insights
```

Characteristics:

- full-text search;
- semantic search;
- memory usage tracking;
- recommendation quality feedback;
- AI explainability improvements.

---

## Stage 5 — Enterprise Hardening

Goal:

```text
Support enterprise-scale governance, compliance and operational resilience.
```

Likely additions:

```text
audit_exports
security_events
policy_versions
data_retention_jobs
data_redaction_requests
export_files
scheduled_reports
workspace_billing_profile
```

Characteristics:

- stronger constraints;
- retention automation;
- partitioning or archiving;
- compliance workflows;
- reporting and scheduled exports;
- production monitoring support.

---

# 5. When to Add a New Table

Add a new table when the concept:

```text
has its own lifecycle
needs separate ownership
needs separate audit trail
is queried independently
has many records per parent
requires permissions
requires retention policy
would make JSONB too opaque
```

Examples:

```text
process_steps should be a table because steps have order and lifecycle.
export_jobs should be a table because exports have status and audit needs.
workspace_access should be a table because access is independent and security-sensitive.
```

Do not add a new table when:

```text
the data is temporary
there is no product behavior yet
the data is simple metadata
the concept is not stable
```

---

# 6. When to Add a New Column

Add a new column when the field:

```text
is frequently queried
is part of business logic
is part of validation
is needed for indexing
is needed for permissions
is needed for audit or traceability
has stable meaning across the product
```

Examples:

```text
status
workspace_id
owner_user_id
confirmed_at
source_object_type
source_object_id
```

Keep data in JSONB when:

```text
structure is unstable
field is rarely queried
field is provider-specific configuration
field is optional metadata
```

---

# 7. When to Split JSONB

JSONB should be split into relational columns or tables when:

```text
queries depend on specific JSON fields
validation becomes important
indexes are needed
permissions depend on the field
analytics depends on the field
field meaning becomes stable
multiple services need the same field
```

Example evolution:

```text
integrations.configuration JSONB
↓
frequently used provider setting becomes column
↓
integration_scopes table added for normalized scope control
```

Rule:

```text
JSONB is a flexibility tool, not a hiding place for core domain structure.
```

---

# 8. Status Evolution

MVP may use text statuses with backend validation.

Evolution path:

```text
TEXT status
↓
centralized backend enum validation
↓
data cleanup and validation queries
↓
CHECK constraint or PostgreSQL ENUM for stable values
```

Stable candidates:

```text
task_status
decision_status
memory_status
runtime_event_status
export_status
```

Avoid making unstable categories into database enums too early.

---

# 9. Constraint Evolution

Constraints should harden over time.

MVP:

```text
basic primary keys
basic foreign keys
minimal NOT NULL
service-level validation
```

Production hardening:

```text
NOT NULL after backfill
UNIQUE where product rules are stable
CHECK constraints for stable statuses
foreign keys for stable relationships
partial unique indexes for active records
```

Rule:

```text
Add constraints when the product rule is stable and existing data is clean.
```

---

# 10. Index Evolution

Indexes should evolve from product usage.

MVP:

```text
workspace_id
workspace_id + status
workspace_id + type
owner_user_id
source_object_type + source_object_id
```

Later:

```text
partial indexes
GIN indexes for JSONB or tags
full-text indexes
vector indexes
partition-aware indexes
```

Rule:

```text
Measure query behavior before adding advanced indexes.
```

---

# 11. Search Evolution

Bizzi search should evolve in phases.

## Phase 1 — Structured Filtering

Use relational filters:

```text
workspace_id
status
owner_user_id
function_id
memory_type
decision_date
```

## Phase 2 — Full-Text Search

Use full-text search for:

```text
memory_entries.title
memory_entries.content
memory_entries.summary
tasks.title
decisions.title
```

## Phase 3 — Semantic Search

Use embeddings for:

```text
memory retrieval
AI context assembly
similar decisions
similar operating gaps
recommendation support
```

Rule:

```text
Semantic search must remain workspace-scoped and security-aware.
```

---

# 12. Memory Evolution

Memory should evolve carefully because it affects AI behavior.

MVP:

```text
memory_entries with source fields
```

Next:

```text
memory_sources
memory_reviews
memory_usage
```

Later:

```text
memory_embeddings
memory_quality_scores
memory_retention_rules
```

Rule:

```text
AI memory should become more structured only after usage patterns are understood.
```

---

# 13. Audit and Event Evolution

MVP:

```text
audit_events
runtime_events
```

Next:

```text
event_failures
event_handler_runs
audit_exports
```

Later:

```text
event_subscriptions
policy_versions
security_events
observability projections
```

Rule:

```text
Audit records preserve evidence; runtime events coordinate product behavior. Do not merge their purposes.
```

---

# 14. Access Control Evolution

MVP:

```text
company_workspaces.owner_user_id
```

Near-MVP:

```text
workspace_access
```

Later:

```text
roles
permissions
role_permissions
workspace_invitations
access_decisions
```

Rule:

```text
Access control should evolve from owner-only to role-based only when collaboration behavior requires it.
```

---

# 15. Integration Evolution

MVP:

```text
integrations
integration_sync_jobs
credential_ref
scopes JSONB
```

Next:

```text
integration_scopes
integration_mappings
integration_credential_references
```

Later:

```text
webhook_events
integration_rate_limits
integration_health_snapshots
```

Rule:

```text
Never evolve integrations in a way that stores raw credentials in runtime tables.
```

---

# 16. Dashboard and Export Evolution

MVP:

```text
dashboard_metrics
export_jobs
```

Next:

```text
dashboard_alerts
dashboard_insights
export_files
export_templates
```

Later:

```text
dashboard_snapshots
scheduled_reports
report_subscriptions
```

Rule:

```text
Persist dashboard data only when it improves performance, auditability or user-facing history.
```

---

# 17. Retention Evolution

MVP:

```text
manual retention rules
archived_at fields
export file expiration
session expiration
```

Next:

```text
retention jobs
retention classifications
redaction workflows
```

Later:

```text
legal hold
privacy request processing
backup retention alignment
policy-driven deletion
```

Rule:

```text
Retention automation must be conservative until legal and compliance policies are defined.
```

---

# 18. Versioning Evolution

Some objects may require versioning later.

Likely candidates:

```text
operating_maps
processes
security_policies
export_templates
memory_entries
```

Versioning options:

```text
version column
snapshot table
history table
event-derived history
```

Rule:

```text
Add versioning when users need comparison, rollback, review or historical reporting.
```

---

# 19. Partitioning Evolution

Partitioning may be needed later for high-volume tables.

Likely candidates:

```text
audit_events
runtime_events
integration_sync_jobs
memory_usage
security_events
```

Possible partition keys:

```text
workspace_id
timestamp
created_at
```

Rule:

```text
Do not partition until data volume and query patterns justify the operational complexity.
```

---

# 20. Deprecation Strategy

Deprecating a table or field should follow:

```text
mark as deprecated in documentation
stop writing new data
migrate or backfill replacement data
stop reading old field
archive old data if needed
drop only after safe window
```

Rule:

```text
Do not silently repurpose old fields with new meaning.
```

---

# 21. Architecture Decision Records

Major database evolution decisions should create an ADR.

ADR-worthy changes:

```text
introducing full RBAC
introducing vector search
partitioning audit_events
moving statuses to PostgreSQL ENUM
adding billing tables
changing retention policy
introducing event outbox
```

ADR should capture:

```text
context
decision
alternatives
consequences
migration impact
rollback impact
```

---

# 22. Evolution Review Checklist

Before changing the database model, review:

```text
Does this change map to a real product behavior?
Does it preserve workspace isolation?
Does it affect API contracts?
Does it affect backend service validation?
Does it affect audit or runtime events?
Does it affect AI memory or context assembly?
Does it require migration or backfill?
Does it require index changes?
Does it require retention policy update?
Does it need documentation update?
```

---

# 23. Evolution Anti-Patterns

Avoid:

```text
adding tables because they might be useful someday
using JSONB for stable core relationships
adding enums too early for unstable categories
renaming fields without compatibility period
removing audit evidence
breaking workspace isolation
creating search indexes without security scope
adding advanced infrastructure before MVP query patterns exist
changing database meaning without updating Domain Model and API contracts
```

---

# 24. Acceptance Criteria

Database Evolution Guide is ready when:

- evolution stages are defined;
- table and column evolution rules are documented;
- JSONB split rules are documented;
- constraint, index and status evolution are defined;
- search, memory, audit, access, integration and dashboard evolution paths are described;
- deprecation and ADR rules are included;
- evolution review checklist is provided.

Status:

```text
Accepted as Data Governance and Evolution Standard
```

---

# 25. Final Statement

```text
Bizzi Database Evolution Guide defines how the platform database should grow from MVP schema into governed, searchable, collaborative and enterprise-ready data architecture while preserving canonical meaning, workspace isolation, auditability and AI safety.
```

This guide completes the strengthening set for the `27_DATA_MODEL` layer before audit addendum or transition into `28_API_CONTRACTS`.