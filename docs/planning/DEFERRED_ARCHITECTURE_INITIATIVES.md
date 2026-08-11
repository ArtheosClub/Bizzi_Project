# Deferred Architecture Initiatives

A strategic review of this repository proposed eleven improvements. The
project owner adopted three immediately (the Abstraction Justification
Rule in `CLAUDE.md`, `PROJECT_MAP.md`, the Purpose-header convention) and
is deferring four here, deliberately, with recorded trigger conditions —
not dropping them. Two more are rejected outright (see "Explicitly not
doing" below).

**Why deferred rather than built now:** all four are sound ideas, and all
four are new architectural layers. The same review that proposed them
concluded with a moratorium on new architectural layers, per the
Abstraction Justification Rule this file is referenced from. That tension
— good idea, wrong time — is the reason for deferral, not doubt about
their value. Building any of them now would repeat the pattern both
2026-07-26 audits already flagged: governance output outpacing shipped
`backend/` code.

---

## D-01 — Architecture Execution Layer

Automated CI verification of authority chain, traceability (ADR→WP,
WP→Code, Module→Engineering Spec), and architecture drift.

**Reopen when:** 5–10 modules are implemented. Verification tooling needs
something to verify; with two models in `backend/` today, it would be
infrastructure built ahead of its subject. The review's own premise here
— "a team of 5–10 developers" — is hypothetical today.

## D-04 — Machine-readable Knowledge Graph

A single JSON/YAML index linking Decision → ADR → Module → Engineering
Spec → Work Package → Implementation → Tests, enabling dependency,
authority, and coverage graphs.

**Reopen when:** the chain has enough real instances to be worth indexing
— roughly the same 5–10 module threshold as D-01. Note the relationship
to RKM-01: the RKM audit recommended cutting RKM-01 §10 from twelve
generated artifacts to two, rather than expanding it. Any future graph
work should scope down RKM-01, not add a parallel mechanism.

## D-05 — Mandatory Module → Engineering Spec → WP → PR chain

Making the chain enforced rather than available.

**Reopen when:** the `70_` Engineering Specification layer comes out of
`DEFERRED — post-MVP` status. Enforcing a chain through a deferred layer
would block MVP coding by side effect — the same trap already caught and
handled in PR #8.

## D-10 — Architectural KPIs

Engineering metrics: ADRs implemented, module specs with code, Work
Packages complete, decisions covered by tests.

**Reopen when:** D-01 exists. These metrics are outputs of the
verification layer; building them separately means building the same
traversal twice.

---

## Explicitly not doing

- **RKM-01 as a service** (`rkm validate/trace/graph/orphan/authority`
  commands). The RKM audit's own recommendation stands instead: scope
  RKM-01 down, add one CI hook that fails when a new top-level directory
  appears without an RKM entry. One check that runs beats five commands
  nobody invokes.
- **Any repository-wide retrofit pass** — applying the Purpose-header
  convention, or any other new convention, to the existing corpus. New
  and substantially-edited documents only, going forward.

---

## Paused Investigations (not Deferred Architecture Initiatives)

Entries in this section are **not** `Deferred` under ADR-0008
(`docs/adr/0008-document-status-vocabulary.md`). `Deferred` is a
document-status value that requires an explicit decision to remove
something from current scope. The items below are open architecture
questions whose further investigation the Project Owner has paused
pending a named trigger — the question remains live, nothing has been
removed from scope, and no position between its live readings has been
taken. Distinct heading, distinct entry prefix (`P-`, not `D-`),
deliberately, to avoid a reader conflating this with the Deferred
Architecture Initiatives above.

### P-01 — ADW-07 Block 2 R3 (Event-specific "once committed" semantics)

`00_ARCHITECTURE/07_AUDIT/EVENTS_AUDIT_AND_PROVENANCE.md`, Block 2,
Residual Question R3, remains OPEN exactly as approved. Investigation
found that D10's "once committed," applied to Domain Event, does not
currently establish whether it denotes a temporal boundary (Temporal
Trigger reading) or merely scopes the existing immutability rule to
already-durable Events (Scoping Qualifier reading); both remain
textually possible, and this entry resolves neither.

**Reopen when** any of the following first occurs:

- Block 1 OQ3 (correction/supersession) reaches a concrete design point
  requiring an answer to whether a durable-but-unpublished Domain Event
  may be mutated, or must instead be corrected via a new record;
- ADW-08's persistence design reaches a point where the distinction
  between a Domain Event's durability and its commitment (in D10's
  sense) becomes materially relevant to that design;
- WP18's schema design reaches a point requiring — or explicitly and
  deliberately declining — a commit-phase state, field, or timestamp
  for Domain Event.
