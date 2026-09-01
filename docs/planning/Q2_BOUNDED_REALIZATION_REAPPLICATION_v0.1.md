# WP19 / Q2 Bounded Realization Re-application v0.1

**Status:** Draft — evaluation only  
**Date:** 2026-08-30  
**Subject:** D1–D5 + accepted Q2-RI application to BR1–BR5  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact compares; it does not select a persisted representation.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Inputs

- D1–D5: CLOSED — ACCEPTED.
- Q2-RI: CLOSED — ACCEPTED — O2 PREFERENCE.
- Q2-ST: OPEN.
- Bounded realizations BR1–BR5: evaluation designs only in `Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md`.

Q2-RI comparative credit is applied per realization and every application records reasoning. Absence of ordinary FK enforcement is not automatic rejection.

## 2. Summary matrix

| Realization | D1 | D2 | D3 | D4 | D5 current scope | Q2-RI credit | Evaluation position |
|---|---|---|---|---|---|---|---|
| BR1 / N1 typed polymorphic | PASS | PASS | PASS* | PASS | PASS | NONE | Conforming bounded realization; app/domain validation burden |
| BR2 / N2 composite-FK family | FAIL current-scope sufficiency | UNDETERMINED for asymmetric types | PASS* locally | FAIL current-scope completeness | FAIL current five | LOCAL ONLY | Not sufficient as current five-type realization |
| BR3 / N3 per-type relations | PASS | PASS | PASS* | PASS | PASS | POSITIVE | Conforming bounded realization; wider shape + exclusivity burden |
| BR4 / N4 typed opaque | PASS | PASS | PASS* | PASS if durable resolver contract is explicit | PASS | NONE | Conforming only with resolver-contract burden |
| BR5 / N5 dedicated content identity | PASS | PASS | PASS* | PASS if dedicated content contract is explicit | PASS | NONE | Conforming only with content/query-validation burden |

`PASS*` on D3 means the realization preserves committed historical identity independently of continued live dereference; it does not decide target deletion policy or FK delete action.

## 3. BR1 / N1 — typed polymorphic reference

### D1–D5

**PASS as bounded realization.**

Reasoning:

- D1: explicit durable `subject_type` identifies one of the current five kinds; one `subject_id` is paired with it.
- D2: `Workspace` can be the subject itself; workspace context for other subjects is not substituted for subject identity.
- D3: the committed typed identifier remains historical identity even if a live target later becomes unavailable. This requires stable type-dispatch interpretation, not permanent live dereference.
- D4: subject identity is explicit and canonical rather than inferred from actor/context/payload. Write-time validation plus durable type-dispatch semantics provide the explicit alternative mechanism required when ordinary FK enforcement is absent.
- D5: all five current kinds can be represented. No future kind is pre-authorized.

### Q2-RI

**Comparative credit: NONE for this bounded realization.**

Recorded reasoning:

- DB-enforced target RI: no ordinary multi-target FK is provided.
- Abstraction test: adding a registry/base table solely to obtain FK enforcement would be an additional persistence abstraction whose justification would be enforcement location; BR1 therefore does not add it.
- Alternative mechanisms: explicit write-time subject validation, durable type dispatch, immutable committed typed identity, and historical interpretation contract.
- Other constraints: no contradiction with D1–D5 is created by locating target validation outside an ordinary FK.

**Effect:** BR1 is not disqualified. It simply receives no Q2-RI comparative credit.

## 4. BR2 / N2 — composite-FK family

### D1–D5

**FAIL as a complete current Q2 bounded realization.**

Reasoning:

- the existing corpus-supported composite shape applies naturally only where the target exposes the relevant composite identity;
- current `Workspace` is the boundary and has no `workspace_id`;
- current `User` has no `workspace_id`;
- BR2 deliberately does not invent synthetic workspace keys or a universal registry;
- therefore one complete durable reference contract covering all five D1/D5 kinds is not established.

This is a current-scope sufficiency failure of BR2, not an architecture rejection of every possible future design that could be called composite-FK.

### Q2-RI

**Comparative credit: LOCAL ONLY; no Q2-wide credit.**

Recorded reasoning:

- DB-enforced RI exists where an applicable composite relation is concretely defined.
- No extra abstraction is required for those already-compatible relations.
- That local property cannot compensate for failure to cover the complete current D1/D5 scope.
- GC-002 Alternative B remains proposed only.

**Effect:** BR2 must not be selected as the current five-type Q2 representation in this form.

## 5. BR3 / N3 — per-type nullable relations

### D1–D5

**PASS as bounded realization.**

Reasoning:

- D1: explicit `subject_type`, exactly one populated type-specific subject slot, and discriminator/slot agreement identify exactly one current kind.
- D2: Workspace has its own subject relation and is not substituted for context on another subject.
- D3: the committed discriminator plus identifier value preserves historical identity; live dereference is a separate lifecycle question. FK delete action remains undecided and must not erase or reinterpret committed identity.
- D4: subject identity is explicit and canonical. Multiple physical paths do not violate one logical subject identity because exactly-one/discriminator-match is an explicit invariant.
- D5: five current kinds are covered. A future kind may require schema evolution, which D5 permits and does not rank against BR3 by extensibility convenience alone.

### Q2-RI

**Comparative credit: POSITIVE for the five concrete target relations.**

Recorded reasoning:

- DB-enforced RI: each subject-specific UUID relation can target the existing corresponding table primary key with an ordinary FK.
- Abstraction test: no auxiliary registry/base table or other persistence abstraction is introduced solely to locate enforcement; the relations are the representation itself.
- Alternative mechanisms: the exactly-one/discriminator-match invariant still needs explicit enforcement; Q2-RI credit for FKs does not pretend that FKs solve cross-slot exclusivity.
- Other constraints: FK delete actions must be chosen consistently with D3 and historical-record authority; no cascade behavior is implied by this evaluation.

**Effect:** BR3 receives a real comparative advantage under accepted Q2-RI. This is not automatic representation selection.

## 6. BR4 / N4 — typed opaque identity

### D1–D5

**PASS only under the bounded realization's explicit durable resolver contract.**

Reasoning:

- D1: type is explicit; opacity applies to the key, not to subject-kind identity.
- D2: resolver semantics must distinguish Workspace-as-subject from workspace context.
- D3: historical resolver semantics must remain stable/versioned when live target availability changes.
- D4: the resolver contract must make identity independently resolvable and cannot infer it from context/payload.
- D5: current five can be mapped without pre-authorizing future kinds.

### Q2-RI

**Comparative credit: NONE.**

Recorded reasoning:

- no ordinary DB FK is part of BR4;
- no registry is introduced solely to manufacture DB RI;
- alternative mechanisms are write validation plus a durable historically stable resolution contract;
- those mechanisms keep BR4 admissible but add semantic infrastructure that must itself be governed.

## 7. BR5 / N5 — dedicated subject identity in persisted content

### D1–D5

**PASS only under the bounded realization's explicit mandatory content contract.**

Reasoning:

- D1: dedicated content contains explicit subject type and durable identifier;
- D2: subject identity is not replaced by workspace context;
- D3: committed content remains historical identity under stable schema/version interpretation;
- D4: the dedicated subject object is canonical and mandatory, not inferred from generic payload/diff/actor/context;
- D5: the contract covers the five current kinds without pre-authorizing future kinds.

### Q2-RI

**Comparative credit: NONE.**

Recorded reasoning:

- no concrete DB target FK is supplied by the content representation;
- no generated-column/trigger/registry design is invented to gain RI credit;
- alternative mechanisms are mandatory content-schema validation, write-time target validation, and stable version-aware interpretation;
- queryability/indexing remains a separate burden and no favorable DB feature is assumed.

## 8. Comparative result after concrete re-application

The bounded pass materially changes the comparison:

1. **BR2/N2 is not sufficient in its bounded corpus-grounded form** for all five current subject kinds.
2. **BR1/N1 and BR3/N3 both have bounded conforming realizations.**
3. **BR3 receives positive Q2-RI comparative credit; BR1 receives none but is not penalized or rejected.**
4. **BR4 and BR5 remain possible only by carrying explicit resolver/content-contract infrastructure and receive no RI credit in the bounded forms.**
5. The Q2-RI advantage of BR3 is now reasoned from an actual realization, not attributed to N3 by class name.

This pass still does **not** select BR3. Remaining comparative burdens include:

- BR3: wider/sparser relational shape, cross-slot exclusivity, cross-type query complexity, schema change when future kinds are separately authorized;
- BR1: application/domain validation and durable type-dispatch/resolution contract without DB target RI;
- BR4: resolver/namespace governance;
- BR5: content contract, queryability, and validation/indexing burden.

C1/C2/C4/C5 must be read together with accepted Q2-RI; RI credit is one comparative input only.

## 9. Q2-ST boundary

Q2-ST remains OPEN and no conclusion above determines its answer.

The BR realizations deliberately use only the current five D1/D5 kinds. Q2-ST may change how future or standalone persisted identities map to logical subject kinds and can therefore change the concrete burden of BR1/BR3/BR4/BR5.

Accordingly:

**do not create the final Q2 representation decision yet.**

The next substantive step is Q2-ST. After Q2-ST acceptance, re-check whether the accepted ranging rule changes any BR realization or comparative conclusion. Only then prepare the final Q2 persisted-representation decision for Project Owner approval.

## 10. Gate result

**BOUNDED CONCRETE RE-APPLICATION COMPLETE — BR3 EARNS Q2-RI CREDIT WITHOUT AUTOMATIC SELECTION — BR1 REMAINS CONFORMING WITHOUT RI CREDIT — BR2 INSUFFICIENT IN CURRENT FORM — BR4/BR5 REMAIN QUALIFIED ALTERNATIVES — Q2-ST OPEN — FINAL Q2 REPRESENTATION NOT AUTHORIZED.**

WP19 remains **BLOCKED / UNAUTHORIZED**.
