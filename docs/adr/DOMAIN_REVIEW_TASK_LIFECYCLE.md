# Domain Review — Task Lifecycle

**Status:** Proposed — awaiting Project Owner approval
**Purpose:** Determine, from D01–D10 and WP02 alone, whether Task is a
first-class entity or an association, what its `phase` values are, and
which of WP15's stated fields (`states`, `owner`, `priority`, `source
object`, timestamps) have an approved source — before any schema is
written.
**Governs:** WP15. Amendment A-04 (narrowing WP15's Deliverables to
model/migration/tests, and fixing its final field set) follows this
review.
**Not necessarily an ADR, and in one place, not this document at all.**
An ADR records a choice between admissible alternatives. Most conclusions
below are readings of an already-approved source, not choices among
several the sources leave open — those stay as conclusions in this
review. One is not: §3a finds that the five `phase` values' *transition
graph*, not the value list itself, is only partly sourced, and that gap
turned out to be a genuine choice, not a reading. §3a presents the gap
and stops there, unedited — the choice itself is recorded in
`docs/adr/0011-task-phase-transition-graph.md`, not retrofitted into this
review's own text. §10/§11 reflect the resolution; §3a does not, on
purpose.

**Two findings worth reading even if nothing else is**: §1 settles entity
status on D08's own vocabulary alone. §9 resolves WP02 §8's "rework"
wording as a Decision Outcome, not a sixth Phase value — a collapse that
would otherwise have surfaced during WP15's own implementation, the same
way WP13's did.

---

## 1. Is Task an entity, or an association between EnterpriseObject and an Actor?

This has to be settled before any field list, because it changes what
"field list" even means.

**Arguments weighed:**

- *For association*: strip `priority`, `progress`, and `owner`/`assignee`
  and what's left — `workspace_id`, `assignee_id`, `source_object_id`,
  `phase` — reads structurally like an association carrying state.
- *For entity*: D08 (`ADW_01_CORE_DOMAIN_SEMANTICS.md` §D08, "Aggregate
  Strategy") states plainly: "Work Item is a shared domain contract and
  coordination abstraction, not one universal aggregate root. Task, Case,
  and Project **are separate aggregate roots**." "Aggregate root" is not
  a description an association carries in this repository's own
  vocabulary — every other use of the term (Enterprise Object, Decision,
  Business Operation, Runtime Session, all in D08/D09/D10) names a
  first-class domain concept with its own identity and lifecycle, never
  a join.
- *For entity*: D10 §8 Invariant 6 gives Work Item terminal states
  (`completed`, `cancelled`) distinct from what it relates to. An
  association that terminates on its own schedule, independent of either
  side it associates, is behaving like an entity with two references, not
  like the reference itself.
- *For entity*: D09 R9's cardinality is **1 Work Item : 0..N Enterprise
  Objects** — the zero case is explicit and approved. An association
  cannot exist with nothing to associate; an entity that optionally
  references something can.

**Operational test applied**: can a Task be created without a
`source_object_id` and meaningfully reach a terminal phase? Yes — nothing
in D09 R9 (0..N, lower bound zero) or D10 §6/§8 makes Task's own phase
transitions conditional on the reference existing or resolving. The two
are independent state domains under D07 §5 ("a transition in one domain
does not automatically determine a transition in another domain unless an
explicit domain rule authorizes that dependency"), and no such rule is
written for Task↔EnterpriseObject.

**Conclusion: Task is an entity** — a Work Item specialization and
aggregate root per D03/D08, not an association. This is confirmed by
three independent sources (D08's own vocabulary, Invariant 6, R9's
cardinality), not a close call decided by the operational test alone.

---

## 1a. Validation after field reduction

Does reducing Task's field set (§4–§6 exclude `progress`, `priority`,
`assignee_id`, `owner_id`, `title`, `description` — see §10) change the
entity-vs-association conclusion?

**Finding: No.**

**Reasoning**: §1's conclusion rests on three sources, and none of them
counts columns. D08's "separate aggregate roots" is a statement about
Task's *kind* — a vocabulary fact true independent of how many fields the
concrete schema carries. D10 §8 Invariant 6's terminal states
(`completed`, `cancelled`, now fixed as genuinely terminal by ADR-0011)
are a behavioral fact about Task's *own* lifecycle machine — that
machine exists and terminates on its own schedule whether or not Task
also carries a `priority` or a `title`; a leaner Task is still a Task
with its own terminal states, not a lighter association. D09 R9's
zero-cardinality case (a Task may exist with no `source_object_id`) is
unaffected by the field reduction — that field survives the cut, and its
optionality was always the point being tested, not something the other
exclusions touch.

If anything, the reduced field set makes the entity conclusion *more*
legible, not less: what remains — `id`, `workspace_id`, `phase`,
`source_object_id`, timestamps — is precisely an aggregate root with its
own identity and its own governed lifecycle (§3, ADR-0011), optionally
referencing another aggregate. That is the shape D08 describes, not the
shape an association would take.

---

## 2. What a Task is

D03 (`ADW_01_CORE_DOMAIN_SEMANTICS.md` §D03, "Work Model"): "Work Item is
the shared representation of governed business work. Task, Case, and
Project are specialized Work Item types." D08 assigns Task its own
aggregate-root status beneath that shared contract. D04 keeps Task
distinct from Runtime Session: "Task and Runtime Session are separate
aggregates. A successful Runtime Session does not automatically complete
a Task" — so nothing about Task's schema may assume a Runtime Session's
outcome writes Task's state directly; that link, when it exists, is R5
(Reference, "the reference never grants Runtime Session authority to
mutate Work Item state").

---

## 3. Phase — five values, derived not chosen

D07 §6 defines Phase and Progress as orthogonal dimensions
("orthogonal... No aggregate... may collapse them into one universal
authoritative `status` field") — the same rule ADR-0009 applied to
`EnterpriseObject.phase`. **This section fixes Phase only.** Progress is
addressed in §4, separately, on purpose.

D10 §6's Per-Concept Lifecycle Capability table, Work Item row:
Archivable — Yes. Supersedable — Yes. "Can become immutable" — "Yes, once
completed, cancelled, or archived, its committed history becomes
immutable." D10 §8 Invariant 6: "A Work Item coordinated by a Business
Operation, or the target of a committed Runtime Session execution, cannot
be physically deleted — only **cancelled, completed, or superseded**."

Read together with EnterpriseObject's already-approved three
(`active`, `archived`, `superseded` — ADR-0009 §2, itself derived from
this same D10 §6 table), Task's row adds exactly two terminal values
neither Invariant 5 (Enterprise Object's row) nor ADR-0009 named:
`cancelled` and `completed`.

**Task's `phase`: `active`, `archived`, `superseded`, `cancelled`,
`completed`.** Five values, all attested directly by D10 §6/§8 — not
derived from WP02's scenario, the same discipline ADR-0009 insisted on
for EnterpriseObject ("not from any scenario"). `active` is the creation
value for the same reason it was for EnterpriseObject: every other value
presupposes a prior condition (`archived`/`cancelled`/`completed` each
describe something *having happened* to an active task; `superseded`
presupposes a predecessor).

**Terminal vs. non-terminal — deferred to §3a.** An earlier draft of this
section asserted `cancelled`/`completed`/`superseded` terminal by analogy
to EnterpriseObject's `superseded`. That analogy is not itself a source:
Task's set is wider than EnterpriseObject's, and terminality has to be
derived for Task's own values, not inherited from a different concept's
three-value case. §3a works through this properly, transition by
transition, before anything here is asserted as settled.

---

## 3a. Transition Matrix

The five values in §3 are a list, not yet proof they form one mutually
exclusive dimension. A single `phase` column can only hold one value at a
time — if a transition exists where the destination value can be reached
from more than one distinct prior condition, and nothing else records
which prior condition applied, that distinction is lost the instant the
transition commits. D10 §5.2 requires exactly the opposite for Archive
specifically: "identity, **current state**, and full history remain
resolvable and preserved." Whether that requirement is satisfiable by a
single five-value column depends on which transitions below are actually
permitted — which is why this has to be checked before a `CHECK`
constraint pins the five values as mutually exclusive.

Six transitions checked directly, plus the two baseline transitions
`superseded`'s status depends on:

| Transition | Permitted? | Source |
|---|---|---|
| `active` → `archived` | Permitted, reversible (`archived` → `active`) | D10 §5.2 ("Archive is reversible in principle"); §6 Work Item row, "Archivable: Yes" |
| `active` → `cancelled` / `completed` / `superseded` | Permitted, not reversible | D10 §8 Invariant 6 names all three as reachable from an active-and-coordinated Work Item |
| `completed` → `archived` | **Not addressed by any source.** D10 §6's "Archivable: Yes" is unqualified — it does not state which prior values archiving is reachable from. §8 Invariant 6 lists `cancelled, completed, or superseded` as alternatives *to physical deletion*, not as a closed statement about what happens after either is reached | D10 §6, §8 Invariant 6 — silent on this specific transition |
| `cancelled` → `archived` | **Not addressed by any source.** Same gap as above | Same |
| `completed` → `superseded` | **Not addressed by any source.** §5.4 defines Supersession generically ("a new subject explicitly and formally succeeds an existing one") without stating whether a `completed` Work Item is eligible to be succeeded | D10 §5.4 — silent on eligibility from `completed` |
| `cancelled` → `superseded` | **Not addressed by any source.** Same gap | Same |
| `superseded` → `archived` | **Not addressed directly.** Depends on whether `superseded` is terminal for Task at all — see below | D10 §8 Invariant 9 — written for the general case, not Task-specific |
| Is `superseded` terminal for Task? | **Not stated for Task.** ADR-0009 concluded terminal for `EnterpriseObject` by reading Invariant 9's "never overwritten to look like the successor" as prohibiting any further transition once superseded. Invariant 9 itself is written at the general (six-concept) level, not re-derived per concept, and nothing in D10 §6's Work Item row or §8 restates it for Work Item specifically | D10 §8 Invariant 9; `docs/adr/0009-enterprise-object-phase-lifecycle.md` "Consequences" (the EnterpriseObject-specific reading, not re-established here) |

**What is and isn't established**: the four `active → X` transitions are
directly sourced. Every transition originating from `cancelled`,
`completed`, or `superseded` — including whether any of the three permits
*any* further transition at all — is not addressed by name in any
approved source. This is a gap in the sources, not an error in this
review's reading of them. This review presents the gap rather than
filling it with an inference dressed as a finding.

**Resolved by ADR-0011**, not by this review. Two incompatible readings
of the same silence were both argued and neither survived as a citation
— a genuine choice between admissible alternatives, an ADR's subject
matter, not a Domain Review's. `docs/adr/0011-task-phase-transition-graph.md`
records the decision: `archived` reachable only from `active`;
`completed`/`cancelled`/`superseded` all terminal. This section is left
exactly as it stood before that ADR — the gap it identifies is real and
stays visible here; only §10/§11 below reflect the resolution.

---

## 4. Progress — excluded from the MVP entirely, not shipped unconstrained

D07 §6.4 defines the dimension ("how much of the planned work has been
completed or accepted") but no approved source — not D01–D10, not the GC
proposals, not `C3_COMPONENT.md` — shapes its values. This is a different
situation from `EnterpriseObject.type`: `type` had no enumeration but an
obvious, undeniable necessity (an object has *some* type). `progress` has
neither an enumeration nor an agreed representation — percentage, named
step, coarse stage, and free-form note are all consistent with D07 §6.4's
one-sentence definition, and none is preferred by any approved source.

Shipping any of those now would mean whoever writes the first row decides
Progress's actual shape by convention, silently, the same failure D07 §6
exists to prevent for Phase — just one dimension over. **Recorded as
deferred, not as an unconstrained column.** No `progress` field in WP15's
schema.

---

## 5. Priority — excluded from the MVP entirely

No approved source anywhere names `priority` for Task, Work Item, or any
of the six D09 concepts. Unlike `type` (no enumeration, but an evident
need — an EnterpriseObject unquestionably has *some* type) or `progress`
(an approved dimension with unshaped values), `priority` has **neither**
an approved source **nor** a demonstrated need: WP02's scenario is one
owner, one task, one recommendation. There is nothing to prioritize
*against* — priority is only meaningful relative to competing claims on
attention, and the MVP scenario has exactly one task in flight.

This is anticipated future need, which the Abstraction Justification Rule
(`CLAUDE.md`) now gates directly: a new field needs either a demonstrated
problem or to be a precondition for the next Work Packages. Neither
applies. **Reopen condition: concurrent tasks genuinely competing for
attention** — i.e., when a scenario exists where more than one open task
per actor is normal, not hypothetical.

---

## 6. Assignment — excluded from WP15 entirely, neither `assignee_id` nor `owner_id`

An earlier draft of this section proposed `assignee_id` as a nullable FK
to `users.id`, on the reasoning that it claims only R10's `assigned_to`
role rather than overclaiming a single "owner." That reasoning was sound
as far as it went, but it didn't go far enough: it still shipped a column
whose name promises any Actor and whose FK can only ever deliver a human.

D09 R10 names four of at least five distinguishable roles a Task's
lifecycle touches: `issued_by`, `performed_by`, `approved_by`,
`assigned_to`, `accountable_for`. WP02's own flow makes the *actual*
`assigned_to` target for this scenario the Process Analysis Agent, not a
human user — the submitting user issues the task, but execution is
assigned to an agent configuration. `AgentDefinition` doesn't exist yet
(blocked on ADW-05/GC-001, `IMPLEMENTATION_BACKLOG.md` WP14), and no
unified `Actor` table exists anywhere in Gate C today.

A column named `assignee_id` that can only reference `users` is a false
contract in a way `source_object_id`'s N≤1 simplification (§7) is not:
`source_object_id`'s name doesn't promise more than one object, so
service code reading it can't be misled about its cardinality. `assignee_id`'s
name promises "whoever this task is assigned to," and the schema can only
deliver "a human, if any" — service code written against it would
silently inherit a wrong assumption about what a Task assignment actually
is, exactly the kind of false-precision this review exists to prevent
(§2's D04 boundary and §9's rework finding are both instances of the same
discipline applied elsewhere).

It also doesn't earn its keep operationally: WP02's actual assignee
(the agent) can't be represented by a `users` FK regardless of what the
column is named, so shipping it doesn't make today's scenario more
supportable — it only adds a column that will be wrong the moment
anything tries to use it for its stated purpose.

**Excluded: no `assignee_id`, no `owner_id`.** Assignment is deferred
until whichever comes first: `AgentDefinition` (WP14/ADW-05), a general
Actor target, or R10 attribution properly modeled. If a genuinely
human-only assignment need arises before any of those, the honest name at
that point is `assignee_user_id` — narrower, not overclaiming — but
WP02 does not demonstrate that need now, so nothing ships under either
name in WP15.

**Creation attribution is likewise not a column here.** Same treatment
`EnterpriseObject.owner_id`'s sibling gap already established:
attribution belongs to the audit/provenance record (R10 itself says
attribution records are "Historical / immutable once recorded... mirrors
D07's transition-record and this project's audit-first principle" — that
is `AuditRecord`/ADW-07 territory), not to a field on the aggregate being
attributed to.

**Flagging plainly, not silently propagating**: R10 (Actor Attribution)
is unmodeled across the entirety of Gate C as it stands — not just here.
`EnterpriseObject.owner_id` has the identical gap, undocumented until
this review first surfaced it. Recording it here makes it visible on the
second occurrence rather than letting a third table repeat it without
comment — and it is recorded on the work-package side too, not only in
this document: `IMPLEMENTATION_BACKLOG.md` WP19 now notes it, since ADW-07
(the workshop R10's own text points to) already governs `AuditRecord`.

---

## 7. `source_object_id` — single nullable FK, 1-to-N simplification recorded

D09 R9: Work Item `relates_to` Enterprise Object, Reference category,
"neither owns the other," cardinality **1 Work Item : 0..N Enterprise
Objects**. The approved relationship permits a Task to relate to zero,
one, or many Enterprise Objects.

`source_object_id` as a single nullable FK to `enterprise_objects.id`
ships the **N ≤ 1** subset of the approved 0..N range. Four points
recorded explicitly, not just the first:

1. **D09 R9's full cardinality (0..N) is not overridden by this
   implementation.** The approved relationship still permits many; WP15
   simply doesn't build the general case yet.
2. **The single FK is not a final domain invariant.** It is an MVP-scope
   simplification, on the same footing as `WorkspaceMembership`'s
   omitted `updated_at` (ADR-0010) — a recorded choice, not a newly
   discovered constitutional limit on how many objects a Task may relate
   to.
3. **Moving to N > 1 requires a relationship table or the general D09
   mechanism** — not a reinterpretation of this column. `source_object_id`
   would be deprecated in favor of it, not widened in place.
4. **Service code must not assume a Task can, by nature, relate to only
   one EnterpriseObject.** The schema simplification is easy to migrate
   later; logic written against a false assumption about Task's actual
   domain shape is not. This applies even though WP15 ships no service
   code itself — it constrains whatever WP23+ eventually writes against
   this column.

WP02's own scenario only ever needs one ("Bizzi creates EnterpriseObject
and Task" — one of each, one relationship between them), so nothing
currently demonstrates a need for more. Recorded here so the
simplification is a visible decision, not a discovery two Work Packages
from now.

---

## 8. `title` / `description` — checked against WP02, not present on Task

WP02 §4/§6/§7 gives the *problem statement*, *observed symptoms*,
*proposed future-state process*, and the rest of the structured
recommendation as content belonging to the submitted business problem and
the agent's output — i.e., to the `EnterpriseObject` being analyzed and
to the eventual `Decision`/result, not to `Task` itself. WP02 §5's
canonical flow creates `EnterpriseObject` and `Task` from the same
submission, but the descriptive content attaches to the object being
analyzed; `Task` is the unit of work performed *on* that object,
referenced via `source_object_id` (§7 above).

No approved source — not WP02, not D01–D10, not `C3_COMPONENT.md` — puts
a title or description field on Task. Adding them by analogy to a
familiar issue-tracker shape would be exactly the model-first reasoning
this review is checking against. **Left out.**

---

## 9. The "rework" state in WP02 §8 — resolved, not a sixth Phase value

WP02 §8: "Request Rework — task returns to an explicit rework state with
comments." Worth resolving explicitly rather than leaving an apparent gap
between the scenario's own wording and the five-value Phase set in §3.

`approved`/`rejected` are already established (Domain Review for
EnterpriseObject, §4a) as Decision Outcome values (D07 §6.3), not
EnterpriseObject phases — "Request Rework" is the same category: an
Outcome of the *Decision* (WP30, D07 §6.3), not a transition of *Task's*
own Phase. D07 §5's rule applies again — a Decision reaching a
Request-Rework outcome does not itself require Task's Phase to change,
absent an explicit domain rule saying so, and none exists. A task sent
back for rework is still, in Phase terms, `active` — it has not reached
any of the five terminal-or-archival values in §3; it is simply
continuing. What "rework" actually changes is a matter for `Progress`
(§4, deferred) or the Decision's own record (WP30) — both already
deferred beyond this Work Package for independent reasons.

**No sixth Phase value.** `active` covers a task awaiting first
execution and a task returned for rework identically, which is
consistent with Phase answering "where is the subject in its governed
lifecycle" (D07 §6.1) rather than "what specifically is happening right
now" (that's Status, D07 §6.2 — also not in scope here, and also not
named by any approved source for Task).

---

## 10. Field summary

| Field | Included in WP15? | Source |
|---|---|---|
| `id` | Yes | Standard, all Gate C entities |
| `workspace_id` | Yes, required, real FK | ADR-0004 (blanket rule, every Gate C entity) |
| `phase` | Yes, five values, `CHECK`-constrained | D10 §6 + §8 Invariant 6 (values, §3); ADR-0011 (transition graph, §3a) |
| `progress` | **No** | D07 §6.4 defines the dimension; no approved value shape — §4 |
| `priority` | **No** | No approved source, no demonstrated need — §5 |
| `assignee_id` / `owner_id` | **No** | False-contract naming problem plus no demonstrated need for a human-only target — §6 |
| `source_object_id` | Yes, nullable FK to `enterprise_objects.id` | D09 R9; N≤1 simplification of approved 0..N — §7 |
| `title` / `description` | **No** | Not attested by WP02 or any approved source — §8 |
| `created_by` | **No** | Attribution deferred to audit infrastructure (ADW-07), same as `EnterpriseObject` — §6 |
| `created_at` / `updated_at` | Yes | Standard, all Gate C entities |

**Final WP15 field set**: `id`, `workspace_id`, `phase`,
`source_object_id`, `created_at`, `updated_at`. Six fields.

---

## 11. What follows

1. This review is approved (or corrected).
2. **§3a is resolved — by ADR-0011, not by this review.** §3a itself is
   left exactly as originally written, gap and all; ADR-0011 records the
   Project Owner's decision on the genuine choice §3a identified. This
   section and §10 above reflect that resolution; §3a's own text does
   not, on purpose — the review derives, the ADR decides, and neither
   should be edited to look like it did the other's job.
3. `phase` now carries a `CHECK` constraint enumerating all five values,
   per ADR-0011's transition graph.
4. Amendment A-04 narrows WP15's Deliverables to model/migration/tests
   (same correction A-02 already applied to WP13, same ADR-0005 reason)
   and fixes the field set to §10's six fields.
5. WP15 implements that field set, with the four Architecture Review
   Checklist answers written into its plan.

---

**Sources.** D01, D02, D03, D04, D05, D08 (`APPROVED`); D07, D09, D10
(`APPROVED — CLOSED`) — `00_ARCHITECTURE/01_DOMAIN/`. `WP02_FIRST_BUSINESS_SCENARIO.md`
(`50_IMPLEMENTATION/GATE_A/`) — the only approved scenario source. ADR-0009
and its own Domain Review (`DOMAIN_REVIEW_ENTERPRISE_OBJECT.md`) — the
precedent this review follows for method and for the `phase`/`type`
inclusion-exclusion pattern applied here to `phase`/`progress`/`priority`.
`CLAUDE.md` — Abstraction Justification Rule, applied to `priority`.
`50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md` WP15/WP19 — WP15's entry
Amendment A-04 corrects; WP19's entry records the R10/ADW-07 gap this
review surfaced. `docs/adr/0011-task-phase-transition-graph.md` — the
ADR resolving §3a's transition-graph gap. No approved source outside
these was found to define Task's fields:
`GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md` and `docs/c4/C3_COMPONENT.md`
were both checked and neither adds anything beyond restating WP15's own
wording.
