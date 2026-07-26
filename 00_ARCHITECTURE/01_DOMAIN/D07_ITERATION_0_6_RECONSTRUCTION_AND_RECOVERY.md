# D07 — Iteration 0.6: Reconstruction and Recovery

**Parent:** `D07_STATE_SEMANTICS.md`  
**Version:** 0.6-draft  
**Status:** IN WORKSHOP  
**Decision:** D07.6 — Reconstruction and Recovery  
**Decision class:** Class A — Constitutional  
**Date:** 2026-07-21

---

## 1. Purpose

This iteration defines how Bizzi determines authoritative state when current snapshots, transition history, audit records, events, and projections disagree or become partially unavailable.

## 2. Constitutional Decision

> Authoritative reconstruction begins from the owning aggregate's committed state and version, supported by its validated transition history and audit evidence.
>
> Domain Events and projections are secondary evidence and must never silently override the owning aggregate.
>
> Any unresolved disagreement affecting business truth must be surfaced as an explicit integrity incident rather than repaired by guesswork.

**Status:** PROPOSED

## 3. Reconstruction Order

The default semantic precedence is:

```text
1. Owning aggregate committed state and version
2. Aggregate-owned significant transition history
3. Durable audit and publication intent
4. Published Domain Events
5. Projections and read models
6. Reports, analytics, caches, search indexes, and AI interpretations
```

This precedence does not mean an inconsistent aggregate snapshot is automatically trusted. It defines where authority originates and how contradictions are investigated.

## 4. Snapshot and History Agreement

A snapshot and transition history agree when:

- subject identity matches;
- committed version matches the final applied transition;
- transition order is valid;
- required invariants hold;
- state dimensions reconstruct to the same semantic condition;
- attribution and authority evidence remain available.

If they disagree, the system must quarantine automated mutation of the affected subject until integrity is restored or an explicit recovery policy permits limited operation.

## 5. Recovery Modes

### Replay

Reapply validated transition records to rebuild a snapshot or projection.

### Rehydrate

Load a trusted snapshot and apply later validated transitions.

### Reconcile

Compare independent records and produce an explicit integrity finding.

### Repair

Create a governed corrective transition or administrative recovery record. Repair must not rewrite prior committed history invisibly.

### Rebuild

Discard and regenerate derived state from authoritative sources.

## 6. Partial Technical Failure

### Commit succeeded, response lost

Resolve by transition identity, aggregate version, or idempotency key before retrying.

### Snapshot written, publication delayed

State remains committed; publication resumes from durable intent.

### Event delivered, projection failed

Projection is marked stale and rebuilt.

### Audit evidence missing

For significant transitions, missing required audit evidence is an integrity incident. The system must not manufacture attribution retroactively without a governed recovery record.

### Aggregate unavailable

Derived state may be used for read-only continuity only when clearly marked with freshness and authority limitations.

## 7. Integrity Incident

An integrity incident exists when records disagree about:

- whether a transition committed;
- the current aggregate version;
- the actor or authority basis;
- the effective time;
- the resulting authoritative state;
- the existence of a required significant transition record.

An integrity incident must have:

- incident identity;
- affected Workspace and subjects;
- detected contradictions;
- risk classification;
- operational restrictions;
- responsible recovery authority;
- evidence preserved;
- final resolution and corrective actions.

## 8. Projection Recovery

Projections are disposable and rebuildable.

A projection rebuild must:

- identify the authoritative source checkpoint;
- preserve or reset consumer idempotency state safely;
- disclose partial availability;
- avoid presenting mixed-version data as coherent current truth;
- verify the final source version represented.

## 9. Time Semantics

Reconstruction must distinguish:

- `recorded_at` — when the system stored a record;
- `committed_at` — when the transition was committed;
- `effective_at` — when the business change became effective;
- `observed_at` — when a derived model observed the source;
- `published_at` — when an event was published.

Wall-clock timestamps alone must not determine authoritative transition order inside an aggregate; committed version remains primary.

## 10. Architectural Laws Added

### LAW-D07-35 — Authority Determines Reconstruction

Reconstruction follows domain ownership and committed version, not convenience or data availability.

### LAW-D07-36 — Derived State Never Repairs Truth

A projection, report, cache, analytic model, or AI output must not silently repair or override authoritative state.

### LAW-D07-37 — Contradiction Must Be Visible

Material disagreement among authoritative records must become an explicit integrity incident.

### LAW-D07-38 — Repair Is a Governed Change

Recovery that changes business truth must occur through a new attributable and auditable governed transition.

### LAW-D07-39 — History Is Not Silently Rewritten

Recovery may rebuild representations but must not invisibly alter prior committed history.

## 11. Decision Record

```text
D07.6 Reconstruction and Recovery: PROPOSED
Iteration 0.6: COMPLETE AS DRAFT
D07 overall status: IN WORKSHOP
```
