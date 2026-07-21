# ADW-01 — Decision Register

**Document ID:** ARCH-DOMAIN-DECISIONS-001  
**Version:** 0.5-draft  
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
| D04 | Task versus Execution | APPROVED |
| D05 | Actor Model | APPROVED |
| D06 | Decision Semantics | PENDING |
| D07 | Operational State | PENDING |
| D08 | Aggregate Strategy | APPROVED |
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

## 6. D04 — Task versus Execution

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

### Decision

> Task represents governed business work and owns its business lifecycle, assignment, objective, completion criteria, and accepted outcome.
>
> Runtime Session represents one governed execution context or attempt performed by one Actor or a coordinated set of Actors.
>
> Task and Runtime Session are separate aggregates with independent identities and lifecycle state.
>
> One Task may have zero, one, or multiple Runtime Sessions.
>
> A successful Runtime Session does not automatically complete a Task. It produces or proposes Results that the Task domain process evaluates against completion, approval, policy, and authority requirements.
>
> Runtime Session state is never the authoritative source of Task state.

### Consequences

1. A Task may be completed manually without creating a Runtime Session.
2. Multiple execution attempts may be associated with one Task without overwriting business-work history.
3. Runtime failures, retries, timeouts, cancellations, and tool errors do not directly determine the business status of the Task.
4. A successful Runtime Session may move a Task to review rather than completion when approval or acceptance is required.
5. Runtime Session owns execution-specific state, including initiating and effective Actors, actions, tool invocations, attempts, failures, and output references.
6. Task owns objective, assignment, deadline, completion criteria, accepted Result, and authoritative business status.
7. Runtime Sessions may serve a Task or another explicitly authorized execution context; detailed cardinality and standalone-operation rules are deferred to ADW-05.
8. Retry, fallback, model routing, human intervention, and execution recovery must be designed around Runtime Session rather than Task state.

### Supersession rule

D04 may be changed only by an explicit architecture decision defining migration of Task state, execution history, result acceptance, retry behavior, and audit semantics.

---

## 7. D05 — Actor Model

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

### Decision

> Actor is the stable identity of a human, agent, service, or external participant capable of initiating, performing, approving, observing, or being accountable for governed actions in the Bizzi Platform.
>
> Human Actor, Agent Actor, Service Actor, and External Actor are explicit Actor types. Actor type must not be inferred only from credentials, roles, or display names.
>
> Actor is distinct from User Account, Role, Agent Definition, and Runtime Session.
>
> Roles and capabilities are assigned to Actors within an explicit Workspace and scope. An Actor may hold multiple contextual roles.
>
> Every governed action must identify the effective Actor and, where different, the initiating, delegating, approving, and technical Actors.
>
> Delegation must be explicit, scoped, time-bounded where appropriate, revocable, auditable, and incapable of granting authority exceeding the delegator's effective authority.
>
> Agent and Service Actors must use distinct identities. Shared generic system identities are prohibited for authoritative business actions.
>
> Actor suspension, retirement, revocation, or compromise must not erase historical attribution or audit records.

### Consequences

1. Human, agent, service, and external participants use one shared Actor abstraction while retaining explicit Actor types.
2. Authentication identity, operational identity, assigned role, agent definition, and execution session remain separate concepts.
3. A User Account authenticates access but is not itself the authoritative business Actor.
4. An Agent Definition may be instantiated as different Agent Actors in different Workspaces without merging their identity, authority, memory, or audit history.
5. Every governed action records the effective Actor and preserves the relevant initiation, delegation, approval, and technical-execution chain.
6. Role and capability assignments are contextual and must include Workspace and scope rather than becoming unrestricted global authority.
7. Delegated authority must be a subset of the delegator's effective authority and must be constrained by purpose, scope, validity, policy, and revocation state.
8. Execution responsibility, decision accountability, and business ownership may belong to different Actors and must not be collapsed into one attribution field.
9. Suspended, retired, revoked, or compromised Actors remain addressable for historical and audit purposes.
10. Generic identities such as `system` must not be used as the authoritative Actor for independent agents, services, connectors, or automations.
11. Detailed authentication, membership, role-assignment, capability-evaluation, and authorization semantics remain assigned to ADW-02 and ADW-03.
12. Detailed runtime actor participation, coordinated execution, and tool-use semantics remain assigned to ADW-05.

### Supersession rule

D05 may be changed only by an explicit architecture decision defining identity migration, attribution compatibility, delegation impact, authorization consequences, audit preservation, and active-credential revocation.

---

## 8. D08 — Aggregate Strategy

**Status:** `APPROVED`  
**Approved by:** Project Owner  
**Approval date:** 2026-07-21

### Decision

> Work Item is a shared domain contract and coordination abstraction, not one universal aggregate root.
>
> Task, Case, and Project are separate aggregate roots because they own materially different lifecycle rules, invariants, state, and outcomes.
>
> Each concrete Work Item aggregate must implement the common Work Item contract for identity, Workspace ownership, objective, status, ownership, priority, lifecycle metadata, relationships, and common coordination operations.
>
> Common orchestration mechanisms may operate through typed Work Item references and shared application services.
>
> No Work Item aggregate may directly own another complete Work Item aggregate. Relationships across Work Items use stable typed references.
>
> A shared Work Item index or read model may be used for search, coordination, and reporting, but it is not the authoritative source of specialized aggregate state.

### Consequences

1. Task, Case, and Project retain independent aggregate boundaries and authoritative state.
2. The common Work Item contract does not require ORM inheritance, a universal database table, or a universal persistence schema.
3. Specialized invariants remain inside the concrete aggregate that owns them.
4. Project and Case aggregates reference related Work Items by stable typed identifiers rather than embedding complete foreign aggregates.
5. Common assignment, prioritization, escalation, search, reporting, and orchestration services may operate through typed Work Item references.
6. A common Work Item index is a projection and may be rebuilt from authoritative aggregate state.
7. New Work Item types may be added by implementing the common contract without modifying existing specialized aggregates.

### Supersession rule

D08 may be changed only by an explicit architecture decision defining aggregate ownership, lifecycle migration, reference compatibility, persistence impact, and authoritative-state transitions.

---

## 9. Workshop Progress

```text
D01: APPROVED
D02: APPROVED
D03: APPROVED
D04: APPROVED
D05: APPROVED
D06-D07: PENDING
D08: APPROVED
D09-D10: OPEN
ADW-01: IN PROGRESS
```
