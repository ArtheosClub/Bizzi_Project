# 00_API_CONTRACTS_VISION.md

# Bizzi Platform

## API Contracts Vision

**Layer:** 28_API_CONTRACTS  
**Component Type:** API Architecture Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**Previous Layer:** 27_DATA_MODEL / 20_DATA_MODEL_AUDIT_ADDENDUM.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the vision for the `28_API_CONTRACTS` layer of Bizzi Platform.

It establishes how Bizzi should expose its product capabilities through stable, workspace-scoped, secure and implementation-ready API contracts that connect frontend clients, backend services, AI agents, integrations and future automation layers.

Core question:

```text
How should Bizzi define API contracts so that product behavior, data model, runtime logic and future implementation remain aligned?
```

---

# 2. API Contracts Layer Role

The API Contracts layer translates the Data Model and Domain Model into externally and internally consumable service boundaries.

It defines:

- resource names;
- endpoint families;
- request structures;
- response structures;
- validation expectations;
- error patterns;
- pagination rules;
- filtering rules;
- sorting rules;
- authorization assumptions;
- workspace scoping rules;
- audit and runtime event expectations;
- AI-safe interaction boundaries.

This layer does not yet implement backend code. It defines the contract that backend, frontend and AI orchestration must follow.

---

# 3. Position in Architecture

The API Contracts layer sits between Data Model and Backend Service Design.

Canonical flow:

```text
Product Definition
↓
Runtime Platform
↓
Domain Model
↓
Data Model
↓
API Contracts
↓
Backend Service Design
↓
Frontend Application
↓
Agent Orchestration
```

API Contracts must remain aligned with:

```text
25_RUNTIME_PLATFORM
26_DOMAIN_MODEL
27_DATA_MODEL
```

---

# 4. API Thesis

```text
Bizzi APIs must expose operating clarity, governed execution, memory, auditability and workspace-safe AI assistance through stable contracts that are simple enough for MVP and strong enough for enterprise evolution.
```

---

# 5. Contract Consumers

Bizzi API contracts will be consumed by:

```text
web frontend
backend services
AI orchestration layer
agent runtime
integration adapters
export generators
dashboard views
future mobile clients
future public API clients
```

The first consumers are expected to be:

```text
Bizzi web app
Bizzi backend service layer
Bizzi agent orchestration runtime
```

---

# 6. API Contract Principles

## 6.1 Workspace First

All operating API calls must be workspace-scoped.

Common path pattern:

```text
/workspaces/{workspace_id}/...
```

Rule:

```text
No workspace scope, no operating API action.
```

---

## 6.2 Resource-Oriented Design

API endpoints should be organized around stable product resources.

Examples:

```text
workspaces
operating-maps
functions
responsibilities
tasks
decisions
memory-entries
audit-events
runtime-events
integrations
dashboard-metrics
export-jobs
```

---

## 6.3 Explicit State Changes

State-changing operations should be explicit and auditable.

Examples:

```text
POST /tasks
PATCH /tasks/{task_id}
POST /tasks/{task_id}/complete
POST /decisions/{decision_id}/confirm
POST /agent-recommendations/{recommendation_id}/apply
```

Rule:

```text
Important business transitions should not be hidden inside vague update calls.
```

---

## 6.4 Stable Internal Field Names

API fields should generally use the same stable snake_case names as the Data Model.

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

---

## 6.5 Human Confirmation for AI Effects

AI may suggest or draft, but official state changes must preserve confirmation when required.

API contracts should distinguish:

```text
suggest
review
confirm
apply
reject
```

Rule:

```text
AI-generated official changes must be traceable to human confirmation or explicit automation authority.
```

---

## 6.6 Audit-Aware by Design

APIs that change important records should define audit expectations.

Examples:

```text
task.created
task.status_changed
decision.confirmed
memory.created
export.completed
integration.sync_started
```

---

## 6.7 MVP Simplicity with Expansion Path

API contracts should start simple but not block future growth.

MVP may expose:

```text
core CRUD
list filtering
basic status transitions
simple dashboard
simple export jobs
```

Expansion may add:

```text
bulk operations
advanced filters
public API tokens
webhooks
real-time subscriptions
external developer API
```

---

# 7. API Style Direction

Recommended initial API style:

```text
REST-like JSON API
```

Reasons:

- simple to implement;
- easy to document;
- easy to test;
- frontend-friendly;
- AI-agent-friendly;
- compatible with future OpenAPI documentation.

Future additions may include:

```text
webhooks
server-sent events
GraphQL-like query layer
internal event bus APIs
public integration API
```

---

# 8. Resource Families

The API layer should be organized into resource families matching Data Model and Domain Model boundaries.

Initial families:

```text
workspace APIs
operating map APIs
function and responsibility APIs
agent APIs
process APIs
task APIs
decision APIs
memory APIs
audit APIs
runtime event APIs
integration APIs
security APIs
dashboard APIs
export APIs
```

---

# 9. MVP API Surface

The MVP API should support the first useful Bizzi product loop:

```text
create workspace
capture workspace context
generate operating map
review operating gaps
create functions
assign responsibilities
create tasks
record decisions
create memory entries
show dashboard
export workspace summary
```

MVP API groups:

```text
Workspace API
Operating Map API
Function Responsibility API
Task API
Decision API
Memory API
Dashboard API
Export API
Audit/Event minimal support
```

---

# 10. Workspace Scope Pattern

Recommended API path pattern:

```text
/api/v1/workspaces/{workspace_id}/resources
```

Examples:

```text
GET /api/v1/workspaces/{workspace_id}/tasks
POST /api/v1/workspaces/{workspace_id}/tasks
GET /api/v1/workspaces/{workspace_id}/decisions
POST /api/v1/workspaces/{workspace_id}/operating-maps/generate
GET /api/v1/workspaces/{workspace_id}/dashboard
```

Global or identity endpoints may exist outside workspace scope:

```text
GET /api/v1/me
GET /api/v1/workspaces
POST /api/v1/workspaces
```

---

# 11. Request Contract Principles

Requests should be:

- explicit;
- minimal;
- validated;
- workspace-scoped;
- idempotent where appropriate;
- aligned with Data Dictionary fields;
- safe for audit and runtime event generation.

Create request example pattern:

```json
{
  "title": "Review supplier contract",
  "description": "Check payment terms and risk exposure",
  "owner_user_id": "uuid",
  "priority": "normal",
  "due_date": "2026-07-15"
}
```

---

# 12. Response Contract Principles

Responses should be:

- predictable;
- typed by resource shape;
- include IDs;
- include status;
- include timestamps;
- include ownership fields where relevant;
- include source traceability where relevant;
- avoid exposing sensitive internal metadata by default.

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

---

# 13. Error Contract Direction

Bizzi APIs should use a consistent error shape.

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

Error contracts will be defined in:

```text
10_ERROR_AND_VALIDATION_CONTRACTS.md
```

---

# 14. Pagination, Filtering and Sorting Direction

List endpoints should support consistent patterns.

Examples:

```text
?page_size=50&page_token=...
?status=open
?owner_user_id=...
?sort=created_at:desc
```

Detailed rules will be defined in:

```text
11_PAGINATION_FILTERING_SORTING.md
```

---

# 15. Security and Authorization Direction

API contracts should assume:

```text
authenticated user
workspace authorization
role or owner checks
agent authority checks
integration scope checks
export authorization
```

MVP may start with:

```text
workspace owner access
```

Near-MVP expands to:

```text
workspace_access roles
```

---

# 16. Audit and Runtime Event Expectations

State-changing APIs should define whether they produce:

```text
audit event
runtime event
memory candidate
dashboard refresh
notification later
```

Example:

```text
POST /tasks
→ task.created runtime event
→ task.created audit event
→ dashboard refresh candidate
```

---

# 17. AI Interaction Contracts

AI-related APIs should distinguish between:

```text
recommendation
draft
confirmation
application
rejection
```

Example resources:

```text
agent_recommendations
agent_action_drafts
memory_candidates
operating_recommendations
```

Rule:

```text
AI suggestions should be reviewable records before becoming official business state.
```

---

# 18. API Versioning

Initial API version:

```text
/api/v1
```

Versioning principles:

```text
Do not break existing clients without version transition.
Prefer additive response fields.
Deprecate before removing.
Keep internal schema evolution separate from external contract stability.
```

---

# 19. OpenAPI Direction

Future implementation should generate or maintain:

```text
OpenAPI specification
request schemas
response schemas
error schemas
auth definitions
example payloads
```

This document layer prepares for that future but does not yet create the formal OpenAPI file.

---

# 20. Relationship to Backend Service Design

API Contracts define what is exposed.

Backend Service Design will define how it is implemented.

Boundary:

```text
API Contracts:
- endpoints
- schemas
- validation surface
- error shapes
- resource behavior

Backend Services:
- transactions
- repositories
- domain validation
- audit/event emission
- authorization implementation
```

---

# 21. Out of Scope

This document does not define:

- actual backend code;
- database migrations;
- frontend components;
- authentication provider implementation;
- deployment environment;
- OpenAPI YAML;
- public developer portal;
- billing API;
- rate limit infrastructure.

These belong to later layers.

---

# 22. API Contracts Layer Deliverables

Expected documents for this layer:

```text
00_API_CONTRACTS_VISION.md
01_API_DESIGN_PRINCIPLES.md
02_API_RESOURCE_CATALOG.md
03_WORKSPACE_API.md
04_OPERATING_MAP_API.md
05_FUNCTION_RESPONSIBILITY_API.md
06_AGENT_PROCESS_TASK_DECISION_API.md
07_MEMORY_AUDIT_EVENT_API.md
08_INTEGRATION_SECURITY_API.md
09_DASHBOARD_EXPORT_API.md
10_ERROR_AND_VALIDATION_CONTRACTS.md
11_PAGINATION_FILTERING_SORTING.md
12_API_CONTRACTS_MILESTONE.md
13_API_CONTRACTS_AUDIT.md
```

---

# 23. Acceptance Criteria

API Contracts Vision is accepted when:

- role of API layer is defined;
- API consumers are identified;
- REST-like JSON direction is established;
- workspace-first API principle is defined;
- resource families are listed;
- MVP API surface is identified;
- request and response principles are defined;
- error, pagination and security directions are established;
- AI interaction contract principles are defined;
- transition readiness from Data Model to API Contracts is clear.

Status:

```text
Accepted for API Design Principles
```

---

# 24. Final Statement

```text
Bizzi API Contracts define the stable product-facing and service-facing interface layer that transforms the Data Model and Domain Model into workspace-scoped, secure, auditable and AI-safe resource operations.
```

This vision starts the transition from data architecture into implementable platform behavior.