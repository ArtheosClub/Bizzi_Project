# 01_ENTITY_CATALOG.md

# Bizzi Platform

## Entity Catalog

**Layer:** 26_DOMAIN_MODEL  
**Component Type:** Domain Entity Catalog  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Previous Document:** 00_DOMAIN_MODEL_VISION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the initial canonical entity catalog for Bizzi Platform.

It translates the Runtime Platform into a set of domain entities that can later become the basis for the data model, API contracts, backend services and frontend screens.

Core question:

```text
Which domain entities must exist for Bizzi to operate as a workspace-scoped, AI-assisted, auditable and memory-enabled enterprise operating system?
```

---

# 2. Catalog Role

The Entity Catalog is the first formal inventory of Bizzi domain objects.

It provides:

- entity names;
- entity purposes;
- entity categories;
- ownership boundaries;
- lifecycle relevance;
- relationships;
- MVP priority;
- alignment to Runtime Platform.

This catalog is not yet the database schema. It defines business meaning before implementation detail.

---

# 3. Entity Classification

Bizzi entities are grouped into the following domains:

```text
Identity Domain
Workspace Domain
Operating Map Domain
Function and Responsibility Domain
Agent Domain
Process Domain
Task Domain
Decision Domain
Memory Domain
Audit and Event Domain
Integration Domain
Security Domain
Dashboard Domain
Export Domain
```

---

# 4. Entity Priority Levels

## Priority 1 — MVP Core

Required for the first runnable vertical slice.

## Priority 2 — Governed Runtime

Needed for structured AI assistance, traceability and operational completeness.

## Priority 3 — Expansion

Useful after MVP or for advanced multi-user and enterprise scenarios.

---

# 5. Identity Domain Entities

## 5.1 User

**Purpose:** Represents a human identity in Bizzi.

**Priority:** 1  
**Aggregate:** User / Workspace Access  
**Runtime Reference:** Runtime Security, Workspace Runtime

Primary responsibilities:

- authenticate into Bizzi;
- own or access workspaces;
- confirm AI-generated outputs;
- create or modify runtime objects;
- appear as actor in audit events.

Key relationships:

```text
User → CompanyWorkspace
User → WorkspaceMember
User → AuditEvent
User → Task
User → Decision
```

---

## 5.2 Session

**Purpose:** Represents an authenticated user session.

**Priority:** 1  
**Aggregate:** User  
**Runtime Reference:** Runtime Security

Primary responsibilities:

- preserve authenticated state;
- expire access;
- support security events;
- protect runtime access.

Key relationships:

```text
Session → User
Session → SecurityEvent
```

---

# 6. Workspace Domain Entities

## 6.1 CompanyWorkspace

**Purpose:** Represents one company operating inside Bizzi.

**Priority:** 1  
**Aggregate Root:** CompanyWorkspace  
**Runtime Reference:** Workspace Runtime

Primary responsibilities:

- define the root boundary for operating state;
- scope all major runtime objects;
- preserve company context;
- provide workspace identity for dashboard and AI context.

Key relationships:

```text
CompanyWorkspace → WorkspaceSettings
CompanyWorkspace → WorkspaceMember
CompanyWorkspace → OperatingMap
CompanyWorkspace → Function
CompanyWorkspace → Agent
CompanyWorkspace → Process
CompanyWorkspace → Task
CompanyWorkspace → Decision
CompanyWorkspace → MemoryEntry
CompanyWorkspace → AuditEvent
CompanyWorkspace → RuntimeEvent
```

Invariant:

```text
No major runtime object may exist without workspace_id.
```

---

## 6.2 WorkspaceMember

**Purpose:** Represents a user’s membership in a workspace.

**Priority:** 3 for MVP, 1 for multi-user expansion  
**Aggregate:** CompanyWorkspace  
**Runtime Reference:** Workspace Runtime, Runtime Security

Primary responsibilities:

- link users to workspace;
- define access role;
- support future collaboration.

Key relationships:

```text
WorkspaceMember → User
WorkspaceMember → CompanyWorkspace
WorkspaceMember → Role
```

---

## 6.3 WorkspaceSettings

**Purpose:** Stores workspace-level configuration.

**Priority:** 1  
**Aggregate:** CompanyWorkspace  
**Runtime Reference:** Workspace Runtime, Runtime Security

Primary responsibilities:

- define language;
- define timezone;
- define default currency;
- enable or disable AI assistance;
- enable memory and audit behavior.

Key relationships:

```text
WorkspaceSettings → CompanyWorkspace
```

---

# 7. Operating Map Domain Entities

## 7.1 OperatingMap

**Purpose:** Represents the structured view of how the company operates.

**Priority:** 1  
**Aggregate Root:** OperatingMap  
**Runtime Reference:** Runtime Architecture, Core User Journey

Primary responsibilities:

- organize functions;
- expose operating gaps;
- connect business context to action;
- support first-hour value.

Key relationships:

```text
OperatingMap → CompanyWorkspace
OperatingMap → Function
OperatingMap → OperatingGap
OperatingMap → Task
OperatingMap → Agent
```

---

## 7.2 OperatingGap

**Purpose:** Represents a missing, weak or unclear operating area.

**Priority:** 1  
**Aggregate:** OperatingMap  
**Runtime Reference:** Runtime Architecture, Task Runtime

Primary responsibilities:

- identify missing ownership;
- identify missing function or process;
- trigger suggested tasks;
- support dashboard insights.

Key relationships:

```text
OperatingGap → OperatingMap
OperatingGap → Function
OperatingGap → Task
OperatingGap → MemoryEntry
```

---

# 8. Function and Responsibility Domain Entities

## 8.1 Function

**Purpose:** Represents a business function inside the company.

**Priority:** 1  
**Aggregate Root:** Function  
**Runtime Reference:** Core Runtime Components

Primary responsibilities:

- define functional areas;
- connect responsibilities;
- group processes, tasks and agents;
- support operating map and dashboard.

Key relationships:

```text
Function → CompanyWorkspace
Function → Responsibility
Function → Agent
Function → Process
Function → Task
Function → Decision
```

---

## 8.2 Responsibility

**Purpose:** Represents ownership or accountability for a function, task or process.

**Priority:** 1  
**Aggregate:** Function / Task / Process  
**Runtime Reference:** Responsibility Runtime

Primary responsibilities:

- assign human accountability;
- detect ownership gaps;
- support escalation;
- connect governance to execution.

Key relationships:

```text
Responsibility → User
Responsibility → Function
Responsibility → Process
Responsibility → Task
Responsibility → AuditEvent
```

Invariant:

```text
Every active operational area should have a clear owner or explicit ownership gap.
```

---

# 9. Agent Domain Entities

## 9.1 Agent

**Purpose:** Represents a governed AI agent role inside a workspace.

**Priority:** 2  
**Aggregate Root:** Agent  
**Runtime Reference:** Agent Runtime

Primary responsibilities:

- assist assigned function or process;
- generate recommendations;
- draft tasks, decisions or memory candidates;
- operate within human ownership and authority scope.

Key relationships:

```text
Agent → CompanyWorkspace
Agent → User
Agent → Function
Agent → Process
Agent → AgentAuthorityScope
Agent → MemoryEntry
Agent → AuditEvent
```

Invariant:

```text
Every active agent must have a human owner.
```

---

## 9.2 AgentAuthorityScope

**Purpose:** Defines what an agent may and may not do.

**Priority:** 2  
**Aggregate:** Agent  
**Runtime Reference:** Agent Runtime, Runtime Security

Primary responsibilities:

- define allowed actions;
- define restricted actions;
- preserve governance boundaries;
- support audit and security.

Key relationships:

```text
AgentAuthorityScope → Agent
AgentAuthorityScope → AuditEvent
```

---

# 10. Process Domain Entities

## 10.1 Process

**Purpose:** Represents a repeatable business process.

**Priority:** 2  
**Aggregate Root:** Process  
**Runtime Reference:** Process Runtime

Primary responsibilities:

- describe recurring work;
- define purpose and steps;
- link to function and owner;
- create tasks and memory.

Key relationships:

```text
Process → CompanyWorkspace
Process → Function
Process → User
Process → ProcessStep
Process → Task
Process → Decision
Process → MemoryEntry
```

---

## 10.2 ProcessStep

**Purpose:** Represents a step in a lightweight process definition.

**Priority:** 2  
**Aggregate:** Process  
**Runtime Reference:** Process Runtime

Primary responsibilities:

- preserve ordered process behavior;
- support process documentation;
- support later workflow design.

Key relationships:

```text
ProcessStep → Process
```

---

# 11. Task Domain Entities

## 11.1 Task

**Purpose:** Represents actionable work inside a workspace.

**Priority:** 1  
**Aggregate Root:** Task  
**Runtime Reference:** Task Runtime

Primary responsibilities:

- capture work to be done;
- assign owner;
- track status;
- link work to gaps, functions, processes, decisions or agents;
- feed dashboard.

Key relationships:

```text
Task → CompanyWorkspace
Task → User
Task → Function
Task → Process
Task → Decision
Task → Agent
Task → MemoryEntry
Task → AuditEvent
```

Invariant:

```text
Important work should not exist only in chat; it should become a task or decision.
```

---

# 12. Decision Domain Entities

## 12.1 Decision

**Purpose:** Represents an important business decision and its rationale.

**Priority:** 1  
**Aggregate Root:** Decision  
**Runtime Reference:** Decision Runtime

Primary responsibilities:

- capture decision context;
- capture final decision;
- capture rationale;
- generate follow-up tasks;
- create decision memory.

Key relationships:

```text
Decision → CompanyWorkspace
Decision → User
Decision → Function
Decision → Process
Decision → Task
Decision → Agent
Decision → MemoryEntry
Decision → AuditEvent
```

Invariant:

```text
Every confirmed decision must have an owner and final decision content.
```

---

# 13. Memory Domain Entities

## 13.1 MemoryEntry

**Purpose:** Represents reusable enterprise memory.

**Priority:** 1  
**Aggregate Root:** MemoryEntry  
**Runtime Reference:** Memory Runtime

Primary responsibilities:

- preserve useful context;
- link to source object;
- support AI context retrieval;
- support dashboard knowledge indicators.

Key relationships:

```text
MemoryEntry → CompanyWorkspace
MemoryEntry → Function
MemoryEntry → Agent
MemoryEntry → Process
MemoryEntry → Task
MemoryEntry → Decision
MemoryEntry → AuditEvent
```

Invariant:

```text
Active memory should have source traceability or explicit manual origin.
```

---

# 14. Audit and Event Domain Entities

## 14.1 AuditEvent

**Purpose:** Represents evidence of a governed runtime action.

**Priority:** 1  
**Aggregate Root:** AuditEvent  
**Runtime Reference:** Audit Runtime

Primary responsibilities:

- record actor;
- record action;
- record target object;
- record timestamp;
- preserve AI assistance and human confirmation where applicable.

Key relationships:

```text
AuditEvent → CompanyWorkspace
AuditEvent → User
AuditEvent → Agent
AuditEvent → RuntimeEvent
```

Invariant:

```text
Every audit event must identify actor, action, target and timestamp.
```

---

## 14.2 RuntimeEvent

**Purpose:** Represents a meaningful runtime state change.

**Priority:** 1  
**Aggregate Root:** RuntimeEvent  
**Runtime Reference:** Event Runtime

Primary responsibilities:

- coordinate internal updates;
- trigger audit, memory or dashboard handlers;
- preserve event traceability.

Key relationships:

```text
RuntimeEvent → CompanyWorkspace
RuntimeEvent → AuditEvent
RuntimeEvent → MemoryEntry
RuntimeEvent → DashboardMetric
```

---

# 15. Integration Domain Entities

## 15.1 Integration

**Purpose:** Represents an external system connected to a workspace.

**Priority:** 2  
**Aggregate Root:** Integration  
**Runtime Reference:** Integration Runtime

Primary responsibilities:

- define provider;
- define connection status;
- define scopes;
- manage integration lifecycle;
- support import and export.

Key relationships:

```text
Integration → CompanyWorkspace
Integration → IntegrationSyncJob
Integration → AuditEvent
Integration → RuntimeEvent
```

Invariant:

```text
Every active integration must have explicit scope.
```

---

## 15.2 IntegrationSyncJob

**Purpose:** Represents an import/export sync execution.

**Priority:** 2  
**Aggregate:** Integration  
**Runtime Reference:** Integration Runtime

Primary responsibilities:

- track sync status;
- record errors;
- preserve data movement traceability;
- feed audit and dashboard.

Key relationships:

```text
IntegrationSyncJob → Integration
IntegrationSyncJob → AuditEvent
RuntimeEvent
```

---

# 16. Security Domain Entities

## 16.1 SecurityPolicy

**Purpose:** Represents security and authorization rules for runtime behavior.

**Priority:** 2  
**Aggregate:** CompanyWorkspace / Runtime Security  
**Runtime Reference:** Runtime Security

Primary responsibilities:

- define security constraints;
- support access decisions;
- protect AI context and integrations;
- support future role and permission expansion.

Key relationships:

```text
SecurityPolicy → CompanyWorkspace
SecurityPolicy → Role
SecurityPolicy → Permission
```

---

## 16.2 Role

**Purpose:** Represents a named access role.

**Priority:** 3 for MVP, 2 for expansion  
**Aggregate:** SecurityPolicy  
**Runtime Reference:** Runtime Security

Primary responsibilities:

- group permissions;
- support workspace access;
- enable future collaboration.

Key relationships:

```text
Role → WorkspaceMember
Role → Permission
```

---

## 16.3 Permission

**Purpose:** Represents an allowed action or access category.

**Priority:** 3 for MVP, 2 for expansion  
**Aggregate:** SecurityPolicy  
**Runtime Reference:** Runtime Security

Primary responsibilities:

- define action boundaries;
- support authorization checks;
- preserve security clarity.

Key relationships:

```text
Permission → Role
Permission → SecurityPolicy
```

---

# 17. Dashboard Domain Entities

## 17.1 DashboardMetric

**Purpose:** Represents a calculated operating indicator.

**Priority:** 1  
**Aggregate:** Dashboard / CompanyWorkspace  
**Runtime Reference:** Dashboard Runtime, Core User Journey

Primary responsibilities:

- show operating state;
- expose tasks, gaps, decisions, agents and memory;
- support first-hour value.

Key relationships:

```text
DashboardMetric → CompanyWorkspace
DashboardMetric → Function
DashboardMetric → Task
DashboardMetric → Decision
DashboardMetric → MemoryEntry
RuntimeEvent
```

---

# 18. Export Domain Entities

## 18.1 ExportJob

**Purpose:** Represents a controlled export of workspace data.

**Priority:** 2  
**Aggregate Root:** ExportJob  
**Runtime Reference:** Export Runtime, Integration Runtime, Runtime Security

Primary responsibilities:

- generate shareable outputs;
- preserve export scope;
- record export activity;
- support audit trail.

Key relationships:

```text
ExportJob → CompanyWorkspace
ExportJob → User
ExportJob → AuditEvent
ExportJob → Integration
```

---

# 19. Cross-Entity Traceability Pattern

Most operating entities should support:

```text
id
workspace_id
created_at
updated_at
created_by
status
source_object_type
source_object_id
```

Not every entity requires every field, but the pattern preserves traceability across the platform.

---

# 20. MVP Entity Set

The first runnable MVP should prioritize:

```text
User
Session
CompanyWorkspace
WorkspaceSettings
OperatingMap
OperatingGap
Function
Responsibility
Task
Decision
MemoryEntry
AuditEvent
RuntimeEvent
DashboardMetric
```

These entities are sufficient for:

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
Record Audit
↓
Show Dashboard
```

---

# 21. Governed AI Entity Set

The governed AI layer requires:

```text
Agent
AgentAuthorityScope
Process
Integration
SecurityPolicy
ExportJob
```

These entities allow Bizzi to move from basic operating map to AI-assisted runtime.

---

# 22. Expansion Entity Set

Later expansion may include:

```text
WorkspaceMember
Role
Permission
IntegrationMapping
DashboardWidget
Notification
Comment
Attachment
BillingAccount
SubscriptionPlan
```

These are intentionally outside the first core domain catalog unless needed later.

---

# 23. Catalog Completeness Criteria

The catalog is complete enough for the next domain documents when:

- each domain area has initial entities;
- MVP priorities are defined;
- aggregate roots are identified;
- key relationships are clear;
- core invariants are stated;
- the catalog supports data model planning.

Status:

```text
Complete for Domain Layer Expansion
```

---

# 24. Architecture Alignment

| Entity Area | Runtime Reference |
|---|---|
| User / Session | Runtime Security |
| CompanyWorkspace | Workspace Runtime |
| OperatingMap / OperatingGap | Runtime Architecture |
| Function / Responsibility | Core Runtime Components |
| Agent / Authority | Agent Runtime |
| Process / Step | Process Runtime |
| Task | Task Runtime |
| Decision | Decision Runtime |
| MemoryEntry | Memory Runtime |
| AuditEvent | Audit Runtime |
| RuntimeEvent | Event Runtime |
| Integration / SyncJob | Integration Runtime |
| SecurityPolicy / Role / Permission | Runtime Security |
| DashboardMetric | Core User Journey |
| ExportJob | Integration / Export Runtime |

---

# 25. Final Entity Catalog Statement

```text
Bizzi Entity Catalog defines the first canonical inventory of domain entities required to transform Runtime Platform architecture into implementable product objects.
```

This catalog becomes the reference for detailed domain documents, data model design and API contracts.