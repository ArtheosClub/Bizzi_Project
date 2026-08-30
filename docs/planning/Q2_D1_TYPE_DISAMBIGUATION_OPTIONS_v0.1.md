# WP19 / Q2 D1 Type-Disambiguation Options v0.1

**Status:** Draft — D1 proposal narrowed for Project Owner acceptance
**Date:** 2026-08-30
**Subject:** ADR-0014 Q2 / D1 — subject-type disambiguation
**Decision owner:** Project Owner through ADW-07
**Authority:** Not yet established. Proposed for explicit Project Owner acceptance.
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending Q2 resolution.

## 1. D1 bounded question

**Can the rule unambiguously distinguish the subject type of a persisted AuditRecord subject reference across the five current Q2 subject types: `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, and `Task`?**

D1 decides only the **subject-type disambiguation rule**.

This pass does not evaluate or decide database integrity, FK enforcement, persistence shape, migration policy/cost, extensibility, immutability/evolution cost, ownership, runtime resolver/API, actor attribution, D2–D5, implementation, or the final Q2 representation.

No N1–N5 candidate and no GC-002 Alternative B is approved by default.

## 2. Source options considered

The D1 evaluation considered these abstract rules:

1. Explicit type tag;
2. Type-qualified identity;
3. Globally unique identifiers;
4. Type-specific slots;
5. Unqualified identifier.

The bounded evaluation used only one criterion: **whether one committed persisted reference can be interpreted as exactly one of the five current subject types without relying on an unresolved additional condition.**

## 3. Narrowing result

### Retained semantic rule — Explicit durable type discriminator

The retained D1 rule is:

> The persisted AuditRecord subject reference carries, as part of its durable reference contract, an explicit subject-type discriminator whose committed value identifies exactly one supported subject type.

For current Q2 scope, the allowed semantic values are:

- `Workspace`;
- `EnterpriseObject`;
- `User`;
- `WorkspaceMembership`;
- `Task`.

A committed reference conforming to this rule cannot be interpreted as more than one of these subject types.

**D1 result: PASS.**

### Type-qualified identity — absorbed into the retained rule

Type-qualified identity is not retained as a separate competing D1 rule. If a durable identity qualification explicitly identifies one subject type, that qualification is simply one encoding of an explicit durable type discriminator.

Therefore D1 does not need a second semantic option for the same requirement, and it does not decide how the discriminator is physically encoded.

### Removed from active D1 choice — Globally unique identifiers

A globally collision-free identifier can identify one subject instance, but uniqueness alone does not state whether the subject is Workspace, EnterpriseObject, User, WorkspaceMembership, or Task.

**D1 result: FAIL.**

It is removed from the active D1 choice because it distinguishes type only if an additional type-bearing convention is introduced. If such qualification is added, the rule becomes the retained explicit-discriminator rule.

### Removed from active D1 choice — Type-specific slots

A type-specific position can convey subject type only if a separate rule guarantees that the active position is unambiguous for one audited subject.

**D1 result: CONDITIONAL.**

It is removed from the active D1 choice because its sufficiency depends on an unresolved structural/exclusivity condition and would couple D1 to persistence shape.

This removal is not an architecture rejection of candidate N3.

### Removed from active D1 choice — Unqualified identifier

An identifier carrying no durable type qualification does not, under established corpus facts, determine whether the subject is Workspace, EnterpriseObject, User, WorkspaceMembership, or Task.

**D1 result: FAIL.**

It is removed from the active D1 choice because type would have to be supplied indirectly through an additional resolver/namespace convention that D1 does not establish.

This removal is not an architecture rejection of candidate N4.

## 4. Preferred D1 proposal

### D1 recommendation

**A persisted AuditRecord subject reference MUST include an explicit durable subject-type discriminator as part of its durable reference contract. The discriminator's committed value MUST identify exactly one of the current Q2 subject types: `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, or `Task`. Type qualification within a durable subject identity satisfies this rule. D1 does not decide the physical placement or persistence mechanism of the discriminator.**

### Why this proposal is preferred

It is the only retained semantic rule that:

- directly resolves the D1 question;
- does not depend on an unresolved external condition;
- does not infer type indirectly;
- does not require D1 to choose a FK/schema/payload/slot mechanism;
- preserves the independence of D2–D5 and the later Q2 representation decision.

## 5. Decision status and explicit non-decisions

### D1 decision status

**PROPOSED — NOT YET ACCEPTED**

### D1 scope

**Type disambiguation only.**

### Explicit non-decisions

D1 does not decide:

- D2;
- D3;
- D4;
- D5;
- persistence shape;
- FK strategy or database-level integrity;
- migration policy;
- extensibility policy;
- immutability/evolution cost;
- ownership;
- runtime resolver/API contract;
- actor attribution;
- implementation;
- final Q2 persisted representation.

### Authority

**NOT YET ESTABLISHED.** This preferred D1 proposal becomes new D1 authority only after explicit Project Owner acceptance and separate authority recording.

## 6. Gate result

**ALL D1 OPTIONS REVIEWED — INDIRECT / AMBIGUOUS / CONDITION-DEPENDENT RULES REMOVED FROM ACTIVE CHOICE — EXPLICIT DURABLE TYPE DISCRIMINATOR RETAINED AS THE SOLE PREFERRED D1 PROPOSAL — NOT YET ACCEPTED.**

No candidate N1–N5 is approved or rejected by this narrowing. GC-002 Alternative B remains Proposed only.

WP19 remains **BLOCKED / UNAUTHORIZED pending Q2 subject-reference representation resolution**.

The next bounded step is explicit Project Owner acceptance or rejection/amendment of the preferred D1 proposal. Only after acceptance may D1 be recorded as authority. D2 remains unopened until that recording is complete.