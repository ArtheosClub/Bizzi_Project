# ADR-0004: Workspace as root aggregate / mandatory multi-tenant scoping

- Status: Accepted
- Date: 2026-07-11
- Deciders: Engineering
- Governance level: L3 (affects every module's data-access contract)

## Context

`26_DOMAIN_MODEL/00_DOMAIN_MODEL_VISION.md` names `CompanyWorkspace` as the
root aggregate, with the stated invariant "no major runtime object may exist
without `workspace_id`." The risk register's single Critical, top-listed risk
is R-DATA-001, Workspace Isolation Failure — a query or response that crosses
a `workspace_id` boundary would leak one customer's data to another.

## Decision

- Every MVP table beyond `users` and `sessions` carries `workspace_id`.
- Every repository method is workspace-scoped by construction:
  `findByIdAndWorkspace`, `listByWorkspace`, `updateByIdAndWorkspace`,
  `archiveByIdAndWorkspace`. A bare `findById(id)` without a workspace
  parameter must never be added to any repository, for any entity, ever.
- `AuthorizationService` always receives workspace context as part of
  `ActorContext`; no service method may skip it.
- This is a coded-in structural rule, not a convention: repository base
  classes/interfaces in the shared kernel (WP-03) should make the
  workspace-scoped signature the only one available.

## Consequences

- Strong tenant isolation by construction, not by developer discipline alone.
- Every new module must plumb `workspace_id` through from day one — no
  "we'll add scoping later" path exists, which is intentional given the risk
  severity.
- Workspace isolation breaking is a named Stop Condition
  (`14_IMPLEMENTATION_CHECKLIST.md` §20) — any code review or test finding
  that violates this halts merge, no exceptions.

## Alternatives considered

- Shared tables with app-level filtering only, no structural repository
  constraint — rejected: relies entirely on every developer (and every
  AI-generated diff) remembering to filter correctly every time; provides no
  mechanical enforcement against exactly the failure mode R-DATA-001
  describes.
- Database-per-tenant — rejected for MVP: excessive operational complexity
  for the current scale target; revisit only if a real multi-tenant scaling
  need emerges post-MVP.

## References

- `26_DOMAIN_MODEL/00_DOMAIN_MODEL_VISION.md`, `01_ENTITY_CATALOG.md`
- `30_BACKEND_IMPLEMENTATION_PLAN/08_REPOSITORY_IMPLEMENTATION_GUIDE.md`
- `30_BACKEND_IMPLEMENTATION_PLAN/12_IMPLEMENTATION_RISK_REGISTER.md` (R-DATA-001)
- `30_BACKEND_IMPLEMENTATION_PLAN/14_IMPLEMENTATION_CHECKLIST.md` §20
