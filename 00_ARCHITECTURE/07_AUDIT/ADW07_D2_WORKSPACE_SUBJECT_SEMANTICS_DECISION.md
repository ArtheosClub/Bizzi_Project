# ADW-07 — Q2 / D2 Workspace Subject Semantics Decision

**Workshop:** ADW-07 — Events, Audit and Provenance  
**Workshop status:** OPEN  
**Decision:** ADR-0014 Q2 / D2 — Semantic Meaning of `Workspace` as an AuditRecord Subject Type  
**Decision status:** ACCEPTED  
**Decision owner:** Project Owner  
**Authority:** Project Owner / Andrew  
**Decision date:** 2026-08-30  

## 1. Accepted D2 decision

> **`Workspace` is a first-class subject type. When the discriminator is `Workspace`, the durable subject reference identifies the Workspace entity itself. A workspace associated with another subject is contextual metadata, not an implicit substitution for that subject.**

## 2. Decision scope

This decision closes **D2 only**.

It establishes the semantic meaning of `Workspace` when the accepted D1 subject-type discriminator has the value `Workspace`.

The decision preserves the following boundaries:

1. `Workspace` is a first-class audited subject type in its own right.
2. Workspace context, ownership, containment, scope, tenancy, or association of another subject does not replace that subject's identity with `Workspace`.
3. `WorkspaceMembership` remains a distinct subject type and is not reduced to the Workspace that it references.
4. Association of an `EnterpriseObject`, `User`, `WorkspaceMembership`, or `Task` with a workspace does not by itself mean that the Workspace is the audited subject.
5. D1 remains a separate accepted rule governing subject-type disambiguation. D2 does not alter D1 or decide physical placement of its discriminator.
6. D3, D4, D5 and the N1–N5 representation candidates remain unresolved/unapproved by this decision.

## 3. Explicit non-decisions

D2 does **not** decide:

- how another subject's workspace association is represented;
- whether every subject or AuditRecord must have workspace context;
- multi-workspace semantics;
- cross-workspace semantics;
- workspace ownership or containment rules;
- subject/workspace consistency enforcement;
- D3 subject deletion / historical resolution;
- D4 database-enforced referential integrity;
- D5 future subject-type / extensibility requirement;
- any N1–N5 candidate approval, rejection, ranking, or selection;
- persistence shape;
- physical placement of the D1 discriminator;
- FK or composite-FK strategy;
- database versus application/domain enforcement;
- migration;
- persistence implementation ownership;
- runtime resolver/API contract;
- actor attribution;
- WP19 implementation;
- final Q2 persisted representation.

## 4. Relationship to D1

D1 is independently **CLOSED — ACCEPTED** and requires an explicit durable subject-type discriminator whose committed value identifies exactly one current Q2 subject type.

D2 does not merge with D1. It supplies only the semantic meaning of one accepted discriminator value: when that value is `Workspace`, the subject is the Workspace entity itself.

## 5. Boundary cases

### Workspace as subject

When the discriminator is `Workspace`, the referenced Workspace entity is the audited subject.

### Workspace as context

A workspace that provides context, ownership, containment, tenancy, or association for another audited subject remains contextual to that subject. D2 does not substitute the Workspace for that subject.

### WorkspaceMembership

When the audited subject is `WorkspaceMembership`, the membership remains the subject. The Workspace referenced by or associated with that membership is not automatically the audited subject.

### Workspace association

Association with a workspace does not itself establish that the Workspace is the audited subject. This applies without prejudice to later scoping or consistency rules.

### Multi-workspace / cross-workspace cases

D2 does not determine whether multi-workspace or cross-workspace audit semantics are permitted or required, nor how such semantics would be represented or enforced. Those questions remain outside this decision.

## 6. Authority and state transition

Project Owner acceptance establishes this document as the canonical D2 authority for ADR-0014 Q2 / ADW-07.

State after this decision:

- D1: **CLOSED — ACCEPTED**;
- D2: **CLOSED — ACCEPTED**;
- D3–D5: **OPEN**;
- Q2 persisted representation: **OPEN**;
- N1–N5: **UNAPPROVED**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED pending Q2 subject-reference representation resolution**;
- WP18 dependency: **NOT RESTORED**.

This decision creates no model, migration, interim persistence representation, or implementation authorization.

## 7. Next bounded step

The next Q2 decision surface is **D3 — Subject deletion / historical resolution**.

D3 must be analyzed separately. It must not infer persistence shape, FK delete behavior, tombstones, permanent subject-row retention, or a representation candidate from D1 or D2.