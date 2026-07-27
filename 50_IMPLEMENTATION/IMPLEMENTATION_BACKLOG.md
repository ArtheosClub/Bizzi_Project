# Implementation Backlog — Gate C / Gate D

Version: 1.0
Status: Planned
Scope: WP12a (new), WP13–WP32, per `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`
and the Epoch III Implementation Readiness Review.
Out of scope: Gate B (WP05–WP12, complete, merged to `main`) and Gate E
(WP33–WP39, post-demo polish).

This document does not modify `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`.
It adds one new work package (WP12a, the Planning Gap identified by the
Implementation Readiness Review) and expands WP13–WP32's existing entries
with the fields an engineering team needs to execute against, without
changing any existing WP's goal, dependency, or acceptance criteria.

**Blocked status key**: 🔴 Blocked (Critical Path — see
`IMPLEMENTATION_SEQUENCE.md`), 🟡 Blocked transitively (depends on a 🔴
item), 🟢 Unblocked.

---

## WP12a — Workspace Model 🟢

- **Goal**: implement the Workspace persistent entity — the primary
  tenancy boundary (D01, `APPROVED — CLOSED`) that every other Gate C
  entity's `workspace_id` foreign key references.
- **Dependencies**: WP07 (PostgreSQL), WP08 (ORM/migrations).
- **Deliverables**: `workspaces` table; `Workspace` ORM model;
  `WorkspaceRepository`; `WorkspaceService`; one Alembic migration.
- **Definition of Done**: migration applies and rolls back cleanly on a
  clean database; table has `id`, `name`, `owner_id`, timestamps; CRUD
  exercised only through the service layer (ADR-0003 CSR).
- **Acceptance Criteria**: a Workspace can be created and retrieved; its
  `id` is a valid, indexed FK target for every WP13–WP22 table.
- **Estimated Complexity**: S.
- **Risk**: Low — no open approval or design question (D01 is closed).
- **Owner**: Engineering.

---

## WP13 — EnterpriseObject Model 🟢

- **Goal**: canonical object model — ID, type, status, owner, timestamps.
- **Dependencies**: WP06, WP08, **WP12a**.
- **Deliverables**: `EnterpriseObject` model/repository/service, migration.
- **Definition of Done**: `workspace_id` required and indexed (ADR-0004);
  every repository method scoped by `workspace_id`.
- **Acceptance Criteria**: CRUD works; a request for another workspace's
  object returns not-found (the query simply never matches — no special
  code path needed regardless of GC-005's approval status).
- **Estimated Complexity**: M.
- **Risk**: Low.
- **Owner**: Engineering.

## WP14 — AgentDefinition Model 🔴

- **Goal**: configurable agent definition with capabilities and permissions.
- **Dependencies**: WP13; **GC-001 approval (Critical Path)**; **ADW-05
  (Critical Path — not yet written)**.
- **Deliverables**: cannot be finalized — schema shape depends on GC-001's
  outcome (global catalog vs. workspace-scoped) and ADW-05's domain
  semantics for `AgentDefinition`/`Provider`/`Model`.
- **Definition of Done**: not determinable until both Critical Path items
  close.
- **Acceptance Criteria**: not determinable until both Critical Path items
  close.
- **Estimated Complexity**: L (uncertain pending resolution).
- **Risk**: High — this is one of the two Critical Path Approval/Modeling
  Gaps identified by the Implementation Readiness Review.
- **Owner**: Project Owner (GC-001 approval, ADW-05), then Engineering.

## WP15 — Task Model and Lifecycle 🟢

- **Goal**: task states, owner, priority, source object, timestamps.
- **Dependencies**: WP13.
- **Deliverables**: `Task` model/repository/service implementing D07's
  state constitution (transition rules, authority, concurrency).
- **Definition of Done**: every D07-defined transition implemented;
  invalid transitions rejected at the service layer.
- **Acceptance Criteria**: a task's lifecycle transitions correctly end to
  end; an invalid transition is rejected with a clear error.
- **Estimated Complexity**: M–L (state-machine correctness is the risk
  driver, not the CRUD shell).
- **Risk**: Medium — D07 is precise but detailed; the risk is an
  overlooked edge case, not an undefined rule.
- **Owner**: Engineering.

## WP16 — Minimal Identity and Authentication 🟢

- **Goal**: one authenticated human user, plus service/agent identities.
- **Dependencies**: WP09.
- **Deliverables**: `User` model, `WorkspaceMembership` join entity (shape
  already resolved per `docs/c4/C3_COMPONENT.md`), auth middleware,
  `ActorContext` resolution.
- **Definition of Done**: login works; `ActorContext` resolves a role via
  `(user_id, workspace_id)` lookup, never via a flat field on `User`.
- **Acceptance Criteria**: an authenticated request resolves the correct
  workspace-scoped role.
- **Estimated Complexity**: M.
- **Risk**: Low — the shape question is already resolved, not open.
- **Owner**: Engineering.

## WP17 — Role and Permission Checks 🟡

- **Goal**: basic RBAC for user, agent, reviewer, approver.
- **Dependencies**: WP14 (🔴), WP16.
- **Deliverables**: role/permission check middleware; depends on GC-003
  (invitation model), GC-004 (role model — low-risk, already matches
  ADR-0006's existing posture), GC-008 (permission templates — low-risk,
  only one architecturally valid alternative per the proposal's own §02.3
  analysis).
- **Definition of Done**: membership and role checks enforced on every
  protected endpoint.
- **Acceptance Criteria**: an unauthorized actor is rejected; an
  authorized one proceeds.
- **Estimated Complexity**: M.
- **Risk**: Medium — transitively blocked by WP14 for the agent-role
  half; the human-role half (GC-003/004/008) is low-risk and can proceed
  once approved.
- **Owner**: Engineering (Project Owner sign-off on GC-003/004/008).

## WP18 — Event Model and Persistence 🟢

- **Goal**: events stored with trace ID, correlation ID, type, source,
  timestamp.
- **Dependencies**: WP08, WP13.
- **Deliverables**: `Event` model/repository/service. GC-002 (composite
  FK to the source entity) is open but non-blocking — build against the
  repository-invariant pattern (ADR-0004's default) now; add the
  composite FK constraint later if GC-002 approves it, without a schema
  rewrite.
- **Definition of Done**: events persisted with `workspace_id` enforced by
  invariant + negative tests.
- **Acceptance Criteria**: an event cannot be created or read across a
  workspace boundary.
- **Estimated Complexity**: M.
- **Risk**: Low–Medium.
- **Owner**: Engineering.

## WP19 — AuditRecord Model 🟢

- **Goal**: high-impact actions create immutable audit records.
- **Dependencies**: WP13, WP16.
- **Deliverables**: `AuditRecord` model/repository/service, atomic with
  the mutation it audits (ADR-0005). GC-006 (which mutations count as
  high-impact) and GC-007 (snapshot vs. diff shape) are open but
  non-blocking for this WP specifically: use GC-006's own conservative
  Alternative B (treat every mutation as high-impact) and GC-007's
  diff-only shape as the interim default.
- **Definition of Done**: business write + audit write share one
  transaction for every mutation (conservative default); audit content is
  a field-level diff, not a full snapshot.
- **Acceptance Criteria**: a mutation without its audit record cannot
  commit.
- **Estimated Complexity**: M–L (transactional correctness is the risk
  driver).
- **Risk**: Medium — must be revisited once GC-001-dependent entities
  (e.g., `WorkspaceProviderConfiguration`, which will hold credential
  references) exist, per the Implementation Readiness Review's finding
  that the diff-only default is only safe until then.
- **Owner**: Engineering.

## WP20 — ContextPackage Model 🟢

- **Goal**: context package stores sources, constraints, confidence,
  expiry.
- **Dependencies**: WP13, WP15.
- **Deliverables**: `ContextPackage` model/repository/service per
  `docs/planning/PRE-CODING-BRIEF.md` §5.2. Same GC-002 non-blocking
  posture as WP18.
- **Definition of Done**: a context package survives session termination.
- **Acceptance Criteria**: a context package created for a task remains
  readable after the originating session ends.
- **Estimated Complexity**: M.
- **Risk**: Low.
- **Owner**: Engineering.

## WP21 — RuntimeSession Model 🔴

- **Goal**: session lifecycle and links to task, agent, context.
- **Dependencies**: WP14 (🔴), WP15, WP18.
- **Deliverables**: blocked by the same root cause as WP14 — a
  `RuntimeSession` links to an `AgentDefinition` that cannot yet be
  modeled.
- **Definition of Done**: not determinable until WP14's Critical Path
  items close.
- **Acceptance Criteria**: not determinable until WP14's Critical Path
  items close.
- **Estimated Complexity**: L.
- **Risk**: High — Critical Path, same root cause as WP14 (GC-001, ADW-05).
- **Owner**: Project Owner (GC-001, ADW-05), then Engineering.

## WP22 — API Error and Response Standard 🟢

- **Goal**: consistent errors, validation responses, request IDs,
  pagination rules.
- **Dependencies**: WP06, WP10.
- **Deliverables**: shared error/response envelope, applied across every
  WP13–WP21 endpoint. GC-005 (uniform 404 vs. membership-level 403) is
  open but low-risk — the recommended alternative restates an existing
  invariant (R-07) rather than introducing a new one; build against it
  now.
- **Definition of Done**: every endpoint returns the standard envelope
  shape.
- **Acceptance Criteria**: a client can rely on one error shape across the
  whole API.
- **Estimated Complexity**: S–M.
- **Risk**: Low.
- **Owner**: Engineering.

## WP23 — Business Request Intake API 🟢

- **Goal**: authenticated user creates request, object, and task.
- **Dependencies**: WP13, WP15, WP16, WP22.
- **Deliverables**: the first real business-facing endpoint.
- **Definition of Done**: one API call produces a persisted
  `EnterpriseObject` + `Task` pair, correctly workspace-scoped.
- **Acceptance Criteria**: an authenticated user submits a request and
  receives a task ID.
- **Estimated Complexity**: M.
- **Risk**: Low, assuming WP13/15/16/22 are complete.
- **Owner**: Engineering.

## WP24 — Agent Selection and Assignment 🟡

- **Goal**: task assigned to Process Analysis Agent by explicit rule.
- **Dependencies**: WP14 (🔴), WP15, WP23.
- **Deliverables**: blocked — assignment requires an `AgentDefinition` to
  assign to.
- **Estimated Complexity**: M.
- **Risk**: High — inherits WP14's Critical Path block.
- **Owner**: Project Owner → Engineering.

## WP25 — Minimal Context Assembly 🟡

- **Goal**: task and related object produce a valid context package.
- **Dependencies**: WP20, WP23, WP24 (🟡).
- **Deliverables**: blocked transitively via WP24.
- **Estimated Complexity**: M.
- **Risk**: High — inherits the block.
- **Owner**: Engineering, after WP24 clears.

## WP26 — LLM Provider Adapter 🔴

- **Goal**: provider-independent interface returns a structured test
  response.
- **Dependencies**: WP09, WP25 (🟡); **also directly requires GC-001
  resolution** — the same Critical Path root cause as WP14, not merely
  inherited.
- **Deliverables**: blocked until the `Provider`/`Model` catalog shape is
  approved.
- **Estimated Complexity**: L.
- **Risk**: High — Critical Path, direct dependency on GC-001/ADW-05.
- **Owner**: Project Owner (GC-001, ADW-05) → Engineering.

## WP27 — Agent Runtime Execution 🔴

- **Goal**: one controlled session executes and stores output.
- **Dependencies**: WP17 (🟡), WP21 (🔴), WP25 (🟡), WP26 (🔴).
- **Deliverables**: blocked — this is the actual agent execution loop, the
  single most complex work package in Gate D, and it sits directly
  downstream of every Critical Path item.
- **Estimated Complexity**: XL.
- **Risk**: High.
- **Owner**: Engineering, after all upstream Critical Path items clear.

## WP28 — Structured Recommendation Result 🟡

- **Goal**: result includes summary, recommendation, confidence,
  assumptions.
- **Dependencies**: WP27 (🔴).
- **Deliverables**: blocked transitively.
- **Estimated Complexity**: M.
- **Risk**: Medium once WP27 clears — the result-shaping logic itself is
  not high-risk.
- **Owner**: Engineering.

## WP29 — Human Approval Flow 🟡

- **Goal**: approver can approve, reject, or request rework.
- **Dependencies**: WP16, WP17 (🟡), WP28 (🟡).
- **Deliverables**: blocked transitively, though the approval mechanics
  themselves (independent of what's being approved) are low complexity.
- **Estimated Complexity**: M.
- **Risk**: Medium.
- **Owner**: Engineering.

## WP30 — Decision Record and Events 🟡

- **Goal**: decision and related events/audit records persisted.
- **Dependencies**: WP18, WP19, WP29 (🟡).
- **Deliverables**: blocked transitively.
- **Estimated Complexity**: M.
- **Risk**: Medium.
- **Owner**: Engineering.

## WP31 — Task and Session Completion 🟡

- **Goal**: task/session statuses close consistently with result
  references.
- **Dependencies**: WP21 (🔴), WP30 (🟡).
- **Deliverables**: blocked transitively; simple once unblocked (a state
  transition plus a reference write).
- **Estimated Complexity**: S–M.
- **Risk**: Medium — inherits the block, low intrinsic complexity.
- **Owner**: Engineering.

## WP32 — Internal End-to-End Demo 🟡

- **Goal**: full scenario runs from request to visible approved result.
- **Dependencies**: WP23–WP31.
- **Deliverables**: integration only — no new logic.
- **Estimated Complexity**: M (integration effort).
- **Risk**: Medium — first time every piece runs together; integration
  risk, not design risk.
- **Owner**: Engineering.
