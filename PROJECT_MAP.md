# Project Map

Pure navigation, by task. `CLAUDE.md` is the actual authority — this file
just points at it faster. If this map and a source document disagree, the
source document wins.

## If you're implementing a Work Package

1. `docs/planning/PRE-CODING-BRIEF.md` — Gate structure, build order.
2. `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` — current WP-level detail.
   **Use this one.**
   **`docs/planning/WORK_PACKAGES.md` is SUPERSEDED — do not use it; it
   carries stale WP definitions.**
3. `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md` — expanded WP entries.
4. Invoke the `bizzi-consult-before-coding` skill before writing any code.

## If you're making an architectural decision

1. `00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md` §3 — the authority
   hierarchy: which document wins when artifacts conflict.
2. `00_ARCHITECTURE/01_DOMAIN/ADW_01_DECISION_REGISTER.md` — the approved
   D01–D10 decisions. D10 §6 indexes lifecycle *capabilities* per concept,
   not status *values* — read it directly, don't infer from a search hit.
3. `docs/adr/README.md` — the ADR index; then the specific ADR
   (`docs/adr/0007-*.md` is the current backend-stack ADR; `0002-*.md` is
   superseded, kept only as historical record).
4. Invoke the `bizzi-write-adr` skill to record the decision.

## If you're creating a module

1. `60_MODULE_SPECIFICATIONS/MODULE_INDEX.md` — existing module specs.
2. `30_BACKEND_IMPLEMENTATION_PLAN/13_BACKEND_CODING_STANDARDS.md` —
   coding rules (principles are stack-agnostic per ADR-0003; literal
   NestJS syntax in that doc is not).
3. `docs/c4/C4_DYNAMIC_CANONICAL_FLOW.md` — the canonical mutation flow.

## If you're auditing or reviewing

1. `docs/planning/AUDIT_2026-07-26_TWO_WEEK_REVIEW.md` and
   `docs/planning/RKM_AUDIT_2026-07-26.md` — most recent audits on `main`.
2. `01_GOVERNANCE/GOVERNANCE_MODEL.md`, `01_GOVERNANCE/AUTHORITY_MATRIX.md`
   — governance/escalation rules. **Use the `01_GOVERNANCE/` copy.** A
   root-level `GOVERNANCE_MODEL.md` also exists and is a content-divergent
   duplicate (different scope, different length, not a synced pair) —
   flagged by the RKM audit; do not treat it as current.
3. Invoke the `bizzi-pre-merge-check` skill before recommending a merge.

## Deferred and rejected architectural work

`docs/planning/DEFERRED_ARCHITECTURE_INITIATIVES.md` — proposed
improvements deliberately not built yet, with reopen conditions. Check
here before proposing new architectural tooling; it may already be
recorded and gated on a specific condition rather than open for a fresh
decision.
