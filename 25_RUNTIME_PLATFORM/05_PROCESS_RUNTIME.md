# 05_PROCESS_RUNTIME.md

# Bizzi Platform

## Process Runtime

**Layer:** 25_RUNTIME_PLATFORM  
**Component Type:** Runtime Component Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 00_RUNTIME_VISION.md, 01_RUNTIME_ARCHITECTURE.md, 02_CORE_RUNTIME_COMPONENTS.md, 03_WORKSPACE_RUNTIME.md, 04_AGENT_RUNTIME.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Process Runtime for Bizzi Platform.

The Process Runtime is responsible for creating, storing, linking and evolving lightweight business process definitions inside a company workspace.

Core question:

```text
How does Bizzi turn informal recurring work into structured, owned and reusable business processes?
```

---

# 2. Runtime Role

Process Runtime connects the business operating model to repeatable execution.

It links processes to:

- workspace;
- functions;
- responsibilities;
- human owners;
- AI agents;
- tasks;
- decisions;
- memory;
- audit events;
- dashboard indicators.

---

# 3. Process Runtime Principle

```text
Process First, Automation Later
```

The MVP must capture and structure processes before attempting complex workflow automation.

A process may begin as a simple draft and evolve into a more formal operating object.

---

# 4. Primary Runtime Objects

Minimum objects:

```text
Process
ProcessStep
ProcessOwner
ProcessInput
ProcessOutput
ProcessStatus
ProcessGap
```

Supporting objects:

```text
CompanyWorkspace
Function
Responsibility
Agent
Task
Decision
MemoryEntry
AuditEvent
RuntimeEvent
```

---

# 5. Process Object

## Purpose

Represents a repeatable business activity or operating procedure inside the workspace.

## Minimum Fields

```text
id
workspace_id
name
purpose
function_id
owner_id
status
created_at
updated_at
```

## Optional Fields

```text
description
trigger
inputs
outputs
steps
agent_id
risk_level
frequency
success_criteria
```

---

# 6. Process Lifecycle

```text
Suggested
↓
Draft
↓
Defined
↓
Active
↓
Reviewed
↓
Improved
↓
Archived
```

## Suggested

Bizzi recommends a process based on operating gaps, tasks or onboarding context.

## Draft

The user or AI creates a first process outline.

## Defined

Purpose, owner, function and basic steps are known.

## Active

Process is used in operations.

## Reviewed

Process is checked for accuracy, gaps or improvement.

## Improved

Process is updated based on lessons learned.

## Archived

Process is retained historically but no longer active.

---

# 7. Process States

```text
suggested
draft
defined
active
reviewed
improved
archived
```

MVP required states:

```text
suggested
draft
active
archived
```

---

# 8. Process Types for MVP

Initial process types:

```text
Operational Process
Customer Process
Sales Process
Finance Process
HR Process
Procurement Process
Support Process
Management Rhythm Process
```

The MVP should avoid deep process taxonomies.

---

# 9. Core Operations

## 9.1 Suggest Process

Creates a process suggestion from onboarding, operating gaps or repeated tasks.

## 9.2 Create Process

Creates a process record inside the workspace.

## 9.3 Define Process Purpose

Captures why the process exists.

## 9.4 Add Process Steps

Adds lightweight ordered steps.

## 9.5 Assign Process Owner

Links a human owner to the process.

## 9.6 Link Process to Function

Connects the process to a business function.

## 9.7 Link Process to Agent

Connects the process to an AI support agent if applicable.

## 9.8 Link Process to Tasks and Decisions

Connects process execution to concrete work and decisions.

## 9.9 Review Process

Allows the owner to confirm or improve the process.

## 9.10 Archive Process

Retains the process historically but removes it from active operations.

---

# 10. Process Creation Flow

```text
Operating gap or recurring task detected
↓
Process Runtime creates suggestion
↓
AI Orchestration Runtime drafts process outline
↓
User reviews draft
↓
Function is linked
↓
Human owner assigned
↓
Steps confirmed
↓
Process activated
↓
Audit event recorded
↓
Memory entry created
↓
Dashboard updated
```

---

# 11. Process Execution Support Flow

MVP does not require full workflow automation.

Instead, process execution support follows this pattern:

```text
User opens process
↓
Process steps are visible
↓
Related tasks are created or linked
↓
Agent may suggest next action
↓
Decision may be logged
↓
Memory captures useful context
↓
Audit records important changes
```

---

# 12. Process Events

Minimum events:

```text
process.suggested
process.created
process.updated
process.step_added
process.owner_assigned
process.linked_to_function
process.linked_to_agent
process.linked_to_task
process.reviewed
process.improved
process.archived
```

Events must include:

```text
event_id
workspace_id
process_id
actor_id
event_type
timestamp
payload
```

---

# 13. Process Audit Requirements

Audit events are required for:

- process creation;
- owner assignment;
- function link changes;
- agent link changes;
- step changes;
- status changes;
- archival;
- AI-generated process drafts confirmed by user.

Audit question:

```text
Who changed the process, what changed, when, and what operational object was affected?
```

---

# 14. Process Memory Integration

Process Runtime should create memory from:

- confirmed process definitions;
- process reviews;
- lessons learned;
- recurring issues;
- process changes;
- process-related decisions.

Memory types:

```text
process_definition
process_lesson
process_change
process_decision
process_gap
```

Memory must remain linked to source process and workspace.

---

# 15. Process Dashboard Integration

Dashboard should show:

- active processes;
- suggested processes;
- processes without owners;
- processes without linked functions;
- process coverage by function;
- recently updated processes;
- process gaps;
- process-related tasks.

Dashboard question:

```text
Which recurring business activities are structured, owned and visible?
```

---

# 16. Process Security Boundary

Process Runtime must enforce:

```text
Process belongs to one workspace.
Process must reference workspace_id.
Only authorized workspace users may create or edit process data.
AI-generated process drafts require human confirmation.
Archived processes cannot receive normal updates except restore or audit actions.
Process memory must be scoped to workspace.
Process audit must be scoped to workspace.
```

---

# 17. Process Context Model

Process context may include:

- workspace profile;
- linked function;
- process owner;
- related tasks;
- related decisions;
- linked agents;
- relevant memory entries;
- current process gaps;
- recent audit events.

This context supports AI recommendations and dashboard insights.

---

# 18. Process API Boundary

Suggested API group:

```text
/processes
```

Minimum endpoints:

```text
POST /workspaces/{workspace_id}/processes
GET /workspaces/{workspace_id}/processes
GET /workspaces/{workspace_id}/processes/{process_id}
PATCH /workspaces/{workspace_id}/processes/{process_id}
POST /workspaces/{workspace_id}/processes/{process_id}/archive
POST /workspaces/{workspace_id}/processes/{process_id}/steps
POST /workspaces/{workspace_id}/processes/{process_id}/review
```

Future endpoints:

```text
GET /workspaces/{workspace_id}/processes/{process_id}/audit
GET /workspaces/{workspace_id}/processes/{process_id}/memory
POST /workspaces/{workspace_id}/processes/{process_id}/improve
POST /workspaces/{workspace_id}/processes/{process_id}/tasks
```

---

# 19. Process Service Responsibilities

`ProcessRuntimeService` responsibilities:

- create process suggestions;
- create process records;
- define process purpose;
- manage process lifecycle;
- add and update process steps;
- assign process owner;
- link process to function;
- link process to agent;
- link process to tasks and decisions;
- emit process events;
- trigger audit recording;
- trigger memory creation;
- expose process status to dashboard.

---

# 20. Process Data Validation

Required validation:

- workspace_id is required;
- process name is required;
- process purpose is recommended;
- function link is recommended;
- owner is required for active state;
- archived processes cannot be edited normally;
- AI-generated process drafts must remain draft until confirmed;
- process steps must preserve order.

---

# 21. MVP Acceptance Criteria

Process Runtime is MVP-ready when:

- user can create a process;
- Bizzi can suggest a process from gaps or repeated tasks;
- user can define purpose and steps;
- user can link process to function;
- user can assign process owner;
- process can be linked to tasks or decisions;
- process changes create audit events;
- process definitions can create memory entries;
- dashboard shows process coverage and process gaps.

---

# 22. Out of Scope for MVP

The MVP does not require:

- BPMN editor;
- complex workflow automation;
- process simulation;
- approval chains;
- external workflow integrations;
- robotic process automation;
- process mining;
- advanced SLA management;
- cross-company process orchestration.

---

# 23. Architecture Alignment

| Process Runtime Area | Architecture Reference |
|---|---|
| Process Object | Process Architecture |
| Process Owner | Governance Baseline |
| Function Link | Enterprise Function Registry |
| Process Steps | Operating Model |
| Process Tasks | Enterprise Operations |
| Process Decisions | Decision Routing |
| Process Memory | Enterprise Memory |
| Process Audit | Observability and Intelligence |
| Process Dashboard | Core User Journey |
| Process Agent Support | Agent Library / AI Governance |

---

# 24. Final Process Runtime Statement

```text
Process Runtime is the component that turns informal recurring work into structured, owned, visible and reusable business processes connected to functions, agents, tasks, decisions, memory and audit.
```

This component allows Bizzi to move from operating clarity toward repeatable execution.