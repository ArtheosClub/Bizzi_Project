---
name: bizzi-pre-merge-check
description: Mandatory checklist to run before merging or pushing any Bizzi Platform backend code to a shared git branch, and before deleting any merged branch. Verifies coding-standards compliance, test coverage, workspace scoping, audit/event wiring, ADR bookkeeping, that no Stop Condition is active, and that a branch's content is provably on main before it is deleted. Use immediately before every `git merge`, `git push` to a shared branch, PR merge that touches backend/ or docs/adr, docs/c4, docs/planning, or branch cleanup.
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
- [ ] Migrations apply cleanly to a fresh database (`uv run alembic upgrade
      head`; `uv run alembic upgrade --sql head` validates the chain with no
      database available).
- [ ] CI is green, not "green after a retry that masked a flake."
- [ ] No test was skipped or weakened to make this change pass.

If any box is unchecked, **stop** — this is a hard gate, not a judgment
call.

## 2. Coding standards (`30_BACKEND_IMPLEMENTATION_PLAN/13_BACKEND_CODING_STANDARDS.md` §27)

- [ ] Routers/endpoints contain no ORM calls, no repository calls, no business
      rules, no direct audit/event emission (ADR-0003).
- [ ] Services never return raw ORM records or bypass `workspace_id`.
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
- [ ] If this change adds/removes a container or Python package/router, or changes
      which services call which, the relevant `docs/c4/` diagram is updated
      in the same change.
- [ ] If this change affects a WP's scope, `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`
      is updated (status, acceptance criteria, or a note).

## 5. Scope discipline

- [ ] This change stays within the WP it claims to implement — no
      unrelated modules, tables, or endpoints snuck in (R-SCOPE-001).
- [ ] Nothing in `02_MVP_VERTICAL_SLICE.md`'s explicit exclusion list
      (full RBAC, agent recommendation application, process engine,
      operating map generation, semantic memory search, custom dashboards,
      etc.) has been quietly implemented ahead of its Phase 3 WP.

Only after every relevant box above is checked: merge.

## 6. After merging — verify before deleting the branch

Do not delete a branch on the strength of GitHub's "merged" label or a
recollection that it was merged. Verify against current remote state, per
the Repository Synchronization Rule in `CLAUDE.md`:

```
git fetch --all --prune
git merge-base --is-ancestor origin/<branch> origin/main
```

**If it exits 0** — every commit on the branch is reachable from `main`.
Delete it, no further questions.

**If it exits 1** — the branch's commits are not ancestors of `main`. This
does *not* mean the work is missing, and it is *not* a block on deletion.
A rebased or squashed branch has different SHAs on `main` carrying the same
content, so it can never satisfy the check no matter how long it is kept.
Before deleting, state explicitly **where the content landed** — the PR
number or the commit on `main` that carries it — and record that statement
wherever the deletion is being tracked (PR comment, cleanup list, or the
session's report to the project owner).

If you cannot identify where the content landed, that is the one case to
stop and ask. An unexplained non-ancestor branch is the only kind whose
deletion actually loses something.

This exists because "merged" is a label and ancestry is a fact, and because
the seven branches consolidated into PR #8 were rebased — their original
SHAs are not on `main` even though all of their content is. A one-stage
check would have refused to ever clear them.
