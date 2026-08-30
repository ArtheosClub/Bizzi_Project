# WP19 / Q2 Post-D1–D5 Candidate Re-application v0.1

**Status:** Suspended — evaluation retained; ranking/recommendation withdrawn pending Q2-RI  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 — re-application of accepted D1–D5 to normalized persistence candidates N1–N5  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact is evaluation material only.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

> **Suspension note — 2026-08-30:** The original version of this artifact recommended N1 over N3. Subsequent review established that the ranking relied on an unresolved decision surface: whether DB-enforced referential integrity is an architecture requirement, a preference, or neither. The approved evaluation framework originally labeled that surface `D4`; because `D4` is now the accepted Subject Reference Semantics decision, the unresolved RI surface is reconciled under the identifier **Q2-RI**. Until Q2-RI is decided, the original `N1 > N3` ranking is withdrawn. The underlying descriptive evaluation is retained as input, not authority.

## 1. Controlling state

D1–D5 are CLOSED / ACCEPTED through separate canonical ADW-07 authority artifacts. They establish explicit durable type qualification, Workspace subject/context separation, historical identity survival, mandatory durable subject-reference semantics, and the current five-type Q2 acceptance scope.

They do **not** establish whether DB-enforced referential integrity is:

- a mandatory requirement;
- a comparative preference;
- or neither.

That unresolved weighting is now **Q2-RI**.

A second gap, **Q2-ST**, concerns the architecture-level rule that determines the admissible subject-type discriminator vocabulary. Q2-ST does not by itself change the current five-type evaluation set and does not establish `AgentDefinition` as a sixth type.

## 2. Candidate findings that remain valid

### N1 — Polymorphic reference

**D1–D5 conformity outlook: strong.**

A conforming N1 realization can carry one explicit durable subject type plus one stable subject identifier and can preserve historical interpretation after live dereference becomes unavailable.

Remaining burdens:

- validation and durable resolution semantics must be explicit;
- conventional cross-table DB FK enforcement is not inherent;
- exact physical fields and enforcement location remain undecided.

### N2 — Composite FK

**Current documented form: not sufficient for the complete five-type Q2 scope.**

GC-002 Alternative B documents a composite `(workspace_id, id)` pattern for named relationships, including a single AuditRecord→aggregate formulation. It does not by itself provide a complete five-type subject-reference representation across structurally asymmetric subjects.

A broader composite-FK design may be possible, but it would be additional design and must not be treated as already approved GC-002 Alternative B.

### N3 — Per-type nullable relations / slots

**D1–D5 conformity outlook: strong.**

A conforming N3 realization can use subject-type-specific persisted paths while preserving one logical audited subject. It requires an explicit exclusivity/cardinality rule so that multiple physical paths cannot create ambiguous subject identity.

Remaining burdens:

- wider/sparser persistence surface;
- explicit exclusivity enforcement is required somewhere;
- cross-type queries are likely more complex;
- future authorized subject types may require schema evolution, which accepted D5 permits.

### N4 — Opaque identifier

**Conforming only with material qualification.**

A bare opaque identifier is insufficient under D1/D4. A conforming form also requires explicit accepted subject type plus a durable, stable resolution convention. That introduces resolver/namespace semantics not otherwise required by current authority.

### N5 — In-payload subject identity

**Conforming only with material qualification.**

ADR-0014 permits subject identification inside persisted AuditRecord content, but D4 prohibits inferring subject identity from generic payload/diff/context. A conforming N5 therefore needs an explicit mandatory subject-identity contract inside persisted content, including D1 type semantics and stable identifier meaning.

## 3. Corrected comparative position

| Candidate | D1–D5 conformity outlook | Principal unresolved burden | Current position |
|---|---|---|---|
| N1 Polymorphic reference | Strong | enforcement / resolution mechanics | **UNDETERMINED vs N3 — Q2-RI REQUIRED** |
| N2 Composite FK | Incomplete as documented | five-type structural adaptation | **Do not select as documented** |
| N3 Per-type nullable relations | Strong | exclusivity + wider schema | **UNDETERMINED vs N1 — Q2-RI REQUIRED** |
| N4 Opaque identifier | Conditional | resolver / namespace contract | **Viable but carries extra semantic infrastructure** |
| N5 In-payload | Conditional | content contract + query/integrity burden | **Viable but carries extra semantic infrastructure** |

## 4. Why the original N1 ranking is withdrawn

The original recommendation used two true observations:

1. D4 describes one logical audited-subject identity.
2. N3 commonly realizes that identity through multiple physical subject-specific paths.

The invalid step was treating the second observation as a comparative disadvantage by itself. D4 establishes semantic singularity, not physical singularity. A valid N3 realization may expose multiple physical relations while still satisfying exactly one logical subject identity.

Therefore physical-path multiplicity cannot rank N1 over N3 without an additional architecture preference.

The other important differentiator is referential-integrity enforcement:

- N3 can naturally support DB-native per-type FK enforcement;
- N1 commonly relies on application/domain validation or additional structure for multi-table resolution.

Existing authority does not yet say whether that DB-native property is required, preferred, or neutral. Therefore the pair is correctly classified:

**N1 vs N3 — UNDETERMINED — Q2-RI DECISION REQUIRED.**

## 5. Q2-ST boundary

This artifact does not decide the rule by which subject-type discriminator values are derived.

The current five values remain the accepted D1/D5 current Q2 scope. The existence of standalone D02 specializations such as AgentDefinition exposes a future/current applicability gap, but does not establish either:

- that `AgentDefinition` is a sixth subject type; or
- that `EnterpriseObject` automatically resolves every standalone specialization.

That rule is a separate bounded surface, **Q2-ST**.

Q2-ST must be closed before final Q2 representation authority, but it does not by itself restore the withdrawn N1>N3 ranking.

## 6. Explicit non-decisions

This artifact does not:

- recommend or approve N1;
- recommend or approve N3;
- reject N2–N5 as architecture authority;
- decide Q2-RI;
- decide Q2-ST;
- approve GC-002 Alternative B;
- choose exact fields, FK policy, CHECK constraints, indexes, resolver APIs, migration, repository, service, or API design;
- define actor attribution / ActorContext persistence semantics;
- restore WP18 → WP19 dependency;
- authorize WP19 implementation;
- close ADW-07.

## 7. Gate result

**POST-D1–D5 DESCRIPTIVE EVALUATION RETAINED — ORIGINAL N1 RECOMMENDATION SUSPENDED — N1 VS N3 UNDETERMINED PENDING Q2-RI — Q2-ST REMAINS SEPARATE — NO REPRESENTATION AUTHORITY ESTABLISHED.**

Current state:

- D1–D5: **CLOSED — ACCEPTED**;
- Q2-RI: **OPEN**;
- Q2-ST: **OPEN**;
- N1 vs N3: **UNDETERMINED — Q2-RI DECISION REQUIRED**;
- Q2 persisted representation: **OPEN / NOT ESTABLISHED**;
- N1–N5: **UNAPPROVED**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- actor attribution / ActorContext: **SEPARATE / UNRESOLVED**;
- WP18 dependency: **NOT RESTORED**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED**.
