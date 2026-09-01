# ADW-07 / D1 Structural Discriminator Clarification Proposal v0.1

**Status:** Draft — clarification proposal only  
**Date:** 2026-08-30  
**Affected accepted authority:** `00_ARCHITECTURE/07_AUDIT/ADW07_D1_SUBJECT_TYPE_DISAMBIGUATION_DECISION.md`  
**Lifecycle classification:** Clarifies an ambiguity under `ADW07_ACCEPTED_DECISION_RECORD_LIFECYCLE_DECISION.md` §3  
**Decision owner:** Project Owner / Andrew  
**Authority:** None. This artifact does not amend or accept a clarification to D1.  
**Implementation effect:** None. Q2 representation remains OPEN and WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Ambiguity requiring clarification

Accepted D1 states:

> A persisted AuditRecord subject reference MUST include an explicit durable subject-type discriminator as part of its durable reference contract. The discriminator’s committed value MUST identify exactly one of the current Q2 subject types: Workspace, EnterpriseObject, User, WorkspaceMembership, or Task. Type qualification within a durable subject identity satisfies this rule. D1 does not decide the physical placement or persistence mechanism of the discriminator.

Two readings remain textually defensible for a BR3-style representation with five subject-specific persisted reference slots:

1. **Value-bearing discriminator reading.** D1 requires a separately represented discriminator component with a committed scalar/token value, even if the subject identity is also structurally type-qualified by its slot.
2. **Structural discriminator reading.** The durable structural position of the one populated subject-specific slot is itself an explicit discriminator mechanism: the committed reference structure identifies exactly one current subject type, so a second scalar discriminator is unnecessary.

D1 did not resolve this distinction. Its canonical text is ACCEPTED and immutable; therefore the ambiguity must not be settled by editing D1 in place or by silently choosing a reading inside the final Q2 representation decision.

## 2. Proposed clarification

**Proposed clarification:**

> **For purposes of accepted D1, an explicit durable subject-type discriminator need not be stored as a separate scalar or token column. A persisted subject-reference structure in which exactly one architecture-authorized, subject-type-specific reference position is durably populated constitutes an explicit durable discriminator when the populated structural position itself unambiguously identifies exactly one accepted subject type. In that realization, the discriminator’s committed value is the durable structural qualification represented by the populated subject-specific position. No second persisted subject-type value is required solely to satisfy D1.**

> **This clarification does not require structural discrimination, does not prohibit a separate discriminator value in another representation, and does not select BR3 or any Q2 persistence representation. Where a representation persists both a separate discriminator value and type-specific structural positions, their consistency remains an independent correctness requirement of that realization.**

## 3. Exact effect on accepted D1

This proposal is a **clarification of ambiguity**, not an amendment or supersession.

If accepted, its exact effect would be limited to interpretation of D1's phrases:

- `explicit durable subject-type discriminator`;
- `the discriminator's committed value`;
- `Type qualification within a durable subject identity satisfies this rule`; and
- `physical placement or persistence mechanism of the discriminator`.

It would establish that durable positional/structural qualification can be the discriminator mechanism and can carry the committed type value semantically through the one populated subject-specific position.

It would not change:

- the five current D1 subject types;
- D1's requirement that exactly one current type be identified;
- D2–D5;
- Q2-ST;
- Q2-RI;
- the final Q2 representation;
- FK strategy;
- exclusivity enforcement location;
- actor attribution;
- WP19 scope or implementation authority.

## 4. Why the clarification matters before representation selection

Without this clarification, selecting a BR3 realization without a separate `subject_type` value risks depending on one contested reading of immutable D1.

Adding a separate `subject_type` merely to avoid the ambiguity creates two persisted representations of subject type:

- the discriminator value; and
- the identity of the populated subject-specific slot.

That realization then requires two invariants:

1. exactly one subject slot is populated; and
2. the populated slot agrees with the separate discriminator.

A committed disagreement between those two historical representations would violate the one-subject identity requirements carried by D3/D4 and could not be repaired by mutating committed history under D10 historical-record authority.

The structural reading avoids that additional disagreement class if BR3 is later selected, but it should be made explicit by authority rather than inferred ad hoc.

## 5. Relationship to Q2-EX

Q2-EX remains conditional on BR3.

If this clarification is accepted, Q2-EX may compare BR3 realizations knowing that a subject-specific populated slot can satisfy D1 without a duplicated scalar discriminator.

If the clarification is rejected, a BR3 realization must retain a separate value-bearing discriminator or otherwise demonstrate literal D1 conformity through another accepted mechanism.

No Q2-EX option is accepted by this proposal.

## 6. Decision gate

Project Owner must separately accept, amend, or reject this clarification before a final Q2 representation decision relies on structural/positional qualification as sufficient D1 compliance.

Until then:

**D1 REMAINS ACCEPTED AND UNCHANGED — STRUCTURAL/POSITIONAL QUALIFICATION SUFFICIENCY IS OPEN — Q2-EX REMAINS OPEN — FINAL Q2 REPRESENTATION REMAINS OPEN — WP19 REMAINS BLOCKED / UNAUTHORIZED.**
