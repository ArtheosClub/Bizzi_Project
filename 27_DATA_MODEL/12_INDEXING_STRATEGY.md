# 12_INDEXING_STRATEGY.md

# Bizzi Platform

## Indexing Strategy

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Model Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Previous Documents:** 00_DATA_MODEL_VISION.md, 01_DATABASE_PRINCIPLES.md, 02_ENTITY_TO_TABLE_MAPPING.md, 03_CORE_TABLES.md, 04_WORKSPACE_DATA_MODEL.md, 05_OPERATING_MAP_DATA_MODEL.md, 06_FUNCTION_RESPONSIBILITY_DATA_MODEL.md, 07_AGENT_PROCESS_TASK_DECISION_DATA_MODEL.md, 08_MEMORY_AUDIT_EVENT_DATA_MODEL.md, 09_INTEGRATION_SECURITY_DATA_MODEL.md, 10_DASHBOARD_EXPORT_DATA_MODEL.md, 11_ENUMS_AND_STATUSES.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the initial indexing strategy for Bizzi Platform.

It identifies the indexes required to support workspace isolation, dashboard loading, task execution, decision logs, memory retrieval, audit review, runtime event handling, integrations, exports and future API filtering.

Core question:

```text
Which database indexes does Bizzi need so that MVP queries are reliable, fast and aligned with workspace-scoped product behavior?
```

---

# 2. Indexing Role

Indexes support:

- workspace-scoped queries;
- dashboard performance;
- task lists;
- decision logs;
- memory retrieval;
- audit history;
- runtime event processing;
- integration status visibility;
- export job tracking;
- owner-based work views;
- source traceability queries.

---

# 3. Indexing Principles

## 3.1 Workspace First

Most operating queries begin with:

```sql
WHERE workspace_id = :workspace_id
```

Therefore most operating tables should have at least:

```text
INDEX(workspace_id)
```

## 3.2 Workspace + Status

Most list views filter by lifecycle state.

Common pattern:

```text
INDEX(workspace_id, status)
```

## 3.3 Workspace + Type

Many dashboards and APIs filter by type.

Common pattern:

```text
INDEX(workspace_id, type_column)
```

Examples:

```text
INDEX(workspace_id, memory_type)
INDEX(workspace_id, event_type)
INDEX(workspace_id, export_type)
```

## 3.4 Source Traceability

Objects that reference source objects should support:

```text
INDEX(source_object_type, source_object_id)
```

## 3.5 Avoid Over-Indexing Early

Every index has write cost.

MVP should index real access patterns, not every possible column.

---

# 4. Common Index Patterns

## Workspace Index

```text
INDEX(workspace_id)
```

Used by almost all workspace-scoped tables.

## Workspace Status Index

```text
INDEX(workspace_id, status)
```

Used by list views and dashboards.

## Workspace Created Index

```text
INDEX(workspace_id, created_at)
```

Used by recent activity lists.

## Workspace Updated Index

```text
INDEX(workspace_id, updated_at)
```

Used by freshness checks and dashboard refresh.

## Owner Index

```text
INDEX(owner_user_id)
```

Used by task, process, decision and responsibility ownership views.

## Source Object Index

```text
INDEX(source_object_type, source_object_id)
```

Used by traceability chains.

---

# 5. Identity and Workspace Indexes

## users

```text
UNIQUE(email)
INDEX(status)
```

Purpose:

- login lookup;
- user status filtering.

## sessions

```text
INDEX(user_id)
INDEX(status)
INDEX(expires_at)
```

Purpose:

- session lookup;
- active session filtering;
- cleanup of expired sessions.

## company_workspaces

```text
INDEX(owner_user_id)
UNIQUE(slug)
INDEX(status)
INDEX(owner_user_id, status)
```

Purpose:

- owner workspace list;
- public or internal workspace slug lookup;
- active workspace filtering.

## workspace_settings

```text
UNIQUE(workspace_id)
```

Purpose:

- one settings record per workspace.

## workspace_access

```text
UNIQUE(workspace_id, user_id)
INDEX(user_id)
INDEX(workspace_id, status)
INDEX(workspace_id, role)
```

Purpose:

- authorization checks;
- user workspace list;
- role-based filtering.

---

# 6. Operating Map Indexes

## operating_maps

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, version)
```

Optional later:

```text
UNIQUE(workspace_id, version)
PARTIAL UNIQUE(workspace_id) WHERE status = 'active'
```

Purpose:

- active operating map lookup;
- version history;
- workspace map list.

## operating_gaps

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, gap_type)
INDEX(operating_map_id)
INDEX(function_id)
INDEX(source_object_type, source_object_id)
INDEX(resolved_by_object_type, resolved_by_object_id)
```

Purpose:

- dashboard gap counts;
- open gap lists;
- gap by function;
- source and resolution traceability.

## operating_recommendations

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, recommendation_type)
INDEX(operating_map_id)
INDEX(source_gap_id)
INDEX(result_object_type, result_object_id)
```

Purpose:

- pending recommendations;
- recommendation review flow;
- applied recommendation traceability.

---

# 7. Function and Responsibility Indexes

## functions

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, category)
INDEX(parent_function_id)
INDEX(source_object_type, source_object_id)
```

Optional later:

```text
UNIQUE(workspace_id, name)
```

Purpose:

- active function list;
- function category dashboard;
- hierarchy lookup;
- source traceability.

## responsibilities

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, object_type, object_id)
INDEX(owner_user_id)
INDEX(assigned_by)
```

Optional later:

```text
UNIQUE(workspace_id, object_type, object_id, responsibility_type)
```

Purpose:

- object ownership lookup;
- owner workload view;
- responsibility dashboard.

## ownership_gaps

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, gap_type)
INDEX(workspace_id, object_type, object_id)
INDEX(recommended_owner_id)
INDEX(resolved_by_responsibility_id)
```

Purpose:

- ownership gap dashboard;
- gap resolution tracking.

---

# 8. Agent Indexes

## agents

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(human_owner_id)
INDEX(function_id)
INDEX(process_id)
INDEX(source_object_type, source_object_id)
```

Purpose:

- active agent list;
- agents by owner;
- agents by function or process.

## agent_authority_scopes

```text
INDEX(workspace_id)
INDEX(agent_id)
INDEX(workspace_id, status)
```

Purpose:

- authority lookup during AI execution;
- authority lifecycle filtering.

## agent_recommendations

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(agent_id)
INDEX(source_object_type, source_object_id)
INDEX(result_object_type, result_object_id)
```

Purpose:

- pending AI recommendation review;
- recommendation traceability;
- recommendation result lookup.

## agent_action_drafts

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(agent_id)
INDEX(source_object_type, source_object_id)
INDEX(result_object_type, result_object_id)
```

Purpose:

- pending draft review;
- applied draft traceability.

---

# 9. Process Indexes

## processes

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(function_id)
INDEX(owner_user_id)
INDEX(agent_id)
INDEX(source_object_type, source_object_id)
```

Purpose:

- active process lists;
- processes by function;
- processes by owner;
- process source traceability.

## process_steps

```text
INDEX(workspace_id)
INDEX(process_id)
INDEX(process_id, step_order)
```

Recommended constraint:

```text
UNIQUE(process_id, step_order)
```

Purpose:

- ordered process step retrieval;
- process editor loading.

---

# 10. Task Indexes

## tasks

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(owner_user_id)
INDEX(function_id)
INDEX(process_id)
INDEX(decision_id)
INDEX(agent_id)
INDEX(operating_gap_id)
INDEX(due_date)
INDEX(source_object_type, source_object_id)
```

Recommended additional MVP index:

```text
INDEX(workspace_id, owner_user_id, status)
```

Optional later:

```text
INDEX(workspace_id, due_date, status)
```

Purpose:

- open task list;
- task board;
- owner task view;
- overdue task view;
- source traceability;
- dashboard task metrics.

---

# 11. Decision Indexes

## decisions

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(owner_user_id)
INDEX(function_id)
INDEX(process_id)
INDEX(task_id)
INDEX(agent_id)
INDEX(decision_date)
INDEX(source_object_type, source_object_id)
```

Recommended additional index:

```text
INDEX(workspace_id, decision_date)
```

Purpose:

- decision log;
- recent decisions;
- decisions by function, task or process;
- decision review lists.

---

# 12. Memory Indexes

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

Recommended MVP additional index:

```text
INDEX(workspace_id, status, memory_type)
```

Optional later:

```text
GIN(tags)
GIN(metadata)
FULL TEXT INDEX(title, content, summary)
```

Purpose:

- active memory retrieval;
- memory by type;
- memory source traceability;
- AI context assembly.

---

# 13. Audit and Event Indexes

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

Recommended MVP additional index:

```text
INDEX(workspace_id, object_type, object_id)
```

Purpose:

- audit history;
- object timeline;
- actor activity;
- critical audit filtering;
- AI-assisted action review.

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

Recommended MVP additional index:

```text
INDEX(workspace_id, status, event_type)
```

Purpose:

- event processing;
- failed event lookup;
- event timeline;
- dashboard refresh.

---

# 14. Integration and Security Indexes

## integrations

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, provider)
INDEX(created_by)
INDEX(last_sync_at)
```

Purpose:

- active integration list;
- provider filtering;
- integration health dashboard.

## integration_sync_jobs

```text
INDEX(workspace_id)
INDEX(integration_id)
INDEX(workspace_id, status)
INDEX(workspace_id, sync_type)
INDEX(started_at)
INDEX(completed_at)
```

Purpose:

- sync job history;
- failed sync lookup;
- integration activity dashboard.

## security_policies

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, policy_type)
```

Purpose:

- active policy lookup;
- AI context and export policy checks.

## security_events

```text
INDEX(workspace_id)
INDEX(user_id)
INDEX(event_type)
INDEX(severity)
INDEX(created_at)
```

Purpose:

- security dashboard;
- access event review.

---

# 15. Dashboard and Export Indexes

## dashboard_metrics

```text
INDEX(workspace_id)
INDEX(workspace_id, metric_type)
INDEX(workspace_id, status)
INDEX(workspace_id, category)
INDEX(workspace_id, severity)
INDEX(updated_at)
INDEX(source_object_type, source_object_id)
```

Recommended MVP additional index:

```text
INDEX(workspace_id, metric_type, status)
```

Purpose:

- fast dashboard loading;
- metric refresh;
- warning and severity filtering.

## export_jobs

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, export_type)
INDEX(requested_by)
INDEX(created_at)
INDEX(completed_at)
INDEX(source_object_type, source_object_id)
INDEX(destination_integration_id)
```

Purpose:

- export history;
- export lifecycle tracking;
- user export list;
- failed export lookup.

## export_files

```text
INDEX(workspace_id)
INDEX(export_job_id)
INDEX(expires_at)
```

Purpose:

- file lookup by export job;
- cleanup of expired export files.

---

# 16. MVP Minimum Index Set

The minimum practical MVP index set should include:

```text
users.email UNIQUE
sessions.user_id
company_workspaces.owner_user_id
workspace_settings.workspace_id UNIQUE
operating_maps.workspace_id, status
operating_gaps.workspace_id, status
functions.workspace_id, status
responsibilities.workspace_id, object_type, object_id
tasks.workspace_id, status
tasks.workspace_id, owner_user_id, status
decisions.workspace_id, status
memory_entries.workspace_id, status
memory_entries.workspace_id, memory_type
audit_events.workspace_id, timestamp
audit_events.workspace_id, object_type, object_id
runtime_events.workspace_id, status
runtime_events.workspace_id, event_type
dashboard_metrics.workspace_id, metric_type, status
```

If exports and integrations are included in MVP:

```text
integrations.workspace_id, status
integration_sync_jobs.integration_id
export_jobs.workspace_id, status
```

---

# 17. Dashboard Query Support

Dashboard requires fast access to:

```text
open tasks
blocked tasks
overdue tasks
recent decisions
active functions
ownership gaps
active agents
memory count
recent audit events
failed runtime events
active integrations
security warnings
```

Recommended dashboard-oriented indexes:

```text
tasks(workspace_id, status)
tasks(workspace_id, due_date, status)
decisions(workspace_id, decision_date)
functions(workspace_id, status)
responsibilities(workspace_id, object_type, object_id)
memory_entries(workspace_id, status, memory_type)
audit_events(workspace_id, timestamp)
runtime_events(workspace_id, status, event_type)
dashboard_metrics(workspace_id, metric_type, status)
```

---

# 18. Traceability Query Support

Traceability requires source and target lookup.

Recommended indexes:

```text
source_object_type, source_object_id
object_type, object_id
resolved_by_object_type, resolved_by_object_id
result_object_type, result_object_id
```

Used by:

```text
operating_gaps
operating_recommendations
functions
agent_recommendations
agent_action_drafts
processes
tasks
decisions
memory_entries
audit_events
runtime_events
dashboard_metrics
export_jobs
```

---

# 19. PostgreSQL Index Types

Recommended MVP index type:

```text
BTREE
```

Use for:

- UUID fields;
- status values;
- timestamps;
- foreign keys;
- type fields.

Optional later:

```text
GIN
```

Use for:

- JSONB metadata queries;
- tags array;
- full-text search.

Potential future:

```text
Partial indexes
Expression indexes
Full-text search indexes
Vector indexes
```

These should be added only after access patterns are clear.

---

# 20. Partial Index Candidates

Potential later partial indexes:

```sql
CREATE INDEX idx_tasks_open
ON tasks(workspace_id, owner_user_id)
WHERE status IN ('open', 'in_progress', 'blocked');
```

```sql
CREATE INDEX idx_memory_active
ON memory_entries(workspace_id, memory_type)
WHERE status = 'active';
```

```sql
CREATE INDEX idx_runtime_events_failed
ON runtime_events(workspace_id, event_type)
WHERE status = 'failed';
```

```sql
CREATE INDEX idx_integrations_active
ON integrations(workspace_id, provider)
WHERE status = 'active';
```

Use partial indexes after real query behavior is observed.

---

# 21. Index Naming Convention

Recommended convention:

```text
idx_<table>_<columns>
```

Examples:

```text
idx_tasks_workspace_status
idx_tasks_workspace_owner_status
idx_audit_events_workspace_timestamp
idx_memory_entries_workspace_type
idx_runtime_events_workspace_status_type
```

Unique indexes:

```text
uq_<table>_<columns>
```

Examples:

```text
uq_users_email
uq_workspace_settings_workspace
uq_workspace_access_workspace_user
```

---

# 22. Indexing Anti-Patterns

Avoid:

```text
indexing every column
creating indexes without query purpose
missing workspace_id in multi-tenant queries
using JSONB indexes before query patterns exist
forgetting indexes on foreign keys used in joins
using only single-column indexes where composite indexes are needed
not reviewing index usage after MVP traffic
```

---

# 23. Migration and Review Strategy

Index creation should follow migration discipline:

```text
Define initial MVP indexes
↓
Measure query patterns
↓
Add composite indexes for real bottlenecks
↓
Remove unused indexes if needed
↓
Add partial or GIN indexes only with evidence
```

Production migrations should consider concurrent index creation where supported.

---

# 24. Acceptance Criteria

Indexing Strategy is ready when:

- common index patterns are defined;
- workspace-first indexing is enforced;
- MVP minimum indexes are identified;
- dashboard indexes are identified;
- traceability indexes are identified;
- table-level index recommendations are documented;
- PostgreSQL index type strategy is documented;
- anti-patterns are listed.

Status:

```text
Accepted for Data Model Milestone
```

---

# 25. Final Statement

```text
Bizzi Indexing Strategy defines the database access-path foundation required for workspace isolation, dashboard performance, task execution, memory retrieval, audit review, runtime event handling and traceability across the platform.
```

This strategy completes the core technical foundation of the `27_DATA_MODEL` layer before milestone and audit.