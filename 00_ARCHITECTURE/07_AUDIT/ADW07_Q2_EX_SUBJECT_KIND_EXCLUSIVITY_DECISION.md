# ADW-07 / Q2-EX — Subject-Kind Exclusivity and Qualification Decision

**Identifier:** Q2-EX  
**Workshop:** ADW-07 — Events, Audit, and Provenance  
**Workshop Status:** OPEN  
**Decision:** Q2-EX — how a per-type-path realization guarantees exactly one audited subject kind, and whether a separate persisted scalar kind token is required  
**Decision Status:** ACCEPTED — CONDITIONAL  
**Decision Owner / Authority / Decider:** Project Owner / Andrew  
**Decision Date:** 2026-09-01  
**Accepted option:** Q2-EX-O1 — structural qualification with database-enforced exactly-one  
**Conditionality:** BR3/N3-conditional. See Conditionality below.

## Conditionality

Q2-EX arises only for a persisted representation that carries the audited subject
through several type-specific reference paths. This decision therefore takes effect
only if the separate Q2 persisted-representation decision selects BR3/N3.

**This decision does not select, endorse, approve, or favour BR3/N3, and must not be
read as making its selection more likely.** It states what a per-path realization
would have to guarantee if one were chosen. The representation decision is separate,
open, and unaffected by this record.

If that decision selects a non-BR3/N3 representation, Q2-EX closes as **NOT
APPLICABLE** and nothing in this record has effect. Conditional and
inoperative-until clauses are already established in this corpus: accepted Q2-ST
carries a permission expressly inoperative until the Q2 representation contract is
accepted, and ADR-0015 establishes a default whose consequences depend on later
per-specialization decisions.

## Decision

**Where the selected Q2 persisted representation carries the audited subject through
type-specific reference paths, the subject kind is qualified structurally — by which
authorized reference path is populated — and no separate persisted scalar subject-kind
token is required or added.**

**Exactly one authorized subject-reference path is populated for every committed
AuditRecord. That guarantee is enforced at the database persistence boundary,
expressed directly over the selected representation's own persisted columns, and not
through an added persistence abstraction.**

**The exact constraint expression, column structure, indexes, and migration mechanism
remain outside this decision and require the later Q2 representation decision.** This
record states a required property and the layer at which it is guaranteed; it
prescribes no schema.

This satisfies accepted D1 under the property test established by `D1-CLAR-01`: the
subject kind is explicit (determinable from the persisted record alone), determinate
(the exactly-one guarantee yields one kind and only one), and durable and stable (the
determination does not change for a committed record), consistent with D3 and D4.

## Disposition of the exposed option set

The Q2-EX option set exposed in
`docs/planning/Q2_EX_BR3_EXCLUSIVITY_DISCRIMINATOR_OPTIONS_v0.1.md` is disposed of in
full. Historical identifiers O1–O4 keep their original meanings and are not
reassigned.

**Q2-EX-O1 — structural qualification, no separate discriminator. ACCEPTED**, subject
to the conditionality above.

**Q2-EX-O2 — separate discriminator with database-enforced exactly-one and match.
REJECTED.** After `D1-CLAR-01` a scalar token is not required for D1 conformity.
Carrying the kind in two places makes one historical fact a pair of statements that
must agree for every committed record, forever, adding a second permanent invariant
whose failure produces a contradictory committed record that D3, D4, and D10 §7.4
leave unrepairable. Its remaining demonstrated benefit is query ergonomics, and no
accepted authority makes scalar kind-only querying a requirement.

**Q2-EX-O3 — separate discriminator with application/service-enforced exactly-one and
match. REJECTED.** O3 carries O2's duplication and its second permanent invariant
while moving the guarantee off the persistence boundary, so every write path —
including future ones, migrations, and repair scripts — becomes individually
responsible for a condition on which the record's historical validity depends. O3 is
rejected on the grounds that reject O2, with the enforcement locus widening the
exposure rather than narrowing it.

**Q2-EX-O4 — separate discriminator without a mandatory exactly-one or match
invariant. EXCLUDED AS NON-CONFORMING.** This is not a comparative rejection. Without
a guaranteed exactly-one condition the persisted state can present zero or several
populated paths, so the subject kind is not determinate: `D1-CLAR-01` property 2 fails,
and accepted D4's requirement that the record identify one logical audited subject
fails with it. O4 is excluded by accepted authority rather than by preference, and no
realization relying on it may be selected.

**Q2-EX-O5 — derived, non-independently-writable kind projection. NOT AUTHORIZED;
DEFERRED, not rejected.** O5 is not an alternative to O1–O4 but an augmentation of O1:
it presupposes structural qualification and adds a database-derived column computing
the kind from which reference path is populated. It would provide the scalar query
ergonomics of O2/O3 without their agreement invariant, because a derived value is not
independently written and cannot disagree with the state it is computed from. It adds
nothing to the durable subject-identity contract.

It is not authorized now because no query workload has been observed that requires it:
WP19 has no implementation, no audit rows exist, and the need is predicted rather than
demonstrated. Deferring it is inexpensive and reversible precisely because it adds no
independently written state — introducing it later changes no committed fact and
creates no historical-consistency obligation, unlike O2 and O3.

**Reopen condition for O5:** a demonstrated query or operational requirement for
kind-as-a-value retrieval that derived logic over the reference paths does not serve
acceptably in practice. Until then no derived column, index, or projection mechanism
is approved by this decision.

**Identifier note.** O5 is a newly exposed option, assigned the next free identifier so
that the historical meanings of O1–O4 are preserved exactly as recorded. No earlier
identifier is reused, renamed, or reinterpreted by this decision.

## Position under accepted Q2-RI

Accepted Q2-RI governs the architectural weight of database-enforced **referential**
integrity — enforcement of the relationship between the persisted subject reference
and the referenced subject identity in another table.

The exactly-one guarantee is a different kind of condition: a property of a single
committed record's own fields, not of its relationship to another table. Neither it nor
O2's token/path agreement invariant is referential integrity.

Every option above offers the identical per-path foreign-key opportunity to the five
current subject targets. **Accepted Q2-RI is therefore neutral across the Q2-EX option
set and did not decide this question.** This decision rests on historical-state
integrity, on the enforcement locus, and on the absence of a demonstrated requirement
for a second stored representation — not on Q2-RI credit.

## Accepted consequences

**Kind as a projected value is derived.** Filtering by a known subject kind remains
direct and indexable, since it is a predicate over one reference path. What becomes
derived is returning or grouping by the subject kind as a value, which requires logic
over the authorized reference paths. `docs/adr/0005-audit-first-mutations.md` expects
the audit trail to remain queryable; this cost is accepted knowingly, and O5's reopen
condition above is the route if practice shows it to be too high.

**Expansion of the authorized kind set is bounded.** Where a further subject kind is
authorized under accepted D5 and Q2-ST, expansion adds one authorized reference path
and extends the exactly-one guarantee. Committed records are not rewritten and their
subject kinds remain determined by the path already populated, satisfying D3 and D4.
Only one representation of kind evolves, because only one exists.

## Relationship to accepted authority

This decision does not amend, supersede, reinterpret, or edit D1, `D1-CLAR-01`, D2–D5,
Q2-RI, Q2-ST, or ADR-0015; their canonical authority remains exclusively in their own
records. It applies the `D1-CLAR-01` property test to a per-path realization and decides
only what that realization must guarantee and what it need not carry.

## Explicit non-decisions

This decision does not:

- select, endorse, or favour BR3/N3 or any Q2 persisted representation;
- reject BR1, BR2, BR4, or BR5;
- define columns, column names, types, constraint expressions, indexes, migrations, ORM
  mappings, or repository/service APIs;
- decide foreign-key delete actions, cascade behavior, or subject-deletion permission;
- authorize a derived kind projection, a registry, or any resolver infrastructure;
- authorize a sixth subject kind or any mapping exception under accepted Q2-ST;
- decide GC-006 audit qualification, GC-007 content shape, or actor attribution /
  ActorContext persistence semantics;
- approve the WP19 scope amendment;
- authorize any WP19 model, migration, repository, service, API, or test work.

## Current state

- D1 and `D1-CLAR-01`: **CLOSED — ACCEPTED**, unaffected;
- D2–D5: **CLOSED — ACCEPTED**, unaffected;
- Q2-RI: **CLOSED — ACCEPTED — O2 PREFERENCE**, unaffected;
- Q2-ST: **CLOSED — ACCEPTED — O2**, unaffected;
- Q2-EX: **CLOSED — ACCEPTED — O1, conditional on BR3/N3 selection**;
- Q2-EX-O2, O3: **REJECTED**; O4: **EXCLUDED AS NON-CONFORMING**; O5: **DEFERRED**;
- Q2 persisted representation: **OPEN / NOT ESTABLISHED**;
- BR3/N3: **NOT SELECTED**;
- WP19 scope amendment: **NOT YET APPROVED**;
- actor attribution / ActorContext: **OPEN**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED**.

## Next bounded step

Re-apply accepted D1–D5, Q2-RI, Q2-ST, and this decision to candidates N1–N5, testing
each for D1–D5 conformity, Q2-EX applicability, database-enforced referential integrity
under Q2-RI, whether an exactly-one guarantee is required of it, migration cost and
historical immutability, and the absence of unjustified abstraction. Only then prepare
the separate Q2 persisted-representation decision. WP19 planning and status are updated
separately, after that decision. This record authorizes no implementation.
