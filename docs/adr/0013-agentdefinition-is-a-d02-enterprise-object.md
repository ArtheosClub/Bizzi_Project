# ADR-0013: AgentDefinition is a D02 EnterpriseObject

- Status: Accepted
- Date: 2026-08-16
- Deciders: Andrew (Project Owner) — decision recorded 2026-08-16;
  evaluated against the D02 five-criterion test derived in
  `docs/adr/DOMAIN_REVIEW_ENTERPRISE_OBJECT.md` §1, with the evidence
  assessment recorded in the Decision section below.
- Governance level: L3 (cross-module domain contract; this ADR applies
  the approved D02 classification to AgentDefinition and records the
  resulting lifecycle consequence under the ADR-0009 precedent). Applies
  approved D02 to a new concept; does not change D01–D10, so no
  Architecture Change Request under DECISION_0003 §11 is required.

## Context

`docs/adr/DOMAIN_REVIEW_ENTERPRISE_OBJECT.md` §5 posed one open question
covering two concepts:

> **Question for the Project Owner:** Are AgentDefinition and ContextPackage
> Enterprise Objects — in which case they inherit the §2 lifecycle and any
> addition (such as ContextPackage's expiry) needs its own basis — or are
> they concepts outside ADW-01's five, in which case their lifecycles are
> undetermined and WP14/WP20 cannot proceed on this review?

D05 (`APPROVED`) states Actor "is distinct from User Account, Role, Agent
Definition, and Runtime Session" — it says what AgentDefinition is *not*,
never what it *is*. D09 (`APPROVED — CLOSED`) names it in none of its six
domain-owning concepts or eleven canonical relationships.
`docs/adr/0009-enterprise-object-phase-lifecycle.md` §5 explicitly
declined to apply its `phase` field to AgentDefinition, deferring to this
exact question instead of assuming an answer.

**This ADR resolves the AgentDefinition half only.** ContextPackage's half
of the same question remains open — WP20 is still blocked on it. This ADR
does not touch, narrow, or imply an answer for ContextPackage.

The classifying test applied is the conjunctive five-criterion reading of
D02 that `DOMAIN_REVIEW_ENTERPRISE_OBJECT.md` §1 derives from D01, D02,
ADW-01 §3, and D07: durable; workspace-owned; business-relevant; has
governed state it authoritatively owns; and is not already one of Actor,
Work Item, Decision, or Business Operation.

## Decision

**AgentDefinition is a D02 EnterpriseObject.**

Stated honestly against the evidence, not as a stronger claim than the
record supports:

- Four criteria are reasonably supported by inference or partial
  authority; the workspace-ownership criterion is not established by
  existing approved authority and is resolved here by Project Owner
  architectural judgment.
- Durability, business relevance, and governed-state ownership are
  reasonably inferred from AgentDefinition's Tier-4 characterization as a
  configurable definition artifact; no Tier 2/3 source states these
  directly.
- The fifth criterion — not already one of Actor, Work Item, Decision, or
  Business Operation — is supported by approved authority for the Actor
  exclusion specifically (D05) and by inference for the remaining three.
- No approved source states whether AgentDefinition is workspace-owned or
  global. Unlike Provider/Model's still-open classification question, no
  competing proposal makes this criterion circular for AgentDefinition; it
  is a clean, standalone judgment call.
- This classification is Project Owner architectural judgment applying
  D02 to a concept D02 does not itself name. It is not a claim that
  D01–D10 compel this outcome.

## Consequences

**Easier.** AgentDefinition inherits D10 §6's Enterprise Object row in
full: physically deletable only if never referenced by any committed
Business Operation, Decision, or Work Item (§8 Invariant 5); archivable;
supersedable — "the standard mechanism for closing out a superseded
version while preserving history"; able to become obsolete at the type or
instance level; and able to become immutable once no further authoritative
mutation applies (D10 gives archived or superseded as examples).

ADR-0009's `phase` rule becomes applicable to AgentDefinition by that
ADR's own stated scope under this classification. Separate governance
recording, a Domain Review update, or a D09 clarification may still be
required; this ADR does not assume that applicability alone closes those
matters.

This reuses fully specified, already-approved mechanics rather than
requiring ADW-05 to design a bespoke lifecycle for AgentDefinition.

**Not settled by this decision, despite the classification.** R7–R9 may be
semantically applicable to AgentDefinition, since their predicates range
over Enterprise Object generically; whether that constitutes automatic D09
coverage or requires explicit confirmation remains unresolved.

D09 is `APPROVED — CLOSED`; its reach must not be expanded by
interpretation through this ADR. More concretely, the RuntimeSession ↔
AgentDefinition relationship is not covered by any of D09's eleven rows:
R5/R6 name Work Item and Business Operation specifically, not Enterprise
Object generically. D09's own supersession rule requires an explicit
Class A architecture decision to extend it. This classification does not
supply that decision.

WP21 remains blocked on the RuntimeSession ↔ AgentDefinition relationship,
in addition to its other stated dependencies, regardless of this ADR.

**Unaffected by this decision, and already settled independently.**
AgentDefinition's workspace-scoping requirement was never contingent on
this classification. `docs/adr/0004-workspace-scoped-multi-tenancy.md`'s
rule — every MVP table beyond `users` and `sessions` carries
`workspace_id` — is keyed to new-MVP-table status, not D02 membership.
AgentDefinition already carried this requirement before this ADR and
continues to after it, absent a future, separately proposed exception.

**WP14 becomes partially, not fully, determinate.** The lifecycle-field
question — whether `phase` applies — is now settled. Deliverables,
Definition of Done, and Acceptance Criteria remain undetermined: any
AgentDefinition fields referencing permitted providers/models await the
Provider/Model classification and catalog-scope question currently
represented by GC-001, and the capabilities-versus-permissions boundary
awaits ADW-05. This ADR does not fully unblock WP14.

WP21 gains only the fact that its link target is now EnterpriseObject-
shaped. It remains blocked on WP15, WP18, the RuntimeSession ↔
AgentDefinition relationship, and the broader ADW-05 runtime-resolution
contract.

**This decision does not settle:** Provider identity; Model identity;
Provider ↔ Model relationship; Provider/Model catalog scope; any GC-001
alternative; `WorkspaceProviderConfiguration`; capabilities versus
permissions; human-role versus agent-role authority; runtime Provider/
Model resolution; credential ownership, storage, or rotation; persistence
and transaction mechanics; D09 coverage; the RuntimeSession ↔
AgentDefinition relationship; or ContextPackage's own classification.

## Alternatives considered

**AgentDefinition is not a D02 EnterpriseObject.** AgentDefinition would
instead be a distinct durable concept whose identity, lifecycle, and
relationship semantics would need explicit ADW-05 definition, without
cancelling category-independent invariants such as ADR-0004's
workspace-scoping rule, D07's generally applicable state-ownership rule,
and D10 §9's Historical Preservation guarantee.

This alternative was rejected because no sourced, positive reason to
exclude AgentDefinition was found, unlike the explicit D10 §6 exclusions
that apply to Runtime Session and Event/AuditRecord. Choosing it would
require ADW-05 to define a separate lifecycle and relationship model
without a currently identified necessity.

D09's approved relationship model supplies no applicable R7–R9
relationship under Alternative B, because those predicates target an
Enterprise Object by definition. This does not imply that all D09
principles or invariants become irrelevant under Alternative B.

**A third category — Actor, Work Item, Decision, or Business Operation** —
has no evidence-supported basis. D05 explicitly excludes Actor by name;
the definitions of Work Item, Decision, and Business Operation make
membership implausible on their face, and no source proposes any of them
for AgentDefinition.

## Reversibility

Before implementation, reversal would primarily require a decision-record
and documentation change.

After production records exist, possible schema, data, and lifecycle
migration may be required, with the exact shape depending on the
implementation chosen after this decision. D10 §9's Historical
Preservation guarantee applies regardless of that shape: already committed
history must remain resolvable and cannot simply be deleted.

## References

- `docs/adr/DOMAIN_REVIEW_ENTERPRISE_OBJECT.md` §5 — the open question this
  ADR resolves, AgentDefinition half only
- `00_ARCHITECTURE/01_DOMAIN/ADW_01_DECISION_REGISTER.md` — D02
  (`APPROVED`), D05 (`APPROVED`), D09 (`APPROVED — CLOSED`), D10
  (`APPROVED — CLOSED`)
- `docs/adr/0009-enterprise-object-phase-lifecycle.md` — the lifecycle
  this decision makes applicable to AgentDefinition
- `docs/adr/0004-workspace-scoped-multi-tenancy.md` — the independent
  workspace-scoping consequence, unaffected by this decision
- `00_ARCHITECTURE/00_GOVERNANCE/DECISION_0002_AUTHORITY_HIERARCHY_AND_VOCABULARY_BASELINE.md`
  §3 — names AgentDefinition/Provider/Model as absent from ADW-01,
  governed by `PRE-CODING-BRIEF.md` until ADW-05; this ADR resolves
  AgentDefinition's category question specifically, ahead of and separate
  from ADW-05's remaining scope
- `00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md` §3 — Tier 0, Project
  Owner decision authority
- `DECISION_0003` §11 — governance classification and Architecture
  Change Request rules
- `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md` — WP14, WP21 entries
