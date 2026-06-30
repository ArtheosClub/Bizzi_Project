# 07_MEMORY_AUDIT_EVENT_API.md

# Bizzi Platform

## Memory Audit Event API

**Layer:** 28_API_CONTRACTS  
**Component Type:** API Contract Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 08_MEMORY_RUNTIME.md, 09_AUDIT_RUNTIME.md, 10_EVENT_RUNTIME.md  
**Domain Reference:** 26_DOMAIN_MODEL / 09_MEMORY_DOMAIN.md, 10_AUDIT_AND_EVENT_DOMAIN.md  
**Data Model Reference:** 27_DATA_MODEL / 08_MEMORY_AUDIT_EVENT_DATA_MODEL.md  
**Previous Document:** 06_AGENT_PROCESS_TASK_DECISION_API.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Memory, Audit and Event API contracts for Bizzi Platform.

These APIs expose the knowledge, evidence and runtime activity layer of Bizzi: reusable workspace memory, immutable audit evidence and controlled runtime event visibility.

Core question:

```text
How should Bizzi expose memory, audit and runtime events through stable, workspace-scoped, secure and AI-safe API contracts?
```

---

# 2. API Scope

This document covers:

```text
memory-entries
audit-events
runtime-events
```

Primary data model references:

```text
memory_entries
audit_events
runtime_events
```

MVP scope:

```text
memory-entries
audit-events read access
runtime-events restricted read access
```

Expansion scope:

```text
memory-sources
memory-usage
memory-reviews
audit-exports
event-failures
event-handler-runs
```

---

# 3. Design Principles Applied

This API follows:

```text
Workspace First
Resource-Oriented Contracts
Audit-Aware Mutations
Runtime Event Awareness
AI-Safe by Default
Least Privilege Authorization
Safe Defaults
Retention Awareness
OpenAPI Readiness
```

---

# 4. Base Paths

Workspace-scoped paths:

```text
/api/v1/workspaces/{workspace_id}/memory-entries
/api/v1/workspaces/{workspace_id}/audit-events
/api/v1/workspaces/{workspace_id}/runtime-events
```

Rule:

```text
Memory, audit and runtime event records are always workspace-scoped when they describe operating behavior.
```

---

# 5. Resource: Memory Entries

## Resource Name

```text
memory-entries
```

## Purpose

Represent reusable business knowledge available to the workspace and, when active, to AI context assembly.

## Data Model Reference

```text
memory_entries
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "memory_type": "decision_summary",
  "title": "Supplier approval rule",
  "summary": "Suppliers above a threshold require owner confirmation",
  "content": "Confirmed purchasing rule for supplier approvals.",
  "status": "active",
  "confidence": "confirmed",
  "source_object_type": "decision",
  "source_object_id": "uuid",
  "function_id": "uuid",
  "process_id": "uuid",
  "task_id": "uuid",
  "decision_id": "uuid",
  "agent_id": "uuid",
  "valid_from": "2026-07-01",
  "valid_until": null,
  "confirmed_by": "uuid",
  "confirmed_at": "2026-07-01T12:00:00Z",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z",
  "metadata": {}
}
```

---

# 6. Endpoint: List Memory Entries

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/memory-entries
```

## Query Parameters

```text
status optional
memory_type optional
confidence optional
source_object_type optional
source_object_id optional
function_id optional
process_id optional
task_id optional
decision_id optional
agent_id optional
valid_on optional
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
      "memory_type": "decision_summary",
      "title": "Supplier approval rule",
      "summary": "Suppliers above a threshold require owner confirmation",
      "status": "active",
      "confidence": "confirmed",
      "source_object_type": "decision",
      "source_object_id": "uuid",
      "created_at": "2026-07-01T09:00:00Z",
      "updated_at": "2026-07-01T12:00:00Z"
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

# 7. Endpoint: Create Memory Entry

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/memory-entries
```

## Purpose

Create a memory entry manually or from a confirmed source object.

## Request Body

```json
{
  "memory_type": "decision_summary",
  "title": "Supplier approval rule",
  "summary": "Suppliers above a threshold require owner confirmation",
  "content": "Confirmed purchasing rule for supplier approvals.",
  "source_object_type": "decision",
  "source_object_id": "uuid",
  "function_id": "uuid",
  "process_id": "uuid",
  "task_id": "uuid",
  "decision_id": "uuid",
  "valid_from": "2026-07-01",
  "valid_until": null
}
```

## Required Fields

```text
title
content or summary
memory_type
```

## Response: 201 Created

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "memory_type": "decision_summary",
  "title": "Supplier approval rule",
  "status": "candidate",
  "confidence": "user_provided",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

## Validation Rules

```text
memory_type must be valid
title is required
content or summary is required
source_object_type must be valid if provided
source_object_id must exist if provided
source object must belong to same workspace if workspace-scoped
valid_until must be after valid_from if both are provided
```

## Audit Events

```text
memory.created
```

## Runtime Events

```text
memory.created
dashboard.refresh_requested optional
```

---

# 8. Endpoint: Get Memory Entry

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "memory_type": "decision_summary",
  "title": "Supplier approval rule",
  "summary": "Suppliers above a threshold require owner confirmation",
  "content": "Confirmed purchasing rule for supplier approvals.",
  "status": "active",
  "confidence": "confirmed",
  "source_object_type": "decision",
  "source_object_id": "uuid",
  "valid_from": "2026-07-01",
  "valid_until": null,
  "confirmed_by": "uuid",
  "confirmed_at": "2026-07-01T12:00:00Z",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z",
  "metadata": {}
}
```

---

# 9. Endpoint: Update Memory Entry

## Method and Path

```text
PATCH /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}
```

## Request Body

```json
{
  "title": "Updated supplier approval rule",
  "summary": "Updated summary",
  "content": "Updated rule content",
  "valid_until": "2027-01-01"
}
```

## Mutable Fields

```text
title
summary
content
valid_from
valid_until
metadata
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "title": "Updated supplier approval rule",
  "status": "active",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

## Audit Events

```text
memory.updated
```

## Runtime Events

```text
memory.updated
```

---

# 10. Endpoint: Activate Memory Entry

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/activate
```

## Request Body

```json
{
  "confirmation_note": "Approved for active AI context"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "active",
  "confirmed_by": "uuid",
  "confirmed_at": "2026-07-01T11:00:00Z",
  "updated_at": "2026-07-01T11:00:00Z"
}
```

## Validation Rules

```text
memory entry must belong to workspace
memory entry must not be archived or rejected
expired memory cannot be activated without updating validity
AI-generated memory requires human confirmation unless automation authority allows it
```

## Audit Events

```text
memory.activated
```

## Runtime Events

```text
memory.activated
```

---

# 11. Endpoint: Archive Memory Entry

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/archive
```

## Request Body

```json
{
  "archive_reason": "Knowledge no longer current"
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

## Rule

```text
Archived memory must not be used as active AI context.
```

## Audit Events

```text
memory.archived
```

## Runtime Events

```text
memory.archived
```

---

# 12. Resource: Audit Events

## Resource Name

```text
audit-events
```

## Purpose

Expose authorized audit history for workspace objects and AI-assisted state changes.

## Data Model Reference

```text
audit_events
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "timestamp": "2026-07-01T12:00:00Z",
  "actor_type": "user",
  "actor_id": "uuid",
  "agent_id": null,
  "action": "decision.confirmed",
  "object_type": "decision",
  "object_id": "uuid",
  "source_event_id": "uuid",
  "ai_assisted": false,
  "human_confirmed": true,
  "severity": "info",
  "correlation_id": "uuid",
  "before_state": {},
  "after_state": {}
}
```

---

# 13. Endpoint: List Audit Events

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/audit-events
```

## Query Parameters

```text
action optional
actor_type optional
actor_id optional
agent_id optional
object_type optional
object_id optional
ai_assisted optional
human_confirmed optional
severity optional
from_timestamp optional
to_timestamp optional
correlation_id optional
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
      "timestamp": "2026-07-01T12:00:00Z",
      "actor_type": "user",
      "actor_id": "uuid",
      "action": "decision.confirmed",
      "object_type": "decision",
      "object_id": "uuid",
      "ai_assisted": false,
      "human_confirmed": true,
      "severity": "info",
      "correlation_id": "uuid"
    }
  ],
  "next_page_token": null
}
```

## Authorization

```text
Workspace owner or authorized auditor/admin.
```

## Rule

```text
Audit events are read-oriented and must not be modified through normal public API flows.
```

---

# 14. Endpoint: Get Audit Event

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/audit-events/{audit_event_id}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "timestamp": "2026-07-01T12:00:00Z",
  "actor_type": "user",
  "actor_id": "uuid",
  "agent_id": null,
  "action": "decision.confirmed",
  "object_type": "decision",
  "object_id": "uuid",
  "source_event_id": "uuid",
  "ai_assisted": false,
  "human_confirmed": true,
  "severity": "info",
  "correlation_id": "uuid",
  "before_state": {},
  "after_state": {},
  "created_at": "2026-07-01T12:00:00Z"
}
```

---

# 15. Resource: Runtime Events

## Resource Name

```text
runtime-events
```

## Purpose

Expose limited runtime event visibility for diagnostics, internal coordination and platform observability.

## Data Model Reference

```text
runtime_events
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "event_type": "task.completed",
  "status": "processed",
  "source_object_type": "task",
  "source_object_id": "uuid",
  "actor_type": "user",
  "actor_id": "uuid",
  "agent_id": null,
  "payload": {},
  "correlation_id": "uuid",
  "causation_id": "uuid",
  "timestamp": "2026-07-01T12:00:00Z",
  "processed_at": "2026-07-01T12:00:05Z"
}
```

---

# 16. Endpoint: List Runtime Events

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/runtime-events
```

## Query Parameters

```text
event_type optional
status optional
source_object_type optional
source_object_id optional
actor_type optional
actor_id optional
agent_id optional
correlation_id optional
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
      "event_type": "task.completed",
      "status": "processed",
      "source_object_type": "task",
      "source_object_id": "uuid",
      "correlation_id": "uuid",
      "timestamp": "2026-07-01T12:00:00Z",
      "processed_at": "2026-07-01T12:00:05Z"
    }
  ],
  "next_page_token": null
}
```

## Authorization

```text
Workspace owner, admin or internal service role.
```

## Rule

```text
Runtime events may expose operational details and should be restricted by default.
```

---

# 17. Endpoint: Get Runtime Event

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/runtime-events/{runtime_event_id}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "event_type": "task.completed",
  "status": "processed",
  "source_object_type": "task",
  "source_object_id": "uuid",
  "actor_type": "user",
  "actor_id": "uuid",
  "agent_id": null,
  "payload": {},
  "correlation_id": "uuid",
  "causation_id": "uuid",
  "timestamp": "2026-07-01T12:00:00Z",
  "processed_at": "2026-07-01T12:00:05Z"
}
```

---

# 18. Common Error Codes

Memory Audit Event API may return:

```text
unauthenticated
forbidden
not_found
validation_error
conflict
workspace_archived
invalid_status_transition
invalid_source_object
human_confirmation_required
audit_event_read_only
runtime_event_restricted
```

Example:

```json
{
  "error": {
    "code": "runtime_event_restricted",
    "message": "Runtime event access is restricted for this user.",
    "correlation_id": "uuid"
  }
}
```

---

# 19. Authorization Matrix

| Operation | MVP Rule | Expansion Rule |
|---|---|---|
| List memory | workspace owner | active workspace access |
| Create memory | workspace owner | owner/admin/manager |
| Update memory | workspace owner | owner/admin/manager |
| Activate memory | workspace owner | owner/admin with confirmation |
| Archive memory | workspace owner | owner/admin/manager |
| List audit events | workspace owner | owner/admin/auditor |
| Get audit event | workspace owner | owner/admin/auditor |
| List runtime events | workspace owner | owner/admin/internal service |
| Get runtime event | workspace owner | owner/admin/internal service |

---

# 20. Audit and Runtime Event Summary

| API Operation | Audit Event | Runtime Event |
|---|---|---|
| Create memory | memory.created | memory.created |
| Update memory | memory.updated | memory.updated |
| Activate memory | memory.activated | memory.activated |
| Archive memory | memory.archived | memory.archived |
| Read audit event | optional audit_event.read | none |
| Read runtime event | optional runtime_event.read | none |

---

# 21. Retention and Safety Rules

Memory retention rules:

```text
active memory may be used for AI context
candidate memory requires review before active use
archived memory must not be used as active AI context
expired memory must not be used as active AI context
```

Audit retention rules:

```text
audit events should be retained for workspace lifetime
audit events are append-oriented
audit events should not be hard-deleted through normal API flows
```

Runtime event retention rules:

```text
processed runtime events may expire after retention window
failed or critical events may be retained longer
runtime event payloads should avoid raw secrets
```

---

# 22. MVP Simplifications

For MVP, Bizzi may simplify by:

- supporting one memory entry resource before memory sources and reviews;
- using audit events as the canonical change history;
- exposing audit and runtime events as read-only administrative views;
- omitting full event handler diagnostics;
- storing memory confidence as a simple controlled text value;
- requiring human confirmation before AI-generated memory becomes active.

These simplifications must preserve workspace scope, traceability, auditability and AI safety.

---

# 23. Future Expansion

Future Memory Audit Event API may add:

```text
memory-sources
memory-usage
memory-reviews
memory-embeddings
audit-exports
audit-redaction-requests
event-failures
event-handler-runs
event-subscriptions
runtime-event-replay internal only
```

---

# 24. Acceptance Criteria

Memory Audit Event API is accepted when:

- memory endpoints are defined;
- audit event read contracts are defined;
- runtime event read contracts are defined;
- request and response shapes are documented;
- validation rules are identified;
- authorization rules are defined;
- audit and runtime event expectations are defined;
- retention and AI safety rules are documented;
- MVP simplifications are documented.

Status:

```text
Accepted for Integration Security API Design
```

---

# 25. Final Statement

```text
Bizzi Memory Audit Event API defines how the platform exposes workspace knowledge, evidence and runtime activity through secure, traceable, auditable and AI-safe API contracts.
```

This API makes Bizzi explainable, governable and capable of preserving enterprise memory.