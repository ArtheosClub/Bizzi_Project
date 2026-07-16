# ADR-0002: Scope the Bizzi Platform MVP backend to TypeScript/NestJS/PostgreSQL/Prisma

- Status: Superseded by ADR-0007
- Date: 2026-07-11
- Deciders: Engineering (scope conflict surfaced during development-plan authoring; flagged for project-owner visibility — see Consequences)
- Governance level: L3 (architecture/tech-stack scoping decision — see note below)

## Context

Two tech stacks appear in this repository at different altitudes, and
nothing in the corpus reconciles them:

1. `10_IMPLEMENTATION/TARGET_TECH_STACK.md` and `TARGET_ARCHITECTURE.md` —
   branded **"Art of Business"**, the long-term platform-wide stack for the
   full multi-agent enterprise OS: Python, FastAPI, LangGraph orchestration,
   Neo4j knowledge graph, Qdrant vector DB, Kafka event bus, Kong API
   gateway, Keycloak identity, HashiCorp Vault, Kubernetes/Terraform/AWS EKS.
   This is vision-level — no execution-level detail (no repo structure,
   module sequence, testing strategy, or coding standards) exists for it
   anywhere in the repository.
2. `30_BACKEND_IMPLEMENTATION_PLAN/01_TECH_STACK_DECISION.md` — branded
   **"Bizzi Platform"**, scoped explicitly to "MVP backend implementation":
   TypeScript, Node.js LTS, NestJS, PostgreSQL, Prisma. Layers 31
   (Implementation Execution), 32 (Codebase Build), and 33 (Source Code
   Implementation) — roughly 47 documents — are all built on top of this
   decision.

Building actual service code requires picking one. Proceeding without
recording this explicitly risks silently locking in a stack choice that
contradicts the platform-wide vision without anyone having agreed to that.

## Decision

All service coding under `docs/planning/DEVELOPMENT_PLAN.md` and
`docs/planning/WORK_PACKAGES.md` targets the **Bizzi Platform MVP backend**
as specified in `30_BACKEND_IMPLEMENTATION_PLAN/01_TECH_STACK_DECISION.md`:
TypeScript, NestJS, PostgreSQL, Prisma. The Art of Business platform-wide
stack remains the long-term target architecture for the full enterprise OS
and is explicitly **out of scope** for this backend build.

Should the two need to converge later — e.g., the Bizzi backend becoming one
service inside the Art of Business platform, or the platform's Python agent
runtime calling into Bizzi's NestJS API — that convergence requires its own
ADR before either stack is changed. This ADR does not attempt to resolve
that; it only unblocks near-term coding.

## Consequences

- Unblocks Phase 0 of the development plan immediately, on the only layer of
  the spec corpus with execution-level detail.
- Risk, tracked and accepted rather than hidden: a future integration
  between Bizzi's NestJS API and an Art of Business Python agent runtime may
  require an adapter layer, a protocol translation, or in the worst case a
  rewrite decision. This is not resolved here.
- **This scope decision is made explicit here specifically for project-owner
  visibility.** It documents the de facto reality already reflected by the
  extensive work in layers 30–33, rather than silently picking a side. If
  this contradicts intent — e.g., if the Bizzi backend was meant to be
  written in Python from the start — raise it before Phase 0 of
  `DEVELOPMENT_PLAN.md` begins; reversing this after Phase 1 ships would mean
  discarding working code.

## Alternatives considered

- Build directly against the platform-wide Python/FastAPI/Kubernetes stack —
  rejected: no execution-level detail exists for it (vision docs only); the
  MVP vertical-slice plan (`02_MVP_VERTICAL_SLICE.md`) and every downstream
  execution/build/source-code doc already assume NestJS/Prisma.
- Treat the conflict as fully blocking and halt all coding pending owner
  resolution — considered, but 30_BACKEND_IMPLEMENTATION_PLAN is the only
  layer with enough detail to build from, and 31–33 already represent
  significant specification investment on top of it; proceeding on it while
  flagging the conflict loudly (this ADR, plus `DEVELOPMENT_PLAN.md` §2) is
  more useful than stalling.

## References

- `10_IMPLEMENTATION/TARGET_TECH_STACK.md`, `10_IMPLEMENTATION/TARGET_ARCHITECTURE.md`
- `30_BACKEND_IMPLEMENTATION_PLAN/01_TECH_STACK_DECISION.md`
- `docs/planning/DEVELOPMENT_PLAN.md` §2
