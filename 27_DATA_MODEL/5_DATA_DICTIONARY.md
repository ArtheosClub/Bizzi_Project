# 5_DATA_DICTIONARY.md

# Bizzi Platform

## Data Dictionary

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Model Reference Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Data Dictionary for Bizzi Platform.

It establishes the common meaning, data type, usage rules and governance expectations for recurring fields used across the `27_DATA_MODEL` layer.

Core question:

```text
What does each recurring Bizzi database field mean, where is it used, and how should engineering teams interpret it consistently?
```

---

# 2. Data Dictionary Role

The Data Dictionary provides a shared language for:

- database design;
- API contracts;
- backend services;
- ORM models;
- validation logic;
- dashboard queries;
- audit interpretation;
- AI context assembly;
- implementation onboarding.

It prevents different parts of the system from using the same field name with different meanings.

---

# 3. Dictionary Scope

This dictionary covers common and cross-cutting fields used across Bizzi tables.

It does not replace table-specific data model documents.

Instead, it standardizes recurring fields such as:

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

# 4. General Data Type Assumptions

Recommended MVP database:

```text
PostgreSQL
```

Common data types:

```text
UUID
TEXT
BOOLEAN
INTEGER
DATE
TIMESTAMPTZ
JSONB
TEXT[]
```

Timestamp convention:

```text
TIMESTAMPTZ using UTC storage semantics
```

---

# 5. Identity Fields

## id

| Property | Definition |
|---|---|
| Type | UUID |
| Required | Yes |
| Indexed | Primary Key |
| Used By | All primary tables |
| Meaning | Unique identifier of the record |

Rule:

```text
Every primary table should use id UUID PRIMARY KEY.
```

---

## user_id

| Property | Definition |
|---|---|
| Type | UUID |
| Required | Context-dependent |
| Indexed | Usually yes |
| References | users.id |
| Meaning | Human user associated with the record |

Used by:

```text
sessions
workspace_access
security_events
```

---

## owner_user_id

| Property | Definition |
|---|---|
| Type | UUID |
| Required | Depends on entity lifecycle |
| Indexed | Yes where ownership queries are common |
| References | users.id |
| Meaning | User accountable for an object |

Used by:

```text
company_workspaces
responsibilities
tasks
decisions
processes
```

Service rule:

```text
Official active operating objects should have an owner or an explicit ownership gap.
```

---

# 6. Workspace Fields

## workspace_id

| Property | Definition |
|---|---|
| Type | UUID |
| Required | Yes for operating tables |
| Indexed | Yes |
| References | company_workspaces.id |
| Meaning | Workspace boundary for the record |

Core rule:

```text
All operating data must be scoped to one workspace unless explicitly global.
```

Used by:

```text
operating_maps
operating_gaps
functions
responsibilities
agents
processes
tasks
decisions
memory_entries
audit_events
runtime_events
integrations
security_policies
dashboard_metrics
export_jobs
```

---

# 7. Lifecycle Fields

## status

| Property | Definition |
|---|---|
| Type | TEXT initially; enum/check later |
| Required | Usually yes |
| Indexed | Usually with workspace_id |
| Meaning | Lifecycle state of the record |

Rule:

```text
Statuses must use controlled values from 11_ENUMS_AND_STATUSES.md.
```

Common patterns:

```text
suggested
draft
active
paused
archived
```

---

## archived_at

| Property | Definition |
|---|---|
| Type | TIMESTAMPTZ |
| Required | No |
| Indexed | Optional |
| Meaning | Timestamp when the object was archived |

Rule:

```text
Important business objects should be archived, not silently deleted.
```

---

## revoked_at

| Property | Definition |
|---|---|
| Type | TIMESTAMPTZ |
| Required | No |
| Indexed | Optional |
| Meaning | Timestamp when access, session, integration or credential reference was revoked |

Used by:

```text
integrations
workspace_access
integration_credential_references
```

---

# 8. Timestamp Fields

## created_at

| Property | Definition |
|---|---|
| Type | TIMESTAMPTZ |
| Required | Yes |
| Default | now() |
| Indexed | Sometimes |
| Meaning | Time when record was created |

Rule:

```text
created_at should not be manually changed after creation.
```

---

## updated_at

| Property | Definition |
|---|---|
| Type | TIMESTAMPTZ |
| Required | Yes for mutable tables |
| Default | now() |
| Indexed | Sometimes |
| Meaning | Time when record was last updated |

Rule:

```text
updated_at should change whenever mutable business fields change.
```

---

## confirmed_at

| Property | Definition |
|---|---|
| Type | TIMESTAMPTZ |
| Required | When object is confirmed |
| Indexed | Optional |
| Meaning | Time when a user confirmed a suggested, draft or AI-assisted object |

Used by:

```text
operating_maps
functions
tasks
decisions
agent_recommendations
agent_action_drafts
memory_entries
```

---

## completed_at

| Property | Definition |
|---|---|
| Type | TIMESTAMPTZ |
| Required | When completion occurs |
| Indexed | Sometimes |
| Meaning | Time when a task, export, sync job or process execution completed |

Used by:

```text
tasks
integration_sync_jobs
export_jobs
```

---

# 9. Actor and Ownership Fields

## created_by

| Property | Definition |
|---|---|
| Type | UUID |
| Required | No, but recommended |
| References | users.id |
| Meaning | User who created the record |

Rule:

```text
created_by may be null for system-created records, but actor should be preserved in audit_events where possible.
```

---

## confirmed_by

| Property | Definition |
|---|---|
| Type | UUID |
| Required | When confirmation is required |
| References | users.id |
| Meaning | User who confirmed the object as official |

Rule:

```text
AI-generated sensitive outputs must not become official without confirmation metadata.
```

---

## assigned_by

| Property | Definition |
|---|---|
| Type | UUID |
| Required | No |
| References | users.id |
| Meaning | User who assigned a responsibility or task owner |

Used by:

```text
responsibilities
workspace_access
```

---

## actor_id

| Property | Definition |
|---|---|
| Type | UUID |
| Required | No |
| References | users.id where actor is human |
| Meaning | Actor that initiated an audit or runtime event |

Used by:

```text
audit_events
runtime_events
```

---

## actor_type

| Property | Definition |
|---|---|
| Type | TEXT |
| Required | Yes in audit events |
| Values | user, agent, system, integration |
| Meaning | Type of actor that performed an action |

Reference:

```text
11_ENUMS_AND_STATUSES.md
```

---

# 10. Source Traceability Fields

## source_object_type

| Property | Definition |
|---|---|
| Type | TEXT |
| Required | Context-dependent |
| Indexed | Yes with source_object_id |
| Meaning | Type of object from which the current record originated |

Examples:

```text
operating_map
operating_gap
agent_recommendation
user_input
decision
task
```

---

## source_object_id

| Property | Definition |
|---|---|
| Type | UUID |
| Required | Context-dependent |
| Indexed | Yes with source_object_type |
| Meaning | Identifier of source object |

Rule:

```text
source_object_type and source_object_id should be used together when source traceability is available.
```

---

## object_type

| Property | Definition |
|---|---|
| Type | TEXT |
| Required | Yes in audit_events and responsibilities |
| Indexed | Yes with object_id |
| Meaning | Type of target object affected or owned |

Used by:

```text
audit_events
responsibilities
ownership_gaps
```

---

## object_id

| Property | Definition |
|---|---|
| Type | UUID |
| Required | Context-dependent |
| Indexed | Yes with object_type |
| Meaning | Identifier of target object affected or owned |

Service rule:

```text
Polymorphic references must be validated by backend services for object existence and workspace consistency.
```

---

## result_object_type

| Property | Definition |
|---|---|
| Type | TEXT |
| Required | No |
| Indexed | With result_object_id where used |
| Meaning | Type of object created as a result of a recommendation or draft |

Used by:

```text
agent_recommendations
agent_action_drafts
operating_recommendations
```

---

## result_object_id

| Property | Definition |
|---|---|
| Type | UUID |
| Required | No |
| Indexed | With result_object_type where used |
| Meaning | Identifier of object created as a result |

---

# 11. AI Governance Fields

## agent_id

| Property | Definition |
|---|---|
| Type | UUID |
| Required | Context-dependent |
| Indexed | Yes where AI filtering is common |
| References | agents.id |
| Meaning | Agent associated with a recommendation, draft, task, decision, memory or audit event |

---

## generated_by_ai

| Property | Definition |
|---|---|
| Type | BOOLEAN |
| Required | Yes where applicable |
| Default | false |
| Meaning | Indicates whether record was initially generated by AI |

Used by:

```text
operating_maps
```

---

## ai_assisted

| Property | Definition |
|---|---|
| Type | BOOLEAN |
| Required | In audit_events where applicable |
| Default | false |
| Meaning | Indicates whether AI assisted the action |

---

## human_confirmed

| Property | Definition |
|---|---|
| Type | BOOLEAN |
| Required | No |
| Meaning | Indicates whether a human confirmed an AI-assisted action |

Used by:

```text
audit_events
```

---

## confidence

| Property | Definition |
|---|---|
| Type | TEXT |
| Required | No |
| Meaning | Confidence classification for AI-generated or memory records |

Values are controlled by:

```text
11_ENUMS_AND_STATUSES.md
```

---

# 12. Classification Fields

## type fields

Common examples:

```text
gap_type
recommendation_type
responsibility_type
memory_type
policy_type
export_type
sync_type
metric_type
event_type
```

| Property | Definition |
|---|---|
| Type | TEXT |
| Required | Usually yes |
| Indexed | Often with workspace_id |
| Meaning | Stable category of the record |

Rule:

```text
Type fields classify what the object is. Status fields describe lifecycle state.
```

---

## severity

| Property | Definition |
|---|---|
| Type | TEXT |
| Required | Context-dependent |
| Indexed | Sometimes |
| Meaning | Importance or seriousness of record |

Common values:

```text
low
medium
high
critical
```

Dashboard/audit display values:

```text
info
warning
critical
```

---

## priority

| Property | Definition |
|---|---|
| Type | TEXT |
| Required | For tasks |
| Default | normal |
| Meaning | Execution priority |

Values:

```text
low
normal
high
urgent
```

---

# 13. Flexible Data Fields

## metadata

| Property | Definition |
|---|---|
| Type | JSONB |
| Required | No |
| Indexed | No by default |
| Meaning | Flexible non-core metadata |

Rule:

```text
metadata must not replace core modeled fields or relationships.
```

Not allowed:

```text
raw credentials
secret values
primary business relationships
```

---

## payload

| Property | Definition |
|---|---|
| Type | JSONB |
| Required | Context-dependent |
| Meaning | Event payload or draft object content |

Used by:

```text
runtime_events
agent_action_drafts
```

Rule:

```text
payload must not contain raw secrets or cross-workspace data.
```

---

## configuration

| Property | Definition |
|---|---|
| Type | JSONB |
| Required | No |
| Meaning | Structured configuration for integrations, templates or policies |

Used by:

```text
integrations
export_templates
```

---

## value

| Property | Definition |
|---|---|
| Type | JSONB |
| Required | In dashboard_metrics |
| Meaning | Calculated metric value in structured form |

Rule:

```text
Dashboard metric values must be derived from structured runtime objects.
```

---

# 14. Event and Audit Fields

## action

| Property | Definition |
|---|---|
| Type | TEXT |
| Required | Yes in audit_events |
| Meaning | Action that occurred |

Examples:

```text
task.created
decision.confirmed
export.completed
access.denied
```

---

## event_type

| Property | Definition |
|---|---|
| Type | TEXT |
| Required | Yes in runtime_events |
| Meaning | Type of runtime event emitted |

Examples:

```text
task.status_changed
memory.created
dashboard.updated
```

---

## correlation_id

| Property | Definition |
|---|---|
| Type | UUID |
| Required | No |
| Indexed | Yes where used |
| Meaning | Groups related events and audit records across one operation |

---

## causation_id

| Property | Definition |
|---|---|
| Type | UUID |
| Required | No |
| Indexed | Optional |
| Meaning | Points to the event that caused the current event |

---

## source_event_id

| Property | Definition |
|---|---|
| Type | UUID |
| Required | No |
| References | runtime_events.id |
| Meaning | Runtime event that caused or corresponds to an audit event |

---

## before_state

| Property | Definition |
|---|---|
| Type | JSONB |
| Required | No |
| Meaning | Snapshot of relevant object state before audited change |

---

## after_state

| Property | Definition |
|---|---|
| Type | JSONB |
| Required | No |
| Meaning | Snapshot of relevant object state after audited change |

---

# 15. Integration and Export Fields

## provider

| Property | Definition |
|---|---|
| Type | TEXT |
| Required | For integrations |
| Indexed | With workspace_id |
| Meaning | External system provider |

Examples:

```text
openai
google_drive
gmail
slack
manual_import
```

---

## credential_ref

| Property | Definition |
|---|---|
| Type | TEXT |
| Required | When integration uses credentials |
| Meaning | Reference to secret stored outside normal application tables |

Rule:

```text
credential_ref must never contain raw credential values.
```

---

## export_scope

| Property | Definition |
|---|---|
| Type | JSONB |
| Required | No, but recommended for exports |
| Meaning | Explicit scope of data included in an export |

Rule:

```text
Export scope must be workspace-scoped and auditable.
```

---

## file_reference

| Property | Definition |
|---|---|
| Type | TEXT |
| Required | When output file exists |
| Meaning | Reference to generated file or storage object |

Rule:

```text
file_reference should point to controlled storage, not expose unrestricted public access.
```

---

# 16. Review and Validity Fields

## review_required

| Property | Definition |
|---|---|
| Type | BOOLEAN |
| Required | No |
| Default | false |
| Meaning | Indicates whether record requires human review |

Used by:

```text
memory_entries
```

---

## review_date

| Property | Definition |
|---|---|
| Type | DATE |
| Required | No |
| Meaning | Planned review date for decision, memory or responsibility |

---

## valid_from

| Property | Definition |
|---|---|
| Type | DATE |
| Required | No |
| Meaning | Date from which the information is valid |

---

## valid_until

| Property | Definition |
|---|---|
| Type | DATE |
| Required | No |
| Meaning | Date until which the information is valid |

---

# 17. Tags and Search Fields

## tags

| Property | Definition |
|---|---|
| Type | TEXT[] |
| Required | No |
| Indexed | GIN later if needed |
| Meaning | Flexible labels for retrieval and grouping |

Used by:

```text
memory_entries
```

---

## summary

| Property | Definition |
|---|---|
| Type | TEXT |
| Required | No |
| Meaning | Short human-readable summary of larger content |

Used by:

```text
operating_maps
memory_entries
dashboard_snapshots
```

---

## content

| Property | Definition |
|---|---|
| Type | TEXT |
| Required | Where main narrative content is stored |
| Meaning | Main body of memory or textual business record |

Used by:

```text
memory_entries
```

---

# 18. Field Governance Rules

## Rule 1 — Same Name Means Same Meaning

A field name should not mean different things in different tables.

## Rule 2 — Status Is Lifecycle Only

Do not use `status` to encode category, ownership or priority.

## Rule 3 — Metadata Is Not a Shortcut

Do not hide core relationships or required fields inside `metadata`.

## Rule 4 — Workspace Scope Is Mandatory

Any operating object must include `workspace_id` unless explicitly global.

## Rule 5 — AI Output Must Be Traceable

AI-created or AI-assisted records should preserve source, agent and confirmation metadata where relevant.

## Rule 6 — Sensitive Data Must Not Leak

Do not store raw credentials, secrets or unrestricted access links in normal tables.

---

# 19. API and Backend Implications

API contracts should expose field meanings consistently.

Backend services should enforce:

```text
workspace_id consistency
status validation
object reference validation
confirmation rules
metadata boundaries
credential safety
source traceability
```

ORM models should preserve the same naming conventions and field semantics.

---

# 20. Acceptance Criteria

Data Dictionary is ready when:

- recurring fields are defined;
- field meanings are consistent;
- required and optional usage is clarified;
- AI governance fields are explained;
- audit and event fields are explained;
- integration and export fields are explained;
- metadata boundaries are defined;
- backend validation implications are documented.

Status:

```text
Accepted as Data Model Reference
```

---

# 21. Final Statement

```text
Bizzi Data Dictionary defines the shared meaning of recurring database fields so that data model, API contracts, backend services, audit logic and AI governance use one consistent implementation language.
```

This document strengthens the `27_DATA_MODEL` layer by turning table definitions into a reusable engineering vocabulary.