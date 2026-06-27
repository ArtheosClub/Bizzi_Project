# 07_DECISION_RUNTIME.md

# Bizzi Platform

## Decision Runtime

**Layer:** 25_RUNTIME_PLATFORM  
**Component Type:** Runtime Component Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 00_RUNTIME_VISION.md, 01_RUNTIME_ARCHITECTURE.md, 02_CORE_RUNTIME_COMPONENTS.md, 03_WORKSPACE_RUNTIME.md, 04_AGENT_RUNTIME.md, 05_PROCESS_RUNTIME.md, 06_TASK_RUNTIME.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Decision Runtime for Bizzi Platform.

Decision Runtime is responsible for recording, structuring, linking and preserving important business decisions inside a company workspace.

Core question:

```text
How does Bizzi ensure that business decisions do not disappear into chats, memory or informal conversations, but become structured, traceable and reusable operating knowledge?
```

---

# 2. Runtime Role

Decision Runtime connects business judgment to operating memory and execution.

It links decisions to:

- workspace;
- functions;
- responsibilities;
- human owners;
- AI agents;
- processes;
- tasks;
- memory;
- audit trail;
- dashboard visibility.

---

# 3. Decision Runtime Principle

```text
Decisions Must Be Remembered
```

Every important decision should have:

- owner;
- context;
- rationale;
- outcome;
- linked business object;
- audit trail;
- memory entry.

---

# 4. Primary Runtime Objects

Minimum objects:

```text
Decision
DecisionOwner
DecisionContext
DecisionOption
DecisionRationale
DecisionOutcome
DecisionLink
DecisionHistory
```

Supporting objects:

```text
CompanyWorkspace
Function
Responsibility
Agent
Process
Task
MemoryEntry
AuditEvent
RuntimeEvent
```

---

# 5. Decision Object

## Purpose

Represents an important business decision made inside the workspace.

## Minimum Fields

```text
id
workspace_id
title
context
owner_id
final_decision
rationale
status
created_at
updated_at
```

## Optional Fields

```text
function_id
process_id
task_id
agent_id
options_considered
expected_impact
risk_level
decision_date
review_date
outcome_summary
```

---

# 6. Decision Lifecycle

```text
Draft
↓
Proposed
↓
Confirmed
↓
Implemented
↓
Reviewed
↓
Archived
```

## Draft

Decision is being captured or prepared.

## Proposed

Decision is suggested by a human or AI agent but not yet confirmed.

## Confirmed

Decision is accepted as official.

## Implemented

Decision has produced actions or tasks.

## Reviewed

Decision is evaluated after implementation.

## Archived

Decision is retained historically but no longer active.

---

# 7. Decision States

```text
draft
proposed
confirmed
implemented
reviewed
archived
```

MVP required states:

```text
draft
confirmed
archived
```

---

# 8. Decision Types for MVP

Initial decision types:

```text
Operational Decision
Management Decision
Process Decision
Responsibility Decision
Customer Decision
Financial Decision
Risk Decision
Agent Recommendation Decision
```

The MVP should avoid excessive decision taxonomy.

---

# 9. Core Operations

## 9.1 Create Decision

Creates a decision record inside the workspace.

## 9.2 Capture Context

Stores the situation or problem that led to the decision.

## 9.3 Capture Options

Stores alternatives considered before the decision.

## 9.4 Capture Rationale

Stores why the selected decision was chosen.

## 9.5 Confirm Decision

Marks the decision as accepted by the human owner.

## 9.6 Link Decision

Links the decision to function, process, task, agent or responsibility.

## 9.7 Generate Follow-up Tasks

Creates tasks required to implement the decision.

## 9.8 Create Decision Memory

Creates structured memory from the decision.

## 9.9 Review Decision

Captures outcome or lessons learned.

## 9.10 Archive Decision

Retains decision history while removing it from active views.

---

# 10. Decision Capture Flow

```text
Decision need identified
↓
Decision record created
↓
Context captured
↓
Options captured if available
↓
Rationale captured
↓
Human owner confirms decision
↓
Decision linked to business objects
↓
Follow-up tasks created if needed
↓
Audit event recorded
↓
Decision memory created
↓
Dashboard updated
```

---

# 11. AI-Assisted Decision Flow

```text
User requests decision support
↓
AI agent receives scoped context
↓
AI drafts options or summary
↓
User reviews draft
↓
User confirms final decision
↓
Decision Runtime records official decision
↓
Audit records AI assistance and human confirmation
↓
Memory stores confirmed decision context
```

MVP rule:

```text
AI may support decisions but cannot make official decisions autonomously.
```

---

# 12. Decision Events

Minimum events:

```text
decision.created
decision.updated
decision.context_added
decision.options_added
decision.rationale_added
decision.confirmed
decision.linked_to_function
decision.linked_to_process
decision.linked_to_task
decision.linked_to_agent
decision.followup_task_created
decision.memory_created
decision.reviewed
decision.archived
```

Events must include:

```text
event_id
workspace_id
decision_id
actor_id
event_type
timestamp
payload
```

---

# 13. Decision Audit Requirements

Audit events are required for:

- decision creation;
- context changes;
- rationale changes;
- confirmation;
- link changes;
- follow-up task creation;
- review;
- archival;
- AI-assisted decision drafts;
- human confirmation of AI-assisted output.

Audit question:

```text
Who made or confirmed the decision, what was decided, why, when, and what business object does it affect?
```

---

# 14. Decision Memory Integration

Decision Runtime should create memory from:

- confirmed decisions;
- decision rationale;
- options considered;
- implementation outcomes;
- lessons learned;
- decision reviews.

Memory types:

```text
decision_context
decision_rationale
decision_outcome
decision_lesson
decision_review
```

Memory must be linked to workspace and source decision.

---

# 15. Decision Dashboard Integration

Dashboard should show:

- recent decisions;
- decisions by function;
- decisions by owner;
- decisions linked to tasks;
- unreviewed decisions;
- decisions requiring follow-up;
- AI-assisted decisions;
- decision memory created.

Dashboard question:

```text
What important decisions were made, why, and what should happen next?
```

---

# 16. Decision Security Boundary

Decision Runtime must enforce:

```text
Decision belongs to one workspace.
Decision must reference workspace_id.
Only authorized users may create or edit decisions.
AI-generated decision drafts require human confirmation.
Archived decisions cannot be edited normally.
Decision memory must be scoped to workspace.
Decision audit must be scoped to workspace.
```

---

# 17. Decision Context Model

Decision context may include:

- workspace profile;
- linked function;
- linked process;
- linked task;
- linked agent;
- relevant memory entries;
- responsibility owner;
- current operating gaps;
- decision history;
- risk notes.

This context supports better decision summaries, recommendations and future retrieval.

---

# 18. Decision API Boundary

Suggested API group:

```text
/decisions
```

Minimum endpoints:

```text
POST /workspaces/{workspace_id}/decisions
GET /workspaces/{workspace_id}/decisions
GET /workspaces/{workspace_id}/decisions/{decision_id}
PATCH /workspaces/{workspace_id}/decisions/{decision_id}
POST /workspaces/{workspace_id}/decisions/{decision_id}/confirm
POST /workspaces/{workspace_id}/decisions/{decision_id}/archive
POST /workspaces/{workspace_id}/decisions/{decision_id}/follow-up-task
```

Future endpoints:

```text
GET /workspaces/{workspace_id}/decisions/{decision_id}/audit
GET /workspaces/{workspace_id}/decisions/{decision_id}/memory
POST /workspaces/{workspace_id}/decisions/{decision_id}/review
POST /workspaces/{workspace_id}/decisions/{decision_id}/link
```

---

# 19. Decision Service Responsibilities

`DecisionRuntimeService` responsibilities:

- create decision records;
- capture context;
- capture options;
- capture rationale;
- confirm decisions;
- link decisions to runtime objects;
- generate follow-up tasks;
- create decision memory;
- emit decision events;
- trigger audit recording;
- expose decision status to dashboard.

---

# 20. Decision Data Validation

Required validation:

- workspace_id is required;
- decision title is required;
- owner is required for confirmed decision;
- final_decision is required for confirmed state;
- rationale is recommended for confirmed state;
- AI-generated decision drafts must remain draft until confirmed;
- archived decisions cannot be edited normally.

---

# 21. MVP Acceptance Criteria

Decision Runtime is MVP-ready when:

- user can create a decision;
- user can capture context and rationale;
- user can confirm final decision;
- decision can be linked to function, process or task;
- decision can generate follow-up tasks;
- decision confirmation creates audit event;
- confirmed decision creates memory entry;
- dashboard shows recent decisions and required follow-up.

---

# 22. Out of Scope for MVP

The MVP does not require:

- complex approval workflows;
- legal signing;
- board-level voting;
- financial authorization engine;
- autonomous decision execution;
- advanced decision analytics;
- decision simulation;
- external governance integrations.

---

# 23. Architecture Alignment

| Decision Runtime Area | Architecture Reference |
|---|---|
| Decision Object | Decision Routing |
| Decision Owner | Governance Baseline |
| Context and Rationale | Enterprise Memory |
| Function Link | Enterprise Function Registry |
| Process Link | Process Architecture |
| Task Link | Operating Model |
| Agent Support | Agent Library / AI Governance |
| Decision Audit | Observability and Intelligence |
| Decision Dashboard | Core User Journey |

---

# 24. Final Decision Runtime Statement

```text
Decision Runtime is the component that turns important business choices into structured, owned, traceable and reusable operating knowledge linked to functions, processes, tasks, agents, memory and audit.
```

This component ensures Bizzi can preserve why the company acts, not only what the company does.