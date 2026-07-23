# ADW-01 — Decision Register

**Document ID:** ARCH-DOMAIN-DECISIONS-001  
**Version:** 0.9-draft  
**Status:** Workshop in progress — D09 closed; D10 next  
**Architecture Gate:** Gate C v1.1  
**Workshop:** ADW-01 — Core Domain Semantics  
**Decision authority:** Project Owner  
**Parent chapter:** `00_ARCHITECTURE/01_DOMAIN/ADW_01_CORE_DOMAIN_SEMANTICS.md`  
**Foundation:** `00_ARCHITECTURE/00_FOUNDATION/DOMAIN_FOUNDATION.md`  
**State constitution:** `00_ARCHITECTURE/01_DOMAIN/D07_STATE_SEMANTICS.md`

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
| D07 | State Semantics | APPROVED — CLOSED |
| D08 | Aggregate Strategy | APPROVED |
| D09 | Relationship Model | APPROVED — CLOSED |
| D10 | Deletion and Supersession | OPEN — NEXT |

---

## 3. D01 — Primary Boundary

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

> Workspace is the primary ownership, authorization, governance, and isolation boundary for workspace-scoped business-state objects in Bizzi.

---

## 4. D02 — Core Business Abstraction

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

> Enterprise Object is the stable platform abstraction for a durable, workspace-owned, business-relevant thing with identity, lifecycle, ownership, relationships, state, and governance requirements.

---

## 5. D03 — Work Model

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

> Work Item is the abstract representation of governed business work. Task, Case, and Project are specialized Work Item types with their own lifecycle rules and invariants.

---

## 6. D04 — Task versus Execution

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

> Task and Runtime Session are separate aggregates. Runtime Session state is never the authoritative source of Task state.

---

## 7. D05 — Actor Model

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

> Actor is the stable identity of a human, agent, service, or external participant capable of initiating, performing, approving, observing, or being accountable for governed actions in Bizzi.

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
> Decision defines an authoritative determination. Business Operation coordinates realization of an intent or Decision.
>
> Business Operation is not a universal aggregate that owns referenced domain objects.
>
> Business Operation completion is determined by validated business outcomes and explicit completion criteria, not solely by technical execution success.

### Binding consequences

1. `Decision + Business Operation` is the primary domain construction of Bizzi.
2. Work Item, Runtime Session, Action, Result, State Transition, and Domain Event remain separate concepts.
3. Detailed state semantics are assigned to D07.
4. Detailed typed relationships are assigned to D09.
5. Deletion, supersession, reversal, compensation, archival, and retention are assigned to D10.

---

## 9. D07 — State Semantics

**Status:** `APPROVED — CLOSED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-22  
**Closure date:** 2026-07-22  
**Decision class:** Class A — Constitutional  
**Canonical decision:** `00_ARCHITECTURE/01_DOMAIN/D07_STATE_SEMANTICS.md`

### Decision

> Authoritative state belongs to exactly one owning aggregate or explicitly defined domain authority.
>
> Execution, workflow, events, projections, reports, caches, analytics, and AI outputs do not own business truth.
>
> State Transition is an aggregate-owned, validated, and committed change from one authoritative state version to another.
>
> Significant transitions additionally produce durable immutable transition records.
>
> Phase, Status, Outcome, Progress, and Health are separate semantic dimensions and must not be collapsed into one universal authoritative field.
>
> Authority to request, approve, validate, and commit change are distinct powers.
>
> Competing mutations require expected-version or equivalent conflict protection.
>
> Repeated requests must produce at most one authoritative business effect.
>
> Aggregate mutation and durable audit/publication intent share an explicit consistency boundary.
>
> Reconstruction follows authoritative ownership and committed history rather than events, projections, reports, caches, analytics, or AI interpretations.

### Approved sub-decisions

| Sub-decision | Subject | Status |
|---|---|---|
| D07.1 | Nature of State Transition | APPROVED |
| D07.2 | State Dimensions | APPROVED |
| D07.3 | Validation and Authority | APPROVED |
| D07.4 | Concurrency and Idempotency | APPROVED |
| D07.5 | Consistency and Publication | APPROVED |
| D07.6 | Reconstruction and Recovery | APPROVED |
| D07.7 | Constitutional Review and Closure | APPROVED — CLOSED |

### Binding consequences

1. Request is not commitment.
2. Validation is not mutation.
3. Mutation is not publication.
4. Publication is not projection.
5. Projection is not authority.
6. Technical completion is not business outcome.
7. Domain Events record committed facts and do not independently mutate authoritative state.
8. Derived state is rebuildable, version-aware, and may be stale.
9. Cross-aggregate consistency requires explicit coordination.
10. AI output remains advisory until accepted through a governed domain process.

### Deferred responsibilities

- D09: typed relationships among state-bearing concepts and transition records.
- D10: deletion, archival, supersession, revocation, reversal, compensation, and retention.
- ADW-03: detailed authorization and policy evaluation.
- ADW-05: runtime-specific execution states and retry mechanics.
- ADW-07: audit, provenance, and event contracts.
- ADW-08: persistence, transactions, outbox, indexing, and recovery mechanics.

### Closure record

D07 is officially closed because authoritative and derived state, ownership, transition semantics, dimensions, validation, concurrency, idempotency, consistency, publication, reconstruction, recovery, and downstream routing are explicitly defined and approved by the Project Owner.

### Supersession rule

D07 may be changed only by an explicit Class A architecture decision that preserves authoritative ownership, state version history, transition attribution, authority basis, idempotency semantics, audit compatibility, projection compatibility, and historical integrity.

---

## 10. D08 — Aggregate Strategy

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

> Work Item is a shared domain contract and coordination abstraction, not one universal aggregate root. Task, Case, and Project are separate aggregate roots.

---

## 11. D09 — Relationship Model

**Status:** `APPROVED — CLOSED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-23  
**Closure date:** 2026-07-23  
**Decision class:** Class A — Constitutional  
**Canonical decision:** `00_ARCHITECTURE/01_DOMAIN/D09_RELATIONSHIP_MODEL.md`

### Decision

> Bizzi defines exactly eleven canonical relationships among Enterprise Object, Actor, Work Item, Decision, Business Operation, and Runtime Session, each with an explicit category, ownership assignment, reference direction, cardinality, and mutation authority.
>
> No relationship among these six concepts transfers ownership, grants cross-aggregate mutation authority, or creates a universal super-aggregate. Business Operation coordinates and references; it does not own. Decision governs; it does not execute. Runtime Session executes; it never becomes the authoritative source of another concept's state. Work Item coordinates Task/Case/Project by type-membership, not by ownership. Actor is attributed to governed actions via Provenance; its identity is owned only by itself.
>
> The inverse view of every relationship is a derived projection of one authoritative forward assertion, never an independent fact. Enterprise Object must never carry an authoritative back-reference collection of everything that references it.
>
> Ten relationship shapes are constitutionally prohibited, each a direct consequence of an already-approved D01–D08 decision. Consistency is enforced at creation time through endpoint and authority-basis validation, never through retroactive rewriting of historical record.

### Approved sub-decisions

| Sub-decision | Subject | Status |
|---|---|---|
| D09.1 | Nature of Relationship | APPROVED |
| D09.2 | Relationship Taxonomy | APPROVED |
| D09.3 | Roles, Direction, and Cardinality | APPROVED |
| D09.4 | Ownership, Authority, and Validation | APPROVED |
| D09.5 | Lifecycle and Temporal Semantics | APPROVED |
| D09.6 | Consistency, Traversal, and Graph Views | APPROVED |
| D09.7 | Constitutional Review and Closure | APPROVED — CLOSED |

### Binding consequences

1. Gate C's Enterprise Object, Task (as a Work Item specialization), Decision, and Runtime Session schema work may proceed using the D09 relationship shapes without re-litigating direction, cardinality, or ownership per entity.
2. Enterprise Object's schema must not include an authoritative field or table holding "all referencing Operations/Decisions/Work Items" — any such view is a read model built outside its own aggregate boundary.
3. Any repository or service method allowing Runtime Session to write directly to Enterprise Object, Decision, or Business Operation state is a Gate C implementation defect, not a valid interpretation of this model.
4. D10 inherits D09's Historical classification as a starting constraint: nothing D09 classifies Historical may be physically deleted by whatever D10 ultimately decides — only superseded, compensated, or archived.

### Deferred responsibilities

- D10: physical deletion, archival, revocation, reversal, compensation, and retention semantics for relationships D09 classifies Historical.
- ADW-03: authorization policy evaluation governing who may create a given relationship instance.
- ADW-05: Runtime Session's internal execution-attempt state machine.
- ADW-07: the event/audit contract for relationship creation and change.
- ADW-08: any persistence representation of these relationships (explicitly out of D09's scope — no schema, no foreign keys, no ORM).

### Closure record

D09 is officially closed because relationship identity, categories, roles, direction, cardinality, ownership, mutation authority, prohibited shapes, lifecycle classification, and consistency rules for all six domain-owning concepts are explicitly defined and approved by the Project Owner.

### Supersession rule

D09 may be changed only by an explicit Class A architecture decision that preserves the ownership assignments in D01–D08, the Historical/append-only guarantees D09 establishes, and the prohibition against any of the six concepts becoming a universal super-aggregate.

---

## 12. Remaining Decisions

### D10 — Deletion and Supersession

**Status:** `OPEN — NEXT`

Must define cancellation, expiration, revocation, supersession, reversal, compensation, archival, deletion, retention, and historical-preservation semantics — inheriting D09's Historical classification as a starting constraint.

---

## 13. Current Workshop State

```text
D01: APPROVED
D02: APPROVED
D03: APPROVED
D04: APPROVED
D05: APPROVED
D06: APPROVED — CLOSED
D07: APPROVED — CLOSED
D08: APPROVED
D09: APPROVED — CLOSED
D10: OPEN — NEXT
ADW-01: IN PROGRESS
```
