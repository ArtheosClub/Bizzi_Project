# ABR-01 — Architecture Baseline Resolution

## 00. Document Control

| Field | Value |
|---|---|
| Document ID | ABR-01 |
| Title | Architecture Baseline Resolution |
| Version | 1.0 |
| Status | **DRAFT — Awaiting Project Owner Signature** |
| Effective Date | Not yet effective — becomes effective upon Project Owner signature (§09) |
| Repository | ArtheosClub/Bizzi_Project |
| Authority | Project Owner (Tier 0, per `DECISION_0002_AUTHORITY_HIERARCHY_AND_VOCABULARY_BASELINE.md` §1) |
| Owner | Project Owner |
| Supersedes | None |
| Related Documents | `00_ARCHITECTURE/00_GOVERNANCE/DECISION_0001_MVP_FIRST.md`; `00_ARCHITECTURE/00_GOVERNANCE/DECISION_0002_AUTHORITY_HIERARCHY_AND_VOCABULARY_BASELINE.md`; `00_ARCHITECTURE/01_DOMAIN/ADW_01_DECISION_REGISTER.md`; `00_ARCHITECTURE/01_DOMAIN/ADW_01_CORE_DOMAIN_SEMANTICS.md`; `00_ARCHITECTURE/00_FOUNDATION/DOMAIN_FOUNDATION.md`; `00_ARCHITECTURE/ARCHITECTURE_SPECIFICATION.md`; `CLAUDE.md`; `50_IMPLEMENTATION/GATE_A/WP02_FIRST_BUSINESS_SCENARIO.md`; `50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md` |

---

## 01. Purpose

This Resolution formally establishes the Architecture Baseline for the
Bizzi Platform MVP backend build. It records, and does not create, the
constitutional facts established through the completed governance process
identified in §02 and §03. Upon Project Owner signature (§09), this
Resolution brings the Architecture Baseline and the Architecture Freeze
into constitutional force for this repository, under the Authority
Hierarchy established by DECISION_0002.

---

## 02. Constitutional Findings

- ADW-01 (Architecture Decision Workshop 01 — Core Domain Semantics) is complete.
- D01–D10 are approved, per `00_ARCHITECTURE/01_DOMAIN/ADW_01_DECISION_REGISTER.md`.
- The ADW-01 Decision Register is complete.
- Decision 0001 (MVP First & Architecture Freeze) is approved.
- DECISION_0002 (Authority Hierarchy and Vocabulary Baseline) is approved.
- The Authority Hierarchy is approved, per DECISION_0002 §1.
- The Canonical Vocabulary Baseline is approved, per DECISION_0002 §3.
- ARR-01 (Architecture Readiness Review) is complete.
- AGR-01 (Architecture Governance Reconciliation) is complete.
- Governance Execution (Steps 1–8) is complete.
- ARC-01 (Architecture Readiness Certification) has certified the repository ready for Architecture Baseline Resolution.

---

## 03. Repository Findings

- Architecture documents are synchronized: `ADW_01_CORE_DOMAIN_SEMANTICS.md`, `DOMAIN_FOUNDATION.md`, `ARCHITECTURE_SPECIFICATION.md`.
- Governance documents are synchronized: `CLAUDE.md`.
- Repository synchronization is complete: `50_IMPLEMENTATION/GATE_A/WP02_FIRST_BUSINESS_SCENARIO.md`, `50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md`.
- Cross-document consistency is verified, per ARC-01.
- The architecture authority hierarchy is established, per DECISION_0002 and `ARCHITECTURE_SPECIFICATION.md` §3.
- The repository is ready for Architecture Baseline activation, per ARC-01's certification decision.

---

## 04. Architecture Baseline Resolution

Therefore, the Project Owner resolves that:

1. ADW-01 is adopted as the official Architecture Baseline for the Bizzi Platform MVP backend build.
2. D01–D10, as recorded in `00_ARCHITECTURE/01_DOMAIN/ADW_01_DECISION_REGISTER.md`, constitute the official Core Domain Semantics.
3. Decision 0001 remains authoritative.
4. DECISION_0002 remains binding.
5. The Authority Hierarchy established by DECISION_0002 §1 becomes binding.
6. The Canonical Vocabulary Baseline established by DECISION_0002 §3 becomes binding.
7. The Architecture Freeze established by Decision 0001 enters into force.
8. Engineering documents derive their authority from the Architecture Baseline.
9. Planning documents derive their authority from the Architecture Baseline.
10. Future semantic changes to Core Domain Semantics require Architecture Governance, exercised through the Project Owner under the Authority Hierarchy.
11. Historical documents remain evidentiary but never override a higher-authority document.
12. Deferred work, including the matters listed in §06, remains deferred.
13. Gate C proposals (`50_IMPLEMENTATION/GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md`, GC-001–GC-010) remain proposals unless separately approved by the Project Owner.

---

## 05. Authority Consequences

The following is a summary view of the Authority Hierarchy. It does not
redefine the hierarchy; the binding definition, including each tier's
full "Authoritative for" scope, is DECISION_0002 §1.

- **Tier 0** — Any explicit Project Owner decision record.
- **Tier 1** — Decision 0001.
- **Tier 2** — `00_ARCHITECTURE/` (`ARCHITECTURE_SPECIFICATION.md`, `DOMAIN_FOUNDATION.md`, D01–D10, the Decision Register).
- **Tier 3** — `docs/adr/*`.
- **Informational documents** — `docs/planning/`, `50_IMPLEMENTATION/`, `docs/c4/*`, `01_GOVERNANCE/GOVERNANCE_MODEL.md`, `AUTHORITY_MATRIX.md`, `CLAUDE.md`.
- **Engineering documents** — `backend/` (code).
- **Historical records** — superseded ADR-0002, `docs/planning/WORK_PACKAGES.md`, original Phase 0–3 `DEVELOPMENT_PLAN.md` text.

---

## 06. Explicit Non-Approvals

This Resolution does not approve:

- GC-001–GC-010.
- Gate C PASS.
- Engineering implementation.
- ADW-02.
- Any future ADR.
- Any future Workshop.
- Deferred audit ownership.
- Deferred retention decisions.
- Any future semantic change.

---

## 07. Effective State

Prior to Project Owner signature, this Resolution is DRAFT and none of
the following is in force. Upon Project Owner signature (§09):

- **Architecture Baseline** — ACTIVE.
- **Architecture Freeze** — IN FORCE.
- **Core Domain Semantics (D01–D10)** — BINDING.
- **Authority Hierarchy** — BINDING, per DECISION_0002 §1.
- **Vocabulary Baseline** — BINDING, per DECISION_0002 §3.
- **Repository State** — SYNCHRONIZED, per ARC-01.

---

## 08. Traceability

| Phase | Authoritative Evidence | Result |
|---|---|---|
| ADW | `00_ARCHITECTURE/01_DOMAIN/ADW_01_CORE_DOMAIN_SEMANTICS.md`, `ADW_01_DECISION_REGISTER.md` | D01–D10 approved |
| ARR | ARR-01 (Architecture Readiness Review) | Findings identified; resolution routed to Governance Execution |
| AGR | AGR-01 (Architecture Governance Reconciliation) | Governance Execution Plan produced |
| Execution | Governance Execution Steps 1–8 (`agent/architecture-specification-v1-1`) | Repository synchronized |
| ARC | ARC-01 (Architecture Readiness Certification) | Repository CERTIFIED READY for Architecture Baseline Resolution |
| ABR | This Resolution (ABR-01) | Architecture Baseline established, subject to §09 |

---

## 09. Project Owner Approval

| Field | Value |
|---|---|
| Approved by | _________________________ |
| Title | Project Owner |
| Signature | _________________________ |
| Date | _________________________ |

This Resolution is effective upon signature.
