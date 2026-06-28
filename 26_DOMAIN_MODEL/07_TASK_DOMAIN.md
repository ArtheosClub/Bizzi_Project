# 07_TASK_DOMAIN.md

# Bizzi Platform

## Task Domain

**Layer:** 26_DOMAIN_MODEL  
**Component Type:** Domain Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 06_TASK_RUNTIME.md  
**Previous Documents:** 00_DOMAIN_MODEL_VISION.md, 01_ENTITY_CATALOG.md, 02_WORKSPACE_DOMAIN.md, 03_OPERATING_MAP_DOMAIN.md, 04_FUNCTION_AND_RESPONSIBILITY_DOMAIN.md, 05_AGENT_DOMAIN.md, 06_PROCESS_DOMAIN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Task Domain for Bizzi Platform.

The Task Domain describes how Bizzi represents actionable work as owned, visible, traceable and auditable operating objects inside a company workspace.

Core question:

```text
How does Bizzi turn operating gaps, process needs, decisions and agent recommendations into concrete work that has an owner, status and business context?
```

---

# 2. Domain Role

The Task Domain is the execution bridge between operating structure and daily action.

It provides:

- actionable work items;
- ownership assignment;
- task status tracking;
- priority and due-date handling;
- linkage to functions, processes, decisions and agents;
- support for operating gap resolution;
- memory and audit traceability;
- dashboard visibility;
- future workflow and project management expansion.

---

# 3. Domain Principle

```text
No Lost Tasks
```

Important work should not remain hidden in chats, notes or informal decisions.

Every important action should become a task or be explicitly rejected as not actionable.

A task should answer:

```text
What needs to happen?
Who owns it?
Why does it exist?
What is its status?
Which business object is it connected to?
```

---

# 4. Aggregate Boundary

Primary aggregate root:

```text
Task
```

Supporting entities:

```text
TaskComment
TaskHistory
TaskLink
TaskStatus
TaskPriority
TaskSource
TaskAssignment
TaskBlocker
```

Related external entities:

```text
CompanyWorkspace
User
Function
Responsibility
OperatingGap
Process
Decision
Agent
AgentRecommendation
MemoryEntry
AuditEvent
RuntimeEvent
DashboardMetric
```

---

# 5. Core Entities

## 5.1 Task

Represents a concrete unit of actionable work.

Minimum domain attributes:

```text
id
workspace_id
title
description
status
priority
owner_user_id
created_at
updated_at
created_by
```

Optional domain attributes:

```text
function_id
process_id
decision_id
agent_id
operating_gap_id
source_object_type
source_object_id
due_date
completed_at
archived_at
blocked_reason
confirmed_by
confirmed_at
```

Domain responsibility:

```text
Task defines work that should be owned, tracked, connected and visible.
```

---

## 5.2 TaskLink

Represents a relationship between a task and another domain object.

Potential attributes:

```text
id
workspace_id
task_id
linked_object_type
linked_object_id
link_type
created_at
created_by
```

Domain responsibility:

```text
TaskLink preserves traceability between work and its business context.
```

MVP simplification:

```text
Task may initially store direct foreign references such as function_id, process_id and decision_id.
```

---

## 5.3 TaskHistory

Represents important task changes over time.

Potential attributes:

```text
id
workspace_id
task_id
action
before_state
after_state
actor_id
created_at
```

Domain responsibility:

```text
TaskHistory preserves the change trail of work execution.
```

MVP simplification:

```text
TaskHistory may be represented through AuditEvent until detailed task history is needed.
```

---

## 5.4 TaskComment

Represents discussion or clarification attached to a task.

Potential attributes:

```text
id
workspace_id
task_id
author_user_id
content
created_at
updated_at
```

Domain responsibility:

```text
TaskComment captures supporting context without replacing task status or ownership.
```

MVP status:

```text
Optional
```

---

## 5.5 TaskBlocker

Represents an obstacle preventing task progress.

Potential attributes:

```text
id
workspace_id
task_id
blocker_type
description
severity
status
created_at
resolved_at
```

Domain responsibility:

```text
TaskBlocker makes execution obstacles visible and actionable.
```

MVP simplification:

```text
Blockers may initially be represented by task status = blocked and blocked_reason.
```

---

# 6. Task Types

Initial task types:

```text
operating_gap_task
function_setup_task
responsibility_assignment_task
process_documentation_task
decision_followup_task
agent_recommendation_task
management_review_task
risk_review_task
memory_review_task
integration_followup_task
```

MVP may begin with:

```text
operating_gap_task
responsibility_assignment_task
process_documentation_task
decision_followup_task
agent_recommendation_task
```

---

# 7. Task Statuses

Recommended lifecycle:

```text
suggested
↓
draft
↓
open
↓
in_progress
↓
blocked
↓
completed
↓
archived
```

MVP lifecycle:

```text
suggested
open
in_progress
completed
archived
```

Optional MVP status:

```text
blocked
```

---

# 8. Task Priorities

Suggested priority values:

```text
low
normal
high
urgent
```

MVP default:

```text
normal
```

Priority should be used to support dashboard ordering, not to replace ownership or due dates.

---

# 9. Task Sources

A task may originate from:

```text
manual_user_input
operating_gap
operating_recommendation
function_gap
responsibility_gap
process_gap
decision_followup
agent_recommendation
memory_review
audit_warning
integration_event
```

Source traceability is important for understanding why a task exists.

---

# 10. Domain Relationships

## 10.1 Workspace to Task

```text
CompanyWorkspace 1 → many Tasks
```

## 10.2 Task to Owner

```text
Task many → 1 User
```

MVP rule:

```text
Open Task should have an owner or be explicitly marked as unassigned.
```

## 10.3 Function to Task

```text
Function 1 → many Tasks
```

## 10.4 Process to Task

```text
Process 1 → many Tasks
```

## 10.5 Decision to Task

```text
Decision 1 → many follow-up Tasks
```

## 10.6 Agent to Task

```text
Agent may suggest, draft or support Tasks
```

## 10.7 OperatingGap to Task

```text
OperatingGap may be resolved by one or more Tasks
```

---

# 11. Domain Invariants

The Task Domain must enforce:

```text
Task must belong to one workspace.
Task title is required.
Task status must be valid.
Task priority must be valid if set.
Completed task must have completed_at.
Archived tasks cannot receive normal updates.
AI-generated tasks remain suggested or draft until confirmed.
Task owner changes must be auditable.
Task source should be traceable where applicable.
Task completion may create memory if outcome is important.
```

---

# 12. AI Suggestion Rules

AI may suggest:

- tasks from operating gaps;
- tasks from missing responsibility;
- tasks from process gaps;
- follow-up tasks from decisions;
- review tasks from memory candidates;
- risk review tasks;
- task summaries;
- next-action recommendations.

AI may not automatically:

- mark important tasks completed;
- assign final human accountability without confirmation;
- delete tasks;
- hide overdue or blocked tasks;
- execute external actions;
- bypass audit.

MVP rule:

```text
AI may suggest work. Human confirms active work and completion.
```

---

# 13. Task Creation Flow

```text
Gap, process need, decision or agent recommendation detected
↓
Task suggestion created
↓
User reviews or accepts task
↓
Owner assigned
↓
Function, process or decision linked
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

# 14. Task Execution Flow

```text
Task opened
↓
Owner begins work
↓
Status changes to in_progress
↓
Task may become blocked
↓
Owner completes task
↓
Completion event recorded
↓
Related gap or decision updated if applicable
↓
Audit event recorded
↓
Memory created if useful
↓
Dashboard updated
```

---

# 15. Task Assignment Flow

```text
Task created or suggested
↓
Responsible function identified
↓
Existing responsibility checked
↓
Owner suggested or selected
↓
User confirms assignment
↓
Task owner set
↓
Ownership gap resolved if applicable
↓
Audit event recorded
```

---

# 16. Domain Events

Task events:

```text
task.suggested
task.created
task.confirmed
task.assigned
task.unassigned
task.updated
task.status_changed
task.priority_changed
task.due_date_changed
task.linked_to_function
task.linked_to_process
task.linked_to_decision
task.linked_to_agent
task.blocked
task.unblocked
task.completed
task.archived
```

---

# 17. Audit Requirements

Audited actions:

```text
task.created
task.confirmed
task.assigned
task.updated
task.status_changed
task.priority_changed
task.due_date_changed
task.linked_to_object
task.blocked
task.completed
task.archived
```

Audit must answer:

```text
Who created or changed the task, what changed, when, and which business object is it connected to?
```

---

# 18. Memory Requirements

Memory may be created from:

- completed important tasks;
- recurring task patterns;
- blocked task causes;
- task outcomes;
- task-related decisions;
- lessons learned.

Memory types:

```text
task_context
task_outcome
task_lesson
task_blocker
task_pattern
```

---

# 19. Dashboard Requirements

Dashboard should show:

- open tasks;
- tasks by owner;
- tasks by function;
- unassigned tasks;
- overdue tasks;
- blocked tasks;
- completed tasks;
- suggested tasks;
- tasks linked to operating gaps;
- decision follow-up tasks.

Dashboard question:

```text
What needs to happen next, who owns it, and what is blocked?
```

---

# 20. Security Requirements

Security requirements:

```text
Task belongs to one workspace.
Only authorized workspace users may create or edit tasks.
AI-generated tasks remain suggested until confirmed.
Archived tasks cannot be edited through normal flows.
Task audit must be workspace-scoped.
Task memory must be workspace-scoped.
Task exports require authorization.
```

---

# 21. MVP Domain Behavior

MVP should support:

```text
Create task
Suggest task from operating gap
Confirm suggested task
Assign owner
Set priority
Set due date
Link task to function
Link task to process
Link task to decision
Update status
Complete task
Archive task
Create audit events
Create memory from important task outcomes
Show task metrics on dashboard
```

---

# 22. Out of Scope for MVP

The Task Domain does not need in MVP:

- full project management suite;
- Gantt charts;
- complex dependencies;
- recurring task automation;
- external task tool sync;
- workload balancing;
- SLA engine;
- kanban customization;
- autonomous execution.

---

# 23. Data Model Implications

Future Data Model should include tables or collections for:

```text
tasks
```

Potential later tables:

```text
task_links
task_history
task_comments
task_blockers
task_assignments
```

Recommended indexes later:

```text
tasks.workspace_id
tasks.owner_user_id
tasks.status
tasks.priority
tasks.function_id
tasks.process_id
tasks.decision_id
tasks.agent_id
tasks.due_date
tasks.source_object_type
tasks.source_object_id
```

---

# 24. API Implications

Future API contracts should support:

```text
POST /workspaces/{workspace_id}/tasks
GET /workspaces/{workspace_id}/tasks
GET /workspaces/{workspace_id}/tasks/{task_id}
PATCH /workspaces/{workspace_id}/tasks/{task_id}
POST /workspaces/{workspace_id}/tasks/{task_id}/assign
POST /workspaces/{workspace_id}/tasks/{task_id}/complete
POST /workspaces/{workspace_id}/tasks/{task_id}/archive
POST /workspaces/{workspace_id}/tasks/{task_id}/link
```

---

# 25. Traceability Pattern

Task traceability chain:

```text
OperatingGap / Process / Decision / AgentRecommendation / User Input
↓
Task
↓
TaskStatus / TaskOwner / TaskLink
↓
Runtime Event
↓
Audit Event
↓
Memory Entry
↓
Dashboard Metric
```

---

# 26. Acceptance Criteria

Task Domain is ready when:

- Task is defined as aggregate root;
- task lifecycle is clear;
- ownership rules are explicit;
- source traceability is defined;
- AI task suggestion rules are defined;
- audit and memory behavior are defined;
- dashboard role is defined;
- data model and API implications are identified.

Status:

```text
Ready for Data Model and API Design
```

---

# 27. Architecture Alignment

| Task Domain Area | Reference |
|---|---|
| Task | 06_TASK_RUNTIME.md |
| Task Owner | Function and Responsibility Domain |
| Task Source | Operating Map / Process / Decision / Agent Domains |
| Task Events | Event Runtime |
| Task Audit | Audit Runtime |
| Task Memory | Memory Runtime |
| Task Dashboard | Core User Journey |
| Task Security | Runtime Security |
| Task AI Suggestions | Agent Domain |

---

# 28. Final Task Domain Statement

```text
Task Domain defines how Bizzi represents actionable work as owned, status-tracked, source-linked, auditable and visible operating objects that connect strategy, gaps, processes, decisions and AI recommendations to daily execution.
```

This domain ensures that operating clarity becomes concrete work and that important tasks are not lost.