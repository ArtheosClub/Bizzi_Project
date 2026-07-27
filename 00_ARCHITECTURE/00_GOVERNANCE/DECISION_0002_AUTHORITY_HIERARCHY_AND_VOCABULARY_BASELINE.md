# DECISION 0002 — Authority Hierarchy and Vocabulary Baseline

Version: 1.0
Status: APPROVED
Class: Governance Decision (not architectural — no domain concept, entity, or D-numbered decision is created, modified, or reopened by this record)
Owner: Project Owner
Approved by: Project Owner
Approval date: 2026-07-23
Effective: Immediately, for governance purposes only (see Scope)

## Purpose

Formally ratify the Authority Hierarchy and Vocabulary Baseline proposed in the Architecture Governance Reconciliation (AGR-01), resolving the competing-authority and vocabulary-mismatch findings raised in the Architecture Readiness Review (ARR-01), without redesigning ADW-01 or reopening D01–D10.

This is Governance Execution Step 2 of the Architecture Baseline Resolution Package. It ratifies the *content* of the hierarchy and vocabulary mapping so that the document-synchronization steps that follow (Steps 3–5) have an approved target to synchronize the repository's other documents toward. It does not itself perform that synchronization.

## Decision

### 1. Authority Hierarchy — APPROVED

The following hierarchy, as defined in AGR-01 §2, is adopted as binding:

| Tier | Document(s) | Authoritative for |
|---|---|---|
| 0 | Any explicit Project Owner decision record | The specific thing it decided |
| 1 | Decision 0001 (MVP First & Architecture Freeze) | What may and may not be built/decided during the MVP phase |
| 2 | `00_ARCHITECTURE/` (`ARCHITECTURE_SPECIFICATION.md`, `DOMAIN_FOUNDATION.md`, D01–D10, Decision Register) | Domain semantics — what concepts exist, what they mean, how they relate, how they end |
| 3 | `docs/adr/*` | Implementation-pattern and technology decisions — coordinate with Tier 2, not subordinate to it; where a specific point genuinely overlaps, Tier 2's domain-semantic ruling governs that point, triggering the ADR's own normal supersession process |
| 4 | `docs/planning/` + `50_IMPLEMENTATION/` | Sequencing and MVP scope, deriving vocabulary from Tier 2 and technology assumptions from Tier 3 |
| 5 | `docs/c4/*` | Illustration of Tiers 2–4; not independently authoritative |
| 6 | `backend/` (code) | Nothing architectural; must conform to all above |
| — | `01_GOVERNANCE/GOVERNANCE_MODEL.md`, `AUTHORITY_MATRIX.md` | The platform-wide "Art of Business" vision — a different, broader system; source vocabulary (L1–L5/A0–A7) that `CLAUDE.md`/`DEVELOPMENT_PLAN.md` §7 adapt in simplified form for the MVP backend build, not directly binding on it except through that adaptation |
| — | `CLAUDE.md` | The process layer — states how the tiers above relate and change; not itself a competing content authority |
| — | Historical records (superseded ADR-0002, `WORK_PACKAGES.md`, original Phase 0–3 `DEVELOPMENT_PLAN.md` text) | Nothing — record only |

**There is exactly one architectural authority as a result of this decision: the Project Owner, exercised through this non-competing tier structure — not any single document.**

### 2. Governance-Classification Mapping — APPROVED

`Class A — Constitutional` (used throughout D01–D10) is confirmed equivalent, in escalation weight, to `DEVELOPMENT_PLAN.md` §7's `L3+/A3+` "stop and consult Project Owner" tier and to `GOVERNANCE_MODEL.md`'s `L5` "Human Approval Required" tier. Every Class A decision has always required exactly what those tiers require — explicit Project Owner sign-off before the decision is binding. This confirms existing practice; it creates no new escalation tier.

### 3. Vocabulary Baseline — APPROVED

The vocabulary reconciliation classifications defined in AGR-01 §4 are adopted as binding, without renaming any term in D01–D10:

| ADW-01 term | Engineering-track term | Classification |
|---|---|---|
| Enterprise Object | EnterpriseObject | Equivalent |
| Runtime Session | RuntimeSession | Equivalent |
| Work Item → Task (specialization) | Task | Equivalent |
| Actor | User + WorkspaceMembership | Documentation update required |
| Business Operation | *(absent from Gate A / PRE-CODING-BRIEF)* | Documentation update required |
| Decision (D06) | "Human Approval / Decision", Decision Record | Equivalent, informally stated pre-ADW-01 |
| AgentDefinition / AgentInstance / Provider / Model | *(absent from ADW-01)* | Future concept — governed by PRE-CODING-BRIEF until ADW-05 |
| Relationship Context (D09 §5.8) | ContextPackage | Historical term / naming coincidence — no action |
| AuditRecord relationships (GC-002) | Audit/Event relationships (ADW-07, not yet written) | Future concept, provisionally governed by GC-002 |
| Class A — Constitutional | L1–L5 / A0–A7 | Equivalent, per §2 above |

## What This Decision Does Not Do

- Does not modify, reopen, or reinterpret D01–D10.
- Does not modify Decision 0001.
- Does not update `ARCHITECTURE_SPECIFICATION.md`, `CLAUDE.md`, `ADW_01_CORE_DOMAIN_SEMANTICS.md`, `DOMAIN_FOUNDATION.md`, Gate A, or `GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md` — those are Steps 3–5 of the Architecture Baseline Resolution Package's Execution Order and remain pending.
- Does not activate the Architecture Baseline.
- Does not constitute the Architecture Baseline Resolution signature (Step 9).
- Does not introduce a new governance principle — it ratifies content AGR-01 already fully specified and ARR-01 already found necessary.

## Governance Activation Status

```text
Step 1 — D10 approval and closure:                    COMPLETE
Step 2 — Authority Hierarchy and Vocabulary Baseline:  COMPLETE (this record)
Step 3 — Synchronize ADW_01_CORE_DOMAIN_SEMANTICS.md:  PENDING
Step 4 — Synchronize DOMAIN_FOUNDATION.md:             PENDING
Step 5 — Synchronize ARCHITECTURE_SPECIFICATION.md:    PENDING
Step 6 — Synchronize CLAUDE.md:                        PENDING
Step 7 — Synchronize Gate A WP02:                      PENDING
Step 8 — Synchronize GATE_C_ARCHITECTURE_DECISION_PROPOSALS.md: PENDING
Step 9 — Project Owner signs Architecture Baseline Resolution:  PENDING

Governance activation: IN PROGRESS
Architecture Baseline: NOT YET ACTIVATED
```

## Decision Rule

This record answers only: *what* hierarchy and vocabulary govern the repository going forward. It does not yet make any other document say so — that is Steps 3–8, each its own scoped action, none authorized by this record alone.
