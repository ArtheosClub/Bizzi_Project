# WP19 / Q2 A1–A6 Application v0.1

**Status:** Historical Q2 application analysis — planning synchronization updated 2026-08-30
**Date:** 2026-08-30
**Subject:** ADR-0014 Q2 — authoritative-constraint application to normalized candidates N1–N5
**Decision owner:** Project Owner through ADW-07
**Authority:** None. This artifact applies the approved procedure; it does not select, rank, approve, or reject a persisted representation.
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED for implementation.

> **Historical-state note:** This artifact records the A1–A6 pass as it was performed before D1–D5 and Q2-RI were accepted. Later accepted authority supersedes the OPEN labels recorded below as current-state claims; the analysis remains historical input. Historical references to the old `D4` DB-referential-integrity surface are synchronized here to the current identifier `Q2-RI` because this planning artifact is non-authoritative.

## 1. Scope and boundary

ADW-07 Block 4 / D6 approves the Q2 evaluation procedure for normative use. `Q2_CANDIDATE_NORMALIZATION_v0.1.md` fixes the normalized candidate set N1–N5 without selecting concrete engineering realizations.

This artifact performs only the A1–A6 stage. It does not rank candidates and does not select a Q2 representation.

## 2. Result matrix

| Candidate | A1 Durable subject resolvability | A2 Committed reference meaning | A3 Subject vs actor | A4 Event/AuditRecord assumption | A5 Retention exclusion | A6 No presumptive approval |
|---|---|---|---|---|---|---|
| N1 Polymorphic reference | UNDETERMINED | UNDETERMINED | PASS | PASS | PASS | PASS |
| N2 Composite FK | UNDETERMINED | UNDETERMINED | PASS | PASS | PASS | PASS |
| N3 Per-type nullable columns | UNDETERMINED | UNDETERMINED | PASS | PASS | PASS | PASS |
| N4 Opaque identifier | UNDETERMINED | UNDETERMINED | PASS | PASS | PASS | PASS |
| N5 In-payload | UNDETERMINED | UNDETERMINED | PASS | PASS | PASS | PASS |

No candidate received a FAIL at this historical stage. No candidate passed A1 or A2 merely because a favorable concrete realization could be invented.

## 3. Candidate findings retained from the original pass

### N1 — Polymorphic reference

A1 and A2 were UNDETERMINED because type interpretation and stable historical interpretation had not yet been decided. A3–A6 PASS. No concrete polymorphic schema, discriminator layout, FK policy, or other realization was presumed.

### N2 — Composite FK

A1 and A2 were UNDETERMINED because the documented GC-002 Alternative B did not establish a complete five-type Q2 mechanism or complete historical behavior. A3–A6 PASS. GC-002 Alternative B remained proposed only. N2 received no preference merely because a realization could use DB enforcement; the architectural weight of DB-enforced RI was then unresolved and is now governed separately by accepted Q2-RI.

### N3 — Per-type nullable columns

A1 and A2 were UNDETERMINED because cardinality/exclusivity and historical target semantics were not established. A3–A6 PASS. No exact columns, FK set, CHECK constraint, nullability rule, or ORM realization was presumed.

### N4 — Opaque identifier

A1 and A2 were UNDETERMINED because no durable namespace/resolution convention or stable interpretation had been established. A3–A6 PASS. No registry or global-ID mechanism was presumed.

### N5 — In-payload

A1 and A2 were UNDETERMINED because no persisted content contract or stable type/identity interpretation had been established. A3–A6 PASS. Payload-contained identification was neither forbidden nor presumed sufficient.

## 4. Historical cross-candidate findings

- No authoritative contradiction eliminated a candidate at the A1–A6 stage.
- A1 exposed different sufficiency dependencies rather than proving candidate equivalence.
- A2 exposed a shared historical-stability requirement.
- At the time of this pass D1–D5 were open. They are now CLOSED — ACCEPTED through separate canonical authority artifacts.
- The historical DB-referential-integrity decision surface formerly labeled `D4` is now `Q2-RI`; Q2-RI is CLOSED — ACCEPTED — O2 PREFERENCE through `00_ARCHITECTURE/07_AUDIT/ADW07_Q2_RI_REFERENTIAL_INTEGRITY_WEIGHT_DECISION.md`.

## 5. Gate result / current interpretation

**HISTORICAL A1–A6 APPLICATION COMPLETE — NO CANDIDATE ELIMINATED AT THAT STAGE.**

Current authority must be taken from the accepted D1–D5 and Q2-RI records, not from the historical OPEN labels of this artifact. Q2-ST and the final Q2 persisted representation remain OPEN. WP19 remains BLOCKED / UNAUTHORIZED.
