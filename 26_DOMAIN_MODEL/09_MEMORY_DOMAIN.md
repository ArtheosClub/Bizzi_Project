# 09_MEMORY_DOMAIN.md

# Bizzi Platform

## Memory Domain

**Layer:** 26_DOMAIN_MODEL  
**Component Type:** Domain Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 08_MEMORY_RUNTIME.md  
**Previous Documents:** 00_DOMAIN_MODEL_VISION.md, 01_ENTITY_CATALOG.md, 02_WORKSPACE_DOMAIN.md, 03_OPERATING_MAP_DOMAIN.md, 04_FUNCTION_AND_RESPONSIBILITY_DOMAIN.md, 05_AGENT_DOMAIN.md, 06_PROCESS_DOMAIN.md, 07_TASK_DOMAIN.md, 08_DECISION_DOMAIN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Memory Domain for Bizzi Platform.

The Memory Domain describes how Bizzi represents reusable enterprise knowledge as structured, source-linked, workspace-scoped and auditable domain objects.

Core question:

```text
How does Bizzi remember useful business context, decisions, lessons, processes and outcomes without turning memory into an uncontrolled text dump?
```

---

# 2. Domain Role

The Memory Domain is the knowledge persistence domain of Bizzi.

It provides:

- structured memory entries;
- source traceability;
- workspace-scoped knowledge;
- memory classification;
- confirmation status;
- confidence and review rules;
- links to tasks, decisions, processes and agents;
- AI context retrieval boundary;
- audit evidence;
- dashboard knowledge coverage.

---

# 3. Domain Principle

```text
Memory by Default, Traceability Always
```

Bizzi should remember useful operating context, but only with clear scope, source and purpose.

Memory must answer:

```text
What is remembered?
Where did it come from?
Why is it useful?
Who or what created it?
Can it be trusted?
When should it be reviewed or archived?
```

---

# 4. Aggregate Boundary

Primary aggregate root:

```text
MemoryEntry
```

Supporting entities:

```text
MemorySource
MemoryLink
MemoryReview
MemoryUsage
MemoryConfidence
MemoryStatus
MemoryTag
```

Related external entities:

```text
CompanyWorkspace
User
Function
Responsibility
Agent
Process
Task
Decision
AuditEvent
RuntimeEvent
DashboardMetric
Integration
```

---

# 5. Core Entities

## 5.1 MemoryEntry

Represents reusable enterprise knowledge inside a workspace.

Minimum domain attributes:

```text
id
workspace_id
memory_type
title
content
status
source_object_type
source_object_id
created_at
updated_at
created_by
```

Optional domain attributes:

```text
summary
confidence
function_id
process_id
task_id
decision_id
agent_id
tags
valid_from
valid_until
review_required
review_date
archived_at
```

Domain responsibility:

```text
MemoryEntry preserves useful operating knowledge as structured, traceable and retrievable domain context.
```

---

## 5.2 MemorySource

Represents the origin of a memory entry.

Potential attributes:

```text
id
workspace_id
memory_id
source_object_type
source_object_id
source_actor_id
source_agent_id
source_created_at
created_at
```

Domain responsibility:

```text
MemorySource preserves where memory came from and why it can be trusted.
```

MVP simplification:

```text
Memory source may initially be represented by source_object_type and source_object_id on MemoryEntry.
```

---

## 5.3 MemoryLink

Represents a relationship between memory and another domain object.

Potential attributes:

```text
id
workspace_id
memory_id
linked_object_type
linked_object_id
link_type
created_at
created_by
```

Domain responsibility:

```text
MemoryLink connects knowledge to the business objects where it is useful.
```

---

## 5.4 MemoryReview

Represents validation or review of memory accuracy.

Potential attributes:

```text
id
workspace_id
memory_id
reviewed_by
reviewed_at
review_result
notes
next_review_date
```

Domain responsibility:

```text
MemoryReview keeps enterprise memory reliable over time.
```

---

## 5.5 MemoryUsage

Represents a record that memory was used in context, especially for AI support.

Potential attributes:

```text
id
workspace_id
memory_id
used_by_object_type
used_by_object_id
used_by_agent_id
purpose
used_at
```

Domain responsibility:

```text
MemoryUsage supports traceability of how memory influenced AI assistance or runtime output.
```

MVP simplification:

```text
Memory usage may initially be tracked through AuditEvent.
```

---

# 6. Memory Types

Initial memory types:

```text
company_context
owner_goal
operating_pain_point
workspace_profile
operating_map_summary
operating_gap
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
integration_context
```

MVP priority memory types:

```text
company_context
operating_gap
function_context
process_definition
task_outcome
decision_context
decision_rationale
agent_recommendation
```

---

# 7. Memory Lifecycle

Recommended lifecycle:

```text
candidate
↓
draft
↓
confirmed
↓
active
↓
reviewed
↓
updated
↓
archived
```

MVP lifecycle:

```text
candidate
active
archived
```

Optional MVP status:

```text
confirmed
```

---

# 8. Memory Confidence

Suggested confidence values:

```text
low
medium
high
verified
```

MVP simplification:

```text
manual
ai_suggested
confirmed
```

Confidence must not replace source traceability.

---

# 9. Domain Relationships

## 9.1 Workspace to MemoryEntry

```text
CompanyWorkspace 1 → many MemoryEntries
```

## 9.2 MemoryEntry to Source Object

```text
MemoryEntry → source_object_type + source_object_id
```

## 9.3 Function to MemoryEntry

```text
Function 1 → many MemoryEntries
```

## 9.4 Process to MemoryEntry

```text
Process 1 → many MemoryEntries
```

## 9.5 Task to MemoryEntry

```text
Task may create or reference MemoryEntries
```

## 9.6 Decision to MemoryEntry

```text
Decision may create decision_context, rationale or outcome memory
```

## 9.7 Agent to MemoryEntry

```text
Agent may suggest MemoryEntries but cannot make untraceable active memory
```

---

# 10. Domain Invariants

The Memory Domain must enforce:

```text
MemoryEntry must belong to one workspace.
MemoryEntry content is required.
MemoryEntry type is required.
Active memory should have source traceability or explicit manual origin.
AI-generated memory must identify source agent or operation.
Archived memory cannot be used as active AI context.
Memory retrieval must respect workspace boundaries.
Memory used for AI context should be auditable.
Sensitive memory should support review or archival.
```

---

# 11. AI Memory Rules

AI may:

- suggest memory candidates;
- summarize source objects into memory;
- classify memory type;
- recommend memory links;
- retrieve scoped memory for context;
- suggest review or archival.

AI may not:

- create untraceable active memory;
- use memory outside workspace scope;
- access secrets;
- silently overwrite confirmed memory;
- treat archived memory as active context;
- bypass audit when memory influences sensitive output.

MVP rule:

```text
AI may suggest memory. Bizzi must preserve source traceability.
```

---

# 12. Memory Creation Flow

```text
Meaningful runtime activity occurs
↓
Memory opportunity detected
↓
Memory candidate created
↓
Source object linked
↓
Memory type assigned
↓
User or governed rule confirms if required
↓
Memory becomes active
↓
Audit event recorded
↓
Dashboard updated
↓
AI context retrieval may use it
```

---

# 13. Memory Retrieval Flow

```text
Runtime service or AI agent requests context
↓
Workspace scope checked
↓
Relevant active memory selected
↓
Source and confidence considered
↓
Sensitive or archived memory excluded
↓
Memory usage recorded if required
↓
Scoped context returned
```

---

# 14. Domain Events

Memory events:

```text
memory.candidate_created
memory.created
memory.confirmed
memory.activated
memory.updated
memory.reviewed
memory.linked_to_source
memory.used_in_context
memory.archived
memory.rejected
```

---

# 15. Audit Requirements

Audited actions:

```text
memory.candidate_created
memory.created
memory.confirmed
memory.updated
memory.reviewed
memory.used_in_ai_context
memory.archived
memory.rejected
memory.source_changed
```

Audit must answer:

```text
What memory was created or used, where did it come from, who confirmed it, and how was it applied?
```

---

# 16. Memory Dashboard Requirements

Dashboard should show:

- total memory entries;
- recent memory;
- memory by type;
- memory created from decisions;
- memory created from processes;
- memory created from tasks;
- memory candidates needing review;
- archived memory count;
- knowledge coverage gaps.

Dashboard question:

```text
What does the company know, what has been preserved, and what knowledge still needs confirmation?
```

---

# 17. Security Requirements

Security requirements:

```text
Memory belongs to one workspace.
Memory retrieval must respect workspace access.
AI context may only use scoped memory.
Archived memory should not be used as active AI context.
Memory source must not be hidden.
Memory audit must be workspace-scoped.
Sensitive memory should not expose secrets to AI context.
```

---

# 18. MVP Domain Behavior

MVP should support:

```text
Create memory entry
Create memory candidate from onboarding context
Create memory from confirmed decision
Create memory from confirmed process
Create memory from important task outcome
Link memory to source object
Retrieve memory by workspace context
Retrieve memory for AI context
Archive memory
Create audit events
Show memory coverage on dashboard
```

---

# 19. Out of Scope for MVP

The Memory Domain does not need in MVP:

- advanced vector database architecture;
- complex semantic search;
- automated forgetting policies;
- cross-workspace memory sharing;
- model fine-tuning;
- external knowledge graph;
- legal retention engine;
- autonomous long-term learning.

---

# 20. Data Model Implications

Future Data Model should include tables or collections for:

```text
memory_entries
```

Potential later tables:

```text
memory_sources
memory_links
memory_reviews
memory_usage
memory_tags
```

Recommended indexes later:

```text
memory_entries.workspace_id
memory_entries.memory_type
memory_entries.status
memory_entries.source_object_type
memory_entries.source_object_id
memory_entries.function_id
memory_entries.process_id
memory_entries.task_id
memory_entries.decision_id
memory_entries.agent_id
memory_entries.created_at
```

---

# 21. API Implications

Future API contracts should support:

```text
POST /workspaces/{workspace_id}/memory
GET /workspaces/{workspace_id}/memory
GET /workspaces/{workspace_id}/memory/{memory_id}
PATCH /workspaces/{workspace_id}/memory/{memory_id}
POST /workspaces/{workspace_id}/memory/{memory_id}/confirm
POST /workspaces/{workspace_id}/memory/{memory_id}/archive
GET /workspaces/{workspace_id}/memory/context
POST /workspaces/{workspace_id}/memory/search
```

---

# 22. Traceability Pattern

Memory traceability chain:

```text
Source Object / User Input / Agent Output
↓
MemoryEntry
↓
MemorySource / MemoryLink
↓
MemoryUsage
↓
Runtime Event
↓
Audit Event
↓
Dashboard Metric
```

---

# 23. Acceptance Criteria

Memory Domain is ready when:

- MemoryEntry is defined as aggregate root;
- memory lifecycle is clear;
- source traceability rules are explicit;
- AI memory rules are defined;
- retrieval boundaries are defined;
- audit behavior is defined;
- dashboard role is defined;
- data model and API implications are identified.

Status:

```text
Ready for Data Model and API Design
```

---

# 24. Architecture Alignment

| Memory Domain Area | Reference |
|---|---|
| MemoryEntry | 08_MEMORY_RUNTIME.md |
| Memory Source | Traceability Matrix / Runtime Architecture |
| Memory Confirmation | Governance Baseline |
| Decision Memory | Decision Domain |
| Process Memory | Process Domain |
| Task Memory | Task Domain |
| Agent Memory | Agent Domain |
| Memory Audit | Audit Runtime |
| Memory Events | Event Runtime |
| Memory Security | Runtime Security |
| Memory Dashboard | Core User Journey |

---

# 25. Final Memory Domain Statement

```text
Memory Domain defines how Bizzi represents reusable enterprise knowledge as structured, workspace-scoped, source-linked and auditable memory that can guide decisions, agents, processes, tasks and future execution.
```

This domain ensures Bizzi can remember how the company works, why decisions were made and what knowledge should guide future action.