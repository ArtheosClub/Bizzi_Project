# ADR-0015: Standalone persistence is the default for D02 EnterpriseObject specializations in the MVP

- Status: Accepted
- Date: 2026-08-23
- Deciders: Andrew (Project Owner) — decision recorded 2026-08-23.
- Governance level: L3 (cross-module domain/persistence contract —
  establishes standalone persistence as the default physical pattern for
  D02 EnterpriseObject specializations in the MVP. A specialization may
  use a different persistence shape only through a separate explicit
  decision justified by its concrete requirements). Applies to how an
  approved D02 classification is physically persisted; does not change
  D01–D10, so no Architecture Change Request under `DECISION_0003` §11 is
  required.

## Context

`docs/adr/0013-agentdefinition-is-a-d02-enterprise-object.md` classified
AgentDefinition as a D02 EnterpriseObject. No approved authority
established whether a D02 specialization should be physically
represented as:

- **A.** a corresponding `enterprise_objects` base row, plus a
  specialization table whose primary key is also a foreign key to that
  row; or
- **B.** a standalone specialization table carrying the mandatory
  EnterpriseObject contract (`id`, `workspace_id`, `phase`, `owner_id`,
  timestamps) directly, with no corresponding `enterprise_objects` row.

WP14's implementation pass stopped at this question correctly — it was
not architecturally authorized, and proceeding without authorization
would have been an irreversible decision made by implication rather than
by anyone actually deciding it.

The following evidence was considered and informs this decision, but none
of it, individually or together, itself establishes the answer:

- `enterprise_objects.type` exists and is documented in its migration
  (`backend/alembic/versions/c3e8b5d1f704_enterprise_object.py`) as "the
  specialization discriminator D02 implies" — Tier 6 implementation
  evidence, not architecture authority;
- the column is required (`NOT NULL`) but unconstrained — no CHECK, no
  enumerated value set;
- existing tests populate it on every `EnterpriseObject` row created, but
  none exercises specialization behavior — no polymorphic loader,
  type-based dispatch, joined specialization table, or PK=FK
  specialization pattern currently exists anywhere in the codebase;
- `test_database_accepts_any_type_string`
  (`backend/tests/test_enterprise_object_persistence.py`) explicitly
  proves that no specialization vocabulary is currently enforced, and is
  designed to fail if a CHECK is ever added, forcing the question back
  through Architecture Review rather than letting it ship silently;
- `00_ARCHITECTURE/01_DOMAIN/D09_RELATIONSHIP_MODEL.md` (`APPROVED —
  CLOSED`) rows R7, R8, R9, and R11 (lines 71–75) refer generically to
  Enterprise Object as their reference target, not to any specific
  specialization;
- `backend/app/models/task.py`'s `source_object_id` is a real
  implementation of R9, a single nullable foreign key to
  `enterprise_objects.id` — built before any specialization existed, so
  it was never itself a choice between A and B.

## Decision

**For the MVP, standalone persistence is the default physical
representation for D02 EnterpriseObject specializations.**

A standalone specialization carries the mandatory EnterpriseObject
contract directly in its own table, rather than requiring a
corresponding row in `enterprise_objects`.

**AgentDefinition will use this default.**

This ADR does not forbid a different representation for a future
specialization. A deviation from the default requires a separate,
explicit architecture decision based on that specialization's concrete
demonstrated requirements — not an automatic exception, and not an
automatic inheritance of this default either.

## Consequences

**This is a default, not a universal mandate.** It sets the MVP starting
point for D02 specializations; it does not fix the representation of
every future one. A future specialization may explicitly deviate through
its own decision.

**D09 is unchanged.** R7, R8, R9, and R11 retain their approved, generic
Enterprise Object semantics exactly as written. This ADR does not narrow,
reinterpret, or expand D09. Standalone persistence means this ADR simply
does not establish a physical mechanism for applying those generic
relationships to AgentDefinition — that mechanism, if and when a concrete
Work Package needs it, is a separate question.

**Reopen trigger.**

> The first concrete Work Package requiring an R7, R8, R9, or R11
> reference to AgentDefinition or another standalone D02 specialization
> is a mandatory architecture reopen trigger before implementation.

A separate Class A decision will be required to establish the physical
representation of that relationship, without silently narrowing or
expanding D09. This ADR does not license that extension in advance.

**`enterprise_objects.type` is unchanged by this ADR.** It remains `NOT
NULL`, unconstrained, and populated only for rows that actually exist in
`enterprise_objects`. AgentDefinition creates no `enterprise_objects` row
under the standalone default, so `type` is not populated for it. This
ADR does not add `agent_definition` to an enumerated type vocabulary,
does not establish `type` as a universal physical specialization
discriminator, and does not require changing
`test_database_accepts_any_type_string`. The column is not reinterpreted
or removed — it is simply not exercised by AgentDefinition under this
decision.

**Easier.** WP14's model, migration, and tests can proceed without a join
or a base-row creation step. Single-table reads and writes for
AgentDefinition-only access.

**Harder.** Any future cross-specialization query (e.g., "everything a
user owns across every Enterprise Object specialization") becomes a
UNION across N standalone tables rather than one `enterprise_objects`
query, growing with each future specialization that uses the default.

**Not decided by this ADR:**

- whether all future D02 specializations must use standalone tables —
  this establishes a default, not a mandate;
- ContextPackage's classification — it remains unclassified under its
  own open question (`docs/adr/DOMAIN_REVIEW_ENTERPRISE_OBJECT.md` §5).
  If it is later classified as a D02 EnterpriseObject, standalone
  persistence is the MVP default established here — but its concrete
  requirements may justify a separately approved deviation. It does not
  automatically inherit an irreversible rule;
- whether D09's R7–R9/R11 automatically apply physically to
  AgentDefinition;
- the future polymorphic reference mechanism, if one is ever needed;
- GC-001 or ADW-05's capabilities-versus-permissions boundary — both
  remain open for their respective later runtime, provider/model,
  authorization, and configuration concerns, but they are not
  prerequisites for the minimum WP14 schema foundation after this ADR;
- Provider/Model, RuntimeSession relationships, or any repository,
  service, or API layer work.

## Alternatives considered

**A — `enterprise_objects` base row plus a specialization table.** Real
advantages: generic D09 references could continue to target
`enterprise_objects.id` uniformly regardless of specialization; shared
fields (`workspace_id`, `phase`, `owner_id`) live once rather than being
redefined per specialization; cross-specialization queries stay simple
(one table). Rejected for the MVP default because: no current Work
Package demonstrates a need for polymorphic cross-specialization
references to AgentDefinition; it introduces a new joined-specialization
persistence pattern with no working precedent in the current backend (no
table's primary key is currently also a foreign key to
`enterprise_objects.id`); it carries immediate costs (two-row writes, a
join for full specialization reads, a cross-table consistency/orphan
concern where a `type`-tagged base row could exist without a matching
specialization row); and it requires an additional explicit decision
about the operational semantics of `enterprise_objects.type`, including
whether its value set remains open or becomes constrained. Per the
Abstraction Justification Rule (`CLAUDE.md`): "A new architectural
abstraction must either solve an existing, demonstrated problem, or be a
necessary precondition for implementing the next Work Packages.
Anticipated future need is not sufficient justification." Option A is not
justified as the MVP default now.

**Deciding persistence independently for every specialization, with no
recorded default.** Rejected: a fresh A/B decision for every D02
specialization would create repeated analysis and schema drift with no
stable baseline. This ADR establishes a default instead. Default ≠
mandate — a specialization may depart from it through a separately
approved architectural decision justified by concrete requirements.

## Reversibility

**Before WP14 implementation:** reversal is documentation-only — no
schema, data, or code exists yet to unwind.

**After standalone AgentDefinition data exists:** moving to the base-row-
plus-specialization-table shape requires a real data migration — creating
a corresponding `enterprise_objects` row for each existing
`agent_definitions` row, restructuring `agent_definitions.id` from a
plain primary key into a primary key that is also a foreign key to that
row, and rewriting any R7/R8/R9/R11 references created in the interim
under the reopen trigger above. This future cost is consciously accepted
for the MVP, in exchange for not paying Option A's costs now against a
need that is not currently demonstrated.

## References

- `docs/adr/0013-agentdefinition-is-a-d02-enterprise-object.md` — the D02
  classification this ADR builds on; the D09-reach boundary this ADR
  reaffirms rather than expands
- `00_ARCHITECTURE/01_DOMAIN/D09_RELATIONSHIP_MODEL.md` lines 71–75 — R7,
  R8, R9, R11, `APPROVED — CLOSED`; existing authority for the generic
  predicate wording, unchanged by this ADR
- `docs/adr/0009-enterprise-object-phase-lifecycle.md` — anti-duplication
  reasoning considered as evidence, not authority, for this decision
- `docs/adr/DOMAIN_REVIEW_ENTERPRISE_OBJECT.md` §5 — ContextPackage's
  still-open classification question, unaffected by this ADR
- `backend/alembic/versions/c3e8b5d1f704_enterprise_object.py` — the
  `type` column's documented (Tier 6) purpose and its deliberate lack of
  a CHECK constraint
- `backend/tests/test_enterprise_object_persistence.py` —
  `test_database_accepts_any_type_string`, unaffected by this decision
- `backend/app/models/task.py` — `source_object_id`, the one existing R9
  implementation, a single generic FK to `enterprise_objects.id`
- `CLAUDE.md` — the Abstraction Justification Rule, the basis for
  rejecting Option A as the MVP default
- `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md` — WP14 entry, to be
  synchronized by a separate amendment, not by this ADR
