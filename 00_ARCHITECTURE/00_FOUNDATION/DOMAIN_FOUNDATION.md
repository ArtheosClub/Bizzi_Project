# Bizzi Domain Foundation

**Document ID:** ARCH-FOUNDATION-DOMAIN-001  
**Version:** 0.2-draft  
**Status:** Stabilized foundation baseline  
**Architecture Gate:** Gate C v1.1  
**Owner:** Project Owner  
**Decision authority:** Project Owner  
**Related workshop:** `ADW-01 — Core Domain Semantics`  
**Authoritative workshop path:** `00_ARCHITECTURE/01_DOMAIN/ADW_01_CORE_DOMAIN_SEMANTICS.md`

---

## 1. Purpose

This document defines the stable conceptual foundation of the Bizzi Platform.

Bizzi is an enterprise operating platform designed to model, govern, execute, observe, and improve business activity performed by human, agent, service, and external Actors under explicit organizational authority.

This foundation is semantic rather than technological. It remains valid independently of programming language, framework, database, AI provider, interface, deployment topology, or integration mechanism.

---

## 2. Enterprise Definition

> An enterprise is a governed socio-technical system that continuously performs Business Operations through Actors in order to change the state of Enterprise Objects according to Decisions, Policies, and Objectives.

Bizzi represents the enterprise as a network of governed Business Operations executed by Actors against Enterprise Objects under Decisions.

---

## 3. Primary Boundary

Workspace is the primary ownership, authorization, governance, and isolation boundary for business-state objects in Bizzi.

Every workspace-scoped domain object belongs to exactly one Workspace unless explicitly classified as platform-global metadata.

Enterprise may group multiple Workspaces, but it is not required as the MVP operational boundary. Tenant remains an infrastructure term and must not replace Workspace in the core domain vocabulary.

---

## 4. Five Fundamental Domain Concepts

Within a Workspace, Bizzi recognizes five fundamental domain concepts.

| Concept | Governing question | Authoritative concern |
|---|---|---|
| Enterprise Object | What does the enterprise manage? | Specialized business state and invariants |
| Actor | Who participates or acts? | Operational identity and attribution |
| Work Item | What work must be organized? | Work coordination and accepted work outcome |
| Decision | What has been authoritatively determined? | Governance determination and authority basis |
| Business Operation | How is an authorized intent realized? | End-to-end operational objective and business outcome |

### 4.1 Enterprise Object

Enterprise Object is the shared platform abstraction for a durable business-relevant thing with identity, lifecycle, ownership, relationships, state, and governance requirements.

It is not one universal table, generic JSON document, or replacement for specialized domain aggregates.

### 4.2 Actor

Actor is the stable identity of a human, agent, service, or external participant capable of initiating, performing, approving, observing, or being accountable for governed activity.

Actor is distinct from User Account, Role, Agent Definition, credential, and Runtime Session.

### 4.3 Work Item

Work Item is the shared representation of governed business work requiring organization, coordination, observation, or completion.

Task, Case, and Project are specialized Work Item types and retain their own aggregate boundaries, lifecycle rules, and invariants.

### 4.4 Decision

Decision is the stable and auditable representation of a governed determination about what should or should not occur within an explicit Workspace, subject, context, authority, and set of conditions.

Decision is distinct from recommendation, command, execution, action, result, state transition, and event.

### 4.5 Business Operation

Business Operation is the stable and traceable representation of a significant governed business action from intent and authorization through execution, validation, outcome evaluation, and closure.

Business Operation is distinct from Decision, Work Item, Workflow, Runtime Session, Action, Result, State Transition, and Domain Event.

---

## 5. Primary Construction

Bizzi adopts the following primary construction:

```text
Decision
+
Business Operation
```

Decision is the governance center: it defines what should or should not occur.

Business Operation is the operational center: it coordinates the realization of an authorized intent or Decision and preserves the end-to-end business history.

Work Item organizes work. Runtime Session represents an execution context or attempt. Neither replaces Decision or Business Operation.

---

## 6. Enterprise Behaviour Model

```text
Intent
  -> Decision
  -> Authorization
  -> Business Operation
  -> Execution Plan
  -> Work Items and Runtime Sessions
  -> Actions
  -> Results
  -> Domain Validation
  -> State Transition
  -> Domain Event
  -> Business Outcome Evaluation
  -> Learning
```

This chain is semantic rather than a mandatory synchronous workflow.

Not every low-risk action requires a separately persisted Decision. Every governed action must nevertheless have an explicit and auditable authority basis derived from a Decision, policy, role, capability, delegation, or approved governance rule.

---

## 7. Domain Ownership

Each domain concept owns only its authoritative truth.

- Enterprise Object owns its specialized business state and invariants.
- Actor owns operational identity and historical attribution.
- Work Item owns work-coordination lifecycle and accepted work outcome.
- Decision owns governance determination, authority basis, conditions, status, and supersession history.
- Business Operation owns operational objective, coordination history, execution trace, validation progress, and business outcome.
- Runtime Session owns execution-attempt state and technical execution history.

Business Operation is not a universal super-aggregate. It coordinates other concepts through contracts and stable typed references but does not absorb their authoritative state.

Only the owning aggregate or an explicitly authorized domain process may commit an authoritative state transition.

---

## 8. State Foundation

State semantics are governed by the following preliminary rules pending completion of D07:

1. Authoritative State belongs to exactly one owning aggregate or explicitly defined domain authority.
2. Execution State, Work State, Decision State, Operation State, and Business Object State are distinct state domains.
3. A Result is not itself an authoritative State Transition.
4. A Domain Event records that a significant fact occurred; it is not a command and does not independently authorize mutation.
5. A Projection or read model is derived and rebuildable; it is not the authoritative source of specialized aggregate state.
6. State transitions must be validated against ownership, invariants, authority, expected version, and applicable policy.
7. Technical success does not imply business-state success.

D07 — State Semantics will finalize the state model, transition contract, consistency boundaries, projections, concurrency, and terminal-state rules.

---

## 9. Architectural Laws

1. **Authority Basis:** No significant Business Operation exists without an explicit and auditable authority basis.
2. **State Ownership:** Only the owning aggregate or authorized domain process may change authoritative state.
3. **Governance and Execution Are Separate:** Decision establishes what should occur; execution attempts to realize it.
4. **Work Coordination Is Not Governance:** Task, Case, Project, Workflow, and Runtime Session do not replace Decision.
5. **Technical Success Is Not Business Success:** Successful execution does not automatically establish completion or outcome.
6. **Historical Truth Is Preserved:** Decisions, Operations, attribution, outcomes, failures, reversals, and compensation history are not erased.
7. **Compensation Is Explicit:** Compensation or reversal is a new governed Business Operation linked to the original.
8. **Typed Contracts:** Shared abstractions do not eliminate specialized schemas, lifecycle rules, authority requirements, or invariants.
9. **Observable Operations:** Significant Business Operations are traceable from intent and authority through execution, validation, state effects, and outcome.
10. **AI Does Not Imply Authority:** AI recommendations become authoritative only through explicit authority or scoped delegation.
11. **Derived State Is Not Authoritative State:** Projections, indexes, caches, and search models never silently become the owner of domain truth.

---

## 10. Architectural Layers

```text
Enterprise Strategy and Objectives
  -> Governance and Policy
  -> Decisions
  -> Business Operations
  -> Work Coordination
  -> Runtime and Tools
  -> Infrastructure
```

Knowledge, Evidence, Audit, Provenance, Risk, Compliance, State Management, and Eventing operate across these layers while respecting Workspace boundaries and domain ownership.

---

## 11. What Bizzi Is Not

Bizzi is not defined as a task manager, workflow engine, BPM suite, ERP, CRM, document management system, AI chat interface, agent framework, or event store.

Bizzi may contain, integrate, or expose these capabilities, but none of them alone defines the platform.

---

## 12. Evolution Rule

This foundation may be changed only through an explicit architecture decision approved by the Project Owner.

Any change must describe semantic compatibility, affected ADW decisions, aggregate ownership, authority implications, state and history migration, API impact, event compatibility, and audit preservation.

---

## 13. Stabilization Record

| Date | Decision | Result |
|---|---|---|
| 2026-07-21 | Architecture Stabilization | `Domain Core` terminology retired; `Core Domain Semantics` established as the single ADW-01 vocabulary. |
| 2026-07-21 | D06 closure | `Decision + Business Operation` approved as the primary construction. |
| 2026-07-21 | D07 initiation | `State Semantics` opened as the final major foundational decision before ADW-02. |
