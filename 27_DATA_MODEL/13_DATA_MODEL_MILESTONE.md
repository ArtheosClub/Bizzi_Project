# 13_DATA_MODEL_MILESTONE.md

# Bizzi Platform

## Data Model Milestone

**Layer:** 27_DATA_MODEL  
**Component Type:** Layer Milestone  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Status:** Milestone Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the milestone for the `27_DATA_MODEL` layer of Bizzi Platform.

It confirms that the Data Model layer has reached a complete architectural checkpoint and can support transition from domain architecture into API contracts, backend services, migrations and implementation planning.

Core question:

```text
Has Bizzi Data Model been defined sufficiently to become the canonical database foundation for MVP implementation?
```

---

# 2. Milestone Scope

This milestone covers the following Data Model documents:

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
```

---

# 3. Layer Purpose

The purpose of `27_DATA_MODEL` is to translate the canonical Bizzi Domain Model into durable storage structures.

The layer defines:

- table families;
- table names;
- core columns;
- primary key strategy;
- workspace scoping;
- foreign key direction;
- polymorphic reference patterns;
- source traceability;
- audit and event persistence;
- enum and status catalog;
- indexing strategy;
- MVP simplifications;
- expansion paths.

---

# 4. Data Model Thesis

```text
Bizzi data must be structured, relational, workspace-scoped, traceable, auditable and implementation-ready.
```

The Data Model turns the Bizzi architecture from conceptual domain objects into a practical database foundation for software implementation.

---

# 5. Completed Data Areas

## 5.1 Data Model Vision

Defines the mission, target database assumption, principles and output structure of the Data Model layer.

Milestone status:

```text
Completed
```

## 5.2 Database Principles

Defines database rules for UUIDs, workspace scope, relational integrity, JSONB usage, audit/event persistence, source traceability and migration discipline.

Milestone status:

```text
Completed
```

## 5.3 Entity to Table Mapping

Maps Domain Model entities to database tables and assigns implementation priorities.

Milestone status:

```text
Completed
```

## 5.4 Core Tables

Defines the Priority 1 MVP table foundation.

Milestone status:

```text
Completed
```

## 5.5 Workspace Data Model

Defines users, sessions, company workspaces, workspace settings and workspace access expansion.

Milestone status:

```text
Completed
```

## 5.6 Operating Map Data Model

Defines operating maps, operating gaps, recommendations and operating map node expansion.

Milestone status:

```text
Completed
```

## 5.7 Function Responsibility Data Model

Defines functions, responsibilities, ownership gaps and responsibility assignment expansion.

Milestone status:

```text
Completed
```

## 5.8 Agent Process Task Decision Data Model

Defines agents, authority scopes, recommendations, action drafts, processes, process steps, tasks and decisions.

Milestone status:

```text
Completed
```

## 5.9 Memory Audit Event Data Model

Defines memory entries, audit events, runtime events and related expansion tables.

Milestone status:

```text
Completed
```

## 5.10 Integration Security Data Model

Defines integrations, integration sync jobs, security policies, workspace access and credential reference rules.

Milestone status:

```text
Completed
```

## 5.11 Dashboard Export Data Model

Defines dashboard metrics, export jobs and expansion tables for insights, alerts, snapshots, templates and files.

Milestone status:

```text
Completed
```

## 5.12 Enums and Statuses

Defines the controlled vocabulary for lifecycle states, categories, severity, priority and object types.

Milestone status:

```text
Completed
```

## 5.13 Indexing Strategy

Defines the MVP and expansion indexing approach for workspace queries, dashboards, traceability, audit and runtime events.

Milestone status:

```text
Completed
```

---

# 6. Canonical MVP Table Foundation

The Data Model establishes the following Priority 1 MVP table set:

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

This table foundation supports the first runnable Bizzi vertical slice.

---

# 7. Governed Runtime Table Foundation

The Data Model establishes the following Priority 2 table set:

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
ownership_gaps
operating_recommendations
```

This foundation supports governed AI assistance, process structure, integrations, security policies and controlled exports.

---

# 8. Expansion Table Foundation

Expansion tables are identified but intentionally deferred:

```text
roles
permissions
role_permissions
workspace_members
workspace_profiles
operating_map_nodes
responsibility_assignments
process_inputs
process_outputs
task_links
task_history
task_comments
decision_options
decision_outcomes
memory_sources
memory_usage
event_failures
security_events
dashboard_snapshots
dashboard_insights
dashboard_alerts
export_templates
export_files
```

Milestone rule:

```text
Expansion tables should be implemented only when product behavior requires them.
```

---

# 9. Workspace Scope Alignment

Workspace scoping is consistently defined for all operating tables.

Core rule:

```text
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
```

Applies to:

- operating maps;
- gaps;
- functions;
- responsibilities;
- agents;
- processes;
- tasks;
- decisions;
- memory;
- audit;
- events;
- integrations;
- security policies;
- dashboard metrics;
- export jobs.

Workspace scope status:

```text
Consistently Defined
```

---

# 10. Traceability Alignment

The Data Model defines traceability through:

```text
source_object_type
source_object_id
object_type
object_id
result_object_type
result_object_id
resolved_by_object_type
resolved_by_object_id
correlation_id
causation_id
source_event_id
```

Traceability chain:

```text
Source Object
↓
Domain Object
↓
Runtime Event
↓
Audit Event
↓
Memory Entry
↓
Dashboard Metric
↓
Export Job
```

Traceability status:

```text
Structurally Defined
```

---

# 11. Audit and Event Readiness

The layer defines `audit_events` and `runtime_events` as first-class tables.

They support:

- action evidence;
- object history;
- AI assistance evidence;
- human confirmation tracking;
- event-driven dashboard refresh;
- memory creation;
- runtime coordination;
- future observability.

Audit and event readiness:

```text
Ready
```

---

# 12. AI Governance Data Readiness

The Data Model supports governed AI through:

```text
agents
agent_authority_scopes
agent_recommendations
agent_action_drafts
memory_entries
audit_events
runtime_events
```

Preserved AI governance fields include:

```text
agent_id
ai_assisted
human_confirmed
confirmed_by
confirmed_at
confidence
source_object_type
source_object_id
result_object_type
result_object_id
```

AI governance status:

```text
Ready
```

---

# 13. Controlled Vocabulary Readiness

The layer defines controlled values for:

- workspace states;
- operating map states;
- function and responsibility states;
- agent states;
- process states;
- task states;
- decision states;
- memory states;
- audit severity;
- runtime event status;
- integration status;
- export status;
- object type references.

Enum readiness:

```text
Ready for API Validation and Backend Service Logic
```

---

# 14. Indexing Readiness

The Data Model defines indexes for:

- workspace-scoped queries;
- workspace + status filtering;
- dashboard loading;
- task boards;
- decision logs;
- memory retrieval;
- audit history;
- runtime event processing;
- integration health;
- export tracking;
- source traceability.

Indexing readiness:

```text
Ready for Migration Planning
```

---

# 15. Database Implementation Assumption

Recommended MVP database:

```text
PostgreSQL
```

Recommended initial implementation style:

```text
UUID primary keys
TEXT statuses with service validation
JSONB for metadata and payloads
BTREE indexes for MVP access patterns
Foreign keys for core relationships
Service-level validation for polymorphic references
```

---

# 16. Known MVP Simplifications

The layer intentionally allows MVP simplifications:

```text
Owner access may use company_workspaces.owner_user_id before full RBAC.
Operating map nodes may be postponed.
Operating recommendations may be represented through suggested functions or tasks.
Ownership gaps may initially be represented as operating gaps.
Task history may be represented through audit_events.
Memory sources may be represented through source fields on memory_entries.
Event failures may be represented through runtime_events fields.
Security events may initially use audit_events and runtime_events.
Dashboard insights may be generated dynamically.
Export files may be represented by file_reference on export_jobs.
```

These simplifications preserve MVP speed without breaking the architecture.

---

# 17. Data Model Risks

## Risk 1 — Over-Indexing

Too many indexes may slow writes.

Mitigation:

```text
Start with MVP minimum indexes and add advanced indexes after real query patterns emerge.
```

## Risk 2 — Polymorphic References Need Service Validation

Fields like `object_type + object_id` cannot always be enforced by foreign keys.

Mitigation:

```text
Backend services must validate object existence and workspace consistency.
```

## Risk 3 — Status Drift

TEXT statuses may become inconsistent without validation.

Mitigation:

```text
Centralize enum validation in backend code and add database constraints later.
```

## Risk 4 — JSONB Overuse

JSONB could hide core model meaning.

Mitigation:

```text
Use JSONB only for flexible metadata, payloads and configuration, not core relationships.
```

## Risk 5 — Weak Workspace Isolation

Implementation may accidentally omit workspace_id filtering.

Mitigation:

```text
Require workspace_id in API, service and repository query patterns.
```

---

# 18. Readiness for Next Layer

The Data Model is ready to support:

```text
28_API_CONTRACTS
29_BACKEND_SERVICE_DESIGN
Database migration planning
ORM model design
Repository layer design
Validation rules
Authorization rules
Dashboard query design
```

Next layer readiness:

```text
Ready
```

---

# 19. Remaining Work Outside This Layer

The Data Model does not yet define:

- actual SQL migration files;
- ORM class implementation;
- API request and response schemas;
- backend service methods;
- frontend screens;
- deployment configuration;
- production monitoring;
- billing tables;
- analytics warehouse.

These belong to later implementation layers.

---

# 20. Milestone Acceptance Criteria

The `27_DATA_MODEL` milestone is accepted when:

- table families are defined;
- core MVP tables are defined;
- governed runtime tables are defined;
- expansion tables are documented;
- workspace scope is consistent;
- traceability fields are defined;
- audit and runtime event tables are defined;
- enums and statuses are cataloged;
- indexes are identified;
- MVP simplifications are documented;
- layer can support API and backend design.

Acceptance result:

```text
Accepted
```

---

# 21. Milestone Result

```text
Layer: 27_DATA_MODEL
Status: Implemented as Data Architecture
Version: Draft v0.1
Milestone Status: Reached
Readiness: Ready for Data Model Audit
Next Document: 14_DATA_MODEL_AUDIT.md
```

---

# 22. Final Milestone Declaration

```text
BIZZI PLATFORM
27_DATA_MODEL
MILESTONE REACHED

The Data Model layer now defines the canonical database foundation for Bizzi as a PostgreSQL-ready, workspace-scoped, traceable, auditable, AI-governed and MVP-oriented platform data architecture.
```

This milestone prepares the layer for audit and controlled transition into API Contract design.