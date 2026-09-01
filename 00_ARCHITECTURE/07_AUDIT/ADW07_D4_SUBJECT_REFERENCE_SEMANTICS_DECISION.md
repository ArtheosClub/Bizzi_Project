# ADW-07 / Q2 D4 — Subject Reference Semantics Decision

**Status:** ACCEPTED  
**Decision:** D4 — CLOSED / ACCEPTED  
**Decision Date:** 2026-08-30  
**Decision Owner:** Project Owner / Andrew  
**Parent:** ADW-07 — Events, Audit and Provenance  
**Scope:** ADR-0014 Q2 / D4 subject-reference semantics only

## 1. Accepted semantic rule

> **AuditRecord subject identity is mandatory, durable, explicit, and independently resolvable. It identifies the audited subject — the object of the audited mutation — and not the actor, initiator, execution context, request context, Workspace context, association participant, route, or audit payload. Actor attribution, ActorContext, request context, Workspace context, association data, route data, and audit payload MUST NOT substitute for subject identity or establish it by implication.**

A committed AuditRecord subject reference MUST satisfy the following semantic properties:

1. **Canonical logical subject identity** — the reference denotes one logical historical subject: what was changed/audited.
2. **Explicit subject kind/type** — the subject type is explicit under accepted D1 authority and is not inferred from actor, route, payload, request context, Workspace context, or current runtime context.
3. **Stable subject identifier** — the durable identity meaning remains stable across later state or lifecycle changes of the subject.
4. **Verifiable historical resolvability** — the system's durable reference contract must make it possible to establish which historical subject the AuditRecord identifies; successful current live dereference is not required for historical validity.
5. **Historical stability** — deletion, deactivation, archival, closure, supersession, or current unavailability of the subject does not by itself make the committed AuditRecord lose or change its historical subject identity, subject to the D3 lifecycle/history boundary and separate legal/compliance authority.
6. **No implicit fallback** — actor identity, ActorContext, Workspace, request context, association participants, route, diff, or payload are not substitutes for missing subject identity.

These semantic requirements apply across all five current D1 subject types: `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, and `Task`. They are not limited to a single aggregate or entity family.

## 2. Relationship to D1–D3

D4 preserves and does not redefine prior accepted authority:

- **D1 — CLOSED / ACCEPTED:** the durable subject reference has an explicit durable subject-type discriminator identifying exactly one current Q2 subject type.
- **D2 — CLOSED / ACCEPTED:** `Workspace` is a first-class subject type; Workspace context associated with another subject does not substitute for that subject.
- **D3 — CLOSED / ACCEPTED:** committed historical subject identity survives later subject deletion/deactivation and is not rewritten by subject/context lifecycle change.

D4 adds the semantic requirement that subject identity itself be mandatory, explicit, durable, stable, independently interpretable, and distinct from actor/context/association semantics.

## 3. Actor-attribution boundary

Audited-subject identity answers **what was audited**.

Actor attribution answers **who or what performed, initiated, authorized, or was attributed to the action**.

These are separate semantic axes. `actor_id`, ActorContext, initiator identity, service identity, current User, or any other attribution mechanism MUST NOT be used as an implicit audited-subject identity.

A `User` may be the audited subject in one record and an actor in another; its semantic role in the record must remain explicit.

D4 does not define the actor-attribution persistence or identity model.

## 4. Unknown, legacy, and unavailable subjects

Current live availability is distinct from historical subject identity.

- A known historical subject may be currently unavailable, deleted, deactivated, archived, or otherwise non-live without invalidating its committed historical identity.
- A legacy identity may be preserved as legacy evidence where it cannot be mapped to the current canonical identity convention without invention.
- Missing or insufficient subject identity MUST NOT be repaired semantically by substituting actor, Workspace, request, route, association, diff, payload, or current runtime context.
- D4 does not create `Unknown`, `Legacy`, or another sixth current D1 subject type.
- Legacy compatibility, migration, repair, and reconciliation procedures remain separate decisions.

## 5. Persistence representation remains open

**Persistence representation: OPEN.**

D4 intentionally does not decide whether the accepted semantic contract is represented as:

- N1 polymorphic reference;
- N2 composite-FK-derived representation;
- N3 per-type nullable representation;
- N4 opaque identifier;
- N5 in-payload representation;
- or another separately evaluated representation.

No N1–N5 candidate is selected, preferred, defaulted, rejected, or approved by D4.

D4 does not select columns, field names, UUID/integer/string/composite values, FK structure, composite FK, payload layout, registry, tombstone, archival structure, resolver implementation, database enforcement, application enforcement, migration, model, repository, service, API, backend, or tests.

GC-002 Alternative B remains **PROPOSED ONLY** and receives no normative authority from D4.

## 6. Q1 / Q2 boundary

ADR-0014 Q1 remains closed: an AuditRecord must durably identify the subject of the audited mutation.

D4 closes the semantic contract addressed here, but it does **not** close ADR-0014 Q2 persisted representation.

**Q2 persisted representation remains OPEN / NOT ESTABLISHED.**

The semantic necessity and properties of the subject reference are therefore authoritative, while its concrete persistence representation remains a separate unresolved architecture decision.

## 7. D3 retention/deletion boundary

D4 relies on D3's historical-identity and lifecycle invariant but does not replace or expand it.

D4 does not establish retention periods, legal holds, erasure/anonymization obligations, subject deletion permission, FK delete actions, cascade behavior, or physical preservation mechanics.

## 8. Routing and ownership boundary

D4 does not itself change the existing ADR-0014 / ADW-07 routing or ownership authority for Q2 persistence representation.

Any future transfer of persistence-representation decision ownership to another decision owner or mechanism requires a separate explicit architecture decision; it MUST NOT be inferred from this D4 semantic decision.

Until Q2 persistence representation is explicitly resolved — or a separate explicit bounded interim-shape authorization is issued — WP19 model/migration implementation remains blocked.

## 9. Explicit non-decisions

D4 does not decide:

- persistence representation;
- N1–N5 selection, ranking, rejection, preference, or default;
- GC-002 Alternative B approval;
- exact persistence fields or constraints;
- referential-integrity enforcement mechanism;
- actor-attribution persistence contract;
- retention/legal/compliance policy;
- migration or legacy repair procedure;
- runtime resolver/API contract;
- WP19 models, migrations, repositories, services, APIs, backend, or tests;
- final Q2 representation;
- ADW-07 closure.

## 10. Decision state

- D1: **CLOSED — ACCEPTED**;
- D2: **CLOSED — ACCEPTED**;
- D3: **CLOSED — ACCEPTED**;
- D4: **CLOSED — ACCEPTED**;
- D5: **OPEN**;
- Q2 persisted representation: **OPEN / NOT ESTABLISHED**;
- N1–N5: **UNAPPROVED**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- ADW-07: **OPEN**;
- WP19 implementation: **BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit interim-shape authorization**.

## 11. Decision result

**D4 CLOSED — ACCEPTED. AUDITRECORD SUBJECT IDENTITY IS MANDATORY, DURABLE, EXPLICIT, STABLE, AND INDEPENDENTLY RESOLVABLE; ACTOR ATTRIBUTION, CONTEXT, ASSOCIATION, REQUEST/ROUTE DATA, AND PAYLOAD DO NOT SUBSTITUTE FOR IT. PERSISTENCE REPRESENTATION REMAINS OPEN / NOT ESTABLISHED.**