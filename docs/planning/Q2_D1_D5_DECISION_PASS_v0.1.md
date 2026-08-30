# WP19 / Q2 D1–D5 Decision Pass v0.1

> **Post-decision synchronization — 2026-08-30:** D1 and D2 are now **CLOSED — ACCEPTED** by Project Owner. Canonical authorities: `00_ARCHITECTURE/07_AUDIT/ADW07_D1_SUBJECT_TYPE_DISAMBIGUATION_DECISION.md` and `00_ARCHITECTURE/07_AUDIT/ADW07_D2_WORKSPACE_SUBJECT_SEMANTICS_DECISION.md`. This document is otherwise preserved as the historical decision-structuring snapshot. D3–D5 remain **OPEN — PROJECT OWNER DECISIONS REQUIRED**.

**Status:** Historical decision-structuring analysis — D1/D2 subsequently ACCEPTED; D3–D5 remain OPEN
**Date:** 2026-08-30
**Subject:** ADR-0014 Q2 — explicit D1–D5 decision pass after A1–A6, S1–S10, and C1–C5
**Decision owner:** Project Owner through ADW-07
**Authority:** Historical analysis only. D1/D2 authority is recorded separately; this artifact still structures D3–D5 for explicit decision authority and does not itself select, approve, reject, recommend, or default a persisted representation.
**Implementation effect:** None. WP19 remains BLOCKED / UNAUTHORIZED pending explicit Q2 persisted-representation resolution or separate explicit authorization of an interim shape.

## 1. Scope and boundary

The approved ADW-07 Block 4 / D6 procedure has completed the following analytical stages:

1. A1–A6 authoritative-constraint application;
2. S1–S10 semantic stress tests;
3. C1–C5 qualitative comparison.

This artifact structures D1–D5 as explicit decision questions for Project Owner decision authority.

It does not:

- select a Q2 persisted representation;
- turn qualitative comparison strength into a default candidate;
- treat stress-test support/failure as candidate approval/rejection;
- decide any still-open D3–D5 question by implication;
- create implementation authorization;
- modify WP19 backlog or implementation sequence;
- restore a WP18 → WP19 dependency;
- resolve GC-006 or GC-007;
- close ADW-07.

## 2. Blocker provenance

WP19 remains **BLOCKED / UNAUTHORIZED pending Q2 persisted AuditRecord subject-reference representation resolution**, unless Project Owner separately issues an explicit authorization for a bounded interim shape.

This blocker is the direct ADR-0014 Q2 blocker. It is **not** a restored dependency on WP18. Neither D1 nor D2 acceptance makes WP19 buildable by itself.

## 3. Inputs carried forward without reinterpretation

- A1–A6, S1–S10, and C1–C5 remain historical evaluation inputs.
- No N1–N5 candidate is approved by D1 or D2.
- GC-002 Alternative B remains Proposed only.
- Candidate rejection, preference, or selection still requires later explicit architecture decision authority.

## 4. D1 — Type disambiguation

### Decision question

**What durable information is required for a committed AuditRecord subject reference to distinguish the subject's type sufficiently for stable resolution?**

### Current state

**CLOSED — ACCEPTED.** Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D1_SUBJECT_TYPE_DISAMBIGUATION_DECISION.md`.

Accepted rule:

> A persisted AuditRecord subject reference MUST include an explicit durable subject-type discriminator as part of its durable reference contract. The discriminator’s committed value MUST identify exactly one of the current Q2 subject types: Workspace, EnterpriseObject, User, WorkspaceMembership, or Task. Type qualification within a durable subject identity satisfies this rule. D1 does not decide the physical placement or persistence mechanism of the discriminator.

D1 does not answer D2–D5 and does not select a persisted representation.

## 5. D2 — `Workspace` subject semantics

### Decision question

**What does `Workspace` mean when the accepted D1 subject-type discriminator of a durable persisted AuditRecord subject reference has the value `Workspace`?**

### Current state

**CLOSED — ACCEPTED.** Canonical authority: `00_ARCHITECTURE/07_AUDIT/ADW07_D2_WORKSPACE_SUBJECT_SEMANTICS_DECISION.md`.

Accepted rule:

> `Workspace` is a first-class subject type. When the discriminator is `Workspace`, the durable subject reference identifies the Workspace entity itself. A workspace associated with another subject is contextual metadata, not an implicit substitution for that subject.

D2 does not define workspace ownership/scoping rules for other subject types, multi-workspace/cross-workspace semantics, persistence shape, enforcement location, or any N1–N5 selection.

## 6. D3 — Subject deletion / historical resolution

### Decision question

**What must remain durably resolvable from a committed AuditRecord if its audited subject is later physically deleted, and may the AuditRecord subject reference itself constrain that deletion?**

The decision must separate two issues:

1. historical identity/resolution after subject deletion; and
2. whether the reference is permitted or required to prevent physical deletion.

### Why D3 is required

A2, S6, S7, and C5 expose a shared historical-stability requirement. None of N1–N5 currently establishes post-deletion behavior. A DB FK does not answer D3 by itself because delete actions and historical policy remain undecided.

D10 governs Historical Record immutability/permanence for AuditRecord itself; it does not by itself establish a universal deletion rule for every possible audited subject.

### What D3 must not decide by accident

D3 must not silently create:

- universal `RESTRICT`/`CASCADE`/`SET NULL` behavior;
- tombstones;
- permanent retention of every subject row;
- a historical identity registry;
- a preference for payload or FK representation.

### Status

**OPEN — PROJECT OWNER DECISION REQUIRED.**

## 7. D4 — DB-enforced referential integrity

### Decision question

**Is database-enforced referential integrity required, preferred, optional, or inappropriate for the AuditRecord subject-reference contract, and must that answer be uniform across all five current subject types?**

### Status

**OPEN — PROJECT OWNER DECISION REQUIRED.**

D4 must not silently approve GC-002 Alternative B, require one uniform FK shape, reject application/domain validation categorically, or select N2.

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
| D3 Subject deletion | OPEN | No |
| D4 DB referential integrity | OPEN | No |
| D5 Subject-type set | OPEN | No |

## 10. Decision-pass gate result

**D1/D2 CLOSED — ACCEPTED; D3–D5 OPEN; NO CANDIDATE DEFAULT, RECOMMENDATION, REJECTION, OR SELECTION CREATED.**

Current state:

- Q2 persisted representation: **OPEN**;
- D1: **CLOSED — ACCEPTED**;
- D2: **CLOSED — ACCEPTED**;
- D3–D5: **OPEN — PROJECT OWNER DECISIONS REQUIRED**;
- N1–N5: **UNAPPROVED CANDIDATES**;
- GC-002 Alternative B: **PROPOSED ONLY**;
- WP19: **BLOCKED / UNAUTHORIZED pending Q2 persisted-representation resolution or separate explicit interim-shape authorization**;
- WP18 dependency: **NOT RESTORED**;
- ADW-07: **OPEN**.

The next bounded decision stage is D3 options/evaluation. D3 must be decided separately before moving to D4, and none of D3–D5 may be treated as an implementation authorization.