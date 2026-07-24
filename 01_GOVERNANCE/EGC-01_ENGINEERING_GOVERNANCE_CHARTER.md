# EGC-01 — Engineering Governance Charter

## 00. Document Control

| Field | Value |
|---|---|
| Document ID | EGC-01 |
| Title | Engineering Governance Charter |
| Version | 1.0 |
| Status | **ACTIVE** |
| Effective Date | 2026-07-24 |
| Repository | ArtheosClub/Bizzi_Project |
| Authority | Project Owner (Tier 0, per `DECISION_0002_AUTHORITY_HIERARCHY_AND_VOCABULARY_BASELINE.md` §1) |
| Owner | Project Owner |
| Supersedes | None |
| Related Documents | `00_ARCHITECTURE/00_GOVERNANCE/DECISION_0001_MVP_FIRST.md`; `00_ARCHITECTURE/00_GOVERNANCE/DECISION_0002_AUTHORITY_HIERARCHY_AND_VOCABULARY_BASELINE.md`; `00_ARCHITECTURE/00_GOVERNANCE/ABR-01_ARCHITECTURE_BASELINE_RESOLUTION.md` |

---

## 01. Purpose

Architecture defines what the Bizzi Platform is. Engineering defines how
it is built. Engineering operates under the Architecture Baseline; it
does not originate architectural authority. This Charter exists to
establish the constitutional governance of engineering activity. It does
not govern architecture.

---

## 02. Constitutional Basis

This Charter's constitutional legitimacy derives from Decision 0001 (MVP
First & Architecture Freeze), DECISION_0002 (Authority Hierarchy and
Vocabulary Baseline), and ABR-01 (Architecture Baseline Resolution). Each
remains fully in force and is unmodified by this Charter. This Charter
exists only because the Architecture Baseline established by ABR-01 is
ACTIVE; it holds no constitutional standing independent of that Baseline.

---

## 03. Scope

This Charter governs engineering activity: implementation, code,
repositories, infrastructure, automation, AI-assisted engineering,
testing, and delivery.

Architecture governance — the definition, interpretation, or evolution of
Core Domain Semantics, the Authority Hierarchy, or the Canonical
Vocabulary Baseline — remains outside this Charter's scope. It is
governed exclusively by ABR-01, Decision 0001, and DECISION_0002.

---

## 04. Engineering Principles

The following are constitutional principles of engineering, binding upon
all engineering activity within scope:

- **Architecture First** — No engineering activity shall proceed in contradiction of the Architecture Baseline.
- **Baseline Integrity** — Engineering shall preserve, and shall not erode, the integrity of the Architecture Baseline.
- **No Architecture Drift** — Engineering shall not introduce architectural meaning not already established by the Architecture Baseline.
- **Implementation Traceability** — Every engineering output shall be traceable to an authoritative source.
- **Deterministic Engineering** — Engineering outcomes shall be reproducible and shall not depend on unrecorded assumption.
- **Small Verifiable Changes** — Engineering change shall proceed in units capable of independent verification.
- **Reproducibility** — Engineering outputs shall be reproducible from recorded, authoritative inputs.
- **Security by Default** — Engineering shall assume the more restrictive posture wherever authority is undetermined.
- **Automation First** — Engineering shall prefer automated, verifiable enforcement over discretionary judgment wherever constitutionally permitted.
- **Evidence Before Assumption** — Engineering shall act only upon verified evidence, never upon assumption of an unverified state.

---

## 05. Engineering Authority

Engineering authority is the authority to determine how approved
architecture is implemented. It is not the authority to determine what
architecture is. Engineering authority is subordinate to, and derived
from, the Architecture Baseline. Where engineering authority and
architectural authority conflict, architectural authority prevails,
without exception.

This Charter defines engineering responsibility. It does not define,
redefine, or extend the Authority Hierarchy established by DECISION_0002
§1.

---

## 06. Engineering Change Policy

Three constitutional categories of engineering change exist:

1. **Change within Architecture Conformance** — engineering change that implements, without altering, an already-approved architectural decision. Such change requires no architectural approval.
2. **Change requiring Architecture Governance** — engineering change that would introduce, alter, or extend architectural meaning not already established by the Architecture Baseline. Such change requires prior Architecture Governance, exercised through the Project Owner under the Authority Hierarchy.
3. **Change prohibited under Architecture Freeze** — engineering change that would contradict, supersede, or bypass a Core Domain Semantic, the Authority Hierarchy, or the Canonical Vocabulary Baseline. Such change is constitutionally prohibited for the duration of the Architecture Freeze.

This Charter states these categories. It does not define the operational
process by which a given change is classified.

---

## 07. Engineering Compliance

Engineering outputs shall remain consistent with the Architecture
Baseline, the Authority Hierarchy, the Canonical Vocabulary Baseline, and
approved ADRs. An engineering output inconsistent with any of these is
not constitutionally valid, irrespective of its technical correctness.

This Charter states the compliance requirement. It does not define the
procedure by which compliance is audited or enforced.

---

## 08. AI Engineering Governance

AI-generated engineering artifacts possess no independent constitutional
authority. Human approval, exercised through the Project Owner under the
Authority Hierarchy, is the sole source of constitutional authority for
any engineering output, whether AI-generated or not.

AI shall not:

- originate a constitutional decision;
- approve a constitutional document;
- activate a constitutional document;
- independently modify a constitutional document;
- exercise constitutional authority.

AI may record, implement, or mechanically apply an already-authorized
constitutional decision, but only under explicit instruction from the
Project Owner or another constitutionally authorized authority. Such
recording or implementation does not constitute constitutional authority
and shall not be interpreted as independent constitutional
decision-making.

AI shall not redefine architecture. AI shall not bypass this Charter,
ABR-01, Decision 0001, or DECISION_0002 under any operational
justification.

---

## 09. Repository Governance

The repository shall preserve its own integrity as a record of
constitutional and engineering fact. Every repository artifact shall
remain traceable to its authoritative source. Where two repository
artifacts conflict, the artifact of higher constitutional authority, per
the Authority Hierarchy, prevails. Evidence of constitutional and
engineering process shall be preserved and shall not be silently altered
or removed.

This Charter states these principles. It does not define version-control
procedure.

---

## 10. Interpretation

In the event of any conflict between this Charter and ABR-01, Decision
0001, or DECISION_0002, the higher-authority document prevails, per the
Authority Hierarchy established by DECISION_0002 §1. This Charter
introduces no authority capable of overriding any of the three.

---

## 11. Project Owner Approval

| Field | Value |
|---|---|
| Approved by | Project Owner |
| Title | Project Owner |
| Signature | APPROVED |
| Date | 2026-07-24 |

Status: **ACTIVE**. Activated and signed 2026-07-24.
