# ADW-07 — Q2-RI Referential-Integrity Weight Decision

**Workshop:** ADW-07 — Events, Audit, and Provenance  
**Workshop Status:** OPEN  
**Decision:** Q2-RI — architectural weight of DB-enforced referential integrity  
**Decision Status:** ACCEPTED  
**Decision Owner / Authority / Decider:** Project Owner / Andrew  
**Decision Date:** 2026-08-30  
**Accepted option:** Q2-RI-O2 — PREFERENCE, not REQUIREMENT

## Decision

This decision does not amend or supersede D1–D5; their canonical authority remains exclusively in their respective accepted decision records.

A realization that provides stronger DB-enforced referential integrity receives comparative credit for that property, provided that obtaining it in that realization does not require introducing a persistence abstraction whose only justification is enforcement location under the repository's Abstraction Justification Rule, and does not contradict another accepted architecture constraint. Where that condition is not met, DB-enforced referential integrity carries no comparative weight for that realization.

Lack of ordinary database foreign-key enforcement is not by itself disqualifying where durable correctness, validation, and historical subject resolvability are established through another explicit, recorded mechanism.

This preference applies to a concrete proposed realization, not to a candidate class. It is a comparative input only: it cannot substitute for D1–D5 conformity, cannot by itself select a Q2 representation, and each application of the preference in candidate evaluation must record its reasoning.

DB-enforced referential integrity is therefore a comparative preference, not a Q2 requirement. Per-subject-type weighting (Q2-RI-O4) was considered and not adopted.

Q2-RI does not decide, constrain, favor, or disfavor a Q2-ST ranging rule. The preference is applied only to a concrete proposed realization under the subject-type rule and subject-type set then in force. Effects caused by the size or extensibility of that set must not be converted into candidate preference; D5 prohibits extensibility convenience from determining, ranking, or defaulting the representation.

## Abstraction Justification Rule reference

The referenced repository rule is `CLAUDE.md`, **Mandatory: before introducing a new architectural abstraction — Abstraction Justification Rule**:

> A new architectural abstraction must either solve an existing, demonstrated problem, or be a necessary precondition for implementing the next Work Packages. Anticipated future need is not sufficient justification.

Q2-RI does not create a weaker or stronger abstraction rule. The repository rule remains controlling.

## Identifier reconciliation required by accepted-record lifecycle authority

This section is an **identifier / traceability correction without substantive change** under `ADW07_ACCEPTED_DECISION_RECORD_LIFECYCLE_DECISION.md`. The original accepted records remain unchanged.

Affected accepted records:

1. `00_ARCHITECTURE/07_AUDIT/ADW07_D1_SUBJECT_TYPE_DISAMBIGUATION_DECISION.md` — its **Explicit non-decisions** list uses the historical label `D4 — DB-enforced referential-integrity policy`.
2. `00_ARCHITECTURE/07_AUDIT/ADW07_D2_WORKSPACE_SUBJECT_SEMANTICS_DECISION.md` — its non-decision list uses the historical label `D4 database-enforced referential integrity`.

Exact reconciliation effect:

- those historical references identify the decision surface now named **Q2-RI — architectural weight of DB-enforced referential integrity**;
- they do **not** identify or modify the later accepted **D4 — Subject Reference Semantics** decision;
- no substantive meaning of D1 or D2 is changed;
- both original accepted records remain preserved without in-place edits.

This reconciliation applies to those accepted authority records. Stale identifier references in non-authoritative planning artifacts are planning synchronization defects and are not preserved by this clause.

## Consequences for candidate evaluation

- DB-enforced RI is evaluated per concrete realization, not attributed to N1–N5 by class name.
- A realization receives RI comparative credit only when the condition in the Decision section is satisfied for that realization.
- Failure to receive that credit is not an automatic architecture rejection.
- Q2-RI alone cannot select a persisted representation.
- Every application of the preference in candidate evaluation must record its reasoning.

## Explicit non-decisions

This decision does not:

- select, approve, reject, default, or implement N1–N5;
- approve GC-002 Alternative B;
- require a foreign key for every subject type;
- adopt Q2-RI-O1, O3, or O4;
- define FK delete/cascade/restrict/set-null behavior;
- define N3 exclusivity/cardinality constraints;
- define a resolver for N1 or N4;
- decide Q2-ST;
- amend D1–D5;
- decide actor attribution / ActorContext;
- decide migration or runtime implementation;
- close ADW-07;
- authorize WP19 implementation.

## Current Q2 state

- D1–D5: **CLOSED — ACCEPTED**.
- Q2-RI: **CLOSED — ACCEPTED — O2 PREFERENCE**.
- Q2-ST: **OPEN**.
- N1–N5: **UNAPPROVED**; candidate evaluation must now re-apply Q2-RI per concrete realization.
- Q2 persisted representation: **OPEN / NOT ESTABLISHED**.
- ADW-07: **OPEN**.
- WP19: **BLOCKED / UNAUTHORIZED** pending explicit Q2 persisted-representation resolution or separate explicit bounded interim-shape authorization.

## Next bounded step

Perform a short post-Q2-RI candidate re-application using the accepted per-realization preference and recorded reasoning. Do not infer a candidate-class preference. Q2-ST remains a separate open decision surface and final Q2 persisted-representation selection remains unauthorized until the required decision work is complete.
