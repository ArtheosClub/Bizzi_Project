# ADR-0014: AuditRecord must durably identify its audited subject

- Status: Accepted
- Date: 2026-08-19
- Deciders: Andrew (Project Owner) — decision recorded 2026-08-19. Q1 and
  Q2 were graded separately because their evidentiary footing differs
  materially; the evidence is set out in Context below.
- Governance level: L3 (cross-module domain contract — WP19 blocks WP30,
  WP36). This decision is made directly by the Project Owner, ahead of
  and independent from ADW-07 (Events, Audit, and Provenance) — the
  workshop `DECISION_0002` §3 names as the eventual semantic destination
  for AuditRecord relationships, not yet written — analogous to
  ADR-0013's precedent of Project Owner judgment preceding a not-yet-
  written workshop. It does not change D01–D10 and does not purport to
  close ADW-07; no Architecture Change Request under `DECISION_0003` §11
  is required.

## Context

WP19 (AuditRecord Model, P0, Gate C) has been carried as buildable —
`IMPLEMENTATION_BACKLOG.md` currently marks it 🟢 — but a three-pass
readiness investigation (completed 2026-08-18/19) found its
target/subject-reference question splits into two, with materially
different evidentiary footing:

**Q1 — must an AuditRecord identify its subject at all?** Four sources
point the same direction, none independently authoritative: ADR-0005
line 23 ("the domain mutation **it records**" — a transactional-coupling
statement inside a same-transaction commit rule, not a schema
statement); `C4_DYNAMIC_CANONICAL_FLOW.md`'s
`record(AuditActions.TASK_COMPLETED, actorContext, task)` (Tier 5,
"Illustration of Tiers 2–4; not independently authoritative" —
`DECISION_0002` line 30 — and illustrating nothing Tier 2 establishes,
since D09 never names AuditRecord); `WP02_FIRST_BUSINESS_SCENARIO.md`
lines 73–74's scenario-ordering placement; and GC-002/006/007's shared,
largely uncited assumption (GC-006/GC-007's "target" language traces to
`GATE_C_WORKSPACE_ISOLATION_AND_AUDIT_ARCHITECTURE_REVIEW.md`, itself
"Status: Architecture Review — Planning Only" — GC-002 itself, the item
actually about `AuditRecord`→aggregate, never cites it). Two distinct
claims must not be conflated here: that an audit-write *call* receives
information about the subject (a service-contract fact) is not the same
claim as that the *persisted* AuditRecord durably identifies that
subject (a schema fact) — none of the four sources above establishes the
second. Before this decision, Q1 was REASONABLE INFERENCE, not
established fact.

**Q2 — what is the persisted structural shape of that reference**,
across five entity types (`Workspace`, `EnterpriseObject`, `User`,
`WorkspaceMembership`, `Task`) sharing one mechanism? No approved source
names a shape. D09 (`APPROVED — CLOSED`) never mentions AuditRecord
(confirmed by direct grep across `00_ARCHITECTURE/01_DOMAIN/`, zero
hits, verified independently on two separate passes). D09 §8's ADW-08
deferral — "any persistence representation of these relationships" — is
anaphorically scoped to D09's own eleven R1–R11 relationships among six
named concepts, none of which is AuditRecord; it does not reach this
question, and must not be extended to AuditRecord by analogy.
`DECISION_0002` (Tier 0) names ADW-07, not yet written, as the
destination for "AuditRecord relationships" generically, with GC-002
provisional in the interim — but makes no semantic/persistence split and
never mentions ADW-08 anywhere in the document. GC-002's own concrete
candidate (Alternative B, composite FK) carries Decision Register status
`Proposed`, GC-002's own text disclaims settled ownership ("ownership is
not settled by any approved source — it does not default to this
proposal"), and its composite-FK wording addresses a single target type
while WP19's subject spans five — a single-target composite FK does not
by itself solve a five-entity-type reference problem.

This ADR resolves Q1 only. Q2 remains open — see Consequences.

## Decision

**An AuditRecord must durably identify the subject of the audited
mutation.** An audit record that cannot be resolved to what was changed
is not a complete audit record for WP19.

**This decision is shape-neutral.** It requires that the audited subject
be durably resolvable from the persisted record. It does **not** require
a dedicated subject-reference column, and does not exclude
representations where the identification is carried within the record's
own content — for example within a before/after diff. Nor does it hold
that such a diff automatically satisfies this requirement: that remains
a candidate representation, not a presumed-sufficient one. Which
representation performs this function is Q2, and Q2 is not decided here.

Before this decision, whether a persisted AuditRecord had to identify
its subject was inference, not established fact. This ADR is the
authority that settles Q1 — it is not a restatement of something
ADR-0005, `C4_DYNAMIC_CANONICAL_FLOW.md`, WP02, or GC-002/006/007
already required. Those sources may explain why this decision is
coherent (see Alternatives considered); none of them is the authority
that creates it.

## Consequences

**Q2 is not settled by this decision, and gets its own explicit routing
obligation.** `DECISION_0002` (Tier 0, existing authority) names ADW-07
as the future semantic destination for AuditRecord relationships
generically — it does not say ADW-07 owns *persistence*, and never
mentions ADW-08. That silence is not filled by this ADR. Instead, this
ADR adds a new, explicit obligation, not inferable from `DECISION_0002`:

> Before WP19 model/migration implementation proceeds, ADW-07 must
> either (a) resolve the persisted AuditRecord subject-reference
> representation, or (b) explicitly establish that persistence
> representation is outside its scope and identify the decision owner
> and follow-on mechanism.

`DECISION_0002` supplies the destination (ADW-07); this ADR supplies the
obligation to use it to close or route the persistence question. The two
propositions must not be merged into "`DECISION_0002` requires ADW-07 to
resolve persistence" — that would misattribute a decision this ADR makes
to a document that doesn't make it. No persistence ownership is assigned
to ADW-08 by analogy — D09 §8's ADW-08 scope, textually, does not reach
AuditRecord.

**WP19's model/migration work is blocked**, effective this ADR, pending
Q2's resolution via the routing obligation above (or an explicitly
authorized interim representation). This blocker is created by this
ADR's Q1 decision plus the pre-existing Q2 gap plus the routing
obligation above — **it is not inherited from WP18.** PR #31
(2026-08-19) removed the `WP18 → WP19` dependency edge from
`IMPLEMENTATION_SEQUENCE.md` on independent sequencing grounds; that
correction stands and is not reopened here. "WP19 is blocked on an
ADW-07-related resolution path" and "WP19 depends on WP18" remain
materially different statements — WP19's blocker runs through
AuditRecord's own Q2 gap, not through Event.

**What this decision does not do.** It does not approve GC-002 or its
Alternative B — Alternative B remains a Proposed candidate only. It does
not choose among polymorphic-reference, composite-FK,
per-type-nullable-column, opaque-identifier, or in-payload
representations — all remain open candidates, none preferred. It does
not assign persistence ownership to ADW-08. It does not resolve GC-006
(high-impact mutation classification) or GC-007 (before/after
representation) — both remain `Requires Owner Decision`, unaffected by
this ADR. It does not define actor attribution or resolve `ActorContext`
— that is a separate dimension (**who** acted, not **what** was acted
on), blocked independently on ADW-02 via WP16's deferred half. It does
not modify D07, D09, D10, ADR-0005, or ADR-0013.

**Easier.** WP19's eventual model/migration work now has one settled
requirement to build toward instead of an inferred one: the persisted
AuditRecord must durably identify its audited subject. The structural
form that satisfies that requirement remains Q2.

**Harder / newly constrained.** WP19 does not become buildable by this
decision alone. Before this ADR, Q1 was not an established
authority-level requirement. After this ADR, durable subject
identification is required, but Q2 still leaves its persisted
representation unresolved. WP19 model/migration implementation is
therefore blocked by the new Q1 requirement together with the existing
Q2 gap and the new routing obligation.

## Alternatives considered

**No reference required.** Rejected on a coherence argument: an audit
record that cannot say what it audits does not support the Auditability
principle ADR-0005 itself invokes ("every decision can be traced and
verified," `Vision.md`/`01_GOVERNANCE/GOVERNANCE_MODEL.md`) —
verification requires resolving the record to a concrete subject. This
argument is reasoning, not a citation, and stands independently of the
four inference-grade sources in Context.

**The question is misframed.** No evidence found supports a framing
distinct from the Q1/Q2 split already applied above. Not adopted for
lack of any supporting basis beyond that split itself.

**Deciding Q2 now, alongside Q1.** Rejected. Q2 has no comparable
evaluative framework to what ADR-0013 applied for AgentDefinition's
classification (D02's five-criterion test) — no approved source states
criteria for choosing among Q2's candidate shapes for this specific
five-entity-type problem. Deciding it now would mean selecting from a
list of examples rather than applying an approved framework, and audit
records are treated as immutable, permanent Historical Record once
written (D10 §7.4 and the footnote following §6; see Reversibility) —
getting Q2 wrong is unusually expensive to correct later (GC-007's own
Decision Stability section: "Estimated future change cost: High...
retroactive shape changes are unusually costly"). Q2 is left open and
explicitly routed instead.

**Silence on Q2's ownership.** Rejected. Leaving `DECISION_0002`'s
ADW-07 destination as the only word on this, without the routing
obligation, would leave WP19 blocked indefinitely with no forcing
mechanism — the same failure mode the routing obligation exists to
prevent.

## Reversibility

Before WP19 implementation, reversal requires only a decision-record
change — no schema, data, or code exists yet to unwind.

After WP19 model/migration work proceeds under whatever shape eventually
resolves Q2, already-committed AuditRecord rows cannot be reshaped to
reverse this decision. D10 states this for Historical Records as a
class, though not by literally naming AuditRecord: the footnote
following §6 states that Domain Event and Significant Transition records
"are Historical Record by construction and are never subject to
Physical Deletion once committed" — protecting the records themselves,
not merely their producers. §7.4 defines "Historical Record" to include
audit records alongside Domain Events and significant transition
records, and draws the same permanence conclusion for the class as a
whole ("Historical Records are permanent under this constitution"). D10
never uses the string "AuditRecord" anywhere (confirmed by direct grep)
— the same citation-precision gap already on record for ADR-0013's D10
§6 reference (see `docs/adr/0013-*.md`'s Alternatives considered) — so
this claim rests on §7.4's general definition and the footnote's
parallel treatment of the other two named record types, not on a
sentence naming AuditRecord specifically.

## References

- `docs/adr/0005-audit-first-mutations.md` — cited as inference-grade
  evidence for Q1, not the authority that creates this decision
- `docs/c4/C4_DYNAMIC_CANONICAL_FLOW.md` — Tier 5, illustration only
  (`DECISION_0002` line 30)
- `50_IMPLEMENTATION/GATE_A/WP02_FIRST_BUSINESS_SCENARIO.md` lines 73–74
- `50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md` — GC-002
  (lines 199–234, 274–278, Decision Register line 1272), GC-006 (line
  702), GC-007 (line 807, Decision Stability lines 918–928)
- `50_IMPLEMENTATION/GATE_C_WORKSPACE_ISOLATION_AND_AUDIT_ARCHITECTURE_REVIEW.md`
  — source of GC-AUD-04/05, "Architecture Review — Planning Only"
- `00_ARCHITECTURE/00_GOVERNANCE/DECISION_0002_AUTHORITY_HIERARCHY_AND_VOCABULARY_BASELINE.md`
  §3 line 56 — names ADW-07 as AuditRecord relationships' future
  semantic destination; existing authority for the routing obligation's
  destination, not its content
- `00_ARCHITECTURE/01_DOMAIN/D09_RELATIONSHIP_MODEL.md` §1, §8 —
  confirms AuditRecord is outside D09's six concepts and R1–R11;
  confirms ADW-08's deferral does not textually reach AuditRecord
- `00_ARCHITECTURE/01_DOMAIN/D10_DELETION_AND_SUPERSESSION.md` §7.4 and
  the footnote following §6 — Historical Record immutability and
  permanence, cited precisely (not via §8 Invariant 7's literal wording,
  which is grammatically about a record's producer, not the record
  itself) in Reversibility
- `docs/adr/0013-agentdefinition-is-a-d02-enterprise-object.md` —
  structural and governance-level precedent for a Project Owner decision
  made ahead of a not-yet-written workshop; also the prior instance of
  the same D10-citation-precision gap noted in Reversibility
- `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md` — WP19 entry,
  synchronized by Amendment A-09
- `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` — Amendment A-09
