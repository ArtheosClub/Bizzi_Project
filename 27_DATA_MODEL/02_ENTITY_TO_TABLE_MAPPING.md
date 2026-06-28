# 02_ENTITY_TO_TABLE_MAPPING.md

# Bizzi Platform

## Entity to Table Mapping

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Mapping Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Domain Reference:** 26_DOMAIN_MODEL  
**Previous Documents:** 00_DATA_MODEL_VISION.md, 01_DATABASE_PRINCIPLES.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document maps Bizzi Domain Model entities to database tables.

It creates the bridge between conceptual domain architecture and implementation-ready relational storage.

Core question:

```text
Which database table stores each Bizzi domain entity, and what is the implementation priority for MVP?
```

---

# 2. Mapping Role

The Entity to Table Mapping defines:

- domain entity names;
- corresponding table names;
- aggregate roots;
- MVP priority;
- workspace scope requirement;
- relationship direction;
- implementation notes;
- deferred supporting tables.

This document does not yet define every column in full detail. That happens in the following Data Model documents.

---

# 3. Naming Convention

Domain entities use PascalCase:

```text
CompanyWorkspace
MemoryEntry
AuditEvent
RuntimeEvent
```

Database tables use snake_case plural:

```text
company_workspaces
memory_entries
audit_events
runtime_events
```

Foreign key columns use snake_case singular references:

```text
workspace_id
user_id
owner_user_id
function_id
process_id
task_id
decision_id
agent_id
```

---

# 4. Mapping Priority

## Priority 1 — MVP Core

Required for the first runnable vertical slice.

## Priority 2 — Governed Runtime

Needed for structured AI assistance, runtime completeness and traceability.

## Priority 3 — Expansion

Useful after MVP or for advanced multi-user, analytics and enterprise scenarios.

---

# 5. Identity Mapping

| Domain Entity | Table | Priority | Workspace Scoped | Notes |
|---|---|---:|---|---|
| User | users | 1 | No | Human identity across platform |
| Session | sessions | 1 | No | Authenticated user session |
| WorkspaceAccess | workspace_access | 2 | Yes | May be simplified by owner_user_id in MVP |
| Role | roles | 3 | Optional | Expansion RBAC table |
| Permission | permissions | 3 | Optional | Expansion RBAC table |
| RolePermission | role_permissions | 3 | Optional | Join table for RBAC |

MVP simplification:

```text
company_workspaces.owner_user_id may represent owner access before full workspace_access and RBAC implementation.
```

---

# 6. Workspace Mapping

| Domain Entity | Table | Priority | Workspace Scoped | Notes |
|---|---|---:|---|---|
| CompanyWorkspace | company_workspaces | 1 | Root | Root tenant / company boundary |
| WorkspaceSettings | workspace_settings | 1 | Yes | One settings record per workspace |
| WorkspaceMember | workspace_members | 3 | Yes | May be replaced by workspace_access later |
| WorkspaceProfile | company_workspaces or workspace_profiles | 2 | Yes | MVP may store profile fields directly on company_workspaces |
| WorkspaceContext | Derived view | 1 | Yes | Usually assembled dynamically, not stored as table |

Recommended MVP:

```text
company_workspaces
workspace_settings
```

---

# 7. Operating Map Mapping

| Domain Entity | Table | Priority | Workspace Scoped | Notes |
|---|---|---:|---|---|
| OperatingMap | operating_maps | 1 | Yes | Active operating map for workspace |
| OperatingMapNode | operating_map_nodes | 3 | Yes | Optional graph-style structure |
| OperatingGap | operating_gaps | 1 | Yes | Missing or weak operating area |
| OperatingRecommendation | operating_recommendations | 2 | Yes | Suggested actions from map or gap analysis |
| SuggestedFunction | functions or operating_recommendations | 1 | Yes | MVP may create suggested functions directly with status |
| SuggestedTask | tasks or operating_recommendations | 1 | Yes | MVP may create suggested tasks directly with status |
| SuggestedAgent | agents or operating_recommendations | 2 | Yes | Optional until Agent runtime is implemented |

MVP simplification:

```text
operating_map_nodes can be postponed if operating_maps, operating_gaps and functions are enough.
```

---

# 8. Function and Responsibility Mapping

| Domain Entity | Table | Priority | Workspace Scoped | Notes |
|---|---|---:|---|---|
| Function | functions | 1 | Yes | Business function or operating area |
| Responsibility | responsibilities | 1 | Yes | Ownership of function, process, task or decision |
| ResponsibilityAssignment | responsibility_assignments | 3 | Yes | May be represented by responsibilities + audit_events |
| OwnershipGap | ownership_gaps | 2 | Yes | May overlap with operating_gaps; useful for explicit ownership tracking |
| FunctionCategory | enum or reference table | 2 | Optional | MVP may use enum-like text |
| ResponsibilityScope | JSONB or table | 3 | Yes | Expansion detail |

Recommended MVP:

```text
functions
responsibilities
```

Optional near-MVP:

```text
ownership_gaps
```

---

# 9. Agent Mapping

| Domain Entity | Table | Priority | Workspace Scoped | Notes |
|---|---|---:|---|---|
| Agent | agents | 2 | Yes | Governed AI agent role |
| AgentAuthorityScope | agent_authority_scopes | 2 | Yes | Defines allowed and restricted actions |
| AgentRecommendation | agent_recommendations | 2 | Yes | Reviewable AI recommendation |
| AgentActionDraft | agent_action_drafts | 2 | Yes | Draft output prepared by agent |
| AgentEscalationRule | agent_escalation_rules | 3 | Yes | Expansion rules engine |
| AgentContextScope | JSONB or table | 3 | Yes | Expansion detail |
| AgentRole | enum or reference table | 3 | Optional | MVP may use text role field |

Recommended governed AI tables:

```text
agents
agent_authority_scopes
agent_recommendations
agent_action_drafts
```

---

# 10. Process Mapping

| Domain Entity | Table | Priority | Workspace Scoped | Notes |
|---|---|---:|---|---|
| Process | processes | 2 | Yes | Repeatable business process |
| ProcessStep | process_steps | 2 | Yes | Ordered process step |
| ProcessInput | process_inputs | 3 | Yes | Optional normalized table |
| ProcessOutput | process_outputs | 3 | Yes | Optional normalized table |
| ProcessGap | process_gaps | 3 | Yes | May be represented by operating_gaps or tasks |
| ProcessReview | process_reviews | 3 | Yes | Expansion process improvement table |

MVP simplification:

```text
process_inputs and process_outputs may start as JSONB fields on processes.
```

---

# 11. Task Mapping

| Domain Entity | Table | Priority | Workspace Scoped | Notes |
|---|---|---:|---|---|
| Task | tasks | 1 | Yes | Core actionable work item |
| TaskLink | task_links | 3 | Yes | MVP may use direct FK fields first |
| TaskHistory | task_history | 3 | Yes | MVP may use audit_events |
| TaskComment | task_comments | 3 | Yes | Optional collaboration feature |
| TaskBlocker | task_blockers | 3 | Yes | MVP may use task.blocked_reason |
| TaskAssignment | task_assignments | 3 | Yes | MVP may use owner_user_id and audit_events |

Recommended MVP:

```text
tasks
```

The table should include direct references where useful:

```text
function_id
process_id
decision_id
agent_id
operating_gap_id
```

---

# 12. Decision Mapping

| Domain Entity | Table | Priority | Workspace Scoped | Notes |
|---|---|---:|---|---|
| Decision | decisions | 1 | Yes | Important business decision |
| DecisionOption | decision_options | 3 | Yes | MVP may store options as JSONB or text |
| DecisionRationale | decisions.rationale | 1 | Yes | MVP field on decisions |
| DecisionOutcome | decision_outcomes | 3 | Yes | Future learning and review |
| DecisionReview | decision_reviews | 3 | Yes | Future governance review |
| DecisionLink | decision_links | 3 | Yes | MVP may use direct references |

Recommended MVP:

```text
decisions
```

---

# 13. Memory Mapping

| Domain Entity | Table | Priority | Workspace Scoped | Notes |
|---|---|---:|---|---|
| MemoryEntry | memory_entries | 1 | Yes | Reusable enterprise memory |
| MemorySource | memory_sources | 3 | Yes | MVP may use source fields on memory_entries |
| MemoryLink | memory_links | 3 | Yes | Optional object relationship table |
| MemoryReview | memory_reviews | 3 | Yes | Future validation table |
| MemoryUsage | memory_usage | 3 | Yes | MVP may use audit_events |
| MemoryTag | memory_tags | 3 | Yes | Optional tag normalization |

Recommended MVP:

```text
memory_entries
```

Core source fields:

```text
source_object_type
source_object_id
```

---

# 14. Audit and Event Mapping

| Domain Entity | Table | Priority | Workspace Scoped | Notes |
|---|---|---:|---|---|
| AuditEvent | audit_events | 1 | Yes | Evidence of governed action |
| RuntimeEvent | runtime_events | 1 | Yes | Meaningful state change |
| AuditExport | audit_exports | 3 | Yes | May be covered by export_jobs |
| EventCorrelation | runtime_events.correlation_id | 2 | Yes | MVP field on runtime_events |
| EventFailure | event_failures | 3 | Yes | MVP may use runtime_events.status and error_message |

Recommended MVP:

```text
audit_events
runtime_events
```

---

# 15. Integration Mapping

| Domain Entity | Table | Priority | Workspace Scoped | Notes |
|---|---|---:|---|---|
| Integration | integrations | 2 | Yes | External system connection |
| IntegrationScope | integration_scopes | 3 | Yes | MVP may store scopes as JSONB |
| IntegrationCredentialReference | integration_credential_references | 3 | Yes | MVP may use credential_ref field on integrations |
| IntegrationSyncJob | integration_sync_jobs | 2 | Yes | Sync execution record |
| IntegrationMapping | integration_mappings | 3 | Yes | Future provider mapping |

Recommended governed integration tables:

```text
integrations
integration_sync_jobs
```

---

# 16. Security Mapping

| Domain Entity | Table | Priority | Workspace Scoped | Notes |
|---|---|---:|---|---|
| SecurityPolicy | security_policies | 2 | Yes | Security rules and AI context policy |
| WorkspaceAccess | workspace_access | 2 | Yes | User access to workspace |
| Role | roles | 3 | Optional | Expansion RBAC |
| Permission | permissions | 3 | Optional | Expansion RBAC |
| SecurityEvent | security_events | 3 | Yes | MVP may use audit_events and runtime_events |
| CredentialReference | external secret store reference | 2 | Yes | Do not store raw secrets |

MVP simplification:

```text
company_workspaces.owner_user_id + audit_events can cover basic owner access until full RBAC is needed.
```

---

# 17. Dashboard Mapping

| Domain Entity | Table | Priority | Workspace Scoped | Notes |
|---|---|---:|---|---|
| DashboardMetric | dashboard_metrics | 1 | Yes | Calculated operating indicator |
| DashboardSnapshot | dashboard_snapshots | 3 | Yes | Optional point-in-time dashboard view |
| DashboardInsight | dashboard_insights | 3 | Yes | AI or system-generated insight |
| DashboardAlert | dashboard_alerts | 3 | Yes | Optional warning table |
| DashboardWidget | dashboard_widgets | 3 | Yes | Future configurable UI |

Recommended MVP:

```text
dashboard_metrics
```

MVP may also compute dashboard views dynamically before persisting many metrics.

---

# 18. Export Mapping

| Domain Entity | Table | Priority | Workspace Scoped | Notes |
|---|---|---:|---|---|
| ExportJob | export_jobs | 2 | Yes | Controlled export request |
| ExportTemplate | export_templates | 3 | Yes or Global | MVP may use hardcoded templates |
| ExportFile | export_files | 3 | Yes | MVP may store file_reference on export_jobs |
| ExportScope | export_jobs.export_scope | 2 | Yes | JSONB or structured text |

Recommended MVP:

```text
export_jobs
```

---

# 19. Canonical MVP Table Set

Priority 1 tables:

```text
users
sessions
company_workspaces
workspace_settings
operating_maps
operating_gaps
functions
responsibilities
tasks
decisions
memory_entries
audit_events
runtime_events
dashboard_metrics
```

These tables support:

```text
Create Workspace
↓
Generate Operating Map
↓
Confirm Functions
↓
Assign Responsibilities
↓
Create Tasks
↓
Log Decisions
↓
Create Memory
↓
Record Audit and Events
↓
Show Dashboard
```

---

# 20. Governed Runtime Table Set

Priority 2 tables:

```text
agents
agent_authority_scopes
agent_recommendations
agent_action_drafts
processes
process_steps
integrations
integration_sync_jobs
security_policies
workspace_access
export_jobs
ownership_gaps
operating_recommendations
```

These tables support:

```text
Governed AI assistance
Process definition
Integration management
Security policies
Controlled exports
Expanded traceability
```

---

# 21. Expansion Table Set

Priority 3 tables:

```text
roles
permissions
role_permissions
workspace_members
operating_map_nodes
responsibility_assignments
process_inputs
process_outputs
process_reviews
task_links
task_history
task_comments
decision_options
decision_outcomes
memory_links
memory_reviews
memory_usage
security_events
dashboard_snapshots
dashboard_insights
dashboard_alerts
export_templates
export_files
```

These should be added only when product behavior requires them.

---

# 22. Mapping Rules

## Rule 1 — Aggregate Roots Become Primary Tables

Every aggregate root should have a primary table.

## Rule 2 — Supporting Entities May Be Deferred

Supporting entities can start as fields or JSONB if not required by MVP workflows.

## Rule 3 — All Operating Tables Need workspace_id

This protects tenant isolation and query clarity.

## Rule 4 — Recommendations and Drafts Must Not Be Hidden

AI-generated suggestions must be persisted as reviewable objects where they affect operations.

## Rule 5 — Audit and Runtime Events Are Not Optional

They are required for trust, traceability and product debugging.

---

# 23. Tables to Avoid in MVP

Avoid creating too early:

```text
complex RBAC tables
workflow automation tables
advanced dashboard widget tables
full process mining tables
external analytics warehouse tables
multi-tenant enterprise hierarchy tables
billing and subscription tables
```

These may distract from the first runnable vertical slice.

---

# 24. Mapping Acceptance Criteria

Entity to Table Mapping is ready when:

- every core Domain Model entity has a table decision;
- MVP priority is clear;
- workspace scoping is identified;
- aggregate roots map to primary tables;
- deferred supporting entities are documented;
- mapping supports next Data Model documents;
- mapping does not overbuild beyond MVP needs.

Status:

```text
Accepted for Core Table Design
```

---

# 25. Final Entity to Table Mapping Statement

```text
Bizzi Entity to Table Mapping translates the canonical Domain Model into an implementation-ready database table plan, preserving workspace scope, aggregate boundaries, AI governance, traceability, auditability and MVP delivery discipline.
```

This document becomes the reference for defining core tables, relationships, enums and indexes in the rest of the `27_DATA_MODEL` layer.