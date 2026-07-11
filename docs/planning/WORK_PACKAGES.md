# Bizzi Platform Backend — Work Package Register

Companion to `DEVELOPMENT_PLAN.md`. WP IDs for Phase 0, 1, and 3 mirror the
step numbers in `30_BACKEND_IMPLEMENTATION_PLAN/06_MODULE_IMPLEMENTATION_SEQUENCE.md`
1:1. Phase 2 WPs (90s) are cross-cutting quality gates with no module-sequence
equivalent.

Every WP inherits the Definition of Ready / Definition of Done /
Governance gate defined in `DEVELOPMENT_PLAN.md` §6–§8 — not repeated per WP
below.

## Summary table

| WP | Name | Phase | Depends on | Primary source docs |
|---|---|---|---|---|
| WP-00 | Backend scaffold | 0 | — | `03_REPOSITORY_STRUCTURE.md`, `10_LOCAL_DEVELOPMENT_WORKFLOW.md` |
| WP-01 | Config module | 0 | WP-00 | `01_TECH_STACK_DECISION.md` |
| WP-02 | Database module (Prisma + baseline migration) | 0 | WP-01 | `01_TECH_STACK_DECISION.md`, `26_DOMAIN_MODEL/01_ENTITY_CATALOG.md` |
| WP-03 | Shared kernel module | 0 | WP-02 | `07_SERVICE_IMPLEMENTATION_GUIDE.md`, `08_REPOSITORY_IMPLEMENTATION_GUIDE.md`, ADR-0003 |
| WP-04 | Identity / auth stub module | 0 | WP-03 | `01_TECH_STACK_DECISION.md` (§Auth) |
| WP-05 | Workspace module | 1 | WP-04 | `02_MVP_VERTICAL_SLICE.md`, ADR-0004 |
| WP-06 | Authorization module | 1 | WP-05 | ADR-0006 |
| WP-07 | Validation module | 1 | WP-06 | `07_SERVICE_IMPLEMENTATION_GUIDE.md` |
| WP-08 | Audit module | 1 | WP-07 | ADR-0005 |
| WP-09 | Event module | 1 | WP-08 | ADR-0005 |
| WP-10 | Task module | 1 | WP-09 | `02_MVP_VERTICAL_SLICE.md` |
| WP-11 | Decision module | 1 | WP-09 | `02_MVP_VERTICAL_SLICE.md` |
| WP-12 | Memory module (minimal) | 1 | WP-09 | `02_MVP_VERTICAL_SLICE.md` |
| WP-13 | Dashboard module (minimal) | 1 | WP-10, WP-11 | `02_MVP_VERTICAL_SLICE.md` |
| WP-14 | Export module skeleton (optional) | 1 | WP-13 | `02_MVP_VERTICAL_SLICE.md` |
| WP-15 | Health module | 1 | WP-00 | `11_CI_CD_READINESS_PLAN.md` |
| WP-90 | Test suite build-out | 2 | WP-05..WP-15 | `09_TESTING_STRATEGY.md` |
| WP-91 | CI pipeline (`backend-ci.yml`) | 2 | WP-90 | `11_CI_CD_READINESS_PLAN.md` |
| WP-92 | Local dev runbook & Docker Compose finalization | 2 | WP-91 | `10_LOCAL_DEVELOPMENT_WORKFLOW.md` |
| WP-93 | MVP vertical-slice audit & go/no-go | 2 | WP-90, WP-91, WP-92 | `14_IMPLEMENTATION_CHECKLIST.md`, `12_IMPLEMENTATION_RISK_REGISTER.md` |
| WP-16 | Operating Map module (backlog) | 3 | WP-93 | `06_MODULE_IMPLEMENTATION_SEQUENCE.md` |
| WP-17 | Function & Responsibility module (backlog) | 3 | WP-16 | ″ |
| WP-18 | Process module (backlog) | 3 | WP-17 | ″ |
| WP-19 | Agent module (backlog, governance-sensitive) | 3 | WP-18 | ″, `01_GOVERNANCE/AUTHORITY_MATRIX.md` |
| WP-20 | Integration module (backlog) | 3 | WP-19 | ″ |
| WP-21 | Security module (backlog) | 3 | WP-20 | ″ |
| WP-22 | Advanced Export module (backlog) | 3 | WP-21 | ″ |
| WP-23 | Advanced Dashboard module (backlog) | 3 | WP-22 | ″ |

## Phase 0 — Foundations

### WP-00 Backend scaffold
- **Deliverables**: `backend/` folder per `03_REPOSITORY_STRUCTURE.md`; `package.json` (pnpm); `tsconfig.json`; ESLint/Prettier config; `.env.example`; Docker Compose with Postgres dev (5432) and test (5433) services.
- **Acceptance**: `pnpm install` and `pnpm build` succeed on a clean checkout; nothing else builds yet.

### WP-01 Config module
- **Deliverables**: `ConfigModule` reading `DATABASE_URL, NODE_ENV, PORT, DEV_AUTH_MODE, JWT_SECRET`.
- **Acceptance**: app boots with a validated, typed config object; missing required env var fails fast at startup.

### WP-02 Database module
- **Deliverables**: `DatabaseModule` (Prisma provider), initial `schema.prisma` for MVP Priority-1 entities (`User, Session, CompanyWorkspace, WorkspaceSettings, Task, Decision, MemoryEntry, AuditEvent, RuntimeEvent, DashboardMetric`, and `WorkspaceSettings`), first committed migration via `prisma migrate dev`.
- **Acceptance**: `prisma migrate deploy` succeeds against a clean database in CI-equivalent conditions; no manual schema edits outside migrations (per coding standards).

### WP-03 Shared kernel module
- **Deliverables**: base error classes (`UnauthenticatedError, ForbiddenError, NotFoundError, WorkspaceArchivedError, ValidationError, InvalidObjectReferenceError, InvalidStatusTransitionError, BusinessRuleViolationError, ConflictError`), DTO base classes, `TransactionManager`, mapper utilities, shared constants.
- **Acceptance**: no feature module needs to redefine an error type or transaction pattern; `SharedKernelModule` imports nothing from `modules/`.

### WP-04 Identity / auth stub module
- **Deliverables**: dev-mode identity stub producing `ActorContext` (`actor_id`, `actor_type`) behind a JWT-compatible interface.
- **Acceptance**: every downstream service receives a typed `ActorContext`; swapping the stub for a real provider (Auth0/Clerk/Supabase) later requires no call-site changes.

## Phase 1 — MVP Vertical Slice ("Workspace Execution Loop v0.1")

### WP-05 Workspace module
- **Deliverables**: `CompanyWorkspace`, `WorkspaceSettings` CRUD-lite, Controller→Service→Repository per ADR-0003.
- **Acceptance**: workspace is creatable/readable/updatable; every later module's repository methods are workspace-scoped (ADR-0004); code-review checklist passed.

### WP-06 Authorization module
- **Deliverables**: `AuthorizationService`, owner-only checks for MVP, RBAC-ready shape (ADR-0006).
- **Acceptance**: no service/controller special-cases "owner" logic outside `AuthorizationService`; a forbidden action returns `ForbiddenError` and is audited.

### WP-07 Validation module
- **Deliverables**: `ValidationService` for business-rule validation, separate from DTO-level `class-validator` checks.
- **Acceptance**: status-transition and object-reference rules live in `ValidationService`, not in controllers or repositories.

### WP-08 Audit module
- **Deliverables**: `AuditService`, `AuditActions` constants (ADR-0005).
- **Acceptance**: no module writes an audit row by any path other than `AuditService.record(...)`.

### WP-09 Event module
- **Deliverables**: `RuntimeEventService` (ADR-0005).
- **Acceptance**: every mutation in WP-10..WP-13 emits a runtime event after successful commit.

### WP-10 Task module
- **Deliverables**: Task create/complete, canonical CSR flow (see `docs/c4/C4_DYNAMIC_CANONICAL_FLOW.md`).
- **Acceptance**: authorization, validation, transaction, audit, and event steps are all present and tested; matches `07_SERVICE_IMPLEMENTATION_GUIDE.md`.

### WP-11 Decision module
- **Deliverables**: Decision create/confirm.
- **Acceptance**: same as WP-10, applied to Decision lifecycle.

### WP-12 Memory module (minimal)
- **Deliverables**: `MemoryEntry` create/activate only — no semantic search (excluded from MVP).
- **Acceptance**: matches `02_MVP_VERTICAL_SLICE.md` exclusions; no scope creep into semantic memory.

### WP-13 Dashboard module (minimal)
- **Deliverables**: `DashboardMetric` read endpoint(s) — no custom dashboards (excluded from MVP).
- **Acceptance**: reads are workspace-scoped and paginated per `28_API_CONTRACTS/01_API_DESIGN_PRINCIPLES.md`.

### WP-14 Export module skeleton (optional)
- **Deliverables**: `ExportFileStorage` interface only, no real file generation (excluded from MVP).
- **Acceptance**: interface exists and is unused/no-op; does not block the vertical slice if deferred entirely.

### WP-15 Health module
- **Deliverables**: liveness/readiness endpoints.
- **Acceptance**: used by CI (WP-91) and local Docker Compose healthchecks.

## Phase 2 — Quality Gates

### WP-90 Test suite build-out
- **Deliverables**: unit, service, repository, API/e2e, transaction, security, and audit/runtime-event tests per `09_TESTING_STRATEGY.md`.
- **Acceptance**: all P1 routes from `02_MVP_VERTICAL_SLICE.md`, all MVP services/repositories, all lifecycle transitions, and all authorization-failure paths have test coverage. No numeric % target — "meaningful scenario coverage."

### WP-91 CI pipeline
- **Deliverables**: `.github/workflows/backend-ci.yml` — install, lint, typecheck, unit/repository/API tests, build, against a Postgres service container with `prisma validate/generate/migrate deploy`.
- **Acceptance**: pipeline is green on a clean PR; matches the skeleton in `11_CI_CD_READINESS_PLAN.md` §23; Phase 2+ deployment stages (Docker, staging, production) remain explicitly out of scope.

### WP-92 Local dev runbook & Docker Compose finalization
- **Deliverables**: finalized `10_LOCAL_DEVELOPMENT_WORKFLOW.md`-aligned Docker Compose, seed script, `pnpm dev/test/lint/typecheck/build` all working end to end.
- **Acceptance**: a new contributor can clone, `docker compose up`, `pnpm db:seed`, `pnpm dev`, and hit a working API within one runbook read-through.

### WP-93 MVP vertical-slice audit & go/no-go
- **Deliverables**: an audit pass against every readiness level in `14_IMPLEMENTATION_CHECKLIST.md` (Level 0–8) and every Critical/High risk in `12_IMPLEMENTATION_RISK_REGISTER.md`.
- **Acceptance**: no Stop Condition active; all Critical risks have a mitigation in place or an explicit accepted-risk sign-off from the project owner. This WP is the gate for Phase 3 — do not start WP-16 before this passes.

## Phase 3 — Post-MVP Expansion (backlog)

Not detailed further here; each WP-16..WP-23 gets its own Definition of Ready
pass (including a fresh governance-gate check per `DEVELOPMENT_PLAN.md` §7)
when Phase 3 is actually greenlit. **WP-19 (Agent module) is explicitly
flagged**: it introduces AI agents acting under delegated authority
(`01_GOVERNANCE/AUTHORITY_MATRIX.md` A0–A7) and is very likely to trip the
L3+/A3+ consult trigger on its own — plan for a human governance review
before scoping it, not just before coding it.
