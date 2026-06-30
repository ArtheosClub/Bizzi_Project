# 04_OPERATING_MAP_API.md

# Bizzi Platform

## Operating Map API

**Layer:** 28_API_CONTRACTS  
**Component Type:** API Contract Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 05_PROCESS_RUNTIME.md  
**Domain Reference:** 26_DOMAIN_MODEL / 03_OPERATING_MAP_DOMAIN.md  
**Data Model Reference:** 27_DATA_MODEL / 05_OPERATING_MAP_DATA_MODEL.md  
**Previous Document:** 03_WORKSPACE_API.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Operating Map API contract for Bizzi Platform.

The Operating Map API exposes operations for generating, reading, confirming and archiving a workspace operating map, as well as reviewing and resolving operating gaps and recommendations.

Core question:

```text
How should Bizzi expose the operating structure of a workspace as stable, reviewable, auditable and AI-safe API resources?
```

---

# 2. API Scope

This document covers:

```text
operating-maps
operating-gaps
operating-recommendations
```

Primary data model references:

```text
operating_maps
operating_gaps
operating_recommendations
```

MVP scope:

```text
operating-maps
operating-gaps
```

Near-MVP / P2 scope:

```text
operating-recommendations
```

---

# 3. Design Principles Applied

The Operating Map API follows:

```text
Workspace First
Resource-Oriented Contracts
Explicit State Transitions
Audit-Aware Mutations
Runtime Event Awareness
AI-Safe by Default
Safe Defaults
OpenAPI Readiness
```

---

# 4. Base Paths

Workspace-scoped paths:

```text
/api/v1/workspaces/{workspace_id}/operating-maps
/api/v1/workspaces/{workspace_id}/operating-gaps
/api/v1/workspaces/{workspace_id}/operating-recommendations
```

Rule:

```text
All operating map resources are workspace-scoped.
```

---

# 5. Resource: Operating Maps

## Resource Name

```text
operating-maps
```

## Purpose

Represent a generated or confirmed map of the workspace operating structure.

## Data Model Reference

```text
operating_maps
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "version": 1,
  "status": "generated",
  "title": "Initial Operating Map",
  "summary": "High-level operating structure for the workspace",
  "generated_by_agent_id": "uuid",
  "confirmed_by": null,
  "confirmed_at": null,
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:15:00Z",
  "metadata": {}
}
```

---

# 6. Endpoint: List Operating Maps

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/operating-maps
```

## Purpose

List operating maps for a workspace.

## Query Parameters

```text
status optional
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
      "version": 1,
      "status": "active",
      "title": "Operating Map v1",
      "summary": "Confirmed operating map",
      "confirmed_by": "uuid",
      "confirmed_at": "2026-07-01T10:00:00Z",
      "created_at": "2026-07-01T09:00:00Z",
      "updated_at": "2026-07-01T10:00:00Z"
    }
  ],
  "next_page_token": null
}
```

## Authorization

```text
User must have access to workspace.
```

---

# 7. Endpoint: Generate Operating Map

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/operating-maps/generate
```

## Purpose

Generate a draft operating map from workspace context, onboarding answers, existing functions, responsibilities, tasks, decisions, memory or AI analysis.

## Request Body

```json
{
  "source_object_type": "user_input",
  "source_object_id": "uuid",
  "generation_mode": "initial",
  "include_recommendations": true
}
```

## Required Fields

```text
none for MVP
```

## Optional Fields

```text
source_object_type
source_object_id
generation_mode
include_recommendations
```

## Response: 202 Accepted

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "version": 1,
  "status": "generated",
  "title": "Generated Operating Map",
  "summary": "Generated from workspace context",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

## Validation Rules

```text
generation_mode must be valid if provided
source_object_type must be valid if provided
source_object_id must exist if provided
source object must belong to same workspace if workspace-scoped
```

## Authorization

```text
Workspace owner or authorized user.
```

## Audit Events

```text
operating_map.generated
```

## Runtime Events

```text
operating_map.generated
operating_gaps.detected
operating_recommendations.created optional
```

---

# 8. Endpoint: Get Operating Map

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/operating-maps/{operating_map_id}
```

## Purpose

Retrieve a single operating map.

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "version": 1,
  "status": "active",
  "title": "Operating Map v1",
  "summary": "Confirmed operating map",
  "confirmed_by": "uuid",
  "confirmed_at": "2026-07-01T10:00:00Z",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T10:00:00Z",
  "metadata": {}
}
```

## Authorization

```text
User must have access to workspace.
```

---

# 9. Endpoint: Confirm Operating Map

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/operating-maps/{operating_map_id}/confirm
```

## Purpose

Confirm a generated operating map as the accepted workspace operating structure.

## Request Body

```json
{
  "confirmation_note": "Confirmed as initial operating map"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "version": 1,
  "status": "active",
  "confirmed_by": "uuid",
  "confirmed_at": "2026-07-01T10:00:00Z",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

## Validation Rules

```text
operating map must belong to workspace
operating map must be in generated, reviewed or confirmed-compatible status
archived operating maps cannot be confirmed
```

## Authorization

```text
Workspace owner or authorized admin.
```

## Audit Events

```text
operating_map.confirmed
```

## Runtime Events

```text
operating_map.confirmed
dashboard.refresh_requested
```

---

# 10. Endpoint: Archive Operating Map

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/operating-maps/{operating_map_id}/archive
```

## Purpose

Archive an operating map while preserving history.

## Request Body

```json
{
  "archive_reason": "Superseded by newer operating map"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "archived",
  "archived_at": "2026-07-01T12:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

## Authorization

```text
Workspace owner or authorized admin.
```

## Audit Events

```text
operating_map.archived
```

## Runtime Events

```text
operating_map.archived
```

---

# 11. Resource: Operating Gaps

## Resource Name

```text
operating-gaps
```

## Purpose

Represent missing functions, missing owners, missing processes, missing tasks or operational risks detected in the workspace operating structure.

## Data Model Reference

```text
operating_gaps
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "operating_map_id": "uuid",
  "function_id": "uuid",
  "gap_type": "missing_owner",
  "title": "Missing owner for finance function",
  "description": "Finance function has no accountable owner assigned",
  "severity": "high",
  "status": "detected",
  "source_object_type": "operating_map",
  "source_object_id": "uuid",
  "resolved_by_object_type": null,
  "resolved_by_object_id": null,
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

---

# 12. Endpoint: List Operating Gaps

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/operating-gaps
```

## Query Parameters

```text
status optional
gap_type optional
severity optional
operating_map_id optional
function_id optional
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
      "operating_map_id": "uuid",
      "gap_type": "missing_owner",
      "title": "Missing owner for finance function",
      "severity": "high",
      "status": "detected",
      "created_at": "2026-07-01T09:00:00Z",
      "updated_at": "2026-07-01T09:00:00Z"
    }
  ],
  "next_page_token": null
}
```

## Authorization

```text
User must have access to workspace.
```

---

# 13. Endpoint: Get Operating Gap

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/operating-gaps/{operating_gap_id}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "operating_map_id": "uuid",
  "function_id": "uuid",
  "gap_type": "missing_owner",
  "title": "Missing owner for finance function",
  "description": "Finance function has no accountable owner assigned",
  "severity": "high",
  "status": "detected",
  "source_object_type": "operating_map",
  "source_object_id": "uuid",
  "resolved_by_object_type": null,
  "resolved_by_object_id": null,
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

---

# 14. Endpoint: Accept Operating Gap

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/operating-gaps/{operating_gap_id}/accept
```

## Purpose

Accept that a detected operating gap is valid and should be addressed.

## Request Body

```json
{
  "acceptance_note": "Confirmed during owner review"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "accepted",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

## Validation Rules

```text
gap must belong to workspace
gap must not be resolved or archived
```

## Audit Events

```text
operating_gap.accepted
```

## Runtime Events

```text
operating_gap.accepted
```

---

# 15. Endpoint: Resolve Operating Gap

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/operating-gaps/{operating_gap_id}/resolve
```

## Purpose

Mark a gap as resolved by linking it to the object that resolved it.

## Request Body

```json
{
  "resolved_by_object_type": "responsibility",
  "resolved_by_object_id": "uuid",
  "resolution_note": "Owner assigned to finance function"
}
```

## Required Fields

```text
resolved_by_object_type
resolved_by_object_id
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "resolved",
  "resolved_by_object_type": "responsibility",
  "resolved_by_object_id": "uuid",
  "resolved_at": "2026-07-01T11:00:00Z",
  "updated_at": "2026-07-01T11:00:00Z"
}
```

## Validation Rules

```text
gap must belong to workspace
resolved_by_object_type must be valid
resolved_by_object_id must exist
resolved object must belong to same workspace if workspace-scoped
gap must not already be resolved or archived
```

## Audit Events

```text
operating_gap.resolved
```

## Runtime Events

```text
operating_gap.resolved
dashboard.refresh_requested
memory.candidate_created optional
```

---

# 16. Endpoint: Archive Operating Gap

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/operating-gaps/{operating_gap_id}/archive
```

## Purpose

Archive an operating gap that is no longer relevant.

## Request Body

```json
{
  "archive_reason": "No longer relevant after operating map update"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "archived",
  "archived_at": "2026-07-01T12:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

## Audit Events

```text
operating_gap.archived
```

## Runtime Events

```text
operating_gap.archived
```

---

# 17. Resource: Operating Recommendations

## Resource Name

```text
operating-recommendations
```

## Purpose

Represent suggested actions derived from operating map analysis and operating gaps.

## MVP Status

```text
P2 / Near-MVP
```

## Data Model Reference

```text
operating_recommendations
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "operating_map_id": "uuid",
  "source_gap_id": "uuid",
  "recommendation_type": "assign_owner",
  "title": "Assign owner for finance function",
  "description": "Finance function should have a named accountable owner",
  "status": "created",
  "confidence": "ai_suggested",
  "result_object_type": null,
  "result_object_id": null,
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

---

# 18. Endpoint: List Operating Recommendations

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/operating-recommendations
```

## Query Parameters

```text
status optional
recommendation_type optional
operating_map_id optional
source_gap_id optional
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
      "recommendation_type": "assign_owner",
      "title": "Assign owner for finance function",
      "status": "created",
      "confidence": "ai_suggested",
      "created_at": "2026-07-01T09:00:00Z"
    }
  ],
  "next_page_token": null
}
```

---

# 19. Endpoint: Confirm Operating Recommendation

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/operating-recommendations/{recommendation_id}/confirm
```

## Purpose

Confirm that a recommendation is valid and ready for application.

## Request Body

```json
{
  "confirmation_note": "Recommendation accepted by owner"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "confirmed",
  "confirmed_by": "uuid",
  "confirmed_at": "2026-07-01T10:00:00Z",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

## Audit Events

```text
operating_recommendation.confirmed
```

## Runtime Events

```text
operating_recommendation.confirmed
```

---

# 20. Endpoint: Apply Operating Recommendation

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/operating-recommendations/{recommendation_id}/apply
```

## Purpose

Apply a confirmed recommendation and create or update the resulting object.

## Request Body

```json
{
  "application_note": "Create responsibility assignment for finance function"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "applied",
  "result_object_type": "responsibility",
  "result_object_id": "uuid",
  "updated_at": "2026-07-01T11:00:00Z"
}
```

## Validation Rules

```text
recommendation must belong to workspace
recommendation must be confirmed or application-compatible
recommendation must not already be applied or rejected
application must respect user authorization
result object must be traceable
```

## Audit Events

```text
operating_recommendation.applied
```

## Runtime Events

```text
operating_recommendation.applied
```

---

# 21. Endpoint: Reject Operating Recommendation

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/operating-recommendations/{recommendation_id}/reject
```

## Request Body

```json
{
  "rejection_reason": "Not relevant for this company"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "rejected",
  "updated_at": "2026-07-01T11:00:00Z"
}
```

## Audit Events

```text
operating_recommendation.rejected
```

## Runtime Events

```text
operating_recommendation.rejected
```

---

# 22. Common Error Codes

Operating Map API may return:

```text
unauthenticated
forbidden
not_found
validation_error
conflict
workspace_archived
invalid_status_transition
invalid_source_object
invalid_resolution_object
```

Example:

```json
{
  "error": {
    "code": "invalid_status_transition",
    "message": "Resolved operating gaps cannot be accepted again.",
    "correlation_id": "uuid"
  }
}
```

---

# 23. Authorization Matrix

| Operation | MVP Rule | Expansion Rule |
|---|---|---|
| List maps | workspace owner | active workspace access |
| Generate map | workspace owner | owner/admin/manager |
| Confirm map | workspace owner | owner/admin |
| Archive map | workspace owner | owner/admin |
| List gaps | workspace owner | active workspace access |
| Accept gap | workspace owner | owner/admin/manager |
| Resolve gap | workspace owner | owner/admin/manager |
| Manage recommendations | workspace owner | owner/admin/manager |

---

# 24. Audit and Runtime Event Summary

| API Operation | Audit Event | Runtime Event |
|---|---|---|
| Generate map | operating_map.generated | operating_map.generated |
| Confirm map | operating_map.confirmed | operating_map.confirmed |
| Archive map | operating_map.archived | operating_map.archived |
| Accept gap | operating_gap.accepted | operating_gap.accepted |
| Resolve gap | operating_gap.resolved | operating_gap.resolved |
| Archive gap | operating_gap.archived | operating_gap.archived |
| Confirm recommendation | operating_recommendation.confirmed | operating_recommendation.confirmed |
| Apply recommendation | operating_recommendation.applied | operating_recommendation.applied |
| Reject recommendation | operating_recommendation.rejected | operating_recommendation.rejected |

---

# 25. MVP Simplifications

For MVP, Bizzi may simplify by:

- generating one initial operating map per workspace;
- using operating gaps without full operating recommendations;
- using simple generated → active → archived lifecycle;
- representing ownership gaps as operating gaps;
- computing some map details dynamically;
- requiring workspace owner confirmation for AI-generated maps.

These simplifications must preserve traceability, workspace scope and auditability.

---

# 26. Future Expansion

Future Operating Map API may add:

```text
operating-map-nodes
operating-map-versions
operating-map-comparisons
bulk gap resolution
map quality scoring
map review workflow
operating health score
map export
collaborative review comments
```

---

# 27. Acceptance Criteria

Operating Map API is accepted when:

- operating map endpoints are defined;
- operating gap endpoints are defined;
- operating recommendation expansion endpoints are defined;
- request and response shapes are documented;
- validation rules are identified;
- authorization rules are defined;
- audit and runtime event expectations are defined;
- MVP simplifications are documented;
- AI-generated map confirmation is explicit.

Status:

```text
Accepted for Function Responsibility API Design
```

---

# 28. Final Statement

```text
Bizzi Operating Map API defines how the platform generates, reviews, confirms and improves the operating structure of a workspace through workspace-scoped, auditable and AI-safe API contracts.
```

This API turns workspace context into an actionable operating structure.