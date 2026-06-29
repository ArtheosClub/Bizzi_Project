# 10_DASHBOARD_EXPORT_DATA_MODEL.md

# Bizzi Platform

## Dashboard and Export Data Model

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Model Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL / 12_DASHBOARD_AND_EXPORT_DOMAIN.md  
**Previous Documents:** 00_DATA_MODEL_VISION.md, 01_DATABASE_PRINCIPLES.md, 02_ENTITY_TO_TABLE_MAPPING.md, 03_CORE_TABLES.md, 04_WORKSPACE_DATA_MODEL.md, 05_OPERATING_MAP_DATA_MODEL.md, 06_FUNCTION_RESPONSIBILITY_DATA_MODEL.md, 07_AGENT_PROCESS_TASK_DECISION_DATA_MODEL.md, 08_MEMORY_AUDIT_EVENT_DATA_MODEL.md, 09_INTEGRATION_SECURITY_DATA_MODEL.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Dashboard and Export Data Model for Bizzi Platform.

It translates the Dashboard and Export Domain into database tables, columns, relationships, constraints and indexing rules that support operating visibility, dashboard metrics, alerts, insights and governed exports.

Core question:

```text
How does Bizzi persist operating visibility and controlled business outputs as workspace-scoped, auditable and implementation-ready data?
```

---

# 2. Data Model Role

This data model defines how Bizzi stores what the user sees and what the system exports.

It supports:

- workspace dashboard metrics;
- operating health indicators;
- alerts and insights;
- export job tracking;
- export scope control;
- export file references;
- dashboard refresh by runtime events;
- audit evidence for exports;
- first-hour product value visibility.

---

# 3. Tables in Scope

Priority 1 MVP table:

```text
dashboard_metrics
```

Priority 2 governed output table:

```text
export_jobs
```

Expansion tables:

```text
dashboard_snapshots
dashboard_insights
dashboard_alerts
export_templates
export_files
```

Recommended MVP implementation:

```text
dashboard_metrics
export_jobs
```

MVP may also compute some dashboard views dynamically from core tables.

---

# 4. Workspace Scope Rule

All Dashboard and Export tables must include:

```text
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
```

This ensures dashboard state and exports are isolated by workspace and safe for permissions, AI context, audit and external sharing.

---

# 5. dashboard_metrics Table

## Purpose

Stores calculated operating indicators for a workspace dashboard.

## Domain Entity

```text
DashboardMetric
```

## Table

```text
dashboard_metrics
```

## Columns

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
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## Status Values

Initial values:

```text
calculated
visible
stale
archived
```

Expansion values:

```text
refreshing
error
```

## Severity Values

```text
info
warning
critical
```

## Notes

MVP may calculate many dashboard values dynamically.

Persisted metrics are useful for expensive calculations, audit-adjacent summaries and quick dashboard loading.

---

# 6. export_jobs Table

## Purpose

Stores controlled export requests and their lifecycle.

## Domain Entity

```text
ExportJob
```

## Table

```text
export_jobs
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
export_type TEXT NOT NULL
status TEXT NOT NULL
requested_by UUID NOT NULL REFERENCES users(id)
export_scope JSONB NULL
format TEXT NOT NULL
file_reference TEXT NULL
template_id UUID NULL
source_object_type TEXT NULL
source_object_id UUID NULL
destination_integration_id UUID NULL REFERENCES integrations(id)
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
started_at TIMESTAMPTZ NULL
completed_at TIMESTAMPTZ NULL
failed_at TIMESTAMPTZ NULL
error_message TEXT NULL
metadata JSONB NULL
```

## Export Type Values

Initial values:

```text
workspace_summary
operating_map_export
task_list_export
decision_log_export
```

Expansion values:

```text
memory_export
audit_export
implementation_brief
```

## Status Values

Initial values:

```text
requested
generating
completed
failed
```

Expansion values:

```text
queued
expired
cancelled
```

## Format Values

Initial values:

```text
markdown
pdf
```

Expansion values:

```text
csv
json
```

---

# 7. dashboard_snapshots Table

## Purpose

Stores a point-in-time dashboard state.

## Domain Entity

```text
DashboardSnapshot
```

## MVP Status

```text
Expansion
```

## Table

```text
dashboard_snapshots
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
snapshot_type TEXT NOT NULL
summary TEXT NULL
metrics JSONB NOT NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
created_by UUID NULL REFERENCES users(id)
metadata JSONB NULL
```

## MVP Simplification

Do not persist snapshots in the first MVP unless a report, audit pack or time-based comparison feature requires it.

---

# 8. dashboard_insights Table

## Purpose

Stores interpreted business insights derived from dashboard data.

## Domain Entity

```text
DashboardInsight
```

## MVP Status

```text
Expansion
```

## Table

```text
dashboard_insights
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
insight_type TEXT NOT NULL
title TEXT NOT NULL
description TEXT NULL
severity TEXT NULL
status TEXT NOT NULL
source_object_type TEXT NULL
source_object_id UUID NULL
created_by_agent_id UUID NULL REFERENCES agents(id)
confirmed_by UUID NULL REFERENCES users(id)
confirmed_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## MVP Simplification

Dashboard insights may initially be generated dynamically and not persisted.

Persist later when insights need review, memory, audit or follow-up tasks.

---

# 9. dashboard_alerts Table

## Purpose

Stores dashboard warnings requiring user attention.

## Domain Entity

```text
DashboardAlert
```

## MVP Status

```text
Expansion / Optional Near-MVP
```

## Table

```text
dashboard_alerts
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
alert_type TEXT NOT NULL
title TEXT NOT NULL
description TEXT NULL
severity TEXT NOT NULL
status TEXT NOT NULL
source_object_type TEXT NULL
source_object_id UUID NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
resolved_at TIMESTAMPTZ NULL
resolved_by UUID NULL REFERENCES users(id)
metadata JSONB NULL
```

## MVP Simplification

Alerts may first be represented by `dashboard_metrics` with severity and status.

---

# 10. export_templates Table

## Purpose

Stores reusable export structures and report configurations.

## Domain Entity

```text
ExportTemplate
```

## MVP Status

```text
Expansion
```

## Table

```text
export_templates
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NULL REFERENCES company_workspaces(id)
name TEXT NOT NULL
export_type TEXT NOT NULL
format TEXT NOT NULL
configuration JSONB NOT NULL
status TEXT NOT NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
created_by UUID NULL REFERENCES users(id)
metadata JSONB NULL
```

## Notes

Templates may be global when `workspace_id` is NULL.

MVP may use hardcoded templates.

---

# 11. export_files Table

## Purpose

Stores metadata for produced export artifacts.

## Domain Entity

```text
ExportFile
```

## MVP Status

```text
Expansion
```

## Table

```text
export_files
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
export_job_id UUID NOT NULL REFERENCES export_jobs(id)
file_name TEXT NOT NULL
file_type TEXT NOT NULL
file_reference TEXT NOT NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
expires_at TIMESTAMPTZ NULL
metadata JSONB NULL
```

## MVP Simplification

Use this field on `export_jobs` first:

```text
file_reference TEXT
```

---

# 12. Relationships

## Workspace to Dashboard Metrics

```text
company_workspaces.id → dashboard_metrics.workspace_id
```

Relationship:

```text
CompanyWorkspace 1 → many DashboardMetrics
```

## Workspace to Export Jobs

```text
company_workspaces.id → export_jobs.workspace_id
```

Relationship:

```text
CompanyWorkspace 1 → many ExportJobs
```

## Export Job to User

```text
users.id → export_jobs.requested_by
```

Relationship:

```text
User 1 → many ExportJobs
```

## Export Job to Integration

```text
integrations.id → export_jobs.destination_integration_id
```

Relationship:

```text
Integration 1 → many ExportJobs
```

## Export Job to Export File

```text
export_jobs.id → export_files.export_job_id
```

Relationship:

```text
ExportJob 1 → many ExportFiles
```

---

# 13. Source Traceability

Dashboard metrics, insights, alerts and export jobs may use:

```text
source_object_type
source_object_id
```

Examples:

```text
source_object_type = 'task'
source_object_type = 'decision'
source_object_type = 'operating_gap'
source_object_type = 'audit_event'
source_object_type = 'runtime_event'
```

This allows Bizzi to explain why a dashboard value or export exists.

---

# 14. Indexing Requirements

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

## dashboard_alerts

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(workspace_id, severity)
INDEX(source_object_type, source_object_id)
```

## export_files

```text
INDEX(workspace_id)
INDEX(export_job_id)
INDEX(expires_at)
```

---

# 15. Data Integrity Rules

Database-level rules:

```text
dashboard_metrics.workspace_id IS NOT NULL
dashboard_metrics.metric_type IS NOT NULL
dashboard_metrics.name IS NOT NULL
dashboard_metrics.value IS NOT NULL
dashboard_metrics.status IS NOT NULL
export_jobs.workspace_id IS NOT NULL
export_jobs.export_type IS NOT NULL
export_jobs.status IS NOT NULL
export_jobs.requested_by IS NOT NULL
export_jobs.format IS NOT NULL
```

Service-level rules:

```text
Dashboard data must be generated from workspace-scoped sources.
Export jobs must be authorized before generation.
Export scope must not include cross-workspace data.
Completed export jobs should have file_reference or export artifact metadata.
Failed export jobs must preserve error_message.
AI-generated export summaries must respect workspace and security boundaries.
```

---

# 16. Dashboard Refresh Pattern

Dashboard refresh may be triggered by runtime events:

```text
task.created
task.status_changed
decision.confirmed
memory.created
audit.recorded
integration.sync_completed
access.denied
```

Flow:

```text
RuntimeEvent
↓
Dashboard handler
↓
Metric calculation
↓
dashboard_metrics upsert
↓
dashboard.updated event
```

MVP may compute dashboard values directly from source tables until persisted metrics are needed.

---

# 17. Export Generation Pattern

Export generation flow:

```text
User requests export
↓
Authorization checked
↓
export_jobs inserted with status = requested
↓
Export generation starts
↓
status = generating
↓
file_reference stored when complete
↓
status = completed
↓
Audit event recorded
↓
Runtime event emitted
```

Failure flow:

```text
status = failed
error_message recorded
Audit event recorded if needed
```

---

# 18. Audit Requirements

Audited actions include:

```text
export.requested
export.authorized
export.denied
export.started
export.completed
export.failed
export.file_accessed
dashboard.critical_alert_created
dashboard.security_warning_displayed
```

Audit target examples:

```text
object_type = 'export_job'
object_id = export_jobs.id
```

```text
object_type = 'dashboard_metric'
object_id = dashboard_metrics.id
```

---

# 19. Runtime Event Requirements

Runtime events include:

```text
dashboard.metric_calculated
dashboard.metric_updated
dashboard.alert_created
dashboard.alert_resolved
export.requested
export.started
export.completed
export.failed
export.file_created
```

Event source pattern:

```text
source_object_type = 'dashboard_metric'
source_object_id = dashboard_metrics.id
```

or:

```text
source_object_type = 'export_job'
source_object_id = export_jobs.id
```

---

# 20. AI Requirements

AI may assist by:

- summarizing dashboard state;
- explaining metrics;
- drafting export summaries;
- highlighting operating gaps;
- identifying next actions.

AI-generated dashboard or export content must preserve:

```text
source_object_type
source_object_id
created_by_agent_id where applicable
confirmed_by where required
metadata
```

Rule:

```text
Dashboard facts must come from structured runtime objects, not invented narrative.
```

---

# 21. Security Requirements

Dashboard and export security rules:

```text
Dashboard data must be workspace-scoped.
Export data must be workspace-scoped.
Export generation requires authorization.
Export files require controlled access.
Export scope must be explicit.
Sensitive audit or security data must not be exported without permission.
AI-generated export summaries must respect workspace and integration boundaries.
```

---

# 22. MVP Simplifications

For MVP, Bizzi may simplify by:

- using `dashboard_metrics` for persisted indicators only where useful;
- computing many dashboard values dynamically from source tables;
- using hardcoded export templates;
- storing export file reference directly on `export_jobs`;
- postponing dashboard_snapshots, dashboard_insights and export_files;
- using text statuses before PostgreSQL ENUM migration.

These simplifications must preserve workspace scope and export auditability.

---

# 23. Future Expansion

Future tables may include:

```text
dashboard_snapshots
dashboard_insights
dashboard_alerts
dashboard_widgets
export_templates
export_files
scheduled_reports
report_subscriptions
```

These should be introduced when product behavior requires deeper reporting or configurable dashboards.

---

# 24. Acceptance Criteria

This data model is ready when:

- dashboard_metrics table is defined;
- export_jobs table is defined;
- dashboard expansion tables are identified;
- export expansion tables are identified;
- workspace scoping is explicit;
- dashboard refresh pattern is defined;
- export generation pattern is defined;
- indexes are identified;
- audit, event, AI and security requirements are documented;
- MVP simplifications are documented.

Status:

```text
Accepted for Implementation Planning
```

---

# 25. Final Statement

```text
Bizzi Dashboard and Export Data Model defines how the platform persists operating visibility and governed outputs as workspace-scoped, source-linked, auditable and secure database records.
```

This model allows Bizzi to show what is happening, what needs attention and what can be safely exported.