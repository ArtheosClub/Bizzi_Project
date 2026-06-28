# 02_WORKSPACE_DOMAIN.md

# Bizzi Platform

## Workspace Domain

**Layer:** 26_DOMAIN_MODEL  
**Component Type:** Domain Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 03_WORKSPACE_RUNTIME.md  
**Previous Documents:** 00_DOMAIN_MODEL_VISION.md, 01_ENTITY_CATALOG.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Workspace Domain for Bizzi Platform.

The Workspace Domain describes the core business objects, rules and relationships that represent a company operating inside Bizzi.

Core question:

```text
How does Bizzi represent a company workspace as the root domain boundary for all operating objects, AI assistance, memory, audit and execution?
```

---

# 2. Domain Role

The Workspace Domain is the root domain of Bizzi.

It provides the boundary for:

- company identity;
- ownership;
- workspace settings;
- runtime object scoping;
- AI context;
- memory;
- audit;
- integrations;
- dashboard visibility;
- exports;
- future collaboration.

No major operating object should exist outside a workspace.

---

# 3. Domain Principle

```text
Workspace First
```

Every meaningful operating object in Bizzi must belong to a `CompanyWorkspace` unless explicitly defined as global platform metadata.

This principle protects:

- isolation;
- security;
- auditability;
- traceability;
- future multi-company scalability;
- clean data modeling;
- reliable AI context scoping.

---

# 4. Aggregate Boundary

Primary aggregate root:

```text
CompanyWorkspace
```

Entities inside or directly attached to the Workspace aggregate:

```text
WorkspaceSettings
WorkspaceMember
WorkspaceProfile
WorkspaceContext
WorkspaceStatus
```

Related external entities:

```text
User
OperatingMap
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
ExportJob
DashboardMetric
SecurityPolicy
```

---

# 5. Core Entities

## 5.1 CompanyWorkspace

Represents one company operating inside Bizzi.

Minimum domain attributes:

```text
id
name
slug
industry
business_type
company_size
owner_user_id
status
created_at
updated_at
```

Optional domain attributes:

```text
country
language
timezone
default_currency
website
operating_pain_points
control_level
ai_usage_level
onboarding_status
```

Domain responsibility:

```text
CompanyWorkspace defines the root boundary for all company operating state.
```

---

## 5.2 WorkspaceSettings

Represents workspace configuration.

Minimum domain attributes:

```text
id
workspace_id
language
timezone
default_currency
ai_assistance_enabled
memory_enabled
audit_enabled
created_at
updated_at
```

Domain responsibility:

```text
WorkspaceSettings controls default runtime behavior inside the workspace.
```

---

## 5.3 WorkspaceMember

Represents a user’s relationship to a workspace.

MVP status:

```text
Expansion entity
```

Minimum future attributes:

```text
id
workspace_id
user_id
role
status
created_at
updated_at
```

Domain responsibility:

```text
WorkspaceMember enables future multi-user collaboration and access control.
```

MVP simplification:

```text
The owner user acts as the only effective workspace member.
```

---

## 5.4 WorkspaceProfile

Represents structured company profile context.

This may be implemented as fields on `CompanyWorkspace` in MVP and separated later if needed.

Potential attributes:

```text
workspace_id
company_description
industry
business_model
primary_customers
main_products_or_services
main_operating_challenges
strategic_goals
```

Domain responsibility:

```text
WorkspaceProfile provides structured business context for operating map generation and AI assistance.
```

---

## 5.5 WorkspaceContext

Represents assembled runtime context for services and AI orchestration.

This is usually a derived object, not necessarily a persisted aggregate.

Context may include:

```text
workspace profile
settings
operating map summary
functions
ownership gaps
active tasks
recent decisions
relevant memory
active agents
integration status
audit summary
```

Domain responsibility:

```text
WorkspaceContext provides scoped and structured context to runtime services and AI components.
```

---

# 6. Workspace Lifecycle

Recommended lifecycle:

```text
created
↓
initialized
↓
onboarding
↓
active
↓
paused
↓
archived
```

MVP lifecycle:

```text
created
onboarding
active
archived
```

---

# 7. State Definitions

## created

Workspace record exists but is not yet ready for operational use.

## onboarding

Workspace exists and business intake or setup is in progress.

## active

Workspace is operational and may contain runtime objects.

## paused

Workspace is temporarily inactive. Future state.

## archived

Workspace is retained historically but normal runtime actions are blocked.

---

# 8. Domain Relationships

## 8.1 User to CompanyWorkspace

```text
User owns CompanyWorkspace
```

MVP cardinality:

```text
User 1 → many CompanyWorkspace later
User 1 → 1 CompanyWorkspace for MVP if needed
```

## 8.2 CompanyWorkspace to WorkspaceSettings

```text
CompanyWorkspace 1 → 1 WorkspaceSettings
```

## 8.3 CompanyWorkspace to Operating Objects

```text
CompanyWorkspace 1 → many Functions
CompanyWorkspace 1 → many Agents
CompanyWorkspace 1 → many Processes
CompanyWorkspace 1 → many Tasks
CompanyWorkspace 1 → many Decisions
CompanyWorkspace 1 → many MemoryEntries
CompanyWorkspace 1 → many AuditEvents
CompanyWorkspace 1 → many RuntimeEvents
CompanyWorkspace 1 → many Integrations
CompanyWorkspace 1 → many ExportJobs
CompanyWorkspace 1 → many DashboardMetrics
```

---

# 9. Domain Invariants

The Workspace Domain must enforce:

```text
CompanyWorkspace must have an owner_user_id.
CompanyWorkspace must have a valid status.
WorkspaceSettings must belong to one CompanyWorkspace.
Runtime objects must reference workspace_id.
Archived workspaces cannot accept normal operating actions.
AI context must be scoped to one workspace.
Exports must be scoped to one workspace.
Audit and memory must be scoped to one workspace.
```

---

# 10. Ownership Rules

MVP ownership model:

```text
Workspace has one owner.
Owner has full MVP access to the workspace.
Owner confirms sensitive AI-generated outputs.
Owner may archive the workspace.
Owner is accountable for workspace-level configuration.
```

Future model:

```text
Workspace may have multiple members.
Members may have roles and permissions.
Ownership may be transferred.
Auditor or viewer roles may exist.
```

---

# 11. Workspace Settings Rules

Default MVP settings:

```text
ai_assistance_enabled: true
memory_enabled: true
audit_enabled: true
```

Rules:

```text
Audit should not be disabled for governed runtime actions in MVP.
Memory may be limited but must preserve important confirmed objects.
AI assistance must never bypass security or audit boundaries.
```

---

# 12. Workspace Context Rules

Workspace context must be:

- scoped;
- structured;
- minimized for purpose;
- safe for AI use;
- traceable to source objects where applicable.

AI context rule:

```text
AI may only receive context from the current workspace and only what is required for the operation.
```

---

# 13. Workspace Events

Workspace Domain should support these domain events:

```text
workspace.created
workspace.initialized
workspace.profile_updated
workspace.settings_updated
workspace.owner_assigned
workspace.status_changed
workspace.archived
workspace.context_loaded
```

These events support runtime audit, memory and dashboard updates.

---

# 14. Workspace Audit Requirements

Audited actions:

```text
workspace.created
workspace.profile_updated
workspace.settings_updated
workspace.owner_assigned
workspace.status_changed
workspace.archived
workspace.access_denied
```

Audit must answer:

```text
Who changed the workspace, what changed, when, and what workspace was affected?
```

---

# 15. Workspace Memory Requirements

Workspace Domain may create memory from:

- company profile;
- business goals;
- operating pain points;
- onboarding context;
- workspace-level decisions;
- major profile changes.

Memory types:

```text
company_context
owner_goal
operating_pain_point
workspace_profile
workspace_change
```

---

# 16. Workspace Dashboard Requirements

Dashboard should show workspace-level context:

- workspace name;
- status;
- onboarding status;
- active functions;
- ownership gaps;
- open tasks;
- recent decisions;
- memory count;
- audit activity;
- active agents;
- integration status.

Dashboard question:

```text
What is the operating state of this company workspace right now?
```

---

# 17. Workspace Security Requirements

Security requirements:

```text
User must be authenticated before workspace access.
User must have workspace access before reading workspace objects.
All workspace objects must be filtered by workspace_id.
Archived workspace cannot be modified through normal runtime flows.
Workspace exports require authorization.
AI context must not include data from another workspace.
```

---

# 18. MVP Domain Behavior

MVP should support:

```text
Create workspace
Store workspace profile
Create default settings
Assign owner
Move workspace into onboarding
Move workspace into active state
Load workspace context
Scope runtime objects to workspace_id
Record audit events
Create initial memory
Show workspace dashboard baseline
```

---

# 19. Out of Scope for MVP

The Workspace Domain does not need in MVP:

- multi-member collaboration;
- workspace transfer;
- multiple organizations;
- billing ownership;
- enterprise SSO;
- workspace marketplace;
- cross-workspace reporting;
- complex tenant hierarchy.

---

# 20. Data Model Implications

Future Data Model should include tables or collections for:

```text
users
sessions
company_workspaces
workspace_settings
workspace_members
```

Most other tables should include:

```text
workspace_id
```

Recommended indexes later:

```text
company_workspaces.owner_user_id
company_workspaces.slug
workspace_settings.workspace_id
workspace_members.workspace_id
workspace_members.user_id
```

---

# 21. API Implications

Future API contracts should support:

```text
POST /workspaces
GET /workspaces/{workspace_id}
PATCH /workspaces/{workspace_id}
GET /workspaces/{workspace_id}/context
PATCH /workspaces/{workspace_id}/settings
POST /workspaces/{workspace_id}/archive
```

MVP may start with a reduced API surface.

---

# 22. Traceability Pattern

Workspace traceability chain:

```text
User
↓
CompanyWorkspace
↓
Runtime Object
↓
Runtime Event
↓
Audit Event
↓
Memory Entry
↓
Dashboard Metric
```

This chain should be preserved across future layers.

---

# 23. Acceptance Criteria

Workspace Domain is ready when:

- CompanyWorkspace is defined as aggregate root;
- workspace ownership is clear;
- settings are defined;
- lifecycle is defined;
- workspace scoping rules are explicit;
- domain events are defined;
- audit and memory behavior are defined;
- MVP simplifications are clear;
- data model and API implications are identified.

Status:

```text
Ready for Data Model and API Design
```

---

# 24. Architecture Alignment

| Workspace Domain Area | Reference |
|---|---|
| CompanyWorkspace | 03_WORKSPACE_RUNTIME.md |
| WorkspaceSettings | 12_RUNTIME_SECURITY.md / 03_WORKSPACE_RUNTIME.md |
| WorkspaceMember | Runtime Security |
| Workspace Context | Runtime Architecture |
| Workspace Events | Event Runtime |
| Workspace Audit | Audit Runtime |
| Workspace Memory | Memory Runtime |
| Workspace Dashboard | Core User Journey |

---

# 25. Final Workspace Domain Statement

```text
Workspace Domain defines the company workspace as the root business boundary of Bizzi, ensuring that every operating object, AI context, memory entry, audit event, integration and dashboard indicator is scoped, governed and traceable.
```

This domain is the foundation for all other Bizzi product domains.