# D07 — Iteration 0.7: Constitutional Review

**Parent:** `D07_STATE_SEMANTICS.md`  
**Version:** 0.7-draft  
**Status:** READY FOR PROJECT OWNER REVIEW  
**Decision:** D07.7 — Constitutional Review and Closure Preparation  
**Decision class:** Class A — Constitutional  
**Date:** 2026-07-21

---

## 1. Purpose

This iteration consolidates the constitutional conclusions of D07, identifies remaining approval points, and defines the conditions required before D07 may be marked `APPROVED — CLOSED`.

This iteration does not itself approve or close D07. Final authority remains with the Project Owner.

## 2. Consolidated Constitutional Position

D07 proposes that Bizzi adopt the following state model:

1. authoritative state belongs to one owning aggregate or explicitly defined domain authority;
2. execution, workflow, events, projections, reports, caches, and AI outputs do not own business truth;
3. State Transition is an aggregate-owned validated and committed change of authoritative state;
4. significant transitions additionally produce durable immutable transition records;
5. Phase, Status, Outcome, Progress, and Health are separate semantic dimensions;
6. authority to request, approve, validate, and commit change are distinct powers;
7. competing mutations require expected-version or equivalent conflict protection;
8. repeated requests must produce at most one authoritative business effect;
9. aggregate mutation and durable audit/publication intent share a consistency boundary;
10. event delivery and projection update may be asynchronous and do not determine commitment;
11. reconstruction follows aggregate ownership, committed version, transition history, and audit evidence;
12. contradictions affecting business truth become explicit integrity incidents;
13. correction, recovery, reversal, and compensation do not erase prior committed history.

## 3. Proposed Decision Set

### D07.1 — Nature of State Transition

**Proposed:** Hybrid model. State Transition is aggregate-owned; significant transitions additionally create an immutable first-class record.

### D07.2 — State Dimensions

**Proposed:** Phase, Status, Outcome, Progress, and Health are orthogonal dimensions and must not be collapsed.

### D07.3 — Validation and Authority

**Proposed:** Transition validity requires explicit authority basis, actor attribution, invariant validation, evidence validation, and owner-controlled commit.

### D07.4 — Concurrency and Idempotency

**Proposed:** Expected version protects competing mutations; idempotency protects the intended business effect.

### D07.5 — Consistency and Publication

**Proposed:** State mutation and durable publication/audit intent are atomic; event delivery and projections are asynchronous derived processes.

### D07.6 — Reconstruction and Recovery

**Proposed:** Aggregate state and validated history are authoritative; derived records cannot silently override them; contradictions become integrity incidents.

## 4. Architectural Laws Consolidated

The complete proposed law set is grouped as follows:

### Ownership and authority

- business truth is owned by the business domain;
- every authoritative state has one owner;
- only the owner or authorized domain process may commit change;
- delegation does not transfer ownership;
- authority basis must be explicit and auditable.

### Transition semantics

- request is not fact;
- result is not mutation;
- validation precedes commit;
- significant transitions preserve immutable history;
- repair and compensation are new governed changes.

### State dimensions

- Phase, Status, Outcome, Progress, and Health are distinct;
- dependencies among dimensions must be explicit;
- completion and 100% progress do not prove success;
- unknown, absent, pending, and not applicable are distinct.

### Concurrency

- authoritative state cannot be overwritten without conflict detection;
- repeated requests create at most one business effect;
- idempotency is semantic;
- unknown commit outcome requires reconciliation;
- merge rules must be owner-defined.

### Consistency and observation

- aggregate mutation and publication intent are committed together;
- event delivery is not commitment;
- projections are derived and material staleness is visible;
- consumers tolerate duplicates and do not assume global ordering.

### Recovery and integrity

- reconstruction follows authority and committed version;
- derived state cannot repair truth;
- contradictions become explicit integrity incidents;
- recovery does not silently rewrite history.

### AI boundary

- AI may observe, classify, recommend, predict, explain, or propose;
- AI output becomes authoritative only through a governed Decision or transition process.

## 5. Deferred Decisions

The following matters remain outside D07 and must be routed explicitly:

### D09 — Relationship Model

- typed links among Decision, Business Operation, Work Item, State Transition, Result, Evidence, Actor, and Domain Event;
- relationship ownership and cardinality;
- cross-reference integrity.

### D10 — Deletion and Supersession

- archival;
- revocation;
- supersession;
- reversal;
- compensation detail;
- legal deletion and retention exceptions.

### Later architecture workshops

- physical persistence schema;
- event transport and broker topology;
- workflow notation;
- projection implementation;
- audit storage;
- security enforcement mechanisms;
- concrete APIs and message envelopes.

## 6. Closure Conditions

D07 may be marked `APPROVED — CLOSED` only when:

1. the Project Owner explicitly approves D07.1 through D07.6;
2. the parent `D07_STATE_SEMANTICS.md` is consolidated with all approved decisions;
3. `DOMAIN_FOUNDATION.md` reflects the final authoritative-state model;
4. `ADW_01_CORE_DOMAIN_SEMANTICS.md` reflects D07 closure;
5. `ADW_01_DECISION_REGISTER.md` records the approved decision and consequences;
6. `ARCHITECTURE_SPECIFICATION.md` references the final state constitution;
7. terminology and law numbering are checked for collisions;
8. deferred matters are assigned without semantic gaps;
9. the repository contains no competing state model presented as authoritative.

## 7. Review Questions for Project Owner

1. Approve the hybrid State Transition model?
2. Approve the five independent state dimensions?
3. Approve Health as derived by default?
4. Approve explicit authority basis for every governed transition?
5. Approve expected-version and semantic idempotency requirements?
6. Approve atomic state mutation plus audit/publication intent?
7. Approve the proposed reconstruction precedence?
8. Approve explicit integrity incidents instead of silent automated repair?
9. Approve all proposed architectural laws as constitutional constraints?
10. Authorize consolidation and synchronized closure of D07?

## 8. Review Outcome

```text
D07.1 Nature of State Transition: PROPOSED
D07.2 State Dimensions: PROPOSED
D07.3 Validation and Authority: PROPOSED
D07.4 Concurrency and Idempotency: PROPOSED
D07.5 Consistency and Publication: PROPOSED
D07.6 Reconstruction and Recovery: PROPOSED
D07.7 Constitutional Review: COMPLETE AS DRAFT

D07 overall status: READY FOR PROJECT OWNER REVIEW
D07 closure status: NOT CLOSED
```
