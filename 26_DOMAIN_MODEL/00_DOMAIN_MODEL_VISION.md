# 00_DOMAIN_MODEL_VISION.md

# Bizzi Platform

## Domain Model Vision

**Layer:** 26_DOMAIN_MODEL  
**Component Type:** Product Engineering Domain Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document opens the `26_DOMAIN_MODEL` layer for Bizzi Platform.

The Domain Model layer translates Runtime Platform architecture into a stable set of business entities, relationships, boundaries and lifecycle rules that can later become the data model, API contracts and backend services.

Core question:

```text
What are the core business objects of Bizzi, how do they relate to each other, and what rules govern their behavior?
```

---

# 2. Layer Mission

The mission of `26_DOMAIN_MODEL` is to define the canonical product domain of Bizzi Platform.

This layer must make the runtime architecture implementable by defining:

- domain entities;
- aggregate boundaries;
- relationships;
- ownership rules;
- lifecycle states;
- invariants;
- domain events;
- cross-entity traceability;
- MVP entity priorities.

---

# 3. Position in Architecture

```text
Art of Business v1.0
↓
24_PRODUCTIZATION_AND_IMPLEMENTATION
↓
25_RUNTIME_PLATFORM
↓
26_DOMAIN_MODEL
↓
27_DATA_MODEL
↓
28_API_CONTRACTS
↓
29_BACKEND_SERVICE_DESIGN
```

Layer 25 defines how Bizzi should run.

Layer 26 defines what Bizzi is made of at the domain level.

---

# 4. Domain Model Thesis

```text
Bizzi must not store random text fragments.
Bizzi must operate through structured business objects with clear ownership, lifecycle, traceability and governance rules.
```

The domain model turns business activity into stable objects that can be stored, queried, audited, remembered and acted upon.

---

# 5. Domain Modeling Principles

## 5.1 Workspace-Scoped Domain

Every business object belongs to a workspace unless explicitly global.

```text
No workspace_id, no operating object.
```

## 5.2 Object Before Automation

Automation should operate on domain objects, not loose chat output.

## 5.3 Human Accountability

Objects that affect business operations must preserve human accountability.

## 5.4 Source Traceability

Important objects must link to their source where applicable.

## 5.5 Lifecycle Discipline

Objects should have explicit states instead of implicit ambiguity.

## 5.6 AI Drafts Before Persistence

AI-generated entities should remain drafts or candidates until confirmed where required.

## 5.7 Audit and Memory Compatibility

Domain objects must support audit events and memory linkage by design.

---

# 6. Core Domain Areas

The Bizzi domain model includes the following areas:

```text
Identity Domain
Workspace Domain
Operating Map Domain
Function Domain
Responsibility Domain
Agent Domain
Process Domain
Task Domain
Decision Domain
Memory Domain
Audit Domain
Event Domain
Integration Domain
Security Domain
Dashboard Domain
Export Domain
```

---

# 7. Core Domain Entities

Initial canonical entity set:

```text
User
Session
CompanyWorkspace
WorkspaceMember
WorkspaceSettings
OperatingMap
OperatingGap
Function
Responsibility
Agent
AgentAuthorityScope
Process
ProcessStep
Task
Decision
MemoryEntry
AuditEvent
RuntimeEvent
Integration
IntegrationSyncJob
SecurityPolicy
ExportJob
DashboardMetric
```

These entities form the first domain foundation for Bizzi MVP.

---

# 8. Aggregate Boundaries

Recommended aggregate roots:

```text
CompanyWorkspace
OperatingMap
Function
Agent
Process
Task
Decision
MemoryEntry
Integration
ExportJob
```

Supporting entities should be managed within or through these aggregate roots where practical.

---

# 9. Workspace as Root Boundary

`CompanyWorkspace` is the root boundary for Bizzi operating state.

All major domain entities should reference:

```text
workspace_id
```

This includes:

- functions;
- responsibilities;
- agents;
- processes;
- tasks;
- decisions;
- memory entries;
- audit events;
- runtime events;
- integrations;
- exports;
- dashboard metrics.

---

# 10. Domain Relationship Pattern

Bizzi domain relationships should support this operating chain:

```text
Workspace
↓
Operating Map
↓
Functions
↓
Responsibilities
↓
Agents / Processes / Tasks / Decisions
↓
Memory / Audit / Events
↓
Dashboard / Export
```

The model should allow each important object to be traced back to workspace, owner, source and runtime activity.

---

# 11. Entity Lifecycle Pattern

Most entities follow a lifecycle pattern:

```text
candidate
↓
draft
↓
active
↓
reviewed
↓
archived
```

Not every entity needs every state, but the pattern should guide consistency.

Examples:

- AI-generated agent: `suggested → active → paused → archived`;
- task: `suggested → open → in_progress → completed → archived`;
- memory: `candidate → active → archived`;
- decision: `draft → confirmed → archived`.

---

# 12. Domain Events

Domain entities should emit or correspond to runtime events.

Examples:

```text
workspace.created
function.created
responsibility.assigned
agent.created
process.created
task.created
decision.confirmed
memory.created
audit.recorded
integration.connected
export.generated
```

Domain events support audit, memory, dashboard and future orchestration.

---

# 13. Domain Invariants

Initial invariants:

```text
Every runtime object must belong to a workspace.
Every active agent must have a human owner.
Every confirmed decision must have an owner.
Every active memory entry should have a source or explicit manual origin.
Every audit event must have actor, action, target and timestamp.
Every integration must have explicit scope.
Every export must be workspace-scoped.
AI-generated sensitive objects require human confirmation.
Archived objects cannot be modified through normal workflows.
```

---

# 14. MVP Domain Priority

Priority 1 — Required for first runnable slice:

```text
User
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

Priority 2 — Needed for governed AI assistance:

```text
Agent
AgentAuthorityScope
Process
Integration
SecurityPolicy
ExportJob
```

Priority 3 — Future expansion:

```text
WorkspaceMember
Advanced Role
Advanced Permission
IntegrationMapping
Advanced DashboardWidget
```

---

# 15. Domain Model Outputs

The `26_DOMAIN_MODEL` layer should produce:

```text
00_DOMAIN_MODEL_VISION.md
01_ENTITY_CATALOG.md
02_WORKSPACE_DOMAIN.md
03_OPERATING_MAP_DOMAIN.md
04_FUNCTION_AND_RESPONSIBILITY_DOMAIN.md
05_AGENT_DOMAIN.md
06_PROCESS_DOMAIN.md
07_TASK_DOMAIN.md
08_DECISION_DOMAIN.md
09_MEMORY_DOMAIN.md
10_AUDIT_AND_EVENT_DOMAIN.md
11_INTEGRATION_AND_SECURITY_DOMAIN.md
12_DASHBOARD_AND_EXPORT_DOMAIN.md
13_DOMAIN_MODEL_MILESTONE.md
14_DOMAIN_MODEL_AUDIT.md
```

---

# 16. Relationship to Data Model

The Domain Model is not yet the database schema.

It defines conceptual objects and rules.

The Data Model will later define:

- tables or collections;
- fields;
- indexes;
- constraints;
- foreign keys;
- storage choices;
- migration strategy.

---

# 17. Relationship to API Contracts

The Domain Model is not yet API design.

It defines business meaning.

The API layer will later define:

- endpoints;
- request schemas;
- response schemas;
- status codes;
- authorization requirements;
- error structures.

---

# 18. Relationship to Backend Services

The Domain Model informs backend service boundaries.

Domain areas should map naturally to runtime services:

```text
Workspace Domain → WorkspaceRuntimeService
Agent Domain → AgentRuntimeService
Task Domain → TaskRuntimeService
Decision Domain → DecisionRuntimeService
Memory Domain → MemoryRuntimeService
Audit Domain → AuditRuntimeService
Integration Domain → IntegrationRuntimeService
Security Domain → SecurityRuntimeService
```

---

# 19. Domain Model Success Criteria

The Domain Model layer is successful when:

- all core entities are defined;
- relationships are clear;
- aggregate boundaries are known;
- lifecycle states are consistent;
- ownership rules are explicit;
- AI-generated object rules are defined;
- traceability rules are defined;
- the model can support data model and API contract design.

---

# 20. Out of Scope

This layer does not define:

- exact database schema;
- implementation classes;
- ORM models;
- API endpoint specifications;
- UI screen layouts;
- deployment configuration;
- production infrastructure;
- billing or pricing entities unless required later.

---

# 21. Final Domain Model Vision Statement

```text
Bizzi Domain Model defines the canonical business objects and rules that allow Bizzi to operate as a structured, workspace-scoped, AI-assisted, auditable and memory-enabled enterprise operating system.
```

This layer begins the transition from runtime architecture to implementable product engineering.