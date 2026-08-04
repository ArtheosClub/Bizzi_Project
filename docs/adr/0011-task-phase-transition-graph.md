# ADR-0011: Task phase transition graph — `archived` reachable only from `active`

- Status: Accepted
- Date: 2026-08-04
- Deciders: Andrew (Project Owner), direct decision
- Governance level: L3 (cross-module domain contract — fixes the
  transition graph for `Task.phase`; does not change D07, D09, or D10,
  it resolves a case those sources leave open)

## Context

`docs/adr/DOMAIN_REVIEW_TASK_LIFECYCLE.md` §3 derives Task's five
`phase` values directly from D10 §6 (Per-Concept Lifecycle Capability,
Work Item row) and §8 Invariant 6: `active`, `archived`, `superseded`,
`cancelled`, `completed`. The value list is a reading, not a choice —
no admissible alternative exists.

The *transition graph* among those five values is a different question,
and §3a of the same review found it genuinely unaddressed by any
approved source for six specific transitions: whether `completed` or
`cancelled` can subsequently become `archived` or `superseded`, and
whether `superseded` is terminal for Task specifically (D10 §8
Invariant 9 establishes terminality for the general six-concept case and
was read that way for `EnterpriseObject` in ADR-0009, but Task's wider
value set was not separately re-derived there).

Two incompatible readings of the same silence were both argued before
this ADR, and neither survives as a citation:

- **Reading 1** (favoring a closed transition set): D10 §8 Invariant 6
  frames `cancelled`/`completed`/`superseded` as *alternatives to
  physical deletion*, which reads naturally as naming end states rather
  than way-stations with further transitions.
- **Reading 2** (the original objection to Reading 1, since withdrawn):
  that `completed → archived` would breach D10 §5.2's requirement that
  Archive preserve "current state," because a single `phase` column
  can't hold both `archived` and the fact that completion preceded it.
  This is wrong: D07 requires significant transitions to be preserved in
  immutable transition history, and D10 forbids rewriting recorded
  history, so `active → completed → archived` does not lose the
  completion fact — it lives in the transition history, not in the
  current-value column. A single column reading `archived` does not by
  itself prove two dimensions were collapsed.

With Reading 2 withdrawn, neither reading is compelled by the text.
D10 §6's unqualified "Archivable: Yes" and §8 Invariant 6's phrasing are
both compatible with either outcome. This is a genuine choice between
admissible alternatives — an ADR's actual subject matter, not a Domain
Review's.

## Decision

**Task's phase transition graph:**

```
creation -> active
active <-> archived        (reversible, per D10 §5.2)
active -> completed        (terminal)
active -> cancelled        (terminal)
active -> superseded       (terminal)

Terminal: completed, cancelled, superseded
  completed  -/-> archived
  cancelled  -/-> archived
  superseded -/-> archived
  completed  -/-> superseded
  cancelled  -/-> superseded
```

`archived` is reachable only from `active`, and is itself reversible back
to `active` (D10 §5.2, same as `EnterpriseObject`). `completed`,
`cancelled`, and `superseded` are each terminal: no transition leads out
of any of them, including to `archived` or to one another. `superseded`'s
terminality is established here for Task specifically, not inherited from
ADR-0009's `EnterpriseObject`-specific reading of Invariant 9 — per the
Domain Review's own instruction to derive it, not inherit it.

This closes the fork the same direction Reading 1 pointed, but as an
explicit Project Owner decision recorded here, not as a derivation the
Domain Review could have reached on its own — because it couldn't; the
sources permit the alternative too.

## Consequences

- WP15's `phase` column may now carry a `CHECK` constraint enumerating
  all five values, since the transition graph — not just the value list
  — is settled. The Domain Review's §11 held the `CHECK` back
  specifically pending this ADR; that block is lifted.
- A task that reaches `completed`, `cancelled`, or `superseded` cannot
  later be archived. If a real operational need for that later
  emerges — e.g. bulk-archiving old completed tasks for a UI view — it
  requires either superseding this ADR or introducing a second
  dimension (Outcome B, considered and rejected below), not a silent
  schema change.
- No service-layer enforcement exists yet (WP15 ships no service, per
  Amendment A-04) — this ADR fixes the schema-level `CHECK`, which is
  the enforceable half available now. Full transition-authority
  enforcement (D07 §8, "who may commit which transition") is WP15's
  eventual service, deferred to when `AuditService` exists at WP19, same
  as WP13's.

## Alternatives considered

**Outcome B — Phase plus a separate disposition dimension** (e.g.
`phase: active / completed / cancelled / superseded` alongside a second
column such as `disposition: current / archived`, allowing any terminal
phase to also be marked archived without losing which one it was).
Rejected for now: no current scenario (WP02, or any approved source)
demonstrates a need to archive a completed or cancelled task separately
from its terminal phase. If this decision turns out wrong, adding a
second dimension later is an additive migration — a new nullable column,
no data loss, no rewrite of existing rows. Removing an unnecessary
dimension already shipped is not additive. The asymmetric cost favors
not building it until a real need shows up, the same reasoning
`WorkspaceInvitation` was deferred under ADR-0010.

**Leaving the transition graph unfixed and shipping `phase` without a
`CHECK`.** Rejected: per the Domain Review's own §11, an unconstrained
five-value column with no enforced transition rule would let the
question resolve itself by accident — whatever the first service
happens to write — instead of by decision. That is the specific failure
this ADR exists to prevent.

## References

- `docs/adr/DOMAIN_REVIEW_TASK_LIFECYCLE.md` §3, §3a — the value
  derivation and the transition-graph gap this ADR resolves
- `docs/adr/0009-enterprise-object-phase-lifecycle.md` — the
  `EnterpriseObject`-specific precedent for `superseded`'s terminality,
  not directly inherited here
- `00_ARCHITECTURE/01_DOMAIN/D10_DELETION_AND_SUPERSESSION.md` §5.2, §6,
  §8 Invariant 6, §8 Invariant 9
- `00_ARCHITECTURE/01_DOMAIN/D07_STATE_SEMANTICS.md` §6, LAW-D07-13
  (Historical Integrity)
- `CLAUDE.md` — Abstraction Justification Rule (relevant to why Outcome B
  wasn't built pre-emptively)
