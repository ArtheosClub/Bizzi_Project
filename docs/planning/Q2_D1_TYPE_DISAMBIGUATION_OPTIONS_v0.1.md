# WP19 / Q2 D1 Type-Disambiguation Options v0.1

**Status:** Draft — D1 decision proposal only
**Date:** 2026-08-30
**Subject:** ADR-0014 Q2 / D1 — subject-type disambiguation
**Decision owner:** Project Owner through ADW-07
**Authority:** Not yet established. Proposed for explicit Project Owner acceptance.
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending Q2 resolution.

## 1. D1 bounded question

**Can the rule unambiguously distinguish the subject type of a persisted AuditRecord subject reference across the five current Q2 subject types: `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, and `Task`?**

D1 chooses only the **subject-type disambiguation rule**.

This pass does not evaluate or decide:

- database-level referential integrity;
- a concrete FK or column schema;
- migration policy or migration cost;
- persistence ownership;
- runtime resolver contract;
- actor attribution;
- D2 workspace/reference scoping semantics;
- D3 deletion/historical-resolution policy;
- D4 DB-enforced referential integrity policy;
- D5 future subject-type/extensibility policy;
- the final Q2 persisted representation.

No N1–N5 candidate and no GC-002 Alternative B is approved by default.

## 2. D1 evaluation rule

An option is sufficient for D1 only if, from the **durably persisted AuditRecord subject-reference information or its durable interpretation rule**, the system can determine exactly one of the five subject types for the committed reference.

The evaluation asks only whether type disambiguation is unambiguous. It does not ask how the identified subject instance is joined, validated, resolved at runtime, migrated, owned, or protected by database constraints.

## 3. D1 options

### D1-O1 — Explicit persisted subject-type discriminator

**Rule:** the persisted AuditRecord subject reference carries an explicit durable subject-type discriminator whose value identifies exactly one supported subject type.

For the current Q2 scope, the discriminator vocabulary must distinguish:

- `Workspace`;
- `EnterpriseObject`;
- `User`;
- `WorkspaceMembership`;
- `Task`.

**D1 evaluation:** **SUFFICIENT.** An explicit discriminator can unambiguously identify one of the five subject types without depending on table shape, workspace semantics, FK enforcement, runtime resolution, or ownership.

**Does not imply:** a `subject_type + subject_id` physical schema, a particular column, enum implementation, FK, resolver, migration, or future extensibility contract.

### D1-O2 — Type inferred solely from subject identifier value

**Rule:** the subject type is determined from the persisted identifier value itself, without a separate explicit type discriminator.

**D1 evaluation:** **NOT CURRENTLY SUFFICIENT.** The current corpus does not establish a shared type-prefixed/global identity namespace or another durable identifier encoding that makes the five subject types unambiguously distinguishable from the identifier alone. Creating such a namespace here would be new architecture, not evaluation of an established D1 rule.

This does not reject opaque-identifier candidate N4. It only means identifier-only type inference lacks an established disambiguation rule at D1 today.

### D1-O3 — Type inferred from physical reference location/slot

**Rule:** subject type is determined by which subject-type-specific persisted reference location is used.

**D1 evaluation:** **CONDITIONALLY SUFFICIENT AS A TYPE RULE, BUT OVER-COUPLED TO PERSISTENCE SHAPE FOR D1.** If mutually interpretable type-specific locations existed, location could distinguish the five types. But adopting this as D1 authority would silently constrain the persistence representation toward a per-type structural shape before the separate Q2 representation decision.

Therefore it is not the preferred D1-only rule. This is not an architecture rejection of N3.

### D1-O4 — Type inferred from referenced database target / FK relation

**Rule:** subject type is determined by the database relation or target to which the persisted reference is constrained.

**D1 evaluation:** **CONDITIONALLY SUFFICIENT AS A TYPE RULE, BUT OUT OF D1 SCOPE AS AN AUTHORITY CHOICE.** A concrete target relation can identify type, but making DB target structure the authoritative type-disambiguation mechanism would decide part of D4/concrete persistence shape by implication.

This is not an architecture rejection of N2 or GC-002 Alternative B.

### D1-O5 — Type inferred from persisted AuditRecord content/payload

**Rule:** subject type is determined from a durable subject-type value or other unambiguous type marker inside persisted AuditRecord content.

**D1 evaluation:** **SUFFICIENT IN PRINCIPLE, BUT PLACEMENT IS NOT A D1 DECISION.** If persisted content contains an explicit durable type discriminator, the type can be unambiguously distinguished. However D1 should decide the semantic rule — explicit durable type discrimination — without deciding that the discriminator must live in payload/content.

This is not an approval or rejection of N5.

## 4. D1 evaluation finding

The representation-neutral common denominator that satisfies D1 without silently deciding D2–D5 or the Q2 persistence shape is:

> **The persisted AuditRecord subject reference must include, or be governed by, an explicit durable subject-type discriminator whose committed value unambiguously identifies exactly one supported subject type.**

For the current Q2 scope, the discriminator must distinguish `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, and `Task`.

The word **explicit** means that type interpretation is part of the durable reference contract rather than being guessed from transient runtime state. It does **not** prescribe where or how that discriminator is physically stored.

The word **durable** means the committed type meaning must remain interpretable as historical AuditRecord meaning. It does not establish a runtime resolver contract or migration policy.

## 5. Proposed explicit D1 choice

### D1 decision — PROPOSED FOR PROJECT OWNER ACCEPTANCE

**A persisted AuditRecord subject reference MUST carry an explicit durable subject-type discriminator, as part of its durable reference contract, whose committed value unambiguously identifies exactly one supported subject type. For the current Q2 scope, that rule MUST distinguish `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, and `Task`. The physical placement and persistence mechanism of that discriminator are not decided by D1.**

### Scope

**Only subject-type disambiguation.**

### Does not decide

- D2 — reference-level workspace semantics;
- D3 — subject deletion / historical-resolution policy;
- D4 — DB-enforced referential-integrity policy;
- D5 — subject-type-set / future-extensibility requirement;
- database-level integrity;
- concrete FK/schema shape;
- migration policy;
- ownership;
- runtime resolver contract;
- actor attribution;
- final Q2 persisted representation.

### Authority

**NOT YET ESTABLISHED — PROPOSED FOR EXPLICIT PROJECT OWNER ACCEPTANCE.**

## 6. Candidate-neutrality check

This proposed D1 rule does not select N1–N5:

- N1 could satisfy it through a durable polymorphic type contract;
- N2 could satisfy it in a concrete realization without D1 deciding the FK mechanism;
- N3 could satisfy it without D1 requiring per-type physical slots as the discriminator mechanism;
- N4 would need an explicit durable type contract in addition to or governing opaque identity, but D1 does not define its resolver;
- N5 could satisfy it through persisted content, but D1 does not require payload placement.

These statements are compatibility observations only. They are not candidate approvals, recommendations, or final Q2 evaluation.

## 7. Gate result

**D1 OPTIONS EVALUATED — ONE REPRESENTATION-NEUTRAL TYPE-DISAMBIGUATION RULE PROPOSED — AUTHORITY NOT YET ESTABLISHED.**

D1 remains **OPEN** until explicit Project Owner acceptance.

WP19 remains **BLOCKED / UNAUTHORIZED pending Q2 subject-reference representation resolution**.

If the Project Owner accepts the proposed D1 rule, the next bounded actions are:

1. record D1 as explicit authority without expanding its scope;
2. keep D2–D5 OPEN;
3. proceed to D2 options as a separate decision pass;
4. do not silently substitute the accepted D1 mechanism into D2–D5.