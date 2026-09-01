# WP19 / Q2 Post-Q2-RI Candidate Re-application v0.1

**Status:** Draft — post-authority evaluation / recommendation only  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 — short candidate re-application after accepted Q2-RI  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact applies accepted Q2-RI; it does not select a representation.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Controlling authority

D1–D5 are CLOSED — ACCEPTED. Q2-RI is CLOSED — ACCEPTED — O2 PREFERENCE.

Q2-RI requires DB-enforced referential-integrity weight to be applied **per concrete realization**, not by candidate class. A realization receives comparative credit only when it actually provides stronger DB-enforced RI and obtaining that property in that realization does not require a persistence abstraction whose only justification is enforcement location under the repository Abstraction Justification Rule, and does not contradict another accepted architecture constraint.

Lack of ordinary DB FK enforcement is not automatically disqualifying. Each application of the preference must record its reasoning.

Q2-ST remains OPEN and is not decided here.

## 2. Re-application discipline

The normalized candidate classes N1–N5 are not concrete realizations. Therefore accepted Q2-RI does **not** permit statements such as:

- `N3 wins because N3 has FKs`;
- `N1 loses because polymorphic references lack FKs`;
- `N2 wins because its name contains FK`.

The valid question is narrower:

> Does the concrete realization presently supported by the corpus provide stronger DB-enforced RI under the accepted Q2-RI condition, and if so what comparative credit follows?

Where the corpus does not define a concrete realization sufficiently to answer that question, Q2-RI credit is **UNDETERMINED**, not invented.

## 3. Candidate-by-candidate application

### N1 — Polymorphic reference

**D1–D5 conformity outlook:** strong for a suitably qualified realization.

**Q2-RI application:** **NO CLASS-LEVEL CREDIT; CONCRETE CREDIT UNDETERMINED.**

Reasoning recorded:

- N1 normalization does not establish one concrete persistence mechanism or DB enforcement structure.
- A conventional multi-table polymorphic `type + id` style cannot receive DB-RI credit merely by label because ordinary FK enforcement across heterogeneous target tables is not inherent.
- A hypothetical registry/base-table/auxiliary target structure is not invented for this comparison. If later proposed, it must independently pass the Abstraction Justification Rule; enforcement location alone cannot justify it.
- Therefore N1 remains admissible without DB-RI credit if its concrete realization establishes correctness through another explicit recorded mechanism, but no positive RI credit is available from the class definition itself.

### N2 — Composite FK

**Current documented form:** not sufficient for complete five-type Q2 scope.

**Q2-RI application:** **LOCAL DOCUMENTED CREDIT WHERE THE COMPOSITE FK ACTUALLY APPLIES; NO Q2-WIDE CREDIT.**

Reasoning recorded:

- GC-002 Alternative B documents DB-native composite-FK enforcement for named relationships matching its `(workspace_id, id)` shape.
- That is a real DB-enforced property of the documented applicable realization and can receive comparative credit locally.
- The documented N2 form still does not provide a complete five-type AuditRecord subject-reference realization across structurally asymmetric subjects.
- Q2-RI preference cannot convert partial documented enforcement into Q2-wide sufficiency and does not approve GC-002 Alternative B.

Current position: **do not select N2 as currently documented.**

### N3 — Per-type nullable relations / slots

**D1–D5 conformity outlook:** strong for a suitably qualified realization.

**Q2-RI application:** **NO CLASS-LEVEL CREDIT; CONCRETE CREDIT AVAILABLE IF PROPOSED RELATIONS ACTUALLY CARRY DB-ENFORCED RI UNDER Q2-RI.**

Reasoning recorded:

- N3 normalization establishes subject-type-specific persisted paths but explicitly does not establish exact columns, FK constraints, CHECK constraints, indexes, or ORM realization.
- Therefore N3 does not receive DB-RI credit merely because per-type relations can naturally be realized as foreign keys.
- A concrete N3 proposal that actually defines ordinary per-type FK enforcement can receive comparative credit for those enforced relations if doing so requires no otherwise-unjustified persistence abstraction and violates no accepted constraint.
- Such a proposal must separately establish the exactly-one/exclusivity semantics required for one logical audited subject; DB FKs alone do not solve that issue.

### N4 — Opaque identifier

**D1–D5 conformity outlook:** conditional on explicit type plus durable stable resolution convention.

**Q2-RI application:** **NO CLASS-LEVEL CREDIT; CONCRETE CREDIT UNDETERMINED.**

Reasoning recorded:

- no approved registry/namespace/DB target structure is part of normalized N4;
- no such abstraction may be invented solely to obtain DB-RI credit;
- lack of DB-native RI does not itself reject a conforming N4 realization.

N4 continues to carry additional resolver/namespace semantic burden independent of Q2-RI.

### N5 — In-payload subject identity

**D1–D5 conformity outlook:** conditional on an explicit mandatory subject-identity content contract.

**Q2-RI application:** **NO CLASS-LEVEL CREDIT; CONCRETE CREDIT UNDETERMINED.**

Reasoning recorded:

- normalized N5 establishes no DB-native target relation merely by carrying identity in persisted content;
- DB/content indexing or constraint mechanisms cannot be assumed without a concrete proposal;
- lack of ordinary FK enforcement does not itself reject a conforming N5 realization.

N5 continues to carry content-contract/query/integrity burden independent of Q2-RI.

## 4. N1 versus N3 after Q2-RI

Accepted Q2-RI resolves the **weighting rule**, but it does not by itself resolve the N1/N3 pair at candidate-class level.

The previous status `UNDETERMINED — Q2-RI DECISION REQUIRED` is therefore replaced by:

**N1 vs N3 — UNDETERMINED AT CLASS LEVEL — CONCRETE REALIZATION COMPARISON REQUIRED.**

This is not a failure of Q2-RI. It is the direct consequence of the accepted rule that RI credit attaches to a realization, not a candidate class.

A concrete N3 realization with actual per-type FK enforcement may receive RI comparative credit that a concrete N1 realization without equivalent DB enforcement does not receive. That is a legitimate result under Q2-RI and does not constitute an automatic N3 win: all other accepted constraints and comparative burdens remain in force.

Conversely, N1 must not be forced to add a registry/base-table abstraction solely to obtain RI credit. Absence of that credit is not disqualification.

## 5. Effect on final representation decision

Q2-RI has removed the prior ambiguity about how to value DB-native integrity, but the normalized candidate classes are still too abstract to produce a defensible final N1-vs-N3 ranking from RI alone.

Before final Q2 representation selection, the surviving leading candidates need bounded concrete realization descriptions sufficient to evaluate:

- D1–D5 conformity;
- Q2-RI per-realization credit;
- N3 exclusivity/cardinality behavior;
- N1 durable validation/resolution behavior;
- C1/C2/C4/C5 consequences without inventing unrelated architecture.

This is evaluation design, not implementation authorization.

Q2-ST remains a separate open architecture decision and must be resolved before final Q2 representation authority under the current agreed sequence.

## 6. Current comparative state

| Candidate | Current state after Q2-RI |
|---|---|
| N1 | Viable class; no class-level RI credit; concrete realization required |
| N2 | Partial/local RI credit where documented; still insufficient as complete five-type Q2 representation |
| N3 | Viable class; no class-level RI credit; concrete realization may earn RI credit; exclusivity still required |
| N4 | Viable with material qualification; no class-level RI credit |
| N5 | Viable with material qualification; no class-level RI credit |

No candidate is selected or rejected by Q2-RI alone.

## 7. Gate result

**Q2-RI RE-APPLICATION COMPLETE — WEIGHTING AMBIGUITY CLOSED — NO CANDIDATE-CLASS RI CREDIT INVENTED — N1 VS N3 REQUIRES CONCRETE REALIZATION COMPARISON — Q2-ST REMAINS OPEN — FINAL Q2 REPRESENTATION NOT SELECTED.**

Current state:

- D1–D5: **CLOSED — ACCEPTED**;
- Q2-RI: **CLOSED — ACCEPTED — O2 PREFERENCE**;
- Q2-ST: **OPEN**;
- N1–N5: **UNAPPROVED**;
- final Q2 persisted representation: **OPEN / NOT ESTABLISHED**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED**.
