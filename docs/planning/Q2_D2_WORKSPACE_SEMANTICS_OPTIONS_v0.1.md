# WP19 / Q2 D2 Workspace-Semantics Options v0.1

**Status:** Draft — D2 decision analysis only
**Date:** 2026-08-30
**Subject:** ADR-0014 Q2 / D2 — reference-level workspace semantics
**Decision owner:** Project Owner through ADW-07
**Authority:** None. This artifact structures and evaluates D2 options; it does not decide D2.
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending Q2 subject-reference representation resolution.

## 1. D2 bounded question

**What workspace/scoping semantics must a persisted AuditRecord subject reference preserve across the current Q2 subject types — `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, and `Task` — without deciding how those semantics are physically stored or enforced?**

D2 addresses only the **durable workspace/scoping meaning of the subject reference**.

D2 does not decide:

- D3 subject deletion / post-deletion historical resolution;
- D4 database-enforced referential integrity;
- D5 future subject-type/extensibility requirement;
- persistence shape;
- FK/composite-FK strategy;
- physical columns or payload layout;
- migration policy or migration cost;
- ownership;
- runtime resolver/API contract;
- actor attribution;
- implementation;
- final Q2 persisted representation.

D1 is already **CLOSED — ACCEPTED** and supplies only the requirement for an explicit durable subject-type discriminator. D2 must not reinterpret or expand D1.

## 2. D2 evaluation criterion

A D2 rule is sufficient only if it gives a durable, unambiguous workspace/scoping interpretation for an AuditRecord subject reference across the five current Q2 subject types without requiring D2 to choose a persistence mechanism or enforcement layer.

For this pass:

- `Workspace`, `EnterpriseObject`, `WorkspaceMembership`, and `Task` are evaluated as subjects whose audit meaning is workspace-bound or workspace-contextual;
- `User` is structurally asymmetric because user identity need not itself be owned by exactly one workspace;
- a rule may use the AuditRecord's own durable workspace context as part of the semantic contract without requiring a particular physical encoding here;
- DB enforcement is explicitly out of scope and remains D4.

Results use:

- `PASS` — the semantic rule itself is sufficient for current-scope workspace interpretation;
- `FAIL` — the rule leaves current-scope workspace meaning ambiguous or contradictory;
- `CONDITIONAL` — the rule works only if an additional unresolved semantic condition is established.

## 3. D2 options

### D2-O1 — Reference-local workspace binding for every subject type

**Rule:** every persisted AuditRecord subject reference carries its own durable workspace binding, independent of any workspace semantics that may already be available from the AuditRecord or subject.

For current types:

- `Workspace`: reference binding denotes that Workspace;
- `EnterpriseObject`: binding denotes the workspace to which the subject belongs;
- `WorkspaceMembership`: binding denotes the membership's workspace;
- `Task`: binding denotes the task's workspace;
- `User`: binding denotes the workspace context in which that User is being audited, not ownership of the User identity itself.

**D2 result: PASS as a semantic rule, but over-prescriptive for D2-only selection.**

It can provide unambiguous workspace meaning, including for User, but making a distinct workspace binding mandatory on every reference risks deciding duplication/placement semantics that belong to persistence-shape evaluation.

**Does not by itself decide:** FK enforcement, composite keys, physical `workspace_id`, migration, resolver, ownership, D3–D5.

### D2-O2 — Subject-derived workspace semantics only

**Rule:** the subject reference carries no independent workspace meaning; workspace context is always derived from the referenced subject's own identity/scoping semantics.

**D2 result: FAIL for current five-type scope.**

This is insufficient because `User` need not have a single workspace ownership semantics, and a `Workspace` subject is the workspace rather than an object contained by another workspace. The rule therefore does not give one uniform durable interpretation for all five current subject types.

This failure does not reject any persistence candidate; it rejects only a D2 semantic rule that relies exclusively on subject-derived workspace meaning.

### D2-O3 — AuditRecord-context-only workspace semantics

**Rule:** the subject reference carries no workspace-specific semantic obligation beyond being interpreted inside the durable workspace context of its containing AuditRecord.

Under this rule, the AuditRecord's workspace context is authoritative for the audit occurrence, while the subject reference itself need not preserve any additional relationship between subject and workspace.

**D2 result: CONDITIONAL / insufficiently strong.**

This establishes where the audit occurred but does not by itself require that a workspace-scoped subject is actually consistent with that workspace. It would allow a reference contract whose audit workspace and subject workspace disagree unless another rule supplies consistency.

Such a consistency rule cannot be silently imported from D4 or implementation.

### D2-O4 — Durable audit-workspace binding plus subject-consistency rule

**Rule:** every persisted AuditRecord subject reference is interpreted within the AuditRecord's durable workspace context, and the durable reference contract must preserve the following semantic consistency:

1. for a `Workspace` subject, the referenced Workspace is the AuditRecord's workspace context;
2. for a workspace-scoped `EnterpriseObject`, `WorkspaceMembership`, or `Task` subject, the subject belongs to the AuditRecord's workspace context;
3. for a `User` subject, the User identity may be globally scoped, but the AuditRecord records that User as the audited subject within the AuditRecord's workspace context; D2 does not assert that the User is owned by that workspace.

The rule requires durable semantic consistency but does not prescribe whether that consistency is represented redundantly in the subject reference, derivable from subject identity, checked by application logic, or enforced by database constraints.

**D2 result: PASS.**

This is sufficient across all five current subject types while respecting the User/Workspace asymmetry and without deciding persistence shape or enforcement location.

### D2-O5 — Per-type independent workspace rules

**Rule:** each subject type may define its own unrelated workspace semantics with no common Q2-level invariant.

**D2 result: FAIL.**

Type-specific details are unavoidable, but without a common invariant the persisted AuditRecord subject-reference contract does not establish what cross-workspace inconsistency means at Q2 level. This leaves S10 unresolved by design rather than deciding it.

Per-type realization details may still be needed later; D2 only requires a common semantic invariant.

## 4. D2 comparison

| Option | Workspace meaning across all five current types | Handles `User` asymmetry | Requires persistence shape? | Requires DB enforcement? | D2 result |
|---|---|---|---|---|---|
| O1 Reference-local binding everywhere | Unambiguous | Yes | Risks over-prescribing duplication/placement | No | PASS but over-prescriptive |
| O2 Subject-derived only | Not uniform | No | No | No | FAIL |
| O3 AuditRecord context only | Audit occurrence scoped, subject consistency unresolved | Yes | No | No | CONDITIONAL |
| O4 Audit workspace + subject consistency | Unambiguous common invariant | Yes | No | No | PASS |
| O5 Per-type unrelated rules | No common invariant | Potentially | No | No | FAIL |

## 5. D2 evaluation finding

The narrowest rule that resolves workspace semantics without choosing physical representation is O4:

- it preserves the AuditRecord's durable workspace context;
- it requires workspace-scoped subjects to be semantically consistent with that context;
- it treats `Workspace` as self-contextual rather than as a child of another workspace;
- it permits `User` identity to remain globally scoped while still locating the audit occurrence in one workspace;
- it does not require a duplicate `workspace_id` inside every subject reference;
- it does not choose DB versus application/domain enforcement;
- it does not select N1–N5 or GC-002 Alternative B.

O1 is semantically sufficient but stronger than necessary because it requires a separate reference-local workspace binding even when durable context could be supplied without that duplication. O3 is too weak because it does not require subject/workspace consistency. O2 and O5 do not provide a sufficient common Q2 invariant.

## 6. D2 recommendation

### D2 recommendation — PROPOSED FOR PROJECT OWNER REVIEW

**A persisted AuditRecord subject reference MUST be interpreted within the AuditRecord's durable workspace context. For a `Workspace` subject, the referenced Workspace MUST be that workspace context. For a workspace-scoped `EnterpriseObject`, `WorkspaceMembership`, or `Task` subject, the subject MUST belong to that workspace context. A `User` subject MAY remain globally scoped; D2 requires only that the AuditRecord identifies that User as the audited subject within the AuditRecord's workspace context and does not assert workspace ownership of the User identity. D2 does not decide how workspace consistency is physically represented or enforced.**

### D2 decision status

**PROPOSED — NOT YET ACCEPTED**

### D2 scope

**Reference-level workspace/scoping semantics only.**

### Explicit non-decisions

D2 does not decide:

- D3;
- D4;
- D5;
- persistence shape;
- whether `workspace_id` is duplicated in the subject reference;
- composite-FK or other FK strategy;
- database versus application/domain enforcement;
- migration;
- ownership;
- runtime resolver/API;
- actor attribution;
- implementation;
- final Q2 persisted representation.

### Authority

**NOT YET ESTABLISHED.** This recommendation becomes D2 authority only after explicit Project Owner acceptance and separate authority recording.

## 7. Gate result

**D2 OPTIONS STRUCTURED AND EVALUATED — ONE REPRESENTATION-NEUTRAL WORKSPACE-SEMANTICS RULE RECOMMENDED — D2 REMAINS OPEN / NOT YET ACCEPTED.**

Current Q2 state:

- D1: **CLOSED — ACCEPTED**;
- D2: **OPEN — PROPOSED / NOT YET ACCEPTED**;
- D3–D5: **OPEN**;
- Q2 persisted representation: **OPEN**;
- N1–N5: **UNAPPROVED**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED pending Q2 subject-reference representation resolution**.

The next bounded step is Project Owner review of the D2 recommendation. No implementation or persisted-representation selection is authorized by this artifact.