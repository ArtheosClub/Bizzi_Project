# ADR-0009: EnterpriseObject carries a three-value `phase`, not a universal `status`

- Status: Proposed
- Date: 2026-08-02
- Deciders: Project Owner (pending) — derived from `docs/adr/DOMAIN_REVIEW_ENTERPRISE_OBJECT.md`
- Governance level: L3 (cross-module domain contract; every Gate C entity either inherits this lifecycle or is explicitly excluded from it). Applies approved decisions D01–D10 to the schema; it does **not** change them, so no Architecture Change Request under DECISION_0003 §11 is required.

## Context

WP13's acceptance criteria specify "CRUD model with canonical ID, type,
**status**, owner, timestamps." That wording predates D07's closure
(2026-07-22) and cannot be implemented literally.

D07 §6 defines five orthogonal state dimensions — Phase, Status, Outcome,
Progress, Health — and LAW-D07-15 prohibits collapsing them into "one
universal authoritative `status` field." A column named `status` holding
lifecycle values is exactly the prohibited construction: it names one
dimension while carrying another, and invites Outcome values (`approved`,
`rejected`) and Progress values (`completed`) to accumulate in it later.

This is a Tier 2 constitutional constraint overriding Tier 4 planning under
the Authority Hierarchy (`ARCHITECTURE_SPECIFICATION.md` §3), so the planning
document is what gives way.

A first proposal derived four values from WP02's Gate A scenario. That was
rejected on the grounds that EnterpriseObject is the canonical form for *any*
business entity, and a lifecycle fitted to one scenario breaks on the second.
`DOMAIN_REVIEW_ENTERPRISE_OBJECT.md` re-derived it from D01–D10 instead and
produced a different, smaller answer. **This ADR records the Domain Review's
result; it does not restate its reasoning.** Where a claim below is
load-bearing, the review's section is cited.

## Decision

### 1. The field is named `phase`

D07 §6.1 defines Phase as "where is the subject in its governed lifecycle" —
exactly what these values express. `status` is reserved for D07 §6.2's
distinct question ("what is happening now within the current lifecycle
context"), which EnterpriseObject does not currently need and which must not
be conflated with this field if it later does.

### 2. Three values

| Value | Basis | Meaning |
|---|---|---|
| `active` | Domain Review §2 | Current, operationally relevant, authoritative for its own state |
| `archived` | D10 §5.2 | No longer operationally active; identity, state, and history remain fully resolvable |
| `superseded` | D10 §5.4, §8 Invariant 9 | A successor with its own identity has formally taken over its role |

New EnterpriseObjects are created directly `active`. Per Domain Review §1a
this is forced rather than chosen: the other two values are each *defined
relative to* a prior active condition, so neither is coherent as an initial
phase.

### 3. Permitted transitions

```text
creation   -> active
active    <-> archived      (archive; unarchive)
active     -> superseded
archived   -> superseded
```

Every other transition is prohibited, including any transition *out of*
`superseded`.

### 4. Constraints

- **`superseded` is terminal.** D10 §8 Invariant 9 forbids overwriting a
  predecessor to look like its successor; there is no transition out.
- **`archived` is not terminal.** D10 §5.2 makes Archive "reversible in
  principle... unless a concept-specific rule forbids it," and no such rule
  exists for Enterprise Object.
- **`deleted` is forbidden as a lifecycle state.** D10 §5.1 requires deletion
  to be qualified as Physical or Logical — "'Deletion' alone is never a
  sufficient lifecycle state name" — and D10 §12 (Binding consequence 3) makes
  a generic `is_deleted` boolean a defect rather than a shortcut. Physical
  deletion is separately constrained by D10 §8 Invariant 5.
- **`approved` / `rejected` / `completed` are not phases here.** They belong to
  Decision (Outcome, D07 §6.3) and Task (Phase/Progress, D10 §8 Invariant 6).
  Domain Review §4a establishes the boundary; WP02 §8 shows the scenario in
  which the temptation to merge them arises.
- **`deprecated` is not a phase.** D10 §5.8 makes Deprecation forward-looking
  guidance that never invalidates existing instances — a deprecated object is
  still active — so folding it into `phase` would collapse two dimensions
  (Domain Review §2).
- **Exactly one authority writes it**: the specialized Enterprise Object
  aggregate that owns the object (D07 §7). Not a Task, not a Decision, not a
  knowledge or projection process (Domain Review §4a).

### 5. This lifecycle is not inherited by other entities

Each Gate C entity's lifecycle is decided against D10 §6 on its own terms.
**The concrete case is RuntimeSession (WP21):** D10 §6 states it is explicitly
**not** supersedable — a retry is a new session related only by a Temporal
"follows" relationship (D09 §13) — and is **freely** physically deletable.
Applying `superseded` to RuntimeSession would breach D10 directly.

Event (WP18) and AuditRecord (WP19) take no phase column at all: D10 §6 makes
them Historical Record by construction, immutable on write. Task (WP15) uses a
superset — the three values plus `cancelled` and `completed` per D10 §8
Invariant 6. AgentDefinition (WP14) and ContextPackage (WP20) are unresolved
and are governed by Domain Review §5's open question, not by this ADR.

### 6. Stored as a constrained string, not a Postgres `ENUM`

`VARCHAR` with a `CHECK` constraint (named by the `ck_` convention in
`backend/app/db/base.py`). A Postgres `ENUM` makes value removal effectively
irreversible and value addition a schema-type migration; a `CHECK` constraint
is alterable in one migration. Given that this ADR's own value set is newly
derived, the reversible form is the appropriate one.

## Consequences

**Easier.** The prohibited construction cannot arise by accident: there is no
`status` column for Outcome or Progress values to drift into. Every Gate C
entity now has a recorded answer for whether it inherits this lifecycle, so
WP15/WP18/WP19/WP21 begin with the question already settled rather than
copying WP13's model by reflex.

**Harder — and this is a real cost.** Anyone reading WP13's acceptance
criteria alone will look for a `status` column and not find one. Step 3 of
this stage amends WP13 to close that gap, but the mismatch will persist in any
cached or exported copy of the plan.

**A constraint on future work, not on WP13.** D10 §12 (Binding consequence 4)
requires supersession to create a new aggregate instance *and* record a
D09-typed Supersession relationship — never mutate the predecessor in place.
That relationship has no representation yet, and this ADR deliberately does
**not** add a `superseded_by_id` column to create one: doing so would commit
to modelling a D09 relationship as a direct foreign key before the general
relationship mechanism has been designed, which is precisely an irreversible
decision that has not been made.

The practical effect is bounded, because WP13 delivers a model with no
service, repository, or API — nothing in WP13's scope performs any transition
at all. **Whichever work package first implements supersession must implement
the D09 relationship in the same change**, or `phase = 'superseded'` will be
set without the successor being resolvable, breaching D10 §12. Recorded here
because that WP does not exist yet and would otherwise inherit the gap
silently.

**Reversal cost if the value set is wrong**: one migration altering a `CHECK`
constraint, plus a data backfill if rows already carry a retired value. This
is why §6 chose `CHECK` over `ENUM`.

## Alternatives considered

**`status` with WP13's literal wording.** Rejected: LAW-D07-15 prohibits it
directly, and D07 is `APPROVED — CLOSED` inside a frozen architecture. The
planning document is Tier 4; D07 is Tier 2.

**Four values including `draft`.** Rejected: no approved source gives
Enterprise Object a pre-active phase. D10 §5's nine lifecycle definitions have
no such term and ADW-01 §5's behaviour chain begins at Intent → Decision.
Adding it would introduce a new domain concept into a frozen domain model.

**No lifecycle field on the shared abstraction at all**, leaving it entirely to
specialized types — arguable from D07 §7, which assigns state ownership to the
*specialized* Enterprise Object aggregate. Rejected because D10 §6 assigns the
lifecycle capability row to **Enterprise Object as a concept**, not to its
specializations. These three values are the shared subset every specialization
possesses; specializations add their own dimensions on top (Task being the
worked example). Omitting the shared field would make each specialization
re-derive it, which is how divergent vocabularies started in the first place
(ADR-0008).

**Two booleans (`is_archived`, `is_superseded`).** Rejected: D10 Lifecycle
Principle 2 and §12 (Binding consequence 3) forbid exactly this — an
undifferentiated flag as authoritative lifecycle state. It also cannot express
that `superseded` is terminal while `archived` is not.

**Postgres `ENUM` for the values.** Rejected per §6: reversibility.

## References

- `docs/adr/DOMAIN_REVIEW_ENTERPRISE_OBJECT.md` — the derivation this ADR records
- `00_ARCHITECTURE/01_DOMAIN/D07_STATE_SEMANTICS.md` §6, §7, LAW-D07-15 (`APPROVED — CLOSED`)
- `00_ARCHITECTURE/01_DOMAIN/D10_DELETION_AND_SUPERSESSION.md` §5, §6, §8, §12 (`APPROVED — CLOSED`)
- `00_ARCHITECTURE/01_DOMAIN/D09_RELATIONSHIP_MODEL.md` R7–R9, R11, §13
- `00_ARCHITECTURE/01_DOMAIN/ADW_01_DECISION_REGISTER.md` D02 (`APPROVED`)
- `00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md` §3 — Authority Hierarchy
- `00_ARCHITECTURE/00_GOVERNANCE/DECISION_0003_IMPLEMENTATION_BASELINE.md` §7, §11
- `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md` WP13 — the criteria this ADR amends
- `50_IMPLEMENTATION/GATE_A/WP02_FIRST_BUSINESS_SCENARIO.md` §8 — the scenario whose Outcome values must not leak into `phase`
- ADR-0004 (workspace scoping), ADR-0008 (document-status vocabulary — a different subject; see Domain Review §3)
- `30_BACKEND_IMPLEMENTATION_PLAN/12_IMPLEMENTATION_RISK_REGISTER.md` R-ARCH-001 (architecture drift)
