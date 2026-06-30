# 02_API_RESOURCE_CATALOG.md

# Bizzi Platform

## API Resource Catalog

**Layer:** 28_API_CONTRACTS  
**Component Type:** API Architecture Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Data Model Reference:** 27_DATA_MODEL v1.1  
**Previous Document:** 01_API_DESIGN_PRINCIPLES.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the API Resource Catalog for Bizzi Platform.

It identifies the canonical API resources, endpoint families, workspace scope, primary operations and implementation priority for the `28_API_CONTRACTS` layer.

Core question:

```text
Which API resources must Bizzi expose so that the platform can support workspace setup, operating maps, functions, responsibilities, tasks, decisions, memory, audit, events, integrations, dashboard and exports?
```

---

# 2. Resource Catalog Role

The Resource Catalog is the bridge between:

```text
Domain Model entities
↓
Data Model tables
↓
API endpoints
↓
Backend services
↓
Frontend screens and AI agents
```

It provides a single reference for:

- API resource naming;
- endpoint grouping;
- MVP vs expansion priority;
- workspace scope rules;
- audit and runtime event expectations;
- future OpenAPI structure.

---

# 3. Resource Naming Rules

API resource names should use:

```text
kebab-case plural nouns
```

Examples:

```text
workspaces
operating-maps
operating-gaps
memory-entries
audit-events
runtime-events
export-jobs
```

API fields inside JSON should use:

```text
snake_case
```

Examples:

```text
workspace_id
owner_user_id
source_object_type
created_at
updated_at
```

---

# 4. Base API Structure

Recommended base path:

```text
/api/v1
```

Workspace-scoped resources:

```text
/api/v1/workspaces/{workspace_id}/{resource}
```

Identity and workspace discovery resources:

```text
/api/v1/me
/api/v1/workspaces
```

---

# 5. Resource Priority Levels

Priority levels:

```text
P1 — MVP core resource
P2 — governed runtime resource
P3 — expansion resource
```

Definitions:

```text
P1 supports the first runnable Bizzi vertical slice.
P2 supports governed AI, integrations, process depth, access and export control.
P3 supports enterprise hardening, collaboration depth, analytics and public API growth.
```

---

# 6. P1 MVP Resource Families

P1 API families:

```text
identity
workspaces
workspace-settings
operating-maps
operating-gaps
functions
responsibilities
tasks
decisions
memory-entries
dashboard
exports
audit-events minimal
runtime-events minimal
```

These support the first product loop:

```text
Create workspace
↓
Generate operating map
↓
Identify gaps
↓
Create functions
↓
Assign responsibilities
↓
Create tasks
↓
Record decisions
↓
Store memory
↓
Show dashboard
↓
Export summary
```

---

# 7. P2 Governed Runtime Resource Families

P2 API families:

```text
agents
agent-authority-scopes
agent-recommendations
agent-action-drafts
processes
process-steps
integrations
integration-sync-jobs
security-policies
workspace-access
export-jobs
ownership-gaps
operating-recommendations
```

These support controlled AI assistance, structured execution and multi-user or integration governance.

---

# 8. P3 Expansion Resource Families

P3 API families:

```text
roles
permissions
role-permissions
workspace-invitations
responsibility-assignments
task-comments
task-history
decision-options
decision-outcomes
memory-sources
memory-usage
dashboard-alerts
dashboard-insights
export-templates
export-files
security-events
webhooks
public-api-clients
```

These should be implemented only when product behavior requires them.

---

# 9. Resource Catalog Summary

| API Resource | Path Segment | Priority | Workspace-Scoped | Data Model Reference |
|---|---|---:|---|---|
| Current User | me | P1 | No | users |
| Workspaces | workspaces | P1 | Mixed | company_workspaces |
| Workspace Settings | workspace-settings | P1 | Yes | workspace_settings |
| Operating Maps | operating-maps | P1 | Yes | operating_maps |
| Operating Gaps | operating-gaps | P1 | Yes | operating_gaps |
| Functions | functions | P1 | Yes | functions |
| Responsibilities | responsibilities | P1 | Yes | responsibilities |
| Tasks | tasks | P1 | Yes | tasks |
| Decisions | decisions | P1 | Yes | decisions |
| Memory Entries | memory-entries | P1 | Yes | memory_entries |
| Dashboard | dashboard | P1 | Yes | dashboard_metrics |
| Export Jobs | export-jobs | P1/P2 | Yes | export_jobs |
| Audit Events | audit-events | P1/P2 | Yes | audit_events |
| Runtime Events | runtime-events | P1/P2 | Yes | runtime_events |
| Agents | agents | P2 | Yes | agents |
| Agent Authority Scopes | agent-authority-scopes | P2 | Yes | agent_authority_scopes |
| Agent Recommendations | agent-recommendations | P2 | Yes | agent_recommendations |
| Agent Action Drafts | agent-action-drafts | P2 | Yes | agent_action_drafts |
| Processes | processes | P2 | Yes | processes |
| Process Steps | process-steps | P2 | Yes | process_steps |
| Integrations | integrations | P2 | Yes | integrations |
| Integration Sync Jobs | integration-sync-jobs | P2 | Yes | integration_sync_jobs |
| Security Policies | security-policies | P2 | Yes | security_policies |
| Workspace Access | workspace-access | P2 | Yes | workspace_access |

---

# 10. Identity Resource

## Resource

```text
me
```

## Purpose

Expose the authenticated user identity and basic available workspace access.

## Example Endpoints

```text
GET /api/v1/me
GET /api/v1/me/workspaces
```

## Priority

```text
P1
```

## Notes

This resource is not workspace-scoped, but it should only return data authorized for the current user.

---

# 11. Workspace Resource

## Resource

```text
workspaces
```

## Purpose

Create, list, read and manage company workspaces.

## Example Endpoints

```text
GET /api/v1/workspaces
POST /api/v1/workspaces
GET /api/v1/workspaces/{workspace_id}
PATCH /api/v1/workspaces/{workspace_id}
POST /api/v1/workspaces/{workspace_id}/archive
```

## Priority

```text
P1
```

## Audit Events

```text
workspace.created
workspace.updated
workspace.archived
```

---

# 12. Workspace Settings Resource

## Resource

```text
workspace-settings
```

## Purpose

Manage workspace-level configuration.

## Example Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/workspace-settings
PATCH /api/v1/workspaces/{workspace_id}/workspace-settings
```

## Priority

```text
P1
```

---

# 13. Operating Map Resource

## Resource

```text
operating-maps
```

## Purpose

Generate, review and manage operating maps.

## Example Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/operating-maps
POST /api/v1/workspaces/{workspace_id}/operating-maps/generate
GET /api/v1/workspaces/{workspace_id}/operating-maps/{operating_map_id}
POST /api/v1/workspaces/{workspace_id}/operating-maps/{operating_map_id}/confirm
POST /api/v1/workspaces/{workspace_id}/operating-maps/{operating_map_id}/archive
```

## Priority

```text
P1
```

## Runtime Events

```text
operating_map.generated
operating_map.confirmed
```

---

# 14. Operating Gap Resource

## Resource

```text
operating-gaps
```

## Purpose

Expose detected operating gaps and allow review, acceptance and resolution.

## Example Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/operating-gaps
GET /api/v1/workspaces/{workspace_id}/operating-gaps/{operating_gap_id}
POST /api/v1/workspaces/{workspace_id}/operating-gaps/{operating_gap_id}/accept
POST /api/v1/workspaces/{workspace_id}/operating-gaps/{operating_gap_id}/resolve
POST /api/v1/workspaces/{workspace_id}/operating-gaps/{operating_gap_id}/archive
```

## Priority

```text
P1
```

---

# 15. Function Resource

## Resource

```text
functions
```

## Purpose

Manage enterprise functions and business capability ownership structure.

## Example Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/functions
POST /api/v1/workspaces/{workspace_id}/functions
GET /api/v1/workspaces/{workspace_id}/functions/{function_id}
PATCH /api/v1/workspaces/{workspace_id}/functions/{function_id}
POST /api/v1/workspaces/{workspace_id}/functions/{function_id}/archive
```

## Priority

```text
P1
```

---

# 16. Responsibility Resource

## Resource

```text
responsibilities
```

## Purpose

Assign and manage responsibility for functions and operating objects.

## Example Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/responsibilities
POST /api/v1/workspaces/{workspace_id}/responsibilities
GET /api/v1/workspaces/{workspace_id}/responsibilities/{responsibility_id}
PATCH /api/v1/workspaces/{workspace_id}/responsibilities/{responsibility_id}
POST /api/v1/workspaces/{workspace_id}/responsibilities/{responsibility_id}/archive
```

## Priority

```text
P1
```

---

# 17. Task Resource

## Resource

```text
tasks
```

## Purpose

Create, assign, track and complete actionable work.

## Example Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/tasks
POST /api/v1/workspaces/{workspace_id}/tasks
GET /api/v1/workspaces/{workspace_id}/tasks/{task_id}
PATCH /api/v1/workspaces/{workspace_id}/tasks/{task_id}
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/start
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/complete
POST /api/v1/workspaces/{workspace_id}/tasks/{task_id}/archive
```

## Priority

```text
P1
```

## Runtime Events

```text
task.created
task.status_changed
task.completed
```

---

# 18. Decision Resource

## Resource

```text
decisions
```

## Purpose

Capture, confirm and review business decisions.

## Example Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/decisions
POST /api/v1/workspaces/{workspace_id}/decisions
GET /api/v1/workspaces/{workspace_id}/decisions/{decision_id}
PATCH /api/v1/workspaces/{workspace_id}/decisions/{decision_id}
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/confirm
POST /api/v1/workspaces/{workspace_id}/decisions/{decision_id}/archive
```

## Priority

```text
P1
```

## Runtime Events

```text
decision.created
decision.confirmed
```

---

# 19. Memory Entry Resource

## Resource

```text
memory-entries
```

## Purpose

Store and retrieve reusable workspace-scoped enterprise memory.

## Example Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/memory-entries
POST /api/v1/workspaces/{workspace_id}/memory-entries
GET /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}
PATCH /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/activate
POST /api/v1/workspaces/{workspace_id}/memory-entries/{memory_entry_id}/archive
```

## Priority

```text
P1
```

## Rule

```text
Archived memory must not be used as active AI context.
```

---

# 20. Dashboard Resource

## Resource

```text
dashboard
```

## Purpose

Expose workspace operating status, metrics and alerts.

## Example Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/dashboard
GET /api/v1/workspaces/{workspace_id}/dashboard/metrics
GET /api/v1/workspaces/{workspace_id}/dashboard/activity
```

## Priority

```text
P1
```

## Notes

Dashboard may combine persisted metrics and dynamic calculations.

---

# 21. Export Job Resource

## Resource

```text
export-jobs
```

## Purpose

Request, track and retrieve governed exports.

## Example Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/export-jobs
POST /api/v1/workspaces/{workspace_id}/export-jobs
GET /api/v1/workspaces/{workspace_id}/export-jobs/{export_job_id}
POST /api/v1/workspaces/{workspace_id}/export-jobs/{export_job_id}/cancel
```

## Priority

```text
P1/P2
```

## Runtime Events

```text
export.requested
export.completed
export.failed
```

---

# 22. Audit Event Resource

## Resource

```text
audit-events
```

## Purpose

Expose authorized audit history for workspace objects.

## Example Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/audit-events
GET /api/v1/workspaces/{workspace_id}/audit-events/{audit_event_id}
```

## Priority

```text
P1/P2
```

## Rule

```text
Audit events are read-oriented and should not be modified through normal public API flows.
```

---

# 23. Runtime Event Resource

## Resource

```text
runtime-events
```

## Purpose

Expose limited runtime event visibility for diagnostics and internal coordination.

## Example Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/runtime-events
GET /api/v1/workspaces/{workspace_id}/runtime-events/{runtime_event_id}
```

## Priority

```text
P1/P2
```

## Rule

```text
Runtime events may be internal-only or restricted to administrative users.
```

---

# 24. Agent and AI Resource Family

## Resources

```text
agents
agent-authority-scopes
agent-recommendations
agent-action-drafts
```

## Purpose

Expose governed AI agent configuration, recommendations and draft actions.

## Example Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/agents
POST /api/v1/workspaces/{workspace_id}/agents
GET /api/v1/workspaces/{workspace_id}/agent-recommendations
POST /api/v1/workspaces/{workspace_id}/agent-recommendations/{recommendation_id}/confirm
POST /api/v1/workspaces/{workspace_id}/agent-recommendations/{recommendation_id}/apply
POST /api/v1/workspaces/{workspace_id}/agent-recommendations/{recommendation_id}/reject
```

## Priority

```text
P2
```

## Rule

```text
AI outputs must remain reviewable before official state changes unless explicit authority allows automation.
```

---

# 25. Process Resource Family

## Resources

```text
processes
process-steps
```

## Purpose

Expose repeatable process definitions and ordered process steps.

## Example Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/processes
POST /api/v1/workspaces/{workspace_id}/processes
GET /api/v1/workspaces/{workspace_id}/processes/{process_id}/steps
POST /api/v1/workspaces/{workspace_id}/processes/{process_id}/steps
```

## Priority

```text
P2
```

---

# 26. Integration and Security Resource Family

## Resources

```text
integrations
integration-sync-jobs
security-policies
workspace-access
```

## Purpose

Expose controlled external connections, sync jobs, policy rules and workspace access.

## Example Endpoints

```text
GET /api/v1/workspaces/{workspace_id}/integrations
POST /api/v1/workspaces/{workspace_id}/integrations
POST /api/v1/workspaces/{workspace_id}/integrations/{integration_id}/sync
GET /api/v1/workspaces/{workspace_id}/security-policies
GET /api/v1/workspaces/{workspace_id}/workspace-access
POST /api/v1/workspaces/{workspace_id}/workspace-access
```

## Priority

```text
P2
```

## Rule

```text
APIs must expose credential references only, never raw credential values.
```

---

# 27. Resource Contract Template

Each detailed resource document should define:

```text
Resource name
Purpose
Data model reference
Endpoint list
Request schemas
Response schemas
Validation rules
Authorization rules
Audit events
Runtime events
MVP scope
Expansion scope
```

---

# 28. Out of Scope for MVP

The following resources are not required for the first MVP unless product behavior demands them:

```text
roles
permissions
role-permissions
workspace-invitations
task-comments
task-history
decision-options
decision-outcomes
memory-usage
memory-embeddings
dashboard-insights
export-templates
security-events
webhooks
public-api-clients
```

---

# 29. Acceptance Criteria

API Resource Catalog is accepted when:

- canonical API resources are listed;
- resource naming is standardized;
- resource priorities are defined;
- workspace scoping is identified;
- MVP resource families are clear;
- governed runtime resource families are identified;
- expansion resources are documented;
- example endpoint families are provided;
- resource contract template is defined.

Status:

```text
Accepted for Workspace API Design
```

---

# 30. Final Statement

```text
Bizzi API Resource Catalog defines the canonical resource map for the API layer, translating Domain Model and Data Model entities into workspace-scoped, secure, auditable and implementation-ready endpoint families.
```

This catalog becomes the roadmap for detailed API contract documents in the `28_API_CONTRACTS` layer.