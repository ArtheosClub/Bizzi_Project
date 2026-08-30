# WP19 / Q2 D1 Type-Disambiguation Options v0.1

**Status:** Draft — D1 decision proposal only
**Date:** 2026-08-30
**Subject:** ADR-0014 Q2 / D1 — subject-type disambiguation
**Decision owner:** Project Owner through ADW-07
**Authority:** Not yet established. Proposed for explicit Project Owner acceptance.
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending Q2 resolution.

## 1. D1 bounded question

**Can the rule unambiguously distinguish the subject type of a persisted AuditRecord subject reference across the five current Q2 subject types: `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, and `Task`?**

D1 evaluates and proposes only a **subject-type disambiguation rule**.

This pass does not evaluate or decide:

- database-level referential integrity or FK enforcement;
- concrete persistence/FK/column shape;
- migration policy or migration cost;
- extensibility beyond the current five types;
- immutability/evolution cost;
- persistence ownership;
- runtime resolver/API contract;
- actor attribution;
- D2, D3, D4, or D5;
- final Q2 persisted representation.

No N1–N5 candidate and no GC-002 Alternative B is approved by default.

## 2. D1 evaluation method

For each option this pass records:

1. the exact type-disambiguation rule;
2. the subject-type values admitted by the rule for current Q2 scope;
3. whether one persisted reference can be interpreted as more than one of those types;
4. a D1-only result: `PASS`, `FAIL`, or `CONDITIONAL`;
5. a short explanation;
6. explicit non-decisions.

`PASS` means the rule itself is sufficient to identify exactly one of the five subject types without requiring an unresolved condition.

`FAIL` means the rule, under currently established corpus facts, does not uniquely determine one of the five types.

`CONDITIONAL` means the rule can uniquely determine type only if an additional durable condition is established. A conditional result is not architecture rejection and does not authorize that condition.

The evaluation asks only whether type disambiguation is unambiguous. It does not compare integrity strength, migration cost, extensibility, resolver design, ownership, or implementation convenience.

## 3. D1 option evaluation

| Option | Exact D1 rule | Allowed current subject-type values | Can one persisted reference mean >1 type? | Result | Short explanation |
|---|---|---|---|---|---|
| **O1 Explicit type tag** | Every persisted subject reference has an explicit durable type discriminator whose committed value denotes exactly one member of the current type vocabulary. | `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, `Task` | **No**, if the discriminator is single-valued and its vocabulary has one semantic meaning per value. | **PASS** | Type is directly and durably disambiguated without needing a persistence-shape or resolver assumption. |
| **O2 Type-qualified identity** | The persisted subject identity is durably qualified by a type/namespace component such that the qualification denotes exactly one current subject type. | Type qualification must map uniquely to `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, or `Task`. | **No**, provided the qualification contract is one-to-one with the five type meanings. | **PASS** | Type qualification is itself an explicit durable disambiguation rule. D1 does not decide how the qualification is physically encoded. |
| **O3 Globally unique identifiers** | All five subject types use one common identifier space, and type is inferred from the identifier alone. | No separate type value is present; all five types participate in the same identifier space. | **Yes under current facts**: uniqueness of an identifier value does not by itself state which subject type owns that value. | **FAIL** | Collision-freedom across types establishes instance uniqueness, not type semantics. A separate type-bearing namespace/encoding would turn this into O2 rather than identifier uniqueness alone. |
| **O4 Type-specific slots** | The persisted reference occurs in one of a set of positions whose durable semantic meaning is bound to a particular subject type. | One distinguishable position/semantic slot for each of `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, `Task`. | **CONDITIONALLY No**: only if the reference contract guarantees an unambiguous active type position. | **CONDITIONAL** | Position can encode type, but the needed unambiguous-position rule must be established. D1 does not authorize a physical per-type-column schema or exclusivity constraint. |
| **O5 Unqualified identifier** | A persisted identifier with no explicit type qualification/discriminator is used, and type is inferred from that value or external interpretation. | No explicit subject-type values are carried by the reference. | **Yes / not proven unique under current corpus.** The current five tables use independently generated identifiers and no established type-bearing identity convention is authoritative. | **FAIL** | An unqualified value does not itself provide durable type semantics. Inventing a resolver or namespace here would exceed D1 evaluation. |

## 4. Option details and explicit non-decisions

### O1 — Explicit type tag — PASS

**Rule:** every persisted AuditRecord subject reference carries, as part of its durable reference contract, one explicit subject-type discriminator value.

**Current allowed type values:** exactly the five current Q2 semantic types: `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, `Task`.

**Ambiguity:** the same committed discriminator value cannot denote more than one of those types under the rule.

**Does not decide:** where the discriminator is stored; whether it is a DB column, payload field, composite component, enum, string, or other encoding; FK enforcement; D2–D5; migration; ownership; runtime resolver/API; actor attribution; implementation.

### O2 — Type-qualified identity — PASS

**Rule:** persisted subject identity contains a durable qualification whose semantic contract identifies one subject type as part of the identity reference.

**Current allowed type values:** the qualification must map one-to-one to the same five current Q2 types.

**Ambiguity:** none if the qualification contract is one-to-one. A qualification that can denote multiple types would not satisfy O2.

**Does not decide:** delimiter/encoding; global registry; DB key shape; FK; resolver; workspace semantics; D2–D5; migration; ownership; implementation.

**Relationship to O1:** O2 is semantically compatible with the broader O1 rule because the type qualification is an explicit durable type discriminator. D1 need not choose its physical encoding.

### O3 — Globally unique identifiers — FAIL

**Rule:** one collision-free identifier space spans all five types and the identifier alone is expected to reveal the type.

**Current allowed type values:** none are explicitly encoded.

**Ambiguity:** global uniqueness can prove that an identifier belongs to at most one subject instance if such a global identity system exists, but it does not make the subject type semantically derivable from the identifier value unless the identifier also carries type qualification. Type qualification would make the rule O2.

**Does not decide:** whether a future global identity system should exist; registry design; resolver; FK; D2–D5; migration; ownership; implementation.

### O4 — Type-specific slots — CONDITIONAL

**Rule:** the durable semantic position occupied by the reference determines subject type.

**Current allowed type values:** one semantic position for each of the five current Q2 types.

**Ambiguity:** disambiguation succeeds only if the contract guarantees that a committed AuditRecord reference cannot simultaneously or ambiguously activate multiple type positions for one audited subject.

**Why conditional:** the current D1 evaluation must not invent an exclusivity/cardinality constraint. Therefore type-specific positions are capable of disambiguation, but their sufficiency depends on a separately established unambiguous-position rule.

**Does not decide:** physical columns; nullability; CHECK constraints; FK enforcement; exact cardinality implementation; D2–D5; migration; ownership; implementation.

### O5 — Unqualified identifier — FAIL

**Rule:** type is inferred from an identifier that carries no explicit durable type qualification.

**Current allowed type values:** no type vocabulary is persisted as part of the rule.

**Ambiguity:** unresolved. Current corpus facts do not establish a durable convention by which the raw identifier alone determines whether the subject is Workspace, EnterpriseObject, User, WorkspaceMembership, or Task.

**Does not decide:** whether an external resolver could be designed later; namespace policy; DB integrity; D2–D5; migration; ownership; implementation.

## 5. D1 evaluation finding

O1 and O2 pass the D1-only test because both make type meaning an explicit durable part of the subject-reference contract. O2 is a qualified encoding of the same semantic requirement rather than a reason to choose a particular persistence shape.

O3 and O5 fail the bounded D1 test because identifier uniqueness or an unqualified identifier does not, by itself, establish durable type semantics.

O4 is conditional because type-specific position can encode type, but D1 cannot silently invent the exclusivity/cardinality rule needed to guarantee unambiguous interpretation.

The narrow representation-neutral rule supported by the D1 evaluation is therefore explicit durable type discrimination, while leaving its physical placement and mechanism open.

## 6. D1 recommendation

### D1 recommendation

**A persisted AuditRecord subject reference MUST include an explicit durable subject-type discriminator as part of its durable reference contract. The discriminator's committed value MUST identify exactly one of the current Q2 subject types: `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, or `Task`. Type qualification within the durable subject identity satisfies this rule. The physical placement and persistence mechanism of the discriminator are not decided by D1.**

### D1 decision status

**PROPOSED — NOT YET ACCEPTED**

### D1 scope

**Type disambiguation only.**

### Explicit non-decisions

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

**NOT YET ESTABLISHED.** This recommendation is proposed for explicit Project Owner acceptance. It becomes new D1 authority only after that acceptance is explicitly given and separately recorded.

## 7. Candidate-neutrality and gate result

This D1 recommendation does not approve or reject N1–N5 and does not approve GC-002 Alternative B. Candidate compatibility with an accepted D1 rule is a later evaluation input; it is not a D1 architecture selection.

**D1 OPTIONS EVALUATED — D1 RECOMMENDATION PRODUCED — DECISION STATUS PROPOSED / NOT YET ACCEPTED — NO NEW AUTHORITY CREATED.**

WP19 remains **BLOCKED / UNAUTHORIZED pending Q2 subject-reference representation resolution**.

Only after explicit Project Owner acceptance may D1 be recorded as a separate Project Owner decision. D2–D5 must remain open, and the accepted D1 rule must not be allowed to close or answer them by implication.