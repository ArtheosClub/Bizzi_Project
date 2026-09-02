# WP19 / Q2-EX — BR3 Exclusivity / Discriminator Consistency Options v0.1

**Status:** Draft — bounded options/evaluation only  
**Date:** 2026-08-30  
**Subject:** BR3/N3 — one logical subject identity, type qualification, exactly-one slot, and discriminator consistency  
**Decision owner:** Project Owner through ADW-07  
**Authority:** None. This artifact exposes and evaluates Q2-EX; it does not select BR3 or a Q2 representation.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Bounded question

BR3/N3 represents the audited subject through subject-type-specific persisted reference slots. Accepted D1 requires an explicit durable subject-type discriminator but expressly states that **type qualification within a durable subject identity satisfies this rule** and does not decide physical placement.

Accepted D4 requires one mandatory, explicit, stable, independently resolvable audited-subject identity. Accepted D3 requires the committed historical identity to remain stable. A BR3 record that permits more than one populated subject slot, no populated slot, or disagreement between an explicit type value and the populated slot does not establish one unambiguous logical subject identity.

Therefore Q2-EX asks:

> **If BR3/N3 remains a live representation candidate, how is exactly one current subject type durably established: by structural qualification through exactly one populated type-specific slot, or by a separately persisted discriminator plus an invariant binding that discriminator to exactly one populated slot; and, for the latter, where is that invariant enforced?**

Q2-EX is representation-specific. BR1/BR4/BR5 do not expose the same duplicate-type-fact problem in their current bounded realizations because each uses one subject-reference path. BR2 is already insufficient in its current corpus-grounded form.

## 2. Why this is architecture, not implementation detail

The normalized candidate analysis explicitly did **not** assume exactly-one population or a CHECK mechanism. The bounded BR3 realization later required an exactly-one/discriminator-match invariant in order to satisfy D1/D4, but left the enforcement mechanism undecided.

This is not merely validation ergonomics:

- zero populated slots means no audited subject identity;
- multiple populated slots mean more than one candidate audited subject;
- an explicit discriminator that disagrees with the populated slot creates two contradictory durable representations of subject type;
- once committed, such contradiction is historical data and cannot be repaired by mutating the committed AuditRecord consistently with D3/D10 historical-record permanence.

The invariant is therefore a conformity condition for BR3, and its representation/enforcement cost belongs in the comparison before BR3 can be selected.

## 3. Inherited authority

Q2-EX must preserve:

- **D1:** explicit durable type disambiguation; type qualification within durable identity is sufficient; physical placement is not predetermined;
- **D3:** committed historical subject identity remains stable;
- **D4:** exactly one mandatory explicit audited-subject identity, independently resolvable;
- **D5:** current scope is the five accepted subject kinds;
- **Q2-RI:** stronger DB-enforced integrity earns comparative credit per concrete realization when it does not require an unjustified abstraction or contradict accepted constraints;
- **Q2-ST-O2:** current five kinds follow canonical persisted subject identity by default; no new kind or mapping exception is introduced here.

Q2-EX does not reopen D1–D5, Q2-RI, or Q2-ST.

## 4. Options

### Q2-EX-O1 — Structural type qualification; no separate discriminator column in BR3

**Rule:** exactly one of the five type-specific subject-reference slots is populated. The identity of that populated slot is itself the explicit durable subject-type qualification required by D1. No second persisted type discriminator is stored for the same subject reference.

For example, a populated Workspace slot durably qualifies the subject as `Workspace`; a populated Task slot qualifies it as `Task`.

**Required invariant:** exactly one current subject slot is populated for every committed AuditRecord.

**D1:** compatible. D1 explicitly allows type qualification within durable subject identity and does not require a dedicated discriminator column.

**D3/D4:** compatible if exactly-one is durably enforced; there is only one persisted representation of type, so discriminator/slot disagreement is structurally impossible.

**Q2-RI:** ordinary FKs on the five slots still receive target-RI credit. Exactly-one integrity is a separate property. If DB enforcement of exactly-one is available without an unjustified abstraction, it can receive comparative credit for stronger integrity in the concrete BR3 realization; application-only enforcement remains possible but receives less DB-integrity credit for that property.

**Costs / consequences:**

- eliminates duplicated type state;
- queries that need a single scalar `subject_type` must derive it from which slot is populated;
- any index/query abstraction for scalar type access is an implementation concern unless it becomes necessary for accepted query requirements;
- a future separately authorized subject kind under BR3 normally adds another slot and extends the exactly-one rule.

### Q2-EX-O2 — Separate persisted discriminator + DB-enforced exactly-one/match invariant

**Rule:** BR3 stores both (a) a separate explicit `subject_type` value and (b) five type-specific subject-reference slots. The database must enforce that exactly one slot is populated and that the populated slot corresponds to the committed discriminator value.

**D1:** compatible; discriminator is explicit and dedicated.

**D3/D4:** compatible if the DB invariant is complete. Contradictory durable type representations are rejected before commit.

**Q2-RI:** receives stronger DB-integrity credit than the same duplicated representation with application-only consistency, provided the enforcement uses ordinary constraints over the representation itself and does not require a new abstraction justified only by enforcement location.

**Costs / consequences:**

- stores subject type twice: once as scalar discriminator and once structurally through the populated slot;
- requires a five-way consistency/exclusivity constraint whose complexity grows when separately authorized kinds are added;
- makes scalar type queries straightforward;
- schema/migration evolution must update both slot set and consistency rule.

No concrete SQL CHECK expression, generated column, trigger, or migration is authorized by this option artifact.

### Q2-EX-O3 — Separate persisted discriminator + application/service-enforced exactly-one/match invariant

**Rule:** BR3 stores the same duplicated discriminator + type-specific slots as O2, but exactly-one and discriminator/slot agreement are enforced by the audited application/service path rather than by a DB constraint.

**D1:** compatible at the data-contract level only if every committed row satisfies the invariant.

**D3/D4:** potentially compatible, but the historical correctness boundary depends on application enforcement covering every write path. A contradictory row that reaches committed persistence violates the accepted subject-identity contract and cannot be treated as a recoverable ordinary validation defect.

**Q2-RI:** receives no DB-integrity credit for discriminator/slot consistency. The five ordinary target FKs can still receive their existing target-RI credit. Under accepted Q2-RI, O3 is not automatically disqualified merely because the consistency invariant is application-enforced, but the weaker enforcement location is a real comparative difference from O2.

**Costs / consequences:**

- retains duplicated type state and its drift risk;
- requires a complete write-path invariant and tests against bypass paths;
- direct DB writes/migrations/imports need independent protection or validation discipline;
- scalar type querying remains straightforward.

### Q2-EX-O4 — Separate discriminator without mandatory exactly-one/match invariant

**Evaluation:** conflicts with D3/D4 and is recommended for rejection.

A representation that permits zero/multiple slots or disagreement between durable discriminator and slot does not guarantee one stable audited-subject identity. Technical ability to store such rows does not satisfy the accepted semantic contract.

This planning artifact recommends rejection; only explicit architecture authority can close Q2-EX.

### Q2-EX-O5 — Derived, non-independently-writable kind projection over structural qualification

**Evaluation:** not an alternative to O1–O4 — an augmentation of O1. Viable, but no demonstrated need; recommended for deferral rather than selection or rejection.

A database-derived column computes the subject kind from which authorized reference path is populated. It provides the scalar type-query ergonomics of O2/O3 without their agreement invariant, because a derived value is not independently written and therefore cannot disagree with the state it is computed from. It presupposes structural qualification and adds nothing to the durable subject-identity contract itself.

No query workload has been observed that requires it: WP19 has no implementation and no audit rows exist, so the need is predicted rather than demonstrated. Deferring it costs little precisely because it introduces no independently written state — adding it later changes no committed fact and creates no historical-consistency obligation, unlike O2 and O3, whose duplicated state is expensive to reverse once records are permanent.

This planning artifact recommends deferral; only explicit architecture authority can close Q2-EX.

## 5. Comparative matrix

| Dimension | O1 Structural qualification | O2 Separate discriminator + DB invariant | O3 Separate discriminator + app invariant |
|---|---|---|---|
| D1 explicit type qualification | Yes — slot identity is the durable qualification | Yes — dedicated scalar | Yes — dedicated scalar |
| Duplicate durable type state | No | Yes | Yes |
| Discriminator/slot drift possible | Structurally no, if exactly-one holds | Rejected by DB | Possible if write-path enforcement fails |
| Exactly-one enforcement still required | Yes | Yes | Yes |
| DB target FK opportunity | Preserved | Preserved | Preserved |
| Additional DB integrity credit | Available if exactly-one is DB-enforced | Strongest for consistency/match | None for consistency/match |
| Scalar `subject_type` query | Derived | Direct | Direct |
| Evolution when a new kind is authorized | Add slot + extend exactly-one | Add slot + discriminator value + extend match rule | Same as O2 plus service validation |

Q2-EX-O5 is not in this matrix: it augments O1 rather than competing with it, so its rows would duplicate O1's on every dimension except the scalar type-query row.

## 6. Decision-sufficiency observation

The choice cannot be postponed until after BR3 selection without hiding a material part of BR3's conformity and cost.

In particular:

- selecting BR3 while assuming a dedicated discriminator implicitly selects duplicated durable type state;
- selecting BR3 while assuming the populated slot itself qualifies type implicitly selects O1;
- selecting BR3 with duplicated state but without deciding enforcement location leaves Q2-RI comparison incomplete.

Therefore Q2-EX should be closed **before or simultaneously with** any final Q2 decision that selects BR3.

If the final Q2 representation does not select BR3/N3, Q2-EX may be closed as NOT APPLICABLE without selecting O1/O2/O3.

## 7. Current state

- D1–D5: CLOSED / ACCEPTED.
- Q2-RI: CLOSED / ACCEPTED — O2 preference.
- Q2-ST: CLOSED / ACCEPTED — O2 persisted-entity default with explicit mapping exceptions.
- Q2-EX: **OPEN — BR3-SPECIFIC CONDITIONAL DECISION SURFACE**.
- BR1/BR3 remain conforming bounded alternatives subject to their stated burdens.
- Q2 persisted representation: OPEN / NOT ESTABLISHED.
- WP19: BLOCKED / UNAUTHORIZED.

## 8. Next bounded step

Q2-EX is now closed by accepted architecture authority; see `00_ARCHITECTURE/07_AUDIT/ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`. This artifact is retained as the options material the decision was taken on.
