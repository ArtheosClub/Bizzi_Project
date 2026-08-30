# WP19 / Q2 D3 Subject-Deletion / Historical-Resolution Options v0.1

**Status:** Historical D3 decision analysis — D3 subsequently ACCEPTED  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 / D3 — audited-subject deletion, deactivation, and historical resolution  
**Decision owner:** Project Owner through ADW-07  
**Authority:** Historical planning only. Canonical D3 authority is `00_ARCHITECTURE/07_AUDIT/ADW07_D3_SUBJECT_DELETION_DECISION.md`.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

> **Planning synchronization note:** This artifact was authored before D3–D5 and Q2-RI were accepted. Its option analysis is retained as historical input. Historical references to the DB-referential-integrity surface formerly labeled `D4` are synchronized to the current identifier `Q2-RI`. This direct planning correction does not modify any accepted authority record.

## 1. D3 bounded question

**What must remain durably resolvable from a committed AuditRecord if its audited subject is later deleted or deactivated, and what does D3 imply — or not imply — about deletion/deactivation of related context?**

D3 separated:

1. audited-subject deletion;
2. audited-subject deactivation;
3. context deletion/deactivation;
4. historical AuditRecord resolvability;
5. referential integrity — whether/how database or application constraints maintain references; this is separate from D3 and is now governed for comparative weight by accepted Q2-RI;
6. retention and legal/compliance policy;
7. physical representation.

D3 must not collapse historical resolvability into continued live-row, active-subject, or live-context existence.

## 2. Authority carried into D3 at the time

D1 was CLOSED — ACCEPTED: a durable subject reference includes an explicit durable subject-type discriminator identifying exactly one current Q2 subject type.

D2 was CLOSED — ACCEPTED: `Workspace` is a first-class subject type; workspace context associated with another subject does not substitute for that subject identity.

D10 requires committed Historical Records, including AuditRecords, to preserve historical truth and remain immutable/durable. ADR-0014 requires a committed AuditRecord to durably identify the subject of the audited mutation.

These authorities required stable historical meaning but did not establish that every audited subject row or related context must exist or remain active forever.

## 3. Option results retained

- **D3-O1 — Live/active-subject-dependent resolution:** FAIL.
- **D3-O2 — Historical identity survives subject deletion/deactivation; live dereference is not required:** PASS.
- **D3-O3 — AuditRecord universally prevents audited-subject deletion or deactivation:** FAIL as a D3-wide requirement.
- **D3-O4 — Historical identity survives lifecycle change; deletion/integrity constraints remain separate:** PASS.
- **D3-O5 — Lifecycle-time mutation of the committed AuditRecord reference:** FAIL.
- **D3-O6 — Context loss changes or replaces subject identity:** FAIL.

The accepted D3 authority was subsequently recorded separately and controls over this planning analysis.

## 4. Cross-cutting boundaries retained

### Durable audit history

Subject deletion, subject deactivation, or context deletion/deactivation must not by themselves destroy or rewrite committed AuditRecord history.

### Referential integrity and cascade behavior

D3 did not select referential-integrity behavior and did not authorize implicit cascade deletion of AuditRecords. At the time this was the open surface historically labeled `D4`; its current identifier is **Q2-RI**. Accepted Q2-RI makes DB-enforced RI a per-realization comparative preference, not a Q2 requirement, and still does not define FK delete/cascade/restrict/set-null behavior.

### Retention / legal / compliance

D3 does not establish retention periods, legal holds, erasure/anonymization policy, regulatory exceptions, or compliance-specific deletion requirements.

### Physical representation

D3 does not select FK, composite FK, payload, opaque identifier, registry, tombstone, archival table, snapshot, or other persistence shape.

### D5 and GC-002 boundary

D3 did not decide D5 future subject-type extensibility. D5 was subsequently accepted through separate authority. GC-002 Alternative B remains PROPOSED ONLY.

## 5. Accepted D3 formulation — historical planning copy only

The planning proposal that was subsequently accepted was:

> **A committed AuditRecord MUST preserve enough durable subject-reference information to identify its historical audited subject after later deletion or deactivation of that subject. Historical resolvability does not require the subject, or any associated context, to remain dereferenceable as a currently live or active entity. Deletion or deactivation of associated context MUST NOT substitute, reinterpret, or rewrite the committed audited-subject identity. Subject deletion, subject deactivation, and context deletion/deactivation do not by themselves authorize deletion or mutation of the committed AuditRecord. D3 does not require the AuditRecord reference itself either to prevent or to permit subject or context lifecycle changes; referential-integrity behavior, retention/legal/compliance policy, and physical representation remain separate decisions.**

This quotation is retained for historical planning traceability only. The canonical accepted text is solely in `ADW07_D3_SUBJECT_DELETION_DECISION.md`.

## 6. Current state

- D1–D5: **CLOSED — ACCEPTED**;
- Q2-RI: **CLOSED — ACCEPTED — O2 PREFERENCE**;
- Q2-ST: **OPEN**;
- Q2 persisted representation: **OPEN / NOT ESTABLISHED**;
- N1–N5: **UNAPPROVED**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED**.
