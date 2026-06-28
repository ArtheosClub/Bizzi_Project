# 10_AUDIT_AND_EVENT_DOMAIN.md

# Bizzi Platform

## Audit and Event Domain

**Layer:** 26_DOMAIN_MODEL  
**Component Type:** Domain Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 25_RUNTIME_PLATFORM / 09_AUDIT_RUNTIME.md, 10_EVENT_RUNTIME.md  
**Previous Documents:** 00_DOMAIN_MODEL_VISION.md, 01_ENTITY_CATALOG.md, 02_WORKSPACE_DOMAIN.md, 03_OPERATING_MAP_DOMAIN.md, 04_FUNCTION_AND_RESPONSIBILITY_DOMAIN.md, 05_AGENT_DOMAIN.md, 06_PROCESS_DOMAIN.md, 07_TASK_DOMAIN.md, 08_DECISION_DOMAIN.md, 09_MEMORY_DOMAIN.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Audit and Event Domain for Bizzi Platform.

The Audit and Event Domain describes how Bizzi represents governed activity, state changes, traceability records and evidence trails as structured domain objects.

Core question:

```text
How does Bizzi make runtime activity traceable, auditable and coordinated across workspaces, agents, tasks, decisions, memory, integrations and dashboards?
```

---

# 2. Domain Role

The Audit and Event Domain is the evidence and coordination domain of Bizzi.

It provides:

- runtime event capture;
- governed action evidence;
- actor/action/target traceability;
- AI assistance auditability;
- human confirmation records;
- object-level history;
- event-driven coordination;
- dashboard freshness;
- memory source support;
- security and compliance foundation.

---

# 3. Domain Principles

## 3.1 Audit by Default

Important governed actions should create audit evidence.

## 3.2 Important Changes Emit Events

Meaningful runtime state changes should emit domain events so other runtime components can react.

## 3.3 Evidence Before Trust

Bizzi should be trusted because important actions can be traced, not because the system claims to be correct.

## 3.4 Events Coordinate, Audit Proves

Events coordinate runtime behavior. Audit events preserve evidence.

---

# 4. Aggregate Boundaries

Primary aggregate roots:

```text
AuditEvent
RuntimeEvent
```

Supporting entities:

```text
AuditActor
AuditTarget
AuditMetadata
AuditExport
EventPayload
EventHandlerStatus
EventCorrelation
EventFailure
```

Related external entities:

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
Integration
ExportJob
DashboardMetric
SecurityPolicy
```

---

# 5. Core Entities

## 5.1 AuditEvent

Represents evidence of a governed runtime action.

Minimum domain attributes:

```text
id
workspace_id
actor_id
actor_type
action
object_type
object_id
timestamp
metadata
```

Optional domain attributes:

```text
source_event_id
agent_id
ai_assisted
human_confirmed
before_state
after_state
severity
correlation_id
ip_address
user_agent
```

Domain responsibility:

```text
AuditEvent records who did what, when, to which object and under which context.
```

---

## 5.2 RuntimeEvent

Represents a meaningful state change or runtime signal.

Minimum domain attributes:

```text
id
workspace_id
event_type
source_component
source_object_type
source_object_id
actor_id
timestamp
payload
status
```

Optional domain attributes:

```text
correlation_id
causation_id
severity
processed_at
handler_status
error_message
retry_count
```

Domain responsibility:

```text
RuntimeEvent coordinates internal state changes and provides a source for audit, memory and dashboard updates.
```

---

## 5.3 AuditExport

Represents a controlled export of audit data.

Potential attributes:

```text
id
workspace_id
requested_by
export_scope
format
status
created_at
completed_at
file_reference
```

Domain responsibility:

```text
AuditExport provides controlled access to audit evidence outside normal runtime screens.
```

---

## 5.4 EventCorrelation

Represents linkage between related runtime events.

Potential attributes:

```text
id
workspace_id
correlation_id
root_event_id
related_event_id
relationship_type
created_at
```

Domain responsibility:

```text
EventCorrelation preserves causal chains across multi-step runtime workflows.
```

MVP simplification:

```text
correlation_id and causation_id may be stored directly on RuntimeEvent.
```

---

## 5.5 EventFailure

Represents a failed event handling attempt.

Potential attributes:

```text
id
workspace_id
runtime_event_id
handler_name
error_message
retry_count
status
created_at
resolved_at
```

Domain responsibility:

```text
EventFailure makes event processing problems visible and diagnosable.
```

MVP simplification:

```text
Event failures may initially be recorded through RuntimeEvent.status and metadata.
```

---

# 6. Audit Categories

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
integration
export
dashboard
ai_assistance
runtime_event
```

MVP priority categories:

```text
workspace
task
decision
memory
agent
security
ai_assistance
```

---

# 7. Event Categories

Initial event categories:

```text
workspace
security
onboarding
operating_map
function
responsibility
agent
process
task
decision
memory
audit
integration
export
dashboard
system
```

---

# 8. Event Naming Convention

Recommended convention:

```text
object.action
```

Examples:

```text
workspace.created
task.created
decision.confirmed
memory.created
audit.recorded
agent.recommendation_created
integration.sync_completed
```

Event names should be stable, readable and implementation-friendly.

---

# 9. Audit Severity Levels

Suggested severity levels:

```text
info
notice
warning
critical
```

MVP levels:

```text
info
warning
critical
```

Severity should support filtering and dashboard alerts, not replace event type or audit category.

---

# 10. Event Statuses

Recommended statuses:

```text
emitted
processing
processed
failed
ignored
```

MVP statuses:

```text
emitted
processed
failed
```

---

# 11. Domain Relationships

## 11.1 Workspace to AuditEvent

```text
CompanyWorkspace 1 → many AuditEvents
```

## 11.2 Workspace to RuntimeEvent

```text
CompanyWorkspace 1 → many RuntimeEvents
```

## 11.3 RuntimeEvent to AuditEvent

```text
RuntimeEvent may cause AuditEvent
```

## 11.4 RuntimeEvent to MemoryEntry

```text
RuntimeEvent may create MemoryEntry candidate
```

## 11.5 RuntimeEvent to DashboardMetric

```text
RuntimeEvent may refresh DashboardMetric
```

## 11.6 AuditEvent to Actor and Target

```text
AuditEvent → actor_id + actor_type
AuditEvent → object_type + object_id
```

---

# 12. Domain Invariants

The Audit and Event Domain must enforce:

```text
AuditEvent must belong to one workspace.
RuntimeEvent must belong to one workspace.
AuditEvent must include actor, action, target and timestamp.
RuntimeEvent must include event_type, source and timestamp.
Audit events should not be silently deleted.
Event payloads must not expose raw secrets.
Audit metadata must not expose unauthorized data.
AI-assisted actions affecting runtime objects must be auditable.
Event handlers must respect workspace boundaries.
```

---

# 13. AI Audit Rules

AI-assisted actions must record:

```text
source_agent_id or source_ai_operation
input_context_scope
output_type
human_confirmation_status
result_object_type
result_object_id
```

AI may not:

- create untraceable governed changes;
- bypass human confirmation where required;
- hide its involvement in confirmed output;
- access audit data outside workspace scope;
- alter audit history.

MVP rule:

```text
If AI output changes a runtime object, Bizzi must record AI involvement and human confirmation status.
```

---

# 14. Event Creation Flow

```text
Runtime action occurs
↓
Domain service emits RuntimeEvent
↓
Event persisted with workspace scope
↓
Relevant handlers process event
↓
Audit may be recorded
↓
Memory may be created or updated
↓
Dashboard may be refreshed
↓
Event status updated
```

---

# 15. Audit Creation Flow

```text
Governed action occurs
↓
Actor and target identified
↓
Before and after state captured where needed
↓
AI involvement identified if applicable
↓
AuditEvent created
↓
Audit event linked to source RuntimeEvent if applicable
↓
Dashboard and export views can use audit evidence
```

---

# 16. Minimum MVP Events

The MVP should support at least:

```text
workspace.created
operating_map.generated
function.created
responsibility.assigned
ownership_gap.detected
agent.created
agent.recommendation_created
process.created
task.created
task.assigned
task.status_changed
decision.created
decision.confirmed
memory.created
memory.used_in_context
audit.recorded
integration.connected
export.generated
dashboard.updated
security.access_denied
```

---

# 17. Minimum MVP Audit Actions

The MVP should audit at least:

```text
workspace.created
workspace.updated
function.created
responsibility.assigned
agent.created
agent.authority_defined
agent.output_confirmed
task.created
task.assigned
task.status_changed
decision.confirmed
memory.created
memory.used_in_ai_context
integration.connected
export.generated
security.access_denied
```

---

# 18. Dashboard Requirements

Dashboard should show:

- recent audit activity;
- recent runtime events;
- critical audit events;
- failed events;
- AI-assisted actions;
- human confirmations;
- memory creation activity;
- decision confirmations;
- task status changes;
- security warnings.

Dashboard question:

```text
What important actions happened, what changed, and can the workspace trust the operating record?
```

---

# 19. Security Requirements

Security requirements:

```text
Audit and events belong to one workspace.
Only authorized users may view audit records.
Event payloads must be minimal and structured.
Raw credentials must never appear in audit or event payloads.
Audit exports require authorization.
Audit records should be append-only where possible.
AI context use of audit or event data must be workspace-scoped.
```

---

# 20. MVP Domain Behavior

MVP should support:

```text
Create runtime event
Persist runtime event
Record audit event
Link audit event to runtime event
Filter audit by workspace
Filter audit by object
Show recent audit activity
Show failed events
Record AI assistance
Record human confirmation
Generate simple audit export
```

---

# 21. Out of Scope for MVP

The Audit and Event Domain does not need in MVP:

- external event bus;
- Kafka or streaming infrastructure;
- full event sourcing;
- immutable blockchain logs;
- enterprise SIEM integration;
- legal-grade e-discovery;
- advanced anomaly detection;
- complex retry orchestration;
- cross-workspace event analytics.

---

# 22. Data Model Implications

Future Data Model should include tables or collections for:

```text
audit_events
runtime_events
```

Potential later tables:

```text
audit_exports
event_correlations
event_failures
event_handler_runs
```

Recommended indexes later:

```text
audit_events.workspace_id
audit_events.actor_id
audit_events.object_type
audit_events.object_id
audit_events.action
audit_events.timestamp
runtime_events.workspace_id
runtime_events.event_type
runtime_events.source_object_type
runtime_events.source_object_id
runtime_events.status
runtime_events.correlation_id
runtime_events.timestamp
```

---

# 23. API Implications

Future API contracts should support:

```text
GET /workspaces/{workspace_id}/audit
GET /workspaces/{workspace_id}/audit/{audit_event_id}
GET /workspaces/{workspace_id}/audit/object/{object_type}/{object_id}
POST /workspaces/{workspace_id}/audit/export
GET /workspaces/{workspace_id}/events
GET /workspaces/{workspace_id}/events/{event_id}
GET /workspaces/{workspace_id}/events/object/{object_type}/{object_id}
GET /workspaces/{workspace_id}/events/correlation/{correlation_id}
```

MVP may expose events indirectly through audit and dashboard.

---

# 24. Traceability Pattern

Audit and Event traceability chain:

```text
User / Agent / System Action
↓
Runtime Object Change
↓
RuntimeEvent
↓
AuditEvent
↓
MemoryEntry if useful
↓
DashboardMetric
↓
AuditExport if requested
```

---

# 25. Acceptance Criteria

Audit and Event Domain is ready when:

- AuditEvent is defined as aggregate root;
- RuntimeEvent is defined as aggregate root;
- audit categories are defined;
- event categories are defined;
- naming conventions are clear;
- AI audit rules are defined;
- dashboard role is defined;
- security rules are explicit;
- data model and API implications are identified.

Status:

```text
Ready for Data Model and API Design
```

---

# 26. Architecture Alignment

| Audit and Event Domain Area | Reference |
|---|---|
| AuditEvent | 09_AUDIT_RUNTIME.md |
| RuntimeEvent | 10_EVENT_RUNTIME.md |
| AI Assistance Audit | Agent Runtime / Runtime Security |
| Human Confirmation | Decision Runtime / Governance Baseline |
| Memory Source Support | Memory Runtime |
| Dashboard Updates | Core User Journey |
| Security Events | Runtime Security |
| Integration Events | Integration Runtime |
| Export Audit | Integration Runtime / Runtime Security |
| Traceability | Traceability Matrix |

---

# 27. Final Audit and Event Domain Statement

```text
Audit and Event Domain defines how Bizzi records evidence of governed activity and coordinates meaningful runtime state changes through workspace-scoped audit events and runtime events.
```

This domain ensures Bizzi can operate as a traceable, trustworthy and event-aware business runtime rather than an opaque AI application.