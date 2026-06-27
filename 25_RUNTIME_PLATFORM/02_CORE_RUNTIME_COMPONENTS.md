# 02_CORE_RUNTIME_COMPONENTS.md

# Bizzi Platform

## Core Runtime Components

**Layer:** 25_RUNTIME_PLATFORM  
**Component Type:** Runtime Component Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Previous Documents:** 00_RUNTIME_VISION.md, 01_RUNTIME_ARCHITECTURE.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the core runtime components required for the first runnable Bizzi Platform MVP.

It translates Runtime Architecture into concrete platform components that can be designed, implemented, tested and evolved.

Core question:

```text
Which executable components must exist for Bizzi to run the first end-to-end product journey?
```

---

# 2. Component Design Principle

Bizzi runtime components must be:

```text
Small enough to build
Clear enough to govern
Structured enough to scale
Traceable enough to audit
```

The first runtime should avoid unnecessary complexity while preserving architectural integrity.

---

# 3. Core Runtime Component Map

The MVP runtime consists of the following core components:

```text
Workspace Runtime
Onboarding Runtime
Operating Map Runtime
Function Registry Runtime
Responsibility Runtime
Agent Registry Runtime
Process Runtime
Task Runtime
Decision Runtime
Memory Runtime
Audit Runtime
Dashboard Runtime
Event Runtime
Security Runtime
AI Orchestration Runtime
Export Runtime
```

---

# 4. Runtime Component Groups

## 4.1 Foundation Components

```text
Workspace Runtime
Security Runtime
Event Runtime
```

These components create the basic execution environment.

## 4.2 Operating Model Components

```text
Onboarding Runtime
Operating Map Runtime
Function Registry Runtime
Responsibility Runtime
Process Runtime
```

These components model the business as an operating system.

## 4.3 Execution Components

```text
Agent Registry Runtime
Task Runtime
Decision Runtime
```

These components turn structure into action.

## 4.4 Intelligence and Evidence Components

```text
Memory Runtime
Audit Runtime
Dashboard Runtime
AI Orchestration Runtime
```

These components preserve context, provide visibility and support intelligent recommendations.

## 4.5 Output Components

```text
Export Runtime
```

This component turns operating data into shareable outputs.

---

# 5. Component 1 — Workspace Runtime

## Purpose

Creates and manages company workspaces.

## Responsibilities

- create workspace;
- store company metadata;
- link users to workspace;
- maintain workspace status;
- provide workspace context to other components.

## Primary Objects

```text
CompanyWorkspace
WorkspaceMember
User
```

## Key Events

```text
workspace.created
workspace.updated
workspace.member_added
```

## MVP Requirement

One owner user must be able to create one company workspace.

---

# 6. Component 2 — Onboarding Runtime

## Purpose

Captures structured business context during first user activation.

## Responsibilities

- ask intake questions;
- store answers;
- classify user pain points;
- prepare structured context for AI processing;
- mark onboarding completion.

## Primary Objects

```text
BusinessIntake
IntakeAnswer
StructuredBusinessContext
```

## Key Events

```text
intake.started
intake.answer_saved
intake.completed
```

## MVP Requirement

User must complete a lightweight intake that provides enough context to generate the first Business Operating Map.

---

# 7. Component 3 — Operating Map Runtime

## Purpose

Generates and maintains the Business Operating Map.

## Responsibilities

- generate initial map;
- suggest functions;
- detect gaps;
- link functions, responsibilities, agents and tasks;
- update map after user confirmation.

## Primary Objects

```text
OperatingMap
OperatingGap
OperatingRecommendation
```

## Key Events

```text
operating_map.generated
operating_map.updated
operating_gap.detected
recommendation.created
```

## MVP Requirement

Bizzi must generate a useful first operating map from onboarding inputs.

---

# 8. Component 4 — Function Registry Runtime

## Purpose

Stores and manages business functions.

## Responsibilities

- create functions;
- edit functions;
- archive functions;
- link functions to responsibilities, agents, processes, tasks and decisions;
- provide function structure for dashboard and AI recommendations.

## Primary Objects

```text
Function
FunctionCategory
FunctionStatus
```

## Key Events

```text
function.created
function.updated
function.archived
```

## MVP Requirement

User must be able to confirm or edit several core business functions.

---

# 9. Component 5 — Responsibility Runtime

## Purpose

Tracks ownership across functions, processes and tasks.

## Responsibilities

- assign owners;
- mark unassigned areas;
- detect ownership gaps;
- support human and AI-assisted ownership;
- link responsibility to audit trail.

## Primary Objects

```text
Responsibility
OwnerAssignment
OwnershipGap
```

## Key Events

```text
responsibility.assigned
responsibility.updated
ownership_gap.detected
```

## MVP Requirement

User must see which functions or tasks have owners and which remain unassigned.

---

# 10. Component 6 — Agent Registry Runtime

## Purpose

Registers AI agents as governed support roles inside the company operating model.

## Responsibilities

- suggest agents;
- create agent records;
- assign human owner;
- define role;
- define allowed actions;
- define escalation rule;
- link agent to function or process.

## Primary Objects

```text
Agent
AgentRole
AgentAuthorityScope
AgentEscalationRule
```

## Key Events

```text
agent.suggested
agent.created
agent.assigned
agent.updated
```

## MVP Requirement

AI agents are suggestions and support roles only. Human ownership is required.

---

# 11. Component 7 — Process Runtime

## Purpose

Stores lightweight process definitions.

## Responsibilities

- create process drafts;
- define process purpose;
- define steps;
- link process to function;
- link process to tasks, agents, decisions and memory.

## Primary Objects

```text
Process
ProcessStep
ProcessInput
ProcessOutput
```

## Key Events

```text
process.created
process.updated
process.linked
```

## MVP Requirement

Processes may start as simple structured drafts. Complex workflow automation is not required in first MVP.

---

# 12. Component 8 — Task Runtime

## Purpose

Creates and routes tasks across the workspace.

## Responsibilities

- create tasks;
- assign owners;
- set priority;
- set status;
- link tasks to functions, processes, decisions and agents;
- expose open tasks to dashboard.

## Primary Objects

```text
Task
TaskStatus
TaskPriority
TaskAssignment
```

## Key Events

```text
task.created
task.assigned
task.status_changed
task.completed
```

## MVP Requirement

User must see actionable next tasks generated from operating gaps.

---

# 13. Component 9 — Decision Runtime

## Purpose

Records important business decisions and rationale.

## Responsibilities

- create decision records;
- capture decision context;
- capture rationale;
- link decision to function, task or process;
- create decision memory;
- expose recent decisions to dashboard.

## Primary Objects

```text
Decision
DecisionContext
DecisionRationale
DecisionOption
```

## Key Events

```text
decision.logged
decision.updated
decision.memory_created
```

## MVP Requirement

User must be able to log a decision so it does not disappear into chat history.

---

# 14. Component 10 — Memory Runtime

## Purpose

Creates and retrieves structured enterprise memory.

## Responsibilities

- create memory entries;
- classify memory type;
- link memory to source objects;
- store operating context;
- support future AI retrieval;
- preserve decision, process and task context.

## Primary Objects

```text
MemoryEntry
MemoryType
MemorySource
MemoryStatus
```

## Key Events

```text
memory.created
memory.updated
memory.linked
```

## MVP Requirement

Memory must be created from onboarding, operating map, decisions, tasks and processes.

---

# 15. Component 11 — Audit Runtime

## Purpose

Records traceable evidence of important runtime activity.

## Responsibilities

- create audit events;
- capture actor;
- capture action;
- capture object reference;
- capture timestamp;
- expose audit trail.

## Primary Objects

```text
AuditEvent
AuditActor
AuditObjectReference
```

## Key Events

```text
audit.recorded
```

## MVP Requirement

Every governed action must be auditable.

---

# 16. Component 12 — Dashboard Runtime

## Purpose

Aggregates runtime state into a visible operating dashboard.

## Responsibilities

- calculate dashboard metrics;
- show functions;
- show ownership gaps;
- show open tasks;
- show agents;
- show recent decisions;
- show memory count;
- show suggested next actions.

## Primary Objects

```text
DashboardMetric
DashboardView
OperatingSummary
```

## Key Events

```text
dashboard.updated
dashboard.viewed
```

## MVP Requirement

Dashboard must answer:

```text
What is happening?
Who is responsible?
What should happen next?
```

---

# 17. Component 13 — Event Runtime

## Purpose

Coordinates runtime state changes through internal events.

## Responsibilities

- emit events;
- persist events;
- notify interested services;
- trigger audit creation;
- trigger dashboard recalculation;
- support future async processing.

## Primary Objects

```text
RuntimeEvent
EventType
EventPayload
```

## Key Events

```text
runtime_event.emitted
runtime_event.processed
```

## MVP Requirement

Internal events may be simple and synchronous. External event bus is not required.

---

# 18. Component 14 — Security Runtime

## Purpose

Controls identity, access and workspace boundaries.

## Responsibilities

- authenticate users;
- authorize workspace access;
- enforce owner role;
- protect workspace data;
- support audit of sensitive actions.

## Primary Objects

```text
User
Role
Permission
Session
```

## Key Events

```text
user.authenticated
access.granted
access.denied
```

## MVP Requirement

One authenticated owner must securely access one workspace.

---

# 19. Component 15 — AI Orchestration Runtime

## Purpose

Coordinates AI-assisted recommendations and generated outputs.

## Responsibilities

- prepare structured AI context;
- call AI provider;
- validate AI output shape;
- convert AI output into draft objects;
- require user confirmation;
- record AI-assisted events.

## Primary Objects

```text
AIRequest
AIResponse
AIDraftObject
AIRecommendation
```

## Key Events

```text
ai.requested
ai.response_received
ai.recommendation_created
ai.output_confirmed
```

## MVP Requirement

AI must recommend and draft. Human confirmation is required before persistence of important objects.

---

# 20. Component 16 — Export Runtime

## Purpose

Creates shareable outputs from runtime data.

## Responsibilities

- export operating map;
- export function registry;
- export responsibility map;
- export task list;
- export decision log;
- export audit trail.

## Primary Objects

```text
ExportJob
ExportFile
ExportFormat
```

## Key Events

```text
export.requested
export.generated
export.downloaded
```

## MVP Requirement

Initial exports may be Markdown, CSV or PDF.

---

# 21. Component Interaction Model

The core runtime interaction model:

```text
Workspace Runtime
↓
Onboarding Runtime
↓
AI Orchestration Runtime
↓
Operating Map Runtime
↓
Function Registry Runtime
↓
Responsibility Runtime
↓
Agent Registry Runtime
↓
Task Runtime
↓
Decision Runtime
↓
Memory Runtime
↓
Audit Runtime
↓
Dashboard Runtime
```

Event Runtime supports all components.

Security Runtime protects all components.

Export Runtime creates outputs from selected runtime objects.

---

# 22. Component Dependency Rules

## Rule 1 — Workspace First

No runtime object may exist without a workspace.

## Rule 2 — Events for Important Changes

Important state changes must emit runtime events.

## Rule 3 — Audit for Governed Actions

Governed actions must create audit records.

## Rule 4 — Memory from Meaningful Context

Decisions, processes, onboarding and operating map changes should create memory where useful.

## Rule 5 — AI Output Requires Review

AI-generated recommendations must remain draft until confirmed by the user.

---

# 23. MVP Component Priority

Build priority:

```text
1. Workspace Runtime
2. Security Runtime
3. Onboarding Runtime
4. AI Orchestration Runtime
5. Operating Map Runtime
6. Function Registry Runtime
7. Responsibility Runtime
8. Task Runtime
9. Dashboard Runtime
10. Audit Runtime
11. Memory Runtime
12. Decision Runtime
13. Agent Registry Runtime
14. Process Runtime
15. Event Runtime refinement
16. Export Runtime
```

Event handling may begin as simple internal service logic and mature over time.

---

# 24. Component Definition of Done

A runtime component is considered ready when it defines:

- purpose;
- primary objects;
- core operations;
- emitted events;
- audit requirements;
- memory behavior if applicable;
- dashboard contribution if applicable;
- MVP acceptance criteria.

---

# 25. Architecture Alignment

| Runtime Component | Product / Architecture Reference |
|---|---|
| Workspace Runtime | 01_MVP_SCOPE.md |
| Onboarding Runtime | 04_CORE_USER_JOURNEY.md |
| Operating Map Runtime | 00_PRODUCT_VISION.md |
| Function Registry Runtime | Art of Business Function Registry |
| Responsibility Runtime | Governance Baseline |
| Agent Registry Runtime | Agent Library |
| Process Runtime | Process Architecture |
| Task Runtime | Operating Model |
| Decision Runtime | Decision Routing |
| Memory Runtime | Enterprise Memory |
| Audit Runtime | Observability and Intelligence |
| Dashboard Runtime | Product Value Proposition |
| Event Runtime | Runtime Architecture |
| Security Runtime | Security / Governance Baseline |
| AI Orchestration Runtime | Enterprise Autonomy Governance |
| Export Runtime | MVP Exports |

---

# 26. Final Component Statement

```text
Bizzi Core Runtime Components define the executable building blocks required to transform product vision into a working AI-orchestrated enterprise operating system.
```

This document becomes the component catalog for the Runtime Platform layer.