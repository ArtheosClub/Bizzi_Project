# WP19 / Q2 Final Bounded Representation Comparison v0.1

**Status:** Active planning evaluation
**Artifact type:** Q2 representation comparison — evaluation only, applying the approved `Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md` procedure to the four bounded arms remaining after Q2-RI, Q2-ST, and Q2-EX
**Date:** 2026-09-05
**Subject:** ADR-0014 Q2 — final bounded comparison of BR1/N1, BR3/N3 (with accepted Q2-EX-O1), BR4/N4, BR5/N5
**Authority:** None — this artifact evaluates and does not select the persisted Q2 representation.
**Implementation effect:** None — WP19 remains BLOCKED / UNAUTHORIZED.

> This artifact does not select a representation. It does not recommend one. It does not rank the four arms into a winner. Per accepted A6 (`docs/planning/Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md` §2), no representation has presumptive approval, and the Project Owner is the only decider. Nothing below should be read as a conclusion that any arm is best, preferred, leading, winning, or dominant.

---

## 1. Scope and method

This artifact applies the procedure approved by `00_ARCHITECTURE/07_AUDIT/ADW07_BLOCK4_Q2_EVALUATION_PROCEDURE_APPROVAL.md` (D6), as defined in `docs/planning/Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md`, using the A2/A4/S9 corrected forms stated in that approval's Scope section:

> "1. **A2 precision:** distinguish D10's direct immutability authority from the derived consequence that correction should be represented by a new historical record rather than mutation of the committed AuditRecord. 2. **A4 precision:** distinguish the open Domain Event ↔ AuditRecord relationship from Block 2 R1, which concerns Domain Event ↔ Durable Audit / Outbox / Publication-Intent identity. 3. **S9 precision:** apply R1 as a stress surface only where a candidate depends on the Domain Event ↔ Durable Audit / Outbox / Publication-Intent identity question; do not use R1 as another name for the Event ↔ AuditRecord relationship." (`00_ARCHITECTURE/07_AUDIT/ADW07_BLOCK4_Q2_EVALUATION_PROCEDURE_APPROVAL.md`, "Scope")

No criterion, stress test, or scoring method is invented here. A1–A6, S1–S10, and C1–C5 are used exactly as defined in `docs/planning/Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md` §2, §5, §6. The candidate evaluation template applied to each arm is §11's, unmodified.

Result vocabulary is fixed and used without decoration. Framework §3 defines exactly three results for A1–A6 — PASS, FAIL, UNDETERMINED — DECISION REQUIRED — and states "No `PARTIAL PASS` status is proposed." Framework §5 defines exactly four results for S1–S10 — SUPPORTED, UNSUPPORTED, UNDETERMINED — DECISION REQUIRED, NOT APPLICABLE. Every Result cell below uses one of these values exactly; any qualification, condition, or cross-reference is carried in the Evidence/rationale or Decision-dependency columns instead.

### 1.1 Arms compared

Exactly four, per the corpus's own bounded-realization definitions:

- **BR1 / N1** — polymorphic reference (`docs/planning/Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §3, `docs/planning/Q2_CANDIDATE_NORMALIZATION_v0.1.md` §3 "N1");
- **BR3 / N3**, together with accepted **Q2-EX-O1** — per-type nullable relations with structural qualification and database-enforced exactly-one (`docs/planning/Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §5, `00_ARCHITECTURE/07_AUDIT/ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`);
- **BR4 / N4** — opaque identifier (`docs/planning/Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §6);
- **BR5 / N5** — in-payload dedicated subject identity (`docs/planning/Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §7).

Candidate wording is taken verbatim from these sources and is not paraphrased into new names.

### 1.2 BR2 / N2 is excluded

`docs/planning/Q2_POST_Q2_ST_BOUNDED_REAPPLICATION_v0.1.md` §4:

> "**Current-five sufficiency:** NOT SUFFICIENT in its corpus-grounded bounded form. ... Q2-ST does not cure the existing structural asymmetry: `Workspace` and `User` do not expose the same `(workspace_id, id)` target shape as the workspace-scoped entities. No synthetic identity or registry is introduced."

And §8, item 2:

> "BR2 remains insufficient in its current corpus-grounded five-type form, with local RI credit only."

BR2 is excluded on this ground and is not repaired, extended, or synthesized into a stronger form to make it comparable. Inventing a synthetic identity or registry so that `Workspace` and `User` present the same `(workspace_id, id)` shape as the workspace-scoped entities would be a new architectural abstraction introduced solely to make BR2 comparable — not to solve a demonstrated problem or to implement a scheduled Work Package. `CLAUDE.md`'s Abstraction Justification Rule:

> "A new architectural abstraction must either solve an existing, demonstrated problem, or be a necessary precondition for implementing the next Work Packages. Anticipated future need is not sufficient justification."

Accepted Q2-ST applied this same rule to decline its own O3 mapping layer (`00_ARCHITECTURE/07_AUDIT/ADW07_Q2_ST_SUBJECT_TYPE_RANGING_RULE_DECISION.md`, "Abstraction Justification Rule reference": "No mapping exception currently exists, so the governance, resolver, and versioning machinery O3 requires would be introduced against predicted rather than demonstrated need."). Repairing BR2 here would be the same move one layer lower, against the same absence of demonstrated need. BR2 is therefore left as recorded and is not part of the four-arm comparison below.

---

## 2. How Q2-RI credit is weighted in this comparison

Accepted Q2-RI (`00_ARCHITECTURE/07_AUDIT/ADW07_Q2_RI_REFERENTIAL_INTEGRITY_WEIGHT_DECISION.md`) is **Q2-RI-O2 — PREFERENCE, not REQUIREMENT**:

> "DB-enforced referential integrity is therefore a comparative preference, not a Q2 requirement." ... "This preference applies to a concrete proposed realization, not to a candidate class. It is a comparative input only: it cannot substitute for D1–D5 conformity, cannot by itself select a Q2 representation, and each application of the preference in candidate evaluation must record its reasoning."

This comparison applies Q2-RI credit **only inside C2 (Integrity characteristics)**, as one qualitative sub-input among several, never as a gate on A1–A6 admissibility and never as a tie-breaking weight that by itself selects between arms. Concretely:

- Q2-RI credit does not appear anywhere in the A1–A6 rows below. BR3's A1 result rests on accepted Q2-EX-O1's exactly-one guarantee (a D1-CLAR-01 property-test question), not on its Q2-RI credit. BR1, BR4, and BR5 carry no Q2-RI credit and this has no bearing on their own A1–A6 results, which are evaluated independently.
- If Q2-RI credit were removed entirely from consideration, no A1–A6 result for any arm below would change. This is the check the framework requires: if weighting Q2-RI as a requirement would make BR3 win by construction, the comparison is void. Since removing it changes nothing at the admissibility layer, it has not been so weighted.
- Within C2 itself, BR3's positive credit is recorded as one qualitative observation about its five per-target relations, alongside its own separately-tracked cost (the cross-slot exactly-one invariant, which accepted Q2-EX is explicit is **not** referential integrity — see §3 below) and alongside BR1/BR4/BR5's own C2 stories, none of which are penalized for lacking DB-native FK credit. Accepted Q2-RI: "Lack of ordinary database foreign-key enforcement is not by itself disqualifying where durable correctness, validation, and historical subject resolvability are established through another explicit, recorded mechanism."

---

## 3. The BR3 asymmetry

BR3 is the only one of the four arms whose exclusivity/qualification surface has been separately worked out and accepted, via Q2-EX. The accepted Q2-EX record is explicit that this must not be read as favoring BR3's selection:

> "This decision does not select, endorse, approve, or favour BR3/N3, and must not be read as making its selection more likely." (`00_ARCHITECTURE/07_AUDIT/ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`, "Conditionality")

This comparison treats the asymmetry as follows, applying §8's representation-neutrality rule (`docs/planning/Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md` §8 — "Does this criterion express a property the architecture needs, or does it silently encode a preferred implementation?"):

- BR3's A1 and A2 rows below cite Q2-EX-O1 because that is the accepted authority that actually resolves BR3's exactly-one question. This is a citation of what exists, not a credit for having been decided first.
- BR1 and BR4 did not receive an equivalent decision because exactly-one holds structurally for them: each carries one reference field (a single `subject_type`/`subject_id` pair, or a single `subject_type`/`subject_key` pair), so there is no multi-slot state in which more than one or zero subjects could be indicated. There is nothing for an exactly-one decision to resolve. BR5 is the same way: its bounded contract is a single mandatory dedicated content object (`docs/planning/Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §7), not per-type slots, so it likewise has no multi-slot ambiguity requiring a separate exactly-one decision.
- BR3 needed Q2-EX specifically because its bounded realization uses five per-type nullable slots (`docs/planning/Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §5), which makes "exactly one populated, and it matches the discriminator" a real, non-trivial condition that a persisted state could otherwise violate. This is a property of the candidates' respective structures, not a procedural favor extended to one arm and withheld from the others.
- The practical asymmetry this leaves in the corpus — BR3's cost here is now explicit, bounded, and closed by an accepted record, while BR1/BR4/BR5 have no equivalent accepted record because none was structurally required for this particular question — is named directly in §9 below (the decision-sufficiency test) and is not treated there as a missing decision dimension, because §3 here already accounts for why no equivalent record exists.

---

## 4. Subject-type set

The current Q2 acceptance scope is five subject types: `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, `Task` (`00_ARCHITECTURE/07_AUDIT/ADW07_D5_SUBJECT_TYPE_EXTENSIBILITY_DECISION.md` §3). This is current corpus state, not a stale figure to be updated: accepted Q2-ST explicitly declines to make `AgentDefinition` a sixth kind, to map it into `EnterpriseObject`, or to authorize AuditRecord production for it (`00_ARCHITECTURE/07_AUDIT/ADW07_Q2_ST_SUBJECT_TYPE_RANGING_RULE_DECISION.md`, "Explicit non-decisions"), and its reopen trigger is keyed to "implementation of an auditable mutation whose audited subject has a persisted identity form not already covered" — which has not occurred (`00_ARCHITECTURE/07_AUDIT/ADW07_Q2_ST_SUBJECT_TYPE_RANGING_RULE_DECISION.md`, "AuditRecord subject-kind reopen trigger"). Every S1–S5 and S8 evaluation below is run against exactly these five types; no hypothetical sixth type is evaluated as though it were in scope.

---

## 5. D5 guardrail applied to this comparison

Accepted D5 guardrail 1:

> "Extensibility convenience MUST NOT by itself determine, rank, or default the Q2 persistence representation. A candidate does not become preferred merely because it appears easier to extend to hypothetical future subject types." (`00_ARCHITECTURE/07_AUDIT/ADW07_D5_SUBJECT_TYPE_EXTENSIBILITY_DECISION.md` §2, item 1)

Every S8 and C3 row below records this guardrail explicitly in its rationale and gives the extension-cost content no comparative weight. Where the vocabulary requires a status value (SUPPORTED for S8; qualitative content for C3), that value describes only whether the arm accommodates a future authorized type without corrupting committed records or requiring reinterpretation — not whether that accommodation is easy, cheap, or preferable.

---

## 6. Per-arm evaluation (§11 template)

D10's full path, cited once here and referenced by the bare identifier `D10 §9` thereafter, consistent with how the accepted corpus itself cites it (e.g. `00_ARCHITECTURE/07_AUDIT/ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`: "D3, D4, and D10 §7.4"; `00_ARCHITECTURE/07_AUDIT/EVENTS_AUDIT_AND_PROVENANCE.md`: "per D10 §9"): `00_ARCHITECTURE/01_DOMAIN/D10_DELETION_AND_SUPERSESSION.md`.

### 6.1 BR1 / N1 — Polymorphic reference

Minimal contract: `docs/planning/Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §3 — explicit durable `subject_type` + `subject_id` pair, with a subject-type dispatch/write-validation contract; no registry or multi-target FK introduced. The `subject_type` value is drawn from D1's already-accepted, fixed five-value vocabulary and `subject_id` refers directly to the corresponding table's own primary key, so the dispatch mapping is a closed, given enumeration rather than an encoding scheme requiring separate design.

| Dimension | Result | Evidence / rationale | Decision dependency |
|---|---|---|---|
| A1 Durable subject resolvability | PASS | Explicit `(subject_type, subject_id)` pair, with `subject_id` a direct reference to the target table's own primary key. Conforms to D1-CLAR-01's property test as a token realization: "A realization that stores a kind token satisfies this requirement where the token is authoritative for the record" (`00_ARCHITECTURE/07_AUDIT/ADW07_D1_DISCRIMINATOR_REALIZATION_CLARIFICATION.md` §2). | The write-validation contract confirming the referenced row exists is not itself designed here (`Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §3, "Explicit exclusions"). |
| A2 Committed reference meaning | PASS | "The committed pair is immutable and remains historically interpretable even if live dereference later becomes unavailable under D3" (`Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §3). | — |
| A3 Subject vs actor separation | PASS | Pair identifies only the audited subject; no actor/context substitution is present in the contract. Consistent with D4 (`00_ARCHITECTURE/07_AUDIT/ADW07_D4_SUBJECT_REFERENCE_SEMANTICS_DECISION.md` §3). | — |
| A4 Event/AuditRecord assumption | PASS | The BR1 contract makes no reference to Domain Event, Outbox, or Publication-Intent identity. | — |
| A5 Retention exclusion | PASS | A5 excludes retention duration as a selection criterion — D10 §9 "Inheritance of Historical Responsibility" (`00_ARCHITECTURE/01_DOMAIN/D10_DELETION_AND_SUPERSESSION.md`): "Retention duration is explicitly not decided here. How long a preserved Historical Record must remain queryable, whether older records may move to a different storage tier, and what (if any) legal retention or erasure obligation applies are business, compliance, and legal questions this project's own planning corpus has already flagged as outside architecture's authority to originate." BR1's contract does not smuggle retention in as a selection criterion. | — |
| A6 No presumptive representation | PASS | Evaluated under the same neutrality rule applied to every other arm; no default preference assumed for BR1. | — |
| S1 Workspace as subject | SUPPORTED | `subject_type=Workspace`, `subject_id`=the Workspace's own id; no parent workspace invented. | — |
| S2 User as subject | SUPPORTED | Dispatch contract maps `subject_type=User` to the User table; contract does not assume `workspace_id` exists for User. | — |
| S3 WorkspaceMembership as subject | SUPPORTED | Distinct `subject_type=WorkspaceMembership` value keeps membership mutation distinct from User mutation, consistent with D2's boundary that "`WorkspaceMembership` remains a distinct subject type and is not reduced to the Workspace that it references" (`00_ARCHITECTURE/07_AUDIT/ADW07_D2_WORKSPACE_SUBJECT_SEMANTICS_DECISION.md` §2). | — |
| S4 EnterpriseObject as subject | SUPPORTED | Canonical case handled by dispatch; contract does not force other subjects to become EnterpriseObjects. | — |
| S5 Task as subject | SUPPORTED | Conventional workspace-scoped case handled identically to S4. | — |
| S6 Subject deletion | SUPPORTED | Immutable pair "remains historically interpretable even if live dereference later becomes unavailable under D3" (`Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §3); no assumption that AuditRecord itself prevents deletion, consistent with D3 (`00_ARCHITECTURE/07_AUDIT/ADW07_D3_SUBJECT_DELETION_DECISION.md` §3). | — |
| S7 Lifecycle change | SUPPORTED | Same immutability property covers archival/supersession. | — |
| S8 New subject type | SUPPORTED | Adding a sixth type extends the dispatch contract's semantic mapping and D1's discriminator vocabulary; no schema/column change is implied by the bounded contract itself. Per D5 guardrail 1 ("Extensibility convenience MUST NOT by itself determine, rank, or default the Q2 persistence representation"), this is recorded as a non-ranking observation, not a comparative credit. | Any sixth type requires separate D5/Q2-ST authority regardless of representation (`00_ARCHITECTURE/07_AUDIT/ADW07_D5_SUBJECT_TYPE_EXTENSIBILITY_DECISION.md` §4). |
| S9 R1 unresolved | NOT APPLICABLE | BR1's contract has no dependency on Domain Event ↔ Durable Audit / Outbox / Publication-Intent identity. | — |
| S10 Cross-workspace ambiguity | SUPPORTED | `subject_type` disambiguates across all five current types regardless of UUID origin; type-specific dispatch means no two types can be confused even though "IDs are independently generated UUIDs per table rather than one shared type-prefixed identity space" (`Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md` §4 — IMPLEMENTATION EVIDENCE, NOT ARCHITECTURE AUTHORITY). | — |
| C1 Queryability | qualitative | `(subject_type, subject_id)` equality is direct and indexable for retrieval by a known subject. Filtering by a known kind is likewise a direct, indexable equality predicate on `subject_type` — BR3's per-path filtering under Q2-EX-O1 is equally direct and indexable on its own populated-path predicate (see §6.2 C1); the two are not distinguished at the filtering level. Returning or grouping the subject kind as a value across heterogeneous records reads `subject_type` directly from the stored column. ADR-0005 "supports queryability as a legitimate concern but does not mandate a particular mechanism" (`docs/planning/Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md` §6, C1). | — |
| C2 Integrity characteristics | qualitative | No DB-native FK; correctness rests on the write-time dispatch/validation contract (application-level). Q2-RI credit: **NONE** (`Q2_POST_Q2_ST_BOUNDED_REAPPLICATION_v0.1.md` §3) because no registry/multi-target FK is introduced to obtain DB enforcement, consistent with the Abstraction Justification Rule condition inside accepted Q2-RI. Not disqualifying per accepted Q2-RI. | — |
| C3 Extensibility | qualitative | Adding a sixth type extends the dispatch contract's semantic mapping and D1's discriminator vocabulary; no schema/column change is implied by the bounded contract itself (see S8). Per D5 guardrail 1, this is recorded as a non-ranking observation, not a comparative credit. | — |
| C4a Write/storage cost | qualitative | Two columns (`subject_type`, `subject_id`); no auxiliary tables. Write path includes an existence-check validation step. | — |
| C4b Read/query cost | qualitative | Reaching the concrete subject row for a known identifier requires an application-level dispatch step rather than one generic SQL join across five tables. Filtering by a known kind, or returning kind for a known row, is direct, as noted under C1. | — |
| C4c Migration cost | qualitative | Minimal at the current five-type scope: two columns, added once. | — |
| C5 Evolution/reversibility | qualitative | Pair format is stable; a future subject type adds a new `subject_type` value without rewriting committed pairs, consistent with D1-CLAR-01's durability/stability property. | — |

### 6.2 BR3 / N3 — Per-type nullable relations, with accepted Q2-EX-O1

Minimal contract: five nullable per-type FK slots, each targeting its corresponding table's primary key with an ordinary DB foreign key (`docs/planning/Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §5, for slot structure only), together with accepted Q2-EX-O1's structural-qualification mechanism: the audited subject kind is determined by which authorized reference path is populated, with **no separate persisted scalar kind column**, and exactly one path is guaranteed populated at the database persistence boundary (`00_ARCHITECTURE/07_AUDIT/ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`, "Decision"). `Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §5 additionally describes a separate `subject_type` discriminator column stored alongside the slots, with an invariant that the populated slot must match it — that is the shape accepted Q2-EX rejected as **Q2-EX-O2** ("separate discriminator with database-enforced exactly-one and match. REJECTED"). Per §1.1 above, this arm is evaluated together with accepted Q2-EX-O1, so accepted authority governs where the two sources differ, and the contract below carries no separate discriminator column and no discriminator/slot agreement invariant. That older document is not edited by this artifact.

| Dimension | Result | Evidence / rationale | Decision dependency |
|---|---|---|---|
| A1 Durable subject resolvability | PASS | "Exactly one authorized subject-reference path is populated for every committed AuditRecord. That guarantee is enforced at the database persistence boundary..." (`ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`, "Decision"). Satisfies D1-CLAR-01's structural-realization branch: "A realization that carries the kind structurally — for example, by which typed reference path of a fixed, architecture-authorized set is populated — likewise satisfies it, provided that the realization guarantees property 2" (`ADW07_D1_DISCRIMINATOR_REALIZATION_CLARIFICATION.md` §2) — which Q2-EX-O1 supplies. Under accepted O1 this is the only branch that applies to BR3, since the token branch belongs to the rejected O2 shape. | The exact constraint expression, columns, indexes, and migration mechanism are explicitly left to the later Q2 representation decision (`ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`, "Decision"). |
| A2 Committed reference meaning | PASS | Q2-EX's own consequences: "Committed records are not rewritten and their subject kinds remain determined by the path already populated, satisfying D3 and D4" (`ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`, "Accepted consequences"). | — |
| A3 Subject vs actor separation | PASS | Consistent with D4; no actor/context substitution present. | — |
| A4 Event/AuditRecord assumption | PASS | No dependency on Event, Outbox, or Publication-Intent identity. | — |
| A5 Retention exclusion | PASS | A5 excludes retention duration as a selection criterion (D10 §9); not addressed by the BR3 contract. | — |
| A6 No presumptive representation | PASS | This PASS is not to be read as making BR3's selection more likely — accepted Q2-EX's own conditionality clause governs (`ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`, "Conditionality"). See §3 above for how this comparison treats the resulting asymmetry with the other three arms. | — |
| S1 Workspace as subject | SUPPORTED | Dedicated Workspace slot; no parent workspace invented. | — |
| S2 User as subject | SUPPORTED | Dedicated User slot; contract does not require `workspace_id` for User. | — |
| S3 WorkspaceMembership as subject | SUPPORTED | Distinct dedicated slot separate from the User slot preserves the D2 boundary. | — |
| S4 EnterpriseObject as subject | SUPPORTED | Dedicated slot; other subjects are not forced into this slot. | — |
| S5 Task as subject | SUPPORTED | Dedicated slot, conventional case. | — |
| S6 Subject deletion | SUPPORTED | "The populated FK identifies the live target while it exists" (`Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §5); the committed populated-slot state (which path, plus its identifier) remains the historical subject identity under D3 even where later lifecycle authority permits loss of live dereference, per Q2-EX's "Accepted consequences" quoted at A2 above. | FK delete action (RESTRICT/CASCADE/SET NULL) is explicitly not chosen in this bounded realization (`Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §5, "Explicit exclusions"; D3 leaves this open, `ADW07_D3_SUBJECT_DELETION_DECISION.md` §5). |
| S7 Lifecycle change | SUPPORTED | Same reasoning as S6. | — |
| S8 New subject type | SUPPORTED | A sixth type would add one new nullable slot and extend the database-enforced exactly-one guarantee to cover it; because Q2-EX-O1 uses no separate scalar kind column, there is no parallel discriminator vocabulary to extend in step. This is a schema-migration cost. Per D5 guardrail 1, it is recorded as a non-ranking observation, not a comparative penalty. | — |
| S9 R1 unresolved | NOT APPLICABLE | No dependency on Event/Outbox/Publication-Intent identity. | — |
| S10 Cross-workspace ambiguity | SUPPORTED | Each slot targets one concrete table with its own FK; the `Workspace`/`User` shape asymmetry does not create ambiguity because each type has its own dedicated slot rather than a shared shape. Because kind is determined structurally rather than by a separately stored value, there is also no possibility of a discriminator/slot disagreement — that was precisely the risk Q2-EX-O2 carried and Q2-EX rejected. | — |
| C1 Queryability | qualitative | Q2-EX draws a three-way distinction that this evaluation follows exactly: "Filtering by a known subject kind remains direct and indexable, since it is a predicate over one reference path. What becomes derived is returning or grouping by the subject kind as a value, which requires logic over the authorized reference paths" (`ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`, "Accepted consequences"). Concretely: (1) filtering by a known kind (e.g. "kind = Task") is a direct, indexable predicate on the Task path being populated; (2) looking up a known subject is a direct predicate or join through that type's own FK path; (3) returning, grouping, ordering, or projecting kind as a scalar value across heterogeneous records requires derived logic over the authorized paths, since no path is itself a stored kind label. This third case is the query-ergonomics cost Q2-EX accepted knowingly: O5 — a derived column computing the kind from which path is populated — would supply that scalar ergonomics but "is not authorized now because no query workload has been observed that requires it," with its own named reopen condition: "a demonstrated query or operational requirement for kind-as-a-value retrieval that derived logic over the reference paths does not serve acceptably in practice" (`ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`, Q2-EX-O5 disposition). This is a known, accepted, reopenable cost — the record itself frames it as accepted knowingly against `docs/adr/0005-audit-first-mutations.md`'s queryability expectation, not as an unresolved defect. | — |
| C2 Integrity characteristics | qualitative | Q2-RI credit: **POSITIVE** for the five concrete per-target relations (`Q2_POST_Q2_ST_BOUNDED_REAPPLICATION_v0.1.md` §5) — weighted per §2 above as one C2 input, not a gate. Separately, and not creditable as referential integrity: "Cross-slot exclusivity is a separate integrity property and is not credited as referential integrity merely because per-type FKs exist" (`Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §5); accepted Q2-EX confirms "Accepted Q2-RI is therefore neutral across the Q2-EX option set and did not decide this question" (`ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`, "Position under accepted Q2-RI"). | — |
| C3 Extensibility | qualitative | See S8: a sixth type requires a new slot and an extended exactly-one guarantee, with no parallel discriminator-vocabulary change since none is stored under O1. Per D5 guardrail 1, recorded as a non-ranking observation, not a comparative credit or penalty. | — |
| C4a Write/storage cost | qualitative | Five nullable UUID columns present on every row (four always NULL for any given record); no separate scalar kind column under accepted Q2-EX-O1. BR1 and BR4 each use two columns for the same purpose. | — |
| C4b Read/query cost | qualitative | Direct FK join for identifier-based retrieval on a known slot. Filtering by a known kind uses the populated-path predicate noted under C1. Returning or grouping kind as a value across heterogeneous records requires the derived logic noted under C1, not an equality filter. | — |
| C4c Migration cost | qualitative | One-time now; a future sixth type requires an actual schema migration — a new nullable slot column plus an extended exactly-one constraint. No parallel discriminator-vocabulary migration is needed since none exists under accepted O1. | — |
| C5 Evolution/reversibility | qualitative | "Expansion of the authorized kind set is bounded. Where a further subject kind is authorized under accepted D5 and Q2-ST, expansion adds one authorized reference path and extends the exactly-one guarantee. Committed records are not rewritten... Only one representation of kind evolves, because only one exists." (`ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`, "Accepted consequences") — a direct consequence of there being no separate stored discriminator to fall out of step with the slots. | — |

### 6.3 BR4 / N4 — Typed opaque identity plus durable resolution contract

Minimal contract: `docs/planning/Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §6 — explicit `subject_type` plus an opaque `subject_key`, not assumed FK-compatible with the concrete subject table; an explicit durable resolution contract maps `(subject_type, subject_key)` to the historical subject identity.

**Reading adopted for A1/S10 — Project Owner ruling.** A bounded realization's own stipulated contract counts at the admissibility layer, at the same level for every arm; undesigned concrete mechanics are recorded as comparative cost, not A1 non-conformance. Applying A1's own three diagnostic questions (`docs/planning/Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md` §2, A1) in turn:

- *"Does the persisted record identify the concrete subject instance?"* The persisted reference is the pair `(subject_type, subject_key)`, and the bounded contract stipulates an explicit durable resolution contract mapping that pair to the historical subject identity (`docs/planning/Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §6).
- *"Can the subject type be determined directly or through an explicitly defined durable convention?"* Directly: `subject_type` is persisted. A1's own text notes that type disambiguation "was later resolved separately by accepted D1 authority" (`docs/planning/Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md` §2, A1), so this diagnostic does not carry the weight the identifier-resolution question below does.
- *"Does resolution survive independently of request state, logs, session memory, transient actor context, or other non-durable information?"* Yes: the pair is persisted and durable, independent of any of those sources.

A1 is satisfied at this level for BR4, on the same basis it is satisfied for the other three arms: a stipulated contract, not a fully engineered mechanism.

For S10, the framework's own question is "can subjects from different architectural scopes become indistinguishable under the persisted reference contract?" (`docs/planning/Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md` §5). `subject_type` is part of the persisted reference contract, so cross-kind indistinguishability cannot arise from the `subject_key` component alone — two records with different `subject_type` values are never confusable under this contract regardless of `subject_key`. A mis-mapping *within* one subject type — the resolver resolving a given `subject_key` to the wrong row of the same type — would be a violation of the stipulated resolution contract's own guarantee, not a separate, unclosed architectural dimension that S10 exists to expose. S10 is therefore SUPPORTED.

**The strongest objection, answered.** BR3's exactly-one guarantee comes from accepted Q2-EX; BR4's resolution contract comes from a document whose own header reads "Authority: None. These are evaluation realizations, not approved persistence designs." If both count toward admissibility, what did Q2-EX add? Q2-EX was not required to establish BR3's admissibility in the abstract — it was required because BR3's five-slot structure makes an actually invalid persisted state possible: zero or several populated paths at once, which D1-CLAR-01 property 2 (determinacy) does not tolerate. That structural possibility forced a real decision about where and how exactly-one is enforced, and Q2-EX is that decision. BR4's bounded contract admits no analogous invalid persisted state — there is exactly one `subject_type` field and exactly one `subject_key` field, so there is no multi-valued state for an equivalent decision to resolve, the same structural point §3 above makes for BR1 and BR5. What remains open for BR4 is not an admissibility question but a design-detail question — the resolver's concrete key encoding, namespace, and versioning — and it is recorded as comparative cost under C2, C4b, C4c, and C5 below, not claimed as an existing mechanism and not designed here.

**The reading not adopted.** An earlier pass held that a stipulation inside a non-authoritative evaluation document cannot establish admissibility, which would make BR4's A1 and S10 both UNDETERMINED — DECISION REQUIRED pending a concrete resolver design. That reading was not adopted because it does not survive being applied evenly: BR1's dispatch mapping and BR5's content-versioning mechanism are stipulated in exactly the same non-authoritative document and were not held to that stricter standard. Applying it only to BR4 would have been an undocumented double standard rather than a principled distinction.

| Dimension | Result | Evidence / rationale | Decision dependency |
|---|---|---|---|
| A1 Durable subject resolvability | PASS | The persisted reference is the pair `(subject_type, subject_key)`; the bounded contract stipulates an explicit durable resolution contract mapping that pair to historical subject identity (`Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §6). Subject type is determined directly, since `subject_type` is persisted. The pair is durable and independent of request state, logs, session memory, or transient actor context. See "Reading adopted" above for the full derivation and the answered objection. | The resolver's concrete key-encoding, namespace, and versioning mechanics are undesigned and are recorded as comparative cost under C2/C4b/C4c/C5 below, not as an A1 dependency. |
| A2 Committed reference meaning | PASS | "Historical interpretation of committed keys must remain stable/versioned rather than silently repointed" (`Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §6) is a requirement on whatever resolver is built. | The versioning mechanism itself is not designed here; recorded as comparative cost under C5. |
| A3 Subject vs actor separation | PASS | No actor/context substitution present. | — |
| A4 Event/AuditRecord assumption | PASS | No dependency on Event/Outbox/Publication-Intent identity. | — |
| A5 Retention exclusion | PASS | A5 excludes retention duration as a selection criterion (D10 §9); not addressed by the BR4 contract. | — |
| A6 No presumptive representation | PASS | Evaluated under the same neutrality rule as every other arm. | — |
| S1 Workspace as subject | SUPPORTED | The `(subject_type=Workspace, subject_key)` shape does not invent a parent workspace. | — |
| S2 User as subject | SUPPORTED | Same reasoning; the shape does not assume `workspace_id` for User. | — |
| S3 WorkspaceMembership as subject | SUPPORTED | Distinct `subject_type` value keeps membership identification distinct from User at the shape level. | — |
| S4 EnterpriseObject as subject | SUPPORTED | Canonical case, same shape-level reasoning. | — |
| S5 Task as subject | SUPPORTED | Conventional case, same shape-level reasoning. | — |
| S6 Subject deletion | SUPPORTED | The contract requires that "historical interpretation of committed keys must remain stable/versioned rather than silently repointed," directly addressing D3 survival as a requirement on the eventual resolver. | The resolver's concrete versioning mechanism is undesigned; recorded as comparative cost under C5. |
| S7 Lifecycle change | SUPPORTED | Same reasoning as S6. | Same as S6. |
| S8 New subject type | SUPPORTED | Adding a sixth type extends the resolution contract's mapping, not the schema. Per D5 guardrail 1, recorded as a non-ranking observation, not a comparative credit. | — |
| S9 R1 unresolved | NOT APPLICABLE | No dependency on Event/Outbox/Publication-Intent identity. | — |
| S10 Cross-workspace ambiguity | SUPPORTED | `subject_type` is part of the persisted reference contract, so cross-kind indistinguishability cannot arise from `subject_key` alone. A mis-mapping within one subject type would violate the stipulated resolution contract's own guarantee rather than expose a separate unclosed architectural dimension. See "Reading adopted" above. | — |
| C1 Queryability | qualitative | BR4 adds a resolver indirection relative to BR1's direct typed dispatch: an opaque key requires the resolver's mapping step to reach the concrete subject table, rather than a direct join. This is a comparative queryability cost, not an A1/S10 conformance question — see "Reading adopted" above. | — |
| C2 Integrity characteristics | qualitative | Q2-RI credit: **NONE** — "No DB-native FK is assumed. A registry/namespace table is not introduced because doing so solely to locate enforcement in the DB would require independent abstraction justification" (`Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §6). Correctness depends on the resolver contract's own design; its concrete key-encoding, namespace, and versioning mechanics are not yet designed (`Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §6, "Explicit exclusions"), recorded here as comparative cost, not as an open admissibility question. | — |
| C3 Extensibility | qualitative | See S8: a sixth type extends the resolution contract's mapping, not the schema. Per D5 guardrail 1, recorded as a non-ranking observation, not a comparative credit. | — |
| C4a Write/storage cost | qualitative | Two columns (`subject_type`, opaque `subject_key`), the same column count as BR1. | — |
| C4b Read/query cost | qualitative | Resolving an opaque key to a concrete subject requires the resolver's mapping step even for a straightforward per-type lookup, an indirection beyond BR1's direct dispatch. The resolver's concrete mechanics — key encoding, namespace, versioning — are undesigned; recorded here as comparative read-cost, not a conformance gap. | — |
| C4c Migration cost | qualitative | Low at the relational-schema level for adding a type; the resolver's own versioning evolution — whose concrete mechanism is undesigned — carries a comparative migration/evolution cost not yet quantifiable. | — |
| C5 Evolution/reversibility | qualitative | Reversibility depends on the resolver's versioning mechanism, which A2 requires but which this bounded realization does not concretely design; recorded here as comparative cost rather than as an unresolved admissibility question. | — |

### 6.4 BR5 / N5 — Explicit subject identity inside persisted AuditRecord content

Minimal contract: `docs/planning/Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §7 — a mandatory dedicated subject-identity object with explicit `subject_type` and durable `subject_id`, inside persisted content; generic diff/actor/context/route data does not establish subject identity by implication.

| Dimension | Result | Evidence / rationale | Decision dependency |
|---|---|---|---|
| A1 Durable subject resolvability | PASS | `Q2_POST_Q2_ST_BOUNDED_REAPPLICATION_v0.1.md` §7: "CONFORMING only with a mandatory dedicated subject-identity content contract." The N5 normalization note is explicit that "mere presence of before/after data is not enough to claim PASS" (`Q2_CANDIDATE_NORMALIZATION_v0.1.md` §3, N5) — this bounded realization satisfies A1 specifically because it requires the dedicated object, with a directly meaningful `subject_id`, not merely a diff. | The content contract's schema/versioning mechanism is not designed here (`Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §7, "Explicit exclusions"); recorded as comparative cost under C5. |
| A2 Committed reference meaning | PASS | "Its schema/version semantics preserve historical interpretation of committed records" (`Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §7). | — |
| A3 Subject vs actor separation | PASS | The dedicated object explicitly excludes diff/actor/route/context data from establishing identity by implication (`Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §7, minimal persisted contract). | — |
| A4 Event/AuditRecord assumption | PASS | No dependency on Event/Outbox/Publication-Intent identity. | — |
| A5 Retention exclusion | PASS | A5 excludes retention duration as a selection criterion (D10 §9); not addressed by the BR5 contract. | — |
| A6 No presumptive representation | PASS | Evaluated under the same neutrality rule as every other arm. | — |
| S1 Workspace as subject | SUPPORTED | The dedicated object's shape is the same for every subject type; `Workspace`'s lack of `workspace_id` is irrelevant to a content-carried identity. | — |
| S2 User as subject | SUPPORTED | Same reasoning; the content object does not assume `workspace_id`. | — |
| S3 WorkspaceMembership as subject | SUPPORTED | `subject_type=WorkspaceMembership` inside the object keeps membership identity distinct from User. | — |
| S4 EnterpriseObject as subject | SUPPORTED | Canonical case, same object shape. | — |
| S5 Task as subject | SUPPORTED | Conventional case, same object shape. | — |
| S6 Subject deletion | SUPPORTED | BR5's content-carried identity does not depend on live-row dereference, so S6 holds without reference to target lifecycle. | — |
| S7 Lifecycle change | SUPPORTED | Same reasoning as S6: archival or supersession of the target row does not affect content already committed inside the AuditRecord. | — |
| S8 New subject type | SUPPORTED | A sixth type extends the content schema/version semantics; no relational column or slot is added. Per D5 guardrail 1, recorded as a non-ranking observation, not a comparative credit. | — |
| S9 R1 unresolved | NOT APPLICABLE | No dependency on Event/Outbox/Publication-Intent identity. | — |
| S10 Cross-workspace ambiguity | SUPPORTED | Explicit `subject_type` + `subject_id` inside the object disambiguates on the same basis as BR1's pair. | — |
| C1 Queryability | qualitative | BR5's subject identity is queryable only to the extent the persistence engine can address or index the dedicated content fields; no such index is assumed in this bounded realization (`Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §7). | — |
| C2 Integrity characteristics | qualitative | Q2-RI credit: **NONE** — "No ordinary FK from content to heterogeneous target tables is assumed. DB JSON/content validation may validate shape but is not treated as target referential integrity" (`Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §7). Correctness rests on write-time content-contract validation. | — |
| C3 Extensibility | qualitative | See S8: a sixth type extends the content schema/version semantics; no relational column or slot is added. Per D5 guardrail 1, recorded as a non-ranking observation. | — |
| C4a Write/storage cost | qualitative | No new relational columns beyond the existing content field(s); the dedicated object's size is not fixed the way a UUID column is. | — |
| C4b Read/query cost | qualitative | Cross-cutting subject-based queries (e.g., "all AuditRecords for Task X") require content-field parsing or an expression/generated-column index, which this bounded realization does not assume. | — |
| C4c Migration cost | qualitative | No relational schema migration needed for the object itself if a content field already exists; content-shape/version evolution carries its own, separately-undesigned versioning burden. | — |
| C5 Evolution/reversibility | qualitative | "Schema/version semantics preserve historical interpretation of committed records" is required by the bounded contract, but its concrete mechanism is not designed here — the same kind of open dependency as BR4's resolver versioning. | Content-versioning mechanism is a named, currently unresolved comparative-cost dependency. |

---

## 7. Comparative criteria across arms (§6)

This section juxtaposes the C1–C5 rows above directly. Per §6 of the framework, "Comparison follows authority checking. Comparative dimensions cannot override A1–A6," and no weights or numeric score are used. C3 cells record only what would change to add a future type; per D5 guardrail 1 (`00_ARCHITECTURE/07_AUDIT/ADW07_D5_SUBJECT_TYPE_EXTENSIBILITY_DECISION.md` §2, item 1) none of this is a ranking input.

| Criterion | BR1/N1 | BR3/N3 (+Q2-EX-O1) | BR4/N4 | BR5/N5 |
|---|---|---|---|---|
| C1 Queryability | Direct equality lookup by known subject; filtering by known kind is likewise a direct, indexable predicate, equivalent to BR3's per-path filtering. Returning or grouping kind as a value reads the stored column directly. | No scalar kind column under O1. Filtering by known kind is a direct, indexable predicate over the one relevant reference path, equivalent to BR1's filtering. Returning or grouping kind as a value across heterogeneous records requires derived logic over the authorized paths — a cost Q2-EX accepted knowingly, deferred to O5 pending demonstrated need. Per-identifier lookups on a known slot are direct FK joins. | Adds a resolver indirection relative to BR1's direct typed dispatch; retrieval by known subject requires the resolver step, whose concrete mechanics are undesigned. | Requires content-field query or index support for direct subject-history retrieval; the bounded realization assumes none. |
| C2 Integrity | No DB FK; write-time dispatch validation. Q2-RI credit: NONE. | DB FK per populated slot. Q2-RI credit: POSITIVE for the five target relations; exactly-one is a separate, already-accepted (Q2-EX) property, not itself RI credit. | No DB FK; correctness depends on the resolver contract's design, whose key-encoding/namespace/versioning mechanics are undesigned. Q2-RI credit: NONE. | No DB FK; correctness depends on write-time content validation. Q2-RI credit: NONE. |
| C3 Extensibility (non-ranking per D5 guardrail 1) | Dispatch-mapping extension only; no schema change. | New slot column plus extended exactly-one constraint; no parallel discriminator-vocabulary change since none is stored under O1. | Resolver-mapping extension only; no schema change. | Content-schema/version extension only; no relational column or slot. |
| C4a Write/storage | Two columns. | Five nullable columns per row (four always NULL for a given record); no separate scalar kind column. | Two columns. | No new relational columns if a content field already exists; content field size is not fixed the way a UUID column is. |
| C4b Read/query | Dispatch step needed to reach the concrete row for a known identifier; filtering or returning kind for a known row is direct, as under C1. | Direct FK join for identifier-based retrieval; kind-only retrieval uses the derived logic noted under C1, not an equality filter. | Resolver step needed for identifier-based retrieval, an indirection beyond BR1's direct dispatch, with undesigned concrete mechanics. | Content parsing or an index on content fields needed for cross-cutting queries. |
| C4c Migration | Minimal, one-time. | One-time now; a future sixth type requires an actual schema migration (new slot, extended constraint), with no parallel discriminator migration since none exists under O1. | Minimal at the schema level; resolver-versioning cost is separate and undesigned. | No schema migration for the object itself; content-versioning cost is separate and undesigned. |
| C5 Evolution/reversibility | Stable pair format; new types add values, not rewrites. | "Committed records are not rewritten... Only one representation of kind evolves, because only one exists" (`ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`) — a direct consequence of there being no separate stored discriminator. | Depends on the resolver's versioning mechanism, which is required but not yet designed. | Depends on the content's versioning mechanism, which is required but not yet designed. |

None of the differences recorded above are converted into a ranking. Per §8's representation-neutrality rule, "must have a foreign key," "must use one column," and "must live outside the payload" are explicitly *not* admitted as criteria merely by assumption (`Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md` §8) — so BR3's DB-FK-heavy C2/C4b story and BR1/BR4/BR5's lighter-schema stories are recorded as facts about each realization, not scored against an implicit "FK is better" or "fewer columns is better" premise.

---

## 8. Stress tests across arms (§5)

| Stress test | BR1/N1 | BR3/N3 | BR4/N4 | BR5/N5 |
|---|---|---|---|---|
| S1 Workspace as subject | SUPPORTED | SUPPORTED | SUPPORTED | SUPPORTED |
| S2 User as subject | SUPPORTED | SUPPORTED | SUPPORTED | SUPPORTED |
| S3 WorkspaceMembership as subject | SUPPORTED | SUPPORTED | SUPPORTED | SUPPORTED |
| S4 EnterpriseObject as subject | SUPPORTED | SUPPORTED | SUPPORTED | SUPPORTED |
| S5 Task as subject | SUPPORTED | SUPPORTED | SUPPORTED | SUPPORTED |
| S6 Subject deletion | SUPPORTED | SUPPORTED | SUPPORTED | SUPPORTED |
| S7 Lifecycle change | SUPPORTED | SUPPORTED | SUPPORTED | SUPPORTED |
| S8 New subject type | SUPPORTED | SUPPORTED | SUPPORTED | SUPPORTED |
| S9 R1 unresolved | NOT APPLICABLE | NOT APPLICABLE | NOT APPLICABLE | NOT APPLICABLE |
| S10 Cross-workspace ambiguity | SUPPORTED | SUPPORTED | SUPPORTED | SUPPORTED |

No arm carries an UNDETERMINED result under this evaluation. Every S8 SUPPORTED result means only that the arm can accommodate a future authorized type without corrupting committed records or requiring reinterpretation; per D5 guardrail 1 the differing extension costs recorded in §6's per-arm tables and §7's C3 row are not converted into a ranking here. BR4's resolver mechanics (key encoding, namespace, versioning) are recorded as comparative cost under C2/C4b/C4c/C5 in §6.3 and §7 rather than as an unresolved stress-test dependency, per the reading adopted in §6.3.

---

## 9. Decision-sufficiency test (§9)

> "If two candidates both satisfy all authoritative constraints, do the stress tests, comparative criteria, and resolved decision surfaces provide enough information to explain a rational choice between them? If not, the response is: **FRAMEWORK INSUFFICIENT — ADD OR RESOLVE DECISION DIMENSION** — not an arbitrary candidate selection." (`docs/planning/Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md` §9)

This is a test of whether enough information exists to support a rational, explicable choice — not a test of whether every arm carries the same amount of decision paperwork. §3 above already establishes that BR1, BR4, and BR5 have no Q2-EX-equivalent record because none was structurally required: their exactly-one/resolvability holds by construction, so there was nothing for such a decision to resolve. Treating that structural asymmetry as a missing decision dimension here would contradict §3, and it is not the ground for the verdict below.

Under the reading adopted in §6.3, all four arms PASS A1–A6, and no arm carries an UNDETERMINED stress-test result (§8). Every arm therefore satisfies the precondition §9's own test states — "candidates [that] both satisfy all authoritative constraints" — so the comparative half of the test applies to all four together, not to a subset.

§7's comparative table shows real, cited, non-arbitrary differences among the four, none of which dominates on every dimension: BR3 carries per-target DB-FK integrity credit and a bounded, accepted evolution story, at the cost of derived logic to return kind as a value across heterogeneous records and a schema migration on a future sixth type; BR1 needs an application-level dispatch step to reach a concrete row and carries no DB-RI credit, but adds no new columns beyond the pair and extends by vocabulary rather than schema; BR4 needs a resolver indirection whose concrete key-encoding, namespace, and versioning mechanics are not yet designed, and carries no DB-RI credit; BR5 requires content-field query or index support this bounded realization does not assume, but adds no relational column and its content-carried identity does not depend on live-row dereference.

The framework does not resolve this kind of qualitative tradeoff by formula: "No weights or numeric score are proposed in v0.1" (`docs/planning/Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md` §6). That is a deliberate feature of the approved procedure, not a gap in it — the procedure's own flow routes exactly this kind of qualitative comparison to "PROJECT OWNER DECISIONS WHERE NECESSARY" downstream of it (`docs/planning/Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md` §1). Having real, evidenced, distinguishing tradeoffs to weigh across all four arms is what makes a Project Owner choice rational rather than arbitrary; it is not evidence that the framework is insufficient.

**Decision-sufficiency result: the test is satisfied.** All four bounded arms conform to A1–A6, no stress test is left unresolved for any of them, and their comparative differences are recorded with citations. The response §9 reserves for the negative case — `FRAMEWORK INSUFFICIENT — ADD OR RESOLVE DECISION DIMENSION` — is not triggered.

What remains is a qualitative weighing among real tradeoffs — a Project Owner judgment the procedure reserves for the next step, not a gap this artifact is positioned to fill. This artifact does not perform that weighing, does not select or rank an arm, and does not treat any arm's particular cost or credit profile as a reason to prefer it.

---

## 10. Forward note — not an action

`docs/planning/Q2_FINAL_REPRESENTATION_DECISION_PRECONDITIONS_v0.1.md` §6 requires that the eventual Q2 representation authority carry an explicit implementation-boundary clause:

> "This decision closes the ADR-0014 Q2 persisted subject-reference representation blocker only. It does not by itself authorize the current full WP19 `model/repository/service` deliverable, does not establish actor-attribution / ActorContext semantics, and does not waive the need for a separately approved WP19 scope amendment if the next implementation pass is narrower than the currently recorded WP19 deliverable. WP19 remains BLOCKED / UNAUTHORIZED until the applicable planning-scope and remaining architecture gates for the intended implementation pass are explicitly cleared." (`docs/planning/Q2_FINAL_REPRESENTATION_DECISION_PRECONDITIONS_v0.1.md` §6)

And §4 requires that the final Q2 authority not silently perform the WP19 backlog amendment:

> "Therefore, if the intended first WP19 implementation pass is schema-only (model + migration + tests), a **separate Project Owner-approved WP19 scope amendment** is required before that narrowed implementation pass is treated as the authorized WP19 deliverable. The final Q2 representation decision must not silently perform that backlog amendment unless it explicitly says it is doing so and the Project Owner approves that additional scope decision." (`docs/planning/Q2_FINAL_REPRESENTATION_DECISION_PRECONDITIONS_v0.1.md` §4)

This artifact records both requirements as a forward note for whoever drafts the eventual Q2 representation decision. It does not draft that clause, does not perform the WP19 scope amendment, and does not edit `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md`.

---

## 11. What this artifact does not do

Consistent with `docs/planning/Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md` §10, this artifact does not:

- select, recommend, rank, reject, or enumerate a final Q2 persisted representation;
- amend, supersede, or edit any accepted decision record (D1, D1-CLAR-01, D2, D3, D4, D5, Q2-RI, Q2-ST, Q2-EX), including header metadata;
- edit `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md` or perform the WP19 scope amendment described in §10 above;
- resolve the Event/AuditRecord relationship, Block 2 Residual Question R1, GC-006, GC-007, or ActorContext/ADW-02;
- authorize WP19 implementation, or any model, migration, repository, service, or API work;
- create an ADR or close ADW-07.

**Q2 persisted representation: OPEN / NOT ESTABLISHED. WP19: BLOCKED / UNAUTHORIZED. ADW-07: OPEN.**
