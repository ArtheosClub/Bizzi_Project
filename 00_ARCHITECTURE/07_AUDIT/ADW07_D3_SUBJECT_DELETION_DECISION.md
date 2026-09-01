# ADW-07 / Q2 D3 — Subject Deletion / Historical Resolution Decision

**Status:** ACCEPTED  
**Decision:** D3 — CLOSED / ACCEPTED  
**Decision Date:** 2026-08-30  
**Decision Owner:** Project Owner / Andrew  
**Parent:** ADW-07 — Events, Audit and Provenance  
**Scope:** ADR-0014 Q2 / D3 only

## 1. Accepted rule

> **A committed AuditRecord MUST preserve enough durable subject-reference information to identify its historical audited subject after later deletion or deactivation of that subject. Historical resolvability does not require the subject, or any associated context, to remain dereferenceable as a currently live or active entity. Deletion or deactivation of associated context MUST NOT substitute, reinterpret, or rewrite the committed audited-subject identity. Subject deletion, subject deactivation, and context deletion/deactivation do not by themselves authorize deletion or mutation of the committed AuditRecord. D3 does not require the AuditRecord reference itself either to prevent or to permit subject or context lifecycle changes; referential-integrity behavior, retention/legal/compliance policy, and physical representation remain separate decisions.**

## 2. Normative meaning

D3 establishes a historical-identity invariant for committed AuditRecords.

For each of the five current Q2 subject types — `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, and `Task` — later subject deletion or deactivation MUST NOT by itself cause a committed AuditRecord to lose or change the historical identity of the audited subject.

Deletion, deactivation, closure, supersession, termination, or loss of availability of an associated Workspace or other context MUST NOT silently replace, reinterpret, or rewrite the committed audited-subject identity.

D3 distinguishes historical subject identity from current live dereferenceability. A historical AuditRecord may remain semantically resolvable even where the audited subject or associated context is no longer a live/active entity.

## 3. Durable audit-history boundary

Subject deletion, subject deactivation, and context deletion/deactivation do not by themselves authorize deletion or mutation of the committed AuditRecord.

D3 therefore does **not** authorize implicit cascade deletion of AuditRecords when a subject or associated context is deleted.

Any future proposal that would delete committed AuditRecords as a consequence of subject/context lifecycle change requires separate explicit architecture authority and must be reconciled with immutable/durable historical-record requirements.

## 4. Subject-type boundary

This decision applies to the current Q2 subject set:

- `Workspace`;
- `EnterpriseObject`;
- `User`;
- `WorkspaceMembership`;
- `Task`.

D3 does not redefine their D1 type identities and does not alter D2 Workspace subject semantics.

For `WorkspaceMembership`, historical membership identity is not collapsed into the related User or Workspace. For another subject associated with a Workspace, loss of Workspace context does not convert that subject into a Workspace subject.

## 5. Explicit non-decisions

D3 does **not** decide:

- whether physical deletion is permitted for any particular subject type;
- whether deactivation, closure, termination, archival, or supersession is permitted or required for any particular subject type;
- whether deletion/deactivation of any particular context is permitted;
- retention periods;
- legal holds, erasure/anonymization obligations, regulatory exceptions, or compliance policy;
- `RESTRICT`, `CASCADE`, `SET NULL`, or any other FK action;
- whether referential integrity is database-enforced, application/domain-enforced, mixed, or absent;
- D4;
- D5;
- FK, composite FK, payload, opaque identifier, registry, tombstone, archival table, snapshot, or any other persistence shape;
- N1–N5 selection, rejection, preference, or default;
- migration;
- runtime resolver/API contract;
- WP19 implementation.

## 6. GC-002 boundary

GC-002 Alternative B remains **PROPOSED ONLY**.

This D3 decision does not approve, incorporate, upgrade, or confer normative authority on GC-002 Alternative B or any composite-FK proposal.

## 7. Relationship to prior Q2 decisions

- D1: **CLOSED — ACCEPTED**. Its explicit durable subject-type-disambiguation rule remains in force.
- D2: **CLOSED — ACCEPTED**. Its first-class `Workspace` subject semantics and subject/context separation remain in force.
- D3: **CLOSED — ACCEPTED** by this artifact.
- D4: **OPEN**.
- D5: **OPEN**.

D3 is independent authority and does not merge D1, D2, D4, or D5 into a single representation decision.

## 8. Q2 and implementation state

Q2 persisted AuditRecord subject-reference representation remains **OPEN**.

N1–N5 remain **UNAPPROVED**.

ADW-07 remains **OPEN**.

WP19 remains **BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution**. No persistence shape, model, migration, or implementation authorization is created by this D3 decision.

A separate explicit interim-shape authorization, if ever issued by Project Owner, would be required to alter that implementation gate before final Q2 representation resolution.

## 9. Decision result

**D3 CLOSED — ACCEPTED. HISTORICAL AUDITED-SUBJECT IDENTITY MUST SURVIVE LATER SUBJECT LIFECYCLE CHANGE; SUBJECT/CONTEXT LIFECYCLE CHANGE DOES NOT AUTHORIZE DELETION OR MUTATION OF COMMITTED AUDIT HISTORY; D4/D5 AND PERSISTENCE REPRESENTATION REMAIN OPEN.**