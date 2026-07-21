# ADW-01 — Decision Register

**Document ID:** ARCH-DOMAIN-DECISIONS-001  
**Version:** 0.1-draft  
**Status:** Workshop in progress  
**Architecture Gate:** Gate C v1.1  
**Workshop:** ADW-01 — Domain Core  
**Decision authority:** Project Owner  
**Parent chapter:** `00_ARCHITECTURE/01_DOMAIN/DOMAIN_CORE.md`

---

## 1. Purpose

This register records Project Owner decisions made during ADW-01 before final synchronization into `DOMAIN_CORE.md`, the Architecture Decision Register, and the root Architecture Specification.

Each decision is recorded independently so the workshop history remains explicit and auditable.

---

## 2. Decision Status Summary

| Decision | Subject | Status |
|---|---|---|
| D01 | Primary Boundary | APPROVED |
| D02 | Core Business Abstraction | PENDING |
| D03 | Work Model | PENDING |
| D04 | Task versus Execution | PENDING |
| D05 | Actor Model | PENDING |
| D06 | Decision Semantics | PENDING |
| D07 | Operational State | PENDING |
| D08 | Aggregate Strategy | OPEN |
| D09 | Relationship Model | OPEN |
| D10 | Deletion and Supersession | OPEN |

---

## 3. D01 — Primary Boundary

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

### Decision

> Workspace is the primary ownership, authorization, and isolation boundary for business-state objects in the Bizzi Platform.
>
> Every workspace-scoped business object belongs to exactly one Workspace.
>
> An Enterprise may group multiple Workspaces, but Enterprise is not required as an operational boundary for the MVP.
>
> The term Tenant is reserved for infrastructure and deployment concerns and must not replace Workspace in the core domain vocabulary.

### Consequences

1. Every workspace-scoped aggregate must contain or securely derive an immutable `workspace_id`.
2. Cross-workspace access is denied unless an explicit platform-level sharing or transfer contract authorizes it.
3. A business object cannot change Workspace through an ordinary update operation.
4. Users, human actors, service actors, and agent definitions may participate in more than one Workspace only through explicit membership or publication rules.
5. Runtime state, memory, evidence, decisions, audit records, and operational agent state remain Workspace-isolated.
6. Enterprise is a future consolidation and governance level, not the MVP operational isolation boundary.
7. Detailed identity, membership, and authorization semantics remain assigned to ADW-02 and ADW-03.

### Supersession rule

D01 may be changed only by an explicit architecture decision approved by the Project Owner and accompanied by a migration and security-impact analysis.

---

## 4. Workshop Progress

```text
D01: APPROVED
D02-D07: PENDING
D08-D10: OPEN
ADW-01: IN PROGRESS
```
