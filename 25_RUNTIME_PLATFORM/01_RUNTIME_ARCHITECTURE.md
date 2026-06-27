# 01_RUNTIME_ARCHITECTURE.md

# Bizzi Platform

## Runtime Architecture

**Layer:** 25_RUNTIME_PLATFORM  
**Component Type:** Runtime Platform Architecture  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Previous Document:** 00_RUNTIME_VISION.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the runtime architecture of Bizzi Platform.

It translates the Runtime Vision into a concrete architectural structure for the first runnable MVP.

The key question:

```text
What runtime components are required for Bizzi to operate as an AI-orchestrated enterprise operating system?
```

---

# 2. Architecture Goal

The runtime architecture must support the first MVP journey:

```text
Create Workspace
↓
Complete Business Intake
↓
Generate Operating Map
↓
Confirm Functions
↓
Assign Responsibilities
↓
Suggest Agents
↓
Create First Tasks
↓
Log Decisions
↓
Create Memory
↓
Record Audit Events
↓
Show Dashboard
```

---

# 3. Runtime Architecture Principle

Bizzi runtime must be simple enough to build quickly and structured enough to evolve safely.

Recommended architecture direction:

```text
Modular Monolith First
Event-Aware Internals
Structured Data Core
AI-Assisted Services
Audit and Memory by Default
API-Ready Boundaries
```

---

# 4. High-Level Runtime Architecture

```text
User Interface
↓
Application Layer
↓
Runtime Services
↓
Domain Object Layer
↓
Event Layer
↓
Memory and Audit Layer
↓
Persistence Layer
↓
AI and Integration Layer
```

---

# 5. Runtime Layers

## 5.1 User Interface Layer

Responsible for user interaction.

Includes:

- onboarding screens;
- workspace dashboard;
- operating map view;
- function registry UI;
- task list;
- decision log;
- agent registry view;
- memory view;
- audit view.

## 5.2 Application Layer

Coordinates user actions and runtime workflows.

Responsibilities:

- receive user requests;
- validate input;
- call runtime services;
- coordinate AI assistance;
- return product-ready responses;
- update UI state.

## 5.3 Runtime Services Layer

Contains executable product services.

Core services:

```text
WorkspaceService
OnboardingService
OperatingMapService
FunctionRegistryService
ResponsibilityService
AgentRegistryService
ProcessService
TaskService
DecisionService
MemoryService
AuditService
DashboardService
EventService
SecurityService
AIOrchestrationService
```

## 5.4 Domain Object Layer

Defines structured business objects.

Minimum objects:

```text
User
CompanyWorkspace
BusinessIntake
OperatingMap
Function
Responsibility
Agent
Process
Task
Decision
MemoryEntry
AuditEvent
DashboardMetric
RuntimeEvent
```

## 5.5 Event Layer

Captures important runtime state changes.

Examples:

```text
workspace.created
intake.completed
operating_map.generated
function.created
responsibility.assigned
agent.suggested
task.created
decision.logged
memory.created
audit.recorded
dashboard.updated
```

## 5.6 Memory and Audit Layer

Preserves operational memory and traceability.

Responsibilities:

- create memory entries;
- create audit events;
- connect memory to source objects;
- preserve decision rationale;
- support dashboard insights.

## 5.7 Persistence Layer

Stores runtime state.

Initial storage needs:

- workspace data;
- users;
- functions;
- responsibilities;
- agents;
- processes;
- tasks;
- decisions;
- memory entries;
- audit events;
- runtime events.

## 5.8 AI and Integration Layer

Provides AI-assisted operations and future external integrations.

MVP AI use cases:

- interpret onboarding answers;
- generate operating map;
- suggest functions;
- identify responsibility gaps;
- suggest agents;
- suggest tasks;
- summarize decisions;
- extract memory.

---

# 6. Runtime Service Responsibilities

## 6.1 WorkspaceService

Creates and manages company workspaces.

Core operations:

- create workspace;
- update workspace;
- load workspace state;
- manage workspace metadata.

## 6.2 OnboardingService

Captures and structures business intake.

Core operations:

- start intake;
- save answers;
- complete intake;
- produce structured context.

## 6.3 OperatingMapService

Generates and updates the Business Operating Map.

Core operations:

- generate map;
- update map;
- detect gaps;
- link map to functions, responsibilities, agents and tasks.

## 6.4 FunctionRegistryService

Manages enterprise functions.

Core operations:

- create function;
- edit function;
- archive function;
- list functions;
- link function to owner, agent, process and task.

## 6.5 ResponsibilityService

Manages ownership.

Core operations:

- assign owner;
- mark unassigned;
- detect ownership gaps;
- link responsibility to function, task or process.

## 6.6 AgentRegistryService

Registers AI agents.

Core operations:

- suggest agent;
- create agent;
- assign human owner;
- define allowed actions;
- define escalation rule.

## 6.7 ProcessService

Stores simple process definitions.

Core operations:

- create process;
- link process to function;
- define steps;
- link process to tasks and memory.

## 6.8 TaskService

Creates and routes tasks.

Core operations:

- create task;
- assign owner;
- set status;
- set priority;
- link task to function, process or decision.

## 6.9 DecisionService

Records decisions and rationale.

Core operations:

- create decision;
- capture context;
- capture rationale;
- link decision to function, task or process;
- generate decision memory.

## 6.10 MemoryService

Creates structured enterprise memory.

Core operations:

- create memory entry;
- link memory to source object;
- classify memory type;
- retrieve memory by workspace.

## 6.11 AuditService

Records governed runtime activity.

Core operations:

- record audit event;
- link event to actor and object;
- preserve timestamp;
- expose audit trail.

## 6.12 DashboardService

Aggregates runtime state for user visibility.

Core operations:

- calculate dashboard metrics;
- show open tasks;
- show ownership gaps;
- show recent decisions;
- show active agents;
- show memory count;
- show audit events.

## 6.13 EventService

Coordinates runtime events.

Core operations:

- emit event;
- persist event;
- trigger memory updates;
- trigger audit updates;
- trigger dashboard recalculation.

## 6.14 SecurityService

Controls identity and access.

Core operations:

- authenticate user;
- authorize workspace access;
- enforce basic role permissions;
- protect workspace data.

## 6.15 AIOrchestrationService

Coordinates AI-assisted generation and recommendations.

Core operations:

- prepare prompts from structured context;
- request AI output;
- validate output shape;
- convert AI output into draft runtime objects;
- require user confirmation before committing sensitive outputs.

---

# 7. Runtime Interaction Pattern

Every important runtime action follows this pattern:

```text
User Action or System Trigger
↓
Application Layer Request
↓
Service Execution
↓
Domain Object Change
↓
Runtime Event Emitted
↓
Audit Event Recorded
↓
Memory Updated if Applicable
↓
Dashboard Updated
↓
User Feedback Returned
```

---

# 8. AI Execution Pattern

AI-assisted runtime actions follow this pattern:

```text
Structured Context
↓
AI Request
↓
Draft Output
↓
Validation
↓
User Review
↓
Runtime Object Creation
↓
Audit Event
↓
Memory Entry
```

MVP rule:

```text
AI recommends. Human confirms.
```

---

# 9. Object Lifecycle Pattern

Most runtime objects follow this lifecycle:

```text
Draft
↓
Confirmed
↓
Active
↓
Updated
↓
Archived
```

Objects that require stronger governance may add:

```text
Pending Review
Approved
Rejected
Escalated
```

---

# 10. Runtime Data Boundary

The MVP should begin with one workspace per company and one primary owner account.

Initial boundary:

```text
One User
One CompanyWorkspace
Multiple Functions
Multiple Responsibilities
Multiple Agents
Multiple Tasks
Multiple Decisions
Multiple Memory Entries
Multiple Audit Events
```

---

# 11. Runtime Event Boundary

MVP runtime events should remain simple and internal.

They do not need external event streaming at first.

Recommended approach:

```text
Internal Event Table
Simple Event Dispatcher
Synchronous Updates First
Async Processing Later
```

---

# 12. Memory Architecture

Memory must be created from meaningful runtime activity.

Memory sources:

- onboarding intake;
- operating map;
- confirmed functions;
- tasks;
- decisions;
- processes;
- agent suggestions;
- lessons learned.

Memory object minimum fields:

```text
id
workspace_id
source_object_type
source_object_id
memory_type
content
created_by
created_at
confidence
status
```

---

# 13. Audit Architecture

Audit events must be created for governed actions.

Audit object minimum fields:

```text
id
workspace_id
actor_id
action
object_type
object_id
timestamp
metadata
```

Audit must support the question:

```text
Who did what, when, and to which object?
```

---

# 14. Dashboard Architecture

Dashboard should aggregate runtime data rather than become a separate source of truth.

Dashboard inputs:

- functions;
- responsibilities;
- tasks;
- decisions;
- agents;
- memory entries;
- audit events;
- operating gaps.

Dashboard outputs:

- operating summary;
- task status;
- ownership gaps;
- recent decisions;
- suggested next actions.

---

# 15. Security Architecture

MVP security must include:

- authenticated user;
- workspace ownership;
- basic role model;
- workspace-level access boundary;
- protected AI context;
- audit of important actions.

Advanced enterprise security is out of scope for first MVP.

---

# 16. API Boundary

Even if the MVP starts as one application, internal boundaries should be API-ready.

Suggested API groups:

```text
/auth
/workspaces
/intake
/operating-map
/functions
/responsibilities
/agents
/processes
/tasks
/decisions
/memory
/audit
/dashboard
/ai
```

---

# 17. Deployment Direction

Recommended MVP deployment direction:

```text
Single Web Application
Backend API
Relational Database
AI Provider Integration
Basic File Export
Simple Hosting
```

Avoid premature complexity:

- no distributed microservices initially;
- no complex event bus initially;
- no multi-region deployment initially;
- no enterprise integration layer initially.

---

# 18. Technology Independence

This architecture does not lock Bizzi into a specific stack.

However, the implementation should favor:

- fast development;
- strong data modeling;
- simple deployment;
- AI integration support;
- good authentication support;
- future API scalability.

---

# 19. MVP Runtime Definition of Done

Runtime architecture is implemented when:

- workspace can be created;
- onboarding data is captured;
- operating map is generated;
- functions are stored;
- responsibilities are assigned;
- agents are suggested or registered;
- tasks are created;
- decisions are logged;
- memory entries are created;
- audit events are recorded;
- dashboard reflects current state;
- AI outputs are reviewed before persistence.

---

# 20. Architecture Alignment

Runtime Architecture maps to previous documents:

| Runtime Architecture Element | Product Definition Reference |
|---|---|
| Workspace Runtime | 01_MVP_SCOPE.md |
| Onboarding Runtime | 04_CORE_USER_JOURNEY.md |
| Operating Map Runtime | 00_PRODUCT_VISION.md / 03_VALUE_PROPOSITION.md |
| Function Registry | 01_MVP_SCOPE.md |
| Agent Registry | 01_MVP_SCOPE.md |
| Task Runtime | 01_MVP_SCOPE.md / 04_CORE_USER_JOURNEY.md |
| Decision Runtime | 01_MVP_SCOPE.md |
| Memory Runtime | 00_PRODUCT_VISION.md |
| Audit Runtime | Art of Business Governance Baseline |
| Dashboard Runtime | 04_CORE_USER_JOURNEY.md |

---

# 21. Final Runtime Architecture Statement

```text
Bizzi Runtime Architecture defines a modular, event-aware and AI-assisted platform that transforms user input into structured enterprise objects, governed actions, memory, audit events and operating visibility.
```

This document becomes the architectural basis for the remaining Runtime Platform components.