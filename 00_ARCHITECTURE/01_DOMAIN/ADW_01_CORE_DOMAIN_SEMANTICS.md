# ADW-01 — Core Domain Semantics

**Document ID:** ARCH-DOMAIN-001  
**Version:** 0.2-draft  
**Status:** Workshop in progress — D07 active  
**Architecture Gate:** Gate C v1.1  
**Owner:** Project Owner  
**Decision authority:** Project Owner  
**Foundation:** `00_ARCHITECTURE/00_FOUNDATION/DOMAIN_FOUNDATION.md`  
**Decision register:** `00_ARCHITECTURE/01_DOMAIN/ADW_01_DECISION_REGISTER.md`

---

## 1. Purpose

ADW-01 defines the stable semantic foundation required for Bizzi to represent, govern, coordinate, execute, and evaluate enterprise activity.

The workshop is concerned with domain meaning rather than implementation structure. Its conclusions remain valid independently of programming language, application framework, database, AI provider, interface, infrastructure, or deployment topology.

`Core Domain Semantics` is the sole approved name of ADW-01. The former term `Domain Core` is retired from the active architecture vocabulary.

---

## 2. Governing Question

> What are the smallest stable concepts, ownership rules, state semantics, and relationships required to describe how an enterprise operates in Bizzi?

---

## 3. Foundation Model

Workspace is the primary ownership, authorization, governance, and isolation boundary.

Within a Workspace, Bizzi recognizes five fundamental domain concepts:

```text
Workspace
  ├── Enterprise Object
  ├── Actor
  ├── Work Item
  ├── Decision
  └── Business Operation
```

| Concept | Governing question |
|---|---|
| Enterprise Object | What does the enterprise manage? |
| Actor | Who participates or acts? |
| Work Item | What work must be organized? |
| Decision | What has been authoritatively determined? |
| Business Operation | How is an authorized intent or Decision realized? |

No concept replaces another.

---

## 4. Primary Construction

ADW-01 adopts the following primary domain construction:

```text
Decision
+
Business Operation
```

Decision is the governance center of enterprise activity.

Business Operation is the operational center of enterprise activity.

Work Items organize work required by operations. Runtime Sessions represent execution contexts or attempts. Actions record what was performed. Results record what execution produced. Domain aggregates validate and own authoritative state. Domain Events record significant facts that occurred.

---

## 5. Enterprise Behaviour Chain

```text
Intent
  -> Decision
  -> Authorization
  -> Business Operation
  -> Execution Plan
  -> Work Items and Runtime Sessions
  -> Actions
  -> Results
  -> Domain Validation
  -> State Transition
  -> Domain Event
  -> Business Outcome Evaluation
```

This chain is semantic rather than a mandatory synchronous workflow. Low-risk or policy-authorized activity may omit a separately persisted Decision, but no governed action may lack an auditable authority basis.

---

## 6. Decision Status

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

## 7. Approved Decisions Summary

### D01 — Primary Boundary

Workspace is the primary ownership, authorization, and isolation boundary for workspace-scoped business state.

### D02 — Core Business Abstraction

Enterprise Object is the shared platform abstraction for durable business-relevant things while specialized types retain explicit contracts and invariants.

### D03 — Work Model

Work Item is the shared representation of governed business work. Task, Case, and Project are specialized Work Item types.

### D04 — Task versus Execution

Task and Runtime Session are separate aggregates. A successful Runtime Session does not automatically complete a Task.

### D05 — Actor Model

Actor is the stable operational identity of a human, agent, service, or external participant. Actor is distinct from User Account, Role, Agent Definition, and Runtime Session.

### D06 — Decision and Business Operation Semantics

**Status:** `APPROVED — CLOSED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21  
**Closure date:** 2026-07-21

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
> Business Operation is not a universal aggregate that owns referenced domain objects. Each aggregate retains authority over its own invariants and lifecycle state.
>
> Business Operation completion is determined by validated business outcomes and explicit completion criteria, not solely by technical execution success.
>
> Compensation or reversal is represented as a new governed Business Operation linked to the original operation and does not erase or rewrite history.

#### D06 closure conditions satisfied

1. `Decision + Business Operation` is recorded in the Domain Foundation.
2. Decision and Business Operation are separately defined and separately owned.
3. Their relationship to Work Item, Runtime Session, Action, Result, State Transition, and Domain Event is explicit.
4. Technical success is separated from business success.
5. History, reversal, and compensation principles are preserved.
6. Later details are explicitly routed to D07, D09, D10, ADW-03, ADW-05, and ADW-07.
7. The Decision Register and root Architecture Specification are synchronized.

### D08 — Aggregate Strategy

Work Item is a shared domain contract and coordination abstraction, not one universal aggregate root. Task, Case, and Project are separate aggregate roots.

---

## 8. D07 — State Semantics

**Status:** `IN WORKSHOP`  
**Opened by:** Project Owner  
**Opening date:** 2026-07-21  
**Decision class:** Class A — Constitutional

### 8.1 Problem

Bizzi now distinguishes Decision, Business Operation, Work Item, Runtime Session, Action, Result, State Transition, and Domain Event. The architecture must define which state is authoritative, who owns it, how transitions are validated, and how derived state differs from domain truth.

Without D07, runtime success, operation progress, work completion, projections, and business-object state may be incorrectly collapsed into one status model.

### 8.2 Governing question

> How does Bizzi represent, own, validate, transition, observe, and reconstruct authoritative and derived state without allowing runtime, workflow, events, projections, or AI outputs to become an accidental source of truth?

### 8.3 State domains to distinguish

```text
Authoritative Business Object State
Decision State
Business Operation State
Work Item State
Runtime Session State
Action / Tool Invocation State
Result Validation State
Business Outcome State
Projection / Read Model State
Event Delivery State
```

These state domains may correlate, but no state transition in one domain automatically determines a transition in another unless an explicit domain rule authorizes it.

### 8.4 Preliminary invariants

1. Every authoritative state belongs to exactly one owning aggregate or explicitly defined domain authority.
2. Only the owner or an authorized domain process may commit a state transition.
3. A Command requests change; it does not prove change occurred.
4. A Result reports output; it does not itself mutate authoritative state.
5. Validation determines whether a Result may support a State Transition.
6. A Domain Event records a committed significant fact; it is not a command or independent authority basis.
7. A Projection, index, cache, search model, dashboard, or report is derived and rebuildable.
8. Runtime Session state is not authoritative Work Item, Business Operation, Decision, or Enterprise Object state.
9. Technical success does not imply accepted result, completed work, successful operation, or achieved business outcome.
10. Transitions require an expected version or equivalent concurrency protection where competing changes are possible.
11. Transition history and superseded state must remain auditable.
12. Cross-aggregate consistency must use explicit application or domain coordination; hidden distributed mutation is prohibited.

### 8.5 Candidate transition contract

```text
StateTransition {
  transition_id
  workspace_id
  subject_reference
  subject_type
  from_state
  to_state
  requested_by_actor
  effective_actor
  authority_basis
  reason
  command_reference
  decision_references
  operation_reference
  result_references
  evidence_references
  expected_version
  committed_version
  validation_outcome
  committed_at
  correlation_id
  causation_id
  idempotency_key
}
```

This is a semantic contract, not a mandatory universal persistence table.

### 8.6 Questions D07 must resolve

1. Is `State Transition` a first-class domain record, an aggregate-owned value, or both depending on risk and type?
2. What normalized top-level phases may be shared across Decision, Business Operation, Work Item, and Runtime Session without flattening specialized lifecycles?
3. How are `status`, `phase`, `outcome`, `health`, and `progress` distinguished?
4. Which transitions require Decision or approval, and which may follow policy authority?
5. What consistency boundary governs aggregate state, audit, and event publication?
6. How are optimistic concurrency, idempotency, retries, and duplicate transition requests handled?
7. How are partial, suspended, expired, failed, cancelled, compensated, and unknown states represented?
8. When may derived state be stale, and how is staleness made explicit?
9. How is state reconstructed when events, audit, and current snapshots disagree?
10. Which details belong to D10, ADW-05, ADW-07, and ADW-08 rather than D07?

### 8.7 Recommended direction for workshop consideration

- Aggregate-owned authoritative state.
- Explicit transition requests and validated transition commits.
- Separate `phase`, `status`, `outcome`, and `progress` semantics.
- Append-oriented transition history for significant transitions.
- Derived projections marked with source version and observation time.
- Atomic persistence of aggregate mutation and outbox/audit intent within the selected consistency boundary.
- No universal state machine for all domain types; shared normalized phases may coexist with specialized lifecycles.

D07 is not yet approved. The next workshop step is to decide the authoritative-state model and the distinction between `phase`, `status`, `outcome`, and `progress`.

---

## 9. Domain Ownership Rules

- Enterprise Object owns specialized business state and invariants.
- Actor owns operational identity and historical attribution.
- Work Item owns work-coordination lifecycle and accepted work outcome.
- Decision owns authoritative determination, authority basis, conditions, status, and supersession history.
- Business Operation owns operational objective, coordination history, execution trace, validation progress, completion criteria, and business outcome.
- Runtime Session owns execution-attempt state and technical execution history.
- Domain Event records a fact and is not the source of authoritative operational state.
- Projection represents derived observation and is never the silent owner of domain truth.

Business Operation coordinates but does not absorb foreign aggregates.

---

## 10. Remaining Decisions

D09 must define typed relationships among Decision, Business Operation, Work Item, Enterprise Object, Actor, Runtime Session, Result, Evidence, State Transition, and Domain Event.

D10 must preserve Decision and Business Operation history and define explicit cancellation, expiration, revocation, supersession, reversal, compensation, archival, and deletion semantics.

---

## 11. Workshop Completion Criteria

ADW-01 is complete when:

1. D01 through D10 have explicit Project Owner decisions;
2. the Decision Register is synchronized with this chapter;
3. the root Architecture Specification references the final semantic model;
4. the domain vocabulary contains no unresolved collisions;
5. aggregate ownership and typed relationship rules are explicit;
6. state, deletion, supersession, reversal, and compensation semantics are resolved;
7. follow-up responsibilities are assigned to later ADWs without semantic gaps.

---

## 12. Architecture Stabilization Record

The 2026-07-21 stabilization performed the following actions:

- retired the active term `Domain Core`;
- established `Core Domain Semantics` as the sole ADW-01 vocabulary;
- designated `DOMAIN_FOUNDATION.md` as the constitutional semantic baseline;
- designated this document as the sole ADW-01 workshop chapter;
- designated `ADW_01_DECISION_REGISTER.md` as the authoritative workshop decision log;
- closed D06 after synchronized recording;
- opened D07 — State Semantics;
- removed the competing `DOMAIN_CORE.md` document.

---

## 13. Current Progress

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
