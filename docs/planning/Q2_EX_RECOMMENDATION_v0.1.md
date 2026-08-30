# WP19 / Q2-EX Recommendation v0.1

**Status:** Draft — recommendation only  
**Date:** 2026-08-30  
**Subject:** BR3/N3 exclusivity / discriminator consistency  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact recommends; it does not decide Q2-EX or final Q2 representation.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Recommendation

If BR3/N3 is selected as the final Q2 persisted representation, recommend:

**Q2-EX-O1 with database-enforced exactly-one structural qualification.**

That means:

- BR3 does **not** persist a second dedicated `subject_type` column solely to repeat the type already encoded by which subject-specific reference slot is populated;
- exactly one current subject-reference slot must be populated for every committed AuditRecord;
- the identity of that populated slot is the explicit durable subject-type qualification required by accepted D1;
- ordinary DB foreign keys remain available on the five subject-specific relations;
- the exactly-one invariant should be DB-enforced in the concrete BR3 realization where ordinary relational constraints over those slots can provide that protection without a new architectural abstraction.

This recommendation is conditional on BR3 selection. If another representation is selected, Q2-EX should be closed as NOT APPLICABLE.

## 2. Why structural qualification satisfies D1

Accepted D1 says:

> Type qualification within a durable subject identity satisfies this rule.

D1 also explicitly leaves physical placement and persistence mechanism undecided.

In BR3, a subject-specific slot is not generic storage. Its structural identity already names the subject kind. A populated Workspace slot durably qualifies the reference as `Workspace`; a populated Task slot qualifies it as `Task`.

Therefore a separate scalar discriminator is not required merely to satisfy D1 if the exactly-one slot invariant is part of the durable reference contract.

## 3. Why a duplicated discriminator is not preferred

Q2-EX-O2/O3 persist the same logical fact twice:

1. scalar subject type; and
2. structural slot selection.

That creates a new invariant whose only purpose is keeping two encodings of the same historical fact synchronized.

The duplicated form can be made conforming, especially under O2 with a complete DB consistency constraint, but it has costs not demonstrated as necessary by current accepted requirements:

- additional historical contradiction state that must be prevented forever;
- wider consistency constraint;
- duplicated schema evolution when subject kinds change;
- extra migration/test burden;
- no accepted requirement currently demands a scalar `subject_type` column for query ergonomics.

Under the repository's Abstraction Justification Rule, convenience for a hypothetical scalar query is not sufficient reason to introduce duplicated durable state before such a requirement is demonstrated.

## 4. Why DB-enforced exactly-one is preferred for BR3

Unlike a duplicated discriminator, the exactly-one rule is not optional duplication management. It is intrinsic to BR3's ability to represent **one logical audited subject identity** under D4.

Without exactly-one:

- zero populated slots means no subject;
- multiple populated slots mean ambiguous/multiple subjects.

Because the five BR3 relations are persisted relational slots and the invariant concerns only their population state, DB enforcement can protect every persistence path rather than only the audited service path.

Under accepted Q2-RI, this is legitimate comparative credit when implemented as ordinary constraints over the selected representation itself and not through a new persistence abstraction introduced solely to relocate enforcement.

Application/service validation may still duplicate the check for user-facing errors, but it should not be the sole durable enforcement boundary in the recommended BR3 realization.

## 5. Q2-RI effect

If BR3 + recommended Q2-EX is selected, its concrete RI profile becomes:

- ordinary DB FK enforcement for each of the five current subject-specific relations;
- DB-enforced exactly-one population across those relations;
- no discriminator/slot consistency problem because no duplicated discriminator is stored.

This strengthens BR3's concrete integrity story relative to the prior bounded realization, but does **not** by itself select BR3. C1/C4/C5 and comparative complexity against BR1/BR4/BR5 remain part of the final representation decision.

Q2-RI credit remains a comparative input, not a mandatory requirement or automatic winner.

## 6. Queryability consequence

The principal tradeoff is that BR3 no longer has a separately persisted scalar type value.

A query needing subject kind must determine which slot is populated. That may be expressed through query logic or, if a later demonstrated requirement justifies it, through a derived/indexed mechanism.

No generated column, expression index, view, ORM property, or other convenience structure is authorized by Q2-EX. Such structure should be justified by an actual query/operational requirement rather than introduced preemptively.

## 7. Evolution consequence

If a future subject kind is separately authorized under D5/Q2-ST and BR3 remains the persisted representation:

- add the corresponding subject-specific reference form;
- extend the exactly-one invariant;
- preserve historical interpretation of existing records;
- re-apply Q2-RI to the changed concrete realization if DB enforcement characteristics change.

Q2-EX does not itself authorize any future kind.

## 8. Recommended normative rule if BR3 is selected

> **For a BR3/N3 per-type subject-reference representation, the subject type MUST be durably qualified by the identity of the populated subject-specific reference slot. Exactly one authorized subject-reference slot MUST be populated in every committed AuditRecord. No separate persisted subject-type discriminator is required solely to repeat that structural qualification. The exactly-one invariant MUST be enforced at the database persistence boundary where it can be expressed as an ordinary constraint over the selected BR3 representation without introducing a separate architectural abstraction. Application/service validation may additionally enforce the same invariant but MUST NOT be the sole protection against committing zero-subject or multi-subject AuditRecords.**

This rule does not choose column names, SQL syntax, FK delete behavior, index shape, ORM mappings, migration details, or future subject kinds.

## 9. Decision gate

Q2-EX remains OPEN until Project Owner acceptance or until a non-BR3 final representation makes it NOT APPLICABLE.

No final Q2 representation is selected by this recommendation. WP19 remains BLOCKED / UNAUTHORIZED.
