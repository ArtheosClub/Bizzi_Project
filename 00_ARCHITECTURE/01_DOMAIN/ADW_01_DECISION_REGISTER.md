# ADW-01 — Decision Register

**Document ID:** ARCH-DOMAIN-DECISIONS-001  
**Version:** 0.7-draft  
**Status:** Workshop in progress — D07 active  
**Architecture Gate:** Gate C v1.1  
**Workshop:** ADW-01 — Core Domain Semantics  
**Decision authority:** Project Owner  
**Parent chapter:** `00_ARCHITECTURE/01_DOMAIN/ADW_01_CORE_DOMAIN_SEMANTICS.md`  
**Foundation:** `00_ARCHITECTURE/00_FOUNDATION/DOMAIN_FOUNDATION.md`

---

## 1. Purpose

This register is the authoritative decision log for ADW-01 — Core Domain Semantics.

Each decision is recorded independently so approval, supersession, closure, and remaining workshop work remain explicit and auditable.

The former active term `Domain Core` and the former parent path `DOMAIN_CORE.md` are retired.

---

## 2. Decision Status Summary

| Decision | Subject | Status |
|---|---|---|
| D01 | Primary Boundary | APPROVED |
| D02 | Core Business Abstraction | APPROVED |
| D03 | Work Model | APPROVED |
| D04 | Task versus Execution | APPROVED |
| D05 | Actor Model | APPROVED |
| D06 | Decision and Business Operation Semantics | APPROVED — CLOSED |
| D07 | State Semantics | IN WORKSHOP |
| D08 | Aggregate Strategy | APPROVED |
| D09 | Relationship Model | OPEN |
| D10 | Deletion and Supersession | OPEN |

---

## 3. D01 — Primary Boundary

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

> Workspace is the primary ownership, authorization, governance, and isolation boundary for workspace-scoped business-state objects in Bizzi.
>
> Every workspace-scoped business object belongs to exactly one Workspace.
>
> Enterprise may group multiple Workspaces but is not required as the MVP operational boundary.
>
> Tenant is reserved for infrastructure and deployment concerns and must not replace Workspace in the domain vocabulary.

### Binding consequences

1. Workspace identity is immutable for ordinary aggregate updates.
2. Cross-workspace access requires an explicit governed contract.
3. Decisions, Business Operations, Work Items, runtime, evidence, events, memory, and audit remain Workspace-scoped unless explicitly platform-global.
4. Detailed membership and authorization semantics remain assigned to ADW-02 and ADW-03.

---

## 4. D02 — Core Business Abstraction

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

> Enterprise Object is the stable platform abstraction for a durable, workspace-owned, business-relevant thing with identity, lifecycle, ownership, relationships, state, and governance requirements.
>
> Enterprise Object defines a shared minimum contract but does not replace specialized domain entities, aggregates, schemas, or invariants.
>
> A universal unvalidated JSON Enterprise Object model is prohibited as the authoritative domain representation.

### Binding consequences

1. Concrete types retain explicit typed contracts and invariants.
2. Enterprise Object does not imply one table, ORM hierarchy, or generic aggregate.
3. Other domain concepts reference Enterprise Objects through stable typed references.

---

## 5. D03 — Work Model

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

> Work Item is the abstract representation of governed business work.
>
> Task, Case, and Project are specialized Work Item types that share a common coordination contract while retaining their own lifecycle rules and invariants.

### Binding consequences

1. Common orchestration may operate through the Work Item contract.
2. Specialized lifecycle behavior must not be hidden inside unvalidated generic fields.
3. Work Items reference Enterprise Objects and other Work Items through explicit relationships.

---

## 6. D04 — Task versus Execution

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

> Task represents governed business work and owns its business lifecycle, assignment, objective, completion criteria, and accepted outcome.
>
> Runtime Session represents one governed execution context or attempt.
>
> Task and Runtime Session are separate aggregates with independent identity and lifecycle state.
>
> Runtime Session state is never the authoritative source of Task state.

### Binding consequences

1. One Task may have zero, one, or multiple Runtime Sessions.
2. Technical execution success does not automatically complete a Task.
3. Retry, fallback, timeout, tool error, and human intervention belong to runtime semantics rather than Task truth.

---

## 7. D05 — Actor Model

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

> Actor is the stable identity of a human, agent, service, or external participant capable of initiating, performing, approving, observing, or being accountable for governed actions in Bizzi.
>
> Actor is distinct from User Account, Role, Agent Definition, credential, and Runtime Session.
>
> Every governed action identifies the effective Actor and, where different, the initiating, delegating, approving, and technical Actors.

### Binding consequences

1. Roles and capabilities are contextual to Workspace and scope.
2. Delegation is explicit, limited, revocable, and auditable.
3. Shared generic system identities are prohibited for authoritative business actions.
4. Historical attribution survives suspension, retirement, revocation, or compromise.

---

## 8. D06 — Decision and Business Operation Semantics

**Status:** `APPROVED — CLOSED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21  
**Closure date:** 2026-07-21  
**Decision class:** Class A — Constitutional

### Decision

> Decision and Business Operation are separate, first-class Workspace-scoped domain concepts within Bizzi.
>
> Decision is the stable and auditable representation of a governed determination about what should or should not occur within an explicit subject, context, authority, and set of conditions.
>
> Business Operation is the stable and traceable representation of a significant governed business action from intent and authorization through execution, validation, outcome evaluation, and closure.
>
> Decision defines an authoritative determination. Business Operation coordinates the realization of an intent or Decision. Work Item organizes required work. Runtime Session represents an execution attempt. Action records what was performed. Result records what execution produced. State Transition modifies authoritative aggregate state after domain validation. Domain Event records a significant fact that occurred.
>
> Business Operation is distinct from Decision, Work Item, Workflow, Runtime Session, Action, Result, State Transition, and Domain Event.
>
> One Decision may govern zero, one, or multiple Business Operations. One Business Operation may depend on multiple Decisions.
>
> Business Operation may coordinate multiple Work Items, Runtime Sessions, Actions, Results, Actors, Decisions, Evidence items, and Enterprise Objects through stable typed references.
>
> Business Operation is not a universal aggregate that owns referenced domain objects. Each aggregate retains authority over its own invariants and lifecycle state.
>
> Business Operation completion is determined by validated business outcomes and explicit completion criteria, not solely by technical execution success.
>
> Operational status, execution status, result-validation status, and business-outcome status remain semantically distinct.
>
> Failed, partial, cancelled, suspended, reversed, compensated, and unknown outcomes are represented explicitly.
>
> Compensation or reversal is a new governed Business Operation linked to the original and does not erase or rewrite history.
>
> Concrete Business Operation types retain explicit schemas, lifecycle rules, authority requirements, and invariants. A universal unvalidated JSON operation model is prohibited as the authoritative domain representation.

### Consequences

1. `Decision + Business Operation` is the primary domain construction of Bizzi.
2. Decision is the governance center; Business Operation is the operational center.
3. Work Item is a work-coordination abstraction, not the end-to-end owner of business execution.
4. Runtime Session is an execution attempt, not the source of Business Operation or business-object truth.
5. Technical success does not imply business success.
6. Only the owning aggregate or authorized domain process may commit authoritative state.
7. AI recommendations are not authoritative Decisions without explicit authority or scoped delegation.
8. Detailed state semantics are assigned to D07.
9. Detailed typed relationships are assigned to D09.
10. Detailed cancellation, supersession, reversal, compensation, archival, and deletion rules are assigned to D10.
11. Detailed authority evaluation remains assigned to ADW-03.
12. Detailed runtime and tool semantics remain assigned to ADW-05.
13. Detailed event, audit, and provenance mechanics remain assigned to ADW-07.

### Closure record

D06 is officially closed because its terminology, ownership boundaries, primary construction, consequences, and downstream decision routing are synchronized across:

- `DOMAIN_FOUNDATION.md`;
- `ADW_01_CORE_DOMAIN_SEMANTICS.md`;
- this Decision Register;
- `ARCHITECTURE_SPECIFICATION.md`.

### Supersession rule

D06 may be changed only by an explicit Class A architecture decision defining semantic compatibility, operation and decision history preservation, authority migration, aggregate-state impact, execution traceability, outcome migration, compensation behavior, event compatibility, and idempotency consequences.

---

## 9. D07 — State Semantics

**Status:** `IN WORKSHOP`  
**Opened by:** Project Owner  
**Opening date:** 2026-07-21  
**Decision class:** Class A — Constitutional

### Problem

Bizzi distinguishes Decision, Business Operation, Work Item, Runtime Session, Action, Result, State Transition, Domain Event, and Enterprise Object. Their states must not collapse into one generic status model.

### Governing question

> How does Bizzi represent, own, validate, transition, observe, and reconstruct authoritative and derived state without allowing runtime, workflow, events, projections, or AI outputs to become an accidental source of truth?

### Preliminary invariants

1. Every authoritative state belongs to exactly one owning aggregate or explicitly defined domain authority.
2. Only the owner or authorized domain process may commit a State Transition.
3. Command requests change; Result reports output; neither proves authoritative mutation.
4. Validation determines whether a Result may support a State Transition.
5. Domain Event records a committed significant fact and is not an independent mutation authority.
6. Projection and read-model state is derived, rebuildable, versioned, and potentially stale.
7. Runtime Session state is not authoritative Work Item, Business Operation, Decision, or Enterprise Object state.
8. Technical success does not imply accepted result, completed work, successful operation, or achieved business outcome.
9. Competing transitions require optimistic concurrency or an equivalent protection.
10. Transition history remains attributable and auditable.
11. Cross-aggregate consistency requires explicit coordination; hidden distributed mutation is prohibited.
12. A universal state machine for all domain types is prohibited.

### Candidate decision direction

- aggregate-owned authoritative state;
- explicit transition requests and validated transition commits;
- separate `phase`, `status`, `outcome`, `health`, and `progress` semantics;
- append-oriented history for significant transitions;
- projections carrying source version and observation time;
- atomic aggregate mutation with the required audit/outbox intent inside the selected consistency boundary;
- shared normalized phases only where they do not replace specialized lifecycles.

### Open D07 questions

1. Is State Transition always a first-class record, or may it be aggregate-owned transition history for low-risk types?
2. What exact meanings are assigned to `phase`, `status`, `outcome`, `health`, and `progress`?
3. Which normalized phases may be shared across Decision, Business Operation, Work Item, and Runtime Session?
4. Which transitions require a Decision or approval versus policy authority?
5. What consistency boundary governs aggregate mutation, audit, and event publication?
6. How are idempotency, expected version, retries, and duplicate requests handled?
7. How are partial, suspended, expired, failed, cancelled, compensated, and unknown states represented?
8. How are stale projections identified and corrected?
9. How is truth reconciled when snapshot, event, audit, and external-system observations disagree?
10. Which matters are deferred to D10, ADW-05, ADW-07, and ADW-08?

D07 is not approved in this revision.

---

## 10. D08 — Aggregate Strategy

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

> Work Item is a shared domain contract and coordination abstraction, not one universal aggregate root.
>
> Task, Case, and Project are separate aggregate roots because they own materially different lifecycle rules, invariants, state, and outcomes.
>
> A shared Work Item index or read model may support search, coordination, and reporting but is not the authoritative source of specialized aggregate state.

### Binding consequences

1. Concrete Work Item aggregates retain independent boundaries and authoritative state.
2. Cross-Work-Item relationships use stable typed references.
3. Shared contracts do not require ORM inheritance, one database table, or one persistence schema.
4. New Work Item types may implement the common contract without modifying existing aggregates.

---

## 11. Remaining Decisions

### D09 — Relationship Model

Must define typed relationships among Decision, Business Operation, Work Item, Enterprise Object, Actor, Runtime Session, Action, Result, Evidence, State Transition, and Domain Event.

### D10 — Deletion and Supersession

Must define cancellation, expiration, revocation, supersession, reversal, compensation, archival, deletion, retention, and historical-preservation semantics.

---

## 12. Architecture Stabilization Record

**Date:** 2026-07-21  
**Authority:** Project Owner

The stabilization:

1. retired `Domain Core` from the active vocabulary;
2. established `Core Domain Semantics` as the sole ADW-01 name;
3. established `DOMAIN_FOUNDATION.md` as the constitutional semantic baseline;
4. established `ADW_01_CORE_DOMAIN_SEMANTICS.md` as the sole ADW-01 workshop chapter;
5. retained this file as the authoritative workshop decision log;
6. synchronized and officially closed D06;
7. opened D07 — State Semantics;
8. removed `DOMAIN_CORE.md` as a competing source of truth.

---

## 13. Workshop Progress

```text
D01: APPROVED
D02: APPROVED
D03: APPROVED
D04: APPROVED
D05: APPROVED
D06: APPROVED — CLOSED
D07: IN WORKSHOP
D08: APPROVED
D09: OPEN
D10: OPEN
ADW-01: IN PROGRESS
```
