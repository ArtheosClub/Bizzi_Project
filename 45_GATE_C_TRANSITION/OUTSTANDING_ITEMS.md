# Outstanding Items Register — Gate C Certification Transition

## 00. Document Control

| Field | Value |
|---|---|
| Document ID | OIR-01 |
| Title | Gate C Outstanding Items Register |
| Version | 1.3 |
| Status | **OPEN REGISTER** (permanent governance record; not a certification instrument) |
| Document Type | Lifecycle-Managed Governance Register |
| Part of | Gate C Transition Record (companion to the Gate C Certification Package — GC-001 Certification Checklist, GC-002 Evidence Register, GC-003 Certification Assessment Report) |
| Repository | ArtheosClub/Bizzi_Project |
| Supersedes | OIR-01 v1.2 (findings and classifications unchanged; OI-009 closed) |

**Version History**

| Version | Change | Findings Affected |
|---|---|---|
| 1.0 | Initial register: twelve Outstanding Items captured from GC-003 §5 | OI-001–OI-012 (created) |
| 1.1 | Refined into a lifecycle-managed governance register: terminology, lifecycle columns, expanded Decision values, Outstanding Item Lifecycle section, Acceptance of Residual Risk section, expanded Governance Rules, expanded Exit Mechanisms, Validation Rules, Repository Integrity (permanence) section | None (no finding added, removed, reclassified, or reweighed) |
| 1.2 | OI-004 closed — PR #2 merged (`dfb8804`, 2026-07-27), resolving the underlying repository condition. Closed directly by Project Owner authorization, 2026-08-03, under OIR-01 §10 Exit Mechanism 3 (Repository Change) | OI-004 (closed) |
| 1.3 | OI-009 closed — `implementation-baseline-v1.0` tag pushed to the remote, resolving the underlying repository condition. Closed directly by Project Owner authorization, 2026-08-03, under OIR-01 §10 Exit Mechanism 3 (Repository Change) | OI-009 (closed) |

This register is not a corrective action plan. This register is not a
backlog. This register is not an implementation roadmap. It exists
solely to preserve traceability between the Gate C Certification
Assessment and the unresolved Outstanding Items that may be considered
after Gate C has been formally closed, and to govern the lifecycle of
each such item until its formal closure. Nothing in this register
modifies, reinterprets, or supersedes the certification outcome recorded
in GC-003.

**Terminology note**: this register refers to every entry as an
**Outstanding Item** (or, equivalently, **Outstanding Finding**), never
as a "non-conformity" — that term belongs to GC-003 §5, which remains
the sole authoritative record of the certification-level assessment.
Each Outstanding Item's underlying audit classification — **Critical**,
**Major**, **Minor**, or **Observation** — is carried forward unchanged
from GC-003 and is never renamed, reweighed, or reclassified by this
register.

---

## 1. Purpose

**Purpose**: to provide a single, authoritative, lifecycle-managed record
of every unresolved finding identified during the Gate C Certification
process (GC-001, GC-002, GC-003), so that no Outstanding Item is lost,
duplicated, or silently forgotten between Gate C Certification and
whatever review or planning activity follows it — and so that, when an
Outstanding Item is eventually closed, that closure is itself traceable,
authorized, and evidenced.

**Scope**: this register captures Outstanding Items already recorded in
GC-001 (the Certification Checklist), GC-002 (the Evidence Register),
and GC-003 (the Certification Assessment Report). It introduces no new
finding, no new evidence, and no new architectural, governance, or
engineering content. Every item in §3 traces to an existing finding in
one of those three documents. This refinement (v1.1) adds lifecycle
governance structure only; it adds, removes, or reclassifies no finding.

**Relationship to GC-003**: GC-003 issued the Gate C certification
recommendation — CONDITIONAL PASS, with five explicit conditions (GC-003
§9) — on the basis of 0 Critical, 4 Major, 5 Minor, and 3 Observation
findings (GC-003 §5, Appendix — Assessment Statistics). This register
catalogues those same twelve Outstanding Items for lifecycle-managed
transition purposes. It does not re-evaluate, re-weigh, upgrade, or
downgrade any of them.

**Relationship to GC-004 (Gate C Approval)**: GC-003 §10 reserves the
certification decision itself to GC-004, which does not yet exist. This
register does not substitute for GC-004, does not approve anything, and
does not recommend an approval outcome.

**Relationship to GC-005 (Gate Closure)**: GC-003 §10 reserves formal
Gate C closure to GC-005, which does not yet exist. This register does
not close Gate C.

**Relationship to Architecture Epoch IV**: DECISION_0003 §12 records that
the repository enters the Implementation Phase upon DECISION_0003, and
that Sprint 0 may begin against unblocked Work Packages. Epoch IV
planning, if and when it occurs, is expected to consult this register for
a complete inventory of what remains open — but this register does not
itself constitute Epoch IV planning, and creates no Epoch IV work
package.

**Relationship to Implementation Planning**: `IMPLEMENTATION_BACKLOG.md`,
`IMPLEMENTATION_SEQUENCE.md`, `IMPLEMENTATION_MILESTONES.md`, and
`IMPLEMENTATION_CHECKLIST.md` (all `50_IMPLEMENTATION/`) already exist and
already record WP12a–WP32. This register does not create, modify, or
reference a new work package. Where an Outstanding Item is already
reflected in that planning set (e.g., ADW-05), this register records the
cross-reference only; it does not restate or re-sequence that planning.

---

## 2. Classification Rules

Every Outstanding Item in §3 is classified along two independent axes,
both carried forward unchanged from the Gate C Certification Package and
never altered by this register:

**Category** (domain of origin) — exactly one of the following nine
values. No additional category is introduced.

- **Architecture**
- **Governance**
- **Repository**
- **Engineering**
- **Documentation**
- **Process**
- **Naming**
- **Branch Management**
- **Repository Hygiene**

**Audit Classification** (severity, as issued by GC-003 §5) — exactly one
of the following four values. No additional value is introduced, and no
item's Audit Classification is changed by this register.

- **Critical**
- **Major**
- **Minor**
- **Observation**

Category reflects the domain of the underlying finding as recorded in its
source document (GC-001's GC-A through GC-F domains, per GC-001 §4).
Audit Classification reflects the severity GC-003 §5 already assigned. A
change to either value would constitute reclassification, which this
register does not perform.

---

## 3. Outstanding Items Register (Master Register)

Twelve Outstanding Items, corresponding exactly to the twelve findings
recorded in GC-003 §5 (4 Major, 5 Minor, 3 Observations; 0 Critical). No
item below originates outside GC-001, GC-002, or GC-003. No item has been
added, removed, or reclassified since v1.0.

**Current Status values** (exactly five, no others): `Open` / `Accepted`
/ `Deferred` / `In Review` / `Closed`. Default: `Open`. All twelve items
were `Open` as of v1.1. **As of 2026-08-03, OI-004 and OI-009 are both
`Closed`** (see §3 and §7/§10) — both authorized directly by the Project
Owner, under OIR-01 §10 Exit Mechanism 3 (Repository Change); Branch
Management (OI-004) and Repository Hygiene (OI-009) are both categories
the Project Owner may close per §7. The remaining ten items are
unchanged since v1.1.

**Decision values** (exactly nine, no others): `Accept` / `Resolve Later`
/ `Architectural Review Required` / `Governance Review Required` /
`Repository Cleanup` / `Reserved` / `Closed by ADR` / `Closed by
Decision` / `Closed by Repository Change`. The three `Closed by *` values
were reserved for future use as of v1.1; `Closed by Repository Change`
now applies to OI-004 and OI-009 (§3).

| Item ID | Origin | Finding | Category | Audit Classification | Current Status | Decision | Disposition Rationale | Closure Reference | Date Opened | Date Closed | Verification Authority | Verification Status | Target Epoch | Owner | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OI-001 | GC-003 §5 (Major #1); GC-002 EV-D-03, EV-A-09; GC-001 GC-A-09, GC-D-03 | The Provider/Model catalog-scope proposal (`GC-001` in `GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md`) remains unapproved, and ADW-05 (Agent/Provider/Model domain semantics) remains unwritten. Together these block `AgentDefinition`, `RuntimeSession`, and nine of Gate D's ten work packages. | Architecture | Major | Open | Architectural Review Required | Requires an Architecture Change Request (DECISION_0003 §11) to approve the catalog-scope proposal and commission ADW-05; not a repository-mechanical fix. | (none — not closed) | 2026-07-26 | | Project Owner (Architecture Change Process, DECISION_0003 §11) | Pending | Epoch IV | Project Owner | Already disclosed and accepted as a condition in `ENGINEERING_BASELINE.md` §9's Conditional Go and in GC-003 §9 Condition 1. Not a newly discovered gap. |
| OI-002 | GC-003 §5 (Major #2); GC-002 EV-C-08 | Seven Document IDs (ARR-01, AGR-01, ARC-01, CR-01, CR-02, EAR-01, GMR-01), cited within `ABR-01_ARCHITECTURE_BASELINE_RESOLUTION.md` and `EGC-01_ENGINEERING_GOVERNANCE_CHARTER.md`, correspond to no committed file in the repository. | Repository | Major | Open | Resolve Later | Resolution requires a governance determination of whether the missing review artifacts should be reconstructed, formally noted as historical-only, or the citations otherwise reconciled — not a mechanical cleanup by itself. | (none — not closed) | 2026-07-26 | | Repository Maintainer (GC-001 §8 signature role) | Pending | Epoch IV | Project Owner | Limits independent auditability of the historical governance record (GC-003 §4.3, R-2). GC-003 §9 Condition 2 records this as an accepted, disclosed traceability gap. |
| OI-003 | GC-003 §5 (Major #3); GC-002 EV-B-08; GC-001 GC-B-08, §8 note | Three of GC-001 §8's five requested certification signature roles ("Architecture Review Board," "Chief Architect," "Chief Orchestrator") are Art-of-Business roles (`01_GOVERNANCE/GOVERNANCE_MODEL.md`) with no defined equivalent in the Bizzi Platform MVP's own governance model. | Governance | Major | Open | Governance Review Required | Requires a Project Owner governance determination mapping (or formally declining to map) each Art-of-Business signature role to an MVP-track authority. | (none — not closed) | 2026-07-26 | | Project Owner (Tier 0, DECISION_0002 §1) | Pending | Epoch IV | Project Owner | GC-001 §8 already identifies de facto substitute authorities (Project Owner; Engineering Governance/EGC-01) without inventing a new role. GC-003 §9 Condition 3: must be resolved before GC-001 §8 is actually executed for a signature cycle. |
| OI-004 | GC-003 §5 (Major #4); GC-003 §4.6; `REPOSITORY_RELEASE_REPORT.md` (PR Review) | Pull Request #2 (`claude/gate-c-platform-backbone`) remains open; five of its files (real, non-conflicting documentation reconciliation) are not yet merged into `main`. | Branch Management | Major | Closed | Closed by Repository Change | Resolvable by merging the remaining reconciliation files via an approved pull request; no architectural or governance decision is required. | Merge Commit `dfb8804` (PR #2, `claude/gate-c-platform-backbone`, merged 2026-07-27) — Exit Mechanism 3 (Repository Change), §10 | 2026-07-26 | 2026-08-03 | Project Owner (Andrew) | Confirmed | Epoch IV | Project Owner | File-by-file resolution already identified in `REPOSITORY_RELEASE_REPORT.md`. GC-003 §9 Condition 4. |
| OI-005 | GC-003 §5 (Minor #1); GC-002 EV-C-05b, EV-F-07b; GC-001 GC-C-05, GC-F-07 | `docs/planning/WORK_PACKAGES.md` lacks a physical supersession banner at the file level, despite `CLAUDE.md`'s Key Entry Points table already asserting that status. | Repository Hygiene | Minor | Open | Repository Cleanup | A direct file edit applying the banner closes this item; no decision or review is required beyond the edit itself. | (none — not closed) | 2026-07-26 | | Repository Maintainer (GC-001 §8 signature role) | Pending | Epoch IV | Project Owner | Also recorded as a Repository Risk in `REPOSITORY_RELEASE_REPORT.md`. GC-003 §9 Condition 5. |
| OI-006 | GC-003 §5 (Minor #2); GC-002 EV-A-08, EV-C-04, EV-F-03, EV-F-04; GC-001 GC-A-08, GC-C-04, GC-F-03, GC-F-04 | No dedicated cross-reference/link-validation artifact exists in the repository. Four separate GC-001 requirements share this one underlying gap. No specific broken reference has been demonstrated by any evidence reviewed. | Process | Minor | Open | Resolve Later | Resolution requires deciding what form a cross-reference validation artifact should take before one can be produced; a process design question, not a single mechanical fix. | (none — not closed) | 2026-07-26 | | Engineering Governance (EGC-01) | Pending | Epoch IV | Project Owner | GC-002 §6 records this as one gap recorded once, applying to all four requirement IDs, rather than four independent gaps. |
| OI-007 | GC-003 §5 (Minor #3); GC-002 EV-A-10; GC-001 GC-A-10 | `Aggregate` (D08, Aggregate Strategy) has no standalone formal definition within `ADW_01_CORE_DOMAIN_SEMANTICS.md`. | Architecture | Minor | Open | Architectural Review Required | Adding a formal domain-term definition is an architecture-governed change to a frozen area (Domain Model, DECISION_0003 §7) and requires the Architecture Change Process. | (none — not closed) | 2026-07-26 | | Project Owner (Architecture Change Process, DECISION_0003 §11) | Pending | Epoch IV | Project Owner | Per GC-003 §4.1, does not block currently-unblocked work packages. |
| OI-008 | GC-003 §5 (Minor #4); GC-002 §0 (Naming note), EV-C-02 (Comments) | This Gate C Certification Package's own document ID, `GC-002`, collides in form with the pre-existing, unrelated, unapproved `GC-002` Architecture Decision Proposal ("Composite Foreign Keys") in `GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md`. | Naming | Minor | Open | Reserved | GC-002's own header states resolving the collision is outside that document's scope; this register does not reopen that scope determination. | (none — not closed) | 2026-07-26 | | Repository Maintainer (GC-001 §8 signature role) | Pending | Not applicable | Project Owner | GC-002's own header states resolving the collision is outside that document's scope. This register does not resolve it either. |
| OI-009 | GC-003 §5 (Minor #5); GC-003 §4.6; `REPOSITORY_RELEASE_REPORT.md` (tag-push attempt) | The `implementation-baseline-v1.0` release tag exists as a local annotated tag object but was not successfully pushed to the remote (outbound proxy returned `HTTP 403` on every attempt). | Repository Hygiene | Minor | Closed | Closed by Repository Change | Resolvable by a successful tag push once the underlying access constraint clears; no decision or review is required. | Tag `implementation-baseline-v1.0` pushed to `origin` (2026-08-03), pointing at merge commit `576465f15d8e35656ad8ff3f6ed5e954ebb74fe8` — Exit Mechanism 3 (Repository Change), §10 | 2026-07-26 | 2026-08-03 | Project Owner (Andrew) | Confirmed | Epoch IV | Project Owner | Local tag object correctly points at merge commit `576465f15d8e35656ad8ff3f6ed5e954ebb74fe8`; ready to push once the underlying access constraint is resolved. |
| OI-010 | GC-003 §5 (Observation #1); RSM-01 §08 (Namespace Analysis); GC-002 EV-C-03 | Root-level `GOVERNANCE_MODEL.md` and `CAPABILITY_MAP_v1.0.md` exist as content-divergent duplicates. | Repository | Observation | Open | Reserved | Art-of-Business track; explicitly outside Gate C Certification scope per DECISION_0002 §1 and GC-003 §2; not reopened by this register. | (none — not closed) | 2026-07-26 | | Repository Maintainer (GC-001 §8 signature role) | Pending | Not applicable | Project Owner | Art-of-Business track; explicitly outside Gate C Certification scope per DECISION_0002 §1 and GC-003 §2. |
| OI-011 | GC-003 §5 (Observation #2); RSM-01 §08 | `06_PLAYBOOKS/` remains empty while 102 `PB0*.md` files sit at repository root. | Repository | Observation | Open | Reserved | Art-of-Business track; explicitly outside Gate C Certification scope, same basis as OI-010. | (none — not closed) | 2026-07-26 | | Repository Maintainer (GC-001 §8 signature role) | Pending | Not applicable | Project Owner | Art-of-Business track; explicitly outside Gate C Certification scope, same basis as OI-010. |
| OI-012 | GC-003 §5 (Observation #3); GC-002 EV-A-09; DECISION_0003 §8 | ADW-07 (Events, Audit, and Provenance domain semantics) remains unwritten. | Architecture | Observation | Open | Resolve Later | Not currently blocking any Gate C work package; awaits its own domain workshop rather than an immediate architectural or repository action. | (none — not closed) | 2026-07-26 | | Project Owner (Architecture Change Process, DECISION_0003 §11) | Pending | Epoch IV | Project Owner | Per GC-003 §5 Observation #3, not currently blocking any Gate C work package; DECISION_0002's Vocabulary Baseline provisionally governs the affected relationships. Also recorded as a Remaining Open Area in DECISION_0003 §8. |

---

## 4. Traceability

Every Outstanding Item in §3 contains the following five traceability
fields, none of which is invented — each is drawn directly from an
existing GC-001, GC-002, or GC-003 citation:

- **Originating Document** — GC-001, GC-002, and/or GC-003.
- **Originating Section** — the specific section or requirement domain
  within that document.
- **Originating Finding** — the specific finding ID, non-conformity
  number, or checklist requirement ID.
- **Evidence Reference** — the GC-002 Evidence ID, where one exists.
- **Future Closure Reference** — left blank in this revision; populated
  only when the item is formally closed, per §7 (Outstanding Item
  Lifecycle) and §10 (Exit Mechanisms).

| Item ID | Originating Document | Originating Section | Originating Finding | Evidence Reference | Related Repository Artifact | Future Closure Reference |
|---|---|---|---|---|---|---|
| OI-001 | GC-001, GC-002, GC-003 | GC-A / GC-D domains; GC-003 §5 | GC-A-09; GC-D-03; Major Non-Conformity #1 | EV-A-09; EV-D-03 | `GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md` (GC-001 proposal); `00_ARCHITECTURE/01_DOMAIN/` (ADW-05, unwritten) | (blank) |
| OI-002 | GC-002, GC-003 | GC-C domain; GC-003 §5 | GC-C-08; Major Non-Conformity #2 | EV-C-08 | `ABR-01_ARCHITECTURE_BASELINE_RESOLUTION.md`; `EGC-01_ENGINEERING_GOVERNANCE_CHARTER.md` | (blank) |
| OI-003 | GC-001, GC-002, GC-003 | GC-B domain, §8; GC-003 §5 | GC-B-08; Major Non-Conformity #3 | EV-B-08 | `40_GATE_C/GC-001_GATE_C_CHECKLIST.md` §8 | (blank) |
| OI-004 | GC-003 | §4.6; §5 | Major Non-Conformity #4 | (none — see `REPOSITORY_RELEASE_REPORT.md`) | `50_IMPLEMENTATION/REPOSITORY_RELEASE_REPORT.md` (PR Review table) | (blank) |
| OI-005 | GC-001, GC-002, GC-003 | GC-C / GC-F domains; GC-003 §5 | GC-C-05; GC-F-07; Minor Non-Conformity #1 | EV-C-05b; EV-F-07b | `docs/planning/WORK_PACKAGES.md` | (blank) |
| OI-006 | GC-001, GC-002, GC-003 | GC-A / GC-C / GC-F domains; GC-003 §5 | GC-A-08; GC-C-04; GC-F-03; GC-F-04; Minor Non-Conformity #2 | EV-A-08; EV-C-04; EV-F-03; EV-F-04 | (no dedicated validation artifact exists — the gap itself) | (blank) |
| OI-007 | GC-001, GC-002, GC-003 | GC-A domain; GC-003 §5 | GC-A-10; Minor Non-Conformity #3 | EV-A-10 | `00_ARCHITECTURE/01_DOMAIN/ADW_01_CORE_DOMAIN_SEMANTICS.md` | (blank) |
| OI-008 | GC-002, GC-003 | §0 (Naming note); GC-003 §5 | Minor Non-Conformity #4 | EV-C-02 (Comments) | `50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md` (GC-002 proposal) | (blank) |
| OI-009 | GC-003 | §4.6; §5 | Minor Non-Conformity #5 | (none — see `REPOSITORY_RELEASE_REPORT.md`) | `50_IMPLEMENTATION/REPOSITORY_RELEASE_REPORT.md` (tag-push attempt) | (blank) |
| OI-010 | GC-002, GC-003 | GC-003 §5 | Observation #1 | EV-C-03 | root `GOVERNANCE_MODEL.md`; root `CAPABILITY_MAP_v1.0.md` | (blank) |
| OI-011 | GC-003 | §5 | Observation #2 | (none) | `06_PLAYBOOKS/`; root `PB0*.md` files | (blank) |
| OI-012 | GC-002, GC-003 | DECISION_0003 §8; GC-003 §5 | Observation #3 | EV-A-09 | `00_ARCHITECTURE/00_GOVERNANCE/DECISION_0002_AUTHORITY_HIERARCHY_AND_VOCABULARY_BASELINE.md` §3 (ADW-07, unwritten) | (blank) |

No item lacks an Originating Document. No item lacks an Originating
Section or Originating Finding. No reference above was invented; every
value is copied from an existing citation already present in GC-001,
GC-002, or GC-003.

---

## 5. Transition Assessment

This section summarizes the twelve Outstanding Items of §3 by category,
distinguishing what is accepted for Epoch IV consideration from what
instead requires a prior ADR, a prior Governance Decision, or ordinary
repository maintenance. No implementation scheduling is stated or
implied.

**Architecture items** (OI-001, OI-007, OI-012): concern an unapproved
architecture decision proposal and unwritten domain workshop (OI-001), an
undefined domain term (OI-007), and an unwritten domain workshop
(OI-012). OI-001 requires Architectural Review (an Architecture Change
Request per DECISION_0003 §11, since it concerns an as-yet-unapproved
proposal). OI-007 requires Architectural Review to add a formal
definition. OI-012 is accepted as a disclosed, non-blocking future item
pending its own domain workshop.

**Governance items** (OI-003): concerns a signature-role gap between the
Bizzi MVP's own governance model and the separate Art-of-Business
`GOVERNANCE_MODEL.md`. Requires a Governance Decision (a role-mapping
resolution) before GC-001 §8 can be executed as a real signature cycle.

**Engineering items**: none of the twelve items is classified Engineering
in isolation; OI-001's downstream effect (blocking nine of Gate D's ten
work packages) is an Engineering consequence but the item itself is
classified Architecture, per §2's rule that classification follows the
finding's domain of origin, not its downstream effect.

**Repository items** (OI-002, OI-004, OI-010, OI-011): OI-002 (orphan
citations) and OI-004 (PR #2 unmerged) are accepted for Epoch IV
consideration as repository-maintenance matters. OI-010 and OI-011 are
Art-of-Business-track observations, explicitly out of scope for the Bizzi
Platform MVP per DECISION_0002 §1, and are reserved rather than accepted
for Epoch IV.

**Documentation items** (OI-005, OI-006, OI-008, OI-009): OI-005
(missing supersession banner) and OI-009 (unpushed tag) are ordinary
repository maintenance, accepted for Epoch IV. OI-006 (no cross-reference
validation artifact) is accepted for Epoch IV consideration as a process
gap. OI-008 (naming collision) is reserved — its own source document
(GC-002) states that resolving it is outside scope, and this register
does not reopen that scope determination.

**Distinctions**:

- **Accepted for Epoch IV consideration**: OI-001, OI-002, OI-003,
  OI-004, OI-005, OI-006, OI-007, OI-009, OI-012.
- **Requires ADR / Architecture Change Request**: OI-001 (GC-001
  catalog-scope proposal), OI-007 (Aggregate definition) — both route
  through DECISION_0003 §11's Architecture Change Process, not through
  this register.
- **Requires Governance Decision**: OI-003 (signature-role mapping).
- **Repository Maintenance**: OI-004 (PR #2 merge), OI-005 (supersession
  banner), OI-009 (tag push), OI-002 (orphan-citation reconciliation).
- **Reserved (out of scope / not reopened by this register)**: OI-008
  (naming collision), OI-010, OI-011 (Art-of-Business track).

No item above is prioritized, sequenced, estimated, or assigned to a
sprint or work package by this register.

---

## 6. Repository Integrity Statement

Outstanding Items recorded in this register do **not** invalidate the
Gate C Certification. GC-003's Certification Recommendation —
**CONDITIONAL PASS** (GC-003 §9) — already accounted for all twelve
Outstanding Items listed in §3 at the time it was issued; none is a new
finding surfaced after certification, and none has been reclassified,
reweighed, or removed by this refinement.

The Gate C Certification outcome remains governed exclusively by:

- **GC-003** (`40_GATE_C/GC-003_CERTIFICATION_REPORT.md`) — the
  certification assessment and recommendation;
- **GC-004** (Gate C Approval) — not yet created;
- **GC-005** (Gate Closure) — not yet created.

This register has no authority over, and does not purport to modify, any
of the three.

---

## 7. Outstanding Item Lifecycle

This section governs how an Outstanding Item moves through its lifecycle
to formal closure.

**How items become Closed**: an Outstanding Item's Current Status changes
from `Open` (or `Accepted` / `Deferred` / `In Review`) to `Closed` only
when (a) one of the closure mechanisms recognized in §10 (Exit
Mechanisms) has actually occurred, (b) the resulting artifact is recorded
in that item's Closure Reference column (§3, §4), and (c) a Verification
Authority (§3) has confirmed the closure evidence satisfies the
originating finding. Closure is never inferred from the mere passage of
time, from an item being reclassified `Accepted` or `Deferred`, or from
this register's own narrative text.

**Who is authorized to close an item**: closure authority follows the
same Authority Hierarchy (DECISION_0002 §1) that governs the rest of the
constitutional record, not a new authority this register creates:

- An **Architecture**-classified item closes only upon action by the
  Project Owner (Tier 0), exercised through the Architecture Change
  Process (DECISION_0003 §11).
- A **Governance**-classified item closes only upon a Project Owner
  governance determination.
- A **Repository**, **Repository Hygiene**, **Branch Management**, or
  **Naming**-classified item closes upon action by the Repository
  Maintainer (the signature role GC-001 §8 already defines) or the
  Project Owner.
- A **Process** or **Documentation**-classified item closes upon action
  by Engineering Governance (EGC-01) or the Project Owner.
- An **Engineering**-classified item closes upon Engineering Governance
  confirmation that the underlying engineering work is complete and
  independently verified.

No AI system closes an Outstanding Item on its own initiative. Recording
a closure in this register, where the underlying authorization and
evidence already exist, is administrative implementation of an
already-authorized decision, consistent with EGC-01 §08 — it is not an
independent exercise of constitutional or governance authority.

**Acceptable closure evidence** (no other closure mechanism is
recognized):

- **ADR** — an Architecture Decision Record, following the Architecture
  Change Process (DECISION_0003 §11).
- **Decision** — a Project Owner Decision (in the sense of Decision
  0001 / DECISION_0002 / DECISION_0003).
- **Merge Commit** — a specific, identified commit SHA that merges the
  resolving change.
- **Approved Pull Request** — a specific, identified, merged pull
  request.
- **Repository Cleanup Commit** — a specific, identified commit SHA that
  performs a direct repository correction (e.g., applying a missing
  banner, pushing a tag).
- **Governance Approval** — a recorded approval by the Project Owner or
  Engineering Governance, where no ADR or Decision is the applicable
  instrument.

---

## 8. Acceptance of Residual Risk

Some Outstanding Items may, at the Project Owner's discretion, be
explicitly accepted as standing residual project risk rather than
remediated. This section defines the governance rules for that
acceptance. It assigns no current Outstanding Item to any of the
categories below — that determination, if made, is a future act by the
Project Owner, recorded at that time with its own Closure Reference or
explicit acceptance record.

Four distinct dispositions are recognized, and are not to be confused
with one another:

- **Accepted Risk** — the Project Owner has explicitly determined that an
  Outstanding Item will not be remediated and its underlying condition
  will persist indefinitely as a known, bounded risk. This requires an
  explicit, dated Project Owner statement naming the item and the risk
  accepted; silence or inaction does not constitute Accepted Risk.
- **Deferred Work** — the Outstanding Item is expected to be remediated,
  but not before a stated future point (e.g., a future Epoch or Gate);
  the item remains `Open` or moves to `Deferred` in §3, and is not
  treated as resolved.
- **Repository Maintenance** — the Outstanding Item requires only a
  direct, low-risk repository correction (per §7's Repository Cleanup
  Commit mechanism) and carries no governance or architectural
  significance beyond that correction.
- **Future Architecture Review** — the Outstanding Item requires
  architectural judgment not yet exercised, and is expected to be
  addressed through the Architecture Change Process (DECISION_0003 §11)
  at a future time, without a committed date.

An Outstanding Item may be assigned to at most one of these four
dispositions at any given time. Assignment does not, by itself, close
the item — closure still requires the mechanisms in §10.

---

## 9. Governance Rules

This register operates under the following explicit constraints, none of
which it has authority to waive for itself:

- This register **SHALL NOT** modify the Gate C Certification.
- This register **SHALL NOT** alter the Certification Decision.
- This register **SHALL NOT** authorize implementation.
- This register **SHALL NOT** replace an ADR, a Decision, or any other
  constitutional or governance instrument.
- This register **SHALL remain subordinate to**: GC-003 (Certification
  Assessment Report), GC-004 (Gate C Approval, not yet created), and
  GC-005 (Gate Closure, not yet created).

Where any statement elsewhere in this register appears to conflict with
GC-003, GC-004, or GC-005, the higher-authority document prevails, per
the Authority Hierarchy established by DECISION_0002 §1. This register
introduces no authority capable of overriding any of the three.

---

## 10. Exit Mechanisms

An Outstanding Item's Current Status changes to `Closed` only through one
of the following seven recognized mechanisms. Each mechanism SHALL
require a Closure Reference — a specific, identified artifact (a
document ID, ADR number, Decision number, commit SHA, or pull request
number) recorded in the item's Closure Reference field (§3, §4). No other
exit mechanism is recognized, and an item is never closed without a
recorded Closure Reference.

1. **Approved ADR** — an Architecture Decision Record resolves an
   architecture-classified item.
2. **Approved Decision** — a Project Owner Decision resolves the item.
3. **Repository Change** — a specific, identified commit or set of
   commits directly resolves the item's underlying repository condition.
4. **Repository Cleanup** — a specific, identified repository-hygiene
   correction (banner applied, tag pushed, duplicate reconciled) resolves
   the item.
5. **Engineering Completion** — the engineering work the item concerns is
   completed and independently verified by Engineering Governance.
6. **Governance Acceptance** — a recorded Governance Approval (§7)
   resolves a governance-classified item.
7. **Explicit Risk Acceptance** — the Project Owner explicitly accepts
   the item as Accepted Risk (§8), recorded with the accepting
   authority, the date, and the accepted-risk statement; this closes the
   item's active remediation lifecycle while preserving its historical
   record per §12.

---

## 11. Validation Rules

Before any Outstanding Item's Current Status may be changed to `Closed`,
the following SHALL be verified and recorded:

- ✓ Closure evidence exists — a specific artifact satisfying one of the
  seven mechanisms in §10.
- ✓ Closure authority exists — the acting authority matches §7's
  authorization rule for that item's Category.
- ✓ Closure reference recorded — the specific artifact identifier is
  entered in the item's Closure Reference field (§3, §4); no item is
  closed with a blank Closure Reference.
- ✓ Lifecycle complete — Date Opened, Date Closed, Verification
  Authority, and Verification Status are all populated for the item.
- ✓ Repository updated where applicable — where closure depends on a
  repository change (Repository Change, Repository Cleanup, Engineering
  Completion), that change is confirmed present in the repository before
  Current Status is changed.
- ✓ No duplicate Closure Reference — the artifact recorded as Closure
  Reference for one item is not already recorded as the Closure
  Reference for a different, unrelated item, unless a single artifact
  genuinely resolves multiple items (in which case each item's row
  states this explicitly).

An item failing any of the above checks remains `Open`, `Accepted`,
`Deferred`, or `In Review`, as applicable, until the failing condition is
corrected.

---

## 12. Repository Integrity

Outstanding Items exist to preserve audit integrity. They **SHALL never
be deleted** from this register, at any point in their lifecycle.

Closed items **SHALL remain in the register** for historical
traceability — a closed item's row is retained, with its Current Status
set to `Closed`, its Date Closed and Closure Reference populated, and
every other field left intact exactly as it stood before closure. A
closed item is never removed, and its row is never overwritten to appear
as though the underlying finding never existed.

This register therefore functions as a **permanent governance record**:
its purpose is not only to track what remains open today, but to
preserve, indefinitely, the complete history of every finding the Gate C
Certification process identified and how — if ever — each was
subsequently resolved, accepted, or otherwise closed.

---

## Repository Integrity Note

This revision (v1.1) was created without modifying GC-001, GC-002, or
GC-003, without creating GC-004 or GC-005, and without modifying any
other repository file. No finding was added, removed, reclassified, or
reprioritized. All twelve Outstanding Items (OI-001–OI-012), their
Categories, and their Audit Classifications are identical to v1.0; only
lifecycle-management structure — terminology, lifecycle columns,
expanded Decision values, the Outstanding Item Lifecycle section, the
Acceptance of Residual Risk section, expanded Governance Rules, expanded
Exit Mechanisms, Validation Rules, and this permanence statement — was
added.
