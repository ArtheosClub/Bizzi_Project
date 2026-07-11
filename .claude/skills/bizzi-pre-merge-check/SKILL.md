---
name: bizzi-pre-merge-check
description: Mandatory checklist to run before merging or pushing any Bizzi Platform backend code to a shared git branch. Verifies coding-standards compliance, test coverage, workspace scoping, audit/event wiring, ADR bookkeeping, and that no Stop Condition is active. Use immediately before every `git merge`, `git push` to a shared branch, or PR merge that touches backend/ or docs/adr, docs/c4, docs/planning.
---

# Pre-merge check — Bizzi Platform backend

Run through this in order. If any item fails, fix it or stop and ask the
user — do not merge past a failing item to "keep moving." Per
`docs/planning/DEVELOPMENT_PLAN.md` §9: "Stop conditions override delivery
speed."

## 1. Stop conditions — check these first (`14_IMPLEMENTATION_CHECKLIST.md` §20)

- [ ] No query or response crosses a `workspace_id` boundary.
- [ ] No authorization bypass exists (every mutating endpoint goes through
      `AuthorizationService`).
- [ ] No state-changing action is missing its `AuditService.record(...)` call.
- [ ] No raw secret, token, or password appears in logs, events, or
      responses.
- [ ] Migrations apply cleanly to a fresh database (`prisma migrate deploy`).
- [ ] CI is green, not "green after a retry that masked a flake."
- [ ] No test was skipped or weakened to make this change pass.

If any box is unchecked, **stop** — this is a hard gate, not a judgment
call.

## 2. Coding standards (`30_BACKEND_IMPLEMENTATION_PLAN/13_BACKEND_CODING_STANDARDS.md` §27)

- [ ] Controllers contain no Prisma calls, no repository calls, no business
      rules, no direct audit/event emission (ADR-0003).
- [ ] Services never return raw Prisma records or bypass `workspace_id`.
- [ ] Repositories never authorize, never own lifecycle rules, never emit
      events, never return DTOs.
- [ ] No bare `findById`/`updateById` without workspace scoping exists
      anywhere in the diff (ADR-0004).
- [ ] File/class/method naming matches convention (kebab-case files,
      PascalCase classes, camelCase methods, snake_case DB fields).
- [ ] No `any` or `@ts-ignore` without an inline justification.
- [ ] Errors thrown are shared-kernel types, not ad-hoc strings.

## 3. Tests (`30_BACKEND_IMPLEMENTATION_PLAN/09_TESTING_STRATEGY.md`)

- [ ] New/changed P1 routes have API-level test coverage.
- [ ] New/changed services and repositories have unit/service-level test
      coverage.
- [ ] Every new lifecycle transition (e.g. task complete, decision confirm)
      has a test for both the success path and at least one
      authorization-failure path.
- [ ] Any new mutation has a test asserting the audit event and runtime
      event were both emitted.

## 4. Traceability

- [ ] If this change made an architectural decision, an ADR exists for it
      (`bizzi-write-adr` skill) and is linked from the PR.
- [ ] If this change adds/removes a container or NestJS module, or changes
      which services call which, the relevant `docs/c4/` diagram is updated
      in the same change.
- [ ] If this change affects a WP's scope, `docs/planning/WORK_PACKAGES.md`
      is updated (status, acceptance criteria, or a note).

## 5. Scope discipline

- [ ] This change stays within the WP it claims to implement — no
      unrelated modules, tables, or endpoints snuck in (R-SCOPE-001).
- [ ] Nothing in `02_MVP_VERTICAL_SLICE.md`'s explicit exclusion list
      (full RBAC, agent recommendation application, process engine,
      operating map generation, semantic memory search, custom dashboards,
      etc.) has been quietly implemented ahead of its Phase 3 WP.

Only after every relevant box above is checked: merge.
