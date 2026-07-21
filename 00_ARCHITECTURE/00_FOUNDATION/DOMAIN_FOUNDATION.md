# Bizzi Domain Foundation

**Document ID:** ARCH-FOUNDATION-DOMAIN-001  
**Version:** 0.1-draft  
**Status:** Foundation draft  
**Architecture Gate:** Gate C v1.1  
**Owner:** Project Owner  
**Decision authority:** Project Owner  
**Related workshop:** ADW-01 — Core Domain Semantics

---

## 1. Purpose

This document defines the stable conceptual foundation of the Bizzi Platform before the detailed Architecture Decision Workshops continue.

Bizzi is an enterprise operating platform designed to model, govern, execute, observe, and improve business activity performed by human, agent, service, and external Actors under explicit organizational authority.

This foundation is semantic rather than technological. It must remain valid independently of programming language, framework, database, AI provider, interface, deployment topology, or integration mechanism.

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

### 4.1 Enterprise Object

Enterprise Object represents a durable business-relevant thing with identity, lifecycle, ownership, relationships, state, and governance requirements.

It answers:

> What does the enterprise manage?

Enterprise Object is a shared platform contract, not one universal table, generic JSON document, or replacement for specialized domain aggregates.

### 4.2 Actor

Actor is the stable identity of a human, agent, service, or external participant capable of initiating, performing, approving, observing, or being accountable for governed activity.

It answers:

> Who participates or acts?

Actor is distinct from User Account, Role, Agent Definition, credential, and Runtime Session.

### 4.3 Work Item

Work Item is the shared representation of governed business work requiring organization, coordination, observation, or completion.

It answers:

> What work must be organized?

Task, Case, and Project are specialized Work Item types and retain their own aggregate boundaries, lifecycle rules, and invariants.

### 4.4 Decision

Decision is the stable and auditable representation of a governed determination about what should or should not occur within an explicit Workspace, subject, context, authority, and set of conditions.

It answers:

> What has been authoritatively determined?

Decision is distinct from recommendation, command, execution, action, result, state transition, and event.

### 4.5 Business Operation

Business Operation is the stable and traceable representation of a significant governed business action from intent and authorization through execution, validation, outcome evaluation, and closure.

It answers:

> How does the enterprise realize an authorized intent or Decision?

Business Operation is distinct from Decision, Work Item, Workflow, Runtime Session, Action, Result, and Domain Event.

---

## 5. Core Construction

Bizzi adopts the following primary construction:

```text
Decision
+
Business Operation
```

Decision is the governance center: it defines what should or should not occur.

Business Operation is the operational center: it coordinates the realization of an authorized intent or Decision and preserves the end-to-end business history.

Work Item is the work-coordination mechanism. Runtime Session is an execution context or attempt. Neither replaces Decision or Business Operation.

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
  -> State Transitions
  -> Domain Events
  -> Business Outcome Evaluation
  -> Learning
```

Not every low-risk technical action requires a separately persisted Decision. Every governed action must nevertheless have an explicit and auditable authority basis derived from a Decision, policy, role, capability, delegation, or approved governance rule.

---

## 7. Relationship Model

```text
Actor
  makes, authorizes, executes, approves, or observes
Decision and Business Operation

Decision
  governs, authorizes, rejects, redirects, suspends, or accepts
Business Operation

Business Operation
  coordinates
Actors, Decisions, Work Items, Runtime Sessions, Actions, Results, and Evidence

Business Operation
  references and affects
Enterprise Objects

Domain Aggregate
  owns and validates
Authoritative State
```

One Decision may govern zero, one, or multiple Business Operations. One Business Operation may depend on multiple Decisions.

One Business Operation may coordinate multiple Work Items and Runtime Sessions. One Work Item may support multiple Business Operations where the domain permits it.

All cross-aggregate relationships use stable typed references unless an explicit aggregate design decision establishes ownership.

---

## 8. Domain Ownership

Each domain concept owns only its authoritative truth.

- Enterprise Object owns its specialized business state and invariants.
- Actor owns operational identity and historical attribution.
- Work Item owns work-coordination lifecycle and accepted work outcome.
- Decision owns governance determination, authority basis, conditions, status, and supersession history.
- Business Operation owns operational objective, coordination history, execution trace, validation progress, and business outcome.
- Runtime Session owns execution-attempt state and technical execution history.

Business Operation is not a universal super-aggregate. It coordinates other concepts through contracts and references but does not absorb their authoritative state.

Only the owning aggregate or authorized domain process may commit an authoritative state transition.

---

## 9. Architectural Laws

### Law 1 — Authority Basis

No significant Business Operation exists without an explicit and auditable authority basis.

### Law 2 — State Ownership

Only the owning aggregate or authorized domain process may change authoritative state.

### Law 3 — Governance and Execution Are Separate

Decision establishes what should occur. Execution attempts to realize it. Neither may be inferred solely from the other.

### Law 4 — Work Coordination Is Not Governance

A Task, Case, Project, Workflow, or Runtime Session does not replace Decision or authority evaluation.

### Law 5 — Technical Success Is Not Business Success

A successful Action or Runtime Session does not automatically establish completion, acceptance, or the intended business outcome.

### Law 6 — Historical Truth Is Preserved

Decisions, Business Operations, attribution, outcomes, failures, reversals, and compensation history are not erased or rewritten.

### Law 7 — Compensation Is Explicit

Compensation or reversal is represented as a new governed Business Operation linked to the original operation.

### Law 8 — Typed Contracts

Fundamental abstractions may share platform contracts, but specialized domain types retain explicit schemas, lifecycle rules, authority requirements, and invariants.

### Law 9 — Observable Operations

Significant Business Operations must be traceable from intent and authority through execution, validation, state effects, and outcome.

### Law 10 — AI Does Not Imply Authority

AI-generated recommendations are not authoritative Decisions unless accepted by an authorized Actor or permitted by an explicit scoped delegation.

---

## 10. What Bizzi Is Not

Bizzi is not defined as any one of the following:

- a task manager;
- a workflow engine;
- a BPM suite;
- an ERP or CRM;
- a document management system;
- an AI chat interface;
- an agent framework;
- an event store.

Bizzi may contain, integrate, or expose these capabilities, but none of them alone defines the platform.

---

## 11. Architectural Layers

```text
Enterprise Strategy and Objectives
  -> Governance and Policy
  -> Decisions
  -> Business Operations
  -> Work Coordination
  -> Runtime and Tools
  -> Infrastructure
```

Knowledge, Evidence, Audit, Provenance, Risk, Compliance, and Eventing operate across these layers while respecting Workspace boundaries and domain ownership.

---

## 12. Evolution Rule

This foundation may be changed only through an explicit architecture decision approved by the Project Owner.

Any change must describe semantic compatibility, affected ADW decisions, aggregate ownership, authority implications, data and history migration, API impact, event compatibility, and audit preservation.
