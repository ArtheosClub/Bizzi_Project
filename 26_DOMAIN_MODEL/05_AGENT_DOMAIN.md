# 05_AGENT_DOMAIN.md

# Bizzi Platform

## Agent Domain

**Layer:** 26_DOMAIN_MODEL  
**Component Type:** Domain Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 04_AGENT_RUNTIME.md  
**Previous Documents:** 00_DOMAIN_MODEL_VISION.md, 01_ENTITY_CATALOG.md, 02_WORKSPACE_DOMAIN.md, 03_OPERATING_MAP_DOMAIN.md, 04_FUNCTION_AND_RESPONSIBILITY_DOMAIN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Agent Domain for Bizzi Platform.

The Agent Domain describes how Bizzi represents AI agents as governed domain objects inside a company workspace, including their roles, authority, ownership, lifecycle, recommendations, outputs, audit requirements and memory relationships.

Core question:

```text
How does Bizzi make AI agents part of the company operating model without losing human accountability, security, traceability and control?
```

---

# 2. Domain Role

The Agent Domain connects AI assistance to the structured enterprise operating model.

It provides:

- AI agent identity;
- human ownership;
- authority boundaries;
- functional assignment;
- recommendation capture;
- draft output governance;
- escalation rules;
- audit evidence;
- memory linkage;
- dashboard visibility.

---

# 3. Domain Principle

```text
AI Agents Are Governed Operating Roles
```

An agent is not a free-floating chatbot.

An agent inside Bizzi must be:

- workspace-scoped;
- assigned to a purpose;
- linked to a human owner;
- constrained by authority;
- auditable;
- safe for memory and context use;
- visible on the dashboard.

---

# 4. Aggregate Boundary

Primary aggregate root:

```text
Agent
```

Supporting entities:

```text
AgentAuthorityScope
AgentRole
AgentRecommendation
AgentActionDraft
AgentEscalationRule
AgentStatus
AgentContextScope
```

Related external entities:

```text
CompanyWorkspace
User
Function
Responsibility
Process
Task
Decision
MemoryEntry
AuditEvent
RuntimeEvent
OperatingRecommendation
DashboardMetric
SecurityPolicy
```

---

# 5. Core Entities

## 5.1 Agent

Represents a governed AI agent role inside a workspace.

Minimum domain attributes:

```text
id
workspace_id
name
role
status
human_owner_id
authority_scope_id
created_at
updated_at
created_by
```

Optional domain attributes:

```text
description
function_id
process_id
model_profile
memory_access_scope
confidence_policy
source_object_type
source_object_id
activated_at
paused_at
archived_at
```

Domain responsibility:

```text
Agent defines a governed AI support role that can assist the workspace within explicit authority and ownership boundaries.
```

---

## 5.2 AgentAuthorityScope

Defines what an agent may and may not do.

Minimum domain attributes:

```text
id
workspace_id
agent_id
allowed_actions
restricted_actions
confirmation_required_actions
status
created_at
updated_at
```

Optional domain attributes:

```text
max_autonomy_level
memory_access_level
external_tool_access
integration_access_scope
configured_by
configured_at
```

Domain responsibility:

```text
AgentAuthorityScope protects Bizzi from uncontrolled AI execution by defining explicit operating limits.
```

---

## 5.3 AgentRecommendation

Represents a recommendation produced by an agent.

Minimum domain attributes:

```text
id
workspace_id
agent_id
title
description
recommendation_type
status
created_at
updated_at
```

Optional domain attributes:

```text
source_object_type
source_object_id
suggested_object_type
suggested_object_payload
confidence
reviewed_by
reviewed_at
confirmed_at
rejected_at
```

Domain responsibility:

```text
AgentRecommendation converts AI reasoning into reviewable, traceable and actionable domain output.
```

---

## 5.4 AgentActionDraft

Represents a draft object or action prepared by an agent but not yet confirmed.

Minimum domain attributes:

```text
id
workspace_id
agent_id
draft_type
title
payload
status
created_at
updated_at
```

Optional domain attributes:

```text
source_object_type
source_object_id
reviewed_by
confirmed_by
confirmed_at
rejected_at
result_object_type
result_object_id
```

Domain responsibility:

```text
AgentActionDraft ensures that AI-generated operational outputs can be reviewed before becoming official runtime objects.
```

---

## 5.5 AgentEscalationRule

Defines when agent output must be escalated to a human.

Potential attributes:

```text
id
workspace_id
agent_id
condition
severity
escalate_to_user_id
status
created_at
updated_at
```

Domain responsibility:

```text
AgentEscalationRule defines how agents raise matters that exceed their authority or confidence.
```

MVP simplification:

```text
Escalation may be represented through dashboard warnings and task creation instead of a separate rules engine.
```

---

# 6. Agent Roles

Initial agent roles:

```text
Executive Summary Agent
Operations Coordinator Agent
Process Analyst Agent
Task Routing Agent
Decision Summary Agent
Memory Capture Agent
Risk Monitor Agent
```

Future roles:

```text
Finance Agent
Legal Support Agent
Sales Support Agent
Procurement Agent
HR Agent
Compliance Agent
Grant Discovery Agent
Integration Agent
```

MVP should begin with support agents, not autonomous managers.

---

# 7. Agent Authority Levels

MVP authority levels:

```text
summarize
classify
draft
recommend
prepare
escalate
```

Explicitly out of scope for MVP:

```text
execute_irreversible_action
send_external_message_without_approval
approve_financial_operation
change_legal_commitment
modify_permissions
delete_workspace_data
```

---

# 8. Agent Lifecycle

Recommended lifecycle:

```text
suggested
↓
draft
↓
configured
↓
active
↓
paused
↓
archived
```

MVP lifecycle:

```text
suggested
active
paused
archived
```

---

# 9. Recommendation Lifecycle

Recommended lifecycle:

```text
created
↓
reviewed
↓
confirmed
↓
applied
↓
rejected
```

MVP lifecycle:

```text
created
confirmed
rejected
```

---

# 10. Domain Relationships

## 10.1 Workspace to Agent

```text
CompanyWorkspace 1 → many Agents
```

## 10.2 Agent to Human Owner

```text
Agent many → 1 User
```

Every active agent must have a human owner.

## 10.3 Agent to Function

```text
Function 1 → many Agents
```

An agent may support one or more operating areas in future, but MVP should prefer one primary function.

## 10.4 Agent to Process, Task and Decision

```text
Agent → many Recommendations
Agent → many ActionDrafts
Agent → many Tasks
Agent → many Decisions
Agent → many MemoryEntries
```

## 10.5 Agent to Audit and Events

```text
Agent output → RuntimeEvent → AuditEvent
```

---

# 11. Domain Invariants

The Agent Domain must enforce:

```text
Agent must belong to one workspace.
Active Agent must have a human_owner_id.
Active Agent must have an authority scope.
Agent cannot modify its own authority.
Agent cannot assign or remove its human owner.
Agent output must identify source agent.
AI-generated sensitive outputs must remain draft until confirmed.
Agent memory access must be workspace-scoped.
Archived agents cannot create new recommendations.
Paused agents cannot create new outputs.
```

---

# 12. AI Output Rules

Agent outputs may include:

- summaries;
- classifications;
- recommendations;
- task drafts;
- decision drafts;
- memory candidates;
- process suggestions;
- risk warnings;
- dashboard explanations.

Output rules:

```text
Every output must be linked to agent_id.
Every output must be scoped to workspace_id.
Every sensitive output must require human confirmation.
Every confirmed output should generate audit evidence.
Useful confirmed outputs may create memory entries.
```

---

# 13. Agent Creation Flow

```text
Operating map or gap identifies need
↓
Agent suggestion created
↓
User reviews suggested agent
↓
Human owner assigned
↓
Authority scope defined
↓
Agent activated
↓
Audit event recorded
↓
Dashboard updated
```

---

# 14. Agent Recommendation Flow

```text
User request or runtime trigger
↓
Agent receives scoped context
↓
Agent creates recommendation or draft
↓
Recommendation stored as reviewable object
↓
User confirms or rejects
↓
Runtime object created or updated if confirmed
↓
Audit event recorded
↓
Memory created if applicable
↓
Dashboard updated
```

---

# 15. Domain Events

Agent events:

```text
agent.suggested
agent.created
agent.configured
agent.activated
agent.paused
agent.archived
agent.owner_assigned
agent.authority_defined
```

Output events:

```text
agent.recommendation_created
agent.action_draft_created
agent.output_confirmed
agent.output_rejected
agent.escalated
```

---

# 16. Audit Requirements

Audited actions:

```text
agent.created
agent.configured
agent.activated
agent.paused
agent.archived
agent.owner_assigned
agent.authority_defined
agent.recommendation_created
agent.output_confirmed
agent.output_rejected
agent.escalated
```

Audit must answer:

```text
Which agent produced what, under which authority, who reviewed it, and what was accepted or rejected?
```

---

# 17. Memory Requirements

Memory may be created from:

- confirmed recommendations;
- decision summaries;
- process summaries;
- task outcomes;
- escalations;
- agent lessons learned;
- recurring patterns.

Memory types:

```text
agent_recommendation
agent_decision_summary
agent_process_summary
agent_task_context
agent_escalation
agent_lesson
```

Memory must include:

```text
source_agent_id
source_object_type
source_object_id
confirmation_status
```

---

# 18. Dashboard Requirements

Dashboard should show:

- active agents;
- suggested agents;
- paused agents;
- agents without owners;
- agents by function;
- pending recommendations;
- pending action drafts;
- escalations;
- AI-assisted decisions;
- agent coverage gaps.

Dashboard question:

```text
Which AI agents are supporting the company, what are they doing, and who is accountable for them?
```

---

# 19. Security Requirements

Security requirements:

```text
Agent belongs to one workspace.
Agent context must be workspace-scoped.
Agent authority must be explicit.
Agent cannot access secrets.
Agent cannot change permissions.
Agent cannot execute irreversible actions in MVP.
Agent memory access must respect scope.
Agent outputs affecting runtime objects must be audited.
```

---

# 20. MVP Domain Behavior

MVP should support:

```text
Suggest agent from operating map or gap
Create agent
Assign human owner
Define authority scope
Activate agent
Pause agent
Archive agent
Create recommendation
Create action draft
Confirm or reject agent output
Record audit events
Create memory from confirmed outputs
Show agent status on dashboard
```

---

# 21. Out of Scope for MVP

The Agent Domain does not need in MVP:

- fully autonomous agents;
- agent-to-agent negotiation;
- complex multi-agent planning;
- long-running autonomous background execution;
- self-modifying agents;
- marketplace of agents;
- external tool execution without approval;
- advanced model routing;
- model fine-tuning.

---

# 22. Data Model Implications

Future Data Model should include tables or collections for:

```text
agents
agent_authority_scopes
agent_recommendations
agent_action_drafts
```

Potential later tables:

```text
agent_roles
agent_escalation_rules
agent_context_scopes
```

Recommended indexes later:

```text
agents.workspace_id
agents.status
agents.human_owner_id
agents.function_id
agent_recommendations.workspace_id
agent_recommendations.agent_id
agent_recommendations.status
agent_action_drafts.workspace_id
agent_action_drafts.agent_id
agent_action_drafts.status
```

---

# 23. API Implications

Future API contracts should support:

```text
POST /workspaces/{workspace_id}/agents
GET /workspaces/{workspace_id}/agents
GET /workspaces/{workspace_id}/agents/{agent_id}
PATCH /workspaces/{workspace_id}/agents/{agent_id}
POST /workspaces/{workspace_id}/agents/{agent_id}/activate
POST /workspaces/{workspace_id}/agents/{agent_id}/pause
POST /workspaces/{workspace_id}/agents/{agent_id}/archive
POST /workspaces/{workspace_id}/agents/{agent_id}/recommendations
POST /workspaces/{workspace_id}/agent-recommendations/{recommendation_id}/confirm
POST /workspaces/{workspace_id}/agent-recommendations/{recommendation_id}/reject
```

---

# 24. Traceability Pattern

Agent traceability chain:

```text
OperatingMap / OperatingGap / User Request
↓
Agent
↓
AgentAuthorityScope
↓
AgentRecommendation / AgentActionDraft
↓
Confirmed Runtime Object
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

# 25. Acceptance Criteria

Agent Domain is ready when:

- Agent is defined as aggregate root;
- AgentAuthorityScope is defined;
- AgentRecommendation is defined;
- AgentActionDraft is defined;
- lifecycle states are clear;
- human owner rule is explicit;
- AI output rules are defined;
- audit and memory behavior are defined;
- dashboard role is defined;
- data model and API implications are identified.

Status:

```text
Ready for Data Model and API Design
```

---

# 26. Architecture Alignment

| Agent Domain Area | Reference |
|---|---|
| Agent | 04_AGENT_RUNTIME.md |
| Human Owner | Governance Baseline / Runtime Security |
| Authority Scope | Runtime Security / Autonomy Governance |
| Recommendations | Operating Map Domain / Agent Runtime |
| Action Drafts | Task Runtime / Decision Runtime / Memory Runtime |
| Audit | Audit Runtime |
| Memory | Memory Runtime |
| Events | Event Runtime |
| Dashboard | Core User Journey |
| Security | Runtime Security |

---

# 27. Final Agent Domain Statement

```text
Agent Domain defines how Bizzi represents AI agents as governed, workspace-scoped, human-owned and authority-limited operating roles that can recommend, draft, summarize, escalate, create memory and support execution without bypassing accountability.
```

This domain ensures Bizzi can use AI operationally while preserving trust, control and enterprise governance.