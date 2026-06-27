# 02_CORE_RUNTIME_COMPONENTS.md

# Bizzi Platform

## Core Runtime Components

**Layer:** 25_RUNTIME_PLATFORM  
**Component Type:** Runtime Platform Component Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Previous Documents:** 00_RUNTIME_VISION.md, 01_RUNTIME_ARCHITECTURE.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the core runtime components required for the Bizzi Platform MVP.

It answers the product-engineering question:

```text
Which executable runtime components must exist for Bizzi to deliver the first operating system experience to a business owner?
```

---

# 2. Component Design Principle

Each runtime component must satisfy five rules:

```text
Own a clear responsibility
Operate on structured objects
Emit or consume runtime events
Support memory and audit where required
Remain traceable to Art of Business v1.0
```

Components must be small enough to build and test, but stable enough to become future service boundaries.

---

# 3. Core Component Map

The MVP runtime consists of the following core components:

```text
Workspace Runtime
Identity and Access Runtime
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
AI Orchestration Runtime
Export Runtime
```

---

# 4. Component Interaction Overview

```text
User
↓
Workspace Runtime
↓
Onboarding Runtime
↓
Operating Map Runtime
↓
Function / Responsibility / Agent Runtime
↓
Task / Decision / Process Runtime
↓
Memory Runtime
↓
Audit Runtime
↓
Dashboard Runtime
```

The Event Runtime coordinates state changes across components.

The AI Orchestration Runtime assists onboarding, operating map generation, gap detection, task suggestions and memory extraction.

---

# 5. Component: Workspace Runtime

## Responsibility

Manages company workspaces.

## Owns

- CompanyWorkspace;
- WorkspaceMember;
- workspace metadata;
- workspace lifecycle.

## Core Actions

- create workspace;
- update workspace;
- retrieve workspace;
- archive workspace;
- initialize default runtime state.

## Events

```text
workspace.created
workspace.updated
workspace.archived
```

## MVP Requirement

The MVP must support one company workspace for the primary user.

---

# 6. Component: Identity and Access Runtime

## Responsibility

Controls user identity and workspace access.

## Owns

- User;
- authentication state;
- workspace membership;
- basic role assignment.

## Core Actions

- register user;
- authenticate user;
- authorize workspace access;
- assign owner role;
- enforce workspace boundary.

## Events

```text
user.created
user.authenticated
workspace_access.granted
workspace_access.denied
```

## MVP Requirement

The MVP must support basic authentication and workspace-owner access.

---

# 7. Component: Onboarding Runtime

## Responsibility

Captures structured business context from the user.

## Owns

- BusinessIntake;
- intake questions;
- intake answers;
- structured context object.

## Core Actions

- start intake;
- save answer;
- complete intake;
- produce structured business context.

## Events

```text
intake.started
intake.answer_saved
intake.completed
```

## MVP Requirement

The onboarding flow must generate enough structured context to create the first Business Operating Map.

---

# 8. Component: Operating Map Runtime

## Responsibility

Generates and manages the Business Operating Map.

## Owns

- OperatingMap;
- operating gaps;
- suggested functions;
- suggested agents;
- suggested tasks;
- map status.

## Core Actions

- generate operating map;
- update operating map;
- identify gaps;
- link map items to functions, responsibilities, agents and tasks.

## Events

```text
operating_map.generated
operating_map.updated
operating_gap.detected
```

## MVP Requirement

This component is central to activation. The user must receive a useful operating map in the first hour.

---

# 9. Component: Function Registry Runtime

## Responsibility

Stores and manages business functions.

## Owns

- Function;
- function category;
- function status;
- function relationships.

## Core Actions

- create function;
- edit function;
- confirm suggested function;
- archive function;
- list functions.

## Events

```text
function.created
function.updated
function.confirmed
function.archived
```

## MVP Requirement

The user must be able to confirm, edit or remove suggested functions.

---

# 10. Component: Responsibility Runtime

## Responsibility

Manages ownership and accountability.

## Owns

- Responsibility;
- owner assignment;
- ownership gaps;
- responsibility status.

## Core Actions

- assign responsibility;
- change owner;
- mark unassigned;
- detect ownership gap;
- link responsibility to function, task or process.

## Events

```text
responsibility.assigned
responsibility.updated
responsibility.unassigned
responsibility_gap.detected
```

## MVP Requirement

The system must make missing ownership visible.

---

# 11. Component: Agent Registry Runtime

## Responsibility

Manages AI agent definitions inside the workspace.

## Owns

- Agent;
- agent role;
- human owner;
- allowed actions;
- escalation rule;
- agent status.

## Core Actions

- suggest agent;
- create agent;
- edit agent;
- assign human owner;
- define allowed actions;
- define escalation route.

## Events

```text
agent.suggested
agent.created
agent.updated
agent.owner_assigned
agent.archived
```

## MVP Requirement

Agents must remain advisory and governed. Every agent must have a human owner.

---

# 12. Component: Process Runtime

## Responsibility

Stores simple process definitions and links them to functions and tasks.

## Owns

- Process;
- process purpose;
- process steps;
- process owner;
- input/output definitions.

## Core Actions

- create process;
- edit process;
- link process to function;
- link process to tasks;
- archive process.

## Events

```text
process.created
process.updated
process.linked_to_function
process.archived
```

## MVP Requirement

The process runtime can remain simple and should support lightweight process drafts.

---

# 13. Component: Task Runtime

## Responsibility

Creates, routes and tracks tasks.

## Owns

- Task;
- task status;
- task owner;
- task priority;
- due date;
- task relationships.

## Core Actions

- create task;
- assign owner;
- update status;
- update priority;
- link task to function, process or decision.

## Events

```text
task.created
task.assigned
task.status_changed
task.priority_changed
task.completed
```

## MVP Requirement

Tasks must be created from onboarding gaps, operating map recommendations and user actions.

---

# 14. Component: Decision Runtime

## Responsibility

Records business decisions and decision rationale.

## Owns

- Decision;
- decision context;
- options considered;
- final decision;
- rationale;
- linked objects.

## Core Actions

- create decision;
- edit decision;
- link decision to function, task or process;
- generate decision memory.

## Events

```text
decision.created
decision.updated
decision.linked
decision.memory_created
```

## MVP Requirement

The user must be able to record at least one meaningful business decision.

---

# 15. Component: Memory Runtime

## Responsibility

Creates and retrieves structured enterprise memory.

## Owns

- MemoryEntry;
- memory type;
- memory source;
- confidence;
- memory status.

## Core Actions

- create memory entry;
- extract memory from object;
- link memory to source;
- retrieve memory by workspace;
- archive memory entry.

## Events

```text
memory.created
memory.updated
memory.linked
memory.archived
```

## MVP Requirement

Memory must be created from onboarding, operating maps, decisions, tasks and process drafts.

---

# 16. Component: Audit Runtime

## Responsibility

Creates audit evidence for governed runtime actions.

## Owns

- AuditEvent;
- actor;
- action;
- target object;
- timestamp;
- metadata.

## Core Actions

- record audit event;
- retrieve audit trail;
- link audit event to runtime object.

## Events

```text
audit.recorded
```

## MVP Requirement

Every important product action must create an audit event.

---

# 17. Component: Dashboard Runtime

## Responsibility

Aggregates runtime state into user-visible operating views.

## Owns

- DashboardMetric;
- dashboard summary;
- operating status;
- next actions.

## Core Actions

- calculate metrics;
- show open tasks;
- show ownership gaps;
- show recent decisions;
- show active agents;
- show memory status;
- show recommended next actions.

## Events

```text
dashboard.updated
dashboard.viewed
```

## MVP Requirement

Dashboard must not be empty. It must be populated from onboarding, operating map, tasks, functions and responsibility gaps.

---

# 18. Component: Event Runtime

## Responsibility

Coordinates important state changes across runtime components.

## Owns

- RuntimeEvent;
- event type;
- event payload;
- event status.

## Core Actions

- emit event;
- persist event;
- dispatch event to subscribers;
- trigger audit update;
- trigger memory update;
- trigger dashboard update.

## Events

```text
runtime_event.emitted
runtime_event.processed
runtime_event.failed
```

## MVP Requirement

The MVP may use an internal event table and simple dispatcher rather than a complex external event bus.

---

# 19. Component: AI Orchestration Runtime

## Responsibility

Coordinates AI-assisted recommendations and generation.

## Owns

- AI request context;
- prompt templates;
- structured output schemas;
- AI draft outputs;
- validation status.

## Core Actions

- prepare AI request;
- generate operating map draft;
- suggest functions;
- suggest agents;
- suggest tasks;
- summarize decisions;
- extract memory;
- validate AI output;
- require user confirmation.

## Events

```text
ai.requested
ai.output_generated
ai.output_validated
ai.output_rejected
ai.output_confirmed
```

## MVP Requirement

AI must produce draft recommendations. Human confirmation is required before important persistence.

---

# 20. Component: Export Runtime

## Responsibility

Generates simple exports for user-visible value and portability.

## Owns

- export request;
- export format;
- export content;
- export status.

## Core Actions

- export operating map;
- export function registry;
- export task list;
- export decision log;
- export audit trail.

## Events

```text
export.requested
export.generated
export.downloaded
```

## MVP Requirement

Exports may initially be Markdown, CSV or PDF depending on implementation priority.

---

# 21. Component Dependency Matrix

| Component | Depends On | Feeds |
|---|---|---|
| Workspace Runtime | Identity Runtime | All workspace components |
| Onboarding Runtime | Workspace Runtime | Operating Map Runtime |
| Operating Map Runtime | Onboarding Runtime, AI Runtime | Functions, Responsibilities, Agents, Tasks |
| Function Registry Runtime | Workspace Runtime | Responsibility, Process, Task, Dashboard |
| Responsibility Runtime | Function Registry | Dashboard, Audit |
| Agent Registry Runtime | Function Registry, Responsibility | Dashboard, Task, Audit |
| Process Runtime | Function Registry | Task, Memory |
| Task Runtime | Function, Responsibility, Process | Dashboard, Memory, Audit |
| Decision Runtime | Workspace, Function, Task | Memory, Audit, Dashboard |
| Memory Runtime | Runtime Objects | Dashboard, AI Context |
| Audit Runtime | Runtime Events | Audit Trail |
| Dashboard Runtime | All Runtime State | User Visibility |
| Event Runtime | All Components | Audit, Memory, Dashboard |
| AI Orchestration Runtime | Structured Context | Operating Map, Suggestions, Memory |
| Export Runtime | Runtime State | User Exports |

---

# 22. First Runnable Component Sequence

Recommended build sequence:

```text
1. Identity and Access Runtime
2. Workspace Runtime
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
14. Export Runtime
```

This sequence prioritizes first-hour value.

---

# 23. Component Definition of Done

A runtime component is complete when:

- its owned objects are defined;
- its actions are implemented;
- its events are emitted;
- audit is recorded where required;
- memory is created where relevant;
- dashboard receives needed state;
- tests cover core behavior;
- component boundaries are documented.

---

# 24. Architecture Alignment

| Runtime Component | Art of Business Reference |
|---|---|
| Workspace Runtime | Enterprise Foundation |
| Identity and Access Runtime | Governance / Security |
| Onboarding Runtime | Capability Discovery |
| Operating Map Runtime | Capability Map / Function Registry |
| Function Registry Runtime | Function Registry |
| Responsibility Runtime | Governance / Decision Routing |
| Agent Registry Runtime | Agent Library |
| Process Runtime | Process Architecture |
| Task Runtime | Operating Model |
| Decision Runtime | Decision Routing / Enterprise Memory |
| Memory Runtime | Enterprise Memory |
| Audit Runtime | Observability and Intelligence |
| Dashboard Runtime | Enterprise Operations |
| Event Runtime | Enterprise Operations |
| AI Orchestration Runtime | Enterprise Autonomy / Governance |
| Export Runtime | Knowledge and Reporting |

---

# 25. Final Component Statement

```text
Bizzi Core Runtime Components define the executable building blocks that transform product vision into workspace creation, operating maps, registries, tasks, decisions, memory, auditability and dashboard visibility.
```

This document becomes the component map for building the first Bizzi Runtime Platform.