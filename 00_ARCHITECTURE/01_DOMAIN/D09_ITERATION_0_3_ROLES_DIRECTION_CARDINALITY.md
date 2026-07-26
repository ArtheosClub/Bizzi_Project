# D09 — Iteration 0.3: Roles, Direction, and Cardinality

**Parent:** `D09_RELATIONSHIP_MODEL.md`  
**Version:** 0.3-draft  
**Status:** IN WORKSHOP  
**Decision:** D09.3 — Roles, Direction, and Cardinality  
**Decision class:** Class A — Constitutional  
**Date:** 2026-07-22

---

## 1. Purpose

This iteration defines how Bizzi expresses endpoint roles, relationship direction, inverse meaning, and cardinality constraints.

It prevents ambiguous graph edges, duplicated inverse records, accidental many-to-many semantics, hidden endpoint responsibilities, and implementation-specific navigation behavior from becoming domain law.

---

## 2. Endpoint Roles

Every authoritative relationship shall define explicit endpoint roles.

A role is not merely an endpoint label. It declares the semantic participation of an endpoint in a relationship type.

Minimum role contract:

```text
role_id
role_name
endpoint_type
participation_semantics
minimum_cardinality
maximum_cardinality
authority_constraints
lifecycle_constraints
inverse_role
```

### 2.1 Source Role

The Source Role identifies the endpoint from which the canonical relationship statement is expressed.

Source does not automatically mean:

- owner;
- controller;
- creator;
- cause;
- parent;
- earlier subject;
- more authoritative subject.

These meanings exist only when declared by the relationship type.

### 2.2 Target Role

The Target Role identifies the endpoint toward which the canonical relationship statement is expressed.

Target does not automatically mean:

- subordinate;
- dependent;
- child;
- governed subject;
- result;
- later subject.

### 2.3 Named Roles

Every domain-significant relationship type shall use semantically meaningful role names.

Preferred form:

```text
Decision --governs--> Business Operation
Policy --constrains--> Decision
Result --supported_by--> Evidence
Work Item --depends_on--> Work Item
```

Generic roles such as `left`, `right`, `node_a`, and `node_b` are prohibited in authoritative domain definitions.

---

## 3. Directionality

A relationship type shall declare one of the following direction models:

1. **Directed** — the source-to-target assertion has distinct semantic meaning;
2. **Symmetric** — endpoint order does not change meaning;
3. **Directed with inverse semantic** — the canonical assertion has a formally defined inverse expression;
4. **Ordered n-ary** — three or more endpoints participate through named ordered roles.

### 3.1 Directed Relationships

Examples:

```text
Decision governs Business Operation
Work Item depends on Work Item
Evidence supports Result
Actor performs Action
```

Reversing endpoints changes or invalidates the meaning.

### 3.2 Symmetric Relationships

Examples may include:

```text
Enterprise Object equivalent_to Enterprise Object
Enterprise Object conflicts_with Enterprise Object
```

Symmetry shall be explicitly declared. It shall never be inferred from storage duplication or bidirectional navigation properties.

### 3.3 Inverse Relationships

A directed relationship may expose an inverse semantic view.

Example:

```text
Decision governs Business Operation
Business Operation governed_by Decision
```

The inverse is a semantic projection of the same relationship instance unless the relationship type explicitly defines two independent assertions.

Systems shall not create duplicate authoritative relationship instances merely to provide inverse traversal.

### 3.4 Bidirectional Navigation

Bidirectional technical navigation does not make a relationship semantically symmetric.

A relationship may be traversable from both endpoints while remaining semantically directed.

---

## 4. Cardinality

Cardinality is part of the relationship type contract.

Bizzi uses minimum and maximum participation constraints for each role.

Supported cardinality forms include:

```text
0..1
1..1
0..N
1..N
```

Common relationship shapes:

- one-to-one;
- one-to-many;
- many-to-one;
- many-to-many.

Cardinality shall be defined semantically before it is implemented physically.

### 4.1 One-to-One

Each participating source may relate to at most one target, and each participating target may relate to at most one source within the relationship context.

One-to-one does not imply shared identity or shared lifecycle.

### 4.2 One-to-Many

One source may relate to multiple targets while each target is constrained to one source within the relationship context.

One-to-many does not automatically imply composition or ownership.

### 4.3 Many-to-Many

Many-to-many relationships are permitted only when the domain meaning is explicit and the relationship itself can carry identity, authority, provenance, validity, and attributes when required.

A many-to-many persistence join table is not sufficient as a domain definition.

### 4.4 Mandatory and Optional Participation

Minimum cardinality defines whether endpoint participation is optional or mandatory.

Mandatory participation shall be enforced at the responsible consistency boundary or through an explicitly governed eventual-consistency rule.

---

## 5. Relationship Identity and Inverse Uniqueness

A single business assertion shall have one authoritative relationship identity.

Inverse traversal, denormalized indexes, read models, graph projections, and cached navigation shall reference that identity rather than create competing relationship facts.

Relationship uniqueness may depend on:

- relationship type;
- source identity and role;
- target identity and role;
- relationship context;
- effective-time interval;
- authority basis;
- declared discriminator attributes.

---

## 6. Cycles

Cycles are evaluated by relationship category and type, not by graph connectivity alone.

### 6.1 Prohibited Cycles

The following are prohibited unless a later constitutional decision explicitly authorizes them:

- ownership cycles;
- composition cycles;
- strict execution-dependency cycles;
- authority cycles that make final decision responsibility indeterminate.

### 6.2 Permitted Cycles

Association, coordination, semantic, traceability, or temporal graphs may contain cycles when the relationship type permits them and the cycle does not violate an invariant.

### 6.3 Cycle Validation

Cycle validation shall operate on the relevant typed subgraph rather than on the entire universal relationship graph.

---

## 7. N-ary Relationships

A relationship involving three or more semantically essential participants shall not be decomposed into binary links when decomposition loses meaning, authority, uniqueness, or provenance.

Example:

```text
Assignment
  assignee: Actor
  assigned_object: Work Item
  assigning_authority: Decision
  applicable_workspace: Workspace
```

An n-ary relationship shall define named roles and may be modeled as a first-class relationship entity.

---

## 8. Endpoint Type Constraints

Each relationship type shall declare permitted endpoint types for every role.

Inheritance or polymorphic endpoint rules must be explicit.

A generic `any subject -> any subject` endpoint contract is prohibited for authoritative relationship types.

Cross-workspace and cross-aggregate endpoint permissions shall be declared independently from cardinality.

---

## 9. Validation Requirements

Before an authoritative relationship instance is committed, validation shall confirm:

1. the relationship type exists and is active;
2. every endpoint exists or is represented by an approved external reference;
3. endpoint types satisfy role constraints;
4. endpoint ordering satisfies direction rules;
5. minimum and maximum cardinalities are not violated;
6. uniqueness constraints are satisfied;
7. prohibited typed cycles are not introduced;
8. the actor or process has authority to bind the named roles;
9. relationship context and effective time are valid;
10. inverse projections resolve to the same authoritative relationship identity.

---

## 10. Constitutional Laws

### LAW-D09-11 — Explicit Roles

Every authoritative relationship type shall define semantically named endpoint roles.

### LAW-D09-12 — Source Is Not Authority

Source and Target are canonical directional roles and do not imply ownership, control, causation, or authority unless explicitly declared.

### LAW-D09-13 — Direction Is Semantic

Relationship direction shall be determined by domain meaning, not by foreign-key placement, API nesting, or object navigation.

### LAW-D09-14 — Symmetry Must Be Declared

A relationship is symmetric only when its type explicitly declares symmetry.

### LAW-D09-15 — One Assertion, One Identity

A relationship and its inverse semantic view shall resolve to one authoritative relationship identity unless explicitly defined as independent assertions.

### LAW-D09-16 — Cardinality Is Constitutional

Minimum and maximum role cardinalities are part of the relationship type contract and shall not be inferred solely from storage schema.

### LAW-D09-17 — Many-to-Many Requires Meaning

A many-to-many relationship shall have explicit domain semantics and shall become first-class when it carries business attributes, authority, provenance, validity, or lifecycle.

### LAW-D09-18 — Typed Cycle Governance

Cycle rules shall be evaluated per relationship category and type. Ownership, composition, strict dependency, and indeterminate authority cycles are prohibited by default.

### LAW-D09-19 — N-ary Integrity

A semantically n-ary relationship shall not be decomposed into binary relationships when decomposition loses essential meaning or governance.

### LAW-D09-20 — Technical Navigation Is Non-Constitutional

ORM navigation properties, graph traversal directions, indexes, caches, and read-model links shall not redefine relationship roles, direction, inverse meaning, or cardinality.

---

## 11. Decision D09.3

> Bizzi defines every authoritative relationship through explicit named endpoint roles, a declared direction model, formal inverse semantics when applicable, and minimum/maximum cardinality constraints for each role.
>
> Source and Target express the canonical statement direction but do not inherently express ownership, authority, causation, hierarchy, or lifecycle control.
>
> A business assertion and its inverse view share one authoritative relationship identity. Cardinality and cycle constraints are domain rules independent of persistence technology.
>
> Semantically essential n-ary relationships shall remain n-ary or become first-class relationship entities rather than being reduced to ambiguous binary edges.

---

## 12. Consequences

This decision enables:

- deterministic relationship validation;
- unambiguous inverse traversal;
- consistent graph and relational projections;
- prevention of accidental ownership and dependency semantics;
- governed many-to-many modeling;
- typed cycle detection;
- stable domain APIs independent of storage layout.

It requires:

- a relationship type registry;
- explicit role metadata;
- cardinality-aware validation;
- inverse-resolution rules;
- typed graph validation rather than universal cycle prohibition.

---

## 13. Roadmap Status

```text
0.1 Foundation                              COMPLETE
0.2 Relationship Taxonomy                   COMPLETE
0.3 Roles, Direction, and Cardinality       COMPLETE — IN WORKSHOP
0.4 Ownership, Authority, and Validation    NEXT
0.5 Lifecycle and Temporal Semantics
0.6 Consistency, Traversal, and Graph Views
0.7 Constitutional Review
```
