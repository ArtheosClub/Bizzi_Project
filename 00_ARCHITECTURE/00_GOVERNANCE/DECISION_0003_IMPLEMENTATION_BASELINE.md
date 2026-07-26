# DECISION 0003 — Implementation Baseline

Version: 1.0
Status: APPROVED
Class: Implementation Governance Decision (operational — activates
existing constitutional authority; creates no new architectural, domain,
or governance authority)
Owner: Project Owner
Approved by: Project Owner
Approval date: 2026-07-26
Effective: Immediately, per §2

## 1. Purpose

This Decision establishes the official Engineering Implementation
Baseline for the Bizzi Platform MVP backend build. The Architecture
Phase is complete: Decision 0001, DECISION_0002, ADW-01 (D01–D10), the
Architecture Baseline (ABR-01), the Engineering Governance Charter
(EGC-01), the Engineering Baseline, and the full implementation-planning
set (MVP Work Package Plan, Implementation Backlog, Sequence,
Milestones, Checklist) all exist and are active.

From this Decision forward, all repository work is implementation work
unless explicitly authorized through the Architecture Change Process
(§11). This Decision creates no new architecture. It activates the
transition from having an architecture to building against one.

## 2. Effective Date

2026-07-26.

## 3. Baseline Branch

`agent/architecture-specification-v1-1` is declared the official
Implementation Baseline Branch. It represents the complete architectural
state described in §1 — every document in the scope defined by §6 exists
on this branch in the state recorded by the Baseline Commit (§4).

## 4. Baseline Commit

The Baseline Commit is the HEAD of `agent/architecture-specification-v1-1`
immediately prior to this Decision, determined directly from the
repository:

```text
63552c3560bc4d2aa012be942bf1cda6d1c694f2
"Add ENGINEERING_BASELINE.md v1.0 (Active)"
```

## 5. Merge Policy

When `agent/architecture-specification-v1-1` is merged into `main`, it
**shall be merged without squash**. Its full commit history — every
governance, architecture, and implementation-planning commit that
produced the Baseline Commit — shall remain intact in `main`'s history.
The resulting merge commit becomes the official Implementation Baseline
Commit on `main`.

This Decision declares the policy; **it does not itself perform the
merge.** Executing the merge is a separate, explicitly authorized act —
`50_IMPLEMENTATION/ENGINEERING_BASELINE.md` §9 already recorded that the
branch-location decision (merge to `main`, or an explicit interim
alternative) is a precondition for Sprint 0, not something this Decision
resolves unilaterally.

## 6. Scope

Included in this baseline, and nothing else:

- Architecture Specification (`00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md`)
- Domain Foundation (`00_ARCHITECTURE/00_FOUNDATION/DOMAIN_FOUNDATION.md`)
- Domain semantics (`00_ARCHITECTURE/01_DOMAIN/ADW_01_CORE_DOMAIN_SEMANTICS.md`, `ADW_01_DECISION_REGISTER.md`, D01–D10)
- Constitution (`00_CONSTITUTION/AI-01_AUTHORITATIVE_INTERPRETATION.md`)
- Governance (Decision 0001, DECISION_0002, ABR-01)
- ADRs (`docs/adr/0001`, `0003`–`0007`; `0002` retained as historical record only, per its own Superseded status)
- Engineering Governance (`01_GOVERNANCE/EGC-01_ENGINEERING_GOVERNANCE_CHARTER.md`)
- Engineering Baseline (`50_IMPLEMENTATION/ENGINEERING_BASELINE.md`)
- MVP Work Package Plan (`50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`)
- Implementation Backlog, Sequence, Milestones, Checklist (`50_IMPLEMENTATION/IMPLEMENTATION_*.md`)
- Gate A documentation (`50_IMPLEMENTATION/GATE_A/`)
- Reference documentation (`06_REFERENCE/RKM-01_REPOSITORY_KNOWLEDGE_MODEL.md`, `RSM-01_REPOSITORY_STRUCTURE_MODEL.md`)

Inclusion in this scope records these documents as part of the baseline
as they currently stand. It does not change any document's own status —
RKM-01 and RSM-01 remain `DRAFT`, not approved for generation, exactly as
their own Document Control fields already state.

## 7. Frozen Areas

The following are explicitly frozen as of this Decision: Architecture,
Vocabulary (per DECISION_0002 §3), Domain Model (D01–D10), Repository
Structure (the repository's current, actual layout — not RKM-01/RSM-01's
proposed future structure, which remains an unapproved design pending
its own activation), Technology Stack (ADR-0007), Engineering
Methodology (EGC-01), Layering (ADR-0003), Authority Hierarchy
(DECISION_0002 §1), Governance.

No modification to any frozen area is permitted without an Architecture
Change Request (§11).

## 8. Remaining Open Areas

Recorded, not redesigned:

- GC-001 through GC-010 (`50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md`).
- ADW-05 (Agent/Provider/Model domain semantics).
- ADW-07 (Events, Audit, and Provenance domain semantics).
- Implementation Work Packages (WP12a, WP13–WP32, per `IMPLEMENTATION_BACKLOG.md`).

## 9. Branch Policy

`main` becomes the Official Implementation Branch, effective upon the
merge described in §5. No direct commits to `main`. All implementation
work must originate from short-lived feature branches merged via pull
request. Architecture work requires dedicated architecture branches,
kept separate from implementation feature branches.

Until the §5 merge occurs, `main` does not yet contain this baseline —
this policy governs `main`'s use from the point the baseline reaches it,
not before.

## 10. Development Policy

Implementation begins from this Baseline (§3, §4). Every implementation
pull request must reference:

- the applicable Work Package(s), per `IMPLEMENTATION_BACKLOG.md`;
- the applicable ADR(s);
- the Engineering Baseline (`50_IMPLEMENTATION/ENGINEERING_BASELINE.md`);
- this Decision (`DECISION_0003`).

No implementation may alter an architectural decision. A pull request
that would do so is out of scope for implementation and must instead
proceed through §11.

## 11. Architecture Change Process

Any architectural modification after this Baseline requires, in order:

```text
Architecture Change Request
        |
        v
Architecture Review
        |
        v
Architecture Approval
        |
        v
Architecture Decision
        |
        v
Implementation
```

No exception. This process operationalizes, and does not replace, EGC-01
§06's existing "Change requiring Architecture Governance" category — it
is the specific procedure by which that category is exercised for
architectural (as distinct from purely engineering) changes.

## 12. Baseline Activation

Upon this Decision:

- The repository officially enters the Implementation Phase.
- Sprint 0 may begin, against the unblocked Work Packages identified in
  `IMPLEMENTATION_BACKLOG.md` and `IMPLEMENTATION_SEQUENCE.md`, subject
  to the branch-location condition in §5/§9.
- Engineering Governance (EGC-01) becomes fully effective for all
  engineering activity within its scope.
- Architecture Governance (Decision 0001, DECISION_0002, ABR-01) remains
  active, exclusively for matters routed through the Architecture Change
  Process (§11).
