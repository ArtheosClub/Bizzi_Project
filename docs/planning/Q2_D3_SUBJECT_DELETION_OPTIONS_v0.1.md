# WP19 / Q2 D3 Subject-Deletion / Historical-Resolution Options v0.1

**Status:** Draft — D3 decision analysis only  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 / D3 — audited-subject deletion and historical resolution  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact structures and evaluates D3 options; it does not decide D3.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit authorization of an interim shape.

## 1. D3 bounded question

**What must remain durably resolvable from a committed AuditRecord if its audited subject is later physically deleted, and what does D3 imply — or not imply — about deletion/deactivation of related context?**

D3 separates the following surfaces and must not collapse them:

1. **Audited-subject deletion** — deletion of the entity identified by the committed AuditRecord subject reference.
2. **Context deletion/deactivation** — deletion, deactivation, closure, supersession, or loss of availability of workspace/context associated with the subject or audit occurrence.
3. **Historical AuditRecord resolvability** — whether the committed AuditRecord still durably identifies the historical subject after live subject/context changes.
4. **Referential integrity** — whether and how database/application constraints maintain live references; this remains D4/persistence territory.
5. **Retention and legal/compliance policy** — retention duration, anonymization, erasure exceptions, and legal/compliance obligations are not decided by D3.
6. **Physical representation** — FK, composite FK, payload, opaque identifier, registry, tombstone, archival row, or other implementation mechanism is not decided by D3.

D3 must not collapse historical resolvability into continued live-row or live-context existence.

## 2. Authority carried into D3

D1 is **CLOSED — ACCEPTED**: a durable subject reference includes an explicit durable subject-type discriminator identifying exactly one current Q2 subject type.

D2 is **CLOSED — ACCEPTED**: `Workspace` is a first-class subject type; workspace context associated with another subject does not substitute for that subject identity.

D10 requires committed Historical Records, including AuditRecords, to preserve historical truth and remain immutable/durable. Correction of committed historical meaning is therefore by a new historical record rather than mutation of the committed record.

ADR-0014 requires a committed AuditRecord to durably identify the subject of the audited mutation.

These authorities require stable historical meaning but do **not** establish that every audited subject row or related context must exist forever.

## 3. D3 evaluation criteria

A D3 rule is sufficient only if:

- deletion of the audited subject cannot make the committed AuditRecord cease to identify which historical subject was audited;
- deletion/deactivation of related context cannot silently substitute a different subject identity or rewrite the committed historical meaning;
- the committed subject reference does not silently acquire a different meaning after deletion or context change;
- D1 type identity remains interpretable after deletion;
- D2 `Workspace` semantics remain intact;
- the rule does not silently choose persistence shape or D4 enforcement mechanism;
- the rule distinguishes historical identity from the ability to dereference a currently live entity or context;
- retention/legal/compliance questions remain separate.

Results use `PASS`, `FAIL`, or `CONDITIONAL`.

## 4. D3 options

### D3-O1 — Live-row-dependent resolution

**Rule:** a committed AuditRecord subject reference is historically resolvable only while the referenced live subject row/entity continues to exist.

**Result: FAIL.**

Physical deletion could destroy the ability to determine which subject was historically audited. That conflicts with ADR-0014 durable subject identification and the historical-stability requirement carried by A2/D10.

This does not mean deletion itself is prohibited; it means historical identity cannot depend solely on continued live-row existence.

### D3-O2 — Historical identity survives audited-subject deletion; live dereference is not required

**Rule:** after physical deletion of the audited subject, the committed AuditRecord MUST retain enough durable information to continue identifying the historical subject according to accepted D1/D2 semantics. The subject need not remain dereferenceable as a currently live entity.

**Result: PASS.**

This preserves historical identity while keeping live-entity lifecycle distinct from Historical Record meaning. It does not prescribe whether the durable information is relational, payload-based, opaque, registry-backed, or otherwise represented.

### D3-O3 — AuditRecord universally prevents audited-subject deletion

**Rule:** any subject referenced by an AuditRecord must remain physically present for as long as the AuditRecord exists; the reference therefore prevents physical deletion.

**Result: FAIL as a D3-wide requirement.**

This is stronger than the established historical requirement. Existing authority requires preservation of historical truth, not permanent retention of every live subject row. It would also risk importing a referential-integrity/delete policy that belongs to D4 or subject lifecycle authority.

A particular subject type may independently have stronger retention/deletion rules; D3 does not override them.

### D3-O4 — Historical identity survives deletion; deletion constraint remains separate

**Rule:** the durable AuditRecord MUST preserve historical subject identity after physical deletion, but D3 does not require the AuditRecord reference itself either to prevent or to permit deletion. Whether a concrete representation constrains deletion is decided separately by applicable subject lifecycle authority and D4/persistence decisions.

**Result: PASS.**

This retains the historical invariant without silently choosing `RESTRICT`, `CASCADE`, `SET NULL`, tombstones, permanent rows, registry infrastructure, or application-only enforcement.

### D3-O5 — Delete-time mutation of the committed AuditRecord reference

**Rule:** when the subject is deleted, the existing committed AuditRecord reference may be rewritten into a replacement historical form.

**Result: FAIL.**

This would mutate committed historical meaning and conflicts with the immutability/stability requirement. Any corrective or supplementary historical fact must be represented without rewriting the committed AuditRecord.

### D3-O6 — Context loss changes or replaces subject identity

**Rule:** deletion/deactivation of a workspace or other associated context may cause the committed AuditRecord subject reference to be reinterpreted as that context, or may invalidate the prior subject identity.

**Result: FAIL.**

This would violate D2 by conflating subject identity with context and would make committed historical meaning contingent on later context lifecycle changes.

Context availability may affect live resolution or operational access, but it must not silently replace the committed audited-subject identity.

## 5. Boundary cases

### 5.1 Audited `Workspace` subject

If the discriminator is `Workspace`, the Workspace itself is the audited subject under D2. Its later deletion/deactivation therefore falls under audited-subject lifecycle. If physical deletion is permitted by governing lifecycle authority, an existing AuditRecord must still identify that historical Workspace subject.

D3 does not decide whether Workspace deletion is allowed.

### 5.2 Workspace used only as context

If a different subject type is audited and a Workspace is merely context/association, deletion or deactivation of that Workspace does not convert the subject into `Workspace` and does not rewrite the committed subject identity.

D3 does not decide whether that context must remain independently resolvable, retained, or live; that depends on separate scoping, lifecycle, retention, and persistence authority.

### 5.3 `WorkspaceMembership`

The membership is the audited subject when the discriminator is `WorkspaceMembership`. Deletion/deactivation of the membership must not collapse its historical identity into either the User or Workspace participating in it. Likewise, later deletion/deactivation of the related User or Workspace must not silently substitute those entities for the committed membership subject identity.

### 5.4 `EnterpriseObject`

If an EnterpriseObject is physically deleted, the AuditRecord must retain the historical identity of that EnterpriseObject. D3 does not require a base `enterprise_objects` row, tombstone, or standalone-specialization row to survive unless separate authority requires it.

Loss or deactivation of an associated Workspace context does not change the EnterpriseObject subject identity.

### 5.5 `User`

D3 does not establish whether User deletion is legally or architecturally permitted. If it is permitted, AuditRecord historical subject identity must remain stable. Privacy/anonymization requirements, if any, are outside D3 unless separately introduced by authority.

Loss of workspace context associated with the audit occurrence does not turn the User subject into a Workspace subject.

### 5.6 `Task`

Task lifecycle/deletion policy is not selected here. Physical deletion, if allowed, cannot make a committed AuditRecord cease to identify the historical Task subject. Loss/deactivation of workspace context does not substitute Workspace for Task identity.

### 5.7 Referential integrity and cascade behavior

D3 does **not** select cascade behavior. In particular, D3 must not be read as authorizing cascade deletion of AuditRecords when their subjects or contexts are deleted. Such behavior could destroy immutable audit history and therefore requires separate explicit architecture justification if ever proposed.

This statement is a boundary/guardrail, not a D4 decision and not a persistence-shape selection.

### 5.8 Retention / legal / compliance

D3 preserves architectural historical identity semantics. It does not establish retention periods, legal holds, erasure/anonymization policy, regulatory exceptions, or compliance-specific deletion requirements.

Those policies may constrain later implementation but are outside this D3 decision unless explicitly incorporated by separate authority.

## 6. Preferred D3 proposal

The narrowest representation-neutral rule satisfying existing authority is:

> **A committed AuditRecord MUST preserve enough durable subject-reference information to identify its historical audited subject even if that subject is later physically deleted. Historical resolvability does not require the subject, or any associated context, to remain dereferenceable as a currently live entity. Deletion or deactivation of associated context MUST NOT substitute, reinterpret, or rewrite the committed audited-subject identity. D3 does not require the AuditRecord reference itself either to prevent or to permit subject or context deletion; referential-integrity behavior, retention/legal/compliance policy, and physical representation remain separate decisions. The committed AuditRecord subject reference MUST NOT be rewritten merely because the subject or associated context is deleted or deactivated.**

This combines the valid parts of O2/O4, adds an explicit context-lifecycle boundary, and rejects live-row dependence, context substitution, and delete-time mutation.

## 7. What this proposal does not decide

D3 does not decide:

- whether physical deletion is permitted for any particular subject type;
- whether deletion/deactivation of any particular context is permitted;
- retention periods or legal/compliance erasure obligations;
- `RESTRICT`, `CASCADE`, `SET NULL`, or other FK action;
- whether referential integrity is DB-enforced, application-enforced, mixed, or absent;
- tombstones;
- historical identity registry;
- archival tables;
- payload snapshots;
- whether names or other descriptive attributes must be preserved;
- anonymization/privacy policy;
- D4 database-enforced referential integrity;
- D5 subject-type extensibility;
- N1–N5 selection or rejection;
- GC-002 Alternative B;
- persistence shape;
- migration;
- runtime resolver/API;
- WP19 implementation.

## 8. D3 decision status

**PROPOSED — NOT YET ACCEPTED.**

**Authority: NOT YET ESTABLISHED.**

The preferred proposal becomes D3 authority only after explicit Project Owner acceptance and separate authority recording.

## 9. Gate result

**D3 OPTIONS STRUCTURED AND EVALUATED — AUDITED-SUBJECT DELETION, CONTEXT LIFECYCLE, HISTORICAL RESOLUTION, REFERENTIAL INTEGRITY, RETENTION/COMPLIANCE, AND PHYSICAL REPRESENTATION KEPT DISTINCT — REPRESENTATION-NEUTRAL RULE PROPOSED — D3 REMAINS OPEN / NOT YET ACCEPTED.**

Current Q2 state:

- D1: **CLOSED — ACCEPTED**;
- D2: **CLOSED — ACCEPTED**;
- D3: **OPEN — PROPOSED / NOT YET ACCEPTED**;
- D4–D5: **OPEN**;
- Q2 persisted representation: **OPEN**;
- N1–N5: **UNAPPROVED**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit interim-shape authorization**.

The next bounded step is explicit Project Owner review/acceptance of the D3 proposal. No implementation authorization is created by this artifact.