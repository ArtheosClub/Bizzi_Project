# ADR-0003: Controller-Service-Repository layering enforced by import boundaries

- Status: Accepted
- Date: 2026-07-11
- Deciders: Engineering
- Governance level: L2

## Context

`29_BACKEND_SERVICE_DESIGN/01_BACKEND_ARCHITECTURE_PRINCIPLES.md` (Principles
B02/B03) and `30_BACKEND_IMPLEMENTATION_PLAN/13_BACKEND_CODING_STANDARDS.md`
both specify a strict Controller→Service→Repository (CSR) layering, but as
prose rules only. Risk R-ARCH-002 ("CSR boundary violation") in the risk
register exists precisely because prose rules get skipped under delivery
pressure, especially in AI-generated code (R-AI-001).

## Decision

Adopt CSR as a hard, one-directional layering, enforced structurally (module
folder layout from `03_REPOSITORY_STRUCTURE.md`: `controllers/ services/
repositories/` per module) and checked in review, not just documented:

- **Controllers**: DTO validation (`class-validator`) and delegation only.
  Never call Prisma, never call a repository directly, never contain
  business rules, never emit audit/runtime events.
- **Services**: own orchestration — authorization, validation, transaction,
  repository calls, audit recording, event emission, response mapping. Never
  return raw Prisma records; never ignore `workspace_id`.
- **Repositories**: workspace-scoped persistence only. Never authorize,
  never own lifecycle rules, never emit events, never return DTOs. Accept
  `DbClient = PrismaClient | Prisma.TransactionClient` so they compose inside
  `TransactionManager.runInTransaction`.
- Dependency direction is one-way: `controller → service → repository`.
  `repository → service` is forbidden. `SharedKernelModule` must not import
  from `modules/`.

The canonical mutation flow this produces is documented as a diagram in
`docs/c4/C4_DYNAMIC_CANONICAL_FLOW.md`.

## Consequences

- Predictable, testable code: services are unit-testable without an HTTP
  layer; repositories are swappable (e.g., off Prisma) without touching
  service logic.
- Slight boilerplate per module (three files minimum instead of one).
- A violation is mechanically checkable in review: "does this controller
  import PrismaClient or a repository?" is a yes/no question, not a judgment
  call.

## Alternatives considered

- Fat controllers with inline business logic — rejected: directly violates
  B02, and is exactly the shape R-ARCH-002 warns about.
- Active-record style models (business logic on the model class) — rejected:
  conflicts with the repository-hides-Prisma decision in
  `01_TECH_STACK_DECISION.md`, which requires repositories to be swappable
  independent of the ORM.

## References

- `29_BACKEND_SERVICE_DESIGN/01_BACKEND_ARCHITECTURE_PRINCIPLES.md` (B02, B03)
- `29_BACKEND_SERVICE_DESIGN/03_CONTROLLER_SERVICE_REPOSITORY_PATTERN.md`
- `30_BACKEND_IMPLEMENTATION_PLAN/07_SERVICE_IMPLEMENTATION_GUIDE.md`
- `30_BACKEND_IMPLEMENTATION_PLAN/08_REPOSITORY_IMPLEMENTATION_GUIDE.md`
- `30_BACKEND_IMPLEMENTATION_PLAN/12_IMPLEMENTATION_RISK_REGISTER.md` (R-ARCH-001, R-ARCH-002, R-AI-001)
