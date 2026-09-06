# ADW-07 / Q2 — Persisted Subject-Reference Representation Decision

**Identifier:** Q2
**Workshop:** ADW-07 — Events, Audit, and Provenance
**Workshop Status:** OPEN
**Decision:** ADR-0014 Q2 — AuditRecord persisted subject-reference representation
**Decision Status:** ACCEPTED
**Decision Owner / Authority / Decider:** Project Owner / Andrew
**Decision Date:** 2026-09-05
**Selected representation:** BR3/N3, with accepted Q2-EX-O1
**Builds on:** ADR-0014 (AuditRecord must durably identify its audited subject), ADW-07 Block 3 (Q2 routing decision), accepted D1, D1-CLAR-01, D2, D3, D4, D5, Q2-RI, Q2-ST, Q2-EX, and `docs/planning/Q2_FINAL_BOUNDED_REPRESENTATION_COMPARISON_v0.1.md` — all unmodified by this document.

---

## 1. Scope

This record decides the ADR-0014 Q2 persisted subject-reference representation: which of the conforming bounded arms — BR1/N1, BR3/N3 with accepted Q2-EX-O1, BR4/N4, BR5/N5 — is selected, and what that selection commits to at the persisted-contract level.

It does not decide, and is not read as deciding, any of the matters listed in §9 below, including the WP19 scope amendment, actor attribution, GC-006, GC-007, the Event/AuditRecord relationship, Block 2 Residual Question R1, or any implementation detail.

## 2. Decision

**The ADR-0014 Q2 persisted subject-reference representation is BR3/N3, with accepted Q2-EX-O1.**

1. AuditRecord persists five authorized typed subject-reference paths, one for each current D1 subject kind: `Workspace`, `EnterpriseObject`, `User`, `WorkspaceMembership`, `Task`.
2. Exactly one authorized subject-reference path is populated for every committed AuditRecord.
3. That exactly-one property is enforced at the database persistence boundary, per accepted Q2-EX-O1.
4. Subject kind is determined structurally by which path is populated. No separate persisted scalar `subject_type` or kind token is part of the selected representation.
5. Committed AuditRecords are not reinterpreted or rewritten when the authorized subject-kind set later evolves. Adding a future subject kind requires separate D5 / Q2-ST authority and corresponding representation evolution; it does not retroactively alter any already-committed record's subject-kind determination.

This restates accepted Q2-EX-O1's own terms as the selected persisted shape; it does not amend, supersede, or reinterpret Q2-EX, whose canonical text remains exclusively `00_ARCHITECTURE/07_AUDIT/ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`.

## 3. Canonical audited-subject identity

For each of the five current subject kinds, the table targeted by that kind's authorized reference path is that kind's canonical audited-subject identity for purposes of the AuditRecord subject-reference contract:

- `Workspace` → the `workspaces` table's own primary key.
- `EnterpriseObject` → the `enterprise_objects` table's own primary key.
- `User` → the `users` table's own primary key.
- `WorkspaceMembership` → the `workspace_memberships` table's own primary key.
- `Task` → the `tasks` table's own primary key.

This grounding is consistent with the current-implementation-evidence description of these five tables' primary-key shape already on record (`docs/planning/Q2_BOUNDED_CONCRETE_REALIZATIONS_v0.1.md` §2 — IMPLEMENTATION EVIDENCE, NOT ARCHITECTURE AUTHORITY in itself; what elevates the identified primary key to canonical status for the AuditRecord subject-reference contract is this decision, not the implementation evidence alone). This declaration satisfies D1-CLAR-01's determinacy property for each kind and is the "final Q2 persisted-representation contract establishing that canonical identity" that accepted Q2-ST's own text names as its own precondition (see §5 below).

## 4. Consequence for Q2-EX

This decision selects BR3/N3 as the ADR-0014 Q2 persisted subject-reference representation. Per Q2-EX's own Conditionality section — "This decision therefore takes effect only if the separate Q2 persisted-representation decision selects BR3/N3" — that condition is met: accepted Q2-EX is operative, not conditional. Q2-EX's own text is unamended, unsuperseded, and unedited by this statement; its canonical authority remains exclusively `00_ARCHITECTURE/07_AUDIT/ADW07_Q2_EX_SUBJECT_KIND_EXCLUSIVITY_DECISION.md`.

## 5. Consequence for Q2-ST

§3 above establishes `enterprise_objects.id` as the canonical audited-subject identity for the existing `EnterpriseObject` subject kind. Accepted Q2-ST's permission —

> "It may use the existing subject kind only where the accepted AuditRecord contract identifies that shared/base identity as the canonical audited-subject identity. This permission is inoperative until the final Q2 persisted-representation contract establishing that canonical identity has been accepted." (`00_ARCHITECTURE/07_AUDIT/ADW07_Q2_ST_SUBJECT_TYPE_RANGING_RULE_DECISION.md`)

— has its stated precondition satisfied by §3's canonical-identity declaration only where separate accepted authority establishes that a persisted subject shares that canonical `EnterpriseObject` identity. This decision does not itself make any such determination for any specific persisted form. In particular, this decision:

- does not classify a standalone D02 specialization (ADR-0015 Option B, no corresponding `enterprise_objects` row) as an `EnterpriseObject` subject;
- does not create an `enterprise_objects` base row for any standalone specialization;
- does not alter ADR-0015's standalone-persistence default or any of its consequences.

Q2-ST's own text is unamended, unsuperseded, and unedited by this statement; its canonical authority remains exclusively `00_ARCHITECTURE/07_AUDIT/ADW07_Q2_ST_SUBJECT_TYPE_RANGING_RULE_DECISION.md`.

## 6. Consequence for ADR-0014 and the Block 3 routing path

This decision fulfils the Q2 resolution path routed to ADW-07 by Block 3, under branch (a) of ADR-0014's routing obligation (`00_ARCHITECTURE/07_AUDIT/EVENTS_AUDIT_AND_PROVENANCE.md`, Block 3). Block 3's own routing choice — accepting substantive Q2 ownership under branch (a) rather than branch (b) — is unaffected and is not reopened here.

**This decision closes the ADR-0014 Q2 persisted subject-reference representation blocker identified for WP19.**

This does not mean WP19 model/migration work as a whole is unblocked or authorized — see §10. ADR-0014 itself is not edited: its Status remains `Accepted`, its Q1 decision (that an AuditRecord must durably identify the subject of the audited mutation) is unaffected, and this record supplies the persisted shape that Q1 left open as Q2, without altering ADR-0014's own text.

## 7. Disposition of the arms not selected

BR1/N1, BR4/N4, and BR5/N5 all conformed to A1–A6 under the merged comparison, and no stress test was left unresolved for any of them (`docs/planning/Q2_FINAL_BOUNDED_REPRESENTATION_COMPARISON_v0.1.md` §§6, 8). They are not selected, and this decision does not find them deficient, does not reject them, and does not amend that comparison's own account of them. Their comparative standing is recorded there and is not reproduced here.

BR2/N2 remains excluded in its existing bounded form on the grounds already recorded (`docs/planning/Q2_POST_Q2_ST_BOUNDED_REAPPLICATION_v0.1.md` §4, §8 item 2; comparison §1.2) and is not revisited by this decision.

## 8. FK delete behavior — deliberately unresolved

No FK delete behavior is selected by this decision. Any later proposed FK action must independently demonstrate conformance with D3, D10, committed AuditRecord immutability, durable historical subject identity, and the Q2-EX-O1 exactly-one persisted-reference contract. This decision neither chooses nor pre-approves any concrete FK delete action.

D3 (`00_ARCHITECTURE/07_AUDIT/ADW07_D3_SUBJECT_DELETION_DECISION.md`) leaves the choice among `RESTRICT`, `CASCADE`, `SET NULL`, or any other FK action open deliberately, as a decision for later work; this record does not narrow that choice and does not name who decides it.

## 9. Explicit non-decisions

This decision does not:

1. decide exact column names;
2. decide SQL or check-constraint syntax for the exactly-one guarantee;
3. decide index definitions;
4. decide migration implementation mechanics;
5. decide FK delete behavior for any of the five target relations (§8 above);
6. authorize Q2-EX-O5 (a derived kind-as-value column), which remains deferred, its own reopen condition (a demonstrated query or operational need) unchanged;
7. decide ActorContext or actor-attribution persistence semantics;
8. resolve GC-006;
9. resolve GC-007;
10. resolve the Event/AuditRecord relationship;
11. resolve Block 2 Residual Question R1;
12. decide WP19's implementation scope, or perform the separate WP19 scope amendment;
13. decide repository, service, or API design;
14. authorize any implementation of any kind;
15. introduce any mechanism beyond the bounded realization already documented — no registry, resolver, identity abstraction, derived column, trigger, or payload machinery is created by this decision.

## 10. Implementation boundary

Per `docs/planning/Q2_FINAL_REPRESENTATION_DECISION_PRECONDITIONS_v0.1.md` §6, this decision:

- closes only the ADR-0014 Q2 persisted subject-reference representation blocker;
- does not by itself authorize the current full WP19 `model/repository/service` deliverable;
- does not establish ActorContext / actor-attribution semantics;
- does not waive the need for a separately Project Owner-approved WP19 scope amendment if the first implementation pass is narrower than the currently recorded WP19 deliverable;
- does not close ADW-07, which remains OPEN.

Per §4 of the same document, this decision does not perform the WP19 backlog amendment. `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md` and every other planning or implementation register are unedited by this decision.

## 11. Relationship to accepted authority

This decision does not amend, supersede, reinterpret, or edit D1, D1-CLAR-01, D2, D3, D4, D5, Q2-RI, Q2-ST, Q2-EX, ADR-0014, ADR-0015, or Block 3; their canonical authority remains exclusively in their own records. It applies them to select the persisted representation those records left open, and it records the consequences that follow from their own already-accepted terms (§§4–6 above).

## 12. Current state and effect

This decision is ACCEPTED as of 2026-09-05. The record stood in `PROPOSED` status, carrying no authority, between drafting and acceptance on that date.

- Q2 persisted representation: CLOSED — ACCEPTED — BR3/N3 with Q2-EX-O1.
- Q2-EX: operative (§4).
- Q2-ST's shared/base-identity permission: operative under the boundary stated in §5.
- ADR-0014's Q2 blocker for WP19: closed by §6, without editing ADR-0014.
- WP19: remains BLOCKED / UNAUTHORIZED pending the separate matters in §10.
- ADW-07: remains OPEN.

## 13. Next step

Nothing follows automatically from this acceptance. The WP19 scope amendment, if pursued, is a separate Project Owner decision (§10), and no implementation step — model, migration, repository, service, or API — is authorized by this record.
