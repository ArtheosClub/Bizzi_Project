# 01_API_DESIGN_PRINCIPLES.md

# Bizzi Platform

## API Design Principles

**Layer:** 28_API_CONTRACTS  
**Component Type:** API Architecture Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**Previous Document:** 00_API_CONTRACTS_VISION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the core API design principles for Bizzi Platform.

It establishes the rules that all Bizzi API contracts must follow so that the platform remains workspace-scoped, secure, predictable, auditable, AI-safe and implementation-ready.

Core question:

```text
Which API design principles should guide every Bizzi endpoint, request, response, error and state transition?
```

---

# 2. API Design Role

API design principles ensure that Bizzi APIs are not a random collection of endpoints.

They provide consistency for:

- frontend implementation;
- backend service design;
- AI agent orchestration;
- integrations;
- dashboard queries;
- export generation;
- audit and runtime event emission;
- future OpenAPI specification;
- long-term versioning.

---

# 3. Principle P01 — Workspace First

All operating API resources must be scoped to a workspace.

Canonical path pattern:

```text
/api/v1/workspaces/{workspace_id}/...
```

Examples:

```text
/api/v1/workspaces/{workspace_id}/tasks
/api/v1/workspaces/{workspace_id}/decisions
/api/v1/workspaces/{workspace_id}/memory-entries
/api/v1/workspaces/{workspace_id}/dashboard
```

Exceptions:

```text
/api/v1/me
/api/v1/workspaces
/api/v1/auth-related endpoints later
```

Rule:

```text
No workspace scope, no operating API action.
```

---

# 4. Principle P02 — Resource-Oriented Contracts

API endpoints should be organized around stable Bizzi resources.

Resource examples:

```text
workspaces
operating-maps
operating-gaps
functions
responsibilities
agents
processes
tasks
decisions
memory-entries
audit-events
runtime-events
integrations
security-policies
dashboard-metrics
export-jobs
```

Rule:

```text
API resources should map back to Domain Model entities and Data Model tables.
```

---

# 5. Principle P03 — Stable Field Names

API fields should use stable internal field names, aligned with `27_DATA_MODEL`.

Preferred style:

```text
snake_case
```

Examples:

```text
workspace_id
owner_user_id
source_object_type
source_object_id
created_at
updated_at
confirmed_by
confirmed_at
```

Rule:

```text
Do not expose temporary UI labels as canonical API fields.
```

---

# 6. Principle P04 — Explicit State Transitions

Important business transitions should be represented by explicit endpoint actions.

Examples:

```text
POST /tasks/{task_id}/complete
POST /decisions/{decision_id}/confirm
POST /agent-recommendations/{recommendation_id}/apply
POST /agent-recommendations/{recommendation_id}/reject
POST /export-jobs/{export_job_id}/cancel
```

Why:

```text
Explicit transitions are easier to validate, audit, authorize and explain.
```

Rule:

```text
Do not hide important lifecycle transitions inside generic PATCH when the transition has business meaning.
```

---

# 7. Principle P05 — Predictable CRUD Where Appropriate

Simple resources may use standard CRUD patterns.

Examples:

```text
GET /resources
POST /resources
GET /resources/{id}
PATCH /resources/{id}
DELETE /resources/{id}
```

However, DELETE should be used carefully.

For important business records, prefer:

```text
archive
revoke
cancel
expire
```

Rule:

```text
CRUD is acceptable for simple records, but governed business transitions need explicit operations.
```

---

# 8. Principle P06 — Consistent Request Shapes

Create and update requests should be minimal, explicit and validated.

Create request should include fields needed to create meaningful state.

Update request should include only fields being changed.

Example:

```json
{
  "title": "Prepare supplier review",
  "description": "Review risk, payment terms and owner responsibility",
  "owner_user_id": "uuid",
  "priority": "normal",
  "due_date": "2026-07-15"
}
```

Rule:

```text
Request contracts should not require clients to send fields the backend can derive safely.
```

---

# 9. Principle P07 — Consistent Response Shapes

Responses should consistently include core identity and lifecycle fields.

Common response foundation:

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "active",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:15:00Z"
}
```

Resource responses may include:

```text
owner_user_id
source_object_type
source_object_id
confirmed_by
confirmed_at
metadata where safe
```

Rule:

```text
Responses should be stable, predictable and safe for frontend and AI consumers.
```

---

# 10. Principle P08 — Consistent Error Shape

All API errors should follow a common error contract.

Recommended pattern:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [
      {
        "field": "title",
        "issue": "required"
      }
    ],
    "correlation_id": "uuid"
  }
}
```

Rule:

```text
Clients should not need endpoint-specific error parsing for common error classes.
```

---

# 11. Principle P09 — Validation Is Part of the Contract

API contracts should define expected validation behavior.

Validation types:

```text
required fields
allowed enum values
status transitions
workspace ownership
authorization
foreign key existence
polymorphic reference validity
AI confirmation requirements
```

Rule:

```text
If an API accepts a field, the contract should define how that field is validated.
```

---

# 12. Principle P10 — Audit-Aware Mutations

State-changing APIs should define audit expectations.

Examples:

```text
POST /tasks → task.created
PATCH /tasks/{task_id} → task.updated
POST /tasks/{task_id}/complete → task.completed
POST /decisions/{decision_id}/confirm → decision.confirmed
POST /exports → export.requested
```

Rule:

```text
Important mutations must be auditable by design.
```

---

# 13. Principle P11 — Runtime Event Awareness

Some API operations should emit runtime events to coordinate internal behavior.

Examples:

```text
task.created
task.status_changed
decision.confirmed
memory.created
export.requested
integration.sync_started
```

Runtime events may trigger:

```text
dashboard refresh
memory candidate creation
notifications later
integration jobs later
audit records
```

Rule:

```text
API contracts should identify which operations produce runtime events.
```

---

# 14. Principle P12 — AI-Safe by Default

API contracts must distinguish AI suggestions from official business state.

AI-related states:

```text
suggested
draft
reviewed
confirmed
applied
rejected
```

AI-related resources:

```text
agent_recommendations
agent_action_drafts
memory_candidates
operating_recommendations
```

Rule:

```text
AI may draft or recommend. Official state requires human confirmation or explicitly authorized automation.
```

---

# 15. Principle P13 — Least Privilege Authorization

API operations should assume the smallest necessary permission.

Authorization checks may include:

```text
authenticated user
workspace access
owner/admin role
resource ownership
agent authority scope
integration scope
export authorization
```

MVP simplification:

```text
workspace owner access
```

Near-MVP:

```text
workspace_access role checks
```

Rule:

```text
Authorization is not optional for workspace-scoped operating data.
```

---

# 16. Principle P14 — Metadata Is Not a Contract Escape Hatch

`metadata` may exist in responses and requests where useful, but it must not hide core API behavior.

Allowed metadata use:

```text
non-core annotations
provider-specific details
UI hints
extension data
```

Not allowed:

```text
ownership
status
workspace scope
core relationships
required audit fields
security decisions
```

Rule:

```text
Core product behavior must use explicit contract fields.
```

---

# 17. Principle P15 — Pagination for Lists

List endpoints should be paginated by default or ready for pagination.

Recommended direction:

```text
page_size
page_token
next_page_token
```

Example:

```text
GET /api/v1/workspaces/{workspace_id}/tasks?page_size=50&page_token=...
```

Rule:

```text
No unbounded list endpoint for potentially growing workspace data.
```

---

# 18. Principle P16 — Filtering and Sorting Are Consistent

List endpoints should use consistent filter and sort conventions.

Examples:

```text
?status=open
?owner_user_id=uuid
?created_after=2026-07-01
?sort=created_at:desc
```

Rule:

```text
The same field should be filtered the same way across resources.
```

---

# 19. Principle P17 — Versioned API Surface

Initial API version:

```text
/api/v1
```

Versioning rule:

```text
Prefer additive changes within a version. Use new versions for breaking changes.
```

Breaking changes include:

```text
renaming fields
removing fields
changing meaning of fields
changing status values incompatibly
changing response shape incompatibly
```

---

# 20. Principle P18 — Idempotency Where Needed

Some operations should support idempotency.

Candidates:

```text
export job creation
integration sync trigger
operating map generation
AI recommendation application
payment/billing later
```

Possible mechanism:

```text
Idempotency-Key header
```

Rule:

```text
Operations that may be retried safely should define idempotency expectations.
```

---

# 21. Principle P19 — Safe Defaults

API contracts should default toward safety.

Examples:

```text
archived records excluded from normal lists
sensitive metadata hidden by default
AI suggestions not applied automatically
export files expire by default
runtime event payloads not exposed publicly by default
```

Rule:

```text
Clients should not accidentally expose sensitive or inactive data through default API calls.
```

---

# 22. Principle P20 — OpenAPI Readiness

All API contracts should be structured so they can later become OpenAPI definitions.

Each endpoint should eventually define:

```text
method
path
purpose
request body
response body
query parameters
errors
authorization
audit events
runtime events
```

Rule:

```text
Markdown contracts should be convertible into formal OpenAPI specifications later.
```

---

# 23. MVP Design Simplifications

For MVP, Bizzi may simplify by:

- using REST-like JSON APIs;
- using workspace owner access before full RBAC;
- using text statuses validated by backend;
- exposing fewer filters initially;
- using simple pagination;
- using synchronous responses before async job orchestration where safe;
- limiting public integration API exposure.

These simplifications must preserve workspace scope, auditability and AI safety.

---

# 24. API Design Anti-Patterns

Avoid:

```text
unscoped operating endpoints
inconsistent field names
UI labels as API values
unbounded list responses
hidden status transitions inside vague updates
AI recommendations applied without confirmation
hard deletes for confirmed business records
metadata used for core relationships
inconsistent error formats
breaking changes without versioning
```

---

# 25. Acceptance Criteria

API Design Principles are accepted when:

- workspace-first API rule is defined;
- resource orientation is defined;
- request and response consistency is defined;
- explicit state transition rule is defined;
- error, validation and pagination principles are defined;
- audit and runtime event expectations are included;
- AI-safe behavior is defined;
- authorization principles are documented;
- OpenAPI readiness is established.

Status:

```text
Accepted for API Resource Catalog
```

---

# 26. Final Statement

```text
Bizzi API Design Principles define the contract rules that keep every endpoint workspace-scoped, resource-oriented, predictable, auditable, AI-safe, secure and ready for backend implementation.
```

These principles govern all remaining documents in the `28_API_CONTRACTS` layer.