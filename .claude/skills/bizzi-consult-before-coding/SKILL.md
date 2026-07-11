---
name: bizzi-consult-before-coding
description: Mandatory pre-flight check before writing or editing any Bizzi Platform backend service code in this repository. Surfaces the governing tech-stack ADR, layering rules, coding standards, module-sequence position, and the governance/escalation gate that decides whether to proceed or stop and ask the project owner first. Use before starting any implementation task under backend/ or docs/planning/WORK_PACKAGES.md, and before creating a new module, table, or endpoint.
---

# Consult before coding — Bizzi Platform backend

This is the pre-flight check required by `docs/planning/DEVELOPMENT_PLAN.md`
§6-§7 (Definition of Ready + Governance gate) before writing any backend
service code.

## 1. Identify what you're about to build

- Find the Work Package this task belongs to in
  `docs/planning/WORK_PACKAGES.md`. If it doesn't map to an existing WP,
  that's already a signal — see step 3.
- Read the WP's listed source docs and acceptance criteria before touching
  code.

## 2. Read the four documents that govern all backend code

1. `docs/adr/0002-bizzi-mvp-backend-stack-scope.md` — this is TypeScript /
   NestJS / PostgreSQL / Prisma, not the platform-wide Python stack. If a
   task description implies otherwise, stop and confirm scope first.
2. `docs/adr/0003-controller-service-repository-layering.md` — Controller
   does DTO validation + delegation only. Service owns authorization,
   validation, transaction, audit, event emission. Repository is
   workspace-scoped persistence only. One-directional dependency.
3. `30_BACKEND_IMPLEMENTATION_PLAN/13_BACKEND_CODING_STANDARDS.md` — naming
   conventions, forbidden patterns (`any`, `@ts-ignore` without
   justification, raw Prisma records leaving a service, manual audit
   writes), and the §27 code-review checklist you will be held to.
4. `docs/c4/C4_DYNAMIC_CANONICAL_FLOW.md` — the exact call sequence
   (Controller→Service→Authorization→Validation→Transaction→Repository→Audit→Event→Response)
   every state-changing endpoint must follow.

## 3. Run the governance gate

Per `docs/planning/DEVELOPMENT_PLAN.md` §7, decide which bucket this task is
in:

**Proceed directly** if the task is routine implementation of a module
already named in `30_BACKEND_IMPLEMENTATION_PLAN/06_MODULE_IMPLEMENTATION_SEQUENCE.md`,
inside an approved WP, following the CSR pattern and coding standards.

**Stop and ask the project owner before writing any code** if any of these
are true:
- You're adding a module, table, or endpoint not named in
  `02_MVP_VERTICAL_SLICE.md` or `06_MODULE_IMPLEMENTATION_SEQUENCE.md`.
- The task changes the authorization model, the tech stack, or a
  service/repository contract other modules depend on.
- The task touches secrets, PII, or anything in
  `30_BACKEND_IMPLEMENTATION_PLAN/12_IMPLEMENTATION_RISK_REGISTER.md`'s
  Critical tier: R-DATA-001 (workspace isolation), R-SEC-001 (authorization
  bypass), R-TEST-001 (happy-path-only testing), R-AI-001 (AI code bypasses
  architecture), R-SCOPE-001 (scope creep).
- The task is part of Phase 3 / WP-19 (Agent module) — this is flagged in
  `docs/planning/WORK_PACKAGES.md` as needing a governance review before
  scoping even begins, because it introduces AI agents acting under
  delegated authority (`01_GOVERNANCE/AUTHORITY_MATRIX.md`, A0-A7).

When in doubt, the Governance Model's own rule applies: **Escalate > Review
> Approve > Execute.** Use `AskUserQuestion` rather than guessing.

## 4. Check for an existing ADR, or flag that one is needed

If step 3 concluded "architectural decision," check `docs/adr/README.md`'s
index first — it may already be decided. If not, this task needs an ADR
before merge: use the `bizzi-write-adr` skill once the decision is made (not
instead of asking the user if it's genuinely ambiguous).

## 5. Only then start coding

Follow the module folder layout in
`30_BACKEND_IMPLEMENTATION_PLAN/03_REPOSITORY_STRUCTURE.md` and the
diagrams in `docs/c4/`. When the task is done, run the
`bizzi-pre-merge-check` skill before merging.
