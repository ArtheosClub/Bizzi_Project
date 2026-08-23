# Q2 Evaluation Framework Candidate v0.1

**Status:** Draft
**Artifact type:** Research candidate — non-authoritative reference material
**Date:** 2026-08-23
**Subject:** ADR-0014 Q2 — persisted `AuditRecord` subject-reference representation
**Decision owner:** Project Owner through ADW-07
**Authority:** None. This artifact records research and a candidate decision procedure only.
**Implementation effect:** None. WP19 remains blocked and unauthorized for implementation.

> **Standing warning:** This document is not an ADR, ADW decision block, architecture decision, planning authority, or implementation authorization. It must not be cited as authority for a Q2 representation or for any D1–D6 decision below. It is filed under `docs/planning/`, `DECISION_0002`'s Tier 4 (`docs/planning/` + `50_IMPLEMENTATION/`: sequencing and MVP scope). Tier 4 standing applies to the directory, not to this document's content — this artifact is not a planning decision or amendment, and its own non-authoritative status rests on this declaration, not on its location. `06_REFERENCE/` was considered and rejected: `DECISION_0002`'s Tier 0–6 hierarchy does not mention that directory at all, so its absence from the table was never an exclusionary ranking to rely on, and its current contents (RKM-01/RSM-01, both Draft) are a different genre of document — proposed repository-reorganization models, not research/decision-support material.

---

## 1. Executive framework

ADR-0014 closes Q1: a persisted `AuditRecord` must durably identify the subject of the audited mutation. The decision is shape-neutral. No dedicated column, foreign key, composite key, payload representation, reference table, or other persisted shape is approved by default.

ADW-07 Block 3 discharges ADR-0014's routing obligation under branch (a) and establishes ADW-07 as the substantive owner of Q2. It does not decide Q2's persisted representation and does not create the evaluative framework required to decide it.

Current state:

```text
Q1 CLOSED
→ routing obligation DISCHARGED
→ ADW-07 ownership of Q2 ESTABLISHED
→ Q2 persisted representation OPEN — NOT ESTABLISHED
→ evaluative framework not yet approved
→ WP19 BLOCKED / implementation unauthorized
```

```text
Routing resolved != Q2 resolved != WP19 implementation authorized
```

This artifact proposes the following candidate procedure:

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

The procedure itself is not yet normative. Project Owner approval is required before it is used as the required Q2 decision method.

---

## 2. Authoritative constraints

### A1 — Durable subject resolvability

**Established — ADR-0014.** A persisted `AuditRecord` must durably resolve to the subject of the audited mutation. The representation mechanism remains unspecified.

Diagnostic questions when applying A1:

- Does the persisted record identify the concrete subject instance?
- Can the subject type be determined directly or through an explicitly defined durable convention?
- Does resolution survive independently of request state, logs, session memory, transient actor context, or other non-durable information?

Type disambiguation is a strong derived concern inside A1, not an independently established hard gate.

### A2 — Committed reference meaning must not silently change

**Established core — D10 historical-record semantics and ADR-0014 reversibility reasoning.** Once committed, the AuditRecord's persisted meaning must not silently repoint to a different subject. Correction requires a new historical record rather than mutation of the committed record.

Diagnostic question:

- Can the same committed AuditRecord later resolve to a different subject without a new historical record? If yes, the candidate conflicts with A2.

A2 does not itself establish that the referenced subject must remain physically present forever.

### A3 — Subject identity is distinct from actor attribution

**Established — ADR-0014.** `What was acted on` and `who acted` are separate questions. Actor attribution cannot substitute for subject identification.

### A4 — Do not assume Event/AuditRecord identity

**Established non-identity; complete relationship still open — ADW-07 Blocks 1–2, R1.** A Q2 representation must not depend on an assumption that Event and AuditRecord share identity or infrastructure. If a candidate requires one particular R1 answer, classify the dependency as `UNDETERMINED — R1 DECISION REQUIRED`.

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
- **S8 New subject type** — what changes if a sixth auditable subject type is introduced?
- **S9 R1 unresolved** — does the candidate require a particular Event/AuditRecord relationship that ADW-07 has not decided?
- **S10 Cross-workspace ambiguity** — can subjects from different architectural scopes become indistinguishable under the persisted reference contract?

---

## 6. Comparative criteria

Comparison follows authority checking. Comparative dimensions cannot override A1–A6.

No weights or numeric score are proposed in v0.1.

- **C1 Queryability / audit retrieval** — how naturally can audit history be retrieved for a known subject? ADR-0005 supports queryability as a legitimate concern but does not mandate a particular mechanism.
- **C2 Integrity characteristics** — what correctness properties can be enforced, and where? Keep this neutral between DB constraints, application/domain validation, durable identifier conventions, and other mechanisms. A DB foreign key receives no automatic preference.
- **C3 Extensibility** — what schema, interpretation, migration, or discriminator changes are required to add another subject type?
- **C4a Write/storage cost** — persisted fields, indexes, storage growth, write complexity.
- **C4b Read/query cost** — joins, predicates, payload parsing, indexability, cross-type querying.
- **C4c Migration cost** — initial migration, future migration burden, historical-data transformation.
- **C5 Evolution/reversibility cost** — can old and new representation versions coexist, and can the representation later change without rewriting committed historical records?

---

## 7. Explicit open decision surfaces

These are questions exposed by the research. This artifact does **not** decide them.

- **D1 — Type disambiguation:** must subject type be structurally encoded, or may another durable convention resolve it?
- **D2 — Reference-level workspace semantics:** how should workspace integrity apply across structurally asymmetric subject types?
- **D3 — Subject deletion:** does an AuditRecord reference itself block physical deletion of its subject? Current authority does not clearly establish this.
- **D4 — DB-enforced referential integrity:** requirement, preference, or neither? Not established.
- **D5 — Subject-type set:** fixed to WP19's five current types or designed for extension? Not established.
- **D6 — Procedure approval:** should ADW-07 use the proposed constraint-check → stress-test → comparison procedure? Candidate only; Project Owner approval required before normative use.

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

Before the framework becomes normative, ask:

> If two future candidates both satisfy all authoritative constraints, do the stress tests and comparative criteria provide enough information to explain a rational choice between them?

If not, the response is:

**FRAMEWORK INSUFFICIENT — ADD DECISION DIMENSION**

not an arbitrary candidate selection.

---

## 10. What this artifact deliberately does not decide

This artifact does not:

- select, recommend, rank, reject, or enumerate candidate representations;
- resolve Event/AuditRecord R1;
- decide D1–D6;
- decide whether AuditRecord references block subject deletion;
- create a uniform workspace-reference rule;
- approve or change GC-002, GC-006, or GC-007;
- authorize WP19;
- alter WP18;
- create an ADW-07 Block 4;
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

That Tier 4 standing belongs to the directory, not automatically to any document filed in it. `docs/planning/DEFERRED_ARCHITECTURE_INITIATIVES.md` already establishes the pattern this artifact follows: a Tier-4 location can and does hold proposed, not-yet-decided material, provided the document's own header states its status plainly. This file does the same — it holds research and a candidate procedure, not a planning decision, and its non-authoritative status rests on the declaration at the top of this document, not on an inference from where it sits.

`06_REFERENCE/` was considered and rejected as a placement. `DECISION_0002`'s Tier 0–6 hierarchy does not mention that directory at all — its absence from the table means the question of its rank was never addressed, not that it was assigned a non-authoritative rank by omission. Its only current occupants, RKM-01 and RSM-01 (both Draft), are a different genre of document — proposed repository-reorganization models, not decision-support research — so filing unrelated material there would establish a new pattern by fiat rather than follow an existing one.

No new authority tier or document-status vocabulary is created here. Under ADR-0008, the document status is `Draft`: authored, not in force, and still materially changeable.

---

## 13. Next review step

Before candidate representations are enumerated:

1. review A1–A6 for completeness and citation precision;
2. confirm that candidate checking is a procedure against A1–A6, not a duplicate gate layer;
3. review S1–S10 and C1–C5 for representation neutrality;
4. decide whether the proposed procedure itself should receive Project Owner approval for normative use;
5. leave D1–D6 unresolved unless and until a separate explicit decision addresses them.

Until then:

**RESEARCH CANDIDATE ONLY — Q2 REMAINS OPEN — WP19 REMAINS BLOCKED.**
