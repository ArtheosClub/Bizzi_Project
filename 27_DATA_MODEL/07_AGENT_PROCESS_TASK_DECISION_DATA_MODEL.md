# 07_AGENT_PROCESS_TASK_DECISION_DATA_MODEL.md

# Bizzi Platform

## Agent, Process, Task and Decision Data Model

**Layer:** 27_DATA_MODEL  
**Component Type:** Data Model Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 04_AGENT_RUNTIME.md, 05_PROCESS_RUNTIME.md, 06_TASK_RUNTIME.md, 07_DECISION_RUNTIME.md  
**Domain Reference:** 26_DOMAIN_MODEL / 05_AGENT_DOMAIN.md, 06_PROCESS_DOMAIN.md, 07_TASK_DOMAIN.md, 08_DECISION_DOMAIN.md  
**Previous Documents:** 00_DATA_MODEL_VISION.md, 01_DATABASE_PRINCIPLES.md, 02_ENTITY_TO_TABLE_MAPPING.md, 03_CORE_TABLES.md, 04_WORKSPACE_DATA_MODEL.md, 05_OPERATING_MAP_DATA_MODEL.md, 06_FUNCTION_RESPONSIBILITY_DATA_MODEL.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the data model for agents, processes, tasks and decisions in Bizzi Platform.

It translates the Agent, Process, Task and Decision domains into database tables, columns, relationships, constraints and indexing rules that support governed AI assistance, repeatable process structure, actionable work and decision memory.

Core question:

```text
How does Bizzi persist AI assistance, repeatable work, actionable tasks and business decisions as governed, traceable and workspace-scoped data?
```

---

# 2. Data Model Role

This data model connects operating structure to execution.

It supports:

- governed AI agents;
- agent authority and recommendations;
- process definition and process steps;
- task creation, ownership and status tracking;
- decision capture and follow-up;
- AI draft review;
- audit and runtime events;
- memory creation;
- dashboard visibility.

---

# 3. Tables in Scope

Priority 1 MVP table:

```text
tasks
decisions
```

Priority 2 governed runtime tables:

```text
agents
agent_authority_scopes
agent_recommendations
agent_action_drafts
processes
process_steps
```

Expansion tables:

```text
agent_escalation_rules
process_inputs
process_outputs
process_reviews
task_links
task_history
task_comments
task_blockers
decision_options
decision_outcomes
decision_reviews
```

Recommended MVP implementation:

```text
tasks
decisions
```

Recommended governed AI and process implementation:

```text
agents
agent_authority_scopes
agent_recommendations
agent_action_drafts
processes
process_steps
```

---

# 4. Workspace Scope Rule

All tables in this model must include:

```text
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
```

This preserves tenant isolation, AI context safety, dashboard filtering, export control and audit traceability.

---

# 5. agents Table

## Purpose

Stores governed AI agent roles inside a workspace.

## Domain Entity

```text
Agent
```

## Table

```text
agents
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
name TEXT NOT NULL
role TEXT NOT NULL
description TEXT NULL
status TEXT NOT NULL
human_owner_id UUID NULL REFERENCES users(id)
authority_scope_id UUID NULL
function_id UUID NULL REFERENCES functions(id)
process_id UUID NULL REFERENCES processes(id)
model_profile TEXT NULL
memory_access_scope TEXT NULL
confidence_policy TEXT NULL
source_object_type TEXT NULL
source_object_id UUID NULL
activated_at TIMESTAMPTZ NULL
paused_at TIMESTAMPTZ NULL
archived_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
created_by UUID NULL REFERENCES users(id)
metadata JSONB NULL
```

## Status Values

Initial values:

```text
suggested
active
paused
archived
```

Expansion values:

```text
draft
configured
```

## Notes

`authority_scope_id` may be added as a foreign key after `agent_authority_scopes` exists. To avoid circular dependency, the first implementation may rely on `agent_authority_scopes.agent_id` and leave `agents.authority_scope_id` nullable.

---

# 6. agent_authority_scopes Table

## Purpose

Stores explicit authority boundaries for agents.

## Domain Entity

```text
AgentAuthorityScope
```

## Table

```text
agent_authority_scopes
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
agent_id UUID NOT NULL REFERENCES agents(id)
allowed_actions JSONB NOT NULL
restricted_actions JSONB NULL
confirmation_required_actions JSONB NULL
max_autonomy_level TEXT NULL
memory_access_level TEXT NULL
external_tool_access JSONB NULL
integration_access_scope JSONB NULL
status TEXT NOT NULL
configured_by UUID NULL REFERENCES users(id)
configured_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## Status Values

```text
draft
active
paused
archived
```

## Notes

This table protects the system from uncontrolled AI execution.

---

# 7. agent_recommendations Table

## Purpose

Stores reviewable recommendations produced by agents.

## Domain Entity

```text
AgentRecommendation
```

## Table

```text
agent_recommendations
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
agent_id UUID NOT NULL REFERENCES agents(id)
title TEXT NOT NULL
description TEXT NULL
recommendation_type TEXT NOT NULL
status TEXT NOT NULL
source_object_type TEXT NULL
source_object_id UUID NULL
suggested_object_type TEXT NULL
suggested_object_payload JSONB NULL
confidence TEXT NULL
reviewed_by UUID NULL REFERENCES users(id)
reviewed_at TIMESTAMPTZ NULL
confirmed_by UUID NULL REFERENCES users(id)
confirmed_at TIMESTAMPTZ NULL
rejected_at TIMESTAMPTZ NULL
result_object_type TEXT NULL
result_object_id UUID NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## Status Values

```text
created
reviewed
confirmed
applied
rejected
archived
```

## Notes

Recommendations must stay reviewable and traceable before they create official runtime objects.

---

# 8. agent_action_drafts Table

## Purpose

Stores draft actions or draft objects prepared by an agent.

## Domain Entity

```text
AgentActionDraft
```

## Table

```text
agent_action_drafts
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
agent_id UUID NOT NULL REFERENCES agents(id)
draft_type TEXT NOT NULL
title TEXT NOT NULL
payload JSONB NOT NULL
status TEXT NOT NULL
source_object_type TEXT NULL
source_object_id UUID NULL
reviewed_by UUID NULL REFERENCES users(id)
confirmed_by UUID NULL REFERENCES users(id)
confirmed_at TIMESTAMPTZ NULL
rejected_at TIMESTAMPTZ NULL
result_object_type TEXT NULL
result_object_id UUID NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## Status Values

```text
draft
reviewed
confirmed
rejected
applied
archived
```

---

# 9. processes Table

## Purpose

Stores repeatable business processes.

## Domain Entity

```text
Process
```

## Table

```text
processes
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
name TEXT NOT NULL
purpose TEXT NULL
description TEXT NULL
function_id UUID NULL REFERENCES functions(id)
owner_user_id UUID NULL REFERENCES users(id)
status TEXT NOT NULL
trigger TEXT NULL
frequency TEXT NULL
risk_level TEXT NULL
maturity_level TEXT NULL
success_criteria TEXT NULL
agent_id UUID NULL REFERENCES agents(id)
source_object_type TEXT NULL
source_object_id UUID NULL
confirmed_by UUID NULL REFERENCES users(id)
confirmed_at TIMESTAMPTZ NULL
last_reviewed_at TIMESTAMPTZ NULL
archived_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
created_by UUID NULL REFERENCES users(id)
metadata JSONB NULL
```

## Status Values

Initial values:

```text
suggested
draft
active
archived
```

Expansion values:

```text
defined
reviewed
improved
```

---

# 10. process_steps Table

## Purpose

Stores ordered steps inside a process.

## Domain Entity

```text
ProcessStep
```

## Table

```text
process_steps
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
process_id UUID NOT NULL REFERENCES processes(id)
step_order INTEGER NOT NULL
title TEXT NOT NULL
description TEXT NULL
status TEXT NOT NULL
responsible_user_id UUID NULL REFERENCES users(id)
expected_input TEXT NULL
expected_output TEXT NULL
automation_candidate BOOLEAN NOT NULL DEFAULT false
agent_assist_allowed BOOLEAN NOT NULL DEFAULT true
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
metadata JSONB NULL
```

## Status Values

```text
active
removed
```

Expansion values:

```text
draft
changed
```

## Constraint

Recommended:

```text
UNIQUE(process_id, step_order)
```

---

# 11. tasks Table

## Purpose

Stores actionable work items.

## Domain Entity

```text
Task
```

## Table

```text
tasks
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
title TEXT NOT NULL
description TEXT NULL
status TEXT NOT NULL
priority TEXT NOT NULL DEFAULT 'normal'
owner_user_id UUID NULL REFERENCES users(id)
function_id UUID NULL REFERENCES functions(id)
process_id UUID NULL REFERENCES processes(id)
decision_id UUID NULL REFERENCES decisions(id)
agent_id UUID NULL REFERENCES agents(id)
operating_gap_id UUID NULL REFERENCES operating_gaps(id)
source_object_type TEXT NULL
source_object_id UUID NULL
due_date DATE NULL
completed_at TIMESTAMPTZ NULL
archived_at TIMESTAMPTZ NULL
blocked_reason TEXT NULL
confirmed_by UUID NULL REFERENCES users(id)
confirmed_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
created_by UUID NULL REFERENCES users(id)
metadata JSONB NULL
```

## Status Values

Initial values:

```text
suggested
open
in_progress
completed
archived
```

Optional MVP value:

```text
blocked
```

## Priority Values

```text
low
normal
high
urgent
```

---

# 12. decisions Table

## Purpose

Stores important business decisions.

## Domain Entity

```text
Decision
```

## Table

```text
decisions
```

## Columns

```text
id UUID PRIMARY KEY
workspace_id UUID NOT NULL REFERENCES company_workspaces(id)
title TEXT NOT NULL
context TEXT NULL
final_decision TEXT NULL
rationale TEXT NULL
owner_user_id UUID NULL REFERENCES users(id)
status TEXT NOT NULL
function_id UUID NULL REFERENCES functions(id)
process_id UUID NULL REFERENCES processes(id)
task_id UUID NULL REFERENCES tasks(id)
agent_id UUID NULL REFERENCES agents(id)
source_object_type TEXT NULL
source_object_id UUID NULL
decision_date DATE NULL
review_date DATE NULL
expected_impact TEXT NULL
risk_level TEXT NULL
outcome_summary TEXT NULL
confirmed_by UUID NULL REFERENCES users(id)
confirmed_at TIMESTAMPTZ NULL
archived_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
created_by UUID NULL REFERENCES users(id)
metadata JSONB NULL
```

## Status Values

Initial values:

```text
draft
confirmed
archived
```

Optional MVP value:

```text
implemented
```

Expansion values:

```text
proposed
reviewed
```

---

# 13. Key Relationships

## Agent Relationships

```text
company_workspaces.id → agents.workspace_id
users.id → agents.human_owner_id
functions.id → agents.function_id
processes.id → agents.process_id
agents.id → agent_authority_scopes.agent_id
agents.id → agent_recommendations.agent_id
agents.id → agent_action_drafts.agent_id
```

## Process Relationships

```text
company_workspaces.id → processes.workspace_id
functions.id → processes.function_id
users.id → processes.owner_user_id
agents.id → processes.agent_id
processes.id → process_steps.process_id
```

## Task Relationships

```text
company_workspaces.id → tasks.workspace_id
users.id → tasks.owner_user_id
functions.id → tasks.function_id
processes.id → tasks.process_id
decisions.id → tasks.decision_id
agents.id → tasks.agent_id
operating_gaps.id → tasks.operating_gap_id
```

## Decision Relationships

```text
company_workspaces.id → decisions.workspace_id
users.id → decisions.owner_user_id
functions.id → decisions.function_id
processes.id → decisions.process_id
tasks.id → decisions.task_id
agents.id → decisions.agent_id
```

---

# 14. Source Traceability

Core source fields:

```text
source_object_type
source_object_id
```

Used by:

```text
agents
processes
tasks
decisions
agent_recommendations
agent_action_drafts
```

Examples:

```text
source_object_type = 'operating_gap'
source_object_type = 'agent_recommendation'
source_object_type = 'decision'
source_object_type = 'process'
source_object_type = 'user_input'
```

---

# 15. Indexing Requirements

## agents

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(human_owner_id)
INDEX(function_id)
INDEX(process_id)
INDEX(source_object_type, source_object_id)
```

## agent_authority_scopes

```text
INDEX(workspace_id)
INDEX(agent_id)
INDEX(workspace_id, status)
```

## agent_recommendations

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(agent_id)
INDEX(source_object_type, source_object_id)
INDEX(result_object_type, result_object_id)
```

## processes

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(function_id)
INDEX(owner_user_id)
INDEX(agent_id)
INDEX(source_object_type, source_object_id)
```

## process_steps

```text
INDEX(workspace_id)
INDEX(process_id)
INDEX(process_id, step_order)
```

## tasks

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(owner_user_id)
INDEX(function_id)
INDEX(process_id)
INDEX(decision_id)
INDEX(agent_id)
INDEX(operating_gap_id)
INDEX(due_date)
INDEX(source_object_type, source_object_id)
```

## decisions

```text
INDEX(workspace_id)
INDEX(workspace_id, status)
INDEX(owner_user_id)
INDEX(function_id)
INDEX(process_id)
INDEX(task_id)
INDEX(agent_id)
INDEX(decision_date)
INDEX(source_object_type, source_object_id)
```

---

# 16. Data Integrity Rules

Database-level rules:

```text
agents.workspace_id IS NOT NULL
agents.name IS NOT NULL
agents.role IS NOT NULL
processes.workspace_id IS NOT NULL
processes.name IS NOT NULL
tasks.workspace_id IS NOT NULL
tasks.title IS NOT NULL
tasks.status IS NOT NULL
decisions.workspace_id IS NOT NULL
decisions.title IS NOT NULL
decisions.status IS NOT NULL
```

Service-level rules:

```text
Active Agent must have human_owner_id.
Active Agent must have authority scope.
Active Process should have owner_user_id.
Process steps must preserve step_order.
Open Task should have owner or be explicitly unassigned.
Completed Task must have completed_at.
Confirmed Decision must have final_decision and owner_user_id.
AI-generated official changes require confirmation.
Referenced objects must belong to the same workspace.
```

---

# 17. AI Governance Persistence

AI-assisted objects must preserve:

```text
agent_id
source_object_type
source_object_id
status
confidence
confirmed_by
confirmed_at
rejected_at
result_object_type
result_object_id
```

Rule:

```text
AI may draft, suggest and recommend. Human confirmation creates official runtime meaning.
```

---

# 18. Audit Requirements

Audited actions include:

```text
agent.created
agent.activated
agent.paused
agent.archived
agent.authority_defined
agent.recommendation_created
agent.output_confirmed
process.created
process.updated
process.step_added
process.owner_assigned
task.created
task.assigned
task.status_changed
task.completed
decision.created
decision.confirmed
decision.followup_task_created
```

Audit target examples:

```text
object_type = 'agent'
object_type = 'process'
object_type = 'task'
object_type = 'decision'
```

---

# 19. Runtime Event Requirements

Runtime events include:

```text
agent.created
agent.recommendation_created
process.created
process.step_added
task.created
task.assigned
task.status_changed
task.completed
decision.created
decision.confirmed
decision.followup_task_created
```

Event source pattern:

```text
source_object_type = 'task'
source_object_id = tasks.id
```

or equivalent object references for agents, processes and decisions.

---

# 20. Dashboard Requirements

Dashboard queries should support:

- active agents;
- pending agent recommendations;
- active processes;
- processes without owners;
- open tasks;
- blocked tasks;
- overdue tasks;
- tasks by owner;
- recent decisions;
- decisions requiring follow-up;
- AI-assisted decisions and actions.

---

# 21. Memory Requirements

Memory may be created from:

- confirmed agent recommendations;
- confirmed process definitions;
- important task outcomes;
- decision context;
- decision rationale;
- decision outcomes;
- recurring blockers.

Memory source references should point back to:

```text
agents.id
agent_recommendations.id
processes.id
tasks.id
decisions.id
```

---

# 22. MVP Simplifications

For MVP, Bizzi may simplify by:

- implementing tasks and decisions before full agents and processes;
- storing process inputs and outputs as text or JSONB on `processes`;
- using audit events instead of task history;
- using direct nullable references instead of task_links and decision_links;
- using text statuses before PostgreSQL ENUM migration;
- using service-level validation for cross-object workspace consistency.

These simplifications must preserve traceability, ownership and auditability.

---

# 23. Future Expansion

Future tables may include:

```text
agent_escalation_rules
agent_context_scopes
process_inputs
process_outputs
process_gaps
process_reviews
task_links
task_history
task_comments
task_blockers
decision_options
decision_outcomes
decision_reviews
decision_links
```

These should be introduced when product behavior requires more detail.

---

# 24. Acceptance Criteria

This data model is ready when:

- agents table is defined;
- agent authority and output tables are defined;
- processes and process_steps are defined;
- tasks table is defined;
- decisions table is defined;
- workspace scoping is explicit;
- ownership and confirmation rules are documented;
- indexes are identified;
- audit and event requirements are defined;
- MVP simplifications are documented.

Status:

```text
Accepted for Implementation Planning
```

---

# 25. Final Statement

```text
Bizzi Agent, Process, Task and Decision Data Model defines how the platform persists governed AI assistance, repeatable work, actionable execution and business decisions as workspace-scoped, auditable and traceable database records.
```

This model enables Bizzi to move from operating clarity into structured execution.