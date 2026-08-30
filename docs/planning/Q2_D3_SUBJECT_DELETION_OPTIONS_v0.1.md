# WP19 / Q2 D3 Subject-Deletion / Historical-Resolution Options v0.1

**Status:** Draft — D3 decision analysis only  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 / D3 — audited-subject deletion and historical resolution  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact structures and evaluates D3 options; it does not decide D3.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit authorization of an interim shape.

## 1. D3 bounded question

**What must remain durably resolvable from a committed AuditRecord if its audited subject is later physically deleted, and may the AuditRecord subject reference itself constrain that deletion?**

D3 separates two independent semantic questions:

1. **Historical resolution:** what subject identity information must remain interpretable after the live subject row/entity no longer exists?
2. **Deletion constraint:** must, may, or must not the AuditRecord reference prevent physical deletion of the live subject?

D3 must not collapse historical resolvability into live-row existence.

## 2. Authority carried into D3

D1 is **CLOSED — ACCEPTED**: a durable subject reference includes an explicit durable subject-type discriminator identifying exactly one current Q2 subject type.

D2 is **CLOSED — ACCEPTED**: `Workspace` is a first-class subject type; workspace context associated with another subject does not substitute for that subject identity.

D10 requires committed Historical Records, including AuditRecords, to preserve historical truth and remain immutable/durable. Correction of committed historical meaning is therefore by a new historical record rather than mutation of the committed record.

ADR-0014 requires a committed AuditRecord to durably identify the subject of the audited mutation.

These authorities require stable historical meaning but do **not** establish that every audited subject row must exist forever.

## 3. D3 evaluation criteria

A D3 rule is sufficient only if:

- deletion of the live subject cannot make the committed AuditRecord cease to identify which historical subject was audited;
- the committed subject reference does not silently acquire a different meaning after deletion;
- D1 type identity remains interpretable after deletion;
- D2 `Workspace` semantics remain intact;
- the rule does not silently choose persistence shape or D4 enforcement mechanism;
- the rule distinguishes historical identity from the ability to dereference a currently live entity.

Results use `PASS`, `FAIL`, or `CONDITIONAL`.

## 4. D3 options

### D3-O1 — Live-row-dependent resolution

**Rule:** a committed AuditRecord subject reference is considered historically resolvable only while the referenced live subject row/entity continues to exist.

**Result: FAIL.**

Physical deletion could destroy the ability to determine which subject was historically audited. That conflicts with ADR-0014 durable subject identification and the historical-stability requirement carried by A2/D10.

This does not mean deletion itself is prohibited; it means historical identity cannot depend solely on continued live-row existence.

### D3-O2 — Historical identity survives deletion; live dereference is not required

**Rule:** after physical deletion of the audited subject, the committed AuditRecord MUST retain enough durable information to continue identifying the historical subject according to the accepted D1/D2 semantics. The subject need not remain dereferenceable as a currently live entity.

**Result: PASS.**

This preserves historical identity while keeping live-entity lifecycle distinct from Historical Record meaning. It does not prescribe whether the durable information is relational, payload-based, opaque, registry-backed, or otherwise represented.

### D3-O3 — AuditRecord universally prevents subject deletion

**Rule:** any subject referenced by an AuditRecord must remain physically present for as long as the AuditRecord exists; the reference therefore prevents physical deletion.

**Result: FAIL as a D3-wide requirement.**

This is stronger than the established historical requirement. Existing authority requires preservation of historical truth, not permanent retention of every live subject row. It would also risk importing a particular referential-integrity/delete policy that belongs to D4 or subject lifecycle authority.

A particular subject type may independently have stronger retention/deletion rules; D3 does not override them.

### D3-O4 — Historical identity survives deletion, while deletion constraint is representation/lifecycle dependent

**Rule:** the durable AuditRecord MUST preserve historical subject identity after physical deletion, but D3 does not require the AuditRecord reference itself either to prevent or to permit deletion. Whether a concrete representation constrains deletion is decided separately by applicable subject lifecycle authority and D4/persistence decisions.

**Result: PASS.**

This retains the historical invariant without silently choosing `RESTRICT`, `CASCADE`, `SET NULL`, tombstones, permanent rows, registry infrastructure, or application-only enforcement.

### D3-O5 — Delete-time mutation of the committed AuditRecord reference

**Rule:** when the subject is deleted, the existing committed AuditRecord reference may be rewritten into a replacement historical form.

**Result: FAIL.**

This would mutate committed historical meaning and conflicts with the immutability/stability requirement. Any corrective or supplementary historical fact must be represented without rewriting the committed AuditRecord.

## 5. Boundary cases

### 5.1 `Workspace`

Deletion or lifecycle treatment of a Workspace is not decided here. If physical deletion is permitted by its governing lifecycle authority, an existing AuditRecord with discriminator `Workspace` must still identify that historical Workspace subject after deletion.

### 5.2 `WorkspaceMembership`

The membership is the audited subject when the discriminator is `WorkspaceMembership`. Deletion of the membership must not collapse its historical identity into either the User or Workspace that participated in the membership.

### 5.3 `EnterpriseObject`

If an EnterpriseObject is physically deleted, the AuditRecord must retain the historical identity of that EnterpriseObject. D3 does not require a base `enterprise_objects` row, tombstone, or standalone-specialization row to survive unless separate authority requires it.

### 5.4 `User`

D3 does not establish whether User deletion is legally or architecturally permitted. If it is permitted, AuditRecord historical subject identity must remain stable. Privacy/anonymization requirements, if any, are outside this D3 decision unless separately introduced by authority.

### 5.5 `Task`

Task lifecycle/deletion policy is not selected here. Physical deletion, if allowed, cannot make a committed AuditRecord cease to identify the historical Task subject.

## 6. Preferred D3 proposal

The narrowest representation-neutral rule satisfying the existing authority is:

> **A committed AuditRecord MUST preserve enough durable subject-reference information to identify its historical audited subject even if that subject is later physically deleted. Historical resolvability does not require the subject to remain dereferenceable as a currently live entity. D3 does not require the AuditRecord reference itself either to prevent or to permit subject deletion; deletion constraints remain governed by applicable subject lifecycle authority and later persistence/integrity decisions. The committed AuditRecord subject reference MUST NOT be rewritten merely because the subject is deleted.**

This combines the valid parts of O2 and O4 and rejects live-row dependence and delete-time mutation.

## 7. What this proposal does not decide

D3 does not decide:

- whether physical deletion is permitted for any particular subject type;
- retention periods;
- `RESTRICT`, `CASCADE`, `SET NULL`, or other FK action;
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

**D3 OPTIONS STRUCTURED AND EVALUATED — REPRESENTATION-NEUTRAL HISTORICAL-IDENTITY RULE PROPOSED — D3 REMAINS OPEN / NOT YET ACCEPTED.**

Current Q2 state:

- D1: **CLOSED — ACCEPTED**;
- D2: **CLOSED — ACCEPTED**;
- D3: **OPEN — PROPOSED / NOT YET ACCEPTED**;
- D4–D5: **OPEN**;
- Q2 persisted representation: **OPEN**;
- N1–N5: **UNAPPROVED**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit interim-shape authorization**.

The next bounded step is Project Owner review of the D3 proposal. No implementation authorization is created by this artifact.