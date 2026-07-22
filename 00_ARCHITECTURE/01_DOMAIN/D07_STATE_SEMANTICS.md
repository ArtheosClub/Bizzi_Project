# D07 — State Semantics

**Subtitle:** The Bizzi State Constitution  
**Document ID:** ARCH-DOMAIN-D07  
**Version:** 1.0  
**Status:** APPROVED — CLOSED  
**Decision class:** Class A — Constitutional  
**Workshop:** ADW-01 — Core Domain Semantics  
**Owner:** Project Owner  
**Decision authority:** Project Owner  
**Opened:** 2026-07-21  
**Approved:** 2026-07-22  
**Closed:** 2026-07-22  
**Last updated:** 2026-07-22

---

## 1. Purpose

D07 defines the semantic constitution of state in Bizzi.

It establishes what may be treated as authoritative business truth, which domain authority owns that truth, how change is requested and validated, how a transition becomes committed, and how authoritative state is distinguished from runtime state, workflow state, projections, events, reports, analytics, caches, and AI-generated interpretations.

D07 is implementation-independent. It does not prescribe a programming language, database engine, event broker, persistence pattern, workflow engine, user-interface technology, or state-machine library.

---

## 2. Governing Question

> How does Bizzi define, own, validate, transition, observe, reconstruct, and preserve authoritative business state without allowing runtime, workflow, events, projections, or AI outputs to become an accidental source of truth?

---

## 3. Approved Constitutional Position

1. Authoritative state belongs to exactly one owning aggregate or explicitly defined domain authority.
2. Execution, workflow, events, projections, reports, caches, analytics, and AI outputs do not own business truth.
3. State Transition is an aggregate-owned, validated, and committed change from one authoritative state version to another.
4. Significant transitions additionally produce durable immutable transition records.
5. Phase, Status, Outcome, Progress, and Health are separate semantic dimensions.
6. Authority to request, approve, validate, and commit change are distinct powers.
7. Competing mutations require expected-version or equivalent conflict protection.
8. Repeated requests must produce at most one authoritative business effect.
9. Aggregate mutation and durable audit/publication intent share an explicit consistency boundary.
10. Domain Events record committed significant facts; they do not independently own or mutate authoritative state.
11. Projections are derived, rebuildable, version-aware, and may be stale.
12. Reconstruction follows authoritative ownership and committed history rather than visibility, event order, or AI interpretation.

---

## 4. Foundational Definitions

### 4.1 State

State is the current semantically meaningful condition of a subject at an identified version and effective time.

### 4.2 Authoritative State

Authoritative State is the state that the owning aggregate or explicitly defined domain authority recognizes as the current business truth for its subject.

Only authoritative state may govern subsequent domain decisions and invariant enforcement.

### 4.3 Derived State

Derived State is an observation, calculation, projection, index, cache, summary, interpretation, or representation produced from authoritative sources.

Derived State may be stale, incomplete, delayed, or temporarily inconsistent. It must never silently replace the authoritative source from which it was derived.

### 4.4 State Transition

A State Transition is an aggregate-owned, validated, and committed change from one authoritative state version to another.

A transition is not equivalent to a command, request, result, event, workflow step, runtime completion, or database write.

### 4.5 Transition Request

A Transition Request expresses an intention to change state. It does not prove that change occurred.

### 4.6 Transition Commit

A Transition Commit is the domain-authorized acceptance and durable recording of a valid transition by the owning aggregate or explicitly authorized domain process.

### 4.7 Significant Transition

A Significant Transition is a committed transition whose business, legal, financial, operational, compliance, security, or audit importance requires a durable immutable transition record in addition to the aggregate's current state.

---

## 5. State Domains

Bizzi distinguishes at least the following state domains:

```text
Authoritative Enterprise Object State
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

These state domains may correlate, but they remain semantically separate.

A transition in one domain does not automatically determine a transition in another domain unless an explicit domain rule authorizes that dependency.

---

## 6. State Dimensions

### 6.1 Phase

Answers: **Where is the subject in its governed lifecycle?**

### 6.2 Status

Answers: **What is happening now within the current lifecycle context?**

### 6.3 Outcome

Answers: **What business result was authoritatively determined?**

### 6.4 Progress

Answers: **How much of the planned work has been completed or accepted?**

### 6.5 Health

Answers: **How healthy, degraded, risky, or uncertain is current execution or observation?**

These dimensions are orthogonal. No aggregate, workflow, projection, interface, or integration may collapse them into one universal authoritative `status` field.

Terminal and non-terminal semantics must remain explicit. Unknown, pending, suspended, blocked, expired, cancelled, failed, rejected, partial, compensated, and completed conditions must not be silently conflated.

---

## 7. State Ownership

Every authoritative state has exactly one owning aggregate or explicitly defined domain authority.

| Subject | State owner |
|---|---|
| Enterprise Object | Specialized Enterprise Object aggregate |
| Decision | Decision aggregate |
| Business Operation | Business Operation aggregate |
| Work Item | Specialized Work Item aggregate |
| Runtime Session | Runtime Session aggregate |
| Result validation | Validating domain authority |
| Business Outcome | Business Operation or specialized outcome authority |
| Projection | Projection subsystem; derived only |
| Event delivery | Messaging infrastructure; technical only |

Business Operation may coordinate changes across multiple aggregates, but it does not absorb or silently own their authoritative state.

---

## 8. Transition Authority and Validation

A valid transition requires:

1. resolved subject and owner;
2. attributable requested and effective Actors;
3. an explicit authority basis;
4. expected-version or equivalent concurrency protection where required;
5. domain invariant validation;
6. required Result and Evidence validation;
7. an explicit transition decision;
8. durable commitment of the new state version.

Authority may arise from an explicit Decision, approval, standing policy, delegated authority, or another approved domain basis. Delegation must remain scoped, attributable, revocable, and auditable.

A rejected transition request does not mutate authoritative state.

---

## 9. Concurrency and Idempotency

1. Competing mutations use optimistic concurrency or an equivalent protection.
2. A stale expected version produces an explicit conflict outcome rather than a silent overwrite.
3. Retries must not create duplicate authoritative business effects.
4. Idempotency scope must identify the authority context, subject, requested effect, and applicable time or operation boundary.
5. An unknown technical response after commit must be resolved through state and idempotency lookup rather than blind re-execution.
6. Merge is allowed only when the owning domain authority defines deterministic merge semantics.

---

## 10. Consistency and Publication

The aggregate state mutation and durable intent for required audit and publication effects must share an explicit consistency boundary.

The approved semantic order is:

```text
Transition Request
  -> Authority and Ownership Resolution
  -> Expected-Version Check
  -> Domain and Evidence Validation
  -> Transition Decision
  -> Atomic Commit of New State Version
  -> Durable Audit / Outbox Intent
  -> Domain Event Publication
  -> Projection Update
  -> Business Outcome Re-evaluation, when applicable
```

Publication failure after commit is a technical recovery condition, not a rollback of authoritative business truth.

Cross-aggregate consistency requires explicit domain or application coordination. Hidden distributed mutation is prohibited.

---

## 11. Reconstruction and Recovery

When sources disagree, the authoritative reconstruction order is:

```text
Owning aggregate state
  -> Significant transition history
  -> Audit and publication intent
  -> Domain Events
  -> Projections
  -> Reports, caches, analytics, and AI interpretations
```

Recovery mechanisms may include replay, rehydrate, reconcile, repair, and rebuild. They must preserve attribution, causation, authority basis, version history, and historical integrity.

A projection may be rebuilt. Authoritative history must not be rewritten merely to make a projection appear consistent.

---

## 12. Constitutional Laws

### LAW-D07-01 — Business Truth Ownership
Business truth is owned by the business domain.

### LAW-D07-02 — Single Authoritative Owner
Every authoritative state has exactly one owning aggregate or explicitly defined domain authority.

### LAW-D07-03 — Execution Separation
Execution never owns authoritative business truth merely because it performed work or completed successfully.

### LAW-D07-04 — Governed Mutation
Only the owning aggregate or an explicitly authorized domain process may commit a transition of authoritative state.

### LAW-D07-05 — Validation Before Commit
A transition must be validated against authority, invariants, expected version, and required evidence before commitment.

### LAW-D07-06 — Request Is Not Fact
A Command or Transition Request asks for change; it does not prove that change occurred.

### LAW-D07-07 — Result Is Not Mutation
A Result reports execution output. It does not independently mutate authoritative state.

### LAW-D07-08 — Event Is Not Authority
A Domain Event records a significant committed fact. It is not a command, transition authority, or independent source of business truth.

### LAW-D07-09 — Derived State Is Replaceable
Projection, cache, index, dashboard, report, analytic model, and search representation are derived and must be rebuildable or replaceable from authoritative sources.

### LAW-D07-10 — AI Is Advisory
AI may observe, classify, recommend, predict, explain, or propose. AI output becomes authoritative only through an explicitly governed domain decision or transition process.

### LAW-D07-11 — Technical Success Is Not Business Success
Technical execution success does not automatically imply accepted Result, completed Work Item, successful Business Operation, or achieved Business Outcome.

### LAW-D07-12 — Versioned Change
Competing changes to authoritative state require an expected version or equivalent concurrency control.

### LAW-D07-13 — Historical Integrity
Committed significant transitions must remain attributable, versioned, auditable, and historically preserved.

### LAW-D07-14 — No Hidden Distributed Mutation
Cross-aggregate consistency must use explicit domain or application coordination. Hidden distributed mutation is prohibited.

### LAW-D07-15 — Orthogonal State Dimensions
Phase, Status, Outcome, Progress, and Health are separate semantic dimensions and must not be collapsed into one universal state field.

### LAW-D07-16 — Idempotent Business Effect
Repeated delivery or retry of the same transition request must produce at most one authoritative business effect.

### LAW-D07-17 — Explicit Consistency Boundary
Aggregate mutation and required durable audit/publication intent must use an explicitly defined consistency boundary.

### LAW-D07-18 — Authoritative Reconstruction Order
Recovery and reconstruction must prefer owning aggregate state and committed transition history over events, projections, reports, caches, analytics, or AI interpretations.

---

## 13. Approved Decisions

### D07.1 — Nature of State Transition
**Status:** APPROVED

State Transition is an aggregate-owned validated change of authoritative state. Significant transitions additionally produce an immutable first-class transition record. Low-risk transitions may remain represented through aggregate-owned history when required attribution, versioning, causation, authority basis, and audit information are preserved.

### D07.2 — State Dimensions
**Status:** APPROVED

Phase, Status, Outcome, Progress, and Health are separate semantic dimensions with independent meaning and transition rules.

### D07.3 — Validation and Authority
**Status:** APPROVED

Authority to request, approve, validate, and commit change are distinct powers. Every committed transition requires an explicit authority basis and validation outcome.

### D07.4 — Concurrency and Idempotency
**Status:** APPROVED

Competing changes require expected-version or equivalent conflict protection. Repeated requests produce at most one authoritative business effect.

### D07.5 — Consistency and Publication
**Status:** APPROVED

Aggregate mutation and durable audit/publication intent share an explicit consistency boundary. Publication and projection are downstream consequences of commit.

### D07.6 — Reconstruction and Recovery
**Status:** APPROVED

Authoritative reconstruction follows the owning aggregate and committed transition history. Derived state is rebuilt or reconciled without rewriting authoritative history.

### D07.7 — Constitutional Review and Closure
**Status:** APPROVED — CLOSED

Project Owner approved D07 on 2026-07-22. All D07 constitutional decisions are binding for downstream architecture work.

---

## 14. Deferred Responsibilities

- D09 defines typed relationships among state-bearing concepts and transition records.
- D10 defines deletion, archival, supersession, revocation, reversal, compensation, and retention semantics.
- ADW-03 defines detailed authorization and policy evaluation.
- ADW-05 defines runtime-specific execution states and retry mechanics.
- ADW-07 defines detailed audit, provenance, and event contracts.
- ADW-08 defines physical persistence, transactions, outbox, indexing, and recovery mechanics.

---

## 15. Closure Record

D07 is officially closed because:

1. authoritative and derived state are explicitly separated;
2. state ownership is explicit;
3. State Transition semantics are defined;
4. state dimensions are separated;
5. authority and validation rules are established;
6. concurrency and idempotency semantics are established;
7. consistency and publication semantics are established;
8. reconstruction and recovery order is established;
9. downstream responsibilities are routed without semantic gaps;
10. Project Owner explicitly approved D07.

```text
D07.1 Nature of State Transition: APPROVED
D07.2 State Dimensions: APPROVED
D07.3 Validation and Authority: APPROVED
D07.4 Concurrency and Idempotency: APPROVED
D07.5 Consistency and Publication: APPROVED
D07.6 Reconstruction and Recovery: APPROVED
D07.7 Constitutional Review and Closure: APPROVED — CLOSED

D07 overall status: APPROVED — CLOSED
```
