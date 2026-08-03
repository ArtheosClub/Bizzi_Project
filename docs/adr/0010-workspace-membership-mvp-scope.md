# ADR-0010: WorkspaceMembership MVP scope — no WorkspaceInvitation; `role` column ships, GC-004 stays unapproved

- Status: Accepted
- Date: 2026-08-03
- Deciders: Andrew (Project Owner), direct decision
- Governance level: L3 (cross-module domain contract — scopes the Gate C
  Architecture Decision Proposals GC-003/GC-004 for the MVP; does not
  change ADR-0004 or ADR-0006, it scopes what those already-accepted ADRs
  apply to)

## Context

GC-003 (Membership Invitation Row Occupancy) and GC-004 (Membership Role
Model) are two of the ten proposals in
`50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md`, which
remains globally `Draft — Architecture Analysis Only. No decision below
is Approved.` Both proposals block WP16/WP17 per
`50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md`.

Verified before this ADR, not assumed: neither proposal's recommendation
had actually been recorded as approved anywhere in the repository. A
switch to GC-003's Alternative B (a separate `WorkspaceInvitation`
entity) had been discussed but existed only in conversation — no ADR, no
C4 diagram, no WP entry reflects it. GC-004's Alternative A (single
`role` column) is consistent with `docs/c4/C3_COMPONENT.md`'s
already-confirmed `WorkspaceMembership` shape and with ADR-0006's
existing posture, but was never itself confirmed via the ADR-0006 update
GC-004's own Dependencies section calls for.

Note the naming collision this ADR had to navigate: `GC-003` and `GC-004`
also name two entirely unrelated Gate C certification milestone documents
(`40_GATE_C/GC-003_CERTIFICATION_REPORT.md`,
`GC-004_APPROVAL_RECORD.md`). This ADR concerns the Architecture Decision
Proposals of those IDs only. See `45_GATE_C_TRANSITION/OUTSTANDING_ITEMS.md`
OI-008 (expanded alongside this ADR) for the collision itself.

## Decision

**GC-003 — deferred / not applicable to the MVP, resolved as neither
alternative.** Both GC-003 alternatives answer *how to store an
invitation*; the MVP has no invitation at all, so choosing a storage
shape for something that doesn't exist is the wrong question to answer
now. MVP membership scope is exactly: `Workspace` -> owner `User` ->
active `WorkspaceMembership`. No `WorkspaceInvitation` entity, no
invitation token, no email-acceptance flow, no pending-membership state,
no expiration, no resend/revoke, no cleanup of expired invitations.

**GC-004 — remains unapproved as a proposal; the `role` column ships
anyway.** These are two separate facts:

- The `role` column ships on `WorkspaceMembership` now. A
  `WorkspaceMembership` without a `role` column silently asserts all
  memberships are equivalent — itself an unstated claim about the future
  model, not a neutral omission. `role` is `VARCHAR` with a `CHECK`
  constraint permitting exactly one value: `owner`.
- GC-004's actual question — single scalar `role` column vs. a
  role-assignment join table — remains unanswered and unapproved. It
  cannot be answered before a second participant type (a second role)
  exists to decide between. `CHECK (role = 'owner')` is deliberately the
  only permitted value today — the moment a second role is needed, GC-004
  must actually be decided (scalar vs. join), not silently resolved by
  whichever shape the `CHECK` happened to imply.

This mirrors ADR-0009's `phase`/`type` split: `phase` was fully decided
and `CHECK`-constrained to three values (a decided enumeration); `type`
shipped with no `CHECK` on its values at all (no approved source
enumerated them). The asymmetry here runs the other way for a different
reason: `role` **is** `CHECK`-constrained, to the one value actually
authorized today — not because the enumeration is decided, but because
exactly one value is currently authorized and nothing else may appear
until GC-004 is actually resolved. WP16's implementation must include a
test asserting the table carries exactly one `CHECK` constraint (on
`role`), so a wider enumeration can't be added quietly later without this
ADR being revisited.

## Consequences

- WP16 can proceed: `WorkspaceMembership(id, workspace_id, user_id, role,
  created_at)`, matching `docs/c4/C3_COMPONENT.md`'s already-confirmed
  shape, `role` constrained to `owner`.
- No `WorkspaceInvitation` table, migration, or code exists until an
  approved multi-user scenario reopens GC-003 — at which point the
  entity should be derived from that real scenario, not designed ahead of
  it (the same reasoning that produced ADR-0009's three-value `phase`
  instead of a scenario-derived four).
- The next role beyond `owner` (e.g. a Reviewer or Approver human role,
  per `docs/planning/PRE-CODING-BRIEF.md` §4) cannot be added to
  `WorkspaceMembership` without first resolving GC-004 (scalar vs. join)
  and amending or superseding this ADR — the `CHECK` constraint makes
  that a schema migration, not a silent code change, which is the point.
- GC-003 and GC-004 in `GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md` are
  not marked Approved by this ADR — that document's per-proposal status
  is untouched. This ADR records the MVP's actual scope decision
  independently, the same relationship ADR-0009 has to the Domain Review
  it derived from.

## Alternatives considered

**GC-003 Alternative A (invitation occupies the membership row, status
enum).** Rejected for the MVP: still designs storage for a scenario
(invite-by-email) that isn't in scope. `PRE-CODING-BRIEF.md` §7's
scenario implies a small number of known users per workspace, not a
self-serve invite flow.

**GC-003 Alternative B (separate `WorkspaceInvitation` entity).**
Rejected for the MVP for the same reason, and rejected as "record it now
for later" — per the Abstraction Justification Rule (`CLAUDE.md`), a new
abstraction needs either a demonstrated problem or to be a precondition
for the next Work Packages; a not-yet-approved multi-user scenario is
neither.

**Treating GC-004 Alternative A (single `role` column) as itself an
approval.** Rejected: treating "the column is a scalar" as equivalent to
"GC-004 is approved" would resolve a real open question (scalar vs. join)
by default, by virtue of a schema convenience — exactly the failure
ADR-0009's Architecture Review Checklist Q4 exists to catch ("does this
make irreversible a decision that hasn't actually been made yet?").
Shipping the column without ruling on GC-004 keeps the schema-level
question genuinely open.

**Leaving `role` off `WorkspaceMembership` entirely until GC-004
resolves.** Rejected: per the Decision section above, omitting it isn't
neutral — it would let every membership be silently treated as
equivalent, an unstated design claim of its own, and would require a
non-additive migration (adding a required column) the moment `owner`
needs distinguishing from anything else, rather than the additive one
(widening a `CHECK`) this decision leaves available.

## References

- `50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md` GC-003,
  GC-004 — the proposals this ADR scopes for the MVP without approving
- `docs/c4/C3_COMPONENT.md` "Multi-tenancy" section — the already-confirmed
  `WorkspaceMembership` join-entity shape this ADR's `role` column matches
- `docs/adr/0009-enterprise-object-phase-lifecycle.md` — the `phase`/`type`
  precedent this ADR's `role`/GC-004-deferral follows
- `docs/adr/0004-workspace-scoped-multi-tenancy.md`,
  `docs/adr/0006-authorization-model-mvp.md` — the ADRs this decision
  applies without changing
- `CLAUDE.md` — Abstraction Justification Rule
- `45_GATE_C_TRANSITION/OUTSTANDING_ITEMS.md` OI-008 — the `GC-*`
  namespace collision this ADR had to navigate, expanded alongside it
- `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md` WP16, WP17 — the work
  packages this ADR unblocks
