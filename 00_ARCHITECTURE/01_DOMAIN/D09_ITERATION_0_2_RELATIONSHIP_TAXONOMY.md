# D09 — Iteration 0.2: Relationship Taxonomy

**Parent:** `D09_RELATIONSHIP_MODEL.md`  
**Version:** 0.2-draft  
**Status:** IN WORKSHOP  
**Decision:** D09.2 — Relationship Taxonomy  
**Decision class:** Class A — Constitutional  
**Date:** 2026-07-22

---

## 1. Purpose

This iteration defines the constitutional taxonomy of relationship categories in Bizzi.

The taxonomy separates semantically different relationship classes so that ownership, composition, aggregation, reference, dependency, association, governance, coordination, traceability, provenance, temporal ordering, and semantic correspondence cannot be collapsed into one generic graph edge or universal relation type.

Each concrete Relationship Type shall declare exactly one primary constitutional category.

---

## 2. Relationship Categories

Bizzi recognizes the following primary categories:

```text
Ownership
Composition
Aggregation
Reference
Dependency
Association
Governance
Coordination
Traceability
Provenance
Temporal
Semantic
```

A category defines the semantic nature of a relationship independently of database representation, graph storage, foreign keys, ORM navigation, API serialization, or user-interface presentation.

---

## 3. Ownership Relationships

Ownership defines responsibility for authoritative business state, invariants, and lifecycle authority.

Typical characteristics:

- authoritative;
- invariant-bearing;
- lifecycle-significant;
- explicitly assigned;
- exclusive unless the relationship type defines a governed shared-ownership model approved by a Class A decision.

Examples:

- Workspace owns a workspace-scoped Enterprise Object;
- an aggregate owns its internal Value Objects;
- Decision owns its authoritative determination state.

Ownership transfer requires an explicit governed transition. A reference, association, dependency, or coordination relationship never transfers ownership by implication.

---

## 4. Composition Relationships

Composition defines strong structural containment where the composed child has no independent authoritative lifecycle outside the parent context.

Properties:

- the child is semantically part of the parent;
- the child cannot be independently reparented without an explicit model rule;
- lifecycle consequences are governed by the parent;
- deletion, archival, retention, and supersession consequences are routed to D10.

Example:

```text
Business Operation
  composes
Operation Step Value
```

Composition is stronger than Aggregation and must not be introduced merely for implementation convenience.

---

## 5. Aggregation Relationships

Aggregation defines logical grouping without transfer of authoritative ownership.

Examples:

- Project aggregates Tasks;
- Business Operation aggregates Work Items for coordination;
- a portfolio aggregates Enterprise Objects for reporting.

Aggregated subjects retain their own aggregate boundary, owner, lifecycle, and invariants.

Aggregation shall never silently become Composition.

---

## 6. Reference Relationships

Reference defines a stable typed business pointer from one subject to another.

Examples:

- Business Operation references an Enterprise Object;
- Decision references a Policy;
- Result references Evidence.

Reference:

- does not transfer ownership;
- does not transfer authority;
- does not merge consistency boundaries;
- does not imply lifecycle dependency;
- does not imply inverse navigability unless the Relationship Type defines it.

---

## 7. Dependency Relationships

Dependency defines a condition in which one subject relies on another subject or outcome before proceeding, completing, or remaining valid.

Examples:

- Work Item depends on another Work Item;
- Business Operation depends on an approved Decision;
- State Transition depends on validated Evidence.

Dependency is directional and may be business, operational, temporal, or validation-related.

Dependency is acyclic by default. Cycles require an explicit Relationship Type that defines cycle semantics, termination, deadlock handling, and validation rules.

Dependency does not imply ownership.

---

## 8. Association Relationships

Association defines a semantically meaningful connection without ownership, composition, dependency, governance, or coordination consequences.

Examples:

- Actor is associated with an Enterprise Object;
- Customer is associated with a Contract;
- Evidence is associated with a Decision context.

Association must not be used as a generic escape hatch where a stronger semantic category is known.

---

## 9. Governance Relationships

Governance defines authority, control, approval, policy applicability, or decision effect.

Examples:

- Decision governs a Business Operation;
- Policy governs a Decision;
- approval governs a transition request;
- a control rule governs validation.

Governance expresses authority semantics. It is distinct from execution, orchestration, grouping, or observation.

---

## 10. Coordination Relationships

Coordination defines the organization of work or activity across independently owned subjects.

Examples:

- Business Operation coordinates Work Items;
- Work Item coordinates Runtime Sessions;
- an orchestrator coordinates Actions.

The coordinator does not become the owner of coordinated endpoint state.

Coordination does not grant mutation authority unless a separate authority rule explicitly permits it.

---

## 11. Traceability Relationships

Traceability defines an auditable path connecting intent, authority, execution, validation, state change, events, and outcomes.

Examples:

- Domain Event traces to a committed State Transition;
- State Transition traces to Decision and Result;
- Audit record traces to Actor and authority basis.

Traceability preserves navigability and accountability. It does not create ownership, dependency, governance, or mutation authority.

---

## 12. Provenance Relationships

Provenance defines origin, production, derivation, observation, or source attribution.

Examples:

- Result was produced by Runtime Session;
- Evidence was generated by Tool Invocation;
- Decision was issued by an effective Actor;
- Projection was derived from authoritative aggregate versions.

Provenance establishes origin but does not establish ownership, acceptance, validity, or authority.

---

## 13. Temporal Relationships

Temporal relationships define ordering, overlap, validity windows, or effective-time relationships.

Examples:

- precedes;
- follows;
- overlaps;
- effective during;
- supersedes in time;
- valid from / valid until.

Temporal ordering does not by itself establish dependency, causation, authority, or ownership.

---

## 14. Semantic Relationships

Semantic relationships define conceptual correspondence or meaning between subjects.

Examples:

- equivalent to;
- duplicate of;
- derived from;
- supersedes;
- refines;
- contradicts;
- classifies.

Semantic relationships may carry important business meaning but do not alter ownership, consistency boundaries, or authority unless the Relationship Type explicitly defines such consequences under an approved rule.

---

## 15. Category Comparison Matrix

| Category | Transfers ownership | Creates lifecycle dependency | Creates authority | Creates consistency boundary | Primarily historical / observational |
|---|---:|---:|---:|---:|---:|
| Ownership | Yes, when explicitly governed | Usually | Yes | Within the owning aggregate | No |
| Composition | Parent owns composed lifecycle | Yes | Through parent | Within parent aggregate | No |
| Aggregation | No | No | No | No | No |
| Reference | No | No | No | No | No |
| Dependency | No | May constrain lifecycle | No | No | No |
| Association | No | No | No | No | No |
| Governance | No | May constrain lifecycle | Yes | No | No |
| Coordination | No | Operationally possible | No by itself | No | No |
| Traceability | No | No | No | No | Yes |
| Provenance | No | No | No | No | Yes |
| Temporal | No | No by itself | No | No | Often |
| Semantic | No | No by itself | No | No | Context-dependent |

The matrix defines default semantics. A concrete Relationship Type may add stricter rules but may not contradict its primary category without a new Class A decision.

---

## 16. Constitutional Laws — Iteration 0.2

### LAW-D09-15 — Category Declaration

Every authoritative Relationship Type shall declare exactly one primary constitutional category.

### LAW-D09-16 — Ownership and Reference Separation

Ownership and Reference shall never be represented by the same Relationship Type.

### LAW-D09-17 — Composition Is Explicit

Composition shall be declared explicitly and shall never be inferred from storage structure, foreign-key placement, object nesting, or API embedding.

### LAW-D09-18 — No Silent Aggregation Upgrade

Aggregation shall never silently become Composition or Ownership.

### LAW-D09-19 — Governance and Coordination Separation

Governance and Coordination are separate categories. Coordination does not establish authority, and governance does not imply execution responsibility.

### LAW-D09-20 — Traceability Is Non-Controlling

Traceability does not establish Dependency, Governance, Ownership, or mutation authority.

### LAW-D09-21 — Provenance Is Not Acceptance

Provenance establishes origin but does not establish business validity, ownership, acceptance, or authority.

### LAW-D09-22 — Temporal Ordering Is Not Causation

Temporal precedence or overlap does not by itself establish causation, dependency, governance, or responsibility.

### LAW-D09-23 — Derived Relationships Remain Derived

Derived, inferred, recommended, or AI-generated relationships remain non-authoritative until governed validation and commitment.

### LAW-D09-24 — Technology Does Not Define Category

Relationship category is determined by domain semantics, not by graph edges, foreign keys, ORM mappings, document embedding, event correlation, or transport representation.

---

## 17. Decision D09.2 — Relationship Taxonomy

**Status:** PROPOSED  
**Decision class:** Class A — Constitutional

> Bizzi adopts a constitutional relationship taxonomy consisting of Ownership, Composition, Aggregation, Reference, Dependency, Association, Governance, Coordination, Traceability, Provenance, Temporal, and Semantic categories.
>
> Every authoritative Relationship Type belongs to exactly one primary category.
>
> Categories define default ownership, lifecycle, authority, consistency, and historical consequences independently of persistence technology or graph representation.
>
> Concrete Relationship Types may impose stricter constraints but may not contradict their primary category without an explicit Class A architecture decision.

---

## 18. Consequences

1. Generic relationship fields without declared semantic type and category are prohibited for authoritative domain use.
2. A technical link must not be interpreted as Ownership, Dependency, Governance, or Composition without an approved Relationship Type.
3. D09.3 must define endpoint roles, directionality, inverse semantics, and cardinality for Relationship Types.
4. D09.4 must define who may create, validate, approve, revoke, or supersede authoritative relationships.
5. D09.5 must define effective time, lifecycle states, expiration, invalidation, and historical preservation.
6. D09.6 must define traversal, derived graph views, consistency boundaries, and query semantics.
7. D10 retains deletion, archival, supersession, retention, and historical-removal consequences.

---

## 19. Iteration Status

```text
D09.1 Relationship Foundation: PROPOSED
D09.2 Relationship Taxonomy: PROPOSED
D09.3 Roles, Direction, and Cardinality: NOT STARTED
D09.4 Ownership, Authority, and Validation: NOT STARTED
D09.5 Lifecycle and Temporal Semantics: NOT STARTED
D09.6 Consistency, Traversal, and Graph Views: NOT STARTED
D09.7 Constitutional Review and Closure: NOT STARTED

D09 overall status: IN WORKSHOP
```
