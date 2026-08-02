# ADR-0008: One document-status vocabulary — Draft / Active / Deferred / Superseded / Historical

- Status: Accepted
- Date: 2026-07-29
- Deciders: Project Owner (direct decision, following the comparison in `docs/planning/RKM_AUDIT_2026-07-26.md` §4.3)
- Governance level: L3 (cross-cutting documentation convention affecting every governance and specification artifact in the repository) — decided directly by the project owner, satisfying the sign-off this level requires.

## Context

`docs/planning/RKM_AUDIT_2026-07-26.md` §4.3 reported that multiple,
independently-invented lifecycle vocabularies had accumulated in the
repository, none reconciled against the others. The audit counted four.
A direct re-derivation from the files found **six**:

| Vocabulary | Values | Object type governed |
|---|---|---|
| RKM-01 §07.1 `Lifecycle` | `Draft` / `Active` / `Superseded` / `Historical` | a document |
| OIR-01 §3 `Current Status` | `Open` / `Accepted` / `Deferred` / `In Review` / `Closed` | a finding |
| `60_MODULE_SPECIFICATIONS/` | `Status: Draft`, plus five pipeline fields (`Not Started` / `Pending`) | a module |
| `70_ENGINEERING_SPECIFICATIONS/` | `Draft` / `Under Review` / `Approved` | an engineering-spec document |
| GC-001 §3 | `NOT REVIEWED` / `PASS` / `FAIL` / `WAIVED` / `NOT APPLICABLE` | a certification requirement |
| GC-002 | `VALID` / `INVALID` / `SUPERSEDED` / `PENDING REVIEW` | an evidence entry |

The decisive observation is that these six are **not six competing
answers to one question**. They govern different object types. Only
three of them — RKM-01's `Lifecycle`, the `60_` framework's `Status`
field, and the `70_` framework's `Status` — describe the same thing: the
current standing of a *document*. That overlap is genuine duplication.
The other three describe findings, verification verdicts, and evidence
validity respectively, and are not interchangeable with document status
or with each other.

## Decision

**One vocabulary governs document status across the repository:**

```text
Draft / Active / Deferred / Superseded / Historical
```

- **`Draft`** — authored but not yet in force; may still change materially.
- **`Active`** — in force and current.
- **`Deferred`** — valid and retained, but explicitly out of current scope by decision; re-enters scope when its stated condition clears. Deferral is never implied by inaction — it requires an explicit decision recording the condition.
- **`Superseded`** — replaced by a named successor document, which must be identified.
- **`Historical`** — retained as evidentiary record only; not replaced by a successor, and not in force.

This extends RKM-01 §07.1's existing four-value `Lifecycle` with
`Deferred`. RKM-01's set was taken as the base because it already
governs the correct object type and is already cited as the lifecycle
authority by RSM-01 §09, GC-001 requirement GC-F-06, and GC-002 evidence
entry EV-F-06.

**Scope of this decision — document status only.** The following are
explicitly **not** changed, and remain authoritative for their own object
types:

- `45_GATE_C_TRANSITION/OUTSTANDING_ITEMS.md` §3 — findings.
- `40_GATE_C/GC-001_GATE_C_CHECKLIST.md` §3 — certification requirements.
- `40_GATE_C/GC-002_EVIDENCE_REGISTER.md` — evidence entries.
- The `60_` framework's *pipeline* fields (Review / Approval /
  Implementation / Verification / Gate D) — these track a module's
  position in a build pipeline, not a document's standing. Only that
  framework's separate `Status` field falls under this ADR.

`70_ENGINEERING_SPECIFICATIONS/`'s ad-hoc `Draft` / `Under Review` /
`Approved` set is **retired**, folded into the vocabulary above.

## Consequences

- A reader encountering a status value on any document in this
  repository can resolve its meaning from one place.
- `Deferred` becomes a first-class, defined document status rather than
  an ad-hoc annotation. The deferrals of MS-007 and the `70_` framework
  already recorded on branch `agent/governance-consolidation` are
  conformant with this ADR as written, and require no rework.
- `70_`'s three-value set no longer exists; `Under Review` has no
  successor value, because review *progress* is a pipeline concern
  (tracked by the `60_` framework's Review field), not a document's
  standing. A document under review remains `Draft` until it is `Active`.
- The three retained vocabularies now have explicitly bounded scope,
  which prevents the reverse failure — someone "unifying" them later and
  destroying the distinctions they encode.
- Application is deliberately **not** performed by this ADR. Retiring the
  `70_` values touches files that exist only on the unmerged
  `agent/governance-consolidation` branch, so that work is sequenced
  after that branch merges.

## Alternatives considered

**Standardize every vocabulary on OIR-01 §3's set** (`Open` / `Accepted`
/ `Deferred` / `In Review` / `Closed`) — the initially-proposed option,
on the reasoning that `Deferred` had already been used from it as
precedent. **Rejected**: those are issue-tracking semantics. `Open` and
`Closed` are meaningless applied to a document. Worse, forcing GC-001's
verdicts into the set collapses `FAIL` and `WAIVED` both to `Closed` —
two opposite outcomes rendered indistinguishable inside a certification
package. The precedent concern was also unfounded on inspection: the
existing `Deferred` usages were applied to document `Status` fields, so
they conform to this ADR unchanged.

**Leave all six vocabularies in place.** Rejected: the three
document-status sets are genuine duplication, and the RKM audit found
zero documents outside RKM-01/RSM-01 using RKM-01's classification —
proliferation with no reconciliation was the observed failure mode.

**Invent a new seventh vocabulary superseding all six.** Rejected: it
would add a vocabulary to solve a problem caused by too many
vocabularies, and would invalidate the three purpose-built sets that are
working correctly.

## References

- `docs/planning/RKM_AUDIT_2026-07-26.md` §4.3 (the finding), §7 (the recommendation to consolidate)
- `06_REFERENCE/RKM-01_REPOSITORY_KNOWLEDGE_MODEL.md` §07.1 (the `Lifecycle` field this extends)
- `06_REFERENCE/RSM-01_REPOSITORY_STRUCTURE_MODEL.md` §09 (cites RKM-01's lifecycle as a placement input)
- `45_GATE_C_TRANSITION/OUTSTANDING_ITEMS.md` §3, `40_GATE_C/GC-001_GATE_C_CHECKLIST.md` §3, `40_GATE_C/GC-002_EVIDENCE_REGISTER.md` (the three retained, out-of-scope vocabularies)
