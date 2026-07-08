# CORE Workflow and State Machine Framework

Version: 1.0
Status: Core Architecture Foundation Specification

Related Architecture:
- CORE_Enterprise_Object_Model.md
- CORE_Enterprise_Event_Model.md
- CORE_Decision_Framework.md

Related Capability:
- C07 Operations
- C13 Technology
- C15 Governance

Primary Owner:
- AG009 Enterprise Architect

Operational Owner:
- AG047 Process Controller

Governance Owner:
- AG002 Chief Orchestrator

Audit Owner:
- AG003 AI Auditor

---

## 00. Executive Summary

The CORE Workflow and State Machine Framework defines how Bizzi represents work, lifecycle states, transitions, approvals, exceptions, and completion.

A workflow is not just a list of tasks. It is a governed state machine that defines what can happen, who may trigger it, what conditions must be met, and what events are emitted.

Core principle:

```text
Every important object should have a visible lifecycle.
Every lifecycle transition should be authorized, traceable, and auditable.
```

---

## 01. Purpose

This document defines:

- workflow structure;
- state machine principles;
- lifecycle states;
- transition rules;
- triggers;
- guard conditions;
- exception handling;
- ownership;
- audit and event integration.

---

## 02. Definitions

### Workflow

A structured sequence of states and transitions that moves work from start to completion.

### State Machine

A formal model defining allowed states, allowed transitions, trigger conditions, and transition outcomes.

### Transition

A movement from one state to another caused by an event, decision, agent action, or system trigger.

---

## 03. Workflow Object Model

```yaml
id: WF-YYYY-####
workflow_name:
related_object:
related_playbook:
owner_agent:
states:
transitions:
entry_conditions:
exit_conditions:
guard_conditions:
exception_paths:
escalation_paths:
events_emitted:
status:
```

---

## 04. Generic State Model

```text
Not Started
  -> Draft / Intake
  -> In Progress
  -> Under Review
  -> Approved / Rejected
  -> Execution
  -> Validation
  -> Completed
  -> Closed / Archived
```

Domain workflows may customize this model, but must preserve traceability.

---

## 05. Transition Data Model

```yaml
transition_id:
from_state:
to_state:
trigger_event:
trigger_agent:
required_decision:
guard_conditions:
outputs:
events_emitted:
audit_required:
escalation_if_failed:
```

---

## 06. Guard Conditions

Guard conditions define what must be true before a transition is allowed.

Examples:

- required fields completed;
- decision approved;
- risk review completed;
- KPI threshold met;
- human override completed;
- audit passed;
- rollback condition not triggered;
- owner assigned.

---

## 07. Exception Handling

Every critical workflow should define exception states:

| Exception State | Meaning |
|---|---|
| Blocked | Cannot continue without intervention |
| Escalated | Higher authority required |
| Rework | Returned to earlier stage |
| Failed | Execution did not complete |
| Rolled Back | Previous state restored |
| Suspended | Temporarily paused |
| Cancelled | Ended without completion |

---

## 08. Workflow Events

Workflow transitions should emit events:

- workflow_started;
- state_entered;
- transition_completed;
- review_requested;
- decision_required;
- escalation_triggered;
- rollback_triggered;
- workflow_completed;
- workflow_failed.

These events follow the CORE Enterprise Event Model.

---

## 09. Workflow Governance

Governance requirements:

- every workflow has an owner;
- every state has a purpose;
- every transition has a trigger;
- high-impact transitions require decision linkage;
- exception paths are defined;
- lifecycle history is preserved;
- state changes are auditable.

---

## 10. Integration

This framework supports:

- PB032 stage lifecycle;
- agent lifecycle;
- decision workflows;
- audit workflows;
- pattern publication;
- memory publication;
- KPI review workflows;
- integration workflows.

---

## 11. Success Criteria

This specification is successful if Bizzi can:

- represent work as governed state machines;
- prevent invalid transitions;
- trigger events consistently;
- support audit and rollback;
- route exceptions clearly;
- enable future workflow automation.

---

## 12. Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-08 | Initial Core Workflow and State Machine Framework foundation specification |
