# Outstanding Items Register — Gate C Certification Transition

Document ID: OIR-01
Title: Gate C Outstanding Items Register
Version: 1.0
Status: OPEN REGISTER (informational; not a certification instrument)
Document Type: Traceability Register
Part of: Gate C Transition Record (companion to the Gate C Certification
Package — GC-001 Certification Checklist, GC-002 Evidence Register,
GC-003 Certification Assessment Report)
Repository: ArtheosClub/Bizzi_Project

This register is not a corrective action plan. This register is not a
backlog. This register is not an implementation roadmap. It exists
solely to preserve traceability between the Gate C Certification
Assessment and the unresolved observations and accepted future work that
may be considered after Gate C has been formally closed. Nothing in this
register modifies, reinterprets, or supersedes the certification outcome
recorded in GC-003.

---

## 1. Purpose

**Purpose**: to provide a single, authoritative record of every
unresolved finding identified during the Gate C Certification process
(GC-001, GC-002, GC-003), so that no observation, gap, or accepted
condition is lost, duplicated, or silently forgotten between Gate C
Certification and whatever review or planning activity follows it.

**Scope**: this register captures findings already recorded in GC-001
(the Certification Checklist), GC-002 (the Evidence Register), and GC-003
(the Certification Assessment Report). It introduces no new finding, no
new evidence, and no new architectural, governance, or engineering
content. Every item in §3 traces to an existing finding in one of those
three documents.

**Relationship to GC-003**: GC-003 issued the Gate C certification
recommendation — CONDITIONAL PASS, with five explicit conditions (GC-003
§9) — on the basis of 0 Critical, 4 Major, 5 Minor, and 3 Observation
non-conformities (GC-003 §5, Appendix — Assessment Statistics). This
register catalogues those same twelve non-conformities for transition
purposes. It does not re-evaluate, re-weigh, upgrade, or downgrade any of
them.

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

Every item in §3 is classified using exactly one of the following nine
categories. No additional category is introduced.

- **Architecture**
- **Governance**
- **Repository**
- **Engineering**
- **Documentation**
- **Process**
- **Naming**
- **Branch Management**
- **Repository Hygiene**

Classification reflects the domain of the underlying finding as recorded
in its source document (GC-001's GC-A through GC-F domains, per GC-001
§4), not a judgment about how the item should eventually be resolved.

---

## 3. Outstanding Items Register

Twelve items, corresponding exactly to the twelve non-conformities
recorded in GC-003 §5 (4 Major, 5 Minor, 3 Observations; 0 Critical). No
item below originates outside GC-001, GC-002, or GC-003.

| Item ID | Origin | Finding | Category | Classification | Current Status | Decision | Target Epoch | Owner | Notes |
|---|---|---|---|---|---|---|---|---|---|
| OI-001 | GC-003 §5 (Major #1); GC-002 EV-D-03, EV-A-09; GC-001 GC-A-09, GC-D-03 | The Provider/Model catalog-scope proposal (`GC-001` in `GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md`) remains unapproved, and ADW-05 (Agent/Provider/Model domain semantics) remains unwritten. Together these block `AgentDefinition`, `RuntimeSession`, and nine of Gate D's ten work packages. | Architecture | Major | Open | Architectural Review Required | Epoch IV | Project Owner | Already disclosed and accepted as a condition in `ENGINEERING_BASELINE.md` §9's Conditional Go and in GC-003 §9 Condition 1. Not a newly discovered gap. |
| OI-002 | GC-003 §5 (Major #2); GC-002 EV-C-08 | Seven Document IDs (ARR-01, AGR-01, ARC-01, CR-01, CR-02, EAR-01, GMR-01), cited within `ABR-01_ARCHITECTURE_BASELINE_RESOLUTION.md` and `EGC-01_ENGINEERING_GOVERNANCE_CHARTER.md`, correspond to no committed file in the repository. | Repository | Major | Open | Resolve Later | Epoch IV | Project Owner | Limits independent auditability of the historical governance record (GC-003 §4.3, R-2). GC-003 §9 Condition 2 records this as an accepted, disclosed traceability gap. |
| OI-003 | GC-003 §5 (Major #3); GC-002 EV-B-08; GC-001 GC-B-08, §8 note | Three of GC-001 §8's five requested certification signature roles ("Architecture Review Board," "Chief Architect," "Chief Orchestrator") are Art-of-Business roles (`01_GOVERNANCE/GOVERNANCE_MODEL.md`) with no defined equivalent in the Bizzi Platform MVP's own governance model. | Governance | Major | Open | Governance Review Required | Epoch IV | Project Owner | GC-001 §8 already identifies de facto substitute authorities (Project Owner; Engineering Governance/EGC-01) without inventing a new role. GC-003 §9 Condition 3: must be resolved before GC-001 §8 is actually executed for a signature cycle. |
| OI-004 | GC-003 §5 (Major #4); GC-003 §4.6; `REPOSITORY_RELEASE_REPORT.md` (PR Review) | Pull Request #2 (`claude/gate-c-platform-backbone`) remains open; five of its files (real, non-conflicting documentation reconciliation) are not yet merged into `main`. | Branch Management | Major | Open | Repository Cleanup | Epoch IV | Project Owner | File-by-file resolution already identified in `REPOSITORY_RELEASE_REPORT.md`. GC-003 §9 Condition 4. |
| OI-005 | GC-003 §5 (Minor #1); GC-002 EV-C-05b, EV-F-07b; GC-001 GC-C-05, GC-F-07 | `docs/planning/WORK_PACKAGES.md` lacks a physical supersession banner at the file level, despite `CLAUDE.md`'s Key Entry Points table already asserting that status. | Repository Hygiene | Minor | Open | Repository Cleanup | Epoch IV | Project Owner | Also recorded as a Repository Risk in `REPOSITORY_RELEASE_REPORT.md`. GC-003 §9 Condition 5. |
| OI-006 | GC-003 §5 (Minor #2); GC-002 EV-A-08, EV-C-04, EV-F-03, EV-F-04; GC-001 GC-A-08, GC-C-04, GC-F-03, GC-F-04 | No dedicated cross-reference/link-validation artifact exists in the repository. Four separate GC-001 requirements share this one underlying gap. No specific broken reference has been demonstrated by any evidence reviewed. | Process | Minor | Open | Resolve Later | Epoch IV | Project Owner | GC-002 §6 records this as one gap recorded once, applying to all four requirement IDs, rather than four independent gaps. |
| OI-007 | GC-003 §5 (Minor #3); GC-002 EV-A-10; GC-001 GC-A-10 | `Aggregate` (D08, Aggregate Strategy) has no standalone formal definition within `ADW_01_CORE_DOMAIN_SEMANTICS.md`. | Architecture | Minor | Open | Architectural Review Required | Epoch IV | Project Owner | Per GC-003 §4.1, does not block currently-unblocked work packages. |
| OI-008 | GC-003 §5 (Minor #4); GC-002 §0 (Naming note), EV-C-02 (Comments) | This Gate C Certification Package's own document ID, `GC-002`, collides in form with the pre-existing, unrelated, unapproved `GC-002` Architecture Decision Proposal ("Composite Foreign Keys") in `GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md`. | Naming | Minor | Open | Reserved | Not applicable | Project Owner | GC-002's own header states resolving the collision is outside that document's scope. This register does not resolve it either. |
| OI-009 | GC-003 §5 (Minor #5); GC-003 §4.6; `REPOSITORY_RELEASE_REPORT.md` (tag-push attempt) | The `implementation-baseline-v1.0` release tag exists as a local annotated tag object but was not successfully pushed to the remote (outbound proxy returned `HTTP 403` on every attempt). | Repository Hygiene | Minor | Open | Repository Cleanup | Epoch IV | Project Owner | Local tag object correctly points at merge commit `576465f15d8e35656ad8ff3f6ed5e954ebb74fe8`; ready to push once the underlying access constraint is resolved. |
| OI-010 | GC-003 §5 (Observation #1); RSM-01 §08 (Namespace Analysis); GC-002 EV-C-03 | Root-level `GOVERNANCE_MODEL.md` and `CAPABILITY_MAP_v1.0.md` exist as content-divergent duplicates. | Repository | Observation | Open | Reserved | Not applicable | Project Owner | Art-of-Business track; explicitly outside Gate C Certification scope per DECISION_0002 §1 and GC-003 §2. |
| OI-011 | GC-003 §5 (Observation #2); RSM-01 §08 | `06_PLAYBOOKS/` remains empty while 102 `PB0*.md` files sit at repository root. | Repository | Observation | Open | Reserved | Not applicable | Project Owner | Art-of-Business track; explicitly outside Gate C Certification scope, same basis as OI-010. |
| OI-012 | GC-003 §5 (Observation #3); GC-002 EV-A-09; DECISION_0003 §8 | ADW-07 (Events, Audit, and Provenance domain semantics) remains unwritten. | Architecture | Observation | Open | Resolve Later | Epoch IV | Project Owner | Per GC-003 §5 Observation #3, not currently blocking any Gate C work package; DECISION_0002's Vocabulary Baseline provisionally governs the affected relationships. Also recorded as a Remaining Open Area in DECISION_0003 §8. |

---

## 4. Traceability

Every item in §3 references, in its Origin column, at minimum: the
source document (GC-001, GC-002, or GC-003), the section or finding ID
within that document, and — where GC-002 assigns one — the Evidence ID.
Every item's Notes column identifies the related repository artifact
where one exists. No identifier in this register was invented; every
Item ID (`OI-001` through `OI-012`) is a new, purely sequential label
assigned only to this register for internal reference and does not
purport to be, or replace, any GC-001/GC-002/GC-003 identifier.

Cross-reference summary:

| Item ID | Source Document | Source Section / ID | Related Repository Artifact |
|---|---|---|---|
| OI-001 | GC-001, GC-002, GC-003 | GC-A-09 / GC-D-03; EV-A-09 / EV-D-03; §5 Major #1 | `GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md` (GC-001 proposal); `00_ARCHITECTURE/01_DOMAIN/` (ADW-05, unwritten) |
| OI-002 | GC-002, GC-003 | EV-C-08; §5 Major #2 | `ABR-01_ARCHITECTURE_BASELINE_RESOLUTION.md`; `EGC-01_ENGINEERING_GOVERNANCE_CHARTER.md` |
| OI-003 | GC-001, GC-002, GC-003 | GC-B-08, §8; EV-B-08; §5 Major #3 | `40_GATE_C/GC-001_GATE_C_CHECKLIST.md` §8 |
| OI-004 | GC-003 | §4.6, §5 Major #4 | `50_IMPLEMENTATION/REPOSITORY_RELEASE_REPORT.md` (PR Review table) |
| OI-005 | GC-001, GC-002, GC-003 | GC-C-05 / GC-F-07; EV-C-05b / EV-F-07b; §5 Minor #1 | `docs/planning/WORK_PACKAGES.md` |
| OI-006 | GC-001, GC-002, GC-003 | GC-A-08 / GC-C-04 / GC-F-03 / GC-F-04; EV-A-08 / EV-C-04 / EV-F-03 / EV-F-04; §5 Minor #2 | (no dedicated validation artifact exists — the gap itself) |
| OI-007 | GC-001, GC-002, GC-003 | GC-A-10; EV-A-10; §5 Minor #3 | `00_ARCHITECTURE/01_DOMAIN/ADW_01_CORE_DOMAIN_SEMANTICS.md` |
| OI-008 | GC-002, GC-003 | §0 (Naming note); §5 Minor #4 | `50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md` (GC-002 proposal) |
| OI-009 | GC-003 | §4.6, §5 Minor #5 | `50_IMPLEMENTATION/REPOSITORY_RELEASE_REPORT.md` (tag-push attempt) |
| OI-010 | GC-002, GC-003 | EV-C-03; §5 Observation #1 | root `GOVERNANCE_MODEL.md`; root `CAPABILITY_MAP_v1.0.md` |
| OI-011 | GC-003 | §5 Observation #2 | `06_PLAYBOOKS/`; root `PB0*.md` files |
| OI-012 | GC-002, GC-003 | EV-A-09; §5 Observation #3 | `00_ARCHITECTURE/00_GOVERNANCE/DECISION_0002_AUTHORITY_HIERARCHY_AND_VOCABULARY_BASELINE.md` §3 (ADW-07, unwritten) |

No item lacks a source document. No item lacks a section or finding
reference. No identifier was invented beyond this register's own
sequential Item IDs.

---

## 5. Transition Assessment

This section summarizes the twelve items of §3 by category, distinguishing
what is accepted for Epoch IV consideration from what instead requires a
prior ADR, a prior Governance Decision, or ordinary repository
maintenance. No implementation scheduling is stated or implied.

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
**CONDITIONAL PASS** (GC-003 §9) — already accounted for all twelve items
listed in §3 at the time it was issued; none is a new finding surfaced
after certification.

Outstanding Items SHALL remain **Open** in this register until formally
resolved through one of the mechanisms in §7, or explicitly accepted as a
standing condition by the Project Owner. This register's own recording of
an item does not, by itself, resolve, close, or accept it.

The Gate C Certification outcome remains governed exclusively by:

- **GC-003** (`40_GATE_C/GC-003_CERTIFICATION_REPORT.md`) — the
  certification assessment and recommendation;
- **GC-004** (Gate C Approval) — not yet created;
- **GC-005** (Gate Closure) — not yet created.

This register has no authority over, and does not purport to modify, any
of the three.

---

## 7. Exit Criteria

An item leaves this register (its Current Status changes from `Open` to
`Closed`) only through one of the following mechanisms. No other exit
mechanism is recognized.

- **Repository cleanup** — the underlying repository artifact is
  corrected directly (e.g., a missing banner is applied, a tag is
  pushed, a pull request is merged), verified, and recorded.
- **Approved ADR** — an Architecture Decision Record, following the
  Architecture Change Process (DECISION_0003 §11), resolves an
  architecture-classified item.
- **Approved Decision** — a Project Owner Decision (in the sense of
  Decision 0001 / DECISION_0002 / DECISION_0003) resolves the item.
- **Governance approval** — a governance instrument (in the sense of
  ABR-01, EGC-01, or AI-01) resolves a governance-classified item.
- **Implementation completion** — the engineering work the item concerns
  is completed and independently verified (applicable only where an item
  is downstream of an engineering deliverable, not to this register's own
  Architecture/Governance-classified items).
- **Explicit acceptance** — the Project Owner explicitly accepts the item
  as a standing, permanent condition rather than a defect to be resolved,
  recorded in this register with the accepting authority and date.

An item's Current Status may also move from `Open` to `Deferred` or
`Accepted` without leaving the register, per the Status values defined in
§3's column definitions, where a decision has been made about the item's
disposition but the exit mechanism above has not yet been executed.

---

## Repository Integrity Note

This register was created without modifying GC-001, GC-002, or GC-003,
without creating GC-004 or GC-005, and without modifying any other
repository file. Every item in §3 traces to an existing, previously
recorded finding; no new finding was introduced during this register's
creation.
