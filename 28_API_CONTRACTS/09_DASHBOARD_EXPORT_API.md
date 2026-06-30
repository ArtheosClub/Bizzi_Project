# 09_DASHBOARD_EXPORT_API.md

# Bizzi Platform

## Dashboard Export API

**Layer:** 28_API_CONTRACTS  
**Component Type:** API Contract Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 13_RUNTIME_MILESTONE.md, 14_RUNTIME_PLATFORM_AUDIT.md  
**Domain Reference:** 26_DOMAIN_MODEL / 12_DASHBOARD_AND_EXPORT_DOMAIN.md  
**Data Model Reference:** 27_DATA_MODEL / 10_DASHBOARD_EXPORT_DATA_MODEL.md  
**Previous Document:** 08_INTEGRATION_SECURITY_API.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Dashboard and Export API contracts for Bizzi Platform.

These APIs expose workspace operating visibility, dashboard metrics, activity summaries, alerts and governed export jobs.

Core question:

```text
How should Bizzi expose operational visibility and exportable business evidence through stable, workspace-scoped, auditable and implementation-ready API contracts?
```

---

# 2. API Scope

This document covers:

```text
dashboard
dashboard-metrics
dashboard-activity
export-jobs
```

Primary data model references:

```text
dashboard_metrics
dashboard_snapshots
dashboard_insights
dashboard_alerts
export_jobs
export_files
```

MVP scope:

```text
dashboard
dashboard-metrics
export-jobs
```

Expansion scope:

```text
dashboard-alerts
dashboard-insights
dashboard-snapshots
export-files
export-templates
scheduled-reports
```

---

# 3. Design Principles Applied

This API follows:

```text
Workspace First
Resource-Oriented Contracts
Safe Defaults
Audit-Aware Mutations
Runtime Event Awareness
Least Privilege Authorization
Pagination for Lists
OpenAPI Readiness
```

---

# 4. Base Paths

Workspace-scoped paths:

```text
/api/v1/workspaces/{workspace_id}/dashboard
/api/v1/workspaces/{workspace_id}/dashboard/metrics
/api/v1/workspaces/{workspace_id}/dashboard/activity
/api/v1/workspaces/{workspace_id}/export-jobs
```

Rule:

```text
Dashboard and export resources are workspace-scoped.
```

---

# 5. Resource: Dashboard Summary

## Resource Name

```text
dashboard
```

## Purpose

Expose a compact summary of workspace operating health and current activity.

## Response Shape

```json
{
  "workspace_id": "uuid",
  "generated_at": "2026-07-01T12:00:00Z",
  "operating_status": "active",
  "summary": {
    "open_tasks": 12,
    "overdue_tasks": 2,
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

---

# 6. Endpoint: Get Dashboard Summary

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/dashboard
```

## Query Parameters

```text
include_activity optional
include_alerts optional
include_insights optional
```

## Response: 200 OK

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
  },
  "recent_activity": [],
  "alerts": [],
  "insights": []
}
```

## Authorization

```text
User must have access to workspace.
```

## Runtime Events

```text
dashboard.viewed optional
```

---

# 7. Resource: Dashboard Metrics

## Resource Name

```text
dashboard-metrics
```

## Purpose

Expose current and historical dashboard metrics.

## Data Model Reference

```text
dashboard_metrics
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "metric_type": "open_tasks",
  "category": "execution",
  "value": 12,
  "unit": "count",
  "period_start": "2026-07-01T00:00:00Z",
  "period_end": "2026-07-01T23:59:59Z",
  "computed_at": "2026-07-01T12:00:00Z",
  "source_object_type": null,
  "source_object_id": null
}
```

---

# 8. Endpoint: List Dashboard Metrics

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/dashboard/metrics
```

## Query Parameters

```text
metric_type optional
category optional
period_start optional
period_end optional
page_size optional
page_token optional
sort optional
```

## Response: 200 OK

```json
{
  "items": [
    {
      "id": "uuid",
      "workspace_id": "uuid",
      "metric_type": "open_tasks",
      "category": "execution",
      "value": 12,
      "unit": "count",
      "computed_at": "2026-07-01T12:00:00Z"
    }
  ],
  "next_page_token": null
}
```

---

# 9. Endpoint: Refresh Dashboard Metrics

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/dashboard/metrics/refresh
```

## Purpose

Request recomputation of dashboard metrics.

## Request Body

```json
{
  "refresh_scope": "workspace_summary",
  "idempotency_key": "client-generated-key"
}
```

## Response: 202 Accepted

```json
{
  "workspace_id": "uuid",
  "status": "queued",
  "refresh_scope": "workspace_summary",
  "requested_at": "2026-07-01T12:00:00Z"
}
```

## Audit Events

```text
dashboard_metrics.refresh_requested
```

## Runtime Events

```text
dashboard.refresh_requested
```

---

# 10. Resource: Dashboard Activity

## Resource Name

```text
dashboard-activity
```

## Purpose

Expose recent workspace activity derived from audit events, runtime events, tasks, decisions and memory changes.

## Endpoint

```text
GET /api/v1/workspaces/{workspace_id}/dashboard/activity
```

## Query Parameters

```text
from_timestamp optional
to_timestamp optional
actor_id optional
object_type optional
page_size optional
page_token optional
```

## Response: 200 OK

```json
{
  "items": [
    {
      "activity_type": "task.completed",
      "title": "Task completed",
      "object_type": "task",
      "object_id": "uuid",
      "actor_id": "uuid",
      "timestamp": "2026-07-01T12:00:00Z"
    }
  ],
  "next_page_token": null
}
```

---

# 11. Resource: Export Jobs

## Resource Name

```text
export-jobs
```

## Purpose

Represent export requests and their lifecycle.

## Data Model Reference

```text
export_jobs
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "export_type": "workspace_summary",
  "format": "pdf",
  "status": "completed",
  "requested_by": "uuid",
  "export_scope": {
    "include_tasks": true,
    "include_decisions": true,
    "include_memory": true
  },
  "file_reference": "file_ref",
  "expires_at": "2026-07-08T12:00:00Z",
  "created_at": "2026-07-01T12:00:00Z",
  "completed_at": "2026-07-01T12:01:00Z"
}
```

---

# 12. Endpoint: List Export Jobs

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/export-jobs
```

## Query Parameters

```text
status optional
export_type optional
format optional
requested_by optional
from_timestamp optional
to_timestamp optional
page_size optional
page_token optional
sort optional
```

## Response: 200 OK

```json
{
  "items": [
    {
      "id": "uuid",
      "workspace_id": "uuid",
      "export_type": "workspace_summary",
      "format": "pdf",
      "status": "completed",
      "requested_by": "uuid",
      "created_at": "2026-07-01T12:00:00Z",
      "completed_at": "2026-07-01T12:01:00Z"
    }
  ],
  "next_page_token": null
}
```

## Authorization

```text
Workspace owner, admin or authorized user.
```

---

# 13. Endpoint: Create Export Job

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/export-jobs
```

## Request Body

```json
{
  "export_type": "workspace_summary",
  "format": "pdf",
  "export_scope": {
    "include_operating_map": true,
    "include_functions": true,
    "include_tasks": true,
    "include_decisions": true,
    "include_memory": true,
    "include_audit_summary": false
  },
  "idempotency_key": "client-generated-key"
}
```

## Required Fields

```text
export_type
format
```

## Response: 202 Accepted

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "export_type": "workspace_summary",
  "format": "pdf",
  "status": "queued",
  "requested_by": "uuid",
  "created_at": "2026-07-01T12:00:00Z"
}
```

## Validation Rules

```text
export_type must be valid
format must be supported
export_scope must be valid for export_type
caller must have export permission
workspace must be active
idempotency key should prevent duplicate export jobs when supplied
```

## Audit Events

```text
export.requested
```

## Runtime Events

```text
export.requested
export.queued
```

---

# 14. Endpoint: Get Export Job

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/export-jobs/{export_job_id}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "export_type": "workspace_summary",
  "format": "pdf",
  "status": "completed",
  "requested_by": "uuid",
  "export_scope": {
    "include_operating_map": true,
    "include_functions": true,
    "include_tasks": true,
    "include_decisions": true,
    "include_memory": true
  },
  "file_reference": "file_ref",
  "expires_at": "2026-07-08T12:00:00Z",
  "created_at": "2026-07-01T12:00:00Z",
  "completed_at": "2026-07-01T12:01:00Z"
}
```

---

# 15. Endpoint: Cancel Export Job

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/export-jobs/{export_job_id}/cancel
```

## Request Body

```json
{
  "cancel_reason": "Export no longer needed"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "cancelled",
  "updated_at": "2026-07-01T12:05:00Z"
}
```

## Audit Events

```text
export.cancelled
```

## Runtime Events

```text
export.cancelled
```

---

# 16. Endpoint: Get Export Download Link

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/export-jobs/{export_job_id}/download
```

## Purpose

Return a temporary download URL or file access reference for a completed export.

## Response: 200 OK

```json
{
  "export_job_id": "uuid",
  "status": "available",
  "download_url": "temporary-signed-url",
  "expires_at": "2026-07-01T13:00:00Z"
}
```

## Security Rules

```text
download URL must be temporary
caller must have export access
export job must belong to workspace
export job must be completed
expired files should not return downloadable links
```

## Audit Events

```text
export.download_link_created
```

---

# 17. Common Error Codes

Dashboard Export API may return:

```text
unauthenticated
forbidden
not_found
validation_error
conflict
workspace_archived
invalid_export_type
invalid_export_format
export_not_ready
export_expired
export_already_cancelled
invalid_metric_type
refresh_already_queued
```

Example:

```json
{
  "error": {
    "code": "export_not_ready",
    "message": "Export job has not completed yet.",
    "correlation_id": "uuid"
  }
}
```

---

# 18. Authorization Matrix

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

---

# 19. Audit and Runtime Event Summary

| API Operation | Audit Event | Runtime Event |
|---|---|---|
| Refresh dashboard metrics | dashboard_metrics.refresh_requested | dashboard.refresh_requested |
| Create export job | export.requested | export.requested |
| Cancel export job | export.cancelled | export.cancelled |
| Create download link | export.download_link_created | none |
| Export completed internally | export.completed | export.completed |
| Export failed internally | export.failed | export.failed |

---

# 20. Retention and Expiration Rules

Dashboard rules:

```text
current dashboard values may be dynamically computed
persisted metrics may be retained for recent history
snapshots should be retained only when used for reporting or audit history
```

Export rules:

```text
export job metadata should be retained with workspace history
export files should expire by default
sensitive exports should have shorter file retention
expired export files should not remove export job metadata
```

---

# 21. MVP Simplifications

For MVP, Bizzi may simplify by:

- computing dashboard summary dynamically;
- persisting only selected dashboard metrics;
- using simple export types such as workspace_summary;
- supporting PDF and JSON before advanced formats;
- using asynchronous export jobs for all non-trivial exports;
- returning temporary file references only after completion;
- omitting scheduled reports until later.

These simplifications must preserve workspace scope, export authorization and auditability.

---

# 22. Future Expansion

Future Dashboard Export API may add:

```text
dashboard-alerts
dashboard-insights
dashboard-snapshots
custom dashboard widgets
export-templates
export-files
scheduled-reports
report-subscriptions
bulk exports
audit exports
compliance export packages
```

---

# 23. Acceptance Criteria

Dashboard Export API is accepted when:

- dashboard summary endpoint is defined;
- dashboard metrics endpoints are defined;
- dashboard activity endpoint is defined;
- export job endpoints are defined;
- download link behavior is defined;
- request and response shapes are documented;
- validation rules are identified;
- authorization rules are defined;
- audit and runtime event expectations are defined;
- retention and expiration rules are documented;
- MVP simplifications are documented.

Status:

```text
Accepted for Error and Validation Contracts
```

---

# 24. Final Statement

```text
Bizzi Dashboard Export API defines how the platform exposes operating visibility, metrics, activity and governed exports through workspace-scoped, secure, auditable and implementation-ready API contracts.
```

This API turns Bizzi operating data into actionable visibility and portable business evidence.