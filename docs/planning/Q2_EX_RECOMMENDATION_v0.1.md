# WP19 / Q2-EX Recommendation v0.1

**Status:** Draft — recommendation only  
**Date:** 2026-08-30  
**Subject:** BR3/N3 exclusivity / discriminator consistency  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact recommends; it does not decide Q2-EX or final Q2 representation.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Recommendation

If BR3/N3 is selected as the final Q2 persisted representation, recommend:

**Q2-EX-O1 with database-enforced exactly-one structural qualification, conditional on separate accepted clarification that this structural/positional qualification satisfies D1.**

That means:

- BR3 does **not** persist a second dedicated `subject_type` column solely to repeat the type already encoded by which subject-specific reference slot is populated;
- exactly one current subject-reference slot must be populated for every committed AuditRecord;
- subject type is represented by the durable structural identity of that populated slot, subject to the separate D1 clarification gate;
- ordinary DB foreign keys remain available on the five subject-specific relations;
- the exactly-one invariant should be DB-enforced in the concrete BR3 realization where ordinary relational constraints over those slots can provide that protection without a new architectural abstraction.

This recommendation is conditional on BR3 selection **and** on accepted D1 clarification. If another representation is selected, Q2-EX should be closed as NOT APPLICABLE.

## 2. D1 clarification prerequisite

Accepted D1 requires an `explicit durable subject-type discriminator`, states that the discriminator's committed value must identify exactly one current Q2 subject type, permits `Type qualification within a durable subject identity`, and leaves physical placement / persistence mechanism open.

For BR3 positional qualification, two readings remain defensible:

1. the one populated subject-specific structural position is itself the discriminator mechanism and its structural qualification carries the committed type value; or
2. D1 requires a separately represented value-bearing discriminator component, so positional qualification alone is insufficient.

Q2-EX must not silently choose between those readings.

The repository therefore carries a separate decision-ready clarification proposal:

`docs/planning/Q2_D1_STRUCTURAL_DISCRIMINATOR_CLARIFICATION_PROPOSAL_v0.1.md`

Until that clarification is accepted, Q2-EX-O1 remains a preferred **conditional** realization rather than an established D1-conforming one.

## 3. Why a duplicated discriminator is not preferred

Q2-EX-O2/O3 persist the same logical fact twice:

1. scalar subject type; and
2. structural slot selection.

That creates two distinct correctness obligations:

1. exactly one subject slot is populated; and
2. the populated slot agrees with the scalar discriminator.

The second obligation exists only because subject type is durably encoded twice. A committed disagreement between those encodings would make the historical AuditRecord internally contradictory. Under D3/D4 that would undermine stable one-subject identity, and under D10 historical-record immutability it could not be repaired by mutating the committed record.

The duplicated form can be made conforming, especially under O2 with a complete DB consistency constraint, but it has costs not demonstrated as necessary by current accepted requirements:

- an additional historical contradiction state that must be prevented forever;
- a wider consistency constraint;
- duplicated schema evolution when subject kinds change;
- extra migration/test burden;
- no accepted requirement currently demands a scalar `subject_type` column for query ergonomics.

The advantage of structural qualification is therefore not merely saving one column. It removes an entire class of discriminator/slot divergence states.

## 4. Why DB-enforced exactly-one is preferred for BR3

Unlike a duplicated discriminator, the exactly-one rule is not optional duplication management. It is intrinsic to BR3's ability to represent **one logical audited subject identity** under D4.

Without exactly-one:

- zero populated slots means no subject;
- multiple populated slots mean ambiguous/multiple subjects.

Because the five BR3 relations are persisted relational slots and the invariant concerns only their population state, DB enforcement can protect every persistence path rather than only the audited service path.

Under accepted Q2-RI, this is legitimate comparative credit when implemented as an ordinary constraint over the selected representation itself and not through a new persistence abstraction introduced solely to relocate enforcement.

Application/service validation may still duplicate the check for user-facing errors, but it should not be the sole durable enforcement boundary in the recommended BR3 realization.

## 5. Q2-RI effect

If BR3 + recommended Q2-EX is selected after D1 clarification, its concrete RI profile becomes:

- ordinary DB FK enforcement for each of the five current subject-specific relations;
- DB-enforced exactly-one population across those relations;
- no discriminator/slot consistency problem because no duplicated discriminator is stored.

This strengthens BR3's concrete integrity story relative to the prior bounded realization, but does **not** by itself select BR3. C1/C4/C5 and comparative complexity against BR1/BR4/BR5 remain part of the final representation decision.

Q2-RI credit remains a comparative input, not a mandatory requirement or automatic winner.

## 6. Queryability consequence

The principal explicit tradeoff is that BR3 would not carry a separately persisted scalar type token.

A query asking only `what subject type does this AuditRecord reference?` must inspect the five subject-reference positions rather than read one scalar discriminator value. Cross-type audit queries and indexing therefore carry higher expression/planning complexity than a design with a dedicated scalar type value.

This matters because ADR-0005 requires the audit trail to be authoritative and queryable. It is a real comparative cost, not a blocker and not a reason by itself to duplicate durable type state.

No generated column, expression index, view, ORM property, materialized projection, or other convenience structure is authorized by Q2-EX. Such structure should be justified by an actual query/operational requirement rather than introduced preemptively.

## 7. Evolution consequence

If a future sixth subject kind is separately authorized under D5/Q2-ST and BR3 remains the persisted representation:

- add the corresponding subject-specific reference form;
- extend the exactly-one invariant to include that form;
- existing committed rows do not require their subject identity to be rewritten, because their type remains determined by the subject-specific position already populated;
- preserve historical interpretation of existing records;
- re-apply Q2-RI to the changed concrete realization if DB enforcement characteristics change.

Thus current historical rows remain stable under ordinary subject-kind-set growth. The schema evolves, but D3/D4 identity of already committed records need not be reinterpreted.

Q2-EX does not itself authorize any future kind.

## 8. Recommended normative rule if BR3 is selected

Subject to prior accepted D1 clarification:

> **For a BR3/N3 per-type subject-reference representation, the subject type MUST be durably qualified by the identity of the populated subject-specific reference slot. Exactly one authorized subject-reference slot MUST be populated in every committed AuditRecord. No separate persisted subject-type discriminator is required solely to repeat that structural qualification. The exactly-one invariant MUST be enforced at the database persistence boundary where it can be expressed as an ordinary constraint over the selected BR3 representation without introducing a separate architectural abstraction. Application/service validation may additionally enforce the same invariant but MUST NOT be the sole protection against committing zero-subject or multi-subject AuditRecords.**

This rule does not choose column names, SQL syntax, FK delete behavior, index shape, ORM mappings, migration details, or future subject kinds.

## 9. Decision gate

Sequence required before relying on this recommendation:

1. accept/reject/amend the separate D1 structural-discriminator clarification;
2. then, if BR3 is selected, close Q2-EX in the same final representation authority;
3. if a non-BR3 representation is selected, close Q2-EX as NOT APPLICABLE.

No final Q2 representation is selected by this recommendation. WP19 remains BLOCKED / UNAUTHORIZED.
