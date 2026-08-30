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

Normalization means only: state the minimum property that must be true for the already-named candidate class to be meaningfully evaluated. It does not choose concrete column names, SQL types, FK layouts, discriminator vocabulary, payload schema, indexes, ORM mappings, migration strategy, or service API.

Every statement below is labeled as one of:

- **CORPUS-DOCUMENTED** — the repository gives more than the candidate name and describes a relevant representation property;
- **CORPUS-NAMED / UNDERSPECIFIED** — ADR-0014 names the candidate class, but the repository does not define enough persisted structure to treat one engineering realization as canonical;
- **EVALUATION ASSUMPTION — NOT ARCHITECTURE AUTHORITY** — a minimum semantic condition used only to make the candidate class testable without pretending that a concrete engineering design has been approved.

No evaluation assumption becomes architecture authority through this document.

## 2. Corpus provenance matrix

| Candidate | Corpus status | Repository basis | Normalization consequence |
|---|---|---|---|
| Polymorphic reference | CORPUS-NAMED / UNDERSPECIFIED | ADR-0014 names `polymorphic-reference` among open candidates and prefers none. No repository contract defining `subject_type + subject_id`, `target_type + target_id`, or an equivalent canonical pair was found in the candidate provenance pass. | Evaluate the class only as a durable reference whose interpretation can distinguish the concrete subject across multiple subject types. Do not assume a specific discriminator-column design. |
| Composite FK | CORPUS-DOCUMENTED, but PROPOSED only | GC-002 Alternative B describes database-level `(workspace_id, id)` composite FK treatment including `AuditRecord`→aggregate. ADR-0014 explicitly states GC-002 Alternative B remains Proposed and notes that its single-target formulation does not by itself solve WP19's five-subject-type problem. | Preserve the documented composite-FK property, but do not silently extend GC-002's one-target description into a five-type schema. Any such extension is an evaluation assumption or later decision. |
| Per-type nullable columns | CORPUS-NAMED / UNDERSPECIFIED | ADR-0014 names `per-type-nullable-column` among open candidates and prefers none. No canonical five-column/FK/check-constraint realization is established by the corpus. | Evaluate the class as using subject-type-specific persisted reference slots, with exactly how exclusivity and integrity are represented left open. |
| Opaque identifier | CORPUS-NAMED / UNDERSPECIFIED | ADR-0014 names `opaque-identifier` among open candidates and prefers none. No approved durable registry, namespace, encoding, or resolution convention is established. | Evaluate only on the assumption that some explicitly defined durable convention can resolve the opaque value to one concrete subject. The convention itself remains unspecified and may expose D1/D2/D4/D5. |
| In-payload | CORPUS-DOCUMENTED CONCEPTUAL CANDIDATE | ADR-0014 expressly permits subject identification to be carried within AuditRecord's own content, giving before/after diff as an example, while stating that a diff is not presumed sufficient. | Evaluate the class as durable subject-identifying information inside persisted AuditRecord content. Do not assume GC-007's before/after shape is approved or sufficient. |

## 3. Normalized candidate contracts

### N1 — Polymorphic reference

**Corpus status:** CORPUS-NAMED / UNDERSPECIFIED.

**Minimum evaluation contract — EVALUATION ASSUMPTION, NOT ARCHITECTURE AUTHORITY:**

A persisted AuditRecord contains or participates in a durable reference convention capable of identifying one concrete subject instance where the subject may belong to more than one subject type. The convention must have some durable way to disambiguate interpretation; this statement does not require that disambiguation to be a dedicated persisted discriminator column.

**Not assumed:**

- column names such as `subject_type` / `subject_id`;
- one-column versus two-column representation;
- FK versus non-FK enforcement;
- shared UUID namespace;
- workspace-key shape;
- registry/table implementation.

### N2 — Composite FK

**Corpus status:** CORPUS-DOCUMENTED, PROPOSED ONLY.

**Corpus-documented core:** GC-002 Alternative B proposes DB-level composite `(workspace_id, id)` foreign-key enforcement for named critical relationships including `AuditRecord`→aggregate, while other relationships use repository invariants plus tests.

**Minimum evaluation contract — EVALUATION ASSUMPTION where WP19 exceeds GC-002's documented scope:**

For purposes of Q2 evaluation, this candidate class means that durable AuditRecord subject identification relies materially on database-enforced composite foreign-key reference semantics. Because ADR-0014 requires one mechanism across five structurally asymmetric subject types and GC-002 documents only a single-target `AuditRecord`→aggregate formulation, the mechanism for extending or adapting composite-FK semantics across all five types is intentionally left unspecified.

**Not assumed:**

- that all five types carry `workspace_id`;
- that all five types can share one composite target;
- that GC-002 Alternative B is approved;
- that DB enforcement is mandatory under D4;
- any concrete multi-target FK layout.

### N3 — Per-type nullable columns

**Corpus status:** CORPUS-NAMED / UNDERSPECIFIED.

**Minimum evaluation contract — EVALUATION ASSUMPTION, NOT ARCHITECTURE AUTHORITY:**

A persisted AuditRecord provides subject-type-specific reference slots such that the populated slot identifies which subject-type relation is being used and resolves to the concrete subject instance.

For evaluation only, the class is interpreted as intending one logical subject per AuditRecord. How the representation guarantees zero/one/exactly-one populated slot is not assumed and must be surfaced under integrity analysis rather than invented here.

**Not assumed:**

- exactly five physical columns;
- FK constraints on every slot;
- CHECK constraints;
- nullability rules;
- whether adding a sixth type requires a new column until tested under C3/D5;
- any ORM relationship shape.

### N4 — Opaque identifier

**Corpus status:** CORPUS-NAMED / UNDERSPECIFIED.

**Minimum evaluation contract — EVALUATION ASSUMPTION, NOT ARCHITECTURE AUTHORITY:**

A persisted AuditRecord stores a durable subject identifier whose value alone is not assumed to encode the subject table/type in an architecture-defined structural form. Resolution to one concrete subject depends on an explicitly defined durable convention, namespace, registry, or equivalent mechanism.

The existence and properties of that resolver are not assumed to be approved. If a required resolver property is necessary to establish A1 or A2 and is not fixed by authority, the correct framework result is `UNDETERMINED — DECISION REQUIRED`, not an invented resolver.

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

The persisted AuditRecord content itself contains durable information intended to resolve the audited mutation to one concrete subject. The evaluation must test whether the content contract actually provides stable instance resolution and adequate type interpretation; mere presence of before/after data is not enough to claim A1 PASS.

**Not assumed:**

- GC-007 approval;
- a particular JSON shape;
- that every mutation has before and after values;
- that payload fields are indexed;
- that payload-only resolution satisfies A1/A2 without further convention;
- that subject identification must live only in payload.

## 4. Common evaluation baseline

To compare these five classes without silently redesigning them, the following baseline applies to every candidate:

1. The candidate is evaluated against the same WP19 Q2 problem established by ADR-0014: one persisted AuditRecord subject-identification mechanism spanning the five current subject types `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, and `Task`.
2. The candidate receives no presumption of approval from being more fully documented in the corpus.
3. A missing engineering detail is not automatically a FAIL. If the detail is necessary to determine compliance and architecture has not decided it, use `UNDETERMINED — DECISION REQUIRED` and name the relevant D1–D5 surface.
4. Conversely, a candidate cannot receive PASS by silently supplying a favorable engineering realization that the corpus does not establish.
5. Implementation facts may be used only as `IMPLEMENTATION EVIDENCE — NOT ARCHITECTURE AUTHORITY`, consistent with the approved framework.
6. Stress tests S1–S10 remain stress tests only; normalization does not promote them to authoritative gates.
7. C1–C5 remain qualitative comparison dimensions and cannot override A1–A6.

## 5. Engineering inventions explicitly excluded from normalization

The following would be new design work and are therefore not introduced here:

- selecting `subject_type + subject_id` as the canonical polymorphic schema;
- inventing a universal `(workspace_id, id)` identity shape for all five subjects;
- defining five concrete nullable FK columns plus an exclusivity CHECK;
- creating a global subject registry for opaque identifiers;
- defining a canonical JSON payload schema for subject identity;
- selecting index strategies, SQLAlchemy mappings, migrations, repository APIs, or query implementations;
- resolving GC-006 or GC-007;
- choosing D1–D5 answers by implication.

If later evaluation shows that one of these or another concrete realization is required to determine a candidate's status, that need must be exposed as a decision dependency rather than filled in silently.

## 6. Normalization result

All five ADR-0014 candidate classes are retained. None is rejected, preferred, or expanded into a sixth candidate.

They are now normalized to a common evaluable level: each has a minimum semantic contract sufficient to begin A1–A6 analysis while preserving all unresolved concrete design choices as explicit assumptions or decision dependencies.

**Next bounded step:** apply A1–A6 to N1–N5 using only the approved framework. Do not yet run S1–S10, C1–C5, decide D1–D5, select a persisted representation, modify WP19 planning status, or authorize implementation.
