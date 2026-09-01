# WP19 / Q2 Candidate Normalization v0.1

**Status:** Draft — Q2 application analysis only
**Date:** 2026-08-30
**Subject:** ADR-0014 Q2 — normalization of the approved candidate universe before A1–A6 evaluation
**Decision owner:** Project Owner through ADW-07
**Authority:** None. This artifact does not select, rank, approve, or reject a persisted representation.
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED for implementation.

## 1. Purpose and boundary

ADW-07 Block 4 / D6 approves the Q2 evaluation procedure for normative use. This artifact performs the bounded normalization step required before applying that procedure to candidate representations.

The candidate universe is fixed from ADR-0014. No sixth candidate is introduced here:

1. polymorphic-reference;
2. composite-FK;
3. per-type-nullable-column;
4. opaque-identifier;
5. in-payload.

Normalization means only: state the minimum property that must be true for the already-named candidate class to be meaningfully evaluated. It does not choose concrete column names, SQL types, FK layouts, discriminator vocabulary, payload schema, indexes, ORM mappings, migration strategy, service API, subject-cardinality rule, or future subject-type policy.

Every statement below is labeled as one of:

- **CORPUS-DOCUMENTED** — the repository gives more than the candidate name and describes a relevant representation property;
- **CORPUS-NAMED / UNDERSPECIFIED** — ADR-0014 names the candidate class, but the repository does not define enough persisted structure to treat one engineering realization as canonical;
- **EVALUATION ASSUMPTION — NOT ARCHITECTURE AUTHORITY** — a minimum semantic condition used only to make the candidate class testable without pretending that a concrete engineering design has been approved;
- **DECISION DEPENDENCY — OPEN** — a question already exposed by the approved framework that must remain explicit rather than entering evaluation as an unstated premise.

No evaluation assumption or decision dependency becomes architecture authority through this document.

## 2. Corpus provenance matrix

| Candidate | Corpus status | Repository basis | Normalization consequence |
|---|---|---|---|
| Polymorphic reference | CORPUS-NAMED / UNDERSPECIFIED | ADR-0014 names `polymorphic-reference` among open candidates and prefers none. No repository contract defining `subject_type + subject_id`, `target_type + target_id`, or an equivalent canonical pair was found in the candidate provenance pass. | Evaluate only the class-level ability to durably resolve a concrete subject across more than one subject type. Whether subject type must be structurally encoded or may be resolved by another durable convention is D1 and is not normalized here. |
| Composite FK | CORPUS-DOCUMENTED, but PROPOSED only | GC-002 Alternative B describes database-level `(workspace_id, id)` composite FK treatment including `AuditRecord`→aggregate. ADR-0014 explicitly states GC-002 Alternative B remains Proposed and notes that its single-target formulation does not by itself solve WP19's five-subject-type problem. | Preserve the documented composite-FK property, but do not silently extend GC-002's one-target description into a five-type schema. Any such extension is an evaluation dependency or later decision, not part of normalization. |
| Per-type nullable columns | CORPUS-NAMED / UNDERSPECIFIED | ADR-0014 names `per-type-nullable-column` among open candidates and prefers none. No canonical five-column/FK/check-constraint realization is established by the corpus. | Evaluate the class as using subject-type-specific persisted reference slots. Do not normalize any zero/one/exactly-one population rule or enforcement mechanism into the candidate. |
| Opaque identifier | CORPUS-NAMED / UNDERSPECIFIED | ADR-0014 names `opaque-identifier` among open candidates and prefers none. No approved durable resolution convention is established. | Evaluate the class only on the premise that the persisted opaque value is intended to participate in durable subject resolution. The form and semantics of any required resolution convention remain unspecified and may expose D1/D2/D4/D5. |
| In-payload | CORPUS-DOCUMENTED CONCEPTUAL CANDIDATE | ADR-0014 expressly permits subject identification to be carried within AuditRecord's own content, giving before/after diff as an example, while stating that a diff is not presumed sufficient. | Evaluate the class as subject-identifying information carried inside persisted AuditRecord content. Whether type must be structurally encoded or may be resolved by another durable convention remains D1; do not assume GC-007's before/after shape is approved or sufficient. |

## 3. Normalized candidate contracts

### N1 — Polymorphic reference

**Corpus status:** CORPUS-NAMED / UNDERSPECIFIED.

**Minimum evaluation contract — EVALUATION ASSUMPTION, NOT ARCHITECTURE AUTHORITY:**

A persisted AuditRecord contains or participates in a durable reference convention intended to identify a concrete subject instance where the subject may belong to more than one subject type.

Normalization does **not** decide how subject type is disambiguated. Under the approved framework, whether type must be structurally encoded or may be resolved through another durable convention is **D1 — OPEN**. If A1 evaluation of this candidate requires a particular D1 answer, the correct result is `UNDETERMINED — DECISION REQUIRED`, not an invented discriminator mechanism.

**Not assumed:**

- column names such as `subject_type` / `subject_id`;
- one-column versus two-column representation;
- a dedicated discriminator column;
- FK versus non-FK enforcement;
- shared UUID namespace;
- workspace-key shape;
- registry/table implementation.

### N2 — Composite FK

**Corpus status:** CORPUS-DOCUMENTED, PROPOSED ONLY.

**Corpus-documented core:** GC-002 Alternative B proposes DB-level composite `(workspace_id, id)` foreign-key enforcement for named critical relationships including `AuditRecord`→aggregate, while other relationships use repository invariants plus tests.

**Minimum evaluation contract — EVALUATION ASSUMPTION where WP19 exceeds GC-002's documented scope:**

For purposes of Q2 evaluation, this candidate class means that durable AuditRecord subject identification relies materially on database-enforced composite foreign-key reference semantics. GC-002 documents only a single-target `AuditRecord`→aggregate formulation, while ADR-0014's current Q2 scope includes five structurally asymmetric subject types. The mechanism, if any, for adapting composite-FK semantics across that current scope is intentionally left unspecified.

This normalization statement does not decide whether the same representation must accommodate subject types beyond the five currently in WP19; that is **D5 — OPEN**.

**Not assumed:**

- that all five current types carry `workspace_id`;
- that all five current types can share one composite target;
- that GC-002 Alternative B is approved;
- that DB enforcement is mandatory under D4;
- any concrete multi-target FK layout;
- any future subject-type extension requirement under D5.

### N3 — Per-type nullable columns

**Corpus status:** CORPUS-NAMED / UNDERSPECIFIED.

**Minimum evaluation contract — EVALUATION ASSUMPTION, NOT ARCHITECTURE AUTHORITY:**

A persisted AuditRecord provides subject-type-specific reference slots intended to resolve the audited subject through the applicable subject-type relation.

Normalization does **not** establish a cardinality or exclusivity rule for those slots. In particular, it does not assume zero-or-one, exactly-one, or any specific CHECK/FK mechanism. If A1 or C2 evaluation depends on a subject-cardinality/exclusivity rule not established by authority, that dependency must be surfaced explicitly rather than supplied by normalization.

**Not assumed:**

- exactly five physical columns;
- one logical populated slot as an architecture rule;
- FK constraints on every slot;
- CHECK constraints;
- nullability rules;
- whether adding a sixth type requires a new column until D5 is resolved and C3/S8 are applied;
- any ORM relationship shape.

### N4 — Opaque identifier

**Corpus status:** CORPUS-NAMED / UNDERSPECIFIED.

**Minimum evaluation contract — EVALUATION ASSUMPTION, NOT ARCHITECTURE AUTHORITY:**

A persisted AuditRecord stores a durable subject identifier whose value is not assumed by normalization to encode the subject table/type in an architecture-defined structural form. The candidate is evaluated on the premise that durable resolution depends on an explicitly defined durable resolution convention; the form of that convention is left unspecified.

No namespace, registry, encoding scheme, global identity space, or other resolver infrastructure is introduced by normalization. If a resolver property is required to establish A1 or A2 and is not fixed by authority, the correct framework result is `UNDETERMINED — DECISION REQUIRED`, with the relevant D1–D5 dependency named.

**Not assumed:**

- globally unique IDs across all subject tables;
- a central identity registry;
- type-prefixed IDs;
- a shared EnterpriseObject identity;
- application-only or DB-only resolution.

### N5 — In-payload

**Corpus status:** CORPUS-DOCUMENTED CONCEPTUAL CANDIDATE.

**Corpus-documented core:** ADR-0014 states that durable subject identification need not use a dedicated subject-reference column and may be carried within the record's own content, for example within a before/after diff. ADR-0014 also states that such a diff is not automatically sufficient.

**Minimum evaluation contract:**

The persisted AuditRecord content itself contains information intended to durably resolve the audited mutation to a concrete subject. The evaluation must test whether the persisted content contract actually satisfies A1; mere presence of before/after data is not enough to claim PASS.

Normalization does **not** decide whether subject type must be encoded in payload, elsewhere in the record, or resolved through another durable convention. That question remains under **D1 — OPEN**.

**Not assumed:**

- GC-007 approval;
- a particular JSON shape;
- that every mutation has before and after values;
- that payload fields are indexed;
- that payload-only resolution satisfies A1/A2 without further convention;
- that subject identification must live only in payload.

## 4. Common evaluation baseline

To compare these five classes without silently redesigning them, the following baseline applies to every candidate:

1. The current WP19 Q2 scope contains five subject types: `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, and `Task`. Each candidate must be evaluated against that current scope. **This is not a decision that the subject-type set is closed, nor a requirement that the same representation must accommodate future subject types.**
2. The candidate receives no presumption of approval from being more fully documented in the corpus.
3. A missing engineering detail is not automatically a FAIL. If the detail is necessary to determine compliance and architecture has not decided it, use `UNDETERMINED — DECISION REQUIRED` and name the relevant D1–D5 surface or other exposed unresolved dependency.
4. Conversely, a candidate cannot receive PASS by silently supplying a favorable engineering realization that the corpus does not establish.
5. Implementation facts may be used only as `IMPLEMENTATION EVIDENCE — NOT ARCHITECTURE AUTHORITY`, consistent with the approved framework.
6. Stress tests S1–S10 remain stress tests only; normalization does not promote them to authoritative gates.
7. C1–C5 remain qualitative comparison dimensions and cannot override A1–A6.
8. No subject-cardinality/exclusivity rule is supplied by normalization. A comparison result may not reward or penalize a candidate on C2 by silently assuming exactly-one, zero-or-one, or another slot/reference cardinality contract.

### Explicit D5 decision dependency — subject-type set / future extension

**DECISION DEPENDENCY — OPEN.** The approved framework defines D5 as: is the Q2 subject-type set fixed to WP19's five current types, or should the persisted representation be designed for extension?

Normalization does not answer D5. Therefore:

- the five current WP19 types are the required present-scope test set;
- a sixth future subject type may be used later under S8/C3 to expose consequences, but cannot be treated as a mandatory architecture requirement before D5 is decided;
- C3 extensibility may describe what would change under each candidate, but comparison must not silently prefer or penalize a candidate by assuming either a closed set or an open-ended set;
- if candidate ranking materially depends on one D5 answer, that dependency must be recorded and carried to the D1–D5 decision stage.

## 5. Engineering inventions explicitly excluded from normalization

The following would be new design work and are therefore not introduced here:

- selecting `subject_type + subject_id` as the canonical polymorphic schema;
- inventing a universal `(workspace_id, id)` identity shape for all five subjects;
- defining five concrete nullable FK columns plus an exclusivity CHECK;
- creating a global subject registry for opaque identifiers;
- defining a canonical JSON payload schema for subject identity;
- selecting index strategies, SQLAlchemy mappings, migrations, repository APIs, or query implementations;
- resolving a subject-cardinality/exclusivity rule by implication;
- resolving GC-006 or GC-007;
- choosing D1–D5 answers by implication.

If later evaluation shows that one of these or another concrete realization is required to determine a candidate's status, that need must be exposed as a decision dependency rather than filled in silently.

## 6. Normalization result

All five ADR-0014 candidate classes are retained. None is rejected, preferred, or expanded into a sixth candidate.

They are normalized to a common evaluable level while preserving D1–D5 and other unresolved semantic dependencies explicitly. In particular, normalization no longer supplies a future subject-type policy, a slot/reference cardinality rule, a mandatory type-disambiguation mechanism, or resolver infrastructure as hidden premises.

**Next bounded step:** apply A1–A6 to N1–N5 using only the approved framework. Do not yet run S1–S10, C1–C5, decide D1–D5, select a persisted representation, modify WP19 planning status, or authorize implementation.
