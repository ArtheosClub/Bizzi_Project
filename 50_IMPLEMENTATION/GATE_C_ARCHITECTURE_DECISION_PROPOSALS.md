# Gate C — Architecture Decision Proposals

Version: 1.1
Status: **Draft — Architecture Analysis Only. No decision below is Approved.**
Implementation Track: 50_IMPLEMENTATION
Scope: Gate C / WP13–WP22, responding to §11 (Open Questions) of
`50_IMPLEMENTATION/GATE_C_WORKSPACE_ISOLATION_AND_AUDIT_ARCHITECTURE_REVIEW.md`
Decision Type: Architecture Decision Package for Project-Owner Review

Related documents:
- `50_IMPLEMENTATION/GATE_C_WORKSPACE_ISOLATION_AND_AUDIT_ARCHITECTURE_REVIEW.md` (source of all 10 open questions, §11)
- `docs/planning/PRE-CODING-BRIEF.md` §4, §5.1–5.3, §7, §8
- `docs/c4/C3_COMPONENT.md`
- `docs/adr/0004-*.md`, `0005-*.md`, `0006-*.md`
- `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`

## Purpose and boundaries of this document

This is an **architecture analysis artifact**, not an implementation
artifact. It converts each of the 10 open questions in the Architecture
Review's §11 into a formal Architecture Decision Proposal, so the project
owner can approve, reject, or amend each one individually at an
architecture review meeting.

**This document does not modify** `docs/adr/`, `docs/c4/`, `docs/planning/`,
or `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`. No ADR is updated, no
planning document is changed, no code, database model, or migration is
created, and no implementation task is opened. Those actions happen only
after every decision below is approved or amended by the project owner —
per the Architecture Review's own §12 Approval Rule.

Every recommendation below is a **proposal**, not a decision already made.

---

## GC-001 — Provider and Model Catalog Scope

### Context

`PRE-CODING-BRIEF.md` §5.3 establishes a provider-neutral context/result
envelope architecture (Canonical Context Envelope → Provider Adapter →
provider-specific request → Model execution → Canonical Result Envelope),
and `TECH_STACK.md` explicitly excludes pinning any LLM/agent provider SDK,
requiring it to sit behind a provider-adapter boundary. The Architecture
Review's entity classification (§02.1) lists `Provider`/`Model` as
"Global or workspace-configured / Conditional," and its §02.2 recommends a
split between a global catalog and workspace-scoped configuration, without
this being formally decided.

### Problem Statement

Should `Provider` and `Model` be global singleton catalog rows shared
across all workspaces, or fully duplicated per workspace? This affects
schema design, credential security, multi-tenant cost/residency policy,
and the effort required to onboard a new provider or model.

### Architectural Alternatives

**A — Global catalog + separate `WorkspaceProviderConfiguration`**
(the Review's own §02.2 recommendation)

- Description: `Provider`/`Model` are global, admin-managed catalog
  tables, no `workspace_id`. A separate
  `WorkspaceProviderConfiguration(workspace_id, provider_id,
  credentials_ref, enabled, cost_policy, residency_policy,
  permitted_model_ids[])` row per workspace–provider pair captures
  everything tenant-specific.
- Advantages: no duplication of static vendor metadata; a new
  platform-wide model is instantly available (pending workspace opt-in);
  clean separation of "what exists" vs. "what a workspace may use and
  how"; credentials structurally isolated to a workspace-scoped table,
  never touching the global catalog.
- Disadvantages: every provider resolution requires a two-table join;
  requires disciplined enforcement that runtime never reads `Provider`
  without going through `WorkspaceProviderConfiguration`.
- Risks: sloppy enforcement could let a service execute against a global
  `Provider` row without checking workspace enablement — mitigated by
  funneling all resolution through one service.
- Operational impact: admin-managed catalog, likely seed/fixture-driven;
  low ongoing overhead.
- Long-term maintenance: easy to add providers/models platform-wide (one
  row); `WorkspaceProviderConfiguration` grows linearly with
  workspace × enabled-provider pairs — manageable.

**B — Fully workspace-scoped, duplicated rows**

- Description: `workspace_id` directly on `Provider` and `Model`; every
  workspace gets its own copies.
- Advantages: uniform with every other Gate C entity — no "conditional"
  case to explain.
- Disadvantages: massive duplication of static vendor metadata per
  workspace; catalog drift risk (one workspace's copy goes stale);
  platform-wide model deprecation becomes an N-workspace operation.
- Risks: data drift across workspaces; higher migration burden on every
  catalog change.
- Operational impact: every new workspace needs a seed/copy step.
- Long-term maintenance: high — every vendor metadata change becomes a
  backfill across all workspace rows.

**C — Hybrid: `Model` global, `Provider` workspace-scoped**

- Description: fold what Alternative A calls
  `WorkspaceProviderConfiguration` directly into a workspace-scoped
  `Provider` row; keep `Model` global.
- Advantages: one fewer table than Alternative A.
- Disadvantages: conflates "the vendor exists" with "this workspace's
  configured connection to the vendor" — doesn't cleanly support multiple
  credentials per vendor per workspace (e.g., prod/sandbox keys); blurs
  exactly the catalog-vs-configuration split the Review wanted.
- Risks: likely needs to split into two tables anyway once
  multi-credential need arises, causing a later migration.
- Operational impact: similar to A, muddier semantics.
- Long-term maintenance: medium — the simplification is likely illusory.

### Recommendation

**Alternative A.** It matches the Review's own §02.2 recommendation and is
architecturally consistent with the provider-neutral envelope pattern
already established in `PRE-CODING-BRIEF.md` §5.3 — that pattern exists
specifically to separate the canonical/global provider abstraction from
workspace-specific execution, which is exactly what Alternative A does at
the schema level. It is the only alternative that keeps credentials
structurally out of any global table (directly serving ADR-0004's
isolation intent and the CLAUDE.md stop condition on raw secrets), scales
cleanly as providers/models are added, and avoids per-workspace metadata
drift.

### Architecture Impact

- Domain model: two new entities (`Provider`, `Model` global;
  `WorkspaceProviderConfiguration` workspace-scoped) instead of one merged
  concept.
- Repositories: `Provider`/`Model` get simple global-catalog repositories
  — the one deliberate, documented exception to ADR-0004's blanket rule;
  `WorkspaceProviderConfiguration` gets a standard workspace-scoped
  repository.
- Database: two new tables beyond what `C3_COMPONENT.md` currently
  implies.
- APIs: provider/model listing is a global read; workspace provider
  configuration is workspace-scoped CRUD.
- Authorization: enabling a provider for a workspace is a
  permission-gated, audited action.
- Auditing: `WorkspaceProviderConfiguration` changes (enable/disable,
  credential rotation) are high-impact, audited mutations (see GC-006).
- Context Engine/Runtime: provider resolution during a `RuntimeSession`
  must always go through `WorkspaceProviderConfiguration` — never read
  credentials from the global catalog, because there are none there to
  read.

### Dependencies

- Requires ADR-0004 update documenting this as an explicit, named
  exception to the flat-`workspace_id` rule.
- Requires `WorkspaceProviderConfiguration` to be added to the Gate C
  entity list (currently absent from WP13–WP22 as named in
  `MVP_WORK_PACKAGE_PLAN.md`).
- Requires the Context Engine/Runtime's provider-resolution code path to
  enforce "never resolve without a `WorkspaceProviderConfiguration`
  lookup."

### Risks

If the `WorkspaceProviderConfiguration` lookup is ever bypassed, a
workspace could invoke another workspace's enabled model without cost or
residency controls — needs an R-02-equivalent repository invariant applied
specifically to provider resolution.

### Decision Stability

- Can change during Gate C? **YES** — this is exactly when the entity
  shape gets built.
- Can change after MVP? Technically yes, at high cost.
- Requires data migration? **YES**, if changed after data exists.
- Requires API breaking change? **YES**, for any provider/config API
  consumer.
- Estimated future change cost: **High** — Gate D's WP26 (LLM Provider
  Adapter) directly depends on this shape; changing it after Gate D ships
  means migrating live runtime configuration.

### Questions Requiring Owner Approval

Whether `WorkspaceProviderConfiguration` needs its own WP number in the
Gate C register, or folds into an existing WP's scope (WP14 or WP21) —
this is a work-package-register question outside this analysis-only
phase's scope, but it follows directly from approving this decision.

---

## GC-002 — Composite Foreign Keys for Cross-Workspace Consistency

### Context

Review §03.4: a foreign key to a globally unique UUID does not guarantee
two related records share a workspace. It names two patterns —
repository/service invariant plus tests (default), and stronger composite
`(workspace_id, id)` foreign keys — recommending the latter "for the most
critical relationships if SQLAlchemy/Alembic complexity remains
manageable," without naming a final, approved scope.

**Governance synchronization note (2026-07-23):** the domain-semantic
question of what these relationships *are* — `AuditRecord`→aggregate,
`ContextPackage`→`Task`, `RuntimeSession`→`Task`, `Event`→`Task`/source —
is governed by `00_ARCHITECTURE/01_DOMAIN/D09_RELATIONSHIP_MODEL.md`
(APPROVED — CLOSED), not by this proposal. This proposal addresses only
the persistence-layer enforcement mechanism for relationships D09 already
defines. Per
`00_ARCHITECTURE/00_GOVERNANCE/DECISION_0002_AUTHORITY_HIERARCHY_AND_VOCABULARY_BASELINE.md`'s
Vocabulary Baseline, audit/event relationship semantics specifically are,
as a future concept, provisionally governed by this proposal (GC-002)
pending ADW-07 (Events, Audit, and Provenance), which has not yet been
written. This note does not change the alternatives, recommendation, or
any other content below — see `00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md`
§3 for the full Authority Hierarchy.

### Problem Statement

For each Gate C relationship between workspace-scoped entities, decide
whether to rely purely on application-level (repository invariant + test)
enforcement, or add database-level composite FK constraints — and produce
an explicit, approved list of which relationships get which treatment.

### Architectural Alternatives

**A — Repository/service invariant only, everywhere**

- Description: every relationship enforced by loading the related entity
  through the same `workspace_id` in code, backed by negative tests
  (R-05, GC-TEST-03). No composite FKs anywhere.
- Advantages: simplest schema; conventional SQLAlchemy models; least
  Alembic complexity; fastest to implement uniformly across WP13–WP22.
- Disadvantages: the isolation guarantee lives entirely in application
  code — a bug in one repository method, or a careless future addition,
  can silently create a cross-workspace link with no database backstop.
  This is exactly the category the Review marks **Critical**.
- Risks: regression risk grows as more repositories are added by future
  contributors, including AI-generated code (R-AI-001).
- Operational impact: none extra.
- Long-term maintenance: every new relationship is one more place
  discipline can lapse.

**B — Composite FKs for the Review's named four, invariant elsewhere**

- Description: `AuditRecord`→aggregate, `ContextPackage`→`Task`,
  `RuntimeSession`→`Task`, `Event`→`Task`/source get DB-level
  `(workspace_id, id)` composite FK enforcement; everything else relies
  on repository invariant plus tests.
- Advantages: database-level guarantee exactly where a cross-workspace
  leak is most damaging — audit trail integrity and context/session
  linkage — turning R-DATA-001 from "must remember to test" into "cannot
  physically happen," while bounding schema complexity to four
  relationships.
- Disadvantages: composite FK modeling in SQLAlchemy is more verbose
  (composite unique constraint on the parent, composite FK on the child,
  explicit `primaryjoin`); two conventions to teach and review instead of
  one; composite-FK Alembic migrations are more failure-prone to hand-write
  correctly.
- Risks: if the ORM model and the actual migration diverge (constraint
  declared in code but not actually created in the database), this
  produces false confidence — mitigated by requiring GC-TEST-01 (migration
  tests inspect actual DB constraints, not ORM metadata) as a hard
  dependency.
- Operational impact: none beyond initial build cost.
- Long-term maintenance: medium — one clear, documented rule, unlike
  case-by-case judgment.

**C — Composite FKs for every workspace-scoped relationship**

- Description: no exceptions — every FK between workspace-scoped
  entities becomes a composite `(workspace_id, id)` FK.
- Advantages: maximum database-level guarantee everywhere; no
  case-by-case judgment needed later.
- Disadvantages: significant schema/migration complexity across all
  Gate C entities; every parent table needs a composite unique constraint
  in addition to its primary key; slows Gate C velocity for a guarantee
  that invariant + negative tests already cover adequately for lower-risk
  relationships.
- Risks: low incremental security benefit over Alternative B for most
  relationships.
- Operational impact: larger migrations, more constraint-related failure
  modes.
- Long-term maintenance: raises the implementation bar for every future
  Gate D+ relationship.

### Recommendation

**Alternative B.** It matches the Review's own explicit list and
concentrates the more expensive database-level guarantee on the
highest-consequence relationships — the audit trail and context/session
linkage — consistent with ADR-0005's audit-first principle. Alternative
C's uniform rigor is disproportionate to the marginal risk it removes for
lower-stakes relationships; Alternative A leaves precisely the
entities the Review calls Critical risk unprotected at the database layer.

### Architecture Impact

- Domain model: `AuditRecord`, `ContextPackage`, `RuntimeSession`, `Event`
  gain composite FK columns/constraints referencing the parent's
  `(workspace_id, id)`.
- Repositories: these four need composite-aware query construction.
- Database: `Task` and `EnterpriseObject` need `UNIQUE(workspace_id, id)`
  in addition to their primary key, to be valid composite FK targets.
- APIs: unaffected directly.
- Auditing: directly hardens the audit subsystem's integrity guarantee.
- Context Engine/Runtime: `ContextPackage`/`RuntimeSession`'s link to
  `Task` becomes database-enforced, closing a gap relevant to
  `PRE-CODING-BRIEF.md` §5.2's context-survival model.

### Dependencies

- Requires ADR-0004 update documenting which relationships get composite
  FK treatment.
- Requires GC-DB-04 and GC-TEST-01 as hard implementation dependencies.
- Requires `Task`/`EnterpriseObject` repositories to expose the
  `(workspace_id, id)` unique constraint other Gate C entities reference.
- Subject to `00_ARCHITECTURE/01_DOMAIN/D09_RELATIONSHIP_MODEL.md` for
  relationship semantics, and provisionally governs audit/event
  relationship semantics pending ADW-07 per
  `DECISION_0002_AUTHORITY_HIERARCHY_AND_VOCABULARY_BASELINE.md` (see
  Context, above).

### Risks

Composite FK migrations are more error-prone to hand-write; mitigated by
requiring GC-TEST-01 to catch a missing/incorrect constraint in CI rather
than production.

### Decision Stability

- Can change during Gate C? **YES**.
- Can change after MVP? **YES**, at real cost.
- Requires data migration? **YES** — adding a composite FK after data
  exists requires validating/backfilling existing rows first.
- Requires API breaking change? **NO** — purely a persistence-layer
  guarantee.
- Estimated future change cost: **High** — retrofitting DB constraints
  onto live data is materially harder than defining them at initial
  migration time.

### Questions Requiring Owner Approval

Confirm the four-relationship scope itself — if a different scope is
wanted (e.g., also composite-FK `Task`→`EnterpriseObject`), that is an
explicit call to make here, not assumed.

---

## GC-003 — Membership Invitation Row Occupancy

### Context

Review §04.2 defines a `WorkspaceMembership` lifecycle
(Invited→Active→Suspended→Revoked) but does not state whether an
"invitation" occupies the `UNIQUE(workspace_id, user_id)` row from the
start, or whether invitation is a separate concept entirely.

### Problem Statement

Does creating an "Invited" `WorkspaceMembership` occupy the unique
membership slot immediately, or is a separate `WorkspaceInvitation` entity
used, with `WorkspaceMembership` created only on acceptance?

### Architectural Alternatives

**A — Invitation occupies the membership row immediately**
(matches the Review's own §04.2 state model directly)

- Description: inviting a user creates
  `WorkspaceMembership(workspace_id, user_id, status=Invited)`
  immediately; acceptance transitions status to `Active`.
- Advantages: single entity/table for the whole lifecycle, no new entity
  type; `UNIQUE(workspace_id, user_id)` naturally prevents double-inviting
  the same user; one full audit trail on one entity.
- Disadvantages: requires the invited user to already have a `User` row
  — invites to an email address with no account yet aren't covered by
  this model alone.
- Risks: if "invite by email, no account yet" is a real MVP requirement,
  this needs a bolt-on regardless.
- Operational impact: none significant at MVP scale.
- Long-term maintenance: low — one entity type, extensible later with a
  new ADR per Review §04.4 if states need to change.

**B — Separate `WorkspaceInvitation` entity**

- Description: `WorkspaceInvitation(workspace_id, email, invited_role,
  token, expires_at)`, not subject to `UNIQUE(workspace_id, user_id)`;
  `WorkspaceMembership` created only on acceptance.
- Advantages: naturally supports inviting by email before the invitee has
  an account; keeps `WorkspaceMembership`'s meaning strictly "confirmed
  relationship."
- Disadvantages: two entities where the Review implied one; more moving
  parts (token generation/expiry, cleanup) for an MVP whose scope may not
  need invite-by-email at all.
- Risks: scope creep relative to what WP16 actually requires, against
  `PRE-CODING-BRIEF.md` §4's tight MVP scope cap.
- Operational impact: requires invitation-expiry handling.
- Long-term maintenance: more code surface, cleaner separation if rich
  invitation flows are needed later.

### Recommendation

**Alternative A for the MVP**, with an explicit non-goal noting
invite-by-email-to-nonexistent-user is out of scope. The MVP scenario
(`PRE-CODING-BRIEF.md` §7 — "pass the recommendation to the owner for
approval") implies a small number of known users per workspace, not a
self-serve invite flow, and WP16 is titled "Minimal" Identity and
Authentication. Alternative A matches the Review's own state model with
zero new entities. If email-invite becomes a real requirement later,
Alternative B is a clean additive layer on top, not a rework.

### Architecture Impact

- Domain model: `WorkspaceMembership` is the only new identity-adjacent
  entity, with status enum Invited/Active/Suspended/Revoked.
- Repositories: standard workspace-scoped CRUD plus a "resolve effective
  membership" read path (§04.5).
- APIs: an endpoint to create a membership in `Invited` status
  (admin/owner-only), and one to accept it.
- Authorization: creating a membership is itself a permission-gated,
  audited action.
- Auditing: every state transition produces an immutable audit record
  (GC-MEM-04).

### Dependencies

Requires ADR-0004/ADR-0006 updates per Review §09.1/§09.3; requires
WP16/WP17 to include this exact state model.

### Risks

If MVP scope silently grows to need email invites mid-Gate-C, this becomes
a scope-creep pressure point — flagged explicitly so it is a conscious
decision, not a surprise.

### Decision Stability

- Can change during Gate C? **YES**.
- Can change after MVP? **YES** — additive; Alternative B can layer on
  top without touching existing `WorkspaceMembership` rows.
- Requires data migration? **NO** for the additive path.
- Requires API breaking change? **NO**, additive.
- Estimated future change cost: **Low** — one of the more easily deferred
  decisions in this package.

### Questions Requiring Owner Approval

Confirm invite-by-email-to-nonexistent-user is genuinely out of MVP
scope — it is not currently listed in `MVP_WORK_PACKAGE_PLAN.md` §09
Non-Goals, so this proposal asserts a new non-goal that needs explicit
confirmation, not assumption.

---

## GC-004 — Membership Role Model: Single Role vs. Role Join

### Context

Review §02.1/§04 assumes `WorkspaceMembership` carries a role, but does
not state whether one role per membership is sufficient for MVP, or
whether a membership-to-role join (multiple simultaneous roles) is
required. ADR-0006 already describes an "owner-only checks... RBAC-ready
shape" posture for MVP authorization.

### Problem Statement

Is a single `role` column on `WorkspaceMembership` sufficient, or does
Gate C need a membership-to-role join table supporting multiple roles per
user per workspace?

### Architectural Alternatives

**A — Single `role` column, one role per membership**

- Description: `WorkspaceMembership.role` is a single value (enum or FK
  to a small static role catalog).
- Advantages: matches ADR-0006's existing MVP posture directly; trivially
  satisfies `UNIQUE(workspace_id, user_id)` with deterministic role
  resolution (Review §04.5); simplest to implement and test for WP17.
- Disadvantages: cannot express "this user is both Reviewer and
  Approver" without a coarser combined role; a genuine multi-role need
  later would be a breaking schema change, not a data backfill.
- Risks: low for MVP — `PRE-CODING-BRIEF.md` §4's 3–5-role cap concerns
  agent runtime roles, and nothing in the MVP scenario implies a human
  needs multiple simultaneous workspace roles.
- Operational impact: none.
- Long-term maintenance: low now, medium later only if multi-role
  becomes a real requirement.

**B — Membership-to-role join table**

- Description: `WorkspaceMembershipRole(membership_id, role)`; a user's
  permissions are the union of all attached roles.
- Advantages: future-proof against multi-role needs without a later
  schema change; role assignment becomes an independent, auditable action.
- Disadvantages: adds a table and a join to every authorization check for
  a capability nothing in the current MVP scenario or ADR-0006 asks for —
  directly against this project's own "don't design for hypothetical
  future requirements" discipline and R-SCOPE-001 (a named Critical
  risk).
- Risks: premature complexity.
- Operational impact: marginally higher query cost on every
  authorization check.
- Long-term maintenance: higher near-term cost for a deferred, unconfirmed
  benefit.

### Recommendation

**Alternative A.** ADR-0006 already commits the MVP to a single-role
posture by construction. Building the join table now is exactly the kind
of speculative complexity R-SCOPE-001 exists to prevent. If multi-role
need emerges, the migration path (add join table, migrate existing
single-role data, one row per existing membership) is bounded and
well-understood.

### Architecture Impact

- Domain model: `WorkspaceMembership.role` as a single field.
- Repositories: role resolution is a direct column read, no join.
- Authorization: ADR-0006's existing model applies unchanged.
- Auditing: role-change audit record (GC-MEM-04) records a simple
  old/new value diff.

### Dependencies

Requires ADR-0006 update per Review §09.3, confirming this single-role
posture explicitly (currently implied, not stated).

### Risks

If a multi-role need emerges mid-Gate-C, that requires a scope
discussion, not a silent workaround.

### Decision Stability

- Can change during Gate C? **YES**.
- Can change after MVP? **YES**, additive migration path exists.
- Requires data migration? **YES**, if changed later.
- Requires API breaking change? **YES** — any API returning `role:
  string` would need to become `roles: string[]`.
- Estimated future change cost: **Medium** — the DB migration is
  mechanical, but the API shape change ripples to every
  authorization-consuming client.

### Questions Requiring Owner Approval

None — this follows directly from ADR-0006's already-stated MVP posture;
included here for explicit, formal confirmation since the Review listed
it as open.

---

## GC-005 — Cross-Workspace Access API Behavior

### Context

Review §07/R-07: "attempting to access an entity from another workspace
must behave as not found or denied according to the API security policy,
without revealing its existence." This states a principle but not a
specific, approved HTTP-status rule.

### Problem Statement

When an authenticated user with valid membership in Workspace A requests
an entity that actually belongs to Workspace B, what should the API
return?

### Architectural Alternatives

**A — Uniform 404 for all cross-workspace entity access**

- Description: the API never reveals that an entity exists in a
  workspace the caller cannot access; a cross-workspace request looks
  identical to a request for a nonexistent ID.
- Advantages: strongest information-security posture — doesn't leak
  entity existence across tenant boundaries; matches R-07 verbatim;
  simplest rule for repository implementers — every scoped lookup that
  misses is just "not found."
- Disadvantages: conflates "truly doesn't exist" with "exists but
  forbidden" into one status, marginally complicating legitimate
  client-side debugging.
- Risks: minimal — the conservative, security-first default.
- Operational impact: none.
- Long-term maintenance: low — one rule, no per-endpoint judgment calls.

**B — Explicit 403 when the entity exists in another workspace**

- Description: the service distinguishes "no row at all" (404) from "row
  exists, wrong workspace" (403).
- Advantages: more informative for legitimate API consumers; conventional
  REST semantics.
- Disadvantages: **to return 403 correctly, the service must perform an
  existence check outside workspace scope first — exactly the unscoped,
  global-ID lookup ADR-0004/R-02 prohibits.** This is the most important
  finding among these three alternatives: it puts this decision in direct
  tension with the Review's own Repository Acceptance Criteria
  (GC-REP-01).
- Risks: high — a developer could "fix" a missing 403 by adding precisely
  the bare `get_by_id(id)` the Review explicitly prohibits.
- Operational impact: none beyond implementation risk.
- Long-term maintenance: higher — every workspace-scoped endpoint needs
  an extra unscoped-existence-check path, and every future entity has to
  remember to replicate it correctly.

**C — Policy-dependent: 404 for entities, 403 only at the membership
level**

- Description: workspace-membership checks (is this user in this
  workspace at all?) may return 403, since that is a check against the
  trusted `ActorContext`, not an unscoped entity lookup; per-entity
  lookups always return 404.
- Advantages: gets Alternative A's information-hiding benefit for entity
  data while still giving a meaningful 403 at the coarser
  membership boundary, without ever performing an unscoped ID lookup.
- Disadvantages: two rules instead of one, needing consistent
  documentation and application.
- Risks: low, but requires WP22's API standard to state this split
  explicitly.
- Operational impact: none.
- Long-term maintenance: low-medium.

### Recommendation

**Alternative A** for entity-level access. Note that the
workspace-membership check (§04.5) already naturally produces its own
distinct deny response at a different point in the request pipeline —
before any entity lookup occurs — so Alternative C's distinction largely
already exists as a byproduct of the membership-resolution flow, without
needing a separately documented rule. The decisive factor against
Alternative B is that it structurally requires the exact unscoped lookup
pattern GC-REP-01 prohibits — recommending it would put this decision and
the repository-invariant decision in direct contradiction with each
other.

### Architecture Impact

- APIs: every workspace-scoped GET/PUT/PATCH/DELETE returns 404 on any
  workspace mismatch, no exceptions — to be documented in WP22's API
  error/response standard.
- Repositories: requires no new code path — this is the natural behavior
  of always querying `WHERE workspace_id = :workspace_id AND id = :id`
  (R-02); a wrong-workspace row simply doesn't match.
- Authorization: workspace-membership-level denial is a separate, earlier
  pipeline check, not in tension with the 404-for-entities rule.

### Dependencies

Requires WP22 to state this rule explicitly; requires ADR-0006 update to
state the membership-vs-entity distinction.

### Risks

None significant — the lowest-risk alternative of the three.

### Decision Stability

- Can change during Gate C? **YES**.
- Can change after MVP? Technically yes, but changing 404→403 later adds
  information disclosure — unlikely to be revisited once shipped.
- Requires data migration? **NO**.
- Requires API breaking change? Changing this later is a breaking change
  for any client branching on status code.
- Estimated future change cost: **Low to decide now, Medium-High to
  reverse later** — cheap now, expensive to walk back.

### Questions Requiring Owner Approval

None — Alternative A restates the Review's own explicit invariant (R-07)
as a formal decision; included for sign-off since §11 listed it as open.

---

## GC-006 — High-Impact Mutation Classification

### Context

ADR-0005 and the Review (R-08, R-09, GC-AUD-04) require that "high-impact
mutations cannot commit without their required audit record" and that
business mutation plus audit write happen atomically "where practical" —
but no enumerated list exists yet for Gate C's actual entities.

### Problem Statement

Which specific mutation types on Gate C's entities are "high-impact" and
therefore require an atomic (same-transaction) business-write-plus-audit
write, versus mutations that are still always audited but without the
same hard atomicity requirement?

### Architectural Alternatives

**A — Curated allowlist**

- Description: an explicit, initial list — `EnterpriseObject`
  create/status-change; `Task` create/status-change/reassignment;
  `AgentDefinition` create/permission-change; `WorkspaceMembership`
  create/role-change/status-change; `RuntimeSession`
  start/complete/fail; approval/decision actions —  reviewed and expanded
  as later gates add mutation types.
- Advantages: directly actionable for WP19; bounds atomic-transaction
  complexity to genuinely high-stakes actions; reviewable against
  `DEVELOPMENT_PLAN.md` §9's stop condition on missing audit events.
- Disadvantages: requires active maintenance — every new mutation type in
  later gates needs a conscious classification decision.
- Risks: medium — an unclassified new mutation could ship without atomic
  audit coverage if classification is skipped; mitigated by making it
  part of each WP's Definition of Ready.
- Operational impact: none.
- Long-term maintenance: medium — a small, evolving, reviewable list.

**B — Blanket rule: every mutation is high-impact**

- Description: all creates/updates/deletes on all Gate C entities require
  an atomic audit write, no triage.
- Advantages: zero ambiguity; maximally conservative.
- Disadvantages: forces genuinely low-stakes mutations through
  atomic-transaction ceremony disproportionate to their risk; makes the
  audit trail noisier, potentially burying the events that matter most
  (approvals, permission changes) — undercutting ADR-0005's own purpose
  of a trustworthy, reviewable trail.
- Risks: low correctness risk, real usability/signal-to-noise risk.
- Operational impact: higher write volume/storage; every mutation pays
  transaction overhead.
- Long-term maintenance: low ambiguity, higher ongoing noise/storage
  cost.

### Recommendation

**Alternative A.** `DEVELOPMENT_PLAN.md` §9's stop condition already
requires *an* audit event for every state-changing action regardless of
which alternative is chosen — what's actually being decided is narrower:
which mutations need *atomic* audit writes. Given the MVP's small,
bounded scope, a curated list matching the Review's own named examples is
concrete enough to implement directly without inventing a blanket rule
that adds transactional overhead to low-stakes mutations and dilutes the
audit trail's signal.

### Architecture Impact

- Domain model: no new entities; `AuditRecord.action` taxonomy should
  mark which actions are on the high-impact list.
- Repositories: high-impact mutations wrap business write + audit write
  in one transaction (R-09); all other mutations still always produce an
  audit record, without the same hard atomicity requirement.
- Auditing: core of WP19's scope.
- Context Engine/Runtime: `RuntimeSession` start/complete/fail is
  explicitly on the high-impact list given its centrality to
  `PRE-CODING-BRIEF.md` §5.2's context-survival model.

### Dependencies

Requires ADR-0005 update (Review §09.2) to carry the explicit list, not
just the principle; requires WP19's acceptance criteria to reference it
directly.

### Risks

List omissions in future gates — mitigated by making classification part
of each new WP's Definition of Ready.

### Decision Stability

- Can change during Gate C? **YES** — refinable as WP13–WP22 are built.
- Can change after MVP? **YES**, additive.
- Requires data migration? **NO**.
- Requires API breaking change? **NO**.
- Estimated future change cost: **Low** — a governance/documentation
  artifact, not a schema commitment.

### Questions Requiring Owner Approval

**The exact contents of the high-impact list.** The alternative above
proposes a starting list grounded in the MVP scenario and the Review's
own examples, but which actions count as high-impact is inherently a
business-risk judgment call, not a purely architectural one, and needs
explicit owner confirmation or amendment.

---

## GC-007 — Audit Before/After State Representation

### Context

GC-AUD-05 requires audit records to "preserve actor, action, target,
timestamp, correlation ID, and before/after references or approved
summaries" — leaving open whether this means full snapshots, diffs,
references, or a sensitivity-aware combination.

### Problem Statement

Should `AuditRecord` store full before/after entity snapshots, a
structured diff, an external reference, or a sensitivity-aware
combination of these?

### Architectural Alternatives

**A — Full before/after JSON snapshots**

- Description: every audited mutation captures the complete entity state
  before and after as JSON.
- Advantages: maximum reconstructability — any historical state reads
  directly from the audit table; simplest query model.
- Disadvantages: a raw secret or PII appearing in a snapshot is a direct
  path to violating the CLAUDE.md/`DEVELOPMENT_PLAN.md` §9 stop condition
  on raw secrets in logs/events/responses, unless every entity's
  serialization is scrubbed — a real risk once GC-001's
  `WorkspaceProviderConfiguration` (holding credential references)
  exists; storage grows quickly for large or frequently-mutated entities.
- Risks: high if scrubbing is inconsistent — easy to get right once and
  regress on when a new field is added without updating the
  audit-scrubbing logic.
- Operational impact: higher storage cost, scaling with entity size ×
  mutation frequency.
- Long-term maintenance: every entity needs an explicit, reviewed
  "what's safe to snapshot" serializer.

**B — Diff-only**

- Description: store only the changed fields
  (`{"field": "status", "before": "open", "after": "closed"}`).
- Advantages: much smaller storage footprint; naturally scoped to what a
  reviewer actually cares about; reduces (but doesn't eliminate) secret
  exposure surface since only changed fields are captured.
- Disadvantages: reconstructing full state at time T requires replaying
  the whole diff chain; a diff-computation bug could misrepresent what
  actually changed.
- Risks: diff-computation correctness becomes its own thing to test.
- Operational impact: lower storage cost than A.
- Long-term maintenance: medium — diff logic is shared-kernel code that
  must stay correct across all entities.

**C — Sensitivity-aware combination**

- Description: extend either base approach with a required field-level
  sensitivity tag (e.g., on `WorkspaceProviderConfiguration.
  credentials_ref`, `User.email`) that is always redacted or
  reference-only in the audit record, regardless of the general
  snapshot/diff choice.
- Advantages: directly closes the secret-exposure risk both A and B
  leave partially open; makes "is this field safe to audit-log" an
  explicit, reviewable schema property; composes with either A or B.
- Disadvantages: requires building and maintaining a field-sensitivity
  classification mechanism — more upfront design work.
- Risks: if classification is incomplete (a new sensitive field added
  without marking), the same exposure risk as A resurfaces.
- Operational impact: similar to whichever base it's paired with.
- Long-term maintenance: requires the classification registry to be kept
  current — an ongoing but well-defined task.

### Recommendation

**Alternative C, using diff (Alternative B's shape) as the default base,
with explicit field-sensitivity marking.** Raw-secret-in-logs/events/
responses is a named, non-negotiable Stop Condition in this project, not
a nice-to-have — any design storing full entity snapshots without a hard
sensitivity mechanism is one missed field-scrub away from tripping it,
and GC-001 guarantees at least one entity with genuinely sensitive fields
will exist in Gate C. Diff-based storage also better fits ADR-0005's
audit-first philosophy — the trail exists primarily to answer "what
changed and who did it," which a diff answers more directly and cheaply
than a full snapshot.

### Architecture Impact

- Domain model: `AuditRecord.before_state`/`after_state` become
  structured diff objects rather than full entity dumps; a new
  cross-cutting field-sensitivity marking concern needs to be added to
  the shared kernel/base model layer.
- Repositories: the audit-write path needs a diff-computation step aware
  of sensitivity markers.
- Auditing: core WP19 scope.
- APIs: audit-record-read endpoints return diffs, which the Command
  Center needs to render as a diff view rather than a snapshot view.

### Dependencies

Requires ADR-0005 update (Review §09.2; GC-AUD-05's "before/after
references or approved summaries" language already points this
direction); requires a shared-kernel field-sensitivity mechanism to exist
*before* any entity with sensitive fields (notably
`WorkspaceProviderConfiguration` from GC-001) is modeled.

### Risks

The sensitivity-classification mechanism is new design surface not yet
specified anywhere in this codebase — this decision creates a dependency
on infrastructure that doesn't exist yet and needs its own design pass
before WP19 can be considered ready.

### Decision Stability

- Can change during Gate C? **YES**.
- Can change after MVP? Changing the audit storage shape after real
  history exists is expensive — old records would need migration or
  permanent dual-format support.
- Requires data migration? **YES**, if changed after data exists.
- Requires API breaking change? **YES**, for any audit-viewer consumer.
- Estimated future change cost: **High** — audit records are meant to be
  immutable/permanent (§05.6), so retroactive shape changes are unusually
  costly compared to other entities.

### Questions Requiring Owner Approval

Whether the field-sensitivity classification mechanism should be its own
small ADR (it is shared-kernel infrastructure, not specific to any one
entity), rather than assuming it folds silently into ADR-0005 or the
proposed ADR-0008.

---

## GC-008 — System Templates: `workspace_id = NULL` vs. Separate Global Tables

### Context

Review §02.1 classifies `PermissionProfile` as "Workspace-scoped unless
system template," and §02.3's Mandatory Rule requires every mutable
business record to satisfy exactly one of: owns a non-null `workspace_id`;
is a documented immutable global catalog record; or is a workspace-enforced
child. A nullable `workspace_id` on an otherwise workspace-scoped table is
not one of these three categories.

### Problem Statement

Should immutable, platform-shipped permission templates live in the same
table as workspace-owned permission profiles with `workspace_id = NULL`
meaning "system template," or in a physically separate global table?

### Architectural Alternatives

**A — Same table, nullable `workspace_id`**

- Description: `PermissionProfile.workspace_id` is nullable; `NULL` rows
  are immutable system defaults, non-`NULL` rows are workspace-owned.
- Advantages: one table, one repository, one API surface; system and
  workspace rows share the same shape naturally.
- Disadvantages: **this is the single sharpest violation of ADR-0004's
  own stated invariant** ("no major runtime object may exist without
  workspace_id") **and directly contradicts the Review's own §02.3
  Mandatory Rule**, which explicitly states this ambiguous middle case
  "is not permitted." Every repository method touching this table needs
  a `NULL`-aware branch — precisely the kind of special-casing that
  raises the chance of an accidental cross-workspace leak.
- Risks: high — this is the Review's own named anti-pattern, not a
  neutral design choice.
- Operational impact: none extra.
- Long-term maintenance: higher risk surface for every future contributor
  touching this table.

**B — Separate global `SystemPermissionTemplate` + workspace-scoped
`PermissionProfile`**

- Description: `SystemPermissionTemplate` (no `workspace_id`, genuine
  global catalog) and `PermissionProfile` (`workspace_id` `NOT NULL`,
  always). A workspace "adopts" a template by copying it into its own
  `PermissionProfile` row at onboarding time.
- Advantages: matches §02.3's three-way classification cleanly — every
  table has one unambiguous category, no nullable-`workspace_id` special
  case anywhere; structurally identical to the GC-001 recommendation
  (global catalog + workspace-scoped operative record), keeping the
  schema's design vocabulary consistent across two independent decisions.
- Disadvantages: two tables and two repositories instead of one;
  "adopting" a template requires an explicit copy step at
  workspace-onboarding time.
- Risks: low — this is the Review's own §02.3 rule applied directly.
- Operational impact: slightly more onboarding logic (seed default
  `PermissionProfile` rows from `SystemPermissionTemplate` on workspace
  creation).
- Long-term maintenance: low — clean, consistent classification.

### Recommendation

**Alternative B.** Alternative A directly contradicts the Review's own
§02.3 Mandatory Rule in the very document this proposal responds to —
recommending it would mean this proposal ignores its own source
material's explicit prohibition. Alternative B is also structurally
identical to the GC-001 recommendation, so adopting it establishes one
repeated, well-understood "global catalog + workspace-scoped instance"
pattern applied consistently, rather than two different ad hoc solutions
to the same underlying shared-vs-per-tenant problem.

### Architecture Impact

- Domain model: two entities instead of one for permissions
  (`SystemPermissionTemplate`, `PermissionProfile`), mirroring GC-001's
  `Provider`/`WorkspaceProviderConfiguration` split.
- Repositories: `SystemPermissionTemplate` is a simple global-catalog
  repository (the same documented ADR-0004 exception as `Provider`/
  `Model`); `PermissionProfile` is fully workspace-scoped, no exceptions.
- Authorization: WP17 reads exclusively from `PermissionProfile`, never
  from `SystemPermissionTemplate` directly at runtime — templates are
  only a seeding source.
- Workspace onboarding: new workspace creation must seed default
  `PermissionProfile` rows from the current `SystemPermissionTemplate`
  set.

### Dependencies

Requires ADR-0004 update documenting this as the second explicit
global-catalog exception alongside `Provider`/`Model` (GC-001), not a
one-off; requires WP17 to include the template-seeding step at workspace
creation.

### Risks

If workspace-creation seeding is skipped or buggy, a workspace could end
up with zero usable `PermissionProfile` rows — needs a test analogous to
GC-TEST-04 verifying every new workspace gets its default profiles.

### Decision Stability

- Can change during Gate C? **YES**.
- Can change after MVP? Changing A→B after A ships requires migrating
  every `NULL`-`workspace_id` row into a new table and updating every
  workspace's profile references — a real migration. B→A is unlikely to
  ever be wanted given A's structural problems.
- Requires data migration? **YES**, if reversed later.
- Requires API breaking change? Likely, if permission-profile endpoints
  currently expose a single unified list.
- Estimated future change cost: **Medium-High**.

### Questions Requiring Owner Approval

None architecturally — this follows directly from the Review's own §02.3
rule; included for formal sign-off since §11 listed it as open.

---

## GC-009 — Retention Policy for Revoked Memberships and Audit Records

### Context

Review §04.4 recommends soft-revoking memberships (never physically
deleting participants in business/audit history) and §05.6 requires audit
records to be append-only/immutable — but no retention or archival
horizon is stated for either.

### Problem Statement

How long are revoked `WorkspaceMembership` rows and `AuditRecord` rows
retained — indefinitely, or under a defined deletion/archival policy?

### Architectural Alternatives

**A — Indefinite retention, no deletion path in the MVP**

- Description: revoked memberships and all audit records are kept
  forever; no purge job, no archival tier.
- Advantages: simplest possible implementation — nothing to build for
  Gate C; the natural extension of §05.6's append-only/immutable
  requirement; avoids the risk of deleting something that turns out to be
  legally or operationally needed later.
- Disadvantages: no mechanism yet for legitimate future deletion needs
  (e.g., a data-subject deletion request, or a workspace closure wanting
  its data gone) — but nothing in the planning corpus currently names
  this as an MVP requirement either.
- Risks: storage growth over time; not a near-term concern at MVP scale.
- Operational impact: none for MVP; a Gate F+ (Post-MVP Platform
  Expansion) concern once scale and compliance requirements are real.
- Long-term maintenance: low now; a real retention/deletion policy needs
  its own ADR later, once the need is concrete.

**B — Time-based retention policy defined and implemented now**

- Description: explicit TTL/archival job built as part of Gate C (e.g.,
  audit records retained N years, revoked memberships purged after N
  months).
- Advantages: avoids unbounded storage growth from day one; satisfies a
  compliance requirement early, if one exists.
- Disadvantages: **no stated compliance requirement exists yet to size
  the policy against** — any N chosen now is a guess, not a grounded
  decision; adds archival/purge-job scope to Gate C not named in any
  WP13–WP22 deliverable; if "purge" is interpreted as deleting audit
  records, this is in tension with §05.6's immutability principle and is
  a much bigger decision than Gate C's scope should carry alone.
- Risks: choosing a retention period without a compliance driver risks
  picking wrong and redoing it once real requirements are known.
- Operational impact: new scheduled job/infrastructure to build and
  monitor.
- Long-term maintenance: retention policy is normally compliance-driven;
  building it now without that input risks work that doesn't match
  eventual real requirements.

### Recommendation

**Alternative A for the MVP.** No compliance, legal, or contractual
retention requirement is named anywhere in this codebase's planning
corpus, and retention policy is fundamentally a business/compliance
decision that architecture should implement, not originate. Building a
guessed policy now risks wasted work and, worse, risks deleting audit
data that turns out to matter — directly working against ADR-0005's core
purpose. This is flagged explicitly as a deferred decision requiring
business/legal input, not silently deferred by omission.

### Architecture Impact

None for Gate C — no new entities, no purge jobs, no additional schema.
The impact of this decision is the *absence* of scope, worth recording so
it is not silently assumed to already be handled elsewhere.

### Dependencies

None for Gate C. A future retention-policy ADR needs input from whoever
owns compliance/legal concerns for the platform — outside pure
architecture.

### Risks

Unbounded long-term storage growth, not an MVP-scale concern; flagged for
revisit at Gate F+ when real usage volume and any compliance requirements
become known.

### Decision Stability

- Can change during Gate C? **N/A** — no Gate C implementation depends on
  this.
- Can change after MVP? **YES**, explicitly meant to be revisited later.
- Requires data migration? **NO**.
- Requires API breaking change? **NO**.
- Estimated future change cost: **Low** — adding a retention policy later
  doesn't require undoing anything Gate C builds.

### Questions Requiring Owner Approval

Whether any compliance/legal retention requirement already exists that
hasn't surfaced in the planning corpus — if so, Alternative B needs
revisiting with that concrete requirement as input, rather than this
proposal's assumption that none exists.

---

## GC-010 — Index/Query Benchmarking Requirement

### Context

Review §03.2 provides an Index Matrix grounded in named query patterns
(workspace+status, workspace+owner, workspace+correlation_id, etc.), but
does not state whether this matrix requires empirical benchmarking before
approval, or can be approved as specified and validated later.

### Problem Statement

Which list and dashboard queries, if any, must be benchmarked against
representative data before the Index Matrix is finalized and approved?

### Architectural Alternatives

**A — Approve the matrix as specified; validate empirically during Gate C**

- Description: treat the Review's §03.2 matrix as a reasonable,
  well-grounded first-pass design, implement it as specified, and rely on
  Gate C's own test suite (GC-TEST-07) plus normal query-plan review to
  catch problems.
- Advantages: no benchmarking infrastructure needed before Gate C starts;
  the matrix is already grounded in concretely named query patterns
  (§03.1), not speculative; MVP data volumes are small (`MVP_WORK_
  PACKAGE_PLAN.md` §08's exit criteria describe one end-to-end scenario,
  not a load target), so premature performance benchmarking is unlikely
  to surface real signal yet.
- Disadvantages: if the matrix has a genuine gap — a query pattern not in
  §03.2 — it won't be caught until it's slow in practice, potentially
  post-MVP.
- Risks: low at MVP scale; grows at Gate F+ scale, out of this decision's
  scope.
- Operational impact: none for Gate C.
- Long-term maintenance: normal — index tuning from real usage is a
  standard, ongoing DB-ops practice, not a one-time Gate C task.

**B — Require empirical benchmarking against synthetic data before approval**

- Description: generate synthetic multi-workspace data at a target scale
  and measure query plans/latency for every §03.2 pattern before the
  matrix is considered approved.
- Advantages: empirically validates the matrix instead of relying on
  judgment alone; could catch a genuinely missing composite index before
  it ships.
- Disadvantages: the MVP's own exit criteria name **no** representative
  data volume to benchmark against — any synthetic volume chosen would
  itself be a guess, undermining the rigor benchmarking is supposed to
  provide; adds real scope to Gate C for a concern the MVP's own success
  criteria don't mention at all.
- Risks: benchmarking against an arbitrary volume risks false confidence
  (fine at the guessed volume, breaks at real volume) or false alarm
  (over-engineering for a volume never reached).
- Operational impact: requires building synthetic-data-generation tooling
  before schema work can be considered approved.
- Long-term maintenance: the tooling has ongoing value for future
  performance work, but is front-loaded cost against an MVP with no
  stated performance target.

### Recommendation

**Alternative A.** `MVP_WORK_PACKAGE_PLAN.md` §08 contains no
performance or scale target — the scenario is one request, one task, one
agent execution, one approval, not a load benchmark. Requiring formal
benchmarking before index approval would optimize against an undefined
target, risking the same premature, hypothetical-future-requirement
engineering this project's conventions warn against elsewhere. The
Review's §03.2 matrix is already grounded in real Gate C/D functionality
(task queues, audit timelines, session status) — the right level of rigor
for this stage. Real benchmarking belongs at Gate F+, once actual usage
patterns and target scale exist to benchmark against.

### Architecture Impact

None beyond what GC-002/the Review's §03.2 already specifies — this
decision is about process (when/whether to benchmark), not schema shape.

### Dependencies

GC-TEST-07 (pagination/counting/search/aggregation isolation tests)
remains required regardless of this decision — it is a correctness test,
distinct from a performance benchmark.

### Risks

If MVP demo data volumes turn out larger than assumed, some queries could
be slow at demo time — low-probability given §08's scenario is
single-digit-record scale; worth a lightweight sanity check (not full
benchmarking) before the Gate D demo (WP32).

### Decision Stability

- Can change during Gate C? **YES**.
- Can change after MVP? **YES** — explicitly meant to be revisited at
  Gate F+.
- Requires data migration? **NO** — adding indexes later doesn't require
  migrating data, only index migrations.
- Requires API breaking change? **NO**.
- Estimated future change cost: **Low** — indexes can be added or
  adjusted post-MVP without disrupting schema shape or APIs.

### Questions Requiring Owner Approval

None — a process/rigor-level decision within architecture's normal
judgment; included for formal sign-off since §11 listed it as open.

---

## Decision Register

| Decision ID | Title | Recommended Option | Status |
|---|---|---|---|
| GC-001 | Provider and Model Catalog Scope | A — Global catalog + workspace-scoped `WorkspaceProviderConfiguration` | Requires Owner Decision |
| GC-002 | Composite Foreign Keys for Cross-Workspace Consistency | B — Composite FKs for AuditRecord/ContextPackage/RuntimeSession/Event; invariant + tests elsewhere | Proposed |
| GC-003 | Membership Invitation Row Occupancy | A — Invitation occupies the membership row immediately | Requires Owner Decision |
| GC-004 | Membership Role Model | A — Single `role` column, one role per membership | Proposed |
| GC-005 | Cross-Workspace Access API Behavior | A — Uniform 404 for entity-level access | Proposed |
| GC-006 | High-Impact Mutation Classification | A — Curated allowlist | Requires Owner Decision |
| GC-007 | Audit Before/After State Representation | C — Diff-based, with field-sensitivity marking | Requires Owner Decision |
| GC-008 | System Template Workspace Scope | B — Separate global `SystemPermissionTemplate` + workspace-scoped `PermissionProfile` | Proposed |
| GC-009 | Retention Policy for Revoked Memberships / Audit Records | A — Indefinite retention, defer policy | Requires Owner Decision |
| GC-010 | Index/Query Benchmarking Requirement | A — Approve matrix as specified, validate empirically later | Proposed |

**No decision above is Approved.** Every row requires explicit
project-owner sign-off — the "Proposed" vs. "Requires Owner Decision"
split reflects only whether a genuine open question or business-risk
judgment call remains beyond the architectural recommendation itself (see
each proposal's "Questions Requiring Owner Approval"), not a difference in
confidence in the recommendation.

**Governance cross-reference (2026-07-23):** GC-002's persistence-enforcement
scope is distinct from, and subordinate to, D09 (Relationship Model,
`00_ARCHITECTURE/01_DOMAIN/D09_RELATIONSHIP_MODEL.md`, APPROVED — CLOSED)
for what these relationships mean; GC-002 itself provisionally governs
audit/event relationship semantics pending ADW-07, per
`DECISION_0002_AUTHORITY_HIERARCHY_AND_VOCABULARY_BASELINE.md`. This does
not change GC-002's Status (`Proposed`) or recommended option above — the
underlying Gate C persistence-layer decision remains open for
project-owner approval independent of this cross-reference.

## What happens after this package is reviewed

Per the Architecture Review's own §12 Approval Rule, none of the
following begins until every decision above is approved or amended:

- ADR-0004, ADR-0005, ADR-0006 updates (per each proposal's Dependencies)
- the proposed new ADR-0008 (Gate C Data Isolation, Indexing, and
  Repository Invariants)
- `docs/c4/C3_COMPONENT.md` and `docs/planning/PRE-CODING-BRIEF.md`
  updates reflecting the approved entity/index/membership/audit shapes
- `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` updates for any newly
  identified scope (e.g., `WorkspaceProviderConfiguration`,
  `SystemPermissionTemplate`)
- any Gate C model, repository, migration, or implementation task

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-19 | Initial Architecture Decision Package — GC-001 through GC-010, responding to the Architecture Review's §11 Open Questions |
| 1.1 | 2026-07-23 | Governance Execution Step 8: added D09/DECISION_0002 cross-references to GC-002 (Context, Dependencies) and the Decision Register, so this document no longer discusses AuditRecord/ContextPackage/RuntimeSession/Event relationship enforcement without acknowledging D09 (Relationship Model) as the now-approved domain-semantics authority. No GC-001–GC-010 recommendation, alternative, or status changed. |
