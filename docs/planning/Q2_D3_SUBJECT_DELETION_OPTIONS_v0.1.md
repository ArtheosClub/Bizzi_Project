# WP19 / Q2 D3 Subject-Deletion / Historical-Resolution Options v0.1

**Status:** Draft — D3 decision analysis only  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 / D3 — audited-subject deletion, deactivation, and historical resolution  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact structures and evaluates D3 options; it does not decide D3.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit authorization of an interim shape.

## 1. D3 bounded question

**What must remain durably resolvable from a committed AuditRecord if its audited subject is later deleted or deactivated, and what does D3 imply — or not imply — about deletion/deactivation of related context?**

D3 separates the following surfaces and must not collapse them:

1. **Audited-subject deletion** — physical deletion/removal of the entity identified by the committed AuditRecord subject reference.
2. **Audited-subject deactivation** — the audited subject continues to exist historically or structurally but is disabled, closed, inactive, superseded, or otherwise no longer operationally active.
3. **Context deletion/deactivation** — deletion, deactivation, closure, supersession, or loss of availability of Workspace or other context associated with the audited subject or audit occurrence.
4. **Historical AuditRecord resolvability** — whether the committed AuditRecord still durably identifies the historical audited subject after later subject/context lifecycle changes.
5. **Referential integrity** — whether and how database/application constraints maintain references; this remains D4/persistence territory.
6. **Retention and legal/compliance policy** — retention duration, legal holds, erasure/anonymization obligations, regulatory exceptions, and compliance policy are not decided by D3.
7. **Physical representation** — FK, composite FK, payload, opaque identifier, registry, tombstone, archival row, or other implementation mechanism is not decided by D3.

D3 must not collapse historical resolvability into continued live-row, active-subject, or live-context existence.

## 2. Authority carried into D3

D1 is **CLOSED — ACCEPTED**: a durable subject reference includes an explicit durable subject-type discriminator identifying exactly one current Q2 subject type.

D2 is **CLOSED — ACCEPTED**: `Workspace` is a first-class subject type; workspace context associated with another subject does not substitute for that subject identity.

D10 requires committed Historical Records, including AuditRecords, to preserve historical truth and remain immutable/durable. Correction of committed historical meaning is therefore by a new historical record rather than mutation of the committed record.

ADR-0014 requires a committed AuditRecord to durably identify the subject of the audited mutation.

These authorities require stable historical meaning but do **not** establish that every audited subject row or related context must exist forever or remain active forever.

## 3. D3 evaluation criteria

A D3 rule is sufficient only if:

- deletion of the audited subject cannot make the committed AuditRecord cease to identify which historical subject was audited;
- deactivation of the audited subject cannot substitute, reinterpret, or rewrite its committed historical identity;
- deletion/deactivation of related context cannot silently substitute a different subject identity or rewrite the committed historical meaning;
- the committed subject reference does not silently acquire a different meaning after later lifecycle change;
- D1 type identity remains interpretable;
- D2 `Workspace` semantics remain intact;
- durable audit history is not implicitly destroyed by subject/context lifecycle operations;
- the rule does not silently choose persistence shape or D4 enforcement mechanism;
- the rule distinguishes historical identity from the ability to dereference a currently live or active entity/context;
- retention/legal/compliance questions remain separate.

Results use `PASS`, `FAIL`, or `CONDITIONAL`.

## 4. D3 options

### D3-O1 — Live/active-subject-dependent resolution

**Rule:** a committed AuditRecord subject reference is historically resolvable only while the referenced subject remains physically present and operationally active.

**Result: FAIL.**

Deletion could destroy historical identity, while deactivation could incorrectly make historical meaning depend on current operational status. Both conflict with durable subject identification and historical stability.

This does not mean deletion or deactivation itself is prohibited; it means historical identity cannot depend solely on continued live/active status.

### D3-O2 — Historical identity survives subject deletion/deactivation; live dereference is not required

**Rule:** after physical deletion or operational deactivation of the audited subject, the committed AuditRecord MUST retain enough durable information to continue identifying the historical audited subject according to accepted D1/D2 semantics. The subject need not remain dereferenceable as a currently live or active entity.

**Result: PASS.**

This preserves historical identity while keeping current lifecycle state distinct from Historical Record meaning. It does not prescribe whether the durable information is relational, payload-based, opaque, registry-backed, or otherwise represented.

### D3-O3 — AuditRecord universally prevents audited-subject deletion or deactivation

**Rule:** any subject referenced by an AuditRecord must remain physically present and active for as long as the AuditRecord exists.

**Result: FAIL as a D3-wide requirement.**

This is stronger than established authority. Historical preservation does not by itself require permanent retention or permanent operational activation of every audited subject. It would also import lifecycle and referential-integrity policy outside D3.

A particular subject type may independently have stronger lifecycle constraints; D3 does not override them.

### D3-O4 — Historical identity survives lifecycle change; deletion/integrity constraints remain separate

**Rule:** the durable AuditRecord MUST preserve historical audited-subject identity after deletion or deactivation, but D3 does not require the AuditRecord reference itself either to prevent or to permit those lifecycle changes. Whether a concrete representation constrains them is decided separately by applicable lifecycle authority and D4/persistence decisions.

**Result: PASS.**

This retains the historical invariant without silently choosing `RESTRICT`, `CASCADE`, `SET NULL`, tombstones, permanent rows, registry infrastructure, or application-only enforcement.

### D3-O5 — Lifecycle-time mutation of the committed AuditRecord reference

**Rule:** when the audited subject is deleted or deactivated, the existing committed AuditRecord reference may be rewritten into a replacement historical form.

**Result: FAIL.**

This would mutate committed historical meaning. A later lifecycle change must not rewrite the identity captured by the committed AuditRecord.

### D3-O6 — Context loss changes or replaces subject identity

**Rule:** deletion/deactivation of a Workspace or other associated context may cause the committed AuditRecord subject reference to be reinterpreted as that context, or may invalidate the prior subject identity.

**Result: FAIL.**

This violates D2 by conflating audited-subject identity with context and makes committed historical meaning contingent on later context lifecycle changes.

Context availability may affect live resolution or operational access, but it must not silently replace the committed audited-subject identity.

## 5. Boundary cases by current Q2 subject type

### 5.1 `Workspace`

When the discriminator is `Workspace`, the Workspace itself is the audited subject under D2.

- **Deletion:** if physical deletion is permitted by separate lifecycle authority, the committed AuditRecord must still identify that historical Workspace.
- **Deactivation/closure:** if the Workspace remains present but inactive/closed/superseded, its historical AuditRecord subject identity remains the same and must not be rewritten because of that status change.
- **Context distinction:** when Workspace is the audited subject, it is not merely context.

D3 does not decide whether Workspace deletion or deactivation is permitted.

### 5.2 `EnterpriseObject`

When the discriminator is `EnterpriseObject`, the EnterpriseObject remains the audited subject.

- **Deletion:** if physically deleted, the committed AuditRecord must continue to identify the historical EnterpriseObject.
- **Deactivation/supersession/lifecycle change:** later inactive, superseded, or terminal state does not rewrite the committed subject identity.
- **Context deletion/deactivation:** loss or deactivation of associated Workspace context does not convert the subject to `Workspace` and does not rewrite EnterpriseObject identity.

D3 does not require a base `enterprise_objects` row, tombstone, specialization row, registry, or other persistence mechanism to survive unless separate authority requires it.

### 5.3 `User`

When the discriminator is `User`, the User remains the audited subject.

- **Deletion:** D3 does not decide whether User deletion is legally or architecturally permitted; if permitted, the committed AuditRecord must preserve historical User subject identity to the extent permitted by applicable legal/compliance authority.
- **Deactivation:** suspension, disablement, account closure, or other inactive status does not rewrite the historical audited-subject identity.
- **Context deletion/deactivation:** loss of Workspace context associated with the audit occurrence does not turn the User subject into a Workspace subject.

Privacy, anonymization, erasure, and legal exceptions remain outside D3 and may impose separate constraints.

### 5.4 `WorkspaceMembership`

When the discriminator is `WorkspaceMembership`, the membership itself is the audited subject.

- **Deletion:** deletion of the membership must not collapse its historical identity into either the User or Workspace participating in it.
- **Deactivation/termination:** revocation, termination, expiration, or inactive status does not rewrite the committed membership subject identity.
- **Context deletion/deactivation:** later deletion/deactivation of related User or Workspace does not silently substitute either entity for the committed membership subject identity.

D3 does not decide membership lifecycle mechanics or retention policy.

### 5.5 `Task`

When the discriminator is `Task`, the Task remains the audited subject.

- **Deletion:** if physical deletion is permitted, the committed AuditRecord must continue to identify the historical Task.
- **Deactivation/terminal lifecycle:** completion, cancellation, archival, inactive status, or another terminal state does not rewrite the committed Task subject identity.
- **Context deletion/deactivation:** loss/deactivation of associated Workspace or other context does not substitute that context for Task identity.

D3 does not select Task lifecycle/deletion policy.

## 6. Cross-cutting boundaries

### 6.1 Durable audit history

Subject deletion, subject deactivation, or context deletion/deactivation must not by themselves destroy or rewrite committed AuditRecord history.

D3 therefore must not be read as authorizing deletion of AuditRecords merely because a referenced subject or context changes lifecycle state.

### 6.2 Referential integrity and cascade behavior

D3 does **not** select referential-integrity behavior. In particular, D3 does not authorize implicit cascade deletion of AuditRecords when subjects or contexts are deleted.

A proposal to cascade-delete AuditRecords could destroy immutable audit history and would require separate explicit architecture authority; it is not established by D3.

This boundary does not itself decide D4 and does not select any FK action or enforcement layer.

### 6.3 Retention / legal / compliance

D3 preserves architectural historical-identity semantics. It does not establish retention periods, legal holds, erasure/anonymization policy, regulatory exceptions, or compliance-specific deletion requirements.

Where legal/compliance authority requires different treatment, that authority must be addressed explicitly rather than inferred from D3.

### 6.4 Physical representation

D3 does not select FK, composite FK, payload, opaque identifier, registry, tombstone, archival table, snapshot, or other persistence shape.

Historical resolvability is an architecture requirement; its concrete representation remains part of the later Q2 persistence decision.

### 6.5 D4, D5, and GC-002 boundary

D3 does not decide D4 database/application referential-integrity policy and does not decide D5 future subject-type extensibility.

GC-002 Alternative B remains **PROPOSED ONLY**. Nothing in D3 approves, upgrades, incorporates, or gives normative authority to GC-002 Alternative B.

## 7. Preferred D3 proposal

The narrowest representation-neutral rule satisfying existing authority is:

> **A committed AuditRecord MUST preserve enough durable subject-reference information to identify its historical audited subject after later deletion or deactivation of that subject. Historical resolvability does not require the subject, or any associated context, to remain dereferenceable as a currently live or active entity. Deletion or deactivation of associated context MUST NOT substitute, reinterpret, or rewrite the committed audited-subject identity. Subject deletion, subject deactivation, and context deletion/deactivation do not by themselves authorize deletion or mutation of the committed AuditRecord. D3 does not require the AuditRecord reference itself either to prevent or to permit subject or context lifecycle changes; referential-integrity behavior, retention/legal/compliance policy, and physical representation remain separate decisions.**

This proposal preserves durable historical identity while keeping lifecycle policy, referential integrity, legal/compliance retention, and persistence shape outside D3.

## 8. What this proposal does not decide

D3 does not decide:

- whether physical deletion is permitted for any particular subject type;
- whether deactivation/closure/termination is permitted or required for any particular subject type;
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
- GC-002 Alternative B approval;
- persistence shape;
- migration;
- runtime resolver/API;
- WP19 implementation.

## 9. D3 decision status

**PROPOSED — NOT YET ACCEPTED.**

**Authority: NOT YET ESTABLISHED.**

The preferred proposal becomes D3 authority only after explicit Project Owner acceptance and separate authority recording.

## 10. Gate result

**D3 OPTIONS STRUCTURED AND EVALUATED — ALL FIVE CURRENT Q2 SUBJECT TYPES COVERED — SUBJECT DELETION, SUBJECT DEACTIVATION, CONTEXT LIFECYCLE, HISTORICAL RESOLUTION, REFERENTIAL INTEGRITY, RETENTION/COMPLIANCE, AND PHYSICAL REPRESENTATION KEPT DISTINCT — NO CASCADE AUTHORIZATION — GC-002 ALTERNATIVE B REMAINS PROPOSED ONLY — D3 REMAINS OPEN / NOT YET ACCEPTED.**

Current Q2 state:

- D1: **CLOSED — ACCEPTED**;
- D2: **CLOSED — ACCEPTED**;
- D3: **OPEN — PROPOSED / NOT YET ACCEPTED**;
- D4–D5: **OPEN**;
- Q2 persisted representation: **OPEN**;
- N1–N5: **UNAPPROVED**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit interim-shape authorization**.

The next bounded step is explicit Project Owner acceptance of the D3 proposal and, only after that acceptance, separate recording in `ADW07_D3_SUBJECT_DELETION_DECISION.md`. No implementation authorization is created by this artifact.