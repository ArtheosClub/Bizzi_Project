# MVP Work Package Plan

Version: 1.0
Status: Active Implementation Plan
Implementation Track: 50_IMPLEMENTATION
Scope: WP00–WP93

Related Documents:
- PB050_Bizzi_Reference_Implementation_Architecture.md
- PB051_Backend_Service_Architecture.md
- PB052_Agent_Runtime_Implementation.md
- PB053_Context_Engine_Implementation.md
- PB054_Knowledge_Graph_Implementation.md
- PB055_Decision_Engine_Implementation.md
- PB056_Command_Center_Implementation.md
- PB057_API_and_Integration_Implementation.md
- PB058_Authentication_and_Authorization_Implementation.md
- PB059_Event_Bus_and_Observability_Implementation.md
- CORE_Canonical_Data_Model.md
- CORE_Architecture_Traceability_Matrix.md
- CORE_Simplicity_and_Usability_Principles.md

Primary Owner:
- AG009 Enterprise Architect

Product Owner:
- AG002 Chief Orchestrator

Implementation Owner:
- AG080 Runtime Manager

Audit Owner:
- AG003 AI Auditor

---

## 00. Executive Summary

This document converts the full WP00–WP93 roadmap into a dependency-driven implementation plan.

The 94 work packages are not a single linear prerequisite chain.

They are divided into:

- MVP Critical Path;
- MVP Hardening;
- Post-MVP Platform Expansion;
- Future Productization.

Core principle:

```text
94 work packages describe the roadmap.
Only the critical path blocks the first working product.
```

The first Bizzi MVP must prove one complete business flow:

```text
User Request
  -> Enterprise Object
  -> Task
  -> Context Package
  -> One Agent Runtime Session
  -> Recommendation / Result
  -> Human Approval or Rejection
  -> Decision Record
  -> Event and Audit Trail
  -> Command Center View
  -> Memory Entry
```

---

## 01. MVP Product Scenario

### First Business Scenario

A user submits a business-process problem.

Bizzi:

1. creates an enterprise object and task;
2. assigns one configured analysis agent;
3. assembles relevant context;
4. executes an agent session;
5. returns a structured recommendation;
6. requests human approval when required;
7. records the decision and outcome;
8. emits events and audit records;
9. displays the result in the Command Center;
10. stores the validated lesson in Enterprise Memory.

### MVP Agent Scope

The MVP does not implement 83+ independent coded agents.

It implements one generic runtime and a minimal set of configured roles:

- Chief Orchestrator;
- Process Analysis Agent;
- Reviewer / Auditor;
- Human Approver;
- optional Knowledge Curator.

Agent differences should initially be configuration, prompts, capabilities, permissions, and tool bindings — not separate software architectures.

---

## 02. Priority Classes

| Priority | Meaning |
|---|---|
| P0 — Critical | Blocks the first end-to-end MVP demonstration |
| P1 — Required | Required for MVP release quality but may not block the earliest internal demo |
| P2 — Next | Valuable immediately after MVP validation |
| P3 — Later | Post-MVP platform expansion |
| P4 — Future | Productization, scale, or advanced enterprise features |

---

## 03. Delivery Gates

| Gate | Scope | Exit Condition |
|---|---|---|
| Gate A — Product Definition | WP00–WP04 | Scenario, user, value, acceptance criteria approved |
| Gate B — Engineering Foundation | WP05–WP12 | Local stack runs with API, DB, migrations, tests, CI |
| Gate C — Platform Backbone | WP13–WP22 | Core objects, auth, events, audit, tasks, context records work |
| Gate D — First Vertical Slice | WP23–WP32 | Request-to-result-to-approval flow works end to end |
| Gate E — MVP Completion | WP33–WP39 | UI, memory, resilience, tests, deployment, documentation ready |
| Gate F — Post-MVP Platform | WP40–WP69 | Graph, orchestration, decision intelligence, integrations expanded |
| Gate G — Productization | WP70–WP93 | Multi-tenancy, marketplace, scale, enterprise deployment |

---

## 04. Critical Path

```text
WP00
  -> WP01
  -> WP02
  -> WP03
  -> WP04
  -> WP05
  -> WP06
  -> WP07
  -> WP08
  -> WP09
  -> WP13
  -> WP14
  -> WP15
  -> WP16
  -> WP18
  -> WP19
  -> WP20
  -> WP23
  -> WP24
  -> WP25
  -> WP26
  -> WP27
  -> WP28
  -> WP29
  -> WP30
  -> WP31
  -> WP32
  -> WP33
  -> WP34
  -> WP35
  -> WP36
  -> WP37
  -> WP38
  -> WP39
```

The earliest useful internal demo ends at WP32.
The release-quality MVP ends at WP39.

---

## 05. Infrastructure Boundary

Infrastructure and scaffolding end after WP22.

At that point Bizzi has:

- a runnable repository;
- backend and frontend shells;
- PostgreSQL and migrations;
- configuration and secrets handling;
- minimal authentication;
- canonical object models;
- task, event, audit, context, and runtime-session records;
- structured logging and health checks.

The first real business functionality starts at WP23, when a user can submit an actual business request that enters the execution flow.

---

## 06. Work Package Standard

Each work package follows this structure:

```yaml
id:
title:
priority:
phase:
depends_on:
blocks:
deliverable:
acceptance_criteria:
demo_value:
status:
```

Default status for all packages in this version: `Planned`.

---

# 07. Detailed Work Packages

## Gate A — Product Definition

| ID | Title | Priority | Depends On | Blocks | Deliverable / Acceptance Criteria |
|---|---|---:|---|---|---|
| WP00 | MVP Charter | P0 | — | WP01 | One-page scope, non-goals, owner, release definition approved |
| WP01 | Primary User Definition | P0 | WP00 | WP02 | Primary user persona and top pain documented |
| WP02 | First Business Scenario | P0 | WP01 | WP03 | Request-to-decision scenario written with example input/output |
| WP03 | MVP Value Hypothesis | P0 | WP02 | WP04 | Measurable user value and success signal defined |
| WP04 | Acceptance and Demo Criteria | P0 | WP03 | WP05 | End-to-end acceptance checklist and demo script approved |

## Gate B — Engineering Foundation

| ID | Title | Priority | Depends On | Blocks | Deliverable / Acceptance Criteria |
|---|---|---:|---|---|---|
| WP05 | Repository Code Structure | P0 | WP04 | WP06 | `/backend`, `/frontend`, `/infra`, `/tests` structure committed |
| WP06 | Python and FastAPI Skeleton | P0 | WP05 | WP07, WP13 | API boots locally and exposes `/health` |
| WP07 | PostgreSQL Local Service | P0 | WP06 | WP08, WP14 | Database runs through Docker Compose and accepts connections |
| WP08 | ORM and Migration Setup | P0 | WP07 | WP13–WP20 | Initial migration applies and rolls back cleanly |
| WP09 | Configuration and Environment Model | P0 | WP06 | WP10, WP16 | Typed settings, `.env.example`, environment separation |
| WP10 | Structured Logging Foundation | P1 | WP09 | WP21, WP36 | JSON logs — see Amendment A-07 |
| WP11 | Test Framework and Quality Checks | P1 | WP06 | WP37 | Unit test command and lint/type checks pass |
| WP12 | CI Foundation | P1 | WP11 | WP39 | CI runs tests and quality checks on push/PR |

## Gate C — Platform Backbone

| ID | Title | Priority | Depends On | Blocks | Deliverable / Acceptance Criteria |
|---|---|---:|---|---|---|
| WP13 | EnterpriseObject Model | P0 | WP06, WP08 | WP14, WP23 | CRUD model with canonical ID, type, `phase`, owner, timestamps — see Amendment A-01 |
| WP14 | AgentDefinition Model | P0 | WP13 | WP24, WP27 | Configurable agent definition with capabilities and permissions |
| WP15 | Task Model and Lifecycle | P0 | WP13 | WP23–WP32 | Task states, owner, priority, source object, timestamps implemented — see Amendment A-04 |
| WP16 | Minimal Identity and Authentication | P0 | WP09 | WP17, WP23, WP29 | One authenticated human user and service/agent identities supported — see Amendment A-03 |
| WP17 | Role and Permission Checks | P1 | WP14, WP16 | WP27, WP29 | Basic RBAC for user, agent, reviewer, approver |
| WP18 | Event Model and Persistence | P0 | WP08, WP13 | WP21, WP30, WP34 | Events stored with trace ID, correlation ID, type, source, timestamp |
| WP19 | AuditRecord Model | P0 | WP13, WP16 | WP30, WP36 | High-impact actions create immutable audit records — see Amendment A-09 |
| WP20 | ContextPackage Model | P0 | WP13, WP15 | WP25, WP27 | Context package stores sources, constraints, confidence, expiry — see Amendment A-06 |
| WP21 | RuntimeSession Model | P1 | WP14, WP15, WP18 | WP27, WP31 | Session lifecycle and links to task, agent, context implemented |
| WP22 | API Error and Response Standard | P1 | WP06, WP10 | WP23–WP39 | Consistent errors, validation responses, request IDs, pagination rules — see Amendments A-07, A-08 |

### Amendments

Amendments are recorded rather than applied silently: the original wording is
preserved here so the change and its reason remain auditable. Each requires
Project Owner approval before the amended criteria are binding.

**Date convention:** each Approval Record's `Decision Date` records when
the Project Owner decided; `Approved Commit or PR` records when that
decision was committed — these are two distinct events and are not
expected to fall on the same calendar date.

| ID | WP | Date | Status | Change |
|---|---|---|---|---|
| A-01 | WP13 | 2026-08-02 | **Approved** | Acceptance criteria field `status` → `phase`. Original wording: *"CRUD model with canonical ID, type, status, owner, timestamps."* |
| A-02 | WP13 | 2026-08-03 | **Approved** | Deliverables field `EnterpriseObject model/repository/service, migration` → `EnterpriseObject model, migration`. Original wording (`IMPLEMENTATION_BACKLOG.md`): *"EnterpriseObject model/repository/service, migration."* |
| A-03 | WP16 | 2026-08-03 | **Approved** | Splits WP16 into a schema foundation (this PR: `User`, `WorkspaceMembership`, migration, tests, plus the `owner_id` FK backfills on `Workspace`/`EnterpriseObject` both prior migrations promised) and a deferred remainder (login, auth middleware, `ActorContext` resolution — blocked on ADW-02 and on ADR-0005/WP19). Original wording: *"One authenticated human user and service/agent identities supported"* stated as a single undivided deliverable. |
| A-04 | WP15 | 2026-08-04 | **Approved** | Deliverables field narrowed to model/migration/tests only, and the field list fixed to `id`, `workspace_id`, `phase`, `source_object_id`, `created_at`, `updated_at`. Original wording: *"`Task` model/repository/service implementing D07's state constitution (transition rules, authority, concurrency)"* with acceptance criteria *"Task states, owner, priority, source object, timestamps."* |
| A-05 | WP18 | 2026-08-05 | **Approved** | Not a field-list narrowing (there is no approved field set to narrow to) — a readiness and scope correction: WP18 status `🟢` → `🔴`, blocked pending ADW-07. Deliverables field `Event model/repository/service` withdrawn; no model, migration, repository, service, API, or field list is authorized until ADW-07 defines event semantics, correlation, provenance, relationships, and sensitive-data rules. Original wording (`IMPLEMENTATION_BACKLOG.md`): *"Deliverables: `Event` model/repository/service"*, acceptance criteria *"trace ID, correlation ID, type, source, timestamp."* |
| A-06 | WP20 | 2026-08-08 | **Approved** | Not a field-list narrowing (there is no approved field set to narrow to) — a readiness and scope correction: WP20 status `🟢` → `🔴`, blocked pending clarification of the governing domain source (candidate governing workshop: ADW-06). Deliverables field `ContextPackage model/repository/service` withdrawn; no model, migration, repository, service, API, or field list is authorized until the governing workshop defines context/knowledge semantics, retention, and relationships. Original wording (`IMPLEMENTATION_BACKLOG.md`): *"Deliverables: `ContextPackage` model/repository/service per `docs/planning/PRE-CODING-BRIEF.md` §5.2"*, acceptance criteria *"a context package created for a task remains readable after the originating session ends."* |
| A-07 | WP10, WP22 | 2026-08-11 | **Approved** | Transfers per-HTTP-request identifier generation and propagation from WP10 to WP22 — the first between-WP scope transfer in this amendment series (A-01–A-06 only narrowed or withdrew scope within one WP). WP10's Deliverables narrow to structured JSON logging only; status remains `🟢`, since the narrowed scope is genuinely delivered (`backend/app/core/logging.py`). WP22's Deliverables gain identifier generation/propagation, with an explicit Tier-6 boundary against Domain Event correlation, causation, provenance, distributed tracing, and cross-request workflow identity. Original wording (`MVP_WORK_PACKAGE_PLAN.md`, WP10): *"JSON logs with request and correlation identifiers."* |
| A-08 | WP22 | 2026-08-11 | **Approved** | Narrows WP22's Definition of Done and Acceptance Criteria from their unqualified `every endpoint`/`whole API` wording to the scope ADR-0012 actually establishes: the standardized error envelope and the one-error-shape guarantee both apply to domain-facing API endpoints; operational/infrastructure endpoints (e.g. `/health`) are outside both. A scope correction, not an editorial clarification — the prior wording on each field committed to more than ADR-0012 delivers. Widened from its original single-field draft (Definition of Done only) once Acceptance Criteria was found to carry the same over-broad claim from the same cause (ADR-0012 §2) — recorded as deliberate, not an accumulation. Original wording (`IMPLEMENTATION_BACKLOG.md`): Definition of Done — *"every endpoint returns the standard envelope shape."*; Acceptance Criteria — *"a client can rely on one error shape across the whole API."* |
| A-09 | WP19 | 2026-08-19 | **Approved** | Readiness and scope correction, per **ADR-0014** (Accepted): WP19 status `🟢` → `🔴`, blocked pending Q2 (the persisted `AuditRecord` subject-reference shape) under ADR-0014's routing obligation, which uses ADW-07 as the future semantic destination named by `DECISION_0002` — not inherited from WP18; PR #31 already established WP19 does not depend on WP18. Deliverables gain an explicit requirement: the persisted `AuditRecord` must durably identify its audited subject (ADR-0014 Q1, shape-neutral — no dedicated reference column mandated). Also corrects two citation errors in the Deliverables field, found while verifying this amendment and unrelated to ADR-0014's own content: "GC-006's own conservative Alternative B" and "GC-007's diff-only shape" both attributed an interim default to the wrong proposal's recommendation — GC-006 recommends Alternative A, GC-007 recommends Alternative C. The interim defaults themselves (Alternative B; plain diff) are unchanged; only the attribution is corrected to WP19's own choice rather than either GC item's recommendation, so `Risk`'s "diff-only default" language stays coherent. Original wording (`IMPLEMENTATION_BACKLOG.md`): Deliverables — *"GC-006 (which mutations count as high-impact) and GC-007 (snapshot vs. diff shape) are open but non-blocking for this WP specifically: use GC-006's own conservative Alternative B (treat every mutation as high-impact) and GC-007's diff-only shape as the interim default."* |
| A-10 | WP14 | 2026-08-24 | **Approved** | Readiness and scope correction: WP14 status `🔴` → `🟡`. ADR-0013, ADR-0015, ADR-0009 and ADR-0004 authorize the schema foundation with exactly `id`, `workspace_id`, `phase`, `owner_id`, `created_at`, `updated_at`. GC-001 and ADW-05 remain open and unresolved; they are removed as schema-foundation blockers only. No repository, service, or API is authorized in this scope; ADR-0005/WP19 still applies. Original wording (`IMPLEMENTATION_BACKLOG.md`): *"Dependencies: WP13; GC-001 approval (Critical Path); ADW-05 (Critical Path — not yet written)."* Deliverables, Definition of Done, and Acceptance Criteria were *"not determinable until both Critical Path items close."* |

**A-01 rationale.** WP13's original criteria were written before D07
(`D07_STATE_SEMANTICS.md`) was approved and closed on 2026-07-22. D07 §6
defines Phase, Status, Outcome, Progress, and Health as orthogonal dimensions
and LAW-D07-15 prohibits collapsing them into "one universal authoritative
`status` field" — so a `status` column carrying lifecycle values cannot be
implemented as literally specified. D07 §6.1 defines Phase as "where is the
subject in its governed lifecycle," which is the dimension WP13 actually
needs.

Under the Authority Hierarchy (`00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md`
§3), D07 is a Tier 2 constitutional decision and this plan is Tier 4, so the
plan is what gives way. The amendment applies an approved decision; it does
not make a new one, and requires no Architecture Change Request under
DECISION_0003 §11.

Governed by `docs/adr/0009-enterprise-object-phase-lifecycle.md`, which fixes
the three permitted values (`active`, `archived`, `superseded`), the permitted
transitions, and the entities that do **not** inherit this lifecycle. Derived
in `docs/adr/DOMAIN_REVIEW_ENTERPRISE_OBJECT.md`.

**A-02 rationale.** `IMPLEMENTATION_BACKLOG.md`'s WP13 Deliverables field, as
originally written, instructs a future reader to build a repository and
service layer for `EnterpriseObject`. ADR-0005 requires audit-inside-transaction
for every state-changing service method, and `AuditService` does not exist
until WP19 — writing the service now would either violate ADR-0005 or
silently pull WP19's dependency forward. This is the same failure mode A-01
corrected for `status`: a live planning document instructing a breach of an
accepted ADR. WP13's actual implementation already scopes correctly — model
and migration only, no repository or service, matching WP12a's precedent —
this amendment brings the written Deliverables field into agreement with
what was built and with ADR-0005.

### Amendment Approval Record (A-01, A-02)

```text
Decision: Approved (A-01, A-02)
Decider: Andrew (Project Owner)
Decision Date: 2026-08-03
Approved Commit or PR: PR #13 (`docs/domain-review-enterprise-object`)
```

**A-03 rationale.** WP16's Deliverables were written as one undivided
line before two of its prerequisites were confirmed unresolved: ADR-0010
(this session) scopes `WorkspaceMembership` but explicitly does not
approve GC-004 itself, and `User`'s field shape has no approved source at
all — ADW-02 (Identity and Workspace Boundary), the domain workshop that
owns identity and credential mechanics, is unwritten
(`ADW_01_CORE_DOMAIN_SEMANTICS.md` §10 lists it as deferred beyond
ADW-01). Shipping `User` with credential fields now would settle ADW-02's
scope by migration rather than by decision — the same irreversibility
Architecture Review Checklist question 4 exists to catch, and the same
treatment `EnterpriseObject.type` already got for its own unenumerated
values. The schema foundation (bare `User` identity, the already-scoped
`WorkspaceMembership`, and the two FK backfills two earlier migrations
already promised) has no such gap and proceeds; login, auth middleware,
and `ActorContext` resolution do not, until ADW-02 exists for the
credential model and `AuditService` (WP19) exists for anything
state-changing (ADR-0005).

### Amendment Approval Record (A-03)

```text
Decision: Approved (A-03)
Decider: Andrew (Project Owner)
Decision Date: 2026-08-03
Approved Commit or PR: PR #19 (`feat/wp16-user-workspace-membership`)
```

**A-04 rationale.** Two separate corrections converge on this amendment.

First, the same failure mode A-02 already corrected for WP13:
`IMPLEMENTATION_BACKLOG.md`'s WP15 entry specifies "`Task`
model/repository/service implementing D07's state constitution
(transition rules, authority, concurrency)" and "every D07-defined
transition implemented; invalid transitions rejected at the service
layer" — a service layer now, which ADR-0005 still forbids until
`AuditService` exists at WP19.

Second, `docs/adr/DOMAIN_REVIEW_TASK_LIFECYCLE.md` re-derived WP15's
field list from D01–D10 and WP02 directly. Against the original stated
criteria ("Task states, owner, priority, source object, timestamps"),
by category:

- **Excluded**, of the originally stated fields: `owner` (Domain Review
  §6 — a column that can only reference `users` would be a false
  contract, since WP02's actual assignee is an agent, not a human; also
  no demonstrated need for a human-only target) and `priority` (§5 — no
  approved source and no demonstrated need; WP02 is one task, nothing to
  prioritize against).
- **Replaced**: `states` becomes the precise `phase` — five values
  derived from D10 §6/§8 Invariant 6 (§3), with its transition graph
  fixed separately by `docs/adr/0011-task-phase-transition-graph.md`
  (§3a identified the graph, not just the value list, as underdetermined
  by the sources alone).
- **Retained, in a limited form**: `source object` becomes
  `source_object_id`, the N≤1 subset of D09 R9's approved 0..N
  cardinality (§7) — a recorded simplification, not a domain limit.
- **Retained as-is**: timestamps (`created_at`, `updated_at`).
- **Additionally examined and not added** — none of these were in
  WP15's original stated criteria, so their absence is a considered
  exclusion, not a removal: `progress` (§4 — an approved D07 dimension
  with no approved value shape), `title`, `description` (§8 — not
  attested by WP02 or any approved source; the descriptive content
  belongs to the `EnterpriseObject`/recommendation, not `Task`).

Field list fixed to exactly `id`, `workspace_id`, `phase`,
`source_object_id`, `created_at`, `updated_at` — six fields, all with a
sourced basis (§10 of the Domain Review). Model, migration, and tests
only; no repository, service, or API, matching WP12a/WP13/WP16's
precedent.

### Amendment Approval Record (A-04)

```text
Decision: Approved (A-04)
Decider: Andrew (Project Owner)
Decision Date: 2026-08-04
Approved Commit or PR: PR #20 (`docs/task-lifecycle-domain-review`)
```

**A-05 rationale.** WP18's stated criteria — "events stored with trace
ID, correlation ID, type, source, timestamp" — were checked directly
against every candidate source, the same standard A-04 applied to WP15,
and none held up:

- **D01–D10**: zero hits for "trace id" or "correlation id" anywhere in
  `00_ARCHITECTURE/01_DOMAIN/`. `D07_STATE_SEMANTICS.md` mentions only
  "Event Delivery State" as technical messaging infrastructure, unrelated
  to this entity's persisted fields.
- **`docs/c4/C3_COMPONENT.md`**: names the same five fields, but its own
  Source column cites `MVP_WORK_PACKAGE_PLAN.md` for them — it quotes the
  WP plan rather than grounding it, the same circularity the Task Domain
  Review found for `priority`.
- **ADW-07** (Events, Audit, and Provenance): `ARCHITECTURE_SPECIFICATION.md`
  names it as owning "event semantics... correlation" — exactly what
  WP18 needs — and it is unwritten. `00_ARCHITECTURE/07_AUDIT/` does not
  exist as a directory.
- **Relationship to Task/EnterpriseObject** (the `source` field's
  implied semantics): GC-002 (`GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md`)
  remains an unapproved proposal. Its governance note originally cited
  `D09_RELATIONSHIP_MODEL.md` as governing `Event`→`Task`/source; D09
  scopes itself to six other concepts and never mentions Event. That
  citation was incorrect and has since been corrected in GC-002's
  governance note (2026-08-06), along with two further misattributions
  found in the same paragraph (`AuditRecord`→aggregate,
  `ContextPackage`→`Task`; see WP18's entry for the full enumeration).
  Correcting the citation does not resolve the underlying domain gap:
  `Event`'s relationship to `Task`/source still has no approved source.

Unlike A-02/A-04, this is not a narrowing to an approved subset — there
is no approved subset to narrow to. The amendment records WP18 as
blocked and withdraws the premature `Event` model/repository/service
deliverable wording (the same over-scope pattern A-02 corrected for WP13
and A-04 for WP15), pending ADW-07.

### Amendment Approval Record (A-05)

```text
Decision: Approved (A-05)
Decider: Andrew (Project Owner)
Decision Date: 2026-08-05
Approved Commit or PR: PR #22 (`docs/wp18-adw07-readiness-correction`)
```

**A-06 rationale.** WP20's stated criteria — "context package stores
sources, constraints, confidence, expiry" — were checked directly
against every candidate source, the same standard A-04/A-05 applied to
WP15/WP18, and none held up:

- **D01–D10**: `ContextPackage` is absent from D09's six declared
  concepts (Enterprise Object, Actor, Work Item, Decision, Business
  Operation, Runtime Session) and from its complete R1–R11 relationship
  matrix.
- **`docs/planning/PRE-CODING-BRIEF.md` §5.2**: this entry's own cited
  source. §5.2 describes a context snapshot surviving `RuntimeSession`
  termination, but never states the four-field list; `ContextPackage`
  otherwise appears in the document only once, as a bare entity name in
  the Architecture Traceability list.
- **Relationship to Task**: GC-002 (`GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md`)
  remains an unapproved proposal. Its governance note originally cited
  `D09_RELATIONSHIP_MODEL.md` as governing `ContextPackage`→`Task`; D09
  scopes itself to six other concepts and never mentions ContextPackage.
  That citation was incorrect and has since been corrected in GC-002's
  governance note (2026-08-06), alongside the same source-attribution
  discrepancy found for `Event` and `AuditRecord` in the same paragraph.
  Correcting the citation does not resolve the underlying domain gap:
  `ContextPackage`'s relationship to `Task` still has no approved
  source.
- **No interim stand-in**: unlike WP19, which has GC-006/GC-007 as
  named non-blocking interim defaults, WP20 has no equivalent — nothing
  stands in for the missing field-set source.

**Important distinction from A-05.** Unlike WP18, no approved document
explicitly assigns `ContextPackage` to ADW-06. ADW-06 is identified only
as the best-supported candidate governing workshop, inferred from its
published scope (`ARCHITECTURE_SPECIFICATION.md`: "knowledge states,
memory, context, validation, learning, retention, and retrieval")
overlapping "context" (and loosely "retention"). This amendment
therefore records an inference rather than an established authority
attribution.

A-05's ADW-07 dependency rests on a direct citation:
`ARCHITECTURE_SPECIFICATION.md` names ADW-07 as owning "event
semantics... correlation," a field-level match to WP18's correlation
ID. A-06's ADW-06 dependency rests on inference alone: none of WP20's
four stated fields appears in ADW-06's description, "ContextPackage"
does not appear in `ARCHITECTURE_SPECIFICATION.md` at all, and the link
is drawn from the shared word "context." "Retention" loosely maps to
"expiry"; the other three fields have no match.

Unlike A-02/A-04, this is not a narrowing to an approved subset — there
is no approved subset to narrow to. The amendment records WP20 as
blocked pending clarification of the governing domain source (candidate
governing workshop: ADW-06) and withdraws the premature `ContextPackage`
model/repository/service deliverable wording (the same over-scope
pattern A-02 corrected for WP13 and A-04 for WP15).

Unlike WP18, the blocking conclusion does not depend on ADW-06
ultimately proving to be the governing workshop. Even if another
workshop is later identified, the underlying problem is unchanged: the
field set, relationship semantics, and persistence shape currently have
no approved source. This amendment blocks implementation because the
authoritative source is missing — not because ADW-06 has been
established as that source.

### Amendment Approval Record (A-06)

```text
Decision: Approved (A-06)
Decider: Andrew (Project Owner)
Decision Date: 2026-08-08
Approved Commit or PR: PR #23 (`docs/wp20-adw06-readiness-correction`)
```

**A-07 rationale.** A WP10↔WP22 identifier-ownership audit found that no
approved source establishes who generates the per-HTTP-request identifier
both WPs name: WP10's deliverable ("JSON logs with request and
correlation identifiers") is the only place in the current plan claiming
it as an output, and WP22 depends on WP10 — a dependency order consistent
with WP10 as generator, WP22 as consumer, but not stated outright
anywhere.

**Planning ownership model selected:** WP10 nominally owns identifier
support; WP22 will own generation and propagation through this explicit
scope transfer. Existing authority does not independently establish that
WP10 must generate the identifier — an earlier draft of this finding
overstated a well-supported inference as a repository fact, corrected
here.

Verified against `backend/`: `app/core/logging.py` implements the JSON
formatter WP10 promised; no request or correlation identifier exists
anywhere in the codebase. WP10's narrowed scope (JSON logging alone) is
genuinely delivered — its status marker is not corrected to `🔴`, only
its written Deliverables are narrowed to match what's actually there,
consistent with the marker staying accurate rather than the WP being
reopened.

No precedent exists in A-01 through A-06 for transferring scope between
WP numbers — each prior amendment narrowed, withdrew, or split scope
within a single WP. This is recorded as the first instance of that shape,
not as an application of an existing one.

**Boundary recorded for WP22's transferred scope:** the identifier
identifies one HTTP request lifecycle only. It is a Tier-6 API/runtime
observability concern. It does not define, implement, alias, or
constrain Domain Event correlation, causation, provenance, distributed
tracing, or cross-request workflow identity — those remain ADW-07 and
ADW-08 territory, undecided. This boundary is a scope clarification, not
a new architectural decision — it asserts nothing about Tier-2 domain
concepts, only declines to claim anything about them.

### Amendment Approval Record (A-07)

```text
Decision: Approved (A-07)
Decider: Andrew (Project Owner)
Decision Date: 2026-08-11
Approved Commit or PR: PR #27 (`docs/a07-wp10-wp22-identifier-scope-transfer`)
```

**A-08 rationale.** ADR-0012 resolves WP22's envelope-scope alternative
as error-only, and explicitly places operational/infrastructure
endpoints such as `/health` outside that envelope's scope — they have no
current error path to govern and are consumed by orchestration tooling,
not application clients.

WP22's Definition of Done and Acceptance Criteria, as originally
recorded, both stated a broader guarantee than ADR-0012 establishes:
Definition of Done read "every endpoint returns the standard envelope
shape"; Acceptance Criteria read "a client can rely on one error shape
across the whole API." Both are unqualified, and both are broader than
the scope ADR-0012 §2 delivers. This narrows both to match the scope
established by ADR-0012 and WP22's existing planning boundary.

Classified as a scope correction, not an editorial clarification, on the
same reasoning A-02 and A-04 established: a WP's Definition of Done and
Acceptance Criteria are each read by a future auditor as a commitment in
their own right, and this repository's own convention (A-05, A-06) treats
"Definition of Done" as an independently authoritative clause, not a
silent restatement of Deliverables — the same reasoning extends to
Acceptance Criteria, which A-01 and A-04 already amended directly as
scope-bearing text, not descriptive prose. Excluding operational
endpoints and narrowing both fields' scope to the domain-facing API
withdraws recorded scope from what a literal reading of the prior text
promised on each — it is not merely restating what was already
understood.

This amendment does not define "domain-facing endpoint" as equivalent to
"WP13–WP21." WP13–WP21 is Deliverables' own historical scoping phrase,
for a different purpose, and is left untouched here; it is not reused as
the definition of either corrected field's scope, since WP13–WP21 is not
itself a durable semantic definition of "domain-facing API" — A-02/A-04
already removed API scope from some of those model WPs, and future
WP23–WP39 endpoints are domain-facing too. The corrected text for both
fields instead uses the semantic term "domain-facing API," matching
ADR-0012 §2's own boundary (application clients, not
operational/infrastructure consumers), not a WP-number list.

**Scope note:** as first drafted, this amendment narrowed only the
Definition of Done. Reviewing the full WP22 entry before commit surfaced
that Acceptance Criteria carries the identical over-broad claim, from
the identical cause (ADR-0012 §2) — leaving it uncorrected would have
left WP22's own entry internally inconsistent immediately after this
amendment landed: a domain-facing-scoped Definition of Done sitting next
to a whole-API-scoped Acceptance Criteria two lines below it. A-08 is
widened to cover both fields for that reason. This amendment has not yet
been merged or numbered against a PR, so no re-approval is formally
required — recorded here so the widening reads as deliberate, not as an
accumulation of unrelated changes.

**Definition of Done, corrected:** every domain-facing API endpoint
returns the standard error envelope on failure, per ADR-0012;
operational/infrastructure endpoints (e.g. `/health`) are outside that
envelope's scope.

**Acceptance Criteria, corrected:** a client can rely on one error shape
across the domain-facing API; operational/infrastructure endpoints (e.g.
`/health`) are outside that guarantee.

### Amendment Approval Record (A-08)

```text
Decision: Approved (A-08)
Decider: Andrew (Project Owner)
Decision Date: 2026-08-11
Approved Commit or PR: PR #28 (`docs/adr0012-a08-wp22-api-contract`)
```

**A-09 rationale.** ADR-0014 (Accepted, 2026-08-19) resolved Q1 of
WP19's subject-reference question — whether a persisted `AuditRecord`
must durably identify what it audited — as a new, shape-neutral Project
Owner decision, while leaving Q2 (the persisted structural shape of
that reference) explicitly open and creating a routing obligation that
uses ADW-07 — the future semantic destination already named by
`DECISION_0002` — as its resolution point. Unlike A-05/A-06, this is
not a case of an unwritten workshop leaving zero established
requirement — ADR-0014 itself is the requirement's authority. What it
shares with A-05/A-06 is the practical consequence: no model,
migration, repository, service, or field list satisfying the
requirement is authorized until Q2 resolves or an interim
representation is explicitly authorized, so WP19's status moves `🟢` →
`🔴` on the same readiness-and-scope-correction basis.

While drafting this amendment, the existing Deliverables wording —
"GC-006's own conservative Alternative B" and "GC-007's diff-only
shape" — was checked directly against GC-006 and GC-007's own
Recommendation sections (`GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md`)
and found to misattribute both: GC-006 recommends Alternative A (a
curated allowlist), not B; GC-007 recommends Alternative C (diff-based,
with field-sensitivity marking), not diff-only B alone, and GC-007's
own text argues against B alone specifically on secret-exposure
grounds. Both interim defaults WP19 actually uses (Alternative B; plain
diff) are unchanged by this correction — only their attribution is,
from "the proposal's own recommendation" to "WP19's own conservative
interim choice." This keeps `Risk`'s existing "diff-only default is
only safe until then" language coherent rather than contradicted.

### Amendment Approval Record (A-09)

```text
Decision: Approved (A-09)
Decider: Andrew (Project Owner)
Decision Date: 2026-08-19
Approved Commit or PR: PR #32 (`docs/adr0014-auditrecord-subject-reference`)
```

**A-10 rationale.** ADR-0013 (Accepted, 2026-08-16) classified
AgentDefinition as a D02 EnterpriseObject; ADR-0015 (Accepted,
2026-08-23) resolved the physical-persistence question ADR-0013 itself
left open — standalone persistence is the MVP default for D02
EnterpriseObject specializations, and AgentDefinition uses it. Together
with ADR-0009 §5's phase-lifecycle rule (made applicable to
AgentDefinition by ADR-0013's own stated scope) and ADR-0004's
independent workspace-scoping rule, the minimum physical schema for
AgentDefinition is now authorized by the accepted domain decisions
together with the established Gate C schema conventions: `id`,
`workspace_id`, `phase`, `owner_id`, `created_at`, `updated_at` — no
more, no fewer.

What they jointly establish is narrower than WP14's original stated goal
("configurable agent definition with capabilities and permissions") —
this amendment authorizes only the six-field schema foundation, not
capabilities, permissions, Provider/Model-referencing fields, runtime
configuration, or RuntimeSession wiring.

GC-001 (Provider/Model catalog scope) and ADW-05 (capabilities-versus-
permissions boundary and AgentDefinition's broader runtime semantics)
are **not resolved** by this amendment or by ADR-0013/ADR-0015. Both
remain genuinely open. What changes is narrower and specific: neither
is a blocker for the six fields above, because none of those fields
references a Provider, a Model, a capability, or a permission. Each
concern remains deferred to the later Work Package or architecture
decision that actually consumes it; A-10 does not re-route or resolve
those concerns.

No repository, service, or API is authorized in this schema-foundation
scope. ADR-0005/WP19 prevents unaudited state-changing service work,
consistent with the schema-first treatment already used in Gate C.

Status moves `🔴` → `🟡`: a schema foundation is unblocked while a real
runtime/configuration remainder stays open. WP14 does not become `🟢`;
the schema foundation's readiness does not imply the WP is complete.

### Amendment Approval Record (A-10)

```text
Decision: Approved (A-10)
Decider: Andrew (Project Owner)
Decision Date: 2026-08-24
Approved Commit or PR: PR #35 (`docs/wp14-a10-planning-sync`)
```

## Gate D — First Vertical Slice

| ID | Title | Priority | Depends On | Blocks | Deliverable / Acceptance Criteria |
|---|---|---:|---|---|---|
| WP23 | Business Request Intake API | P0 | WP13, WP15, WP16, WP22 | WP24 | Authenticated user creates request, object, and task |
| WP24 | Agent Selection and Assignment | P0 | WP14, WP15, WP23 | WP25 | Task assigned to Process Analysis Agent by explicit rule |
| WP25 | Minimal Context Assembly | P0 | WP20, WP23, WP24 | WP26 | Task and related object produce a valid context package |
| WP26 | LLM Provider Adapter | P0 | WP09, WP25 | WP27 | Provider-independent interface returns structured test response |
| WP27 | Agent Runtime Execution | P0 | WP17, WP21, WP25, WP26 | WP28 | One controlled session executes and stores output |
| WP28 | Structured Recommendation Result | P0 | WP27 | WP29 | Result includes summary, recommendation, confidence, assumptions |
| WP29 | Human Approval Flow | P0 | WP16, WP17, WP28 | WP30 | Approver can approve, reject, or request rework |
| WP30 | Decision Record and Events | P0 | WP18, WP19, WP29 | WP31, WP34 | Decision and related events/audit records persisted |
| WP31 | Task and Session Completion | P0 | WP21, WP30 | WP32 | Task/session statuses close consistently with result references |
| WP32 | Internal End-to-End Demo | P0 | WP23–WP31 | WP33–WP39 | Full scenario runs from request to visible approved result |

## Gate E — MVP Completion

| ID | Title | Priority | Depends On | Blocks | Deliverable / Acceptance Criteria |
|---|---|---:|---|---|---|
| WP33 | Command Center MVP Screen | P1 | WP15, WP18, WP30, WP32 | WP39 | Shows tasks, status, recommendation, decision, timestamps |
| WP34 | Enterprise Timeline MVP | P1 | WP18, WP30, WP32 | WP39 | Chronological events shown for one business request |
| WP35 | Enterprise Memory Entry | P1 | WP28, WP30 | WP39, WP45 | Approved result can be stored as validated memory entry |
| WP36 | Error Handling and Recovery | P1 | WP10, WP19, WP27 | WP37, WP39 | Provider, DB, validation, and execution failures remain visible and recoverable |
| WP37 | Integration Test Suite | P1 | WP11, WP23–WP36 | WP38, WP39 | Automated request-to-approval integration test passes |
| WP38 | Demo Data and Seed Script | P1 | WP37 | WP39 | One-command creation of user, agents, and demo scenario |
| WP39 | MVP Deployment and Runbook | P1 | WP12, WP33–WP38 | — | Docker Compose deployment, startup guide, demo guide, rollback notes |

## Gate F — Post-MVP Platform Expansion

| ID | Title | Priority | Depends On | Blocks | Deliverable / Acceptance Criteria |
|---|---|---:|---|---|---|
| WP40 | Redis Runtime Cache | P2 | WP39 | WP41, WP42 | Cache/session support introduced only with measured need |
| WP41 | Background Worker Queue | P2 | WP40 | WP42, WP58 | Long-running runtime tasks execute asynchronously |
| WP42 | Retry and Dead-Letter Handling | P2 | WP41 | WP58 | Failed jobs have bounded retries and visible dead-letter state |
| WP43 | Memory Retrieval Service | P2 | WP35 | WP44, WP47 | Relevant memory entries retrieved by filters and text search |
| WP44 | Semantic Retrieval | P2 | WP43 | WP47, WP55 | Embedding-based retrieval with source and confidence visibility |
| WP45 | Graph Node Projection | P2 | WP13, WP35 | WP46 | Core objects and memory projected into graph model |
| WP46 | Graph Relationships and Traversal | P2 | WP45 | WP47, WP55 | Typed relationships and neighborhood queries work |
| WP47 | Graph-Enriched Context | P2 | WP44, WP46 | WP55 | Context engine uses memory and graph results |
| WP48 | Additional Agent Configurations | P2 | WP14, WP27 | WP49 | Reviewer and Knowledge Curator run through same generic runtime |
| WP49 | Sequential Multi-Agent Handoff | P2 | WP48 | WP50, WP51 | Analysis agent hands result to reviewer agent |
| WP50 | Parallel Agent Workstreams | P3 | WP49 | WP51 | Two agent workstreams execute and merge results |
| WP51 | Conflict and Result Integration | P3 | WP49, WP50 | WP52 | Disagreement is surfaced and resolved by explicit strategy |
| WP52 | Escalation Engine | P2 | WP29, WP51 | WP53 | Authority, risk, and blocked-work escalation routes implemented |
| WP53 | Human-in-the-Loop Queue | P2 | WP52 | WP60 | Central queue for pending human actions |
| WP54 | Decision Option Model | P2 | WP30 | WP55 | Multiple options stored per decision |
| WP55 | Decision Scoring and Ranking | P2 | WP47, WP54 | WP56 | Transparent scoring and recommendation ranking |
| WP56 | Decision Outcome Analytics | P3 | WP55 | WP61 | Expected versus actual outcome tracking |
| WP57 | Workflow State Machine Service | P2 | WP15, WP18 | WP58, WP59 | Configurable state transitions and guards |
| WP58 | Durable Workflow Execution | P3 | WP42, WP57 | WP59 | Long-running workflow recovery and resumability |
| WP59 | Operational Alert Engine | P2 | WP18, WP36, WP57 | WP60 | Rules generate visible alerts from events and failures |
| WP60 | Expanded Command Center | P2 | WP53, WP59 | WP61 | Queues, alerts, approvals, runtime health views |
| WP61 | KPI and Decision Dashboards | P3 | WP56, WP60 | WP69 | Governed KPI and decision analytics views |
| WP62 | GitHub Integration Adapter | P2 | WP57 | — | Repository read/write adapter with audit events |
| WP63 | Email Integration Adapter | P3 | WP57 | — | Email intake and notification adapter |
| WP64 | Calendar Integration Adapter | P3 | WP57 | — | Calendar event and approval scheduling adapter |
| WP65 | Document Storage Adapter | P2 | WP57 | — | Documents stored by reference with metadata and access rules |
| WP66 | Advanced Audit Queries | P3 | WP19, WP34 | WP69 | Searchable audit histories and decision reconstruction |
| WP67 | Observability Metrics and Traces | P2 | WP10, WP18, WP39 | WP68 | OpenTelemetry-compatible traces and metrics |
| WP68 | Operational SLOs and Alerts | P3 | WP67 | WP69 | Initial latency, failure, queue, and availability objectives |
| WP69 | Post-MVP Platform Release | P2 | WP40–WP68 as selected | WP70 | Stable expanded platform release and review |

## Gate G — Productization and Enterprise Scale

| ID | Title | Priority | Depends On | Blocks | Deliverable / Acceptance Criteria |
|---|---|---:|---|---|---|
| WP70 | Tenant Model | P3 | WP69 | WP71–WP74 | Tenant isolation model and ownership boundaries |
| WP71 | Tenant-Aware Authorization | P3 | WP70 | WP74 | Permissions enforce tenant boundaries |
| WP72 | Tenant Configuration | P3 | WP70 | WP74 | Tenant-specific configuration and defaults |
| WP73 | Tenant Data Isolation Tests | P3 | WP70, WP71 | WP74 | Automated isolation validation |
| WP74 | Multi-Tenant Release | P3 | WP71–WP73 | WP75 | Multi-tenant platform baseline |
| WP75 | Agent SDK | P3 | WP69 | WP79, WP80 | Supported interface for defining agents |
| WP76 | Tool SDK | P3 | WP69 | WP79, WP80 | Supported tool adapter interface |
| WP77 | Workflow SDK | P3 | WP58, WP69 | WP79, WP80 | Supported workflow extension interface |
| WP78 | Integration SDK | P3 | WP62–WP65 | WP79, WP80 | Supported connector development interface |
| WP79 | Extension Validation and Signing | P4 | WP75–WP78 | WP80 | Security and compatibility validation process |
| WP80 | Agent and Tool Marketplace MVP | P4 | WP79 | WP81 | Catalog, install, permission review, versioning |
| WP81 | Marketplace Governance | P4 | WP80 | — | Review, deprecation, trust, and audit model |
| WP82 | Advanced Process Simulation | P4 | WP56, WP69 | WP83 | Scenario simulations and predicted KPI impact |
| WP83 | Digital Twin Runtime | P4 | WP46, WP82 | WP84 | Live process model connected to events and KPIs |
| WP84 | Enterprise Impact Analysis | P4 | WP46, WP83 | WP85 | Change impact traversal and risk view |
| WP85 | Enterprise Live Map | P4 | WP60, WP84 | — | Interactive graph/runtime/alert map |
| WP86 | Production Container Platform | P3 | WP69 or WP74 | WP87–WP89 | Production container deployment architecture |
| WP87 | Kubernetes Deployment | P4 | WP86, demonstrated scale need | WP88, WP89 | Kubernetes manifests/Helm and managed environments |
| WP88 | Horizontal Scaling and Resilience | P4 | WP87 | WP89 | Autoscaling, failover, disruption testing |
| WP89 | Production Observability Stack | P3 | WP67, WP87 | WP90 | Central logs, traces, metrics, alert routing |
| WP90 | Security Hardening and Threat Model | P3 | WP74 or WP86 | WP91 | Threat model, secrets, dependency and permission hardening |
| WP91 | Performance and Load Testing | P3 | WP89, WP90 | WP92 | Validated workload and capacity envelope |
| WP92 | Enterprise Release Readiness | P3 | WP88–WP91 | WP93 | Operations, security, support, recovery sign-off |
| WP93 | Bizzi Enterprise v1 Release | P4 | WP92 | — | Production enterprise release with documented scope |

---

## 08. MVP Exit Criteria

The MVP is complete when all of the following are true:

- the scenario in WP02 works end to end;
- one user can authenticate;
- one business request creates an object and task;
- one configured agent executes through the generic runtime;
- one context package is assembled and source-linked;
- one structured recommendation is produced;
- a human can approve, reject, or request rework;
- task, session, decision, event, and audit records remain traceable;
- the Command Center displays the full request history;
- an approved result can be stored in Enterprise Memory;
- integration tests pass;
- Docker Compose deployment and runbook work from a clean environment.

---

## 09. Explicit MVP Non-Goals

The following do not block MVP:

- coding all 83+ agents;
- native graph database;
- full semantic search;
- autonomous multi-agent negotiation;
- automatic conflict resolution;
- advanced decision scoring;
- advanced simulation;
- multi-tenancy;
- marketplace;
- Kubernetes;
- industry-specific domain suites;
- enterprise-scale integrations.

---

## 10. Architecture Traceability

| MVP Capability | Work Packages | Architecture Source |
|---|---|---|
| Object Management | WP13, WP23 | CORE Object Model, Canonical Data Model |
| Identity and Permissions | WP16, WP17 | PB058, Governance |
| Task Execution | WP15, WP21, WP24, WP27 | Layer 40, PB052 |
| Context | WP20, WP25 | PB040D, PB053 |
| Decisions | WP28–WP30 | CORE Decision Framework, PB055 |
| Events and Audit | WP18, WP19, WP30, WP34 | CORE Event Model, PB059 |
| Command Center | WP33, WP34 | Layer 44, PB056 |
| Memory | WP35 | PB034, Layer 39 |
| Knowledge Graph | WP45–WP47 | Layer 43, PB054 |
| Orchestration | WP48–WP53 | Layer 41 |
| Productization | WP70–WP93 | Future implementation track |

---

## 11. Planning Rules

- WP IDs do not imply strict execution order.
- Dependencies, not numbering, determine readiness.
- No P2–P4 package may delay the P0 critical path without explicit product-owner approval.
- Architecture work after closure must map to a concrete WP or discovered implementation risk.
- New agents should be configuration-first.
- New infrastructure should be introduced only after a demonstrated operational need.
- The first real user workflow takes priority over platform completeness.

---

## 12. Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-15 | Initial WP00–WP93 MVP dependency and prioritization plan |