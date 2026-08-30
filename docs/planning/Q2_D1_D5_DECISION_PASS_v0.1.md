# WP19 / Q2 D1–D5 Decision Pass v0.1

> **Post-decision synchronization — 2026-08-30:** D1, D2, and D3 are now **CLOSED — ACCEPTED** by Project Owner. Canonical authorities: `00_ARCHITECTURE/07_AUDIT/ADW07_D1_SUBJECT_TYPE_DISAMBIGUATION_DECISION.md`, `00_ARCHITECTURE/07_AUDIT/ADW07_D2_WORKSPACE_SUBJECT_SEMANTICS_DECISION.md`, and `00_ARCHITECTURE/07_AUDIT/ADW07_D3_SUBJECT_DELETION_DECISION.md`. D4 and D5 remain **OPEN**.
>
> **D4 scope clarification — 2026-08-30:** Project Owner has explicitly narrowed/reframed the active D4 decision stage as a separate semantic/options question about the durable AuditRecord subject-reference contract. The earlier planning formulation of D4 as “DB-enforced referential integrity” is retained below only as historical scaffolding and is **not** the active D4 definition. Referential-integrity mechanism remains unresolved and must not be inferred as a D4 answer, persistence-shape choice, or approval of GC-002 Alternative B.

**Status:** Historical decision-structuring analysis — D1/D2/D3 subsequently ACCEPTED; D4/D5 remain OPEN
**Date:** 2026-08-30
**Subject:** ADR-0014 Q2 — explicit D1–D5 decision pass after A1–A6, S1–S10, and C1–C5
**Decision owner:** Project Owner through ADW-07
**Authority:** Historical analysis only. D1–D3 authority is recorded separately. Active D4 scope is governed by the Project Owner clarification recorded above and by the dedicated D4 options artifact; this file does not itself decide D4/D5 or select a persisted representation.
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending explicit Q2 persisted-representation resolution or separate explicit authorization of an interim shape.

## 1. Scope and boundary

The approved ADW-07 Block 4 / D6 procedure completed A1–A6 authoritative-constraint application, S1–S10 semantic stress tests, and C1–C5 qualitative comparison.

This artifact historically structured D1–D5. It does not:

- select a Q2 persisted representation;
- turn qualitative comparison strength into a default candidate;
- treat stress-test support/failure as candidate approval/rejection;
- decide D4 or D5 by implication;
- create implementation authorization;
- modify WP19 backlog or implementation sequence;
- restore a WP18 → WP19 dependency;
- resolve GC-006 or GC-007;
- close ADW-07.

## 2. Blocker provenance

WP19 remains **BLOCKED / UNAUTHORIZED pending Q2 persisted AuditRecord subject-reference representation resolution**, unless Project Owner separately issues explicit authorization for a bounded interim shape.

This is the direct ADR-0014 Q2 blocker, not a restored WP18 dependency. Acceptance of D1–D3 does not make WP19 buildable.

## 3. Candidate and authority guardrails

- N1–N5 remain options/candidates until separate explicit decision authority acts.
- No candidate becomes default because it is more concretely documented.
- GC-002 Alternative B remains **PROPOSED ONLY**.
- D4 must not approve a persistence shape, FK strategy, composite-FK strategy, or enforcement layer by implication.

## 4. D1 — Type disambiguation

**CLOSED — ACCEPTED.** Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D1_SUBJECT_TYPE_DISAMBIGUATION_DECISION.md`.

D1 requires an explicit durable subject-type discriminator identifying exactly one current Q2 subject type and does not decide physical placement or persistence mechanism.

## 5. D2 — `Workspace` subject semantics

**CLOSED — ACCEPTED.** Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D2_WORKSPACE_SUBJECT_SEMANTICS_DECISION.md`.

D2 makes `Workspace` a first-class audited subject and keeps another subject's workspace context distinct from subject identity.

## 6. D3 — Subject lifecycle / historical resolution

**CLOSED — ACCEPTED.** Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D3_SUBJECT_DELETION_DECISION.md`.

D3 requires committed historical audited-subject identity to survive later subject deletion/deactivation and context lifecycle changes. It does not authorize deletion/mutation of committed AuditRecords, select referential-integrity behavior, choose retention/legal/compliance policy, or choose persistence shape.

## 7. D4 — Active scope: durable subject-reference semantics

### Active bounded question

D4 must clarify the semantic contract of a durable AuditRecord subject reference without selecting persistence shape and without replacing D1–D3.

The active D4 surfaces include:

- what constitutes the subject identity carried by the reference beyond the already-accepted D1 type discriminator;
- which identity forms are semantically admissible at the contract level;
- how subject identity remains distinct from context and association;
- what temporal resolvability the durable reference must provide;
- how unknown, legacy, unavailable, deleted, or inactive subjects are treated semantically;
- how D4 relates to, but does not replace, D3 historical-resolution and retention/deletion boundaries.

### Explicit D4 non-decisions

D4 does not decide:

- models, migrations, repositories, services, APIs, backend implementation, or tests;
- N1–N5 selection/default;
- FK/composite-FK/payload/opaque/registry/other persistence shape;
- database versus application/domain referential-integrity enforcement;
- GC-002 Alternative B approval;
- retention periods or legal/compliance policy;
- D5.

### Historical planning note

The earlier planning formulation asked whether DB-enforced referential integrity was required/preferred/optional/inappropriate. That question remains a legitimate unresolved persistence/integrity surface, but **it is not the active definition of D4 after the Project Owner scope clarification of 2026-08-30**. It must not be silently answered inside D4 semantic analysis.

### Status

**OPEN — PROJECT OWNER DECISION REQUIRED.**

## 8. D5 — Subject-type set / extensibility requirement

### Decision question

**For Q2, is the architecture requirement limited to the current five subject types, or must the persisted representation also satisfy an explicit extensibility requirement for future auditable subject types?**

### Status

**OPEN — PROJECT OWNER DECISION REQUIRED.**

D5 must state any extensibility requirement at architecture level without selecting an implementation mechanism by implication.

## 9. Decision interaction map

| Decision | Current state | Does answering it select a candidate by itself? |
|---|---|---|
| D1 Type disambiguation | CLOSED — ACCEPTED | No |
| D2 Workspace subject semantics | CLOSED — ACCEPTED | No |
| D3 Subject lifecycle / historical resolution | CLOSED — ACCEPTED | No |
| D4 Durable subject-reference semantics | OPEN | No |
| D5 Subject-type set / extensibility | OPEN | No |

## 10. Current gate result

**D1/D2/D3 CLOSED — ACCEPTED; D4/D5 OPEN; NO CANDIDATE DEFAULT, RECOMMENDATION, REJECTION, OR SELECTION CREATED.**

Current state:

- Q2 persisted representation: **OPEN**;
- D1: **CLOSED — ACCEPTED**;
- D2: **CLOSED — ACCEPTED**;
- D3: **CLOSED — ACCEPTED**;
- D4–D5: **OPEN — PROJECT OWNER DECISIONS REQUIRED**;
- N1–N5: **UNAPPROVED CANDIDATES**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- WP19: **BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit interim-shape authorization**;
- WP18 dependency: **NOT RESTORED**;
- ADW-07: **OPEN**.

The next bounded stage is D4 semantic/options analysis. It must not become an implementation pass or a persistence-shape decision.