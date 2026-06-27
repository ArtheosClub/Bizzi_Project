# 10_EVENT_RUNTIME.md

# Bizzi Platform

## Event Runtime

**Layer:** 25_RUNTIME_PLATFORM  
**Component Type:** Runtime Component Specification  
**Foundation:** Art of Business Canonical Release v1.0  
**Product Definition Reference:** 24_PRODUCTIZATION_AND_IMPLEMENTATION  
**Runtime Reference:** 00_RUNTIME_VISION.md, 01_RUNTIME_ARCHITECTURE.md, 02_CORE_RUNTIME_COMPONENTS.md, 03_WORKSPACE_RUNTIME.md, 04_AGENT_RUNTIME.md, 05_PROCESS_RUNTIME.md, 06_TASK_RUNTIME.md, 07_DECISION_RUNTIME.md, 08_MEMORY_RUNTIME.md, 09_AUDIT_RUNTIME.md  
**Status:** Draft v0.1  
**Product:** Bizzi Platform  
**Implementation Phase:** Epoch II — Reference Implementation

---

# 1. Purpose

This document defines the Event Runtime for Bizzi Platform.

Event Runtime is responsible for capturing, coordinating and distributing important state changes across Bizzi runtime components.

Core question:

```text
How does Bizzi coordinate runtime state changes so that workspace actions, tasks, decisions, memory, audit and dashboards remain synchronized and traceable?
```

---

# 2. Runtime Role

Event Runtime is the internal coordination layer of Bizzi.

It connects events across:

- workspace;
- onboarding;
- operating map;
- functions;
- responsibilities;
- agents;
- processes;
- tasks;
- decisions;
- memory;
- audit;
- dashboard;
- security;
- exports;
- AI orchestration.

---

# 3. Event Runtime Principle

```text
Important Changes Emit Events
```

Bizzi should not rely only on direct service calls for meaningful state changes.

Important runtime actions should emit events so other components can react, record evidence, update memory and refresh dashboards.

---

# 4. Primary Runtime Objects

Minimum objects:

```text
RuntimeEvent
EventType
EventPayload
EventSource
EventHandler
EventStatus
EventCorrelation
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
AuditEvent
DashboardMetric
```

---

# 5. RuntimeEvent Object

## Purpose

Represents a meaningful state change or runtime signal inside Bizzi.

## Minimum Fields

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

## Optional Fields

```text
correlation_id
causation_id
severity
handler_status
processed_at
error_message
retry_count
```

---

# 6. Event Categories

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
dashboard
export
ai
system
```

The MVP should keep categories simple and expandable.

---

# 7. Event Naming Convention

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
dashboard.updated
agent.recommendation_created
```

Event names should be stable and readable.

---

# 8. Core Operations

## 8.1 Emit Event

Creates a runtime event when an important state change occurs.

## 8.2 Persist Event

Stores the event for traceability and replay potential.

## 8.3 Dispatch Event

Sends the event to relevant runtime handlers.

## 8.4 Process Event

Executes event-driven updates such as audit recording, memory creation or dashboard refresh.

## 8.5 Track Event Status

Tracks whether an event was emitted, processed, failed or ignored.

## 8.6 Correlate Events

Links related events into a traceable chain.

---

# 9. Event Flow

```text
Runtime action occurs
↓
Service emits event
↓
Event Runtime persists event
↓
Event Runtime dispatches event
↓
Audit Runtime records evidence
↓
Memory Runtime creates or updates memory if applicable
↓
Dashboard Runtime refreshes relevant metrics
↓
Event status is updated
```

---

# 10. MVP Event Handling Model

The MVP should start simple:

```text
Internal Event Table
Synchronous Dispatch First
Simple Handler Registry
Audit and Dashboard Handlers First
Async Later
```

This avoids premature infrastructure complexity while preserving event-aware architecture.

---

# 11. Event Statuses

Suggested statuses:

```text
emitted
processing
processed
failed
ignored
```

MVP required statuses:

```text
emitted
processed
failed
```

---

# 12. Minimum Events

The MVP should support at least:

```text
workspace.created
workspace.updated
intake.completed
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
audit.recorded
dashboard.updated
export.generated
```

---

# 13. Event Handlers

Initial handlers:

```text
AuditEventHandler
MemoryEventHandler
DashboardEventHandler
NotificationEventHandler
AIContextEventHandler
```

MVP priority:

```text
AuditEventHandler
DashboardEventHandler
MemoryEventHandler
```

---

# 14. Event Audit Integration

Event Runtime supports Audit Runtime by providing structured event sources.

Audit Runtime may create audit records from events such as:

- workspace.created;
- agent.authority_defined;
- task.status_changed;
- decision.confirmed;
- memory.confirmed;
- export.generated;
- access.denied.

Audit question:

```text
Which runtime event caused this audit record?
```

---

# 15. Event Memory Integration

Event Runtime supports Memory Runtime when events represent meaningful knowledge.

Memory candidates may be created from:

- decision.confirmed;
- process.reviewed;
- task.completed;
- agent.recommendation_confirmed;
- operating_gap.detected;
- onboarding.completed.

Memory question:

```text
Which event produced or updated this memory entry?
```

---

# 16. Event Dashboard Integration

Event Runtime supports dashboard freshness.

Dashboard updates may be triggered by:

- task.created;
- task.status_changed;
- responsibility.assigned;
- ownership_gap.detected;
- decision.confirmed;
- memory.created;
- audit.recorded;
- agent.created.

Dashboard question:

```text
Which event changed the visible operating state?
```

---

# 17. Event Security Boundary

Event Runtime must enforce:

```text
Events belong to one workspace.
Events must reference workspace_id.
Event payloads must not expose unauthorized data.
Only authorized services may emit governed events.
Event handlers must respect workspace access boundaries.
Event logs should not be silently deleted.
AI usage of event data must be workspace-scoped.
```

---

# 18. Event Context Model

Event context may include:

- workspace id;
- actor id;
- actor type;
- source component;
- object type;
- object id;
- action;
- timestamp;
- payload;
- correlation id;
- causation id;
- severity.

This context supports traceability and future observability.

---

# 19. Event API Boundary

Event Runtime may initially remain internal.

Suggested future API group:

```text
/events
```

Future endpoints:

```text
GET /workspaces/{workspace_id}/events
GET /workspaces/{workspace_id}/events/{event_id}
GET /workspaces/{workspace_id}/events/object/{object_type}/{object_id}
GET /workspaces/{workspace_id}/events/correlation/{correlation_id}
```

MVP may expose events only indirectly through audit and dashboard.

---

# 20. Event Service Responsibilities

`EventRuntimeService` responsibilities:

- define event types;
- emit runtime events;
- persist runtime events;
- dispatch events to handlers;
- track event status;
- support correlation and causation;
- trigger audit, memory and dashboard updates;
- expose event logs for debugging and future observability.

---

# 21. Event Data Validation

Required validation:

- workspace_id is required;
- event_type is required;
- source_component is required;
- timestamp is required;
- payload must be structured;
- event_type should follow naming convention;
- source_object_type and source_object_id are recommended;
- correlation_id is recommended for multi-step workflows.

---

# 22. MVP Acceptance Criteria

Event Runtime is MVP-ready when:

- important runtime actions emit events;
- events are persisted;
- events include workspace, type, source and timestamp;
- audit can be triggered from events;
- dashboard can be refreshed from events;
- memory candidates can be created from selected events;
- event failures can be recorded;
- event model remains simple enough for MVP implementation.

---

# 23. Out of Scope for MVP

The MVP does not require:

- external event bus;
- Kafka or similar streaming infrastructure;
- event sourcing for all objects;
- distributed saga orchestration;
- complex retries;
- cross-workspace event streams;
- public event API;
- real-time websocket event delivery.

---

# 24. Architecture Alignment

| Event Runtime Area | Architecture Reference |
|---|---|
| RuntimeEvent | Runtime Architecture |
| Event Flow | Core Runtime Components |
| Audit Handler | Audit Runtime |
| Memory Handler | Memory Runtime |
| Dashboard Handler | Core User Journey |
| Workspace Scope | Workspace Runtime |
| Event Security | Security / Governance Baseline |
| Event Traceability | Traceability Matrix |

---

# 25. Final Event Runtime Statement

```text
Event Runtime is the component that coordinates meaningful state changes across Bizzi, allowing runtime actions to trigger audit, memory, dashboard and future orchestration behavior in a traceable and extensible way.
```

This component gives Bizzi an event-aware internal nervous system without requiring premature distributed infrastructure.