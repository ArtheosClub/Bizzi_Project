# ADW-01 — Core Domain Semantics

**Document ID:** ARCH-DOMAIN-001  
**Version:** 0.1-draft  
**Status:** Workshop in progress  
**Architecture Gate:** Gate C v1.1  
**Owner:** Project Owner  
**Decision authority:** Project Owner  
**Foundation:** `00_ARCHITECTURE/00_FOUNDATION/DOMAIN_FOUNDATION.md`  
**Decision register:** `00_ARCHITECTURE/01_DOMAIN/ADW_01_DECISION_REGISTER.md`

---

## 1. Purpose

ADW-01 defines the stable semantic foundation required for Bizzi to represent, govern, coordinate, execute, and evaluate enterprise activity.

The workshop is concerned with domain meaning rather than implementation structure. Its conclusions must remain valid independently of programming language, application framework, database, AI provider, interface, infrastructure, or deployment topology.

---

## 2. Governing Question

> What are the smallest stable concepts and ownership rules required to describe how an enterprise operates in Bizzi?

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

They answer different questions:

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

Work Items organize work required by operations. Runtime Sessions represent execution contexts or attempts. Actions record performed operations. Results record produced outputs. Domain aggregates validate and own authoritative state. Domain Events record significant facts that have occurred.

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

## 6. Approved Decisions

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

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

> Decision and Business Operation are separate, first-class domain concepts within Bizzi.
>
> Decision is the stable and auditable representation of a governed determination about what should or should not occur within an explicit Workspace, subject, context, authority, and set of conditions.
>
> Business Operation is the stable and traceable representation of a significant governed business action from intent and authorization through execution, validation, outcome evaluation, and closure.
>
> Decision defines an authoritative determination. Business Operation coordinates the realization of an intent or Decision. Work Item organizes required work. Runtime Session represents an execution attempt. Action records what was performed. Result records what execution produced. State Transition modifies authoritative aggregate state after domain validation. Domain Event records a significant fact that has occurred.
>
> Business Operation is distinct from Decision, Work Item, Workflow, Runtime Session, Action, Result, and Domain Event.
>
> One Decision may govern zero, one, or multiple Business Operations. One Business Operation may depend on multiple Decisions.
>
> Business Operation is not a universal aggregate that owns referenced domain objects. Each aggregate retains authority over its own invariants and lifecycle state.
>
> Business Operation completion is determined by validated business outcomes and explicit completion criteria, not solely by technical execution success.
>
> Compensation or reversal is represented as a new governed Business Operation linked to the original operation and does not erase or rewrite history.

#### D06 consequences

1. Decision and Business Operation become separate first-class Workspace-scoped domain concepts.
2. Decision state, execution state, operational state, and business outcome state remain semantically distinct.
3. Business Operation may coordinate multiple Work Items, Runtime Sessions, Actions, Results, Actors, Decisions, Evidence items, and Enterprise Objects through stable typed references.
4. Technical success does not automatically establish business success.
5. Only the owning aggregate or authorized domain process may commit authoritative state.
6. AI recommendations are not authoritative Decisions unless accepted by an authorized Actor or permitted by explicit scoped delegation.
7. Failed, partial, cancelled, suspended, reversed, compensated, and unknown outcomes must remain distinguishable.
8. Concrete Business Operation types retain specialized schemas, lifecycle rules, authority requirements, and invariants.
9. A universal unvalidated JSON operation model is prohibited as the authoritative domain representation.
10. Detailed authority evaluation remains assigned to ADW-03; detailed runtime and tool semantics remain assigned to ADW-05; detailed operational lifecycle normalization remains coordinated with D07.

### D08 — Aggregate Strategy

Work Item is a shared domain contract and coordination abstraction, not one universal aggregate root. Task, Case, and Project are separate aggregate roots.

---

## 7. Pending Decisions

| Decision | Subject | Status |
|---|---|---|
| D07 | Operational State | PENDING |
| D09 | Relationship Model | OPEN |
| D10 | Deletion and Supersession | OPEN |

D09 must now include typed relationships among Decision, Business Operation, Work Item, Enterprise Object, Actor, Runtime Session, Result, Evidence, and Domain Event.

D10 must preserve Decision and Business Operation history and define explicit cancellation, expiration, revocation, supersession, reversal, and compensation semantics.

---

## 8. Domain Ownership Rules

- Enterprise Object owns specialized business state and invariants.
- Actor owns operational identity and historical attribution.
- Work Item owns work-coordination lifecycle and accepted work outcome.
- Decision owns authoritative determination, authority basis, conditions, status, and supersession history.
- Business Operation owns operational objective, coordination history, execution trace, validation progress, completion criteria, and business outcome.
- Runtime Session owns execution-attempt state and technical execution history.
- Domain Event records a fact and is not the source of authoritative operational state.

Business Operation coordinates but does not absorb foreign aggregates.

---

## 9. Workshop Completion Criteria

ADW-01 is complete when:

1. D01 through D10 have explicit Project Owner decisions;
2. the Decision Register is synchronized with this chapter;
3. the root Architecture Specification references the final semantic model;
4. the domain vocabulary contains no unresolved collisions;
5. aggregate ownership and typed relationship rules are explicit;
6. operational state, deletion, supersession, reversal, and compensation semantics are resolved;
7. follow-up responsibilities are assigned to later ADWs without semantic gaps.

---

## 10. Current Progress

```text
D01: APPROVED
D02: APPROVED
D03: APPROVED
D04: APPROVED
D05: APPROVED
D06: APPROVED
D07: PENDING
D08: APPROVED
D09: OPEN
D10: OPEN
ADW-01: IN PROGRESS
```
