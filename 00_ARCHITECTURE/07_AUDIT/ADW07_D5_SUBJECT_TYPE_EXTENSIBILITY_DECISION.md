# ADW-07 / Q2 D5 — Subject-Type Set / Extensibility Decision

**Status:** ACCEPTED  
**Decision:** D5 — CLOSED / ACCEPTED  
**Decision Date:** 2026-08-30  
**Decision Owner:** Project Owner / Andrew  
**Parent:** ADW-07 — Events, Audit and Provenance  
**Scope:** ADR-0014 Q2 / D5 subject-type set and extensibility requirement only

## 1. Accepted rule

> **For the current ADR-0014 Q2 decision, the persisted AuditRecord subject-reference representation MUST support all five currently accepted subject types: `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, and `Task`. These five types define the current Q2 acceptance scope, not a permanently closed audited-subject universe. Any future auditable subject type requires separate explicit architecture authority and MUST satisfy the then-applicable D1–D4 subject-reference invariants. D5 does not require the current persistence representation to admit arbitrary future subject types without migration, configuration, schema change, or representation evolution, and it does not pre-authorize wildcard, `Unknown`, `Other`, or implementation-defined subject kinds.**

## 2. Extensibility guardrails

D5 additionally establishes two explicit guardrails:

1. **Extensibility convenience MUST NOT by itself determine, rank, or default the Q2 persistence representation.** A candidate does not become preferred merely because it appears easier to extend to hypothetical future subject types.
2. **Technical encodability does not confer architecture authority.** A future subject type does not become a valid audited subject merely because the selected persistence mechanism can technically encode another discriminator or identifier form. Separate explicit architecture authority is required first.

These guardrails prevent D5 from becoming an implicit candidate-selection mechanism.

## 3. Current acceptance scope

The current Q2 acceptance scope is exactly the five existing D1 subject types:

- `Workspace`;
- `EnterpriseObject`;
- `User`;
- `WorkspaceMembership`;
- `Task`.

A Q2 persistence representation must satisfy the accepted D1–D4 semantic requirements for all five current types.

D5 does not require one mechanism to encode arbitrary future types without later evolution.

## 4. Future subject types

A future auditable subject type may be introduced only by separate explicit architecture authority.

Such a future decision must:

- explicitly add or revise the accepted subject-type set;
- preserve the then-applicable D1–D4 subject-reference invariants;
- evaluate compatibility with the then-current persistence representation;
- decide whether migration, schema evolution, configuration change, resolver evolution, or another architecture change is required.

D5 does not pre-authorize placeholders, wildcards, `Unknown`, `Other`, or implementation-defined discriminator values.

## 5. Candidate neutrality

D5 does **not** select, prefer, rank, reject, approve, or default any Q2 representation candidate.

In particular:

- N2/N3 are not disfavored merely because future subject types may require schema evolution;
- N1/N4/N5 are not favored merely because they may appear more open-ended;
- GC-002 Alternative B remains **PROPOSED ONLY** and receives no authority or default status from D5;
- C3 extensibility remains a comparative/evolution consideration, not an independent mandatory preference rule.

## 6. Relationship to D1–D4

- **D1 — CLOSED / ACCEPTED:** current subject references have explicit durable type disambiguation.
- **D2 — CLOSED / ACCEPTED:** `Workspace` is a first-class audited subject and context does not substitute for subject identity.
- **D3 — CLOSED / ACCEPTED:** historical audited-subject identity survives later lifecycle change.
- **D4 — CLOSED / ACCEPTED:** subject identity is mandatory, durable, explicit, stable, independently resolvable, and distinct from actor attribution / ActorContext / context / association / route / payload.
- **D5 — CLOSED / ACCEPTED:** current five types are sufficient for Q2 acceptance; future types require separate explicit architecture authority; open-ended zero-migration extensibility is not required now.

D5 does not redefine D1–D4.

## 7. Actor-attribution / ActorContext boundary

D5 concerns only the audited-subject type set.

It does not define actor types, actor identity, ActorContext, initiator/service-principal categories, attribution persistence, or actor extensibility. Those remain separate unresolved architecture surfaces.

Actor categories must not be folded into the audited-subject type set by implication.

## 8. Persistence representation remains open

**Q2 persisted representation remains OPEN / NOT ESTABLISHED.**

D5 does not select:

- N1 polymorphic reference;
- N2 composite-FK-derived representation;
- N3 per-type nullable representation;
- N4 opaque identifier;
- N5 in-payload representation;
- or another separately evaluated representation.

D5 does not choose fields, columns, discriminator storage, FK/composite-FK shape, payload layout, registry, resolver implementation, enforcement layer, migration, model, repository, service, API, backend, or tests.

## 9. Dependency and implementation boundary

D5 does not restore a WP18 → WP19 dependency.

WP19 model/migration implementation remains **BLOCKED / UNAUTHORIZED pending explicit Q2 persisted-representation resolution**, unless Project Owner separately issues explicit bounded interim-shape authorization.

D5 acceptance alone does not make WP19 buildable.

## 10. Decision state

- D1: **CLOSED — ACCEPTED**;
- D2: **CLOSED — ACCEPTED**;
- D3: **CLOSED — ACCEPTED**;
- D4: **CLOSED — ACCEPTED**;
- D5: **CLOSED — ACCEPTED**;
- Q2 persisted representation: **OPEN / NOT ESTABLISHED**;
- N1–N5: **UNAPPROVED CANDIDATES**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- actor attribution / ActorContext persistence semantics: **SEPARATE / UNRESOLVED**;
- WP18 dependency: **NOT RESTORED**;
- ADW-07: **OPEN**;
- WP19 implementation: **BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit interim-shape authorization**.

## 11. Decision result

**D5 CLOSED — ACCEPTED. CURRENT Q2 ACCEPTANCE SCOPE IS THE FIVE EXISTING SUBJECT TYPES; FUTURE SUBJECT TYPES REQUIRE SEPARATE EXPLICIT ARCHITECTURE AUTHORITY; ZERO-MIGRATION OPEN-ENDED EXTENSIBILITY IS NOT REQUIRED; EXTENSIBILITY CONVENIENCE DOES NOT SELECT OR DEFAULT N1–N5; TECHNICAL ENCODABILITY DOES NOT CREATE SUBJECT-TYPE AUTHORITY.**