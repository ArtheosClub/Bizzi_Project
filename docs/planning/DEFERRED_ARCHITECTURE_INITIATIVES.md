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

## D-11 — Reusable AuditRecord subject-kind ↔ persisted-identity mapping layer

Q2-ST analysis identified an architecturally viable alternative in which
AuditRecord subject kinds are governed through an explicit reusable mapping
layer between logical subject kinds and one or more permitted persisted
identity forms (Q2-ST-O3).

The idea is deferred rather than rejected. Under the current recommended
Q2-ST-O2 rule, mapping is an exception mechanism rather than the default
architecture layer. Building a general mapping layer before any mapping
exception exists would introduce governance/resolver/versioning machinery
against predicted future specialization growth rather than a demonstrated
need.

**Reopen when:** the **first mapping exception is explicitly accepted**
under the Q2-ST subject-ranging authority — i.e. the first time one already-
authorized AuditRecord subject kind is permitted to resolve to an additional
persisted identity form that is not already covered by its canonical
persisted subject-identity contract.

That event is itself evidence that a reusable mapping abstraction may now
solve an existing problem. On reopen, compare continuing with explicit
per-exception authority against promoting a reusable versioned mapping
contract. The review must preserve D3/D4 historical stability, D5-equivalent
authority for expansion of the audited-subject universe, and accepted Q2-RI
per-realization weighting.

This entry does not authorize O3, any mapping exception, any resolver
infrastructure, or any new AuditRecord subject kind.

---

## D-12 — AR-2: reinstating main-push CI

The push: main trigger removal covers only initial publication of
feat/wp15-bounded-task-service. Block E item 4 requires:
"A main-push run is reinstated, under its own Owner admission, before any second
pull request to main or as soon as main can differ from a tested head,
whichever comes first."
This records the reopen condition, not permission to enable or execute CI.

MAINCI-A prospectively admits event-discriminated PR/push-main contracts and one restoration delivery PR (explicitly the second PR) plus one exact final-H fast-forward as the sole AR2-55 freeze exception. See ADR-0019 and external MAINCI-A source SHA-256 35abda606c016c60db4a4130835f99a9ef3120ed5aabb7ab338c3edf2e2695a4. This publication is not runtime proof: implementation, local runtime, publication, hosted PR, G2, main integration, push observation and Owner closure require their separate records. Restoration status: PENDING observed exact-main push backend/compose success, reviewed native before/after/forced/deleted evidence and explicit Owner closure. No closure is claimed. On that closure the special AR2-55 freeze ends and Block E item 4 is satisfied, without granting future PR/main writes; Record L and action permissions remain. Unprotected-main residual retained.

## D-13 — B4-E: deferred committed-audited-state interpretation

No B4-E/D10 exception is adopted. **Reopen when** more than one test genuinely
requires committed, audited state (Block G item 2), or a second local-only
candidate arises (Block L item 4: Owner reconsideration of B4-E). Neither trigger
automatically expands the one-file venue decision or deletion rules.

## D-14 — Option L: reconsider local-only verification venue

Editorial entry selected by Owner for this publication; not a DAI requirement
invented from Block L. Return the single lock node to CI only under a new
approved venue decision when admitted CI means satisfy Invariant 13 and
preserve-rows STOP, with proper implementation/runtime/evidence. Variables,
log streaming or post-test upload alone do not meet it (Block L item 10).
Coverage frequency is reduced, provenance is local collector/Owner machine,
and automation is reduced. Every exact candidate HEAD, including docs-only
or rebase, needs a new approved local gate/review; no reuse on matching subtrees.
Actual merge-result tree must equal tested tree; changed main is STOP.

Sources for D-12–D-14:
- External adopted source `workflow_BIZZI/2026-10_adw02/RC_DRAFT_OWNER_DECISION_BACKEND_CI_APPROVAL_AND_DECISION_2026-10-07.md`, SHA-256 `99d9efcdbd6644035cec2c13d16cb782648a4a114077f851b448cafbc2cb44a2`.
- External adopted source `workflow_BIZZI/2026-10_adw02/RC_DRAFT_OWNER_DECISION_G_B4_ALTERNATIVE_D_2026-10-07.md`, SHA-256 `30b02899692ad495bbab2f56df0c18bc1eaa51d984dbb28a05b2c7f6d5ded782`.
- External adopted source `workflow_BIZZI/2026-10_adw02/CODEX_DRAFT_OWNER_RECORD_L_OPTION_L_ARCHITECTURE_DECISION_2026-10-07_rev2.md`, SHA-256 `0123ced0601f832838cc0d0ccc4ab0c9a13c1bccdea30091d8b1e18b76d149b3`.

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
