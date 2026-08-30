# WP19 / Q2 Post-D1–D5 Candidate Re-application v0.1

**Status:** Draft — post-decision evaluation / recommendation only  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 — re-application of accepted D1–D5 to normalized persistence candidates N1–N5  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact evaluates and recommends; it does not select or approve a persisted representation.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending explicit Q2 persisted-representation decision or separate explicit bounded interim-shape authorization.

## 1. Purpose and controlling authority

The earlier normalization, A1–A6, S1–S10, and C1–C5 artifacts were intentionally evaluated while D1–D5 were unresolved. D1–D5 are now CLOSED / ACCEPTED and must be re-applied before a Q2 representation decision.

Canonical decision authorities:

- `00_ARCHITECTURE/07_AUDIT/ADW07_D1_SUBJECT_TYPE_DISAMBIGUATION_DECISION.md`
- `00_ARCHITECTURE/07_AUDIT/ADW07_D2_WORKSPACE_SUBJECT_SEMANTICS_DECISION.md`
- `00_ARCHITECTURE/07_AUDIT/ADW07_D3_SUBJECT_DELETION_DECISION.md`
- `00_ARCHITECTURE/07_AUDIT/ADW07_D4_SUBJECT_REFERENCE_SEMANTICS_DECISION.md`
- `00_ARCHITECTURE/07_AUDIT/ADW07_D5_SUBJECT_TYPE_EXTENSIBILITY_DECISION.md`

This pass does not reopen D1–D5 and does not silently reinterpret them.

## 2. Accepted D1–D5 requirements relevant to candidate evaluation

A conforming Q2 representation must provide, for all five current subject types (`Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, `Task`):

1. **D1 — explicit durable subject type:** exactly one current subject kind is explicit; it is not inferred from actor, route, payload, or context.
2. **D2 — subject/context separation:** Workspace context does not substitute for another audited subject; association participants do not substitute for an association subject.
3. **D3 — historical identity survival:** later deletion/deactivation/context loss does not rewrite or destroy the committed audited-subject identity; current live dereference is not universally required.
4. **D4 — explicit logical subject identity:** AuditRecord has one mandatory, durable, stable, independently resolvable audited-subject identity. Actor attribution, ActorContext, request/runtime/Workspace context, route, diff, association data, and payload do not establish the subject by implication or serve as fallback.
5. **D5 — bounded current scope:** all five current types must be supported. Arbitrary future-type support without migration/redesign is not required. Future types require separate architecture authority. Extensibility convenience alone must not rank N1–N5.

No accepted D1–D5 authority requires database-enforced referential integrity, a universal FK, zero-migration extensibility, or one specific storage location.

## 3. Evaluation status vocabulary

- **CONFORMING REALIZATION AVAILABLE:** the candidate class can satisfy D1–D5 without changing its essential candidate identity, but concrete design is still required.
- **CONFORMING ONLY WITH MATERIAL QUALIFICATION:** the candidate can remain in the universe, but satisfying D1–D5 requires a qualification that removes a common/naive realization or materially narrows the class.
- **NOT SUFFICIENT AS CURRENTLY DOCUMENTED:** the corpus-documented candidate does not cover the accepted current Q2 scope; making it sufficient requires additional design not established by its documented form.

These are evaluation results, not architecture approval/rejection.

## 4. N1 — Polymorphic reference

**Result: CONFORMING REALIZATION AVAILABLE.**

A polymorphic reference can satisfy D1–D5 if its durable contract contains:

- an explicit accepted subject type;
- a stable subject identifier interpreted under that type;
- exactly one logical audited-subject identity;
- historical interpretation that remains stable even when live dereference later fails.

This does **not** require a particular pair of columns such as `subject_type + subject_id`; that would be persistence design. It does require the logical equivalent of explicit type qualification plus durable identity because D1/D4 now make those semantics authoritative.

### Strengths after D1–D5

- naturally models one logical subject reference across all five types;
- aligns directly with D1 explicit type plus D4 one logical identity;
- keeps actor/context separation straightforward;
- current five-type support does not require future-proof open-ended design under D5;
- can provide direct subject-oriented audit query semantics if the concrete fields are indexable.

### Burdens / unresolved design

- cross-table DB FK enforcement is not inherent and may be impossible in a conventional relational realization without auxiliary structure;
- write-time validation and durable resolution semantics must be explicit;
- historical interpretation of `(kind, identifier)` must remain stable under D3/D4.

These burdens are not architecture failures because DB-enforced referential integrity is not an accepted requirement.

## 5. N2 — Composite FK

**Result: NOT SUFFICIENT AS CURRENTLY DOCUMENTED.**

GC-002 Alternative B documents a composite `(workspace_id, id)` FK approach for named relationships including a single `AuditRecord`→aggregate formulation. The accepted Q2 scope contains five structurally asymmetric subject types. D2 also prevents Workspace context from being treated as a substitute for another subject's identity.

Therefore the documented N2 form does not itself establish one complete D1/D4-conforming subject-reference representation across all five current types.

A Q2-wide composite-FK solution could potentially be engineered, but that would require a new concrete multi-target/target-normalization design. It must not be smuggled in as “GC-002 Alternative B”.

### Strengths

- strongest DB-native referential enforcement where target/key shape fits;
- relational query semantics can be direct for applicable targets.

### Burdens

- five-type structural asymmetry is a first-order problem, not a future extensibility problem;
- adapting the mechanism may introduce multiple FK paths, target normalization, registry/base-table indirection, or other new design;
- any such adaptation risks ceasing to be the documented GC-002 Alternative B and becoming a new persistence design.

**GC-002 Alternative B remains PROPOSED ONLY and is not recommended as a default Q2 answer.**

## 6. N3 — Per-type nullable relations/slots

**Result: CONFORMING REALIZATION AVAILABLE.**

N3 can satisfy D1–D5 if the representation preserves one logical subject identity while using subject-type-specific persisted reference paths.

D1/D4 now require the realization to make subject type explicit and to prevent ambiguity about which one logical subject is identified. Therefore a valid N3 realization needs an explicit semantic exclusivity rule: a committed AuditRecord must not represent multiple audited subjects merely because several physical slots exist. The exact database CHECK/FK/nullability mechanism is not decided here.

### Strengths after D1–D5

- explicit relation to each concrete target type;
- strong potential DB-native referential integrity per type;
- straightforward known-type query paths;
- covers the current five-type D5 scope without requiring a universal shared identity space;
- future schema additions are acceptable under D5 rather than an architectural defect.

### Burdens

- sparse/wider AuditRecord persistence surface;
- one-logical-subject exclusivity must be enforced somewhere explicitly;
- cross-type queries become more complex;
- each future authorized subject type likely creates schema/relationship evolution.

D5 makes the final burden acceptable in principle, but does not turn it into a preference.

## 7. N4 — Opaque identifier

**Result: CONFORMING ONLY WITH MATERIAL QUALIFICATION.**

A bare opaque identifier is not enough under D1/D4. A conforming N4 realization must also carry the explicit accepted subject type and must have a durable, stable resolution convention capable of identifying one historical subject instance independently of actor/context/runtime state.

Once those requirements are added, N4 remains conceptually possible, but its primary simplicity is partly offset by the need for a normative namespace/resolution contract.

### Strengths

- storage shape can remain compact;
- historical identity can be decoupled from current table layout if the resolution convention is durable.

### Burdens

- resolver/namespace semantics become critical architecture;
- integrity and queryability can shift from relational schema into application/resolution infrastructure;
- a shared global namespace or registry must not be invented by implication;
- opaque identity offers no accepted benefit sufficient to justify introducing resolver infrastructure by default.

N4 remains viable but is not preferred on current authority/evidence.

## 8. N5 — In-payload subject identity

**Result: CONFORMING ONLY WITH MATERIAL QUALIFICATION.**

ADR-0014 permits subject identification within AuditRecord content. D4 now makes clear, however, that generic audit payload, diff, request data, actor data, or contextual facts may **not** establish subject identity by implication or serve as fallback.

Therefore a conforming N5 realization cannot mean “inspect the diff/payload and infer what changed.” It would need an explicit, mandatory, durable subject-identity contract inside persisted content, including explicit D1 subject type and stable subject identifier semantics.

This preserves N5 as a candidate because D4 did not prohibit payload placement. It rejects only the inferential form of N5.

### Strengths

- historical identifying data can travel with the immutable AuditRecord;
- may avoid dedicated relational reference columns depending on physical design.

### Burdens

- queryability/indexing depends heavily on content structure and DB capabilities;
- integrity is dependent on a mandatory versioned content contract;
- historical reader/version semantics become critical;
- using the same payload for both mutation detail and canonical subject identity risks semantic coupling;
- ADR-0005's queryable audit-trail objective gives no affirmative reason to prefer a harder-to-query content representation when simpler explicit reference structures are available.

N5 remains admissible but is not preferred.

## 9. Comparative result after D1–D5

| Candidate | D1–D5 conformity outlook | Principal unresolved burden | Current evaluation position |
|---|---|---|---|
| N1 Polymorphic reference | Strong | enforcement/resolution mechanics | **Preferred for final consideration** |
| N2 Composite FK | Incomplete as documented | five-type structural adaptation | **Do not select as documented** |
| N3 Per-type nullable relations | Strong | exclusivity + wider schema | **Viable alternative / runner-up** |
| N4 Opaque identifier | Conditional | durable resolver/namespace contract | **Viable but not preferred** |
| N5 In-payload | Conditional | explicit content contract + query/integrity burden | **Viable but not preferred** |

## 10. Recommendation

### Recommended Q2 representation class: N1 — Polymorphic reference

The post-D1–D5 evaluation recommends **N1 Polymorphic reference** as the best representation class to carry into the separate Project Owner Q2 persisted-representation decision.

The recommendation is based on the accepted architecture requirements, not on speculative future extensibility:

1. D1 already requires explicit subject type; N1 expresses that naturally as part of one logical reference.
2. D4 requires one mandatory, explicit, independently resolvable subject identity; N1 maps directly to that semantic model without multiplying type-specific physical paths.
3. D2 and the actor/context boundary are easy to preserve because the subject reference is first-class rather than inferred from Workspace/actor/payload.
4. D3 historical stability can be achieved by preserving the committed type+identifier meaning; live-row survival is not required.
5. D5 removes the need to reject N3 for future migrations, but it also removes future extensibility as a reason to prefer N1. N1 is preferred here because it is the simplest direct expression of the already-accepted **single logical typed subject identity** across the current five types.
6. N2's stronger DB-native integrity does not outweigh its incomplete five-type fit because DB-enforced RI is not an accepted mandatory architecture requirement.
7. N3 is a credible alternative but introduces multiple physical subject paths to represent a semantic contract that D4 defines as one logical reference.
8. N4/N5 move essential subject-resolution meaning into resolver/content contracts without an established need to take on that extra semantic infrastructure.

### Important limitation

This recommendation does **not** approve `subject_type + subject_id`, any exact columns, SQL types, indexes, FK policy, resolver API, validation location, or migration. Those belong to the subsequent concrete representation decision/design after Project Owner selects the representation class.

## 11. Explicit non-decisions

This artifact does not:

- accept or approve N1;
- reject N2–N5 as architecture authority;
- approve GC-002 Alternative B;
- choose exact persistence fields or constraints;
- decide DB versus application referential-integrity enforcement;
- define actor attribution / ActorContext persistence semantics;
- restore WP18 → WP19 dependency;
- authorize WP19 implementation;
- modify backlog or `IMPLEMENTATION_SEQUENCE.md`;
- close ADW-07.

## 12. Gate result

**POST-D1–D5 RE-APPLICATION COMPLETE — N1 POLYMORPHIC REFERENCE RECOMMENDED — N3 RETAINED AS STRONG ALTERNATIVE — N2 NOT SUFFICIENT AS CURRENTLY DOCUMENTED — N4/N5 REMAIN CONDITIONALLY VIABLE — NO REPRESENTATION AUTHORITY ESTABLISHED.**

Current state:

- D1–D5: **CLOSED — ACCEPTED**;
- recommended candidate: **N1 POLYMORPHIC REFERENCE — RECOMMENDATION ONLY**;
- Q2 persisted representation: **OPEN / NOT ESTABLISHED**;
- N1–N5: **UNAPPROVED**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- actor attribution / ActorContext persistence semantics: **SEPARATE / UNRESOLVED**;
- WP18 dependency: **NOT RESTORED**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED pending explicit Q2 persisted-representation decision or separate explicit bounded interim-shape authorization**.

The next bounded step is a **separate Project Owner Q2 persisted-representation decision**. Recommendation is not acceptance.