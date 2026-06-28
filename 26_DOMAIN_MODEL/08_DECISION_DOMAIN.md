# 08_DECISION_DOMAIN.md

# Bizzi Platform

## Decision Domain

**Layer:** 26_DOMAIN_MODEL  
**Component Type:** Domain Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 07_DECISION_RUNTIME.md  
**Previous Documents:** 00_DOMAIN_MODEL_VISION.md, 01_ENTITY_CATALOG.md, 02_WORKSPACE_DOMAIN.md, 03_OPERATING_MAP_DOMAIN.md, 04_FUNCTION_AND_RESPONSIBILITY_DOMAIN.md, 05_AGENT_DOMAIN.md, 06_PROCESS_DOMAIN.md, 07_TASK_DOMAIN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Decision Domain for Bizzi Platform.

The Decision Domain describes how Bizzi represents important business choices as structured, owned, traceable and reusable operating knowledge inside a company workspace.

Core question:

```text
How does Bizzi preserve business decisions, their context, rationale, consequences and follow-up actions so they can guide future execution?
```

---

# 2. Domain Role

The Decision Domain connects business judgment to execution and memory.

It provides:

- decision capture;
- decision ownership;
- context and rationale;
- options considered;
- follow-up tasks;
- links to functions, processes, agents and memory;
- audit evidence;
- dashboard visibility;
- future decision review and learning.

---

# 3. Domain Principle

```text
Decisions Must Be Remembered
```

Important business decisions should not disappear into chat history, informal discussion or undocumented assumptions.

A decision should answer:

```text
What was decided?
Why was it decided?
Who confirmed it?
What alternatives were considered?
What should happen next?
What was the outcome?
```

---

# 4. Aggregate Boundary

Primary aggregate root:

```text
Decision
```

Supporting entities:

```text
DecisionContext
DecisionOption
DecisionRationale
DecisionOutcome
DecisionReview
DecisionLink
DecisionStatus
```

Related external entities:

```text
CompanyWorkspace
User
Function
Responsibility
Process
Task
Agent
AgentRecommendation
MemoryEntry
AuditEvent
RuntimeEvent
DashboardMetric
```

---

# 5. Core Entities

## 5.1 Decision

Represents an important business decision.

Minimum domain attributes:

```text
id
workspace_id
title
context
final_decision
rationale
owner_user_id
status
created_at
updated_at
created_by
```

Optional domain attributes:

```text
function_id
process_id
task_id
agent_id
source_object_type
source_object_id
decision_date
review_date
expected_impact
risk_level
outcome_summary
confirmed_by
confirmed_at
archived_at
```

Domain responsibility:

```text
Decision preserves important business judgment as structured, accountable and reusable knowledge.
```

---

## 5.2 DecisionOption

Represents an alternative considered before a decision was confirmed.

Potential attributes:

```text
id
workspace_id
decision_id
title
description
pros
cons
risk_notes
created_at
updated_at
```

Domain responsibility:

```text
DecisionOption preserves alternatives considered during decision-making.
```

MVP simplification:

```text
Options may initially be stored as structured text inside Decision.
```

---

## 5.3 DecisionRationale

Represents the reasoning behind the final decision.

Potential attributes:

```text
id
workspace_id
decision_id
summary
reasoning_factors
tradeoffs
created_by
created_at
```

Domain responsibility:

```text
DecisionRationale explains why the final decision was selected.
```

MVP simplification:

```text
Rationale may initially be a required field on Decision.
```

---

## 5.4 DecisionOutcome

Represents what happened after a decision was implemented.

Potential attributes:

```text
id
workspace_id
decision_id
summary
result_status
measured_impact
lessons_learned
reviewed_by
reviewed_at
```

Domain responsibility:

```text
DecisionOutcome enables learning from decisions after execution.
```

---

## 5.5 DecisionReview

Represents a formal review of a decision.

Potential attributes:

```text
id
workspace_id
decision_id
reviewed_by
reviewed_at
review_result
notes
recommended_followup
```

Domain responsibility:

```text
DecisionReview supports controlled learning, follow-up and correction.
```

---

# 6. Decision Types

Initial decision types:

```text
operational_decision
management_decision
process_decision
responsibility_decision
customer_decision
financial_decision
risk_decision
agent_recommendation_decision
integration_decision
```

MVP may begin with:

```text
operational_decision
management_decision
process_decision
risk_decision
agent_recommendation_decision
```

---

# 7. Decision Lifecycle

Recommended lifecycle:

```text
draft
↓
proposed
↓
confirmed
↓
implemented
↓
reviewed
↓
archived
```

MVP lifecycle:

```text
draft
confirmed
archived
```

Optional MVP status:

```text
implemented
```

---

# 8. Domain Relationships

## 8.1 Workspace to Decision

```text
CompanyWorkspace 1 → many Decisions
```

## 8.2 Decision to Owner

```text
Decision many → 1 User
```

MVP rule:

```text
Confirmed Decision must have owner_user_id.
```

## 8.3 Function to Decision

```text
Function 1 → many Decisions
```

## 8.4 Process to Decision

```text
Process 1 → many Decisions
```

## 8.5 Task to Decision

```text
Task may originate from or produce a Decision
```

## 8.6 Agent to Decision

```text
Agent may draft, summarize or recommend Decisions
```

## 8.7 Decision to Tasks

```text
Decision 1 → many follow-up Tasks
```

---

# 9. Domain Invariants

The Decision Domain must enforce:

```text
Decision must belong to one workspace.
Decision title is required.
Confirmed Decision must have final_decision.
Confirmed Decision must have owner_user_id.
Confirmed Decision should have rationale.
AI-generated decision drafts must remain draft until confirmed.
Archived decisions cannot receive normal updates.
Decision confirmation must be auditable.
Confirmed decisions may create memory entries.
Decision follow-up tasks should link back to the source decision.
```

---

# 10. AI Assistance Rules

AI may assist by:

- summarizing decision context;
- drafting options;
- identifying tradeoffs;
- drafting rationale;
- suggesting follow-up tasks;
- creating decision memory candidates;
- preparing review summaries.

AI may not automatically:

- confirm official decisions;
- make legal or financial commitments;
- assign final accountability;
- hide alternatives;
- mark decisions implemented;
- bypass audit.

MVP rule:

```text
AI may support decision-making. Human confirms official decisions.
```

---

# 11. Decision Capture Flow

```text
Decision need identified
↓
Decision draft created
↓
Context captured
↓
Options captured if available
↓
Rationale drafted or entered
↓
Human owner confirms final decision
↓
Decision linked to function, process, task or agent
↓
Follow-up tasks created if needed
↓
Audit event recorded
↓
Memory entry created
↓
Dashboard updated
```

---

# 12. Decision Review Flow

```text
Decision selected for review
↓
Outcome and impact checked
↓
Lessons learned captured
↓
Follow-up tasks or process changes created
↓
Decision outcome recorded
↓
Memory updated
↓
Audit event recorded
↓
Dashboard refreshed
```

---

# 13. Domain Events

Decision events:

```text
decision.created
decision.updated
decision.context_added
decision.options_added
decision.rationale_added
decision.confirmed
decision.implemented
decision.reviewed
decision.archived
```

Link and follow-up events:

```text
decision.linked_to_function
decision.linked_to_process
decision.linked_to_task
decision.linked_to_agent
decision.followup_task_created
decision.memory_created
```

---

# 14. Audit Requirements

Audited actions:

```text
decision.created
decision.updated
decision.confirmed
decision.implemented
decision.reviewed
decision.archived
decision.followup_task_created
decision.linked_to_object
```

Audit must answer:

```text
Who made or confirmed the decision, what was decided, why, when, and what business object does it affect?
```

---

# 15. Memory Requirements

Memory may be created from:

- confirmed decisions;
- decision rationale;
- options considered;
- implementation outcomes;
- decision reviews;
- lessons learned.

Memory types:

```text
decision_context
decision_rationale
decision_outcome
decision_lesson
decision_review
```

---

# 16. Dashboard Requirements

Dashboard should show:

- recent decisions;
- decisions by function;
- decisions by owner;
- decisions linked to tasks;
- decisions requiring follow-up;
- unreviewed decisions;
- AI-assisted decisions;
- decision outcomes and lessons.

Dashboard question:

```text
What important decisions were made, why, and what should happen next?
```

---

# 17. Security Requirements

Security requirements:

```text
Decision belongs to one workspace.
Only authorized workspace users may create or edit decisions.
AI-generated decision drafts require human confirmation.
Archived decisions cannot be edited through normal flows.
Decision memory must be workspace-scoped.
Decision audit must be workspace-scoped.
Sensitive decisions may require stricter confirmation later.
```

---

# 18. MVP Domain Behavior

MVP should support:

```text
Create decision
Capture context
Capture final decision
Capture rationale
Confirm decision
Link decision to function
Link decision to process
Link decision to task
Generate follow-up task
Archive decision
Create audit events
Create memory from confirmed decision
Show decision status on dashboard
```

---

# 19. Out of Scope for MVP

The Decision Domain does not need in MVP:

- complex approval workflows;
- board voting;
- legal signing;
- financial authorization engine;
- autonomous decision execution;
- advanced decision analytics;
- simulation of decision outcomes;
- external governance integrations.

---

# 20. Data Model Implications

Future Data Model should include tables or collections for:

```text
decisions
```

Potential later tables:

```text
decision_options
decision_outcomes
decision_reviews
decision_links
```

Recommended indexes later:

```text
decisions.workspace_id
decisions.owner_user_id
decisions.status
decisions.function_id
decisions.process_id
decisions.task_id
decisions.agent_id
decisions.decision_date
decisions.source_object_type
decisions.source_object_id
```

---

# 21. API Implications

Future API contracts should support:

```text
POST /workspaces/{workspace_id}/decisions
GET /workspaces/{workspace_id}/decisions
GET /workspaces/{workspace_id}/decisions/{decision_id}
PATCH /workspaces/{workspace_id}/decisions/{decision_id}
POST /workspaces/{workspace_id}/decisions/{decision_id}/confirm
POST /workspaces/{workspace_id}/decisions/{decision_id}/archive
POST /workspaces/{workspace_id}/decisions/{decision_id}/follow-up-task
POST /workspaces/{workspace_id}/decisions/{decision_id}/review
```

---

# 22. Traceability Pattern

Decision traceability chain:

```text
User Input / Agent Recommendation / Process Need / Task Context
↓
Decision
↓
Decision Rationale / Options / Outcome
↓
Follow-up Task
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

# 23. Acceptance Criteria

Decision Domain is ready when:

- Decision is defined as aggregate root;
- decision lifecycle is clear;
- decision ownership rules are explicit;
- rationale and context requirements are defined;
- AI decision support rules are defined;
- follow-up task behavior is defined;
- audit and memory behavior are defined;
- dashboard role is defined;
- data model and API implications are identified.

Status:

```text
Ready for Data Model and API Design
```

---

# 24. Architecture Alignment

| Decision Domain Area | Reference |
|---|---|
| Decision | 07_DECISION_RUNTIME.md |
| Decision Owner | Function and Responsibility Domain |
| Decision Context | Memory Runtime |
| Follow-up Tasks | Task Domain |
| Agent Support | Agent Domain |
| Decision Events | Event Runtime |
| Decision Audit | Audit Runtime |
| Decision Memory | Memory Runtime |
| Decision Dashboard | Core User Journey |
| Decision Security | Runtime Security |

---

# 25. Final Decision Domain Statement

```text
Decision Domain defines how Bizzi represents important business choices as owned, contextual, rationale-backed, traceable and reusable operating knowledge connected to tasks, processes, agents, memory, audit and dashboard visibility.
```

This domain ensures Bizzi can preserve not only what the company does, but why it decided to act.