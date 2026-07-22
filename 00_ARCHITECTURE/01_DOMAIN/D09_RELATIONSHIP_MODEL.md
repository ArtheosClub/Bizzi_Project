# D09 — Relationship Model

**Subtitle:** The Bizzi Relationship Constitution  
**Document ID:** ARCH-DOMAIN-D09  
**Version:** 0.1-draft  
**Status:** IN WORKSHOP  
**Decision class:** Class A — Constitutional  
**Workshop:** ADW-01 — Core Domain Semantics  
**Owner:** Project Owner  
**Decision authority:** Project Owner  
**Opened:** 2026-07-22  
**Last updated:** 2026-07-22

---

## 1. Purpose

D09 defines the constitutional semantics of relationships in Bizzi.

It establishes how domain subjects may reference, depend on, contain, govern, coordinate, trace, supersede, or otherwise relate to one another without creating hidden ownership, accidental aggregate coupling, ambiguous authority, or an ungoverned universal business graph.

D09 is implementation-independent. It does not prescribe one graph database, relational schema, ORM model, API representation, event envelope, or user-interface notation.

---

## 2. Governing Question

> How does Bizzi represent typed, directional, attributable, governed, and historically meaningful relationships among domain subjects without confusing reference with ownership, coordination with control, observation with authority, or graph connectivity with aggregate consistency?

---

## 3. Scope

D09 governs:

1. relationship identity and semantic type;
2. source and target roles;
3. directionality and inverse meaning;
4. cardinality and multiplicity;
5. ownership versus reference;
6. dependency, containment, composition, aggregation, association, governance, coordination, and traceability;
7. relationship authority and creation rights;
8. relationship lifecycle, validity, effective time, and historical preservation;
9. cross-aggregate and cross-workspace relationship rules;
10. relationship attributes, evidence, provenance, and attribution;
11. relationship consistency boundaries;
12. derived graph views and traversal semantics;
13. relationship validation and invariant enforcement;
14. the relationship of Decision, Business Operation, Work Item, Enterprise Object, Actor, Runtime Session, Action, Result, Evidence, State Transition, and Domain Event.

D09 does not define:

- full deletion, archival, supersession, reversal, compensation, and retention semantics, which belong to D10;
- physical graph or relational persistence schemas;
- authorization policy evaluation, which belongs to ADW-03;
- event transport and delivery infrastructure;
- user-interface graph visualization;
- implementation-specific ORM navigation properties;
- unrestricted semantic knowledge graphs.

---

## 4. Relationship Philosophy

Bizzi adopts the following foundational principle:

> A relationship is an explicit domain assertion, not an incidental technical link.

A foreign key, object pointer, URL, event correlation identifier, graph edge, workflow dependency, or shared identifier does not automatically constitute an authoritative business relationship.

An authoritative relationship exists only when its semantic type, endpoints, authority basis, validity rules, ownership rules, and lifecycle are explicitly defined and accepted by the responsible domain authority.

---

## 5. Foundational Definitions

### 5.1 Relationship

A Relationship is a semantically typed assertion connecting two or more identifiable subjects within an explicit context, direction, validity period, authority basis, and lifecycle.

### 5.2 Relationship Type

A Relationship Type defines the meaning, permitted endpoint types, directionality, inverse semantics, cardinality, authority requirements, lifecycle rules, and invariants of a class of relationships.

### 5.3 Relationship Instance

A Relationship Instance is a concrete governed assertion that identified subjects participate in a specific Relationship Type.

### 5.4 Source and Target

Source and Target identify the directional roles of a binary relationship. Direction is semantic, not merely visual or technical.

The inverse of a relationship must be explicitly defined where inverse traversal carries business meaning.

### 5.5 Relationship Owner

The Relationship Owner is the aggregate or explicitly defined domain authority responsible for validating, creating, changing, suspending, terminating, and preserving the authoritative relationship assertion.

Relationship ownership does not automatically imply ownership of either endpoint.

### 5.6 Endpoint Owner

An Endpoint Owner owns the authoritative state and invariants of an endpoint subject. A relationship may reference an endpoint without acquiring authority over it.

### 5.7 Derived Relationship

A Derived Relationship is inferred, calculated, projected, indexed, correlated, recommended, or generated from authoritative sources.

Derived relationships may support discovery and analysis but cannot silently become authoritative business assertions.

### 5.8 Relationship Context

Relationship Context identifies the Workspace, domain scope, temporal scope, operational context, Decision, policy, or Business Operation within which the relationship has meaning.

---

## 6. Initial Relationship Families

D09 initially distinguishes the following semantic families:

| Family | Governing question |
|---|---|
| Ownership | Who owns the lifecycle and authoritative state of the subject? |
| Containment | What boundary contains the subject? |
| Composition | Is the part lifecycle-dependent on the whole? |
| Aggregation | Is the subject grouped without lifecycle ownership? |
| Association | What stable business connection exists? |
| Dependency | What must exist or occur for another subject to remain valid or proceed? |
| Governance | What Decision, policy, approval, or authority governs the subject? |
| Coordination | What operation or work structure coordinates the subject? |
| Participation | Which Actor or participant performs, approves, observes, or is accountable? |
| Traceability | What caused, produced, validated, or evidences the subject? |
| Temporal | What precedes, follows, overlaps, replaces, or is effective with another subject? |
| Equivalence | Under what governed rule do distinct identities represent the same external or business referent? |
| Derivation | From what authoritative source was a result, projection, or interpretation derived? |

These families are not universal edge labels. Each concrete relationship type must define its own contract.

---

## 7. Preliminary Constitutional Laws

### LAW-D09-01 — Explicit Semantic Type

Every authoritative relationship has an explicit semantic type.

### LAW-D09-02 — Reference Is Not Ownership

Referencing a subject never transfers ownership of its state, lifecycle, invariants, or authorization boundary.

### LAW-D09-03 — Coordination Is Not Control

A Business Operation, Work Item, workflow, or application service may coordinate multiple subjects without becoming their owner.

### LAW-D09-04 — Direction Is Semantic

Relationship direction and endpoint roles must be defined by domain meaning rather than storage layout or interface convenience.

### LAW-D09-05 — Relationship Authority

Only the relationship owner or an explicitly authorized domain process may create, change, suspend, or terminate an authoritative relationship.

### LAW-D09-06 — Endpoint Integrity

A relationship must not violate the invariants, visibility, Workspace boundary, or lifecycle restrictions of its endpoints.

### LAW-D09-07 — No Hidden Coupling

Object references, database joins, shared identifiers, event correlations, and workflow links must not create undeclared domain dependencies.

### LAW-D09-08 — Historical Preservation

Significant relationship changes remain attributable, temporally identifiable, auditable, and historically preserved.

### LAW-D09-09 — Derived Graph Is Not Truth

Graph projections, search indexes, recommendations, inferred links, similarity links, and AI-generated associations are derived unless explicitly promoted through a governed relationship process.

### LAW-D09-10 — Workspace Boundary

Cross-workspace relationships are prohibited by default and require an explicit governed contract defining authority, visibility, tenancy, data handling, and revocation.

### LAW-D09-11 — Aggregate Boundaries Remain Intact

A relationship between aggregates does not merge their consistency boundaries.

### LAW-D09-12 — Typed Traversal

Traversal is permitted only through relationship types whose semantics, direction, visibility, and authorization rules are known.

### LAW-D09-13 — No Universal Edge

A universal unvalidated `related_to` relationship is prohibited as an authoritative domain representation.

### LAW-D09-14 — AI Is Advisory

AI may discover, rank, suggest, or explain potential relationships. AI output does not create an authoritative relationship without governed validation and commitment.

---

## 8. Preliminary Relationship Contract

```text
Relationship {
  relationship_id
  workspace_id
  relationship_type
  source_reference
  source_role
  target_reference
  target_role
  owner_reference
  authority_basis
  attributes
  evidence_references
  decision_references
  operation_reference
  valid_from
  valid_until
  effective_status
  created_by_actor
  effective_actor
  created_at
  updated_at
  version
  correlation_id
  causation_id
}
```

This is a semantic contract, not a mandatory universal database table, graph edge schema, aggregate, or event envelope.

Later iterations must determine which fields are universal, conditional, specialized, or prohibited for particular relationship types.

---

## 9. First Workshop Decision

### D09.1 — Nature of Relationship

**Status:** PROPOSED  
**Decision class:** Class A — Constitutional

Proposed decision:

> Relationship is a first-class semantic assertion with an explicit type, endpoints, roles, direction, authority basis, validity, owner, and lifecycle.
>
> Relationship does not transfer ownership of endpoint state unless the relationship type explicitly defines composition or another approved ownership consequence.
>
> Cross-aggregate relationships use stable typed references and do not merge aggregate consistency boundaries.
>
> Derived and AI-inferred relationships remain non-authoritative until validated and committed by the responsible domain authority.

D09.1 remains proposed until explicitly approved by the Project Owner.

---

## 10. Iteration Roadmap

D09 will be developed and committed incrementally.

### Iteration 0.1 — Foundation

- purpose, governing question, scope, and exclusions;
- relationship philosophy;
- foundational definitions;
- initial relationship families;
- preliminary constitutional laws;
- candidate relationship contract;
- proposed D09.1 decision.

### Iteration 0.2 — Relationship Taxonomy

- ownership;
- containment;
- composition;
- aggregation;
- association;
- dependency;
- governance;
- coordination;
- participation;
- traceability;
- derivation;
- temporal and equivalence relationships.

### Iteration 0.3 — Roles, Direction, and Cardinality

- source and target roles;
- inverse relationships;
- directed, symmetric, and asymmetric semantics;
- one-to-one, one-to-many, many-to-many;
- optionality and exclusivity;
- ordered and ranked relationships.

### Iteration 0.4 — Ownership, Authority, and Validation

- relationship owner;
- endpoint authority;
- creation, change, and termination rights;
- Decision-authorized and policy-authorized relationships;
- evidence and invariant validation;
- cross-workspace restrictions.

### Iteration 0.5 — Lifecycle and Temporal Semantics

- proposed, active, suspended, expired, terminated, invalidated, and superseded relationships;
- valid time and transaction time;
- effective dating;
- historical preservation;
- correction versus deletion.

### Iteration 0.6 — Consistency, Traversal, and Graph Views

- aggregate consistency boundaries;
- cross-aggregate coordination;
- traversal authorization;
- graph projections;
- stale and incomplete graph views;
- cycle detection and prohibited cycles;
- relationship reconstruction.

### Iteration 0.7 — Constitutional Review

- consolidated decisions and laws;
- deferred decisions and routing;
- synchronization with Domain Foundation, ADW-01, Decision Register, and Architecture Specification;
- Project Owner approval and D09 closure.

---

## 11. Open Questions

1. Which relationship types require first-class identity and history, and which may remain aggregate-owned values?
2. Which relationships are owned by an endpoint and which require an independent relationship authority?
3. How are composition and containment distinguished from ordinary reference?
4. Which inverse relationships are authoritative and which are derived views?
5. How are relationship cardinality and exclusivity enforced across aggregates?
6. Which relationships may cross Workspace boundaries?
7. How are external-system identities and equivalence relationships governed?
8. Which relationship cycles are valid, suspicious, or prohibited?
9. When must relationship attributes become a specialized associative aggregate?
10. Which lifecycle and deletion semantics are resolved by D09 versus deferred to D10?

---

## 12. Current Workshop Status

```text
D09.1 Nature of Relationship: PROPOSED
D09.2 Relationship Taxonomy: NOT STARTED
D09.3 Roles, Direction, and Cardinality: NOT STARTED
D09.4 Ownership, Authority, and Validation: NOT STARTED
D09.5 Lifecycle and Temporal Semantics: NOT STARTED
D09.6 Consistency, Traversal, and Graph Views: NOT STARTED
D09.7 Constitutional Review and Closure: NOT STARTED

D09 overall status: IN WORKSHOP
```
