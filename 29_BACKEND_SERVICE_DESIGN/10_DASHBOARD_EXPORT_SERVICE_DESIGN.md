# 10_DASHBOARD_EXPORT_SERVICE_DESIGN.md

# Bizzi Platform

## Dashboard Export Service Design

**Layer:** 29_BACKEND_SERVICE_DESIGN  
**Component Type:** Backend Service Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 13_RUNTIME_MILESTONE.md, 14_RUNTIME_PLATFORM_AUDIT.md  
**Domain Reference:** 26_DOMAIN_MODEL / 12_DASHBOARD_AND_EXPORT_DOMAIN.md  
**Data Model Reference:** 27_DATA_MODEL / 10_DASHBOARD_EXPORT_DATA_MODEL.md  
**API Contracts Reference:** 28_API_CONTRACTS / 09_DASHBOARD_EXPORT_API.md  
**Previous Document:** 09_INTEGRATION_SECURITY_SERVICE_DESIGN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the backend service design for dashboard and export behavior in Bizzi Platform.

It specifies the services, repositories, validation rules, authorization rules, computation patterns, transaction patterns, audit events and runtime events required to implement the Dashboard Export API.

Core question:

```text
How should Bizzi backend services compute operating visibility and generate governed exports safely, efficiently and consistently?
```

---

# 2. Service Scope

This design covers:

```text
DashboardService
DashboardMetricService
DashboardActivityService
DashboardRefreshService
ExportService
ExportJobService
ExportFileService
ExportGenerationService
```

Primary API references:

```text
GET /api/v1/workspaces/{workspace_id}/dashboard
GET /api/v1/workspaces/{workspace_id}/dashboard/metrics
POST /api/v1/workspaces/{workspace_id}/dashboard/metrics/refresh
GET /api/v1/workspaces/{workspace_id}/dashboard/activity
GET /api/v1/workspaces/{workspace_id}/export-jobs
POST /api/v1/workspaces/{workspace_id}/export-jobs
GET /api/v1/workspaces/{workspace_id}/export-jobs/{export_job_id}
POST /api/v1/workspaces/{workspace_id}/export-jobs/{export_job_id}/cancel
GET /api/v1/workspaces/{workspace_id}/export-jobs/{export_job_id}/download
```

Primary data references:

```text
dashboard_metrics
dashboard_snapshots
dashboard_insights
dashboard_alerts
export_jobs
export_files
tasks
decisions
memory_entries
audit_events
runtime_events
operating_gaps
integrations
```

---

# 3. Module Ownership

Dashboard and export behavior belongs to:

```text
DashboardModule
ExportModule
```

Supporting modules:

```text
WorkspaceModule
AuthorizationModule
ValidationModule
AuditModule
EventModule
TaskModule
DecisionModule
MemoryModule
OperatingMapModule
IntegrationModule
JobQueueModule
IdempotencyModule
TransactionModule
```

Rule:

```text
DashboardModule owns operating visibility. ExportModule owns governed export lifecycle and export file access.
```

---

# 4. Service Responsibilities

## DashboardService

Responsibilities:

```text
compute dashboard summary
combine dynamic and persisted metrics
read operating status
read workspace health indicators
include optional activity, alerts and insights
respect workspace authorization
return dashboard DTO
```

## DashboardMetricService

Responsibilities:

```text
list dashboard metrics
compute metric values
persist selected metric records
validate metric filters
support period-based metrics
```

## DashboardActivityService

Responsibilities:

```text
assemble recent activity
read audit events and runtime events
map events into activity DTOs
filter by actor, object and time
respect restricted event visibility
```

## DashboardRefreshService

Responsibilities:

```text
request dashboard refresh
process dashboard.refresh_requested events
recompute selected metrics
store dashboard_metrics records
coordinate future snapshots, insights and alerts
```

## ExportService

Responsibilities:

```text
create export jobs
validate export_type and format
validate export_scope
check export authorization
coordinate idempotency
emit export audit and runtime events
```

## ExportJobService

Responsibilities:

```text
list export jobs
get export job
cancel export job
track export lifecycle
validate status transitions
```

## ExportGenerationService

Responsibilities:

```text
execute export generation internally
collect export data
render export output
store export file reference
mark export completed or failed
emit export completion runtime events
```

## ExportFileService

Responsibilities:

```text
create temporary download links
validate export availability
validate file expiration
protect sensitive exports
expire export files
preserve export metadata
```

---

# 5. Repository Responsibilities

## DashboardMetricRepository

Methods:

```text
createMetric(data)
createManyMetrics(metrics)
findByIdAndWorkspace(metric_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
findLatestByType(workspace_id, metric_type)
deleteOrArchiveOldMetrics(workspace_id, retention_policy) later
```

## DashboardSnapshotRepository later

Methods:

```text
createSnapshot(data)
findByIdAndWorkspace(snapshot_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
```

## ExportJobRepository

Methods:

```text
createExportJob(data)
findByIdAndWorkspace(export_job_id, workspace_id)
listByWorkspace(workspace_id, filters, pagination)
updateStatus(export_job_id, workspace_id, status_data)
cancelByIdAndWorkspace(export_job_id, workspace_id, cancel_data)
markCompleted(export_job_id, workspace_id, completed_data)
markFailed(export_job_id, workspace_id, failure_data)
findByIdempotencyKey(workspace_id, idempotency_key)
```

## ExportFileRepository

Methods:

```text
createExportFile(data)
findByExportJobId(workspace_id, export_job_id)
markExpired(export_file_id, workspace_id, expiration_data)
listExpiredFiles(now)
```

---

# 6. Service Context

Every service method must receive:

```text
workspace_id
actor_id
actor_type
correlation_id
request_id
idempotency_key optional
```

Export generation internal context may also include:

```text
export_job_id
internal_service_actor
job_id
```

Rule:

```text
Dashboard and export services must never read or export data outside the workspace scope defined by context.
```

---

# 7. Dashboard Summary Flow

## Service Method

```text
DashboardService.getDashboardSummary(context, input)
```

## Input

```text
include_activity optional
include_alerts optional
include_insights optional
```

## Flow

```text
validate authenticated actor
load workspace
check dashboard view permission
compute current summary values
load latest persisted metrics if needed
compute health indicators
optionally load recent activity
optionally load alerts and insights later
return dashboard summary DTO
```

Summary values may include:

```text
open_tasks
overdue_tasks
completed_tasks_30d
confirmed_decisions
active_memory_entries
open_operating_gaps
active_integrations
```

---

# 8. Dashboard Summary Computation Rules

Computation rules:

```text
open_tasks count tasks with open or in_progress status
overdue_tasks count non-completed tasks with due_date before current date
completed_tasks_30d count completed tasks completed within last 30 days
confirmed_decisions count confirmed decisions
active_memory_entries count active non-expired memory entries
open_operating_gaps count detected or accepted unresolved gaps
active_integrations count active integrations
```

Health indicators may be derived from:

```text
overdue task ratio
open gap severity
missing ownership indicators
recent failed runtime events
integration sync failures
```

Rule:

```text
Dashboard values should be explainable and traceable to source records.
```

---

# 9. List Dashboard Metrics Flow

## Service Method

```text
DashboardMetricService.listMetrics(context, filters, pagination)
```

Supported filters:

```text
metric_type
category
period_start
period_end
```

Flow:

```text
validate authenticated actor
check workspace access
validate filters
call DashboardMetricRepository.listByWorkspace
return paginated metric DTOs
```

Default sort:

```text
computed_at:desc
```

---

# 10. Refresh Dashboard Metrics Flow

## Service Method

```text
DashboardRefreshService.requestRefresh(context, input)
```

Input:

```text
refresh_scope
idempotency_key optional
```

Flow:

```text
validate authenticated actor
load workspace
check workspace is active
check refresh permission
validate refresh_scope
check idempotency if key supplied
begin transaction
record dashboard_metrics.refresh_requested audit event
emit dashboard.refresh_requested runtime event
commit transaction
return accepted refresh DTO
```

## Internal Processing

```text
DashboardRefreshService.processRefresh(internal_context, event_id)
```

Flow:

```text
load runtime event
compute requested metrics
persist dashboard_metrics records
mark runtime event processed
```

---

# 11. Dashboard Activity Flow

## Service Method

```text
DashboardActivityService.listActivity(context, filters, pagination)
```

Supported filters:

```text
from_timestamp
to_timestamp
actor_id
object_type
page_size
page_token
```

Flow:

```text
validate authenticated actor
check activity view permission
validate filters
read audit events as primary activity source
optionally merge safe runtime events
map records to activity DTOs
return paginated activity list
```

Rule:

```text
Dashboard activity should prefer audit events for business activity and avoid exposing restricted runtime details by default.
```

---

# 12. Create Export Job Flow

## Service Method

```text
ExportService.createExportJob(context, input)
```

## Input

```text
export_type
format
export_scope
idempotency_key optional
```

## Flow

```text
validate authenticated actor
load workspace
check workspace is active
check export permission
validate export_type
validate format
validate export_scope
check idempotency if key supplied
begin transaction
create export_job with queued status
record export.requested audit event
emit export.requested runtime event
emit export.queued runtime event
commit transaction
enqueue export generation job if JobQueueModule is available
return export job DTO
```

---

# 13. Export Validation Rules

Validation rules:

```text
export_type must be valid
format must be supported
export_scope must be valid for export_type
caller must have permission for included data categories
workspace must be active for export creation
idempotency key must not conflict with different payload
```

Supported MVP export types:

```text
workspace_summary
```

Supported MVP formats:

```text
pdf
json
```

Error mappings:

```text
invalid export_type → invalid_export_type
invalid format → invalid_export_format
invalid scope → validation_error
forbidden scope → forbidden
idempotency conflict → idempotency_conflict
```

---

# 14. List and Get Export Job Flow

## List Method

```text
ExportJobService.listExportJobs(context, filters, pagination)
```

Supported filters:

```text
status
export_type
format
requested_by
from_timestamp
to_timestamp
```

Flow:

```text
validate authenticated actor
check export job read permission
validate filters
call ExportJobRepository.listByWorkspace
return paginated export job DTOs
```

## Get Method

```text
ExportJobService.getExportJob(context, export_job_id)
```

Flow:

```text
validate authenticated actor
check export job read permission
load export job by id and workspace_id
return export job DTO
```

---

# 15. Cancel Export Job Flow

## Service Method

```text
ExportJobService.cancelExportJob(context, export_job_id, input)
```

Input:

```text
cancel_reason optional
```

Flow:

```text
validate authenticated actor
load workspace
check cancel export permission
load export job by id and workspace_id
validate status allows cancellation
capture before_state
begin transaction
set status cancelled
record export.cancelled audit event
emit export.cancelled runtime event
commit transaction
return export job DTO
```

Allowed cancellation statuses:

```text
queued
processing
```

---

# 16. Execute Export Generation Flow

## Internal Service Method

```text
ExportGenerationService.executeExport(internal_context, export_job_id)
```

Flow:

```text
load export job by id and workspace_id
validate job status is queued or retryable
mark export job processing
collect source data according to export_scope
render export content in requested format
store file in secure file storage
create export_file record
mark export job completed
record export.completed audit event optional
emit export.completed runtime event
```

Failure flow:

```text
capture sanitized error
mark export job failed
record export.failed audit event optional
emit export.failed runtime event
```

Rule:

```text
Export generation must preserve workspace scope and must not include data outside the authorized export_scope.
```

---

# 17. Export Data Collection Rules

Export data may include:

```text
workspace summary
operating map summary
functions
responsibilities
tasks
decisions
memory summaries
audit summary
```

Rules:

```text
include only requested and authorized sections
avoid raw runtime event payloads by default
avoid raw secrets always
redact sensitive integration configuration when needed
preserve source timestamps and identifiers when useful
```

---

# 18. Download Export Link Flow

## Service Method

```text
ExportFileService.createDownloadLink(context, export_job_id)
```

Flow:

```text
validate authenticated actor
check export download permission
load export job by id and workspace_id
validate export job status is completed
load export file
validate file is not expired
create temporary signed URL or access reference
record export.download_link_created audit event
return download link DTO
```

Rule:

```text
Download links must be temporary and scoped to authorized users.
```

---

# 19. Authorization Rules

Dashboard and export authorization matrix:

| Operation | MVP Rule | Expansion Rule |
|---|---|---|
| View dashboard | workspace owner | active workspace access |
| View metrics | workspace owner | active workspace access |
| Refresh metrics | workspace owner | owner/admin/manager |
| View activity | workspace owner | owner/admin/manager/auditor |
| List export jobs | workspace owner | owner/admin/export manager |
| Create export job | workspace owner | owner/admin/export manager |
| Cancel export job | workspace owner | owner/admin/export manager |
| Download export | workspace owner | owner/admin/export manager/auditor depending scope |
| Execute export | internal service | internal service only |

---

# 20. Audit Events

Services should emit:

```text
dashboard_metrics.refresh_requested
export.requested
export.cancelled
export.download_link_created
export.completed optional internal
export.failed optional internal
```

Audit payload rules:

```text
include workspace_id
include actor_id and actor_type
include export_type and format where relevant
include object reference
include correlation_id
exclude raw secrets
exclude raw signed URL values from audit payload when possible
```

---

# 21. Runtime Events

Services should emit:

```text
dashboard.refresh_requested
export.requested
export.queued
export.cancelled
export.completed
export.failed
```

Runtime events may trigger:

```text
metric recomputation
export generation worker
notification later
retention cleanup later
observability later
```

---

# 22. DTOs

Dashboard Summary DTO:

```json
{
  "workspace_id": "uuid",
  "generated_at": "2026-07-01T12:00:00Z",
  "operating_status": "active",
  "summary": {
    "open_tasks": 12,
    "overdue_tasks": 2,
    "completed_tasks_30d": 18,
    "confirmed_decisions": 8,
    "active_memory_entries": 20,
    "open_operating_gaps": 3,
    "active_integrations": 1
  },
  "health": {
    "overall_score": 72,
    "risk_level": "medium",
    "attention_required": true
  }
}
```

Export Job DTO:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "export_type": "workspace_summary",
  "format": "pdf",
  "status": "queued",
  "requested_by": "uuid",
  "export_scope": {
    "include_tasks": true,
    "include_decisions": true,
    "include_memory": true
  },
  "created_at": "2026-07-01T12:00:00Z"
}
```

Download Link DTO:

```json
{
  "export_job_id": "uuid",
  "status": "available",
  "download_url": "temporary-signed-url",
  "expires_at": "2026-07-01T13:00:00Z"
}
```

---

# 23. Error Mapping

Dashboard and export service errors:

```text
Unauthenticated → unauthenticated
WorkspaceNotFound → not_found
WorkspaceArchived → workspace_archived
DashboardAccessDenied → forbidden
MetricNotFound → not_found
ExportJobNotFound → not_found
ExportFileNotFound → not_found
InvalidMetricType → invalid_metric_type
InvalidExportType → invalid_export_type
InvalidExportFormat → invalid_export_format
ExportNotReady → export_not_ready
ExportExpired → export_expired
ExportAlreadyCancelled → export_already_cancelled
RefreshAlreadyQueued → refresh_already_queued
IdempotencyConflict → idempotency_conflict
```

---

# 24. Performance and Caching Rules

Dashboard rules:

```text
small workspace dashboard may be computed dynamically
high-frequency metrics may be persisted
expensive metrics should be refreshed asynchronously
activity should be paginated
queries should use workspace-aware indexes
```

Export rules:

```text
non-trivial exports should be asynchronous
large exports should stream or generate in background
export files should expire by default
export generation should avoid loading unbounded data into memory
```

---

# 25. Retention and Expiration Rules

Dashboard retention:

```text
current summary may be dynamic
persisted metrics may be retained for recent history
snapshots should be retained only when needed for reports or audit history
```

Export retention:

```text
export job metadata should remain as workspace history
export files should expire by default
sensitive exports should have shorter retention
expired files should not remove export job metadata
```

---

# 26. MVP Simplifications

MVP may simplify by:

```text
dynamic dashboard summary computation
basic dashboard metrics only
no custom dashboard widgets
no dashboard snapshots
no scheduled reports
workspace_summary export only
PDF and JSON export formats only
simple file storage reference
manual export creation only
owner-only authorization
```

MVP must preserve:

```text
workspace scope
export authorization
audit event for export request and download link creation
runtime event for export generation
temporary download links
export file expiration
structured error mapping
```

---

# 27. Future Expansion

Future service expansion may add:

```text
dashboard alerts
dashboard insights
dashboard snapshots
custom dashboard widgets
saved dashboard views
scheduled reports
export templates
bulk exports
audit exports
compliance packages
report subscriptions
advanced health scoring
predictive operating risk indicators
```

---

# 28. Testing Expectations

Service tests should cover:

```text
dashboard summary computes core counts correctly
dashboard summary excludes archived records
metric refresh emits runtime event
activity uses audit events as primary source
create export validates export_type and format
create export validates export_scope permission
create export creates queued job and emits events
cancel export rejects completed jobs
download link rejects incomplete export
download link rejects expired file
export generation preserves workspace scope
export generation excludes raw secrets
workspace archived blocks export creation
```

Repository tests should cover:

```text
list metrics by workspace and filters
find latest metric by type
list export jobs by workspace and filters
find export job by id and workspace
mark export job completed
find export file by export job
list expired files
pagination and sorting behavior
```

---

# 29. Acceptance Criteria

Dashboard Export Service Design is accepted when:

- DashboardService responsibilities are defined;
- DashboardMetricService responsibilities are defined;
- DashboardActivityService responsibilities are defined;
- ExportService responsibilities are defined;
- ExportJobService responsibilities are defined;
- ExportGenerationService responsibilities are defined;
- ExportFileService responsibilities are defined;
- repository methods are identified;
- dashboard summary, metric refresh and activity flows are documented;
- export creation, generation, cancellation and download flows are documented;
- authorization matrix is defined;
- audit and runtime event expectations are defined;
- DTOs, error mappings, performance and retention rules are documented;
- MVP simplifications and testing expectations are documented.

Status:

```text
Accepted for Authorization Validation Services
```

---

# 30. Final Statement

```text
Bizzi Dashboard Export Service Design defines how backend services transform workspace operating data into actionable visibility and governed portable business evidence.
```

This service layer makes Bizzi observable, reportable and export-ready while preserving workspace scope, security and auditability.