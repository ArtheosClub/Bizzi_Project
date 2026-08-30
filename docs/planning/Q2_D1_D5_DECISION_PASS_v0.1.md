# WP19 / Q2 D1–D5 Decision Pass v0.1

> **Post-decision synchronization — 2026-08-30:** D1, D2, D3, and D4 are now **CLOSED — ACCEPTED** by Project Owner. Canonical authorities:
> - `00_ARCHITECTURE/07_AUDIT/ADW07_D1_SUBJECT_TYPE_DISAMBIGUATION_DECISION.md`
> - `00_ARCHITECTURE/07_AUDIT/ADW07_D2_WORKSPACE_SUBJECT_SEMANTICS_DECISION.md`
> - `00_ARCHITECTURE/07_AUDIT/ADW07_D3_SUBJECT_DELETION_DECISION.md`
> - `00_ARCHITECTURE/07_AUDIT/ADW07_D4_SUBJECT_REFERENCE_SEMANTICS_DECISION.md`
>
> D5 remains **OPEN**. Q2 persisted representation remains **OPEN / NOT ESTABLISHED**.

**Status:** Historical decision-structuring analysis — D1–D4 subsequently ACCEPTED; D5 remains OPEN  
**Date:** 2026-08-30  
**Subject:** ADR-0014 Q2 — D1–D5 decision pass  
**Decision owner:** Project Owner through ADW-07  
**Authority:** Historical planning only. D1–D4 authority is recorded in the canonical artifacts above. This file does not select a persisted representation or decide D5.  
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending explicit Q2 persisted-representation resolution or separate explicit authorization of an interim shape.

## 1. Scope and guardrails

This planning artifact records the current decision-pass state after the approved D6 evaluation procedure and explicit Project Owner decisions D1–D4.

It does not:

- select, prefer, default, reject, or approve N1–N5;
- turn qualitative comparison strength or implementation concreteness into architecture authority;
- approve GC-002 Alternative B;
- choose FK/composite-FK/payload/opaque/registry or another persistence shape;
- decide database/application referential-integrity enforcement;
- define or close actor attribution or ActorContext persistence semantics;
- restore a WP18 → WP19 dependency;
- authorize WP19 implementation;
- modify WP19 backlog or implementation sequence;
- resolve GC-006 or GC-007;
- close ADW-07.

## 2. Blocker provenance

WP19 remains **BLOCKED / UNAUTHORIZED pending Q2 persisted AuditRecord subject-reference representation resolution**, unless Project Owner separately issues explicit authorization for a bounded interim shape.

This is the direct ADR-0014 Q2 blocker. It is **not** a restored WP18 dependency. D1–D4 acceptance does not by itself make WP19 buildable.

## 3. Candidate guardrails

N1–N5 remain **UNAPPROVED CANDIDATES**. D4 semantic authority does not imply that any candidate is more approved than another.

GC-002 Alternative B remains **PROPOSED ONLY**. Its existing concrete description does not make it the default and does not confer normative authority.

Persistence representation remains **OPEN / NOT ESTABLISHED**.

## 4. D1 — Type disambiguation

**CLOSED — ACCEPTED.** Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D1_SUBJECT_TYPE_DISAMBIGUATION_DECISION.md`.

D1 requires explicit durable subject-type disambiguation and does not decide physical placement or persistence mechanism.

## 5. D2 — Workspace subject semantics

**CLOSED — ACCEPTED.** Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D2_WORKSPACE_SUBJECT_SEMANTICS_DECISION.md`.

D2 makes `Workspace` a first-class audited subject and keeps Workspace context associated with another subject distinct from subject identity.

## 6. D3 — Subject lifecycle / historical resolution

**CLOSED — ACCEPTED.** Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D3_SUBJECT_DELETION_DECISION.md`.

D3 requires committed historical audited-subject identity to survive later subject deletion/deactivation and context lifecycle changes. It does not authorize deletion/mutation of committed AuditRecords, select retention/legal/compliance policy, choose referential-integrity behavior, or choose persistence shape.

## 7. D4 — Durable subject-reference semantics

**CLOSED — ACCEPTED.** Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D4_SUBJECT_REFERENCE_SEMANTICS_DECISION.md`.

D4 establishes that AuditRecord subject identity is mandatory, durable, explicit, stable, and independently resolvable. It identifies what was audited and remains distinct from actor attribution, ActorContext, request/runtime/Workspace context, association participants, route, diff, and payload.

D4 does **not** select N1–N5, choose persistence representation, approve GC-002 Alternative B, choose referential-integrity enforcement, or authorize implementation.

Actor attribution and ActorContext persistence/identity semantics remain **separate unresolved architecture surfaces**; D4 only establishes that they cannot substitute for audited-subject identity or establish it by implication.

## 8. D5 — Subject-type set / extensibility requirement

### Decision question

**For Q2, is the architecture requirement limited to the current five subject types, or must the persisted representation also satisfy an explicit extensibility requirement for future auditable subject types?**

### Status

**OPEN — PROJECT OWNER DECISION REQUIRED.**

D5 must state any extensibility requirement at architecture level without selecting an implementation mechanism by implication.

## 9. Decision interaction map

| Decision | Current state | Selects a persistence candidate by itself? |
|---|---|---|
| D1 Type disambiguation | CLOSED — ACCEPTED | No |
| D2 Workspace subject semantics | CLOSED — ACCEPTED | No |
| D3 Subject lifecycle / historical resolution | CLOSED — ACCEPTED | No |
| D4 Durable subject-reference semantics | CLOSED — ACCEPTED | No |
| D5 Subject-type set / extensibility | OPEN | No |

## 10. Current gate result

**D1–D4 CLOSED — ACCEPTED; D5 OPEN; Q2 PERSISTED REPRESENTATION OPEN / NOT ESTABLISHED; NO N1–N5 DEFAULT OR SELECTION; GC-002 ALTERNATIVE B PROPOSED ONLY; ACTOR ATTRIBUTION / ACTORCONTEXT REMAIN SEPARATE UNRESOLVED SURFACES; WP18 DEPENDENCY NOT RESTORED.**

Current state:

- D1–D4: **CLOSED — ACCEPTED**;
- D5: **OPEN**;
- Q2 persisted representation: **OPEN / NOT ESTABLISHED**;
- N1–N5: **UNAPPROVED CANDIDATES**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- actor attribution / ActorContext persistence semantics: **SEPARATE / UNRESOLVED**;
- WP18 dependency: **NOT RESTORED**;
- ADW-07: **OPEN**;
- WP19: **BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit interim-shape authorization**.

The next bounded decision stage is D5. Nothing in this planning synchronization authorizes models, migrations, repositories, services, APIs, backend changes, or tests.