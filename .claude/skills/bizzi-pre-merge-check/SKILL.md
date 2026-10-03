---
name: bizzi-pre-merge-check
description: Mandatory Bizzi Platform checklist before every git push to a shared branch (including first publication), git merge or PR merge involving backend/, docs/adr/, docs/c4/, docs/planning/, or project governance/skills, and before deleting a merged branch. Review stop conditions, scope, tests, audit/event obligations, and integration evidence. Apply checks to the change and publication stage; applicable PR-triggered CI must pass before merge, not before the first push needed to create the PR.
---

# Pre-merge check — Bizzi Platform

This review is mandatory before shared-branch pushes and merges, including
changes to `.claude/skills/` such as this checklist itself, and before
merged-branch deletion. Apply the scope and stage distinctions below.

Review the actual diff and current governing sources, not remembered status.
Follow the Repository Synchronization Rule in `CLAUDE.md` before branch
planning or merge recommendations. Use `git --no-optional-locks` for local
Git checks, especially status, to avoid optional index writes.

Record relevant checks as passed, failed, or not verified; mark an
inapplicable check N/A with a short reason. Missing evidence for an
applicable gate is not N/A. Match verification effort to the change:
documentation edits do not require inventing backend work or new CI.
Approved ADRs and amendments govern applicability; this checklist neither
changes their scope nor grants permission to push, merge, or delete.

Save one item-by-item review artifact in the external `workflow_BIZZI`
directory before the action under review. Identify the action, reviewed
revision (or uncommitted diff), and date. Give each checklist item and
applicable stage-specific gate a disposition plus a concise evidence
reference or reason; include N/A items rather than silently omitting them.
An existing review artifact may be updated or referenced: no separate file
per item is needed. The artifact records evidence, not action authorization.

## 1. Stop conditions and publication stage

Apply `30_BACKEND_IMPLEMENTATION_PLAN/14_IMPLEMENTATION_CHECKLIST.md` §20
and `docs/planning/DEVELOPMENT_PLAN.md` §9:

- [ ] Workspace isolation is not broken.
- [ ] Authorization is not bypassed where required by the approved scope.
      Required checks go through `AuthorizationService` (ADR-0006), not
      inline ownership-policy substitutes.
      Workspace filtering alone is not authorization; a persistence-only
      slice does not authorize deferred endpoints or access policy.
- [ ] Required mutation audit records are not missing.
- [ ] Raw secrets do not appear in logs, events, or API responses.
- [ ] Relevant migrations can apply to a clean database. For migration or
      persistence changes, use clean-database execution evidence;
      `alembic upgrade --sql head` generates SQL, not this proof.
- [ ] CI is not repeatedly failing without resolution; tests have not been
      skipped or weakened to force progress.
- [ ] AI-generated code is not repeatedly violating architecture boundaries.

An active stop condition pauses implementation. Resolve it or ask the owner;
delivery speed does not override it. A retry is not inherently a violation:
explain the failure and resolution rather than hiding an unresolved flake.

Distinguish publication from merge:

- Before a first feature-branch push, review applicable local evidence.
  If the workflow only runs for that branch after a PR exists, record CI
  as pending publication, not green. That absence alone does not prohibit
  the push needed to create the PR.
- Before merge, verify all applicable CI jobs required by the project or
  platform have completed successfully on the exact PR head. Missing,
  pending, failed, or unexpectedly skipped jobs do not satisfy this gate.
  Re-read `.github/workflows/backend-ci.yml` and any other current workflows;
  do not infer success from an empty check list or from an older head.
- If path filters intentionally exclude the entire change, record CI as
  not applicable and use relevant document checks (`git diff --check`,
  links, and parsing/rendering for changed diagrams). Do not claim a new
  backend test result. If a docs workflow applies, verify it too.
  Support this N/A with the workflow path and revision, relevant event/path
  filters, and changed paths showing why no applicable trigger matches.

## 2. Current-stack coding standards

Use ADR-0007 (`docs/adr/0007-bizzi-mvp-backend-stack-python-fastapi.md`),
`backend/pyproject.toml`, and the stack-agnostic principles in
`30_BACKEND_IMPLEMENTATION_PLAN/13_BACKEND_CODING_STANDARDS.md`.
Historical TypeScript/NestJS syntax is not a Python naming requirement.

- [ ] Routers contain no ORM/repository calls, business rules, or direct
      audit/event emission (ADR-0003).
- [ ] Services do not return raw ORM records or bypass workspace scope.
- [ ] Repositories do not authorize, own lifecycle decisions, emit events,
      or return DTOs. Scoped entity lookups include workspace scope
      (ADR-0004); honor the approved contract for insert operations.
- [ ] Python modules/functions use snake_case and classes use PascalCase;
      Ruff and mypy requirements follow the current project configuration.
      Any typing escape has a concrete justification, not a blanket waiver.
- [ ] Error behavior follows the layer's approved contract. Do not force
      HTTP exception types or new error vocabulary into a repository or
      service-only slice; preserve ADR-0012's API boundary and no-leak
      contract when HTTP behavior is involved.

## 3. Tests and mutation obligations

Use the current WP acceptance criteria and Definition of Done, with
`30_BACKEND_IMPLEMENTATION_PLAN/09_TESTING_STRATEGY.md` for principles.

- [ ] New/changed P1 routes have API-level coverage; changed services and
      repositories have appropriate unit/service and persistence coverage.
- [ ] Lifecycle changes cover success, invalid transitions, and workspace
      isolation. Test authorization failures where authorization is in
      scope; do not implement deferred authorization merely to fill a box.
- [ ] Mutations prove required audit and transaction behavior under ADR-0005
      (`docs/adr/0005-audit-first-mutations.md`): audit through
      `AuditService.record(...)`, not direct audit-repository access from
      domain services, in the same transaction as the mutation.
- [ ] RuntimeEvent obligations follow ADR-0005 unless a specifically
      approved amendment defers them. Tests cover required post-commit
      emission; audit is not event emission.

For the A-12-bounded WP13 `create`/`archive`/`unarchive` slice, consult
Amendment A-12 in `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` and the
matching WP13 entry in `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md`:

- Mutation and audit share the caller's session/transaction. Neither
  module commits or rolls back; tests establish caller rollback behavior.
- RuntimeEvent emission is explicitly deferred, not completed or waived.
  Preserve the stated handoff to the work package delivering
  `RuntimeEventService` after ADW-07. Preserve A-12's source explanation
  and static tests excluding RuntimeEvent imports/calls from these modules.
- Do not generalize the deferral to other mutations or add API, delete,
  supersession, or actor-attribution work outside A-12. Use all of A-12's
  acceptance criteria, not just this summary.

Tie evidence to the reviewed source revision. If relevant bytes change
after a run, revalidate affected checks; do not present an older run as
covering untested code. A prose-only change need not trigger an unrelated
full test run.

## 4. Traceability and scope

- [ ] Architectural decisions have the required approval and ADR record
      (`bizzi-write-adr`); do not rewrite accepted decisions retroactively.
- [ ] Relevant C4 views reflect changed components/dependencies, with
      type dependencies distinguished from runtime calls. Render the
      actual document reviewed, not an uncommitted layout candidate.
- [ ] Work remains within its approved WP and explicit exclusions in
      `30_BACKEND_IMPLEMENTATION_PLAN/02_MVP_VERTICAL_SLICE.md` and current
      amendments. Scope changes require the governing approval process,
      not merely a status note in a register.
- [ ] Register updates follow their amendment rules. Historical snapshots
      retain their stated correction convention; do not silently rewrite
      a snapshot as a living status report.

Recommend merge only when applicable gates are satisfied and outstanding
non-blocking limitations are explicit. Performing the merge additionally
requires the owner's authorization; a recommendation does not grant it.
Keep documentation clarification distinct from new implementation claims.

## 5. After merging — verification is not deletion approval

For specifically authorized branch cleanup, refresh remote state and pin
the exact branch and main tips. Check ancestry against those tips:

```sh
git --no-optional-locks fetch --all --prune
git --no-optional-locks merge-base --is-ancestor origin/<branch> origin/main
```

- Exit 0 proves commit reachability, not permission to delete. Confirm the
  target is still the verified tip before deleting the authorized ref.
- Exit 1 is not proof of missing work: rebases and squash merges change
  commit identities. Inspect integration and remaining unique work;
  record where the content landed and why deletion preserves it. A PR's
  merged label alone is insufficient evidence.
  This preserves the reason for the alternative proof: integrated content
  can survive even when the original commits are not ancestors of main.
- Any other exit status is an error, not a negative ancestry result.
  If verification fails, the target moved, or integration remains unclear,
  stop cleanup and resolve that uncertainty.

Do not expand remote-branch cleanup into local-branch deletion, tracking
configuration changes, bundle removal, or object-store maintenance. Those
are separate actions with their own authorization and preservation needs.
