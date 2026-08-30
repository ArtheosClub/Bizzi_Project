# WP19 / Q2 A1–A6 Application v0.1

**Status:** Draft — Q2 application analysis only
**Date:** 2026-08-30
**Subject:** ADR-0014 Q2 — authoritative-constraint application to normalized candidates N1–N5
**Decision owner:** Project Owner through ADW-07
**Authority:** None. This artifact applies the approved procedure; it does not select, rank, approve, or reject a persisted representation.
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED for implementation.

## 1. Scope and boundary

ADW-07 Block 4 / D6 approves the Q2 evaluation procedure for normative use. `Q2_CANDIDATE_NORMALIZATION_v0.1.md` fixes the normalized candidate set N1–N5 without selecting concrete engineering realizations.

This artifact performs only the next procedure stage:

```text
AUTHORITATIVE CONSTRAINTS A1–A6
        ↓
CHECK N1–N5 AGAINST THOSE CONSTRAINTS
  PASS / FAIL / UNDETERMINED — DECISION REQUIRED
```

It does **not** run S1–S10, does **not** run C1–C5, does **not** decide D1–D5, does **not** rank candidates, and does **not** select a Q2 representation.

A `PASS` is assigned only where the normalized candidate satisfies the constraint without supplying an unresolved engineering or architecture assumption. A `FAIL` requires contradiction with established authority. Otherwise the result is `UNDETERMINED — DECISION REQUIRED` and the dependency is named.

## 2. Result matrix

| Candidate | A1 Durable subject resolvability | A2 Committed reference meaning | A3 Subject vs actor | A4 Event/AuditRecord assumption | A5 Retention exclusion | A6 No presumptive approval |
|---|---|---|---|---|---|---|
| N1 Polymorphic reference | UNDETERMINED | UNDETERMINED | PASS | PASS | PASS | PASS |
| N2 Composite FK | UNDETERMINED | UNDETERMINED | PASS | PASS | PASS | PASS |
| N3 Per-type nullable columns | UNDETERMINED | UNDETERMINED | PASS | PASS | PASS | PASS |
| N4 Opaque identifier | UNDETERMINED | UNDETERMINED | PASS | PASS | PASS | PASS |
| N5 In-payload | UNDETERMINED | UNDETERMINED | PASS | PASS | PASS | PASS |

No candidate receives a FAIL at this stage. No candidate passes A1 or A2 merely because a favorable concrete realization could be invented.

## 3. N1 — Polymorphic reference

### A1 — UNDETERMINED — D1 DECISION REQUIRED

ADR-0014 requires the persisted AuditRecord to durably resolve to one concrete audited subject. N1 establishes only a durable reference convention intended to identify a subject across more than one subject type. Normalization deliberately leaves type disambiguation unresolved.

A1 therefore cannot be marked PASS without supplying a D1 answer: whether subject type must be structurally encoded or may be determined through another durable convention. No discriminator mechanism is invented here.

### A2 — UNDETERMINED — STABLE-INTERPRETATION DEPENDENCY

N1 does not establish enough about the durable reference convention to prove that an already committed reference can never acquire a different interpretation later. AuditRecord immutability prevents mutation of the committed record itself, but A2 also tests whether the same persisted reference could later resolve to a different subject through changed interpretation or resolution semantics.

No such instability is established, so this is not FAIL. Stable interpretation must be established before PASS.

### A3 — PASS

N1 identifies the audited subject and does not use actor attribution as a substitute. This is consistent with ADR-0014's separation of `what was acted on` from `who acted`.

### A4 — PASS

N1 contains no dependency on Domain Event/AuditRecord identity and no dependency on a particular Block 2 R1 outcome.

### A5 — PASS

N1 introduces no retention-duration requirement or selection criterion.

### A6 — PASS

N1 is evaluated only as a normalized candidate class. No polymorphic schema, discriminator layout, FK policy, or other realization receives presumptive approval.

## 4. N2 — Composite FK

### A1 — UNDETERMINED — CURRENT-SCOPE RESOLUTION DEPENDENCY

The corpus-documented GC-002 Alternative B describes a composite `(workspace_id, id)` FK for a single `AuditRecord`→aggregate target. ADR-0014 Q2 currently spans five structurally asymmetric subject types. Normalization intentionally does not invent a multi-target composite-FK realization.

It is therefore not established that N2, as currently documented/normalized, durably resolves every subject in the current five-type scope. That missing realization is not itself a contradiction with A1, so the result is UNDETERMINED rather than FAIL.

This result does not decide D5 and does not require support for a future sixth type.

### A2 — UNDETERMINED — HISTORICAL REFERENCE STABILITY DEPENDENCY

Database-enforced FK semantics can constrain a reference while its target exists, but the normalized candidate does not establish the complete historical behavior needed by A2 across subject lifecycle/deletion and any multi-target adaptation. A2 cannot be passed merely from the words `composite FK`.

D3 may become relevant to the eventual answer, but this pass does not decide whether an AuditRecord reference blocks physical deletion. No A2 contradiction is established.

### A3 — PASS

The candidate concerns subject reference semantics and does not substitute actor attribution for subject identity.

### A4 — PASS

The candidate does not depend on Event/AuditRecord identity or on a particular R1 answer.

### A5 — PASS

No retention-duration criterion is introduced.

### A6 — PASS

GC-002 Alternative B remains Proposed only. Evaluating its documented composite-FK property does not approve it and does not make DB-enforced referential integrity mandatory under D4.

## 5. N3 — Per-type nullable columns

### A1 — UNDETERMINED — SUBJECT-CARDINALITY / EXCLUSIVITY DEPENDENCY

N3 provides subject-type-specific persisted reference slots intended to resolve the audited subject through the applicable relation. Normalization explicitly does not establish whether zero, one, or multiple slots may be populated.

Without a settled semantic rule sufficient to ensure that a committed AuditRecord identifies one concrete audited subject, A1 cannot be marked PASS. Supplying an `exactly one` CHECK or equivalent rule here would be new design work. No contradiction with A1 is established, so the result is UNDETERMINED.

### A2 — UNDETERMINED — HISTORICAL REFERENCE STABILITY DEPENDENCY

The persisted slots themselves would be part of an immutable AuditRecord, but normalization does not establish enough about target identity/lifecycle semantics to prove that their committed meaning cannot later resolve differently. A2 therefore remains undetermined rather than being inferred from column persistence alone.

### A3 — PASS

The slots represent subject relations and do not use actor attribution as subject identity.

### A4 — PASS

No Event/AuditRecord identity or R1 assumption is required by the normalized candidate.

### A5 — PASS

No retention-duration criterion is introduced.

### A6 — PASS

No concrete number of columns, FK set, CHECK constraint, nullability rule, or ORM realization is presumed approved.

## 6. N4 — Opaque identifier

### A1 — UNDETERMINED — D1 / DURABLE-RESOLUTION-CONVENTION DEPENDENCY

N4 stores a durable opaque subject identifier and states only that durable resolution depends on an explicitly defined durable convention whose form remains unspecified. The repository has no approved namespace, registry, encoding, shared identity space, or equivalent resolution contract.

A1 cannot be marked PASS until the required durable interpretation is established. Depending on the eventual mechanism, D1 may be required. Inventing a resolver would violate normalization, so the result is UNDETERMINED.

### A2 — UNDETERMINED — STABLE-RESOLUTION DEPENDENCY

Because the resolution convention is unspecified, it is not established that the same committed opaque value is permanently prevented from resolving to a different subject through later convention or resolver changes. That risk is not proven to occur, so the candidate does not FAIL A2; the required stability is simply unresolved.

### A3 — PASS

The opaque value is evaluated as subject identification and is not derived from actor attribution.

### A4 — PASS

No Event/AuditRecord identity or R1 answer is assumed.

### A5 — PASS

No retention-duration criterion is introduced.

### A6 — PASS

No registry, namespace, global-ID system, application-only resolver, or DB-only resolver receives presumptive approval.

## 7. N5 — In-payload

### A1 — UNDETERMINED — D1 / PERSISTED-CONTENT-CONTRACT DEPENDENCY

ADR-0014 explicitly allows subject identification to be carried within persisted AuditRecord content, but also explicitly states that a before/after diff is not presumed sufficient. N5 therefore remains admissible but not automatically sufficient.

The normalized candidate does not establish a concrete persisted content contract that proves durable instance resolution and does not decide how subject type is interpreted. A1 is therefore UNDETERMINED; D1 may be required depending on the eventual content contract.

### A2 — UNDETERMINED — STABLE-CONTENT-INTERPRETATION DEPENDENCY

AuditRecord content is historical and immutable once committed, but A2 also requires that the meaning of the persisted subject reference not silently repoint through later interpretation. No approved payload/content contract currently establishes that stability. The candidate therefore cannot receive PASS yet, but no contradiction with A2 is established.

### A3 — PASS

N5 concerns subject-identifying persisted content and does not substitute actor attribution for subject identity.

### A4 — PASS

The normalized in-payload candidate does not depend on Event/AuditRecord identity or a particular R1 outcome.

### A5 — PASS

No retention-duration criterion is introduced.

### A6 — PASS

Payload-contained identification is treated exactly as ADR-0014 requires: neither forbidden nor presumed sufficient. GC-007 and any particular JSON/before-after shape remain unapproved.

## 8. Cross-candidate findings from A1–A6 only

### Finding A — no authoritative contradiction eliminates a candidate yet

No N1–N5 candidate contradicts A3–A6 in its normalized form. No candidate can therefore be rejected at this stage on those constraints.

### Finding B — A1 is intentionally discriminating on sufficiency, not candidate labels

Every candidate remains UNDETERMINED on A1 because the normalization pass correctly refused to manufacture the concrete semantic details required to prove durable resolution. The dependencies differ:

- N1: D1/type interpretation;
- N2: current five-type resolution mechanism;
- N3: subject-cardinality/exclusivity semantics;
- N4: D1 and durable resolution convention;
- N5: D1 and persisted-content contract.

The common status does not mean the candidates are equivalent; it means A1 cannot be honestly passed from class labels alone.

### Finding C — A2 exposes a shared historical-stability requirement

All five candidates are UNDETERMINED on A2 because the normalized class descriptions do not yet establish enough to prove stable interpretation of a committed reference across later lifecycle or resolution changes. This is not a new representation criterion. It is direct application of approved A2.

The next stages must not convert this shared uncertainty into an invented universal identity or deletion rule.

### Finding D — D1–D5 remain open

This pass records dependencies but decides none of them. In particular:

- D1 remains open despite being exposed by N1/N4/N5;
- D2 remains open;
- D3 remains open and may matter to A2/historical behavior;
- D4 remains open; N2 receives no preference because it can use DB enforcement;
- D5 remains open and was not used to require future extensibility.

## 9. Gate result

**A1–A6 APPLICATION COMPLETE — NO CANDIDATE ELIMINATED — DECISION DEPENDENCIES EXPOSED.**

This result does not mean all candidates are acceptable Q2 answers. It means the authoritative-constraint pass alone has not established a FAIL for any normalized candidate and has not established A1/A2 sufficiency for any of them.

WP19 remains **BLOCKED / UNAUTHORIZED**. Q2 remains **OPEN**. D1–D5 remain **OPEN**.

**Next bounded step under the approved procedure:** apply semantic stress tests S1–S10 to N1–N5, carrying the A1/A2 dependencies forward without resolving them by implication. Do not yet run C1–C5, decide D1–D5, select a persisted representation, or authorize WP19 implementation.
