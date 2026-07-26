# D07 — Iteration 0.5: Consistency and Publication

**Parent:** `D07_STATE_SEMANTICS.md`  
**Version:** 0.5-draft  
**Status:** IN WORKSHOP  
**Decision:** D07.5 — Consistency and Publication  
**Decision class:** Class A — Constitutional  
**Date:** 2026-07-21

---

## 1. Purpose

This iteration defines the consistency boundary between authoritative aggregate mutation, transition history, audit intent, event publication, and derived projections.

## 2. Constitutional Decision

> Authoritative aggregate mutation and the durable intent to publish its significant facts must be committed within one consistency boundary.
>
> Event delivery and projection update may be asynchronous, but their delay, duplication, failure, and staleness must never alter the authoritative state already committed by the owning aggregate.

**Status:** PROPOSED

## 3. Aggregate Consistency Boundary

The owning aggregate is the primary strong-consistency boundary for its invariants and state version.

A successful authoritative commit must atomically preserve:

- the new aggregate state version;
- required significant transition history;
- actor and authority attribution;
- audit intent;
- publication intent for significant domain facts.

The physical mechanism may differ by implementation, but no committed state change may depend on a best-effort later process to create its only audit or publication record.

## 4. Cross-Aggregate Coordination

One aggregate must not directly mutate another aggregate's authoritative state inside a hidden distributed transaction.

Cross-aggregate change must use explicit coordination through:

- Business Operation;
- application service;
- saga or process manager;
- command and response sequence;
- compensating Business Operation where required.

Each aggregate independently validates and commits its own state.

## 5. Publication Intent

A significant committed transition must create a durable publication intent containing enough information to publish or reconstruct the corresponding Domain Event.

Publication intent is not the Domain Event delivery itself. It is the durable obligation to publish the committed fact.

## 6. Domain Event Semantics

A Domain Event:

- records a significant fact after authoritative commitment;
- references the subject and committed version;
- carries correlation and causation context;
- may be delivered more than once;
- may arrive late or out of order across aggregates;
- does not independently own or mutate business truth.

Consumers must be idempotent and version-aware where ordering matters.

## 7. Projection Semantics

A projection is derived state and must disclose, where material:

- source aggregate version or checkpoint;
- observation time;
- projection update time;
- freshness or lag;
- incomplete or degraded state;
- rebuild status.

A projection may be eventually consistent. It must not present stale data as current authoritative truth when the distinction affects decisions or risk.

## 8. Failure Scenarios

### State committed, event not yet published

The aggregate state remains authoritative. Publication is retried from durable intent.

### Event published more than once

Consumers deduplicate or process idempotently using event identity and source version.

### Projection update fails

The projection is marked stale or degraded and rebuilt. Authoritative state is not rolled back.

### Consumer rejects an event

The rejection is a consumer-side technical or domain result. It does not reverse the source transition.

### Audit subsystem unavailable

If required audit intent cannot be durably committed, the significant transition must not be accepted.

## 9. Staleness

Staleness is the difference between the authoritative source version and the version represented by a derived model.

Staleness must be explicit when it may affect:

- approvals;
- financial decisions;
- compliance;
- access control;
- safety;
- contractual obligations;
- operational prioritization.

## 10. Architectural Laws Added

### LAW-D07-30 — Commit and Publication Intent Are Atomic

Authoritative mutation and durable publication intent for significant facts must share a consistency boundary.

### LAW-D07-31 — Delivery Is Not Commitment

Event delivery success or failure does not determine whether the authoritative transition occurred.

### LAW-D07-32 — Aggregate Autonomy

Each aggregate owns and commits its own invariants; cross-aggregate coordination must remain explicit.

### LAW-D07-33 — Projection Staleness Is Observable

Derived state must expose material staleness rather than silently presenting it as authoritative current state.

### LAW-D07-34 — Consumers Expect Duplication

Event consumers must tolerate duplicate delivery and must not assume global ordering across aggregates.

## 11. Decision Record

```text
D07.5 Consistency and Publication: PROPOSED
Iteration 0.5: COMPLETE AS DRAFT
D07 overall status: IN WORKSHOP
```
