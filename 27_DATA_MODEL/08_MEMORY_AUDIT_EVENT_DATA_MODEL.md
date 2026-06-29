# 08_MEMORY_AUDIT_EVENT_DATA_MODEL.md

# Bizzi Platform

## Memory, Audit and Event Data Model

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Model Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 08_MEMORY_RUNTIME.md, 09_AUDIT_RUNTIME.md, 10_EVENT_RUNTIME.md  
**Domain Reference:** 26_DOMAIN_MODEL / 09_MEMORY_DOMAIN.md, 10_AUDIT_AND_EVENT_DOMAIN.md  
**Previous Documents:** 00_DATA_MODEL_VISION.md, 01_DATABASE_PRINCIPLES.md, 02_ENTITY_TO_TABLE_MAPPING.md, 03_CORE_TABLES.md, 04_WORKSPACE_DATA_MODEL.md, 05_OPERATING_MAP_DATA_MODEL.md, 06_FUNCTION_RESPONSIBILITY_DATA_MODEL.md, 07_AGENT_PROCESS_TASK_DECISION_DATA_MODEL.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the data model for Memory, Audit and Runtime Events in Bizzi Platform.

It translates the Memory Domain and Audit and Event Domain into database tables, columns, relationships, constraints and indexing rules that support enterprise knowledge persistence, governed traceability and runtime coordination.

Core question:

```text
How does Bizzi persist what the company knows, what changed, who acted, and which runtime events coordinate the operating system?
```

---

# 2. Data Model Role

This data model is the trust and continuity foundation of Bizzi.

It supports:

- reusable enterprise memory;
- memory source traceability;
- AI context retrieval boundaries;
- audit records;
- runtime events;
- human confirmation evidence;
- AI assistance evidence;
- dashboard freshness;
- export traceability;
- future observability and compliance.

---

# 3. Tables in Scope

Priority 1 MVP tables:

```text
memory_entries
audit_events
runtime_events
```

Expansion tables:

```text
memory_sources
memory_links
memory_reviews
memory_usage
audit_exports
event_failures
event_correlations
event_handler_runs
```

Recommended MVP implementation:

```text
memory_entries
audit_events
runtime_events
```

---

# 4. Workspace Scope Rule

All Memory, Audit and Event tables must include:

```text
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
```

This protects workspace isolation, AI context safety, memory retrieval boundaries, audit filtering, event processing, dashboard accuracy and export scope control.

---

# 5. memory_entries Table

## Purpose

Stores reusable enterprise knowledge as structured, source-linked memory.

## Domain Entity

```text
MemoryEntry
```

## Table

```text
memory_entries
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
memory_type TEXT NOT NULL
title TEXT NOT NULL
content TEXT NOT NULL
summary TEXT NULL
status TEXT NOT NULL
confidence TEXT NULL
source_object_type TEXT NULL
source_object_id UUID NULL
function_id UUID NULL REFERENCES functions(id)
process_id UUID NULL REFERENCES processes(id)
task_id UUID NULL REFERENCES tasks(id)
decision_id UUID NULL REFERENCES decisions(id)
agent_id UUID NULL REFERENCES agents(id)
tags TEXT[] NULL
valid_from DATE NULL
valid_until DATE NULL
review_required BOOLEAN NOT NULL DEFAULT false
review_date DATE NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
created_by UUID NULL REFERENCES users(id)
archived_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## Status Values

Initial values:

```text
candidate
active
archived
```

Expansion values:

```text
draft
confirmed
reviewed
updated
rejected
```

## Confidence Values

Initial values:

```text
manual
ai_suggested
confirmed
```

Expansion values:

```text
low
medium
high
verified
```

## Notes

Memory entries must be source-linked where possible.

AI-generated memory should remain candidate or draft until confirmation rules allow activation.

---

# 6. audit_events Table

## Purpose

Stores evidence of governed runtime actions.

## Domain Entity

```text
AuditEvent
```

## Table

```text
audit_events
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
actor_id UUID NULL REFERENCES users(id)
actor_type TEXT NOT NULL
action TEXT NOT NULL
object_type TEXT NOT NULL
object_id UUID NULL
timestamp TIMESTAMPTZ NOT NULL DEFAULT now()
source_event_id UUID NULL REFERENCES runtime_events(id)
agent_id UUID NULL REFERENCES agents(id)
ai_assisted BOOLEAN NOT NULL DEFAULT false
human_confirmed BOOLEAN NULL
before_state JSONB NULL
after_state JSONB NULL
severity TEXT NULL
correlation_id UUID NULL
client_context TEXT NULL
metadata JSONB NULL
```

## Actor Types

Initial values:

```text
user
agent
system
integration
```

## Severity Values

Initial values:

```text
info
warning
critical
```

Expansion value:

```text
notice
```

## Notes

Audit events should be append-oriented and should not be silently deleted.

Sensitive data should not be stored in audit metadata.

---

# 7. runtime_events Table

## Purpose

Stores meaningful runtime state changes and coordination events.

## Domain Entity

```text
RuntimeEvent
```

## Table

```text
runtime_events
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
event_type TEXT NOT NULL
source_component TEXT NULL
source_object_type TEXT NULL
source_object_id UUID NULL
actor_id UUID NULL REFERENCES users(id)
timestamp TIMESTAMPTZ NOT NULL DEFAULT now()
payload JSONB NULL
status TEXT NOT NULL
correlation_id UUID NULL
causation_id UUID NULL
severity TEXT NULL
processed_at TIMESTAMPTZ NULL
error_message TEXT NULL
retry_count INTEGER NOT NULL DEFAULT 0
metadata JSONB NULL
```

## Status Values

Initial values:

```text
emitted
processed
failed
```

Expansion values:

```text
processing
ignored
```

## Notes

Runtime events coordinate audit creation, memory creation and dashboard refresh.

They are not merely logs; they are product coordination records.

---

# 8. memory_sources Table

## Purpose

Stores normalized memory source records.

## Domain Entity

```text
MemorySource
```

## MVP Status

```text
Expansion
```

## Table

```text
memory_sources
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
memory_id UUID NOT NULL REFERENCES memory_entries(id)
source_object_type TEXT NOT NULL
source_object_id UUID NULL
source_actor_id UUID NULL REFERENCES users(id)
source_agent_id UUID NULL REFERENCES agents(id)
source_created_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## MVP Simplification

Use these fields directly on `memory_entries`:

```text
source_object_type
source_object_id
created_by
agent_id
metadata
```

---

# 9. memory_usage Table

## Purpose

Stores records of memory being used in AI context or runtime decisions.

## Domain Entity

```text
MemoryUsage
```

## MVP Status

```text
Expansion
```

## Table

```text
memory_usage
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
memory_id UUID NOT NULL REFERENCES memory_entries(id)
used_by_object_type TEXT NULL
used_by_object_id UUID NULL
used_by_agent_id UUID NULL REFERENCES agents(id)
purpose TEXT NULL
used_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## MVP Simplification

Memory usage may initially be recorded through audit events.

---

# 10. event_failures Table

## Purpose

Stores failed runtime event handling attempts.

## Domain Entity

```text
EventFailure
```

## MVP Status

```text
Expansion
```

## Table

```text
event_failures
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
runtime_event_id UUID NOT NULL REFERENCES runtime_events(id)
handler_name TEXT NOT NULL
error_message TEXT NULL
retry_count INTEGER NOT NULL DEFAULT 0
status TEXT NOT NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
resolved_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## MVP Simplification

Use these fields directly on `runtime_events`:

```text
status
error_message
retry_count
```

---

# 11. Relationships

## Workspace to Memory

```text
company_workspaces.id → memory_entries.workspace_id
```

Relationship:

```text
CompanyWorkspace 1 → many MemoryEntries
```

## Workspace to Audit

```text
company_workspaces.id → audit_events.workspace_id
```

Relationship:

```text
CompanyWorkspace 1 → many AuditEvents
```

## Workspace to Runtime Events

```text
company_workspaces.id → runtime_events.workspace_id
```

Relationship:

```text
CompanyWorkspace 1 → many RuntimeEvents
```

## Runtime Event to Audit Event

```text
runtime_events.id → audit_events.source_event_id
```

Relationship:

```text
RuntimeEvent 1 → many AuditEvents
```

## Memory to Domain Objects

```text
memory_entries.function_id → functions.id
memory_entries.process_id → processes.id
memory_entries.task_id → tasks.id
memory_entries.decision_id → decisions.id
memory_entries.agent_id → agents.id
```

---

# 12. Source Traceability

Memory source fields:

```text
source_object_type
source_object_id
```

Audit target fields:

```text
object_type
object_id
```

Runtime event source fields:

```text
source_object_type
source_object_id
```

Correlation fields:

```text
correlation_id
causation_id
source_event_id
```

These fields allow Bizzi to reconstruct:

```text
Source Object
↓
Runtime Event
↓
Audit Event
↓
Memory Entry
↓
Dashboard Metric
```

---

# 13. Indexing Requirements

## memory_entries

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, memory_type)
INDEX(source_object_type, source_object_id)
INDEX(function_id)
INDEX(process_id)
INDEX(task_id)
INDEX(decision_id)
INDEX(agent_id)
INDEX(created_at)
```

Optional later:

```text
GIN(tags)
GIN(metadata)
FULL TEXT INDEX(title, content, summary)
```

## audit_events

```text
INDEX(workspace_id)
INDEX(workspace_id, timestamp)
INDEX(actor_id)
INDEX(object_type, object_id)
INDEX(action)
INDEX(source_event_id)
INDEX(agent_id)
INDEX(correlation_id)
INDEX(workspace_id, severity)
```

## runtime_events

```text
INDEX(workspace_id)
INDEX(workspace_id, event_type)
INDEX(workspace_id, status)
INDEX(source_object_type, source_object_id)
INDEX(actor_id)
INDEX(correlation_id)
INDEX(causation_id)
INDEX(timestamp)
```

---

# 14. Data Integrity Rules

Database-level rules:

```text
memory_entries.workspace_id IS NOT NULL
memory_entries.memory_type IS NOT NULL
memory_entries.title IS NOT NULL
memory_entries.content IS NOT NULL
memory_entries.status IS NOT NULL
audit_events.workspace_id IS NOT NULL
audit_events.actor_type IS NOT NULL
audit_events.action IS NOT NULL
audit_events.object_type IS NOT NULL
audit_events.timestamp IS NOT NULL
runtime_events.workspace_id IS NOT NULL
runtime_events.event_type IS NOT NULL
runtime_events.timestamp IS NOT NULL
runtime_events.status IS NOT NULL
```

Service-level rules:

```text
Archived memory cannot be used as active AI context.
AI-generated memory must preserve source traceability.
Audit events should not be deleted through normal flows.
Runtime event payloads must exclude sensitive credential material.
Memory retrieval must be workspace-scoped.
Audit filtering must be workspace-scoped.
Event handlers must enforce workspace boundaries.
```

---

# 15. AI Memory and Audit Rules

AI-generated or AI-used records should preserve:

```text
agent_id
ai_assisted
human_confirmed
source_object_type
source_object_id
confidence
metadata
```

AI memory rules:

```text
AI may suggest memory candidates.
AI may retrieve active workspace-scoped memory.
AI may not use archived memory as active context.
AI may not create untraceable active memory.
```

AI audit rules:

```text
If AI output changes a runtime object, the system must record AI involvement and human confirmation status.
```

---

# 16. Audit Requirements

Audit actions should include:

```text
memory.candidate_created
memory.created
memory.confirmed
memory.used_in_ai_context
memory.archived
runtime_event.emitted
runtime_event.failed
agent.output_confirmed
task.status_changed
decision.confirmed
export.generated
access.denied
```

Audit events must answer:

```text
Who or what acted?
What action occurred?
Which object was affected?
Was AI involved?
Was human confirmation required or provided?
```

---

# 17. Runtime Event Requirements

MVP runtime events should include:

```text
workspace.created
operating_map.generated
function.created
responsibility.assigned
agent.recommendation_created
process.created
task.created
task.status_changed
decision.confirmed
memory.created
memory.used_in_context
audit.recorded
dashboard.updated
access.denied
```

Event handlers may update:

- audit records;
- memory candidates;
- dashboard metrics;
- notifications later;
- integration status later.

---

# 18. Dashboard Requirements

Dashboard queries should support:

- recent memory entries;
- memory candidates needing review;
- memory by type;
- recent audit events;
- critical audit events;
- failed runtime events;
- AI-assisted actions;
- human confirmations;
- task and decision activity.

Core query support:

```text
memory_entries.workspace_id, status
memory_entries.workspace_id, memory_type
audit_events.workspace_id, timestamp
audit_events.workspace_id, severity
runtime_events.workspace_id, status
runtime_events.workspace_id, event_type
```

---

# 19. Export Requirements

Memory, audit and event data may be exported later.

Export rules:

```text
Exports must be workspace-scoped.
Audit exports require authorization.
Memory exports should exclude archived or sensitive memory unless explicitly authorized.
Runtime event exports should avoid sensitive payload material.
```

---

# 20. MVP Simplifications

For MVP, Bizzi may simplify by:

- implementing only `memory_entries`, `audit_events` and `runtime_events`;
- using `source_object_type/source_object_id` instead of normalized memory_sources;
- using audit_events instead of memory_usage;
- using runtime_events.status and error_message instead of event_failures;
- using text statuses before PostgreSQL ENUM migration;
- storing event payloads and audit metadata as JSONB.

These simplifications must preserve workspace scope, source traceability and AI auditability.

---

# 21. Future Expansion

Future tables may include:

```text
memory_sources
memory_links
memory_reviews
memory_usage
memory_embeddings
audit_exports
event_failures
event_correlations
event_handler_runs
event_subscriptions
```

These should be introduced only when product behavior requires them.

---

# 22. Acceptance Criteria

This data model is ready when:

- memory_entries table is defined;
- audit_events table is defined;
- runtime_events table is defined;
- workspace scoping is explicit;
- source traceability is defined;
- AI memory and audit rules are documented;
- indexes are identified;
- dashboard and export requirements are defined;
- MVP simplifications are documented.

Status:

```text
Accepted for Implementation Planning
```

---

# 23. Final Statement

```text
Bizzi Memory, Audit and Event Data Model defines how the platform persists enterprise knowledge, governed action evidence and runtime coordination events as workspace-scoped, source-linked, auditable and AI-safe database records.
```

This model gives Bizzi durable memory, trust and traceability.