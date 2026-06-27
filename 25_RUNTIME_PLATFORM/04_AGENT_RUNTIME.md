# 04_AGENT_RUNTIME.md

# Bizzi Platform

## Agent Runtime

**Layer:** 25_RUNTIME_PLATFORM  
**Component Type:** Runtime Component Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 00_RUNTIME_VISION.md, 01_RUNTIME_ARCHITECTURE.md, 02_CORE_RUNTIME_COMPONENTS.md, 03_WORKSPACE_RUNTIME.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Agent Runtime for Bizzi Platform.

The Agent Runtime is responsible for registering, configuring, governing and supervising AI agents inside a company workspace.

Core question:

```text
How does Bizzi make AI agents part of the company operating system without losing human accountability, governance, traceability and auditability?
```

---

# 2. Runtime Role

Agent Runtime transforms AI from a generic assistant into a governed operational role inside the company.

It connects agents to:

- workspace;
- functions;
- responsibilities;
- human owners;
- tasks;
- decisions;
- processes;
- memory;
- audit trail;
- dashboard visibility.

---

# 3. Agent Runtime Principle

```text
AI recommends. Human confirms.
```

For the MVP, agents must not perform irreversible autonomous execution.

Agents may:

- suggest;
- draft;
- summarize;
- classify;
- detect gaps;
- prepare tasks;
- prepare decisions;
- prepare memory entries.

Humans confirm important actions before persistence or execution.

---

# 4. Primary Runtime Objects

Minimum objects:

```text
Agent
AgentRole
AgentAuthorityScope
AgentOwner
AgentStatus
AgentEscalationRule
AgentRecommendation
AgentActionDraft
```

Supporting objects:

```text
CompanyWorkspace
Function
Responsibility
Process
Task
Decision
MemoryEntry
AuditEvent
RuntimeEvent
```

---

# 5. Agent Object

## Purpose

Represents an AI agent role registered inside a workspace.

## Minimum Fields

```text
id
workspace_id
name
role
function_id
human_owner_id
status
authority_scope
created_at
updated_at
```

## Optional Fields

```text
description
allowed_actions
restricted_actions
escalation_rule_id
memory_access_scope
model_provider
model_profile
confidence_policy
```

---

# 6. Agent Lifecycle

```text
Suggested
↓
Draft
↓
Configured
↓
Active
↓
Paused
↓
Archived
```

## Suggested

Bizzi recommends an agent based on functions, gaps or onboarding context.

## Draft

The user is reviewing the proposed agent.

## Configured

Role, function, owner and authority are defined.

## Active

Agent is available for governed assistance.

## Paused

Agent is temporarily disabled.

## Archived

Agent is retained historically but no longer active.

---

# 7. Agent States

```text
suggested
draft
configured
active
paused
archived
```

MVP required states:

```text
suggested
active
paused
archived
```

---

# 8. Agent Types for MVP

Initial suggested agent types:

```text
Operations Coordinator Agent
Process Analyst Agent
Task Routing Agent
Decision Summary Agent
Memory Capture Agent
Risk Monitor Agent
Executive Summary Agent
```

These are support agents, not autonomous managers.

---

# 9. Agent Authority Model

Agent authority defines what an agent may do.

MVP authority levels:

```text
Recommend
Draft
Summarize
Classify
Prepare
Escalate
```

Out of scope for MVP:

```text
Execute Irreversible Action
Send External Communication Without Approval
Approve Financial Operation
Change Legal Commitment
Modify Permissions
Delete Workspace Data
```

---

# 10. Human Owner Requirement

Every agent must have a human owner.

The human owner is accountable for:

- agent configuration;
- agent authority boundaries;
- reviewing important recommendations;
- confirming action drafts;
- pausing or archiving the agent;
- resolving escalations.

No active agent may exist without a human owner.

---

# 11. Core Operations

## 11.1 Suggest Agent

Creates an agent recommendation based on operating map, function gaps or onboarding input.

## 11.2 Create Agent

Creates an agent record after user confirmation.

## 11.3 Configure Agent

Defines role, function, owner, authority and escalation rules.

## 11.4 Activate Agent

Makes the configured agent available for assistance.

## 11.5 Pause Agent

Temporarily disables the agent.

## 11.6 Archive Agent

Removes the agent from active use while preserving history.

## 11.7 Generate Recommendation

Agent produces a governed recommendation or draft.

## 11.8 Escalate

Agent raises a matter to the human owner when authority is insufficient.

---

# 12. Agent Suggestion Flow

```text
Business context captured
↓
Operating gaps detected
↓
Function structure confirmed
↓
AI Orchestration Runtime suggests agent
↓
Agent Runtime creates suggestion
↓
User reviews suggestion
↓
Human owner assigned
↓
Authority scope defined
↓
Agent activated
```

---

# 13. Agent Action Flow

```text
User request or runtime trigger
↓
Agent receives scoped context
↓
Agent prepares recommendation or draft
↓
Output validated
↓
Human reviews
↓
Human confirms or rejects
↓
Runtime object updated if confirmed
↓
Audit event recorded
↓
Memory updated if applicable
↓
Dashboard updated
```

---

# 14. Agent Events

Minimum events:

```text
agent.suggested
agent.created
agent.configured
agent.activated
agent.paused
agent.archived
agent.owner_assigned
agent.authority_defined
agent.recommendation_created
agent.action_draft_created
agent.output_confirmed
agent.output_rejected
agent.escalated
```

Events must include:

```text
event_id
workspace_id
agent_id
actor_id
event_type
timestamp
payload
```

---

# 15. Agent Audit Requirements

Audit events are required for:

- agent creation;
- owner assignment;
- authority changes;
- activation;
- pause;
- archive;
- recommendations confirmed by user;
- rejected AI drafts;
- escalations;
- agent-generated memory candidates.

Audit question:

```text
Which agent produced what, under which authority, who reviewed it, and what was accepted or rejected?
```

---

# 16. Agent Memory Integration

Agent Runtime may create or suggest memory from:

- recommendations;
- confirmed action drafts;
- decision summaries;
- process summaries;
- task patterns;
- escalations;
- lessons learned.

Memory types:

```text
agent_recommendation
agent_decision_summary
agent_process_summary
agent_task_context
agent_escalation
```

Memory must include:

```text
source_agent_id
source_object_type
source_object_id
confirmation_status
```

---

# 17. Agent Dashboard Integration

Dashboard should show:

- active agents;
- suggested agents;
- agents without owners;
- agents by function;
- recent recommendations;
- pending confirmations;
- escalations;
- paused agents;
- agent coverage gaps.

Dashboard question:

```text
Which AI agents are supporting the business, where, and under whose accountability?
```

---

# 18. Agent Security Boundary

Agent Runtime must enforce:

```text
Agent context is scoped to workspace_id.
Agent actions are constrained by authority_scope.
Agent outputs remain draft until confirmed where required.
Agent memory access is limited by scope.
Agent cannot change its own authority.
Agent cannot assign or remove its human owner.
Agent cannot bypass audit.
```

---

# 19. Agent Context Model

Agent context may include:

- workspace profile;
- assigned function;
- relevant responsibilities;
- open tasks;
- recent decisions;
- relevant memory entries;
- current operating gaps;
- escalation rules;
- authority scope.

The context must be structured and minimized to the task.

---

# 20. Agent API Boundary

Suggested API group:

```text
/agents
```

Minimum endpoints:

```text
POST /workspaces/{workspace_id}/agents
GET /workspaces/{workspace_id}/agents
GET /workspaces/{workspace_id}/agents/{agent_id}
PATCH /workspaces/{workspace_id}/agents/{agent_id}
POST /workspaces/{workspace_id}/agents/{agent_id}/activate
POST /workspaces/{workspace_id}/agents/{agent_id}/pause
POST /workspaces/{workspace_id}/agents/{agent_id}/archive
POST /workspaces/{workspace_id}/agents/{agent_id}/recommendations
```

Future endpoints:

```text
GET /workspaces/{workspace_id}/agents/{agent_id}/audit
GET /workspaces/{workspace_id}/agents/{agent_id}/memory
POST /workspaces/{workspace_id}/agents/{agent_id}/escalate
```

---

# 21. Agent Service Responsibilities

`AgentRuntimeService` responsibilities:

- create agent suggestions;
- create agent records;
- assign human owner;
- define authority scope;
- manage lifecycle state;
- link agents to functions;
- generate recommendations;
- create action drafts;
- validate confirmation requirements;
- emit agent events;
- trigger audit recording;
- trigger memory creation where appropriate;
- expose agent status to dashboard.

---

# 22. Agent Data Validation

Required validation:

- workspace_id is required;
- agent name is required;
- agent role is required;
- human owner is required for active state;
- authority scope is required for active state;
- function link is recommended for MVP;
- archived agents cannot create recommendations;
- paused agents cannot create new outputs;
- AI-generated output must declare source agent.

---

# 23. MVP Acceptance Criteria

Agent Runtime is MVP-ready when:

- Bizzi can suggest agents from onboarding or operating map;
- user can create an agent from suggestion;
- user can assign human owner;
- user can link agent to function;
- authority scope can be defined;
- agent can create recommendations or drafts;
- important outputs require confirmation;
- agent actions create audit events;
- agent outputs can create memory entries when confirmed;
- dashboard shows active and suggested agents.

---

# 24. Out of Scope for MVP

The MVP does not require:

- fully autonomous agents;
- autonomous external communication;
- financial execution;
- legal execution;
- tool marketplace;
- agent-to-agent negotiation;
- multi-agent planning engine;
- long-running autonomous background agents;
- complex permission matrix;
- self-modifying agents.

---

# 25. Architecture Alignment

| Agent Runtime Area | Architecture Reference |
|---|---|
| Agent Object | Agent Library |
| Human Owner | Governance Baseline |
| Authority Scope | Autonomy Governance |
| Agent Recommendations | Product Vision / MVP Scope |
| Agent Events | Runtime Architecture |
| Agent Memory | Enterprise Memory |
| Agent Audit | Observability and Intelligence |
| Agent Dashboard | Core User Journey |
| Agent Security | Security / Governance Baseline |

---

# 26. Final Agent Runtime Statement

```text
Agent Runtime is the governed execution environment that allows Bizzi to place AI agents inside company functions, connect them to human owners, constrain their authority, capture their recommendations, preserve memory and produce audit evidence.
```

This component makes AI operational inside Bizzi without sacrificing accountability.