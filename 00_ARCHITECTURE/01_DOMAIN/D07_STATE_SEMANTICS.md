# D07 — State Semantics

**Subtitle:** The Bizzi State Constitution  
**Document ID:** ARCH-DOMAIN-D07  
**Version:** 0.1-draft  
**Status:** IN WORKSHOP  
**Decision class:** Class A — Constitutional  
**Workshop:** ADW-01 — Core Domain Semantics  
**Owner:** Project Owner  
**Decision authority:** Project Owner  
**Opened:** 2026-07-21  
**Last updated:** 2026-07-21

---

## 1. Purpose

D07 defines the semantic constitution of state in Bizzi.

It establishes what may be treated as authoritative business truth, which domain authority owns that truth, how a change may be requested and validated, how a transition becomes committed, and how authoritative state is distinguished from runtime state, workflow state, projections, events, reports, analytics, caches, and AI-generated interpretations.

D07 is intentionally implementation-independent. It does not prescribe a programming language, database engine, event broker, persistence pattern, workflow engine, or user-interface technology.

---

## 2. Governing Question

> How does Bizzi define, own, validate, transition, observe, reconstruct, and preserve authoritative business state without allowing runtime, workflow, events, projections, or AI outputs to become an accidental source of truth?

---

## 3. Scope

D07 governs:

1. authoritative and derived state;
2. state ownership and authority boundaries;
3. transition requests, validation, commitment, and observation;
4. separation of phase, status, outcome, progress, and health;
5. state versioning, concurrency, and idempotency semantics;
6. significant transition history and auditability;
7. consistency between aggregate mutation, audit intent, and event publication;
8. reconstruction and conflict resolution among current state, transition history, audit records, and projections;
9. the semantic relationship between state and Decision, Business Operation, Work Item, Runtime Session, Action, Result, Domain Event, and Business Outcome.

D07 does not define:

- the complete typed relationship model, which belongs to D09;
- deletion, archival, supersession, reversal, and compensation details, which belong to D10;
- physical persistence schemas, which belong to the persistence architecture workshop;
- event transport and delivery infrastructure;
- concrete workflow notation;
- user-interface state;
- implementation-specific state-machine libraries.

---

## 4. State Philosophy

Bizzi adopts the following foundational principle:

> State belongs to the business domain, not to execution.

Execution may attempt work, produce results, fail, retry, pause, or complete technically. None of those facts automatically changes authoritative business state.

Authoritative state changes only when the owning domain authority validates the proposed change and commits a transition according to its invariants, authority basis, and consistency rules.

---

## 5. Foundational Definitions

### 5.1 State

State is the current semantically meaningful condition of a subject at an identified version and effective time.

State is not merely a stored value. It is a governed assertion whose meaning depends on:

- the subject;
- the owning authority;
- the applicable invariants;
- the version;
- the effective time;
- the evidence and authority basis supporting the assertion.

### 5.2 Authoritative State

Authoritative State is the state that the owning aggregate or explicitly defined domain authority recognizes as the current business truth for its subject.

Only authoritative state may govern subsequent domain decisions and invariant enforcement.

### 5.3 Derived State

Derived State is an observation, calculation, projection, index, cache, summary, interpretation, or representation produced from authoritative sources.

Derived State may be useful, stale, incomplete, delayed, or temporarily inconsistent. It must never silently replace the authoritative source from which it was derived.

### 5.4 State Transition

A State Transition is an aggregate-owned, validated, and committed change from one authoritative state version to another.

A transition is not equivalent to a command, request, result, event, workflow step, runtime completion, or database write.

### 5.5 Transition Request

A Transition Request expresses an intention to change state. It may contain a proposed target state, authority basis, reason, evidence, expected version, and correlation context.

A request has no authority to prove that the transition occurred.

### 5.6 Transition Commit

A Transition Commit is the domain-authorized acceptance and durable recording of a valid transition by the owning aggregate or explicitly authorized domain process.

### 5.7 Significant Transition

A Significant Transition is a committed transition whose business, legal, financial, operational, compliance, security, or audit importance requires a durable immutable transition record in addition to the aggregate's current state.

The exact significance policy remains subject to later D07 iterations.

---

## 6. State Domains

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

Examples:

- a successful Runtime Session does not automatically complete a Work Item;
- a completed Work Item does not automatically complete a Business Operation;
- technical completion does not automatically establish a successful Business Outcome;
- publication of a Domain Event does not independently change authoritative state;
- a dashboard value does not become authoritative because it is visible to a user;
- an AI conclusion does not become authoritative because it is plausible or confidently expressed.

---

## 7. State Ownership

Every authoritative state has exactly one owning aggregate or explicitly defined domain authority.

The owner is responsible for:

- defining valid state semantics;
- enforcing invariants;
- validating transition requests;
- authorizing or rejecting transitions;
- controlling version advancement;
- preserving required transition history;
- emitting or scheduling significant domain facts after commitment.

Initial ownership model:

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

Business Operation may coordinate state changes across multiple aggregates, but it does not absorb or silently own their authoritative state.

---

## 8. Preliminary Transition Model

The initial semantic flow is:

```text
Transition Request
  -> Identity and Authority Check
  -> Subject and Ownership Resolution
  -> Expected-Version Check
  -> Domain Invariant Validation
  -> Evidence and Result Validation
  -> Transition Decision
  -> Atomic Commit of New State Version
  -> Audit / Outbox Intent
  -> Domain Event Publication
  -> Projection Update
  -> Business Outcome Re-evaluation, when applicable
```

This flow is semantic. It does not require every implementation to use the same process topology or synchronous execution model.

The following distinctions are mandatory:

- request is not commitment;
- validation is not mutation;
- mutation is not publication;
- publication is not projection;
- projection is not authority;
- technical completion is not business outcome.

---

## 9. Candidate Transition Contract

```text
StateTransition {
  transition_id
  workspace_id
  subject_reference
  subject_type
  owner_reference
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
  requested_at
  committed_at
  effective_at
  correlation_id
  causation_id
  idempotency_key
  significance_class
}
```

This is a semantic contract, not a mandatory universal table, event envelope, or shared aggregate type.

Later iterations must determine which fields are universally required, which are conditional, and which belong only to significant transition records.

---

## 10. Constitutional Laws — Iteration 0.1

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

---

## 11. First Workshop Decision

### D07.1 — Nature of State Transition

**Status:** PROPOSED  
**Decision class:** Class A — Constitutional

Proposed decision:

> State Transition is an aggregate-owned validated change of authoritative state.
>
> The owning aggregate or an explicitly authorized domain process is the only authority capable of committing that transition.
>
> Significant transitions additionally produce an immutable first-class transition record.
>
> Low-risk transitions may remain represented through aggregate-owned history, provided required attribution, versioning, causation, authority basis, and audit information are preserved.

This hybrid model avoids two undesirable extremes:

1. a universal State Transition aggregate or state engine imposed on every domain type;
2. opaque aggregate-local mutation with insufficient historical and audit semantics.

D07.1 remains proposed until explicitly approved by the Project Owner.

---

## 12. Iteration Roadmap

D07 will be developed and committed incrementally.

### Iteration 0.1 — Foundation

- purpose and governing question;
- scope and exclusions;
- foundational definitions;
- state domains;
- initial ownership model;
- preliminary transition model;
- candidate transition contract;
- first constitutional laws;
- proposed D07.1 decision.

### Iteration 0.2 — State Dimensions

- phase;
- status;
- outcome;
- progress;
- health;
- terminal and non-terminal semantics;
- unknown, pending, suspended, blocked, expired, cancelled, failed, rejected, and compensated conditions.

### Iteration 0.3 — Validation and Authority

- transition authority basis;
- policy-authorized versus Decision-authorized transitions;
- evidence and Result validation;
- actor attribution;
- effective actor and delegated authority.

### Iteration 0.4 — Concurrency and Idempotency

- expected version;
- optimistic concurrency;
- duplicate requests;
- retries;
- idempotency scope;
- conflict outcomes.

### Iteration 0.5 — Consistency and Publication

- aggregate consistency boundary;
- audit intent;
- transactional outbox semantics;
- event publication;
- projection lag and staleness.

### Iteration 0.6 — Reconstruction and Recovery

- authoritative reconstruction order;
- snapshot and history disagreement;
- audit conflict;
- projection rebuild;
- recovery after partial technical failure.

### Iteration 0.7 — Final Constitutional Review

- complete architectural laws;
- deferred decisions and routing;
- synchronization with Domain Foundation, ADW-01, Decision Register, and Architecture Specification;
- Project Owner approval and D07 closure.

---

## 13. Open Questions

1. Which state dimensions may be shared across Decision, Business Operation, Work Item, and Runtime Session without flattening specialized lifecycles?
2. Is `health` an authoritative state dimension, a derived observation, or context-dependent?
3. Which transitions are always significant?
4. Which transitions require explicit Decision approval?
5. Which transitions may rely on standing policy authority?
6. What is the minimum immutable transition record?
7. When may derived state be stale, and how must staleness be disclosed?
8. What is the authoritative reconstruction order when current snapshot, transition history, audit record, and event stream disagree?
9. Which compensation semantics belong to D07 and which must be deferred to D10?
10. Which persistence and eventing details must remain outside ADW-01?

---

## 14. Current Workshop Status

```text
D07.1 Nature of State Transition: PROPOSED
D07.2 State Dimensions: NOT STARTED
D07.3 Validation and Authority: NOT STARTED
D07.4 Concurrency and Idempotency: NOT STARTED
D07.5 Consistency and Publication: NOT STARTED
D07.6 Reconstruction and Recovery: NOT STARTED
D07.7 Constitutional Review and Closure: NOT STARTED

D07 overall status: IN WORKSHOP
```
