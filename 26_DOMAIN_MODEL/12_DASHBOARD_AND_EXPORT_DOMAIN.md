# 12_DASHBOARD_AND_EXPORT_DOMAIN.md

# Bizzi Platform

## Dashboard and Export Domain

**Layer:** 26_DOMAIN_MODEL  
**Component Type:** Domain Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Previous Documents:** 00_DOMAIN_MODEL_VISION.md, 01_ENTITY_CATALOG.md, 02_WORKSPACE_DOMAIN.md, 03_OPERATING_MAP_DOMAIN.md, 04_FUNCTION_AND_RESPONSIBILITY_DOMAIN.md, 05_AGENT_DOMAIN.md, 06_PROCESS_DOMAIN.md, 07_TASK_DOMAIN.md, 08_DECISION_DOMAIN.md, 09_MEMORY_DOMAIN.md, 10_AUDIT_AND_EVENT_DOMAIN.md, 11_INTEGRATION_AND_SECURITY_DOMAIN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Dashboard and Export Domain for Bizzi Platform.

The domain describes how Bizzi represents operating visibility, dashboard metrics, summaries, export jobs and shareable business outputs as structured product objects.

Core question:

```text
How does Bizzi make workspace operating state visible, understandable and exportable without losing traceability, security and governance?
```

---

# 2. Domain Role

The Dashboard and Export Domain is the visibility and output domain of Bizzi.

It provides:

- workspace operating overview;
- dashboard metrics;
- operating health indicators;
- task and gap visibility;
- agent and memory visibility;
- audit and security warnings;
- export jobs;
- controlled shareable outputs;
- first-hour value presentation;
- product experience readiness.

---

# 3. Domain Principles

## 3.1 Visibility Before Complexity

Bizzi should first make business state visible before adding advanced analytics.

## 3.2 Dashboard Reflects Runtime State

Dashboard data should be derived from structured runtime objects, not disconnected text.

## 3.3 Export with Governance

Exports must be scoped, authorized and auditable.

## 3.4 First-Hour Value

The dashboard should quickly show what Bizzi discovered, structured and recommends next.

---

# 4. Aggregate Boundaries

Primary aggregate roots:

```text
DashboardMetric
ExportJob
```

Supporting entities:

```text
DashboardSnapshot
DashboardInsight
DashboardWidget
DashboardAlert
ExportTemplate
ExportFile
ExportScope
ExportStatus
```

Related external entities:

```text
CompanyWorkspace
User
OperatingMap
OperatingGap
Function
Responsibility
Agent
Process
Task
Decision
MemoryEntry
AuditEvent
RuntimeEvent
Integration
SecurityEvent
```

---

# 5. Core Dashboard Entities

## 5.1 DashboardMetric

Represents a calculated operating indicator.

Minimum domain attributes:

```text
id
workspace_id
metric_type
name
value
status
created_at
updated_at
```

Optional domain attributes:

```text
category
source_object_type
source_object_id
calculation_method
severity
trend
metadata
```

Domain responsibility:

```text
DashboardMetric converts runtime state into visible operating indicators.
```

---

## 5.2 DashboardSnapshot

Represents a point-in-time view of workspace operating state.

Potential attributes:

```text
id
workspace_id
snapshot_type
summary
metrics
created_at
created_by
```

Domain responsibility:

```text
DashboardSnapshot preserves a structured view of the workspace at a specific moment.
```

MVP simplification:

```text
Snapshots may initially be generated dynamically instead of persisted.
```

---

## 5.3 DashboardInsight

Represents a meaningful interpretation of dashboard data.

Potential attributes:

```text
id
workspace_id
insight_type
title
description
severity
source_object_type
source_object_id
status
created_at
```

Domain responsibility:

```text
DashboardInsight turns metrics into understandable business meaning.
```

---

## 5.4 DashboardAlert

Represents a warning or important dashboard signal.

Potential attributes:

```text
id
workspace_id
alert_type
title
description
severity
status
created_at
resolved_at
```

Domain responsibility:

```text
DashboardAlert highlights operating risks, gaps or security issues that require attention.
```

---

# 6. Core Export Entities

## 6.1 ExportJob

Represents a controlled export of workspace data.

Minimum domain attributes:

```text
id
workspace_id
export_type
status
requested_by
created_at
updated_at
```

Optional domain attributes:

```text
export_scope
format
file_reference
completed_at
failed_at
error_message
template_id
destination_integration_id
```

Domain responsibility:

```text
ExportJob creates governed shareable outputs from workspace operating data.
```

---

## 6.2 ExportTemplate

Represents a reusable export structure.

Potential attributes:

```text
id
workspace_id
name
export_type
format
configuration
status
created_at
updated_at
```

Domain responsibility:

```text
ExportTemplate defines repeatable export formats for reports, summaries and operating documents.
```

MVP simplification:

```text
Export templates may be hardcoded before becoming editable domain objects.
```

---

## 6.3 ExportFile

Represents the produced file or output artifact.

Potential attributes:

```text
id
workspace_id
export_job_id
file_name
file_type
file_reference
created_at
expires_at
```

Domain responsibility:

```text
ExportFile represents the generated output artifact while preserving access and audit control.
```

---

# 7. Dashboard Metric Types

Initial metric types:

```text
workspace_status
operating_map_status
open_operating_gaps
ownership_gaps
active_functions
active_agents
active_processes
open_tasks
blocked_tasks
completed_tasks
recent_decisions
memory_entries
audit_events
integration_status
security_warnings
```

MVP priority metrics:

```text
open_operating_gaps
ownership_gaps
active_functions
open_tasks
recent_decisions
memory_entries
active_agents
security_warnings
```

---

# 8. Export Types

Initial export types:

```text
workspace_summary
operating_map_export
task_list_export
decision_log_export
memory_export
audit_export
implementation_brief
```

MVP priority exports:

```text
workspace_summary
operating_map_export
task_list_export
decision_log_export
```

---

# 9. Export Formats

Initial export formats:

```text
markdown
pdf
csv
json
```

MVP priority formats:

```text
markdown
pdf
```

---

# 10. Dashboard Lifecycle

Dashboard metrics may follow this lifecycle:

```text
calculated
↓
visible
↓
refreshed
↓
stale
↓
archived
```

MVP simplification:

```text
Metrics may be recalculated on demand or refreshed by runtime events.
```

---

# 11. Export Lifecycle

Recommended lifecycle:

```text
requested
↓
queued
↓
generating
↓
completed
↓
failed
↓
expired
```

MVP lifecycle:

```text
requested
generating
completed
failed
```

---

# 12. Domain Relationships

## 12.1 Workspace to DashboardMetric

```text
CompanyWorkspace 1 → many DashboardMetrics
```

## 12.2 RuntimeEvent to DashboardMetric

```text
RuntimeEvent may trigger DashboardMetric update
```

## 12.3 DashboardMetric to Source Object

```text
DashboardMetric → source_object_type + source_object_id
```

## 12.4 Workspace to ExportJob

```text
CompanyWorkspace 1 → many ExportJobs
```

## 12.5 ExportJob to User

```text
ExportJob many → 1 requesting User
```

## 12.6 ExportJob to AuditEvent

```text
ExportJob should create AuditEvent
```

---

# 13. Domain Invariants

The Dashboard and Export Domain must enforce:

```text
DashboardMetric must belong to one workspace.
ExportJob must belong to one workspace.
ExportJob must have requested_by.
Export content must be workspace-scoped.
Export generation must be authorized.
Export generation must be auditable.
Dashboard metrics must not expose unauthorized data.
Metrics derived from archived objects should be handled explicitly.
Failed export jobs must preserve error state.
```

---

# 14. AI Dashboard Rules

AI may assist by:

- summarizing dashboard state;
- explaining operating gaps;
- identifying next actions;
- drafting export summaries;
- preparing management briefs;
- highlighting risks and blockers.

AI may not:

- invent metrics not grounded in runtime objects;
- hide critical warnings;
- export data without authorization;
- include cross-workspace data;
- include secrets or credential values;
- override audit requirements.

MVP rule:

```text
AI may explain dashboard state, but dashboard facts must come from structured runtime objects.
```

---

# 15. Dashboard Refresh Flow

```text
Runtime event occurs
↓
Dashboard handler receives event
↓
Affected metric identified
↓
Metric recalculated or refreshed
↓
Dashboard insight or alert created if needed
↓
Audit recorded for sensitive dashboard changes if needed
↓
User sees updated operating state
```

---

# 16. Export Generation Flow

```text
User requests export
↓
Authorization checked
↓
Export scope defined
↓
Workspace data selected
↓
Export generated
↓
Export file reference created
↓
Runtime event emitted
↓
Audit event recorded
↓
Dashboard export activity updated
```

---

# 17. Domain Events

Dashboard events:

```text
dashboard.metric_calculated
dashboard.metric_updated
dashboard.insight_created
dashboard.alert_created
dashboard.alert_resolved
dashboard.snapshot_created
```

Export events:

```text
export.requested
export.authorized
export.denied
export.started
export.completed
export.failed
export.file_created
export.expired
```

---

# 18. Audit Requirements

Audited actions:

```text
export.requested
export.authorized
export.denied
export.completed
export.failed
export.file_accessed
dashboard.critical_alert_created
dashboard.security_warning_displayed
```

Audit must answer:

```text
Who requested or accessed an export, what data scope was included, and which workspace was affected?
```

---

# 19. Memory Requirements

Memory may be created from:

- dashboard insights;
- recurring dashboard warnings;
- operating health summaries;
- exported management summaries;
- repeated blockers or risks;
- resolved dashboard alerts.

Memory types:

```text
dashboard_insight
operating_health_summary
export_summary
recurring_warning
resolved_alert
```

---

# 20. Security Requirements

Security requirements:

```text
Dashboard data must be workspace-scoped.
Export data must be workspace-scoped.
Only authorized users may generate exports.
Export files should have controlled access.
Export scope must be explicit.
Sensitive audit or security data must not be exported without permission.
AI-generated export summaries must respect workspace and integration boundaries.
```

---

# 21. MVP Domain Behavior

MVP should support:

```text
Show workspace dashboard
Show operating map status
Show open tasks
Show ownership gaps
Show recent decisions
Show memory count
Show active agents
Show audit warnings
Generate workspace summary export
Generate task list export
Generate decision log export
Record export audit event
Show export status
```

---

# 22. Out of Scope for MVP

The Dashboard and Export Domain does not need in MVP:

- advanced BI dashboards;
- custom dashboard builder;
- real-time collaborative dashboards;
- complex charting engine;
- scheduled reporting;
- external data warehouse;
- custom report designer;
- multi-workspace analytics;
- automated board packs.

---

# 23. Data Model Implications

Future Data Model should include tables or collections for:

```text
dashboard_metrics
export_jobs
```

Potential later tables:

```text
dashboard_snapshots
dashboard_insights
dashboard_alerts
export_templates
export_files
```

Recommended indexes later:

```text
dashboard_metrics.workspace_id
dashboard_metrics.metric_type
dashboard_metrics.status
dashboard_metrics.updated_at
export_jobs.workspace_id
export_jobs.requested_by
export_jobs.export_type
export_jobs.status
export_jobs.created_at
```

---

# 24. API Implications

Future API contracts should support:

```text
GET /workspaces/{workspace_id}/dashboard
GET /workspaces/{workspace_id}/dashboard/metrics
GET /workspaces/{workspace_id}/dashboard/alerts
POST /workspaces/{workspace_id}/dashboard/refresh
POST /workspaces/{workspace_id}/exports
GET /workspaces/{workspace_id}/exports
GET /workspaces/{workspace_id}/exports/{export_job_id}
GET /workspaces/{workspace_id}/exports/{export_job_id}/file
```

---

# 25. Traceability Pattern

Dashboard and export traceability chain:

```text
Runtime Object / Runtime Event
↓
DashboardMetric / DashboardInsight
↓
Dashboard View / ExportJob
↓
ExportFile if generated
↓
AuditEvent
↓
MemoryEntry if useful
```

---

# 26. Acceptance Criteria

Dashboard and Export Domain is ready when:

- DashboardMetric is defined as aggregate root;
- ExportJob is defined as aggregate root;
- dashboard metric types are defined;
- export types and formats are defined;
- dashboard refresh behavior is defined;
- export generation behavior is defined;
- audit and security rules are explicit;
- data model and API implications are identified.

Status:

```text
Ready for Data Model and API Design
```

---

# 27. Architecture Alignment

| Dashboard and Export Domain Area | Reference |
|---|---|
| DashboardMetric | Core User Journey / Runtime Architecture |
| Dashboard Insights | Memory Runtime / Event Runtime |
| Operating Map Metrics | Operating Map Domain |
| Task Metrics | Task Domain |
| Decision Metrics | Decision Domain |
| Agent Metrics | Agent Domain |
| ExportJob | Integration Runtime / Runtime Security |
| Export Audit | Audit Runtime |
| Export Security | Runtime Security |
| Export Memory | Memory Runtime |

---

# 28. Final Dashboard and Export Domain Statement

```text
Dashboard and Export Domain defines how Bizzi makes workspace operating state visible, understandable and shareable through structured metrics, insights, alerts and governed exports.
```

This domain ensures Bizzi can show what is happening, what needs attention and what can be safely shared outside the runtime.