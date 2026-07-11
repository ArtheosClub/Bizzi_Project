# Architecture Decision Records (ADR)

This directory records architecture decisions for **service coding** on the
Bizzi Platform backend — the actual TypeScript/NestJS implementation, not the
enterprise-wide specification corpus (`00_RELEASE` … `50_IMPLEMENTATION`).
Those numbered directories describe *what the system should be*; ADRs record
*why we built it a specific way*, tied to git history.

## When an ADR is required

Write an ADR before merging code whenever the change is:

- An architectural or cross-module decision (per `01_GOVERNANCE/GOVERNANCE_MODEL.md`,
  decision level **L3 or higher**).
- A choice among real alternatives, not a mechanical application of an
  already-decided pattern.
- Something the Risk Register (`30_BACKEND_IMPLEMENTATION_PLAN/12_IMPLEMENTATION_RISK_REGISTER.md`)
  flags under **R-ARCH-001 / R-ARCH-002** (architecture drift / CSR boundary
  violation) — i.e. any change to the layering, authorization model, tech
  stack, or a service/repository contract other module code depends on.

Routine module implementation that follows an already-accepted ADR or the
`06_MODULE_IMPLEMENTATION_SEQUENCE.md` plan does **not** need a new ADR.

See the `bizzi-write-adr` skill (`.claude/skills/bizzi-write-adr/SKILL.md`)
for the step-by-step procedure.

## Format

[Michael Nygard's ADR format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions),
one decision per file. Template: `0000-adr-template.md`.

## Numbering and lifecycle

- Sequential, zero-padded 4 digits: `0001-`, `0002-`, …
- Status is one of: `Proposed`, `Accepted`, `Superseded by ADR-XXXX`, `Deprecated`.
- **ADRs are immutable once Accepted.** To change a decision, write a new
  ADR that supersedes it; do not edit the old one except to update its
  Status line.

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted |
| [0002](0002-bizzi-mvp-backend-stack-scope.md) | Scope the Bizzi Platform MVP backend to TypeScript/NestJS/PostgreSQL/Prisma | Accepted |
| [0003](0003-controller-service-repository-layering.md) | Controller-Service-Repository layering enforced by import boundaries | Accepted |
| [0004](0004-workspace-scoped-multi-tenancy.md) | Workspace as root aggregate / mandatory multi-tenant scoping | Accepted |
| [0005](0005-audit-first-mutations.md) | Audit-first mutations via AuditService + RuntimeEventService | Accepted |
| [0006](0006-authorization-model-mvp.md) | Owner-only authorization for MVP, RBAC-ready extension path | Accepted |
