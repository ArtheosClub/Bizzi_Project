# WP19 / Q2 Final Representation Decision Preconditions v0.1

**Status:** Active planning gate — non-authoritative  
**Date:** 2026-08-30  
**Scope:** Preconditions and residual implementation gates around the final ADR-0014 Q2 persisted-representation decision  
**Authority:** None. This artifact records existing accepted authority and exposed open surfaces; it does not select a representation or authorize WP19 implementation.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED.

## 1. Purpose

Accepted D1–D5, Q2-RI, and Q2-ST now establish the semantic and comparative framework needed to prepare a final persisted AuditRecord subject-reference decision. One bounded representation-specific surface remains before a BR3 selection can be made without hiding a material conformity cost: **Q2-EX — BR3 exclusivity / discriminator consistency**.

This artifact also records an independent distinction that must survive the final Q2 decision: **closing ADR-0014 Q2 does not by itself authorize the current full WP19 deliverable.**

## 2. Q2-EX prerequisite

`docs/planning/Q2_EX_BR3_EXCLUSIVITY_DISCRIMINATOR_OPTIONS_v0.1.md` exposes the BR3-specific requirement that one and only one audited subject identity be durably represented.

If BR3/N3 is selected, the final Q2 authority must either:

1. resolve Q2-EX within the same authority; or
2. rely on a separately accepted Q2-EX authority already in force.

If a non-BR3 representation is selected, the final Q2 authority may close Q2-EX as **NOT APPLICABLE TO THE SELECTED REPRESENTATION**.

A BR3 selection must not assume by implication whether D1 type qualification is structural or separately duplicated, nor where an exactly-one/discriminator-match invariant is enforced.

## 3. What final Q2 representation authority closes

The final Q2 representation decision, when accepted, closes the persistence-representation blocker created by ADR-0014 Q2 and routed into ADW-07.

It may establish the canonical persisted AuditRecord subject-reference shape and any representation-specific invariants necessary for D1–D5 conformity.

It does **not**, merely by closing ADR-0014 Q2, authorize all work currently named under WP19.

## 4. Residual WP19 gate — deliverable scope

The current `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md` WP19 entry still states a combined deliverable:

`AuditRecord model/repository/service`

The established Gate C pattern has repeatedly separated schema foundation from later repository/service work where the latter depends on unresolved audited-service semantics or neighboring architecture:

- A-02 / WP13;
- A-04 / WP15;
- A-10 / WP14;
- A-03 / WP16 provides the same split pattern for schema vs deferred behavior.

Therefore, if the intended first WP19 implementation pass is schema-only (model + migration + tests), a **separate Project Owner-approved WP19 scope amendment** is required before that narrowed implementation pass is treated as the authorized WP19 deliverable. The final Q2 representation decision must not silently perform that backlog amendment unless it explicitly says it is doing so and the Project Owner approves that additional scope decision.

## 5. Residual WP19 gate — actor attribution / ActorContext

The current WP19 entry already distinguishes:

- **what was acted on** — audited subject identity, governed by ADR-0014 Q1/Q2 and ADW-07; and
- **who acted** — actor attribution / ActorContext, tied to WP16's deferred half and ADW-02.

Closing Q2 resolves only the subject-reference representation. It does not resolve actor attribution or the deferred `ActorContext` contract.

Accordingly:

- a future schema-only WP19 amendment may explicitly bound actor attribution out of that schema foundation if architecture permits and the Project Owner approves the scope;
- the **full existing WP19 Definition of Done / service-level completion remains dependent on the actor-attribution/ActorContext surface** unless separately amended by authority;
- Q2 closure must not be reported as “WP19 fully unblocked” or “WP19 implementation authorized” without those additional gates being satisfied.

## 6. Required wording in the final Q2 representation decision

The final Q2 authority should include an explicit implementation-boundary clause substantially equivalent to:

> **This decision closes the ADR-0014 Q2 persisted subject-reference representation blocker only. It does not by itself authorize the current full WP19 `model/repository/service` deliverable, does not establish actor-attribution / ActorContext semantics, and does not waive the need for a separately approved WP19 scope amendment if the next implementation pass is narrower than the currently recorded WP19 deliverable. WP19 remains BLOCKED / UNAUTHORIZED until the applicable planning-scope and remaining architecture gates for the intended implementation pass are explicitly cleared.**

This clause prevents “Q2 closed” from being read as “WP19 can now be built end-to-end.”

## 7. Q2-ST AuditRecord trigger discoverability

Accepted `ADW07_Q2_ST_SUBJECT_TYPE_RANGING_RULE_DECISION.md` establishes a MUST reopen trigger for new/uncovered persisted subject identity forms and material canonical-identity target changes.

The trigger is expected to become operational during service-layer authorization, including potentially WP14's deferred runtime/service remainder before WP19 itself.

The canonical execution entries that should contain direct pointer-only references are:

- `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md` — WP14 entry, Deferred Concerns / runtime-service boundary;
- `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md` — WP19 entry, governing/blocker boundary.

The pointer should cite the accepted Q2-ST authority and must not duplicate or weaken its normative trigger text.

This direct-entry synchronization is planning discoverability, not new architecture authority.

## 8. Current gate state

- D1–D5: CLOSED / ACCEPTED.
- Q2-RI: CLOSED / ACCEPTED — O2 preference.
- Q2-ST: CLOSED / ACCEPTED — O2 persisted-entity default with explicit mapping exceptions.
- Q2-EX: OPEN — BR3-specific conditional surface.
- Q2 persisted representation: OPEN / NOT ESTABLISHED.
- WP19 current deliverable scope: model/repository/service — unchanged.
- WP19 schema-only amendment: NOT YET APPROVED.
- actor attribution / ActorContext: SEPARATE / UNRESOLVED.
- ADW-02 dependency for ActorContext: OPEN.
- WP19: BLOCKED / UNAUTHORIZED.

## 9. Next bounded step

Evaluate and close Q2-EX before or together with a BR3 selection. Then prepare the separate final Q2 persisted-representation decision with the residual WP19 implementation-boundary clause above.

Do not treat final Q2 selection as a substitute for a WP19 scope amendment or actor-attribution authority.
