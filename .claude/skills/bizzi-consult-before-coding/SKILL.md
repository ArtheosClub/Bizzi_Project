---
name: bizzi-consult-before-coding
description: Mandatory pre-flight check before writing or editing any Bizzi Platform backend service code in this repository. Surfaces the governing tech-stack ADR, layering rules, coding standards, module-sequence position, and the governance/escalation gate that decides whether to proceed or stop and ask the project owner first. Use before starting any implementation task under backend/ or 50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md, and before creating a new module, table, or endpoint.
---

# Consult before coding — Bizzi Platform backend

This is the pre-flight check required by `docs/planning/DEVELOPMENT_PLAN.md`
§6-§7 (Definition of Ready + Governance gate) before writing any backend
service code.

## 1. Identify what you're about to build

- Find the Work Package this task belongs to in
  `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` (the current register —
  `docs/planning/WORK_PACKAGES.md` is superseded), and its expanded entry in
  `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md`. If it doesn't map to an existing WP,
  that's already a signal — see step 4.
- Read the WP's listed source docs and acceptance criteria before touching
  code.

## 2. Read the four documents that govern all backend code

1. `docs/adr/0007-bizzi-mvp-backend-stack-python-fastapi.md` — this is
   Python / FastAPI / PostgreSQL / SQLAlchemy + Alembic. It supersedes
   ADR-0002 (TypeScript/NestJS/Prisma), which is retained only as a
   historical record. If a task description implies the NestJS stack, stop
   and confirm scope first.
2. `docs/adr/0003-controller-service-repository-layering.md` — read
   "Controller" as "Router/Endpoint" for FastAPI, per that ADR's own
   terminology note. The Router/Endpoint does DTO validation + delegation only. Service owns authorization,
   validation, transaction, audit, event emission. Repository is
   workspace-scoped persistence only. One-directional dependency.
3. `30_BACKEND_IMPLEMENTATION_PLAN/13_BACKEND_CODING_STANDARDS.md` — naming
   conventions, forbidden patterns (`any`, `@ts-ignore` without
   justification, raw ORM records leaving a service, manual audit
   writes), and the §27 code-review checklist you will be held to. Its
   principles apply stack-agnostically per ADR-0003; its literal NestJS
   syntax does not.
4. `docs/c4/C4_DYNAMIC_CANONICAL_FLOW.md` — the exact call sequence
   (Router/Endpoint→Service→Authorization→Validation→Transaction→Repository→Audit→Event→Response)
   every state-changing endpoint must follow.

## 3. Run the Architecture Review Checklist — and write the answers down

Four questions, before implementing any WP. **Answer all four explicitly in
the pre-coding plan and carry the answers into the PR description.** An
unwritten check is unprovable a month later, and "I considered it" is not
evidence that it was considered.

1. Does the implementation fully comply with D01–D10
   (`00_ARCHITECTURE/01_DOMAIN/`)?
2. Does it introduce any new domain concept?
3. Does it collapse any orthogonal dimensions defined by D07?
4. Does it make irreversible a decision that hasn't actually been made yet?

**If any answer is YES — stop and report before writing code.**

### Why this checklist exists

Three real cases were caught by luck rather than by process. Each maps to
one of the questions above, and each would have been caught systematically
if this checklist had existed:

- **Q3 — D07 vs. WP13's `status` field.** WP13's acceptance criteria name a
  `status` column, but D07 §6 (`APPROVED — CLOSED`) forbids collapsing
  Phase, Status, Outcome, Progress and Health into "one universal
  authoritative `status` field." Implementing WP13 literally would have
  breached a constitutional decision inside a frozen architecture. Found
  only because someone went looking for approved status values.
- **Q1 — ADR-0005 vs. a premature `WorkspaceService`.** WP12a's Definition
  of Done lists a service and repository, but ADR-0005 requires
  audit-inside-transaction for every state-changing service method, and
  `AuditService` does not exist until WP19. Writing the service would have
  either violated ADR-0005 or silently pulled WP19 forward.
- **Q4 — the model-aggregation `DROP TABLE` footgun.** `Base.metadata` is
  populated only as a side effect of importing a model's module. With no
  aggregation module, `alembic revision --autogenerate` reads real tables
  as ones that should not exist and emits `DROP TABLE` for them. Committing
  the first model without the aggregation in the same commit would have
  made a data-loss path the default, before anyone decided that was
  acceptable.

Note on Q4's wording: it deliberately asks about *irreversible decisions
not yet made*, not "does this reduce future flexibility." Nearly every
concrete decision narrows something, so the broader phrasing is too
subjective to function as a stop condition. Irreversibility is checkable.

## 4. Run the governance gate

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
  `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md` as needing a governance review before
  scoping even begins, because it introduces AI agents acting under
  delegated authority (`01_GOVERNANCE/AUTHORITY_MATRIX.md`, A0-A7).

When in doubt, the Governance Model's own rule applies: **Escalate > Review
> Approve > Execute.** Use `AskUserQuestion` rather than guessing.

## 5. Check for an existing ADR, or flag that one is needed

If step 4 concluded "architectural decision," check `docs/adr/README.md`'s
index first — it may already be decided. If not, this task needs an ADR
before merge: use the `bizzi-write-adr` skill once the decision is made (not
instead of asking the user if it's genuinely ambiguous).

## 6. Only then start coding

Follow the module folder layout in
`30_BACKEND_IMPLEMENTATION_PLAN/03_REPOSITORY_STRUCTURE.md` and the
diagrams in `docs/c4/`. When the task is done, run the
`bizzi-pre-merge-check` skill before merging.
