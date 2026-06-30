# 06_AGENT_PROCESS_TASK_DECISION_API.md

# Bizzi Platform

## Agent Process Task Decision API

**Layer:** 28_API_CONTRACTS  
**Component Type:** API Contract Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 04_AGENT_RUNTIME.md, 05_PROCESS_RUNTIME.md, 06_TASK_RUNTIME.md, 07_DECISION_RUNTIME.md  
**Domain Reference:** 26_DOMAIN_MODEL / 05_AGENT_DOMAIN.md, 06_PROCESS_DOMAIN.md, 07_TASK_DOMAIN.md, 08_DECISION_DOMAIN.md  
**Data Model Reference:** 27_DATA_MODEL / 07_AGENT_PROCESS_TASK_DECISION_DATA_MODEL.md  
**Previous Document:** 05_FUNCTION_RESPONSIBILITY_API.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Agent, Process, Task and Decision API contracts for Bizzi Platform.

These API contracts expose the core execution layer of Bizzi: governed AI agents, repeatable processes, actionable tasks and accountable decisions.

Core question:

```text
How should Bizzi expose agents, processes, tasks and decisions through stable, workspace-scoped, auditable and AI-safe API contracts?
```

---

# 2. API Scope

This document covers:

```text
agents
agent-authority-scopes
agent-recommendations
agent-action-drafts
processes
process-steps
tasks
decisions
```

Primary data model references:

```text
agents
agent_authority_scopes
agent_recommendations
agent_action_drafts
processes
process_steps
tasks
decisions
```

MVP scope:

```text
tasks
decisions
```

Near-MVP / P2 scope:

```text
agents
agent-recommendations
agent-action-drafts
processes
process-steps
agent-authority-scopes
```

---

# 3. Design Principles Applied

This API follows:

```text
Workspace First
Resource-Oriented Contracts
Explicit State Transitions
Audit-Aware Mutations
Runtime Event Awareness
AI-Safe by Default
Least Privilege Authorization
Safe Defaults
OpenAPI Readiness
```

---

# 4. Base Paths

Workspace-scoped paths:

```text
/api/v1/workspaces/{workspace_id}/agents
/api/v1/workspaces/{workspace_id}/agent-authority-scopes
/api/v1/workspaces/{workspace_id}/agent-recommendations
/api/v1/workspaces/{workspace_id}/agent-action-drafts
/api/v1/workspaces/{workspace_id}/processes
/api/v1/workspaces/{workspace_id}/tasks
/api/v1/workspaces/{workspace_id}/decisions
```

Rule:

```text
All execution resources are workspace-scoped.
```

---

# 5. Resource Family: Agents

## Resource Name

```text
agents
```

## Purpose

Represent AI agents configured to support workspace operations.

## Data Model Reference

```text
agents
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "name": "Business Analyst Agent",
  "agent_type": "business_analyst",
  "status": "active",
  "description": "Analyzes workspace structure and suggests improvements",
  "authority_level": "recommend_only",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:15:00Z",
  "metadata": {}
}
```

---

# 6. Endpoint: List Agents

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/agents
```

## Query Parameters

```text
status optional
agent_type optional
authority_level optional
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
      "name": "Business Analyst Agent",
      "agent_type": "business_analyst",
      "status": "active",
      "authority_level": "recommend_only",
      "created_at": "2026-07-01T09:00:00Z"
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

# 7. Endpoint: Create Agent

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/agents
```

## Request Body

```json
{
  "name": "Business Analyst Agent",
  "agent_type": "business_analyst",
  "description": "Analyzes workspace structure and suggests improvements",
  "authority_level": "recommend_only"
}
```

## Required Fields

```text
name
agent_type
```

## Response: 201 Created

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "name": "Business Analyst Agent",
  "agent_type": "business_analyst",
  "status": "active",
  "authority_level": "recommend_only",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

## Validation Rules

```text
name is required
agent_type must be valid
authority_level must be valid if provided
workspace must be active
```

## Audit Events

```text
agent.created
```

## Runtime Events

```text
agent.created
```

---

# 8. Endpoint: Update Agent

## Method and Path

```text
PATCH /api/v1/workspaces/{workspace_id}/agents/{agent_id}
```

## Request Body

```json
{
  "name": "Senior Business Analyst Agent",
  "description": "Updated agent description",
  "status": "active",
  "authority_level": "draft_actions"
}
```

## Mutable Fields

```text
name
description
status
authority_level
metadata
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "name": "Senior Business Analyst Agent",
  "status": "active",
  "authority_level": "draft_actions",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

## Audit Events

```text
agent.updated
```

## Runtime Events

```text
agent.updated
```

---

# 9. Endpoint: Archive Agent

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/agents/{agent_id}/archive
```

## Request Body

```json
{
  "archive_reason": "Agent no longer used"
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
agent.archived
```

## Runtime Events

```text
agent.archived
```

---

# 10. Resource Family: Agent Recommendations

## Resource Name

```text
agent-recommendations
```

## Purpose

Represent AI-generated recommendations that must be reviewed before becoming official business state.

## Data Model Reference

```text
agent_recommendations
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "agent_id": "uuid",
  "recommendation_type": "create_task",
  "title": "Create task to review finance ownership",
  "description": "Finance function has missing owner risk",
  "status": "created",
  "confidence": "medium",
  "source_object_type": "operating_gap",
  "source_object_id": "uuid",
  "result_object_type": null,
  "result_object_id": null,
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

---

# 11. Endpoint: List Agent Recommendations

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/agent-recommendations
```

## Query Parameters

```text
status optional
agent_id optional
recommendation_type optional
source_object_type optional
source_object_id optional
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
      "agent_id": "uuid",
      "recommendation_type": "create_task",
      "title": "Create task to review finance ownership",
      "status": "created",
      "confidence": "medium",
      "created_at": "2026-07-01T09:00:00Z"
    }
  ],
  "next_page_token": null
}
```

---

# 12. Endpoint: Confirm Agent Recommendation

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/agent-recommendations/{recommendation_id}/confirm
```

## Request Body

```json
{
  "confirmation_note": "Recommendation accepted"
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
agent_recommendation.confirmed
```

## Runtime Events

```text
agent_recommendation.confirmed
```

---

# 13. Endpoint: Apply Agent Recommendation

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/agent-recommendations/{recommendation_id}/apply
```

## Request Body

```json
{
  "application_note": "Create suggested task"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "applied",
  "result_object_type": "task",
  "result_object_id": "uuid",
  "updated_at": "2026-07-01T11:00:00Z"
}
```

## Validation Rules

```text
recommendation must belong to workspace
recommendation must be confirmed or application-compatible
recommendation must not already be applied or rejected
agent authority must allow application path
human confirmation must exist unless automation authority allows direct application
```

## Audit Events

```text
agent_recommendation.applied
```

## Runtime Events

```text
agent_recommendation.applied
```

---

# 14. Endpoint: Reject Agent Recommendation

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/agent-recommendations/{recommendation_id}/reject
```

## Request Body

```json
{
  "rejection_reason": "Not relevant"
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
agent_recommendation.rejected
```

## Runtime Events

```text
agent_recommendation.rejected
```

---

# 15. Resource Family: Agent Action Drafts

## Resource Name

```text
agent-action-drafts
```

## Purpose

Represent AI-generated draft actions that may create or modify official records after review.

## Data Model Reference

```text
agent_action_drafts
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "agent_id": "uuid",
  "draft_type": "create_task",
  "status": "draft",
  "title": "Draft task for finance review",
  "payload": {
    "title": "Review finance ownership",
    "priority": "high"
  },
  "source_object_type": "operating_gap",
  "source_object_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

## Key Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/agent-action-drafts
GET /api/v1/workspaces/{workspace_id}/agent-action-drafts/{draft_id}
POST /api/v1/workspaces/{workspace_id}/agent-action-drafts/{draft_id}/approve
POST /api/v1/workspaces/{workspace_id}/agent-action-drafts/{draft_id}/apply
POST /api/v1/workspaces/{workspace_id}/agent-action-drafts/{draft_id}/reject
```

## Rule

```text
Drafts are not official business state until approved and applied.
```

---

# 16. Resource Family: Processes

## Resource Name

```text
processes
```

## Purpose

Represent repeatable business processes inside a workspace.

## Data Model Reference

```text
processes
process_steps
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "function_id": "uuid",
  "owner_user_id": "uuid",
  "name": "Supplier Review Process",
  "description": "Review and approve supplier contracts",
  "status": "active",
  "source_object_type": "function",
  "source_object_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:15:00Z"
}
```

---

# 17. Endpoint: List Processes

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/processes
```

## Query Parameters

```text
status optional
function_id optional
owner_user_id optional
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
      "function_id": "uuid",
      "owner_user_id": "uuid",
      "name": "Supplier Review Process",
      "status": "active",
      "created_at": "2026-07-01T09:00:00Z"
    }
  ],
  "next_page_token": null
}
```

---

# 18. Endpoint: Create Process

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/processes
```

## Request Body

```json
{
  "function_id": "uuid",
  "owner_user_id": "uuid",
  "name": "Supplier Review Process",
  "description": "Review and approve supplier contracts",
  "source_object_type": "function",
  "source_object_id": "uuid"
}
```

## Required Fields

```text
name
```

## Response: 201 Created

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "function_id": "uuid",
  "owner_user_id": "uuid",
  "name": "Supplier Review Process",
  "status": "draft",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

## Validation Rules

```text
name is required
function_id must belong to workspace if provided
owner_user_id must exist if provided
source object must belong to same workspace if workspace-scoped
```

## Audit Events

```text
process.created
```

## Runtime Events

```text
process.created
```

---

# 19. Endpoint: Activate Process

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/processes/{process_id}/activate
```

## Request Body

```json
{
  "activation_note": "Process reviewed and accepted"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "active",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

## Audit Events

```text
process.activated
```

## Runtime Events

```text
process.activated
```

---

# 20. Resource: Process Steps

## Resource Name

```text
process-steps
```

## Base Path

```text
/api/v1/workspaces/{workspace_id}/processes/{process_id}/steps
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "process_id": "uuid",
  "step_order": 1,
  "title": "Collect supplier documents",
  "description": "Gather contract, invoice and compliance documents",
  "status": "active",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

## Key Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/processes/{process_id}/steps
POST /api/v1/workspaces/{workspace_id}/processes/{process_id}/steps
PATCH /api/v1/workspaces/{workspace_id}/processes/{process_id}/steps/{step_id}
POST /api/v1/workspaces/{workspace_id}/processes/{process_id}/steps/{step_id}/archive
```

---

# 21. Resource Family: Tasks

## Resource Name

```text
tasks
```

## Purpose

Represent actionable work items in a workspace.

## Data Model Reference

```text
tasks
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "function_id": "uuid",
  "process_id": "uuid",
  "owner_user_id": "uuid",
  "agent_id": "uuid",
  "title": "Review supplier contract",
  "description": "Check payment terms and risk exposure",
  "status": "open",
  "priority": "normal",
  "due_date": "2026-07-15",
  "source_object_type": "operating_gap",
  "source_object_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:15:00Z"
}
```

---

# 22. Endpoint: List Tasks

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/tasks
```

## Query Parameters

```text
status optional
priority optional
owner_user_id optional
function_id optional
process_id optional
due_before optional
due_after optional
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
      "title": "Review supplier contract",
      "status": "open",
      "priority": "normal",
      "owner_user_id": "uuid",
      "due_date": "2026-07-15",
      "created_at": "2026-07-01T09:00:00Z"
    }
  ],
  "next_page_token": null
}
```

---

# 23. Endpoint: Create Task

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/tasks
```

## Request Body

```json
{
  "title": "Review supplier contract",
  "description": "Check payment terms and risk exposure",
  "function_id": "uuid",
  "process_id": "uuid",
  "owner_user_id": "uuid",
  "priority": "normal",
  "due_date": "2026-07-15",
  "source_object_type": "operating_gap",
  "source_object_id": "uuid"
}
```

## Required Fields

```text
title
```

## Response: 201 Created

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "title": "Review supplier contract",
  "status": "open",
  "priority": "normal",
  "owner_user_id": "uuid",
  "due_date": "2026-07-15",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

## Validation Rules

```text
title is required
priority must be valid if provided
due_date must be valid if provided
function_id must belong to workspace if provided
process_id must belong to workspace if provided
owner_user_id must exist if provided
source object must belong to same workspace if workspace-scoped
```

## Audit Events

```text
task.created
```

## Runtime Events

```text
task.created
dashboard.refresh_requested
```

---

# 24. Endpoint: Update Task

## Method and Path

```text
PATCH /api/v1/workspaces/{workspace_id}/tasks/{task_id}
```

## Request Body

```json
{
  "title": "Review updated supplier contract",
  "description": "Check risk exposure and ownership",
  "owner_user_id": "uuid",
  "priority": "high",
  "due_date": "2026-07-20"
}
```

## Mutable Fields

```text
title
description
function_id
process_id
owner_user_id
priority
due_date
metadata
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "title": "Review updated supplier contract",
  "status": "open",
  "priority": "high",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

## Audit Events

```text
task.updated
```

## Runtime Events

```text
task.updated
dashboard.refresh_requested
```

---

# 25. Endpoint: Start Task

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/start
```

## Request Body

```json
{
  "start_note": "Work started"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "in_progress",
  "updated_at": "2026-07-01T10:00:00Z"
}
```

## Audit Events

```text
task.started
```

## Runtime Events

```text
task.status_changed
```

---

# 26. Endpoint: Complete Task

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/complete
```

## Request Body

```json
{
  "completion_note": "Supplier contract reviewed",
  "result_summary": "Payment terms accepted"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "completed",
  "completed_at": "2026-07-01T12:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

## Audit Events

```text
task.completed
```

## Runtime Events

```text
task.completed
dashboard.refresh_requested
memory.candidate_created optional
```

---

# 27. Endpoint: Archive Task

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/archive
```

## Request Body

```json
{
  "archive_reason": "Task no longer relevant"
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
task.archived
```

## Runtime Events

```text
task.archived
```

---

# 28. Resource Family: Decisions

## Resource Name

```text
decisions
```

## Purpose

Represent business decisions, their context, confirmation and traceability.

## Data Model Reference

```text
decisions
```

## Resource Shape

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "task_id": "uuid",
  "function_id": "uuid",
  "owner_user_id": "uuid",
  "agent_id": "uuid",
  "title": "Approve supplier contract",
  "description": "Decision to approve supplier contract after review",
  "decision_type": "approval",
  "status": "draft",
  "decision_date": null,
  "confirmed_by": null,
  "confirmed_at": null,
  "source_object_type": "task",
  "source_object_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:15:00Z"
}
```

---

# 29. Endpoint: List Decisions

## Method and Path

```text
GET /api/v1/workspaces/{workspace_id}/decisions
```

## Query Parameters

```text
status optional
decision_type optional
owner_user_id optional
function_id optional
task_id optional
decision_date_from optional
decision_date_to optional
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
      "title": "Approve supplier contract",
      "decision_type": "approval",
      "status": "draft",
      "owner_user_id": "uuid",
      "created_at": "2026-07-01T09:00:00Z"
    }
  ],
  "next_page_token": null
}
```

---

# 30. Endpoint: Create Decision

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/decisions
```

## Request Body

```json
{
  "title": "Approve supplier contract",
  "description": "Decision to approve supplier contract after review",
  "decision_type": "approval",
  "task_id": "uuid",
  "function_id": "uuid",
  "owner_user_id": "uuid",
  "source_object_type": "task",
  "source_object_id": "uuid"
}
```

## Required Fields

```text
title
```

## Response: 201 Created

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "title": "Approve supplier contract",
  "decision_type": "approval",
  "status": "draft",
  "owner_user_id": "uuid",
  "created_at": "2026-07-01T09:00:00Z",
  "updated_at": "2026-07-01T09:00:00Z"
}
```

## Validation Rules

```text
title is required
decision_type must be valid if provided
task_id must belong to workspace if provided
function_id must belong to workspace if provided
owner_user_id must exist if provided
source object must belong to same workspace if workspace-scoped
```

## Audit Events

```text
decision.created
```

## Runtime Events

```text
decision.created
```

---

# 31. Endpoint: Confirm Decision

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm
```

## Request Body

```json
{
  "confirmation_note": "Decision confirmed by owner",
  "decision_date": "2026-07-01"
}
```

## Response: 200 OK

```json
{
  "id": "uuid",
  "workspace_id": "uuid",
  "status": "confirmed",
  "decision_date": "2026-07-01",
  "confirmed_by": "uuid",
  "confirmed_at": "2026-07-01T12:00:00Z",
  "updated_at": "2026-07-01T12:00:00Z"
}
```

## Validation Rules

```text
decision must belong to workspace
decision must not be archived
decision must be in draft, reviewed or confirmation-compatible status
AI-generated decision must preserve human confirmation unless automation authority explicitly permits it
```

## Audit Events

```text
decision.confirmed
```

## Runtime Events

```text
decision.confirmed
dashboard.refresh_requested
memory.candidate_created optional
```

---

# 32. Endpoint: Archive Decision

## Method and Path

```text
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/archive
```

## Request Body

```json
{
  "archive_reason": "Decision superseded"
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
decision.archived
```

## Runtime Events

```text
decision.archived
```

---

# 33. Common Error Codes

This API may return:

```text
unauthenticated
forbidden
not_found
validation_error
conflict
workspace_archived
invalid_status_transition
invalid_object_reference
invalid_agent_authority
human_confirmation_required
```

Example:

```json
{
  "error": {
    "code": "human_confirmation_required",
    "message": "This AI-generated action requires human confirmation before application.",
    "correlation_id": "uuid"
  }
}
```

---

# 34. Authorization Matrix

| Operation | MVP Rule | Expansion Rule |
|---|---|---|
| List tasks | workspace owner | active workspace access |
| Create task | workspace owner | owner/admin/manager/member with permission |
| Start task | workspace owner | owner/admin/assigned user |
| Complete task | workspace owner | owner/admin/assigned user |
| Archive task | workspace owner | owner/admin/manager |
| List decisions | workspace owner | active workspace access |
| Create decision | workspace owner | owner/admin/manager |
| Confirm decision | workspace owner | owner/admin/authorized decision owner |
| Manage agents | workspace owner | owner/admin |
| Apply AI recommendation | workspace owner | role + agent authority + confirmation |
| Manage processes | workspace owner | owner/admin/manager |

---

# 35. Audit and Runtime Event Summary

| API Operation | Audit Event | Runtime Event |
|---|---|---|
| Create agent | agent.created | agent.created |
| Update agent | agent.updated | agent.updated |
| Archive agent | agent.archived | agent.archived |
| Confirm recommendation | agent_recommendation.confirmed | agent_recommendation.confirmed |
| Apply recommendation | agent_recommendation.applied | agent_recommendation.applied |
| Reject recommendation | agent_recommendation.rejected | agent_recommendation.rejected |
| Create process | process.created | process.created |
| Activate process | process.activated | process.activated |
| Create task | task.created | task.created |
| Update task | task.updated | task.updated |
| Start task | task.started | task.status_changed |
| Complete task | task.completed | task.completed |
| Archive task | task.archived | task.archived |
| Create decision | decision.created | decision.created |
| Confirm decision | decision.confirmed | decision.confirmed |
| Archive decision | decision.archived | decision.archived |

---

# 36. MVP Simplifications

For MVP, Bizzi may simplify by:

- implementing tasks and decisions before full agent configuration;
- using simple task statuses;
- using simple decision statuses;
- using owner-only workspace authorization;
- storing AI suggestions as recommendations before allowing action drafts;
- using audit_events instead of dedicated task history;
- postponing process steps until process behavior is needed;
- requiring human confirmation for all AI-generated official actions.

These simplifications must preserve workspace scope, auditability and AI safety.

---

# 37. Future Expansion

Future API expansion may add:

```text
bulk task creation
task comments
task history
decision options
decision outcomes
decision review workflow
process versioning
process inputs and outputs
agent performance metrics
agent authority policy simulation
automated task assignment
agent run logs
```

---

# 38. Acceptance Criteria

Agent Process Task Decision API is accepted when:

- agent endpoints are defined;
- agent recommendation and draft concepts are defined;
- process endpoints are defined;
- task endpoints are defined;
- decision endpoints are defined;
- request and response shapes are documented;
- validation rules are identified;
- authorization rules are defined;
- audit and runtime event expectations are defined;
- MVP simplifications are documented;
- AI confirmation requirements are explicit.

Status:

```text
Accepted for Memory Audit Event API Design
```

---

# 39. Final Statement

```text
Bizzi Agent Process Task Decision API defines how the platform exposes governed AI assistance, repeatable execution, actionable work and accountable decisions through workspace-scoped, auditable and AI-safe API contracts.
```

This API forms the execution core of Bizzi Platform.