# 06_PROCESS_DOMAIN.md

# Bizzi Platform

## Process Domain

**Layer:** 26_DOMAIN_MODEL  
**Component Type:** Domain Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 05_PROCESS_RUNTIME.md  
**Previous Documents:** 00_DOMAIN_MODEL_VISION.md, 01_ENTITY_CATALOG.md, 02_WORKSPACE_DOMAIN.md, 03_OPERATING_MAP_DOMAIN.md, 04_FUNCTION_AND_RESPONSIBILITY_DOMAIN.md, 05_AGENT_DOMAIN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Process Domain for Bizzi Platform.

The Process Domain describes how Bizzi represents repeatable business activities as structured, owned, reviewable and reusable operating objects inside a company workspace.

Core question:

```text
How does Bizzi turn recurring business work into structured processes that can connect functions, owners, agents, tasks, decisions, memory and audit?
```

---

# 2. Domain Role

The Process Domain connects operating clarity to repeatable execution.

It provides:

- lightweight process definition;
- process ownership;
- process steps;
- input and output visibility;
- links to functions and responsibilities;
- agent support;
- task generation;
- decision linkage;
- memory capture;
- audit traceability;
- dashboard process coverage.

---

# 3. Domain Principle

```text
Process First, Automation Later
```

Bizzi should first make recurring work visible and understandable before attempting advanced workflow automation.

A process may begin as a simple draft and later mature into a formal workflow.

---

# 4. Aggregate Boundary

Primary aggregate root:

```text
Process
```

Supporting entities:

```text
ProcessStep
ProcessInput
ProcessOutput
ProcessOwner
ProcessGap
ProcessReview
ProcessStatus
```

Related external entities:

```text
CompanyWorkspace
Function
Responsibility
User
Agent
Task
Decision
MemoryEntry
AuditEvent
RuntimeEvent
OperatingGap
OperatingRecommendation
DashboardMetric
```

---

# 5. Core Entities

## 5.1 Process

Represents a repeatable business activity or operating procedure.

Minimum domain attributes:

```text
id
workspace_id
name
purpose
function_id
owner_user_id
status
created_at
updated_at
created_by
```

Optional domain attributes:

```text
description
trigger
frequency
risk_level
maturity_level
success_criteria
agent_id
source_object_type
source_object_id
confirmed_by
confirmed_at
last_reviewed_at
archived_at
```

Domain responsibility:

```text
Process defines repeatable work that should be visible, owned and connected to execution.
```

---

## 5.2 ProcessStep

Represents an ordered step inside a process.

Minimum domain attributes:

```text
id
workspace_id
process_id
step_order
title
status
created_at
updated_at
```

Optional domain attributes:

```text
description
responsible_user_id
expected_input
expected_output
automation_candidate
agent_assist_allowed
```

Domain responsibility:

```text
ProcessStep preserves the structure and order of a process.
```

---

## 5.3 ProcessInput

Represents information, resource or trigger needed by a process.

Potential attributes:

```text
id
workspace_id
process_id
name
description
source_type
source_object_id
required
```

Domain responsibility:

```text
ProcessInput defines what a process needs before it can operate.
```

MVP simplification:

```text
Process inputs may initially be stored as structured fields on Process.
```

---

## 5.4 ProcessOutput

Represents a result produced by a process.

Potential attributes:

```text
id
workspace_id
process_id
name
description
output_type
linked_object_type
linked_object_id
```

Domain responsibility:

```text
ProcessOutput defines what a process produces and how it connects to execution or memory.
```

---

## 5.5 ProcessGap

Represents a weakness or missing element inside a process.

Potential attributes:

```text
id
workspace_id
process_id
gap_type
title
description
severity
status
created_at
updated_at
```

Domain responsibility:

```text
ProcessGap identifies process weaknesses that may become tasks, decisions or improvements.
```

---

## 5.6 ProcessReview

Represents an evaluation of process quality, accuracy or usefulness.

Potential attributes:

```text
id
workspace_id
process_id
reviewed_by
reviewed_at
summary
result
recommended_changes
```

Domain responsibility:

```text
ProcessReview preserves learning and improvement context for recurring work.
```

---

# 6. Process Types

Initial process types:

```text
operational_process
customer_process
sales_process
finance_process
hr_process
procurement_process
support_process
management_rhythm_process
risk_control_process
```

MVP may begin with:

```text
operational_process
sales_process
finance_process
management_rhythm_process
```

---

# 7. Process Lifecycle

Recommended lifecycle:

```text
suggested
↓
draft
↓
defined
↓
active
↓
reviewed
↓
improved
↓
archived
```

MVP lifecycle:

```text
suggested
draft
active
archived
```

---

# 8. Process Step Lifecycle

Recommended lifecycle:

```text
draft
↓
active
↓
changed
↓
removed
```

MVP lifecycle:

```text
active
removed
```

---

# 9. Domain Relationships

## 9.1 Workspace to Process

```text
CompanyWorkspace 1 → many Processes
```

## 9.2 Function to Process

```text
Function 1 → many Processes
```

## 9.3 Process to Owner

```text
Process many → 1 User
```

MVP rule:

```text
Active Process should have an owner_user_id.
```

## 9.4 Process to Steps

```text
Process 1 → many ProcessSteps
```

## 9.5 Process to Agent

```text
Process may be supported by Agent
```

## 9.6 Process to Task and Decision

```text
Process → many Tasks
Process → many Decisions
```

---

# 10. Domain Invariants

The Process Domain must enforce:

```text
Process must belong to one workspace.
Active Process should have an owner.
Process should link to a function when possible.
Process steps must preserve order.
Archived processes cannot receive normal operational updates.
AI-generated process drafts require confirmation before becoming authoritative.
Process changes must be auditable.
Confirmed process definitions may create memory entries.
```

---

# 11. AI Suggestion Rules

AI may suggest:

- process drafts;
- process steps;
- missing process gaps;
- possible owners;
- improvement opportunities;
- tasks from process gaps;
- memory candidates from process definitions.

AI may not automatically:

- make a process official without confirmation;
- assign final accountability;
- delete process history;
- mark process risk resolved;
- bypass audit;
- execute external workflow actions in MVP.

MVP rule:

```text
AI may draft process structure. Human confirms operating procedure.
```

---

# 12. Process Creation Flow

```text
Operating gap or recurring work detected
↓
Process suggestion created
↓
AI drafts process outline if enabled
↓
User reviews and edits
↓
Function linked
↓
Owner assigned
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

# 13. Process Review Flow

```text
Process selected for review
↓
Owner checks purpose, steps and outputs
↓
Gaps or improvements identified
↓
Tasks or decisions created if needed
↓
Review recorded
↓
Memory updated
↓
Audit event recorded
↓
Dashboard refreshed
```

---

# 14. Domain Events

Process events:

```text
process.suggested
process.created
process.updated
process.step_added
process.step_updated
process.step_removed
process.owner_assigned
process.linked_to_function
process.linked_to_agent
process.reviewed
process.improved
process.archived
```

Gap and review events:

```text
process_gap.detected
process_gap.resolved
process_review.created
```

---

# 15. Audit Requirements

Audited actions:

```text
process.created
process.updated
process.step_added
process.step_updated
process.step_removed
process.owner_assigned
process.linked_to_function
process.linked_to_agent
process.reviewed
process.archived
```

Audit must answer:

```text
Who changed the process, what changed, when, and which operating object was affected?
```

---

# 16. Memory Requirements

Memory may be created from:

- confirmed process definitions;
- process reviews;
- lessons learned;
- recurring process issues;
- process-related decisions;
- process improvements.

Memory types:

```text
process_definition
process_lesson
process_change
process_decision
process_gap
process_review
```

---

# 17. Dashboard Requirements

Dashboard should show:

- active processes;
- processes by function;
- processes without owners;
- suggested processes;
- recently updated processes;
- process gaps;
- process-related tasks;
- process coverage by function.

Dashboard question:

```text
Which recurring activities are structured, owned and ready for execution?
```

---

# 18. Security Requirements

Security requirements:

```text
Process belongs to one workspace.
Only authorized workspace users may create or edit processes.
AI-generated process drafts remain draft until confirmed.
Archived processes cannot be edited through normal flows.
Process memory must be workspace-scoped.
Process audit must be workspace-scoped.
```

---

# 19. MVP Domain Behavior

MVP should support:

```text
Create process
Suggest process from operating gap
Define process purpose
Add ordered process steps
Link process to function
Assign process owner
Link process to tasks and decisions
Review process
Archive process
Create audit events
Create memory from confirmed process definition
Show process status on dashboard
```

---

# 20. Out of Scope for MVP

The Process Domain does not need in MVP:

- BPMN editor;
- workflow automation engine;
- process simulation;
- approval chains;
- process mining;
- RPA integration;
- SLA engine;
- complex dependency graph;
- external workflow execution.

---

# 21. Data Model Implications

Future Data Model should include tables or collections for:

```text
processes
process_steps
```

Potential later tables:

```text
process_inputs
process_outputs
process_gaps
process_reviews
```

Recommended indexes later:

```text
processes.workspace_id
processes.function_id
processes.owner_user_id
processes.status
process_steps.workspace_id
process_steps.process_id
process_steps.step_order
```

---

# 22. API Implications

Future API contracts should support:

```text
POST /workspaces/{workspace_id}/processes
GET /workspaces/{workspace_id}/processes
GET /workspaces/{workspace_id}/processes/{process_id}
PATCH /workspaces/{workspace_id}/processes/{process_id}
POST /workspaces/{workspace_id}/processes/{process_id}/archive
POST /workspaces/{workspace_id}/processes/{process_id}/steps
PATCH /workspaces/{workspace_id}/processes/{process_id}/steps/{step_id}
POST /workspaces/{workspace_id}/processes/{process_id}/review
```

---

# 23. Traceability Pattern

Process traceability chain:

```text
OperatingGap / Function / User Input
↓
Process
↓
ProcessStep
↓
Task / Decision / Agent Recommendation
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

# 24. Acceptance Criteria

Process Domain is ready when:

- Process is defined as aggregate root;
- ProcessStep is defined;
- process lifecycle is clear;
- process ownership rules are explicit;
- AI process drafting rules are defined;
- audit and memory behavior are defined;
- dashboard role is defined;
- data model and API implications are identified.

Status:

```text
Ready for Data Model and API Design
```

---

# 25. Architecture Alignment

| Process Domain Area | Reference |
|---|---|
| Process | 05_PROCESS_RUNTIME.md |
| ProcessStep | Process Runtime |
| Process Owner | Function and Responsibility Domain |
| Process Gap | Operating Map Domain / Task Runtime |
| Agent Support | Agent Domain |
| Process Tasks | Task Runtime |
| Process Decisions | Decision Runtime |
| Process Memory | Memory Runtime |
| Process Audit | Audit Runtime |
| Process Events | Event Runtime |
| Process Dashboard | Core User Journey |

---

# 26. Final Process Domain Statement

```text
Process Domain defines how Bizzi represents recurring business work as structured, owned, reviewable and reusable operating processes connected to functions, agents, tasks, decisions, memory, audit and dashboard visibility.
```

This domain allows Bizzi to move from operating clarity toward repeatable execution.