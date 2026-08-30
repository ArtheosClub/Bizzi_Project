# WP19 / Q2 D5 Subject-Type Set / Extensibility Options v0.1

**Status:** Draft — D5 options/evaluation only  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 / D5 — current subject-type set and future extensibility requirement  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact structures and evaluates D5 options; it does not decide D5.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit authorization of an interim shape.

## 1. D5 bounded question

**For ADR-0014 Q2, is the architecture requirement limited to the five currently supported audited-subject types, or must the persisted subject-reference representation also preserve an explicit architecture-level capability to add future auditable subject types without redefining the accepted D1–D4 semantic contract?**

D5 is an extensibility-requirement decision. It is not a persistence-shape decision.

## 2. Authority already fixed by D1–D4

D5 inherits and MUST NOT redefine:

- **D1:** each committed subject reference has an explicit durable subject-type discriminator identifying exactly one current Q2 subject type.
- **D2:** `Workspace` is a first-class subject type; context does not substitute for subject identity.
- **D3:** historical audited-subject identity survives later lifecycle change and does not depend on live dereference.
- **D4:** subject identity is mandatory, durable, explicit, stable, independently resolvable, and distinct from actor attribution / ActorContext / context / association / route / payload.

The five current D1 subject types are:

- `Workspace`;
- `EnterpriseObject`;
- `User`;
- `WorkspaceMembership`;
- `Task`.

D5 does not add a sixth type and does not change the current D1 accepted discriminator values.

## 3. D5 semantic surfaces

D5 evaluates only the following architecture questions:

1. **Current-set sufficiency:** is satisfying the five current types enough for Q2 acceptance?
2. **Future-type admissibility:** may future architecture add another auditable subject type under a separate explicit decision?
3. **Contract continuity:** if future types are added, must they satisfy the same D1–D4 subject-reference invariants?
4. **Representation adaptability:** is the selected Q2 representation required now to accommodate future types without a representation migration/redesign, or is later explicit change acceptable?
5. **Authority boundary:** does D5 itself authorize any future type? It must not.

## 4. Options

### D5-O1 — Closed five-type architecture

**Rule:** Q2 architecture defines the audited-subject universe as permanently limited to the current five types. Any sixth type is architecturally prohibited unless D5 itself is reopened/replaced.

**Evaluation: NOT RECOMMENDED.**

The current corpus establishes five types as the present Q2 scope, but no accepted authority establishes them as a permanent closed universe. Making the set permanently closed would create a new restriction not required by D1–D4.

### D5-O2 — Current five types are sufficient for Q2; future types require separate explicit architecture decision

**Rule:** Q2 acceptance requires complete support for the current five subject types. Future auditable subject types may be introduced only by separate explicit architecture authority. A future type must conform to the accepted D1–D4 semantic contract, but D5 does not require the current persistence representation to support every hypothetical future type without later schema/representation evolution.

**Evaluation: PASS / PREFERRED.**

This preserves current bounded scope, avoids speculative design, and does not turn extensibility into an implementation mechanism. It also keeps future architecture evolution possible without silently widening the current subject set.

### D5-O3 — Open-ended representation extensibility required now

**Rule:** Q2 may be accepted only if the chosen persistence representation can add arbitrary future subject types without schema migration, representation redesign, or new persistence mechanism.

**Evaluation: FAIL AS A CURRENT ARCHITECTURE REQUIREMENT.**

No accepted authority requires zero-migration or zero-redesign extensibility. This would convert C3 extensibility from a qualitative comparison dimension into a mandatory gate and could implicitly favor some N1–N5 candidates.

### D5-O4 — Future types may be added implicitly by implementation

**Rule:** implementation may introduce new subject kinds whenever needed so long as a technical representation can encode them.

**Evaluation: FAIL.**

This would bypass architecture authority, undermine D1's explicit subject-type semantics, and let persistence capability define domain authority.

### D5-O5 — Future subject type may reuse an existing type discriminator by contextual interpretation

**Rule:** a future subject category may be represented under one of the existing five discriminator values if context/payload/association distinguishes it.

**Evaluation: FAIL.**

This conflicts with D1 and D4 explicit type/identity semantics and would create implicit subject-type polymorphism by context.

## 5. Candidate impact without candidate selection

D5 must not rank or select N1–N5. Its effect on later candidate re-application is limited to this distinction:

- candidates need to satisfy the five current subject types for the present Q2 decision;
- future extensibility remains a qualitative/evolution concern rather than a requirement that every future type be addable without migration;
- any future new subject type requires explicit architecture authority and may trigger a separate representation compatibility/reopen decision.

Therefore:

- N2/N3 are not rejected merely because future types may require schema evolution;
- N1/N4/N5 are not preferred merely because they may appear more open-ended;
- GC-002 Alternative B receives no preference or default status;
- C3 remains informative but not dispositive by itself.

## 6. Relationship to D1 discriminator set

D1's current five discriminator values remain authoritative for the current Q2 scope.

Under preferred D5-O2, introducing a future sixth subject type would require a separate architecture decision that explicitly expands or revises the accepted type set. D5 does not pre-authorize a placeholder, wildcard, `Unknown`, `Other`, or implementation-defined discriminator.

## 7. Actor attribution / ActorContext boundary

D5 concerns only the audited-subject type set.

It does not define actor types, actor identity, ActorContext, initiator categories, service principals, attribution persistence, or actor extensibility. Those remain separate unresolved architecture surfaces and MUST NOT be folded into the subject-type set.

## 8. Persistence and implementation boundaries

D5 does not decide:

- N1–N5 selection/default/ranking/rejection;
- exact persistence representation;
- FK/composite-FK/payload/opaque/registry shape;
- whether future types require schema migration;
- database/application enforcement;
- migration design;
- runtime resolver/API contract;
- GC-002 Alternative B approval;
- WP19 models, migrations, repositories, services, APIs, backend changes, or tests.

D5 also does not restore a WP18 → WP19 dependency.

## 9. Preferred D5 proposal

> **For the current ADR-0014 Q2 decision, the persisted AuditRecord subject-reference representation MUST support all five currently accepted subject types: `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, and `Task`. These five types define the current Q2 acceptance scope, not a permanently closed audited-subject universe. Any future auditable subject type requires separate explicit architecture authority and MUST satisfy the then-applicable D1–D4 subject-reference invariants. D5 does not require the current persistence representation to admit arbitrary future subject types without migration or representation evolution, and it does not pre-authorize wildcard, `Unknown`, `Other`, or implementation-defined subject kinds.**

## 10. D5 status

**OPEN — PROPOSED / NOT YET ACCEPTED.**

No authority artifact has been created. Project Owner acceptance is required before D5 becomes normative.

## 11. Gate result

**D5 OPTIONS STRUCTURED — CURRENT FIVE TYPES TREATED AS PRESENT Q2 ACCEPTANCE SCOPE — FUTURE TYPES REQUIRE SEPARATE EXPLICIT ARCHITECTURE AUTHORITY — NO ZERO-MIGRATION EXTENSIBILITY REQUIREMENT CREATED — NO N1–N5 SELECTION OR DEFAULT — GC-002 ALTERNATIVE B REMAINS PROPOSED ONLY — ACTOR ATTRIBUTION / ACTORCONTEXT REMAIN SEPARATE — WP18 DEPENDENCY NOT RESTORED — WP19 IMPLEMENTATION REMAINS BLOCKED.**

Current state:

- D1–D4: **CLOSED — ACCEPTED**;
- D5: **OPEN — PROPOSED / NOT YET ACCEPTED**;
- Q2 persisted representation: **OPEN / NOT ESTABLISHED**;
- N1–N5: **UNAPPROVED CANDIDATES**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- actor attribution / ActorContext: **SEPARATE / UNRESOLVED**;
- WP18 dependency: **NOT RESTORED**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit interim-shape authorization**.