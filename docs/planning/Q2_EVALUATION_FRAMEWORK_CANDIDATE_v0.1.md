# Q2 Evaluation Framework Candidate v0.1

**Status:** Active — evaluation procedure approved for normative use  
**Artifact type:** Approved evaluation procedure; not Q2 representation authority  
**Date:** 2026-08-23  
**Procedure approval:** 2026-08-28 — ADW-07 Block 4  
**Subject:** ADR-0014 Q2 — persisted `AuditRecord` subject-reference representation  
**Decision owner:** Project Owner through ADW-07  
**Authority:** Procedure authority conferred by `00_ARCHITECTURE/07_AUDIT/ADW07_BLOCK4_Q2_EVALUATION_PROCEDURE_APPROVAL.md`. This artifact defines the approved evaluation method; it does not itself select a Q2 representation or replace the separate authority artifacts that decide individual decision surfaces.  
**Implementation effect:** None. WP19 remains blocked and unauthorized for implementation pending explicit Q2 persisted-representation resolution or separate explicit bounded interim-shape authorization.

> **Authority boundary:** This document was originally authored as a research candidate and subsequently approved by ADW-07 Block 4 for normative procedural use. Its procedure is therefore active. Representation outcomes and later decisions are not created by this document merely because the procedure is active. D1–D5 are governed by their separate canonical ADW-07 authority artifacts. Q2 persisted representation remains unresolved.

---

## 1. Executive framework

ADR-0014 closes Q1: a persisted `AuditRecord` must durably identify the subject of the audited mutation. The decision is shape-neutral. No dedicated column, foreign key, composite key, payload representation, reference table, or other persisted shape is approved by default.

ADW-07 Block 3 discharges ADR-0014's routing obligation under branch (a) and establishes ADW-07 as the substantive owner of Q2. ADW-07 Block 4 subsequently approved the evaluation procedure in this artifact for normative use. D1–D5 were then decided through separate canonical ADW-07 authority artifacts. None of those decisions selects the final persisted representation.

Current state:

```text
Q1 CLOSED
→ routing obligation DISCHARGED
→ ADW-07 ownership of Q2 ESTABLISHED
→ evaluation procedure ACTIVE / APPROVED FOR NORMATIVE USE
→ D1–D5 CLOSED / ACCEPTED through separate authority artifacts
→ Q2-RI OPEN — DB-enforced referential-integrity weight not established
→ Q2 persisted representation OPEN — NOT ESTABLISHED
→ WP19 BLOCKED / implementation unauthorized
```

```text
Procedure approved != decision surfaces resolved != Q2 representation resolved != WP19 implementation authorized
```

The approved procedure is:

```text
AUTHORITATIVE CONSTRAINTS
        ↓
CHECK EACH CANDIDATE AGAINST THOSE CONSTRAINTS
  PASS / FAIL / UNDETERMINED — DECISION REQUIRED
        ↓
SEMANTIC STRESS TESTS
        ↓
COMPARATIVE EVALUATION
        ↓
EXPOSED DECISION GAPS
        ↓
PROJECT OWNER DECISIONS WHERE NECESSARY
        ↓
Q2 REPRESENTATION DECISION
        ↓
SEPARATE WP19 READINESS RE-EVALUATION
```

---

## 2. Authoritative constraints

### A1 — Durable subject resolvability

**Established — ADR-0014.** A persisted `AuditRecord` must durably resolve to the subject of the audited mutation. The representation mechanism remains unspecified.

Diagnostic questions when applying A1:

- Does the persisted record identify the concrete subject instance?
- Can the subject type be determined directly or through an explicitly defined durable convention?
- Does resolution survive independently of request state, logs, session memory, transient actor context, or other non-durable information?

Type disambiguation was a strong derived concern inside A1 when this framework was authored. It was later resolved separately by accepted D1 authority.

### A2 — Committed reference meaning must not silently change

**Established core — D10 historical-record semantics and ADR-0014 reversibility reasoning.** Once committed, the AuditRecord's persisted meaning must not silently repoint to a different subject. Because audit records are durable and immutable, silently changing the meaning of an already committed audit reference is not permitted. A correction should therefore be represented as a new historical record rather than by mutating the committed record; this is a derived consequence of the immutability rule, not a separately quoted D10 sentence.

Diagnostic question:

- Can the same committed AuditRecord later resolve to a different subject without a new historical record? If yes, the candidate conflicts with A2.

A2 does not itself establish that the referenced subject must remain physically present forever.

### A3 — Subject identity is distinct from actor attribution

**Established — ADR-0014.** `What was acted on` and `who acted` are separate questions. Actor attribution cannot substitute for subject identification.

### A4 — Do not assume Event/AuditRecord identity

**Established non-identity; complete relationship still open — ADW-07 Block 1.** Domain Event is not an AuditRecord, and their complete relationship remains open. A Q2 representation must not depend on an assumption that Event and AuditRecord share identity or infrastructure.

Separately, Block 2 Residual Question R1 remains open concerning Domain Event ↔ Durable Audit / Outbox / Publication-Intent identity. Do not treat R1 as synonymous with the Event/AuditRecord relationship. If a candidate depends on one particular R1 answer, classify that dependency as `UNDETERMINED — R1 DECISION REQUIRED`.

### A5 — Retention duration is excluded

**Established exclusion — D10 §9.** Retention duration is not an architectural Q2 representation-selection criterion.

### A6 — No representation has presumptive approval

**Established — ADR-0014.** In particular:

- GC-002 Alternative B remains Proposed only;
- payload-contained identification is neither presumed sufficient nor forbidden;
- DB-enforced referential integrity is not established as mandatory;
- ADW-08 is not assigned ownership of AuditRecord persistence.

---

## 3. Candidate-check procedure

The admissibility step is **not a second layer of requirements**. It is the procedure for checking a candidate against A1–A6.

For each applicable authoritative constraint, assign exactly one result:

### PASS

The candidate satisfies the authoritative constraint and every interpretation required for that conclusion is established.

### FAIL

The candidate contradicts established authority. Every FAIL must cite the authority violated.

### UNDETERMINED — DECISION REQUIRED

The candidate's status depends on an architectural question that has not yet been decided.

This is neither PASS nor FAIL. It is a forcing signal for an explicit decision.

No `PARTIAL PASS` status is proposed.

---

## 4. Structural facts the procedure must not hide

Current implementation evidence shows that the five Q2 subject types are structurally asymmetric:

- `Workspace` is itself the workspace boundary and has no parent `workspace_id`;
- `User` has no `workspace_id`;
- `EnterpriseObject`, `WorkspaceMembership`, and `Task` are workspace-scoped in their current persisted forms;
- IDs are independently generated UUIDs per table rather than one shared type-prefixed identity space.

These are **IMPLEMENTATION EVIDENCE — NOT ARCHITECTURE AUTHORITY**.

They matter because a framework must not silently assume that all five subjects share one workspace-key shape, lifecycle model, database identity mechanism, or `EnterpriseObject` identity.

---

## 5. Semantic stress tests

Stress tests expose hidden assumptions. They are not automatically hard gates and are not numeric scores.

Use `SUPPORTED`, `UNSUPPORTED`, `UNDETERMINED — DECISION REQUIRED`, or `NOT APPLICABLE`, with rationale.

- **S1 Workspace as subject** — can the representation identify the workspace without inventing a parent workspace?
- **S2 User as subject** — does it incorrectly assume every subject row carries `workspace_id`?
- **S3 WorkspaceMembership as subject** — does it preserve the distinction between mutation of the membership and mutation of the User?
- **S4 EnterpriseObject as subject** — does it work for the canonical enterprise-object case without implying all subjects must become EnterpriseObjects?
- **S5 Task as subject** — does it work for a conventional workspace-scoped work item?
- **S6 Subject deletion** — does historical subject identity remain meaningful if a subject may later be physically deleted? Does the candidate assume, without authority, that AuditRecord itself prevents deletion?
- **S7 Lifecycle change** — does reference meaning survive archival, supersession, or other lifecycle changes without rewriting the AuditRecord?
- **S8 New subject type** — what changes if a future auditable subject type is introduced under separate architecture authority?
- **S9 R1 unresolved** — if the candidate depends on a particular Domain Event ↔ Durable Audit / Outbox / Publication-Intent identity answer, does it require one R1 outcome that ADW-07 has not decided? R1 is not another name for the separate, still-open Event/AuditRecord relationship.
- **S10 Cross-workspace ambiguity** — can subjects from different architectural scopes become indistinguishable under the persisted reference contract?

---

## 6. Comparative criteria

Comparison follows authority checking. Comparative dimensions cannot override A1–A6.

No weights or numeric score are proposed in v0.1.

- **C1 Queryability / audit retrieval** — how naturally can audit history be retrieved for a known subject? ADR-0005 supports queryability as a legitimate concern but does not mandate a particular mechanism.
- **C2 Integrity characteristics** — what correctness properties can be enforced, and where? Keep this neutral between DB constraints, application/domain validation, durable identifier conventions, and other mechanisms. A DB foreign key receives no automatic preference unless separate authority establishes such a preference or requirement.
- **C3 Extensibility** — what schema, interpretation, migration, or discriminator changes are required to add another subject type? Under accepted D5, extensibility convenience is informative but is not by itself a ranking preference.
- **C4a Write/storage cost** — persisted fields, indexes, storage growth, write complexity.
- **C4b Read/query cost** — joins, predicates, payload parsing, indexability, cross-type querying.
- **C4c Migration cost** — initial migration, future migration burden, historical-data transformation.
- **C5 Evolution/reversibility cost** — can old and new representation versions coexist, and can the representation later change without rewriting committed historical records?

---

## 7. Decision surfaces and identifier reconciliation

The original research candidate exposed six decision surfaces labeled D1–D6. D1–D5 have since been decided through separate canonical ADW-07 authority artifacts, and D6 was approved by ADW-07 Block 4. This section preserves traceability while reconciling one identifier collision discovered after those decisions were recorded.

- **D1 — Type disambiguation:** CLOSED / ACCEPTED. Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D1_SUBJECT_TYPE_DISAMBIGUATION_DECISION.md`.
- **D2 — Workspace subject semantics:** CLOSED / ACCEPTED. Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D2_WORKSPACE_SUBJECT_SEMANTICS_DECISION.md`.
- **D3 — Subject deletion / historical identity:** CLOSED / ACCEPTED. Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D3_SUBJECT_DELETION_DECISION.md`.
- **D4 — Subject-reference semantics:** CLOSED / ACCEPTED. Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D4_SUBJECT_REFERENCE_SEMANTICS_DECISION.md`.
- **D5 — Current subject-type scope / extensibility:** CLOSED / ACCEPTED. Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D5_SUBJECT_TYPE_EXTENSIBILITY_DECISION.md`.
- **D6 — Procedure approval:** CLOSED / APPROVED by ADW-07 Block 4. Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_BLOCK4_Q2_EVALUATION_PROCEDURE_APPROVAL.md`.
- **Q2-RI — DB-enforced referential integrity:** OPEN. Is DB-enforced referential integrity a requirement, a preference, or neither for the Q2 persisted subject-reference representation? Not established.

**Identifier reconciliation note:** the original v0.1 research candidate labeled the DB-enforced referential-integrity surface as `D4`. The identifier `D4` was subsequently assigned to the accepted Subject Reference Semantics decision. The historical RI surface is therefore renamed **Q2-RI** for all current and future work. This is a namespace reconciliation only; it does not answer the RI question.

A separate subject-type ranging-rule gap has also been exposed after D1/D5 acceptance. It is not silently added to D1 or D5 and is handled as a separate bounded surface, **Q2-ST**, outside the historical D1–D6 numbering.

---

## 8. Representation-neutrality rule

Before admitting any criterion, ask:

> Does this criterion express a property the architecture needs, or does it silently encode a preferred implementation?

The following are **not** admitted merely by assumption:

- must have a foreign key;
- must use one column;
- must use a discriminator column;
- must be joinable without application code;
- must reuse EnterpriseObject identity;
- must live outside the payload;
- must live inside the payload.

---

## 9. Decision-sufficiency test

Before selecting a representation, ask:

> If two candidates both satisfy all authoritative constraints, do the stress tests, comparative criteria, and resolved decision surfaces provide enough information to explain a rational choice between them?

If not, the response is:

**FRAMEWORK INSUFFICIENT — ADD OR RESOLVE DECISION DIMENSION**

not an arbitrary candidate selection.

---

## 10. What this artifact deliberately does not decide

This artifact does not:

- select, recommend, rank, reject, or enumerate candidate representations;
- resolve the Event/AuditRecord relationship or Block 2 Residual Question R1 (Domain Event ↔ Durable Audit / Outbox / Publication-Intent identity);
- itself decide D1–D5; their authority lives in separate canonical files;
- decide Q2-RI;
- decide Q2-ST;
- create a uniform workspace-reference rule beyond accepted D2;
- approve or change GC-002, GC-006, or GC-007;
- authorize WP19;
- alter WP18;
- create an ADR;
- change backend or schema scope.

---

## 11. Candidate evaluation template

| Dimension | Result | Evidence / rationale | Decision dependency |
|---|---|---|---|
| A1 Durable subject resolvability | PASS / FAIL / UNDETERMINED | | |
| A2 Committed reference meaning | PASS / FAIL / UNDETERMINED | | |
| A3 Subject vs actor separation | PASS / FAIL / UNDETERMINED | | |
| A4 Event/AuditRecord assumption | PASS / FAIL / UNDETERMINED | | |
| A5 Retention exclusion | PASS / FAIL / UNDETERMINED | | |
| A6 No presumptive representation | PASS / FAIL / UNDETERMINED | | |
| S1–S10 | SUPPORTED / UNSUPPORTED / UNDETERMINED / N/A | | |
| C1 Queryability | qualitative | | |
| C2 Integrity characteristics | qualitative | | |
| C3 Extensibility | qualitative | | |
| C4a Write/storage cost | qualitative | | |
| C4b Read/query cost | qualitative | | |
| C4c Migration cost | qualitative | | |
| C5 Evolution/reversibility | qualitative | | |

Every architecture-based result must cite authority. Implementation-based results must be labeled `IMPLEMENTATION EVIDENCE — NOT ARCHITECTURE AUTHORITY`. Open decision dependencies must be named explicitly.

---

## 12. Governance basis for placement

`DECISION_0002` establishes the binding Tier 0–6 authority chain and explicitly assigns `docs/planning/` (together with `50_IMPLEMENTATION/`) to Tier 4: "Sequencing and MVP scope, deriving vocabulary from Tier 2 and technology assumptions from Tier 3" (`DECISION_0002` §1; mirrored in `ARCHITECTURE_SPECIFICATION.md` §3). This is an explicit ranking, not an absence.

The artifact was originally placed here as a research candidate. Its later procedural authority is conferred externally by ADW-07 Block 4; its directory placement does not by itself elevate representation recommendations or decisions. Canonical D1–D5 authority remains in `00_ARCHITECTURE/07_AUDIT/`.

No new authority tier is created by activating the approved procedure.

---

## 13. Current next steps

The evaluation procedure is already approved and D1–D5 are already accepted. Before a Project Owner Q2 persisted-representation decision:

1. resolve **Q2-RI** — DB-enforced referential-integrity weight (`requirement / preference / neither` or another explicitly approved formulation);
2. resolve **Q2-ST** — the architecture-level rule that determines the admissible AuditRecord subject-type discriminator vocabulary;
3. re-apply the resulting authority to N1–N5 without importing a physical-shape preference by implication;
4. only then prepare the separate Project Owner Q2 persisted-representation decision.

Until that separate representation decision:

**PROCEDURE ACTIVE — Q2 REPRESENTATION OPEN — WP19 REMAINS BLOCKED / UNAUTHORIZED.**
