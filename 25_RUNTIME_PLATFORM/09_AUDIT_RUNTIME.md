# 09_AUDIT_RUNTIME.md

# Bizzi Platform

## Audit Runtime

**Layer:** 25_RUNTIME_PLATFORM  
**Component Type:** Runtime Component Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 00_RUNTIME_VISION.md, 01_RUNTIME_ARCHITECTURE.md, 02_CORE_RUNTIME_COMPONENTS.md, 03_WORKSPACE_RUNTIME.md, 04_AGENT_RUNTIME.md, 05_PROCESS_RUNTIME.md, 06_TASK_RUNTIME.md, 07_DECISION_RUNTIME.md, 08_MEMORY_RUNTIME.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Audit Runtime for Bizzi Platform.

Audit Runtime is responsible for recording traceable evidence of important runtime activity inside a company workspace.

Core question:

```text
How does Bizzi make business actions, AI assistance, ownership changes, decisions, memory and operating events auditable by default?
```

---

# 2. Runtime Role

Audit Runtime is the evidence layer of Bizzi.

It connects audit records to:

- workspace;
- users;
- functions;
- responsibilities;
- agents;
- processes;
- tasks;
- decisions;
- memory entries;
- runtime events;
- dashboard visibility;
- exports.

---

# 3. Audit Runtime Principle

```text
Audit by Default
```

Every governed action should produce audit evidence.

Audit evidence should answer:

```text
Who did what?
When did it happen?
Which object was affected?
What changed?
Was AI involved?
Was human confirmation required?
```

---

# 4. Primary Runtime Objects

Minimum objects:

```text
AuditEvent
AuditActor
AuditAction
AuditTarget
AuditMetadata
AuditSource
AuditSeverity
AuditExport
```

Supporting objects:

```text
CompanyWorkspace
User
Agent
Function
Responsibility
Process
Task
Decision
MemoryEntry
RuntimeEvent
DashboardMetric
```

---

# 5. AuditEvent Object

## Purpose

Represents a traceable record of an important runtime action.

## Minimum Fields

```text
id
workspace_id
actor_id
action
object_type
object_id
timestamp
metadata
```

## Optional Fields

```text
actor_type
source_event_id
agent_id
ai_assisted
human_confirmed
before_state
after_state
severity
ip_address
user_agent
correlation_id
```

---

# 6. Audit Event Categories

Initial audit categories:

```text
workspace
security
function
responsibility
agent
process
task
decision
memory
dashboard
export
ai_assistance
runtime_event
```

The MVP should keep categories simple and expandable.

---

# 7. Audit Severity Levels

Suggested severity levels:

```text
info
notice
warning
critical
```

MVP may begin with:

```text
info
warning
critical
```

Examples:

- `info`: task created;
- `warning`: ownership gap detected;
- `critical`: permission change or archived workspace.

---

# 8. Core Operations

## 8.1 Record Audit Event

Creates an audit event for a governed runtime action.

## 8.2 Link Audit to Runtime Object

Connects audit event to affected object.

## 8.3 Link Audit to Actor

Connects audit event to human user, system or AI agent.

## 8.4 Record Before and After State

Captures change details when appropriate.

## 8.5 Query Audit Trail

Retrieves audit events by workspace, object, actor, category or time range.

## 8.6 Export Audit Trail

Produces a shareable audit export.

## 8.7 Record AI Assistance

Captures when AI generated, suggested or drafted content.

## 8.8 Record Human Confirmation

Captures when human approval was required and given.

---

# 9. Audit Creation Flow

```text
Governed action occurs
↓
Runtime service emits event
↓
Audit Runtime receives audit request
↓
Actor, action and target are identified
↓
Metadata is attached
↓
Audit event is stored
↓
Dashboard and export views can use it
```

---

# 10. AI-Assisted Audit Flow

```text
AI generates recommendation or draft
↓
Agent Runtime or AI Orchestration Runtime records source
↓
User reviews output
↓
User confirms or rejects
↓
Audit Runtime records AI involvement
↓
Audit Runtime records human confirmation
↓
Memory and object changes link back to audit record
```

MVP rule:

```text
AI-assisted outputs must be auditable when they affect runtime objects.
```

---

# 11. Audit Events

Minimum events emitted by Audit Runtime:

```text
audit.recorded
audit.export_requested
audit.export_generated
audit.query_executed
audit.ai_assistance_recorded
audit.human_confirmation_recorded
```

Audit records must include:

```text
audit_event_id
workspace_id
actor_id
action
object_type
object_id
timestamp
metadata
```

---

# 12. Audited Runtime Actions

Minimum audited actions:

```text
workspace.created
workspace.profile_updated
workspace.archived
function.created
function.updated
responsibility.assigned
responsibility.changed
agent.created
agent.authority_defined
agent.output_confirmed
process.created
process.updated
task.created
task.assigned
task.status_changed
decision.created
decision.confirmed
memory.created
memory.confirmed
memory.used_in_context
export.generated
access.denied
```

---

# 13. Audit Dashboard Integration

Dashboard should show:

- recent audit activity;
- critical audit events;
- AI-assisted actions;
- human confirmations;
- ownership changes;
- decision confirmations;
- memory creations;
- exports generated;
- access warnings.

Dashboard question:

```text
What important actions happened in the workspace, and can they be traced?
```

---

# 14. Audit Memory Integration

Audit events do not automatically become enterprise memory.

However, audit events may support memory when they reveal:

- repeated operational patterns;
- lessons learned;
- governance issues;
- risk events;
- decision history;
- process changes.

Possible memory types:

```text
audit_summary
governance_lesson
risk_signal
operating_pattern
```

---

# 15. Audit Security Boundary

Audit Runtime must enforce:

```text
Audit events belong to one workspace.
Audit events must reference workspace_id.
Audit events should be append-only where possible.
Audit events should not be silently deleted.
Audit metadata must not expose unauthorized data.
Audit export must respect workspace access.
AI usage of audit data must be scoped to workspace permissions.
```

---

# 16. Audit Context Model

Audit context may include:

- actor;
- actor type;
- action;
- object type;
- object id;
- timestamp;
- before state;
- after state;
- AI involvement;
- human confirmation;
- severity;
- correlation id.

This context supports traceability, dashboard visibility and future compliance workflows.

---

# 17. Audit API Boundary

Suggested API group:

```text
/audit
```

Minimum endpoints:

```text
GET /workspaces/{workspace_id}/audit
GET /workspaces/{workspace_id}/audit/{audit_event_id}
GET /workspaces/{workspace_id}/audit/object/{object_type}/{object_id}
POST /workspaces/{workspace_id}/audit/export
```

Future endpoints:

```text
GET /workspaces/{workspace_id}/audit/actor/{actor_id}
GET /workspaces/{workspace_id}/audit/ai-assisted
GET /workspaces/{workspace_id}/audit/critical
POST /workspaces/{workspace_id}/audit/query
```

---

# 18. Audit Service Responsibilities

`AuditRuntimeService` responsibilities:

- record audit events;
- validate actor and target;
- store audit metadata;
- link audit to runtime events;
- record AI involvement;
- record human confirmation;
- expose audit trail by workspace;
- support object-level audit lookup;
- support dashboard audit summaries;
- generate audit exports.

---

# 19. Audit Data Validation

Required validation:

- workspace_id is required;
- actor_id or actor_type is required;
- action is required;
- object_type is required;
- object_id is recommended;
- timestamp is required;
- metadata must be structured;
- AI-assisted actions should identify source agent or AI service;
- human confirmations should identify confirming user.

---

# 20. MVP Acceptance Criteria

Audit Runtime is MVP-ready when:

- governed actions create audit events;
- audit events include actor, action, object and timestamp;
- AI-assisted object changes are auditable;
- human confirmations are auditable;
- audit trail can be viewed by workspace;
- audit trail can be filtered by object;
- dashboard can show recent audit activity;
- audit export can be generated in a simple format.

---

# 21. Out of Scope for MVP

The MVP does not require:

- enterprise compliance certification;
- immutable blockchain audit logs;
- external SIEM integration;
- advanced anomaly detection;
- legal-grade e-discovery;
- complex retention policies;
- cross-workspace audit analytics;
- automated compliance reporting.

---

# 22. Architecture Alignment

| Audit Runtime Area | Architecture Reference |
|---|---|
| AuditEvent | Observability and Intelligence |
| Actor and Target | Governance Baseline |
| AI Assistance Audit | Autonomy Governance |
| Human Confirmation | Decision Routing / Governance |
| Object Linkage | Traceability Matrix |
| Audit Dashboard | Core User Journey |
| Audit Export | MVP Scope |
| Audit Security | Security / Governance Baseline |

---

# 23. Final Audit Runtime Statement

```text
Audit Runtime is the component that records evidence of governed activity, making Bizzi actions, AI assistance, human confirmations, decisions, memory and operating changes traceable by default.
```

This component ensures Bizzi can be trusted as an enterprise operating system, not only used as a productivity tool.