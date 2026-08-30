# WP19 / Q2 D2 Workspace-Semantics Options v0.1

**Status:** Draft — D2 proposal narrowed for Project Owner review  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 / D2 — semantic meaning of `Workspace` as an AuditRecord subject type  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact proposes a D2 semantic rule; it does not decide D2.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending Q2 subject-reference representation resolution.

## 1. D2 bounded question

**What does `Workspace` mean when the accepted D1 subject-type discriminator of a durable persisted AuditRecord subject reference has the value `Workspace`?**

D2 is limited to the semantic meaning of `Workspace` as a first-class audited subject type.

D2 must not convert `Workspace` into an implicit owning/current/context workspace for another subject type.

D1 is already **CLOSED — ACCEPTED** and establishes only that every durable subject reference has an explicit subject-type discriminator whose committed value identifies exactly one of the five current Q2 subject types.

## 2. Required semantic distinctions

D2 must keep the following concepts distinct:

1. **`Workspace` as subject** — the audited subject identity is the Workspace entity itself.
2. **Workspace associated with another subject** — workspace ownership, containment, scope, tenancy, or other contextual relation of a different subject.
3. **`WorkspaceMembership` as subject** — the audited subject is the membership entity/relationship itself, not the Workspace it references.
4. **`EnterpriseObject` associated with a workspace** — the audited subject remains the EnterpriseObject; its workspace association is contextual metadata unless separately made part of that subject-reference contract by another decision.
5. **No workspace context** — D2 does not require every subject reference or every possible audit semantic to derive identity from a workspace context.
6. **Multi-workspace / cross-workspace semantics** — if such semantics are allowed or required, D2 does not define them here. They remain an independent scoping/context question and must not redefine `Workspace` subject identity by implication.

The same separation applies to `User` and `Task`: a workspace related to those subjects is not an implicit substitution for their subject identity.

## 3. D2 options considered

### D2-O1 — `Workspace` is the Workspace entity itself

**Rule:** when the D1 discriminator value is `Workspace`, the durable AuditRecord subject reference identifies the Workspace entity itself.

A workspace associated with another audited subject is contextual metadata or a separate relation; it does not substitute for that subject.

**Result: PASS.**

This directly defines the semantic meaning of the `Workspace` discriminator without importing ownership, containment, tenancy, or workspace-consistency rules for the other four subject types.

### D2-O2 — `Workspace` means the owning/current workspace of another subject

**Rule:** a `Workspace` discriminator may be used to stand for the workspace that owns, contains, scopes, or is currently associated with another audited object.

**Result: FAIL.**

This collapses subject identity into contextual ownership. It would allow an AuditRecord whose actual audited subject is an `EnterpriseObject`, `WorkspaceMembership`, `Task`, or `User` context to be represented as `Workspace`, despite D1 requiring the discriminator to identify exactly one subject type.

### D2-O3 — `Workspace` is a fallback subject whenever workspace context exists

**Rule:** where an operation occurs in a workspace, `Workspace` may be used as the subject even if another current Q2 subject type is the concrete audited entity.

**Result: FAIL.**

This makes `Workspace` a universal fallback and weakens the accepted D1 distinction among the five subject types.

### D2-O4 — `Workspace` subject plus mandatory ownership/scoping rule for every other type

**Rule:** `Workspace` identifies the Workspace entity itself, while D2 simultaneously defines how every other subject type must relate to a workspace.

**Result: OUT OF D2 SCOPE.**

The first clause is valid D2 semantics. The second clause broadens D2 into contextual ownership, scoping, consistency, or cross-workspace policy and risks deciding later decision surfaces or persistence constraints by implication.

## 4. Narrowing finding

Only D2-O1 is retained as the bounded D2 semantic rule.

The following are rejected from the active D2 choice:

- using `Workspace` as the owning/current workspace of another subject;
- using `Workspace` as a fallback whenever workspace context exists;
- using D2 to impose a universal workspace-consistency or ownership rule on `EnterpriseObject`, `User`, `WorkspaceMembership`, or `Task`.

These removals do not decide how workspace context is represented, whether cross-workspace operations exist, or what consistency rules may later apply.

## 5. Preferred D2 proposal

### D2 recommendation

**`Workspace` is a first-class subject type. When the discriminator is `Workspace`, the durable subject reference identifies the Workspace entity itself. A workspace associated with another subject is contextual metadata, not an implicit substitution for that subject.**

This rule means, in particular:

- `Workspace` does not stand in for an `EnterpriseObject` merely because that object belongs to a workspace;
- `Workspace` does not stand in for a `WorkspaceMembership` merely because the membership references that workspace;
- `Workspace` does not stand in for a `Task` merely because the task is workspace-scoped;
- `Workspace` does not stand in for a `User` merely because the audit occurs in a workspace context.

## 6. D2 decision status

**PROPOSED — NOT YET ACCEPTED**

### D2 scope

**Semantic meaning of `Workspace` as a subject type only.**

### Explicit non-decisions

D2 does not decide:

- how another subject's workspace association is represented;
- whether all subjects must have workspace context;
- multi-workspace semantics;
- cross-workspace semantics;
- workspace ownership or containment rules;
- subject/workspace consistency enforcement;
- D3;
- D4;
- D5;
- persistence shape;
- physical placement of the D1 type discriminator;
- FK or composite-FK strategy;
- database versus application/domain enforcement;
- migration;
- ownership of persistence implementation;
- runtime resolver/API contract;
- actor attribution;
- implementation;
- final Q2 persisted representation.

### Authority

**NOT YET ESTABLISHED.** This proposal becomes D2 authority only after explicit Project Owner acceptance and separate authority recording.

## 7. Gate result

**D2 NARROWED TO `Workspace` SUBJECT IDENTITY — SUBJECT IDENTITY KEPT DISTINCT FROM WORKSPACE CONTEXT / OWNERSHIP — ONE SEMANTIC RULE PROPOSED — NOT YET ACCEPTED.**

Current Q2 state:

- D1: **CLOSED — ACCEPTED**;
- D2: **OPEN — PROPOSED / NOT YET ACCEPTED**;
- D3–D5: **OPEN**;
- Q2 persisted representation: **OPEN**;
- N1–N5: **UNAPPROVED**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED pending Q2 subject-reference representation resolution**.

No model, migration, interim persistence representation, or WP19 implementation authorization is created by this artifact.