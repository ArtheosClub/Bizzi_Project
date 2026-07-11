# ADR-0005: Audit-first mutations via AuditService + RuntimeEventService

- Status: Accepted
- Date: 2026-07-11
- Deciders: Engineering
- Governance level: L2 (implements an already-accepted governance principle)

## Context

`Vision.md` and `01_GOVERNANCE/GOVERNANCE_MODEL.md` both name **Auditability**
as a constitutional principle: "every decision can be traced and verified."
`29_BACKEND_SERVICE_DESIGN` Principles B07/B08 translate this into backend
terms: "audit is first-class" and "runtime events coordinate, not prove."
The Implementation Checklist names a missing audit event on a state-changing
action as a hard Stop Condition.

## Decision

- Every state-changing service method calls `AuditService.record(...)` using
  named constants from `AuditActions` (e.g. `AuditActions.TASK_COMPLETED`) —
  never a manual/ad-hoc audit table write from anywhere else in the codebase.
- The audit write happens **inside the same transaction**
  (`TransactionManager.runInTransaction`) as the domain mutation it records —
  if the mutation doesn't commit, neither does its audit trail, and vice
  versa.
- After the transaction commits, the service emits a `RuntimeEvent` via
  `RuntimeEventService` for coordination/observability purposes.
  `RuntimeEvent`s are not the audit record — they exist to let other parts of
  the system react, not to prove what happened. `AuditEvent` is the
  authoritative, queryable trail.

## Consequences

- Every mutation carries two extra calls (audit + event), but this is
  non-negotiable given the Auditability principle and is mechanically
  checkable in review: "does this service call `AuditService.record`?"
- Because audit and mutation share a transaction, there is no window where a
  state change exists without its audit record.
- Distinguishing audit-as-truth from events-as-coordination avoids a common
  failure mode: treating an emitted event as proof something happened, when
  event delivery is not guaranteed the way a committed transaction is.

## Alternatives considered

- Log-based audit only (structured logs, no DB table) — rejected: not
  reliably queryable/joinable against domain entities for traceability
  requirements.
- Fully event-sourced audit (derive audit trail from an event stream) —
  rejected for MVP: adds significant complexity (event store, replay
  logic) that the MVP vertical slice explicitly excludes; revisit in Phase 3+
  if event volume/replay needs justify it.

## References

- `Vision.md` (Auditability principle)
- `01_GOVERNANCE/GOVERNANCE_MODEL.md`
- `29_BACKEND_SERVICE_DESIGN/01_BACKEND_ARCHITECTURE_PRINCIPLES.md` (B07, B08)
- `30_BACKEND_IMPLEMENTATION_PLAN/14_IMPLEMENTATION_CHECKLIST.md` §20
