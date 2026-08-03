# Bizzi Project — instructions for Claude Code

For fast navigation by task ("I'm implementing a WP", "I'm making an
architectural decision", "I'm creating a module", "I'm auditing") see
`PROJECT_MAP.md` at the repo root. It is pure navigation — this file
remains the actual authority when the two differ.

## What this repository is

Two things live here at different altitudes:

1. **The Art of Business specification** — an enormous, largely complete
   architectural spec (`00_RELEASE` … `50_IMPLEMENTATION`, plus root-level
   `PB0xx_*.md` playbooks) for an AI-orchestrated enterprise operating
   system. Treat this as read-mostly reference material. Changes to
   `CAPABILITY_MAP`, `GOVERNANCE_MODEL`, or `AGENT_REGISTRY` require the
   project owner's explicit sign-off (see root `README.md`, "Contributing").
2. **The Bizzi Platform MVP backend build** — the actual Python/FastAPI
   service this repo is being coded toward (ADR-0007; supersedes the
   original NestJS/TypeScript scope in ADR-0002), planned in
   `docs/planning/` and `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`,
   decided in `docs/adr/`, and diagrammed in `docs/c4/`. **Gate B
   (Engineering Foundation) is done and merged to `main`** — see
   `backend/`. **Gate C (Platform Backbone) is next** — see
   `docs/planning/PRE-CODING-BRIEF.md` §8 and
   `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` (WP13–WP22) for scope.
   Domain semantics for Gate C — what a concept means, who owns it, how
   it relates to others, how it ends — are governed by `00_ARCHITECTURE/`
   (the Architecture Decision Workshop, ADW-01, decisions D01–D10). This
   file does not restate that hierarchy; see
   `00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md` §3 for the full,
   approved authority hierarchy governing which document wins when
   artifacts conflict.

If a task is ambiguous about which of the two it concerns, ask before
proceeding — editing spec prose and writing service code are governed by
different rules (below).

## Mandatory: before any repository-wide analysis, triage, or merge decision

**Repository Synchronization Rule.** Before any of the following, the agent
SHALL synchronize with current remote state:

- repository-wide analysis or audit;
- branch planning or triage;
- conflict analysis;
- a merge or close recommendation for any pull request or branch.

"Synchronize" means, at minimum: run `git fetch --all`; re-check the actual
current status of every pull request and branch named in the plan (open /
closed / merged, and its commits-ahead/behind count); and treat any earlier
snapshot — **including this session's own prior messages, prior audits, and
prior tool output** — as potentially stale rather than as current truth.

This rule exists because repository state changes outside the agent's
session: the project owner or another session may merge, close, or push
directly at any time. It is not a style preference. On 2026-07-27, pull
request #2 was merged by the project owner; a later step in the same agent
session treated it as still open, and opened two pull requests against a
stale `main`. One of them (#6) would have reverted that merge — restoring
two superseded NestJS-era C4 diagrams and deleting
`docs/planning/GATE_A_PRODUCT_DEFINITION.md` — had it been merged rather
than caught.

Stale-state analysis is a Stop Condition in its own right: if a plan's
premises cannot be re-verified against current remote state, halt and
re-derive them rather than proceeding on the earlier snapshot.

## Mandatory: before writing or editing any backend service code

Invoke the `bizzi-consult-before-coding` skill (or read, at minimum,
`docs/planning/DEVELOPMENT_PLAN.md` §6-§7, `docs/adr/0007-*.md`
(Python/FastAPI stack — supersedes `docs/adr/0002-*.md`, kept only as
historical record), `docs/adr/0003-*.md`,
`30_BACKEND_IMPLEMENTATION_PLAN/13_BACKEND_CODING_STANDARDS.md` (principles
apply stack-agnostically per ADR-0003; literal NestJS syntax in that doc
does not), `docs/c4/C4_DYNAMIC_CANONICAL_FLOW.md`, and — for Gate C work
specifically — `00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md` and the
approved ADW-01 decisions (D01–D10) for the governing domain semantics.
This is not optional
housekeeping — `30_BACKEND_IMPLEMENTATION_PLAN/12_IMPLEMENTATION_RISK_REGISTER.md`
names R-AI-001 ("AI-generated code bypasses architecture") as a Critical
risk specifically because AI coding agents skip exactly this step under
time pressure.

The governance gate in `docs/planning/DEVELOPMENT_PLAN.md` §7 decides
whether to proceed directly or stop and consult the project owner first.
When in doubt: **Escalate > Review > Approve > Execute**
(`01_GOVERNANCE/GOVERNANCE_MODEL.md`) — use `AskUserQuestion`, don't guess.

## Mandatory: before merging or pushing to a shared branch

Run the `bizzi-pre-merge-check` skill in full. It checks Stop Conditions,
coding-standards compliance, test coverage, workspace-scoping, audit/event
wiring, and ADR/C4 bookkeeping. Do not merge past a failed check to keep
moving — per `docs/planning/DEVELOPMENT_PLAN.md` §9, "stop conditions
override delivery speed."

## Mandatory: when a coding task involves an architectural decision

Use the `bizzi-write-adr` skill. An ADR is required whenever a change is
L3+ per `01_GOVERNANCE/GOVERNANCE_MODEL.md`, is a real choice among
alternatives, or touches anything `12_IMPLEMENTATION_RISK_REGISTER.md`
flags as architecture drift (R-ARCH-001/002). See `docs/adr/README.md` for
the full trigger list. Never silently make an architectural call and move
on — write it down first.

## Mandatory: before introducing a new architectural abstraction

**Abstraction Justification Rule.** A new architectural abstraction must
either solve an existing, demonstrated problem, or be a necessary
precondition for implementing the next Work Packages. Anticipated future
need is not sufficient justification.

This is a stop condition, not advice — same register as the Repository
Synchronization Rule above. It would have caught the Epoch IV package and
the `70_` Engineering Specification layer before they were written (see
the RKM audit's Step 5, finding #4). A backend-code-specific counterpart
to this rule already exists: the `bizzi-consult-before-coding` skill's
Architecture Review Checklist, §3 — this rule is the repo-wide version,
not limited to backend code.

Anticipated-future-need ideas are not simply dropped: record them in
`docs/planning/DEFERRED_ARCHITECTURE_INITIATIVES.md` with a concrete
reopen condition instead of building them now.

### Convention: Purpose header for new architectural documents

New architectural documents (not code, not every markdown file) open
with:

```
Purpose · Why this exists · What it changes ·
Affected modules · Affected Work Packages · Affected code
```

Applies to documents created or substantially edited from now on. No
retrofit pass across the existing corpus.

## Non-negotiable stop conditions

Halt immediately (don't push through for delivery speed) if any of these
show up, per `30_BACKEND_IMPLEMENTATION_PLAN/14_IMPLEMENTATION_CHECKLIST.md` §20:

- A query or response crosses a `workspace_id` boundary.
- An authorization bypass is found.
- A state-changing action is missing its audit event.
- A raw secret, token, or password appears in logs, events, or responses.
- A migration fails against a clean database.
- CI is repeatedly failing, or a test is being skipped to force progress.

## Implementation Baseline

The repository is in the Implementation Phase, per
`00_ARCHITECTURE/00_GOVERNANCE/DECISION_0003_IMPLEMENTATION_BASELINE.md`.

- **Current baseline branch**: `main`.
- **Current baseline commit**: `576465f15d8e35656ad8ff3f6ed5e954ebb74fe8`.
- **Architecture is frozen.** Architecture, vocabulary, the domain model,
  repository structure, technology stack, engineering methodology,
  layering, the Authority Hierarchy, and governance are all frozen per
  DECISION_0003 §7.
- **No architectural redesign is authorized** outside the Architecture
  Change Process (DECISION_0003 §11): Architecture Change Request →
  Architecture Review → Architecture Approval → Architecture Decision →
  Implementation. No exception.
- Every implementation pull request must reference the applicable Work
  Package(s), the applicable ADR(s), `50_IMPLEMENTATION/ENGINEERING_BASELINE.md`,
  and DECISION_0003 itself (DECISION_0003 §10).

## Key entry points

| Need | Read |
|---|---|
| What to build next | `docs/planning/PRE-CODING-BRIEF.md` (Gate structure), `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` (WP-level detail — **use this one**), `docs/planning/DEVELOPMENT_PLAN.md` (governance gates). **`docs/planning/WORK_PACKAGES.md` is SUPERSEDED — do not use it; it carries stale WP definitions.** |
| What a domain concept means (Gate C v1.1) | `00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md` (authority hierarchy), `00_ARCHITECTURE/01_DOMAIN/ADW_01_DECISION_REGISTER.md` (D01–D10, the approved decisions) |
| Why something was built a certain way | `docs/adr/` |
| How the system fits together | `docs/c4/` |
| Exact coding rules | `30_BACKEND_IMPLEMENTATION_PLAN/13_BACKEND_CODING_STANDARDS.md` |
| Business/architecture spec | root `README.md`, `Vision.md` |
| Governance/escalation | `01_GOVERNANCE/GOVERNANCE_MODEL.md`, `01_GOVERNANCE/AUTHORITY_MATRIX.md` |

## Language convention

Business/architecture spec documents (root-level, `00_RELEASE` …
`50_IMPLEMENTATION`) are written in Russian. Engineering-process artifacts
for actual service coding (`docs/adr/`, `docs/c4/`, `docs/planning/`,
coding-standards docs) are in English, matching layers 29-33. Match the
existing language of whichever file you're editing.
