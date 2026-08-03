# Domain Review — EnterpriseObject

**Status:** Approved
**Purpose:** Define EnterpriseObject's domain role and lifecycle independently
of any scenario, so ADR-0009 derives the lifecycle field from the domain
rather than from Gate A's flow.
**Governs:** ADR-0009 (not yet written), WP13.
**Not an ADR.** It makes no decision; it establishes what the approved domain
already determines, and isolates the one thing it does not.

This review supersedes an earlier verbal proposal of `draft / active /
archived / superseded`, which was derived from WP02's scenario. Working from
the domain instead produces a different and smaller answer, and rules `draft`
out. The objection that prompted this review was correct.

---

## 1. What an EnterpriseObject is

D02 (`APPROVED`) already defines it:

> Enterprise Object is the stable platform abstraction for a durable,
> workspace-owned, business-relevant thing with identity, lifecycle,
> ownership, relationships, state, and governance requirements.

Two qualifiers in the approved set matter more than the definition sentence,
because both constrain what WP13 may build:

- **It is an abstraction, not an aggregate.** D02 continues: "while
  specialized types retain explicit contracts and invariants." D07 §7 assigns
  the state owner as the *"Specialized Enterprise Object aggregate"* — not the
  shared abstraction. WP13's table is therefore the shared contract; it is not
  the owner of any specialized type's authoritative state.
- **It is referenced, never owner-of.** D09 R7/R8/R9 give Business Operation,
  Decision, and Work Item each a `Reference` relationship *to* Enterprise
  Object, with "neither owns the other." D09 §Prohibition 5 forbids
  EnterpriseObject from holding an authoritative collection of what references
  it.

**The distinguishing test** — what makes something an EnterpriseObject rather
than not — follows from D02's five requirements read as conjunctive:

| Test | Excludes |
|---|---|
| Durable — outlives the operation that created it | RuntimeSession (execution-attempt state only, D04) |
| Workspace-owned — a Workspace is its isolation boundary (D01) | Nothing in Gate C |
| Business-relevant — the enterprise manages it (ADW-01 §3) | Event, AuditRecord (records *about* management) |
| Has governed state it authoritatively owns | Event, AuditRecord (immutable on write) |
| Not already one of the other four concepts | Actor, Work Item, Decision, Business Operation |

The fifth row is why EnterpriseObject is not a universal base class: ADW-01 §3
names five sibling concepts, and "no concept replaces another."

---

## 1a. Point of creation

**Creation is not a State Transition.** D07 §4.4 defines a State Transition as
a change "from one authoritative state version to another." Creation has no
prior version, so it falls outside that definition — it is the governed act
that produces the first authoritative version, which subsequent transitions
then change. D10 §9 states the same thing from the other side: a subject's
"own history begins at its own creation."

**Nothing else has to exist first.** This follows from D09's cardinalities
rather than from any convenience argument. R7 (Business Operation `targets`),
R8 (Decision `concerns`), and R9 (Work Item `relates_to`) all point *toward*
Enterprise Object, and each is created by the *other* side's owner — never by
Enterprise Object. From Enterprise Object's side all three are optional, and
D10 §8 Invariant 5 confirms it directly: an Enterprise Object referenced by no
committed Business Operation, Decision, or Work Item is physically deletable,
which is only meaningful if such an object can exist at all.

So an EnterpriseObject is brought into existence by an authorized act within a
Workspace (D01), independently of any Decision, Business Operation, or Work
Item. It may later be referenced by all three, or by none.

**It is created directly `active`, and this is forced rather than chosen.**
`draft` is unavailable (§2). The other two phases are each *defined relative to
a prior active condition*: D10 §5.2 defines Archive as "no longer operationally
active," and §5.4 defines Supersession as a successor to "an existing one."
Neither is coherent as an initial phase. `active` is the only admissible one.

**On attribution.** D02 gives Enterprise Object ownership, so the owning Actor
is part of its state. But note that D09 R10 attributes an Actor to
{Decision, Business Operation, Work Item, Runtime Session} — the set
deliberately **excludes** Enterprise Object; Actor's link to it is R11, a
non-attribution business association. The creating act is therefore made
auditable through the audit record (ADW-07, unwritten — deferred per ADW-01
§10), not through a D09 relationship. WP13 records ownership; it does not
model creation attribution, and should not invent a relationship to carry it.

---

## 2. States it passes through by its nature

D10 §6's Per-Concept Lifecycle Capability table (`APPROVED — CLOSED`) already
answers this scenario-independently, for the concept rather than for any
instance of it. Enterprise Object's row grants exactly: archivable, supersedable,
can become obsolete, can become immutable, physically deletable only under
§8 Invariant 5.

Read against D10 §5's nine definitions, that yields **three** Phase values:

| Phase | Approved basis | Meaning |
|---|---|---|
| `active` | The default condition the other two are defined against (D10 §5.2, §5.4) | Current, operationally relevant, authoritative for its own state |
| `archived` | D10 §5.2 | No longer operationally active; identity, state, and history remain fully resolvable |
| `superseded` | D10 §5.4, §8 Invariant 9 | A successor with its own identity has formally taken over its role; its historical validity for the period it was current is intact |

Three things are deliberately **not** Phase values:

- **`draft` is not one.** No approved source gives Enterprise Object a
  pre-active phase. D10 §5 has no such term, and ADW-01 §5's behaviour chain
  begins at Intent → Decision, not at a draft object. Introducing it would
  introduce a new domain concept — Architecture Review Checklist question 2,
  answered YES, which is a stop. This is exactly the failure the review was
  called to prevent.
- **`deprecated` is not one.** D10 §6 grants Enterprise Object "can become
  obsolete," but §5.8 defines Deprecation as forward-looking guidance that
  "never invalidates existing instances" — a deprecated object is still
  active. It is orthogonal to Phase, and folding it in would collapse two
  dimensions in violation of D07 §6 / LAW-D07-15.
- **`cancelled`, `invalidated`, `expired` are not.** D10 §6 does not grant
  these to Enterprise Object; §8 Invariant 6 assigns cancellation to Work
  Item, and §5.7 assigns expiration to time-bounded subjects. Borrowing them
  would import another concept's lifecycle.

The field is named **`phase`**, not `status`. D07 §6.1 defines Phase as "where
is the subject in its governed lifecycle" — precisely these three — and D07 §6
prohibits one universal authoritative `status` field. WP13's acceptance
criteria name a `status` column; that wording predates D07's closure and
cannot be implemented literally.

---

## 3. Terminal vs. non-terminal

D07 §6 requires this to stay explicit.

| Phase | Terminal? | Why |
|---|---|---|
| `active` | No | — |
| `archived` | **No** | D10 §5.2: "Archive is reversible in principle (a subject may be unarchived) unless a concept-specific rule forbids it." No such rule exists for Enterprise Object. |
| `superseded` | **Yes** | D10 §5.4 ends the predecessor's currency at a defined point; §8 Invariant 9 forbids overwriting it to look like the successor. There is no transition out. |

Physical deletion is not a phase. Per D10 §8 Invariant 5 an Enterprise Object
referenced by any committed Business Operation, Decision, or Work Item cannot
be physically deleted at all, and per D10 §12 (Binding consequence 3) a
generic `is_deleted` boolean is a defect, not a shortcut.

**Not a new vocabulary.** ADR-0008 settled *document* status — Draft / Active
/ Deferred / Superseded / Historical — for repository artifacts. `phase` here
governs a domain entity, is derived from D10 §5's approved lifecycle
definitions rather than invented, and shares two words with ADR-0008 by
coincidence of English, not by borrowing. The two never apply to the same
subject: no document has a `phase`, and no EnterpriseObject has a document
status.

---

## 4. Validation against the other Gate C entities

The point of this section is to find conflicts now rather than at WP15.
**Two conflicts and one gap were found.**

| Entity | WP | ADW-01 concept | Does the three-phase set apply? |
|---|---|---|---|
| Task | WP15 | Work Item specialization (D03, D08) | **Superset.** D10 §6 grants Work Item archivable and supersedable, so all three carry over — but §8 Invariant 6 adds `cancelled` and `completed`. Compatible; Task extends rather than contradicts. |
| Event | WP18 | Not an aggregate — a state domain (D07 §5) | **No.** D10 §6's closing note: Domain Event is Historical Record by construction, never subject to Physical Deletion once committed. Immutable on write; it has no lifecycle to model. A phase column here would be a defect. |
| AuditRecord | WP19 | Same as Event | **No.** Same basis. |
| RuntimeSession | WP21 | Runtime Session (D04) | **Conflicts.** D10 §6 states Runtime Session is explicitly **not** supersedable — a retry is a new session related only by a Temporal "follows" relationship (D09 §13) — and is **freely** physically deletable. Applying `superseded` to it would breach D10 directly. |
| AgentDefinition | WP14 | **Unclassified** | Undetermined — see §5. |
| ContextPackage | WP20 | **Unclassified** | Undetermined — see §5. |

The two conflicts are both cases where an entity must *not* inherit the shared
lifecycle. Neither blocks WP13; both are recorded here so WP18/WP19/WP21 do
not copy the EnterpriseObject model by reflex.

---

## 4a. Boundaries with Task, Decision, and Knowledge

§4 established that the lifecycle is not universal. This section states where
the *authority* boundaries fall, because that is where Phase and Outcome will
be tempted to merge.

**The general rule is already approved.** D07 §5: "A transition in one domain
does not automatically determine a transition in another domain unless an
explicit domain rule authorizes that dependency." No such rule exists for any
of the three below.

**Task (WP15).** Related by D09 R9 — Work Item `relates_to` Enterprise Object,
Reference category, "neither owns the other," the reference created and
maintained by the Work Item's own owner. A Task carries Progress (D07 §6.4)
and reaches `completed` or `cancelled` in its own Phase (D10 §8 Invariant 6).
**Completing a Task does not transition the EnterpriseObject it relates to.**
The two are separate state domains under D07 §5, and D09 gives the reference no
mutation authority in either direction.

**Decision (WP30).** Related by D09 R8 — Decision `concerns` Enterprise Object,
Reference, created by the Decision's own owner. A Decision produces an Outcome
(D07 §6.3, "what business result was authoritatively determined"), owned by the
Decision aggregate. **`approved` and `rejected` are Decision Outcome values.
They are not EnterpriseObject phases**, and a Decision reaching either does not
move the EnterpriseObject it concerns. D09 Prohibition 4 already forbids the
converse direction — a Decision's status may not be mutated by anything else —
and Prohibition 5 forbids EnterpriseObject from holding an authoritative
collection of what references it, so it cannot even accumulate its Decisions as
owned state.

**Knowledge.** Not a domain concept. `DOMAIN_FOUNDATION.md` §10 places
Knowledge among the capabilities that "operate across these layers" —
alongside Evidence, Audit, Provenance, Risk, and Compliance — rather than among
ADW-01 §3's five concepts. It has no aggregate, no lifecycle, and no row in
D10 §6. Knowledge derived from EnterpriseObjects is Derived State (D07 §4.3),
which "must never silently replace the authoritative source from which it was
derived" (also Architectural Law 11). **An EnterpriseObject is therefore never
a knowledge artifact, and no knowledge process may write its phase.**
`60_MODULE_SPECIFICATIONS/` contains no Knowledge module, consistent with this.

**The resulting rule for WP13**, stated once so ADR-0009 can cite rather than
restate it: EnterpriseObject's `phase` is written by exactly one authority —
the specialized Enterprise Object aggregate that owns it (D07 §7). Not by a
Task, not by a Decision, not by a knowledge or projection process.

---

## 5. The one open question

D05 states that Actor "is distinct from User Account, Role, **Agent
Definition**, and Runtime Session" — it says what AgentDefinition is *not*,
and no approved source says what it *is*. ContextPackage appears in no ADW-01
decision at all, and WP20 gives it an expiry, which is D10 §5.7 Expiration —
a capability Enterprise Object's §6 row does not grant.

So D10 §6 has no row for either, and the three-phase set can be neither
applied nor excluded for them.

> **Question for the Project Owner:** Are AgentDefinition and ContextPackage
> Enterprise Objects — in which case they inherit the §2 lifecycle and any
> addition (such as ContextPackage's expiry) needs its own basis — or are they
> concepts outside ADW-01's five, in which case their lifecycles are
> undetermined and WP14/WP20 cannot proceed on this review?

This blocks WP14 and WP20. It does **not** block WP13.

---

## 6. What follows

1. This review is approved (or corrected).
2. ADR-0009 records the decision: field named `phase`, three values, terminal
   semantics per §3, with §2's exclusions stated so they are not re-litigated.
3. WP13 implements it, with the four Architecture Review Checklist answers
   written into its plan.

WP14 and WP20 wait on §5.

---

## 7. Project Owner Decision

Decision: **Approved**
Decider: Andrew (Project Owner)
Decision Date: 2026-08-03
Approved Commit or PR: PR #13 (`docs/domain-review-enterprise-object`)

### Owner Decision Record

```text
Decision: Approved
Reason: EnterpriseObject's domain role and lifecycle, derived
independently of any single scenario from D01-D10, reviewed in full and
found correct. Supersedes the earlier scenario-derived
draft/active/archived/superseded proposal. Governs ADR-0009 and WP13.
```

---

**Sources.** D01, D02, D03, D04, D05 (`APPROVED`); D07, D09, D10
(`APPROVED — CLOSED`) — `00_ARCHITECTURE/01_DOMAIN/`. Concept model:
`ADW_01_CORE_DOMAIN_SEMANTICS.md` §3, §5, §8. WP definitions:
`50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`. Authority hierarchy:
`00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md` §3. No approved source outside
these was found to define EnterpriseObject's lifecycle: the Gate C
Certification Package, `60_MODULE_SPECIFICATIONS/`, and WP02's scenario were
each checked and none does.
