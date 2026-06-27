# 08_MEMORY_RUNTIME.md

# Bizzi Platform

## Memory Runtime

**Layer:** 25_RUNTIME_PLATFORM  
**Component Type:** Runtime Component Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 00_RUNTIME_VISION.md, 01_RUNTIME_ARCHITECTURE.md, 02_CORE_RUNTIME_COMPONENTS.md, 03_WORKSPACE_RUNTIME.md, 04_AGENT_RUNTIME.md, 05_PROCESS_RUNTIME.md, 06_TASK_RUNTIME.md, 07_DECISION_RUNTIME.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Memory Runtime for Bizzi Platform.

Memory Runtime is responsible for creating, storing, classifying, linking and retrieving structured enterprise memory inside a company workspace.

Core question:

```text
How does Bizzi ensure that company knowledge, decisions, context, processes, lessons and operating history are preserved as reusable structured memory?
```

---

# 2. Runtime Role

Memory Runtime is the knowledge persistence layer of Bizzi.

It connects memory to:

- workspace;
- functions;
- responsibilities;
- agents;
- processes;
- tasks;
- decisions;
- audit events;
- dashboard insights;
- AI orchestration.

---

# 3. Memory Runtime Principle

```text
Memory by Default, Traceability Always
```

Useful operating context should become memory only when it has a clear source, scope and purpose.

Memory must not become an unverified text dump.

Every memory entry should answer:

```text
What is remembered?
Where did it come from?
Why is it useful?
Who or what created it?
Can it be trusted?
```

---

# 4. Primary Runtime Objects

Minimum objects:

```text
MemoryEntry
MemoryType
MemorySource
MemoryStatus
MemoryScope
MemoryConfidence
MemoryLink
MemoryHistory
```

Supporting objects:

```text
CompanyWorkspace
Function
Responsibility
Agent
Process
Task
Decision
AuditEvent
RuntimeEvent
DashboardMetric
```

---

# 5. MemoryEntry Object

## Purpose

Represents a reusable piece of enterprise knowledge inside a workspace.

## Minimum Fields

```text
id
workspace_id
memory_type
content
source_object_type
source_object_id
status
created_at
updated_at
```

## Optional Fields

```text
title
summary
confidence
created_by
agent_id
function_id
process_id
task_id
decision_id
tags
valid_from
valid_until
review_required
```

---

# 6. Memory Lifecycle

```text
Candidate
↓
Draft
↓
Confirmed
↓
Active
↓
Reviewed
↓
Updated
↓
Archived
```

## Candidate

Memory is suggested by system or AI but not yet accepted.

## Draft

Memory is being reviewed or edited.

## Confirmed

Memory is accepted as valid by user or governed system logic.

## Active

Memory is available for retrieval and dashboard insights.

## Reviewed

Memory has been checked for accuracy.

## Updated

Memory has been revised with newer context.

## Archived

Memory is retained historically but not used as active context.

---

# 7. Memory States

```text
candidate
draft
confirmed
active
reviewed
updated
archived
```

MVP required states:

```text
candidate
active
archived
```

---

# 8. Memory Types for MVP

Initial memory types:

```text
company_context
owner_goal
operating_pain_point
function_context
responsibility_context
agent_recommendation
process_definition
process_lesson
task_context
task_outcome
decision_context
decision_rationale
decision_outcome
audit_summary
```

The MVP should keep memory taxonomy simple and expandable.

---

# 9. Core Operations

## 9.1 Create Memory Entry

Creates a memory entry from a source object or user input.

## 9.2 Suggest Memory Candidate

Creates a memory candidate from AI output, decisions, tasks, process changes or onboarding context.

## 9.3 Confirm Memory

Marks memory as accepted and usable.

## 9.4 Link Memory to Source

Connects memory to its originating runtime object.

## 9.5 Classify Memory

Assigns memory type, scope and tags.

## 9.6 Retrieve Memory

Returns relevant memory for workspace, function, process, task, decision or agent context.

## 9.7 Review Memory

Allows user or governed process to validate accuracy.

## 9.8 Archive Memory

Removes memory from active retrieval while preserving history.

---

# 10. Memory Creation Flow

```text
Meaningful runtime activity occurs
↓
Memory Runtime detects memory opportunity
↓
Memory candidate is created
↓
Source object is linked
↓
Memory type is assigned
↓
User or system confirms memory
↓
Audit event recorded
↓
Memory becomes active
↓
Dashboard and AI context can use it
```

---

# 11. AI-Assisted Memory Flow

```text
AI analyzes structured context
↓
AI suggests memory candidate
↓
Memory Runtime validates required fields
↓
User reviews candidate if needed
↓
Candidate is confirmed or rejected
↓
Confirmed memory becomes active
↓
Audit records source and confirmation
```

MVP rule:

```text
AI may suggest memory. Bizzi must preserve source traceability.
```

---

# 12. Memory Events

Minimum events:

```text
memory.candidate_created
memory.created
memory.confirmed
memory.updated
memory.reviewed
memory.linked_to_source
memory.used_in_context
memory.archived
memory.rejected
```

Events must include:

```text
event_id
workspace_id
memory_id
actor_id
event_type
timestamp
payload
```

---

# 13. Memory Audit Requirements

Audit events are required for:

- memory creation;
- AI-generated memory candidate creation;
- memory confirmation;
- memory update;
- memory archival;
- memory retrieval for AI context;
- memory source changes;
- memory rejection.

Audit question:

```text
What memory was created or used, where did it come from, who confirmed it, and how was it applied?
```

---

# 14. Memory Source Model

Every memory entry should have a source.

Source object types:

```text
workspace
onboarding
operating_map
function
responsibility
agent
process
task
decision
audit_event
manual_note
```

Minimum source fields:

```text
source_object_type
source_object_id
source_created_at
source_actor_id
```

---

# 15. Memory Retrieval Model

Memory retrieval should support:

- workspace-level context;
- function-level context;
- process-level context;
- task-level context;
- decision-level context;
- agent-specific context;
- dashboard summaries.

Retrieval should prefer:

- active memory;
- recent memory;
- confirmed memory;
- memory linked to current object;
- memory with clear source.

---

# 16. Memory Dashboard Integration

Dashboard should show:

- total memory entries;
- recent memory;
- memory by type;
- memory created from decisions;
- memory created from processes;
- memory candidates needing review;
- archived memory count;
- knowledge coverage gaps.

Dashboard question:

```text
What does the company know, and what important knowledge has been preserved?
```

---

# 17. Memory Security Boundary

Memory Runtime must enforce:

```text
Memory belongs to one workspace.
Memory must reference workspace_id.
Memory retrieval must respect workspace access.
AI context may only use memory scoped to the workspace.
Archived memory should not be used as active AI context.
Memory source must not be hidden.
Memory audit must be scoped to workspace.
```

---

# 18. Memory Context Model

Memory context may include:

- memory content;
- memory type;
- source object;
- linked function;
- linked process;
- linked task;
- linked decision;
- linked agent;
- confidence;
- status;
- review state;
- audit references.

This context supports AI recommendations, dashboard summaries and future knowledge retrieval.

---

# 19. Memory API Boundary

Suggested API group:

```text
/memory
```

Minimum endpoints:

```text
POST /workspaces/{workspace_id}/memory
GET /workspaces/{workspace_id}/memory
GET /workspaces/{workspace_id}/memory/{memory_id}
PATCH /workspaces/{workspace_id}/memory/{memory_id}
POST /workspaces/{workspace_id}/memory/{memory_id}/confirm
POST /workspaces/{workspace_id}/memory/{memory_id}/archive
GET /workspaces/{workspace_id}/memory/context
```

Future endpoints:

```text
GET /workspaces/{workspace_id}/memory/{memory_id}/audit
POST /workspaces/{workspace_id}/memory/{memory_id}/review
POST /workspaces/{workspace_id}/memory/search
POST /workspaces/{workspace_id}/memory/retrieve-for-agent
```

---

# 20. Memory Service Responsibilities

`MemoryRuntimeService` responsibilities:

- create memory entries;
- create memory candidates;
- classify memory;
- link memory to source objects;
- confirm or reject memory;
- retrieve memory by context;
- archive memory;
- emit memory events;
- trigger audit recording;
- expose memory metrics to dashboard;
- provide scoped memory context to AI orchestration.

---

# 21. Memory Data Validation

Required validation:

- workspace_id is required;
- memory_type is required;
- content is required;
- source_object_type is recommended;
- source_object_id is recommended;
- active memory should have source traceability;
- archived memory cannot be used as active AI context;
- AI-generated memory must identify source agent or source operation.

---

# 22. MVP Acceptance Criteria

Memory Runtime is MVP-ready when:

- memory can be created from onboarding context;
- memory can be created from decisions;
- memory can be created from processes;
- memory can be created from important task outcomes;
- memory entries are linked to source objects;
- memory can be retrieved by workspace context;
- AI can receive scoped memory context;
- memory actions create audit events;
- dashboard shows memory coverage and recent memory.

---

# 23. Out of Scope for MVP

The MVP does not require:

- advanced vector database architecture;
- complex semantic search;
- long-term autonomous learning;
- cross-workspace memory sharing;
- model fine-tuning;
- external knowledge graph;
- automated memory deletion policies;
- enterprise retention policy engine.

---

# 24. Architecture Alignment

| Memory Runtime Area | Architecture Reference |
|---|---|
| MemoryEntry | Enterprise Memory |
| Memory Source | Traceability Matrix |
| Memory Confirmation | Governance Baseline |
| Decision Memory | Decision Routing |
| Process Memory | Process Architecture |
| Task Memory | Operating Model |
| Agent Memory | Agent Library / AI Governance |
| Memory Audit | Observability and Intelligence |
| Memory Dashboard | Core User Journey |

---

# 25. Final Memory Runtime Statement

```text
Memory Runtime is the component that turns meaningful business activity into structured, source-linked, auditable and reusable enterprise memory.
```

This component ensures Bizzi can remember how the company works, why decisions were made, what was learned and what context should guide future action.