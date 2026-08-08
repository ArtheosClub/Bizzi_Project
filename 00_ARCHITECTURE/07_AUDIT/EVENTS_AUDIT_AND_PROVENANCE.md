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
