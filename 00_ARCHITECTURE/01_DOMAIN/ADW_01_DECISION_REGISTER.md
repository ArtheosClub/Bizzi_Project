# ADW-01 — Decision Register

**Document ID:** ARCH-DOMAIN-DECISIONS-001  
**Version:** 0.2-draft  
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
| D02 | Core Business Abstraction | APPROVED |
| D03 | Work Model | APPROVED |
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

## 4. D02 — Core Business Abstraction

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

### Decision

> Enterprise Object is the stable platform abstraction for a durable, workspace-owned, business-relevant thing with identity, lifecycle, ownership, relationships, and governance requirements.
>
> Enterprise Object defines a shared minimum contract but does not replace specialized domain entities, aggregates, schemas, or invariants.
>
> Concrete Enterprise Object types must retain explicit typed contracts.
>
> A universal unvalidated JSON-based Enterprise Object model is prohibited as the authoritative domain representation.

### Consequences

1. Durable business entities share a minimum platform contract for identity, Workspace ownership, lifecycle, ownership metadata, versioning, classification, and relationships.
2. Customer, Supplier, Contract, Invoice, Shipment, Asset, and other concrete types retain their own schemas, behavior, and invariants.
3. Work Items, Decisions, Evidence, Runtime Sessions, events, and audit records may reference Enterprise Objects through stable typed references.
4. Enterprise Object is not required to be implemented as one universal table or one generic aggregate.
5. New Enterprise Object types may be introduced without changing core coordination mechanisms, provided they satisfy the shared contract.
6. Task, Decision, Evidence, Runtime Session, Domain Event, and Audit Record are not automatically classified as Enterprise Objects.

### Supersession rule

D02 may be changed only by an explicit architecture decision that defines compatibility, data migration, validation, and API impact.

---

## 5. D03 — Work Model

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

### Decision

> Work Item is the abstract representation of governed business work.
>
> Task, Case, and Project are specialized Work Item types that share the common operational contract while retaining their own lifecycle rules and business invariants.
>
> Orchestration, assignment, prioritization, approval, escalation, observation, and execution mechanisms operate against the Work Item abstraction where the shared contract is sufficient.

### Consequences

1. Every Work Item has a common minimum contract including identity, Workspace ownership, type, objective, status, ownership, priority, lifecycle metadata, and relationships.
2. Task, Case, and Project are not reduced to one identical behavior model.
3. New Work Item types may be added without redesigning common orchestration mechanisms.
4. A Work Item may reference one or more Enterprise Objects through explicit typed relationships.
5. An Enterprise Object may participate in multiple concurrent Work Items, subject to domain policies and authorization.
6. Specialized lifecycle behavior must not be hidden inside unvalidated generic fields.
7. Whether Task, Case, and Project are one aggregate hierarchy or separate aggregate roots remains a separate D08 decision.

### Supersession rule

D03 may be changed only by an explicit architecture decision defining migration of work types, lifecycle behavior, references, authorization, and orchestration contracts.

---

## 6. Workshop Progress

```text
D01: APPROVED
D02: APPROVED
D03: APPROVED
D04-D07: PENDING
D08-D10: OPEN
ADW-01: IN PROGRESS
```
