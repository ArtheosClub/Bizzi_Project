# 03_CORE_TABLES.md

# Bizzi Platform

## Core Tables

**Layer:** 27_DATA_MODEL  
**Component Type:** Core Data Model Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Previous Documents:** 00_DATA_MODEL_VISION.md, 01_DATABASE_PRINCIPLES.md, 02_ENTITY_TO_TABLE_MAPPING.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the core database tables for Bizzi Platform.

It establishes the first implementation-ready table foundation for MVP storage, using the Domain Model and Entity-to-Table Mapping as source references.

Core question:

```text
Which tables form the minimum durable persistence foundation for Bizzi MVP, and what structural responsibilities does each table carry?
```

---

# 2. Core Table Role

Core tables are the tables required for the first runnable Bizzi vertical slice.

They must support:

- user identity;
- workspace creation;
- workspace settings;
- operating map generation;
- operating gap tracking;
- function definition;
- responsibility assignment;
- task execution;
- decision logging;
- memory creation;
- audit recording;
- runtime event coordination;
- dashboard visibility.

---

# 3. Core Table Set

Priority 1 MVP tables:

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

These tables are sufficient for the first MVP chain:

```text
User
↓
Workspace
↓
Operating Map
↓
Functions and Responsibilities
↓
Tasks and Decisions
↓
Memory
↓
Audit and Events
↓
Dashboard
```

---

# 4. Common Table Standards

Most operating tables should include:

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL
status TEXT NOT NULL
created_at TIMESTAMPTZ NOT NULL
updated_at TIMESTAMPTZ NOT NULL
created_by UUID NULL
metadata JSONB NULL
```

Recommended timestamp defaults:

```sql
created_at TIMESTAMPTZ DEFAULT now()
updated_at TIMESTAMPTZ DEFAULT now()
```

The exact implementation may be adjusted by ORM and migration tooling.

---

# 5. Global vs Workspace-Scoped Tables

Global or user-level tables:

```text
users
sessions
```

Workspace-root table:

```text
company_workspaces
```

Workspace-scoped operating tables:

```text
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

Rule:

```text
Every workspace-scoped table must include workspace_id and be queryable by workspace_id.
```

---

# 6. users

## Purpose

Stores human identities.

## Domain Entity

```text
User
```

## Minimum Columns

```text
id UUID PRIMARY KEY
email TEXT NOT NULL UNIQUE
name TEXT NULL
status TEXT NOT NULL
created_at TIMESTAMPTZ NOT NULL
updated_at TIMESTAMPTZ NOT NULL
```

## Notes

`users` is not workspace-scoped because one user may later access multiple workspaces.

## Initial Indexes

```text
users.email UNIQUE
users.status
```

---

# 7. sessions

## Purpose

Stores authenticated session records or session references.

## Domain Entity

```text
Session
```

## Minimum Columns

```text
id UUID PRIMARY KEY
user_id UUID NOT NULL REFERENCES users(id)
status TEXT NOT NULL
created_at TIMESTAMPTZ NOT NULL
expires_at TIMESTAMPTZ NULL
last_seen_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## Notes

The actual authentication provider may store session state externally, but Bizzi may keep session references for security events and audit correlation.

## Initial Indexes

```text
sessions.user_id
sessions.status
sessions.expires_at
```

---

# 8. company_workspaces

## Purpose

Stores one company workspace as the root operating boundary.

## Domain Entity

```text
CompanyWorkspace
```

## Minimum Columns

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
created_at TIMESTAMPTZ NOT NULL
updated_at TIMESTAMPTZ NOT NULL
archived_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## Notes

`company_workspaces` is the root tenant boundary for Bizzi operating data.

## Initial Indexes

```text
company_workspaces.owner_user_id
company_workspaces.slug UNIQUE
company_workspaces.status
```

---

# 9. workspace_settings

## Purpose

Stores workspace-level configuration.

## Domain Entity

```text
WorkspaceSettings
```

## Minimum Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
language TEXT NULL
timezone TEXT NULL
default_currency TEXT NULL
ai_assistance_enabled BOOLEAN NOT NULL DEFAULT true
memory_enabled BOOLEAN NOT NULL DEFAULT true
audit_enabled BOOLEAN NOT NULL DEFAULT true
created_at TIMESTAMPTZ NOT NULL
updated_at TIMESTAMPTZ NOT NULL
metadata JSONB NULL
```

## Notes

One workspace should normally have one settings record.

## Initial Indexes

```text
workspace_settings.workspace_id UNIQUE
```

---

# 10. operating_maps

## Purpose

Stores structured operating maps for a workspace.

## Domain Entity

```text
OperatingMap
```

## Minimum Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
title TEXT NOT NULL
summary TEXT NULL
status TEXT NOT NULL
version INTEGER NOT NULL DEFAULT 1
generated_by_ai BOOLEAN NOT NULL DEFAULT false
confirmed_by UUID NULL REFERENCES users(id)
confirmed_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL
updated_at TIMESTAMPTZ NOT NULL
created_by UUID NULL REFERENCES users(id)
archived_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## Notes

MVP may support one active operating map per workspace.

## Initial Indexes

```text
operating_maps.workspace_id
operating_maps.workspace_id, status
```

---

# 11. operating_gaps

## Purpose

Stores detected operating gaps.

## Domain Entity

```text
OperatingGap
```

## Minimum Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
operating_map_id UUID NULL REFERENCES operating_maps(id)
function_id UUID NULL REFERENCES functions(id)
gap_type TEXT NOT NULL
title TEXT NOT NULL
description TEXT NULL
severity TEXT NULL
status TEXT NOT NULL
source_object_type TEXT NULL
source_object_id UUID NULL
resolved_by_object_type TEXT NULL
resolved_by_object_id UUID NULL
resolved_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL
updated_at TIMESTAMPTZ NOT NULL
created_by UUID NULL REFERENCES users(id)
metadata JSONB NULL
```

## Notes

This table supports first-hour value by making missing ownership, process and execution areas visible.

## Initial Indexes

```text
operating_gaps.workspace_id
operating_gaps.workspace_id, status
operating_gaps.operating_map_id
operating_gaps.function_id
```

---

# 12. functions

## Purpose

Stores business functions or operating areas.

## Domain Entity

```text
Function
```

## Minimum Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
name TEXT NOT NULL
category TEXT NULL
description TEXT NULL
purpose TEXT NULL
status TEXT NOT NULL
priority TEXT NULL
risk_level TEXT NULL
maturity_level TEXT NULL
source_object_type TEXT NULL
source_object_id UUID NULL
confirmed_by UUID NULL REFERENCES users(id)
confirmed_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL
updated_at TIMESTAMPTZ NOT NULL
created_by UUID NULL REFERENCES users(id)
archived_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## Notes

Functions are central to operating map, task routing and responsibility assignment.

## Initial Indexes

```text
functions.workspace_id
functions.workspace_id, status
functions.workspace_id, category
```

---

# 13. responsibilities

## Purpose

Stores ownership and accountability assignments.

## Domain Entity

```text
Responsibility
```

## Minimum Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
object_type TEXT NOT NULL
object_id UUID NOT NULL
owner_user_id UUID NULL REFERENCES users(id)
responsibility_type TEXT NOT NULL
status TEXT NOT NULL
scope TEXT NULL
assigned_by UUID NULL REFERENCES users(id)
assigned_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL
updated_at TIMESTAMPTZ NOT NULL
metadata JSONB NULL
```

## Notes

The pair `object_type + object_id` allows responsibility assignment across functions, processes, tasks and decisions.

## Initial Indexes

```text
responsibilities.workspace_id
responsibilities.workspace_id, object_type, object_id
responsibilities.owner_user_id
responsibilities.workspace_id, status
```

---

# 14. tasks

## Purpose

Stores actionable work.

## Domain Entity

```text
Task
```

## Minimum Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
title TEXT NOT NULL
description TEXT NULL
status TEXT NOT NULL
priority TEXT NOT NULL DEFAULT 'normal'
owner_user_id UUID NULL REFERENCES users(id)
function_id UUID NULL REFERENCES functions(id)
process_id UUID NULL REFERENCES processes(id)
decision_id UUID NULL REFERENCES decisions(id)
agent_id UUID NULL REFERENCES agents(id)
operating_gap_id UUID NULL REFERENCES operating_gaps(id)
source_object_type TEXT NULL
source_object_id UUID NULL
due_date DATE NULL
completed_at TIMESTAMPTZ NULL
archived_at TIMESTAMPTZ NULL
blocked_reason TEXT NULL
confirmed_by UUID NULL REFERENCES users(id)
confirmed_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL
updated_at TIMESTAMPTZ NOT NULL
created_by UUID NULL REFERENCES users(id)
metadata JSONB NULL
```

## Notes

Some foreign keys reference Priority 2 tables such as `processes` and `agents`; implementation can add nullable fields before those tables are fully used.

## Initial Indexes

```text
tasks.workspace_id
tasks.workspace_id, status
tasks.owner_user_id
tasks.function_id
tasks.process_id
tasks.decision_id
tasks.due_date
tasks.source_object_type, source_object_id
```

---

# 15. decisions

## Purpose

Stores important business decisions.

## Domain Entity

```text
Decision
```

## Minimum Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
title TEXT NOT NULL
context TEXT NULL
final_decision TEXT NULL
rationale TEXT NULL
owner_user_id UUID NULL REFERENCES users(id)
status TEXT NOT NULL
function_id UUID NULL REFERENCES functions(id)
process_id UUID NULL REFERENCES processes(id)
task_id UUID NULL REFERENCES tasks(id)
agent_id UUID NULL REFERENCES agents(id)
source_object_type TEXT NULL
source_object_id UUID NULL
decision_date DATE NULL
review_date DATE NULL
expected_impact TEXT NULL
risk_level TEXT NULL
outcome_summary TEXT NULL
confirmed_by UUID NULL REFERENCES users(id)
confirmed_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL
updated_at TIMESTAMPTZ NOT NULL
created_by UUID NULL REFERENCES users(id)
archived_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## Notes

Confirmed decisions must have final decision content and owner in service-level validation.

## Initial Indexes

```text
decisions.workspace_id
decisions.workspace_id, status
decisions.owner_user_id
decisions.function_id
decisions.process_id
decisions.task_id
decisions.decision_date
```

---

# 16. memory_entries

## Purpose

Stores reusable enterprise memory.

## Domain Entity

```text
MemoryEntry
```

## Minimum Columns

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
review_required BOOLEAN NOT NULL DEFAULT false
review_date DATE NULL
created_at TIMESTAMPTZ NOT NULL
updated_at TIMESTAMPTZ NOT NULL
created_by UUID NULL REFERENCES users(id)
archived_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## Notes

Memory must remain workspace-scoped and source-linked where possible.

## Initial Indexes

```text
memory_entries.workspace_id
memory_entries.workspace_id, status
memory_entries.workspace_id, memory_type
memory_entries.source_object_type, source_object_id
memory_entries.function_id
memory_entries.process_id
memory_entries.task_id
memory_entries.decision_id
memory_entries.agent_id
```

---

# 17. audit_events

## Purpose

Stores evidence of governed runtime actions.

## Domain Entity

```text
AuditEvent
```

## Minimum Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
actor_id UUID NULL REFERENCES users(id)
actor_type TEXT NOT NULL
action TEXT NOT NULL
object_type TEXT NOT NULL
object_id UUID NULL
timestamp TIMESTAMPTZ NOT NULL
source_event_id UUID NULL REFERENCES runtime_events(id)
agent_id UUID NULL REFERENCES agents(id)
ai_assisted BOOLEAN NOT NULL DEFAULT false
human_confirmed BOOLEAN NULL
before_state JSONB NULL
after_state JSONB NULL
severity TEXT NULL
correlation_id UUID NULL
metadata JSONB NULL
```

## Notes

Audit events should be append-oriented and not silently deleted.

## Initial Indexes

```text
audit_events.workspace_id
audit_events.workspace_id, timestamp
audit_events.actor_id
audit_events.object_type, object_id
audit_events.action
audit_events.correlation_id
```

---

# 18. runtime_events

## Purpose

Stores meaningful runtime state changes.

## Domain Entity

```text
RuntimeEvent
```

## Minimum Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
event_type TEXT NOT NULL
source_component TEXT NULL
source_object_type TEXT NULL
source_object_id UUID NULL
actor_id UUID NULL REFERENCES users(id)
timestamp TIMESTAMPTZ NOT NULL
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

## Notes

Runtime events coordinate audit, memory and dashboard updates.

## Initial Indexes

```text
runtime_events.workspace_id
runtime_events.workspace_id, event_type
runtime_events.workspace_id, status
runtime_events.source_object_type, source_object_id
runtime_events.correlation_id
runtime_events.timestamp
```

---

# 19. dashboard_metrics

## Purpose

Stores calculated operating indicators.

## Domain Entity

```text
DashboardMetric
```

## Minimum Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
metric_type TEXT NOT NULL
name TEXT NOT NULL
value JSONB NOT NULL
status TEXT NOT NULL
category TEXT NULL
source_object_type TEXT NULL
source_object_id UUID NULL
calculation_method TEXT NULL
severity TEXT NULL
trend TEXT NULL
created_at TIMESTAMPTZ NOT NULL
updated_at TIMESTAMPTZ NOT NULL
metadata JSONB NULL
```

## Notes

Dashboard metrics may also be generated dynamically in MVP, but storing them supports refresh and visibility.

## Initial Indexes

```text
dashboard_metrics.workspace_id
dashboard_metrics.workspace_id, metric_type
dashboard_metrics.workspace_id, status
dashboard_metrics.updated_at
```

---

# 20. Core Foreign Key Considerations

Some core tables reference Priority 2 tables that may be created shortly after MVP core tables:

```text
processes
agents
```

Implementation options:

1. Create minimal `processes` and `agents` tables early.
2. Add nullable references later through migration.
3. Use source_object_type/source_object_id until detailed tables exist.

Recommended approach:

```text
Create minimal Priority 2 tables early if the MVP includes agent or process views.
Otherwise add nullable references through controlled migration.
```

---

# 21. Core Status Dependencies

Core tables depend on controlled statuses such as:

```text
workspace_status
operating_map_status
operating_gap_status
function_status
responsibility_status
task_status
decision_status
memory_status
audit_severity
runtime_event_status
dashboard_metric_status
```

These are fully defined later in:

```text
11_ENUMS_AND_STATUSES.md
```

---

# 22. Core Indexing Requirements

At minimum, all workspace-scoped tables require:

```text
workspace_id
workspace_id + status
created_at or updated_at where used for lists
```

Object traceability tables should include:

```text
source_object_type + source_object_id
object_type + object_id
```

Detailed strategy is defined later in:

```text
12_INDEXING_STRATEGY.md
```

---

# 23. MVP Core Acceptance Criteria

The core table model is ready when:

- Priority 1 tables are defined;
- each core table maps to a Domain Model entity;
- workspace scope is explicit;
- primary keys are UUID-based;
- key foreign keys are identified;
- common columns are consistent;
- audit and runtime events are first-class;
- dashboard storage is represented;
- next detailed domain-specific data model files can build on this foundation.

Status:

```text
Accepted for Detailed Data Model Expansion
```

---

# 24. Final Core Tables Statement

```text
Bizzi Core Tables define the minimum durable database foundation required to operate the first MVP vertical slice: workspace, operating map, functions, responsibilities, tasks, decisions, memory, audit, events and dashboard visibility.
```

This document becomes the baseline for detailed table definitions across the rest of the `27_DATA_MODEL` layer.