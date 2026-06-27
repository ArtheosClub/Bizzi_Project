# 03_WORKSPACE_RUNTIME.md

# Bizzi Platform

## Workspace Runtime

**Layer:** 25_RUNTIME_PLATFORM  
**Component Type:** Runtime Component Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 00_RUNTIME_VISION.md, 01_RUNTIME_ARCHITECTURE.md, 02_CORE_RUNTIME_COMPONENTS.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Workspace Runtime for Bizzi Platform.

The Workspace Runtime is the root execution container for a company inside Bizzi. It creates the business environment where users, functions, responsibilities, agents, tasks, decisions, memory, audit events and dashboards exist.

Core question:

```text
How does Bizzi create and manage the company workspace as the runtime foundation of the enterprise operating system?
```

---

# 2. Runtime Role

The Workspace Runtime provides the first durable boundary of the product.

It answers:

```text
Which company is this?
Who owns it?
What context belongs to it?
Which runtime objects are inside it?
What permissions apply to it?
What state is it in?
```

No meaningful Bizzi runtime object should exist outside a workspace.

---

# 3. Workspace Runtime Principle

```text
Workspace First
```

Every core runtime object must be scoped to a `CompanyWorkspace`.

This ensures:

- isolation;
- ownership;
- traceability;
- auditability;
- memory boundaries;
- dashboard boundaries;
- future multi-company scalability.

---

# 4. Primary Runtime Objects

Minimum objects:

```text
CompanyWorkspace
WorkspaceMember
WorkspaceSettings
WorkspaceProfile
WorkspaceStatus
WorkspaceContext
```

Supporting objects:

```text
User
Role
Permission
AuditEvent
MemoryEntry
DashboardMetric
RuntimeEvent
```

---

# 5. CompanyWorkspace Object

## Purpose

Represents one company operating inside Bizzi.

## Minimum Fields

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

## Optional Fields

```text
country
language
timezone
website
operating_pain_points
control_level
ai_usage_level
```

---

# 6. Workspace Lifecycle

```text
Created
↓
Initialized
↓
Onboarding
↓
Active
↓
Paused
↓
Archived
```

## Created

Workspace record exists but has not completed initialization.

## Initialized

Basic metadata and owner relationship are established.

## Onboarding

Business intake is in progress.

## Active

Workspace is operational and can contain runtime objects.

## Paused

Workspace is temporarily inactive.

## Archived

Workspace is retained for history but no longer active.

---

# 7. Workspace States

```text
created
initialized
onboarding
active
paused
archived
```

MVP required states:

```text
created
onboarding
active
archived
```

---

# 8. Core Operations

## 8.1 Create Workspace

Creates the company workspace and links it to the owner user.

Inputs:

- user_id;
- company_name;
- business_type;
- company_size;
- industry.

Outputs:

- CompanyWorkspace;
- workspace.created event;
- audit event.

## 8.2 Initialize Workspace

Sets basic settings and prepares the workspace for onboarding.

## 8.3 Update Workspace Profile

Updates company metadata.

## 8.4 Load Workspace Context

Provides context for onboarding, AI orchestration, dashboard and runtime services.

## 8.5 Archive Workspace

Moves workspace into archived state.

---

# 9. Workspace Membership Model

The MVP begins with a simple model:

```text
Owner
```

Future roles:

```text
Admin
Manager
Member
Viewer
Consultant
AgentOperator
```

The MVP should support role extensibility even if only Owner is implemented first.

---

# 10. Workspace Owner

The workspace owner is the accountable human for the company workspace.

Responsibilities:

- creates workspace;
- confirms onboarding outputs;
- approves AI-generated drafts;
- owns workspace data;
- can archive workspace;
- is accountable for AI-supported operating model.

---

# 11. Workspace Settings

Minimum settings:

```text
workspace_id
language
timezone
default_currency
ai_assistance_enabled
audit_enabled
memory_enabled
```

MVP defaults:

```text
ai_assistance_enabled: true
audit_enabled: true
memory_enabled: true
```

---

# 12. Workspace Context

Workspace context is the structured information passed to runtime services and AI orchestration.

Includes:

- company profile;
- industry;
- company size;
- pain points;
- confirmed functions;
- ownership gaps;
- active agents;
- open tasks;
- recent decisions;
- memory summaries.

The context must be structured, not only free text.

---

# 13. Workspace Initialization Flow

```text
User signs up
↓
User creates workspace
↓
Workspace profile saved
↓
Owner assigned
↓
Workspace settings initialized
↓
workspace.created event emitted
↓
Audit event recorded
↓
Initial memory created
↓
Onboarding starts
```

---

# 14. Workspace Events

Minimum events:

```text
workspace.created
workspace.initialized
workspace.profile_updated
workspace.owner_assigned
workspace.status_changed
workspace.archived
workspace.context_loaded
```

Events must include:

```text
event_id
workspace_id
actor_id
event_type
timestamp
payload
```

---

# 15. Workspace Audit Requirements

Audit events are required for:

- workspace creation;
- owner assignment;
- workspace profile changes;
- status changes;
- archive action;
- permission changes.

Audit question:

```text
Who changed the workspace state or profile, when, and what changed?
```

---

# 16. Workspace Memory Integration

Workspace Runtime should create initial memory entries from:

- company profile;
- business type;
- operating pain points;
- owner goals;
- onboarding context.

Memory types:

```text
company_context
owner_goal
operating_pain_point
workspace_profile
```

Memory must remain linked to the workspace and source object.

---

# 17. Workspace Dashboard Integration

Workspace Runtime provides the dashboard baseline.

Dashboard inputs:

- workspace name;
- status;
- onboarding status;
- number of functions;
- number of ownership gaps;
- number of tasks;
- number of decisions;
- number of memory entries;
- recent audit activity.

The workspace dashboard must never open as an empty shell after onboarding begins.

---

# 18. Workspace Security Boundary

Workspace Runtime defines the first access boundary.

Rules:

```text
A user may access only workspaces where membership exists.
A workspace owner has full MVP access.
Runtime objects must include workspace_id.
AI context must be scoped to workspace_id.
Exports must be scoped to workspace_id.
Audit events must be scoped to workspace_id.
```

---

# 19. Workspace Isolation

Workspace isolation is essential for future multi-tenant architecture.

Every core table or collection should include:

```text
workspace_id
```

This applies to:

- functions;
- responsibilities;
- agents;
- processes;
- tasks;
- decisions;
- memory entries;
- audit events;
- dashboard metrics;
- runtime events.

---

# 20. Workspace API Boundary

Suggested API group:

```text
/workspaces
```

Minimum endpoints:

```text
POST /workspaces
GET /workspaces/{workspace_id}
PATCH /workspaces/{workspace_id}
POST /workspaces/{workspace_id}/archive
GET /workspaces/{workspace_id}/context
```

Future endpoints:

```text
GET /workspaces
POST /workspaces/{workspace_id}/members
PATCH /workspaces/{workspace_id}/settings
GET /workspaces/{workspace_id}/audit
GET /workspaces/{workspace_id}/memory
```

---

# 21. Workspace Service Responsibilities

`WorkspaceService` responsibilities:

- create workspace;
- validate workspace ownership;
- update workspace profile;
- initialize workspace settings;
- load workspace context;
- change workspace status;
- archive workspace;
- emit workspace events;
- trigger audit recording;
- trigger initial memory creation.

---

# 22. Workspace Data Validation

Required validation:

- company name is required;
- owner user is required;
- workspace status must be valid;
- workspace slug must be unique within tenant boundary;
- archived workspace cannot accept normal runtime actions;
- user must have access to workspace before reading context.

---

# 23. MVP Acceptance Criteria

Workspace Runtime is MVP-ready when:

- user can create a company workspace;
- workspace is linked to owner;
- workspace profile is stored;
- workspace status is tracked;
- workspace context can be loaded;
- audit event is recorded on creation;
- initial company context memory can be created;
- other runtime objects can be scoped to workspace_id;
- dashboard can display workspace baseline.

---

# 24. Out of Scope for MVP

The MVP does not require:

- multi-workspace switching;
- complex team roles;
- enterprise SSO;
- billing plans per workspace;
- organization-level administration;
- cross-workspace analytics;
- workspace marketplace;
- external workspace integrations.

---

# 25. Architecture Alignment

| Workspace Runtime Area | Architecture Reference |
|---|---|
| CompanyWorkspace | Enterprise Foundation |
| Workspace Owner | Governance Baseline |
| Workspace Context | Product Vision / Core User Journey |
| Workspace Events | Runtime Architecture |
| Workspace Memory | Enterprise Memory |
| Workspace Audit | Observability and Intelligence |
| Workspace Security | Security / Governance Baseline |
| Workspace Dashboard | Value Proposition / Core User Journey |

---

# 26. Final Workspace Runtime Statement

```text
Workspace Runtime is the root execution container of Bizzi Platform. It defines where the company exists, who owns it, what context belongs to it, and how all runtime objects remain scoped, governed, auditable and ready for product execution.
```

This component is the foundation for all subsequent Runtime Platform components.