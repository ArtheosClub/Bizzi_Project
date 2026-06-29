# 15_DATA_DICTIONARY.md

# Bizzi Platform

## Data Dictionary

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Standard Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Previous Documents:** 00_DATA_MODEL_VISION.md through 14_DATA_MODEL_AUDIT.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the initial Data Dictionary for Bizzi Platform.

It standardizes the meaning, type, usage and governance expectations for recurring database fields across the `27_DATA_MODEL` layer.

Core question:

```text
What does each recurring Bizzi data field mean, how should it be typed, and how should it be used consistently across the platform?
```

---

# 2. Data Dictionary Role

The Data Dictionary provides a shared vocabulary for:

- database schema design;
- ORM model design;
- API contracts;
- backend validation;
- migrations;
- analytics;
- audit review;
- AI context assembly;
- documentation consistency.

It prevents different services from using the same column name with different meanings.

---

# 3. Dictionary Scope

This document covers common and recurring fields used across Bizzi tables.

It does not replace table-specific specifications in earlier files.

Instead, it defines standard field meanings for columns such as:

```text
id
workspace_id
status
created_at
updated_at
created_by
owner_user_id
source_object_type
source_object_id
metadata
confirmed_by
confirmed_at
archived_at
```

---

# 4. Field Definition Format

Each field is described by:

```text
Field Name
Recommended Type
Required Pattern
Meaning
Used By
Indexing Notes
Governance Notes
```

---

# 5. Identity Fields

## 5.1 id

Recommended type:

```text
UUID PRIMARY KEY
```

Meaning:

```text
Unique identifier of a record within its table.
```

Used by:

```text
All primary domain tables
```

Indexing notes:

```text
Primary key index is created automatically.
```

Governance notes:

```text
IDs should be stable, non-sequential and safe for API references.
```

---

## 5.2 user_id

Recommended type:

```text
UUID REFERENCES users(id)
```

Meaning:

```text
Reference to a human user identity.
```

Used by:

```text
sessions
workspace_access
security_events
```

Governance notes:

```text
Use user_id when the column represents the user being referenced, not necessarily the actor who created or changed the record.
```

---

## 5.3 owner_user_id

Recommended type:

```text
UUID REFERENCES users(id)
```

Meaning:

```text
Human user accountable for a workspace, process, task, decision or other operating object.
```

Used by:

```text
company_workspaces
tasks
decisions
processes
responsibilities
```

Governance notes:

```text
owner_user_id indicates accountability. It should not be used merely as a creator field.
```

---

## 5.4 created_by

Recommended type:

```text
UUID REFERENCES users(id) NULL
```

Meaning:

```text
User who created the record, where known.
```

Used by:

```text
Most operating tables
```

Governance notes:

```text
created_by may be NULL for system-created or imported records. Use actor_type in audit_events for richer origin tracking.
```

---

## 5.5 assigned_by

Recommended type:

```text
UUID REFERENCES users(id) NULL
```

Meaning:

```text
User who assigned ownership or responsibility.
```

Used by:

```text
responsibilities
responsibility_assignments
```

---

# 6. Workspace Fields

## 6.1 workspace_id

Recommended type:

```text
UUID NOT NULL REFERENCES company_workspaces(id)
```

Meaning:

```text
Root workspace boundary for an operating record.
```

Used by:

```text
All workspace-scoped operating tables
```

Indexing notes:

```text
Most workspace-scoped tables should include INDEX(workspace_id).
```

Governance notes:

```text
No workspace_id, no operating record. All API and service queries for operating data should include workspace_id.
```

---

## 6.2 workspace_access.role

Recommended type:

```text
TEXT
```

Meaning:

```text
User role inside a workspace.
```

Allowed values:

```text
owner
admin
manager
member
viewer
consultant
auditor
```

Governance notes:

```text
MVP may only use owner. Full RBAC may later move role definitions into roles and permissions tables.
```

---

# 7. Lifecycle Fields

## 7.1 status

Recommended type:

```text
TEXT NOT NULL
```

Meaning:

```text
Lifecycle state of a record.
```

Used by:

```text
Most primary domain tables
```

Governance notes:

```text
Status values must come from 11_ENUMS_AND_STATUSES.md. Service layer must validate allowed transitions.
```

---

## 7.2 archived_at

Recommended type:

```text
TIMESTAMPTZ NULL
```

Meaning:

```text
Timestamp when a record was archived and removed from normal active workflows.
```

Used by:

```text
company_workspaces
operating_maps
functions
tasks
decisions
memory_entries
agents
processes
```

Governance notes:

```text
Important operating records should be archived rather than hard deleted.
```

---

## 7.3 revoked_at

Recommended type:

```text
TIMESTAMPTZ NULL
```

Meaning:

```text
Timestamp when access, integration or credential reference was revoked.
```

Used by:

```text
integrations
workspace_access
integration_credential_references
```

---

## 7.4 completed_at

Recommended type:

```text
TIMESTAMPTZ NULL
```

Meaning:

```text
Timestamp when a task, sync job or export completed.
```

Used by:

```text
tasks
integration_sync_jobs
export_jobs
```

Governance notes:

```text
Completed records should preserve completion timestamp for audit and dashboard metrics.
```

---

## 7.5 resolved_at

Recommended type:

```text
TIMESTAMPTZ NULL
```

Meaning:

```text
Timestamp when a gap, alert or issue was resolved.
```

Used by:

```text
operating_gaps
ownership_gaps
dashboard_alerts
event_failures
```

---

# 8. Timestamp Fields

## 8.1 created_at

Recommended type:

```text
TIMESTAMPTZ NOT NULL DEFAULT now()
```

Meaning:

```text
Timestamp when the record was created.
```

Used by:

```text
All primary tables
```

Governance notes:

```text
Store timestamps in UTC. Display localization belongs to frontend or API formatting.
```

---

## 8.2 updated_at

Recommended type:

```text
TIMESTAMPTZ NOT NULL DEFAULT now()
```

Meaning:

```text
Timestamp when the record was last updated.
```

Used by:

```text
Mutable operating tables
```

Governance notes:

```text
updated_at should change on meaningful record update. It may support optimistic concurrency later.
```

---

## 8.3 timestamp

Recommended type:

```text
TIMESTAMPTZ NOT NULL DEFAULT now()
```

Meaning:

```text
Event occurrence time.
```

Used by:

```text
audit_events
runtime_events
```

Governance notes:

```text
Use timestamp for event time, not created_at, when recording an action or runtime event.
```

---

# 9. Confirmation Fields

## 9.1 confirmed_by

Recommended type:

```text
UUID REFERENCES users(id) NULL
```

Meaning:

```text
User who confirmed a draft, AI-generated output, recommendation, map, task, decision or memory.
```

Used by:

```text
operating_maps
functions
tasks
decisions
memory_entries
agent_recommendations
agent_action_drafts
dashboard_insights
```

Governance notes:

```text
AI-generated outputs that become official should preserve confirmation actor.
```

---

## 9.2 confirmed_at

Recommended type:

```text
TIMESTAMPTZ NULL
```

Meaning:

```text
Timestamp when a record was confirmed.
```

Used by:

```text
Operating map, function, task, decision, memory and AI output tables
```

---

## 9.3 reviewed_by

Recommended type:

```text
UUID REFERENCES users(id) NULL
```

Meaning:

```text
User who reviewed a recommendation, draft or insight.
```

Used by:

```text
agent_recommendations
agent_action_drafts
operating_recommendations
```

---

## 9.4 reviewed_at

Recommended type:

```text
TIMESTAMPTZ NULL
```

Meaning:

```text
Timestamp when review occurred.
```

---

## 9.5 rejected_at

Recommended type:

```text
TIMESTAMPTZ NULL
```

Meaning:

```text
Timestamp when a recommendation, draft or candidate was rejected.
```

Used by:

```text
agent_recommendations
agent_action_drafts
operating_recommendations
```

---

# 10. Source and Traceability Fields

## 10.1 source_object_type

Recommended type:

```text
TEXT NULL
```

Meaning:

```text
Type of object from which the current record originated.
```

Used by:

```text
operating_gaps
functions
agent_recommendations
agent_action_drafts
processes
tasks
decisions
memory_entries
runtime_events
dashboard_metrics
export_jobs
```

Governance notes:

```text
Values should come from object type catalog in 11_ENUMS_AND_STATUSES.md.
```

---

## 10.2 source_object_id

Recommended type:

```text
UUID NULL
```

Meaning:

```text
Identifier of the object from which the current record originated.
```

Indexing notes:

```text
Use with source_object_type in composite index where traceability queries are needed.
```

---

## 10.3 object_type

Recommended type:

```text
TEXT NOT NULL or NULL depending on table
```

Meaning:

```text
Target object type for responsibility, audit or security event.
```

Used by:

```text
responsibilities
audit_events
security_events
```

---

## 10.4 object_id

Recommended type:

```text
UUID NULL or NOT NULL depending on table
```

Meaning:

```text
Target object identifier for responsibility, audit or security event.
```

Governance notes:

```text
Polymorphic object references require backend validation for existence and workspace consistency.
```

---

## 10.5 result_object_type

Recommended type:

```text
TEXT NULL
```

Meaning:

```text
Type of object created or affected after recommendation or draft application.
```

Used by:

```text
agent_recommendations
agent_action_drafts
operating_recommendations
```

---

## 10.6 result_object_id

Recommended type:

```text
UUID NULL
```

Meaning:

```text
Identifier of object created or affected after recommendation or draft application.
```

---

## 10.7 resolved_by_object_type

Recommended type:

```text
TEXT NULL
```

Meaning:

```text
Type of object that resolved a gap or alert.
```

Used by:

```text
operating_gaps
```

---

## 10.8 resolved_by_object_id

Recommended type:

```text
UUID NULL
```

Meaning:

```text
Identifier of object that resolved a gap or alert.
```

---

# 11. Audit and Event Fields

## 11.1 actor_id

Recommended type:

```text
UUID REFERENCES users(id) NULL
```

Meaning:

```text
Human user who performed or triggered an auditable action or runtime event.
```

Used by:

```text
audit_events
runtime_events
```

---

## 11.2 actor_type

Recommended type:

```text
TEXT NOT NULL
```

Meaning:

```text
Category of actor that performed an action.
```

Allowed values:

```text
user
agent
system
integration
```

---

## 11.3 action

Recommended type:

```text
TEXT NOT NULL
```

Meaning:

```text
Audited action name.
```

Used by:

```text
audit_events.action
```

Governance notes:

```text
Use stable dot notation such as task.created, decision.confirmed or export.completed.
```

---

## 11.4 event_type

Recommended type:

```text
TEXT NOT NULL
```

Meaning:

```text
Runtime event name.
```

Used by:

```text
runtime_events.event_type
```

Governance notes:

```text
Use stable dot notation and align event names with Runtime Platform documents.
```

---

## 11.5 correlation_id

Recommended type:

```text
UUID NULL
```

Meaning:

```text
Identifier linking related operations, events and audit records across a workflow.
```

Used by:

```text
audit_events
runtime_events
```

---

## 11.6 causation_id

Recommended type:

```text
UUID NULL
```

Meaning:

```text
Identifier of prior event that caused the current runtime event.
```

Used by:

```text
runtime_events
```

---

## 11.7 source_event_id

Recommended type:

```text
UUID REFERENCES runtime_events(id) NULL
```

Meaning:

```text
Runtime event that caused or is associated with an audit event.
```

Used by:

```text
audit_events
```

---

## 11.8 before_state

Recommended type:

```text
JSONB NULL
```

Meaning:

```text
Selected state of an object before an auditable change.
```

Used by:

```text
audit_events
```

Governance notes:

```text
Do not store raw secrets or excessive sensitive payloads.
```

---

## 11.9 after_state

Recommended type:

```text
JSONB NULL
```

Meaning:

```text
Selected state of an object after an auditable change.
```

---

# 12. AI Governance Fields

## 12.1 agent_id

Recommended type:

```text
UUID REFERENCES agents(id) NULL
```

Meaning:

```text
AI agent associated with a recommendation, draft, task, decision, memory, audit event or runtime event.
```

Used by:

```text
agent outputs
tasks
decisions
memory_entries
audit_events
runtime_events
```

---

## 12.2 ai_assisted

Recommended type:

```text
BOOLEAN NOT NULL DEFAULT false
```

Meaning:

```text
Indicates that AI assisted the action or record creation.
```

Used by:

```text
audit_events
```

---

## 12.3 human_confirmed

Recommended type:

```text
BOOLEAN NULL
```

Meaning:

```text
Indicates whether a human confirmed an AI-assisted sensitive action.
```

Used by:

```text
audit_events
```

---

## 12.4 confidence

Recommended type:

```text
TEXT NULL
```

Meaning:

```text
Confidence classification for AI-generated memory, recommendation or output.
```

Used by:

```text
memory_entries
agent_recommendations
operating_recommendations
```

Governance notes:

```text
Confidence is not a substitute for human confirmation.
```

---

# 13. Metadata and Payload Fields

## 13.1 metadata

Recommended type:

```text
JSONB NULL
```

Meaning:

```text
Flexible non-core metadata for the record.
```

Used by:

```text
Most domain tables
```

Governance notes:

```text
Do not use metadata to hide core relational fields. Do not store raw secrets.
```

---

## 13.2 payload

Recommended type:

```text
JSONB NULL or JSONB NOT NULL depending on table
```

Meaning:

```text
Structured event or draft payload.
```

Used by:

```text
runtime_events
agent_action_drafts
```

---

## 13.3 configuration

Recommended type:

```text
JSONB NULL or JSONB NOT NULL depending on table
```

Meaning:

```text
Structured configuration for integrations, templates or policies.
```

Used by:

```text
integrations
export_templates
```

---

## 13.4 rules

Recommended type:

```text
JSONB NOT NULL
```

Meaning:

```text
Structured security or policy rules.
```

Used by:

```text
security_policies
```

---

# 14. Classification Fields

## 14.1 type fields

Common examples:

```text
gap_type
recommendation_type
memory_type
export_type
policy_type
sync_type
metric_type
alert_type
insight_type
```

Recommended type:

```text
TEXT NOT NULL
```

Meaning:

```text
Stable internal classification of a record.
```

Governance notes:

```text
Type fields should use controlled values from 11_ENUMS_AND_STATUSES.md or later reference tables.
```

---

## 14.2 category

Recommended type:

```text
TEXT NULL
```

Meaning:

```text
Higher-level grouping used for dashboard, filtering or classification.
```

Used by:

```text
functions
dashboard_metrics
permissions
```

---

## 14.3 severity

Recommended type:

```text
TEXT NULL
```

Meaning:

```text
Importance, risk or urgency classification.
```

Common values:

```text
info
warning
critical
low
medium
high
critical
```

Governance notes:

```text
Use display severity for dashboard and audit visibility; use risk severity for gaps and risks.
```

---

## 14.4 priority

Recommended type:

```text
TEXT NOT NULL DEFAULT 'normal'
```

Meaning:

```text
Task or work priority.
```

Allowed values:

```text
low
normal
high
urgent
```

Used by:

```text
tasks
```

---

# 15. Export and Integration Fields

## 15.1 provider

Recommended type:

```text
TEXT NOT NULL
```

Meaning:

```text
External provider name for an integration.
```

Used by:

```text
integrations
```

---

## 15.2 credential_ref

Recommended type:

```text
TEXT NULL
```

Meaning:

```text
Reference to a secret stored outside normal runtime tables.
```

Used by:

```text
integrations
integration_credential_references
```

Governance notes:

```text
credential_ref must never contain the actual secret value.
```

---

## 15.3 file_reference

Recommended type:

```text
TEXT NULL
```

Meaning:

```text
Reference to generated or stored export file artifact.
```

Used by:

```text
export_jobs
export_files
```

---

## 15.4 export_scope

Recommended type:

```text
JSONB NULL
```

Meaning:

```text
Structured definition of what data is included in an export.
```

Used by:

```text
export_jobs
```

Governance notes:

```text
Export scope must be workspace-scoped and auditable.
```

---

# 16. Content Fields

## 16.1 title

Recommended type:

```text
TEXT NOT NULL
```

Meaning:

```text
Human-readable title of a record.
```

Used by:

```text
operating_gaps
tasks
decisions
memory_entries
agent_recommendations
agent_action_drafts
dashboard_insights
dashboard_alerts
```

---

## 16.2 description

Recommended type:

```text
TEXT NULL
```

Meaning:

```text
Human-readable description or explanation.
```

---

## 16.3 summary

Recommended type:

```text
TEXT NULL
```

Meaning:

```text
Short summarized version of longer content.
```

Used by:

```text
operating_maps
memory_entries
dashboard_snapshots
```

---

## 16.4 content

Recommended type:

```text
TEXT NOT NULL or NULL depending on table
```

Meaning:

```text
Main body content of a memory entry or document-like object.
```

Used by:

```text
memory_entries
```

---

# 17. Date Fields

## 17.1 due_date

Recommended type:

```text
DATE NULL
```

Meaning:

```text
Date by which a task should be completed.
```

Used by:

```text
tasks
```

---

## 17.2 decision_date

Recommended type:

```text
DATE NULL
```

Meaning:

```text
Date on which a decision was made or became effective.
```

Used by:

```text
decisions
```

---

## 17.3 review_date

Recommended type:

```text
DATE NULL
```

Meaning:

```text
Date on which a record should be reviewed.
```

Used by:

```text
decisions
memory_entries
responsibilities
```

---

## 17.4 valid_from / valid_until

Recommended type:

```text
DATE NULL
```

Meaning:

```text
Date range during which a memory entry or rule is valid.
```

Used by:

```text
memory_entries
```

---

# 18. Field Usage Rules

## Rule 1 — Same Name, Same Meaning

A column name should mean the same thing across all tables.

## Rule 2 — Do Not Use Metadata for Core Fields

Core relationships, statuses and ownership must be explicit columns.

## Rule 3 — All Operating Records Need Workspace Scope

Any business operating object should include `workspace_id` unless explicitly global.

## Rule 4 — AI Output Must Preserve Confirmation Fields

AI-generated official records should preserve `confirmed_by` and `confirmed_at` where required.

## Rule 5 — Traceability Fields Must Use Controlled Object Types

`source_object_type`, `object_type`, `result_object_type` and related fields must use stable internal object type strings.

---

# 19. MVP Minimum Dictionary Fields

The minimum field set that engineering should standardize first:

```text
id
workspace_id
status
created_at
updated_at
created_by
owner_user_id
source_object_type
source_object_id
metadata
confirmed_by
confirmed_at
archived_at
actor_id
actor_type
action
event_type
object_type
object_id
correlation_id
```

---

# 20. Future Data Dictionary Expansion

Future versions may add:

- full table-by-table column catalog;
- nullability matrix;
- default value catalog;
- validation rule catalog;
- API field mapping;
- ORM field mapping;
- analytics field mapping;
- privacy classification;
- retention classification;
- encryption classification.

---

# 21. Acceptance Criteria

Data Dictionary is ready when:

- recurring fields are defined;
- field meanings are standardized;
- field types are recommended;
- governance usage is documented;
- AI, audit and traceability fields are included;
- workspace scoping field is defined as canonical;
- metadata and JSONB usage boundaries are documented.

Status:

```text
Accepted as Data Model Standard
```

---

# 22. Final Statement

```text
Bizzi Data Dictionary defines the canonical meaning and usage of recurring database fields, ensuring that the Data Model, API Contracts, Backend Services and future migrations speak the same data language.
```

This dictionary strengthens the `27_DATA_MODEL` layer as a practical implementation standard.