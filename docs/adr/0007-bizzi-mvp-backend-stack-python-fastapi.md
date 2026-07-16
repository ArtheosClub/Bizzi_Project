# ADR-0007: Bizzi MVP backend stack is Python + FastAPI, not TypeScript/NestJS

- Status: Accepted
- Date: 2026-07-16
- Deciders: Project Owner (direct decision, delivered via `docs/planning/PRE-CODING-BRIEF.md`)
- Governance level: L3 (architecture/tech-stack scoping decision, same class as the ADR it supersedes) — decided directly by the project owner, satisfying the sign-off this level requires.

## Context

ADR-0002 recorded a scope decision — TypeScript/NestJS/PostgreSQL/Prisma —
for the Bizzi Platform MVP backend, made by Engineering to unblock coding
given two competing stacks in the spec corpus (the platform-wide "Art of
Business" Python/Kubernetes vision vs. the execution-detailed
`30_BACKEND_IMPLEMENTATION_PLAN` NestJS plan). ADR-0002 explicitly flagged
itself as provisional and asked for project-owner review before any Phase 0
code was written: *"If this contradicts intent ... raise it before Phase 0
of `DEVELOPMENT_PLAN.md` begins."*

The project owner has now reviewed it and responded with
`docs/planning/PRE-CODING-BRIEF.md`, which resolves the stack question
explicitly and directly (brief §1): the MVP backend is **Python + FastAPI**,
not TypeScript/NestJS. This arrives before any Phase 0/Gate B code exists —
confirmed by repository audit (see Consequences) — so this is a course
correction on paper, not a rewrite of working code.

The brief also resolves adjacent architecture questions bundled with the
stack choice: frontend is React + TypeScript, MVP deployment is Docker
Compose, architecture style is a modular monolith, and Kubernetes is
explicitly deferred until the MVP works and a real scaling need is proven
("Kubernetes-ready, but not Kubernetes-dependent").

## Decision

The Bizzi Platform MVP backend stack is:

- **Backend**: Python + FastAPI
- **Database**: PostgreSQL (ORM/migration tooling to be decided in a
  follow-up WP-level change — e.g. SQLAlchemy + Alembic — not fixed by this
  ADR)
- **Frontend**: React + TypeScript
- **Architecture style**: modular monolith
- **MVP deployment**: Docker Compose
- **Kubernetes**: not part of MVP; module boundaries and service interfaces
  should be designed so a future extraction to Kubernetes is possible, but
  no Kubernetes manifests, service mesh, or orchestration complexity are
  built now

This ADR formally supersedes **ADR-0002**, whose Status header is updated to
`Superseded by ADR-0007` in this same change. ADR-0002's original Context,
Decision, Consequences, Alternatives, and References sections are left
untouched as a historical record of the reasoning that led here — per
`docs/adr/README.md`, ADRs are immutable once accepted and are superseded,
not rewritten.

## Consequences

- **Unblocks Gate B (Engineering Foundation)** per the Pre-Coding Brief's
  gate structure, on the stack that is now definitively decided rather than
  provisionally scoped.
- **No code to discard.** Repository audit at the time of this ADR found no
  NestJS/Prisma (or any) source code anywhere in the repository — no
  `package.json`, `*.prisma`, `*.ts`, `*.tsx`, `*.js`, `*.jsx`,
  `nest-cli.json`, `tsconfig*.json`, or `prisma/`/`backend/`/`src/`
  directories outside `node_modules`. Everything produced under ADR-0002 was
  documentation and governance scaffolding (`docs/planning/`, `docs/adr/`,
  `docs/c4/`, `.claude/skills/`, `CLAUDE.md`), not application code. This
  ADR does not need to declare any source deletion/rewrite plan because
  there is nothing to delete.
- **What still needs updating is deferred, on purpose.** Per explicit
  instruction, this change does **not** touch `docs/c4/C2_CONTAINER.md`,
  `docs/c4/C3_COMPONENT.md` (NestJS-module-based, no FastAPI equivalent), or
  `docs/planning/WORK_PACKAGES.md` / `DEVELOPMENT_PLAN.md`
  (NestJS/Prisma-specific deliverables, e.g. Prisma migrations). Those are
  follow-up changes, to happen after this ADR is reviewed.
- **What carries over unchanged**, because it encodes stack-agnostic
  architectural principles rather than NestJS-specific implementation:
  ADR-0003 (Controller-Service-Repository layering — reinterpret
  "Controller" as "Router/Endpoint" for FastAPI in a future pass, no new ADR
  needed for that relabeling), ADR-0004 (workspace-scoped multi-tenancy),
  ADR-0005 (audit-first mutations), ADR-0006 (MVP authorization model),
  `docs/c4/C1_CONTEXT.md`, and `docs/c4/C4_DYNAMIC_CANONICAL_FLOW.md`.
- **`CLAUDE.md` governance gates and stop conditions are unaffected** —
  workspace isolation, authorization bypass, missing audit records, and CI
  failures as hard blockers are stack-agnostic and remain in force as
  written.
- Risk carried over from ADR-0002 is now resolved rather than merely
  tracked: there is no longer a live question of whether Bizzi's backend
  needs to bridge to the Art of Business platform's Python runtime through
  an adapter layer — both now speak Python, which simplifies (but does not
  by itself guarantee) that future integration.

## Alternatives considered

- **Keep TypeScript/NestJS per ADR-0002** — rejected: superseded by explicit
  project-owner direction; ADR-0002 itself invited exactly this correction
  before Phase 0 began, and no code exists yet to make reversing it costly.
- **Adopt Kubernetes alongside the stack change** — rejected per the brief's
  explicit "Kubernetes-ready, but not Kubernetes-dependent" principle:
  premature orchestration complexity before the MVP exists and a scaling
  need is demonstrated.
- **Rewrite ADR-0002 in place instead of superseding it** — rejected: would
  destroy the historical record of why NestJS was chosen and violates the
  immutability rule in `docs/adr/README.md`.

## References

- `docs/planning/PRE-CODING-BRIEF.md` (§1 Architecture Decision, §9 Stack
  decision supersedes PR #1)
- `docs/adr/0002-bizzi-mvp-backend-stack-scope.md` (superseded by this ADR)
- `docs/adr/0003-controller-service-repository-layering.md`,
  `0004-workspace-scoped-multi-tenancy.md`,
  `0005-audit-first-mutations.md`,
  `0006-authorization-model-mvp.md` (carried over, stack-agnostic)
- `docs/adr/README.md` (ADR immutability / supersession rule)
