# ADW-07 — Events, Audit, and Provenance

## Block 1: Event Semantics — Core Definition

**Document ID:** [not assigned — no numbering convention exists yet
for a non-ADW-01 chapter]
**Workshop:** ADW-07 — Events, Audit, and Provenance
**Workshop Status:** OPEN
**Block:** Block 1 — Event Semantics / Core Definition
**Block Status:** APPROVED
**Owner:** Project Owner
**Decision authority:** Project Owner
**Decider:** Andrew (Project Owner)
**Decision Date:** 2026-08-08
**Remaining ADW-07 work:** OPEN / NOT YET DECIDED
**Builds on:** D07 (State Semantics), D09 (Relationship Model), D10
(Deletion and Supersession) — all APPROVED — CLOSED, none modified by
this document.

**Recording note:** this is the first Project Owner-authorized
incremental recording of an OPEN architecture workshop in this
repository. No general cross-workshop recording rule is established by
this document; whether and how such a rule should be codified for
future workshops remains a separate governance question.

---

## Scope

This Block defines the minimum conceptual semantics of Domain Event:
what it is, its non-authoritative nature, its immutability, and its
Workspace scope. It does not define Event's fields, relationships to
other concepts, production-qualification rule, correction mechanism,
or persistence shape. Those remain open or deferred, as stated below.

## Decision

A Domain Event is an immutable, workspace-scoped record that a
significant committed fact has occurred. It records occurrence; it
does not itself hold or grant authority over authoritative state.

A Domain Event is scoped to exactly one Workspace.

Not every committed state mutation necessarily produces a Domain
Event.

## Existing Authority

- A Domain Event records a significant committed fact, and does not
  itself hold or grant authority over authoritative state.
  (LAW-D07-08; AP-12, `ARCHITECTURE_SPECIFICATION.md` §5)
- A Domain Event, once committed, is never mutated and is never
  physically deleted. (D10 §6, §7.4, §8 Invariant 7)
- A Domain Event does not authorize, request, or independently
  perform a state transition. (LAW-D07-08; AP-12)
- Publication failure after the underlying fact is committed does not
  erase authoritative business truth. (`ARCHITECTURE_SPECIFICATION.md`
  §10 Invariant 14; D07.5) This concerns authoritative business truth
  only; it does not establish whether the Domain Event record itself
  exists durably before publication (Open Question 2).

## New Decisions Approved by Project Owner

1. A Domain Event is scoped to exactly one Workspace.
   No approved source names Event specifically for workspace scope;
   this is a new decision, motivated by (not derived from) AP-03's
   isolation-by-default posture and `ARCHITECTURE_SPECIFICATION.md`
   §10 Invariant 1's default rule.
2. Not every committed state mutation necessarily produces a Domain
   Event.
   No approved source states this directly. It is motivated by (not
   derived from) LAW-D07-08's "significant" qualifier and, more
   loosely, by D07.1's carve-out for a different, adjacent artifact
   (the significant-transition record, not Domain Event itself).

## Rationale

D07 and D10 already establish core semantics of a committed Domain
Event, including its non-authoritative nature, immutability, and
non-deletion. Neither source states whether Workspace scope applies
to Event specifically, or whether every mutation must produce one.
Both gaps are real — an implementer following D07/D10 alone could not
derive either answer. Project Owner approval closes both gaps as
explicit new decisions, without claiming either was already
established.

## Invariants

1. A Domain Event, once committed, is never mutated and is never
   physically deleted. [EXISTING AUTHORITY]
2. A Domain Event does not authorize, request, or independently
   perform a state transition. [EXISTING AUTHORITY]
3. Publication failure after the underlying fact is committed does
   not erase authoritative business truth. [EXISTING AUTHORITY]
4. A Domain Event is scoped to exactly one Workspace. [NEW DECISION —
   PROJECT OWNER APPROVED]
5. Not every committed state mutation necessarily produces a Domain
   Event. [NEW DECISION — PROJECT OWNER APPROVED]

## Distinctions from Adjacent Concepts

These statements establish non-identity only. They do not establish
relationship, cardinality, ordering, derivation, or co-occurrence
semantics between the named concepts. Any such relationship remains
open and is deferred to later ADW-07 work.

- A Domain Event is not Event Delivery State. Event Delivery State is
  technical messaging infrastructure, owned by messaging
  infrastructure. (D07 §5, §7)
- A Domain Event is not an AuditRecord. (D10 §7.4 enumerates them as
  separate items.) How they relate is not established here.
- A Domain Event is not a significant-transition record. (D10 §7.4;
  D07 §11's reconstruction-precedence order ranks them separately.)
  How they relate is not established here.

## Open Questions

**Open Question 1 — Event qualification / significance rule.**
Which occurrences meet the significance bar for producing a Domain
Event is unresolved. Does not block Block 1 approval or the core
definition. Directly blocks authoritative Event-production semantics.
Does not by itself make a bare persistence schema logically
impossible, but materially affects informed persistence design —
expected Event cardinality/write volume is unknown, and no approved
source supplies a workload constraint (engineering consequence, not
architectural fact). Resolution: a later, not-yet-numbered ADW-07
block.

**Open Question 2 — Event persistence / publication boundary.**
Whether a committed Domain Event record exists durably before
downstream publication succeeds, or whether "Domain Event Publication"
is the act that materializes it, is not disambiguated by D07 §10's
sequence or any other approved source. Independent of Open Question 1
— affects WP18's persistence semantics separately. Resolution: a
later, not-yet-numbered ADW-07 block.

**Open Question 3 — Event correction / supersession mechanism.**
How an incorrect committed Domain Event is corrected, superseded, or
compensated for is unresolved. D10 establishes immutability and
non-deletion but gives Event no lifecycle-capability row from which
to inherit an entity-level mechanism. Resolution: a later, not-yet-
numbered ADW-07 block.

## Non-Goals / Deferred Questions

Deferred to later, not-yet-numbered ADW-07 work (distinct from the
three Open Questions above):

- AuditRecord's own domain definition; Event/AuditRecord relationship.
- Event's relationships to Enterprise Object, Actor, Work Item,
  Decision, Business Operation, Runtime Session.
- Correlation and causation representation.
- Provenance/source representation.
- Timestamp semantics (occurred/recorded/published/delivered).
- Publication/delivery mechanics.
- Sensitive-data handling.
- Schema/field shape.

Outside architecture's authority entirely, per D10 §9 — not an
ADW-07 subject:
- Retention duration.

## Impact on Work Packages

**WP18** remains BLOCKED under Amendment A-05. This Block does not
satisfy A-05's Definition of Done (ADW-07 completed and approved,
plus a subsequent WP18 schema-scope amendment) and authorizes no
model, migration, repository, service, or API work.

**WP19** is unaffected. Its current status and its use of GC-006/
GC-007 as non-blocking interim defaults are not reviewed or changed by
this Block.

## Source Notes / Traceability

- `D07_STATE_SEMANTICS.md`: LAW-D07-08, §5, §7, §10, §11, D07.1, D07.5.
- `D09_RELATIONSHIP_MODEL.md`: §1, Deferred Responsibilities.
- `D10_DELETION_AND_SUPERSESSION.md`: §6, §7.4, §8 Invariant 7.
- `ARCHITECTURE_SPECIFICATION.md`: §5 AP-03, AP-08, AP-12; §10
  Invariant 1, Invariant 4, Invariant 14.
- `DOMAIN_FOUNDATION.md` §7: independent confirmation of the
  six-concept domain-ownership list.
- Citation-precision note (not corrected here, no document edited):
  D10 §6 attributes "state domains, not aggregates" to "D07 §5"; D07
  §5 lists "Event Delivery State" but not those two terms verbatim.
  Loose/imprecise citation, not broken; the substantive conclusion is
  independently supported by `DOMAIN_FOUNDATION.md` §7.

## Approval Record

```text
Decision: Approved — ADW-07 Block 1 (the two new decisions restated in
Invariants 4 and 5; all other normative statements in this Block either
restate existing authority or remain explicitly OPEN/deferred)
Decider: Andrew (Project Owner)
Decision Date: 2026-08-08
Chapter Status: ADW-07 remains OPEN. This approval covers Block 1 and
exactly the two new decisions listed above. It does not approve the
three Open Questions, later ADW-07 subject matter, Event schema,
Event relationships, WP18 implementation, or ADW-07 as a whole.
```

---

## Block 2: Event Persistence Timing

**Document ID:** [not assigned — same numbering gap noted in Block 1]
**Workshop:** ADW-07 — Events, Audit, and Provenance
**Workshop Status:** OPEN
**Block:** Block 2 — Event Persistence Timing
**Block Status:** APPROVED
**Owner:** Project Owner
**Decision authority:** Project Owner
**Decider:** Andrew (Project Owner)
**Decision Date:** 2026-08-09
**Remaining ADW-07 work:** OPEN / NOT YET DECIDED
**Builds on:** Block 1 (Event Semantics — Core Definition), D07 (State Semantics), D10 (Deletion and Supersession) — all unmodified by this document.

**Recording note:** this is the second Project Owner-authorized incremental recording within the still-OPEN ADW-07 workshop. Block 1 was the repository's first such recording; neither Block 1 nor this Block establishes a general cross-workshop recording rule.

---

### Scope

This Block decides one question, in two clauses: whether a Domain Event's durable existence is contingent on downstream publication succeeding, and whether that existence is fixed at or before the publication attempt begins. It resolves Open Question 2 as recorded in Block 1, on the timing axis only. It does not decide the identity of Event relative to the Durable Audit / Outbox Intent artifact named in D07 §10, the persistence mechanism satisfying this requirement, or when D10's immutability trigger applies to Event specifically. All three remain open, named individually below.

### Decision

A Domain Event exists as a durable record before downstream publication is attempted. Its existence does not depend on publication succeeding.

### Existing Authority

**A. Sequence and downstream framing** (`D07_STATE_SEMANTICS.md` §10, D07.5) — the approved sequence is `Atomic Commit of New State Version → Durable Audit / Outbox Intent → Domain Event Publication → Projection Update`; publication and projection are downstream consequences of commit.

**B. Publication-failure protection** (`ARCHITECTURE_SPECIFICATION.md` §10 Invariant 14) — publication failure after commit does not erase authoritative business truth.

**C. Event's non-authoritative nature** (Block 1, Decision) — a Domain Event records occurrence; it does not itself hold or grant authority over authoritative state.

**D. Durability and immutability** (`D10_DELETION_AND_SUPERSESSION.md` §7.4, §6) — "The durable, immutable trace — significant transition records, audit records, attribution records, Domain Events — that exists independently of its subject's current lifecycle state... removable only via Physical Deletion" (§7.4); Domain Event is "Historical Record by construction and... never subject to Physical Deletion once committed" (§6). Durability and immutability are already established here — not invented by this Block. What is *not* established is the timing of that durability relative to publication (this Block's decision) or the exact moment "committed" refers to for Event (Residual Question R3).

None of A–D states Block 2's timing decision — that is the new content below.

### New Decision Approved by Project Owner

A Domain Event exists as a durable record before downstream publication is attempted; its existence does not depend on publication succeeding.

No approved source states this. D07.5 and §10 establish that publication is a downstream consequence of commit and that its failure doesn't erase business truth; D10 establishes that Event, once it is a Historical Record, is durable and immutable. Neither states *when* Event's durable record comes to exist relative to a publication attempt. This decision closes that gap, as a single proposition in two clauses, without asserting anything about Event's identity relative to other named artifacts, the mechanism satisfying it, or when D10's immutability trigger fires.

### Rationale

Two readings were tested. Reading A: Event exists durably before publication. Reading B: publication is the act that materializes Event. Neither is excluded by citation — this decision does not rest on eliminating Reading B textually, because no source does that.

Under Reading B, non-production could result from downstream infrastructure failure rather than from the deliberate semantic qualification rule established by Block 1 (Invariant 5: not every committed state mutation necessarily produces a Domain Event). The Project Owner prefers Reading A for that reason: once an occurrence qualifies for a Domain Event, its existence is not made contingent on downstream publication infrastructure succeeding.

One citation was checked and is not used as support here: D10 §6 states significant facts are "committed... to the owning aggregate's own transition history and Domain Events (D07 §10)." Checked against §10's actual text, that compressed phrasing is not there — §10 has "Atomic Commit of New State Version" (aggregate-scoped) and, separately, "Domain Event Publication" as a later step. Noted in Source Notes as a citation-precision finding; not repaired; not used as support for this decision.

### Invariants

1. A Domain Event exists as a durable record before downstream publication is attempted. `[NEW DECISION — PROJECT OWNER APPROVED; CLAUSE 1 OF THE SINGLE BLOCK 2 DECISION]`
2. A Domain Event's existence does not depend on downstream publication succeeding. `[NEW DECISION — PROJECT OWNER APPROVED; CLAUSE 2 OF THE SAME SINGLE BLOCK 2 DECISION]`

### Block 2 Residual Questions

**R1 — Event ↔ Audit/Outbox/Publication-Intent identity.** Whether Domain Event and the Durable Audit / Outbox Intent artifact named in D07 §10 are the same artifact, are distinct artifacts, one derives from the other, or whether that compound phrase identifies more than one artifact, is not determined by approved architecture. This Block's decision does not address it — it was written to avoid referencing that artifact's identity at all. This must be resolved before any later schema scope whose shape depends on Event/publication-intent artifact identity can be finalized.

**R2 — Persistence / Transaction / Consistency Mechanism.** How the durability requirement in this Block's Decision is physically satisfied — persistence representation, transaction boundary, outbox pattern, or otherwise — is unresolved. `D07_STATE_SEMANTICS.md` §14 assigns physical persistence, transactions, outbox, indexing, and recovery mechanics to ADW-08, which does not yet exist (`00_ARCHITECTURE/08_PERSISTENCE/` is absent). This constrains later WP18 persistence/schema design; this Block does not establish ADW-08 as an additional formal WP18 governance dependency — A-05's existing unblock sequence remains authoritative and unchanged.

**R3 — Event-specific "once committed" semantics.** D10 §6/§7.4/§8 Invariant 7 establish that Domain Event is immutable and never physically deleted once committed — that protection itself is not open. What is unresolved is the exact moment "committed" refers to for Domain Event specifically: D10 defines an analogous commit point only for state transitions (`D07_STATE_SEMANTICS.md` §4.6, "Transition Commit"), not for Event. This Block establishes when Event durably exists relative to publication; it does not assert that this is the same moment D10 means by "committed" for Event, nor that publication determines it. This affects exactly when D10's already-established immutability protection attaches to a given Event, and may affect future correction/supersession semantics for a durable-but-unpublished Event.

### Non-Goals / Deferred Questions

Not decided by this Block:

- Event qualification/significance rule — Block 1 Open Question 1.
- Event correction/supersession mechanism — Block 1 Open Question 3.
- Strict Event/publication-intent identity — Block 2 R1.
- Persistence/transaction/outbox mechanism — Block 2 R2 / ADW-08.
- Event-specific "once committed" trigger — Block 2 R3.
- Any Event/AuditRecord relationship.
- Any retry, delivery, or idempotency implementation.
- Any schema, table, or field shape.
- Correlation, causation, provenance representation, timestamps.
- Sensitive-data handling.
- All other Block 1 Non-Goals, unchanged and not restated here.

### Impact on Work Packages

**WP18** remains BLOCKED under Amendment A-05. Block 2 removes one semantic uncertainty but does not satisfy A-05's Definition of Done and authorizes no model, migration, repository, service, API, or schema implementation.

**WP19** remains unchanged. Not reopened or affected by this Block.

### Source Notes / Traceability

- `D07_STATE_SEMANTICS.md` §10, D07.5.
- `ARCHITECTURE_SPECIFICATION.md` §10 Invariant 14.
- `00_ARCHITECTURE/07_AUDIT/EVENTS_AUDIT_AND_PROVENANCE.md` (Block 1) — Decision, Invariant 5.
- `D10_DELETION_AND_SUPERSESSION.md` §6, §7.4, §8 Invariant 7 — durability, immutability, non-deletion of Domain Event as Historical Record.
- `D07_STATE_SEMANTICS.md` §14 — ADW-08's assignment of physical persistence, transactions, outbox, indexing, and recovery mechanics; `00_ARCHITECTURE/08_PERSISTENCE/` does not exist.
- Citation-precision note, not corrected here: D10 §6's phrase "committed... to the owning aggregate's own transition history and Domain Events (D07 §10)" is not literally supported by §10's text — loose/imprecise citation, not broken. Not used as support for this Block's decision. Not counted as a new numbered discrepancy in this pass.

### Approval Record

```text
Decision: Approved — ADW-07 Block 2. Exactly one new architectural
decision, consisting of two clauses:
  (1) A Domain Event exists as a durable record before downstream
      publication is attempted.
  (2) A Domain Event's existence does not depend on downstream
      publication succeeding.
Decider: Andrew (Project Owner)
Decision Date: 2026-08-09
Chapter Status: ADW-07 remains OPEN. Block 2 is APPROVED. Block 2
Residual Questions R1 (Event/publication-intent identity), R2
(persistence/transaction/consistency mechanism), and R3 (Event-specific
"once committed" semantics) remain OPEN. Block 1's Open Question 1
(qualification/significance) and Open Question 3 (correction/
supersession) remain OPEN. This approval does not extend to later
ADW-07 subject matter, Event schema, Event relationships, WP18
implementation, or ADW-07 as a whole.
```

---

## Block 3: AuditRecord Persisted Subject-Reference — Routing Decision

**Document ID:** [not assigned — same numbering gap noted in Blocks 1 and 2]
**Workshop:** ADW-07 — Events, Audit, and Provenance
**Workshop Status:** OPEN
**Block:** Block 3 — AuditRecord Persisted Subject-Reference / Routing Decision
**Block Status:** APPROVED
**Owner:** Project Owner
**Decision authority:** Project Owner
**Decider:** Andrew (Project Owner)
**Decision Date:** 2026-08-22
**Remaining ADW-07 work:** OPEN / NOT YET DECIDED
**Builds on:** Block 1 (Event Semantics — Core Definition), Block 2 (Event Persistence Timing), ADR-0014 (AuditRecord must durably identify its audited subject) — all unmodified by this document. D09 (Relationship Model), D10 (Deletion and Supersession) — both `APPROVED — CLOSED`, unmodified.

**Recording note:** this is the third Project Owner-authorized incremental recording within the still-OPEN ADW-07 workshop, and the first triggered by an ADR's routing obligation rather than a WP readiness pass. It is also the first Block in this workshop that was shown to the Project Owner for review prior to approval — Blocks 1 and 2 were each recorded only after approval had already occurred. This Block is recorded here in its approved, post-approval form.

---

### Scope

This Block decides only whether ADW-07 accepts substantive ownership of the WP19 AuditRecord persisted subject-reference question — ADR-0014's Q2 — under branch (a) of ADR-0014's routing obligation, rather than invoking branch (b). It does not decide Q2's persisted representation, Residual Question R1 (Event ↔ Audit/Outbox/Publication-Intent identity), AuditRecord's complete domain definition, the Event/AuditRecord relationship, Open Question 1 (significance rule), Open Question 3 (correction/supersession mechanism), GC-002, GC-006, or GC-007, or Residual Questions R2/R3. Those remain open or deferred, as stated below.

### Decision

ADW-07 accepts substantive ownership of the persisted AuditRecord subject-reference question (ADR-0014 Q2), under branch (a) of ADR-0014's routing obligation. Resolution of Q2's actual persisted representation remains deferred to a later, not-yet-numbered ADW-07 block, contingent on an evaluative framework this Block does not create (see Non-Goals).

### Existing Authority

- ADR-0014, Consequences: "Before WP19 model/migration implementation proceeds, ADW-07 must either (a) resolve the persisted AuditRecord subject-reference representation, or (b) explicitly establish that persistence representation is outside its scope and identify the decision owner and follow-on mechanism." This is existing authority for the fact that a decision is required and for the two branches available — not for which branch is correct. That choice is this Block's own decision, below.
- `ARCHITECTURE_SPECIFICATION.md` §7: ADW-07's declared purpose is "Define event semantics, immutable audit, provenance, correlation, and sensitive-data handling" — the only named workshop's scope statement that textually intersects an AuditRecord-shape question at all.
- `D10_DELETION_AND_SUPERSESSION.md` §3, §14: assigns "the detailed audit/event record schema for lifecycle transitions" to ADW-07 by name. Scoped to lifecycle-transition audit records specifically — a proper subset of WP19's actual scope ("high-impact actions" generally, `IMPLEMENTATION_BACKLOG.md` WP19 Goal), not a citation that by itself reaches all of Q2.
- This document, Block 1, Non-Goals: already deferred "AuditRecord's own domain definition; Event/AuditRecord relationship" to later ADW-07 work — adjacent to, but not identical with, Q2's persisted-shape question.

None of the above states that ADW-07 owns Q2 specifically. Each is partial, adjacent existing authority. Read together they were convergent evidence, not prior authority for the ownership question itself — that gap is what this Block closes, not what it finds already closed.

### New Decision Approved by Project Owner

ADW-07 accepts substantive ownership of Q2 under branch (a) of ADR-0014's routing obligation.

No approved source stated this directly before this Block. The three existing-authority citations above converge on ADW-07 without any one of them reaching Q2 by name; this decision is the act of closing that gap, as a Project Owner judgment on convergent evidence, not a restatement of something already established. Before this Block, "ADW-07 substantively owns Q2" was Inference. It becomes decision-level authority upon this approval — the earlier sources remain evidence for why the decision is coherent, not proof that it was already required beforehand.

### Rationale

Three lines of evidence were checked and found convergent, none alone sufficient: ADW-07's own declared scope ("immutable audit"); D10's partial schema deferral (lifecycle-transitions subset); and this document's own Block 1 Non-Goals deferral (domain definition and Event relationship). Every other named workshop's declared scope was checked against Q2 and found not to fit — ADW-08's scope ("repositories, transactions, outbox, idempotency, storage, indexing, and retention") is mechanism/storage language, not a domain-semantic "what does this record identify" question, consistent with ADR-0014's own finding that D09 §8's adjacent ADW-08 deferral does not textually reach AuditRecord; ADW-02/03/04/05/06/09/10's declared scopes do not intersect the question at all.

This absence is evidence, not proof of exclusivity. No presently established alternative owner was found for branch (b) — that is what this investigation supported. It does not establish that no alternative owner could ever validly have been created or designated: ADR-0014 explicitly permitted ADW-07 to identify a decision owner and follow-on mechanism under branch (b), and nothing in this Block forecloses that path for a future question found not to fit ADW-07. The Project Owner also already has a demonstrated channel to decide domain-adjacent questions directly, bypassing a not-yet-written workshop entirely (ADR-0013's precedent; ADR-0014's own Q1 decision) — that channel was considered for Q2 specifically in ADR-0014's Alternatives-considered section and declined there for lack of an evaluative framework, not for lack of authority to use it. This Block's branch-(a) choice is a judgment made on convergent evidence in the absence of a better-fitting alternative, not a claim that ADW-07 is the only workshop that could ever have been assigned this question.

### Invariants

1. ADR-0014 requires ADW-07 to resolve Q2 (branch a) or explicitly establish it is outside ADW-07's scope and route it elsewhere (branch b). `[EXISTING AUTHORITY]`
2. ADW-07 substantively owns the persisted AuditRecord subject-reference question (Q2), pending future resolution by a later ADW-07 block. `[NEW DECISION — PROJECT OWNER APPROVED]`
3. This ownership decision does not itself select, favor, or exclude any candidate persisted representation for Q2. `[NEW DECISION — PROJECT OWNER APPROVED]`

### Non-Goals / Deferred Questions

Not decided by this Block:

- Q2's persisted representation (composite FK, polymorphic reference, in-payload diff, opaque identifier, or any other candidate shape).
- Residual Question R1 (Event ↔ Audit/Outbox/Publication-Intent identity).
- AuditRecord's complete domain definition.
- The Event/AuditRecord relationship.
- Open Question 1 (event qualification/significance rule).
- Open Question 3 (event correction/supersession mechanism).
- GC-002, GC-006, GC-007 — all remain at their current Decision Register status, unaffected.
- Residual Question R2 (persistence/transaction/consistency mechanism — ADW-08's question) and Residual Question R3 (paused, P-01).

The evaluative framework Q2's shape decision requires — candidate representations, decision criteria, and their trade-offs — does not exist and is not created here. This is the same gap ADR-0014 cited when it declined to decide Q2 alongside Q1. This Block's approval does not make a future Q2 shape block ready to proceed; the missing framework remains the next prerequisite, recorded here as an absence, not invented.

### Impact on Work Packages

**Before this Block:** WP19 was blocked, with Q1 already closed by ADR-0014, Q2 unresolved, and ADR-0014's routing obligation still outstanding.

**After this Block:**
- **Q1 remains CLOSED** — unaffected, already settled by ADR-0014 — and continues as a binding, shape-neutral constraint on Q2's eventual representation. It is not itself an unresolved blocker.
- **ADR-0014's routing obligation is DISCHARGED** via branch (a).
- **ADW-07's substantive ownership of Q2 is ESTABLISHED**, by this Block.
- **Q2's persisted representation remains OPEN — NOT ESTABLISHED.**
- **The evaluative framework required to decide Q2 still does not exist** — the same gap ADR-0014 identified when declining to decide Q2 alongside Q1.
- **Therefore WP19 model/migration implementation remains BLOCKED / unauthorized** — not because Q1 or the routing obligation remain unresolved (they do not), but because Q2's representation itself remains undecided and lacks a framework.

Three states must be kept distinct: **routing resolved ≠ Q2 resolved ≠ WP19 implementation authorized.** "Routing closed" does not imply "path open" does not imply "WP19 implementation may proceed" — that inference chain is false and must not be drawn from this Block.

**WP18** is unaffected — still blocked under Amendment A-05, on independent grounds unrelated to Q2.

### Source Notes / Traceability

- `docs/adr/0014-auditrecord-must-durably-identify-its-subject.md` — Consequences section, the routing obligation itself.
- `00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md` §7 — ADW-07's declared scope line.
- `D10_DELETION_AND_SUPERSESSION.md` §3, §14 — partial schema deferral to ADW-07 (lifecycle transitions subset).
- `00_ARCHITECTURE/07_AUDIT/EVENTS_AUDIT_AND_PROVENANCE.md` (this document, Block 1) — Non-Goals deferral of AuditRecord's domain definition and Event relationship.
- `D09_RELATIONSHIP_MODEL.md` §8 — checked and found *not* to reach AuditRecord (its ADW-07 deferral is anaphorically scoped to D09's own R1–R11 relationships among six named concepts, none of which is AuditRecord); not used as support for this Block's decision, recorded here per the same discipline Block 2 applied to a citation it checked and did not use.
- `00_ARCHITECTURE/00_GOVERNANCE/DECISION_0002_AUTHORITY_HIERARCHY_AND_VOCABULARY_BASELINE.md` §3, line 56 — names ADW-07 as the future destination for "AuditRecord relationships" generically; existing authority for the destination, not for this Block's ownership decision (same distinction ADR-0014 itself draws for this citation).
- `50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md` — GC-002 Decision Register status (`Proposed`), unaffected by this Block.

### Approval Record

```text
Decision: Approved — ADW-07 Block 3. ADW-07 accepts substantive
ownership of the persisted AuditRecord subject-reference question
(ADR-0014 Q2) under branch (a) of ADR-0014's routing obligation.
Decider: Andrew (Project Owner)
Decision Date: 2026-08-22
Chapter Status: ADW-07 remains OPEN. Block 3 is APPROVED. Block 3
resolves only the routing question. It does not approve Q2's persisted
representation, R1, AuditRecord's complete domain definition, the
Event/AuditRecord relationship, OQ1, OQ3, GC-002/006/007, R2, or R3.
WP19 remains BLOCKED after this approval; this Block does not authorize
WP19 model, migration, repository, service, or API work.
```
