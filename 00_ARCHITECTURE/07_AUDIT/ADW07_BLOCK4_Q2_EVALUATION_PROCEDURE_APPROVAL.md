# ADW-07 Block 4 — Q2 Evaluation Procedure Approval

**Workshop:** ADW-07 — Events, Audit, and Provenance
**Workshop Status:** OPEN
**Block:** Block 4 — AuditRecord Q2 Evaluation Procedure Approval
**Block Status:** APPROVED
**Owner:** Project Owner
**Decision authority:** Project Owner
**Decider:** Andrew (Project Owner)
**Decision Date:** 2026-08-28
**Remaining ADW-07 work:** OPEN / NOT YET DECIDED
**Builds on:** ADR-0014 (AuditRecord must durably identify its audited subject), ADW-07 Block 3 (Q2 routing decision), and `docs/planning/Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md` after the approved minor precision corrections.

**Recording note:** this Block records D6 only: approval of the procedure ADW-07 will use to evaluate Q2 candidate representations. It does not decide Q2's persisted representation and does not authorize WP19 implementation.

---

## Scope

This Block decides only whether the Q2 evaluation procedure described in `docs/planning/Q2_EVALUATION_FRAMEWORK_CANDIDATE_v0.1.md`, after the three minor precision corrections approved by the Project Owner, is approved for normative use within ADW-07.

The approved corrections are limited to:

1. **A2 precision:** distinguish D10's direct immutability authority from the derived consequence that correction should be represented by a new historical record rather than mutation of the committed AuditRecord.
2. **A4 precision:** distinguish the open Domain Event ↔ AuditRecord relationship from Block 2 R1, which concerns Domain Event ↔ Durable Audit / Outbox / Publication-Intent identity.
3. **S9 precision:** apply R1 as a stress surface only where a candidate depends on the Domain Event ↔ Durable Audit / Outbox / Publication-Intent identity question; do not use R1 as another name for the Event ↔ AuditRecord relationship.

These corrections do not alter A1–A6, add or remove a criterion, add or remove a stress test, select a persistence representation, alter the procedure order, close D1–D5, or make WP19 buildable.

## Decision

The Q2 evaluation procedure is **APPROVED FOR NORMATIVE USE** within ADW-07 after the three minor precision corrections listed above.

The approved procedure is:

```text
AUTHORITATIVE CONSTRAINTS
        ↓
CHECK EACH CANDIDATE AGAINST THOSE CONSTRAINTS
  PASS / FAIL / UNDETERMINED — DECISION REQUIRED
        ↓
SEMANTIC STRESS TESTS
        ↓
COMPARATIVE EVALUATION
        ↓
EXPOSED DECISION GAPS
        ↓
PROJECT OWNER DECISIONS WHERE NECESSARY
        ↓
Q2 REPRESENTATION DECISION
        ↓
SEPARATE WP19 READINESS RE-EVALUATION
```

The framework's representation-neutrality rule and decision-sufficiency test are part of the approved procedure. Comparative criteria remain subordinate to authoritative constraints and cannot override them.

## Consequences

- **Q2 evaluation procedure:** APPROVED for normative use.
- **Q2 persisted representation:** OPEN — NOT DECIDED by this Block.
- **D1–D5:** OPEN — NOT DECIDED by this Block.
- **WP19 implementation:** BLOCKED. No model, migration, repository, service, or API work is authorized by this Block.
- **GC-002 Alternative B:** remains Proposed candidate only; no presumptive approval is created.
- **ADW-07 routing:** already discharged by Block 3; unchanged.
- **ADW-07 substantive Q2 ownership:** remains established by Block 3.
- **ADW-08:** receives no new ownership of AuditRecord persistence from this Block.
- **GC-006 / GC-007:** unchanged and unresolved at their existing status.
- **Event/AuditRecord relationship:** remains open.
- **Block 2 R1:** remains open and distinct from the Event/AuditRecord relationship.
- **WP18:** unchanged; this Block authorizes no WP18 implementation.

Approval of the evaluation procedure is not approval of any representation that may later be evaluated under it. A separate explicit Q2 representation decision is required before WP19 model/migration implementation can be reconsidered.

## Non-Goals

This Block does not:

- enumerate, rank, recommend, approve, or reject Q2 representation candidates;
- approve GC-002 Alternative B or any interim representation by default;
- create or modify a WP19 model, migration, repository, service, or API;
- decide D1–D5;
- resolve GC-006 or GC-007;
- resolve ActorContext or merge Q1 with actor attribution;
- assign AuditRecord persistence ownership to ADW-08;
- modify ADR-0013;
- modify `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md`;
- modify `50_IMPLEMENTATION/IMPLEMENTATION_SEQUENCE.md`;
- authorize WP18 implementation;
- close ADW-07 as a whole.

The stale WP14 wording in `IMPLEMENTATION_SEQUENCE.md` remains a separate planning-housekeeping issue and is intentionally outside this decision.

## Approval Record

```text
Decision: Approved — ADW-07 Block 4 / D6.
The corrected Q2 evaluation framework is approved for normative use as
ADW-07's required procedure for evaluating Q2 representation candidates.

Decider: Andrew (Project Owner)
Decision Date: 2026-08-28

Q2 representation: OPEN.
D1–D5: OPEN.
WP19 implementation: BLOCKED / UNAUTHORIZED.
GC-002 Alternative B: PROPOSED CANDIDATE ONLY.
ADW-07: OPEN.

This approval establishes a decision method only. It selects no
persistence shape and creates no implementation authorization.
```
