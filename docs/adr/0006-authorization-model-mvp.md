# ADR-0006: Owner-only authorization for MVP, RBAC-ready extension path

- Status: Accepted
- Date: 2026-07-11
- Deciders: Engineering
- Governance level: L2 (implements scope already fixed by `02_MVP_VERTICAL_SLICE.md`)

## Context

`30_BACKEND_IMPLEMENTATION_PLAN/01_TECH_STACK_DECISION.md` scopes the MVP
authorization model to owner-only checks and explicitly excludes full RBAC
from `02_MVP_VERTICAL_SLICE.md`. Long-term, `01_GOVERNANCE/AUTHORITY_MATRIX.md`
defines an eight-level authority model (A0 Observe Only … A7 Human Reserved
Authority) that will eventually need to reach into the backend's
authorization checks once AI agents (WP-19, Phase 3) start acting through the
API.

## Decision

`AuthorizationService` implements owner-only checks for the MVP, but is built
behind a single interface/shape designed to later support `workspace_access`
roles and agent authority scopes without changing call sites:

- Every authorization check goes through `AuthorizationService`
  (`assertCan<Action>(actorContext, resource)` shape) — no controller or
  service special-cases "is this the owner?" logic inline.
- The service's internal implementation may be a simple owner-equality check
  today; callers depend only on the pass/`ForbiddenError` contract, not on
  how the check is made.

## Consequences

- MVP ships faster — no role/permission schema needed yet.
- The eventual RBAC expansion (post-MVP) is a change inside
  `AuthorizationService` only; it does not require touching every module that
  calls it, because they already depend on the abstract contract.
- Until RBAC lands, only the workspace owner can act — this is a real
  functional limitation, not just an implementation detail, and should be
  communicated as such if the MVP is used beyond single-owner testing.

## Alternatives considered

- Build full RBAC now — rejected: explicitly out of MVP scope per
  `02_MVP_VERTICAL_SLICE.md`; would delay the vertical slice for a capability
  nothing in Phase 0/1 needs yet.
- Inline ownership checks per module (no central `AuthorizationService`) —
  rejected: violates ADR-0003 layering and would require touching every call
  site when RBAC is eventually added.

## References

- `30_BACKEND_IMPLEMENTATION_PLAN/01_TECH_STACK_DECISION.md` (§Authorization)
- `30_BACKEND_IMPLEMENTATION_PLAN/02_MVP_VERTICAL_SLICE.md`
- `01_GOVERNANCE/AUTHORITY_MATRIX.md`
- ADR-0003 (Controller-Service-Repository layering)
