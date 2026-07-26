# Engineering Baseline — Bizzi Platform

Version: 1.0
Status: Active
Repository: ArtheosClub/Bizzi_Project
Baseline branch: `agent/architecture-specification-v1-1`

This document freezes the exact repository state from which
implementation begins. It verifies, summarizes, and normalizes what
already exists; it invents nothing, redesigns nothing, and modifies no
approved document. Everything after this baseline belongs to
implementation, not architecture.

---

## 1. Executive Summary

**Repository maturity**: high for architecture and governance, low for
product code. The constitutional and domain-semantics work (Decision
0001, DECISION_0002, ADW-01/D01–D10, ABR-01, EGC-01, AI-01) is complete
and active. The implementation-planning work (work package plan,
backlog, sequence, milestones, checklist) is complete. The actual
codebase is a Gate B skeleton only — no domain model has been written.

**Architecture maturity**: Frozen. The Architecture Baseline is `ACTIVE`
(ABR-01) and the Architecture Freeze (Decision 0001) is in force.

**Engineering maturity**: Partial. Ten Gate C engineering proposals
(GC-001–GC-010) remain unapproved; two planned domain workshops (ADW-05,
ADW-07) remain unwritten; one domain term (`Aggregate`, D08) remains
undefined.

**Implementation readiness**: Partial, and unevenly distributed. Six of
ten Gate C work packages (plus the newly-identified `WP12a`) are
unblocked today; the remainder of Gate C and effectively all of Gate D
are gated behind a single root cause (GC-001 approval + ADW-05).

**Suitability for Sprint 0**: **Conditional.** The content is ready.
One structural condition — stated plainly in §9 — must be resolved
first: the entire baseline described in this document exists only on
`agent/architecture-specification-v1-1`, not on `main`.

---

## 2. Baseline Scope

**Included**: constitutional governance (Decision 0001 → AI-01);
domain semantics (ADW-01, D01–D10); the Authority Hierarchy and
Vocabulary Baseline (DECISION_0002); accepted ADRs (0001, 0003–0007);
C4 diagrams; the MVP Work Package Plan and the four Implementation
documents (Backlog, Sequence, Milestones, Checklist); the Gate B
codebase as it exists today.

**Not Included**: any code beyond the Gate B skeleton; any Gate C
domain model; any resolution of GC-001–GC-010.

**Deferred**: ADW-05 (Agent/Provider/Model), ADW-07 (Events, Audit,
Provenance), the `Aggregate` term definition (D08), the Business
Operation documentation sync (DECISION_0002 Vocabulary Baseline, still
open), Gate E (WP33–WP39).

**Out of Scope**: the "Art of Business" platform-wide vision
(`01_GOVERNANCE/GOVERNANCE_MODEL.md`, `AUTHORITY_MATRIX.md`,
`02_CAPABILITY_MAP` … `33_BACKEND_SOURCE_CODE_IMPLEMENTATION`) — a
separate system, per DECISION_0002 §1, not binding on this baseline
except through adaptation.

---

## 3. Authoritative Documents

No document appears in more than one category. Where a document exists
but is not yet approved or not yet binding, it is listed with that
status rather than omitted.

**Architecture**
- `00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md`
- `00_ARCHITECTURE/00_FOUNDATION/DOMAIN_FOUNDATION.md`

**Governance**
- `00_ARCHITECTURE/00_GOVERNANCE/DECISION_0001_MVP_FIRST.md` — `APPROVED`
- `00_ARCHITECTURE/00_GOVERNANCE/DECISION_0002_AUTHORITY_HIERARCHY_AND_VOCABULARY_BASELINE.md` — `APPROVED`
- `00_ARCHITECTURE/00_GOVERNANCE/ABR-01_ARCHITECTURE_BASELINE_RESOLUTION.md` — `ACTIVE`
- `01_GOVERNANCE/EGC-01_ENGINEERING_GOVERNANCE_CHARTER.md` — `ACTIVE`
- `00_CONSTITUTION/AI-01_AUTHORITATIVE_INTERPRETATION.md` — `ACTIVE`

**Domain**
- `00_ARCHITECTURE/01_DOMAIN/ADW_01_CORE_DOMAIN_SEMANTICS.md`
- `00_ARCHITECTURE/01_DOMAIN/ADW_01_DECISION_REGISTER.md` (D01–D10, all `APPROVED` or `APPROVED — CLOSED`)
- `00_ARCHITECTURE/01_DOMAIN/D07_STATE_SEMANTICS.md`, `D09_RELATIONSHIP_MODEL.md`, `D10_DELETION_AND_SUPERSESSION.md` (dedicated deep-dive files)

**ADR**
- Accepted: `0001-record-architecture-decisions.md`, `0003-controller-service-repository-layering.md`, `0004-workspace-scoped-multi-tenancy.md`, `0005-audit-first-mutations.md`, `0006-authorization-model-mvp.md`, `0007-bizzi-mvp-backend-stack-python-fastapi.md`
- Superseded (historical only): `0002-bizzi-mvp-backend-stack-scope.md` (by 0007)
- Template, not itself authoritative content: `0000-adr-template.md`

**Implementation**
- `50_IMPLEMENTATION/MVP_WORK_PACKAGE_PLAN.md`
- `50_IMPLEMENTATION/IMPLEMENTATION_BACKLOG.md`, `IMPLEMENTATION_SEQUENCE.md`, `IMPLEMENTATION_MILESTONES.md`, `IMPLEMENTATION_CHECKLIST.md`
- `50_IMPLEMENTATION/GATE_A/` (WP00–WP04, `GATE_A_REVIEW_AND_APPROVAL.md`)
- `50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md` — **proposals only; GC-001–GC-010 are not yet approved and are not authoritative**

**Reference**
- `06_REFERENCE/RKM-01_REPOSITORY_KNOWLEDGE_MODEL.md` — **DRAFT, not approved for generation; descriptive, not binding**
- `06_REFERENCE/RSM-01_REPOSITORY_STRUCTURE_MODEL.md` — **DRAFT, same status**

**Planning**
- `docs/planning/DEVELOPMENT_PLAN.md`
- `docs/planning/PRE-CODING-BRIEF.md`
- `docs/planning/TECH_STACK.md`
- Historical only: `docs/planning/WORK_PACKAGES.md` (superseded by `MVP_WORK_PACKAGE_PLAN.md`)

**Review**
- No committed file exists for ARR-01, AGR-01, ARC-01, CR-01, CR-02, EAR-01, or GMR-01. Each was conducted and its conclusions were incorporated into the documents above (ABR-01 and EGC-01 both cite them by name in their Traceability/Constitutional Findings sections), but the review outputs themselves were never persisted as repository files. This is recorded here, not resolved — see §7.

---

## 4. Repository State

**Structure**: two tracks share this repository, per `CLAUDE.md` — a
largely-Russian "Art of Business" enterprise specification
(`00_RELEASE`…`50_IMPLEMENTATION` numbered directories, excluding the
MVP-specific subset below) and the Bizzi Platform MVP backend build
(`00_ARCHITECTURE/`, `00_CONSTITUTION/`, the `01_GOVERNANCE/EGC-01`
file specifically, `docs/`, `backend/`, and the MVP-relevant contents of
`50_IMPLEMENTATION/`).

**Major folders** (MVP-relevant): `00_ARCHITECTURE/` (constitution +
domain semantics), `00_CONSTITUTION/` (AI-01), `01_GOVERNANCE/` (EGC-01,
alongside the separate Art-of-Business governance files), `06_REFERENCE/`
(RKM-01, RSM-01), `50_IMPLEMENTATION/` (work-package plan, four
implementation documents, Gate A/Gate C packages), `docs/adr/`,
`docs/c4/`, `docs/planning/`, `backend/`.

**Documentation structure**: consistent within the MVP track — every
constitutional/architecture document carries Version, Status, and
Related Documents fields; every ADR follows the Nygard template.

**Implementation structure**: `backend/app/` follows the CSR layering
declared in ADR-0003 (`api/`, `core/`, `db/`) but currently contains only
infrastructure — no `models/`, `repositories/`, or `services/` directory
exists yet, because no domain entity has been built.

**Current code status**: Gate B complete — FastAPI app (`app.main`),
health endpoint, typed settings, structured JSON logging, SQLAlchemy
engine/session (not wired to any route), Alembic with one intentionally
empty baseline migration. `backend/app/db/base.py` is an empty
`DeclarativeBase`, by design, verified directly: zero domain tables
exist.

**Infrastructure status**: Docker Compose for local Postgres; `.env`
examples for dev/test/prod separation; entrypoint script. No deployment
infrastructure beyond local/dev exists yet — out of scope for this
baseline.

**Testing status**: one test file, `backend/tests/test_health.py`, plus
`conftest.py`. No domain tests exist because no domain code exists.

**CI status**: `.github/workflows/backend-ci.yml` exists, correctly
scoped to trigger only on `backend/**` and its own path, running on PRs
and on push to `main`. It currently has nothing but the health endpoint
to exercise.

**Branch state**: `main` is 54 commits behind
`agent/architecture-specification-v1-1`, with zero divergence (a clean
fast-forward relationship, not a conflicting one). `main` contains Gate
B's code and the Gate A documentation package (merged via PR #3), but
**does not contain** `00_ARCHITECTURE/`, `00_CONSTITUTION/`, EGC-01,
`06_REFERENCE/`, or the four Implementation documents. `main` also still
contains `TEST_WRITE.md`/`CONNECTOR_TEST.md`, deleted on the feature
branch (RTC-01) but not yet merged forward.

---

## 5. Engineering Readiness

**Architecture Freeze**: in force. Decision 0001 established it;
ABR-01 (`ACTIVE`) confirmed it operationally.

**Implementation Backlog / Sequence / Milestones / Checklist**: all four
exist (`50_IMPLEMENTATION/IMPLEMENTATION_*.md`), covering WP12a and
WP13–WP32.

**Critical Path**: WP12a → WP13 → WP14 (blocked) → … . Nine of Gate D's
ten work packages (WP24–WP32) trace to one root cause: GC-001 approval
and ADW-05 completion. Five to six Gate C work packages (WP12a, WP13,
WP15, WP16, WP18, WP20, and the human-role half of WP17) are unblocked
independent of that root cause.

**Current blockers**: GC-001 (Provider/Model catalog scope) and ADW-05
(Agent/Provider/Model domain semantics, unwritten) — both Critical Path.
GC-002, GC-003, GC-004, GC-005, GC-006, GC-007, GC-008, GC-009, GC-010
are open but non-blocking, each with a documented safe interim default.

**Current approvals**: none of GC-001–GC-010 is approved. D01–D10,
Decision 0001, DECISION_0002, ABR-01, EGC-01, and AI-01 are all approved
and active.

**Current implementation-ready work packages**: WP12a, WP13, WP15,
WP16, WP18, WP20, WP22, and the human-role portion of WP17 — per
`IMPLEMENTATION_BACKLOG.md`.

---

## 6. Baseline Decisions (Frozen)

- **Technology stack**: Python 3.13.14, FastAPI, PostgreSQL 18.4, SQLAlchemy + Alembic, `uv` — ADR-0007 (supersedes ADR-0002).
- **Repository/service layering**: strict Controller(Router)→Service→Repository, one-directional — ADR-0003.
- **Multi-tenancy pattern**: `workspace_id` as a required, indexed flat field on every Gate C entity, with the documented `WorkspaceMembership` join-entity exception for Identity — ADR-0004.
- **Audit pattern**: business write + audit write atomic for high-impact mutations; `workspace_id` inherited by the repository layer, never set independently — ADR-0005.
- **Authorization model (MVP)**: owner-only checks, RBAC-ready shape — ADR-0006.
- **ADR governance process itself**: ADR-0001.
- **Domain semantics**: D01–D10 (Workspace as Primary Boundary, EnterpriseObject, Work Model, Task/Execution split, Actor Model, Decision/Business Operation, State Constitution, Aggregate Strategy, Relationship Model, Deletion/Supersession).
- **Authority Hierarchy and Vocabulary Baseline**: DECISION_0002.
- **Architecture Baseline activation**: ABR-01.
- **Engineering Governance Charter**: EGC-01.
- **Branch strategy**: **not yet formally documented anywhere in the repository.** Recorded here as a gap (§7), not invented.

---

## 7. Known Open Items

**Approval Gaps**
- GC-001 through GC-010 — all unapproved (`50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md`).

**Modeling Gaps**
- ADW-05 (Agent/Provider/Model domain semantics) — not written.
- ADW-07 (Events, Audit, and Provenance domain semantics) — not written; `Event`/`AuditRecord` relationship semantics are only provisionally governed by GC-002 in the interim.

**Engineering Gaps**
- Branch strategy undocumented.
- `WP12a` (Workspace) exists only in `IMPLEMENTATION_BACKLOG.md`, not in the canonical `MVP_WORK_PACKAGE_PLAN.md` itself.

**Documentation Gaps**
- `Aggregate` (D08) remains formally undefined (ARR-01's R5 finding, never closed).
- Business Operation's absence from `PRE-CODING-BRIEF.md` — flagged by DECISION_0002's Vocabulary Baseline as "documentation update required," still open.
- The review-process documents (ARR-01, AGR-01, ARC-01, CR-01, CR-02, EAR-01, GMR-01) are cited by name in committed documents but were never themselves committed as files (§3).
- Root-level `GOVERNANCE_MODEL.md` and `CAPABILITY_MAP_v1.0.md` each exist as content-divergent duplicates of their `01_GOVERNANCE/`/`02_CAPABILITY_MAP/` counterparts (RSM-01 §08, unresolved).

**Operational Gaps**
- **`agent/architecture-specification-v1-1` is not merged to `main`.** Every constitutional, domain, and implementation-planning document in §3 exists only on this branch.
- `06_PLAYBOOKS/` is empty; 102 `PB0*.md` files sit loose at repository root instead (RSM-01 §08, unresolved).
- `06_PLAYBOOKS` and `06_REFERENCE` share the same numeric prefix (RSM-01, unresolved).
- `TEST_WRITE.md`/`CONNECTOR_TEST.md` were removed on the feature branch (RTC-01) but still exist on `main`.

---

## 8. Readiness Matrix

| Area | Status | Notes |
|---|---|---|
| Architecture | READY | Frozen; ABR-01 `ACTIVE`. |
| Governance | READY | DECISION_0002, EGC-01 `ACTIVE`; AI-01 resolves the one open interpretation question found. |
| Domain | PARTIALLY READY | D01–D10 approved; `Aggregate` undefined; ADW-05/ADW-07 unwritten. |
| Planning | PARTIALLY READY | Work-package plan and four Implementation documents complete; Business Operation doc sync still open. |
| Implementation | PARTIALLY READY | ~6 of 10 Gate C WPs unblocked; Gate D almost entirely gated on GC-001/ADW-05. |
| Infrastructure | READY | Gate B complete: API, DB, migrations, config, logging, Docker Compose. |
| Codebase | PARTIALLY READY | Skeleton only; zero domain models — expected at this stage, not a defect. |
| Testing | PARTIALLY READY | Framework and health-check coverage exist; no domain coverage possible yet. |
| Delivery | PARTIALLY READY | CI correctly scoped; branch strategy undocumented. |
| Operations | BLOCKED | The baseline described in this document does not exist on `main`. |

---

## 9. Go / No-Go Assessment

**Can Sprint 0 begin? Conditional.**

The content is ready: six to seven work packages have no open dependency
and a fully specified engineering checklist. The blocking conditions are
structural, not architectural:

1. **Branch location must be resolved first.** This baseline exists only
   on `agent/architecture-specification-v1-1`. Before Sprint 0 work is
   assigned, there must be an explicit decision — merge this branch to
   `main`, or explicitly designate it as the working base for Sprint 0 —
   because "the repository" cannot mean two different things to two
   different engineers starting at the same time.
2. **GC-001 and ADW-05 gate the majority of Gate D**, though not Gate C's
   unblocked work packages (§5). Sprint 0 can proceed on those without
   waiting for this condition, but Gate D cannot.

With condition 1 resolved, Sprint 0 can begin immediately against
WP12a, WP13, WP15, WP16, WP18, WP20, WP22, and the human-role half of
WP17, in parallel with resolving condition 2.

---

## 10. Baseline Declaration

This document establishes Engineering Baseline v1.0 for the Bizzi
Platform.

All architectural work preceding this baseline is considered frozen
unless modified through the formal Architecture Governance process
established by DECISION_0002 and ABR-01.

All future implementation work shall reference this baseline.

This baseline is recorded as it exists on `agent/architecture-specification-v1-1`
at the time of writing. It does not itself resolve the branch-location
condition in §9 — that decision belongs to the Project Owner, not to
this document.
