# 06_TASK_RUNTIME.md

# Bizzi Platform

## Task Runtime

**Layer:** 25_RUNTIME_PLATFORM  
**Component Type:** Runtime Component Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 00_RUNTIME_VISION.md, 01_RUNTIME_ARCHITECTURE.md, 02_CORE_RUNTIME_COMPONENTS.md, 03_WORKSPACE_RUNTIME.md, 04_AGENT_RUNTIME.md, 05_PROCESS_RUNTIME.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Task Runtime for Bizzi Platform.

Task Runtime is responsible for creating, routing, tracking and connecting actionable work inside a company workspace.

Core question:

```text
How does Bizzi turn business gaps, processes, decisions and agent recommendations into owned, visible and auditable tasks?
```

---

# 2. Runtime Role

Task Runtime is the execution bridge between operating structure and daily action.

It links tasks to:

- workspace;
- functions;
- responsibilities;
- human owners;
- AI agents;
- processes;
- decisions;
- memory;
- audit trail;
- dashboard visibility.

---

# 3. Task Runtime Principle

```text
No Lost Tasks
```

Every important action should have:

- owner;
- status;
- priority;
- source;
- workspace scope;
- audit trail;
- dashboard visibility.

---

# 4. Primary Runtime Objects

Minimum objects:

```text
Task
TaskOwner
TaskStatus
TaskPriority
TaskSource
TaskLink
TaskComment
TaskHistory
```

Supporting objects:

```text
CompanyWorkspace
Function
Responsibility
Agent
Process
Decision
MemoryEntry
AuditEvent
RuntimeEvent
```

---

# 5. Task Object

## Purpose

Represents a concrete unit of actionable work inside Bizzi.

## Minimum Fields

```text
id
workspace_id
title
description
owner_id
status
priority
created_at
updated_at
```

## Optional Fields

```text
function_id
process_id
decision_id
agent_id
source_type
source_id
due_date
created_by
completed_at
```

---

# 6. Task Lifecycle

```text
Suggested
↓
Draft
↓
Open
↓
In Progress
↓
Blocked
↓
Completed
↓
Archived
```

## Suggested

Task is recommended by Bizzi from a gap, process, decision or agent output.

## Draft

Task exists but is not yet accepted into active work.

## Open

Task is accepted and waiting for action.

## In Progress

Task is actively being worked on.

## Blocked

Task cannot progress without resolution.

## Completed

Task is finished.

## Archived

Task is retained historically but no longer active.

---

# 7. Task States

```text
suggested
draft
open
in_progress
blocked
completed
archived
```

MVP required states:

```text
suggested
open
in_progress
completed
archived
```

---

# 8. Task Types for MVP

Initial task types:

```text
Operating Gap Task
Function Setup Task
Responsibility Assignment Task
Process Documentation Task
Decision Follow-up Task
Agent Recommendation Task
Management Review Task
```

---

# 9. Core Operations

## 9.1 Suggest Task

Creates a task recommendation from operating gaps, onboarding, process gaps or agent output.

## 9.2 Create Task

Creates a task record inside the workspace.

## 9.3 Assign Task Owner

Assigns a human owner or marks task as unassigned.

## 9.4 Link Task

Links task to function, process, decision, agent or memory source.

## 9.5 Update Task Status

Moves task through its lifecycle.

## 9.6 Set Priority

Defines task urgency or importance.

## 9.7 Set Due Date

Defines expected completion date.

## 9.8 Complete Task

Marks task as completed and records completion event.

## 9.9 Archive Task

Retains task history while removing it from active views.

---

# 10. Task Creation Flow

```text
Gap, process, decision or agent recommendation detected
↓
Task Runtime creates suggested task
↓
User reviews or accepts
↓
Owner assigned
↓
Function or process linked
↓
Task becomes open
↓
Audit event recorded
↓
Dashboard updated
↓
Memory created if useful
```

---

# 11. Task Routing Flow

```text
Task created
↓
Function identified
↓
Responsibility checked
↓
Owner assigned or gap detected
↓
Priority set
↓
Task appears on dashboard
↓
Escalation triggered if unassigned or blocked
```

---

# 12. Task Events

Minimum events:

```text
task.suggested
task.created
task.assigned
task.unassigned
task.updated
task.status_changed
task.priority_changed
task.linked_to_function
task.linked_to_process
task.linked_to_decision
task.linked_to_agent
task.completed
task.archived
```

Events must include:

```text
event_id
workspace_id
task_id
actor_id
event_type
timestamp
payload
```

---

# 13. Task Audit Requirements

Audit events are required for:

- task creation;
- owner assignment;
- status changes;
- priority changes;
- due date changes;
- link changes;
- completion;
- archival;
- AI-generated task confirmation.

Audit question:

```text
Who created or changed the task, what changed, when, and what business object is it connected to?
```

---

# 14. Task Memory Integration

Task Runtime may create memory from:

- completed important tasks;
- recurring task patterns;
- blocked task causes;
- lessons learned;
- task outcomes;
- task-related decisions.

Memory types:

```text
task_context
task_outcome
task_lesson
task_blocker
task_pattern
```

Memory must be linked to workspace and source task.

---

# 15. Task Dashboard Integration

Dashboard should show:

- open tasks;
- tasks by owner;
- tasks by function;
- unassigned tasks;
- overdue tasks;
- blocked tasks;
- completed tasks;
- suggested tasks;
- task gaps created from operating map.

Dashboard question:

```text
What needs to happen next, and who owns it?
```

---

# 16. Task Security Boundary

Task Runtime must enforce:

```text
Task belongs to one workspace.
Task must reference workspace_id.
Only authorized users may create or edit tasks.
AI-generated tasks remain suggested until confirmed.
Archived tasks cannot be edited normally.
Task audit must be scoped to workspace.
Task memory must be scoped to workspace.
```

---

# 17. Task Context Model

Task context may include:

- workspace profile;
- linked function;
- assigned owner;
- linked process;
- linked decision;
- linked agent;
- relevant memory entries;
- status history;
- related audit events.

This context supports AI recommendations, dashboard summaries and future task automation.

---

# 18. Task API Boundary

Suggested API group:

```text
/tasks
```

Minimum endpoints:

```text
POST /workspaces/{workspace_id}/tasks
GET /workspaces/{workspace_id}/tasks
GET /workspaces/{workspace_id}/tasks/{task_id}
PATCH /workspaces/{workspace_id}/tasks/{task_id}
POST /workspaces/{workspace_id}/tasks/{task_id}/assign
POST /workspaces/{workspace_id}/tasks/{task_id}/complete
POST /workspaces/{workspace_id}/tasks/{task_id}/archive
```

Future endpoints:

```text
GET /workspaces/{workspace_id}/tasks/{task_id}/audit
GET /workspaces/{workspace_id}/tasks/{task_id}/memory
POST /workspaces/{workspace_id}/tasks/{task_id}/block
POST /workspaces/{workspace_id}/tasks/{task_id}/link
```

---

# 19. Task Service Responsibilities

`TaskRuntimeService` responsibilities:

- create task suggestions;
- create task records;
- assign owners;
- update task status;
- set priority;
- set due date;
- link task to functions, processes, decisions and agents;
- emit task events;
- trigger audit recording;
- trigger memory creation where useful;
- expose task metrics to dashboard.

---

# 20. Task Data Validation

Required validation:

- workspace_id is required;
- task title is required;
- status must be valid;
- priority must be valid if set;
- owner is recommended for open tasks;
- completed tasks require completed_at;
- archived tasks cannot be edited normally;
- AI-generated tasks must remain suggested until confirmed.

---

# 21. MVP Acceptance Criteria

Task Runtime is MVP-ready when:

- user can create a task;
- Bizzi can suggest tasks from operating gaps;
- task can be assigned to an owner;
- task can be linked to function or process;
- task status can be updated;
- task completion is recorded;
- task events create audit records;
- task data appears on dashboard;
- task outcomes can create memory entries when useful.

---

# 22. Out of Scope for MVP

The MVP does not require:

- advanced project management;
- Gantt charts;
- complex dependencies;
- external task tool integration;
- recurring task automation;
- SLA engine;
- advanced workload balancing;
- autonomous task execution.

---

# 23. Architecture Alignment

| Task Runtime Area | Architecture Reference |
|---|---|
| Task Object | Operating Model |
| Task Owner | Governance Baseline |
| Function Link | Enterprise Function Registry |
| Process Link | Process Architecture |
| Agent Link | Agent Library / AI Governance |
| Decision Link | Decision Routing |
| Task Memory | Enterprise Memory |
| Task Audit | Observability and Intelligence |
| Task Dashboard | Core User Journey |

---

# 24. Final Task Runtime Statement

```text
Task Runtime is the component that turns operating gaps, process needs, decisions and agent recommendations into owned, visible, trackable and auditable work.
```

This component ensures Bizzi can move from operating clarity to daily execution.