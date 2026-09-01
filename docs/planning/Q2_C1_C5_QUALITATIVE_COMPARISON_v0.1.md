# WP19 / Q2 C1–C5 Qualitative Comparison v0.1

**Status:** Draft — Q2 application analysis only
**Date:** 2026-08-30
**Subject:** ADR-0014 Q2 — qualitative comparison of normalized candidates N1–N5
**Decision owner:** Project Owner through ADW-07
**Authority:** None. This artifact performs the approved comparison stage; it does not recommend, rank, approve, reject, or select a persisted representation.
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending Q2 resolution.

## 1. Scope and boundary

ADW-07 Block 4 / D6 approves the Q2 procedure in this order:

```text
A1–A6 authoritative constraint check
        ↓
S1–S10 semantic stress tests
        ↓
C1–C5 qualitative comparison
        ↓
exposed D1–D5 decision gaps
        ↓
Project Owner decisions where necessary
        ↓
separate Q2 representation decision
```

`Q2_A1_A6_APPLICATION_v0.1.md` completed A1–A6. `Q2_S1_S10_STRESS_TEST_APPLICATION_v0.1.md` completed S1–S10 without ranking or recommendation.

This artifact performs **only C1–C5 qualitative comparison**. It does not:

- assign numeric scores or weights;
- declare a winner, preferred candidate, shortlist, recommendation, or rejection;
- resolve D1–D5 by implication;
- reinterpret an S1–S10 result as an architecture decision;
- invent a concrete realization for an underspecified candidate;
- modify WP19 planning status or authorize implementation.

### Governance guardrail — stress-test result is not architecture rejection

A stress-test result such as `UNSUPPORTED` or `UNDETERMINED` is an evaluation-framework observation. It is **not** an architecture rejection.

Architecture rejection requires a later decision step with appropriate decision authority after the comparison and exposed decision dependencies are available. Likewise, `SUPPORTED` is not approval and does not create a preference.

Therefore this comparison may describe advantages, burdens, uncertainties, or dependencies, but it may not convert those observations into candidate acceptance or rejection.

## 2. Inputs carried forward

### A1–A6

- No N1–N5 candidate was eliminated by authoritative contradiction.
- A1 and A2 remain `UNDETERMINED` for all five candidates for different reasons.
- A3–A6 are PASS for all five normalized candidates.
- D1–D5 remain OPEN.

### S1–S10

- N3 has several class-level `SUPPORTED` results on the current five-type structural cases, but still lacks A1 sufficiency because cardinality/exclusivity semantics are unresolved.
- N2 exposes current-scope adaptation pressure for structurally asymmetric Workspace/User cases.
- N1, N4, and N5 remain more underspecified on several concrete subject stress surfaces.
- S6/S7 remain unresolved for all candidates and carry A2/D3 concerns.
- S8 remains D5-dependent for all candidates.
- S9 is supported for all candidates; R1 does not block comparison.
- S10 remains D2-sensitive for all candidates.

These findings are inputs, not ranking signals.

## 3. Comparison method

The approved framework defines:

- **C1 Queryability / audit retrieval**
- **C2 Integrity characteristics**
- **C3 Extensibility**
- **C4a Write/storage cost**
- **C4b Read/query cost**
- **C4c Migration cost**
- **C5 Evolution/reversibility cost**

Comparison is qualitative and representation-neutral. No DB FK receives automatic preference; no application-level or payload convention receives automatic penalty merely because it is not DB-native.

For underspecified candidates, the comparison distinguishes:

- **CLASS-LEVEL PROPERTY** — follows from the normalized candidate class;
- **DEPENDENT ON CONCRETE REALIZATION** — cannot be concluded without inventing design;
- **DECISION DEPENDENCY** — depends materially on D1–D5 or another unresolved architecture rule.

## 4. C1 — Queryability / audit retrieval

### N1 — Polymorphic reference

**CLASS-LEVEL PROPERTY:** a polymorphic reference is intended to provide a durable route from AuditRecord to a subject across multiple subject types.

**DEPENDENT ON CONCRETE REALIZATION:** query ergonomics cannot be determined without knowing whether type and identity are directly persisted, resolved by convention, indexed, or require application interpretation.

**Comparison observation:** N1 could support direct subject-oriented audit retrieval, but the normalized class does not establish whether that retrieval is simple SQL, multi-step lookup, or application-mediated.

**Decision dependency:** D1 may materially affect query shape.

### N2 — Composite FK

**CLASS-LEVEL PROPERTY:** for a subject type that fits the documented `(workspace_id, id)` form, relational retrieval can be naturally expressed through persisted key predicates and joins.

**CURRENT-SCOPE LIMITATION:** the documented GC-002 form is not a complete five-type Q2 mechanism. Workspace and User are structurally asymmetric, and no adaptation is normalized.

**Comparison observation:** N2 has comparatively explicit relational query semantics where its documented shape fits, but Q2-wide queryability cannot be assessed until current-scope adaptation is defined.

**Decision dependency:** D2/D4 may affect the final relational contract but are not decided here.

### N3 — Per-type nullable columns

**CLASS-LEVEL PROPERTY:** type-specific reference slots make the subject-type relation explicit at the persisted-shape class level.

**Comparison observation:** retrieval for a known subject type can be expressed against its corresponding relation/slot without first resolving an external type convention. Cross-type retrieval would likely require combining multiple subject-specific paths, but the exact query burden depends on concrete schema realization.

**Not assumed:** five exact columns, FK constraints, indexes, or exclusivity checks.

### N4 — Opaque identifier

**CLASS-LEVEL PROPERTY:** persisted opaque identity is available, but its interpretation is intentionally external to the raw value.

**Comparison observation:** subject-oriented retrieval depends strongly on the durable resolution convention. Without that convention, neither SQL ergonomics nor application lookup cost can be honestly characterized.

**Decision dependency:** D1 and the eventual durable resolver semantics.

### N5 — In-payload

**CLASS-LEVEL PROPERTY:** subject-identifying information lives within persisted AuditRecord content.

**Comparison observation:** queryability depends materially on payload/content structure, indexing capabilities, and whether the subject identity fields are stable and addressable. ADR-0014 permits this class but does not make a before/after diff sufficient.

**Decision dependency:** D1 and the eventual persisted-content contract. GC-007 remains unresolved and is not imported here.

### C1 comparison finding

C1 differentiates candidates primarily by **where query semantics become explicit**:

- N2 and N3 expose more relational structure at class level;
- N1 can be relational or convention-mediated depending on realization;
- N4 depends most directly on a durable resolution convention;
- N5 depends on a stable, queryable content contract.

This is not a preference statement. The framework has no authority saying SQL-direct retrieval is mandatory or superior to a durable application-mediated convention.

## 5. C2 — Integrity characteristics

### Guardrail

Normalization explicitly does not supply a subject-cardinality/exclusivity rule. C2 must therefore not reward or penalize a candidate by silently assuming exactly-one, zero-or-one, or another cardinality contract.

### N1 — Polymorphic reference

**DEPENDENT ON CONCRETE REALIZATION:** integrity may be enforced through structural fields, application/domain validation, durable conventions, or a combination. The candidate class does not establish which.

**Comparison observation:** N1 can potentially express one multi-type reference contract, but its integrity strength and enforcement location remain unresolved.

**Decision dependency:** D1, D2, D4.

### N2 — Composite FK

**CLASS-LEVEL PROPERTY:** database-enforced composite FK semantics provide strong relational enforcement for targets matching the key shape.

**CURRENT-SCOPE LIMITATION:** the documented shape does not naturally cover all five current subject types without an unspecified adaptation.

**Comparison observation:** N2 has the clearest DB-native integrity semantics in its documented applicable case, but that does not make DB enforcement mandatory under D4 and does not establish a complete Q2-wide integrity model.

**Decision dependency:** D2, D3, D4.

### N3 — Per-type nullable columns

**CLASS-LEVEL PROPERTY:** subject-type-specific slots can make distinct target relations explicit.

**UNRESOLVED SEMANTICS:** integrity across multiple slots depends on cardinality/exclusivity rules that normalization deliberately does not define.

**Comparison observation:** relation-specific integrity can potentially be enforced independently per slot, but the correctness of the AuditRecord as one audited-subject record cannot be assessed until slot semantics are decided.

**Decision dependency:** unresolved cardinality/exclusivity semantics, D2, D4.

### N4 — Opaque identifier

**DEPENDENT ON CONCRETE REALIZATION:** integrity depends on the durable resolution convention and where that convention is validated.

**Comparison observation:** N4 may decouple historical identity from current table shape, but without an approved namespace/resolver contract the enforcement characteristics remain largely undefined. No registry or global identity mechanism is assumed.

**Decision dependency:** D1, D2, D4.

### N5 — In-payload

**DEPENDENT ON CONCRETE REALIZATION:** integrity depends on the content schema, validation rules, and whether subject identity fields are stable and mandatory.

**Comparison observation:** payload persistence can preserve identifying facts inside the historical record itself, but the normalized candidate does not establish structural enforcement comparable to a DB reference or a mandatory content schema.

**Decision dependency:** D1, D2, D4 and the eventual content contract.

### C2 comparison finding

C2 exposes a difference between **DB-native referential enforcement**, **relation-specific persisted structure**, and **convention/content-based integrity**. Existing authority does not choose among those enforcement locations. Therefore C2 can describe enforcement characteristics but cannot yet convert stronger DB-native enforcement into automatic architectural preference.

## 6. C3 — Extensibility

### D5 guardrail

D5 is OPEN. C3 may describe what would change if another subject type were introduced, but cannot assume either:

- that open-ended extension is mandatory; or
- that the set is permanently fixed to the current five types.

### N1 — Polymorphic reference

**CLASS-LEVEL PROPERTY:** the candidate class is intended to reference more than one subject type through a shared reference concept.

**Comparison observation:** adding a type may be localized to the interpretation/type convention if the concrete realization is designed that way, but this is not guaranteed by normalization.

**Decision dependency:** D1 and D5.

### N2 — Composite FK

**Comparison observation:** additional subject types can require new/adapted relational target structures when they do not share the existing composite-key shape. The current five-type asymmetry already demonstrates this pressure.

This is a migration/evolution observation, not a defect while D5 is open.

**Decision dependency:** D2, D4, D5.

### N3 — Per-type nullable columns

**CLASS-LEVEL PROPERTY:** subject-type-specific slots tie representation structure to known subject relations.

**Comparison observation:** a new subject type is likely to require a new subject-specific persisted relation/slot in a conventional realization, but normalization intentionally does not assert an exact physical column model.

This may imply schema evolution under an open-ended D5 answer; it is not a penalty while D5 remains unresolved.

### N4 — Opaque identifier

**Comparison observation:** extension burden may be low at the AuditRecord storage surface if a durable resolution convention can incorporate new subject types without changing the stored shape. That favorable outcome is not guaranteed because the resolver is unspecified.

**Decision dependency:** D1, D5 and resolver semantics.

### N5 — In-payload

**Comparison observation:** a stable content envelope could potentially add new subject-type representations without top-level schema changes, but payload schema/versioning may still need evolution. No particular JSON contract is assumed.

**Decision dependency:** D1, D5 and content-versioning semantics.

### C3 comparison finding

C3 reveals different likely **locations of future change**:

- N2/N3 tend to expose change at relational schema/relationship level;
- N1/N4 tend to expose change in type/resolution convention;
- N5 tends to expose change in content schema/versioning.

Because D5 is open, C3 records where change would occur but does not rank those change locations.

## 7. C4a — Write/storage cost

### N1

Storage/write cost is realization-dependent. A compact structural reference may be small; a richer durable convention may require more persisted state. No concrete shape is normalized.

### N2

Composite-key semantics imply persistence of the key components needed for the relation plus supporting indexes/constraints in a conventional relational realization. Multi-target adaptation may add further structure, but that has not been designed.

### N3

Type-specific persisted slots can increase sparse schema surface as subject-type relations accumulate. Actual storage overhead depends on the physical representation and DB null/index behavior, none of which is fixed here.

### N4

The AuditRecord-side stored identifier may be compact, while supporting resolution infrastructure could carry cost elsewhere. Since that infrastructure is unspecified, total storage/write cost cannot be concluded from the identifier alone.

### N5

Subject identity carried in record content can add bytes to every AuditRecord and may duplicate identifying context. Actual overhead depends on payload schema and whether those fields already exist for other audit reasons.

### C4a comparison finding

The candidates shift cost between the AuditRecord row, indexes/constraints, resolver infrastructure, and payload. No approved criterion weights one storage location more heavily than another.

## 8. C4b — Read/query cost

### N1

Could range from direct indexed lookup to application-mediated resolution depending on concrete representation.

### N2

For targets matching the relational key shape, read paths can use conventional predicates/joins. Q2-wide cost remains unknown because current-scope adaptation is unresolved.

### N3

Known-type reads can target a subject-specific relation directly; cross-type retrieval may require OR/union-like logic or multiple relation paths depending on realization.

### N4

Read cost depends substantially on resolver semantics and whether resolution requires secondary lookup/application logic.

### N5

Read cost depends on payload parsing, indexability, DB support, and the stability of content fields used for subject identity.

### C4b comparison finding

C4b differentiates likely read paths but does not establish a universal low-cost winner because the most underspecified candidates have the widest realization range and because query workload priorities have not been assigned weights.

## 9. C4c — Migration cost

### N1

Initial migration cost depends on concrete fields/convention. Future migration cost depends on whether reference interpretation can evolve without rewriting historical AuditRecords.

### N2

Relational constraints and any required target uniqueness/composite-key support can increase migration coordination. Extending the pattern to structurally asymmetric targets may require additional schema work.

### N3

Initial migration is conceptually direct once subject-specific relations are chosen, but adding/changing supported relations may require schema migrations. Exact burden depends on physical realization.

### N4

AuditRecord-side migration may be small if the opaque shape is stable, but establishing or changing resolver semantics/infrastructure can shift migration complexity outside the AuditRecord table.

### N5

Initial schema migration may be small if existing content storage is reused, but historical content transformation or version-aware readers may become necessary if the identifying content contract changes.

### C4c comparison finding

Migration cost is redistributed rather than eliminated:

- relational candidates concentrate more cost in schema/constraints;
- convention-based candidates can move cost into resolver/version semantics;
- payload-based representation can move cost into historical content compatibility.

No weighting is applied.

## 10. C5 — Evolution / reversibility cost

A2 and D10 historical-record semantics are controlling background: committed AuditRecords cannot have their historical meaning silently rewritten.

### N1

Evolution is safe only if old reference conventions remain permanently interpretable. Changing type/discriminator semantics may require versioned interpretation rather than mutation of historical records.

### N2

Relational schema changes can coexist with historical rows if old target identity remains valid, but supersession/deletion behavior and multi-target evolution remain unresolved. A FK does not itself solve historical semantic versioning.

### N3

Adding new subject-specific relations can coexist with old slots, but changing the meaning of an existing slot would threaten A2. Historical compatibility therefore favors additive/version-aware evolution over reinterpretation.

### N4

The stored opaque value can remain unchanged only if old resolver semantics remain durable. Resolver replacement that changes meaning of old values would conflict with A2.

### N5

Historical payload bytes can remain immutable while readers become version-aware. However changing the interpretation of an existing content field without preserving old semantics would conflict with A2.

### C5 comparison finding

All five candidates require a durable **old-reference interpretation story**. The location differs:

- N1: reference/type convention;
- N2: relational target/identity semantics;
- N3: subject-specific slot meaning;
- N4: resolver convention;
- N5: content schema/version interpretation.

No candidate receives automatic reversibility superiority from its class label alone.

## 11. Cross-candidate comparison findings

### C-F1 — relational explicitness and semantic flexibility trade locations, not authority

N2/N3 expose more reference structure in the relational persisted shape. N1/N4/N5 leave more meaning to a type/resolution/content convention. The framework contains no authority saying either location is inherently preferable.

### C-F2 — the current five-type asymmetry is most visibly costly to a uniform composite-key formulation

The Workspace/User asymmetry creates a concrete adaptation burden for N2's documented `(workspace_id, id)` form. This is a comparative burden, not an architecture rejection. N2 remains a candidate until decision authority acts on the full comparison and decision dependencies.

### C-F3 — N3's class-level structural coverage carries an unresolved integrity contract

N3's S1–S5 support and explicit type-specific relations are useful comparison facts, but its subject-cardinality/exclusivity rule remains unresolved. Its structural clarity therefore must not be converted into an automatic recommendation.

### C-F4 — N4 and N5 can move complexity out of top-level relational schema, but do not eliminate it

For N4 complexity moves into durable resolver semantics; for N5 into persisted-content schema/version/query semantics. This is a location-of-complexity difference, not evidence that either class is intrinsically simpler.

### C-F5 — D1–D5 materially affect any eventual preference

A rational recommendation cannot yet be produced without knowing which unresolved architecture properties matter as requirements or preferences. In particular:

- D1 changes interpretation burden for N1/N4/N5 and potentially N2/N3;
- D2 changes workspace-integrity comparison;
- D3 changes deletion/historical-reference behavior;
- D4 changes the significance of DB-enforced RI;
- D5 changes how C3 should influence the decision.

## 12. Comparison gate result

**C1–C5 QUALITATIVE COMPARISON COMPLETE — TRADEOFFS EXPOSED — NO WINNER, RECOMMENDATION, OR ARCHITECTURE REJECTION CREATED.**

The comparison does not alter prior authority state:

- Q2 persisted representation remains OPEN;
- D1–D5 remain OPEN;
- no candidate is approved or rejected;
- GC-002 Alternative B remains Proposed only;
- GC-006 / GC-007 remain unresolved and unchanged;
- WP19 remains BLOCKED / UNAUTHORIZED pending Q2 resolution.

A stress-test `UNSUPPORTED` result, if one exists in a future revision, remains an evaluation result rather than architecture rejection. Architecture rejection or selection requires a later explicit decision by the appropriate decision authority.

**Next bounded step under the approved procedure:** expose and structure the D1–D5 decision gaps using the A1–A6, S1–S10, and C1–C5 findings as evidence. Do not yet select a persisted representation or authorize WP19 implementation.