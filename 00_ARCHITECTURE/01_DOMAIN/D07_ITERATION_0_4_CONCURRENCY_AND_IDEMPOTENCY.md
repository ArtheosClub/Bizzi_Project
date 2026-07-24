# D07 — Iteration 0.4: Concurrency and Idempotency

**Parent:** `D07_STATE_SEMANTICS.md`  
**Version:** 0.4-draft  
**Status:** IN WORKSHOP  
**Decision:** D07.4 — Concurrency and Idempotency  
**Decision class:** Class A — Constitutional  
**Date:** 2026-07-21

---

## 1. Purpose

This iteration defines how Bizzi protects authoritative state from lost updates, duplicate requests, retries, races, and ambiguous execution outcomes.

## 2. Constitutional Decision

> Every competing mutation of authoritative state must be protected by an expected version or an equivalent conflict-detection mechanism.
>
> Repeated delivery of the same transition request must not create multiple authoritative effects.
>
> Idempotency applies to the governed business effect, not merely to transport or API response reuse.

**Status:** PROPOSED

## 3. State Version

Every authoritative aggregate state must expose a monotonically advancing version or equivalent concurrency token.

A committed transition advances the version exactly once.

The version represents the order of accepted aggregate mutations. It is not a business timestamp and must not be inferred from wall-clock time.

## 4. Expected Version

A transition request that may compete with other changes must declare the state version against which it was evaluated.

The commit is accepted only when:

```text
expected_version == current_authoritative_version
```

or when an explicitly defined merge rule proves that the competing changes are compatible.

## 5. Conflict Outcomes

A concurrency conflict must produce an explicit result such as:

```text
RejectedAsStale
RequiresRevalidation
RequiresMerge
SupersededByNewerState
AlreadyApplied
```

The platform must not silently overwrite newer authoritative state.

## 6. Idempotency Key

A transition request that may be retried must carry an idempotency key scoped to:

- Workspace;
- owning aggregate or domain authority;
- operation or command type;
- intended business effect;
- defined retention period.

The same key with the same semantic intent must return or reference the original accepted outcome.

The same key with materially different intent must be rejected as an idempotency conflict.

## 7. Retry Semantics

Retries are new execution attempts for the same intended business effect.

A retry must not:

- create duplicate authoritative transitions;
- duplicate financial or legal effects;
- erase the original failure;
- bypass revalidation when state or policy changed;
- reuse stale evidence without explicit validity rules.

## 8. Unknown Commit Outcome

When a caller cannot determine whether a commit succeeded, it must query by transition identity or idempotency key before issuing a new mutation.

An unknown technical response must never be interpreted as proof that the business transition failed.

## 9. Merge Rules

Automatic merge is permitted only when the owning aggregate explicitly defines commutative or conflict-free semantics.

Absence of a merge rule means competing changes require rejection and re-evaluation.

## 10. Ordering

Aggregate version defines authoritative mutation order within an aggregate.

Correlation time, event publication time, projection time, and receipt time must not replace aggregate version as the authoritative ordering mechanism.

Cross-aggregate global ordering is not assumed.

## 11. Architectural Laws Added

### LAW-D07-25 — No Lost Update

Authoritative state must not be overwritten without conflict detection.

### LAW-D07-26 — One Business Effect

Repeated delivery of the same governed request must produce at most one authoritative business effect.

### LAW-D07-27 — Idempotency Is Semantic

Idempotency is defined by intended business effect, not only by request bytes, endpoint, or transport message.

### LAW-D07-28 — Unknown Is Not Failed

An unknown commit outcome requires reconciliation before retry and must not be treated as confirmed failure.

### LAW-D07-29 — Merge Must Be Explicit

Concurrent changes may be merged only through owner-defined semantics.

## 12. Decision Record

```text
D07.4 Concurrency and Idempotency: PROPOSED
Iteration 0.4: COMPLETE AS DRAFT
D07 overall status: IN WORKSHOP
```
