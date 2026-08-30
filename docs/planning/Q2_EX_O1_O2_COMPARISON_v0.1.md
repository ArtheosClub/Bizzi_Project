# WP19 / Q2-EX — O1 vs O2 Comparison v0.1

**Status:** Draft — bounded comparative analysis only  
**Date:** 2026-08-30  
**Subject:** BR3/N3 — structural qualification versus duplicated scalar discriminator  
**Authority:** None. This artifact compares Q2-EX-O1 and Q2-EX-O2; it does not select BR3 or final Q2 representation.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Compared realizations

### Q2-EX-O1 — structural qualification

- five subject-type-specific nullable reference slots;
- exactly one slot populated for every committed AuditRecord;
- subject kind is the identity of the populated slot;
- no separate persisted scalar `subject_type` token;
- ordinary FK integrity remains available per slot;
- exactly-one must be durably enforced if BR3 is selected.

### Q2-EX-O2 — duplicated scalar discriminator

- the same five subject-type-specific nullable reference slots;
- a separate persisted scalar `subject_type` token;
- exactly one slot populated;
- the populated slot must agree with `subject_type`;
- ordinary FK integrity remains available per slot;
- both exactly-one and discriminator/slot agreement must be durably enforced if BR3 is selected.

## 2. Accepted-authority conformity

Accepted `D1-CLAR-01` establishes that D1 is a property requirement, not a mechanism requirement. Structural qualification is conforming when the persisted subject reference alone makes the kind explicit, determinate, durable, and stable. O1 therefore does not need a scalar type token merely for D1 compliance.

O2 also conforms to D1, but carries subject kind twice: once in the scalar token and once structurally in slot identity. Under `D1-CLAR-01`, those two representations must agree for every committed record.

Both options can satisfy D3/D4. The difference is the number of historical consistency conditions that must remain true forever.

## 3. Historical-integrity comparison

### O1

O1 has one durable representation of subject kind. Its critical invariant is:

> exactly one authorized subject-reference slot is populated.

If that invariant holds, the record has one subject identity and one subject kind. There is no separate discriminator/slot contradiction state.

### O2

O2 has two durable representations of subject kind. Its critical invariants are:

1. exactly one authorized subject-reference slot is populated; and
2. the populated slot agrees with the scalar discriminator.

The second invariant exists only because the same historical fact is stored twice. A failure of that invariant creates a contradictory committed historical record that cannot later be repaired by reinterpretation or mutation consistently with D3/D4/D10 §7.4.

**Comparative result:** O1 is structurally safer because it removes an entire class of invalid historical states rather than merely enforcing against them.

## 4. Q2-RI comparison

Both O1 and O2 preserve the same ordinary per-slot FK opportunity to the five current subject targets.

O1 additionally requires an exactly-one persistence invariant. Where expressed as an ordinary DB constraint over the selected BR3 columns, that enforcement is part of the representation itself and does not introduce a separate architectural abstraction. It therefore qualifies for positive per-realization Q2-RI consideration.

O2 requires both exactly-one and discriminator/slot agreement. Those constraints can likewise receive DB-integrity credit when implemented directly over the selected representation.

Q2-RI does not create a preference for duplicated state merely because the DB can enforce its consistency. Enforcement credit rewards integrity of a realization; it does not reward adding an avoidable second representation of the same fact.

**Comparative result:** DB-RI does not offset O2's duplication burden. O1 obtains a complete integrity story with fewer independent invariants.

## 5. Queryability comparison

### O1 cost

A query asking only for subject kind cannot read one scalar token. It must determine which of the five type-specific slots is populated.

Consequences:

- cross-type audit queries need derived type logic;
- scalar type filtering is less direct;
- indexing a single type token is not immediately available;
- a future generated/derived/indexed convenience mechanism may be justified if actual query workloads demonstrate the need, but Q2-EX should not pre-authorize one.

This is a real C1/read-query cost and must be recorded in any final BR3 decision because ADR-0005 expects the audit trail to remain queryable.

### O2 benefit

O2 provides direct scalar type filtering and simpler type-only indexing/query predicates.

However, the query convenience is obtained by persisting the same historical fact twice and introducing the agreement invariant.

**Comparative result:** O2 is better for scalar type-query ergonomics; O1 is better for historical-state minimality and integrity. No accepted authority makes scalar type-only query convenience a mandatory requirement.

## 6. Evolution comparison

If a sixth subject kind is separately authorized under D5/Q2-ST and BR3 remains selected:

### O1

- add one new type-specific subject-reference slot;
- extend the exactly-one invariant;
- existing committed rows remain unchanged;
- their subject kinds remain determined by their already-populated slots.

### O2

- add the new type-specific slot;
- add/authorize the new scalar discriminator value;
- extend exactly-one;
- extend discriminator/slot agreement logic;
- existing committed rows can remain unchanged, but the duplicated type contract and its consistency logic become wider.

Both options can preserve D3/D4 during expansion. O1 has the smaller evolution surface because only one representation of type evolves.

## 7. Abstraction-justification comparison

O1 contains no additional durable state solely for convenience. Its exactly-one invariant is necessary for BR3 to represent one audited subject.

O2's scalar discriminator is not necessary for D1 after `D1-CLAR-01`; its remaining demonstrated benefit is query ergonomics. The current corpus does not establish a requirement that AuditRecord subject kind must be retrievable through a dedicated scalar token.

Under the repository Abstraction Justification Rule, anticipated convenience alone is weak justification for adding duplicated durable historical state and the invariant required to keep it synchronized.

This does not make O2 non-conforming. It makes O1 the narrower realization unless a demonstrated query/operational requirement later justifies the duplicated token.

## 8. Comparison matrix

| Dimension | O1 Structural qualification | O2 Scalar discriminator + slots |
|---|---|---|
| D1 / D1-CLAR-01 | PASS | PASS |
| D3/D4 | PASS with exactly-one | PASS with exactly-one + match |
| Durable representations of type | 1 | 2 |
| Required independent invariants | 1 | 2 |
| Contradictory type-state class | Structurally absent | Must be prevented forever |
| Per-slot DB FK opportunity | Same | Same |
| DB exactly-one opportunity | Yes | Yes |
| Additional DB match constraint | No | Yes |
| Scalar type-only queries | Derived | Direct |
| New-kind evolution | Slot + exactly-one | Slot + token value + exactly-one + match |
| Historical-state minimality | Stronger | Weaker |
| Current demonstrated need for extra token | None | None beyond query convenience |

## 9. Bounded recommendation

**If BR3/N3 is selected as the final Q2 persisted representation, prefer Q2-EX-O1 — structural qualification with DB-enforced exactly-one — over Q2-EX-O2.**

Reason:

O1 satisfies the accepted D1 property test, preserves the same per-target FK opportunities, can enforce the one-subject condition at the DB persistence boundary, and removes the discriminator/slot disagreement state entirely. O2's principal benefit is simpler scalar subject-type querying, but no accepted requirement currently justifies paying for that convenience with duplicated immutable historical state and an additional permanent consistency invariant.

This is a BR3-conditional recommendation only. It does not select BR3 over BR1/BR4/BR5 and does not authorize implementation.

## 10. Decision consequence

If final Q2 representation selects BR3, the same authority should close Q2-EX by accepting O1 unless Project Owner separately chooses O2 based on a demonstrated query/operational requirement.

If final Q2 representation selects a non-BR3 representation, Q2-EX should close as NOT APPLICABLE.

WP19 remains BLOCKED / UNAUTHORIZED after this analysis.
