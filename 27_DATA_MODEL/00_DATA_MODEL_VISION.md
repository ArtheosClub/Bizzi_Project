# 00_DATA_MODEL_VISION.md

# Bizzi Platform

## Data Model Vision

**Layer:** 27_DATA_MODEL  
**Component Type:** Product Engineering Data Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document opens the `27_DATA_MODEL` layer for Bizzi Platform.

The Data Model layer translates the canonical Domain Model into durable storage structures that can support MVP implementation, API contracts, backend services, auditability, memory, workspace isolation and future scale.

Core question:

```text
How does Bizzi store its domain objects so that the platform remains workspace-scoped, traceable, secure, queryable and implementation-ready?
```

---

# 2. Layer Mission

The mission of `27_DATA_MODEL` is to define the canonical persistence model for Bizzi Platform.

This layer must translate:

```text
Domain Entities → Tables
Aggregate Roots → Primary Tables
Relationships → Foreign Keys
Statuses → ENUMs
Traceability → Source Links and Indexes
Auditability → Audit Tables and References
Runtime Events → Event Tables
Workspace Scope → workspace_id Constraints
```

The result should be sufficiently clear for database schema creation, ORM modeling and API implementation.

---

# 3. Position in Architecture

```text
Art of Business v1.0
↓
24_PRODUCTIZATION_AND_IMPLEMENTATION
↓
25_RUNTIME_PLATFORM
↓
26_DOMAIN_MODEL
↓
27_DATA_MODEL
↓
28_API_CONTRACTS
↓
29_BACKEND_SERVICE_DESIGN
↓
30_FRONTEND_EXPERIENCE
```

Layer 26 defines what exists in the product domain.

Layer 27 defines how those objects are stored.

---

# 4. Data Model Thesis

```text
Bizzi data must not be a collection of disconnected chat outputs.
Bizzi data must be structured, relational, workspace-scoped, auditable and ready for AI-assisted execution.
```

The data model is the durable backbone of the platform.

It must preserve the meaning and governance defined by the Domain Model.

---

# 5. Target Database Assumption

Recommended MVP database:

```text
PostgreSQL
```

Reasoning:

- strong relational integrity;
- mature indexing;
- JSONB support for flexible metadata;
- transaction safety;
- good ORM support;
- suitable for SaaS multi-tenant workspace scoping;
- compatible with future analytics and audit queries.

---

# 6. Data Modeling Principles

## 6.1 Workspace-Scoped by Default

Most business tables must include:

```text
workspace_id
```

Rule:

```text
No workspace_id, no operating record.
```

Exceptions may include global platform metadata such as enum reference tables or public templates.

---

## 6.2 UUID Primary Keys

Primary keys should use UUID values.

Recommended pattern:

```text
id UUID PRIMARY KEY
```

This supports distributed-safe creation, clean API references and future scaling.

---

## 6.3 Explicit Foreign Keys

Relationships should be represented through explicit foreign keys where practical.

Examples:

```text
workspace_id → company_workspaces.id
owner_user_id → users.id
function_id → functions.id
process_id → processes.id
decision_id → decisions.id
```

---

## 6.4 ENUM Discipline

Statuses and stable categories should be modeled as controlled enum values.

Examples:

```text
task_status
decision_status
memory_status
agent_status
integration_status
export_status
```

---

## 6.5 JSONB for Flexible Metadata

Use JSONB for flexible non-critical metadata.

Examples:

```text
metadata
configuration
payload
before_state
after_state
mapping_rules
```

JSONB should not replace core relational fields.

---

## 6.6 Audit and Event First

Important changes should be represented in audit and event tables.

Core tables:

```text
audit_events
runtime_events
```

---

## 6.7 Source Traceability

Objects derived from other objects should support:

```text
source_object_type
source_object_id
```

This is essential for memory, AI output, task suggestions and operating recommendations.

---

## 6.8 MVP Simplicity Before Full Normalization

The first schema should be normalized enough for correctness, but not over-fragmented.

Supporting entities may initially be represented as columns or JSONB where documented by the Domain Model.

---

# 7. Core Table Families

The Data Model layer should define these table families:

```text
Identity Tables
Workspace Tables
Operating Map Tables
Function and Responsibility Tables
Agent Tables
Process Tables
Task Tables
Decision Tables
Memory Tables
Audit and Event Tables
Integration and Security Tables
Dashboard and Export Tables
```

---

# 8. Canonical Table Foundation

Initial canonical table set:

```text
users
sessions
company_workspaces
workspace_settings
workspace_access
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
tasks
decisions
memory_entries
audit_events
runtime_events
integrations
integration_sync_jobs
security_policies
dashboard_metrics
export_jobs
```

Supporting tables may be added later when needed.

---

# 9. MVP Table Priority

Priority 1 — Required for first runnable slice:

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

Priority 2 — Needed for governed AI and structured runtime:

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
export_jobs
```

Priority 3 — Expansion:

```text
workspace_access
ownership_gaps
operating_recommendations
dashboard_alerts
dashboard_snapshots
export_files
roles
permissions
```

---

# 10. Common Column Pattern

Most domain tables should include:

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

Not every table requires every field, but consistency improves implementation quality.

---

# 11. Workspace Isolation Pattern

Every query for operating data should be scoped by:

```text
workspace_id
```

This affects:

- API authorization;
- dashboard queries;
- memory retrieval;
- audit filtering;
- export generation;
- integration sync;
- AI context assembly.

The database should support this with indexes on `workspace_id` across major tables.

---

# 12. Traceability Pattern

Traceability fields:

```text
source_object_type TEXT
source_object_id UUID
```

Used by:

- operating gaps;
- operating recommendations;
- agent recommendations;
- agent action drafts;
- tasks;
- decisions;
- memory entries;
- audit events;
- dashboard metrics;
- export jobs where useful.

This preserves the chain from source to action.

---

# 13. Audit Data Pattern

Audit events should capture:

```text
id
workspace_id
actor_id
actor_type
action
object_type
object_id
timestamp
metadata
```

Optional:

```text
source_event_id
agent_id
ai_assisted
human_confirmed
before_state
after_state
severity
correlation_id
```

Audit must support object-level history and workspace-level review.

---

# 14. Runtime Event Data Pattern

Runtime events should capture:

```text
id
workspace_id
event_type
source_component
source_object_type
source_object_id
actor_id
timestamp
payload
status
```

Optional:

```text
correlation_id
causation_id
severity
processed_at
error_message
retry_count
```

Events support internal coordination and dashboard refresh.

---

# 15. Memory Data Pattern

Memory entries should capture:

```text
id
workspace_id
memory_type
title
content
status
source_object_type
source_object_id
created_at
updated_at
created_by
```

Optional:

```text
summary
confidence
function_id
process_id
task_id
decision_id
agent_id
tags
review_required
review_date
archived_at
```

Memory must remain source-linked and workspace-scoped.

---

# 16. AI Output Data Pattern

AI-generated outputs should be stored as draft, candidate or recommendation objects before becoming official.

Examples:

```text
agent_recommendations
agent_action_drafts
operating_recommendations
memory_entries with status = candidate
```

Core fields:

```text
workspace_id
agent_id
source_object_type
source_object_id
suggested_object_type
suggested_object_payload
status
confidence
reviewed_by
confirmed_by
confirmed_at
rejected_at
```

---

# 17. Security Data Pattern

Security-related data should support:

```text
users
sessions
workspace_access
security_policies
```

MVP simplification:

```text
Owner access may be represented through company_workspaces.owner_user_id before full RBAC tables are implemented.
```

Security-sensitive operations must still be auditable.

---

# 18. Indexing Vision

Indexes should support:

- workspace-scoped queries;
- dashboard loading;
- task lists;
- memory retrieval;
- audit history;
- event processing;
- integration status;
- export status;
- owner-based filtering.

Common indexes:

```text
(workspace_id)
(workspace_id, status)
(workspace_id, created_at)
(workspace_id, updated_at)
(workspace_id, owner_user_id)
(source_object_type, source_object_id)
```

---

# 19. Data Model Outputs

The `27_DATA_MODEL` layer should produce:

```text
00_DATA_MODEL_VISION.md
01_DATABASE_PRINCIPLES.md
02_ENTITY_TO_TABLE_MAPPING.md
03_CORE_TABLES.md
04_WORKSPACE_DATA_MODEL.md
05_OPERATING_MAP_DATA_MODEL.md
06_FUNCTION_RESPONSIBILITY_DATA_MODEL.md
07_AGENT_PROCESS_TASK_DECISION_DATA_MODEL.md
08_MEMORY_AUDIT_EVENT_DATA_MODEL.md
09_INTEGRATION_SECURITY_DATA_MODEL.md
10_DASHBOARD_EXPORT_DATA_MODEL.md
11_ENUMS_AND_STATUSES.md
12_INDEXING_STRATEGY.md
13_DATA_MODEL_MILESTONE.md
14_DATA_MODEL_AUDIT.md
15_IMPLEMENTATION_READY.md
```

---

# 20. Relationship to API Contracts

The Data Model is not the API contract, but it informs API design.

API contracts will later define:

- request schemas;
- response schemas;
- validation rules;
- error structures;
- authorization behavior;
- endpoint naming;
- pagination and filtering.

The data model provides the persistence foundation for those contracts.

---

# 21. Relationship to Backend Services

Backend services should enforce domain rules before writing data.

The database should preserve structural integrity, but business logic belongs in services.

Example:

```text
TaskService validates ownership and status transition.
Database stores task and audit records.
```

---

# 22. Relationship to Frontend

Frontend screens should not drive the schema directly.

The schema should reflect domain objects and runtime rules.

Frontend will consume the model through APIs, especially for:

- dashboard;
- workspace setup;
- operating map;
- task board;
- decision log;
- memory view;
- audit view;
- exports.

---

# 23. Data Model Success Criteria

The Data Model layer is successful when:

- all Priority 1 domain entities map to tables;
- key relationships are represented;
- workspace scoping is enforced structurally;
- statuses and enums are defined;
- audit and event storage is defined;
- memory source traceability is defined;
- indexing strategy supports MVP queries;
- schema can support API contract and backend implementation.

---

# 24. Out of Scope

This layer does not define:

- complete ORM classes;
- production migrations;
- physical infrastructure;
- database hosting provider;
- API request and response schemas;
- frontend screens;
- backend service methods;
- analytics warehouse;
- billing data model unless added later.

---

# 25. Final Data Model Vision Statement

```text
Bizzi Data Model defines the durable relational storage foundation that transforms the Domain Model into workspace-scoped, traceable, auditable and implementation-ready database structures.
```

This layer begins the transition from product domain architecture to executable software engineering.