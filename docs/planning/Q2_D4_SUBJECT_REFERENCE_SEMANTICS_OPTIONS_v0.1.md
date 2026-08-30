# WP19 / Q2 D4 Durable Subject-Reference Semantics Options v0.1

> **Post-decision synchronization — 2026-08-30:** D4 is now **CLOSED — ACCEPTED** by Project Owner. Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D4_SUBJECT_REFERENCE_SEMANTICS_DECISION.md`. This document is retained as the historical D4 options/evaluation artifact and has no implementation effect.

**Status:** Historical options/evaluation — D4 subsequently CLOSED / ACCEPTED  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 / D4 — semantic contract of durable AuditRecord subject reference  
**Decision owner:** Project Owner through ADW-07  
**Authority:** Historical analysis only. Normative D4 authority is `00_ARCHITECTURE/07_AUDIT/ADW07_D4_SUBJECT_REFERENCE_SEMANTICS_DECISION.md`.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit authorization of an interim shape.

## 1. Historical D4 bounded question

D4 evaluated the semantic contract a durable persisted AuditRecord subject reference must satisfy beyond D1–D3 so that subject identity remains unambiguous, historically meaningful, and distinguishable from context, association, and actor attribution over time.

D4 was a semantic/options decision stage, not a persistence-design stage.

## 2. Accepted D4 authority summary

The canonical authority establishes that AuditRecord subject identity is mandatory, durable, explicit, stable, and independently resolvable. It identifies the audited subject — what was changed/audited — rather than the actor, initiator, execution/request/Workspace context, association participant, route, diff, or audit payload.

The accepted semantic properties are:

1. one canonical logical historical subject identity;
2. explicit subject kind/type under D1;
3. stable subject identifier semantics across lifecycle changes;
4. verifiable historical resolvability without requiring current live dereference;
5. historical stability consistent with D3;
6. no implicit fallback through actor attribution, ActorContext, Workspace/request/runtime context, association participants, route, diff, or payload.

The rule applies across all five current D1 subject types: `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, and `Task`.

This summary is non-canonical; where wording differs, the D4 authority artifact controls.

## 3. Actor-attribution / ActorContext boundary

D4 deliberately keeps audited-subject identity and actor attribution as separate semantic axes.

Actor attribution answers who or what performed, initiated, authorized, or was attributed to the action. It does not establish audited-subject identity by implication.

D4 does **not** define or close the actor-attribution persistence contract, ActorContext identity model, attribution fields, or attribution mechanism. Those remain separate unresolved architecture surfaces.

## 4. Persistence representation remains open

D4 does not select, prefer, default, reject, or approve any N1–N5 candidate:

- N1 polymorphic reference;
- N2 composite-FK-derived representation;
- N3 per-type nullable representation;
- N4 opaque identifier;
- N5 in-payload representation.

D4 does not select columns, field names, FK/composite-FK structure, payload layout, registry, resolver implementation, database/application enforcement, migration, model, repository, service, API, backend, or tests.

GC-002 Alternative B remains **PROPOSED ONLY**. Its concreteness does not make it a default or confer normative authority.

## 5. D1–D3 and D5 boundaries

- D1: **CLOSED — ACCEPTED**; D4 does not redefine type disambiguation.
- D2: **CLOSED — ACCEPTED**; D4 does not collapse subject into Workspace context.
- D3: **CLOSED — ACCEPTED**; D4 does not replace lifecycle/history, deletion, retention, legal/compliance, cascade, or preservation-mechanism boundaries.
- D4: **CLOSED — ACCEPTED**; canonical authority is the D4 decision artifact.
- D5: **OPEN**; D4 does not decide future subject-type extensibility.

## 6. Dependency and implementation guardrails

The WP19 blocker remains the unresolved Q2 persisted AuditRecord subject-reference representation, unless Project Owner separately issues explicit bounded interim-shape authorization.

No WP18 → WP19 dependency is restored by D4 acceptance or by this planning synchronization.

D4 does not authorize WP19 models, migrations, repositories, services, APIs, backend changes, or tests.

## 7. Historical option outcomes

The D4 analysis rejected semantics that require permanent live resolution, allow context/association/actor substitution, or invent a sixth `Unknown`/`Legacy` subject type under current D1 authority.

It supported stable type-qualified historical identity and the principle that historical identity may remain valid when current live resolution is unavailable. Legacy evidence may be preserved without inventing canonical identity; migration/repair remains separate.

These historical option outcomes do not constitute persistence-candidate selection.

## 8. Current state

- D1: **CLOSED — ACCEPTED**;
- D2: **CLOSED — ACCEPTED**;
- D3: **CLOSED — ACCEPTED**;
- D4: **CLOSED — ACCEPTED**;
- D5: **OPEN**;
- Q2 persisted representation: **OPEN / NOT ESTABLISHED**;
- N1–N5: **UNAPPROVED CANDIDATES**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- actor attribution / ActorContext persistence semantics: **SEPARATE / UNRESOLVED**;
- WP18 dependency: **NOT RESTORED**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit interim-shape authorization**.

The next bounded architecture stage is D5. This historical D4 artifact creates no implementation authorization and no persistence-representation default.