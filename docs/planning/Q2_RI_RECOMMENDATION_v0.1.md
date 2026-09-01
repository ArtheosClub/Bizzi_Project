# WP19 / Q2-RI Recommendation v0.1

**Status:** Draft — recommendation only  
**Date:** 2026-08-30  
**Subject:** Q2-RI — architectural weight of DB-enforced referential integrity  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact recommends; it does not decide Q2-RI.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Decision surface

Q2-RI asks:

> For the persisted AuditRecord subject-reference representation, what architectural weight, if any, should DB-enforced referential integrity receive: mandatory requirement, comparative preference, or neither?

The options are defined in `Q2_RI_REFERENTIAL_INTEGRITY_WEIGHT_OPTIONS_v0.1.md`.

## 2. Recommendation

**Recommend Q2-RI-O2 — DB-enforced referential integrity is a PREFERENCE, not a REQUIREMENT.**

Recommended rule:

> **Compliance with the accepted AuditRecord subject-reference semantics is mandatory. Among otherwise conforming persisted representations, stronger DB-enforced referential integrity is a legitimate comparative advantage and SHOULD be preferred where it can be obtained without introducing disproportionate structural indirection or contradicting other accepted architecture constraints. Lack of ordinary database foreign-key enforcement is not by itself disqualifying when durable correctness, validation, and historical subject resolvability are established through another explicit mechanism. DB-enforced referential integrity is therefore a comparative preference, not a universal Q2 requirement.**

## 3. Why O2 is preferred

### 3.1 O1 REQUIREMENT is stronger than demonstrated need

No accepted authority establishes database enforcement as mandatory. Elevating it to a hard requirement would force every Q2 representation to provide a complete DB-native target constraint across structurally asymmetric subject types.

For conventional polymorphic multi-table references, that could require registry/base-table indirection or other additional persistence structure solely to satisfy enforcement location. The repository's abstraction discipline does not justify introducing such structure without a demonstrated need.

A database constraint is valuable, but its value does not by itself prove that every correct architecture must locate the invariant in the database.

### 3.2 O3 NEITHER discards a real correctness advantage

The opposite extreme is also too weak. Where an ordinary FK or equivalent DB constraint can cheaply prevent dangling or malformed subject references, that property is materially useful.

Treating DB-native enforcement as architecturally irrelevant would force the comparison to ignore a real correctness boundary even when two candidates are otherwise conforming.

The approved framework already treats integrity characteristics as a legitimate comparative dimension. O2 gives that dimension weight without turning it into a universal gate.

### 3.3 O2 restores a fair N1 vs N3 comparison

Before Q2-RI, N1 and N3 are correctly `UNDETERMINED — Q2-RI DECISION REQUIRED` for ranking.

Under O2:

- N1 may remain fully admissible if it establishes explicit durable validation/resolution semantics despite lacking ordinary cross-table FK enforcement;
- N3 gains a legitimate comparative strength if its type-specific relations permit straightforward DB-native FK enforcement;
- N3 does not automatically win, because the comparison must still include query shape, exclusivity semantics, schema width/evolution, migration cost, and historical-interpretation stability;
- N1 does not automatically win merely because D4 defines one logical subject identity.

This is the decision weight the previous post-D1–D5 recommendation lacked.

### 3.4 O4 should remain an escape hatch, not the baseline

Context-dependent weighting could be justified if concrete subject types demonstrate materially different integrity requirements. No accepted authority currently supplies such a per-type policy.

Choosing O4 now would create another rule-definition step before the comparison can proceed. O2 already accommodates structural asymmetry because a candidate can receive comparative credit wherever DB-native enforcement is actually available without making it mandatory everywhere.

## 4. Boundaries

If accepted, O2 would NOT:

- select N1 or N3;
- approve N2 or GC-002 Alternative B;
- require a foreign key for every subject type;
- define FK delete actions;
- define exactly-one/exclusivity constraints for N3;
- choose database versus application validation for a concrete representation;
- define a resolver for N1/N4;
- decide Q2-ST;
- alter D1–D5;
- authorize WP19 implementation.

## 5. Required identifier reconciliation in the future authority

The accepted ADW-07 decision-record lifecycle authority prohibits rewriting earlier accepted D1/D2 records in place.

Therefore the future Q2-RI authority must state explicitly:

> **Historical references in earlier Q2 decision records to `D4 — DB-enforced referential integrity` refer to the unresolved decision surface now identified as `Q2-RI`. They do not refer to the later accepted `D4 — Subject Reference Semantics` decision. This clause reconciles identifiers only and does not change the substantive meaning of the earlier accepted records.**

This reconciliation is required governance housekeeping attached to the Q2-RI authority, not a new persistence decision.

## 6. Decision gate

**Recommendation ready for Project Owner decision: Q2-RI-O2 — PREFERENCE.**

Until explicitly accepted:

- Q2-RI remains OPEN;
- N1 vs N3 remains UNDETERMINED;
- the suspended post-D1–D5 ranking remains suspended;
- Q2 persisted representation remains OPEN;
- WP19 remains BLOCKED / UNAUTHORIZED.
