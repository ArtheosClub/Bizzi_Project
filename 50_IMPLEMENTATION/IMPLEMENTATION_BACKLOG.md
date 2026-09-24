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

- **Goal**: canonical object model — ID, type, `phase`, owner, timestamps.
  *(Amendment A-01, `MVP_WORK_PACKAGE_PLAN.md` § Gate C — Amendments;
  approved 2026-08-03 by Project Owner, PR #13. Original wording: "ID,
  type, status, owner, timestamps." `status` → `phase` per D07 §6 /
  LAW-D07-15, governed by ADR-0009.)*
- **Dependencies**: WP06, WP08, **WP12a**.
- **Deliverables**: WP13's complete Deliverables, as amended. The first item
  was delivered under A-01/A-02; the remainder is the audited-service half
  restored by Amendment A-12:
  - The existing `EnterpriseObject` model and its Alembic migration, unchanged
    by A-12.
  - A workspace-scoped `EnterpriseObject` repository: insert, get-by-id within
    a workspace, and list-by-workspace. The two read methods take
    `workspace_id` explicitly (ADR-0004). Insert accepts an already-formed
    instance whose `workspace_id` the service has established, and takes no
    second `workspace_id` parameter of its own — a competing source of the
    same truth is a defect, not a safeguard. No delete path. No update method
    — an update mutates a loaded instance and is flushed, matching the audit
    repository's shape.
  - A bounded `EnterpriseObjectService` with exactly three operations:
    `create`, `archive`, `unarchive`.
  - `create` persists `workspace_id`, `type` and `owner_id`, and forces
    `phase` to `active` — ADR-0009 §3 admits only `creation -> active`. The
    instance is flushed before the audit write, because
    `AuditService.record(...)` requires a persistent subject with a persisted
    identity. Audited as `AuditActions.ENTERPRISE_OBJECT_CREATED` with a
    field-level diff whose `before` values are null.
  - `archive` and `unarchive` perform `active -> archived` and `archived -> active`
    only, audited as `AuditActions.ENTERPRISE_OBJECT_UPDATED` with the diff
    `{"phase": [before, after]}`.
  - `archive` and `unarchive` take `workspace_id` and the `EnterpriseObject`
    identity, load the subject through the repository's workspace-scoped get,
    and return not-found when the identity belongs to another workspace. They
    do not accept a freely supplied ORM subject.
  - All audit writes occur in the caller's session and transaction. Neither
    the service nor the repository commits or rolls back; the caller owns the
    transaction, matching the audit layer's contract.
  - No method on a mutation path returns a mutable ORM instance. `create`
    returns the new identity; callers that need the row read it back through
    the repository's workspace-scoped read.
  - No new action constants. The two existing `EnterpriseObject` constants and
    their A-11 admissibility entry are sufficient and unchanged.
  - **Transitions into `superseded` are out of scope, and not because ADR-0009
    forbids them.** ADR-0009 §3 permits `active -> superseded` and
    `archived -> superseded`. They are excluded because D10 §12 Binding
    consequence 4 requires supersession to record a D09-typed relationship,
    the general relationship mechanism is not designed, and the model
    deliberately carries no `superseded_by_id`. Unimplementable today, not
    prohibited.
  - **Not in scope**: any API, controller or route — that is WP23, itself
    blocked through WP16 on ADW-02; mutation of `type` or `owner_id`, neither
    of which has approved change semantics; any delete path, since D10 §5.1
    forbids unqualified deletion, D10 §12 Binding consequence 3 makes a
    generic `is_deleted` a defect, and physical deletion is separately
    constrained by D10 §8 Invariant 5; WP15's `Task` service; actor
    attribution, still blocked on ADW-02.
  - **RuntimeEvent, deferred and recorded**: WP13's service does not emit a
    `RuntimeEvent`. ADR-0005's post-commit emission obligation is neither
    discharged nor reinterpreted by A-12; it is inherited by whichever work
    package delivers `RuntimeEventService`, which cannot be WP18 until ADW-07
    defines event semantics. The absence is stated in the service module so a
    future reader finds it without reading this amendment.
  *(Amendment A-02, `MVP_WORK_PACKAGE_PLAN.md` § Gate C — Amendments; approved
  2026-08-03 by Project Owner, PR #13. Original wording: "EnterpriseObject
  model/repository/service, migration." Repository and service deferred to
  WP19 — ADR-0005 requires audit-inside-transaction, and `AuditService` did
  not exist when A-02 was approved.)*
  *(Amendment A-12, `MVP_WORK_PACKAGE_PLAN.md` § Gate C — Amendments; approved
  2026-09-24 by Project Owner. WP19 delivered `AuditService`, merged as
  `2e8512d7`. The text below mirrors `#### A-12 approved WP13 field text`
  normatively.)*
- **Definition of Done**:
  - Every mutation and its audit write use the caller's same session and
    transaction. Neither module commits or rolls back. When the caller rolls
    back after any mutation or audit failure, neither change becomes durable;
    the modules do not and cannot enforce that the caller handles the failure
    correctly.
  - Every repository read takes `workspace_id`; a request for another
    workspace's object returns not-found because the query never matches, with
    no special code path.
  - `create` yields `phase = active`, with the migration's `server_default`
    proven by a direct-insert test rather than by the Python default alone.
  - `archive` and `unarchive` reject every transition other than the two they
    implement, including any attempt to reach `superseded`.
  - No mutation-path method returns a mutable ORM instance.
  - Neither module contains an executable commit or rollback call, asserted
    statically in the shape WP19 already uses.
  - The deferred `RuntimeEvent` emission is discoverable in the source, and a
    static test asserts that neither `enterprise_object_service.py` nor its
    repository imports or calls a `RuntimeEvent` or `RuntimeEventService`
    symbol. The prohibition is bounded to the slice WP13 delivers, so it
    cannot later forbid the implementation of `RuntimeEventService` itself.
    Testing the absence of a component that does not exist is otherwise almost
    contentless; what is testable is that this slice's modules do not pretend
    otherwise.
- **Acceptance Criteria**:
  - A `create` produces one persisted object and exactly one audit record
    whose populated subject column is the `EnterpriseObject` one.
  - `archive` followed by `unarchive` produces two audit records carrying the
    expected phase diffs in order.
  - A get or list scoped to another workspace returns nothing.
  - An `archive` or `unarchive` request using another workspace's identity
    returns not-found and changes neither the object nor the audit trail.
  - An attempt to reach `superseded` through the service is rejected.
  - In caller-controlled transaction tests, an audit-side failure followed by
    rollback leaves neither the business mutation nor an audit record durable;
    a business-side failure after the audit flush followed by rollback leaves
    neither durable.
  - Neither `enterprise_object_service.py` nor its repository imports or calls
    a `RuntimeEvent` or `RuntimeEventService` symbol, asserted statically, and
    the omission is recorded in the service module's own text.
- **Blocked on**: nothing for the scope above. The `RuntimeEvent` obligation
  remains recorded and unaddressed, carried by whichever work package delivers
  `RuntimeEventService`.
- **Estimated Complexity**: M.
- **Risk**: Low.
- **Owner**: Engineering.

## WP14 — AgentDefinition Model 🟡

Split by Amendment A-10 (`MVP_WORK_PACKAGE_PLAN.md` § Gate C —
Amendments; approved 2026-08-24 by Project Owner) into a schema
foundation — now ready — and a deferred runtime/configuration
remainder, the same split shape WP16 carries after A-03.

- **Goal**: schema foundation for `AgentDefinition` as a D02
  EnterpriseObject (ADR-0013), persisted standalone for the MVP
  (ADR-0015). Capabilities, permissions, and runtime semantics remain
  out of scope for this schema-foundation deliverable — see Deferred
  Concerns.
- **Dependencies**: WP13.
- **Governing decisions**: ADR-0013, ADR-0015, ADR-0009 (phase),
  ADR-0004 (workspace scoping). **GC-001 and ADW-05 are no longer
  dependencies of the schema foundation** — see Deferred Concerns below.
- **Deliverables**: `AgentDefinition` model, migration, tests only —
  same scope discipline as WP13/WP15/WP16's schema foundations. Field
  list fixed to exactly `id`, `workspace_id`, `phase`, `owner_id`,
  `created_at`, `updated_at`:
  - `id` — UUID primary key, established WP13/Task/WorkspaceMembership
    convention.
  - `workspace_id` — required independently by ADR-0004 ("every MVP
    table beyond `users` and `sessions` carries `workspace_id`"), cited
    directly, not derived through the D02 classification.
  - `phase` — governed by ADR-0009 §5 plus ADR-0013's applicability
    consequence, not by D10 §6 alone: `active` / `archived` /
    `superseded`, creation default `active`, `String`/`VARCHAR` with a
    database `CHECK` constraint, not a PostgreSQL `ENUM`.
  - `owner_id` — represents EnterpriseObject ownership, consistent with
    the existing `EnterpriseObject` contract (WP13/WP16). Ownership,
    not actor attribution — creation attribution belongs to the audit
    record (ADW-07, deferred), not to this column.
  - `created_at`, `updated_at` — established WP13/Task/
    WorkspaceMembership convention.

  No `enterprise_objects` row is created for `AgentDefinition` — ADR-0015
  establishes standalone persistence as the MVP default. No repository,
  service, or API is authorized in this schema-foundation scope.
  ADR-0005/WP19 prevents unaudited state-changing service work,
  consistent with the schema-first treatment already used in Gate C.
- **Definition of Done**:
  - `AgentDefinition` is persisted as a standalone table with exactly
    the six fields above.
  - The database `CHECK` rejects `phase` values outside `active`,
    `archived`, `superseded`; creation defaults to `active`.
  - `workspace_id` and `owner_id` are enforced as real foreign keys.
  - No `enterprise_objects` row, repository, service, or API is created
    by this WP.
- **Acceptance Criteria (schema-level)**: valid phase values are
  accepted; unknown phase values are rejected; omitted phase resolves
  to `active`; `workspace_id` and `owner_id` constraints are enforced;
  the exact six-field column set is preserved, no more, no fewer.
- **Estimated Complexity**: M (schema only, same class as WP13/WP15/
  WP16 — narrowed from the prior `L (uncertain pending resolution)` now
  that the persistence-representation question is resolved).
- **Risk**: Low for the schema foundation — the field set is sourced
  (ADR-0013, ADR-0015, ADR-0009, ADR-0004) and the persistence pattern
  is decided. Medium/deferred for the eventual runtime/configuration
  layer — GC-001 and ADW-05 remain genuinely open (see Deferred
  Concerns), and this WP's schema-foundation completion does not reduce
  that uncertainty; it only removes it as a blocker for the six fields
  above.
- **Owner**: Engineering, for the schema foundation. Project Owner
  (GC-001 approval) and ADW-05's eventual resolution remain owned as
  before for the deferred remainder.
- **Deferred Concerns** — remain **OPEN, NOT resolved**, and are not
  schema-foundation blockers: GC-001 (Provider/Model catalog scope),
  Provider identity, Model identity, the Provider↔Model relationship,
  `WorkspaceProviderConfiguration`, capabilities, permissions, the
  capabilities-versus-permissions boundary (ADW-05), the RuntimeSession
  ↔ AgentDefinition relationship, runtime Provider/Model resolution,
  credential ownership/storage/rotation, tool policy, context policy,
  escalation policy, and runtime configuration generally. Each concern
  remains deferred to the later Work Package or architecture decision
  that actually consumes it; A-10 does not re-route or resolve those
  concerns.
- **AuditRecord subject-kind trigger.** Before any service or runtime
  work in this WP's deferred remainder introduces an auditable mutation
  for a persisted identity form not already covered by accepted
  AuditRecord subject authority, consult
  `00_ARCHITECTURE/07_AUDIT/ADW07_Q2_ST_SUBJECT_TYPE_RANGING_RULE_DECISION.md`.
  Pointer only; the canonical rule is in that record.
- **Marker note**: `🟡`, not `🟢` — the same distinction WP16's marker
  note draws. Schema foundation is unblocked; the deferred runtime/
  configuration remainder is not. `🟡` here means "nothing
  architecturally undecided is blocking this WP's schema-foundation
  scope," not "fully complete end-to-end."

## WP15 — Task Model and Lifecycle 🟢

Narrowed by Amendment A-04 (`MVP_WORK_PACKAGE_PLAN.md` § Gate C —
Amendments; approved 2026-08-04 by Project Owner) after
`docs/adr/DOMAIN_REVIEW_TASK_LIFECYCLE.md` and `docs/adr/0011-task-phase-transition-graph.md`.

- **Goal**: `Task` as a Work Item specialization (D03/D08), workspace-scoped,
  with a five-value governed `phase` and an optional reference to the
  `EnterpriseObject` it's work on.
- **Dependencies**: WP13.
- **Deliverables**: `Task` model, migration, tests only. Fields: `id`,
  `workspace_id`, `phase` (`active`/`archived`/`superseded`/`cancelled`/
  `completed`, value-domain `CHECK`-constrained), `source_object_id`
  (nullable FK to `enterprise_objects.id`, N≤1 simplification of D09
  R9's approved 0..N — service code must not assume a Task can by
  nature relate to only one EnterpriseObject), `created_at`,
  `updated_at`. No `progress`, `priority`, `title`, `description`,
  `assignee_id`, or `owner_id` — none has an approved source and a
  demonstrated need together (Domain Review §4–§6).
- **Definition of Done**:
  - `Task.phase` is persisted as a constrained five-value field.
  - The database `CHECK` rejects values outside `active`, `archived`,
    `superseded`, `cancelled`, `completed`.
  - Creation defaults to `active` (Python-level `default` and migration
    `server_default` both set — only a direct-insert test proves the
    latter).
  - ADR-0011 is the normative source for the *transition graph*; WP15's
    migration implements only the *value domain*, and those are not the
    same thing — a `CHECK` sees a row's current value, not its prior
    one, so it cannot and does not reject `completed → archived` or any
    other disallowed transition. WP15 does not enforce transitions
    between existing values.
  - Transition validation, authority, concurrency, atomic audit
    recording, and rejection of invalid transitions are all deferred to
    the audited service layer, blocked on `AuditService` (WP19) — same
    as WP13's, and for the same ADR-0005 reason. WP15 intentionally does
    not introduce database-level transition enforcement — transition
    authority belongs to the audited service layer, a scope boundary for
    this WP, not a permanent prohibition on the database ever enforcing
    it.
- **Acceptance Criteria (schema-level)**: valid phase values are
  accepted; unknown phase values are rejected; omitted phase resolves to
  `active`; `workspace_id` and `source_object_id` constraints are
  enforced; the exact approved column set is preserved. **Not included**:
  transition execution, previous-state validation, transition authority,
  atomic audit recording, concurrency control.
- **Estimated Complexity**: M (schema only; state-machine *enforcement*
  moves to whichever WP builds the service).
- **Risk**: Low for the schema — the value domain is sourced (D10 §6/§8)
  and the transition graph is normatively fixed (ADR-0011), even though
  this WP doesn't enforce it. Medium, deferred, for the eventual
  service — D07 is precise but detailed.
- **Owner**: Engineering.
- **Marker note**: stays 🟢, not 🟡 like WP16. The distinction is real,
  not cosmetic: WP16's deferred half is blocked on ADW-02, an unwritten
  domain workshop with no scheduled resolution. WP15's deferred half
  (transition enforcement) is blocked on `AuditService`, a known,
  already-scoped Work Package (WP19) — a sequencing fact, not an open
  architectural question. 🟢 here means "nothing architecturally
  undecided is blocking this WP's own scope," not "fully complete
  end-to-end."

## WP16 — Minimal Identity and Authentication 🟡

Split by Amendment A-03 (`MVP_WORK_PACKAGE_PLAN.md` § Gate C —
Amendments; approved 2026-08-03 by Project Owner) into a schema
foundation and a deferred remainder — not fully unblocked, despite the
shape question being resolved.

- **Goal**: one authenticated human user, plus service/agent identities.
- **Dependencies**: WP09 (schema foundation); **ADW-02 (Identity and
  Workspace Boundary — not yet written)** for the deferred remainder,
  same phrasing as WP14's ADW-05 dependency.
- **Deliverables — schema foundation (unblocked, this PR)**: `User`
  model (`id`, `created_at`, `updated_at` only — no credential fields;
  ADW-02 owns those and doesn't exist yet), `WorkspaceMembership` join
  entity (shape already resolved per `docs/c4/C3_COMPONENT.md`;
  `role` column ships `CHECK`-constrained to `owner` only, no
  `WorkspaceInvitation`, per ADR-0010), plus the `owner_id` FK backfills
  on `Workspace`/`EnterpriseObject` that both prior migrations
  explicitly promised ("WP16's own migration adds it").
- **Deliverables — deferred (blocked)**: auth middleware, `ActorContext`
  resolution, login. Blocked on ADW-02 for `User`'s credential model, and
  on ADR-0005/WP19 (`AuditService` doesn't exist yet) for anything
  service-shaped — same class of gap A-02 already recorded for WP13.
- **Definition of Done**: schema foundation — the two new tables exist,
  migrated, tested, and the two FK backfills apply cleanly. Deferred
  remainder's Definition of Done ("login works; `ActorContext` resolves a
  role via `(user_id, workspace_id)` lookup") does not close in this PR.
- **Acceptance Criteria**: schema foundation only — CRUD-level model
  correctness, asserted by tests. The full WP's acceptance criteria ("an
  authenticated request resolves the correct workspace-scoped role")
  waits on the deferred remainder.
- **Estimated Complexity**: M (schema foundation); not determinable for
  the deferred remainder until ADW-02 exists.
- **Risk**: Low for the schema foundation — the shape question is already
  resolved. Medium for the deferred remainder — genuinely blocked, not
  merely unscheduled.
- **Owner**: Engineering (schema foundation); Project Owner (ADW-02),
  then Engineering (deferred remainder).

## WP17 — Role and Permission Checks 🟡

- **Goal**: basic RBAC for user, agent, reviewer, approver.
- **Dependencies**: WP14 (🟡 — specifically WP14's deferred runtime/
  configuration remainder, not its schema foundation), WP16 (🟡 —
  specifically WP16's deferred `ActorContext` remainder, not just its
  schema foundation; permission checks need a resolved actor/role at
  request time, which the schema alone doesn't provide).
- **Deliverables**: role/permission check middleware. GC-003 (invitation
  model) is resolved by ADR-0010 as deferred/not-applicable to the MVP —
  no longer a blocker. GC-004 (role model) is *not* approved by ADR-0010;
  ADR-0010 ships the `role` column CHECK-constrained to `owner` only and
  explicitly defers the scalar-vs-join question until a second role
  exists — WP17 introducing a second role (reviewer, approver) is exactly
  the trigger that reopens GC-004, and must resolve it, not assume
  scalar. GC-008 (permission templates — low-risk, only one
  architecturally valid alternative per the proposal's own §02.3
  analysis) remains open.
- **Definition of Done**: membership and role checks enforced on every
  protected endpoint.
- **Acceptance Criteria**: an unauthorized actor is rejected; an
  authorized one proceeds.
- **Estimated Complexity**: M.
- **Risk**: Medium — the agent-role half remains blocked on WP14's
  deferred runtime/configuration concerns; the human-role half requires
  resolving GC-004 for real (a second role forces the scalar-vs-join
  question ADR-0010 deferred), plus GC-008.
- **Owner**: Engineering (Project Owner sign-off on GC-004, GC-008).

## WP18 — Event Model and Persistence 🔴

Blocked by Amendment A-05 (`MVP_WORK_PACKAGE_PLAN.md` § Gate C —
Amendments; approved 2026-08-05 by Project Owner). Not a field-list
narrowing like A-02/A-04 — there is no approved field set to narrow to.

- **Goal**: events stored with trace ID, correlation ID, type, source,
  timestamp — **none of these five fields has an approved source in
  D01–D10 or any ADW.** `D07_STATE_SEMANTICS.md` mentions only "Event
  Delivery State" as technical messaging infrastructure, unrelated to
  this entity's persisted fields. `00_ARCHITECTURE/01_DOMAIN/` has zero
  hits for "trace id" or "correlation id". `docs/c4/C3_COMPONENT.md`'s
  own Source column cites `MVP_WORK_PACKAGE_PLAN.md` for this field
  list — it quotes the WP plan rather than grounding it, the same
  circularity the Task Domain Review found for `priority`. **This is one
  of six confirmed source-attribution discrepancies identified as of
  2026-08-08** — enumerated here so the count doesn't need re-deriving
  and stays checkable rather than trusted:
  1. `C3_COMPONENT.md` → `MVP_WORK_PACKAGE_PLAN.md` (this entry's Event
     field list, circular).
  2. GC-002 → `D09_RELATIONSHIP_MODEL.md`, for `Event`→`Task`/source
     (corrected 2026-08-05).
  3. WP20's field list → `PRE-CODING-BRIEF.md` §5.2, which doesn't
     actually contain it.
  4. GC-002 → `D09_RELATIONSHIP_MODEL.md`, for `AuditRecord`→aggregate
     (corrected 2026-08-06).
  5. GC-002 → `D09_RELATIONSHIP_MODEL.md`, for `ContextPackage`→`Task`
     (corrected 2026-08-06).
  6. `DECISION_0002` → D09 §5.8, for a "Relationship Context"/
     `ContextPackage` naming-coincidence finding: the cited §5.8 does
     not exist in the current D09 or its available iteration drafts;
     the historical finding may still be valid, but its cited basis is
     unverifiable from the current repository corpus (found 2026-08-08
     while drafting A-06).

  Three of the six sit inside one paragraph of one document (GC-002's
  governance note), where the pattern concentrated. Citations made by
  plausibility rather than verification; worth checking whenever a WP's
  stated source is relied on.

  Instance 6 is a different kind from the first five: the first five
  involve circular grounding or attribution to an existing source that
  does not support the stated claim. Instance 6 instead cites a section
  that does not exist in the current architecture corpus —
  `00_ARCHITECTURE/01_DOMAIN/D09_RELATIONSHIP_MODEL.md` has no numbered
  subsections under §5 at all, and the only §5.8 anywhere in
  `01_DOMAIN/` belongs to a different document,
  `D10_DELETION_AND_SUPERSESSION.md` (§5.8, Deprecation — unrelated). An
  adjacent, unverifiable citation sits next to it in the same source
  document: D09 §5 itself cites "Iteration 0.1 §5.7," a document not
  present anywhere in this repo, so its content cannot be checked either
  way. Noted here alongside instance 6 rather than counted as a seventh,
  since the absence of the cited document is absence of evidence, not
  evidence of a further discrepancy.

  Not corrected here or by A-06: `DECISION_0002` is a Tier 0 governance
  document; the row may be historically accurate against a version of
  D09 that no longer exists, and resolving that is outside this WP's and
  this amendment's scope. Recorded as a finding, not applied as a fix.
- **Dependencies**: WP08, WP13; **ADW-07 (Events, Audit, and Provenance —
  blocking dependency, not yet written)**. `00_ARCHITECTURE/07_AUDIT/`
  does not exist as a directory — ADW-07 is wholly undrafted, not
  partially.
- **Deliverables**: **BLOCKED pending ADW-07.** No `Event` model,
  migration, repository, service, API, or field list is authorized until
  event semantics, correlation, provenance, relationships, and
  sensitive-data rules are defined. (The prior wording's
  "model/repository/service" deliverable was also premature scope of the
  kind A-02/A-04 already corrected elsewhere — noted in passing; it is
  not the point of this amendment.)
- **Relationship to Task/EnterpriseObject**: not resolved by any approved
  source. GC-002 (`50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md`)
  remains an unapproved proposal; its governance note was corrected
  (2026-08-05, then 2026-08-06) to remove three false D09 citations —
  `Event`→`Task`/source, `AuditRecord`→aggregate, and
  `ContextPackage`→`Task` were each incorrectly attributed to D09, which
  scopes to six other concepts (Enterprise Object, Actor, Work Item,
  Decision, Business Operation, Runtime Session) and mentions none of the
  three. Only `RuntimeSession`→`Task` is actually D09-governed (R4 + R5).
  Fixing the citation did not resolve the underlying gap: `Event`'s
  relationship to Task/source still has no approved source anywhere.
- **Definition of Done for unblock**:
  - ADW-07 is completed and approved.
  - Event semantics and field shape have an approved source.
  - WP18 receives a subsequent schema-scope amendment.
  - Only then may model/migration/tests begin.
- **Acceptance Criteria**: not determinable until the above unblock
  sequence completes.
- **Estimated Complexity**: M (pending re-estimate once ADW-07 defines
  actual scope).
- **Risk**: High — blocked on an unwritten domain workshop, same class as
  WP14/ADW-05.
- **Owner**: Project Owner (ADW-07), then Engineering.

ADW-07 must define, at minimum:
- Event identity and semantics
- the distinction between Event, AuditRecord, and delivery state
- correlation and causation semantics
- source/provenance representation
- Event relationships to Task, EnterpriseObject, Business Operation,
  RuntimeSession, and Actor
- occurred/recorded/published/delivered time semantics
- immutability, retention, and sensitive-data rules

(Detailed diagnostic questions for the ADW-07 working session are kept in
`handover.md`, not here — this entry stays a scope record, not a
workshop draft.)

## WP19 — AuditRecord Model 🟡

Amended by A-11 (`MVP_WORK_PACKAGE_PLAN.md` § Gate C — Amendments;
approved 2026-09-06 by Project Owner). The authorized scope is the minimal
operational audit core below; actor attribution remains deferred.

- **Goal**: high-impact actions create immutable audit records.
- **Dependencies**: WP13, WP16 (schema foundation). Actor attribution on
  the audit record additionally needs WP16's deferred half
  (`ActorContext`, still blocked on ADW-02). **Who** acted (`ActorContext`)
  remains independent of **what** was acted on (ADR-0014 Q1/Q2).
- **Deliverables**:
  - `AuditRecord` model, migration, tests.
  - An **append-only** repository: insert and read only; no update or delete
    path is implemented. Read methods are workspace-scoped (ADR-0004).
  - A minimal `AuditService.record(...)`, called by state-changing service
    methods per ADR-0005.
  - The business mutation and its audit record are written through **one
    SQLAlchemy session and one transaction** — if the mutation does not
    commit, neither does its audit record, and vice versa.
  - `workspace_id` is **required and indexed** (ADR-0004). An ordinary caller
    does not pass it as a free value: `AuditService` derives it from the
    already-loaded workspace-scoped subject or from a trusted mutation
    envelope.
  - Five nullable subject-reference columns, one per accepted D1 subject kind:
    `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, `Task`.
    Each holds that kind's canonical audited-subject identity per the accepted
    Q2 decision §3.
  - **Exactly one** subject-reference column is populated per committed record,
    enforced at the database persistence boundary (accepted Q2-EX-O1).
  - **No persisted `subject_type` or kind token.** Subject kind is determined
    structurally by which column is populated.
  - **Write-time validation contract**: a caller does not pass an arbitrary
    subject UUID; `AuditService` accepts a trusted loaded subject or mutation
    envelope; the service determines the permitted subject path, canonical
    primary key and workspace; the repository accepts an already-validated
    representation; a workspace mismatch or unsupported subject kind rejects
    the whole transaction. This is the explicit recorded mechanism Q2-RI
    requires where database FK enforcement is absent. Without this, the
    exactly-one constraint guarantees only that one UUID is present, not that
    it ever denoted a real subject.
  - The five subject-reference columns are **not foreign-key constraints**.
    No delete behavior is selected or pre-approved.
  - Action is recorded as a **named constant** (`AuditActions.*` per ADR-0005),
    never an ad-hoc string.
  - Content is recorded as a **field-level diff**, not a full snapshot — WP19's
    own conservative interim choice, narrower than GC-007's recommended
    Alternative C.
  - **Every state-changing mutation within the authorized operational slice**
    requires atomic audit — WP19's own conservative interim choice, more
    conservative than GC-006's recommended Alternative A. The initial callable
    slice covers `EnterpriseObject` and `Task` mutations needed by WP13 and
    WP15. Other subject kinds remain schema-supported — all five columns exist
    — but require their own applicable workspace/context source and service
    authorization before use.
    `User` in particular has no `workspace_id` of its own, so the source of the
    required `AuditRecord.workspace_id` remains unestablished for it pending
    `ActorContext`/ADW-02.
  - **Not in scope**: actor attribution (`ActorContext`, WP16's deferred
    remainder, blocked on ADW-02) and D09 R10 attribution modeling; foreign-key
    constraints and any delete behavior; audit query or API surface; GC-006's
    curated allowlist; GC-007's field-sensitivity marking; any relationship to
    `Event`/WP18; audited `AgentDefinition` mutations.
  - **Naming reconciliation, bounded**: for the bounded A-11 implementation,
    `AuditService.record(...)` persists an `AuditRecord`. This is the
    implementation target for ADR-0005's authoritative audit-trail write. It
    does not identify `AuditRecord` with Domain Event, resolve the
    Event/AuditRecord relationship, or amend ADR-0005's accepted text.
- **Definition of Done**:
  - A state-changing service method and its audit record commit or fail
    together, through one session and one transaction.
  - `workspace_id` is present, non-null and indexed on every committed record,
    and is derived by the service rather than supplied freely by the caller.
  - Repository read methods are workspace-scoped.
  - Every committed `AuditRecord` has exactly one populated subject-reference
    column, and the database rejects zero or more than one.
  - Subject kind is derivable from the populated column alone; no
    `subject_type` column exists.
  - The repository exposes no update or delete path.
  - The write-time validation contract rejects an unsupported subject kind or
    a workspace mismatch by failing the whole transaction.
  - Actions are recorded from named constants only; audit content is a
    field-level diff.
  - No foreign-key constraint is created on any subject-reference column, and
    no delete behavior is selected.
- **Acceptance Criteria**:
  - A mutation without its audit record cannot commit — atomicity test in both
    directions.
  - A committed `AuditRecord` retains its populated subject-reference value and
    its structural subject-kind determination independently of later subject
    lifecycle state or loss of live dereferenceability. This criterion neither
    requires nor authorizes physical subject deletion.
  - Inserting a record with zero populated subject-reference columns is rejected
    by the database; so is inserting one with two or more.
  - A record whose subject reference was never validated against a loaded
    subject cannot be produced through the service path.
  - An `AuditRecord` that cannot be resolved to what it audited is not a
    complete audit record (ADR-0014).
- **Estimated Complexity**: M–L (transactional correctness is the risk driver).
- **Risk**: Medium — must be revisited once GC-001-dependent entities (e.g.,
  `WorkspaceProviderConfiguration`, which will hold credential references)
  exist, per the Implementation Readiness Review's finding that the diff-only
  default is only safe until then.
- **Blocked on**: nothing for the authorized scope above. The deferred
  actor-attribution remainder remains blocked on ADW-02. WP19 does not depend on
  WP18 (PR #31).
- **AuditRecord subject-kind trigger.** Before implementation introduces an
  auditable mutation for a persisted identity form not already covered by
  accepted AuditRecord subject authority, consult
  `00_ARCHITECTURE/07_AUDIT/ADW07_Q2_ST_SUBJECT_TYPE_RANGING_RULE_DECISION.md`.
  Pointer only; the canonical rule is in that record.
- **Owner**: Engineering.

## WP20 — ContextPackage Model 🔴

Blocked by Amendment A-06 (`MVP_WORK_PACKAGE_PLAN.md` § Gate C —
Amendments; approved 2026-08-08 by Project Owner). Not a field-list
narrowing like A-02/A-04 — there is no approved field set to narrow to.

- **Goal**: context package stores sources, constraints, confidence,
  expiry — **none of these four fields has an approved source.**
  `docs/planning/PRE-CODING-BRIEF.md` §5.2 — this entry's own cited
  source — describes a context snapshot surviving `RuntimeSession`
  termination but never states this field list; `ContextPackage`
  otherwise appears in that document only once, as a bare entity name in
  the Architecture Traceability list. This is one of the six confirmed
  source-attribution discrepancies identified as of 2026-08-08 (see
  WP18's entry, #3: WP20's field list → `PRE-CODING-BRIEF.md` §5.2,
  which doesn't actually contain it).
- **Dependencies**: WP13, WP15; **blocked pending clarification of the
  governing domain source (candidate governing workshop: ADW-06 —
  Knowledge and Memory)**. `00_ARCHITECTURE/06_KNOWLEDGE/` does not
  exist as a directory — the candidate workshop is wholly undrafted, not
  partially.
- **Deliverables**: **BLOCKED pending clarification of the governing
  domain source.** No `ContextPackage` model, migration, repository,
  service, API, or field list is authorized until the governing
  workshop defines context/knowledge semantics, retention, and
  relationships. (The prior wording's "model/repository/service"
  deliverable was also premature scope of the kind A-02/A-04 already
  corrected elsewhere — noted in passing; it is not the point of this
  amendment.)
- **Relationship to Task**: not resolved by any approved source. GC-002
  (`50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md`)
  remains an unapproved proposal; its governance note (corrected
  2026-08-06) removed the false attribution of `ContextPackage`→`Task`
  to D09, which scopes to six other concepts (Enterprise Object, Actor,
  Work Item, Decision, Business Operation, Runtime Session) and does not
  mention ContextPackage. Fixing the citation did not resolve the
  underlying gap: `ContextPackage`'s relationship to `Task` still has no
  approved source anywhere.
- **Important distinction from A-05**: Unlike WP18, no approved document
  explicitly assigns `ContextPackage` to ADW-06. ADW-06 is identified
  only as the best-supported candidate governing workshop, inferred from
  its published scope overlapping "context" (and loosely "retention").
  This amendment therefore records an inference rather than an
  established authority attribution.
- **Definition of Done for unblock**:
  - The governing domain source is identified, completed, and approved
    (candidate governing workshop currently: ADW-06).
  - `ContextPackage` field shape and relationship semantics have an
    approved source.
  - WP20 receives a subsequent schema-scope amendment.
  - Only then may model/migration/tests begin.
- **Acceptance Criteria**: not determinable until the above unblock
  sequence completes.
- **Estimated Complexity**: M (pending re-estimate once the governing
  workshop defines actual scope).
- **Risk**: High — blocked pending an approved governing domain source;
  the best-supported candidate governing workshop (ADW-06) is currently
  unwritten.
- **Owner**: Project Owner, then Engineering.
- **Blocking prerequisite**: approved governing domain source (candidate
  governing workshop currently: ADW-06).

The candidate governing workshop (currently ADW-06) will need to define
at least:
- `ContextPackage` identity and its relationship to `Task` and
  `RuntimeSession`
- the field set — including whether sources, constraints, confidence,
  and expiry are the right fields at all
- retention and expiry semantics
- how a context snapshot survives `RuntimeSession` termination (the
  behavior `PRE-CODING-BRIEF.md` §5.2 already describes, without fixing
  a schema for it)
- immutability rules for a persisted context snapshot

Unlike WP18, the blocking conclusion does not depend on ADW-06
ultimately proving to be the governing workshop. Even if another
workshop is later identified, the underlying problem is unchanged: the
field set, relationship semantics, and persistence shape currently have
no approved source. This amendment blocks implementation because the
authoritative source is missing — not because ADW-06 has been
established as that source.

## WP21 — RuntimeSession Model 🔴

- **Goal**: session lifecycle and links to task, agent, context.
- **Dependencies**: WP14 (🟡 — specifically WP14's deferred runtime/
  configuration remainder, not its schema foundation), WP15, WP18 (🔴).
- **Deliverables**: blocked on three independent prerequisite classes:
  WP18's Event-model block; the unresolved RuntimeSession ↔
  AgentDefinition relationship, which ADR-0013 explicitly leaves outside
  D09 and requires a separate Class A architecture decision; and WP14's
  deferred runtime/configuration remainder (including runtime
  Provider/Model resolution under GC-001/ADW-05). The `AgentDefinition`
  schema foundation is now authorized, but none of those three blockers
  is resolved by A-10.
- **Definition of Done**: not determinable until WP18 is unblocked, the
  RuntimeSession ↔ AgentDefinition relationship has an explicit approved
  architecture decision, and the WP14 deferred runtime/configuration
  concerns required by WP21 are resolved.
- **Acceptance Criteria**: not determinable until all three prerequisite
  classes above are resolved.
- **Estimated Complexity**: L.
- **Risk**: High — Critical Path; WP18 remains directly blocked; the
  RuntimeSession ↔ AgentDefinition relationship remains an independent
  architecture blocker under ADR-0013; and GC-001/ADW-05 still govern
  WP14's relevant runtime/configuration remainder even though WP14's
  schema foundation is unblocked.
- **Owner**: Project Owner (RuntimeSession ↔ AgentDefinition decision,
  GC-001, ADW-05, and WP18's governing unblock), then Engineering.

## WP22 — API Error and Response Standard 🟢

- **Goal**: consistent errors, validation responses, request IDs,
  pagination rules.
- **Dependencies**: WP06, WP10.
- **Deliverables**: shared error/response envelope, applied across every
  WP13–WP21 endpoint; per-HTTP-request identifier generation and
  propagation, transferred from WP10 by Amendment A-07 — this
  identifies one HTTP request lifecycle only and does not define,
  implement, alias, or constrain Domain Event correlation, causation,
  provenance, distributed tracing, or cross-request workflow identity
  (ADW-07/ADW-08 territory, undecided). GC-005 (uniform 404 vs.
  membership-level 403) is open but low-risk — ADR-0012 §6 selects
  uniform `not_found` for WP22's generic HTTP error mapping, an
  engineering-contract choice within the space R-07 permits, not a
  consequence R-07 forces; build against it. GC-005 itself remains
  `Proposed`, neither approved nor foreclosed.
- **Definition of Done**: every domain-facing API endpoint returns the
  standard error envelope on failure, per ADR-0012 — see Amendment A-08.
  Operational/infrastructure endpoints (e.g. `/health`) are outside that
  envelope's scope.
- **Acceptance Criteria**: a client can rely on one error shape across
  the domain-facing API; operational/infrastructure endpoints (e.g.
  `/health`) are outside that guarantee — see Amendment A-08.
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
- **Dependencies**: WP14 (🟡 — specifically WP14's deferred runtime/
  configuration remainder, not its schema foundation), WP15, WP23.
- **Deliverables**: blocked — assignment requires the deferred
  AgentDefinition runtime/configuration semantics needed to select and
  assign an agent; the six-field schema foundation alone is insufficient.
- **Estimated Complexity**: M.
- **Risk**: High — inherits WP14's deferred runtime/configuration block,
  not its now-unblocked schema foundation.
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
