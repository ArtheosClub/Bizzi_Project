# WP19 / Q2 D5 Subject-Type Set / Extensibility Options v0.1

> **Post-decision synchronization — 2026-08-30:** D5 is now **CLOSED — ACCEPTED** by Project Owner. Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D5_SUBJECT_TYPE_EXTENSIBILITY_DECISION.md`. This document is retained as the historical D5 options/evaluation artifact and has no implementation effect.

**Status:** Historical options/evaluation — D5 subsequently CLOSED / ACCEPTED  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 / D5 — current subject-type set and future extensibility requirement  
**Decision owner:** Project Owner through ADW-07  
**Authority:** Historical analysis only. Normative D5 authority is `00_ARCHITECTURE/07_AUDIT/ADW07_D5_SUBJECT_TYPE_EXTENSIBILITY_DECISION.md`.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit authorization of an interim shape.

## 1. Historical D5 bounded question

D5 evaluated whether Q2 acceptance is limited to the five current audited-subject types or must additionally require open-ended future subject-type extensibility without later representation evolution.

D5 was an extensibility-requirement decision, not a persistence-shape decision.

## 2. Accepted D5 authority summary

The current Q2 acceptance scope consists of exactly five current D1 subject types:

- `Workspace`;
- `EnterpriseObject`;
- `User`;
- `WorkspaceMembership`;
- `Task`.

The selected Q2 persistence representation must satisfy D1–D4 for all five current types.

These five types are sufficient for current Q2 acceptance but are not declared a permanently closed audited-subject universe. Any future auditable subject type requires separate explicit architecture authority and must preserve the then-applicable D1–D4 invariants.

D5 does not require arbitrary future subject types to be addable without migration, configuration, schema change, or representation evolution.

This summary is non-canonical; where wording differs, the D5 authority artifact controls.

## 3. Accepted extensibility guardrails

D5 authority additionally establishes:

1. **Extensibility convenience MUST NOT by itself determine, rank, or default the Q2 persistence representation.**
2. **Technical encodability does not confer architecture authority.** A persistence mechanism's ability to encode another discriminator or identifier does not make that future subject type valid without separate explicit architecture authority.

Therefore:

- N2/N3 are not disfavored merely because future types may require schema evolution;
- N1/N4/N5 are not favored merely because they may appear more open-ended;
- C3 remains a comparative/evolution concern rather than an independent selection rule;
- GC-002 Alternative B remains **PROPOSED ONLY**.

## 4. D1–D5 state

- D1: **CLOSED — ACCEPTED**;
- D2: **CLOSED — ACCEPTED**;
- D3: **CLOSED — ACCEPTED**;
- D4: **CLOSED — ACCEPTED**;
- D5: **CLOSED — ACCEPTED**.

D5 does not redefine D1–D4.

## 5. Actor-attribution / ActorContext boundary

D5 concerns only audited-subject type scope and extensibility.

Actor attribution, ActorContext identity/persistence semantics, actor categories, service principals, initiator identity, and actor extensibility remain **separate unresolved architecture surfaces**. They are not included in the D5 subject-type set.

## 6. Persistence representation remains open

D5 does not select, prefer, rank, reject, approve, or default any N1–N5 candidate.

**Q2 persisted representation remains OPEN / NOT ESTABLISHED.**

D5 does not choose FK/composite-FK/payload/opaque/registry shape, fields/columns, enforcement layer, resolver implementation, migration design, models, repositories, services, APIs, backend changes, or tests.

## 7. Dependency and implementation guardrails

D5 acceptance does not restore a WP18 → WP19 dependency.

WP19 remains **BLOCKED / UNAUTHORIZED pending explicit Q2 persisted-representation resolution**, unless Project Owner separately issues explicit bounded interim-shape authorization.

No implementation authorization is created by D5 or this planning synchronization.

## 8. Historical option outcomes

The historical analysis rejected:

- permanently closing architecture to the five current types;
- requiring zero-migration/zero-redesign support for arbitrary future types now;
- allowing implementation to introduce new subject kinds implicitly;
- reusing an existing discriminator value for a different future subject type via context interpretation.

It preferred the now-accepted rule: current five types are sufficient for Q2; future types require separate explicit architecture authority; later representation evolution is permissible when explicitly decided.

These option outcomes do not constitute persistence-candidate selection.

## 9. Current state

- D1–D5: **CLOSED — ACCEPTED**;
- Q2 persisted representation: **OPEN / NOT ESTABLISHED**;
- N1–N5: **UNAPPROVED CANDIDATES**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- actor attribution / ActorContext persistence semantics: **SEPARATE / UNRESOLVED**;
- WP18 dependency: **NOT RESTORED**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit interim-shape authorization**.

The next architecture stage is to re-apply accepted D1–D5 to N1–N5 and prepare a separate Q2 persisted-representation evaluation/recommendation. This historical D5 artifact creates no implementation authorization and no candidate default.